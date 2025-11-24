/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.StaticTemplateCounter = publicWidget.Widget.extend({
    selector: '.header_theme_crest_1',
    events: {
        'click .left-btn': '_scrollLeft',
        'click .right-btn': '_scrollRight',
    },

    start() {
        this._updateScrollButtons();
        this._bindScrollEvent();
    },

    _scrollLeft(ev) {
        const scrollContainer = document.getElementById('category-scroll');
        scrollContainer.scrollLeft -= 200; // Scroll left by 200px
        this._updateScrollButtons(); // Update button visibility
    },

    _scrollRight(ev) {
        const scrollContainer = document.getElementById('category-scroll');
        scrollContainer.scrollLeft += 200; // Scroll right by 200px
        this._updateScrollButtons(); // Update button visibility
    },

    _bindScrollEvent() {
        const scrollContainer = document.getElementById('category-scroll');
        scrollContainer.addEventListener('scroll', this._updateScrollButtons.bind(this));
    },

    _updateScrollButtons() {
        const scrollContainer = document.getElementById('category-scroll');
        const scrollLeft = scrollContainer.scrollLeft;
        const maxScrollLeft = scrollContainer.scrollWidth - scrollContainer.clientWidth;

        const leftButton = document.querySelector('.left-btn');
        const rightButton = document.querySelector('.right-btn');

        // Show or hide the left button
        if (scrollLeft <= 0) {
            leftButton.style.display = 'none'; // Hide the left button
        } else {
            leftButton.style.display = 'block'; // Show the left button
        }

        // Show or hide the right button
        if (scrollLeft >= maxScrollLeft) {
            rightButton.style.display = 'none'; // Hide the right button
        } else {
            rightButton.style.display = 'block'; // Show the right button
        }
    },
})

publicWidget.registry.HeaderOffer = publicWidget.Widget.extend({
    selector: 'header',
    events: { 'click .header-close-btn': '_onCloseHeader' },
    start() {
        this._super.apply(this, arguments);
        this._offerHeader();
    },
    _offerHeader() {

        $('.pricelist-carousel-offers').owlCarousel({
            loop: true,
            margin: 0,
            nav: true,
            autoplay: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 3000,
            autoplayHoverPause: true,
            navText: [
                '<i class="fa fa-angle-left"></i>',
                '<i class="fa fa-angle-right"></i>'
            ],
            responsive: {
                0: {
                    items: 1
                },

            }
        })
    },
    _onCloseHeader(ev) {
        ev.preventDefault();
        $('.header-offers-top').hide();
    }
})
