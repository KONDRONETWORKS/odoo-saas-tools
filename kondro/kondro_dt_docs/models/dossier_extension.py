# -*- coding: utf-8 -*-
from odoo import fields, models, _


class KondroCommercialDossier(models.Model):
    _inherit = "kondro.commercial.dossier"

    dt_document_ids = fields.One2many("kondro.dt.document", "dossier_id", string="Documents DT")
    dt_document_count = fields.Integer(compute="_compute_dt_document_count", string="Documents DT")

    def _compute_dt_document_count(self):
        for dossier in self:
            dossier.dt_document_count = len(dossier.dt_document_ids)

    def action_open_dt_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Documents du dossier"),
            "res_model": "kondro.dt.document",
            "view_mode": "kanban,tree,form",
            "domain": [("dossier_id", "=", self.id)],
            "context": {"default_dossier_id": self.id},
        }
