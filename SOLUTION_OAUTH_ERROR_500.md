# 🚨 Solution 500 - Erreur OAuth Internal Server Error

## 🔴 Problèmes Identifiés

1. **AttributeError: module 'werkzeug' has no attribute 'url_encode'**
   - Dans `saas_oauth_provider/controllers/main.py` lignes 101 et 106
   - La fonction `werkzeug.url_encode()` n'existe plus dans Odoo 18

2. **client_id=False**
   - Le provider OAuth n'a pas de `client_id` configuré
   - URL : `http://localhost:8069/oauth2/auth?client_id=False&...`

---

## ✅ Corrections Appliquées

### **1. Correction werkzeug.url_encode()**

**Fichiers corrigés :**
- ✅ `saas_oauth_provider/controllers/main.py` → Utilise `urlencode()` depuis `oauthlib.common`
- ✅ `saas_portal/models/saas_portal.py` → Utilise `werkzeug.urls.url_encode()`
- ✅ `saas_client/controllers/main.py` → Utilise `werkzeug.urls.url_encode()`
- ✅ `saas_server/controllers/main.py` → Utilise `werkzeug.urls.url_encode()`
- ✅ `saas_auth_oauth_ip/models.py` → Utilise `urllib.parse.urlencode()`

### **2. Problème client_id=False**

Le `client_id=False` indique que le provider OAuth n'a pas de `client_id` configuré. 

**Solutions possibles :**

#### **Solution A : Initialiser via l'interface**

1. **Settings** → **Technical** → **OAuth Applications** → **Providers**
2. Trouvez le provider "SaaS" (`saas_client.saas_oauth_provider`)
3. Vérifiez que le champ `Client ID` n'est pas vide
4. Si vide :
   - Utilisez le `database.uuid` comme client_id
   - OU créez un UUID : `uuidgen` (macOS/Linux) ou générez-en un
   - Enregistrez

#### **Solution B : Script d'initialisation**

Le module `saas_client` a déjà un mécanisme d'initialisation dans `models/ir_configparameter.py` :

```python
oauth_oe = self.env.ref('saas_client.saas_oauth_provider')
dbuuid = self.sudo().get_param('database.uuid')
oauth_oe.write({'client_id': dbuuid})
```

**Pour forcer l'initialisation :**

1. Allez dans **Settings** → **Technical** → **Parameters** → **System Parameters**
2. Cherchez `database.uuid`
3. Copiez la valeur
4. Allez dans **Settings** → **Technical** → **OAuth Applications** → **Providers**
5. Trouvez "SaaS" et collez l'UUID dans `Client ID`
6. Sauvegardez

#### **Solution C : Script Python**

Créez un script pour initialiser automatiquement :

```python
# Dans Odoo shell ou script externe
env = request.env
provider = env.ref('saas_client.saas_oauth_provider', raise_if_not_found=False)
if provider and not provider.client_id:
    dbuuid = env['ir.config_parameter'].sudo().get_param('database.uuid')
    if dbuuid:
        provider.sudo().write({'client_id': dbuuid})
```

---

## 🔧 Actions Requises

### **Étape 1 : Mettre à Jour les Modules**

```bash
python3.11 ../odoo/odoo-bin -c odoo.conf --stop-after-init -u saas_oauth_provider,saas_portal,saas_client,saas_server
```

### **Étape 2 : Initialiser le Client ID**

**Via l'interface (recommandé) :**

1. **Settings** → **Technical** → **OAuth Applications** → **Providers**
2. Provider "SaaS" → Vérifier/Configurer `Client ID`
3. Si vide, utiliser `database.uuid` ou générer un UUID
4. Sauvegarder

**Via SQL (alternative) :**

```sql
-- Obtenir database.uuid
SELECT value FROM ir_config_parameter WHERE key = 'database.uuid';

-- Mettre à jour le provider (remplacer UUID par la valeur ci-dessus)
UPDATE auth_oauth_provider 
SET client_id = '<UUID>' 
WHERE id = (SELECT res_id FROM ir_model_data WHERE module = 'saas_client' AND name = 'saas_oauth_provider');
```

### **Étape 3 : Vérifier**

1. **Rafraîchir la page** (Ctrl+F5)
2. Tester la connexion OAuth
3. L'URL devrait maintenant avoir un vrai `client_id` : `http://localhost:8069/oauth2/auth?client_id=<uuid>&...`

---

## 📋 Vérification

### **Vérifier les Providers OAuth**

```sql
SELECT id, name, auth_endpoint, client_id, enabled
FROM auth_oauth_provider
WHERE name = 'SaaS';
```

Le `client_id` ne doit **PAS** être `False` ou vide.

### **Vérifier database.uuid**

```sql
SELECT key, value 
FROM ir_config_parameter 
WHERE key = 'database.uuid';
```

---

## ⚠️ Notes Importantes

1. **Client ID Unique :** Chaque provider doit avoir un `client_id` unique. Ne pas utiliser le même pour plusieurs providers.

2. **Format UUID :** Le `client_id` peut être un UUID (format : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`) ou toute autre chaîne unique.

3. **Provider désactivé :** Vérifiez que le provider est activé (`enabled=True`) pour fonctionner.

4. **Deux providers :** Il y a généralement deux providers "SaaS" :
   - `saas_client.saas_oauth_provider` (pour clients)
   - `saas_server.saas_oauth_provider` (pour serveurs)
   
   Les deux doivent avoir un `client_id` configuré.

---

## 🆘 Si le Problème Persiste

1. **Vérifier les logs :**
   ```bash
   tail -f odoo.log | grep -i "oauth\|error\|traceback"
   ```

2. **Vérifier que les modules sont installés :**
   - `saas_oauth_provider`
   - `auth_oauth`
   - `saas_client`
   - `saas_server`

3. **Vérifier la configuration du provider :**
   - `Auth endpoint` : `http://localhost:8069/oauth2/auth`
   - `Validation endpoint` : `http://localhost:8069/oauth2/tokeninfo`
   - `Client ID` : Non vide
   - `Enabled` : True

---

**Les corrections devraient résoudre l'erreur 500 !** 🎉

