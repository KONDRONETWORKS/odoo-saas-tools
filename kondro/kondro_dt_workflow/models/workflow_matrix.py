# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class KondroDtWorkflowMatrix(models.Model):
    _name = "kondro.dt.workflow.matrix"
    _description = "Matrice RACI Directeur Technique"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "process_type, name"

    name = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id)
    process_type = fields.Selection(
        [
            ("internal_expense", "Dépense interne"),
            ("commercial_expense", "Dépense commerciale"),
            ("change_request", "Change request"),
        ],
        string="Processus",
        required=True,
        tracking=True,
    )
    project_id = fields.Many2one("kondro.project", string="Projet ciblé", ondelete="cascade", tracking=True)
    department_id = fields.Many2one("hr.department", string="Service concerné", tracking=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string="Notes")
    line_ids = fields.One2many("kondro.dt.workflow.matrix.line", "matrix_id", string="Participants")
    escalation_user_id = fields.Many2one("res.users", string="Contact d’escalade", tracking=True)
    sla_hours = fields.Integer(string="SLA (heures)", help="Délai avant relance automatique", default=24)

    _sql_constraints = [
        (
            "kondro_dt_matrix_unique",
            "unique(process_type, project_id, department_id, company_id)",
            "Une matrice existe déjà pour ce processus dans le périmètre sélectionné.",
        )
    ]

    def get_users_by_role(self, role):
        self.ensure_one()
        users = self.env["res.users"]
        for line in self.line_ids.filtered(lambda line: line.role_type == role):
            users |= line._get_users()
        return users

    def get_partners_by_role(self, role):
        return self.get_users_by_role(role).mapped("partner_id")

    def action_open_lines(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Participants RACI"),
            "res_model": "kondro.dt.workflow.matrix.line",
            "view_mode": "tree,form",
            "domain": [("matrix_id", "=", self.id)],
            "context": {"default_matrix_id": self.id},
        }


class KondroDtWorkflowMatrixLine(models.Model):
    _name = "kondro.dt.workflow.matrix.line"
    _description = "Participant RACI"
    _order = "role_type, user_id"

    matrix_id = fields.Many2one("kondro.dt.workflow.matrix", required=True, ondelete="cascade")
    role_type = fields.Selection(
        [
            ("responsible", "Responsible"),
            ("accountable", "Accountable"),
            ("consulted", "Consulted"),
            ("informed", "Informed"),
        ],
        string="Rôle",
        required=True,
    )
    user_id = fields.Many2one("res.users", string="Utilisateur", required=False)
    group_id = fields.Many2one("res.groups", string="Groupe")
    notes = fields.Char(string="Commentaire")

    @api.constrains("user_id", "group_id")
    def _check_user_or_group(self):
        for line in self:
            if not line.user_id and not line.group_id:
                raise ValidationError("Sélectionnez un utilisateur ou un groupe pour la ligne RACI.")

    def _get_users(self):
        users = self.env["res.users"]
        if self.user_id:
            users |= self.user_id
        if self.group_id:
            users |= self.group_id.users
        return users

