# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import api, fields, models, _


class KondroDtMetric(models.Model):
    """Indicateurs du tableau de bord Directeur Technique."""

    _name = "kondro.dt.metric"
    _description = "Indicateur Hub Directeur Technique"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, id"

    name = fields.Char(required=True, tracking=True)
    technical_name = fields.Char(required=True, index=True)
    sequence = fields.Integer(default=10)
    metric_type = fields.Selection(
        [
            ("number", "Valeur numérique"),
            ("currency", "Montant"),
            ("percentage", "Pourcentage"),
            ("text", "Texte"),
        ],
        default="number",
        required=True,
    )
    currency_id = fields.Many2one("res.currency", string="Devise", default=lambda self: self.env.company.currency_id.id)
    value_float = fields.Float(string="Valeur", compute="_compute_metric_values", store=False)
    value_text = fields.Char(string="Commentaire", compute="_compute_metric_values", store=False)
    value_percentage = fields.Float(string="Pourcentage", compute="_compute_metric_values", store=False)
    delta_value = fields.Float(string="Delta", compute="_compute_metric_values", store=False)
    trend = fields.Selection(
        [("up", "Hausse"), ("down", "Baisse"), ("steady", "Stable")],
        string="Tendance",
        compute="_compute_metric_values",
        store=False,
    )
    last_evaluation = fields.Datetime(string="Dernière mise à jour", compute="_compute_metric_values", store=False)

    @api.model
    def _gather_stats(self):
        """Rassemble les statistiques consolidées pour les indicateurs."""
        Dashboard = self.env["kondro.dashboard.data"]
        stats = defaultdict(dict)
        try:
            overall = Dashboard.get_overall_stats()
        except Exception:
            overall = {}

        stats.update(overall or {})

        # Calculs complémentaires spécifiques au Directeur Technique
        Project = self.env["kondro.project"]
        Expense = self.env["kondro.expense.request"]

        projects = Project.search([])
        expenses = Expense.search([])

        stats.setdefault("projects", {})
        stats.setdefault("expenses", {})

        if "deadline_date" in Project._fields:
            late_projects = projects.filtered(lambda p: p.status == "in_progress" and p.deadline_date and p.deadline_date < fields.Date.today())
            stats["projects"]["late"] = len(late_projects)
        else:
            stats["projects"]["late"] = 0

        if "team_capacity" in Project._fields:
            stats["projects"]["capacity"] = sum(projects.mapped("team_capacity"))
        else:
            stats["projects"]["capacity"] = 0.0

        if "state" in Expense._fields:
            awaiting_states = {"approved", "planned"}
            stats["expenses"]["awaiting_payment"] = len(expenses.filtered(lambda e: e.state in awaiting_states))
        else:
            stats["expenses"]["awaiting_payment"] = 0

        return stats

    def _compute_metric_values(self):
        stats = self._gather_stats()
        today = fields.Datetime.now()
        for metric in self:
            metric.last_evaluation = today
            metric.value_float = 0.0
            metric.value_text = False
            metric.value_percentage = 0.0
            metric.delta_value = 0.0
            metric.trend = "steady"

            handler = getattr(metric, f"_compute_{metric.technical_name}_metric", None)
            if handler:
                handler(stats)
                continue

            # Fallback générique sur le dictionnaire stats
            value = self._extract_stat_value(stats, metric.technical_name)
            if isinstance(value, (int, float)):
                metric.value_float = float(value)
            elif isinstance(value, str):
                metric.value_text = value

    def _extract_stat_value(self, stats, technical_name):
        """Permet d’extraire une valeur depuis les stats agrégées avec un chemin du type 'projects.total'."""
        parts = technical_name.split(".")
        current = stats
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return 0.0
        return current

    # --- Indicateurs spécifiques -------------------------------------------------

    def _compute_projects_total_metric(self, stats):
        value = self._extract_stat_value(stats, "projects.total")
        self.value_float = float(value)

    def _compute_projects_in_progress_metric(self, stats):
        value = self._extract_stat_value(stats, "projects.in_progress")
        self.value_float = float(value)

    def _compute_projects_late_metric(self, stats):
        value = self._extract_stat_value(stats, "projects.late")
        self.value_float = float(value)

    def _compute_treasury_balance_metric(self, stats):
        value = self._extract_stat_value(stats, "treasury.balance")
        self.value_float = float(value)
        self.metric_type = "currency"
        self.currency_id = self.env.company.currency_id

    def _compute_expenses_pending_metric(self, stats):
        value = self._extract_stat_value(stats, "expenses.pending")
        self.value_float = float(value)

    def _compute_expenses_total_metric(self, stats):
        value = self._extract_stat_value(stats, "expenses.total_amount")
        self.value_float = float(value)
        self.metric_type = "currency"
        self.currency_id = self.env.company.currency_id

    def _compute_expenses_awaiting_payment_metric(self, stats):
        value = self._extract_stat_value(stats, "expenses.awaiting_payment")
        self.value_float = float(value)

    def _compute_commercial_total_value_metric(self, stats):
        value = self._extract_stat_value(stats, "commercial.total_value")
        self.value_float = float(value)
        self.metric_type = "currency"
        self.currency_id = self.env.company.currency_id

    def _compute_treasury_income_metric(self, stats):
        value = self._extract_stat_value(stats, "treasury.total_income")
        self.value_float = float(value)
        self.metric_type = "currency"
        self.currency_id = self.env.company.currency_id

    def _compute_treasury_expense_metric(self, stats):
        value = self._extract_stat_value(stats, "treasury.total_expense")
        self.value_float = float(value)
        self.metric_type = "currency"
        self.currency_id = self.env.company.currency_id

    def _compute_treasury_balance_text_metric(self, stats):
        balance = self._extract_stat_value(stats, "treasury.balance")
        income = self._extract_stat_value(stats, "treasury.total_income")
        expense = self._extract_stat_value(stats, "treasury.total_expense")
        self.metric_type = "text"
        self.value_text = _("Solde: %.2f / Entrées: %.2f / Sorties: %.2f") % (balance, income, expense)

