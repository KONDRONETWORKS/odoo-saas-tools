#!/usr/bin/env python3
"""
Script pour créer des éléments SaaS de base via l'API XML-RPC :
- 1 serveur SaaS
- 1 plan SaaS
- 1 client de test

Les templates doivent être créés manuellement depuis l'interface Odoo car ils nécessitent des permissions système.

Utilisation:
  python3 saas_portal/scripts/create_saas_data.py
"""

import xmlrpc.client
import sys

# Configuration de connexion
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
print("🚀 Création des éléments SaaS")
print("="*60)

# 1. Créer un serveur SaaS
print("\n1️⃣ Création du serveur SaaS...")
server_vals = {
    'name': 'saas-server-001',
    'request_scheme': 'http',
    'local_request_scheme': 'http',
    'request_port': 8069,
    'local_host': 'localhost',
    'local_port': '8069',  # Port local pour les requêtes serveur-à-serveur
    'verify_ssl': False,
    'active': True,
    'sequence': 1,
}

# Vérifier si le serveur existe déjà
existing_server = models.execute_kw(
    DB, uid, PASSWORD,
    'saas_portal.server', 'search',
    [[('name', '=', server_vals['name'])]]
)

if existing_server:
    print(f"   ⚠️  Serveur '{server_vals['name']}' existe déjà (ID: {existing_server[0]})")
    server_id = existing_server[0]
else:
    server_id = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.server', 'create',
        [server_vals]
    )
    print(f"   ✅ Serveur créé: {server_vals['name']} (ID: {server_id})")

# 2. Informations sur les templates
print("\n2️⃣ Templates de bases de données...")
print("   ℹ️  Les templates doivent être créés manuellement depuis l'interface Odoo:")
print("      - Allez dans SaaS > Bases de données")
print("      - Créez les templates: template-basic, template-standard, template-premium")
print("      - Définissez leur état sur 'Template'")
print("      - Assurez-vous qu'ils sont liés au serveur créé")

# Vérifier s'il existe des templates (peut nécessiter des permissions spéciales)
existing_templates = []
template_data = []
try:
    existing_templates = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.database', 'search',
        [[('state', '=', 'template')]],
        {'limit': 10}
    )
    if existing_templates:
        template_data = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.database', 'read',
            [existing_templates],
            {'fields': ['name', 'state', 'server_id']}
        )
        print(f"\n   ✅ Templates existants trouvés: {len(existing_templates)}")
        for template in template_data:
            print(f"      - {template['name']} (ID: {template['id']}, Serveur: {template['server_id'][1] if template['server_id'] else 'Aucun'})")
except Exception as e:
    print(f"   ⚠️  Impossible de vérifier les templates (permissions requises): {e}")
    print("   💡 Créez les templates manuellement depuis l'interface Odoo")

template_id = existing_templates[0] if existing_templates else False

