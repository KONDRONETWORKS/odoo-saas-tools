from odoo import fields, models, _

class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    category_banner = fields.Binary('Category Banner') 
    product_count = fields.Integer('Products Count',compute='_get_product_count')


    def _get_product_count(self):
        for categ in self:
            categ_ids = [categ.id]
            child_ids = [categ.id]
            # prepare all categ ids list
            while child_ids:
                child_ids = categ.env['product.public.category'].sudo().search([('parent_id', 'in', child_ids)]).ids
                categ_ids = categ_ids + child_ids
                
            product_domain = [('public_categ_ids', 'in', list(set(categ_ids)))]
            if not categ.env.user.has_group('base.group_system'):
                product_domain.append(("website_published", '=', True))
            context = categ.env.context or {}
            if 'product_categ_search' in context and context['product_categ_search']:
                product_domain.append(("name", 'ilike', context['product_categ_search'].strip())) 
            categ.product_count = self.env['product.template'].sudo().search_count(product_domain)

