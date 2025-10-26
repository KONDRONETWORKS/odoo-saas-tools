SaaS Portal Sale
=================

Vente et facturation de services SaaS.

**Description:**
Ce module permet de vendre des services SaaS via le module de vente Odoo. Il crée des commandes et factures pour les clients SaaS et gère les attributs spécifiques aux produits SaaS.

**Dépendances:**
- saas_portal
- sale

**Codes d'attributs pour produits SaaS:**
- **SUBSCRIPTION_PERIOD** : Période d'abonnement (mensuel, annuel, etc.)
- **MAX_USERS** : Nombre maximum d'utilisateurs autorisés

**Configuration:**
1. Aller dans Ventes > Configuration > Catégories & Attributs > Attributs
2. Créer les attributs avec les codes ci-dessus
3. Assigner les valeurs dans Attributs > Valeurs

**Fonctionnalités:**
- Création automatique de devis pour abonnements
- Génération de factures récurrentes
- Association produits → plan SaaS
- Gestion des périodes d'abonnement
- Application des limites (users, records)

**Workflow de vente:**
1. Client sélectionne un plan sur le portail
2. Un devis est créé automatiquement
3. Client confirme la commande
4. Système crée l'instance SaaS avec les paramètres du produit
5. Facture générée automatiquement

**Intégration:**
- Compatible avec saas_portal_sale_online (boutique web)
- Compatible avec saas_portal_sale_subscription (abonnements)
- Compatible avec payment providers standards

**Known issues:**
- Voir le ticket tracker GitHub

**Relations:**
- Étend le module de vente standard Odoo
- Intègre avec saas_portal pour création d'instances
- Utilisé par la boutique en ligne SaaS
