# Architecture Simplifiée - Modules KONDRONETWORKS

## 📊 Analyse des Besoins

D'après `kondro.md`, les besoins principaux sont :
1. **Gestion de trésorerie** (caisse, banque, Djamo)
2. **Workflow de paiement** (dépenses internes + commerciales)
3. **Dossiers commerciaux** avec projets
4. **Vue CRM/Overview** pour suivi global
5. **Rapports et tableaux de bord**

## 🎯 Solution : 3 Modules Principaux

### 1. **kondro_core** - Module Central avec Vue CRM
**Rôle :** Vue d'ensemble CRM unifiée + Configuration de base

**Fonctionnalités :**
- **Dashboard CRM** : Vue unifiée de tous les projets, dossiers, dépenses
- **Dossiers commerciaux** : Gestion complète des dossiers clients
- **Projets unifiés** : IT, Audit, Commercial (un seul modèle de projet)
- **Contacts et relations** : Clients, fournisseurs, équipes
- **Documents** : Gestion centralisée des pièces jointes
- **Activités et suivi** : Timeline, activités, notes

**Avantages :**
- Vue CRM complète pour tous les projets
- Un seul point d'entrée pour la gestion commerciale
- Suivi unifié des opportunités et projets

---

### 2. **kondro_finance** - Gestion Financière Unifiée
**Rôle :** Trésorerie + Dépenses (internes + commerciales) + Workflow de paiement

**Fonctionnalités :**
- **Comptes de trésorerie** : Banque, Caisse, Djamo
- **Mouvements financiers** : Entrées/Sorties avec traçabilité
- **Dépenses internes** : Workflow complet (Brouillon → Payée → Clôturée)
- **Dépenses commerciales** : Liées aux projets avec workflow
- **Workflow de paiement** : Validation hiérarchique unifiée
- **Planification** : Plan de décaissement
- **Rapports financiers** : État de trésorerie, suivi des dépenses

**Avantages :**
- Un seul module pour toute la gestion financière
- Workflow unifié pour dépenses internes et commerciales
- Traçabilité complète des flux financiers

---

### 3. **kondro_dashboard** - Tableaux de Bord et Rapports
**Rôle :** Visualisation et reporting avancé

**Fonctionnalités :**
- **Dashboard financier** : Solde trésorerie, plan de décaissement
- **Dashboard commercial** : Projets, budgets, marges
- **Dashboard opérationnel** : Dépenses par service, par projet
- **Rapports personnalisés** : Excel/PDF avec filtres
- **KPI en temps réel** : Indicateurs de performance

**Avantages :**
- Vue consolidée de tous les indicateurs
- Rapports personnalisables
- Export facile

---

## 🔄 Migration depuis les Modules Existants

### Modules à Fusionner

| Module Actuel | Nouveau Module | Fonctionnalités Migrées |
|--------------|----------------|-------------------------|
| `kondro_commercial_dossier` | → `kondro_core` | Dossiers commerciaux |
| `kondro_it_project` | → `kondro_core` | Projets IT (unifié avec projets commerciaux) |
| `kondro_audit` | → `kondro_core` | Projets d'audit (unifié) |
| `kondro_treasury` | → `kondro_finance` | Comptes et mouvements de trésorerie |
| `kondro_internal_expenses` | → `kondro_finance` | Dépenses internes + workflow |
| `kondro_dashboard` | → `kondro_dashboard` | Amélioré avec plus de vues |

### Modules à Conserver

- `kondro_company` : Configuration entreprise (déjà créé)
- `kondro_crm_override` : Personnalisations CRM (si nécessaire)

---

## 📐 Structure des Modèles Unifiés

### Dans `kondro_core`

