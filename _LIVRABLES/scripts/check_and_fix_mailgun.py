#!/usr/bin/env python3
"""
Script pour vérifier et corriger le module saas_sysadmin_mailgun
"""
import sys
import os

# Ajouter le chemin d'Odoo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../odoo'))

import odoo
from odoo import api, SUPERUSER_ID

def check_module():
    """Vérifier l'état du module"""
    odoo.tools.config.parse_config(['-c', 'odoo.conf'])
    
    with odoo.api.Environment.manage():
        db_name = odoo.tools.config['db_name'] or 'odoo'
        
        try:
            registry = odoo.registry(db_name)
            with registry.cursor() as cr:
                env = api.Environment(cr, SUPERUSER_ID, {})
                
                # Vérifier si le module est installé
                module = env['ir.module.module'].search([
                    ('name', '=', 'saas_sysadmin_mailgun')
                ])
                
                if not module:
                    print("❌ Module saas_sysadmin_mailgun non trouvé dans la base")
                    return False
                
                print(f"✅ Module trouvé: {module.name}, État: {module.state}")
                
                # Vérifier si le modèle res.config.settings a le champ
                model = env['ir.model'].search([
                    ('model', '=', 'res.config.settings')
                ])
                
                if not model:
                    print("❌ Modèle res.config.settings non trouvé")
                    return False
                
                print(f"✅ Modèle res.config.settings trouvé (ID: {model.id})")
                
                # Vérifier si le champ existe
                field = env['ir.model.fields'].search([
                    ('model', '=', 'res.config.settings'),
                    ('name', '=', 'saas_mailgun_api_key')
                ])
                
                if field:
                    print(f"✅ Champ saas_mailgun_api_key trouvé (ID: {field.id})")
                else:
                    print("❌ Champ saas_mailgun_api_key non trouvé dans la base")
                    print("   Le champ doit être créé lors de la mise à jour du module")
                
                # Vérifier la vue
                view = env['ir.ui.view'].search([
                    ('name', '=', 'res.config.settings.view.form.inherit.sys_maigun')
                ])
                
                if view:
                    print(f"✅ Vue trouvée (ID: {view.id})")
                else:
                    print("❌ Vue non trouvée")
                
                return True
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("🔍 Vérification du module saas_sysadmin_mailgun...")
    print("=" * 60)
    check_module()
    print("=" * 60)
    print("\n💡 Si le champ n'existe pas, exécutez:")
    print("   python3.11 ../odoo/odoo-bin -c odoo.conf --stop-after-init -u saas_sysadmin_mailgun")

