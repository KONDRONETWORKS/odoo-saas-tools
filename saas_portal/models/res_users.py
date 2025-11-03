"""
Extended Res Users model for SaaS Portal.
"""
from odoo import api, fields, models


class ResUsers(models.Model):
    """Extended res.users model with support team field."""
    _inherit = 'res.users'

    support_team_id = fields.Many2one(
        'saas_portal.support_team',
        'Support Team',
        help='Support team for SaaS')

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to handle SaaS signup."""
        users = super().create(vals_list)
        if self.env.context.get('saas_signup'):
            for user in users:
                user.partner_id.signup_prepare()
        return users
