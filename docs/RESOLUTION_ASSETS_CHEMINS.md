# Résolution des Erreurs 500 sur les Assets - Correction des Chemins

## 🔍 Problème Identifié

Erreur 500 sur les assets (frontend et backend) avec l'erreur :
```
FileNotFoundError: [Errno 2] No such file or directory: 
'/var/lib/odoo/filestore/filestore/odoo/odoo/...'
```

**Causes principales :**

- Les `store_fname` dans `ir_attachment` contenaient le préfixe `odoo/`, alors qu'Odoo ajoute déjà automatiquement le nom de la base de données au chemin final ⇒ double `odoo/odoo/`.
- Après modification de `data_dir`, les fichiers historiques sont restés dans l'ancien dossier `filestore/odoo/…` → il faut les recopier vers le nouveau répertoire d'attente d'Odoo.

## ✅ Solution

### Principe

Dans Odoo, le chemin complet d'un fichier est construit comme suit :
```
chemin_complet = data_dir + '/' + nom_base + '/' + store_fname
```

Où :
- `data_dir` = `/var/lib/odoo/filestore` (configuré dans `odoo.conf`)
- `nom_base` = `odoo` (nom de la base de données)
- `store_fname` = chemin relatif (ex: `f1/f12faee5341e22423805816f3f6921ffe694928e`)

**Le `store_fname` ne doit PAS contenir le préfixe `odoo/`.**

### Correction SQL

```sql
-- Enlever le préfixe 'odoo/' de tous les store_fname
UPDATE ir_attachment 
SET store_fname = SUBSTRING(store_fname FROM 6) 
WHERE store_fname LIKE 'odoo/%' 
  AND res_model = 'ir.ui.view';
```

### Migration des fichiers existants

Si vous aviez déjà des fichiers sous `filestore/odoo/…`, recopiez-les dans le nouveau répertoire attendu (`<data_dir>/odoo/`) :

```bash
docker exec saas-odoo-dev /bin/sh -c "cd /var/lib/odoo/filestore && cp -a filestore/odoo/. odoo/"
```

> Adaptez les chemins si vous n'êtes pas dans Docker. L'objectif est d'avoir les mêmes fichiers sous `<data_dir>/<nom_base>/…`.

### Vérification

```sql
-- Vérifier que les chemins sont corrects
SELECT id, name, store_fname 
FROM ir_attachment 
WHERE name LIKE '%assets_%' 
  AND res_model = 'ir.ui.view' 
LIMIT 5;
```

Les `store_fname` doivent ressembler à : `f1/f12faee5341e22423805816f3f6921ffe694928e`
**Pas** : `odoo/f1/f12faee5341e22423805816f3f6921ffe694928e`

## 🔧 Script de Correction Automatique

```python
import sys
sys.path.insert(0, '/usr/lib/python3/dist-packages')
import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config

config.parse_config(['--config=/etc/odoo/odoo.conf'])
registry = odoo.registry('odoo')

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Trouver tous les assets avec 'odoo/' dans le chemin
    assets = env['ir.attachment'].search([
        ('store_fname', 'like', 'odoo/%'),
        ('res_model', '=', 'ir.ui.view')
    ])
    
    corrected = 0
    for att in assets:
        # Enlever le préfixe 'odoo/'
        new_fname = att.store_fname[5:]  # Enlever 'odoo/'
        att.store_fname = new_fname
        corrected += 1
    
    if corrected > 0:
        cr.commit()
        print(f'✅ {corrected} chemins corrigés')
    else:
        print('ℹ️  Aucun chemin à corriger')
```

## 📝 Prévention

### Configuration Correcte

Dans `odoo.conf` (local) et/ou `odoo.conf.docker` (conteneur) :
```ini
data_dir = /var/lib/odoo
```

**Pas :**
```ini
data_dir = /var/lib/odoo/filestore  # ❌ CRÉE UN DOUBLE `filestore/`
```

### Structure des Fichiers

Les fichiers doivent être organisés comme suit :
```
/var/lib/odoo/filestore/
  └── odoo/                    # Nom de la base de données
      └── f1/
          └── f12faee5341e22423805816f3f6921ffe694928e
```

Le `store_fname` dans la base est : `f1/f12faee5341e22423805816f3f6921ffe694928e`

## 🆘 Si le Problème Persiste

1. **Vérifier les logs** :
   ```bash
   docker compose -f config/docker-compose.simple.yml logs odoo --tail 100 | grep FileNotFoundError
   ```

2. **Vérifier la configuration** :
   ```bash
   docker exec saas-odoo-dev cat /etc/odoo/odoo.conf | grep data_dir
   ```

3. **Vérifier les chemins dans la base** :
   ```sql
   SELECT name, store_fname 
   FROM ir_attachment 
   WHERE name LIKE '%assets_%' 
   LIMIT 5;
   ```

4. **Supprimer et régénérer les assets** :
   ```python
   # Supprimer tous les assets
   env['ir.attachment'].search([
       ('name', 'like', 'assets_'),
       ('res_model', '=', 'ir.ui.view')
   ]).unlink()
   
   # Vider le cache
   env['ir.qweb'].clear_caches()
   ```

5. **Redémarrer Odoo** :
   ```bash
   docker compose -f config/docker-compose.simple.yml restart odoo
   ```

## ✅ Vérification Finale

Après correction, tester :
```bash
curl -I "http://localhost:8069/web/assets/7907478/web.assets_web.min.css?db=odoo"
```

Devrait retourner `HTTP/1.0 200 OK` au lieu de `500`.

