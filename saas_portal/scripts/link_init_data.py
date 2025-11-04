#!/usr/bin/env python3
"""
Script pour lier les templates et plans d'initialisation au serveur par défaut.
Utile après une mise à jour du module.
"""

import xmlrpc.client
import ssl
import sys

# Configuration
HOST = 'localhost'
PORT = 8069
DB = 'saas-portal-18.local'
USER = 'admin'
PASSWORD = 'admin'

# Bypass SSL verification for local development
_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

def db_connect(db_name):
    """Connecter à Odoo via XML-RPC."""
    try:
        common = xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}/xmlrpc/2/common')
        uid = common.authenticate(db_name, USER, PASSWORD, {})
        if not uid:
            raise Exception("Authentication failed for Odoo XML-RPC.")
        return uid
    except Exception as e:
        print(f"❌ Erreur de connexion XML-RPC: {e}")
        sys.exit(1)

def link_data():
    """Lier les templates et plans au serveur par défaut."""
    print("🔗 Liaison des templates et plans au serveur...")
    try:
        uid = db_connect(DB)
        print(f"✅ Connecté avec uid: {uid}")

        common = xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}/xmlrpc/2/common')
        models = xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}/xmlrpc/2/object')

        # 1. Trouver ou créer un serveur
        print("\n📡 Recherche du serveur...")
        server_ids = models.execute_kw(DB, uid, PASSWORD,
                                       'saas_portal.server', 'search',
                                       [[]])
        if not server_ids:
            print("⚠️  Aucun serveur trouvé, création d'un serveur par défaut...")
            server_id = models.execute_kw(DB, uid, PASSWORD,
                                         'saas_portal.server', 'create',
                                         [{
                                             'name': 'server-default',
                                             'request_scheme': 'http',
                                             'local_request_scheme': 'http',
                                             'request_port': 8069,
                                             'local_host': 'localhost',
                                             'local_port': '8069',
                                             'verify_ssl': False,
                                             'active': True,
                                             'sequence': 1,
                                         }])
            print(f"✅ Serveur créé: ID {server_id}")
        else:
            server_id = server_ids[0]
            server_data = models.execute_kw(DB, uid, PASSWORD,
                                           'saas_portal.server', 'read',
                                           [[server_id], ['name']])
            print(f"✅ Serveur trouvé: {server_data[0]['name']} (ID: {server_id})")

        # 2. Lier les templates au serveur
        print("\n🗄️  Liaison des templates au serveur...")
        template_names = ['template-odoo-standard', 'template-odoo-demo']
        for template_name in template_names:
            template_ids = models.execute_kw(DB, uid, PASSWORD,
                                            'saas_portal.database', 'search',
                                            [[('name', '=', template_name)]])
            if template_ids:
                template_id = template_ids[0]
                template_data = models.execute_kw(DB, uid, PASSWORD,
                                                 'saas_portal.database', 'read',
                                                 [[template_id], ['server_id']])
                if not template_data[0]['server_id']:
                    models.execute_kw(DB, uid, PASSWORD,
                                     'saas_portal.database', 'write',
                                     [[template_id], {'server_id': server_id}])
                    print(f"   ✅ Template '{template_name}' lié au serveur")
                else:
                    print(f"   ℹ️  Template '{template_name}' déjà lié à un serveur")
            else:
                print(f"   ⚠️  Template '{template_name}' non trouvé")

        # 3. Lier les plans au serveur
        print("\n💰 Liaison des plans au serveur...")
        plan_names = ['Plan Starter', 'Plan Business', 'Plan Demo']
        for plan_name in plan_names:
            plan_ids = models.execute_kw(DB, uid, PASSWORD,
                                        'saas_portal.plan', 'search',
                                        [[('name', '=', plan_name)]])
            if plan_ids:
                plan_id = plan_ids[0]
                plan_data = models.execute_kw(DB, uid, PASSWORD,
                                             'saas_portal.plan', 'read',
                                             [[plan_id], ['server_id']])
                if not plan_data[0]['server_id']:
                    models.execute_kw(DB, uid, PASSWORD,
                                     'saas_portal.plan', 'write',
                                     [[plan_id], {'server_id': server_id}])
                    print(f"   ✅ Plan '{plan_name}' lié au serveur")
                else:
                    print(f"   ℹ️  Plan '{plan_name}' déjà lié à un serveur")
            else:
                print(f"   ⚠️  Plan '{plan_name}' non trouvé")

        print("\n=== ✅ LIAISON TERMINÉE ===")
        print(f"\n📝 Prochaines étapes:")
        print("   1. Allez dans SaaS > Plans")
        print("   2. Ouvrez un plan (ex: Plan Starter)")
        print("   3. Cliquez sur 'Create template DB' pour activer le template")

    except xmlrpc.client.Fault as e:
        print(f"❌ Erreur XML-RPC: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    link_data()
