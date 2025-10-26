#!/usr/bin/env python3
"""
Script pour corriger l'indentation des fichiers XML Odoo 18.0
- Corrige l'indentation pour être conforme à Odoo 18.0
- Valide la structure XML
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def fix_xml_indentation(file_path):
    """Corriger l'indentation d'un fichier XML pour Odoo 18.0"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Parser le XML pour reconstruire avec la bonne indentation
        try:
            root = ET.fromstring(content)
            
            # Reconstruire le XML avec la bonne indentation
            def indent_xml(elem, level=0):
                i = "\n" + level * "    "
                if len(elem):
                    if not elem.text or not elem.text.strip():
                        elem.text = i + "    "
                    if not elem.tail or not elem.tail.strip():
                        elem.tail = i
                    for child in elem:
                        indent_xml(child, level + 1)
                    if not child.tail or not child.tail.strip():
                        child.tail = i
                else:
                    if level and (not elem.tail or not elem.tail.strip()):
                        elem.tail = i
            
            indent_xml(root)
            
            # Convertir en string
            content = '<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(root, encoding='unicode')
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ {file_path} - Indentation corrigée")
                return True
            else:
                print(f"✓ {file_path} - Indentation déjà correcte")
                return False
                
        except ET.ParseError as e:
            print(f"✗ Erreur XML dans {file_path}: {e}")
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
    print("🔧 Correction de l'indentation XML pour Odoo 18.0")
    print("=================================================")
    
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
        
        if fix_xml_indentation(file_path):
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
        print("✅ TOUS les fichiers XML ont une indentation correcte pour Odoo 18.0 !")
    else:
        print(f"⚠️ {xml_errors_count} fichiers ont encore des erreurs XML")

if __name__ == "__main__":
    main()
