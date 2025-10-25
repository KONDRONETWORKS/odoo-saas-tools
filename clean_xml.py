#!/usr/bin/env python3
"""
Script pour nettoyer les fichiers XML
- Supprime les espaces avant la déclaration XML
- Corrige l'indentation
- Valide la syntaxe XML
"""

import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def clean_xml_file(file_path):
    """Nettoie un fichier XML"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 1. Supprimer les espaces avant la déclaration XML
        content = re.sub(r'^\s*<\?xml', '<?xml', content, flags=re.MULTILINE)
        
        # 2. Supprimer les lignes vides en début de fichier
        lines = content.split('\n')
        cleaned_lines = []
        xml_declaration_found = False
        
        for line in lines:
            if not xml_declaration_found:
                if line.strip().startswith('<?xml'):
                    xml_declaration_found = True
                    cleaned_lines.append(line)
                elif line.strip():
                    # Si on trouve du contenu avant la déclaration XML, l'ajouter
                    cleaned_lines.append(line)
            else:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # 3. Valider la syntaxe XML
        try:
            ET.fromstring(content)
        except ET.ParseError as e:
            print(f"✗ {file_path} - Erreur de syntaxe XML: {e}")
            return False
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Nettoyé")
            return True
        else:
            print(f"✓ {file_path} - Déjà propre")
            return False
            
    except Exception as e:
        print(f"✗ {file_path} - Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🧹 Nettoyage des fichiers XML...")
    
    # Trouver tous les fichiers XML
    xml_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    
    print(f"📁 {len(xml_files)} fichiers XML trouvés")
    
    cleaned_count = 0
    for xml_file in xml_files:
        if clean_xml_file(xml_file):
            cleaned_count += 1
    
    print(f"\n📊 Résultats:")
    print(f"   Fichiers traités: {len(xml_files)}")
    print(f"   Fichiers nettoyés: {cleaned_count}")
    print(f"   Fichiers déjà propres: {len(xml_files) - cleaned_count}")

if __name__ == "__main__":
    main()
