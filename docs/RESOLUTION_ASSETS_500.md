# Résolution des Erreurs 500 sur les Assets Odoo

## 🔍 Problème

Erreurs 500 lors du chargement des assets :
- `web.assets_frontend.min.css`
- `web.assets_frontend_minimal.min.js`
- `fontawesome-webfont.woff2`
- `favicon.ico`

## ✅ Solutions

### Solution 1 : Vider le cache des assets (Recommandée)

```bash
# Vider le cache des assets dans Odoo
docker exec saas-odoo-dev odoo shell -d odoo --no-http --stop-after-init <<'EOF'
env['ir.attachment'].search([('name', 'like', 'web.assets')]).unlink()
env['ir.qweb'].clear_caches()
env.cr.commit()
print("✅ Cache vidé")
EOF

# Redémarrer Odoo
docker compose -f config/docker-compose.simple.yml restart odoo
```

### Solution 2 : Vider le cache navigateur

**Très important !** Après avoir vidé le cache Odoo :

1. **Chrome/Edge** : `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)
2. **Firefox** : `Ctrl+F5` ou `Cmd+Shift+R`
3. **Safari** : `Cmd+Option+R`

Ou ouvrir en navigation privée pour tester.

### Solution 3 : Vérifier le data_dir

```bash
# Vérifier la configuration
docker exec saas-odoo-dev cat /etc/odoo/odoo.conf | grep data_dir

# Devrait afficher : data_dir = /var/lib/odoo

# Vérifier que le répertoire existe
docker exec saas-odoo-dev ls -la /var/lib/odoo/filestore/
```

### Solution 4 : Forcer la régénération complète

```bash
# Arrêter Odoo
docker compose -f config/docker-compose.simple.yml stop odoo

# Supprimer les assets corrompus
docker exec saas-odoo-dev rm -rf /var/lib/odoo/filestore/odoo/web.assets*

# Vider le cache dans la base
docker exec saas-odoo-dev odoo shell -d odoo --no-http --stop-after-init <<'EOF'
env['ir.attachment'].search([('name', 'like', 'web.assets')]).unlink()
env['ir.qweb'].clear_caches()
env.cr.commit()
EOF

# Redémarrer
docker compose -f config/docker-compose.simple.yml up -d odoo
```

### Solution 5 : Réinitialiser complètement (Dernier recours)

```bash
# ⚠️ ATTENTION : Cela supprimera tous les assets et fichiers uploadés

# Arrêter les services
docker compose -f config/docker-compose.simple.yml down

# Supprimer le filestore (optionnel, seulement si nécessaire)
# docker volume rm saas_odoo_filestore  # Si vous utilisez un volume nommé

# Redémarrer
docker compose -f config/docker-compose.simple.yml up -d

# Attendre que Odoo démarre complètement
sleep 30

# Les assets seront régénérés automatiquement au premier accès
```

## 🔍 Diagnostic

### Vérifier les logs

```bash
# Voir les erreurs récentes
docker compose -f config/docker-compose.simple.yml logs odoo --tail 100 | grep -i error

# Voir tous les logs
docker compose -f config/docker-compose.simple.yml logs odoo -f
```

### Vérifier les assets dans la base

```bash
docker exec saas-odoo-dev odoo shell -d odoo --no-http <<'EOF'
assets = env['ir.attachment'].search([
    ('name', 'like', 'web.assets'),
    ('store_fname', '!=', False)
], limit=5)
for asset in assets:
    print(f"{asset.name}: {asset.store_fname}")
EOF
```

### Vérifier les fichiers physiques

```bash
# Chercher les fichiers assets
docker exec saas-odoo-dev find /var/lib/odoo/filestore -name "*web.assets*" -type f

# Vérifier les permissions
docker exec saas-odoo-dev ls -la /var/lib/odoo/filestore/odoo/ 2>/dev/null | head -10
```

## 📋 Checklist de Résolution

- [ ] Vider le cache Odoo (Solution 1)
- [ ] Vider le cache navigateur (Solution 2)
- [ ] Vérifier que `data_dir` est correct
- [ ] Vérifier les logs pour erreurs spécifiques
- [ ] Si problème persiste : Solution 4 (régénération complète)
- [ ] En dernier recours : Solution 5 (réinitialisation)

## 💡 Prévention

Pour éviter ce problème à l'avenir :

1. **Ne pas modifier manuellement les fichiers assets**
2. **Utiliser `--dev=all` en développement** pour régénération automatique
3. **Vider le cache navigateur régulièrement** lors du développement
4. **Vérifier les permissions** du répertoire filestore

## 🚀 Mode Développement (Recommandé)

Pour éviter les problèmes d'assets en développement, activez le mode dev :

```yaml
# Dans docker-compose.simple.yml, modifier la commande :
command: >
  odoo
  --config=/etc/odoo/odoo.conf
  --dev=all
  # ... autres options
```

Cela régénère automatiquement les assets à chaque modification.
