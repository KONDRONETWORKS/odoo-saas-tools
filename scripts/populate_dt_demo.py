# -*- coding: utf-8 -*-
"""Jeu de données de démonstration pour la suite Directeur Technique."""

from datetime import date



MODULES_DT = [
    'kondro_dt_hub',
    'kondro_dt_projects',
    'kondro_dt_workflow',
    'kondro_dt_docs',
    'kondro_dt_reporting',
]


def _ensure_modules(env):
    Module = env['ir.module.module']
    mods = Module.search([('name', 'in', MODULES_DT)])
    for mod in mods.filtered(lambda m: m.state not in ('installed', 'to install', 'to upgrade')):
        mod.with_context(overwrite=True).button_immediate_install()
    pending = Module.search([('name', 'in', MODULES_DT), ('state', 'in', ['to install', 'to upgrade'])])
    if pending:
        pending.button_immediate_install()



def _check_models(env):
    required = [
        'kondro.dt.document.category',
        'kondro.dt.document',
        'kondro.dt.report.config',
        'kondro.dt.reporting.board',
    ]
    missing = [name for name in required if name not in env.registry.models]
    if missing:
        raise RuntimeError('Modules requis non installés: %s' % ', '.join(missing))


def _ensure_category(env, name, sequence=10):
    Category = env["kondro.dt.document.category"]
    category = Category.search([("name", "=", name)], limit=1)
    if category:
        return category
    return Category.create({"name": name, "sequence": sequence})


def _ensure_tag(env, name, color=0):
    Tag = env["kondro.dt.document.tag"]
    tag = Tag.search([("name", "=", name)], limit=1)
    if tag:
        return tag
    return Tag.create({"name": name, "color": color})


def _create_demo_project(env, company):
    Project = env["kondro.project"]
    partner = env.ref("base.res_partner_1")
    project = Project.search([("name", "=", "Projet Plateau Cloud")], limit=1)
    if project:
        return project
    return Project.create({
        "name": "Projet Plateau Cloud",
        "project_type": "it",
        "status": "in_progress",
        "client_id": partner.id,
        "budget": 25000000,
        "start_date": date.today().replace(day=1),
        "company_id": company.id,
    })


def _create_demo_dossier(env, project, company):
    Dossier = env["kondro.commercial.dossier"]
    dossier = Dossier.search([("name", "=", "Dossier Cloud Public")], limit=1)
    if dossier:
        if project not in dossier.project_ids:
            dossier.write({"project_ids": [(4, project.id)]})
        return dossier
    return Dossier.create({
        "name": "Dossier Cloud Public",
        "client_id": project.client_id.id,
        "commercial_id": env.user.id,
        "project_manager_id": env.user.id,
        "budget": project.budget,
        "project_ids": [(6, 0, [project.id])],
        "company_id": company.id,
    })


def _create_demo_expense(env, project, company):
    Expense = env["kondro.expense.request"]
    expense = Expense.search([("name", "=", "Serveurs QA")], limit=1)
    if expense:
        return expense
    return Expense.create({
        "name": "Serveurs QA",
        "expense_type": "commercial",
        "state": "approved",
        "estimated_amount": 1800000,
        "project_id": project.id,
        "planned_payment_date": date.today(),
        "company_id": company.id,
    })


def _create_demo_document(env, project, category, tag, company):
    Document = env["kondro.dt.document"]
    doc = Document.search([("name", "=", "HLD Plateau Cloud")], limit=1)
    if doc:
        return doc
    return Document.create({
        "name": "HLD Plateau Cloud",
        "category_id": category.id,
        "tag_ids": [(6, 0, [tag.id])],
        "project_id": project.id,
        "description": "Architecture fonctionnelle du projet plateau cloud.",
        "company_id": company.id,
    })


def _create_demo_kpis(env, company):
    Config = env["kondro.dt.report.config"]
    Model = env["ir.model"]
    configs = []

    project_model = Model._get("kondro.project")
    configs.append(Config.create({
        "name": "Projets en cours",
        "code": "KPI_PROJETS_EN_COURS",
        "model_id": project_model.id,
        "aggregator": "count",
        "domain": "[('status', '=', 'in_progress')]",
        "periodicity": "weekly",
        "company_id": company.id,
    }))

    expense_model = Model._get("kondro.expense.request")
    configs.append(Config.create({
        "name": "Dépenses en attente",
        "code": "KPI_DEPENSES_EN_ATTENTE",
        "model_id": expense_model.id,
        "aggregator": "count",
        "domain": "[('state', 'in', ['submitted', 'validated'])]",
        "periodicity": "weekly",
        "company_id": company.id,
    }))

    risk_model = Model._get("kondro.dt.project.risk")
    configs.append(Config.create({
        "name": "Risques critiques",
        "code": "KPI_RISQUES_CRITIQUES",
        "model_id": risk_model.id,
        "aggregator": "count",
        "domain": "[('probability', '=', 'critical')]",
        "periodicity": "weekly",
        "company_id": company.id,
    }))

    for config in configs:
        config.action_compute_snapshot()
    return configs


def _ensure_board(env, configs, company):
    Board = env["kondro.dt.reporting.board"]
    board = Board.search([("name", "=", "Tableau DG Hebdo")], limit=1)
    if board:
        board.write({"config_ids": [(6, 0, configs.ids)]})
        return board
    return Board.create({
        "name": "Tableau DG Hebdo",
        "sequence": 5,
        "config_ids": [(6, 0, configs.ids)],
        "company_id": company.id,
    })


def run(env):  # odoo shell fournit env
    try:
        _ensure_modules(env)
        _check_models(env)
    except RuntimeError as err:
        print(f'Impossible de créer les données DT : {err}')
        return
    company = env.company

    category_hld = _ensure_category(env, "HLD", sequence=5)
    tag_archi = _ensure_tag(env, "Architecture", color=2)

    project = _create_demo_project(env, company)
    dossier = _create_demo_dossier(env, project, company)
    expense = _create_demo_expense(env, project, company)
    document = _create_demo_document(env, project, category_hld, tag_archi, company)

    configs = env["kondro.dt.report.config"].browse()
    required_codes = {"KPI_PROJETS_EN_COURS", "KPI_DEPENSES_EN_ATTENTE", "KPI_RISQUES_CRITIQUES"}
    missing = required_codes - set(env["kondro.dt.report.config"].search([]).mapped("code"))
    if missing:
        configs = _create_demo_kpis(env, company)
    else:
        configs = env["kondro.dt.report.config"].search([("code", "in", list(required_codes))])

    board = _ensure_board(env, configs, company)

    print(
        "Données DT ➜ projet=%s, dossier=%s, dépense=%s, document=%s, board=%s" %
        (project.name, dossier.name, expense.name, document.name, board.name)
    )


if __name__ == "__main__":
    run(env)  # type: ignore[name-defined]
