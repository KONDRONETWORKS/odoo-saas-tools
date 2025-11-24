# -*- coding: utf-8 -*-
#################################################################################
# Author      : Terabits Technolab (<www.terabits.xyz>)
# Copyright(c): 2024-25
# All Rights Reserved.
#
# This module is copyright property of the author mentioned above.
# You can't redistribute/reshare/recreate it for any purpose.
#
#################################################################################
{ 
    'name': 'Theme Crest', 
    'description': """ 
        Crest Theme is a versatile and feature-rich Odoo website theme designed to fulfill all types of websites requirments, 
        from dynamic business portfolios to fully functional e-commerce platforms. 
        Packed with modern features and intuitive tools, Crest Theme empowers users to create stunning, 
        professional websites with ease and efficiency.
    """,
    'summary': """ 
        Design. Innovate. Sell. All with Crest Theme. The ultimate Odoo theme, offering cutting-edge features for building business and e-commerce websites effortlessly.
    """,
    'version': '18.0.1.0.2',
    'license': 'OPL-1',
    'category': 'Theme/Creative',
    'depends': [
        'web','web_editor','crest_theme_core','website_sale','odoo_gpt_chat','saas_dynamic_features'
    ],
    'data': [
        "templates/snippets/dynamic_snippets.xml",
        "templates/snippets/snippets.xml",
        "templates/website_layout/headers.xml",
        "templates/website_layout/footers.xml",
        "templates/shop/product_price.xml",
        "templates/shop/shop_product_style.xml",
        "templates/shop/shop.xml",
        "templates/shop/shop_cart.xml",
        "templates/shop/product_page.xml",
        "templates/shop/product_attributes.xml",
        "templates/shop/quick_view.xml", 
        "templates/shop/shop_wishlist.xml",
        "templates/snippets/theme_customise_option.xml",
        'templates/product/product.xml',
        'templates/image_hotspot_popup.xml',
        'templates/contact_us/contact_us.xml', 
        'templates/sign_up/sign_up.xml',
        'templates/shop/our_collections.xml',
        'templates/website_menu.xml',
        'templates/shop/b2b.xml',
        'templates/shop/product_buy_notify.xml',
        'templates/assets.xml',
        'views/immersive_snippet.xml',
    ],
    # Assets
    'assets': {
        'web._assets_primary_variables':[
            "/theme_crest/static/src/scss/theme_general/theme_variable.scss",
            "/theme_crest/static/src/scss/theme_general/font_icon_mixin.scss",
        ],
        'web.assets_frontend': [
            'theme_crest/static/src/js/pwa_webapp.js',
            'theme_crest/static/fonts/Albert_Sans/stylesheet.css', 
            'theme_crest/static/src/xml/*',
            'theme_crest/static/src/website_sale/website_sale.js',
            'theme_crest/static/src/website_sale/shop_widgets.js',
            'theme_crest/static/src/website_sale/quick_view.js',
            'theme_crest/static/src/website_sale/min_cart.js',
            'theme_crest/static/src/website_sale/product_widgets.js',
            'theme_crest/static/src/website_sale/shop_load_more.js',
            'theme_crest/static/src/website_sale/theme_script.js',
            'theme_crest/static/src/js/quick_view_hotspot.js',
            'theme_crest/static/src/scss/website_layout/footer.scss',
            'theme_crest/static/src/scss/website_layout/header.scss',
            'theme_crest/static/src/scss/shop_layout/our_collections.scss',
            'theme_crest/static/src/scss/shop_layout/general.scss',
            'theme_crest/static/src/scss/shop_layout/dialog.scss',
            'theme_crest/static/src/scss/shop_layout/product.scss',
            'theme_crest/static/src/scss/shop_layout/shop.scss', 
            'theme_crest/static/src/scss/shop_layout/shop_cart.scss',
            'theme_crest/static/src/scss/shop_layout/shop_checkout.scss',
            'theme_crest/static/src/scss/shop_layout/shop_wishlist.scss', 
            'theme_crest/static/src/website_sale/dynamic_snippet.js',
            'theme_crest/static/src/js/static_template/gallery_filter.js',
            'theme_crest/static/src/js/static_template/config_carousel.js',
            'theme_crest/static/src/scss/static_template/static_template_style.scss',
            'theme_crest/static/src/lib/OwlCarousel-2.3.4/assets/owl.carousel.min.css',
            'theme_crest/static/src/lib/OwlCarousel-2.3.4/assets/owl.theme.default.css',
            'theme_crest/static/src/scss/dynamic_snippets/dynamic_snippets_template.scss',
            'theme_crest/static/src/lib/OwlCarousel-2.3.4/owl.carousel.js',
            'theme_crest/static/src/js/static_template/static_tem_carousel.js', 
            'theme_crest/static/src/lib/count-up-smooth-animation/counterup.js',
            'theme_crest/static/src/js/static_template/static_offer_couner.js',
            'theme_crest/static/src/scss/image_hotspot_design.scss',
            'theme_crest/static/src/scss/sign_up/sign_up.scss', 
            'theme_crest/static/src/js/header_category.js',
            'theme_crest/static/src/js/search_filter.js', 
            'theme_crest/static/src/js/product_attribute.js',
        ],
        'web.assets_backend': [
        ],
        'website.assets_wysiwyg': [   
            'theme_crest/static/src/lib/OwlCarousel-2.3.4/assets/owl.carousel.min.css',
            'theme_crest/static/src/lib/OwlCarousel-2.3.4/assets/owl.theme.default.css',
            'theme_crest/static/src/scss/dynamic_snippets/dynamic_snippets_template.scss',
            'theme_crest/static/src/lib/OwlCarousel-2.3.4/owl.carousel.js', 
            'theme_crest/static/src/js/static_template/config_carousel.js',
            'theme_crest/static/src/js/jquery-ui.min.js',
            'theme_crest/static/src/js/snippet.option.js',
            'theme_crest/static/src/js/snippet_hotspot_option.js',
            'theme_crest/static/src/snippet_editor/**/*', 
            'theme_crest/static/src/xml/default_row_template.xml',
            'theme_crest/static/src/xml/static_template.xml',
            'theme_crest/static/src/scss/static_template/static_template_style.scss', 
        ],
    },
    # Author
    'author': 'Cheick Oumar Tidiane Traore',
    'website': 'https://www.terabits.xyz/apps/18.0/theme_crest',
    'maintainer': 'Terabits Technolab', 
    'images': [
        'static/description/logo.gif',
        'static/description/theme_screenshot.gif',
        
    ],
    'icon': 'static/description/icon.png',
    # Technical
    'installable': True,
    'auto_install': False,
    'application': True,
    "price": "00.0",
    'currency': 'USD',
    'live_test_url': 'https://www.terabits.xyz/request_demo?source=index&version=18&app=theme_crest',
}
