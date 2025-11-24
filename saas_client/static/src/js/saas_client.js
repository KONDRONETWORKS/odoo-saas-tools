/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SaasDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({
            announcement: null,
            announcementUrl: null,
        });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        try {
            const result = await this.orm.call("ir.config_parameter", "search_read", [
                [['key', 'in', ['saas_client.ab_location', 'saas_client.ab_register']]],
                ['key', 'value']
            ]);

            let announcementUrl = null;
            let announcementRegister = null;

            result.forEach(r => {
                if (r.key === 'saas_client.ab_location') {
                    announcementUrl = r.value;
                } else if (r.key === 'saas_client.ab_register') {
                    announcementRegister = r.value;
                }
            });

            if (announcementUrl) {
                this.state.announcement = "New updates are available!";
                this.state.announcementUrl = announcementUrl;
            }
        } catch (e) {
            console.error("Failed to load SaaS data", e);
        }
    }

    async onRefresh() {
        await this.loadData();
    }

    onContactSupport() {
        this.action.doAction({
            type: "ir.actions.act_url",
            url: "mailto:support@example.com",
            target: "self",
        });
    }
}

SaasDashboard.template = "saas_client.SaasDashboard";

registry.category("actions").add("saas_client.dashboard", SaasDashboard);
