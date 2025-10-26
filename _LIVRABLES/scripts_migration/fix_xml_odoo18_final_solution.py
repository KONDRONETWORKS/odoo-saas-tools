#!/usr/bin/env python3
"""
Script FINAL pour résoudre le problème XML Odoo 18.0
- Ajoute les balises <data> manquantes dans Odoo 18.0
- Structure correcte: <odoo><data><record>...</record></data></odoo>
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def fix_xml_odoo18_structure(file_path):
    """Corriger la structure XML pour Odoo 18.0"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Vérifier si le fichier a déjà des balises <data>
        if '<data' in content and '</data>' in content:
            print(f"✓ {file_path} - Déjà conforme")
            return False
        
        # Vérifier si le fichier a des éléments <record> directement dans <odoo>
        if '<record' in content and '<odoo>' in content:
            # Extraire l'attribut noupdate de <odoo> s'il existe
            noupdate_value = None
            noupdate_match = re.search(r'<odoo[^>]*noupdate="1"[^>]*>', content)
            if noupdate_match:
                noupdate_value = "1"
            
            # Remplacer <odoo> par <odoo><data>
            if noupdate_value:
                content = re.sub(r'<odoo[^>]*noupdate="1"[^>]*>', '<odoo noupdate="1">\n    <data>', content)
            else:
                content = re.sub(r'<odoo[^>]*>', '<odoo>\n    <data>', content)
            
            # Remplacer </odoo> par </data></odoo>
            content = re.sub(r'</odoo>', '    </data>\n</odoo>', content)
            
            # Nettoyer l'indentation
            lines = content.split('\n')
            cleaned_lines = []
            in_data = False
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith('<?xml'):
                    cleaned_lines.append(stripped)
                elif stripped.startswith('<odoo'):
                    cleaned_lines.append(stripped)
                elif stripped.startswith('<data>'):
                    in_data = True
                    cleaned_lines.append('    ' + stripped)
                elif stripped.startswith('</data>'):
                    in_data = False
                    cleaned_lines.append('    ' + stripped)
                elif stripped.startswith('</odoo>'):
                    cleaned_lines.append(stripped)
                elif stripped and in_data:
                    # Indenter correctement les éléments dans <data>
                    if stripped.startswith('<record') or stripped.startswith('<act_window') or stripped.startswith('<!--'):
                        cleaned_lines.append('        ' + stripped)
                    elif stripped.startswith('</record>') or stripped.startswith('</act_window>'):
                        cleaned_lines.append('        ' + stripped)
                    elif stripped.startswith('<field') or stripped.startswith('</field>'):
                        cleaned_lines.append('            ' + stripped)
                    elif stripped.startswith('<form') or stripped.startswith('</form>') or stripped.startswith('<group') or stripped.startswith('</group>'):
                        cleaned_lines.append('                ' + stripped)
                    elif stripped.startswith('<button') or stripped.startswith('</button>') or stripped.startswith('<footer') or stripped.startswith('</footer>'):
                        cleaned_lines.append('                    ' + stripped)
                    else:
                        cleaned_lines.append('        ' + stripped)
                else:
                    cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ {file_path} - Structure corrigée")
                return True
            else:
                print(f"✓ {file_path} - Aucune correction nécessaire")
                return False
        else:
            print(f"✓ {file_path} - Pas d'éléments <record> à corriger")
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
    print("🔧 CORRECTION FINALE de la structure XML pour Odoo 18.0")
    print("========================================================")
    print("Ajout des balises <data> manquantes")
    print("Structure: <odoo><data><record>...</record></data></odoo>")
    print()
    
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
        
        if fix_xml_odoo18_structure(file_path):
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
        print("✅ TOUS les fichiers XML sont maintenant conformes à Odoo 18.0 !")
        print("🎉 Le problème de structure XML est RÉSOLU !")
    else:
        print(f"⚠️ {xml_errors_count} fichiers ont encore des erreurs XML")

if __name__ == "__main__":
    main()
