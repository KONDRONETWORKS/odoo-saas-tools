/** @odoo-module **/

export const carouselConfigs = [
    {
        selector: '.owl-carousel-clients-1', options: {
            loop: false, margin: 10, dots: false, nav: false, autoplay: true,
            autoplayTimeout: 2000, smartSpeed: 2000, slideTransition: 'linear',
            responsive: {
                0: { items: 1 }, 500: { items: 2 }, 768: { items: 4 },
                1000: { items: 5 }, 1200: { items: 6 }
            }
        }
    },
    {
        selector: '.owl-carousel-portfolio-1', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 }, 768: { items: 2 }, 1200: { items: 3 } }
        }
    },
    {
        selector: '.owl-carousel-team-2', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 }, 576: { items: 2 }, 992: { items: 3 }, 1200: { items: 4 } }
        }
    },
    {
        selector: '.owl-carousel-team-3', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 }, 992: { items: 2 }, 1200: { items: 3 } }
        }
    },
    {
        selector: '.owl-carousel-testimonials-1', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 }, 992: { items: 2 }, 1200: { items: 3 } }
        }
    },
    {
        selector: '.owl-carousel-testimonials-2', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 }, 992: { items: 2 }, 1200: { items: 3 } }
        }
    },
    {
        selector: '.owl-carousel-testimonials-4', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 } }
        }
    },
    {
        selector: '.owl-carousel-testimonials-6', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 } }
        }
    },
    {
        selector: '.owl-carousel-testimonials-7', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 }, 992: { items: 2 }, 1200: { items: 3 } }
        }
    },
    {
        selector: '.owl-carousel-testimonials-8', options: {
            loop: false, margin: 20, dots: true, nav: false,
            responsive: { 0: { items: 1 } }
        }
    }
];



