# 🔄 Instructions : Mise à jour des vues de configuration

## ✅ Modifications appliquées

Les vues suivantes ont été mises à jour pour améliorer l'affichage :
- ✅ `saas_server_backup_rotate/views/res_config.xml` - Rotate Backup Settings
- ✅ `saas_server_backup_s3/views/res_config.xml` - AWS S3 Backup Settings  
- ✅ `saas_server/views/res_config_settings_views.xml` - SaaS Server Configuration

## 🔄 Étapes pour voir les changements

### 1. Redémarrer Odoo (si nécessaire)

```bash
# Arrêter Odoo si il tourne
# Puis redémarrer
./start_local.sh
# ou
./start_complete.sh
```

### 2. Mettre à jour les modules dans Odoo

**Option A : Via l'interface Odoo (Recommandé)**

1. Activer le **Mode Développeur** :
   - Aller dans **Paramètres > Activer le mode développeur**
   - Ou : `?debug=1` dans l'URL

2. Mettre à jour les modules :
   - Aller dans **Paramètres > Applications**
   - Cliquer sur **"Mettre à jour la liste des applications"**
   - Rechercher et mettre à jour chaque module :
     - `saas_server_backup_rotate`
     - `saas_server_backup_s3`
     - `saas_server`

**Option B : Via la ligne de commande**

```bash
# Avec odoo-bin
./odoo-server -u saas_server_backup_rotate,saas_server_backup_s3,saas_server -d votre_base_de_donnees

# Ou via l'interface Odoo en mode shell
```

### 3. Vider le cache du navigateur

**Chrome / Edge :**
- Appuyer sur `Ctrl+Shift+Delete` (Windows/Linux) ou `Cmd+Shift+Delete` (Mac)
- Sélectionner "Images et fichiers en cache"
- Cliquer sur "Effacer les données"

**Firefox :**
- Appuyer sur `Ctrl+Shift+Delete` (Windows/Linux) ou `Cmd+Shift+Delete` (Mac)
- Sélectionner "Cache"
- Cliquer sur "Effacer maintenant"

**Safari :**
- `Cmd+Option+E` pour vider le cache
- Ou : Menu Safari > Préférences > Avancé > Cocher "Afficher le menu Développement"
- Puis : Menu Développement > Vider les caches

### 4. Recharger la page

**Important :** Faire un rechargement forcé pour ignorer le cache :
- `Ctrl+F5` (Windows/Linux)
- `Cmd+Shift+R` (Mac)
- Ou : Ouvrir les outils développeur (F12) > Clic droit sur le bouton actualiser > "Vider le cache et actualiser"

### 5. Vérifier les changements

Aller dans **Paramètres > Configuration SaaS Server** et vérifier que :
- Les labels sont bien visibles à gauche
- Les descriptions sont plus détaillées
- Les champs sont mieux organisés
- La structure correspond à la vue SFTP Backup Settings

## 🐛 Si les changements n'apparaissent toujours pas

### Vérifier les erreurs dans les logs Odoo

```bash
tail -f odoo.log | grep -i error
```

### Vérifier que les fichiers sont bien chargés

Dans Odoo (mode développeur) :
- **Paramètres > Technique > Vues**
- Rechercher : `res.config.settings.view.form.inherit.backup_rotate`
- Vérifier que le contenu correspond à nos modifications

### Forcer la mise à jour des assets

Dans l'URL, ajouter : `?debug=assets`

### Recompiler les vues

Dans Odoo (mode développeur) :
- **Paramètres > Technique > Base de données > Recompiler les vues**

## ✅ Vérification finale

La nouvelle structure doit afficher :
- ✅ Labels à gauche avec attribut `string` explicite
- ✅ Descriptions détaillées avec `mb-2`
- ✅ Champs organisés dans `content-group` avec `row mt16`
- ✅ Styles uniformisés (`width: 100%; max-width: none;`)

## 📝 Notes

- Les changements de vues nécessitent toujours une mise à jour du module
- Le cache du navigateur peut cacher les anciennes versions
- Le mode développeur est nécessaire pour mettre à jour les modules
- Les vues sont mises en cache par Odoo, d'où l'importance de mettre à jour les modules

---

**Date :** 1er Novembre 2025

