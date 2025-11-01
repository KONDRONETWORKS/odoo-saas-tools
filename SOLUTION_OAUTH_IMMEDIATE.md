# 🚨 Solution Immédiate - Problème OAuth odoo.local

## 🔴 Problème

Erreur : `DNS_PROBE_STARTED - odoo.local introuvable`
URL problématique : `http://odoo.local/oauth2/auth?client_id=False&...`

## ✅ Solutions Rapides

### **Solution 1 : Via l'Interface Odoo (RECOMMANDÉ)**

#### **Étape 1 : Configurer le domaine**

1. **Connectez-vous à Odoo** (http://localhost:8069)

2. **Allez dans :**
   ```
   Settings → SaaS Portal → Settings
   ```

3. **Dans la section "Domain" :**
   - Champ `Base SaaS domain` : entrez **`localhost:8069`**
   - Cliquez sur **"Save"** ou **"Apply"**

4. **Les endpoints OAuth sont automatiquement mis à jour !** ✅

#### **Étape 2 : Vérifier et corriger manuellement si nécessaire**

1. **Allez dans :**
   ```
   Settings → Technical → OAuth Applications → Providers
   ```

2. **Trouvez le provider "SaaS"** (il y en a peut-être deux : un pour `saas_client` et un pour `saas_server`)

3. **Pour chaque provider "SaaS" :**
   - Vérifiez `Auth endpoint` : doit être `http://localhost:8069/oauth2/auth`
   - Vérifiez `Validation endpoint` : doit être `http://localhost:8069/oauth2/tokeninfo`
   - Si ce n'est pas le cas, modifiez manuellement
   - Vérifiez que `Client ID` n'est pas vide (si vide, mettez le `database.uuid`)

4. **Sauvegardez**

5. **Activez le provider** si `Enabled` = False

#### **Étape 3 : Rafraîchir et tester**

1. **Rafraîchissez la page** (Ctrl+F5 ou Cmd+Shift+R)

2. **Testez la connexion OAuth :**
   - Allez sur la page de login
   - Cliquez sur "Log in via SaaS Portal"
   - L'URL devrait maintenant être : `http://localhost:8069/oauth2/auth?...`

---

### **Solution 2 : Via la Base de Données (SQL)**

Si vous avez accès à la base de données :

```sql
-- Mettre à jour les endpoints OAuth
UPDATE auth_oauth_provider 
SET 
    auth_endpoint = 'http://localhost:8069/oauth2/auth',
    validation_endpoint = 'http://localhost:8069/oauth2/tokeninfo'
WHERE 
    name = 'SaaS' 
    AND (auth_endpoint LIKE '%odoo.local%' OR auth_endpoint IS NULL);

-- Vérifier le résultat
SELECT name, auth_endpoint, validation_endpoint, client_id, enabled 
FROM auth_oauth_provider 
WHERE name = 'SaaS';
```

---

### **Solution 3 : Via le Script Python**

1. **Activez l'environnement virtuel :**
   ```bash
   source .venv/bin/activate
   ```

2. **Exécutez le script de correction :**
   ```bash
   python3 fix_oauth_endpoints.py --db odoo --domain localhost:8069
   ```

---

## 🔧 Corrections Automatiques Implémentées

✅ **Mise à jour automatique lors du changement de `base_saas_domain`**
   - Fichier : `saas_portal/models/res_config.py`
   - Les endpoints sont mis à jour quand vous changez le domaine dans les paramètres

✅ **Détection automatique au démarrage**
   - Fichier : `saas_portal/models/ir_config_parameter.py`
   - Si `base_saas_domain` est configuré mais les endpoints pointent vers `odoo.local`, ils sont automatiquement corrigés

---

## 🎯 Vérification Rapide

Pour vérifier que tout fonctionne :

1. **Vérifiez les endpoints dans la base :**
   ```sql
   SELECT name, auth_endpoint, validation_endpoint 
   FROM auth_oauth_provider 
   WHERE name = 'SaaS';
   ```

2. **Testez l'endpoint directement :**
   ```bash
   curl http://localhost:8069/oauth2/auth
   ```
   (Ne devrait pas donner d'erreur DNS)

3. **Vérifiez le paramètre `base_saas_domain` :**
   ```sql
   SELECT key, value 
   FROM ir_config_parameter 
   WHERE key = 'saas_portal.base_saas_domain';
   ```

---

## ⚠️ Notes Importantes

1. **client_id=False** : Ce problème peut être causé si le provider OAuth n'a pas de `client_id` configuré. Dans ce cas :
   - Utilisez le `database.uuid` comme `client_id`
   - Ou laissez-le vide, OAuth le générera automatiquement

2. **Provider désactivé** : Par défaut, le provider dans `saas_client` peut être désactivé. Activez-le si nécessaire.

3. **Deux providers** : Il y a deux providers OAuth "SaaS" :
   - `saas_client.saas_oauth_provider` : pour les clients
   - `saas_server.saas_oauth_provider` : pour les serveurs
   
   **Les deux doivent être mis à jour !**

---

## ✅ Après Correction

Une fois corrigé, l'URL OAuth devrait ressembler à :
```
http://localhost:8069/oauth2/auth?response_type=token&client_id=<uuid>&redirect_uri=...
```

Au lieu de :
```
http://odoo.local/oauth2/auth?response_type=token&client_id=False&...
```

---

## 🆘 Si le problème persiste

1. **Vérifiez les logs Odoo :**
   ```bash
   tail -f odoo.log | grep -i oauth
   ```

2. **Vérifiez que les modules sont bien installés :**
   - `saas_client`
   - `saas_server`
   - `saas_portal`
   - `saas_oauth_provider`

3. **Mettez à jour les modules :**
   ```bash
   python3.11 ../odoo/odoo-bin -c odoo.conf --stop-after-init -u saas_portal,saas_client,saas_server
   ```

---

**Le problème devrait maintenant être résolu !** 🎉

