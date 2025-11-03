"""
SaaS Portal Models
==================

Modèles principaux pour la gestion du portail SaaS.
"""
import simplejson
import werkzeug
import werkzeug.urls
import requests
import random
import logging
from datetime import datetime, timedelta

from odoo import api, exceptions, fields, models
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

from odoo.addons.saas_base.exceptions import MaximumTrialDBException
from odoo.addons.saas_base.exceptions import MaximumDBException
from werkzeug.exceptions import Forbidden

_logger = logging.getLogger(__name__)


def _tz_get(env):
    """Get timezone list for Odoo 18.0 compatibility."""
    import pytz
    return [(tz, tz) for tz in pytz.all_timezones]


def _compute_host(self):
    """Compute host name for server/database."""
    base_saas_domain = self.env['ir.config_parameter'].sudo().get_param('saas_portal.base_saas_domain')
    for r in self:
        host = r.name
        if base_saas_domain and '.' not in r.name:
            host = '%s.%s' % (r.name, base_saas_domain)
        r.host = host


class SaasPortalServer(models.Model):
    """SaaS Server - Représente un serveur SaaS."""
    _name = 'saas_portal.server'
    _description = 'SaaS Server'
    _rec_name = 'name'
    _inherit = ['mail.thread']
    _inherits = {'oauth.application': 'oauth_application_id'}

    name = fields.Char('Database name', required=True)
    oauth_application_id = fields.Many2one(
        'oauth.application', 'OAuth Application', required=True, ondelete='cascade')
    sequence = fields.Integer('Sequence')
    active = fields.Boolean('Active', default=True)
    request_scheme = fields.Selection(
        [('http', 'http'), ('https', 'https')], 'Scheme', default='http', required=True)
    verify_ssl = fields.Boolean(
        'Verify SSL', default=True,
        help="verify SSL certificates for server-side HTTPS requests, just like a web browser")
    request_port = fields.Integer('Request Port', default=80)
    client_ids = fields.One2many('saas_portal.client', 'server_id', string='Clients')
    local_host = fields.Char('Local host', help='local host or ip address of server for server-side requests')
    local_port = fields.Char('Local port', help='local tcp port of server for server-side requests')
    local_request_scheme = fields.Selection(
        [('http', 'http'), ('https', 'https')], 'Scheme', default='http', required=True)
    host = fields.Char('Host', compute=_compute_host)
    odoo_version = fields.Char('Odoo version', readonly=True)
    password = fields.Char()
    clients_host_template = fields.Char(
        'Template for clients host names',
        help='The possible dynamic parts of the host names are: {dbname}, {base_saas_domain}, {base_saas_domain_1}')

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to automatically create OAuth application if needed."""
        for vals in vals_list:
            if 'oauth_application_id' not in vals or not vals.get('oauth_application_id'):
                oauth_app = self.env['oauth.application'].sudo().create({})
                vals['oauth_application_id'] = oauth_app.id

        records = super().create(vals_list)
        for record in records:
            record.oauth_application_id._get_access_token(create=True)
        return records

    def _request_params(self, path='/web', scheme=None, port=None, state=None, scope=None, client_id=None):
        """Build request parameters for OAuth requests."""
        self.ensure_one()
        if not state:
            state = {}
        scheme = scheme or self.request_scheme
        port = port or self.request_port
        scope = scope or ['userinfo', 'force_login', 'trial', 'skiptheuse']
        scope = ' '.join(scope)
        client_id = client_id or self.env['oauth.application'].generate_client_id()
        params = {
            'scope': scope,
            'state': simplejson.dumps(state),
            'redirect_uri': '{scheme}://{saas_server}:{port}{path}'.format(
                scheme=scheme, port=port, saas_server=self.host, path=path),
            'response_type': 'token',
            'client_id': client_id,
        }
        return params

    def _request(self, **kwargs):
        """Generate OAuth authorization URL."""
        self.ensure_one()
        params = self._request_params(**kwargs)
        url = '/oauth2/auth?%s' % werkzeug.urls.url_encode(params)
        return url

    def _request_server(self, path=None, scheme=None, port=None, **kwargs):
        """Prepare server-side request with OAuth token."""
        self.ensure_one()
        scheme = scheme or self.local_request_scheme or self.request_scheme
        host = self.local_host or self.host
        port = port or self.local_port or self.request_port
        params = self._request_params(**kwargs)
        access_token = self.oauth_application_id.sudo()._get_access_token(create=True)
        params.update({
            'token_type': 'Bearer',
            'access_token': access_token,
            'expires_in': 3600,
        })
        url = '{scheme}://{host}:{port}{path}'.format(
            scheme=scheme, host=host, port=port, path=path)
        req = requests.Request('GET', url, data=params, headers={'host': self.host})
        req_kwargs = {'verify': self.verify_ssl}
        return req.prepare(), req_kwargs

    def action_redirect_to_server(self):
        """Action to redirect to server web interface."""
        r = self[0]
        url = '{scheme}://{saas_server}:{port}{path}'.format(
            scheme=r.request_scheme, saas_server=r.host, port=r.request_port, path='/web')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'name': 'Redirection',
            'url': url
        }

    @api.model
    def action_sync_server_all(self):
        """Sync all servers and monitor storage."""
        self.search([]).action_sync_server()
        self.env['saas_portal.client'].search([]).storage_usage_monitoring()

    def action_sync_server(self, updating_client_ID=None):
        """Synchronize server with remote SaaS server."""
        for server in self:
            state = {
                'd': server.name,
                'client_id': server.client_id,
                'updating_client_ID': updating_client_ID,
            }
            req, req_kwargs = server._request_server(
                path='/saas_server/sync_server', state=state, client_id=server.client_id)
            res = requests.Session().send(req, **req_kwargs)

            if not res.ok:
                raise exceptions.Warning(_('Reason: %s \n Message: %s') % (res.reason, res.content))
            try:
                data = simplejson.loads(res.text)
            except Exception as e:
                _logger.error('Error on parsing response: %s\n%s', [req.url, req.headers, req.body], res.text)
                raise
            for r in data:
                r['server_id'] = server.id
                client = server.env['saas_portal.client'].with_context(active_test=False).search([
                    ('client_id', '=', r.get('client_id'))
                ])
                if not client:
                    database = server.env['saas_portal.database'].search([
                        ('client_id', '=', r.get('client_id'))
                    ])
                    if database:
                        database.write(r)
                        continue
                    client = server.env['saas_portal.client'].create(r)
                else:
                    client.write(r)
        return None

    @api.model
    def get_saas_server(self):
        """Get a random active SaaS server."""
        saas_server_list = self.sudo().search([('active', '=', True)])
        if not saas_server_list:
            return self.browse()
        return saas_server_list[random.randint(0, len(saas_server_list) - 1)]


class SaasPortalPlan(models.Model):
    """SaaS Plan - Définit un plan d'abonnement SaaS."""
    _name = 'saas_portal.plan'
    _description = 'SaaS Portal Plan'
    _order = 'sequence'

    def _register_hook(self):
        """Ensure list view exists for Odoo 18 compatibility."""
        super()._register_hook()
        view = self.env['ir.ui.view'].sudo().search([
            ('model', '=', 'saas_portal.plan'),
            ('type', '=', 'list'),
            ('name', '=', 'saas_portal.plans.list')
        ], limit=1)
        if not view:
            self.env['ir.ui.view'].sudo().create({
                'name': 'saas_portal.plans.list',
                'model': 'saas_portal.plan',
                'type': 'list',
                'priority': 1,
                'active': True,
                'arch': '''<?xml version="1.0"?>
<list string="Plans">
    <field name="sequence" invisible="1"/>
    <field name="name"/>
    <field name="template_id"/>
    <field name="state"/>
</list>'''
            })

    name = fields.Char('Plan', required=True)
    summary = fields.Char('Summary')
    template_id = fields.Many2one('saas_portal.database', 'Template', ondelete='restrict')
    demo = fields.Boolean('Install Demo Data')
    maximum_allowed_dbs_per_partner = fields.Integer(
        'Maximum Allowed DBs per Partner',
        help='maximum allowed non-trial databases per customer', required=True, default=0)
    maximum_allowed_trial_dbs_per_partner = fields.Integer(
        'Maximum Allowed Trial DBs per Partner',
        help='maximum allowed trial databases per customer', required=True, default=0)
    max_users = fields.Char('Initial Max users', default='0', help='leave 0 for no limit')
    total_storage_limit = fields.Integer('Total storage limit (MB)', help='leave 0 for no limit')
    block_on_expiration = fields.Boolean('Block clients on expiration', default=False)
    block_on_storage_exceed = fields.Boolean('Block clients on storage exceed', default=False)

    def _get_default_lang(self):
        """Get default language from user preferences."""
        return self.env.user.lang

    def _default_tz(self):
        """Get default timezone from user preferences."""
        return self.env.user.tz

    lang = fields.Selection([
        ('en_US', 'English'),
        ('fr_FR', 'French'),
        ('es_ES', 'Spanish'),
        ('de_DE', 'German')
    ], 'Language', default=_get_default_lang)
    tz = fields.Selection(selection=_tz_get, string='TimeZone', default=_default_tz)
    sequence = fields.Integer('Sequence')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed')],
        'State', compute='_compute_get_state', store=True)
    expiration = fields.Integer('Expiration (hours)', help='time to delete database. Use for demo')
    grace_period = fields.Integer('Grace period (days)', help='initial days before expiration')
    dbname_template = fields.Char(
        'DB Names',
        help='Used for generating client database domain name. Use %i for numbering. Ignore if you use manually created db names')
    server_id = fields.Many2one(
        'saas_portal.server',
        string='SaaS Server',
        ondelete='restrict',
        help='Use this saas server or choose random')
    website_description = fields.Html('Website description')
    logo = fields.Binary('Logo')
    on_create = fields.Selection([
        ('login', 'Log into just created instance'),
    ], string="Workflow on create", default='login')
    on_create_email_template = fields.Many2one(
        'mail.template',
        default=lambda self: self.env.ref('saas_portal.email_template_create_saas', raise_if_not_found=False))

    @api.depends('template_id.state')
    def _compute_get_state(self):
        """Compute plan state based on template state."""
        for plan in self:
            plan.state = 'confirmed' if plan.template_id.state == 'template' else 'draft'

    def _new_database_vals(self, vals):
        """Add plan-specific values to database creation values."""
        self.ensure_one()
        vals.setdefault('max_users', self.max_users)
        vals.setdefault('total_storage_limit', self.total_storage_limit)
        vals.setdefault('block_on_expiration', self.block_on_expiration)
        vals.setdefault('block_on_storage_exceed', self.block_on_storage_exceed)
        return vals

    def _prepare_owner_user_data(self, user_id):
        """
        Prepare the dict of values to update owner user data in client instance.
        This method may be overridden to implement custom values.
        """
        self.ensure_one()
        owner_user = self.env['res.users'].browse(user_id) or self.env.user
        return {
            'user_id': owner_user.id,
            'login': owner_user.login,
            'name': owner_user.name,
            'email': owner_user.email,
            'password_crypt': owner_user.password_crypt,
        }

    def _get_expiration(self, trial):
        """Calculate expiration datetime based on trial status."""
        self.ensure_one()
        if trial and self.expiration:
            expiration_dt = datetime.now() + timedelta(hours=self.expiration)
            return expiration_dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)

    def create_new_database(self, **kwargs):
        """Public method to create new database."""
        return self._create_new_database(**kwargs)

    def _create_new_database(self, dbname=None, client_id=None, partner_id=None,
                             user_id=None, notify_user=True, trial=False,
                             support_team_id=None, async_mode=None):
        """Create a new client database."""
        self.ensure_one()
        p_client = self.env['saas_portal.client']
        p_server = self.env['saas_portal.server']
        server = self.server_id or p_server.get_saas_server()

        if not partner_id and user_id:
            user = self.env['res.users'].browse(user_id)
            partner_id = user.partner_id.id

        # Check database limits
        if not trial and self.maximum_allowed_dbs_per_partner != 0:
            db_count = p_client.search_count([
                ('partner_id', '=', partner_id),
                ('state', '=', 'open'),
                ('plan_id', '=', self.id),
                ('trial', '=', False)
            ])
            if db_count >= self.maximum_allowed_dbs_per_partner:
                raise MaximumDBException(
                    "Limit of databases for this plan is %(maximum)s reached" % {
                        'maximum': self.maximum_allowed_dbs_per_partner})

        if trial and self.maximum_allowed_trial_dbs_per_partner != 0:
            trial_db_count = p_client.search_count([
                ('partner_id', '=', partner_id),
                ('state', '=', 'open'),
                ('plan_id', '=', self.id),
                ('trial', '=', True)
            ])
            if trial_db_count >= self.maximum_allowed_trial_dbs_per_partner:
                raise MaximumTrialDBException(
                    "Limit of trial databases for this plan is %(maximum)s reached" % {
                        'maximum': self.maximum_allowed_trial_dbs_per_partner})

        client_expiration = self._get_expiration(trial)
        vals = {
            'name': dbname or self.generate_dbname(),
            'server_id': server.id,
            'plan_id': self.id,
            'partner_id': partner_id,
            'trial': trial,
            'support_team_id': support_team_id,
            'expiration_datetime': client_expiration,
        }
        client = None
        if client_id:
            vals['client_id'] = client_id
            client = p_client.search([('client_id', '=', client_id)])

        vals = self._new_database_vals(vals)

        if client:
            client.write(vals)
        else:
            client = p_client.create(vals)
        client_id = client.client_id

        owner_user_data = self._prepare_owner_user_data(user_id)

        state = {
            'd': client.name,
            'public_url': client.public_url,
            'e': client_expiration,
            'r': client.public_url + 'web',
            'h': client.host,
            'owner_user': owner_user_data,
            't': client.trial,
        }
        if self.template_id:
            state['db_template'] = self.template_id.name

        req, req_kwargs = server._request_server(
            path='/saas_server/new_database',
            state=state,
            client_id=client_id,
            scope=['userinfo', 'force_login', 'trial', 'skiptheuse'],
        )
        res = requests.Session().send(req, **req_kwargs)
        if res.status_code != 200:
            raise exceptions.Warning(_('Error on request: %s\nReason: %s \n Message: %s') % (
                req.url, res.reason, res.content))
        data = simplejson.loads(res.text)
        params = {
            'state': data.get('state'),
            'access_token': client.oauth_application_id._get_access_token(user_id, create=True),
        }
        url = '{url}?{params}'.format(url=data.get('url'), params=werkzeug.urls.url_encode(params))
        auth_url = url

        # Send email notification if template exists
        template = self.on_create_email_template
        if template and notify_user:
            user = self.env['res.users'].browse(user_id)
            client.with_context(user=user).message_post_with_template(
                template.id, composition_mode='comment')

        client.send_params_to_client_db()
        client.sync_client()

        return {
            'url': url,
            'id': client.id,
            'client_id': client_id,
            'auth_url': auth_url
        }

    def generate_dbname(self, raise_error=True):
        """Generate database name from template."""
        self.ensure_one()
        if not self.dbname_template:
            if raise_error:
                raise exceptions.Warning(_('Template for db name is not configured'))
            return ''
        sequence = self.env['ir.sequence'].get('saas_portal.plan')
        return self.dbname_template.replace('%i', sequence)

    def create_template_button(self):
        """Button action to create template."""
        return self.create_template()

    def create_template(self, addons=None):
        """Create template database from plan."""
        self.ensure_one()
        server = self.server_id or self.env['saas_portal.server'].get_saas_server()

        state = {
            'd': self.template_id.name,
            'demo': self.demo and 1 or 0,
            'addons': addons or [],
            'lang': self.lang,
            'tz': self.tz,
            'is_template_db': 1,
        }
        client_id = self.template_id.client_id
        self.template_id.server_id = server

        req, req_kwargs = server._request_server(
            path='/saas_server/new_database', state=state, client_id=client_id)
        res = requests.Session().send(req, **req_kwargs)

        if not res.ok:
            raise exceptions.Warning(_('Error on request: %s\nReason: %s \n Message: %s') %
                          (req.url, res.reason, res.content))
        try:
            data = simplejson.loads(res.text)
        except Exception as e:
            _logger.error('Error on parsing response: %s\n%s', [req.url, req.headers, req.body], res.text)
            raise

        self.template_id.password = data.get('superuser_password')
        self.template_id.state = data.get('state')
        return data

    def action_sync_server(self):
        """Sync server for this plan."""
        for plan in self:
            if plan.server_id:
                plan.server_id.action_sync_server()
        return True

    def edit_template(self):
        """Edit template database."""
        return self[0].template_id.edit_database()

    def upgrade_template(self):
        """Show upgrade wizard for template."""
        return self[0].template_id.show_upgrade_wizard()

    def delete_template(self):
        """Delete template database."""
        self.ensure_one()
        return self.template_id.delete_database_server()


