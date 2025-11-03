#!/usr/bin/env python3
"""Script pour vérifier les templates de bases de données existants."""
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

print(f"✅ Connecté en tant que {USERNAME} (UID: {uid})\n")

models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')

# Vérifier les templates
try:
    templates = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.database', 'search',
        [[('state', '=', 'template')]],
        {'limit': 100}
    )
    
    if templates:
        print(f"✅ {len(templates)} template(s) trouvé(s):\n")
        template_data = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.database', 'read',
            [templates],
            {'fields': ['name', 'state', 'server_id', 'host']}
        )
        
        for template in template_data:
            print(f"   📦 {template['name']}")
            print(f"      - ID: {template['id']}")
            print(f"      - État: {template['state']}")
            if template.get('server_id'):
                print(f"      - Serveur: {template['server_id'][1]} (ID: {template['server_id'][0]})")
            else:
                print(f"      - Serveur: Aucun")
            if template.get('host'):
                print(f"      - Host: {template['host']}")
            print()
    else:
        print("⚠️  Aucun template trouvé avec l'état 'Template'")
        print("\n💡 Pour créer des templates:")
        print("   1. Accédez à http://localhost:8069")
        print("   2. Allez dans SaaS > Bases de données")
        print("   3. Créez des templates avec l'état 'Template'")
        
except Exception as e:
    error_msg = str(e)
    if 'autorisé' in error_msg or 'permission' in error_msg.lower():
        print("⚠️  Permissions insuffisantes pour vérifier les templates")
        print("💡 Les templates doivent être vérifiés depuis l'interface Odoo")
    else:
        print(f"❌ Erreur: {e}")

# Vérifier aussi tous les enregistrements de saas_portal.database
try:
    all_databases = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.database', 'search',
        [[]],
        {'limit': 100}
    )
    
    if all_databases:
        print(f"\n📊 Total de bases de données: {len(all_databases)}")
        db_data = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.database', 'read',
            [all_databases],
            {'fields': ['name', 'state']}
        )
        
        states = {}
        for db in db_data:
            state = db['state']
            states[state] = states.get(state, 0) + 1
        
        print("   Répartition par état:")
        for state, count in states.items():
            print(f"      - {state}: {count}")
            
except Exception as e:
    print(f"⚠️  Impossible de vérifier toutes les bases de données: {e}")

