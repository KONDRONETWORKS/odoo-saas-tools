from odoo import fields, models,_

class ProductInquiry(models.Model):
    _name = 'product.inquiry'
    _description = 'Product Inquiry'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', required=True)
    message = fields.Char(string='Message', required=True)
    product_id = fields.Many2one('product.template', string='Product')
    state = fields.Selection([
        ('new', 'New'), ('pending', 'Pending'), ('done', 'Done'), ('cancel', 'Cancel')], 
         string='State', default='new')
    website_id = fields.Many2one('website', string='Website')

    # user_id = fields.Many2one('res.users', string='User')

    