/** @odoo-module **/

import {
  Component,
  useEffect,
  useState,
  onWillStart,
} from "@odoo/owl";
import { SearchSnippet } from "../searchSnippet/searchSnippet";
import { useService } from "@web/core/utils/hooks";
import { DomainSnippet } from "../domainSnippet/domainSnippet";
import { DEFAULT_TEMPLATE, ORDER_BY } from "../utils";

export class DynamicSnippetData extends Component {
  setup() {
    this.state = useState({
      isAddRow: false,
      colValue: false,
      data: [],
      selectedDomainData: {},
      selectedCol: false,
      selectedModel: 'product.template',
      selectedMode: "manual",
      selectedRecords: [],
    });
    this.orm = useService("orm");
    onWillStart(async () => {
      this.state.data = this.props.data;
      this.state.selectedCol = this.props.selectedCol;
      this.state.colValue = []
        .concat(...this.state.data)
        .find((ele) => ele?._uid == this.state.selectedCol);
      if (this?.state?.colValue?.data?.template) {
        this.state.selectedMode = "advance";
      } else {
        this.state.selectedMode = "manual";
      }
      await this.getData();
    });

    useEffect(
      () => {
        if (this.state.selectedModel && this.state.selectedMode == "advance")
          this.getRecords();
      },
      () => [this.state.domaindata]
    );
  }

  async onSearchInput(ev) {
    let domain = this.props.model == 'product.public.category' ? [["name", "ilike", ev.target.value]] : [["name", "ilike", ev.target.value], ["is_published", "=", true]];
    const res = await this.orm.call(this.props.model, "search_read", [], {
      domain: domain, fields: ["id", "name"], limit: 5,
    });
    this.state.records = res;
  }

  async getData() {
    this.state.selectedModel = this?.state?.colValue?.data?.model ? this?.state?.colValue?.data?.model : false;
    const records = this?.state?.colValue?.data?.records
      ? this?.state?.colValue?.data?.records
      : [];
    if (records.length > 0 && this.state.selectedModel) {
      if (this.state.selectedModel == "blog.post") {
        const domain = [["id", "in", [...records]], ["is_published", "=", true]];
        const res = await this.orm.call(
          this.state.selectedModel,
          "search_read",
          [],
          {
            domain: domain,
            fields: ["id", "name", "cover_properties"],
            limit: 5,
          }
        );
        const updatedRecords = res.map((record) => {
          let background = JSON.parse(record.cover_properties)['background-image']
          record.cover_properties = background
          return record
        })
        this.state.selectedRecords = updatedRecords;

      } else {
        let domain = this.state.selectedModel == 'product.public.category' ? [["id", "in", [...records]]] :[["id", "in", [...records]], ["is_published", "=", true]];
        const res = await this.orm.call(
          this.state.selectedModel,
          "search_read",
          [],
          {
            domain: domain,
            fields: ["id", "name"],
            limit: 5,
          }
        );
        this.state.selectedRecords = res;
      }

    }
  }

  updateCol(removeData = false) {
    const data = this.state.data.map((row) => {
      return row.map((col) => {
        if (col?._uid == this.state.selectedCol) {
          if (!removeData) {
            if (this.state.selectedModel == "static_template") {
              col.data = {
                model: this.state.selectedModel,
              };
              return col;
            }
            if (this.state.selectedMode == "manual")
              col.data = {
                records: this.state.selectedRecords.map((ele) => ele.id),
                model: this.state.selectedModel,
              };
            else

              col.data = {
                ...this.state.domaindata,
                model: this.state.selectedModel,
                records: this.state.selectedRecords.map((ele) => ele.id),
                template: ''
              };
            if (this.state.selectModel != 'product.template') {
              col.visual = {}
            }
          } else col.data = {};
        }
        return col;
      });
    });
    this.props.update(data);
  }

  selectModel(model) {
    this.state.selectedRecords = [];
    this.state.selectedMode = "manual";
    this.state.selectedModel = model;
    this.updateCol();
  }

  selectMode(mode) {
    this.state.selectedRecords = [];
    this.state.selectedMode = mode;
    this.updateCol();
  }
  addRecord(record) {
    if (
      this.state.selectedRecords.length > 0 &&
      this.state.selectedRecords.findIndex((ele) => ele.id == record.id) >= 0
    )
      return;
    this.state.selectedRecords.push(record);
    this.updateCol();
  }

  addRecords(records) {
    this.state.selectedRecords = records;
    this.updateCol();
  }

  deleteRecord(index) {
    this.state.selectedRecords = [
      ...this.state.selectedRecords.slice(0, index),
      ...this.state.selectedRecords.slice(index + 1),
    ];
    this.updateCol();
  }

  addDomain(domainData) {

    this.state.domaindata = domainData;
    this.updateCol();
  }

  async getRecords() {
    let order = "";

    if (this?.state?.domaindata?.template == "default") {
      order = this?.state?.domaindata?.order;
    }
    else {
      order = DEFAULT_TEMPLATE.find((ele) => ele.id == this?.state?.domaindata?.template)?.orderBy;
    }
    if (order) {
      const domain = [["is_published", "=", true]];
      if (this.state.selectedModel == "blog.post") {
        const res = await this.orm.call(
          this.state.selectedModel,
          "search_read",
          [],
          {
            domain: domain,
            order: order,
            fields: ["id", "name", "cover_properties"],
            limit: this?.state?.domaindata?.limit,
          }
        );

        const updatedRecords = res.map((record) => {
          let background = JSON.parse(record.cover_properties)['background-image']
          record.cover_properties = background

          return record
        })
        this.state.selectedRecords = updatedRecords;

      } else {
        let domain = this.state.selectedModel == 'product.public.category' ? [] : [["is_published", "=", true]];
        const res = await this.orm.call(
          this.state.selectedModel,
          "search_read",
          [],
          {
            domain: domain,
            order: order,
            fields: ["id", "name"],
            limit: this?.state?.domaindata?.limit,
          }
        );
        this.state.selectedRecords = res;
      }
      this.updateCol();

    }
  }
}

DynamicSnippetData.components = { SearchSnippet, DomainSnippet };
DynamicSnippetData.template = "theme_crest.DynamicSnippetData";
