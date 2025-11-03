#!/usr/bin/env python3
"""Script pour vérifier les clients existants."""
import xmlrpc.client

URL = 'http://localhost:8069'
DB = 'saas-portal-18.local'
USERNAME = 'admin'
PASSWORD = 'admin'

print("🔌 Connexion à Odoo...")
common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
uid = common.authenticate(DB, USERNAME, PASSWORD, {})

if not uid:
    print("❌ Erreur: Échec de l'authentification")
    exit(1)

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

print("\n🔍 Recherche des clients...")
clients = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.client', 'search',
    [[]]
)

print(f"Nombre de clients trouvés: {len(clients)}")

if clients:
    client_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.client', 'read',
        [clients],
        {'fields': ['name', 'state', 'active', 'partner_id', 'plan_id', 'server_id']}
    )
    print("\nClients trouvés:")
    for c in client_data:
        print(f"  - {c['name']} (ID: {c['id']}, État: {c.get('state', 'N/A')}, Actif: {c.get('active', 'N/A')})")
        if c.get('partner_id'):
            print(f"    Partenaire: {c['partner_id'][1]}")
        if c.get('plan_id'):
            print(f"    Plan: {c['plan_id'][1]}")
else:
    print("❌ Aucun client trouvé dans la base de données")
    
    # Vérifier si le problème vient des permissions
    print("\n🔍 Vérification des permissions...")
    try:
        all_clients = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.client', 'search',
            [[]],
            {'context': {'active_test': False}}
        )
        print(f"Clients (avec active_test=False): {len(all_clients)}")
    except Exception as e:
        print(f"Erreur: {e}")

