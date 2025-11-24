from odoo import fields, models, _

class ProductLabelBits(models.Model):
    _name = 'product.label.bits'
    _description = 'Products label'

    name = fields.Char('Lable Name')
    bg_color = fields.Char('Background Color')
    text_color = fields.Char('Text Color') 
    lable_style = fields.Selection([('style_1','Style 1'),('style_2','Style 2'),('style_3','Style 3')],string='Label Style',default='style_1')

    website_id = fields.Many2one('website','Website')
    Product_tmpl_id = fields.Many2one('product.template','Product')