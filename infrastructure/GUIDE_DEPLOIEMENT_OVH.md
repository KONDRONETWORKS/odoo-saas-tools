# 🚀 Guide de Déploiement - VM Ubuntu 22.04.5 sur OVH

## 📋 Informations de déploiement

- **Serveur**: VM OVH
- **Adresse IP**: 10.10.10.40
- **OS**: Ubuntu 22.04.5 LTS
- **Type**: Premier déploiement en production

---

## 🎯 Prérequis VM

### Configuration minimale recommandée
- **CPU**: 4 vCPUs minimum (8 recommandé)
- **RAM**: 8 GB minimum (16 GB recommandé)
- **Stockage**: 100 GB SSD minimum
- **Réseau**: IP fixe configurée (10.10.10.40)

### Ports nécessaires
- **80**: HTTP (Nginx)
- **443**: HTTPS (Nginx avec SSL)
- **8069**: Odoo (optionnel, pour debug)
- **5432**: PostgreSQL (interne uniquement)
- **22**: SSH (sécurisé)

---

## 🔧 ÉTAPE 1 : Préparation de la VM

### 1.1 Connexion SSH à la VM

```bash
# Depuis votre machine locale
ssh root@10.10.10.40

# Ou avec un utilisateur
ssh votre_user@10.10.10.40
```

### 1.2 Mise à jour du système

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git vim nano ufw net-tools htop
```

### 1.3 Configuration du firewall

```bash
# Activer UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8069/tcp  # Temporaire pour debug
sudo ufw enable
sudo ufw status
```

### 1.4 Créer un utilisateur dédié (recommandé)

```bash
sudo adduser odoo
sudo usermod -aG sudo odoo
sudo su - odoo
```

---

## 🐳 ÉTAPE 2 : Installation Docker & Docker Compose

### 2.1 Installation Docker

```bash
# Supprimer anciennes versions
sudo apt remove docker docker-engine docker.io containerd runc

# Installer les dépendances
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Ajouter la clé GPG Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Ajouter le dépôt Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Installer Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER
newgrp docker

# Vérifier l'installation
docker --version
docker compose version
```

### 2.2 Configuration Docker (optionnel)

```bash
# Créer le fichier de configuration
sudo mkdir -p /etc/docker
sudo nano /etc/docker/daemon.json
```

Ajouter la configuration suivante :

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
```

```bash
# Redémarrer Docker
sudo systemctl restart docker
sudo systemctl enable docker
```

---

## 📦 ÉTAPE 3 : Cloner et configurer le projet

### 3.1 Cloner le repository

```bash
cd /opt
sudo mkdir -p odoo-saas
sudo chown -R $USER:$USER odoo-saas
cd odoo-saas

# Cloner le projet (remplacer par votre URL git)
git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git .

# Ou copier depuis votre machine locale
# scp -r /Users/apple/.cursor/worktrees/odoo-saas-tools/eDJSm/* odoo@10.10.10.40:/opt/odoo-saas/
```

### 3.2 Configuration des variables d'environnement

```bash
cd /opt/odoo-saas
nano .env
```

Ajouter les variables suivantes :

```bash
# Base de données
POSTGRES_PASSWORD=VotreMotDePasseSecurise123!
POSTGRES_DB=odoo_prod
POSTGRES_USER=odoo

# Odoo
ODOO_ADMIN_PASSWD=VotreMotDePasseAdminOdoo123!
ODOO_DB_PASSWORD=VotreMotDePasseSecurise123!

# SMTP (pour les emails)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre.email@gmail.com
SMTP_PASSWORD=VotreMotDePasseEmail

# Domaine
DOMAIN_NAME=votre-domaine.com
```

**⚠️ IMPORTANT**: Changez tous les mots de passe par des valeurs sécurisées !

### 3.3 Créer les répertoires nécessaires

```bash
mkdir -p /opt/odoo-saas/filestore
mkdir -p /opt/odoo-saas/backups
mkdir -p /opt/odoo-saas/logs
mkdir -p /opt/odoo-saas/ssl

# Permissions
chmod -R 755 /opt/odoo-saas/filestore
chmod -R 755 /opt/odoo-saas/backups
chmod -R 755 /opt/odoo-saas/logs
```

---

## 🚀 ÉTAPE 4 : Adapter la configuration Docker pour la production

### 4.1 Créer un docker-compose.ovh.yml

```bash
cd /opt/odoo-saas
nano config/docker-compose.ovh.yml
```

Ce fichier sera créé automatiquement par le script suivant.

### 4.2 Créer la configuration Nginx

```bash
nano config/nginx.ovh.conf
```

Ce fichier sera également créé automatiquement.

---

## 🔐 ÉTAPE 5 : Configuration SSL (HTTPS)

### Option A : Avec Let's Encrypt (domaine public)

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir un certificat SSL
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Renouvellement automatique
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Option B : Certificat auto-signé (pour tests)

```bash
sudo mkdir -p /opt/odoo-saas/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /opt/odoo-saas/ssl/server.key \
  -out /opt/odoo-saas/ssl/server.crt \
  -subj "/C=FR/ST=IDF/L=Paris/O=VotreEntreprise/CN=10.10.10.40"

sudo chmod 600 /opt/odoo-saas/ssl/server.key
sudo chmod 644 /opt/odoo-saas/ssl/server.crt
```

