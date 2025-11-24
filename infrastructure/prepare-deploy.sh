#!/bin/bash

# 📦 Script de préparation pour le déploiement
# Ce script prépare les fichiers nécessaires pour le transfert vers le serveur OVH

set -e

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

info() {
    echo -e "${BLUE}[→]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Banner
cat << "EOF"
╔════════════════════════════════════════════╗
║  📦 PRÉPARATION DÉPLOIEMENT OVH           ║
║  Serveur: 10.10.10.40                     ║
╚════════════════════════════════════════════╝
EOF

echo ""

# Répertoire du projet
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

log "Répertoire du projet: $PROJECT_ROOT"

# 1. Rendre les scripts exécutables
log "Étape 1/5: Configuration des permissions des scripts..."

chmod +x infrastructure/deploy-ovh.sh
chmod +x infrastructure/prepare-deploy.sh
chmod +x scripts/backup.sh
chmod +x scripts/restore.sh
chmod +x scripts/maintenance.sh
chmod +x config/docker-entrypoint.sh

info "✓ Permissions configurées"

# 2. Vérifier les fichiers essentiels
log "Étape 2/5: Vérification des fichiers essentiels..."

REQUIRED_FILES=(
    "config/docker-compose.ovh.yml"
    "config/nginx.ovh.conf"
    "config/Dockerfile"
    "config/docker-entrypoint.sh"
    "config/env.template"
    "infrastructure/deploy-ovh.sh"
    "infrastructure/GUIDE_DEPLOIEMENT_OVH.md"
    "scripts/backup.sh"
    "scripts/restore.sh"
    "scripts/maintenance.sh"
    "requirements.txt"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        info "✓ $file"
    else
        warning "✗ $file (MANQUANT)"
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -ne 0 ]; then
    echo ""
    warning "⚠️  Certains fichiers sont manquants. Le déploiement pourrait échouer."
    echo ""
fi

# 3. Créer une archive pour le transfert
log "Étape 3/5: Création d'une archive pour le transfert..."

ARCHIVE_NAME="odoo-saas-deploy-$(date +%Y%m%d_%H%M%S).tar.gz"
ARCHIVE_DIR="/tmp/odoo-deploy"

mkdir -p "$ARCHIVE_DIR"

# Fichiers à inclure dans l'archive
tar -czf "$ARCHIVE_DIR/$ARCHIVE_NAME" \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='filestore/*' \
    --exclude='backups/*' \
    --exclude='logs/*' \
    --exclude='.env' \
    --exclude='.venv' \
    --exclude='node_modules' \
    --exclude='*.log' \
    config/ \
    infrastructure/ \
    scripts/ \
    kondro/ \
    saas_*/ \
    requirements.txt \
    README.md \
    LICENSE \
    2>/dev/null

ARCHIVE_SIZE=$(du -h "$ARCHIVE_DIR/$ARCHIVE_NAME" | cut -f1)
info "✓ Archive créée: $ARCHIVE_DIR/$ARCHIVE_NAME ($ARCHIVE_SIZE)"

# 4. Générer les commandes de déploiement
log "Étape 4/5: Génération des commandes de déploiement..."

COMMANDS_FILE="$ARCHIVE_DIR/COMMANDES_DEPLOIEMENT.txt"

cat > "$COMMANDS_FILE" << 'EOF'
═══════════════════════════════════════════════════════════
  COMMANDES POUR LE DÉPLOIEMENT SUR LE SERVEUR OVH
═══════════════════════════════════════════════════════════

1️⃣  TRANSFÉRER L'ARCHIVE VERS LE SERVEUR
────────────────────────────────────────────────────────────

Sur votre machine locale, exécutez :

    scp /tmp/odoo-deploy/odoo-saas-deploy-*.tar.gz root@10.10.10.40:/tmp/

Ou si vous avez un utilisateur non-root :

    scp /tmp/odoo-deploy/odoo-saas-deploy-*.tar.gz user@10.10.10.40:/tmp/


2️⃣  SE CONNECTER AU SERVEUR
────────────────────────────────────────────────────────────

    ssh root@10.10.10.40

Ou avec un utilisateur :

    ssh user@10.10.10.40


3️⃣  EXTRAIRE L'ARCHIVE SUR LE SERVEUR
────────────────────────────────────────────────────────────

    sudo mkdir -p /opt/odoo-saas
    sudo tar -xzf /tmp/odoo-saas-deploy-*.tar.gz -C /opt/odoo-saas
    sudo chown -R $USER:$USER /opt/odoo-saas


4️⃣  LANCER LE SCRIPT D'INSTALLATION
────────────────────────────────────────────────────────────

    cd /opt/odoo-saas
    bash infrastructure/deploy-ovh.sh

Le script va :
- Mettre à jour le système
- Installer Docker et Docker Compose
- Configurer le firewall
- Générer les certificats SSL
- Créer les fichiers de configuration (.env)
- Construire et démarrer les conteneurs


5️⃣  VÉRIFIER L'INSTALLATION
────────────────────────────────────────────────────────────

    # Vérifier les conteneurs
    docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml ps

    # Vérifier les logs
    docker compose -f /opt/odoo-saas/config/docker-compose.ovh.yml logs -f

    # Vérifier la santé des services
    bash /opt/odoo-saas/scripts/maintenance.sh health


6️⃣  ACCÉDER À L'APPLICATION
────────────────────────────────────────────────────────────

Dans votre navigateur :

    - HTTP:  http://10.10.10.40
    - HTTPS: https://10.10.10.40
    - Direct: http://10.10.10.40:8069


7️⃣  SCRIPTS DE MAINTENANCE DISPONIBLES
────────────────────────────────────────────────────────────

    # Maintenance générale
    bash /opt/odoo-saas/scripts/maintenance.sh [start|stop|restart|status|logs|health]

    # Sauvegardes
    bash /opt/odoo-saas/scripts/backup.sh [daily|weekly|monthly]

    # Restauration
    bash /opt/odoo-saas/scripts/restore.sh /path/to/backup.sql.gz


8️⃣  CONFIGURATION DES SAUVEGARDES AUTOMATIQUES
────────────────────────────────────────────────────────────

Ajouter au crontab :

    crontab -e

Puis ajouter :

    # Backup quotidien à 2h du matin
    0 2 * * * /opt/odoo-saas/scripts/backup.sh daily

    # Backup hebdomadaire le dimanche à 3h
    0 3 * * 0 /opt/odoo-saas/scripts/backup.sh weekly

    # Backup mensuel le 1er du mois à 4h
    0 4 1 * * /opt/odoo-saas/scripts/backup.sh monthly


9️⃣  SÉCURISATION (APRÈS LES TESTS)
────────────────────────────────────────────────────────────

    # Désactiver l'accès direct au port 8069
    sudo ufw delete allow 8069/tcp

    # Installer Let's Encrypt pour SSL
    sudo apt install -y certbot python3-certbot-nginx
    sudo certbot --nginx -d votre-domaine.com

    # Configurer fail2ban
    sudo apt install -y fail2ban
    sudo systemctl enable fail2ban
    sudo systemctl start fail2ban


🔟  DOCUMENTATION COMPLÈTE
────────────────────────────────────────────────────────────

Consultez la documentation détaillée :

    cat /opt/odoo-saas/infrastructure/GUIDE_DEPLOIEMENT_OVH.md


═══════════════════════════════════════════════════════════
  SUPPORT
═══════════════════════════════════════════════════════════

En cas de problème :
- Email: apps@itexperts4africa.com
- Logs: /opt/odoo-saas/logs/
- Documentation: /opt/odoo-saas/infrastructure/

═══════════════════════════════════════════════════════════
EOF

info "✓ Fichier de commandes créé: $COMMANDS_FILE"

# 5. Afficher le résumé
log "Étape 5/5: Résumé de la préparation"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ PRÉPARATION TERMINÉE                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
info "📦 Archive prête pour le transfert:"
echo "   $ARCHIVE_DIR/$ARCHIVE_NAME"
echo ""
info "📋 Commandes de déploiement:"
echo "   $COMMANDS_FILE"
echo ""
info "🚀 Prochaines étapes:"
echo ""
echo "   1. Transférez l'archive vers le serveur:"
echo "      scp $ARCHIVE_DIR/$ARCHIVE_NAME root@10.10.10.40:/tmp/"
echo ""
echo "   2. Connectez-vous au serveur:"
echo "      ssh root@10.10.10.40"
echo ""
echo "   3. Extrayez et déployez:"
echo "      sudo mkdir -p /opt/odoo-saas"
echo "      sudo tar -xzf /tmp/$(basename $ARCHIVE_NAME) -C /opt/odoo-saas"
echo "      cd /opt/odoo-saas && bash infrastructure/deploy-ovh.sh"
echo ""
info "📖 Documentation complète disponible dans le fichier:"
echo "   $COMMANDS_FILE"
echo ""

# Copier aussi les commandes dans le terminal pour faciliter le copier-coller
warning "💡 TIP: Consultez le fichier COMMANDES_DEPLOIEMENT.txt pour toutes les étapes détaillées"

exit 0

