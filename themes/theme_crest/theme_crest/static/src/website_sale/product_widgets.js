/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { rpc } from "@web/core/network/rpc";
import { Dialog } from '@web/core/dialog/dialog';
import { markup, onWillStart, onMounted, useRef } from "@odoo/owl";
  
export class ProductDialogBits extends Dialog {
  static components = { Dialog };
  static template = "theme_crest.ProductDialog";
  static props = {
    ...Dialog.props,
    widget: { type: Object, optional: true },
    record_id: { type: Number, optional: true },
    dialog_type: { type: String, optional: true },
    title: { type: String, optional: true },
    close: { type: Function, optional: true },
  };
  static defaultProps = {
    ...Dialog.defaultProps,
    size: "xl",
  };
  setup() {
    super.setup();
    this.markup = markup;
    this.dialogTitle = this.props.title;
    this.ProductDialog = useRef("productDialog");
    onWillStart(this.onWillStart);
    onMounted(this.onMounted);
  }
  async onWillStart() {
    var self = this
    let res = await rpc('/get/dialog/data', { record_id: this.props.record_id, dialog_type: this.props.dialog_type });
    
    self.$content = res.dialog_body;
  }
  onMounted() {
    if (this.props.widget) {
      this.props.widget.trigger_up("widgets_start_request", {
        $target: $(this.ProductDialog.el),
      });
    }
  }
}


publicWidget.registry.ProductDialogBits = publicWidget.Widget.extend({
  selector: ".product_offers_container",
  events: {
    "click .off_more_detail,.attr_more_detail": "_clickMoreDetails",
  },
  _clickMoreDetails: function (ev) {
    var $targetData = $(ev.currentTarget).data(); 
    this.call("dialog", "add", ProductDialogBits, {
      widget: this,
      record_id: $targetData.record_id,
      dialog_type: $targetData.dtype,
      title: $targetData.title,
    });
  },
}); 
