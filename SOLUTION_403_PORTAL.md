# 🚨 Solution 403 - Accès Interdit au Portail

## 🔴 Problème

**Erreur :** `403 : Interdit - Vous n'êtes pas autorisé à accéder aux enregistrements 'Client' (saas_portal.client)`

**Route :** `http://localhost:8069/fr/my`

**Cause :** Les utilisateurs portail n'avaient pas de droits d'accès pour lire leurs propres clients SaaS.

---

## ✅ Corrections Appliquées

### **1. Contrôleur Corrigé**

**Fichier :** `saas_portal_portal/controllers/portal.py`

**Changement :** Utilisation de `sudo()` pour accéder aux clients dans `_prepare_portal_layout_values()`

```python
# AVANT
SaasPortalClient = request.env['saas_portal.client']
instance_count = SaasPortalClient.search_count([...])

# APRÈS
SaasPortalClient = request.env['saas_portal.client'].sudo()
instance_count = SaasPortalClient.search_count([...])
```

### **2. Règles d'Accès Ajoutées**

**Fichier :** `saas_portal_portal/security/ir.model.access.csv`

**Ajout :** Permissions de lecture pour :
- `base.group_user` (utilisateurs internes)
- `portal.group_portal` (utilisateurs portail)

### **3. Règles de Record Ajoutées**

**Fichier :** `saas_portal_portal/security/ir.rule.csv`

**Ajout :** Règles pour limiter l'accès uniquement aux clients qui appartiennent au partenaire de l'utilisateur connecté :

```python
[('partner_id', '=', user.partner_id.id)]
```

---

## 🔧 Actions Requises

### **Étape 1 : Mettre à Jour le Module**

```bash
# Arrêter le serveur Odoo si nécessaire
# Puis mettre à jour le module
python3.11 ../odoo/odoo-bin -c odoo.conf --stop-after-init -u saas_portal_portal
```

OU via l'interface :
1. **Settings** → **Apps**
2. Rechercher `saas_portal_portal`
3. Cliquer sur **Upgrade**

### **Étape 2 : Vérifier les Règles de Sécurité**

1. **Settings** → **Technical** → **Security** → **Access Rights**
2. Rechercher `saas_portal.client`
3. Vérifier que les règles suivantes existent :
   - `saas_portal.client.portal` (group_user)
   - `saas_portal.client.portal.portal` (group_portal)

### **Étape 3 : Vérifier les Règles de Record**

1. **Settings** → **Technical** → **Security** → **Record Rules**
2. Rechercher `saas_portal.client`
3. Vérifier que les règles suivantes existent :
   - `saas_portal.client.portal.rule` (group_portal)
   - `saas_portal.client.user.rule` (group_user)

### **Étape 4 : Tester**

1. **Rafraîchir la page** (Ctrl+F5 ou Cmd+Shift+R)
2. Aller sur `http://localhost:8069/fr/my`
3. L'accès devrait maintenant fonctionner ✅

---

## 📋 Structure des Fichiers de Sécurité

```
saas_portal_portal/
├── security/
│   ├── ir.model.access.csv    # Droits d'accès par groupe
│   └── ir.rule.csv             # Règles de record (domaine)
```

### **ir.model.access.csv**

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_saas_client_portal,saas_portal.client.portal,saas_portal.model_saas_portal_client,base.group_user,1,0,0,0
access_saas_client_portal_portal,saas_portal.client.portal.portal,saas_portal.model_saas_portal_client,portal.group_portal,1,0,0,0
```

### **ir.rule.csv**

```csv
id,name,model_id:id,domain_force,groups
rule_saas_client_portal,saas_portal.client.portal.rule,saas_portal.model_saas_portal_client,"[('partner_id', '=', user.partner_id.id)]",portal.group_portal
rule_saas_client_user,saas_portal.client.user.rule,saas_portal.model_saas_portal_client,"[('partner_id', '=', user.partner_id.id)]",base.group_user
```

---

## 🔍 Vérification

### **Via l'Interface**

1. **Settings** → **Technical** → **Security** → **Access Rights**
   - Filtrer par modèle : `saas_portal.client`
   - Vérifier les permissions pour `group_user` et `group_portal`

2. **Settings** → **Technical** → **Security** → **Record Rules**
   - Filtrer par modèle : `saas_portal.client`
   - Vérifier les règles de domaine

### **Via la Base de Données**

```sql
-- Vérifier les règles d'accès
SELECT name, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink
FROM ir_model_access
WHERE model_id = (SELECT id FROM ir_model WHERE model = 'saas_portal.client');

-- Vérifier les règles de record
SELECT name, model_id, domain_force, groups
FROM ir_rule
WHERE model_id = (SELECT id FROM ir_model WHERE model = 'saas_portal.client');
```

---

## ⚠️ Notes Importantes

1. **Sécurité :** Les règles de record garantissent que les utilisateurs ne peuvent voir QUE leurs propres clients (basé sur `partner_id`).

2. **Permissions :** Les utilisateurs portail ont uniquement le droit de **lecture** (`perm_read=1`), pas de modification (`perm_write=0`).

3. **Droits Administrateurs :** Les administrateurs (`base.group_system`) conservent tous les droits via la règle existante dans `saas_portal/security/ir.model.access.csv`.

---

## 🆘 Si le Problème Persiste

1. **Vérifier les logs Odoo :**
   ```bash
   tail -f odoo.log | grep -i "access\|security\|403"
   ```

2. **Vérifier que l'utilisateur a le bon groupe :**
   - L'utilisateur doit être dans `portal.group_portal` ou `base.group_user`

3. **Vérifier que le client est bien associé au partenaire :**
   ```sql
   SELECT id, name, partner_id 
   FROM saas_portal_client 
   WHERE partner_id = <partner_id_utilisateur>;
   ```

4. **Recréer les règles manuellement si nécessaire :**
   - Via l'interface : **Settings** → **Technical** → **Security**

---

**Le problème devrait maintenant être résolu !** 🎉

