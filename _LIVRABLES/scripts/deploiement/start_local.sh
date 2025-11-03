#!/bin/bash
# Script de démarrage local pour Odoo SaaS Tools

set -e

echo "🚀 Démarrage Odoo SaaS Tools en local"

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
python -c "import psycopg2, requests, simplejson" || {
    echo "❌ Dépendances manquantes. Installation..."
    pip install -r requirements.txt
}

# Créer le répertoire filestore si nécessaire
mkdir -p filestore

# Démarrer l'application
echo "🎯 Démarrage de l'application SaaS..."
python saas.py --portal-create --server-create --plan-create --run
