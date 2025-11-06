#!/bin/bash
# Script pour corriger le Master Password dans Docker

echo "============================================================"
echo "🔐 Correction du Master Password Odoo"
echo "============================================================"
echo ""

# Vérifier que odoo.conf existe
if [ ! -f "odoo.conf" ]; then
    echo "❌ Fichier odoo.conf non trouvé"
    exit 1
fi

# Vérifier le Master Password actuel
echo "📋 Master Password actuel dans odoo.conf:"
grep "admin_passwd" odoo.conf || echo "   (non trouvé)"

# S'assurer que le Master Password est en clair
echo ""
echo "🔧 Mise à jour du Master Password en clair..."
sed -i.bak 's/^admin_passwd = .*/admin_passwd = admin/' odoo.conf

# Vérifier la modification
echo ""
echo "✅ Master Password mis à jour:"
grep "admin_passwd" odoo.conf

# Redémarrer le conteneur
echo ""
echo "🔄 Redémarrage du conteneur Odoo..."
docker compose -f config/docker-compose.simple.yml restart

echo ""
echo "⏳ Attente du démarrage (15 secondes)..."
sleep 15

# Vérifier dans le conteneur
echo ""
echo "📋 Vérification dans le conteneur:"
CONTAINER_NAME=$(docker ps --format "{{.Names}}" | grep saas-odoo | head -1)
if [ -n "$CONTAINER_NAME" ]; then
    docker exec "$CONTAINER_NAME" cat /etc/odoo/odoo.conf 2>/dev/null | grep admin_passwd || echo "   (non accessible)"
else
    echo "   (conteneur non trouvé)"
fi

echo ""
echo "============================================================"
echo "✅ Correction terminée"
echo "============================================================"
echo ""
echo "💡 Vous pouvez maintenant utiliser 'admin' comme Master Password"
echo "   dans l'interface web: http://localhost:8069/web/database/manager"

