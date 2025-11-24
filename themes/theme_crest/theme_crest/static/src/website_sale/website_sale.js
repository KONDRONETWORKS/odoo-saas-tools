/** @odoo-module **/
import {WebsiteSale} from "@website_sale/js/website_sale";

WebsiteSale.include({
    events: Object.assign({}, WebsiteSale.prototype.events, {
        "click .o_wsale_product_btn_bits .a-submit": "async _onClickAdd",
    }),
    _onChangeCombination: function(ev, $parent, combination) {
        this._super.apply(this, arguments);
        this.$el.find('.p_sku_bits').html(arguments[2].product_sku)
    }
});
