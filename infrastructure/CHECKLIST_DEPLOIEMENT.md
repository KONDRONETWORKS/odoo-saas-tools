# ✅ CHECKLIST DE DÉPLOIEMENT - VM OVH

**Serveur**: 10.10.10.40  
**OS**: Ubuntu 22.04.5 LTS  
**Date**: _______________  
**Responsable**: _______________

---

## 📋 PHASE 1 : PRÉPARATION (Machine locale)

### Vérification des fichiers

- [ ] Tous les fichiers du projet sont à jour
- [ ] Le dépôt Git est propre (git status)
- [ ] Les modules Kondro sont présents
- [ ] Les modules SaaS sont présents
- [ ] Les fichiers de configuration existent

### Exécution du script de préparation

```bash
cd /Users/apple/.cursor/worktrees/odoo-saas-tools/eDJSm
bash infrastructure/prepare-deploy.sh
```

- [ ] Script exécuté sans erreur
- [ ] Archive créée dans `/tmp/odoo-deploy/`
- [ ] Taille de l'archive: _______________ MB
- [ ] Fichier COMMANDES_DEPLOIEMENT.txt créé

---

## 📋 PHASE 2 : TRANSFERT VERS LE SERVEUR

### Connexion au serveur

- [ ] Connexion SSH fonctionnelle: `ssh root@10.10.10.40`
- [ ] Accès root ou sudo disponible
- [ ] Espace disque suffisant (>= 100 GB)

### Transfert de l'archive

```bash
scp /tmp/odoo-deploy/odoo-saas-deploy-*.tar.gz root@10.10.10.40:/tmp/
```

- [ ] Transfert réussi
- [ ] Archive présente sur le serveur
- [ ] Intégrité vérifiée (taille identique)

---

## 📋 PHASE 3 : INSTALLATION SUR LE SERVEUR

### Extraction de l'archive

```bash
ssh root@10.10.10.40
sudo mkdir -p /opt/odoo-saas
sudo tar -xzf /tmp/odoo-saas-deploy-*.tar.gz -C /opt/odoo-saas
```

- [ ] Extraction réussie
- [ ] Fichiers présents dans `/opt/odoo-saas/`
- [ ] Permissions correctes

### Lancement du script d'installation

```bash
cd /opt/odoo-saas
bash infrastructure/deploy-ovh.sh
```

- [ ] Mise à jour du système terminée
- [ ] Firewall UFW configuré
- [ ] Docker installé: Version _____________
- [ ] Docker Compose installé: Version _____________
- [ ] Répertoires créés (filestore, backups, logs, ssl)
- [ ] Fichier .env créé avec mots de passe sécurisés
- [ ] Certificat SSL généré
- [ ] Images Docker construites
- [ ] Services démarrés

#### Mots de passe à sauvegarder

- **PostgreSQL**: _________________________________
- **Admin Odoo**: _________________________________

⚠️ **IMPORTANT**: Conservez ces mots de passe dans un coffre-fort sécurisé !

---

## 📋 PHASE 4 : VÉRIFICATION POST-DÉPLOIEMENT

### Vérification des services Docker

```bash
docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml ps
```

- [ ] Service `postgres` : RUNNING
- [ ] Service `odoo` : RUNNING
- [ ] Service `nginx` : RUNNING
- [ ] Service `backup` : CREATED

### Vérification de la santé des services

```bash
cd /opt/odoo-saas
bash scripts/maintenance.sh health
```

- [ ] PostgreSQL répond (pg_isready OK)
- [ ] Odoo répond sur le port 8069
- [ ] Nginx répond sur le port 80
- [ ] HTTPS répond sur le port 443
- [ ] Espace disque OK (< 80%)
- [ ] Mémoire disponible OK (> 20%)

### Tests d'accès web

- [ ] HTTP accessible: http://10.10.10.40
- [ ] HTTPS accessible: https://10.10.10.40 (certificat auto-signé)
- [ ] Port direct accessible: http://10.10.10.40:8069
- [ ] Page de création de base de données s'affiche

### Vérification des logs

```bash
docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml logs --tail=50
```

- [ ] Aucune erreur critique dans les logs
- [ ] PostgreSQL initialisé correctement
- [ ] Odoo démarré correctement
- [ ] Nginx démarré correctement

---

## 📋 PHASE 5 : CONFIGURATION INITIALE

### Création de la première base de données

Via le navigateur à http://10.10.10.40:

- [ ] Base de données créée: Nom _____________
- [ ] Langue: Français
- [ ] Pays: France (ou autre)
- [ ] Données de démo: Désactivées
- [ ] Connexion admin réussie

### Installation des modules SaaS

Dans Odoo (Apps):

- [ ] Module `saas_base` installé
- [ ] Module `saas_portal` installé
- [ ] Module `saas_server` installé
- [ ] Modules `kondro_*` installés (si nécessaire)

---

## 📋 PHASE 6 : SÉCURISATION

### Firewall

```bash
sudo ufw status
```

- [ ] Port 22 (SSH) ouvert
- [ ] Port 80 (HTTP) ouvert
- [ ] Port 443 (HTTPS) ouvert
- [ ] Port 5432 (PostgreSQL) FERMÉ (accès externe)
- [ ] UFW activé et fonctionnel

### SSL/TLS

#### Option A : Certificat auto-signé (temporaire)

- [ ] Certificat généré dans `/opt/odoo-saas/ssl/`
- [ ] HTTPS fonctionne (avertissement navigateur normal)

