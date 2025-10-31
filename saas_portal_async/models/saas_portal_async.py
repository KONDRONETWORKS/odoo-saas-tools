from odoo import api
from odoo import models
try:
    from odoo.addons.connector.queue.job import job
    from odoo.addons.connector.session import ConnectorSession
    CONNECTOR_AVAILABLE = True
except Exception as e:
    def empty_decorator(func):
        return func
    job = empty_decorator
    ConnectorSession = None
    CONNECTOR_AVAILABLE = False


@job
def async_client_create(session, mself, *args, **kwargs):
    model = session.env[mself].browse(args[0])
    plan_id = model.id
    plan = model.env['saas_portal.plan'].browse(plan_id)
    res = plan._create_new_database(**kwargs)
    client = model.env['saas_portal.client'].browse(res.get('id'))
    client.server_id.action_sync_server()


class SaasPortalPlan(models.Model):
    _inherit = 'saas_portal.plan'

    def create_new_database(self, async_mode=None, **kwargs):
        if async_mode and CONNECTOR_AVAILABLE and ConnectorSession:
            session = ConnectorSession(self._cr, self._uid, self._context)
            job_uuid = async_client_create.delay(
                session, self._name, self.id, async_mode=async_mode, **kwargs)
        else:
            if async_mode and not CONNECTOR_AVAILABLE:
                # Si connector n'est pas disponible, créer en mode synchrone
                pass
            res = super(SaasPortalPlan, self)._create_new_database(
                async_mode=async_mode, **kwargs)
            return res
