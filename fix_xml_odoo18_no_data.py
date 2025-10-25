#!/usr/bin/env python3
"""
Script pour corriger la structure XML des fichiers Odoo 18.0
- Supprime les balises <data> dans Odoo 18.0
- Corrige les attributs noupdate
- Valide la structure XML
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def fix_xml_file(file_path):
    """Corriger un fichier XML pour Odoo 18.0"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer les balises <data> et </data>
        content = re.sub(r'<data[^>]*>', '', content)
        content = re.sub(r'</data>', '', content)
        
        # Déplacer l'attribut noupdate de <data> vers <odoo>
        noupdate_match = re.search(r'<data[^>]*noupdate="1"[^>]*>', original_content)
        if noupdate_match:
            # Ajouter noupdate à <odoo> s'il n'y en a pas déjà
            if 'noupdate' not in content:
                content = re.sub(r'<odoo([^>]*)>', r'<odoo\1 noupdate="1">', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Corrigé")
            return True
        else:
            print(f"✓ {file_path} - Aucune correction nécessaire")
            return False
            
    except Exception as e:
        print(f"✗ Erreur lors du traitement de {file_path}: {e}")
        return False

def validate_xml(file_path):
    """Valider la structure XML"""
    try:
        ET.parse(file_path)
        return True
    except ET.ParseError as e:
        print(f"✗ Erreur XML dans {file_path}: {e}")
        return False

def main():
    print("🔧 Correction de la structure XML pour Odoo 18.0 (SANS balises <data>)")
    print("=====================================================================")
    
    project_root = Path(__file__).resolve().parent
    modified_files_count = 0
    xml_errors_count = 0
    
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
        
        if fix_xml_file(file_path):
            modified_files_count += 1
        
        # Valider le XML après correction
        if not validate_xml(file_path):
            xml_errors_count += 1
    
    print()
    print("📊 Statistiques Finales")
    print("=======================")
    print(f"Fichiers traités : {len(xml_files)}")
    print(f"Fichiers corrigés : {modified_files_count}")
    print(f"Fichiers déjà conformes : {len(xml_files) - modified_files_count}")
    print(f"Erreurs XML : {xml_errors_count}")
    
    if xml_errors_count == 0:
        print("✅ Tous les fichiers XML sont maintenant conformes à Odoo 18.0 !")
    else:
        print(f"⚠️ {xml_errors_count} fichiers ont encore des erreurs XML")

if __name__ == "__main__":
    main()