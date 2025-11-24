# 🎯 DÉPLOIEMENT RAPIDE - VM OVH

## 📋 Informations

- **Serveur**: 10.10.10.40
- **OS**: Ubuntu 22.04.5 LTS
- **Type**: Premier déploiement en production

---

## 🚀 Installation en 3 étapes

### Étape 1️⃣ : Sur votre machine locale

Préparez les fichiers pour le transfert :

```bash
cd /Users/apple/.cursor/worktrees/odoo-saas-tools/eDJSm
bash infrastructure/prepare-deploy.sh
```

Ce script va :
- ✅ Vérifier tous les fichiers nécessaires
- ✅ Rendre les scripts exécutables
- ✅ Créer une archive prête pour le transfert
- ✅ Générer les commandes de déploiement

### Étape 2️⃣ : Transférer vers le serveur

Envoyez l'archive vers votre serveur OVH :

```bash
# L'archive sera dans /tmp/odoo-deploy/
scp /tmp/odoo-deploy/odoo-saas-deploy-*.tar.gz root@10.10.10.40:/tmp/
```

Ou si vous avez un utilisateur non-root :

```bash
scp /tmp/odoo-deploy/odoo-saas-deploy-*.tar.gz votre_user@10.10.10.40:/tmp/
```

### Étape 3️⃣ : Sur le serveur OVH

Connectez-vous et déployez :

```bash
# Connexion SSH
ssh root@10.10.10.40

# Extraction
sudo mkdir -p /opt/odoo-saas
sudo tar -xzf /tmp/odoo-saas-deploy-*.tar.gz -C /opt/odoo-saas

# Déploiement automatique
cd /opt/odoo-saas
bash infrastructure/deploy-ovh.sh
```

Le script va **tout installer automatiquement** :
- ✅ Mise à jour du système
- ✅ Installation de Docker & Docker Compose
- ✅ Configuration du firewall (UFW)
- ✅ Génération des certificats SSL
- ✅ Configuration des variables d'environnement
- ✅ Construction des images Docker
- ✅ Démarrage de tous les services

---

## 🎉 C'est tout !

Après environ **5-10 minutes**, votre Odoo SaaS sera accessible à :

- **HTTP**: http://10.10.10.40
- **HTTPS**: https://10.10.10.40
- **Direct**: http://10.10.10.40:8069

---

## 🔧 Commandes de maintenance

Une fois déployé, utilisez ces commandes :

```bash
# Aller dans le répertoire du projet
cd /opt/odoo-saas

# Voir l'état des services
bash scripts/maintenance.sh status

# Voir les logs
bash scripts/maintenance.sh logs

# Vérifier la santé
bash scripts/maintenance.sh health

# Redémarrer
bash scripts/maintenance.sh restart

# Faire un backup
bash scripts/backup.sh daily
```

---

## 📁 Structure des fichiers sur le serveur

```
/opt/odoo-saas/
├── config/
│   ├── docker-compose.ovh.yml    # Configuration Docker
│   ├── nginx.ovh.conf             # Configuration Nginx
│   ├── Dockerfile                 # Image Odoo personnalisée
│   └── env.template               # Template des variables
├── infrastructure/
│   ├── deploy-ovh.sh              # Script d'installation
│   └── GUIDE_DEPLOIEMENT_OVH.md   # Documentation complète
├── scripts/
│   ├── backup.sh                  # Sauvegarde automatique
│   ├── restore.sh                 # Restauration
│   └── maintenance.sh             # Maintenance générale
├── kondro/                        # Modules Kondro
├── saas_*/                        # Modules SaaS
├── filestore/                     # Fichiers Odoo
├── backups/                       # Sauvegardes
├── logs/                          # Logs
├── ssl/                           # Certificats SSL
└── .env                           # Variables d'environnement (généré)
```

---

## 🔐 Sécurité

### Mots de passe générés automatiquement

Le script `deploy-ovh.sh` génère automatiquement des mots de passe sécurisés pour :
- PostgreSQL
- Admin Odoo

**⚠️ Important**: Sauvegardez ces mots de passe ! Ils s'affichent à la fin du déploiement.

### Configuration SSL

#### Option 1 : Certificat auto-signé (par défaut)

Le script génère un certificat auto-signé pour les tests.

#### Option 2 : Let's Encrypt (recommandé pour la production)

```bash
# Installer Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtenir un certificat (remplacez votre-domaine.com)
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com

# Renouvellement automatique
sudo systemctl enable certbot.timer
```

---

## 💾 Sauvegardes automatiques

Configurez des sauvegardes automatiques avec cron :

```bash
# Éditer le crontab
crontab -e

# Ajouter ces lignes :
# Backup quotidien à 2h du matin
0 2 * * * /opt/odoo-saas/scripts/backup.sh daily

# Backup hebdomadaire le dimanche à 3h
0 3 * * 0 /opt/odoo-saas/scripts/backup.sh weekly

# Backup mensuel le 1er du mois à 4h
0 4 1 * * /opt/odoo-saas/scripts/backup.sh monthly
```

Les sauvegardes seront stockées dans `/opt/odoo-saas/backups/`

---

## 🔍 Dépannage

### Les services ne démarrent pas

```bash
# Vérifier les logs
docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml logs

# Vérifier l'espace disque
df -h

# Vérifier la mémoire
free -h
```

### Impossible d'accéder à Odoo

```bash
# Vérifier que les ports sont ouverts
sudo netstat -tlnp | grep -E '80|443|8069'

# Vérifier le firewall
sudo ufw status

# Vérifier les conteneurs
docker ps -a
```

### Erreur de base de données

```bash
# Se connecter à PostgreSQL
docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml exec postgres psql -U odoo

# Lister les bases
\l

# Quitter
\q
```

---

## 📚 Documentation complète

Pour plus de détails, consultez :

```bash
cat /opt/odoo-saas/infrastructure/GUIDE_DEPLOIEMENT_OVH.md
```

---

## 📞 Support

- **Email**: apps@itexperts4africa.com
- **Documentation**: `/opt/odoo-saas/_LIVRABLES/`
- **Logs**: `/opt/odoo-saas/logs/`

---

## ✅ Checklist post-déploiement

- [ ] Services démarrés (postgres, odoo, nginx)
- [ ] Accès web fonctionnel (http://10.10.10.40)
- [ ] Base de données créée
- [ ] Certificat SSL configuré
- [ ] Sauvegardes automatiques configurées
- [ ] Firewall activé
- [ ] Mots de passe sauvegardés
- [ ] Monitoring en place
- [ ] Documentation consultée

---

**Dernière mise à jour**: 2024-11-13  
**Version**: 1.0  
**Auteur**: KONDRO Networks

