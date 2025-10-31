from odoo import models, fields, api
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class SaasPortalMonitoring(models.Model):
    _name = 'saas_portal.monitoring'
    _description = 'SaaS Portal Monitoring Metrics'
    _order = 'create_date desc'

    client_id = fields.Many2one(
        'saas_portal.client',
        string='Client',
        required=True,
        ondelete='cascade',
        index=True)
    
    server_id = fields.Many2one(
        'saas_portal.server',
        string='Server',
        related='client_id.server_id',
        store=True,
        readonly=True)
    
    metric_type = fields.Selection([
        ('cpu', 'CPU Usage (%)'),
        ('ram', 'RAM Usage (%)'),
        ('disk', 'Disk Usage (%)'),
        ('response_time', 'Response Time (ms)'),
        ('uptime', 'Uptime'),
        ('error_rate', 'Error Rate (%)'),
        ('active_users', 'Active Users'),
        ('requests', 'Requests/min'),
    ], string='Metric Type', required=True, index=True)
    
    value = fields.Float(
        string='Value',
        required=True,
        digits=(16, 2),
        help='Metric value')
    
    threshold_warning = fields.Float(
        string='Warning Threshold',
        digits=(16, 2),
        help='Warning threshold for this metric')
    
    threshold_critical = fields.Float(
        string='Critical Threshold',
        digits=(16, 2),
        help='Critical threshold for this metric')
    
    status = fields.Selection([
        ('ok', 'OK'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('down', 'Down'),
    ], string='Status', compute='_compute_status', store=True)
    
    timestamp = fields.Datetime(
        string='Timestamp',
        default=fields.Datetime.now,
        required=True,
        index=True)
    
    note = fields.Text(string='Notes')
    
    @api.depends('value', 'threshold_warning', 'threshold_critical')
    def _compute_status(self):
        """Compute status based on value and thresholds"""
        for record in self:
            if record.value == 0 and record.metric_type in ['response_time', 'uptime']:
                record.status = 'down'
            elif record.threshold_critical and record.value >= record.threshold_critical:
                record.status = 'critical'
            elif record.threshold_warning and record.value >= record.threshold_warning:
                record.status = 'warning'
            else:
                record.status = 'ok'

    @api.model
    def collect_metrics(self, client_id):
        """
        Collect metrics for a specific client instance
        This method can be called via RPC from the server
        """
        client = self.env['saas_portal.client'].browse(client_id)
        if not client.exists():
            return False
        
        metrics = {}
        try:
            # Try to get metrics from the server via RPC
            if client.server_id and client.server_id.has_method('get_instance_metrics'):
                metrics = client.server_id.get_instance_metrics(client.name)
            else:
                # Fallback: use basic metrics
                metrics = self._get_basic_metrics(client)
        except Exception as e:
            _logger.error(f"Error collecting metrics for client {client.name}: {e}")
            metrics = self._get_basic_metrics(client)
        
        # Store metrics
        metric_values = {
            'cpu': metrics.get('cpu', 0),
            'ram': metrics.get('ram', 0),
            'disk': metrics.get('disk', 0),
            'response_time': metrics.get('response_time', 0),
            'uptime': metrics.get('uptime', 0),
            'error_rate': metrics.get('error_rate', 0),
            'active_users': metrics.get('active_users', 0),
            'requests': metrics.get('requests', 0),
        }
        
        # Get thresholds from plan
        thresholds = self._get_thresholds(client)
        
        # Create monitoring records
        for metric_type, value in metric_values.items():
            self.create({
                'client_id': client_id,
                'metric_type': metric_type,
                'value': value,
                'threshold_warning': thresholds.get(metric_type, {}).get('warning'),
                'threshold_critical': thresholds.get(metric_type, {}).get('critical'),
            })
        
        return True

    def _get_basic_metrics(self, client):
        """Get basic metrics when RPC is not available"""
        return {
            'cpu': 0,
            'ram': 0,
            'disk': 0,
            'response_time': 0,
            'uptime': 100 if client.state == 'open' else 0,
            'error_rate': 0,
            'active_users': 0,
            'requests': 0,
        }

    def _get_thresholds(self, client):
        """Get thresholds from plan or default values"""
        thresholds = {
            'cpu': {'warning': 70, 'critical': 90},
            'ram': {'warning': 75, 'critical': 90},
            'disk': {'warning': 80, 'critical': 95},
            'response_time': {'warning': 1000, 'critical': 3000},
            'error_rate': {'warning': 1, 'critical': 5},
        }
        
        # TODO: Get thresholds from plan configuration
        return thresholds

    @api.model
    def get_latest_metrics(self, client_id):
        """Get latest metrics for a client"""
        latest = self.search([
            ('client_id', '=', client_id)
        ], limit=8, order='timestamp desc')
        
        return {
            metric.metric_type: {
                'value': metric.value,
                'status': metric.status,
                'timestamp': metric.timestamp,
            }
            for metric in latest
        }

    @api.model
    def get_metrics_history(self, client_id, metric_type, hours=24):
        """Get metrics history for a specific metric type"""
        since = fields.Datetime.now() - timedelta(hours=hours)
        return self.search([
            ('client_id', '=', client_id),
            ('metric_type', '=', metric_type),
            ('timestamp', '>=', since),
        ], order='timestamp asc')

    @api.model
    def clean_old_metrics(self, days=30):
        """Clean monitoring metrics older than specified days"""
        cutoff_date = fields.Datetime.now() - timedelta(days=days)
        old_metrics = self.search([
            ('timestamp', '<', cutoff_date),
        ])
        count = len(old_metrics)
        old_metrics.unlink()
        _logger.info(f"Cleaned {count} monitoring metrics older than {days} days")
        return count

