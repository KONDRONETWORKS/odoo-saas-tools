"""
Exceptions personnalisées pour le SaaS avec messages utilisateur-friendly
"""
from odoo import _


class MaximumDBException(Exception):
    """Exception levée lorsqu'on atteint le maximum de bases de données"""
    
    def __init__(self, message=None, user_message=None):
        self.message = message or "Maximum number of databases reached"
        self.user_message = user_message or _(
            "Vous avez atteint le nombre maximum de bases de données autorisées. "
            "Veuillez supprimer une instance existante ou passer à un plan supérieur."
        )
        super().__init__(self.message)


class MaximumTrialDBException(Exception):
    """Exception levée lorsqu'on atteint le maximum de bases de données d'essai"""
    
    def __init__(self, message=None, user_message=None):
        self.message = message or "Maximum number of trial databases reached"
        self.user_message = user_message or _(
            "Vous avez atteint le nombre maximum de bases de données d'essai. "
            "Veuillez supprimer une instance d'essai existante ou passer à un plan payant."
        )
        super().__init__(self.message)


class SuspendedDBException(Exception):
    """Exception levée lorsqu'une base de données est suspendue"""
    
    def __init__(self, message=None, user_message=None):
        self.message = message or "Database is suspended"
        self.user_message = user_message or _(
            "Votre instance SaaS est actuellement suspendue. "
            "Veuillez renouveler votre abonnement pour réactiver l'accès."
        )
        super().__init__(self.message)


class DatabaseCreationException(Exception):
    """Exception levée lors de la création d'une base de données"""
    
    def __init__(self, message=None, user_message=None, details=None):
        self.message = message or "Failed to create database"
        self.user_message = user_message or _(
            "Impossible de créer votre instance SaaS. "
            "Veuillez réessayer dans quelques instants ou contacter le support si le problème persiste."
        )
        self.details = details or {}
        super().__init__(self.message)


class ServerConnectionException(Exception):
    """Exception levée lors d'une erreur de connexion au serveur"""
    
    def __init__(self, server_name, message=None, user_message=None):
        self.server_name = server_name
        self.message = message or f"Failed to connect to server: {server_name}"
        self.user_message = user_message or _(
            "Impossible de se connecter au serveur SaaS. "
            "Le serveur est peut-être temporairement indisponible. "
            "Veuillez réessayer dans quelques instants."
        )
        super().__init__(self.message)
