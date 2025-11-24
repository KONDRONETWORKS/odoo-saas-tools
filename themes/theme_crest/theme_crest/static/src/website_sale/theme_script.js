/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import '@website_sale_wishlist/js/website_sale_wishlist';

let setTimer;

publicWidget.registry.HotspotShowDisplay = publicWidget.Widget.extend({
    selector: ".target_hotspot_tag.show_card_product",
    events: {
        'mouseenter': 'MouseEnter',
        'mouseleave': 'MouseLeave',
    },

    start: function () {
        this.$el.popover({
            trigger: 'manual',
            animation: true,
            html: true,
            container: 'body',
            placement: 'auto',
            sanitize: false,
            template: `<div class="popup-hover popup-hover-hotspot" role="tooltip"><div class="tooltip-arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>`
        });
        return this._super.apply(this, arguments);
    },
    MouseEnter: function (ev) {
        let self = this;
        self.hovered = true;
        clearTimeout(setTimer);

        $(this.selector).not(ev.currentTarget).popover('hide');

        setTimer = setTimeout(async function () {
            try {
                let productId = parseInt($(ev.currentTarget).attr("data-product-template-ids"));
                let response = await $.get("/product-pop-details", { 'product': productId });
                let popoverInstance = Popover.getInstance(self.$el[0]);

                if (popoverInstance) {
                    if (typeof popoverInstance.getTipElement === 'function') {
                        popoverInstance._config.content = response;
                        popoverInstance.setContent(popoverInstance.getTipElement());
                        self.$el.popover("show");
                    } else {
                        popoverInstance._config.content = response;
                        self.$el.popover("show");
                    }

                    $('.popup-hover').on('mouseleave', () => {
                        self.$el.trigger('mouseleave');
                    });

                    $(document).on("click", ".add-to-cart-hotspot-bits", function (ev) {
                        ev.preventDefault();
                        let $form = $(this).closest("form");

                        if (!$form.length) {
                            console.error("Form not found!");
                            return;
                        }

                        let websiteSaleInstance = publicWidget.registry.WebsiteSale;
                        if (websiteSaleInstance && websiteSaleInstance.prototype._handleAdd) {
                            $form.submit();
                        }
                    });

                } else {
                    console.error("Popover instance is not available.");
                }

            } catch (error) {
                console.error("Error fetching product details:", error);
            }
        }, 300);
    },


    MouseLeave: function (ev) {
        let self = this;
        self.hovered = false;
        setTimeout(function () {
            if ($('.popup-hover:hover').length) {
                return;
            }
            if (!self.$el.is(':hover')) {
                self.$el.popover('hide');
            }
        }, 2000);
    },
});