/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";

export class AppsMenu extends Component {
    setup() {
        // Temporarily disabled auto-close feature to fix crash
    }
}

Object.assign(AppsMenu, {
    template: 'modern_theme.AppsMenu',
    components: { Dropdown },
});