"""
Surcharge de ir.actions.act_window pour mapper 'tree' → 'list' dans view_mode
"""
from odoo import models, api


class IrActionsActWindow(models.Model):
    _inherit = 'ir.actions.act_window'
    
    def read(self, fields=None, load='_classic_read'):
        """Mappe 'tree' → 'list' dans view_mode lors de la lecture"""
        result = super().read(fields=fields, load=load)
        
        if isinstance(result, list):
            for record in result:
                if 'view_mode' in record and isinstance(record['view_mode'], str):
                    if 'tree' in record['view_mode']:
                        record['view_mode'] = record['view_mode'].replace('tree', 'list')
        
        return result
    
    @api.model
    def _for_xml_id(self, xml_id):
        """Mappe 'tree' → 'list' lors du chargement par XML ID"""
        action = super()._for_xml_id(xml_id)
        if action and 'view_mode' in action and isinstance(action['view_mode'], str):
            if 'tree' in action['view_mode']:
                action['view_mode'] = action['view_mode'].replace('tree', 'list')
        return action
