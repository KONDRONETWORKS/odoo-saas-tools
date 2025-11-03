# Configuration Odoo SaaS Tools pour Windows

## ✅ Ce qui a été configuré

1. **Environnement virtuel Python** créé dans `venv/`
2. **Dépendances installées** depuis `requirements.txt`
3. **Fichier de configuration** `odoo.conf` adapté pour Windows
4. **Répertoire filestore** créé
5. **Compatibilité Windows** : corrections apportées à `saas.py` pour fonctionner sur Windows

## 📋 Prérequis

Avant de lancer l'application, vous devez avoir :

1. **PostgreSQL** installé et en cours d'exécution
   - Port par défaut : 5432
   - Utilisateur : `postgres` (peut être modifié dans `odoo.conf`)
   - Base de données : `odoo` sera créée automatiquement

2. **Odoo 18.0** installé
   - Chemin par défaut : `../odoo/odoo-bin`
   - Ou spécifier avec `--odoo-script` lors du lancement
   - Les modules doivent être accessibles dans `../odoo/addons`

3. **Python 3.8+** (déjà vérifié ✅)

## 🚀 Démarrage rapide

### Option 1 : Script PowerShell (Recommandé)

```powershell
.\start_saas.ps1
```

Le script vous guidera à travers les étapes.

### Option 2 : Commandes manuelles

1. **Activer l'environnement virtuel :**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Créer et lancer l'application (première fois) :**
   ```powershell
   python saas.py --portal-create --server-create --plan-create --run --odoo-config=odoo.conf
   ```

3. **Ou simplement lancer (si déjà configuré) :**
   ```powershell
   python saas.py --run --odoo-config=odoo.conf
   ```

## ⚙️ Configuration

### Fichier `odoo.conf`

Le fichier a été adapté pour Windows avec les chemins suivants :
- `addons_path = .,../odoo/addons,../odoo/odoo/addons`
- `data_dir = ./filestore`
- `db_user = postgres` (à adapter selon votre configuration PostgreSQL)

**Modifiez selon votre environnement :**
- `db_user` : Nom d'utilisateur PostgreSQL
- `db_password` : Mot de passe PostgreSQL (si nécessaire)
- `addons_path` : Chemins vers les modules Odoo

### Options de lancement

```powershell
# Créer uniquement le portail
python saas.py --portal-create --odoo-config=odoo.conf

# Créer uniquement le serveur
python saas.py --server-create --odoo-config=odoo.conf

# Créer uniquement un plan
python saas.py --plan-create --odoo-config=odoo.conf

# Spécifier un chemin Odoo différent
python saas.py --run --odoo-config=odoo.conf --odoo-script=C:\path\to\odoo\odoo-bin
```

## 🔧 Dépannage

### Erreur : PostgreSQL non accessible
- Vérifiez que PostgreSQL est en cours d'exécution
- Vérifiez les paramètres dans `odoo.conf` (db_host, db_port, db_user, db_password)

### Erreur : Odoo non trouvé
- Vérifiez que Odoo est installé dans `../odoo/`
- Ou utilisez `--odoo-script` pour spécifier le chemin

### Erreur : Port déjà utilisé
- Le port 8069 est peut-être déjà utilisé
- Modifiez `xmlrpc_port` dans `odoo.conf` ou utilisez `--odoo-xmlrpc-port`

## 📚 Documentation complète

Consultez le fichier `README.md` pour la documentation complète du projet.

## 🎯 Accès à l'application

Une fois lancée, l'application sera accessible à :
- **Interface principale** : http://localhost:8069
- **Identifiants par défaut** : admin / admin

---

**Note** : Ce projet nécessite Odoo et PostgreSQL pour fonctionner. Assurez-vous qu'ils sont installés et configurés avant de lancer l'application.

