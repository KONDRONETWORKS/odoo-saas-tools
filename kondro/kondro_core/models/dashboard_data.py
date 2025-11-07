# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DashboardData(models.Model):
    """Données du Tableau de Bord KONDRO (fusionné depuis kondro_dashboard)"""
    _name = 'kondro.dashboard.data'
    _description = 'Données du Tableau de Bord KONDRO'
    _auto = False

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
            'expenses': self.get_expenses_stats()
        }

