# -*- coding: utf-8 -*-

"""
Utilitaires et fonctions communes pour le système SaaS
"""

import uuid
import secrets
import string
from datetime import datetime, timedelta
from odoo import api, models, tools
import logging

_logger = logging.getLogger(__name__)


def generate_unique_id():
    """Générer un ID unique"""
    return str(uuid.uuid4())


def generate_client_secret(length=32):
    """Générer un secret client sécurisé"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_subdomain():
    """Générer un sous-domaine unique"""
    return f"{generate_unique_id()[:8]}"


def calculate_expiration(hours=None, days=None, months=None, years=None):
    """
    Calculer une date d'expiration
    
    Args:
        hours: Nombre d'heures
        days: Nombre de jours
        months: Nombre de mois
        years: Nombre d'années
    
    Returns:
        datetime: Date d'expiration
    """
    now = datetime.now()
    
    if years:
        delta = timedelta(days=years * 365)
    elif months:
        delta = timedelta(days=months * 30)
    elif days:
        delta = timedelta(days=days)
    elif hours:
        delta = timedelta(hours=hours)
    else:
        delta = timedelta(days=30)  # Default: 30 days
    
    return now + delta


def validate_domain(domain):
    """
    Valider un nom de domaine
    
    Args:
        domain: Nom de domaine à valider
    
    Returns:
        bool: True si valide
    """
    import re
    
    pattern = r'^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?)*$'
    return bool(re.match(pattern, domain.lower()))


def log_action(action, model, record_id, user_id=None, details=None):
    """
    Logger une action pour audit trail
    
    Args:
        action: Action effectuée
        model: Modèle concerné
        record_id: ID de l'enregistrement
        user_id: ID utilisateur
        details: Détails additionnels
    """
    user_id = user_id or 1
    _logger.info(
        f"AUDIT: {action} on {model} (ID: {record_id}) by user {user_id} - {details or ''}"
    )


def safe_call(func, *args, **kwargs):
    """
    Appeler une fonction avec gestion d'erreurs sécurisée
    
    Args:
        func: Fonction à appeler
        *args: Arguments positionnels
        **kwargs: Arguments nommés
    
    Returns:
        tuple: (success, result, error_message)
    """
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except Exception as e:
        _logger.error(f"Error in safe_call: {e}")
        return False, None, str(e)


class SaasTools(models.AbstractModel):
    """Utilitaires SaaS accessibles via Odoo ORM"""
    _name = 'saas.tools'
    _description = 'SaaS Tools'
    
    def generate_dbname(self, prefix='saas', length=8):
        """Générer un nom de base de données unique"""
        unique_part = generate_unique_id()[:length].replace('-', '')
        return f"{prefix}_{unique_part}"
    
    def validate_email(self, email):
        """Valider une adresse email"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def format_storage(self, bytes_value):
        """Formater une taille de stockage"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"

