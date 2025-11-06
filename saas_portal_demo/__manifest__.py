{
    'name': 'SaaS Portal Demo Databases',
    'summary': 'Tout ce dont vous avez besoin pour créer des démos de vos applications dans Odoo Apps Store',
    'category': 'SaaS',
    'images': [],
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'website': 'https://www.itexperts4africa.com',
    'license': 'GPL-3',
    'description': """
SaaS Portal Demo
================

Module complet pour créer et gérer des bases de données de démonstration pour vos applications dans Odoo Apps Store.

**Fonctionnalités principales:**

**Gestion des Démonstrations:**
- Création automatique de bases de données de démo
- Configuration de produits démo dans le catalogue
- Gestion du cycle de vie des démos
- Expiration automatique des démos

**Intégration Apps Store:**
- Compatible avec Odoo Apps Store
- Création de démos depuis les pages produits
- Liens automatiques vers les instances de démo
- Gestion des accès temporaires

**Automatisation:**
- Tâches cron pour la maintenance des démos
- Nettoyage automatique des démos expirées
- Notifications par email
- Actions automatiques configurables

**Templates et Produits:**
- Configuration de templates de démo
- Association produits-démos
- Personnalisation des pages de démo
- Gestion des variantes de produits

**Sécurité:**
- Accès contrôlé aux démos
- Expiration automatique
- Isolation des données
- Permissions configurées

**Avantages:**
- Facilite la démonstration de vos applications
- Automatisation complète du processus
- Intégration native avec Odoo Apps Store
- Réduction des coûts de maintenance
""",
    'depends': ['saas_portal', 'website_sale', 'saas_portal_sale_online', 'portal'],
    'external_dependencies': {'python': ['requests'], 'bin': []},
    'data': ['security/ir.model.access.csv', 'security/saas_portal_demo.xml', 'views/templates.xml', 'views/saas_portal_demo.xml', 'views/product.xml', 'views/saas_portal_demo_templates.xml', 'data/product.xml', 'data/ir_cron.xml', 'data/mail_template.xml', 'data/ir_actions.xml'],
    'qweb': [],
    'demo': [],
    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 10,
}
