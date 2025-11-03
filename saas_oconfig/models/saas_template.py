# -*- coding: utf-8 -*-

"""
Configuration des templates et versions SaaS
"""

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class SaasOptimizedTemplate(models.Model):
    """Template de base de données SaaS"""
    
    _name = 'saas.otemplate'
    _description = 'SaaS Template'
    _inherit = 'saas.base'
    
    code = fields.Char(string='Template Code', required=True, unique=True)
    odoo_version = fields.Char(string='Odoo Version', required=True)
    modules_to_install = fields.Text(string='Modules to Install', help='Comma-separated list')
    is_active = fields.Boolean(string='Active', default=True)


class SaasOptimizedVersion(models.Model):
    """Version d'Odoo supportée"""
    
    _name = 'saas.oversion'
    _description = 'Odoo Version'
    
    name = fields.Char(string='Version Name', required=True, unique=True)
    code = fields.Char(string='Version Code', required=True, unique=True)
    is_active = fields.Boolean(string='Active', default=True)

