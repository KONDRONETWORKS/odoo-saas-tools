# -*- coding: utf-8 -*-
"""
Hooks pour le module kondro_core
"""

def pre_init_hook(cr):
    """
    Hook exécuté AVANT l'installation/mise à jour du module.
    Supprime l'ancien action_kondro_dashboard de type ir.actions.act_window
    pour permettre la création du nouveau de type ir.actions.client.
    """
    # Supprimer l'ancien enregistrement ir.actions.act_window
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
    
    # Supprimer l'entrée dans ir_model_data
    cr.execute("""
        DELETE FROM ir_model_data
        WHERE module = 'kondro_core'
        AND name = 'action_kondro_dashboard'
        AND model = 'ir.actions.act_window'
    """)

