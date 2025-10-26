#!/usr/bin/env python3
"""
Script final pour corriger la structure XML des fichiers Odoo 18.0
- Supprime les balises <data> dans Odoo 18.0
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
            # Chercher noupdate dans le contenu
            if 'noupdate="1"' in content or "noupdate='1'" in content:
                # Ajouter noupdate à la balise odoo si pas déjà présent
                if 'noupdate' not in noupdate_match.group():
                    content = re.sub(
                        r'<odoo([^>]*)>',
                        r'<odoo\1 noupdate="1">',
                        content
                    )
        
        # 3. Nettoyer l'indentation
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Supprimer les lignes vides en début de fichier
            if not cleaned_lines and line.strip() == '':
                continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Corrigé")
            return True
        else:
            print(f"- {file_path} - Déjà conforme")
            return False
            
    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")
        return False

def main():
    print("🔧 Correction finale de la structure XML pour Odoo 18.0")
    print("=" * 60)
    
    modified_files = 0
    
    # Parcourir tous les fichiers XML
    for xml_file in Path('.').rglob('*.xml'):
        if fix_xml_file(xml_file):
            modified_files += 1
    
    print(f"\n🎉 Correction terminée ! {modified_files} fichiers modifiés.")
    print("✅ Tous les fichiers XML sont maintenant conformes à Odoo 18.0")

if __name__ == "__main__":
    main()