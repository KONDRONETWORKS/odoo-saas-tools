#!/bin/bash

# 🔧 Script de maintenance - Odoo SaaS
# Usage: ./maintenance.sh [start|stop|restart|status|logs|update]

set -e

PROJECT_DIR="/opt/odoo-saas"
COMPOSE_FILE="$PROJECT_DIR/config/docker-compose.ovh.yml"

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERREUR]${NC} $1"
    exit 1
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Fonction d'aide
show_help() {
    cat << EOF
🔧 Script de maintenance Odoo SaaS

Usage: $0 [commande]

Commandes disponibles:
  start       Démarrer tous les services
  stop        Arrêter tous les services
  restart     Redémarrer tous les services
  status      Afficher l'état des services
  logs        Afficher les logs en temps réel
  update      Mettre à jour le code et redémarrer
  backup      Effectuer une sauvegarde complète
  clean       Nettoyer les ressources Docker inutilisées
  stats       Afficher les statistiques d'utilisation
  health      Vérifier la santé des services
  shell       Ouvrir un shell dans le conteneur Odoo
  psql        Ouvrir PostgreSQL en ligne de commande
  help        Afficher cette aide

Exemples:
  $0 start
  $0 logs
  $0 backup
  $0 health

EOF
}

# Vérifier que le projet existe
check_project() {
    if [ ! -d "$PROJECT_DIR" ]; then
        error "Projet non trouvé dans $PROJECT_DIR"
    fi
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        error "Fichier docker-compose non trouvé: $COMPOSE_FILE"
    fi
}

# Démarrer les services
cmd_start() {
    log "🚀 Démarrage des services..."
    docker compose -f "$COMPOSE_FILE" up -d
    log "✅ Services démarrés"
}

# Arrêter les services
cmd_stop() {
    log "⏸️  Arrêt des services..."
    docker compose -f "$COMPOSE_FILE" down
    log "✅ Services arrêtés"
}

# Redémarrer les services
cmd_restart() {
    log "🔄 Redémarrage des services..."
    docker compose -f "$COMPOSE_FILE" restart
    log "✅ Services redémarrés"
}

# Afficher le statut
cmd_status() {
    log "📊 État des services:"
    docker compose -f "$COMPOSE_FILE" ps
    echo ""
    info "Utilisation des ressources:"
    docker stats --no-stream
}

# Afficher les logs
cmd_logs() {
    log "📋 Logs en temps réel (Ctrl+C pour quitter):"
    docker compose -f "$COMPOSE_FILE" logs -f --tail=100
}

# Mettre à jour
cmd_update() {
    log "🔄 Mise à jour du code..."
    
    cd "$PROJECT_DIR"
    
    # Sauvegarder avant la mise à jour
    info "💾 Sauvegarde avant mise à jour..."
    bash "$PROJECT_DIR/scripts/backup.sh" pre-update 2>/dev/null || true
    
    # Mettre à jour le code
    if [ -d .git ]; then
        git pull
    else
        error "Ce n'est pas un dépôt Git"
    fi
    
    # Reconstruire les images
    log "🏗️  Reconstruction des images..."
    docker compose -f "$COMPOSE_FILE" build --no-cache
    
    # Redémarrer
    log "🔄 Redémarrage..."
    docker compose -f "$COMPOSE_FILE" down
    docker compose -f "$COMPOSE_FILE" up -d
    
    log "✅ Mise à jour terminée"
}

# Effectuer une sauvegarde
cmd_backup() {
    log "💾 Lancement de la sauvegarde..."
    bash "$PROJECT_DIR/scripts/backup.sh" manual
}

# Nettoyer Docker
cmd_clean() {
    log "🧹 Nettoyage de Docker..."
    
    info "Suppression des conteneurs arrêtés..."
    docker container prune -f
    
    info "Suppression des images inutilisées..."
    docker image prune -f
    
    info "Suppression des volumes inutilisés..."
    docker volume prune -f
    
    info "Suppression des réseaux inutilisés..."
    docker network prune -f
    
    log "✅ Nettoyage terminé"
    
    info "Espace disque libéré:"
    docker system df
}

# Statistiques
cmd_stats() {
    log "📊 Statistiques du système:"
    echo ""
    
    info "=== Services Docker ==="
    docker compose -f "$COMPOSE_FILE" ps
    echo ""
    
    info "=== Utilisation CPU/Mémoire ==="
    docker stats --no-stream
    echo ""
    
    info "=== Espace disque ==="
    df -h | grep -E "Filesystem|/$|/opt"
    echo ""
    
    info "=== Taille des backups ==="
    du -sh "$PROJECT_DIR/backups" 2>/dev/null || echo "Aucune sauvegarde"
    echo ""
    
    info "=== Logs ==="
    du -sh "$PROJECT_DIR/logs" 2>/dev/null || echo "Aucun log"
}

# Vérifier la santé
cmd_health() {
    log "🏥 Vérification de la santé des services..."
    echo ""
    
    # PostgreSQL
    info "PostgreSQL:"
    if docker compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U odoo; then
        echo -e "${GREEN}✅ PostgreSQL OK${NC}"
    else
        echo -e "${RED}❌ PostgreSQL KO${NC}"
    fi
    echo ""
    
    # Odoo
    info "Odoo:"
    if curl -sf http://localhost:8069 > /dev/null; then
        echo -e "${GREEN}✅ Odoo OK (port 8069)${NC}"
    else
        echo -e "${RED}❌ Odoo KO${NC}"
    fi
    echo ""
    
    # Nginx
    info "Nginx:"
    if curl -sf http://localhost > /dev/null; then
        echo -e "${GREEN}✅ Nginx OK (port 80)${NC}"
    else
        echo -e "${RED}❌ Nginx KO${NC}"
    fi
    echo ""
    
    # Espace disque
    info "Espace disque:"
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -lt 80 ]; then
        echo -e "${GREEN}✅ Espace disque OK ($DISK_USAGE%)${NC}"
    else
        echo -e "${YELLOW}⚠️  Espace disque faible ($DISK_USAGE%)${NC}"
    fi
    echo ""
    
    # Mémoire
    info "Mémoire:"
    FREE_MEM=$(free -m | awk 'NR==2 {printf "%.0f", $7/$2*100}')
    if [ "$FREE_MEM" -gt 20 ]; then
        echo -e "${GREEN}✅ Mémoire OK (${FREE_MEM}% disponible)${NC}"
    else
        echo -e "${YELLOW}⚠️  Mémoire faible (${FREE_MEM}% disponible)${NC}"
    fi
}

# Shell Odoo
cmd_shell() {
    log "🐚 Ouverture d'un shell dans le conteneur Odoo..."
    docker compose -f "$COMPOSE_FILE" exec odoo bash
}

# PostgreSQL
cmd_psql() {
    log "🗄️  Ouverture de PostgreSQL..."
    docker compose -f "$COMPOSE_FILE" exec postgres psql -U odoo
}

# Main
check_project

case "${1:-help}" in
    start)
        cmd_start
        ;;
    stop)
        cmd_stop
        ;;
    restart)
        cmd_restart
        ;;
    status)
        cmd_status
        ;;
    logs)
        cmd_logs
        ;;
    update)
        cmd_update
        ;;
    backup)
        cmd_backup
        ;;
    clean)
        cmd_clean
        ;;
    stats)
        cmd_stats
        ;;
    health)
        cmd_health
        ;;
    shell)
        cmd_shell
        ;;
    psql)
        cmd_psql
        ;;
    help|*)
        show_help
        ;;
esac

exit 0

