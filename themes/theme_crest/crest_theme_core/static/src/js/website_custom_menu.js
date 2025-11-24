/** @odoo-module **/
import { ThemeConfig } from '../theme_config/config_dialog_bits';   
import { registry } from "@web/core/registry";
 
registry.category('website_custom_menus').add('crest_theme_core.menu_theme_config_bits', {
    Component: ThemeConfig,
    isDisplayed: (env) => !!env.services.website.currentWebsite && env.services.website.isDesigner
});