from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        SaasPortalClient = request.env['saas_portal.client'].sudo()

        instance_count = SaasPortalClient.search_count([
            ('partner_id', '=', partner.id),
        ])

        values.update({
            'instance_count': instance_count,
        })
        return values

    @http.route(['/my/instances', '/my/instances/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_instances(self, page=1, limit=20, **kw):
        """Page avec pagination optimisée"""
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        SaasPortalClient = request.env['saas_portal.client']
        
        # Domaine de recherche
        domain = [('partner_id', '=', partner.id)]
        
        # Compter le total
        total = SaasPortalClient.sudo().search_count(domain)
        
        # Pagination
        limit = int(limit) if limit else 20
        page = int(page)
        offset = (page - 1) * limit
        
        # Rechercher avec pagination
        instances = SaasPortalClient.sudo().search(
            domain, 
            limit=limit, 
            offset=offset,
            order='expiration_datetime desc, name asc'
        )
        
        # Calculer les informations de pagination
        pager = request.website.pager(
            url='/my/instances',
            total=total,
            page=page,
            step=limit,
            url_args=kw
        )
        
        values.update({
            'instances': instances,
            'pager': pager,
        })
        return request.render("saas_portal_client_web.portal_my_instances", values)
    
    @http.route('/saas_portal/api/instances', type='json', auth='user', methods=['POST'])
    def api_get_instances(self, page=1, limit=20, **kw):
        """API JSON pour charger les instances de manière asynchrone"""
        partner = request.env.user.partner_id
        SaasPortalClient = request.env['saas_portal.client']
        
        domain = [('partner_id', '=', partner.id)]
        total = SaasPortalClient.sudo().search_count(domain)
        
        limit = int(limit) if limit else 20
        page = int(page)
        offset = (page - 1) * limit
        
        instances = SaasPortalClient.sudo().search(
            domain,
            limit=limit,
            offset=offset,
            order='expiration_datetime desc, name asc'
        )
        
        # Préparer les données pour JSON
        instances_data = []
        for instance in instances:
            instances_data.append({
                'id': instance.id,
                'name': instance.name,
                'state': instance.state,
                'plan_name': instance.plan_id.name if instance.plan_id else '',
                'expiration_datetime': instance.expiration_datetime.isoformat() if instance.expiration_datetime else None,
                'expired': instance.expired,
                'public_url': instance.public_url if hasattr(instance, 'public_url') else '',
            })
        
        return {
            'instances': instances_data,
            'total': total,
            'page': page,
            'limit': limit,
            'pages': (total + limit - 1) // limit if limit > 0 else 1,
        }

    @http.route("/my/domain/<int:instance_id>", type='http', auth="user", website=True)
    def change_domain(self, instance_id, **post):
        instance = request.env['saas_portal.client'].sudo().browse(instance_id)
        ICPsudo = request.env['ir.config_parameter'].sudo()
        base_saas_domain = ICPsudo.get_param('base_saas_domain')
        values = {
            'domain_name': instance.name,
            'saas_portal_client': instance,
            'base_saas_domain': base_saas_domain,
        }
        return request.render("saas_portal_client_web.change_domain", values)
