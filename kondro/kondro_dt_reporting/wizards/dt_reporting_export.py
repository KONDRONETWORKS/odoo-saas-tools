# -*- coding: utf-8 -*-
import io
import csv
import base64

from odoo import fields, models, _


class KondroDtReportingExportWizard(models.TransientModel):
    _name = "kondro.dt.reporting.export.wizard"
    _description = "Assistant d'export KPI DT"

    date_from = fields.Date(string="Date de début")
    date_to = fields.Date(string="Date de fin")
    config_ids = fields.Many2many("kondro.dt.report.config", string="KPIs")
    include_details = fields.Boolean(string="Inclure détails", default=False)
    data_file = fields.Binary(readonly=True)
    filename = fields.Char(readonly=True)

    def action_export(self):
        self.ensure_one()
        configs = self.config_ids or self.env["kondro.dt.report.config"].search([])
        snapshots_domain = [("config_id", "in", configs.ids)]
        if self.date_from:
            snapshots_domain.append(("period_end", ">=", self.date_from))
        if self.date_to:
            snapshots_domain.append(("period_end", "<=", self.date_to))
        snapshots = self.env["kondro.dt.kpi.snapshot"].search(snapshots_domain, order="period_end desc")

        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow([
            "Code",
            "Nom",
            "Période début",
            "Période fin",
            "Valeur",
            "Delta",
            "Delta %",
            "Cible",
            "Unité",
        ])
        for snap in snapshots:
            writer.writerow([
                snap.code,
                snap.name,
                snap.period_start,
                snap.period_end,
                f"{snap.value:.2f}",
                f"{snap.delta_value:.2f}",
                f"{snap.delta_percent:.2f}",
                f"{snap.target_value:.2f}" if snap.target_value else "",
                snap.unit_label or "",
            ])
        content = buffer.getvalue().encode()
        buffer.close()

        filename = "kpi_dt_export.csv"
        self.write({
            "data_file": base64.b64encode(content),
            "filename": filename,
        })
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{self.id}?model={self._name}&field=data_file&download=true&filename={filename}",
            "target": "self",
        }
