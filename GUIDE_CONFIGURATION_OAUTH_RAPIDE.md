# ⚡ Guide Rapide - Configuration OAuth

## 🎯 Problème : "odoo.local introuvable"

L'erreur `DNS_PROBE_STARTED` signifie que le navigateur ne peut pas résoudre `odoo.local`.

---

## ✅ Solution Immédiate

### **Étape 1 : Configurer le Domaine dans Odoo**

1. **Connectez-vous à Odoo** (http://localhost:8069)

2. **Allez dans les paramètres :**
   ```
   Settings → Technical → Parameters → System Parameters
   ```

   OU directement via :
   ```
   Settings → SaaS Portal → Settings → Domain
   ```

3. **Configurez `Base SaaS domain` :**
   - Pour développement local : `localhost:8069`
   - Pour production : votre domaine (ex: `odoo.example.com`)

4. **Cliquez sur "Save" ou "Apply"**

### **Étape 2 : Mettre à Jour le Provider OAuth**

1. **Allez dans :**
   ```
   Settings → Technical → OAuth Applications → Providers
   ```

2. **Trouvez le provider "SaaS"**

3. **Vérifiez les endpoints :**
   - `Auth endpoint` : devrait être `http://localhost:8069/oauth2/auth`
   - `Validation endpoint` : devrait être `http://localhost:8069/oauth2/tokeninfo`

4. **Si nécessaire, modifiez manuellement :**
   - Auth endpoint : `http://localhost:8069/oauth2/auth`
   - Validation endpoint : `http://localhost:8069/oauth2/tokeninfo`

5. **Sauvegardez**

### **Étape 3 : Activer le Provider**

1. Dans le provider "SaaS", vérifiez que `Enabled` est coché

2. Si le provider n'est pas activé, activez-le

### **Étape 4 : Tester**

1. **Allez sur la page de login** (http://localhost:8069)

2. **Cliquez sur "Log in via SaaS Portal"**

3. **Vous devriez être redirigé vers :** `http://localhost:8069/oauth2/auth?...`

---

## 🔧 Configuration Alternative : Utiliser odoo.local

Si vous préférez utiliser `odoo.local` au lieu de `localhost:8069` :

### **macOS / Linux :**

1. **Ajoutez à `/etc/hosts` :**
   ```bash
   sudo nano /etc/hosts
   ```
   
2. **Ajoutez cette ligne :**
   ```
   127.0.0.1    odoo.local
   ```

3. **Sauvegardez et testez :**
   ```bash
   ping odoo.local
   # Devrait répondre depuis 127.0.0.1
   ```

4. **Dans Odoo :**
   - Configurez `Base SaaS domain` : `odoo.local`
   - Les endpoints seront automatiquement mis à jour

### **Windows :**

1. **Ouvrez en administrateur :**
   ```
   C:\Windows\System32\drivers\etc\hosts
   ```

2. **Ajoutez :**
   ```
   127.0.0.1    odoo.local
   ```

3. **Sauvegardez**

---

## 🚀 Solution Automatique Implémentée

Le système met maintenant **automatiquement à jour** les endpoints OAuth quand vous changez `base_saas_domain` dans les paramètres !

**Fonctionnalités :**
- ✅ Détection automatique du changement
- ✅ Mise à jour des providers `saas_client` et `saas_server`
- ✅ Support `localhost` pour développement
- ✅ Support domaines complets pour production

---

## 📝 Vérification Rapide

Pour vérifier que tout fonctionne :

```bash
# Vérifier que le serveur écoute sur le bon port
netstat -an | grep 8069

# Tester l'endpoint OAuth
curl http://localhost:8069/oauth2/auth
```

---

## ⚠️ Notes Importantes

1. **Après modification :** Rafraîchissez la page (Ctrl+F5 ou Cmd+Shift+R)

2. **Provider désactivé :** Par défaut, le provider dans `saas_client` est désactivé (`enabled=False`). Activez-le si nécessaire.

3. **Deux providers :** Il y a un provider dans `saas_client` (pour clients) et un dans `saas_server` (pour serveur). Les deux sont mis à jour automatiquement.

---

## ✅ Résumé

**Changements appliqués :**
- ✅ Endpoints par défaut : `odoo.local` → `localhost:8069`
- ✅ Mise à jour automatique lors du changement de `base_saas_domain`
- ✅ Support développement et production

**Action requise :**
1. Configurer `Base SaaS domain` dans les paramètres
2. Vérifier/activer le provider OAuth "SaaS"
3. Tester la connexion

Le problème devrait être résolu ! 🎉

