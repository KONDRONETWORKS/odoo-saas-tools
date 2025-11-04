# 🐳 Guide Docker Compose - Odoo SaaS Tools

Ce dossier contient plusieurs configurations Docker Compose adaptées à différents cas d'usage.

## 📋 Configurations Disponibles

### 1. `docker-compose.yml` - Démarrage Rapide ⚡

**Usage:** Démarrage rapide avec auto-setup complet

```bash
docker-compose up -d
```

**Caractéristiques:**
- ✅ Build depuis Dockerfile local
- ✅ Auto-setup via `saas.py` (portal, server, plan)
- ✅ Configuration minimale
- ✅ Port PostgreSQL: 5433 (évite conflits)
- ✅ Idéal pour: Tests rapides, démo, premier lancement

**Volumes:**
- Modules core uniquement (saas_base, saas_portal, saas_server, saas_client)
- Configuration: `odoo.conf`
- Filestore: `../filestore`

---

### 2. `docker-compose.simple.yml` - Développement Complet 🏗️

**Usage:** Développement avec tous les modules montés individuellement

```bash
docker-compose -f config/docker-compose.simple.yml up -d
```

**Caractéristiques:**
- ✅ Image officielle Odoo 18
- ✅ Tous les modules SaaS montés individuellement (30+ modules)
- ✅ Configuration complète avec workers
- ✅ Healthchecks PostgreSQL et Odoo
- ✅ Logging configuré
- ✅ Idéal pour: Développement complet, tests de modules

**Volumes:**
- Tous les modules SaaS montés individuellement
- Configuration: `odoo.conf`
- Filestore: `../filestore`
- Logs: Volume dédié

---

### 3. `docker-compose.dev.yml` - Développement Hot Reload 🔥

**Usage:** Développement avec rechargement automatique

```bash
docker-compose -f config/docker-compose.dev.yml up
```

**Caractéristiques:**
- ✅ Mode développement (`--dev=all`)
- ✅ Log level: debug
- ✅ Workers désactivés (0) pour développement
- ✅ Tous les modules montés depuis la racine
- ✅ Hot reload activé
- ✅ Idéal pour: Développement actif, debugging

**Volumes:**
- Toute la racine montée: `../:/mnt/extra-addons`
- Modifications en temps réel

---

### 4. `docker-compose.prod.yml` - Production 🚀

**Usage:** Déploiement en production

```bash
docker-compose -f config/docker-compose.prod.yml up -d
```

**Caractéristiques:**
- ✅ Configuration optimisée production
- ✅ Workers configurés (3+)
- ✅ Logging structuré
- ✅ Healthchecks complets
- ✅ Ressources limitées
- ✅ Sécurité renforcée

---

## 🔄 Comparaison Rapide

| Configuration | Image | Modules | Workers | Usage |
|---------------|-------|---------|---------|-------|
| `docker-compose.yml` | Build local | Core (4) | Auto | Démarrage rapide |
| `docker-compose.simple.yml` | Odoo:18 | Tous (30+) | 3 | Développement complet |
| `docker-compose.dev.yml` | Odoo:18 | Tous | 0 | Dev hot reload |
| `docker-compose.prod.yml` | Odoo:18 | Tous | 3+ | Production |

---

## 🚀 Commandes Utiles

### Démarrer
```bash
# Démarrage rapide
docker-compose up -d

# Développement complet
docker-compose -f config/docker-compose.simple.yml up -d

# Développement hot reload
docker-compose -f config/docker-compose.dev.yml up
```

### Arrêter
```bash
docker-compose down
# ou
docker-compose -f config/docker-compose.simple.yml down
```

### Voir les logs
```bash
docker-compose logs -f odoo
docker-compose -f config/docker-compose.simple.yml logs -f odoo
```

### Rebuild
```bash
docker-compose build --no-cache
```

### Nettoyer
```bash
# Supprimer les conteneurs et volumes
docker-compose down -v

# Nettoyer complètement
docker system prune -a --volumes
```

---

## 📊 Ports Utilisés

| Service | Port | Description |
|---------|------|-------------|
| Odoo XML-RPC | 8069 | Interface web Odoo |
| Odoo Longpolling | 8072 | WebSocket pour temps réel |
| PostgreSQL | 5433 | Base de données (évite conflit avec local) |

---

## 🔧 Configuration

### Variables d'Environnement

Toutes les configurations utilisent:
- `POSTGRES_DB=odoo`
- `POSTGRES_USER=odoo`
- `POSTGRES_PASSWORD=odoo`
- `DB_HOST=postgres`
- `DB_PORT=5432`

### Fichier de Configuration

Le fichier `odoo.conf` est monté en lecture seule (`:ro`) dans toutes les configurations.

---

## 🐛 Troubleshooting

### Port déjà utilisé
```bash
# Vérifier les ports
lsof -i :8069
lsof -i :5433

# Tuer les processus
pkill -f odoo
```

### Erreur de connexion PostgreSQL
```bash
# Vérifier le healthcheck
docker-compose ps
docker-compose logs postgres
```

### Modules non trouvés
```bash
# Vérifier les volumes
docker-compose exec odoo ls -la /mnt/extra-addons/
```

### Rebuild nécessaire
```bash
docker-compose build --no-cache odoo
docker-compose up -d
```

---

## 📚 Documentation Complémentaire

- **Dockerfile:** `config/Dockerfile`
- **Configuration Odoo:** `odoo.conf`
- **Script principal:** `saas.py`
- **Documentation complète:** `README.md`

---

**Dernière mise à jour:** 4 Novembre 2025

