# -*- coding: utf-8 -*-
from odoo import api, fields, models


class KondroDtDocumentCategory(models.Model):
    _name = "kondro.dt.document.category"
    _description = "Catégorie documentaire DT"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    description = fields.Text()
    active = fields.Boolean(default=True)
    color = fields.Integer()
    document_count = fields.Integer(compute="_compute_document_count")

    def _compute_document_count(self):
        Document = self.env["kondro.dt.document"]
        for category in self:
            category.document_count = Document.search_count([("category_id", "=", category.id)])

    def action_open_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": self.name,
            "res_model": "kondro.dt.document",
            "view_mode": "kanban,tree,form",
            "domain": [("category_id", "=", self.id)],
            "context": {"default_category_id": self.id},
        }
