#!/usr/bin/env python3
"""
Script pour restaurer les éléments act_window sans le champ view_type
"""
import os
from pathlib import Path

def restore_act_windows():
    """Restaurer les éléments act_window manquants"""
    
    # Restaurer action_edit_database dans config_wizard.xml
    config_wizard_path = Path("saas_portal/wizard/config_wizard.xml")
    if config_wizard_path.exists():
        with open(config_wizard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter l'action manquante avant la fermeture de </odoo>
        if 'action_edit_database' not in content:
            action_edit = '''    <act_window id="action_edit_database" name="Edit Database" res_model="saas_portal.edit_database" view_mode="form" target="new" />
'''
            content = content.replace('</odoo>', action_edit + '</odoo>')
            
            with open(config_wizard_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ action_edit_database restauré dans config_wizard.xml")
    
    # Restaurer action_duplicate_client dans config_wizard.xml
    if config_wizard_path.exists():
        with open(config_wizard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'action_duplicate_client' not in content:
            action_duplicate = '''    <act_window id="action_duplicate_client" name="Create More Like This" res_model="saas_portal.duplicate_client" src_model="saas_portal.client" target="new" view_mode="form" />
'''
            content = content.replace('</odoo>', action_duplicate + '</odoo>')
            
            with open(config_wizard_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ action_duplicate_client restauré dans config_wizard.xml")
    
    # Restaurer action_rename_database dans config_wizard.xml
    if config_wizard_path.exists():
        with open(config_wizard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'action_rename_database' not in content:
            action_rename = '''    <act_window id="action_rename_database" name="Rename Database" res_model="saas_portal.rename_database" view_mode="form" target="new" />
'''
            content = content.replace('</odoo>', action_rename + '</odoo>')
            
            with open(config_wizard_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ action_rename_database restauré dans config_wizard.xml")

def main():
    print("🔧 RESTAURATION des éléments act_window manquants")
    print("=================================================")
    print("Restauration des actions supprimées sans le champ view_type")
    print()
    
    restore_act_windows()
    
    print()
    print("✅ Actions restaurées !")
    print("🎉 Les références XML devraient maintenant fonctionner !")

if __name__ == "__main__":
    main()
