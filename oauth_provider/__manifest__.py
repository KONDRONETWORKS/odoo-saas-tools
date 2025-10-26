{
    'name': 'OAuth2 provider',
    'version': '18.0.1.0.0',
    'author': 'Ivan Yelizariev',
    'license': 'LGPL-3',
    'category': 'SaaS',
    "support": "apps@itexperts4africa.com",
    'website': 'https://www.itexperts4africa.com',

    'depends': ['web'],
    'external_dependencies': {
        'python': ['oauthlib'],
    },
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
