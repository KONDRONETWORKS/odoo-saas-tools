# -*- coding: utf-8 -*-
{
    'name': "YLHC Theme Base",

    'summary': """
        Base for themes, it support free login for odoo
    """,

    'description': """
        Odoo Login, 
        Odoo login page, 
        Odoo login theme
        Login, 
        ylhc Theme Base,
        ylhc Theme,
        Ylhc Theme,
        Multi tab theme,
        Pop form theme
    """,

    'author': "Cheick Oumar Tidiane Traore",

    'website': "https://www.ylhctec.com",
    'live_test_url': 'https://www.ylhctec.com',

    'license': 'OPL-1',
    'images': ['static/description/screen_shot.png', 'static/description/banner.png'],
    'icon': 'static/description/icon.png',
    'maintainer': 'ylhctec',
    'category': 'Themes/Backend',
    'version': '18.0.1.0.0',

    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',

    'depends': ['base', 'web'],
    
    'data': [],

    'assets': {
        'web.assets_backend': [
            'theme_ylhc_base/static/css/ylhc_scroll.scss',
            'theme_ylhc_base/static/css/ylhc_misc.scss',
        ]
    }
}
