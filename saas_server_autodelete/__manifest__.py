{
    'name': 'SaaS Server - Autodelete expired databases',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'depends': ['saas_server'],
    'data': ['data/ir_cron.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
