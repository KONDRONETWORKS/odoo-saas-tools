{
    'name': 'Create databases after signup custom',
    'summary': 'Création automatique de plusieurs bases de données pour les nouveaux clients après inscription',
    'category': 'SaaS',
    'images': [],
    'version': '18.0.1.0.0',
    'application': False,
    'author': 'IT-Projects LLC, Ildar Nasyrov',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'license': 'GPL-3',
    'description': """
SaaS Portal Signup Custom
==========================

Module permettant la création automatique de plusieurs bases de données pour les nouveaux clients lors de l'inscription, basé sur les produits sélectionnés.

**Fonctionnalités principales:**

**Création Multiple:**
- Création automatique de plusieurs bases de données après inscription
- Basé sur les produits sélectionnés lors de l'inscription
- Configuration par produit pour le nombre de bases à créer
- Support des plans multiples

**Intégration Inscription:**
- Fonctionne avec saas_portal_signup
- Création automatique lors du processus d'inscription
- Association avec les produits achetés
- Configuration via les vues produits

**Personnalisation:**
- Configuration par produit du nombre de bases
- Vues personnalisées pour l'inscription
- Paramètres configurables par plan
- Flexibilité dans la création

**Avantages:**
- Automatisation complète de la création
- Support des offres multi-instances
- Expérience utilisateur simplifiée
- Réduction des erreurs manuelles

**Note:** Ce module est actuellement désactivé (installable: False). Activez-le si vous avez besoin de créer plusieurs bases par client.
""",
    'depends': ['saas_portal_sale', 'saas_portal_signup'],
    'external_dependencies': {'python': [], 'bin': []},
    'data': ['security/ir.model.access.csv', 'views/product_view.xml', 'views/signup.xml', 'views/saas_portal.xml'],
    'qweb': [],
    'demo': [],
    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'auto_install': False,
    'installable': False,
    'sequence': 10,
}
