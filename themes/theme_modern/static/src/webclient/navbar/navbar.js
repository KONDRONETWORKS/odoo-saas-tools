/** @odoo-module **/

/**********************************************************************************
 * 
**********************************************************************************/

import { patch } from '@web/core/utils/patch';
import { NavBar } from '@web/webclient/navbar/navbar';
import { AppsMenu } from "@theme_modern/webclient/appsmenu/appsmenu";
import { AppsSearch } from "@theme_modern/webclient/appssearch/appssearch";
import { useRef } from "@odoo/owl";
import { useBus } from "@web/core/utils/hooks";

patch(NavBar.prototype, {
    setup() {
        super.setup(...arguments);
        this.appsMenuRef = useRef("appsMenu");
        useBus(this.env.bus, "ACTION_MANAGER:UI-UPDATED", () => {
            if (this.appsMenuRef.comp) {
                this.appsMenuRef.comp.close();
            }
        });
    },

	getAppsMenuItems(apps) {
		return apps.map((menu) => {
			const appsMenuItem = {
				id: menu.id,
				name: menu.name,
				xmlid: menu.xmlid,
				appID: menu.appID,
				actionID: menu.actionID,
				href: this.getMenuItemHref(menu),
				action: () => this.menuService.selectMenu(menu),
			};
		    if (menu.webIconData) {
		        const prefix = (
		        	menu.webIconData.startsWith('P') ? 
	    			'data:image/svg+xml;base64,' : 
					'data:image/png;base64,'
	            );
		        appsMenuItem.webIconData = (
	    			menu.webIconData.startsWith('data:image') ? 
					menu.webIconData : 
					prefix + menu.webIconData.replace(/\s/g, '')
	            );
		    }
			return appsMenuItem;
		});
    },
});

patch(NavBar, {
    components: {
        ...NavBar.components,
        AppsMenu,
        AppsSearch,
    },
});
