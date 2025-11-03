# 🚀 Guide de Démarrage Complet - Odoo SaaS Tools Windows

## 📋 Résumé de la Configuration

### ✅ Ce qui est configuré

1. **saas.py** : Adapté pour Windows avec :
   - Gestion d'erreurs améliorée
   - Recherche automatique d'Odoo sur Windows
   - Messages d'erreur clairs
   - Logs dans `saas.log`

2. **config/odoo.conf** : Configuration adaptée Windows :
   - `db_user = postgres` (Windows par défaut)
   - `db_password = postgres`
   - `logfile = ./odoo.log` (logs locaux)
   - Chemins relatifs pour Windows

3. **Docker Compose** : Prêt dans `config/docker-compose.windows.yml`

---

## 🔍 Diagnostic Actuel

### Vérifier l'état des services

```powershell
# PostgreSQL
Test-NetConnection localhost -Port 5432

# Odoo
Test-NetConnection localhost -Port 8069

# Docker (si installé)
docker --version
docker compose -f config/docker-compose.windows.yml ps
```

### Consulter les logs

```powershell
# Logs saas.py
Get-Content saas.log -Tail 50

# Logs Odoo
Get-Content odoo.log -Tail 50

# Logs Docker (si utilisé)
docker compose -f config/docker-compose.windows.yml logs -f
```

---

## 🎯 Options de Démarrage

### Option A : Avec Docker (Recommandé)

Si Docker Desktop est installé :

```powershell
# 1. Démarrer Docker
docker compose -f config/docker-compose.windows.yml up -d

# 2. Attendre 15-20 secondes que les services démarrent

# 3. Vérifier l'état
docker compose -f config/docker-compose.windows.yml ps

# 4. Lancer saas.py
.\venv\Scripts\Activate.ps1
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

**Avantages** :
- Pas besoin d'installer Odoo localement
- PostgreSQL et Odoo dans des conteneurs isolés
- Configuration simplifiée

### Option B : Sans Docker (Odoo Local)

Si Odoo 18.0 est installé localement :

```powershell
# 1. Vérifier PostgreSQL
Get-Service postgresql*

# 2. Adapter config/odoo.conf avec vos identifiants PostgreSQL

# 3. Lancer saas.py avec le chemin Odoo
.\venv\Scripts\Activate.ps1
python saas.py --portal-create --server-create --plan-create --run --odoo-script=C:\chemin\vers\odoo\odoo-bin --odoo-config=config/odoo.conf
```

### Option C : Utiliser Odoo existant (port 8069 déjà ouvert)

Si Odoo tourne déjà (via Docker ou autre) :

```powershell
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

---

## 🐛 Problèmes Courants et Solutions

### 1. "Rien ne s'affiche dans le navigateur"

**Diagnostic** :
```powershell
# Vérifier que le port 8069 est ouvert
Test-NetConnection localhost -Port 8069

# Si False, Odoo n'est pas démarré
```

**Solutions** :
- Si Docker : `docker compose -f config/docker-compose.windows.yml up -d`
- Si local : Vérifier qu'Odoo est lancé
- Attendre 30-60 secondes pour le démarrage complet

### 2. "Odoo script not found"

**Message** : `ERROR: Odoo script not found: ../odoo/odoo-bin`

**Solutions** :
- **Option 1 (Recommandée)** : Utiliser Docker
  ```powershell
  docker compose -f config/docker-compose.windows.yml up -d
  python saas.py --use-existed-odoo ...
  ```
- **Option 2** : Installer Odoo et spécifier le chemin
  ```powershell
  python saas.py --odoo-script=C:\odoo\odoo-bin ...
  ```

### 3. "Connection refused" PostgreSQL

**Diagnostic** :
```powershell
# Vérifier PostgreSQL
Get-Service postgresql*
Test-NetConnection localhost -Port 5432
```

**Solutions** :
- Démarrer PostgreSQL : `Start-Service postgresql-x64-XX`
- Vérifier les identifiants dans `config/odoo.conf`
- Adapter `db_user` et `db_password` selon votre installation

### 4. Port 8069 déjà utilisé

**Diagnostic** :
```powershell
netstat -ano | Select-String ":8069"
```

**Solutions** :
- Arrêter le processus utilisant le port
- Ou changer le port dans `config/odoo.conf` : `xmlrpc_port = 8069` → `xmlrpc_port = 8070`

---

## 📊 Vérification Finale

Une fois tout lancé correctement :

1. **Port 8069 ouvert** :
   ```powershell
   Test-NetConnection localhost -Port 8069  # Doit retourner True
   ```

2. **Accès navigateur** :
   - Ouvrir : http://localhost:8069
   - Identifiants par défaut : `admin` / `admin`

3. **Logs sans erreurs** :
   ```powershell
   Get-Content saas.log -Tail 20
   Get-Content odoo.log -Tail 20
   ```

---

## 📝 Commandes de Maintenance

```powershell
# Arrêter Docker
docker compose -f config/docker-compose.windows.yml down

# Redémarrer Docker
docker compose -f config/docker-compose.windows.yml restart

# Voir les logs Docker en continu
docker compose -f config/docker-compose.windows.yml logs -f

# Nettoyer les logs
Remove-Item saas.log, odoo.log -ErrorAction SilentlyContinue
```

---

## 🔗 Documentation

- **Configuration détaillée** : `docs/setup/CONFIGURATION_WINDOWS.md`
- **Démarrage rapide** : `docs/setup/DEMARRAGE_RAPIDE.md`
- **Documentation principale** : `README.md`

---

## 💡 Astuce

Pour un démarrage automatique, créez un fichier `start.ps1` à la racine :

```powershell
# start.ps1
docker compose -f config/docker-compose.windows.yml up -d
Start-Sleep -Seconds 15
.\venv\Scripts\Activate.ps1
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

Puis lancez : `.\start.ps1`

