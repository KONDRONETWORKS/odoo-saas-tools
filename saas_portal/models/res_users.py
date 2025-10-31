from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    support_team_id = fields.Many2one('saas_portal.support_team',
                                      'Support Team',
                                      help='Support team for SaaS')

    def __init__(self, env, ids=(), prefetch_ids=()):
        super(ResUsers, self).__init__(env, ids, prefetch_ids)
        # SELF_WRITEABLE_FIELDS n'est plus modifiable dans Odoo 18.0
        # Utiliser une approche différente pour ajouter support_team_id

    @api.model_create_multi
    def create(self, vals_list):
        # overridden to signup along with creation of db through saas backend wizard
        users = super(ResUsers, self).create(vals_list)
        if self.env.context.get('saas_signup'):
            for user in users:
                user.partner_id.signup_prepare()
        return users
