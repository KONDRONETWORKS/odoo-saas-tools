{
    'name': 'SaaS Auth OAuth - Check Client ID',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Validation du Client ID lors des requêtes OAuth pour sécurité renforcée',
    'description': """
Auth OAuth - Check Client ID
=============================

Module ajoutant une validation supplémentaire du Client ID lors des requêtes OAuth pour renforcer la sécurité du système SaaS.

**Rôle:**
Ce module étend les fonctionnalités OAuth standard d'Odoo en ajoutant une validation stricte du Client ID lors de chaque requête authentifiée.

**Fonctionnalités:**

**Validation Client ID:**
- Vérification que le Client ID correspond à l'application OAuth configurée
- Rejet des requêtes avec Client ID invalide
- Logging des tentatives d'accès non autorisées
- Protection contre les attaques de type token theft

**Sécurité Renforcée:**
- Double validation (token + Client ID)
- Prévention des accès non autorisés
- Audit trail des validations
- Compatible avec les autres modules de sécurité SaaS

**Intégration:**
- Fonctionne avec auth_oauth standard
- Utilisé par saas_client pour validation côté client
- Utilisé par saas_server pour validation côté serveur
- Compatible avec saas_auth_oauth_ip

**Utilisation:**
Ce module fonctionne automatiquement en arrière-plan. Aucune configuration supplémentaire n'est nécessaire après l'installation.
""",
    'depends': ['auth_oauth'],
    'data': [],
    'installable': True,
    'application': False,
    'sequence': 10,
}
