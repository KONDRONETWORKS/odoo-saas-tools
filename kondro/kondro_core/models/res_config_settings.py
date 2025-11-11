# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dashboard_title = fields.Char(
        string="Titre du tableau de bord",
        config_parameter='kondro_core.dashboard_title',
        default=lambda self: _('Tableau de bord'),
    )
    dashboard_subtitle = fields.Char(
        string="Sous-titre du tableau de bord",
        config_parameter='kondro_core.dashboard_subtitle',
        default=lambda self: _('Vue d\'ensemble des activités'),
    )
    dashboard_currency_locale = fields.Char(
        string="Locale de formatage monétaire",
        config_parameter='kondro_core.dashboard_currency_locale',
        default=lambda self: self.env.user.lang or 'fr_FR',
        help="Locale utilisée pour formatter les montants (ex: fr_FR, en_US).",
    )
    dashboard_currency_code = fields.Char(
        string="Devise pour l\'affichage",
        config_parameter='kondro_core.dashboard_currency_code',
        default=lambda self: self.env.company.currency_id.name or 'XOF',
    )

    dashboard_project_action_id = fields.Many2one(
        'ir.actions.actions',
        string="Action projets",
        domain="[('type', '=', 'ir.actions.act_window')]",
        config_parameter='kondro_core.dashboard_project_action_id',
        default=lambda self: self._get_default_action_xmlid('kondro_core.action_kondro_project'),
    )
    dashboard_project_label = fields.Char(
        string="Libellé action projets",
        config_parameter='kondro_core.dashboard_project_label',
        default=lambda self: _('Projets'),
    )
    dashboard_project_icon = fields.Char(
        string="Icône action projets",
        config_parameter='kondro_core.dashboard_project_icon',
        default='📊',
    )

    dashboard_commercial_action_id = fields.Many2one(
        'ir.actions.actions',
        string="Action dossiers commerciaux",
        domain="[('type', '=', 'ir.actions.act_window')]",
        config_parameter='kondro_core.dashboard_commercial_action_id',
        default=lambda self: self._get_default_action_xmlid('kondro_core.action_kondro_commercial_dossier'),
    )
    dashboard_commercial_label = fields.Char(
        string="Libellé action dossiers commerciaux",
        config_parameter='kondro_core.dashboard_commercial_label',
        default=lambda self: _('Dossiers Commerciaux'),
    )
    dashboard_commercial_icon = fields.Char(
        string="Icône action dossiers commerciaux",
        config_parameter='kondro_core.dashboard_commercial_icon',
        default='📋',
    )

    dashboard_treasury_action_id = fields.Many2one(
        'ir.actions.actions',
        string="Action trésorerie",
        domain="[('type', '=', 'ir.actions.act_window')]",
        config_parameter='kondro_core.dashboard_treasury_action_id',
        default=lambda self: self._get_default_action_xmlid('kondro_finance.action_kondro_treasury_movement'),
    )
    dashboard_treasury_label = fields.Char(
        string="Libellé action trésorerie",
        config_parameter='kondro_core.dashboard_treasury_label',
        default=lambda self: _('Trésorerie'),
    )
    dashboard_treasury_icon = fields.Char(
        string="Icône action trésorerie",
        config_parameter='kondro_core.dashboard_treasury_icon',
        default='💰',
    )

    dashboard_expense_action_id = fields.Many2one(
        'ir.actions.actions',
        string="Action dépenses",
        domain="[('type', '=', 'ir.actions.act_window')]",
        config_parameter='kondro_core.dashboard_expense_action_id',
        default=lambda self: self._get_default_action_xmlid('kondro_finance.action_kondro_expense_request'),
    )
    dashboard_expense_label = fields.Char(
        string="Libellé action dépenses",
        config_parameter='kondro_core.dashboard_expense_label',
        default=lambda self: _('Dépenses'),
    )
    dashboard_expense_icon = fields.Char(
        string="Icône action dépenses",
        config_parameter='kondro_core.dashboard_expense_icon',
        default='💳',
    )

    @api.model
    def _get_default_action_xmlid(self, xmlid):
        action = self.env.ref(xmlid, raise_if_not_found=False)
        return action.id if action else False

