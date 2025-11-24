# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.tools.translate import html_translate

class ProductOffersBits(models.Model):
    _name = "product.offers.bits"
    _description = "Product Offers"

    name = fields.Char("name",translate=True, required=True)
    sequence = fields.Integer(string="Sequence") 
    offer_icon = fields.Char(default="tags") 
    offer_description = fields.Char(string="Description", translate=True)
    offer_details = fields.Html(translate=True)
    product_ids = fields.Many2many("product.template", string="Offer Products")