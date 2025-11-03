# -*- coding: utf-8 -*-

"""
Modèle utilisateur optimisé avec rôles et permissions étendus
"""

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _
import logging

_logger = logging.getLogger(__name__)


class ResUsersOptimized(models.Model):
    """
    Utilisateurs SaaS avec fonctionnalités étendues
    """
    _name = 'res.users'
    _inherit = ['res.users', 'saas.base']
    
    # Rôles
    saas_role_ids = fields.Many2many(
        'saas.role',
        'saas_user_role_rel',
        'user_id',
        'role_id',
        string='SaaS Roles',
        help='Roles assigned to this user'
    )
    
    saas_role_name = fields.Char(string='Primary Role', compute='_compute_primary_role')
    
    # Permissions
    saas_permissions = fields.Text(string='Permissions Summary', compute='_compute_permissions')
    
    # Audit
    last_login_ip = fields.Char(string='Last Login IP')
    login_count = fields.Integer(string='Login Count', default=0)
    last_action_date = fields.Datetime(string='Last Action')
    
    # Restrictions
    can_create_instances = fields.Boolean(string='Can Create Instances', default=False)
    can_delete_instances = fields.Boolean(string='Can Delete Instances', default=False)
    max_instances_allowed = fields.Integer(string='Max Instances Allowed', default=0)
    
    @api.depends('saas_role_ids')
    def _compute_primary_role(self):
        """Calculer le rôle principal"""
        for user in self:
            if user.saas_role_ids:
                user.saas_role_name = user.saas_role_ids[0].name
            else:
                user.saas_role_name = 'No Role'
    
    @api.depends('saas_role_ids', 'saas_role_ids.permission_ids')
    def _compute_permissions(self):
        """Calculer le résumé des permissions"""
        for user in self:
            permissions = user.saas_role_ids.mapped('permission_ids')
            permission_names = permissions.mapped('name')
            user.saas_permissions = ', '.join(permission_names) if permission_names else 'No permissions'
    
    def has_permission(self, permission_code):
        """Vérifier si l'utilisateur a une permission"""
        self.ensure_one()
        
        # Super admin a toutes les permissions
        if self.has_group('base.group_system'):
            return True
        
        # Vérifier les permissions via les rôles
        permissions = self.saas_role_ids.mapped('permission_ids')
        return permission_code in permissions.mapped('code')
    
    def can_access_model(self, model_name):
        """Vérifier l'accès à un modèle"""
        self.ensure_one()
        return self.has_group('base.group_system') or self.has_permission(f'model.{model_name}')


class SaasRole(models.Model):
    """
    Rôles SaaS personnalisables
    """
    _name = 'saas.role'
    _description = 'SaaS Role'
    _inherit = 'saas.base'
    
    name = fields.Char(string='Role Name', required=True)
    code = fields.Char(string='Role Code', required=True, unique=True)
    
    # Permissions
    permission_ids = fields.Many2many(
        'saas.permission',
        'saas_role_permission_rel',
        'role_id',
        'permission_id',
        string='Permissions'
    )
    
    # Utilisateurs
    user_ids = fields.Many2many(
        'res.users',
        'saas_user_role_rel',
        'role_id',
        'user_id',
        string='Users'
    )
    
    user_count = fields.Integer(string='User Count', compute='_compute_user_count')
    
    # Description
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Role code must be unique!'),
    ]
    
    def _compute_user_count(self):
        """Calculer le nombre d'utilisateurs"""
        for role in self:
            role.user_count = len(role.user_ids)


class SaasPermission(models.Model):
    """
    Permissions granulaires pour le système SaaS
    """
    _name = 'saas.permission'
    _description = 'SaaS Permission'
    _inherit = 'saas.base'
    
    name = fields.Char(string='Permission Name', required=True)
    code = fields.Char(string='Permission Code', required=True, unique=True)
    
    # Type de permission
    permission_type = fields.Selection([
        ('model', 'Model Access'),
        ('action', 'Action'),
        ('menu', 'Menu'),
        ('api', 'API Endpoint'),
    ], string='Permission Type', required=True)
    
    # Détails
    resource_id = fields.Char(string='Resource ID', help='Model name, action ID, etc.')
    
    # Rôles
    role_ids = fields.Many2many(
        'saas.role',
        'saas_role_permission_rel',
        'permission_id',
        'role_id',
        string='Roles'
    )
    
    # Description
    description = fields.Text(string='Description')
    
    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Permission code must be unique!'),
    ]


class SaasAudit(models.Model):
    """
    Journal d'audit pour traçabilité
    """
    _name = 'saas.audit'
    _description = 'SaaS Audit Trail'
    _order = 'timestamp desc'
    
    # Informations de base
    action = fields.Char(string='Action', required=True)
    model = fields.Char(string='Model')
    record_id = fields.Integer(string='Record ID')
    
    # Utilisateur
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user)
    user_ip = fields.Char(string='User IP')
    
    # Timestamp
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, required=True)
    
    # Détails
    details = fields.Text(string='Details')
    old_values = fields.Text(string='Old Values')
    new_values = fields.Text(string='New Values')
    
    # Sécurité
    is_security_event = fields.Boolean(string='Security Event')
    
    @api.model
    def log_action(self, action, model=None, record_id=None, details=None, security=False):
        """Logger une action dans l'audit trail"""
        self.create({
            'action': action,
            'model': model,
            'record_id': record_id,
            'user_id': self.env.user.id,
            'details': details,
            'is_security_event': security,
        })

