#!/usr/bin/env python3
"""
Script de vérification de compatibilité pour Odoo 18.0
"""

import sys
import subprocess
import importlib
try:
    import pkg_resources
except ImportError:
    # Fallback pour les versions récentes de Python
    import importlib.metadata as metadata
    pkg_resources = None
from pathlib import Path

def check_python_version():
    """Vérifier la version de Python"""
    print("🐍 Vérification de la version Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} détecté. Python 3.8+ requis.")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor} compatible.")
        return True

def check_dependencies():
    """Vérifier les dépendances Python"""
    print("\n📦 Vérification des dépendances...")
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Fichier requirements.txt non trouvé.")
        return False
    
    with open(requirements_file, 'r') as f:
        requirements = f.read().splitlines()
    
    missing_deps = []
    for req in requirements:
        if req.strip() and not req.startswith('#'):
            try:
                if pkg_resources:
                    pkg_resources.require(req)
                else:
                    # Utiliser importlib.metadata pour les versions récentes
                    package_name = req.split('>=')[0].split('==')[0]
                    metadata.distribution(package_name)
                print(f"✅ {req}")
            except (pkg_resources.DistributionNotFound, metadata.PackageNotFoundError):
                missing_deps.append(req)
                print(f"❌ {req} - Non installé")
            except (pkg_resources.VersionConflict, Exception) as e:
                print(f"⚠️  {req} - Version incompatible: {e}")
    
    if missing_deps:
        print(f"\n📋 Dépendances manquantes: {', '.join(missing_deps)}")
        print("💡 Installez avec: pip install -r requirements.txt")
        return False
    
    return True

def check_odoo_modules():
    """Vérifier la structure des modules Odoo"""
    print("\n🔍 Vérification des modules Odoo...")
    
    modules = [
        "saas_base", "saas_client", "saas_portal", "saas_server",
        "oauth_provider", "auth_oauth_check_client_id"
    ]
    
    issues = []
    for module in modules:
        module_path = Path(module)
        if not module_path.exists():
            issues.append(f"Module {module} non trouvé")
            continue
        
        manifest_path = module_path / "__manifest__.py"
        if not manifest_path.exists():
            issues.append(f"Manifest manquant pour {module}")
            continue
        
        # Vérifier la version dans le manifest
        with open(manifest_path, 'r') as f:
            content = f.read()
            if "'version': '18.0." not in content:
                issues.append(f"Version incorrecte dans {module}")
    
    if issues:
        for issue in issues:
            print(f"❌ {issue}")
        return False
    else:
        print("✅ Tous les modules sont correctement configurés.")
        return True

def check_postgresql():
    """Vérifier PostgreSQL"""
    print("\n🐘 Vérification de PostgreSQL...")
    try:
        result = subprocess.run(['psql', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.strip()
            print(f"✅ {version_line}")
            return True
        else:
            print("❌ PostgreSQL non trouvé ou non accessible")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ PostgreSQL non trouvé. Installez PostgreSQL 12+")
        return False

def main():
    """Fonction principale"""
    print("🚀 Vérification de compatibilité Odoo 18.0")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_odoo_modules(),
        check_postgresql()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 Toutes les vérifications sont passées !")
        print("✅ Votre environnement est prêt pour Odoo 18.0")
        return 0
    else:
        print("⚠️  Certaines vérifications ont échoué.")
        print("🔧 Corrigez les problèmes avant de continuer.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
