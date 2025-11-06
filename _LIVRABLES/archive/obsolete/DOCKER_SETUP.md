# 🐳 Configuration Docker - Odoo SaaS Tools

## ✅ État Actuel

**Docker est maintenant configuré et fonctionnel !**

### Conteneurs Actifs

- ✅ **saas-postgres** : PostgreSQL 15 (port 5433 sur host)
- ✅ **saas-odoo** : Odoo 18 (ports 8069 et 8072)

### Accès

- **Interface Odoo** : http://localhost:8069
- **PostgreSQL Docker** : localhost:5433 (host) → 5432 (conteneur)
- **PostgreSQL local** : localhost:5432 (inchangé)

---

## 🚀 Commandes Utiles

### Démarrer les conteneurs

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml up -d
```

### Arrêter le serveur

```bash
# Arrêter les conteneurs (recommandé)
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml stop

# Ou arrêter uniquement Odoo
docker stop saas-odoo

# Ou arrêter tous les conteneurs SaaS
docker stop saas-odoo saas-postgres
```

### Redémarrer le serveur

```bash
# Redémarrer tous les conteneurs (recommandé)
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml restart

# Ou redémarrer uniquement Odoo
docker restart saas-odoo

# Ou arrêter puis redémarrer
docker compose -f config/docker-compose.simple.yml stop
docker compose -f config/docker-compose.simple.yml up -d
```

### Vérifier l'état du serveur

```bash
# Vérifier si les conteneurs sont en cours d'exécution
docker ps | grep saas

# Vérifier l'état détaillé
docker compose -f config/docker-compose.simple.yml ps

# Vérifier les logs en temps réel
docker logs saas-odoo -f
```

### Voir les logs

```bash
# Logs Odoo
docker logs saas-odoo -f

# Logs PostgreSQL
docker logs saas-postgres -f

# Logs des deux
docker compose -f config/docker-compose.simple.yml logs -f

# Dernières lignes des logs
docker logs saas-odoo --tail 100
```

### Arrêter et supprimer (sans données)

```bash
docker compose -f config/docker-compose.simple.yml down
```

### Arrêter et supprimer (avec données)

```bash
docker compose -f config/docker-compose.simple.yml down -v
```

---

## 🔄 Commandes Rapides - Arrêt et Redémarrage

### Arrêter le serveur

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml stop
```

### Redémarrer le serveur

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
docker compose -f config/docker-compose.simple.yml restart
```

### Redémarrer après modification de configuration

```bash
# 1. Arrêter
docker compose -f config/docker-compose.simple.yml stop

# 2. Redémarrer
docker compose -f config/docker-compose.simple.yml up -d

# 3. Vérifier les logs
docker logs saas-odoo -f
```

### Arrêter complètement (avec suppression des conteneurs)

```bash
# Arrêter et supprimer les conteneurs (les données sont conservées)
docker compose -f config/docker-compose.simple.yml down

# Pour redémarrer après
docker compose -f config/docker-compose.simple.yml up -d
```

---

## 📝 Utilisation du Script saas.py avec Docker

Une fois Docker démarré, utilisez le script `saas.py` avec l'option `--use-existed-odoo` :

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
python3 saas.py \
  --use-existed-odoo \
  --odoo-config odoo.conf \
  --master-password admin \
  --admin-password admin \
  --portal-create \
  --server-create \
  --plan-create \
  --run
```

### Options importantes

- `--use-existed-odoo` : Utilise l'instance Odoo dans Docker au lieu d'en lancer une nouvelle
- `--master-password admin` : Mot de passe maître pour créer les bases de données
- `--admin-password admin` : Mot de passe admin par défaut

---

## 🔧 Configuration

### Fichier Docker Compose

Le fichier utilisé est : `config/docker-compose.simple.yml`

### Ports

- **8069** : Interface web Odoo
- **8072** : Longpolling Odoo
- **5433** : PostgreSQL (pour éviter conflit avec PostgreSQL local)

### Volumes

Les modules SaaS sont montés depuis le répertoire local vers `/mnt/extra-addons/` dans le conteneur.

Le filestore est monté vers `/var/lib/odoo/filestore`.

---

## ⚠️ Notes Importantes

1. **PostgreSQL local** : Votre PostgreSQL local continue de tourner sur le port 5432. Le PostgreSQL Docker utilise le port 5433.

2. **Dépendance oauthlib** : Installée manuellement dans le conteneur. Pour la rendre permanente, modifiez le Dockerfile.

3. **Bases de données** : Les bases de données créées sont stockées dans le volume Docker `postgres_data`.

4. **Persistance** : Les données sont conservées même après arrêt des conteneurs (grâce aux volumes Docker).

---

## 🐛 Dépannage

### Vérifier l'état des conteneurs

```bash
# Liste des conteneurs SaaS
docker ps | grep saas

# État détaillé
docker compose -f config/docker-compose.simple.yml ps

# Vérifier si le port 8069 est utilisé
lsof -ti:8069
```

### Vérifier les logs d'erreur

```bash
# Erreurs récentes
docker logs saas-odoo 2>&1 | grep -i error | tail -20

# Toutes les erreurs
docker logs saas-odoo 2>&1 | grep -i "error\|exception\|traceback"

# Logs complets
docker logs saas-odoo --tail 200
```

### Accéder au shell du conteneur

```bash
# Shell interactif Odoo
docker exec -it saas-odoo bash

# Shell PostgreSQL
docker exec -it saas-postgres bash

# Exécuter une commande dans le conteneur
docker exec saas-odoo ls -la /mnt/extra-addons/
```

### Redémarrer après une erreur

```bash
# 1. Arrêter
docker compose -f config/docker-compose.simple.yml stop

# 2. Vérifier les logs de l'erreur
docker logs saas-odoo --tail 100

# 3. Redémarrer
docker compose -f config/docker-compose.simple.yml up -d

# 4. Surveiller les logs
docker logs saas-odoo -f
```

### Réinitialiser complètement

```bash
# Arrêter et supprimer
docker compose -f config/docker-compose.simple.yml down -v

# Redémarrer
docker compose -f config/docker-compose.simple.yml up -d

# Réinitialiser la base de données
docker exec saas-odoo odoo -d odoo -i base --stop-after-init --db_host=postgres --db_user=odoo --db_password=odoo
```

---

## 📊 État Actuel

✅ **Docker Desktop** : Démarré  
✅ **PostgreSQL** : Conteneur actif (port 5433)  
✅ **Odoo** : Conteneur actif (ports 8069, 8072)  
✅ **Base de données Odoo** : Initialisée  
✅ **Bases SaaS** : En cours de création  
✅ **Interface web** : Accessible sur http://localhost:8069  

---

**Migration vers Docker réussie ! 🎉**

