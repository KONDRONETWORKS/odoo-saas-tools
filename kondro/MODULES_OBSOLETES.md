# Modules Obsolètes - Migration

## 📋 Modules Retirés

Les modules suivants ont été retirés du `docker-compose.simple.yml` car ils sont remplacés par la nouvelle architecture simplifiée :

### Modules Remplacés par `kondro_core`
- ❌ `kondro_commercial_dossier` → ✅ `kondro_core` (dossiers commerciaux)
- ❌ `kondro_it_project` → ✅ `kondro_core` (projets IT unifiés)
- ❌ `kondro_audit` → ✅ `kondro_core` (projets audit unifiés)

### Modules Remplacés par `kondro_finance`
- ❌ `kondro_treasury` → ✅ `kondro_finance` (comptes et mouvements)
- ❌ `kondro_internal_expenses` → ✅ `kondro_finance` (dépenses unifiées)

## 🔄 Migration des Données

Si vous avez des données dans les anciens modules, vous devrez les migrer vers les nouveaux modules :

### Migration des Projets
- `kondro.it.project` → `kondro.project` (type='it')
- `audit.project` → `kondro.project` (type='audit')
- `commercial.dossier` → `kondro.commercial.dossier` + `kondro.project` (type='commercial')

### Migration de la Trésorerie
- `treasury.account` → `kondro.treasury.account`
- `treasury.movement` → `kondro.treasury.movement`

### Migration des Dépenses
- `expense.request` → `kondro.expense.request` (type='internal')
- Dépenses commerciales → `kondro.expense.request` (type='commercial')

## 📝 Actions à Effectuer

1. **Vérifier les données existantes** dans les anciens modules
2. **Créer un script de migration** si nécessaire
3. **Tester la migration** sur une copie de la base
4. **Supprimer les anciens modules** du système de fichiers (optionnel)

## ✅ Modules Obsolètes Supprimés

Les modules obsolètes ont été **supprimés** du système de fichiers :

- ✅ `kondro_audit/` - Supprimé
- ✅ `kondro_internal_expenses/` - Supprimé
- ✅ `kondro_it_project/` - Supprimé
- ✅ `kondro_treasury/` - Supprimé
- ✅ `kondro_commercial_dossier/` - Supprimé
- ✅ `kondro_budget_optional/` - Supprimé

**Note :** Si vous aviez des données dans ces modules, assurez-vous d'avoir effectué la migration vers les nouveaux modules avant la suppression.

## ✅ Modules Actifs

- ✅ `kondro_company` - Configuration entreprise
- ✅ `kondro_core` - CRM unifié
- ✅ `kondro_finance` - Gestion financière unifiée
- ✅ `kondro_dashboard` - Tableaux de bord

