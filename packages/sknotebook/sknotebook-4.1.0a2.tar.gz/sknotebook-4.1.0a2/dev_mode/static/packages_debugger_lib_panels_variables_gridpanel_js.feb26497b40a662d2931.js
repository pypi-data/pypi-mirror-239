"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_debugger_lib_panels_variables_gridpanel_js"],{

/***/ "../packages/debugger/lib/panels/variables/gridpanel.js":
/*!**************************************************************!*\
  !*** ../packages/debugger/lib/panels/variables/gridpanel.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Grid": () => (/* binding */ Grid),
/* harmony export */   "GridModel": () => (/* binding */ GridModel)
/* harmony export */ });
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../ */ "../packages/debugger/lib/debugger.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * A class wrapping the underlying variables datagrid.
 */
class Grid extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel {
    /**
     * Instantiate a new VariablesGrid.
     *
     * @param options The instantiation options for a VariablesGrid.
     */
    constructor(options) {
        super();
        const { commands, model, themeManager } = options;
        this.model = model;
        const dataModel = new GridModel(options.translator);
        const grid = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__.DataGrid();
        const mouseHandler = new Private.MouseHandler();
        mouseHandler.doubleClicked.connect((_, hit) => commands.execute(___WEBPACK_IMPORTED_MODULE_4__.Debugger.CommandIDs.inspectVariable, {
            variableReference: dataModel.getVariableReference(hit.row),
            name: dataModel.getVariableName(hit.row)
        }));
        mouseHandler.selected.connect((_, hit) => {
            const { row } = hit;
            this.model.selectedVariable = {
                name: dataModel.getVariableName(row),
                value: dataModel.data('body', row, 1),
                type: dataModel.data('body', row, 2),
                variablesReference: dataModel.getVariableReference(row)
            };
        });
        grid.dataModel = dataModel;
        grid.keyHandler = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__.BasicKeyHandler();
        grid.mouseHandler = mouseHandler;
        grid.selectionModel = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__.BasicSelectionModel({
            dataModel
        });
        grid.stretchLastColumn = true;
        grid.node.style.height = '100%';
        this._grid = grid;
        // Compute the grid's styles based on the current theme.
        if (themeManager) {
            themeManager.themeChanged.connect(this._updateStyles, this);
        }
        this.addWidget(grid);
    }
    /**
     * Set the variable filter list.
     *
     * @param filter The variable filter to apply.
     */
    set filter(filter) {
        this._grid.dataModel.filter = filter;
        this.update();
    }
    /**
     * Set the scope for the variables data model.
     *
     * @param scope The scopes for the variables
     */
    set scope(scope) {
        this._grid.dataModel.scope = scope;
        this.update();
    }
    /**
     * Get the data model for the data grid.
     */
    get dataModel() {
        return this._grid.dataModel;
    }
    /**
     * Handle `after-attach` messages.
     *
     * @param message - The `after-attach` message.
     */
    onAfterAttach(message) {
        super.onAfterAttach(message);
        this._updateStyles();
    }
    /**
     * Update the computed style for the data grid on theme change.
     */
    _updateStyles() {
        const { style, textRenderer } = Private.computeStyle();
        this._grid.cellRenderers.update({}, textRenderer);
        this._grid.style = style;
    }
}
/**
 * A data grid model for variables.
 */
