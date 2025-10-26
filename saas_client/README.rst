SaaS Client
===========

Module installé dans chaque instance client pour limitations et sécurité.

**Description:**
Ce module est installé dans chaque instance Odoo cliente. Il gère les limitations d'utilisateurs, l'authentification OAuth, et les restrictions de fonctionnalités.

**Dépendances:**
- base ⭐ (CRITIQUE)
- auth_oauth
- auth_oauth_ip
- auth_oauth_check_client_id
- mail
- web_settings_dashboard
- access_limit_records_number

**Fichiers principaux:**
- models/res_user.py : Limitation nombre d'utilisateurs
- models/saas_client.py : Configuration et limites client
- controllers/main.py : Routes OAuth et authentification

**Fonctionnalités principales:**
- Limite le nombre d'utilisateurs par instance
- Limite le nombre d'enregistrements (optionnel)
- Authentification OAuth sécurisée
- Vérification de l'ID client OAuth
- Dashboard avec statistiques

**Configuration:**
- saas_client.max_users : Nombre max d'utilisateurs autorisés
- saas_client.max_records : Nombre max d'enregistrements (par modèle)

**Relations:**
- Installé dans CHAQUE instance client
- Communique avec Server via OAuth
- Isolé des autres instances
- Même code Odoo, données séparées

**Sécurité:**
- Authentification OAuth2 obligatoire
- Validation stricte client_id
- Contrôle par adresse IP optionnel
- Isolation complète des données

**Cas d'usage:**
- Limitation pour plans basiques (ex: max 5 users)
- Contrôle d'usage pour plans premium
- Multi-tenant sécurisé
- Reporting d'utilisation
