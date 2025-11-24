#!/bin/bash

# 💾 Script de sauvegarde automatique - Odoo SaaS
# Usage: ./backup.sh [daily|weekly|monthly]

set -e

# Configuration
PROJECT_DIR="/opt/odoo-saas"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

# Type de backup (daily par défaut)
BACKUP_TYPE="${1:-daily}"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERREUR]${NC} $1"
    exit 1
}

# Charger les variables d'environnement
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(cat "$PROJECT_DIR/.env" | grep -v '^#' | xargs)
else
    error "Fichier .env non trouvé dans $PROJECT_DIR"
fi

# Créer le répertoire de backup
mkdir -p "$BACKUP_DIR/$BACKUP_TYPE"

log "🚀 Début de la sauvegarde ($BACKUP_TYPE)..."

# 1. Backup de la base de données
log "📦 Sauvegarde de la base de données..."
BACKUP_FILE="$BACKUP_DIR/$BACKUP_TYPE/odoo_db_${DATE}.sql.gz"

docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" exec -T postgres \
    pg_dump -U "${POSTGRES_USER:-odoo}" "${POSTGRES_DB:-odoo_prod}" | gzip > "$BACKUP_FILE"

if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    log "✅ Base de données sauvegardée: $BACKUP_FILE ($BACKUP_SIZE)"
else
    error "Échec de la sauvegarde de la base de données"
fi

# 2. Backup des filestores
log "📁 Sauvegarde des filestores..."
FILESTORE_BACKUP="$BACKUP_DIR/$BACKUP_TYPE/filestore_${DATE}.tar.gz"

if [ -d "$PROJECT_DIR/filestore" ]; then
    tar -czf "$FILESTORE_BACKUP" -C "$PROJECT_DIR" filestore
    FILESTORE_SIZE=$(du -h "$FILESTORE_BACKUP" | cut -f1)
    log "✅ Filestores sauvegardés: $FILESTORE_BACKUP ($FILESTORE_SIZE)"
else
    log "⚠️  Répertoire filestore non trouvé"
fi

# 3. Backup de la configuration
log "⚙️  Sauvegarde de la configuration..."
CONFIG_BACKUP="$BACKUP_DIR/$BACKUP_TYPE/config_${DATE}.tar.gz"

tar -czf "$CONFIG_BACKUP" \
    -C "$PROJECT_DIR" \
    config/ \
    --exclude='*.log' \
    2>/dev/null || true

if [ -f "$CONFIG_BACKUP" ]; then
    log "✅ Configuration sauvegardée: $CONFIG_BACKUP"
fi

# 4. Créer un fichier de métadonnées
METADATA_FILE="$BACKUP_DIR/$BACKUP_TYPE/backup_${DATE}.info"
cat > "$METADATA_FILE" << EOF
Backup Date: $(date)
Backup Type: $BACKUP_TYPE
Database: $POSTGRES_DB
Database File: $BACKUP_FILE
Filestore File: $FILESTORE_BACKUP
Config File: $CONFIG_BACKUP
Server: $(hostname)
Odoo Version: $(docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" exec -T odoo odoo --version 2>/dev/null || echo "Unknown")
EOF

log "📝 Métadonnées sauvegardées: $METADATA_FILE"

# 5. Nettoyer les anciennes sauvegardes
log "🧹 Nettoyage des anciennes sauvegardes (> $RETENTION_DAYS jours)..."
find "$BACKUP_DIR/$BACKUP_TYPE" -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR/$BACKUP_TYPE" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR/$BACKUP_TYPE" -name "*.info" -mtime +$RETENTION_DAYS -delete

# 6. Afficher un résumé
log "📊 Résumé de la sauvegarde:"
echo "   Type: $BACKUP_TYPE"
echo "   Date: $(date)"
echo "   Base de données: $BACKUP_SIZE"
echo "   Emplacement: $BACKUP_DIR/$BACKUP_TYPE"

# 7. Statistiques d'espace
TOTAL_BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
log "💽 Espace total utilisé par les backups: $TOTAL_BACKUP_SIZE"

# 8. Optionnel: Envoi vers S3 ou FTP
if [ "${BACKUP_S3_ENABLED:-false}" = "true" ]; then
    log "☁️  Envoi vers S3..."
    # Ajouter ici la commande pour envoyer vers S3
    # aws s3 cp "$BACKUP_FILE" "s3://$BACKUP_S3_BUCKET/"
fi

log "✅ Sauvegarde terminée avec succès!"

exit 0