---

## 🎬 ÉTAPE 6 : Lancement de l'application

### 6.1 Construction des images

```bash
cd /opt/odoo-saas

# Build des images Docker
docker compose -f config/docker-compose.ovh.yml build --no-cache
```

### 6.2 Démarrage des services

```bash
# Démarrer tous les services
docker compose -f config/docker-compose.ovh.yml up -d

# Vérifier les logs
docker compose -f config/docker-compose.ovh.yml logs -f

# Vérifier l'état des conteneurs
docker compose -f config/docker-compose.ovh.yml ps
```

### 6.3 Vérification

```bash
# Tester la connexion à Odoo
curl http://10.10.10.40:8069

# Vérifier PostgreSQL
docker compose -f config/docker-compose.ovh.yml exec postgres pg_isready -U odoo

# Vérifier les logs Odoo
docker compose -f config/docker-compose.ovh.yml logs odoo --tail=100
```

---

## 🔍 ÉTAPE 7 : Accès à l'application

### 7.1 Accès web

Ouvrez votre navigateur :
- **HTTP**: http://10.10.10.40
- **HTTPS**: https://10.10.10.40 (si SSL configuré)
- **Direct Odoo**: http://10.10.10.40:8069

### 7.2 Première connexion

1. Créer la première base de données
2. Utilisateur: admin
3. Mot de passe: celui configuré dans `.env` (ODOO_ADMIN_PASSWD)

---

## 🛠️ ÉTAPE 8 : Maintenance et monitoring

### 8.1 Commandes utiles

```bash
# Arrêter les services
docker compose -f config/docker-compose.ovh.yml down

# Redémarrer un service
docker compose -f config/docker-compose.ovh.yml restart odoo

# Voir les logs en temps réel
docker compose -f config/docker-compose.ovh.yml logs -f odoo

# Exécuter une commande dans le conteneur
docker compose -f config/docker-compose.ovh.yml exec odoo bash

# Backup manuel de la base de données
docker compose -f config/docker-compose.ovh.yml exec postgres pg_dump -U odoo odoo_prod > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 8.2 Mise à jour du code

```bash
cd /opt/odoo-saas
git pull origin main
docker compose -f config/docker-compose.ovh.yml down
docker compose -f config/docker-compose.ovh.yml build --no-cache
docker compose -f config/docker-compose.ovh.yml up -d
```

### 8.3 Monitoring

```bash
# Voir l'utilisation des ressources
docker stats

# Espace disque
df -h

# Processus
htop
```

---

## 🔒 ÉTAPE 9 : Sécurisation

### 9.1 Désactiver l'accès direct au port 8069

```bash
sudo ufw delete allow 8069/tcp
```

### 9.2 Configurer fail2ban (anti brute-force)

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 9.3 Sauvegardes automatiques

Créer un script de backup automatique (voir `/opt/odoo-saas/scripts/backup.sh`)

```bash
# Ajouter au crontab
crontab -e

# Backup quotidien à 2h du matin
0 2 * * * /opt/odoo-saas/scripts/backup.sh
```

---

## 📊 ÉTAPE 10 : Vérification finale

### Checklist de déploiement

- [ ] Docker et Docker Compose installés
- [ ] Firewall configuré (UFW)
- [ ] Variables d'environnement configurées (.env)
- [ ] SSL/TLS configuré (Let's Encrypt ou auto-signé)
- [ ] Services démarrés (Postgres, Odoo, Nginx)
- [ ] Accès web fonctionnel
- [ ] Base de données créée et accessible
- [ ] Backups configurés
- [ ] Monitoring en place
- [ ] Logs accessibles
- [ ] Documentation à jour

---

## 🆘 Dépannage

### Problème : Les conteneurs ne démarrent pas

```bash
# Voir les logs détaillés
docker compose -f config/docker-compose.ovh.yml logs

# Vérifier les ressources
docker system df
free -h
```

### Problème : Impossible d'accéder à Odoo

```bash
# Vérifier que les ports sont ouverts
sudo netstat -tlnp | grep -E '80|443|8069'

# Vérifier le firewall
sudo ufw status

# Vérifier les conteneurs
docker ps -a
```

### Problème : Erreur de base de données

```bash
# Se connecter à PostgreSQL
docker compose -f config/docker-compose.ovh.yml exec postgres psql -U odoo

# Lister les bases
\l

# Se connecter à la base
\c odoo_prod

# Quitter
\q
```

---

## 📞 Support

Pour toute question ou problème :
- Email: apps@itexperts4africa.com
- Documentation: voir `/opt/odoo-saas/_LIVRABLES/`
- Issues GitHub: https://github.com/KONDRONETWORKS/odoo-saas-tools/issues

---

## 📝 Notes importantes

1. **Sauvegardes**: Configurez des sauvegardes automatiques dès le premier jour
2. **Monitoring**: Installez un système de monitoring (Prometheus, Grafana)
3. **Logs**: Vérifiez régulièrement les logs pour détecter les problèmes
4. **Mises à jour**: Planifiez des maintenances régulières
5. **Sécurité**: Changez tous les mots de passe par défaut
6. **SSL**: Utilisez toujours HTTPS en production

---

**Date de création**: 2024-11-13  
**Version**: 1.0  
**Auteur**: KONDRO Networks

