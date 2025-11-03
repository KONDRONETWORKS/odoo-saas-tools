# -*- coding: utf-8 -*-

"""
Exceptions personnalisées pour le système SaaS
"""

from odoo import _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaasException(UserError):
    """Exception de base pour le système SaaS"""
    
    def __init__(self, message, user_message=None):
        self.user_message = user_message or message
        super().__init__(message)


class CapacityExceededException(SaasException):
    """Exception levée lorsque la capacité maximale est atteinte"""
    
    def __init__(self, message=None, user_message=None):
        super().__init__(
            message or "Maximum capacity exceeded",
            user_message or _("La capacité maximale a été atteinte. Veuillez contacter le support.")
        )


class SuspendedInstanceException(SaasException):
    """Exception levée lorsque l'instance est suspendue"""
    
    def __init__(self, message=None, user_message=None):
        super().__init__(
            message or "Instance suspended",
            user_message or _("Cette instance est actuellement suspendue. Veuillez contacter le support.")
        )


class ExpiredInstanceException(SaasException):
    """Exception levée lorsque l'instance a expiré"""
    
    def __init__(self, message=None, user_message=None):
        super().__init__(
            message or "Instance expired",
            user_message or _("Votre période d'essai a expiré. Veuillez passer à un plan payant.")
        )


class DatabaseCreationException(SaasException):
    """Exception levée lors de la création d'une base de données"""
    
    def __init__(self, message=None, user_message=None, details=None):
        super().__init__(
            message or "Database creation failed",
            user_message or _("La création de la base de données a échoué. Veuillez réessayer ou contacter le support.")
        )
        self.details = details or {}


class ServerConnectionException(SaasException):
    """Exception levée lors d'une erreur de connexion serveur"""
    
    def __init__(self, message=None, user_message=None):
        super().__init__(
            message or "Server connection error",
            user_message or _("Impossible de se connecter au serveur. Veuillez réessayer dans quelques instants.")
        )


class AuthenticationError(SaasException):
    """Exception levée lors d'une erreur d'authentification"""
    
    def __init__(self, message=None, user_message=None):
        super().__init__(
            message or "Authentication failed",
            user_message or _("Erreur d'authentification. Veuillez vérifier vos identifiants.")
        )


class InvalidConfigurationException(SaasException):
    """Exception levée lors d'une configuration invalide"""
    
    def __init__(self, message=None, user_message=None):
        super().__init__(
            message or "Invalid configuration",
            user_message or _("La configuration est invalide. Veuillez vérifier les paramètres.")
        )

