# -*- coding: utf-8 -*-
import logging
import operator
import json
from odoo.http import request
from odoo import models, fields, api, tools, _
from odoo.tools import convert

_logger = logging.getLogger(__name__)

class IrUiMenu(models.Model):
	_inherit = 'ir.ui.menu'

	use_font_icon = fields.Boolean("Use Font Icon", compute='_compute_use_font_icon')

	def _compute_use_font_icon(self):
		for record in self:
			record.use_font_icon = self.env['res.config.settings'].default_get('default_use_font_icon').get('default_use_font_icon')


class Http(models.AbstractModel):
	_inherit = 'ir.http'

	def webclient_rendering_context(self):
		result = super(Http, self).webclient_rendering_context()
		res_config = request.env['res.config.settings'].sudo().default_get('default_use_font_icon')
		if res_config.get('default_use_font_icon'):
			result['use_font_icon'] = res_config.get('default_use_font_icon')

		return result
