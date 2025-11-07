# Résolution de l'Erreur 500 - Chemin Filestore Double

## 🔍 Problème Identifié

Erreur 500 sur les assets frontend avec l'erreur suivante dans les logs :

```
FileNotFoundError: [Errno 2] No such file or directory: 
'/var/lib/odoo/filestore/filestore/odoo/8d/8d7708fd728f11ec5a250bc33277609734fac2b3'
```

**Cause :** Le chemin du filestore contient un double `filestore` : `/var/lib/odoo/filestore/filestore/odoo/...`

## ✅ Solution Appliquée

### Étape 1 : Corriger les Chemins dans la Base de Données

Les enregistrements `ir_attachment` contenaient des chemins avec `filestore/filestore/` au lieu de `filestore/`.

**Commande SQL de correction :**

```sql
UPDATE ir_attachment 
SET store_fname = REPLACE(store_fname, 'filestore/filestore/', 'filestore/') 
WHERE store_fname LIKE 'filestore/filestore/%';
```

### Étape 2 : Redémarrer Odoo

Après la correction, redémarrer le conteneur Odoo :

```bash
docker compose -f config/docker-compose.simple.yml restart odoo
```

### Étape 3 : Vérifier

Attendre 15-30 secondes puis tester :

```bash
curl -I "http://localhost:8069/web/assets/fbee2df/web.assets_frontend.min.css?db=odoo"
```

Devrait retourner `HTTP/1.0 200 OK` au lieu de `500`.

## 🔧 Prévention

### Vérifier la Configuration `data_dir`

Dans `odoo.conf.docker`, la configuration doit être :

```ini
data_dir = /var/lib/odoo/filestore
```

**Pas :**
```ini
data_dir = /var/lib/odoo/filestore/filestore  # ❌ INCORRECT
```

### Vérifier les Chemins dans la Base

Pour vérifier s'il y a encore des chemins incorrects :

```sql
SELECT COUNT(*) FROM ir_attachment 
WHERE store_fname LIKE 'filestore/filestore%';
```

Devrait retourner `0`.

## 📝 Notes

- Cette erreur peut se produire si la configuration `data_dir` a été modifiée après la création de la base de données
- Les assets sont stockés dans `ir_attachment` avec le chemin relatif au `data_dir`
- Si le `data_dir` change, les chemins dans la base doivent être mis à jour

## 🆘 Si le Problème Persiste

1. Vérifier les logs : `docker compose -f config/docker-compose.simple.yml logs odoo --tail 100`
2. Vérifier la configuration : `docker exec saas-odoo-dev cat /etc/odoo/odoo.conf | grep data_dir`
3. Vérifier les permissions : `docker exec saas-odoo-dev ls -la /var/lib/odoo/filestore/`
4. Vider le cache des assets : Se connecter à Odoo > Paramètres > Technique > Base de données > Vider le cache

