from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'

    # Quota usage fields
    quota_usage_ids = fields.One2many(
        'saas_portal.quota_usage',
        'client_id',
        string='Quota Usage',
        readonly=True)
    
    quota_current_users = fields.Integer(
        string='Current Users',
        compute='_compute_quota_usage',
        store=False,
        help='Current number of users')
    
    quota_current_storage_mb = fields.Float(
        string='Current Storage (MB)',
        compute='_compute_quota_usage',
        store=False,
        digits=(16, 2),
        help='Current storage usage in MB')
    
    quota_status_overall = fields.Selection([
        ('ok', 'OK'),
        ('alert', 'Alert'),
        ('warning', 'Warning'),
        ('blocked', 'Blocked'),
    ], string='Quota Status',
        compute='_compute_quota_status',
        store=False,
        help='Overall quota status')

    @api.depends('quota_usage_ids')
    def _compute_quota_usage(self):
        """Compute current quota usage from latest usage records"""
        quota_model = self.env['saas_portal.quota_usage']
        for client in self:
            current_usage = quota_model.get_current_usage(client.id)
            
            client.quota_current_users = int(current_usage.get('users', {}).get('current', 0))
            client.quota_current_storage_mb = current_usage.get('storage', {}).get('current', 0)

    @api.depends('quota_usage_ids.status')
    def _compute_quota_status(self):
        """Compute overall quota status"""
        for client in self:
            statuses = client.quota_usage_ids.mapped('status')
            if 'blocked' in statuses:
                client.quota_status_overall = 'blocked'
            elif 'warning' in statuses:
                client.quota_status_overall = 'warning'
            elif 'alert' in statuses:
                client.quota_status_overall = 'alert'
            else:
                client.quota_status_overall = 'ok'

    def check_quota(self, quota_type, required_value=1):
        """
        Check if quota allows an operation
        
        :param quota_type: Type of quota to check
        :param required_value: Value required for the operation
        :return: True if allowed, False if blocked
        :raises: UserError if blocked with message
        """
        self.ensure_one()
        
        if not self.plan_id:
            return True  # No plan = no limits
        
        plan = self.plan_id
        
        # Get current usage
        quota_model = self.env['saas_portal.quota_usage']
        current_usage = quota_model.get_current_usage(self.id)
        
        usage_info = current_usage.get(quota_type, {})
        current = usage_info.get('current', 0)
        limit = usage_info.get('limit', 0)
        status = usage_info.get('status', 'ok')
        
        # No limit
        if limit == 0:
            return True
        
        # Check if operation would exceed limit
        if current + required_value > limit:
            # Check enforcement settings
            enforce = {
                'users': plan.quota_enforce_users,
                'storage': plan.quota_enforce_storage,
                'api_calls_hour': plan.quota_enforce_api,
                'api_calls_day': plan.quota_enforce_api,
                'modules': plan.quota_enforce_modules,
            }.get(quota_type, True)
            
            if enforce:
                quota_names = {
                    'users': 'utilisateurs',
                    'storage': 'stockage',
                    'api_calls_hour': 'appels API/heure',
                    'api_calls_day': 'appels API/jour',
                    'modules': 'modules',
                }
                raise UserError(
                    f"Limite de {quota_names.get(quota_type, quota_type)} atteinte!\n"
                    f"Utilisation actuelle: {current}/{limit}\n"
                    f"Veuillez passer à un plan supérieur.")
            
        # Check if blocked
        if status == 'blocked':
            raise UserError("Ce quota est actuellement bloqué. Veuillez contacter le support.")
        
        return True

    def update_quota_usage(self, quota_type, usage_value):
        """Update quota usage for this client"""
        self.ensure_one()
        quota_model = self.env['saas_portal.quota_usage']
        return quota_model.update_quota_usage(self.id, quota_type, usage_value)

    def action_refresh_quotas(self):
        """Manually refresh quota usage"""
        self.ensure_one()
        
        # This would typically call the server to get current usage
        # For now, we'll just sync with existing data
        if self.users_len:
            self.update_quota_usage('users', self.users_len)
        
        if self.file_storage or self.db_storage:
            total_storage = (self.file_storage or 0) + (self.db_storage or 0)
            self.update_quota_usage('storage', total_storage)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Quotas Refreshed',
                'message': 'Quota usage has been refreshed.',
                'type': 'success',
                'sticky': False,
            }
        }

    def action_view_quota_usage(self):
        """Open quota usage view for this client"""
        self.ensure_one()
        return {
            'name': f'Quota Usage - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'saas_portal.quota_usage',
            'view_mode': 'list,graph,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }

    def action_upgrade_plan(self):
        """Action to upgrade to higher plan"""
        self.ensure_one()
        if not self.plan_id.quota_upgrade_plan_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Upgrade Available',
                    'message': 'No upgrade plan configured for this plan.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        # Open upgrade wizard or action
        return {
            'type': 'ir.actions.act_window',
            'name': 'Upgrade Plan',
            'res_model': 'saas_portal.client',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

