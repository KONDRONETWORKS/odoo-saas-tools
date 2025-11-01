#!/bin/bash
# Script pour redémarrer le serveur et corriger OAuth

set -e

echo "🔄 Redémarrage du serveur Odoo et correction OAuth"
echo "=================================================="

# Arrêter le serveur si en cours
echo ""
echo "🛑 Arrêt du serveur Odoo..."
lsof -ti tcp:8069 | xargs -r kill -9 2>/dev/null || true
sleep 2

# Activer l'environnement virtuel
echo "🐍 Activation de l'environnement virtuel..."
cd "$(dirname "$0")"
source .venv/bin/activate

# Nettoyer le cache Python
echo ""
echo "🧹 Nettoyage du cache Python..."
find saas_oauth_provider -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
find saas_oauth_provider -type f -name "*.pyc" -delete 2>/dev/null || true

# Mettre à jour le module pour charger les nouvelles règles de sécurité
echo ""
echo "📦 Mise à jour du module saas_oauth_provider..."
python3.11 ../odoo/odoo-bin -c odoo.conf --stop-after-init -u saas_oauth_provider 2>&1 | grep -E "(Updating|Module.*loaded|ERROR)" || true

# Initialiser le client_id
echo ""
echo "🔑 Initialisation du client_id OAuth..."
python3 fix_oauth_client_id.py --db odoo 2>&1 || echo "⚠️  Script d'initialisation client_id non disponible"

# Redémarrer le serveur
echo ""
echo "🚀 Redémarrage du serveur Odoo..."
python3.11 ../odoo/odoo-bin -c odoo.conf --logfile=odoo.log &

echo ""
echo "✅ Redémarrage terminé !"
echo ""
echo "⏳ Attendre 5-10 secondes que le serveur démarre..."
sleep 5

echo ""
echo "📊 Vérification des logs:"
tail -20 odoo.log | grep -E "(ERROR|loaded|HTTP)" || echo "   Aucune erreur visible"

echo ""
echo "✅ Serveur redémarré !"
echo ""
echo "💡 Pour tester:"
echo "   1. Allez sur http://localhost:8069"
echo "   2. Essayez la connexion OAuth"
echo "   3. Vérifiez les logs: tail -f odoo.log"
echo ""

