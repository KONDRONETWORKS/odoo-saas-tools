SaaS Server Backup S3
=====================

Sauvegarde automatique des bases de données vers AWS S3.

**Description:**
Ce module permet de sauvegarder automatiquement toutes les bases de données client vers Amazon S3. Il est installé sur le serveur SaaS et s'exécute selon une planification configurable.

**Dépendances:**
- saas_server

**Installation requise:**
- `pip install boto` (AWS SDK Python)
- `pip install filechunkio` (Performance boost, optionnel)

**Configuration:**
1. Configurer AWS ID & KEY dans les paramètres
2. Définir le bucket S3 de destination
3. S'assurer que le bucket existe
4. Configurer la fréquence de sauvegarde

**Fonctionnalités:**
- Backup automatique quotidien
- Compression des sauvegardes
- Upload vers S3
- Versioning des sauvegardes (optionnel)
- Rotation automatique

**Structure des backups:**
- Une sauvegarde par base client
- Nom: {db_name}_{timestamp}.sql.gz
- Stockage dans: s3://bucket/{server_name}/backups/

**Avantages:**
- Sécurité cloud AWS
- Scalabilité illimitée
- Durabilité garantie (11×9)
- Redondance automatique

**TODO:**
- Utiliser FileChunkIO et boto pour le traitement parallèle de fichiers volumineux
- Améliorer les performances pour bases > 1 GB

**Relations:**
- Installé sur saas_server
- Complète saas_server_backup_rotate_s3
- Alternative à saas_server_backup_ftp
