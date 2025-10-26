# Copyright 2018 Ildar Nasyrov <https://www.itexperts4africa.com/team/iledarn>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Existing field
    module_saas_server_backup_ftp = fields.Boolean(
        string='Use SFTP Backup profile', 
        help='Use saas_server_backup_ftp module'
    )

    # New SaaS Server Configuration Fields
    saas_server_enable_backup = fields.Boolean(
        string='Enable Automated Backup',
        config_parameter='saas_server.enable_backup',
        help='Enable automated backup for client databases',
        default=False
    )
    
    saas_server_backup_frequency = fields.Integer(
        string='Backup Frequency (hours)',
        config_parameter='saas_server.backup_frequency',
        help='How often to backup client databases (in hours)',
        default=24
    )

    # Module enablement fields
    module_saas_server_backup_s3 = fields.Boolean(
        string='Use AWS S3 Backup',
        help='Enable AWS S3 backup storage (requires saas_server_backup_s3 module)'
    )

    module_saas_sysadmin_aws_route53 = fields.Boolean(
        string='Use AWS Route53 DNS',
        help='Enable AWS Route53 DNS management'
    )

    @api.model
    def set_values(self):
        """Save configuration values"""
        super(ResConfigSettings, self).set_values()
        # Additional custom logic can be added here if needed

    def get_values(self):
        """Load configuration values"""
        res = super(ResConfigSettings, self).get_values()
        # Load current values from config parameters
        return res
