# 🚀 Démarrage Rapide avec Docker

## ⚠️ Prérequis : Docker Desktop

Docker doit être installé et en cours d'exécution :

1. Téléchargez Docker Desktop : https://www.docker.com/products/docker-desktop
2. Installez Docker Desktop
3. Vérifiez l'installation : `docker --version`

## 📋 Étapes de Démarrage

### 1. Démarrer les conteneurs Docker

```powershell
# Depuis la racine du projet
docker compose -f config/docker-compose.windows.yml up -d
```

### 2. Vérifier que les services sont prêts

```powershell
# Voir l'état des conteneurs
docker compose -f config/docker-compose.windows.yml ps

# Voir les logs
docker compose -f config/docker-compose.windows.yml logs -f
```

Attendez quelques secondes que PostgreSQL et Odoo soient complètement démarrés.

### 3. Lancer saas.py

```powershell
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Lancer saas.py avec l'option --use-existed-odoo pour utiliser l'Odoo dans Docker
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

## 🎯 Commande Complète en Une Ligne

```powershell
docker compose -f config/docker-compose.windows.yml up -d; Start-Sleep -Seconds 10; .\venv\Scripts\Activate.ps1; python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

## ✅ Vérification

Une fois tout lancé :
- Odoo sera accessible sur : http://localhost:8069
- Identifiants par défaut : admin / admin
- PostgreSQL accessible sur : localhost:5432

## 🛑 Arrêter les services

```powershell
# Arrêter les conteneurs
docker compose -f config/docker-compose.windows.yml down

# Arrêter et supprimer les volumes (⚠️ supprime les données)
docker compose -f config/docker-compose.windows.yml down -v
```

## 🔧 Commandes Utiles

```powershell
# Redémarrer les services
docker compose -f config/docker-compose.windows.yml restart

# Voir les logs en continu
docker compose -f config/docker-compose.windows.yml logs -f odoo
docker compose -f config/docker-compose.windows.yml logs -f postgres

# Accéder au shell d'Odoo
docker exec -it saas-odoo bash

# Accéder à PostgreSQL
docker exec -it saas-postgres psql -U odoo -d odoo
```
