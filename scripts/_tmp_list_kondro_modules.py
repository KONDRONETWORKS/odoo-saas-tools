modules = env['ir.module.module'].search([('name','like','kondro%')])
print(sorted([(m.name, m.state) for m in modules]))
