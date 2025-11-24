#!/bin/bash
# 🚀 Script de Déploiement Odoo SaaS Tools
# Pour Ubuntu 22.04.5 sur VM OVH (10.10.10.40)
# Usage: sudo ./deploy-ubuntu-vm.sh

set -e

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables de configuration
VM_IP="10.10.10.40"
PROJECT_DIR="/opt/odoo-saas-tools"
ODOO_USER="odoo"
POSTGRES_USER="odoo"
DOMAIN_NAME="${DOMAIN_NAME:-saas.local}"  # À modifier selon votre domaine
EMAIL="${EMAIL:-admin@example.com}"  # Pour Let's Encrypt

# Fonction de logging
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérification des privilèges root
check_root() {
    if [ "$EUID" -ne 0 ]; then 
        log_error "Ce script doit être exécuté en tant que root (utilisez sudo)"
        exit 1
    fi
}

# Mise à jour du système
update_system() {
    log_info "Mise à jour du système..."
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get upgrade -y
    log_success "Système mis à jour"
}

# Installation des dépendances système
install_dependencies() {
    log_info "Installation des dépendances système..."
    
    apt-get install -y \
        curl \
        wget \
        git \
        build-essential \
        python3.11 \
        python3.11-pip \
        python3.11-venv \
        python3.11-dev \
        libpq-dev \
        postgresql-client \
        nginx \
        certbot \
        python3-certbot-nginx \
        ufw \
        htop \
        unzip \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg \
        lsb-release
    
    log_success "Dépendances installées"
}

# Installation de Docker et Docker Compose
install_docker() {
    log_info "Installation de Docker..."
    
    # Vérifier si Docker est déjà installé
    if command -v docker &> /dev/null; then
        log_warning "Docker est déjà installé"
        return
    fi
    
    # Installer Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    
    # Installer Docker Compose plugin
    apt-get install -y docker-compose-plugin
    
    # Démarrer Docker
    systemctl enable docker
    systemctl start docker
    
    log_success "Docker installé et démarré"
}

# Configuration du firewall
configure_firewall() {
    log_info "Configuration du firewall (UFW)..."
    
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
    
    log_success "Firewall configuré"
}

# Configuration PostgreSQL
setup_postgresql() {
    log_info "Configuration de PostgreSQL..."
    
    # Installer PostgreSQL si pas déjà installé
    if ! command -v psql &> /dev/null; then
        apt-get install -y postgresql postgresql-contrib
    fi
    
    # Générer un mot de passe sécurisé
    if [ -z "$POSTGRES_PASSWORD" ]; then
        POSTGRES_PASSWORD=$(openssl rand -hex 32)
        log_info "Mot de passe PostgreSQL généré: $POSTGRES_PASSWORD"
        echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> /root/.odoo-deploy.env
    fi
    
    # Créer l'utilisateur et la base de données
    sudo -u postgres psql -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';" || true
    sudo -u postgres psql -c "ALTER USER $POSTGRES_USER CREATEDB;" || true
    sudo -u postgres psql -c "CREATE DATABASE odoo OWNER $POSTGRES_USER;" || true
    
    # Configuration PostgreSQL pour accepter les connexions Docker
    PG_VERSION=$(psql --version | grep -oP '\d+' | head -1)
    PG_CONF="/etc/postgresql/${PG_VERSION}/main/postgresql.conf"
    PG_HBA="/etc/postgresql/${PG_VERSION}/main/pg_hba.conf"
    
    if [ -f "$PG_CONF" ]; then
        sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"
    fi
    
    if [ -f "$PG_HBA" ]; then
        if ! grep -q "host    all             all             172.17.0.0/16           md5" "$PG_HBA"; then
            echo "host    all             all             172.17.0.0/16           md5" >> "$PG_HBA"
        fi
    fi
    
    systemctl restart postgresql || true
    
    log_success "PostgreSQL configuré"
}

# Création de l'utilisateur Odoo
create_odoo_user() {
    log_info "Création de l'utilisateur $ODOO_USER..."
    
    if id "$ODOO_USER" &>/dev/null; then
        log_warning "L'utilisateur $ODOO_USER existe déjà"
    else
        useradd -m -s /bin/bash -G docker $ODOO_USER
        log_success "Utilisateur $ODOO_USER créé"
    fi
}

