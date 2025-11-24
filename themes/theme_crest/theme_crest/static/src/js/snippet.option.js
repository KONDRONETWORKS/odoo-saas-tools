/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import { renderToElement } from "@web/core/utils/render";
import { SnippetEditorDialog } from "../snippet_editor/snippetEditorDialog/snippetEditorDialog";
import { carouselConfigs } from "./static_template/config_carousel";
options.registry.theme_crest_dynamic_snippet = options.Class.extend({
  onBuilt: function () {
    this._super();
    this.call("dialog", "add", SnippetEditorDialog, {
      data: [],
      save: this._storeData.bind(this),
    });
  },

  setGrid: function (previewMode, value, $opt) {
    let data = [];
    this.$target.children().children()
      .each((i, row) => {
        const $row = $(row);
        let row_data = [];
        $row.children().each((i, col) => {
          const $col = $(col);
          const dt = $col.data().snp_config;
          row_data.push(dt);
        });
        data.push(row_data);
      });
    this.call("dialog", "add", SnippetEditorDialog, {
      data: data,
      save: this._storeData.bind(this),
    });
  },

  _storeData(data) {
    // this.$target[0].dataset["snippet_data"] = JSON.stringify(data);
    let containerAry = []
    if (data.length != 0) {
      data.map(async (row, index) => {
        let container = $("<div class='container'></div>");
        let row_template = $("<div class='row'></div>");
        let snippet_class = "demo-snippet"
        row.map(async (col, colIndex) => {
          if (col?.data?.model == 'static_template') {
            snippet_class = 'snp_static_bits';
          }
          if (col?.data?.model != 'static_template') {
            snippet_class = 'snp_dynamic_bits';
          }

          if (snippet_class == 'snp_static_bits') {
            let col_template = $(`<div class='${snippet_class} ${this._getResponsiveClasses(col?.class)} oe_structure oe_empty'></div>`);
            let col_inside;
            if (col?.visual?.template) {
              try {
                col_inside = renderToElement(col?.visual?.template);
              } catch (err) {
                col_inside = `<div>row: ${index} col: ${colIndex} </div>`;
              }
            } else {
              col_inside = `<div>row: ${index} col: ${colIndex} </div>`;
            }
            col_template.append(col_inside);
            col_template.attr("data-snp_config", JSON.stringify(col));
            row_template.append(col_template);
          } else {
            let col_template = $(`<div class='${snippet_class} ${this._getResponsiveClasses(col?.class)} oe_structure oe_empty'>
              <div class="dynamic_snippet_template"><img src="/theme_crest/static/images/loader-bigsize-gif.gif" alt="loading.." class="col-12 col-md-6 mx-auto" />
            </div>`);
            col_template.attr("data-snp_config", JSON.stringify(col));
            row_template.append(col_template);
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
      col_template.append(col_inside);
      let col = {
        "class": "col-12",
        "_uid": this.getRandomUid(),
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
      col_template.attr("data-snp_config", JSON.stringify(col));
      row_template.append(col_template);
      container.append(row_template);
      containerAry.push(container)
    }

    this.$target.empty();
    this.$target.append(containerAry);
    this._initializeCarousels()
    this._initCounter();
    this.options.wysiwyg.odooEditor.observerActive();
    this.$target.trigger("content_changed");
  },
  getRandomUid() {
    var S4 = function () {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    };
    return S4();
  },
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
  },
  _initializeCarousels() {
    carouselConfigs.forEach(config => {
      const $carousel = this.$target.find(config.selector);
      if ($carousel.length && !$carousel.hasClass('owl-loaded')) {
        $carousel.owlCarousel(config.options);
      }
    });
  },
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

});
