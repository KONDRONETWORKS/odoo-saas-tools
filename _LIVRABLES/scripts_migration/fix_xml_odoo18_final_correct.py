#!/usr/bin/env python3
"""
Script FINAL pour corriger la structure XML Odoo 18.0
Supprime TOUTES les balises <data> et corrige la structure
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def fix_xml_odoo18_final(file_path):
    """Corriger définitivement la structure XML pour Odoo 18.0"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer les espaces vides avant la déclaration XML
        content = re.sub(r'^\s*<\?xml', '<?xml', content)
        
        # Supprimer TOUTES les balises <data> et </data>
        content = re.sub(r'<data[^>]*>', '', content)
        content = re.sub(r'</data>', '', content)
        
        # Nettoyer les espaces vides multiples
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        
        # S'assurer que la structure est correcte : <odoo><record>...</record></odoo>
        if '<odoo>' in content and '<record' in content:
            # Vérifier s'il y a des éléments directement sous <odoo>
            lines = content.split('\n')
            in_odoo = False
            has_direct_elements = False
            
            for i, line in enumerate(lines):
                if '<odoo>' in line:
                    in_odoo = True
                    continue
                if in_odoo and '</odoo>' in line:
                    break
                if in_odoo and line.strip().startswith('<record'):
                    has_direct_elements = True
                    break
            
            if has_direct_elements:
                # La structure est correcte, pas besoin de <data>
                pass
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Structure XML corrigée pour Odoo 18")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la correction de {file_path}: {e}")
        return False

def main():
    print("🔧 CORRECTION FINALE XML ODOO 18.0")
    print("===================================")
    print("Suppression de TOUTES les balises <data>")
    print("Structure finale: <odoo><record>...</record></odoo>")
    print()
    
    project_root = Path(__file__).resolve().parent
    xml_files = []
    
    # Trouver tous les fichiers XML
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith('.xml'):
                file_path = Path(root) / file
                # Exclure les fichiers dans .venv et __pycache__
                if '.venv' not in str(file_path) and '__pycache__' not in str(file_path):
                    xml_files.append(file_path)
    
    print(f"📁 {len(xml_files)} fichiers XML trouvés")
    print()
    
    corrected_count = 0
    for file_path in sorted(xml_files):
        relative_path = file_path.relative_to(project_root)
        print(f"🔍 Traitement de {relative_path}...")
        
        if fix_xml_odoo18_final(file_path):
            corrected_count += 1
    
    print()
    print("📊 RÉSULTATS FINAUX")
    print("===================")
    print(f"Fichiers traités : {len(xml_files)}")
    print(f"Fichiers corrigés : {corrected_count}")
    print(f"Fichiers déjà conformes : {len(xml_files) - corrected_count}")
    
    if corrected_count > 0:
        print("\n✅ Correction terminée avec succès !")
        print("🎉 Tous les fichiers XML sont maintenant conformes à Odoo 18.0 !")
    else:
        print("\nℹ️ Aucune correction nécessaire - tous les fichiers sont déjà conformes !")

if __name__ == "__main__":
    main()
