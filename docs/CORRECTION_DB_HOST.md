# Correction du Problème de Connexion à la Base de Données

## Problème Identifié

Le conteneur Odoo essayait de se connecter à `localhost` au lieu de `postgres` (nom du service Docker), ce qui causait l'erreur :
```
Database connection failure: connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

## Solutions Appliquées

### 1. Création de `odoo.conf.docker`
Un fichier de configuration spécifique pour Docker a été créé avec `db_host = postgres` au lieu de `db_host = localhost`.

### 2. Modification de `docker-compose.simple.yml`
- Suppression de l'avertissement `version` (obsolète dans Docker Compose v2+)
- Montage de `odoo.conf.docker` au lieu de `odoo.conf`
- Configuration en lecture seule (`:ro`) pour éviter les modifications accidentelles

### 3. Variables d'Environnement
Les variables d'environnement suivantes sont configurées :
- `HOST=postgres`
- `DB_HOST=postgres`
- `USER=odoo`
- `PASSWORD=odoo`

## État Actuel

✅ **Problème de connexion résolu** : Odoo se connecte maintenant correctement à PostgreSQL via le réseau Docker.

⚠️ **Problème restant** : La base de données `odoo` existe mais n'est pas initialisée avec les tables Odoo.

## Solution pour Initialiser la Base de Données

### Option 1 : Via l'Interface Web (Recommandé)
1. Accéder à `http://localhost:8069/web/database/manager`
2. Créer une nouvelle base de données :
   - **Master Password**: `admin`
   - **Database Name**: `odoo`
   - **Language**: Français
   - **Country**: France
   - **Demo data**: No
   - **Email**: (votre email)
   - **Password**: (votre mot de passe admin)

### Option 2 : Via la Ligne de Commande
```bash
# Arrêter le conteneur Odoo
docker compose -f config/docker-compose.simple.yml stop saas-odoo-dev

# Initialiser la base de données
docker run --rm --network saas_network_dev \
  -v $(pwd):/mnt/extra-addons \
  odoo:18 odoo -d odoo -i base --stop-after-init \
  --db_host=postgres --db_user=odoo --db_password=odoo \
  --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons

# Redémarrer le conteneur
docker compose -f config/docker-compose.simple.yml start saas-odoo-dev
```

## Fichiers Modifiés

- `config/docker-compose.simple.yml` : Suppression de `version`, montage de `odoo.conf.docker`
- `odoo.conf.docker` : Nouveau fichier avec `db_host = postgres`

## Vérification

Pour vérifier que tout fonctionne :
```bash
# Vérifier les conteneurs
docker ps | grep saas

# Vérifier les logs
docker logs saas-odoo-dev --tail 50

# Tester l'accès
curl -s -o /dev/null -w "%{http_code}" http://localhost:8069
```

