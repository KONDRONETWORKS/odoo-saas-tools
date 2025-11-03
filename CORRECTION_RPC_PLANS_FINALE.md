# ✅ Correction Erreur RPC Plans Finale

## 🔧 PROBLEME IDENTIFIE

**Erreur** : `ValueError: Expected singleton: ir.ui.view('l', 'i', 's', 't')`

**Cause racine** : `browse('list')` créant un recordset invalide.

---

## ✅ SOLUTION APPLIQUEE

### Simplification de `ir_ui_view.py`

**Avant** : Surcharge complexe de `_get_combined_arch` avec multiples vérifications.

**Après** : Surcharge simplifiée qui délègue à la méthode parente.

```python
def _get_combined_arch(self):
    """
    Surcharge supprimée - _get_view intercepte déjà les problèmes
    """
    # Déléguer complètement à la méthode parente
    # _get_view() intercepte déjà les chaînes invalides
    return super()._get_combined_arch()
```

**Logique** : `_get_view` intercepte les chaînes invalides avant `browse`, donc `_get_combined_arch` n’a pas besoin d’autres protections.

---

## 🔍 CORRECTIONS MANTENUES

### 1. `_get_view` (lignes 15-50)

Intercepte `view_id` chaîne avant `browse()` :

- `isinstance(view_id, str)` → `view_id = False`
- `view_id not in (int, bool, False, None)` → `view_id = False`
- Mapping 'tree' → 'list'

### 2. `saas_portal_plan.py` (lignes 15-85)

Normalise les vues côté modèle :

- Détecte `(id, type)` ou `(type, id)`
- `view_id` chaîne → `view_id = False`
- Mapping 'tree' → 'list'
- Nettoyage du résultat

---

## 🚀 REDEMARRAGE REQUIS

### Étape 1 : Arrêter Odoo

```bash
# Dans le terminal où Odoo tourne :
Ctrl+C
```

### Étape 2 : Vider le cache

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
rm -rf .odoo_logs odoo.log
```

### Étape 3 : Redémarrer Odoo

```bash
./.venv/bin/python odoo/odoo-bin -c infrastructure/config/odoo.conf --dev=reload
```

### Étape 4 : Mettre à jour le module

1. Ouvrir http://localhost:8069
2. Apps → rechercher `saas_portal`
3. Upgrade

---

## ✅ VERIFICATION

Après le redémarrage :

- [ ] Plans accessibles
- [ ] Création/modification de plan OK
- [ ] Pas d’erreur `Expected singleton`
- [ ] Serveurs, clients accessibles

---

## 📝 FICHIERS MODIFIES

- ✅ `saas_portal/models/ir_ui_view.py` simplifié
- ✅ `saas_portal/models/saas_portal_plan.py` OK
- ✅ `saas_portal_client_web/security/ir.model.access.csv` corrigé

---

**Status** : Prêt pour redémarrage et test.

