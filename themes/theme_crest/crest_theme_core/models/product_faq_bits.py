from odoo import models, fields, _

class ProductFaqBits(models.Model):
    _name = 'product.faq.bits'
    _description = 'Product FAQ'

    name = fields.Char('Name')
    product_faq_line_ids = fields.One2many('product.faq.lines.bits','product_faq_id')
    product_id = fields.One2many('product.template','product_faq_id')

class ProductFaqLinesBits(models.Model):
    _name = 'product.faq.lines.bits'
    _description = 'Product FAQs Lines'

    name = fields.Char('Question')
    answer = fields.Char('Answer') 
    product_faq_id = fields.Many2one('product.faq.bits','FAQ')

