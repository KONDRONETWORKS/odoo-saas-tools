/** @odoo-module **/

import {
  Component, 
  useState, 
} from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { DOMAIN_TEMPLATE } from "../utils";

export class Domain extends Component {
  setup() {
    this.state = useState({
      domainTemplate: DOMAIN_TEMPLATE,
      selectedField: "name",
      selectedOperator: "ilike",
      value: "",
      records: [],
      timeoutlId: false,
      showDomain: false,
    });
    this.orm = useService("orm");
  }

  async onSearchInput(ev) {}

  showDomain(id = false) {
    this.state.showDomain = true;
    this.state.record.push([this.state.selectedField,this.state.selectedOperator,]);
    if (!id) {
      this.state = {
        ...this.state,
        selectedField: "name",
        selectedOperator: "ilike",
        value: "",
      };
    } else {
    }
  }
}

Domain.components = {};
Domain.template = "theme_crest.Domain";
