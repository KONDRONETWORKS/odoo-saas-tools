# -*- coding: utf-8 -*-

from odoo import api, SUPERUSER_ID

def post_init_hook(env):
    """Set default theme parameters if they don't exist."""
    defaults = {
        'saas_portal.theme_bg_color_light': '#ffffff',
        'saas_portal.theme_bg_color_dark': '#1e1e2d',
        'saas_portal.theme_text_color_light': '#212529',
        'saas_portal.theme_text_color_dark': '#ffffff',
        'saas_portal.theme_button_radius': '4',
        'saas_portal.theme_card_radius': '8',
        'saas_portal.theme_input_radius': '4',
        'saas_portal.theme_font_size_base': '14',
        'saas_portal.theme_link_decoration': 'none',
    }
    
    for key, value in defaults.items():
        param = env['ir.config_parameter'].search([('key', '=', key)], limit=1)
        if not param:
            env['ir.config_parameter'].set_param(key, value)
