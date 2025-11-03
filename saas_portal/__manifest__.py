{
    'name': 'SaaS Portal',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Portail principal de gestion des instances SaaS - Plans, serveurs et clients',
    'description': """
SaaS Portal
============

Module central du système SaaS qui gère le portail d'administration des instances Odoo.

**Fonctionnalités principales:**

**Gestion des Plans:**
- Création et configuration de plans d'abonnement
- Templates de bases de données par plan
- Limites configurables (utilisateurs, stockage, essais)
- Gestion des états (draft, confirmed)

**Gestion des Serveurs:**
- Configuration de serveurs SaaS distants
- Authentification OAuth2 avec les serveurs
- Synchronisation automatique des données clients
- Gestion des versions Odoo par serveur

**Gestion des Clients:**
- Création automatique d'instances client
- Suivi des bases de données par client
- Gestion des expirations et essais
- Tableau de bord client

**Configuration:**
- Paramètres de domaine SaaS
- Pages d'erreur personnalisables
- Notifications d'expiration
- Équipes de support

**Workflow:**
1. Création d'un plan avec template DB
2. Configuration du serveur de destination
3. Création d'instances client à la demande
4. Synchronisation et monitoring automatique

**Sécurité:**
- Authentification OAuth2 entre Portal et Server
- Gestion des permissions par groupe
- Isolation des données clients
""",
    'depends': ['base', 'saas_oauth_provider', 'website', 'auth_signup', 'saas_base'],
    'data': ['data/mail_template_data.xml', 'data/plan_sequence.xml', 'data/cron.xml', 'wizard/config_wizard_minimal.xml', 'wizard/batch_delete.xml', 'views/saas_portal.xml', 'data/ir_config_parameter.xml', 'data/subtype.xml', 'data/support_team.xml', 'views/res_users.xml', 'data/res_users.xml', 'security/groups.xml', 'security/ir.model.access.csv'],
    'post_init_hook': 'hooks.post_init_hook',
    'post_load': None,
    'installable': True,
    'application': False,
    'sequence': 10,
}
