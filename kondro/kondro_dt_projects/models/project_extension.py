# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class KondroProject(models.Model):
    _inherit = "kondro.project"

    technical_stage = fields.Selection(
        [
            ("definition", "Définition"),
            ("design", "Conception"),
            ("implementation", "Mise en œuvre"),
            ("validation", "Validation"),
            ("handover", "Transfert"),
        ],
        string="Phase Technique",
        default="definition",
        tracking=True,
    )
    deadline_date = fields.Date(string="Date limite technique", tracking=True)
    technical_summary = fields.Text(string="Synthèse technique", tracking=True)

    milestone_ids = fields.One2many(
        "kondro.dt.project.milestone",
        "project_id",
        string="Jalons techniques",
    )
    risk_ids = fields.One2many(
        "kondro.dt.project.risk",
        "project_id",
        string="Risques techniques",
    )
    design_ids = fields.One2many(
        "kondro.dt.project.design",
        "project_id",
        string="Documents techniques",
    )

    milestone_count = fields.Integer(compute="_compute_dt_counts", string="Jalons")
    risk_count = fields.Integer(compute="_compute_dt_counts", string="Risques")
    design_count = fields.Integer(compute="_compute_dt_counts", string="Documents techniques")

    def _compute_dt_counts(self):
        for project in self:
            project.milestone_count = len(project.milestone_ids)
            project.risk_count = len(project.risk_ids)
            project.design_count = len(project.design_ids)

    def action_view_dt_milestones(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Jalons techniques"),
            "res_model": "kondro.dt.project.milestone",
            "view_mode": "tree,form",
            "domain": [("project_id", "=", self.id)],
            "context": {"default_project_id": self.id},
        }

    def action_view_dt_risks(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Risques techniques"),
            "res_model": "kondro.dt.project.risk",
            "view_mode": "tree,form",
            "domain": [("project_id", "=", self.id)],
            "context": {"default_project_id": self.id},
        }

    def action_view_dt_designs(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Documents techniques"),
            "res_model": "kondro.dt.project.design",
            "view_mode": "tree,form",
            "domain": [("project_id", "=", self.id)],
            "context": {"default_project_id": self.id},
        }
