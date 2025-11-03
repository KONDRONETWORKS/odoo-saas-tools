"""
Surcharge de ir.ui.view pour mapper 'tree' → 'list' (Odoo 18)
Solution optimisée sans surcharge de browse()
"""
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'
    
    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        """
        Surcharge CRITIQUE : Intercepte view_id AVANT browse() pour éviter browse('list')
        """
        # CORRECTION PRINCIPALE : Si view_id est une chaîne, le remplacer par False
        if isinstance(view_id, str):
            _logger.warning(f"_get_view: view_id est une chaîne '{view_id}', remplacement par False")
            view_id = False
        
        # Vérifier que view_id est valide (int, bool, False ou None uniquement)
        if view_id is not None and not isinstance(view_id, (int, bool)) and view_id is not False:
            _logger.warning(f"_get_view: view_id invalide: {view_id} (type: {type(view_id)}), remplacement par False")
            view_id = False
        
        # Mapper 'tree' → 'list' pour view_type
        if view_type == 'tree':
            view_type = 'list'
        
        # Protection supplémentaire : si view_id est "list" ou autre chaîne, le remplacer
        if view_id == 'list' or view_id == 'tree':
            _logger.warning(f"_get_view: view_id est '{view_id}' (chaîne), remplacement par False")
            view_id = False
        
        # Appeler la méthode parente avec les paramètres corrigés
        try:
            return super()._get_view(view_id=view_id, view_type=view_type, **options)
        except (ValueError, AttributeError, TypeError) as e:
            error_str = str(e).lower()
            if 'singleton' in error_str or 'list' in error_str or 'invalid' in error_str:
                _logger.warning(f"_get_view: erreur détectée: {e}, réessai avec view_id=False")
                try:
                    return super()._get_view(view_id=False, view_type=view_type, **options)
                except Exception as retry_error:
                    _logger.error(f"_get_view: erreur lors du réessai: {retry_error}")
                    raise
            raise
    
    def _get_combined_arch(self):
        """
        Surcharge supprimée - _get_view intercepte déjà les problèmes
        """
        # Déléguer complètement à la méthode parente
        # _get_view() intercepte déjà les chaînes invalides
        return super()._get_combined_arch()
    
    def default_view(self, model, view_type):
        """Mappe 'tree' → 'list' pour les recherches de vue par défaut"""
        if view_type == 'tree':
            view_type = 'list'
        return super().default_view(model, view_type)
    
    @api.model
    def _get_default_view(self, view_type, res_model):
        """Mappe 'tree' → 'list' pour les vues par défaut"""
        if view_type == 'tree':
            view_type = 'list'
        return super()._get_default_view(view_type, res_model)

