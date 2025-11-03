#!/usr/bin/env python3
"""
Script pour renommer les modules SaaS sans préfixe saas_*
"""

import os
import shutil
import re
from pathlib import Path

# Mappings des modules à renommer
MODULE_RENAMES = {
    'saas_oauth_provider': 'saas_oauth_provider',
    'saas_auth_oauth_check_client_id': 'saas_auth_oauth_check_client_id',
    'saas_auth_oauth_ip': 'saas_auth_oauth_ip',
    'saas_product_price_factor': 'saas_product_price_factor',
}

def update_file_content(file_path, mappings):
    """Mettre à jour le contenu d'un fichier avec les nouveaux noms de modules"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacer toutes les références
        for old_name, new_name in mappings.items():
            # Dans les depends
            content = re.sub(
                rf"(['\"]){re.escape(old_name)}\1",
                rf"\1{new_name}\1",
                content
            )
            # Dans les imports Python
            content = re.sub(
                rf"from {re.escape(old_name)}\b",
                f"from {new_name}",
                content
            )
            content = re.sub(
                rf"import {re.escape(old_name)}\b",
                f"import {new_name}",
                content
            )
            # Dans les ref XML (ref="module.id")
            content = re.sub(
                rf'ref="{re.escape(old_name)}\.',
                f'ref="{new_name}.',
                content
            )
            # Dans les chemins de fichiers
            content = re.sub(
                rf"/{re.escape(old_name)}/",
                f"/{new_name}/",
                content
            )
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de {file_path}: {e}")
    return False

def rename_modules(base_dir='.'):
    """Renommer les modules et mettre à jour toutes les références"""
    base_path = Path(base_dir)
    updated_files = []
    
    # Étape 1: Renommer les dossiers
    print("📦 Étape 1: Renommage des dossiers...")
    for old_name, new_name in MODULE_RENAMES.items():
        old_dir = base_path / old_name
        new_dir = base_path / new_name
        
        if old_dir.exists() and old_dir.is_dir():
            print(f"  Renommage: {old_name} → {new_name}")
            if new_dir.exists():
                print(f"  ⚠️  Le dossier {new_name} existe déjà !")
            else:
                shutil.move(str(old_dir), str(new_dir))
                print(f"  ✅ Dossier renommé")
        else:
            print(f"  ⚠️  Dossier {old_name} non trouvé")
    
    # Étape 2: Mettre à jour tous les fichiers
    print("\n📝 Étape 2: Mise à jour des références dans les fichiers...")
    
    # Parcourir tous les fichiers pertinents
    file_extensions = ['.py', '.xml', '.csv', '.rst', '.md', '.txt', '.conf']
    
    for ext in file_extensions:
        for file_path in base_path.rglob(f'*{ext}'):
            # Ignorer certains dossiers
            if any(ignore in str(file_path) for ignore in ['.git', '__pycache__', '.venv', 'filestore', '_build']):
                continue
            
            if update_file_content(file_path, MODULE_RENAMES):
                updated_files.append(file_path)
                print(f"  ✅ Mis à jour: {file_path}")
    
    print(f"\n✅ {len(updated_files)} fichiers mis à jour")
    return updated_files

if __name__ == '__main__':
    print("🔄 Renommage des modules SaaS...\n")
    print("Modules à renommer:")
    for old, new in MODULE_RENAMES.items():
        print(f"  - {old} → {new}")
    print()
    
    response = input("Continuer ? (oui/non): ")
    if response.lower() in ['oui', 'o', 'yes', 'y']:
        updated = rename_modules()
        print(f"\n✅ Terminé ! {len(updated)} fichiers modifiés")
        print("\n⚠️  ATTENTION: Vous devrez peut-être:")
        print("  1. Mettre à jour la base de données Odoo")
        print("  2. Vérifier les références XMLID dans ir.model.data")
        print("  3. Redémarrer le serveur Odoo")
    else:
        print("❌ Opération annulée")

