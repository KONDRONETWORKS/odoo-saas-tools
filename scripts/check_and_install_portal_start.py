#!/usr/bin/env python3
"""
Script pour vérifier et installer automatiquement saas_portal_start
"""
import xmlrpc.client
import sys
import os

# Configuration
ODOO_URL = "http://localhost:8069"
DB_NAME = "saas-portal-18.local"
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin"

def check_and_install_module():
    """Vérifie et installe saas_portal_start si nécessaire"""
    try:
        # Connexion à Odoo
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(DB_NAME, ADMIN_USER, ADMIN_PASSWORD, {})
        
        if not uid:
            print("❌ Erreur d'authentification")
            return False
        
        print(f"✅ Connecté à Odoo (UID: {uid})")
        
        # Accès aux modèles
        models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
        
        # Chercher le module saas_portal_start
        module_ids = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'ir.module.module', 'search',
            [[['name', '=', 'saas_portal_start']]]
        )
        
        if not module_ids:
            print("⚠️  Module saas_portal_start non trouvé dans la base de données")
            print("💡 Assurez-vous que le module est présent dans le répertoire des addons")
            return False
        
        # Lire les informations du module
        module_info = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'ir.module.module', 'read',
            [module_ids],
            {'fields': ['name', 'state', 'summary']}
        )
        
        module = module_info[0]
        state = module['state']
        name = module['name']
        
        print(f"📦 Module trouvé: {name}")
        print(f"📊 État actuel: {state}")
        
        if state == 'installed':
            print("✅ Module saas_portal_start est déjà installé")
            return True
        
        elif state in ['uninstalled', 'to install']:
            print(f"🔄 Installation du module {name}...")
            
            # Installer le module
            try:
                models.execute_kw(
                    DB_NAME, uid, ADMIN_PASSWORD,
                    'ir.module.module', 'button_immediate_install',
                    [module_ids]
                )
                print("✅ Module saas_portal_start installé avec succès")
                print("🌐 La page /page/start est maintenant accessible")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de l'installation: {e}")
                return False
        
        else:
            print(f"⚠️  État inattendu: {state}")
            print("💡 Vous pouvez essayer de mettre à jour la liste des modules dans Odoo")
            return False
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("🔍 Vérification et Installation de saas_portal_start")
    print("=" * 60)
    print()
    
    success = check_and_install_module()
    
    print()
    print("=" * 60)
    if success:
        print("✅ Opération terminée avec succès")
        sys.exit(0)
    else:
        print("⚠️  Opération terminée avec des avertissements")
        sys.exit(1)

