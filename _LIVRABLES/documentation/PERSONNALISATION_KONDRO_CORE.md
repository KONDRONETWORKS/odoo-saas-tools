# Personnalisation des modules KONDRO

Ce guide explique comment adapter les modules `kondro_core` et ses dépendances pour d'autres entreprises du même secteur.

## 1. Pré-requis

- Odoo 18 installé avec les modules `kondro_core`, `kondro_finance`, `kondro_dt_*` selon les besoins.
- Accès administrateur pour modifier les paramètres systèmes et les droits d'accès.

## 2. Branding du tableau de bord

1. Ouvrir `Paramètres → Général → Tableau de bord secteur`.
2. Modifier :
   - **Titre / Sous-titre** pour refléter le nom et les priorités de l'entreprise.
   - **Devise** (code ISO) et **Locale** pour le format monétaire (`en_US`, `fr_FR`, …).
3. Configurer les actions rapides :
   - Sélectionner l'action à lancer (act_window) pour chaque tuile.
   - Adapter le libellé et l'icône (emoji ou texte bref).

Les valeurs sont stockées via `ir.config_parameter` et prises en compte sans modification de code.

## 3. Adaptation fonctionnelle

- **Modèles** : surcharger les modèles `kondro.project`, `kondro.commercial.dossier`, `kondro.expense.request` via des modules d'extension (ex : `custom_partner_project`).
- **Hooks Python** : le modèle `kondro.dashboard.data` propose des méthodes spécialisées (`get_projects_stats`, `get_treasury_stats`, …). Il est recommandé de les surcharger (`super()`) dans un module dédié pour inclure d'autres indicateurs.
- **Sécurité** : dupliquer les groupes `kondro_core.group_*` si de nouvelles policies sont nécessaires puis ajuster les règles `ir.rule`.

## 4. Assets et thèmes

- Les fichiers CSS/JS sont centralisés dans `kondro_core/static/src`.
- Ajouter un module theme spécifique si des modifications lourdes sont nécessaires, plutôt que d'éditer directement les fichiers fournis.

## 5. Tests et validation

- Relancer la suite JS (`./odoo-bin --test-tags web`) si des composants OWL sont modifiés.
- Pour la logique métier, utiliser `./odoo-bin --test-tags kondro_core` après avoir créé des tests dans `kondro_core/tests`.
- Vérifier les scénarios principaux : création de projets, flux dépenses, rafraîchissement du dashboard.

## 6. Flux de déploiement

1. Mettre à jour les paramètres via l'interface ou en script (`ir.config_parameter.set_param`).
2. Appliquer les modules personnalisés (`./odoo-bin -u custom_module`).
3. Exécuter les tests automatisés dans la CI (cf. workflow `.github/workflows/ci.yml`).
4. Pousser en staging puis production via le job de déploiement GitHub.

## 7. Bonnes pratiques

- Centraliser les personnalisations dans un module `custom_<client>` pour simplifier les montées de version.
- Documenter les actions rapides sélectionnées et les paramètres liés à la devise.
- Sauvegarder les valeurs `ir.config_parameter` dans un script d'init pour répliquer rapidement un environnement.

---

**Contact** : Équipe SaaS/KONDRO Networks – support interne.*** End Patch

