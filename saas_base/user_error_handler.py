"""
Système de gestion d'erreurs amélioré pour les utilisateurs
- Messages d'erreur user-friendly et traduits
- Gestion centralisée des exceptions
- Boundaries pour les API
"""
from odoo import _, http
from odoo.http import request
from odoo.exceptions import UserError, ValidationError, AccessError
import logging
import traceback
import json

_logger = logging.getLogger(__name__)


class SaasUserFriendlyException(Exception):
    """Exception de base avec message utilisateur-friendly"""
    
    def __init__(self, message, user_message=None, error_code=None, details=None):
        """
        :param message: Message technique pour les logs
        :param user_message: Message traduit pour l'utilisateur
        :param error_code: Code d'erreur pour le frontend
        :param details: Détails supplémentaires (dict)
        """
        self.message = message
        self.user_message = user_message or message
        self.error_code = error_code or 'GENERIC_ERROR'
        self.details = details or {}
        super().__init__(self.message)


class DatabaseCreationError(SaasUserFriendlyException):
    """Erreur lors de la création d'une base de données"""
    
    def __init__(self, message, details=None):
        user_msg = _(
            "Impossible de créer votre instance SaaS. "
            "Veuillez réessayer dans quelques instants ou contacter le support si le problème persiste."
        )
        super().__init__(message, user_msg, 'DB_CREATION_ERROR', details)


class DatabaseNotFoundError(SaasUserFriendlyException):
    """Base de données non trouvée"""
    
    def __init__(self, db_name, details=None):
        message = f"Database not found: {db_name}"
        user_msg = _(
            "L'instance demandée est introuvable. "
            "Elle a peut-être été supprimée ou vous n'avez pas les permissions nécessaires."
        )
        super().__init__(message, user_msg, 'DB_NOT_FOUND', details)


class AuthenticationError(SaasUserFriendlyException):
    """Erreur d'authentification"""
    
    def __init__(self, message="Authentication failed", details=None):
        user_msg = _(
            "Erreur d'authentification. "
            "Veuillez vérifier vos identifiants et réessayer."
        )
        super().__init__(message, user_msg, 'AUTH_ERROR', details)


class PermissionError(SaasUserFriendlyException):
    """Erreur de permissions"""
    
    def __init__(self, message="Permission denied", details=None):
        user_msg = _(
            "Vous n'avez pas les permissions nécessaires pour effectuer cette action. "
            "Contactez votre administrateur si vous pensez qu'il s'agit d'une erreur."
        )
        super().__init__(message, user_msg, 'PERMISSION_ERROR', details)


class ServerConnectionError(SaasUserFriendlyException):
    """Erreur de connexion au serveur"""
    
    def __init__(self, server_name, details=None):
        message = f"Failed to connect to server: {server_name}"
        user_msg = _(
            "Impossible de se connecter au serveur SaaS. "
            "Le serveur est peut-être temporairement indisponible. "
            "Veuillez réessayer dans quelques instants."
        )
        super().__init__(message, user_msg, 'SERVER_CONNECTION_ERROR', details)


class QuotaExceededError(SaasUserFriendlyException):
    """Quota dépassé"""
    
    def __init__(self, quota_type, limit, details=None):
        message = f"Quota exceeded: {quota_type} (limit: {limit})"
        user_msg = _(
            "Vous avez atteint la limite de votre plan (%(quota_type)s). "
            "Veuillez passer à un plan supérieur ou contacter le support.",
            quota_type=quota_type
        )
        super().__init__(message, user_msg, 'QUOTA_EXCEEDED', details)


class DatabaseLimitExceededError(SaasUserFriendlyException):
    """Limite de bases de données atteinte"""
    
    def __init__(self, current, limit, details=None):
        message = f"Database limit exceeded: {current}/{limit}"
        user_msg = _(
            "Vous avez atteint la limite de bases de données (%(current)d/%(limit)d). "
            "Veuillez supprimer une instance existante ou passer à un plan supérieur.",
            current=current,
            limit=limit
        )
        super().__init__(message, user_msg, 'DB_LIMIT_EXCEEDED', details)


