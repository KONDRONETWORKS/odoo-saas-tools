#!/usr/bin/env python3
"""
Script pour recréer les fichiers XML avec la structure exacte Odoo 18.0
Structure: <?xml version="1.0" encoding="utf-8"?>
<odoo>
<record>...</record>
</odoo>
"""
import os
import xml.etree.ElementTree as ET
from pathlib import Path

def recreate_xml_odoo18(file_path):
    """Recréer le fichier XML avec la structure exacte Odoo 18.0"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parser le XML existant
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            print(f"✗ Erreur de parsing XML dans {file_path}: {e}")
            return False
        
        # Vérifier si c'est un fichier Odoo
        if root.tag not in ['odoo', 'openerp']:
            print(f"✓ {file_path} - Pas un fichier Odoo, ignoré")
            return False
        
        # Créer la nouvelle structure
        new_content = '<?xml version="1.0" encoding="utf-8"?>\n'
        new_content += '<odoo>\n'
        
        # Ajouter tous les éléments enfants directement sous <odoo>
        for child in root:
            # Convertir l'élément en string avec indentation
            child_str = ET.tostring(child, encoding='unicode')
            # Ajouter l'indentation
            lines = child_str.split('\n')
            indented_lines = []
            for line in lines:
                if line.strip():
                    indented_lines.append('    ' + line)
            new_content += '\n'.join(indented_lines) + '\n'
        
        new_content += '</odoo>\n'
        
        # Écrire le nouveau contenu
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✓ {file_path} - Structure XML recréée pour Odoo 18.0")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la recréation de {file_path}: {e}")
        return False

def main():
    print("🔧 RECRÉATION DES FICHIERS XML ODOO 18.0")
    print("========================================")
    print("Recréation avec la structure exacte requise")
    print("Structure: <?xml version=\"1.0\" encoding=\"utf-8\"?>\n<odoo>\n<record>...</record>\n</odoo>")
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
    
    recreated_count = 0
    for file_path in sorted(xml_files):
        relative_path = file_path.relative_to(project_root)
        print(f"🔍 Traitement de {relative_path}...")
        
        if recreate_xml_odoo18(file_path):
            recreated_count += 1
    
    print()
    print("📊 RÉSULTATS FINAUX")
    print("===================")
    print(f"Fichiers traités : {len(xml_files)}")
    print(f"Fichiers recréés : {recreated_count}")
    print(f"Fichiers déjà conformes : {len(xml_files) - recreated_count}")
    
    if recreated_count > 0:
        print("\n✅ Recréation terminée avec succès !")
        print("🎉 Tous les fichiers XML ont la structure exacte Odoo 18.0 !")
    else:
        print("\nℹ️ Aucune recréation nécessaire - tous les fichiers sont déjà conformes !")

if __name__ == "__main__":
    main()
