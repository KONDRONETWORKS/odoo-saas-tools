# -*- coding: utf-8 -*-
{
    'name': 'KONDRONETWORKS - Configuration Entreprise',
    'version': '18.0.1.0.0',
    'category': 'Localization',
    'summary': 'Configuration de l\'entreprise KONDRONETWORKS pour la Côte d\'Ivoire',
    'description': """
KONDRONETWORKS - Configuration Entreprise
==========================================

Module de configuration spécifique pour KONDRONETWORKS en Côte d'Ivoire.

**Fonctionnalités:**
- Configuration automatique de l'entreprise KONDRONETWORKS
- Paramètres de localisation Côte d'Ivoire (XOF, langue française)
- Configuration fiscale et légale ivoirienne
- Données de base de l'entreprise
- Paramètres par défaut pour les modules KONDRO

**Informations Entreprise:**
- Nom: KONDRONETWORKS
- Pays: Côte d'Ivoire
- Devise: XOF (Franc CFA Ouest-Africain)
- Langue: Français
- Fuseau horaire: Africa/Abidjan

**Note:** Ce module doit être installé en premier pour configurer correctement l'environnement KONDRONETWORKS.
""",
    'author': 'KONDRONETWORKS',
    'website': 'https://www.kondronetworks.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'base_setup',
    ],
    'data': [
        'data/res_company_data.xml',
        'data/res_currency_data.xml',
        'data/res_country_data.xml',
        'data/res_lang_data.xml',
        'data/ir_config_parameter_data.xml',
        'data/res_users_data.xml',
        'views/res_company_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 1,
}

