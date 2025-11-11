from datetime import date, timedelta

env.cr.execute("SAVEPOINT dt_suite")
try:
    partner = env['res.partner'].create({
        'name': 'Client QA DT',
        'company_type': 'company',
        'email': 'client.qa@example.com',
    })

    dept = env['hr.department'].create({'name': 'QA DT Test'})
    employee = env['hr.employee'].create({
        'name': 'QA DT Employé',
        'work_email': 'qa.dt@example.com',
        'department_id': dept.id,
    })

    project = env['kondro.project'].create({
        'name': 'Projet QA DT',
        'client_id': partner.id,
        'technical_summary': 'Projet généré pour tests automatisés',
        'deadline_date': date.today() + timedelta(days=30),
    })

    matrix = env['kondro.dt.workflow.matrix'].create({
        'name': 'Matrice QA',
        'process_type': 'internal_expense',
        'department_id': dept.id,
        'project_id': project.id,
        'line_ids': [(0, 0, {
            'role_type': 'accountable',
            'user_id': env.ref('base.user_admin').id,
        })],
    })

    expense = env['kondro.expense.request'].create({
        'name': 'Test dépense DT',
        'expense_type': 'internal',
        'department_id': dept.id,
        'employee_id': employee.id,
        'estimated_amount': 500000,
        'dt_matrix_id': matrix.id,
        'dt_requires_validation': True,
    })
    expense.action_submit()
    expense.action_dt_validate()
    expense.action_validate()
    expense.action_approve()

    document_category = env['kondro.dt.document.category'].create({'name': 'Specs'})
    document = env['kondro.dt.document'].create({
        'name': 'Spec QA',
        'version': '1.0',
        'project_id': project.id,
        'category_id': document_category.id,
        'owner_id': env.ref('base.user_admin').id,
    })
    document.action_submit_review()
    document.action_approve()

    cron = env.ref('kondro_dt_reporting.cron_kondro_dt_reporting_daily')
    print('Cron DT reporting actif:', cron.active)

    print("✔ Scénario DT exécuté sans erreur.")
finally:
    env.cr.execute("ROLLBACK TO SAVEPOINT dt_suite")
