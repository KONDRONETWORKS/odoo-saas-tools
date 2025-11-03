"""
Override ir.actions.act_window to map 'tree' → 'list' in view_mode (Odoo 18 compatibility).
"""
from odoo import models, api


class IrActionsActWindow(models.Model):
    """Extended ir.actions.act_window model."""
    _inherit = 'ir.actions.act_window'
    
    def read(self, fields=None, load='_classic_read'):
        """Map 'tree' → 'list' in view_mode when reading."""
        result = super().read(fields=fields, load=load)
        
        if isinstance(result, list):
            for record in result:
                if 'view_mode' in record and isinstance(record['view_mode'], str):
                    if 'tree' in record['view_mode']:
                        record['view_mode'] = record['view_mode'].replace('tree', 'list')
        elif isinstance(result, dict):
            if 'view_mode' in result and isinstance(result['view_mode'], str):
                if 'tree' in result['view_mode']:
                    result['view_mode'] = result['view_mode'].replace('tree', 'list')
        
        return result
    
    @api.model
    def _for_xml_id(self, xml_id):
        """Map 'tree' → 'list' when loading by XML ID."""
        action = super()._for_xml_id(xml_id)
        if action and 'view_mode' in action and isinstance(action['view_mode'], str):
            if 'tree' in action['view_mode']:
                action['view_mode'] = action['view_mode'].replace('tree', 'list')
        return action
