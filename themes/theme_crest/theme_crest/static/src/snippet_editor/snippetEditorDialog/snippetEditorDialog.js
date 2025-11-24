/** @odoo-module **/

import { Dialog } from "@web/core/dialog/dialog";
import { Component, useEffect, useState, onWillStart, useRef, toRaw, onWillUpdateProps } from "@odoo/owl";

import { DynamicSnippetStructure } from "../DynamicSnippetStructure/DynamicSnippetStructure";
import { DynamicSnippetData } from "../dynamicSnippetData/dynamicSnippetData";
import { DynamicSnippetVisual } from "../dynamicSnippetVisual/dynamicSnippetVisual";
import { DynamicSnippetPreview } from "../dynamicSnippetPreview/dynamicSnippetPreview";

export class ThemeDialog extends Dialog {
  setup() {
    super.setup();
    useEffect(
      () => {
        this.modalRef.el.classList.add("theme-bits-dialog");
        if (this.modalRef.el.querySelector(".modal-dialog").classList.contains("modal-xl")) {
          this.modalRef.el.querySelector(".modal-dialog").classList.remove("modal-xl");
          this.modalRef.el.querySelector(".modal-dialog").classList.add("modal-container", "p-0");
        }
      },
      () => []
    );
  }
}
ThemeDialog.components = { ...Dialog.components };
ThemeDialog.props = { ...Dialog.props };

export class SnippetEditorDialog extends Component {
  setup() {
    this.state = useState({
      data: [],
      selectedCol: false,
      selectedTab: "structure",
    });
    onWillStart(() => {
      if (this.props.data) this.state.data = this.props.data;
    });
 
  }

  closeDialog() {
    this.props.close();
  }

  close_dialog() {
    this.closeDialog();
  }
  confirm_edit() {
    this.state.selectedTab = 'structure'
    this.props.save(this.state.data);
    this.close_dialog()
  }
  selectCol(col) {
    this.state.selectedCol = col;
    this.state.selectedTab = "data_visuals";
  }

  updateData(data) {
    this.state.data = data;
  }

  hasData() {
    if (!this.state.selectedCol) return true;
    const data = []
      .concat(...this.state.data)
      .find((ele) => ele?._uid == this.state.selectedCol)?.data;
    if (data?.model == "static_template") return false;
    if (data?.template) return false;
    if (data?.records && data?.records?.length > 0) return false;
    return true;
  }
  hasSaveData() {
    const flattenedData = [].concat(...this.state.data);

    const isDataValid = flattenedData.some(item => {
      if (item?.data?.model == "static_template") {
        return item?.data?.model == "static_template"
      } else {
        return item?.data?.model && item.data?.records?.length > 0
      }

    });
    if (!isDataValid) {
      this.props.data = []
      this.props.save(this.props.data)

    }
    return !isDataValid;
  }

}

SnippetEditorDialog.components = {
  ThemeDialog,
  DynamicSnippetStructure,
  DynamicSnippetData,
  DynamicSnippetVisual,
  DynamicSnippetPreview
};
SnippetEditorDialog.template = "theme_crest.SnippetEditorDialog";
