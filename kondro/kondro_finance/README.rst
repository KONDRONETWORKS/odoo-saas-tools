KONDRO Finance - Gestion Financière Unifiée
=============================================

Module de gestion financière unifié pour KONDRONETWORKS.

Fonctionnalités principales
----------------------------

Gestion de Trésorerie
~~~~~~~~~~~~~~~~~~~~~

* Comptes de trésorerie (Banque, Caisse, Djamo)
* Mouvements financiers (Entrées/Sorties)
* Calcul automatique des soldes
* Traçabilité complète des opérations

Dépenses Unifiées
~~~~~~~~~~~~~~~~~

* Dépenses internes avec workflow complet
* Dépenses commerciales liées aux projets
* Workflow de validation hiérarchique unifié
* Planification des décaissements

Workflow de Paiement
~~~~~~~~~~~~~~~~~~~~

Le workflow complet suit ces étapes :

1. **Brouillon** : Création de la demande
2. **Soumise** : Soumission pour validation
3. **Validée** : Validation par chef de service/projet
4. **Approuvée** : Approbation par direction
5. **Planifiée** : Planification du paiement
6. **Payée** : Exécution et enregistrement automatique
7. **Clôturée** : Clôture de la dépense

Intégration
-----------

* Lien avec kondro_core pour les projets
* Génération automatique des mouvements de trésorerie
* Rapports financiers consolidés

Installation
------------

1. Assurez-vous que ``kondro_company`` et ``kondro_core`` sont installés
2. Installez ce module depuis Apps > Rechercher "KONDRO Finance"
3. Le module créera automatiquement les comptes de trésorerie par défaut

Dépendances
-----------

* base
* mail
* account
* kondro_company
* kondro_core

Comptes par défaut
------------------

Le module crée automatiquement trois comptes de trésorerie :

* **Banque de l'Entreprise** : Pour les opérations bancaires
* **Caisse Principale** : Pour les opérations en espèces
* **Djamo** : Pour les opérations mobile money

Note
----

Ce module remplace les anciens modules :
* kondro_treasury
* kondro_internal_expenses

