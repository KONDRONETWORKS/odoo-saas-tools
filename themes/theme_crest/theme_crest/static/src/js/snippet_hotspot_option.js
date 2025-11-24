/** @odoo-module **/

import options from '@web_editor/js/editor/snippets.options';


options.registry.ImageHotspot = options.Class.extend({
    start: function () {
        this.$target.parent().find('.target_hotspot_tag').draggable({
            containment: 'parent',
            scroll: false,
            revertDuration: 200,
            refreshPositions: true,
            stop: function () {
                let left = (100 * parseFloat($(this).position().left / parseFloat($(this).parent().width()))) + "%";
                let top = (100 * parseFloat($(this).position().top / parseFloat($(this).parent().height()))) + "%";
                $(this).css("left", left);
                $(this).css("top", top);
                $(this).find('img').click();
            }
        });
    },

    async setImgHotspot(previewMode, widgetValue, params) {
        if (widgetValue == 'enabled') {
            this.$target.parent().find('.target_hotspot_tag').remove();
            this.$target.parent().append(`<section contenteditable="false" name="Hotspot-Block" style="--hotspot-border-color: #red;" data-exclude=".s_col_no_resize, .s_col_no_bgcolor" class="hotspot_draggable target_hotspot_tag o_not_editable s_col_no_resize s_col_no_bgcolor fade_hotspot shape-none show_icon"><span class="show_hotspot" draggable="true" > <i class="fa fa-plus hotspot-icon"></i></span></section>`);

            this.trigger_up('activate_snippet', {
                $snippet: this.$target.parent().find('.target_hotspot_tag'),
            });
        } else {
            this.$target.parent().find('.target_hotspot_tag').remove();
        }
    },
});

options.registry.ImageHotspotEvent = options.Class.extend({
    start: function () {
        this._super.apply(this, arguments);
        this.$target.draggable({
            containment: 'parent',
            scroll: false,
            revertDuration: 200,
            refreshPositions: true,
            stop: function () {
                $(this).css({
                    "left": $(this).position().left + "px",
                    "top": $(this).position().top + "px"
                });

                $(this).find('img').click();
            }
        });
    },

    onFocus() {
        this.options.wysiwyg.odooEditor.addEventListener('activate_image_link_tool', this._activateLinkTool);
        this.options.wysiwyg.odooEditor.addEventListener('deactivate_image_link_tool', this._deactivateLinkTool);
        this.rerender = true;
    },

    onBlur() {
        this.options.wysiwyg.odooEditor.removeEventListener('activate_image_link_tool', this._activateLinkTool);
        this.options.wysiwyg.odooEditor.removeEventListener('deactivate_image_link_tool', this._deactivateLinkTool);
    },

    setLink(previewMode, widgetValue, params) {
        const hotspotDot = this.$target.find('.show_hotspot')[0];
        let parentTag = hotspotDot.parentNode;

        parentTag = parentTag.tagName !== 'A'
            ? (() => {
                const wrapperEl = document.createElement('a');
                hotspotDot.after(wrapperEl);
                wrapperEl.appendChild(hotspotDot);
                return wrapperEl;
            })()
            : (() => {
                parentTag.replaceWith(hotspotDot);
                return hotspotDot.parentNode;
            })();
    },
    _activateLinkTool() {
        this.$target.find('.show_hotspot')[0].parentElement.tagName === 'A'
            ? this._requestUserValueWidgets('media_url_opt')[0].focus()
            : this._requestUserValueWidgets('media_link_opt')[0].enable();
    },
    setNewWindow(previewMode, widgetValue, params) {
        const linkEl = this.$target.find('.show_hotspot')[0].parentElement;
        widgetValue ? linkEl.setAttribute('target', '_blank') : linkEl.removeAttribute('target');
    },
    _deactivateLinkTool() {
        const parentTag = this.$target.children('.show_hotspot')[0].parentNode;
        if (parentTag.tagName === 'A') {
            this._requestUserValueWidgets('media_link_opt')[0].enable();
        }
    },
    setAction(previewMode, widgetValue, params) {
        const hotspotDot = this.$target.find('.show_hotspot')[0];

        let parentTag = hotspotDot.parentNode;
        if (parentTag.tagName !== 'A') {
            const wrapperEl = document.createElement('a');
            wrapperEl.href = '#';
            wrapperEl.classList.add('hotspot-link');
            parentTag.replaceChild(wrapperEl, hotspotDot);
            wrapperEl.appendChild(hotspotDot);
            parentTag = wrapperEl;
        }

        parentTag.href = widgetValue === 'redirect_product'
            ? `/shop/product/${this.$target[0].getAttribute('data-product-template-ids') || ''}`
            : widgetValue === 'redirect_url'
                ? params?.url || '#'
                : '#';
    },
    setProductLink(previewMode, widgetValue, params) {
        const targetEl = this.$target[0];
        const parentTag = this.$target.find('.show_hotspot')[0].parentNode;
        const productID = targetEl.getAttribute('data-product-template-ids');

        targetEl.classList.contains('redirect_product') && parentTag.tagName === 'A'
            ? productID && $(this.$target.find('a')[0]).attr('href', `/shop/product/${productID}`)
            : targetEl.classList.contains('show_card_hotspot_bits')
                ? this.$target.attr('data-id', productID)
                : null;
    },


    setUrl(previewMode, widgetValue, params) {
        const linkEl = this.$target.find('.show_hotspot')[0].parentElement;
        let url = widgetValue;

        !url
            ? (linkEl.removeAttribute('href'), this.$target.trigger('href_changed'))
            : (!url.startsWith('/') && !url.startsWith('#') && !/^([a-zA-Z]*.):.+$/gm.test(url)
                ? url = 'http://' + url
                : null,
                linkEl.setAttribute('href', url),
                this.rerender = true,
                this.$target.trigger('href_changed'));
    },
    async updateUI() {
        if (this.rerender) {
            this.rerender = false;
            await this._rerenderXML();
            return;
        }
        return this._super.apply(this, arguments);
    },

    _computeWidgetState(methodName, params) {
        const parentTag = this.$target.find('a');
        let linkEl = parentTag.length !== 0 && parentTag[0].tagName === 'A' ? parentTag : null;

        if (methodName === 'setLink') {
            return linkEl ? 'true' : '';
        } else if (methodName === 'setUrl') {
            let href = linkEl ? linkEl[0].getAttribute('href') : '';
            return href || '';
        } else if (methodName === 'setNewWindow') {
            const target = linkEl ? linkEl[0].getAttribute('target') : '';
            return target === '_blank' ? 'true' : '';
        }

        return this._super(...arguments);
    },

    async _computeWidgetVisibility(widgetName, params) {
        return widgetName === 'media_link_opt' && this.$target?.[0]
            ? this.$target[0].matches('img')
                ? isImageSupportedForStyle(this.$target[0])
                : !this.$target.find('.show_hotspot')[0]?.classList.contains('media_iframe_video')
            : this._super(...arguments);
    },
});
