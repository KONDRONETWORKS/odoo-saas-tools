# -*- coding: utf-8 -*-
from odoo import fields, models


class KondroDtKpiSnapshot(models.Model):
    _name = "kondro.dt.kpi.snapshot"
    _description = "Snapshot KPI DT"
    _order = "period_end desc, config_id, id desc"

    config_id = fields.Many2one("kondro.dt.report.config", string="KPI", required=True, ondelete="cascade")
    name = fields.Char(related="config_id.name", store=True, readonly=True)
    code = fields.Char(related="config_id.code", store=True, readonly=True)
    value = fields.Float(string="Valeur", digits="Product Price")
    delta_value = fields.Float(string="Delta")
    delta_percent = fields.Float(string="Delta %")
    target_value = fields.Float(related="config_id.target_value", store=True, readonly=True)
    unit_label = fields.Char(related="config_id.unit_label", store=True, readonly=True)
    currency_id = fields.Many2one(related="config_id.currency_id", store=True, readonly=True)
    periodicity = fields.Selection(
        [("daily", "Quotidien"), ("weekly", "Hebdomadaire"), ("monthly", "Mensuel")],
        store=True,
        readonly=True,
    )
    period_start = fields.Date(string="Début période")
    period_end = fields.Date(string="Fin période")
    computed_at = fields.Datetime(string="Calculé le", default=fields.Datetime.now, readonly=True)
    previous_snapshot_id = fields.Many2one("kondro.dt.kpi.snapshot", string="Précédent", readonly=True)
    board_ids = fields.Many2many("kondro.dt.reporting.board", string="Tableaux", copy=False)
    notes = fields.Text(string="Commentaires")

    def action_view_details(self):
        self.ensure_one()
        action = (
            self.config_id.model_id.get_formview_action()
            if hasattr(self.config_id.model_id, "get_formview_action")
            else None
        )
        domain = self.config_id._compute_domain(self.period_start, self.period_end)
        if not action:
            return {
                "type": "ir.actions.act_window",
                "name": self.config_id.name,
                "res_model": self.config_id.model_name,
                "view_mode": "tree,form",
                "domain": domain,
            }
        action = dict(action)
        action["domain"] = domain
        action.setdefault("view_mode", "tree,form")
        return action
