# Comment voir les modules OVH dans Odoo Apps Store

## ✅ Vérification que les modules sont montés

Les modules sont maintenant correctement montés dans le conteneur :
- ✅ `saas_sysadmin_ovh`
- ✅ `saas_sysadmin_ovh_route53`
- ✅ `saas_server_backup_ovh`

## 🔄 Mise à jour de la liste des modules

Après avoir ajouté de nouveaux modules, vous devez mettre à jour la liste dans Odoo :

### Méthode 1 : Via l'interface Odoo (Recommandée)

1. Connectez-vous à Odoo : http://localhost:8069
2. Allez dans **Apps**
3. Cliquez sur **"Mettre à jour la liste des applications"** (en haut à droite)
4. Attendez que la mise à jour se termine
5. Recherchez les modules avec "OVH" dans le filtre

### Méthode 2 : Via la ligne de commande

```bash
# Mettre à jour la liste des modules
docker exec saas-odoo-dev odoo shell -d odoo --no-http --stop-after-init <<'EOF'
env['ir.module.module'].update_list()
print("✅ Liste des modules mise à jour")
EOF

# Redémarrer Odoo
docker compose -f config/docker-compose.simple.yml restart odoo
```

### Méthode 3 : Via le mode développeur

1. Activez le mode développeur dans Odoo
2. Allez dans **Apps**
3. Cliquez sur **"Mettre à jour la liste des applications"**
4. Les modules apparaîtront immédiatement

## 🔍 Rechercher les modules

Dans l'Apps Store, recherchez :
- **"OVH"** pour trouver tous les modules OVH
- **"SaaS Sysadmin OVH"** pour le module de configuration
- **"SaaS Sysadmin OVH Route53"** pour le module DNS
- **"SaaS Server Backup OVH"** pour le module de sauvegarde

## ⚠️ Si les modules n'apparaissent toujours pas

1. **Vérifier que les modules sont montés** :
   ```bash
   docker exec saas-odoo-dev ls -la /mnt/extra-addons/ | grep ovh
   ```

2. **Vérifier les logs pour erreurs** :
   ```bash
   docker compose -f config/docker-compose.simple.yml logs odoo | grep -i error
   ```

3. **Vérifier le manifest** :
   ```bash
   docker exec saas-odoo-dev cat /mnt/extra-addons/saas_sysadmin_ovh/__manifest__.py
   ```

4. **Forcer la mise à jour** :
   ```bash
   docker exec saas-odoo-dev odoo shell -d odoo --no-http <<'EOF'
   # Supprimer les modules de la base
   env['ir.module.module'].search([('name', 'in', ['saas_sysadmin_ovh', 'saas_sysadmin_ovh_route53', 'saas_server_backup_ovh'])]).unlink()
   # Mettre à jour la liste
   env['ir.module.module'].update_list()
   EOF
   ```

5. **Redémarrer complètement** :
   ```bash
   docker compose -f config/docker-compose.simple.yml down
   docker compose -f config/docker-compose.simple.yml up -d
   ```

## 📋 Modules à installer (dans l'ordre)

1. **SaaS Sysadmin OVH** (prérequis)
2. **SaaS Server Backup OVH** (optionnel, pour sauvegardes)
3. **SaaS Sysadmin OVH Route53** (nécessite saas_sysadmin_ovh)

