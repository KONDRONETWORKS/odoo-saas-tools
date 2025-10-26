#!/usr/bin/env python3
"""
Script pour corriger la structure XML des fichiers Odoo 18.0
- Supprime les balises <data> inutiles dans Odoo 18.0
- Corrige les attributs noupdate
- Valide la structure XML
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def fix_xml_file(file_path):
    """Corrige un fichier XML pour Odoo 18.0"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Supprimer les balises <data> et </data>
        content = re.sub(r'<data[^>]*>', '', content)
        content = re.sub(r'</data>', '', content)
        
        # 2. Déplacer l'attribut noupdate de <data> vers <odoo>
        noupdate_match = re.search(r'<odoo[^>]*>', content)
        if noupdate_match:
            # Chercher noupdate dans le contenu original
            data_noupdate = re.search(r'<data[^>]*noupdate="([^"]*)"[^>]*>', original_content)
            if data_noupdate:
                noupdate_value = data_noupdate.group(1)
                # Ajouter noupdate à la balise odoo si pas déjà présent
                if 'noupdate=' not in noupdate_match.group(0):
                    content = re.sub(
                        r'<odoo([^>]*)>',
                        f'<odoo\\1 noupdate="{noupdate_value}">',
                        content
                    )
        
        # 3. Nettoyer les espaces et indentation
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Supprimer les lignes vides excessives
            if line.strip() == '' and len(cleaned_lines) > 0 and cleaned_lines[-1].strip() == '':
                continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # 4. Valider la structure XML
        try:
            ET.fromstring(content)
            print(f"✅ {file_path} - Structure XML valide")
        except ET.ParseError as e:
            print(f"❌ {file_path} - Erreur XML: {e}")
            return False
        
        # 5. Sauvegarder si des changements ont été faits
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"🔧 {file_path} - Fichier corrigé")
            return True
        else:
            print(f"✅ {file_path} - Aucune correction nécessaire")
            return True
            
    except Exception as e:
        print(f"❌ {file_path} - Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    project_root = Path(__file__).parent
    xml_files = list(project_root.rglob('*.xml'))
    
    print(f"🔍 Analyse de {len(xml_files)} fichiers XML...")
    print("=" * 60)
    
    fixed_count = 0
    error_count = 0
    
    for xml_file in xml_files:
        if fix_xml_file(xml_file):
            fixed_count += 1
        else:
            error_count += 1
    
    print("=" * 60)
    print(f"📊 Résumé:")
    print(f"   ✅ Fichiers traités avec succès: {fixed_count}")
    print(f"   ❌ Fichiers avec erreurs: {error_count}")
    print(f"   📁 Total de fichiers: {len(xml_files)}")

if __name__ == "__main__":
    main()
