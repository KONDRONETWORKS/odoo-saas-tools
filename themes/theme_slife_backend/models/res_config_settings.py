# -*- coding: utf-8 -*-
import logging
import operator
from odoo import models, fields, api, tools, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_use_font_icon = fields.Boolean("Use Font Icon", default_model='ir.ui.menu')
