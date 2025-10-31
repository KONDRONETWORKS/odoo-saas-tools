#!/usr/bin/env python3
"""
Script pour vérifier les dépendances de tous les modules Odoo
"""
import os
import ast
import sys
from pathlib import Path
from collections import defaultdict

def extract_module_name_from_path(path):
    """Extrait le nom du module depuis le chemin"""
    return Path(path).parent.name

def parse_manifest(manifest_path):
    """Parse un fichier __manifest__.py et retourne les dépendances"""
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Exécuter le manifest comme du code Python
            manifest_dict = ast.literal_eval(content)
            module_name = extract_module_name_from_path(manifest_path)
            depends = manifest_dict.get('depends', [])
            if isinstance(depends, str):
                depends = [depends]
            return {
                'name': module_name,
                'depends': depends,
                'version': manifest_dict.get('version', 'N/A'),
                'installable': manifest_dict.get('installable', True)
            }
    except Exception as e:
        module_name = extract_module_name_from_path(manifest_path)
        print(f"⚠️  Erreur lors du parsing de {module_name}: {e}", file=sys.stderr)
        return {
            'name': module_name,
            'depends': [],
            'version': 'ERROR',
            'installable': False
        }

def find_all_modules(base_path):
    """Trouve tous les modules dans le répertoire"""
    modules = {}
    base = Path(base_path)
    for manifest_path in base.glob('*/__manifest__.py'):
        module_info = parse_manifest(manifest_path)
        modules[module_info['name']] = module_info
    return modules

def check_dependencies(modules):
    """Vérifie que toutes les dépendances existent"""
    module_names = set(modules.keys())
    issues = []
    dependency_graph = defaultdict(list)
    
    for module_name, module_info in modules.items():
        if not module_info.get('installable', True):
            continue
            
        for dep in module_info['depends']:
            dependency_graph[module_name].append(dep)
            
                # Vérifier si la dépendance existe dans nos modules
            if dep not in module_names:
                # Liste étendue des modules Odoo standards
                odoo_standard_modules = [
                    'base', 'web', 'website', 'sale', 'purchase', 'account',
                    'stock', 'crm', 'project', 'hr', 'mail', 'calendar',
                    'contacts', 'portal', 'auth', 'auth_oauth', 'auth_signup',
                    'product', 'sale_management', 'account_invoicing', 'contract',
                    'website_sale', 'base_automation', 'account_accountant',
                    'sale_crm', 'website_crm', 'website_membership',
                    'website_portal', 'website_blog', 'website_forum',
                    'payment', 'payment_transfer', 'website_payment'
                ]
                
                # Vérifier si c'est un module OCA commun
                oca_common_modules = [
                    'connector', 'component', 'component_event',
                    'website_sale_require_login'  # Module OCA e-commerce
                ]
                
                if dep not in odoo_standard_modules and dep not in oca_common_modules:
                    # Marquer comme dépendance externe potentielle
                    issues.append({
                        'module': module_name,
                        'missing_dep': dep,
                        'type': 'external' if dep.startswith('website_') or dep.startswith('payment_') else 'missing'
                    })
                elif dep in oca_common_modules:
                    # Marquer comme module OCA (nécessite installation externe)
                    issues.append({
                        'module': module_name,
                        'missing_dep': dep,
                        'type': 'oca'
                    })
    
    return issues, dependency_graph

def generate_report(modules, issues, dependency_graph):
    """Génère un rapport détaillé"""
    print("=" * 80)
    print("RAPPORT D'ANALYSE DES DÉPENDANCES DES MODULES")
    print("=" * 80)
    print()
    
    print(f"📦 Nombre total de modules trouvés: {len(modules)}")
    print()
    
    # Modules par catégorie
    print("=" * 80)
    print("LISTE DES MODULES")
    print("=" * 80)
    print(f"{'Module':<40} {'Version':<15} {'Installable':<12} {'Dépendances'}")
    print("-" * 80)
    
    for module_name in sorted(modules.keys()):
        info = modules[module_name]
        installable = "✅ Oui" if info.get('installable', True) else "❌ Non"
        deps = ', '.join(info['depends']) if info['depends'] else 'Aucune'
        print(f"{module_name:<40} {info['version']:<15} {installable:<12} {deps}")
    
    print()
    print("=" * 80)
    print("PROBLÈMES DÉTECTÉS")
    print("=" * 80)
    
    if not issues:
        print("✅ Aucun problème détecté ! Toutes les dépendances sont résolues.")
    else:
        print(f"ℹ️  {len(issues)} dépendance(s) externe(s) détectée(s):\n")
        
        oca_issues = [i for i in issues if i['type'] == 'oca']
        missing_issues = [i for i in issues if i['type'] == 'missing']
        
        if oca_issues:
            print("📦 Modules OCA (Odoo Community Association) requis:")
            for issue in oca_issues:
                if issue['missing_dep'] == 'website_sale_require_login':
                    print(f"  ⚠️  Module '{issue['module']}' nécessite '{issue['missing_dep']}'")
                    print(f"     → Disponible sur: https://github.com/OCA/e-commerce")
                    print(f"     → Installer depuis le dépôt OCA e-commerce")
                elif issue['missing_dep'] == 'connector':
                    print(f"  ⚠️  Module '{issue['module']}' nécessite '{issue['missing_dep']}'")
                    print(f"     → Module OCA connector (framework d'intégration)")
            print()
        
        if missing_issues:
            print("❌ Modules manquants (à vérifier):")
            for issue in missing_issues:
                print(f"  ⚠️  Module '{issue['module']}' dépend de '{issue['missing_dep']}' qui n'existe pas")
            print()
    
    print()
    print("=" * 80)
    print("GRAPHE DES DÉPENDANCES (modules internes uniquement)")
    print("=" * 80)
    
    internal_deps = {}
    for module_name, deps in dependency_graph.items():
        internal = [d for d in deps if d in modules.keys()]
        if internal:
            internal_deps[module_name] = internal
    
    if internal_deps:
        for module_name in sorted(internal_deps.keys()):
            print(f"\n{module_name}:")
            for dep in internal_deps[module_name]:
                print(f"  └─> {dep}")
    else:
        print("Aucune dépendance interne détectée.")
    
    print()
    return issues

if __name__ == '__main__':
    base_path = Path(__file__).parent
    modules = find_all_modules(base_path)
    issues, dependency_graph = check_dependencies(modules)
    generate_report(modules, issues, dependency_graph)
    
    if issues:
        sys.exit(1)
    else:
        sys.exit(0)

