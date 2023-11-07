"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_outputarea_lib_index_js"],{

/***/ "../packages/outputarea/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/outputarea/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputArea": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.OutputArea),
/* harmony export */   "OutputAreaModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel),
/* harmony export */   "OutputPrompt": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.OutputPrompt),
/* harmony export */   "SimplifiedOutputArea": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.SimplifiedOutputArea),
/* harmony export */   "Stdin": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.Stdin)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./model */ "../packages/outputarea/lib/model.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/outputarea/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module outputarea
 */




/***/ }),

/***/ "../packages/outputarea/lib/model.js":
/*!*******************************************!*\
  !*** ../packages/outputarea/lib/model.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputAreaModel": () => (/* binding */ OutputAreaModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/nbformat */ "webpack/sharing/consume/default/@jupyterlab/nbformat/@jupyterlab/nbformat");
/* harmony import */ var _jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The default implementation of the IOutputAreaModel.
 */
class OutputAreaModel {
    /**
     * Construct a new observable outputs instance.
     */
    constructor(options = {}) {
        /**
         * A flag that is set when we want to clear the output area
         * *after* the next addition to it.
         */
        this.clearNext = false;
        this._lastStream = '';
        this._trusted = false;
        this._isDisposed = false;
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._trusted = !!options.trusted;
        this.contentFactory =
            options.contentFactory || OutputAreaModel.defaultContentFactory;
        this.list = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__.ObservableList();
        if (options.values) {
            for (const value of options.values) {
                const index = this._add(value) - 1;
                const item = this.list.get(index);
                item.changed.connect(this._onGenericChange, this);
            }
        }
        this.list.changed.connect(this._onListChanged, this);
    }
    /**
     * A signal emitted when an item changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * A signal emitted when the list of items changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Get the length of the items in the model.
     */
    get length() {
        return this.list ? this.list.length : 0;
    }
    /**
     * Get whether the model is trusted.
     */
    get trusted() {
        return this._trusted;
    }
    /**
     * Set whether the model is trusted.
     *
     * #### Notes
     * Changing the value will cause all of the models to re-set.
     */
    set trusted(value) {
        if (value === this._trusted) {
            return;
        }
        const trusted = (this._trusted = value);
        for (let i = 0; i < this.list.length; i++) {
            const oldItem = this.list.get(i);
            const value = oldItem.toJSON();
            const item = this._createItem({ value, trusted });
            this.list.set(i, item);
            oldItem.dispose();
        }
    }
    /**
     * Test whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.list.dispose();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal.clearData(this);
    }
    /**
     * Get an item at the specified index.
     */
    get(index) {
        return this.list.get(index);
    }
    /**
     * Set the value at the specified index.
     */
    set(index, value) {
        value = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(value);
        // Normalize stream data.
        Private.normalize(value);
        const item = this._createItem({ value, trusted: this._trusted });
        this.list.set(index, item);
    }
    /**
     * Add an output, which may be combined with previous output.
     *
     * @returns The total number of outputs.
     *
     * #### Notes
     * The output bundle is copied.
     * Contiguous stream outputs of the same `name` are combined.
     */
    add(output) {
        // If we received a delayed clear message, then clear now.
        if (this.clearNext) {
            this.clear();
            this.clearNext = false;
        }
        return this._add(output);
    }
    /**
     * Clear all of the output.
     *
     * @param wait Delay clearing the output until the next message is added.
     */
    clear(wait = false) {
        this._lastStream = '';
        if (wait) {
            this.clearNext = true;
            return;
        }
        for (const item of this.list) {
            item.dispose();
        }
        this.list.clear();
    }
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    fromJSON(values) {
        this.clear();
        for (const value of values) {
            this._add(value);
        }
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        return Array.from((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.map)(this.list, (output) => output.toJSON()));
    }
    /**
     * Add a copy of the item to the list.
     *
     * @returns The list length
     */
    _add(value) {
        const trusted = this._trusted;
        value = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(value);
        // Normalize the value.
        Private.normalize(value);
        // Consolidate outputs if they are stream outputs of the same kind.
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value) &&
            this._lastStream &&
            value.name === this._lastName &&
            this.shouldCombine({
                value,
                lastModel: this.list.get(this.length - 1)
            })) {
            // In order to get a list change event, we add the previous
            // text to the current item and replace the previous item.
            // This also replaces the metadata of the last item.
            this._lastStream += value.text;
            this._lastStream = Private.removeOverwrittenChars(this._lastStream);
            value.text = this._lastStream;
            const item = this._createItem({ value, trusted });
            const index = this.length - 1;
            const prev = this.list.get(index);
            this.list.set(index, item);
            prev.dispose();
            return this.length;
        }
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value)) {
            value.text = Private.removeOverwrittenChars(value.text);
        }
        // Create the new item.
        const item = this._createItem({ value, trusted });
        // Update the stream information.
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value)) {
            this._lastStream = value.text;
            this._lastName = value.name;
        }
        else {
            this._lastStream = '';
        }
        // Add the item to our list and return the new length.
        return this.list.push(item);
    }
    /**
     * Whether a new value should be consolidated with the previous output.
     *
     * This will only be called if the minimal criteria of both being stream
     * messages of the same type.
     */
    shouldCombine(options) {
        return true;
    }
    /**
     * Create an output item and hook up its signals.
     */
    _createItem(options) {
        const factory = this.contentFactory;
        const item = factory.createOutputModel(options);
        return item;
    }
    /**
     * Handle a change to the list.
     */
    _onListChanged(sender, args) {
        switch (args.type) {
            case 'add':
                args.newValues.forEach(item => {
                    item.changed.connect(this._onGenericChange, this);
                });
                break;
            case 'remove':
                args.oldValues.forEach(item => {
                    item.changed.disconnect(this._onGenericChange, this);
                });
                break;
            case 'set':
                args.newValues.forEach(item => {
                    item.changed.connect(this._onGenericChange, this);
                });
                args.oldValues.forEach(item => {
                    item.changed.disconnect(this._onGenericChange, this);
                });
                break;
        }
        this._changed.emit(args);
    }
    /**
     * Handle a change to an item.
     */
    _onGenericChange(itemModel) {
        let idx;
        let item = null;
        for (idx = 0; idx < this.list.length; idx++) {
            item = this.list.get(idx);
            if (item === itemModel) {
                break;
            }
        }
        if (item != null) {
            this._stateChanged.emit(idx);
            this._changed.emit({
                type: 'set',
                newIndex: idx,
                oldIndex: idx,
                oldValues: [item],
                newValues: [item]
            });
        }
    }
}
/**
 * The namespace for OutputAreaModel class statics.
 */
(function (OutputAreaModel) {
    /**
     * The default implementation of a `IModelOutputFactory`.
     */
    class ContentFactory {
        /**
         * Create an output model.
         */
        createOutputModel(options) {
            return new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.OutputModel(options);
        }
    }
    OutputAreaModel.ContentFactory = ContentFactory;
    /**
     * The default output model factory.
     */
    OutputAreaModel.defaultContentFactory = new ContentFactory();
})(OutputAreaModel || (OutputAreaModel = {}));
/**
 * A namespace for module-private functionality.
 */
