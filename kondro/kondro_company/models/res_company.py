# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _setup_kondronetworks_company(self):
        """Configure l'entreprise KONDRONETWORKS avec les paramètres de la Côte d'Ivoire"""
        # Récupérer ou créer l'entreprise principale
        company = self.env['res.company'].search([('name', '=', 'KONDRONETWORKS')], limit=1)
        
        if not company:
            company = self.env['res.company'].create({
                'name': 'KONDRONETWORKS',
                'country_id': self.env.ref('base.ci').id,  # Côte d'Ivoire
                'currency_id': self.env.ref('base.XOF').id,  # Franc CFA
                'phone': '+225 XX XX XX XX XX',
                'email': 'contact@kondronetworks.com',
                'website': 'https://www.kondronetworks.com',
                'vat': 'CIXXXXXXXXX',  # Numéro d'identification fiscale
                'street': 'Abidjan, Côte d\'Ivoire',
                'city': 'Abidjan',
                'zip': '01 BP',
                'state_id': False,
            })
            _logger.info("✅ Entreprise KONDRONETWORKS créée")
        else:
            # Mettre à jour les informations si nécessaire
            company.write({
                'country_id': self.env.ref('base.ci').id,
                'currency_id': self.env.ref('base.XOF').id,
            })
            _logger.info("✅ Entreprise KONDRONETWORKS mise à jour")
        
        return company

