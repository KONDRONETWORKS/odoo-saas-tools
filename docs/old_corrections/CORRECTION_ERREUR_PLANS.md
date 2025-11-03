# 🔧 Correction : Erreur RPC lors de l'accès aux Plans

## Problème Identifié

Erreur lors de l'accès à `SaaS > Plans` :
```
psycopg2.errors.InvalidTextRepresentation: invalid input syntax for type integer: "l"
LINE 1: ...id" FROM "ir_ui_view" WHERE "ir_ui_view"."id" IN ('l', 'i', ...
```

**Cause** : La chaîne "list" est utilisée comme ID de vue au lieu d'un ID numérique.

## ✅ Corrections Appliquées

### 1. `saas_portal/models/ir_ui_view.py`

**Méthode `_get_combined_arch`** :
- ✅ Vérification que `self.id` est un entier AVANT d'appeler `exists()`
- ✅ Gestion d'erreurs améliorée avec fallback vers `arch` directe
- ✅ Protection contre les IDs invalides (chaînes, None, etc.)

**Méthode `_get_view`** :
- ✅ Protection supplémentaire contre les chaînes "list" ou "tree" comme view_id
- ✅ Gestion d'erreurs améliorée avec réessai automatique

### 2. `saas_portal/models/saas_portal_plan.py`

**Méthode `get_views`** :
- ✅ Protection supplémentaire contre les chaînes "list" ou "tree" comme view_id
- ✅ Validation stricte du type de view_id avant normalisation

## 🚀 Actions à Effectuer

### 1. Redémarrer Odoo

```bash
# Arrêter Odoo
# Redémarrer Odoo
```

### 2. Vider le Cache

Dans Odoo :
1. Activer le mode développeur
2. Settings > Technical > Database Structure > Views
3. Rechercher les vues avec type='tree' pour `saas_portal.plan`
4. Les convertir en type='list' si nécessaire

### 3. Vérifier les Vues

```python
# Dans la console Odoo
env['ir.ui.view'].search([
    ('model', '=', 'saas_portal.plan'),
    ('type', '=', 'tree')
])
# Supprimer ou convertir ces vues
```

## 🔍 Vérification

Après redémarrage :
1. Accéder à `SaaS > Plans`
2. Vérifier que la liste s'affiche correctement
3. Vérifier que la création fonctionne

## 📝 Notes

- Les corrections sont défensives et interceptent les erreurs avant qu'elles ne se propagent
- Les logs détaillés aideront à identifier d'autres problèmes similaires
- Si le problème persiste, vérifier les vues XML pour s'assurer qu'elles utilisent `type="list"` et non `type="tree"`

---

**Status**: ✅ **Corrections appliquées**

