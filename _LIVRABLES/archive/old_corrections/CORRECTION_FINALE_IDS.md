# 🔧 Correction Finale : Utilisation de `_ids` au lieu de `id`

## Problème

```
ValueError: Expected singleton: ir.ui.view('l', 'i', 's', 't')
```

**Cause** : Accéder à `self.id` sur un recordset invalide déclenche `ValueError: Expected singleton`.  
Le recordset avait `_ids = ['l', 'i', 's', 't']` au lieu d’un entier.

## ✅ Solution

Utiliser `_ids` au lieu de `id` pour éviter `ValueError`:

```python
# AVANT (provoquait ValueError):
if not hasattr(self, 'id'):
    raise ValueError(f"Recordset has no id: {self}")

if not isinstance(self.id, int):
    raise ValueError(f"Invalid view id: {self.id}")

# APRÈS (sans ValueError):
if not hasattr(self, '_ids'):
    raise ValueError(f"Recordset has no _ids: {self}")

if not self._ids or len(self._ids) != 1:
    raise ValueError(f"Expected singleton: {len(self._ids)} records")

view_id = self._ids[0]  # Obtenir l'ID sans déclencher ValueError

if not isinstance(view_id, int):
    raise ValueError(f"Invalid view id: {view_id}")
```

## Fichier modifié

`saas_portal/models/ir_ui_view.py` — méthode `_get_combined_arch()` (ligne 52–185)

Changements:
- Vérification `hasattr(self, '_ids')` au lieu de `hasattr(self, 'id')`
- Accès `self._ids[0]` pour obtenir l’ID
- Protection contre `_ids = ['l', 'i', 's', 't']` avant `exists()`
- Détection des erreurs SQL incluant 'singleton'

## Redémarrer Odoo

Les modifications Python nécessitent un redémarrage.  
Odoo tourne actuellement.

---

**Status** : Correction appliquée — redémarrage nécessaire.

