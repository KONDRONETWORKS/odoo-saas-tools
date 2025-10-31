from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SaasPortalQuotaUsage(models.Model):
    _name = 'saas_portal.quota_usage'
    _description = 'SaaS Portal Quota Usage Tracking'
    _order = 'create_date desc'

    client_id = fields.Many2one(
        'saas_portal.client',
        string='Client',
        required=True,
        ondelete='cascade',
        index=True)
    
    quota_type = fields.Selection([
        ('users', 'Users'),
        ('storage', 'Storage (MB)'),
        ('api_calls_hour', 'API Calls/Hour'),
        ('api_calls_day', 'API Calls/Day'),
        ('modules', 'Modules'),
        ('records', 'Records'),
        ('bandwidth', 'Bandwidth (MB)'),
    ], string='Quota Type', required=True, index=True)
    
    current_usage = fields.Float(
        string='Current Usage',
        required=True,
        digits=(16, 2),
        help='Current usage value')
    
    limit = fields.Float(
        string='Limit',
        required=True,
        digits=(16, 2),
        help='Quota limit (0 = unlimited)')
    
    usage_percentage = fields.Float(
        string='Usage %',
        compute='_compute_usage_percentage',
        store=True,
        digits=(16, 2),
        help='Usage percentage')
    
    status = fields.Selection([
        ('ok', 'OK'),
        ('alert', 'Alert Sent'),
        ('warning', 'Warning'),
        ('blocked', 'Blocked'),
    ], string='Status', compute='_compute_status', store=True)
    
    timestamp = fields.Datetime(
        string='Timestamp',
        default=fields.Datetime.now,
        required=True,
        index=True)
    
    alert_sent = fields.Boolean(
        string='Alert Sent',
        default=False,
        help='Alert has been sent for this quota')

    @api.depends('current_usage', 'limit')
    def _compute_usage_percentage(self):
        """Compute usage percentage"""
        for record in self:
            if record.limit > 0:
                record.usage_percentage = (record.current_usage / record.limit) * 100
            else:
                record.usage_percentage = 0

    @api.depends('usage_percentage', 'client_id.plan_id')
    def _compute_status(self):
        """Compute status based on usage and plan thresholds"""
        for record in self:
            if not record.client_id.plan_id:
                record.status = 'ok'
                continue
            
            plan = record.client_id.plan_id
            percentage = record.usage_percentage
            
            if plan.quota_block_percentage and percentage >= plan.quota_block_percentage:
                record.status = 'blocked'
            elif plan.quota_warning_percentage and percentage >= plan.quota_warning_percentage:
                record.status = 'warning'
            elif plan.quota_alert_percentage and percentage >= plan.quota_alert_percentage:
                record.status = 'alert'
            else:
                record.status = 'ok'

    @api.model
    def update_quota_usage(self, client_id, quota_type, usage_value):
        """Update quota usage for a client"""
        client = self.env['saas_portal.client'].browse(client_id)
        if not client.exists() or not client.plan_id:
            return False
        
        plan = client.plan_id
        
        # Get limit from plan
        limits = {
            'users': plan.quota_max_users or 0,
            'storage': plan.quota_max_storage_mb or 0,
            'api_calls_hour': plan.quota_max_api_calls_per_hour or 0,
            'api_calls_day': plan.quota_max_api_calls_per_day or 0,
            'modules': plan.quota_max_modules or 0,
            'bandwidth': plan.quota_bandwidth_mb_per_month or 0,
        }
        
        limit = limits.get(quota_type, 0)
        
        # Create or update usage record
        existing = self.search([
            ('client_id', '=', client_id),
            ('quota_type', '=', quota_type),
        ], limit=1, order='timestamp desc')
        
        vals = {
            'client_id': client_id,
            'quota_type': quota_type,
            'current_usage': usage_value,
            'limit': limit,
            'timestamp': fields.Datetime.now(),
        }
        
        if existing:
            existing.write(vals)
            record = existing
        else:
            record = self.create(vals)
        
        # Check if alert/warning/block should be triggered
        record._check_quota_thresholds()
        
        return record

    def _check_quota_thresholds(self):
        """Check if quota thresholds are reached and trigger actions"""
        for record in self:
            if not record.client_id.plan_id:
                continue
            
            plan = record.client_id.plan_id
            percentage = record.usage_percentage
            
            # Check if blocked
            if plan.quota_block_percentage and percentage >= plan.quota_block_percentage:
                if record.status != 'blocked':
                    record._trigger_block()
            
            # Check if warning
            elif plan.quota_warning_percentage and percentage >= plan.quota_warning_percentage:
                if record.status not in ('warning', 'blocked'):
                    record._trigger_warning()
            
            # Check if alert
            elif plan.quota_alert_percentage and percentage >= plan.quota_alert_percentage:
                if not record.alert_sent:
                    record._trigger_alert()
                    record.alert_sent = True

    def _trigger_alert(self):
        """Trigger alert when quota reaches alert threshold"""
        # This will be handled by base_automation
        _logger.info(f"Quota alert for client {self.client_id.name}, type {self.quota_type}")

    def _trigger_warning(self):
        """Trigger warning when quota reaches warning threshold"""
        _logger.warning(f"Quota warning for client {self.client_id.name}, type {self.quota_type}")

    def _trigger_block(self):
        """Trigger block when quota reaches block threshold"""
        _logger.error(f"Quota block for client {self.client_id.name}, type {self.quota_type}")
        # Mark client as blocked if needed
        if self.quota_type == 'users' and self.client_id.plan_id.quota_enforce_users:
            self.client_id.write({'state': 'blocked'})

    @api.model
    def get_current_usage(self, client_id):
        """Get current quota usage for a client"""
        usages = self.search([
            ('client_id', '=', client_id),
        ], order='timestamp desc', limit=10)
        
        result = {}
        for usage in usages:
            if usage.quota_type not in result:
                result[usage.quota_type] = {
                    'current': usage.current_usage,
                    'limit': usage.limit,
                    'percentage': usage.usage_percentage,
                    'status': usage.status,
                }
        
        return result

