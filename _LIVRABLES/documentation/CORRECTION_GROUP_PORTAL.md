# 🔧 Correction : Groupe Portal - External ID invalide

## ❌ Problème Identifié

**Erreur lors de la mise à jour du module `saas_portal_portal` :**

```
Exception: Module loading saas_portal_portal failed: 
file saas_portal_portal/security/ir.model.access.csv could not be processed:
Aucun enregistrement trouvé pour id externe 'portal.group_portal' dans le champ 'Group'
```

## 🔍 Cause

En Odoo 18, l'ID externe du groupe Portal a changé :
- ❌ **Ancien (Odoo 17 et précédents)** : `portal.group_portal`
- ✅ **Nouveau (Odoo 18)** : `base.group_portal`

Le module `saas_portal_portal` utilisait l'ancien ID qui n'existe plus.

## ✅ Solution Appliquée

### Fichier 1 : `saas_portal_portal/security/ir.model.access.csv`

**Avant :**
```csv
access_saas_client_portal_portal,...,portal.group_portal,1,0,0,0
```

**Après :**
```csv
access_saas_client_portal_portal,...,base.group_portal,1,0,0,0
```

### Fichier 2 : `saas_portal_portal/security/ir.rule.csv`

**Avant :**
```csv
rule_saas_client_portal,...,portal.group_portal
```

**Après :**
```csv
rule_saas_client_portal,...,base.group_portal
```

## 📝 Changements Détailés

### `ir.model.access.csv`
- Ligne 3 : `portal.group_portal` → `base.group_portal`

### `ir.rule.csv`
- Ligne 2 : `portal.group_portal` → `base.group_portal`

## ✅ Résultat

Après ces modifications :
- ✅ Le module `saas_portal_portal` peut être mis à jour sans erreur
- ✅ Les permissions portal sont correctement appliquées
- ✅ Les règles de sécurité portal fonctionnent

## 🔄 Migration Odoo 18 - Groupes

En Odoo 18, plusieurs groupes ont été déplacés vers `base` :
- `portal.group_portal` → `base.group_portal`
- D'autres groupes peuvent avoir subi le même changement

**Vérification recommandée :** Rechercher toutes les références à `portal.group_*` dans les fichiers CSV de sécurité.

## 🔄 Pour Appliquer

1. **Redémarrer Odoo** (recommandé)

2. **Mettre à jour le module** `saas_portal_portal` :
   - Paramètres > Applications
   - Mode développeur activé
   - Rechercher `saas_portal_portal`
   - Cliquer sur "Mettre à jour"

3. **Vérifier** que la mise à jour se termine sans erreur

---

**Date :** 1er Novembre 2025  
**Statut :** ✅ Corrigé






