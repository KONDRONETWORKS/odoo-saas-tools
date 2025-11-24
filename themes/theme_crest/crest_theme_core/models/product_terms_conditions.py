# -*- coding: utf-8 -*-

from odoo import fields, models, _

class ProductTermsCondiotions(models.Model):
    _name = "product.terms.conditions"
    _description = "Product terms ans conditions"

    name = fields.Char(string="name")
    product_terms_lines = fields.One2many('product.terms.lines','product_term_id',string='Terms Lines')
     

class ProductTermsLines(models.Model):
    _name = "product.terms.lines"
    _description = "Product terms ans conditions lines"

    name = fields.Char(string="name")
    indication_type = fields.Selection([('icon','Icon'),('image','Image')],string="Indication Type")
    indication_img = fields.Binary('Indication Image')
    indication_icon = fields.Char('Indication Icon')
    product_term_id = fields.Many2one('product.terms.conditions','Product Terms Ans Condition')
