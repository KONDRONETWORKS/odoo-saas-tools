{
    'name': 'SaaS Utils',
    'version': '18.0.1.0.1',
    'author': 'ITExperts4Africa, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'support': 'apps@itexperts4africa.com',
    'website': 'http://www.ITExperts4Africa.com',
    'category': 'Base',
    'summary': 'Module d\'utilitaires communs pour le développement et les opérations SaaS',
    'description': """
SaaS Utils
==========

Module contenant des fonctions utilitaires utilisées par l'équipe de développement pour faciliter les opérations courantes dans le système SaaS.

**Fonctionnalités principales:**

- Fonctions utilitaires réutilisables pour la manipulation de données
- Helpers pour le développement et la maintenance
- Outils de connexion et d'appel de méthodes Odoo
- Gestion des bases de données et templates
- Utilitaires pour les scripts d'administration

**Utilisation:**

Ce module est utilisé en interne par les autres modules SaaS et les scripts d'administration pour fournir des fonctionnalités communes et éviter la duplication de code.
""",
    'depends': ['base'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
