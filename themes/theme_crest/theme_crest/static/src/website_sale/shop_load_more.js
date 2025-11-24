/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import '@website_sale/js/website_sale';
import { QuickViewdialogBits } from './quick_view';
import { _t } from '@web/core/l10n/translation';
import { renderToElement } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";

export const QuickViewBits = publicWidget.Widget.extend({
    selector: ".quick_view_container",
    events: {
        'click .o_quick_view_btn': '_init_quick_view',
    },
    start: function () {
        this.dialog = this.bindService("dialog");
    },
    _init_quick_view: function (ev) {
        this.call("dialog", "add", QuickViewdialogBits, {
            widget: this,
            product_id: parseInt($(ev.currentTarget).attr('data-product-template-id'))
        }); 
    }
});
publicWidget.registry.QuickViewBits = QuickViewBits;

export const LoadMoreProductsBits = publicWidget.Widget.extend({
    selector: ".bits-pager.container",
    events: {
        'click .load-more-bits': '_loadMoreBits'
    },
    init: function () {
        this._super.apply(this, arguments);
        this.rpc = rpc;
        this.loader = renderToElement('theme_crest.loader_bits', {});
    },
    _loadMoreBits: function (ev) {
        ev.preventDefault();
        var self = this;
        var action = ev.target.getAttribute('href');
        var BaseTarget = $('.o_wsale_products_grid_table_wrapper section');
        var pagerContainer = $('.products_pager')
        pagerContainer.empty().append(this.loader);
        $.ajax({
            url: action,
            type: 'GET',
            success: function (response) {
                var newProducts = $(response).find('.o_wsale_products_grid_table_wrapper section .oe_product');
                var pager = $(response).find('#products_grid .bits-pager.container');
                BaseTarget.append(newProducts);
                pagerContainer.empty().append(pager);
                self.trigger_up('widgets_start_request', { $target: $('.quick_view_container'), });
                self.trigger_up('widgets_start_request', { $target: $('form.oe_product_cart'), });
            }
        });

    }
});

publicWidget.registry.LoadMoreProductsBits = LoadMoreProductsBits;