class OauthApplication(models.Model):
    """Extended OAuth Application model."""
    _inherit = 'oauth.application'

    client_id = fields.Char('Database UUID')
    last_connection = fields.Char(
        compute='_compute_get_last_connection',
        string='Last Connection', size=64)
    server_db_ids = fields.One2many(
        'saas_portal.server', 'oauth_application_id',
        string='Server Database')
    template_db_ids = fields.One2many(
        'saas_portal.database', 'oauth_application_id',
        string='Template Database')
    client_db_ids = fields.One2many(
        'saas_portal.client', 'oauth_application_id', string='Client Database')

    def _compute_get_last_connection(self):
        """Compute last connection date from access tokens."""
        for r in self:
            r.last_connection = False
            try:
                access_token = self.env['oauth.access_token'].search([
                    ('application_id', '=', r.id)
                ], order='id DESC', limit=1)
                if access_token and access_token.user_id:
                    login_date = getattr(access_token.user_id, 'login_date', None)
                    if login_date:
                        r.last_connection = str(login_date)
                    elif hasattr(access_token, 'create_date'):
                        r.last_connection = str(access_token.create_date)
            except Exception:
                pass


class SaasPortalDatabase(models.Model):
    """SaaS Portal Database model."""
    _name = 'saas_portal.database'
    _description = 'SaaS Portal Database'
    _inherits = {'oauth.application': 'oauth_application_id'}

    name = fields.Char('Database name', readonly=False)
    oauth_application_id = fields.Many2one(
        'oauth.application', 'OAuth Application',
        required=True, ondelete='cascade')
    server_id = fields.Many2one(
        'saas_portal.server', ondelete='restrict',
        string='Server', readonly=True)
    state = fields.Selection(
        [('draft', 'New'), ('open', 'In Progress'), ('cancelled', 'Cancelled'),
         ('pending', 'Pending'), ('deleted', 'Deleted'), ('template', 'Template')],
        'State', default='draft')
    host = fields.Char('Host', compute='_compute_host')
    public_url = fields.Char(compute='_compute_public_url')
    password = fields.Char()

    def _compute_host(self):
        """Compute host name based on template or default."""
        base_saas_domain = self.env['ir.config_parameter'].sudo().get_param('saas_portal.base_saas_domain')
        base_saas_domain_1 = '.'.join(base_saas_domain.rsplit('.', 2)[-2:]) if base_saas_domain else ''
        name_dict = {
            'base_saas_domain': base_saas_domain or '',
            'base_saas_domain_1': base_saas_domain_1,
        }
        for record in self:
            if record.server_id and record.server_id.clients_host_template:
                name_dict['dbname'] = record.name
                record.host = record.server_id.clients_host_template.format(**name_dict)
            else:
                _compute_host(record)

    def _compute_public_url(self):
        """Compute public URL for database."""
        for record in self:
            if not record.server_id:
                record.public_url = ''
                continue
            scheme = record.server_id.request_scheme
            host = record.host
            port = record.server_id.request_port
            public_url = "%s://%s" % (scheme, host)
            if (scheme == 'http' and port != 80) or (scheme == 'https' and port != 443):
                public_url = public_url + ':' + str(port)
            record.public_url = public_url + '/'

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to automatically create OAuth application if needed."""
        for vals in vals_list:
            if 'oauth_application_id' not in vals or not vals.get('oauth_application_id'):
                oauth_app = self.env['oauth.application'].sudo().create({})
                vals['oauth_application_id'] = oauth_app.id
        return super().create(vals_list)

    def _backup(self):
        """Call remote server to backup database."""
        self.ensure_one()
        state = {
            'd': self.name,
            'client_id': self.client_id,
        }
        req, req_kwargs = self.server_id._request_server(
            path='/saas_server/backup_database', state=state, client_id=self.client_id)
        res = requests.Session().send(req, **req_kwargs)
        _logger.info('backup database: %s', res.text)
        if not res.ok:
            raise exceptions.Warning(_('Reason: %s \n Message: %s') % (res.reason, res.content))
        data = simplejson.loads(res.text)
        if not isinstance(data[0], dict):
            raise exceptions.Warning(data)
        if data[0]['status'] != 'success':
            warning = data[0].get('message', _('Could not backup database; please check your logs'))
            raise exceptions.Warning(warning)
        return True

    def action_sync_server(self):
        """Sync server for this database."""
        for record in self:
            if record.server_id:
                record.server_id.action_sync_server()

    @api.model
    def _proceed_url(self, url):
        """Return action to proceed to URL."""
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'name': 'Redirection',
            'url': url
        }

    def _request_url(self, path):
        """Build request URL for database operation."""
        r = self[0]
        state = {
            'd': r.name,
            'host': r.host,
            'public_url': r.public_url,
            'client_id': r.client_id,
        }
        url = r.server_id._request(path=path, state=state, client_id=r.client_id)
        return url

    def _request(self, path):
        """Return action to request path."""
        url = self._request_url(path)
        return self._proceed_url(url)

    def edit_database(self):
        """Obsolete. Use saas_portal.edit_database widget instead."""
        for database_obj in self:
            return database_obj._request('/saas_server/edit_database')

    def delete_database(self):
        """Delete database via remote request."""
        for database_obj in self:
            return database_obj._request('/saas_server/delete_database')

    def upgrade(self, payload=None):
        """Upgrade database with payload."""
        config_obj = self.env['saas.config']
        res = []
        if payload is not None:
            for database_obj in self:
                res.append(config_obj.do_upgrade_database(payload.copy(), database_obj))
        return res

    def delete_database_server(self, **kwargs):
        """Delete database on server."""
        self.ensure_one()
        return self._delete_database_server(**kwargs)

    def _delete_database_server(self, force_delete=False):
        """Internal method to delete database on server."""
        for database in self:
            state = {
                'd': database.name,
                'client_id': database.client_id,
            }
            if force_delete:
                state['force_delete'] = 1
            req, req_kwargs = database.server_id._request_server(
                path='/saas_server/delete_database',
                state=state, client_id=database.client_id)
            res = requests.Session().send(req, **req_kwargs)
            _logger.info('delete database: %s', res.text)
            if res.status_code != 500:
                database.state = 'deleted'

    def show_upgrade_wizard(self):
        """Show upgrade wizard for database."""
        obj = self[0]
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'saas.config',
            'target': 'new',
            'context': {
                'default_action': 'upgrade',
                'default_database': obj.name
            }
        }


class SaasPortalClient(models.Model):
    """SaaS Portal Client - Représente un client SaaS."""
    _name = 'saas_portal.client'
    _description = 'Client'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'saas_portal.database', 'saas_base.client']

    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    plan_id = fields.Many2one('saas_portal.plan', string='Plan', ondelete='set null', readonly=True)
    expiration_datetime = fields.Datetime(string="Expiration")
    expired = fields.Boolean('Expired', readonly=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Salesperson')
    notification_sent = fields.Boolean(
        default=False, readonly=True,
        help='notification about oncoming expiration has sent')
    support_team_id = fields.Many2one('saas_portal.support_team', 'Support Team')
    active = fields.Boolean(default=True, compute='_compute_active', store=True)
    block_on_expiration = fields.Boolean('Block clients on expiration', default=False)
    block_on_storage_exceed = fields.Boolean('Block clients on storage exceed', default=False)
    storage_exceed = fields.Boolean('Storage limit has been exceed', default=False)
    trial_hours = fields.Integer(
        'Initial period for trial (hours)',
        help='Subscription initial period in hours for trials',
        readonly=True)
    visible_addons = fields.Char(
        'Visible addons',
        help='Comma separated addons, what are visible in Apps page')

    # TODO: Migrate to new tracking API when available
    _track = {
        'expired': {
            'saas_portal.mt_expired': lambda self, cr, uid, obj, ctx=None: obj.expired
        }
    }

    @api.depends('state')
    def _compute_active(self):
        """Compute active state based on database state."""
        for record in self:
            record.active = record.state != 'deleted'

    @api.model
    def _cron_suspend_expired_clients(self):
        """Cron job to suspend expired clients."""
        payload = {
            'params': [{'key': 'saas_client.suspended', 'value': '1', 'hidden': True}],
        }
        now = fields.Datetime.now()
        expired = self.search([
            ('expiration_datetime', '<', now),
            ('expired', '=', False)
        ])
        expired.write({'expired': True})
        for record in expired:
            if record.trial or record.block_on_expiration:
                template = self.env.ref('saas_portal.email_template_has_expired_notify')
                record.message_post_with_template(template.id, composition_mode='comment')
                record.upgrade(payload)
                record.state = 'pending'

    @api.model
    def _cron_notify_expired_clients(self):
        """Cron job to notify clients about upcoming expiration."""
        notification_delta = int(self.env['ir.config_parameter'].sudo().get_param(
            'saas_portal.expiration_notify_in_advance', '0'))
        if notification_delta > 0:
            expiration_date = (datetime.now() + timedelta(days=notification_delta)).strftime(
                DEFAULT_SERVER_DATETIME_FORMAT)
            records = self.search([
                ('expiration_datetime', '<=', expiration_date),
                ('notification_sent', '=', False)
            ])
            records.write({'notification_sent': True})
            template = self.env.ref('saas_portal.email_template_expiration_notify')
            for record in records:
                record.with_context(days=notification_delta).message_post_with_template(
                    template.id, composition_mode='comment')

    def unlink(self):
        """Override unlink to clean up OAuth tokens."""
        for obj in self:
            tokens = self.env['oauth.access_token'].search([('application_id', '=', obj.id)])
            tokens.unlink()
        return super().unlink()

    def write(self, values):
        """Override write to sync parameters to client database."""
        payload_params = []
        if 'expiration_datetime' in values:
            payload_params.append({
                'key': 'saas_client.expiration_datetime',
                'value': values['expiration_datetime'],
                'hidden': True,
            })
        if 'visible_addons' in values:
            payload_params.append({
                'key': 'saas_client.visible_modules',
                'value': values['visible_addons'],
                'hidden': False,
            })
        for record in self:
            if payload_params:
                record.upgrade({"params": payload_params})
        return super().write(values)

    def rename_database(self, new_dbname):
        """Rename database on remote server."""
        self.ensure_one()
        state = {
            'd': self.name,
            'client_id': self.client_id,
            'new_dbname': new_dbname,
        }
        req, req_kwargs = self.server_id._request_server(
            path='/saas_server/rename_database', state=state, client_id=self.client_id)
        res = requests.Session().send(req, **req_kwargs)
        _logger.info('rename database: %s', res.text)
        if res.status_code != 500:
            self.name = new_dbname

    def sync_client(self):
        """Synchronize client with server."""
        self.ensure_one()
        self.server_id.action_sync_server(updating_client_ID=self.client_id)

    def check_partner_access(self, partner_id):
        """Check if partner has access to this client."""
        for record in self:
            if record.partner_id.id != partner_id:
                raise Forbidden

    def duplicate_database(self, dbname=None, partner_id=None, expiration=None, target_server=None):
        """Duplicate database to new client."""
        self.ensure_one()
        p_client = self.env['saas_portal.client']
        p_server = self.env['saas_portal.server']

        owner_user = self.env['res.users'].search(
            [('partner_id', '=', partner_id)], limit=1) or self.env.user

        if target_server and self.server_id != target_server:
            req, req_kwargs = self.server_id._request_server(
                path='/saas_server/dump_database_prepare',
                client_id=self.client_id,
            )
            origin_res = requests.Session().send(req, **req_kwargs)
            if not origin_res.ok:
                raise exceptions.Warning(_('Reason: %s \n Message: %s') % (origin_res.reason, origin_res.content))

            req, req_kwargs = target_server._request_server(
                path='/saas_server/restore_database',
                state={
                    "origin_uri": '{scheme}://{host}:{port}/saas_server/dump_database?dump_database_token={database_token}'.format(
                        scheme=self.server_id.local_request_scheme or self.server_id.request_scheme,
                        host=self.server_id.local_host or self.server_id.host,
                        port=self.server_id.request_port or 80,
                        database_token=origin_res.text,
                    )
                }
            )

            target_res = requests.Session().send(req, **req_kwargs)
            if not target_res.ok:
                raise exceptions.Warning(_('Reason: %s \n Message: %s') % (target_res.reason, target_res.content))

            server = target_server
            db_template = target_res.text
        else:
            server = self.server_id or p_server.get_saas_server()
            db_template = self.name

        server.action_sync_server()

        vals = {
            'name': dbname,
            'server_id': server.id,
            'plan_id': self.plan_id.id,
            'partner_id': partner_id or self.partner_id.id,
        }
        if expiration:
            now = datetime.now()
            delta = timedelta(hours=expiration)
            vals['expiration_datetime'] = (now + delta).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        client = p_client.create(vals)
        client_id = client.client_id

        owner_user_data = {
            'user_id': owner_user.id,
            'login': owner_user.login,
            'name': owner_user.name,
            'email': owner_user.email,
        }

        state = {
            'd': client.name,
            'e': client.expiration_datetime,
            'r': client.public_url + 'web',
            'owner_user': owner_user_data,
            'public_url': client.public_url,
            'db_template': db_template,
            'disable_mail_server': True,
        }

        req, req_kwargs = server._request_server(
            path='/saas_server/new_database',
            state=state, client_id=client_id, scope=['userinfo', 'force_login', 'trial', 'skiptheuse'])
        res = requests.Session().send(req, **req_kwargs)

        if not res.ok:
            raise exceptions.Warning(_('Reason: %s \n Message: %s') % (res.reason, res.content))
        try:
            data = simplejson.loads(res.text)
        except Exception as e:
            _logger.error('Error on parsing response: %s\n%s', [req.url, req.headers, req.body], res.text)
            raise

        data['id'] = client.id
        return data

    def get_upgrade_database_payload(self):
        """Get payload for database upgrade."""
        self.ensure_one()
        return {
            'params': [{
                'key': 'saas_client.expiration_datetime',
                'value': self.expiration_datetime,
                'hidden': True
            }]
        }

    def send_params_to_client_db(self):
        """Send parameters to client database."""
        for record in self:
            payload = {
                'params': [
                    {'key': 'saas_client.max_users', 'value': record.max_users, 'hidden': True},
                    {'key': 'saas_client.expiration_datetime', 'value': record.expiration_datetime, 'hidden': True},
                    {'key': 'saas_client.total_storage_limit', 'value': record.total_storage_limit, 'hidden': True}
                ]
            }
            self.env['saas.config'].do_upgrade_database(payload, record)

    def send_expiration_info_to_partner(self):
        """Send expiration information to partner."""
        for record in self:
            if record.expiration_datetime:
                template = self.env.ref('saas_portal.email_template_expiration_datetime_updated')
                record.message_post_with_template(template.id, composition_mode='comment')

    def storage_usage_monitoring(self):
        """Monitor storage usage and suspend if needed."""
        payload = {
            'params': [{'key': 'saas_client.suspended', 'value': '1', 'hidden': True}],
        }
        for r in self:
            if r.total_storage_limit and r.total_storage_limit < r.file_storage + r.db_storage and not r.storage_exceed:
                r.write({'storage_exceed': True})
                template = self.env.ref('saas_portal.email_template_storage_exceed')
                r.message_post_with_template(template.id, composition_mode='comment')
                if r.block_on_storage_exceed:
                    self.env['saas.config'].do_upgrade_database(payload, r)
            if (not r.total_storage_limit or r.total_storage_limit >= r.file_storage + r.db_storage) and r.storage_exceed:
                r.write({'storage_exceed': False})


class SaasPortalSupportTeams(models.Model):
    """SaaS Portal Support Team model."""
    _name = 'saas_portal.support_team'
    _description = 'SaaS Portal Support Team'
    _inherit = ['mail.thread']
    name = fields.Char('Team name')
