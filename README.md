# 🏢 Odoo SaaS Tools - Plateforme SaaS Complète (MAJ 2024)
```bash
docker compose -f config/docker-compose.simple.yml restart odoo
```

[![Build Status](http://runbot.it-projects.info/runbot/badge/flat/odoo-saas-tools/18.0.svg)](http://runbot.it-projects.info/demo/odoo-saas-tools/18.0)
[![Version](https://img.shields.io/badge/version-18.0.2.1.0-blue.svg)](https://github.com/KONDRONETWORKS/odoo-saas-tools)
[![License](https://img.shields.io/badge/license-LGPL--3-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://python.org)

## 🚀 NOUVEAUTÉS & MISES À JOUR 2024

- **Compatibilité Odoo 18.x - 2024**
- **Support PostgreSQL 15+**
- **Scripts de provisioning simplifiés**
- **API SaaS v2 améliorée & + sécurisée**
- **Nouvel installateur one-shot pour les démos & prod**
- **Sauvegardes externalisées automatiques (S3, FTP, Minio, Azure Blob)**
- **Templates de plans e-commerce & SaaS entreprise inclus**
- **Portail Auto-Démo RESTYLÉ (Nouveau Module: saas_portal_demo2)**
- **Mode Multi-Région pour cloud (multi-VPC, tests CI/CD, blue/green)**
- **Scripts de migration/upgrade inclus**
- **Documentation FR/EN automatisée**

---

## 🌟 INSTALLATION RAPIDE - LA NOUVELLE PROCÉDURE

> **Odoo 18.0+ / Python 3.11+ / PostgreSQL 15+ requis**
>
> Installez en 2 minutes !

```bash
git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git
cd odoo-saas-tools
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1 seule ligne pour tout initialiser (données tests + prod)
python3.11 setup_all.py --full-init
```

**Docker :**
```bash
docker compose -f docker/docker-compose.yml up -d
```

**Commandes de base :**
```bash
python3.11 saas.py --all
```

> Voir la [Documentation Mode d’Emploi](docs/setup/DEMARRAGE_RAPIDE.md) pour la version détaillée.

---

## 🏗️ NOUVELLE ARCHITECTURE DES MODULES

| Groupe           | Modules Principaux (MAJ 2024)       | Notes/Nouveautés           |
|------------------|-------------------------------------|----------------------------|
| **Fondation**    | `saas_base`                         | Classes core, logs, OAuth2 |
| **Sécurité**     | `auth_oauth`, `auth_oauth_check_client_id`, `auth_oauth_ip`, `oauth_provider` | Audit log & 2FA            |
| **Portail**      | `saas_portal`, `saas_portal_portal`, `saas_portal_demo2`  | Nouveau portail client UX  |
| **Serveur**      | `saas_server`, `saas_server_demo`   | Moteur de création, test   |
| **Client**       | `saas_client`                       | UX client simplifiée       |
| **Ventes**       | `saas_portal_sale*`, `saas_portal_sale_online`, `saas_portal_sale_subscription`, `saas_portal_subscription` | Paiements Stripe, Paypal   |
| **Backup**       | `saas_server_backup_ftp`, `saas_server_backup_s3`, `saas_server_backup_minio`, `saas_server_backup_rotate`, `saas_portal_backup_ui` | Minio/Blob S3 natif        |
| **Infra/Outils** | `saas_sysadmin`, `saas_utils`, `saas_portal_tagging`, `saas_portal_async`, `saas_server_autodelete`, `saas_portal_signup_custom` | Monitoring Prometheus, slack |
| **Templates**    | `saas_portal_templates`, `saas_portal_start`, `saas_portal_signup`, `saas_portal_demo` | Nouvel import/export plans |

---

## 🖥️ INFRASTRUCTURE & PRÉREQUIS MAJ

### Système minimum recommandé
- Python 3.11+ (obligatoire depuis v18.x.2.0)
- PostgreSQL 15+
- Odoo 18.0.x (communauté ou entreprise)
- Docker Compose (optionnel recommandé)
- Ubuntu 22.04 / Debian 12 / macOS Sonoma

### Cloud compatible & tested :
- AWS, GCP, Azure, Scaleway, DigitalOcean, Hetzner, OVH, Contabo, etc.

### Exemples déploiements
#### Développement local
```yaml
CPU: 2-4 vCPU
RAM: 6-12 GB
SSD: 60-200 GB
```
#### Production PME/SaaS
```yaml
CPU: 8 vCPU
RAM: 24-32 GB
Disque: 200+ GB SSD NVMe
Load Balancer: Nginx/HAProxy
Sauvegarde: S3, Blob, FTP
```

---

## 🐳 DOCKER / K8s (AVANCÉ)

- `docker/docker-compose.yml` prêt à l’emploi
- Support Kubernetes via Helm chart (cf. `infra/k8s/`)

#### Lancement simple :
```bash
docker compose up -d
```
#### Monitoring :
```bash
docker compose -f docker/monitoring.yml up -d
```

---

## 🚨 NOUVEAUTÉS/MIGRATION

- **API GraphQL** disponible (module `saas_api_graphql`)
- **Export/Import bulk des clients & plans**
- **Module de démo prêt à l’emploi**
- **Plus de scripts de migration Odoo 18**
- **Auto scaling vertical/horizontal par plan**

---

## 🛡️ SÉCURITÉ & SAUVEGARDE AUTOMATISÉES

- Sauvegardes: planifiable via UI ou CRON (`saas_portal_backup_ui`)
- Notifications sécurisées (Email, Slack, Discord)
- 2FA admins & logs de sécurité
- Audit des accès et journalisation complète (`auditlog` recommandé)

---

## 🔄 WORKFLOWS ET FLUX DE COMMUNICATION (MAJ V2)

- Création client SaaS → Génération instance → Provisioning → Notification email/sms
- Paiement (Stripe/Paypal/Sepa/Factures) → Activation → Livraison automatique
- Sauvegardes (locales/externalisées) → Rétention paramétrable
- Monitoring (Prometheus/Influx/ELK/Slack)

---

## 📚 DOCUMENTATION & SUPPORT MAJ

- [Documentation FR/EN](https://odoo-saas-tools.readthedocs.io/)
- **Nouveaux guides** : Quickstart, upgrade, troubleshooting, FAQ
- **Mises à jour régulières** : https://github.com/KONDRONETWORKS/odoo-saas-tools

---

## 🛠️ OUTILS DE DÉV / DEVOPS

- Scripts CLI : `setup_all.py`, `saas.py`, `migrate_db.py`, etc.
- Tests : `pytest`, `black .`, `flake8 .`
- Santé cloud : `/health` endpoint natif, Prometheus, Grafana

---

## 🤝 SUPPORT ET CONTRIBUTIONS

- Email : apps@itexperts4africa.com
- Issues & demandes : [Créer une issue GitHub](https://github.com/KONDRONETWORKS/odoo-saas-tools/issues)
- Slack communautaire (voir documentation)
- Documentation FAQ & guides vidéo mis à jour
- Bugs, questions, suggestions : bienvenus !

---

## 📄 LICENCE OPEN SOURCE

Projet sous licence **LGPL-3** (voir [LICENSE](LICENSE))

---

**Créez votre SaaS Odoo — plus simple, sécurisé et scalable que jamais avec la version 2024 !**
