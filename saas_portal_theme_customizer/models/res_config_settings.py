# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Personnalisation des thèmes pour SaaS Portal"""
    _inherit = 'res.config.settings'

    # Couleurs principales
    theme_primary_color = fields.Char(
        string='Couleur Primaire',
        config_parameter='saas_portal.theme_primary_color',
        default='#714B67',
        help='Couleur principale utilisée dans la barre de navigation et les boutons'
    )
    
    theme_secondary_color = fields.Char(
        string='Couleur Secondaire',
        config_parameter='saas_portal.theme_secondary_color',
        default='#2D3142',
        help='Couleur secondaire utilisée dans les éléments complémentaires'
    )
    
    theme_accent_color = fields.Char(
        string='Couleur d\'Accent',
        config_parameter='saas_portal.theme_accent_color',
        default='#A53860',
        help='Couleur d\'accent pour les éléments importants'
    )
    
    # Image de fond
    theme_background_image = fields.Binary(
        string='Image de Fond',
        related='company_id.background_image',
        readonly=False,
        help='Image de fond pour l\'interface backend'
    )

    # Couleurs de Fond et Texte (Light/Dark)
    theme_bg_color_light = fields.Char(
        string='Fond (Mode Clair)',
        config_parameter='saas_portal.theme_bg_color_light',
        default='#ffffff',
        help='Couleur de fond pour le mode clair'
    )
    
    theme_bg_color_dark = fields.Char(
        string='Fond (Mode Sombre)',
        config_parameter='saas_portal.theme_bg_color_dark',
        default='#1e1e2d',
        help='Couleur de fond pour le mode sombre'
    )
    
    theme_text_color_light = fields.Char(
        string='Texte (Mode Clair)',
        config_parameter='saas_portal.theme_text_color_light',
        default='#212529',
        help='Couleur de texte pour le mode clair'
    )
    
    theme_text_color_dark = fields.Char(
        string='Texte (Mode Sombre)',
        config_parameter='saas_portal.theme_text_color_dark',
        default='#ffffff',
        help='Couleur de texte pour le mode sombre'
    )

    # UI Elements Customization
    theme_button_radius = fields.Integer(
        string='Rayon Bordure Boutons (px)',
        config_parameter='saas_portal.theme_button_radius',
        default=4,
        help='Arrondi des boutons'
    )
    
    theme_card_radius = fields.Integer(
        string='Rayon Bordure Cartes (px)',
        config_parameter='saas_portal.theme_card_radius',
        default=8,
        help='Arrondi des cartes et conteneurs'
    )
    
    theme_input_radius = fields.Integer(
        string='Rayon Bordure Champs (px)',
        config_parameter='saas_portal.theme_input_radius',
        default=4,
        help='Arrondi des champs de saisie'
    )
    
    theme_font_size_base = fields.Integer(
        string='Taille Police Base (px)',
        config_parameter='saas_portal.theme_font_size_base',
        default=14,
        help='Taille de la police de base'
    )
    
    theme_link_decoration = fields.Selection(
        [('none', 'Aucune'), ('underline', 'Souligné')],
        string='Décoration Liens',
        config_parameter='saas_portal.theme_link_decoration',
        default='none'
    )
    
    # Couleurs supplémentaires
    theme_success_color = fields.Char(
        string='Couleur Succès',
        config_parameter='saas_portal.theme_success_color',
        default='#28a745'
    )
    
    theme_warning_color = fields.Char(
        string='Couleur Avertissement',
        config_parameter='saas_portal.theme_warning_color',
        default='#ffc107'
    )
    
    theme_danger_color = fields.Char(
        string='Couleur Danger',
        config_parameter='saas_portal.theme_danger_color',
        default='#dc3545'
    )
    
    # Options de style
    theme_show_branding = fields.Boolean(
        string='Afficher le Badge SaaS Portal',
        config_parameter='saas_portal.theme_show_branding',
        default=True,
        help='Afficher l\'indicateur "🚀 SaaS Portal" dans la barre de navigation'
    )
    
    theme_show_top_bar = fields.Boolean(
        string='Afficher la Barre Supérieure Colorée',
        config_parameter='saas_portal.theme_show_top_bar',
        default=True,
        help='Afficher la barre colorée en haut de la page'
    )

