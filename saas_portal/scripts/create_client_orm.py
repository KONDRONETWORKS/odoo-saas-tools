#!/usr/bin/env python3
"""Créer un client directement via Odoo ORM (bypass permissions)."""
import odoo
from odoo import api, SUPERUSER_ID

# Configuration
db_name = 'saas-portal-18.local'
config_file = '/etc/odoo/odoo.conf'

# Initialiser Odoo
odoo.tools.config.parse_config(['-c', config_file])
registry = odoo.registry(db_name)
env = api.Environment(registry.cursor(), SUPERUSER_ID, {})

print("🔧 Création du client via Odoo ORM...")

# Récupérer les données nécessaires
server = env['saas_portal.server'].search([], limit=1)
plan = env['saas_portal.plan'].search([], limit=1)
partner = env['res.partner'].search([('email', '=', 'client-test@example.com')], limit=1)

if not partner:
    partner = env['res.partner'].create({
        'name': 'Client Test SaaS',
        'email': 'client-test@example.com',
        'is_company': True,
    })
    print(f"✅ Partenaire créé: {partner.name}")

# Supprimer l'ancien client s'il existe
existing = env['saas_portal.client'].search([('name', '=', 'client-test-001')])
if existing:
    existing.unlink()
    print(f"🗑️  Ancien client supprimé")
    env.cr.commit()

# Créer le nouveau client avec sudo() pour bypasser les permissions
client = env['saas_portal.client'].sudo().create({
    'name': 'client-test-001',
    'partner_id': partner.id,
    'plan_id': plan.id if plan else False,
    'server_id': server.id if server else False,
    'state': 'open',
})

env.cr.commit()

print(f"✅ Client créé: {client.name} (ID: {client.id})")
print(f"   Partenaire: {client.partner_id.name}")
print(f"   Plan: {client.plan_id.name if client.plan_id else 'Aucun'}")
print(f"   Serveur: {client.server_id.name if client.server_id else 'Aucun'}")
print(f"   État: {client.state}")

env.cr.close()

