from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Users(models.Model):
    _inherit = "res.users"

    access_right_ids = fields.One2many('ir.model.access', 'user_id')
    show_bot_access_rights_tab = fields.Boolean(string="Show Bot Access Rights Tab", compute='_compute_show_bot_access_rights_tab')

    def _compute_show_bot_access_rights_tab(self):
        for user in self:
            user.show_bot_access_rights_tab = self.env.ref('odoo_gpt_chat.group_bot_user') in user.groups_id
