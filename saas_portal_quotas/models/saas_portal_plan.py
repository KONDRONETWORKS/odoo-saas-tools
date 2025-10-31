from odoo import models, fields, api


class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'

    # Quota Limits
    quota_max_users = fields.Integer(
        string='Maximum Users',
        default=0,
        help='Maximum number of users allowed (0 = unlimited)')
    
    quota_max_storage_mb = fields.Integer(
        string='Maximum Storage (MB)',
        default=0,
        help='Maximum storage in MB (0 = unlimited)')
    
    quota_max_api_calls_per_hour = fields.Integer(
        string='Max API Calls/Hour',
        default=0,
        help='Maximum API calls per hour (0 = unlimited)')
    
    quota_max_api_calls_per_day = fields.Integer(
        string='Max API Calls/Day',
        default=0,
        help='Maximum API calls per day (0 = unlimited)')
    
    quota_max_modules = fields.Integer(
        string='Maximum Modules',
        default=0,
        help='Maximum number of modules that can be installed (0 = unlimited)')
    
    quota_max_records_per_model = fields.Integer(
        string='Max Records per Model',
        default=0,
        help='Maximum records per model (0 = unlimited)')
    
    quota_bandwidth_mb_per_month = fields.Integer(
        string='Bandwidth per Month (MB)',
        default=0,
        help='Maximum bandwidth per month in MB (0 = unlimited)')

    # Quota Alert Settings
    quota_alert_percentage = fields.Integer(
        string='Alert at (%)',
        default=80,
        help='Send alert when quota reaches this percentage')
    
    quota_warning_percentage = fields.Integer(
        string='Warning at (%)',
        default=90,
        help='Show warning when quota reaches this percentage')
    
    quota_block_percentage = fields.Integer(
        string='Block at (%)',
        default=100,
        help='Block usage when quota reaches this percentage')
    
    quota_grace_period_days = fields.Integer(
        string='Grace Period (days)',
        default=3,
        help='Number of days after reaching limit before blocking')
    
    quota_auto_upgrade = fields.Boolean(
        string='Auto-upgrade on Limit',
        default=False,
        help='Automatically upgrade to next plan when limit reached')
    
    quota_upgrade_plan_id = fields.Many2one(
        'saas_portal.plan',
        string='Upgrade Plan',
        help='Plan to upgrade to when limit is reached')

    # Quota Enforcement Settings
    quota_enforce_users = fields.Boolean(
        string='Enforce User Limit',
        default=True,
        help='Block new user creation when limit reached')
    
    quota_enforce_storage = fields.Boolean(
        string='Enforce Storage Limit',
        default=True,
        help='Block operations when storage limit reached')
    
    quota_enforce_api = fields.Boolean(
        string='Enforce API Limits',
        default=True,
        help='Block API calls when limit reached')
    
    quota_enforce_modules = fields.Boolean(
        string='Enforce Module Limit',
        default=False,
        help='Block module installation when limit reached')

