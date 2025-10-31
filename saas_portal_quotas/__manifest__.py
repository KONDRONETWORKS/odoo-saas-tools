{
    'name': 'SaaS Portal Quotas',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Gestion automatique des quotas et limites par plan',
    'description': """
SaaS Portal Quotas
===================

Gestion complète des quotas et limites pour les instances SaaS.

**Fonctionnalités principales:**
- Limites configurables par plan (utilisateurs, stockage, API calls)
- Surveillance en temps réel de la consommation
- Alertes automatiques avant limite atteinte
- Blocage automatique si dépassement
- Upgrade automatique proposé
- Dashboard de consommation
- Historique des quotas utilisés

**Types de quotas:**
- Utilisateurs maximum
- Stockage (disque/FTP)
- Appels API par période
- Modules installables
- Records par modèle
- Bandwidth mensuel

**Fonctionnalités:**
- Alertes configurable (% avant limite)
- Blocage progressif (warning → soft block → hard block)
- Grace period configurable
- Auto-upgrade vers plan supérieur
- Reporting détaillé
""",
    'depends': [
        'saas_portal',
        'base_automation',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/quota_cron.xml',
        'data/base_automation.xml',
        'views/saas_portal_plan_views.xml',
        'views/saas_portal_client_views.xml',
        'views/saas_portal_quota_views.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 25,
}

