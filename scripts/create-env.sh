#!/bin/bash

# 🔐 Script de création du fichier .env
# Usage: bash scripts/create-env.sh

set -e

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Répertoire du projet
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

ENV_FILE="$PROJECT_ROOT/.env"

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  🔐 CRÉATION DU FICHIER .env${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Vérifier si le fichier existe déjà
if [ -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  Le fichier .env existe déjà.${NC}"
    read -p "Voulez-vous le remplacer? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Opération annulée."
        exit 0
    fi
    echo ""
fi

# Générer des mots de passe sécurisés
echo -e "${BLUE}Génération de mots de passe sécurisés...${NC}"
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-30)
ODOO_ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-30)
SECRET_KEY=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-30)

echo -e "${GREEN}✅ Mots de passe générés${NC}"
echo ""

# Créer le fichier .env
cat > "$ENV_FILE" << EOF
# 🔐 Configuration d'environnement - Odoo SaaS Production OVH
# Serveur: 10.10.10.40
# OS: Ubuntu 22.04.5 LTS
# Date de création: $(date +%Y-%m-%d)
#
# ⚠️ IMPORTANT: Ce fichier contient des informations sensibles
# Ne le commitez JAMAIS dans Git (il est dans .gitignore)

# ==================== BASE DE DONNÉES ====================
POSTGRES_DB=odoo_prod
POSTGRES_USER=odoo
POSTGRES_PASSWORD=$POSTGRES_PASSWORD

# ==================== ODOO ====================
ODOO_ADMIN_PASSWD=$ODOO_ADMIN_PASSWORD
ODOO_DB_PASSWORD=$POSTGRES_PASSWORD

# ==================== SERVEUR ====================
SERVER_IP=10.10.10.40
DOMAIN_NAME=10.10.10.40

# ==================== EMAIL / SMTP ====================
# Configurez ces valeurs selon votre fournisseur d'email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre.email@gmail.com
SMTP_PASSWORD=VotreMotDePasseEmail123!
SMTP_SSL=False

# Pour Gmail, créez un mot de passe d'application:
# https://myaccount.google.com/apppasswords

# Pour AWS SES:
# SMTP_SERVER=email-smtp.eu-west-1.amazonaws.com
# SMTP_PORT=587
# SMTP_USER=votre_access_key_id
# SMTP_PASSWORD=votre_secret_access_key

# ==================== SÉCURITÉ ====================
# Clé secrète pour les sessions
SECRET_KEY=$SECRET_KEY

# ==================== SAUVEGARDES ====================
# S3 (AWS, OVH, etc.) - À configurer si nécessaire
BACKUP_S3_ENABLED=false
BACKUP_S3_BUCKET=odoo-backups
BACKUP_S3_ACCESS_KEY=
BACKUP_S3_SECRET_KEY=
BACKUP_S3_REGION=eu-west-1

# FTP - À configurer si nécessaire
BACKUP_FTP_ENABLED=false
BACKUP_FTP_HOST=ftp.votreserveur.com
BACKUP_FTP_USER=
BACKUP_FTP_PASSWORD=
BACKUP_FTP_PORT=21

# ==================== MONITORING ====================
# Sentry (optionnel)
SENTRY_DSN=
SENTRY_ENVIRONMENT=production

# Prometheus (optionnel)
PROMETHEUS_ENABLED=false
PROMETHEUS_PORT=9090

# ==================== LOGS ====================
LOG_LEVEL=info
LOG_HANDLER=:INFO
LOG_DB=false

# ==================== PERFORMANCE ====================
# Nombre de workers (recommandé: nombre de CPU * 2 + 1)
# Pour une VM avec 4 CPU, on utilise 4 workers
WORKERS=4
MAX_CRON_THREADS=2

# Limites mémoire (en octets)
# 2 GB soft, 2.5 GB hard
LIMIT_MEMORY_SOFT=2147483648
LIMIT_MEMORY_HARD=2684354560

# Limites de temps (en secondes)
LIMIT_TIME_CPU=600
LIMIT_TIME_REAL=1200

# ==================== DÉVELOPPEMENT ====================
# À désactiver en production !
DEV_MODE=false
DEBUG_MODE=false
RELOAD=false

# ==================== RÉSEAU ====================
# Proxy mode (activé si derrière Nginx)
PROXY_MODE=true

# Database filter (pour multi-database)
DB_FILTER=^%d$

# ==================== MODULES ====================
# Modules à charger au démarrage
SERVER_WIDE_MODULES=base,web,queue_job

# Path des addons (séparés par des virgules)
ADDONS_PATH=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons

# ==================== DIVERS ====================
# Désactiver les données de démonstration
WITHOUT_DEMO=all

# Activer la base de données de listing (false en production)
LIST_DB=false

# Timezone
TZ=Europe/Paris

# ==================== NOTES IMPORTANTES ====================
# 
# 1. Mots de passe générés automatiquement:
#    - PostgreSQL: $POSTGRES_PASSWORD
#    - Admin Odoo: $ODOO_ADMIN_PASSWORD
#
# 2. ⚠️ SAUVEGARDEZ CES MOTS DE PASSE DANS UN ENDROIT SÛR !
#
# 3. Configurez SMTP_USER et SMTP_PASSWORD pour l'envoi d'emails
#
# 4. Pour les sauvegardes S3/FTP, configurez les variables BACKUP_* si nécessaire
#
# 5. Ce fichier est dans .gitignore et ne sera pas versionné
#
EOF

# Protéger le fichier
chmod 600 "$ENV_FILE"

echo -e "${GREEN}✅ Fichier .env créé avec succès !${NC}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}⚠️  MOTS DE PASSE GÉNÉRÉS - SAUVEGARDEZ-LES !${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "📦 PostgreSQL: ${GREEN}$POSTGRES_PASSWORD${NC}"
echo -e "👤 Admin Odoo: ${GREEN}$ODOO_ADMIN_PASSWORD${NC}"
echo ""
echo -e "${YELLOW}⚠️  Ces mots de passe sont aussi dans le fichier .env${NC}"
echo -e "${YELLOW}⚠️  Sauvegardez-les dans un endroit sûr avant de continuer !${NC}"
echo ""
echo -e "${BLUE}Emplacement du fichier:${NC} $ENV_FILE"
echo -e "${BLUE}Permissions:${NC} $(ls -l "$ENV_FILE" | awk '{print $1}')"
echo ""

# Afficher les prochaines étapes
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  📋 PROCHAINES ÉTAPES${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo "1. Vérifiez le fichier .env et modifiez si nécessaire:"
echo "   nano .env"
echo ""
echo "2. Configurez SMTP_USER et SMTP_PASSWORD pour les emails"
echo ""
echo "3. Sur le serveur, lancez le déploiement:"
echo "   docker compose -f config/docker-compose.ovh.yml up -d"
echo ""
echo "4. Ou utilisez le script automatique:"
echo "   bash infrastructure/deploy-ovh.sh"
echo ""

exit 0





