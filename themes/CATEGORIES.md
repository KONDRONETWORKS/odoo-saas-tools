# 📂 Catégories des Modules Themes

## 🎯 Catégories Standardisées

Tous les modules themes utilisent des catégories standardisées selon leur type :

### Backend Themes (Thèmes Backend)
**Catégorie : `Themes/Backend`**

Thèmes qui modifient l'interface backend d'Odoo (interface d'administration).

| Module | Catégorie |
|--------|-----------|
| `theme_backend_odoo12` | `Themes/Backend` |
| `theme_hue_backend` | `Themes/Backend` |
| `theme_modern` | `Themes/Backend` |
| `theme_slife_backend` | `Themes/Backend` |
| `theme_ylhc_base` | `Themes/Backend` |
| `theme_diwy` | `Themes/Backend` |

### Website Themes (Thèmes Website)
**Catégorie : `Themes/Website`**

Thèmes qui modifient l'interface frontend/public d'Odoo (site web).

| Module | Catégorie |
|--------|-----------|
| `theme_magic3brothers` | `Themes/Website` |

### eCommerce Themes (Thèmes eCommerce)
**Catégorie : `Themes/eCommerce`**

Thèmes complets pour sites e-commerce avec fonctionnalités avancées.

| Module | Catégorie |
|--------|-----------|
| `theme_crest` | `Themes/eCommerce` |

## 📋 Structure des Catégories

```
Themes/
├── Backend/          ← Thèmes backend (interface admin)
├── Website/          ← Thèmes website (interface publique)
└── eCommerce/        ← Thèmes e-commerce complets
```

## 🔧 Règles de Nommage

1. **Backend Themes** : Tous les thèmes qui modifient l'interface backend utilisent `Themes/Backend`
2. **Website Themes** : Les thèmes pour le site public utilisent `Themes/Website`
3. **eCommerce Themes** : Les thèmes e-commerce complets utilisent `Themes/eCommerce`

## ✅ Vérification

Pour vérifier les catégories de tous les modules :

```bash
cd themes
for dir in theme_*/; do
    echo "=== $(basename "$dir") ==="
    grep "category" "$dir/__manifest__.py" 2>/dev/null || echo "Pas de catégorie"
done
```

## 📝 Notes

- Toutes les catégories commencent par `Themes/` (au pluriel)
- Les sous-catégories sont en PascalCase (Backend, Website, eCommerce)
- Les catégories sont cohérentes avec les standards Odoo

---

**Dernière mise à jour :** Novembre 2025

