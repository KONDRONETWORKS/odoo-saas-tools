"""
Override ir.ui.view to map 'tree' → 'list' (Odoo 18 compatibility).
Optimized solution without browse() override.
"""
from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class IrUiView(models.Model):
    """Extended ir.ui.view model."""
    _inherit = 'ir.ui.view'
    
    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        """Override to intercept view_id before browse() to avoid browse('list')."""
        if isinstance(view_id, str):
            _logger.warning("_get_view: view_id is a string '%s', replacing with False", view_id)
            view_id = False
        
        if view_id is not None and not isinstance(view_id, (int, bool)) and view_id is not False:
            _logger.warning("_get_view: invalid view_id: %s (type: %s), replacing with False", view_id, type(view_id))
            view_id = False
        
        if view_type == 'tree':
            view_type = 'list'
        
        if view_id == 'list' or view_id == 'tree':
            _logger.warning("_get_view: view_id is '%s' (string), replacing with False", view_id)
            view_id = False
        
        try:
            return super()._get_view(view_id=view_id, view_type=view_type, **options)
        except Exception as e:
            from odoo.exceptions import UserError
            error_str = str(e).lower()
            
            # Handle "tree view not found" errors - retry with 'list'
            if isinstance(e, UserError) and 'tree' in error_str and ('vue' in error_str or 'view' in error_str):
                if view_type == 'tree':
                    _logger.warning("_get_view: tree view not found, retrying with 'list': %s", e)
                    try:
                        return super()._get_view(view_id=view_id, view_type='list', **options)
                    except Exception as list_error:
                        _logger.error("_get_view: error with 'list' view: %s", list_error)
                        raise
            
            # Handle singleton and other errors
            if 'singleton' in error_str or 'list' in error_str or 'invalid' in error_str:
                _logger.warning("_get_view: error detected: %s, retrying with view_id=False", e)
                try:
                    return super()._get_view(view_id=False, view_type=view_type, **options)
                except Exception as retry_error:
                    _logger.error("_get_view: error during retry: %s", retry_error)
                    raise
            raise
    
    def _get_combined_arch(self):
        """
        Override to handle cases where root might be a string instead of a recordset.
        Never access self.model directly when self might not be a singleton.
        """
        # Check if self is valid singleton BEFORE accessing any fields
        if not self or len(self) != 1:
            _logger.error("_get_combined_arch: self is not a singleton: %s", self)
            # Cannot access self.model safely, need to get model from context or options
            # Return arch directly if available, otherwise let parent handle it
            if hasattr(self, 'arch') and self.arch:
                return self.arch
            # Try to get model from _name if available
            model_name = getattr(self, '_name', None)
            if model_name and model_name != 'ir.ui.view':
                view_list = self.env['ir.ui.view'].search([
                    ('model', '=', model_name),
                    ('type', '=', 'list'),
                    ('active', '=', True)
                ], limit=1, order='priority desc, id desc')
                if view_list:
                    return view_list._get_combined_arch()
            # Fallback: let parent handle it, it will raise appropriate error
            return super()._get_combined_arch()
        
        # Check _ids BEFORE accessing self.model (which calls ensure_one())
        if hasattr(self, '_ids') and self._ids:
            if isinstance(self._ids, (list, tuple)) and len(self._ids) > 0:
                first_id = self._ids[0]
                if isinstance(first_id, str):
                    _logger.warning("_get_combined_arch: _ids contains string '%s', cannot use self.model", first_id)
                    # Get model name from _name or context, not from self.model
                    model_name = getattr(self, '_name', None)
                    if not model_name or model_name == 'ir.ui.view':
                        # Try to get from parent call stack or context
                        # For now, return arch if available
                        if hasattr(self, 'arch') and self.arch:
                            return self.arch
                        # Cannot recover, let parent handle
                        return super()._get_combined_arch()
                    view_list = self.env['ir.ui.view'].search([
                        ('model', '=', model_name),
                        ('type', '=', 'list'),
                        ('active', '=', True)
                    ], limit=1, order='priority desc, id desc')
                    if view_list:
                        return view_list._get_combined_arch()
                    if hasattr(self, 'arch') and self.arch:
                        return self.arch
        
        # Now safe to access self.model if self is a valid singleton
        try:
            return super()._get_combined_arch()
        except ValueError as e:
            error_msg = str(e).lower()
            if 'singleton' in error_msg and ('list' in error_msg or 'tree' in error_msg):
                _logger.warning("_get_combined_arch: singleton error detected: %s", e)
                try:
                    # Use _name instead of self.model to avoid ensure_one()
                    model_name = getattr(self, '_name', None)
                    if not model_name:
                        # Try to get model from arch if available
                        if hasattr(self, 'arch') and self.arch:
                            return self.arch
                        raise e
                    
                    # Search for list view
                    view_list = self.env['ir.ui.view'].search([
                        ('model', '=', model_name),
                        ('type', '=', 'list'),
                        ('active', '=', True)
                    ], limit=1, order='priority desc, id desc')
                    
                    if not view_list:
                        view_list = self.env['ir.ui.view'].search([
                            ('model', '=', model_name),
                            ('type', '=', 'list')
                        ], limit=1, order='priority desc, id desc')
                    
                    if view_list and len(view_list) == 1:
                        return view_list._get_combined_arch()
                    
                    # Last resort: return arch if available
                    if hasattr(self, 'arch') and self.arch:
                        return self.arch
                except Exception as recovery_error:
                    _logger.error("_get_combined_arch: error during recovery: %s", recovery_error)
                    # If we have arch, return it as last resort
                    if hasattr(self, 'arch') and self.arch:
                        return self.arch
                    raise e
            raise
    
    def default_view(self, model, view_type):
        """Map 'tree' → 'list' for view searches."""
        if view_type == 'tree':
            view_type = 'list'
        return super().default_view(model, view_type)
    
    @api.model
    def _get_default_view(self, view_type, res_model):
        """Map 'tree' → 'list' for default views."""
        if view_type == 'tree':
            view_type = 'list'
        return super()._get_default_view(view_type, res_model)
