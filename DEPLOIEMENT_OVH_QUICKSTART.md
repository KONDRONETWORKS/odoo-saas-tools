# ⚡ DÉPLOIEMENT OVH - GUIDE EXPRESS

> 🎯 **Objectif**: Déployer Odoo SaaS sur VM Ubuntu 22.04.5 à l'adresse **10.10.10.40**

---

## 🚀 DÉMARRAGE RAPIDE (3 commandes)

### 1️⃣ Sur votre machine locale

```bash
cd /Users/apple/.cursor/worktrees/odoo-saas-tools/eDJSm
bash infrastructure/prepare-deploy.sh
```

### 2️⃣ Transférer vers le serveur

```bash
scp /tmp/odoo-deploy/odoo-saas-deploy-*.tar.gz root@10.10.10.40:/tmp/
```

### 3️⃣ Sur le serveur OVH

```bash
ssh root@10.10.10.40
sudo mkdir -p /opt/odoo-saas && sudo tar -xzf /tmp/odoo-saas-deploy-*.tar.gz -C /opt/odoo-saas
cd /opt/odoo-saas && bash infrastructure/deploy-ovh.sh
```

---

## ✅ Après 5-10 minutes

Votre application sera accessible à :

- 🌐 **HTTP**: http://10.10.10.40
- 🔒 **HTTPS**: https://10.10.10.40
- 🐳 **Direct**: http://10.10.10.40:8069

---

## 🔧 Commandes essentielles

```bash
# Aller dans le projet
cd /opt/odoo-saas

# État des services
bash scripts/maintenance.sh status

# Logs en temps réel
bash scripts/maintenance.sh logs

# Redémarrer
bash scripts/maintenance.sh restart

# Sauvegarde
bash scripts/backup.sh daily

# Santé du système
bash scripts/maintenance.sh health
```

---

## 📁 Fichiers créés

Tous les fichiers nécessaires ont été créés :

### Configuration Docker
- ✅ `config/docker-compose.ovh.yml` - Configuration production
- ✅ `config/nginx.ovh.conf` - Configuration Nginx avec SSL
- ✅ `config/Dockerfile` - Image Odoo optimisée
- ✅ `config/docker-entrypoint.sh` - Script de démarrage
- ✅ `config/env.template` - Template des variables d'environnement

### Scripts de déploiement
- ✅ `infrastructure/deploy-ovh.sh` - Script d'installation automatique
- ✅ `infrastructure/prepare-deploy.sh` - Préparation des fichiers
- ✅ `infrastructure/GUIDE_DEPLOIEMENT_OVH.md` - Guide complet

### Scripts de maintenance
- ✅ `scripts/backup.sh` - Sauvegarde automatique
- ✅ `scripts/restore.sh` - Restauration de backup
- ✅ `scripts/maintenance.sh` - Commandes de maintenance

### Documentation
- ✅ `infrastructure/README_DEPLOIEMENT_OVH.md` - README déploiement
- ✅ `DEPLOIEMENT_OVH_QUICKSTART.md` - Ce guide express

---

## 🔐 Sécurité

Le script génère automatiquement :
- 🔑 Mot de passe PostgreSQL sécurisé
- 🔑 Mot de passe Admin Odoo sécurisé
- 🔒 Certificat SSL auto-signé

**⚠️ Sauvegardez les mots de passe affichés en fin de déploiement !**

---

## 💾 Sauvegardes automatiques

Après le déploiement, configurez les backups automatiques :

```bash
crontab -e
```

Ajoutez :

```cron
# Backup quotidien à 2h du matin
0 2 * * * /opt/odoo-saas/scripts/backup.sh daily

# Backup hebdomadaire le dimanche
0 3 * * 0 /opt/odoo-saas/scripts/backup.sh weekly

# Backup mensuel le 1er du mois
0 4 1 * * /opt/odoo-saas/scripts/backup.sh monthly
```

---

## 🆘 Problèmes ?

### Service ne démarre pas
```bash
docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml logs
```

### Vérifier l'état
```bash
docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml ps
```

### Redémarrer tout
```bash
cd /opt/odoo-saas
docker compose -f config/docker-compose.ovh.yml restart
```

---

## 📚 Documentation complète

Pour plus de détails :

- **Guide complet**: `infrastructure/GUIDE_DEPLOIEMENT_OVH.md`
- **README**: `infrastructure/README_DEPLOIEMENT_OVH.md`
- **Logs**: Consultez `/opt/odoo-saas/logs/` sur le serveur

---

## 📊 Architecture déployée

```
┌─────────────────────────────────────────┐
│         Nginx (Port 80/443)             │
│         - Reverse Proxy                 │
│         - SSL/TLS                       │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│         Odoo (Port 8069)                │
│         - Application SaaS              │
│         - Workers: 4                    │
│         - Modules Kondro + SaaS         │
└──────────────┬──────────────────────────┘
               │
┌──────────────┴──────────────────────────┐
│      PostgreSQL 15 (Port 5432)          │
│         - Base de données               │
│         - Backups automatiques          │
└─────────────────────────────────────────┘
```

---

## 🎯 Ce qui est inclus

### Services Docker
- ✅ PostgreSQL 15
- ✅ Odoo 18 avec tous les modules SaaS
- ✅ Nginx avec SSL
- ✅ Service de backup

### Modules Odoo SaaS
- ✅ `saas_base` - Fondation
- ✅ `saas_portal` - Portail SaaS
- ✅ `saas_server` - Serveur SaaS
- ✅ `saas_client` - Client SaaS
- ✅ `kondro_*` - Modules Kondro personnalisés
- ✅ Tous les modules de backup, monitoring, etc.

### Sécurité
- ✅ Firewall UFW configuré
- ✅ Ports sécurisés (80, 443, 22)
- ✅ SSL/TLS activé
- ✅ Proxy mode activé
- ✅ Mots de passe générés aléatoirement

---

## 📞 Support

- **Email**: apps@itexperts4africa.com
- **Documentation locale**: `/opt/odoo-saas/infrastructure/`
- **Logs de déploiement**: `/tmp/odoo-deploy-*.log`

---

## ✅ Checklist finale

Après le déploiement, vérifiez :

- [ ] ✅ Services démarrés (status = running)
- [ ] ✅ Accessible via navigateur
- [ ] ✅ Base de données créée
- [ ] ✅ SSL fonctionne (https://)
- [ ] ✅ Mots de passe sauvegardés
- [ ] ✅ Backups configurés (crontab)
- [ ] ✅ Firewall actif (ufw status)
- [ ] ✅ Monitoring configuré

---

## 🚀 Prêt pour la production ?

Avant la mise en production :

1. **Configurez Let's Encrypt** (certificat SSL valide)
   ```bash
   sudo certbot --nginx -d votre-domaine.com
   ```

2. **Désactivez le port 8069** (accès direct)
   ```bash
   sudo ufw delete allow 8069/tcp
   ```

3. **Configurez les sauvegardes externes** (S3, FTP)
   
4. **Installez le monitoring** (Prometheus, Grafana)

5. **Testez la restauration** des backups

---

**Date de création**: 2024-11-13  
**Version**: 1.0  
**Serveur cible**: 10.10.10.40  
**OS**: Ubuntu 22.04.5 LTS  
**Auteur**: KONDRO Networks

---

> 💡 **Astuce**: Utilisez `prepare-deploy.sh` avant chaque déploiement pour vérifier que tous les fichiers sont à jour !

