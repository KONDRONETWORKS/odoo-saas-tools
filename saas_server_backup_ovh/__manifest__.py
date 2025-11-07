# -*- coding: utf-8 -*-

{
    'name': 'SaaS Server Backup OVH',
    'version': '18.0.1.0.0',
    'author': 'Salton Massally, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Sauvegarde des bases SaaS vers OVH Object Storage (Swift/S3 compatible)',
    'description': """
SaaS Server Backup OVH
======================

Module de sauvegarde automatique des bases client vers OVH Object Storage.

Fonctionnalités :
- Paramétrage du projet Public Cloud OVH (Application/Consumer Key + Project ID)
- Configuration du container Object Storage et de la région
- Champs prêts pour intégrer les scripts d'upload (Swift API ou S3 compatible)

Le module stocke les identifiants côté Odoo et fournit l'interface de configuration pour les scripts de sauvegarde planifiée.
""",
    'depends': ['saas_server'],
    'external_dependencies': {'python': ['ovh']},
    'data': ['views/res_config.xml'],
    'installable': True,
    'application': False,
    'sequence': 11,
}


