# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class DashboardData(models.AbstractModel):
    """Données du Tableau de Bord génériques"""
    _name = 'kondro.dashboard.data'
    _description = 'Données du Tableau de Bord'

    def _get_config_parameter(self, key, default=None):
        ICP = self.env['ir.config_parameter'].sudo()
        value = ICP.get_param(key)
        if value is None or value == '':
            return default
        return value

    def _get_branding_payload(self):
        company = self.env.company
        default_title = company.display_name or _('Tableau de bord')
        title = self._get_config_parameter('kondro_core.dashboard_title', default_title)
        subtitle = self._get_config_parameter(
            'kondro_core.dashboard_subtitle', _('Vue d\'ensemble des activités')
        )
        currency = company.currency_id or self.env.company.currency_id
        currency_code = self._get_config_parameter(
            'kondro_core.dashboard_currency_code', currency and currency.name or 'XOF'
        )
        currency_locale = self._get_config_parameter(
            'kondro_core.dashboard_currency_locale', self.env.user.lang or 'fr_FR'
        )
        return {
            'title': title,
            'subtitle': subtitle,
            'company_name': company.display_name,
            'currency_code': currency_code,
            'currency_locale': currency_locale,
        }

    def _get_action_payload(
        self, action_param, label_param, icon_param, default_xmlid, default_label, default_icon, default_style
    ):
        ICP = self.env['ir.config_parameter'].sudo()
        action_id_str = ICP.get_param(action_param)
        action = None
        if action_id_str:
            try:
                action = self.env['ir.actions.actions'].browse(int(action_id_str))
                if not action or not action.exists():
                    action = None
            except ValueError:
                action = None
        if not action and default_xmlid:
            action = self.env.ref(default_xmlid, raise_if_not_found=False)

        label = ICP.get_param(label_param) or default_label
        icon = ICP.get_param(icon_param) or default_icon

        return {
            'label': label,
            'icon': icon,
            'style': default_style,
            'action_id': action.id if action else False,
        }

    def _get_quick_actions_payload(self):
        return [
            self._get_action_payload(
                'kondro_core.dashboard_project_action_id',
                'kondro_core.dashboard_project_label',
                'kondro_core.dashboard_project_icon',
                'kondro_core.action_kondro_project',
                _('Projets'),
                '📊',
                'primary',
            ),
            self._get_action_payload(
                'kondro_core.dashboard_commercial_action_id',
                'kondro_core.dashboard_commercial_label',
                'kondro_core.dashboard_commercial_icon',
                'kondro_core.action_kondro_commercial_dossier',
                _('Dossiers Commerciaux'),
                '📋',
                'secondary',
            ),
            self._get_action_payload(
                'kondro_core.dashboard_treasury_action_id',
                'kondro_core.dashboard_treasury_label',
                'kondro_core.dashboard_treasury_icon',
                'kondro_finance.action_kondro_treasury_movement',
                _('Trésorerie'),
                '💰',
                'success',
            ),
            self._get_action_payload(
                'kondro_core.dashboard_expense_action_id',
                'kondro_core.dashboard_expense_label',
                'kondro_core.dashboard_expense_icon',
                'kondro_finance.action_kondro_expense_request',
                _('Dépenses'),
                '💳',
                'info',
            ),
        ]

    @api.model
    def get_projects_stats(self):
        """Statistiques des projets unifiés"""
        Project = self.env.get('kondro.project')
        if not Project:
            return {'total': 0, 'in_progress': 0, 'completed': 0, 'planned': 0, 'total_budget': 0, 'actual_cost': 0}
        
        projects = Project.search([])
        
        return {
            'total': len(projects),
            'in_progress': len(projects.filtered(lambda p: p.status == 'in_progress')),
            'completed': len(projects.filtered(lambda p: p.status in ['delivered', 'closed'])),
            'planned': len(projects.filtered(lambda p: p.status == 'planned')),
            'total_budget': sum(projects.mapped('budget')),
            'actual_cost': sum(projects.mapped('paid_amount'))
        }
    
    @api.model
    def get_treasury_stats(self):
        """Statistiques de la trésorerie"""
        Movement = self.env.get('kondro.treasury.movement')
        if not Movement:
            return {'total_income': 0, 'total_expense': 0, 'balance': 0, 'movements_count': 0}
        
        movements = Movement.search([])
        
        total_income = sum(movements.filtered(lambda m: m.movement_type == 'in').mapped('amount'))
        total_expense = sum(movements.filtered(lambda m: m.movement_type == 'out').mapped('amount'))
        
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': total_income - total_expense,
            'movements_count': len(movements)
        }
    
    @api.model
    def get_commercial_stats(self):
        """Statistiques commerciales"""
        Dossier = self.env.get('kondro.commercial.dossier')
        if not Dossier:
            return {'total_dossiers': 0, 'active_dossiers': 0, 'total_value': 0, 'won_dossiers': 0}
        
        dossiers = Dossier.search([])
        
        return {
            'total_dossiers': len(dossiers),
            'active_dossiers': len(dossiers.filtered(lambda d: d.state == 'in_progress')),
            'total_value': sum(dossiers.mapped('budget')),
            'won_dossiers': len(dossiers.filtered(lambda d: d.state == 'won'))
        }
    
    @api.model
    def get_expenses_stats(self):
        """Statistiques des dépenses"""
        Expense = self.env.get('kondro.expense.request')
        if not Expense:
            return {'total_requests': 0, 'pending': 0, 'approved': 0, 'total_amount': 0}
        
        expenses = Expense.search([])
        
        return {
            'total_requests': len(expenses),
            'pending': len(expenses.filtered(lambda e: e.state == 'draft')),
            'approved': len(expenses.filtered(lambda e: e.state == 'approved')),
            'total_amount': sum(expenses.mapped('estimated_amount'))
        }
    
    @api.model
    def get_overall_stats(self):
        """Statistiques globales"""
        return {
            'projects': self.get_projects_stats(),
            'treasury': self.get_treasury_stats(),
            'commercial': self.get_commercial_stats(),
            'expenses': self.get_expenses_stats(),
            'branding': self._get_branding_payload(),
            'quick_actions': self._get_quick_actions_payload(),
        }

