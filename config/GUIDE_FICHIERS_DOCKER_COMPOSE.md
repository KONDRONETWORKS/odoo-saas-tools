# 📚 Guide des Fichiers Docker Compose

## 🎯 Fichier Principal (À Utiliser)

### `docker-compose.simple.yml` ⭐

**C'est le fichier à utiliser pour le développement local.**

- ✅ Configuration complète avec tous les modules
- ✅ Utilise l'image officielle Odoo 18
- ✅ Montage de tous les modules individuellement
- ✅ Configuration optimisée pour le développement

**Usage :**
```bash
docker compose -f config/docker-compose.simple.yml up -d
```

---

## 📋 Autres Fichiers (Référence)

### `docker-compose.yml`

**Ancienne configuration simplifiée** (peut être obsolète)

- Configuration minimale
- Auto-setup via saas.py
- Peut ne pas être à jour

**⚠️ Non recommandé pour l'instant**

---

### `docker-compose.dev.yml`

**Configuration pour développement avec hot reload**

- Mode développement activé (`--dev=all`)
- Hot reload des modules
- Logs détaillés
- 0 workers (mode debug)

**Usage :** Pour développement actif avec rechargement automatique

---

### `docker-compose.prod.yml`

**Configuration pour production**

- Optimisations de performance
- Configuration sécurisée
- Logs structurés
- Workers configurés

**Usage :** Pour déploiement en production

---

### `docker-compose.windows.yml`

**Configuration spécifique Windows**

- Chemins Windows
- Configuration adaptée
- Compatible Windows Server

**Usage :** Uniquement sur Windows

---

## ✅ Recommandation

**Pour le développement quotidien :**

```bash
# Utilisez TOUJOURS ce fichier
docker compose -f config/docker-compose.simple.yml up -d
```

**Ou utilisez le script :**

```bash
./scripts/start_saas.sh start
```

---

## 🔄 Migration

Si vous utilisez un autre fichier, migrez vers `docker-compose.simple.yml` :

1. **Arrêter l'ancien service :**
   ```bash
   docker compose -f config/docker-compose.[ancien].yml down
   ```

2. **Démarrer avec le nouveau :**
   ```bash
   docker compose -f config/docker-compose.simple.yml up -d
   ```

---

## 📝 Résumé

| Fichier | Usage | Recommandé |
|---------|-------|------------|
| `docker-compose.simple.yml` | Développement local | ✅ **OUI** |
| `docker-compose.dev.yml` | Dev avec hot reload | ⚠️ Si besoin |
| `docker-compose.prod.yml` | Production | ⚠️ Pour prod |
| `docker-compose.windows.yml` | Windows uniquement | ⚠️ Si Windows |
| `docker-compose.yml` | Ancien | ❌ Non |

---

**Utilisez `docker-compose.simple.yml` pour simplifier !**

