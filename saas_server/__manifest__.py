{
    'name': 'SaaS Server',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Module serveur pour créer et gérer les bases de données client via API REST',
    'description': """
SaaS Server
===========

Module installé sur les serveurs distants qui gère la création, modification et suppression des bases de données client.

**Rôle:**
Ce module transforme un serveur Odoo en "SaaS Server" capable de créer et gérer des instances client autonomes.

**Fonctionnalités principales:**

**Gestion des Bases de Données:**
- Création automatique de bases PostgreSQL pour chaque client
- Initialisation d'instances Odoo complètes
- Installation automatique de modules demandés
- Configuration automatique (langue, timezone, démo)

**API REST:**
- Endpoint `/saas_server/new_database` : Création de nouvelles bases
- Endpoint `/saas_server/edit_database` : Modification de bases existantes
- Endpoint `/saas_server/delete_database` : Suppression de bases
- Endpoint `/saas_server/sync_server` : Synchronisation des statistiques

**Sécurité:**
- Authentification OAuth2 requise pour toutes les opérations
- Validation des tokens avant création/suppression
- Isolation complète des bases de données client

**Monitoring:**
- Suivi des statistiques client (utilisateurs, stockage)
- Synchronisation automatique avec le Portal
- Gestion des états (open, pending, deleted)

**Workflow:**
1. Le Portal envoie une requête avec token OAuth2
2. Le Server valide le token
3. Le Server crée la base PostgreSQL
4. Le Server initialise l'instance Odoo
5. Le Server retourne les credentials

**Installation:**
Ce module doit être installé sur chaque serveur distant qui hébergera les instances client.
""",
    'depends': ['base', 'auth_oauth', 'saas_auth_oauth_ip', 'saas_base', 'website'],
    'data': ['views/saas_server.xml', 'views/res_config_settings_views.xml', 'data/auth_oauth_data.xml', 'data/ir_config_parameter.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
