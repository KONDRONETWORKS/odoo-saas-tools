from odoo import api
from odoo import models

import logging
_logger = logging.getLogger(__name__)


class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'

    def create_template(self):
        assert len(self) == 1, 'This method is applied only for single record'
        plan = self[0]
        if plan.server_id.aws_hosted_zone_id:
            plan.server_id._update_zone(plan.template_id.name, value=plan.server_id.name, type='cname')
        return super(SaasPortalPlan, self).create_template()

    def delete_template(self):
        super(SaasPortalPlan, self).delete_template()
        plan = self[0]
        if plan.server_id.aws_hosted_zone_id:
            plan.server_id._update_zone(plan.template_id.name, type='cname', action='delete')
        return True


class SaasPortalClient(models.Model):
    _inherit = 'saas_portal.client'

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        if isinstance(vals_list, dict):
            vals_list = [vals_list]
        clients = super(SaasPortalClient, self).create(vals_list)
        for client in clients:
            if client.server_id.aws_hosted_zone_id:
                client.server_id._update_zone(client.name, value=client.server_id.name, type='cname')
        return clients

    def write(self, vals):
        for client in self:
            if 'server_id' in vals:
                server = self.env['saas_portal.server'].browse(vals['server_id'])
                if client.server_id.aws_hosted_zone_id and server.id != client.server_id.id:
                    client.server_id._update_zone(client.name, value=client.server_id.name,
                                                  type='cname', action='update')
        super(SaasPortalClient, self).write(vals)
        return True

    def unlink(self):
        for client in self:
            if client.server_id.aws_hosted_zone_id:
                client.server_id._update_zone(client.name, type='cname', action='delete')
        return super(SaasPortalClient, self).unlink()
