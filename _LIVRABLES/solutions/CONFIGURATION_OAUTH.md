# 🔧 Configuration OAuth - Guide de Résolution

## 🐛 Problème Résolu

**Erreur :** `DNS_PROBE_STARTED - odoo.local introuvable` lors de l'utilisation de "SaaS login"

**Cause :** Les endpoints OAuth pointaient vers `odoo.local` qui n'est pas résolu par le DNS local.

---

## ✅ Solutions Appliquées

### **1. Endpoints par Défaut Corrigés**

Les endpoints OAuth utilisent maintenant `localhost:8069` par défaut au lieu de `odoo.local` :

**Fichiers modifiés :**
- ✅ `saas_client/data/auth_oauth_data.xml`
- ✅ `saas_server/data/auth_oauth_data.xml`

**Changements :**
```xml
<!-- AVANT -->
<field name="auth_endpoint">http://odoo.local/oauth2/auth</field>
<field name="validation_endpoint">http://odoo.local/oauth2/tokeninfo</field>

<!-- APRÈS -->
<field name="auth_endpoint">http://localhost:8069/oauth2/auth</field>
<field name="validation_endpoint">http://localhost:8069/oauth2/tokeninfo</field>
```

### **2. Mise à Jour Automatique**

Le module `saas_portal` met maintenant à jour automatiquement les endpoints OAuth quand vous changez le `base_saas_domain` dans les paramètres.

**Fichier modifié :** `saas_portal/models/res_config.py`

**Fonctionnalités :**
- ✅ Détection automatique du changement de domaine
- ✅ Mise à jour des providers `saas_client` et `saas_server`
- ✅ Support de `localhost` pour le développement local
- ✅ Support des domaines complets (ex: `odoo.com`)

---

## 📋 Comment Configurer

### **Pour le Développement Local (localhost)**

1. **Aller dans les paramètres :**
   - Menu : `Settings` → `SaaS Portal` → `Settings`
   - Section : `Domain`

2. **Configurer le domaine :**
   - Dans le champ `Base SaaS domain`, entrer : `localhost:8069`
   - Cliquer sur `Save` ou `Apply`

3. **Vérifier :**
   - Les endpoints OAuth sont automatiquement mis à jour
   - Vous pouvez maintenant utiliser "SaaS login"

### **Pour la Production**

1. **Configurer le domaine :**
   - Dans `Base SaaS domain`, entrer votre domaine (ex: `odoo.example.com`)
   - Les endpoints utiliseront `https://odoo.example.com`

2. **Configuration DNS :**
   - Assurez-vous que votre domaine pointe vers votre serveur
   - Vérifiez les enregistrements DNS A/AAAA

---

## 🔍 Vérification

### **Vérifier la Configuration Actuelle**

1. **Via l'interface :**
   - `Settings` → `Technical` → `OAuth Applications`
   - Vérifier le provider "SaaS"
   - Vérifier les endpoints `auth_endpoint` et `validation_endpoint`

2. **Via la base de données :**
   ```sql
   SELECT name, auth_endpoint, validation_endpoint 
   FROM auth_oauth_provider 
   WHERE name = 'SaaS';
   ```

### **Tester la Connexion**

1. Aller sur la page de login
2. Cliquer sur "Log in via SaaS Portal"
3. Vérifier que la redirection fonctionne vers `localhost:8069/oauth2/auth`

---

## 🛠️ Solutions Alternatives

### **Option 1 : Configuration DNS Locale (macOS/Linux)**

Si vous voulez utiliser `odoo.local`, ajoutez-le à votre fichier hosts :

**macOS/Linux :**
```bash
sudo nano /etc/hosts
# Ajouter cette ligne :
127.0.0.1    odoo.local
```

**Windows :**
```
C:\Windows\System32\drivers\etc\hosts
# Ajouter cette ligne :
127.0.0.1    odoo.local
```

### **Option 2 : Utiliser l'IP Directement**

Vous pouvez aussi utiliser `127.0.0.1:8069` dans `Base SaaS domain`.

---

## ⚙️ Comportement Automatique

Le système détecte automatiquement le type de domaine :

| Domaine Saisi | Endpoint Généré | Usage |
|---------------|-----------------|-------|
| `localhost:8069` | `http://localhost:8069/oauth2/auth` | Développement local |
| `127.0.0.1:8069` | `http://127.0.0.1:8069/oauth2/auth` | Développement local (IP) |
| `odoo.com` | `https://odoo.com/oauth2/auth` | Production |
| `odoo.local` | `http://localhost:8069/oauth2/auth` | Fallback local |

---

## 📝 Notes Importantes

1. **Après changement de domaine :** Les endpoints sont mis à jour automatiquement, mais il faut peut-être rafraîchir la page.

2. **Pour activer le provider :** Assurez-vous que `enabled=True` dans le provider OAuth.

3. **Modules requis :** Les modules `saas_client` et `saas_server` doivent être installés pour que la mise à jour automatique fonctionne.

---

## ✅ Statut

- ✅ Endpoints par défaut corrigés (`localhost:8069`)
- ✅ Mise à jour automatique implémentée
- ✅ Support développement et production
- ✅ Documentation créée

Le problème OAuth devrait maintenant être résolu !

