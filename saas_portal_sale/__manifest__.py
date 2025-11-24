{
    'name': 'Saas Portal Sale',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'category': 'SaaS',
    'summary': 'Intégration des ventes avec les plans SaaS - Facturation automatique',
    'description': """
Saas Portal Sale
=================

Module intégrant le système de ventes Odoo avec les plans SaaS, permettant la facturation automatique des abonnements.

**Fonctionnalités principales:**

**Intégration Plans - Produits:**
- Association des plans SaaS avec des produits de vente
- Facturation automatique lors de la création d'une instance
- Gestion des prix selon le plan sélectionné
- Support des facteurs de prix personnalisés

**Facturation:**
- Création automatique de commandes de vente
- Génération de factures pour les abonnements
- Facturation récurrente configurable
- Support des remises et promotions

**Gestion des Produits:**
- Configuration des plans comme produits vendables
- Attributs produits pour différencier les plans
- Codes produits pour identification
- Templates de facturation par plan

**Reporting:**
- Suivi des ventes par plan
- Analyse des revenus SaaS
- Intégration avec le module Analytique
- Tableaux de bord de ventes

**Workflow:**
1. Client commande un plan SaaS
2. Commande de vente créée automatiquement
3. Facture générée selon le plan
4. Instance client créée après paiement (optionnel)

**Intégration:**
- Nécessite sale pour les ventes
- Nécessite saas_product_price_factor pour calcul des prix
- Nécessite analytic pour le reporting
- Nécessite saas_portal_start pour l'initialisation
""",
    'depends': ['sale', 'saas_portal', 'saas_product_price_factor', 'saas_portal_start', 'analytic'],
    'data': ['views/product_template_views.xml', 'views/product_attribute_views.xml', 'views/saas_portal.xml', 'views/pricing_page.xml', 'data/mail_template_data.xml', 'data/ir_config_parameter.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
