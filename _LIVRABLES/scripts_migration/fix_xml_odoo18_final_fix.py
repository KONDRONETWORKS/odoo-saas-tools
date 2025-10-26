#!/usr/bin/env python3
"""
Script FINAL pour corriger la structure XML des fichiers Odoo 18.0
- Supprime TOUTES les balises <data> et </data>
- Déplace l'attribut noupdate de <data> vers <odoo>
- Nettoie l'indentation
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
        
        # Vérifier si le fichier a des balises <data>
        if '<data' not in content and '</data>' not in content:
            print(f"✓ {file_path} - Déjà conforme")
            return False
        
        # Extraire l'attribut noupdate de <data> s'il existe
        noupdate_value = None
        noupdate_match = re.search(r'<data[^>]*noupdate="1"[^>]*>', content)
        if noupdate_match:
            noupdate_value = "1"
        
        # Supprimer toutes les balises <data> et </data>
        content = re.sub(r'<data[^>]*>', '', content)
        content = re.sub(r'</data>', '', content)
        
        # Ajouter noupdate="1" à <odoo> si nécessaire
        if noupdate_value and 'noupdate' not in content:
            content = re.sub(r'<odoo([^>]*)>', r'<odoo\1 noupdate="1">', content)
        
        # Nettoyer l'indentation
        lines = content.split('\n')
        cleaned_lines = []
        in_odoo = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('<?xml'):
                cleaned_lines.append(stripped)
            elif stripped.startswith('<odoo'):
                in_odoo = True
                cleaned_lines.append(stripped)
            elif stripped.startswith('</odoo>'):
                in_odoo = False
                cleaned_lines.append(stripped)
            elif stripped and in_odoo:
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
    print("🔧 CORRECTION FINALE de la structure XML pour Odoo 18.0")
    print("========================================================")
    print("Suppression de TOUTES les balises <data> et </data>")
    print("Déplacement de noupdate vers <odoo>")
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
        print("✅ TOUS les fichiers XML sont maintenant conformes à Odoo 18.0 !")
        print("🎉 Le problème de structure XML est RÉSOLU !")
    else:
        print(f"⚠️ {xml_errors_count} fichiers ont encore des erreurs XML")

if __name__ == "__main__":
    main()
