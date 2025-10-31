#!/bin/bash
# Script pour mettre à jour le module saas_sysadmin_mailgun

echo "🔄 Mise à jour du module saas_sysadmin_mailgun"
echo "=============================================="

# Configuration
ODOO_BIN="../odoo/odoo-bin"
CONFIG_FILE="odoo.conf"
MODULE_NAME="saas_sysadmin_mailgun"

# Activer l'environnement virtuel si présent
if [ -d ".venv" ]; then
    echo "🐍 Activation de l'environnement virtuel..."
    source .venv/bin/activate
fi

# Mettre à jour le module
echo ""
echo "📦 Mise à jour du module ${MODULE_NAME}..."
python3.11 "${ODOO_BIN}" -c "${CONFIG_FILE}" \
    --logfile=odoo.log \
    --stop-after-init \
    -u "${MODULE_NAME}"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Module mis à jour avec succès!"
    echo ""
    echo "💡 Instructions:"
    echo "   1. Redémarrez le serveur Odoo"
    echo "   2. Videz le cache du navigateur (Ctrl+F5 ou Cmd+Shift+R)"
    echo "   3. Allez dans Settings et vérifiez que le champ apparaît"
else
    echo ""
    echo "❌ Erreur lors de la mise à jour"
    echo "📊 Vérifiez les logs: tail -f odoo.log"
    exit 1
fi

