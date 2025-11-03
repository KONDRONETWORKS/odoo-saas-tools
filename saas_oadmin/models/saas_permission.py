# -*- coding: utf-8 -*-

"""
Modèle de permissions granulaires
"""

from odoo import models, fields


class SaasPermission(models.Model):
    """Permission SaaS granulaire"""
    
    _name = 'saas.permission'
    _description = 'SaaS Permission'
    
    name = fields.Char(string='Permission Name', required=True)
    code = fields.Char(string='Permission Code', required=True, unique=True)
    
    permission_type = fields.Selection([
        ('model', 'Model Access'),
        ('action', 'Action'),
        ('menu', 'Menu'),
        ('api', 'API Endpoint'),
    ], string='Permission Type', required=True)
    
    resource_id = fields.Char(string='Resource ID')
    
    role_ids = fields.Many2many(
        'saas.role',
        'saas_role_permission_rel',
        'permission_id',
        'role_id',
        string='Roles'
    )
    
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Permission code must be unique!'),
    ]

