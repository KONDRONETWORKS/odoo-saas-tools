# -*- coding: utf-8 -*-
from odoo import fields, models


class KondroDtDocumentTag(models.Model):
    _name = "kondro.dt.document.tag"
    _description = "Tag documentaire DT"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    color = fields.Integer()
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
