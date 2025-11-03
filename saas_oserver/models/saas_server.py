# -*- coding: utf-8 -*-

"""
Gestion des serveurs et bases de données SaaS optimisées
"""

from odoo import models, fields, api
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class SaasOptimizedServer(models.Model):
    """
    Serveur SaaS avec OAuth et gestion de capacité
    """
    _name = 'saas.oserver'
    _description = 'SaaS Server'
    _inherit = 'saas.server.base'
    
    # Configuration OAuth
    oauth_application_id = fields.Many2one('oauth.application', string='OAuth Application', required=True)
    
    # Capacité
    max_instances = fields.Integer(string='Max Instances', default=100)
    current_instances = fields.Integer(string='Current Instances', compute='_compute_instances')
    
    # Instances
    instance_ids = fields.One2many('saas.oinstance', 'server_id', string='Instances')
    
    # Monitoring
    last_check = fields.Datetime(string='Last Health Check')
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('degraded', 'Degraded'),
        ('down', 'Down'),
    ], string='Health Status', default='healthy')
    
    def _compute_instances(self):
        """Calculer le nombre d'instances"""
        for server in self:
            server.current_instances = len(server.instance_ids.filtered(lambda i: i.state != 'deleted'))
    
    def check_capacity(self):
        """Vérifier la capacité"""
        if self.max_instances and self.current_instances >= self.max_instances:
            from odoo.addons.saas_ocore.exceptions import CapacityExceededException
            raise CapacityExceededException()
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create pour OAuth app"""
        for vals in vals_list:
            if 'oauth_application_id' not in vals or not vals.get('oauth_application_id'):
                oauth_app = self.env['oauth.application'].sudo().create({})
                vals['oauth_application_id'] = oauth_app.id
        return super().create(vals_list)


class SaasOptimizedDatabase(models.Model):
    """
    Gestion de création des bases de données
    """
    _name = 'saas.odatabase'
    _description = 'SaaS Database Manager'
    
    name = fields.Char(string='Database Name', required=True)
    server_id = fields.Many2one('saas.oserver', string='Server', required=True)
    
    # Configuration
    db_template = fields.Char(string='Template DB', default='template1')
    odoo_version = fields.Char(string='Odoo Version', default='18.0')
    admin_password = fields.Char(string='Admin Password')
    
    # État
    state = fields.Selection([
        ('draft', 'Draft'),
        ('creating', 'Creating'),
        ('created', 'Created'),
        ('error', 'Error'),
    ], string='State', default='draft')
    
    # Métriques
    size_mb = fields.Float(string='Size (MB)', readonly=True)
    created_on = fields.Datetime(string='Created On', readonly=True)
    
    def action_create_database(self):
        """Créer la base de données"""
        self.write({'state': 'creating'})
        try:
            # À implémenter : création réelle
            self.write({
                'state': 'created',
                'created_on': fields.Datetime.now(),
            })
        except Exception as e:
            _logger.error(f"Error creating database: {e}")
            self.write({'state': 'error'})


class SaasOptimizedBackup(models.Model):
    """
    Gestion des backups
    """
    _name = 'saas.obackup'
    _description = 'SaaS Backup'
    
    name = fields.Char(string='Backup Name', required=True)
    instance_id = fields.Many2one('saas.oinstance', string='Instance', required=True)
    
    # Configuration
    backup_type = fields.Selection([
        ('full', 'Full'),
        ('incremental', 'Incremental'),
    ], string='Backup Type', default='full')
    
    # État
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string='State', default='scheduled')
    
    # Fichier
    filename = fields.Char(string='Filename')
    size_mb = fields.Float(string='Size (MB)')
    storage_path = fields.Char(string='Storage Path')
    
    # Timestamps
    start_time = fields.Datetime(string='Start Time')
    end_time = fields.Datetime(string='End Time')
    duration_seconds = fields.Integer(string='Duration (seconds)')

