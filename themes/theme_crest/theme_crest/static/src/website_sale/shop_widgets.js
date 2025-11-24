/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
const { DateTime } = luxon;
import { rpc } from "@web/core/network/rpc";
import { deserializeDateTime } from "@web/core/l10n/dates";
import VariantMixin from "@website_sale/js/sale_variant_mixin";
import wSaleUtils from "@website_sale/js/website_sale_utils";
import { Dialog } from '@web/core/dialog/dialog';
import { markup, onWillStart, onMounted, useRef } from "@odoo/owl";

const cartHandlerMixin = wSaleUtils.cartHandlerMixin;

class ProductInquiryDialogBits extends Dialog {
    static components = { Dialog };
    static template = "theme_crest.ProductInquiryDialog";
    static props = {
        ...Dialog.props,
        product_id: { type: Number, optional: true },
        widget: { type: Object, optional: true },
        product_name: { type: String, optional: true },
    };
    static defaultProps = {
        ...Dialog.defaultProps,
        size: "xl",
        parent: Object,
    };
    setup() {
        super.setup();
        this.markup = markup;
        this.ProductInquiry = useRef("productinquirydialog");
        onWillStart(this.onWillStart);
        onMounted(this.onMounted);
    }
    async onWillStart() {
        var self = this
        let res = await rpc('/form/product-inquiry-form', { product_id: this.props.product_id, product_name: this.props.product_name });
        self.$content = res.productinquiry_dialog;
    }
    onMounted() {
        this.props.widget.trigger_up("widgets_start_request", {
            $target: $(this.ProductInquiry.el),
        });
    }
}

const ProductInquiryBits = publicWidget.Widget.extend({
    selector: '.s_website_form_crm',
    events: ({
        "click .s_website_form_send_submit": "SubmitForm",
    }),
    start(ele, otps) {
        this.notification = this.bindService("notification");
        return this._super.apply(this, arguments);
    },
    SubmitForm: async function (ev) {
        ev.preventDefault(ev);
        var self = this;
        var target = this.$el.find('form');
        const $button = target.find('.s_website_form_send_submit, .s_website_form_send_submit');
        $button.addClass('disabled').attr('disabled', 'disabled');
        target.find('#s_website_form_result, #o_website_form_result').empty();
        this.form_fields = target.serializeArray();
        var form_values = {};
        this.form_fields.forEach((input) => {
            if (input.name in form_values) {
                if (Array.isArray(form_values[input.name])) {
                    form_values[input.name].push(input.value);
                } else {
                    form_values[input.name] = [form_values[input.name], input.value];
                }
            } else {
                form_values[input.name] = input.value;
            }
        });

        // Include product_id in the form submission
        form_values.product_id = target.find('[name="product_id"]').val();

        rpc('/form/crm', form_values).then((result) => {
            if (result.success) {
                form_values = {};
                $button.removeClass('disabled').removeAttr('disabled');

                this.notification.add(result.message, {
                    title: _t("Form submit"),
                    type: "success",
                });
                window.location.reload()
            } else {
                this.notification.add(result.message, {
                    title: _t("Form submit"),
                    type: "danger",
                });
                $button.removeClass('disabled').removeAttr('disabled');

            }
        }).catch((error) => {
            console.error("Error submitting form:", error);
            $button.removeClass('disabled').removeAttr('disabled');

        });
    }
});

publicWidget.registry.ProductInquiryBits = ProductInquiryBits;

publicWidget.registry.WebsiteShopBits = publicWidget.Widget.extend({
    selector: ".oe_website_sale",
    events: {
        'scroll': '_stickyCart',
        'click .attr_container .attrib_value .fa-close': '_removeFilter',
    },
    start: function () {
        // $('img.lazyload').lazyload();
    },
    _stickyCart: function (ev) {
        var self = this;
        var target = self.$target.find('.sticky-product-container')
        if (self.$target.find('.js_sale.o_wsale_product_page').length != 0) {
            const top = self.$target.find('#add_to_cart').offset().top;
            const bottom = self.$target.find('#add_to_cart').offset().top + self.$target.find('#add_to_cart').outerHeight();
            const bottom_screen = $(window).scrollTop() + $(window).innerHeight();
            const top_screen = $(window).scrollTop();
            if ((bottom_screen > top) && (top_screen < bottom)) {
                target.toggleClass("show");
            } else {
                if (top < 0) {
                    target.toggleClass("show");
                }
            }
        }
    },
    _removeFilter(ev) {
        let aval = $(ev.currentTarget).parent().data().aval;
        let fname = $(ev.currentTarget).parent().data().fname;
        let href = window.location.href;
        let urlObj = new URL(href);
        let params = urlObj.searchParams;
        let newParams = new URLSearchParams();
        params.forEach((value, key) => {
            if (['attribs', 'tags'].includes(key)) {
                aval = aval.toString();
            }
            if (!(key === fname && value === aval)) {
                newParams.append(key, value);
            }
        });
        urlObj.search = newParams.toString();
        window.location.href = urlObj.href;
    }
});

