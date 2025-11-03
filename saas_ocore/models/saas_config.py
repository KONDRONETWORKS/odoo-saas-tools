# -*- coding: utf-8 -*-

"""
Configuration système centralisée pour le SaaS
"""

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaasConfig(models.Model):
    """
    Configuration système centralisée
    """
    _name = 'saas.config'
    _description = 'SaaS Configuration'
    _order = 'key'
    
    key = fields.Char(string='Configuration Key', required=True, unique=True, index=True)
    value = fields.Text(string='Value', required=True)
    description = fields.Text(string='Description')
    is_sensitive = fields.Boolean(string='Sensitive Data', help='Hide in logs')
    active = fields.Boolean(string='Active', default=True)
    
    _sql_constraints = [
        ('key_unique', 'UNIQUE(key)', 'Configuration key must be unique!'),
    ]
    
    @api.model
    def get(self, key, default=None):
        """Récupérer une configuration par clé"""
        config = self.search([('key', '=', key), ('active', '=', True)], limit=1)
        if config:
            return config.value
        return default
    
    @api.model
    def set(self, key, value, description=None):
        """Définir une configuration"""
        config = self.search([('key', '=', key)], limit=1)
        if config:
            config.write({'value': value})
        else:
            self.create({
                'key': key,
                'value': value,
                'description': description or f"Configuration for {key}",
            })
    
    @api.model
    def get_int(self, key, default=0):
        """Récupérer une configuration comme entier"""
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    @api.model
    def get_float(self, key, default=0.0):
        """Récupérer une configuration comme float"""
        value = self.get(key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    @api.model
    def get_bool(self, key, default=False):
        """Récupérer une configuration comme booléen"""
        value = self.get(key, str(default))
        return value.lower() in ('true', '1', 'yes', 'on')


class SaasSystemSettings(models.TransientModel):
    """
    Paramètres système pour le SaaS
    """
    _name = 'saas.system.settings'
    _description = 'SaaS System Settings'
    _inherit = 'res.config.settings'
    
    # Configuration générale
    base_domain = fields.Char(string='Base Domain', required=True, config_parameter='saas.base_domain')
    default_trial_days = fields.Integer(string='Default Trial Days', default=14, config_parameter='saas.default_trial_days')
    auto_suspend_expired = fields.Boolean(string='Auto Suspend Expired', default=True, config_parameter='saas.auto_suspend_expired')
    
    # Limites par défaut
    max_users_default = fields.Integer(string='Default Max Users', default=5, config_parameter='saas.max_users_default')
    max_storage_gb_default = fields.Float(string='Default Max Storage (GB)', default=10, config_parameter='saas.max_storage_gb_default')
    
    # Notifications
    notify_expiration_days = fields.Integer(string='Notify Before Expiration (Days)', default=7, config_parameter='saas.notify_expiration_days')
    notify_admins_on_error = fields.Boolean(string='Notify Admins on Errors', default=True, config_parameter='saas.notify_admins_on_error')
    
    # OAuth
    oauth_token_expiry = fields.Integer(string='OAuth Token Expiry (Hours)', default=24, config_parameter='saas.oauth_token_expiry')
    
    def set_values(self):
        """Enregistrer les valeurs"""
        super().set_values()
        _logger.info("SaaS system settings updated")

