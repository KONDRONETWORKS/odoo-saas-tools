{
    'name': 'Website Sale Require Login',
    'version': '18.0.1.0.0',
    'author': 'ITExperts4Africa',
    'license': 'LGPL-3',
    'category': 'Website',
    'summary': 'Require login to access website sale',
    'description': '''
        Website Sale Require Login
        ==========================
        
        This module requires users to be logged in before accessing the website sale pages.
        
        Features:
        - Redirects anonymous users to login page when accessing shop
        - Allows configuration via Settings > Website
    ''',
    'depends': ['website_sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 10,
}

