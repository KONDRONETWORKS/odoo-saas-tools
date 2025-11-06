{
    'name': 'SaaS Portal Tagging',
    'summary': 'Système d\'étiquetage pour organiser et filtrer les bases de données client',
    'version': '18.0.1.0.0',
    'author': 'Salton Massally <salton.massally@gmail.com>, Cheick Oumar Tidiane Traore',
    'license': 'GPL-3',
    'category': 'SaaS',
    'website': 'idtlabs.sl',
    'description': """
SaaS Portal Tagging
===================

Module permettant d'ajouter des étiquettes (tags) aux bases de données client pour faciliter l'organisation, le filtrage et la recherche.

**Fonctionnalités principales:**

**Système d'Étiquetage:**
- Ajout de tags multiples par base de données
- Création et gestion de tags personnalisés
- Catégorisation flexible des instances
- Organisation hiérarchique possible

**Filtrage et Recherche:**
- Filtrage des clients par tags
- Recherche rapide par étiquettes
- Vues personnalisées par tag
- Groupement automatique

**Wizard de Gestion:**
- Interface simple pour ajouter/supprimer des tags
- Gestion en masse des étiquettes
- Application rapide sur plusieurs clients
- Prévisualisation des changements

**Avantages:**
- Organisation améliorée des instances
- Recherche et filtrage facilités
- Catégorisation flexible
- Gestion simplifiée de grandes quantités de clients

**Cas d'usage:**
- Organiser par type de client (entreprise, particulier)
- Marquer par statut (actif, essai, expiré)
- Catégoriser par secteur d'activité
- Grouper par plan ou fonctionnalités
""",
    'depends': ['saas_portal'],
    'data': ['views/saas_portal_tagging_views.xml', 'views/wizard.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
