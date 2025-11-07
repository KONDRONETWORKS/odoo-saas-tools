SaaS Sysadmin OVH Route53
==========================

Module de gestion automatique des DNS OVH pour les instances SaaS.

**Configuration :**
1. Installez le module saas_sysadmin_ovh et configurez les credentials OVH
2. Créez une zone DNS dans OVH (via l'interface OVH ou ce module)
3. Associez la zone au serveur SaaS dans saas_portal.server

**Fonctionnement :**
- Lors de la création d'une instance client, un enregistrement DNS A est créé automatiquement
- Lors de la mise à jour du serveur (IP), le DNS est mis à jour
- Lors de la suppression d'une instance, le DNS est supprimé

**Types d'enregistrements supportés :**
- A (IPv4)
- CNAME
- TXT
- MX

