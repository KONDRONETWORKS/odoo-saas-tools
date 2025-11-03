#!/usr/bin/env python3
"""
Script complet pour créer un nouveau client SaaS
Création: Serveur → Plan → Client

Usage:
    python3 scripts/create_complete_setup.py \
        --server-name server-1 \
        --plan-name "Plan Starter" \
        --client-name client-1 \
        --partner-email client@example.com
"""

import sys
import os
import argparse

# Ajouter le chemin Odoo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from odoo import api, SUPERUSER_ID
    from odoo.tools import config
    from odoo.service.db import db_connect
except ImportError:
    print("❌ Erreur: Impossible d'importer Odoo")
    print("   Assurez-vous d'être dans l'environnement Odoo")
    sys.exit(1)


def create_complete_saas_setup(
    portal_db='saas-portal-18.local',
    server_name='server-1',
    server_host='localhost',
    plan_name='Plan Starter',
    plan_price=99.00,
    plan_trial_days=14,
    client_name=None,
    partner_email='client@example.com',
    partner_name=None,
    trial=False,
    verbose=False,
):
    """
    Créer un setup SaaS complet : Serveur → Plan → Client
    """
    print("🚀 Création du setup SaaS complet...\n")
    
    # Générer le nom du client si non fourni
    if not client_name:
        import uuid
        client_name = f"client-{uuid.uuid4().hex[:8]}"
    
    # Générer le nom du partner si non fourni
    if not partner_name:
        partner_name = partner_email.split('@')[0].title()
    
    # Connexion au portail
    try:
        cr = db_connect(portal_db)
        registry = api.Environment(cr, SUPERUSER_ID, {})
        if verbose:
            print(f"✅ Connexion au portail: {portal_db}")
    except Exception as e:
        print(f"❌ Erreur connexion portail: {e}")
        return False
    
    try:
        # 1. Créer ou récupérer le serveur
        print(f"📦 Étape 1: Gestion du serveur '{server_name}'...")
        server = registry['saas_portal.server'].search([
            ('name', '=', server_name)
        ], limit=1)
        
        if not server:
            server = registry['saas_portal.server'].create({
                'name': server_name,
                'host': server_host,
                'max_clients': 100,
                'state': 'open',
            })
            print(f"   ✅ Serveur créé: {server.name}")
        else:
            print(f"   ℹ️  Serveur existant: {server.name}")
        
        # Synchroniser le serveur
        try:
            server.action_sync_server()
            print(f"   ✅ Serveur synchronisé")
        except Exception as e:
            print(f"   ⚠️  Erreur synchronisation: {e}")
        
        # 2. Créer ou récupérer le plan
        print(f"\n💰 Étape 2: Gestion du plan '{plan_name}'...")
        plan = registry['saas_portal.plan'].search([
            ('name', '=', plan_name)
        ], limit=1)
        
        if not plan:
            plan = registry['saas_portal.plan'].create({
                'name': plan_name,
                'server_id': server.id,
                'trial': plan_trial_days,
                'price': plan_price,
                'description': f'Plan {plan_name}',
            })
            print(f"   ✅ Plan créé: {plan.name}")
        else:
            print(f"   ℹ️  Plan existant: {plan.name}")
        
        # Vérifier si template DB existe
        if plan.template_id:
            print(f"   ℹ️  Template DB: {plan.template_id.name}")
        else:
            print(f"   ⚠️  Aucun template DB configuré pour ce plan")
        
        # 3. Créer ou récupérer le partner
        print(f"\n👤 Étape 3: Gestion du partner...")
        partner = registry['res.partner'].search([
            ('email', '=', partner_email)
        ], limit=1)
        
        if not partner:
            partner = registry['res.partner'].create({
                'name': partner_name,
                'email': partner_email,
            })
            print(f"   ✅ Partner créé: {partner.name} ({partner.email})")
        else:
            print(f"   ℹ️  Partner existant: {partner.name} ({partner.email})")
        
        # 4. Créer le client
        print(f"\n🚀 Étape 4: Création du client '{client_name}'...")
        client = registry['saas_portal.client'].search([
            ('name', '=', client_name)
        ], limit=1)
        
        if client:
            print(f"   ⚠️  Client existant: {client.name}")
            print(f"   ℹ️  URL: {client.public_url}")
            print(f"   ℹ️  State: {client.state}")
            return client
        
        try:
            print(f"   ⏳ Création en cours... (cela peut prendre quelques minutes)")
            result = plan.create_new_database(
                dbname=client_name,
                partner_id=partner.id,
                user_id=SUPERUSER_ID,
                trial=trial,
                notify_user=False,  # Pas d'email pour les tests
            )
            
            client = registry['saas_portal.client'].browse(result['id'])
            
            # Synchroniser le serveur après création
            try:
                client.server_id.action_sync_server()
                print(f"   ✅ Serveur synchronisé après création")
            except Exception as e:
                print(f"   ⚠️  Erreur synchronisation: {e}")
            
            print(f"\n✅ Client créé avec succès!")
            print(f"   📝 Nom: {client.name}")
            print(f"   🌐 URL: {client.public_url}")
            print(f"   📊 State: {client.state}")
            print(f"   💰 Plan: {client.plan_id.name if client.plan_id else 'N/A'}")
            print(f"   🖥️  Serveur: {client.server_id.name if client.server_id else 'N/A'}")
            print(f"   👤 Partner: {client.partner_id.name if client.partner_id else 'N/A'}")
            print(f"   📅 Expiration: {client.expiration_datetime or 'N/A'}")
            
            return client
            
        except Exception as e:
            print(f"   ❌ Erreur création client: {e}")
            import traceback
            traceback.print_exc()
            return None
        
    finally:
        cr.close()


