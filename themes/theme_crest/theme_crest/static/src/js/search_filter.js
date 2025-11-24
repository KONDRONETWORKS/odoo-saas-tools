/** @odoo-module **/


import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.BrandSearchFilter = publicWidget.Widget.extend({
    selector: '.search_filter_category',
    events: {
        'input .js-brand-search': '_onSearchInputBrand',
        'input .js-tags-search': '_onSearchInputTag',
        'input .js-color-search': '_onSearchInputColor',
        'input .js-radio-search': '_onSearchInputRadio',
        'input .js-pills-search': '_onSearchInputPills',
        'input .js-multi-search': '_onSearchInputMulti',
        'input .js-select-search': '_onSearchInputSelect',
        'input .js-sort-search': '_onSearchInputSort',

    },
    _onSearchInputBrand(ev) {
        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.brand-item');
        this._onSearchInput(brandItems, searchTerm)
    },
    _onSearchInputTag(ev) {
        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.tags-items');
        this._onSearchInput(brandItems, searchTerm)
    },
    _onSearchInputColor(ev) {

        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.color-filter-itmes');
        this._onSearchInput(brandItems, searchTerm)
    },

    _onSearchInputRadio(ev) {
        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.radio-filter-itmes');
        this._onSearchInput(brandItems, searchTerm)
    },
    _onSearchInputPills(ev) {
        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.pills-filter-itmes');
        this._onSearchInput(brandItems, searchTerm)
    },
    _onSearchInputMulti(ev) {
        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.multi-filter-itmes');
        this._onSearchInput(brandItems, searchTerm)
    },
    _onSearchInputSelect(ev) {
        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.select-filter-itmes');
        this._onSearchInput(brandItems, searchTerm)
    },
    _onSearchInputSort(ev) {
        
        const searchTerm = ev.target.value.toLowerCase().trim();
        const brandItems = document.querySelectorAll('.sort-filter-itmes');
        this._onSearchInput(brandItems, searchTerm)
    },
    _onSearchInput(brandItems, searchTerm) {
        brandItems.forEach((item) => {
            
            const brandName = item.dataset.name.toLowerCase();
            if (brandName.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    },
});
