# -*- coding: utf-8 -*-
# Copyright 2021, 2022 Odooland - Milad Sadeghi
# License LGPL-3.0 or later (https://choosealicense.com/licenses/agpl-3.0/).
{
    'name': "Modern Backend Theme",
    'version': '18.0.1.0.0',
    'sequence': 1,
    'summary': """
        Odoo Land Modern Theme""",

    'description': """
        Modern theme is a Odoo backend theme for Community edition, with the latest template design methods and support full responsive.
    """,

    'author': "Cheick Oumar Tidiane Traore",
    'maintainer': ["milad-sadeghi"],
    'website': "http://www.odooland.com",
    'support': "odooland.dev@gmail.com",
    'category': "Themes/Backend",
    'depends': ['base', 'web', 'mail'],
    'Live_test_url':'demo.odooland.com',
    'assets': {
        'web._assets_primary_variables': [
            'theme_modern/static/src/scss/primary_variables_custom.scss',
        ],
        'web._assets_backend_helpers': [
            'theme_modern/static/src/webclient/mixins.scss',
        ],
        'web.assets_backend': [
            'theme_modern/static/src/css/main.css',
            'theme_modern/static/src/css/navbar.css',
            'theme_modern/static/src/css/header.css',
            'theme_modern/static/src/css/form.css',
            'theme_modern/static/src/css/list.css',
            'theme_modern/static/src/css/kanban.css',
            'theme_modern/static/src/css/calendar.css',
            'theme_modern/static/src/css/pivot.css',
            'theme_modern/static/src/css/graph.css',
            'theme_modern/static/src/css/activity.css',
            'theme_modern/static/src/css/mail.css',
            'theme_modern/static/src/css/card.css',
            'theme_modern/static/src/css/dashboard.css',
            'theme_modern/static/src/css/chatter.css',
            'theme_modern/static/src/css/other.css',
            'theme_modern/static/src/xml/mail.xml',
            'theme_modern/static/src/webclient/**/*.xml',
            'theme_modern/static/src/webclient/**/*.scss',
            'theme_modern/static/src/webclient/**/*.js',
        ],
        'point_of_sale.assets': [
            'theme_modern/static/src/css/pos.css',
        ]
        
    },
    'images': [
        'static/description/icon.png',
        'static/description/theme_screenshot.png',
    ],
    'icon': 'static/description/icon.png',
    'price': 0.0,
    'currency': 'USD',
    'application': False,
    'auto_install': False,
    'installable': True,
    'license': 'LGPL-3',
}
