#!/bin/bash
# Script d'entrée Docker personnalisé pour Odoo SaaS

set -e

# Fonction de log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

# Attendre que PostgreSQL soit prêt
wait_for_postgres() {
    log "Attente de PostgreSQL..."
    until PGPASSWORD="${PASSWORD}" psql -h "${HOST}" -U "${USER}" -d postgres -c '\q' 2>/dev/null; do
        log "PostgreSQL n'est pas encore prêt - attente..."
        sleep 2
    done
    log "PostgreSQL est prêt!"
}

# Vérifier les variables d'environnement
check_env_vars() {
    log "Vérification des variables d'environnement..."
    
    if [ -z "${HOST}" ]; then
        log "ERREUR: Variable HOST non définie"
        exit 1
    fi
    
    if [ -z "${USER}" ]; then
        log "ERREUR: Variable USER non définie"
        exit 1
    fi
    
    if [ -z "${PASSWORD}" ]; then
        log "ERREUR: Variable PASSWORD non définie"
        exit 1
    fi
    
    log "Variables d'environnement OK"
}

# Créer les répertoires nécessaires
create_directories() {
    log "Création des répertoires..."
    mkdir -p /var/lib/odoo/filestore
    mkdir -p /var/lib/odoo/sessions
    mkdir -p /var/lib/odoo/backups
    mkdir -p /var/log/odoo
    log "Répertoires créés"
}

# Définir les permissions
set_permissions() {
    log "Configuration des permissions..."
    chown -R odoo:odoo /var/lib/odoo || true
    chown -R odoo:odoo /var/log/odoo || true
    log "Permissions configurées"
}

# Main
main() {
    log "Démarrage du conteneur Odoo SaaS..."
    
    check_env_vars
    create_directories
    set_permissions
    wait_for_postgres
    
    log "Démarrage d'Odoo..."
    
    # Exécuter la commande Odoo
    exec "$@"
}

# Point d'entrée
if [ "${1:0:1}" = '-' ]; then
    set -- odoo "$@"
fi

if [ "$1" = 'odoo' ]; then
    main "$@"
else
    exec "$@"
fi

