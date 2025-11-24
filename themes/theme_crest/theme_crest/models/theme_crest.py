
from odoo import api, models


class ThemeCrest(models.AbstractModel):
    _inherit = 'theme.utils'

    @api.model
    def _reset_default_config(self):

        self.disable_view('theme_crest.header_theme_crest_1')
        self.disable_view('theme_crest.header_theme_crest_2')
        self.disable_view('theme_crest.header_theme_crest_3')
        self.disable_view('theme_crest.header_theme_crest_4')
        self.disable_view('theme_crest.header_theme_crest_5')
        self.disable_view('theme_crest.header_theme_crest_6')
        self.disable_view('theme_crest.header_theme_crest_7')

        super(ThemeCrest, self)._reset_default_config()
