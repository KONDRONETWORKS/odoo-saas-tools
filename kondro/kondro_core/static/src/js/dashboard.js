/** @odoo-module **/

import { Component, onMounted, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

class KondroDashboard extends Component {
    static template = "kondro_dashboard.DashboardView";
    
    setup() {
        this.dashboardData = useState({});
        this.loading = useState(true);
        
        onMounted(() => {
            this.loadDashboardData();
        });
    }
    
    async loadDashboardData() {
        try {
            this.loading = true;
            
            // Charger les données du tableau de bord
            const data = await this.env.services.rpc({
                model: 'kondro.dashboard.data',
                method: 'get_overall_stats',
                args: []
            });
            
            this.dashboardData = data;
            this.updateDashboard();
            
        } catch (error) {
            console.error('Erreur lors du chargement des données:', error);
        } finally {
            this.loading = false;
        }
    }
    
    updateDashboard() {
        // Mettre à jour les métriques Projets (unifiés)
        this.updateElement('projects-total', this.dashboardData.projects?.total || 0);
        this.updateElement('projects-in-progress', this.dashboardData.projects?.in_progress || 0);
        this.updateElement('projects-completed', this.dashboardData.projects?.completed || 0);
        
        // Mettre à jour la trésorerie
        this.updateElement('treasury-balance', this.formatCurrency(this.dashboardData.treasury?.balance || 0));
        this.updateElement('treasury-income', this.formatCurrency(this.dashboardData.treasury?.total_income || 0));
        this.updateElement('treasury-expense', this.formatCurrency(this.dashboardData.treasury?.total_expense || 0));
        
        // Mettre à jour les dossiers commerciaux
        this.updateElement('commercial-total', this.dashboardData.commercial?.total_dossiers || 0);
        this.updateElement('commercial-active', this.dashboardData.commercial?.active_dossiers || 0);
        this.updateElement('commercial-won', this.dashboardData.commercial?.won_dossiers || 0);
        
        // Mettre à jour les dépenses
        this.updateElement('expense-total', this.dashboardData.expenses?.total_requests || 0);
        this.updateElement('expense-pending', this.dashboardData.expenses?.pending || 0);
        this.updateElement('expense-approved', this.dashboardData.expenses?.approved || 0);
        this.updateElement('expense-amount', this.formatCurrency(this.dashboardData.expenses?.total_amount || 0));
        
        // Mettre à jour la barre de progression (projets unifiés)
        this.updateProgressBar('projects-progress', 'projects-progress-text', this.calculateProgress(this.dashboardData.projects));
    }
    
    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
    
    updateProgressBar(barId, textId, percentage) {
        const bar = document.getElementById(barId);
        const text = document.getElementById(textId);
        
        if (bar && text) {
            bar.style.width = `${percentage}%`;
            text.textContent = `${Math.round(percentage)}%`;
        }
    }
    
    calculateProgress(projectData) {
        if (!projectData || projectData.total === 0) return 0;
        
        const completed = projectData.completed || 0;
        const inProgress = projectData.in_progress || 0;
        
        // Calculer le pourcentage basé sur les projets terminés et en cours
        return (completed / projectData.total) * 100 + (inProgress / projectData.total) * 50;
    }
    
    formatCurrency(amount) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'XOF',
            minimumFractionDigits: 0
        }).format(amount);
    }
}

// Enregistrer le composant
registry.category("views").add("kondro_core.dashboard", KondroDashboard);

export { KondroDashboard };
