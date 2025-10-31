from odoo import models, fields, api
from odoo.exceptions import UserError


class SaasPortalCategory(models.Model):

    def name_get(self):
        res = []
        for record in self:
            res.append((record.id, record.display_name))
        return res

    @api.depends('name', 'parent_id')
    def _name_get_fnc(self):
        for record in self:
            name = record.name
            if record.parent_id:
                name = record.parent_id.name + ' / ' + name
            record.display_name = name

    _name = "saas.portal.category"
    _description = "SaaS Client  Category"
    name = fields.Char(
        "Employee Tag",
        required=True
    )
    display_name = fields.Char(
        'Name',
        compute='_name_get_fnc',
        store=True,
        readonly=True
    )
    parent_id = fields.Many2one(
        'saas.portal.category',
        'Parent Employee Tag',
        index=True
    )
    child_ids = fields.One2many(
        'saas.portal.category',
        'parent_id',
        'Child Categories'
    )

    @api.constrains('parent_id')

    def _check_recursion(self):
        level = 100
        cr = self.env.cr
        ids = self.ids
        while len(ids):
            cr.execute('select distinct parent_id from saas_portal_category where id IN %s', (tuple(ids), ))
            ids = [_f for _f in [x[0] for x in cr.fetchall()] if _f]
            if not level:
                raise UserError('Error! You cannot create recursive Categories')
            level -= 1
        return True


class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'

    category_ids = fields.Many2many(
        'saas.portal.category',
        string='Tags'
    )

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('plan_id'):
                plan = self.env['saas_portal.plan'].browse(vals['plan_id'])
                vals['category_ids'] = [(6, 0, plan.category_ids.ids)]
        return super(SaasPortalClient, self).create(vals_list)


class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'

    category_ids = fields.Many2many(
        'saas.portal.category',
        string='Client Tags'
    )
