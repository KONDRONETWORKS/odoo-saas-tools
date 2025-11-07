# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class KondroTreasuryMovement(models.Model):
    """Mouvement de Trésorerie KONDRO"""
    _name = 'kondro.treasury.movement'
    _description = 'Mouvement de Trésorerie KONDRO'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, id desc'

    name = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        index=True,
        default=lambda self: _('Nouveau')
    )
    
    # Compte
    account_id = fields.Many2one(
        'kondro.treasury.account',
        string='Compte',
        required=True,
        tracking=True,
        ondelete='restrict'
    )
    
    account_type = fields.Selection(
        related='account_id.account_type',
        string='Type de Compte',
        store=True,
        readonly=True
    )
    
    # Type de mouvement
    movement_type = fields.Selection([
        ('in', 'Entrée'),
        ('out', 'Sortie')
    ], string='Type', required=True, default='out', tracking=True)
    
    # Montant et date
    amount = fields.Monetary(
        string='Montant (XOF)',
        currency_field='currency_id',
        required=True,
        tracking=True
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        tracking=True,
        index=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        related='account_id.currency_id',
        store=True,
        readonly=True
    )
    
    # Méthode de paiement
    payment_method = fields.Selection([
        ('transfer', 'Virement'),
        ('check', 'Chèque'),
        ('cash', 'Espèces'),
        ('mobile_money', 'Mobile Money'),
        ('other', 'Autre')
    ], string='Méthode de Paiement', required=True, default='transfer', tracking=True)
    
    # Partenaire
    partner_id = fields.Many2one(
        'res.partner',
        string='Bénéficiaire / Payeur',
        tracking=True
    )
    
    # Référence
    reference = fields.Char(
        string='Référence',
        tracking=True,
        help="Référence du paiement (numéro de chèque, virement, etc.)"
    )
    
    # Commentaire
    comment = fields.Text(
        string='Commentaire',
        tracking=True
    )
    
    # Pièces jointes
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'kondro_movement_attachment_rel',
        'movement_id',
        'attachment_id',
        string='Pièces Justificatives',
        tracking=True
    )
    
    # Liens avec dépenses et projets
    expense_request_id = fields.Many2one(
        'kondro.expense.request',
        string='Dépense Liée',
        tracking=True,
        ondelete='set null'
    )
    
    project_id = fields.Many2one(
        'kondro.project',
        string='Projet Lié',
        tracking=True,
        ondelete='set null'
    )
    
    # Saisie
    entered_by_id = fields.Many2one(
        'res.users',
        string='Saisi par',
        default=lambda self: self.env.user,
        readonly=True,
        tracking=True
    )
    
    @api.model
    def create(self, vals):
        """Génère automatiquement la référence"""
        if vals.get('name', _('Nouveau')) == _('Nouveau'):
            seq_code = 'kondro.treasury.movement'
            if vals.get('movement_type') == 'in':
                seq_code = 'kondro.treasury.movement.in'
            elif vals.get('movement_type') == 'out':
                seq_code = 'kondro.treasury.movement.out'
            vals['name'] = self.env['ir.sequence'].next_by_code(seq_code) or _('Nouveau')
        return super().create(vals)
    
    @api.constrains('amount')
    def _check_amount(self):
        """Vérifie que le montant est positif"""
        for record in self:
            if record.amount <= 0:
                raise ValidationError(_("Le montant doit être strictement positif."))

