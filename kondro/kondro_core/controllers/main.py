# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class KondroCRMController(http.Controller):
    """Contrôleur pour les vues CRM et API"""

    @http.route('/kondro/crm/dashboard', type='http', auth='user', website=True)
    def crm_dashboard(self):
        """Dashboard CRM principal"""
        return request.render('kondro_core.crm_dashboard_view', {})

