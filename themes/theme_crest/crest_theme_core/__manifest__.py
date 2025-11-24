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
    'name': 'Crest theme core',
    'description': 'Design. Innovate. Sell. All with Crest Theme. The ultimate Odoo theme, offering cutting-edge features for building business and e-commerce websites effortlessly.',
    'category': 'Base',
    'summary': 'Design. Innovate. Sell. All with Crest Theme. The ultimate Odoo theme, offering cutting-edge features for building business and e-commerce websites effortlessly.',
    'version': '18.0.1.0.1',
    'license': 'OPL-1',
    'depends': [
            'website','website_blog',
            'website_sale',
            'website_sale_wishlist',
            'website_sale_comparison',
            'website_sale_stock_wishlist',
            'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/website_terabits_config.xml',
        'views/theme_configuration_view.xml',
        'views/product_label_bits_view.xml',
        'views/product_public_category_view.xml',
        'views/product_template_view.xml',
        'views/product_template_view.xml', 
        'views/product_offers_bits_view.xml',
        'views/product_attrib_details_bits_view.xml',
        'views/product_attributes_view.xml',
        'views/product_brands_view.xml',
        'views/product_terms_conditions_view.xml',
        'template/brand_template.xml',
        'template/mega_menu.xml',
        'views/website_menu_view.xml',
        'views/product_inquiry_view.xml',
        'views/product_pricelist_item.xml'
    ],
    'assets': { 
        'web.assets_frontend': [
            "crest_theme_core/static/src/scss/brands_template.scss",
            "crest_theme_core/static/src/scss/mega_menu.scss",
        ],
        'web.assets_backend': [  
            'crest_theme_core/static/src/js/attendence_menu/*',
        ],  
        'website.assets_editor': [
            'crest_theme_core/static/src/theme_config/*',
            'crest_theme_core/static/src/js/website_custom_menu.js', 
        ],
        'website.assets_wysiwyg': [],
    },
    # Author
    'author': 'Terabits Technolab',
    'website': 'https://www.terabits.xyz/apps/17.0/crest_theme_core',
    'maintainer': 'Terabits Technolab', 
    'images': [
        'static/description/banner-sub.gif',
    ],
    'icon': 'static/description/icon.png',
    # Technical
    'installable': True,
    'auto_install': False,
    "price": "00.0",
    'currency': 'USD',
}
