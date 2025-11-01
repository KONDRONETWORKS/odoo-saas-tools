from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

BASE_SAAS_DOMAIN = 'saas_portal.base_saas_domain'


class IrConfigParameter(models.Model):

    _inherit = 'ir.config_parameter'

    @api.model
    def set_param(self, key, value):
        if key == 'web.base.url' and not self.get_param(BASE_SAAS_DOMAIN):
            domain_only = value
            if '/' in domain_only:
                # get rid of "http(s)://" at the beggining and "/" and the end if any
                domain_only = domain_only.split('/')[2]
            self.set_param(BASE_SAAS_DOMAIN, domain_only)
        
        # Auto-update OAuth endpoints when base_saas_domain is set
        if key == BASE_SAAS_DOMAIN and value:
            self._auto_update_oauth_endpoints(value)
        
        return super(IrConfigParameter, self).set_param(key, value)
    
    def _auto_update_oauth_endpoints(self, domain):
        """Automatically update OAuth provider endpoints based on base_saas_domain"""
        try:
            # Determine scheme and host
            if domain == 'localhost' or domain.startswith('127.0.0.1') or 'localhost' in domain:
                scheme = 'http'
                host = 'localhost:8069' if ':8069' not in domain else domain
            elif '.' in domain and not domain.startswith('localhost'):
                # Full domain like odoo.com
                scheme = 'https' if not domain.startswith('localhost') else 'http'
                host = domain if ':' in domain else f'{domain}:8069'
            else:
                # Simple domain like 'odoo' - use localhost for local dev
                scheme = 'http'
                host = 'localhost:8069'
            
            auth_endpoint = f'{scheme}://{host}/oauth2/auth'
            validation_endpoint = f'{scheme}://{host}/oauth2/tokeninfo'
            
            # Update saas_client OAuth provider if exists and still has odoo.local
            try:
                provider = self.env.ref('saas_client.saas_oauth_provider', raise_if_not_found=False)
                if provider and ('odoo.local' in (provider.auth_endpoint or '') or 
                                provider.auth_endpoint != auth_endpoint):
                    provider.sudo().write({
                        'auth_endpoint': auth_endpoint,
                        'validation_endpoint': validation_endpoint,
                    })
                    _logger.info(f"Updated saas_client OAuth provider endpoints to {auth_endpoint}")
            except Exception as e:
                _logger.debug(f"Could not update saas_client OAuth provider: {e}")
            
            # Update saas_server OAuth provider if exists and still has odoo.local
            try:
                provider = self.env.ref('saas_server.saas_oauth_provider', raise_if_not_found=False)
                if provider and ('odoo.local' in (provider.auth_endpoint or '') or 
                                provider.auth_endpoint != auth_endpoint):
                    provider.sudo().write({
                        'auth_endpoint': auth_endpoint,
                        'validation_endpoint': validation_endpoint,
                    })
                    _logger.info(f"Updated saas_server OAuth provider endpoints to {auth_endpoint}")
            except Exception as e:
                _logger.debug(f"Could not update saas_server OAuth provider: {e}")
        except Exception as e:
            _logger.error(f"Error auto-updating OAuth endpoints: {e}")
