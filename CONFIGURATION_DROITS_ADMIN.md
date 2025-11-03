# 👥 Configuration des Droits Utilisateurs Admin

## 📋 Objectif

Donner tous les droits au groupe/administrateur [admin, admin].

## ✅ Solution Appliquée

**Fichier créé** : `saas_portal/security/groups.xml`

### 1. Groupe SaaS Manager

Création d'un nouveau groupe `group_saas_manager` avec tous les droits SaaS :
```xml
<record id="group_saas_manager" model="res.groups">
    <field name="name">SaaS Manager</field>
    <field name="comment">Accès complet à toutes les fonctionnalités SaaS (plans, serveurs, clients)</field>
    <field name="users" eval="[(4, ref('base.user_root'))]" />
</record>
```

### 2. Droits Administrateur

L'utilisateur `admin` (`base.user_root`) est automatiquement ajouté à :
- ✅ `base.group_user` - Utilisateur standard
- ✅ `base.group_system` - Droits système complets
- ✅ `base.group_admin` - Administration complète

### 3. Intégration dans le Manifest

Le fichier `groups.xml` a été ajouté au manifest de `saas_portal` :
```python
'data': [
    # ... autres fichiers ...
    'security/groups.xml',
    'security/ir.model.access.csv',
],
```

## 🚀 Activation

### Option 1 : Redémarrer Odoo (Recommandé)
```bash
# Arrêter Odoo (Ctrl+C)
# Redémarrer :
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
./.venv/bin/python odoo/odoo-bin -c infrastructure/config/odoo.conf --dev=reload
```

### Option 2 : Mise à jour module
1. Ouvrir Odoo : http://localhost:8069
2. Settings > Apps
3. Rechercher `saas_portal`
4. Cliquer "Upgrade"

## 🎯 Résultat

Après redémarrage :
1. ✅ L'utilisateur admin a tous les droits systèmes
2. ✅ Le groupe SaaS Manager existe
3. ✅ L'admin appartient au groupe SaaS Manager
4. ✅ Création/modification/suppression autorisées sur tous les modèles SaaS

## 🔍 Vérification

Après redémarrage, vérifier :
1. Ouvrir Odoo et se connecter avec [admin, admin]
2. Settings > Users & Companies > Groups
3. Rechercher "SaaS Manager"
4. Vérifier que l'admin y appartient
5. Tester la création d'un serveur/client

---

**Status** : ✅ **Configuration prête**

**Prochaine étape** : Redémarrer Odoo

