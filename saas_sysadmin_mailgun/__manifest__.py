{
    'name': 'Saas Sysadmin Mailgun',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'summary': 'Configuration automatique de Mailgun pour permettre l\'envoi et la réception d\'emails',
    'description': """
Saas Sysadmin Mailgun
=====================

Module permettant la configuration automatique de Mailgun pour chaque nouvelle base de données client, permettant l'envoi et la réception d'emails.

**Fonctionnalités principales:**

**Configuration Mailgun Automatique:**
- Configuration automatique de Mailgun lors de la création d'une instance client
- Création des routes email pour chaque domaine client
- Configuration des paramètres SMTP dans l'instance client
- Gestion des domaines Mailgun

**Intégration Mailgun:**
- Utilisation de l'API Mailgun pour configuration
- Création automatique des routes de réception
- Configuration des webhooks pour bounces et événements
- Support de plusieurs domaines Mailgun

**Gestion Email:**
- Configuration SMTP automatique dans les instances client
- Support de l'envoi d'emails transactionnels
- Réception d'emails via routes Mailgun
- Gestion des bounces et spam

**Configuration:**
- Interface de configuration dans Paramètres > SaaS Server
- Configuration de la clé API Mailgun
- Sélection du domaine Mailgun principal
- Paramètres de routage email

**Avantages:**
- Configuration automatique pour chaque nouveau client
- Pas besoin de configurer manuellement Mailgun par client
- Gestion centralisée des emails
- Support des emails transactionnels

**Utilisation:**
1. Créer un compte Mailgun
2. Configurer la clé API dans Paramètres > SaaS Server
3. Les instances créées seront automatiquement configurées pour Mailgun
""",
    'depends': ['base'],
    'external_dependencies': {'python': [], 'bin': []},
    'data': ['views/res_config.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
