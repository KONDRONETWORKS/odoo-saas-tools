#!/usr/bin/env python3
"""
Script pour supprimer @api.multi dans Odoo 18.0
"""

import os
import re
from pathlib import Path

def remove_api_multi(file_path):
    """Supprimer @api.multi d'un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer         content = re.sub(r'^\s*@api\.multi\s*$', '', content, flags=re.MULTILINE)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - @api.multi supprimé")
            return True
        else:
            print(f"- {file_path} - Aucun @api.multi trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")
        return False

def main():
    print("🔧 Suppression de @api.multi pour Odoo 18.0")
    print("=" * 50)
    
    modified_files = 0
    
    # Parcourir tous les fichiers Python
    for py_file in Path('.').rglob('*.py'):
        if remove_api_multi(py_file):
            modified_files += 1
    
    print(f"\n🎉 Correction terminée ! {modified_files} fichiers modifiés.")
    print("✅ Tous les @api.multi ont été supprimés pour Odoo 18.0")

if __name__ == "__main__":
    main()
