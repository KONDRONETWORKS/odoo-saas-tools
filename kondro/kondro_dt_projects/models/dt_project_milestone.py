# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class KondroDtProjectMilestone(models.Model):
    _name = "kondro.dt.project.milestone"
    _description = "Jalon technique de projet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "target_date, sequence, id"

    name = fields.Char(string="Titre", required=True, tracking=True)
    project_id = fields.Many2one("kondro.project", string="Projet", required=True, ondelete="cascade", tracking=True)
    sequence = fields.Integer(default=10)
    owner_id = fields.Many2one("res.users", string="Responsable", tracking=True, default=lambda self: self.env.user)
    target_date = fields.Date(string="Date cible", tracking=True)
    completion_date = fields.Date(string="Date de réalisation", tracking=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("planned", "Planifié"),
            ("in_progress", "En cours"),
            ("done", "Terminé"),
            ("cancelled", "Annulé"),
        ],
        string="Statut",
        default="draft",
        tracking=True,
    )
    description = fields.Text(string="Description")
    blocking = fields.Boolean(string="Bloquant", tracking=True)
    progress = fields.Integer(string="Progression (%)", default=0, tracking=True)

    @api.onchange("state")
    def _onchange_state(self):
        if self.state == "done" and not self.completion_date:
            self.completion_date = fields.Date.today()

