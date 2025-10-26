#!/usr/bin/env python3
"""
Script pour corriger les problèmes de références XML dans ir_module_module.xml
"""
import xml.etree.ElementTree as ET
import sys

def fix_module_xml():
    xml_file = '/Users/apple/KONDRO/odoo-sass/odoo/odoo/addons/base/data/ir_module_module.xml'
    
    # Parser le XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Trouver et commenter les enregistrements problématiques
    problematic_categories = [
        'base.module_category_services_timesheets',
        'base.module_category_marketing_email_marketing',
        'base.module_category_sales_pos',
        'base.module_category_sales_sales',
        'base.module_category_project_project',
        'base.module_category_manufacturing_manufacturing',
        'base.module_category_accounting_accounting',
    ]
    
    records_to_comment = []
    for record in root.findall('.//record[@model="ir.module.module"]'):
        category_ref = record.find('field[@name="category_id"]')
        if category_ref is not None and 'ref' in category_ref.attrib:
            ref_value = category_ref.get('ref')
            if ref_value in problematic_categories:
                records_to_comment.append(record)
    
    # Commenter les enregistrements problématiques
    if records_to_comment:
        print(f"Commentaire de {len(records_to_comment)} enregistrements problématiques...")
        for record in records_to_comment:
            # Créer un commentaire
            record_xml = ET.tostring(record, encoding='unicode')
            comment_text = f'\n        Temporarily commented out due to missing category\n        {record_xml}\n        '
            comment = ET.Comment(comment_text)
            
            # Trouver le parent
            for parent in root.iter():
                if record in list(parent):
                    parent.insert(list(parent).index(record), comment)
                    parent.remove(record)
                    break
    
    # Sauvegarder le fichier
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    print(f"✓ Fichier corrigé: {xml_file}")

if __name__ == "__main__":
    fix_module_xml()
