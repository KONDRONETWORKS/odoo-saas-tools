/** @odoo-module **/

import {
  Component,
  useEffect,
  useState,
  onWillStart,
} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { TEMPATE } from "../utils";
import { CATEGORIES } from "../utils";
export class DynamicSnippetVisual extends Component {
  setup() {
    let initialModel = [].concat(...this.props.data).find((ele) => ele?._uid == this.props.selectedCol);

    let selectedTemplate;
    if (initialModel.data.model === 'product.template') {
      selectedTemplate = 'dy_prod_tmp_style_1_bits';
    } else if (initialModel.data.model === 'product.public.category') {
      selectedTemplate = 'dy_categ_tmp_style_1_bits';
    } else if (initialModel.data.model === 'blog.post') {
      selectedTemplate = 'dy_blog_tmp_style_1_bits';
    }


    this.state = useState({
      colValue: false,
      model: "",
      selectedCol: false,
      templates: TEMPATE,
      catgorys: CATEGORIES,
      selectedTemplate: selectedTemplate,
      selectedCategory: "banner",
      visual: {},
      limit: 4,
      selectedType: "grid",
      selectedButton: [],
      borderStyle: 'rounded',
      dost: false,
      nav: true,
      autoplay: false,
    });
    this.orm = useService("orm");

    useEffect(
      () => {

        this.state.visual = {
          template: this.state.selectedTemplate,
          limit: this.state.limit,
          type: this.state.selectedType,
          buttons: this.state.selectedButton,
          dost: this.state.dost,
          nav: this.state.nav,
          autoplay: this.state.autoplay,
          borderstyle: this.state.borderStyle,
        };
        this.updateCol();
      },
      () => [
        this.state.selectedTemplate,
        this.state.limit,
        this.state.selectedType,
        this.state.borderStyle,
        this.state.selectedButton,
        this.state.dost,
        this.state.autoplay,
        this.state.nav,
      ]
    );
    onWillStart(async () => {
      this.state.data = this.props.data;
      this.state.selectedCol = this.props.selectedCol;
      this.state.colValue = [].concat(...this.state.data).find((ele) => ele?._uid == this.state.selectedCol);
      this.state.model = this?.state?.colValue?.data?.model;
      if (this.state.model == 'product.public.category') {
        this.state.selectTemplate = 'dy_categ_tmp_style_1_bits'
      } else if (this.state.model == 'blog.post') {
        this.state.selectTemplate = 'dy_blog_tmp_style_1_bits'
      }

      if (this?.state?.colValue?.visual?.template)
        this.state.selectedTemplate = this?.state?.colValue?.visual?.template;

      if (this.state.model == 'product.template') {
        this.state.templates = TEMPATE.filter((t) => t.tmp_for == 'product');
      }
      if (this.state.model == 'product.public.category') {
        this.state.templates = TEMPATE.filter((t) => t.tmp_for == 'category');
      }
      if (this.state.model == 'blog.post') {
        this.state.templates = TEMPATE.filter((t) => t.tmp_for == 'blog');
      }
      this.state.limit = this?.state?.colValue?.visual?.limit || 4;
      this.state.selectedType = this?.state?.colValue?.visual?.type || "grid";
      this.state.selectedButton = this?.state?.colValue?.visual?.buttons || [];
      this.state.dost = this?.state?.colValue?.visual?.dost || false;
      this.state.nav = this?.state?.colValue?.visual?.nav || true;
      this.state.autoplay = this?.state?.colValue?.visual?.autoplay || false;
      this.state.borderStyle = this?.state?.colValue?.visual?.borderstyle || 'rounded';
    });
  }

  selectTemplate(template) {
    this.state.selectedTemplate = template.id;
    this.updateCol();
  }
  selectCategory(catgoryId) {
    this.state.selectedCategory = catgoryId
    this.updateCol();
  }
  updateCol() {
    const data = this.state.data.map((row) => {
      return row.map((col) => {
        if (col?._uid == this.state.selectedCol) {
          col.visual = this.state.visual;
        }
        return col;
      });
    });
    this.props.update(data);
  }

  toggleBtn(type) {
    if (this.state.selectedButton.includes(type)) {
      const index = this.state.selectedButton.findIndex((data) => data == type);
      this.state.selectedButton = [
        ...this.state.selectedButton.slice(0, index),
        ...this.state.selectedButton.slice(index + 1),
      ];
    } else {
      this.state.selectedButton.push(type);
    }
  }
}

DynamicSnippetVisual.components = {};
DynamicSnippetVisual.template = "theme_crest.DynamicSnippetVisual";
