"""
Hooks pour post-init et post-upgrade du module saas_portal
"""
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """Hook appelé après l'installation du module"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    _ensure_plan_list_view(env)


def post_upgrade_hook(cr, registry):
    """Hook appelé après la mise à jour du module"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    _ensure_plan_list_view(env)


def _ensure_plan_list_view(env):
    """Force la création de la vue list pour saas_portal.plan (Odoo 18 utilise 'list' au lieu de 'tree')"""
    # Chercher la vue list existante
    view_list = env['ir.ui.view'].search([
        ('model', '=', 'saas_portal.plan'),
        ('type', '=', 'list'),
        ('name', '=', 'saas_portal.plans.list')
    ], limit=1)
    
    arch_content = '''<?xml version="1.0"?>
<list string="Plans">
    <field name="sequence" invisible="1"/>
    <field name="name"/>
    <field name="template_id"/>
    <field name="state"/>
</list>'''
    
    # Si la vue n'existe pas, la créer
    if not view_list:
        env['ir.ui.view'].create({
            'name': 'saas_portal.plans.list',
            'model': 'saas_portal.plan',
            'type': 'list',
            'priority': 1,
            'active': True,
            'arch': arch_content
        })
        return True
    
    # Vérifier que la vue est active et a la bonne priorité
    if not view_list.active or view_list.priority != 1:
        view_list.write({
            'active': True,
            'priority': 1
        })
        # Mettre à jour l'architecture si nécessaire
        if '<list' not in str(view_list.arch_db):
            view_list.write({'arch': arch_content})
    
    return False

