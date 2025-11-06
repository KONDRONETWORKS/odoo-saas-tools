{
    'name': 'SaaS Local IP for OAuth requests',
    'summary': 'Permet la validation des tokens OAuth via requêtes sur le réseau local',
    'category': 'SaaS',
    'images': [],
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'license': 'LGPL-3',
    'description': """
Local IP for OAuth Requests
===========================

Module permettant la validation des tokens OAuth2 via des requêtes sur le réseau local entre le Portal et les serveurs.

**Rôle:**
Ce module étend les fonctionnalités OAuth pour permettre la validation des tokens d'accès via des requêtes HTTP sur le réseau local, essentiel pour la communication Portal-Server dans un environnement SaaS.

**Fonctionnalités:**
- Validation des access tokens via requêtes réseau local
- Support des connexions inter-serveurs sécurisées
- Configuration de l'hôte et port local pour les requêtes
- Gestion des schémas HTTP/HTTPS

**Cas d'usage:**
- Communication Portal → Server sur réseau privé
- Validation des tokens sans exposition publique
- Sécurisation des requêtes internes

**Sécurité:**
- Validation uniquement sur réseau local configuré
- Support SSL/TLS pour connexions sécurisées
- Pas d'exposition publique des endpoints

**Utilisé par:**
- saas_portal : Pour valider les tokens auprès des serveurs
- saas_server : Pour accepter les validations de tokens
""",
    'depends': ['auth_oauth'],
    'external_dependencies': {'python': [], 'bin': []},
    'data': ['views.xml'],
    'qweb': [],
    'demo': [],
    'post_load': None,
    'pre_init_hook': None,
    'post_init_hook': None,
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 10,
}
