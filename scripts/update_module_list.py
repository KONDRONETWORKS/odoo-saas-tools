#!/usr/bin/env python3
"""
Script pour mettre à jour la liste des modules Odoo
"""
import xmlrpc.client
import sys

ODOO_URL = "http://localhost:8069"
DB_NAME = "saas-portal-18.local"
ADMIN_USER = "admin"
ADMIN_PASSWORD = "admin"

def update_module_list():
    """Met à jour la liste des modules"""
    try:
        common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
        uid = common.authenticate(DB_NAME, ADMIN_USER, ADMIN_PASSWORD, {})
        
        if not uid:
            print("❌ Erreur d'authentification")
            return False
        
        models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
        
        print("🔄 Mise à jour de la liste des modules...")
        models.execute_kw(
            DB_NAME, uid, ADMIN_PASSWORD,
            'ir.module.module', 'update_list',
            []
        )
        print("✅ Liste des modules mise à jour")
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    update_module_list()

