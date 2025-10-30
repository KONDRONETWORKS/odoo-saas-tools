{
    'name': 'SaaS Portal Subscription',
    'version': '18.0.1.0.0',
    'author': 'PlanetaTIC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'info@planetatic.com',
    'website': 'https://www.planetatic.com',
    'depends': ['saas_portal', 'base_automation'],
    'data': ['data/base_automation.xml', 'wizard/subscription_wizard.xml', 'views/saas_portal.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
