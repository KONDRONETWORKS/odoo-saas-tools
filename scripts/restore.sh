#!/bin/bash

# 🔄 Script de restauration - Odoo SaaS
# Usage: ./restore.sh <backup_file.sql.gz>

set -e

# Configuration
PROJECT_DIR="/opt/odoo-saas"

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

warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1"
}

# Vérifier les arguments
if [ $# -eq 0 ]; then
    error "Usage: $0 <backup_file.sql.gz>"
fi

BACKUP_FILE="$1"

# Vérifier que le fichier existe
if [ ! -f "$BACKUP_FILE" ]; then
    error "Fichier de sauvegarde introuvable: $BACKUP_FILE"
fi

# Charger les variables d'environnement
if [ -f "$PROJECT_DIR/.env" ]; then
    export $(cat "$PROJECT_DIR/.env" | grep -v '^#' | xargs)
else
    error "Fichier .env non trouvé dans $PROJECT_DIR"
fi

# Confirmation
warning "⚠️  ATTENTION: Cette opération va écraser la base de données actuelle!"
warning "Base de données: ${POSTGRES_DB:-odoo_prod}"
warning "Fichier de restauration: $BACKUP_FILE"
echo ""
read -p "Êtes-vous sûr de vouloir continuer? (oui/non) " -r
if [[ ! $REPLY =~ ^(oui|OUI|yes|YES)$ ]]; then
    log "Restauration annulée"
    exit 0
fi

log "🚀 Début de la restauration..."

# 1. Arrêter Odoo (mais garder PostgreSQL)
log "⏸️  Arrêt d'Odoo..."
docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" stop odoo

# 2. Créer une sauvegarde de sécurité avant restauration
log "💾 Création d'une sauvegarde de sécurité..."
SAFETY_BACKUP="$PROJECT_DIR/backups/before_restore_$(date +%Y%m%d_%H%M%S).sql.gz"
docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" exec -T postgres \
    pg_dump -U "${POSTGRES_USER:-odoo}" "${POSTGRES_DB:-odoo_prod}" | gzip > "$SAFETY_BACKUP"
log "✅ Sauvegarde de sécurité créée: $SAFETY_BACKUP"

# 3. Supprimer l'ancienne base de données
log "🗑️  Suppression de l'ancienne base de données..."
docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" exec -T postgres \
    psql -U "${POSTGRES_USER:-odoo}" -c "DROP DATABASE IF EXISTS ${POSTGRES_DB:-odoo_prod};"

# 4. Créer une nouvelle base de données
log "🆕 Création d'une nouvelle base de données..."
docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" exec -T postgres \
    psql -U "${POSTGRES_USER:-odoo}" -c "CREATE DATABASE ${POSTGRES_DB:-odoo_prod};"

# 5. Restaurer la sauvegarde
log "📥 Restauration de la sauvegarde..."
gunzip -c "$BACKUP_FILE" | docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" exec -T postgres \
    psql -U "${POSTGRES_USER:-odoo}" "${POSTGRES_DB:-odoo_prod}"

if [ $? -eq 0 ]; then
    log "✅ Base de données restaurée avec succès"
else
    error "Échec de la restauration"
fi

# 6. Redémarrer Odoo
log "▶️  Redémarrage d'Odoo..."
docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" start odoo

# Attendre qu'Odoo démarre
log "⏳ Attente du démarrage d'Odoo (30 secondes)..."
sleep 30

# 7. Vérifier qu'Odoo fonctionne
log "✅ Vérification d'Odoo..."
if curl -s http://localhost:8069 > /dev/null; then
    log "✅ Odoo répond correctement"
else
    warning "⚠️  Odoo ne répond pas encore (peut prendre quelques minutes)"
fi

log "✅ Restauration terminée avec succès!"
log "💾 Sauvegarde de sécurité conservée: $SAFETY_BACKUP"

exit 0