var Private;
(function (Private) {
    /**
     * Normalize an output.
     */
    function normalize(value) {
        if (_jupyterlab_nbformat__WEBPACK_IMPORTED_MODULE_0__.isStream(value)) {
            if (Array.isArray(value.text)) {
                value.text = value.text.join('\n');
            }
        }
    }
    Private.normalize = normalize;
    /**
     * Remove characters that are overridden by backspace characters.
     */
    function fixBackspace(txt) {
        let tmp = txt;
        do {
            txt = tmp;
            // Cancel out anything-but-newline followed by backspace
            tmp = txt.replace(/[^\n]\x08/gm, ''); // eslint-disable-line no-control-regex
        } while (tmp.length < txt.length);
        return txt;
    }
    /**
     * Remove chunks that should be overridden by the effect of
     * carriage return characters.
     */
    function fixCarriageReturn(txt) {
        txt = txt.replace(/\r+\n/gm, '\n'); // \r followed by \n --> newline
        while (txt.search(/\r[^$]/g) > -1) {
            const base = txt.match(/^(.*)\r+/m)[1];
            let insert = txt.match(/\r+(.*)$/m)[1];
            insert = insert + base.slice(insert.length, base.length);
            txt = txt.replace(/\r+.*$/m, '\r').replace(/^.*\r/m, insert);
        }
        return txt;
    }
    /*
     * Remove characters overridden by backspaces and carriage returns
     */
    function removeOverwrittenChars(text) {
        return fixCarriageReturn(fixBackspace(text));
    }
    Private.removeOverwrittenChars = removeOverwrittenChars;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/outputarea/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/outputarea/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "OutputArea": () => (/* binding */ OutputArea),
/* harmony export */   "OutputPrompt": () => (/* binding */ OutputPrompt),
/* harmony export */   "SimplifiedOutputArea": () => (/* binding */ SimplifiedOutputArea),
/* harmony export */   "Stdin": () => (/* binding */ Stdin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * The class name added to an output area widget.
 */
const OUTPUT_AREA_CLASS = 'jp-OutputArea';
/**
 * The class name added to the direction children of OutputArea
 */
const OUTPUT_AREA_ITEM_CLASS = 'jp-OutputArea-child';
/**
 * The class name added to actual outputs
 */
const OUTPUT_AREA_OUTPUT_CLASS = 'jp-OutputArea-output';
/**
 * The class name added to prompt children of OutputArea.
 */
const OUTPUT_AREA_PROMPT_CLASS = 'jp-OutputArea-prompt';
/**
 * The class name added to OutputPrompt.
 */
const OUTPUT_PROMPT_CLASS = 'jp-OutputPrompt';
/**
 * The class name added to an execution result.
 */
const EXECUTE_CLASS = 'jp-OutputArea-executeResult';
/**
 * The class name added stdin items of OutputArea
 */
const OUTPUT_AREA_STDIN_ITEM_CLASS = 'jp-OutputArea-stdin-item';
/**
 * The class name added to stdin widgets.
 */
const STDIN_CLASS = 'jp-Stdin';
/**
 * The class name added to stdin data prompt nodes.
 */
const STDIN_PROMPT_CLASS = 'jp-Stdin-prompt';
/**
 * The class name added to stdin data input nodes.
 */
const STDIN_INPUT_CLASS = 'jp-Stdin-input';
/**
 * The overlay that can be clicked to switch between output scrolling modes.
 */
const OUTPUT_PROMPT_OVERLAY = 'jp-OutputArea-promptOverlay';
/** ****************************************************************************
 * OutputArea
 ******************************************************************************/
/**
 * An output area widget.
 *
 * #### Notes
 * The widget model must be set separately and can be changed
 * at any time.  Consumers of the widget must account for a
 * `null` model, and may want to listen to the `modelChanged`
 * signal.
 */
class OutputArea extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget {
    /**
     * Construct an output area widget.
     */
    constructor(options) {
        var _a, _b, _c, _d;
        super();
        /**
         * A public signal used to indicate the number of displayed outputs has changed.
         *
         * #### Notes
         * This is useful for parents who want to apply styling based on the number
         * of outputs. Emits the current number of outputs.
         */
        this.outputLengthChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        /**
         * Handle an iopub message.
         */
        this._onIOPub = (msg) => {
            const model = this.model;
            const msgType = msg.header.msg_type;
            let output;
            const transient = (msg.content.transient || {});
            const displayId = transient['display_id'];
            let targets;
            switch (msgType) {
                case 'execute_result':
                case 'display_data':
                case 'stream':
                case 'error':
                    output = { ...msg.content, output_type: msgType };
                    model.add(output);
                    break;
                case 'clear_output': {
                    const wait = msg.content.wait;
                    model.clear(wait);
                    break;
                }
                case 'update_display_data':
                    output = { ...msg.content, output_type: 'display_data' };
                    targets = this._displayIdMap.get(displayId);
                    if (targets) {
                        for (const index of targets) {
                            model.set(index, output);
                        }
                    }
                    break;
                default:
                    break;
            }
            if (displayId && msgType === 'display_data') {
                targets = this._displayIdMap.get(displayId) || [];
                targets.push(model.length - 1);
                this._displayIdMap.set(displayId, targets);
            }
        };
        /**
         * Handle an execute reply message.
         */
        this._onExecuteReply = (msg) => {
            // API responses that contain a pager are special cased and their type
            // is overridden from 'execute_reply' to 'display_data' in order to
            // render output.
            const model = this.model;
            const content = msg.content;
            if (content.status !== 'ok') {
                return;
            }
            const payload = content && content.payload;
            if (!payload || !payload.length) {
                return;
            }
            const pages = payload.filter((i) => i.source === 'page');
            if (!pages.length) {
                return;
            }
            const page = JSON.parse(JSON.stringify(pages[0]));
            const output = {
                output_type: 'display_data',
                data: page.data,
                metadata: {}
            };
            model.add(output);
        };
        this._displayIdMap = new Map();
        this._minHeightTimeout = null;
        this._inputRequested = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._toggleScrolling = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._initialize = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._outputTracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({
            namespace: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.UUID.uuid4()
        });
        this._inputHistoryScope = 'global';
        super.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.PanelLayout();
        this.addClass(OUTPUT_AREA_CLASS);
        this.contentFactory =
            (_a = options.contentFactory) !== null && _a !== void 0 ? _a : OutputArea.defaultContentFactory;
        this.rendermime = options.rendermime;
        this._maxNumberOutputs = (_b = options.maxNumberOutputs) !== null && _b !== void 0 ? _b : Infinity;
        this._translator = (_c = options.translator) !== null && _c !== void 0 ? _c : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._inputHistoryScope = (_d = options.inputHistoryScope) !== null && _d !== void 0 ? _d : 'global';
        const model = (this.model = options.model);
        for (let i = 0; i < Math.min(model.length, this._maxNumberOutputs + 1); i++) {
            const output = model.get(i);
            this._insertOutput(i, output);
        }
        model.changed.connect(this.onModelChanged, this);
        model.stateChanged.connect(this.onStateChanged, this);
        if (options.promptOverlay) {
            this._addPromptOverlay();
        }
    }
    /**
     * Narrow the type of OutputArea's layout prop
     */
    get layout() {
        return super.layout;
    }
    /**
     * A read-only sequence of the children widgets in the output area.
     */
    get widgets() {
        return this.layout.widgets;
    }
    /**
     * The kernel future associated with the output area.
     */
    get future() {
        return this._future;
    }
    set future(value) {
        // Bail if the model is disposed.
        if (this.model.isDisposed) {
            throw Error('Model is disposed');
        }
        if (this._future === value) {
            return;
        }
        if (this._future) {
            this._future.dispose();
        }
        this._future = value;
        this.model.clear();
        // Make sure there were no input widgets.
        if (this.widgets.length) {
            this._clear();
            this.outputLengthChanged.emit(Math.min(this.model.length, this._maxNumberOutputs));
        }
        // Handle published messages.
        value.onIOPub = this._onIOPub;
        // Handle the execute reply.
        value.onReply = this._onExecuteReply;
        // Handle stdin.
        value.onStdin = msg => {
            if (_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.KernelMessage.isInputRequestMsg(msg)) {
                this.onInputRequest(msg, value);
            }
        };
    }
    /**
     * Signal emitted when an output area is requesting an input.
     */
    get inputRequested() {
        return this._inputRequested;
    }
    /**
     * The maximum number of output items to display on top and bottom of cell output.
     *
     * ### Notes
     * It is set to Infinity if no trim is applied.
     */
    get maxNumberOutputs() {
        return this._maxNumberOutputs;
    }
    set maxNumberOutputs(limit) {
        if (limit <= 0) {
            console.warn(`OutputArea.maxNumberOutputs must be strictly positive.`);
            return;
        }
        const lastShown = this._maxNumberOutputs;
        this._maxNumberOutputs = limit;
        if (lastShown < limit) {
            this._showTrimmedOutputs(lastShown);
        }
    }
    /**
     * Dispose of the resources used by the output area.
     */
    dispose() {
        if (this._future) {
            this._future.dispose();
            this._future = null;
        }
        this._displayIdMap.clear();
        this._outputTracker.dispose();
        super.dispose();
    }
    /**
     * Follow changes on the model state.
     */
    onModelChanged(sender, args) {
        switch (args.type) {
            case 'add':
                this._insertOutput(args.newIndex, args.newValues[0]);
                break;
            case 'remove':
                if (this.widgets.length) {
                    // all items removed from model
                    if (this.model.length === 0) {
                        this._clear();
                    }
                    else {
                        // range of items removed from model
                        // remove widgets corresponding to removed model items
                        const startIndex = args.oldIndex;
                        for (let i = 0; i < args.oldValues.length && startIndex < this.widgets.length; ++i) {
                            const widget = this.widgets[startIndex];
                            widget.parent = null;
                            widget.dispose();
                        }
                        // apply item offset to target model item indices in _displayIdMap
                        this._moveDisplayIdIndices(startIndex, args.oldValues.length);
                        // prevent jitter caused by immediate height change
                        this._preventHeightChangeJitter();
                    }
                }
                break;
            case 'set':
                this._setOutput(args.newIndex, args.newValues[0]);
                break;
            default:
                break;
        }
        this.outputLengthChanged.emit(Math.min(this.model.length, this._maxNumberOutputs));
    }
    /**
     * Emitted when user requests toggling of the output scrolling mode.
     */
    get toggleScrolling() {
        return this._toggleScrolling;
    }
    get initialize() {
        return this._initialize;
    }
    /**
     * Add overlay allowing to toggle scrolling.
     */
    _addPromptOverlay() {
        const overlay = document.createElement('div');
        overlay.className = OUTPUT_PROMPT_OVERLAY;
        overlay.addEventListener('click', () => {
            this._toggleScrolling.emit();
        });
        this.node.appendChild(overlay);
        requestAnimationFrame(() => {
            this._initialize.emit();
        });
    }
    /**
     * Update indices in _displayIdMap in response to element remove from model items
     *
     * @param startIndex - The index of first element removed
     *
     * @param count - The number of elements removed from model items
     *
     */
    _moveDisplayIdIndices(startIndex, count) {
        this._displayIdMap.forEach((indices) => {
            const rangeEnd = startIndex + count;
            const numIndices = indices.length;
            // reverse loop in order to prevent removing element affecting the index
            for (let i = numIndices - 1; i >= 0; --i) {
                const index = indices[i];
                // remove model item indices in removed range
                if (index >= startIndex && index < rangeEnd) {
                    indices.splice(i, 1);
                }
                else if (index >= rangeEnd) {
                    // move model item indices that were larger than range end
                    indices[i] -= count;
                }
            }
        });
    }
    /**
     * Follow changes on the output model state.
     */
    onStateChanged(sender, change) {
        const outputLength = Math.min(this.model.length, this._maxNumberOutputs);
        if (change) {
            if (change >= this._maxNumberOutputs) {
                // Bail early
                return;
            }
            this._setOutput(change, this.model.get(change));
        }
        else {
            for (let i = 0; i < outputLength; i++) {
                this._setOutput(i, this.model.get(i));
            }
        }
        this.outputLengthChanged.emit(outputLength);
    }
    /**
     * Clear the widget outputs.
     */
    _clear() {
        // Bail if there is no work to do.
        if (!this.widgets.length) {
            return;
        }
        // Remove all of our widgets.
        const length = this.widgets.length;
        for (let i = 0; i < length; i++) {
            const widget = this.widgets[0];
            widget.parent = null;
            widget.dispose();
        }
        // Clear the display id map.
        this._displayIdMap.clear();
        // prevent jitter caused by immediate height change
        this._preventHeightChangeJitter();
    }
    _preventHeightChangeJitter() {
        // When an output area is cleared and then quickly replaced with new
        // content (as happens with @interact in widgets, for example), the
        // quickly changing height can make the page jitter.
        // We introduce a small delay in the minimum height
        // to prevent this jitter.
        const rect = this.node.getBoundingClientRect();
        this.node.style.minHeight = `${rect.height}px`;
        if (this._minHeightTimeout) {
            window.clearTimeout(this._minHeightTimeout);
        }
        this._minHeightTimeout = window.setTimeout(() => {
            if (this.isDisposed) {
                return;
            }
            this.node.style.minHeight = '';
        }, 50);
    }
    /**
     * Handle an input request from a kernel.
     */
    onInputRequest(msg, future) {
        // Add an output widget to the end.
        const factory = this.contentFactory;
        const stdinPrompt = msg.content.prompt;
        const password = msg.content.password;
        const panel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Panel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        panel.addClass(OUTPUT_AREA_STDIN_ITEM_CLASS);
        const prompt = factory.createOutputPrompt();
        prompt.addClass(OUTPUT_AREA_PROMPT_CLASS);
        panel.addWidget(prompt);
        const input = factory.createStdin({
            parent_header: msg.header,
            prompt: stdinPrompt,
            password,
            future,
            translator: this._translator,
            inputHistoryScope: this._inputHistoryScope
        });
        input.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(input);
        // Increase number of outputs to display the result up to the input request.
        if (this.model.length >= this.maxNumberOutputs) {
            this.maxNumberOutputs = this.model.length;
        }
        this.layout.addWidget(panel);
        this._inputRequested.emit();
        /**
         * Wait for the stdin to complete, add it to the model (so it persists)
         * and remove the stdin widget.
         */
        void input.value.then(value => {
            // Increase number of outputs to display the result of stdin if needed.
            if (this.model.length >= this.maxNumberOutputs) {
                this.maxNumberOutputs = this.model.length + 1;
            }
            // Use stdin as the stream so it does not get combined with stdout.
            this.model.add({
                output_type: 'stream',
                name: 'stdin',
                text: value + '\n'
            });
            panel.dispose();
        });
    }
    /**
     * Update an output in the layout in place.
     */
    _setOutput(index, model) {
        if (index >= this._maxNumberOutputs) {
            return;
        }
        const panel = this.layout.widgets[index];
        const renderer = (panel.widgets ? panel.widgets[1] : panel);
        // Check whether it is safe to reuse renderer:
        // - Preferred mime type has not changed
        // - Isolation has not changed
        const mimeType = this.rendermime.preferredMimeType(model.data, model.trusted ? 'any' : 'ensure');
        if (Private.currentPreferredMimetype.get(renderer) === mimeType &&
            OutputArea.isIsolated(mimeType, model.metadata) ===
                renderer instanceof Private.IsolatedRenderer) {
            void renderer.renderModel(model);
        }
        else {
            this.layout.widgets[index].dispose();
            this._insertOutput(index, model);
        }
    }
    /**
     * Render and insert a single output into the layout.
     *
     * @param index - The index of the output to be inserted.
     * @param model - The model of the output to be inserted.
     */
    _insertOutput(index, model) {
        if (index > this._maxNumberOutputs) {
            return;
        }
        const layout = this.layout;
        if (index === this._maxNumberOutputs) {
            const warning = new Private.TrimmedOutputs(this._maxNumberOutputs, () => {
                const lastShown = this._maxNumberOutputs;
                this._maxNumberOutputs = Infinity;
                this._showTrimmedOutputs(lastShown);
            });
            layout.insertWidget(index, this._wrappedOutput(warning));
        }
        else {
            let output = this.createOutputItem(model);
            if (output) {
                output.toggleClass(EXECUTE_CLASS, model.executionCount !== null);
            }
            else {
                output = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget();
            }
            if (!this._outputTracker.has(output)) {
                void this._outputTracker.add(output);
            }
            layout.insertWidget(index, output);
        }
    }
    /**
     * A widget tracker for individual output widgets in the output area.
     */
    get outputTracker() {
        return this._outputTracker;
    }
    /**
     * Dispose information message and show output models from the given
     * index to maxNumberOutputs
     *
     * @param lastShown Starting model index to insert.
     */
    _showTrimmedOutputs(lastShown) {
        // Dispose information widget
        this.widgets[lastShown].dispose();
        for (let idx = lastShown; idx < this.model.length; idx++) {
            this._insertOutput(idx, this.model.get(idx));
        }
        this.outputLengthChanged.emit(Math.min(this.model.length, this._maxNumberOutputs));
    }
    /**
     * Create an output item with a prompt and actual output
     *
     * @returns a rendered widget, or null if we cannot render
     * #### Notes
     */
    createOutputItem(model) {
        const output = this.createRenderedMimetype(model);
        if (!output) {
            return null;
        }
        return this._wrappedOutput(output, model.executionCount);
    }
    /**
     * Render a mimetype
     */
    createRenderedMimetype(model) {
        const mimeType = this.rendermime.preferredMimeType(model.data, model.trusted ? 'any' : 'ensure');
        if (!mimeType) {
            return null;
        }
        let output = this.rendermime.createRenderer(mimeType);
        const isolated = OutputArea.isIsolated(mimeType, model.metadata);
        if (isolated === true) {
            output = new Private.IsolatedRenderer(output);
        }
        Private.currentPreferredMimetype.set(output, mimeType);
        output.renderModel(model).catch(error => {
            // Manually append error message to output
            const pre = document.createElement('pre');
            const trans = this._translator.load('jupyterlab');
            pre.textContent = trans.__('Javascript Error: %1', error.message);
            output.node.appendChild(pre);
            // Remove mime-type-specific CSS classes
            output.node.className = 'lm-Widget jp-RenderedText';
            output.node.setAttribute('data-mime-type', 'application/vnd.jupyter.stderr');
        });
        return output;
    }
    /**
     * Wrap a output widget within a output panel
     *
     * @param output Output widget to wrap
     * @param executionCount Execution count
     * @returns The output panel
     */
    _wrappedOutput(output, executionCount = null) {
        const panel = new Private.OutputPanel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        const prompt = this.contentFactory.createOutputPrompt();
        prompt.executionCount = executionCount;
        prompt.addClass(OUTPUT_AREA_PROMPT_CLASS);
        panel.addWidget(prompt);
        output.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(output);
        return panel;
    }
}
class SimplifiedOutputArea extends OutputArea {
    /**
     * Handle an input request from a kernel by doing nothing.
     */
    onInputRequest(msg, future) {
        return;
    }
    /**
     * Create an output item without a prompt, just the output widgets
     */
    createOutputItem(model) {
        const output = this.createRenderedMimetype(model);
        if (!output) {
            return null;
        }
        const panel = new Private.OutputPanel();
        panel.addClass(OUTPUT_AREA_ITEM_CLASS);
        output.addClass(OUTPUT_AREA_OUTPUT_CLASS);
        panel.addWidget(output);
        return panel;
    }
}
/**
 * A namespace for OutputArea statics.
 */
(function (OutputArea) {
    /**
     * Execute code on an output area.
     */
    async function execute(code, output, sessionContext, metadata) {
        var _a;
        // Override the default for `stop_on_error`.
        let stopOnError = true;
        if (metadata &&
            Array.isArray(metadata.tags) &&
            metadata.tags.indexOf('raises-exception') !== -1) {
            stopOnError = false;
        }
        const content = {
            code,
            stop_on_error: stopOnError
        };
        const kernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            throw new Error('Session has no kernel.');
        }
        const future = kernel.requestExecute(content, false, metadata);
        output.future = future;
        return future.done;
    }
    OutputArea.execute = execute;
    function isIsolated(mimeType, metadata) {
        const mimeMd = metadata[mimeType];
        // mime-specific higher priority
        if (mimeMd && mimeMd['isolated'] !== undefined) {
            return !!mimeMd['isolated'];
        }
        else {
            // fallback on global
            return !!metadata['isolated'];
        }
    }
    OutputArea.isIsolated = isIsolated;
    /**
     * The default implementation of `IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create the output prompt for the widget.
         */
        createOutputPrompt() {
            return new OutputPrompt();
        }
        /**
         * Create an stdin widget.
         */
        createStdin(options) {
            return new Stdin(options);
        }
    }
    OutputArea.ContentFactory = ContentFactory;
    /**
     * The default `ContentFactory` instance.
     */
    OutputArea.defaultContentFactory = new ContentFactory();
})(OutputArea || (OutputArea = {}));
/**
 * The default output prompt implementation
 */
class OutputPrompt extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget {
    /*
     * Create an output prompt widget.
     */
    constructor() {
        super();
        this._executionCount = null;
        this.addClass(OUTPUT_PROMPT_CLASS);
    }
    /**
     * The execution count for the prompt.
     */
    get executionCount() {
        return this._executionCount;
    }
    set executionCount(value) {
        this._executionCount = value;
        if (value === null) {
            this.node.textContent = '';
        }
        else {
            this.node.textContent = `[${value}]:`;
        }
    }
}
/**
 * The default stdin widget.
 */
class Stdin extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget {
    static _historyIx(key, ix) {
        const history = Stdin._history.get(key);
        if (!history) {
            return undefined;
        }
        const len = history.length;
        // wrap nonpositive ix to nonnegative ix
        if (ix <= 0) {
            return len + ix;
        }
    }
    static _historyAt(key, ix) {
        const history = Stdin._history.get(key);
        if (!history) {
            return undefined;
        }
        const len = history.length;
        const ixpos = Stdin._historyIx(key, ix);
        if (ixpos !== undefined && ixpos < len) {
            return history[ixpos];
        }
        // return undefined if ix is out of bounds
    }
    static _historyPush(key, line) {
        const history = Stdin._history.get(key);
        history.push(line);
        if (history.length > 1000) {
            // truncate line history if it's too long
            history.shift();
        }
    }
    static _historySearch(key, pat, ix, reverse = true) {
        const history = Stdin._history.get(key);
        const len = history.length;
        const ixpos = Stdin._historyIx(key, ix);
        const substrFound = (x) => x.search(pat) !== -1;
        if (ixpos === undefined) {
            return;
        }
        if (reverse) {
            if (ixpos === 0) {
                // reverse search fails if already at start of history
                return;
            }
            const ixFound = history.slice(0, ixpos).findLastIndex(substrFound);
            if (ixFound !== -1) {
                // wrap ix to negative
                return ixFound - len;
            }
        }
        else {
            if (ixpos >= len - 1) {
                // forward search fails if already at end of history
                return;
            }
            const ixFound = history.slice(ixpos + 1).findIndex(substrFound);
            if (ixFound !== -1) {
                // wrap ix to negative and adjust for slice
                return ixFound - len + ixpos + 1;
            }
        }
    }
    /**
     * Construct a new input widget.
     */
    constructor(options) {
        var _a;
        super({
            node: Private.createInputWidgetNode(options.prompt, options.password)
        });
        this._promise = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        this.addClass(STDIN_CLASS);
        this._future = options.future;
        this._historyIndex = 0;
        this._historyKey =
            options.inputHistoryScope === 'session'
                ? options.parent_header.session
                : '';
        this._historyPat = '';
        this._parentHeader = options.parent_header;
        this._password = options.password;
        this._trans = ((_a = options.translator) !== null && _a !== void 0 ? _a : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator).load('jupyterlab');
        this._value = options.prompt + ' ';
        this._input = this.node.getElementsByTagName('input')[0];
        // make users aware of the line history feature
        this._input.placeholder = this._trans.__('↑↓ for history. Search history with c-↑/c-↓');
        // initialize line history
        if (!Stdin._history.has(this._historyKey)) {
            Stdin._history.set(this._historyKey, []);
        }
    }
    /**
     * The value of the widget.
     */
    get value() {
        return this._promise.promise.then(() => this._value);
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
        const input = this._input;
        if (event.type === 'keydown') {
            if (event.key === 'Enter') {
                this.resetSearch();
                this._future.sendInputReply({
                    status: 'ok',
                    value: input.value
                }, this._parentHeader);
                if (this._password) {
                    this._value += '········';
                }
                else {
                    this._value += input.value;
                    Stdin._historyPush(this._historyKey, input.value);
                }
                this._promise.resolve(void 0);
            }
            else if (event.key === 'Escape') {
                // currently this gets clobbered by the documentsearch:end command at the notebook level
                this.resetSearch();
                input.blur();
            }
            else if (event.ctrlKey &&
                (event.key === 'ArrowUp' || event.key === 'ArrowDown')) {
                // if _historyPat is blank, use input as search pattern. Otherwise, reuse the current search pattern
                if (this._historyPat === '') {
                    this._historyPat = input.value;
                }
                const reverse = event.key === 'ArrowUp';
                const searchHistoryIx = Stdin._historySearch(this._historyKey, this._historyPat, this._historyIndex, reverse);
                if (searchHistoryIx !== undefined) {
                    const historyLine = Stdin._historyAt(this._historyKey, searchHistoryIx);
                    if (historyLine !== undefined) {
                        if (this._historyIndex === 0) {
                            this._valueCache = input.value;
                        }
                        this._setInputValue(historyLine);
                        this._historyIndex = searchHistoryIx;
                        // The default action for ArrowUp is moving to first character
                        // but we want to keep the cursor at the end.
                        event.preventDefault();
                    }
                }
            }
            else if (event.key === 'ArrowUp') {
                this.resetSearch();
                const historyLine = Stdin._historyAt(this._historyKey, this._historyIndex - 1);
                if (historyLine) {
                    if (this._historyIndex === 0) {
                        this._valueCache = input.value;
                    }
                    this._setInputValue(historyLine);
                    --this._historyIndex;
                    // The default action for ArrowUp is moving to first character
                    // but we want to keep the cursor at the end.
                    event.preventDefault();
                }
            }
            else if (event.key === 'ArrowDown') {
                this.resetSearch();
                if (this._historyIndex === 0) {
                    // do nothing
                }
                else if (this._historyIndex === -1) {
                    this._setInputValue(this._valueCache);
                    ++this._historyIndex;
                }
                else {
                    const historyLine = Stdin._historyAt(this._historyKey, this._historyIndex + 1);
                    if (historyLine) {
                        this._setInputValue(historyLine);
                        ++this._historyIndex;
                    }
                }
            }
        }
    }
    resetSearch() {
        this._historyPat = '';
    }
    /**
     * Handle `after-attach` messages sent to the widget.
     */
    onAfterAttach(msg) {
        this._input.addEventListener('keydown', this);
        this._input.focus();
    }
    /**
     * Handle `before-detach` messages sent to the widget.
     */
    onBeforeDetach(msg) {
        this._input.removeEventListener('keydown', this);
    }
    _setInputValue(value) {
        this._input.value = value;
        // Set cursor at the end; this is usually not necessary when input is
        // focused but having the explicit placement ensures consistency.
        this._input.setSelectionRange(value.length, value.length);
    }
}
Stdin._history = new Map();

/** ****************************************************************************
 * Private namespace
 ******************************************************************************/
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Create the node for an InputWidget.
     */
    function createInputWidgetNode(prompt, password) {
        const node = document.createElement('div');
        const promptNode = document.createElement('pre');
        promptNode.className = STDIN_PROMPT_CLASS;
        promptNode.textContent = prompt;
        const input = document.createElement('input');
        input.className = STDIN_INPUT_CLASS;
        if (password) {
            input.type = 'password';
        }
        node.appendChild(promptNode);
        promptNode.appendChild(input);
        return node;
    }
    Private.createInputWidgetNode = createInputWidgetNode;
    /**
     * A renderer for IFrame data.
     */
    class IsolatedRenderer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget {
        /**
         * Create an isolated renderer.
         */
        constructor(wrapped) {
            super({ node: document.createElement('iframe') });
            this.addClass('jp-mod-isolated');
            this._wrapped = wrapped;
            // Once the iframe is loaded, the subarea is dynamically inserted
            const iframe = this.node;
            iframe.frameBorder = '0';
            iframe.scrolling = 'auto';
            iframe.addEventListener('load', () => {
                // Workaround needed by Firefox, to properly render svg inside
                // iframes, see https://stackoverflow.com/questions/10177190/
                // svg-dynamically-added-to-iframe-does-not-render-correctly
                iframe.contentDocument.open();
                // Insert the subarea into the iframe
                // We must directly write the html. At this point, subarea doesn't
                // contain any user content.
                iframe.contentDocument.write(this._wrapped.node.innerHTML);
                iframe.contentDocument.close();
                const body = iframe.contentDocument.body;
                // Adjust the iframe height automatically
                iframe.style.height = `${body.scrollHeight}px`;
                iframe.heightChangeObserver = new ResizeObserver(() => {
                    iframe.style.height = `${body.scrollHeight}px`;
                });
                iframe.heightChangeObserver.observe(body);
            });
        }
        /**
         * Render a mime model.
         *
         * @param model - The mime model to render.
         *
         * @returns A promise which resolves when rendering is complete.
         *
         * #### Notes
         * This method may be called multiple times during the lifetime
         * of the widget to update it if and when new data is available.
         */
        renderModel(model) {
            return this._wrapped.renderModel(model);
        }
    }
    Private.IsolatedRenderer = IsolatedRenderer;
    Private.currentPreferredMimetype = new _lumino_properties__WEBPACK_IMPORTED_MODULE_4__.AttachedProperty({
        name: 'preferredMimetype',
        create: owner => ''
    });
    /**
     * A `Panel` that's focused by a `contextmenu` event.
     */
    class OutputPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Panel {
        /**
         * Construct a new `OutputPanel` widget.
         */
        constructor(options) {
            super(options);
        }
        /**
         * A callback that focuses on the widget.
         */
        _onContext(_) {
            this.node.focus();
        }
        /**
         * Handle `after-attach` messages sent to the widget.
         */
        onAfterAttach(msg) {
            super.onAfterAttach(msg);
            this.node.addEventListener('contextmenu', this._onContext.bind(this));
        }
        /**
         * Handle `before-detach` messages sent to the widget.
         */
        onBeforeDetach(msg) {
            super.onAfterDetach(msg);
            this.node.removeEventListener('contextmenu', this._onContext.bind(this));
        }
    }
    Private.OutputPanel = OutputPanel;
    /**
     * Trimmed outputs information widget.
     */
    class TrimmedOutputs extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget {
        /**
         * Widget constructor
         *
         * ### Notes
         * The widget will be disposed on click after calling the callback.
         *
         * @param maxNumberOutputs Maximal number of outputs to display
         * @param _onClick Callback on click event on the widget
         */
        constructor(maxNumberOutputs, onClick) {
            const node = document.createElement('div');
            const title = `The first ${maxNumberOutputs} are displayed`;
            const msg = 'Show more outputs';
            node.insertAdjacentHTML('afterbegin', `<a title=${title}>
          <pre>${msg}</pre>
        </a>`);
            super({
                node
            });
            this._onClick = onClick;
            this.addClass('jp-TrimmedOutputs');
            this.addClass('jp-RenderedHTMLCommon');
        }
        /**
         * Handle the DOM events for widget.
         *
         * @param event - The DOM event sent to the widget.
         *
         * #### Notes
         * This method implements the DOM `EventListener` interface and is
         * called in response to events on the widget's DOM node. It should
         * not be called directly by user code.
         */
        handleEvent(event) {
            if (event.type === 'click') {
                this._onClick(event);
            }
        }
        /**
         * Handle `after-attach` messages for the widget.
         */
        onAfterAttach(msg) {
            super.onAfterAttach(msg);
            this.node.addEventListener('click', this);
        }
        /**
         * A message handler invoked on a `'before-detach'`
         * message
         */
        onBeforeDetach(msg) {
            super.onBeforeDetach(msg);
            this.node.removeEventListener('click', this);
        }
    }
    Private.TrimmedOutputs = TrimmedOutputs;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfb3V0cHV0YXJlYV9saWJfaW5kZXhfanMuZDZmOGRjNDMxNTlkM2UyYmNiZDUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRXFCO0FBQ0M7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1J6QiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRVY7QUFDeUI7QUFDUDtBQUMzQjtBQUNJO0FBRVE7QUFxSHBEOztHQUVHO0FBQ0ksTUFBTSxlQUFlO0lBQzFCOztPQUVHO0lBQ0gsWUFBWSxVQUFxQyxFQUFFO1FBdU9uRDs7O1dBR0c7UUFDTyxjQUFTLEdBQUcsS0FBSyxDQUFDO1FBdUVwQixnQkFBVyxHQUFHLEVBQUUsQ0FBQztRQUVqQixhQUFRLEdBQUcsS0FBSyxDQUFDO1FBQ2pCLGdCQUFXLEdBQUcsS0FBSyxDQUFDO1FBQ3BCLGtCQUFhLEdBQUcsSUFBSSxxREFBTSxDQUEwQixJQUFJLENBQUMsQ0FBQztRQUMxRCxhQUFRLEdBQUcsSUFBSSxxREFBTSxDQUMzQixJQUFJLENBQ0wsQ0FBQztRQXhUQSxJQUFJLENBQUMsUUFBUSxHQUFHLENBQUMsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDO1FBQ2xDLElBQUksQ0FBQyxjQUFjO1lBQ2pCLE9BQU8sQ0FBQyxjQUFjLElBQUksZUFBZSxDQUFDLHFCQUFxQixDQUFDO1FBQ2xFLElBQUksQ0FBQyxJQUFJLEdBQUcsSUFBSSxtRUFBYyxFQUFnQixDQUFDO1FBQy9DLElBQUksT0FBTyxDQUFDLE1BQU0sRUFBRTtZQUNsQixLQUFLLE1BQU0sS0FBSyxJQUFJLE9BQU8sQ0FBQyxNQUFNLEVBQUU7Z0JBQ2xDLE1BQU0sS0FBSyxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDO2dCQUNuQyxNQUFNLElBQUksR0FBRyxJQUFJLENBQUMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMs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LENBQUMsQ0FBQztRQUMvQyxDQUFDO0tBR0Y7SUFqRVksc0JBQWMsaUJBaUUxQjtBQUNILENBQUMsRUF4TVMsT0FBTyxLQUFQLE9BQU8sUUF3TWhCIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL291dHB1dGFyZWEvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vdXRwdXRhcmVhL3NyYy9tb2RlbC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb3V0cHV0YXJlYS9zcmMvd2lkZ2V0LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG91dHB1dGFyZWFcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL21vZGVsJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0ICogYXMgbmJmb3JtYXQgZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgSU9ic2VydmFibGVMaXN0LCBPYnNlcnZhYmxlTGlzdCB9IGZyb20gJ0BqdXB5dGVybGFiL29ic2VydmFibGVzJztcbmltcG9ydCB7IElPdXRwdXRNb2RlbCwgT3V0cHV0TW9kZWwgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IG1hcCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IEpTT05FeHQgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogVGhlIG1vZGVsIGZvciBhbiBvdXRwdXQgYXJlYS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJT3V0cHV0QXJlYU1vZGVsIGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBvdXRwdXQgaXRlbSBjaGFuZ2VzLlxuICAgKlxuICAgKiBUaGUgbnVtYmVyIGlzIHRoZSBpbmRleCBvZiB0aGUgb3V0cHV0IHRoYXQgY2hhbmdlZC5cbiAgICovXG4gIHJlYWRvbmx5IHN0YXRlQ2hhbmdlZDogSVNpZ25hbDxJT3V0cHV0QXJlYU1vZGVsLCBudW1iZXI+O1xuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGxpc3Qgb2YgaXRlbXMgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IGNoYW5nZWQ6IElTaWduYWw8SU91dHB1dEFyZWFNb2RlbCwgSU91dHB1dEFyZWFNb2RlbC5DaGFuZ2VkQXJncz47XG5cbiAgLyoqXG4gICAqIFRoZSBsZW5ndGggb2YgdGhlIGl0ZW1zIGluIHRoZSBtb2RlbC5cbiAgICovXG4gIHJlYWRvbmx5IGxlbmd0aDogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBvdXRwdXQgYXJlYSBpcyB0cnVzdGVkLlxuICAgKi9cbiAgdHJ1c3RlZDogYm9vbGVhbjtcblxuICAvKipcbiAgICogVGhlIG91dHB1dCBjb250ZW50IGZhY3RvcnkgdXNlZCBieSB0aGUgbW9kZWwuXG4gICAqL1xuICByZWFkb25seSBjb250ZW50RmFjdG9yeTogSU91dHB1dEFyZWFNb2RlbC5JQ29udGVudEZhY3Rvcnk7XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpdGVtIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqL1xuICBnZXQoaW5kZXg6IG51bWJlcik6IElPdXRwdXRNb2RlbDtcblxuICAvKipcbiAgICogQWRkIGFuIG91dHB1dCwgd2hpY2ggbWF5IGJlIGNvbWJpbmVkIHdpdGggcHJldmlvdXMgb3V0cHV0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgdG90YWwgbnVtYmVyIG9mIG91dHB1dHMuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIG91dHB1dCBidW5kbGUgaXMgY29waWVkLlxuICAgKiBDb250aWd1b3VzIHN0cmVhbSBvdXRwdXRzIG9mIHRoZSBzYW1lIGBuYW1lYCBhcmUgY29tYmluZWQuXG4gICAqL1xuICBhZGQob3V0cHV0OiBuYmZvcm1hdC5JT3V0cHV0KTogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqL1xuICBzZXQoaW5kZXg6IG51bWJlciwgb3V0cHV0OiBuYmZvcm1hdC5JT3V0cHV0KTogdm9pZDtcblxuICAvKipcbiAgICogQ2xlYXIgYWxsIG9mIHRoZSBvdXRwdXQuXG4gICAqXG4gICAqIEBwYXJhbSB3YWl0IC0gRGVsYXkgY2xlYXJpbmcgdGhlIG91dHB1dCB1bnRpbCB0aGUgbmV4dCBtZXNzYWdlIGlzIGFkZGVkLlxuICAgKi9cbiAgY2xlYXIod2FpdD86IGJvb2xlYW4pOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBEZXNlcmlhbGl6ZSB0aGUgbW9kZWwgZnJvbSBKU09OLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgd2lsbCBjbGVhciBhbnkgZXhpc3RpbmcgZGF0YS5cbiAgICovXG4gIGZyb21KU09OKHZhbHVlczogbmJmb3JtYXQuSU91dHB1dFtdKTogdm9pZDtcblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklPdXRwdXRbXTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBJT3V0cHV0QXJlYU1vZGVsIGludGVyZmFjZXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSU91dHB1dEFyZWFNb2RlbCB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGNyZWF0ZSBhIG91dHB1dCBhcmVhIG1vZGVsLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGluaXRpYWwgdmFsdWVzIGZvciB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgdmFsdWVzPzogbmJmb3JtYXQuSU91dHB1dFtdO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgb3V0cHV0IGlzIHRydXN0ZWQuICBUaGUgZGVmYXVsdCBpcyBmYWxzZS5cbiAgICAgKi9cbiAgICB0cnVzdGVkPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBvdXRwdXQgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIG1vZGVsLlxuICAgICAqXG4gICAgICogSWYgbm90IGdpdmVuLCBhIGRlZmF1bHQgZmFjdG9yeSB3aWxsIGJlIHVzZWQuXG4gICAgICovXG4gICAgY29udGVudEZhY3Rvcnk/OiBJQ29udGVudEZhY3Rvcnk7XG4gIH1cblxuICAvKipcbiAgICogQSB0eXBlIGFsaWFzIGZvciBjaGFuZ2VkIGFyZ3MuXG4gICAqL1xuICBleHBvcnQgdHlwZSBDaGFuZ2VkQXJncyA9IElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8SU91dHB1dE1vZGVsPjtcblxuICAvKipcbiAgICogVGhlIGludGVyZmFjZSBmb3IgYW4gb3V0cHV0IGNvbnRlbnQgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUNvbnRlbnRGYWN0b3J5IHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYW4gb3V0cHV0IG1vZGVsLlxuICAgICAqL1xuICAgIGNyZWF0ZU91dHB1dE1vZGVsKG9wdGlvbnM6IElPdXRwdXRNb2RlbC5JT3B0aW9ucyk6IElPdXRwdXRNb2RlbDtcbiAgfVxufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIHRoZSBJT3V0cHV0QXJlYU1vZGVsLlxuICovXG5leHBvcnQgY2xhc3MgT3V0cHV0QXJlYU1vZGVsIGltcGxlbWVudHMgSU91dHB1dEFyZWFNb2RlbCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgb2JzZXJ2YWJsZSBvdXRwdXRzIGluc3RhbmNlLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogSU91dHB1dEFyZWFNb2RlbC5JT3B0aW9ucyA9IHt9KSB7XG4gICAgdGhpcy5fdHJ1c3RlZCA9ICEhb3B0aW9ucy50cnVzdGVkO1xuICAgIHRoaXMuY29udGVudEZhY3RvcnkgPVxuICAgICAgb3B0aW9ucy5jb250ZW50RmFjdG9yeSB8fCBPdXRwdXRBcmVhTW9kZWwuZGVmYXVsdENvbnRlbnRGYWN0b3J5O1xuICAgIHRoaXMubGlzdCA9IG5ldyBPYnNlcnZhYmxlTGlzdDxJT3V0cHV0TW9kZWw+KCk7XG4gICAgaWYgKG9wdGlvbnMudmFsdWVzKSB7XG4gICAgICBmb3IgKGNvbnN0IHZhbHVlIG9mIG9wdGlvbnMudmFsdWVzKSB7XG4gICAgICAgIGNvbnN0IGluZGV4ID0gdGhpcy5fYWRkKHZhbHVlKSAtIDE7XG4gICAgICAgIGNvbnN0IGl0ZW0gPSB0aGlzLmxpc3QuZ2V0KGluZGV4KTtcbiAgICAgICAgaXRlbS5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25HZW5lcmljQ2hhbmdlLCB0aGlzKTtcbiAgICAgIH1cbiAgICB9XG4gICAgdGhpcy5saXN0LmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkxpc3RDaGFuZ2VkLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gYW4gaXRlbSBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IHN0YXRlQ2hhbmdlZCgpOiBJU2lnbmFsPElPdXRwdXRBcmVhTW9kZWwsIG51bWJlcj4ge1xuICAgIHJldHVybiB0aGlzLl9zdGF0ZUNoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBsaXN0IG9mIGl0ZW1zIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPElPdXRwdXRBcmVhTW9kZWwsIElPdXRwdXRBcmVhTW9kZWwuQ2hhbmdlZEFyZ3M+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGxlbmd0aCBvZiB0aGUgaXRlbXMgaW4gdGhlIG1vZGVsLlxuICAgKi9cbiAgZ2V0IGxlbmd0aCgpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLmxpc3QgPyB0aGlzLmxpc3QubGVuZ3RoIDogMDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgd2hldGhlciB0aGUgbW9kZWwgaXMgdHJ1c3RlZC5cbiAgICovXG4gIGdldCB0cnVzdGVkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl90cnVzdGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCB3aGV0aGVyIHRoZSBtb2RlbCBpcyB0cnVzdGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIENoYW5naW5nIHRoZSB2YWx1ZSB3aWxsIGNhdXNlIGFsbCBvZiB0aGUgbW9kZWxzIHRvIHJlLXNldC5cbiAgICovXG4gIHNldCB0cnVzdGVkKHZhbHVlOiBib29sZWFuKSB7XG4gICAgaWYgKHZhbHVlID09PSB0aGlzLl90cnVzdGVkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHRydXN0ZWQgPSAodGhpcy5fdHJ1c3RlZCA9IHZhbHVlKTtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IHRoaXMubGlzdC5sZW5ndGg7IGkrKykge1xuICAgICAgY29uc3Qgb2xkSXRlbSA9IHRoaXMubGlzdC5nZXQoaSk7XG4gICAgICBjb25zdCB2YWx1ZSA9IG9sZEl0ZW0udG9KU09OKCk7XG4gICAgICBjb25zdCBpdGVtID0gdGhpcy5fY3JlYXRlSXRlbSh7IHZhbHVlLCB0cnVzdGVkIH0pO1xuICAgICAgdGhpcy5saXN0LnNldChpLCBpdGVtKTtcbiAgICAgIG9sZEl0ZW0uZGlzcG9zZSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgb3V0cHV0IGNvbnRlbnQgZmFjdG9yeSB1c2VkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnRlbnRGYWN0b3J5OiBJT3V0cHV0QXJlYU1vZGVsLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSBtb2RlbCBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyB1c2VkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICB0aGlzLmxpc3QuZGlzcG9zZSgpO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGFuIGl0ZW0gYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICovXG4gIGdldChpbmRleDogbnVtYmVyKTogSU91dHB1dE1vZGVsIHtcbiAgICByZXR1cm4gdGhpcy5saXN0LmdldChpbmRleCk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSB2YWx1ZSBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKi9cbiAgc2V0KGluZGV4OiBudW1iZXIsIHZhbHVlOiBuYmZvcm1hdC5JT3V0cHV0KTogdm9pZCB7XG4gICAgdmFsdWUgPSBKU09ORXh0LmRlZXBDb3B5KHZhbHVlKTtcbiAgICAvLyBOb3JtYWxpemUgc3RyZWFtIGRhdGEuXG4gICAgUHJpdmF0ZS5ub3JtYWxpemUodmFsdWUpO1xuICAgIGNvbnN0IGl0ZW0gPSB0aGlzLl9jcmVhdGVJdGVtKHsgdmFsdWUsIHRydXN0ZWQ6IHRoaXMuX3RydXN0ZWQgfSk7XG4gICAgdGhpcy5saXN0LnNldChpbmRleCwgaXRlbSk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGFuIG91dHB1dCwgd2hpY2ggbWF5IGJlIGNvbWJpbmVkIHdpdGggcHJldmlvdXMgb3V0cHV0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgdG90YWwgbnVtYmVyIG9mIG91dHB1dHMuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIG91dHB1dCBidW5kbGUgaXMgY29waWVkLlxuICAgKiBDb250aWd1b3VzIHN0cmVhbSBvdXRwdXRzIG9mIHRoZSBzYW1lIGBuYW1lYCBhcmUgY29tYmluZWQuXG4gICAqL1xuICBhZGQob3V0cHV0OiBuYmZvcm1hdC5JT3V0cHV0KTogbnVtYmVyIHtcbiAgICAvLyBJZiB3ZSByZWNlaXZlZCBhIGRlbGF5ZWQgY2xlYXIgbWVzc2FnZSwgdGhlbiBjbGVhciBub3cuXG4gICAgaWYgKHRoaXMuY2xlYXJOZXh0KSB7XG4gICAgICB0aGlzLmNsZWFyKCk7XG4gICAgICB0aGlzLmNsZWFyTmV4dCA9IGZhbHNlO1xuICAgIH1cblxuICAgIHJldHVybiB0aGlzLl9hZGQob3V0cHV0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciBhbGwgb2YgdGhlIG91dHB1dC5cbiAgICpcbiAgICogQHBhcmFtIHdhaXQgRGVsYXkgY2xlYXJpbmcgdGhlIG91dHB1dCB1bnRpbCB0aGUgbmV4dCBtZXNzYWdlIGlzIGFkZGVkLlxuICAgKi9cbiAgY2xlYXIod2FpdDogYm9vbGVhbiA9IGZhbHNlKTogdm9pZCB7XG4gICAgdGhpcy5fbGFzdFN0cmVhbSA9ICcnO1xuICAgIGlmICh3YWl0KSB7XG4gICAgICB0aGlzLmNsZWFyTmV4dCA9IHRydWU7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGZvciAoY29uc3QgaXRlbSBvZiB0aGlzLmxpc3QpIHtcbiAgICAgIGl0ZW0uZGlzcG9zZSgpO1xuICAgIH1cbiAgICB0aGlzLmxpc3QuY2xlYXIoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEZXNlcmlhbGl6ZSB0aGUgbW9kZWwgZnJvbSBKU09OLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgd2lsbCBjbGVhciBhbnkgZXhpc3RpbmcgZGF0YS5cbiAgICovXG4gIGZyb21KU09OKHZhbHVlczogbmJmb3JtYXQuSU91dHB1dFtdKTogdm9pZCB7XG4gICAgdGhpcy5jbGVhcigpO1xuICAgIGZvciAoY29uc3QgdmFsdWUgb2YgdmFsdWVzKSB7XG4gICAgICB0aGlzLl9hZGQodmFsdWUpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBTZXJpYWxpemUgdGhlIG1vZGVsIHRvIEpTT04uXG4gICAqL1xuICB0b0pTT04oKTogbmJmb3JtYXQuSU91dHB1dFtdIHtcbiAgICByZXR1cm4gQXJyYXkuZnJvbShcbiAgICAgIG1hcCh0aGlzLmxpc3QsIChvdXRwdXQ6IElPdXRwdXRNb2RlbCkgPT4gb3V0cHV0LnRvSlNPTigpKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgY29weSBvZiB0aGUgaXRlbSB0byB0aGUgbGlzdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGxpc3QgbGVuZ3RoXG4gICAqL1xuICBwcml2YXRlIF9hZGQodmFsdWU6IG5iZm9ybWF0LklPdXRwdXQpOiBudW1iZXIge1xuICAgIGNvbnN0IHRydXN0ZWQgPSB0aGlzLl90cnVzdGVkO1xuICAgIHZhbHVlID0gSlNPTkV4dC5kZWVwQ29weSh2YWx1ZSk7XG5cbiAgICAvLyBOb3JtYWxpemUgdGhlIHZhbHVlLlxuICAgIFByaXZhdGUubm9ybWFsaXplKHZhbHVlKTtcblxuICAgIC8vIENvbnNvbGlkYXRlIG91dHB1dHMgaWYgdGhleSBhcmUgc3RyZWFtIG91dHB1dHMgb2YgdGhlIHNhbWUga2luZC5cbiAgICBpZiAoXG4gICAgICBuYmZvcm1hdC5pc1N0cmVhbSh2YWx1ZSkgJiZcbiAgICAgIHRoaXMuX2xhc3RTdHJlYW0gJiZcbiAgICAgIHZhbHVlLm5hbWUgPT09IHRoaXMuX2xhc3ROYW1lICYmXG4gICAgICB0aGlzLnNob3VsZENvbWJpbmUoe1xuICAgICAgICB2YWx1ZSxcbiAgICAgICAgbGFzdE1vZGVsOiB0aGlzLmxpc3QuZ2V0KHRoaXMubGVuZ3RoIC0gMSlcbiAgICAgIH0pXG4gICAgKSB7XG4gICAgICAvLyBJbiBvcmRlciB0byBnZXQgYSBsaXN0IGNoYW5nZSBldmVudCwgd2UgYWRkIHRoZSBwcmV2aW91c1xuICAgICAgLy8gdGV4dCB0byB0aGUgY3VycmVudCBpdGVtIGFuZCByZXBsYWNlIHRoZSBwcmV2aW91cyBpdGVtLlxuICAgICAgLy8gVGhpcyBhbHNvIHJlcGxhY2VzIHRoZSBtZXRhZGF0YSBvZiB0aGUgbGFzdCBpdGVtLlxuICAgICAgdGhpcy5fbGFzdFN0cmVhbSArPSB2YWx1ZS50ZXh0IGFzIHN0cmluZztcbiAgICAgIHRoaXMuX2xhc3RTdHJlYW0gPSBQcml2YXRlLnJlbW92ZU92ZXJ3cml0dGVuQ2hhcnModGhpcy5fbGFzdFN0cmVhbSk7XG4gICAgICB2YWx1ZS50ZXh0ID0gdGhpcy5fbGFzdFN0cmVhbTtcbiAgICAgIGNvbnN0IGl0ZW0gPSB0aGlzLl9jcmVhdGVJdGVtKHsgdmFsdWUsIHRydXN0ZWQgfSk7XG4gICAgICBjb25zdCBpbmRleCA9IHRoaXMubGVuZ3RoIC0gMTtcbiAgICAgIGNvbnN0IHByZXYgPSB0aGlzLmxpc3QuZ2V0KGluZGV4KTtcbiAgICAgIHRoaXMubGlzdC5zZXQoaW5kZXgsIGl0ZW0pO1xuICAgICAgcHJldi5kaXNwb3NlKCk7XG4gICAgICByZXR1cm4gdGhpcy5sZW5ndGg7XG4gICAgfVxuXG4gICAgaWYgKG5iZm9ybWF0LmlzU3RyZWFtKHZhbHVlKSkge1xuICAgICAgdmFsdWUudGV4dCA9IFByaXZhdGUucmVtb3ZlT3ZlcndyaXR0ZW5DaGFycyh2YWx1ZS50ZXh0IGFzIHN0cmluZyk7XG4gICAgfVxuXG4gICAgLy8gQ3JlYXRlIHRoZSBuZXcgaXRlbS5cbiAgICBjb25zdCBpdGVtID0gdGhpcy5fY3JlYXRlSXRlbSh7IHZhbHVlLCB0cnVzdGVkIH0pO1xuXG4gICAgLy8gVXBkYXRlIHRoZSBzdHJlYW0gaW5mb3JtYXRpb24uXG4gICAgaWYgKG5iZm9ybWF0LmlzU3RyZWFtKHZhbHVlKSkge1xuICAgICAgdGhpcy5fbGFzdFN0cmVhbSA9IHZhbHVlLnRleHQgYXMgc3RyaW5nO1xuICAgICAgdGhpcy5fbGFzdE5hbWUgPSB2YWx1ZS5uYW1lO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9sYXN0U3RyZWFtID0gJyc7XG4gICAgfVxuXG4gICAgLy8gQWRkIHRoZSBpdGVtIHRvIG91ciBsaXN0IGFuZCByZXR1cm4gdGhlIG5ldyBsZW5ndGguXG4gICAgcmV0dXJuIHRoaXMubGlzdC5wdXNoKGl0ZW0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgYSBuZXcgdmFsdWUgc2hvdWxkIGJlIGNvbnNvbGlkYXRlZCB3aXRoIHRoZSBwcmV2aW91cyBvdXRwdXQuXG4gICAqXG4gICAqIFRoaXMgd2lsbCBvbmx5IGJlIGNhbGxlZCBpZiB0aGUgbWluaW1hbCBjcml0ZXJpYSBvZiBib3RoIGJlaW5nIHN0cmVhbVxuICAgKiBtZXNzYWdlcyBvZiB0aGUgc2FtZSB0eXBlLlxuICAgKi9cbiAgcHJvdGVjdGVkIHNob3VsZENvbWJpbmUob3B0aW9uczoge1xuICAgIHZhbHVlOiBuYmZvcm1hdC5JT3V0cHV0O1xuICAgIGxhc3RNb2RlbDogSU91dHB1dE1vZGVsO1xuICB9KTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKipcbiAgICogQSBmbGFnIHRoYXQgaXMgc2V0IHdoZW4gd2Ugd2FudCB0byBjbGVhciB0aGUgb3V0cHV0IGFyZWFcbiAgICogKmFmdGVyKiB0aGUgbmV4dCBhZGRpdGlvbiB0byBpdC5cbiAgICovXG4gIHByb3RlY3RlZCBjbGVhck5leHQgPSBmYWxzZTtcblxuICAvKipcbiAgICogQW4gb2JzZXJ2YWJsZSBsaXN0IGNvbnRhaW5pbmcgdGhlIG91dHB1dCBtb2RlbHNcbiAgICogZm9yIHRoaXMgb3V0cHV0IGFyZWEuXG4gICAqL1xuICBwcm90ZWN0ZWQgbGlzdDogSU9ic2VydmFibGVMaXN0PElPdXRwdXRNb2RlbD47XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiBvdXRwdXQgaXRlbSBhbmQgaG9vayB1cCBpdHMgc2lnbmFscy5cbiAgICovXG4gIHByaXZhdGUgX2NyZWF0ZUl0ZW0ob3B0aW9uczogSU91dHB1dE1vZGVsLklPcHRpb25zKTogSU91dHB1dE1vZGVsIHtcbiAgICBjb25zdCBmYWN0b3J5ID0gdGhpcy5jb250ZW50RmFjdG9yeTtcbiAgICBjb25zdCBpdGVtID0gZmFjdG9yeS5jcmVhdGVPdXRwdXRNb2RlbChvcHRpb25zKTtcbiAgICByZXR1cm4gaXRlbTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIGxpc3QuXG4gICAqL1xuICBwcml2YXRlIF9vbkxpc3RDaGFuZ2VkKFxuICAgIHNlbmRlcjogSU9ic2VydmFibGVMaXN0PElPdXRwdXRNb2RlbD4sXG4gICAgYXJnczogSU9ic2VydmFibGVMaXN0LklDaGFuZ2VkQXJnczxJT3V0cHV0TW9kZWw+XG4gICkge1xuICAgIHN3aXRjaCAoYXJncy50eXBlKSB7XG4gICAgICBjYXNlICdhZGQnOlxuICAgICAgICBhcmdzLm5ld1ZhbHVlcy5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgICAgIGl0ZW0uY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uR2VuZXJpY0NoYW5nZSwgdGhpcyk7XG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3JlbW92ZSc6XG4gICAgICAgIGFyZ3Mub2xkVmFsdWVzLmZvckVhY2goaXRlbSA9PiB7XG4gICAgICAgICAgaXRlbS5jaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5fb25HZW5lcmljQ2hhbmdlLCB0aGlzKTtcbiAgICAgICAgfSk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnc2V0JzpcbiAgICAgICAgYXJncy5uZXdWYWx1ZXMuZm9yRWFjaChpdGVtID0+IHtcbiAgICAgICAgICBpdGVtLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkdlbmVyaWNDaGFuZ2UsIHRoaXMpO1xuICAgICAgICB9KTtcbiAgICAgICAgYXJncy5vbGRWYWx1ZXMuZm9yRWFjaChpdGVtID0+IHtcbiAgICAgICAgICBpdGVtLmNoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9vbkdlbmVyaWNDaGFuZ2UsIHRoaXMpO1xuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICAgIHRoaXMuX2NoYW5nZWQuZW1pdChhcmdzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gYW4gaXRlbS5cbiAgICovXG4gIHByaXZhdGUgX29uR2VuZXJpY0NoYW5nZShpdGVtTW9kZWw6IElPdXRwdXRNb2RlbCk6IHZvaWQge1xuICAgIGxldCBpZHg6IG51bWJlcjtcbiAgICBsZXQgaXRlbTogSU91dHB1dE1vZGVsIHwgbnVsbCA9IG51bGw7XG4gICAgZm9yIChpZHggPSAwOyBpZHggPCB0aGlzLmxpc3QubGVuZ3RoOyBpZHgrKykge1xuICAgICAgaXRlbSA9IHRoaXMubGlzdC5nZXQoaWR4KTtcbiAgICAgIGlmIChpdGVtID09PSBpdGVtTW9kZWwpIHtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgfVxuICAgIGlmIChpdGVtICE9IG51bGwpIHtcbiAgICAgIHRoaXMuX3N0YXRlQ2hhbmdlZC5lbWl0KGlkeCk7XG4gICAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgICB0eXBlOiAnc2V0JyxcbiAgICAgICAgbmV3SW5kZXg6IGlkeCxcbiAgICAgICAgb2xkSW5kZXg6IGlkeCxcbiAgICAgICAgb2xkVmFsdWVzOiBbaXRlbV0sXG4gICAgICAgIG5ld1ZhbHVlczogW2l0ZW1dXG4gICAgICB9KTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9sYXN0U3RyZWFtID0gJyc7XG4gIHByaXZhdGUgX2xhc3ROYW1lOiAnc3Rkb3V0JyB8ICdzdGRlcnInO1xuICBwcml2YXRlIF90cnVzdGVkID0gZmFsc2U7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfc3RhdGVDaGFuZ2VkID0gbmV3IFNpZ25hbDxPdXRwdXRBcmVhTW9kZWwsIG51bWJlcj4odGhpcyk7XG4gIHByaXZhdGUgX2NoYW5nZWQgPSBuZXcgU2lnbmFsPE91dHB1dEFyZWFNb2RlbCwgSU91dHB1dEFyZWFNb2RlbC5DaGFuZ2VkQXJncz4oXG4gICAgdGhpc1xuICApO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIE91dHB1dEFyZWFNb2RlbCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE91dHB1dEFyZWFNb2RlbCB7XG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBpbXBsZW1lbnRhdGlvbiBvZiBhIGBJTW9kZWxPdXRwdXRGYWN0b3J5YC5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBDb250ZW50RmFjdG9yeSBpbXBsZW1lbnRzIElPdXRwdXRBcmVhTW9kZWwuSUNvbnRlbnRGYWN0b3J5IHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYW4gb3V0cHV0IG1vZGVsLlxuICAgICAqL1xuICAgIGNyZWF0ZU91dHB1dE1vZGVsKG9wdGlvbnM6IElPdXRwdXRNb2RlbC5JT3B0aW9ucyk6IElPdXRwdXRNb2RlbCB7XG4gICAgICByZXR1cm4gbmV3IE91dHB1dE1vZGVsKG9wdGlvbnMpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBvdXRwdXQgbW9kZWwgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBkZWZhdWx0Q29udGVudEZhY3RvcnkgPSBuZXcgQ29udGVudEZhY3RvcnkoKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgbW9kdWxlLXByaXZhdGUgZnVuY3Rpb25hbGl0eS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogTm9ybWFsaXplIGFuIG91dHB1dC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBub3JtYWxpemUodmFsdWU6IG5iZm9ybWF0LklPdXRwdXQpOiB2b2lkIHtcbiAgICBpZiAobmJmb3JtYXQuaXNTdHJlYW0odmFsdWUpKSB7XG4gICAgICBpZiAoQXJyYXkuaXNBcnJheSh2YWx1ZS50ZXh0KSkge1xuICAgICAgICB2YWx1ZS50ZXh0ID0gKHZhbHVlLnRleHQgYXMgc3RyaW5nW10pLmpvaW4oJ1xcbicpO1xuICAgICAgfVxuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgY2hhcmFjdGVycyB0aGF0IGFyZSBvdmVycmlkZGVuIGJ5IGJhY2tzcGFjZSBjaGFyYWN0ZXJzLlxuICAgKi9cbiAgZnVuY3Rpb24gZml4QmFja3NwYWNlKHR4dDogc3RyaW5nKTogc3RyaW5nIHtcbiAgICBsZXQgdG1wID0gdHh0O1xuICAgIGRvIHtcbiAgICAgIHR4dCA9IHRtcDtcbiAgICAgIC8vIENhbmNlbCBvdXQgYW55dGhpbmctYnV0LW5ld2xpbmUgZm9sbG93ZWQgYnkgYmFja3NwYWNlXG4gICAgICB0bXAgPSB0eHQucmVwbGFjZSgvW15cXG5dXFx4MDgvZ20sICcnKTsgLy8gZXNsaW50LWRpc2FibGUtbGluZSBuby1jb250cm9sLXJlZ2V4XG4gICAgfSB3aGlsZSAodG1wLmxlbmd0aCA8IHR4dC5sZW5ndGgpO1xuICAgIHJldHVybiB0eHQ7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGNodW5rcyB0aGF0IHNob3VsZCBiZSBvdmVycmlkZGVuIGJ5IHRoZSBlZmZlY3Qgb2ZcbiAgICogY2FycmlhZ2UgcmV0dXJuIGNoYXJhY3RlcnMuXG4gICAqL1xuICBmdW5jdGlvbiBmaXhDYXJyaWFnZVJldHVybih0eHQ6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgdHh0ID0gdHh0LnJlcGxhY2UoL1xccitcXG4vZ20sICdcXG4nKTsgLy8gXFxyIGZvbGxvd2VkIGJ5IFxcbiAtLT4gbmV3bGluZVxuICAgIHdoaWxlICh0eHQuc2VhcmNoKC9cXHJbXiRdL2cpID4gLTEpIHtcbiAgICAgIGNvbnN0IGJhc2UgPSB0eHQubWF0Y2goL14oLiopXFxyKy9tKSFbMV07XG4gICAgICBsZXQgaW5zZXJ0ID0gdHh0Lm1hdGNoKC9cXHIrKC4qKSQvbSkhWzFdO1xuICAgICAgaW5zZXJ0ID0gaW5zZXJ0ICsgYmFzZS5zbGljZShpbnNlcnQubGVuZ3RoLCBiYXNlLmxlbmd0aCk7XG4gICAgICB0eHQgPSB0eHQucmVwbGFjZSgvXFxyKy4qJC9tLCAnXFxyJykucmVwbGFjZSgvXi4qXFxyL20sIGluc2VydCk7XG4gICAgfVxuICAgIHJldHVybiB0eHQ7XG4gIH1cblxuICAvKlxuICAgKiBSZW1vdmUgY2hhcmFjdGVycyBvdmVycmlkZGVuIGJ5IGJhY2tzcGFjZXMgYW5kIGNhcnJpYWdlIHJldHVybnNcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiByZW1vdmVPdmVyd3JpdHRlbkNoYXJzKHRleHQ6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgcmV0dXJuIGZpeENhcnJpYWdlUmV0dXJuKGZpeEJhY2tzcGFjZSh0ZXh0KSk7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVNlc3Npb25Db250ZXh0LCBXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0ICogYXMgbmJmb3JtYXQgZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgSU91dHB1dE1vZGVsLCBJUmVuZGVyTWltZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJUmVuZGVyTWltZSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUtaW50ZXJmYWNlcyc7XG5pbXBvcnQgeyBLZXJuZWwsIEtlcm5lbE1lc3NhZ2UgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7XG4gIEpTT05PYmplY3QsXG4gIFByb21pc2VEZWxlZ2F0ZSxcbiAgUmVhZG9ubHlKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBVVUlEXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBBdHRhY2hlZFByb3BlcnR5IH0gZnJvbSAnQGx1bWluby9wcm9wZXJ0aWVzJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFBhbmVsLCBQYW5lbExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IElPdXRwdXRBcmVhTW9kZWwgfSBmcm9tICcuL21vZGVsJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhbiBvdXRwdXQgYXJlYSB3aWRnZXQuXG4gKi9cbmNvbnN0IE9VVFBVVF9BUkVBX0NMQVNTID0gJ2pwLU91dHB1dEFyZWEnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSBkaXJlY3Rpb24gY2hpbGRyZW4gb2YgT3V0cHV0QXJlYVxuICovXG5jb25zdCBPVVRQVVRfQVJFQV9JVEVNX0NMQVNTID0gJ2pwLU91dHB1dEFyZWEtY2hpbGQnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGFjdHVhbCBvdXRwdXRzXG4gKi9cbmNvbnN0IE9VVFBVVF9BUkVBX09VVFBVVF9DTEFTUyA9ICdqcC1PdXRwdXRBcmVhLW91dHB1dCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gcHJvbXB0IGNoaWxkcmVuIG9mIE91dHB1dEFyZWEuXG4gKi9cbmNvbnN0IE9VVFBVVF9BUkVBX1BST01QVF9DTEFTUyA9ICdqcC1PdXRwdXRBcmVhLXByb21wdCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gT3V0cHV0UHJvbXB0LlxuICovXG5jb25zdCBPVVRQVVRfUFJPTVBUX0NMQVNTID0gJ2pwLU91dHB1dFByb21wdCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYW4gZXhlY3V0aW9uIHJlc3VsdC5cbiAqL1xuY29uc3QgRVhFQ1VURV9DTEFTUyA9ICdqcC1PdXRwdXRBcmVhLWV4ZWN1dGVSZXN1bHQnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHN0ZGluIGl0ZW1zIG9mIE91dHB1dEFyZWFcbiAqL1xuY29uc3QgT1VUUFVUX0FSRUFfU1RESU5fSVRFTV9DTEFTUyA9ICdqcC1PdXRwdXRBcmVhLXN0ZGluLWl0ZW0nO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHN0ZGluIHdpZGdldHMuXG4gKi9cbmNvbnN0IFNURElOX0NMQVNTID0gJ2pwLVN0ZGluJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBzdGRpbiBkYXRhIHByb21wdCBub2Rlcy5cbiAqL1xuY29uc3QgU1RESU5fUFJPTVBUX0NMQVNTID0gJ2pwLVN0ZGluLXByb21wdCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gc3RkaW4gZGF0YSBpbnB1dCBub2Rlcy5cbiAqL1xuY29uc3QgU1RESU5fSU5QVVRfQ0xBU1MgPSAnanAtU3RkaW4taW5wdXQnO1xuXG4vKipcbiAqIFRoZSBvdmVybGF5IHRoYXQgY2FuIGJlIGNsaWNrZWQgdG8gc3dpdGNoIGJldHdlZW4gb3V0cHV0IHNjcm9sbGluZyBtb2Rlcy5cbiAqL1xuY29uc3QgT1VUUFVUX1BST01QVF9PVkVSTEFZID0gJ2pwLU91dHB1dEFyZWEtcHJvbXB0T3ZlcmxheSc7XG5cbi8qKiAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqXG4gKiBPdXRwdXRBcmVhXG4gKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuXG4vKipcbiAqIEFuIG91dHB1dCBhcmVhIHdpZGdldC5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGUgd2lkZ2V0IG1vZGVsIG11c3QgYmUgc2V0IHNlcGFyYXRlbHkgYW5kIGNhbiBiZSBjaGFuZ2VkXG4gKiBhdCBhbnkgdGltZS4gIENvbnN1bWVycyBvZiB0aGUgd2lkZ2V0IG11c3QgYWNjb3VudCBmb3IgYVxuICogYG51bGxgIG1vZGVsLCBhbmQgbWF5IHdhbnQgdG8gbGlzdGVuIHRvIHRoZSBgbW9kZWxDaGFuZ2VkYFxuICogc2lnbmFsLlxuICovXG5leHBvcnQgY2xhc3MgT3V0cHV0QXJlYSBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYW4gb3V0cHV0IGFyZWEgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogT3V0cHV0QXJlYS5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgc3VwZXIubGF5b3V0ID0gbmV3IFBhbmVsTGF5b3V0KCk7XG4gICAgdGhpcy5hZGRDbGFzcyhPVVRQVVRfQVJFQV9DTEFTUyk7XG4gICAgdGhpcy5jb250ZW50RmFjdG9yeSA9XG4gICAgICBvcHRpb25zLmNvbnRlbnRGYWN0b3J5ID8/IE91dHB1dEFyZWEuZGVmYXVsdENvbnRlbnRGYWN0b3J5O1xuICAgIHRoaXMucmVuZGVybWltZSA9IG9wdGlvbnMucmVuZGVybWltZTtcbiAgICB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzID0gb3B0aW9ucy5tYXhOdW1iZXJPdXRwdXRzID8/IEluZmluaXR5O1xuICAgIHRoaXMuX3RyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5faW5wdXRIaXN0b3J5U2NvcGUgPSBvcHRpb25zLmlucHV0SGlzdG9yeVNjb3BlID8/ICdnbG9iYWwnO1xuXG4gICAgY29uc3QgbW9kZWwgPSAodGhpcy5tb2RlbCA9IG9wdGlvbnMubW9kZWwpO1xuICAgIGZvciAoXG4gICAgICBsZXQgaSA9IDA7XG4gICAgICBpIDwgTWF0aC5taW4obW9kZWwubGVuZ3RoLCB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzICsgMSk7XG4gICAgICBpKytcbiAgICApIHtcbiAgICAgIGNvbnN0IG91dHB1dCA9IG1vZGVsLmdldChpKTtcbiAgICAgIHRoaXMuX2luc2VydE91dHB1dChpLCBvdXRwdXQpO1xuICAgIH1cbiAgICBtb2RlbC5jaGFuZ2VkLmNvbm5lY3QodGhpcy5vbk1vZGVsQ2hhbmdlZCwgdGhpcyk7XG4gICAgbW9kZWwuc3RhdGVDaGFuZ2VkLmNvbm5lY3QodGhpcy5vblN0YXRlQ2hhbmdlZCwgdGhpcyk7XG4gICAgaWYgKG9wdGlvbnMucHJvbXB0T3ZlcmxheSkge1xuICAgICAgdGhpcy5fYWRkUHJvbXB0T3ZlcmxheSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnRlbnRGYWN0b3J5OiBPdXRwdXRBcmVhLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogVGhlIG1vZGVsIHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIHJlYWRvbmx5IG1vZGVsOiBJT3V0cHV0QXJlYU1vZGVsO1xuXG4gIC8qKlxuICAgKiBUaGUgcmVuZGVybWltZSBpbnN0YW5jZSB1c2VkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICByZWFkb25seSByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5O1xuXG4gIC8qKlxuICAgKiBOYXJyb3cgdGhlIHR5cGUgb2YgT3V0cHV0QXJlYSdzIGxheW91dCBwcm9wXG4gICAqL1xuICBnZXQgbGF5b3V0KCk6IFBhbmVsTGF5b3V0IHtcbiAgICByZXR1cm4gc3VwZXIubGF5b3V0IGFzIFBhbmVsTGF5b3V0O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcmVhZC1vbmx5IHNlcXVlbmNlIG9mIHRoZSBjaGlsZHJlbiB3aWRnZXRzIGluIHRoZSBvdXRwdXQgYXJlYS5cbiAgICovXG4gIGdldCB3aWRnZXRzKCk6IFJlYWRvbmx5QXJyYXk8V2lkZ2V0PiB7XG4gICAgcmV0dXJuIHRoaXMubGF5b3V0LndpZGdldHM7XG4gIH1cblxuICAvKipcbiAgICogQSBwdWJsaWMgc2lnbmFsIHVzZWQgdG8gaW5kaWNhdGUgdGhlIG51bWJlciBvZiBkaXNwbGF5ZWQgb3V0cHV0cyBoYXMgY2hhbmdlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGlzIHVzZWZ1bCBmb3IgcGFyZW50cyB3aG8gd2FudCB0byBhcHBseSBzdHlsaW5nIGJhc2VkIG9uIHRoZSBudW1iZXJcbiAgICogb2Ygb3V0cHV0cy4gRW1pdHMgdGhlIGN1cnJlbnQgbnVtYmVyIG9mIG91dHB1dHMuXG4gICAqL1xuICByZWFkb25seSBvdXRwdXRMZW5ndGhDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBudW1iZXI+KHRoaXMpO1xuXG4gIC8qKlxuICAgKiBUaGUga2VybmVsIGZ1dHVyZSBhc3NvY2lhdGVkIHdpdGggdGhlIG91dHB1dCBhcmVhLlxuICAgKi9cbiAgZ2V0IGZ1dHVyZSgpOiBLZXJuZWwuSVNoZWxsRnV0dXJlPFxuICAgIEtlcm5lbE1lc3NhZ2UuSUV4ZWN1dGVSZXF1ZXN0TXNnLFxuICAgIEtlcm5lbE1lc3NhZ2UuSUV4ZWN1dGVSZXBseU1zZ1xuICA+IHtcbiAgICByZXR1cm4gdGhpcy5fZnV0dXJlO1xuICB9XG5cbiAgc2V0IGZ1dHVyZShcbiAgICB2YWx1ZTogS2VybmVsLklTaGVsbEZ1dHVyZTxcbiAgICAgIEtlcm5lbE1lc3NhZ2UuSUV4ZWN1dGVSZXF1ZXN0TXNnLFxuICAgICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcGx5TXNnXG4gICAgPlxuICApIHtcbiAgICAvLyBCYWlsIGlmIHRoZSBtb2RlbCBpcyBkaXNwb3NlZC5cbiAgICBpZiAodGhpcy5tb2RlbC5pc0Rpc3Bvc2VkKSB7XG4gICAgICB0aHJvdyBFcnJvcignTW9kZWwgaXMgZGlzcG9zZWQnKTtcbiAgICB9XG4gICAgaWYgKHRoaXMuX2Z1dHVyZSA9PT0gdmFsdWUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKHRoaXMuX2Z1dHVyZSkge1xuICAgICAgdGhpcy5fZnV0dXJlLmRpc3Bvc2UoKTtcbiAgICB9XG4gICAgdGhpcy5fZnV0dXJlID0gdmFsdWU7XG5cbiAgICB0aGlzLm1vZGVsLmNsZWFyKCk7XG5cbiAgICAvLyBNYWtlIHN1cmUgdGhlcmUgd2VyZSBubyBpbnB1dCB3aWRnZXRzLlxuICAgIGlmICh0aGlzLndpZGdldHMubGVuZ3RoKSB7XG4gICAgICB0aGlzLl9jbGVhcigpO1xuICAgICAgdGhpcy5vdXRwdXRMZW5ndGhDaGFuZ2VkLmVtaXQoXG4gICAgICAgIE1hdGgubWluKHRoaXMubW9kZWwubGVuZ3RoLCB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzKVxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvLyBIYW5kbGUgcHVibGlzaGVkIG1lc3NhZ2VzLlxuICAgIHZhbHVlLm9uSU9QdWIgPSB0aGlzLl9vbklPUHViO1xuXG4gICAgLy8gSGFuZGxlIHRoZSBleGVjdXRlIHJlcGx5LlxuICAgIHZhbHVlLm9uUmVwbHkgPSB0aGlzLl9vbkV4ZWN1dGVSZXBseTtcblxuICAgIC8vIEhhbmRsZSBzdGRpbi5cbiAgICB2YWx1ZS5vblN0ZGluID0gbXNnID0+IHtcbiAgICAgIGlmIChLZXJuZWxNZXNzYWdlLmlzSW5wdXRSZXF1ZXN0TXNnKG1zZykpIHtcbiAgICAgICAgdGhpcy5vbklucHV0UmVxdWVzdChtc2csIHZhbHVlKTtcbiAgICAgIH1cbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIFNpZ25hbCBlbWl0dGVkIHdoZW4gYW4gb3V0cHV0IGFyZWEgaXMgcmVxdWVzdGluZyBhbiBpbnB1dC5cbiAgICovXG4gIGdldCBpbnB1dFJlcXVlc3RlZCgpOiBJU2lnbmFsPE91dHB1dEFyZWEsIHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5faW5wdXRSZXF1ZXN0ZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG1heGltdW0gbnVtYmVyIG9mIG91dHB1dCBpdGVtcyB0byBkaXNwbGF5IG9uIHRvcCBhbmQgYm90dG9tIG9mIGNlbGwgb3V0cHV0LlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogSXQgaXMgc2V0IHRvIEluZmluaXR5IGlmIG5vIHRyaW0gaXMgYXBwbGllZC5cbiAgICovXG4gIGdldCBtYXhOdW1iZXJPdXRwdXRzKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX21heE51bWJlck91dHB1dHM7XG4gIH1cbiAgc2V0IG1heE51bWJlck91dHB1dHMobGltaXQ6IG51bWJlcikge1xuICAgIGlmIChsaW1pdCA8PSAwKSB7XG4gICAgICBjb25zb2xlLndhcm4oYE91dHB1dEFyZWEubWF4TnVtYmVyT3V0cHV0cyBtdXN0IGJlIHN0cmljdGx5IHBvc2l0aXZlLmApO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBsYXN0U2hvd24gPSB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzO1xuICAgIHRoaXMuX21heE51bWJlck91dHB1dHMgPSBsaW1pdDtcbiAgICBpZiAobGFzdFNob3duIDwgbGltaXQpIHtcbiAgICAgIHRoaXMuX3Nob3dUcmltbWVkT3V0cHV0cyhsYXN0U2hvd24pO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgdXNlZCBieSB0aGUgb3V0cHV0IGFyZWEuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9mdXR1cmUpIHtcbiAgICAgIHRoaXMuX2Z1dHVyZS5kaXNwb3NlKCk7XG4gICAgICB0aGlzLl9mdXR1cmUgPSBudWxsITtcbiAgICB9XG4gICAgdGhpcy5fZGlzcGxheUlkTWFwLmNsZWFyKCk7XG4gICAgdGhpcy5fb3V0cHV0VHJhY2tlci5kaXNwb3NlKCk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEZvbGxvdyBjaGFuZ2VzIG9uIHRoZSBtb2RlbCBzdGF0ZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbk1vZGVsQ2hhbmdlZChcbiAgICBzZW5kZXI6IElPdXRwdXRBcmVhTW9kZWwsXG4gICAgYXJnczogSU91dHB1dEFyZWFNb2RlbC5DaGFuZ2VkQXJnc1xuICApOiB2b2lkIHtcbiAgICBzd2l0Y2ggKGFyZ3MudHlwZSkge1xuICAgICAgY2FzZSAnYWRkJzpcbiAgICAgICAgdGhpcy5faW5zZXJ0T3V0cHV0KGFyZ3MubmV3SW5kZXgsIGFyZ3MubmV3VmFsdWVzWzBdKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdyZW1vdmUnOlxuICAgICAgICBpZiAodGhpcy53aWRnZXRzLmxlbmd0aCkge1xuICAgICAgICAgIC8vIGFsbCBpdGVtcyByZW1vdmVkIGZyb20gbW9kZWxcbiAgICAgICAgICBpZiAodGhpcy5tb2RlbC5sZW5ndGggPT09IDApIHtcbiAgICAgICAgICAgIHRoaXMuX2NsZWFyKCk7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIC8vIHJhbmdlIG9mIGl0ZW1zIHJlbW92ZWQgZnJvbSBtb2RlbFxuICAgICAgICAgICAgLy8gcmVtb3ZlIHdpZGdldHMgY29ycmVzcG9uZGluZyB0byByZW1vdmVkIG1vZGVsIGl0ZW1zXG4gICAgICAgICAgICBjb25zdCBzdGFydEluZGV4ID0gYXJncy5vbGRJbmRleDtcbiAgICAgICAgICAgIGZvciAoXG4gICAgICAgICAgICAgIGxldCBpID0gMDtcbiAgICAgICAgICAgICAgaSA8IGFyZ3Mub2xkVmFsdWVzLmxlbmd0aCAmJiBzdGFydEluZGV4IDwgdGhpcy53aWRnZXRzLmxlbmd0aDtcbiAgICAgICAgICAgICAgKytpXG4gICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdGhpcy53aWRnZXRzW3N0YXJ0SW5kZXhdO1xuICAgICAgICAgICAgICB3aWRnZXQucGFyZW50ID0gbnVsbDtcbiAgICAgICAgICAgICAgd2lkZ2V0LmRpc3Bvc2UoKTtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgLy8gYXBwbHkgaXRlbSBvZmZzZXQgdG8gdGFyZ2V0IG1vZGVsIGl0ZW0gaW5kaWNlcyBpbiBfZGlzcGxheUlkTWFwXG4gICAgICAgICAgICB0aGlzLl9tb3ZlRGlzcGxheUlkSW5kaWNlcyhzdGFydEluZGV4LCBhcmdzLm9sZFZhbHVlcy5sZW5ndGgpO1xuXG4gICAgICAgICAgICAvLyBwcmV2ZW50IGppdHRlciBjYXVzZWQgYnkgaW1tZWRpYXRlIGhlaWdodCBjaGFuZ2VcbiAgICAgICAgICAgIHRoaXMuX3ByZXZlbnRIZWlnaHRDaGFuZ2VKaXR0ZXIoKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdzZXQnOlxuICAgICAgICB0aGlzLl9zZXRPdXRwdXQoYXJncy5uZXdJbmRleCwgYXJncy5uZXdWYWx1ZXNbMF0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgICB0aGlzLm91dHB1dExlbmd0aENoYW5nZWQuZW1pdChcbiAgICAgIE1hdGgubWluKHRoaXMubW9kZWwubGVuZ3RoLCB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogRW1pdHRlZCB3aGVuIHVzZXIgcmVxdWVzdHMgdG9nZ2xpbmcgb2YgdGhlIG91dHB1dCBzY3JvbGxpbmcgbW9kZS5cbiAgICovXG4gIGdldCB0b2dnbGVTY3JvbGxpbmcoKTogSVNpZ25hbDxPdXRwdXRBcmVhLCB2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3RvZ2dsZVNjcm9sbGluZztcbiAgfVxuXG4gIGdldCBpbml0aWFsaXplKCk6IElTaWduYWw8T3V0cHV0QXJlYSwgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9pbml0aWFsaXplO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBvdmVybGF5IGFsbG93aW5nIHRvIHRvZ2dsZSBzY3JvbGxpbmcuXG4gICAqL1xuICBwcml2YXRlIF9hZGRQcm9tcHRPdmVybGF5KCkge1xuICAgIGNvbnN0IG92ZXJsYXkgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICBvdmVybGF5LmNsYXNzTmFtZSA9IE9VVFBVVF9QUk9NUFRfT1ZFUkxBWTtcbiAgICBvdmVybGF5LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgKCkgPT4ge1xuICAgICAgdGhpcy5fdG9nZ2xlU2Nyb2xsaW5nLmVtaXQoKTtcbiAgICB9KTtcbiAgICB0aGlzLm5vZGUuYXBwZW5kQ2hpbGQob3ZlcmxheSk7XG4gICAgcmVxdWVzdEFuaW1hdGlvbkZyYW1lKCgpID0+IHtcbiAgICAgIHRoaXMuX2luaXRpYWxpemUuZW1pdCgpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSBpbmRpY2VzIGluIF9kaXNwbGF5SWRNYXAgaW4gcmVzcG9uc2UgdG8gZWxlbWVudCByZW1vdmUgZnJvbSBtb2RlbCBpdGVtc1xuICAgKlxuICAgKiBAcGFyYW0gc3RhcnRJbmRleCAtIFRoZSBpbmRleCBvZiBmaXJzdCBlbGVtZW50IHJlbW92ZWRcbiAgICpcbiAgICogQHBhcmFtIGNvdW50IC0gVGhlIG51bWJlciBvZiBlbGVtZW50cyByZW1vdmVkIGZyb20gbW9kZWwgaXRlbXNcbiAgICpcbiAgICovXG4gIHByaXZhdGUgX21vdmVEaXNwbGF5SWRJbmRpY2VzKHN0YXJ0SW5kZXg6IG51bWJlciwgY291bnQ6IG51bWJlcikge1xuICAgIHRoaXMuX2Rpc3BsYXlJZE1hcC5mb3JFYWNoKChpbmRpY2VzOiBudW1iZXJbXSkgPT4ge1xuICAgICAgY29uc3QgcmFuZ2VFbmQgPSBzdGFydEluZGV4ICsgY291bnQ7XG4gICAgICBjb25zdCBudW1JbmRpY2VzID0gaW5kaWNlcy5sZW5ndGg7XG4gICAgICAvLyByZXZlcnNlIGxvb3AgaW4gb3JkZXIgdG8gcHJldmVudCByZW1vdmluZyBlbGVtZW50IGFmZmVjdGluZyB0aGUgaW5kZXhcbiAgICAgIGZvciAobGV0IGkgPSBudW1JbmRpY2VzIC0gMTsgaSA+PSAwOyAtLWkpIHtcbiAgICAgICAgY29uc3QgaW5kZXggPSBpbmRpY2VzW2ldO1xuICAgICAgICAvLyByZW1vdmUgbW9kZWwgaXRlbSBpbmRpY2VzIGluIHJlbW92ZWQgcmFuZ2VcbiAgICAgICAgaWYgKGluZGV4ID49IHN0YXJ0SW5kZXggJiYgaW5kZXggPCByYW5nZUVuZCkge1xuICAgICAgICAgIGluZGljZXMuc3BsaWNlKGksIDEpO1xuICAgICAgICB9IGVsc2UgaWYgKGluZGV4ID49IHJhbmdlRW5kKSB7XG4gICAgICAgICAgLy8gbW92ZSBtb2RlbCBpdGVtIGluZGljZXMgdGhhdCB3ZXJlIGxhcmdlciB0aGFuIHJhbmdlIGVuZFxuICAgICAgICAgIGluZGljZXNbaV0gLT0gY291bnQ7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGb2xsb3cgY2hhbmdlcyBvbiB0aGUgb3V0cHV0IG1vZGVsIHN0YXRlLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uU3RhdGVDaGFuZ2VkKFxuICAgIHNlbmRlcjogSU91dHB1dEFyZWFNb2RlbCxcbiAgICBjaGFuZ2U6IG51bWJlciB8IHZvaWRcbiAgKTogdm9pZCB7XG4gICAgY29uc3Qgb3V0cHV0TGVuZ3RoID0gTWF0aC5taW4odGhpcy5tb2RlbC5sZW5ndGgsIHRoaXMuX21heE51bWJlck91dHB1dHMpO1xuICAgIGlmIChjaGFuZ2UpIHtcbiAgICAgIGlmIChjaGFuZ2UgPj0gdGhpcy5fbWF4TnVtYmVyT3V0cHV0cykge1xuICAgICAgICAvLyBCYWlsIGVhcmx5XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRoaXMuX3NldE91dHB1dChjaGFuZ2UsIHRoaXMubW9kZWwuZ2V0KGNoYW5nZSkpO1xuICAgIH0gZWxzZSB7XG4gICAgICBmb3IgKGxldCBpID0gMDsgaSA8IG91dHB1dExlbmd0aDsgaSsrKSB7XG4gICAgICAgIHRoaXMuX3NldE91dHB1dChpLCB0aGlzLm1vZGVsLmdldChpKSk7XG4gICAgICB9XG4gICAgfVxuICAgIHRoaXMub3V0cHV0TGVuZ3RoQ2hhbmdlZC5lbWl0KG91dHB1dExlbmd0aCk7XG4gIH1cblxuICAvKipcbiAgICogQ2xlYXIgdGhlIHdpZGdldCBvdXRwdXRzLlxuICAgKi9cbiAgcHJpdmF0ZSBfY2xlYXIoKTogdm9pZCB7XG4gICAgLy8gQmFpbCBpZiB0aGVyZSBpcyBubyB3b3JrIHRvIGRvLlxuICAgIGlmICghdGhpcy53aWRnZXRzLmxlbmd0aCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIC8vIFJlbW92ZSBhbGwgb2Ygb3VyIHdpZGdldHMuXG4gICAgY29uc3QgbGVuZ3RoID0gdGhpcy53aWRnZXRzLmxlbmd0aDtcbiAgICBmb3IgKGxldCBpID0gMDsgaSA8IGxlbmd0aDsgaSsrKSB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0aGlzLndpZGdldHNbMF07XG4gICAgICB3aWRnZXQucGFyZW50ID0gbnVsbDtcbiAgICAgIHdpZGdldC5kaXNwb3NlKCk7XG4gICAgfVxuXG4gICAgLy8gQ2xlYXIgdGhlIGRpc3BsYXkgaWQgbWFwLlxuICAgIHRoaXMuX2Rpc3BsYXlJZE1hcC5jbGVhcigpO1xuXG4gICAgLy8gcHJldmVudCBqaXR0ZXIgY2F1c2VkIGJ5IGltbWVkaWF0ZSBoZWlnaHQgY2hhbmdlXG4gICAgdGhpcy5fcHJldmVudEhlaWdodENoYW5nZUppdHRlcigpO1xuICB9XG5cbiAgcHJpdmF0ZSBfcHJldmVudEhlaWdodENoYW5nZUppdHRlcigpIHtcbiAgICAvLyBXaGVuIGFuIG91dHB1dCBhcmVhIGlzIGNsZWFyZWQgYW5kIHRoZW4gcXVpY2tseSByZXBsYWNlZCB3aXRoIG5ld1xuICAgIC8vIGNvbnRlbnQgKGFzIGhhcHBlbnMgd2l0aCBAaW50ZXJhY3QgaW4gd2lkZ2V0cywgZm9yIGV4YW1wbGUpLCB0aGVcbiAgICAvLyBxdWlja2x5IGNoYW5naW5nIGhlaWdodCBjYW4gbWFrZSB0aGUgcGFnZSBqaXR0ZXIuXG4gICAgLy8gV2UgaW50cm9kdWNlIGEgc21hbGwgZGVsYXkgaW4gdGhlIG1pbmltdW0gaGVpZ2h0XG4gICAgLy8gdG8gcHJldmVudCB0aGlzIGppdHRlci5cbiAgICBjb25zdCByZWN0ID0gdGhpcy5ub2RlLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xuICAgIHRoaXMubm9kZS5zdHlsZS5taW5IZWlnaHQgPSBgJHtyZWN0LmhlaWdodH1weGA7XG4gICAgaWYgKHRoaXMuX21pbkhlaWdodFRpbWVvdXQpIHtcbiAgICAgIHdpbmRvdy5jbGVhclRpbWVvdXQodGhpcy5fbWluSGVpZ2h0VGltZW91dCk7XG4gICAgfVxuICAgIHRoaXMuX21pbkhlaWdodFRpbWVvdXQgPSB3aW5kb3cuc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRoaXMubm9kZS5zdHlsZS5taW5IZWlnaHQgPSAnJztcbiAgICB9LCA1MCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFuIGlucHV0IHJlcXVlc3QgZnJvbSBhIGtlcm5lbC5cbiAgICovXG4gIHByb3RlY3RlZCBvbklucHV0UmVxdWVzdChcbiAgICBtc2c6IEtlcm5lbE1lc3NhZ2UuSUlucHV0UmVxdWVzdE1zZyxcbiAgICBmdXR1cmU6IEtlcm5lbC5JU2hlbGxGdXR1cmVcbiAgKTogdm9pZCB7XG4gICAgLy8gQWRkIGFuIG91dHB1dCB3aWRnZXQgdG8gdGhlIGVuZC5cbiAgICBjb25zdCBmYWN0b3J5ID0gdGhpcy5jb250ZW50RmFjdG9yeTtcbiAgICBjb25zdCBzdGRpblByb21wdCA9IG1zZy5jb250ZW50LnByb21wdDtcbiAgICBjb25zdCBwYXNzd29yZCA9IG1zZy5jb250ZW50LnBhc3N3b3JkO1xuXG4gICAgY29uc3QgcGFuZWwgPSBuZXcgUGFuZWwoKTtcbiAgICBwYW5lbC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9JVEVNX0NMQVNTKTtcbiAgICBwYW5lbC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9TVERJTl9JVEVNX0NMQVNTKTtcblxuICAgIGNvbnN0IHByb21wdCA9IGZhY3RvcnkuY3JlYXRlT3V0cHV0UHJvbXB0KCk7XG4gICAgcHJvbXB0LmFkZENsYXNzKE9VVFBVVF9BUkVBX1BST01QVF9DTEFTUyk7XG4gICAgcGFuZWwuYWRkV2lkZ2V0KHByb21wdCk7XG5cbiAgICBjb25zdCBpbnB1dCA9IGZhY3RvcnkuY3JlYXRlU3RkaW4oe1xuICAgICAgcGFyZW50X2hlYWRlcjogbXNnLmhlYWRlcixcbiAgICAgIHByb21wdDogc3RkaW5Qcm9tcHQsXG4gICAgICBwYXNzd29yZCxcbiAgICAgIGZ1dHVyZSxcbiAgICAgIHRyYW5zbGF0b3I6IHRoaXMuX3RyYW5zbGF0b3IsXG4gICAgICBpbnB1dEhpc3RvcnlTY29wZTogdGhpcy5faW5wdXRIaXN0b3J5U2NvcGVcbiAgICB9KTtcbiAgICBpbnB1dC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9PVVRQVVRfQ0xBU1MpO1xuICAgIHBhbmVsLmFkZFdpZGdldChpbnB1dCk7XG5cbiAgICAvLyBJbmNyZWFzZSBudW1iZXIgb2Ygb3V0cHV0cyB0byBkaXNwbGF5IHRoZSByZXN1bHQgdXAgdG8gdGhlIGlucHV0IHJlcXVlc3QuXG4gICAgaWYgKHRoaXMubW9kZWwubGVuZ3RoID49IHRoaXMubWF4TnVtYmVyT3V0cHV0cykge1xuICAgICAgdGhpcy5tYXhOdW1iZXJPdXRwdXRzID0gdGhpcy5tb2RlbC5sZW5ndGg7XG4gICAgfVxuICAgIHRoaXMubGF5b3V0LmFkZFdpZGdldChwYW5lbCk7XG5cbiAgICB0aGlzLl9pbnB1dFJlcXVlc3RlZC5lbWl0KCk7XG5cbiAgICAvKipcbiAgICAgKiBXYWl0IGZvciB0aGUgc3RkaW4gdG8gY29tcGxldGUsIGFkZCBpdCB0byB0aGUgbW9kZWwgKHNvIGl0IHBlcnNpc3RzKVxuICAgICAqIGFuZCByZW1vdmUgdGhlIHN0ZGluIHdpZGdldC5cbiAgICAgKi9cbiAgICB2b2lkIGlucHV0LnZhbHVlLnRoZW4odmFsdWUgPT4ge1xuICAgICAgLy8gSW5jcmVhc2UgbnVtYmVyIG9mIG91dHB1dHMgdG8gZGlzcGxheSB0aGUgcmVzdWx0IG9mIHN0ZGluIGlmIG5lZWRlZC5cbiAgICAgIGlmICh0aGlzLm1vZGVsLmxlbmd0aCA+PSB0aGlzLm1heE51bWJlck91dHB1dHMpIHtcbiAgICAgICAgdGhpcy5tYXhOdW1iZXJPdXRwdXRzID0gdGhpcy5tb2RlbC5sZW5ndGggKyAxO1xuICAgICAgfVxuICAgICAgLy8gVXNlIHN0ZGluIGFzIHRoZSBzdHJlYW0gc28gaXQgZG9lcyBub3QgZ2V0IGNvbWJpbmVkIHdpdGggc3Rkb3V0LlxuICAgICAgdGhpcy5tb2RlbC5hZGQoe1xuICAgICAgICBvdXRwdXRfdHlwZTogJ3N0cmVhbScsXG4gICAgICAgIG5hbWU6ICdzdGRpbicsXG4gICAgICAgIHRleHQ6IHZhbHVlICsgJ1xcbidcbiAgICAgIH0pO1xuICAgICAgcGFuZWwuZGlzcG9zZSgpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSBhbiBvdXRwdXQgaW4gdGhlIGxheW91dCBpbiBwbGFjZS5cbiAgICovXG4gIHByaXZhdGUgX3NldE91dHB1dChpbmRleDogbnVtYmVyLCBtb2RlbDogSU91dHB1dE1vZGVsKTogdm9pZCB7XG4gICAgaWYgKGluZGV4ID49IHRoaXMuX21heE51bWJlck91dHB1dHMpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgcGFuZWwgPSB0aGlzLmxheW91dC53aWRnZXRzW2luZGV4XSBhcyBQYW5lbDtcbiAgICBjb25zdCByZW5kZXJlciA9IChcbiAgICAgIHBhbmVsLndpZGdldHMgPyBwYW5lbC53aWRnZXRzWzFdIDogcGFuZWxcbiAgICApIGFzIElSZW5kZXJNaW1lLklSZW5kZXJlcjtcbiAgICAvLyBDaGVjayB3aGV0aGVyIGl0IGlzIHNhZmUgdG8gcmV1c2UgcmVuZGVyZXI6XG4gICAgLy8gLSBQcmVmZXJyZWQgbWltZSB0eXBlIGhhcyBub3QgY2hhbmdlZFxuICAgIC8vIC0gSXNvbGF0aW9uIGhhcyBub3QgY2hhbmdlZFxuICAgIGNvbnN0IG1pbWVUeXBlID0gdGhpcy5yZW5kZXJtaW1lLnByZWZlcnJlZE1pbWVUeXBlKFxuICAgICAgbW9kZWwuZGF0YSxcbiAgICAgIG1vZGVsLnRydXN0ZWQgPyAnYW55JyA6ICdlbnN1cmUnXG4gICAgKTtcbiAgICBpZiAoXG4gICAgICBQcml2YXRlLmN1cnJlbnRQcmVmZXJyZWRNaW1ldHlwZS5nZXQocmVuZGVyZXIpID09PSBtaW1lVHlwZSAmJlxuICAgICAgT3V0cHV0QXJlYS5pc0lzb2xhdGVkKG1pbWVUeXBlLCBtb2RlbC5tZXRhZGF0YSkgPT09XG4gICAgICAgIHJlbmRlcmVyIGluc3RhbmNlb2YgUHJpdmF0ZS5Jc29sYXRlZFJlbmRlcmVyXG4gICAgKSB7XG4gICAgICB2b2lkIHJlbmRlcmVyLnJlbmRlck1vZGVsKG1vZGVsKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5sYXlvdXQud2lkZ2V0c1tpbmRleF0uZGlzcG9zZSgpO1xuICAgICAgdGhpcy5faW5zZXJ0T3V0cHV0KGluZGV4LCBtb2RlbCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciBhbmQgaW5zZXJ0IGEgc2luZ2xlIG91dHB1dCBpbnRvIHRoZSBsYXlvdXQuXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBpbmRleCBvZiB0aGUgb3V0cHV0IHRvIGJlIGluc2VydGVkLlxuICAgKiBAcGFyYW0gbW9kZWwgLSBUaGUgbW9kZWwgb2YgdGhlIG91dHB1dCB0byBiZSBpbnNlcnRlZC5cbiAgICovXG4gIHByaXZhdGUgX2luc2VydE91dHB1dChpbmRleDogbnVtYmVyLCBtb2RlbDogSU91dHB1dE1vZGVsKTogdm9pZCB7XG4gICAgaWYgKGluZGV4ID4gdGhpcy5fbWF4TnVtYmVyT3V0cHV0cykge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IGxheW91dCA9IHRoaXMubGF5b3V0IGFzIFBhbmVsTGF5b3V0O1xuXG4gICAgaWYgKGluZGV4ID09PSB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzKSB7XG4gICAgICBjb25zdCB3YXJuaW5nID0gbmV3IFByaXZhdGUuVHJpbW1lZE91dHB1dHModGhpcy5fbWF4TnVtYmVyT3V0cHV0cywgKCkgPT4ge1xuICAgICAgICBjb25zdCBsYXN0U2hvd24gPSB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzO1xuICAgICAgICB0aGlzLl9tYXhOdW1iZXJPdXRwdXRzID0gSW5maW5pdHk7XG4gICAgICAgIHRoaXMuX3Nob3dUcmltbWVkT3V0cHV0cyhsYXN0U2hvd24pO1xuICAgICAgfSk7XG4gICAgICBsYXlvdXQuaW5zZXJ0V2lkZ2V0KGluZGV4LCB0aGlzLl93cmFwcGVkT3V0cHV0KHdhcm5pbmcpKTtcbiAgICB9IGVsc2Uge1xuICAgICAgbGV0IG91dHB1dCA9IHRoaXMuY3JlYXRlT3V0cHV0SXRlbShtb2RlbCk7XG4gICAgICBpZiAob3V0cHV0KSB7XG4gICAgICAgIG91dHB1dC50b2dnbGVDbGFzcyhFWEVDVVRFX0NMQVNTLCBtb2RlbC5leGVjdXRpb25Db3VudCAhPT0gbnVsbCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBvdXRwdXQgPSBuZXcgV2lkZ2V0KCk7XG4gICAgICB9XG5cbiAgICAgIGlmICghdGhpcy5fb3V0cHV0VHJhY2tlci5oYXMob3V0cHV0KSkge1xuICAgICAgICB2b2lkIHRoaXMuX291dHB1dFRyYWNrZXIuYWRkKG91dHB1dCk7XG4gICAgICB9XG4gICAgICBsYXlvdXQuaW5zZXJ0V2lkZ2V0KGluZGV4LCBvdXRwdXQpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBIHdpZGdldCB0cmFja2VyIGZvciBpbmRpdmlkdWFsIG91dHB1dCB3aWRnZXRzIGluIHRoZSBvdXRwdXQgYXJlYS5cbiAgICovXG4gIGdldCBvdXRwdXRUcmFja2VyKCk6IFdpZGdldFRyYWNrZXI8V2lkZ2V0PiB7XG4gICAgcmV0dXJuIHRoaXMuX291dHB1dFRyYWNrZXI7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBpbmZvcm1hdGlvbiBtZXNzYWdlIGFuZCBzaG93IG91dHB1dCBtb2RlbHMgZnJvbSB0aGUgZ2l2ZW5cbiAgICogaW5kZXggdG8gbWF4TnVtYmVyT3V0cHV0c1xuICAgKlxuICAgKiBAcGFyYW0gbGFzdFNob3duIFN0YXJ0aW5nIG1vZGVsIGluZGV4IHRvIGluc2VydC5cbiAgICovXG4gIHByaXZhdGUgX3Nob3dUcmltbWVkT3V0cHV0cyhsYXN0U2hvd246IG51bWJlcikge1xuICAgIC8vIERpc3Bvc2UgaW5mb3JtYXRpb24gd2lkZ2V0XG4gICAgdGhpcy53aWRnZXRzW2xhc3RTaG93bl0uZGlzcG9zZSgpO1xuXG4gICAgZm9yIChsZXQgaWR4ID0gbGFzdFNob3duOyBpZHggPCB0aGlzLm1vZGVsLmxlbmd0aDsgaWR4KyspIHtcbiAgICAgIHRoaXMuX2luc2VydE91dHB1dChpZHgsIHRoaXMubW9kZWwuZ2V0KGlkeCkpO1xuICAgIH1cblxuICAgIHRoaXMub3V0cHV0TGVuZ3RoQ2hhbmdlZC5lbWl0KFxuICAgICAgTWF0aC5taW4odGhpcy5tb2RlbC5sZW5ndGgsIHRoaXMuX21heE51bWJlck91dHB1dHMpXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYW4gb3V0cHV0IGl0ZW0gd2l0aCBhIHByb21wdCBhbmQgYWN0dWFsIG91dHB1dFxuICAgKlxuICAgKiBAcmV0dXJucyBhIHJlbmRlcmVkIHdpZGdldCwgb3IgbnVsbCBpZiB3ZSBjYW5ub3QgcmVuZGVyXG4gICAqICMjIyMgTm90ZXNcbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVPdXRwdXRJdGVtKG1vZGVsOiBJT3V0cHV0TW9kZWwpOiBXaWRnZXQgfCBudWxsIHtcbiAgICBjb25zdCBvdXRwdXQgPSB0aGlzLmNyZWF0ZVJlbmRlcmVkTWltZXR5cGUobW9kZWwpO1xuXG4gICAgaWYgKCFvdXRwdXQpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cblxuICAgIHJldHVybiB0aGlzLl93cmFwcGVkT3V0cHV0KG91dHB1dCwgbW9kZWwuZXhlY3V0aW9uQ291bnQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciBhIG1pbWV0eXBlXG4gICAqL1xuICBwcm90ZWN0ZWQgY3JlYXRlUmVuZGVyZWRNaW1ldHlwZShtb2RlbDogSU91dHB1dE1vZGVsKTogV2lkZ2V0IHwgbnVsbCB7XG4gICAgY29uc3QgbWltZVR5cGUgPSB0aGlzLnJlbmRlcm1pbWUucHJlZmVycmVkTWltZVR5cGUoXG4gICAgICBtb2RlbC5kYXRhLFxuICAgICAgbW9kZWwudHJ1c3RlZCA/ICdhbnknIDogJ2Vuc3VyZSdcbiAgICApO1xuXG4gICAgaWYgKCFtaW1lVHlwZSkge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIGxldCBvdXRwdXQgPSB0aGlzLnJlbmRlcm1pbWUuY3JlYXRlUmVuZGVyZXIobWltZVR5cGUpO1xuICAgIGNvbnN0IGlzb2xhdGVkID0gT3V0cHV0QXJlYS5pc0lzb2xhdGVkKG1pbWVUeXBlLCBtb2RlbC5tZXRhZGF0YSk7XG4gICAgaWYgKGlzb2xhdGVkID09PSB0cnVlKSB7XG4gICAgICBvdXRwdXQgPSBuZXcgUHJpdmF0ZS5Jc29sYXRlZFJlbmRlcmVyKG91dHB1dCk7XG4gICAgfVxuICAgIFByaXZhdGUuY3VycmVudFByZWZlcnJlZE1pbWV0eXBlLnNldChvdXRwdXQsIG1pbWVUeXBlKTtcbiAgICBvdXRwdXQucmVuZGVyTW9kZWwobW9kZWwpLmNhdGNoKGVycm9yID0+IHtcbiAgICAgIC8vIE1hbnVhbGx5IGFwcGVuZCBlcnJvciBtZXNzYWdlIHRvIG91dHB1dFxuICAgICAgY29uc3QgcHJlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncHJlJyk7XG4gICAgICBjb25zdCB0cmFucyA9IHRoaXMuX3RyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgICAgcHJlLnRleHRDb250ZW50ID0gdHJhbnMuX18oJ0phdmFzY3JpcHQgRXJyb3I6ICUxJywgZXJyb3IubWVzc2FnZSk7XG4gICAgICBvdXRwdXQubm9kZS5hcHBlbmRDaGlsZChwcmUpO1xuXG4gICAgICAvLyBSZW1vdmUgbWltZS10eXBlLXNwZWNpZmljIENTUyBjbGFzc2VzXG4gICAgICBvdXRwdXQubm9kZS5jbGFzc05hbWUgPSAnbG0tV2lkZ2V0IGpwLVJlbmRlcmVkVGV4dCc7XG4gICAgICBvdXRwdXQubm9kZS5zZXRBdHRyaWJ1dGUoXG4gICAgICAgICdkYXRhLW1pbWUtdHlwZScsXG4gICAgICAgICdhcHBsaWNhdGlvbi92bmQuanVweXRlci5zdGRlcnInXG4gICAgICApO1xuICAgIH0pO1xuICAgIHJldHVybiBvdXRwdXQ7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFuIGlvcHViIG1lc3NhZ2UuXG4gICAqL1xuICBwcml2YXRlIF9vbklPUHViID0gKG1zZzogS2VybmVsTWVzc2FnZS5JSU9QdWJNZXNzYWdlKSA9PiB7XG4gICAgY29uc3QgbW9kZWwgPSB0aGlzLm1vZGVsO1xuICAgIGNvbnN0IG1zZ1R5cGUgPSBtc2cuaGVhZGVyLm1zZ190eXBlO1xuICAgIGxldCBvdXRwdXQ6IG5iZm9ybWF0LklPdXRwdXQ7XG4gICAgY29uc3QgdHJhbnNpZW50ID0gKChtc2cuY29udGVudCBhcyBhbnkpLnRyYW5zaWVudCB8fCB7fSkgYXMgSlNPTk9iamVjdDtcbiAgICBjb25zdCBkaXNwbGF5SWQgPSB0cmFuc2llbnRbJ2Rpc3BsYXlfaWQnXSBhcyBzdHJpbmc7XG4gICAgbGV0IHRhcmdldHM6IG51bWJlcltdIHwgdW5kZWZpbmVkO1xuXG4gICAgc3dpdGNoIChtc2dUeXBlKSB7XG4gICAgICBjYXNlICdleGVjdXRlX3Jlc3VsdCc6XG4gICAgICBjYXNlICdkaXNwbGF5X2RhdGEnOlxuICAgICAgY2FzZSAnc3RyZWFtJzpcbiAgICAgIGNhc2UgJ2Vycm9yJzpcbiAgICAgICAgb3V0cHV0ID0geyAuLi5tc2cuY29udGVudCwgb3V0cHV0X3R5cGU6IG1zZ1R5cGUgfTtcbiAgICAgICAgbW9kZWwuYWRkKG91dHB1dCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnY2xlYXJfb3V0cHV0Jzoge1xuICAgICAgICBjb25zdCB3YWl0ID0gKG1zZyBhcyBLZXJuZWxNZXNzYWdlLklDbGVhck91dHB1dE1zZykuY29udGVudC53YWl0O1xuICAgICAgICBtb2RlbC5jbGVhcih3YWl0KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgICBjYXNlICd1cGRhdGVfZGlzcGxheV9kYXRhJzpcbiAgICAgICAgb3V0cHV0ID0geyAuLi5tc2cuY29udGVudCwgb3V0cHV0X3R5cGU6ICdkaXNwbGF5X2RhdGEnIH07XG4gICAgICAgIHRhcmdldHMgPSB0aGlzLl9kaXNwbGF5SWRNYXAuZ2V0KGRpc3BsYXlJZCk7XG4gICAgICAgIGlmICh0YXJnZXRzKSB7XG4gICAgICAgICAgZm9yIChjb25zdCBpbmRleCBvZiB0YXJnZXRzKSB7XG4gICAgICAgICAgICBtb2RlbC5zZXQoaW5kZXgsIG91dHB1dCk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICAgIGlmIChkaXNwbGF5SWQgJiYgbXNnVHlwZSA9PT0gJ2Rpc3BsYXlfZGF0YScpIHtcbiAgICAgIHRhcmdldHMgPSB0aGlzLl9kaXNwbGF5SWRNYXAuZ2V0KGRpc3BsYXlJZCkgfHwgW107XG4gICAgICB0YXJnZXRzLnB1c2gobW9kZWwubGVuZ3RoIC0gMSk7XG4gICAgICB0aGlzLl9kaXNwbGF5SWRNYXAuc2V0KGRpc3BsYXlJZCwgdGFyZ2V0cyk7XG4gICAgfVxuICB9O1xuXG4gIC8qKlxuICAgKiBIYW5kbGUgYW4gZXhlY3V0ZSByZXBseSBtZXNzYWdlLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25FeGVjdXRlUmVwbHkgPSAobXNnOiBLZXJuZWxNZXNzYWdlLklFeGVjdXRlUmVwbHlNc2cpID0+IHtcbiAgICAvLyBBUEkgcmVzcG9uc2VzIHRoYXQgY29udGFpbiBhIHBhZ2VyIGFyZSBzcGVjaWFsIGNhc2VkIGFuZCB0aGVpciB0eXBlXG4gICAgLy8gaXMgb3ZlcnJpZGRlbiBmcm9tICdleGVjdXRlX3JlcGx5JyB0byAnZGlzcGxheV9kYXRhJyBpbiBvcmRlciB0b1xuICAgIC8vIHJlbmRlciBvdXRwdXQuXG4gICAgY29uc3QgbW9kZWwgPSB0aGlzLm1vZGVsO1xuICAgIGNvbnN0IGNvbnRlbnQgPSBtc2cuY29udGVudDtcbiAgICBpZiAoY29udGVudC5zdGF0dXMgIT09ICdvaycpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgcGF5bG9hZCA9IGNvbnRlbnQgJiYgY29udGVudC5wYXlsb2FkO1xuICAgIGlmICghcGF5bG9hZCB8fCAhcGF5bG9hZC5sZW5ndGgpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgcGFnZXMgPSBwYXlsb2FkLmZpbHRlcigoaTogYW55KSA9PiAoaSBhcyBhbnkpLnNvdXJjZSA9PT0gJ3BhZ2UnKTtcbiAgICBpZiAoIXBhZ2VzLmxlbmd0aCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBwYWdlID0gSlNPTi5wYXJzZShKU09OLnN0cmluZ2lmeShwYWdlc1swXSkpO1xuICAgIGNvbnN0IG91dHB1dDogbmJmb3JtYXQuSU91dHB1dCA9IHtcbiAgICAgIG91dHB1dF90eXBlOiAnZGlzcGxheV9kYXRhJyxcbiAgICAgIGRhdGE6IChwYWdlIGFzIGFueSkuZGF0YSBhcyBuYmZvcm1hdC5JTWltZUJ1bmRsZSxcbiAgICAgIG1ldGFkYXRhOiB7fVxuICAgIH07XG4gICAgbW9kZWwuYWRkKG91dHB1dCk7XG4gIH07XG5cbiAgLyoqXG4gICAqIFdyYXAgYSBvdXRwdXQgd2lkZ2V0IHdpdGhpbiBhIG91dHB1dCBwYW5lbFxuICAgKlxuICAgKiBAcGFyYW0gb3V0cHV0IE91dHB1dCB3aWRnZXQgdG8gd3JhcFxuICAgKiBAcGFyYW0gZXhlY3V0aW9uQ291bnQgRXhlY3V0aW9uIGNvdW50XG4gICAqIEByZXR1cm5zIFRoZSBvdXRwdXQgcGFuZWxcbiAgICovXG4gIHByaXZhdGUgX3dyYXBwZWRPdXRwdXQoXG4gICAgb3V0cHV0OiBXaWRnZXQsXG4gICAgZXhlY3V0aW9uQ291bnQ6IG51bWJlciB8IG51bGwgPSBudWxsXG4gICk6IFBhbmVsIHtcbiAgICBjb25zdCBwYW5lbCA9IG5ldyBQcml2YXRlLk91dHB1dFBhbmVsKCk7XG4gICAgcGFuZWwuYWRkQ2xhc3MoT1VUUFVUX0FSRUFfSVRFTV9DTEFTUyk7XG5cbiAgICBjb25zdCBwcm9tcHQgPSB0aGlzLmNvbnRlbnRGYWN0b3J5LmNyZWF0ZU91dHB1dFByb21wdCgpO1xuICAgIHByb21wdC5leGVjdXRpb25Db3VudCA9IGV4ZWN1dGlvbkNvdW50O1xuICAgIHByb21wdC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9QUk9NUFRfQ0xBU1MpO1xuICAgIHBhbmVsLmFkZFdpZGdldChwcm9tcHQpO1xuXG4gICAgb3V0cHV0LmFkZENsYXNzKE9VVFBVVF9BUkVBX09VVFBVVF9DTEFTUyk7XG4gICAgcGFuZWwuYWRkV2lkZ2V0KG91dHB1dCk7XG4gICAgcmV0dXJuIHBhbmVsO1xuICB9XG5cbiAgcHJpdmF0ZSBfZGlzcGxheUlkTWFwID0gbmV3IE1hcDxzdHJpbmcsIG51bWJlcltdPigpO1xuICBwcml2YXRlIF9mdXR1cmU6IEtlcm5lbC5JU2hlbGxGdXR1cmU8XG4gICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcXVlc3RNc2csXG4gICAgS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcGx5TXNnXG4gID47XG4gIC8qKlxuICAgKiBUaGUgbWF4aW11bSBvdXRwdXRzIHRvIHNob3cgaW4gdGhlIHRyaW1tZWRcbiAgICogb3V0cHV0IGFyZWEuXG4gICAqL1xuICBwcml2YXRlIF9tYXhOdW1iZXJPdXRwdXRzOiBudW1iZXI7XG4gIHByaXZhdGUgX21pbkhlaWdodFRpbWVvdXQ6IG51bWJlciB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9pbnB1dFJlcXVlc3RlZCA9IG5ldyBTaWduYWw8T3V0cHV0QXJlYSwgdm9pZD4odGhpcyk7XG4gIHByaXZhdGUgX3RvZ2dsZVNjcm9sbGluZyA9IG5ldyBTaWduYWw8T3V0cHV0QXJlYSwgdm9pZD4odGhpcyk7XG4gIHByaXZhdGUgX2luaXRpYWxpemUgPSBuZXcgU2lnbmFsPE91dHB1dEFyZWEsIHZvaWQ+KHRoaXMpO1xuICBwcml2YXRlIF9vdXRwdXRUcmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8V2lkZ2V0Pih7XG4gICAgbmFtZXNwYWNlOiBVVUlELnV1aWQ0KClcbiAgfSk7XG4gIHByaXZhdGUgX3RyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9pbnB1dEhpc3RvcnlTY29wZTogJ2dsb2JhbCcgfCAnc2Vzc2lvbicgPSAnZ2xvYmFsJztcbn1cblxuZXhwb3J0IGNsYXNzIFNpbXBsaWZpZWRPdXRwdXRBcmVhIGV4dGVuZHMgT3V0cHV0QXJlYSB7XG4gIC8qKlxuICAgKiBIYW5kbGUgYW4gaW5wdXQgcmVxdWVzdCBmcm9tIGEga2VybmVsIGJ5IGRvaW5nIG5vdGhpbmcuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25JbnB1dFJlcXVlc3QoXG4gICAgbXNnOiBLZXJuZWxNZXNzYWdlLklJbnB1dFJlcXVlc3RNc2csXG4gICAgZnV0dXJlOiBLZXJuZWwuSVNoZWxsRnV0dXJlXG4gICk6IHZvaWQge1xuICAgIHJldHVybjtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYW4gb3V0cHV0IGl0ZW0gd2l0aG91dCBhIHByb21wdCwganVzdCB0aGUgb3V0cHV0IHdpZGdldHNcbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVPdXRwdXRJdGVtKG1vZGVsOiBJT3V0cHV0TW9kZWwpOiBXaWRnZXQgfCBudWxsIHtcbiAgICBjb25zdCBvdXRwdXQgPSB0aGlzLmNyZWF0ZVJlbmRlcmVkTWltZXR5cGUobW9kZWwpO1xuXG4gICAgaWYgKCFvdXRwdXQpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cblxuICAgIGNvbnN0IHBhbmVsID0gbmV3IFByaXZhdGUuT3V0cHV0UGFuZWwoKTtcbiAgICBwYW5lbC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9JVEVNX0NMQVNTKTtcblxuICAgIG91dHB1dC5hZGRDbGFzcyhPVVRQVVRfQVJFQV9PVVRQVVRfQ0xBU1MpO1xuICAgIHBhbmVsLmFkZFdpZGdldChvdXRwdXQpO1xuICAgIHJldHVybiBwYW5lbDtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBPdXRwdXRBcmVhIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgT3V0cHV0QXJlYSB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB0byBjcmVhdGUgYW4gYE91dHB1dEFyZWFgLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIG1vZGVsIHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICAgKi9cbiAgICBtb2RlbDogSU91dHB1dEFyZWFNb2RlbDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjb250ZW50IGZhY3RvcnkgdXNlZCBieSB0aGUgd2lkZ2V0IHRvIGNyZWF0ZSBjaGlsZHJlbi5cbiAgICAgKi9cbiAgICBjb250ZW50RmFjdG9yeT86IElDb250ZW50RmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZW5kZXJtaW1lIGluc3RhbmNlIHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICAgKi9cbiAgICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1heGltdW0gbnVtYmVyIG9mIG91dHB1dCBpdGVtcyB0byBkaXNwbGF5IG9uIHRvcCBhbmQgYm90dG9tIG9mIGNlbGwgb3V0cHV0LlxuICAgICAqL1xuICAgIG1heE51bWJlck91dHB1dHM/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIHNob3cgcHJvbXB0IG92ZXJsYXkgZW1pdHRpbmcgYHRvZ2dsZVNjcm9sbGluZ2Agc2lnbmFsLlxuICAgICAqL1xuICAgIHByb21wdE92ZXJsYXk/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVHJhbnNsYXRvclxuICAgICAqL1xuICAgIHJlYWRvbmx5IHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gc3BsaXQgc3RkaW4gbGluZSBoaXN0b3J5IGJ5IGtlcm5lbCBzZXNzaW9uIG9yIGtlZXAgZ2xvYmFsbHkgYWNjZXNzaWJsZS5cbiAgICAgKi9cbiAgICBpbnB1dEhpc3RvcnlTY29wZT86ICdnbG9iYWwnIHwgJ3Nlc3Npb24nO1xuICB9XG5cbiAgLyoqXG4gICAqIEV4ZWN1dGUgY29kZSBvbiBhbiBvdXRwdXQgYXJlYS5cbiAgICovXG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiBleGVjdXRlKFxuICAgIGNvZGU6IHN0cmluZyxcbiAgICBvdXRwdXQ6IE91dHB1dEFyZWEsXG4gICAgc2Vzc2lvbkNvbnRleHQ6IElTZXNzaW9uQ29udGV4dCxcbiAgICBtZXRhZGF0YT86IEpTT05PYmplY3RcbiAgKTogUHJvbWlzZTxLZXJuZWxNZXNzYWdlLklFeGVjdXRlUmVwbHlNc2cgfCB1bmRlZmluZWQ+IHtcbiAgICAvLyBPdmVycmlkZSB0aGUgZGVmYXVsdCBmb3IgYHN0b3Bfb25fZXJyb3JgLlxuICAgIGxldCBzdG9wT25FcnJvciA9IHRydWU7XG4gICAgaWYgKFxuICAgICAgbWV0YWRhdGEgJiZcbiAgICAgIEFycmF5LmlzQXJyYXkobWV0YWRhdGEudGFncykgJiZcbiAgICAgIG1ldGFkYXRhLnRhZ3MuaW5kZXhPZigncmFpc2VzLWV4Y2VwdGlvbicpICE9PSAtMVxuICAgICkge1xuICAgICAgc3RvcE9uRXJyb3IgPSBmYWxzZTtcbiAgICB9XG4gICAgY29uc3QgY29udGVudDogS2VybmVsTWVzc2FnZS5JRXhlY3V0ZVJlcXVlc3RNc2dbJ2NvbnRlbnQnXSA9IHtcbiAgICAgIGNvZGUsXG4gICAgICBzdG9wX29uX2Vycm9yOiBzdG9wT25FcnJvclxuICAgIH07XG5cbiAgICBjb25zdCBrZXJuZWwgPSBzZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgaWYgKCFrZXJuZWwpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignU2Vzc2lvbiBoYXMgbm8ga2VybmVsLicpO1xuICAgIH1cbiAgICBjb25zdCBmdXR1cmUgPSBrZXJuZWwucmVxdWVzdEV4ZWN1dGUoY29udGVudCwgZmFsc2UsIG1ldGFkYXRhKTtcbiAgICBvdXRwdXQuZnV0dXJlID0gZnV0dXJlO1xuICAgIHJldHVybiBmdXR1cmUuZG9uZTtcbiAgfVxuXG4gIGV4cG9ydCBmdW5jdGlvbiBpc0lzb2xhdGVkKFxuICAgIG1pbWVUeXBlOiBzdHJpbmcsXG4gICAgbWV0YWRhdGE6IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3RcbiAgKTogYm9vbGVhbiB7XG4gICAgY29uc3QgbWltZU1kID0gbWV0YWRhdGFbbWltZVR5cGVdIGFzIFJlYWRvbmx5SlNPTk9iamVjdCB8IHVuZGVmaW5lZDtcbiAgICAvLyBtaW1lLXNwZWNpZmljIGhpZ2hlciBwcmlvcml0eVxuICAgIGlmIChtaW1lTWQgJiYgbWltZU1kWydpc29sYXRlZCddICE9PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybiAhIW1pbWVNZFsnaXNvbGF0ZWQnXTtcbiAgICB9IGVsc2Uge1xuICAgICAgLy8gZmFsbGJhY2sgb24gZ2xvYmFsXG4gICAgICByZXR1cm4gISFtZXRhZGF0YVsnaXNvbGF0ZWQnXTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQW4gb3V0cHV0IGFyZWEgd2lkZ2V0IGNvbnRlbnQgZmFjdG9yeS5cbiAgICpcbiAgICogVGhlIGNvbnRlbnQgZmFjdG9yeSBpcyB1c2VkIHRvIGNyZWF0ZSBjaGlsZHJlbiBpbiBhIHdheVxuICAgKiB0aGF0IGNhbiBiZSBjdXN0b21pemVkLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhbiBvdXRwdXQgcHJvbXB0LlxuICAgICAqL1xuICAgIGNyZWF0ZU91dHB1dFByb21wdCgpOiBJT3V0cHV0UHJvbXB0O1xuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGFuIHN0ZGluIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVTdGRpbihvcHRpb25zOiBTdGRpbi5JT3B0aW9ucyk6IElTdGRpbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBpbXBsZW1lbnRhdGlvbiBvZiBgSUNvbnRlbnRGYWN0b3J5YC5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBDb250ZW50RmFjdG9yeSBpbXBsZW1lbnRzIElDb250ZW50RmFjdG9yeSB7XG4gICAgLyoqXG4gICAgICogQ3JlYXRlIHRoZSBvdXRwdXQgcHJvbXB0IGZvciB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIGNyZWF0ZU91dHB1dFByb21wdCgpOiBJT3V0cHV0UHJvbXB0IHtcbiAgICAgIHJldHVybiBuZXcgT3V0cHV0UHJvbXB0KCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQ3JlYXRlIGFuIHN0ZGluIHdpZGdldC5cbiAgICAgKi9cbiAgICBjcmVhdGVTdGRpbihvcHRpb25zOiBTdGRpbi5JT3B0aW9ucyk6IElTdGRpbiB7XG4gICAgICByZXR1cm4gbmV3IFN0ZGluKG9wdGlvbnMpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBgQ29udGVudEZhY3RvcnlgIGluc3RhbmNlLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRDb250ZW50RmFjdG9yeSA9IG5ldyBDb250ZW50RmFjdG9yeSgpO1xufVxuXG4vKiogKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKlxuICogT3V0cHV0UHJvbXB0XG4gKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuXG4vKipcbiAqIFRoZSBpbnRlcmZhY2UgZm9yIGFuIG91dHB1dCBwcm9tcHQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU91dHB1dFByb21wdCBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBUaGUgZXhlY3V0aW9uIGNvdW50IGZvciB0aGUgcHJvbXB0LlxuICAgKi9cbiAgZXhlY3V0aW9uQ291bnQ6IG5iZm9ybWF0LkV4ZWN1dGlvbkNvdW50O1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IG91dHB1dCBwcm9tcHQgaW1wbGVtZW50YXRpb25cbiAqL1xuZXhwb3J0IGNsYXNzIE91dHB1dFByb21wdCBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElPdXRwdXRQcm9tcHQge1xuICAvKlxuICAgKiBDcmVhdGUgYW4gb3V0cHV0IHByb21wdCB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuYWRkQ2xhc3MoT1VUUFVUX1BST01QVF9DTEFTUyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGV4ZWN1dGlvbiBjb3VudCBmb3IgdGhlIHByb21wdC5cbiAgICovXG4gIGdldCBleGVjdXRpb25Db3VudCgpOiBuYmZvcm1hdC5FeGVjdXRpb25Db3VudCB7XG4gICAgcmV0dXJuIHRoaXMuX2V4ZWN1dGlvbkNvdW50O1xuICB9XG4gIHNldCBleGVjdXRpb25Db3VudCh2YWx1ZTogbmJmb3JtYXQuRXhlY3V0aW9uQ291bnQpIHtcbiAgICB0aGlzLl9leGVjdXRpb25Db3VudCA9IHZhbHVlO1xuICAgIGlmICh2YWx1ZSA9PT0gbnVsbCkge1xuICAgICAgdGhpcy5ub2RlLnRleHRDb250ZW50ID0gJyc7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMubm9kZS50ZXh0Q29udGVudCA9IGBbJHt2YWx1ZX1dOmA7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfZXhlY3V0aW9uQ291bnQ6IG5iZm9ybWF0LkV4ZWN1dGlvbkNvdW50ID0gbnVsbDtcbn1cblxuLyoqICoqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKipcbiAqIFN0ZGluXG4gKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqL1xuXG4vKipcbiAqIFRoZSBzdGRpbiBpbnRlcmZhY2VcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJU3RkaW4gZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogVGhlIHN0ZGluIHZhbHVlLlxuICAgKi9cbiAgcmVhZG9ubHkgdmFsdWU6IFByb21pc2U8c3RyaW5nPjtcbn1cblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBzdGRpbiB3aWRnZXQuXG4gKi9cbmV4cG9ydCBjbGFzcyBTdGRpbiBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElTdGRpbiB7XG4gIHByaXZhdGUgc3RhdGljIF9oaXN0b3J5OiBNYXA8c3RyaW5nLCBzdHJpbmdbXT4gPSBuZXcgTWFwKCk7XG5cbiAgcHJpdmF0ZSBzdGF0aWMgX2hpc3RvcnlJeChrZXk6IHN0cmluZywgaXg6IG51bWJlcik6IG51bWJlciB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgaGlzdG9yeSA9IFN0ZGluLl9oaXN0b3J5LmdldChrZXkpO1xuICAgIGlmICghaGlzdG9yeSkge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG4gICAgY29uc3QgbGVuID0gaGlzdG9yeS5sZW5ndGg7XG4gICAgLy8gd3JhcCBub25wb3NpdGl2ZSBpeCB0byBub25uZWdhdGl2ZSBpeFxuICAgIGlmIChpeCA8PSAwKSB7XG4gICAgICByZXR1cm4gbGVuICsgaXg7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBzdGF0aWMgX2hpc3RvcnlBdChrZXk6IHN0cmluZywgaXg6IG51bWJlcik6IHN0cmluZyB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgaGlzdG9yeSA9IFN0ZGluLl9oaXN0b3J5LmdldChrZXkpO1xuICAgIGlmICghaGlzdG9yeSkge1xuICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG4gICAgY29uc3QgbGVuID0gaGlzdG9yeS5sZW5ndGg7XG4gICAgY29uc3QgaXhwb3MgPSBTdGRpbi5faGlzdG9yeUl4KGtleSwgaXgpO1xuXG4gICAgaWYgKGl4cG9zICE9PSB1bmRlZmluZWQgJiYgaXhwb3MgPCBsZW4pIHtcbiAgICAgIHJldHVybiBoaXN0b3J5W2l4cG9zXTtcbiAgICB9XG4gICAgLy8gcmV0dXJuIHVuZGVmaW5lZCBpZiBpeCBpcyBvdXQgb2YgYm91bmRzXG4gIH1cblxuICBwcml2YXRlIHN0YXRpYyBfaGlzdG9yeVB1c2goa2V5OiBzdHJpbmcsIGxpbmU6IHN0cmluZyk6IHZvaWQge1xuICAgIGNvbnN0IGhpc3RvcnkgPSBTdGRpbi5faGlzdG9yeS5nZXQoa2V5KSE7XG4gICAgaGlzdG9yeS5wdXNoKGxpbmUpO1xuICAgIGlmIChoaXN0b3J5Lmxlbmd0aCA+IDEwMDApIHtcbiAgICAgIC8vIHRydW5jYXRlIGxpbmUgaGlzdG9yeSBpZiBpdCdzIHRvbyBsb25nXG4gICAgICBoaXN0b3J5LnNoaWZ0KCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBzdGF0aWMgX2hpc3RvcnlTZWFyY2goXG4gICAga2V5OiBzdHJpbmcsXG4gICAgcGF0OiBzdHJpbmcsXG4gICAgaXg6IG51bWJlcixcbiAgICByZXZlcnNlID0gdHJ1ZVxuICApOiBudW1iZXIgfCB1bmRlZmluZWQge1xuICAgIGNvbnN0IGhpc3RvcnkgPSBTdGRpbi5faGlzdG9yeS5nZXQoa2V5KSE7XG4gICAgY29uc3QgbGVuID0gaGlzdG9yeS5sZW5ndGg7XG4gICAgY29uc3QgaXhwb3MgPSBTdGRpbi5faGlzdG9yeUl4KGtleSwgaXgpO1xuICAgIGNvbnN0IHN1YnN0ckZvdW5kID0gKHg6IHN0cmluZykgPT4geC5zZWFyY2gocGF0KSAhPT0gLTE7XG5cbiAgICBpZiAoaXhwb3MgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGlmIChyZXZlcnNlKSB7XG4gICAgICBpZiAoaXhwb3MgPT09IDApIHtcbiAgICAgICAgLy8gcmV2ZXJzZSBzZWFyY2ggZmFpbHMgaWYgYWxyZWFkeSBhdCBzdGFydCBvZiBoaXN0b3J5XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cblxuICAgICAgY29uc3QgaXhGb3VuZCA9IChoaXN0b3J5LnNsaWNlKDAsIGl4cG9zKSBhcyBhbnkpLmZpbmRMYXN0SW5kZXgoXG4gICAgICAgIHN1YnN0ckZvdW5kXG4gICAgICApO1xuICAgICAgaWYgKGl4Rm91bmQgIT09IC0xKSB7XG4gICAgICAgIC8vIHdyYXAgaXggdG8gbmVnYXRpdmVcbiAgICAgICAgcmV0dXJuIGl4Rm91bmQgLSBsZW47XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIGlmIChpeHBvcyA+PSBsZW4gLSAxKSB7XG4gICAgICAgIC8vIGZvcndhcmQgc2VhcmNoIGZhaWxzIGlmIGFscmVhZHkgYXQgZW5kIG9mIGhpc3RvcnlcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICBjb25zdCBpeEZvdW5kID0gaGlzdG9yeS5zbGljZShpeHBvcyArIDEpLmZpbmRJbmRleChzdWJzdHJGb3VuZCk7XG4gICAgICBpZiAoaXhGb3VuZCAhPT0gLTEpIHtcbiAgICAgICAgLy8gd3JhcCBpeCB0byBuZWdhdGl2ZSBhbmQgYWRqdXN0IGZvciBzbGljZVxuICAgICAgICByZXR1cm4gaXhGb3VuZCAtIGxlbiArIGl4cG9zICsgMTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IGlucHV0IHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IFN0ZGluLklPcHRpb25zKSB7XG4gICAgc3VwZXIoe1xuICAgICAgbm9kZTogUHJpdmF0ZS5jcmVhdGVJbnB1dFdpZGdldE5vZGUob3B0aW9ucy5wcm9tcHQsIG9wdGlvbnMucGFzc3dvcmQpXG4gICAgfSk7XG4gICAgdGhpcy5hZGRDbGFzcyhTVERJTl9DTEFTUyk7XG4gICAgdGhpcy5fZnV0dXJlID0gb3B0aW9ucy5mdXR1cmU7XG4gICAgdGhpcy5faGlzdG9yeUluZGV4ID0gMDtcbiAgICB0aGlzLl9oaXN0b3J5S2V5ID1cbiAgICAgIG9wdGlvbnMuaW5wdXRIaXN0b3J5U2NvcGUgPT09ICdzZXNzaW9uJ1xuICAgICAgICA/IG9wdGlvbnMucGFyZW50X2hlYWRlci5zZXNzaW9uXG4gICAgICAgIDogJyc7XG4gICAgdGhpcy5faGlzdG9yeVBhdCA9ICcnO1xuICAgIHRoaXMuX3BhcmVudEhlYWRlciA9IG9wdGlvbnMucGFyZW50X2hlYWRlcjtcbiAgICB0aGlzLl9wYXNzd29yZCA9IG9wdGlvbnMucGFzc3dvcmQ7XG4gICAgdGhpcy5fdHJhbnMgPSAob3B0aW9ucy50cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgdGhpcy5fdmFsdWUgPSBvcHRpb25zLnByb21wdCArICcgJztcblxuICAgIHRoaXMuX2lucHV0ID0gdGhpcy5ub2RlLmdldEVsZW1lbnRzQnlUYWdOYW1lKCdpbnB1dCcpWzBdO1xuICAgIC8vIG1ha2UgdXNlcnMgYXdhcmUgb2YgdGhlIGxpbmUgaGlzdG9yeSBmZWF0dXJlXG4gICAgdGhpcy5faW5wdXQucGxhY2Vob2xkZXIgPSB0aGlzLl90cmFucy5fXyhcbiAgICAgICfihpHihpMgZm9yIGhpc3RvcnkuIFNlYXJjaCBoaXN0b3J5IHdpdGggYy3ihpEvYy3ihpMnXG4gICAgKTtcblxuICAgIC8vIGluaXRpYWxpemUgbGluZSBoaXN0b3J5XG4gICAgaWYgKCFTdGRpbi5faGlzdG9yeS5oYXModGhpcy5faGlzdG9yeUtleSkpIHtcbiAgICAgIFN0ZGluLl9oaXN0b3J5LnNldCh0aGlzLl9oaXN0b3J5S2V5LCBbXSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRoZSB2YWx1ZSBvZiB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZ2V0IHZhbHVlKCk6IFByb21pc2U8c3RyaW5nPiB7XG4gICAgcmV0dXJuIHRoaXMuX3Byb21pc2UucHJvbWlzZS50aGVuKCgpID0+IHRoaXMuX3ZhbHVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIERPTSBldmVudHMgZm9yIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSBldmVudCAtIFRoZSBET00gZXZlbnQgc2VudCB0byB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgbWV0aG9kIGltcGxlbWVudHMgdGhlIERPTSBgRXZlbnRMaXN0ZW5lcmAgaW50ZXJmYWNlIGFuZCBpc1xuICAgKiBjYWxsZWQgaW4gcmVzcG9uc2UgdG8gZXZlbnRzIG9uIHRoZSBkb2NrIHBhbmVsJ3Mgbm9kZS4gSXQgc2hvdWxkXG4gICAqIG5vdCBiZSBjYWxsZWQgZGlyZWN0bHkgYnkgdXNlciBjb2RlLlxuICAgKi9cbiAgaGFuZGxlRXZlbnQoZXZlbnQ6IEtleWJvYXJkRXZlbnQpOiB2b2lkIHtcbiAgICBjb25zdCBpbnB1dCA9IHRoaXMuX2lucHV0O1xuXG4gICAgaWYgKGV2ZW50LnR5cGUgPT09ICdrZXlkb3duJykge1xuICAgICAgaWYgKGV2ZW50LmtleSA9PT0gJ0VudGVyJykge1xuICAgICAgICB0aGlzLnJlc2V0U2VhcmNoKCk7XG5cbiAgICAgICAgdGhpcy5fZnV0dXJlLnNlbmRJbnB1dFJlcGx5KFxuICAgICAgICAgIHtcbiAgICAgICAgICAgIHN0YXR1czogJ29rJyxcbiAgICAgICAgICAgIHZhbHVlOiBpbnB1dC52YWx1ZVxuICAgICAgICAgIH0sXG4gICAgICAgICAgdGhpcy5fcGFyZW50SGVhZGVyXG4gICAgICAgICk7XG4gICAgICAgIGlmICh0aGlzLl9wYXNzd29yZCkge1xuICAgICAgICAgIHRoaXMuX3ZhbHVlICs9ICfCt8K3wrfCt8K3wrfCt8K3JztcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICB0aGlzLl92YWx1ZSArPSBpbnB1dC52YWx1ZTtcbiAgICAgICAgICBTdGRpbi5faGlzdG9yeVB1c2godGhpcy5faGlzdG9yeUtleSwgaW5wdXQudmFsdWUpO1xuICAgICAgICB9XG4gICAgICAgIHRoaXMuX3Byb21pc2UucmVzb2x2ZSh2b2lkIDApO1xuICAgICAgfSBlbHNlIGlmIChldmVudC5rZXkgPT09ICdFc2NhcGUnKSB7XG4gICAgICAgIC8vIGN1cnJlbnRseSB0aGlzIGdldHMgY2xvYmJlcmVkIGJ5IHRoZSBkb2N1bWVudHNlYXJjaDplbmQgY29tbWFuZCBhdCB0aGUgbm90ZWJvb2sgbGV2ZWxcbiAgICAgICAgdGhpcy5yZXNldFNlYXJjaCgpO1xuICAgICAgICBpbnB1dC5ibHVyKCk7XG4gICAgICB9IGVsc2UgaWYgKFxuICAgICAgICBldmVudC5jdHJsS2V5ICYmXG4gICAgICAgIChldmVudC5rZXkgPT09ICdBcnJvd1VwJyB8fCBldmVudC5rZXkgPT09ICdBcnJvd0Rvd24nKVxuICAgICAgKSB7XG4gICAgICAgIC8vIGlmIF9oaXN0b3J5UGF0IGlzIGJsYW5rLCB1c2UgaW5wdXQgYXMgc2VhcmNoIHBhdHRlcm4uIE90aGVyd2lzZSwgcmV1c2UgdGhlIGN1cnJlbnQgc2VhcmNoIHBhdHRlcm5cbiAgICAgICAgaWYgKHRoaXMuX2hpc3RvcnlQYXQgPT09ICcnKSB7XG4gICAgICAgICAgdGhpcy5faGlzdG9yeVBhdCA9IGlucHV0LnZhbHVlO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgcmV2ZXJzZSA9IGV2ZW50LmtleSA9PT0gJ0Fycm93VXAnO1xuICAgICAgICBjb25zdCBzZWFyY2hIaXN0b3J5SXggPSBTdGRpbi5faGlzdG9yeVNlYXJjaChcbiAgICAgICAgICB0aGlzLl9oaXN0b3J5S2V5LFxuICAgICAgICAgIHRoaXMuX2hpc3RvcnlQYXQsXG4gICAgICAgICAgdGhpcy5faGlzdG9yeUluZGV4LFxuICAgICAgICAgIHJldmVyc2VcbiAgICAgICAgKTtcblxuICAgICAgICBpZiAoc2VhcmNoSGlzdG9yeUl4ICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICBjb25zdCBoaXN0b3J5TGluZSA9IFN0ZGluLl9oaXN0b3J5QXQoXG4gICAgICAgICAgICB0aGlzLl9oaXN0b3J5S2V5LFxuICAgICAgICAgICAgc2VhcmNoSGlzdG9yeUl4XG4gICAgICAgICAgKTtcbiAgICAgICAgICBpZiAoaGlzdG9yeUxpbmUgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgaWYgKHRoaXMuX2hpc3RvcnlJbmRleCA9PT0gMCkge1xuICAgICAgICAgICAgICB0aGlzLl92YWx1ZUNhY2hlID0gaW5wdXQudmFsdWU7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIHRoaXMuX3NldElucHV0VmFsdWUoaGlzdG9yeUxpbmUpO1xuICAgICAgICAgICAgdGhpcy5faGlzdG9yeUluZGV4ID0gc2VhcmNoSGlzdG9yeUl4O1xuICAgICAgICAgICAgLy8gVGhlIGRlZmF1bHQgYWN0aW9uIGZvciBBcnJvd1VwIGlzIG1vdmluZyB0byBmaXJzdCBjaGFyYWN0ZXJcbiAgICAgICAgICAgIC8vIGJ1dCB3ZSB3YW50IHRvIGtlZXAgdGhlIGN1cnNvciBhdCB0aGUgZW5kLlxuICAgICAgICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSBpZiAoZXZlbnQua2V5ID09PSAnQXJyb3dVcCcpIHtcbiAgICAgICAgdGhpcy5yZXNldFNlYXJjaCgpO1xuXG4gICAgICAgIGNvbnN0IGhpc3RvcnlMaW5lID0gU3RkaW4uX2hpc3RvcnlBdChcbiAgICAgICAgICB0aGlzLl9oaXN0b3J5S2V5LFxuICAgICAgICAgIHRoaXMuX2hpc3RvcnlJbmRleCAtIDFcbiAgICAgICAgKTtcbiAgICAgICAgaWYgKGhpc3RvcnlMaW5lKSB7XG4gICAgICAgICAgaWYgKHRoaXMuX2hpc3RvcnlJbmRleCA9PT0gMCkge1xuICAgICAgICAgICAgdGhpcy5fdmFsdWVDYWNoZSA9IGlucHV0LnZhbHVlO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aGlzLl9zZXRJbnB1dFZhbHVlKGhpc3RvcnlMaW5lKTtcbiAgICAgICAgICAtLXRoaXMuX2hpc3RvcnlJbmRleDtcbiAgICAgICAgICAvLyBUaGUgZGVmYXVsdCBhY3Rpb24gZm9yIEFycm93VXAgaXMgbW92aW5nIHRvIGZpcnN0IGNoYXJhY3RlclxuICAgICAgICAgIC8vIGJ1dCB3ZSB3YW50IHRvIGtlZXAgdGhlIGN1cnNvciBhdCB0aGUgZW5kLlxuICAgICAgICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSBpZiAoZXZlbnQua2V5ID09PSAnQXJyb3dEb3duJykge1xuICAgICAgICB0aGlzLnJlc2V0U2VhcmNoKCk7XG5cbiAgICAgICAgaWYgKHRoaXMuX2hpc3RvcnlJbmRleCA9PT0gMCkge1xuICAgICAgICAgIC8vIGRvIG5vdGhpbmdcbiAgICAgICAgfSBlbHNlIGlmICh0aGlzLl9oaXN0b3J5SW5kZXggPT09IC0xKSB7XG4gICAgICAgICAgdGhpcy5fc2V0SW5wdXRWYWx1ZSh0aGlzLl92YWx1ZUNhY2hlKTtcbiAgICAgICAgICArK3RoaXMuX2hpc3RvcnlJbmRleDtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBjb25zdCBoaXN0b3J5TGluZSA9IFN0ZGluLl9oaXN0b3J5QXQoXG4gICAgICAgICAgICB0aGlzLl9oaXN0b3J5S2V5LFxuICAgICAgICAgICAgdGhpcy5faGlzdG9yeUluZGV4ICsgMVxuICAgICAgICAgICk7XG4gICAgICAgICAgaWYgKGhpc3RvcnlMaW5lKSB7XG4gICAgICAgICAgICB0aGlzLl9zZXRJbnB1dFZhbHVlKGhpc3RvcnlMaW5lKTtcbiAgICAgICAgICAgICsrdGhpcy5faGlzdG9yeUluZGV4O1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfVxuXG4gIHByb3RlY3RlZCByZXNldFNlYXJjaCgpOiB2b2lkIHtcbiAgICB0aGlzLl9oaXN0b3J5UGF0ID0gJyc7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzIHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMuX2lucHV0LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCB0aGlzKTtcbiAgICB0aGlzLl9pbnB1dC5mb2N1cygpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgc2VudCB0byB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQmVmb3JlRGV0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMuX2lucHV0LnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCB0aGlzKTtcbiAgfVxuXG4gIHByaXZhdGUgX3NldElucHV0VmFsdWUodmFsdWU6IHN0cmluZykge1xuICAgIHRoaXMuX2lucHV0LnZhbHVlID0gdmFsdWU7XG4gICAgLy8gU2V0IGN1cnNvciBhdCB0aGUgZW5kOyB0aGlzIGlzIHVzdWFsbHkgbm90IG5lY2Vzc2FyeSB3aGVuIGlucHV0IGlzXG4gICAgLy8gZm9jdXNlZCBidXQgaGF2aW5nIHRoZSBleHBsaWNpdCBwbGFjZW1lbnQgZW5zdXJlcyBjb25zaXN0ZW5jeS5cbiAgICB0aGlzLl9pbnB1dC5zZXRTZWxlY3Rpb25SYW5nZSh2YWx1ZS5sZW5ndGgsIHZhbHVlLmxlbmd0aCk7XG4gIH1cblxuICBwcml2YXRlIF9mdXR1cmU6IEtlcm5lbC5JU2hlbGxGdXR1cmU7XG4gIHByaXZhdGUgX2hpc3RvcnlJbmRleDogbnVtYmVyO1xuICBwcml2YXRlIF9oaXN0b3J5S2V5OiBzdHJpbmc7XG4gIHByaXZhdGUgX2hpc3RvcnlQYXQ6IHN0cmluZztcbiAgcHJpdmF0ZSBfaW5wdXQ6IEhUTUxJbnB1dEVsZW1lbnQ7XG4gIHByaXZhdGUgX3BhcmVudEhlYWRlcjogS2VybmVsTWVzc2FnZS5JSW5wdXRSZXBseU1zZ1sncGFyZW50X2hlYWRlciddO1xuICBwcml2YXRlIF9wYXNzd29yZDogYm9vbGVhbjtcbiAgcHJpdmF0ZSBfcHJvbWlzZSA9IG5ldyBQcm9taXNlRGVsZWdhdGU8dm9pZD4oKTtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF92YWx1ZTogc3RyaW5nO1xuICBwcml2YXRlIF92YWx1ZUNhY2hlOiBzdHJpbmc7XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgU3RkaW4ge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdG8gY3JlYXRlIGEgc3RkaW4gd2lkZ2V0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIHByb21wdCB0ZXh0LlxuICAgICAqL1xuICAgIHByb21wdDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgaW5wdXQgaXMgYSBwYXNzd29yZC5cbiAgICAgKi9cbiAgICBwYXNzd29yZDogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBrZXJuZWwgZnV0dXJlIGFzc29jaWF0ZWQgd2l0aCB0aGUgcmVxdWVzdC5cbiAgICAgKi9cbiAgICBmdXR1cmU6IEtlcm5lbC5JU2hlbGxGdXR1cmU7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgaGVhZGVyIG9mIHRoZSBpbnB1dF9yZXF1ZXN0IG1lc3NhZ2UuXG4gICAgICovXG4gICAgcGFyZW50X2hlYWRlcjogS2VybmVsTWVzc2FnZS5JSW5wdXRSZXBseU1zZ1sncGFyZW50X2hlYWRlciddO1xuXG4gICAgLyoqXG4gICAgICogVHJhbnNsYXRvclxuICAgICAqL1xuICAgIHJlYWRvbmx5IHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gc3BsaXQgc3RkaW4gbGluZSBoaXN0b3J5IGJ5IGtlcm5lbCBzZXNzaW9uIG9yIGtlZXAgZ2xvYmFsbHkgYWNjZXNzaWJsZS5cbiAgICAgKi9cbiAgICBpbnB1dEhpc3RvcnlTY29wZT86ICdnbG9iYWwnIHwgJ3Nlc3Npb24nO1xuICB9XG59XG5cbi8qKiAqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqXG4gKiBQcml2YXRlIG5hbWVzcGFjZVxuICoqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKioqKi9cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgdGhlIG5vZGUgZm9yIGFuIElucHV0V2lkZ2V0LlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZUlucHV0V2lkZ2V0Tm9kZShcbiAgICBwcm9tcHQ6IHN0cmluZyxcbiAgICBwYXNzd29yZDogYm9vbGVhblxuICApOiBIVE1MRWxlbWVudCB7XG4gICAgY29uc3Qgbm9kZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIGNvbnN0IHByb21wdE5vZGUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdwcmUnKTtcbiAgICBwcm9tcHROb2RlLmNsYXNzTmFtZSA9IFNURElOX1BST01QVF9DTEFTUztcbiAgICBwcm9tcHROb2RlLnRleHRDb250ZW50ID0gcHJvbXB0O1xuICAgIGNvbnN0IGlucHV0ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaW5wdXQnKTtcbiAgICBpbnB1dC5jbGFzc05hbWUgPSBTVERJTl9JTlBVVF9DTEFTUztcbiAgICBpZiAocGFzc3dvcmQpIHtcbiAgICAgIGlucHV0LnR5cGUgPSAncGFzc3dvcmQnO1xuICAgIH1cbiAgICBub2RlLmFwcGVuZENoaWxkKHByb21wdE5vZGUpO1xuICAgIHByb21wdE5vZGUuYXBwZW5kQ2hpbGQoaW5wdXQpO1xuICAgIHJldHVybiBub2RlO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcmVuZGVyZXIgZm9yIElGcmFtZSBkYXRhLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIElzb2xhdGVkUmVuZGVyZXJcbiAgICBleHRlbmRzIFdpZGdldFxuICAgIGltcGxlbWVudHMgSVJlbmRlck1pbWUuSVJlbmRlcmVyXG4gIHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYW4gaXNvbGF0ZWQgcmVuZGVyZXIuXG4gICAgICovXG4gICAgY29uc3RydWN0b3Iod3JhcHBlZDogSVJlbmRlck1pbWUuSVJlbmRlcmVyKSB7XG4gICAgICBzdXBlcih7IG5vZGU6IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2lmcmFtZScpIH0pO1xuICAgICAgdGhpcy5hZGRDbGFzcygnanAtbW9kLWlzb2xhdGVkJyk7XG5cbiAgICAgIHRoaXMuX3dyYXBwZWQgPSB3cmFwcGVkO1xuXG4gICAgICAvLyBPbmNlIHRoZSBpZnJhbWUgaXMgbG9hZGVkLCB0aGUgc3ViYXJlYSBpcyBkeW5hbWljYWxseSBpbnNlcnRlZFxuICAgICAgY29uc3QgaWZyYW1lID0gdGhpcy5ub2RlIGFzIEhUTUxJRnJhbWVFbGVtZW50ICYge1xuICAgICAgICBoZWlnaHRDaGFuZ2VPYnNlcnZlcjogUmVzaXplT2JzZXJ2ZXI7XG4gICAgICB9O1xuXG4gICAgICBpZnJhbWUuZnJhbWVCb3JkZXIgPSAnMCc7XG4gICAgICBpZnJhbWUuc2Nyb2xsaW5nID0gJ2F1dG8nO1xuXG4gICAgICBpZnJhbWUuYWRkRXZlbnRMaXN0ZW5lcignbG9hZCcsICgpID0+IHtcbiAgICAgICAgLy8gV29ya2Fyb3VuZCBuZWVkZWQgYnkgRmlyZWZveCwgdG8gcHJvcGVybHkgcmVuZGVyIHN2ZyBpbnNpZGVcbiAgICAgICAgLy8gaWZyYW1lcywgc2VlIGh0dHBzOi8vc3RhY2tvdmVyZmxvdy5jb20vcXVlc3Rpb25zLzEwMTc3MTkwL1xuICAgICAgICAvLyBzdmctZHluYW1pY2FsbHktYWRkZWQtdG8taWZyYW1lLWRvZXMtbm90LXJlbmRlci1jb3JyZWN0bHlcbiAgICAgICAgaWZyYW1lLmNvbnRlbnREb2N1bWVudCEub3BlbigpO1xuXG4gICAgICAgIC8vIEluc2VydCB0aGUgc3ViYXJlYSBpbnRvIHRoZSBpZnJhbWVcbiAgICAgICAgLy8gV2UgbXVzdCBkaXJlY3RseSB3cml0ZSB0aGUgaHRtbC4gQXQgdGhpcyBwb2ludCwgc3ViYXJlYSBkb2Vzbid0XG4gICAgICAgIC8vIGNvbnRhaW4gYW55IHVzZXIgY29udGVudC5cbiAgICAgICAgaWZyYW1lLmNvbnRlbnREb2N1bWVudCEud3JpdGUodGhpcy5fd3JhcHBlZC5ub2RlLmlubmVySFRNTCk7XG5cbiAgICAgICAgaWZyYW1lLmNvbnRlbnREb2N1bWVudCEuY2xvc2UoKTtcblxuICAgICAgICBjb25zdCBib2R5ID0gaWZyYW1lLmNvbnRlbnREb2N1bWVudCEuYm9keTtcblxuICAgICAgICAvLyBBZGp1c3QgdGhlIGlmcmFtZSBoZWlnaHQgYXV0b21hdGljYWxseVxuICAgICAgICBpZnJhbWUuc3R5bGUuaGVpZ2h0ID0gYCR7Ym9keS5zY3JvbGxIZWlnaHR9cHhgO1xuICAgICAgICBpZnJhbWUuaGVpZ2h0Q2hhbmdlT2JzZXJ2ZXIgPSBuZXcgUmVzaXplT2JzZXJ2ZXIoKCkgPT4ge1xuICAgICAgICAgIGlmcmFtZS5zdHlsZS5oZWlnaHQgPSBgJHtib2R5LnNjcm9sbEhlaWdodH1weGA7XG4gICAgICAgIH0pO1xuICAgICAgICBpZnJhbWUuaGVpZ2h0Q2hhbmdlT2JzZXJ2ZXIub2JzZXJ2ZShib2R5KTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlbmRlciBhIG1pbWUgbW9kZWwuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gbW9kZWwgLSBUaGUgbWltZSBtb2RlbCB0byByZW5kZXIuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBBIHByb21pc2Ugd2hpY2ggcmVzb2x2ZXMgd2hlbiByZW5kZXJpbmcgaXMgY29tcGxldGUuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyBtZXRob2QgbWF5IGJlIGNhbGxlZCBtdWx0aXBsZSB0aW1lcyBkdXJpbmcgdGhlIGxpZmV0aW1lXG4gICAgICogb2YgdGhlIHdpZGdldCB0byB1cGRhdGUgaXQgaWYgYW5kIHdoZW4gbmV3IGRhdGEgaXMgYXZhaWxhYmxlLlxuICAgICAqL1xuICAgIHJlbmRlck1vZGVsKG1vZGVsOiBJUmVuZGVyTWltZS5JTWltZU1vZGVsKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICByZXR1cm4gdGhpcy5fd3JhcHBlZC5yZW5kZXJNb2RlbChtb2RlbCk7XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfd3JhcHBlZDogSVJlbmRlck1pbWUuSVJlbmRlcmVyO1xuICB9XG5cbiAgZXhwb3J0IGNvbnN0IGN1cnJlbnRQcmVmZXJyZWRNaW1ldHlwZSA9IG5ldyBBdHRhY2hlZFByb3BlcnR5PFxuICAgIElSZW5kZXJNaW1lLklSZW5kZXJlcixcbiAgICBzdHJpbmdcbiAgPih7XG4gICAgbmFtZTogJ3ByZWZlcnJlZE1pbWV0eXBlJyxcbiAgICBjcmVhdGU6IG93bmVyID0+ICcnXG4gIH0pO1xuXG4gIC8qKlxuICAgKiBBIGBQYW5lbGAgdGhhdCdzIGZvY3VzZWQgYnkgYSBgY29udGV4dG1lbnVgIGV2ZW50LlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE91dHB1dFBhbmVsIGV4dGVuZHMgUGFuZWwge1xuICAgIC8qKlxuICAgICAqIENvbnN0cnVjdCBhIG5ldyBgT3V0cHV0UGFuZWxgIHdpZGdldC5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3RvcihvcHRpb25zPzogUGFuZWwuSU9wdGlvbnMpIHtcbiAgICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgY2FsbGJhY2sgdGhhdCBmb2N1c2VzIG9uIHRoZSB3aWRnZXQuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfb25Db250ZXh0KF86IEV2ZW50KTogdm9pZCB7XG4gICAgICB0aGlzLm5vZGUuZm9jdXMoKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBIYW5kbGUgYGFmdGVyLWF0dGFjaGAgbWVzc2FnZXMgc2VudCB0byB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgICAgc3VwZXIub25BZnRlckF0dGFjaChtc2cpO1xuICAgICAgdGhpcy5ub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2NvbnRleHRtZW51JywgdGhpcy5fb25Db250ZXh0LmJpbmQodGhpcykpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgc2VudCB0byB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIHByb3RlY3RlZCBvbkJlZm9yZURldGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICAgIHN1cGVyLm9uQWZ0ZXJEZXRhY2gobXNnKTtcbiAgICAgIHRoaXMubm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdjb250ZXh0bWVudScsIHRoaXMuX29uQ29udGV4dC5iaW5kKHRoaXMpKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVHJpbW1lZCBvdXRwdXRzIGluZm9ybWF0aW9uIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBUcmltbWVkT3V0cHV0cyBleHRlbmRzIFdpZGdldCB7XG4gICAgLyoqXG4gICAgICogV2lkZ2V0IGNvbnN0cnVjdG9yXG4gICAgICpcbiAgICAgKiAjIyMgTm90ZXNcbiAgICAgKiBUaGUgd2lkZ2V0IHdpbGwgYmUgZGlzcG9zZWQgb24gY2xpY2sgYWZ0ZXIgY2FsbGluZyB0aGUgY2FsbGJhY2suXG4gICAgICpcbiAgICAgKiBAcGFyYW0gbWF4TnVtYmVyT3V0cHV0cyBNYXhpbWFsIG51bWJlciBvZiBvdXRwdXRzIHRvIGRpc3BsYXlcbiAgICAgKiBAcGFyYW0gX29uQ2xpY2sgQ2FsbGJhY2sgb24gY2xpY2sgZXZlbnQgb24gdGhlIHdpZGdldFxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKFxuICAgICAgbWF4TnVtYmVyT3V0cHV0czogbnVtYmVyLFxuICAgICAgb25DbGljazogKGV2ZW50OiBNb3VzZUV2ZW50KSA9PiB2b2lkXG4gICAgKSB7XG4gICAgICBjb25zdCBub2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgICBjb25zdCB0aXRsZSA9IGBUaGUgZmlyc3QgJHttYXhOdW1iZXJPdXRwdXRzfSBhcmUgZGlzcGxheWVkYDtcbiAgICAgIGNvbnN0IG1zZyA9ICdTaG93IG1vcmUgb3V0cHV0cyc7XG4gICAgICBub2RlLmluc2VydEFkamFjZW50SFRNTChcbiAgICAgICAgJ2FmdGVyYmVnaW4nLFxuICAgICAgICBgPGEgdGl0bGU9JHt0aXRsZX0+XG4gICAgICAgICAgPHByZT4ke21zZ308L3ByZT5cbiAgICAgICAgPC9hPmBcbiAgICAgICk7XG4gICAgICBzdXBlcih7XG4gICAgICAgIG5vZGVcbiAgICAgIH0pO1xuICAgICAgdGhpcy5fb25DbGljayA9IG9uQ2xpY2s7XG4gICAgICB0aGlzLmFkZENsYXNzKCdqcC1UcmltbWVkT3V0cHV0cycpO1xuICAgICAgdGhpcy5hZGRDbGFzcygnanAtUmVuZGVyZWRIVE1MQ29tbW9uJyk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB3aWRnZXQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICAgKiBjYWxsZWQgaW4gcmVzcG9uc2UgdG8gZXZlbnRzIG9uIHRoZSB3aWRnZXQncyBET00gbm9kZS4gSXQgc2hvdWxkXG4gICAgICogbm90IGJlIGNhbGxlZCBkaXJlY3RseSBieSB1c2VyIGNvZGUuXG4gICAgICovXG4gICAgaGFuZGxlRXZlbnQoZXZlbnQ6IEV2ZW50KTogdm9pZCB7XG4gICAgICBpZiAoZXZlbnQudHlwZSA9PT0gJ2NsaWNrJykge1xuICAgICAgICB0aGlzLl9vbkNsaWNrKGV2ZW50IGFzIE1vdXNlRXZlbnQpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEhhbmRsZSBgYWZ0ZXItYXR0YWNoYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICAgKi9cbiAgICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICAgIHN1cGVyLm9uQWZ0ZXJBdHRhY2gobXNnKTtcbiAgICAgIHRoaXMubm9kZS5hZGRFdmVudExpc3RlbmVyKCdjbGljaycsIHRoaXMpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgbWVzc2FnZSBoYW5kbGVyIGludm9rZWQgb24gYSBgJ2JlZm9yZS1kZXRhY2gnYFxuICAgICAqIG1lc3NhZ2VcbiAgICAgKi9cbiAgICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgICBzdXBlci5vbkJlZm9yZURldGFjaChtc2cpO1xuICAgICAgdGhpcy5ub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcyk7XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfb25DbGljazogKGV2ZW50OiBNb3VzZUV2ZW50KSA9PiB2b2lkO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=