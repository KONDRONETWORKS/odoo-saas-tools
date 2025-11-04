# 🚀 Instructions de Démarrage - État Actuel

## ✅ Docker est Démarré

Les conteneurs sont en cours d'exécution :
- ✅ PostgreSQL (port 5432) - **HEALTHY**
- ✅ Odoo (port 8069) - **DÉMARRAGE**

## 🌐 Accès à l'Application

**URL** : http://localhost:8069

⚠️ **Note** : Au premier démarrage, Odoo peut prendre 1-2 minutes pour initialiser la base de données.

## 📋 Prochaines Étapes

### 1. Attendre l'Initialisation Complète

Odoo doit créer sa base de données. Attendez 30-60 secondes puis :

1. Ouvrez votre navigateur : **http://localhost:8069**
2. Vous devriez voir la page de création de base de données Odoo

### 2. Initialiser la Base de Données

Sur la page Odoo :
- **Nom de la base** : `odoo` (ou autre nom)
- **Email** : votre email
- **Mot de passe** : choisissez un mot de passe admin
- **Langue** : Français
- **Pays** : Votre pays
- Cliquez sur **Créer la base de données**

### 3. Lancer saas.py

Une fois la base créée via l'interface web, vous pouvez lancer saas.py :

```powershell
.\venv\Scripts\Activate.ps1
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

## 🔍 Vérification

### Vérifier que tout fonctionne :

```powershell
# 1. Vérifier les conteneurs
$env:PATH += ";C:\Program Files\Docker\Docker\resources\bin"
docker compose -f config/docker-compose.windows.yml ps

# 2. Vérifier les logs Odoo
docker compose -f config/docker-compose.windows.yml logs -f odoo

# 3. Vérifier le port
Test-NetConnection localhost -Port 8069
```

## 🐛 Si Rien Ne S'Affiche dans le Navigateur

1. **Attendre plus longtemps** (Odoo initialise la DB)
2. **Vérifier les logs** :
   ```powershell
   docker compose -f config/docker-compose.windows.yml logs odoo
   ```
3. **Vérifier que le port est ouvert** :
   ```powershell
   Test-NetConnection localhost -Port 8069
   ```
4. **Essayer en navigation privée** (cache du navigateur)

## 📝 Commandes Utiles

```powershell
# Ajouter Docker au PATH (si besoin dans une nouvelle session)
$env:PATH += ";C:\Program Files\Docker\Docker\resources\bin"

# Voir l'état
docker compose -f config/docker-compose.windows.yml ps

# Voir les logs en continu
docker compose -f config/docker-compose.windows.yml logs -f

# Arrêter
docker compose -f config/docker-compose.windows.yml down

# Redémarrer
docker compose -f config/docker-compose.windows.yml restart
```

---

**État Actuel** : 
- ✅ Docker démarré
- ✅ Conteneurs en cours d'exécution
- ⏳ En attente de l'initialisation complète d'Odoo (30-60 secondes)
- 🌐 Accès : http://localhost:8069

