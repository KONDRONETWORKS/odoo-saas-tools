{
    'name': 'SaaS Portal - templates',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Sélection de templates de bases de données pour la création d\'instances',
    'description': """
SaaS Portal Templates
====================

Module ajoutant une page web permettant de choisir parmi les templates de bases de données disponibles lors de la création d'une nouvelle instance SaaS.

**Fonctionnalités principales:**

- Page de sélection de templates (/saas_portal_templates/select-template)
- Affichage des plans confirmés avec leurs templates
- Création automatique de nouvelle base de données basée sur le template sélectionné
- Interface similaire à accounts.odoo.com/odoo-enterprise/select-app mais basée sur les templates de bases de données

**Utilisation:**

Les utilisateurs peuvent parcourir les templates disponibles et créer une nouvelle instance SaaS en sélectionnant le template qui correspond à leurs besoins.
""",
    'depends': ['saas_portal'],
    'data': ['views/website.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
