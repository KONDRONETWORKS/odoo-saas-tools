/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ProductAttrsChange = publicWidget.Widget.extend({
    selector: '.dy_prod_template_style_bits',
    events: {
        "click .color-attr-bits, .all-attr-bits": "_onVariantClick",
    },

    start: function () {
        this._setDefaultActiveVariant();
        return this._super.apply(this, arguments);
    },

    _setDefaultActiveVariant: function () {
        this.$(".dy_prod_template_style_bits").each((index, card) => {
            let $card = $(card);
            let $firstVariant = $card.find(".color-attr-bits, .all-attr-bits").first();
            if ($firstVariant.length) {
                $firstVariant.addClass("active");
                this._updateProductImage($firstVariant, $card);
            }
        });
    },

    _onVariantClick: function (ev) {
        let $target = $(ev.currentTarget);
        let $card = $target.closest(".dy_prod_template_style_bits");
        if ($card.length) {
            $card.find(".color-attr-bits, .all-attr-bits").removeClass("active");
            $target.addClass("active");
            this._updateProductImage($target, $card);
        }
    },

    _updateProductImage: function ($variant, $card) {
        if (!$card || !$variant) return;
        let newImage = $variant.attr("data-main-image");
        if (newImage) {
            $card.find(".product-img-bits").attr("src", newImage);
        }
    },
});

publicWidget.registry.ProductAttrsChange;
