# ⚙️ Configuration Odoo SaaS Tools pour Windows

## 📋 Prérequis

### 1. PostgreSQL
- **Installation** : Téléchargez depuis https://www.postgresql.org/download/windows/
- **Configuration** : Par défaut utilise `postgres` / `postgres`
- **Vérification** : 
  ```powershell
  # Vérifier que PostgreSQL tourne
  Get-Service -Name postgresql*
  ```

### 2. Docker Desktop (Optionnel mais recommandé)
- **Installation** : https://www.docker.com/products/docker-desktop
- **Alternative** : Installer Odoo 18.0 localement

## 🔧 Configuration

### Fichier `config/odoo.conf`

Configuration par défaut pour Windows :

```ini
[options]
admin_passwd = admin
db_host = localhost
db_port = 5432
db_user = postgres          # Utilisateur PostgreSQL Windows par défaut
db_password = postgres      # Mot de passe PostgreSQL
db_name = odoo
addons_path = .
data_dir = ./filestore
xmlrpc_port = 8069
longpolling_port = 8072
log_level = info
logfile = ./odoo.log        # Logs dans le répertoire courant
without_demo = True
```

**Adapter selon votre installation PostgreSQL** :
- Si votre utilisateur est différent : changez `db_user` et `db_password`
- Si PostgreSQL utilise un autre port : changez `db_port`

### Options de lancement saas.py

#### Avec Docker (Recommandé)
```powershell
# 1. Démarrer Docker
docker compose -f config/docker-compose.windows.yml up -d

# 2. Lancer saas.py (utilise Odoo dans Docker)
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

#### Sans Docker (Odoo installé localement)
```powershell
# Spécifier le chemin vers odoo-bin
python saas.py --portal-create --server-create --plan-create --run --odoo-script=C:\chemin\vers\odoo\odoo-bin --odoo-config=config/odoo.conf
```

## 🔍 Diagnostic

### Vérifier PostgreSQL
```powershell
# Test de connexion
.\venv\Scripts\python.exe -c "import psycopg2; psycopg2.connect(host='localhost', port=5432, user='postgres', password='postgres')"
```

### Vérifier le port 8069
```powershell
# Vérifier si le port est ouvert
Test-NetConnection -ComputerName localhost -Port 8069

# Voir qui utilise le port
netstat -ano | Select-String ":8069"
```

### Vérifier les logs
```powershell
# Logs saas.py (dans la console)
# Logs Odoo (si configuré)
Get-Content odoo.log -Tail 50
```

## 🐛 Problèmes Courants

### "Odoo script not found"
**Solution** :
- Utiliser Docker avec `--use-existed-odoo`
- Ou installer Odoo et spécifier le chemin avec `--odoo-script`

### "Connection refused" sur PostgreSQL
**Solutions** :
1. Vérifier que PostgreSQL est démarré : `Get-Service postgresql*`
2. Vérifier les identifiants dans `config/odoo.conf`
3. Tester la connexion manuellement

### Port 8069 déjà utilisé
**Solutions** :
1. Trouver le processus : `netstat -ano | Select-String ":8069"`
2. Arrêter le processus ou changer le port dans `config/odoo.conf`

### Rien ne s'affiche dans le navigateur
**Vérifications** :
1. Le port 8069 est-il ouvert ? `Test-NetConnection localhost -Port 8069`
2. Odoo est-il démarré ? (Docker ou local)
3. Consulter les logs : `Get-Content odoo.log -Tail 50`
4. Vérifier l'URL : http://localhost:8069 (pas https)

## 🚀 Démarrage Rapide

### Méthode 1 : Docker (Recommandé)
```powershell
# Tout en une fois
docker compose -f config/docker-compose.windows.yml up -d
Start-Sleep -Seconds 15
.\venv\Scripts\Activate.ps1
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

### Méthode 2 : Odoo Local
```powershell
.\venv\Scripts\Activate.ps1
python saas.py --portal-create --server-create --plan-create --run --odoo-script=C:\odoo\odoo-bin --odoo-config=config/odoo.conf
```

## 📝 Commandes Utiles

```powershell
# Vérifier l'état
docker compose -f config/docker-compose.windows.yml ps
docker compose -f config/docker-compose.windows.yml logs -f

# Arrêter Docker
docker compose -f config/docker-compose.windows.yml down

# Voir les processus Python/Odoo
Get-Process | Where-Object { $_.ProcessName -like "*python*" -or $_.ProcessName -like "*odoo*" }
```

