"""
Surcharge de saas_portal.plan pour mapper 'tree' → 'list' (Odoo 18)
Solution simple et directe
"""
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'
    
    @api.model
    def get_views(self, views=None, options=None):
        """
        Normalise les formats de views et mappe 'tree' → 'list'
        """
        # Vérifier que views est bien une liste/tuple
        if views is not None and not isinstance(views, (list, tuple)):
            _logger.warning(f"get_views: views n'est pas une liste/tuple: {type(views)}")
            views = None
        
        # Normaliser les views
        if views:
            normalized_views = []
            for item in views:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    first, second = item[0], item[1]
                    
                    # Détecter le format: (id, type) ou (type, id)
                    if isinstance(first, (int, bool)) or first is False:
                        if isinstance(second, str):
                            view_id, view_type = first, second  # Format: (id, type)
                        else:
                            continue  # Format invalide
                    elif isinstance(first, str):
                        view_type, view_id = first, second  # Format: (type, id)
                    else:
                        continue  # Format invalide
                    
                    # Vérifier que view_type est une chaîne
                    if not isinstance(view_type, str):
                        continue
                    
                    # CORRECTION CRITIQUE : Si view_id est une chaîne, le remplacer par False
                    if isinstance(view_id, str):
                        _logger.warning(f"get_views: view_id est une chaîne '{view_id}', remplacement par False")
                        view_id = False
                    
                    # Protection supplémentaire : si view_id est "list" ou "tree", le remplacer
                    if view_id in ('list', 'tree'):
                        _logger.warning(f"get_views: view_id est '{view_id}' (chaîne), remplacement par False")
                        view_id = False
                    
                    # Vérifier que view_id est valide (int, bool, False ou None uniquement)
                    if view_id is not None and not isinstance(view_id, (int, bool)) and view_id is not False:
                        _logger.warning(f"get_views: view_id invalide: {view_id} (type: {type(view_id)}), remplacement par False")
                        view_id = False
                    
                    # Mapper 'tree' → 'list'
                    if view_type == 'tree':
                        view_type = 'list'
                    
                    # Format attendu par Odoo: (type, id)
                    # S'assurer que view_id n'est jamais une chaîne
                    if isinstance(view_id, str):
                        view_id = False
                    
                    normalized_views.append((view_type, view_id))
            
            views = normalized_views if normalized_views else None
        
        # Appeler la méthode parente directement sans recherche récursive
        result = super().get_views(views=views, options=options)
        
        # Nettoyer le résultat : supprimer 'tree' si présent
        if result and 'views' in result:
            views_dict = result['views']
            if 'tree' in views_dict:
                if 'list' not in views_dict:
                    views_dict['list'] = views_dict['tree']
                del views_dict['tree']
        
        return result

