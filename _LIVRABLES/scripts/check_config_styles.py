#!/usr/bin/env python3
"""
Script pour vérifier la compatibilité des styles dans les fichiers res_config.xml
avec les standards Odoo 18
"""
import os
import re
from pathlib import Path

# Standards Odoo 18 pour res.config.settings
ODOO18_STANDARDS = {
    'classes_col': ['col-12', 'col-lg-6', 'col-lg-10', 'col-lg-12'],
    'setting_structure': ['o_setting_box', 'o_setting_left_pane', 'o_setting_right_pane'],
    'container_classes': ['row', 'mt16', 'o_settings_container'],
    'field_widgets': {
        'password': 'widget="password"',  # Odoo 18
        'old_password': 'password="True"',  # Ancien (non compatible)
    },
    'field_classes': ['o_field_char', 'o_field_integer', 'o_field_boolean'],
}

def check_file(file_path):
    """Vérifier un fichier res_config.xml"""
    issues = []
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier password="True" (non compatible Odoo 18)
    if 'password="True"' in content:
        issues.append({
            'type': 'error',
            'message': 'Utilise password="True" au lieu de widget="password"',
            'file': file_path,
            'fix': 'Remplacer password="True" par widget="password"'
        })
    
    # Vérifier les classes col utilisées
    col_matches = re.findall(r'class="([^"]*col[^"]*)"', content)
    for match in col_matches:
        classes = match.split()
        has_col = any('col' in c for c in classes)
        if has_col:
            # Vérifier si c'est une classe Bootstrap valide
            valid_col = any(c in ODOO18_STANDARDS['classes_col'] or 
                          re.match(r'col-(xs|sm|md|lg|xl)-\d+', c) for c in classes)
            if not valid_col and 'col-' in match:
                issues.append({
                    'type': 'warning',
                    'message': f'Classe col potentiellement invalide: {match}',
                    'file': file_path
                })
    
    # Vérifier la structure o_setting
    if 'o_setting_box' in content:
        if 'o_setting_left_pane' not in content and 'o_setting_right_pane' not in content:
            issues.append({
                'type': 'info',
                'message': 'o_setting_box sans o_setting_left_pane/right_pane',
                'file': file_path
            })
    
    # Vérifier les styles inline (devraient être évités si possible)
    style_count = content.count('style=')
    if style_count > 10:
        issues.append({
            'type': 'info',
            'message': f'Utilise {style_count} styles inline - considérer CSS externe',
            'file': file_path
        })
    
    return issues

def main():
    """Vérifier tous les fichiers res_config.xml"""
    base_path = Path('/Users/apple/KONDRO/odoo-sass/odoo-saas-tools')
    
    config_files = list(base_path.rglob('**/res_config*.xml'))
    
    print("🔍 Vérification de la compatibilité avec Odoo 18")
    print("=" * 60)
    
    all_issues = []
    for config_file in config_files:
        issues = check_file(config_file)
        if issues:
            print(f"\n📄 {config_file.relative_to(base_path)}")
            for issue in issues:
                icon = {
                    'error': '❌',
                    'warning': '⚠️',
                    'info': 'ℹ️'
                }.get(issue['type'], '•')
                print(f"  {icon} {issue['message']}")
                if 'fix' in issue:
                    print(f"     → {issue['fix']}")
            all_issues.extend(issues)
    
    print("\n" + "=" * 60)
    if not all_issues:
        print("✅ Tous les fichiers sont compatibles avec Odoo 18 !")
    else:
        error_count = sum(1 for i in all_issues if i['type'] == 'error')
        warning_count = sum(1 for i in all_issues if i['type'] == 'warning')
        info_count = sum(1 for i in all_issues if i['type'] == 'info')
        print(f"📊 Résumé: {error_count} erreur(s), {warning_count} avertissement(s), {info_count} info(s)")
    
    return len([i for i in all_issues if i['type'] == 'error']) == 0

if __name__ == '__main__':
    exit(0 if main() else 1)

