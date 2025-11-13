#!/bin/bash
# Script simple pour démarrer/arrêter le service SaaS
# 
# Ce script utilise docker-compose.simple.yml qui est la configuration
# principale pour le développement local avec tous les modules.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Fichier principal à utiliser (évite les confusions)
COMPOSE_FILE="$PROJECT_DIR/config/docker-compose.simple.yml"

cd "$PROJECT_DIR"

case "${1:-start}" in
    start)
        echo "🚀 Démarrage du service SaaS..."
        docker compose -f "$COMPOSE_FILE" up -d
        echo ""
        echo "⏳ Attente du démarrage (30 secondes)..."
        sleep 30
        echo ""
        echo "✅ Service démarré !"
        echo ""
        echo "📊 État des conteneurs:"
        docker compose -f "$COMPOSE_FILE" ps
        echo ""
        echo "🌐 Accès:"
        echo "   - Interface Odoo: http://localhost:8069"
        echo "   - Portail SaaS: http://localhost:8069/web?db=saas-portal-18.local"
        ;;
    stop)
        echo "🛑 Arrêt du service SaaS..."
        docker compose -f "$COMPOSE_FILE" stop
        echo "✅ Service arrêté"
        ;;
    restart)
        echo "🔄 Redémarrage du service SaaS..."
        docker compose -f "$COMPOSE_FILE" restart
        echo "✅ Service redémarré"
        ;;
    down)
        echo "🗑️  Arrêt et suppression des conteneurs..."
        docker compose -f "$COMPOSE_FILE" down
        echo "✅ Conteneurs supprimés (données conservées)"
        ;;
    status)
        echo "📊 État du service SaaS:"
        docker compose -f "$COMPOSE_FILE" ps
        echo ""
        echo "📋 Conteneurs actifs:"
        docker ps --format "table {{.Names}}\t{{.Status}}" | grep saas || echo "Aucun conteneur actif"
        ;;
    logs)
        echo "📝 Logs du service SaaS:"
        docker compose -f "$COMPOSE_FILE" logs -f
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|down|status|logs}"
        echo ""
        echo "Commandes:"
        echo "  start   - Démarrer le service"
        echo "  stop    - Arrêter le service"
        echo "  restart - Redémarrer le service"
        echo "  down    - Arrêter et supprimer les conteneurs"
        echo "  status  - Voir l'état du service"
        echo "  logs    - Voir les logs en temps réel"
        exit 1
        ;;
esac

