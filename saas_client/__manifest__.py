{
    'name': 'SaaS Client',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Module installé sur les instances client pour gérer la connexion au Portal',
    'description': """
SaaS Client
===========

Module installé sur chaque instance client qui permet la communication avec le Portal et la gestion de l'authentification OAuth2.

**Rôle:**
Ce module transforme une instance Odoo standard en "SaaS Client" capable de communiquer avec le Portal pour les mises à jour, synchronisation et gestion.

**Fonctionnalités principales:**

**Authentification OAuth2:**
- Connexion automatique au Portal via OAuth2
- Validation des tokens d'accès
- Gestion sécurisée des identifiants
- Vérification par IP pour sécurité renforcée

**Synchronisation avec Portal:**
- Envoi automatique des statistiques (utilisateurs, stockage)
- Notification des changements d'état
- Synchronisation des paramètres de configuration
- Reporting automatique

**Gestion du Domaine:**
- Affichage du domaine actuel de l'instance
- Redirection vers le Portal pour changement de domaine
- Validation des domaines configurés

**Sécurité:**
- Vérification du Client ID lors des requêtes
- Validation par adresse IP
- Isolation des données client
- Permissions strictes

**Automatisation:**
- Actions planifiées pour synchronisation
- Cron jobs pour reporting
- Notifications automatiques au Portal

**Installation:**
Ce module est automatiquement installé lors de la création d'une instance client via le Portal.
""",
    'depends': ['base', 'auth_oauth', 'saas_auth_oauth_ip', 'saas_auth_oauth_check_client_id', 'mail'],
    'data': ['views/saas_client.xml', 'views/res_config.xml', 'security/rules.xml', 'security/groups.xml', 'data/ir_cron.xml', 'data/auth_oauth_data.xml', 'data/ir_config_parameter.xml', 'data/ir_actions.xml'],
    'assets': {
        'web.assets_backend': [
            'saas_client/static/src/js/saas_client.js',
            'saas_client/static/src/xml/dashboard.xml',
        ],
    },
    'installable': True,
    'application': False,
    'sequence': 10,
}
