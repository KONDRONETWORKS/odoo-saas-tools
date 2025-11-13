# -*- coding: utf-8 -*-
{
    'name': 'KONDRO Core - CRM Unifié',
    'version': '18.0.1.0.0',
    'category': 'KONDRO/CRM',
    'summary': 'Module central CRM avec projets unifiés et dossiers commerciaux',
    'description': """
KONDRO Core - CRM Unifié
========================

Module central offrant une vue CRM complète et unifiée pour tous les projets et dossiers commerciaux.

**Fonctionnalités principales:**

**Vue CRM Unifiée:**
- Dashboard central avec vue d'ensemble de tous les projets
- Kanban unifié pour IT, Audit et projets commerciaux
- Timeline et activités pour suivi en temps réel
- Gestion des contacts, clients et équipes

**Projets Unifiés:**
- Un seul modèle pour tous les types de projets (IT, Audit, Commercial)
- Suivi budgétaire et financier intégré
- Gestion des équipes et responsabilités
- Documents et pièces jointes centralisés

**Dossiers Commerciaux:**
- Gestion complète des dossiers clients
- Lien avec projets et dépenses
- Documents commerciaux (devis, factures, commandes)
- Suivi des budgets et marges

**Intégration:**
- Lien avec kondro_finance pour les dépenses
- Lien avec kondro_dashboard pour les rapports
- Compatible avec les modules Odoo standards (CRM, Sales, Project)

**Note:** Ce module remplace kondro_commercial_dossier, kondro_it_project et kondro_audit.
""",
    'author': 'KONDRONETWORKS',
    'website': 'https://www.kondronetworks.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'contacts',
        'crm',
        'sale',
        'project',
        'kondro_company',
    ],
    'data': [
        'security/kondro_core_security.xml',
        'security/ir.model.access.csv',
        'data/kondro_core_data.xml',
        'views/kondro_project_views.xml',
        'views/kondro_commercial_dossier_views.xml',
        'views/kondro_crm_dashboard_views.xml',
        'views/kondro_dashboard_views.xml',
        'views/kondro_menu.xml',
        'views/res_config_settings.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'kondro_core/static/src/css/crm_dashboard.css',
            'kondro_core/static/src/css/dashboard.css',
            'kondro_core/static/src/js/crm_dashboard.js',
            'kondro_core/static/src/js/dashboard.js',
            'kondro_core/static/src/xml/dashboard_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 10,
    'pre_init_hook': 'pre_init_hook',
}