class GridModel extends _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__.DataModel {
    /**
     * Create gird model
     * @param translator optional translator
     */
    constructor(translator) {
        super();
        this._filter = new Set();
        this._scope = '';
        this._data = {
            name: [],
            type: [],
            value: [],
            variablesReference: []
        };
        this._trans = (translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator).load('jupyterlab');
    }
    /**
     * The variable filter list.
     */
    get filter() {
        return this._filter;
    }
    set filter(filter) {
        this._filter = filter;
    }
    /**
     * The current scope for the variables.
     */
    get scope() {
        return this._scope;
    }
    set scope(scope) {
        this._scope = scope;
    }
    /**
     * Get the row count for a particular region in the data grid.
     *
     * @param region The datagrid region.
     */
    rowCount(region) {
        return region === 'body' ? this._data.name.length : 1;
    }
    /**
     * Get the column count for a particular region in the data grid.
     *
     * @param region The datagrid region.
     */
    columnCount(region) {
        return region === 'body' ? 2 : 1;
    }
    /**
     * Get the data count for a particular region, row and column in the data grid.
     *
     * @param region The datagrid region.
     * @param row The datagrid row
     * @param column The datagrid column
     */
    data(region, row, column) {
        if (region === 'row-header') {
            return this._data.name[row];
        }
        if (region === 'column-header') {
            return column === 1 ? this._trans.__('Value') : this._trans.__('Type');
        }
        if (region === 'corner-header') {
            return this._trans.__('Name');
        }
        return column === 1 ? this._data.value[row] : this._data.type[row];
    }
    /**
     * Get the variable reference for a given row
     *
     * @param row The row in the datagrid.
     */
    getVariableReference(row) {
        return this._data.variablesReference[row];
    }
    /**
     * Get the variable name for a given row
     *
     * @param row The row in the datagrid.
     */
    getVariableName(row) {
        return this._data.name[row];
    }
    /**
     * Set the datagrid model data from the list of variables.
     *
     * @param scopes The list of variables.
     */
    setData(scopes) {
        var _a, _b;
        this._clearData();
        this.emitChanged({
            type: 'model-reset',
            region: 'body'
        });
        const scope = (_a = scopes.find(scope => scope.name === this._scope)) !== null && _a !== void 0 ? _a : scopes[0];
        const variables = (_b = scope === null || scope === void 0 ? void 0 : scope.variables) !== null && _b !== void 0 ? _b : [];
        const filtered = variables.filter(variable => variable.name && !this._filter.has(variable.name));
        filtered.forEach((variable, index) => {
            var _a;
            this._data.name[index] = variable.name;
            this._data.type[index] = (_a = variable.type) !== null && _a !== void 0 ? _a : '';
            this._data.value[index] = variable.value;
            this._data.variablesReference[index] = variable.variablesReference;
        });
        this.emitChanged({
            type: 'rows-inserted',
            region: 'body',
            index: 1,
            span: filtered.length
        });
    }
    /**
     * Clear all the data in the datagrid.
     */
    _clearData() {
        this._data = {
            name: [],
            type: [],
            value: [],
            variablesReference: []
        };
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create a color palette element.
     */
    function createPalette() {
        const div = document.createElement('div');
        div.className = 'jp-DebuggerVariables-colorPalette';
        div.innerHTML = `
        <div class="jp-mod-void"></div>
        <div class="jp-mod-background"></div>
        <div class="jp-mod-header-background"></div>
        <div class="jp-mod-grid-line"></div>
        <div class="jp-mod-header-grid-line"></div>
        <div class="jp-mod-selection"></div>
        <div class="jp-mod-text"></div>
      `;
        return div;
    }
    /**
     * Compute the style and renderer for a data grid.
     */
    function computeStyle() {
        const palette = createPalette();
        document.body.appendChild(palette);
        let node;
        node = palette.querySelector('.jp-mod-void');
        const voidColor = getComputedStyle(node).color;
        node = palette.querySelector('.jp-mod-background');
        const backgroundColor = getComputedStyle(node).color;
        node = palette.querySelector('.jp-mod-header-background');
        const headerBackgroundColor = getComputedStyle(node).color;
        node = palette.querySelector('.jp-mod-grid-line');
        const gridLineColor = getComputedStyle(node).color;
        node = palette.querySelector('.jp-mod-header-grid-line');
        const headerGridLineColor = getComputedStyle(node).color;
        node = palette.querySelector('.jp-mod-selection');
        const selectionFillColor = getComputedStyle(node).color;
        node = palette.querySelector('.jp-mod-text');
        const textColor = getComputedStyle(node).color;
        document.body.removeChild(palette);
        return {
            style: {
                voidColor,
                backgroundColor,
                headerBackgroundColor,
                gridLineColor,
                headerGridLineColor,
                rowBackgroundColor: (i) => i % 2 === 0 ? voidColor : backgroundColor,
                selectionFillColor
            },
            textRenderer: new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__.TextRenderer({
                font: '12px sans-serif',
                textColor,
                backgroundColor: '',
                verticalAlignment: 'center',
                horizontalAlignment: 'left'
            })
        };
    }
    Private.computeStyle = computeStyle;
    /**
     * A custom click handler to handle clicks on the variables grid.
     */
    class MouseHandler extends _lumino_datagrid__WEBPACK_IMPORTED_MODULE_0__.BasicMouseHandler {
        constructor() {
            super(...arguments);
            this._doubleClicked = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
            this._selected = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        }
        /**
         * A signal emitted when the variables grid is double clicked.
         */
        get doubleClicked() {
            return this._doubleClicked;
        }
        /**
         * A signal emitted when the variables grid received mouse down or context menu event.
         */
        get selected() {
            return this._selected;
        }
        /**
         * Dispose of the resources held by the mouse handler.
         */
        dispose() {
            if (this.isDisposed) {
                return;
            }
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.disconnectSender(this);
            super.dispose();
        }
        /**
         * Handle a mouse double-click event.
         *
         * @param grid The datagrid clicked.
         * @param event The mouse event.
         */
        onMouseDoubleClick(grid, event) {
            const hit = grid.hitTest(event.clientX, event.clientY);
            this._doubleClicked.emit(hit);
        }
        /**
         * Handle the mouse down event for the data grid.
         *
         * @param grid - The data grid of interest.
         *
         * @param event - The mouse down event of interest.
         */
        onMouseDown(grid, event) {
            // Unpack the event.
            let { clientX, clientY } = event;
            // Hit test the grid.
            let hit = grid.hitTest(clientX, clientY);
            this._selected.emit(hit);
            // Propagate event to Lumino DataGrid BasicMouseHandler.
            super.onMouseDown(grid, event);
        }
        /**
         * Handle the context menu event for the data grid.
         *
         * @param grid - The data grid of interest.
         *
         * @param event - The context menu event of interest.
         */
        onContextMenu(grid, event) {
            // Unpack the event.
            let { clientX, clientY } = event;
            // Hit test the grid.
            let hit = grid.hitTest(clientX, clientY);
            this._selected.emit(hit);
        }
    }
    Private.MouseHandler = MouseHandler;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZGVidWdnZXJfbGliX3BhbmVsc192YXJpYWJsZXNfZ3JpZHBhbmVsX2pzLmZlYjI2NDk3YjQwYTY2MmQyOTMxLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQVVqQztBQUMwQjtBQUNaO0FBT1A7QUFHQztBQUVsQzs7R0FFRztBQUNJLE1BQU0sSUFBSyxTQUFRLGtEQUFLO0lBQzdCOzs7O09BSUc7SUFDSCxZQUFZLE9BQXNCO1FBQ2hDLEtBQUssRUFBRSxDQUFDO1FBQ1IsTUFBTSxFQUFFLFFBQVEsRUFBRSxLQUFLLEVBQUUsWUFBWSxFQUFFLEdBQUcsT0FBTyxDQUFDO1FBQ2xELElBQUksQ0FBQyxLQUFLLEdBQUcsS0FBSyxDQUFDO1FBQ25CLE1BQU0sU0FBUyxHQUFHLElBQUksU0FBUyxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsQ0FBQztRQUNwRCxNQUFNLElBQUksR0FBRyxJQUFJLHNEQUFRLEVBQUUsQ0FBQztRQUM1QixNQUFNLFlBQVksR0FBRyxJQUFJLE9BQU8sQ0FBQyxZQUFZLEVBQUUsQ0FBQztRQUNoRCxZQUFZLENBQUMsYUFBYSxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUMsRUFBRSxHQUFHLEVBQUUsRUFBRSxDQUM1QyxRQUFRLENBQUMsT0FBTyxDQUFDLGtFQUFtQyxFQUFFO1lBQ3BELGlCQUFpQixFQUFFLFNBQVMsQ0FBQyxvQkFBb0IsQ0FBQyxHQUFHLENBQUMsR0FBRyxDQUFDO1lBQzFELElBQUksRUFBRSxTQUFTLENBQUMsZUFBZSxDQUFDLEdBQUcsQ0FBQyxHQUFHLENBQUM7U0FDekMsQ0FBQyxDQUNILENBQUM7UUFDRixZQUFZLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUMsRUFBRSxHQUFHLEVBQUUsRUFBRTtZQUN2QyxNQUFNLEVBQUUsR0FBRyxFQUFFLEdBQUcsR0FBRyxDQUFDO1lBQ3BCLElBQUksQ0FBQyxLQUFLLENBQUMsZ0JB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Z2VzL2RlYnVnZ2VyL3NyYy9wYW5lbHMvdmFyaWFibGVzL2dyaWRwYW5lbC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHtcbiAgQmFzaWNLZXlIYW5kbGVyLFxuICBCYXNpY01vdXNlSGFuZGxlcixcbiAgQmFzaWNTZWxlY3Rpb25Nb2RlbCxcbiAgRGF0YUdyaWQsXG4gIERhdGFNb2RlbCxcbiAgVGV4dFJlbmRlcmVyXG59IGZyb20gJ0BsdW1pbm8vZGF0YWdyaWQnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgUGFuZWwgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG5pbXBvcnQgeyBJVGhlbWVNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbmltcG9ydCB7IElEZWJ1Z2dlciB9IGZyb20gJy4uLy4uL3Rva2Vucyc7XG5pbXBvcnQgeyBEZWJ1Z2dlciB9IGZyb20gJy4uLy4uLyc7XG5cbi8qKlxuICogQSBjbGFzcyB3cmFwcGluZyB0aGUgdW5kZXJseWluZyB2YXJpYWJsZXMgZGF0YWdyaWQuXG4gKi9cbmV4cG9ydCBjbGFzcyBHcmlkIGV4dGVuZHMgUGFuZWwge1xuICAvKipcbiAgICogSW5zdGFudGlhdGUgYSBuZXcgVmFyaWFibGVzR3JpZC5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSBWYXJpYWJsZXNHcmlkLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogR3JpZC5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgY29uc3QgeyBjb21tYW5kcywgbW9kZWwsIHRoZW1lTWFuYWdlciB9ID0gb3B0aW9ucztcbiAgICB0aGlzLm1vZGVsID0gbW9kZWw7XG4gICAgY29uc3QgZGF0YU1vZGVsID0gbmV3IEdyaWRNb2RlbChvcHRpb25zLnRyYW5zbGF0b3IpO1xuICAgIGNvbnN0IGdyaWQgPSBuZXcgRGF0YUdyaWQoKTtcbiAgICBjb25zdCBtb3VzZUhhbmRsZXIgPSBuZXcgUHJpdmF0ZS5Nb3VzZUhhbmRsZXIoKTtcbiAgICBtb3VzZUhhbmRsZXIuZG91YmxlQ2xpY2tlZC5jb25uZWN0KChfLCBoaXQpID0+XG4gICAgICBjb21tYW5kcy5leGVjdXRlKERlYnVnZ2VyLkNvbW1hbmRJRHMuaW5zcGVjdFZhcmlhYmxlLCB7XG4gICAgICAgIHZhcmlhYmxlUmVmZXJlbmNlOiBkYXRhTW9kZWwuZ2V0VmFyaWFibGVSZWZlcmVuY2UoaGl0LnJvdyksXG4gICAgICAgIG5hbWU6IGRhdGFNb2RlbC5nZXRWYXJpYWJsZU5hbWUoaGl0LnJvdylcbiAgICAgIH0pXG4gICAgKTtcbiAgICBtb3VzZUhhbmRsZXIuc2VsZWN0ZWQuY29ubmVjdCgoXywgaGl0KSA9PiB7XG4gICAgICBjb25zdCB7IHJvdyB9ID0gaGl0O1xuICAgICAgdGhpcy5tb2RlbC5zZWxlY3RlZFZhcmlhYmxlID0ge1xuICAgICAgICBuYW1lOiBkYXRhTW9kZWwuZ2V0VmFyaWFibGVOYW1lKHJvdyksXG4gICAgICAgIHZhbHVlOiBkYXRhTW9kZWwuZGF0YSgnYm9keScsIHJvdywgMSksXG4gICAgICAgIHR5cGU6IGRhdGFNb2RlbC5kYXRhKCdib2R5Jywgcm93LCAyKSxcbiAgICAgICAgdmFyaWFibGVzUmVmZXJlbmNlOiBkYXRhTW9kZWwuZ2V0VmFyaWFibGVSZWZlcmVuY2Uocm93KVxuICAgICAgfTtcbiAgICB9KTtcbiAgICBncmlkLmRhdGFNb2RlbCA9IGRhdGFNb2RlbDtcbiAgICBncmlkLmtleUhhbmRsZXIgPSBuZXcgQmFzaWNLZXlIYW5kbGVyKCk7XG4gICAgZ3JpZC5tb3VzZUhhbmRsZXIgPSBtb3VzZUhhbmRsZXI7XG4gICAgZ3JpZC5zZWxlY3Rpb25Nb2RlbCA9IG5ldyBCYXNpY1NlbGVjdGlvbk1vZGVsKHtcbiAgICAgIGRhdGFNb2RlbFxuICAgIH0pO1xuICAgIGdyaWQuc3RyZXRjaExhc3RDb2x1bW4gPSB0cnVlO1xuICAgIGdyaWQubm9kZS5zdHlsZS5oZWlnaHQgPSAnMTAwJSc7XG4gICAgdGhpcy5fZ3JpZCA9IGdyaWQ7XG5cbiAgICAvLyBDb21wdXRlIHRoZSBncmlkJ3Mgc3R5bGVzIGJhc2VkIG9uIHRoZSBjdXJyZW50IHRoZW1lLlxuICAgIGlmICh0aGVtZU1hbmFnZXIpIHtcbiAgICAgIHRoZW1lTWFuYWdlci50aGVtZUNoYW5nZWQuY29ubmVjdCh0aGlzLl91cGRhdGVTdHlsZXMsIHRoaXMpO1xuICAgIH1cbiAgICB0aGlzLmFkZFdpZGdldChncmlkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHZhcmlhYmxlIGZpbHRlciBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gZmlsdGVyIFRoZSB2YXJpYWJsZSBmaWx0ZXIgdG8gYXBwbHkuXG4gICAqL1xuICBzZXQgZmlsdGVyKGZpbHRlcjogU2V0PHN0cmluZz4pIHtcbiAgICAodGhpcy5fZ3JpZC5kYXRhTW9kZWwgYXMgR3JpZE1vZGVsKS5maWx0ZXIgPSBmaWx0ZXI7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHNjb3BlIGZvciB0aGUgdmFyaWFibGVzIGRhdGEgbW9kZWwuXG4gICAqXG4gICAqIEBwYXJhbSBzY29wZSBUaGUgc2NvcGVzIGZvciB0aGUgdmFyaWFibGVzXG4gICAqL1xuICBzZXQgc2NvcGUoc2NvcGU6IHN0cmluZykge1xuICAgICh0aGlzLl9ncmlkLmRhdGFNb2RlbCBhcyBHcmlkTW9kZWwpLnNjb3BlID0gc2NvcGU7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGRhdGEgbW9kZWwgZm9yIHRoZSBkYXRhIGdyaWQuXG4gICAqL1xuICBnZXQgZGF0YU1vZGVsKCk6IEdyaWRNb2RlbCB7XG4gICAgcmV0dXJuIHRoaXMuX2dyaWQuZGF0YU1vZGVsIGFzIEdyaWRNb2RlbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGFmdGVyLWF0dGFjaGAgbWVzc2FnZXMuXG4gICAqXG4gICAqIEBwYXJhbSBtZXNzYWdlIC0gVGhlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2UuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtZXNzYWdlOiBhbnkpOiB2b2lkIHtcbiAgICBzdXBlci5vbkFmdGVyQXR0YWNoKG1lc3NhZ2UpO1xuICAgIHRoaXMuX3VwZGF0ZVN0eWxlcygpO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgY29tcHV0ZWQgc3R5bGUgZm9yIHRoZSBkYXRhIGdyaWQgb24gdGhlbWUgY2hhbmdlLlxuICAgKi9cbiAgcHJpdmF0ZSBfdXBkYXRlU3R5bGVzKCk6IHZvaWQge1xuICAgIGNvbnN0IHsgc3R5bGUsIHRleHRSZW5kZXJlciB9ID0gUHJpdmF0ZS5jb21wdXRlU3R5bGUoKTtcbiAgICB0aGlzLl9ncmlkLmNlbGxSZW5kZXJlcnMudXBkYXRlKHt9LCB0ZXh0UmVuZGVyZXIpO1xuICAgIHRoaXMuX2dyaWQuc3R5bGUgPSBzdHlsZTtcbiAgfVxuXG4gIHByaXZhdGUgX2dyaWQ6IERhdGFHcmlkO1xuICBwcm90ZWN0ZWQgbW9kZWw6IElEZWJ1Z2dlci5Nb2RlbC5JVmFyaWFibGVzO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBWYXJpYWJsZXNHcmlkIGBzdGF0aWNzYC5cbiAqL1xubmFtZXNwYWNlIEdyaWQge1xuICAvKipcbiAgICogSW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBgVmFyaWFibGVzR3JpZGAuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY29tbWFuZHMgcmVnaXN0cnkuXG4gICAgICovXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSB2YXJpYWJsZXMgbW9kZWwuXG4gICAgICovXG4gICAgbW9kZWw6IElEZWJ1Z2dlci5Nb2RlbC5JVmFyaWFibGVzO1xuXG4gICAgLyoqXG4gICAgICogQW4gb3B0aW9uYWwgYXBwbGljYXRpb24gdGhlbWUgbWFuYWdlciB0byBkZXRlY3QgdGhlbWUgY2hhbmdlcy5cbiAgICAgKi9cbiAgICB0aGVtZU1hbmFnZXI/OiBJVGhlbWVNYW5hZ2VyIHwgbnVsbDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuXG4vKipcbiAqIEEgZGF0YSBncmlkIG1vZGVsIGZvciB2YXJpYWJsZXMuXG4gKi9cbmV4cG9ydCBjbGFzcyBHcmlkTW9kZWwgZXh0ZW5kcyBEYXRhTW9kZWwge1xuICAvKipcbiAgICogQ3JlYXRlIGdpcmQgbW9kZWxcbiAgICogQHBhcmFtIHRyYW5zbGF0b3Igb3B0aW9uYWwgdHJhbnNsYXRvclxuICAgKi9cbiAgY29uc3RydWN0b3IodHJhbnNsYXRvcj86IElUcmFuc2xhdG9yKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl90cmFucyA9ICh0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHZhcmlhYmxlIGZpbHRlciBsaXN0LlxuICAgKi9cbiAgZ2V0IGZpbHRlcigpOiBTZXQ8c3RyaW5nPiB7XG4gICAgcmV0dXJuIHRoaXMuX2ZpbHRlcjtcbiAgfVxuICBzZXQgZmlsdGVyKGZpbHRlcjogU2V0PHN0cmluZz4pIHtcbiAgICB0aGlzLl9maWx0ZXIgPSBmaWx0ZXI7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgc2NvcGUgZm9yIHRoZSB2YXJpYWJsZXMuXG4gICAqL1xuICBnZXQgc2NvcGUoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fc2NvcGU7XG4gIH1cbiAgc2V0IHNjb3BlKHNjb3BlOiBzdHJpbmcpIHtcbiAgICB0aGlzLl9zY29wZSA9IHNjb3BlO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgcm93IGNvdW50IGZvciBhIHBhcnRpY3VsYXIgcmVnaW9uIGluIHRoZSBkYXRhIGdyaWQuXG4gICAqXG4gICAqIEBwYXJhbSByZWdpb24gVGhlIGRhdGFncmlkIHJlZ2lvbi5cbiAgICovXG4gIHJvd0NvdW50KHJlZ2lvbjogRGF0YU1vZGVsLlJvd1JlZ2lvbik6IG51bWJlciB7XG4gICAgcmV0dXJuIHJlZ2lvbiA9PT0gJ2JvZHknID8gdGhpcy5fZGF0YS5uYW1lLmxlbmd0aCA6IDE7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBjb2x1bW4gY291bnQgZm9yIGEgcGFydGljdWxhciByZWdpb24gaW4gdGhlIGRhdGEgZ3JpZC5cbiAgICpcbiAgICogQHBhcmFtIHJlZ2lvbiBUaGUgZGF0YWdyaWQgcmVnaW9uLlxuICAgKi9cbiAgY29sdW1uQ291bnQocmVnaW9uOiBEYXRhTW9kZWwuQ29sdW1uUmVnaW9uKTogbnVtYmVyIHtcbiAgICByZXR1cm4gcmVnaW9uID09PSAnYm9keScgPyAyIDogMTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGRhdGEgY291bnQgZm9yIGEgcGFydGljdWxhciByZWdpb24sIHJvdyBhbmQgY29sdW1uIGluIHRoZSBkYXRhIGdyaWQuXG4gICAqXG4gICAqIEBwYXJhbSByZWdpb24gVGhlIGRhdGFncmlkIHJlZ2lvbi5cbiAgICogQHBhcmFtIHJvdyBUaGUgZGF0YWdyaWQgcm93XG4gICAqIEBwYXJhbSBjb2x1bW4gVGhlIGRhdGFncmlkIGNvbHVtblxuICAgKi9cbiAgZGF0YShyZWdpb246IERhdGFNb2RlbC5DZWxsUmVnaW9uLCByb3c6IG51bWJlciwgY29sdW1uOiBudW1iZXIpOiBhbnkge1xuICAgIGlmIChyZWdpb24gPT09ICdyb3ctaGVhZGVyJykge1xuICAgICAgcmV0dXJuIHRoaXMuX2RhdGEubmFtZVtyb3ddO1xuICAgIH1cblxuICAgIGlmIChyZWdpb24gPT09ICdjb2x1bW4taGVhZGVyJykge1xuICAgICAgcmV0dXJuIGNvbHVtbiA9PT0gMSA/IHRoaXMuX3RyYW5zLl9fKCdWYWx1ZScpIDogdGhpcy5fdHJhbnMuX18oJ1R5cGUnKTtcbiAgICB9XG4gICAgaWYgKHJlZ2lvbiA9PT0gJ2Nvcm5lci1oZWFkZXInKSB7XG4gICAgICByZXR1cm4gdGhpcy5fdHJhbnMuX18oJ05hbWUnKTtcbiAgICB9XG5cbiAgICByZXR1cm4gY29sdW1uID09PSAxID8gdGhpcy5fZGF0YS52YWx1ZVtyb3ddIDogdGhpcy5fZGF0YS50eXBlW3Jvd107XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSB2YXJpYWJsZSByZWZlcmVuY2UgZm9yIGEgZ2l2ZW4gcm93XG4gICAqXG4gICAqIEBwYXJhbSByb3cgVGhlIHJvdyBpbiB0aGUgZGF0YWdyaWQuXG4gICAqL1xuICBnZXRWYXJpYWJsZVJlZmVyZW5jZShyb3c6IG51bWJlcik6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX2RhdGEudmFyaWFibGVzUmVmZXJlbmNlW3Jvd107XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSB2YXJpYWJsZSBuYW1lIGZvciBhIGdpdmVuIHJvd1xuICAgKlxuICAgKiBAcGFyYW0gcm93IFRoZSByb3cgaW4gdGhlIGRhdGFncmlkLlxuICAgKi9cbiAgZ2V0VmFyaWFibGVOYW1lKHJvdzogbnVtYmVyKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fZGF0YS5uYW1lW3Jvd107XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBkYXRhZ3JpZCBtb2RlbCBkYXRhIGZyb20gdGhlIGxpc3Qgb2YgdmFyaWFibGVzLlxuICAgKlxuICAgKiBAcGFyYW0gc2NvcGVzIFRoZSBsaXN0IG9mIHZhcmlhYmxlcy5cbiAgICovXG4gIHNldERhdGEoc2NvcGVzOiBJRGVidWdnZXIuSVNjb3BlW10pOiB2b2lkIHtcbiAgICB0aGlzLl9jbGVhckRhdGEoKTtcbiAgICB0aGlzLmVtaXRDaGFuZ2VkKHtcbiAgICAgIHR5cGU6ICdtb2RlbC1yZXNldCcsXG4gICAgICByZWdpb246ICdib2R5J1xuICAgIH0pO1xuICAgIGNvbnN0IHNjb3BlID0gc2NvcGVzLmZpbmQoc2NvcGUgPT4gc2NvcGUubmFtZSA9PT0gdGhpcy5fc2NvcGUpID8/IHNjb3Blc1swXTtcbiAgICBjb25zdCB2YXJpYWJsZXMgPSBzY29wZT8udmFyaWFibGVzID8/IFtdO1xuICAgIGNvbnN0IGZpbHRlcmVkID0gdmFyaWFibGVzLmZpbHRlcihcbiAgICAgIHZhcmlhYmxlID0+IHZhcmlhYmxlLm5hbWUgJiYgIXRoaXMuX2ZpbHRlci5oYXModmFyaWFibGUubmFtZSlcbiAgICApO1xuICAgIGZpbHRlcmVkLmZvckVhY2goKHZhcmlhYmxlLCBpbmRleCkgPT4ge1xuICAgICAgdGhpcy5fZGF0YS5uYW1lW2luZGV4XSA9IHZhcmlhYmxlLm5hbWU7XG4gICAgICB0aGlzLl9kYXRhLnR5cGVbaW5kZXhdID0gdmFyaWFibGUudHlwZSA/PyAnJztcbiAgICAgIHRoaXMuX2RhdGEudmFsdWVbaW5kZXhdID0gdmFyaWFibGUudmFsdWU7XG4gICAgICB0aGlzLl9kYXRhLnZhcmlhYmxlc1JlZmVyZW5jZVtpbmRleF0gPSB2YXJpYWJsZS52YXJpYWJsZXNSZWZlcmVuY2U7XG4gICAgfSk7XG4gICAgdGhpcy5lbWl0Q2hhbmdlZCh7XG4gICAgICB0eXBlOiAncm93cy1pbnNlcnRlZCcsXG4gICAgICByZWdpb246ICdib2R5JyxcbiAgICAgIGluZGV4OiAxLFxuICAgICAgc3BhbjogZmlsdGVyZWQubGVuZ3RoXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQ2xlYXIgYWxsIHRoZSBkYXRhIGluIHRoZSBkYXRhZ3JpZC5cbiAgICovXG4gIHByaXZhdGUgX2NsZWFyRGF0YSgpOiB2b2lkIHtcbiAgICB0aGlzLl9kYXRhID0ge1xuICAgICAgbmFtZTogW10sXG4gICAgICB0eXBlOiBbXSxcbiAgICAgIHZhbHVlOiBbXSxcbiAgICAgIHZhcmlhYmxlc1JlZmVyZW5jZTogW11cbiAgICB9O1xuICB9XG5cbiAgcHJpdmF0ZSBfZmlsdGVyID0gbmV3IFNldDxzdHJpbmc+KCk7XG4gIHByaXZhdGUgX3Njb3BlID0gJyc7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfZGF0YToge1xuICAgIG5hbWU6IHN0cmluZ1tdO1xuICAgIHR5cGU6IHN0cmluZ1tdO1xuICAgIHZhbHVlOiBzdHJpbmdbXTtcbiAgICB2YXJpYWJsZXNSZWZlcmVuY2U6IG51bWJlcltdO1xuICB9ID0ge1xuICAgIG5hbWU6IFtdLFxuICAgIHR5cGU6IFtdLFxuICAgIHZhbHVlOiBbXSxcbiAgICB2YXJpYWJsZXNSZWZlcmVuY2U6IFtdXG4gIH07XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQ3JlYXRlIGEgY29sb3IgcGFsZXR0ZSBlbGVtZW50LlxuICAgKi9cbiAgZnVuY3Rpb24gY3JlYXRlUGFsZXR0ZSgpOiBIVE1MRGl2RWxlbWVudCB7XG4gICAgY29uc3QgZGl2ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgZGl2LmNsYXNzTmFtZSA9ICdqcC1EZWJ1Z2dlclZhcmlhYmxlcy1jb2xvclBhbGV0dGUnO1xuICAgIGRpdi5pbm5lckhUTUwgPSBgXG4gICAgICAgIDxkaXYgY2xhc3M9XCJqcC1tb2Qtdm9pZFwiPjwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzPVwianAtbW9kLWJhY2tncm91bmRcIj48L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImpwLW1vZC1oZWFkZXItYmFja2dyb3VuZFwiPjwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzPVwianAtbW9kLWdyaWQtbGluZVwiPjwvZGl2PlxuICAgICAgICA8ZGl2IGNsYXNzPVwianAtbW9kLWhlYWRlci1ncmlkLWxpbmVcIj48L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImpwLW1vZC1zZWxlY3Rpb25cIj48L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzcz1cImpwLW1vZC10ZXh0XCI+PC9kaXY+XG4gICAgICBgO1xuICAgIHJldHVybiBkaXY7XG4gIH1cblxuICAvKipcbiAgICogQ29tcHV0ZSB0aGUgc3R5bGUgYW5kIHJlbmRlcmVyIGZvciBhIGRhdGEgZ3JpZC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBjb21wdXRlU3R5bGUoKToge1xuICAgIHN0eWxlOiBEYXRhR3JpZC5TdHlsZTtcbiAgICB0ZXh0UmVuZGVyZXI6IFRleHRSZW5kZXJlcjtcbiAgfSB7XG4gICAgY29uc3QgcGFsZXR0ZSA9IGNyZWF0ZVBhbGV0dGUoKTtcbiAgICBkb2N1bWVudC5ib2R5LmFwcGVuZENoaWxkKHBhbGV0dGUpO1xuICAgIGxldCBub2RlOiBIVE1MRGl2RWxlbWVudCB8IG51bGw7XG4gICAgbm9kZSA9IHBhbGV0dGUucXVlcnlTZWxlY3RvcignLmpwLW1vZC12b2lkJyk7XG4gICAgY29uc3Qgdm9pZENvbG9yID0gZ2V0Q29tcHV0ZWRTdHlsZShub2RlISkuY29sb3I7XG4gICAgbm9kZSA9IHBhbGV0dGUucXVlcnlTZWxlY3RvcignLmpwLW1vZC1iYWNrZ3JvdW5kJyk7XG4gICAgY29uc3QgYmFja2dyb3VuZENvbG9yID0gZ2V0Q29tcHV0ZWRTdHlsZShub2RlISkuY29sb3I7XG4gICAgbm9kZSA9IHBhbGV0dGUucXVlcnlTZWxlY3RvcignLmpwLW1vZC1oZWFkZXItYmFja2dyb3VuZCcpO1xuICAgIGNvbnN0IGhlYWRlckJhY2tncm91bmRDb2xvciA9IGdldENvbXB1dGVkU3R5bGUobm9kZSEpLmNvbG9yO1xuICAgIG5vZGUgPSBwYWxldHRlLnF1ZXJ5U2VsZWN0b3IoJy5qcC1tb2QtZ3JpZC1saW5lJyk7XG4gICAgY29uc3QgZ3JpZExpbmVDb2xvciA9IGdldENvbXB1dGVkU3R5bGUobm9kZSEpLmNvbG9yO1xuICAgIG5vZGUgPSBwYWxldHRlLnF1ZXJ5U2VsZWN0b3IoJy5qcC1tb2QtaGVhZGVyLWdyaWQtbGluZScpO1xuICAgIGNvbnN0IGhlYWRlckdyaWRMaW5lQ29sb3IgPSBnZXRDb21wdXRlZFN0eWxlKG5vZGUhKS5jb2xvcjtcbiAgICBub2RlID0gcGFsZXR0ZS5xdWVyeVNlbGVjdG9yKCcuanAtbW9kLXNlbGVjdGlvbicpO1xuICAgIGNvbnN0IHNlbGVjdGlvbkZpbGxDb2xvciA9IGdldENvbXB1dGVkU3R5bGUobm9kZSEpLmNvbG9yO1xuICAgIG5vZGUgPSBwYWxldHRlLnF1ZXJ5U2VsZWN0b3IoJy5qcC1tb2QtdGV4dCcpO1xuICAgIGNvbnN0IHRleHRDb2xvciA9IGdldENvbXB1dGVkU3R5bGUobm9kZSEpLmNvbG9yO1xuICAgIGRvY3VtZW50LmJvZHkucmVtb3ZlQ2hpbGQocGFsZXR0ZSk7XG4gICAgcmV0dXJuIHtcbiAgICAgIHN0eWxlOiB7XG4gICAgICAgIHZvaWRDb2xvcixcbiAgICAgICAgYmFja2dyb3VuZENvbG9yLFxuICAgICAgICBoZWFkZXJCYWNrZ3JvdW5kQ29sb3IsXG4gICAgICAgIGdyaWRMaW5lQ29sb3IsXG4gICAgICAgIGhlYWRlckdyaWRMaW5lQ29sb3IsXG4gICAgICAgIHJvd0JhY2tncm91bmRDb2xvcjogKGk6IG51bWJlcik6IHN0cmluZyA9PlxuICAgICAgICAgIGkgJSAyID09PSAwID8gdm9pZENvbG9yIDogYmFja2dyb3VuZENvbG9yLFxuICAgICAgICBzZWxlY3Rpb25GaWxsQ29sb3JcbiAgICAgIH0sXG4gICAgICB0ZXh0UmVuZGVyZXI6IG5ldyBUZXh0UmVuZGVyZXIoe1xuICAgICAgICBmb250OiAnMTJweCBzYW5zLXNlcmlmJyxcbiAgICAgICAgdGV4dENvbG9yLFxuICAgICAgICBiYWNrZ3JvdW5kQ29sb3I6ICcnLFxuICAgICAgICB2ZXJ0aWNhbEFsaWdubWVudDogJ2NlbnRlcicsXG4gICAgICAgIGhvcml6b250YWxBbGlnbm1lbnQ6ICdsZWZ0J1xuICAgICAgfSlcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgY3VzdG9tIGNsaWNrIGhhbmRsZXIgdG8gaGFuZGxlIGNsaWNrcyBvbiB0aGUgdmFyaWFibGVzIGdyaWQuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgTW91c2VIYW5kbGVyIGV4dGVuZHMgQmFzaWNNb3VzZUhhbmRsZXIge1xuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgdmFyaWFibGVzIGdyaWQgaXMgZG91YmxlIGNsaWNrZWQuXG4gICAgICovXG4gICAgZ2V0IGRvdWJsZUNsaWNrZWQoKTogSVNpZ25hbDx0aGlzLCBEYXRhR3JpZC5IaXRUZXN0UmVzdWx0PiB7XG4gICAgICByZXR1cm4gdGhpcy5fZG91YmxlQ2xpY2tlZDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIHZhcmlhYmxlcyBncmlkIHJlY2VpdmVkIG1vdXNlIGRvd24gb3IgY29udGV4dCBtZW51IGV2ZW50LlxuICAgICAqL1xuICAgIGdldCBzZWxlY3RlZCgpOiBJU2lnbmFsPHRoaXMsIERhdGFHcmlkLkhpdFRlc3RSZXN1bHQ+IHtcbiAgICAgIHJldHVybiB0aGlzLl9zZWxlY3RlZDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgbW91c2UgaGFuZGxlci5cbiAgICAgKi9cbiAgICBkaXNwb3NlKCk6IHZvaWQge1xuICAgICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIFNpZ25hbC5kaXNjb25uZWN0U2VuZGVyKHRoaXMpO1xuXG4gICAgICBzdXBlci5kaXNwb3NlKCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogSGFuZGxlIGEgbW91c2UgZG91YmxlLWNsaWNrIGV2ZW50LlxuICAgICAqXG4gICAgICogQHBhcmFtIGdyaWQgVGhlIGRhdGFncmlkIGNsaWNrZWQuXG4gICAgICogQHBhcmFtIGV2ZW50IFRoZSBtb3VzZSBldmVudC5cbiAgICAgKi9cbiAgICBvbk1vdXNlRG91YmxlQ2xpY2soZ3JpZDogRGF0YUdyaWQsIGV2ZW50OiBNb3VzZUV2ZW50KTogdm9pZCB7XG4gICAgICBjb25zdCBoaXQgPSBncmlkLmhpdFRlc3QoZXZlbnQuY2xpZW50WCwgZXZlbnQuY2xpZW50WSk7XG4gICAgICB0aGlzLl9kb3VibGVDbGlja2VkLmVtaXQoaGl0KTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBIYW5kbGUgdGhlIG1vdXNlIGRvd24gZXZlbnQgZm9yIHRoZSBkYXRhIGdyaWQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gZ3JpZCAtIFRoZSBkYXRhIGdyaWQgb2YgaW50ZXJlc3QuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgbW91c2UgZG93biBldmVudCBvZiBpbnRlcmVzdC5cbiAgICAgKi9cbiAgICBvbk1vdXNlRG93bihncmlkOiBEYXRhR3JpZCwgZXZlbnQ6IE1vdXNlRXZlbnQpOiB2b2lkIHtcbiAgICAgIC8vIFVucGFjayB0aGUgZXZlbnQuXG4gICAgICBsZXQgeyBjbGllbnRYLCBjbGllbnRZIH0gPSBldmVudDtcblxuICAgICAgLy8gSGl0IHRlc3QgdGhlIGdyaWQuXG4gICAgICBsZXQgaGl0ID0gZ3JpZC5oaXRUZXN0KGNsaWVudFgsIGNsaWVudFkpO1xuXG4gICAgICB0aGlzLl9zZWxlY3RlZC5lbWl0KGhpdCk7XG5cbiAgICAgIC8vIFByb3BhZ2F0ZSBldmVudCB0byBMdW1pbm8gRGF0YUdyaWQgQmFzaWNNb3VzZUhhbmRsZXIuXG4gICAgICBzdXBlci5vbk1vdXNlRG93bihncmlkLCBldmVudCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogSGFuZGxlIHRoZSBjb250ZXh0IG1lbnUgZXZlbnQgZm9yIHRoZSBkYXRhIGdyaWQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gZ3JpZCAtIFRoZSBkYXRhIGdyaWQgb2YgaW50ZXJlc3QuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgY29udGV4dCBtZW51IGV2ZW50IG9mIGludGVyZXN0LlxuICAgICAqL1xuICAgIG9uQ29udGV4dE1lbnUoZ3JpZDogRGF0YUdyaWQsIGV2ZW50OiBNb3VzZUV2ZW50KTogdm9pZCB7XG4gICAgICAvLyBVbnBhY2sgdGhlIGV2ZW50LlxuICAgICAgbGV0IHsgY2xpZW50WCwgY2xpZW50WSB9ID0gZXZlbnQ7XG5cbiAgICAgIC8vIEhpdCB0ZXN0IHRoZSBncmlkLlxuICAgICAgbGV0IGhpdCA9IGdyaWQuaGl0VGVzdChjbGllbnRYLCBjbGllbnRZKTtcblxuICAgICAgdGhpcy5fc2VsZWN0ZWQuZW1pdChoaXQpO1xuICAgIH1cblxuICAgIHByaXZhdGUgX2RvdWJsZUNsaWNrZWQgPSBuZXcgU2lnbmFsPHRoaXMsIERhdGFHcmlkLkhpdFRlc3RSZXN1bHQ+KHRoaXMpO1xuICAgIHByaXZhdGUgX3NlbGVjdGVkID0gbmV3IFNpZ25hbDx0aGlzLCBEYXRhR3JpZC5IaXRUZXN0UmVzdWx0Pih0aGlzKTtcbiAgfVxufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9