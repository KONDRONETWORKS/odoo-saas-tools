from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    current_domain = fields.Char(compute='_compute_domain', readonly=True)
    domain_change_link = fields.Html(compute='_compute_domain', readonly=True)

    @api.depends()
    def _compute_domain(self):
        """Compute domain values"""
        for record in self:
            current_domain = self.env["ir.config_parameter"].sudo().get_param('web.base.url', default=None)
            link = self.env["ir.config_parameter"].sudo().get_param('saas_client.saas_dashboard', default=None)
            label = _('You can change your domain name here')
            html = link and f'<a href="{link}" target="_blank" class="oe_link"><i class="fa fa-fw fa-arrow-right"></i>{label}</a>' or False
            record.current_domain = current_domain or False
            record.domain_change_link = html
