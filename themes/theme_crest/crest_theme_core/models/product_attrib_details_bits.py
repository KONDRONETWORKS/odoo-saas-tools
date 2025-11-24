from odoo import fields, models, _
from odoo.tools.translate import html_translate

class ProductAttribDetailsBits(models.Model):
    _name = 'product.attrib.details.bits'
    _description = 'Product Attribute Details'

    sequence = fields.Integer(string="Sequence") 
    name = fields.Char('Name',translate=True, required=True) 
    attribute_details = fields.Html(translate=html_translate, sanitize_form=False, sanitize_attributes=False) 
