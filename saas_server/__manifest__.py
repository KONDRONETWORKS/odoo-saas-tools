{
    'name': 'SaaS Server',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'depends': ['base', 'auth_oauth', 'saas_auth_oauth_ip', 'saas_base', 'website'],
    'data': ['views/saas_server.xml', 'views/res_config_settings_views.xml', 'data/auth_oauth_data.xml', 'data/ir_config_parameter.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
