from odoo import models, fields

class MenuLabel(models.Model):
    _name = "menu.label"
    _description = "Menu Label"

    name = fields.Char(string="Label Name", required=True)
    background_color = fields.Char(string="Background Color", help="Background color in hex, e.g., #FFFFFF")
    color = fields.Char(string="Text Color", help="Text color in hex, e.g., #000000")
    menu_ids = fields.One2many('website.menu', 'menu_label_id', string="Menus")
    label_style = fields.Selection([('lable_style_1', 'Label Style 1'), ('lable_style_2', 'Label Style 2'), ('lable_style_3', 'Label Style 3')],default='lable_style_1')  
    label_position = fields.Selection([('label_top', 'Label Top'), ('label_bottom', 'Label Bottom')],default='label_top')
    
class WebsiteMenu(models.Model):
    _inherit = "website.menu"

    menu_label_id = fields.Many2one('menu.label', string="Menu Label")
