{
    'name': 'SaaS Server Rotate Backup',
    'version': '18.0.1.0.0',
    'author': 'Salton Masssally, Cheick Oumar Tidiane Traore',
    'license': 'GPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Rotation automatique des sauvegardes pour éviter l\'accumulation excessive',
    'description': """
SaaS Server Rotate Backup
==========================

Module gérant la rotation automatique des sauvegardes pour éviter l'accumulation excessive et optimiser l'espace de stockage.

**Fonctionnalités principales:**

**Gestion de la Rotation:**
- Suppression automatique des anciennes sauvegardes
- Conservation des sauvegardes récentes (quotidiennes, hebdomadaires, mensuelles)
- Configuration du nombre de sauvegardes à conserver
- Support des stratégies de rétention personnalisées

**Stratégies de Conservation:**
- Sauvegardes quotidiennes (derniers N jours)
- Sauvegardes hebdomadaires (dernières N semaines)
- Sauvegardes mensuelles (derniers N mois)
- Sauvegardes illimitées (option désactivable)

**Automatisation:**
- Action planifiée pour nettoyage automatique
- Rotation basée sur l'âge des fichiers
- Compatible avec saas_server_backup_ftp et autres systèmes de sauvegarde

**Configuration:**
- Interface dans Paramètres > SaaS Server
- Paramètres de rotation configurables par période
- Option pour désactiver la rotation (sauvegardes illimitées)

**Bénéfices:**
- Économie d'espace disque
- Gestion automatique des sauvegardes
- Conservation intelligente des sauvegardes importantes
- Réduction des coûts de stockage

**Utilisation:**
1. Configurer les paramètres de rotation dans Paramètres
2. Activer l'action planifiée "Rotate Backups"
3. Les anciennes sauvegardes seront supprimées automatiquement
""",
    'depends': ['saas_server'],
    'data': ['data/ir_cron.xml', 'views/res_config.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
