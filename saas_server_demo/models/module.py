import os

from odoo import models, fields, api, tools
# from odoo.addons.base.module.module import Module as A  # N'existe plus dans Odoo 18
from odoo.modules import get_module_resource


class ModuleDemo(models.Model):
    _inherit = "ir.module.module"

    demo_addons = fields.Char(
        string='Demo addons', help='Comma-separated string of modules technical names')
    demo_addons_hidden = fields.Char(
        string='Demo addons hidden', help='Comma-separated string of modules technical names')
    demo_url = fields.Char(string='Demo url')
    demo_title = fields.Char(
        string='Title of a demo set. Also title for demo product on the portal')
    demo_summary = fields.Char(string='Demo set summary')
    price = fields.Float(string='Price', default=0)
    currency = fields.Char(
        "Currency", help="The currency the field is expressed in.")
    demo_images = fields.Char(
        help="file names, the files should be placed in /static/description/demo of the module")
    
    # Note: En Odoo 18, le champ installable n'existe plus dans ir.module.module
    # Mais certains modules standards (comme base_import_module) essaient encore d'y accéder
    # On crée un champ calculé pour éviter les erreurs SQL
    installable = fields.Boolean(
        string='Installable',
        compute='_compute_installable',
        store=False,
        help='Module can be installed (always True in Odoo 18 - computed from state)'
    )
    
    @api.depends('state')
    def _compute_installable(self):
        """Compute installable from state - in Odoo 18, installable field was removed"""
        for module in self:
            # Un module est installable s'il n'est pas en état 'uninstallable'
            module.installable = module.state != 'uninstallable'

    @staticmethod
    def get_values_from_terp(terp):
        # Dans Odoo 18, la méthode update_list() gère elle-même les champs standards
        # On ne retourne que les champs spécifiques au module demo (définis dans cette classe)
        # pour éviter les erreurs avec les champs qui n'existent plus ou qui ont changé
        res = {
            'demo_title': terp.get('demo_title', False),
            'demo_summary': terp.get('demo_summary', False),
            'demo_addons': ','.join(terp.get('demo_addons', [])) if terp.get('demo_addons') else False,
            'demo_addons_hidden': ','.join(terp.get('demo_addons_hidden', [])) if terp.get('demo_addons_hidden') else False,
            'demo_url': terp.get('demo_url', False),
            'price': terp.get('price', False) or 0,
            'currency': terp.get('currency', False),
            'demo_images': ','.join(terp.get('demo_images', [])) if terp.get('demo_images') else False,
        }
        # Filtrer les valeurs False pour éviter de mettre à jour avec False
        return {k: v for k, v in res.items() if v is not False}

    def get_demo_images(self):
        self.ensure_one()
        demo_images = self.demo_images and self.demo_images.split(',')
        res = []
        mod_path = get_module_resource(self.name)
        for image_name in demo_images:
            full_name = os.path.join(mod_path, image_name)
            try:
                with tools.file_open(full_name, 'rb') as image_file:
                    import base64
                    res.append(
                        (image_name, base64.b64encode(image_file.read()).decode('utf-8')))
            except Exception as e:
                pass
        return res