publicWidget.registry.StickyProductDetail = publicWidget.Widget.extend({
    selector: "#wrapwrap",
    events: {
        'scroll': '_stickyCart',
    },
    _stickyCart: function (ev) {
        var self = this;
        if (self.$target.find('.sticky-product-container').length) {
            const top = self.$target.find('#add_to_cart').offset().top;
            const bottom = self.$target.find('#add_to_cart').offset().top + self.$target.find('#add_to_cart').outerHeight();
            const bottom_screen = $(window).scrollTop() + $(window).innerHeight();
            const top_screen = $(window).scrollTop();
            if ((bottom_screen > top) && (top_screen < bottom)) {
                if (self.$target.find('.sticky-product-container').hasClass("show")) {
                    self.$target.find('.sticky-product-container').removeClass("show");
                }
            } else {
                if (top < 0) {
                    if (!self.$target.find('.sticky-product-container').hasClass("show")) {
                        self.$target.find('.sticky-product-container').addClass("show");
                    }
                }
            }
        }
        var offset = 450;
        var $back_to_top = $('.sticky-product-container');
        ($('#wrapwrap').scrollTop() > offset) ? $back_to_top.addClass('show') : $back_to_top.removeClass('show');
    },
});

publicWidget.registry.ShopProductCardBits = publicWidget.Widget.extend({
    selector: "form.oe_product_cart",
    events: {
        // "mouseenter .color-attr-bits": "_onMouseEnter",
        "click .color-attr-bits": "_onMouseEnter",
        "focusout .color-attr-bits": "_onMouseLeave",
        "mouseleave .color-attr-bits": "_onMouseLeave",
        "mouseenter .oe_product_image_link": "_onhoverOnImage",
        "mouseleave .oe_product_image_link": "_onhoverOutImage"
    },
    start: function () {
        this.orm = this.bindService("orm");
        return this._super.apply(this, arguments);
    },
    // events for variant image change
    _onMouseEnter: async function (event) {
        var target = $(event.currentTarget).data();
        var TargetImage = $(event.currentTarget).parents('.oe_product_image').find('.oe_product_image_img_wrapper img');
        var value_id = target.valid;
        var product_id = target.product_id;
        var prod_data = await this.orm.call("product.template", "prepare_variant_data", [[product_id], value_id]);
        TargetImage.attr('src', prod_data.product_image);
    },
    _onMouseLeave: function (event) {
        var targetData = $(event.currentTarget).data();
        var TargetImage = $(event.currentTarget).parents('.oe_product_image').find('.oe_product_image_img_wrapper img');
        TargetImage.attr('src', targetData.mainImage);
    },
    // event for product hover image change
    _onhoverOnImage: function (event) {
        var traget = $(event.currentTarget).find('img.product-img-bits');
        if (traget.data().hover_enabled) {
            let image = traget.data().hover_image;
            traget.attr('src', image);
        }
    },
    _onhoverOutImage: function (event) {
        var traget = $(event.currentTarget).find('img.product-img-bits');
        if (traget.data().hover_enabled) {
            let image = traget.data().src;
            traget.attr('src', image);
        }
    }
});

publicWidget.registry.ProductCardInquirybits = publicWidget.Widget.extend({
    selector: "#product_detail #product_details",
    events: {
        "click .btn-inquiry": "_onClickInquiry",
    },
    start: function () {
        this.orm = this.bindService("orm");
        return this._super.apply(this, arguments);
    },
    _onClickInquiry: function (ev) {
        var $targetData = $(ev.currentTarget).data();
        const ProductInquiry = new publicWidget.registry.ProductInquiryBits(this, {});
        this.call("dialog", "add", ProductInquiryDialogBits, {
            widget: ProductInquiry,
            product_id: $targetData.product_id,
            product_name: $targetData.product_name,

        });

    }
});

publicWidget.registry.PricelistOfferTimerbits = publicWidget.Widget.extend({
    selector: ".card_item_timer_bits",
    events: {},
    start: function () {
        var self = this;
        var offer_due = this.$el.find('.pl_offer_timer').data().offerends;
        this.offer_due = deserializeDateTime(offer_due);
        this.timer = setInterval(function () { self.start_countdown() }, 1000);
    },
    start_countdown() {
        var now = DateTime.now();
        const timeLeft = this.offer_due - now;
        if (timeLeft < 0) {
            clearInterval(this.timer);
            this.$el.hide();
            return;
        } else {
            this.$el.show();
        }
        // Calculate days, hours, minutes, and seconds
        const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        // Display the result
        if (!this.$el.find('.counter').hasClass('pading-space')) {
            this.$el.find('.counter').addClass('pading-space');
        }
        this.$el.find('.days').html(String(days));
        this.$el.find('.hours').html(String(hours));
        this.$el.find('.minutes').html(String(minutes));
        this.$el.find('.seconds').html(String(seconds));
    }
});

