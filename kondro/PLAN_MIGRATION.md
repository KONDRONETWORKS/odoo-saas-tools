# Plan de Migration vers Architecture Simplifiée

## 🎯 Objectif
Réduire de 7-8 modules à 3 modules principaux tout en conservant une vue CRM unifiée.

## 📦 Nouveaux Modules à Créer

### 1. kondro_core (Module Central CRM)
**Remplace :** `kondro_commercial_dossier`, `kondro_it_project`, `kondro_audit`

**Fonctionnalités :**
- ✅ Dossiers commerciaux
- ✅ Projets unifiés (IT, Audit, Commercial)
- ✅ Vue CRM/Overview
- ✅ Gestion des contacts et équipes
- ✅ Documents et pièces jointes
- ✅ Activités et timeline

### 2. kondro_finance (Gestion Financière Unifiée)
**Remplace :** `kondro_treasury`, `kondro_internal_expenses`

**Fonctionnalités :**
- ✅ Comptes de trésorerie (Banque, Caisse, Djamo)
- ✅ Mouvements financiers
- ✅ Dépenses internes avec workflow
- ✅ Dépenses commerciales avec workflow
- ✅ Workflow de paiement unifié
- ✅ Planification des décaissements

### 3. kondro_dashboard (Amélioré)
**Améliore :** `kondro_dashboard` existant

**Fonctionnalités :**
- ✅ Dashboard financier
- ✅ Dashboard commercial
- ✅ Dashboard opérationnel
- ✅ Rapports personnalisés
- ✅ KPIs en temps réel

## 🔄 Mapping des Données

### Migration kondro_commercial_dossier → kondro_core
```python
# Ancien modèle
commercial.dossier → kondro.commercial.dossier

# Nouveau modèle unifié
kondro.project (type='commercial')
  + kondro.commercial.dossier (pour documents et suivi)
```

### Migration kondro_it_project → kondro_core
```python
# Ancien modèle
kondro.it.project → kondro.project (type='it')
```

### Migration kondro_audit → kondro_core
```python
# Ancien modèle
audit.project → kondro.project (type='audit')
```

### Migration kondro_treasury → kondro_finance
```python
# Anciens modèles
treasury.account → kondro.treasury.account
treasury.movement → kondro.treasury.movement
```

### Migration kondro_internal_expenses → kondro_finance
```python
# Ancien modèle
expense.request → kondro.expense.request (type='internal')
```

## 📝 Étapes de Migration

### Étape 1 : Préparation
1. Backup complet de la base de données
2. Documentation des workflows existants
3. Identification des dépendances entre modules

### Étape 2 : Création des nouveaux modules
1. Créer `kondro_core` avec modèles unifiés
2. Créer `kondro_finance` avec workflow unifié
3. Améliorer `kondro_dashboard`

### Étape 3 : Migration des données
1. Script de migration pour chaque ancien module
2. Test de migration sur copie de base
3. Validation des données migrées

### Étape 4 : Tests
1. Tests unitaires des nouveaux modèles
2. Tests d'intégration des workflows
3. Tests utilisateurs (UAT)

### Étape 5 : Déploiement
1. Migration en production
2. Formation des utilisateurs
3. Support post-migration

## ⚠️ Points d'Attention

1. **Compatibilité** : Maintenir temporairement les anciens modules en lecture seule
2. **Données historiques** : Préserver toute l'historique lors de la migration
3. **Workflows** : S'assurer que tous les workflows sont fonctionnels
4. **Permissions** : Migrer les règles de sécurité
5. **Rapports** : Adapter les rapports existants aux nouveaux modèles

## 📊 Bénéfices Attendus

- ✅ **-60% de modules** : De 7-8 à 3 modules
- ✅ **Vue CRM unifiée** : Tous les projets dans une interface
- ✅ **Maintenance simplifiée** : Moins de code à maintenir
- ✅ **Performance améliorée** : Moins de requêtes entre modules
- ✅ **Expérience utilisateur** : Interface cohérente et intuitive

