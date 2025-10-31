{
    'name': 'SaaS Client',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'depends': ['base', 'auth_oauth', 'saas_auth_oauth_ip', 'saas_auth_oauth_check_client_id', 'mail'],
    'data': ['views/saas_client.xml', 'views/res_config.xml', 'security/rules.xml', 'security/groups.xml', 'data/ir_cron.xml', 'data/auth_oauth_data.xml', 'data/ir_config_parameter.xml', 'data/ir_actions.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
