# -*- coding: utf-8 -*-
"""
Migration script pour supprimer l'ancien action_kondro_dashboard (ir.actions.act_window)
et permettre la création du nouveau (ir.actions.client)
"""

def migrate(cr, version):
    """Supprime l'ancien action_kondro_dashboard de type act_window"""
    # Rechercher l'ancien enregistrement par XML ID externe
    cr.execute("""
        DELETE FROM ir_actions_act_window
        WHERE id IN (
            SELECT res_id
            FROM ir_model_data
            WHERE module = 'kondro_core'
            AND name = 'action_kondro_dashboard'
            AND model = 'ir.actions.act_window'
        )
    """)
    
    # Supprimer aussi l'entrée dans ir_model_data si elle existe
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE module = 'kondro_core'
        AND name = 'action_kondro_dashboard'
        AND model = 'ir.actions.act_window'
    """)

