#!/usr/bin/env python3
"""
Script pour installer automatiquement le module queue_job
"""
import xmlrpc.client
import sys
import os

# Configuration
ODOO_URL = os.getenv("ODOO_URL", "http://localhost:8069")
DB_NAME = os.getenv("DB_NAME", "odoo")  # Utiliser la base par défaut
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

def install_queue_job():
    """Installe le module queue_job"""
    try:
        print(f"🔌 Connexion à Odoo: {ODOO_URL}")
        print(f"📦 Base de données: {DB_NAME}")
        
        # Connexion à Odoo
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(DB_NAME, ADMIN_USER, ADMIN_PASSWORD, {})
        
        if not uid:
            print("❌ Erreur d'authentification")
            print(f"💡 Vérifiez les identifiants: {ADMIN_USER}/{ADMIN_PASSWORD}")
            return False
        
        print(f"✅ Connecté à Odoo (UID: {uid})")
        
        # Accès aux modèles
        models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
        
        # Mettre à jour la liste des modules
        print("🔄 Mise à jour de la liste des modules...")
        try:
            models.execute_kw(
                DB_NAME, uid, ADMIN_PASSWORD,
                'ir.module.module', 'update_list',
                []
            )
            print("✅ Liste des modules mise à jour")
        except Exception as e:
            print(f"⚠️  Erreur lors de la mise à jour: {e}")
        
        # Chercher le module queue_job
        print("🔍 Recherche du module queue_job...")
        module_ids = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'ir.module.module', 'search',
            [[['name', '=', 'queue_job']]]
        )
        
        if not module_ids:
            print("❌ Module queue_job non trouvé dans la base de données")
            print("💡 Vérifiez que le module est dans le chemin des addons")
            print("💡 Chemin attendu: /mnt/extra-addons/oca_addons/queue/queue_job")
            return False
        
        # Lire les informations du module
        module_info = models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'ir.module.module', 'read',
            [module_ids],
            {'fields': ['name', 'state', 'summary', 'author']}
        )
        
        module = module_info[0]
        state = module['state']
        name = module['name']
        summary = module.get('summary', 'N/A')
        author = module.get('author', 'N/A')
        
        print(f"📦 Module trouvé: {name}")
        print(f"📝 Description: {summary}")
        print(f"👤 Auteur: {author}")
        print(f"📊 État actuel: {state}")
        
        if state == 'installed':
            print("✅ Module queue_job est déjà installé")
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
                print("✅ Module queue_job installé avec succès")
                return True
            except Exception as e:
                print(f"❌ Erreur lors de l'installation: {e}")
                import traceback
                traceback.print_exc()
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
    print("🚀 Installation automatique du module queue_job")
    print("=" * 60)
    print()
    
    success = install_queue_job()
    
    print()
    if success:
        print("=" * 60)
        print("✅ Installation terminée avec succès")
        print("=" * 60)
        sys.exit(0)
    else:
        print("=" * 60)
        print("❌ Installation échouée")
        print("=" * 60)
        sys.exit(1)

