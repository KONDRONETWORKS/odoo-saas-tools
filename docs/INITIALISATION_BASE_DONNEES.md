# Initialisation de la Base de Données Odoo

## 🔍 Problème

Erreur 500 sur les assets frontend (`web.assets_frontend.min.css`) indiquant que la base de données n'est pas initialisée.

## ✅ Solution : Créer la Base de Données

### Étape 1 : Accéder à la Page de Gestion

1. Ouvrez votre navigateur
2. Accédez à : **http://localhost:8069/web/database/manager**
3. Vous devriez voir la page de gestion des bases de données

### Étape 2 : Créer une Nouvelle Base

1. Cliquez sur **"Create Database"** ou **"Créer une base de données"**

2. Remplissez le formulaire :
   - **Database Name** : `odoo` (ou un autre nom)
   - **Master Password** : `admin` (ou le mot de passe configuré dans `odoo.conf`)
   - **Email** : Votre adresse email
   - **Password** : Votre mot de passe administrateur (pour vous connecter)
   - **Phone** : (optionnel)
   - **Language** : `French / Français`
   - **Country** : `Côte d'Ivoire` ou `Ivory Coast`
   - **Demo data** : Cochez si vous voulez des données de démonstration

3. Cliquez sur **"Create Database"** ou **"Créer"**

### Étape 3 : Attendre l'Initialisation

- L'initialisation peut prendre **1-3 minutes**
- Ne fermez pas la page pendant l'initialisation
- Vous verrez un message de progression

### Étape 4 : Se Connecter

1. Une fois l'initialisation terminée, vous serez redirigé vers la page de login
2. Connectez-vous avec :
   - **Email** : Celui que vous avez saisi
   - **Password** : Le mot de passe administrateur que vous avez défini

### Étape 5 : Vérifier les Assets

1. Après connexion, les assets CSS/JS devraient se charger correctement
2. Si vous voyez encore des erreurs, videz le cache du navigateur :
   - `Ctrl+Shift+Delete` (Windows/Linux)
   - `Cmd+Shift+Delete` (Mac)

## 🔧 Vérification via Ligne de Commande

Pour vérifier si une base existe :

```bash
docker exec saas-postgres-dev psql -U odoo -d postgres -c "\l"
```

## ⚠️ Note Importante

- **Ne créez pas plusieurs bases de données** avec le même nom
- Si une base existe déjà, vous pouvez la sélectionner depuis la page de gestion
- Le Master Password doit correspondre à celui dans `odoo.conf` (par défaut : `admin`)

## 📝 Configuration du Master Password

Si vous avez besoin de changer le Master Password :

```bash
# Utiliser le script fourni
python3 scripts/update_master_password.py admin --config odoo.conf.docker
```

Puis redémarrez le conteneur :

```bash
docker compose -f config/docker-compose.simple.yml restart odoo
```

## 🆘 Si le Problème Persiste

1. Vérifiez les logs : `docker compose -f config/docker-compose.simple.yml logs odoo --tail 100`
2. Vérifiez que PostgreSQL est accessible
3. Vérifiez les permissions sur les fichiers

