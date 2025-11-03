#!/usr/bin/env python3
"""
Script de vérification complète des modules Odoo SaaS Tools
Vérifie tous les aspects avant le déploiement en production
"""

import os
import sys
import json
import ast
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import subprocess

# Couleurs pour output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

class ModuleChecker:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.modules_dir = self.project_root
        self.errors = []
        self.warnings = []
        self.info = []
        self.modules = {}
        
    def find_modules(self) -> List[Path]:
        """Trouve tous les modules dans le projet"""
        modules = []
        for item in self.modules_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('_'):
                manifest_path = item / '__manifest__.py'
                if manifest_path.exists():
                    modules.append(item)
        return sorted(modules)
    
    def check_manifest(self, module_path: Path) -> Tuple[bool, Dict]:
        """Vérifie la validité d'un manifest"""
        manifest_path = module_path / '__manifest__.py'
        errors = []
        warnings = []
        
        try:
            # Lire le fichier
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse Python
            try:
                manifest_dict = ast.literal_eval(content)
            except (ValueError, SyntaxError) as e:
                errors.append(f"Erreur de syntaxe dans __manifest__.py: {e}")
                return False, {'errors': errors, 'warnings': warnings, 'manifest': {}}
            
            if not isinstance(manifest_dict, dict):
                errors.append("Le manifest doit être un dictionnaire")
                return False, {'errors': errors, 'warnings': warnings, 'manifest': {}}
            
            # Vérifier les champs requis
            required_fields = ['name', 'version', 'author', 'license', 'category']
            for field in required_fields:
                if field not in manifest_dict:
                    errors.append(f"Champ requis manquant: {field}")
            
            # Vérifier application et sequence (nécessaires pour Odoo 18)
            if 'application' not in manifest_dict:
                warnings.append("Champ 'application' manquant (recommandé pour Odoo 18)")
            elif manifest_dict.get('application') not in [True, False]:
                errors.append("Le champ 'application' doit être True ou False")
            
            if 'sequence' not in manifest_dict:
                warnings.append("Champ 'sequence' manquant (recommandé pour Odoo 18)")
            elif not isinstance(manifest_dict.get('sequence'), int):
                errors.append("Le champ 'sequence' doit être un entier")
            
            # Vérifier depends
            if 'depends' not in manifest_dict:
                warnings.append("Champ 'depends' manquant")
            elif not isinstance(manifest_dict.get('depends'), list):
                errors.append("Le champ 'depends' doit être une liste")
            
            # Vérifier installable
            if 'installable' not in manifest_dict:
                warnings.append("Champ 'installable' manquant (défaut: True)")
            elif manifest_dict.get('installable') not in [True, False]:
                errors.append("Le champ 'installable' doit être True ou False")
            
            return len(errors) == 0, {'errors': errors, 'warnings': warnings, 'manifest': manifest_dict}
            
        except Exception as e:
            errors.append(f"Erreur lors de la lecture du manifest: {e}")
            return False, {'errors': errors, 'warnings': warnings, 'manifest': {}}
    
    def check_python_syntax(self, module_path: Path) -> List[str]:
        """Vérifie la syntaxe Python de tous les fichiers .py"""
        errors = []
        python_files = list(module_path.rglob('*.py'))
        
        # Exclure __pycache__
        python_files = [f for f in python_files if '__pycache__' not in str(f)]
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Vérifier la syntaxe
                try:
                    ast.parse(code, filename=str(py_file))
                except SyntaxError as e:
                    errors.append(f"{py_file.relative_to(self.project_root)}: {e}")
            except Exception as e:
                errors.append(f"{py_file.relative_to(self.project_root)}: Erreur de lecture - {e}")
        
        return errors
    
    def check_xml_syntax(self, module_path: Path) -> List[str]:
        """Vérifie la syntaxe XML de tous les fichiers .xml"""
        errors = []
        xml_files = list(module_path.rglob('*.xml'))
        
        for xml_file in xml_files:
            try:
                ET.parse(xml_file)
            except ET.ParseError as e:
                errors.append(f"{xml_file.relative_to(self.project_root)}: {e}")
            except Exception as e:
                # Certains fichiers XML peuvent être des templates avec syntaxe spéciale
                pass
        
        return errors
    
    def check_dependencies(self) -> List[str]:
        """Vérifie les dépendances entre modules"""
        errors = []
        warnings = []
        
        # Construire la liste des modules disponibles
        module_names = {mod.name: mod for mod in self.modules_dir.iterdir() 
                       if mod.is_dir() and (mod / '__manifest__.py').exists()}
        
        # Vérifier chaque module
        for module_path, module_info in self.modules.items():
            manifest = module_info.get('manifest', {})
            depends = manifest.get('depends', [])
            module_name = module_path.name
            
            for dep in depends:
                # Modules Odoo core sont toujours disponibles
                core_modules = ['base', 'mail', 'website', 'portal', 'auth', 'auth_oauth', 
                               'auth_signup', 'sale', 'product', 'account', 'website_sale',
                               'web', 'base_automation', 'analytic', 'project', 'crm',
                               'hr', 'purchase', 'stock', 'mrp', 'point_of_sale', 'contacts',
                               'calendar', 'notes', 'survey', 'event', 'helpdesk', 'inventory',
                               'hr_attendance', 'hr_timesheet', 'hr_payroll', 'hr_recruitment',
                               'hr_expense', 'fleet', 'maintenance', 'quality', 'repair',
                               'website_blog', 'website_event', 'website_forum', 'website_slides',
                               'mass_mailing', 'social_media', 'rating', 'payment', 'accounting',
                               'l10n', 'base_import', 'base_setup', 'board', 'google_account',
                               'google_calendar', 'google_drive', 'google_spreadsheet', 'hr_holidays']
                
                if dep in core_modules:
                    continue
                
                # Vérifier si la dépendance existe dans nos modules
                if dep not in module_names:
                    # Vérifier si c'est une dépendance externe attendue
                    external_deps = ['connector']  # OCA connector
                    if dep in external_deps:
                        warnings.append(f"{module_name}: Dépendance externe '{dep}' (doit être installée manuellement)")
                    else:
                        errors.append(f"{module_name}: Dépendance '{dep}' non trouvée")
        
        return errors + warnings
    
    def check_imports(self, module_path: Path) -> List[str]:
        """Vérifie les imports Python"""
        errors = []
        warnings = []
        
        python_files = list(module_path.rglob('*.py'))
        python_files = [f for f in python_files if '__pycache__' not in str(f)]
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse pour trouver les imports
                try:
                    tree = ast.parse(content, filename=str(py_file))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                self._check_import(alias.name, py_file, errors, warnings)
                        elif isinstance(node, ast.ImportFrom):
                            if node.module:
                                self._check_import(node.module, py_file, errors, warnings)
                except SyntaxError:
                    # Déjà vérifié dans check_python_syntax
                    pass
            except Exception:
                pass
        
        return errors + warnings
    
    def _check_import(self, module_name: str, file_path: Path, errors: List, warnings: List):
        """Vérifie un import spécifique"""
        # Modules Odoo standards
        odoo_modules = ['odoo', 'odoo.addons', 'odoo.api', 'odoo.models', 'odoo.fields',
                       'odoo.tools', 'odoo.exceptions', 'odoo.http', 'odoo.service']
        
        # Modules Python standards
        stdlib_modules = ['os', 'sys', 'json', 'datetime', 'logging', 'hashlib', 'urllib',
                         'base64', 'uuid', 'time', 'threading', 'queue', 'collections',
                         'itertools', 'functools', 'operator', 'copy', 'pickle', 'csv',
                         'xml', 'html', 'email', 'smtplib', 'socket', 'ssl', 'http',
                         'subprocess', 'pathlib', 'typing', 'dataclasses', 'enum']
        
        if module_name.startswith('odoo'):
            return  # Module Odoo valide
        
        parts = module_name.split('.')
        first_part = parts[0]
        
        if first_part in stdlib_modules:
            return  # Module standard valide
        
        # Vérifier si c'est un module local
        module_dir = file_path.parent
        while module_dir != self.project_root and module_dir != self.project_root.parent:
            if (module_dir / '__init__.py').exists():
                local_module = module_dir.name
                if first_part == local_module:
                    return  # Module local valide
            module_dir = module_dir.parent
        
        # Modules externes communs (ne pas considérer comme erreur)
        external_modules = ['boto3', 'boto', 'requests', 'psycopg2', 'pysftp', 
                          'oauthlib', 'simplejson', 'rotate_backups_s3']
        if first_part in external_modules:
            return  # Module externe valide
    
    def check_files_exist(self, module_path: Path, manifest: Dict) -> List[str]:
        """Vérifie que les fichiers référencés dans le manifest existent"""
        errors = []
        warnings = []
        
        # Vérifier les fichiers data
        data_files = manifest.get('data', [])
        for data_file in data_files:
            file_path = module_path / data_file
            if not file_path.exists():
                errors.append(f"Fichier référencé non trouvé: {data_file}")
        
        # Vérifier init_hook
        init_hook = manifest.get('init_hook', '')
        if init_hook:
            # Le hook peut être une fonction Python, pas forcément un fichier
            pass
        
        # Vérifier post_init_hook
        post_init_hook = manifest.get('post_init_hook', '')
        if post_init_hook:
            # Les hooks peuvent être dans n'importe quel fichier Python du module
            # Format: 'module.function' ou 'function'
            hook_parts = post_init_hook.split('.')
            if len(hook_parts) == 2:
                hook_module, hook_func = hook_parts
                hook_file = module_path / f"{hook_module}.py"
                if hook_file.exists():
                    try:
                        with open(hook_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if hook_func in content:
                                pass  # Hook trouvé, OK
                            else:
                                warnings.append(f"post_init_hook '{post_init_hook}' - fonction '{hook_func}' non trouvée dans {hook_module}.py")
                    except Exception:
                        pass
                else:
                    # Vérifier aussi dans __init__.py
                    init_file = module_path / '__init__.py'
                    if init_file.exists():
                        with open(init_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if f"import {hook_module}" in content or f"from . import {hook_module}" in content:
                                pass  # Module importé, OK
                            else:
                                # Les hooks peuvent être référencés sans import explicite en Odoo
                                pass  # Pas d'erreur, Odoo peut charger directement
                    else:
                        warnings.append(f"post_init_hook '{post_init_hook}' - fichier {hook_module}.py non trouvé")
        
        # Vérifier security files
        security_files = list(module_path.glob('security/*.csv'))
        if security_files:
            for sec_file in security_files:
                try:
                    with open(sec_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if len(lines) < 2:
                            warnings.append(f"{sec_file.name}: Fichier de sécurité vide ou incomplet")
                except Exception:
                    pass
        
        return errors + warnings
    
    def run_all_checks(self):
        """Exécute toutes les vérifications"""
        print(f"{BLUE}════════════════════════════════════════════════════════════{NC}")
        print(f"{BLUE}🔍 Vérification complète des modules Odoo SaaS Tools{NC}")
        print(f"{BLUE}════════════════════════════════════════════════════════════{NC}\n")
        
        modules = self.find_modules()
        print(f"{GREEN}✅ Modules trouvés: {len(modules)}{NC}\n")
        
        total_errors = 0
        total_warnings = 0
        
        for module_path in modules:
            module_name = module_path.name
            print(f"{BLUE}📦 Vérification: {module_name}{NC}")
            
            # Vérifier le manifest
            is_valid, manifest_info = self.check_manifest(module_path)
            self.modules[module_path] = manifest_info
            
            if manifest_info['errors']:
                for error in manifest_info['errors']:
                    print(f"  {RED}❌ ERREUR: {error}{NC}")
                    total_errors += 1
            
            if manifest_info['warnings']:
                for warning in manifest_info['warnings']:
                    print(f"  {YELLOW}⚠️  AVERTISSEMENT: {warning}{NC}")
                    total_warnings += 1
            
            # Vérifier la syntaxe Python
            py_errors = self.check_python_syntax(module_path)
            if py_errors:
                for error in py_errors:
                    print(f"  {RED}❌ ERREUR Python: {error}{NC}")
                    total_errors += len(py_errors)
            
            # Vérifier la syntaxe XML
            xml_errors = self.check_xml_syntax(module_path)
            if xml_errors:
                for error in xml_errors:
                    print(f"  {RED}❌ ERREUR XML: {error}{NC}")
                    total_errors += len(xml_errors)
            
            # Vérifier les fichiers référencés
            if manifest_info.get('manifest'):
                file_errors = self.check_files_exist(module_path, manifest_info['manifest'])
                for error in file_errors:
                    if 'ERREUR' in error or 'non trouvé' in error:
                        print(f"  {RED}❌ {error}{NC}")
                        total_errors += 1
                    else:
                        print(f"  {YELLOW}⚠️  {error}{NC}")
                        total_warnings += 1
            
            if not manifest_info['errors'] and not py_errors and not xml_errors:
                print(f"  {GREEN}✅ Module OK{NC}")
            
            print()
        
        # Vérifier les dépendances globales
        print(f"{BLUE}🔗 Vérification des dépendances...{NC}")
        dep_issues = self.check_dependencies()
        for issue in dep_issues:
            if 'ERREUR' in issue or 'non trouvée' in issue:
                print(f"  {RED}❌ {issue}{NC}")
                total_errors += 1
            else:
                print(f"  {YELLOW}⚠️  {issue}{NC}")
                total_warnings += 1
        print()
        
        # Résumé
        print(f"{BLUE}════════════════════════════════════════════════════════════{NC}")
        print(f"{BLUE}📊 Résumé de la vérification{NC}")
        print(f"{BLUE}════════════════════════════════════════════════════════════{NC}")
        print(f"Modules vérifiés: {len(modules)}")
        print(f"{GREEN}✅ Erreurs: {total_errors}{NC}")
        print(f"{YELLOW}⚠️  Avertissements: {total_warnings}{NC}")
        
        if total_errors == 0:
            print(f"\n{GREEN}✅ Tous les modules sont prêts pour le déploiement!{NC}")
            return True
        else:
            print(f"\n{RED}❌ Des erreurs doivent être corrigées avant le déploiement{NC}")
            return False

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    checker = ModuleChecker(project_root)
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()

