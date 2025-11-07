# -*- coding: utf-8 -*-

{
    'name': 'SaaS Sysadmin OVH Route53',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'category': 'SaaS',
    'summary': 'Gestion automatique DNS OVH pour instances SaaS',
    'description': """
SaaS Sysadmin OVH Route53
==========================

Module permettant la gestion automatique des DNS OVH lors de la création/suppression d'instances client.

**Fonctionnalités :**
- Création automatique des enregistrements DNS lors de la création d'une instance
- Mise à jour DNS lors des changements de domaine
- Suppression DNS lors de la suppression d'instance
- Support des zones DNS OVH multiples
- Gestion des types d'enregistrements (A, CNAME, TXT)

**Intégration :**
- Fonctionne avec saas_portal pour les créations d'instances
- Nécessite saas_sysadmin_ovh pour les credentials
""",
    'depends': ['saas_portal', 'saas_sysadmin_ovh'],
    'external_dependencies': {'python': ['ovh']},
    'data': [
        'security/ir.model.access.csv',
        'views/saas_sysadmin_ovh_route53.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 13,
}

