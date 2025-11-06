{
    'name': 'SaaS Portal Subscription',
    'version': '18.0.1.0.0',
    'author': 'PlanetaTIC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'info@planetatic.com',
    'website': 'https://www.planetatic.com',
    'summary': 'Gestion complète des abonnements SaaS avec suivi des expirations et historique',
    'description': """
SaaS Portal Subscription
========================

Module permettant la gestion complète des abonnements SaaS avec suivi détaillé des dates d'expiration et historique des modifications.

**Fonctionnalités principales:**

**Gestion des Abonnements:**
- Calcul automatique de la date d'expiration basé sur:
  * Date de création du client SaaS
  * Modifications manuelles de l'expiration
  * Jours de grâce configurés dans le plan
  * Heures d'essai configurées dans le plan

**Historique des Modifications:**
- Journal complet de toutes les modifications d'expiration
- Enregistrement de la raison de chaque modification
- Traçabilité complète des changements
- Vue détaillée de l'historique par client

**Notifications Automatiques:**
- Email envoyé automatiquement au client après chaque modification d'expiration
- Templates d'email personnalisables
- Notifications via base_automation

**Wizard de Modification:**
- Interface simple pour modifier les dates d'expiration
- Affichage de l'expiration actuelle et nouvelle
- Champ obligatoire pour la raison du changement
- Application immédiate des modifications

**Avantages:**
- Traçabilité complète des abonnements
- Gestion transparente des essais et périodes de grâce
- Communication automatique avec les clients
- Conformité et audit facilités
""",
    'depends': ['saas_portal', 'base_automation'],
    'data': ['data/base_automation.xml', 'wizard/subscription_wizard.xml', 'views/saas_portal.xml'],
    'installable': True,
    'application': False,
    'sequence': 10,
}
