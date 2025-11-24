#!/bin/bash
# 🔄 Script de Mise à Jour des Références dans les Modules Themes
# Usage: ./scripts/update_theme_references.sh

set -e

THEMES_DIR="$(cd "$(dirname "$0")/../themes" && pwd)"

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Mappings des anciens noms vers les nouveaux
declare -A RENAMES=(
    ["backend_theme_odoo12"]="theme_backend_odoo12"
    ["hue_backend_theme"]="theme_hue_backend"
    ["modern_theme"]="theme_modern"
    ["slife_backend_theme"]="theme_slife_backend"
)

log_info "Mise à jour des références dans les fichiers..."

# Pour chaque module renommé
for old_name in "${!RENAMES[@]}"; do
    new_name="${RENAMES[$old_name]}"
    log_info "Mise à jour: $old_name → $new_name"
    
    # Mettre à jour dans le dossier du module
    if [ -d "$THEMES_DIR/$new_name" ]; then
        # Mettre à jour dans tous les fichiers Python, XML, SCSS, CSS, JS
        find "$THEMES_DIR/$new_name" -type f \( -name "*.py" -o -name "*.xml" -o -name "*.scss" -o -name "*.css" -o -name "*.js" -o -name "*.json" -o -name "__manifest__.py" \) -exec sed -i '' "s|$old_name|$new_name|g" {} \;
        log_success "Références mises à jour dans $new_name"
    fi
done

log_success "Toutes les références ont été mises à jour!"

