SaaS Server
===========

Module serveur technique pour la gestion des bases de données clients.

**Description:**
Ce module gère la création, modification et suppression des bases de données clients. Il communique avec le Portal via OAuth2 et crée les instances PostgreSQL automatiquement.

**Dépendances:**
- base ⭐ (CRITIQUE)
- auth_oauth
- auth_oauth_ip
- saas_base
- website

**Tables principales:**
- saas_server.client : Instances client (nom, DB, host, expiration)
- saas_server.repository : Dépôts de modules disponibles

**Fichiers principaux:**
- models/saas_server.py : Gestion bases de données clients
- controllers/main.py : Endpoints RPC (/new_database)

**Endpoints RPC:**
- POST /saas_server/new_database : Crée nouvelle base
- POST /saas_server/edit_database : Modifie base existante
- POST /saas_server/delete_database : Supprime base

**Sécurité:**
- Validation OAuth2 avant toute création
- Isolation complète des données clients
- Chaque base PostgreSQL est indépendante

**Relations:**
- Reçoit requêtes du Portal via XML-RPC + OAuth2
- Crée et initialise bases PostgreSQL
- Installe modules sur les instances clients
- Gère la configuration automatique

**Workflow de création:**
1. Portal envoie requête avec token OAuth2
2. Server valide le token
3. Server crée base PostgreSQL
4. Server initialise instance Odoo
5. Server installe modules demandés
6. Server retourne credentials au Portal

**Installé sur:**
- Serveurs dédiés (VPS, EC2)
- Chaque Server peut gérer des milliers d'instances
- Multi-servers possible pour scaling 
