#!/usr/bin/env python3
"""Script pour créer un client de test directement (sans template requis)."""
import xmlrpc.client
import sys

URL = 'http://localhost:8069'
DB = 'saas-portal-18.local'
USERNAME = 'admin'
PASSWORD = 'admin'

print("🔌 Connexion à Odoo...")
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USERNAME, PASSWORD, {})

if not uid:
    print("❌ Erreur: Échec de l'authentification")
    sys.exit(1)

print(f"✅ Connecté en tant que {USERNAME} (UID: {uid})")

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

print("\n" + "="*60)
print("🚀 Création d'un client de test")
print("="*60)

# 1. Vérifier/Créer un serveur
print("\n1️⃣ Serveur SaaS...")
servers = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.server', 'search',
    [[]]
)

if servers:
    server_id = servers[0]
    server_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.server', 'read',
        [[server_id]],
        {'fields': ['name']}
    )
    print(f"   ✅ Serveur trouvé: {server_data[0]['name']} (ID: {server_id})")
else:
    print("   ⚠️  Aucun serveur trouvé. Créez-en un depuis l'interface Odoo.")
    sys.exit(1)

# 2. Créer ou trouver un plan (sans template requis)
print("\n2️⃣ Plan SaaS...")
plans = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.plan', 'search',
    [[]]
)

if plans:
    plan_id = plans[0]
    plan_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.plan', 'read',
        [[plan_id]],
        {'fields': ['name']}
    )
    print(f"   ✅ Plan trouvé: {plan_data[0]['name']} (ID: {plan_id})")
else:
    print("   ⚠️  Aucun plan trouvé. Création d'un plan simple...")
    plan_vals = {
        'name': 'Plan Test',
        'server_id': server_id,
        'maximum_allowed_dbs_per_partner': 5,
        'maximum_allowed_trial_dbs_per_partner': 2,
        'max_users': '10',
        'demo': False,
    }
    plan_id = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.plan', 'create',
        [plan_vals]
    )
    print(f"   ✅ Plan créé: Plan Test (ID: {plan_id})")

# 3. Créer ou trouver un partenaire
print("\n3️⃣ Partenaire...")
partner = models.execute_kw(
    DB, uid, PASSWORD,
    'res.partner', 'search',
    [[('email', '=', 'client-test@example.com')]],
    {'limit': 1}
)

if not partner:
    partner_vals = {
        'name': 'Client Test SaaS',
        'email': 'client-test@example.com',
        'is_company': True,
    }
    partner_id = models.execute_kw(
        DB, uid, PASSWORD,
        'res.partner', 'create',
        [partner_vals]
    )
    print(f"   ✅ Partenaire créé: Client Test SaaS (ID: {partner_id})")
else:
    partner_id = partner[0]
    partner_data = models.execute_kw(
        DB, uid, PASSWORD,
        'res.partner', 'read',
        [[partner_id]],
        {'fields': ['name']}
    )
    print(f"   ✅ Partenaire trouvé: {partner_data[0]['name']} (ID: {partner_id})")

# 4. Créer le client
print("\n4️⃣ Client de test...")
client_vals = {
    'name': 'client-test-001',
    'partner_id': partner_id,
    'plan_id': plan_id,
    'server_id': server_id,
    'state': 'open',
}

existing_client = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.client', 'search',
    [[('name', '=', client_vals['name'])]]
)

if existing_client:
    client_id = existing_client[0]
    print(f"   ⚠️  Client '{client_vals['name']}' existe déjà (ID: {client_id})")
else:
    client_id = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.client', 'create',
        [client_vals]
    )
    print(f"   ✅ Client créé: {client_vals['name']} (ID: {client_id})")

# Afficher les détails du client
client_data = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.client', 'read',
    [[client_id]],
    {'fields': ['name', 'partner_id', 'plan_id', 'server_id', 'state']}
)
client = client_data[0]

print("\n" + "="*60)
print("📋 Détails du client créé")
print("="*60)
print(f"Nom: {client['name']}")
print(f"Partenaire: {client['partner_id'][1] if client['partner_id'] else 'Aucun'}")
print(f"Plan: {client['plan_id'][1] if client['plan_id'] else 'Aucun'}")
print(f"Serveur: {client['server_id'][1] if client['server_id'] else 'Aucun'}")
print(f"État: {client['state']}")

print("\n✅ Client créé avec succès!")
print("\n💡 Accédez à Odoo > SaaS > Clients pour voir le client créé")
print("   URL: http://localhost:8069")

