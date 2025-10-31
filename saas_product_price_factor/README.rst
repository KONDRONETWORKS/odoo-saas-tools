Product Price Factor
====================

Facteur de prix pour les attributs de produits.

**Description:**
Ce module ajoute la possibilité de définir des facteurs de prix sur les valeurs d'attributs de produits. Lors de la création de variantes de produits, le prix peut être calculé en utilisant ces facteurs.

**Dépendances:**
- product
- sale

**Fonctionnalités:**
- Ajout d'un champ `price_factor` sur `product.attribute.value`
- Calcul du facteur de prix total pour les variantes de produits
- Multiplication des prix basée sur les attributs de produits

**Cas d'usage:**
- Différents prix selon les attributs de produits (taille, couleur, etc.)
- Multiplicateurs de période d'abonnement (mensuel, trimestriel, annuel)
- Multiplicateurs de prix basés sur le nombre d'utilisateurs

**Configuration:**
1. Aller dans Ventes > Configuration > Catégories & Attributs > Attributs
2. Sélectionner un attribut et ses valeurs
3. Pour chaque valeur d'attribut, définir le facteur de prix :
   - 1.0 = prix identique au prix de base
   - 1.5 = augmentation de 50%
   - 0.5 = réduction de 50%
   - 2.0 = doublement du prix

**Exemple d'utilisation:**
Pour un produit SaaS avec attributs "Période" et "Utilisateurs":

- Période "Mensuel" : price_factor = 1.0
- Période "Trimestriel" : price_factor = 1.0 (souvent avec price_extra)
- Période "Annuel" : price_factor = 1.0

- Utilisateurs "1" : price_factor = 1.0
- Utilisateurs "5" : price_factor = 2.0
- Utilisateurs "10" : price_factor = 3.0

Le prix final d'une variante serait : prix_base × facteur_période × facteur_utilisateurs

**Méthodes disponibles:**
- `product.attribute.value._get_price_factor()` : Retourne le facteur de prix d'une valeur d'attribut
- `product.product._get_price_factor_total()` : Calcule le facteur total pour une variante de produit

**Intégration:**
Ce module peut être utilisé par d'autres modules pour appliquer les facteurs de prix :
- Dans `sale.order.line` pour calculer les prix de vente
- Dans `product.pricelist` pour ajuster les prix
- Dans les modules SaaS pour calculer les prix d'abonnement

**Relations:**
- Étend `product.attribute.value` avec le champ `price_factor`
- Étend `product.product` avec la méthode `_get_price_factor_total()`
- Utilisé par `saas_portal_sale` pour les calculs de prix d'abonnement

