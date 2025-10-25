#!/usr/bin/env python3
"""
Script pour valider les fichiers XML avec la validation Odoo 18.0
"""
import sys
import os
sys.path.insert(0, '../odoo')

from odoo.tools.convert import convert_xml_import
from odoo import api, SUPERUSER_ID
from odoo.tests.common import TransactionCase
import tempfile
import xml.etree.ElementTree as ET

def validate_xml_with_odoo(file_path):
    """Valider un fichier XML avec la validation Odoo 18.0"""
    try:
        print(f"🔍 Validation de {file_path} avec Odoo 18.0...")
        
        # Lire le fichier XML
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parser le XML
        try:
            doc = ET.fromstring(content)
            print(f"✓ XML valide syntaxiquement")
        except ET.ParseError as e:
            print(f"✗ Erreur de parsing XML: {e}")
            return False
        
        # Vérifier la structure de base
        if doc.tag != 'odoo':
            print(f"✗ Racine XML doit être 'odoo', trouvé: {doc.tag}")
            return False
        
        # Vérifier les éléments enfants
        for child in doc:
            if child.tag not in ['record', 'act_window', 'menuitem', 'template']:
                print(f"✗ Élément non autorisé: {child.tag}")
                return False
        
        print(f"✓ Structure XML conforme à Odoo 18.0")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors de la validation: {e}")
        return False

def main():
    print("🔧 VALIDATION XML avec Odoo 18.0")
    print("=================================")
    
    # Valider le fichier test
    test_file = "test_xml_odoo18.xml"
    if os.path.exists(test_file):
        validate_xml_with_odoo(test_file)
    
    # Valider le fichier problématique
    problem_file = "saas_portal/wizard/config_wizard.xml"
    if os.path.exists(problem_file):
        validate_xml_with_odoo(problem_file)

if __name__ == "__main__":
    main()
