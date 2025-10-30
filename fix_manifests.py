#!/usr/bin/env python3
"""
Script pour corriger tous les __manifest__.py en ajoutant les champs requis pour Odoo 18
"""

import os
import ast
import glob
import re

def fix_manifest(file_path):
    """Corriger un fichier manifest en ajoutant les champs manquants"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    try:
        # Parser le fichier pour vérifier la syntaxe
        manifest = ast.literal_eval(content)
    except (SyntaxError, ValueError) as e:
        print(f"⚠️  Erreur de syntaxe dans {file_path}: {e}")
        return False
    
    # Champs requis pour Odoo 18
    required_fields = {
        'application': False,  # La plupart des modules SaaS ne sont pas des applications
        'sequence': 10,       # Position par défaut
    }
    
    updated = False
    for key, value in required_fields.items():
        if key not in manifest:
            manifest[key] = value
            updated = True
    
    if updated:
        # Réécrire le fichier en préservant le format
        # Convertir le dict en string Python avec indent
        
        # Créer une nouvelle représentation
        output_lines = ['{\n']
        
        for key, value in manifest.items():
            if isinstance(value, str):
                output_lines.append(f"    '{key}': '{value}',\n")
            elif isinstance(value, list):
                output_lines.append(f"    '{key}': {value},\n")
            elif isinstance(value, dict):
                output_lines.append(f"    '{key}': {value},\n")
            elif isinstance(value, bool):
                output_lines.append(f"    '{key}': {value},\n")
            else:
                output_lines.append(f"    '{key}': {value},\n")
        
        output_lines.append('}\n')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(''.join(output_lines))
        
        print(f"✅ Corrigé {os.path.basename(os.path.dirname(file_path))}")
        return True
    
    return False

def main():
    """Fonction principale"""
    base_dir = '.'
    fixed_count = 0
    
    # Trouver tous les __manifest__.py
    manifest_files = glob.glob(os.path.join(base_dir, '*/__manifest__.py'))
    
    print(f"🔍 Recherche de {len(manifest_files)} fichiers manifest...\n")
    
    for manifest_file in sorted(manifest_files):
        if fix_manifest(manifest_file):
            fixed_count += 1
    
    print(f"\n✅ {fixed_count} fichiers manifest corrigés sur {len(manifest_files)}")

if __name__ == '__main__':
    main()
