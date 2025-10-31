#!/usr/bin/env python3
"""
Script pour corriger automatiquement @api.multi dans Odoo 18.0
"""

import os
import re
from pathlib import Path

def fix_api_multi_in_file(file_path):
    """Corriger @api.multi dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer @api.multi par rien (supprimer la ligne)
        # Garder l'indentation et le nom de la méthode
        pattern = r'(\s*)@api\.multi\s*\n(\s*def\s+\w+)'
        replacement = r'\2'
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Corrigé: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 Correction automatique de @api.multi pour Odoo 18.0")
    print("=" * 60)
    
    # Dossiers à traiter
    directories = [
        "saas_portal",
        "saas_oauth_provider", 
        "saas_base",
        "saas_client",
        "saas_server",
        "saas_auth_oauth_check_client_id",
        "saas_auth_oauth_ip"
    ]
    
    total_fixed = 0
    
    for directory in directories:
        if not os.path.exists(directory):
            continue
            
        print(f"\n📁 Traitement de {directory}/")
        dir_path = Path(directory)
        
        # Trouver tous les fichiers Python
        for py_file in dir_path.rglob("*.py"):
            if fix_api_multi_in_file(py_file):
                total_fixed += 1
    
    print(f"\n🎉 Correction terminée ! {total_fixed} fichiers modifiés.")
    print("✅ Tous les @api.multi ont été supprimés pour Odoo 18.0")

if __name__ == "__main__":
    main()
