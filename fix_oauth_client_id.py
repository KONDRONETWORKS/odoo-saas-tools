#!/usr/bin/env python3
"""
Script pour initialiser le client_id du provider OAuth SaaS
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'odoo'))

import odoo
from odoo import api, SUPERUSER_ID

def fix_client_id(dbname='odoo'):
    """Initialiser le client_id pour les providers OAuth SaaS"""
    registry = odoo.registry(dbname)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Obtenir database.uuid
        dbuuid = env['ir.config_parameter'].sudo().get_param('database.uuid')
        if not dbuuid:
            print("❌ database.uuid non trouvé")
            return
        
        print(f"📋 Database UUID: {dbuuid}")
        
        # Corriger saas_client provider
        try:
            provider = env.ref('saas_client.saas_oauth_provider', raise_if_not_found=False)
            if provider:
                if not provider.client_id or provider.client_id == 'False':
                    provider.sudo().write({'client_id': dbuuid})
                    print(f"✅ saas_client provider: client_id initialisé = {dbuuid}")
                else:
                    print(f"ℹ️  saas_client provider: client_id déjà configuré = {provider.client_id}")
            else:
                print("⚠️  saas_client.saas_oauth_provider non trouvé")
        except Exception as e:
            print(f"❌ Erreur saas_client: {e}")
        
        # Corriger saas_server provider
        try:
            provider = env.ref('saas_server.saas_oauth_provider', raise_if_not_found=False)
            if provider:
                if not provider.client_id or provider.client_id == 'False':
                    provider.sudo().write({'client_id': dbuuid})
                    print(f"✅ saas_server provider: client_id initialisé = {dbuuid}")
                else:
                    print(f"ℹ️  saas_server provider: client_id déjà configuré = {provider.client_id}")
            else:
                print("⚠️  saas_server.saas_oauth_provider non trouvé")
        except Exception as e:
            print(f"❌ Erreur saas_server: {e}")
        
        cr.commit()
        print("\n✅ Correction terminée!")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Initialiser client_id pour providers OAuth')
    parser.add_argument('--db', default='odoo', help='Nom de la base de données')
    args = parser.parse_args()
    
    print("🔧 Initialisation client_id pour providers OAuth SaaS")
    print("=" * 50)
    fix_client_id(dbname=args.db)
