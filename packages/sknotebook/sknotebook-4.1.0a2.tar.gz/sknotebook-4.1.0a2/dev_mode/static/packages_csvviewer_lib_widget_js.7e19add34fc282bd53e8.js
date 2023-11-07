"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_csvviewer_lib_widget_js"],{

/***/ "../packages/csvviewer/lib/toolbar.js":
/*!********************************************!*\
  !*** ../packages/csvviewer/lib/toolbar.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CSVDelimiter": () => (/* binding */ CSVDelimiter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to a csv toolbar widget.
 */
const CSV_DELIMITER_CLASS = 'jp-CSVDelimiter';
const CSV_DELIMITER_LABEL_CLASS = 'jp-CSVDelimiter-label';
/**
 * The class name added to a csv toolbar's dropdown element.
 */
const CSV_DELIMITER_DROPDOWN_CLASS = 'jp-CSVDelimiter-dropdown';
/**
 * A widget for selecting a delimiter.
 */
class CSVDelimiter extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Construct a new csv table widget.
     */
    constructor(options) {
        super({
            node: Private.createNode(options.widget.delimiter, options.translator)
        });
        this._widget = options.widget;
        this.addClass(CSV_DELIMITER_CLASS);
    }
    /**
     * The delimiter dropdown menu.
     */
    get selectNode() {
        return this.node.getElementsByTagName('select')[0];
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'change':
                this._widget.delimiter = this.selectNode.value;
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        this.selectNode.addEventListener('change', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        this.selectNode.removeEventListener('change', this);
    }
}
/**
 * A namespace for private toolbar methods.
 */
var Private;
(function (Private) {
    /**
     * Create the node for the delimiter switcher.
     */
    function createNode(selected, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        const trans = translator === null || translator === void 0 ? void 0 : translator.load('jupyterlab');
        // The supported parsing delimiters and labels.
        const delimiters = [
            [',', ','],
            [';', ';'],
            ['\t', trans.__('tab')],
            ['|', trans.__('pipe')],
            ['#', trans.__('hash')]
        ];
        const div = document.createElement('div');
        const label = document.createElement('span');
        const select = document.createElement('select');
        label.textContent = trans.__('Delimiter: ');
        label.className = CSV_DELIMITER_LABEL_CLASS;
        for (const [delimiter, label] of delimiters) {
            const option = document.createElement('option');
            option.value = delimiter;
            option.textContent = label;
            if (delimiter === selected) {
                option.selected = true;
            }
            select.appendChild(option);
        }
        div.appendChild(label);
        const node = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.Styling.wrapSelect(select);
        node.classList.add(CSV_DELIMITER_DROPDOWN_CLASS);
        div.appendChild(node);
        return div;
    }
    Private.createNode = createNode;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/csvviewer/lib/widget.js":
/*!*******************************************!*\
  !*** ../packages/csvviewer/lib/widget.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CSVDocumentWidget": () => (/* binding */ CSVDocumentWidget),
/* harmony export */   "CSVViewer": () => (/* binding */ CSVViewer),
/* harmony export */   "CSVViewerFactory": () => (/* binding */ CSVViewerFactory),
/* harmony export */   "GridSearchService": () => (/* binding */ GridSearchService),
/* harmony export */   "TSVViewerFactory": () => (/* binding */ TSVViewerFactory),
/* harmony export */   "TextRenderConfig": () => (/* binding */ TextRenderConfig)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _toolbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./toolbar */ "../packages/csvviewer/lib/toolbar.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The class name added to a CSV viewer.
 */
const CSV_CLASS = 'jp-CSVViewer';
/**
 * The class name added to a CSV viewer datagrid.
 */
const CSV_GRID_CLASS = 'jp-CSVViewer-grid';
/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
const RENDER_TIMEOUT = 1000;
/**
 * Configuration for cells textrenderer.
 */
class TextRenderConfig {
}
/**
 * Search service remembers the search state and the location of the last
 * match, for incremental searching.
 * Search service is also responsible of providing a cell renderer function
 * to set the background color of cells matching the search text.
 */
class GridSearchService {
    constructor(grid) {
        this._looping = true;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._grid = grid;
        this._query = null;
        this._row = 0;
        this._column = -1;
    }
    /**
     * A signal fired when the grid changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Returns a cellrenderer config function to render each cell background.
     * If cell match, background is matchBackgroundColor, if it's the current
     * match, background is currentMatchBackgroundColor.
     */
    cellBackgroundColorRendererFunc(config) {
        return ({ value, row, column }) => {
            if (this._query) {
                if (value.match(this._query)) {
                    if (this._row === row && this._column === column) {
                        return config.currentMatchBackgroundColor;
                    }
                    return config.matchBackgroundColor;
                }
            }
            return '';
        };
    }
    /**
     * Clear the search.
     */
    clear() {
        this._query = null;
        this._row = 0;
        this._column = -1;
        this._changed.emit(undefined);
    }
    /**
     * incrementally look for searchText.
     */
    find(query, reverse = false) {
        const model = this._grid.dataModel;
        const rowCount = model.rowCount('body');
        const columnCount = model.columnCount('body');
        if (this._query !== query) {
            // reset search
            this._row = 0;
            this._column = -1;
        }
        this._query = query;
        // check if the match is in current viewport
        const minRow = this._grid.scrollY / this._grid.defaultSizes.rowHeight;
        const maxRow = (this._grid.scrollY + this._grid.pageHeight) /
            this._grid.defaultSizes.rowHeight;
        const minColumn = this._grid.scrollX / this._grid.defaultSizes.columnHeaderHeight;
        const maxColumn = (this._grid.scrollX + this._grid.pageWidth) /
            this._grid.defaultSizes.columnHeaderHeight;
        const isInViewport = (row, column) => {
            return (row >= minRow &&
                row <= maxRow &&
                column >= minColumn &&
                column <= maxColumn);
        };
        const increment = reverse ? -1 : 1;
        this._column += increment;
        for (let row = this._row; reverse ? row >= 0 : row < rowCount; row += increment) {
            for (let col = this._column; reverse ? col >= 0 : col < columnCount; col += increment) {
                const cellData = model.data('body', row, col);
                if (cellData.match(query)) {
                    // to update the background of matching cells.
                    // TODO: we only really need to invalidate the previous and current
                    // cell rects, not the entire grid.
                    this._changed.emit(undefined);
                    if (!isInViewport(row, col)) {
                        this._grid.scrollToRow(row);
                    }
                    this._row = row;
                    this._column = col;
                    return true;
                }
            }
            this._column = reverse ? columnCount - 1 : 0;
        }
        // We've finished searching all the way to the limits of the grid. If this
        // is the first time through (looping is true), wrap the indices and search
        // again. Otherwise, give up.
        if (this._looping) {
            this._looping = false;
            this._row = reverse ? 0 : rowCount - 1;
            this._wrapRows(reverse);
            try {
                return this.find(query, reverse);
            }
            finally {
                this._looping = true;
            }
        }
        return false;
    }
    /**
     * Wrap indices if needed to just before the start or just after the end.
     */
    _wrapRows(reverse = false) {
        const model = this._grid.dataModel;
        const rowCount = model.rowCount('body');
        const columnCount = model.columnCount('body');
        if (reverse && this._row <= 0) {
            // if we are at the front, wrap to just past the end.
            this._row = rowCount - 1;
            this._column = columnCount;
        }
        else if (!reverse && this._row >= rowCount - 1) {
            // if we are at the end, wrap to just before the front.
            this._row = 0;
            this._column = -1;
        }
    }
    get query() {
        return this._query;
    }
}
/**
 * A viewer for CSV tables.
 */
class CSVViewer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new CSV viewer.
     */
    constructor(options) {
        super();
        this._monitor = null;
        this._delimiter = ',';
        this._revealed = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
        this._baseRenderer = null;
        this._context = options.context;
        this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.PanelLayout();
        this.addClass(CSV_CLASS);
        this._ready = this.initialize();
    }
    /**
     * Promise which resolves when the content is ready.
     */
    get ready() {
        return this._ready;
    }
    async initialize() {
        const layout = this.layout;
        if (this.isDisposed || !layout) {
            return;
        }
        const { BasicKeyHandler, BasicMouseHandler, DataGrid } = await Private.ensureDataGrid();
        this._defaultStyle = DataGrid.defaultStyle;
        this._grid = new DataGrid({
            defaultSizes: {
                rowHeight: 24,
                columnWidth: 144,
                rowHeaderWidth: 64,
                columnHeaderHeight: 36
            }
        });
        this._grid.addClass(CSV_GRID_CLASS);
        this._grid.headerVisibility = 'all';
        this._grid.keyHandler = new BasicKeyHandler();
        this._grid.mouseHandler = new BasicMouseHandler();
        this._grid.copyConfig = {
            separator: '\t',
            format: DataGrid.copyFormatGeneric,
            headers: 'all',
            warningThreshold: 1e6
        };
        layout.addWidget(this._grid);
        this._searchService = new GridSearchService(this._grid);
        this._searchService.changed.connect(this._updateRenderer, this);
        await this._context.ready;
        await this._updateGrid();
        this._revealed.resolve(undefined);
        // Throttle the rendering rate of the widget.
        this._monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.ActivityMonitor({
            signal: this._context.model.contentChanged,
            timeout: RENDER_TIMEOUT
        });
        this._monitor.activityStopped.connect(this._updateGrid, this);
    }
    /**
     * The CSV widget's context.
     */
    get context() {
        return this._context;
    }
    /**
     * A promise that resolves when the csv viewer is ready to be revealed.
     */
    get revealed() {
        return this._revealed.promise;
    }
    /**
     * The delimiter for the file.
     */
    get delimiter() {
        return this._delimiter;
    }
    set delimiter(value) {
        if (value === this._delimiter) {
            return;
        }
        this._delimiter = value;
        void this._updateGrid();
    }
    /**
     * The style used by the data grid.
     */
    get style() {
        return this._grid.style;
    }
    set style(value) {
        this._grid.style = { ...this._defaultStyle, ...value };
    }
    /**
     * The config used to create text renderer.
     */
    set rendererConfig(rendererConfig) {
        this._baseRenderer = rendererConfig;
        void this._updateRenderer();
    }
    /**
     * The search service
     */
    get searchService() {
        return this._searchService;
    }
    /**
     * Dispose of the resources used by the widget.
     */
    dispose() {
        if (this._monitor) {
            this._monitor.dispose();
        }
        super.dispose();
    }
    /**
     * Go to line
     */
    goToLine(lineNumber) {
        this._grid.scrollToRow(lineNumber);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.tabIndex = -1;
        this.node.focus();
    }
    /**
     * Create the model for the grid.
     */
    async _updateGrid() {
        const { BasicSelectionModel } = await Private.ensureDataGrid();
        const { DSVModel } = await Private.ensureDSVModel();
        const data = this._context.model.toString();
        const delimiter = this._delimiter;
        const oldModel = this._grid.dataModel;
        const dataModel = (this._grid.dataModel = new DSVModel({
            data,
            delimiter
        }));
        this._grid.selectionModel = new BasicSelectionModel({ dataModel });
        if (oldModel) {
            oldModel.dispose();
        }
    }
    /**
     * Update the renderer for the grid.
     */
    async _updateRenderer() {
        if (this._baseRenderer === null) {
            return;
        }
        const { TextRenderer } = await Private.ensureDataGrid();
        const rendererConfig = this._baseRenderer;
        const renderer = new TextRenderer({
            textColor: rendererConfig.textColor,
            horizontalAlignment: rendererConfig.horizontalAlignment,
            backgroundColor: this._searchService.cellBackgroundColorRendererFunc(rendererConfig)
        });
        this._grid.cellRenderers.update({
            body: renderer,
            'column-header': renderer,
            'corner-header': renderer,
            'row-header': renderer
        });
    }
}
/**
 * A document widget for CSV content widgets.
 */
class CSVDocumentWidget extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget {
    constructor(options) {
        let { content, context, delimiter, reveal, ...other } = options;
        content = content || Private.createContent(context);
        reveal = Promise.all([reveal, content.revealed]);
        super({ content, context, reveal, ...other });
        if (delimiter) {
            content.delimiter = delimiter;
        }
    }
    /**
     * Set URI fragment identifier for rows
     */
    setFragment(fragment) {
        const parseFragments = fragment.split('=');
        // TODO: expand to allow columns and cells to be selected
        // reference: https://tools.ietf.org/html/rfc7111#section-3
        if (parseFragments[0] !== '#row') {
            return;
        }
        // multiple rows, separated by semi-colons can be provided, we will just
        // go to the top one
        let topRow = parseFragments[1].split(';')[0];
        // a range of rows can be provided, we will take the first value
        topRow = topRow.split('-')[0];
        // go to that row
        void this.context.ready.then(() => {
            this.content.goToLine(Number(topRow));
        });
    }
}
/**
 * A widget factory for CSV widgets.
 */
class CSVViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const translator = this.translator;
        return new CSVDocumentWidget({ context, translator });
    }
    /**
     * Default factory for toolbar items to be added after the widget is created.
     */
    defaultToolbarFactory(widget) {
        return [
            {
                name: 'delimiter',
                widget: new _toolbar__WEBPACK_IMPORTED_MODULE_5__.CSVDelimiter({
                    widget: widget.content,
                    translator: this.translator
                })
            }
        ];
    }
}
/**
 * A widget factory for TSV widgets.
 */