```python
# Projet unifié (remplace IT, Audit, Commercial)
kondro.project
  - name, client_id, type (it/audit/commercial)
  - commercial_dossier_id (lien avec dossier)
  - budget, actual_cost
  - status, priority
  - team members
  - documents
  - timeline/activities

# Dossier commercial
kondro.commercial.dossier
  - client_id, commercial_id
  - project_ids (One2many vers kondro.project)
  - documents (devis, factures, etc.)
  - expenses (liées via projet)
```

### Dans `kondro_finance`

```python
# Compte de trésorerie
kondro.treasury.account
  - name (Banque, Caisse, Djamo)
  - initial_balance
  - current_balance (computed)

# Mouvement financier
kondro.treasury.movement
  - account_id, movement_type (in/out)
  - amount, date, method
  - partner_id (fournisseur/client)
  - project_id (si dépense commerciale)
  - expense_request_id (si dépense interne)

# Demande de dépense (unifiée)
kondro.expense.request
  - type (internal/commercial)
  - project_id (si commercial)
  - workflow: draft → submitted → validated → approved → planned → paid → closed
  - treasury_movement_id (lien avec mouvement)
```

---

## 🎨 Vue CRM Unifiée

### Dashboard Principal (`kondro_core`)

**Vue Kanban des Projets :**
- Colonnes : Opportunités → En Cours → Validation → Livré → Clôturé
- Cartes avec : Client, Budget, Dépenses, Progression
- Filtres : Type, Responsable, Période

**Vue Liste des Dossiers :**
- Numéro, Client, Commercial, Budget, Engagé, Payé, Marge
- Lien direct vers projets associés

**Vue Timeline :**
- Activités récentes (dépenses, validations, paiements)
- Par projet ou global

**Widgets Dashboard :**
- Trésorerie (solde caisse, banque, Djamo)
- Dépenses en attente de validation
- Projets en cours
- Plan de décaissement à venir

---

## ✅ Avantages de cette Architecture

1. **Moins de modules** : 3 au lieu de 7-8
2. **Vue CRM unifiée** : Tous les projets dans une seule interface
3. **Workflow unifié** : Même processus pour dépenses internes/commerciales
4. **Maintenance simplifiée** : Moins de dépendances, code plus cohérent
5. **Performance** : Moins de requêtes entre modules
6. **Évolutivité** : Facile d'ajouter de nouveaux types de projets

---

## 🚀 Plan d'Implémentation

### Phase 1 : Créer `kondro_core`
- Modèle de projet unifié
- Dossiers commerciaux
- Vue CRM/Overview
- Migration des données depuis `kondro_commercial_dossier`, `kondro_it_project`, `kondro_audit`

### Phase 2 : Créer `kondro_finance`
- Fusionner `kondro_treasury` + `kondro_internal_expenses`
- Workflow unifié de dépenses
- Lien avec projets de `kondro_core`
- Migration des données

### Phase 3 : Améliorer `kondro_dashboard`
- Intégrer les nouvelles vues
- Ajouter les KPIs financiers et commerciaux
- Rapports personnalisés

### Phase 4 : Déprécier les anciens modules
- Marquer comme obsolètes
- Documentation de migration
- Support temporaire pour compatibilité

---

## 📋 Checklist de Migration

- [ ] Créer `kondro_core` avec modèles unifiés
- [ ] Créer `kondro_finance` avec workflow unifié
- [ ] Migrer les données des anciens modules
- [ ] Créer les vues CRM unifiées
- [ ] Tester les workflows complets
- [ ] Documenter la migration
- [ ] Former les utilisateurs
- [ ] Déprécier les anciens modules

---

## 💡 Recommandation Finale

**Adopter cette architecture simplifiée permet de :**
- Réduire la complexité de 7-8 modules à 3 modules
- Offrir une vue CRM complète et unifiée
- Simplifier la maintenance et l'évolution
- Améliorer l'expérience utilisateur avec une interface cohérente

**Le module `kondro_core` devient le point d'entrée principal avec une vue CRM complète, tandis que `kondro_finance` gère toute la partie financière de manière unifiée.**

