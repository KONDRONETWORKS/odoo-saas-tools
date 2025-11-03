#!/usr/bin/env python3
"""Script pour corriger la configuration du serveur SaaS."""
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

print("\n🔧 Correction de la configuration du serveur...")
servers = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.server', 'search',
    [[]]
)

if not servers:
    print("⚠️  Aucun serveur trouvé")
    exit(1)

for server_id in servers:
    server_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.server', 'read',
        [[server_id]],
        {'fields': ['name', 'local_host', 'local_port', 'request_port', 'local_request_scheme']}
    )
    server = server_data[0]
    
    print(f"\n📋 Serveur: {server['name']} (ID: {server_id})")
    print(f"   Avant:")
    print(f"      Local Host: {server.get('local_host', 'Non défini')}")
    print(f"      Local Port: {server.get('local_port', 'Non défini')}")
    print(f"      Request Port: {server.get('request_port', 'Non défini')}")
    
    # Corriger la configuration
    update_vals = {
        'local_host': 'localhost',
        'local_port': '8069',  # Port XML-RPC, pas longpolling
        'request_port': 8069,
        'local_request_scheme': 'http',
        'request_scheme': 'http',
    }
    
    models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.server', 'write',
        [[server_id], update_vals]
    )
    
    # Vérifier après mise à jour
    updated_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.server', 'read',
        [[server_id]],
        {'fields': ['name', 'local_host', 'local_port', 'request_port', 'local_request_scheme']}
    )
    updated = updated_data[0]
    
    print(f"   Après:")
    print(f"      Local Host: {updated.get('local_host', 'Non défini')}")
    print(f"      Local Port: {updated.get('local_port', 'Non défini')}")
    print(f"      Request Port: {updated.get('request_port', 'Non défini')}")
    print(f"   ✅ Configuration corrigée!")

print("\n✅ Configuration des serveurs mise à jour!")

