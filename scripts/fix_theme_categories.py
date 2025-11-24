#!/usr/bin/env python3
"""
Script pour corriger les catégories des thèmes dans Odoo
À exécuter après chaque mise à jour de la liste des modules
"""

import odoo
import sys
import os

# Configuration
db_name = os.getenv('DB_NAME', 'odoo')
config_file = os.getenv('ODOO_CONFIG', 'odoo.conf')

# Initialisation Odoo
odoo.tools.config.parse_config(['-c', config_file])
registry = odoo.modules.registry.Registry.new(db_name)

with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    
    print("="*70)
    print("🔧 CORRECTION DES CATÉGORIES DE THÈMES")
    print("="*70)
    
    # Trouver les catégories
    themes_backend_cat = env['ir.module.category'].search([
        ('name', '=', 'Themes/Backend')
    ], limit=1)
    
    themes_website_cat = env['ir.module.category'].search([
        ('name', '=', 'Themes/Website')
    ], limit=1)
    
    # Créer si nécessaire
    if not themes_backend_cat:
        themes_parent = env['ir.module.category'].search([
            ('name', '=', 'Themes')
        ], limit=1)
        if themes_parent:
            themes_backend_cat = env['ir.module.category'].create({
                'name': 'Themes/Backend',
                'parent_id': themes_parent.id,
                'sequence': 1,
            })
            print("✅ Catégorie 'Themes/Backend' créée")
    
    if not themes_website_cat:
        themes_parent = env['ir.module.category'].search([
            ('name', '=', 'Themes')
        ], limit=1)
        if themes_parent:
            themes_website_cat = env['ir.module.category'].create({
                'name': 'Themes/Website',
                'parent_id': themes_parent.id,
                'sequence': 2,
            })
            print("✅ Catégorie 'Themes/Website' créée")
    
    # Assigner les thèmes
    backend_themes = ['theme_modern', 'theme_backend_odoo12', 'theme_hue_backend', 
                      'theme_diwy', 'theme_slife_backend', 'theme_ylhc_base']
    
    if themes_backend_cat:
        for theme_name in backend_themes:
            theme = env['ir.module.module'].search([('name', '=', theme_name)], limit=1)
            if theme:
                current_cat = theme.category_id.name if theme.category_id else 'N/A'
                if current_cat != 'Themes/Backend':
                    theme.sudo().write({'category_id': themes_backend_cat.id})
                    print(f"✅ {theme_name}: Catégorie corrigée vers 'Themes/Backend'")
    
    if themes_website_cat:
        website_theme = env['ir.module.module'].search([('name', '=', 'theme_magic3brothers')], limit=1)
        if website_theme:
            current_cat = website_theme.category_id.name if website_theme.category_id else 'N/A'
            if current_cat != 'Themes/Website':
                website_theme.sudo().write({'category_id': themes_website_cat.id})
                print(f"✅ theme_magic3brothers: Catégorie corrigée vers 'Themes/Website'")
    
    env.cr.commit()
    
    # Vérification finale
    print("\n" + "="*70)
    print("✅ VÉRIFICATION FINALE")
    print("="*70)
    
    backend_count = env['ir.module.module'].search_count([
        ('category_id', '=', themes_backend_cat.id if themes_backend_cat else False),
        ('name', 'in', backend_themes)
    ])
    
    website_count = env['ir.module.module'].search_count([
        ('category_id', '=', themes_website_cat.id if themes_website_cat else False),
        ('name', '=', 'theme_magic3brothers')
    ])
    
    print(f"✅ Thèmes dans 'Themes/Backend': {backend_count}/{len(backend_themes)}")
    print(f"✅ Thèmes dans 'Themes/Website': {website_count}/1")
    print("\n" + "="*70)

