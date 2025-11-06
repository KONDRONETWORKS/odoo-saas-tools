{
    'name': 'SaaS OAuth2 Provider',
    'version': '18.0.1.0.0',
    'author': 'Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Fournisseur OAuth2 pour l\'authentification sécurisée entre Portal et Server',
    'description': """
OAuth2 Provider
===============

Module fournissant les fonctionnalités OAuth2 nécessaires à l'authentification sécurisée entre le Portal SaaS et les serveurs distants.

**Rôle:**
Ce module implémente le protocole OAuth2 pour sécuriser toutes les communications entre le Portal (serveur central) et les Server (serveurs de bases de données).

**Fonctionnalités principales:**

**Gestion des Applications OAuth:**
- Création et configuration d'applications OAuth2
- Génération automatique de Client ID et Client Secret
- Gestion des tokens d'accès (access tokens)
- Expiration et renouvellement automatique des tokens

**Sécurité:**
- Validation des tokens avant chaque requête
- Vérification des scopes d'autorisation
- Gestion des tokens expirés
- Logs de connexion pour audit

**Intégration:**
- Utilisé par saas_portal pour authentifier les requêtes
- Utilisé par saas_server pour valider les requêtes
- Support des endpoints standards OAuth2

**Workflow d'authentification:**
1. Le Portal demande un token d'accès
2. Le Provider valide les credentials
3. Le Provider génère un token sécurisé
4. Le token est utilisé pour les requêtes suivantes

**Dépendances:**
- oauthlib (bibliothèque Python pour OAuth2)

**Note:** Ce module est un prérequis pour tous les autres modules SaaS.
""",
    'depends': ['web'],
    'external_dependencies': {'python': ['oauthlib']},
    'data': ['security/ir.model.access.csv'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
