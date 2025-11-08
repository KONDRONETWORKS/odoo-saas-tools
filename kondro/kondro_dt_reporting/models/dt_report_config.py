# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _  # type: ignore
from odoo.tools.safe_eval import safe_eval  # type: ignore


class KondroDtReportConfig(models.Model):
    _name = "kondro.dt.report.config"
    _description = "Configuration KPI DT"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    sequence = fields.Integer(default=10)
    description = fields.Text()
    active = fields.Boolean(default=True)

    model_id = fields.Many2one("ir.model", string="Modèle", required=True, ondelete="restrict", tracking=True)
    model_name = fields.Char(related="model_id.model", store=True)

    domain = fields.Text(string="Domaine", help="Expression domaine, par ex: [('status', '=', 'in_progress')]", tracking=True)
    date_field_id = fields.Many2one(
        "ir.model.fields",
        string="Champ date",
        domain="[('model_id', '=', model_id), ('ttype', 'in', ('date', 'datetime'))]",
        tracking=True,
    )
    measure_field_id = fields.Many2one(
        "ir.model.fields",
        string="Champ de mesure",
        domain="[('model_id', '=', model_id), ('ttype', 'in', ('float', 'integer', 'monetary'))]",
        tracking=True,
    )
    aggregator = fields.Selection(
        [
            ("count", "Nombre de lignes"),
            ("sum", "Somme"),
            ("avg", "Moyenne"),
        ],
        default="count",
        required=True,
        tracking=True,
    )
    currency_id = fields.Many2one("res.currency", string="Devise", default=lambda self: self.env.company.currency_id)
    target_value = fields.Float(string="Cible")
    unit_label = fields.Char(string="Unité")
    periodicity = fields.Selection(
        [("daily", "Quotidien"), ("weekly", "Hebdomadaire"), ("monthly", "Mensuel")],
        default="weekly",
        required=True,
        tracking=True,
    )

    last_snapshot_id = fields.Many2one("kondro.dt.kpi.snapshot", string="Dernier relevé", readonly=True, copy=False)
    last_value = fields.Float(string="Valeur actuelle", readonly=True, digits="Product Price")
    last_delta = fields.Float(string="Delta", readonly=True)
    last_delta_percent = fields.Float(string="Delta %", readonly=True)

    report_board_ids = fields.Many2many("kondro.dt.reporting.board", string="Tableaux", copy=False)

    _sql_constraints = [
        ("kondro_dt_report_config_code_unique", "unique(code)", "Le code KPI doit être unique."),
    ]

    def _compute_domain(self, date_from=None, date_to=None):
        domain = []
        if self.domain:
            try:
                domain = safe_eval(self.domain)
            except Exception:
                domain = []
        domain = list(domain)
        if self.date_field_id and (date_from or date_to):
            field_name = self.date_field_id.name
            if date_from:
                domain.append((field_name, ">=", date_from))
            if date_to:
                domain.append((field_name, "<=", date_to))
        return domain

    def _compute_value(self, date_from=None, date_to=None):
        self.ensure_one()
        model = self.env[self.model_name]
        domain = self._compute_domain(date_from, date_to)
        if self.aggregator == "count":
            return model.search_count(domain)
        if not self.measure_field_id:
            return 0.0
        field_name = self.measure_field_id.name
        records = model.search(domain)
        if not records:
            return 0.0
        values = [value for value in records.mapped(field_name) if value is not None]
        if not values:
            return 0.0
        if self.aggregator == "sum":
            return float(sum(values))
        if self.aggregator == "avg":
            return float(sum(values) / len(values))
        return 0.0

    def action_compute_snapshot(self):
        today = fields.Date.context_today(self)
        period_map = {
            "daily": (today, today),
            "weekly": (today - timedelta(days=today.weekday()), today),
            "monthly": (today.replace(day=1), today),
        }
        for config in self:
            if not config.active:
                continue
            date_from, date_to = period_map.get(config.periodicity, (today, today))
            value = config._compute_value(date_from, date_to)
            snapshot = self.env["kondro.dt.kpi.snapshot"].create({
                "config_id": config.id,
                "period_start": date_from,
                "period_end": date_to,
                "value": value,
                "periodicity": config.periodicity,
            })
            config._update_last_snapshot(snapshot)
        return True

    @api.model
    def cron_compute_snapshots(self):
        configs = self.search([("active", "=", True)])
        if configs:
            configs.action_compute_snapshot()
        return True

    def _update_last_snapshot(self, snapshot):
        self.ensure_one()
        delta = delta_percent = 0.0
        previous = self.env["kondro.dt.kpi.snapshot"].search(
            [
                ("config_id", "=", self.id),
                ("id", "!=", snapshot.id),
            ],
            order="period_end desc, create_date desc",
            limit=1,
        )
        if previous:
            delta = snapshot.value - previous.value
            delta_percent = (delta / previous.value * 100.0) if previous.value else 0.0
            snapshot.delta_value = delta
            snapshot.delta_percent = delta_percent
            snapshot.previous_snapshot_id = previous.id
        self.write(
            {
                "last_snapshot_id": snapshot.id,
                "last_value": snapshot.value,
                "last_delta": delta,
                "last_delta_percent": delta_percent,
            }
        )
