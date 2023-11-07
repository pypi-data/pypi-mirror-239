"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_codeeditor_lib_index_js"],{

/***/ "../packages/codeeditor/lib/editor.js":
/*!********************************************!*\
  !*** ../packages/codeeditor/lib/editor.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeEditor": () => (/* binding */ CodeEditor)
/* harmony export */ });
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter/ydoc */ "webpack/sharing/consume/default/@jupyter/ydoc/@jupyter/ydoc");
/* harmony import */ var _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_ydoc__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _mimetype__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./mimetype */ "../packages/codeeditor/lib/mimetype.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A namespace for code editors.
 *
 * #### Notes
 * - A code editor is a set of common assumptions which hold for all concrete editors.
 * - Changes in implementations of the code editor should only be caused by changes in concrete editors.
 * - Common JLab services which are based on the code editor should belong to `IEditorServices`.
 */
var CodeEditor;
(function (CodeEditor) {
    /**
     * The default implementation of the editor model.
     */
    class Model {
        /**
         * Construct a new Model.
         */
        constructor(options = {}) {
            var _a, _b;
            /**
             * Whether the model should disposed the shared model on disposal or not.
             */
            this.standaloneModel = false;
            this._isDisposed = false;
            this._selections = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_1__.ObservableMap();
            this._mimeType = _mimetype__WEBPACK_IMPORTED_MODULE_3__.IEditorMimeTypeService.defaultMimeType;
            this._mimeTypeChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
            // Track if we need to dispose the model or not.
            this.standaloneModel = typeof options.sharedModel === 'undefined';
            this.sharedModel = (_a = options.sharedModel) !== null && _a !== void 0 ? _a : new _jupyter_ydoc__WEBPACK_IMPORTED_MODULE_0__.YFile();
            this._mimeType =
                (_b = options.mimeType) !== null && _b !== void 0 ? _b : _mimetype__WEBPACK_IMPORTED_MODULE_3__.IEditorMimeTypeService.defaultMimeType;
        }
        /**
         * A signal emitted when a mimetype changes.
         */
        get mimeTypeChanged() {
            return this._mimeTypeChanged;
        }
        /**
         * Get the selections for the model.
         */
        get selections() {
            return this._selections;
        }
        /**
         * A mime type of the model.
         */
        get mimeType() {
            return this._mimeType;
        }
        set mimeType(newValue) {
            const oldValue = this.mimeType;
            if (oldValue === newValue) {
                return;
            }
            this._mimeType = newValue;
            this._mimeTypeChanged.emit({
                name: 'mimeType',
                oldValue: oldValue,
                newValue: newValue
            });
        }
        /**
         * Whether the model is disposed.
         */
        get isDisposed() {
            return this._isDisposed;
        }
        /**
         * Dispose of the resources used by the model.
         */
        dispose() {
            if (this._isDisposed) {
                return;
            }
            this._isDisposed = true;
            this._selections.dispose();
            if (this.standaloneModel) {
                this.sharedModel.dispose();
            }
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
        }
    }
    CodeEditor.Model = Model;
})(CodeEditor || (CodeEditor = {}));


/***/ }),

/***/ "../packages/codeeditor/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/codeeditor/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeEditor": () => (/* reexport safe */ _editor__WEBPACK_IMPORTED_MODULE_0__.CodeEditor),
/* harmony export */   "CodeEditorWrapper": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_6__.CodeEditorWrapper),
/* harmony export */   "CodeViewerWidget": () => (/* reexport safe */ _viewer__WEBPACK_IMPORTED_MODULE_5__.CodeViewerWidget),
/* harmony export */   "IEditorMimeTypeService": () => (/* reexport safe */ _mimetype__WEBPACK_IMPORTED_MODULE_3__.IEditorMimeTypeService),
/* harmony export */   "IEditorServices": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.IEditorServices),
/* harmony export */   "IPositionModel": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.IPositionModel),
/* harmony export */   "JSONEditor": () => (/* reexport safe */ _jsoneditor__WEBPACK_IMPORTED_MODULE_1__.JSONEditor),
/* harmony export */   "LineCol": () => (/* reexport safe */ _lineCol__WEBPACK_IMPORTED_MODULE_2__.LineCol)
/* harmony export */ });
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./editor */ "../packages/codeeditor/lib/editor.js");
/* harmony import */ var _jsoneditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./jsoneditor */ "../packages/codeeditor/lib/jsoneditor.js");
/* harmony import */ var _lineCol__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./lineCol */ "../packages/codeeditor/lib/lineCol.js");
/* harmony import */ var _mimetype__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./mimetype */ "../packages/codeeditor/lib/mimetype.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokens */ "../packages/codeeditor/lib/tokens.js");
/* harmony import */ var _viewer__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./viewer */ "../packages/codeeditor/lib/viewer.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "../packages/codeeditor/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module codeeditor
 */










/***/ }),

/***/ "../packages/codeeditor/lib/jsoneditor.js":
/*!************************************************!*\
  !*** ../packages/codeeditor/lib/jsoneditor.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JSONEditor": () => (/* binding */ JSONEditor)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./editor */ "../packages/codeeditor/lib/editor.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The class name added to a JSONEditor instance.
 */
const JSONEDITOR_CLASS = 'jp-JSONEditor';
/**
 * The class name added when the Metadata editor contains invalid JSON.
 */
const ERROR_CLASS = 'jp-mod-error';
/**
 * The class name added to the editor host node.
 */
const HOST_CLASS = 'jp-JSONEditor-host';
/**
 * The class name added to the header area.
 */
const HEADER_CLASS = 'jp-JSONEditor-header';
/**
 * A widget for editing observable JSON.
 */
class JSONEditor extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Construct a new JSON editor.
     */
    constructor(options) {
        super();
        this._dataDirty = false;
        this._inputDirty = false;
        this._source = null;
        this._originalValue = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.emptyObject;
        this._changeGuard = false;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.addClass(JSONEDITOR_CLASS);
        this.headerNode = document.createElement('div');
        this.headerNode.className = HEADER_CLASS;
        this.revertButtonNode = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.undoIcon.element({
            tag: 'span',
            title: this._trans.__('Revert changes to data')
        });
        this.commitButtonNode = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.checkIcon.element({
            tag: 'span',
            title: this._trans.__('Commit changes to data'),
            marginLeft: '8px'
        });
        this.editorHostNode = document.createElement('div');
        this.editorHostNode.className = HOST_CLASS;
        this.headerNode.appendChild(this.revertButtonNode);
        this.headerNode.appendChild(this.commitButtonNode);
        this.node.appendChild(this.headerNode);
        this.node.appendChild(this.editorHostNode);
        const model = new _editor__WEBPACK_IMPORTED_MODULE_4__.CodeEditor.Model({ mimeType: 'application/json' });
        model.sharedModel.changed.connect(this._onModelChanged, this);
        this.model = model;
        this.editor = options.editorFactory({
            host: this.editorHostNode,
            model,
            config: {
                readOnly: true
            }
        });
    }
    /**
     * The observable source.
     */
    get source() {
        return this._source;
    }
    set source(value) {
        if (this._source === value) {
            return;
        }
        if (this._source) {
            this._source.changed.disconnect(this._onSourceChanged, this);
        }
        this._source = value;
        this.editor.setOption('readOnly', value === null);
        if (value) {
            value.changed.connect(this._onSourceChanged, this);
        }
        this._setValue();
    }
    /**
     * Get whether the editor is dirty.
     */
    get isDirty() {
        return this._dataDirty || this._inputDirty;
    }
    /**
     * Dispose of the editor.
     */
    dispose() {
        var _a;
        if (this.isDisposed) {
            return;
        }
        (_a = this.source) === null || _a === void 0 ? void 0 : _a.dispose();
        this.model.dispose();
        this.editor.dispose();
        super.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'blur':
                this._evtBlur(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        const node = this.editorHostNode;
        node.addEventListener('blur', this, true);
        node.addEventListener('click', this, true);
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.headerNode.addEventListener('click', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.editorHostNode;
        node.removeEventListener('blur', this, true);
        node.removeEventListener('click', this, true);
        this.headerNode.removeEventListener('click', this);
    }
    /**
     * Handle a change to the metadata of the source.
     */
    _onSourceChanged(sender, args) {
        if (this._changeGuard) {
            return;
        }
        if (this._inputDirty || this.editor.hasFocus()) {
            this._dataDirty = true;
            return;
        }
        this._setValue();
    }
    /**
     * Handle change events.
     */
    _onModelChanged(model, change) {
        if (change.sourceChange) {
            let valid = true;
            try {
                const value = JSON.parse(this.editor.model.sharedModel.getSource());
                this.removeClass(ERROR_CLASS);
                this._inputDirty =
                    !this._changeGuard && !_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(value, this._originalValue);
            }
            catch (err) {
                this.addClass(ERROR_CLASS);
                this._inputDirty = true;
                valid = false;
            }
            this.revertButtonNode.hidden = !this._inputDirty;
            this.commitButtonNode.hidden = !valid || !this._inputDirty;
        }
    }
    /**
     * Handle blur events for the text area.
     */
    _evtBlur(event) {
        // Update the metadata if necessary.
        if (!this._inputDirty && this._dataDirty) {
            this._setValue();
        }
    }
    /**
     * Handle click events for the buttons.
     */
    _evtClick(event) {
        const target = event.target;
        if (this.revertButtonNode.contains(target)) {
            this._setValue();
        }
        else if (this.commitButtonNode.contains(target)) {
            if (!this.commitButtonNode.hidden && !this.hasClass(ERROR_CLASS)) {
                this._changeGuard = true;
                this._mergeContent();
                this._changeGuard = false;
                this._setValue();
            }
        }
        else if (this.editorHostNode.contains(target)) {
            this.editor.focus();
        }
    }
    /**
     * Merge the user content.
     */
    _mergeContent() {
        const model = this.editor.model;
        const old = this._originalValue;
        const user = JSON.parse(model.sharedModel.getSource());
        const source = this.source;
        if (!source) {
            return;
        }
        // If it is in user and has changed from old, set in new.
        for (const key in user) {
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(user[key], old[key] || null)) {
                source.set(key, user[key]);
            }
        }
        // If it was in old and is not in user, remove from source.
        for (const key in old) {
            if (!(key in user)) {
                source.delete(key);
            }
        }
    }
    /**
     * Set the value given the owner contents.
     */
    _setValue() {
        this._dataDirty = false;
        this._inputDirty = false;
        this.revertButtonNode.hidden = true;
        this.commitButtonNode.hidden = true;
        this.removeClass(ERROR_CLASS);
        const model = this.editor.model;
        const content = this._source ? this._source.toJSON() : {};
        this._changeGuard = true;
        if (content === void 0) {
            model.sharedModel.setSource(this._trans.__('No data!'));
            this._originalValue = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.emptyObject;
        }
        else {
            const value = JSON.stringify(content, null, 4);
            model.sharedModel.setSource(value);
            this._originalValue = content;
            // Move the cursor to within the brace.
            if (value.length > 1 && value[0] === '{') {
                this.editor.setCursorPosition({ line: 0, column: 1 });
            }
        }
        this._changeGuard = false;
        this.commitButtonNode.hidden = true;
        this.revertButtonNode.hidden = true;
    }
}


/***/ }),

/***/ "../packages/codeeditor/lib/lineCol.js":
/*!*********************************************!*\
  !*** ../packages/codeeditor/lib/lineCol.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LineCol": () => (/* binding */ LineCol)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * A component for rendering a "go-to-line" form.
 */
class LineFormComponent extends (react__WEBPACK_IMPORTED_MODULE_3___default().Component) {
    /**
     * Construct a new LineFormComponent.
     */
    constructor(props) {
        super(props);
        /**
         * Handle a change to the value in the input field.
         */
        this._handleChange = (event) => {
            this.setState({ value: event.currentTarget.value });
        };
        /**
         * Handle submission of the input field.
         */
        this._handleSubmit = (event) => {
            event.preventDefault();
            const value = parseInt(this._textInput.value, 10);
            if (!isNaN(value) &&
                isFinite(value) &&
                1 <= value &&
                value <= this.props.maxLine) {
                this.props.handleSubmit(value);
            }
            return false;
        };
        /**
         * Handle focusing of the input field.
         */
        this._handleFocus = () => {
            this.setState({ hasFocus: true });
        };
        /**
         * Handle blurring of the input field.
         */
        this._handleBlur = () => {
            this.setState({ hasFocus: false });
        };
        this._textInput = null;
        this.translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.state = {
            value: '',
            hasFocus: false
        };
    }
    /**
     * Focus the element on mount.
     */
    componentDidMount() {
        this._textInput.focus();
    }
    /**
     * Render the LineFormComponent.
     */
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-lineFormSearch" },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("form", { name: "lineColumnForm", onSubmit: this._handleSubmit, noValidate: true },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.classes)('jp-lineFormWrapper', 'lm-lineForm-wrapper', this.state.hasFocus ? 'jp-lineFormWrapperFocusWithin' : undefined) },
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { type: "text", className: "jp-lineFormInput", onChange: this._handleChange, onFocus: this._handleFocus, onBlur: this._handleBlur, value: this.state.value, ref: input => {
                            this._textInput = input;
                        } }),
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-baseLineForm jp-lineFormButtonContainer" },
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.lineFormIcon.react, { className: "jp-baseLineForm jp-lineFormButtonIcon", elementPosition: "center" }),
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { type: "submit", className: "jp-baseLineForm jp-lineFormButton", value: "" }))),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("label", { className: "jp-lineFormCaption" }, this._trans.__('Go to line number between 1 and %1', this.props.maxLine)))));
    }
}
/**
 * A pure functional component for rendering a line/column
 * status item.
 */
function LineColComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__.TextItem, { onClick: props.handleClick, source: trans.__('Ln %1, Col %2', props.line, props.column), title: trans.__('Go to line number…') }));
}
/**
 * A widget implementing a line/column status item.
 */
class LineCol extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomRenderer {
    /**
     * Construct a new LineCol status item.
     */
    constructor(translator) {
        super(new LineCol.Model());
        this._popup = null;
        this.addClass('jp-mod-highlighted');
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    }
    /**
     * Render the status item.
     */
    render() {
        if (this.model === null) {
            return null;
        }
        else {
            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(LineColComponent, { line: this.model.line, column: this.model.column, translator: this.translator, handleClick: () => this._handleClick() }));
        }
    }
    /**
     * A click handler for the widget.
     */
    _handleClick() {
        if (this._popup) {
            this._popup.dispose();
        }
        const body = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_3___default().createElement(LineFormComponent, { handleSubmit: val => this._handleSubmit(val), currentLine: this.model.line, maxLine: this.model.editor.lineCount, translator: this.translator }));
        this._popup = (0,_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__.showPopup)({
            body: body,
            anchor: this,
            align: 'right'
        });
    }
    /**
     * Handle submission for the widget.
     */
    _handleSubmit(value) {
        this.model.editor.setCursorPosition({ line: value - 1, column: 0 });
        this._popup.dispose();
        this.model.editor.focus();
    }
}
/**
 * A namespace for LineCol statics.
 */
