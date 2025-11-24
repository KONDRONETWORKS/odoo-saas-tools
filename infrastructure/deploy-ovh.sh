#!/bin/bash

# 🚀 Script de déploiement automatique - VM OVH Ubuntu 22.04.5
# Auteur: KONDRO Networks
# Date: 2024-11-13
# Usage: bash deploy-ovh.sh

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
PROJECT_DIR="/opt/odoo-saas"
SERVER_IP="10.10.10.40"
LOG_FILE="/tmp/odoo-deploy-$(date +%Y%m%d_%H%M%S).log"

# Fonctions utilitaires
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERREUR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}[ATTENTION]${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}[✓]${NC} $1" | tee -a "$LOG_FILE"
}

# Vérifier si le script est exécuté en tant que root
check_root() {
    if [ "$EUID" -eq 0 ]; then
        warning "Ce script ne doit PAS être exécuté en tant que root"
        warning "Utilisez sudo uniquement quand nécessaire"
        return 1
    fi
    return 0
}

# Banner
show_banner() {
    clear
    echo -e "${BLUE}"
    cat << "EOF"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║     🚀 DÉPLOIEMENT ODOO SAAS - VM OVH                    ║
║                                                          ║
║     📍 Serveur: 10.10.10.40                              ║
║     💻 OS: Ubuntu 22.04.5 LTS                            ║
║     🐳 Docker: Dernière version                          ║
║                                                          ║
║     KONDRO Networks © 2024                               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Étape 1: Mise à jour du système
update_system() {
    log "Étape 1/10: Mise à jour du système..."
    
    sudo apt update | tee -a "$LOG_FILE"
    sudo apt upgrade -y | tee -a "$LOG_FILE"
    sudo apt install -y curl wget git vim nano ufw net-tools htop | tee -a "$LOG_FILE"
    
    success "Système mis à jour"
}

# Étape 2: Configuration du firewall
configure_firewall() {
    log "Étape 2/10: Configuration du firewall..."
    
    sudo ufw --force enable
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 8069/tcp  # Temporaire pour debug
    sudo ufw status | tee -a "$LOG_FILE"
    
    success "Firewall configuré"
}

# Étape 3: Installation Docker
install_docker() {
    log "Étape 3/10: Installation de Docker..."
    
    # Vérifier si Docker est déjà installé
    if command -v docker &> /dev/null; then
        warning "Docker est déjà installé"
        docker --version
        return 0
    fi
    
    # Supprimer les anciennes versions
    sudo apt remove -y docker docker-engine docker.io containerd runc 2>/dev/null || true
    
    # Installer les dépendances
    sudo apt install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release | tee -a "$LOG_FILE"
    
    # Ajouter la clé GPG
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    
    # Ajouter le dépôt
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Installer Docker
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin | tee -a "$LOG_FILE"
    
    # Ajouter l'utilisateur au groupe docker
    sudo usermod -aG docker $USER
    
    # Configurer Docker
    sudo mkdir -p /etc/docker
    cat <<EOL | sudo tee /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2"
}
EOL
    
    sudo systemctl restart docker
    sudo systemctl enable docker
    
    success "Docker installé: $(docker --version)"
    success "Docker Compose: $(docker compose version)"
}

# Étape 4: Créer les répertoires
create_directories() {
    log "Étape 4/10: Création des répertoires..."
    
    sudo mkdir -p "$PROJECT_DIR"
    sudo chown -R $USER:$USER "$PROJECT_DIR"
    
    cd "$PROJECT_DIR"
    mkdir -p filestore backups logs ssl
    chmod -R 755 filestore backups logs ssl
    
    success "Répertoires créés dans $PROJECT_DIR"
}

