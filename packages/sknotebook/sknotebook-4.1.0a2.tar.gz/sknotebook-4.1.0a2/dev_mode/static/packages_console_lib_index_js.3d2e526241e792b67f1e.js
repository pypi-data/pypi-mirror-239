"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_console_lib_index_js"],{

/***/ "../packages/console/lib/foreign.js":
/*!******************************************!*\
  !*** ../packages/console/lib/foreign.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ForeignHandler": () => (/* binding */ ForeignHandler)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

const FOREIGN_CELL_CLASS = 'jp-CodeConsole-foreignCell';
/**
 * A handler for capturing API messages from other sessions that should be
 * rendered in a given parent.
 */
class ForeignHandler {
    /**
     * Construct a new foreign message handler.
     */
    constructor(options) {
        this._enabled = false;
        this._isDisposed = false;
        this.sessionContext = options.sessionContext;
        this.sessionContext.iopubMessage.connect(this.onIOPubMessage, this);
        this._parent = options.parent;
    }
    /**
     * Set whether the handler is able to inject foreign cells into a console.
     */
    get enabled() {
        return this._enabled;
    }
    set enabled(value) {
        this._enabled = value;
    }
    /**
     * The foreign handler's parent receiver.
     */
    get parent() {
        return this._parent;
    }
    /**
     * Test whether the handler is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the resources held by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    /**
     * Handler IOPub messages.
     *
     * @returns `true` if the message resulted in a new cell injection or a
     * previously injected cell being updated and `false` for all other messages.
     */
    onIOPubMessage(sender, msg) {
        var _a;
        // Only process messages if foreign cell injection is enabled.
        if (!this._enabled) {
            return false;
        }
        const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return false;
        }
        // Check whether this message came from an external session.
        const parent = this._parent;
        const session = msg.parent_header.session;
        if (session === kernel.clientId) {
            return false;
        }
        const msgType = msg.header.msg_type;
        const parentHeader = msg.parent_header;
        const parentMsgId = parentHeader.msg_id;
        let cell;
        switch (msgType) {
            case 'execute_input': {
                const inputMsg = msg;
                cell = this._newCell(parentMsgId);
                const model = cell.model;
                model.executionCount = inputMsg.content.execution_count;
                model.sharedModel.setSource(inputMsg.content.code);
                model.trusted = true;
                parent.update();
                return true;
            }
            case 'execute_result':
            case 'display_data':
            case 'stream':
            case 'error': {
                cell = this._parent.getCell(parentMsgId);
                if (!cell) {
                    return false;
                }
                const output = {
                    ...msg.content,
                    output_type: msgType
                };
                cell.model.outputs.add(output);
                parent.update();
                return true;
            }
            case 'clear_output': {
                const wait = msg.content.wait;
                cell = this._parent.getCell(parentMsgId);
                if (cell) {
                    cell.model.outputs.clear(wait);
                }
                return true;
            }
            default:
                return false;
        }
    }
    /**
     * Create a new code cell for an input originated from a foreign session.
     */
    _newCell(parentMsgId) {
        const cell = this.parent.createCodeCell();
        cell.addClass(FOREIGN_CELL_CLASS);
        this._parent.addCell(cell, parentMsgId);
        return cell;
    }
}


/***/ }),

/***/ "../packages/console/lib/history.js":
/*!******************************************!*\
  !*** ../packages/console/lib/history.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConsoleHistory": () => (/* binding */ ConsoleHistory)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A console history manager object.
 */
class ConsoleHistory {
    /**
     * Construct a new console history object.
     */
    constructor(options) {
        this._cursor = 0;
        this._hasSession = false;
        this._history = [];
        this._placeholder = '';
        this._setByHistory = false;
        this._isDisposed = false;
        this._editor = null;
        this._filtered = [];
        const { sessionContext } = options;
        if (sessionContext) {
            this.sessionContext = sessionContext;
            void this._handleKernel();
            this.sessionContext.kernelChanged.connect(this._handleKernel, this);
        }
    }
    /**
     * The current editor used by the history manager.
     */
    get editor() {
        return this._editor;
    }
    set editor(value) {
        if (this._editor === value) {
            return;
        }
        const prev = this._editor;
        if (prev) {
            prev.edgeRequested.disconnect(this.onEdgeRequest, this);
            prev.model.sharedModel.changed.disconnect(this.onTextChange, this);
        }
        this._editor = value;
        if (value) {
            value.edgeRequested.connect(this.onEdgeRequest, this);
            value.model.sharedModel.changed.connect(this.onTextChange, this);
        }
    }
    /**
     * The placeholder text that a history session began with.
     */
    get placeholder() {
        return this._placeholder;
    }
    /**
     * Get whether the console history manager is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the console history manager.
     */
    dispose() {
        this._isDisposed = true;
        this._history.length = 0;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    /**
     * Get the previous item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    back(placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
            // Filter the history with the placeholder string.
            this.setFilter(placeholder);
            this._cursor = this._filtered.length - 1;
        }
        --this._cursor;
        this._cursor = Math.max(0, this._cursor);
        const content = this._filtered[this._cursor];
        return Promise.resolve(content);
    }
    /**
     * Get the next item in the console history.
     *
     * @param placeholder - The placeholder string that gets temporarily added
     * to the history only for the duration of one history session. If multiple
     * placeholders are sent within a session, only the first one is accepted.
     *
     * @returns A Promise for console command text or `undefined` if unavailable.
     */
    forward(placeholder) {
        if (!this._hasSession) {
            this._hasSession = true;
            this._placeholder = placeholder;
            // Filter the history with the placeholder string.
            this.setFilter(placeholder);
            this._cursor = this._filtered.length;
        }
        ++this._cursor;
        this._cursor = Math.min(this._filtered.length - 1, this._cursor);
        const content = this._filtered[this._cursor];
        return Promise.resolve(content);
    }
    /**
     * Add a new item to the bottom of history.
     *
     * @param item The item being added to the bottom of history.
     *
     * #### Notes
     * If the item being added is undefined or empty, it is ignored. If the item
     * being added is the same as the last item in history, it is ignored as well
     * so that the console's history will consist of no contiguous repetitions.
     */
    push(item) {
        if (item && item !== this._history[this._history.length - 1]) {
            this._history.push(item);
        }
        this.reset();
    }
    /**
     * Reset the history navigation state, i.e., start a new history session.
     */
    reset() {
        this._cursor = this._history.length;
        this._hasSession = false;
        this._placeholder = '';
    }
    /**
     * Populate the history collection on history reply from a kernel.
     *
     * @param value The kernel message history reply.
     *
     * #### Notes
     * History entries have the shape:
     * [session: number, line: number, input: string]
     * Contiguous duplicates are stripped out of the API response.
     */
    onHistory(value) {
        this._history.length = 0;
        let last = '';
        let current = '';
        if (value.content.status === 'ok') {
            for (let i = 0; i < value.content.history.length; i++) {
                current = value.content.history[i][2];
                if (current !== last) {
                    this._history.push((last = current));
                }
            }
        }
        // Reset the history navigation cursor back to the bottom.
        this._cursor = this._history.length;
    }
    /**
     * Handle a text change signal from the editor.
     */
    onTextChange() {
        if (this._setByHistory) {
            this._setByHistory = false;
            return;
        }
        this.reset();
    }
    /**
     * Handle an edge requested signal.
     */
    onEdgeRequest(editor, location) {
        const sharedModel = editor.model.sharedModel;
        const source = sharedModel.getSource();
        if (location === 'top' || location === 'topLine') {
            void this.back(source).then(value => {
                if (this.isDisposed || !value) {
                    return;
                }
                if (sharedModel.getSource() === value) {
                    return;
                }
                this._setByHistory = true;
                sharedModel.setSource(value);
                let columnPos = 0;
                columnPos = value.indexOf('\n');
                if (columnPos < 0) {
                    columnPos = value.length;
                }
                editor.setCursorPosition({ line: 0, column: columnPos });
            });
        }
        else {
            void this.forward(source).then(value => {
                if (this.isDisposed) {
                    return;
                }
                const text = value || this.placeholder;
                if (sharedModel.getSource() === text) {
                    return;
                }
                this._setByHistory = true;
                sharedModel.setSource(text);
                const pos = editor.getPositionAt(text.length);
                if (pos) {
                    editor.setCursorPosition(pos);
                }
            });
        }
    }
    /**
     * Handle the current kernel changing.
     */
    async _handleKernel() {
        var _a, _b;
        const kernel = (_b = (_a = this.sessionContext) === null || _a === void 0 ? void 0 : _a.session) === null || _b === void 0 ? void 0 : _b.kernel;
        if (!kernel) {
            this._history.length = 0;
            return;
        }
        return kernel.requestHistory(Private.initialRequest).then(v => {
            this.onHistory(v);
        });
    }
    /**
     * Set the filter data.
     *
     * @param filterStr - The string to use when filtering the data.
     */
    setFilter(filterStr = '') {
        // Apply the new filter and remove contiguous duplicates.
        this._filtered.length = 0;
        let last = '';
        let current = '';
        for (let i = 0; i < this._history.length; i++) {
            current = this._history[i];
            if (current !== last &&
                filterStr === current.slice(0, filterStr.length)) {
                this._filtered.push((last = current));
            }
        }
        this._filtered.push(filterStr);
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    Private.initialRequest = {
        output: false,
        raw: true,
        hist_access_type: 'tail',
        n: 500
    };
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/console/lib/index.js":
/*!****************************************!*\
  !*** ../packages/console/lib/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeConsole": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_4__.CodeConsole),
/* harmony export */   "ConsoleHistory": () => (/* reexport safe */ _history__WEBPACK_IMPORTED_MODULE_1__.ConsoleHistory),
/* harmony export */   "ConsolePanel": () => (/* reexport safe */ _panel__WEBPACK_IMPORTED_MODULE_2__.ConsolePanel),
/* harmony export */   "ForeignHandler": () => (/* reexport safe */ _foreign__WEBPACK_IMPORTED_MODULE_0__.ForeignHandler),
/* harmony export */   "IConsoleTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IConsoleTracker)
/* harmony export */ });
/* harmony import */ var _foreign__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./foreign */ "../packages/console/lib/foreign.js");
/* harmony import */ var _history__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./history */ "../packages/console/lib/history.js");
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./panel */ "../packages/console/lib/panel.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "../packages/console/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widget */ "../packages/console/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module console
 */







/***/ }),

/***/ "../packages/console/lib/panel.js":
/*!****************************************!*\
  !*** ../packages/console/lib/panel.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConsolePanel": () => (/* binding */ ConsolePanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./widget */ "../packages/console/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to console panels.
 */
const PANEL_CLASS = 'jp-ConsolePanel';
/**
 * A panel which contains a console and the ability to add other children.
 */
class ConsolePanel extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget {
    /**
     * Construct a console panel.
     */
    constructor(options) {
        super({ content: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Panel() });
        this._executed = null;
        this._connected = null;
        this.addClass(PANEL_CLASS);
        let { rendermime, mimeTypeService, path, basePath, name, manager, modelFactory, sessionContext, translator } = options;
        this.translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        const contentFactory = (this.contentFactory = options.contentFactory);
        const count = Private.count++;
        if (!path) {
            path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(basePath || '', `console-${count}-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.UUID.uuid4()}`);
        }
        sessionContext = this._sessionContext =
            sessionContext !== null && sessionContext !== void 0 ? sessionContext : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.SessionContext({
                sessionManager: manager.sessions,
                specsManager: manager.kernelspecs,
                path: manager.contents.localPath(path),
                name: name || trans.__('Console %1', count),
                type: 'console',
                kernelPreference: options.kernelPreference,
                setBusy: options.setBusy
            });
        const resolver = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.RenderMimeRegistry.UrlResolver({
            path,
            contents: manager.contents
        });
        rendermime = rendermime.clone({ resolver });
        this.console = contentFactory.createConsole({
            rendermime,
            sessionContext: sessionContext,
            mimeTypeService,
            contentFactory,
            modelFactory,
            translator
        });
        this.content.addWidget(this.console);
        void sessionContext.initialize().then(async (value) => {
            var _a;
            if (value) {
                await ((_a = options.sessionDialogs) !== null && _a !== void 0 ? _a : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.SessionContextDialogs({ translator })).selectKernel(sessionContext);
            }
            this._connected = new Date();
            this._updateTitlePanel();
        });
        this.console.executed.connect(this._onExecuted, this);
        this._updateTitlePanel();
        sessionContext.kernelChanged.connect(this._updateTitlePanel, this);
        sessionContext.propertyChanged.connect(this._updateTitlePanel, this);
        this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.consoleIcon;
        this.title.closable = true;
        this.id = `console-${count}`;
    }
    /**
     * The session used by the panel.
     */
    get sessionContext() {
        return this._sessionContext;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        this.sessionContext.dispose();
        this.console.dispose();
        super.dispose();
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        const prompt = this.console.promptCell;
        if (prompt) {
            prompt.editor.focus();
        }
    }
    /**
     * Handle `'close-request'` messages.
     */
    onCloseRequest(msg) {
        super.onCloseRequest(msg);
        this.dispose();
    }
    /**
     * Handle a console execution.
     */
    _onExecuted(sender, args) {
        this._executed = args;
        this._updateTitlePanel();
    }
    /**
     * Update the console panel title.
     */
    _updateTitlePanel() {
        Private.updateTitle(this, this._connected, this._executed, this.translator);
    }
}
/**
 * A namespace for ConsolePanel statics.
 */
(function (ConsolePanel) {
    /**
     * Default implementation of `IContentFactory`.
     */
    class ContentFactory extends _widget__WEBPACK_IMPORTED_MODULE_7__.CodeConsole.ContentFactory {
        /**
         * Create a new console panel.
         */
        createConsole(options) {
            return new _widget__WEBPACK_IMPORTED_MODULE_7__.CodeConsole(options);
        }
    }
    ConsolePanel.ContentFactory = ContentFactory;
    /**
     * The console renderer token.
     */
    ConsolePanel.IContentFactory = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.Token('@jupyterlab/console:IContentFactory', 'A factory object that creates new code consoles. Use this if you want to create and host code consoles in your own UI elements.');
})(ConsolePanel || (ConsolePanel = {}));
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The counter for new consoles.
     */
    Private.count = 1;
    /**
     * Update the title of a console panel.
     */
    function updateTitle(panel, connected, executed, translator) {
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const sessionContext = panel.console.sessionContext.session;
        if (sessionContext) {
            // FIXME:
            let caption = trans.__('Name: %1\n', sessionContext.name) +
                trans.__('Directory: %1\n', _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(sessionContext.path)) +
                trans.__('Kernel: %1', panel.console.sessionContext.kernelDisplayName);
            if (connected) {
                caption += trans.__('\nConnected: %1', _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.Time.format(connected.toISOString()));
            }
            if (executed) {
                caption += trans.__('\nLast Execution: %1');
            }
            panel.title.label = sessionContext.name;
            panel.title.caption = caption;
        }
        else {
            panel.title.label = trans.__('Console');
            panel.title.caption = '';
        }
    }
    Private.updateTitle = updateTitle;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/console/lib/tokens.js":
/*!*****************************************!*\
  !*** ../packages/console/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IConsoleTracker": () => (/* binding */ IConsoleTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The console tracker token.
 */
const IConsoleTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/console:IConsoleTracker', `A widget tracker for code consoles.
  Use this if you want to be able to iterate over and interact with code consoles
  created by the application.`);


/***/ }),

/***/ "../packages/console/lib/widget.js":
/*!*****************************************!*\
  !*** ../packages/console/lib/widget.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeConsole": () => (/* binding */ CodeConsole)
/* harmony export */ });
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @codemirror/state */ "webpack/sharing/consume/default/@codemirror/state/@codemirror/state");
/* harmony import */ var _codemirror_state__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_codemirror_state__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @codemirror/view */ "webpack/sharing/consume/default/@codemirror/view/@codemirror/view");
/* harmony import */ var _codemirror_view__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_codemirror_view__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyter/ydoc */ "webpack/sharing/consume/default/@jupyter/ydoc/@jupyter/ydoc");
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/dragdrop */ "webpack/sharing/consume/default/@lumino/dragdrop/@lumino/dragdrop");
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_dragdrop__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _history__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./history */ "../packages/console/lib/history.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.











/**
 * The data attribute added to a widget that has an active kernel.
 */
const KERNEL_USER = 'jpKernelUser';
/**
 * The data attribute added to a widget can run code.
 */
const CODE_RUNNER = 'jpCodeRunner';
/**
 * The class name added to console widgets.
 */
const CONSOLE_CLASS = 'jp-CodeConsole';
/**
 * The class added to console cells
 */
const CONSOLE_CELL_CLASS = 'jp-Console-cell';
/**
 * The class name added to the console banner.
 */
const BANNER_CLASS = 'jp-CodeConsole-banner';
/**
 * The class name of the active prompt cell.
 */
const PROMPT_CLASS = 'jp-CodeConsole-promptCell';
/**
 * The class name of the panel that holds cell content.
 */
const CONTENT_CLASS = 'jp-CodeConsole-content';
/**
 * The class name of the panel that holds prompts.
 */
const INPUT_CLASS = 'jp-CodeConsole-input';
/**
 * The timeout in ms for execution requests to the kernel.
 */
const EXECUTION_TIMEOUT = 250;
/**
 * The mimetype used for Jupyter cell data.
 */
const JUPYTER_CELL_MIME = 'application/vnd.jupyter.cells';
/**
 * A widget containing a Jupyter console.
 *
 * #### Notes
 * The CodeConsole class is intended to be used within a ConsolePanel
 * instance. Under most circumstances, it is not instantiated by user code.
 */
class CodeConsole extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.Widget {
    /**
     * Construct a console widget.
     */
    constructor(options) {
        var _a, _b;
        super();
        /**
         * The configuration options for the text editor widget.
         */
        this.editorConfig = CodeConsole.defaultEditorConfig;
        this._banner = null;
        this._executed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__.Signal(this);
        this._mimetype = 'text/x-ipython';
        this._msgIds = new Map();
        this._msgIdCells = new Map();
        this._promptCellCreated = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__.Signal(this);
        this._dragData = null;
        this._drag = null;
        this._focusedCell = null;
        this._translator = (_a = options.translator) !== null && _a !== void 0 ? _a : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.nullTranslator;
        this.addClass(CONSOLE_CLASS);
        this.node.dataset[KERNEL_USER] = 'true';
        this.node.dataset[CODE_RUNNER] = 'true';
        this.node.tabIndex = -1; // Allow the widget to take focus.
        // Create the panels that hold the content and input.
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.PanelLayout());
        this._cells = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_4__.ObservableList();
        this._content = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.Panel();
        this._input = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_9__.Panel();
        this.contentFactory = options.contentFactory;
        this.modelFactory = (_b = options.modelFactory) !== null && _b !== void 0 ? _b : CodeConsole.defaultModelFactory;
        this.rendermime = options.rendermime;
        this.sessionContext = options.sessionContext;
        this._mimeTypeService = options.mimeTypeService;
        // Add top-level CSS classes.
        this._content.addClass(CONTENT_CLASS);
        this._input.addClass(INPUT_CLASS);
        // Insert the content and input panes into the widget.
        layout.addWidget(this._content);
        layout.addWidget(this._input);
        this._history = new _history__WEBPACK_IMPORTED_MODULE_10__.ConsoleHistory({
            sessionContext: this.sessionContext
        });
        void this._onKernelChanged();
        this.sessionContext.kernelChanged.connect(this._onKernelChanged, this);
        this.sessionContext.statusChanged.connect(this._onKernelStatusChanged, this);
    }
    /**
     * A signal emitted when the console finished executing its prompt cell.
     */
    get executed() {
        return this._executed;
    }
    /**
     * A signal emitted when a new prompt cell is created.
     */
    get promptCellCreated() {
        return this._promptCellCreated;
    }
    /**
     * The list of content cells in the console.
     *
     * #### Notes
     * This list does not include the current banner or the prompt for a console.
     * It may include previous banners as raw cells.
     */
    get cells() {
        return this._cells;
    }
    /*
     * The console input prompt cell.
     */
    get promptCell() {
        const inputLayout = this._input.layout;
        return inputLayout.widgets[0] || null;
    }
    /**
     * Add a new cell to the content panel.
     *
     * @param cell - The code cell widget being added to the content panel.
     *
     * @param msgId - The optional execution message id for the cell.
     *
     * #### Notes
     * This method is meant for use by outside classes that want to add cells to a
     * console. It is distinct from the `inject` method in that it requires
     * rendered code cell widgets and does not execute them (though it can store
     * the execution message id).
     */
    addCell(cell, msgId) {
        cell.addClass(CONSOLE_CELL_CLASS);
        this._content.addWidget(cell);
        this._cells.push(cell);
        if (msgId) {
            this._msgIds.set(msgId, cell);
            this._msgIdCells.set(cell, msgId);
        }
        cell.disposed.connect(this._onCellDisposed, this);
        this.update();
    }
    /**
     * Add a banner cell.
     */
    addBanner() {
        if (this._banner) {
            // An old banner just becomes a normal cell now.
            const cell = this._banner;
            this._cells.push(this._banner);
            cell.disposed.connect(this._onCellDisposed, this);
        }
        // Create the banner.
        const model = this.modelFactory.createRawCell({
            sharedModel: (0,_jupyter_ydoc__WEBPACK_IMPORTED_MODULE_2__.createStandaloneCell)({
                cell_type: 'raw',
                source: '...'
            })
        });
        const banner = (this._banner = new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.RawCell({
            model,
            contentFactory: this.contentFactory,
            placeholder: false,
            editorConfig: {
                autoClosingBrackets: false,
                codeFolding: false,
                highlightActiveLine: false,
                highlightTrailingWhitespace: false,
                highlightWhitespace: false,
                indentUnit: '4',
                lineNumbers: false,
                lineWrap: true,
                matchBrackets: false,
                readOnly: true,
                rulers: [],
                scrollPastEnd: false,
                smartIndent: false,
                tabSize: 4,
                theme: 'jupyter'
            }
        })).initializeState();
        banner.addClass(BANNER_CLASS);
        banner.readOnly = true;
        this._content.addWidget(banner);
    }
    /**
     * Clear the code cells.
     */
    clear() {
        // Dispose all the content cells
        const cells = this._cells;
        while (cells.length > 0) {
            cells.get(0).dispose();
        }
    }
    /**
     * Create a new cell with the built-in factory.
     */
    createCodeCell() {
        const factory = this.contentFactory;
        const options = this._createCodeCellOptions();
        const cell = factory.createCodeCell(options);
        cell.readOnly = true;
        cell.model.mimeType = this._mimetype;
        return cell;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        // Do nothing if already disposed.
        if (this.isDisposed) {
            return;
        }
        this._msgIdCells = null;
        this._msgIds = null;
        this._history.dispose();
        super.dispose();
    }
    /**
     * Execute the current prompt.
     *
     * @param force - Whether to force execution without checking code
     * completeness.
     *
     * @param timeout - The length of time, in milliseconds, that the execution
     * should wait for the API to determine whether code being submitted is
     * incomplete before attempting submission anyway. The default value is `250`.
     */
    async execute(force = false, timeout = EXECUTION_TIMEOUT) {
        var _a, _b;
        if (((_b = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) === null || _b === void 0 ? void 0 : _b.status) === 'dead') {
            return;
        }
        const promptCell = this.promptCell;
        if (!promptCell) {
            throw new Error('Cannot execute without a prompt cell');
        }
        promptCell.model.trusted = true;
        if (force) {
            // Create a new prompt cell before kernel execution to allow typeahead.
            this.newPromptCell();
            await this._execute(promptCell);
            return;
        }
        // Check whether we should execute.
        const shouldExecute = await this._shouldExecute(timeout);
        if (this.isDisposed) {
            return;
        }
        if (shouldExecute) {
            // Create a new prompt cell before kernel execution to allow typeahead.
            this.newPromptCell();
            this.promptCell.editor.focus();
            await this._execute(promptCell);
        }
        else {
            // add a newline if we shouldn't execute
            promptCell.editor.newIndentedLine();
        }
    }
    /**
     * Get a cell given a message id.
     *
     * @param msgId - The message id.
     */
    getCell(msgId) {
        return this._msgIds.get(msgId);
    }
    /**
     * Inject arbitrary code for the console to execute immediately.
     *
     * @param code - The code contents of the cell being injected.
     *
     * @returns A promise that indicates when the injected cell's execution ends.
     */
    inject(code, metadata = {}) {
        const cell = this.createCodeCell();
        cell.model.sharedModel.setSource(code);
        for (const key of Object.keys(metadata)) {
            cell.model.setMetadata(key, metadata[key]);
        }
        this.addCell(cell);
        return this._execute(cell);
    }
    /**
     * Insert a line break in the prompt cell.
     */
    insertLinebreak() {
        const promptCell = this.promptCell;
        if (!promptCell) {
            return;
        }
        promptCell.editor.newIndentedLine();
    }
    /**
     * Replaces the selected text in the prompt cell.
     *
     * @param text - The text to replace the selection.
     */
    replaceSelection(text) {
        var _a, _b;
        const promptCell = this.promptCell;
        if (!promptCell) {
            return;
        }
        (_b = (_a = promptCell.editor).replaceSelection) === null || _b === void 0 ? void 0 : _b.call(_a, text);
    }
    /**
     * Serialize the output.
     *
     * #### Notes
     * This only serializes the code cells and the prompt cell if it exists, and
     * skips any old banner cells.
     */
    serialize() {
        const cells = [];
        for (const cell of this._cells) {
            const model = cell.model;
            if ((0,_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.isCodeCellModel)(model)) {
                cells.push(model.toJSON());
            }
        }
        if (this.promptCell) {
            cells.push(this.promptCell.model.toJSON());
        }
        return cells;
    }
    /**
     * Handle `mousedown` events for the widget.
     */
    _evtMouseDown(event) {
        const { button, shiftKey } = event;
        // We only handle main or secondary button actions.
        if (!(button === 0 || button === 2) ||
            // Shift right-click gives the browser default behavior.
            (shiftKey && button === 2)) {
            return;
        }
        let target = event.target;
        const cellFilter = (node) => node.classList.contains(CONSOLE_CELL_CLASS);
        let cellIndex = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CellDragUtils.findCell(target, this._cells, cellFilter);
        if (cellIndex === -1) {
            // `event.target` sometimes gives an orphaned node in
            // Firefox 57, which can have `null` anywhere in its parent line. If we fail
            // to find a cell using `event.target`, try again using a target
            // reconstructed from the position of the click event.
            target = document.elementFromPoint(event.clientX, event.clientY);
            cellIndex = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CellDragUtils.findCell(target, this._cells, cellFilter);
        }
        if (cellIndex === -1) {
            return;
        }
        const cell = this._cells.get(cellIndex);
        const targetArea = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CellDragUtils.detectTargetArea(cell, event.target);
        if (targetArea === 'prompt') {
            this._dragData = {
                pressX: event.clientX,
                pressY: event.clientY,
                index: cellIndex
            };
            this._focusedCell = cell;
            document.addEventListener('mouseup', this, true);
            document.addEventListener('mousemove', this, true);
            event.preventDefault();
        }
    }
    /**
     * Handle `mousemove` event of widget
     */
    _evtMouseMove(event) {
        const data = this._dragData;
        if (data &&
            _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CellDragUtils.shouldStartDrag(data.pressX, data.pressY, event.clientX, event.clientY)) {
            void this._startDrag(data.index, event.clientX, event.clientY);
        }
    }
    /**
     * Start a drag event
     */
    _startDrag(index, clientX, clientY) {
        const cellModel = this._focusedCell.model;
        const selected = [cellModel.toJSON()];
        const dragImage = _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CellDragUtils.createCellDragImage(this._focusedCell, selected);
        this._drag = new _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_7__.Drag({
            mimeData: new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__.MimeData(),
            dragImage,
            proposedAction: 'copy',
            supportedActions: 'copy',
            source: this
        });
        this._drag.mimeData.setData(JUPYTER_CELL_MIME, selected);
        const textContent = cellModel.sharedModel.getSource();
        this._drag.mimeData.setData('text/plain', textContent);
        this._focusedCell = null;
        document.removeEventListener('mousemove', this, true);
        document.removeEventListener('mouseup', this, true);
        return this._drag.start(clientX, clientY).then(() => {
            if (this.isDisposed) {
                return;
            }
            this._drag = null;
            this._dragData = null;
        });
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event -The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeyDown(event);
                break;
            case 'mousedown':
                this._evtMouseDown(event);
                break;
            case 'mousemove':
                this._evtMouseMove(event);
                break;
            case 'mouseup':
                this._evtMouseUp(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after_attach` messages for the widget.
     */
    onAfterAttach(msg) {
        const node = this.node;
        node.addEventListener('keydown', this, true);
        node.addEventListener('click', this);
        node.addEventListener('mousedown', this);
        // Create a prompt if necessary.
        if (!this.promptCell) {
            this.newPromptCell();
        }
        else {
            this.promptCell.editor.focus();
            this.update();
        }
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('keydown', this, true);
        node.removeEventListener('click', this);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        const editor = this.promptCell && this.promptCell.editor;
        if (editor) {
            editor.focus();
        }
        this.update();
    }
    /**
     * Make a new prompt cell.
     */
    newPromptCell() {
        var _a;
        let promptCell = this.promptCell;
        const input = this._input;
        // Make the last prompt read-only, clear its signals, and move to content.
        if (promptCell) {
            promptCell.readOnly = true;
            promptCell.removeClass(PROMPT_CLASS);
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_8__.Signal.clearData(promptCell.editor);
            // Ensure to clear the cursor
            (_a = promptCell.editor) === null || _a === void 0 ? void 0 : _a.blur();
            const child = input.widgets[0];
            child.parent = null;
            this.addCell(promptCell);
        }
        // Create the new prompt cell.
        const factory = this.contentFactory;
        const options = this._createCodeCellOptions();
        promptCell = factory.createCodeCell(options);
        promptCell.model.mimeType = this._mimetype;
        promptCell.addClass(PROMPT_CLASS);
        // Add the prompt cell to the DOM, making `this.promptCell` valid again.
        this._input.addWidget(promptCell);
        this._history.editor = promptCell.editor;
        this._promptCellCreated.emit(promptCell);
    }
    /**
     * Handle `update-request` messages.
     */
    onUpdateRequest(msg) {
        Private.scrollToBottom(this._content.node);
    }
    /**
     * Handle the `'keydown'` event for the widget.
     */
    _evtKeyDown(event) {
        const editor = this.promptCell && this.promptCell.editor;
        if (!editor) {
            return;
        }
        if (event.keyCode === 13 && !editor.hasFocus()) {
            event.preventDefault();
            editor.focus();
        }
        else if (event.keyCode === 27 && editor.hasFocus()) {
            // Set to command mode
            event.preventDefault();
            event.stopPropagation();
            this.node.focus();
        }
    }
    /**
     * Handle the `'mouseup'` event for the widget.
     */
    _evtMouseUp(event) {
        if (this.promptCell &&
            this.promptCell.node.contains(event.target)) {
            this.promptCell.editor.focus();
        }
    }
    /**
     * Execute the code in the current prompt cell.
     */
    _execute(cell) {
        const source = cell.model.sharedModel.getSource();
        this._history.push(source);
        // If the source of the console is just "clear", clear the console as we
        // do in IPython or QtConsole.
        if (source === 'clear' || source === '%clear') {
            this.clear();
            return Promise.resolve(void 0);
        }
        cell.model.contentChanged.connect(this.update, this);
        const onSuccess = (value) => {
            if (this.isDisposed) {
                return;
            }
            if (value && value.content.status === 'ok') {
                const content = value.content;
                // Use deprecated payloads for backwards compatibility.
                if (content.payload && content.payload.length) {
                    const setNextInput = content.payload.filter(i => {
                        return i.source === 'set_next_input';
                    })[0];
                    if (setNextInput) {
                        const text = setNextInput.text;
                        // Ignore the `replace` value and always set the next cell.
                        cell.model.sharedModel.setSource(text);
                    }
                }
            }
            else if (value && value.content.status === 'error') {
                for (const cell of this._cells) {
                    if (cell.model.executionCount === null) {
                        cell.setPrompt('');
                    }
                }
            }
            cell.model.contentChanged.disconnect(this.update, this);
            this.update();
            this._executed.emit(new Date());
        };
        const onFailure = () => {
            if (this.isDisposed) {
                return;
            }
            cell.model.contentChanged.disconnect(this.update, this);
            this.update();
        };
        return _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCell.execute(cell, this.sessionContext).then(onSuccess, onFailure);
    }
    /**
     * Update the console based on the kernel info.
     */
    _handleInfo(info) {
        if (info.status !== 'ok') {
            this._banner.model.sharedModel.setSource('Error in getting kernel banner');
            return;
        }
        this._banner.model.sharedModel.setSource(info.banner);
        const lang = info.language_info;
        this._mimetype = this._mimeTypeService.getMimeTypeByLanguage(lang);
        if (this.promptCell) {
            this.promptCell.model.mimeType = this._mimetype;
        }
    }
    /**
     * Create the options used to initialize a code cell widget.
     */
    _createCodeCellOptions() {
        const contentFactory = this.contentFactory;
        const modelFactory = this.modelFactory;
        const model = modelFactory.createCodeCell({});
        const rendermime = this.rendermime;
        const editorConfig = this.editorConfig;
        // Suppress the default "Enter" key handling.
        const onKeyDown = _codemirror_view__WEBPACK_IMPORTED_MODULE_1__.EditorView.domEventHandlers({
            keydown: (event, view) => {
                if (event.keyCode === 13) {
                    event.preventDefault();
                    return true;
                }
                return false;
            }
        });
        return {
            model,
            rendermime,
            contentFactory,
            editorConfig,
            editorExtensions: [_codemirror_state__WEBPACK_IMPORTED_MODULE_0__.Prec.high(onKeyDown)],
            placeholder: false,
            translator: this._translator
        };
    }
    /**
     * Handle cell disposed signals.
     */
    _onCellDisposed(sender, args) {
        if (!this.isDisposed) {
            this._cells.removeValue(sender);
            const msgId = this._msgIdCells.get(sender);
            if (msgId) {
                this._msgIdCells.delete(sender);
                this._msgIds.delete(msgId);
            }
        }
    }
    /**
     * Test whether we should execute the prompt cell.
     */
    _shouldExecute(timeout) {
        const promptCell = this.promptCell;
        if (!promptCell) {
            return Promise.resolve(false);
        }
        const model = promptCell.model;
        const code = model.sharedModel.getSource();
        return new Promise((resolve, reject) => {
            var _a;
            const timer = setTimeout(() => {
                resolve(true);
            }, timeout);
            const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (!kernel) {
                resolve(false);
                return;
            }
            kernel
                .requestIsComplete({ code })
                .then(isComplete => {
                clearTimeout(timer);
                if (this.isDisposed) {
                    resolve(false);
                }
                if (isComplete.content.status !== 'incomplete') {
                    resolve(true);
                    return;
                }
                resolve(false);
            })
                .catch(() => {
                resolve(true);
            });
        });
    }
    /**
     * Handle a change to the kernel.
     */
    async _onKernelChanged() {
        var _a;
        this.clear();
        if (this._banner) {
            this._banner.dispose();
            this._banner = null;
        }
        this.addBanner();
        if ((_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel) {
            this._handleInfo(await this.sessionContext.session.kernel.info);
        }
    }
    /**
     * Handle a change to the kernel status.
     */
    async _onKernelStatusChanged() {
        var _a;
        const kernel = (_a = this.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if ((kernel === null || kernel === void 0 ? void 0 : kernel.status) === 'restarting') {
            this.addBanner();
            this._handleInfo(await (kernel === null || kernel === void 0 ? void 0 : kernel.info));
        }
    }
}
/**
 * A namespace for CodeConsole statics.
 */
(function (CodeConsole) {
    /**
     * Default console editor configuration
     */
    CodeConsole.defaultEditorConfig = {
        codeFolding: false,
        lineNumbers: false
    };
    /**
     * Default implementation of `IContentFactory`.
     */
    class ContentFactory extends _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.Cell.ContentFactory {
        /**
         * Create a new code cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createCodeCell(options) {
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCell(options).initializeState();
        }
        /**
         * Create a new raw cell widget.
         *
         * #### Notes
         * If no cell content factory is passed in with the options, the one on the
         * notebook content factory is used.
         */
        createRawCell(options) {
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.RawCell(options).initializeState();
        }
    }
    CodeConsole.ContentFactory = ContentFactory;
    /**
     * The default implementation of an `IModelFactory`.
     */
    class ModelFactory {
        /**
         * Create a new cell model factory.
         */
        constructor(options = {}) {
            this.codeCellContentFactory =
                options.codeCellContentFactory || _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCellModel.defaultContentFactory;
        }
        /**
         * Create a new code cell.
         * @param options - The data to use for the original source data.
         * @returns A new code cell. If a source cell is provided, the
        new cell will be initialized with the data from the source.
        If the contentFactory is not provided, the instance
        `codeCellContentFactory` will be used.
         */
        createCodeCell(options = {}) {
            if (!options.contentFactory) {
                options.contentFactory = this.codeCellContentFactory;
            }
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCellModel(options);
        }
        /**
         * Create a new raw cell.
         * @param options - The data to use for the original source data.
         * @returns A new raw cell. If a source cell is provided, the
        new cell will be initialized with the data from the source.
         */
        createRawCell(options) {
            return new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.RawCellModel(options);
        }
    }
    CodeConsole.ModelFactory = ModelFactory;
    /**
     * The default `ModelFactory` instance.
     */
    CodeConsole.defaultModelFactory = new ModelFactory({});
})(CodeConsole || (CodeConsole = {}));
/**
 * A namespace for console widget private data.
 */
var Private;
(function (Private) {
    /**
     * Jump to the bottom of a node.
     *
     * @param node - The scrollable element.
     */
    function scrollToBottom(node) {
        node.scrollTop = node.scrollHeight - node.clientHeight;
    }
    Private.scrollToBottom = scrollToBottom;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY29uc29sZV9saWJfaW5kZXhfanMuM2QyZTUyNjI0MWU3OTJiNjdmMWUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQU9oQjtBQUUzQyxNQUFNLGtCQUFrQixHQUFHLDRCQUE0QixDQUFDO0FBRXhEOzs7R0FHRztBQUNJLE1BQU0sY0FBYztJQUN6Qjs7T0FFRztJQUNILFlBQVksT0FBZ0M7UUE2SHBDLGFBQVEsR0FBRyxLQUFLLENBQUM7UUFFakIsZ0JBQVcsR0FBRyxLQUFLLENBQUM7UUE5SDFCLElBQUksQ0FBQyxjQUFjLEdBQUcsT0FBTyxDQUFDLGNBQWMsQ0FBQztRQUM3QyxJQUFJLENBQUMsY0FBYyxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLGNBQWMsRUFBRSxJQUFJLENBQUMsQ0FBQztRQUNwRSxJQUFJLENBQUMsT0FBTyxHQUFHLE9BQU8sQ0FBQyxNQUFNLENBQUM7SUFDaEMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxPQUFPO1FBQ1QsT0FBTyxJQUFJLENBQUMsUUFBUSxDQUFDO0lBQ3ZCLENBQUM7SUFDRCxJQUFJLE9BQU8sQ0FBQyxLQUFjO1FBQ3hCLElBQUksQ0FBQyxRQUFRLEdBQUcsS0FBSyxDQUFDO0lBQ3hCLENBQUM7SUFPRDs7T0FFRztJQUNILElBQUksTUFBTTtRQUNSLE9BQU8sSUFBSSxDQUFDLE9BQU8sQ0FBQztJQUN0QixDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLFVBQVU7UUFDWixPQUFPLElBQUksQ0FBQyxXQUFXLENBQUM7SUFDMUIsQ0FBQztJQUVEOztPQUVHO0lBQ0gsT0FBTztRQUNMLElBQUksSUFBSSxDQUFDLFVBQVUsRUFBRTtZQUNuQixPQUFPO1NBQ1I7UUFDRCxJQUFJLENBQUMsV0FBVyxHQUFHLElBQUksQ0FBQztRQUN4QiwrREFBZ0IsQ0FBQyxJQUFJLENBQUMsQ0FBQztJQUN6QixDQUFDO0lBRUQ7Ozs7O09BS0c7SUFD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YyxpQkFFN0I7QUFDSCxDQUFDLEVBVFMsT0FBTyxLQUFQLE9BQU8sUUFTaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29uc29sZS9zcmMvZm9yZWlnbi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29uc29sZS9zcmMvaGlzdG9yeS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29uc29sZS9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvbnNvbGUvc3JjL3BhbmVsLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb25zb2xlL3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvbnNvbGUvc3JjL3dpZGdldC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElTZXNzaW9uQ29udGV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IENvZGVDZWxsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY2VsbHMnO1xuaW1wb3J0ICogYXMgbmJmb3JtYXQgZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgS2VybmVsTWVzc2FnZSB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcblxuY29uc3QgRk9SRUlHTl9DRUxMX0NMQVNTID0gJ2pwLUNvZGVDb25zb2xlLWZvcmVpZ25DZWxsJztcblxuLyoqXG4gKiBBIGhhbmRsZXIgZm9yIGNhcHR1cmluZyBBUEkgbWVzc2FnZXMgZnJvbSBvdGhlciBzZXNzaW9ucyB0aGF0IHNob3VsZCBiZVxuICogcmVuZGVyZWQgaW4gYSBnaXZlbiBwYXJlbnQuXG4gKi9cbmV4cG9ydCBjbGFzcyBGb3JlaWduSGFuZGxlciBpbXBsZW1lbnRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBmb3JlaWduIG1lc3NhZ2UgaGFuZGxlci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEZvcmVpZ25IYW5kbGVyLklPcHRpb25zKSB7XG4gICAgdGhpcy5zZXNzaW9uQ29udGV4dCA9IG9wdGlvbnMuc2Vzc2lvbkNvbnRleHQ7XG4gICAgdGhpcy5zZXNzaW9uQ29udGV4dC5pb3B1Yk1lc3NhZ2UuY29ubmVjdCh0aGlzLm9uSU9QdWJNZXNzYWdlLCB0aGlzKTtcbiAgICB0aGlzLl9wYXJlbnQgPSBvcHRpb25zLnBhcmVudDtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgd2hldGhlciB0aGUgaGFuZGxlciBpcyBhYmxlIHRvIGluamVjdCBmb3JlaWduIGNlbGxzIGludG8gYSBjb25zb2xlLlxuICAgKi9cbiAgZ2V0IGVuYWJsZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2VuYWJsZWQ7XG4gIH1cbiAgc2V0IGVuYWJsZWQodmFsdWU6IGJvb2xlYW4pIHtcbiAgICB0aGlzLl9lbmFibGVkID0gdmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGNsaWVudCBzZXNzaW9uIHVzZWQgYnkgdGhlIGZvcmVpZ24gaGFuZGxlci5cbiAgICovXG4gIHJlYWRvbmx5IHNlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQ7XG5cbiAgLyoqXG4gICAqIFRoZSBmb3JlaWduIGhhbmRsZXIncyBwYXJlbnQgcmVjZWl2ZXIuXG4gICAqL1xuICBnZXQgcGFyZW50KCk6IEZvcmVpZ25IYW5kbGVyLklSZWNlaXZlciB7XG4gICAgcmV0dXJuIHRoaXMuX3BhcmVudDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUZXN0IHdoZXRoZXIgdGhlIGhhbmRsZXIgaXMgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgaGFuZGxlci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZXIgSU9QdWIgbWVzc2FnZXMuXG4gICAqXG4gICAqIEByZXR1cm5zIGB0cnVlYCBpZiB0aGUgbWVzc2FnZSByZXN1bHRlZCBpbiBhIG5ldyBjZWxsIGluamVjdGlvbiBvciBhXG4gICAqIHByZXZpb3VzbHkgaW5qZWN0ZWQgY2VsbCBiZWluZyB1cGRhdGVkIGFuZCBgZmFsc2VgIGZvciBhbGwgb3RoZXIgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25JT1B1Yk1lc3NhZ2UoXG4gICAgc2VuZGVyOiBJU2Vzc2lvbkNvbnRleHQsXG4gICAgbXNnOiBLZXJuZWxNZXNzYWdlLklJT1B1Yk1lc3NhZ2VcbiAgKTogYm9vbGVhbiB7XG4gICAgLy8gT25seSBwcm9jZXNzIG1lc3NhZ2VzIGlmIGZvcmVpZ24gY2VsbCBpbmplY3Rpb24gaXMgZW5hYmxlZC5cbiAgICBpZiAoIXRoaXMuX2VuYWJsZWQpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gICAgY29uc3Qga2VybmVsID0gdGhpcy5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgaWYgKCFrZXJuZWwpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG5cbiAgICAvLyBDaGVjayB3aGV0aGVyIHRoaXMgbWVzc2FnZSBjYW1lIGZyb20gYW4gZXh0ZXJuYWwgc2Vzc2lvbi5cbiAgICBjb25zdCBwYXJlbnQgPSB0aGlzLl9wYXJlbnQ7XG4gICAgY29uc3Qgc2Vzc2lvbiA9IChtc2cucGFyZW50X2hlYWRlciBhcyBLZXJuZWxNZXNzYWdlLklIZWFkZXIpLnNlc3Npb247XG4gICAgaWYgKHNlc3Npb24gPT09IGtlcm5lbC5jbGllbnRJZCkge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgICBjb25zdCBtc2dUeXBlID0gbXNnLmhlYWRlci5tc2dfdHlwZTtcbiAgICBjb25zdCBwYXJlbnRIZWFkZXIgPSBtc2cucGFyZW50X2hlYWRlciBhcyBLZXJuZWxNZXNzYWdlLklIZWFkZXI7XG4gICAgY29uc3QgcGFyZW50TXNnSWQgPSBwYXJlbnRIZWFkZXIubXNnX2lkIGFzIHN0cmluZztcbiAgICBsZXQgY2VsbDogQ29kZUNlbGwgfCB1bmRlZmluZWQ7XG4gICAgc3dpdGNoIChtc2dUeXBlKSB7XG4gICAgICBjYXNlICdleGVjdXRlX2lucHV0Jzoge1xuICAgICAgICBjb25zdCBpbnB1dE1zZyA9IG1zZyBhcyBLZXJuZWxNZXNzYWdlLklFeGVjdXRlSW5wdXRNc2c7XG4gICAgICAgIGNlbGwgPSB0aGlzLl9uZXdDZWxsKHBhcmVudE1zZ0lkKTtcbiAgICAgICAgY29uc3QgbW9kZWwgPSBjZWxsLm1vZGVsO1xuICAgICAgICBtb2RlbC5leGVjdXRpb25Db3VudCA9IGlucHV0TXNnLmNvbnRlbnQuZXhlY3V0aW9uX2NvdW50O1xuICAgICAgICBtb2RlbC5zaGFyZWRNb2RlbC5zZXRTb3VyY2UoaW5wdXRNc2cuY29udGVudC5jb2RlKTtcbiAgICAgICAgbW9kZWwudHJ1c3RlZCA9IHRydWU7XG4gICAgICAgIHBhcmVudC51cGRhdGUoKTtcbiAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICB9XG4gICAgICBjYXNlICdleGVjdXRlX3Jlc3VsdCc6XG4gICAgICBjYXNlICdkaXNwbGF5X2RhdGEnOlxuICAgICAgY2FzZSAnc3RyZWFtJzpcbiAgICAgIGNhc2UgJ2Vycm9yJzoge1xuICAgICAgICBjZWxsID0gdGhpcy5fcGFyZW50LmdldENlbGwocGFyZW50TXNnSWQpO1xuICAgICAgICBpZiAoIWNlbGwpIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgICAgY29uc3Qgb3V0cHV0OiBuYmZvcm1hdC5JT3V0cHV0ID0ge1xuICAgICAgICAgIC4uLm1zZy5jb250ZW50LFxuICAgICAgICAgIG91dHB1dF90eXBlOiBtc2dUeXBlXG4gICAgICAgIH07XG4gICAgICAgIGNlbGwubW9kZWwub3V0cHV0cy5hZGQob3V0cHV0KTtcbiAgICAgICAgcGFyZW50LnVwZGF0ZSgpO1xuICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgIH1cbiAgICAgIGNhc2UgJ2NsZWFyX291dHB1dCc6IHtcbiAgICAgICAgY29uc3Qgd2FpdCA9IChtc2cgYXMgS2VybmVsTWVzc2FnZS5JQ2xlYXJPdXRwdXRNc2cpLmNvbnRlbnQud2FpdDtcbiAgICAgICAgY2VsbCA9IHRoaXMuX3BhcmVudC5nZXRDZWxsKHBhcmVudE1zZ0lkKTtcbiAgICAgICAgaWYgKGNlbGwpIHtcbiAgICAgICAgICBjZWxsLm1vZGVsLm91dHB1dHMuY2xlYXIod2FpdCk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICB9XG4gICAgICBkZWZhdWx0OlxuICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBjb2RlIGNlbGwgZm9yIGFuIGlucHV0IG9yaWdpbmF0ZWQgZnJvbSBhIGZvcmVpZ24gc2Vzc2lvbi5cbiAgICovXG4gIHByaXZhdGUgX25ld0NlbGwocGFyZW50TXNnSWQ6IHN0cmluZyk6IENvZGVDZWxsIHtcbiAgICBjb25zdCBjZWxsID0gdGhpcy5wYXJlbnQuY3JlYXRlQ29kZUNlbGwoKTtcbiAgICBjZWxsLmFkZENsYXNzKEZPUkVJR05fQ0VMTF9DTEFTUyk7XG4gICAgdGhpcy5fcGFyZW50LmFkZENlbGwoY2VsbCwgcGFyZW50TXNnSWQpO1xuICAgIHJldHVybiBjZWxsO1xuICB9XG5cbiAgcHJpdmF0ZSBfZW5hYmxlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9wYXJlbnQ6IEZvcmVpZ25IYW5kbGVyLklSZWNlaXZlcjtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgRm9yZWlnbkhhbmRsZXJgIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgRm9yZWlnbkhhbmRsZXIge1xuICAvKipcbiAgICogVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSBmb3JlaWduIGhhbmRsZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY2xpZW50IHNlc3Npb24gdXNlZCBieSB0aGUgZm9yZWlnbiBoYW5kbGVyLlxuICAgICAqL1xuICAgIHNlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcGFyZW50IGludG8gd2hpY2ggdGhlIGhhbmRsZXIgd2lsbCBpbmplY3QgY29kZSBjZWxscy5cbiAgICAgKi9cbiAgICBwYXJlbnQ6IElSZWNlaXZlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHJlY2VpdmVyIG9mIG5ld2x5IGNyZWF0ZWQgZm9yZWlnbiBjZWxscy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVJlY2VpdmVyIHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBjZWxsLlxuICAgICAqL1xuICAgIGNyZWF0ZUNvZGVDZWxsKCk6IENvZGVDZWxsO1xuXG4gICAgLyoqXG4gICAgICogQWRkIGEgbmV3bHkgY3JlYXRlZCBjZWxsLlxuICAgICAqL1xuICAgIGFkZENlbGwoY2VsbDogQ29kZUNlbGwsIG1zZ0lkOiBzdHJpbmcpOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogVHJpZ2dlciBhIHJlbmRlcmluZyB1cGRhdGUgb24gdGhlIHJlY2VpdmVyLlxuICAgICAqL1xuICAgIHVwZGF0ZSgpOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogR2V0IGEgY2VsbCBhc3NvY2lhdGVkIHdpdGggYSBtZXNzYWdlIGlkLlxuICAgICAqL1xuICAgIGdldENlbGwobXNnSWQ6IHN0cmluZyk6IENvZGVDZWxsIHwgdW5kZWZpbmVkO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElTZXNzaW9uQ29udGV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IENvZGVFZGl0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IEtlcm5lbE1lc3NhZ2UgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogVGhlIGRlZmluaXRpb24gb2YgYSBjb25zb2xlIGhpc3RvcnkgbWFuYWdlciBvYmplY3QuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUNvbnNvbGVIaXN0b3J5IGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAvKipcbiAgICogVGhlIHNlc3Npb24gY29udGV4dCB1c2VkIGJ5IHRoZSBmb3JlaWduIGhhbmRsZXIuXG4gICAqL1xuICByZWFkb25seSBzZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0IHwgbnVsbDtcblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgZWRpdG9yIHVzZWQgYnkgdGhlIGhpc3Rvcnkgd2lkZ2V0LlxuICAgKi9cbiAgZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsO1xuXG4gIC8qKlxuICAgKiBUaGUgcGxhY2Vob2xkZXIgdGV4dCB0aGF0IGEgaGlzdG9yeSBzZXNzaW9uIGJlZ2FuIHdpdGguXG4gICAqL1xuICByZWFkb25seSBwbGFjZWhvbGRlcjogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHByZXZpb3VzIGl0ZW0gaW4gdGhlIGNvbnNvbGUgaGlzdG9yeS5cbiAgICpcbiAgICogQHBhcmFtIHBsYWNlaG9sZGVyIC0gVGhlIHBsYWNlaG9sZGVyIHN0cmluZyB0aGF0IGdldHMgdGVtcG9yYXJpbHkgYWRkZWRcbiAgICogdG8gdGhlIGhpc3Rvcnkgb25seSBmb3IgdGhlIGR1cmF0aW9uIG9mIG9uZSBoaXN0b3J5IHNlc3Npb24uIElmIG11bHRpcGxlXG4gICAqIHBsYWNlaG9sZGVycyBhcmUgc2VudCB3aXRoaW4gYSBzZXNzaW9uLCBvbmx5IHRoZSBmaXJzdCBvbmUgaXMgYWNjZXB0ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgUHJvbWlzZSBmb3IgY29uc29sZSBjb21tYW5kIHRleHQgb3IgYHVuZGVmaW5lZGAgaWYgdW5hdmFpbGFibGUuXG4gICAqL1xuICBiYWNrKHBsYWNlaG9sZGVyOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz47XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgbmV4dCBpdGVtIGluIHRoZSBjb25zb2xlIGhpc3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbGFjZWhvbGRlciAtIFRoZSBwbGFjZWhvbGRlciBzdHJpbmcgdGhhdCBnZXRzIHRlbXBvcmFyaWx5IGFkZGVkXG4gICAqIHRvIHRoZSBoaXN0b3J5IG9ubHkgZm9yIHRoZSBkdXJhdGlvbiBvZiBvbmUgaGlzdG9yeSBzZXNzaW9uLiBJZiBtdWx0aXBsZVxuICAgKiBwbGFjZWhvbGRlcnMgYXJlIHNlbnQgd2l0aGluIGEgc2Vzc2lvbiwgb25seSB0aGUgZmlyc3Qgb25lIGlzIGFjY2VwdGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIFByb21pc2UgZm9yIGNvbnNvbGUgY29tbWFuZCB0ZXh0IG9yIGB1bmRlZmluZWRgIGlmIHVuYXZhaWxhYmxlLlxuICAgKi9cbiAgZm9yd2FyZChwbGFjZWhvbGRlcjogc3RyaW5nKTogUHJvbWlzZTxzdHJpbmc+O1xuXG4gIC8qKlxuICAgKiBBZGQgYSBuZXcgaXRlbSB0byB0aGUgYm90dG9tIG9mIGhpc3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSBpdGVtIFRoZSBpdGVtIGJlaW5nIGFkZGVkIHRvIHRoZSBib3R0b20gb2YgaGlzdG9yeS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJZiB0aGUgaXRlbSBiZWluZyBhZGRlZCBpcyB1bmRlZmluZWQgb3IgZW1wdHksIGl0IGlzIGlnbm9yZWQuIElmIHRoZSBpdGVtXG4gICAqIGJlaW5nIGFkZGVkIGlzIHRoZSBzYW1lIGFzIHRoZSBsYXN0IGl0ZW0gaW4gaGlzdG9yeSwgaXQgaXMgaWdub3JlZCBhcyB3ZWxsXG4gICAqIHNvIHRoYXQgdGhlIGNvbnNvbGUncyBoaXN0b3J5IHdpbGwgY29uc2lzdCBvZiBubyBjb250aWd1b3VzIHJlcGV0aXRpb25zLlxuICAgKi9cbiAgcHVzaChpdGVtOiBzdHJpbmcpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBSZXNldCB0aGUgaGlzdG9yeSBuYXZpZ2F0aW9uIHN0YXRlLCBpLmUuLCBzdGFydCBhIG5ldyBoaXN0b3J5IHNlc3Npb24uXG4gICAqL1xuICByZXNldCgpOiB2b2lkO1xufVxuXG4vKipcbiAqIEEgY29uc29sZSBoaXN0b3J5IG1hbmFnZXIgb2JqZWN0LlxuICovXG5leHBvcnQgY2xhc3MgQ29uc29sZUhpc3RvcnkgaW1wbGVtZW50cyBJQ29uc29sZUhpc3Rvcnkge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IGNvbnNvbGUgaGlzdG9yeSBvYmplY3QuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBDb25zb2xlSGlzdG9yeS5JT3B0aW9ucykge1xuICAgIGNvbnN0IHsgc2Vzc2lvbkNvbnRleHQgfSA9IG9wdGlvbnM7XG4gICAgaWYgKHNlc3Npb25Db250ZXh0KSB7XG4gICAgICB0aGlzLnNlc3Npb25Db250ZXh0ID0gc2Vzc2lvbkNvbnRleHQ7XG4gICAgICB2b2lkIHRoaXMuX2hhbmRsZUtlcm5lbCgpO1xuICAgICAgdGhpcy5zZXNzaW9uQ29udGV4dC5rZXJuZWxDaGFuZ2VkLmNvbm5lY3QodGhpcy5faGFuZGxlS2VybmVsLCB0aGlzKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIGNsaWVudCBzZXNzaW9uIHVzZWQgYnkgdGhlIGZvcmVpZ24gaGFuZGxlci5cbiAgICovXG4gIHJlYWRvbmx5IHNlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQgfCBudWxsO1xuXG4gIC8qKlxuICAgKiBUaGUgY3VycmVudCBlZGl0b3IgdXNlZCBieSB0aGUgaGlzdG9yeSBtYW5hZ2VyLlxuICAgKi9cbiAgZ2V0IGVkaXRvcigpOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fZWRpdG9yO1xuICB9XG4gIHNldCBlZGl0b3IodmFsdWU6IENvZGVFZGl0b3IuSUVkaXRvciB8IG51bGwpIHtcbiAgICBpZiAodGhpcy5fZWRpdG9yID09PSB2YWx1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHByZXYgPSB0aGlzLl9lZGl0b3I7XG4gICAgaWYgKHByZXYpIHtcbiAgICAgIHByZXYuZWRnZVJlcXVlc3RlZC5kaXNjb25uZWN0KHRoaXMub25FZGdlUmVxdWVzdCwgdGhpcyk7XG4gICAgICBwcmV2Lm1vZGVsLnNoYXJlZE1vZGVsLmNoYW5nZWQuZGlzY29ubmVjdCh0aGlzLm9uVGV4dENoYW5nZSwgdGhpcyk7XG4gICAgfVxuXG4gICAgdGhpcy5fZWRpdG9yID0gdmFsdWU7XG5cbiAgICBpZiAodmFsdWUpIHtcbiAgICAgIHZhbHVlLmVkZ2VSZXF1ZXN0ZWQuY29ubmVjdCh0aGlzLm9uRWRnZVJlcXVlc3QsIHRoaXMpO1xuICAgICAgdmFsdWUubW9kZWwuc2hhcmVkTW9kZWwuY2hhbmdlZC5jb25uZWN0KHRoaXMub25UZXh0Q2hhbmdlLCB0aGlzKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIHBsYWNlaG9sZGVyIHRleHQgdGhhdCBhIGhpc3Rvcnkgc2Vzc2lvbiBiZWdhbiB3aXRoLlxuICAgKi9cbiAgZ2V0IHBsYWNlaG9sZGVyKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX3BsYWNlaG9sZGVyO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB3aGV0aGVyIHRoZSBjb25zb2xlIGhpc3RvcnkgbWFuYWdlciBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBjb25zb2xlIGhpc3RvcnkgbWFuYWdlci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgdGhpcy5faGlzdG9yeS5sZW5ndGggPSAwO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBwcmV2aW91cyBpdGVtIGluIHRoZSBjb25zb2xlIGhpc3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbGFjZWhvbGRlciAtIFRoZSBwbGFjZWhvbGRlciBzdHJpbmcgdGhhdCBnZXRzIHRlbXBvcmFyaWx5IGFkZGVkXG4gICAqIHRvIHRoZSBoaXN0b3J5IG9ubHkgZm9yIHRoZSBkdXJhdGlvbiBvZiBvbmUgaGlzdG9yeSBzZXNzaW9uLiBJZiBtdWx0aXBsZVxuICAgKiBwbGFjZWhvbGRlcnMgYXJlIHNlbnQgd2l0aGluIGEgc2Vzc2lvbiwgb25seSB0aGUgZmlyc3Qgb25lIGlzIGFjY2VwdGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIFByb21pc2UgZm9yIGNvbnNvbGUgY29tbWFuZCB0ZXh0IG9yIGB1bmRlZmluZWRgIGlmIHVuYXZhaWxhYmxlLlxuICAgKi9cbiAgYmFjayhwbGFjZWhvbGRlcjogc3RyaW5nKTogUHJvbWlzZTxzdHJpbmc+IHtcbiAgICBpZiAoIXRoaXMuX2hhc1Nlc3Npb24pIHtcbiAgICAgIHRoaXMuX2hhc1Nlc3Npb24gPSB0cnVlO1xuICAgICAgdGhpcy5fcGxhY2Vob2xkZXIgPSBwbGFjZWhvbGRlcjtcbiAgICAgIC8vIEZpbHRlciB0aGUgaGlzdG9yeSB3aXRoIHRoZSBwbGFjZWhvbGRlciBzdHJpbmcuXG4gICAgICB0aGlzLnNldEZpbHRlcihwbGFjZWhvbGRlcik7XG4gICAgICB0aGlzLl9jdXJzb3IgPSB0aGlzLl9maWx0ZXJlZC5sZW5ndGggLSAxO1xuICAgIH1cblxuICAgIC0tdGhpcy5fY3Vyc29yO1xuICAgIHRoaXMuX2N1cnNvciA9IE1hdGgubWF4KDAsIHRoaXMuX2N1cnNvcik7XG4gICAgY29uc3QgY29udGVudCA9IHRoaXMuX2ZpbHRlcmVkW3RoaXMuX2N1cnNvcl07XG4gICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShjb250ZW50KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIG5leHQgaXRlbSBpbiB0aGUgY29uc29sZSBoaXN0b3J5LlxuICAgKlxuICAgKiBAcGFyYW0gcGxhY2Vob2xkZXIgLSBUaGUgcGxhY2Vob2xkZXIgc3RyaW5nIHRoYXQgZ2V0cyB0ZW1wb3JhcmlseSBhZGRlZFxuICAgKiB0byB0aGUgaGlzdG9yeSBvbmx5IGZvciB0aGUgZHVyYXRpb24gb2Ygb25lIGhpc3Rvcnkgc2Vzc2lvbi4gSWYgbXVsdGlwbGVcbiAgICogcGxhY2Vob2xkZXJzIGFyZSBzZW50IHdpdGhpbiBhIHNlc3Npb24sIG9ubHkgdGhlIGZpcnN0IG9uZSBpcyBhY2NlcHRlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBQcm9taXNlIGZvciBjb25zb2xlIGNvbW1hbmQgdGV4dCBvciBgdW5kZWZpbmVkYCBpZiB1bmF2YWlsYWJsZS5cbiAgICovXG4gIGZvcndhcmQocGxhY2Vob2xkZXI6IHN0cmluZyk6IFByb21pc2U8c3RyaW5nPiB7XG4gICAgaWYgKCF0aGlzLl9oYXNTZXNzaW9uKSB7XG4gICAgICB0aGlzLl9oYXNTZXNzaW9uID0gdHJ1ZTtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyID0gcGxhY2Vob2xkZXI7XG4gICAgICAvLyBGaWx0ZXIgdGhlIGhpc3Rvcnkgd2l0aCB0aGUgcGxhY2Vob2xkZXIgc3RyaW5nLlxuICAgICAgdGhpcy5zZXRGaWx0ZXIocGxhY2Vob2xkZXIpO1xuICAgICAgdGhpcy5fY3Vyc29yID0gdGhpcy5fZmlsdGVyZWQubGVuZ3RoO1xuICAgIH1cblxuICAgICsrdGhpcy5fY3Vyc29yO1xuICAgIHRoaXMuX2N1cnNvciA9IE1hdGgubWluKHRoaXMuX2ZpbHRlcmVkLmxlbmd0aCAtIDEsIHRoaXMuX2N1cnNvcik7XG4gICAgY29uc3QgY29udGVudCA9IHRoaXMuX2ZpbHRlcmVkW3RoaXMuX2N1cnNvcl07XG4gICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShjb250ZW50KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSBuZXcgaXRlbSB0byB0aGUgYm90dG9tIG9mIGhpc3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSBpdGVtIFRoZSBpdGVtIGJlaW5nIGFkZGVkIHRvIHRoZSBib3R0b20gb2YgaGlzdG9yeS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJZiB0aGUgaXRlbSBiZWluZyBhZGRlZCBpcyB1bmRlZmluZWQgb3IgZW1wdHksIGl0IGlzIGlnbm9yZWQuIElmIHRoZSBpdGVtXG4gICAqIGJlaW5nIGFkZGVkIGlzIHRoZSBzYW1lIGFzIHRoZSBsYXN0IGl0ZW0gaW4gaGlzdG9yeSwgaXQgaXMgaWdub3JlZCBhcyB3ZWxsXG4gICAqIHNvIHRoYXQgdGhlIGNvbnNvbGUncyBoaXN0b3J5IHdpbGwgY29uc2lzdCBvZiBubyBjb250aWd1b3VzIHJlcGV0aXRpb25zLlxuICAgKi9cbiAgcHVzaChpdGVtOiBzdHJpbmcpOiB2b2lkIHtcbiAgICBpZiAoaXRlbSAmJiBpdGVtICE9PSB0aGlzLl9oaXN0b3J5W3RoaXMuX2hpc3RvcnkubGVuZ3RoIC0gMV0pIHtcbiAgICAgIHRoaXMuX2hpc3RvcnkucHVzaChpdGVtKTtcbiAgICB9XG4gICAgdGhpcy5yZXNldCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlc2V0IHRoZSBoaXN0b3J5IG5hdmlnYXRpb24gc3RhdGUsIGkuZS4sIHN0YXJ0IGEgbmV3IGhpc3Rvcnkgc2Vzc2lvbi5cbiAgICovXG4gIHJlc2V0KCk6IHZvaWQge1xuICAgIHRoaXMuX2N1cnNvciA9IHRoaXMuX2hpc3RvcnkubGVuZ3RoO1xuICAgIHRoaXMuX2hhc1Nlc3Npb24gPSBmYWxzZTtcbiAgICB0aGlzLl9wbGFjZWhvbGRlciA9ICcnO1xuICB9XG5cbiAgLyoqXG4gICAqIFBvcHVsYXRlIHRoZSBoaXN0b3J5IGNvbGxlY3Rpb24gb24gaGlzdG9yeSByZXBseSBmcm9tIGEga2VybmVsLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgVGhlIGtlcm5lbCBtZXNzYWdlIGhpc3RvcnkgcmVwbHkuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogSGlzdG9yeSBlbnRyaWVzIGhhdmUgdGhlIHNoYXBlOlxuICAgKiBbc2Vzc2lvbjogbnVtYmVyLCBsaW5lOiBudW1iZXIsIGlucHV0OiBzdHJpbmddXG4gICAqIENvbnRpZ3VvdXMgZHVwbGljYXRlcyBhcmUgc3RyaXBwZWQgb3V0IG9mIHRoZSBBUEkgcmVzcG9uc2UuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25IaXN0b3J5KHZhbHVlOiBLZXJuZWxNZXNzYWdlLklIaXN0b3J5UmVwbHlNc2cpOiB2b2lkIHtcbiAgICB0aGlzLl9oaXN0b3J5Lmxlbmd0aCA9IDA7XG4gICAgbGV0IGxhc3QgPSAnJztcbiAgICBsZXQgY3VycmVudCA9ICcnO1xuICAgIGlmICh2YWx1ZS5jb250ZW50LnN0YXR1cyA9PT0gJ29rJykge1xuICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCB2YWx1ZS5jb250ZW50Lmhpc3RvcnkubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgY3VycmVudCA9ICh2YWx1ZS5jb250ZW50Lmhpc3RvcnlbaV0gYXMgc3RyaW5nW10pWzJdO1xuICAgICAgICBpZiAoY3VycmVudCAhPT0gbGFzdCkge1xuICAgICAgICAgIHRoaXMuX2hpc3RvcnkucHVzaCgobGFzdCA9IGN1cnJlbnQpKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICAvLyBSZXNldCB0aGUgaGlzdG9yeSBuYXZpZ2F0aW9uIGN1cnNvciBiYWNrIHRvIHRoZSBib3R0b20uXG4gICAgdGhpcy5fY3Vyc29yID0gdGhpcy5faGlzdG9yeS5sZW5ndGg7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgdGV4dCBjaGFuZ2Ugc2lnbmFsIGZyb20gdGhlIGVkaXRvci5cbiAgICovXG4gIHByb3RlY3RlZCBvblRleHRDaGFuZ2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX3NldEJ5SGlzdG9yeSkge1xuICAgICAgdGhpcy5fc2V0QnlIaXN0b3J5ID0gZmFsc2U7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMucmVzZXQoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYW4gZWRnZSByZXF1ZXN0ZWQgc2lnbmFsLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uRWRnZVJlcXVlc3QoXG4gICAgZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3IsXG4gICAgbG9jYXRpb246IENvZGVFZGl0b3IuRWRnZUxvY2F0aW9uXG4gICk6IHZvaWQge1xuICAgIGNvbnN0IHNoYXJlZE1vZGVsID0gZWRpdG9yLm1vZGVsLnNoYXJlZE1vZGVsO1xuICAgIGNvbnN0IHNvdXJjZSA9IHNoYXJlZE1vZGVsLmdldFNvdXJjZSgpO1xuXG4gICAgaWYgKGxvY2F0aW9uID09PSAndG9wJyB8fCBsb2NhdGlvbiA9PT0gJ3RvcExpbmUnKSB7XG4gICAgICB2b2lkIHRoaXMuYmFjayhzb3VyY2UpLnRoZW4odmFsdWUgPT4ge1xuICAgICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkIHx8ICF2YWx1ZSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBpZiAoc2hhcmVkTW9kZWwuZ2V0U291cmNlKCkgPT09IHZhbHVlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuX3NldEJ5SGlzdG9yeSA9IHRydWU7XG4gICAgICAgIHNoYXJlZE1vZGVsLnNldFNvdXJjZSh2YWx1ZSk7XG4gICAgICAgIGxldCBjb2x1bW5Qb3MgPSAwO1xuICAgICAgICBjb2x1bW5Qb3MgPSB2YWx1ZS5pbmRleE9mKCdcXG4nKTtcbiAgICAgICAgaWYgKGNvbHVtblBvcyA8IDApIHtcbiAgICAgICAgICBjb2x1bW5Qb3MgPSB2YWx1ZS5sZW5ndGg7XG4gICAgICAgIH1cbiAgICAgICAgZWRpdG9yLnNldEN1cnNvclBvc2l0aW9uKHsgbGluZTogMCwgY29sdW1uOiBjb2x1bW5Qb3MgfSk7XG4gICAgICB9KTtcbiAgICB9IGVsc2Uge1xuICAgICAgdm9pZCB0aGlzLmZvcndhcmQoc291cmNlKS50aGVuKHZhbHVlID0+IHtcbiAgICAgICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCB0ZXh0ID0gdmFsdWUgfHwgdGhpcy5wbGFjZWhvbGRlcjtcbiAgICAgICAgaWYgKHNoYXJlZE1vZGVsLmdldFNvdXJjZSgpID09PSB0ZXh0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuX3NldEJ5SGlzdG9yeSA9IHRydWU7XG4gICAgICAgIHNoYXJlZE1vZGVsLnNldFNvdXJjZSh0ZXh0KTtcbiAgICAgICAgY29uc3QgcG9zID0gZWRpdG9yLmdldFBvc2l0aW9uQXQodGV4dC5sZW5ndGgpO1xuICAgICAgICBpZiAocG9zKSB7XG4gICAgICAgICAgZWRpdG9yLnNldEN1cnNvclBvc2l0aW9uKHBvcyk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGN1cnJlbnQga2VybmVsIGNoYW5naW5nLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfaGFuZGxlS2VybmVsKCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IGtlcm5lbCA9IHRoaXMuc2Vzc2lvbkNvbnRleHQ/LnNlc3Npb24/Lmtlcm5lbDtcbiAgICBpZiAoIWtlcm5lbCkge1xuICAgICAgdGhpcy5faGlzdG9yeS5sZW5ndGggPSAwO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHJldHVybiBrZXJuZWwucmVxdWVzdEhpc3RvcnkoUHJpdmF0ZS5pbml0aWFsUmVxdWVzdCkudGhlbih2ID0+IHtcbiAgICAgIHRoaXMub25IaXN0b3J5KHYpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgZmlsdGVyIGRhdGEuXG4gICAqXG4gICAqIEBwYXJhbSBmaWx0ZXJTdHIgLSBUaGUgc3RyaW5nIHRvIHVzZSB3aGVuIGZpbHRlcmluZyB0aGUgZGF0YS5cbiAgICovXG4gIHByb3RlY3RlZCBzZXRGaWx0ZXIoZmlsdGVyU3RyOiBzdHJpbmcgPSAnJyk6IHZvaWQge1xuICAgIC8vIEFwcGx5IHRoZSBuZXcgZmlsdGVyIGFuZCByZW1vdmUgY29udGlndW91cyBkdXBsaWNhdGVzLlxuICAgIHRoaXMuX2ZpbHRlcmVkLmxlbmd0aCA9IDA7XG5cbiAgICBsZXQgbGFzdCA9ICcnO1xuICAgIGxldCBjdXJyZW50ID0gJyc7XG5cbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IHRoaXMuX2hpc3RvcnkubGVuZ3RoOyBpKyspIHtcbiAgICAgIGN1cnJlbnQgPSB0aGlzLl9oaXN0b3J5W2ldO1xuICAgICAgaWYgKFxuICAgICAgICBjdXJyZW50ICE9PSBsYXN0ICYmXG4gICAgICAgIGZpbHRlclN0ciA9PT0gY3VycmVudC5zbGljZSgwLCBmaWx0ZXJTdHIubGVuZ3RoKVxuICAgICAgKSB7XG4gICAgICAgIHRoaXMuX2ZpbHRlcmVkLnB1c2goKGxhc3QgPSBjdXJyZW50KSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgdGhpcy5fZmlsdGVyZWQucHVzaChmaWx0ZXJTdHIpO1xuICB9XG5cbiAgcHJpdmF0ZSBfY3Vyc29yID0gMDtcbiAgcHJpdmF0ZSBfaGFzU2Vzc2lvbiA9IGZhbHNlO1xuICBwcml2YXRlIF9oaXN0b3J5OiBzdHJpbmdbXSA9IFtdO1xuICBwcml2YXRlIF9wbGFjZWhvbGRlcjogc3RyaW5nID0gJyc7XG4gIHByaXZhdGUgX3NldEJ5SGlzdG9yeSA9IGZhbHNlO1xuICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG4gIHByaXZhdGUgX2VkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX2ZpbHRlcmVkOiBzdHJpbmdbXSA9IFtdO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBDb25zb2xlSGlzdG9yeSBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIENvbnNvbGVIaXN0b3J5IHtcbiAgLyoqXG4gICAqIFRoZSBpbml0aWFsaXphdGlvbiBvcHRpb25zIGZvciBhIGNvbnNvbGUgaGlzdG9yeSBvYmplY3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY2xpZW50IHNlc3Npb24gdXNlZCBieSB0aGUgZm9yZWlnbiBoYW5kbGVyLlxuICAgICAqL1xuICAgIHNlc3Npb25Db250ZXh0PzogSVNlc3Npb25Db250ZXh0O1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICBleHBvcnQgY29uc3QgaW5pdGlhbFJlcXVlc3Q6IEtlcm5lbE1lc3NhZ2UuSUhpc3RvcnlSZXF1ZXN0TXNnWydjb250ZW50J10gPSB7XG4gICAgb3V0cHV0OiBmYWxzZSxcbiAgICByYXc6IHRydWUsXG4gICAgaGlzdF9hY2Nlc3NfdHlwZTogJ3RhaWwnLFxuICAgIG46IDUwMFxuICB9O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY29uc29sZVxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vZm9yZWlnbic7XG5leHBvcnQgKiBmcm9tICcuL2hpc3RvcnknO1xuZXhwb3J0ICogZnJvbSAnLi9wYW5lbCc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7XG4gIElTZXNzaW9uQ29udGV4dCxcbiAgTWFpbkFyZWFXaWRnZXQsXG4gIFNlc3Npb25Db250ZXh0LFxuICBTZXNzaW9uQ29udGV4dERpYWxvZ3Ncbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSUVkaXRvck1pbWVUeXBlU2VydmljZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHsgUGF0aEV4dCwgVGltZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICBSZW5kZXJNaW1lUmVnaXN0cnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBTZXJ2aWNlTWFuYWdlciB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGNvbnNvbGVJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBUb2tlbiwgVVVJRCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBQYW5lbCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBDb2RlQ29uc29sZSB9IGZyb20gJy4vd2lkZ2V0JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBjb25zb2xlIHBhbmVscy5cbiAqL1xuY29uc3QgUEFORUxfQ0xBU1MgPSAnanAtQ29uc29sZVBhbmVsJztcblxuLyoqXG4gKiBBIHBhbmVsIHdoaWNoIGNvbnRhaW5zIGEgY29uc29sZSBhbmQgdGhlIGFiaWxpdHkgdG8gYWRkIG90aGVyIGNoaWxkcmVuLlxuICovXG5leHBvcnQgY2xhc3MgQ29uc29sZVBhbmVsIGV4dGVuZHMgTWFpbkFyZWFXaWRnZXQ8UGFuZWw+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIGNvbnNvbGUgcGFuZWwuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBDb25zb2xlUGFuZWwuSU9wdGlvbnMpIHtcbiAgICBzdXBlcih7IGNvbnRlbnQ6IG5ldyBQYW5lbCgpIH0pO1xuICAgIHRoaXMuYWRkQ2xhc3MoUEFORUxfQ0xBU1MpO1xuICAgIGxldCB7XG4gICAgICByZW5kZXJtaW1lLFxuICAgICAgbWltZVR5cGVTZXJ2aWNlLFxuICAgICAgcGF0aCxcbiAgICAgIGJhc2VQYXRoLFxuICAgICAgbmFtZSxcbiAgICAgIG1hbmFnZXIsXG4gICAgICBtb2RlbEZhY3RvcnksXG4gICAgICBzZXNzaW9uQ29udGV4dCxcbiAgICAgIHRyYW5zbGF0b3JcbiAgICB9ID0gb3B0aW9ucztcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGNvbnN0IGNvbnRlbnRGYWN0b3J5ID0gKHRoaXMuY29udGVudEZhY3RvcnkgPSBvcHRpb25zLmNvbnRlbnRGYWN0b3J5KTtcbiAgICBjb25zdCBjb3VudCA9IFByaXZhdGUuY291bnQrKztcbiAgICBpZiAoIXBhdGgpIHtcbiAgICAgIHBhdGggPSBQYXRoRXh0LmpvaW4oYmFzZVBhdGggfHwgJycsIGBjb25zb2xlLSR7Y291bnR9LSR7VVVJRC51dWlkNCgpfWApO1xuICAgIH1cblxuICAgIHNlc3Npb25Db250ZXh0ID0gdGhpcy5fc2Vzc2lvbkNvbnRleHQgPVxuICAgICAgc2Vzc2lvbkNvbnRleHQgPz9cbiAgICAgIG5ldyBTZXNzaW9uQ29udGV4dCh7XG4gICAgICAgIHNlc3Npb25NYW5hZ2VyOiBtYW5hZ2VyLnNlc3Npb25zLFxuICAgICAgICBzcGVjc01hbmFnZXI6IG1hbmFnZXIua2VybmVsc3BlY3MsXG4gICAgICAgIHBhdGg6IG1hbmFnZXIuY29udGVudHMubG9jYWxQYXRoKHBhdGgpLFxuICAgICAgICBuYW1lOiBuYW1lIHx8IHRyYW5zLl9fKCdDb25zb2xlICUxJywgY291bnQpLFxuICAgICAgICB0eXBlOiAnY29uc29sZScsXG4gICAgICAgIGtlcm5lbFByZWZlcmVuY2U6IG9wdGlvbnMua2VybmVsUHJlZmVyZW5jZSxcbiAgICAgICAgc2V0QnVzeTogb3B0aW9ucy5zZXRCdXN5XG4gICAgICB9KTtcblxuICAgIGNvbnN0IHJlc29sdmVyID0gbmV3IFJlbmRlck1pbWVSZWdpc3RyeS5VcmxSZXNvbHZlcih7XG4gICAgICBwYXRoLFxuICAgICAgY29udGVudHM6IG1hbmFnZXIuY29udGVudHNcbiAgICB9KTtcbiAgICByZW5kZXJtaW1lID0gcmVuZGVybWltZS5jbG9uZSh7IHJlc29sdmVyIH0pO1xuXG4gICAgdGhpcy5jb25zb2xlID0gY29udGVudEZhY3RvcnkuY3JlYXRlQ29uc29sZSh7XG4gICAgICByZW5kZXJtaW1lLFxuICAgICAgc2Vzc2lvbkNvbnRleHQ6IHNlc3Npb25Db250ZXh0LFxuICAgICAgbWltZVR5cGVTZXJ2aWNlLFxuICAgICAgY29udGVudEZhY3RvcnksXG4gICAgICBtb2RlbEZhY3RvcnksXG4gICAgICB0cmFuc2xhdG9yXG4gICAgfSk7XG4gICAgdGhpcy5jb250ZW50LmFkZFdpZGdldCh0aGlzLmNvbnNvbGUpO1xuXG4gICAgdm9pZCBzZXNzaW9uQ29udGV4dC5pbml0aWFsaXplKCkudGhlbihhc3luYyB2YWx1ZSA9PiB7XG4gICAgICBpZiAodmFsdWUpIHtcbiAgICAgICAgYXdhaXQgKFxuICAgICAgICAgIG9wdGlvbnMuc2Vzc2lvbkRpYWxvZ3MgPz8gbmV3IFNlc3Npb25Db250ZXh0RGlhbG9ncyh7IHRyYW5zbGF0b3IgfSlcbiAgICAgICAgKS5zZWxlY3RLZXJuZWwoc2Vzc2lvbkNvbnRleHQhKTtcbiAgICAgIH1cbiAgICAgIHRoaXMuX2Nvbm5lY3RlZCA9IG5ldyBEYXRlKCk7XG4gICAgICB0aGlzLl91cGRhdGVUaXRsZVBhbmVsKCk7XG4gICAgfSk7XG5cbiAgICB0aGlzLmNvbnNvbGUuZXhlY3V0ZWQuY29ubmVjdCh0aGlzLl9vbkV4ZWN1dGVkLCB0aGlzKTtcbiAgICB0aGlzLl91cGRhdGVUaXRsZVBhbmVsKCk7XG4gICAgc2Vzc2lvbkNvbnRleHQua2VybmVsQ2hhbmdlZC5jb25uZWN0KHRoaXMuX3VwZGF0ZVRpdGxlUGFuZWwsIHRoaXMpO1xuICAgIHNlc3Npb25Db250ZXh0LnByb3BlcnR5Q2hhbmdlZC5jb25uZWN0KHRoaXMuX3VwZGF0ZVRpdGxlUGFuZWwsIHRoaXMpO1xuXG4gICAgdGhpcy50aXRsZS5pY29uID0gY29uc29sZUljb247XG4gICAgdGhpcy50aXRsZS5jbG9zYWJsZSA9IHRydWU7XG4gICAgdGhpcy5pZCA9IGBjb25zb2xlLSR7Y291bnR9YDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIGNvbnNvbGUgcGFuZWwuXG4gICAqL1xuICByZWFkb25seSBjb250ZW50RmFjdG9yeTogQ29uc29sZVBhbmVsLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogVGhlIGNvbnNvbGUgd2lkZ2V0IHVzZWQgYnkgdGhlIHBhbmVsLlxuICAgKi9cbiAgY29uc29sZTogQ29kZUNvbnNvbGU7XG5cbiAgLyoqXG4gICAqIFRoZSBzZXNzaW9uIHVzZWQgYnkgdGhlIHBhbmVsLlxuICAgKi9cbiAgZ2V0IHNlc3Npb25Db250ZXh0KCk6IElTZXNzaW9uQ29udGV4dCB7XG4gICAgcmV0dXJuIHRoaXMuX3Nlc3Npb25Db250ZXh0O1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIHRoaXMuc2Vzc2lvbkNvbnRleHQuZGlzcG9zZSgpO1xuICAgIHRoaXMuY29uc29sZS5kaXNwb3NlKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FjdGl2YXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2YXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBjb25zdCBwcm9tcHQgPSB0aGlzLmNvbnNvbGUucHJvbXB0Q2VsbDtcbiAgICBpZiAocHJvbXB0KSB7XG4gICAgICBwcm9tcHQuZWRpdG9yIS5mb2N1cygpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdjbG9zZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25DbG9zZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgc3VwZXIub25DbG9zZVJlcXVlc3QobXNnKTtcbiAgICB0aGlzLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjb25zb2xlIGV4ZWN1dGlvbi5cbiAgICovXG4gIHByaXZhdGUgX29uRXhlY3V0ZWQoc2VuZGVyOiBDb2RlQ29uc29sZSwgYXJnczogRGF0ZSkge1xuICAgIHRoaXMuX2V4ZWN1dGVkID0gYXJncztcbiAgICB0aGlzLl91cGRhdGVUaXRsZVBhbmVsKCk7XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBjb25zb2xlIHBhbmVsIHRpdGxlLlxuICAgKi9cbiAgcHJpdmF0ZSBfdXBkYXRlVGl0bGVQYW5lbCgpOiB2b2lkIHtcbiAgICBQcml2YXRlLnVwZGF0ZVRpdGxlKHRoaXMsIHRoaXMuX2Nvbm5lY3RlZCwgdGhpcy5fZXhlY3V0ZWQsIHRoaXMudHJhbnNsYXRvcik7XG4gIH1cblxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfZXhlY3V0ZWQ6IERhdGUgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfY29ubmVjdGVkOiBEYXRlIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX3Nlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQ7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIENvbnNvbGVQYW5lbCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIENvbnNvbGVQYW5lbCB7XG4gIC8qKlxuICAgKiBUaGUgaW5pdGlhbGl6YXRpb24gb3B0aW9ucyBmb3IgYSBjb25zb2xlIHBhbmVsLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIHJlbmRlcm1pbWUgaW5zdGFuY2UgdXNlZCBieSB0aGUgcGFuZWwuXG4gICAgICovXG4gICAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjb250ZW50IGZhY3RvcnkgZm9yIHRoZSBwYW5lbC5cbiAgICAgKi9cbiAgICBjb250ZW50RmFjdG9yeTogSUNvbnRlbnRGYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHNlcnZpY2UgbWFuYWdlciB1c2VkIGJ5IHRoZSBwYW5lbC5cbiAgICAgKi9cbiAgICBtYW5hZ2VyOiBTZXJ2aWNlTWFuYWdlci5JTWFuYWdlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBwYXRoIG9mIGFuIGV4aXN0aW5nIGNvbnNvbGUuXG4gICAgICovXG4gICAgcGF0aD86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBiYXNlIHBhdGggZm9yIGEgbmV3IGNvbnNvbGUuXG4gICAgICovXG4gICAgYmFzZVBhdGg/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZSBvZiB0aGUgY29uc29sZS5cbiAgICAgKi9cbiAgICBuYW1lPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQSBrZXJuZWwgcHJlZmVyZW5jZS5cbiAgICAgKi9cbiAgICBrZXJuZWxQcmVmZXJlbmNlPzogSVNlc3Npb25Db250ZXh0LklLZXJuZWxQcmVmZXJlbmNlO1xuXG4gICAgLyoqXG4gICAgICogQW4gZXhpc3Rpbmcgc2Vzc2lvbiBjb250ZXh0IHRvIHVzZS5cbiAgICAgKi9cbiAgICBzZXNzaW9uQ29udGV4dD86IElTZXNzaW9uQ29udGV4dDtcblxuICAgIC8qKlxuICAgICAqIFNlc3Npb24gZGlhbG9ncyB0byB1c2UuXG4gICAgICovXG4gICAgc2Vzc2lvbkRpYWxvZ3M/OiBJU2Vzc2lvbkNvbnRleHQuSURpYWxvZ3M7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbW9kZWwgZmFjdG9yeSBmb3IgdGhlIGNvbnNvbGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIG1vZGVsRmFjdG9yeT86IENvZGVDb25zb2xlLklNb2RlbEZhY3Rvcnk7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2VydmljZSB1c2VkIHRvIGxvb2sgdXAgbWltZSB0eXBlcy5cbiAgICAgKi9cbiAgICBtaW1lVHlwZVNlcnZpY2U6IElFZGl0b3JNaW1lVHlwZVNlcnZpY2U7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRvIGNhbGwgd2hlbiB0aGUga2VybmVsIGlzIGJ1c3kuXG4gICAgICovXG4gICAgc2V0QnVzeT86ICgpID0+IElEaXNwb3NhYmxlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb25zb2xlIHBhbmVsIHJlbmRlcmVyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29udGVudEZhY3RvcnkgZXh0ZW5kcyBDb2RlQ29uc29sZS5JQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBjb25zb2xlIHBhbmVsLlxuICAgICAqL1xuICAgIGNyZWF0ZUNvbnNvbGUob3B0aW9uczogQ29kZUNvbnNvbGUuSU9wdGlvbnMpOiBDb2RlQ29uc29sZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIGBJQ29udGVudEZhY3RvcnlgLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIENvbnRlbnRGYWN0b3J5XG4gICAgZXh0ZW5kcyBDb2RlQ29uc29sZS5Db250ZW50RmFjdG9yeVxuICAgIGltcGxlbWVudHMgSUNvbnRlbnRGYWN0b3J5XG4gIHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgY29uc29sZSBwYW5lbC5cbiAgICAgKi9cbiAgICBjcmVhdGVDb25zb2xlKG9wdGlvbnM6IENvZGVDb25zb2xlLklPcHRpb25zKTogQ29kZUNvbnNvbGUge1xuICAgICAgcmV0dXJuIG5ldyBDb2RlQ29uc29sZShvcHRpb25zKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBuYW1lc3BhY2UgZm9yIHRoZSBjb25zb2xlIHBhbmVsIGNvbnRlbnQgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBuYW1lc3BhY2UgQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIE9wdGlvbnMgZm9yIHRoZSBjb2RlIGNvbnNvbGUgY29udGVudCBmYWN0b3J5LlxuICAgICAqL1xuICAgIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMgZXh0ZW5kcyBDb2RlQ29uc29sZS5Db250ZW50RmFjdG9yeS5JT3B0aW9ucyB7fVxuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb25zb2xlIHJlbmRlcmVyIHRva2VuLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IElDb250ZW50RmFjdG9yeSA9IG5ldyBUb2tlbjxJQ29udGVudEZhY3Rvcnk+KFxuICAgICdAanVweXRlcmxhYi9jb25zb2xlOklDb250ZW50RmFjdG9yeScsXG4gICAgJ0EgZmFjdG9yeSBvYmplY3QgdGhhdCBjcmVhdGVzIG5ldyBjb2RlIGNvbnNvbGVzLiBVc2UgdGhpcyBpZiB5b3Ugd2FudCB0byBjcmVhdGUgYW5kIGhvc3QgY29kZSBjb25zb2xlcyBpbiB5b3VyIG93biBVSSBlbGVtZW50cy4nXG4gICk7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogVGhlIGNvdW50ZXIgZm9yIG5ldyBjb25zb2xlcy5cbiAgICovXG4gIGV4cG9ydCBsZXQgY291bnQgPSAxO1xuXG4gIC8qKlxuICAgKiBVcGRhdGUgdGhlIHRpdGxlIG9mIGEgY29uc29sZSBwYW5lbC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiB1cGRhdGVUaXRsZShcbiAgICBwYW5lbDogQ29uc29sZVBhbmVsLFxuICAgIGNvbm5lY3RlZDogRGF0ZSB8IG51bGwsXG4gICAgZXhlY3V0ZWQ6IERhdGUgfCBudWxsLFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiB2b2lkIHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgY29uc3Qgc2Vzc2lvbkNvbnRleHQgPSBwYW5lbC5jb25zb2xlLnNlc3Npb25Db250ZXh0LnNlc3Npb247XG4gICAgaWYgKHNlc3Npb25Db250ZXh0KSB7XG4gICAgICAvLyBGSVhNRTpcbiAgICAgIGxldCBjYXB0aW9uID1cbiAgICAgICAgdHJhbnMuX18oJ05hbWU6ICUxXFxuJywgc2Vzc2lvbkNvbnRleHQubmFtZSkgK1xuICAgICAgICB0cmFucy5fXygnRGlyZWN0b3J5OiAlMVxcbicsIFBhdGhFeHQuZGlybmFtZShzZXNzaW9uQ29udGV4dC5wYXRoKSkgK1xuICAgICAgICB0cmFucy5fXygnS2VybmVsOiAlMScsIHBhbmVsLmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQua2VybmVsRGlzcGxheU5hbWUpO1xuXG4gICAgICBpZiAoY29ubmVjdGVkKSB7XG4gICAgICAgIGNhcHRpb24gKz0gdHJhbnMuX18oXG4gICAgICAgICAgJ1xcbkNvbm5lY3RlZDogJTEnLFxuICAgICAgICAgIFRpbWUuZm9ybWF0KGNvbm5lY3RlZC50b0lTT1N0cmluZygpKVxuICAgICAgICApO1xuICAgICAgfVxuXG4gICAgICBpZiAoZXhlY3V0ZWQpIHtcbiAgICAgICAgY2FwdGlvbiArPSB0cmFucy5fXygnXFxuTGFzdCBFeGVjdXRpb246ICUxJyk7XG4gICAgICB9XG4gICAgICBwYW5lbC50aXRsZS5sYWJlbCA9IHNlc3Npb25Db250ZXh0Lm5hbWU7XG4gICAgICBwYW5lbC50aXRsZS5jYXB0aW9uID0gY2FwdGlvbjtcbiAgICB9IGVsc2Uge1xuICAgICAgcGFuZWwudGl0bGUubGFiZWwgPSB0cmFucy5fXygnQ29uc29sZScpO1xuICAgICAgcGFuZWwudGl0bGUuY2FwdGlvbiA9ICcnO1xuICAgIH1cbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJV2lkZ2V0VHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgQ29uc29sZVBhbmVsIH0gZnJvbSAnLi9wYW5lbCc7XG5cbi8qKlxuICogVGhlIGNvbnNvbGUgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElDb25zb2xlVHJhY2tlciA9IG5ldyBUb2tlbjxJQ29uc29sZVRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvY29uc29sZTpJQ29uc29sZVRyYWNrZXInLFxuICBgQSB3aWRnZXQgdHJhY2tlciBmb3IgY29kZSBjb25zb2xlcy5cbiAgVXNlIHRoaXMgaWYgeW91IHdhbnQgdG8gYmUgYWJsZSB0byBpdGVyYXRlIG92ZXIgYW5kIGludGVyYWN0IHdpdGggY29kZSBjb25zb2xlc1xuICBjcmVhdGVkIGJ5IHRoZSBhcHBsaWNhdGlvbi5gXG4pO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgY29uc29sZSB3aWRnZXRzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElDb25zb2xlVHJhY2tlciBleHRlbmRzIElXaWRnZXRUcmFja2VyPENvbnNvbGVQYW5lbD4ge31cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgUHJlYyB9IGZyb20gJ0Bjb2RlbWlycm9yL3N0YXRlJztcbmltcG9ydCB7IEVkaXRvclZpZXcgfSBmcm9tICdAY29kZW1pcnJvci92aWV3JztcbmltcG9ydCB7IGNyZWF0ZVN0YW5kYWxvbmVDZWxsLCBJU2hhcmVkUmF3Q2VsbCB9IGZyb20gJ0BqdXB5dGVyL3lkb2MnO1xuaW1wb3J0IHsgSVNlc3Npb25Db250ZXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgQXR0YWNobWVudHNDZWxsTW9kZWwsXG4gIENlbGwsXG4gIENlbGxEcmFnVXRpbHMsXG4gIENvZGVDZWxsLFxuICBDb2RlQ2VsbE1vZGVsLFxuICBJQ29kZUNlbGxNb2RlbCxcbiAgSVJhd0NlbGxNb2RlbCxcbiAgaXNDb2RlQ2VsbE1vZGVsLFxuICBSYXdDZWxsLFxuICBSYXdDZWxsTW9kZWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvY2VsbHMnO1xuaW1wb3J0IHsgSUVkaXRvck1pbWVUeXBlU2VydmljZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0ICogYXMgbmJmb3JtYXQgZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgSU9ic2VydmFibGVMaXN0LCBPYnNlcnZhYmxlTGlzdCB9IGZyb20gJ0BqdXB5dGVybGFiL29ic2VydmFibGVzJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IEtlcm5lbE1lc3NhZ2UgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBKU09OT2JqZWN0LCBNaW1lRGF0YSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERyYWcgfSBmcm9tICdAbHVtaW5vL2RyYWdkcm9wJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBQYW5lbCwgUGFuZWxMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBDb25zb2xlSGlzdG9yeSwgSUNvbnNvbGVIaXN0b3J5IH0gZnJvbSAnLi9oaXN0b3J5JztcblxuLyoqXG4gKiBUaGUgZGF0YSBhdHRyaWJ1dGUgYWRkZWQgdG8gYSB3aWRnZXQgdGhhdCBoYXMgYW4gYWN0aXZlIGtlcm5lbC5cbiAqL1xuY29uc3QgS0VSTkVMX1VTRVIgPSAnanBLZXJuZWxVc2VyJztcblxuLyoqXG4gKiBUaGUgZGF0YSBhdHRyaWJ1dGUgYWRkZWQgdG8gYSB3aWRnZXQgY2FuIHJ1biBjb2RlLlxuICovXG5jb25zdCBDT0RFX1JVTk5FUiA9ICdqcENvZGVSdW5uZXInO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGNvbnNvbGUgd2lkZ2V0cy5cbiAqL1xuY29uc3QgQ09OU09MRV9DTEFTUyA9ICdqcC1Db2RlQ29uc29sZSc7XG5cbi8qKlxuICogVGhlIGNsYXNzIGFkZGVkIHRvIGNvbnNvbGUgY2VsbHNcbiAqL1xuY29uc3QgQ09OU09MRV9DRUxMX0NMQVNTID0gJ2pwLUNvbnNvbGUtY2VsbCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gdGhlIGNvbnNvbGUgYmFubmVyLlxuICovXG5jb25zdCBCQU5ORVJfQ0xBU1MgPSAnanAtQ29kZUNvbnNvbGUtYmFubmVyJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBvZiB0aGUgYWN0aXZlIHByb21wdCBjZWxsLlxuICovXG5jb25zdCBQUk9NUFRfQ0xBU1MgPSAnanAtQ29kZUNvbnNvbGUtcHJvbXB0Q2VsbCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgb2YgdGhlIHBhbmVsIHRoYXQgaG9sZHMgY2VsbCBjb250ZW50LlxuICovXG5jb25zdCBDT05URU5UX0NMQVNTID0gJ2pwLUNvZGVDb25zb2xlLWNvbnRlbnQnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIG9mIHRoZSBwYW5lbCB0aGF0IGhvbGRzIHByb21wdHMuXG4gKi9cbmNvbnN0IElOUFVUX0NMQVNTID0gJ2pwLUNvZGVDb25zb2xlLWlucHV0JztcblxuLyoqXG4gKiBUaGUgdGltZW91dCBpbiBtcyBmb3IgZXhlY3V0aW9uIHJlcXVlc3RzIHRvIHRoZSBrZXJuZWwuXG4gKi9cbmNvbnN0IEVYRUNVVElPTl9USU1FT1VUID0gMjUwO1xuXG4vKipcbiAqIFRoZSBtaW1ldHlwZSB1c2VkIGZvciBKdXB5dGVyIGNlbGwgZGF0YS5cbiAqL1xuY29uc3QgSlVQWVRFUl9DRUxMX01JTUUgPSAnYXBwbGljYXRpb24vdm5kLmp1cHl0ZXIuY2VsbHMnO1xuXG4vKipcbiAqIEEgd2lkZ2V0IGNvbnRhaW5pbmcgYSBKdXB5dGVyIGNvbnNvbGUuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhlIENvZGVDb25zb2xlIGNsYXNzIGlzIGludGVuZGVkIHRvIGJlIHVzZWQgd2l0aGluIGEgQ29uc29sZVBhbmVsXG4gKiBpbnN0YW5jZS4gVW5kZXIgbW9zdCBjaXJjdW1zdGFuY2VzLCBpdCBpcyBub3QgaW5zdGFudGlhdGVkIGJ5IHVzZXIgY29kZS5cbiAqL1xuZXhwb3J0IGNsYXNzIENvZGVDb25zb2xlIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIGNvbnNvbGUgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogQ29kZUNvbnNvbGUuSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX3RyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5hZGRDbGFzcyhDT05TT0xFX0NMQVNTKTtcbiAgICB0aGlzLm5vZGUuZGF0YXNldFtLRVJORUxfVVNFUl0gPSAndHJ1ZSc7XG4gICAgdGhpcy5ub2RlLmRhdGFzZXRbQ09ERV9SVU5ORVJdID0gJ3RydWUnO1xuICAgIHRoaXMubm9kZS50YWJJbmRleCA9IC0xOyAvLyBBbGxvdyB0aGUgd2lkZ2V0IHRvIHRha2UgZm9jdXMuXG5cbiAgICAvLyBDcmVhdGUgdGhlIHBhbmVscyB0aGF0IGhvbGQgdGhlIGNvbnRlbnQgYW5kIGlucHV0LlxuICAgIGNvbnN0IGxheW91dCA9ICh0aGlzLmxheW91dCA9IG5ldyBQYW5lbExheW91dCgpKTtcbiAgICB0aGlzLl9jZWxscyA9IG5ldyBPYnNlcnZhYmxlTGlzdDxDZWxsPigpO1xuICAgIHRoaXMuX2NvbnRlbnQgPSBuZXcgUGFuZWwoKTtcbiAgICB0aGlzLl9pbnB1dCA9IG5ldyBQYW5lbCgpO1xuXG4gICAgdGhpcy5jb250ZW50RmFjdG9yeSA9IG9wdGlvbnMuY29udGVudEZhY3Rvcnk7XG4gICAgdGhpcy5tb2RlbEZhY3RvcnkgPSBvcHRpb25zLm1vZGVsRmFjdG9yeSA/PyBDb2RlQ29uc29sZS5kZWZhdWx0TW9kZWxGYWN0b3J5O1xuICAgIHRoaXMucmVuZGVybWltZSA9IG9wdGlvbnMucmVuZGVybWltZTtcbiAgICB0aGlzLnNlc3Npb25Db250ZXh0ID0gb3B0aW9ucy5zZXNzaW9uQ29udGV4dDtcbiAgICB0aGlzLl9taW1lVHlwZVNlcnZpY2UgPSBvcHRpb25zLm1pbWVUeXBlU2VydmljZTtcblxuICAgIC8vIEFkZCB0b3AtbGV2ZWwgQ1NTIGNsYXNzZXMuXG4gICAgdGhpcy5fY29udGVudC5hZGRDbGFzcyhDT05URU5UX0NMQVNTKTtcbiAgICB0aGlzLl9pbnB1dC5hZGRDbGFzcyhJTlBVVF9DTEFTUyk7XG5cbiAgICAvLyBJbnNlcnQgdGhlIGNvbnRlbnQgYW5kIGlucHV0IHBhbmVzIGludG8gdGhlIHdpZGdldC5cbiAgICBsYXlvdXQuYWRkV2lkZ2V0KHRoaXMuX2NvbnRlbnQpO1xuICAgIGxheW91dC5hZGRXaWRnZXQodGhpcy5faW5wdXQpO1xuXG4gICAgdGhpcy5faGlzdG9yeSA9IG5ldyBDb25zb2xlSGlzdG9yeSh7XG4gICAgICBzZXNzaW9uQ29udGV4dDogdGhpcy5zZXNzaW9uQ29udGV4dFxuICAgIH0pO1xuXG4gICAgdm9pZCB0aGlzLl9vbktlcm5lbENoYW5nZWQoKTtcblxuICAgIHRoaXMuc2Vzc2lvbkNvbnRleHQua2VybmVsQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uS2VybmVsQ2hhbmdlZCwgdGhpcyk7XG4gICAgdGhpcy5zZXNzaW9uQ29udGV4dC5zdGF0dXNDaGFuZ2VkLmNvbm5lY3QoXG4gICAgICB0aGlzLl9vbktlcm5lbFN0YXR1c0NoYW5nZWQsXG4gICAgICB0aGlzXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGNvbnNvbGUgZmluaXNoZWQgZXhlY3V0aW5nIGl0cyBwcm9tcHQgY2VsbC5cbiAgICovXG4gIGdldCBleGVjdXRlZCgpOiBJU2lnbmFsPHRoaXMsIERhdGU+IHtcbiAgICByZXR1cm4gdGhpcy5fZXhlY3V0ZWQ7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGEgbmV3IHByb21wdCBjZWxsIGlzIGNyZWF0ZWQuXG4gICAqL1xuICBnZXQgcHJvbXB0Q2VsbENyZWF0ZWQoKTogSVNpZ25hbDx0aGlzLCBDb2RlQ2VsbD4ge1xuICAgIHJldHVybiB0aGlzLl9wcm9tcHRDZWxsQ3JlYXRlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIGNvbnNvbGUuXG4gICAqL1xuICByZWFkb25seSBjb250ZW50RmFjdG9yeTogQ29kZUNvbnNvbGUuSUNvbnRlbnRGYWN0b3J5O1xuXG4gIC8qKlxuICAgKiBUaGUgbW9kZWwgZmFjdG9yeSBmb3IgdGhlIGNvbnNvbGUgd2lkZ2V0LlxuICAgKi9cbiAgcmVhZG9ubHkgbW9kZWxGYWN0b3J5OiBDb2RlQ29uc29sZS5JTW9kZWxGYWN0b3J5O1xuXG4gIC8qKlxuICAgKiBUaGUgcmVuZGVybWltZSBpbnN0YW5jZSB1c2VkIGJ5IHRoZSBjb25zb2xlLlxuICAgKi9cbiAgcmVhZG9ubHkgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcblxuICAvKipcbiAgICogVGhlIGNsaWVudCBzZXNzaW9uIHVzZWQgYnkgdGhlIGNvbnNvbGUuXG4gICAqL1xuICByZWFkb25seSBzZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0O1xuXG4gIC8qKlxuICAgKiBUaGUgY29uZmlndXJhdGlvbiBvcHRpb25zIGZvciB0aGUgdGV4dCBlZGl0b3Igd2lkZ2V0LlxuICAgKi9cbiAgZWRpdG9yQ29uZmlnOiBSZWNvcmQ8c3RyaW5nLCBhbnk+ID0gQ29kZUNvbnNvbGUuZGVmYXVsdEVkaXRvckNvbmZpZztcblxuICAvKipcbiAgICogVGhlIGxpc3Qgb2YgY29udGVudCBjZWxscyBpbiB0aGUgY29uc29sZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGxpc3QgZG9lcyBub3QgaW5jbHVkZSB0aGUgY3VycmVudCBiYW5uZXIgb3IgdGhlIHByb21wdCBmb3IgYSBjb25zb2xlLlxuICAgKiBJdCBtYXkgaW5jbHVkZSBwcmV2aW91cyBiYW5uZXJzIGFzIHJhdyBjZWxscy5cbiAgICovXG4gIGdldCBjZWxscygpOiBJT2JzZXJ2YWJsZUxpc3Q8Q2VsbD4ge1xuICAgIHJldHVybiB0aGlzLl9jZWxscztcbiAgfVxuXG4gIC8qXG4gICAqIFRoZSBjb25zb2xlIGlucHV0IHByb21wdCBjZWxsLlxuICAgKi9cbiAgZ2V0IHByb21wdENlbGwoKTogQ29kZUNlbGwgfCBudWxsIHtcbiAgICBjb25zdCBpbnB1dExheW91dCA9IHRoaXMuX2lucHV0LmxheW91dCBhcyBQYW5lbExheW91dDtcbiAgICByZXR1cm4gKGlucHV0TGF5b3V0LndpZGdldHNbMF0gYXMgQ29kZUNlbGwpIHx8IG51bGw7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgbmV3IGNlbGwgdG8gdGhlIGNvbnRlbnQgcGFuZWwuXG4gICAqXG4gICAqIEBwYXJhbSBjZWxsIC0gVGhlIGNvZGUgY2VsbCB3aWRnZXQgYmVpbmcgYWRkZWQgdG8gdGhlIGNvbnRlbnQgcGFuZWwuXG4gICAqXG4gICAqIEBwYXJhbSBtc2dJZCAtIFRoZSBvcHRpb25hbCBleGVjdXRpb24gbWVzc2FnZSBpZCBmb3IgdGhlIGNlbGwuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaXMgbWVhbnQgZm9yIHVzZSBieSBvdXRzaWRlIGNsYXNzZXMgdGhhdCB3YW50IHRvIGFkZCBjZWxscyB0byBhXG4gICAqIGNvbnNvbGUuIEl0IGlzIGRpc3RpbmN0IGZyb20gdGhlIGBpbmplY3RgIG1ldGhvZCBpbiB0aGF0IGl0IHJlcXVpcmVzXG4gICAqIHJlbmRlcmVkIGNvZGUgY2VsbCB3aWRnZXRzIGFuZCBkb2VzIG5vdCBleGVjdXRlIHRoZW0gKHRob3VnaCBpdCBjYW4gc3RvcmVcbiAgICogdGhlIGV4ZWN1dGlvbiBtZXNzYWdlIGlkKS5cbiAgICovXG4gIGFkZENlbGwoY2VsbDogQ29kZUNlbGwsIG1zZ0lkPzogc3RyaW5nKTogdm9pZCB7XG4gICAgY2VsbC5hZGRDbGFzcyhDT05TT0xFX0NFTExfQ0xBU1MpO1xuICAgIHRoaXMuX2NvbnRlbnQuYWRkV2lkZ2V0KGNlbGwpO1xuICAgIHRoaXMuX2NlbGxzLnB1c2goY2VsbCk7XG4gICAgaWYgKG1zZ0lkKSB7XG4gICAgICB0aGlzLl9tc2dJZHMuc2V0KG1zZ0lkLCBjZWxsKTtcbiAgICAgIHRoaXMuX21zZ0lkQ2VsbHMuc2V0KGNlbGwsIG1zZ0lkKTtcbiAgICB9XG4gICAgY2VsbC5kaXNwb3NlZC5jb25uZWN0KHRoaXMuX29uQ2VsbERpc3Bvc2VkLCB0aGlzKTtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIGJhbm5lciBjZWxsLlxuICAgKi9cbiAgYWRkQmFubmVyKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9iYW5uZXIpIHtcbiAgICAgIC8vIEFuIG9sZCBiYW5uZXIganVzdCBiZWNvbWVzIGEgbm9ybWFsIGNlbGwgbm93LlxuICAgICAgY29uc3QgY2VsbCA9IHRoaXMuX2Jhbm5lcjtcbiAgICAgIHRoaXMuX2NlbGxzLnB1c2godGhpcy5fYmFubmVyKTtcbiAgICAgIGNlbGwuZGlzcG9zZWQuY29ubmVjdCh0aGlzLl9vbkNlbGxEaXNwb3NlZCwgdGhpcyk7XG4gICAgfVxuICAgIC8vIENyZWF0ZSB0aGUgYmFubmVyLlxuICAgIGNvbnN0IG1vZGVsID0gdGhpcy5tb2RlbEZhY3RvcnkuY3JlYXRlUmF3Q2VsbCh7XG4gICAgICBzaGFyZWRNb2RlbDogY3JlYXRlU3RhbmRhbG9uZUNlbGwoe1xuICAgICAgICBjZWxsX3R5cGU6ICdyYXcnLFxuICAgICAgICBzb3VyY2U6ICcuLi4nXG4gICAgICB9KSBhcyBJU2hhcmVkUmF3Q2VsbFxuICAgIH0pO1xuICAgIGNvbnN0IGJhbm5lciA9ICh0aGlzLl9iYW5uZXIgPSBuZXcgUmF3Q2VsbCh7XG4gICAgICBtb2RlbCxcbiAgICAgIGNvbnRlbnRGYWN0b3J5OiB0aGlzLmNvbnRlbnRGYWN0b3J5LFxuICAgICAgcGxhY2Vob2xkZXI6IGZhbHNlLFxuICAgICAgZWRpdG9yQ29uZmlnOiB7XG4gICAgICAgIGF1dG9DbG9zaW5nQnJhY2tldHM6IGZhbHNlLFxuICAgICAgICBjb2RlRm9sZGluZzogZmFsc2UsXG4gICAgICAgIGhpZ2hsaWdodEFjdGl2ZUxpbmU6IGZhbHNlLFxuICAgICAgICBoaWdobGlnaHRUcmFpbGluZ1doaXRlc3BhY2U6IGZhbHNlLFxuICAgICAgICBoaWdobGlnaHRXaGl0ZXNwYWNlOiBmYWxzZSxcbiAgICAgICAgaW5kZW50VW5pdDogJzQnLFxuICAgICAgICBsaW5lTnVtYmVyczogZmFsc2UsXG4gICAgICAgIGxpbmVXcmFwOiB0cnVlLFxuICAgICAgICBtYXRjaEJyYWNrZXRzOiBmYWxzZSxcbiAgICAgICAgcmVhZE9ubHk6IHRydWUsXG4gICAgICAgIHJ1bGVyczogW10sXG4gICAgICAgIHNjcm9sbFBhc3RFbmQ6IGZhbHNlLFxuICAgICAgICBzbWFydEluZGVudDogZmFsc2UsXG4gICAgICAgIHRhYlNpemU6IDQsXG4gICAgICAgIHRoZW1lOiAnanVweXRlcidcbiAgICAgIH1cbiAgICB9KSkuaW5pdGlhbGl6ZVN0YXRlKCk7XG4gICAgYmFubmVyLmFkZENsYXNzKEJBTk5FUl9DTEFTUyk7XG4gICAgYmFubmVyLnJlYWRPbmx5ID0gdHJ1ZTtcbiAgICB0aGlzLl9jb250ZW50LmFkZFdpZGdldChiYW5uZXIpO1xuICB9XG5cbiAgLyoqXG4gICAqIENsZWFyIHRoZSBjb2RlIGNlbGxzLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZCB7XG4gICAgLy8gRGlzcG9zZSBhbGwgdGhlIGNvbnRlbnQgY2VsbHNcbiAgICBjb25zdCBjZWxscyA9IHRoaXMuX2NlbGxzO1xuICAgIHdoaWxlIChjZWxscy5sZW5ndGggPiAwKSB7XG4gICAgICBjZWxscy5nZXQoMCkuZGlzcG9zZSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgY2VsbCB3aXRoIHRoZSBidWlsdC1pbiBmYWN0b3J5LlxuICAgKi9cbiAgY3JlYXRlQ29kZUNlbGwoKTogQ29kZUNlbGwge1xuICAgIGNvbnN0IGZhY3RvcnkgPSB0aGlzLmNvbnRlbnRGYWN0b3J5O1xuICAgIGNvbnN0IG9wdGlvbnMgPSB0aGlzLl9jcmVhdGVDb2RlQ2VsbE9wdGlvbnMoKTtcbiAgICBjb25zdCBjZWxsID0gZmFjdG9yeS5jcmVhdGVDb2RlQ2VsbChvcHRpb25zKTtcbiAgICBjZWxsLnJlYWRPbmx5ID0gdHJ1ZTtcbiAgICBjZWxsLm1vZGVsLm1pbWVUeXBlID0gdGhpcy5fbWltZXR5cGU7XG4gICAgcmV0dXJuIGNlbGw7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgLy8gRG8gbm90aGluZyBpZiBhbHJlYWR5IGRpc3Bvc2VkLlxuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fbXNnSWRDZWxscyA9IG51bGwhO1xuICAgIHRoaXMuX21zZ0lkcyA9IG51bGwhO1xuICAgIHRoaXMuX2hpc3RvcnkuZGlzcG9zZSgpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBFeGVjdXRlIHRoZSBjdXJyZW50IHByb21wdC5cbiAgICpcbiAgICogQHBhcmFtIGZvcmNlIC0gV2hldGhlciB0byBmb3JjZSBleGVjdXRpb24gd2l0aG91dCBjaGVja2luZyBjb2RlXG4gICAqIGNvbXBsZXRlbmVzcy5cbiAgICpcbiAgICogQHBhcmFtIHRpbWVvdXQgLSBUaGUgbGVuZ3RoIG9mIHRpbWUsIGluIG1pbGxpc2Vjb25kcywgdGhhdCB0aGUgZXhlY3V0aW9uXG4gICAqIHNob3VsZCB3YWl0IGZvciB0aGUgQVBJIHRvIGRldGVybWluZSB3aGV0aGVyIGNvZGUgYmVpbmcgc3VibWl0dGVkIGlzXG4gICAqIGluY29tcGxldGUgYmVmb3JlIGF0dGVtcHRpbmcgc3VibWlzc2lvbiBhbnl3YXkuIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGAyNTBgLlxuICAgKi9cbiAgYXN5bmMgZXhlY3V0ZShmb3JjZSA9IGZhbHNlLCB0aW1lb3V0ID0gRVhFQ1VUSU9OX1RJTUVPVVQpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBpZiAodGhpcy5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw/LnN0YXR1cyA9PT0gJ2RlYWQnKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3QgcHJvbXB0Q2VsbCA9IHRoaXMucHJvbXB0Q2VsbDtcbiAgICBpZiAoIXByb21wdENlbGwpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignQ2Fubm90IGV4ZWN1dGUgd2l0aG91dCBhIHByb21wdCBjZWxsJyk7XG4gICAgfVxuICAgIHByb21wdENlbGwubW9kZWwudHJ1c3RlZCA9IHRydWU7XG5cbiAgICBpZiAoZm9yY2UpIHtcbiAgICAgIC8vIENyZWF0ZSBhIG5ldyBwcm9tcHQgY2VsbCBiZWZvcmUga2VybmVsIGV4ZWN1dGlvbiB0byBhbGxvdyB0eXBlYWhlYWQuXG4gICAgICB0aGlzLm5ld1Byb21wdENlbGwoKTtcbiAgICAgIGF3YWl0IHRoaXMuX2V4ZWN1dGUocHJvbXB0Q2VsbCk7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gQ2hlY2sgd2hldGhlciB3ZSBzaG91bGQgZXhlY3V0ZS5cbiAgICBjb25zdCBzaG91bGRFeGVjdXRlID0gYXdhaXQgdGhpcy5fc2hvdWxkRXhlY3V0ZSh0aW1lb3V0KTtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGlmIChzaG91bGRFeGVjdXRlKSB7XG4gICAgICAvLyBDcmVhdGUgYSBuZXcgcHJvbXB0IGNlbGwgYmVmb3JlIGtlcm5lbCBleGVjdXRpb24gdG8gYWxsb3cgdHlwZWFoZWFkLlxuICAgICAgdGhpcy5uZXdQcm9tcHRDZWxsKCk7XG4gICAgICB0aGlzLnByb21wdENlbGwhLmVkaXRvciEuZm9jdXMoKTtcbiAgICAgIGF3YWl0IHRoaXMuX2V4ZWN1dGUocHJvbXB0Q2VsbCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIGFkZCBhIG5ld2xpbmUgaWYgd2Ugc2hvdWxkbid0IGV4ZWN1dGVcbiAgICAgIHByb21wdENlbGwuZWRpdG9yIS5uZXdJbmRlbnRlZExpbmUoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogR2V0IGEgY2VsbCBnaXZlbiBhIG1lc3NhZ2UgaWQuXG4gICAqXG4gICAqIEBwYXJhbSBtc2dJZCAtIFRoZSBtZXNzYWdlIGlkLlxuICAgKi9cbiAgZ2V0Q2VsbChtc2dJZDogc3RyaW5nKTogQ29kZUNlbGwgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB0aGlzLl9tc2dJZHMuZ2V0KG1zZ0lkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbmplY3QgYXJiaXRyYXJ5IGNvZGUgZm9yIHRoZSBjb25zb2xlIHRvIGV4ZWN1dGUgaW1tZWRpYXRlbHkuXG4gICAqXG4gICAqIEBwYXJhbSBjb2RlIC0gVGhlIGNvZGUgY29udGVudHMgb2YgdGhlIGNlbGwgYmVpbmcgaW5qZWN0ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGluZGljYXRlcyB3aGVuIHRoZSBpbmplY3RlZCBjZWxsJ3MgZXhlY3V0aW9uIGVuZHMuXG4gICAqL1xuICBpbmplY3QoY29kZTogc3RyaW5nLCBtZXRhZGF0YTogSlNPTk9iamVjdCA9IHt9KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgY2VsbCA9IHRoaXMuY3JlYXRlQ29kZUNlbGwoKTtcbiAgICBjZWxsLm1vZGVsLnNoYXJlZE1vZGVsLnNldFNvdXJjZShjb2RlKTtcbiAgICBmb3IgKGNvbnN0IGtleSBvZiBPYmplY3Qua2V5cyhtZXRhZGF0YSkpIHtcbiAgICAgIGNlbGwubW9kZWwuc2V0TWV0YWRhdGEoa2V5LCBtZXRhZGF0YVtrZXldKTtcbiAgICB9XG4gICAgdGhpcy5hZGRDZWxsKGNlbGwpO1xuICAgIHJldHVybiB0aGlzLl9leGVjdXRlKGNlbGwpO1xuICB9XG5cbiAgLyoqXG4gICAqIEluc2VydCBhIGxpbmUgYnJlYWsgaW4gdGhlIHByb21wdCBjZWxsLlxuICAgKi9cbiAgaW5zZXJ0TGluZWJyZWFrKCk6IHZvaWQge1xuICAgIGNvbnN0IHByb21wdENlbGwgPSB0aGlzLnByb21wdENlbGw7XG4gICAgaWYgKCFwcm9tcHRDZWxsKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHByb21wdENlbGwuZWRpdG9yIS5uZXdJbmRlbnRlZExpbmUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXBsYWNlcyB0aGUgc2VsZWN0ZWQgdGV4dCBpbiB0aGUgcHJvbXB0IGNlbGwuXG4gICAqXG4gICAqIEBwYXJhbSB0ZXh0IC0gVGhlIHRleHQgdG8gcmVwbGFjZSB0aGUgc2VsZWN0aW9uLlxuICAgKi9cbiAgcmVwbGFjZVNlbGVjdGlvbih0ZXh0OiBzdHJpbmcpOiB2b2lkIHtcbiAgICBjb25zdCBwcm9tcHRDZWxsID0gdGhpcy5wcm9tcHRDZWxsO1xuICAgIGlmICghcHJvbXB0Q2VsbCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBwcm9tcHRDZWxsLmVkaXRvciEucmVwbGFjZVNlbGVjdGlvbj8uKHRleHQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNlcmlhbGl6ZSB0aGUgb3V0cHV0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgb25seSBzZXJpYWxpemVzIHRoZSBjb2RlIGNlbGxzIGFuZCB0aGUgcHJvbXB0IGNlbGwgaWYgaXQgZXhpc3RzLCBhbmRcbiAgICogc2tpcHMgYW55IG9sZCBiYW5uZXIgY2VsbHMuXG4gICAqL1xuICBzZXJpYWxpemUoKTogbmJmb3JtYXQuSUNvZGVDZWxsW10ge1xuICAgIGNvbnN0IGNlbGxzOiBuYmZvcm1hdC5JQ29kZUNlbGxbXSA9IFtdO1xuICAgIGZvciAoY29uc3QgY2VsbCBvZiB0aGlzLl9jZWxscykge1xuICAgICAgY29uc3QgbW9kZWwgPSBjZWxsLm1vZGVsO1xuICAgICAgaWYgKGlzQ29kZUNlbGxNb2RlbChtb2RlbCkpIHtcbiAgICAgICAgY2VsbHMucHVzaChtb2RlbC50b0pTT04oKSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgaWYgKHRoaXMucHJvbXB0Q2VsbCkge1xuICAgICAgY2VsbHMucHVzaCh0aGlzLnByb21wdENlbGwubW9kZWwudG9KU09OKCkpO1xuICAgIH1cbiAgICByZXR1cm4gY2VsbHM7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBtb3VzZWRvd25gIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2V2dE1vdXNlRG93bihldmVudDogTW91c2VFdmVudCk6IHZvaWQge1xuICAgIGNvbnN0IHsgYnV0dG9uLCBzaGlmdEtleSB9ID0gZXZlbnQ7XG5cbiAgICAvLyBXZSBvbmx5IGhhbmRsZSBtYWluIG9yIHNlY29uZGFyeSBidXR0b24gYWN0aW9ucy5cbiAgICBpZiAoXG4gICAgICAhKGJ1dHRvbiA9PT0gMCB8fCBidXR0b24gPT09IDIpIHx8XG4gICAgICAvLyBTaGlmdCByaWdodC1jbGljayBnaXZlcyB0aGUgYnJvd3NlciBkZWZhdWx0IGJlaGF2aW9yLlxuICAgICAgKHNoaWZ0S2V5ICYmIGJ1dHRvbiA9PT0gMilcbiAgICApIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBsZXQgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuICAgIGNvbnN0IGNlbGxGaWx0ZXIgPSAobm9kZTogSFRNTEVsZW1lbnQpID0+XG4gICAgICBub2RlLmNsYXNzTGlzdC5jb250YWlucyhDT05TT0xFX0NFTExfQ0xBU1MpO1xuICAgIGxldCBjZWxsSW5kZXggPSBDZWxsRHJhZ1V0aWxzLmZpbmRDZWxsKHRhcmdldCwgdGhpcy5fY2VsbHMsIGNlbGxGaWx0ZXIpO1xuXG4gICAgaWYgKGNlbGxJbmRleCA9PT0gLTEpIHtcbiAgICAgIC8vIGBldmVudC50YXJnZXRgIHNvbWV0aW1lcyBnaXZlcyBhbiBvcnBoYW5lZCBub2RlIGluXG4gICAgICAvLyBGaXJlZm94IDU3LCB3aGljaCBjYW4gaGF2ZSBgbnVsbGAgYW55d2hlcmUgaW4gaXRzIHBhcmVudCBsaW5lLiBJZiB3ZSBmYWlsXG4gICAgICAvLyB0byBmaW5kIGEgY2VsbCB1c2luZyBgZXZlbnQudGFyZ2V0YCwgdHJ5IGFnYWluIHVzaW5nIGEgdGFyZ2V0XG4gICAgICAvLyByZWNvbnN0cnVjdGVkIGZyb20gdGhlIHBvc2l0aW9uIG9mIHRoZSBjbGljayBldmVudC5cbiAgICAgIHRhcmdldCA9IGRvY3VtZW50LmVsZW1lbnRGcm9tUG9pbnQoXG4gICAgICAgIGV2ZW50LmNsaWVudFgsXG4gICAgICAgIGV2ZW50LmNsaWVudFlcbiAgICAgICkgYXMgSFRNTEVsZW1lbnQ7XG4gICAgICBjZWxsSW5kZXggPSBDZWxsRHJhZ1V0aWxzLmZpbmRDZWxsKHRhcmdldCwgdGhpcy5fY2VsbHMsIGNlbGxGaWx0ZXIpO1xuICAgIH1cblxuICAgIGlmIChjZWxsSW5kZXggPT09IC0xKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3QgY2VsbCA9IHRoaXMuX2NlbGxzLmdldChjZWxsSW5kZXgpO1xuXG4gICAgY29uc3QgdGFyZ2V0QXJlYTogQ2VsbERyYWdVdGlscy5JQ2VsbFRhcmdldEFyZWEgPVxuICAgICAgQ2VsbERyYWdVdGlscy5kZXRlY3RUYXJnZXRBcmVhKGNlbGwsIGV2ZW50LnRhcmdldCBhcyBIVE1MRWxlbWVudCk7XG5cbiAgICBpZiAodGFyZ2V0QXJlYSA9PT0gJ3Byb21wdCcpIHtcbiAgICAgIHRoaXMuX2RyYWdEYXRhID0ge1xuICAgICAgICBwcmVzc1g6IGV2ZW50LmNsaWVudFgsXG4gICAgICAgIHByZXNzWTogZXZlbnQuY2xpZW50WSxcbiAgICAgICAgaW5kZXg6IGNlbGxJbmRleFxuICAgICAgfTtcblxuICAgICAgdGhpcy5fZm9jdXNlZENlbGwgPSBjZWxsO1xuXG4gICAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdtb3VzZXVwJywgdGhpcywgdHJ1ZSk7XG4gICAgICBkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKCdtb3VzZW1vdmUnLCB0aGlzLCB0cnVlKTtcbiAgICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgbW91c2Vtb3ZlYCBldmVudCBvZiB3aWRnZXRcbiAgICovXG4gIHByaXZhdGUgX2V2dE1vdXNlTW92ZShldmVudDogTW91c2VFdmVudCkge1xuICAgIGNvbnN0IGRhdGEgPSB0aGlzLl9kcmFnRGF0YTtcbiAgICBpZiAoXG4gICAgICBkYXRhICYmXG4gICAgICBDZWxsRHJhZ1V0aWxzLnNob3VsZFN0YXJ0RHJhZyhcbiAgICAgICAgZGF0YS5wcmVzc1gsXG4gICAgICAgIGRhdGEucHJlc3NZLFxuICAgICAgICBldmVudC5jbGllbnRYLFxuICAgICAgICBldmVudC5jbGllbnRZXG4gICAgICApXG4gICAgKSB7XG4gICAgICB2b2lkIHRoaXMuX3N0YXJ0RHJhZyhkYXRhLmluZGV4LCBldmVudC5jbGllbnRYLCBldmVudC5jbGllbnRZKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU3RhcnQgYSBkcmFnIGV2ZW50XG4gICAqL1xuICBwcml2YXRlIF9zdGFydERyYWcoXG4gICAgaW5kZXg6IG51bWJlcixcbiAgICBjbGllbnRYOiBudW1iZXIsXG4gICAgY2xpZW50WTogbnVtYmVyXG4gICk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IGNlbGxNb2RlbCA9IHRoaXMuX2ZvY3VzZWRDZWxsIS5tb2RlbCBhcyBJQ29kZUNlbGxNb2RlbDtcbiAgICBjb25zdCBzZWxlY3RlZDogbmJmb3JtYXQuSUNlbGxbXSA9IFtjZWxsTW9kZWwudG9KU09OKCldO1xuXG4gICAgY29uc3QgZHJhZ0ltYWdlID0gQ2VsbERyYWdVdGlscy5jcmVhdGVDZWxsRHJhZ0ltYWdlKFxuICAgICAgdGhpcy5fZm9jdXNlZENlbGwhLFxuICAgICAgc2VsZWN0ZWRcbiAgICApO1xuXG4gICAgdGhpcy5fZHJhZyA9IG5ldyBEcmFnKHtcbiAgICAgIG1pbWVEYXRhOiBuZXcgTWltZURhdGEoKSxcbiAgICAgIGRyYWdJbWFnZSxcbiAgICAgIHByb3Bvc2VkQWN0aW9uOiAnY29weScsXG4gICAgICBzdXBwb3J0ZWRBY3Rpb25zOiAnY29weScsXG4gICAgICBzb3VyY2U6IHRoaXNcbiAgICB9KTtcblxuICAgIHRoaXMuX2RyYWcubWltZURhdGEuc2V0RGF0YShKVVBZVEVSX0NFTExfTUlNRSwgc2VsZWN0ZWQpO1xuICAgIGNvbnN0IHRleHRDb250ZW50ID0gY2VsbE1vZGVsLnNoYXJlZE1vZGVsLmdldFNvdXJjZSgpO1xuICAgIHRoaXMuX2RyYWcubWltZURhdGEuc2V0RGF0YSgndGV4dC9wbGFpbicsIHRleHRDb250ZW50KTtcblxuICAgIHRoaXMuX2ZvY3VzZWRDZWxsID0gbnVsbDtcblxuICAgIGRvY3VtZW50LnJlbW92ZUV2ZW50TGlzdGVuZXIoJ21vdXNlbW92ZScsIHRoaXMsIHRydWUpO1xuICAgIGRvY3VtZW50LnJlbW92ZUV2ZW50TGlzdGVuZXIoJ21vdXNldXAnLCB0aGlzLCB0cnVlKTtcbiAgICByZXR1cm4gdGhpcy5fZHJhZy5zdGFydChjbGllbnRYLCBjbGllbnRZKS50aGVuKCgpID0+IHtcbiAgICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgdGhpcy5fZHJhZyA9IG51bGw7XG4gICAgICB0aGlzLl9kcmFnRGF0YSA9IG51bGw7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLVRoZSBET00gZXZlbnQgc2VudCB0byB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgbWV0aG9kIGltcGxlbWVudHMgdGhlIERPTSBgRXZlbnRMaXN0ZW5lcmAgaW50ZXJmYWNlIGFuZCBpc1xuICAgKiBjYWxsZWQgaW4gcmVzcG9uc2UgdG8gZXZlbnRzIG9uIHRoZSBub3RlYm9vayBwYW5lbCdzIG5vZGUuIEl0IHNob3VsZFxuICAgKiBub3QgYmUgY2FsbGVkIGRpcmVjdGx5IGJ5IHVzZXIgY29kZS5cbiAgICovXG4gIGhhbmRsZUV2ZW50KGV2ZW50OiBFdmVudCk6IHZvaWQge1xuICAgIHN3aXRjaCAoZXZlbnQudHlwZSkge1xuICAgICAgY2FzZSAna2V5ZG93bic6XG4gICAgICAgIHRoaXMuX2V2dEtleURvd24oZXZlbnQgYXMgS2V5Ym9hcmRFdmVudCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnbW91c2Vkb3duJzpcbiAgICAgICAgdGhpcy5fZXZ0TW91c2VEb3duKGV2ZW50IGFzIE1vdXNlRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ21vdXNlbW92ZSc6XG4gICAgICAgIHRoaXMuX2V2dE1vdXNlTW92ZShldmVudCBhcyBNb3VzZUV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdtb3VzZXVwJzpcbiAgICAgICAgdGhpcy5fZXZ0TW91c2VVcChldmVudCBhcyBNb3VzZUV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlcl9hdHRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3Qgbm9kZSA9IHRoaXMubm9kZTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCB0aGlzLCB0cnVlKTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcyk7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgICAvLyBDcmVhdGUgYSBwcm9tcHQgaWYgbmVjZXNzYXJ5LlxuICAgIGlmICghdGhpcy5wcm9tcHRDZWxsKSB7XG4gICAgICB0aGlzLm5ld1Byb21wdENlbGwoKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5wcm9tcHRDZWxsLmVkaXRvciEuZm9jdXMoKTtcbiAgICAgIHRoaXMudXBkYXRlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3Qgbm9kZSA9IHRoaXMubm9kZTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCB0aGlzLCB0cnVlKTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnYWN0aXZhdGUtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWN0aXZhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IGVkaXRvciA9IHRoaXMucHJvbXB0Q2VsbCAmJiB0aGlzLnByb21wdENlbGwuZWRpdG9yO1xuICAgIGlmIChlZGl0b3IpIHtcbiAgICAgIGVkaXRvci5mb2N1cygpO1xuICAgIH1cbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIE1ha2UgYSBuZXcgcHJvbXB0IGNlbGwuXG4gICAqL1xuICBwcm90ZWN0ZWQgbmV3UHJvbXB0Q2VsbCgpOiB2b2lkIHtcbiAgICBsZXQgcHJvbXB0Q2VsbCA9IHRoaXMucHJvbXB0Q2VsbDtcbiAgICBjb25zdCBpbnB1dCA9IHRoaXMuX2lucHV0O1xuXG4gICAgLy8gTWFrZSB0aGUgbGFzdCBwcm9tcHQgcmVhZC1vbmx5LCBjbGVhciBpdHMgc2lnbmFscywgYW5kIG1vdmUgdG8gY29udGVudC5cbiAgICBpZiAocHJvbXB0Q2VsbCkge1xuICAgICAgcHJvbXB0Q2VsbC5yZWFkT25seSA9IHRydWU7XG4gICAgICBwcm9tcHRDZWxsLnJlbW92ZUNsYXNzKFBST01QVF9DTEFTUyk7XG4gICAgICBTaWduYWwuY2xlYXJEYXRhKHByb21wdENlbGwuZWRpdG9yKTtcbiAgICAgIC8vIEVuc3VyZSB0byBjbGVhciB0aGUgY3Vyc29yXG4gICAgICBwcm9tcHRDZWxsLmVkaXRvcj8uYmx1cigpO1xuICAgICAgY29uc3QgY2hpbGQgPSBpbnB1dC53aWRnZXRzWzBdO1xuICAgICAgY2hpbGQucGFyZW50ID0gbnVsbDtcbiAgICAgIHRoaXMuYWRkQ2VsbChwcm9tcHRDZWxsKTtcbiAgICB9XG5cbiAgICAvLyBDcmVhdGUgdGhlIG5ldyBwcm9tcHQgY2VsbC5cbiAgICBjb25zdCBmYWN0b3J5ID0gdGhpcy5jb250ZW50RmFjdG9yeTtcbiAgICBjb25zdCBvcHRpb25zID0gdGhpcy5fY3JlYXRlQ29kZUNlbGxPcHRpb25zKCk7XG4gICAgcHJvbXB0Q2VsbCA9IGZhY3RvcnkuY3JlYXRlQ29kZUNlbGwob3B0aW9ucyk7XG4gICAgcHJvbXB0Q2VsbC5tb2RlbC5taW1lVHlwZSA9IHRoaXMuX21pbWV0eXBlO1xuICAgIHByb21wdENlbGwuYWRkQ2xhc3MoUFJPTVBUX0NMQVNTKTtcblxuICAgIC8vIEFkZCB0aGUgcHJvbXB0IGNlbGwgdG8gdGhlIERPTSwgbWFraW5nIGB0aGlzLnByb21wdENlbGxgIHZhbGlkIGFnYWluLlxuICAgIHRoaXMuX2lucHV0LmFkZFdpZGdldChwcm9tcHRDZWxsKTtcblxuICAgIHRoaXMuX2hpc3RvcnkuZWRpdG9yID0gcHJvbXB0Q2VsbC5lZGl0b3I7XG4gICAgdGhpcy5fcHJvbXB0Q2VsbENyZWF0ZWQuZW1pdChwcm9tcHRDZWxsKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYHVwZGF0ZS1yZXF1ZXN0YCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvblVwZGF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgUHJpdmF0ZS5zY3JvbGxUb0JvdHRvbSh0aGlzLl9jb250ZW50Lm5vZGUpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgYCdrZXlkb3duJ2AgZXZlbnQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9ldnRLZXlEb3duKGV2ZW50OiBLZXlib2FyZEV2ZW50KTogdm9pZCB7XG4gICAgY29uc3QgZWRpdG9yID0gdGhpcy5wcm9tcHRDZWxsICYmIHRoaXMucHJvbXB0Q2VsbC5lZGl0b3I7XG4gICAgaWYgKCFlZGl0b3IpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKGV2ZW50LmtleUNvZGUgPT09IDEzICYmICFlZGl0b3IuaGFzRm9jdXMoKSkge1xuICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICAgIGVkaXRvci5mb2N1cygpO1xuICAgIH0gZWxzZSBpZiAoZXZlbnQua2V5Q29kZSA9PT0gMjcgJiYgZWRpdG9yLmhhc0ZvY3VzKCkpIHtcbiAgICAgIC8vIFNldCB0byBjb21tYW5kIG1vZGVcbiAgICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICBldmVudC5zdG9wUHJvcGFnYXRpb24oKTtcbiAgICAgIHRoaXMubm9kZS5mb2N1cygpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnbW91c2V1cCdgIGV2ZW50IGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0TW91c2VVcChldmVudDogTW91c2VFdmVudCk6IHZvaWQge1xuICAgIGlmIChcbiAgICAgIHRoaXMucHJvbXB0Q2VsbCAmJlxuICAgICAgdGhpcy5wcm9tcHRDZWxsLm5vZGUuY29udGFpbnMoZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50KVxuICAgICkge1xuICAgICAgdGhpcy5wcm9tcHRDZWxsLmVkaXRvciEuZm9jdXMoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogRXhlY3V0ZSB0aGUgY29kZSBpbiB0aGUgY3VycmVudCBwcm9tcHQgY2VsbC5cbiAgICovXG4gIHByaXZhdGUgX2V4ZWN1dGUoY2VsbDogQ29kZUNlbGwpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCBzb3VyY2UgPSBjZWxsLm1vZGVsLnNoYXJlZE1vZGVsLmdldFNvdXJjZSgpO1xuICAgIHRoaXMuX2hpc3RvcnkucHVzaChzb3VyY2UpO1xuICAgIC8vIElmIHRoZSBzb3VyY2Ugb2YgdGhlIGNvbnNvbGUgaXMganVzdCBcImNsZWFyXCIsIGNsZWFyIHRoZSBjb25zb2xlIGFzIHdlXG4gICAgLy8gZG8gaW4gSVB5dGhvbiBvciBRdENvbnNvbGUuXG4gICAgaWYgKHNvdXJjZSA9PT0gJ2NsZWFyJyB8fCBzb3VyY2UgPT09ICclY2xlYXInKSB7XG4gICAgICB0aGlzLmNsZWFyKCk7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKHZvaWQgMCk7XG4gICAgfVxuICAgIGNlbGwubW9kZWwuY29udGVudENoYW5nZWQuY29ubmVjdCh0aGlzLnVwZGF0ZSwgdGhpcyk7XG4gICAgY29uc3Qgb25TdWNjZXNzID0gKHZhbHVlOiBLZXJuZWxNZXNzYWdlLklFeGVjdXRlUmVwbHlNc2cpID0+IHtcbiAgICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgaWYgKHZhbHVlICYmIHZhbHVlLmNvbnRlbnQuc3RhdHVzID09PSAnb2snKSB7XG4gICAgICAgIGNvbnN0IGNvbnRlbnQgPSB2YWx1ZS5jb250ZW50O1xuICAgICAgICAvLyBVc2UgZGVwcmVjYXRlZCBwYXlsb2FkcyBmb3IgYmFja3dhcmRzIGNvbXBhdGliaWxpdHkuXG4gICAgICAgIGlmIChjb250ZW50LnBheWxvYWQgJiYgY29udGVudC5wYXlsb2FkLmxlbmd0aCkge1xuICAgICAgICAgIGNvbnN0IHNldE5leHRJbnB1dCA9IGNvbnRlbnQucGF5bG9hZC5maWx0ZXIoaSA9PiB7XG4gICAgICAgICAgICByZXR1cm4gKGkgYXMgYW55KS5zb3VyY2UgPT09ICdzZXRfbmV4dF9pbnB1dCc7XG4gICAgICAgICAgfSlbMF07XG4gICAgICAgICAgaWYgKHNldE5leHRJbnB1dCkge1xuICAgICAgICAgICAgY29uc3QgdGV4dCA9IChzZXROZXh0SW5wdXQgYXMgYW55KS50ZXh0O1xuICAgICAgICAgICAgLy8gSWdub3JlIHRoZSBgcmVwbGFjZWAgdmFsdWUgYW5kIGFsd2F5cyBzZXQgdGhlIG5leHQgY2VsbC5cbiAgICAgICAgICAgIGNlbGwubW9kZWwuc2hhcmVkTW9kZWwuc2V0U291cmNlKHRleHQpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSBlbHNlIGlmICh2YWx1ZSAmJiB2YWx1ZS5jb250ZW50LnN0YXR1cyA9PT0gJ2Vycm9yJykge1xuICAgICAgICBmb3IgKGNvbnN0IGNlbGwgb2YgdGhpcy5fY2VsbHMpIHtcbiAgICAgICAgICBpZiAoKGNlbGwubW9kZWwgYXMgSUNvZGVDZWxsTW9kZWwpLmV4ZWN1dGlvbkNvdW50ID09PSBudWxsKSB7XG4gICAgICAgICAgICBjZWxsLnNldFByb21wdCgnJyk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgICBjZWxsLm1vZGVsLmNvbnRlbnRDaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICAgIHRoaXMuX2V4ZWN1dGVkLmVtaXQobmV3IERhdGUoKSk7XG4gICAgfTtcbiAgICBjb25zdCBvbkZhaWx1cmUgPSAoKSA9PiB7XG4gICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNlbGwubW9kZWwuY29udGVudENoYW5nZWQuZGlzY29ubmVjdCh0aGlzLnVwZGF0ZSwgdGhpcyk7XG4gICAgICB0aGlzLnVwZGF0ZSgpO1xuICAgIH07XG4gICAgcmV0dXJuIENvZGVDZWxsLmV4ZWN1dGUoY2VsbCwgdGhpcy5zZXNzaW9uQ29udGV4dCkudGhlbihcbiAgICAgIG9uU3VjY2VzcyxcbiAgICAgIG9uRmFpbHVyZVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBjb25zb2xlIGJhc2VkIG9uIHRoZSBrZXJuZWwgaW5mby5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZUluZm8oaW5mbzogS2VybmVsTWVzc2FnZS5JSW5mb1JlcGx5TXNnWydjb250ZW50J10pOiB2b2lkIHtcbiAgICBpZiAoaW5mby5zdGF0dXMgIT09ICdvaycpIHtcbiAgICAgIHRoaXMuX2Jhbm5lciEubW9kZWwuc2hhcmVkTW9kZWwuc2V0U291cmNlKFxuICAgICAgICAnRXJyb3IgaW4gZ2V0dGluZyBrZXJuZWwgYmFubmVyJ1xuICAgICAgKTtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fYmFubmVyIS5tb2RlbC5zaGFyZWRNb2RlbC5zZXRTb3VyY2UoaW5mby5iYW5uZXIpO1xuICAgIGNvbnN0IGxhbmcgPSBpbmZvLmxhbmd1YWdlX2luZm8gYXMgbmJmb3JtYXQuSUxhbmd1YWdlSW5mb01ldGFkYXRhO1xuICAgIHRoaXMuX21pbWV0eXBlID0gdGhpcy5fbWltZVR5cGVTZXJ2aWNlLmdldE1pbWVUeXBlQnlMYW5ndWFnZShsYW5nKTtcbiAgICBpZiAodGhpcy5wcm9tcHRDZWxsKSB7XG4gICAgICB0aGlzLnByb21wdENlbGwubW9kZWwubWltZVR5cGUgPSB0aGlzLl9taW1ldHlwZTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIHRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhIGNvZGUgY2VsbCB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9jcmVhdGVDb2RlQ2VsbE9wdGlvbnMoKTogQ29kZUNlbGwuSU9wdGlvbnMge1xuICAgIGNvbnN0IGNvbnRlbnRGYWN0b3J5ID0gdGhpcy5jb250ZW50RmFjdG9yeTtcbiAgICBjb25zdCBtb2RlbEZhY3RvcnkgPSB0aGlzLm1vZGVsRmFjdG9yeTtcbiAgICBjb25zdCBtb2RlbCA9IG1vZGVsRmFjdG9yeS5jcmVhdGVDb2RlQ2VsbCh7fSk7XG4gICAgY29uc3QgcmVuZGVybWltZSA9IHRoaXMucmVuZGVybWltZTtcbiAgICBjb25zdCBlZGl0b3JDb25maWcgPSB0aGlzLmVkaXRvckNvbmZpZztcblxuICAgIC8vIFN1cHByZXNzIHRoZSBkZWZhdWx0IFwiRW50ZXJcIiBrZXkgaGFuZGxpbmcuXG4gICAgY29uc3Qgb25LZXlEb3duID0gRWRpdG9yVmlldy5kb21FdmVudEhhbmRsZXJzKHtcbiAgICAgIGtleWRvd246IChldmVudDogS2V5Ym9hcmRFdmVudCwgdmlldzogRWRpdG9yVmlldykgPT4ge1xuICAgICAgICBpZiAoZXZlbnQua2V5Q29kZSA9PT0gMTMpIHtcbiAgICAgICAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHJldHVybiB7XG4gICAgICBtb2RlbCxcbiAgICAgIHJlbmRlcm1pbWUsXG4gICAgICBjb250ZW50RmFjdG9yeSxcbiAgICAgIGVkaXRvckNvbmZpZyxcbiAgICAgIGVkaXRvckV4dGVuc2lvbnM6IFtQcmVjLmhpZ2gob25LZXlEb3duKV0sXG4gICAgICBwbGFjZWhvbGRlcjogZmFsc2UsXG4gICAgICB0cmFuc2xhdG9yOiB0aGlzLl90cmFuc2xhdG9yXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgY2VsbCBkaXNwb3NlZCBzaWduYWxzLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25DZWxsRGlzcG9zZWQoc2VuZGVyOiBDZWxsLCBhcmdzOiB2b2lkKTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHRoaXMuX2NlbGxzLnJlbW92ZVZhbHVlKHNlbmRlcik7XG4gICAgICBjb25zdCBtc2dJZCA9IHRoaXMuX21zZ0lkQ2VsbHMuZ2V0KHNlbmRlciBhcyBDb2RlQ2VsbCk7XG4gICAgICBpZiAobXNnSWQpIHtcbiAgICAgICAgdGhpcy5fbXNnSWRDZWxscy5kZWxldGUoc2VuZGVyIGFzIENvZGVDZWxsKTtcbiAgICAgICAgdGhpcy5fbXNnSWRzLmRlbGV0ZShtc2dJZCk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRlc3Qgd2hldGhlciB3ZSBzaG91bGQgZXhlY3V0ZSB0aGUgcHJvbXB0IGNlbGwuXG4gICAqL1xuICBwcml2YXRlIF9zaG91bGRFeGVjdXRlKHRpbWVvdXQ6IG51bWJlcik6IFByb21pc2U8Ym9vbGVhbj4ge1xuICAgIGNvbnN0IHByb21wdENlbGwgPSB0aGlzLnByb21wdENlbGw7XG4gICAgaWYgKCFwcm9tcHRDZWxsKSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKGZhbHNlKTtcbiAgICB9XG4gICAgY29uc3QgbW9kZWwgPSBwcm9tcHRDZWxsLm1vZGVsO1xuICAgIGNvbnN0IGNvZGUgPSBtb2RlbC5zaGFyZWRNb2RlbC5nZXRTb3VyY2UoKTtcbiAgICByZXR1cm4gbmV3IFByb21pc2U8Ym9vbGVhbj4oKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgY29uc3QgdGltZXIgPSBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgcmVzb2x2ZSh0cnVlKTtcbiAgICAgIH0sIHRpbWVvdXQpO1xuICAgICAgY29uc3Qga2VybmVsID0gdGhpcy5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgICBpZiAoIWtlcm5lbCkge1xuICAgICAgICByZXNvbHZlKGZhbHNlKTtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAga2VybmVsXG4gICAgICAgIC5yZXF1ZXN0SXNDb21wbGV0ZSh7IGNvZGUgfSlcbiAgICAgICAgLnRoZW4oaXNDb21wbGV0ZSA9PiB7XG4gICAgICAgICAgY2xlYXJUaW1lb3V0KHRpbWVyKTtcbiAgICAgICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgICByZXNvbHZlKGZhbHNlKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgaWYgKGlzQ29tcGxldGUuY29udGVudC5zdGF0dXMgIT09ICdpbmNvbXBsZXRlJykge1xuICAgICAgICAgICAgcmVzb2x2ZSh0cnVlKTtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICB9XG4gICAgICAgICAgcmVzb2x2ZShmYWxzZSk7XG4gICAgICAgIH0pXG4gICAgICAgIC5jYXRjaCgoKSA9PiB7XG4gICAgICAgICAgcmVzb2x2ZSh0cnVlKTtcbiAgICAgICAgfSk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSBrZXJuZWwuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9vbktlcm5lbENoYW5nZWQoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgdGhpcy5jbGVhcigpO1xuICAgIGlmICh0aGlzLl9iYW5uZXIpIHtcbiAgICAgIHRoaXMuX2Jhbm5lci5kaXNwb3NlKCk7XG4gICAgICB0aGlzLl9iYW5uZXIgPSBudWxsO1xuICAgIH1cbiAgICB0aGlzLmFkZEJhbm5lcigpO1xuICAgIGlmICh0aGlzLnNlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbCkge1xuICAgICAgdGhpcy5faGFuZGxlSW5mbyhhd2FpdCB0aGlzLnNlc3Npb25Db250ZXh0LnNlc3Npb24ua2VybmVsLmluZm8pO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIGtlcm5lbCBzdGF0dXMuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9vbktlcm5lbFN0YXR1c0NoYW5nZWQoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3Qga2VybmVsID0gdGhpcy5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgaWYgKGtlcm5lbD8uc3RhdHVzID09PSAncmVzdGFydGluZycpIHtcbiAgICAgIHRoaXMuYWRkQmFubmVyKCk7XG4gICAgICB0aGlzLl9oYW5kbGVJbmZvKGF3YWl0IGtlcm5lbD8uaW5mbyk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfYmFubmVyOiBSYXdDZWxsIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX2NlbGxzOiBJT2JzZXJ2YWJsZUxpc3Q8Q2VsbD47XG4gIHByaXZhdGUgX2NvbnRlbnQ6IFBhbmVsO1xuICBwcml2YXRlIF9leGVjdXRlZCA9IG5ldyBTaWduYWw8dGhpcywgRGF0ZT4odGhpcyk7XG4gIHByaXZhdGUgX2hpc3Rvcnk6IElDb25zb2xlSGlzdG9yeTtcbiAgcHJpdmF0ZSBfaW5wdXQ6IFBhbmVsO1xuICBwcml2YXRlIF9taW1ldHlwZSA9ICd0ZXh0L3gtaXB5dGhvbic7XG4gIHByaXZhdGUgX21pbWVUeXBlU2VydmljZTogSUVkaXRvck1pbWVUeXBlU2VydmljZTtcbiAgcHJpdmF0ZSBfbXNnSWRzID0gbmV3IE1hcDxzdHJpbmcsIENvZGVDZWxsPigpO1xuICBwcml2YXRlIF9tc2dJZENlbGxzID0gbmV3IE1hcDxDb2RlQ2VsbCwgc3RyaW5nPigpO1xuICBwcml2YXRlIF9wcm9tcHRDZWxsQ3JlYXRlZCA9IG5ldyBTaWduYWw8dGhpcywgQ29kZUNlbGw+KHRoaXMpO1xuICBwcml2YXRlIF9kcmFnRGF0YToge1xuICAgIHByZXNzWDogbnVtYmVyO1xuICAgIHByZXNzWTogbnVtYmVyO1xuICAgIGluZGV4OiBudW1iZXI7XG4gIH0gfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfZHJhZzogRHJhZyB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9mb2N1c2VkQ2VsbDogQ2VsbCB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF90cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgQ29kZUNvbnNvbGUgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb2RlQ29uc29sZSB7XG4gIC8qKlxuICAgKiBUaGUgaW5pdGlhbGl6YXRpb24gb3B0aW9ucyBmb3IgYSBjb25zb2xlIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBjb250ZW50IGZhY3RvcnkgZm9yIHRoZSBjb25zb2xlIHdpZGdldC5cbiAgICAgKi9cbiAgICBjb250ZW50RmFjdG9yeTogSUNvbnRlbnRGYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1vZGVsIGZhY3RvcnkgZm9yIHRoZSBjb25zb2xlIHdpZGdldC5cbiAgICAgKi9cbiAgICBtb2RlbEZhY3Rvcnk/OiBJTW9kZWxGYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1pbWUgcmVuZGVyZXIgZm9yIHRoZSBjb25zb2xlIHdpZGdldC5cbiAgICAgKi9cbiAgICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNsaWVudCBzZXNzaW9uIGZvciB0aGUgY29uc29sZSB3aWRnZXQuXG4gICAgICovXG4gICAgc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBzZXJ2aWNlIHVzZWQgdG8gbG9vayB1cCBtaW1lIHR5cGVzLlxuICAgICAqL1xuICAgIG1pbWVUeXBlU2VydmljZTogSUVkaXRvck1pbWVUeXBlU2VydmljZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBEZWZhdWx0IGNvbnNvbGUgZWRpdG9yIGNvbmZpZ3VyYXRpb25cbiAgICovXG4gIGV4cG9ydCBjb25zdCBkZWZhdWx0RWRpdG9yQ29uZmlnOiBSZWNvcmQ8c3RyaW5nLCBhbnk+ID0ge1xuICAgIGNvZGVGb2xkaW5nOiBmYWxzZSxcbiAgICBsaW5lTnVtYmVyczogZmFsc2VcbiAgfTtcblxuICAvKipcbiAgICogQSBjb250ZW50IGZhY3RvcnkgZm9yIGNvbnNvbGUgY2hpbGRyZW4uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDb250ZW50RmFjdG9yeSBleHRlbmRzIENlbGwuSUNvbnRlbnRGYWN0b3J5IHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgY29kZSBjZWxsIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVDb2RlQ2VsbChvcHRpb25zOiBDb2RlQ2VsbC5JT3B0aW9ucyk6IENvZGVDZWxsO1xuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IHJhdyBjZWxsIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVSYXdDZWxsKG9wdGlvbnM6IFJhd0NlbGwuSU9wdGlvbnMpOiBSYXdDZWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIERlZmF1bHQgaW1wbGVtZW50YXRpb24gb2YgYElDb250ZW50RmFjdG9yeWAuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgQ29udGVudEZhY3RvcnlcbiAgICBleHRlbmRzIENlbGwuQ29udGVudEZhY3RvcnlcbiAgICBpbXBsZW1lbnRzIElDb250ZW50RmFjdG9yeVxuICB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IGNvZGUgY2VsbCB3aWRnZXQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgbm8gY2VsbCBjb250ZW50IGZhY3RvcnkgaXMgcGFzc2VkIGluIHdpdGggdGhlIG9wdGlvbnMsIHRoZSBvbmUgb24gdGhlXG4gICAgICogbm90ZWJvb2sgY29udGVudCBmYWN0b3J5IGlzIHVzZWQuXG4gICAgICovXG4gICAgY3JlYXRlQ29kZUNlbGwob3B0aW9uczogQ29kZUNlbGwuSU9wdGlvbnMpOiBDb2RlQ2VsbCB7XG4gICAgICByZXR1cm4gbmV3IENvZGVDZWxsKG9wdGlvbnMpLmluaXRpYWxpemVTdGF0ZSgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyByYXcgY2VsbCB3aWRnZXQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgbm8gY2VsbCBjb250ZW50IGZhY3RvcnkgaXMgcGFzc2VkIGluIHdpdGggdGhlIG9wdGlvbnMsIHRoZSBvbmUgb24gdGhlXG4gICAgICogbm90ZWJvb2sgY29udGVudCBmYWN0b3J5IGlzIHVzZWQuXG4gICAgICovXG4gICAgY3JlYXRlUmF3Q2VsbChvcHRpb25zOiBSYXdDZWxsLklPcHRpb25zKTogUmF3Q2VsbCB7XG4gICAgICByZXR1cm4gbmV3IFJhd0NlbGwob3B0aW9ucykuaW5pdGlhbGl6ZVN0YXRlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEEgbmFtZXNwYWNlIGZvciB0aGUgY29kZSBjb25zb2xlIGNvbnRlbnQgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBuYW1lc3BhY2UgQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIEFuIGluaXRpYWxpemUgb3B0aW9ucyBmb3IgYENvbnRlbnRGYWN0b3J5YC5cbiAgICAgKi9cbiAgICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIGV4dGVuZHMgQ2VsbC5JQ29udGVudEZhY3Rvcnkge31cbiAgfVxuXG4gIC8qKlxuICAgKiBBIG1vZGVsIGZhY3RvcnkgZm9yIGEgY29uc29sZSB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNb2RlbEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIFRoZSBmYWN0b3J5IGZvciBjb2RlIGNlbGwgY29udGVudC5cbiAgICAgKi9cbiAgICByZWFkb25seSBjb2RlQ2VsbENvbnRlbnRGYWN0b3J5OiBDb2RlQ2VsbE1vZGVsLklDb250ZW50RmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBjb2RlIGNlbGwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIHRoZSBjZWxsLlxuICAgICAqXG4gICAgICogQHJldHVybnMgQSBuZXcgY29kZSBjZWxsLiBJZiBhIHNvdXJjZSBjZWxsIGlzIHByb3ZpZGVkLCB0aGVcbiAgICAgKiAgIG5ldyBjZWxsIHdpbGwgYmUgaW5pdGlhbGl6ZWQgd2l0aCB0aGUgZGF0YSBmcm9tIHRoZSBzb3VyY2UuXG4gICAgICovXG4gICAgY3JlYXRlQ29kZUNlbGwob3B0aW9uczogQ29kZUNlbGxNb2RlbC5JT3B0aW9ucyk6IElDb2RlQ2VsbE1vZGVsO1xuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IHJhdyBjZWxsLlxuICAgICAqXG4gICAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgb3B0aW9ucyB1c2VkIHRvIGNyZWF0ZSB0aGUgY2VsbC5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIEEgbmV3IHJhdyBjZWxsLiBJZiBhIHNvdXJjZSBjZWxsIGlzIHByb3ZpZGVkLCB0aGVcbiAgICAgKiAgIG5ldyBjZWxsIHdpbGwgYmUgaW5pdGlhbGl6ZWQgd2l0aCB0aGUgZGF0YSBmcm9tIHRoZSBzb3VyY2UuXG4gICAgICovXG4gICAgY3JlYXRlUmF3Q2VsbChcbiAgICAgIG9wdGlvbnM6IEF0dGFjaG1lbnRzQ2VsbE1vZGVsLklPcHRpb25zPElTaGFyZWRSYXdDZWxsPlxuICAgICk6IElSYXdDZWxsTW9kZWw7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgaW1wbGVtZW50YXRpb24gb2YgYW4gYElNb2RlbEZhY3RvcnlgLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsRmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGEgbmV3IGNlbGwgbW9kZWwgZmFjdG9yeS5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJTW9kZWxGYWN0b3J5T3B0aW9ucyA9IHt9KSB7XG4gICAgICB0aGlzLmNvZGVDZWxsQ29udGVudEZhY3RvcnkgPVxuICAgICAgICBvcHRpb25zLmNvZGVDZWxsQ29udGVudEZhY3RvcnkgfHwgQ29kZUNlbGxNb2RlbC5kZWZhdWx0Q29udGVudEZhY3Rvcnk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGZhY3RvcnkgZm9yIG91dHB1dCBhcmVhIG1vZGVscy5cbiAgICAgKi9cbiAgICByZWFkb25seSBjb2RlQ2VsbENvbnRlbnRGYWN0b3J5OiBDb2RlQ2VsbE1vZGVsLklDb250ZW50RmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBjb2RlIGNlbGwuXG4gICAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgZGF0YSB0byB1c2UgZm9yIHRoZSBvcmlnaW5hbCBzb3VyY2UgZGF0YS5cbiAgICAgKiBAcmV0dXJucyBBIG5ldyBjb2RlIGNlbGwuIElmIGEgc291cmNlIGNlbGwgaXMgcHJvdmlkZWQsIHRoZVxuICAgIG5ldyBjZWxsIHdpbGwgYmUgaW5pdGlhbGl6ZWQgd2l0aCB0aGUgZGF0YSBmcm9tIHRoZSBzb3VyY2UuXG4gICAgSWYgdGhlIGNvbnRlbnRGYWN0b3J5IGlzIG5vdCBwcm92aWRlZCwgdGhlIGluc3RhbmNlXG4gICAgYGNvZGVDZWxsQ29udGVudEZhY3RvcnlgIHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBjcmVhdGVDb2RlQ2VsbChvcHRpb25zOiBDb2RlQ2VsbE1vZGVsLklPcHRpb25zID0ge30pOiBJQ29kZUNlbGxNb2RlbCB7XG4gICAgICBpZiAoIW9wdGlvbnMuY29udGVudEZhY3RvcnkpIHtcbiAgICAgICAgb3B0aW9ucy5jb250ZW50RmFjdG9yeSA9IHRoaXMuY29kZUNlbGxDb250ZW50RmFjdG9yeTtcbiAgICAgIH1cbiAgICAgIHJldHVybiBuZXcgQ29kZUNlbGxNb2RlbChvcHRpb25zKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgcmF3IGNlbGwuXG4gICAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgZGF0YSB0byB1c2UgZm9yIHRoZSBvcmlnaW5hbCBzb3VyY2UgZGF0YS5cbiAgICAgKiBAcmV0dXJucyBBIG5ldyByYXcgY2VsbC4gSWYgYSBzb3VyY2UgY2VsbCBpcyBwcm92aWRlZCwgdGhlXG4gICAgbmV3IGNlbGwgd2lsbCBiZSBpbml0aWFsaXplZCB3aXRoIHRoZSBkYXRhIGZyb20gdGhlIHNvdXJjZS5cbiAgICAgKi9cbiAgICBjcmVhdGVSYXdDZWxsKFxuICAgICAgb3B0aW9uczogQXR0YWNobWVudHNDZWxsTW9kZWwuSU9wdGlvbnM8SVNoYXJlZFJhd0NlbGw+XG4gICAgKTogSVJhd0NlbGxNb2RlbCB7XG4gICAgICByZXR1cm4gbmV3IFJhd0NlbGxNb2RlbChvcHRpb25zKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGEgYE1vZGVsRmFjdG9yeWAuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNb2RlbEZhY3RvcnlPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZmFjdG9yeSBmb3Igb3V0cHV0IGFyZWEgbW9kZWxzLlxuICAgICAqL1xuICAgIGNvZGVDZWxsQ29udGVudEZhY3Rvcnk/OiBDb2RlQ2VsbE1vZGVsLklDb250ZW50RmFjdG9yeTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBgTW9kZWxGYWN0b3J5YCBpbnN0YW5jZS5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBkZWZhdWx0TW9kZWxGYWN0b3J5ID0gbmV3IE1vZGVsRmFjdG9yeSh7fSk7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGNvbnNvbGUgd2lkZ2V0IHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogSnVtcCB0byB0aGUgYm90dG9tIG9mIGEgbm9kZS5cbiAgICpcbiAgICogQHBhcmFtIG5vZGUgLSBUaGUgc2Nyb2xsYWJsZSBlbGVtZW50LlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHNjcm9sbFRvQm90dG9tKG5vZGU6IEhUTUxFbGVtZW50KTogdm9pZCB7XG4gICAgbm9kZS5zY3JvbGxUb3AgPSBub2RlLnNjcm9sbEhlaWdodCAtIG5vZGUuY2xpZW50SGVpZ2h0O1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=