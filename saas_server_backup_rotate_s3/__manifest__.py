{
    'name': 'SaaS Server Rotate Backup S3',
    'version': '18.0.1.0.0',
    'author': 'Salton Masssally, Cheick Oumar Tidiane Traore',
    'license': 'GPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Rotation automatique des sauvegardes stockées sur Amazon S3',
    'description': """
SaaS Server Rotate Backup S3
=============================

Module gérant la rotation automatique des sauvegardes stockées dans Amazon S3, optimisant les coûts de stockage AWS.

**Fonctionnalités principales:**

**Rotation S3:**
- Suppression automatique des anciennes sauvegardes dans S3
- Utilisation de la bibliothèque rotate_backups_s3 pour S3
- Support des stratégies de rétention complexes
- Gestion des transitions vers classes de stockage moins chères (Glacier, Deep Archive)

**Stratégies de Conservation:**
- Conservation intelligente basée sur l'âge
- Sauvegardes récentes (S3 Standard)
- Sauvegardes anciennes (S3 Glacier ou suppression)
- Configuration du nombre de sauvegardes par période

**Optimisation des Coûts:**
- Réduction des coûts de stockage S3
- Migration automatique vers classes moins chères
- Suppression des sauvegardes non nécessaires
- Respect des politiques de cycle de vie S3

**Compatibilité:**
- Fonctionne avec saas_server_backup_s3
- Nécessite saas_server_backup_rotate
- Utilise les credentials AWS configurés dans saas_server_backup_s3

**Dépendances:**
- boto : Bibliothèque Python pour AWS
- rotate_backups_s3 : Bibliothèque spécialisée pour rotation S3

**Avantages:**
- Économie sur les coûts AWS S3
- Gestion automatique du cycle de vie
- Compatible avec les politiques S3 Lifecycle
- Rotation optimisée pour S3

**Installation:**
Ce module nécessite saas_server_backup_s3 et saas_server_backup_rotate.
""",
    'depends': ['saas_server', 'saas_server_backup_s3', 'saas_server_backup_rotate'],
    'external_dependencies': {'python': ['boto', 'rotate_backups_s3'], 'bin': []},
    'data': [],
    'installable': True,
    'application': False,
    'sequence': 10,
}
