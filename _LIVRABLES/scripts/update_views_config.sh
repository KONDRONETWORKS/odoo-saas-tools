#!/bin/bash
# Script pour mettre à jour les modules de configuration après modification des vues

echo "🔄 Mise à jour des modules de configuration..."
echo ""

MODULES=(
    "saas_server_backup_rotate"
    "saas_server_backup_s3"
    "saas_server"
)

echo "Modules à mettre à jour :"
for module in "${MODULES[@]}"; do
    echo "  - $module"
done

echo ""
echo "⚠️  Instructions :"
echo "1. Dans Odoo, allez dans : Paramètres > Applications"
echo "2. Activez le mode développeur (si ce n'est pas déjà fait)"
echo "3. Cliquez sur 'Mettre à jour la liste des applications'"
echo "4. Recherchez chaque module et cliquez sur 'Mettre à jour'"
echo ""
echo "Modules à mettre à jour manuellement :"
for module in "${MODULES[@]}"; do
    echo "  - $module"
done
echo ""
echo "5. Videz le cache du navigateur :"
echo "   - Chrome/Edge: Ctrl+Shift+Delete (ou Cmd+Shift+Delete sur Mac)"
echo "   - Firefox: Ctrl+Shift+Delete (ou Cmd+Shift+Delete sur Mac)"
echo "   - Ou utilisez le mode incognito/navigation privée"
echo ""
echo "6. Rechargez la page de configuration avec Ctrl+F5 (ou Cmd+Shift+R sur Mac)"
echo ""

