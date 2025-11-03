"""
Override saas_portal.plan.get_views to map 'tree' → 'list' (Odoo 18 compatibility).
Minimal approach: only clean the result, don't modify the logic.
"""
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class SaasPortalPlan(models.Model):
    """Extended saas_portal.plan model."""
    _inherit = 'saas_portal.plan'
    
    @api.model
    def get_views(self, views=None, options=None):
        """
        Minimal override: just clean the result to map 'tree' → 'list'.
        Let parent handle all the logic.
        """
        # Call parent first - don't modify anything
        try:
            result = super().get_views(views=views, options=options)
        except Exception as e:
            _logger.error("get_views: error calling super().get_views: %s", e, exc_info=True)
            # Return minimal valid structure only if parent fails
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        # Only modify result if it's valid
        if not result:
            _logger.warning("get_views: result is empty, returning minimal structure")
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        if not isinstance(result, dict):
            _logger.error("get_views: result is not a dict: %s", type(result))
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        # Ensure required keys exist (defensive)
        if 'fields' not in result:
            result['fields'] = {}
        if 'views' not in result:
            result['views'] = {}
        if 'models' not in result:
            result['models'] = {}
        
        # Ensure values are dicts (defensive)
        if result.get('fields') is None:
            result['fields'] = {}
        if result.get('views') is None:
            result['views'] = {}
        if result.get('models') is None:
            result['models'] = {}
        
        if not isinstance(result.get('fields'), dict):
            result['fields'] = {}
        if not isinstance(result.get('views'), dict):
            result['views'] = {}
        if not isinstance(result.get('models'), dict):
            result['models'] = {}
        
        # ONLY clean 'tree' → 'list' mapping, nothing else
        if isinstance(result.get('views'), dict):
            views_dict = result['views']
            if 'tree' in views_dict and 'list' not in views_dict:
                views_dict['list'] = views_dict['tree']
            if 'tree' in views_dict:
                del views_dict['tree']
        
        return result
