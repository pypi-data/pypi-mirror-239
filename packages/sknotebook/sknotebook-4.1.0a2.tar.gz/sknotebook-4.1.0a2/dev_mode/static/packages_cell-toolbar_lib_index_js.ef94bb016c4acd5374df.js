"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_cell-toolbar_lib_index_js"],{

/***/ "../packages/cell-toolbar/lib/celltoolbartracker.js":
/*!**********************************************************!*\
  !*** ../packages/cell-toolbar/lib/celltoolbartracker.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellBarExtension": () => (/* binding */ CellBarExtension),
/* harmony export */   "CellToolbarTracker": () => (/* binding */ CellToolbarTracker)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/





/*
 * Text mime types
 */
const TEXT_MIME_TYPES = [
    'text/plain',
    'application/vnd.jupyter.stdout',
    'application/vnd.jupyter.stderr'
];
/**
 * Widget cell toolbar classes
 */
const CELL_TOOLBAR_CLASS = 'jp-cell-toolbar';
const CELL_MENU_CLASS = 'jp-cell-menu';
/**
 * Class for a cell whose contents overlap with the cell toolbar
 */
const TOOLBAR_OVERLAP_CLASS = 'jp-toolbar-overlap';
/**
 * Watch a notebook so that a cell toolbar appears on the active cell
 */
class CellToolbarTracker {
    constructor(panel, toolbar) {
        var _a;
        this._isDisposed = false;
        this._panel = panel;
        this._previousActiveCell = this._panel.content.activeCell;
        this._toolbar = toolbar;
        this._onToolbarChanged();
        this._toolbar.changed.connect(this._onToolbarChanged, this);
        // Only add the toolbar to the notebook's active cell (if any) once it has fully rendered and been revealed.
        void panel.revealed.then(() => {
            // Wait one frame (at 60 fps) for the panel to render the first cell, then display the cell toolbar on it if possible.
            setTimeout(() => {
                this._onActiveCellChanged(panel.content);
            }, 1000 / 60);
        });
        // Check whether the toolbar should be rendered upon a layout change
        panel.content.renderingLayoutChanged.connect(this._onActiveCellChanged, this);
        // Handle subsequent changes of active cell.
        panel.content.activeCellChanged.connect(this._onActiveCellChanged, this);
        (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.metadataChanged.connect(this._onMetadataChanged, this);
        panel.disposed.connect(() => {
            var _a;
            panel.content.activeCellChanged.disconnect(this._onActiveCellChanged);
            (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.metadataChanged.disconnect(this._onMetadataChanged);
        });
    }
    _onMetadataChanged(model, args) {
        if (args.key === 'jupyter') {
            if (typeof args.newValue === 'object' &&
                args.newValue.source_hidden === true &&
                (args.type === 'add' || args.type === 'change')) {
                // Cell just became hidden; remove toolbar
                this._removeToolbar(model);
            }
            // Check whether input visibility changed
            else if (typeof args.oldValue === 'object' &&
                args.oldValue.source_hidden === true) {
                // Cell just became visible; add toolbar
                this._addToolbar(model);
            }
        }
    }
    _onActiveCellChanged(notebook) {
        if (this._previousActiveCell && !this._previousActiveCell.isDisposed) {
            // Disposed cells do not have a model anymore.
            this._removeToolbar(this._previousActiveCell.model);
            this._previousActiveCell.model.metadataChanged.disconnect(this._onMetadataChanged);
        }
        const activeCell = notebook.activeCell;
        if (activeCell === null || activeCell.inputHidden) {
            return;
        }
        activeCell.model.metadataChanged.connect(this._onMetadataChanged, this);
        this._addToolbar(activeCell.model);
        this._previousActiveCell = activeCell;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        var _a;
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._toolbar.changed.disconnect(this._onToolbarChanged, this);
        const cells = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.context.model.cells;
        if (cells) {
            for (const model of cells) {
                this._removeToolbar(model);
            }
        }
        this._panel = null;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.clearData(this);
    }
    _addToolbar(model) {
        const cell = this._getCell(model);
        if (cell) {
            const toolbarWidget = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.Toolbar();
            toolbarWidget.addClass(CELL_MENU_CLASS);
            const promises = [];
            for (const { name, widget } of this._toolbar) {
                toolbarWidget.addItem(name, widget);
                if (widget instanceof _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ReactWidget &&
                    widget.renderPromise !== undefined) {
                    widget.update();
                    promises.push(widget.renderPromise);
                }
            }
            // Wait for all the buttons to be rendered before attaching the toolbar.
            Promise.all(promises)
                .then(() => {
                toolbarWidget.addClass(CELL_TOOLBAR_CLASS);
                cell.layout.insertWidget(0, toolbarWidget);
                // For rendered markdown, watch for resize events.
                cell.displayChanged.connect(this._resizeEventCallback, this);
                // Watch for changes in the cell's contents.
                cell.model.contentChanged.connect(this._changedEventCallback, this);
                // Hide the cell toolbar if it overlaps with cell contents
                this._updateCellForToolbarOverlap(cell);
            })
                .catch(e => {
                console.error('Error rendering buttons of the cell toolbar: ', e);
            });
        }
    }
    _getCell(model) {
        var _a;
        return (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.widgets.find(widget => widget.model === model);
    }
    _findToolbarWidgets(cell) {
        const widgets = cell.layout.widgets;
        // Search for header using the CSS class or use the first one if not found.
        return widgets.filter(widget => widget.hasClass(CELL_TOOLBAR_CLASS)) || [];
    }
    _removeToolbar(model) {
        const cell = this._getCell(model);
        if (cell) {
            this._findToolbarWidgets(cell).forEach(widget => {
                widget.dispose();
            });
            // Attempt to remove the resize and changed event handlers.
            cell.displayChanged.disconnect(this._resizeEventCallback, this);
        }
        model.contentChanged.disconnect(this._changedEventCallback, this);
    }
    /**
     * Call back on settings changes
     */
    _onToolbarChanged() {
        var _a;
        // Reset toolbar when settings changes
        const activeCell = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.activeCell;
        if (activeCell) {
            this._removeToolbar(activeCell.model);
            this._addToolbar(activeCell.model);
        }
    }
    _changedEventCallback() {
        var _a;
        const activeCell = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.activeCell;
        if (activeCell === null || activeCell === undefined) {
            return;
        }
        this._updateCellForToolbarOverlap(activeCell);
    }
    _resizeEventCallback() {
        var _a;
        const activeCell = (_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.activeCell;
        if (activeCell === null || activeCell === undefined) {
            return;
        }
        this._updateCellForToolbarOverlap(activeCell);
    }
    _updateCellForToolbarOverlap(activeCell) {
        // When we do change in cell, If we don't wait the browser might not have
        // completed the layout update, resulting in the previous width being returned
        // using `getBoundingClientRect().width` in later functions.
        requestAnimationFrame(() => {
            // Remove the "toolbar overlap" class from the cell, rendering the cell's toolbar
            const activeCellElement = activeCell.node;
            activeCellElement.classList.remove(TOOLBAR_OVERLAP_CLASS);
            if (this._cellToolbarOverlapsContents(activeCell)) {
                // Add the "toolbar overlap" class to the cell, completely concealing the toolbar,
                // if the first line of the content overlaps with it at all
                activeCellElement.classList.add(TOOLBAR_OVERLAP_CLASS);
            }
        });
    }
    _cellToolbarOverlapsContents(activeCell) {
        var _a;
        const cellType = activeCell.model.type;
        // If the toolbar is too large for the current cell, hide it.
        const cellLeft = this._cellEditorWidgetLeft(activeCell);
        const cellRight = this._cellEditorWidgetRight(activeCell);
        const toolbarLeft = this._cellToolbarLeft(activeCell);
        if (toolbarLeft === null) {
            return false;
        }
        // The toolbar should not take up more than 50% of the cell.
        if ((cellLeft + cellRight) / 2 > toolbarLeft) {
            return true;
        }
        if (cellType === 'markdown' && activeCell.rendered) {
            // Check for overlap in rendered markdown content
            return this._markdownOverlapsToolbar(activeCell);
        }
        // Check for overlap in code content
        if (((_a = this._panel) === null || _a === void 0 ? void 0 : _a.content.renderingLayout) === 'default') {
            return this._codeOverlapsToolbar(activeCell);
        }
        else {
            return this._outputOverlapsToolbar(activeCell);
        }
    }
    /**
     * Check for overlap between rendered Markdown and the cell toolbar
     *
     * @param activeCell A rendered MarkdownCell
     * @returns `true` if the first line of the output overlaps with the cell toolbar, `false` otherwise
     */
    _markdownOverlapsToolbar(activeCell) {
        const markdownOutput = activeCell.inputArea; // Rendered markdown appears in the input area
        if (!markdownOutput) {
            return false;
        }
        // Get the rendered markdown as a widget.
        const markdownOutputWidget = markdownOutput.renderedInput;
        const markdownOutputElement = markdownOutputWidget.node;
        const firstOutputElementChild = markdownOutputElement.firstElementChild;
        if (firstOutputElementChild === null) {
            return false;
        }
        // Temporarily set the element's max width so that the bounding client rectangle only encompasses the content.
        const oldMaxWidth = firstOutputElementChild.style.maxWidth;
        firstOutputElementChild.style.maxWidth = 'max-content';
        const lineRight = firstOutputElementChild.getBoundingClientRect().right;
        // Reinstate the old max width.
        firstOutputElementChild.style.maxWidth = oldMaxWidth;
        const toolbarLeft = this._cellToolbarLeft(activeCell);
        return toolbarLeft === null ? false : lineRight > toolbarLeft;
    }
    _outputOverlapsToolbar(activeCell) {
        const outputArea = activeCell.outputArea.node;
        if (outputArea) {
            const outputs = outputArea.querySelectorAll('[data-mime-type]');
            const toolbarRect = this._cellToolbarRect(activeCell);
            if (toolbarRect) {
                const { left: toolbarLeft, bottom: toolbarBottom } = toolbarRect;
                return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.some)(outputs, output => {
                    const node = output.firstElementChild;
                    if (node) {
                        const range = new Range();
                        if (TEXT_MIME_TYPES.includes(output.getAttribute('data-mime-type') || '')) {
                            // If the node is plain text, it's in a <pre>. To get the true bounding box of the
                            // text, the node contents need to be selected.
                            range.selectNodeContents(node);
                        }
                        else {
                            range.selectNode(node);
                        }
                        const { right: nodeRight, top: nodeTop } = range.getBoundingClientRect();
                        // Note: y-coordinate increases toward the bottom of page
                        return nodeRight > toolbarLeft && nodeTop < toolbarBottom;
                    }
                    return false;
                });
            }
        }
        return false;
    }
    _codeOverlapsToolbar(activeCell) {
        const editorWidget = activeCell.editorWidget;
        const editor = activeCell.editor;
        if (!editorWidget || !editor) {
            return false;
        }
        if (editor.lineCount < 1) {
            return false; // Nothing in the editor
        }
        const codeMirrorLines = editorWidget.node.getElementsByClassName('cm-line');
        if (codeMirrorLines.length < 1) {
            return false; // No lines present
        }
        let lineRight = codeMirrorLines[0].getBoundingClientRect().left;
        const range = document.createRange();
        range.selectNodeContents(codeMirrorLines[0]);
        lineRight += range.getBoundingClientRect().width;
        const toolbarLeft = this._cellToolbarLeft(activeCell);
        return toolbarLeft === null ? false : lineRight > toolbarLeft;
    }
    _cellEditorWidgetLeft(activeCell) {
        var _a, _b;
        return (_b = (_a = activeCell.editorWidget) === null || _a === void 0 ? void 0 : _a.node.getBoundingClientRect().left) !== null && _b !== void 0 ? _b : 0;
    }
    _cellEditorWidgetRight(activeCell) {
        var _a, _b;
        return (_b = (_a = activeCell.editorWidget) === null || _a === void 0 ? void 0 : _a.node.getBoundingClientRect().right) !== null && _b !== void 0 ? _b : 0;
    }
    _cellToolbarRect(activeCell) {
        const toolbarWidgets = this._findToolbarWidgets(activeCell);
        if (toolbarWidgets.length < 1) {
            return null;
        }
        const activeCellToolbar = toolbarWidgets[0].node;
        return activeCellToolbar.getBoundingClientRect();
    }
    _cellToolbarLeft(activeCell) {
        var _a;
        return ((_a = this._cellToolbarRect(activeCell)) === null || _a === void 0 ? void 0 : _a.left) || null;
    }
}
const defaultToolbarItems = [
    {
        command: 'notebook:duplicate-below',
        name: 'duplicate-cell'
    },
    {
        command: 'notebook:move-cell-up',
        name: 'move-cell-up'
    },
    {
        command: 'notebook:move-cell-down',
        name: 'move-cell-down'
    },
    {
        command: 'notebook:insert-cell-above',
        name: 'insert-cell-above'
    },
    {
        command: 'notebook:insert-cell-below',
        name: 'insert-cell-below'
    },
    {
        command: 'notebook:delete-cell',
        name: 'delete-cell'
    }
];
/**
 * Widget extension that creates a CellToolbarTracker each time a notebook is
 * created.
 */
class CellBarExtension {
    constructor(commands, toolbarFactory) {
        this._commands = commands;
        this._toolbarFactory = toolbarFactory !== null && toolbarFactory !== void 0 ? toolbarFactory : this.defaultToolbarFactory;
    }
    get defaultToolbarFactory() {
        const itemFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.createDefaultFactory)(this._commands);
        return (widget) => new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__.ObservableList({
            values: defaultToolbarItems.map(item => {
                return {
                    name: item.name,
                    widget: itemFactory(CellBarExtension.FACTORY_NAME, widget, item)
                };
            })
        });
    }
    createNew(panel) {
        return new CellToolbarTracker(panel, this._toolbarFactory(panel));
    }
}
CellBarExtension.FACTORY_NAME = 'Cell';



/***/ }),

