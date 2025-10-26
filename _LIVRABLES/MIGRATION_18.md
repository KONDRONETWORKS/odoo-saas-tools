# Migration vers Odoo 18.0

## 🚀 Changements Principaux

### Versions Mises à Jour
- **Odoo** : 11.0 → 18.0
- **Python** : 2.7/3.6 → 3.8+
- **PostgreSQL** : 9.6+ → 12+

### Dépendances Mises à Jour
- `boto` → `boto3>=1.34.0`
- `sphinx==1.2.3` → `sphinx>=7.0.0`
- `mercurial==3.2.2` → Supprimé (obsolète)
- Ajout de `psycopg2-binary>=2.9.0`
- Ajout de `requests>=2.31.0`

## 📋 Étapes de Migration

### 1. Prérequis
```bash
# Python 3.8+ requis
python3 --version

# PostgreSQL 12+ requis
psql --version

# Installer les nouvelles dépendances
pip install -r requirements.txt
```

### 2. Sauvegarde
```bash
# Sauvegarder la base de données
pg_dump your_database > backup_odoo11.sql

# Sauvegarder les fichiers
tar -czf odoo11_backup.tar.gz /path/to/odoo/filestore
```

### 3. Migration de la Base de Données
```bash
# Utiliser l'outil de migration d'Odoo
python3 odoo-bin -d your_database -u all --stop-after-init
```

### 4. Tests
```bash
# Installer les dépendances de test
pip install -r requirements-dev.txt

# Lancer les tests
pytest
```

## ⚠️ Points d'Attention

### Changements d'API
- Certaines méthodes d'API ont été modifiées
- Vérifiez la compatibilité des modules tiers
- Testez toutes les fonctionnalités personnalisées

### Modules OCA
- Vérifiez la compatibilité des modules OCA avec Odoo 18.0
- Certains modules peuvent nécessiter des mises à jour

### Configuration
- Mettez à jour les fichiers de configuration
- Vérifiez les paramètres de sécurité
- Adaptez les règles de routage si nécessaire

## 🔧 Outils de Migration

### Formatage de Code
```bash
# Formater le code avec Black
black .

# Organiser les imports avec isort
isort .

# Vérifier la qualité du code
flake8 .
```

### Tests
```bash
# Tests unitaires
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Tests avec couverture
pytest --cov=.
```

## 📚 Ressources

- [Documentation Odoo 18.0](https://www.odoo.com/documentation/18.0/)
- [Notes de version Odoo 18.0](https://www.odoo.com/fr_FR/odoo-18-release-notes)
- [Guide de migration Odoo](https://www.odoo.com/documentation/18.0/administration/deploy/upgrade.html)

## 🆘 Support

En cas de problème :
1. Consultez les logs d'erreur
2. Vérifiez la compatibilité des modules
3. Contactez le support : apps@itexperts4africa.com
