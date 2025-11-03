# -*- coding: utf-8 -*-

"""
Contrôleurs pour l'API d'administration
"""

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class SaasAdminController(http.Controller):
    """Contrôleur d'administration SaaS"""
    
    @http.route('/saas_api/admin/users', type='json', auth='user')
    def get_users(self):
        """Récupérer la liste des utilisateurs"""
        users = request.env['res.users'].search([])
        return {
            'users': users.read(['id', 'name', 'login', 'saas_role_name']),
        }
    
    @http.route('/saas_api/admin/roles', type='json', auth='user')
    def get_roles(self):
        """Récupérer la liste des rôles"""
        roles = request.env['saas.role'].search([])
        return {
            'roles': roles.read(['id', 'name', 'code', 'user_count']),
        }
    
    @http.route('/saas_api/admin/stats', type='json', auth='user')
    def get_stats(self):
        """Récupérer les statistiques admin"""
        return {
            'total_users': 0,
            'total_instances': 0,
            'active_instances': 0,
        }
