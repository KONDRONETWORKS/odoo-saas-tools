# Déploiement SaaS sur OVH

## 📋 Vue d'Ensemble

Ce guide décrit la configuration et le déploiement de votre SaaS Odoo sur un serveur dédié OVH.

## 🔧 Modules OVH Disponibles

### 1. saas_sysadmin_ovh
**Configuration des identifiants OVH API**

- Application Key / Secret / Consumer Key
- Endpoint OVH (ovh-eu, ovh-ca, etc.)
- Domaine racine pour les sous-domaines clients

**Configuration :**
- Paramètres > SaaS Server > OVH Configuration
- Renseigner les credentials OVH obtenus depuis l'espace client OVH

### 2. saas_sysadmin_ovh_route53
**Gestion automatique des DNS OVH**

- Création automatique des enregistrements DNS lors de la création d'instances
- Mise à jour DNS lors des changements
- Suppression DNS lors de la suppression d'instances

**Configuration :**
1. Créer une zone DNS dans OVH (via interface OVH ou module)
2. Associer la zone au serveur SaaS dans `saas_portal.server`
3. Les DNS seront créés automatiquement

### 3. saas_server_backup_ovh
**Sauvegarde vers OVH Object Storage**

- Configuration du projet Public Cloud OVH
- Région et container Object Storage
- Sauvegarde automatique des bases et filestores

**Configuration :**
- Paramètres > SaaS Server > Backup Settings
- Renseigner Project ID, Région, Container

## 🚀 Installation

### Étape 1 : Prérequis Serveur OVH

**Configuration recommandée :**
- Serveur : GAME-1 ou ADV-2 (32 Go RAM minimum)
- OS : Ubuntu 22.04 LTS
- Stockage : RAID1 NVMe 2×480 Go
- Réseau : IP publique fixe

**Installation des dépendances :**
```bash
# Mise à jour système
sudo apt update && sudo apt upgrade -y

# Installation Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Installation Docker Compose
sudo apt install docker-compose-plugin

# Installation PostgreSQL (si non Docker)
sudo apt install postgresql postgresql-contrib

# Installation Python et dépendances
sudo apt install python3-pip python3-venv
pip3 install ovh>=1.1.0
```

### Étape 2 : Configuration OVH API

**Créer une application OVH :**
1. Connectez-vous à https://eu.api.ovh.com/createApp/
2. Créez une application avec les permissions :
   - `/domain/zone/*` (pour DNS)
   - `/cloud/project/*/storage/*` (pour Object Storage)
3. Notez l'Application Key et Secret
4. Générez un Consumer Key avec les permissions nécessaires

**Configurer dans Odoo :**
- Paramètres > SaaS Server > OVH Configuration
- Renseigner Application Key, Secret, Consumer Key
- Sélectionner l'endpoint (ovh-eu par défaut)
- Définir le domaine racine (ex: saas.example.com)

### Étape 3 : Configuration DNS

**Créer une zone DNS :**
1. Dans OVH Manager > Domaines > Zone DNS
2. Créer ou sélectionner la zone (ex: example.com)
3. Dans Odoo : SaaS Portal > Configuration > Zones DNS OVH
4. Créer une zone avec le nom du domaine
5. Associer la zone au serveur SaaS

### Étape 4 : Configuration Object Storage

**Créer un container Object Storage :**
1. OVH Manager > Public Cloud > Object Storage
2. Créer un container (ex: saas-backups)
3. Notez la région (GRA, SBG, BHS, etc.)

**Configurer dans Odoo :**
- Paramètres > SaaS Server > Backup Settings
- Renseigner Project ID, Région, Container
- Configurer les credentials OVH pour Object Storage

### Étape 5 : Déploiement

**Cloner le projet :**
```bash
git clone https://github.com/votre-repo/odoo-saas-tools.git
cd odoo-saas-tools
```

**Configurer Docker Compose :**
```bash
# Copier et adapter la configuration
cp config/docker-compose.simple.yml config/docker-compose.ovh.yml
# Modifier les chemins et configurations selon votre environnement
```

**Démarrer les services :**
```bash
docker compose -f config/docker-compose.ovh.yml up -d
```

**Installer les modules OVH :**
1. Se connecter à Odoo
2. Apps > Rechercher "OVH"
3. Installer :
   - SaaS Sysadmin OVH
   - SaaS Sysadmin OVH Route53
   - SaaS Server Backup OVH

## 🔄 Workflow de Création d'Instance

Lorsqu'un client s'inscrit :

1. **Création de la base de données** (saas_server)
2. **Création automatique DNS** (saas_sysadmin_ovh_route53)
   - Enregistrement A créé : `client-001.saas.example.com -> IP_SERVEUR`
3. **Initialisation Odoo** avec modules du plan
4. **Email de bienvenue** avec URL et credentials

## 💾 Sauvegardes Automatiques

**Script de sauvegarde :**
```bash
# Sauvegarder toutes les bases
python3 scripts/backup_ovh_object_storage.py --db odoo --all --config odoo.conf

# Sauvegarder une base spécifique
python3 scripts/backup_ovh_object_storage.py --db odoo --client client-001 --config odoo.conf
```

**Planification cron :**
```bash
# Ajouter au crontab
0 2 * * * /usr/bin/python3 /path/to/scripts/backup_ovh_object_storage.py --db odoo --all --config /path/to/odoo.conf >> /var/log/ovh_backup.log 2>&1
```

## 🔍 Vérification

**Vérifier les DNS créés :**
- OVH Manager > Domaines > Zone DNS > Voir les enregistrements
- Ou via Odoo : SaaS Portal > Configuration > Zones DNS OVH

**Vérifier les sauvegardes :**
- OVH Manager > Public Cloud > Object Storage > Container
- Vérifier la présence des fichiers de sauvegarde

## 🆘 Dépannage

**Erreur "Credentials OVH non configurés" :**
- Vérifier que les modules saas_sysadmin_ovh sont installés
- Vérifier la configuration dans Paramètres > SaaS Server

**Erreur "Zone DNS non trouvée" :**
- Vérifier que la zone existe dans OVH Manager
- Vérifier les permissions de l'application OVH

**Erreur lors de l'upload Object Storage :**
- Vérifier les permissions du Consumer Key
- Vérifier que le container existe
- Vérifier la région configurée

## 📚 Ressources

- Documentation OVH API : https://docs.ovh.com/
- Documentation OVH Object Storage : https://docs.ovh.com/fr/storage/object-storage/
- SDK Python OVH : https://github.com/ovh/python-ovh

