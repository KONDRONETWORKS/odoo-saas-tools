#!/bin/bash
# Script de nettoyage et réorganisation de la racine du projet

set -e

PROJECT_ROOT="/Users/apple/KONDRO/odoo-sass/odoo-saas-tools"

echo "🧹 Nettoyage et réorganisation du projet..."

# Déplacer les scripts de test/legacy
echo "📦 Déplacement des scripts legacy..."
mv -f "$PROJECT_ROOT/fix_plan_view.py" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/fix_plan_view_now.py" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/fix_plan_view_immediate.sh" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/force_create_plan_view.py" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/force_fix_tree_cache.py" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/recreate_plan_views.py" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/create_tree_view_compat.py" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/check_plan_views.py" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/update_saas_portal.sh" "$PROJECT_ROOT/scripts/legacy/" 2>/dev/null || true

# Déplacer les tests
echo "🧪 Déplacement des tests..."
mv -f "$PROJECT_ROOT/test_create_client.py" "$PROJECT_ROOT/tests/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/test_frontend_tree_request.py" "$PROJECT_ROOT/tests/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/test_get_views_unit.py" "$PROJECT_ROOT/tests/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/test_tree_fix.py" "$PROJECT_ROOT/tests/legacy/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/test_xml_odoo18.xml" "$PROJECT_ROOT/tests/legacy/" 2>/dev/null || true

# Déplacer les fichiers de solution temporaires
echo "📄 Déplacement des fichiers de solution temporaires..."
mv -f "$PROJECT_ROOT/SOLUTION_FINALE_TREE.md" "$PROJECT_ROOT/docs/temp/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/SOLUTION_VUE_TREE_PLANS.md" "$PROJECT_ROOT/docs/temp/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/TEST_CREATION_CLIENT.md" "$PROJECT_ROOT/docs/temp/" 2>/dev/null || true

# Déplacer les logs
echo "📋 Déplacement des logs..."
mv -f "$PROJECT_ROOT/odoo.log" "$PROJECT_ROOT/.logs/" 2>/dev/null || true
mv -f "$PROJECT_ROOT/saas.log" "$PROJECT_ROOT/.logs/" 2>/dev/null || true

# Créer .logs si nécessaire
mkdir -p "$PROJECT_ROOT/.logs"

# Garder à la racine uniquement les fichiers essentiels
echo "✅ Nettoyage terminé"
echo ""
echo "📁 Structure organisée:"
echo "  - scripts/legacy/ - Scripts de migration et fixes temporaires"
echo "  - tests/legacy/ - Tests temporaires"
echo "  - docs/temp/ - Documentation temporaire"
echo "  - .logs/ - Fichiers de logs"

