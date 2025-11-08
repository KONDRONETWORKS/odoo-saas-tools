Kondro DT Hub
=============

Module central du Directeur Technique : fournit un tableau de bord unifié avec
les indicateurs clés (trésorerie, projets, dépenses, portefeuille commercial).

Fonctionnalités
---------------

* Vue kanban regroupant les indicateurs prêts à l’emploi.
* Calcul automatique des métriques via `kondro_core` et `kondro_finance`.
* Menus dédiés au Directeur Technique.
* Intégration avec le bus de messagerie (suivi, notes) pour chaque indicateur.

Installation
------------

1. Installer les dépendances `kondro_core` et `kondro_finance`.
2. Installer ``kondro_dt_hub`` depuis les Apps.
3. Attribuer les groupes ``Kondro - Directeur Technique`` aux utilisateurs.

Configuration
-------------

Les indicateurs fournis par défaut peuvent être enrichis ou ajustés via les vues
formulaires. Les données sont recalculées à l’ouverture et affichées dans le
Hub Directeur Technique.
