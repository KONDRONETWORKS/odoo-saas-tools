SaaS Portal Portal
===================

Espace client pour la gestion des instances SaaS.

**Description:**
Ce module fournit l'interface client pour que les utilisateurs puissent gérer leurs instances SaaS. Il ajoute une page dans l'espace portal pour lister et configurer les instances du client.

**Dépendances:**
- portal ⭐ (CRITIQUE)
- saas_portal ⭐ (CRITIQUE)
- website ⭐ (CRITIQUE - AJOUTÉ POUR ODOO 18)

**Fichiers principaux:**
- views/website_instance_templates.xml : Templates affichage instances
- controllers/main.py : Routes pour interface client
- static/src/js/main.js : JavaScript personnalisé pour gestion instances

**Fonctionnalités:**
- Liste toutes les instances du client connecté
- Affichage des informations de chaque instance (plan, expiration)
- Gestion des domaines personnalisés (via change_domain template)
- Interface responsive dans le portal

**Routes:**
- /my/instances : Liste des instances du client
- /my/domain/<instance_id> : Configuration du domaine

**Templates:**
- portal_instances : Page principale liste
- portal_my_instances : Affichage détaillé des instances
- change_domain : Configuration domaine personnalisé

**Relations:**
- Étend saas_portal pour ajouter la vue client
- Utilise portal pour l'espace client standard
- Nécessite website pour les assets frontend

**Note importante:**
Ce module hérite de website.assets_frontend, nécessitant la dépendance 'website' dans le manifest (ajouté en Odoo 18).
