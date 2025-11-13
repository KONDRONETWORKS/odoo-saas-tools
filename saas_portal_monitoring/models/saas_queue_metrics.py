from datetime import timedelta
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaasPortalQueueMetric(models.Model):
    _name = "saas_portal.queue.metric"
    _description = "SaaS Queue Job Metrics"
    _order = "timestamp desc, channel"

    channel = fields.Char(required=True, index=True)
    pending_count = fields.Integer(string="Jobs en attente", default=0)
    started_count = fields.Integer(string="Jobs en cours", default=0)
    failed_count = fields.Integer(string="Jobs en erreur", default=0)
    oldest_pending_minutes = fields.Integer(string="Ancienneté max (min)", default=0)
    severity = fields.Selection(
        [
            ("ok", "OK"),
            ("warning", "Avertissement"),
            ("critical", "Critique"),
        ],
        default="ok",
        index=True,
    )
    timestamp = fields.Datetime(default=fields.Datetime.now, required=True, index=True)

    @api.model
    def _get_thresholds(self):
        icp = self.env["ir.config_parameter"].sudo()
        return {
            "pending_warning": int(icp.get_param("saas_portal.queue.warning_pending", 20)),
            "pending_critical": int(icp.get_param("saas_portal.queue.critical_pending", 50)),
            "failed_warning": int(icp.get_param("saas_portal.queue.warning_failed", 1)),
            "failed_critical": int(icp.get_param("saas_portal.queue.critical_failed", 5)),
            "oldest_warning": int(icp.get_param("saas_portal.queue.warning_oldest_min", 10)),
            "oldest_critical": int(
                icp.get_param("saas_portal.queue.critical_oldest_min", 30)
            ),
        }

    def _compute_severity(self, values, thresholds):
        severity = "ok"
        pending = values["pending_count"]
        failed = values["failed_count"]
        oldest = values["oldest_pending_minutes"]

        if (
            pending >= thresholds["pending_critical"]
            or failed >= thresholds["failed_critical"]
            or oldest >= thresholds["oldest_critical"]
        ):
            severity = "critical"
        elif (
            pending >= thresholds["pending_warning"]
            or failed >= thresholds["failed_warning"]
            or oldest >= thresholds["oldest_warning"]
        ):
            severity = "warning"
        return severity

    @api.model
    def collect_queue_metrics(self):
        """Collect queue statistics per channel."""
        # Vérifier si le module queue_job est installé
        if not self.env['ir.module.module'].sudo().search([
            ('name', '=', 'queue_job'),
            ('state', '=', 'installed')
        ]):
            _logger.warning("Module queue_job non installé. Les métriques de queue ne peuvent pas être collectées.")
            return 0
        
        Job = self.env["queue.job"].sudo()
        now = fields.Datetime.now()
        thresholds = self._get_thresholds()

        channels = [
            data["channel"]
            for data in Job.read_group([], ["channel"], ["channel"])
            if data["channel"]
        ]
        if not channels:
            channels = ["root"]

        records = []
        for channel in channels:
            pending_domain = [
                ("channel", "=", channel),
                ("state", "in", ["pending", "enqueued"]),
            ]
            started_domain = [
                ("channel", "=", channel),
                ("state", "=", "started"),
            ]
            failed_domain = [
                ("channel", "=", channel),
                ("state", "=", "failed"),
            ]

            pending_count = Job.search_count(pending_domain)
            started_count = Job.search_count(started_domain)
            failed_count = Job.search_count(failed_domain)

            oldest_minutes = 0
            if pending_count:
                oldest_job = Job.search(
                    pending_domain,
                    limit=1,
                    order="date_enqueued asc, date_created asc",
                )
                if oldest_job:
                    reference_date = oldest_job.date_enqueued or oldest_job.date_created
                    if reference_date:
                        delta = now - reference_date
                        oldest_minutes = int(delta.total_seconds() // 60)

            values = {
                "channel": channel,
                "pending_count": pending_count,
                "started_count": started_count,
                "failed_count": failed_count,
                "oldest_pending_minutes": oldest_minutes,
                "timestamp": now,
            }
            values["severity"] = self._compute_severity(values, thresholds)
            records.append(values)

        created_records = self.create(records) if records else self.browse()
        if created_records:
            self._send_alerts(created_records)
        return len(created_records)

    def _send_alerts(self, metrics):
        Mail = self.env["mail.mail"].sudo()
        admins = self.env.ref("base.group_system").users.filtered("email")
        if not admins:
            return
        email_to = ",".join(admins.mapped("email"))
        for metric in metrics:
            if metric.severity == "ok" or not metric._should_notify():
                continue
            subject = self.env[
                "ir.translation"
            ]._get_source(
                None,
                None,
                self.env.lang,
                "Alerte Queue Jobs (%s) - %s" % (metric.severity.upper(), metric.channel),
            )
            body = """
                <p><b>Canal :</b> {channel}</p>
                <p><b>Gravité :</b> {severity}</p>
                <p><b>Jobs en attente :</b> {pending}</p>
                <p><b>Jobs en cours :</b> {started}</p>
                <p><b>Jobs en erreur :</b> {failed}</p>
                <p><b>Ancienneté max :</b> {oldest} minutes</p>
            """.format(
                channel=metric.channel,
                severity=metric.severity.upper(),
                pending=metric.pending_count,
                started=metric.started_count,
                failed=metric.failed_count,
                oldest=metric.oldest_pending_minutes,
            )
            Mail.create(
                {
                    "subject": subject,
                    "body_html": body,
                    "email_to": email_to,
                }
            )

    def _should_notify(self):
        window = self.timestamp - timedelta(minutes=30)
        previous = self.search(
            [
                ("channel", "=", self.channel),
                ("id", "!=", self.id),
                ("timestamp", ">=", window),
            ],
            order="timestamp desc",
            limit=1,
        )
        return not previous or previous.severity != self.severity

    @api.model
    def cron_collect_queue_metrics(self):
        return self.collect_queue_metrics()

    @api.model
    def clean_old_queue_metrics(self, days=7):
        cutoff = fields.Datetime.now() - timedelta(days=days)
        old_records = self.search([("timestamp", "<", cutoff)])
        count = len(old_records)
        old_records.unlink()
        if count:
            _logger.info("Cleaned %s queue metrics older than %s days", count, days)
        return count

