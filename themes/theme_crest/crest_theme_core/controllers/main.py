from odoo import _, http
import logging
import base64
import io
import json
import re
import string
from collections import defaultdict
import datetime
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)

try:
    from werkzeug.utils import send_file
except ImportError:
    from odoo.tools._vendor.send_file import send_file

from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo.http import request
from odoo.osv import expression
from odoo.tools import html_escape, file_path, file_open
from odoo.tools.mimetypes import guess_mimetype
from odoo.addons.website_sale.controllers import main
from odoo.tools import lazy

default_theme_config_vals = {
        'h_lang_select':True, 'h_pricelist_select':True, 'h_offer_line':True, 'b2b_mode':False,'pricelist_offer_timer':False,'h_category_menu' : False,
        'card_cart_btn':True, 'card_compare_btn':False, 'card_quickview_btn':False, 'card_wishlist_btn':False,
        'card_border_style':'square', 'card_rattings':False, 'card_stock_lbl':False,'card_product_lbl':True,
        'filters_design':'style-1', 'filter_in_sidebar':False, 'filter_product_count':True, 'shop_category_style':'style-1','h_cart_popup' : True,'card_product_terms_and_condition' : True,
        'shop_category_banner':True, 'card_hover_image':False,'enable_loadmore_products':True,'show_category_in_filter':True,
        'show_ratings_filter':True,'show_stock_avail_filter':True,'enable_lazyload_image':True,
        'product_zoom':True, 'product_inquiry':False, 'product_offers':False,'product_tags':True,'product_faq':True,'product_sku':True,'product_sharing':True,'product_conditions':True,
        'product_brand_detail':True,'product_review_tab':False,'product_sticky_view':True,'navbar_hover_effect':'navbar_hover_effect_1',
        'card_product_style':'card_product_style_1','image_on_hover_style':'hover_style_1',
    }
shop_theme_config_fields = ['h_lang_select','h_pricelist_select','h_offer_line','b2b_mode','card_cart_btn','card_compare_btn','card_product_lbl','pricelist_offer_timer','card_product_style','image_on_hover_style',
        'card_quickview_btn','card_wishlist_btn','card_border_style','card_rattings','card_stock_lbl','filters_design','h_category_menu','h_cart_popup','card_product_terms_and_condition',
        'filter_in_sidebar','filter_product_count','shop_category_style','card_hover_image','enable_loadmore_products','navbar_hover_effect',
        'show_category_in_filter','show_ratings_filter','show_stock_avail_filter','enable_lazyload_image']

