SaaS Portal Start
=================

Page de démarrage et d'inscription pour le portail SaaS.

**Description:**
Ce module crée la page d'accueil et d'inscription du portail SaaS, similaire à https://www.odoo.com/page/start. Il permet aux nouveaux clients de s'inscrire et de choisir un plan.

**Dépendances:**
- portal
- saas_portal
- website

**Fichiers principaux:**
- controllers/main.py : Page d'inscription
- views/website_templates.xml : Templates de la page
- data/website_data.xml : Données de configuration

**Fonctionnalités:**
- Page d'accueil personnalisable
- Affichage des plans disponibles
- Formulaire d'inscription
- Sélection de plan

**Routes:**
- /page/start : Page d'accueil SaaS
- /page/signup : Page d'inscription

**Relations:**
- Utilisé pour l'inscription des nouveaux clients
- Appelle saas_portal_signup pour le traitement
- Connecté avec saas_portal pour les plans
