# -*- coding: utf-8 -*-
{
	'name': "SLife Backend Theme",
	'summary': """Accordion Menu, Font Awesome Icon""",
	'description': """Accordion Menu, Font Awesome Icon""",
	'author': "Cheick Oumar Tidiane Traore",
	'category': 'Themes/Backend',
	'version': '18.0.1.0.0',
	'license': 'AGPL-3',
	'depends': ['web', 'mail'],
    'data': [
        'views/webclient_templates.xml',
        'views/slife_menu_view.xml',
        'views/res_config_settings_views.xml',
    ],
	'qweb': [
		'static/src/xml/slife_icon_template.xml'
	],
	'images': [
        'static/description/slife_screenshot.png',
    ],
    'icon': 'static/description/icon.png',
	'application': True,
    'installable': True,
    'auto_install': False,
}
