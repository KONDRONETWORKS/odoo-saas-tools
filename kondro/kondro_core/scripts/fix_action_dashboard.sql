-- Script SQL pour supprimer l'ancien action_kondro_dashboard (ir.actions.act_window)
-- À exécuter AVANT la mise à jour du module kondro_core
-- 
-- Usage: psql -d votre_base_de_donnees -f fix_action_dashboard.sql

-- Supprimer l'ancien enregistrement ir.actions.act_window
DELETE FROM ir_actions_act_window
WHERE id IN (
    SELECT res_id
    FROM ir_model_data
    WHERE module = 'kondro_core'
    AND name = 'action_kondro_dashboard'
    AND model = 'ir.actions.act_window'
);

-- Supprimer l'entrée dans ir_model_data
DELETE FROM ir_model_data
WHERE module = 'kondro_core'
AND name = 'action_kondro_dashboard'
AND model = 'ir.actions.act_window';


