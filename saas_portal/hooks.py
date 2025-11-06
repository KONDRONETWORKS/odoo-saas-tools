"""
Hooks pour post-init et post-upgrade du module saas_portal
"""
from odoo import SUPERUSER_ID, api
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Hook appelé après l'installation du module"""
    # Dans Odoo 18, le hook reçoit directement l'environnement
    
    # 1. S'assurer que la vue list existe
    _ensure_plan_list_view(env)
    
    # 2. Créer un serveur par défaut si aucun n'existe
    _ensure_default_server(env)
    
    # 3. Lier les templates au serveur par défaut
    _link_templates_to_server(env)
    
    # 4. Installer automatiquement saas_portal_start si disponible
    _install_portal_start_module(env)
    
    _logger.info("✅ post_init_hook terminé avec succès")


def _ensure_plan_list_view(env):
    """S'assurer que la vue list existe pour Odoo 18"""
    view = env['ir.ui.view'].sudo().search([
        ('model', '=', 'saas_portal.plan'),
        ('type', '=', 'list'),
        ('name', '=', 'saas_portal.plans.list')
    ], limit=1)
    if not view:
        env['ir.ui.view'].sudo().create({
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


def _ensure_default_server(env):
    """Créer un serveur par défaut si aucun n'existe"""
    server_obj = env['saas_portal.server']
    
    # Chercher un serveur existant
    existing_server = server_obj.sudo().search([], limit=1)
    
    if existing_server:
        _logger.info(f"✅ Serveur existant trouvé: {existing_server.name} (ID: {existing_server.id})")
        return existing_server
    
    # Créer un serveur par défaut
    try:
        # L'application OAuth sera créée automatiquement par le modèle
        default_server = server_obj.sudo().create({
            'name': 'server-default',
            'request_scheme': 'http',
            'local_request_scheme': 'http',
            'request_port': 8069,
            'local_host': 'localhost',
            'local_port': '8069',
            'verify_ssl': False,
            'active': True,
            'sequence': 1,
        })
        _logger.info(f"✅ Serveur par défaut créé: {default_server.name} (ID: {default_server.id})")
        return default_server
    except Exception as e:
        _logger.error(f"❌ Erreur lors de la création du serveur par défaut: {e}")
        return None


def _link_templates_to_server(env):
    """Lier les templates au serveur par défaut"""
    server_obj = env['saas_portal.server']
    template_obj = env['saas_portal.database']
    plan_obj = env['saas_portal.plan']
    
    # Récupérer le serveur par défaut (ou le créer)
    server = _ensure_default_server(env)
    if not server:
        _logger.warning("⚠️  Aucun serveur disponible pour lier les templates")
        return
    
    # Trouver tous les templates sans serveur
    templates_without_server = template_obj.sudo().search([
        ('server_id', '=', False)
    ])
    
    if templates_without_server:
        templates_without_server.write({'server_id': server.id})
        _logger.info(f"✅ {len(templates_without_server)} template(s) lié(s) au serveur {server.name}")
    
    # Trouver tous les plans sans serveur qui ont un template
    plans_without_server = plan_obj.sudo().search([
        ('server_id', '=', False),
        ('template_id', '!=', False)
    ])
    
    if plans_without_server:
        plans_without_server.write({'server_id': server.id})
        _logger.info(f"✅ {len(plans_without_server)} plan(s) lié(s) au serveur {server.name}")


def _install_portal_start_module(env):
    """Installer automatiquement saas_portal_start si disponible"""
    module_obj = env['ir.module.module']
    
    # Chercher le module saas_portal_start
    portal_start = module_obj.sudo().search([
        ('name', '=', 'saas_portal_start'),
        ('state', 'in', ['uninstalled', 'to install'])
    ], limit=1)
    
    if portal_start:
        try:
            portal_start.button_immediate_install()
            _logger.info("✅ Module saas_portal_start installé automatiquement")
        except Exception as e:
            _logger.warning(f"⚠️  Impossible d'installer saas_portal_start automatiquement: {e}")
            _logger.info("💡 Vous pouvez l'installer manuellement depuis Apps > SaaS Portal - /page/start")
    else:
        # Vérifier si déjà installé
        installed = module_obj.sudo().search([
            ('name', '=', 'saas_portal_start'),
            ('state', '=', 'installed')
        ], limit=1)
        if installed:
            _logger.info("✅ Module saas_portal_start déjà installé")
        else:
            _logger.info("ℹ️  Module saas_portal_start non trouvé. Installation manuelle requise.")


def post_upgrade_hook(env):
    """Hook appelé après la mise à jour du module"""
    # Dans Odoo 18, le hook reçoit directement l'environnement
    _ensure_plan_list_view(env)
    _link_templates_to_server(env)
    _install_portal_start_module(env)
    _logger.info("✅ post_upgrade_hook terminé avec succès")

