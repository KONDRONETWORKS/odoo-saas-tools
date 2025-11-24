# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    background_image = fields.Binary(
        string="Image de Fond",
        help="Image de fond utilisée par le personnalisateur de thème"
    )