def main():
    parser = argparse.ArgumentParser(
        description='Créer un setup SaaS complet: Serveur → Plan → Client'
    )
    
    parser.add_argument(
        '--portal-db',
        default='saas-portal-18.local',
        help='Nom de la base de données du portail'
    )
    
    parser.add_argument(
        '--server-name',
        default='server-1',
        help='Nom du serveur SaaS'
    )
    
    parser.add_argument(
        '--server-host',
        default='localhost',
        help='Host du serveur SaaS'
    )
    
    parser.add_argument(
        '--plan-name',
        default='Plan Starter',
        help='Nom du plan'
    )
    
    parser.add_argument(
        '--plan-price',
        type=float,
        default=99.00,
        help='Prix du plan'
    )
    
    parser.add_argument(
        '--plan-trial-days',
        type=int,
        default=14,
        help='Durée de la période d\'essai (jours)'
    )
    
    parser.add_argument(
        '--client-name',
        default=None,
        help='Nom de la base de données du client (auto-généré si non fourni)'
    )
    
    parser.add_argument(
        '--partner-email',
        default='client@example.com',
        help='Email du partner/client'
    )
    
    parser.add_argument(
        '--partner-name',
        default=None,
        help='Nom du partner/client (auto-généré si non fourni)'
    )
    
    parser.add_argument(
        '--trial',
        action='store_true',
        help='Créer le client en mode essai'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mode verbeux'
    )
    
    args = parser.parse_args()
    
    client = create_complete_saas_setup(
        portal_db=args.portal_db,
        server_name=args.server_name,
        server_host=args.server_host,
        plan_name=args.plan_name,
        plan_price=args.plan_price,
        plan_trial_days=args.plan_trial_days,
        client_name=args.client_name,
        partner_email=args.partner_email,
        partner_name=args.partner_name,
        trial=args.trial,
        verbose=args.verbose,
    )
    
    if client:
        print(f"\n✅ Setup complet créé avec succès!")
        print(f"\n🌐 Accéder au client: {client.public_url}")
        sys.exit(0)
    else:
        print(f"\n❌ Échec de la création")
        sys.exit(1)


if __name__ == '__main__':
    main()

