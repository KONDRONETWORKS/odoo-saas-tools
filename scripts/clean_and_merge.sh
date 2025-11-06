#!/bin/bash
# Script pour nettoyer, fusionner et démarrer le SaaS

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

echo "============================================================"
echo "🧹 Nettoyage et Fusion - Odoo SaaS Tools"
echo "============================================================"
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

DELETED=0
MERGED=0

# Fonction pour supprimer
delete_file() {
    if [ -f "$1" ] || [ -d "$1" ]; then
        rm -rf "$1"
        echo -e "${GREEN}✅ Supprimé:${NC} $1"
        ((DELETED++))
    fi
}

# Fonction pour archiver
archive_file() {
    if [ -f "$1" ]; then
        mkdir -p "_LIVRABLES/archive/obsolete"
        mv "$1" "_LIVRABLES/archive/obsolete/"
        echo -e "${YELLOW}📦 Archivé:${NC} $1"
    fi
}

echo "📋 Étape 1: Suppression des fichiers obsolètes à la racine..."

# Fichiers obsolètes à la racine (déjà dans _LIVRABLES)
delete_file "ACTIONS_RESTANTES.md"
delete_file "CHECKLIST_FINAL.md"
delete_file "GUIDE_DEPLOIEMENT_AWS.md"  # Dupliqué dans _LIVRABLES
delete_file "RESUME_CI_CD.md"  # Peut être fusionné avec docs/CI_CD_GUIDE.md
delete_file "README_CLEAN_CODE.md"  # Fusionné dans CLEAN_CODE.md

echo ""
echo "📋 Étape 2: Fusion de la documentation Docker..."

# Fusionner DOCKER_SETUP.md et DEMARRAGE_RAPIDE.md
if [ -f "DOCKER_SETUP.md" ] && [ -f "DEMARRAGE_RAPIDE.md" ]; then
    echo -e "${YELLOW}🔄 Fusion de DOCKER_SETUP.md et DEMARRAGE_RAPIDE.md...${NC}"
    {
        echo "# 🐳 Guide Docker - Odoo SaaS Tools"
        echo ""
        echo "## 🚀 Démarrage Rapide"
        echo ""
        cat DEMARRAGE_RAPIDE.md | tail -n +2
        echo ""
        echo "---"
        echo ""
        echo "## 📝 Configuration Détaillée"
        echo ""
        cat DOCKER_SETUP.md | tail -n +2
    } > "docs/DOCKER_GUIDE.md"
    archive_file "DOCKER_SETUP.md"
    archive_file "DEMARRAGE_RAPIDE.md"
    ((MERGED++))
fi

echo ""
echo "📋 Étape 3: Archivage des fichiers Docker Compose obsolètes..."

# Archiver les fichiers Docker Compose non utilisés (garder simple.yml)
mkdir -p "_LIVRABLES/archive/docker-compose"
if [ -f "config/docker-compose.yml" ]; then
    archive_file "config/docker-compose.yml"
fi

echo ""
echo "📋 Étape 4: Nettoyage des fichiers temporaires..."

# Nettoyer les fichiers de backup et cache
find . -type f \( -name "*.bak" -o -name "*.old" -o -name "*.backup" \) \
    -not -path "./.git/*" -not -path "./_LIVRABLES/*" -not -path "./filestore/*" \
    -exec rm -f {} \; 2>/dev/null || true

# Nettoyer le cache Python
find . -type d -name "__pycache__" \
    -not -path "./.git/*" -not -path "./_LIVRABLES/*" \
    -exec rm -rf {} + 2>/dev/null || true

find . -type f \( -name "*.pyc" -o -name "*.pyo" \) \
    -not -path "./.git/*" -not -path "./_LIVRABLES/*" \
    -exec rm -f {} \; 2>/dev/null || true

echo ""
echo "📋 Étape 5: Création d'un index de documentation..."

# Créer un index consolidé
cat > "docs/INDEX.md" << 'EOF'
# 📚 Index de la Documentation

## 🚀 Démarrage Rapide
- [Guide Docker](DOCKER_GUIDE.md) - Configuration et démarrage Docker
- [Guide CI/CD](CI_CD_GUIDE.md) - Configuration CI/CD avec GitHub Actions

## 📖 Guides Utilisateur
- [Scénario Utilisateur](SCENARIO_UTILISATEUR_SAAS.md) - Comment un utilisateur accède au SaaS
- [Résumé Scénario](RESUME_SCENARIO_UTILISATEUR.md) - Résumé visuel du scénario

## 🔧 Configuration
- [Corriger Master Password](CORRIGER_MASTER_PASSWORD.md) - Résoudre les problèmes de Master Password
- [Suppression Base de Données](SUPPRESSION_BASE_DONNEES.md) - Comment supprimer une base
- [Noms Conteneurs Docker](NOMS_CONTENEURS_DOCKER.md) - Guide des conteneurs
- [Comportement saas_portal_start](COMPORTEMENT_SAAS_PORTAL_START.md) - Module de démarrage

## 📁 Structure
- [Setup](setup/) - Guides de configuration détaillés
- [Guides](guides/) - Guides d'utilisation
EOF

echo ""
echo "============================================================"
echo "✅ Nettoyage et fusion terminés!"
echo "============================================================"
echo ""
echo "📊 Statistiques:"
echo "   - Fichiers supprimés: $DELETED"
echo "   - Fichiers fusionnés: $MERGED"
echo ""

