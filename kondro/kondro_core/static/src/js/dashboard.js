/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class KondroDashboard extends Component {
    static template = "kondro_core.DashboardView";

    setup() {
        this.rpc = useService("rpc");
        this.action = useService("action");
        
        this.state = useState({
            loading: true,
            branding: {
                title: '',
                subtitle: '',
                company_name: '',
                currency_code: 'XOF',
                currency_locale: 'fr-FR',
            },
            quickActions: [],
            projects: { total: 0, in_progress: 0, completed: 0 },
            treasury: { balance: 0, total_income: 0, total_expense: 0 },
            commercial: { total_dossiers: 0, active_dossiers: 0, won_dossiers: 0 },
            expenses: { total_requests: 0, pending: 0, approved: 0, total_amount: 0 },
        });

        onMounted(() => {
            this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        try {
            this.state.loading = true;

            const data = await this.rpc("/web/dataset/call_kw", {
                model: 'kondro.dashboard.data',
                method: 'get_overall_stats',
                args: [],
                kwargs: {},
            });

            this._applyData(data || {});
        } catch (error) {
            console.error('Erreur lors du chargement des données:', error);
        } finally {
            this.state.loading = false;
        }
    }

    _applyData(data) {
        const normalised = {
            projects: {
                total: data.projects?.total || 0,
                in_progress: data.projects?.in_progress || 0,
                completed: data.projects?.completed || 0,
            },
            treasury: {
                balance: data.treasury?.balance || 0,
                total_income: data.treasury?.total_income || 0,
                total_expense: data.treasury?.total_expense || 0,
            },
            commercial: {
                total_dossiers: data.commercial?.total_dossiers || 0,
                active_dossiers: data.commercial?.active_dossiers || 0,
                won_dossiers: data.commercial?.won_dossiers || 0,
            },
            expenses: {
                total_requests: data.expenses?.total_requests || 0,
                pending: data.expenses?.pending || 0,
                approved: data.expenses?.approved || 0,
                total_amount: data.expenses?.total_amount || 0,
            },
            branding: {
                title: data.branding?.title || data.branding?.company_name || this.env.company?.name || '',
                subtitle: data.branding?.subtitle || '',
                company_name: data.branding?.company_name || '',
                currency_code: data.branding?.currency_code || 'XOF',
                currency_locale: data.branding?.currency_locale || (this.env.user?.lang ?? 'fr-FR'),
            },
            quickActions: Array.isArray(data.quick_actions) ? data.quick_actions : [],
        };

        Object.assign(this.state, normalised);
    }

    get projectsProgress() {
        const { total, completed, in_progress } = this.state.projects;
        if (!total) {
            return 0;
        }
        return (completed / total) * 100 + (in_progress / total) * 50;
    }

    openAction(action) {
        if (!action || !action.action_id) {
            return;
        }
        this.action.doAction(action.action_id);
    }

    calculateProgress(projectData) {
        if (!projectData || projectData.total === 0) return 0;

        const completed = projectData.completed || 0;
        const inProgress = projectData.in_progress || 0;

        return (completed / projectData.total) * 100 + (inProgress / projectData.total) * 50;
    }

    formatCurrency(amount) {
        const locale = this.state.branding.currency_locale || 'fr-FR';
        const currency = this.state.branding.currency_code || 'XOF';
        let formatter;
        try {
            formatter = new Intl.NumberFormat(locale, {
            style: 'currency',
            currency,
            minimumFractionDigits: 0,
        });
        } catch (error) {
            formatter = new Intl.NumberFormat('fr-FR', {
                style: 'currency',
                currency: 'XOF',
                minimumFractionDigits: 0,
            });
        }
        return formatter.format(amount || 0);
    }

    get formattedProjectsProgress() {
        return Math.round(this.projectsProgress);
    }
}

registry.category("actions").add("kondro_core.dashboard", KondroDashboard);

export { KondroDashboard };
