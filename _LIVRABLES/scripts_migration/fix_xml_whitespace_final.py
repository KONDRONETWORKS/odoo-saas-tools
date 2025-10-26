#!/usr/bin/env python3
"""
Script FINAL pour supprimer les espaces vides dans les fichiers XML Odoo 18.0
Le problème RelaxNG est causé par les espaces vides entre <odoo> et les éléments
"""
import os
import re
from pathlib import Path

def fix_xml_whitespace(file_path):
    """Supprimer les espaces vides dans les fichiers XML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer les espaces vides avant la déclaration XML
        content = re.sub(r'^\s*<\?xml', '<?xml', content)
        
        # Supprimer les espaces vides entre <odoo> et les éléments
        content = re.sub(r'<odoo>\s*\n\s*\n', '<odoo>\n', content)
        content = re.sub(r'<odoo>\s*\n\s*', '<odoo>\n', content)
        
        # Supprimer les espaces vides avant </odoo>
        content = re.sub(r'\n\s*\n\s*</odoo>', '\n</odoo>', content)
        
        # Nettoyer les espaces vides multiples
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Espaces vides supprimés")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la correction de {file_path}: {e}")
        return False

def main():
    print("🔧 SUPPRESSION DES ESPACES VIDES XML ODOO 18.0")
    print("==============================================")
    print("Suppression des espaces vides qui causent l'erreur RelaxNG")
    print()
    
    project_root = Path(__file__).resolve().parent
    xml_files = []
    
    # Trouver tous les fichiers XML
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith('.xml'):
                file_path = Path(root) / file
                # Exclure les fichiers dans .venv et __pycache__
                if '.venv' not in str(file_path) and '__pycache__' not in str(file_path):
                    xml_files.append(file_path)
    
    print(f"📁 {len(xml_files)} fichiers XML trouvés")
    print()
    
    corrected_count = 0
    for file_path in sorted(xml_files):
        relative_path = file_path.relative_to(project_root)
        print(f"🔍 Traitement de {relative_path}...")
        
        if fix_xml_whitespace(file_path):
            corrected_count += 1
    
    print()
    print("📊 RÉSULTATS FINAUX")
    print("===================")
    print(f"Fichiers traités : {len(xml_files)}")
    print(f"Fichiers corrigés : {corrected_count}")
    print(f"Fichiers déjà conformes : {len(xml_files) - corrected_count}")
    
    if corrected_count > 0:
        print("\n✅ Correction terminée avec succès !")
        print("🎉 Tous les espaces vides ont été supprimés !")
    else:
        print("\nℹ️ Aucune correction nécessaire - tous les fichiers sont déjà conformes !")

if __name__ == "__main__":
    main()
