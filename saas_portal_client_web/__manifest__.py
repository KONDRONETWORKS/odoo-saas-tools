{
    'name': 'SaaS Portal Client Web',
    'version': '18.0.1.1.1',
    'author': 'IT-Projects LLC, Cheick Oumar Tidiane Traore',
    'license': 'LGPL-3',
    'category': 'SaaS',
    'support': 'apps@itexperts4africa.com',
    'website': 'https://www.itexperts4africa.com',
    'summary': 'Interface web client pour gestion des instances SaaS depuis le portail',
    'description': """
SaaS Portal Client Web
=======================

Module ajoutant une interface portail web permettant aux clients de visualiser et gérer leurs instances SaaS depuis le site web du Portal.

**Fonctionnalités principales:**

**Interface Portail Client:**
- Accès via "/my/instances" pour les utilisateurs portail
- Liste des instances client accessibles
- Informations détaillées par instance (domaine, plan, état)
- Actions rapides sur les instances

**Sécurité:**
- Accès restreint aux utilisateurs du groupe Portal
- Règles de sécurité pour isoler les données par client
- Permissions en lecture seule pour les clients
- Validation des partenaires associés

**Interface Web:**
- Templates QWeb pour affichage des instances
- Design responsive et moderne
- Intégration avec le module Portal standard Odoo
- Compatible avec les thèmes Website

**Workflow:**
1. Client se connecte au portail web
2. Accède à la section "Mes Instances"
3. Visualise toutes ses instances SaaS
4. Consulte les détails (domaine, plan, expiration, etc.)

**Intégration:**
- Utilise le module Portal standard d'Odoo
- Nécessite saas_portal pour les données
- Nécessite Website pour l'affichage web

**Permissions:**
- Groupe Portal : Accès en lecture à leurs propres instances
- Règles de domaine : Filtrage automatique par partner_id
- Sécurité : Les clients ne voient que leurs propres instances
""",
    'depends': ['portal', 'saas_portal', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/website_instance_templates.xml',
        'views/website_instance_templates_async.xml',
    ],
    'installable': True,
    'application': False,
    'sequence': 10,
}
