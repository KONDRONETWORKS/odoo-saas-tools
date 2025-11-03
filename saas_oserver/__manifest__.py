# saas_oserver - Gestion Serveurs
{
    'name': 'SaaS Optimized Server',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Gestion optimisée des serveurs et création de bases de données',
    'description': """
SaaS Optimized Server
=====================

Module de gestion des serveurs et création de bases de données optimisé.

**Fonctionnalités principales:**

**Gestion Serveurs:**
- Serveurs avec configuration OAuth
- État et capacité
- Répartition de charge
- Monitoring

**Création de bases:**
- PostgreSQL
- Initialisation Odoo
- Templates
- Déploiement automatique

**Backups:**
- Sauvegardes
- Rotation
- Stockage S3/FTP
- Restauration

**API:**
- RPC sécurisé
- OAuth2
- Rate limiting
- Logs
""",
    'depends': ['saas_ocore', 'auth_oauth'],
    'data': [
        'security/ir.model.access.csv',
        'views/server_views.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 40,
}