def handle_api_error(func):
    """
    Decorator pour gérer les erreurs dans les API avec messages user-friendly
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SaasUserFriendlyException as e:
            # Exception déjà user-friendly
            _logger.warning(
                "User-friendly error [%s]: %s",
                e.error_code,
                e.message
            )
            return request.make_response(
                json.dumps({
                    'error': True,
                    'error_code': e.error_code,
                    'message': e.user_message,
                    'details': e.details
                }),
                headers=[('Content-Type', 'application/json')],
                status=400
            )
        except (UserError, ValidationError) as e:
            # Exceptions Odoo standard
            _logger.warning("Odoo error: %s", str(e))
            return request.make_response(
                json.dumps({
                    'error': True,
                    'error_code': 'VALIDATION_ERROR',
                    'message': str(e),
                }),
                headers=[('Content-Type', 'application/json')],
                status=400
            )
        except AccessError as e:
            # Erreur de permissions
            _logger.warning("Access error: %s", str(e))
            return request.make_response(
                json.dumps({
                    'error': True,
                    'error_code': 'PERMISSION_ERROR',
                    'message': _("Vous n'avez pas les permissions nécessaires pour cette action."),
                }),
                headers=[('Content-Type', 'application/json')],
                status=403
            )
        except Exception as e:
            # Erreur générique
            _logger.exception("Unexpected error in %s: %s", func.__name__, str(e))
            return request.make_response(
                json.dumps({
                    'error': True,
                    'error_code': 'INTERNAL_ERROR',
                    'message': _(
                        "Une erreur inattendue s'est produite. "
                        "Notre équipe a été notifiée. Veuillez réessayer dans quelques instants."
                    ),
                }),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
    return wrapper


def handle_http_error(func):
    """
    Decorator pour gérer les erreurs dans les contrôleurs HTTP
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SaasUserFriendlyException as e:
            _logger.warning(
                "User-friendly error [%s]: %s",
                e.error_code,
                e.message
            )
            # Afficher le message d'erreur dans un template
            return request.render('saas_base.error_page', {
                'error_code': e.error_code,
                'error_message': e.user_message,
                'error_details': e.details,
            })
        except (UserError, ValidationError) as e:
            _logger.warning("Odoo error: %s", str(e))
            return request.render('saas_base.error_page', {
                'error_code': 'VALIDATION_ERROR',
                'error_message': str(e),
            })
        except AccessError as e:
            _logger.warning("Access error: %s", str(e))
            return request.render('saas_base.error_page', {
                'error_code': 'PERMISSION_ERROR',
                'error_message': _("Vous n'avez pas les permissions nécessaires pour cette action."),
            })
        except Exception as e:
            _logger.exception("Unexpected error in %s: %s", func.__name__, str(e))
            return request.render('saas_base.error_page', {
                'error_code': 'INTERNAL_ERROR',
                'error_message': _(
                    "Une erreur inattendue s'est produite. "
                    "Notre équipe a été notifiée. Veuillez réessayer dans quelques instants."
                ),
            })
    return wrapper


def format_error_response(error_code, message, details=None, status_code=400):
    """
    Formater une réponse d'erreur JSON standardisée
    """
    response_data = {
        'success': False,
        'error': {
            'code': error_code,
            'message': message,
        }
    }
    
    if details:
        response_data['error']['details'] = details
    
    return request.make_response(
        json.dumps(response_data, ensure_ascii=False),
        headers=[('Content-Type', 'application/json')],
        status=status_code
    )


def log_error_with_context(exception, context=None, user_id=None):
    """
    Logger une erreur avec contexte complet pour le debugging
    """
    context_dict = context.to_dict() if hasattr(context, 'to_dict') else (context or {})
    
    _logger.error(
        "🚨 ERROR [User: %s]\n"
        "Exception: %s\n"
        "Message: %s\n"
        "Traceback:\n%s\n"
        "Context: %s",
        user_id or 'Unknown',
        type(exception).__name__,
        str(exception),
        traceback.format_exc(),
        json.dumps(context_dict, indent=2, default=str)
    )
    
    # Enregistrer dans la table d'erreurs si disponible
    try:
        error_log = request.env.get('saas.error.log')
        if error_log:
            error_log.sudo().create({
                'operation': context_dict.get('operation', 'unknown'),
                'error_message': str(exception),
                'traceback': traceback.format_exc(),
                'user_id': user_id,
                'context_data': json.dumps(context_dict, default=str),
                'severity': 'high' if isinstance(exception, SaasUserFriendlyException) else 'medium',
            })
    except Exception:
        # Ne pas bloquer si l'enregistrement échoue
        pass

