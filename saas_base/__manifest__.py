{
    'name': 'SaaS Base',
    'version': '18.0.1.0.1',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Module de base pour le système SaaS - Fonctionnalités communes',
    'description': """
SaaS Base
=========

Module fondamental fournissant les fonctionnalités de base nécessaires à tous les autres modules SaaS.

**Rôle principal:**
Ce module définit les modèles de base et les classes abstraites utilisées par tous les modules SaaS. Il doit être installé avant tous les autres modules SaaS.

**Fonctionnalités:**
- Modèles de base pour clients et serveurs
- Classes abstraites pour la gestion SaaS
- Méthodes communes partagées entre modules
- Structure de données fondamentale

**Note:** Ce module ne fournit pas d'interface utilisateur, c'est un module technique de base.
""",
    'depends': ['base', 'mail'],
    'data': [
        'views/error_log_views.xml',
        'views/error_templates.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'sequence': 10,
}
