{
    'name': 'SaaS Dynamic Features',
    'version': '18.0.1.0.0',
    'category': 'Website/Theme',
    'summary': 'Dynamic features and snippets for Odoo 18 SaaS',
    'description': """
SaaS Dynamic Features
=====================
Adds dynamic, interactive, and immersive features to your SaaS website.
- Dynamic Snippets with 3D effects
- Advanced animations
- Theme customization enhancements
    """,
    'author': 'Kondro Networks',
    'depends': ['website', 'web_editor'],
    'data': [
        'views/snippets.xml',
        'views/footer.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'saas_dynamic_features/static/src/scss/dynamic_features.scss',
            'saas_dynamic_features/static/src/js/dynamic_features.js',
        ],
        'web.assets_backend': [
             'saas_dynamic_features/static/src/scss/dynamic_features.scss',
             'saas_dynamic_features/static/src/js/dynamic_features.js',
             'saas_dynamic_features/static/src/xml/app_dashboard.xml',
        ],
    },
    'installable': True,
    'application': False,
}
