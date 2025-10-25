#!/usr/bin/env python3
"""
Script pour supprimer TOUTES les balises <data> des fichiers XML Odoo 18.0
Structure finale: <odoo><record>...</record></odoo>
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def remove_data_tags(file_path):
    """Supprimer les balises <data> des fichiers XML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Vérifier si le fichier a des balises <data>
        if '<data' not in content and '</data>' not in content:
            print(f"✓ {file_path} - Pas de balises <data> à supprimer")
            return False
        
        # Supprimer les balises <data> et </data>
        content = re.sub(r'<data[^>]*>', '', content)
        content = re.sub(r'</data>', '', content)
        
        # Nettoyer l'indentation
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('<?xml'):
                cleaned_lines.append(stripped)
            elif stripped.startswith('<odoo'):
                cleaned_lines.append(stripped)
            elif stripped.startswith('</odoo>'):
                cleaned_lines.append(stripped)
            elif stripped and not stripped.startswith('<!--'):
                # Ajuster l'indentation pour les éléments dans <odoo>
                if stripped.startswith('<record') or stripped.startswith('<act_window'):
                    cleaned_lines.append('    ' + stripped)
                elif stripped.startswith('</record>') or stripped.startswith('</act_window>'):
                    cleaned_lines.append('    ' + stripped)
                elif stripped.startswith('<field') or stripped.startswith('</field>'):
                    cleaned_lines.append('        ' + stripped)
                elif stripped.startswith('<form') or stripped.startswith('</form>') or stripped.startswith('<group') or stripped.startswith('</group>'):
                    cleaned_lines.append('            ' + stripped)
                elif stripped.startswith('<button') or stripped.startswith('</button>') or stripped.startswith('<footer') or stripped.startswith('</footer>'):
                    cleaned_lines.append('                ' + stripped)
                else:
                    cleaned_lines.append('    ' + stripped)
            else:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Balises <data> supprimées")
            return True
        else:
            print(f"✓ {file_path} - Aucune modification nécessaire")
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
    print("🔧 SUPPRESSION des balises <data> pour Odoo 18.0")
    print("================================================")
    print("Structure finale: <odoo><record>...</record></odoo>")
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
        
        if remove_data_tags(file_path):
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
