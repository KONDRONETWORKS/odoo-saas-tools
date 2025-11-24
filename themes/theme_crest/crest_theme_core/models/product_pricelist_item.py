from odoo import models,fields

class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    offer_name = fields.Char('Name' , translate=True, default='Best Value Offer')

     