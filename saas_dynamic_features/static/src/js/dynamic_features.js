/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import publicWidget from "@web/legacy/js/public/public_widget";

// Existing Public Widgets
publicWidget.registry.DynamicHero = publicWidget.Widget.extend({
    selector: '.s_dynamic_hero',
    start: function () {
        this._super.apply(this, arguments);
        console.log("Dynamic Hero initialized");
    },
});

publicWidget.registry.ThreeDFeatures = publicWidget.Widget.extend({
    selector: '.s_3d_features',
    start: function () {
        this._super.apply(this, arguments);
    },
});

// New App Dashboard Component
export class AppDashboard extends Component {
    setup() {
        this.actionService = useService("action");
        this.menuService = useService("menu");
        this.state = useState({
            apps: []
        });

        onWillStart(async () => {
            const menu = this.menuService.getMenuAsTree("root");
            this.state.apps = this._processMenu(menu);
        });
    }

    _processMenu(menu) {
        // Mock data for visual demonstration based on the image
        // In a real scenario, we would map the actual menu items
        return [
            { id: 1, name: 'Discuss', icon: 'fa-comments', colorClass: 'bg-gradient-primary', action: 'mail.action_discuss' },
            { id: 2, name: 'Calendar', icon: 'fa-calendar', colorClass: 'bg-gradient-warning', action: 'calendar.action_calendar_event' },
            { id: 3, name: 'CRM', icon: 'fa-handshake-o', colorClass: 'bg-gradient-info', action: 'crm.crm_lead_action_pipeline' },
            { id: 4, name: 'Sales', icon: 'fa-line-chart', colorClass: 'bg-gradient-success', action: 'sale.action_quotations_with_onboarding' },
            { id: 5, name: 'Dashboards', icon: 'fa-th-large', colorClass: 'bg-gradient-danger', action: 'spreadsheet_dashboard.dashboard_action' },
            { id: 6, name: 'Accounting', icon: 'fa-pie-chart', colorClass: 'bg-gradient-primary', action: 'account.action_move_out_invoice_type' },
            { id: 7, name: 'Project', icon: 'fa-check-square-o', colorClass: 'bg-gradient-success', action: 'project.open_view_project_all' },
            { id: 8, name: 'Website', icon: 'fa-globe', colorClass: 'bg-gradient-warning', action: 'website.action_website_configuration' },
        ];
    }

    openApp(app) {
        if (app.action) {
            this.actionService.doAction(app.action);
        }
    }
}

AppDashboard.template = "saas_dynamic_features.AppDashboard";

// Register as a client action
registry.category("actions").add("saas_dynamic_features.dashboard", AppDashboard);
