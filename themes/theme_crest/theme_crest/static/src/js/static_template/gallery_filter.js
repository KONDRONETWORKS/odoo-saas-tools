/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.PortfolioFilter = publicWidget.Widget.extend({
    selector: '.portfolio-style-3',

    start() {
        this._super.apply(this, arguments);
        this._initFiltering();
    },

    _initFiltering() {
        const $filterButtons = this.$target.find('.filter-item'); // Scoped to the snippet's container
        const $portfolioItems = this.$target.find('.project-items'); // Scoped to the snippet's container

        $filterButtons.on('click', (event) => {
            event.preventDefault();
            const $button = $(event.currentTarget);
            $filterButtons.removeClass('active');
            $button.addClass('active');
            const filter = $button.data('filter');
            $portfolioItems.each(function () {
                const $item = $(this);
                if (filter === '*' || $item.hasClass(filter.slice(1))) {
                    $item.show();
                } else {
                    $item.hide();
                }
            });
        });
    },
});


export default publicWidget.registry.PortfolioFilter;