#### Option B : Let's Encrypt (production)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

- [ ] Certbot installé
- [ ] Certificat obtenu pour le domaine
- [ ] Renouvellement automatique configuré
- [ ] HTTPS fonctionne sans avertissement

### Fail2ban (protection brute-force)

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

- [ ] Fail2ban installé
- [ ] Fail2ban activé au démarrage
- [ ] Fail2ban en cours d'exécution

### Désactivation du port direct (après tests)

```bash
sudo ufw delete allow 8069/tcp
```

- [ ] Port 8069 fermé (après validation complète)

---

## 📋 PHASE 7 : SAUVEGARDES

### Test de sauvegarde manuelle

```bash
cd /opt/odoo-saas
bash scripts/backup.sh manual
```

- [ ] Sauvegarde créée dans `/opt/odoo-saas/backups/`
- [ ] Fichier de base de données: Taille _____________
- [ ] Fichier filestore: Taille _____________
- [ ] Fichier de métadonnées créé

### Configuration des sauvegardes automatiques

```bash
crontab -e
```

Ajouter :
```cron
0 2 * * * /opt/odoo-saas/scripts/backup.sh daily
0 3 * * 0 /opt/odoo-saas/scripts/backup.sh weekly
0 4 1 * * /opt/odoo-saas/scripts/backup.sh monthly
```

- [ ] Crontab configuré
- [ ] Backup quotidien: 2h du matin
- [ ] Backup hebdomadaire: Dimanche 3h
- [ ] Backup mensuel: 1er du mois 4h

### Test de restauration

```bash
bash scripts/restore.sh /opt/odoo-saas/backups/manual/odoo_db_*.sql.gz
```

- [ ] Restauration testée et fonctionnelle

---

## 📋 PHASE 8 : MONITORING & LOGS

### Configuration des logs

- [ ] Logs Odoo activés: `/opt/odoo-saas/logs/`
- [ ] Logs Nginx activés: `/opt/odoo-saas/config/nginx-logs/`
- [ ] Rotation des logs configurée (Docker)

### Commandes de monitoring

```bash
# État des services
bash scripts/maintenance.sh status

# Statistiques système
bash scripts/maintenance.sh stats

# Santé globale
bash scripts/maintenance.sh health
```

- [ ] Toutes les commandes fonctionnent
- [ ] Monitoring accessible

---

## 📋 PHASE 9 : DOCUMENTATION

### Documentation sur le serveur

- [ ] Guide complet présent: `/opt/odoo-saas/infrastructure/GUIDE_DEPLOIEMENT_OVH.md`
- [ ] README présent: `/opt/odoo-saas/infrastructure/README_DEPLOIEMENT_OVH.md`
- [ ] Scripts documentés et exécutables

### Documentation interne

- [ ] Mots de passe sauvegardés dans le coffre-fort
- [ ] Procédures de backup documentées
- [ ] Procédures de restauration documentées
- [ ] Contacts support notés
- [ ] Architecture réseau documentée

---

## 📋 PHASE 10 : TESTS FONCTIONNELS

### Tests de base

- [ ] Création d'utilisateur
- [ ] Création d'un client SaaS (si applicable)
- [ ] Envoi d'email de test
- [ ] Upload de fichier
- [ ] Génération de rapport PDF
- [ ] Accès concurrent (plusieurs utilisateurs)

### Tests de performance

- [ ] Temps de réponse acceptable (< 2s)
- [ ] Utilisation CPU normale (< 70%)
- [ ] Utilisation mémoire normale (< 80%)
- [ ] Espace disque suffisant (> 20% libre)

### Tests de résilience

- [ ] Redémarrage des services OK
- [ ] Redémarrage du serveur OK
- [ ] Services redémarrent automatiquement
- [ ] Données persistantes après redémarrage

---

## 📋 VALIDATION FINALE

### Checklist de mise en production

- [ ] Tous les tests passés
- [ ] Sauvegardes configurées et testées
- [ ] SSL/TLS configuré (Let's Encrypt)
- [ ] Monitoring en place
- [ ] Documentation complète
- [ ] Équipe formée sur les procédures
- [ ] Support technique disponible
- [ ] Plan de rollback préparé

### Informations de production

- **URL de production**: _________________________________
- **Base de données**: _________________________________
- **Date de mise en production**: _________________________________
- **Version Odoo**: _________________________________
- **Nombre d'utilisateurs prévus**: _________________________________

---

## 📞 CONTACTS SUPPORT

### Support technique
- **Email**: apps@itexperts4africa.com
- **Téléphone**: _________________________________

### Hébergement OVH
- **IP Serveur**: 10.10.10.40
- **Compte OVH**: _________________________________
- **Contact OVH**: _________________________________

### Équipe interne
- **Administrateur système**: _________________________________
- **Administrateur Odoo**: _________________________________
- **Responsable projet**: _________________________________

---

## 📝 NOTES & OBSERVATIONS

```
Date: _______________

Problèmes rencontrés:
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________

Solutions appliquées:
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________

Améliorations futures:
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________

Autres remarques:
_____________________________________________________________________________
_____________________________________________________________________________
_____________________________________________________________________________
```

---

## ✅ VALIDATION

**Je certifie que toutes les étapes de cette checklist ont été complétées avec succès.**

**Nom**: _________________________________  
**Signature**: _________________________________  
**Date**: _________________________________

---

**Document généré le**: 2024-11-13  
**Version**: 1.0  
**Serveur**: 10.10.10.40  
**Auteur**: KONDRO Networks

