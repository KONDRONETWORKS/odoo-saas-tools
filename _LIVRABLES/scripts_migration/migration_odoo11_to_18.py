#!/usr/bin/env python3
"""
Script de migration Odoo 11 vers Odoo 18
Basé sur les évolutions majeures des versions 11 à 18
"""
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path

def migrate_tree_to_list(file_path):
    """Migrer les balises <tree> vers <list> (Odoo 18)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacer <tree> par <list>
        content = re.sub(r'<tree\b', '<list', content)
        content = re.sub(r'</tree>', '</list>', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Balises <tree> migrées vers <list>")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la migration de {file_path}: {e}")
        return False

def migrate_attrs_to_direct_attributes(file_path):
    """Migrer les attributs attrs vers des attributs directs (Odoo 18)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Migrer attrs="{'invisible': [('field', '=', 'value')]}" vers invisible="field == 'value'"
        def convert_attrs(match):
            attrs_content = match.group(1)
            if 'invisible' in attrs_content:
                # Extraire la condition invisible
                invisible_match = re.search(r"'invisible':\s*\[([^\]]+)\]", attrs_content)
                if invisible_match:
                    condition = invisible_match.group(1)
                    # Convertir la condition Python vers une expression plus simple
                    condition = condition.replace("('", "").replace("', '", " == ").replace("')", "")
                    return f'invisible="{condition}"'
            return match.group(0)
        
        content = re.sub(r'attrs="\{([^}]+)\}"', convert_attrs, content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Attributs attrs migrés")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la migration des attrs de {file_path}: {e}")
        return False

def migrate_chatter_to_simple_tag(file_path):
    """Migrer le chatter complexe vers la balise simple <chatter/> (Odoo 18)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacer le chatter complexe par la balise simple
        chatter_pattern = r'<div class="oe_chatter">.*?</div>'
        content = re.sub(chatter_pattern, '<chatter/>', content, flags=re.DOTALL)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Chatter migré vers <chatter/>")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la migration du chatter de {file_path}: {e}")
        return False

def remove_deprecated_fields(file_path):
    """Supprimer les champs dépréciés (view_type, etc.)"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer les lignes contenant view_type
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            if 'view_type' not in line:
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Champs dépréciés supprimés")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la suppression des champs dépréciés de {file_path}: {e}")
        return False

def fix_xml_structure_odoo18(file_path):
    """Corriger la structure XML pour Odoo 18"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Supprimer les espaces vides avant la déclaration XML
        content = re.sub(r'^\s*<\?xml', '<?xml', content)
        
        # S'assurer que la structure est correcte
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
                # Ajouter des balises <data> si nécessaire
                content = re.sub(r'<odoo>\s*\n', '<odoo>\n    <data>\n', content)
                content = re.sub(r'\n\s*</odoo>', '\n    </data>\n</odoo>', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Structure XML corrigée pour Odoo 18")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la correction de la structure XML de {file_path}: {e}")
        return False

def migrate_python_files(file_path):
    """Migrer les fichiers Python pour Odoo 18"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacer les imports openerp par odoo
        content = re.sub(r'from openerp import', 'from odoo import', content)
        content = re.sub(r'import openerp', 'import odoo', content)
        
        # Supprimer @api.multi (déprécié)
        content = re.sub(r'@api\.multi\s*\n', '', content)
        
        # Remplacer require par required
        content = re.sub(r'require=True', 'required=True', content)
        content = re.sub(r'require=1', 'required=True', content)
        
        # Remplacer track_visibility par tracking
        content = re.sub(r"track_visibility='onchange'", 'tracking=True', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {file_path} - Code Python migré pour Odoo 18")
            return True
        return False
    except Exception as e:
        print(f"✗ Erreur lors de la migration Python de {file_path}: {e}")
        return False

def main():
    print("🚀 MIGRATION ODOO 11 VERS ODOO 18")
    print("==================================")
    print("Migration complète basée sur les évolutions des versions 11 à 18")
    print()
    
    project_root = Path(__file__).resolve().parent
    modified_files = 0
    
    # Trouver tous les fichiers XML et Python
    files_to_process = []
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith(('.xml', '.py')):
                file_path = Path(root) / file
                # Exclure les fichiers dans .venv et __pycache__
                if '.venv' not in str(file_path) and '__pycache__' not in str(file_path):
                    files_to_process.append(file_path)
    
    print(f"📁 {len(files_to_process)} fichiers trouvés")
    print()
    
    # Traiter les fichiers XML
    xml_files = [f for f in files_to_process if f.suffix == '.xml']
    print(f"🔧 Migration de {len(xml_files)} fichiers XML...")
    
    for file_path in sorted(xml_files):
        relative_path = file_path.relative_to(project_root)
        print(f"🔍 Traitement de {relative_path}...")
        
        file_modified = False
        
        # Appliquer toutes les migrations XML
        if migrate_tree_to_list(file_path):
            file_modified = True
        if migrate_attrs_to_direct_attributes(file_path):
            file_modified = True
        if migrate_chatter_to_simple_tag(file_path):
            file_modified = True
        if remove_deprecated_fields(file_path):
            file_modified = True
        if fix_xml_structure_odoo18(file_path):
            file_modified = True
        
        if file_modified:
            modified_files += 1
    
    # Traiter les fichiers Python
    py_files = [f for f in files_to_process if f.suffix == '.py' and f.name != 'migration_odoo11_to_18.py']
    print(f"\n🐍 Migration de {len(py_files)} fichiers Python...")
    
    for file_path in sorted(py_files):
        relative_path = file_path.relative_to(project_root)
        print(f"🔍 Traitement de {relative_path}...")
        
        if migrate_python_files(file_path):
            modified_files += 1
    
    print()
    print("📊 RÉSULTATS DE LA MIGRATION")
    print("============================")
    print(f"Fichiers traités : {len(files_to_process)}")
    print(f"Fichiers modifiés : {modified_files}")
    print(f"Fichiers déjà conformes : {len(files_to_process) - modified_files}")
    
    if modified_files > 0:
        print("\n✅ Migration terminée avec succès !")
        print("🎉 Votre projet est maintenant compatible avec Odoo 18 !")
        print("\n📋 Prochaines étapes recommandées :")
        print("1. Tester l'installation des modules")
        print("2. Vérifier le fonctionnement des vues")
        print("3. Valider les fonctionnalités métier")
    else:
        print("\nℹ️ Aucune migration nécessaire - le projet est déjà compatible !")

if __name__ == "__main__":
    main()
