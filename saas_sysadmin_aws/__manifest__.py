{
    'name': 'Saas Sysadmin AWS',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'category': 'SaaS',
    'summary': 'Configuration AWS Route53 pour gestion automatique des DNS des instances client',
    'description': """
Saas Sysadmin AWS
=================

Module permettant la gestion automatique des DNS via AWS Route53 lors de la création d'instances client.

**Fonctionnalités principales:**

**Gestion DNS Route53:**
- Création automatique des enregistrements DNS pour les nouvelles instances
- Configuration des sous-domaines pour chaque client
- Mise à jour automatique lors des changements de domaine
- Support de plusieurs zones DNS

**Configuration AWS:**
- Configuration des identifiants AWS (Access Key ID et Secret Key)
- Sélection de la zone Route53 à utiliser
- Validation des credentials avant utilisation

**Automatisation:**
- Création DNS lors de la création d'une instance client
- Suppression DNS lors de la suppression d'une instance
- Mise à jour automatique des enregistrements

**Intégration:**
- Fonctionne avec saas_server pour les créations
- Compatible avec saas_sysadmin_aws_route53 pour fonctionnalités avancées
- Nécessite des credentials AWS avec permissions Route53

**Sécurité:**
- Credentials AWS stockés de manière sécurisée
- Support IAM pour permissions granulaires
- Connexions HTTPS vers AWS

**Utilisation:**
1. Configurer les credentials AWS dans Paramètres > SaaS Server
2. Configurer la zone Route53 à utiliser
3. Les DNS seront créés automatiquement lors de la création d'instances
""",
    'depends': ['base'],
    'data': ['views/res_config.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
