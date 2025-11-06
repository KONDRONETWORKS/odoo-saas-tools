# 🔐 Corriger le Master Password - "Access Denied"

## ⚠️ Problème

Lorsque vous essayez de mettre à jour le Master Password via l'interface web Odoo (`http://localhost:8069/web/database/manager`), vous obtenez l'erreur :

```
Master password update error: Access Denied
```

Même en utilisant `admin` comme ancien et nouveau mot de passe.

---

## 🔍 Cause

Le Master Password dans le conteneur Docker est **hashé** (format pbkdf2-sha512), alors que le fichier `odoo.conf` local contient le mot de passe en **clair** (`admin`).

**Résultat :** Odoo compare le hash avec le mot de passe en clair, ce qui échoue.

---

## ✅ Solution 1 : Réinitialiser le Master Password dans odoo.conf

### Étape 1 : Vérifier le fichier de configuration

Le fichier `odoo.conf` local doit contenir :

```ini
[options]
admin_passwd = admin
```

### Étape 2 : Mettre à jour le fichier

Si le mot de passe est hashé dans `odoo.conf`, remplacez-le par :

```ini
admin_passwd = admin
```

### Étape 3 : Redémarrer Odoo

```bash
docker compose -f config/docker-compose.simple.yml restart
```

### Étape 4 : Tester dans l'interface web

1. Allez sur `http://localhost:8069/web/database/manager`
2. Cliquez sur "Master Password"
3. Ancien mot de passe : `admin`
4. Nouveau mot de passe : `admin` (ou votre nouveau mot de passe)
5. Cliquez sur "Update"

---

## ✅ Solution 2 : Utiliser le script de mise à jour

Un script Python est disponible pour mettre à jour automatiquement le Master Password.

### Utilisation

**Mettre à jour le Master Password :**
```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
python3 scripts/update_master_password.py "admin" --config odoo.conf
```

**Voir le Master Password actuel :**
```bash
python3 scripts/update_master_password.py "dummy" --config odoo.conf --show-current
```

**Avec hashage (recommandé pour production) :**
```bash
python3 scripts/update_master_password.py "votre-nouveau-mot-de-passe" --config odoo.conf --hash
```

### Après la mise à jour

**Redémarrer Odoo :**
```bash
docker compose -f config/docker-compose.simple.yml restart
```

---

## ✅ Solution 3 : Réinitialiser complètement

Si les solutions précédentes ne fonctionnent pas, réinitialisez le Master Password :

### Étape 1 : Modifier odoo.conf

Ouvrez `odoo.conf` et assurez-vous que :

```ini
[options]
admin_passwd = admin
```

### Étape 2 : Redémarrer le conteneur

```bash
docker compose -f config/docker-compose.simple.yml restart
```

### Étape 3 : Vérifier dans le conteneur

```bash
docker exec saas-odoo cat /etc/odoo/odoo.conf | grep admin_passwd
```

Le résultat doit être : `admin_passwd = admin` (en clair)

---

## 🔧 Vérification

### Vérifier le Master Password dans le conteneur

```bash
docker exec saas-odoo cat /etc/odoo/odoo.conf | grep admin_passwd
```

**Résultat attendu :**
```
admin_passwd = admin
```

**Si le résultat est hashé (commence par `$pbkdf2`),** le fichier `odoo.conf` local n'est pas correctement monté ou a été modifié dans le conteneur.

### Vérifier le fichier local

```bash
cat odoo.conf | grep admin_passwd
```

**Résultat attendu :**
```
admin_passwd = admin
```

---

## 🐛 Dépannage

### Problème : Le conteneur utilise toujours un mot de passe hashé

**Solution :** Le fichier `odoo.conf` dans le conteneur est peut-être en lecture seule ou a été modifié.

1. **Vérifier le montage du volume :**
   ```bash
   docker inspect saas-odoo | grep -A 10 "Mounts"
   ```

2. **Vérifier que odoo.conf est monté en lecture-écriture :**
   Dans `docker-compose.simple.yml`, la ligne doit être :
   ```yaml
   - ../odoo.conf:/etc/odoo/odoo.conf:ro
   ```
   
   Changez `:ro` en `:rw` pour permettre l'écriture :
   ```yaml
   - ../odoo.conf:/etc/odoo/odoo.conf:rw
   ```

3. **Redémarrer :**
   ```bash
   docker compose -f config/docker-compose.simple.yml restart
   ```

### Problème : Le script ne trouve pas le fichier

**Solution :** Utilisez le chemin absolu :

```bash
python3 scripts/update_master_password.py "admin" \
  --config /Users/apple/KONDRO/odoo-sass/odoo-saas-tools/odoo.conf
```

### Problème : L'interface web refuse toujours

**Solution :** 

1. Videz le cache du navigateur
2. Utilisez une fenêtre de navigation privée
3. Vérifiez que le serveur a bien redémarré :
   ```bash
   docker logs saas-odoo --tail 50 | grep -i "starting\|ready"
   ```

---

## 📝 Notes Importantes

### Master Password en clair vs hashé

- **En clair** : `admin_passwd = admin` (plus simple pour développement)
- **Hashé** : `admin_passwd = $pbkdf2-sha512$...` (plus sécurisé pour production)

### Pour le développement

Il est recommandé d'utiliser le mot de passe en clair (`admin`) pour faciliter les tests.

### Pour la production

Utilisez un mot de passe fort et hashé :

```bash
python3 scripts/update_master_password.py "VotreMotDePasseSecure123!" \
  --config odoo.conf --hash
```

---

## 🔄 Workflow Recommandé

1. **Vérifier le Master Password actuel :**
   ```bash
   python3 scripts/update_master_password.py "dummy" --config odoo.conf --show-current
   ```

2. **Mettre à jour si nécessaire :**
   ```bash
   python3 scripts/update_master_password.py "admin" --config odoo.conf
   ```

3. **Redémarrer Odoo :**
   ```bash
   docker compose -f config/docker-compose.simple.yml restart
   ```

4. **Tester dans l'interface web :**
   - Allez sur `http://localhost:8069/web/database/manager`
   - Testez la mise à jour du Master Password

---

## ✅ Résumé

**Pour corriger l'erreur "Access Denied" :**

1. ✅ Assurez-vous que `odoo.conf` contient `admin_passwd = admin` (en clair)
2. ✅ Utilisez le script `update_master_password.py` si nécessaire
3. ✅ Redémarrez Odoo après modification
4. ✅ Testez dans l'interface web avec `admin` comme ancien et nouveau mot de passe

**Le Master Password doit être en clair dans `odoo.conf` pour que l'interface web fonctionne correctement.**

