{
    'name': 'SaaS System Administration',
    'summary': 'Framework d\'administration système pour les outils SaaS',
    'version': '18.0.1.0.0',
    'author': 'Salton Massally <smassally@idtlabs.sl> (iDT Labs), Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'website': 'idtlabs.sl',
    'description': """
SaaS System Administration
===========================

Framework d'administration système fournissant les fonctionnalités de base pour la gestion et l'administration des outils SaaS.

**Fonctionnalités principales:**

**Framework d'Administration:**
- Structure de base pour les modules d'administration
- Interfaces communes pour la gestion système
- Méthodes utilitaires partagées
- Architecture extensible

**Gestion Système:**
- Vues d'administration centralisées
- Configuration des paramètres système
- Monitoring et supervision
- Outils de maintenance

**Extensibilité:**
- Base pour d'autres modules sysadmin (AWS, Route53, Mailgun)
- Architecture modulaire
- Interfaces standardisées
- Facilite l'ajout de nouvelles fonctionnalités

**Intégration:**
- Fonctionne avec saas_portal
- Compatible avec les autres modules SaaS
- Support des configurations avancées
- Intégration avec les services externes

**Avantages:**
- Architecture cohérente pour l'administration
- Réduction de la duplication de code
- Facilité d'extension
- Maintenance simplifiée
""",
    'depends': ['saas_portal'],
    'data': ['views/saas_portal_views.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
