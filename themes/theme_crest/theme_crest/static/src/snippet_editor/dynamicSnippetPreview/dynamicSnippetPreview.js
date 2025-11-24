/** @odoo-module **/

import {
  Component, useState, onMounted,
} from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";
import { useService } from "@web/core/utils/hooks";
import { renderToElement } from "@web/core/utils/render";
import { carouselConfigs } from "../../js/static_template/config_carousel";
import { deserializeDateTime } from "@web/core/l10n/dates";

export class DynamicSnippetPreview extends Component {
  setup() {
    this.rpc = rpc
    this.state = useState({
      sliderConfigs: [],
      timer: null,
      offerDue: null,
    })
    onMounted(async () => {
      const data = this.props?.data;
      this.$target = $("#snippet_preview");
      let containerAry = [];
      let sliderConfi = []

      if (data.length != 0) {
        // Use Promise.all to wait for all async operations 
        data.map(async (row, index) => {
          let container = $("<div class='container'></div>");
          let row_template = $("<div class='row'></div>");

          // Use Promise.all to wait for all async operations
          row.map(async (col, colIndex) => {
            let snippet_class = "demo-snippet"
            if (col?.data?.model == 'static_template') {
              snippet_class = 'snp_static_bits';
            }
            if (col?.data?.model != 'static_template') {
              snippet_class = 'snp_dynamic_bits';
            }

            if (col?.data?.model == 'static_template') {
              let col_template = $(`<div class='${this._getResponsiveClasses(col?.class)}   oe_structure oe_empty ${snippet_class}'></div>`);
              let col_inside;
              if (col?.visual?.template) {
                try {
                  col_inside = renderToElement(col?.visual?.template);
                } catch (err) {
                  col_inside = col_inside = renderToElement('theme_crest.no_records', {});
                }
              } else {
                col_inside = col_inside = renderToElement('theme_crest.no_records', {});
              }
              col_template.append(col_inside);
              col_template.attr("data-snp_config", JSON.stringify(col));
              row_template.append(col_template);
            } else {
              let col_template = $(`<div class='${this._getResponsiveClasses(col?.class)}  oe_structure oe_empty ${snippet_class}'></div>`);
              let col_inside;
              row_template.append(col_template);
              try {
                const res_view = await this.rpc('/website/snippet/get', {
                  'model': col.data.model,
                  'template_key': col.visual.template ? col.visual.template : 'dy_prod_tmp_style_1_bits',
                  'visual': col.visual,
                  'data': col.data
                });
                col_inside = res_view.view;

                if (col.visual.type == "slider") {
                  col_inside = $(col_inside).find(".owl-carousel").addClass(`dy-prod-owl-carousel-style-${col?._uid}`)
                  let selector = `dy-prod-owl-carousel-style-${col?._uid}`
                  if (selector) {
                    let options = {
                      loop: true,
                      margin: 0,
                      dots: col.visual['dost'],
                      nav: col.visual['nav'],
                      autoplay: col.visual['autoplay'],
                      items: Number(col.visual.limit),
                      responsive: {
                        0: { items: 1 },
                        600: { items: Math.min(Number(col.visual.limit), 2) },
                        1000: { items: Math.min(Number(col.visual.limit), 3) },
                        1200: { items: Math.min(Number(col.visual.limit), 5) },
                        1400: { items: Number(col.visual.limit) }
                      }
                    }
                    sliderConfi.push({ selector, options })
                  }
                }
                this.state.sliderConfigs = sliderConfi
                col_template.append(col_inside);
                col_template.attr("data-snp_config", JSON.stringify(col));

                if (this.$target.find('.pl_offer_timer').attr('data-offerends')) {
                  this._start_countdown();
                }
                this.owlCarouselDynamic();
              } catch (error) {
                col_inside = renderToElement('theme_crest.no_records', {});
                col_template.append(col_inside);

              }
            }

          });
          if (row[0]?.container == true) {
            container.removeClass('container').addClass('container-fluid');
          } else {
            container.removeClass('container-fluid').addClass('container');
          }

          container.append(row_template);
          containerAry.push(container)
        });
      } else {
        let container = $("<div class='container'></div>");
        let row_template = $("<div class='row'></div>");
        let col_template = $(`<div class='col-12 oe_structure oe_empty'></div>`);
        let col_inside = renderToElement('theme_crest.not_data_available', {});
        let col = {
          "class": "col-12",
          "_uid": `${this.getRandomUid()}`,
          "container": false,
          "data": {
            "model": "static_template"
          },
          "visual": {
            "template": "theme_crest.not_data_available",
            "limit": 4,
            "type": "grid",
            "buttons": [],
            "dost": false,
            "nav": true,
            "autoplay": false,
            "borderstyle": "rounded"
          }
        }
        col_template.append(col_inside);
        col_template.attr("data-snp_config", JSON.stringify(col));
        container.append(row_template);
        containerAry.push(container)
      }

      this.$target.empty();
      this.$target.append(containerAry);
      this._initializeCarousels();
      this.owlCarouselDynamic();
      this._initCounter();
      this._initFiltering()
      if (this.$target.find('.pl_offer_timer').attr('data-offerends')) {
        this._start_countdown();

      }

    });
  }
  _start_countdown() {

    const offerDueString = this.$target.find('.pl_offer_timer').attr('data-offerends');
    if (!offerDueString) {
      console.log("Offer end date not found.");
      return;
    }
    const offerDue = deserializeDateTime(offerDueString);
    this.state.timer = setInterval(() => {
      const now = new Date().getTime();
      const timeLeft = offerDue.ts - now;

      if (timeLeft <= 0) {
        clearInterval(this.state.timer);
        this.$target.find('.card_item_timer_bits').hide();
        return;
      } else {
        this.$target.find('.card_item_timer_bits').show();
      }

      const days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
      const hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

      const $timer = this.$target.find('.pl_offer_timer');
      $timer.find('.days').html(String(days));
      $timer.find('.hours').html(String(hours));
      $timer.find('.minutes').html(String(minutes));
      $timer.find('.seconds').html(String(seconds));

      if (!$timer.find('.counter').hasClass('pading-space')) {
        $timer.find('.counter').addClass('pading-space');
      }
    }, 1000);
  }

