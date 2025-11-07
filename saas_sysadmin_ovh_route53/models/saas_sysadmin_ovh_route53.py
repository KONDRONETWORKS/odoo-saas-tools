# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

try:
    import ovh
except ImportError:
    _logger.critical('SAAS OVH Route53 Requires the python library ovh which is not found on your installation')
    ovh = None


def _get_ovh_client(env):
    """Retourne un client OVH configuré"""
    if not ovh:
        raise UserError('Module ovh non installé. Installez-le avec: pip install ovh')
    
    ir_params = env['ir.config_parameter']
    application_key = ir_params.sudo().get_param('saas_sysadmin_ovh.application_key')
    application_secret = ir_params.sudo().get_param('saas_sysadmin_ovh.application_secret')
    consumer_key = ir_params.sudo().get_param('saas_sysadmin_ovh.consumer_key')
    endpoint = ir_params.sudo().get_param('saas_sysadmin_ovh.endpoint', 'ovh-eu')
    
    if not all([application_key, application_secret, consumer_key]):
        raise UserError('Veuillez configurer les identifiants OVH dans Paramètres > SaaS Server > OVH Configuration')
    
    return ovh.Client(
        endpoint=endpoint,
        application_key=application_key,
        application_secret=application_secret,
        consumer_key=consumer_key
    )


class SaasOvhZone(models.Model):
    """Zone DNS OVH"""
    _name = 'saas_sysadmin.ovh.zone'
    _description = 'SaaS OVH DNS Zone'

    name = fields.Char('Nom de domaine', required=True, help="Exemple: example.com")
    zone_name = fields.Char('Zone OVH', readonly=True, help="Nom technique de la zone dans OVH")
    active = fields.Boolean('Active', default=True)

    @api.model_create_multi
    def create(self, vals_list):
        zones = super().create(vals_list)
        for zone in zones:
            zone._sync_ovh_zone()
        return zones

    def _sync_ovh_zone(self):
        """Synchronise la zone avec OVH"""
        try:
            client = _get_ovh_client(self.env)
            # Vérifier si la zone existe
            zones = client.get('/domain/zone')
            if self.name not in zones:
                _logger.warning(f'Zone DNS {self.name} non trouvée dans OVH')
            else:
                self.zone_name = self.name
        except Exception as e:
            _logger.exception(f'Erreur lors de la synchronisation de la zone {self.name}: {e}')


class SaasPortalServer(models.Model):
    _inherit = 'saas_portal.server'

    ovh_zone_id = fields.Many2one(
        'saas_sysadmin.ovh.zone',
        string='Zone DNS OVH',
        help="Zone DNS OVH à utiliser pour créer les enregistrements DNS"
    )

    def _update_ovh_dns(self, subdomain, value=None, action='add', record_type='A', ttl=300):
        """
        Ajoute, met à jour ou supprime un enregistrement DNS OVH
        
        :param subdomain: Sous-domaine (ex: client-001)
        :param value: Valeur de l'enregistrement (IP pour A, domaine pour CNAME)
        :param action: 'add', 'update', 'delete'
        :param record_type: 'A', 'CNAME', 'TXT', 'MX'
        :param ttl: TTL en secondes
        """
        if not self.ovh_zone_id:
            return False
        
        if action in ('add', 'update') and not value:
            raise UserError('Cette opération nécessite une valeur')
        
        try:
            client = _get_ovh_client(self.env)
            zone_name = self.ovh_zone_id.name
            
            # Construire le nom complet
            if subdomain:
                full_name = f'{subdomain}.{zone_name}'
            else:
                full_name = zone_name
            
            if action == 'add':
                # Créer l'enregistrement
                client.post(
                    f'/domain/zone/{zone_name}/record',
                    fieldType=record_type,
                    subDomain=subdomain or '',
                    target=value,
                    ttl=ttl
                )
                # Déclencher la validation de la zone
                client.post(f'/domain/zone/{zone_name}/refresh')
                _logger.info(f'Enregistrement DNS créé: {full_name} -> {value} ({record_type})')
                
            elif action == 'update':
                # Trouver l'enregistrement existant
                records = client.get(f'/domain/zone/{zone_name}/record', fieldType=record_type, subDomain=subdomain or '')
                if records:
                    record_id = records[0]
                    client.put(
                        f'/domain/zone/{zone_name}/record/{record_id}',
                        target=value,
                        ttl=ttl
                    )
                    client.post(f'/domain/zone/{zone_name}/refresh')
                    _logger.info(f'Enregistrement DNS mis à jour: {full_name} -> {value}')
                else:
                    # Créer si n'existe pas
                    self._update_ovh_dns(subdomain, value, 'add', record_type, ttl)
                    
            elif action == 'delete':
                # Trouver et supprimer l'enregistrement
                records = client.get(f'/domain/zone/{zone_name}/record', fieldType=record_type, subDomain=subdomain or '')
                for record_id in records:
                    client.delete(f'/domain/zone/{zone_name}/record/{record_id}')
                if records:
                    client.post(f'/domain/zone/{zone_name}/refresh')
                    _logger.info(f'Enregistrement DNS supprimé: {full_name}')
                    
        except Exception as e:
            _logger.exception(f'Erreur lors de la modification DNS OVH pour {subdomain}: {e}')
            raise UserError(f'Erreur DNS OVH: {e}')

    @api.model_create_multi
    def create(self, vals_list):
        servers = super().create(vals_list)
        for server in servers:
            if server.ovh_zone_id and server.local_host:
                # Créer l'enregistrement DNS A pour le serveur
                server._update_ovh_dns(
                    server.name,
                    value=server.local_host,
                    action='add',
                    record_type='A'
                )
        return servers

    def write(self, vals):
        super().write(vals)
        for server in self:
            if server.ovh_zone_id:
                if 'local_host' in vals:
                    # Mettre à jour l'enregistrement DNS
                    server._update_ovh_dns(
                        server.name,
                        value=server.local_host,
                        action='update',
                        record_type='A'
                    )
        return True


class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'

    def _create_new_database(self, **kwargs):
        """Override pour créer l'enregistrement DNS après création de la base"""
        result = super()._create_new_database(**kwargs)
        
        # Créer l'enregistrement DNS si configuré
        if self.server_id.ovh_zone_id:
            root_domain = self.env['ir.config_parameter'].sudo().get_param(
                'saas_sysadmin_ovh.root_domain', ''
            )
            if root_domain:
                # Extraire le sous-domaine depuis self.host
                subdomain = self.host.split('.')[0] if '.' in self.host else self.host
                # Créer l'enregistrement CNAME ou A
                self.server_id._update_ovh_dns(
                    subdomain,
                    value=self.server_id.local_host or self.server_id.host,
                    action='add',
                    record_type='A'
                )
        
        return result

    def unlink(self):
        """Supprimer les enregistrements DNS lors de la suppression"""
        for client in self:
            if client.server_id.ovh_zone_id:
                root_domain = self.env['ir.config_parameter'].sudo().get_param(
                    'saas_sysadmin_ovh.root_domain', ''
                )
                if root_domain:
                    subdomain = client.host.split('.')[0] if '.' in client.host else client.host
                    client.server_id._update_ovh_dns(
                        subdomain,
                        action='delete',
                        record_type='A'
                    )
        return super().unlink()

