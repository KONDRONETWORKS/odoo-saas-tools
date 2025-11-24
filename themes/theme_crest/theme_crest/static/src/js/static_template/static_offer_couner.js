/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.StaticTemplateCounter = publicWidget.Widget.extend({
    selector: '.snp_static_bits',
    start: function () {
        this._super.apply(this, arguments);
        this._initCounter();
    },

    _initCounter: function () { 
        var counters = $(".counter-temp");
        var countersQuantity = counters.length;
        var counter = [];
        for (let i = 0; i < countersQuantity; i++) {
            counter[i] = parseInt(counters[i].innerHTML);
        }
        var count = function (start, value, id) {
            var localStart = start;
            setInterval(function () {
                if (localStart < value) {
                    if (value.toString().length == 1) {
                        localStart++; // Increment by 1
                    } else if (value.toString().length == 3) {
                        localStart += 10; // Increment by 100
                    } else if (value.toString().length == 4) {
                        localStart += 100; // Increment by 100
                    } else {
                        localStart++;
                    }
                    counters[id].innerHTML = localStart;
                }
            }, 40);
        }

        for (let j = 0; j < countersQuantity; j++) {
            count(0, counter[j], j);
        }
    },
});

export default publicWidget.registry.StaticTemplateCounter;