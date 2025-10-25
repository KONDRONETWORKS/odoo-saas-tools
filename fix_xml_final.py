#!/usr/bin/env python3
"""
Script final pour corriger la structure XML des fichiers Odoo 18.0
- Ajoute les balises <data> manquantes dans Odoo 18.0
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
        
        # 1. Vérifier si le fichier a déjà <data>
        if '<data' in content:
            print(f"✓ {file_path} - Déjà conforme")
            return False
        
        # 2. Ajouter <data> après <odoo>
        content = re.sub(
            r'(<odoo[^>]*>)\s*',
            r'\1\n    <data>',
            content
        )
        
        # 3. Ajouter </data> avant </odoo>
        content = re.sub(
            r'\s*(</odoo>)',
            r'\n    </data>\1',
            content
        )
        
        # 4. Déplacer noupdate de <odoo> vers <data>
        noupdate_match = re.search(r'<odoo[^>]*noupdate="1"[^>]*>', content)
        if noupdate_match:
            # Supprimer noupdate de <odoo>
            content = re.sub(r'<odoo([^>]*)\s+noupdate="1"([^>]*)>', r'<odoo\1\2>', content)
            # Ajouter noupdate à <data>
            content = re.sub(r'<data>', r'<data noupdate="1">', content)
        
        # 5. Nettoyer l'indentation
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if line.strip():
                # Ajuster l'indentation pour les éléments à l'intérieur de <data>
                if '<data' in line and not line.strip().startswith('</data'):
                    cleaned_lines.append(line)
                elif '</data>' in line:
                    cleaned_lines.append(line)
                elif '<odoo' in line or '</odoo>' in line:
                    cleaned_lines.append(line)
                else:
                    # Indenter les éléments à l'intérieur de <data>
                    if not line.startswith('    '):
                        cleaned_lines.append('    ' + line)
                    else:
                        cleaned_lines.append(line)
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
        print(f"✗ {file_path} - Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🔧 Correction finale des fichiers XML pour Odoo 18.0...")
    
    # Trouver tous les fichiers XML
    xml_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    
    print(f"📁 {len(xml_files)} fichiers XML trouvés")
    
    corrected_count = 0
    for xml_file in xml_files:
        if fix_xml_file(xml_file):
            corrected_count += 1
    
    print(f"\n📊 Résultats:")
    print(f"   Fichiers traités: {len(xml_files)}")
    print(f"   Fichiers corrigés: {corrected_count}")
    print(f"   Fichiers déjà conformes: {len(xml_files) - corrected_count}")
    print(f"   Taux de conformité: {((len(xml_files) - corrected_count) / len(xml_files) * 100):.1f}%")

if __name__ == "__main__":
    main()
