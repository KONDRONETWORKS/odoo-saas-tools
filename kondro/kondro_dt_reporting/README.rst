Kondro DT Reporting
===================

Module BI orienté KPI pour le Directeur Technique : suivi consolidé,
visualisations et export rapide.

Fonctionnalités
---------------

* Configurations KPI (code, domaine, agrégateur, périodicité) avec calcul
  automatique via cron.
* Historique des snapshots (graph/pivot) et tableaux personnalisés regroupant
  plusieurs indicateurs.
* Actions rapides depuis le Hub DT : menus KPIs, Tableaux, Export.
* Assistant d’export CSV prêt pour Excel / Power BI.
* Lien direct vers les enregistrements sources (projets, dépenses, documents).

Installation
------------

1. Installer les modules ``kondro_dt_hub``, ``kondro_dt_projects``,
   ``kondro_dt_workflow`` et ``kondro_dt_docs``.
2. Installer ``kondro_dt_reporting`` depuis les Apps.
3. Définir vos premiers KPI via le menu « Reporting / Configurations » puis
   lancer « Actualiser ».

Les KPIs alimentent automatiquement les tableaux et peuvent être exportés pour
une exploitation dans des outils BI externes.
