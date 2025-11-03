# -*- coding: utf-8 -*-

"""
Module de gestion des clients SaaS optimisé
"""

from odoo import models, fields, api
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class SaasClient(models.Model):
    """
    Client SaaS avec fonctionnalités étendues
    """
    _name = 'saas.oclient'
    _description = 'SaaS Client'
    _inherit = 'saas.client.base'
    
    # Informations client
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    email = fields.Char(string='Email', related='partner_id.email', readonly=True)
    phone = fields.Char(string='Phone', related='partner_id.phone', readonly=True)
    
    # Instances
    instance_ids = fields.One2many('saas.oinstance', 'client_id', string='Instances')
    instance_count = fields.Integer(string='Instance Count', compute='_compute_instances')
    
    # Plan
    plan_id = fields.Many2one('saas.oplan', string='Plan', required=True)
    
    # Statut commercial
    billing_status = fields.Selection([
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ], string='Billing Status', default='trial', tracking=True)
    
    # Statistiques
    total_users = fields.Integer(string='Total Users', compute='_compute_stats')
    total_storage_gb = fields.Float(string='Total Storage (GB)', compute='_compute_stats')
    last_activity = fields.Datetime(string='Last Activity', compute='_compute_stats')
    
    def _compute_instances(self):
        """Calculer le nombre d'instances"""
        for client in self:
            client.instance_count = len(client.instance_ids)
    
    def _compute_stats(self):
        """Calculer les statistiques"""
        for client in self:
            client.total_users = 0
            client.total_storage_gb = 0.0
            client.last_activity = False
            
            for instance in client.instance_ids:
                client.total_users += instance.user_count or 0
                client.total_storage_gb += instance.storage_gb or 0.0
                if instance.last_activity and (not client.last_activity or instance.last_activity > client.last_activity):
                    client.last_activity = instance.last_activity
    
    def action_view_instances(self):
        """Afficher les instances"""
        action = {
            'name': _('Instances'),
            'type': 'ir.actions.act_window',
            'res_model': 'saas.oinstance',
            'view_mode': 'list,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }
        return action
    
    def create_instance(self):
        """Créer une nouvelle instance"""
        # À implémenter
        pass


class SaasOptimizedInstance(models.Model):
    """
    Instance SaaS avec monitoring
    """
    _name = 'saas.oinstance'
    _description = 'SaaS Instance'
    _inherit = 'saas.base'
    
    # Client
    client_id = fields.Many2one('saas.oclient', string='Client', required=True)
    
    # Informations
    subdomain = fields.Char(string='Subdomain', required=True, unique=True)
    full_domain = fields.Char(string='Full Domain', compute='_compute_domain')
    
    # Serveur
    server_id = fields.Many2one('saas.oserver', string='Server')
    
    # Plan
    plan_id = fields.Many2one('saas.oplan', string='Plan', required=True)
    
    # État
    state = fields.Selection([
        ('draft', 'Draft'),
        ('creating', 'Creating'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('maintenance', 'Maintenance'),
        ('deleted', 'Deleted'),
    ], string='State', default='draft', tracking=True)
    
    # Monitoring
    user_count = fields.Integer(string='Users')
    storage_gb = fields.Float(string='Storage (GB)')
    last_activity = fields.Datetime(string='Last Activity')
    
    # Maintenance
    maintenance_mode = fields.Boolean(string='Maintenance Mode', default=False)
    maintenance_message = fields.Text(string='Maintenance Message')
    
    def _compute_domain(self):
        """Calculer le domaine complet"""
        base_domain = self.env['saas.config'].get('base_domain', 'localhost')
        for instance in self:
            instance.full_domain = f"{instance.subdomain}.{base_domain}" if instance.subdomain else ""
    
    def action_start(self):
        """Démarrer l'instance"""
        self.write({'state': 'active'})
    
    def action_suspend(self):
        """Suspendre l'instance"""
        self.write({'state': 'suspended'})
    
    def action_maintenance(self):
        """Activer le mode maintenance"""
        self.write({
            'maintenance_mode': True,
            'state': 'maintenance',
        })


class SaasOptimizedPlan(models.Model):
    """
    Plan tarifaire SaaS
    """
    _name = 'saas.oplan'
    _description = 'SaaS Plan'
    _inherit = 'saas.base'
    
    # Configuration
    code = fields.Char(string='Plan Code', required=True, unique=True)
    price_monthly = fields.Float(string='Monthly Price')
    price_yearly = fields.Float(string='Yearly Price')
    
    # Limites
    max_instances = fields.Integer(string='Max Instances', default=1)
    max_users = fields.Integer(string='Max Users', default=5)
    max_storage_gb = fields.Float(string='Max Storage (GB)', default=10)
    
    # Trial
    trial_days = fields.Integer(string='Trial Days', default=14)
    allow_trial = fields.Boolean(string='Allow Trial', default=True)
    
    # Clients
    client_ids = fields.One2many('saas.oclient', 'plan_id', string='Clients')
    client_count = fields.Integer(string='Client Count', compute='_compute_client_count')
    
    def _compute_client_count(self):
        """Calculer le nombre de clients"""
        for plan in self:
            plan.client_count = len(plan.client_ids)

