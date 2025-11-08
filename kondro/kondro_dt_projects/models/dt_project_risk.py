# -*- coding: utf-8 -*-
from odoo import api, fields, models


class KondroDtProjectRisk(models.Model):
    _name = "kondro.dt.project.risk"
    _description = "Risque technique de projet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "impact desc, probability desc, id"

    name = fields.Char(string="Risque", required=True, tracking=True)
    project_id = fields.Many2one("kondro.project", string="Projet", required=True, ondelete="cascade", tracking=True)
    owner_id = fields.Many2one("res.users", string="Pilote", tracking=True, default=lambda self: self.env.user)
    category = fields.Selection(
        [
            ("technical", "Technique"),
            ("resource", "Ressource"),
            ("planning", "Planning"),
            ("quality", "Qualité"),
            ("other", "Autre"),
        ],
        string="Catégorie",
        default="technical",
        tracking=True,
    )
    probability = fields.Selection(
        [("low", "Faible"), ("medium", "Moyenne"), ("high", "Élevée"), ("critical", "Critique")],
        string="Probabilité",
        default="medium",
        tracking=True,
    )
    impact = fields.Selection(
        [("low", "Faible"), ("medium", "Moyen"), ("high", "Élevé"), ("critical", "Critique")],
        string="Impact",
        default="medium",
        tracking=True,
    )
    risk_level = fields.Selection(
        [
            ("acceptable", "Acceptable"),
            ("monitor", "À surveiller"),
            ("mitigate", "À atténuer"),
            ("escalate", "Escalade"),
        ],
        string="Niveau de risque",
        compute="_compute_risk_level",
        store=True,
    )
    mitigation_plan = fields.Text(string="Plan d’atténuation")
    status = fields.Selection(
        [("open", "Ouvert"), ("mitigated", "Atténué"), ("closed", "Clôturé")],
        string="Statut",
        default="open",
        tracking=True,
    )
    next_review_date = fields.Date(string="Prochaine revue")

    @api.depends("probability", "impact")
    def _compute_risk_level(self):
        mapping = {
            ("low", "low"): "acceptable",
            ("low", "medium"): "monitor",
            ("low", "high"): "mitigate",
            ("low", "critical"): "escalate",
            ("medium", "low"): "monitor",
            ("medium", "medium"): "mitigate",
            ("medium", "high"): "escalate",
            ("medium", "critical"): "escalate",
            ("high", "low"): "mitigate",
            ("high", "medium"): "escalate",
            ("high", "high"): "escalate",
            ("high", "critical"): "escalate",
            ("critical", "low"): "escalate",
            ("critical", "medium"): "escalate",
            ("critical", "high"): "escalate",
            ("critical", "critical"): "escalate",
        }
        for record in self:
            key = (record.probability or "medium", record.impact or "medium")
            record.risk_level = mapping.get(key, "monitor")

