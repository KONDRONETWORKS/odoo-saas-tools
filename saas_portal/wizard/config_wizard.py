import requests

from odoo import api, fields, models
from odoo.tools.translate import _


class SaasConfig(models.TransientModel):
    _name = 'saas.config'
    _description = 'SaaS Configuration'

    def _default_database_ids(self):
        return self._context.get('active_ids')

    action = fields.Selection([('edit', 'Edit'),
                               ('upgrade', 'Configure'),
                               ('delete', 'Delete')],
                              'Action')
    database_ids = fields.Many2many(
        'saas_portal.client', string='Database', default=_default_database_ids)
    update_addons_list = fields.Boolean('Update Addon List', default=True)
    update_addons = fields.Char('Update Addons')
    install_addons = fields.Char('Install Addons')
    uninstall_addons = fields.Char('Uninstall Addons')
    access_owner_add = fields.Char('Grant access to Owner')
    access_remove = fields.Char(
        'Restrict access',
        help='Restrict access for all users except super-user.\nNote, that ')
    fix_ids = fields.One2many('saas.config.fix', 'config_id', 'Fixes')
    limit_line_ids = fields.One2many(
        'saas.config.limit_number_of_records_line', 'config_id', 'Limit line')
    param_ids = fields.One2many('saas.config.param', 'config_id', 'Parameters')
    description = fields.Text('Result')

    def execute_action(self):
        res = False
        method = '%s_database' % self.action
        if hasattr(self, method):
            res = getattr(self, method)()
        return res

    def delete_database(self):
        return self.database_ids.delete_database()

    def upgrade_database(self):
        self.ensure_one()
        obj = self[0]
        payload = {
            # TODO: add configure mail server option here
            'update_addons_list': (obj.update_addons_list or ''),
            'update_addons': obj.update_addons.split(',') if obj.update_addons else [],
            'install_addons': obj.install_addons.split(',') if obj.install_addons else [],
            'uninstall_addons': obj.uninstall_addons.split(',') if obj.uninstall_addons else [],
            'access_owner_add': obj.access_owner_add.split(',') if obj.access_owner_add else [],
            'access_remove': obj.access_remove.split(',') if obj.access_remove else [],
            'fixes': [[x.model, x.method] for x in obj.fix_ids],
            'params': [{'key': x.key,
                        'value': x.value,
                        'hidden': x.hidden} for x in obj.param_ids],
            'limit_nuber_of_records': [{
                'model': x.model,
                'max_records': x.max_records,
                'domain': x.domain} for x in obj.limit_line_ids],
        }
        res = self.database_ids.upgrade(payload=payload)

        res_str = '\n\n'.join(res)
        obj.write({'description': res_str})
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'saas.config',
            'res_id': obj.id,
            'target': 'new'
        }

    @api.model
    def do_upgrade_database(self, payload, database_record):
        state = {
            'data': payload,
        }
        req, req_kwargs = database_record.server_id._request_server(
            path='/saas_server/upgrade_database',
            client_id=database_record.client_id,
            state=state,
        )
        res = requests.Session().send(req, **req_kwargs)
        if not res.ok:
            raise Warning(_('Reason: %s \n Message: %s') %
                          (res.reason, res.content))
        return res.text


class SaasConfigFix(models.TransientModel):
    _name = 'saas.config.fix'
    _description = 'SaaS Configuration Fix'

    model = fields.Char('Model', required=True)
    method = fields.Char('Method', required=True)
    config_id = fields.Many2one('saas.config', 'Config')


class SaasConfigLimitNumberOfRecords(models.TransientModel):
    _name = 'saas.config.limit_number_of_records_line'
    _description = 'SaaS Configuration Limit Number of Records'

    model = fields.Char('Model', required=True)
    domain = fields.Char('Domain', required=True, default='[]')
    max_records = fields.Integer(string='Maximum Records', required=True)
    config_id = fields.Many2one('saas.config', 'Config')


class SaasConfigParam(models.TransientModel):
    _name = 'saas.config.param'
    _description = 'SaaS Configuration Parameter'

    def _get_keys(self):
        return [
            # this parameter is obsolete.Use access_limit_records_number module
            ('saas_client.max_users', 'Max Users (obsolete)'),
            ('saas_client.suspended', 'Suspended'),
            ('saas_client.total_storage_limit', 'Total storage limit'),
        ]

    key = fields.Selection(selection=_get_keys,
                           string='Key', required=True)
    value = fields.Char('Value', required=True)
    config_id = fields.Many2one('saas.config', 'Config')
    hidden = fields.Boolean('Hidden parameter', default=True)