(function (LineCol) {
    /**
     * A VDom model for a status item tracking the line/column of an editor.
     */
    class Model extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomModel {
        constructor() {
            super(...arguments);
            /**
             * React to a change in the cursors of the current editor.
             */
            this._onSelectionChanged = () => {
                const oldState = this._getAllState();
                const pos = this.editor.getCursorPosition();
                this._line = pos.line + 1;
                this._column = pos.column + 1;
                this._triggerChange(oldState, this._getAllState());
            };
            this._line = 1;
            this._column = 1;
            this._editor = null;
        }
        /**
         * The current editor of the model.
         */
        get editor() {
            return this._editor;
        }
        set editor(editor) {
            var _a;
            const oldEditor = this._editor;
            if ((_a = oldEditor === null || oldEditor === void 0 ? void 0 : oldEditor.model) === null || _a === void 0 ? void 0 : _a.selections) {
                oldEditor.model.selections.changed.disconnect(this._onSelectionChanged);
            }
            const oldState = this._getAllState();
            this._editor = editor;
            if (!this._editor) {
                this._column = 1;
                this._line = 1;
            }
            else {
                this._editor.model.selections.changed.connect(this._onSelectionChanged);
                const pos = this._editor.getCursorPosition();
                this._column = pos.column + 1;
                this._line = pos.line + 1;
            }
            this._triggerChange(oldState, this._getAllState());
        }
        /**
         * The current line of the model.
         */
        get line() {
            return this._line;
        }
        /**
         * The current column of the model.
         */
        get column() {
            return this._column;
        }
        _getAllState() {
            return [this._line, this._column];
        }
        _triggerChange(oldState, newState) {
            if (oldState[0] !== newState[0] || oldState[1] !== newState[1]) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    LineCol.Model = Model;
})(LineCol || (LineCol = {}));


/***/ }),

/***/ "../packages/codeeditor/lib/mimetype.js":
/*!**********************************************!*\
  !*** ../packages/codeeditor/lib/mimetype.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IEditorMimeTypeService": () => (/* binding */ IEditorMimeTypeService)
/* harmony export */ });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * A namespace for `IEditorMimeTypeService`.
 */
var IEditorMimeTypeService;
(function (IEditorMimeTypeService) {
    /**
     * The default mime type.
     */
    IEditorMimeTypeService.defaultMimeType = 'text/plain';
})(IEditorMimeTypeService || (IEditorMimeTypeService = {}));


/***/ }),

/***/ "../packages/codeeditor/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/codeeditor/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IEditorServices": () => (/* binding */ IEditorServices),
/* harmony export */   "IPositionModel": () => (/* binding */ IPositionModel)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Code editor services token.
 */
