/** @odoo-module **/

import { Component, useEffect, useState, onWillStart } from "@odoo/owl";
import { DEFAULT_TEMPLATE, ORDER_BY } from "../utils";
import { Domain } from "../domain/Domain";

export class DomainSnippet extends Component {
  setup() {
    this.state = useState({
      orderBy: ORDER_BY,
      defaulTemplate: DEFAULT_TEMPLATE,
      limit: 10,
      selectedOrder: "",
      selectedTemplate: this.props.model != "product.template" ? "a_to_z" : "new-arrival",
      isInitaited: false,
    });

    useEffect(
      () => {
        if (this.state.isInitaited) {
          const data = {
            order: this.state.selectedOrder,
            template: this.state.selectedTemplate,
            limit: this.state.limit,
          };
          this.props.addDomain(data);
        }
      },
      () => [
        this.state.selectedOrder,
        this.state.selectedTemplate,
        this.state.limit,
      ]
    );

    onWillStart(async () => {
      let template_for = this.get_temp_for();
      this.state.defaulTemplate = this.state.defaulTemplate.filter((i) => i.tmp_for == template_for);
      if (this?.props?.colValue?.data?.template) {
        this.state.selectedOrder = this?.props?.colValue?.data?.order;
        this.state.selectedTemplate = this?.props?.colValue?.data?.template;
        this.state.limit = this?.props?.colValue?.data?.limit;
      }
      this.state.isInitaited = true;
    });
  }
  get_temp_for() {
    let template_for = ''
    if (this.props.model == 'product.public.category') {
      template_for = 'category';
    }
    if (this.props.model == 'product.template') {
      template_for = 'product';
    }
    if (this.props.model == 'blog.post') {
      template_for = 'blog';
    }
    return template_for;
  }
}

DomainSnippet.components = { Domain };
DomainSnippet.template = "theme_crest.DomainSnippet";
