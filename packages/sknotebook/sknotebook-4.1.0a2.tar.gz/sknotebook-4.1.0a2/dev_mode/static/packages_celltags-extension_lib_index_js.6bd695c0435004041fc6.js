"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_celltags-extension_lib_index_js"],{

/***/ "../packages/celltags-extension/lib/celltag.js":
/*!*****************************************************!*\
  !*** ../packages/celltags-extension/lib/celltag.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellTagField": () => (/* binding */ CellTagField)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */




/**
 * The class name added to the cell-tags field.
 */
const CELL_TAGS_WIDGET_CLASS = 'jp-CellTags';
/**
 * The class name added to each tag element.
 */
const CELL_TAGS_ELEMENT_CLASS = 'jp-CellTags-Tag';
/**
 * The class name added to each applied tag element.
 */
const CELL_TAGS_ELEMENT_APPLIED_CLASS = 'jp-CellTags-Applied';
/**
 * The class name added to each unapplied tag element.
 */
const CELL_TAGS_ELEMENT_UNAPPLIED_CLASS = 'jp-CellTags-Unapplied';
/**
 * The class name added to the tag holder.
 */
const CELL_TAGS_HOLDER_CLASS = 'jp-CellTags-Holder';
/**
 * The class name added to the add-tag input.
 */
const CELL_TAGS_ADD_CLASS = 'jp-CellTags-Add';
/**
 * The class name added to an empty input.
 */
const CELL_TAGS_EMPTY_CLASS = 'jp-CellTags-Empty';
class CellTagField {
    constructor(tracker, translator) {
        this._tracker = tracker;
        this._translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        this._trans = this._translator.load('jupyterlab');
        this._editing = false;
    }
    addTag(props, tag) {
        const data = props.formData;
        if (tag && !data.includes(tag)) {
            data.push(tag);
            props.formContext.updateMetadata({ [props.name]: data }, true);
        }
    }
    /**
     * Pull from cell metadata all the tags used in the notebook and update the
     * stored tag list.
     */
    pullTags() {
        var _a, _b;
        const notebook = (_a = this._tracker) === null || _a === void 0 ? void 0 : _a.currentWidget;
        const cells = (_b = notebook === null || notebook === void 0 ? void 0 : notebook.model) === null || _b === void 0 ? void 0 : _b.cells;
        if (cells === undefined) {
            return [];
        }
        const allTags = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_2__.reduce)(cells, (allTags, cell) => {
            var _a;
            const tags = (_a = cell.getMetadata('tags')) !== null && _a !== void 0 ? _a : [];
            return [...allTags, ...tags];
        }, []);
        return [...new Set(allTags)].filter(tag => tag !== '');
    }
    _emptyAddTag(target) {
        target.value = '';
        target.style.width = '';
        target.classList.add(CELL_TAGS_EMPTY_CLASS);
    }
    _onAddTagKeyDown(props, event) {
        const input = event.target;
        if (event.ctrlKey)
            return;
        if (event.key === 'Enter') {
            this.addTag(props, input.value);
        }
        else if (event.key === 'Escape') {
            this._emptyAddTag(input);
        }
    }
    _onAddTagFocus(event) {
        if (!this._editing) {
            event.target.blur();
        }
    }
    _onAddTagBlur(input) {
        if (this._editing) {
            this._editing = false;
            this._emptyAddTag(input);
        }
    }
    _onChange(event) {
        if (!event.target.value) {
            this._emptyAddTag(event.target);
        }
        else {
            event.target.classList.remove(CELL_TAGS_EMPTY_CLASS);
            const tmp = document.createElement('span');
            tmp.className = CELL_TAGS_ADD_CLASS;
            tmp.textContent = event.target.value;
            // set width to the pixel length of the text
            document.body.appendChild(tmp);
            event.target.style.setProperty('width', `calc(${tmp.getBoundingClientRect().width}px + var(--jp-add-tag-extra-width))`);
            document.body.removeChild(tmp);
        }
    }
    _onAddTagClick(props, event) {
        const elem = event.target.closest('div');
        const input = elem === null || elem === void 0 ? void 0 : elem.childNodes[0];
        if (!this._editing) {
            this._editing = true;
            input.value = '';
            input.focus();
        }
        else if (event.target !== input) {
            this.addTag(props, input.value);
        }
        event.preventDefault();
    }
    _onTagClick(props, tag) {
        const data = props.formData;
        if (data.includes(tag)) {
            data.splice(data.indexOf(tag), 1);
        }
        else {
            data.push(tag);
        }
        props.formContext.updateMetadata({ [props.name]: data }, true);
    }
    render(props) {
        const allTags = this.pullTags();
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: CELL_TAGS_WIDGET_CLASS },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, "Cell Tags"),
            allTags &&
                allTags.map((tag, i) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { key: i, className: `${CELL_TAGS_ELEMENT_CLASS} ${props.formData.includes(tag)
                        ? CELL_TAGS_ELEMENT_APPLIED_CLASS
                        : CELL_TAGS_ELEMENT_UNAPPLIED_CLASS}`, onClick: () => this._onTagClick(props, tag) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: CELL_TAGS_HOLDER_CLASS },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("span", null, tag),
                        props.formData.includes(tag) && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon.resolveReact, { icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.checkIcon, tag: "span", elementPosition: "center", height: "18px", width: "18px", marginLeft: "5px", marginRight: "-3px" })))))),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: `${CELL_TAGS_ELEMENT_CLASS} ${CELL_TAGS_ELEMENT_UNAPPLIED_CLASS}` },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: CELL_TAGS_HOLDER_CLASS, onMouseDown: (e) => this._onAddTagClick(props, e) },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: `${CELL_TAGS_ADD_CLASS} ${CELL_TAGS_EMPTY_CLASS}`, type: "text", placeholder: this._trans.__('Add Tag'), onKeyDown: (e) => this._onAddTagKeyDown(props, e), onFocus: (e) => this._onAddTagFocus(e), onBlur: (e) => this._onAddTagBlur(e.target), onChange: (e) => {
                            this._onChange(e);
                        } }),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon.resolveReact, { icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.addIcon, tag: "span", height: "18px", width: "18px", marginLeft: "5px", marginRight: "-3px" })))));
    }
}


