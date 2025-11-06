{
    'name': 'SaaS Server - Autodelete expired databases',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Suppression automatique des bases de données expirées pour libérer les ressources',
    'description': """
SaaS Server - Autodelete Expired Databases
==========================================

Module ajoutant une tâche planifiée (cron) pour supprimer automatiquement les bases de données expirées, libérant ainsi les ressources serveur.

**Fonctionnalités principales:**

**Suppression Automatique:**
- Tâche cron exécutée toutes les heures
- Détection automatique des bases de données expirées
- Suppression sécurisée des instances expirées
- Libération automatique des ressources (espace disque, mémoire)

**Gestion des Essais:**
- Suppression automatique des bases d'essai expirées
- Respect des périodes de grâce configurées
- Conservation des bases actives
- Protection contre les suppressions accidentelles

**Configuration:**
- Exécution horaire par défaut (configurable)
- Basé sur les dates d'expiration des clients SaaS
- Intégration avec saas_server pour la gestion des bases

**Avantages:**
- Libération automatique de l'espace disque
- Réduction des coûts d'infrastructure
- Maintenance automatisée
- Pas d'intervention manuelle nécessaire

**Sécurité:**
- Seules les bases expirées sont supprimées
- Vérification des dates avant suppression
- Logs des suppressions effectuées
- Pas de suppression de bases actives

**Utilisation:**
Ce module fonctionne automatiquement après installation. La tâche cron se déclenche toutes les heures pour vérifier et supprimer les bases expirées.
""",
    'depends': ['saas_server'],
    'data': ['data/ir_cron.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
