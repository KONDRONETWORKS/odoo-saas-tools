{
    'name': 'SaaS Portal',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'depends': ['base', 'saas_oauth_provider', 'website', 'auth_signup', 'saas_base'],
    'data': ['data/mail_template_data.xml', 'data/plan_sequence.xml', 'data/cron.xml', 'wizard/config_wizard_minimal.xml', 'wizard/batch_delete.xml', 'views/saas_portal.xml', 'data/ir_config_parameter.xml', 'data/subtype.xml', 'data/support_team.xml', 'views/res_users.xml', 'data/res_users.xml', 'security/ir.model.access.csv'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
