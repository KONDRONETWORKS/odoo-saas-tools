SaaS Portal
===========

Module principal de contrôle pour le système SaaS.

**Description:**
Ce module gère le portail central de contrôle SaaS. Il permet de créer et gérer les plans d'abonnement, les clients, et les serveurs SaaS.

**Dépendances:**
- base ⭐ (CRITIQUE)
- oauth_provider
- website
- auth_signup
- saas_base

**Tables principales:**
- saas_portal.plan : Plans d'abonnement (nom, prix, template, essai)
- saas_portal.client : Clients SaaS (plan, serveur, expiration)
- saas_portal.server : Serveurs SaaS (hostname, OAuth, limite)

**Fichiers principaux:**
- models/saas_portal.py : Plans, Clients, Servers
- models/res_users.py : Extension utilisateurs
- controllers/main.py : Routes web pour inscription/création
- wizard/config_wizard.py : Assistants de création clients

**Relations:**
- Commande des serveurs SaaS via OAuth2
- Gère les plans d'abonnement
- Interface d'administration centralisée
- Authentification et autorisation

**Utilisé par:**
- saas_portal_start (page d'inscription)
- saas_portal_client_web (espace client)
- saas_portal_signup (processus d'inscription)
- Tous les modules Portal

**Workflow:**
1. Administration définit plans et serveurs
2. Client s'inscrit via saas_portal_start
3. Module crée compte et instance via OAuth2
4. Client accède à son instance isolée
