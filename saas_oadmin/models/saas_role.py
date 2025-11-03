# -*- coding: utf-8 -*-

"""
Modèle de rôles pour gestion des permissions
"""

from odoo import models, fields, api


class SaasRole(models.Model):
    """Rôle SaaS personnalisable"""
    
    _name = 'saas.role'
    _description = 'SaaS Role'
    
    name = fields.Char(string='Role Name', required=True)
    code = fields.Char(string='Role Code', required=True, unique=True)
    
    permission_ids = fields.Many2many(
        'saas.permission',
        'saas_role_permission_rel',
        'role_id',
        'permission_id',
        string='Permissions'
    )
    
    user_ids = fields.Many2many(
        'res.users',
        'saas_user_role_rel',
        'role_id',
        'user_id',
        string='Users'
    )
    
    user_count = fields.Integer(string='User Count', compute='_compute_user_count')
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Role code must be unique!'),
    ]
    
    def _compute_user_count(self):
        for role in self:
            role.user_count = len(role.user_ids)

