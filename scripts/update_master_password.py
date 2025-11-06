#!/usr/bin/env python3
"""
Script pour mettre à jour le Master Password dans odoo.conf
"""
import configparser
import sys
import argparse
import os
import hashlib

def hash_password(password):
    """Hash le mot de passe au format Odoo (SHA-256)"""
    return hashlib.sha256(password.encode()).hexdigest()

def update_master_password(config_file, new_password, use_hash=False):
    """Met à jour le Master Password dans odoo.conf"""
    try:
        # Lire le fichier de configuration
        config = configparser.ConfigParser()
        config.read(config_file)
        
        if 'options' not in config:
            config.add_section('options')
        
        # Vérifier l'ancien mot de passe actuel
        current_password = config.get('options', 'admin_passwd', fallback=None)
        
        if current_password:
            print(f"📋 Master Password actuel dans {config_file}:")
            if len(current_password) == 64:  # Hash SHA-256
                print(f"   (hashé - longueur: {len(current_password)} caractères)")
            else:
                print(f"   (en clair: {current_password})")
        
        # Mettre à jour le mot de passe
        if use_hash:
            # Hasher le mot de passe
            hashed_password = hash_password(new_password)
            config.set('options', 'admin_passwd', hashed_password)
            print(f"✅ Master Password mis à jour (hashé) dans {config_file}")
        else:
            # Stocker en clair
            config.set('options', 'admin_passwd', new_password)
            print(f"✅ Master Password mis à jour (en clair) dans {config_file}")
        
        # Écrire le fichier
        with open(config_file, 'w') as f:
            config.write(f)
        
        print(f"💡 Nouveau Master Password: {new_password}")
        print(f"⚠️  Redémarrez Odoo pour que les changements prennent effet")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Fichier de configuration non trouvé: {config_file}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        import traceback
        traceback.print_exc()
        return False

def get_current_password(config_file):
    """Récupère le Master Password actuel"""
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        
        if 'options' not in config:
            return None
        
        password = config.get('options', 'admin_passwd', fallback=None)
        return password
        
    except Exception as e:
        print(f"❌ Erreur lors de la lecture: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mettre à jour le Master Password Odoo')
    parser.add_argument('new_password', help='Nouveau Master Password')
    parser.add_argument('--config', default='odoo.conf', help='Fichier de configuration (défaut: odoo.conf)')
    parser.add_argument('--hash', action='store_true', help='Hasher le mot de passe (SHA-256)')
    parser.add_argument('--show-current', action='store_true', help='Afficher le Master Password actuel')
    
    args = parser.parse_args()
    
    # Résoudre le chemin absolu
    config_file = os.path.abspath(args.config)
    
    if not os.path.exists(config_file):
        print(f"❌ Fichier de configuration non trouvé: {config_file}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔐 Mise à jour du Master Password Odoo")
    print("=" * 60)
    print()
    
    if args.show_current:
        current = get_current_password(config_file)
        if current:
            if len(current) == 64:
                print(f"📋 Master Password actuel: (hashé - {len(current)} caractères)")
            else:
                print(f"📋 Master Password actuel: {current}")
        else:
            print("📋 Aucun Master Password configuré")
        sys.exit(0)
    
    # Confirmation
    print(f"📝 Fichier de configuration: {config_file}")
    print(f"🔑 Nouveau Master Password: {args.new_password}")
    print()
    
    response = input("⚠️  Continuer ? (oui/non): ")
    if response.lower() not in ['oui', 'o', 'yes', 'y']:
        print("❌ Opération annulée")
        sys.exit(0)
    
    print()
    success = update_master_password(config_file, args.new_password, args.hash)
    
    if success:
        print()
        print("=" * 60)
        print("✅ Master Password mis à jour avec succès")
        print("=" * 60)
        print()
        print("📝 Prochaines étapes:")
        print("   1. Redémarrer Odoo pour appliquer les changements")
        print("   2. Utiliser le nouveau Master Password dans l'interface web")
        print()
        print("🔄 Pour redémarrer Odoo:")
        print("   docker compose -f config/docker-compose.simple.yml restart")
        sys.exit(0)
    else:
        print()
        print("=" * 60)
        print("❌ Échec de la mise à jour")
        print("=" * 60)
        sys.exit(1)

