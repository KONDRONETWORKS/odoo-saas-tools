/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";

export const themeManagerService = {
    dependencies: ["orm"],
    async start(env, { orm }) {
        const applyTheme = async () => {
            const params = await orm.searchRead(
                "ir.config_parameter",
                [["key", "like", "saas_portal.theme_%"]],
                ["key", "value"]
            );

            console.log("[ThemeManager] Fetched params:", params);

            const root = document.documentElement;
            params.forEach((param) => {
                const cssVar = "--" + param.key.replace("saas_portal.", "").replace(/_/g, "-");
                let value = param.value;

                // Add px to specific properties if they are just numbers
                if (['theme-button-radius', 'theme-card-radius', 'theme-input-radius', 'theme-font-size-base'].includes(cssVar.replace('--', ''))) {
                    if (!isNaN(value) && !value.endsWith('px')) {
                        value += 'px';
                    }
                }

                console.log(`[ThemeManager] Setting ${cssVar} to ${value}`);
                root.style.setProperty(cssVar, value);
            });
        };

        await applyTheme();
    },
};

registry.category("services").add("theme_manager", themeManagerService);
