"""
SQL optimizations with relation preloading.
"""
from odoo import models, api


class SaasPortalClient(models.Model):
    """SQL optimizations for saas_portal.client."""
    _inherit = 'saas_portal.client'
    
    def read(self, fields=None, load='_classic_read'):
        """Override read() to preload relations."""
        records = super().read(fields=fields, load=load)
        
        if not records:
            return records
        
        requested_fields = fields or []
        
        if 'plan_id' in requested_fields or not fields:
            plan_ids = [r['plan_id'][0] for r in records 
                       if r.get('plan_id') and isinstance(r.get('plan_id'), tuple)]
            if plan_ids:
                self.env['saas_portal.plan'].browse(plan_ids).read(['name', 'state', 'summary'])
        
        if 'server_id' in requested_fields or not fields:
            server_ids = [r['server_id'][0] for r in records 
                         if r.get('server_id') and isinstance(r.get('server_id'), tuple)]
            if server_ids:
                self.env['saas_portal.server'].browse(server_ids).read(['name', 'host', 'active'])
        
        if 'partner_id' in requested_fields or not fields:
            partner_ids = [r['partner_id'][0] for r in records 
                          if r.get('partner_id') and isinstance(r.get('partner_id'), tuple)]
            if partner_ids:
                self.env['res.partner'].browse(partner_ids).read(['name', 'email'])
        
        return records
    
    @api.model
    def _read_group(self, domain, groupby, aggregates, having, offset=0, limit=None, order=None):
        """Optimize groupings with preloading."""
        result = super()._read_group(domain, groupby, aggregates, having, offset, limit, order)
        
        if isinstance(result, list) and result:
            for group in result:
                if isinstance(group, dict):
                    if 'plan_id' in group:
                        plan_id = group['plan_id']
                        if plan_id and isinstance(plan_id, (list, tuple)):
                            self.env['saas_portal.plan'].browse(plan_id[0]).read(['name'])
                    
                    if 'server_id' in group:
                        server_id = group['server_id']
                        if server_id and isinstance(server_id, (list, tuple)):
                            self.env['saas_portal.server'].browse(server_id[0]).read(['name'])
        
        return result
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        """Optimize search_read with preloading."""
        records = self.search(domain or [], offset=offset, limit=limit, order=order)
        return records.read(fields=fields)


class SaasPortalPlan(models.Model):
    """SQL optimizations for saas_portal.plan."""
    _inherit = 'saas_portal.plan'
    
    def read(self, fields=None, load='_classic_read'):
        """Override read() to preload relations."""
        records = super().read(fields=fields, load=load)
        
        if not records:
            return records
        
        requested_fields = fields or []
        
        if 'template_id' in requested_fields or not fields:
            template_ids = [r['template_id'][0] for r in records 
                           if r.get('template_id') and isinstance(r.get('template_id'), tuple)]
            if template_ids:
                self.env['saas_portal.database'].browse(template_ids).read(['name', 'state'])
        
        if 'server_id' in requested_fields or not fields:
            server_ids = [r['server_id'][0] for r in records 
                         if r.get('server_id') and isinstance(r.get('server_id'), tuple)]
            if server_ids:
                self.env['saas_portal.server'].browse(server_ids).read(['name', 'host'])
        
        return records


class SaasPortalServer(models.Model):
    """SQL optimizations for saas_portal.server."""
    _inherit = 'saas_portal.server'
    
    def read(self, fields=None, load='_classic_read'):
        """Override read() to preload relations."""
        records = super().read(fields=fields, load=load)
        
        if not records:
            return records
        
        requested_fields = fields or []
        
        if 'oauth_application_id' in requested_fields or not fields:
            oauth_ids = [r['oauth_application_id'][0] for r in records 
                        if r.get('oauth_application_id') and isinstance(r.get('oauth_application_id'), tuple)]
            if oauth_ids:
                self.env['oauth.application'].browse(oauth_ids).read(['client_id'])
        
        return records
