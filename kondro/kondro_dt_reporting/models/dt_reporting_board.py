# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class KondroDtReportingBoard(models.Model):
    _name = "kondro.dt.reporting.board"
    _description = "Tableau de bord DT"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True, tracking=True)
    sequence = fields.Integer(default=10)
    description = fields.Text()
    active = fields.Boolean(default=True)
    owner_id = fields.Many2one("res.users", string="Responsable", default=lambda self: self.env.user)
    config_ids = fields.Many2many("kondro.dt.report.config", string="KPIs inclus")
    snapshot_ids = fields.Many2many("kondro.dt.kpi.snapshot", string="Relevés", compute="_compute_snapshot_ids", store=False)
    snapshot_count = fields.Integer(compute="_compute_snapshot_ids")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)

    def _compute_snapshot_ids(self):
        for board in self:
            if not board.config_ids:
                board.snapshot_ids = False
                board.snapshot_count = 0
                continue
            snapshots = self.env["kondro.dt.kpi.snapshot"].search([
                ("config_id", "in", board.config_ids.ids)
            ], limit=60, order="period_end desc")
            board.snapshot_ids = snapshots
            board.snapshot_count = len(snapshots)

    def action_refresh_snapshots(self):
        self.ensure_one()
        self.config_ids.action_compute_snapshot()
        return {
            "type": "ir.actions.act_window",
            "name": _("KPIs"),
            "res_model": "kondro.dt.kpi.snapshot",
            "view_mode": "graph,tree",
            "domain": [("config_id", "in", self.config_ids.ids)],
            "context": {"search_default_group_by_config_id": 1},
        }
