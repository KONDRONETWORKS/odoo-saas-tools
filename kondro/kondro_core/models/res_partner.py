# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    """Extension des contacts pour KONDRO"""
    _inherit = 'res.partner'

    # Projets liés
    kondro_project_ids = fields.One2many(
        'kondro.project',
        'client_id',
        string='Projets KONDRO'
    )
    
    kondro_project_count = fields.Integer(
        string='Nombre de Projets',
        compute='_compute_kondro_project_count'
    )
    
    # Dossiers commerciaux
    kondro_dossier_ids = fields.One2many(
        'kondro.commercial.dossier',
        'client_id',
        string='Dossiers Commerciaux'
    )
    
    kondro_dossier_count = fields.Integer(
        string='Nombre de Dossiers',
        compute='_compute_kondro_dossier_count'
    )
    
    def _compute_kondro_project_count(self):
        """Compte les projets du client"""
        for record in self:
            record.kondro_project_count = len(record.kondro_project_ids)
    
    def _compute_kondro_dossier_count(self):
        """Compte les dossiers commerciaux du client"""
        for record in self:
            record.kondro_dossier_count = len(record.kondro_dossier_ids)
    
    def action_view_kondro_projects(self):
        """Ouvre la vue des projets du client"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Projets KONDRO',
            'res_model': 'kondro.project',
            'view_mode': 'tree,form,kanban',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }
    
    def action_view_kondro_dossiers(self):
        """Ouvre la vue des dossiers commerciaux du client"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dossiers Commerciaux',
            'res_model': 'kondro.commercial.dossier',
            'view_mode': 'tree,form,kanban',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }

