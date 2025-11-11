# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class KondroExpenseRequest(models.Model):
    """Demande de Dépense KONDRO (Unifiée pour internes et commerciales)"""
    _name = 'kondro.expense.request'
    _description = 'Demande de Dépense KONDRO'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Objet de la Dépense',
        required=True,
        tracking=True
    )
    
    # Type de dépense
    expense_type = fields.Selection([
        ('internal', 'Dépense Interne'),
        ('commercial', 'Dépense Commerciale')
    ], string='Type de Dépense', required=True, default='internal', tracking=True)
    
    # Workflow
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('submitted', 'Soumise'),
        ('validated', 'Validée'),
        ('approved', 'Approuvée'),
        ('planned', 'Planifiée'),
        ('paid', 'Payée'),
        ('closed', 'Clôturée')
    ], string='État', default='draft', tracking=True, required=True)
    
    # Service / Projet
    department_id = fields.Many2one(
        'hr.department',
        string='Service Demandeur',
        tracking=True,
        help="Service pour les dépenses internes"
    )
    
    project_id = fields.Many2one(
        'kondro.project',
        string='Projet',
        tracking=True,
        help="Projet pour les dépenses commerciales"
    )
    
    # Montant
    estimated_amount = fields.Monetary(
        string='Montant Estimé (XOF)',
        currency_field='currency_id',
        required=True,
        tracking=True
    )
    
    paid_amount = fields.Monetary(
        string='Montant Payé (XOF)',
        currency_field='currency_id',
        compute='_compute_paid_amount',
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    # Fournisseur / Employé
    supplier_id = fields.Many2one(
        'res.partner',
        string='Fournisseur',
        tracking=True,
        domain=[('supplier_rank', '>', 0)]
    )
    
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employé',
        tracking=True,
        help="Pour les notes de frais"
    )
    
    # Description
    description = fields.Text(
        string='Description',
        tracking=True
    )
    
    # Budget
    budget_line_id = fields.Many2one(
        'account.budget.post',
        string='Ligne Budgétaire',
        tracking=True
    )
    
    # Pièces jointes
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'kondro_expense_attachment_rel',
        'expense_id',
        'attachment_id',
        string='Pièces Jointes',
        tracking=True
    )
    
    # Mouvements de trésorerie liés
    treasury_movement_ids = fields.One2many(
        'kondro.treasury.movement',
        'expense_request_id',
        string='Mouvements de Trésorerie',
        readonly=True
    )
    
    treasury_movement_count = fields.Integer(
        string='Nombre de Mouvements',
        compute='_compute_treasury_movement_count'
    )
    
    # Validation
    validated_by_id = fields.Many2one(
        'res.users',
        string='Validé par',
        readonly=True,
        tracking=True
    )
    
    validated_date = fields.Datetime(
        string='Date de Validation',
        readonly=True,
        tracking=True
    )
    
    approved_by_id = fields.Many2one(
        'res.users',
        string='Approuvé par',
        readonly=True,
        tracking=True
    )
    
    approved_date = fields.Datetime(
        string='Date d\'Approbation',
        readonly=True,
        tracking=True
    )
    
    # Planification
    planned_payment_date = fields.Date(
        string='Date de Paiement Planifiée',
        tracking=True
    )
    
    # Paiement
    payment_date = fields.Date(
        string='Date de Paiement',
        tracking=True
    )
    
    payment_account_id = fields.Many2one(
        'kondro.treasury.account',
        string='Compte de Paiement',
        tracking=True
    )
    
    payment_method = fields.Selection([
        ('transfer', 'Virement'),
        ('check', 'Chèque'),
        ('cash', 'Espèces'),
        ('mobile_money', 'Mobile Money')
    ], string='Méthode de Paiement', tracking=True)
    
    @api.depends('treasury_movement_ids.amount', 'treasury_movement_ids.movement_type')
    def _compute_paid_amount(self):
        """Calcule le montant payé depuis les mouvements"""
        for record in self:
            paid = sum(record.treasury_movement_ids.filtered(
                lambda m: m.movement_type == 'out'
            ).mapped('amount'))
            record.paid_amount = paid
    
    def _compute_treasury_movement_count(self):
        """Compte les mouvements de trésorerie"""
        for record in self:
            record.treasury_movement_count = len(record.treasury_movement_ids)
    
    def action_submit(self):
        """Soumet la dépense pour validation"""
        for record in self:
            if record.state != 'draft':
                raise UserError(_("Seules les dépenses en brouillon peuvent être soumises."))
            record.state = 'submitted'
            record.message_post(body=_("Dépense soumise pour validation."))
    
    def action_validate(self):
        """Valide la dépense (par chef de service/projet)"""
        for record in self:
            if record.state != 'submitted':
                raise UserError(_("Seules les dépenses soumises peuvent être validées."))
            record.state = 'validated'
            record.validated_by_id = self.env.user
            record.validated_date = fields.Datetime.now()
            record.message_post(body=_("Dépense validée par %s.") % self.env.user.name)
    
    def action_approve(self):
        """Approuve la dépense (par direction)"""
        for record in self:
            if record.state != 'validated':
                raise UserError(_("Seules les dépenses validées peuvent être approuvées."))
            record.state = 'approved'
            record.approved_by_id = self.env.user
            record.approved_date = fields.Datetime.now()
            record.message_post(body=_("Dépense approuvée par %s.") % self.env.user.name)
    
    def action_plan(self):
        """Planifie le paiement"""
        for record in self:
            if record.state != 'approved':
                raise UserError(_("Seules les dépenses approuvées peuvent être planifiées."))
            if not record.planned_payment_date:
                raise ValidationError(_("La date de paiement planifiée est requise."))
            record.state = 'planned'
            record.message_post(body=_("Paiement planifié pour le %s.") % record.planned_payment_date)
    
    def action_pay(self):
        """Exécute le paiement et crée le mouvement de trésorerie"""
        for record in self:
            if record.state != 'planned':
                raise UserError(_("Seules les dépenses planifiées peuvent être payées."))
            if not record.payment_account_id:
                raise ValidationError(_("Le compte de paiement est requis."))
            
            # Créer le mouvement de trésorerie
            movement = self.env['kondro.treasury.movement'].create({
                'account_id': record.payment_account_id.id,
                'movement_type': 'out',
                'amount': record.estimated_amount,
                'date': record.payment_date or fields.Date.today(),
                'payment_method': record.payment_method or 'transfer',
                'partner_id': record.supplier_id.id or record.employee_id.partner_id.id if record.employee_id else False,
                'reference': record.name,
                'comment': record.description,
                'expense_request_id': record.id,
                'project_id': record.project_id.id if record.expense_type == 'commercial' else False,
            })
            
            record.state = 'paid'
            record.payment_date = record.payment_date or fields.Date.today()
            record.message_post(body=_("Paiement exécuté. Mouvement créé: %s") % movement.name)
    
    def action_close(self):
        """Clôture la dépense"""
        for record in self:
            if record.state != 'paid':
                raise UserError(_("Seules les dépenses payées peuvent être clôturées."))
            record.state = 'closed'
            record.message_post(body=_("Dépense clôturée."))
    
    def action_view_treasury_movements(self):
        """Ouvre la vue des mouvements de trésorerie"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Mouvements de Trésorerie'),
            'res_model': 'kondro.treasury.movement',
            'view_mode': 'tree,form',
            'domain': [('expense_request_id', '=', self.id)],
            'context': {'default_expense_request_id': self.id},
        }
    
    @api.constrains('expense_type', 'project_id', 'department_id')
    def _check_expense_type(self):
        """Vérifie la cohérence du type de dépense"""
        for record in self:
            if record.expense_type == 'commercial' and not record.project_id:
                raise ValidationError(_("Une dépense commerciale doit être liée à un projet."))
            if record.expense_type == 'internal' and not record.department_id:
                raise ValidationError(_("Une dépense interne doit avoir un service demandeur."))

