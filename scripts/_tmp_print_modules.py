modules = env['ir.module.module'].search([])
print('count', len(modules))
print(modules.filtered(lambda m: m.name in ['test_mod','kondro_dt_hub']).mapped(lambda m: (m.name, m.state)))
