# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class KondroCommercialDossier(models.Model):
    """Dossier Commercial KONDRO"""
    _name = 'kondro.commercial.dossier'
    _description = 'Dossier Commercial KONDRO'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(
        string='Numéro du Dossier',
        required=True,
        copy=False,
        index=True,
        tracking=True,
        default=lambda self: _('Nouveau')
    )
    
    # Client
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        tracking=True,
        domain=[('is_company', '=', True)]
    )
    
    # Équipe commerciale
    commercial_id = fields.Many2one(
        'res.users',
        string='Commercial Responsable',
        required=True,
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
    
    # Description du projet
    description = fields.Text(
        string='Description du Projet',
        tracking=True
    )
    
    duration = fields.Char(
        string='Durée de Réalisation',
        tracking=True
    )
    
    # Nature du projet
    nature = fields.Selection([
        ('hardware', 'Vente de Matériel'),
        ('services', 'Vente de Services'),
        ('mixed', 'Mixte'),
    ], string='Nature du Projet', default='services', tracking=True)
    
    # Budget et montants
    budget = fields.Monetary(
        string='Budget Total (XOF)',
        currency_field='currency_id',
        tracking=True
    )
    
    engaged_amount = fields.Monetary(
        string='Montant Engagé',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=False
    )
    
    paid_amount = fields.Monetary(
        string='Montant Payé',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=False
    )
    
    margin = fields.Monetary(
        string='Marge',
        currency_field='currency_id',
        compute='_compute_amounts',
        store=False
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )
    
    # Projets liés
    project_ids = fields.One2many(
        'kondro.project',
        'commercial_dossier_id',
        string='Projets',
        tracking=True
    )
    
    project_count = fields.Integer(
        string='Nombre de Projets',
        compute='_compute_project_count'
    )
    
    # Documents commerciaux
    document_ids = fields.Many2many(
        'ir.attachment',
        'kondro_dossier_document_rel',
        'dossier_id',
        'attachment_id',
        string='Documents',
        tracking=True
    )
    
    document_count = fields.Integer(
        string='Nombre de Documents',
        compute='_compute_document_count'
    )
    
    # Statut
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('proposal', 'Proposition'),
        ('won', 'Gagné'),
        ('in_progress', 'En Cours'),
        ('delivered', 'Livré'),
        ('closed', 'Clôturé'),
        ('lost', 'Perdu')
    ], string='Statut', default='draft', tracking=True)
    
    @api.depends('project_ids')
    def _compute_project_count(self):
        """Compte les projets liés"""
        for record in self:
            record.project_count = len(record.project_ids)
    
    @api.depends('project_ids', 'budget', 'project_ids.engaged_amount', 'project_ids.paid_amount')
    def _compute_amounts(self):
        """Calcule les montants engagés et payés depuis les projets"""
        for record in self:
            engaged = sum(record.project_ids.mapped('engaged_amount'))
            paid = sum(record.project_ids.mapped('paid_amount'))
            
            record.engaged_amount = engaged
            record.paid_amount = paid
            record.margin = (record.budget or 0.0) - engaged
    
    def _compute_document_count(self):
        """Compte les documents liés"""
        for record in self:
            record.document_count = len(record.document_ids) + len(record.message_attachment_ids)
    
    def action_view_projects(self):
        """Ouvre la vue des projets liés"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Projets'),
            'res_model': 'kondro.project',
            'view_mode': 'tree,form,kanban',
            'domain': [('commercial_dossier_id', '=', self.id)],
            'context': {'default_commercial_dossier_id': self.id},
        }
    
    def action_view_documents(self):
        """Ouvre la vue des documents"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Documents'),
            'res_model': 'ir.attachment',
            'view_mode': 'tree,form',
            'domain': ['|',
                ('id', 'in', self.document_ids.ids),
                ('res_model', '=', 'kondro.commercial.dossier'),
                ('res_id', '=', self.id)
            ],
        }
    
    @api.model
    def create(self, vals):
        """Génère automatiquement le numéro de dossier"""
        if vals.get('name', _('Nouveau')) == _('Nouveau'):
            vals['name'] = self.env['ir.sequence'].next_by_code('kondro.commercial.dossier') or _('Nouveau')
        return super().create(vals)

