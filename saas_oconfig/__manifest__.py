# saas_oconfig - Configuration
{
    'name': 'SaaS Optimized Config',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Configuration et paramètres SaaS centralisés',
    'description': """
SaaS Optimized Config
=====================

Module de configuration centralisée pour le système SaaS.

**Fonctionnalités:**
- Paramètres système
- Templates configurables
- Versions Odoo
- Domaines et DNS
""",
    'depends': ['saas_ocore'],
    'data': [
        'security/ir.model.access.csv',
        'views/config_views.xml',
        'data/config_data.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 50,
}

