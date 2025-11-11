# -*- coding: utf-8 -*-
{
    "name": "Kondro DT Projects",
    "summary": "Extension projets pour le Directeur Technique",
    "version": "18.0.1.0.0",
    "category": "Kondro/Directeur Technique",
    "author": "Kondro",
    "website": "https://kondro.example",
    "depends": [
        "mail",
        "kondro_core",
        "kondro_dt_hub",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/dt_project_views.xml",
        "views/dt_project_milestone_views.xml",
        "views/dt_project_risk_views.xml",
        "views/dt_project_design_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
