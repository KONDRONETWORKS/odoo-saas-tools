#!/usr/bin/env python3
"""Script pour créer un client directement via Odoo shell (bypass permissions)."""
import sys
import os

# Instructions pour créer le client depuis Odoo shell
print("""
🔧 CRÉATION DU CLIENT DIRECTEMENT DANS ODOO

Le problème semble venir des permissions sur saas_portal.database.
Créons le client directement depuis Odoo shell pour contourner ce problème.

ÉTAPES:

1. Exécutez cette commande dans le conteneur Docker:
""")

print('   docker compose -f config/docker-compose.windows.yml exec odoo odoo-bin shell -d saas-portal-18.local')

print("""
2. Dans le shell Python qui s'ouvre, exécutez:

   # Créer le client directement
   server = env['saas_portal.server'].search([], limit=1)
   plan = env['saas_portal.plan'].search([], limit=1)
   partner = env['res.partner'].search([('email', '=', 'client-test@example.com')], limit=1)
   
   if not partner:
       partner = env['res.partner'].create({
           'name': 'Client Test SaaS',
           'email': 'client-test@example.com',
           'is_company': True,
       })
   
   client = env['saas_portal.client'].create({
       'name': 'client-test-001',
       'partner_id': partner.id,
       'plan_id': plan.id if plan else False,
       'server_id': server.id,
       'state': 'open',
   })
   
   print(f"Client créé: {client.name} (ID: {client.id})")
   env.cr.commit()

3. Rafraîchissez l'interface Odoo

ALTERNATIVE: Créer depuis l'interface Odoo directement
""")

print("""
📋 OU Créez le client depuis l'interface Odoo:

1. Allez dans SaaS > Clients
2. Cliquez sur "Créer" (ou le bouton "+")
3. Remplissez:
   - Nom: client-test-001
   - Plan: Plan Test (ou un autre plan)
   - Partenaire: Créez ou sélectionnez un partenaire
   - Serveur: saas-server-001
   - État: open
4. Enregistrez

Si le bouton "Créer" n'est pas visible, vérifiez les permissions.
""")

