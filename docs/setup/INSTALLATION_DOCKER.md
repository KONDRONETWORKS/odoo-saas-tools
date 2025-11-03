# 🐳 Installation Docker Desktop pour Windows

## 📥 Installation

### Méthode 1 : Téléchargement Direct

1. **Télécharger Docker Desktop** :
   - Site officiel : https://www.docker.com/products/docker-desktop
   - Ou directement : https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

2. **Installer** :
   - Exécuter l'installateur téléchargé
   - Suivre l'assistant d'installation
   - Redémarrer l'ordinateur si demandé

3. **Démarrer Docker Desktop** :
   - Chercher "Docker Desktop" dans le menu Démarrer
   - Lancer l'application
   - Attendre que Docker soit complètement démarré (icône dans la barre des tâches)

### Méthode 2 : Via Winget (Windows Package Manager)

```powershell
# Si winget est disponible
winget install Docker.DockerDesktop
```

### Méthode 3 : Via Chocolatey

```powershell
# Si Chocolatey est installé
choco install docker-desktop
```

---

## ✅ Vérification de l'Installation

### Vérifier que Docker est installé

```powershell
docker --version
```

### Vérifier que Docker Desktop est démarré

```powershell
docker info
```

Si vous voyez des informations sur Docker, c'est que tout fonctionne.

### Vérifier Docker Compose

```powershell
docker compose version
```

---

## 🚀 Démarrage des Conteneurs

Une fois Docker Desktop installé et démarré :

```powershell
# Depuis la racine du projet
docker compose -f config/docker-compose.windows.yml up -d
```

### Vérifier l'état

```powershell
docker compose -f config/docker-compose.windows.yml ps
```

Vous devriez voir deux conteneurs :
- `saas-postgres` (PostgreSQL)
- `saas-odoo` (Odoo)

### Voir les logs

```powershell
docker compose -f config/docker-compose.windows.yml logs -f
```

---

## 🔧 Dépannage

### Docker n'est pas dans le PATH

Si `docker --version` ne fonctionne pas après l'installation :

1. Fermer tous les terminaux PowerShell
2. Redémarrer Docker Desktop
3. Ouvrir un nouveau terminal PowerShell
4. Réessayer `docker --version`

### Docker Desktop ne démarre pas

1. Vérifier les prérequis :
   - Windows 10/11 64-bit
   - WSL 2 activé (Docker Desktop peut le proposer d'installer)
   - Virtualisation activée dans le BIOS

2. Redémarrer l'ordinateur

3. Vérifier les logs dans Docker Desktop (Settings > Troubleshoot)

### Les conteneurs ne démarrent pas

```powershell
# Voir les logs d'erreur
docker compose -f config/docker-compose.windows.yml logs

# Redémarrer les conteneurs
docker compose -f config/docker-compose.windows.yml restart

# Si problème, recréer
docker compose -f config/docker-compose.windows.yml down
docker compose -f config/docker-compose.windows.yml up -d
```

---

## 📝 Commandes Utiles

```powershell
# Démarrer les conteneurs
docker compose -f config/docker-compose.windows.yml up -d

# Arrêter les conteneurs
docker compose -f config/docker-compose.windows.yml down

# Voir l'état
docker compose -f config/docker-compose.windows.yml ps

# Voir les logs
docker compose -f config/docker-compose.windows.yml logs -f

# Redémarrer
docker compose -f config/docker-compose.windows.yml restart

# Arrêter et supprimer les volumes (⚠️ supprime les données)
docker compose -f config/docker-compose.windows.yml down -v
```

---

## 🎯 Prochaines Étapes

Une fois Docker démarré et les conteneurs lancés :

```powershell
# 1. Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# 2. Lancer saas.py
python saas.py --portal-create --server-create --plan-create --use-existed-odoo --odoo-config=config/odoo.conf
```

L'application sera accessible sur http://localhost:8069

