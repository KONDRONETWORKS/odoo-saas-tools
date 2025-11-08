# -*- coding: utf-8 -*-
from odoo import fields, models, _


class KondroProject(models.Model):
    _inherit = "kondro.project"

    dt_document_ids = fields.One2many("kondro.dt.document", "project_id", string="Documents DT")
    dt_document_count = fields.Integer(compute="_compute_dt_document_count", string="Documents DT")

    def _compute_dt_document_count(self):
        for project in self:
            project.dt_document_count = len(project.dt_document_ids)

    def action_open_dt_documents(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Documents du projet"),
            "res_model": "kondro.dt.document",
            "view_mode": "kanban,tree,form",
            "domain": [("project_id", "=", self.id)],
            "context": {
                "default_project_id": self.id,
            },
        }
