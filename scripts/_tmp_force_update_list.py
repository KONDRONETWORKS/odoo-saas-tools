modules = env['ir.module.module']
modules.update_list()
env.cr.commit()
print('dt modules', env['ir.module.module'].search([('name','like','kondro_dt%')]).mapped(lambda m: (m.name, m.state)))
