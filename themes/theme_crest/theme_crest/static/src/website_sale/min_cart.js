/** @odoo-module **/

import { Dialog } from '@web/core/dialog/dialog';
import publicWidget from "@web/legacy/js/public/public_widget";
import '@website_sale/js/website_sale';
import '@website_sale_wishlist/js/website_sale_wishlist';
import '@website_sale_comparison/js/website_sale_comparison';
import { _t } from '@web/core/l10n/translation';
import { debounce } from "@web/core/utils/timing";
import VariantMixin from '@website_sale/js/sale_variant_mixin';
import { rpc } from "@web/core/network/rpc";
import { markup, onWillStart, onMounted, useRef } from "@odoo/owl";

export class MiniCartProductBits extends Dialog {
    static components = { Dialog };
    static template = "theme_crest.MiniCartDialog";
    static props = {
        ...Dialog.props,
        widget: { type: Object, optional: true },
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
        this.MiniCartDialog = useRef("minicartdialog");
        onWillStart(this.onWillStart);
        onMounted(this.onMounted);
    }
    async onWillStart() {
        let res = await rpc('/get_mini_cart', {});
        this.$content = res?.mini_cart_bits;
    }
    onMounted() {

        if (this.props.widget) {
            this.props.widget.trigger_up("widgets_start_request", {
                $target: $(this.MiniCartDialog.el),
            });
        }
    }
}
const MiniCartProductWidgetBits = publicWidget.Widget.extend({
    selector: ".mini-cart-style-bits",
    events: ({
        'click a.js_add_cart_json': '_onUpdateQty',
        'change input.js_quantity[data-product-id]': '_onChangeQty',
        'click .js_delete_product': '_onClickRemoveProduct',
        'click .clr_cart_bits': '_ClearCartBits',
        'click a.js_add_suggested_products': '_onClickSuggestedProduct',
    }),
    start(ele, otps) {
        this._super(...arguments);
        this._changeCartQuantity = debounce(this._changeCartQuantity.bind(this), 500);
    },
    willStart: async function () {

        var template = rpc('/get_mini_cart', {});
        return Promise.all([this._super(...arguments), template]).then((response) => {
            this.$el = $(response[1]['mini_cart_bits']);
        });
    },
    _onUpdateQty: function (ev) {
        VariantMixin.onClickAddCartJSON(ev);
    },
    _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs, productList, target) {
        $input.data('update_change', true);
        rpc("/shop/cart/update_json", {
            line_id: line_id,
            product_id: parseInt($input.data('product-id'), 10),
            set_qty: value,
            display: true,
        }).then((data) => {
            $input.data('update_change', false);
            if (!data.cart_quantity) {
                $(target).parents().find(('.js_delete_product')).trigger('click');
            }
            else {
                $input.val(data.quantity);
                $('.js_quantity[data-line-id=' + line_id + ']').val(data.quantity).text(data.quantity);
                this.$el.find(".qty_bits").empty().append(data.cart_quantity);
                this.UpdateCartNavBar(data);
            }
        });
    },
    _onChangeQty: function (ev) {
        var $input = $(ev.currentTarget);
        if ($input.data('update_change')) {
            return;
        }
        var value = parseInt($input.val() || 0, 10);
        var $dom = $input.closest('tr');
        var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
        var line_id = parseInt($input.data('line-id'), 10);
        var productIDs = [parseInt($input.data('product-id'), 10)];
        var productList = $(ev.currentTarget).data('productList')
        if (productList && productList.includes(Number($(ev.currentTarget).data('productId')))) {
            var line_class = '.sale_line_' + Number($(ev.currentTarget).data('productId'))
            $(line_class).val(Number($(line_class).val()) + 1).trigger('change')
        }
        else {
            this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs, productList, ev.currentTarget);
        }
    },
    _onClickRemoveProduct: function (ev) {
        ev.preventDefault();
        if ($('.mini-cart-products-bits').find('li.mc-media-bits').length == 1) {
            this._ClearCartBits();
        }
        else {
            $(ev.currentTarget).siblings().find('.js_quantity').val(0).trigger("change");
        }
    },
    _ClearCartBits: function () {
        rpc('/as_clear_cart', {}).then((response) => {
            $(".cart_body").replaceWith(response['empty_mini_cart']);
        });
        this.$el.find(".qty_bits").empty().append(0);
        $(".my_cart_quantity").text("0")
        $(".clr_cart_bits").remove()
    },

    UpdateCartNavBar(data) {
        sessionStorage.setItem('website_sale_cart_quantity', data.cart_quantity);
        $(".my_cart_quantity")
            .parents('li.o_wsale_my_cart').removeClass('d-none').end().toggleClass('d-none', data.cart_quantity === 0)
            .addClass('o_mycart_zoom_animation').delay(300)
            .queue(function () {
                $(this)
                    .attr('title', data.warning)
                    .text(data.cart_quantity || '')
                    .removeClass('o_mycart_zoom_animation')
                    .dequeue();
            });
        $("#cart_total").replaceWith(data['website_sale.total']);

        rpc('/get_mini_cart', {}).then((response) => {
            $(".mini-main-cart-bits").replaceWith(response['mini_cart_lines_bits']);
        });
        if (data.cart_ready) {
            document.querySelector("a[name='website_sale_main_button']")?.classList.remove('disabled');
        } else {
            document.querySelector("a[name='website_sale_main_button']")?.classList.add('disabled');
        }
    },
    _onClickSuggestedProduct: function (ev) {
        $(ev.currentTarget).prev('input').val(1).trigger('change');
    },
})
publicWidget.registry.MiniCartProductWidgetBits = MiniCartProductWidgetBits;


publicWidget.registry.MiniCartBits = publicWidget.Widget.extend({
    selector: "header",
    events: {
        'click .min-cart-bits': '_show_mini_cart',
    },
    _show_mini_cart: function (ev) {
        ev.preventDefault();
        const miniCart = new publicWidget.registry.MiniCartProductWidgetBits(this, {});
        
        this.call("dialog", "add", MiniCartProductBits, {
            widget: miniCart,
        });
    },
});