const IEditorServices = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/codeeditor:IEditorServices', `A service for the text editor provider
  for the application. Use this to create new text editors and host them in your
  UI elements.`);
/**
 * Code editor cursor position token.
 */
const IPositionModel = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/codeeditor:IPositionModel', `A service to handle an code editor cursor position.`);


/***/ }),

/***/ "../packages/codeeditor/lib/viewer.js":
/*!********************************************!*\
  !*** ../packages/codeeditor/lib/viewer.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeViewerWidget": () => (/* binding */ CodeViewerWidget)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./editor */ "../packages/codeeditor/lib/editor.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/codeeditor/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



class CodeViewerWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Construct a new code viewer widget.
     */
    constructor(options) {
        var _a;
        super();
        this.model = options.model;
        const editorWidget = new _widget__WEBPACK_IMPORTED_MODULE_1__.CodeEditorWrapper({
            factory: options.factory,
            model: this.model,
            editorOptions: {
                ...options.editorOptions,
                config: { ...(_a = options.editorOptions) === null || _a === void 0 ? void 0 : _a.config, readOnly: true }
            }
        });
        this.editor = editorWidget.editor;
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.StackedLayout());
        layout.addWidget(editorWidget);
    }
    static createCodeViewer(options) {
        const { content, mimeType, ...others } = options;
        const model = new _editor__WEBPACK_IMPORTED_MODULE_2__.CodeEditor.Model({
            mimeType
        });
        model.sharedModel.setSource(content);
        const widget = new CodeViewerWidget({ ...others, model });
        widget.disposed.connect(() => {
            model.dispose();
        });
        return widget;
    }
    get content() {
        return this.model.sharedModel.getSource();
    }
    get mimeType() {
        return this.model.mimeType;
    }
}


/***/ }),

/***/ "../packages/codeeditor/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/codeeditor/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CodeEditorWrapper": () => (/* binding */ CodeEditorWrapper)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The class name added to an editor widget that has a primary selection.
 */
const HAS_SELECTION_CLASS = 'jp-mod-has-primary-selection';
/**
 * The class name added to an editor widget that has a cursor/selection
 * within the whitespace at the beginning of a line
 */
const HAS_IN_LEADING_WHITESPACE_CLASS = 'jp-mod-in-leading-whitespace';
/**
 * A class used to indicate a drop target.
 */
const DROP_TARGET_CLASS = 'jp-mod-dropTarget';
/**
 * RegExp to test for leading whitespace
 */
const leadingWhitespaceRe = /^\s+$/;
/**
 * A widget which hosts a code editor.
 */
class CodeEditorWrapper extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Construct a new code editor widget.
     */
    constructor(options) {
        super();
        const { factory, model, editorOptions } = options;
        const editor = (this.editor = factory({
            host: this.node,
            model,
            ...editorOptions
        }));
        editor.model.selections.changed.connect(this._onSelectionsChanged, this);
    }
    /**
     * Get the model used by the widget.
     */
    get model() {
        return this.editor.model;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.editor.dispose();
        super.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the notebook panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'lm-dragenter':
                this._evtDragEnter(event);
                break;
            case 'lm-dragleave':
                this._evtDragLeave(event);
                break;
            case 'lm-dragover':
                this._evtDragOver(event);
                break;
            case 'lm-drop':
                this._evtDrop(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.editor.focus();
    }
    /**
     * A message handler invoked on an `'after-attach'` message.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener('lm-dragenter', this);
        node.addEventListener('lm-dragleave', this);
        node.addEventListener('lm-dragover', this);
        node.addEventListener('lm-drop', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('lm-dragenter', this);
        node.removeEventListener('lm-dragleave', this);
        node.removeEventListener('lm-dragover', this);
        node.removeEventListener('lm-drop', this);
    }
    /**
     * Handle a change in model selections.
     */
    _onSelectionsChanged() {
        const { start, end } = this.editor.getSelection();
        if (start.column !== end.column || start.line !== end.line) {
            // a selection was made
            this.addClass(HAS_SELECTION_CLASS);
            this.removeClass(HAS_IN_LEADING_WHITESPACE_CLASS);
        }
        else {
            // the cursor was placed
            this.removeClass(HAS_SELECTION_CLASS);
            if (this.editor
                .getLine(end.line)
                .slice(0, end.column)
                .match(leadingWhitespaceRe)) {
                this.addClass(HAS_IN_LEADING_WHITESPACE_CLASS);
            }
            else {
                this.removeClass(HAS_IN_LEADING_WHITESPACE_CLASS);
            }
        }
    }
    /**
     * Handle the `'lm-dragenter'` event for the widget.
     */
    _evtDragEnter(event) {
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        this.addClass('jp-mod-dropTarget');
    }
    /**
     * Handle the `'lm-dragleave'` event for the widget.
     */
    _evtDragLeave(event) {
        this.removeClass(DROP_TARGET_CLASS);
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
    }
    /**
     * Handle the `'lm-dragover'` event for the widget.
     */
    _evtDragOver(event) {
        this.removeClass(DROP_TARGET_CLASS);
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        event.preventDefault();
        event.stopPropagation();
        event.dropAction = 'copy';
        this.addClass(DROP_TARGET_CLASS);
    }
    /**
     * Handle the `'lm-drop'` event for the widget.
     */
    _evtDrop(event) {
        if (this.editor.getOption('readOnly') === true) {
            return;
        }
        const data = Private.findTextData(event.mimeData);
        if (data === undefined) {
            return;
        }
        const coordinate = {
            top: event.y,
            bottom: event.y,
            left: event.x,
            right: event.x,
            x: event.x,
            y: event.y,
            width: 0,
            height: 0
        };
        const position = this.editor.getPositionForCoordinate(coordinate);
        if (position === null) {
            return;
        }
        this.removeClass(DROP_TARGET_CLASS);
        event.preventDefault();
        event.stopPropagation();
        if (event.proposedAction === 'none') {
            event.dropAction = 'none';
            return;
        }
        const offset = this.editor.getOffsetAt(position);
        this.model.sharedModel.updateSource(offset, offset, data);
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Given a MimeData instance, extract the first text data, if any.
     */
    function findTextData(mime) {
        const types = mime.types();
        const textType = types.find(t => t.indexOf('text') === 0);
        if (textType === undefined) {
            return undefined;
        }
        return mime.getData(textType);
    }
    Private.findTextData = findTextData;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY29kZWVkaXRvcl9saWJfaW5kZXhfanMuM2U0MDQ1Y2U5YWE4MTVmMGQzYzYuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBR1I7QUFFcUI7QUFJcEI7QUFDQTtBQUVwRDs7Ozs7OztHQU9HO0FBQ0ksSUFBVSxVQUFVLENBNGhCMUI7QUE1aEJELFdBQWlCLFVBQVU7SUFzSXpCOztPQUVHO0lBQ0gsTUFBYSxLQUFLO1FBQ2hCOztXQUVHO1FBQ0gsWUFBWSxVQUEwQixFQUFFOztZQW9FeEM7O2VBRUc7WUFDTyxvQkFBZSxHQUFHLEtBQUssQ0FBQztZQUUxQixnQkFBVyxHQUFHLEtBQUssQ0FBQztZQUNwQixnQkFBVyxHQUFHLElBQUksa0VBQWEsRUFBb0IsQ0FBQztZQUNwRCxjQUFTLEdBQUcsNkVBQXNDLENBQUM7WUFDbkQscUJBQWdCLEdBQUcsSUFBSSxxREFBTSxDQUE2QixJQUFJLENBQUMsQ0FBQztZQTNFdEUsZ0RBQWdEO1lBQ2hELElBQUksQ0FBQyxlQUFlLEdBQUcsT0FBTyxPQUFPLENBQUMsV0FBVyxLQUFLLFdBQVcsQ0FBQztZQUNsRSxJQUFJLENBQUMsV0FBVyxHQUFHLGFBQU8sQ0FBQyxXQUFXLG1DQUFJLElBQUksZ0RBQUssRUFBRSxDQUFDO1lBQ3RELElBQUksQ0FBQyxTQUFTO2dCQUNaLGFBQU8sQ0FBQyxRQUFRLG1DQUFJLDZFQUFzQyxDQUFDO1FBQy9ELENBQUM7UUFPRDs7V0FFRztRQUNILElBQUksZUFBZTtZQUNqQixPQUFPLElBQUksQ0FBQyxnQkFBZ0IsQ0FBQztRQUMvQixDQUFDO1FBRUQ7O1dBRUc7UUFDSCxJQUFJLFVBQVU7WUFDWixPQUFPLElBQUksQ0FBQyxXQUFXLENBQUM7UUFDMUIsQ0FBQztRQUVEOztXQUVHO1FBQ0gsSUFBSSxRQUFRO1lBQ1YsT0FBTyxJQUFJLENBQUMsU0FBUyxDQUFDO1FBQ3hCLENBQUM7UUFDRCxJQUFJLFFBQVEsQ0FBQyxR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aWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvZWRpdG9yLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb2RlZWRpdG9yL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvanNvbmVkaXRvci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvbGluZUNvbC50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvZGVlZGl0b3Ivc3JjL21pbWV0eXBlLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb2RlZWRpdG9yL3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvZGVlZGl0b3Ivc3JjL3ZpZXdlci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29kZWVkaXRvci9zcmMvd2lkZ2V0LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHR5cGUgeyBFeHRlbnNpb24gfSBmcm9tICdAY29kZW1pcnJvci9zdGF0ZSc7XG5pbXBvcnQgeyBJU2hhcmVkVGV4dCwgWUZpbGUgfSBmcm9tICdAanVweXRlci95ZG9jJztcbmltcG9ydCB7IElDaGFuZ2VkQXJncyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJT2JzZXJ2YWJsZU1hcCwgT2JzZXJ2YWJsZU1hcCB9IGZyb20gJ0BqdXB5dGVybGFiL29ic2VydmFibGVzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgSlNPTk9iamVjdCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IElFZGl0b3JNaW1lVHlwZVNlcnZpY2UgfSBmcm9tICcuL21pbWV0eXBlJztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgY29kZSBlZGl0b3JzLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIC0gQSBjb2RlIGVkaXRvciBpcyBhIHNldCBvZiBjb21tb24gYXNzdW1wdGlvbnMgd2hpY2ggaG9sZCBmb3IgYWxsIGNvbmNyZXRlIGVkaXRvcnMuXG4gKiAtIENoYW5nZXMgaW4gaW1wbGVtZW50YXRpb25zIG9mIHRoZSBjb2RlIGVkaXRvciBzaG91bGQgb25seSBiZSBjYXVzZWQgYnkgY2hhbmdlcyBpbiBjb25jcmV0ZSBlZGl0b3JzLlxuICogLSBDb21tb24gSkxhYiBzZXJ2aWNlcyB3aGljaCBhcmUgYmFzZWQgb24gdGhlIGNvZGUgZWRpdG9yIHNob3VsZCBiZWxvbmcgdG8gYElFZGl0b3JTZXJ2aWNlc2AuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQ29kZUVkaXRvciB7XG4gIC8qKlxuICAgKiBBIHplcm8tYmFzZWQgcG9zaXRpb24gaW4gdGhlIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVBvc2l0aW9uIGV4dGVuZHMgSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogVGhlIGN1cnNvciBsaW5lIG51bWJlci5cbiAgICAgKi9cbiAgICByZWFkb25seSBsaW5lOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3Vyc29yIGNvbHVtbiBudW1iZXIuXG4gICAgICovXG4gICAgcmVhZG9ubHkgY29sdW1uOiBudW1iZXI7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRpbWVuc2lvbiBvZiBhbiBlbGVtZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJRGltZW5zaW9uIHtcbiAgICAvKipcbiAgICAgKiBUaGUgd2lkdGggb2YgYW4gZWxlbWVudCBpbiBwaXhlbHMuXG4gICAgICovXG4gICAgcmVhZG9ubHkgd2lkdGg6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBoZWlnaHQgb2YgYW4gZWxlbWVudCBpbiBwaXhlbHMuXG4gICAgICovXG4gICAgcmVhZG9ubHkgaGVpZ2h0OiBudW1iZXI7XG4gIH1cblxuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGRlc2NyaWJpbmcgZWRpdG9yIHN0YXRlIGNvb3JkaW5hdGVzLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29vcmRpbmF0ZSBleHRlbmRzIERPTVJlY3RSZWFkT25seSB7fVxuXG4gIC8qKlxuICAgKiBBIHJhbmdlLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUmFuZ2UgZXh0ZW5kcyBKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBUaGUgcG9zaXRpb24gb2YgdGhlIGZpcnN0IGNoYXJhY3RlciBpbiB0aGUgY3VycmVudCByYW5nZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBJZiB0aGlzIHBvc2l0aW9uIGlzIGdyZWF0ZXIgdGhhbiBbZW5kXSB0aGVuIHRoZSByYW5nZSBpcyBjb25zaWRlcmVkXG4gICAgICogdG8gYmUgYmFja3dhcmQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgc3RhcnQ6IElQb3NpdGlvbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBwb3NpdGlvbiBvZiB0aGUgbGFzdCBjaGFyYWN0ZXIgaW4gdGhlIGN1cnJlbnQgcmFuZ2UuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgdGhpcyBwb3NpdGlvbiBpcyBsZXNzIHRoYW4gW3N0YXJ0XSB0aGVuIHRoZSByYW5nZSBpcyBjb25zaWRlcmVkXG4gICAgICogdG8gYmUgYmFja3dhcmQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgZW5kOiBJUG9zaXRpb247XG4gIH1cblxuICAvKipcbiAgICogQSB0ZXh0IHNlbGVjdGlvbi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVRleHRTZWxlY3Rpb24gZXh0ZW5kcyBJUmFuZ2Uge1xuICAgIC8qKlxuICAgICAqIFRoZSB1dWlkIG9mIHRoZSB0ZXh0IHNlbGVjdGlvbiBvd25lci5cbiAgICAgKi9cbiAgICByZWFkb25seSB1dWlkOiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGZvciBhIHRleHQgdG9rZW4sIHN1Y2ggYXMgYSB3b3JkLCBrZXl3b3JkLCBvciB2YXJpYWJsZS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVRva2VuIHtcbiAgICAvKipcbiAgICAgKiBUaGUgdmFsdWUgb2YgdGhlIHRva2VuLlxuICAgICAqL1xuICAgIHZhbHVlOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgb2Zmc2V0IG9mIHRoZSB0b2tlbiBpbiB0aGUgY29kZSBlZGl0b3IuXG4gICAgICovXG4gICAgb2Zmc2V0OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBBbiBvcHRpb25hbCB0eXBlIGZvciB0aGUgdG9rZW4uXG4gICAgICovXG4gICAgdHlwZT86IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiBpbnRlcmZhY2UgdG8gbWFuYWdlIHNlbGVjdGlvbnMgYnkgc2VsZWN0aW9uIG93bmVycy5cbiAgICpcbiAgICogIyMjIyBEZWZpbml0aW9uc1xuICAgKiAtIGEgdXNlciBjb2RlIHRoYXQgaGFzIGFuIGFzc29jaWF0ZWQgdXVpZCBpcyBjYWxsZWQgYSBzZWxlY3Rpb24gb3duZXIsIHNlZSBgQ29kZUVkaXRvci5JU2VsZWN0aW9uT3duZXJgXG4gICAqIC0gYSBzZWxlY3Rpb24gYmVsb25ncyB0byBhIHNlbGVjdGlvbiBvd25lciBvbmx5IGlmIGl0IGlzIGFzc29jaWF0ZWQgd2l0aCB0aGUgb3duZXIgYnkgYW4gdXVpZCwgc2VlIGBDb2RlRWRpdG9yLklUZXh0U2VsZWN0aW9uYFxuICAgKlxuICAgKiAjIyMjIFJlYWQgYWNjZXNzXG4gICAqIC0gYW55IHVzZXIgY29kZSBjYW4gb2JzZXJ2ZSBhbnkgc2VsZWN0aW9uXG4gICAqXG4gICAqICMjIyMgV3JpdGUgYWNjZXNzXG4gICAqIC0gaWYgYSB1c2VyIGNvZGUgaXMgYSBzZWxlY3Rpb24gb3duZXIgdGhlbjpcbiAgICogICAtIGl0IGNhbiBjaGFuZ2Ugc2VsZWN0aW9ucyBiZWxvbmdpbmcgdG8gaXRcbiAgICogICAtIGJ1dCBpdCBtdXN0IG5vdCBjaGFuZ2Ugc2VsZWN0aW9ucyBiZWxvbmdpbmcgdG8gb3RoZXIgc2VsZWN0aW9uIG93bmVyc1xuICAgKiAtIG90aGVyd2lzZSBpdCBtdXN0IG5vdCBjaGFuZ2UgYW55IHNlbGVjdGlvblxuICAgKi9cblxuICAvKipcbiAgICogQW4gZWRpdG9yIG1vZGVsLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTW9kZWwgZXh0ZW5kcyBJRGlzcG9zYWJsZSB7XG4gICAgLyoqXG4gICAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGEgcHJvcGVydHkgY2hhbmdlcy5cbiAgICAgKi9cbiAgICBtaW1lVHlwZUNoYW5nZWQ6IElTaWduYWw8SU1vZGVsLCBJQ2hhbmdlZEFyZ3M8c3RyaW5nPj47XG5cbiAgICAvKipcbiAgICAgKiBBIG1pbWUgdHlwZSBvZiB0aGUgbW9kZWwuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSXQgaXMgbmV2ZXIgYG51bGxgLCB0aGUgZGVmYXVsdCBtaW1lIHR5cGUgaXMgYHRleHQvcGxhaW5gLlxuICAgICAqL1xuICAgIG1pbWVUeXBlOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudGx5IHNlbGVjdGVkIGNvZGUuXG4gICAgICovXG4gICAgcmVhZG9ubHkgc2VsZWN0aW9uczogSU9ic2VydmFibGVNYXA8SVRleHRTZWxlY3Rpb25bXT47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2hhcmVkIG1vZGVsIGZvciB0aGUgY2VsbCBlZGl0b3IuXG4gICAgICovXG4gICAgcmVhZG9ubHkgc2hhcmVkTW9kZWw6IElTaGFyZWRUZXh0O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIHRoZSBlZGl0b3IgbW9kZWwuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgTW9kZWwgaW1wbGVtZW50cyBJTW9kZWwge1xuICAgIC8qKlxuICAgICAqIENvbnN0cnVjdCBhIG5ldyBNb2RlbC5cbiAgICAgKi9cbiAgICBjb25zdHJ1Y3RvcihvcHRpb25zOiBNb2RlbC5JT3B0aW9ucyA9IHt9KSB7XG4gICAgICAvLyBUcmFjayBpZiB3ZSBuZWVkIHRvIGRpc3Bvc2UgdGhlIG1vZGVsIG9yIG5vdC5cbiAgICAgIHRoaXMuc3RhbmRhbG9uZU1vZGVsID0gdHlwZW9mIG9wdGlvbnMuc2hhcmVkTW9kZWwgPT09ICd1bmRlZmluZWQnO1xuICAgICAgdGhpcy5zaGFyZWRNb2RlbCA9IG9wdGlvbnMuc2hhcmVkTW9kZWwgPz8gbmV3IFlGaWxlKCk7XG4gICAgICB0aGlzLl9taW1lVHlwZSA9XG4gICAgICAgIG9wdGlvbnMubWltZVR5cGUgPz8gSUVkaXRvck1pbWVUeXBlU2VydmljZS5kZWZhdWx0TWltZVR5cGU7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIHNoYXJlZCBtb2RlbCBmb3IgdGhlIGNlbGwgZWRpdG9yLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHNoYXJlZE1vZGVsOiBJU2hhcmVkVGV4dDtcblxuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhIG1pbWV0eXBlIGNoYW5nZXMuXG4gICAgICovXG4gICAgZ2V0IG1pbWVUeXBlQ2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElDaGFuZ2VkQXJnczxzdHJpbmc+PiB7XG4gICAgICByZXR1cm4gdGhpcy5fbWltZVR5cGVDaGFuZ2VkO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgc2VsZWN0aW9ucyBmb3IgdGhlIG1vZGVsLlxuICAgICAqL1xuICAgIGdldCBzZWxlY3Rpb25zKCk6IElPYnNlcnZhYmxlTWFwPElUZXh0U2VsZWN0aW9uW10+IHtcbiAgICAgIHJldHVybiB0aGlzLl9zZWxlY3Rpb25zO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgbWltZSB0eXBlIG9mIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICBnZXQgbWltZVR5cGUoKTogc3RyaW5nIHtcbiAgICAgIHJldHVybiB0aGlzLl9taW1lVHlwZTtcbiAgICB9XG4gICAgc2V0IG1pbWVUeXBlKG5ld1ZhbHVlOiBzdHJpbmcpIHtcbiAgICAgIGNvbnN0IG9sZFZhbHVlID0gdGhpcy5taW1lVHlwZTtcbiAgICAgIGlmIChvbGRWYWx1ZSA9PT0gbmV3VmFsdWUpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgdGhpcy5fbWltZVR5cGUgPSBuZXdWYWx1ZTtcbiAgICAgIHRoaXMuX21pbWVUeXBlQ2hhbmdlZC5lbWl0KHtcbiAgICAgICAgbmFtZTogJ21pbWVUeXBlJyxcbiAgICAgICAgb2xkVmFsdWU6IG9sZFZhbHVlLFxuICAgICAgICBuZXdWYWx1ZTogbmV3VmFsdWVcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIG1vZGVsIGlzIGRpc3Bvc2VkLlxuICAgICAqL1xuICAgIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIHVzZWQgYnkgdGhlIG1vZGVsLlxuICAgICAqL1xuICAgIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgICBpZiAodGhpcy5faXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICAgIHRoaXMuX3NlbGVjdGlvbnMuZGlzcG9zZSgpO1xuICAgICAgaWYgKHRoaXMuc3RhbmRhbG9uZU1vZGVsKSB7XG4gICAgICAgIHRoaXMuc2hhcmVkTW9kZWwuZGlzcG9zZSgpO1xuICAgICAgfVxuICAgICAgU2lnbmFsLmNsZWFyRGF0YSh0aGlzKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBtb2RlbCBzaG91bGQgZGlzcG9zZWQgdGhlIHNoYXJlZCBtb2RlbCBvbiBkaXNwb3NhbCBvciBub3QuXG4gICAgICovXG4gICAgcHJvdGVjdGVkIHN0YW5kYWxvbmVNb2RlbCA9IGZhbHNlO1xuXG4gICAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xuICAgIHByaXZhdGUgX3NlbGVjdGlvbnMgPSBuZXcgT2JzZXJ2YWJsZU1hcDxJVGV4dFNlbGVjdGlvbltdPigpO1xuICAgIHByaXZhdGUgX21pbWVUeXBlID0gSUVkaXRvck1pbWVUeXBlU2VydmljZS5kZWZhdWx0TWltZVR5cGU7XG4gICAgcHJpdmF0ZSBfbWltZVR5cGVDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBJQ2hhbmdlZEFyZ3M8c3RyaW5nPj4odGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogQSBzZWxlY3Rpb24gb3duZXIuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElTZWxlY3Rpb25Pd25lciB7XG4gICAgLyoqXG4gICAgICogVGhlIHV1aWQgb2YgdGhpcyBzZWxlY3Rpb24gb3duZXIuXG4gICAgICovXG4gICAgdXVpZDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogUmV0dXJucyB0aGUgcHJpbWFyeSBwb3NpdGlvbiBvZiB0aGUgY3Vyc29yLCBuZXZlciBgbnVsbGAuXG4gICAgICovXG4gICAgZ2V0Q3Vyc29yUG9zaXRpb24oKTogSVBvc2l0aW9uO1xuXG4gICAgLyoqXG4gICAgICogU2V0IHRoZSBwcmltYXJ5IHBvc2l0aW9uIG9mIHRoZSBjdXJzb3IuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gcG9zaXRpb24gLSBUaGUgbmV3IHByaW1hcnkgcG9zaXRpb24uXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyB3aWxsIHJlbW92ZSBhbnkgc2Vjb25kYXJ5IGN1cnNvcnMuXG4gICAgICovXG4gICAgc2V0Q3Vyc29yUG9zaXRpb24ocG9zaXRpb246IElQb3NpdGlvbik6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBSZXR1cm5zIHRoZSBwcmltYXJ5IHNlbGVjdGlvbiwgbmV2ZXIgYG51bGxgLlxuICAgICAqL1xuICAgIGdldFNlbGVjdGlvbigpOiBJUmFuZ2U7XG5cbiAgICAvKipcbiAgICAgKiBTZXQgdGhlIHByaW1hcnkgc2VsZWN0aW9uLlxuICAgICAqXG4gICAgICogQHBhcmFtIHNlbGVjdGlvbiAtIFRoZSBkZXNpcmVkIHNlbGVjdGlvbiByYW5nZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIHdpbGwgcmVtb3ZlIGFueSBzZWNvbmRhcnkgY3Vyc29ycy5cbiAgICAgKi9cbiAgICBzZXRTZWxlY3Rpb24oc2VsZWN0aW9uOiBJUmFuZ2UpOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogR2V0cyB0aGUgc2VsZWN0aW9ucyBmb3IgYWxsIHRoZSBjdXJzb3JzLCBuZXZlciBgbnVsbGAgb3IgZW1wdHkuXG4gICAgICovXG4gICAgZ2V0U2VsZWN0aW9ucygpOiBJUmFuZ2VbXTtcblxuICAgIC8qKlxuICAgICAqIFNldHMgdGhlIHNlbGVjdGlvbnMgZm9yIGFsbCB0aGUgY3Vyc29ycy5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBzZWxlY3Rpb25zIC0gVGhlIG5ldyBzZWxlY3Rpb25zLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIEN1cnNvcnMgd2lsbCBiZSByZW1vdmVkIG9yIGFkZGVkLCBhcyBuZWNlc3NhcnkuXG4gICAgICogUGFzc2luZyBhbiBlbXB0eSBhcnJheSByZXNldHMgYSBjdXJzb3IgcG9zaXRpb24gdG8gdGhlIHN0YXJ0IG9mIGFcbiAgICAgKiBkb2N1bWVudC5cbiAgICAgKi9cbiAgICBzZXRTZWxlY3Rpb25zKHNlbGVjdGlvbnM6IElSYW5nZVtdKTogdm9pZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIGtleWRvd24gaGFuZGxlciB0eXBlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFJldHVybiBgdHJ1ZWAgdG8gcHJldmVudCB0aGUgZGVmYXVsdCBoYW5kbGluZyBvZiB0aGUgZXZlbnQgYnkgdGhlXG4gICAqIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCB0eXBlIEtleWRvd25IYW5kbGVyID0gKFxuICAgIGluc3RhbmNlOiBJRWRpdG9yLFxuICAgIGV2ZW50OiBLZXlib2FyZEV2ZW50XG4gICkgPT4gYm9vbGVhbjtcblxuICAvKipcbiAgICogVGhlIGxvY2F0aW9uIG9mIHJlcXVlc3RlZCBlZGdlcy5cbiAgICovXG4gIGV4cG9ydCB0eXBlIEVkZ2VMb2NhdGlvbiA9ICd0b3AnIHwgJ3RvcExpbmUnIHwgJ2JvdHRvbSc7XG5cbiAgLyoqXG4gICAqIEEgd2lkZ2V0IHRoYXQgcHJvdmlkZXMgYSBjb2RlIGVkaXRvci5cbiAgICpcbiAgICogQXMgb2YgSnVweXRlckxhYiA0LjAuMCwgaXQgaXMgbm90IHBvc3NpYmxlIHRvIHByb3ZpZGUgYW4gZWRpdG9yXG4gICAqIHRoYXQgaXMgZGlmZmVyZW50IG9mIENvZGVNaXJyb3IgNi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUVkaXRvciBleHRlbmRzIElTZWxlY3Rpb25Pd25lciwgSURpc3Bvc2FibGUge1xuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBlaXRoZXIgdGhlIHRvcCBvciBib3R0b20gZWRnZSBpcyByZXF1ZXN0ZWQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgZWRnZVJlcXVlc3RlZDogSVNpZ25hbDxJRWRpdG9yLCBFZGdlTG9jYXRpb24+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIERPTSBub2RlIHRoYXQgaG9zdHMgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICByZWFkb25seSBob3N0OiBIVE1MRWxlbWVudDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBtb2RlbCB1c2VkIGJ5IHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgcmVhZG9ubHkgbW9kZWw6IElNb2RlbDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBoZWlnaHQgb2YgYSBsaW5lIGluIHRoZSBlZGl0b3IgaW4gcGl4ZWxzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGxpbmVIZWlnaHQ6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSB3aWRnZXQgb2YgYSBjaGFyYWN0ZXIgaW4gdGhlIGVkaXRvciBpbiBwaXhlbHMuXG4gICAgICovXG4gICAgcmVhZG9ubHkgY2hhcldpZHRoOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIG51bWJlciBvZiBsaW5lcyBpbiB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGxpbmVDb3VudDogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogR2V0IGEgY29uZmlnIG9wdGlvbiBmb3IgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICBnZXRPcHRpb24ob3B0aW9uOiBzdHJpbmcpOiB1bmtub3duO1xuXG4gICAgLyoqXG4gICAgICogU2V0IGEgY29uZmlnIG9wdGlvbiBmb3IgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICBzZXRPcHRpb24ob3B0aW9uOiBzdHJpbmcsIHZhbHVlOiB1bmtub3duKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFNldCBjb25maWcgb3B0aW9ucyBmb3IgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICBzZXRPcHRpb25zKG9wdGlvbnM6IFJlY29yZDxzdHJpbmcsIGFueT4pOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogSW5qZWN0IGFuIGV4dGVuc2lvbiBpbnRvIHRoZSBlZGl0b3JcbiAgICAgKlxuICAgICAqIEBhbHBoYVxuICAgICAqIEBleHBlcmltZW50YWxcbiAgICAgKiBAcGFyYW0gZXh0IEVkaXRvciBleHRlbnNpb25cbiAgICAgKi9cbiAgICBpbmplY3RFeHRlbnNpb24oZXh0OiBFeHRlbnNpb24pOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogUmV0dXJucyB0aGUgY29udGVudCBmb3IgdGhlIGdpdmVuIGxpbmUgbnVtYmVyLlxuICAgICAqXG4gICAgICogQHBhcmFtIGxpbmUgLSBUaGUgbGluZSBvZiBpbnRlcmVzdC5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIFRoZSB2YWx1ZSBvZiB0aGUgbGluZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBMaW5lcyBhcmUgMC1iYXNlZCwgYW5kIGFjY2Vzc2luZyBhIGxpbmUgb3V0IG9mIHJhbmdlIHJldHVybnNcbiAgICAgKiBgdW5kZWZpbmVkYC5cbiAgICAgKi9cbiAgICBnZXRMaW5lKGxpbmU6IG51bWJlcik6IHN0cmluZyB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIEZpbmQgYW4gb2Zmc2V0IGZvciB0aGUgZ2l2ZW4gcG9zaXRpb24uXG4gICAgICpcbiAgICAgKiBAcGFyYW0gcG9zaXRpb24gLSBUaGUgcG9zaXRpb24gb2YgaW50ZXJlc3QuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBUaGUgb2Zmc2V0IGF0IHRoZSBwb3NpdGlvbiwgY2xhbXBlZCB0byB0aGUgZXh0ZW50IG9mIHRoZVxuICAgICAqIGVkaXRvciBjb250ZW50cy5cbiAgICAgKi9cbiAgICBnZXRPZmZzZXRBdChwb3NpdGlvbjogSVBvc2l0aW9uKTogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogRmluZCBhIHBvc2l0aW9uIGZvciB0aGUgZ2l2ZW4gb2Zmc2V0LlxuICAgICAqXG4gICAgICogQHBhcmFtIG9mZnNldCAtIFRoZSBvZmZzZXQgb2YgaW50ZXJlc3QuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBUaGUgcG9zaXRpb24gYXQgdGhlIG9mZnNldCwgY2xhbXBlZCB0byB0aGUgZXh0ZW50IG9mIHRoZVxuICAgICAqIGVkaXRvciBjb250ZW50cy5cbiAgICAgKi9cbiAgICBnZXRQb3NpdGlvbkF0KG9mZnNldDogbnVtYmVyKTogSVBvc2l0aW9uIHwgdW5kZWZpbmVkO1xuXG4gICAgLyoqXG4gICAgICogVW5kbyBvbmUgZWRpdCAoaWYgYW55IHVuZG8gZXZlbnRzIGFyZSBzdG9yZWQpLlxuICAgICAqL1xuICAgIHVuZG8oKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFJlZG8gb25lIHVuZG9uZSBlZGl0LlxuICAgICAqL1xuICAgIHJlZG8oKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIENsZWFyIHRoZSB1bmRvIGhpc3RvcnkuXG4gICAgICovXG4gICAgY2xlYXJIaXN0b3J5KCk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBCcmluZ3MgYnJvd3NlciBmb2N1cyB0byB0aGlzIGVkaXRvciB0ZXh0LlxuICAgICAqL1xuICAgIGZvY3VzKCk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBUZXN0IHdoZXRoZXIgdGhlIGVkaXRvciBoYXMga2V5Ym9hcmQgZm9jdXMuXG4gICAgICovXG4gICAgaGFzRm9jdXMoKTogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIEV4cGxpY2l0bHkgYmx1ciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGJsdXIoKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIFJldmVhbHMgdGhlIGdpdmVuIHBvc2l0aW9uIGluIHRoZSBlZGl0b3IuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gcG9zaXRpb24gLSBUaGUgZGVzaXJlZCBwb3NpdGlvbiB0byByZXZlYWwuXG4gICAgICovXG4gICAgcmV2ZWFsUG9zaXRpb24ocG9zaXRpb246IElQb3NpdGlvbik6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBSZXZlYWxzIHRoZSBnaXZlbiBzZWxlY3Rpb24gaW4gdGhlIGVkaXRvci5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBzZWxlY3Rpb24gLSBUaGUgZGVzaXJlZCBzZWxlY3Rpb24gdG8gcmV2ZWFsLlxuICAgICAqL1xuICAgIHJldmVhbFNlbGVjdGlvbihzZWxlY3Rpb246IElSYW5nZSk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIHdpbmRvdyBjb29yZGluYXRlcyBnaXZlbiBhIGN1cnNvciBwb3NpdGlvbi5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBwb3NpdGlvbiAtIFRoZSBkZXNpcmVkIHBvc2l0aW9uLlxuICAgICAqXG4gICAgICogQHJldHVybnMgVGhlIGNvb3JkaW5hdGVzIG9mIHRoZSBwb3NpdGlvbi5cbiAgICAgKi9cbiAgICBnZXRDb29yZGluYXRlRm9yUG9zaXRpb24ocG9zaXRpb246IElQb3NpdGlvbik6IElDb29yZGluYXRlO1xuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBjdXJzb3IgcG9zaXRpb24gZ2l2ZW4gd2luZG93IGNvb3JkaW5hdGVzLlxuICAgICAqXG4gICAgICogQHBhcmFtIGNvb3JkaW5hdGUgLSBUaGUgZGVzaXJlZCBjb29yZGluYXRlLlxuICAgICAqXG4gICAgICogQHJldHVybnMgVGhlIHBvc2l0aW9uIG9mIHRoZSBjb29yZGluYXRlcywgb3IgbnVsbCBpZiBub3RcbiAgICAgKiAgIGNvbnRhaW5lZCBpbiB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGdldFBvc2l0aW9uRm9yQ29vcmRpbmF0ZShjb29yZGluYXRlOiBJQ29vcmRpbmF0ZSk6IElQb3NpdGlvbiB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBHZXQgYSBsaXN0IG9mIHRva2VucyBmb3IgdGhlIGN1cnJlbnQgZWRpdG9yIHRleHQgY29udGVudC5cbiAgICAgKi9cbiAgICBnZXRUb2tlbnMoKTogQ29kZUVkaXRvci5JVG9rZW5bXTtcblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgdG9rZW4gYXQgYSBnaXZlbiBlZGl0b3IgcG9zaXRpb24uXG4gICAgICovXG4gICAgZ2V0VG9rZW5BdChvZmZzZXQ6IG51bWJlcik6IENvZGVFZGl0b3IuSVRva2VuO1xuXG4gICAgLyoqXG4gICAgICogR2V0IHRoZSB0b2tlbiBhIHRoZSBjdXJzb3IgcG9zaXRpb24uXG4gICAgICovXG4gICAgZ2V0VG9rZW5BdEN1cnNvcigpOiBDb2RlRWRpdG9yLklUb2tlbjtcblxuICAgIC8qKlxuICAgICAqIEluc2VydHMgYSBuZXcgbGluZSBhdCB0aGUgY3Vyc29yIHBvc2l0aW9uIGFuZCBpbmRlbnRzIGl0LlxuICAgICAqL1xuICAgIG5ld0luZGVudGVkTGluZSgpOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogUmVwbGFjZXMgc2VsZWN0aW9uIHdpdGggdGhlIGdpdmVuIHRleHQuXG4gICAgICovXG4gICAgcmVwbGFjZVNlbGVjdGlvbj8odGV4dDogc3RyaW5nKTogdm9pZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIGZhY3RvcnkgdXNlZCB0byBjcmVhdGUgYSBjb2RlIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCB0eXBlIEZhY3RvcnkgPSAob3B0aW9uczogSU9wdGlvbnMpID0+IENvZGVFZGl0b3IuSUVkaXRvcjtcblxuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGFuIGVkaXRvci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBob3N0IHdpZGdldCB1c2VkIGJ5IHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgaG9zdDogSFRNTEVsZW1lbnQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbW9kZWwgdXNlZCBieSB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIG1vZGVsOiBJTW9kZWw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29uZmlndXJhdGlvbiBvcHRpb25zIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGNvbmZpZz86IFJlY29yZDxzdHJpbmcsIGFueT47XG5cbiAgICAvKipcbiAgICAgKiBMaXN0IG9mIGVkaXRvciBleHRlbnNpb25zIHRvIGJlIGFkZGVkLlxuICAgICAqL1xuICAgIGV4dGVuc2lvbnM/OiBFeHRlbnNpb25bXTtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIGVkaXRvciB3aWxsIGJlIGlubGluZSBvciBub3QuXG4gICAgICovXG4gICAgaW5saW5lPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjb25maWd1cmF0aW9uIG9wdGlvbnMgZm9yIHRoZSBlZGl0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGRlc2lyZWQgdXVpZCBmb3IgdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICB1dWlkPzogc3RyaW5nO1xuICB9XG5cbiAgZXhwb3J0IG5hbWVzcGFjZSBNb2RlbCB7XG4gICAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgICAvKipcbiAgICAgICAqIEEgdW5pcXVlIGlkZW50aWZpZXIgZm9yIHRoZSBtb2RlbC5cbiAgICAgICAqL1xuICAgICAgaWQ/OiBzdHJpbmc7XG5cbiAgICAgIC8qKlxuICAgICAgICogVGhlIG1pbWV0eXBlIG9mIHRoZSBtb2RlbC5cbiAgICAgICAqL1xuICAgICAgbWltZVR5cGU/OiBzdHJpbmc7XG5cbiAgICAgIC8qKlxuICAgICAgICogU2hhcmVkIGVkaXRvciB0ZXh0LlxuICAgICAgICovXG4gICAgICBzaGFyZWRNb2RlbD86IElTaGFyZWRUZXh0O1xuICAgIH1cbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY29kZWVkaXRvclxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vZWRpdG9yJztcbmV4cG9ydCAqIGZyb20gJy4vZmFjdG9yeSc7XG5leHBvcnQgKiBmcm9tICcuL2pzb25lZGl0b3InO1xuZXhwb3J0ICogZnJvbSAnLi9saW5lQ29sJztcbmV4cG9ydCAqIGZyb20gJy4vbWltZXR5cGUnO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuZXhwb3J0ICogZnJvbSAnLi92aWV3ZXInO1xuZXhwb3J0ICogZnJvbSAnLi93aWRnZXQnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJT2JzZXJ2YWJsZUpTT04gfSBmcm9tICdAanVweXRlcmxhYi9vYnNlcnZhYmxlcyc7XG5pbXBvcnQgeyBJU2hhcmVkVGV4dCwgU291cmNlQ2hhbmdlIH0gZnJvbSAnQGp1cHl0ZXIveWRvYyc7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGNoZWNrSWNvbiwgdW5kb0ljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7XG4gIEpTT05FeHQsXG4gIEpTT05PYmplY3QsXG4gIFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3Rcbn0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnLi9lZGl0b3InO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgSlNPTkVkaXRvciBpbnN0YW5jZS5cbiAqL1xuY29uc3QgSlNPTkVESVRPUl9DTEFTUyA9ICdqcC1KU09ORWRpdG9yJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB3aGVuIHRoZSBNZXRhZGF0YSBlZGl0b3IgY29udGFpbnMgaW52YWxpZCBKU09OLlxuICovXG5jb25zdCBFUlJPUl9DTEFTUyA9ICdqcC1tb2QtZXJyb3InO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSBlZGl0b3IgaG9zdCBub2RlLlxuICovXG5jb25zdCBIT1NUX0NMQVNTID0gJ2pwLUpTT05FZGl0b3ItaG9zdCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gdGhlIGhlYWRlciBhcmVhLlxuICovXG5jb25zdCBIRUFERVJfQ0xBU1MgPSAnanAtSlNPTkVkaXRvci1oZWFkZXInO1xuXG4vKipcbiAqIEEgd2lkZ2V0IGZvciBlZGl0aW5nIG9ic2VydmFibGUgSlNPTi5cbiAqL1xuZXhwb3J0IGNsYXNzIEpTT05FZGl0b3IgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IEpTT04gZWRpdG9yLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogSlNPTkVkaXRvci5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gb3B0aW9ucy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLmFkZENsYXNzKEpTT05FRElUT1JfQ0xBU1MpO1xuXG4gICAgdGhpcy5oZWFkZXJOb2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgdGhpcy5oZWFkZXJOb2RlLmNsYXNzTmFtZSA9IEhFQURFUl9DTEFTUztcblxuICAgIHRoaXMucmV2ZXJ0QnV0dG9uTm9kZSA9IHVuZG9JY29uLmVsZW1lbnQoe1xuICAgICAgdGFnOiAnc3BhbicsXG4gICAgICB0aXRsZTogdGhpcy5fdHJhbnMuX18oJ1JldmVydCBjaGFuZ2VzIHRvIGRhdGEnKVxuICAgIH0pO1xuXG4gICAgdGhpcy5jb21taXRCdXR0b25Ob2RlID0gY2hlY2tJY29uLmVsZW1lbnQoe1xuICAgICAgdGFnOiAnc3BhbicsXG4gICAgICB0aXRsZTogdGhpcy5fdHJhbnMuX18oJ0NvbW1pdCBjaGFuZ2VzIHRvIGRhdGEnKSxcbiAgICAgIG1hcmdpbkxlZnQ6ICc4cHgnXG4gICAgfSk7XG5cbiAgICB0aGlzLmVkaXRvckhvc3ROb2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgdGhpcy5lZGl0b3JIb3N0Tm9kZS5jbGFzc05hbWUgPSBIT1NUX0NMQVNTO1xuXG4gICAgdGhpcy5oZWFkZXJOb2RlLmFwcGVuZENoaWxkKHRoaXMucmV2ZXJ0QnV0dG9uTm9kZSk7XG4gICAgdGhpcy5oZWFkZXJOb2RlLmFwcGVuZENoaWxkKHRoaXMuY29tbWl0QnV0dG9uTm9kZSk7XG5cbiAgICB0aGlzLm5vZGUuYXBwZW5kQ2hpbGQodGhpcy5oZWFkZXJOb2RlKTtcbiAgICB0aGlzLm5vZGUuYXBwZW5kQ2hpbGQodGhpcy5lZGl0b3JIb3N0Tm9kZSk7XG5cbiAgICBjb25zdCBtb2RlbCA9IG5ldyBDb2RlRWRpdG9yLk1vZGVsKHsgbWltZVR5cGU6ICdhcHBsaWNhdGlvbi9qc29uJyB9KTtcbiAgICBtb2RlbC5zaGFyZWRNb2RlbC5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25Nb2RlbENoYW5nZWQsIHRoaXMpO1xuXG4gICAgdGhpcy5tb2RlbCA9IG1vZGVsO1xuICAgIHRoaXMuZWRpdG9yID0gb3B0aW9ucy5lZGl0b3JGYWN0b3J5KHtcbiAgICAgIGhvc3Q6IHRoaXMuZWRpdG9ySG9zdE5vZGUsXG4gICAgICBtb2RlbCxcbiAgICAgIGNvbmZpZzoge1xuICAgICAgICByZWFkT25seTogdHJ1ZVxuICAgICAgfVxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb2RlIGVkaXRvciB1c2VkIGJ5IHRoZSBlZGl0b3IuXG4gICAqL1xuICByZWFkb25seSBlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvcjtcblxuICAvKipcbiAgICogVGhlIGNvZGUgZWRpdG9yIG1vZGVsIHVzZWQgYnkgdGhlIGVkaXRvci5cbiAgICovXG4gIHJlYWRvbmx5IG1vZGVsOiBDb2RlRWRpdG9yLklNb2RlbDtcblxuICAvKipcbiAgICogVGhlIGVkaXRvciBob3N0IG5vZGUgdXNlZCBieSB0aGUgSlNPTiBlZGl0b3IuXG4gICAqL1xuICByZWFkb25seSBoZWFkZXJOb2RlOiBIVE1MRGl2RWxlbWVudDtcblxuICAvKipcbiAgICogVGhlIGVkaXRvciBob3N0IG5vZGUgdXNlZCBieSB0aGUgSlNPTiBlZGl0b3IuXG4gICAqL1xuICByZWFkb25seSBlZGl0b3JIb3N0Tm9kZTogSFRNTERpdkVsZW1lbnQ7XG5cbiAgLyoqXG4gICAqIFRoZSByZXZlcnQgYnV0dG9uIHVzZWQgYnkgdGhlIEpTT04gZWRpdG9yLlxuICAgKi9cbiAgcmVhZG9ubHkgcmV2ZXJ0QnV0dG9uTm9kZTogSFRNTFNwYW5FbGVtZW50O1xuXG4gIC8qKlxuICAgKiBUaGUgY29tbWl0IGJ1dHRvbiB1c2VkIGJ5IHRoZSBKU09OIGVkaXRvci5cbiAgICovXG4gIHJlYWRvbmx5IGNvbW1pdEJ1dHRvbk5vZGU6IEhUTUxTcGFuRWxlbWVudDtcblxuICAvKipcbiAgICogVGhlIG9ic2VydmFibGUgc291cmNlLlxuICAgKi9cbiAgZ2V0IHNvdXJjZSgpOiBJT2JzZXJ2YWJsZUpTT04gfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fc291cmNlO1xuICB9XG4gIHNldCBzb3VyY2UodmFsdWU6IElPYnNlcnZhYmxlSlNPTiB8IG51bGwpIHtcbiAgICBpZiAodGhpcy5fc291cmNlID09PSB2YWx1ZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBpZiAodGhpcy5fc291cmNlKSB7XG4gICAgICB0aGlzLl9zb3VyY2UuY2hhbmdlZC5kaXNjb25uZWN0KHRoaXMuX29uU291cmNlQ2hhbmdlZCwgdGhpcyk7XG4gICAgfVxuICAgIHRoaXMuX3NvdXJjZSA9IHZhbHVlO1xuICAgIHRoaXMuZWRpdG9yLnNldE9wdGlvbigncmVhZE9ubHknLCB2YWx1ZSA9PT0gbnVsbCk7XG4gICAgaWYgKHZhbHVlKSB7XG4gICAgICB2YWx1ZS5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25Tb3VyY2VDaGFuZ2VkLCB0aGlzKTtcbiAgICB9XG4gICAgdGhpcy5fc2V0VmFsdWUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgd2hldGhlciB0aGUgZWRpdG9yIGlzIGRpcnR5LlxuICAgKi9cbiAgZ2V0IGlzRGlydHkoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2RhdGFEaXJ0eSB8fCB0aGlzLl9pbnB1dERpcnR5O1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIGVkaXRvci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMuc291cmNlPy5kaXNwb3NlKCk7XG4gICAgdGhpcy5tb2RlbC5kaXNwb3NlKCk7XG4gICAgdGhpcy5lZGl0b3IuZGlzcG9zZSgpO1xuXG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgRE9NIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC0gVGhlIERPTSBldmVudCBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaW1wbGVtZW50cyB0aGUgRE9NIGBFdmVudExpc3RlbmVyYCBpbnRlcmZhY2UgYW5kIGlzXG4gICAqIGNhbGxlZCBpbiByZXNwb25zZSB0byBldmVudHMgb24gdGhlIG5vdGVib29rIHBhbmVsJ3Mgbm9kZS4gSXQgc2hvdWxkXG4gICAqIG5vdCBiZSBjYWxsZWQgZGlyZWN0bHkgYnkgdXNlciBjb2RlLlxuICAgKi9cbiAgaGFuZGxlRXZlbnQoZXZlbnQ6IEV2ZW50KTogdm9pZCB7XG4gICAgc3dpdGNoIChldmVudC50eXBlKSB7XG4gICAgICBjYXNlICdibHVyJzpcbiAgICAgICAgdGhpcy5fZXZ0Qmx1cihldmVudCBhcyBGb2N1c0V2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdjbGljayc6XG4gICAgICAgIHRoaXMuX2V2dENsaWNrKGV2ZW50IGFzIE1vdXNlRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGFmdGVyLWF0dGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBjb25zdCBub2RlID0gdGhpcy5lZGl0b3JIb3N0Tm9kZTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2JsdXInLCB0aGlzLCB0cnVlKTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcywgdHJ1ZSk7XG4gICAgdGhpcy5yZXZlcnRCdXR0b25Ob2RlLmhpZGRlbiA9IHRydWU7XG4gICAgdGhpcy5jb21taXRCdXR0b25Ob2RlLmhpZGRlbiA9IHRydWU7XG4gICAgdGhpcy5oZWFkZXJOb2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBiZWZvcmUtZGV0YWNoYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkJlZm9yZURldGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBjb25zdCBub2RlID0gdGhpcy5lZGl0b3JIb3N0Tm9kZTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2JsdXInLCB0aGlzLCB0cnVlKTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcywgdHJ1ZSk7XG4gICAgdGhpcy5oZWFkZXJOb2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIHRoZSBtZXRhZGF0YSBvZiB0aGUgc291cmNlLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25Tb3VyY2VDaGFuZ2VkKFxuICAgIHNlbmRlcjogSU9ic2VydmFibGVKU09OLFxuICAgIGFyZ3M6IElPYnNlcnZhYmxlSlNPTi5JQ2hhbmdlZEFyZ3NcbiAgKSB7XG4gICAgaWYgKHRoaXMuX2NoYW5nZUd1YXJkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGlmICh0aGlzLl9pbnB1dERpcnR5IHx8IHRoaXMuZWRpdG9yLmhhc0ZvY3VzKCkpIHtcbiAgICAgIHRoaXMuX2RhdGFEaXJ0eSA9IHRydWU7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX3NldFZhbHVlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGNoYW5nZSBldmVudHMuXG4gICAqL1xuICBwcml2YXRlIF9vbk1vZGVsQ2hhbmdlZChtb2RlbDogSVNoYXJlZFRleHQsIGNoYW5nZTogU291cmNlQ2hhbmdlKTogdm9pZCB7XG4gICAgaWYgKGNoYW5nZS5zb3VyY2VDaGFuZ2UpIHtcbiAgICAgIGxldCB2YWxpZCA9IHRydWU7XG4gICAgICB0cnkge1xuICAgICAgICBjb25zdCB2YWx1ZSA9IEpTT04ucGFyc2UodGhpcy5lZGl0b3IubW9kZWwuc2hhcmVkTW9kZWwuZ2V0U291cmNlKCkpO1xuICAgICAgICB0aGlzLnJlbW92ZUNsYXNzKEVSUk9SX0NMQVNTKTtcbiAgICAgICAgdGhpcy5faW5wdXREaXJ0eSA9XG4gICAgICAgICAgIXRoaXMuX2NoYW5nZUd1YXJkICYmICFKU09ORXh0LmRlZXBFcXVhbCh2YWx1ZSwgdGhpcy5fb3JpZ2luYWxWYWx1ZSk7XG4gICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgdGhpcy5hZGRDbGFzcyhFUlJPUl9DTEFTUyk7XG4gICAgICAgIHRoaXMuX2lucHV0RGlydHkgPSB0cnVlO1xuICAgICAgICB2YWxpZCA9IGZhbHNlO1xuICAgICAgfVxuICAgICAgdGhpcy5yZXZlcnRCdXR0b25Ob2RlLmhpZGRlbiA9ICF0aGlzLl9pbnB1dERpcnR5O1xuICAgICAgdGhpcy5jb21taXRCdXR0b25Ob2RlLmhpZGRlbiA9ICF2YWxpZCB8fCAhdGhpcy5faW5wdXREaXJ0eTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGJsdXIgZXZlbnRzIGZvciB0aGUgdGV4dCBhcmVhLlxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0Qmx1cihldmVudDogRm9jdXNFdmVudCk6IHZvaWQge1xuICAgIC8vIFVwZGF0ZSB0aGUgbWV0YWRhdGEgaWYgbmVjZXNzYXJ5LlxuICAgIGlmICghdGhpcy5faW5wdXREaXJ0eSAmJiB0aGlzLl9kYXRhRGlydHkpIHtcbiAgICAgIHRoaXMuX3NldFZhbHVlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBjbGljayBldmVudHMgZm9yIHRoZSBidXR0b25zLlxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0Q2xpY2soZXZlbnQ6IE1vdXNlRXZlbnQpOiB2b2lkIHtcbiAgICBjb25zdCB0YXJnZXQgPSBldmVudC50YXJnZXQgYXMgSFRNTEVsZW1lbnQ7XG4gICAgaWYgKHRoaXMucmV2ZXJ0QnV0dG9uTm9kZS5jb250YWlucyh0YXJnZXQpKSB7XG4gICAgICB0aGlzLl9zZXRWYWx1ZSgpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5jb21taXRCdXR0b25Ob2RlLmNvbnRhaW5zKHRhcmdldCkpIHtcbiAgICAgIGlmICghdGhpcy5jb21taXRCdXR0b25Ob2RlLmhpZGRlbiAmJiAhdGhpcy5oYXNDbGFzcyhFUlJPUl9DTEFTUykpIHtcbiAgICAgICAgdGhpcy5fY2hhbmdlR3VhcmQgPSB0cnVlO1xuICAgICAgICB0aGlzLl9tZXJnZUNvbnRlbnQoKTtcbiAgICAgICAgdGhpcy5fY2hhbmdlR3VhcmQgPSBmYWxzZTtcbiAgICAgICAgdGhpcy5fc2V0VmFsdWUoKTtcbiAgICAgIH1cbiAgICB9IGVsc2UgaWYgKHRoaXMuZWRpdG9ySG9zdE5vZGUuY29udGFpbnModGFyZ2V0KSkge1xuICAgICAgdGhpcy5lZGl0b3IuZm9jdXMoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogTWVyZ2UgdGhlIHVzZXIgY29udGVudC5cbiAgICovXG4gIHByaXZhdGUgX21lcmdlQ29udGVudCgpOiB2b2lkIHtcbiAgICBjb25zdCBtb2RlbCA9IHRoaXMuZWRpdG9yLm1vZGVsO1xuICAgIGNvbnN0IG9sZCA9IHRoaXMuX29yaWdpbmFsVmFsdWU7XG4gICAgY29uc3QgdXNlciA9IEpTT04ucGFyc2UobW9kZWwuc2hhcmVkTW9kZWwuZ2V0U291cmNlKCkpIGFzIEpTT05PYmplY3Q7XG4gICAgY29uc3Qgc291cmNlID0gdGhpcy5zb3VyY2U7XG4gICAgaWYgKCFzb3VyY2UpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBJZiBpdCBpcyBpbiB1c2VyIGFuZCBoYXMgY2hhbmdlZCBmcm9tIG9sZCwgc2V0IGluIG5ldy5cbiAgICBmb3IgKGNvbnN0IGtleSBpbiB1c2VyKSB7XG4gICAgICBpZiAoIUpTT05FeHQuZGVlcEVxdWFsKHVzZXJba2V5XSwgb2xkW2tleV0gfHwgbnVsbCkpIHtcbiAgICAgICAgc291cmNlLnNldChrZXksIHVzZXJba2V5XSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gSWYgaXQgd2FzIGluIG9sZCBhbmQgaXMgbm90IGluIHVzZXIsIHJlbW92ZSBmcm9tIHNvdXJjZS5cbiAgICBmb3IgKGNvbnN0IGtleSBpbiBvbGQpIHtcbiAgICAgIGlmICghKGtleSBpbiB1c2VyKSkge1xuICAgICAgICBzb3VyY2UuZGVsZXRlKGtleSk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgdmFsdWUgZ2l2ZW4gdGhlIG93bmVyIGNvbnRlbnRzLlxuICAgKi9cbiAgcHJpdmF0ZSBfc2V0VmFsdWUoKTogdm9pZCB7XG4gICAgdGhpcy5fZGF0YURpcnR5ID0gZmFsc2U7XG4gICAgdGhpcy5faW5wdXREaXJ0eSA9IGZhbHNlO1xuICAgIHRoaXMucmV2ZXJ0QnV0dG9uTm9kZS5oaWRkZW4gPSB0cnVlO1xuICAgIHRoaXMuY29tbWl0QnV0dG9uTm9kZS5oaWRkZW4gPSB0cnVlO1xuICAgIHRoaXMucmVtb3ZlQ2xhc3MoRVJST1JfQ0xBU1MpO1xuICAgIGNvbnN0IG1vZGVsID0gdGhpcy5lZGl0b3IubW9kZWw7XG4gICAgY29uc3QgY29udGVudCA9IHRoaXMuX3NvdXJjZSA/IHRoaXMuX3NvdXJjZS50b0pTT04oKSA6IHt9O1xuICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gdHJ1ZTtcbiAgICBpZiAoY29udGVudCA9PT0gdm9pZCAwKSB7XG4gICAgICBtb2RlbC5zaGFyZWRNb2RlbC5zZXRTb3VyY2UodGhpcy5fdHJhbnMuX18oJ05vIGRhdGEhJykpO1xuICAgICAgdGhpcy5fb3JpZ2luYWxWYWx1ZSA9IEpTT05FeHQuZW1wdHlPYmplY3Q7XG4gICAgfSBlbHNlIHtcbiAgICAgIGNvbnN0IHZhbHVlID0gSlNPTi5zdHJpbmdpZnkoY29udGVudCwgbnVsbCwgNCk7XG4gICAgICBtb2RlbC5zaGFyZWRNb2RlbC5zZXRTb3VyY2UodmFsdWUpO1xuICAgICAgdGhpcy5fb3JpZ2luYWxWYWx1ZSA9IGNvbnRlbnQ7XG4gICAgICAvLyBNb3ZlIHRoZSBjdXJzb3IgdG8gd2l0aGluIHRoZSBicmFjZS5cbiAgICAgIGlmICh2YWx1ZS5sZW5ndGggPiAxICYmIHZhbHVlWzBdID09PSAneycpIHtcbiAgICAgICAgdGhpcy5lZGl0b3Iuc2V0Q3Vyc29yUG9zaXRpb24oeyBsaW5lOiAwLCBjb2x1bW46IDEgfSk7XG4gICAgICB9XG4gICAgfVxuICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gZmFsc2U7XG4gICAgdGhpcy5jb21taXRCdXR0b25Ob2RlLmhpZGRlbiA9IHRydWU7XG4gICAgdGhpcy5yZXZlcnRCdXR0b25Ob2RlLmhpZGRlbiA9IHRydWU7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfZGF0YURpcnR5ID0gZmFsc2U7XG4gIHByaXZhdGUgX2lucHV0RGlydHkgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfc291cmNlOiBJT2JzZXJ2YWJsZUpTT04gfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfb3JpZ2luYWxWYWx1ZTogUmVhZG9ubHlQYXJ0aWFsSlNPTk9iamVjdCA9IEpTT05FeHQuZW1wdHlPYmplY3Q7XG4gIHByaXZhdGUgX2NoYW5nZUd1YXJkID0gZmFsc2U7XG59XG5cbi8qKlxuICogVGhlIHN0YXRpYyBuYW1lc3BhY2UgSlNPTkVkaXRvciBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIEpTT05FZGl0b3Ige1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGEganNvbiBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZWRpdG9yIGZhY3RvcnkgdXNlZCBieSB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGVkaXRvckZhY3Rvcnk6IENvZGVFZGl0b3IuRmFjdG9yeTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBQb3B1cCwgc2hvd1BvcHVwLCBUZXh0SXRlbSB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXR1c2Jhcic7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7XG4gIGNsYXNzZXMsXG4gIGxpbmVGb3JtSWNvbixcbiAgUmVhY3RXaWRnZXQsXG4gIFZEb21Nb2RlbCxcbiAgVkRvbVJlbmRlcmVyXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IENvZGVFZGl0b3IgfSBmcm9tICcuL2VkaXRvcic7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIExpbmVGb3JtQ29tcG9uZW50IHN0YXRpY3MuXG4gKi9cbm5hbWVzcGFjZSBMaW5lRm9ybUNvbXBvbmVudCB7XG4gIC8qKlxuICAgKiBUaGUgcHJvcHMgZm9yIExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIEEgY2FsbGJhY2sgZm9yIHdoZW4gdGhlIGZvcm0gaXMgc3VibWl0dGVkLlxuICAgICAqL1xuICAgIGhhbmRsZVN1Ym1pdDogKHZhbHVlOiBudW1iZXIpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBsaW5lIG9mIHRoZSBmb3JtLlxuICAgICAqL1xuICAgIGN1cnJlbnRMaW5lOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbWF4aW11bSBsaW5lIHRoZSBmb3JtIGNhbiB0YWtlICh0eXBpY2FsbHkgdGhlXG4gICAgICogbWF4aW11bSBsaW5lIG9mIHRoZSByZWxldmFudCBlZGl0b3IpLlxuICAgICAqL1xuICAgIG1heExpbmU6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgcHJvcHMgZm9yIExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJU3RhdGUge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IHZhbHVlIG9mIHRoZSBmb3JtLlxuICAgICAqL1xuICAgIHZhbHVlOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBmb3JtIGhhcyBmb2N1cy5cbiAgICAgKi9cbiAgICBoYXNGb2N1czogYm9vbGVhbjtcbiAgfVxufVxuXG4vKipcbiAqIEEgY29tcG9uZW50IGZvciByZW5kZXJpbmcgYSBcImdvLXRvLWxpbmVcIiBmb3JtLlxuICovXG5jbGFzcyBMaW5lRm9ybUNvbXBvbmVudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudDxcbiAgTGluZUZvcm1Db21wb25lbnQuSVByb3BzLFxuICBMaW5lRm9ybUNvbXBvbmVudC5JU3RhdGVcbj4ge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgY29uc3RydWN0b3IocHJvcHM6IExpbmVGb3JtQ29tcG9uZW50LklQcm9wcykge1xuICAgIHN1cGVyKHByb3BzKTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBwcm9wcy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgdmFsdWU6ICcnLFxuICAgICAgaGFzRm9jdXM6IGZhbHNlXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGb2N1cyB0aGUgZWxlbWVudCBvbiBtb3VudC5cbiAgICovXG4gIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgIHRoaXMuX3RleHRJbnB1dCEuZm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgdGhlIExpbmVGb3JtQ29tcG9uZW50LlxuICAgKi9cbiAgcmVuZGVyKCkge1xuICAgIHJldHVybiAoXG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLWxpbmVGb3JtU2VhcmNoXCI+XG4gICAgICAgIDxmb3JtIG5hbWU9XCJsaW5lQ29sdW1uRm9ybVwiIG9uU3VibWl0PXt0aGlzLl9oYW5kbGVTdWJtaXR9IG5vVmFsaWRhdGU+XG4gICAgICAgICAgPGRpdlxuICAgICAgICAgICAgY2xhc3NOYW1lPXtjbGFzc2VzKFxuICAgICAgICAgICAgICAnanAtbGluZUZvcm1XcmFwcGVyJyxcbiAgICAgICAgICAgICAgJ2xtLWxpbmVGb3JtLXdyYXBwZXInLFxuICAgICAgICAgICAgICB0aGlzLnN0YXRlLmhhc0ZvY3VzID8gJ2pwLWxpbmVGb3JtV3JhcHBlckZvY3VzV2l0aGluJyA6IHVuZGVmaW5lZFxuICAgICAgICAgICAgKX1cbiAgICAgICAgICA+XG4gICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgdHlwZT1cInRleHRcIlxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1saW5lRm9ybUlucHV0XCJcbiAgICAgICAgICAgICAgb25DaGFuZ2U9e3RoaXMuX2hhbmRsZUNoYW5nZX1cbiAgICAgICAgICAgICAgb25Gb2N1cz17dGhpcy5faGFuZGxlRm9jdXN9XG4gICAgICAgICAgICAgIG9uQmx1cj17dGhpcy5faGFuZGxlQmx1cn1cbiAgICAgICAgICAgICAgdmFsdWU9e3RoaXMuc3RhdGUudmFsdWV9XG4gICAgICAgICAgICAgIHJlZj17aW5wdXQgPT4ge1xuICAgICAgICAgICAgICAgIHRoaXMuX3RleHRJbnB1dCA9IGlucHV0O1xuICAgICAgICAgICAgICB9fVxuICAgICAgICAgICAgLz5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtYmFzZUxpbmVGb3JtIGpwLWxpbmVGb3JtQnV0dG9uQ29udGFpbmVyXCI+XG4gICAgICAgICAgICAgIDxsaW5lRm9ybUljb24ucmVhY3RcbiAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1iYXNlTGluZUZvcm0ganAtbGluZUZvcm1CdXR0b25JY29uXCJcbiAgICAgICAgICAgICAgICBlbGVtZW50UG9zaXRpb249XCJjZW50ZXJcIlxuICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgICB0eXBlPVwic3VibWl0XCJcbiAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1iYXNlTGluZUZvcm0ganAtbGluZUZvcm1CdXR0b25cIlxuICAgICAgICAgICAgICAgIHZhbHVlPVwiXCJcbiAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDxsYWJlbCBjbGFzc05hbWU9XCJqcC1saW5lRm9ybUNhcHRpb25cIj5cbiAgICAgICAgICAgIHt0aGlzLl90cmFucy5fXyhcbiAgICAgICAgICAgICAgJ0dvIHRvIGxpbmUgbnVtYmVyIGJldHdlZW4gMSBhbmQgJTEnLFxuICAgICAgICAgICAgICB0aGlzLnByb3BzLm1heExpbmVcbiAgICAgICAgICAgICl9XG4gICAgICAgICAgPC9sYWJlbD5cbiAgICAgICAgPC9mb3JtPlxuICAgICAgPC9kaXY+XG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIHZhbHVlIGluIHRoZSBpbnB1dCBmaWVsZC5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZUNoYW5nZSA9IChldmVudDogUmVhY3QuQ2hhbmdlRXZlbnQ8SFRNTElucHV0RWxlbWVudD4pID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHsgdmFsdWU6IGV2ZW50LmN1cnJlbnRUYXJnZXQudmFsdWUgfSk7XG4gIH07XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBzdWJtaXNzaW9uIG9mIHRoZSBpbnB1dCBmaWVsZC5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZVN1Ym1pdCA9IChldmVudDogUmVhY3QuRm9ybUV2ZW50PEhUTUxGb3JtRWxlbWVudD4pID0+IHtcbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuXG4gICAgY29uc3QgdmFsdWUgPSBwYXJzZUludCh0aGlzLl90ZXh0SW5wdXQhLnZhbHVlLCAxMCk7XG4gICAgaWYgKFxuICAgICAgIWlzTmFOKHZhbHVlKSAmJlxuICAgICAgaXNGaW5pdGUodmFsdWUpICYmXG4gICAgICAxIDw9IHZhbHVlICYmXG4gICAgICB2YWx1ZSA8PSB0aGlzLnByb3BzLm1heExpbmVcbiAgICApIHtcbiAgICAgIHRoaXMucHJvcHMuaGFuZGxlU3VibWl0KHZhbHVlKTtcbiAgICB9XG5cbiAgICByZXR1cm4gZmFsc2U7XG4gIH07XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBmb2N1c2luZyBvZiB0aGUgaW5wdXQgZmllbGQuXG4gICAqL1xuICBwcml2YXRlIF9oYW5kbGVGb2N1cyA9ICgpID0+IHtcbiAgICB0aGlzLnNldFN0YXRlKHsgaGFzRm9jdXM6IHRydWUgfSk7XG4gIH07XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBibHVycmluZyBvZiB0aGUgaW5wdXQgZmllbGQuXG4gICAqL1xuICBwcml2YXRlIF9oYW5kbGVCbHVyID0gKCkgPT4ge1xuICAgIHRoaXMuc2V0U3RhdGUoeyBoYXNGb2N1czogZmFsc2UgfSk7XG4gIH07XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF90cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gIHByaXZhdGUgX3RleHRJbnB1dDogSFRNTElucHV0RWxlbWVudCB8IG51bGwgPSBudWxsO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBMaW5lQ29sQ29tcG9uZW50LlxuICovXG5uYW1lc3BhY2UgTGluZUNvbENvbXBvbmVudCB7XG4gIC8qKlxuICAgKiBQcm9wcyBmb3IgTGluZUNvbENvbXBvbmVudC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBsaW5lIG51bWJlci5cbiAgICAgKi9cbiAgICBsaW5lOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBjb2x1bW4gbnVtYmVyLlxuICAgICAqL1xuICAgIGNvbHVtbjogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuXG4gICAgLyoqXG4gICAgICogQSBjbGljayBoYW5kbGVyIGZvciB0aGUgTGluZUNvbENvbXBvbmVudCwgd2hpY2hcbiAgICAgKiB3ZSB1c2UgdG8gbGF1bmNoIHRoZSBMaW5lRm9ybUNvbXBvbmVudC5cbiAgICAgKi9cbiAgICBoYW5kbGVDbGljazogKCkgPT4gdm9pZDtcbiAgfVxufVxuXG4vKipcbiAqIEEgcHVyZSBmdW5jdGlvbmFsIGNvbXBvbmVudCBmb3IgcmVuZGVyaW5nIGEgbGluZS9jb2x1bW5cbiAqIHN0YXR1cyBpdGVtLlxuICovXG5mdW5jdGlvbiBMaW5lQ29sQ29tcG9uZW50KFxuICBwcm9wczogTGluZUNvbENvbXBvbmVudC5JUHJvcHNcbik6IFJlYWN0LlJlYWN0RWxlbWVudDxMaW5lQ29sQ29tcG9uZW50LklQcm9wcz4ge1xuICBjb25zdCB0cmFuc2xhdG9yID0gcHJvcHMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgcmV0dXJuIChcbiAgICA8VGV4dEl0ZW1cbiAgICAgIG9uQ2xpY2s9e3Byb3BzLmhhbmRsZUNsaWNrfVxuICAgICAgc291cmNlPXt0cmFucy5fXygnTG4gJTEsIENvbCAlMicsIHByb3BzLmxpbmUsIHByb3BzLmNvbHVtbil9XG4gICAgICB0aXRsZT17dHJhbnMuX18oJ0dvIHRvIGxpbmUgbnVtYmVy4oCmJyl9XG4gICAgLz5cbiAgKTtcbn1cblxuLyoqXG4gKiBBIHdpZGdldCBpbXBsZW1lbnRpbmcgYSBsaW5lL2NvbHVtbiBzdGF0dXMgaXRlbS5cbiAqL1xuZXhwb3J0IGNsYXNzIExpbmVDb2wgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8TGluZUNvbC5Nb2RlbD4ge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IExpbmVDb2wgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICBjb25zdHJ1Y3Rvcih0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3IpIHtcbiAgICBzdXBlcihuZXcgTGluZUNvbC5Nb2RlbCgpKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1tb2QtaGlnaGxpZ2h0ZWQnKTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICByZW5kZXIoKTogUmVhY3QuUmVhY3RFbGVtZW50PExpbmVDb2xDb21wb25lbnQuSVByb3BzPiB8IG51bGwge1xuICAgIGlmICh0aGlzLm1vZGVsID09PSBudWxsKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPExpbmVDb2xDb21wb25lbnRcbiAgICAgICAgICBsaW5lPXt0aGlzLm1vZGVsLmxpbmV9XG4gICAgICAgICAgY29sdW1uPXt0aGlzLm1vZGVsLmNvbHVtbn1cbiAgICAgICAgICB0cmFuc2xhdG9yPXt0aGlzLnRyYW5zbGF0b3J9XG4gICAgICAgICAgaGFuZGxlQ2xpY2s9eygpID0+IHRoaXMuX2hhbmRsZUNsaWNrKCl9XG4gICAgICAgIC8+XG4gICAgICApO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9oYW5kbGVDbGljaygpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fcG9wdXApIHtcbiAgICAgIHRoaXMuX3BvcHVwLmRpc3Bvc2UoKTtcbiAgICB9XG4gICAgY29uc3QgYm9keSA9IFJlYWN0V2lkZ2V0LmNyZWF0ZShcbiAgICAgIDxMaW5lRm9ybUNvbXBvbmVudFxuICAgICAgICBoYW5kbGVTdWJtaXQ9e3ZhbCA9PiB0aGlzLl9oYW5kbGVTdWJtaXQodmFsKX1cbiAgICAgICAgY3VycmVudExpbmU9e3RoaXMubW9kZWwhLmxpbmV9XG4gICAgICAgIG1heExpbmU9e3RoaXMubW9kZWwhLmVkaXRvciEubGluZUNvdW50fVxuICAgICAgICB0cmFuc2xhdG9yPXt0aGlzLnRyYW5zbGF0b3J9XG4gICAgICAvPlxuICAgICk7XG5cbiAgICB0aGlzLl9wb3B1cCA9IHNob3dQb3B1cCh7XG4gICAgICBib2R5OiBib2R5LFxuICAgICAgYW5jaG9yOiB0aGlzLFxuICAgICAgYWxpZ246ICdyaWdodCdcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgc3VibWlzc2lvbiBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2hhbmRsZVN1Ym1pdCh2YWx1ZTogbnVtYmVyKTogdm9pZCB7XG4gICAgdGhpcy5tb2RlbCEuZWRpdG9yIS5zZXRDdXJzb3JQb3NpdGlvbih7IGxpbmU6IHZhbHVlIC0gMSwgY29sdW1uOiAwIH0pO1xuICAgIHRoaXMuX3BvcHVwIS5kaXNwb3NlKCk7XG4gICAgdGhpcy5tb2RlbCEuZWRpdG9yIS5mb2N1cygpO1xuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9wb3B1cDogUG9wdXAgfCBudWxsID0gbnVsbDtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgTGluZUNvbCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIExpbmVDb2wge1xuICAvKipcbiAgICogQSBWRG9tIG1vZGVsIGZvciBhIHN0YXR1cyBpdGVtIHRyYWNraW5nIHRoZSBsaW5lL2NvbHVtbiBvZiBhbiBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgTW9kZWwgZXh0ZW5kcyBWRG9tTW9kZWwge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IGVkaXRvciBvZiB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgZ2V0IGVkaXRvcigpOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9lZGl0b3I7XG4gICAgfVxuICAgIHNldCBlZGl0b3IoZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsKSB7XG4gICAgICBjb25zdCBvbGRFZGl0b3IgPSB0aGlzLl9lZGl0b3I7XG4gICAgICBpZiAob2xkRWRpdG9yPy5tb2RlbD8uc2VsZWN0aW9ucykge1xuICAgICAgICBvbGRFZGl0b3IubW9kZWwuc2VsZWN0aW9ucy5jaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5fb25TZWxlY3Rpb25DaGFuZ2VkKTtcbiAgICAgIH1cblxuICAgICAgY29uc3Qgb2xkU3RhdGUgPSB0aGlzLl9nZXRBbGxTdGF0ZSgpO1xuICAgICAgdGhpcy5fZWRpdG9yID0gZWRpdG9yO1xuICAgICAgaWYgKCF0aGlzLl9lZGl0b3IpIHtcbiAgICAgICAgdGhpcy5fY29sdW1uID0gMTtcbiAgICAgICAgdGhpcy5fbGluZSA9IDE7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB0aGlzLl9lZGl0b3IubW9kZWwuc2VsZWN0aW9ucy5jaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25TZWxlY3Rpb25DaGFuZ2VkKTtcblxuICAgICAgICBjb25zdCBwb3MgPSB0aGlzLl9lZGl0b3IuZ2V0Q3Vyc29yUG9zaXRpb24oKTtcbiAgICAgICAgdGhpcy5fY29sdW1uID0gcG9zLmNvbHVtbiArIDE7XG4gICAgICAgIHRoaXMuX2xpbmUgPSBwb3MubGluZSArIDE7XG4gICAgICB9XG5cbiAgICAgIHRoaXMuX3RyaWdnZXJDaGFuZ2Uob2xkU3RhdGUsIHRoaXMuX2dldEFsbFN0YXRlKCkpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IGxpbmUgb2YgdGhlIG1vZGVsLlxuICAgICAqL1xuICAgIGdldCBsaW5lKCk6IG51bWJlciB7XG4gICAgICByZXR1cm4gdGhpcy5fbGluZTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBjb2x1bW4gb2YgdGhlIG1vZGVsLlxuICAgICAqL1xuICAgIGdldCBjb2x1bW4oKTogbnVtYmVyIHtcbiAgICAgIHJldHVybiB0aGlzLl9jb2x1bW47XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVhY3QgdG8gYSBjaGFuZ2UgaW4gdGhlIGN1cnNvcnMgb2YgdGhlIGN1cnJlbnQgZWRpdG9yLlxuICAgICAqL1xuICAgIHByaXZhdGUgX29uU2VsZWN0aW9uQ2hhbmdlZCA9ICgpID0+IHtcbiAgICAgIGNvbnN0IG9sZFN0YXRlID0gdGhpcy5fZ2V0QWxsU3RhdGUoKTtcbiAgICAgIGNvbnN0IHBvcyA9IHRoaXMuZWRpdG9yIS5nZXRDdXJzb3JQb3NpdGlvbigpO1xuICAgICAgdGhpcy5fbGluZSA9IHBvcy5saW5lICsgMTtcbiAgICAgIHRoaXMuX2NvbHVtbiA9IHBvcy5jb2x1bW4gKyAxO1xuXG4gICAgICB0aGlzLl90cmlnZ2VyQ2hhbmdlKG9sZFN0YXRlLCB0aGlzLl9nZXRBbGxTdGF0ZSgpKTtcbiAgICB9O1xuXG4gICAgcHJpdmF0ZSBfZ2V0QWxsU3RhdGUoKTogW251bWJlciwgbnVtYmVyXSB7XG4gICAgICByZXR1cm4gW3RoaXMuX2xpbmUsIHRoaXMuX2NvbHVtbl07XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfdHJpZ2dlckNoYW5nZShcbiAgICAgIG9sZFN0YXRlOiBbbnVtYmVyLCBudW1iZXJdLFxuICAgICAgbmV3U3RhdGU6IFtudW1iZXIsIG51bWJlcl1cbiAgICApIHtcbiAgICAgIGlmIChvbGRTdGF0ZVswXSAhPT0gbmV3U3RhdGVbMF0gfHwgb2xkU3RhdGVbMV0gIT09IG5ld1N0YXRlWzFdKSB7XG4gICAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBwcml2YXRlIF9saW5lOiBudW1iZXIgPSAxO1xuICAgIHByaXZhdGUgX2NvbHVtbjogbnVtYmVyID0gMTtcbiAgICBwcml2YXRlIF9lZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvciB8IG51bGwgPSBudWxsO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIG5iZm9ybWF0IGZyb20gJ0BqdXB5dGVybGFiL25iZm9ybWF0JztcblxuLyoqXG4gKiBUaGUgbWltZSB0eXBlIHNlcnZpY2Ugb2YgYSBjb2RlIGVkaXRvci5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlIHtcbiAgLyoqXG4gICAqIEdldCBhIG1pbWUgdHlwZSBmb3IgdGhlIGdpdmVuIGxhbmd1YWdlIGluZm8uXG4gICAqXG4gICAqIEBwYXJhbSBpbmZvIC0gVGhlIGxhbmd1YWdlIGluZm9ybWF0aW9uLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHZhbGlkIG1pbWV0eXBlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIElmIGEgbWltZSB0eXBlIGNhbm5vdCBiZSBmb3VuZCByZXR1cm5zIHRoZSBkZWZhdWx0IG1pbWUgdHlwZSBgdGV4dC9wbGFpbmAsIG5ldmVyIGBudWxsYC5cbiAgICogVGhlcmUgbWF5IGJlIG1vcmUgdGhhbiBvbmUgbWltZSB0eXBlLCBidXQgb25seSB0aGUgZmlyc3Qgb25lIHdpbGwgYmUgcmV0dXJuZWQuXG4gICAqIFRvIGFjY2VzcyBhbGwgbWltZSB0eXBlcywgdXNlIGBJRWRpdG9yTGFuZ3VhZ2VSZWdpc3RyeWAgaW5zdGVhZC5cbiAgICovXG4gIGdldE1pbWVUeXBlQnlMYW5ndWFnZShpbmZvOiBuYmZvcm1hdC5JTGFuZ3VhZ2VJbmZvTWV0YWRhdGEpOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIEdldCBhIG1pbWUgdHlwZSBmb3IgdGhlIGdpdmVuIGZpbGUgcGF0aC5cbiAgICpcbiAgICogQHBhcmFtIGZpbGVQYXRoIC0gVGhlIGZ1bGwgcGF0aCB0byB0aGUgZmlsZS5cbiAgICpcbiAgICogQHJldHVybnMgQSB2YWxpZCBtaW1ldHlwZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJZiBhIG1pbWUgdHlwZSBjYW5ub3QgYmUgZm91bmQgcmV0dXJucyB0aGUgZGVmYXVsdCBtaW1lIHR5cGUgYHRleHQvcGxhaW5gLCBuZXZlciBgbnVsbGAuXG4gICAqIFRoZXJlIG1heSBiZSBtb3JlIHRoYW4gb25lIG1pbWUgdHlwZSwgYnV0IG9ubHkgdGhlIGZpcnN0IG9uZSB3aWxsIGJlIHJldHVybmVkLlxuICAgKiBUbyBhY2Nlc3MgYWxsIG1pbWUgdHlwZXMsIHVzZSBgSUVkaXRvckxhbmd1YWdlUmVnaXN0cnlgIGluc3RlYWQuXG4gICAqL1xuICBnZXRNaW1lVHlwZUJ5RmlsZVBhdGgoZmlsZVBhdGg6IHN0cmluZyk6IHN0cmluZztcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYElFZGl0b3JNaW1lVHlwZVNlcnZpY2VgLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElFZGl0b3JNaW1lVHlwZVNlcnZpY2Uge1xuICAvKipcbiAgICogVGhlIGRlZmF1bHQgbWltZSB0eXBlLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRNaW1lVHlwZTogc3RyaW5nID0gJ3RleHQvcGxhaW4nO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnLi9lZGl0b3InO1xuaW1wb3J0IHsgSUVkaXRvckZhY3RvcnlTZXJ2aWNlIH0gZnJvbSAnLi9mYWN0b3J5JztcbmltcG9ydCB7IElFZGl0b3JNaW1lVHlwZVNlcnZpY2UgfSBmcm9tICcuL21pbWV0eXBlJztcblxuLyoqXG4gKiBDb2RlIGVkaXRvciBzZXJ2aWNlcyB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElFZGl0b3JTZXJ2aWNlcyA9IG5ldyBUb2tlbjxJRWRpdG9yU2VydmljZXM+KFxuICAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcjpJRWRpdG9yU2VydmljZXMnLFxuICBgQSBzZXJ2aWNlIGZvciB0aGUgdGV4dCBlZGl0b3IgcHJvdmlkZXJcbiAgZm9yIHRoZSBhcHBsaWNhdGlvbi4gVXNlIHRoaXMgdG8gY3JlYXRlIG5ldyB0ZXh0IGVkaXRvcnMgYW5kIGhvc3QgdGhlbSBpbiB5b3VyXG4gIFVJIGVsZW1lbnRzLmBcbik7XG5cbi8qKlxuICogQ29kZSBlZGl0b3Igc2VydmljZXMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUVkaXRvclNlcnZpY2VzIHtcbiAgLyoqXG4gICAqIFRoZSBjb2RlIGVkaXRvciBmYWN0b3J5LlxuICAgKi9cbiAgcmVhZG9ubHkgZmFjdG9yeVNlcnZpY2U6IElFZGl0b3JGYWN0b3J5U2VydmljZTtcblxuICAvKipcbiAgICogVGhlIGVkaXRvciBtaW1lIHR5cGUgc2VydmljZS5cbiAgICovXG4gIHJlYWRvbmx5IG1pbWVUeXBlU2VydmljZTogSUVkaXRvck1pbWVUeXBlU2VydmljZTtcbn1cblxuLyoqXG4gKiBDb2RlIGVkaXRvciBjdXJzb3IgcG9zaXRpb24gdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJUG9zaXRpb25Nb2RlbCA9IG5ldyBUb2tlbjxJUG9zaXRpb25Nb2RlbD4oXG4gICdAanVweXRlcmxhYi9jb2RlZWRpdG9yOklQb3NpdGlvbk1vZGVsJyxcbiAgYEEgc2VydmljZSB0byBoYW5kbGUgYW4gY29kZSBlZGl0b3IgY3Vyc29yIHBvc2l0aW9uLmBcbik7XG5cbi8qKlxuICogQ29kZSBlZGl0b3IgY3Vyc29yIHBvc2l0aW9uIG1vZGVsLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElQb3NpdGlvbk1vZGVsIHtcbiAgLyoqXG4gICAqIEFkZCBhIGVkaXRvciBwcm92aWRlci5cbiAgICpcbiAgICogQSBwcm92aWRlciB3aWxsIHJlY2VpdmUgdGhlIGN1cnJlbnRseSBhY3RpdmUgd2lkZ2V0IGFuZCBtdXN0IHJldHVybiB0aGVcbiAgICogYXNzb2NpYXRlZCBlZGl0b3IgaWYgaXQgY2FuIG9yIG51bGwgb3RoZXJ3aXNlLlxuICAgKi9cbiAgYWRkRWRpdG9yUHJvdmlkZXI6IChcbiAgICBwcm92aWRlcjogKHdpZGdldDogV2lkZ2V0IHwgbnVsbCkgPT4gUHJvbWlzZTxDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsPlxuICApID0+IHZvaWQ7XG5cbiAgLyoqXG4gICAqIENhbGxiYWNrIHRvIGZvcmNlIHVwZGF0aW5nIHRoZSBwcm92aWRlclxuICAgKi9cbiAgdXBkYXRlKCk6IHZvaWQ7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFN0YWNrZWRMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnLi9lZGl0b3InO1xuaW1wb3J0IHsgQ29kZUVkaXRvcldyYXBwZXIgfSBmcm9tICcuL3dpZGdldCc7XG5cbmV4cG9ydCBjbGFzcyBDb2RlVmlld2VyV2lkZ2V0IGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBjb2RlIHZpZXdlciB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBDb2RlVmlld2VyV2lkZ2V0LklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLm1vZGVsID0gb3B0aW9ucy5tb2RlbDtcblxuICAgIGNvbnN0IGVkaXRvcldpZGdldCA9IG5ldyBDb2RlRWRpdG9yV3JhcHBlcih7XG4gICAgICBmYWN0b3J5OiBvcHRpb25zLmZhY3RvcnksXG4gICAgICBtb2RlbDogdGhpcy5tb2RlbCxcbiAgICAgIGVkaXRvck9wdGlvbnM6IHtcbiAgICAgICAgLi4ub3B0aW9ucy5lZGl0b3JPcHRpb25zLFxuICAgICAgICBjb25maWc6IHsgLi4ub3B0aW9ucy5lZGl0b3JPcHRpb25zPy5jb25maWcsIHJlYWRPbmx5OiB0cnVlIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgICB0aGlzLmVkaXRvciA9IGVkaXRvcldpZGdldC5lZGl0b3I7XG5cbiAgICBjb25zdCBsYXlvdXQgPSAodGhpcy5sYXlvdXQgPSBuZXcgU3RhY2tlZExheW91dCgpKTtcbiAgICBsYXlvdXQuYWRkV2lkZ2V0KGVkaXRvcldpZGdldCk7XG4gIH1cblxuICBzdGF0aWMgY3JlYXRlQ29kZVZpZXdlcihcbiAgICBvcHRpb25zOiBDb2RlVmlld2VyV2lkZ2V0LklOb01vZGVsT3B0aW9uc1xuICApOiBDb2RlVmlld2VyV2lkZ2V0IHtcbiAgICBjb25zdCB7IGNvbnRlbnQsIG1pbWVUeXBlLCAuLi5vdGhlcnMgfSA9IG9wdGlvbnM7XG4gICAgY29uc3QgbW9kZWwgPSBuZXcgQ29kZUVkaXRvci5Nb2RlbCh7XG4gICAgICBtaW1lVHlwZVxuICAgIH0pO1xuICAgIG1vZGVsLnNoYXJlZE1vZGVsLnNldFNvdXJjZShjb250ZW50KTtcbiAgICBjb25zdCB3aWRnZXQgPSBuZXcgQ29kZVZpZXdlcldpZGdldCh7IC4uLm90aGVycywgbW9kZWwgfSk7XG4gICAgd2lkZ2V0LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgbW9kZWwuZGlzcG9zZSgpO1xuICAgIH0pO1xuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICBnZXQgY29udGVudCgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLm1vZGVsLnNoYXJlZE1vZGVsLmdldFNvdXJjZSgpO1xuICB9XG5cbiAgZ2V0IG1pbWVUeXBlKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMubW9kZWwubWltZVR5cGU7XG4gIH1cblxuICByZWFkb25seSBtb2RlbDogQ29kZUVkaXRvci5JTW9kZWw7XG4gIHJlYWRvbmx5IGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGNvZGUgdmlld2VyIHdpZGdldC5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb2RlVmlld2VyV2lkZ2V0IHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGFuIGNvZGUgdmlld2VyIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIEEgY29kZSBlZGl0b3IgZmFjdG9yeS5cbiAgICAgKi9cbiAgICBmYWN0b3J5OiBDb2RlRWRpdG9yLkZhY3Rvcnk7XG4gICAgLyoqXG4gICAgICogVGhlIGNvbnRlbnQgbW9kZWwgZm9yIHRoZSB2aWV3ZXIuXG4gICAgICovXG4gICAgbW9kZWw6IENvZGVFZGl0b3IuSU1vZGVsO1xuICAgIC8qKlxuICAgICAqIENvZGUgZWRpdG9yIG9wdGlvbnNcbiAgICAgKi9cbiAgICBlZGl0b3JPcHRpb25zPzogT21pdDxDb2RlRWRpdG9yLklPcHRpb25zLCAnaG9zdCcgfCAnbW9kZWwnPjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGNyZWF0ZSBhbiBjb2RlIHZpZXdlciB3aWRnZXQgd2l0aG91dCBhIG1vZGVsLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTm9Nb2RlbE9wdGlvbnMgZXh0ZW5kcyBPbWl0PElPcHRpb25zLCAnbW9kZWwnPiB7XG4gICAgLyoqXG4gICAgICogVGhlIGNvbnRlbnQgdG8gZGlzcGxheSBpbiB0aGUgdmlld2VyLlxuICAgICAqL1xuICAgIGNvbnRlbnQ6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBtaW1lIHR5cGUgZm9yIHRoZSBjb250ZW50LlxuICAgICAqL1xuICAgIG1pbWVUeXBlPzogc3RyaW5nO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IE1pbWVEYXRhIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRHJhZyB9IGZyb20gJ0BsdW1pbm8vZHJhZ2Ryb3AnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnLi8nO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGFuIGVkaXRvciB3aWRnZXQgdGhhdCBoYXMgYSBwcmltYXJ5IHNlbGVjdGlvbi5cbiAqL1xuY29uc3QgSEFTX1NFTEVDVElPTl9DTEFTUyA9ICdqcC1tb2QtaGFzLXByaW1hcnktc2VsZWN0aW9uJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhbiBlZGl0b3Igd2lkZ2V0IHRoYXQgaGFzIGEgY3Vyc29yL3NlbGVjdGlvblxuICogd2l0aGluIHRoZSB3aGl0ZXNwYWNlIGF0IHRoZSBiZWdpbm5pbmcgb2YgYSBsaW5lXG4gKi9cbmNvbnN0IEhBU19JTl9MRUFESU5HX1dISVRFU1BBQ0VfQ0xBU1MgPSAnanAtbW9kLWluLWxlYWRpbmctd2hpdGVzcGFjZSc7XG5cbi8qKlxuICogQSBjbGFzcyB1c2VkIHRvIGluZGljYXRlIGEgZHJvcCB0YXJnZXQuXG4gKi9cbmNvbnN0IERST1BfVEFSR0VUX0NMQVNTID0gJ2pwLW1vZC1kcm9wVGFyZ2V0JztcblxuLyoqXG4gKiBSZWdFeHAgdG8gdGVzdCBmb3IgbGVhZGluZyB3aGl0ZXNwYWNlXG4gKi9cbmNvbnN0IGxlYWRpbmdXaGl0ZXNwYWNlUmUgPSAvXlxccyskLztcblxuLyoqXG4gKiBBIHdpZGdldCB3aGljaCBob3N0cyBhIGNvZGUgZWRpdG9yLlxuICovXG5leHBvcnQgY2xhc3MgQ29kZUVkaXRvcldyYXBwZXIgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IGNvZGUgZWRpdG9yIHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IENvZGVFZGl0b3JXcmFwcGVyLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICBjb25zdCB7IGZhY3RvcnksIG1vZGVsLCBlZGl0b3JPcHRpb25zIH0gPSBvcHRpb25zO1xuICAgIGNvbnN0IGVkaXRvciA9ICh0aGlzLmVkaXRvciA9IGZhY3Rvcnkoe1xuICAgICAgaG9zdDogdGhpcy5ub2RlLFxuICAgICAgbW9kZWwsXG4gICAgICAuLi5lZGl0b3JPcHRpb25zXG4gICAgfSkpO1xuICAgIGVkaXRvci5tb2RlbC5zZWxlY3Rpb25zLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vblNlbGVjdGlvbnNDaGFuZ2VkLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGVkaXRvciB3cmFwcGVkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICByZWFkb25seSBlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvcjtcblxuICAvKipcbiAgICogR2V0IHRoZSBtb2RlbCB1c2VkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICBnZXQgbW9kZWwoKTogQ29kZUVkaXRvci5JTW9kZWwge1xuICAgIHJldHVybiB0aGlzLmVkaXRvci5tb2RlbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuZWRpdG9yLmRpc3Bvc2UoKTtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICogY2FsbGVkIGluIHJlc3BvbnNlIHRvIGV2ZW50cyBvbiB0aGUgbm90ZWJvb2sgcGFuZWwncyBub2RlLiBJdCBzaG91bGRcbiAgICogbm90IGJlIGNhbGxlZCBkaXJlY3RseSBieSB1c2VyIGNvZGUuXG4gICAqL1xuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBzd2l0Y2ggKGV2ZW50LnR5cGUpIHtcbiAgICAgIGNhc2UgJ2xtLWRyYWdlbnRlcic6XG4gICAgICAgIHRoaXMuX2V2dERyYWdFbnRlcihldmVudCBhcyBEcmFnLkV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdsbS1kcmFnbGVhdmUnOlxuICAgICAgICB0aGlzLl9ldnREcmFnTGVhdmUoZXZlbnQgYXMgRHJhZy5FdmVudCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnbG0tZHJhZ292ZXInOlxuICAgICAgICB0aGlzLl9ldnREcmFnT3ZlcihldmVudCBhcyBEcmFnLkV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdsbS1kcm9wJzpcbiAgICAgICAgdGhpcy5fZXZ0RHJvcChldmVudCBhcyBEcmFnLkV2ZW50KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAnYWN0aXZhdGUtcmVxdWVzdCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWN0aXZhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMuZWRpdG9yLmZvY3VzKCk7XG4gIH1cblxuICAvKipcbiAgICogQSBtZXNzYWdlIGhhbmRsZXIgaW52b2tlZCBvbiBhbiBgJ2FmdGVyLWF0dGFjaCdgIG1lc3NhZ2UuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBzdXBlci5vbkFmdGVyQXR0YWNoKG1zZyk7XG4gICAgY29uc3Qgbm9kZSA9IHRoaXMubm9kZTtcbiAgICBub2RlLmFkZEV2ZW50TGlzdGVuZXIoJ2xtLWRyYWdlbnRlcicsIHRoaXMpO1xuICAgIG5vZGUuYWRkRXZlbnRMaXN0ZW5lcignbG0tZHJhZ2xlYXZlJywgdGhpcyk7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdsbS1kcmFnb3ZlcicsIHRoaXMpO1xuICAgIG5vZGUuYWRkRXZlbnRMaXN0ZW5lcignbG0tZHJvcCcsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgYmVmb3JlLWRldGFjaGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3Qgbm9kZSA9IHRoaXMubm9kZTtcbiAgICBub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2xtLWRyYWdlbnRlcicsIHRoaXMpO1xuICAgIG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignbG0tZHJhZ2xlYXZlJywgdGhpcyk7XG4gICAgbm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdsbS1kcmFnb3ZlcicsIHRoaXMpO1xuICAgIG5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcignbG0tZHJvcCcsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSBpbiBtb2RlbCBzZWxlY3Rpb25zLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25TZWxlY3Rpb25zQ2hhbmdlZCgpOiB2b2lkIHtcbiAgICBjb25zdCB7IHN0YXJ0LCBlbmQgfSA9IHRoaXMuZWRpdG9yLmdldFNlbGVjdGlvbigpO1xuXG4gICAgaWYgKHN0YXJ0LmNvbHVtbiAhPT0gZW5kLmNvbHVtbiB8fCBzdGFydC5saW5lICE9PSBlbmQubGluZSkge1xuICAgICAgLy8gYSBzZWxlY3Rpb24gd2FzIG1hZGVcbiAgICAgIHRoaXMuYWRkQ2xhc3MoSEFTX1NFTEVDVElPTl9DTEFTUyk7XG4gICAgICB0aGlzLnJlbW92ZUNsYXNzKEhBU19JTl9MRUFESU5HX1dISVRFU1BBQ0VfQ0xBU1MpO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyB0aGUgY3Vyc29yIHdhcyBwbGFjZWRcbiAgICAgIHRoaXMucmVtb3ZlQ2xhc3MoSEFTX1NFTEVDVElPTl9DTEFTUyk7XG5cbiAgICAgIGlmIChcbiAgICAgICAgdGhpcy5lZGl0b3JcbiAgICAgICAgICAuZ2V0TGluZShlbmQubGluZSkhXG4gICAgICAgICAgLnNsaWNlKDAsIGVuZC5jb2x1bW4pXG4gICAgICAgICAgLm1hdGNoKGxlYWRpbmdXaGl0ZXNwYWNlUmUpXG4gICAgICApIHtcbiAgICAgICAgdGhpcy5hZGRDbGFzcyhIQVNfSU5fTEVBRElOR19XSElURVNQQUNFX0NMQVNTKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMucmVtb3ZlQ2xhc3MoSEFTX0lOX0xFQURJTkdfV0hJVEVTUEFDRV9DTEFTUyk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgYCdsbS1kcmFnZW50ZXInYCBldmVudCBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2V2dERyYWdFbnRlcihldmVudDogRHJhZy5FdmVudCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmVkaXRvci5nZXRPcHRpb24oJ3JlYWRPbmx5JykgPT09IHRydWUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgZGF0YSA9IFByaXZhdGUuZmluZFRleHREYXRhKGV2ZW50Lm1pbWVEYXRhKTtcbiAgICBpZiAoZGF0YSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGV2ZW50LnByZXZlbnREZWZhdWx0KCk7XG4gICAgZXZlbnQuc3RvcFByb3BhZ2F0aW9uKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtbW9kLWRyb3BUYXJnZXQnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGAnbG0tZHJhZ2xlYXZlJ2AgZXZlbnQgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcml2YXRlIF9ldnREcmFnTGVhdmUoZXZlbnQ6IERyYWcuRXZlbnQpOiB2b2lkIHtcbiAgICB0aGlzLnJlbW92ZUNsYXNzKERST1BfVEFSR0VUX0NMQVNTKTtcbiAgICBpZiAodGhpcy5lZGl0b3IuZ2V0T3B0aW9uKCdyZWFkT25seScpID09PSB0cnVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGRhdGEgPSBQcml2YXRlLmZpbmRUZXh0RGF0YShldmVudC5taW1lRGF0YSk7XG4gICAgaWYgKGRhdGEgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgIGV2ZW50LnN0b3BQcm9wYWdhdGlvbigpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgYCdsbS1kcmFnb3ZlcidgIGV2ZW50IGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfZXZ0RHJhZ092ZXIoZXZlbnQ6IERyYWcuRXZlbnQpOiB2b2lkIHtcbiAgICB0aGlzLnJlbW92ZUNsYXNzKERST1BfVEFSR0VUX0NMQVNTKTtcbiAgICBpZiAodGhpcy5lZGl0b3IuZ2V0T3B0aW9uKCdyZWFkT25seScpID09PSB0cnVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGRhdGEgPSBQcml2YXRlLmZpbmRUZXh0RGF0YShldmVudC5taW1lRGF0YSk7XG4gICAgaWYgKGRhdGEgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgIGV2ZW50LnN0b3BQcm9wYWdhdGlvbigpO1xuICAgIGV2ZW50LmRyb3BBY3Rpb24gPSAnY29weSc7XG4gICAgdGhpcy5hZGRDbGFzcyhEUk9QX1RBUkdFVF9DTEFTUyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBgJ2xtLWRyb3AnYCBldmVudCBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX2V2dERyb3AoZXZlbnQ6IERyYWcuRXZlbnQpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5lZGl0b3IuZ2V0T3B0aW9uKCdyZWFkT25seScpID09PSB0cnVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGRhdGEgPSBQcml2YXRlLmZpbmRUZXh0RGF0YShldmVudC5taW1lRGF0YSk7XG4gICAgaWYgKGRhdGEgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBjb29yZGluYXRlID0ge1xuICAgICAgdG9wOiBldmVudC55LFxuICAgICAgYm90dG9tOiBldmVudC55LFxuICAgICAgbGVmdDogZXZlbnQueCxcbiAgICAgIHJpZ2h0OiBldmVudC54LFxuICAgICAgeDogZXZlbnQueCxcbiAgICAgIHk6IGV2ZW50LnksXG4gICAgICB3aWR0aDogMCxcbiAgICAgIGhlaWdodDogMFxuICAgIH0gYXMgQ29kZUVkaXRvci5JQ29vcmRpbmF0ZTtcbiAgICBjb25zdCBwb3NpdGlvbiA9IHRoaXMuZWRpdG9yLmdldFBvc2l0aW9uRm9yQ29vcmRpbmF0ZShjb29yZGluYXRlKTtcbiAgICBpZiAocG9zaXRpb24gPT09IG51bGwpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5yZW1vdmVDbGFzcyhEUk9QX1RBUkdFVF9DTEFTUyk7XG4gICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICBldmVudC5zdG9wUHJvcGFnYXRpb24oKTtcbiAgICBpZiAoZXZlbnQucHJvcG9zZWRBY3Rpb24gPT09ICdub25lJykge1xuICAgICAgZXZlbnQuZHJvcEFjdGlvbiA9ICdub25lJztcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3Qgb2Zmc2V0ID0gdGhpcy5lZGl0b3IuZ2V0T2Zmc2V0QXQocG9zaXRpb24pO1xuICAgIHRoaXMubW9kZWwuc2hhcmVkTW9kZWwudXBkYXRlU291cmNlKG9mZnNldCwgb2Zmc2V0LCBkYXRhKTtcbiAgfVxufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIHRoZSBgQ29kZUVkaXRvcldyYXBwZXJgIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQ29kZUVkaXRvcldyYXBwZXIge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGEgY29kZSBlZGl0b3Igd2lkZ2V0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogQSBjb2RlIGVkaXRvciBmYWN0b3J5LlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoZSB3aWRnZXQgbmVlZHMgYSBmYWN0b3J5IGFuZCBhIHRoZSBlZGl0b3Igb3B0aW9uc1xuICAgICAqIGJlY2F1c2UgaXQgbmVlZHMgdG8gcHJvdmlkZSBpdHMgb3duIG5vZGUgYXMgdGhlIGhvc3QuXG4gICAgICovXG4gICAgZmFjdG9yeTogQ29kZUVkaXRvci5GYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbnRlbnQgbW9kZWwgZm9yIHRoZSB3cmFwcGVyLlxuICAgICAqL1xuICAgIG1vZGVsOiBDb2RlRWRpdG9yLklNb2RlbDtcblxuICAgIC8qKlxuICAgICAqIENvZGUgZWRpdG9yIG9wdGlvbnNcbiAgICAgKi9cbiAgICBlZGl0b3JPcHRpb25zPzogT21pdDxDb2RlRWRpdG9yLklPcHRpb25zLCAnaG9zdCcgfCAnbW9kZWwnPjtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGZ1bmN0aW9uYWxpdHkuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEdpdmVuIGEgTWltZURhdGEgaW5zdGFuY2UsIGV4dHJhY3QgdGhlIGZpcnN0IHRleHQgZGF0YSwgaWYgYW55LlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGZpbmRUZXh0RGF0YShtaW1lOiBNaW1lRGF0YSk6IHN0cmluZyB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgdHlwZXMgPSBtaW1lLnR5cGVzKCk7XG4gICAgY29uc3QgdGV4dFR5cGUgPSB0eXBlcy5maW5kKHQgPT4gdC5pbmRleE9mKCd0ZXh0JykgPT09IDApO1xuICAgIGlmICh0ZXh0VHlwZSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICByZXR1cm4gdW5kZWZpbmVkO1xuICAgIH1cbiAgICByZXR1cm4gbWltZS5nZXREYXRhKHRleHRUeXBlKSBhcyBzdHJpbmc7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==