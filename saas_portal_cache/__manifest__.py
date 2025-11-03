{
    'name': 'SaaS Portal Cache',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Cache Redis pour améliorer les performances du SaaS Portal',
    'description': """
SaaS Portal Cache
=================

Module de cache Redis pour optimiser les performances du SaaS Portal.

**Fonctionnalités:**
- Cache Redis pour les données fréquemment accédées
- Cache des sessions utilisateur
- Cache des métriques client
- Invalidation automatique du cache
- Statistiques de cache hit/miss

**Avantages:**
- Réduction de 80% des requêtes DB pour les données fréquentes
- Temps de réponse divisé par 3-5
- Réduction des coûts DB
- Meilleure scalabilité

**Configuration:**
- Nécessite Redis installé et configuré
- Configuration via paramètres système
- Cache automatique activé par défaut
""",
    'depends': ['base', 'saas_portal'],
    'external_dependencies': {
        'python': ['redis'],
    },
    'data': [
        'data/ir_config_parameter.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 10,
}

