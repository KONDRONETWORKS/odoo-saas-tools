{
    'name': 'SaaS Portal Asynchronous database creation',
    'version': '18.0.1.0.0',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'license': 'GPL-3',
    'category': 'SaaS',
    'summary': 'Création asynchrone des bases de données client pour éviter les timeouts',
    'description': """
SaaS Portal Asynchronous Database Creation
===========================================

Module permettant la création asynchrone des bases de données client pour éviter les timeouts lors de la création d'instances.

**Rôle:**
Ce module ajoute une option pour créer les bases de données client de manière asynchrone, ce qui évite les timeouts lors de la création d'instances lourdes.

**Fonctionnalités:**

**Création Asynchrone:**
- Option dans le wizard de création de client
- Création en arrière-plan via actions planifiées
- Notification de l'utilisateur lors de la création
- Suivi du statut de création

**Avantages:**
- Pas de timeout pour les grandes bases de données
- L'utilisateur peut continuer à travailler pendant la création
- Meilleure expérience utilisateur
- Support des instances complexes

**Utilisation:**
1. Lors de la création d'un client, cocher "Async Creation"
2. La création sera lancée en arrière-plan
3. Un email de notification sera envoyé à la fin

**Cas d'usage:**
- Bases de données avec beaucoup de données de démonstration
- Instances avec de nombreux modules à installer
- Bases de données avec des configurations complexes
- Environnements où la création peut prendre plusieurs minutes
""",
    'depends': ['base', 'saas_portal', 'queue_job'],
    'installable': True,
    'application': False,
    'data': ['views/wizard.xml'],
    'sequence': 10,
}
