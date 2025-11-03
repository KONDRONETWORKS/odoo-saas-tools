"""
Override saas_portal.plan.get_views to map 'tree' → 'list' (Odoo 18 compatibility).
Minimal approach: only clean the result, don't modify the logic.
"""
from odoo import models, api
from odoo.exceptions import UserError
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
        # Normalize views parameter to handle 'tree' → 'list' mapping
        # This is critical for Odoo 18 which uses 'list' instead of 'tree'
        if views is not None:
            if isinstance(views, list):
                views = [
                    (view_id, 'list' if view_type == 'tree' else view_type)
                    for view_id, view_type in views
                ]
            elif isinstance(views, dict):
                # Handle dict format if used
                if 'tree' in views and 'list' not in views:
                    views['list'] = views['tree']
                if 'tree' in views:
                    del views['tree']
        
        # If views is None, Odoo will try to load default views
        # We need to ensure that when Odoo tries to load default 'tree' view,
        # it gets 'list' instead. This is handled in ir_ui_view._get_view()
        
        # Call parent first - don't modify anything
        try:
            result = super().get_views(views=views, options=options)
        except UserError as e:
            # Special handling for "tree view not found" errors
            error_msg = str(e).lower()
            if 'tree' in error_msg and ('vue' in error_msg or 'view' in error_msg):
                _logger.warning("get_views: tree view not found error: %s, trying with 'list' instead", e)
                # Try to get views with 'list' instead of 'tree'
                try:
                    # Normalize views to use 'list' instead of 'tree'
                    normalized_views = views
                    if views is not None and isinstance(views, list):
                        normalized_views = [
                            (view_id, 'list' if view_type == 'tree' else view_type)
                            for view_id, view_type in views
                        ]
                    # Retry with normalized views
                    result = super().get_views(views=normalized_views, options=options)
                    # Continue with normal processing
                except Exception as retry_error:
                    _logger.error("get_views: retry with 'list' also failed: %s", retry_error)
                    # Return minimal structure as last resort
                    return {
                        'fields': {},
                        'views': {},
                        'models': {},
                    }
            else:
                # Re-raise other UserError exceptions
                raise
        except Exception as e:
            _logger.error("get_views: error calling super().get_views: %s", e, exc_info=True, stack_info=True)
            # Return minimal valid structure only if parent fails
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        # CRITICAL: Ensure result is always a valid dict structure
        # Handle None, empty, or invalid results
        if result is None:
            _logger.warning("get_views: result is None, returning minimal structure")
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        if not result:
            _logger.warning("get_views: result is empty, returning minimal structure")
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        if not isinstance(result, dict):
            _logger.error("get_views: result is not a dict: %s (type: %s)", result, type(result))
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        # Ensure required keys exist (defensive) - CRITICAL for frontend
        if 'fields' not in result:
            result['fields'] = {}
        if 'views' not in result:
            result['views'] = {}
        if 'models' not in result:
            result['models'] = {}
        
        # Ensure values are dicts (defensive) - CRITICAL for frontend
        if result.get('fields') is None:
            result['fields'] = {}
        if result.get('views') is None:
            result['views'] = {}
        if result.get('models') is None:
            result['models'] = {}
        
        # Ensure values are proper dicts, not other types
        if not isinstance(result.get('fields'), dict):
            _logger.warning("get_views: fields is not a dict: %s, replacing with empty dict", type(result.get('fields')))
            result['fields'] = {}
        if not isinstance(result.get('views'), dict):
            _logger.warning("get_views: views is not a dict: %s, replacing with empty dict", type(result.get('views')))
            result['views'] = {}
        if not isinstance(result.get('models'), dict):
            _logger.warning("get_views: models is not a dict: %s, replacing with empty dict", type(result.get('models')))
            result['models'] = {}
        
        # ONLY clean 'tree' → 'list' mapping, nothing else
        if isinstance(result.get('views'), dict):
            views_dict = result['views']
            if 'tree' in views_dict and 'list' not in views_dict:
                views_dict['list'] = views_dict['tree']
            if 'tree' in views_dict:
                del views_dict['tree']
        
        # Final validation before return
        if not isinstance(result, dict) or 'fields' not in result or 'views' not in result or 'models' not in result:
            _logger.error("get_views: final validation failed, returning minimal structure")
            return {
                'fields': {},
                'views': {},
                'models': {},
            }
        
        return result
