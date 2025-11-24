# 📁 Guide d'Emplacement du Projet sur Serveur Ubuntu

## 🎯 Emplacement Recommandé

Le projet doit être placé dans :

```
/opt/odoo-saas-tools/
```

## ✅ Pourquoi `/opt/` ?

- ✅ **Standard Linux** : `/opt/` est destiné aux logiciels optionnels/add-on
- ✅ **Permissions** : Facile à gérer avec un utilisateur dédié
- ✅ **Séparation** : Isolé des fichiers système
- ✅ **Convention** : Suit les bonnes pratiques Linux

## 🚀 Installation sur Ubuntu

### Méthode 1 : Clonage depuis GitHub (Recommandé)

```bash
# Se connecter au serveur Ubuntu
ssh user@votre-serveur-ubuntu

# Créer le répertoire avec les bonnes permissions
sudo mkdir -p /opt/odoo-saas-tools
sudo chown $USER:$USER /opt/odoo-saas-tools

# Cloner le projet
cd /opt
git clone https://github.com/KONDRONETWORKS/odoo-saas-tools.git

# Vérifier
ls -la /opt/odoo-saas-tools
```

### Méthode 2 : Transfert depuis votre machine locale

```bash
# Depuis votre machine locale
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools

# Transférer le projet (excluant .git pour économiser l'espace)
rsync -avz --exclude '.git' \
  --exclude 'filestore' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  ./ user@votre-serveur:/opt/odoo-saas-tools/

# Ou utiliser scp pour un transfert simple
scp -r . user@votre-serveur:/opt/odoo-saas-tools/
```

### Méthode 3 : Utilisation du script de déploiement

```bash
# Le script deploy-ubuntu-vm.sh fait tout automatiquement
sudo ./infrastructure/deploy-ubuntu-vm.sh
```

## 👤 Utilisateur et Permissions

### Créer un utilisateur dédié (Recommandé)

```bash
# Créer l'utilisateur odoo
sudo useradd -m -s /bin/bash odoo

# Donner les permissions
sudo chown -R odoo:odoo /opt/odoo-saas-tools

# Ajouter l'utilisateur au groupe docker (si Docker est utilisé)
sudo usermod -aG docker odoo
```

### Structure des permissions

```
/opt/odoo-saas-tools/
├── .env                    (odoo:odoo, 600)
├── filestore/              (odoo:odoo, 755)
├── config/                 (odoo:odoo, 755)
└── ...                     (odoo:odoo, 755)
```

## 📋 Structure Complète sur le Serveur

```
/opt/odoo-saas-tools/
├── .env                    ← Fichier de configuration (créé manuellement)
├── .gitignore
├── README.md
├── docker-compose.yml
├── config/
│   ├── docker-compose.prod.yml
│   ├── docker-compose.ubuntu-vm.yml
│   └── ...
├── infrastructure/
│   ├── deploy-ubuntu-vm.sh
│   └── ...
├── saas_portal/
├── kondro/
├── filestore/              ← Données Odoo
└── ...
```

## 🔧 Configuration Post-Installation

### 1. Créer le fichier .env

```bash
cd /opt/odoo-saas-tools
cp infrastructure/env.example .env
nano .env  # Modifier les valeurs
```

### 2. Vérifier les permissions

```bash
# Vérifier que l'utilisateur odoo peut accéder
sudo -u odoo ls -la /opt/odoo-saas-tools

# Si nécessaire, corriger les permissions
sudo chown -R odoo:odoo /opt/odoo-saas-tools
```

### 3. Démarrer les services

```bash
cd /opt/odoo-saas-tools

# Avec Docker Compose
docker compose -f config/docker-compose.ubuntu-vm.yml up -d

# Ou avec le script
./scripts/start_saas.sh start
```

## 🔒 Sécurité

### Permissions recommandées

```bash
# Fichier .env (sensible)
chmod 600 /opt/odoo-saas-tools/.env

# Répertoire principal
chmod 755 /opt/odoo-saas-tools

# Filestore (données)
chmod 755 /opt/odoo-saas-tools/filestore
```

### Firewall

```bash
# Autoriser uniquement les ports nécessaires
sudo ufw allow ssh
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## 📊 Espace Disque Requis

| Composant | Espace Requis |
|-----------|---------------|
| Code source | ~500 MB |
| Modules OCA | ~200 MB |
| Filestore (vide) | ~100 MB |
| Docker images | ~2 GB |
| Base de données | Variable |
| **Total minimum** | **~3 GB** |
| **Recommandé** | **50+ GB** |

## 🔄 Mise à Jour

```bash
cd /opt/odoo-saas-tools

# Mettre à jour depuis Git
git pull origin 18.0

# Redémarrer les services
docker compose -f config/docker-compose.ubuntu-vm.yml restart
```

## 📝 Notes Importantes

1. **Ne jamais placer dans `/home/`** : Risque de permissions et problèmes de sécurité
2. **Ne jamais placer dans `/var/www/`** : Réservé pour les applications web classiques
3. **Utiliser `/opt/`** : Standard pour les applications tierces
4. **Utilisateur dédié** : Créer un utilisateur `odoo` pour isoler les permissions

## 🆘 Dépannage

### Problème de permissions

```bash
# Vérifier les permissions
ls -la /opt/odoo-saas-tools

# Corriger
sudo chown -R odoo:odoo /opt/odoo-saas-tools
```

### Problème d'espace disque

```bash
# Vérifier l'espace
df -h /opt

# Nettoyer Docker
docker system prune -a
```

---

**Dernière mise à jour :** Novembre 2025

