SaaS Server Backup OVH
======================

Stocke les paramètres nécessaires pour pousser automatiquement les sauvegardes bases/filestore vers OVH Object Storage :

- Project ID Public Cloud
- Région et nom du container
- Credentials OVH (Application Key / Secret / Consumer Key)

Les scripts de sauvegarde (cron) peuvent ensuite lire ces valeurs via `ir.config_parameter` et utiliser l'API OVH (`ovh` Python SDK) ou l'API Swift/S3 compatible pour téléverser les dumps.


