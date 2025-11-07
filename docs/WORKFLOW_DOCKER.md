# Workflow de Développement avec Docker

## 🔄 Après Modification du Code

### 1. **Modifications de Code Python (.py)**

**Un simple restart suffit généralement** car les fichiers sont montés en volume :

```bash
# Redémarrer le conteneur Odoo
docker compose -f config/docker-compose.simple.yml restart odoo

# OU redémarrer tous les services
docker compose -f config/docker-compose.simple.yml restart
```

**⚠️ Exception :** Si vous modifiez le `__manifest__.py` ou ajoutez de nouveaux modèles/champs :
- Redémarrer le conteneur
- **Mettre à jour le module dans Odoo** : Apps > Rechercher le module > Mettre à jour

### 2. **Modifications de Vues XML (.xml)**

**Deux options :**

**Option A (Recommandée) :**
```bash
# Redémarrer le conteneur
docker compose -f config/docker-compose.simple.yml restart odoo

# Puis mettre à jour le module dans Odoo
# Apps > Rechercher le module > Mettre à jour
```

**Option B (Plus rapide pour développement) :**
- Redémarrer le conteneur
- Vider le cache navigateur (Ctrl+Shift+R ou Cmd+Shift+R)
- Les changements XML sont souvent pris en compte automatiquement

### 3. **Nouveaux Modules**

**Étapes complètes :**

1. **Ajouter le volume dans docker-compose.simple.yml** (si nouveau module)
   ```yaml
   - ../nouveau_module:/mnt/extra-addons/nouveau_module
   ```

2. **Redémarrer le conteneur**
   ```bash
   docker compose -f config/docker-compose.simple.yml restart odoo
   ```

3. **Mettre à jour la liste des modules dans Odoo**
   - Apps > Mettre à jour la liste des applications

4. **Installer le module**
   - Apps > Rechercher le module > Installer

### 4. **Modifications de Fichiers Statiques (CSS/JS)**

**Workflow :**
```bash
# Redémarrer le conteneur
docker compose -f config/docker-compose.simple.yml restart odoo

# Vider le cache navigateur (très important !)
# Chrome/Edge: Ctrl+Shift+R (Windows) ou Cmd+Shift+R (Mac)
# Firefox: Ctrl+F5 ou Cmd+Shift+R
```

**Si les assets ne se chargent toujours pas :**
```bash
# Vider le cache Odoo des assets
docker exec saas-odoo-dev odoo shell -d odoo --no-http <<EOF
env['ir.attachment'].search([('name', 'like', 'web.assets')]).unlink()
env['ir.qweb'].clear_caches()
EOF

# Redémarrer
docker compose -f config/docker-compose.simple.yml restart odoo
```

### 5. **Modifications de Configuration (odoo.conf)**

**⚠️ Attention :** Le fichier `odoo.conf.docker` est monté en **lecture seule** (`:ro`)

**Pour modifier la config :**
1. Modifier `odoo.conf.docker` localement
2. Redémarrer le conteneur
3. Les changements seront pris en compte

**Si vous devez modifier la config depuis le conteneur :**
- Utiliser les variables d'environnement dans `docker-compose.simple.yml`
- Ou modifier le volume mount pour `:rw` (non recommandé)

## 📋 Checklist Rapide

**Après modification du code :**

- [ ] Les fichiers sont montés en volume dans `docker-compose.simple.yml` ?
- [ ] Redémarrer le conteneur : `docker compose restart odoo`
- [ ] Si modification `__manifest__.py` ou nouveaux champs : Mettre à jour le module dans Odoo
- [ ] Si modification CSS/JS : Vider le cache navigateur
- [ ] Si nouveau module : Ajouter le volume + Mettre à jour la liste des apps

## 🚀 Commandes Utiles

```bash
# Voir les logs en temps réel
docker compose -f config/docker-compose.simple.yml logs -f odoo

# Redémarrer uniquement Odoo
docker compose -f config/docker-compose.simple.yml restart odoo

# Redémarrer tous les services
docker compose -f config/docker-compose.simple.yml restart

# Reconstruire complètement (si problème)
docker compose -f config/docker-compose.simple.yml down
docker compose -f config/docker-compose.simple.yml up -d

# Accéder au shell du conteneur
docker exec -it saas-odoo-dev bash

# Vérifier que les modules sont bien montés
docker exec saas-odoo-dev ls -la /mnt/extra-addons/ | grep saas_sysadmin_ovh
```

## ⚡ Mode Développement Rapide

Pour un développement actif, vous pouvez utiliser le mode `--dev=all` :

```bash
# Modifier la commande dans docker-compose.simple.yml
command: >
  odoo
  --config=/etc/odoo/odoo.conf
  --dev=all
  # ... autres options
```

**Avantages :**
- Rechargement automatique des vues XML
- Pas besoin de mettre à jour les modules pour les vues
- Meilleur pour le développement

**Inconvénients :**
- Plus lent au démarrage
- Consomme plus de mémoire
- Non recommandé en production

