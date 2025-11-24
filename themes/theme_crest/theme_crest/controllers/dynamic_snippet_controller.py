# -*- coding: utf-8 -*-
from odoo import http, fields, _
import json
 
from odoo.http import request
from odoo.addons.website_sale.controllers import main
from odoo.addons.website.controllers.main import QueryURL
import logging 

_logger = logging.getLogger(__name__)

class DSController(http.Controller): 
    @http.route(['/website/snippet/get'], type='json', auth="public", website=True)
    def get_website_snippet(self, model='',template_key='',visual=None,data={},**kwargs):
        vals = {}
        if not template_key or not model:
            dummay_view = request.env['ir.ui.view'].sudo()._render_template('theme_crest.no_data_template_bits',{})
            return {'template_block':dummay_view}
        if not visual.get('borderstyle'):
            visual['borderstyle'] = 'rounded'
            
        try:
            order = data.get('order') or 'name asc'
            limit = data.get('limit') or len(data.get('records'))
            domain = self.prepare_record_domain(data,model)
            records = request.env[model].sudo().search(domain,limit=limit,order=order)
            
            col_temp = int(visual.get('limit', 3))
            responsiveclass = 's-res-w-1 py-2'
            if col_temp == 1:
                responsiveclass = 's-res-w-1 py-2'
            elif col_temp == 2:
                responsiveclass = 's-res-w-2 s-res-w-sm-2 py-2'
            elif col_temp == 3:
                responsiveclass = 's-res-w-3 s-res-w-lg-3 s-res-w-sm-3 py-2'
            elif col_temp == 4:
                responsiveclass = 's-res-w-4 s-res-w-xl-4 s-res-w-lg-4 s-res-w-sm-4 py-2'
            elif col_temp == 5:
                responsiveclass = 's-res-w-5 s-res-w-xl-5 s-res-w-lg-5 s-res-w-sm-5 py-2'
            elif col_temp == 6:
                responsiveclass = 's-res-w-6 s-res-w-xxl-6 s-res-w-xl-6  s-res-w-lg-6 s-res-w-sm-6 py-2'
            elif col_temp == 7:
                responsiveclass = 's-res-w-7 s-res-w-xxl-6 s-res-w-xl-6  s-res-w-lg-6 s-res-w-sm-6 py-2'
            elif col_temp == 8:
                responsiveclass = 's-res-w-8 s-res-w-xxl-6 s-res-w-xl-6  s-res-w-lg-6 s-res-w-sm-6 py-2'
                
            vals = {
                'records':records,
                'template_key':template_key or 'dy_prod_tmp_style_1_bits',
                'visual':visual,
                'responsiveclass' :responsiveclass,
                'keep' : QueryURL('/shop')
            }
            view = request.env['ir.ui.view'].sudo()._render_template('theme_crest.dynamic_template_bits',vals)
            vals.update({'view':view})
        except Exception as e:
            _logger.warning("Something went wrong.")
        
        return vals

    def prepare_record_domain(self,data,model):
        domain = [('is_published', '=', True)] 
        if model == 'product.public.category':
            domain = []
        record_ids = data.get('records')
        if record_ids and len(record_ids): 
            domain.append(('id','in',record_ids))
        return domain
