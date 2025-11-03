{
    'name': 'SaaS Server Backup SFTP',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'GPL-3',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'category': 'SaaS',
    'summary': 'Sauvegarde automatique des bases de données client via SFTP',
    'description': """
SaaS Server Backup SFTP
========================

Module permettant la sauvegarde automatique des bases de données client vers un serveur SFTP distant.

**Fonctionnalités principales:**

**Configuration SFTP:**
- Configuration du serveur SFTP (adresse IP/hostname)
- Authentification par nom d'utilisateur/mot de passe
- Support de l'authentification par clé RSA
- Configuration du chemin de destination des sauvegardes

**Sauvegarde Automatique:**
- Sauvegarde automatique des bases de données client
- Format : Dumps PostgreSQL compressés
- Planification via actions planifiées Odoo
- Support de la rotation des sauvegardes (avec saas_server_backup_rotate)

**Sécurité:**
- Support des clés SSH RSA
- Passphrase pour les clés privées
- Validation de la clé publique du serveur
- Connexions sécurisées SFTP

**Configuration:**
- Interface de configuration dans Paramètres > SaaS Server
- Test de connexion SFTP intégré
- Validation des paramètres avant sauvegarde

**Dépendances:**
- pysftp : Bibliothèque Python pour connexions SFTP
- saas_server : Module de base serveur

**Utilisation:**
1. Configurer les paramètres SFTP dans Paramètres
2. Activer l'action planifiée "Backup saas databases scheduler"
3. Les sauvegardes seront créées automatiquement
""",
    'depends': ['saas_server'],
    'external_dependencies': {'python': ['pysftp'], 'bin': []},
    'data': ['views/res_config.xml', 'data/ir_cron.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