# Étape 5: Vérifier/cloner le projet
setup_project() {
    log "Étape 5/10: Configuration du projet..."
    
    if [ -d "$PROJECT_DIR/.git" ]; then
        warning "Le projet existe déjà. Mise à jour..."
        cd "$PROJECT_DIR"
        git pull
    else
        warning "Le projet n'est pas encore cloné."
        info "Vous devez copier les fichiers du projet dans $PROJECT_DIR"
        info "Exemple: scp -r /chemin/local/projet/* user@$SERVER_IP:$PROJECT_DIR/"
    fi
    
    success "Projet configuré"
}

# Étape 6: Configuration des variables d'environnement
configure_env() {
    log "Étape 6/10: Configuration des variables d'environnement..."
    
    ENV_FILE="$PROJECT_DIR/.env"
    
    if [ -f "$ENV_FILE" ]; then
        warning "Le fichier .env existe déjà"
        read -p "Voulez-vous le régénérer? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 0
        fi
    fi
    
    # Générer des mots de passe sécurisés
    POSTGRES_PWD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    ODOO_ADMIN_PWD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)
    
    cat > "$ENV_FILE" << EOF
# Configuration générée automatiquement le $(date)
POSTGRES_DB=odoo_prod
POSTGRES_USER=odoo
POSTGRES_PASSWORD=$POSTGRES_PWD

ODOO_ADMIN_PASSWD=$ODOO_ADMIN_PWD
ODOO_DB_PASSWORD=$POSTGRES_PWD

SERVER_IP=$SERVER_IP
DOMAIN_NAME=odoo.local

WORKERS=4
MAX_CRON_THREADS=2
LIMIT_MEMORY_SOFT=2147483648
LIMIT_MEMORY_HARD=2684354560
EOF
    
    chmod 600 "$ENV_FILE"
    
    success "Fichier .env créé avec des mots de passe sécurisés"
    info "Mot de passe PostgreSQL: $POSTGRES_PWD"
    info "Mot de passe Admin Odoo: $ODOO_ADMIN_PWD"
    warning "Sauvegardez ces mots de passe dans un endroit sûr!"
}

# Étape 7: Générer un certificat SSL auto-signé
generate_ssl() {
    log "Étape 7/10: Génération du certificat SSL..."
    
    SSL_DIR="$PROJECT_DIR/ssl"
    
    if [ -f "$SSL_DIR/server.crt" ]; then
        warning "Certificat SSL déjà existant"
        return 0
    fi
    
    sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$SSL_DIR/server.key" \
        -out "$SSL_DIR/server.crt" \
        -subj "/C=FR/ST=IDF/L=Paris/O=KONDRO/CN=$SERVER_IP" \
        2>&1 | tee -a "$LOG_FILE"
    
    sudo chmod 600 "$SSL_DIR/server.key"
    sudo chmod 644 "$SSL_DIR/server.crt"
    
    success "Certificat SSL auto-signé généré"
    warning "Pour la production, utilisez Let's Encrypt: sudo certbot --nginx"
}

# Étape 8: Build des images Docker
build_images() {
    log "Étape 8/10: Construction des images Docker..."
    
    cd "$PROJECT_DIR"
    
    # Charger les variables d'environnement
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs)
    fi
    
    docker compose -f config/docker-compose.ovh.yml build --no-cache 2>&1 | tee -a "$LOG_FILE"
    
    success "Images Docker construites"
}

# Étape 9: Démarrage des services
start_services() {
    log "Étape 9/10: Démarrage des services..."
    
    cd "$PROJECT_DIR"
    
    docker compose -f config/docker-compose.ovh.yml up -d 2>&1 | tee -a "$LOG_FILE"
    
    # Attendre que les services démarrent
    info "Attente du démarrage des services (30 secondes)..."
    sleep 30
    
    # Vérifier l'état des services
    docker compose -f config/docker-compose.ovh.yml ps
    
    success "Services démarrés"
}

