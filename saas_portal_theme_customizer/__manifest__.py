# -*- coding: utf-8 -*-
{
    'name': 'SaaS Portal Theme Manager',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'summary': 'Gestion avancée des thèmes pour SaaS Portal',
    'description': """
SaaS Portal Theme Manager
=========================

Module permettant de gérer et personnaliser les thèmes backend dans le portail SaaS.

**Fonctionnalités:**
- Personnalisation des couleurs (primaire, secondaire, accent)
- Image de fond personnalisable
- Configuration depuis Settings > Themes
- Prévisualisation en temps réel
- Export/Import des configurations
""",
    'depends': ['base', 'web', 'saas_portal'],
    'data': [
        'views/res_config_settings_views.xml',
        'security/ir.model.access.csv',
    ],
    'post_init_hook': 'post_init_hook',
    'assets': {
        'web.assets_backend': [
            'saas_portal_theme_customizer/static/src/css/theme_customizer.scss',
            'saas_portal_theme_customizer/static/src/js/theme_manager.js',
        ],
    },
    'installable': True,
    'application': True,
    'sequence': 20,
}

