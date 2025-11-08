# -*- coding: utf-8 -*-
{
    "name": "Kondro DT Reporting",
    "summary": "Reporting BI pour le Directeur Technique",
    "version": "16.0.1.0.0",
    "category": "Kondro/Directeur Technique",
    "author": "Kondro",
    "website": "https://kondro.example",
    "depends": [
        "mail",
        "kondro_dt_hub",
        "kondro_dt_projects",
        "kondro_dt_workflow",
        "kondro_dt_docs",
        "kondro_finance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/dt_reporting_dashboard.xml",
        "views/dt_reporting_menu.xml",
        "views/dt_report_config_views.xml",
        "views/dt_kpi_snapshot_views.xml",
        "views/dt_board_views.xml",
        "wizards/dt_reporting_export_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