class WebsiteSaleBits(WebsiteSale): 
    @http.route()
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post): 
        website = request.website
        env_context = dict(request.env.context)
        # product brands  
        filters_dict = self.prepare_filters_dict(post)
        # product_brands = request.env['product.brands'].sudo().search([('active','=',True),('website_ids','in',website.ids)])
        request_args = request.httprequest.args
        attribs_list = request_args.getlist('attribs')
        attribs_values = [int(v) for v in attribs_list]
        if attribs_values:
            post['attribs'] = attribs_values
        # ----theme configs 
        theme_config = request.env['theme.configuration'].sudo().search([('website_id','=',website.id)],limit=1)  
        if len(theme_config):
            env_context.update({'theme_config':theme_config.search_read()[0]})
        else: 
            env_context.update({'theme_config':default_theme_config_vals})
        
        # ----ratting filters and add in context for domain
        rating_params = request.httprequest.args.getlist('rt')
        in_stock = request.httprequest.args.get('in_stock')
        
        env_context.update({
            'rating':rating_params,
            'in_stock':in_stock,
        })
        request.env.context = env_context
        # ----calling super
        res = super().shop(page=page, category=category, search=search, min_price=min_price, max_price=max_price, ppg=ppg, **post)
        
        ProductBrands = request.env['product.brands']
        search_products = res.qcontext.get('search_product')
        product_brands = lazy(lambda: ProductBrands.search([
                ('product_ids', 'in', search_products.ids)]))
        # For Rating
        search_products = res.qcontext['search_product']
        rating_ln = 1
        if len(search_products.sudo().mapped("rating_avg")):
            rating_ln = int(max(search_products.sudo().mapped("rating_avg"))) + 1
        applied_ratings = [int(rating) for rating in rating_params]
 
        res.qcontext.update({
            'ratings_avg': rating_ln,
            'applied_ratings':applied_ratings,
            'in_stock_applied':True if in_stock else False,
            'brands':product_brands,
            'attribs_set':attribs_values,
            'filters_dict':filters_dict,
        })
        return res

    def _get_search_options(self, category=None, attrib_values=None, tags=None, min_price=0.0, max_price=0.0,conversion_rate=1, **post):
        res = super()._get_search_options(category, attrib_values, tags, min_price, max_price, conversion_rate, **post)
        attribs_list = post.get('attribs', [])
        res['attribs_list'] = attribs_list
        return res 
    def check_in_stock(self, product):
        combination = product.sudo()._get_first_possible_combination()
        combination_info = product.sudo()._get_combination_info(combination, add_qty=1)
        product_obj = request.env['product.product'].sudo().browse([combination_info['product_id']])
        website = request.env['website'].get_current_website()
        if not product_obj.sudo().allow_out_of_stock_order and product_obj.sudo().with_context(warehouse=website._get_warehouse_available()).free_qty <= 0:
            return False
        else:
            return product.id

    def _shop_lookup_products(self, attrib_set, options, post, search, website): 
        product_count, details, fuzzy_search_term = website._search_with_fuzzy("products_only", search, limit=None, order=self._get_search_order(post), options=options)
        search_result = details[0].get('results', request.env['product.template']).with_context(bin_size=True)
        in_stock = post.get("in_stock", False)
        if in_stock:
            search_result = request.env["product.template"].sudo().browse(list([prod_id for prod_id in map(self.check_in_stock, search_result) if prod_id != False]))
        
        return fuzzy_search_term, product_count, search_result

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs): 
        return request.render("theme_crest.product_replace_bits", self._prepare_product_values(product, category, search, **kwargs))
    
    def _prepare_product_values(self, product, category, search, **kwargs):
        values = super()._prepare_product_values(product, category, search, **kwargs)
        website = request.website
        theme_config = request.env['theme.configuration'].sudo().search([('website_id','=',website.id)],limit=1)
        # fields = ['']
        if len(theme_config):
            values['theme_config'] = theme_config.search_read()[0]
        else:
            values['theme_config'] = {
                'product_offers':False, 'product_tags':True, 'product_faq':True, 'product_sku':True, 'product_sharing':True, 'product_conditions':True,
                'product_brand_detail':True, 'product_review_tab':False, 'product_sticky_view':True, 'enable_lazyload_image':True, 'card_rattings':False,
                'card_product_lbl':True
            }
        return values
    
    def prepare_filters_dict(self,post):
        vals = {}   
        # brands
        attribs_list = request.httprequest.args.getlist('attribs')
        # attributes
        attrib_list = request.httprequest.args.getlist('attrib')
        # tags
        tags_list = request.httprequest.args.getlist('tags') 
        try:
            if len(attribs_list):
                brand_list = []
                for b_id in attribs_list: 
                    brand = request.env['product.brands'].sudo().search([('id','in',[int(b_id)])])
                    brand_list.append([brand.id,brand.name]) 
                vals.update({'Brands': brand_list}) 

            if len(attrib_list):
                attributes = {}
                for a_id in attrib_list:
                    if a_id:
                        a_and_v = a_id.split('-')
                        attribute = request.env['product.attribute'].sudo().search([('id','in',[int(a_and_v[0])])])
                        attribute_value = request.env['product.attribute.value'].sudo().search([('id','in',[int(a_and_v[1])])])
                        if len(attribute):
                            if attribute.name not in attributes.keys():
                                attributes.update({attribute.name:[[attribute.id,attribute_value.id,attribute_value.name]]})
                            else:
                                attributes[attribute.name].append([attribute.id,attribute_value.id,attribute_value.name])
                vals.update({'Attributes': attributes})
            
            if len(tags_list):
                tags = []
                for t_id in tags_list:
                    tag = request.env['product.tag'].sudo().search([('id','in',[int(t_id)])])
                    tags.append([tag.id,tag.name])
                vals.update({'Tags': tags}) 
        except (ValidationError):
            _logger.exception('Invalid attribute value')

        return vals

    @http.route('/product-pop-details', type='http', auth='public', website=True)
    def get_popup_product_details(self, **kw):
        product_id = kw.get('product')
        
        if product_id:
            product = request.env['product.template'].sudo().browse(int(product_id))
            return request.render(
                "theme_crest.product_popup_bits", 
                {'product': product}, 
                headers={'Cache-Control': 'no-cache'}
            )
        
        return request.not_found()

