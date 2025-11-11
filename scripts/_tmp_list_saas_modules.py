mods = env['ir.module.module'].search([('name','ilike','saas')])
print([(m.name, m.state) for m in mods][:10])
