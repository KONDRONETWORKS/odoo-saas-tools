#!/usr/bin/env python3
"""
Script pour supprimer une base de données Odoo
"""
import psycopg2
import sys
import argparse

# Configuration par défaut
DB_HOST = "localhost"
DB_PORT = 5433  # Port Docker PostgreSQL
DB_USER = "odoo"
DB_PASSWORD = "odoo"

def drop_database(db_name, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD):
    """Supprime une base de données PostgreSQL"""
    try:
        # Connexion à la base de données par défaut (postgres)
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'  # On se connecte à postgres pour pouvoir supprimer d'autres bases
        )
        conn.autocommit = True  # Nécessaire pour DROP DATABASE
        cursor = conn.cursor()
        
        # Vérifier si la base existe
        cursor.execute("""
            SELECT datname FROM pg_database WHERE datname = %s;
        """, (db_name,))
        
        if not cursor.fetchone():
            print(f"⚠️  La base de données '{db_name}' n'existe pas")
            return False
        
        # Terminer toutes les connexions actives à la base
        print(f"🔄 Fermeture des connexions actives à '{db_name}'...")
        cursor.execute("""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = %s AND pid <> pg_backend_pid();
        """, (db_name,))
        
        # Supprimer la base de données
        print(f"🗑️  Suppression de la base de données '{db_name}'...")
        cursor.execute(f'DROP DATABASE "{db_name}";')
        
        cursor.close()
        conn.close()
        
        print(f"✅ Base de données '{db_name}' supprimée avec succès")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Erreur de connexion: {e}")
        print(f"💡 Vérifiez que PostgreSQL est accessible sur {host}:{port}")
        return False
    except psycopg2.Error as e:
        print(f"❌ Erreur PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        return False

def list_databases(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD):
    """Liste toutes les bases de données"""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database='postgres'
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT datname FROM pg_database 
            WHERE datistemplate = false 
            ORDER BY datname;
        """)
        
        databases = cursor.fetchall()
        cursor.close()
        conn.close()
        
        print("📋 Bases de données disponibles:")
        for db in databases:
            print(f"  - {db[0]}")
        
        return [db[0] for db in databases]
        
    except Exception as e:
        print(f"❌ Erreur lors de la liste: {e}")
        return []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Supprimer une base de données Odoo')
    parser.add_argument('db_name', nargs='?', help='Nom de la base de données à supprimer')
    parser.add_argument('--list', action='store_true', help='Lister toutes les bases de données')
    parser.add_argument('--host', default=DB_HOST, help=f'Host PostgreSQL (défaut: {DB_HOST})')
    parser.add_argument('--port', type=int, default=DB_PORT, help=f'Port PostgreSQL (défaut: {DB_PORT})')
    parser.add_argument('--user', default=DB_USER, help=f'Utilisateur PostgreSQL (défaut: {DB_USER})')
    parser.add_argument('--password', default=DB_PASSWORD, help=f'Mot de passe PostgreSQL (défaut: {DB_PASSWORD})')
    parser.add_argument('--confirm', action='store_true', help='Confirmer la suppression sans demander')
    
    args = parser.parse_args()
    
    if args.list:
        list_databases(args.host, args.port, args.user, args.password)
        sys.exit(0)
    
    if not args.db_name:
        print("❌ Veuillez spécifier le nom de la base de données à supprimer")
        print("💡 Utilisez --list pour voir les bases disponibles")
        sys.exit(1)
    
    print("=" * 60)
    print(f"🗑️  Suppression de la base de données: {args.db_name}")
    print("=" * 60)
    print()
    
    if not args.confirm:
        response = input(f"⚠️  Êtes-vous sûr de vouloir supprimer '{args.db_name}' ? (oui/non): ")
        if response.lower() not in ['oui', 'o', 'yes', 'y']:
            print("❌ Suppression annulée")
            sys.exit(0)
    
    success = drop_database(args.db_name, args.host, args.port, args.user, args.password)
    
    sys.exit(0 if success else 1)

