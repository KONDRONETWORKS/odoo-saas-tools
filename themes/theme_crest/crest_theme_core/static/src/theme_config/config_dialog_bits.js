/** @odoo-module **/

import { WebsiteDialog } from '@website/components/dialog/dialog';
import { useService } from '@web/core/utils/hooks';
import { _t } from "@web/core/l10n/translation";
import { Component, useState, onWillStart } from "@odoo/owl";

export class ThemeConfig extends Component {
    setup() {
        this.orm = useService('orm');
        this.website = useService('website');
        this.title = _t("Theme Configuration");
        this.primaryTitle = _t("Save");
        this.size = 'lg';
        this.updatedValue = {};
        this.state = useState({
            crm_installed: false,
            active_tab: 'general',
            config_value: {
                h_lang_select: true, h_pricelist_select: true, h_offer_line: true, b2b_mode: false, pricelist_offer_timer: false,
                card_cart_btn: true, card_compare_btn: false, card_quickview_btn: false, card_wishlist_btn: false, card_product_style: 'card_product_style_1', image_on_hover_style: 'hover_style_1', h_category_menu: false,
                card_border_style: 'square', card_rattings: false, card_stock_lbl: false, card_product_lbl: false,
                filters_design: 'style-1', filter_in_sidebar: false, filter_product_count: true, shop_category_style: 'style-1', h_cart_popup : true,card_product_terms_and_condition:false,
                shop_category_banner: true, product_zoom: true, product_inquiry: false, product_offers: false,
                product_sticky_view: true, card_hover_image: true, enable_loadmore_products: true, product_review_tab: false,
                show_category_in_filter: true, show_stock_avail_filter: true, show_ratings_filter: true, enable_lazyload_image: true,
                product_brand_detail: true, product_tags: true, product_sku: true, product_sharing: true, product_conditions: true,
                show_sticky_product_buy_notify:true, select_when_notify_show:'on_add_to_cart', show_alternative_products:false,
                show_accessory_products: false, navbar_hover_effect: 'navbar_hover_effect_1',
            }
        });
        onWillStart(async () => {
            // get config data
            var theme_configuration = await this.orm.call("theme.configuration", "get_theme_config", [false, this.website.currentWebsite.id]);
            for (var key in theme_configuration[0]) {
                if (Object.keys(this.state.config_value).includes(key)) {
                    this.state.config_value[key] = theme_configuration[0][key];
                }
            }
            this.state.crm_installed = theme_configuration[0]?.crm_installed;
        });
    }
    onChangeValue(ev) {
        var field = ev.currentTarget.name;
        if (ev.currentTarget.type == 'checkbox') {
            var field_value = ev.currentTarget.checked;
        } else if (['input', 'select-one'].includes(ev.currentTarget.type)) {
            var field_value = ev.currentTarget.value;
        }
        if (field) {
            this.state.config_value[field] = field_value;
        }
    }
    async onActivateCRM(ev) {
        this.env.services.ui.block();
        var res = await this.orm.call("theme.configuration", "install_crm_module", [[]]);
        if (res) {
            this.state.crm_installed = true;
            this.env.services.ui.unblock();
        }
        else {
            this.state.crm_installed = false;
            this.env.services.ui.unblock();
        }
    }
    async saveConfig() {
        await this.orm.call("theme.configuration", "save_theme_configuration", [[], this.website.currentWebsite.id, this.state.config_value]);
        window.location.reload();
    }
}

ThemeConfig.template = 'ConfigDialogBits';
ThemeConfig.components = { WebsiteDialog }; 
