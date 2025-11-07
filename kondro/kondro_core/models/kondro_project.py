# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class KondroProject(models.Model):
    """Projet unifié KONDRO (remplace IT, Audit, Commercial)"""
    _name = 'kondro.project'
    _description = 'Projet KONDRO Unifié'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Nom du Projet',
        required=True,
        tracking=True,
        index=True
    )
    
    # Type de projet
    project_type = fields.Selection([
        ('it', 'Projet IT'),
        ('audit', 'Audit'),
        ('commercial', 'Commercial'),
        ('other', 'Autre')
    ], string='Type de Projet', required=True, default='commercial', tracking=True)
    
    # Statut du projet
    status = fields.Selection([
        ('draft', 'Brouillon'),
        ('opportunity', 'Opportunité'),
        ('planned', 'Planifié'),
        ('in_progress', 'En Cours'),
        ('validation', 'En Validation'),
        ('delivered', 'Livré'),
        ('closed', 'Clôturé'),
        ('cancelled', 'Annulé')
    ], string='Statut', default='draft', tracking=True)
    
    # Priorité
    priority = fields.Selection([
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('urgent', 'Urgente')
    ], string='Priorité', default='medium', tracking=True)
    
    # Client et relations commerciales
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        tracking=True,
        domain=[('is_company', '=', True)]
    )
    
    commercial_dossier_id = fields.Many2one(
        'kondro.commercial.dossier',
        string='Dossier Commercial',
        tracking=True,
        ondelete='set null'
    )
    
    # Équipe
    commercial_id = fields.Many2one(
        'res.users',
        string='Commercial Responsable',
        tracking=True
    )
    
    project_manager_id = fields.Many2one(
        'res.users',
        string='Chef de Projet',
        tracking=True
    )
    
    lead_engineer_id = fields.Many2one(
        'res.users',
        string='Ingénieur Principal',
        tracking=True
    )
    
    team_member_ids = fields.Many2many(
        'res.users',
        'kondro_project_team_rel',
        'project_id',
        'user_id',
        string='Équipe',
        tracking=True
    )
    
    # Dates
    start_date = fields.Date(
        string='Date de Début',
        tracking=True
    )
    
    end_date = fields.Date(
        string='Date de Fin',
        tracking=True
    )
    
    actual_start_date = fields.Date(
        string='Date de Début Réelle',
        tracking=True
    )
    
    actual_end_date = fields.Date(
        string='Date de Fin Réelle',
        tracking=True
    )
    
    # Budget et coûts
    budget = fields.Monetary(
        string='Budget (XOF)',
        currency_field='currency_id',
        tracking=True
    )
    
    engaged_amount = fields.Monetary(
        string='Montant Engagé',
        currency_field='currency_id',
        compute='_compute_financial_amounts',
        store=True
    )
    
    paid_amount = fields.Monetary(
        string='Montant Payé',
        currency_field='currency_id',
        compute='_compute_financial_amounts',
        store=True
    )
    
    margin = fields.Monetary(
        string='Marge',
        currency_field='currency_id',
        compute='_compute_financial_amounts',
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    # Description
    description = fields.Text(
        string='Description',
        tracking=True
    )
    
    # Progression
    progress = fields.Float(
        string='Progression (%)',
        compute='_compute_progress',
        store=True
    )
    
    # Dépenses liées (via kondro_finance)
    expense_count = fields.Integer(
        string='Nombre de Dépenses',
        compute='_compute_expense_count'
    )
    
    # Documents
    document_count = fields.Integer(
        string='Nombre de Documents',
        compute='_compute_document_count'
    )
    
    @api.depends('status', 'actual_start_date', 'actual_end_date', 'start_date', 'end_date')
    def _compute_progress(self):
        """Calcule la progression du projet"""
        for record in self:
            if record.status == 'closed' or record.status == 'delivered':
                record.progress = 100.0
            elif record.status == 'draft' or record.status == 'opportunity':
                record.progress = 0.0
            elif record.actual_start_date and record.end_date:
                # Calcul basé sur les dates
                from datetime import date
                today = date.today()
                if today >= record.end_date:
                    record.progress = 100.0
                elif today >= record.actual_start_date:
                    total_days = (record.end_date - record.actual_start_date).days
                    elapsed_days = (today - record.actual_start_date).days
                    if total_days > 0:
                        record.progress = min(100.0, (elapsed_days / total_days) * 100)
                    else:
                        record.progress = 0.0
                else:
                    record.progress = 0.0
            else:
                # Progression basée sur le statut
                status_progress = {
                    'planned': 10.0,
                    'in_progress': 50.0,
                    'validation': 80.0,
                }
                record.progress = status_progress.get(record.status, 0.0)
    
    @api.depends('commercial_dossier_id', 'expense_count')
    def _compute_financial_amounts(self):
        """Calcule les montants financiers depuis les dépenses"""
        for record in self:
            Expense = self.env.get('kondro.expense.request')
            Movement = self.env.get('kondro.treasury.movement')
            
            if Expense:
                # Montant engagé = somme des dépenses estimées
                expenses = Expense.search([('project_id', '=', record.id)])
                record.engaged_amount = sum(expenses.mapped('estimated_amount'))
            else:
                record.engaged_amount = 0.0
            
            if Movement:
                # Montant payé = somme des mouvements sorties
                movements = Movement.search([
                    ('project_id', '=', record.id),
                    ('movement_type', '=', 'out')
                ])
                record.paid_amount = sum(movements.mapped('amount'))
            else:
                record.paid_amount = 0.0
            
            record.margin = (record.budget or 0.0) - record.engaged_amount
    
    def _compute_expense_count(self):
        """Compte les dépenses liées au projet"""
        for record in self:
            Expense = self.env.get('kondro.expense.request')
            if Expense:
                record.expense_count = Expense.search_count([('project_id', '=', record.id)])
            else:
                record.expense_count = 0
    
    def _compute_document_count(self):
        """Compte les documents liés au projet"""
        for record in self:
            # Compter les pièces jointes dans les messages
            record.document_count = len(record.message_attachment_ids)
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """Vérifie la cohérence des dates"""
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("La date de début doit être antérieure à la date de fin."))
    
    def action_view_expenses(self):
        """Ouvre la vue des dépenses liées au projet"""
        Expense = self.env.get('kondro.expense.request')
        if not Expense:
            return {'type': 'ir.actions.act_window_close'}
        return {
            'type': 'ir.actions.act_window',
            'name': _('Dépenses'),
            'res_model': 'kondro.expense.request',
            'view_mode': 'kanban,tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id, 'default_expense_type': 'commercial'},
        }
    
    def action_view_documents(self):
        """Ouvre la vue des documents du projet"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Documents'),
            'res_model': 'ir.attachment',
            'view_mode': 'tree,form',
            'domain': [('res_model', '=', 'kondro.project'), ('res_id', '=', self.id)],
        }

