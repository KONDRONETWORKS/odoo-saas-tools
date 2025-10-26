{
    'name': "saas_server_backup_ftp",
    'author': "IT-Projects LLC, Ildar Nasyrov, Nicolas JEUDY",
    'license': 'GPL-3',
    "support": "apps@itexperts4africa.com",
    'website': "https://twitter.com/nasyrov_ildar",
    'category': 'SaaS',
    'version': '18.0.1.0.0',
    'depends': ['saas_server'],
    "external_dependencies": {"python": ['pysftp'], "bin": []},
    'data': [
        'views/res_config.xml',
        'data/ir_cron.xml',
    ],
}
