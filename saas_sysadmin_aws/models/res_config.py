from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    saas_route53_aws_accessid = fields.Char(
        string='AWS Access ID',
        config_parameter='saas_route53.saas_route53_aws_accessid',
        help='AWS Access ID for Route53 DNS management'
    )
    
    saas_route53_aws_accesskey = fields.Char(
        string='AWS Secret Key',
        config_parameter='saas_route53.saas_route53_aws_accesskey',
        help='AWS Secret Key for Route53 DNS management'
    )
