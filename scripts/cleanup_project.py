#!/usr/bin/env python3
"""
Script de nettoyage et réorganisation du projet Odoo SaaS Tools
Supprime les fichiers obsolètes, dupliqués et réorganise la structure
"""

import os
import shutil
from pathlib import Path
from datetime import datetime

# Répertoire racine du projet
ROOT_DIR = Path(__file__).parent.parent

# Fichiers/dossiers à supprimer
FILES_TO_DELETE = [
    # Fichiers de backup
    "config/docker-compose.windows.yml.backup",
    "docs/conf.py.backup",
    "saas_portal/views/res_config.xml.bak",
    
    # Fichiers obsolètes
    "saas_client/static/src/js/saas_dashboard.js.old",
    "saas_client/controllers/_web_settings_dashboard.py.old",
]

# Fichiers de documentation à consolider (déplacer vers _LIVRABLES/documentation/)
DOCS_TO_MOVE = [
    "ACCES_FINAL.md",
    "ETAT_APPLICATION.md",
    "INFORMATIONS_CONNEXION.md",
    "INITIALISATION_REUSSIE.md",
    "INSTRUCTIONS_DEMARRAGE.md",
    "RESUME_CONFIGURATION.md",
    "RESUME_FINAL.md",
    "SOLUTION_COMPLETE.md",
    "SOLUTION_POSTGRESQL.md",
    "STATUS_SAAS.md",
    "docs/CORRECTION_ROUTE_SAAS_SERVER.md",
    "docs/TEMPLATES_INITIALISATION.md",
]

# Dossiers temporaires à nettoyer
TEMP_DIRS = [
    "docs/temp",
    "docs/old_corrections",
    "docs/old_resumes",
]

def log(message):
    """Affiche un message avec timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def delete_file(filepath):
    """Supprime un fichier"""
    full_path = ROOT_DIR / filepath
    if full_path.exists():
        try:
            full_path.unlink()
            log(f"✅ Supprimé: {filepath}")
            return True
        except Exception as e:
            log(f"❌ Erreur suppression {filepath}: {e}")
            return False
    else:
        log(f"⚠️  Fichier non trouvé: {filepath}")
        return False

def move_file(source, destination):
    """Déplace un fichier"""
    src_path = ROOT_DIR / source
    dst_path = ROOT_DIR / destination
    
    if src_path.exists():
        try:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_path), str(dst_path))
            log(f"✅ Déplacé: {source} → {destination}")
            return True
        except Exception as e:
            log(f"❌ Erreur déplacement {source}: {e}")
            return False
    else:
        log(f"⚠️  Fichier non trouvé: {source}")
        return False

def cleanup_temp_dirs():
    """Nettoie les dossiers temporaires"""
    cleaned = 0
    for temp_dir in TEMP_DIRS:
        full_path = ROOT_DIR / temp_dir
        if full_path.exists() and full_path.is_dir():
            try:
                # Déplacer vers _LIVRABLES au lieu de supprimer
                dest = ROOT_DIR / "_LIVRABLES" / "archive" / temp_dir.replace("docs/", "")
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists():
                    shutil.rmtree(str(dest))
                shutil.move(str(full_path), str(dest))
                log(f"✅ Archivé: {temp_dir} → {dest}")
                cleaned += 1
            except Exception as e:
                log(f"❌ Erreur archivage {temp_dir}: {e}")
    return cleaned

def main():
    """Fonction principale"""
    log("🧹 Début du nettoyage du projet Odoo SaaS Tools")
    log(f"📁 Répertoire: {ROOT_DIR}")
    
    deleted = 0
    moved = 0
    
    # 1. Supprimer les fichiers obsolètes
    log("\n📋 Étape 1: Suppression des fichiers obsolètes")
    for filepath in FILES_TO_DELETE:
        if delete_file(filepath):
            deleted += 1
    
    # 2. Déplacer la documentation vers _LIVRABLES
    log("\n📋 Étape 2: Consolidation de la documentation")
    for doc in DOCS_TO_MOVE:
        if doc.startswith("docs/"):
            dest = f"_LIVRABLES/documentation/{Path(doc).name}"
        else:
            dest = f"_LIVRABLES/documentation/{doc}"
        if move_file(doc, dest):
            moved += 1
    
    # 3. Nettoyer les dossiers temporaires
    log("\n📋 Étape 3: Archivage des dossiers temporaires")
    archived = cleanup_temp_dirs()
    
    # Résumé
    log("\n" + "="*60)
    log(f"✅ Nettoyage terminé:")
    log(f"   - Fichiers supprimés: {deleted}")
    log(f"   - Fichiers déplacés: {moved}")
    log(f"   - Dossiers archivés: {archived}")
    log("="*60)

if __name__ == "__main__":
    main()

