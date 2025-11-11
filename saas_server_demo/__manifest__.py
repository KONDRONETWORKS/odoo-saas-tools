{
    'name': 'Saas Server Demo',
    'summary': 'Paramètres et contrôle des dépôts pour la création de modules de démonstration',
    'category': 'SaaS',
    'images': [],
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'website': 'https://www.itexperts4africa.com',
    'license': 'GPL-3',
    'description': """
SaaS Server Demo
================

Module ajoutant des paramètres spécifiques pour les modules de démonstration et le contrôle des dépôts Git utilisés pour les démos.

**Fonctionnalités principales:**

**Configuration des Démonstrations:**
- Paramètres spécifiques dans les manifests pour les modules démo
- Contrôle des dépôts Git utilisés pour les démonstrations
- Configuration des modules à installer dans les démos
- Gestion des versions et branches

**Contrôle des Dépôts:**
- Configuration des dépôts Git pour les démos
- Gestion des branches et tags
- Contrôle d'accès aux dépôts
- Synchronisation automatique

**Vues de Configuration:**
- Interface pour configurer les paramètres de démo
- Gestion des dépôts depuis l'interface
- Configuration des modules démonstratifs
- Paramètres avancés

**Intégration:**
- Fonctionne avec saas_server pour la création de bases
- Compatible avec saas_portal_demo
- Support des modules Odoo standard
- Gestion des dépendances

**Avantages:**
- Configuration centralisée des démos
- Contrôle précis des dépôts utilisés
- Automatisation de la création de démos
- Flexibilité dans la configuration
""",
    'depends': ['saas_server'],
    'external_dependencies': {'python': [], 'bin': ['git']},
    'data': ['views/saas_server_demo.xml'],
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
