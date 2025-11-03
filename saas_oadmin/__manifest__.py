# saas_oadmin - Gestion Utilisateurs & Administration
{
    'name': 'SaaS Optimized Admin',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Gestion avancée des utilisateurs et administration SaaS',
    'description': """
SaaS Optimized Admin
====================

Module de gestion des utilisateurs et administration du système SaaS.

**Fonctionnalités principales:**

**Gestion Utilisateurs:**
- Utilisateurs étendus avec rôles personnalisés
- Permissions granulaires par module
- Audit trail automatique
- Gestion des sessions

**Rôles & Permissions:**
- Rôles personnalisables (Admin, Manager, Support, Client)
- Permissions par modèle et action
- Héritage de permissions
- Vérification en temps réel

**Sécurité:**
- Authentification OAuth2
- Journalisation des actions
- Détection d'anomalies
- Blocage automatique

**Administration:**
- Tableau de bord administrateur
- Gestion des accès centralisée
- Rapports d'utilisation
- Configuration des droits
""",
    'depends': ['base', 'auth_signup', 'saas_ocore'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/admin_views.xml',
        'data/res_users_data.xml',
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 20,
}

