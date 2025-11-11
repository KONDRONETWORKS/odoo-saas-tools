# -*- coding: utf-8 -*-
{
    "name": "Kondro DT Docs",
    "summary": "Bibliothèque documentaire du Directeur Technique",
    "version": "18.0.1.0.0",
    "category": "Kondro/Directeur Technique",
    "author": "Kondro",
    "website": "https://kondro.example",
    "depends": [
        "mail",
        "kondro_dt_projects",
        "kondro_dt_workflow",
    ],
    "data": [
        "data/dt_docs_sequence.xml",
        "security/dt_docs_security.xml",
        "security/ir.model.access.csv",
        "views/dt_docs_menu.xml",
        "views/dt_document_views.xml",
        "views/dt_document_category_views.xml",
        "views/dt_project_extension_views.xml",
        "views/dt_dossier_extension_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
