"""
Système de debugging amélioré pour le SaaS
Améliore le logging, la gestion des erreurs et le debugging
"""
import traceback
import functools
import json
from datetime import datetime
from odoo import http, _
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class DebugContext:
    """Contexte de debugging pour capturer les informations d'erreur"""
    
    def __init__(self, operation=None, user_id=None, partner_id=None, 
                 database=None, plan_id=None, **kwargs):
        self.operation = operation
        self.user_id = user_id
        self.partner_id = partner_id
        self.database = database
        self.plan_id = plan_id
        self.extra_data = kwargs
        self.start_time = datetime.now()
        self.errors = []
        
    def add_error(self, error, traceback_str=None):
        """Ajouter une erreur au contexte"""
        self.errors.append({
            'error': str(error),
            'traceback': traceback_str,
            'timestamp': datetime.now().isoformat()
        })
    
    def to_dict(self):
        """Convertir le contexte en dictionnaire"""
        return {
            'operation': self.operation,
            'user_id': self.user_id,
            'partner_id': self.partner_id,
            'database': self.database,
            'plan_id': self.plan_id,
            'extra_data': self.extra_data,
            'start_time': self.start_time.isoformat(),
            'duration': (datetime.now() - self.start_time).total_seconds(),
            'errors': self.errors
        }


def debug_log(operation_name=None, log_request=True, log_response=True):
    """
    Décorateur pour logger automatiquement les requêtes et réponses avec contexte
    
    Usage:
        @debug_log(operation_name="create_database", log_request=True, log_response=True)
        def create_database(self, **kwargs):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            
            # Créer le contexte de debug
            debug_ctx = DebugContext(
                operation=op_name,
                user_id=request.session.uid if hasattr(request, 'session') else None,
                partner_id=request.env.user.partner_id.id if hasattr(request, 'env') else None,
                **kwargs
            )
            
            # Logger la requête
            if log_request:
                _logger.info(
                    "🔍 [%s] START - Args: %s, Kwargs: %s",
                    op_name,
                    str(args)[:200],
                    json.dumps(kwargs, default=str)[:500] if kwargs else {}
                )
            
            try:
                # Exécuter la fonction
                result = func(*args, **kwargs)
                
                # Logger la réponse
                if log_response:
                    result_str = str(result)[:500] if result else "None"
                    _logger.info(
                        "✅ [%s] SUCCESS - Duration: %.2fs, Result: %s",
                        op_name,
                        debug_ctx.to_dict()['duration'],
                        result_str
                    )
                
                return result
                
            except Exception as e:
                # Capturer l'erreur avec traceback
                tb_str = traceback.format_exc()
                debug_ctx.add_error(e, tb_str)
                
                # Logger l'erreur avec contexte complet
                _logger.error(
                    "❌ [%s] ERROR - Duration: %.2fs\n"
                    "User: %s, Partner: %s, Database: %s\n"
                    "Error: %s\n"
                    "Traceback:\n%s\n"
                    "Context: %s",
                    op_name,
                    debug_ctx.to_dict()['duration'],
                    debug_ctx.user_id,
                    debug_ctx.partner_id,
                    debug_ctx.database,
                    str(e),
                    tb_str,
                    json.dumps(debug_ctx.to_dict(), indent=2, default=str)
                )
                
                # Enregistrer l'erreur dans la base de données si disponible
                if hasattr(request, 'env'):
                    try:
                        request.env['saas.error.log'].sudo().create({
                            'operation': op_name,
                            'error_message': str(e),
                            'traceback': tb_str,
                            'user_id': debug_ctx.user_id,
                            'partner_id': debug_ctx.partner_id,
                            'database': debug_ctx.database,
                            'context_data': json.dumps(debug_ctx.to_dict(), default=str),
                        })
                    except Exception:
                        # Si le modèle n'existe pas encore, juste logger
                        pass
                
                raise
                
        return wrapper
    return decorator


def safe_redirect(url, error_message=None, error_code=None, debug_info=None):
    """
    Fonction helper pour les redirections avec gestion d'erreur améliorée
    
    Args:
        url: URL de redirection
        error_message: Message d'erreur optionnel
        error_code: Code d'erreur optionnel
        debug_info: Informations de debug additionnelles
    
    Returns:
        werkzeug Response avec redirection
    """
    import werkzeug.utils
    
    if error_message or error_code:
        # Logger l'erreur avant redirection
        _logger.warning(
            "🔄 REDIRECT with ERROR - URL: %s, Message: %s, Code: %s, Debug: %s",
            url, error_message, error_code, debug_info
        )
        
        # Ajouter les paramètres d'erreur à l'URL si nécessaire
        if error_message and '?' not in url:
            params = {}
            if error_message:
                params['error'] = error_message[:100]  # Limiter la longueur
            if error_code:
                params['error_code'] = error_code
            if params:
                from urllib.parse import urlencode
                url = f"{url}?{urlencode(params)}"
    
    return werkzeug.utils.redirect(url)


def handle_exception(exception, context=None, redirect_url=None):
    """
    Gestion centralisée des exceptions avec logging amélioré
    
    Args:
        exception: L'exception levée
        context: Contexte DebugContext optionnel
        redirect_url: URL de redirection en cas d'erreur
    
    Returns:
        Response HTTP appropriée
    """
    import werkzeug.utils
    from odoo.addons.saas_base.exceptions import (
        MaximumDBException, MaximumTrialDBException, SuspendedDBException
    )
    
    # Construire les informations de contexte
    ctx_info = context.to_dict() if context else {}
    
    # Logger l'exception avec tous les détails
    _logger.error(
        "🚨 EXCEPTION HANDLED\n"
        "Type: %s\n"
        "Message: %s\n"
        "Traceback:\n%s\n"
        "Context: %s",
        type(exception).__name__,
        str(exception),
        traceback.format_exc(),
        json.dumps(ctx_info, indent=2, default=str)
    )
    
    # Gérer les exceptions spécifiques SaaS
    if isinstance(exception, MaximumDBException):
        url = redirect_url or request.env['ir.config_parameter'].sudo().get_param(
            'saas_portal.page_for_maximumdb', '/'
        )
        return safe_redirect(
            url,
            error_message=str(exception),
            error_code='MAX_DB_REACHED',
            debug_info=ctx_info
        )
    
    elif isinstance(exception, MaximumTrialDBException):
        url = redirect_url or request.env['ir.config_parameter'].sudo().get_param(
            'saas_portal.page_for_maximumtrialdb', '/'
        )
        return safe_redirect(
            url,
            error_message=str(exception),
            error_code='MAX_TRIAL_DB_REACHED',
            debug_info=ctx_info
        )
    
    elif isinstance(exception, SuspendedDBException):
        url = redirect_url or '/'
        return safe_redirect(
            url,
            error_message=str(exception),
            error_code='DB_SUSPENDED',
            debug_info=ctx_info
        )
    
    # Exception générique
    url = redirect_url or '/'
    return safe_redirect(
        url,
        error_message=_("Une erreur s'est produite. Veuillez contacter le support."),
        error_code='GENERIC_ERROR',
        debug_info=ctx_info
    )

