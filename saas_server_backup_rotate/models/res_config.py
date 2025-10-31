from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    backup_rotate_unlimited = fields.Boolean(
        string='Unlimited Backup',
        config_parameter='saas_server.backup_rotate_unlimited',
        help='Enable unlimited backups (disable rotation)',
        default=False
    )
    
    backup_rotate_yearly = fields.Integer(
        string='Yearly Count',
        config_parameter='saas_server.backup_rotate_yearly',
        help='Set the number of yearly backups to preserve during rotation',
        default=2
    )
    
    backup_rotate_monthly = fields.Integer(
        string='Monthly Count',
        config_parameter='saas_server.backup_rotate_monthly',
        help='Set the number of monthly backups to preserve during rotation',
        default=12
    )
    
    backup_rotate_weekly = fields.Integer(
        string='Weekly Count',
        config_parameter='saas_server.backup_rotate_weekly',
        help='Set the number of weekly backups to preserve during rotation',
        default=4
    )
    
    backup_rotate_daily = fields.Integer(
        string='Daily Count',
        config_parameter='saas_server.backup_rotate_daily',
        help='Set the number of daily backups to preserve during rotation',
        default=7
    )
    
    backup_rotate_hourly = fields.Integer(
        string='Hourly Count',
        config_parameter='saas_server.backup_rotate_hourly',
        help='Set the number of hourly backups to preserve during rotation',
        default=24
    )
