# 🏢 Odoo SaaS Tools - Plateforme SaaS Complète

[![Build Status](http://runbot.it-projects.info/runbot/badge/flat/odoo-saas-tools/18.0.svg)](http://runbot.it-projects.info/demo/odoo-saas-tools/18.0)
[![Version](https://img.shields.io/badge/version-18.0.1.0.0-blue.svg)](https://github.com/KONDRONETWORKS/odoo-saas-tools)
[![License](https://img.shields.io/badge/license-LGPL--3-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)

> **Système complet pour créer et gérer des plateformes SaaS basées sur Odoo**

## 📋 Table des Matières

- [🎯 Vue d'ensemble](#-vue-densemble)
- [🏗️ Architecture](#️-architecture)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [📦 Modules](#-modules)
- [🔧 Mode Opératoire](#-mode-opératoire)
- [📚 Documentation](#-documentation)
- [🤝 Support](#-support)

## 🎯 Vue d'ensemble

**Odoo SaaS Tools** est un système complet permettant de créer et gérer des plateformes SaaS (Software as a Service) basées sur Odoo. Il automatise la création, la gestion et la monétisation d'instances Odoo pour vos clients.

### ✨ Fonctionnalités Principales

- 🏗️ **Création automatique** de bases de données clients
- 💰 **Monétisation** via abonnements et ventes en ligne
- 🎛️ **Gestion centralisée** de toutes les instances
- 📊 **Monitoring** et métriques avancées
- 🔐 **Sécurité** renforcée avec OAuth2
- 🛡️ **Sauvegardes** automatiques (FTP, S3, rotation)
- 🌐 **Multi-serveurs** pour la scalabilité

## 🏗️ Architecture

Le système est composé de **3 composants principaux** :

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SaaS Portal   │    │  SaaS Servers   │    │  SaaS Clients   │
│                 │    │                 │    │                 │
│ • Contrôle      │◄──►│ • Création      │◄──►│ • Instances     │
│   central       │    │   bases         │    │   Odoo          │
│ • Gestion plans │    │ • Gestion       │    │ • Clients       │
│ • Administration│    │   technique     │    │   finaux        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔧 Composants Techniques

- **SaaS Portal** : Base de données principale de contrôle
- **SaaS Servers** : Serveurs techniques pour la gestion des instances
- **SaaS Clients** : Bases de données utilisées par les clients finaux

## 🚀 Installation

### Prérequis

- **Python** 3.8+
- **PostgreSQL** 12+
- **Odoo** 18.0
- **Git**

### Installation Rapide

```bash
# Cloner le repository
git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git
cd odoo-saas-tools

# Installer les dépendances
pip install -r requirements.txt

# Vérifier la compatibilité
python3 check_compatibility.py

# Créer l'environnement SaaS
python3 saas.py --portal-create --server-create --plan-create --run
```

### Installation avec Docker

```bash
# Démarrer avec Docker Compose
docker-compose up -d

# Ou construire l'image
docker build -t odoo-saas-tools:18.0 .
```

## ⚙️ Configuration

### Variables d'Environnement

```bash
# Configuration Odoo
ODOO_VERSION=18
ODOO_SCRIPT=./odoo-server
ODOO_CONFIG=./odoo.conf

# Configuration Base de Données
DB_HOST=localhost
DB_PORT=5432
DB_USER=odoo
DB_PASSWORD=odoo

# Configuration SaaS
BASE_DOMAIN=your-domain.com
ADMIN_PASSWORD=admin
MASTER_PASSWORD=admin
```

### Fichier de Configuration

Créez un fichier `odoo.conf` :

```ini
[options]
addons_path = /path/to/addons
data_dir = /path/to/filestore
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
xmlrpc_port = 8069
longpolling_port = 8072
```

## 📦 Modules

### 🏢 Modules Principaux

#### `saas_base`
**Fonctionnalités de base du système SaaS**
- Classes de base pour tous les modules SaaS
- Outils communs et exceptions
- Configuration système

#### `saas_portal`
**Portail principal de gestion SaaS**
- Interface d'administration centrale
- Gestion des serveurs et clients
- Configuration des plans et templates
- Monitoring des instances

#### `saas_server`
**Serveur technique de gestion**
- Création et suppression de bases de données
- Gestion des instances clients
- Communication avec le portail
- Configuration OAuth2

#### `saas_client`
**Interface client**
- Authentification OAuth2
- Limitation des utilisateurs
- Dashboard client
- Gestion des accès

### 🛒 Modules de Vente

#### `saas_portal_sale`
**Vente d'abonnements SaaS**
- Gestion des plans tarifaires
- Facturation des abonnements
- Suivi des paiements
- Gestion des contrats

#### `saas_portal_sale_online`
**Vente en ligne**
- Boutique en ligne intégrée
- Processus de commande
- Paiements en ligne
- Gestion des devis

#### `saas_portal_sale_subscription`
**Gestion des souscriptions**
- Cycles de facturation
- Renouvellements automatiques
- Notifications d'expiration
- Gestion des suspensions

### 🎨 Modules de Portail

#### `saas_portal_start`
**Page de démarrage**
- Interface de création de compte
- Sélection de sous-domaine
- Processus d'onboarding
- Templates de démarrage

#### `saas_portal_signup`
**Inscription des clients**
- Formulaires d'inscription
- Validation des données
- Création automatique de compte
- Emails de bienvenue

#### `saas_portal_demo`
**Démonstrations**
- Accès aux démos
- Limitation de temps
- Conversion vers compte payant
- Gestion des essais

#### `saas_portal_templates`
**Gestion des templates**
- Création de templates
- Configuration des modules
- Déploiement automatique
- Gestion des versions

### 🛡️ Modules de Sauvegarde

#### `saas_server_backup_ftp`
**Sauvegarde FTP**
- Sauvegardes automatiques
- Transfert FTP sécurisé
- Rotation des sauvegardes
- Restauration rapide

#### `saas_server_backup_s3`
**Sauvegarde Amazon S3**
- Intégration AWS S3
- Sauvegardes chiffrées
- Gestion des coûts
- Restauration cloud

#### `saas_server_backup_rotate`
**Rotation des sauvegardes**
- Politiques de rétention
- Compression automatique
- Nettoyage des anciennes sauvegardes
- Optimisation de l'espace

### 🔐 Modules de Sécurité

#### `oauth_provider`
**Fournisseur OAuth2**
- Authentification sécurisée
- Gestion des tokens
- Intégration SSO
- Sécurité renforcée

#### `auth_oauth_check_client_id`
**Vérification des clients OAuth**
- Validation des clients
- Contrôle d'accès
- Audit des connexions
- Sécurité des API

#### `auth_oauth_ip`
**Authentification par IP**
- Contrôle géographique
- Listes blanches/noires
- Sécurité réseau
- Monitoring des accès

### 🛠️ Modules d'Administration

#### `saas_sysadmin`
**Administration système**
- Monitoring des serveurs
- Gestion des ressources
- Alertes système
- Maintenance automatique

#### `saas_sysadmin_aws`
**Intégration AWS**
- Gestion des instances EC2
- Auto-scaling
- Load balancing
- Monitoring CloudWatch

#### `saas_sysadmin_route53`
**Gestion DNS Route53**
- Configuration DNS automatique
- Gestion des sous-domaines
- SSL automatique
- Monitoring DNS

#### `saas_sysadmin_mailgun`
**Intégration email**
- Envoi d'emails transactionnels
- Templates d'emails
- Suivi des livraisons
- Gestion des bounces

### 🔧 Modules Utilitaires

#### `saas_utils`
**Utilitaires généraux**
- Fonctions communes
- Helpers et helpers
- Outils de développement
- Tests automatisés

#### `saas_portal_tagging`
**Système de tags**
- Classification des clients
- Segmentation marketing
- Rapports personnalisés
- Gestion des segments

#### `saas_portal_async`
**Traitement asynchrone**
- Tâches en arrière-plan
- Queue de traitement
- Monitoring des jobs
- Gestion des erreurs

## 🔧 Mode Opératoire

### 1. 🚀 Démarrage Initial

#### Création de l'Environnement

```bash
# 1. Créer le portail principal
python3 saas.py --portal-create --run

# 2. Créer un serveur SaaS
python3 saas.py --server-create --run

# 3. Créer un plan de base
python3 saas.py --plan-create --run
```

#### Configuration Initiale

1. **Accéder au portail** : `http://localhost:8069`
2. **Se connecter** avec admin/admin
3. **Configurer le domaine de base** : Settings > SaaS Portal Settings
4. **Ajouter un serveur** : SaaS > Servers > Create
5. **Créer un plan** : SaaS > Plans > Create

### 2. 📊 Gestion des Clients

#### Création d'un Client

```bash
# Via l'interface web
1. Aller dans SaaS > Clients
2. Cliquer sur "Create"
3. Remplir les informations
4. Sélectionner le plan
5. Cliquer sur "Save"

# Via l'API
curl -X POST http://localhost:8069/api/saas/client \
  -H "Content-Type: application/json" \
  -d '{"name": "client1", "plan_id": 1, "subdomain": "client1"}'
```

#### Gestion des Instances

1. **Accéder à l'instance** : Cliquer sur le nom du client
2. **Installer des modules** : Apps > Install
3. **Configurer les paramètres** : Settings > Parameters
4. **Gérer les utilisateurs** : Users > Manage
5. **Surveiller l'utilisation** : Dashboard > Statistics

### 3. 💰 Gestion Commerciale

#### Configuration des Plans

1. **Créer un plan** : SaaS > Plans > Create
2. **Définir les tarifs** : Pricing > Set Prices
3. **Configurer les limites** : Limits > Set Limits
4. **Activer la vente** : Sales > Enable

#### Processus de Vente

1. **Client visite** la page de démarrage
2. **Sélectionne** un plan
3. **Remplit** le formulaire d'inscription
4. **Effectue** le paiement
5. **Reçoit** l'accès à son instance

### 4. 🛡️ Maintenance et Monitoring

#### Surveillance des Serveurs

```bash
# Vérifier l'état des serveurs
python3 saas.py --test

# Monitorer les ressources
python3 saas.py --monitor

# Vérifier les sauvegardes
python3 saas.py --backup-check
```

#### Gestion des Sauvegardes

1. **Configurer les sauvegardes** : Settings > Backup
2. **Programmer les sauvegardes** : Schedule > Set Schedule
3. **Vérifier les sauvegardes** : Backup > Check Status
4. **Restaurer si nécessaire** : Backup > Restore

### 5. 🔧 Administration Avancée

#### Gestion Multi-Serveurs

```bash
# Ajouter un nouveau serveur
python3 saas.py --server-create --server-name server2

# Configurer le load balancing
python3 saas.py --configure-load-balancer

# Migrer des clients
python3 saas.py --migrate-clients --from-server server1 --to-server server2
```

#### Monitoring et Alertes

1. **Configurer les alertes** : Settings > Alerts
2. **Définir les seuils** : Thresholds > Set Limits
3. **Configurer les notifications** : Notifications > Setup
4. **Surveiller les métriques** : Dashboard > Metrics

### 6. 📈 Optimisation et Scaling

#### Auto-Scaling

```bash
# Configurer l'auto-scaling
python3 saas.py --configure-auto-scaling

# Définir les règles de scaling
python3 saas.py --set-scaling-rules

# Monitorer les performances
python3 saas.py --monitor-performance
```

#### Optimisation des Performances

1. **Analyser les performances** : Reports > Performance
2. **Optimiser les requêtes** : Database > Optimize
3. **Configurer le cache** : Cache > Configure
4. **Ajuster les ressources** : Resources > Adjust

## 📚 Documentation

### 📖 Guides Détaillés

- **[Guide de Migration](MIGRATION_18.md)** - Migration vers Odoo 18.0
- **[Résultats des Tests](TEST_RESULTS.md)** - Tests de compatibilité
- **[Résumé de Migration](MIGRATION_SUMMARY.md)** - Résumé des modifications

### 🔗 Liens Utiles

- **Site Principal** : https://it-projects-llc.github.io/odoo-saas-tools/
- **Documentation** : https://odoo-saas-tools.readthedocs.io/
- **Démarrage Rapide** : https://it-projects-llc.github.io/odoo-saas-tools/getting-started/
- **Blog** : https://it-projects-llc.github.io/odoo-saas-tools/blog/

### 🛠️ Outils de Développement

- **Script de vérification** : `python3 check_compatibility.py`
- **Tests automatisés** : `pytest`
- **Formatage de code** : `black . && isort .`
- **Linting** : `flake8 .`

## 🤝 Support

### 📞 Contact

- **Email** : apps@it-projects.info
- **GitHub Issues** : [Créer une issue](https://github.com/KONDRONETWORKS/odoo-saas-tools/issues)
- **Documentation** : [Lire la documentation](https://odoo-saas-tools.readthedocs.io/)

### 🐛 Signaler un Bug

1. Vérifiez les [issues existantes](https://github.com/KONDRONETWORKS/odoo-saas-tools/issues)
2. Créez une nouvelle issue avec :
   - Description détaillée du problème
   - Étapes pour reproduire
   - Logs d'erreur
   - Version utilisée

### 💡 Proposer une Amélioration

1. Créez une issue avec le label "enhancement"
2. Décrivez l'amélioration souhaitée
3. Expliquez les bénéfices
4. Proposez une implémentation si possible

---

## 📄 Licence

Ce projet est sous licence **LGPL-3**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- **IT-Projects LLC** - Développement initial
- **KONDRO Networks** - Maintenance et améliorations
- **Communauté Odoo** - Contributions et retours

---

**🎯 Créez votre propre plateforme SaaS Odoo avec Odoo SaaS Tools !**
