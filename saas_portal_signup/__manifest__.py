{
    'name': 'SaaS Portal Sign Up',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Inscription automatique de nouveaux clients lors de l\'inscription sur le portail',
    'description': """
SaaS Portal Sign Up
===================

Module permettant l'inscription automatique de nouveaux clients dans le système SaaS lors de l'inscription sur le portail web.

**Fonctionnalités principales:**

**Inscription Automatique:**
- Création automatique d'un enregistrement client lors de l'inscription
- Association automatique avec le compte utilisateur créé
- Configuration par défaut selon les paramètres du Portal

**Workflow d'Inscription:**
1. Utilisateur s'inscrit sur le portail web
2. Compte utilisateur créé via auth_signup
3. Enregistrement client créé automatiquement dans saas_portal.client
4. Association automatique utilisateur-client

**Configuration:**
- Utilise les templates de formulaire d'inscription Odoo
- Personnalisation via vues XML
- Intégration transparente avec auth_signup

**Avantages:**
- Automatisation complète du processus
- Pas besoin de créer manuellement le client
- Expérience utilisateur fluide
- Réduction des erreurs manuelles

**Utilisation:**
Ce module fonctionne automatiquement lors de l'inscription d'un nouvel utilisateur sur le portail web. Aucune configuration supplémentaire n'est nécessaire.
""",
    'depends': ['auth_signup', 'saas_portal'],
    'data': ['views/signup.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
