# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    saas_ovh_project_id = fields.Char(
        string='OVH Project ID',
        config_parameter='saas_server_backup_ovh.project_id',
        help="Identifiant du projet Public Cloud OVH (serviceName)."
    )

    saas_ovh_storage_region = fields.Char(
        string='Région Object Storage',
        config_parameter='saas_server_backup_ovh.region',
        help="Région Object Storage (ex: GRA, SBG, BHS)."
    )

    saas_ovh_container_name = fields.Char(
        string='Container Object Storage',
        config_parameter='saas_server_backup_ovh.container',
        help="Nom du container (Swift) ou bucket S3 compatible où stocker les sauvegardes."
    )

    saas_ovh_application_key = fields.Char(
        string='OVH Application Key',
        config_parameter='saas_server_backup_ovh.application_key'
    )

    saas_ovh_application_secret = fields.Char(
        string='OVH Application Secret',
        config_parameter='saas_server_backup_ovh.application_secret'
    )

    saas_ovh_consumer_key = fields.Char(
        string='OVH Consumer Key',
        config_parameter='saas_server_backup_ovh.consumer_key'
    )


