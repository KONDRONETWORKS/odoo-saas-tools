from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_sale_require_login = fields.Boolean(
        string='Require Login for Shop',
        help='Require users to be logged in to access the shop',
        config_parameter='website_sale.require_login',
        default=False,
    )

