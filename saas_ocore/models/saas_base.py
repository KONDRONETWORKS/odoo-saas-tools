# -*- coding: utf-8 -*-

"""
Module de base optimisé pour le système SaaS
"""

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaasBaseModel(models.AbstractModel):
    """
    Modèle abstrait de base pour tous les modèles SaaS
    
    Fournit des fonctionnalités communes :
    - Audit trail automatique
    - Logging des modifications
    - Validation des données
    - Gestion des permissions
    """
    _name = 'saas.base'
    _description = 'Base SaaS Model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    
    # Champs standards
    name = fields.Char(string='Name', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    description = fields.Text(string='Description')
    notes = fields.Html(string='Notes')
    
    # Métadonnées
    created_by = fields.Many2one(
        'res.users', 
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True
    )
    created_on = fields.Datetime(string='Created On', default=fields.Datetime.now, readonly=True)
    updated_by = fields.Many2one('res.users', string='Updated By', readonly=True)
    updated_on = fields.Datetime(string='Updated On', readonly=True)
    
    # État
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('archived', 'Archived'),
    ], string='State', default='draft', tracking=True)
    
    def write(self, vals):
        """Override write pour tracker les modifications"""
        if 'state' not in vals:
            vals['updated_by'] = self.env.user.id
            vals['updated_on'] = fields.Datetime.now()
        return super().write(vals)
    
    def archive(self):
        """Archiver un enregistrement"""
        self.write({'state': 'archived', 'active': False})
    
    def activate(self):
        """Activer un enregistrement"""
        self.write({'state': 'active', 'active': True})
    
    def suspend(self):
        """Suspension temporaire"""
        self.write({'state': 'suspended'})


class SaasClientBase(SaasBaseModel):
    """
    Modèle abstrait pour les clients SaaS
    
    Fournit les fonctionnalités communes aux clients :
    - Gestion d'expiration
    - Limites et quotas
    - Suivi des ressources
    """
    _name = 'saas.client.base'
    _description = 'Base Client SaaS Model'
    _inherit = 'saas.base'
    
    # Configuration client
    trial = fields.Boolean(string='Trial', default=False, tracking=True)
    expiration_date = fields.Datetime(string='Expiration Date', tracking=True)
    is_expired = fields.Boolean(string='Expired', compute='_compute_expiration')
    
    # Limites
    max_users = fields.Integer(string='Maximum Users', default=0)
    max_storage_gb = fields.Float(string='Maximum Storage (GB)', default=0)
    block_on_expiration = fields.Boolean(string='Block on Expiration', default=False)
    
    def _compute_expiration(self):
        """Calculer si l'instance est expirée"""
        for record in self:
            if record.expiration_date:
                record.is_expired = fields.Datetime.now() > record.expiration_date
            else:
                record.is_expired = False
    
    def check_expiration(self):
        """Vérifier l'expiration et bloquer si nécessaire"""
        if self.is_expired and self.block_on_expiration:
            from odoo.addons.saas_ocore.exceptions import SuspendedInstanceException
            raise SuspendedInstanceException("This instance has expired")


class SaasServerBase(SaasBaseModel):
    """
    Modèle abstrait pour les serveurs SaaS
    
    Fournit les fonctionnalités communes aux serveurs :
    - Configuration OAuth
    - Gestion des connexions
    - Monitoring
    """
    _name = 'saas.server.base'
    _description = 'Base Server SaaS Model'
    _inherit = 'saas.base'
    
    # Configuration serveur
    host = fields.Char(string='Host', required=True)
    port = fields.Integer(string='Port', default=8069)
    scheme = fields.Selection([
        ('http', 'HTTP'),
        ('https', 'HTTPS'),
    ], string='Scheme', default='https', required=True)
    
    # OAuth
    oauth_enabled = fields.Boolean(string='OAuth Enabled', default=True)
    oauth_application_id = fields.Many2one('oauth.application', string='OAuth Application')
    
    # État
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('maintenance', 'Maintenance'),
        ('down', 'Down'),
    ], string='State', default='draft')
    
    # Capacité
    max_instances = fields.Integer(string='Maximum Instances', default=0)
    current_instances = fields.Integer(string='Current Instances', compute='_compute_instances')
    
    def _compute_instances(self):
        """Calculer le nombre d'instances actuelles"""
        for server in self:
            # À implémenter selon les relations réelles
            server.current_instances = 0
    
    def check_capacity(self):
        """Vérifier la capacité du serveur"""
        if self.max_instances and self.current_instances >= self.max_instances:
            from odoo.addons.saas_ocore.exceptions import CapacityExceededException
            raise CapacityExceededException("Server at maximum capacity")

