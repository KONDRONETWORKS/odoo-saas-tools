/** @odoo-module **/

import {Dialog} from '@web/core/dialog/dialog';
import { _t } from '@web/core/l10n/translation';
import { rpc } from "@web/core/network/rpc"; 
import { markup, onWillStart, onMounted, useRef } from "@odoo/owl";

export class QuickViewdialogBits extends Dialog {
    static components = { Dialog};
    static template = "theme_crest.QuickView";
    static props = {
        ...Dialog.props,
        product_id: { type: Number, optional: true }, 
        widget: { type: Object, optional: true },
        close: { type: Function, optional: true }, 
    };
    static defaultProps = {
        ...Dialog.defaultProps,
        size: "xl",
        parent: Object,
    };
    setup() {
        super.setup();
        this.markup = markup;
        this.QuickView = useRef("quickview");
        onWillStart(this.onWillStart);
        onMounted(this.onMounted);
    }
    async onWillStart() {
        var self = this
        let res = await rpc('/product/get_quick_view_data', { product_id: this.props.product_id });
        self.$content = res; 
    }
    onMounted() { 
        this.props.widget.trigger_up("widgets_start_request", {
            $target: $(this.QuickView.el),
        });
    }
}