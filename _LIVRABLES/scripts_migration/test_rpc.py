#!/usr/bin/env python3
"""
Test simple pour vérifier le problème RPC
"""

import xmlrpc.client

# Connexion au serveur
server = xmlrpc.client.ServerProxy('http://127.0.0.1:8069/xmlrpc/2/object')

# Test de la méthode read
try:
    result = server.execute_kw('test_db', 1, 'admin', 'auth.oauth.provider', 'read', [1], {})
    print(f"Résultat read: {result}")
except Exception as e:
    print(f"Erreur: {e}")
