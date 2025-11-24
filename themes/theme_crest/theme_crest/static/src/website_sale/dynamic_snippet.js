/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";
import { uniqueId } from "@web/core/utils/functions";
import { utils as uiUtils } from "@web/core/ui/ui_service";
import { renderToElement } from "@web/core/utils/render";
import { rpc } from "@web/core/network/rpc";

publicWidget.registry.Test = publicWidget.Widget.extend({
    selector: '.snp_dynamic_bits',
    events: {
    },
    init: function () {
        this._super.apply(this, arguments);
        /**
         * The dynamic filter data source data formatted with the chosen template.
         * Can be accessed when overriding the _render_content() function in order to generate
         * a new renderedContent from the original data.
         *
         * @type {*|jQuery.fn.init|jQuery|HTMLElement}
         */
        this.data = [];
        this.config = {};
        this.renderedContent = '';
        this.isDesplayedAsMobile = uiUtils.isSmall();
        this.unique_id = uniqueId("s_dynamic_snippet_");
        this.template_key = 'website.s_dynamic_snippet.grid';
        this.rpc = rpc;
    },
    /**
     *
     * @override
     */
    willStart: function () {
        return this._super.apply(this, arguments).then(
            () => Promise.all([
                this._fetchData(),
            ])
        );
    },
    /**
     *
     * @override
     */
    start: function () {
        return this._super.apply(this, arguments)
            .then(() => {
                this._render();
            });
    },
    /**
     *
     * @override
     */
    destroy: function () {
        this.options.wysiwyg && this.options.wysiwyg.odooEditor.observerUnactive();
        this._toggleVisibility(false);
        // this._setupSizeChangedManagement(false);
        this._clearContent();
        this.options.wysiwyg && this.options.wysiwyg.odooEditor.observerActive();
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _clearContent: function () {
        const $templateArea = this.$el.find('.dynamic_snippet_template');
        this.trigger_up('widgets_stop_request', {
            $target: $templateArea,
        });
        $templateArea.html('<img src="/theme_crest/static/images/loader-bigsize-gif.gif" alt="loading.." class="col-12 col-md-6 mx-auto" />');
    },
    /**
     * Method to be overridden in child components if additional configuration elements
     * are required in order to fetch data.
     * @private
     */
    _isConfigComplete: function () {
        this.config = this.$el.data('snp_config');
        return this.config?.data?.model !== undefined;
    },
    /**
     * Method to be overridden in child components in order to provide a search
     * domain if needed.
     * @private
     */
    _getSearchDomain: function () {
        return [];
    },
    /**
     * Method to be overridden in child components in order to add custom parameters if needed.
     * @private
     */
    _getRpcParameters: function () {
        return {};
    },
    /**
     * Fetches the data.
     * @private
     */
    async _fetchData() {
        if (this._isConfigComplete()) {
            // const nodeData = this.el.dataset;
            const res_view = await this.rpc(
                '/website/snippet/get',
                Object.assign({
                    'model': this.config.data.model,
                    // 'template_key': 'default_template',
                    'template_key': this.config.visual.template ? this.config.visual.template : 'dy_prod_tmp_style_1_bits',
                    'visual': this.config.visual,
                    'data': this.config.data
                }, this._getRpcParameters())
            );

            this.data = res_view
        } else {
            this.data = renderToElement('theme_crest.no_records',{});
        }
    },
    /**
     *
     * @private
     */
    _render: function () {
        if (this.data?.view) {
            this.$el.removeClass('o_dynamic_empty');
            let view = this.data?.visual?.type == 'slider' ? $(this.data?.view).find(".owl-carousel").addClass(`dy-prod-owl-carousel-style-${this.config?._uid}`) : this.data?.view
            this.renderedContent = view;
        } else {
            this.$el.addClass('o_dynamic_empty');
            this.renderedContent = renderToElement('theme_crest.no_records',{});;
        }
        this._renderContent();
        this.trigger_up('widgets_start_request', {
            $target: this.$el.children(),
            options: { parent: this },
            editableMode: this.editableMode,
        });
        // carousel 
    },
    /**
     * @private
     */
    _renderContent: function () {
        const $templateArea = this.$el.find('.dynamic_snippet_template');
        this.trigger_up('widgets_stop_request', {
            $target: $templateArea,
        });
        $templateArea.html(this.renderedContent);
        if (this.data?.visual?.type == 'slider') {
            this.owlCarouselDynamic()
        }

        this.trigger_up('widgets_start_request', {
            $target: $templateArea,
            editableMode: this.editableMode,
        });
    },
    /**
     *
     * @param visible
     * @private
     */
    _toggleVisibility: function (visible) {
        this.$el.toggleClass('o_dynamic_empty', !visible);
    },
    /**
     * Called when the size has reached a new bootstrap breakpoint.
     *
     * @private
     */
    _onSizeChanged: function () {
        if (this.isDesplayedAsMobile !== uiUtils.isSmall()) {
            this.isDesplayedAsMobile = uiUtils.isSmall();
            this._render();
        }
    },

    owlCarouselDynamic: function () {
        let is_rtl = false;
        if ($('#wrapwrap').hasClass('o_rtl')) {
            is_rtl = true;
        }
        let selector = `.dy-prod-owl-carousel-style-${this.config._uid}`;
        let option = {
            loop: true,
            margin: 0,
            dots: this.data.visual['dost'],
            nav: this.data.visual['nav'],
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            autoplay: this.data.visual['autoplay'],
            items: Number(this.data.visual.limit),
            rtl: is_rtl,
            responsive: {
                0: { items: 1 },
                600: { items: Math.min(Number(this.data.visual.limit), 2) },
                1000: { items: Math.min(Number(this.data.visual.limit), 3) },
                1200: { items: Math.min(Number(this.data.visual.limit), 5) },
                1400: { items: Number(this.data.visual.limit) }
            }
        }
        if (selector.length) {
            $(selector).owlCarousel(option);
            // $("img.lazyload").lazyload();
        } else {
            console.warn(`Carousel selector not found: ${selector.selector}`);
        }
    }
});