publicWidget.registry.ProductWishlist = publicWidget.registry.ProductWishlist.extend({
    _removeWish: function (e, deferred_redirect) {
        var tr = $(e.currentTarget).closest('.wishlist-items');
        var wish = tr.data('wish-id');
        var product = tr.data('product-id');
        var self = this;

        rpc('/shop/wishlist/remove/' + wish).then(function () {
            $(tr).hide();
        });

        this.wishlistProductIDs = this.wishlistProductIDs.filter((p) => p !== product);
        sessionStorage.setItem('website_sale_wishlist_product_ids', JSON.stringify(this.wishlistProductIDs));
        if (this.wishlistProductIDs.length === 0) {
            if (deferred_redirect) {
                deferred_redirect.then(function () {
                    self._redirectNoWish();
                });
            }
        }
        this._updateWishlistView();
    },

    _addOrMoveWish: function (e) {
        var tr = $(e.currentTarget).closest('.wishlist-items');
        var product = tr.data('product-id');
        $('.o_wsale_my_cart').removeClass('d-none');

        if ($('#b2b_wish').is(':checked')) {
            return this._addToCart(product, tr.find('add_qty').val() || 1);
        } else {
            var adding_deffered = this._addToCart(product, tr.find('add_qty').val() || 1);
            this._removeWish(e, adding_deffered);
            return adding_deffered;
        }
    },
});

publicWidget.registry.BitsAddCart = publicWidget.Widget.extend(cartHandlerMixin, VariantMixin, {
    selector: "#wrapwrap",
    events: {
        'click .btn_cart_bits': 'async _addToCart',
    },
    init: function () {
        this._super.apply(this, arguments);
        this.rpc = rpc;
    },
    _addToCart: function (ev) {
        ev.preventDefault();
        var def = () => {
            this.isBuyNow = ev.currentTarget.classList.contains('o_we_buy_now');
            const targetSelector = ev.currentTarget.dataset.animationSelector || 'img';
            this.$itemImgContainer = this.$(ev.currentTarget).closest(`:has(${targetSelector})`);
            return this._handleAdd($(ev.currentTarget).closest('form'));
        };
        return def();
    },
    _handleAdd: function ($form) {
        var self = this;
        this.$form = $form;
        var productSelector = [
            'input[type="hidden"][name="product_id"]',
            'input[type="radio"][name="product_id"]:checked'
        ];
        var productReady = this.selectOrCreateProduct(
            $form,
            parseInt($form.find(productSelector.join(', ')).first().val(), 10),
            $form.find('.product_template_id').val(),
            false
        );
        return productReady.then(function (productId) {
            $form.find(productSelector.join(', ')).val(productId);
            self._updateRootProduct($form, productId);
            return self._onProductReady();
        });
    },
    _updateRootProduct($form, productId) {
        this.rootProduct = {
            product_id: productId,
            quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1),
            product_custom_attribute_values: this.getCustomVariantValues($form.find('.js_product')),
            variant_values: this.getSelectedVariantValues($form.find('.js_product')),
            no_variant_attribute_values: this.getNoVariantAttributeValues($form.find('.js_product'))
        };
    },
    _onProductReady: function () {
        return this._submitForm();
    },
    _submitForm: function () {
        const params = this.rootProduct;
        params.add_qty = params.quantity;
        params.product_custom_attribute_values = JSON.stringify(params.product_custom_attribute_values);
        params.no_variant_attribute_values = JSON.stringify(params.no_variant_attribute_values);
        delete params.quantity;
        this.stayOnPageOption = true;
        return this.addToCart(params);
    },
});

// ProductWishlist 
publicWidget.registry.ProductWishlist.include({
    selector: '#wrapwrap',
})
// Comparison btn
publicWidget.registry.ProductComparison.include({
    selector: '#wrapwrap',
})

publicWidget.registry.BitsAddCartNotifier = publicWidget.Widget.extend({
    selector: ".bits-notify-container",
    events: {
        'click .recent-close': 'closeNotify',
    },
    init: function () {
        this._super.apply(this, arguments);
        this.rpc = rpc;
        this.init_notifier();
    },
    init_notifier: async function (ev) {
        let self = this
        setInterval(async function () {
            const response = await rpc('/get/cart_notify');
            if (response && response.product_id) {
                self.$el.empty();
                self.$el.append(response.popup_html);
                self.$el.toggleClass('make-toast');
                setTimeout(function () {
                    self.$el.toggleClass('make-toast');
                }, 5000);
            }
        }, 20000);
    },
    closeNotify: function (ev) {

        this.$el.empty();
    }
}) 
