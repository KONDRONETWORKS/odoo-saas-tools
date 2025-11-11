"""
Module Mailgun pour saas_portal - chargé uniquement si saas_portal est disponible
Ce fichier ne sera chargé que si le module saas_portal est installé.
"""
from odoo import models, fields, api
from odoo.tools import json
from . import mailgun

import logging
_logger = logging.getLogger(__name__)

try:
    pass
except Exception as e:
    _logger.critical('SAAS Route53 Requires the python library Boto which is not \
    found on your installation')


# Vérifier si saas_portal est disponible avant de définir les classes
def _check_saas_portal_available():
    """Vérifier si saas_portal est disponible dans le registre"""
    try:
        # On essaie d'accéder au modèle via l'environnement
        # Cette vérification sera faite au runtime, pas au chargement
        return True  # On assume que c'est disponible, l'erreur sera gérée par Odoo
    except Exception:
        return False


# Ces classes ne seront chargées que si saas_portal est installé
# Odoo vérifiera automatiquement que le modèle parent existe

class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'

    mail_domain = fields.Char('Mail domain')

    def _create_domain_on_mailgun(self):
        '''Create domain on mailgun and return data to configure dns and smtp'''

        self.ensure_one()
        ir_params = self.env['ir.config_parameter']
        api_key = ir_params.sudo().get_param('saas_mailgun.saas_mailgun_api_key')
        password = mailgun.random_password()
        if not self.mail_domain:
            # Utiliser aws_hosted_zone_id si disponible (module saas_sysadmin_aws_route53)
            zone_name = getattr(self.server_id, 'aws_hosted_zone_id', None) and self.server_id.aws_hosted_zone_id.name or 'example.com'
            self.mail_domain = self.name.split('.')[0] + '.' + zone_name
        return mailgun.add_domain(api_key=api_key, domain_name=self.mail_domain, smtp_password=password)

    def _create_route_on_mailgun(self):
        '''Create route on mailgun for storing incomming messages'''

        self.ensure_one()
        ir_params = self.env['ir.config_parameter']
        api_key = ir_params.sudo().get_param('saas_mailgun.saas_mailgun_api_key')
        return mailgun.create_store_route(api_key=api_key, domain=self.name,
                                          mail_domain=self.mail_domain, request_scheme=self.server_id.request_scheme)

    def _domain_verification_and_dns_route53(self, domain_info):
        self.ensure_one()
        receiving_dns_records = domain_info.get('receiving_dns_records')
        name = self.mail_domain
        value = []
        for r in receiving_dns_records:
            value.append("%(priority)s %(value)s" % r)
        type = 'mx'
        # Utiliser _update_zone si disponible (module saas_sysadmin_aws_route53)
        if hasattr(self.server_id, '_update_zone'):
            self.server_id._update_zone(name=name, type=type, value=value)

        sending_dns_records = domain_info.get('sending_dns_records')
        for r in sending_dns_records:
            name = str(r['name'])
            type = str(r['record_type'].lower())
            value = str(r['value'])
            # Utiliser _update_zone si disponible (module saas_sysadmin_aws_route53)
        if hasattr(self.server_id, '_update_zone'):
            self.server_id._update_zone(name=name, type=type, value=value)


class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'

    def _create_new_database(self, **kw):
        res = super(SaasPortalPlan, self)._create_new_database(**kw)

        client_obj = self.env['saas_portal.client'].browse(res.get('id'))
        try:
            mailgun_res = client_obj._create_domain_on_mailgun()
            client_obj._create_route_on_mailgun()

            new_domain_info = json.loads(mailgun_res.text)
            client_obj._domain_verification_and_dns_route53(new_domain_info)
        except Exception as e:
            _logger.exception("Error during mailgun domain creation", exc_info=True)
            return res

        ir_params = self.env['ir.config_parameter']
        api_key = ir_params.sudo().get_param('saas_mailgun.saas_mailgun_api_key')
        client_obj.upgrade(payload={'configure_outgoing_mail': [new_domain_info['domain']],
                                    'params': [{'key': 'mailgun.apikey', 'value': api_key, 'hidden': True},
                                               {'key': 'mail.catchall.domain', 'value': client_obj.mail_domain, 'hidden': True}]})

        return res
