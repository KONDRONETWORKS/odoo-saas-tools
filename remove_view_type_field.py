#!/usr/bin/env python3
"""
Script pour supprimer le champ 'view_type' des fichiers XML Odoo 18.0
Ce champ a été supprimé dans Odoo 18.0
"""
import os
import re
from pathlib import Path

def remove_view_type_field(file_path):
    """Supprimer le champ view_type des fichiers XML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer les lignes contenant view_type
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Garder la ligne si elle ne contient pas view_type
            if 'view_type' not in line:
                cleaned_lines.append(line)
            else:
                print(f"  Suppression: {line.strip()}")
        
        content = '\n'.join(cleaned_lines)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Champ view_type supprimé")
            return True
        else:
            print(f"✓ {file_path} - Aucun champ view_type trouvé")
            return False
            
    except Exception as e:
        print(f"✗ Erreur lors du traitement de {file_path}: {e}")
        return False

def main():
    print("🔧 SUPPRESSION du champ 'view_type' pour Odoo 18.0")
    print("==================================================")
    print("Le champ 'view_type' a été supprimé dans Odoo 18.0")
    print()
    
    project_root = Path(__file__).resolve().parent
    modified_files_count = 0
    
    # Trouver tous les fichiers XML
    xml_files = []
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith('.xml'):
                file_path = Path(root) / file
                # Exclure les fichiers dans .venv et __pycache__
                if '.venv' not in str(file_path) and '__pycache__' not in str(file_path):
                    xml_files.append(file_path)
    
    print(f"📁 {len(xml_files)} fichiers XML trouvés")
    print()
    
    for file_path in sorted(xml_files):
        relative_path = file_path.relative_to(project_root)
        print(f"🔍 Traitement de {relative_path}...")
        
        if remove_view_type_field(file_path):
            modified_files_count += 1
    
    print()
    print("📊 Statistiques Finales")
    print("=======================")
    print(f"Fichiers traités : {len(xml_files)}")
    print(f"Fichiers corrigés : {modified_files_count}")
    print(f"Fichiers déjà conformes : {len(xml_files) - modified_files_count}")
    
    if modified_files_count > 0:
        print("✅ Tous les champs 'view_type' ont été supprimés !")
        print("🎉 Compatibilité Odoo 18.0 améliorée !")
    else:
        print("ℹ️ Aucun champ 'view_type' trouvé dans les fichiers XML")

if __name__ == "__main__":
    main()
