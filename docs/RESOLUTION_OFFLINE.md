# Résolution du Problème "You are offline" dans Odoo

## 🔍 Diagnostic

Le message "You are offline" dans Odoo peut apparaître pour plusieurs raisons :

### Causes Possibles

1. **Conteneur en cours de démarrage** : Odoo n'a pas encore terminé son initialisation
2. **Cache du navigateur** : Le navigateur a mis en cache une ancienne version
3. **Service Worker** : Odoo utilise un service worker qui peut être obsolète
4. **Problème de réseau** : Connexion entre le navigateur et le conteneur

## ✅ Solutions

### 1. Vérifier l'état du conteneur

```bash
docker compose -f config/docker-compose.simple.yml ps
```

Le conteneur doit être en statut **"healthy"** ou **"Up"**.

### 2. Vider le cache du navigateur

**Chrome/Edge :**
- Appuyez sur `Ctrl+Shift+Delete` (Windows/Linux) ou `Cmd+Shift+Delete` (Mac)
- Sélectionnez "Images et fichiers en cache"
- Cliquez sur "Effacer les données"

**Firefox :**
- Appuyez sur `Ctrl+Shift+Delete` (Windows/Linux) ou `Cmd+Shift+Delete` (Mac)
- Sélectionnez "Cache"
- Cliquez sur "Effacer maintenant"

### 3. Hard Refresh (Rechargement forcé)

- **Windows/Linux** : `Ctrl+Shift+R` ou `Ctrl+F5`
- **Mac** : `Cmd+Shift+R`

### 4. Désactiver le Service Worker

1. Ouvrez les outils de développement (F12)
2. Allez dans l'onglet "Application" (Chrome) ou "Stockage" (Firefox)
3. Cliquez sur "Service Workers"
4. Cliquez sur "Unregister" pour désactiver le service worker
5. Rechargez la page

### 5. Mode Navigation Privée

Testez dans une fenêtre de navigation privée pour éviter les problèmes de cache.

### 6. Redémarrer le conteneur

Si le problème persiste :

```bash
# Arrêter
docker compose -f config/docker-compose.simple.yml stop odoo

# Redémarrer
docker compose -f config/docker-compose.simple.yml start odoo

# Ou recréer complètement
docker compose -f config/docker-compose.simple.yml up -d odoo
```

### 7. Vérifier les logs

```bash
docker compose -f config/docker-compose.simple.yml logs odoo --tail 50
```

Cherchez les erreurs ou warnings.

## 🔧 Commande Rapide

Pour redémarrer proprement Odoo :

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml restart odoo
sleep 30
# Puis vider le cache du navigateur et recharger
```

## 📝 Note

Le message "You are offline" est souvent un problème côté client (navigateur) plutôt que côté serveur. Si le conteneur est "healthy" et répond aux requêtes HTTP, le problème vient généralement du cache du navigateur.

