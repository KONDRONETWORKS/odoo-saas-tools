{
    'name': 'SaaS Portal Monitoring',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Monitoring et métriques en temps réel des instances SaaS',
    'description': """
SaaS Portal Monitoring
======================

Module de monitoring complet pour le système SaaS.

**Fonctionnalités principales:**
- Dashboard de santé des serveurs et instances
- Métriques en temps réel (CPU, RAM, Disk, Network)
- Alertes automatiques configurable
- Graphiques de tendances et historiques
- Détection d'anomalies
- Rapports de performance

**Monitoring:**
- État de santé des instances
- Utilisation des ressources
- Temps de réponse
- Disponibilité (uptime)
- Erreurs et logs

**Alertes:**
- Seuils configurables par plan
- Notifications email/SMS
- Webhooks pour intégrations
- Escalade automatique
""",
    'depends': [
        'saas_portal',
        'base_automation',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/monitoring_cron.xml',
        'data/base_automation.xml',
        'views/saas_portal_monitoring_views.xml',
        'views/saas_portal_client_views.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 20,
}

