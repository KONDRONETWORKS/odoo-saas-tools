# Résolution de l'Erreur "null is not an object (evaluating 'n.parentElement.closest')"

## 🔍 Problème

Erreur JavaScript dans le module `website` :
```
TypeError: null is not an object (evaluating 'n.parentElement.closest')
```

**Cause :** Le module `website` essaie d'accéder à un élément DOM qui n'existe plus ou qui n'a pas de parent.

## ✅ Solutions

### Solution 1 : Recharger la page (Rapide)

Parfois, c'est juste un problème de timing avec le DOM :

1. **Recharger complètement la page** : `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)
2. **Vider le cache navigateur** si nécessaire
3. Réessayer l'action

### Solution 2 : Désactiver temporairement le mode dev

Le mode `--dev=all` charge les assets en mode debug qui peuvent causer des problèmes :

**Modifier `config/docker-compose.simple.yml` :**

```yaml
command: >
  odoo
  --config=/etc/odoo/odoo.conf
  --db_host=postgres
  --db_user=odoo
  --db_password=odoo
  --addons-path=/mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
  --data-dir=/var/lib/odoo
  --xmlrpc-port=8069
  --gevent-port=8072
  --workers=3
  --max-cron-threads=2
  --without-demo=all
  --db-filter=.*
  --log-level=info
  --logfile=/var/log/odoo/odoo.log
  # --dev=all  # Commenter cette ligne
```

Puis redémarrer :
```bash
docker compose -f config/docker-compose.simple.yml restart odoo
```

### Solution 3 : Mettre à jour le module website

Si le module `website` n'est pas à jour :

1. Aller dans **Apps**
2. Rechercher **"Website"**
3. Mettre à jour le module si disponible
4. Redémarrer Odoo

### Solution 4 : Vérifier les modules installés

Cette erreur peut être causée par un conflit entre modules :

```bash
# Vérifier les modules website installés
docker exec saas-odoo-dev odoo shell -d odoo --no-http <<'EOF'
website_modules = env['ir.module.module'].search([
    ('name', 'like', 'website'),
    ('state', '=', 'installed')
])
for mod in website_modules:
    print(f"{mod.name}: {mod.state}")
EOF
```

### Solution 5 : Patch JavaScript temporaire (Avancé)

Si le problème persiste, vous pouvez ajouter un patch dans la console du navigateur :

```javascript
// Patch temporaire pour l'erreur parentElement.closest
(function() {
    const originalClosest = Element.prototype.closest;
    Element.prototype.closest = function(selector) {
        if (!this || !this.parentElement) {
            return null;
        }
        return originalClosest.call(this, selector);
    };
})();
```

⚠️ **Note :** Ce patch est temporaire et ne devrait être utilisé qu'en développement.

## 🔧 Diagnostic

### Vérifier si c'est lié au mode dev

```bash
# Voir les assets chargés
docker compose -f config/docker-compose.simple.yml logs odoo | grep "website.backend_assets"
```

### Vérifier les erreurs dans la console

1. Ouvrir DevTools (F12)
2. Onglet **Console**
3. Vérifier s'il y a d'autres erreurs avant celle-ci
4. Vérifier l'onglet **Network** pour voir si des assets ne se chargent pas

## 📋 Checklist de Résolution

- [ ] Recharger complètement la page (Solution 1)
- [ ] Vider le cache navigateur
- [ ] Si problème persiste : Désactiver `--dev=all` (Solution 2)
- [ ] Vérifier que le module website est à jour (Solution 3)
- [ ] Vérifier les conflits de modules (Solution 4)

## 💡 Prévention

Pour éviter ce problème :

1. **Utiliser le mode dev avec précaution** - Il peut causer des problèmes avec certains modules
2. **Mettre à jour régulièrement les modules** Odoo
3. **Tester en mode production** (`--dev=all` désactivé) avant de déployer

## 🚀 Recommandation

**Pour l'installation de modules**, il est recommandé de :

1. **Désactiver temporairement `--dev=all`**
2. **Installer les modules**
3. **Réactiver `--dev=all` si nécessaire pour le développement**

Cela évite les problèmes liés aux assets en mode debug.

