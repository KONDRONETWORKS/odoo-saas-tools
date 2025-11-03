# saas_oclient - Gestion Clients & Instances
{
    'name': 'SaaS Optimized Client',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Gestion optimisée des clients et instances SaaS',
    'description': """
SaaS Optimized Client
=====================

Module de gestion des clients et instances SaaS optimisé.

**Fonctionnalités principales:**

**Gestion Clients:**
- Clients avec données complètes
- Multi-instances par client
- Suivi de l'historique
- Statistiques d'utilisation

**Instances:**
- Création/gestion instances
- Templates configurables
- Déploiement automatique
- Monitoring temps réel

**Plans:**
- Plans tarifaires
- Limites et quotas
- Renouvellement auto
- Facturation

**Monitoring:**
- Métriques en temps réel
- Alertes automatiques
- Rapports personnalisés
- Dashboard client
""",
    'depends': ['saas_ocore', 'saas_oadmin'],
    'data': [
        'security/ir.model.access.csv',
        'views/client_views.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'sequence': 30,
}

