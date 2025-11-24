/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { carouselConfigs } from "./config_carousel";
export const CarouselStaticTemplate = publicWidget.Widget.extend({
    selector: ".snp_static_bits",

    start: function () {
        this._super.apply(this, arguments);
        this._initializeCarousel();
    },

    _initializeCarousel: function () {
        const self = this;
        carouselConfigs.forEach((config, index) => {
            const $carousel = self.$el.find(config.selector);
            if ($carousel.length) {
                $carousel.owlCarousel(config.options);

                // Keep only the last set of owl-dots
                let dots = $carousel.find('.owl-dots');
                if (dots.length > 1) {
                    dots.slice(0, -1).remove();
                }
                // Move the remaining owl-dots to the end of the carousel
                $carousel.append(dots.last());
            }
        });
    },


});

publicWidget.registry.CarouselStaticTemplate = CarouselStaticTemplate 