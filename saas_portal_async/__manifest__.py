{
    'name': 'SaaS Portal Asynchronous database creation',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Nicolas JEUDY',
    "support": "apps@itexperts4africa.com",
    'website': "https://www.itexperts4africa.com",
    'license': 'GPL-3',
    'category': 'SaaS',
    'depends': [
        'base',
        'saas_portal',
        'connector',
    ],
    'installable': False,
    'application': False,
    'data': [
        'views/wizard.xml',
    ],
}