# Clonage ou mise à jour du projet
setup_project() {
    log_info "Configuration du projet dans $PROJECT_DIR..."
    
    if [ -d "$PROJECT_DIR" ]; then
        log_warning "Le répertoire $PROJECT_DIR existe déjà"
        cd "$PROJECT_DIR"
        sudo -u $ODOO_USER git pull || true
    else
        mkdir -p "$PROJECT_DIR"
        chown $ODOO_USER:$ODOO_USER "$PROJECT_DIR"
        
        # Si le projet est déjà présent localement, le copier
        if [ -d "/root/odoo-saas-tools" ] || [ -d "$(dirname $0)/../.." ]; then
            log_info "Copie du projet local..."
            SRC_DIR=$(find /root -name "odoo-saas-tools" -type d 2>/dev/null | head -1)
            if [ -z "$SRC_DIR" ]; then
                SRC_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
            fi
            if [ -d "$SRC_DIR" ]; then
                cp -r "$SRC_DIR"/* "$PROJECT_DIR/" 2>/dev/null || true
                chown -R $ODOO_USER:$ODOO_USER "$PROJECT_DIR"
            fi
        else
            log_info "Clonage depuis GitHub..."
            sudo -u $ODOO_USER git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git "$PROJECT_DIR" || {
                log_error "Impossible de cloner le projet. Vérifiez votre connexion internet."
                exit 1
            }
        fi
    fi
    
    log_success "Projet configuré"
}

# Configuration des variables d'environnement
setup_env_file() {
    log_info "Configuration du fichier .env..."
    
    ENV_FILE="$PROJECT_DIR/.env"
    
    if [ ! -f "$ENV_FILE" ]; then
        cat > "$ENV_FILE" << EOF
# Configuration Odoo SaaS Tools - Production
# VM: $VM_IP
# Date: $(date)

# PostgreSQL
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_USER=$POSTGRES_USER
POSTGRES_DB=odoo

# Odoo
ODOO_ADMIN_PASSWD=$(openssl rand -hex 32)
ODOO_DB_PASSWORD=$POSTGRES_PASSWORD

# Domaine
DOMAIN_NAME=$DOMAIN_NAME
EMAIL=$EMAIL

# Sécurité
LIST_DB=False
PROXY_MODE=True

# Workers (ajuster selon les ressources)
WORKERS=4
MAX_CRON_THREADS=2

# Limites mémoire (en octets)
LIMIT_MEMORY_SOFT=2147483648
LIMIT_MEMORY_HARD=2684354560
EOF
        chown $ODOO_USER:$ODOO_USER "$ENV_FILE"
        chmod 600 "$ENV_FILE"
        log_success "Fichier .env créé"
    else
        log_warning "Le fichier .env existe déjà"
    fi
}

# Configuration Nginx
setup_nginx() {
    log_info "Configuration de Nginx..."
    
    NGINX_CONF="/etc/nginx/sites-available/odoo-saas"
    
    cat > "$NGINX_CONF" << EOF
# Configuration Nginx pour Odoo SaaS Tools
# VM: $VM_IP

upstream odoo {
    server 127.0.0.1:8069;
}

upstream odoochat {
    server 127.0.0.1:8072;
}

# Redirection HTTP vers HTTPS
server {
    listen 80;
    server_name $DOMAIN_NAME;
    
    # Pour Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }
    
    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# Configuration HTTPS
server {
    listen 443 ssl http2;
    server_name $DOMAIN_NAME;
    
    # Certificats SSL (seront générés par Certbot)
    # ssl_certificate /etc/letsencrypt/live/$DOMAIN_NAME/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/$DOMAIN_NAME/privkey.pem;
    
    # Configuration SSL recommandée
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Logs
    access_log /var/log/nginx/odoo-access.log;
    error_log /var/log/nginx/odoo-error.log;
    
    # Augmenter les limites
    client_max_body_size 100M;
    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;
    
    # Proxy vers Odoo
    location / {
        proxy_pass http://odoo;
        proxy_redirect off;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Longpolling
    location /longpolling {
        proxy_pass http://odochat;
        proxy_redirect off;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Cache pour les assets statiques
    location ~* /web/static/ {
        proxy_cache_valid 200 60m;
        proxy_buffering on;
        expires 864000;
        proxy_pass http://odoo;
    }
}
EOF
    
    # Activer la configuration
    ln -sf "$NGINX_CONF" /etc/nginx/sites-enabled/odoo-saas
    rm -f /etc/nginx/sites-enabled/default
    
    # Tester la configuration
    nginx -t
    
    log_success "Nginx configuré"
}

# Démarrage des services Docker
start_services() {
    log_info "Démarrage des services Docker..."
    
    cd "$PROJECT_DIR"
    
    # Charger les variables d'environnement
    if [ -f ".env" ]; then
        set -a
        source .env
        set +a
    fi
    
    # Démarrer avec docker-compose
    if [ -f "config/docker-compose.ubuntu-vm.yml" ]; then
        docker compose -f config/docker-compose.ubuntu-vm.yml up -d
    elif [ -f "config/docker-compose.prod.yml" ]; then
        log_warning "Utilisation de docker-compose.prod.yml (ubuntu-vm.yml non trouvé)"
        docker compose -f config/docker-compose.prod.yml up -d
    else
        log_error "Aucun fichier docker-compose trouvé"
        exit 1
    fi
    
    log_success "Services démarrés"
}

# Configuration SSL avec Let's Encrypt
setup_ssl() {
    if [ "$DOMAIN_NAME" != "saas.local" ] && [ -n "$EMAIL" ]; then
        log_info "Configuration SSL avec Let's Encrypt..."
        
        certbot --nginx -d "$DOMAIN_NAME" --non-interactive --agree-tos --email "$EMAIL" || {
            log_warning "Impossible d'obtenir le certificat SSL. Configurez-le manuellement plus tard."
        }
        
        # Redémarrer Nginx
        systemctl restart nginx
        
        log_success "SSL configuré"
    else
        log_warning "Domaine non configuré, SSL ignoré"
    fi
}

# Affichage des informations finales
show_summary() {
    log_success "Déploiement terminé !"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📋 INFORMATIONS DE DÉPLOIEMENT"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📍 Adresse VM:        $VM_IP"
    echo "🌐 Domaine:           $DOMAIN_NAME"
    echo "📁 Répertoire:        $PROJECT_DIR"
    echo "👤 Utilisateur:       $ODOO_USER"
    echo ""
    echo "🔐 MOTS DE PASSE:"
    echo "   PostgreSQL:        $POSTGRES_PASSWORD"
    if [ -f "$PROJECT_DIR/.env" ]; then
        echo "   Odoo Admin:        $(grep ODOO_ADMIN_PASSWD "$PROJECT_DIR/.env" | cut -d'=' -f2)"
    fi
    echo ""
    echo "📝 Les mots de passe sont sauvegardés dans:"
    echo "   - $PROJECT_DIR/.env"
    echo "   - /root/.odoo-deploy.env"
    echo ""
    echo "🚀 PROCHAINES ÉTAPES:"
    echo "   1. Accédez à Odoo: http://$VM_IP:8069 ou https://$DOMAIN_NAME"
    echo "   2. Installez les modules SaaS dans l'ordre:"
    echo "      - saas_base, saas_portal, saas_server, saas_client"
    echo "   3. Configurez les paramètres dans Odoo"
    echo ""
    echo "📊 COMMANDES UTILES:"
    echo "   - Voir les logs:    docker compose -f $PROJECT_DIR/config/docker-compose.ubuntu-vm.yml logs -f"
    echo "   - Redémarrer:       docker compose -f $PROJECT_DIR/config/docker-compose.ubuntu-vm.yml restart"
    echo "   - Arrêter:          docker compose -f $PROJECT_DIR/config/docker-compose.ubuntu-vm.yml down"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Fonction principale
main() {
    log_info "🚀 Déploiement Odoo SaaS Tools sur Ubuntu 22.04.5"
    log_info "VM: $VM_IP"
    echo ""
    
    check_root
    update_system
    install_dependencies
    install_docker
    configure_firewall
    setup_postgresql
    create_odoo_user
    setup_project
    setup_env_file
    setup_nginx
    start_services
    
    # Attendre que les services soient prêts
    log_info "Attente du démarrage des services (30 secondes)..."
    sleep 30
    
    setup_ssl
    show_summary
}

# Exécution
main "$@"

