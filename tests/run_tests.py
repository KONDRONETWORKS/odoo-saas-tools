#!/usr/bin/env python3
"""
Script pour exécuter tous les tests unitaires et générer un rapport
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).parent.parent

def run_tests():
    """Exécute tous les tests et génère un rapport"""
    print("="*80)
    print("🧪 EXECUTION DES TESTS UNITAIRES - ODOO SAAS TOOLS")
    print("="*80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Tests à exécuter
    test_files = [
        "tests/test_modules_implementation.py",
        "tests/test_module_communication.py",
        "tests/test_module_validation.py",
    ]
    
    results = {}
    
    for test_file in test_files:
        test_path = ROOT_DIR / test_file
        if not test_path.exists():
            print(f"⚠️  Fichier de test non trouvé: {test_file}")
            continue
        
        print(f"\n📋 Exécution: {test_file}")
        print("-" * 80)
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_path), "-v", "--tb=short"],
                cwd=ROOT_DIR,
                capture_output=True,
                text=True
            )
            
            results[test_file] = {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
            }
            
            print(result.stdout)
            if result.stderr:
                print("Erreurs:", result.stderr)
            
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution de {test_file}: {e}")
            results[test_file] = {'error': str(e)}
    
    # Générer le rapport
    print("\n" + "="*80)
    print("📊 RAPPORT FINAL")
    print("="*80)
    
    total_tests = len(test_files)
    passed_tests = sum(1 for r in results.values() if r.get('returncode') == 0)
    failed_tests = total_tests - passed_tests
    
    print(f"\nTests exécutés: {total_tests}")
    print(f"✅ Réussis: {passed_tests}")
    print(f"❌ Échoués: {failed_tests}")
    
    # Suggestions
    print("\n" + "="*80)
    print("💡 SUGGESTIONS")
    print("="*80)
    
    if failed_tests > 0:
        print("\n⚠️  Certains tests ont échoué:")
        for test_file, result in results.items():
            if result.get('returncode') != 0:
                print(f"  - {test_file}")
        
        print("\n🔧 Actions recommandées:")
        print("  1. Vérifier que tous les modules existent")
        print("  2. Vérifier les manifests (__manifest__.py)")
        print("  3. Vérifier les dépendances entre modules")
        print("  4. Vérifier la structure des fichiers")
    else:
        print("\n✅ Tous les tests structurels sont passés!")
        print("\n🔧 Prochaines étapes:")
        print("  1. Exécuter les tests dans un environnement Odoo réel")
        print("  2. Tester les communications Portal <-> Server")
        print("  3. Tester les workflows complets")
        print("  4. Ajouter des tests d'intégration")
    
    return failed_tests == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

