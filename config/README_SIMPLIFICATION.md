# 📋 Simplification des Fichiers Docker Compose

## 🎯 Fichier Principal à Utiliser

### `docker-compose.simple.yml` ⭐ **UTILISEZ CELUI-CI**

C'est le fichier principal pour le développement local avec tous les modules.

**Usage :**
```bash
docker compose -f config/docker-compose.simple.yml up -d
```

**Ou utilisez le script :**
```bash
./scripts/start_saas.sh start
```

---

## 📁 Autres Fichiers (Cas Spécifiques)

Ces fichiers sont conservés pour des cas d'usage spécifiques mais **ne sont pas nécessaires** pour le développement quotidien :

| Fichier | Usage | Nécessaire ? |
|---------|-------|--------------|
| `docker-compose.simple.yml` | **Développement local** | ✅ **OUI - Principal** |
| `docker-compose.dev.yml` | Dev avec hot reload | ⚠️ Optionnel |
| `docker-compose.prod.yml` | Production | ⚠️ Pour prod uniquement |
| `docker-compose.windows.yml` | Windows | ⚠️ Si Windows |
| `docker-compose.ubuntu-vm.yml` | Ubuntu VM | ⚠️ Pour déploiement VM |

---

## ✅ Recommandation

**Pour éviter les confusions, utilisez TOUJOURS :**

```bash
# Option 1 : Via le script (recommandé)
./scripts/start_saas.sh start

# Option 2 : Directement
docker compose -f config/docker-compose.simple.yml up -d
```

---

## 🔄 Si vous voulez simplifier davantage

Vous pouvez :
1. **Garder uniquement** `docker-compose.simple.yml`
2. **Archiver** les autres fichiers dans `config/archive/` si vous ne les utilisez pas
3. **Renommer** `docker-compose.simple.yml` en `docker-compose.yml` pour usage par défaut

---

**Dernière mise à jour :** Novembre 2025