class TSVViewerFactory extends CSVViewerFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const delimiter = '\t';
        return new CSVDocumentWidget({
            context,
            delimiter,
            translator: this.translator
        });
    }
}
var Private;
(function (Private) {
    let gridLoaded = null;
    let modelLoaded = null;
    /**
     * Lazily load the datagrid module when the first grid is requested.
     */
    async function ensureDataGrid() {
        if (gridLoaded == null) {
            gridLoaded = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
            gridLoaded.resolve(await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_lumino_datagrid_lumino_datagrid").then(__webpack_require__.t.bind(__webpack_require__, /*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid/@lumino/datagrid", 23)));
        }
        return gridLoaded.promise;
    }
    Private.ensureDataGrid = ensureDataGrid;
    async function ensureDSVModel() {
        if (modelLoaded == null) {
            modelLoaded = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
            modelLoaded.resolve(await Promise.all(/*! import() */[__webpack_require__.e("webpack_sharing_consume_default_lumino_datagrid_lumino_datagrid"), __webpack_require__.e("packages_csvviewer_lib_model_js")]).then(__webpack_require__.bind(__webpack_require__, /*! ./model */ "../packages/csvviewer/lib/model.js")));
        }
        return modelLoaded.promise;
    }
    Private.ensureDSVModel = ensureDSVModel;
    function createContent(context) {
        return new CSVViewer({ context });
    }
    Private.createContent = createContent;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY3N2dmlld2VyX2xpYl93aWRnZXRfanMuN2UxOWFkZDM0ZmMyODJiZDUzZTguanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFVztBQUNsQjtBQUVYO0FBR3pDOztHQUVHO0FBQ0gsTUFBTSxtQkFBbUIsR0FBRyxpQkFBaUIsQ0FBQztBQUU5QyxNQUFNLHlCQUF5QixHQUFHLHVCQUF1QixDQUFDO0FBRTFEOztHQUVHO0FBQ0gsTUFBTSw0QkFBNEIsR0FBRywwQkFBMEIsQ0FBQztBQUVoRTs7R0FFRztBQUNJLE1BQU0sWUFBYSxTQUFRLG1EQUFNO0lBQ3RDOztPQUVHO0lBQ0gsWUFBWSxPQUE0QjtRQUN0QyxLQUFLLENBQUM7WUFDSixJQUFJLEVBQUUsT0FBTyxDQUFDLFVBQVUsQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLFNBQVMsRUFBRSxPQUFPLENBQUMsVUFBVSxDQUFDO1NBQ3ZFLENBQUMsQ0FBQztRQUNILElBQUksQ0FBQyxPQUFPLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQztRQUM5QixJQUFJLENBQUMsUUFBUSxDQUFDLG1CQUFtQixDQUFDLENBQUM7SUFDckMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxVQUFVO1FBQ1osT0FBTyxJQUFJLENBQUMsSUFBSSxDQUFDLG9CQUFvQixDQUFDLFFBQVEsQ0FBRSxDQUFDLENBQUMsQ0FBQyxDQUFDO0lBQ3RELENBQUM7SUFFRDs7Ozs7Ozs7O09BU0c7SUFDSCxXQUFXLENBQUMsS0FBWTtRQUN0QixRQUFRLEtBQUssQ0FBQyxJQUFJLEVBQUU7WUFDbEIsS0FBSyxRQUFRO2dCQUNYLElBQUksQ0FBQyxPQUFPLENBQUMsU0FBUyxHQUFHLElBQUksQ0FBQyxVQUFVLENBQUMsS0FBSyxDQUFDO2dCQUMvQyxNQUFNO1lBQ1I7Z0JBQ0UsTUFBTTtTQUNUO0lBQ0gsQ0FBQztJQUVEOztPQUVHO0lBQ08sYUFBYSxDQUFDLEdBQVk7UUFDbEMs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SUFDN0IsQ0FBQztJQU5xQixzQkFBYyxpQkFNbkM7SUFFRCxTQUFnQixhQUFhLENBQzNCLE9BQTJEO1FBRTNELE9BQU8sSUFBSSxTQUFTLENBQUMsRUFBRSxPQUFPLEVBQUUsQ0FBQyxDQUFDO0lBQ3BDLENBQUM7SUFKZSxxQkFBYSxnQkFJNUI7QUFDSCxDQUFDLEVBNUJTLE9BQU8sS0FBUCxPQUFPLFFBNEJoQiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jc3Z2aWV3ZXIvc3JjL3Rvb2xiYXIudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NzdnZpZXdlci9zcmMvd2lkZ2V0LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgU3R5bGluZyB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgdHlwZSB7IENTVlZpZXdlciB9IGZyb20gJy4vd2lkZ2V0JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIGNzdiB0b29sYmFyIHdpZGdldC5cbiAqL1xuY29uc3QgQ1NWX0RFTElNSVRFUl9DTEFTUyA9ICdqcC1DU1ZEZWxpbWl0ZXInO1xuXG5jb25zdCBDU1ZfREVMSU1JVEVSX0xBQkVMX0NMQVNTID0gJ2pwLUNTVkRlbGltaXRlci1sYWJlbCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYSBjc3YgdG9vbGJhcidzIGRyb3Bkb3duIGVsZW1lbnQuXG4gKi9cbmNvbnN0IENTVl9ERUxJTUlURVJfRFJPUERPV05fQ0xBU1MgPSAnanAtQ1NWRGVsaW1pdGVyLWRyb3Bkb3duJztcblxuLyoqXG4gKiBBIHdpZGdldCBmb3Igc2VsZWN0aW5nIGEgZGVsaW1pdGVyLlxuICovXG5leHBvcnQgY2xhc3MgQ1NWRGVsaW1pdGVyIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBjc3YgdGFibGUgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogQ1NWVG9vbGJhci5JT3B0aW9ucykge1xuICAgIHN1cGVyKHtcbiAgICAgIG5vZGU6IFByaXZhdGUuY3JlYXRlTm9kZShvcHRpb25zLndpZGdldC5kZWxpbWl0ZXIsIG9wdGlvbnMudHJhbnNsYXRvcilcbiAgICB9KTtcbiAgICB0aGlzLl93aWRnZXQgPSBvcHRpb25zLndpZGdldDtcbiAgICB0aGlzLmFkZENsYXNzKENTVl9ERUxJTUlURVJfQ0xBU1MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkZWxpbWl0ZXIgZHJvcGRvd24gbWVudS5cbiAgICovXG4gIGdldCBzZWxlY3ROb2RlKCk6IEhUTUxTZWxlY3RFbGVtZW50IHtcbiAgICByZXR1cm4gdGhpcy5ub2RlLmdldEVsZW1lbnRzQnlUYWdOYW1lKCdzZWxlY3QnKSFbMF07XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICogY2FsbGVkIGluIHJlc3BvbnNlIHRvIGV2ZW50cyBvbiB0aGUgZG9jayBwYW5lbCdzIG5vZGUuIEl0IHNob3VsZFxuICAgKiBub3QgYmUgY2FsbGVkIGRpcmVjdGx5IGJ5IHVzZXIgY29kZS5cbiAgICovXG4gIGhhbmRsZUV2ZW50KGV2ZW50OiBFdmVudCk6IHZvaWQge1xuICAgIHN3aXRjaCAoZXZlbnQudHlwZSkge1xuICAgICAgY2FzZSAnY2hhbmdlJzpcbiAgICAgICAgdGhpcy5fd2lkZ2V0LmRlbGltaXRlciA9IHRoaXMuc2VsZWN0Tm9kZS52YWx1ZTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5zZWxlY3ROb2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2NoYW5nZScsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5zZWxlY3ROb2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NoYW5nZScsIHRoaXMpO1xuICB9XG5cbiAgcHJvdGVjdGVkIF93aWRnZXQ6IENTVlZpZXdlcjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYENTVlRvb2xiYXJgIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQ1NWVG9vbGJhciB7XG4gIC8qKlxuICAgKiBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhIENTViB0b29sYmFyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogRG9jdW1lbnQgd2lkZ2V0IGZvciB0aGlzIHRvb2xiYXJcbiAgICAgKi9cbiAgICB3aWRnZXQ6IENTVlZpZXdlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIHRvb2xiYXIgbWV0aG9kcy5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQ3JlYXRlIHRoZSBub2RlIGZvciB0aGUgZGVsaW1pdGVyIHN3aXRjaGVyLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZU5vZGUoXG4gICAgc2VsZWN0ZWQ6IHN0cmluZyxcbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3JcbiAgKTogSFRNTEVsZW1lbnQge1xuICAgIHRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvcj8ubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgLy8gVGhlIHN1cHBvcnRlZCBwYXJzaW5nIGRlbGltaXRlcnMgYW5kIGxhYmVscy5cbiAgICBjb25zdCBkZWxpbWl0ZXJzID0gW1xuICAgICAgWycsJywgJywnXSxcbiAgICAgIFsnOycsICc7J10sXG4gICAgICBbJ1xcdCcsIHRyYW5zLl9fKCd0YWInKV0sXG4gICAgICBbJ3wnLCB0cmFucy5fXygncGlwZScpXSxcbiAgICAgIFsnIycsIHRyYW5zLl9fKCdoYXNoJyldXG4gICAgXTtcblxuICAgIGNvbnN0IGRpdiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIGNvbnN0IGxhYmVsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc3BhbicpO1xuICAgIGNvbnN0IHNlbGVjdCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ3NlbGVjdCcpO1xuICAgIGxhYmVsLnRleHRDb250ZW50ID0gdHJhbnMuX18oJ0RlbGltaXRlcjogJyk7XG4gICAgbGFiZWwuY2xhc3NOYW1lID0gQ1NWX0RFTElNSVRFUl9MQUJFTF9DTEFTUztcbiAgICBmb3IgKGNvbnN0IFtkZWxpbWl0ZXIsIGxhYmVsXSBvZiBkZWxpbWl0ZXJzKSB7XG4gICAgICBjb25zdCBvcHRpb24gPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdvcHRpb24nKTtcbiAgICAgIG9wdGlvbi52YWx1ZSA9IGRlbGltaXRlcjtcbiAgICAgIG9wdGlvbi50ZXh0Q29udGVudCA9IGxhYmVsO1xuICAgICAgaWYgKGRlbGltaXRlciA9PT0gc2VsZWN0ZWQpIHtcbiAgICAgICAgb3B0aW9uLnNlbGVjdGVkID0gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIHNlbGVjdC5hcHBlbmRDaGlsZChvcHRpb24pO1xuICAgIH1cbiAgICBkaXYuYXBwZW5kQ2hpbGQobGFiZWwpO1xuICAgIGNvbnN0IG5vZGUgPSBTdHlsaW5nLndyYXBTZWxlY3Qoc2VsZWN0KTtcbiAgICBub2RlLmNsYXNzTGlzdC5hZGQoQ1NWX0RFTElNSVRFUl9EUk9QRE9XTl9DTEFTUyk7XG4gICAgZGl2LmFwcGVuZENoaWxkKG5vZGUpO1xuICAgIHJldHVybiBkaXY7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgQWN0aXZpdHlNb25pdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIEFCQ1dpZGdldEZhY3RvcnksXG4gIERvY3VtZW50UmVnaXN0cnksXG4gIERvY3VtZW50V2lkZ2V0LFxuICBJRG9jdW1lbnRXaWRnZXRcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHR5cGUgKiBhcyBEYXRhR3JpZE1vZHVsZSBmcm9tICdAbHVtaW5vL2RhdGFncmlkJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBQYW5lbExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB0eXBlICogYXMgRFNWTW9kZWxNb2R1bGUgZnJvbSAnLi9tb2RlbCc7XG5pbXBvcnQgeyBDU1ZEZWxpbWl0ZXIgfSBmcm9tICcuL3Rvb2xiYXInO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgQ1NWIHZpZXdlci5cbiAqL1xuY29uc3QgQ1NWX0NMQVNTID0gJ2pwLUNTVlZpZXdlcic7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYSBDU1Ygdmlld2VyIGRhdGFncmlkLlxuICovXG5jb25zdCBDU1ZfR1JJRF9DTEFTUyA9ICdqcC1DU1ZWaWV3ZXItZ3JpZCc7XG5cbi8qKlxuICogVGhlIHRpbWVvdXQgdG8gd2FpdCBmb3IgY2hhbmdlIGFjdGl2aXR5IHRvIGhhdmUgY2Vhc2VkIGJlZm9yZSByZW5kZXJpbmcuXG4gKi9cbmNvbnN0IFJFTkRFUl9USU1FT1VUID0gMTAwMDtcblxuLyoqXG4gKiBDb25maWd1cmF0aW9uIGZvciBjZWxscyB0ZXh0cmVuZGVyZXIuXG4gKi9cbmV4cG9ydCBjbGFzcyBUZXh0UmVuZGVyQ29uZmlnIHtcbiAgLyoqXG4gICAqIGRlZmF1bHQgdGV4dCBjb2xvclxuICAgKi9cbiAgdGV4dENvbG9yOiBzdHJpbmc7XG4gIC8qKlxuICAgKiBiYWNrZ3JvdW5kIGNvbG9yIGZvciBhIHNlYXJjaCBtYXRjaFxuICAgKi9cbiAgbWF0Y2hCYWNrZ3JvdW5kQ29sb3I6IHN0cmluZztcbiAgLyoqXG4gICAqIGJhY2tncm91bmQgY29sb3IgZm9yIHRoZSBjdXJyZW50IHNlYXJjaCBtYXRjaC5cbiAgICovXG4gIGN1cnJlbnRNYXRjaEJhY2tncm91bmRDb2xvcjogc3RyaW5nO1xuICAvKipcbiAgICogaG9yaXpvbnRhbEFsaWdubWVudCBvZiB0aGUgdGV4dFxuICAgKi9cbiAgaG9yaXpvbnRhbEFsaWdubWVudDogRGF0YUdyaWRNb2R1bGUuVGV4dFJlbmRlcmVyLkhvcml6b250YWxBbGlnbm1lbnQ7XG59XG5cbi8qKlxuICogU2VhcmNoIHNlcnZpY2UgcmVtZW1iZXJzIHRoZSBzZWFyY2ggc3RhdGUgYW5kIHRoZSBsb2NhdGlvbiBvZiB0aGUgbGFzdFxuICogbWF0Y2gsIGZvciBpbmNyZW1lbnRhbCBzZWFyY2hpbmcuXG4gKiBTZWFyY2ggc2VydmljZSBpcyBhbHNvIHJlc3BvbnNpYmxlIG9mIHByb3ZpZGluZyBhIGNlbGwgcmVuZGVyZXIgZnVuY3Rpb25cbiAqIHRvIHNldCB0aGUgYmFja2dyb3VuZCBjb2xvciBvZiBjZWxscyBtYXRjaGluZyB0aGUgc2VhcmNoIHRleHQuXG4gKi9cbmV4cG9ydCBjbGFzcyBHcmlkU2VhcmNoU2VydmljZSB7XG4gIGNvbnN0cnVjdG9yKGdyaWQ6IERhdGFHcmlkTW9kdWxlLkRhdGFHcmlkKSB7XG4gICAgdGhpcy5fZ3JpZCA9IGdyaWQ7XG4gICAgdGhpcy5fcXVlcnkgPSBudWxsO1xuICAgIHRoaXMuX3JvdyA9IDA7XG4gICAgdGhpcy5fY29sdW1uID0gLTE7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZmlyZWQgd2hlbiB0aGUgZ3JpZCBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IGNoYW5nZWQoKTogSVNpZ25hbDxHcmlkU2VhcmNoU2VydmljZSwgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybnMgYSBjZWxscmVuZGVyZXIgY29uZmlnIGZ1bmN0aW9uIHRvIHJlbmRlciBlYWNoIGNlbGwgYmFja2dyb3VuZC5cbiAgICogSWYgY2VsbCBtYXRjaCwgYmFja2dyb3VuZCBpcyBtYXRjaEJhY2tncm91bmRDb2xvciwgaWYgaXQncyB0aGUgY3VycmVudFxuICAgKiBtYXRjaCwgYmFja2dyb3VuZCBpcyBjdXJyZW50TWF0Y2hCYWNrZ3JvdW5kQ29sb3IuXG4gICAqL1xuICBjZWxsQmFja2dyb3VuZENvbG9yUmVuZGVyZXJGdW5jKFxuICAgIGNvbmZpZzogVGV4dFJlbmRlckNvbmZpZ1xuICApOiBEYXRhR3JpZE1vZHVsZS5DZWxsUmVuZGVyZXIuQ29uZmlnRnVuYzxzdHJpbmc+IHtcbiAgICByZXR1cm4gKHsgdmFsdWUsIHJvdywgY29sdW1uIH0pID0+IHtcbiAgICAgIGlmICh0aGlzLl9xdWVyeSkge1xuICAgICAgICBpZiAoKHZhbHVlIGFzIHN0cmluZykubWF0Y2godGhpcy5fcXVlcnkpKSB7XG4gICAgICAgICAgaWYgKHRoaXMuX3JvdyA9PT0gcm93ICYmIHRoaXMuX2NvbHVtbiA9PT0gY29sdW1uKSB7XG4gICAgICAgICAgICByZXR1cm4gY29uZmlnLmN1cnJlbnRNYXRjaEJhY2tncm91bmRDb2xvcjtcbiAgICAgICAgICB9XG4gICAgICAgICAgcmV0dXJuIGNvbmZpZy5tYXRjaEJhY2tncm91bmRDb2xvcjtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgcmV0dXJuICcnO1xuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogQ2xlYXIgdGhlIHNlYXJjaC5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQge1xuICAgIHRoaXMuX3F1ZXJ5ID0gbnVsbDtcbiAgICB0aGlzLl9yb3cgPSAwO1xuICAgIHRoaXMuX2NvbHVtbiA9IC0xO1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh1bmRlZmluZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIGluY3JlbWVudGFsbHkgbG9vayBmb3Igc2VhcmNoVGV4dC5cbiAgICovXG4gIGZpbmQocXVlcnk6IFJlZ0V4cCwgcmV2ZXJzZSA9IGZhbHNlKTogYm9vbGVhbiB7XG4gICAgY29uc3QgbW9kZWwgPSB0aGlzLl9ncmlkLmRhdGFNb2RlbCE7XG4gICAgY29uc3Qgcm93Q291bnQgPSBtb2RlbC5yb3dDb3VudCgnYm9keScpO1xuICAgIGNvbnN0IGNvbHVtbkNvdW50ID0gbW9kZWwuY29sdW1uQ291bnQoJ2JvZHknKTtcblxuICAgIGlmICh0aGlzLl9xdWVyeSAhPT0gcXVlcnkpIHtcbiAgICAgIC8vIHJlc2V0IHNlYXJjaFxuICAgICAgdGhpcy5fcm93ID0gMDtcbiAgICAgIHRoaXMuX2NvbHVtbiA9IC0xO1xuICAgIH1cbiAgICB0aGlzLl9xdWVyeSA9IHF1ZXJ5O1xuXG4gICAgLy8gY2hlY2sgaWYgdGhlIG1hdGNoIGlzIGluIGN1cnJlbnQgdmlld3BvcnRcblxuICAgIGNvbnN0IG1pblJvdyA9IHRoaXMuX2dyaWQuc2Nyb2xsWSAvIHRoaXMuX2dyaWQuZGVmYXVsdFNpemVzLnJvd0hlaWdodDtcbiAgICBjb25zdCBtYXhSb3cgPVxuICAgICAgKHRoaXMuX2dyaWQuc2Nyb2xsWSArIHRoaXMuX2dyaWQucGFnZUhlaWdodCkgL1xuICAgICAgdGhpcy5fZ3JpZC5kZWZhdWx0U2l6ZXMucm93SGVpZ2h0O1xuICAgIGNvbnN0IG1pbkNvbHVtbiA9XG4gICAgICB0aGlzLl9ncmlkLnNjcm9sbFggLyB0aGlzLl9ncmlkLmRlZmF1bHRTaXplcy5jb2x1bW5IZWFkZXJIZWlnaHQ7XG4gICAgY29uc3QgbWF4Q29sdW1uID1cbiAgICAgICh0aGlzLl9ncmlkLnNjcm9sbFggKyB0aGlzLl9ncmlkLnBhZ2VXaWR0aCkgL1xuICAgICAgdGhpcy5fZ3JpZC5kZWZhdWx0U2l6ZXMuY29sdW1uSGVhZGVySGVpZ2h0O1xuICAgIGNvbnN0IGlzSW5WaWV3cG9ydCA9IChyb3c6IG51bWJlciwgY29sdW1uOiBudW1iZXIpID0+IHtcbiAgICAgIHJldHVybiAoXG4gICAgICAgIHJvdyA+PSBtaW5Sb3cgJiZcbiAgICAgICAgcm93IDw9IG1heFJvdyAmJlxuICAgICAgICBjb2x1bW4gPj0gbWluQ29sdW1uICYmXG4gICAgICAgIGNvbHVtbiA8PSBtYXhDb2x1bW5cbiAgICAgICk7XG4gICAgfTtcblxuICAgIGNvbnN0IGluY3JlbWVudCA9IHJldmVyc2UgPyAtMSA6IDE7XG4gICAgdGhpcy5fY29sdW1uICs9IGluY3JlbWVudDtcbiAgICBmb3IgKFxuICAgICAgbGV0IHJvdyA9IHRoaXMuX3JvdztcbiAgICAgIHJldmVyc2UgPyByb3cgPj0gMCA6IHJvdyA8IHJvd0NvdW50O1xuICAgICAgcm93ICs9IGluY3JlbWVudFxuICAgICkge1xuICAgICAgZm9yIChcbiAgICAgICAgbGV0IGNvbCA9IHRoaXMuX2NvbHVtbjtcbiAgICAgICAgcmV2ZXJzZSA/IGNvbCA+PSAwIDogY29sIDwgY29sdW1uQ291bnQ7XG4gICAgICAgIGNvbCArPSBpbmNyZW1lbnRcbiAgICAgICkge1xuICAgICAgICBjb25zdCBjZWxsRGF0YSA9IG1vZGVsLmRhdGEoJ2JvZHknLCByb3csIGNvbCkgYXMgc3RyaW5nO1xuICAgICAgICBpZiAoY2VsbERhdGEubWF0Y2gocXVlcnkpKSB7XG4gICAgICAgICAgLy8gdG8gdXBkYXRlIHRoZSBiYWNrZ3JvdW5kIG9mIG1hdGNoaW5nIGNlbGxzLlxuXG4gICAgICAgICAgLy8gVE9ETzogd2Ugb25seSByZWFsbHkgbmVlZCB0byBpbnZhbGlkYXRlIHRoZSBwcmV2aW91cyBhbmQgY3VycmVudFxuICAgICAgICAgIC8vIGNlbGwgcmVjdHMsIG5vdCB0aGUgZW50aXJlIGdyaWQuXG4gICAgICAgICAgdGhpcy5fY2hhbmdlZC5lbWl0KHVuZGVmaW5lZCk7XG5cbiAgICAgICAgICBpZiAoIWlzSW5WaWV3cG9ydChyb3csIGNvbCkpIHtcbiAgICAgICAgICAgIHRoaXMuX2dyaWQuc2Nyb2xsVG9Sb3cocm93KTtcbiAgICAgICAgICB9XG4gICAgICAgICAgdGhpcy5fcm93ID0gcm93O1xuICAgICAgICAgIHRoaXMuX2NvbHVtbiA9IGNvbDtcbiAgICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgdGhpcy5fY29sdW1uID0gcmV2ZXJzZSA/IGNvbHVtbkNvdW50IC0gMSA6IDA7XG4gICAgfVxuICAgIC8vIFdlJ3ZlIGZpbmlzaGVkIHNlYXJjaGluZyBhbGwgdGhlIHdheSB0byB0aGUgbGltaXRzIG9mIHRoZSBncmlkLiBJZiB0aGlzXG4gICAgLy8gaXMgdGhlIGZpcnN0IHRpbWUgdGhyb3VnaCAobG9vcGluZyBpcyB0cnVlKSwgd3JhcCB0aGUgaW5kaWNlcyBhbmQgc2VhcmNoXG4gICAgLy8gYWdhaW4uIE90aGVyd2lzZSwgZ2l2ZSB1cC5cbiAgICBpZiAodGhpcy5fbG9vcGluZykge1xuICAgICAgdGhpcy5fbG9vcGluZyA9IGZhbHNlO1xuICAgICAgdGhpcy5fcm93ID0gcmV2ZXJzZSA/IDAgOiByb3dDb3VudCAtIDE7XG4gICAgICB0aGlzLl93cmFwUm93cyhyZXZlcnNlKTtcbiAgICAgIHRyeSB7XG4gICAgICAgIHJldHVybiB0aGlzLmZpbmQocXVlcnksIHJldmVyc2UpO1xuICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgdGhpcy5fbG9vcGluZyA9IHRydWU7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXcmFwIGluZGljZXMgaWYgbmVlZGVkIHRvIGp1c3QgYmVmb3JlIHRoZSBzdGFydCBvciBqdXN0IGFmdGVyIHRoZSBlbmQuXG4gICAqL1xuICBwcml2YXRlIF93cmFwUm93cyhyZXZlcnNlID0gZmFsc2UpIHtcbiAgICBjb25zdCBtb2RlbCA9IHRoaXMuX2dyaWQuZGF0YU1vZGVsITtcbiAgICBjb25zdCByb3dDb3VudCA9IG1vZGVsLnJvd0NvdW50KCdib2R5Jyk7XG4gICAgY29uc3QgY29sdW1uQ291bnQgPSBtb2RlbC5jb2x1bW5Db3VudCgnYm9keScpO1xuXG4gICAgaWYgKHJldmVyc2UgJiYgdGhpcy5fcm93IDw9IDApIHtcbiAgICAgIC8vIGlmIHdlIGFyZSBhdCB0aGUgZnJvbnQsIHdyYXAgdG8ganVzdCBwYXN0IHRoZSBlbmQuXG4gICAgICB0aGlzLl9yb3cgPSByb3dDb3VudCAtIDE7XG4gICAgICB0aGlzLl9jb2x1bW4gPSBjb2x1bW5Db3VudDtcbiAgICB9IGVsc2UgaWYgKCFyZXZlcnNlICYmIHRoaXMuX3JvdyA+PSByb3dDb3VudCAtIDEpIHtcbiAgICAgIC8vIGlmIHdlIGFyZSBhdCB0aGUgZW5kLCB3cmFwIHRvIGp1c3QgYmVmb3JlIHRoZSBmcm9udC5cbiAgICAgIHRoaXMuX3JvdyA9IDA7XG4gICAgICB0aGlzLl9jb2x1bW4gPSAtMTtcbiAgICB9XG4gIH1cblxuICBnZXQgcXVlcnkoKTogUmVnRXhwIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX3F1ZXJ5O1xuICB9XG5cbiAgcHJpdmF0ZSBfZ3JpZDogRGF0YUdyaWRNb2R1bGUuRGF0YUdyaWQ7XG4gIHByaXZhdGUgX3F1ZXJ5OiBSZWdFeHAgfCBudWxsO1xuICBwcml2YXRlIF9yb3c6IG51bWJlcjtcbiAgcHJpdmF0ZSBfY29sdW1uOiBudW1iZXI7XG4gIHByaXZhdGUgX2xvb3BpbmcgPSB0cnVlO1xuICBwcml2YXRlIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDxHcmlkU2VhcmNoU2VydmljZSwgdm9pZD4odGhpcyk7XG59XG5cbi8qKlxuICogQSB2aWV3ZXIgZm9yIENTViB0YWJsZXMuXG4gKi9cbmV4cG9ydCBjbGFzcyBDU1ZWaWV3ZXIgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IENTViB2aWV3ZXIuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBDU1ZWaWV3ZXIuSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuXG4gICAgdGhpcy5fY29udGV4dCA9IG9wdGlvbnMuY29udGV4dDtcbiAgICB0aGlzLmxheW91dCA9IG5ldyBQYW5lbExheW91dCgpO1xuXG4gICAgdGhpcy5hZGRDbGFzcyhDU1ZfQ0xBU1MpO1xuXG4gICAgdGhpcy5fcmVhZHkgPSB0aGlzLmluaXRpYWxpemUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBQcm9taXNlIHdoaWNoIHJlc29sdmVzIHdoZW4gdGhlIGNvbnRlbnQgaXMgcmVhZHkuXG4gICAqL1xuICBnZXQgcmVhZHkoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3JlYWR5O1xuICB9XG5cbiAgcHJvdGVjdGVkIGFzeW5jIGluaXRpYWxpemUoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgbGF5b3V0ID0gdGhpcy5sYXlvdXQgYXMgUGFuZWxMYXlvdXQ7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCB8fCAhbGF5b3V0KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHsgQmFzaWNLZXlIYW5kbGVyLCBCYXNpY01vdXNlSGFuZGxlciwgRGF0YUdyaWQgfSA9XG4gICAgICBhd2FpdCBQcml2YXRlLmVuc3VyZURhdGFHcmlkKCk7XG4gICAgdGhpcy5fZGVmYXVsdFN0eWxlID0gRGF0YUdyaWQuZGVmYXVsdFN0eWxlO1xuICAgIHRoaXMuX2dyaWQgPSBuZXcgRGF0YUdyaWQoe1xuICAgICAgZGVmYXVsdFNpemVzOiB7XG4gICAgICAgIHJvd0hlaWdodDogMjQsXG4gICAgICAgIGNvbHVtbldpZHRoOiAxNDQsXG4gICAgICAgIHJvd0hlYWRlcldpZHRoOiA2NCxcbiAgICAgICAgY29sdW1uSGVhZGVySGVpZ2h0OiAzNlxuICAgICAgfVxuICAgIH0pO1xuICAgIHRoaXMuX2dyaWQuYWRkQ2xhc3MoQ1NWX0dSSURfQ0xBU1MpO1xuICAgIHRoaXMuX2dyaWQuaGVhZGVyVmlzaWJpbGl0eSA9ICdhbGwnO1xuICAgIHRoaXMuX2dyaWQua2V5SGFuZGxlciA9IG5ldyBCYXNpY0tleUhhbmRsZXIoKTtcbiAgICB0aGlzLl9ncmlkLm1vdXNlSGFuZGxlciA9IG5ldyBCYXNpY01vdXNlSGFuZGxlcigpO1xuICAgIHRoaXMuX2dyaWQuY29weUNvbmZpZyA9IHtcbiAgICAgIHNlcGFyYXRvcjogJ1xcdCcsXG4gICAgICBmb3JtYXQ6IERhdGFHcmlkLmNvcHlGb3JtYXRHZW5lcmljLFxuICAgICAgaGVhZGVyczogJ2FsbCcsXG4gICAgICB3YXJuaW5nVGhyZXNob2xkOiAxZTZcbiAgICB9O1xuXG4gICAgbGF5b3V0LmFkZFdpZGdldCh0aGlzLl9ncmlkKTtcblxuICAgIHRoaXMuX3NlYXJjaFNlcnZpY2UgPSBuZXcgR3JpZFNlYXJjaFNlcnZpY2UodGhpcy5fZ3JpZCk7XG4gICAgdGhpcy5fc2VhcmNoU2VydmljZS5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fdXBkYXRlUmVuZGVyZXIsIHRoaXMpO1xuXG4gICAgYXdhaXQgdGhpcy5fY29udGV4dC5yZWFkeTtcbiAgICBhd2FpdCB0aGlzLl91cGRhdGVHcmlkKCk7XG4gICAgdGhpcy5fcmV2ZWFsZWQucmVzb2x2ZSh1bmRlZmluZWQpO1xuICAgIC8vIFRocm90dGxlIHRoZSByZW5kZXJpbmcgcmF0ZSBvZiB0aGUgd2lkZ2V0LlxuICAgIHRoaXMuX21vbml0b3IgPSBuZXcgQWN0aXZpdHlNb25pdG9yKHtcbiAgICAgIHNpZ25hbDogdGhpcy5fY29udGV4dC5tb2RlbC5jb250ZW50Q2hhbmdlZCxcbiAgICAgIHRpbWVvdXQ6IFJFTkRFUl9USU1FT1VUXG4gICAgfSk7XG4gICAgdGhpcy5fbW9uaXRvci5hY3Rpdml0eVN0b3BwZWQuY29ubmVjdCh0aGlzLl91cGRhdGVHcmlkLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgQ1NWIHdpZGdldCdzIGNvbnRleHQuXG4gICAqL1xuICBnZXQgY29udGV4dCgpOiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQge1xuICAgIHJldHVybiB0aGlzLl9jb250ZXh0O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIGNzdiB2aWV3ZXIgaXMgcmVhZHkgdG8gYmUgcmV2ZWFsZWQuXG4gICAqL1xuICBnZXQgcmV2ZWFsZWQoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3JldmVhbGVkLnByb21pc2U7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlbGltaXRlciBmb3IgdGhlIGZpbGUuXG4gICAqL1xuICBnZXQgZGVsaW1pdGVyKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2RlbGltaXRlcjtcbiAgfVxuICBzZXQgZGVsaW1pdGVyKHZhbHVlOiBzdHJpbmcpIHtcbiAgICBpZiAodmFsdWUgPT09IHRoaXMuX2RlbGltaXRlcikge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9kZWxpbWl0ZXIgPSB2YWx1ZTtcbiAgICB2b2lkIHRoaXMuX3VwZGF0ZUdyaWQoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc3R5bGUgdXNlZCBieSB0aGUgZGF0YSBncmlkLlxuICAgKi9cbiAgZ2V0IHN0eWxlKCk6IERhdGFHcmlkTW9kdWxlLkRhdGFHcmlkLlN0eWxlIHtcbiAgICByZXR1cm4gdGhpcy5fZ3JpZC5zdHlsZTtcbiAgfVxuICBzZXQgc3R5bGUodmFsdWU6IERhdGFHcmlkTW9kdWxlLkRhdGFHcmlkLlN0eWxlKSB7XG4gICAgdGhpcy5fZ3JpZC5zdHlsZSA9IHsgLi4udGhpcy5fZGVmYXVsdFN0eWxlLCAuLi52YWx1ZSB9O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb25maWcgdXNlZCB0byBjcmVhdGUgdGV4dCByZW5kZXJlci5cbiAgICovXG4gIHNldCByZW5kZXJlckNvbmZpZyhyZW5kZXJlckNvbmZpZzogVGV4dFJlbmRlckNvbmZpZykge1xuICAgIHRoaXMuX2Jhc2VSZW5kZXJlciA9IHJlbmRlcmVyQ29uZmlnO1xuICAgIHZvaWQgdGhpcy5fdXBkYXRlUmVuZGVyZXIoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc2VhcmNoIHNlcnZpY2VcbiAgICovXG4gIGdldCBzZWFyY2hTZXJ2aWNlKCk6IEdyaWRTZWFyY2hTZXJ2aWNlIHtcbiAgICByZXR1cm4gdGhpcy5fc2VhcmNoU2VydmljZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgdXNlZCBieSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fbW9uaXRvcikge1xuICAgICAgdGhpcy5fbW9uaXRvci5kaXNwb3NlKCk7XG4gICAgfVxuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHbyB0byBsaW5lXG4gICAqL1xuICBnb1RvTGluZShsaW5lTnVtYmVyOiBudW1iZXIpOiB2b2lkIHtcbiAgICB0aGlzLl9ncmlkLnNjcm9sbFRvUm93KGxpbmVOdW1iZXIpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FjdGl2YXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2YXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLm5vZGUudGFiSW5kZXggPSAtMTtcbiAgICB0aGlzLm5vZGUuZm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgdGhlIG1vZGVsIGZvciB0aGUgZ3JpZC5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3VwZGF0ZUdyaWQoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgeyBCYXNpY1NlbGVjdGlvbk1vZGVsIH0gPSBhd2FpdCBQcml2YXRlLmVuc3VyZURhdGFHcmlkKCk7XG4gICAgY29uc3QgeyBEU1ZNb2RlbCB9ID0gYXdhaXQgUHJpdmF0ZS5lbnN1cmVEU1ZNb2RlbCgpO1xuICAgIGNvbnN0IGRhdGE6IHN0cmluZyA9IHRoaXMuX2NvbnRleHQubW9kZWwudG9TdHJpbmcoKTtcbiAgICBjb25zdCBkZWxpbWl0ZXIgPSB0aGlzLl9kZWxpbWl0ZXI7XG4gICAgY29uc3Qgb2xkTW9kZWwgPSB0aGlzLl9ncmlkLmRhdGFNb2RlbCBhcyBEU1ZNb2RlbE1vZHVsZS5EU1ZNb2RlbDtcbiAgICBjb25zdCBkYXRhTW9kZWwgPSAodGhpcy5fZ3JpZC5kYXRhTW9kZWwgPSBuZXcgRFNWTW9kZWwoe1xuICAgICAgZGF0YSxcbiAgICAgIGRlbGltaXRlclxuICAgIH0pKTtcbiAgICB0aGlzLl9ncmlkLnNlbGVjdGlvbk1vZGVsID0gbmV3IEJhc2ljU2VsZWN0aW9uTW9kZWwoeyBkYXRhTW9kZWwgfSk7XG4gICAgaWYgKG9sZE1vZGVsKSB7XG4gICAgICBvbGRNb2RlbC5kaXNwb3NlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgcmVuZGVyZXIgZm9yIHRoZSBncmlkLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfdXBkYXRlUmVuZGVyZXIoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKHRoaXMuX2Jhc2VSZW5kZXJlciA9PT0gbnVsbCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCB7IFRleHRSZW5kZXJlciB9ID0gYXdhaXQgUHJpdmF0ZS5lbnN1cmVEYXRhR3JpZCgpO1xuICAgIGNvbnN0IHJlbmRlcmVyQ29uZmlnID0gdGhpcy5fYmFzZVJlbmRlcmVyO1xuICAgIGNvbnN0IHJlbmRlcmVyID0gbmV3IFRleHRSZW5kZXJlcih7XG4gICAgICB0ZXh0Q29sb3I6IHJlbmRlcmVyQ29uZmlnLnRleHRDb2xvcixcbiAgICAgIGhvcml6b250YWxBbGlnbm1lbnQ6IHJlbmRlcmVyQ29uZmlnLmhvcml6b250YWxBbGlnbm1lbnQsXG4gICAgICBiYWNrZ3JvdW5kQ29sb3I6XG4gICAgICAgIHRoaXMuX3NlYXJjaFNlcnZpY2UuY2VsbEJhY2tncm91bmRDb2xvclJlbmRlcmVyRnVuYyhyZW5kZXJlckNvbmZpZylcbiAgICB9KTtcbiAgICB0aGlzLl9ncmlkLmNlbGxSZW5kZXJlcnMudXBkYXRlKHtcbiAgICAgIGJvZHk6IHJlbmRlcmVyLFxuICAgICAgJ2NvbHVtbi1oZWFkZXInOiByZW5kZXJlcixcbiAgICAgICdjb3JuZXItaGVhZGVyJzogcmVuZGVyZXIsXG4gICAgICAncm93LWhlYWRlcic6IHJlbmRlcmVyXG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9jb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQ7XG4gIHByaXZhdGUgX2dyaWQ6IERhdGFHcmlkTW9kdWxlLkRhdGFHcmlkO1xuICBwcml2YXRlIF9kZWZhdWx0U3R5bGU6IHR5cGVvZiBEYXRhR3JpZE1vZHVsZS5EYXRhR3JpZC5kZWZhdWx0U3R5bGU7XG4gIHByaXZhdGUgX3NlYXJjaFNlcnZpY2U6IEdyaWRTZWFyY2hTZXJ2aWNlO1xuICBwcml2YXRlIF9tb25pdG9yOiBBY3Rpdml0eU1vbml0b3I8RG9jdW1lbnRSZWdpc3RyeS5JTW9kZWwsIHZvaWQ+IHwgbnVsbCA9XG4gICAgbnVsbDtcbiAgcHJpdmF0ZSBfZGVsaW1pdGVyID0gJywnO1xuICBwcml2YXRlIF9yZXZlYWxlZCA9IG5ldyBQcm9taXNlRGVsZWdhdGU8dm9pZD4oKTtcbiAgcHJpdmF0ZSBfYmFzZVJlbmRlcmVyOiBUZXh0UmVuZGVyQ29uZmlnIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX3JlYWR5OiBQcm9taXNlPHZvaWQ+O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgQ1NWVmlld2VyYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIENTVlZpZXdlciB7XG4gIC8qKlxuICAgKiBJbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIENTViB3aWRnZXRzLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGRvY3VtZW50IGNvbnRleHQgZm9yIHRoZSBDU1YgYmVpbmcgcmVuZGVyZWQgYnkgdGhlIHdpZGdldC5cbiAgICAgKi9cbiAgICBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQ7XG4gIH1cbn1cblxuLyoqXG4gKiBBIGRvY3VtZW50IHdpZGdldCBmb3IgQ1NWIGNvbnRlbnQgd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGNsYXNzIENTVkRvY3VtZW50V2lkZ2V0IGV4dGVuZHMgRG9jdW1lbnRXaWRnZXQ8Q1NWVmlld2VyPiB7XG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IENTVkRvY3VtZW50V2lkZ2V0LklPcHRpb25zKSB7XG4gICAgbGV0IHsgY29udGVudCwgY29udGV4dCwgZGVsaW1pdGVyLCByZXZlYWwsIC4uLm90aGVyIH0gPSBvcHRpb25zO1xuICAgIGNvbnRlbnQgPSBjb250ZW50IHx8IFByaXZhdGUuY3JlYXRlQ29udGVudChjb250ZXh0KTtcbiAgICByZXZlYWwgPSBQcm9taXNlLmFsbChbcmV2ZWFsLCBjb250ZW50LnJldmVhbGVkXSk7XG4gICAgc3VwZXIoeyBjb250ZW50LCBjb250ZXh0LCByZXZlYWwsIC4uLm90aGVyIH0pO1xuXG4gICAgaWYgKGRlbGltaXRlcikge1xuICAgICAgY29udGVudC5kZWxpbWl0ZXIgPSBkZWxpbWl0ZXI7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFNldCBVUkkgZnJhZ21lbnQgaWRlbnRpZmllciBmb3Igcm93c1xuICAgKi9cbiAgc2V0RnJhZ21lbnQoZnJhZ21lbnQ6IHN0cmluZyk6IHZvaWQge1xuICAgIGNvbnN0IHBhcnNlRnJhZ21lbnRzID0gZnJhZ21lbnQuc3BsaXQoJz0nKTtcblxuICAgIC8vIFRPRE86IGV4cGFuZCB0byBhbGxvdyBjb2x1bW5zIGFuZCBjZWxscyB0byBiZSBzZWxlY3RlZFxuICAgIC8vIHJlZmVyZW5jZTogaHR0cHM6Ly90b29scy5pZXRmLm9yZy9odG1sL3JmYzcxMTEjc2VjdGlvbi0zXG4gICAgaWYgKHBhcnNlRnJhZ21lbnRzWzBdICE9PSAnI3JvdycpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBtdWx0aXBsZSByb3dzLCBzZXBhcmF0ZWQgYnkgc2VtaS1jb2xvbnMgY2FuIGJlIHByb3ZpZGVkLCB3ZSB3aWxsIGp1c3RcbiAgICAvLyBnbyB0byB0aGUgdG9wIG9uZVxuICAgIGxldCB0b3BSb3cgPSBwYXJzZUZyYWdtZW50c1sxXS5zcGxpdCgnOycpWzBdO1xuXG4gICAgLy8gYSByYW5nZSBvZiByb3dzIGNhbiBiZSBwcm92aWRlZCwgd2Ugd2lsbCB0YWtlIHRoZSBmaXJzdCB2YWx1ZVxuICAgIHRvcFJvdyA9IHRvcFJvdy5zcGxpdCgnLScpWzBdO1xuXG4gICAgLy8gZ28gdG8gdGhhdCByb3dcbiAgICB2b2lkIHRoaXMuY29udGV4dC5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgIHRoaXMuY29udGVudC5nb1RvTGluZShOdW1iZXIodG9wUm93KSk7XG4gICAgfSk7XG4gIH1cbn1cblxuZXhwb3J0IG5hbWVzcGFjZSBDU1ZEb2N1bWVudFdpZGdldCB7XG4gIC8vIFRPRE86IEluIFR5cGVTY3JpcHQgMi44LCB3ZSBjYW4gbWFrZSBqdXN0IHRoZSBjb250ZW50IHByb3BlcnR5IG9wdGlvbmFsXG4gIC8vIHVzaW5nIHNvbWV0aGluZyBsaWtlIGh0dHBzOi8vc3RhY2tvdmVyZmxvdy5jb20vYS80Njk0MTgyNCwgaW5zdGVhZCBvZlxuICAvLyBpbmhlcml0aW5nIGZyb20gdGhpcyBJT3B0aW9uc09wdGlvbmFsQ29udGVudC5cblxuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zXG4gICAgZXh0ZW5kcyBEb2N1bWVudFdpZGdldC5JT3B0aW9uc09wdGlvbmFsQ29udGVudDxDU1ZWaWV3ZXI+IHtcbiAgICAvKipcbiAgICAgKiBEYXRhIGRlbGltaXRlciBjaGFyYWN0ZXJcbiAgICAgKi9cbiAgICBkZWxpbWl0ZXI/OiBzdHJpbmc7XG4gIH1cbn1cblxuLyoqXG4gKiBBIHdpZGdldCBmYWN0b3J5IGZvciBDU1Ygd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGNsYXNzIENTVlZpZXdlckZhY3RvcnkgZXh0ZW5kcyBBQkNXaWRnZXRGYWN0b3J5PFxuICBJRG9jdW1lbnRXaWRnZXQ8Q1NWVmlld2VyPlxuPiB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGdpdmVuIGEgY29udGV4dC5cbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVOZXdXaWRnZXQoXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0XG4gICk6IElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+IHtcbiAgICBjb25zdCB0cmFuc2xhdG9yID0gdGhpcy50cmFuc2xhdG9yO1xuICAgIHJldHVybiBuZXcgQ1NWRG9jdW1lbnRXaWRnZXQoeyBjb250ZXh0LCB0cmFuc2xhdG9yIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIERlZmF1bHQgZmFjdG9yeSBmb3IgdG9vbGJhciBpdGVtcyB0byBiZSBhZGRlZCBhZnRlciB0aGUgd2lkZ2V0IGlzIGNyZWF0ZWQuXG4gICAqL1xuICBwcm90ZWN0ZWQgZGVmYXVsdFRvb2xiYXJGYWN0b3J5KFxuICAgIHdpZGdldDogSURvY3VtZW50V2lkZ2V0PENTVlZpZXdlcj5cbiAgKTogRG9jdW1lbnRSZWdpc3RyeS5JVG9vbGJhckl0ZW1bXSB7XG4gICAgcmV0dXJuIFtcbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ2RlbGltaXRlcicsXG4gICAgICAgIHdpZGdldDogbmV3IENTVkRlbGltaXRlcih7XG4gICAgICAgICAgd2lkZ2V0OiB3aWRnZXQuY29udGVudCxcbiAgICAgICAgICB0cmFuc2xhdG9yOiB0aGlzLnRyYW5zbGF0b3JcbiAgICAgICAgfSlcbiAgICAgIH1cbiAgICBdO1xuICB9XG59XG5cbi8qKlxuICogQSB3aWRnZXQgZmFjdG9yeSBmb3IgVFNWIHdpZGdldHMuXG4gKi9cbmV4cG9ydCBjbGFzcyBUU1ZWaWV3ZXJGYWN0b3J5IGV4dGVuZHMgQ1NWVmlld2VyRmFjdG9yeSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGdpdmVuIGEgY29udGV4dC5cbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVOZXdXaWRnZXQoXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0XG4gICk6IElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+IHtcbiAgICBjb25zdCBkZWxpbWl0ZXIgPSAnXFx0JztcbiAgICByZXR1cm4gbmV3IENTVkRvY3VtZW50V2lkZ2V0KHtcbiAgICAgIGNvbnRleHQsXG4gICAgICBkZWxpbWl0ZXIsXG4gICAgICB0cmFuc2xhdG9yOiB0aGlzLnRyYW5zbGF0b3JcbiAgICB9KTtcbiAgfVxufVxuXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGxldCBncmlkTG9hZGVkOiBQcm9taXNlRGVsZWdhdGU8dHlwZW9mIERhdGFHcmlkTW9kdWxlPiB8IG51bGwgPSBudWxsO1xuICBsZXQgbW9kZWxMb2FkZWQ6IFByb21pc2VEZWxlZ2F0ZTx0eXBlb2YgRFNWTW9kZWxNb2R1bGU+IHwgbnVsbCA9IG51bGw7XG5cbiAgLyoqXG4gICAqIExhemlseSBsb2FkIHRoZSBkYXRhZ3JpZCBtb2R1bGUgd2hlbiB0aGUgZmlyc3QgZ3JpZCBpcyByZXF1ZXN0ZWQuXG4gICAqL1xuICBleHBvcnQgYXN5bmMgZnVuY3Rpb24gZW5zdXJlRGF0YUdyaWQoKTogUHJvbWlzZTx0eXBlb2YgRGF0YUdyaWRNb2R1bGU+IHtcbiAgICBpZiAoZ3JpZExvYWRlZCA9PSBudWxsKSB7XG4gICAgICBncmlkTG9hZGVkID0gbmV3IFByb21pc2VEZWxlZ2F0ZSgpO1xuICAgICAgZ3JpZExvYWRlZC5yZXNvbHZlKGF3YWl0IGltcG9ydCgnQGx1bWluby9kYXRhZ3JpZCcpKTtcbiAgICB9XG4gICAgcmV0dXJuIGdyaWRMb2FkZWQucHJvbWlzZTtcbiAgfVxuXG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiBlbnN1cmVEU1ZNb2RlbCgpOiBQcm9taXNlPHR5cGVvZiBEU1ZNb2RlbE1vZHVsZT4ge1xuICAgIGlmIChtb2RlbExvYWRlZCA9PSBudWxsKSB7XG4gICAgICBtb2RlbExvYWRlZCA9IG5ldyBQcm9taXNlRGVsZWdhdGUoKTtcbiAgICAgIG1vZGVsTG9hZGVkLnJlc29sdmUoYXdhaXQgaW1wb3J0KCcuL21vZGVsJykpO1xuICAgIH1cbiAgICByZXR1cm4gbW9kZWxMb2FkZWQucHJvbWlzZTtcbiAgfVxuXG4gIGV4cG9ydCBmdW5jdGlvbiBjcmVhdGVDb250ZW50KFxuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuSUNvbnRleHQ8RG9jdW1lbnRSZWdpc3RyeS5JTW9kZWw+XG4gICk6IENTVlZpZXdlciB7XG4gICAgcmV0dXJuIG5ldyBDU1ZWaWV3ZXIoeyBjb250ZXh0IH0pO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=