"""
Modèle pour enregistrer les erreurs et faciliter le debugging
"""
from odoo import models, fields, api, _
from datetime import datetime
import json


class SaasErrorLog(models.Model):
    _name = 'saas.error.log'
    _description = 'SaaS Error Log'
    _order = 'create_date desc'
    
    name = fields.Char(string='Error ID', compute='_compute_name', store=True)
    operation = fields.Char(string='Operation', required=True, index=True)
    error_message = fields.Text(string='Error Message', required=True)
    traceback = fields.Text(string='Traceback')
    error_type = fields.Char(string='Error Type', compute='_compute_error_type', store=True)
    
    # Contexte
    user_id = fields.Many2one('res.users', string='User', index=True)
    partner_id = fields.Many2one('res.partner', string='Partner', index=True)
    database = fields.Char(string='Database', index=True)
    plan_id = fields.Many2one('saas_portal.plan', string='Plan', index=True)
    server_id = fields.Many2one('saas_portal.server', string='Server', index=True)
    
    # Données additionnelles
    context_data = fields.Text(string='Context Data (JSON)')
    request_url = fields.Char(string='Request URL')
    request_method = fields.Char(string='Request Method')
    request_params = fields.Text(string='Request Parameters')
    
    # Statut
    state = fields.Selection([
        ('new', 'New'),
        ('investigating', 'Investigating'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    ], string='State', default='new', index=True)
    
    resolution = fields.Text(string='Resolution Notes')
    resolved_by = fields.Many2one('res.users', string='Resolved By')
    resolved_date = fields.Datetime(string='Resolved Date')
    
    # Ticket
    ticket_id = fields.Char(string='Ticket ID')
    ticket_url = fields.Char(string='Ticket URL')
    
    # Métadonnées
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity', default='medium', index=True)
    
    occurrence_count = fields.Integer(string='Occurrence Count', default=1)
    first_occurrence = fields.Datetime(string='First Occurrence', default=fields.Datetime.now)
    last_occurrence = fields.Datetime(string='Last Occurrence', default=fields.Datetime.now)
    
    @api.depends('error_message')
    def _compute_error_type(self):
        """Déduire le type d'erreur du message"""
        for record in self:
            msg = record.error_message or ''
            if 'MaximumDBException' in msg or 'maximum' in msg.lower():
                record.error_type = 'MaximumDBException'
            elif 'MaximumTrialDBException' in msg or 'trial' in msg.lower():
                record.error_type = 'MaximumTrialDBException'
            elif 'SuspendedDBException' in msg or 'suspended' in msg.lower():
                record.error_type = 'SuspendedDBException'
            elif 'auth' in msg.lower() or 'authentication' in msg.lower():
                record.error_type = 'AuthenticationError'
            elif 'permission' in msg.lower() or 'access' in msg.lower():
                record.error_type = 'PermissionError'
            else:
                record.error_type = 'GenericError'
    
    @api.depends('create_date', 'operation', 'error_type')
    def _compute_name(self):
        """Générer un nom unique pour l'erreur"""
        for record in self:
            if record.create_date:
                timestamp = record.create_date.strftime('%Y%m%d-%H%M%S')
                error_type = (record.error_type or 'ERROR')[:20]
                op = (record.operation or 'UNKNOWN')[:20]
                record.name = f"{error_type}-{op}-{timestamp}"
            else:
                record.name = f"ERROR-{record.id}"
    
    def get_context_dict(self):
        """Retourner le contexte sous forme de dictionnaire"""
        if self.context_data:
            try:
                return json.loads(self.context_data)
            except:
                return {}
        return {}
    
    def action_create_ticket(self):
        """Créer un ticket de support pour cette erreur"""
        self.ensure_one()
        
        # Préparer les informations du ticket
        ticket_data = {
            'subject': f"[SaaS Error] {self.error_type} - {self.operation}",
            'description': f"""
Error Details:
- Type: {self.error_type}
- Operation: {self.operation}
- Message: {self.error_message}
- Database: {self.database or 'N/A'}
- User: {self.user_id.name if self.user_id else 'N/A'}
- Occurrence: {self.occurrence_count} times
- First seen: {self.first_occurrence}
- Last seen: {self.last_occurrence}

Traceback:
{self.traceback or 'N/A'}

Context:
{json.dumps(self.get_context_dict(), indent=2)}
""",
            'partner_id': self.partner_id.id if self.partner_id else False,
            'user_id': self.user_id.id if self.user_id else False,
        }
        
        # Créer le ticket (à adapter selon votre système de tickets)
        # Exemple avec helpdesk module si disponible
        try:
            ticket = self.env['helpdesk.ticket'].create(ticket_data)
            self.write({
                'ticket_id': str(ticket.id),
                'ticket_url': f"/helpdesk/ticket/{ticket.id}",
                'state': 'investigating'
            })
            return {
                'type': 'ir.actions.act_window',
                'name': 'Ticket Created',
                'res_model': 'helpdesk.ticket',
                'res_id': ticket.id,
                'view_mode': 'form',
                'target': 'current',
            }
        except:
            # Si helpdesk n'est pas disponible, retourner une action pour créer manuellement
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Ticket Creation'),
                    'message': _('Please create a ticket manually with the error details.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }
    
    def action_resolve(self):
        """Marquer l'erreur comme résolue"""
        self.ensure_one()
        self.write({
            'state': 'resolved',
            'resolved_by': self.env.user.id,
            'resolved_date': fields.Datetime.now()
        })
    
    def action_ignore(self):
        """Ignorer cette erreur"""
        self.ensure_one()
        self.write({'state': 'ignored'})
    
    @api.model
    def create(self, vals):
        """Surcharger create pour gérer les doublons"""
        # Vérifier si une erreur similaire existe déjà
        domain = [
            ('operation', '=', vals.get('operation')),
            ('error_message', '=', vals.get('error_message')),
            ('state', 'in', ['new', 'investigating'])
        ]
        existing = self.search(domain, limit=1)
        
        if existing:
            # Incrémenter le compteur d'occurrences
            existing.write({
                'occurrence_count': existing.occurrence_count + 1,
                'last_occurrence': fields.Datetime.now(),
                'traceback': vals.get('traceback', existing.traceback),  # Garder la dernière traceback
            })
            return existing
        else:
            # Créer une nouvelle entrée
            return super().create(vals)

