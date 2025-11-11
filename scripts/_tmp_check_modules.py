from pprint import pprint
mods = env['ir.module.module'].search([('name','in',['kondro_dt_hub','kondro_dt_projects','kondro_dt_workflow','kondro_dt_docs','kondro_dt_reporting'])])
print({m.name: m.state for m in mods})
