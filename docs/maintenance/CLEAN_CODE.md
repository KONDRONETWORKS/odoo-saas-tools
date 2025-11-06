# 🧹 Clean Code - Guide de Nettoyage

## 🎯 Objectif

Maintenir un code propre, organisé et facile à maintenir.

---

## 🚀 Nettoyage Rapide

### Script Automatique

```bash
./scripts/clean_code.sh
```

Ce script supprime automatiquement :
- ✅ Fichiers de backup (`.bak`, `.backup`, `.old`)
- ✅ Fichiers temporaires (`.tmp`, `.swp`, `*~`)
- ✅ Cache Python (`__pycache__`, `*.pyc`, `*.pyo`)
- ✅ Fichiers système (`.DS_Store`)
- ✅ Logs anciens (plus de 7 jours)
- ✅ Fichiers de test temporaires

---

## 📋 Nettoyage Manuel

### 1. Fichiers Docker Compose

**Fichier principal à utiliser :**
- ✅ `config/docker-compose.simple.yml` - **À UTILISER**

**Fichiers de référence (ne pas supprimer) :**
- 📚 `config/docker-compose.dev.yml` - Pour développement avec hot reload
- 📚 `config/docker-compose.prod.yml` - Pour production
- 📚 `config/docker-compose.windows.yml` - Pour Windows
- 📚 `config/docker-compose.yml` - Ancienne version (référence)

**Documentation :** Voir `config/GUIDE_FICHIERS_DOCKER_COMPOSE.md`

### 2. Fichiers de Configuration

**À garder :**
- ✅ `odoo.conf` - Configuration principale
- ✅ `requirements.txt` - Dépendances Python
- ✅ `requirements-dev.txt` - Dépendances développement
- ✅ `pytest.ini` - Configuration tests
- ✅ `pyproject.toml` - Configuration Python

**À supprimer :**
- ❌ `odoo.conf.bak` - Backup
- ❌ `odoo.conf.old` - Ancienne version
- ❌ `*.local` - Configurations locales

### 3. Documentation

**Structure organisée :**
```
docs/                    # Documentation principale
├── setup/               # Guides de configuration
├── guides/              # Guides d'utilisation
└── *.md                 # Documentation spécifique

_LIVRABLES/              # Livrables et archives
├── documentation/       # Documentation consolidée
└── archive/            # Fichiers archivés
```

**À nettoyer :**
- ❌ Documentation dupliquée
- ❌ Fichiers temporaires dans `docs/temp/`
- ❌ Anciens résumés obsolètes

### 4. Scripts

**Structure :**
```
scripts/
├── start_saas.sh           # Démarrage/arrêt service
├── clean_code.sh           # Nettoyage automatique
├── drop_database.py        # Suppression bases
├── update_master_password.py # Mise à jour Master Password
└── check_and_install_portal_start.py # Installation modules
```

**À supprimer :**
- ❌ Scripts temporaires (`test_*.py`, `fix_*.py`)
- ❌ Scripts obsolètes (déplacer vers `_LIVRABLES/scripts/`)

### 5. Modules Odoo

**À nettoyer dans chaque module :**
- ❌ `__pycache__/` - Cache Python
- ❌ `*.pyc`, `*.pyo` - Bytecode Python
- ❌ Fichiers `.old`, `.bak` - Backups

---

## 🔍 Vérifications

### Avant de commiter

```bash
# 1. Nettoyer le code
./scripts/clean_code.sh

# 2. Vérifier les changements
git status

# 3. Vérifier les fichiers ignorés
git check-ignore -v *

# 4. Vérifier la taille des fichiers
find . -type f -size +1M -not -path "./.git/*" -not -path "./filestore/*"
```

### Vérifier les fichiers obsolètes

```bash
# Fichiers de backup
find . -type f \( -name "*.bak" -o -name "*.backup" -o -name "*.old" \) \
  -not -path "./.git/*" -not -path "./_LIVRABLES/*"

# Cache Python
find . -type d -name "__pycache__" \
  -not -path "./.git/*" -not -path "./_LIVRABLES/*"

# Fichiers temporaires
find . -type f \( -name "*.tmp" -o -name "*.swp" -o -name "*~" \) \
  -not -path "./.git/*" -not -path "./_LIVRABLES/*"
```

---

## 📝 Règles de Clean Code

### 1. Fichiers à Ignorer

Tous les fichiers suivants doivent être dans `.gitignore` :
- Logs (`*.log`)
- Cache Python (`__pycache__/`, `*.pyc`)
- Fichiers temporaires (`*.tmp`, `*.bak`, `*.old`)
- Fichiers système (`.DS_Store`, `*.swp`)

### 2. Structure du Projet

```
odoo-saas-tools/
├── config/              # Configurations Docker
├── docs/               # Documentation principale
├── scripts/            # Scripts utilitaires
├── tests/              # Tests unitaires
├── infrastructure/     # Infrastructure AWS/Terraform
├── _LIVRABLES/        # Livrables et archives
└── saas_*/            # Modules Odoo
```

### 3. Nommage

- **Scripts** : `snake_case.sh` ou `snake_case.py`
- **Documentation** : `UPPER_CASE.md` pour guides principaux
- **Modules** : `saas_module_name/`

### 4. Documentation

- Un fichier README.md à la racine
- Documentation dans `docs/`
- Guides spécifiques dans `docs/guides/`
- Configuration dans `docs/setup/`

---

## 🛠️ Maintenance Régulière

### Hebdomadaire

```bash
# Nettoyer le code
./scripts/clean_code.sh

# Vérifier les logs
du -sh *.log 2>/dev/null || echo "Pas de logs"
```

### Mensuelle

```bash
# Nettoyer les logs anciens
find . -name "*.log" -mtime +30 -delete

# Vérifier les fichiers volumineux
find . -type f -size +10M -not -path "./.git/*" -not -path "./filestore/*"
```

---

## ✅ Checklist Clean Code

Avant de commiter :

- [ ] Exécuter `./scripts/clean_code.sh`
- [ ] Vérifier qu'il n'y a pas de fichiers `.bak`, `.old`, `.tmp`
- [ ] Vérifier qu'il n'y a pas de `__pycache__/`
- [ ] Vérifier que les logs ne sont pas commités
- [ ] Vérifier la structure des dossiers
- [ ] Vérifier que la documentation est à jour

---

## 📚 Ressources

- **Script de nettoyage** : `scripts/clean_code.sh`
- **Guide Docker Compose** : `config/GUIDE_FICHIERS_DOCKER_COMPOSE.md`
- **Guide démarrage** : `DEMARRAGE_RAPIDE.md`
- **Documentation complète** : `docs/`

---

**Maintenez votre code propre ! 🧹**

