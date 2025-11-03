{
    'name': 'SaaS Server Backup S3',
    'version': '18.0.1.0.0',
    'author': 'Salton Massally, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Sauvegarde automatique des bases de données client vers Amazon S3',
    'description': """
SaaS Server Backup S3
======================

Module permettant la sauvegarde automatique des bases de données client vers Amazon S3 (Simple Storage Service).

**Fonctionnalités principales:**

**Configuration AWS S3:**
- Configuration des identifiants AWS (Access Key ID et Secret Key)
- Sélection du bucket S3 de destination
- Support de tous les types de buckets AWS S3
- Validation des credentials avant sauvegarde

**Sauvegarde Automatique:**
- Sauvegarde automatique des bases de données client
- Format : Dumps PostgreSQL compressés
- Upload direct vers S3
- Planification via actions planifiées Odoo

**Avantages S3:**
- Stockage scalable et durable
- Réplication automatique AWS
- Accès rapide depuis n'importe où
- Gestion du cycle de vie des objets
- Compatible avec saas_server_backup_rotate_s3 pour rotation

**Sécurité:**
- Credentials AWS stockés de manière sécurisée
- Connexions HTTPS vers AWS
- Support IAM pour permissions granulaires

**Configuration:**
- Interface de configuration dans Paramètres > SaaS Server
- Section dédiée "AWS S3 Backup Settings"
- Champs masqués pour les secrets

**Dépendances:**
- boto : Bibliothèque Python pour AWS SDK
- saas_server : Module de base serveur

**Utilisation:**
1. Créer un bucket S3 dans AWS
2. Créer des credentials IAM avec accès S3
3. Configurer dans Paramètres > SaaS Server > AWS S3 Access
4. Activer les sauvegardes automatiques
""",
    'external_dependencies': {'python': ['boto']},
    'depends': ['saas_server'],
    'data': ['views/res_config.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
