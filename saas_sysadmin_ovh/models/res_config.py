# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    saas_ovh_application_key = fields.Char(
        string='OVH Application Key',
        config_parameter='saas_sysadmin_ovh.application_key',
        help="Clé d'application OVH. À générer depuis l'espace client OVH (APIv6)."
    )

    saas_ovh_application_secret = fields.Char(
        string='OVH Application Secret',
        config_parameter='saas_sysadmin_ovh.application_secret',
        help="Secret associé à l'application OVH. Conserver confidentiel."
    )

    saas_ovh_consumer_key = fields.Char(
        string='OVH Consumer Key',
        config_parameter='saas_sysadmin_ovh.consumer_key',
        help="Consumer Key autorisée à manipuler les zones DNS du compte OVH."
    )

    saas_ovh_endpoint = fields.Selection(
        selection=[
            ('ovh-eu', 'ovh-eu'),
            ('ovh-ca', 'ovh-ca'),
            ('ovh-us', 'ovh-us'),
            ('soyoustart-eu', 'soyoustart-eu'),
            ('soyoustart-ca', 'soyoustart-ca'),
            ('kimsufi-eu', 'kimsufi-eu'),
            ('kimsufi-ca', 'kimsufi-ca'),
        ],
        default='ovh-eu',
        string='OVH Endpoint',
        config_parameter='saas_sysadmin_ovh.endpoint',
        help="Endpoint API OVH à utiliser en fonction de la zone de votre compte."
    )

    saas_ovh_root_domain = fields.Char(
        string='Domaine Racine',
        config_parameter='saas_sysadmin_ovh.root_domain',
        help="Domaine principal sur lequel seront créés les sous-domaines client (ex: saas.example.com)."
    )


