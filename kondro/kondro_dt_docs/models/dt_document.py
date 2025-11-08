# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class KondroDtDocument(models.Model):
    _name = "kondro.dt.document"
    _description = "Document DT"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name, version desc"

    name = fields.Char(required=True, tracking=True)
    sequence = fields.Integer(default=10)
    reference = fields.Char(string="Référence", readonly=True, copy=False)
    version = fields.Char(string="Version", default="1.0", tracking=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("in_review", "En revue"),
            ("approved", "Validé"),
            ("archived", "Archivé"),
        ],
        default="draft",
        tracking=True,
    )
    category_id = fields.Many2one(
        "kondro.dt.document.category",
        string="Catégorie",
        required=True,
        tracking=True,
    )
    tag_ids = fields.Many2many("kondro.dt.document.tag", string="Tags")
    owner_id = fields.Many2one("res.users", string="Responsable", default=lambda self: self.env.user, tracking=True)
    reviewer_id = fields.Many2one("res.users", string="Relecteur", tracking=True)
    approver_id = fields.Many2one("res.users", string="Validateur", tracking=True)
    approval_date = fields.Date(string="Date de validation", tracking=True)
    review_deadline = fields.Date(string="Date limite de revue")
    next_revision_date = fields.Date(string="Prochaine révision")

    project_id = fields.Many2one("kondro.project", string="Projet", tracking=True)
    dossier_id = fields.Many2one("kondro.commercial.dossier", string="Dossier commercial", tracking=True)
    design_id = fields.Many2one("kondro.dt.project.design", string="Artefact technique", tracking=True)
    expense_id = fields.Many2one("kondro.expense.request", string="Dépense liée", tracking=True)

    attachment_id = fields.Many2one("ir.attachment", string="Fichier principal")
    attachment_ids = fields.Many2many(
        "ir.attachment",
        "kondro_dt_document_attachment_rel",
        "document_id",
        "attachment_id",
        string="Pièces jointes",
    )
    url_link = fields.Char(string="Lien externe (SharePoint, Drive…)")
    description = fields.Text(string="Résumé fonctionnel / technique")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company.id, index=True)

    is_locked = fields.Boolean(string="Lecture seule", compute="_compute_is_locked", store=True)
    color = fields.Integer(related="category_id.color", readonly=True)

    _sql_constraints = [
        ("kondro_dt_document_reference_unique", "unique(reference, company_id)", "La référence doit être unique."),
    ]

    @api.depends("state")
    def _compute_is_locked(self):
        for document in self:
            document.is_locked = document.state in {"approved", "archived"}

    @api.model
    def create(self, vals):
        if not vals.get("reference"):
            vals["reference"] = self._generate_reference(vals)
        document = super().create(vals)
        document._subscribe_stakeholders()
        return document

    def write(self, vals):
        res = super().write(vals)
        if any(field in vals for field in ["owner_id", "reviewer_id", "approver_id"]):
            self._subscribe_stakeholders()
        if vals.get("state") == "approved":
            self.filtered(lambda doc: doc.state == "approved" and not doc.approval_date).write({
                "approval_date": fields.Date.today()
            })
        return res

    def unlink(self):
        locked_docs = self.filtered(lambda doc: doc.state == "approved")
        if locked_docs:
            raise ValidationError(_("Impossible de supprimer un document validé."))
        return super().unlink()

    def _subscribe_stakeholders(self):
        for document in self:
            partners = document.mapped("owner_id.partner_id")
            partners |= document.mapped("reviewer_id.partner_id")
            partners |= document.mapped("approver_id.partner_id")
            partners = partners.filtered(lambda p: p)
            if partners:
                document.message_subscribe(partner_ids=partners.ids)

    def _generate_reference(self, vals):
        company = self.env.company
        category_id = vals.get("category_id")
        prefix = "DT"
        if category_id:
            category = self.env["kondro.dt.document.category"].browse(category_id)
            if category:
                prefix = (category.name or "DT").upper()[:3]
        sequence = self.env["ir.sequence"].next_by_code("kondro.dt.document") or "0000"
        return f"{prefix}-{sequence}"

    def action_submit_review(self):
        for document in self:
            if document.state == "archived":
                raise ValidationError(_("Impossible de relire un document archivé."))
            document.state = "in_review"
            if document.reviewer_id:
                document.activity_schedule(
                    "mail.mail_activity_data_todo",
                    user_id=document.reviewer_id.id,
                    summary=_("Relecture documentaire"),
                    date_deadline=document.review_deadline,
                )

    def action_approve(self):
        for document in self:
            document.state = "approved"
            document.approval_date = fields.Date.today()
            if document.approver_id:
                document.activity_schedule(
                    "mail.mail_activity_data_todo",
                    user_id=document.approver_id.id,
                    summary=_("Contrôler la diffusion du document validé"),
                )

    def action_archive(self):
        for document in self:
            document.state = "archived"

    def action_reset_draft(self):
        for document in self:
            document.state = "draft"
            document.approval_date = False

    def action_open_attachment(self):
        self.ensure_one()
        if self.attachment_id:
            return {
                "type": "ir.actions.act_url",
                "target": "new",
                "url": f"/web/content/{self.attachment_id.id}?download=true",
            }
        raise ValidationError(_("Aucun fichier principal n'est défini."))

    @api.constrains("project_id", "dossier_id", "design_id")
    def _check_links(self):
        for document in self:
            if document.design_id and document.design_id.project_id and document.project_id and document.design_id.project_id != document.project_id:
                raise ValidationError(_("Le document technique doit être rattaché au même projet que l’artefact."))

    def name_get(self):
        result = []
        for record in self:
            display = record.name
            if record.version:
                display = f"{display} ({record.version})"
            if record.reference:
                display = f"[{record.reference}] {display}"
            result.append((record.id, display))
        return result
