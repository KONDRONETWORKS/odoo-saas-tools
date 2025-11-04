# 🔧 Correction : Route `/saas_server/new_database` retourne 404

## 🐛 Problème

Lors de la création d'un template DB depuis un plan, l'erreur suivante apparaît :

```
Error on request: http://localhost:8069/saas_server/new_database
Reason: NOT FOUND 
Message: 404 Not Found
```

## ✅ Solution

Le module `saas_server` n'était pas installé dans la base de données. Il faut l'installer :

```bash
# Arrêter Odoo
pkill -f "odoo-bin"

# Installer le module saas_server
python3.11 odoo/odoo-bin \
  --db_user=odoo \
  --db_password=odoo \
  --db_port=5432 \
  --addons-path=odoo-saas-tools,odoo/addons \
  -d saas-portal-18.local \
  -i saas_server \
  --stop-after-init

# Redémarrer Odoo
python3.11 odoo/odoo-bin \
  --db_user=odoo \
  --db_password=odoo \
  --db_port=5432 \
  --addons-path=odoo-saas-tools,odoo/addons
```

## 📋 Vérification

Pour vérifier que le module est installé :

```sql
SELECT name, state FROM ir_module_module WHERE name = 'saas_server';
```

Le résultat doit être :
```
    name     |   state   
-------------+-----------
 saas_server | installed
```

## ⚠️ Important

Le module `saas_server` doit être installé sur :
- ✅ **Le serveur Portal** (pour recevoir les requêtes)
- ✅ **Chaque serveur distant** (pour créer les bases de données client)

Dans un environnement de développement local, le Portal et le Server sont la même instance, donc une seule installation suffit.

## 🔍 Dépannage

Si la route retourne toujours 404 après l'installation :

1. **Vérifier que le module est chargé** :
   - Vérifier les logs Odoo pour "Module saas_server loaded"
   
2. **Vérifier les imports** :
   - `saas_server/__init__.py` doit contenir `from . import controllers`
   - `saas_server/controllers/__init__.py` doit contenir `from . import main`

3. **Redémarrer Odoo complètement** :
   - Arrêter tous les processus Odoo
   - Redémarrer avec un registre propre

4. **Vérifier la route** :
   ```bash
   curl -v "http://localhost:8069/saas_server/new_database?state=%7B%7D&access_token=test&client_id=test"
   ```

## 📝 Notes

- Le module `saas_server` fournit les endpoints API REST pour créer/gérer les bases de données client
- La route `/saas_server/new_database` nécessite :
  - `state` : JSON contenant les informations de création
  - `access_token` : Token OAuth2 pour l'authentification
  - `client_id` : UUID du client