/***/ "../packages/cell-toolbar/lib/index.js":
/*!*********************************************!*\
  !*** ../packages/cell-toolbar/lib/index.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CellBarExtension": () => (/* reexport safe */ _celltoolbartracker__WEBPACK_IMPORTED_MODULE_0__.CellBarExtension),
/* harmony export */   "CellToolbarTracker": () => (/* reexport safe */ _celltoolbartracker__WEBPACK_IMPORTED_MODULE_0__.CellToolbarTracker)
/* harmony export */ });
/* harmony import */ var _celltoolbartracker__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./celltoolbartracker */ "../packages/cell-toolbar/lib/celltoolbartracker.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module cell-toolbar
 */



/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY2VsbC10b29sYmFyX2xpYl9pbmRleF9qcy5lZjk0YmIwMTZjNGFjZDUzNzRkZi5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUNGO0FBVUg7QUFDVDtBQUN4QjtBQUdFO0FBSTNDOztHQUVHO0FBQ0gsTUFBTSxlQUFlLEdBQUc7SUFDdEIsWUFBWTtJQUNaLGdDQUFnQztJQUNoQyxnQ0FBZ0M7Q0FDakMsQ0FBQztBQUVGOztHQUVHO0FBQ0gsTUFBTSxrQkFBa0IsR0FBRyxpQkFBaUIsQ0FBQztBQUM3QyxNQUFNLGVBQWUsR0FBRyxjQUFjLENBQUM7QUFFdkM7O0dBRUc7QUFDSCxNQUFNLHFCQUFxQixHQUFHLG9CQUFvQixDQUFDO0FBRW5EOztHQUVHO0FBQ0ksTUFBTSxrQkFBa0I7SUFDN0IsWUFDRSxLQUFvQixFQUNwQixPQUFzRDs7UUF3V2hELGdCQUFXLEdBQUcsS0FBSyxDQUFDO1FBdFcxQixJQUFJLENBQUMsTUFBTSxHQUFHLEtBQUssQ0FBQztRQUNwQixJQUFJLENBQUMsbUJBQW1CLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsVUFBVSxDQUFDO1FBQzFELElBQUksQ0FBQyxRQUFRLEdBQUcsT0FBTyxDQUFDO1FBRXhCLElBQUksQ0FBQyxpQkFBaUIsRUFBRSxDQUFDO1FBQ3pCLElBQUksQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsaUJBQWlCLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFFNUQsNEdBQTRHO1FBQzVHLEtBQUssS0FBSyxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsR0FBRyxFQUFFO1lBQzVCLHNIQUFzSDtZQUN0SCxVQUFVLENBQUMsR0FBRyxFQUFFO2dCQUNkLElBQUksQ0FBQyxvQkFBb0IsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUM7WUFDM0MsQ0FBQyxFQUFFLElBQUksR0FBRyxFQUFFLENBQUMsQ0FBQztR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Rjs7O0dBR0c7QUFDSCxNQUFhLGdCQUFnQjtJQUczQixZQUNFLFFBQXlCLEVBQ3pCLGNBRWtEO1FBRWxELElBQUksQ0FBQyxTQUFTLEdBQUcsUUFBUSxDQUFDO1FBQzFCLElBQUksQ0FBQyxlQUFlLEdBQUcsY0FBYyxhQUFkLGNBQWMsY0FBZCxjQUFjLEdBQUksSUFBSSxDQUFDLHFCQUFxQixDQUFDO0lBQ3RFLENBQUM7SUFFRCxJQUFjLHFCQUFxQjtRQUdqQyxNQUFNLFdBQVcsR0FBRywwRUFBb0IsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLENBQUM7UUFDekQsT0FBTyxDQUFDLE1BQWMsRUFBRSxFQUFFLENBQ3hCLElBQUksbUVBQWMsQ0FBQztZQUNqQixNQUFNLEVBQUUsbUJBQW1CLENBQUMsR0FBRyxDQUFDLElBQUksQ0FBQyxFQUFFO2dCQUNyQyxPQUFPO29CQUNMLElBQUksRUFBRSxJQUFJLENBQUMsSUFBSTtvQkFDZixNQUFNLEVBQUUsV0FBVyxDQUFDLGdCQUFnQixDQUFDLFlBQVksRUFBRSxNQUFNLEVBQUUsSUFBSSxDQUFDO2lCQUNqRSxDQUFDO1lBQ0osQ0FBQyxDQUFDO1NBQ0gsQ0FBQyxDQUFDO0lBQ1AsQ0FBQztJQUVELFNBQVMsQ0FBQyxLQUFvQjtRQUM1QixPQUFPLElBQUksa0JBQWtCLENBQUMsS0FBSyxFQUFFLElBQUksQ0FBQyxlQUFlLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQztJQUNwRSxDQUFDOztBQTdCTSw2QkFBWSxHQUFHLE1BQU0sQ0FBQztBQURGOzs7Ozs7Ozs7Ozs7Ozs7OztBQzliN0I7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBQ2tDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NlbGwtdG9vbGJhci9zcmMvY2VsbHRvb2xiYXJ0cmFja2VyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jZWxsLXRvb2xiYXIvc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuaW1wb3J0IHsgY3JlYXRlRGVmYXVsdEZhY3RvcnksIFRvb2xiYXJSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7XG4gIENlbGwsXG4gIENlbGxNb2RlbCxcbiAgQ29kZUNlbGwsXG4gIElDZWxsTW9kZWwsXG4gIE1hcmtkb3duQ2VsbFxufSBmcm9tICdAanVweXRlcmxhYi9jZWxscyc7XG5pbXBvcnQgeyBEb2N1bWVudFJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgTm90ZWJvb2ssIE5vdGVib29rUGFuZWwgfSBmcm9tICdAanVweXRlcmxhYi9ub3RlYm9vayc7XG5pbXBvcnQgeyBJT2JzZXJ2YWJsZUxpc3QsIE9ic2VydmFibGVMaXN0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvb2JzZXJ2YWJsZXMnO1xuaW1wb3J0IHsgUmVhY3RXaWRnZXQsIFRvb2xiYXIgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IHNvbWUgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBDb21tYW5kUmVnaXN0cnkgfSBmcm9tICdAbHVtaW5vL2NvbW1hbmRzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFBhbmVsTGF5b3V0LCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgSU1hcENoYW5nZSB9IGZyb20gJ0BqdXB5dGVyL3lkb2MnO1xuXG4vKlxuICogVGV4dCBtaW1lIHR5cGVzXG4gKi9cbmNvbnN0IFRFWFRfTUlNRV9UWVBFUyA9IFtcbiAgJ3RleHQvcGxhaW4nLFxuICAnYXBwbGljYXRpb24vdm5kLmp1cHl0ZXIuc3Rkb3V0JyxcbiAgJ2FwcGxpY2F0aW9uL3ZuZC5qdXB5dGVyLnN0ZGVycidcbl07XG5cbi8qKlxuICogV2lkZ2V0IGNlbGwgdG9vbGJhciBjbGFzc2VzXG4gKi9cbmNvbnN0IENFTExfVE9PTEJBUl9DTEFTUyA9ICdqcC1jZWxsLXRvb2xiYXInO1xuY29uc3QgQ0VMTF9NRU5VX0NMQVNTID0gJ2pwLWNlbGwtbWVudSc7XG5cbi8qKlxuICogQ2xhc3MgZm9yIGEgY2VsbCB3aG9zZSBjb250ZW50cyBvdmVybGFwIHdpdGggdGhlIGNlbGwgdG9vbGJhclxuICovXG5jb25zdCBUT09MQkFSX09WRVJMQVBfQ0xBU1MgPSAnanAtdG9vbGJhci1vdmVybGFwJztcblxuLyoqXG4gKiBXYXRjaCBhIG5vdGVib29rIHNvIHRoYXQgYSBjZWxsIHRvb2xiYXIgYXBwZWFycyBvbiB0aGUgYWN0aXZlIGNlbGxcbiAqL1xuZXhwb3J0IGNsYXNzIENlbGxUb29sYmFyVHJhY2tlciBpbXBsZW1lbnRzIElEaXNwb3NhYmxlIHtcbiAgY29uc3RydWN0b3IoXG4gICAgcGFuZWw6IE5vdGVib29rUGFuZWwsXG4gICAgdG9vbGJhcjogSU9ic2VydmFibGVMaXN0PFRvb2xiYXJSZWdpc3RyeS5JVG9vbGJhckl0ZW0+XG4gICkge1xuICAgIHRoaXMuX3BhbmVsID0gcGFuZWw7XG4gICAgdGhpcy5fcHJldmlvdXNBY3RpdmVDZWxsID0gdGhpcy5fcGFuZWwuY29udGVudC5hY3RpdmVDZWxsO1xuICAgIHRoaXMuX3Rvb2xiYXIgPSB0b29sYmFyO1xuXG4gICAgdGhpcy5fb25Ub29sYmFyQ2hhbmdlZCgpO1xuICAgIHRoaXMuX3Rvb2xiYXIuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uVG9vbGJhckNoYW5nZWQsIHRoaXMpO1xuXG4gICAgLy8gT25seSBhZGQgdGhlIHRvb2xiYXIgdG8gdGhlIG5vdGVib29rJ3MgYWN0aXZlIGNlbGwgKGlmIGFueSkgb25jZSBpdCBoYXMgZnVsbHkgcmVuZGVyZWQgYW5kIGJlZW4gcmV2ZWFsZWQuXG4gICAgdm9pZCBwYW5lbC5yZXZlYWxlZC50aGVuKCgpID0+IHtcbiAgICAgIC8vIFdhaXQgb25lIGZyYW1lIChhdCA2MCBmcHMpIGZvciB0aGUgcGFuZWwgdG8gcmVuZGVyIHRoZSBmaXJzdCBjZWxsLCB0aGVuIGRpc3BsYXkgdGhlIGNlbGwgdG9vbGJhciBvbiBpdCBpZiBwb3NzaWJsZS5cbiAgICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgICB0aGlzLl9vbkFjdGl2ZUNlbGxDaGFuZ2VkKHBhbmVsLmNvbnRlbnQpO1xuICAgICAgfSwgMTAwMCAvIDYwKTtcbiAgICB9KTtcblxuICAgIC8vIENoZWNrIHdoZXRoZXIgdGhlIHRvb2xiYXIgc2hvdWxkIGJlIHJlbmRlcmVkIHVwb24gYSBsYXlvdXQgY2hhbmdlXG4gICAgcGFuZWwuY29udGVudC5yZW5kZXJpbmdMYXlvdXRDaGFuZ2VkLmNvbm5lY3QoXG4gICAgICB0aGlzLl9vbkFjdGl2ZUNlbGxDaGFuZ2VkLFxuICAgICAgdGhpc1xuICAgICk7XG5cbiAgICAvLyBIYW5kbGUgc3Vic2VxdWVudCBjaGFuZ2VzIG9mIGFjdGl2ZSBjZWxsLlxuICAgIHBhbmVsLmNvbnRlbnQuYWN0aXZlQ2VsbENoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkFjdGl2ZUNlbGxDaGFuZ2VkLCB0aGlzKTtcbiAgICBwYW5lbC5jb250ZW50LmFjdGl2ZUNlbGw/Lm1vZGVsLm1ldGFkYXRhQ2hhbmdlZC5jb25uZWN0KFxuICAgICAgdGhpcy5fb25NZXRhZGF0YUNoYW5nZWQsXG4gICAgICB0aGlzXG4gICAgKTtcbiAgICBwYW5lbC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHBhbmVsLmNvbnRlbnQuYWN0aXZlQ2VsbENoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9vbkFjdGl2ZUNlbGxDaGFuZ2VkKTtcbiAgICAgIHBhbmVsLmNvbnRlbnQuYWN0aXZlQ2VsbD8ubW9kZWwubWV0YWRhdGFDaGFuZ2VkLmRpc2Nvbm5lY3QoXG4gICAgICAgIHRoaXMuX29uTWV0YWRhdGFDaGFuZ2VkXG4gICAgICApO1xuICAgIH0pO1xuICB9XG5cbiAgX29uTWV0YWRhdGFDaGFuZ2VkKG1vZGVsOiBDZWxsTW9kZWwsIGFyZ3M6IElNYXBDaGFuZ2UpIHtcbiAgICBpZiAoYXJncy5rZXkgPT09ICdqdXB5dGVyJykge1xuICAgICAgaWYgKFxuICAgICAgICB0eXBlb2YgYXJncy5uZXdWYWx1ZSA9PT0gJ29iamVjdCcgJiZcbiAgICAgICAgYXJncy5uZXdWYWx1ZS5zb3VyY2VfaGlkZGVuID09PSB0cnVlICYmXG4gICAgICAgIChhcmdzLnR5cGUgPT09ICdhZGQnIHx8IGFyZ3MudHlwZSA9PT0gJ2NoYW5nZScpXG4gICAgICApIHtcbiAgICAgICAgLy8gQ2VsbCBqdXN0IGJlY2FtZSBoaWRkZW47IHJlbW92ZSB0b29sYmFyXG4gICAgICAgIHRoaXMuX3JlbW92ZVRvb2xiYXIobW9kZWwpO1xuICAgICAgfVxuICAgICAgLy8gQ2hlY2sgd2hldGhlciBpbnB1dCB2aXNpYmlsaXR5IGNoYW5nZWRcbiAgICAgIGVsc2UgaWYgKFxuICAgICAgICB0eXBlb2YgYXJncy5vbGRWYWx1ZSA9PT0gJ29iamVjdCcgJiZcbiAgICAgICAgYXJncy5vbGRWYWx1ZS5zb3VyY2VfaGlkZGVuID09PSB0cnVlXG4gICAgICApIHtcbiAgICAgICAgLy8gQ2VsbCBqdXN0IGJlY2FtZSB2aXNpYmxlOyBhZGQgdG9vbGJhclxuICAgICAgICB0aGlzLl9hZGRUb29sYmFyKG1vZGVsKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgX29uQWN0aXZlQ2VsbENoYW5nZWQobm90ZWJvb2s6IE5vdGVib29rKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX3ByZXZpb3VzQWN0aXZlQ2VsbCAmJiAhdGhpcy5fcHJldmlvdXNBY3RpdmVDZWxsLmlzRGlzcG9zZWQpIHtcbiAgICAgIC8vIERpc3Bvc2VkIGNlbGxzIGRvIG5vdCBoYXZlIGEgbW9kZWwgYW55bW9yZS5cbiAgICAgIHRoaXMuX3JlbW92ZVRvb2xiYXIodGhpcy5fcHJldmlvdXNBY3RpdmVDZWxsLm1vZGVsKTtcbiAgICAgIHRoaXMuX3ByZXZpb3VzQWN0aXZlQ2VsbC5tb2RlbC5tZXRhZGF0YUNoYW5nZWQuZGlzY29ubmVjdChcbiAgICAgICAgdGhpcy5fb25NZXRhZGF0YUNoYW5nZWRcbiAgICAgICk7XG4gICAgfVxuXG4gICAgY29uc3QgYWN0aXZlQ2VsbCA9IG5vdGVib29rLmFjdGl2ZUNlbGw7XG4gICAgaWYgKGFjdGl2ZUNlbGwgPT09IG51bGwgfHwgYWN0aXZlQ2VsbC5pbnB1dEhpZGRlbikge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGFjdGl2ZUNlbGwubW9kZWwubWV0YWRhdGFDaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25NZXRhZGF0YUNoYW5nZWQsIHRoaXMpO1xuXG4gICAgdGhpcy5fYWRkVG9vbGJhcihhY3RpdmVDZWxsLm1vZGVsKTtcbiAgICB0aGlzLl9wcmV2aW91c0FjdGl2ZUNlbGwgPSBhY3RpdmVDZWxsO1xuICB9XG5cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG5cbiAgICB0aGlzLl90b29sYmFyLmNoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9vblRvb2xiYXJDaGFuZ2VkLCB0aGlzKTtcblxuICAgIGNvbnN0IGNlbGxzID0gdGhpcy5fcGFuZWw/LmNvbnRleHQubW9kZWwuY2VsbHM7XG4gICAgaWYgKGNlbGxzKSB7XG4gICAgICBmb3IgKGNvbnN0IG1vZGVsIG9mIGNlbGxzKSB7XG4gICAgICAgIHRoaXMuX3JlbW92ZVRvb2xiYXIobW9kZWwpO1xuICAgICAgfVxuICAgIH1cblxuICAgIHRoaXMuX3BhbmVsID0gbnVsbDtcblxuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICBwcml2YXRlIF9hZGRUb29sYmFyKG1vZGVsOiBJQ2VsbE1vZGVsKTogdm9pZCB7XG4gICAgY29uc3QgY2VsbCA9IHRoaXMuX2dldENlbGwobW9kZWwpO1xuXG4gICAgaWYgKGNlbGwpIHtcbiAgICAgIGNvbnN0IHRvb2xiYXJXaWRnZXQgPSBuZXcgVG9vbGJhcigpO1xuICAgICAgdG9vbGJhcldpZGdldC5hZGRDbGFzcyhDRUxMX01FTlVfQ0xBU1MpO1xuXG4gICAgICBjb25zdCBwcm9taXNlczogUHJvbWlzZTx2b2lkPltdID0gW107XG4gICAgICBmb3IgKGNvbnN0IHsgbmFtZSwgd2lkZ2V0IH0gb2YgdGhpcy5fdG9vbGJhcikge1xuICAgICAgICB0b29sYmFyV2lkZ2V0LmFkZEl0ZW0obmFtZSwgd2lkZ2V0KTtcbiAgICAgICAgaWYgKFxuICAgICAgICAgIHdpZGdldCBpbnN0YW5jZW9mIFJlYWN0V2lkZ2V0ICYmXG4gICAgICAgICAgKHdpZGdldCBhcyBSZWFjdFdpZGdldCkucmVuZGVyUHJvbWlzZSAhPT0gdW5kZWZpbmVkXG4gICAgICAgICkge1xuICAgICAgICAgICh3aWRnZXQgYXMgUmVhY3RXaWRnZXQpLnVwZGF0ZSgpO1xuICAgICAgICAgIHByb21pc2VzLnB1c2goKHdpZGdldCBhcyBSZWFjdFdpZGdldCkucmVuZGVyUHJvbWlzZSEpO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIC8vIFdhaXQgZm9yIGFsbCB0aGUgYnV0dG9ucyB0byBiZSByZW5kZXJlZCBiZWZvcmUgYXR0YWNoaW5nIHRoZSB0b29sYmFyLlxuICAgICAgUHJvbWlzZS5hbGwocHJvbWlzZXMpXG4gICAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgICB0b29sYmFyV2lkZ2V0LmFkZENsYXNzKENFTExfVE9PTEJBUl9DTEFTUyk7XG4gICAgICAgICAgKGNlbGwubGF5b3V0IGFzIFBhbmVsTGF5b3V0KS5pbnNlcnRXaWRnZXQoMCwgdG9vbGJhcldpZGdldCk7XG5cbiAgICAgICAgICAvLyBGb3IgcmVuZGVyZWQgbWFya2Rvd24sIHdhdGNoIGZvciByZXNpemUgZXZlbnRzLlxuICAgICAgICAgIGNlbGwuZGlzcGxheUNoYW5nZWQuY29ubmVjdCh0aGlzLl9yZXNpemVFdmVudENhbGxiYWNrLCB0aGlzKTtcblxuICAgICAgICAgIC8vIFdhdGNoIGZvciBjaGFuZ2VzIGluIHRoZSBjZWxsJ3MgY29udGVudHMuXG4gICAgICAgICAgY2VsbC5tb2RlbC5jb250ZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMuX2NoYW5nZWRFdmVudENhbGxiYWNrLCB0aGlzKTtcblxuICAgICAgICAgIC8vIEhpZGUgdGhlIGNlbGwgdG9vbGJhciBpZiBpdCBvdmVybGFwcyB3aXRoIGNlbGwgY29udGVudHNcbiAgICAgICAgICB0aGlzLl91cGRhdGVDZWxsRm9yVG9vbGJhck92ZXJsYXAoY2VsbCk7XG4gICAgICAgIH0pXG4gICAgICAgIC5jYXRjaChlID0+IHtcbiAgICAgICAgICBjb25zb2xlLmVycm9yKCdFcnJvciByZW5kZXJpbmcgYnV0dG9ucyBvZiB0aGUgY2VsbCB0b29sYmFyOiAnLCBlKTtcbiAgICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfZ2V0Q2VsbChtb2RlbDogSUNlbGxNb2RlbCk6IENlbGwgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB0aGlzLl9wYW5lbD8uY29udGVudC53aWRnZXRzLmZpbmQod2lkZ2V0ID0+IHdpZGdldC5tb2RlbCA9PT0gbW9kZWwpO1xuICB9XG5cbiAgcHJpdmF0ZSBfZmluZFRvb2xiYXJXaWRnZXRzKGNlbGw6IENlbGwpOiBXaWRnZXRbXSB7XG4gICAgY29uc3Qgd2lkZ2V0cyA9IChjZWxsLmxheW91dCBhcyBQYW5lbExheW91dCkud2lkZ2V0cztcblxuICAgIC8vIFNlYXJjaCBmb3IgaGVhZGVyIHVzaW5nIHRoZSBDU1MgY2xhc3Mgb3IgdXNlIHRoZSBmaXJzdCBvbmUgaWYgbm90IGZvdW5kLlxuICAgIHJldHVybiB3aWRnZXRzLmZpbHRlcih3aWRnZXQgPT4gd2lkZ2V0Lmhhc0NsYXNzKENFTExfVE9PTEJBUl9DTEFTUykpIHx8IFtdO1xuICB9XG5cbiAgcHJpdmF0ZSBfcmVtb3ZlVG9vbGJhcihtb2RlbDogSUNlbGxNb2RlbCk6IHZvaWQge1xuICAgIGNvbnN0IGNlbGwgPSB0aGlzLl9nZXRDZWxsKG1vZGVsKTtcbiAgICBpZiAoY2VsbCkge1xuICAgICAgdGhpcy5fZmluZFRvb2xiYXJXaWRnZXRzKGNlbGwpLmZvckVhY2god2lkZ2V0ID0+IHtcbiAgICAgICAgd2lkZ2V0LmRpc3Bvc2UoKTtcbiAgICAgIH0pO1xuICAgICAgLy8gQXR0ZW1wdCB0byByZW1vdmUgdGhlIHJlc2l6ZSBhbmQgY2hhbmdlZCBldmVudCBoYW5kbGVycy5cbiAgICAgIGNlbGwuZGlzcGxheUNoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9yZXNpemVFdmVudENhbGxiYWNrLCB0aGlzKTtcbiAgICB9XG4gICAgbW9kZWwuY29udGVudENoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9jaGFuZ2VkRXZlbnRDYWxsYmFjaywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogQ2FsbCBiYWNrIG9uIHNldHRpbmdzIGNoYW5nZXNcbiAgICovXG4gIHByaXZhdGUgX29uVG9vbGJhckNoYW5nZWQoKTogdm9pZCB7XG4gICAgLy8gUmVzZXQgdG9vbGJhciB3aGVuIHNldHRpbmdzIGNoYW5nZXNcbiAgICBjb25zdCBhY3RpdmVDZWxsOiBDZWxsPElDZWxsTW9kZWw+IHwgbnVsbCB8IHVuZGVmaW5lZCA9XG4gICAgICB0aGlzLl9wYW5lbD8uY29udGVudC5hY3RpdmVDZWxsO1xuICAgIGlmIChhY3RpdmVDZWxsKSB7XG4gICAgICB0aGlzLl9yZW1vdmVUb29sYmFyKGFjdGl2ZUNlbGwubW9kZWwpO1xuICAgICAgdGhpcy5fYWRkVG9vbGJhcihhY3RpdmVDZWxsLm1vZGVsKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9jaGFuZ2VkRXZlbnRDYWxsYmFjaygpOiB2b2lkIHtcbiAgICBjb25zdCBhY3RpdmVDZWxsID0gdGhpcy5fcGFuZWw/LmNvbnRlbnQuYWN0aXZlQ2VsbDtcbiAgICBpZiAoYWN0aXZlQ2VsbCA9PT0gbnVsbCB8fCBhY3RpdmVDZWxsID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl91cGRhdGVDZWxsRm9yVG9vbGJhck92ZXJsYXAoYWN0aXZlQ2VsbCk7XG4gIH1cblxuICBwcml2YXRlIF9yZXNpemVFdmVudENhbGxiYWNrKCk6IHZvaWQge1xuICAgIGNvbnN0IGFjdGl2ZUNlbGwgPSB0aGlzLl9wYW5lbD8uY29udGVudC5hY3RpdmVDZWxsO1xuICAgIGlmIChhY3RpdmVDZWxsID09PSBudWxsIHx8IGFjdGl2ZUNlbGwgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMuX3VwZGF0ZUNlbGxGb3JUb29sYmFyT3ZlcmxhcChhY3RpdmVDZWxsKTtcbiAgfVxuXG4gIHByaXZhdGUgX3VwZGF0ZUNlbGxGb3JUb29sYmFyT3ZlcmxhcChhY3RpdmVDZWxsOiBDZWxsPElDZWxsTW9kZWw+KSB7XG4gICAgLy8gV2hlbiB3ZSBkbyBjaGFuZ2UgaW4gY2VsbCwgSWYgd2UgZG9uJ3Qgd2FpdCB0aGUgYnJvd3NlciBtaWdodCBub3QgaGF2ZVxuICAgIC8vIGNvbXBsZXRlZCB0aGUgbGF5b3V0IHVwZGF0ZSwgcmVzdWx0aW5nIGluIHRoZSBwcmV2aW91cyB3aWR0aCBiZWluZyByZXR1cm5lZFxuICAgIC8vIHVzaW5nIGBnZXRCb3VuZGluZ0NsaWVudFJlY3QoKS53aWR0aGAgaW4gbGF0ZXIgZnVuY3Rpb25zLlxuICAgIHJlcXVlc3RBbmltYXRpb25GcmFtZSgoKSA9PiB7XG4gICAgICAvLyBSZW1vdmUgdGhlIFwidG9vbGJhciBvdmVybGFwXCIgY2xhc3MgZnJvbSB0aGUgY2VsbCwgcmVuZGVyaW5nIHRoZSBjZWxsJ3MgdG9vbGJhclxuICAgICAgY29uc3QgYWN0aXZlQ2VsbEVsZW1lbnQgPSBhY3RpdmVDZWxsLm5vZGU7XG4gICAgICBhY3RpdmVDZWxsRWxlbWVudC5jbGFzc0xpc3QucmVtb3ZlKFRPT0xCQVJfT1ZFUkxBUF9DTEFTUyk7XG4gICAgICBpZiAodGhpcy5fY2VsbFRvb2xiYXJPdmVybGFwc0NvbnRlbnRzKGFjdGl2ZUNlbGwpKSB7XG4gICAgICAgIC8vIEFkZCB0aGUgXCJ0b29sYmFyIG92ZXJsYXBcIiBjbGFzcyB0byB0aGUgY2VsbCwgY29tcGxldGVseSBjb25jZWFsaW5nIHRoZSB0b29sYmFyLFxuICAgICAgICAvLyBpZiB0aGUgZmlyc3QgbGluZSBvZiB0aGUgY29udGVudCBvdmVybGFwcyB3aXRoIGl0IGF0IGFsbFxuICAgICAgICBhY3RpdmVDZWxsRWxlbWVudC5jbGFzc0xpc3QuYWRkKFRPT0xCQVJfT1ZFUkxBUF9DTEFTUyk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9jZWxsVG9vbGJhck92ZXJsYXBzQ29udGVudHMoYWN0aXZlQ2VsbDogQ2VsbDxJQ2VsbE1vZGVsPik6IGJvb2xlYW4ge1xuICAgIGNvbnN0IGNlbGxUeXBlID0gYWN0aXZlQ2VsbC5tb2RlbC50eXBlO1xuXG4gICAgLy8gSWYgdGhlIHRvb2xiYXIgaXMgdG9vIGxhcmdlIGZvciB0aGUgY3VycmVudCBjZWxsLCBoaWRlIGl0LlxuICAgIGNvbnN0IGNlbGxMZWZ0ID0gdGhpcy5fY2VsbEVkaXRvcldpZGdldExlZnQoYWN0aXZlQ2VsbCk7XG4gICAgY29uc3QgY2VsbFJpZ2h0ID0gdGhpcy5fY2VsbEVkaXRvcldpZGdldFJpZ2h0KGFjdGl2ZUNlbGwpO1xuICAgIGNvbnN0IHRvb2xiYXJMZWZ0ID0gdGhpcy5fY2VsbFRvb2xiYXJMZWZ0KGFjdGl2ZUNlbGwpO1xuXG4gICAgaWYgKHRvb2xiYXJMZWZ0ID09PSBudWxsKSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgLy8gVGhlIHRvb2xiYXIgc2hvdWxkIG5vdCB0YWtlIHVwIG1vcmUgdGhhbiA1MCUgb2YgdGhlIGNlbGwuXG4gICAgaWYgKChjZWxsTGVmdCArIGNlbGxSaWdodCkgLyAyID4gdG9vbGJhckxlZnQpIHtcbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cblxuICAgIGlmIChjZWxsVHlwZSA9PT0gJ21hcmtkb3duJyAmJiAoYWN0aXZlQ2VsbCBhcyBNYXJrZG93bkNlbGwpLnJlbmRlcmVkKSB7XG4gICAgICAvLyBDaGVjayBmb3Igb3ZlcmxhcCBpbiByZW5kZXJlZCBtYXJrZG93biBjb250ZW50XG4gICAgICByZXR1cm4gdGhpcy5fbWFya2Rvd25PdmVybGFwc1Rvb2xiYXIoYWN0aXZlQ2VsbCBhcyBNYXJrZG93bkNlbGwpO1xuICAgIH1cblxuICAgIC8vIENoZWNrIGZvciBvdmVybGFwIGluIGNvZGUgY29udGVudFxuICAgIGlmICh0aGlzLl9wYW5lbD8uY29udGVudC5yZW5kZXJpbmdMYXlvdXQgPT09ICdkZWZhdWx0Jykge1xuICAgICAgcmV0dXJuIHRoaXMuX2NvZGVPdmVybGFwc1Rvb2xiYXIoYWN0aXZlQ2VsbCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLl9vdXRwdXRPdmVybGFwc1Rvb2xiYXIoYWN0aXZlQ2VsbCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIENoZWNrIGZvciBvdmVybGFwIGJldHdlZW4gcmVuZGVyZWQgTWFya2Rvd24gYW5kIHRoZSBjZWxsIHRvb2xiYXJcbiAgICpcbiAgICogQHBhcmFtIGFjdGl2ZUNlbGwgQSByZW5kZXJlZCBNYXJrZG93bkNlbGxcbiAgICogQHJldHVybnMgYHRydWVgIGlmIHRoZSBmaXJzdCBsaW5lIG9mIHRoZSBvdXRwdXQgb3ZlcmxhcHMgd2l0aCB0aGUgY2VsbCB0b29sYmFyLCBgZmFsc2VgIG90aGVyd2lzZVxuICAgKi9cbiAgcHJpdmF0ZSBfbWFya2Rvd25PdmVybGFwc1Rvb2xiYXIoYWN0aXZlQ2VsbDogTWFya2Rvd25DZWxsKTogYm9vbGVhbiB7XG4gICAgY29uc3QgbWFya2Rvd25PdXRwdXQgPSBhY3RpdmVDZWxsLmlucHV0QXJlYTsgLy8gUmVuZGVyZWQgbWFya2Rvd24gYXBwZWFycyBpbiB0aGUgaW5wdXQgYXJlYVxuICAgIGlmICghbWFya2Rvd25PdXRwdXQpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICAvLyBHZXQgdGhlIHJlbmRlcmVkIG1hcmtkb3duIGFzIGEgd2lkZ2V0LlxuICAgIGNvbnN0IG1hcmtkb3duT3V0cHV0V2lkZ2V0ID0gbWFya2Rvd25PdXRwdXQucmVuZGVyZWRJbnB1dDtcbiAgICBjb25zdCBtYXJrZG93bk91dHB1dEVsZW1lbnQgPSBtYXJrZG93bk91dHB1dFdpZGdldC5ub2RlO1xuXG4gICAgY29uc3QgZmlyc3RPdXRwdXRFbGVtZW50Q2hpbGQgPVxuICAgICAgbWFya2Rvd25PdXRwdXRFbGVtZW50LmZpcnN0RWxlbWVudENoaWxkIGFzIEhUTUxFbGVtZW50O1xuICAgIGlmIChmaXJzdE91dHB1dEVsZW1lbnRDaGlsZCA9PT0gbnVsbCkge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIC8vIFRlbXBvcmFyaWx5IHNldCB0aGUgZWxlbWVudCdzIG1heCB3aWR0aCBzbyB0aGF0IHRoZSBib3VuZGluZyBjbGllbnQgcmVjdGFuZ2xlIG9ubHkgZW5jb21wYXNzZXMgdGhlIGNvbnRlbnQuXG4gICAgY29uc3Qgb2xkTWF4V2lkdGggPSBmaXJzdE91dHB1dEVsZW1lbnRDaGlsZC5zdHlsZS5tYXhXaWR0aDtcbiAgICBmaXJzdE91dHB1dEVsZW1lbnRDaGlsZC5zdHlsZS5tYXhXaWR0aCA9ICdtYXgtY29udGVudCc7XG5cbiAgICBjb25zdCBsaW5lUmlnaHQgPSBmaXJzdE91dHB1dEVsZW1lbnRDaGlsZC5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS5yaWdodDtcblxuICAgIC8vIFJlaW5zdGF0ZSB0aGUgb2xkIG1heCB3aWR0aC5cbiAgICBmaXJzdE91dHB1dEVsZW1lbnRDaGlsZC5zdHlsZS5tYXhXaWR0aCA9IG9sZE1heFdpZHRoO1xuXG4gICAgY29uc3QgdG9vbGJhckxlZnQgPSB0aGlzLl9jZWxsVG9vbGJhckxlZnQoYWN0aXZlQ2VsbCk7XG5cbiAgICByZXR1cm4gdG9vbGJhckxlZnQgPT09IG51bGwgPyBmYWxzZSA6IGxpbmVSaWdodCA+IHRvb2xiYXJMZWZ0O1xuICB9XG5cbiAgcHJpdmF0ZSBfb3V0cHV0T3ZlcmxhcHNUb29sYmFyKGFjdGl2ZUNlbGw6IENlbGw8SUNlbGxNb2RlbD4pOiBib29sZWFuIHtcbiAgICBjb25zdCBvdXRwdXRBcmVhID0gKGFjdGl2ZUNlbGwgYXMgQ29kZUNlbGwpLm91dHB1dEFyZWEubm9kZTtcbiAgICBpZiAob3V0cHV0QXJlYSkge1xuICAgICAgY29uc3Qgb3V0cHV0cyA9IG91dHB1dEFyZWEucXVlcnlTZWxlY3RvckFsbCgnW2RhdGEtbWltZS10eXBlXScpO1xuICAgICAgY29uc3QgdG9vbGJhclJlY3QgPSB0aGlzLl9jZWxsVG9vbGJhclJlY3QoYWN0aXZlQ2VsbCk7XG4gICAgICBpZiAodG9vbGJhclJlY3QpIHtcbiAgICAgICAgY29uc3QgeyBsZWZ0OiB0b29sYmFyTGVmdCwgYm90dG9tOiB0b29sYmFyQm90dG9tIH0gPSB0b29sYmFyUmVjdDtcbiAgICAgICAgcmV0dXJuIHNvbWUob3V0cHV0cywgb3V0cHV0ID0+IHtcbiAgICAgICAgICBjb25zdCBub2RlID0gb3V0cHV0LmZpcnN0RWxlbWVudENoaWxkO1xuICAgICAgICAgIGlmIChub2RlKSB7XG4gICAgICAgICAgICBjb25zdCByYW5nZSA9IG5ldyBSYW5nZSgpO1xuICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICBURVhUX01JTUVfVFlQRVMuaW5jbHVkZXMoXG4gICAgICAgICAgICAgICAgb3V0cHV0LmdldEF0dHJpYnV0ZSgnZGF0YS1taW1lLXR5cGUnKSB8fCAnJ1xuICAgICAgICAgICAgICApXG4gICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgLy8gSWYgdGhlIG5vZGUgaXMgcGxhaW4gdGV4dCwgaXQncyBpbiBhIDxwcmU+LiBUbyBnZXQgdGhlIHRydWUgYm91bmRpbmcgYm94IG9mIHRoZVxuICAgICAgICAgICAgICAvLyB0ZXh0LCB0aGUgbm9kZSBjb250ZW50cyBuZWVkIHRvIGJlIHNlbGVjdGVkLlxuICAgICAgICAgICAgICByYW5nZS5zZWxlY3ROb2RlQ29udGVudHMobm9kZSk7XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICByYW5nZS5zZWxlY3ROb2RlKG5vZGUpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgY29uc3QgeyByaWdodDogbm9kZVJpZ2h0LCB0b3A6IG5vZGVUb3AgfSA9XG4gICAgICAgICAgICAgIHJhbmdlLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xuXG4gICAgICAgICAgICAvLyBOb3RlOiB5LWNvb3JkaW5hdGUgaW5jcmVhc2VzIHRvd2FyZCB0aGUgYm90dG9tIG9mIHBhZ2VcbiAgICAgICAgICAgIHJldHVybiBub2RlUmlnaHQgPiB0b29sYmFyTGVmdCAmJiBub2RlVG9wIDwgdG9vbGJhckJvdHRvbTtcbiAgICAgICAgICB9XG4gICAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG5cbiAgcHJpdmF0ZSBfY29kZU92ZXJsYXBzVG9vbGJhcihhY3RpdmVDZWxsOiBDZWxsPElDZWxsTW9kZWw+KTogYm9vbGVhbiB7XG4gICAgY29uc3QgZWRpdG9yV2lkZ2V0ID0gYWN0aXZlQ2VsbC5lZGl0b3JXaWRnZXQ7XG4gICAgY29uc3QgZWRpdG9yID0gYWN0aXZlQ2VsbC5lZGl0b3I7XG4gICAgaWYgKCFlZGl0b3JXaWRnZXQgfHwgIWVkaXRvcikge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIGlmIChlZGl0b3IubGluZUNvdW50IDwgMSkge1xuICAgICAgcmV0dXJuIGZhbHNlOyAvLyBOb3RoaW5nIGluIHRoZSBlZGl0b3JcbiAgICB9XG5cbiAgICBjb25zdCBjb2RlTWlycm9yTGluZXMgPSBlZGl0b3JXaWRnZXQubm9kZS5nZXRFbGVtZW50c0J5Q2xhc3NOYW1lKCdjbS1saW5lJyk7XG4gICAgaWYgKGNvZGVNaXJyb3JMaW5lcy5sZW5ndGggPCAxKSB7XG4gICAgICByZXR1cm4gZmFsc2U7IC8vIE5vIGxpbmVzIHByZXNlbnRcbiAgICB9XG5cbiAgICBsZXQgbGluZVJpZ2h0ID0gY29kZU1pcnJvckxpbmVzWzBdLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLmxlZnQ7XG4gICAgY29uc3QgcmFuZ2UgPSBkb2N1bWVudC5jcmVhdGVSYW5nZSgpO1xuICAgIHJhbmdlLnNlbGVjdE5vZGVDb250ZW50cyhjb2RlTWlycm9yTGluZXNbMF0pO1xuICAgIGxpbmVSaWdodCArPSByYW5nZS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS53aWR0aDtcblxuICAgIGNvbnN0IHRvb2xiYXJMZWZ0ID0gdGhpcy5fY2VsbFRvb2xiYXJMZWZ0KGFjdGl2ZUNlbGwpO1xuXG4gICAgcmV0dXJuIHRvb2xiYXJMZWZ0ID09PSBudWxsID8gZmFsc2UgOiBsaW5lUmlnaHQgPiB0b29sYmFyTGVmdDtcbiAgfVxuXG4gIHByaXZhdGUgX2NlbGxFZGl0b3JXaWRnZXRMZWZ0KGFjdGl2ZUNlbGw6IENlbGw8SUNlbGxNb2RlbD4pOiBudW1iZXIge1xuICAgIHJldHVybiBhY3RpdmVDZWxsLmVkaXRvcldpZGdldD8ubm9kZS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS5sZWZ0ID8/IDA7XG4gIH1cblxuICBwcml2YXRlIF9jZWxsRWRpdG9yV2lkZ2V0UmlnaHQoYWN0aXZlQ2VsbDogQ2VsbDxJQ2VsbE1vZGVsPik6IG51bWJlciB7XG4gICAgcmV0dXJuIGFjdGl2ZUNlbGwuZWRpdG9yV2lkZ2V0Py5ub2RlLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLnJpZ2h0ID8/IDA7XG4gIH1cblxuICBwcml2YXRlIF9jZWxsVG9vbGJhclJlY3QoYWN0aXZlQ2VsbDogQ2VsbDxJQ2VsbE1vZGVsPik6IERPTVJlY3QgfCBudWxsIHtcbiAgICBjb25zdCB0b29sYmFyV2lkZ2V0cyA9IHRoaXMuX2ZpbmRUb29sYmFyV2lkZ2V0cyhhY3RpdmVDZWxsKTtcbiAgICBpZiAodG9vbGJhcldpZGdldHMubGVuZ3RoIDwgMSkge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIGNvbnN0IGFjdGl2ZUNlbGxUb29sYmFyID0gdG9vbGJhcldpZGdldHNbMF0ubm9kZTtcblxuICAgIHJldHVybiBhY3RpdmVDZWxsVG9vbGJhci5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKTtcbiAgfVxuXG4gIHByaXZhdGUgX2NlbGxUb29sYmFyTGVmdChhY3RpdmVDZWxsOiBDZWxsPElDZWxsTW9kZWw+KTogbnVtYmVyIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX2NlbGxUb29sYmFyUmVjdChhY3RpdmVDZWxsKT8ubGVmdCB8fCBudWxsO1xuICB9XG5cbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9wYW5lbDogTm90ZWJvb2tQYW5lbCB8IG51bGw7XG4gIHByaXZhdGUgX3ByZXZpb3VzQWN0aXZlQ2VsbDogQ2VsbDxJQ2VsbE1vZGVsPiB8IG51bGw7XG4gIHByaXZhdGUgX3Rvb2xiYXI6IElPYnNlcnZhYmxlTGlzdDxUb29sYmFyUmVnaXN0cnkuSVRvb2xiYXJJdGVtPjtcbn1cblxuY29uc3QgZGVmYXVsdFRvb2xiYXJJdGVtczogVG9vbGJhclJlZ2lzdHJ5LklXaWRnZXRbXSA9IFtcbiAge1xuICAgIGNvbW1hbmQ6ICdub3RlYm9vazpkdXBsaWNhdGUtYmVsb3cnLFxuICAgIG5hbWU6ICdkdXBsaWNhdGUtY2VsbCdcbiAgfSxcbiAge1xuICAgIGNvbW1hbmQ6ICdub3RlYm9vazptb3ZlLWNlbGwtdXAnLFxuICAgIG5hbWU6ICdtb3ZlLWNlbGwtdXAnXG4gIH0sXG4gIHtcbiAgICBjb21tYW5kOiAnbm90ZWJvb2s6bW92ZS1jZWxsLWRvd24nLFxuICAgIG5hbWU6ICdtb3ZlLWNlbGwtZG93bidcbiAgfSxcbiAge1xuICAgIGNvbW1hbmQ6ICdub3RlYm9vazppbnNlcnQtY2VsbC1hYm92ZScsXG4gICAgbmFtZTogJ2luc2VydC1jZWxsLWFib3ZlJ1xuICB9LFxuICB7XG4gICAgY29tbWFuZDogJ25vdGVib29rOmluc2VydC1jZWxsLWJlbG93JyxcbiAgICBuYW1lOiAnaW5zZXJ0LWNlbGwtYmVsb3cnXG4gIH0sXG4gIHtcbiAgICBjb21tYW5kOiAnbm90ZWJvb2s6ZGVsZXRlLWNlbGwnLFxuICAgIG5hbWU6ICdkZWxldGUtY2VsbCdcbiAgfVxuXTtcblxuLyoqXG4gKiBXaWRnZXQgZXh0ZW5zaW9uIHRoYXQgY3JlYXRlcyBhIENlbGxUb29sYmFyVHJhY2tlciBlYWNoIHRpbWUgYSBub3RlYm9vayBpc1xuICogY3JlYXRlZC5cbiAqL1xuZXhwb3J0IGNsYXNzIENlbGxCYXJFeHRlbnNpb24gaW1wbGVtZW50cyBEb2N1bWVudFJlZ2lzdHJ5LldpZGdldEV4dGVuc2lvbiB7XG4gIHN0YXRpYyBGQUNUT1JZX05BTUUgPSAnQ2VsbCc7XG5cbiAgY29uc3RydWN0b3IoXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICB0b29sYmFyRmFjdG9yeT86IChcbiAgICAgIHdpZGdldDogV2lkZ2V0XG4gICAgKSA9PiBJT2JzZXJ2YWJsZUxpc3Q8VG9vbGJhclJlZ2lzdHJ5LklUb29sYmFySXRlbT5cbiAgKSB7XG4gICAgdGhpcy5fY29tbWFuZHMgPSBjb21tYW5kcztcbiAgICB0aGlzLl90b29sYmFyRmFjdG9yeSA9IHRvb2xiYXJGYWN0b3J5ID8/IHRoaXMuZGVmYXVsdFRvb2xiYXJGYWN0b3J5O1xuICB9XG5cbiAgcHJvdGVjdGVkIGdldCBkZWZhdWx0VG9vbGJhckZhY3RvcnkoKTogKFxuICAgIHdpZGdldDogV2lkZ2V0XG4gICkgPT4gSU9ic2VydmFibGVMaXN0PFRvb2xiYXJSZWdpc3RyeS5JVG9vbGJhckl0ZW0+IHtcbiAgICBjb25zdCBpdGVtRmFjdG9yeSA9IGNyZWF0ZURlZmF1bHRGYWN0b3J5KHRoaXMuX2NvbW1hbmRzKTtcbiAgICByZXR1cm4gKHdpZGdldDogV2lkZ2V0KSA9PlxuICAgICAgbmV3IE9ic2VydmFibGVMaXN0KHtcbiAgICAgICAgdmFsdWVzOiBkZWZhdWx0VG9vbGJhckl0ZW1zLm1hcChpdGVtID0+IHtcbiAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgbmFtZTogaXRlbS5uYW1lLFxuICAgICAgICAgICAgd2lkZ2V0OiBpdGVtRmFjdG9yeShDZWxsQmFyRXh0ZW5zaW9uLkZBQ1RPUllfTkFNRSwgd2lkZ2V0LCBpdGVtKVxuICAgICAgICAgIH07XG4gICAgICAgIH0pXG4gICAgICB9KTtcbiAgfVxuXG4gIGNyZWF0ZU5ldyhwYW5lbDogTm90ZWJvb2tQYW5lbCk6IElEaXNwb3NhYmxlIHtcbiAgICByZXR1cm4gbmV3IENlbGxUb29sYmFyVHJhY2tlcihwYW5lbCwgdGhpcy5fdG9vbGJhckZhY3RvcnkocGFuZWwpKTtcbiAgfVxuXG4gIHByaXZhdGUgX2NvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnk7XG4gIHByaXZhdGUgX3Rvb2xiYXJGYWN0b3J5OiAoXG4gICAgd2lkZ2V0OiBXaWRnZXRcbiAgKSA9PiBJT2JzZXJ2YWJsZUxpc3Q8VG9vbGJhclJlZ2lzdHJ5LklUb29sYmFySXRlbT47XG59XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGNlbGwtdG9vbGJhclxuICovXG5leHBvcnQgKiBmcm9tICcuL2NlbGx0b29sYmFydHJhY2tlcic7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=