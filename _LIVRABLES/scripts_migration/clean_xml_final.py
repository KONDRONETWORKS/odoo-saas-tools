#!/usr/bin/env python3
"""
Script pour nettoyer définitivement les fichiers XML Odoo 18.0
- Supprime les espaces vides entre <odoo> et le premier élément
- Corrige l'indentation
- Valide la structure XML
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def clean_xml_file(file_path):
    """Nettoyer un fichier XML pour Odoo 18.0"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer les espaces vides entre <?xml> et <odoo>
        content = re.sub(r'^\s*<\?xml[^>]*>\s*\n\s*<odoo>', '<?xml version="1.0" encoding="utf-8"?>\n<odoo>', content)
        
        # Supprimer les espaces vides entre <odoo> et le premier élément
        content = re.sub(r'<odoo[^>]*>\s*\n\s*\n\s*<', '<odoo>\n        <', content)
        
        # Nettoyer l'indentation générale
        lines = content.split('\n')
        cleaned_lines = []
        in_xml_declaration = False
        in_odoo_tag = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('<?xml'):
                in_xml_declaration = True
                cleaned_lines.append(stripped)
            elif stripped.startswith('<odoo'):
                in_odoo_tag = True
                cleaned_lines.append(stripped)
            elif stripped.startswith('</odoo>'):
                in_odoo_tag = False
                cleaned_lines.append(stripped)
            elif stripped and in_xml_declaration and not in_odoo_tag:
                # Ligne entre XML declaration et <odoo>
                continue
            elif stripped and in_odoo_tag:
                # Indenter correctement les éléments dans <odoo>
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
            print(f"✓ {file_path} - Nettoyé")
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
    print("🧹 Nettoyage final des fichiers XML pour Odoo 18.0")
    print("==================================================")
    
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
        
        if clean_xml_file(file_path):
            modified_files_count += 1
        
        # Valider le XML après correction
        if not validate_xml(file_path):
            xml_errors_count += 1
    
    print()
    print("📊 Statistiques Finales")
    print("=======================")
    print(f"Fichiers traités : {len(xml_files)}")
    print(f"Fichiers nettoyés : {modified_files_count}")
    print(f"Fichiers déjà propres : {len(xml_files) - modified_files_count}")
    print(f"Erreurs XML : {xml_errors_count}")
    
    if xml_errors_count == 0:
        print("✅ Tous les fichiers XML sont maintenant propres et conformes à Odoo 18.0 !")
    else:
        print(f"⚠️ {xml_errors_count} fichiers ont encore des erreurs XML")

if __name__ == "__main__":
    main()
