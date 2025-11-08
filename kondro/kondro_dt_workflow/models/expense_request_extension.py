# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class KondroExpenseRequest(models.Model):
    _inherit = "kondro.expense.request"

    dt_matrix_id = fields.Many2one("kondro.dt.workflow.matrix", string="Matrice DT", tracking=True)
    dt_responsible_id = fields.Many2one("res.users", string="Responsible (R)", tracking=True)
    dt_accountable_id = fields.Many2one("res.users", string="Accountable (A)", tracking=True)
    dt_consulted_ids = fields.Many2many(
        "res.users",
        "kondro_expense_dt_consulted_rel",
        "expense_id",
        "user_id",
        string="Consulted (C)",
        tracking=True,
    )
    dt_informed_ids = fields.Many2many(
        "res.users",
        "kondro_expense_dt_informed_rel",
        "expense_id",
        "user_id",
        string="Informed (I)",
        tracking=True,
    )
    dt_validation_state = fields.Selection(
        [
            ("pending", "En attente"),
            ("approved", "Validée techniquement"),
            ("changes", "À revoir"),
        ],
        string="Validation technique",
        default="pending",
        tracking=True,
    )
    dt_validation_user_id = fields.Many2one("res.users", string="Validé techniquement par", tracking=True)
    dt_validation_date = fields.Datetime(string="Date validation technique", tracking=True)
    dt_requires_validation = fields.Boolean(string="Validation technique requise", compute="_compute_dt_requires_validation", store=True)

    @api.depends("expense_type", "project_id", "department_id")
    def _compute_dt_requires_validation(self):
        for record in self:
            record.dt_requires_validation = bool(record.expense_type == "commercial" or record.project_id)

    def action_submit(self):
        res = super().action_submit()
        self._assign_dt_matrix()
        return res

    def action_validate(self):
        res = super().action_validate()
        for record in self:
            if record.dt_requires_validation and record.dt_validation_state != "approved":
                record.message_post(body=_("Validation technique en attente."))
        return res

    def action_approve(self):
        for record in self:
            if record.dt_requires_validation and record.dt_validation_state != "approved":
                raise UserError(_("La validation technique doit être réalisée avant l'approbation."))
        return super().action_approve()

    def action_dt_validate(self):
        self.ensure_one()
        self.dt_validation_state = "approved"
        self.dt_validation_user_id = self.env.user
        self.dt_validation_date = fields.Datetime.now()
        self.message_post(body=_("Validation technique réalisée par %s.") % self.env.user.display_name)

    def action_dt_request_changes(self):
        self.ensure_one()
        self.dt_validation_state = "changes"
        self.dt_validation_user_id = self.env.user
        self.dt_validation_date = fields.Datetime.now()
        self.message_post(body=_("Demande de modifications techniques par %s.") % self.env.user.display_name)

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

    def _assign_dt_matrix(self):
        Matrix = self.env["kondro.dt.workflow.matrix"]
        for record in self:
            matrix = record.dt_matrix_id
            responsible_users = self.env["res.users"]
            if not matrix and record.project_id and getattr(record.project_id, "dt_matrix_id", False):
                matrix = record.project_id.dt_matrix_id
            if not matrix:
                domain = [("process_type", "=", "commercial_expense" if record.expense_type == "commercial" else "internal_expense")]
                if record.project_id:
                    matched = Matrix.search(domain + [("project_id", "=", record.project_id.id)], limit=1)
                    matrix = matched or matrix
                if not matrix and record.department_id:
                    matched = Matrix.search(domain + [("department_id", "=", record.department_id.id)], limit=1)
                    matrix = matched or matrix
                if not matrix:
                    matrix = Matrix.search(domain, limit=1)

            if matrix:
                record.dt_matrix_id = matrix
                responsible_users = matrix.get_users_by_role("responsible")
                accountable_users = matrix.get_users_by_role("accountable")
                consulted_users = matrix.get_users_by_role("consulted")
                informed_users = matrix.get_users_by_role("informed")

                record.dt_responsible_id = responsible_users[:1].id if responsible_users else False
                record.dt_accountable_id = accountable_users[:1].id if accountable_users else False
                record.dt_consulted_ids = [(6, 0, consulted_users.ids)]
                record.dt_informed_ids = [(6, 0, informed_users.ids)]

                partners_to_subscribe = matrix.get_partners_by_role("informed") | matrix.get_partners_by_role("consulted")
                if partners_to_subscribe:
                    record.message_subscribe(partner_ids=partners_to_subscribe.ids)
            else:
                record.dt_matrix_id = False
                record.dt_responsible_id = False
                record.dt_accountable_id = False
                record.dt_consulted_ids = [(5, 0, 0)]
                record.dt_informed_ids = [(5, 0, 0)]
            if record.dt_requires_validation and record.dt_validation_state == "pending" and matrix and responsible_users:
                for user in responsible_users:
                    record.activity_schedule(
                        "mail.mail_activity_data_todo",
                        user_id=user.id,
                        summary=_("Validation technique requise"),
                    )
