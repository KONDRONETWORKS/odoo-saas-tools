# -*- coding: utf-8 -*-
{
    "name": "Kondro DT Workflow",
    "summary": "Matrices RACI et validations transverses pour le Directeur Technique",
    "version": "16.0.1.0.0",
    "category": "Kondro/Directeur Technique",
    "author": "Kondro",
    "website": "https://kondro.example",
    "depends": [
        "mail",
        "kondro_dt_projects",
        "kondro_finance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/dt_workflow_matrix_views.xml",
        "views/dt_expense_request_views.xml",
        "views/dt_project_workflow_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
