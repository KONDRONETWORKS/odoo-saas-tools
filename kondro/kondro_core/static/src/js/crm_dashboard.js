/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@owl/core/component";

export class KondroCRMDashboard extends Component {
    setup() {
        // Initialiser le dashboard
        this.loadDashboardData();
    }

    async loadDashboardData() {
        // Charger les statistiques depuis le serveur
        // TODO: Implémenter l'appel RPC pour récupérer les données
    }
}

KondroCRMDashboard.template = "kondro_core.CRMDashboard";

registry.category("actions").add("kondro_crm_dashboard", KondroCRMDashboard);

