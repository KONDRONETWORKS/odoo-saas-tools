# -*- coding: utf-8 -*-

"""
Modèle d'audit trail pour traçabilité
"""

from odoo import models, fields


class SaasAudit(models.Model):
    """Journal d'audit SaaS"""
    
    _name = 'saas.audit'
    _description = 'SaaS Audit Trail'
    _order = 'timestamp desc'
    
    action = fields.Char(string='Action', required=True)
    model = fields.Char(string='Model')
    record_id = fields.Integer(string='Record ID')
    
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    user_ip = fields.Char(string='User IP')
    
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, required=True)
    
    details = fields.Text(string='Details')
    old_values = fields.Text(string='Old Values')
    new_values = fields.Text(string='New Values')
    
    is_security_event = fields.Boolean(string='Security Event')
    
    def log_action(self, action, model=None, record_id=None, details=None, security=False):
        """Logger une action"""
        self.create({
            'action': action,
            'model': model,
            'record_id': record_id,
            'user_id': self.env.user.id,
            'details': details,
            'is_security_event': security,
        })

