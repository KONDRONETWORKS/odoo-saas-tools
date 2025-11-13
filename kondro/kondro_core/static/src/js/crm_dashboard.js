/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class KondroCRMDashboard extends Component {
    static template = "kondro_core.CRMDashboard";

    setup() {
        this.rpc = useService("rpc");
        this.state = useState({
            loading: true,
            data: null,
        });
        
        onMounted(() => {
            this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            this.state.loading = true;
            // Charger les statistiques depuis le serveur
            const data = await this.rpc("/web/dataset/call_kw", {
                model: "kondro.project",
                method: "get_crm_stats",
                args: [],
                kwargs: {},
            });
            this.state.data = data || {};
        } catch (error) {
            console.error("Erreur lors du chargement des données CRM:", error);
        } finally {
            this.state.loading = false;
        }
    }
}

registry.category("actions").add("kondro_crm_dashboard", KondroCRMDashboard);

