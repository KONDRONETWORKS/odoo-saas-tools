#!/bin/bash
# Script de nettoyage complet du projet Odoo SaaS Tools

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

echo "============================================================"
echo "🧹 Nettoyage du Code - Odoo SaaS Tools"
echo "============================================================"
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Compteurs
DELETED=0
CLEANED=0

# Fonction pour supprimer un fichier
delete_file() {
    if [ -f "$1" ] || [ -d "$1" ]; then
        rm -rf "$1"
        echo -e "${GREEN}✅ Supprimé:${NC} $1"
        ((DELETED++))
    fi
}

# Fonction pour nettoyer un fichier
clean_file() {
    if [ -f "$1" ]; then
        echo -e "${YELLOW}🧹 Nettoyé:${NC} $1"
        ((CLEANED++))
    fi
}

echo "📋 Étape 1: Suppression des fichiers de backup..."
# Fichiers de backup
delete_file "odoo.conf.bak"
find . -name "*.bak" -type f -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done

echo ""
echo "📋 Étape 2: Suppression des fichiers temporaires..."
# Fichiers temporaires
find . -name "*.tmp" -type f -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done
find . -name "*.old" -type f -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done
find . -name "*.backup" -type f -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done

echo ""
echo "📋 Étape 3: Nettoyage des fichiers Python..."
# Cache Python
find . -type d -name "__pycache__" -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read dir; do
    delete_file "$dir"
done
find . -name "*.pyc" -type f -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done
find . -name "*.pyo" -type f -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done
find . -name ".Python" -type f -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done

echo ""
echo "📋 Étape 4: Nettoyage des logs..."
# Logs (garder les récents)
if [ -f "odoo.log" ]; then
    if [ $(find "odoo.log" -mtime +7 | wc -l) -gt 0 ]; then
        > odoo.log
        clean_file "odoo.log"
    fi
fi
if [ -f "saas.log" ]; then
    if [ $(find "saas.log" -mtime +7 | wc -l) -gt 0 ]; then
        > saas.log
        clean_file "saas.log"
    fi
fi

echo ""
echo "📋 Étape 5: Nettoyage des fichiers système..."
# Fichiers système
delete_file ".DS_Store"
find . -name ".DS_Store" -type f -not -path "./.git/*" | while read file; do
    delete_file "$file"
done
find . -name "*.swp" -type f -not -path "./.git/*" | while read file; do
    delete_file "$file"
done
find . -name "*~" -type f -not -path "./.git/*" | while read file; do
    delete_file "$file"
done

echo ""
echo "📋 Étape 6: Nettoyage des fichiers de test temporaires..."
# Fichiers de test temporaires
delete_file "test-unitaire.txt"
find . -name "test_*.py" -type f -not -path "./tests/*" -not -path "./.git/*" -not -path "./_LIVRABLES/*" | while read file; do
    delete_file "$file"
done

echo ""
echo "📋 Étape 7: Vérification des fichiers Docker Compose..."
# Vérifier que docker-compose.simple.yml existe
if [ ! -f "config/docker-compose.simple.yml" ]; then
    echo -e "${RED}❌ ERREUR: config/docker-compose.simple.yml n'existe pas!${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Fichier principal trouvé: config/docker-compose.simple.yml${NC}"

echo ""
echo "📋 Étape 8: Nettoyage des fichiers de configuration obsolètes..."
# Fichiers de configuration obsolètes (garder seulement les essentiels)
# Ne pas supprimer les docker-compose, juste documenter

echo ""
echo "============================================================"
echo "✅ Nettoyage terminé!"
echo "============================================================"
echo ""
echo "📊 Statistiques:"
echo "   - Fichiers/dossiers supprimés: $DELETED"
echo "   - Fichiers nettoyés: $CLEANED"
echo ""
echo "💡 Prochaines étapes:"
echo "   1. Vérifier les changements: git status"
echo "   2. Commit si nécessaire: git add . && git commit -m 'Clean code'"
echo ""

