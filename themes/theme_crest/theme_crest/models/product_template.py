# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round
from odoo.addons.website.models import ir_http


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    bits_sales_count = fields.Float(string="Sold", compute='_compute_bits_sales_count', digits='Product sale count', store=True)
 
    @api.depends('product_variant_ids.sales_count')
    def _compute_bits_sales_count(self):
        for product in self:
            product.bits_sales_count = float_round(sum([p.sales_count for p in product.with_context(active_test=False).product_variant_ids]), precision_rounding=product.uom_id.rounding)

    # prepare product attr values for color variants

    def prepare_variant_data(self,value_id):
        pa_vals = {}
        product_variant_obj = self.product_variant_ids.product_template_variant_value_ids and self.product_variant_ids.filtered(
            lambda p: int(value_id) in p.product_template_variant_value_ids.product_attribute_value_id.ids)[0]
        product_attr_values = self.attribute_line_ids.filtered(lambda a:a.attribute_id.display_type == 'color')
        # for pav in product.
        if product_variant_obj:
            pa_vals['product_image'] = '/web/image/product.product/'+ str(product_variant_obj.id) + '/image_1920'
            pa_vals['product_id'] = product_variant_obj.id
        return pa_vals

    

    