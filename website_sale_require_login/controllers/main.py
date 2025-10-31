from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleRequireLogin(WebsiteSale):

    def _check_require_login(self):
        """Check if login is required and redirect if needed"""
        require_login = request.env['ir.config_parameter'].sudo().get_param('website_sale.require_login', False)
        
        if require_login and request.env.user._is_public():
            # User is anonymous and login is required, redirect to login
            return request.redirect('/web/login?redirect=' + request.httprequest.path)
        return False

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        """Override shop route to require login"""
        redirect = self._check_require_login()
        if redirect:
            return redirect
        return super().shop(page=page, category=category, search=search, ppg=ppg, **post)

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        """Override product route to require login"""
        redirect = self._check_require_login()
        if redirect:
            return redirect
        return super().product(product=product, category=category, search=search, **kwargs)

