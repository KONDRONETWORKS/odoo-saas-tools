from odoo import http, fields
from odoo.http import request
import json


class MonitoringController(http.Controller):

    @http.route('/saas_portal/monitoring/metrics/<int:client_id>', 
                type='http', auth='user', methods=['GET'], csrf=False)
    def get_client_metrics(self, client_id, **kwargs):
        """API endpoint to get latest metrics for a client"""
        try:
            client = request.env['saas_portal.client'].browse(client_id)
            if not client.exists():
                return request.make_response(
                    json.dumps({'error': 'Client not found'}),
                    headers=[('Content-Type', 'application/json')],
                    status=404)
            
            monitoring_model = request.env['saas_portal.monitoring']
            metrics = monitoring_model.get_latest_metrics(client_id)
            
            return request.make_response(
                json.dumps({
                    'client_id': client_id,
                    'client_name': client.name,
                    'health_status': client.health_status,
                    'metrics': metrics,
                    'timestamp': fields.Datetime.now().isoformat(),
                }),
                headers=[('Content-Type', 'application/json')])
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers=[('Content-Type', 'application/json')],
                status=500)

    @http.route('/saas_portal/monitoring/health', 
                type='http', auth='public', methods=['GET'], csrf=False)
    def health_check(self, **kwargs):
        """Public health check endpoint"""
        return request.make_response(
            json.dumps({'status': 'ok'}),
            headers=[('Content-Type', 'application/json')])

