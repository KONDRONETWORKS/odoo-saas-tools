mods = env['ir.module.module'].search([('name','like','kondro_dt%')])
print([(m.name, m.state) for m in mods])
