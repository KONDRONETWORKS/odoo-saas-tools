{
    'name': 'SaaS Portal Sale Subscription',
    'version': '18.0.1.0.0',
    'author': 'PlanetaTIC, IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'info@planetatic.com',
    'website': 'https://www.planetatic.com',
    'summary': 'Intégration des ventes avec la gestion des abonnements SaaS',
    'description': """
SaaS Portal Sale Subscription
==============================

Module intégrant la gestion des ventes avec le système d'abonnements SaaS pour une facturation et gestion complète.

**Fonctionnalités principales:**

**Intégration Vente-Abonnement:**
- Synchronisation automatique entre les factures et les abonnements
- Mise à jour automatique des dates d'expiration lors de la facturation
- Gestion des renouvellements d'abonnement
- Suivi des paiements et expirations

**Gestion des Factures:**
- Vue dédiée pour les factures liées aux abonnements SaaS
- Affichage des informations d'abonnement sur les factures
- Mise à jour automatique des dates d'expiration
- Historique complet des facturations

**Attributs Produit:**
- Configuration des attributs produits pour les plans SaaS
- Facteurs de prix configurables par attribut
- Gestion des variantes de produits
- Intégration avec les plans SaaS

**Wizard d'Abonnement:**
- Interface pour modifier les abonnements depuis les factures
- Synchronisation bidirectionnelle facture-abonnement
- Gestion des renouvellements
- Calcul automatique des nouvelles dates

**Avantages:**
- Facturation automatisée des abonnements
- Synchronisation complète entre ventes et abonnements
- Gestion simplifiée des renouvellements
- Traçabilité financière complète
""",
    'depends': ['saas_portal_sale', 'saas_portal_subscription'],
    'data': ['views/account_invoice_view.xml', 'views/product_attribute_views.xml', 'views/saas_portal.xml', 'wizard/subscription_wizard.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
