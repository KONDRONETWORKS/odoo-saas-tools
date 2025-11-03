"""
Configuration Settings for SaaS Portal.
"""
from odoo import api, fields, models


class SaasPortalConfigWizard(models.TransientModel):
    """Configuration wizard for SaaS Portal settings."""
    _inherit = 'res.config.settings'

    base_saas_domain = fields.Char('Base SaaS domain')
    page_for_maximumdb = fields.Char(
        help='Redirection url for maximum non-trial databases limit exception')
    page_for_maximumtrialdb = fields.Char(
        help='Redirection url for maximum trial databases limit exception')
    page_for_nonfree_subdomains = fields.Char(
        help='Redirection url from /page/start when subdomains is not free and not paid')
    expiration_notify_in_advance = fields.Char(
        help='Notify partners when less than defined number of days left before expiration')
    module_saas_portal_sale_online = fields.Boolean(
        string='Sale SaaS from website shop',
        help='Use saas_portal_sale_online module')
    module_saas_server_backup_rotate = fields.Boolean(
        string='Rotate backups',
        help='Use saas_server_backup_rotate module')

    def set_values(self):
        """Save configuration values."""
        super().set_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        old_domain = icp_sudo.get_param("saas_portal.base_saas_domain", "")
        
        icp_sudo.set_param("saas_portal.base_saas_domain", self.base_saas_domain)
        icp_sudo.set_param("saas_portal.page_for_maximumdb", self.page_for_maximumdb)
        icp_sudo.set_param("saas_portal.page_for_maximumtrialdb", self.page_for_maximumtrialdb)
        icp_sudo.set_param("saas_portal.page_for_nonfree_subdomains", self.page_for_nonfree_subdomains)
        icp_sudo.set_param("saas_portal.expiration_notify_in_advance", self.expiration_notify_in_advance)
        
        if self.base_saas_domain and self.base_saas_domain != old_domain:
            self._update_oauth_providers(self.base_saas_domain)
    
    def _update_oauth_providers(self, domain):
        """Update OAuth provider endpoints with the new domain."""
        if not domain:
            return
            
        if domain == 'localhost' or domain.startswith('127.0.0.1') or domain.startswith('localhost'):
            scheme = 'http'
            host = 'localhost:8069'
        elif '.' in domain:
            scheme = 'https' if not domain.startswith('localhost') else 'http'
            host = domain
        else:
            scheme = 'http'
            host = 'localhost:8069'
        
        auth_endpoint = f'{scheme}://{host}/oauth2/auth'
        validation_endpoint = f'{scheme}://{host}/oauth2/tokeninfo'
        
        for provider_xmlid in ['saas_client.saas_oauth_provider', 'saas_server.saas_oauth_provider']:
            try:
                provider = self.env.ref(provider_xmlid, raise_if_not_found=False)
                if provider:
                    provider.sudo().write({
                        'auth_endpoint': auth_endpoint,
                        'validation_endpoint': validation_endpoint,
                    })
            except Exception:
                pass

    @api.model
    def get_values(self):
        """Get configuration values."""
        res = super().get_values()
        icp_sudo = self.env['ir.config_parameter'].sudo()
        res.update(
            base_saas_domain=icp_sudo.get_param('saas_portal.base_saas_domain'),
            page_for_maximumdb=icp_sudo.get_param('saas_portal.page_for_maximumdb'),
            page_for_maximumtrialdb=icp_sudo.get_param('saas_portal.page_for_maximumtrialdb'),
            page_for_nonfree_subdomains=icp_sudo.get_param('saas_portal.page_for_nonfree_subdomains'),
            expiration_notify_in_advance=icp_sudo.get_param('saas_portal.expiration_notify_in_advance'),
        )
        return res
