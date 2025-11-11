#!/bin/bash
# Script de démarrage complet pour Odoo SaaS Tools

set -e

echo "🚀 Démarrage complet Odoo SaaS Tools"

# Vérifier que PostgreSQL est en cours d'exécution
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo "❌ PostgreSQL n'est pas en cours d'exécution"
    echo "💡 Démarrez PostgreSQL avec: brew services start postgresql@17"
    exit 1
fi

# Activer l'environnement virtuel
echo "🐍 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python -c "import psycopg2, requests" || {
    echo "❌ Dépendances manquantes. Installation..."
    pip install -r requirements.txt
}

# Créer le répertoire filestore si nécessaire
mkdir -p filestore

# Vérifier si Odoo est installé
if [ ! -f "../odoo/odoo-bin" ]; then
    echo "❌ Odoo n'est pas trouvé dans ../odoo/odoo-bin"
    echo "💡 Veuillez installer Odoo 18.0 dans le répertoire parent"
    exit 1
fi

# Démarrer Odoo en arrière-plan
echo "🎯 Démarrage d'Odoo..."
nohup ../odoo/odoo-bin -c odoo.conf --logfile=odoo.log --log-level=info > /dev/null 2>&1 &
ODOO_PID=$!

# Attendre qu'Odoo soit prêt
echo "⏳ Attente du démarrage d'Odoo..."
for i in {1..30}; do
    if curl -s http://localhost:8069 > /dev/null 2>&1; then
        echo "✅ Odoo est prêt !"
        break
    fi
    echo "   Tentative $i/30..."
    sleep 2
done

# Vérifier si Odoo est accessible
if ! curl -s http://localhost:8069 > /dev/null 2>&1; then
    echo "❌ Odoo n'est pas accessible après 60 secondes"
    kill $ODOO_PID 2>/dev/null || true
    exit 1
fi

# Démarrer l'application SaaS
echo "🎯 Démarrage de l'application SaaS..."
python saas.py --portal-create --server-create --plan-create --run

# Nettoyer à la sortie
trap "kill $ODOO_PID 2>/dev/null || true" EXIT
