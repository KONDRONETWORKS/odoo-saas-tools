# -*- coding: utf-8 -*-
{
    "name": "Kondro DT Hub",
    "summary": "Tableau de bord central pour le Directeur Technique",
    "version": "16.0.1.0.0",
    "category": "Kondro/Directeur Technique",
    "author": "Kondro",
    "website": "https://kondro.example",
    "depends": [
        "base",
        "mail",
        "kondro_core",
        "kondro_finance",
    ],
    "data": [
        "security/dt_hub_security.xml",
        "security/ir.model.access.csv",
        "data/dt_hub_metric_data.xml",
        "views/dt_hub_menu.xml",
        "views/dt_hub_dashboard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # TODO: ajouter des assets spécifiques si nécessaire
        ],
    },
    "license": "LGPL-3",
    "installable": True,
    "application": True,
}
