from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    saas_s3_aws_accessid = fields.Char(
        string='AWS Access ID',
        config_parameter='saas_s3.saas_s3_aws_accessid',
        help='AWS Access ID for S3 storage'
    )
    
    saas_s3_aws_accesskey = fields.Char(
        string='AWS Secret Key',
        config_parameter='saas_s3.saas_s3_aws_accesskey',
        help='AWS Secret Key for S3 storage'
    )
    
    saas_s3_aws_bucket = fields.Char(
        string='S3 Bucket',
        config_parameter='saas_s3.saas_s3_aws_bucket',
        help='S3 Bucket name for storing backups'
    )