/***/ }),

/***/ "../packages/celltags-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/celltags-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _celltag__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./celltag */ "../packages/celltags-extension/lib/celltag.js");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module celltags-extension
 */



/**
 * Registering cell tag field.
 */
const customCellTag = {
    id: '@jupyterlab/celltags-extension:plugin',
    description: 'Adds the cell tags editor.',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    optional: [_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.IFormRendererRegistry],
    activate: (app, tracker, formRegistry) => {
        // Register the custom field
        if (formRegistry) {
            const component = {
                fieldRenderer: (props) => {
                    return new _celltag__WEBPACK_IMPORTED_MODULE_2__.CellTagField(tracker).render(props);
                }
            };
            formRegistry.addRenderer('@jupyterlab/celltags-extension:plugin.renderer', component);
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([customCellTag]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY2VsbHRhZ3MtZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy42YmQ2OTVjMDQzNTAwNDA0MWZjNi5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7O0dBR0c7QUFFdUI7QUFHOEM7QUFDN0I7QUFLVjtBQUVqQzs7R0FFRztBQUNILE1BQU0sc0JBQXNCLEdBQUcsYUFBYSxDQUFDO0FBQzdDOztHQUVHO0FBQ0gsTUFBTSx1QkFBdUIsR0FBRyxpQkFBaUIsQ0FBQztBQUNsRDs7R0FFRztBQUNILE1BQU0sK0JBQStCLEdBQUcscUJBQXFCLENBQUM7QUFDOUQ7O0dBRUc7QUFDSCxNQUFNLGlDQUFpQyxHQUFHLHVCQUF1QixDQUFDO0FBQ2xFOztHQUVHO0FBQ0gsTUFBTSxzQkFBc0IsR0FBRyxvQkFBb0IsQ0FBQztBQUNwRDs7R0FFRztBQUNILE1BQU0sbUJBQW1CLEdBQUcsaUJBQWlCLENBQUM7QUFDOUM7O0dBRUc7QUFDSCxNQUFNLHFCQUFxQixHQUFHLG1CQUFtQixDQUFDO0FBRTNDLE1BQU0sWUFBWTtJQUN2QixZQUFZLE9BQXlCLEVBQUUsVUFBd0I7UUFDN0QsSUFBSSxDQUFDLFFBQVEsR0FBRyxPQUFPLENBQUM7UUFDeEIsSUFBSSxDQUFDLFdBQVcsR0FBRyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUNoRCxJQUFJLENBQUMsTUFBTSxHQUFHLElBQUksQ0FBQyxXQUFXLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQ2xELElBQUksQ0FBQyxRQUFRLEdBQUcsS0FBSyxDQUFDO0lBQ3hCLENBQUM7SUFFRCxNQUFNLENBQUMsS0FBaUIsRUFBRSxHQUFXO1FBQ25DLE1BQU0sSUFBSSxHQUFHLEtBQUssQ0FBQyxRQUFRLENBQUM7UUFDNUIsSUFBSSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLEdBQUcsQ0FBQyxFQUFFO1lBQzlCLElBQUksQ0FBQyxJQUFJLENBQUMsR0FBRyxDQUFDLENBQUM7WUFDZixL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Q0FBdUM7SUFDM0MsV0FBVyxFQUFFLDRCQUE0QjtJQUN6QyxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLGtFQUFnQixDQUFDO0lBQzVCLFFBQVEsRUFBRSxDQUFDLDRFQUFxQixDQUFDO0lBQ2pDLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLE9BQXlCLEVBQ3pCLFlBQW9DLEVBQ3BDLEVBQUU7UUFDRiw0QkFBNEI7UUFDNUIsSUFBSSxZQUFZLEVBQUU7WUFDaEIsTUFBTSxTQUFTLEdBQWtCO2dCQUMvQixhQUFhLEVBQUUsQ0FBQyxLQUFpQixFQUFFLEVBQUU7b0JBQ25DLE9BQU8sSUFBSSxrREFBWSxDQUFDLE9BQU8sQ0FBQyxDQUFDLE1BQU0sQ0FBQyxLQUFLLENBQUMsQ0FBQztnQkFDakQsQ0FBQzthQUNGLENBQUM7WUFDRixZQUFZLENBQUMsV0FBVyxDQUN0QixnREFBZ0QsRUFDaEQsU0FBUyxDQUNWLENBQUM7U0FDSDtJQUNILENBQUM7Q0FDRixDQUFDO0FBRUYsaUVBQWUsQ0FBQyxhQUFhLENBQUMsRUFBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jZWxsdGFncy1leHRlbnNpb24vc3JjL2NlbGx0YWcudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jZWxsdGFncy1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qXG4gKiBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbiAqIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4gKi9cblxuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IEZpZWxkUHJvcHMgfSBmcm9tICdAcmpzZi91dGlscyc7XG5pbXBvcnQgeyBJTm90ZWJvb2tUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbm90ZWJvb2snO1xuaW1wb3J0IHsgYWRkSWNvbiwgY2hlY2tJY29uLCBMYWJJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyByZWR1Y2UgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byB0aGUgY2VsbC10YWdzIGZpZWxkLlxuICovXG5jb25zdCBDRUxMX1RBR1NfV0lER0VUX0NMQVNTID0gJ2pwLUNlbGxUYWdzJztcbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gZWFjaCB0YWcgZWxlbWVudC5cbiAqL1xuY29uc3QgQ0VMTF9UQUdTX0VMRU1FTlRfQ0xBU1MgPSAnanAtQ2VsbFRhZ3MtVGFnJztcbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gZWFjaCBhcHBsaWVkIHRhZyBlbGVtZW50LlxuICovXG5jb25zdCBDRUxMX1RBR1NfRUxFTUVOVF9BUFBMSUVEX0NMQVNTID0gJ2pwLUNlbGxUYWdzLUFwcGxpZWQnO1xuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBlYWNoIHVuYXBwbGllZCB0YWcgZWxlbWVudC5cbiAqL1xuY29uc3QgQ0VMTF9UQUdTX0VMRU1FTlRfVU5BUFBMSUVEX0NMQVNTID0gJ2pwLUNlbGxUYWdzLVVuYXBwbGllZCc7XG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSB0YWcgaG9sZGVyLlxuICovXG5jb25zdCBDRUxMX1RBR1NfSE9MREVSX0NMQVNTID0gJ2pwLUNlbGxUYWdzLUhvbGRlcic7XG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSBhZGQtdGFnIGlucHV0LlxuICovXG5jb25zdCBDRUxMX1RBR1NfQUREX0NMQVNTID0gJ2pwLUNlbGxUYWdzLUFkZCc7XG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGFuIGVtcHR5IGlucHV0LlxuICovXG5jb25zdCBDRUxMX1RBR1NfRU1QVFlfQ0xBU1MgPSAnanAtQ2VsbFRhZ3MtRW1wdHknO1xuXG5leHBvcnQgY2xhc3MgQ2VsbFRhZ0ZpZWxkIHtcbiAgY29uc3RydWN0b3IodHJhY2tlcjogSU5vdGVib29rVHJhY2tlciwgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yKSB7XG4gICAgdGhpcy5fdHJhY2tlciA9IHRyYWNrZXI7XG4gICAgdGhpcy5fdHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLl90cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLl9lZGl0aW5nID0gZmFsc2U7XG4gIH1cblxuICBhZGRUYWcocHJvcHM6IEZpZWxkUHJvcHMsIHRhZzogc3RyaW5nKSB7XG4gICAgY29uc3QgZGF0YSA9IHByb3BzLmZvcm1EYXRhO1xuICAgIGlmICh0YWcgJiYgIWRhdGEuaW5jbHVkZXModGFnKSkge1xuICAgICAgZGF0YS5wdXNoKHRhZyk7XG4gICAgICBwcm9wcy5mb3JtQ29udGV4dC51cGRhdGVNZXRhZGF0YSh7IFtwcm9wcy5uYW1lXTogZGF0YSB9LCB0cnVlKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogUHVsbCBmcm9tIGNlbGwgbWV0YWRhdGEgYWxsIHRoZSB0YWdzIHVzZWQgaW4gdGhlIG5vdGVib29rIGFuZCB1cGRhdGUgdGhlXG4gICAqIHN0b3JlZCB0YWcgbGlzdC5cbiAgICovXG4gIHB1bGxUYWdzKCk6IHN0cmluZ1tdIHtcbiAgICBjb25zdCBub3RlYm9vayA9IHRoaXMuX3RyYWNrZXI/LmN1cnJlbnRXaWRnZXQ7XG4gICAgY29uc3QgY2VsbHMgPSBub3RlYm9vaz8ubW9kZWw/LmNlbGxzO1xuICAgIGlmIChjZWxscyA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICByZXR1cm4gW107XG4gICAgfVxuICAgIGNvbnN0IGFsbFRhZ3MgPSByZWR1Y2UoXG4gICAgICBjZWxscyxcbiAgICAgIChhbGxUYWdzOiBzdHJpbmdbXSwgY2VsbCkgPT4ge1xuICAgICAgICBjb25zdCB0YWdzOiBzdHJpbmdbXSA9IChjZWxsLmdldE1ldGFkYXRhKCd0YWdzJykgYXMgc3RyaW5nW10pID8/IFtdO1xuICAgICAgICByZXR1cm4gWy4uLmFsbFRhZ3MsIC4uLnRhZ3NdO1xuICAgICAgfSxcbiAgICAgIFtdXG4gICAgKTtcbiAgICByZXR1cm4gWy4uLm5ldyBTZXQoYWxsVGFncyldLmZpbHRlcih0YWcgPT4gdGFnICE9PSAnJyk7XG4gIH1cblxuICBwcml2YXRlIF9lbXB0eUFkZFRhZyh0YXJnZXQ6IEhUTUxJbnB1dEVsZW1lbnQpIHtcbiAgICB0YXJnZXQudmFsdWUgPSAnJztcbiAgICB0YXJnZXQuc3R5bGUud2lkdGggPSAnJztcbiAgICB0YXJnZXQuY2xhc3NMaXN0LmFkZChDRUxMX1RBR1NfRU1QVFlfQ0xBU1MpO1xuICB9XG5cbiAgcHJpdmF0ZSBfb25BZGRUYWdLZXlEb3duKFxuICAgIHByb3BzOiBGaWVsZFByb3BzLFxuICAgIGV2ZW50OiBSZWFjdC5LZXlib2FyZEV2ZW50PEhUTUxJbnB1dEVsZW1lbnQ+XG4gICkge1xuICAgIGNvbnN0IGlucHV0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxJbnB1dEVsZW1lbnQ7XG5cbiAgICBpZiAoZXZlbnQuY3RybEtleSkgcmV0dXJuO1xuXG4gICAgaWYgKGV2ZW50LmtleSA9PT0gJ0VudGVyJykge1xuICAgICAgdGhpcy5hZGRUYWcocHJvcHMsIGlucHV0LnZhbHVlKTtcbiAgICB9IGVsc2UgaWYgKGV2ZW50LmtleSA9PT0gJ0VzY2FwZScpIHtcbiAgICAgIHRoaXMuX2VtcHR5QWRkVGFnKGlucHV0KTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9vbkFkZFRhZ0ZvY3VzKGV2ZW50OiBSZWFjdC5Gb2N1c0V2ZW50PEhUTUxJbnB1dEVsZW1lbnQ+KSB7XG4gICAgaWYgKCF0aGlzLl9lZGl0aW5nKSB7XG4gICAgICAoZXZlbnQudGFyZ2V0IGFzIEhUTUxJbnB1dEVsZW1lbnQpLmJsdXIoKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9vbkFkZFRhZ0JsdXIoaW5wdXQ6IEhUTUxJbnB1dEVsZW1lbnQpIHtcbiAgICBpZiAodGhpcy5fZWRpdGluZykge1xuICAgICAgdGhpcy5fZWRpdGluZyA9IGZhbHNlO1xuICAgICAgdGhpcy5fZW1wdHlBZGRUYWcoaW5wdXQpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX29uQ2hhbmdlKGV2ZW50OiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MSW5wdXRFbGVtZW50Pikge1xuICAgIGlmICghZXZlbnQudGFyZ2V0LnZhbHVlKSB7XG4gICAgICB0aGlzLl9lbXB0eUFkZFRhZyhldmVudC50YXJnZXQpO1xuICAgIH0gZWxzZSB7XG4gICAgICBldmVudC50YXJnZXQuY2xhc3NMaXN0LnJlbW92ZShDRUxMX1RBR1NfRU1QVFlfQ0xBU1MpO1xuICAgICAgY29uc3QgdG1wID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc3BhbicpO1xuICAgICAgdG1wLmNsYXNzTmFtZSA9IENFTExfVEFHU19BRERfQ0xBU1M7XG4gICAgICB0bXAudGV4dENvbnRlbnQgPSBldmVudC50YXJnZXQudmFsdWU7XG4gICAgICAvLyBzZXQgd2lkdGggdG8gdGhlIHBpeGVsIGxlbmd0aCBvZiB0aGUgdGV4dFxuICAgICAgZG9jdW1lbnQuYm9keS5hcHBlbmRDaGlsZCh0bXApO1xuICAgICAgZXZlbnQudGFyZ2V0LnN0eWxlLnNldFByb3BlcnR5KFxuICAgICAgICAnd2lkdGgnLFxuICAgICAgICBgY2FsYygke1xuICAgICAgICAgIHRtcC5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS53aWR0aFxuICAgICAgICB9cHggKyB2YXIoLS1qcC1hZGQtdGFnLWV4dHJhLXdpZHRoKSlgXG4gICAgICApO1xuICAgICAgZG9jdW1lbnQuYm9keS5yZW1vdmVDaGlsZCh0bXApO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX29uQWRkVGFnQ2xpY2soXG4gICAgcHJvcHM6IEZpZWxkUHJvcHMsXG4gICAgZXZlbnQ6IFJlYWN0Lk1vdXNlRXZlbnQ8SFRNTEVsZW1lbnQ+XG4gICkge1xuICAgIGNvbnN0IGVsZW0gPSAoZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50KS5jbG9zZXN0KCdkaXYnKTtcbiAgICBjb25zdCBpbnB1dCA9IGVsZW0/LmNoaWxkTm9kZXNbMF0gYXMgSFRNTElucHV0RWxlbWVudDtcbiAgICBpZiAoIXRoaXMuX2VkaXRpbmcpIHtcbiAgICAgIHRoaXMuX2VkaXRpbmcgPSB0cnVlO1xuICAgICAgaW5wdXQudmFsdWUgPSAnJztcbiAgICAgIGlucHV0LmZvY3VzKCk7XG4gICAgfSBlbHNlIGlmIChldmVudC50YXJnZXQgIT09IGlucHV0KSB7XG4gICAgICB0aGlzLmFkZFRhZyhwcm9wcywgaW5wdXQudmFsdWUpO1xuICAgIH1cbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICB9XG5cbiAgcHJpdmF0ZSBfb25UYWdDbGljayhwcm9wczogRmllbGRQcm9wcywgdGFnOiBzdHJpbmcpIHtcbiAgICBjb25zdCBkYXRhID0gcHJvcHMuZm9ybURhdGE7XG4gICAgaWYgKGRhdGEuaW5jbHVkZXModGFnKSkge1xuICAgICAgZGF0YS5zcGxpY2UoZGF0YS5pbmRleE9mKHRhZyksIDEpO1xuICAgIH0gZWxzZSB7XG4gICAgICBkYXRhLnB1c2godGFnKTtcbiAgICB9XG5cbiAgICBwcm9wcy5mb3JtQ29udGV4dC51cGRhdGVNZXRhZGF0YSh7IFtwcm9wcy5uYW1lXTogZGF0YSB9LCB0cnVlKTtcbiAgfVxuXG4gIHJlbmRlcihwcm9wczogRmllbGRQcm9wcyk6IEpTWC5FbGVtZW50IHtcbiAgICBjb25zdCBhbGxUYWdzOiBzdHJpbmdbXSA9IHRoaXMucHVsbFRhZ3MoKTtcblxuICAgIHJldHVybiAoXG4gICAgICA8ZGl2IGNsYXNzTmFtZT17Q0VMTF9UQUdTX1dJREdFVF9DTEFTU30+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtRm9ybUdyb3VwLWZpZWxkTGFiZWwganAtRm9ybUdyb3VwLWNvbnRlbnRJdGVtXCI+XG4gICAgICAgICAgQ2VsbCBUYWdzXG4gICAgICAgIDwvZGl2PlxuICAgICAgICB7YWxsVGFncyAmJlxuICAgICAgICAgIGFsbFRhZ3MubWFwKCh0YWc6IHN0cmluZywgaTogbnVtYmVyKSA9PiAoXG4gICAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICAgIGtleT17aX1cbiAgICAgICAgICAgICAgY2xhc3NOYW1lPXtgJHtDRUxMX1RBR1NfRUxFTUVOVF9DTEFTU30gJHtcbiAgICAgICAgICAgICAgICBwcm9wcy5mb3JtRGF0YS5pbmNsdWRlcyh0YWcpXG4gICAgICAgICAgICAgICAgICA/IENFTExfVEFHU19FTEVNRU5UX0FQUExJRURfQ0xBU1NcbiAgICAgICAgICAgICAgICAgIDogQ0VMTF9UQUdTX0VMRU1FTlRfVU5BUFBMSUVEX0NMQVNTXG4gICAgICAgICAgICAgIH1gfVxuICAgICAgICAgICAgICBvbkNsaWNrPXsoKSA9PiB0aGlzLl9vblRhZ0NsaWNrKHByb3BzLCB0YWcpfVxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT17Q0VMTF9UQUdTX0hPTERFUl9DTEFTU30+XG4gICAgICAgICAgICAgICAgPHNwYW4+e3RhZ308L3NwYW4+XG4gICAgICAgICAgICAgICAge3Byb3BzLmZvcm1EYXRhLmluY2x1ZGVzKHRhZykgJiYgKFxuICAgICAgICAgICAgICAgICAgPExhYkljb24ucmVzb2x2ZVJlYWN0XG4gICAgICAgICAgICAgICAgICAgIGljb249e2NoZWNrSWNvbn1cbiAgICAgICAgICAgICAgICAgICAgdGFnPVwic3BhblwiXG4gICAgICAgICAgICAgICAgICAgIGVsZW1lbnRQb3NpdGlvbj1cImNlbnRlclwiXG4gICAgICAgICAgICAgICAgICAgIGhlaWdodD1cIjE4cHhcIlxuICAgICAgICAgICAgICAgICAgICB3aWR0aD1cIjE4cHhcIlxuICAgICAgICAgICAgICAgICAgICBtYXJnaW5MZWZ0PVwiNXB4XCJcbiAgICAgICAgICAgICAgICAgICAgbWFyZ2luUmlnaHQ9XCItM3B4XCJcbiAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICApKX1cbiAgICAgICAgPGRpdlxuICAgICAgICAgIGNsYXNzTmFtZT17YCR7Q0VMTF9UQUdTX0VMRU1FTlRfQ0xBU1N9ICR7Q0VMTF9UQUdTX0VMRU1FTlRfVU5BUFBMSUVEX0NMQVNTfWB9XG4gICAgICAgID5cbiAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICBjbGFzc05hbWU9e0NFTExfVEFHU19IT0xERVJfQ0xBU1N9XG4gICAgICAgICAgICBvbk1vdXNlRG93bj17KGU6IFJlYWN0Lk1vdXNlRXZlbnQ8SFRNTEVsZW1lbnQ+KSA9PlxuICAgICAgICAgICAgICB0aGlzLl9vbkFkZFRhZ0NsaWNrKHByb3BzLCBlKVxuICAgICAgICAgICAgfVxuICAgICAgICAgID5cbiAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICBjbGFzc05hbWU9e2Ake0NFTExfVEFHU19BRERfQ0xBU1N9ICR7Q0VMTF9UQUdTX0VNUFRZX0NMQVNTfWB9XG4gICAgICAgICAgICAgIHR5cGU9XCJ0ZXh0XCJcbiAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9e3RoaXMuX3RyYW5zLl9fKCdBZGQgVGFnJyl9XG4gICAgICAgICAgICAgIG9uS2V5RG93bj17KGU6IFJlYWN0LktleWJvYXJkRXZlbnQ8SFRNTElucHV0RWxlbWVudD4pID0+XG4gICAgICAgICAgICAgICAgdGhpcy5fb25BZGRUYWdLZXlEb3duKHByb3BzLCBlKVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIG9uRm9jdXM9eyhlOiBSZWFjdC5Gb2N1c0V2ZW50PEhUTUxJbnB1dEVsZW1lbnQ+KSA9PlxuICAgICAgICAgICAgICAgIHRoaXMuX29uQWRkVGFnRm9jdXMoZSlcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICBvbkJsdXI9eyhlOiBSZWFjdC5Gb2N1c0V2ZW50PEhUTUxJbnB1dEVsZW1lbnQ+KSA9PlxuICAgICAgICAgICAgICAgIHRoaXMuX29uQWRkVGFnQmx1cihlLnRhcmdldClcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICBvbkNoYW5nZT17KGU6IFJlYWN0LkNoYW5nZUV2ZW50PEhUTUxJbnB1dEVsZW1lbnQ+KSA9PiB7XG4gICAgICAgICAgICAgICAgdGhpcy5fb25DaGFuZ2UoZSk7XG4gICAgICAgICAgICAgIH19XG4gICAgICAgICAgICAvPlxuICAgICAgICAgICAgPExhYkljb24ucmVzb2x2ZVJlYWN0XG4gICAgICAgICAgICAgIGljb249e2FkZEljb259XG4gICAgICAgICAgICAgIHRhZz1cInNwYW5cIlxuICAgICAgICAgICAgICBoZWlnaHQ9XCIxOHB4XCJcbiAgICAgICAgICAgICAgd2lkdGg9XCIxOHB4XCJcbiAgICAgICAgICAgICAgbWFyZ2luTGVmdD1cIjVweFwiXG4gICAgICAgICAgICAgIG1hcmdpblJpZ2h0PVwiLTNweFwiXG4gICAgICAgICAgICAvPlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgICk7XG4gIH1cblxuICBwcml2YXRlIF90cmFja2VyOiBJTm90ZWJvb2tUcmFja2VyO1xuICBwcml2YXRlIF90cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9lZGl0aW5nOiBib29sZWFuO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY2VsbHRhZ3MtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHR5cGUgeyBGaWVsZFByb3BzIH0gZnJvbSAnQHJqc2YvdXRpbHMnO1xuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuXG5pbXBvcnQgeyBJTm90ZWJvb2tUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbm90ZWJvb2snO1xuXG5pbXBvcnQgeyBDZWxsVGFnRmllbGQgfSBmcm9tICcuL2NlbGx0YWcnO1xuaW1wb3J0IHtcbiAgSUZvcm1SZW5kZXJlcixcbiAgSUZvcm1SZW5kZXJlclJlZ2lzdHJ5XG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG4vKipcbiAqIFJlZ2lzdGVyaW5nIGNlbGwgdGFnIGZpZWxkLlxuICovXG5jb25zdCBjdXN0b21DZWxsVGFnOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY2VsbHRhZ3MtZXh0ZW5zaW9uOnBsdWdpbicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0aGUgY2VsbCB0YWdzIGVkaXRvci4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSU5vdGVib29rVHJhY2tlcl0sXG4gIG9wdGlvbmFsOiBbSUZvcm1SZW5kZXJlclJlZ2lzdHJ5XSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFja2VyOiBJTm90ZWJvb2tUcmFja2VyLFxuICAgIGZvcm1SZWdpc3RyeT86IElGb3JtUmVuZGVyZXJSZWdpc3RyeVxuICApID0+IHtcbiAgICAvLyBSZWdpc3RlciB0aGUgY3VzdG9tIGZpZWxkXG4gICAgaWYgKGZvcm1SZWdpc3RyeSkge1xuICAgICAgY29uc3QgY29tcG9uZW50OiBJRm9ybVJlbmRlcmVyID0ge1xuICAgICAgICBmaWVsZFJlbmRlcmVyOiAocHJvcHM6IEZpZWxkUHJvcHMpID0+IHtcbiAgICAgICAgICByZXR1cm4gbmV3IENlbGxUYWdGaWVsZCh0cmFja2VyKS5yZW5kZXIocHJvcHMpO1xuICAgICAgICB9XG4gICAgICB9O1xuICAgICAgZm9ybVJlZ2lzdHJ5LmFkZFJlbmRlcmVyKFxuICAgICAgICAnQGp1cHl0ZXJsYWIvY2VsbHRhZ3MtZXh0ZW5zaW9uOnBsdWdpbi5yZW5kZXJlcicsXG4gICAgICAgIGNvbXBvbmVudFxuICAgICAgKTtcbiAgICB9XG4gIH1cbn07XG5cbmV4cG9ydCBkZWZhdWx0IFtjdXN0b21DZWxsVGFnXTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==