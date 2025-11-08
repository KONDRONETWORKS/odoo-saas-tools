# -*- coding: utf-8 -*-
from odoo import fields, models


class KondroDtProjectDesign(models.Model):
    _name = "kondro.dt.project.design"
    _description = "Document technique de projet"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "design_type, version desc, id desc"

    name = fields.Char(string="Titre", required=True, tracking=True)
    project_id = fields.Many2one("kondro.project", string="Projet", required=True, ondelete="cascade", tracking=True)
    design_type = fields.Selection(
        [
            ("hld", "High Level Design (HLD)"),
            ("lld", "Low Level Design (LLD)"),
            ("procedure", "Procédure / Script"),
            ("report", "Rapport / PV"),
            ("other", "Autre"),
        ],
        string="Type de document",
        default="hld",
        tracking=True,
    )
    version = fields.Char(string="Version", default="1.0", tracking=True)
    owner_id = fields.Many2one("res.users", string="Rédacteur", tracking=True, default=lambda self: self.env.user)
    attachment_id = fields.Many2one("ir.attachment", string="Pièce jointe")
    url_link = fields.Char(string="Lien (SharePoint, Drive…)")
    description = fields.Text(string="Notes")
    validated = fields.Boolean(string="Validé", tracking=True, default=False)
    validation_date = fields.Date(string="Date de validation", tracking=True)

    def action_open_attachment(self):
        self.ensure_one()
        if self.attachment_id:
            return {
                "type": "ir.actions.act_url",
                "target": "new",
                "url": "/web/content/%s?download=true" % self.attachment_id.id,
            }
        return False

