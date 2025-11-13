# 📋 Guide du Fichier .env

## 📍 Emplacement du Fichier .env

Le fichier `.env` doit être placé **à la racine du projet** :

```
/Users/apple/KONDRO/odoo-sass/odoo-saas-tools/
├── .env                    ← ICI (à la racine)
├── .gitignore
├── README.md
├── docker-compose.yml
├── config/
│   ├── docker-compose.prod.yml
│   ├── docker-compose.dev.yml
│   └── ...
├── infrastructure/
│   └── env.example         ← Fichier exemple
└── ...
```

## 🚀 Création du Fichier .env

### Méthode 1 : Copie depuis l'exemple (Recommandé)

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
cp infrastructure/env.example .env
nano .env  # ou votre éditeur préféré
```

### Méthode 2 : Création manuelle

```bash
cd /Users/apple/KONDRO/odoo-sass/odoo-saas-tools
touch .env
nano .env
```

## ⚙️ Utilisation par Docker Compose

Docker Compose lit **automatiquement** le fichier `.env` à la racine du projet lorsque vous utilisez :

```bash
docker compose -f config/docker-compose.prod.yml up -d
```

Les variables définies dans `.env` seront disponibles via `${VARIABLE_NAME}` dans les fichiers docker-compose.

## 🔒 Sécurité

⚠️ **IMPORTANT :** Le fichier `.env` contient des mots de passe et secrets.

- ✅ Le fichier `.env` est automatiquement ignoré par Git (via .gitignore)
- ❌ **NE JAMAIS** commiter le fichier `.env` dans Git
- ✅ Utilisez `infrastructure/env.example` comme template (sans secrets)

## 📝 Variables Principales

Les variables les plus importantes à configurer :

```bash
# PostgreSQL
POSTGRES_PASSWORD=votre_mot_de_passe_securise

# Odoo
ODOO_ADMIN_PASSWD=votre_mot_de_passe_admin

# Domaine
DOMAIN_NAME=votre-domaine.com
EMAIL=votre-email@example.com

# Workers (optionnel)
ODOO_WORKERS=4
ODOO_CRON_THREADS=2
```

## 🔍 Vérification

Pour vérifier que Docker Compose trouve votre fichier `.env` :

```bash
# Vérifier que le fichier existe
ls -la .env

# Tester le chargement des variables
docker compose -f config/docker-compose.prod.yml config | grep POSTGRES_PASSWORD
```

## 📚 Références

- Fichier exemple : `infrastructure/env.example`
- Documentation Docker Compose : https://docs.docker.com/compose/environment-variables/