  _getResponsiveClasses(colClass) {
    const colSize = Number(colClass?.replace("col-", ""));
    const sizeMap = {
      12: "col-12",
      11: "col-12 col-lg-11",
      10: "col-12 col-lg-10",
      9: "col-12 col-lg-9",
      8: "col-12 col-lg-8",
      7: "col-12 col-lg-7",
      6: "col-12 col-lg-6",
      4: "col-12 col-md-6 col-lg-4",
      3: "col-12 col-md-6 col-lg-3 col-xl-3",
      2: "col-12 col-lg-3 col-md-4 col-sm-6 col-xl-2",
      1: "col-12 col-lg-3 col-md-4 col-sm-6 col-xl-1",
    };
    return sizeMap[colSize] || "col-12";
  }

  getRandomUid() {
    var S4 = function () {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    };
    return S4();
  }
  _initializeCarousels() {
    // Initialize all carousels after rendering
    carouselConfigs.forEach(config => {
      const $carousel = this.$target.find(config.selector);
      if ($carousel.length) {
        $carousel.owlCarousel(config.options);
      }
    });
  }
  _initCounter() {
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
  }
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
  }
  owlCarouselDynamic() {
    // Ensure all carousels are initialized after rendering
    this.state.sliderConfigs.forEach((config) => {
      if (config.selector) {
        const $carousel = $(`.${config.selector}`);
        if ($carousel.length) {
          $carousel.owlCarousel(config.options);
        }
      }
    });
  }
}

DynamicSnippetPreview.components = {};
DynamicSnippetPreview.template = "theme_crest.DynamicSnippetPreview";
