/** @odoo-module **/
import { debounce } from "@web/core/utils/timing";
import { KeepLast } from "@web/core/utils/concurrency";
import { Component, useState, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class SearchSnippet extends Component {
  setup() {
    this.state = useState({ records: [], timeoutlId: false });
    this.inputref = useRef("inputRef");
    this.orm = useService("orm");
    this.keepLast = new KeepLast();
    this.debounceSerach = debounce(this.onSearchInput.bind(this), 250);
  }
  async onSearchInput(value) {
    if (!value) {
      this.state.records = [];
    } else {
      this.keepLast.add(this._fetch(value));
    }
  }
  async _fetch(value) {
    if (value) {
      
      let domain = this.props.model == 'product.public.category' ? [["name", "ilike", value]] : [["name", "ilike", value], ["is_published", "=", true]];
      if (this.props.model == "blog.post") {
        const res = await this.orm.call(this.props.model, "search_read", [], {
          domain: domain,
          fields: ["id", "name", "cover_properties",],
        });
        const updatedRecords = res.map((record) => {
          let background = JSON.parse(record.cover_properties)['background-image']
          record.cover_properties = background
          return record
        })
        this.state.records = updatedRecords;
      } else {
        
        const res = await this.orm.call(this.props.model, "search_read", [], {
          domain: domain,
          fields: ["id", "name"],
        });
        this.state.records = res;
      }

    }
  }
  get SerchFor() {
    if (this.props.model == 'product.template') {
      return 'Products'
    } else if (this.props.model == 'product.public.category') {
      return 'Product Categories'
    } else if (this.props.model == 'blog.post') {
      return 'Blogs'
    } else {
      return ''
    }
  }
}

SearchSnippet.components = {};
SearchSnippet.template = "theme_crest.SearchSnippet";
