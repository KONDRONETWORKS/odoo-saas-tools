# Architecture Simplifiée KONDRONETWORKS

## 📊 Vue d'Ensemble

L'architecture a été simplifiée de **7-8 modules** à **3 modules principaux** tout en conservant une **vue CRM unifiée**.

## 🎯 Modules Principaux (Architecture Finale)

### 1. **kondro_company** ✅
**Rôle :** Configuration de l'entreprise KONDRONETWORKS

**Fonctionnalités :**
- Configuration automatique de l'entreprise
- Paramètres Côte d'Ivoire (XOF, langue française)
- Fuseau horaire Africa/Abidjan

---

### 2. **kondro_core** ✅ (NOUVEAU - FUSIONNÉ)
**Rôle :** Module central CRM avec projets unifiés

**Remplace :** `kondro_commercial_dossier`, `kondro_it_project`, `kondro_audit`

**Fonctionnalités :**
- ✅ Vue CRM unifiée pour tous les projets
- ✅ Projets unifiés (IT, Audit, Commercial)
- ✅ Dossiers commerciaux
- ✅ Gestion des contacts et équipes
- ✅ Documents et pièces jointes
- ✅ Timeline et activités
- ✅ **Dashboard et statistiques** (fusionné depuis kondro_dashboard)
- ✅ **Override CRM** (fusionné depuis kondro_crm_override)

**Modèles :**
- `kondro.project` - Projet unifié
- `kondro.commercial.dossier` - Dossier commercial

---

### 3. **kondro_finance** ✅ (NOUVEAU)
**Rôle :** Gestion financière unifiée

**Remplace :** `kondro_treasury`, `kondro_internal_expenses`

**Fonctionnalités :**
- ✅ Comptes de trésorerie (Banque, Caisse, Djamo)
- ✅ Mouvements financiers (Entrées/Sorties)
- ✅ Dépenses internes avec workflow
- ✅ Dépenses commerciales avec workflow
- ✅ Workflow de paiement unifié
- ✅ Planification des décaissements

**Modèles :**
- `kondro.treasury.account` - Compte de trésorerie
- `kondro.treasury.movement` - Mouvement financier
- `kondro.expense.request` - Demande de dépense (unifiée)

**Workflow :**
```
Brouillon → Soumise → Validée → Approuvée → Planifiée → Payée → Clôturée
```

---

### 4. **kondro_dashboard** ✅ (FUSIONNÉ DANS kondro_core)
**Rôle :** Tableaux de bord et rapports consolidés

**Statut :** Fusionné dans `kondro_core` pour simplifier l'architecture

**Fonctionnalités (dans kondro_core) :**
- Dashboard financier (trésorerie, dépenses)
- Dashboard commercial (projets, budgets, marges)
- Dashboard opérationnel (par service, par projet)
- Statistiques en temps réel

---

## 🔄 Migration depuis les Anciens Modules

### Modules Obsolètes (à migrer progressivement)

| Module Obsolète | Nouveau Module | Statut |
|----------------|----------------|--------|
| `kondro_commercial_dossier` | → `kondro_core` | ✅ Remplacé |
| `kondro_it_project` | → `kondro_core` | ✅ Remplacé |
| `kondro_audit` | → `kondro_core` | ✅ Remplacé |
| `kondro_treasury` | → `kondro_finance` | ✅ Remplacé |
| `kondro_internal_expenses` | → `kondro_finance` | ✅ Remplacé |

### Plan de Migration

1. **Phase 1 :** Installer les nouveaux modules
2. **Phase 2 :** Migrer les données
3. **Phase 3 :** Tester les workflows
4. **Phase 4 :** Déprécier les anciens modules

---

## 🧭 Suite Directeur Technique (DT Hub)

| Module | Rôle | Points clés |
|--------|------|-------------|
| `kondro_dt_hub` | Tableau de bord DT | Indicateurs consolidés (projets, trésorerie, dépenses), notifications ciblées |
| `kondro_dt_projects` | Orchestration projets techniques | Jalons HLD/LLD, risques, artefacts, phase technique & intégration dépenses |
| `kondro_dt_workflow` | Matrices RACI & validations | Matrices par processus, assignation R/A/C/I, escalades et validations techniques |
| `kondro_dt_docs` | Bibliothèque documentaire | Gestion HLD/LLD, versions, approbation, liens projets/dossiers/dépenses |
| `kondro_dt_reporting` | KPI & exports BI | Config KPI, snapshots historisés, tableaux DT, export CSV pour Power BI/Excel |

### Flux DT simplifié
```
Projets/Dossiers → Documents & Jalons → Matrices RACI → KPI & Reporting
```

### Intégrations clés
- Les projets et dossiers exposent des onglets « Technique » / « Docs DT » / « Workflow DT ».
- Les dépenses commerciales utilisent les matrices DT pour la validation technique.
- Les documents validés alimentent le reporting via les indicateurs configurés.
- Les tableaux `kondro_dt_reporting` sont accessibles depuis le hub pour DG/Daf/RH.

---

## 📐 Structure des Données

### Projet Unifié (`kondro.project`)
- Type : IT, Audit, Commercial, Autre
- Statut : Brouillon → Opportunité → En Cours → Livré → Clôturé
- Budget, Engagé, Payé, Marge
- Lien avec dossier commercial
- Lien avec dépenses

### Dossier Commercial (`kondro.commercial.dossier`)
- Client, Commercial, Chef de projet
- Budget, Engagé, Payé, Marge
- Projets liés (One2many)
- Documents commerciaux

### Dépense Unifiée (`kondro.expense.request`)
- Type : Interne ou Commerciale
- Workflow complet de validation
- Lien avec projet (si commerciale)
- Lien avec service (si interne)
- Génération automatique de mouvement de trésorerie

### Mouvement de Trésorerie (`kondro.treasury.movement`)
- Compte (Banque, Caisse, Djamo)
- Type : Entrée ou Sortie
- Lien avec dépense et projet
- Pièces justificatives

---

## 🎨 Vue CRM Unifiée

### Dashboard Principal
- Vue d'ensemble de tous les projets
- Statistiques financières
- Dépenses en attente
- Plan de décaissement

### Kanban des Projets
- Tous les projets (IT, Audit, Commercial) dans une vue
- Filtres par type, statut, responsable
- Progression visuelle

### Timeline
- Activités récentes
- Validations et paiements
- Par projet ou global

---

## ✅ Avantages

- **-70% de modules** : De 7-8 à **3 modules** (fusion supplémentaire)
- **Vue CRM unifiée** : Tous les projets dans une interface
- **Workflow unifié** : Même processus pour dépenses internes/commerciales
- **Maintenance simplifiée** : Moins de code à maintenir
- **Performance** : Moins de requêtes entre modules
- **Expérience utilisateur** : Interface cohérente
- **Architecture optimale** : Tout centralisé dans kondro_core

---

## 📝 Prochaines Étapes

1. ✅ Créer `kondro_core`
2. ✅ Créer `kondro_finance`
3. ✅ Fusionner `kondro_dashboard` dans `kondro_core`
4. ✅ Fusionner `kondro_crm_override` dans `kondro_core`
5. ✅ Déployer la suite Directeur Technique (`kondro_dt_*`)
5. ⏳ Créer les scripts de migration
6. ⏳ Tester les workflows complets
7. ⏳ Documenter la migration

---

## 📚 Documentation

- `ARCHITECTURE_SIMPLIFIEE.md` - Architecture détaillée
- `PLAN_MIGRATION.md` - Plan de migration
- `kondro.md` - Expression de besoin originale

