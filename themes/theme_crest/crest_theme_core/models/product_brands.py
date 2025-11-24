from odoo import fields, models, _

class ProductBrands(models.Model):
    _name = 'product.brands'
    _description = 'Product brand'

    name = fields.Char('Brand Name')
    active = fields.Boolean('Active',default=True)
    brand_image = fields.Binary('Brand Image')
    brand_description = fields.Char('Brand Description')
    product_ids = fields.One2many('product.template','brand_id',string="Product Ids")
    product_count = fields.Integer("Product Count",compute="_compute_product_count",store=True)
    website_ids = fields.Many2many('website',string="Website")

    def _compute_product_count(self):
        for rec in self:
            rec.product_count = len(rec.product_ids.ids)
