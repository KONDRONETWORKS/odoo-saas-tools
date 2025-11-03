# saas_ocore - Module Base Optimisé
{
    'name': 'SaaS Optimized Core',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Module de base optimisé pour le système SaaS - Fonctionnalités communes',
    'description': """
SaaS Optimized Core
===================

Module fondamental fournissant les fonctionnalités de base nécessaires à tous les autres modules SaaS optimisés.

**Rôle principal:**
Ce module définit les modèles de base, exceptions, utilitaires et configuration partagés par tous les modules SaaS.

**Fonctionnalités:**
- Modèles abstraits pour clients, serveurs et instances
- Système d'exceptions centralisé avec messages utilisateur
- Utilitaires de manipulation de bases de données
- Configuration système centralisée
- Logging et debugging améliorés

**Note:** Ce module doit être installé avant tous les autres modules SaaS optimisés.
""",
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_views.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 10,
    'auto_install': False,
}

