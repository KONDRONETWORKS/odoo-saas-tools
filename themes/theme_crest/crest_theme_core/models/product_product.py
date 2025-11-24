from odoo import fields, models, _

class ProductProduct(models.Model):
    _inherit = "product.product"


    def _get_offer_timing(self, pricelist):
        domain = [('date_end','!=',False)]
        # check for product offer applied
        ptmpl_offer = pricelist.item_ids.search([('id','in',pricelist.item_ids.mapped('id')),('product_tmpl_id','=',self.product_tmpl_id.id),('applied_on','=','1_product')] + domain, limit=1)
        # check for variant offer applied
        product_variant_offer = pricelist.item_ids.search([('id','in',pricelist.item_ids.mapped('id')),('applied_on','=','0_product_variant'), ('product_id','=',self.id)] + domain, limit=1)
        # check for category offer applied
        category_offer = pricelist.item_ids.search([('id','in',pricelist.item_ids.mapped('id')),('applied_on','=','2_product_category'),('categ_id','=',self.categ_id.id)] + domain, limit=1)
        # check for global offer applied
        global_offer = pricelist.item_ids.search([('id','in',pricelist.item_ids.mapped('id')),('applied_on','=','3_global')] + domain, limit=1) 
        
        if ptmpl_offer and (fields.Datetime.today() >= ptmpl_offer.date_start):
            return ptmpl_offer.date_end 
        elif product_variant_offer and (fields.Datetime.today() >= product_variant_offer.date_start):
            return product_variant_offer.date_end
        elif category_offer and (fields.Datetime.today() >= category_offer.date_start):
            return category_offer.date_end
        elif global_offer and (fields.Datetime.today() >= global_offer.date_start):
            return global_offer.date_end
        return False