#!/bin/bash
# 🔄 Script de Mise à Jour des Versions des Modules vers 18.0.1.0.0
# Usage: ./scripts/update_theme_versions.sh

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Version cible
TARGET_VERSION="18.0.1.0.0"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

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

# Fonction pour mettre à jour la version dans un fichier __manifest__.py
update_manifest_version() {
    local manifest_file="$1"
    local current_version=$(grep -E "^\s*['\"]version['\"]\s*:" "$manifest_file" | head -1 | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/" || echo "")
    
    if [ -z "$current_version" ]; then
        log_warning "Version non trouvée dans $manifest_file"
        return 1
    fi
    
    if [ "$current_version" != "$TARGET_VERSION" ]; then
        log_info "Mise à jour $manifest_file: $current_version -> $TARGET_VERSION"
        
        # Mettre à jour la version (gère les guillemets simples et doubles)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' -E "s/(['\"]version['\"]\s*:\s*['\"])[^'\"]+(['\"])/\1${TARGET_VERSION}\2/" "$manifest_file"
        else
            # Linux
            sed -i -E "s/(['\"]version['\"]\s*:\s*['\"])[^'\"]+(['\"])/\1${TARGET_VERSION}\2/" "$manifest_file"
        fi
        
        log_success "Version mise à jour dans $manifest_file"
        return 0
    else
        log_info "Version déjà à jour dans $manifest_file"
        return 0
    fi
}

# Fonction pour créer un __manifest__.py depuis __openerp__.py
convert_openerp_to_manifest() {
    local openerp_file="$1"
    local manifest_file="$(dirname "$openerp_file")/__manifest__.py"
    
    if [ -f "$manifest_file" ]; then
        log_info "__manifest__.py existe déjà pour $(dirname "$openerp_file")"
        return 0
    fi
    
    log_info "Conversion de $openerp_file vers __manifest__.py"
    
    # Créer __manifest__.py avec la version mise à jour
    cat > "$manifest_file" << EOF
# -*- coding: utf-8 -*-
{
    'version': '${TARGET_VERSION}',
EOF
    
    # Copier le reste du contenu (sans la version)
    grep -v "version" "$openerp_file" | sed '1d' | sed '$d' >> "$manifest_file"
    
    log_success "__manifest__.py créé pour $(dirname "$openerp_file")"
}

# Trouver tous les fichiers __manifest__.py
log_info "Recherche des fichiers __manifest__.py..."
MANIFEST_FILES=$(find "$PROJECT_DIR" -name "__manifest__.py" -type f | grep -v "__pycache__" | grep -v ".git")

# Trouver les fichiers __openerp__.py (ancien format)
log_info "Recherche des fichiers __openerp__.py (ancien format)..."
OPENERP_FILES=$(find "$PROJECT_DIR" -name "__openerp__.py" -type f | grep -v "__pycache__" | grep -v ".git")

# Compteurs
UPDATED=0
ALREADY_UPDATED=0
CONVERTED=0
ERRORS=0

# Mettre à jour tous les __manifest__.py
log_info "Mise à jour des versions dans les __manifest__.py..."
for manifest_file in $MANIFEST_FILES; do
    if update_manifest_version "$manifest_file"; then
        if grep -q "$TARGET_VERSION" "$manifest_file"; then
            if grep -E "^\s*['\"]version['\"]\s*:\s*['\"]${TARGET_VERSION}['\"]" "$manifest_file" > /dev/null; then
                ((ALREADY_UPDATED++))
            else
                ((UPDATED++))
            fi
        fi
    else
        ((ERRORS++))
    fi
done

# Convertir les __openerp__.py
log_info "Conversion des __openerp__.py vers __manifest__.py..."
for openerp_file in $OPENERP_FILES; do
    if convert_openerp_to_manifest "$openerp_file"; then
        ((CONVERTED++))
    else
        ((ERRORS++))
    fi
done

# Résumé
echo ""
log_info "=========================================="
log_info "Résumé de la mise à jour"
log_info "=========================================="
log_success "Versions mises à jour: $UPDATED"
log_info "Versions déjà à jour: $ALREADY_UPDATED"
log_success "Fichiers convertis (__openerp__ -> __manifest__): $CONVERTED"
if [ $ERRORS -gt 0 ]; then
    log_error "Erreurs: $ERRORS"
fi
log_info "Version cible: $TARGET_VERSION"
log_info "=========================================="

if [ $ERRORS -eq 0 ]; then
    log_success "✅ Mise à jour terminée avec succès!"
    exit 0
else
    log_error "❌ Des erreurs sont survenues"
    exit 1
fi

