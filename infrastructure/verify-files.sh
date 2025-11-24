#!/bin/bash

# 🔍 Script de vérification des fichiers de déploiement
# Usage: bash verify-files.sh

set -e

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Compteurs
TOTAL=0
PRESENT=0
MISSING=0
EXEC_OK=0
EXEC_NOK=0

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔════════════════════════════════════════════╗
║  🔍 VÉRIFICATION DES FICHIERS             ║
║     Déploiement OVH                       ║
╚════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Répertoire du projet
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}Répertoire du projet: $PROJECT_ROOT${NC}\n"

# Fonction de vérification
check_file() {
    local file="$1"
    local exec="$2"
    
    TOTAL=$((TOTAL + 1))
    
    if [ -f "$file" ]; then
        PRESENT=$((PRESENT + 1))
        
        if [ "$exec" = "yes" ]; then
            if [ -x "$file" ]; then
                echo -e "${GREEN}✅${NC} $file (exécutable)"
                EXEC_OK=$((EXEC_OK + 1))
            else
                echo -e "${YELLOW}⚠️${NC}  $file (NON exécutable - chmod +x requis)"
                EXEC_NOK=$((EXEC_NOK + 1))
            fi
        else
            echo -e "${GREEN}✅${NC} $file"
        fi
    else
        echo -e "${RED}❌${NC} $file (MANQUANT)"
        MISSING=$((MISSING + 1))
    fi
}

# Vérification des fichiers

echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}1. Configuration Docker${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
check_file "config/docker-compose.ovh.yml" "no"
check_file "config/nginx.ovh.conf" "no"
check_file "config/Dockerfile" "no"
check_file "config/docker-entrypoint.sh" "yes"
check_file "config/env.template" "no"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}2. Scripts de déploiement${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
check_file "infrastructure/deploy-ovh.sh" "yes"
check_file "infrastructure/prepare-deploy.sh" "yes"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}3. Scripts de maintenance${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
check_file "scripts/backup.sh" "yes"
check_file "scripts/restore.sh" "yes"
check_file "scripts/maintenance.sh" "yes"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}4. Documentation${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
check_file "infrastructure/GUIDE_DEPLOIEMENT_OVH.md" "no"
check_file "infrastructure/README_DEPLOIEMENT_OVH.md" "no"
check_file "infrastructure/CHECKLIST_DEPLOIEMENT.md" "no"
check_file "infrastructure/FICHIERS_DEPLOIEMENT.md" "no"
check_file "DEPLOIEMENT_OVH_QUICKSTART.md" "no"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}5. Fichiers requis existants${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
check_file "requirements.txt" "no"
check_file "README.md" "no"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}RÉSUMÉ${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo ""
echo -e "Total de fichiers vérifiés:  ${BLUE}$TOTAL${NC}"
echo -e "Fichiers présents:           ${GREEN}$PRESENT${NC}"
echo -e "Fichiers manquants:          ${RED}$MISSING${NC}"
echo ""
echo -e "Scripts exécutables OK:      ${GREEN}$EXEC_OK${NC}"
echo -e "Scripts nécessitant chmod:   ${YELLOW}$EXEC_NOK${NC}"
echo ""

# Vérifier les modules
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}MODULES ODOO${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo ""

MODULES=0
SAAS_MODULES=$(find . -maxdepth 1 -type d -name "saas_*" | wc -l)
KONDRO_MODULES=$(find kondro -maxdepth 1 -type d 2>/dev/null | grep -v "^kondro$" | wc -l || echo 0)

echo -e "Modules SaaS trouvés:        ${GREEN}$SAAS_MODULES${NC}"
echo -e "Modules Kondro trouvés:      ${GREEN}$KONDRO_MODULES${NC}"
echo ""

# Vérifier l'espace disque
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}ESPACE DISQUE${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo ""

PROJECT_SIZE=$(du -sh "$PROJECT_ROOT" | cut -f1)
echo -e "Taille du projet:            ${BLUE}$PROJECT_SIZE${NC}"
echo ""

# Résultat final
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo -e "${BLUE}RÉSULTAT${NC}"
echo -e "${BLUE}═══════════════════════════════════════════${NC}"
echo ""

if [ $MISSING -eq 0 ] && [ $EXEC_NOK -eq 0 ]; then
    echo -e "${GREEN}✅ TOUS LES FICHIERS SONT PRÉSENTS ET PRÊTS !${NC}"
    echo ""
    echo -e "${GREEN}Vous pouvez lancer le déploiement:${NC}"
    echo -e "  ${BLUE}bash infrastructure/prepare-deploy.sh${NC}"
    echo ""
    exit 0
elif [ $MISSING -gt 0 ]; then
    echo -e "${RED}❌ CERTAINS FICHIERS SONT MANQUANTS${NC}"
    echo ""
    echo -e "${YELLOW}Fichiers manquants: $MISSING${NC}"
    echo -e "${YELLOW}Veuillez régénérer les fichiers manquants.${NC}"
    echo ""
    exit 1
elif [ $EXEC_NOK -gt 0 ]; then
    echo -e "${YELLOW}⚠️  CERTAINS SCRIPTS NE SONT PAS EXÉCUTABLES${NC}"
    echo ""
    echo -e "${YELLOW}Exécutez cette commande pour corriger:${NC}"
    echo -e "  ${BLUE}chmod +x infrastructure/*.sh scripts/*.sh config/docker-entrypoint.sh${NC}"
    echo ""
    exit 2
else
    echo -e "${GREEN}✅ FICHIERS OK${NC}"
    echo ""
    exit 0
fi

