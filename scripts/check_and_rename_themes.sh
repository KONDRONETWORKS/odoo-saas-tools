#!/bin/bash
# 🔍 Script de Vérification et Renommage des Modules Themes
# Usage: ./scripts/check_and_rename_themes.sh

set -e

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

THEMES_DIR="$(cd "$(dirname "$0")/../themes" && pwd)"
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

# Fonction pour extraire le nom technique du module depuis __manifest__.py
get_module_technical_name() {
    local manifest_file="$1"
    local dir_name=$(basename "$(dirname "$manifest_file")")
    
    # Si c'est un sous-module dans theme_crest, retourner le nom du dossier parent
    if [[ "$manifest_file" == *"theme_crest"* ]]; then
        echo "$dir_name"
    else
        echo "$dir_name"
    fi
}

# Fonction pour vérifier la cohérence nom dossier / nom module
check_module_consistency() {
    local theme_dir="$1"
    local manifest_file="$theme_dir/__manifest__.py"
    local openerp_file="$theme_dir/__openerp__.py"
    
    if [ ! -f "$manifest_file" ] && [ ! -f "$openerp_file" ]; then
        log_warning "Aucun manifest trouvé dans $theme_dir"
        return 1
    fi
    
    local dir_name=$(basename "$theme_dir")
    local manifest_name=""
    
    if [ -f "$manifest_file" ]; then
        # Extraire le nom depuis __manifest__.py
        manifest_name=$(grep -E "^\s*['\"]name['\"]\s*:" "$manifest_file" | head -1 | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/" || echo "")
    elif [ -f "$openerp_file" ]; then
        manifest_name=$(grep -E "^\s*['\"]name['\"]\s*:" "$openerp_file" | head -1 | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/" || echo "")
    fi
    
    if [ -z "$manifest_name" ]; then
        log_warning "Nom non trouvé dans le manifest de $theme_dir"
        return 1
    fi
    
    # Générer le nom technique attendu depuis le nom du manifest
    local expected_tech_name=$(echo "$manifest_name" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g' | sed 's/__*/_/g' | sed 's/^_\|_$//g')
    
    # Liste des correspondances spéciales
    case "$dir_name" in
        "theme_crest-18.0.1.0.2")
            expected_tech_name="theme_crest"
            ;;
        "backend_theme_odoo12")
            expected_tech_name="backend_theme_odoo12"  # Garder tel quel
            ;;
        "site_magic3brothers")
            expected_tech_name="theme_magic3brothers"  # Renommer pour standardiser
            ;;
        "ylhc_theme_base")
            expected_tech_name="theme_ylhc_base"  # Standardiser
            ;;
    esac
    
    if [ "$dir_name" != "$expected_tech_name" ]; then
        log_warning "Incohérence: dossier='$dir_name' vs attendu='$expected_tech_name'"
        echo "$theme_dir|$expected_tech_name"
        return 1
    fi
    
    return 0
}

# Fonction pour renommer un dossier
rename_theme_directory() {
    local old_path="$1"
    local new_name="$2"
    local parent_dir=$(dirname "$old_path")
    local new_path="$parent_dir/$new_name"
    
    if [ -d "$new_path" ]; then
        log_error "Le dossier $new_path existe déjà!"
        return 1
    fi
    
    log_info "Renommage: $(basename "$old_path") -> $new_name"
    mv "$old_path" "$new_path"
    log_success "Dossier renommé: $new_path"
    
    return 0
}

# Fonction pour supprimer les anciens fichiers __openerp__.py
remove_old_openerp_files() {
    local theme_dir="$1"
    local openerp_file="$theme_dir/__openerp__.py"
    
    if [ -f "$openerp_file" ] && [ -f "$theme_dir/__manifest__.py" ]; then
        log_info "Suppression de l'ancien fichier __openerp__.py dans $theme_dir"
        rm -f "$openerp_file"
        log_success "__openerp__.py supprimé"
    fi
}

log_info "=========================================="
log_info "Vérification des Modules Themes"
log_info "=========================================="

# Liste des dossiers à vérifier
THEME_DIRS=$(find "$THEMES_DIR" -maxdepth 1 -type d ! -path "$THEMES_DIR" ! -name ".*" | sort)

RENAME_LIST=""
ISSUES=0

# Vérifier chaque module
for theme_dir in $THEME_DIRS; do
    theme_name=$(basename "$theme_dir")
    log_info "Vérification: $theme_name"
    
    # Vérifier la cohérence
    if ! check_module_consistency "$theme_dir"; then
        result=$(check_module_consistency "$theme_dir" 2>&1 | grep "|" || echo "")
        if [ -n "$result" ]; then
            RENAME_LIST="${RENAME_LIST}${result}\n"
            ((ISSUES++))
        fi
    else
        log_success "✓ $theme_name est cohérent"
    fi
    
    # Supprimer les anciens fichiers __openerp__.py
    remove_old_openerp_files "$theme_dir"
done

# Afficher les problèmes trouvés
if [ $ISSUES -gt 0 ]; then
    echo ""
    log_warning "=========================================="
    log_warning "Problèmes détectés:"
    log_warning "=========================================="
    echo -e "$RENAME_LIST"
    
    echo ""
    log_info "Voulez-vous renommer automatiquement? (y/n)"
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo -e "$RENAME_LIST" | while IFS='|' read -r old_path new_name; do
            if [ -n "$old_path" ] && [ -n "$new_name" ]; then
                rename_theme_directory "$old_path" "$new_name"
            fi
        done
        log_success "Renommage terminé!"
    else
        log_info "Renommage annulé"
    fi
else
    log_success "Tous les modules sont cohérents!"
fi

# Vérifications supplémentaires
log_info ""
log_info "=========================================="
log_info "Vérifications Supplémentaires"
log_info "=========================================="

# Vérifier les versions
log_info "Vérification des versions..."
VERSION_ISSUES=0
for manifest in $(find "$THEMES_DIR" -name "__manifest__.py" | sort); do
    version=$(grep -E "^\s*['\"]version['\"]\s*:" "$manifest" | head -1 | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/" || echo "")
    if [[ ! "$version" =~ ^18\.0\. ]]; then
        log_warning "Version non standard dans $(dirname "$manifest"): $version"
        ((VERSION_ISSUES++))
    fi
done

if [ $VERSION_ISSUES -eq 0 ]; then
    log_success "Toutes les versions sont en 18.0.x.x.x"
else
    log_warning "$VERSION_ISSUES modules avec versions non standard"
fi

# Résumé final
echo ""
log_info "=========================================="
log_info "Résumé"
log_info "=========================================="
log_info "Modules vérifiés: $(echo "$THEME_DIRS" | wc -l | tr -d ' ')"
log_info "Problèmes détectés: $ISSUES"
log_info "Versions non standard: $VERSION_ISSUES"
log_info "=========================================="

