# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class KondroTreasuryAccount(models.Model):
    """Compte de Trésorerie KONDRO (Banque, Caisse, Djamo)"""
    _name = 'kondro.treasury.account'
    _description = 'Compte de Trésorerie KONDRO'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(
        string='Nom du Compte',
        required=True,
        tracking=True
    )
    
    account_type = fields.Selection([
        ('bank', 'Banque'),
        ('cash', 'Caisse'),
        ('djamo', 'Djamo'),
        ('other', 'Autre')
    ], string='Type de Compte', required=True, default='bank', tracking=True)
    
    sequence = fields.Integer(
        string='Séquence',
        default=10
    )
    
    # Solde
    initial_balance = fields.Monetary(
        string='Solde Initial (XOF)',
        currency_field='currency_id',
        default=0.0,
        tracking=True
    )
    
    current_balance = fields.Monetary(
        string='Solde Courant (XOF)',
        currency_field='currency_id',
        compute='_compute_current_balance',
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id,
        required=True
    )
    
    # Mouvements
    movement_ids = fields.One2many(
        'kondro.treasury.movement',
        'account_id',
        string='Mouvements',
        readonly=True
    )
    
    movement_count = fields.Integer(
        string='Nombre de Mouvements',
        compute='_compute_movement_count'
    )
    
    # Comptabilité
    account_id = fields.Many2one(
        'account.account',
        string='Compte Comptable',
        domain=[('deprecated', '=', False)],
        help="Compte comptable associé pour l'intégration comptable"
    )
    
    active = fields.Boolean(
        string='Actif',
        default=True
    )
    
    @api.depends('initial_balance', 'movement_ids.amount', 'movement_ids.movement_type')
    def _compute_current_balance(self):
        """Calcule le solde courant : solde initial + entrées - sorties"""
        for record in self:
            balance = record.initial_balance
            for movement in record.movement_ids:
                if movement.movement_type == 'in':
                    balance += movement.amount
                elif movement.movement_type == 'out':
                    balance -= movement.amount
            record.current_balance = balance
    
    def _compute_movement_count(self):
        """Compte les mouvements"""
        for record in self:
            record.movement_count = len(record.movement_ids)
    
    def action_view_movements(self):
        """Ouvre la vue des mouvements du compte"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Mouvements'),
            'res_model': 'kondro.treasury.movement',
            'view_mode': 'tree,form',
            'domain': [('account_id', '=', self.id)],
            'context': {'default_account_id': self.id},
        }

