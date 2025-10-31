from odoo import models, fields, api
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'

    # Fields for monitoring
    last_health_check = fields.Datetime(
        string='Last Health Check',
        readonly=True,
        help='Last time health check was performed')
    
    health_status = fields.Selection([
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('down', 'Down'),
        ('unknown', 'Unknown'),
    ], string='Health Status', default='unknown', readonly=True)
    
    cpu_usage = fields.Float(
        string='CPU Usage (%)',
        readonly=True,
        digits=(16, 2),
        help='Current CPU usage percentage')
    
    ram_usage = fields.Float(
        string='RAM Usage (%)',
        readonly=True,
        digits=(16, 2),
        help='Current RAM usage percentage')
    
    disk_usage = fields.Float(
        string='Disk Usage (%)',
        readonly=True,
        digits=(16, 2),
        help='Current disk usage percentage')
    
    response_time = fields.Float(
        string='Response Time (ms)',
        readonly=True,
        digits=(16, 2),
        help='Average response time in milliseconds')
    
    uptime_percentage = fields.Float(
        string='Uptime (%)',
        readonly=True,
        digits=(16, 2),
        help='Uptime percentage over last 24 hours')
    
    active_users_count = fields.Integer(
        string='Active Users',
        readonly=True,
        help='Number of active users')
    
    monitoring_enabled = fields.Boolean(
        string='Monitoring Enabled',
        default=True,
        help='Enable monitoring for this client')
    
    monitoring_metrics_ids = fields.One2many(
        'saas_portal.monitoring',
        'client_id',
        string='Monitoring Metrics',
        readonly=True)

    def action_collect_metrics(self):
        """Action to manually collect metrics for this client"""
        self.ensure_one()
        if not self.monitoring_enabled:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Monitoring Disabled',
                    'message': 'Monitoring is disabled for this client.',
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        monitoring_model = self.env['saas_portal.monitoring']
        result = monitoring_model.collect_metrics(self.id)
        
        if result:
            # Update client fields with latest metrics
            latest = monitoring_model.get_latest_metrics(self.id)
            
            self.write({
                'last_health_check': fields.Datetime.now(),
                'cpu_usage': latest.get('cpu', {}).get('value', 0),
                'ram_usage': latest.get('ram', {}).get('value', 0),
                'disk_usage': latest.get('disk', {}).get('value', 0),
                'response_time': latest.get('response_time', {}).get('value', 0),
                'active_users_count': int(latest.get('active_users', {}).get('value', 0)),
                'health_status': self._compute_health_status(latest),
            })
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Metrics Collected',
                    'message': 'Metrics successfully collected.',
                    'type': 'success',
                    'sticky': False,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'Failed to collect metrics.',
                    'type': 'danger',
                    'sticky': False,
                }
            }

    def _compute_health_status(self, metrics):
        """Compute overall health status from metrics"""
        if not metrics:
            return 'unknown'
        
        statuses = [metric.get('status', 'ok') for metric in metrics.values()]
        
        if 'critical' in statuses or 'down' in statuses:
            return 'critical'
        elif 'warning' in statuses:
            return 'warning'
        else:
            return 'healthy'

    def action_view_metrics(self):
        """Open metrics view for this client"""
        self.ensure_one()
        return {
            'name': f'Monitoring Metrics - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'saas_portal.monitoring',
            'view_mode': 'tree,graph,form',
            'domain': [('client_id', '=', self.id)],
            'context': {'default_client_id': self.id},
        }

    @api.model
    def collect_all_metrics(self):
        """Collect metrics for all clients with monitoring enabled"""
        clients = self.search([
            ('state', '=', 'open'),
            ('monitoring_enabled', '=', True),
        ])
        
        monitoring_model = self.env['saas_portal.monitoring']
        for client in clients:
            try:
                monitoring_model.collect_metrics(client.id)
            except Exception as e:
                _logger.error(f"Error collecting metrics for client {client.name}: {e}")
        
        return True

