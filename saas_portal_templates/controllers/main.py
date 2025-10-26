from odoo import http
from odoo.http import request
from odoo.addons.saas_portal.controllers.main import SaasPortal as saas_portal_controller


class SaasPortalTemplates(saas_portal_controller):

    @http.route(['/saas_portal_templates/select-template'], type='http', auth='public', website=True)
    def select_template(self, **post):
        domain = [('state', 'in', ['confirmed'])]
        fields = ['id', 'name', 'summary']
        templates = request.env['saas_portal.plan'].sudo().search_read(domain=domain, fields=fields)
        values = {'templates': templates}
        return request.website.render("saas_portal_templates.select_template", values)

    @http.route(['/saas_portal_templates/new_database'], type='http', auth='public', website=True)
    def new_database(self, **post):
        if not request.session.uid:
            # Redirection vers la page de login si l'utilisateur n'est pas connecté
            redirect = str('/saas_portal_templates/new_database?' + request.httprequest.query_string.decode('utf-8'))
            query = {'redirect': redirect}
            return http.local_redirect(path='/web/login', query=query)
        plan_id = int(post.get('plan_id'))

        res = self.create_new_database(plan_id)
        return request.redirect(res.get('url'))
