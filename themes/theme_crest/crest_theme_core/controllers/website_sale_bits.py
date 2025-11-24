# -*- coding: utf-8 -*-
from odoo import http, fields, _
import json
 
from odoo.http import request
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.variant import WebsiteSaleVariantController
from datetime import datetime, timedelta
import random

class WebsiteSaleBits(http.Controller):
    @http.route(['/product/get_quick_view_data'], type='json', auth="public", website=True)
    def get_quick_view_data(self, product_id=None):
        if product_id:
            product = request.env['product.template'].search([['id', '=', product_id]])
            website = request.website
            theme_config = request.env['theme.configuration'].sudo().search([('website_id','=',website.id)],limit=1)
            fields = ['']
            if len(theme_config):
                theme_config = theme_config.search_read()[0]
            else:
                theme_config = {
                    'product_offers':False, 'product_tags':True, 'product_faq':True, 'product_sku':True, 'product_sharing':True, 'product_conditions':True,
                    'product_brand_detail':True, 'product_review_tab':False, 'product_sticky_view':True, 'enable_lazyload_image':True, 'card_rattings':False,
                    'card_product_lbl':True
                }

            response = http.Response(template="theme_crest.product_quick_view_bits", qcontext={'product': product,'theme_config':theme_config})
            return response.render()

    @http.route(['/get/dialog/data'], type='json', auth="public", website=True)
    def get_dialog_data(self, record_id, dialog_type):
        response = {'dialog_body':''}
        if dialog_type == 'attribute':
            attr_obj = request.env['product.attrib.details.bits'].sudo().search([('id','=',record_id)])
            if len(attr_obj):
                response['dialog_body'] = attr_obj.attribute_details
        
        if dialog_type == 'offer':
            offer_obj = request.env['product.offers.bits'].sudo().search([('id','=',record_id)])
            if len(offer_obj):
                response['dialog_body'] = offer_obj.offer_details
        return response

    @http.route(['/check/activity_menu'], type='json', auth="user", website=True)
    def check_activity_menu(self):
        return {'active':False}

    @http.route('/our/brands', type='http', auth='public', website=True)
    def brand_page(self, **kwargs):
        # Initialize the values dictionary
        vals = {
            'filter_btn' : ['All','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z','0-9']
        }
         
        aplha_default = request.env['product.brands'].sudo().search([], order='name asc')
        # Get the 'alpha' parameter from the request
        alpha = kwargs.get('alpha')

        if alpha and alpha != 'All':
            if alpha == '0-9':
                # Filter brands with names starting with any digit (0-9)
                brands = request.env['product.brands'].sudo().search([('name', '>=', '0'), ('name', '<=', '9Z')], order='name asc')
            else:
                # Filter brands that start with the given letter (case-insensitive)
                brands = request.env['product.brands'].sudo().search([('name', '=ilike', f'{alpha}%')], order='name asc')
            vals['active_alpha'] = alpha
        else:
            # If no specific letter is provided or 'All' is selected, show all brands
            brands = request.env['product.brands'].sudo().search([], order='name asc')
            vals['active_alpha'] = 'All'
            
        # Add the filtered brands to the values dictionary
        vals['brands'] = brands
        return request.render('crest_theme_core.brand_page_bits', vals)

    @http.route(['/our/collections'], type='http', website=True)
    def our_collections_bits(self, page=1, **kwargs):
        # Define how many items per page
        items_per_page = 6
        page = int(page)  # Ensure 'page' is an integer

        # Calculate the offset based on the current page
        offset = (page - 1) * items_per_page

        # Get the total number of categories
        total_categories = request.env['product.public.category'].sudo().search_count([])

        # Fetch categories for the current page
        categories = request.env['product.public.category'].sudo().search([], limit=items_per_page, offset=offset)

        # Calculate the total number of pages
        total_pages = (total_categories + items_per_page - 1) // items_per_page

        # Determine previous and next page numbers
        previous_page = page - 1 if page > 1 else None
        next_page = page + 1 if page < total_pages else None

        # Generate pagination information
        pager = {
            'previous': f'/our/collections?page={previous_page}' if previous_page else None,
            'next': f'/our/collections?page={next_page}' if next_page else None,
            'currentpage' : page,
            'pages': [
                {'number': p, 'url': f'/our/collections?page={p}', 'current': (p == page)}
                for p in range(1, total_pages + 1)
            ]
        }

        # Pass categories and pager to the template
        vals = {
            'categories': categories,
            'pager': pager,
        }
        return request.render("theme_crest.our_collections_bits", vals)

    @http.route(['/get/cart_notify'], type='json', website=True, auth="public")
    def get_cart_notify(self):
        config = request.website.get_theme_config()
        state = 'draft'
        if config and config.select_when_notify_show != 'on_add_to_cart':
            state = 'sale'

        days_ago = datetime.now() - timedelta(days=8)
        offset = random.randint(1, 10)
        domain = [('order_id.state', '=', state), ('create_date', '>=', days_ago)] 
        cart_line = request.env['sale.order.line'].sudo().search(domain, order='create_date desc', limit=1, offset=offset)
        purchased_time = ''
        user_location_str = ''
        if cart_line:
            # prepare cust location str
            order = cart_line.order_id
            c_name = order.partner_id.name or ''
            c_city = order.partner_id.city or order.partner_id.state_id.name or ''
            state_str = ''
            if state == 'draft':
                state_str = ' added to cart! From'
            else:
                state_str = ' purchased! From '            
            c_country = order.partner_id.country_id.code or ''
            user_location_str = c_name + state_str + c_city + ', ' + c_country
            # calc time 
            time_diff = datetime.now() - order.create_date
            days = time_diff.days
            seconds = time_diff.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60

            if days > 0:
                time_ago = f"{days} day(s) ago"
            elif hours > 0:
                time_ago = f"{hours} hour(s) ago"
            else:
                time_ago = f"{minutes} minute(s) ago"
            purchased_time = time_ago
        #-------  
        view_vals = { 
            'product': cart_line.sudo().product_id,'order': len(cart_line) and cart_line.sudo().order_id.name or False,
            'purchased_time': purchased_time,
            'user_location_str': user_location_str 
        }
        # make cart line notified 
        res_view = request.env['ir.ui.view']._render_template('theme_crest.product_buy_notify_bits',view_vals)
        return {
            'popup_html': res_view, 
            'product_id': len(cart_line) and cart_line.sudo().product_id.id or False,  
        }
        
    @http.route('/get_mini_cart', auth='public', type="json", website=True)
    def mini_cart(self, **kw):
        order = request.website.sale_get_order()
        suggested_products = order.website_order_line.sudo().product_id.mapped('accessory_product_ids').filtered(lambda x: (x.is_published and x.sale_ok) and x.allow_out_of_stock_order)
        context = {'website_sale_order': order,'suggested_products':suggested_products}
        value = { 'mini_cart_lines_bits':request.env["ir.ui.view"]._render_template("theme_crest.mini_cart_lines_bits", context),'mini_cart_bits': request.env["ir.ui.view"]._render_template("theme_crest.mini_cart_bits", context)}
        return value

    @http.route('/as_clear_cart', type="json", auth="public", website=True)
    def as_clear_cart(self, **kw):
        order = request.website.sale_get_order()
        request.session['website_sale_cart_quantity'] = 0
        order.unlink()
        return {'empty_mini_cart': request.env["ir.ui.view"]._render_template("theme_crest.empty_mini_cart_bits")}

class WSVControllerBits(WebsiteSaleVariantController):
    @http.route('/website_sale/get_combination_info', type='json', auth='public', methods=['POST'], website=True)
    def get_combination_info_website(self, product_template_id, product_id, combination, add_qty, parent_combination=None, **kwargs):
        res = super(WSVControllerBits, self).get_combination_info_website(
            product_template_id=product_template_id, product_id=product_id, combination=combination, add_qty=add_qty,
            parent_combination=parent_combination, **kwargs)
        product = request.env['product.product'].sudo().search([('id', '=', res.get('product_id'))])
        product_tempate = request.env['product.template'].sudo().search([('id', '=', product_template_id)])
        res.update({'product_sku': product.default_code or 'N/A' if product_tempate.product_variant_count > 1 else product_tempate.default_code or 'N/A'})
          
        return res
