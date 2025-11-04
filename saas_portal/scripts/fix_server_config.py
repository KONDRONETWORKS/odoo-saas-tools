#!/usr/bin/env python3
"""
Script pour corriger la configuration des serveurs SaaS.
Assure que tous les serveurs ont local_host et local_port configurés.
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

def fix_servers():
    """Corriger la configuration de tous les serveurs."""
    print("🔧 Correction de la configuration des serveurs...")
    try:
        uid = db_connect(DB)
        print(f"✅ Connecté avec uid: {uid}")

        common = xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}/xmlrpc/2/common')
        models = xmlrpc.client.ServerProxy(f'http://{HOST}:{PORT}/xmlrpc/2/object')

        # Récupérer tous les serveurs
        print("\n📡 Recherche des serveurs...")
        server_ids = models.execute_kw(DB, uid, PASSWORD,
                                       'saas_portal.server', 'search',
                                       [[]])
        
        if not server_ids:
            print("⚠️  Aucun serveur trouvé!")
            return
        
        servers = models.execute_kw(DB, uid, PASSWORD,
                                   'saas_portal.server', 'read',
                                   [server_ids],
                                   {'fields': ['id', 'name', 'local_host', 'local_port', 'local_request_scheme', 'request_port']})
        
        print(f"\n📋 Serveurs trouvés: {len(servers)}")
        
        # Corriger chaque serveur
        for server in servers:
            server_id = server['id']
            server_name = server['name']
            needs_fix = False
            updates = {}
            
            # Vérifier local_host
            if not server.get('local_host'):
                updates['local_host'] = 'localhost'
                needs_fix = True
                print(f"\n   ⚠️  Serveur '{server_name}' (ID: {server_id}): local_host manquant")
            
            # Vérifier local_port
            if not server.get('local_port'):
                # Utiliser request_port si disponible, sinon 8069
                updates['local_port'] = str(server.get('request_port', 8069))
                needs_fix = True
                print(f"   ⚠️  Serveur '{server_name}' (ID: {server_id}): local_port manquant")
            
            # Vérifier local_request_scheme
            if not server.get('local_request_scheme'):
                updates['local_request_scheme'] = 'http'
                needs_fix = True
                print(f"   ⚠️  Serveur '{server_name}' (ID: {server_id}): local_request_scheme manquant")
            
            # Appliquer les corrections
            if needs_fix:
                models.execute_kw(DB, uid, PASSWORD,
                                 'saas_portal.server', 'write',
                                 [[server_id], updates])
                print(f"   ✅ Serveur '{server_name}' corrigé: {updates}")
            else:
                print(f"\n   ✅ Serveur '{server_name}' (ID: {server_id}): Configuration OK")
                print(f"      local_host: {server.get('local_host')}")
                print(f"      local_port: {server.get('local_port')}")
                print(f"      local_request_scheme: {server.get('local_request_scheme')}")
        
        print("\n=== ✅ CORRECTION TERMINÉE ===")
        print(f"\n📝 Vous pouvez maintenant créer des templates depuis les plans")

    except xmlrpc.client.Fault as e:
        print(f"❌ Erreur XML-RPC: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    fix_servers()