# 3. Créer un plan SaaS (uniquement si un template existe)
if template_id:
    print("\n3️⃣ Création du plan SaaS...")
    plan_vals = {
        'name': 'Plan Standard',
        'summary': 'Plan SaaS standard avec fonctionnalités de base',
        'template_id': template_id,
        'server_id': server_id,
        'maximum_allowed_dbs_per_partner': 5,
        'maximum_allowed_trial_dbs_per_partner': 2,
        'max_users': '10',
        'total_storage_limit': 1000,
        'demo': False,
        'lang': 'fr_FR',
        'tz': 'Europe/Paris',
        'sequence': 1,
        'expiration': 0,
        'grace_period': 7,
        'block_on_expiration': False,
        'block_on_storage_exceed': False,
        'on_create': 'login',
        'website_description': '<p>Plan SaaS standard avec toutes les fonctionnalités essentielles.</p>',
    }

    existing_plan = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.plan', 'search',
        [[('name', '=', plan_vals['name'])]]
    )

    if existing_plan:
        print(f"   ⚠️  Plan '{plan_vals['name']}' existe déjà (ID: {existing_plan[0]})")
        plan_id = existing_plan[0]
    else:
        plan_id = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.plan', 'create',
            [plan_vals]
        )
        plan_data = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.plan', 'read',
            [[plan_id]],
            {'fields': ['name', 'template_id', 'server_id', 'maximum_allowed_dbs_per_partner', 'maximum_allowed_trial_dbs_per_partner']}
        )
        plan = plan_data[0]
        print(f"   ✅ Plan créé: {plan['name']} (ID: {plan_id})")
        print(f"      - Template: {plan['template_id'][1] if plan['template_id'] else 'Aucun'}")
        print(f"      - Serveur: {plan['server_id'][1] if plan['server_id'] else 'Aucun'}")
        print(f"      - Max DBs/partenaire: {plan['maximum_allowed_dbs_per_partner']}")
        print(f"      - Max DBs essai/partenaire: {plan['maximum_allowed_trial_dbs_per_partner']}")

    # 4. Créer un client de test
    print("\n4️⃣ Création du client de test...")

    # Vérifier si un partenaire de test existe
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
        partner_data = models.execute_kw(
            DB, uid, PASSWORD,
            'res.partner', 'read',
            [[partner_id]],
            {'fields': ['name']}
        )
        print(f"   ✅ Partenaire créé: {partner_data[0]['name']} (ID: {partner_id})")
    else:
        partner_id = partner[0]
        partner_data = models.execute_kw(
            DB, uid, PASSWORD,
            'res.partner', 'read',
            [[partner_id]],
            {'fields': ['name']}
        )
        print(f"   ℹ️  Partenaire existant utilisé: {partner_data[0]['name']} (ID: {partner_id})")

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
        print(f"   ⚠️  Client '{client_vals['name']}' existe déjà (ID: {existing_client[0]})")
        client_id = existing_client[0]
    else:
        client_id = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.client', 'create',
            [client_vals]
        )
        client_data = models.execute_kw(
            DB, uid, PASSWORD,
            'saas_portal.client', 'read',
            [[client_id]],
            {'fields': ['name', 'partner_id', 'plan_id', 'server_id', 'state']}
        )
        client = client_data[0]
        print(f"   ✅ Client créé: {client['name']} (ID: {client_id})")
        print(f"      - Partenaire: {client['partner_id'][1] if client['partner_id'] else 'Aucun'}")
        print(f"      - Plan: {client['plan_id'][1] if client['plan_id'] else 'Aucun'}")
        print(f"      - Serveur: {client['server_id'][1] if client['server_id'] else 'Aucun'}")
        print(f"      - État: {client['state']}")

    # Résumé
    print("\n" + "="*60)
    print("📋 Résumé de la création")
    print("="*60)
    server_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.server', 'read',
        [[server_id]],
        {'fields': ['name']}
    )
    print(f"✅ Serveur SaaS: {server_data[0]['name']} (ID: {server_id})")
    
    if existing_templates:
        print(f"✅ Templates disponibles: {len(existing_templates)}")
        for template in template_data:
            print(f"   - {template['name']} (ID: {template['id']})")
    
    plan_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.plan', 'read',
        [[plan_id]],
        {'fields': ['name']}
    )
    print(f"✅ Plan SaaS: {plan_data[0]['name']} (ID: {plan_id})")
    
    client_data = models.execute_kw(
        DB, uid, PASSWORD,
        'saas_portal.client', 'read',
        [[client_id]],
        {'fields': ['name']}
    )
    print(f"✅ Client: {client_data[0]['name']} (ID: {client_id})")
    
    print("\n💡 Vous pouvez maintenant accéder à ces éléments dans Odoo:")
    print("   - SaaS > Serveurs")
    print("   - SaaS > Plans")
    print("   - SaaS > Clients")
    print("\n✅ Tous les éléments ont été créés avec succès!")
else:
    print("\n⚠️  Plan et client non créés car aucun template n'est disponible.")
    print("   Créez d'abord des templates depuis l'interface Odoo, puis relancez ce script.")
