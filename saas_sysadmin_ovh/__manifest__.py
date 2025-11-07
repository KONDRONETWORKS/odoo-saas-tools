# -*- coding: utf-8 -*-

{
    'name': 'SaaS Sysadmin OVH',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'category': 'SaaS',
    'summary': "Configuration OVH API pour la gestion automatique des DNS d'instances SaaS",
    'description': """
SaaS Sysadmin OVH
=================

Module fournissant l'intégration OVH (API v6) pour automatiser la gestion DNS des instances client.

Fonctionnalités clés :
- Stockage sécurisé des identifiants OVH (Application Key, Application Secret, Consumer Key)
- Paramétrage de l'endpoint OVH (ovh-eu, ovh-ca, etc.) et du domaine racine
- Hooks prêts à l'emploi pour créer / mettre à jour / supprimer les entrées DNS depuis saas_server

Ce module prépare les paramètres nécessaires afin que les scripts d'automatisation puissent piloter OVH DNS depuis Odoo.
""",
    'depends': ['base'],
    'data': ['views/res_config.xml'],
    'installable': True,
    'application': False,
    'sequence': 12,
}


