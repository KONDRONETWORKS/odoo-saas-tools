# 📁 Structure du Projet Odoo SaaS Tools

## Organisation des Fichiers

### 📂 Racine du Projet

**Fichiers essentiels** :
- `README.md` - Documentation principale
- `requirements.txt` - Dépendances Python
- `requirements-dev.txt` - Dépendances développement
- `Dockerfile` - Configuration Docker
- `docker-compose.yml` - Configuration Docker Compose dev
- `docker-compose.prod.yml` - Configuration Docker Compose prod
- `LICENSE` - Licence du projet
- `check_modules.py` - Script de vérification des modules

### 📂 Modules SaaS (`saas_*/`)

Tous les modules Odoo sont organisés dans des dossiers séparés :
- `saas_base/` - Module de base
- `saas_portal/` - Portail principal
- `saas_server/` - Serveur SaaS
- `saas_client/` - Client SaaS
- `saas_portal_cache/` - Cache Redis
- etc.

### 📂 Infrastructure (`infrastructure/`)

- `terraform/` - Infrastructure AWS Terraform
- `config/` - Fichiers de configuration production
- `deploy-aws-production.sh` - Script de déploiement
- `README.md` - Documentation déploiement

### 📂 Scripts (`scripts/`)

- `legacy/` - Scripts de migration et fixes temporaires (obsolètes)
- `cleanup_root.sh` - Script de nettoyage

### 📂 Tests (`tests/`)

- `legacy/` - Tests temporaires (obsolètes)

### 📂 Documentation (`docs/`)

- `temp/` - Documentation temporaire
- Documentation principale dans `_LIVRABLES/`

### 📂 Logs (`.logs/`)

- Fichiers de logs (ignorés par Git)

---

## 🧹 Nettoyage Effectué

### Fichiers Déplacés

**Scripts legacy** → `scripts/legacy/`:
- `fix_plan_view.py`
- `fix_plan_view_now.py`
- `fix_plan_view_immediate.sh`
- `force_create_plan_view.py`
- `force_fix_tree_cache.py`
- `recreate_plan_views.py`
- `create_tree_view_compat.py`
- `check_plan_views.py`
- `update_saas_portal.sh`

**Tests legacy** → `tests/legacy/`:
- `test_create_client.py`
- `test_frontend_tree_request.py`
- `test_get_views_unit.py`
- `test_tree_fix.py`
- `test_xml_odoo18.xml`

**Documentation temporaire** → `docs/temp/`:
- `SOLUTION_FINALE_TREE.md`
- `SOLUTION_VUE_TREE_PLANS.md`
- `TEST_CREATION_CLIENT.md`

**Logs** → `.logs/`:
- `odoo.log`
- `saas.log`

---

## ✅ Fichiers Conservés à la Racine

- `README.md` - Documentation principale
- `requirements.txt` - Dépendances
- `Dockerfile` - Docker
- `docker-compose.yml` - Docker Compose
- `check_modules.py` - Script de vérification
- Modules SaaS (`saas_*/`)
- Infrastructure (`infrastructure/`)
- Documentation (`_LIVRABLES/`, `docs/`)

---

## 📝 Règles de Nettoyage

### Ne JAMAIS mettre à la racine :

- Scripts de test temporaires
- Fichiers de logs
- Scripts de migration/fix ponctuels
- Documentation temporaire
- Fichiers de configuration personnels

### Toujours organiser dans :

- `scripts/` - Scripts utilitaires
- `tests/` - Tests
- `docs/` - Documentation
- `.logs/` - Logs

---

## 🔄 Commandes de Nettoyage

```bash
# Nettoyer automatiquement
./scripts/cleanup_root.sh

# Vérifier les modules
python3 check_modules.py
```

