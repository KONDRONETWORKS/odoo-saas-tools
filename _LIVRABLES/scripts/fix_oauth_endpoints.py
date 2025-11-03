#!/usr/bin/env python3
"""
Script pour corriger les endpoints OAuth qui pointent vers odoo.local
Utilisation: python3 fix_oauth_endpoints.py
"""

import sys
import os

# Ajoutez le chemin d'Odoo si nécessaire
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'odoo'))

import odoo
from odoo import api, SUPERUSER_ID

def fix_oauth_endpoints(dbname='odoo', domain='localhost:8069'):
    """Corriger les endpoints OAuth dans la base de données"""
    
    # Connexion à Odoo
    registry = odoo.registry(dbname)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Déterminer scheme et host
        if domain == 'localhost' or domain.startswith('127.0.0.1') or 'localhost' in domain:
            scheme = 'http'
            host = 'localhost:8069' if ':8069' not in domain else domain
        elif '.' in domain and not domain.startswith('localhost'):
            scheme = 'https' if not domain.startswith('localhost') else 'http'
            host = domain if ':' in domain else f'{domain}:8069'
        else:
            scheme = 'http'
            host = 'localhost:8069'
        
        auth_endpoint = f'{scheme}://{host}/oauth2/auth'
        validation_endpoint = f'{scheme}://{host}/oauth2/tokeninfo'
        
        print(f"🔧 Mise à jour des endpoints OAuth vers: {auth_endpoint}")
        
        # Mettre à jour saas_client provider
        try:
            provider = env.ref('saas_client.saas_oauth_provider', raise_if_not_found=False)
            if provider:
                old_auth = provider.auth_endpoint
                provider.write({
                    'auth_endpoint': auth_endpoint,
                    'validation_endpoint': validation_endpoint,
                })
                print(f"✅ saas_client provider mis à jour: {old_auth} → {auth_endpoint}")
            else:
                print("⚠️  saas_client.saas_oauth_provider non trouvé")
        except Exception as e:
            print(f"❌ Erreur mise à jour saas_client: {e}")
        
        # Mettre à jour saas_server provider
        try:
            provider = env.ref('saas_server.saas_oauth_provider', raise_if_not_found=False)
            if provider:
                old_auth = provider.auth_endpoint
                provider.write({
                    'auth_endpoint': auth_endpoint,
                    'validation_endpoint': validation_endpoint,
                })
                print(f"✅ saas_server provider mis à jour: {old_auth} → {auth_endpoint}")
            else:
                print("⚠️  saas_server.saas_oauth_provider non trouvé")
        except Exception as e:
            print(f"❌ Erreur mise à jour saas_server: {e}")
        
        # Vérifier le client_id pour saas_client
        try:
            provider = env.ref('saas_client.saas_oauth_provider', raise_if_not_found=False)
            if provider and not provider.client_id:
                dbuuid = env['ir.config_parameter'].sudo().get_param('database.uuid')
                if dbuuid:
                    provider.write({'client_id': dbuuid})
                    print(f"✅ client_id initialisé pour saas_client: {dbuuid}")
                else:
                    print("⚠️  database.uuid non trouvé, impossible d'initialiser client_id")
        except Exception as e:
            print(f"❌ Erreur initialisation client_id: {e}")
        
        cr.commit()
        print("\n✅ Correction terminée!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Corriger les endpoints OAuth')
    parser.add_argument('--db', default='odoo', help='Nom de la base de données')
    parser.add_argument('--domain', default='localhost:8069', 
                       help='Domaine à utiliser (ex: localhost:8069 ou odoo.example.com)')
    
    args = parser.parse_args()
    
    print("🔧 Correction des endpoints OAuth")
    print("=" * 50)
    fix_oauth_endpoints(dbname=args.db, domain=args.domain)

