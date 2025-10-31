from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    saas_mailgun_api_key = fields.Char(
        string='Mailgun API Key',
        config_parameter='saas_mailgun.saas_mailgun_api_key',
        help='Mailgun API Key for sending emails'
    )
