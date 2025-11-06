{
    'name': 'Saas Portal Sale Online',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://twitter.com/nasyrov_ildar',
    'category': 'SaaS',
    'version': '18.0.1.0.0',
    'summary': 'Vente en ligne de plans SaaS directement depuis le site web',
    'description': """
SaaS Portal Sale Online
========================

Module permettant la vente en ligne de plans SaaS directement depuis le site web public, avec intégration complète du e-commerce Odoo.

**Fonctionnalités principales:**

**Boutique en Ligne:**
- Affichage des plans SaaS comme produits sur le site web
- Intégration avec website_sale pour le processus d'achat
- Bouton "Try trial" sur les pages produits
- Création automatique d'instance d'essai depuis le site

**Processus d'Achat:**
- Les clients peuvent acheter des plans SaaS directement en ligne
- Connexion requise pour l'achat (website_sale_require_login)
- Intégration avec le panier et le processus de paiement
- Création automatique de l'instance après achat

**Essai Gratuit:**
- Bouton "Try trial" visible sur chaque produit SaaS
- Création d'instance d'essai sans achat
- Redirection vers la création de client avec paramètre trial=1
- Expérience utilisateur fluide

**Avantages:**
- Vente automatisée des plans SaaS
- Réduction de la friction pour les nouveaux clients
- Essais gratuits facilités
- Intégration native avec le e-commerce Odoo
""",
    'depends': ['website_sale', 'saas_portal', 'saas_portal_sale', 'website_sale_require_login'],
    'data': ['views/templates.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
