Kondro DT Workflow
==================

Orchestre les validations transverses du Directeur Technique : matrices RACI,
validation technique des dépenses et escalades projet.

Fonctionnalités
---------------

* Matrices RACI configurables par processus (dépense interne/commerciale,
  change request) avec lignes utilisateur ou groupe.
* Affectation automatique des participants aux dépenses et notifications
  (Responsible, Accountable, Consulted, Informed).
* Boutons de validation technique, suivi des demandes de modifications et
  activités planifiées.
* Intégration avec les projets et dossiers commerciaux pour appliquer une
  matrice DT par défaut.

Installation
------------

1. Installer ``kondro_dt_hub`` et ``kondro_dt_projects``.
2. Installer ``kondro_dt_workflow`` depuis les Apps.
3. Configurer les matrices RACI dans le menu ``Directeur Technique / Workflow``.

Les matrices s’appliqueront automatiquement lors de la soumission des dépenses
et alimenteront les indicateurs du Hub DT.