# Étape 10: Vérifications finales
verify_installation() {
    log "Étape 10/10: Vérifications finales..."
    
    # Vérifier PostgreSQL
    info "Vérification de PostgreSQL..."
    docker compose -f "$PROJECT_DIR/config/docker-compose.ovh.yml" exec -T postgres pg_isready -U odoo
    
    # Vérifier Odoo
    info "Vérification d'Odoo..."
    sleep 10
    if curl -s http://localhost:8069 > /dev/null; then
        success "Odoo répond sur le port 8069"
    else
        warning "Odoo ne répond pas encore (cela peut prendre quelques minutes)"
    fi
    
    # Vérifier Nginx
    info "Vérification de Nginx..."
    if curl -s http://localhost > /dev/null; then
        success "Nginx répond sur le port 80"
    else
        warning "Nginx ne répond pas"
    fi
    
    success "Vérifications terminées"
}

# Afficher le résumé
show_summary() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}║  ✅ DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!                     ║${NC}"
    echo -e "${GREEN}║                                                          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    info "📍 Accès à l'application:"
    echo "   - HTTP:  http://$SERVER_IP"
    echo "   - HTTPS: https://$SERVER_IP (certificat auto-signé)"
    echo "   - Direct: http://$SERVER_IP:8069"
    echo ""
    info "📝 Fichiers importants:"
    echo "   - Projet: $PROJECT_DIR"
    echo "   - Config: $PROJECT_DIR/.env"
    echo "   - Logs: $LOG_FILE"
    echo "   - Logs Docker: $PROJECT_DIR/logs/"
    echo ""
    info "🔧 Commandes utiles:"
    echo "   - Voir les logs: docker compose -f $PROJECT_DIR/config/docker-compose.ovh.yml logs -f"
    echo "   - Arrêter: docker compose -f $PROJECT_DIR/config/docker-compose.ovh.yml down"
    echo "   - Redémarrer: docker compose -f $PROJECT_DIR/config/docker-compose.ovh.yml restart"
    echo "   - Status: docker compose -f $PROJECT_DIR/config/docker-compose.ovh.yml ps"
    echo ""
    warning "⚠️  N'oubliez pas de:"
    echo "   1. Sauvegarder vos mots de passe"
    echo "   2. Configurer les sauvegardes automatiques"
    echo "   3. Installer Let's Encrypt pour SSL en production"
    echo "   4. Désactiver le port 8069 après les tests: sudo ufw delete allow 8069/tcp"
    echo ""
    info "📖 Documentation complète: $PROJECT_DIR/infrastructure/GUIDE_DEPLOIEMENT_OVH.md"
    echo ""
}

# Fonction principale
main() {
    show_banner
    
    log "Début du déploiement..."
    log "Logs enregistrés dans: $LOG_FILE"
    echo ""
    
    # Vérifications préliminaires
    if ! check_root; then
        error "Exécutez le script sans sudo, le script demandera les permissions quand nécessaire"
    fi
    
    # Confirmation
    warning "Ce script va installer Docker et déployer Odoo SaaS sur ce serveur"
    read -p "Voulez-vous continuer? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        error "Déploiement annulé par l'utilisateur"
    fi
    
    echo ""
    
    # Exécuter les étapes
    update_system
    configure_firewall
    install_docker
    create_directories
    setup_project
    configure_env
    generate_ssl
    
    # Demander si l'utilisateur veut continuer avec Docker
    echo ""
    warning "Les étapes suivantes vont construire et démarrer les conteneurs Docker"
    read -p "Voulez-vous continuer? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        build_images
        start_services
        verify_installation
    else
        info "Vous pouvez démarrer manuellement avec:"
        info "cd $PROJECT_DIR && docker compose -f config/docker-compose.ovh.yml up -d"
    fi
    
    echo ""
    show_summary
    
    success "Déploiement terminé!"
}

# Gestion des erreurs
trap 'error "Une erreur est survenue. Consultez les logs: $LOG_FILE"' ERR

# Exécution
main "$@"

