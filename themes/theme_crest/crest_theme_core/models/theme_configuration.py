from odoo import fields, models, _

class ThemeConfiguration(models.Model):
    _name = 'theme.configuration'
    _description = 'Theme Configuration'
    _rec_name = 'website_id'

    website_id = fields.Many2one('website','Website')
    # general/header settings
    h_lang_select = fields.Boolean('Show language Selector in Header')
    h_pricelist_select = fields.Boolean('Show Pricelist Selector in Header')
    h_offer_line = fields.Boolean("Show Offer Line in Header",default=True)
    pricelist_offer_timer = fields.Boolean("Show Offer Timer")
    h_cart_popup = fields.Boolean("Show Cart Popup", default=True)
    b2b_mode = fields.Boolean('Enable B2B Mode')
    h_category_menu = fields.Boolean("Show categories menu",default=True)
    navbar_hover_effect = fields.Selection([('navbar_hover_effect_1','NavBar Hover Effect 1'),('navbar_hover_effect_2','NavBar Hover Effect 2'),('navbar_hover_effect_3','NavBar Hover Effect 3')],"Card Product Style", default='navbar_hover_effect_1')
    #------- shop settings
    card_product_style = fields.Selection([('card_product_style_1','Card Product Style 1'),('card_product_style_2','Card Product Style 2'),('card_product_style_3','Card Product Style 3'),('card_product_style_4','Card Product Style 4')],"Card Product Style", default='card_product_style_1')
    card_border_style = fields.Selection([('square','Square'),('rounded','rounded')],"Border Style", default='square')

    image_on_hover_style = fields.Selection(
        string='Product Image On Hover Style',
        selection=[('hover_style_1', 'Hover Style 1'), ('hover_style_2', 'hover_style_2'),('hover_style_3', 'Hover Style 3')],
        default='hover_style_1'
    )
    card_cart_btn = fields.Boolean("Show cart button",default=True)
    card_compare_btn = fields.Boolean("Show compare button",default=False)
    card_quickview_btn = fields.Boolean("Show quickview button", default=True)
    card_wishlist_btn = fields.Boolean("Show wishlist button", default=True)
    card_rattings = fields.Boolean("Show rattings button", default=False)
    card_stock_lbl = fields.Boolean("Show stock button", default=False)
    card_product_lbl = fields.Boolean("Show product label", default=False)
    card_product_terms_and_condition = fields.Boolean("Show product label", default=False)
    card_hover_image = fields.Boolean("Show Hover Image", default=False)
    enable_lazyload_image = fields.Boolean("Enable lazy load image", default=True)
    # card_show_similar = fields.Boolean("Show similar Products button", default=False) 

    filters_design = fields.Selection([('style-1','Style 1'),('style-2','Style 2'),('style-3','Style 3'),('style-4','Style 4')],string='Filters Design',default='style-1')
    filter_in_sidebar = fields.Boolean('Enable Sidebar Filter')
    filter_product_count = fields.Boolean('Enable Product Count')
    show_category_in_filter = fields.Boolean('Show Categories In Filter')
    show_ratings_filter = fields.Boolean('Show Ratings Filter',default=True)
    show_stock_avail_filter = fields.Boolean('Show Stock Availability Filter',default=True)

    shop_category_style = fields.Selection([('style-1','Style 1'),('style-2','Style 2'),('style-3','Style 3'),('style-4','Style 4')],string='Filters Design',default='style-1')
    shop_category_banner = fields.Boolean('Enable Catgory banner')

    enable_loadmore_products = fields.Boolean('Enable Load More Products',default=True)
    #-------Product page settings
    product_zoom = fields.Boolean('Enable Product Zoom')
    product_offers = fields.Boolean('Enable Product Offers')
    product_brand_detail = fields.Boolean('Enable Product Brand Detail')
    product_sku = fields.Boolean('Show Product SKU')
    product_tags = fields.Boolean('Show Product Tags')
    product_sharing = fields.Boolean('Enable Sharing')
    product_inquiry = fields.Boolean('Enable Product Inquiry')
    product_conditions = fields.Boolean('Show Product Conditions')
    # product_enable_tabs = fields.Boolean('Enable Product Details Tab')
    product_review_tab = fields.Boolean('Show Product Review')
    product_sticky_view = fields.Boolean('Show Sticky Product view')
    product_faq = fields.Boolean('Show Product FAQ')
    show_alternative_products = fields.Boolean('Show alternative products')
    show_accessory_products = fields.Boolean('Show accessories products')
    # sticky product purhcase/buy popup
    show_sticky_product_buy_notify = fields.Boolean('Show Sticky Product Buy Notification')
    select_when_notify_show = fields.Selection([('on_add_to_cart','On Add To Cart'),('on_purchase','On Purchase')],string='When to show notification',default='on_add_to_cart')    

    def get_theme_config(self,website_id):
        website_config = self.sudo().search([('website_id','=',website_id)])
        config = {}
        if not len(website_config):
            website_config = self.sudo().create({'website_id':website_id})
        
        config = website_config.sudo().search_read()
        crm_module = self.env.ref('base.module_crm')
        if crm_module.state == 'installed':
            config[0]['crm_installed'] = True
        else:
            config[0]['crm_installed'] = False
        return config

    def save_theme_configuration(self, website_id, config):
        website_config = self.sudo().search([('website_id','=',website_id)])
        website_config.sudo().write(config)
        self.env.registry.clear_cache()
        return True

    def install_crm_module(self):
        crm_module = self.env.ref('base.module_crm')
        crm_module.sudo().button_immediate_install() 
        if crm_module.state == 'installed':
            return True
        else:
            return False
