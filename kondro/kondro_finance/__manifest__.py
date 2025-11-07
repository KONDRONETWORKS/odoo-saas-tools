# -*- coding: utf-8 -*-
{
    'name': 'KONDRO Finance - Gestion Financière Unifiée',
    'version': '18.0.1.0.0',
    'category': 'KONDRO/Finance',
    'summary': 'Gestion de trésorerie et workflow de paiement unifié',
    'description': """
KONDRO Finance - Gestion Financière Unifiée
===========================================

Module de gestion financière unifié pour KONDRONETWORKS.

**Fonctionnalités principales:**

**Gestion de Trésorerie:**
- Comptes de trésorerie (Banque, Caisse, Djamo)
- Mouvements financiers (Entrées/Sorties)
- Calcul automatique des soldes
- Traçabilité complète des opérations

**Dépenses Unifiées:**
- Dépenses internes avec workflow complet
- Dépenses commerciales liées aux projets
- Workflow de validation hiérarchique unifié
- Planification des décaissements

**Workflow de Paiement:**
- Brouillon → Soumise → Validée → Approuvée → Planifiée → Payée → Clôturée
- Validation par chef de service/projet
- Approbation par direction
- Exécution et enregistrement automatique

**Intégration:**
- Lien avec kondro_core pour les projets
- Génération automatique des mouvements de trésorerie
- Rapports financiers consolidés

**Note:** Ce module remplace kondro_treasury et kondro_internal_expenses.
""",
    'author': 'KONDRONETWORKS',
    'website': 'https://www.kondronetworks.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'account',
        'kondro_company',
        'kondro_core',
    ],
    'data': [
        'security/kondro_finance_security.xml',
        'security/ir.model.access.csv',
        'data/kondro_finance_data.xml',
        'data/kondro_expense_sequence.xml',
        'views/kondro_treasury_account_views.xml',
        'views/kondro_treasury_movement_views.xml',
        'views/kondro_expense_request_views.xml',
        'views/kondro_finance_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 20,
}