class SaasPortalCreateClient(models.TransientModel):
    _name = 'saas_portal.create_client'
    _description = 'SaaS Portal Create Client'

    def _default_plan_id(self):
        return self._context.get('active_id')

    def _default_name(self):
        plan_id = self._default_plan_id()
        if plan_id:
            plan = self.env['saas_portal.plan'].browse(plan_id)
            return plan.generate_dbname(raise_error=False)
        return ''

    name = fields.Char('Database name', required=True, default=_default_name)
    plan_id = fields.Many2one(
        'saas_portal.plan', string='Plan',
        readonly=True, default=_default_plan_id)
    partner_id = fields.Many2one('res.partner', string='Partner')
    user_id = fields.Many2one('res.users', string='User')
    notify_user = fields.Boolean(
        help='Notify user by email when database will have been created',
        default=True)
    support_team_id = fields.Many2one(
        'saas_portal.support_team', 'Support Team',
        default=lambda self: self.env.user.support_team_id)
    async_creation = fields.Boolean(
        'Asynchronous',
        default=False, help='Asynchronous creation of client base')
    trial = fields.Boolean('Trial')

    @api.onchange('user_id')
    def update_partner(self):
        if self.user_id:
            self.partner_id = self.user_id.partner_id

    def apply(self):
        self.ensure_one()
        plan_id = self.plan_id
        res = plan_id.create_new_database(
            dbname=self.name,
            partner_id=self.partner_id.id,
            user_id=self.user_id.id,
            notify_user=self.notify_user,
            support_team_id=self.support_team_id.id,
            async_mode=self.async_creation,
            trial=self.trial)
        if self.async_creation:
            return
        client = self.env['saas_portal.client'].browse(res.get('id'))
        client.server_id.action_sync_server()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'saas_portal.client',
            'res_id': client.id,
            'target': 'current',
        }


class SaasPortalDuplicateClient(models.TransientModel):
    _name = 'saas_portal.duplicate_client'
    _description = 'SaaS Portal Duplicate Client'

    def _default_client_id(self):
        return self._context.get('active_id')

    def _default_partner(self):
        client_id = self._default_client_id()
        if client_id:
            client = self.env['saas_portal.client'].browse(client_id)
            return client.partner_id
        return ''

    def _default_expiration(self):
        client_id = self._default_client_id()
        if client_id:
            client = self.env['saas_portal.client'].browse(client_id)
            return client.plan_id.expiration
        return ''

    def _default_target_server(self):
        client_id = self._default_client_id()
        if client_id:
            client = self.env['saas_portal.client'].browse(client_id)
            return client.server_id
        return ''

    name = fields.Char('Database Name', required=True)
    client_id = fields.Many2one(
        'saas_portal.client', string='Base Client',
        readonly=True, default=_default_client_id)
    expiration = fields.Integer('Expiration', default=_default_expiration)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', default=_default_partner)
    target_server = fields.Many2one(
        'saas_portal.server',
        string="Target server",
        default=_default_target_server
        )

    def apply(self):
        self.ensure_one()
        res = self.client_id.duplicate_database(
            dbname=self.name, partner_id=self.partner_id.id, expiration=None,
            target_server=self.target_server)
        client = self.env['saas_portal.client'].browse(res.get('id'))
        client.server_id.action_sync_server()
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'saas_portal.client',
            'res_id': client.id,
            'target': 'current',
        }


class SaasPortalRenameDatabase(models.TransientModel):
    _name = 'saas_portal.rename_database'
    _description = 'SaaS Portal Rename Database'

    def _default_client_id(self):
        return self._context.get('active_id')

    name = fields.Char('New Name', required=True)
    client_id = fields.Many2one(
        'saas_portal.client', string='Base Client',
        readonly=True, default=_default_client_id)

    def apply(self):
        self.ensure_one()
        self.client_id.rename_database(new_dbname=self.name)
        return {
            'type': 'ir.actions.act_window_close',
        }


class SaasPortalEditDatabase(models.TransientModel):
    _name = 'saas_portal.edit_database'
    _description = 'SaaS Portal Edit Database'

    name = fields.Char(readonly=True)
    active_id = fields.Char()
    active_model = fields.Char()
    edit_database_url = fields.Char(readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(SaasPortalEditDatabase, self).default_get(fields)
        print(('default_get', self._context))
        res['active_model'] = self._context.get('active_model')
        res['active_id'] = self._context.get('active_id')

        active_record = self.env[res['active_model']].browse(res['active_id'])
        if res['active_model'] == 'saas_portal.plan':
            active_record = active_record.template_id
        res['name'] = active_record.name
        res['edit_database_url'] = active_record._request_url(
            '/saas_server/edit_database')
        return res
