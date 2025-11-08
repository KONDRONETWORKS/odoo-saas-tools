# -*- coding: utf-8 -*-
from odoo import api, fields, models


class KondroProject(models.Model):
    _inherit = "kondro.project"

    dt_matrix_id = fields.Many2one(
        "kondro.dt.workflow.matrix",
        string="Matrice DT par défaut",
        domain="[('process_type', '=', 'commercial_expense')]",
        help="Matrice RACI appliquée par défaut aux dépenses liées à ce projet.",
    )
    dt_escalation_user_id = fields.Many2one("res.users", string="Contact escalade DT")
    dt_workflow_note = fields.Text(string="Consignes workflow DT")

    @api.model
    def create(self, vals):
        dossier_id = vals.get("commercial_dossier_id")
        if not vals.get("dt_matrix_id") and dossier_id:
            dossier = self.env["kondro.commercial.dossier"].browse(dossier_id)
            if dossier and dossier.dt_matrix_id:
                vals["dt_matrix_id"] = dossier.dt_matrix_id.id
        return super().create(vals)

    def write(self, vals):
        if self.env.context.get("skip_dt_matrix_auto"):
            return super().write(vals)
        res = super().write(vals)
        if "commercial_dossier_id" in vals and not vals.get("dt_matrix_id"):
            to_update = self.filtered(
                lambda p: p.commercial_dossier_id and p.commercial_dossier_id.dt_matrix_id and not p.dt_matrix_id
            )
            for project in to_update:
                project.with_context(skip_dt_matrix_auto=True).write(
                    {"dt_matrix_id": project.commercial_dossier_id.dt_matrix_id.id}
                )
        return res

    @api.onchange("commercial_dossier_id")
    def _onchange_commercial_dossier_id(self):
        if self.commercial_dossier_id and self.commercial_dossier_id.dt_matrix_id:
            self.dt_matrix_id = self.commercial_dossier_id.dt_matrix_id

    def action_open_dt_matrix(self):
        self.ensure_one()
        if self.dt_matrix_id:
            return {
                "type": "ir.actions.act_window",
                "name": self.dt_matrix_id.name,
                "res_model": "kondro.dt.workflow.matrix",
                "res_id": self.dt_matrix_id.id,
                "view_mode": "form",
            }
        return False


class KondroCommercialDossier(models.Model):
    _inherit = "kondro.commercial.dossier"

    dt_matrix_id = fields.Many2one("kondro.dt.workflow.matrix", string="Matrice DT", help="Pour préconfigurer les projets issus de ce dossier.")

    def action_open_dt_matrix(self):
        self.ensure_one()
        if self.dt_matrix_id:
            return {
                "type": "ir.actions.act_window",
                "name": self.dt_matrix_id.name,
                "res_model": "kondro.dt.workflow.matrix",
                "res_id": self.dt_matrix_id.id,
                "view_mode": "form",
            }
        return False
