# 🚀 Guide de Déploiement - Ubuntu 22.04.5 VM OVH

Ce guide vous accompagne pour déployer **Odoo SaaS Tools** sur une machine virtuelle Ubuntu 22.04.5.

**VM cible:** 10.10.10.40 (OVH)

---

## 📋 Table des Matières

1. [Prérequis](#prérequis)
2. [Préparation de la VM](#préparation-de-la-vm)
3. [Déploiement Automatique](#déploiement-automatique)
4. [Déploiement Manuel](#déploiement-manuel)
5. [Configuration Post-Déploiement](#configuration-post-déploiement)
6. [Vérification et Tests](#vérification-et-tests)
7. [Dépannage](#dépannage)
8. [Maintenance](#maintenance)

---

## 📦 Prérequis

### Sur votre machine locale

- Accès SSH à la VM (10.10.10.40)
- Clé SSH configurée
- Connaissance de base de Linux/Ubuntu

### Sur la VM

- Ubuntu 22.04.5 LTS installé
- Accès root ou utilisateur avec sudo
- Connexion internet active
- Au moins **4 Go de RAM** (8 Go recommandé)
- Au moins **50 Go d'espace disque** (100 Go recommandé)

### Optionnel

- Un nom de domaine pointant vers l'IP 10.10.10.40 (pour SSL)
- Email valide (pour Let's Encrypt)

---

## 🖥️ Préparation de la VM

### 1. Connexion à la VM

```bash
ssh root@10.10.10.40
# ou
ssh votre-utilisateur@10.10.10.40
```

### 2. Vérification du système

```bash
# Vérifier la version Ubuntu
lsb_release -a

# Vérifier l'espace disque
df -h

# Vérifier la RAM
free -h

# Mettre à jour le système
sudo apt update && sudo apt upgrade -y
```

### 3. Configuration du firewall

Le script de déploiement configurera automatiquement UFW, mais vous pouvez le faire manuellement :

```bash
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 🚀 Déploiement Automatique (Recommandé)

### Option 1: Depuis votre machine locale

```bash
# 1. Transférer le script sur la VM
scp infrastructure/deploy-ubuntu-vm.sh root@10.10.10.40:/root/

# 2. Se connecter à la VM
ssh root@10.10.10.40

# 3. Rendre le script exécutable
chmod +x /root/deploy-ubuntu-vm.sh

# 4. Configurer les variables d'environnement (optionnel)
export DOMAIN_NAME="votre-domaine.com"
export EMAIL="votre-email@example.com"

# 5. Exécuter le script
sudo ./deploy-ubuntu-vm.sh
```

### Option 2: Depuis la VM directement

```bash
# 1. Se connecter à la VM
ssh root@10.10.10.40

# 2. Cloner ou copier le projet
git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git /opt/odoo-saas-tools
# OU transférer le projet depuis votre machine locale

# 3. Aller dans le répertoire
cd /opt/odoo-saas-tools

# 4. Configurer les variables (optionnel)
export DOMAIN_NAME="votre-domaine.com"
export EMAIL="votre-email@example.com"

# 5. Exécuter le script
sudo infrastructure/deploy-ubuntu-vm.sh
```

### Ce que fait le script automatiquement

✅ Mise à jour du système  
✅ Installation de Docker et Docker Compose  
✅ Installation de PostgreSQL, Nginx, Python 3.11  
✅ Configuration du firewall  
✅ Création de l'utilisateur `odoo`  
✅ Configuration de PostgreSQL  
✅ Clonage/copie du projet  
✅ Création du fichier `.env` avec mots de passe sécurisés  
✅ Configuration de Nginx  
✅ Démarrage des services Docker  
✅ Configuration SSL avec Let's Encrypt (si domaine configuré)  

**Durée estimée:** 15-30 minutes selon la connexion internet

---

## 🔧 Déploiement Manuel

Si vous préférez déployer manuellement étape par étape :

### 1. Installation des dépendances

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y \
    curl \
    wget \
    git \
    build-essential \
    python3.11 \
    python3.11-pip \
    python3.11-venv \
    python3.11-dev \
    libpq-dev \
    postgresql-client \
    nginx \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop \
    unzip \
    software-properties-common
```

### 2. Installation de Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install -y docker-compose-plugin
sudo systemctl enable docker
sudo systemctl start docker
```

### 3. Configuration PostgreSQL

```bash
sudo apt install -y postgresql postgresql-contrib

# Générer un mot de passe sécurisé
POSTGRES_PASSWORD=$(openssl rand -hex 32)

# Créer l'utilisateur et la base
sudo -u postgres psql << EOF
CREATE USER odoo WITH PASSWORD '$POSTGRES_PASSWORD';
ALTER USER odoo CREATEDB;
CREATE DATABASE odoo OWNER odoo;
EOF
```

### 4. Préparation du projet

```bash
# Créer le répertoire
sudo mkdir -p /opt/odoo-saas-tools
sudo chown $USER:$USER /opt/odoo-saas-tools

# Cloner ou copier le projet
cd /opt
git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git
# OU copier depuis votre machine locale

cd odoo-saas-tools
```

### 5. Configuration des variables d'environnement

```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer avec vos valeurs
nano .env
```

**Important:** Modifiez au minimum :
- `POSTGRES_PASSWORD` (générez avec `openssl rand -hex 32`)
- `ODOO_ADMIN_PASSWD` (générez avec `openssl rand -hex 32`)
- `DOMAIN_NAME` (votre domaine ou IP)
- `EMAIL` (pour Let's Encrypt)

### 6. Configuration de Nginx

```bash
# Copier la configuration
sudo cp infrastructure/nginx-odoo.conf /etc/nginx/sites-available/odoo-saas

# Modifier le domaine dans le fichier
sudo nano /etc/nginx/sites-available/odoo-saas
# Remplacez `_` par votre domaine dans les lignes `server_name`

# Activer la configuration
sudo ln -s /etc/nginx/sites-available/odoo-saas /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Tester la configuration
sudo nginx -t

# Redémarrer Nginx
sudo systemctl restart nginx
```

### 7. Démarrage des services Docker

```bash
cd /opt/odoo-saas-tools

# Charger les variables d'environnement
set -a
source .env
set +a

# Démarrer les services
docker compose -f config/docker-compose.ubuntu-vm.yml up -d

# Vérifier les logs
docker compose -f config/docker-compose.ubuntu-vm.yml logs -f
```

### 8. Configuration SSL (si domaine configuré)

```bash
sudo certbot --nginx -d votre-domaine.com --non-interactive --agree-tos --email votre-email@example.com

# Redémarrer Nginx
sudo systemctl restart nginx
```

---

## ⚙️ Configuration Post-Déploiement

### 1. Accéder à Odoo

Ouvrez votre navigateur et allez à :
- **HTTP:** `http://10.10.10.40:8069` ou `http://votre-domaine.com`
- **HTTPS:** `https://votre-domaine.com` (si SSL configuré)

### 2. Créer la base de données initiale

1. Connectez-vous à l'interface Odoo
2. Créez une nouvelle base de données
3. Configurez les paramètres de base

### 3. Installer les modules SaaS

Dans Odoo, allez dans **Apps** et installez dans cet ordre :

#### Modules de base (OBLIGATOIRES)

1. `auth_oauth`
2. `auth_oauth_ip`
3. `auth_oauth_check_client_id`
4. `oauth_provider`
5. `saas_base`

#### Modules core (OBLIGATOIRES)

6. `saas_portal`
7. `saas_server`
8. `saas_client`
9. `saas_ocore`
10. `saas_oserver`
11. `saas_oclient`
12. `saas_oconfig`
13. `saas_oadmin`

#### Modules portail (RECOMMANDÉS)

14. `saas_portal_portal`
15. `saas_portal_start`
16. `saas_portal_signup`
17. `saas_portal_templates`

#### Modules optionnels

- `saas_portal_sale` - Ventes
- `saas_portal_sale_online` - Ventes en ligne
- `saas_sysadmin_ovh` - Intégration OVH
- `saas_server_backup_s3` - Sauvegardes S3
- `saas_portal_monitoring` - Monitoring

### 4. Configuration initiale

1. **Paramètres > SaaS Server**
   - Configurez le serveur SaaS
   - Définissez les paramètres de création d'instances

2. **Paramètres > SaaS Portal**
   - Configurez le portail client
   - Définissez les plans disponibles

3. **Paramètres > OVH** (si applicable)
   - Configurez les credentials OVH API
   - Définissez le domaine racine

---

## ✅ Vérification et Tests

### Vérifier les services

```bash
# Vérifier Docker
docker ps

# Vérifier les logs
docker compose -f config/docker-compose.ubuntu-vm.yml logs -f

# Vérifier PostgreSQL
docker exec -it odoo-postgres-prod psql -U odoo -d odoo -c "\l"

# Vérifier Nginx
sudo systemctl status nginx
sudo nginx -t

# Vérifier le firewall
sudo ufw status
```

### Tester l'accès

```bash
# Test HTTP
curl -I http://10.10.10.40:8069

# Test HTTPS (si configuré)
curl -I https://votre-domaine.com

# Test depuis l'extérieur
# Depuis votre machine locale
curl -I http://10.10.10.40:8069
```

### Vérifier les performances

```bash
# Utilisation CPU/RAM
htop

# Espace disque
df -h

# Logs Odoo
docker compose -f config/docker-compose.ubuntu-vm.yml logs odoo --tail=100
```

---

## 🔍 Dépannage

### Problème: Odoo ne démarre pas

```bash
# Vérifier les logs
docker compose -f config/docker-compose.ubuntu-vm.yml logs odoo

# Vérifier la connexion à PostgreSQL
docker exec -it odoo-main-prod psql -h postgres -U odoo -d odoo

# Redémarrer les services
docker compose -f config/docker-compose.ubuntu-vm.yml restart
```

### Problème: Erreur de connexion à la base de données

```bash
# Vérifier que PostgreSQL est démarré
docker ps | grep postgres

# Vérifier les variables d'environnement
cat .env | grep POSTGRES

# Tester la connexion manuellement
docker exec -it odoo-postgres-prod psql -U odoo -d odoo
```

### Problème: Nginx ne fonctionne pas

```bash
# Vérifier la configuration
sudo nginx -t

# Vérifier les logs
sudo tail -f /var/log/nginx/error.log

# Redémarrer Nginx
sudo systemctl restart nginx
```

### Problème: SSL ne fonctionne pas

```bash
# Vérifier le certificat
sudo certbot certificates

# Renouveler le certificat
sudo certbot renew

# Vérifier que le domaine pointe vers l'IP
dig votre-domaine.com
```

### Problème: Port déjà utilisé

```bash
# Vérifier les ports utilisés
sudo netstat -tulpn | grep -E '8069|8072|5432'

# Arrêter les services conflictuels
sudo systemctl stop service-name
```

### Problème: Permissions

```bash
# Vérifier les permissions du répertoire
ls -la /opt/odoo-saas-tools

# Corriger les permissions
sudo chown -R odoo:odoo /opt/odoo-saas-tools
sudo chmod -R 755 /opt/odoo-saas-tools
```

---

## 🔄 Maintenance

### Sauvegardes

```bash
# Sauvegarde de la base de données
docker exec odoo-postgres-prod pg_dump -U odoo odoo > backup_$(date +%Y%m%d).sql

# Sauvegarde du filestore
tar -czf filestore_backup_$(date +%Y%m%d).tar.gz /opt/odoo-saas-tools/filestore
```

### Mise à jour

```bash
cd /opt/odoo-saas-tools

# Sauvegarder d'abord
# ... (voir section sauvegardes)

# Mettre à jour le code
git pull

# Reconstruire les conteneurs
docker compose -f config/docker-compose.ubuntu-vm.yml up -d --build

# Vérifier les logs
docker compose -f config/docker-compose.ubuntu-vm.yml logs -f
```

### Redémarrage des services

```bash
# Redémarrer tous les services
docker compose -f config/docker-compose.ubuntu-vm.yml restart

# Redémarrer un service spécifique
docker compose -f config/docker-compose.ubuntu-vm.yml restart odoo

# Arrêter les services
docker compose -f config/docker-compose.ubuntu-vm.yml down

# Démarrer les services
docker compose -f config/docker-compose.ubuntu-vm.yml up -d
```

### Monitoring

```bash
# Logs en temps réel
docker compose -f config/docker-compose.ubuntu-vm.yml logs -f

# Utilisation des ressources
docker stats

# Espace disque Docker
docker system df
```

---

## 📞 Support

En cas de problème :

1. Consultez les logs : `docker compose logs`
2. Vérifiez la documentation : [README.md](../README.md)
3. Créez une issue sur GitHub
4. Contactez le support : apps@itexperts4africa.com

---

## 📝 Checklist de Déploiement

- [ ] VM Ubuntu 22.04.5 prête
- [ ] Accès SSH configuré
- [ ] Script de déploiement exécuté
- [ ] Services Docker démarrés
- [ ] Nginx configuré et fonctionnel
- [ ] SSL configuré (si domaine disponible)
- [ ] Odoo accessible via navigateur
- [ ] Base de données créée
- [ ] Modules SaaS installés
- [ ] Configuration initiale effectuée
- [ ] Sauvegardes configurées
- [ ] Monitoring en place

---

**Félicitations ! Votre plateforme Odoo SaaS Tools est maintenant déployée ! 🎉**

