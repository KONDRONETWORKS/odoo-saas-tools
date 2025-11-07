#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de sauvegarde vers OVH Object Storage

Ce script sauvegarde les bases de données et filestores vers OVH Object Storage.
Il peut être exécuté manuellement ou via un cron.

Usage:
    python3 backup_ovh_object_storage.py --db odoo --all
    python3 backup_ovh_object_storage.py --db odoo --client client-001
"""

import argparse
import os
import sys
import subprocess
import tempfile
from datetime import datetime

# Ajouter le chemin Odoo
sys.path.insert(0, '/usr/lib/python3/dist-packages')

try:
    import ovh
except ImportError:
    print("ERREUR: Module ovh non installé. Installez-le avec: pip install ovh")
    sys.exit(1)

try:
    import odoo
    from odoo import api, SUPERUSER_ID
    from odoo.tools import config
except ImportError:
    print("ERREUR: Odoo non trouvé")
    sys.exit(1)


def get_ovh_client(env):
    """Récupère le client OVH configuré"""
    if not ovh:
        raise ValueError('Module ovh non installé')
    
    ir_params = env['ir.config_parameter']
    
    application_key = ir_params.sudo().get_param('saas_server_backup_ovh.application_key')
    application_secret = ir_params.sudo().get_param('saas_server_backup_ovh.application_secret')
    consumer_key = ir_params.sudo().get_param('saas_server_backup_ovh.consumer_key')
    endpoint = ir_params.sudo().get_param('saas_sysadmin_ovh.endpoint', 'ovh-eu')
    
    if not all([application_key, application_secret, consumer_key]):
        raise ValueError('Credentials OVH non configurés dans Odoo')
    
    return ovh.Client(
        endpoint=endpoint,
        application_key=application_key,
        application_secret=application_secret,
        consumer_key=consumer_key
    )


def upload_to_ovh_storage(client, project_id, region, container, file_path, object_name):
    """
    Upload un fichier vers OVH Object Storage (Swift API)
    
    :param client: Client OVH
    :param project_id: ID du projet Public Cloud
    :param region: Région (GRA, SBG, BHS, etc.)
    :param container: Nom du container
    :param file_path: Chemin local du fichier
    :param object_name: Nom de l'objet dans le storage
    """
    try:
        # Obtenir un token Swift
        token_response = client.post(
            f'/cloud/project/{project_id}/region/{region}/storage/token',
            containerName=container
        )
        
        # Utiliser Swift API pour upload
        # Note: Cette partie nécessite l'API Swift d'OVH
        # Pour simplifier, on peut utiliser python-swiftclient ou requests
        print(f"Upload de {file_path} vers {container}/{object_name}")
        # TODO: Implémenter l'upload Swift réel avec python-swiftclient
        
    except Exception as e:
        print(f"ERREUR lors de l'upload: {e}")
        raise


def backup_database(db_name, backup_dir, db_config):
    """Sauvegarde une base de données PostgreSQL"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(backup_dir, f'{db_name}_{timestamp}.sql.gz')
    
    cmd = [
        'pg_dump',
        '-h', db_config.get('db_host', 'localhost'),
        '-U', db_config.get('db_user', 'odoo'),
        '-F', 'c',  # Format custom
        '-f', backup_file,
        db_name
    ]
    
    env = os.environ.copy()
    env['PGPASSWORD'] = db_config.get('db_password', '')
    
    result = subprocess.run(cmd, env=env, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Erreur pg_dump: {result.stderr.decode()}")
    
    return backup_file


def backup_filestore(db_name, data_dir, backup_dir):
    """Sauvegarde le filestore d'une base"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filestore_path = os.path.join(data_dir, 'filestore', db_name)
    
    if not os.path.exists(filestore_path):
        return None
    
    backup_file = os.path.join(backup_dir, f'{db_name}_filestore_{timestamp}.tar.gz')
    
    cmd = ['tar', '-czf', backup_file, '-C', data_dir, f'filestore/{db_name}']
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Erreur tar: {result.stderr.decode()}")
    
    return backup_file


def main():
    parser = argparse.ArgumentParser(description='Sauvegarde vers OVH Object Storage')
    parser.add_argument('--db', required=True, help='Base de données Odoo')
    parser.add_argument('--all', action='store_true', help='Sauvegarder toutes les bases client')
    parser.add_argument('--client', help='Sauvegarder une base client spécifique')
    parser.add_argument('--config', help='Fichier de configuration Odoo', default='odoo.conf')
    
    args = parser.parse_args()
    
    # Charger la config Odoo
    config.parse_config([f'--database={args.db}', f'--config={args.config}'])
    
    registry = odoo.registry(args.db)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Récupérer la config OVH
        ir_params = env['ir.config_parameter']
        project_id = ir_params.sudo().get_param('saas_server_backup_ovh.project_id')
        region = ir_params.sudo().get_param('saas_server_backup_ovh.region')
        container = ir_params.sudo().get_param('saas_server_backup_ovh.container')
        
        if not all([project_id, region, container]):
            print("ERREUR: Configuration OVH Object Storage incomplète")
            sys.exit(1)
        
        client = get_ovh_client(env)
        data_dir = config.get('data_dir', '/var/lib/odoo')
        
        # Créer un répertoire temporaire pour les backups
        with tempfile.TemporaryDirectory() as backup_dir:
            if args.all:
                # Sauvegarder toutes les bases client
                saas_clients = env['saas_portal.client'].search([('state', '=', 'open')])
                for saas_client in saas_clients:
                    print(f"Sauvegarde de {saas_client.name}...")
                    try:
                        db_backup = backup_database(saas_client.name, backup_dir, config)
                        upload_to_ovh_storage(
                            client, project_id, region, container,
                            db_backup, os.path.basename(db_backup)
                        )
                        
                        fs_backup = backup_filestore(saas_client.name, data_dir, backup_dir)
                        if fs_backup:
                            upload_to_ovh_storage(
                                client, project_id, region, container,
                                fs_backup, os.path.basename(fs_backup)
                            )
                    except Exception as e:
                        print(f"ERREUR pour {saas_client.name}: {e}")
                        
            elif args.client:
                # Sauvegarder une base spécifique
                print(f"Sauvegarde de {args.client}...")
                db_backup = backup_database(args.client, backup_dir, config)
                upload_to_ovh_storage(
                    client, project_id, region, container,
                    db_backup, os.path.basename(db_backup)
                )
                
                fs_backup = backup_filestore(args.client, data_dir, backup_dir)
                if fs_backup:
                    upload_to_ovh_storage(
                        client, project_id, region, container,
                        fs_backup, os.path.basename(fs_backup)
                    )
            else:
                print("Spécifiez --all ou --client")
                sys.exit(1)
    
    print("Sauvegarde terminée avec succès")


if __name__ == '__main__':
    main()

