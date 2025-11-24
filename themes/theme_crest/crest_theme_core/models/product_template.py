from odoo import fields, models, api, _
from odoo.osv import expression

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_label_ids = fields.One2many('product.label.bits','Product_tmpl_id','Product Lables')
    hover_image_bits = fields.Binary('Product Hover Image')
    free_qty = fields.Float('Available Qty', compute='_compute_quantities', search='_search_available_qty', compute_sudo=True, digits='Avaialble')
    product_offers_ids = fields.Many2many('product.offers.bits',string='Product Offers',help="To configure and show offers for product")
    product_faq_id = fields.Many2one('product.faq.bits',string='Product FAQ')
    brand_id = fields.Many2one('product.brands',"Product Brand")
    terms_conditions_id = fields.Many2one('product.terms.conditions','Product Extra T&C',help="To configure extra terms and conditions for product.")

    def check_inventory_config(self):
        show_stock_lable = False
        website = self.env['website'].get_current_website() 
        if not self.sudo().allow_out_of_stock_order and self.sudo().with_context(warehouse=website._get_warehouse_available()).free_qty < 1:
            show_stock_lable =  True
        return show_stock_lable
         

    @api.depends('product_variant_ids.outgoing_qty','product_variant_ids.free_qty','product_variant_ids.virtual_available','product_variant_ids.incoming_qty',)
    def _compute_quantities(self):
        super(ProductTemplate, self)._compute_quantities()
        res = self._compute_qty_dict_bits()
        for product in self:
            product.free_qty = res[product.id]['free_qty']

    @api.model
    def _search_get_detail(self, website, order, options):
        res = super(ProductTemplate, self)._search_get_detail(website, order, options)
        attribs_vals = options.get('attribs_list', [])
        new_domain = []
        if len(attribs_vals): 
            new_domain.append(('brand_id', 'in', attribs_vals))  
        res['base_domain'].append(new_domain)
        return res 
        
    def _compute_qty_dict_bits(self):
        website = self.env['website'].get_current_website()
        # prepare variants qty
        available_variants = {pv['id']: pv for pv in self.sudo().with_context(warehouse=website._get_warehouse_available()).product_variant_ids.read(['free_qty']) }
        prod_available = {}
        for product in self:
            free_qty = 0
            for pv in product.product_variant_ids:
                free_qty += available_variants[pv.id]['free_qty']
            prod_available[product.id] = { 'free_qty': free_qty, }
        return prod_available

    def _search_available_qty(self, operator, value):
        domain = [('free_qty', operator, value)]
        product_variants_data = self.env['product.product'].sudo()._search(domain)
        return [('product_variant_ids', 'in', product_variants_data)]

    @api.model
    def _search_build_domain(self, domain_list, search, fields, extra=None):
        res = super(ProductTemplate, self)._search_build_domain(domain_list, search, fields, extra)
        domain = [res]
        context = self.env.context 

        if context.get('rating') and len(context.get('rating')):
            domain.append([('rating_avg', '>=', max([int(rat) for rat in context['rating']]))])
        res = expression.AND(domain)
        return res

    @api.model
    def _get_accessory_product_filter(self):
        return self.env.ref('website_sale.dynamic_filter_cross_selling_accessories').id
 

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    attribute_details_id = fields.Many2one('product.attrib.details.bits','Attribute Details') 
    show_on_ecomm_card = fields.Boolean('Show on Ecommerce Card', help="To show this attribute on product card in website shop")

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    products_count = fields.Integer("Product Count", compute="_compute_product_count") 

    def _compute_product_count(self):
        for attr in self:
            product_domain = [('attribute_line_ids.value_ids', '=', attr.id)] 
            if not attr.env.user.has_group('base.group_system'):
                product_domain.append(("website_published", '=', True))
            ctx = self.env.context or {}
            if 'attrib_search' in ctx and ctx['attrib_search']:
                product_domain.append(("name", 'ilike', ctx['attrib_search'].strip())) 
            attr.products_count = self.env['product.template'].sudo().search_count(product_domain)


