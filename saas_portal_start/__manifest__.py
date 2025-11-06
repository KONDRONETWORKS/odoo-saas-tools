{
    'name': 'SaaS Portal - /page/start',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Page de démarrage et d\'inscription pour le portail SaaS',
    'description': """
SaaS Portal Start
=================

Module créant la page d'accueil et d'inscription du portail SaaS, similaire à https://www.odoo.com/page/start.

**Fonctionnalités principales:**

- Page d'accueil personnalisable pour le portail SaaS
- Affichage des plans disponibles
- Formulaire d'inscription intégré
- Sélection de plan lors de l'inscription
- Route /page/start pour l'accès public

**Utilisation:**

Ce module permet aux nouveaux clients de découvrir les plans disponibles et de s'inscrire directement depuis la page d'accueil du portail SaaS.
""",
    'depends': ['website', 'saas_portal'],
    'data': ['views/website.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
