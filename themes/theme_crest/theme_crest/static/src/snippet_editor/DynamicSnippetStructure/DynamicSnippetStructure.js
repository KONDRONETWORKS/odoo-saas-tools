/** @odoo-module **/
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import {
  Component,
  useState, useEffect,
  onWillStart,
} from "@odoo/owl";
export class DynamicSnippetStructure extends Component {
  setup() {
    this.dialogService = useService("dialog");
    this.state = useState({ isAddRow: false, colValue: false, data: [], selectedColumns: [], deleteData: true });
    onWillStart(() => {
      this.state.data = this.props?.data;
    });
    useEffect(
      () => {
        if (this.state.data.length == 0) {
          this.state.deleteData = true
        } else {
          this.state.deleteData = false
        }
      },
      () => [
        this.state.deleteData
      ])
  }

  onAddRowClicked() {
    this.state.isAddRow = true;
    if (!this.state.colValue) this.state.colValue = 1;
  }

  colValueChanged(ev) {
    this.state.colValue = Number(ev.target.value);
  }

  onAddColClick() {
    let arr = [];
    for (let i = 0; i < this.state.colValue; i++) {
      arr.push({
        class: `col-${12 / this.state.colValue}`,
        _uid: this.getRandomUid(),
        container: false,
      });
    }
    this.state.deleteData = false
    this.state.data.push(arr);
    this.state.isAddRow = false;
    this.state.colValue = false;
    this.props.update(this.state.data);
  }
  toggleColumnSelection(uid, index_row) {
    if (!this.state.selectedColumns[index_row]) {
      this.state.selectedColumns[index_row] = [];
    }
    let selectedColumnsForRow = this.state.selectedColumns[index_row];
    const index = selectedColumnsForRow.indexOf(uid);
    if (index === -1) {
      selectedColumnsForRow.push(uid);
    } else {
      selectedColumnsForRow.splice(index, 1);
    }
  }
  mergeColumns(index_row) {
    const selectedInRow = this.state.selectedColumns[index_row];
    if (!selectedInRow || selectedInRow.length >= 2) {
      this.dialogService.add(ConfirmationDialog, {
        body: _t("Are you sure you want to merge selected columns? The column data will be erased after the merge."),
        confirmClass: "btn s_o_btn-primary",
        confirmLabel: _t("ok"),
        confirm: () => {
          this.state.data = this.state.data.map((row, currentRowIndex) => {
            if (currentRowIndex === index_row) {
              const newRow = [];
              let totalWidth = 0;
              const mergedData = [];
              let firstId = null;
              let indexAdd = 0;
              row.forEach((col, pos) => {
                if (selectedInRow.includes(col?._uid)) {
                  const colWidth = Number(col.class.replace("col-", ""));
                  totalWidth += colWidth;

                  if (!firstId) {
                    firstId = col?._uid;
                    indexAdd = pos;
                  }
                  if (col.data) {
                    mergedData.push(...(Array.isArray(col.data) ? col.data : [col.data]));
                  }
                } else {
                  newRow.push(col);
                }
              });

              totalWidth = Math.min(totalWidth, 12);
              if (firstId) {
                newRow.splice(indexAdd, 0, {
                  _uid: firstId,
                  class: `col-${totalWidth}`,
                  data: {
                    "model": "static_template"
                  },
                  visual: {
                    "template": "theme_crest.not_data_available",
                    "limit": 4,
                    "type": "grid",
                    "buttons": [],
                    "dost": false,
                    "nav": true,
                    "autoplay": false,
                    "borderstyle": "rounded",
                  },
                  container: false,
                });
              }
              return newRow;
            } else {
              return row;
            }
          });
          this.props.update(this.state.data);
          this.state.selectedColumns[index_row] = [];
        },
        cancelLabel: _t("Cancel"),
        cancel: () => { },
      })
    }
  }

  deleteRow(index) {
    this.state.data = [
      ...this.state.data.slice(0, index),
      ...this.state.data.slice(index + 1),
    ];
    if (this.state?.data.length == 0) {
      this.state.deleteData = true
    }
    this.props.update(this.state.data);
  }

  resetData(uid) {
    this.state.data = this.state.data.map((row) => {
      return row.map((col) => {
        if (col._uid == uid) {
          delete col.data;
          delete col.visual;
        }
        return col;
      });
    });
  }
  selectContainer(index, ev) {
    this.state.data = this.state.data.map((row, pos) => {
      if (pos == index) {
        return row.map((col) => {
          let clickValue = col.container;
          if (!clickValue) {
            col.container = true
          } else {
            col.container = false
          }
          return col;
        });
      } else {
        return row
      }
    });

  }
  getRandomUid() {
    var S4 = function () {
      return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    };
    return S4();
  }
}

DynamicSnippetStructure.components = { Dialog };
DynamicSnippetStructure.template = "theme_crest.DynamicSnippetStructure";
