"""
Extended Ir Config Parameter model for auto-updating OAuth endpoints.
"""
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

BASE_SAAS_DOMAIN = 'saas_portal.base_saas_domain'


class IrConfigParameter(models.Model):
    """Extended ir.config_parameter model."""
    _inherit = 'ir.config_parameter'

    @api.model
    def set_param(self, key, value):
        """Override set_param to auto-update OAuth endpoints."""
        if key == 'web.base.url' and not self.get_param(BASE_SAAS_DOMAIN):
            domain_only = value
            if '/' in domain_only:
                domain_only = domain_only.split('/')[2]
            self.set_param(BASE_SAAS_DOMAIN, domain_only)
        
        if key == BASE_SAAS_DOMAIN and value:
            self._auto_update_oauth_endpoints(value)
        
        return super().set_param(key, value)
    
    def _auto_update_oauth_endpoints(self, domain):
        """Automatically update OAuth provider endpoints based on base_saas_domain."""
        try:
            if domain == 'localhost' or domain.startswith('127.0.0.1') or 'localhost' in domain:
                scheme = 'http'
                host = 'localhost:8069' if ':8069' not in domain else domain
            elif '.' in domain and not domain.startswith('localhost'):
                scheme = 'https' if not domain.startswith('localhost') else 'http'
                host = domain if ':' in domain else f'{domain}:8069'
            else:
                scheme = 'http'
                host = 'localhost:8069'
            
            auth_endpoint = f'{scheme}://{host}/oauth2/auth'
            validation_endpoint = f'{scheme}://{host}/oauth2/tokeninfo'
            
            for provider_xmlid in ['saas_client.saas_oauth_provider', 'saas_server.saas_oauth_provider']:
            try:
                    provider = self.env.ref(provider_xmlid, raise_if_not_found=False)
                if provider and ('odoo.local' in (provider.auth_endpoint or '') or 
                                provider.auth_endpoint != auth_endpoint):
                    provider.sudo().write({
                        'auth_endpoint': auth_endpoint,
                        'validation_endpoint': validation_endpoint,
                    })
                        _logger.info("Updated %s OAuth provider endpoints to %s", provider_xmlid, auth_endpoint)
            except Exception as e:
                    _logger.debug("Could not update %s OAuth provider: %s", provider_xmlid, e)
        except Exception as e:
            _logger.error("Error auto-updating OAuth endpoints: %s", e)
