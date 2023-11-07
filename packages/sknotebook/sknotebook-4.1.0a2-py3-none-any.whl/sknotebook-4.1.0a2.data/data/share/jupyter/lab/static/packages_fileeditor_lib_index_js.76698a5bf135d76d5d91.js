"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_fileeditor_lib_index_js"],{

/***/ "../packages/fileeditor/lib/fileeditorlspadapter.js":
/*!**********************************************************!*\
  !*** ../packages/fileeditor/lib/fileeditorlspadapter.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FileEditorAdapter": () => (/* binding */ FileEditorAdapter)
/* harmony export */ });
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/lsp */ "webpack/sharing/consume/default/@jupyterlab/lsp/@jupyterlab/lsp");
/* harmony import */ var _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



class FileEditorAdapter extends _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__.WidgetLSPAdapter {
    constructor(editorWidget, options) {
        const { docRegistry, ...others } = options;
        super(editorWidget, others);
        this._readyDelegate = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
        this.editor = editorWidget.content;
        this._docRegistry = docRegistry;
        // Ensure editor uniqueness
        this._virtualEditor = Object.freeze({
            getEditor: () => this.editor.editor,
            ready: () => Promise.resolve(this.editor.editor),
            reveal: () => Promise.resolve(this.editor.editor)
        });
        Promise.all([this.editor.context.ready, this.connectionManager.ready])
            .then(async () => {
            await this.initOnceReady();
            this._readyDelegate.resolve();
        })
            .catch(console.error);
    }
    /**
     * Promise that resolves once the adapter is initialized
     */
    get ready() {
        return this._readyDelegate.promise;
    }
    /**
     * Get current path of the document.
     */
    get documentPath() {
        return this.widget.context.path;
    }
    /**
     * Get the mime type of the document.
     */
    get mimeType() {
        var _a;
        const mimeTypeFromModel = this.editor.model.mimeType;
        const codeMirrorMimeType = Array.isArray(mimeTypeFromModel)
            ? (_a = mimeTypeFromModel[0]) !== null && _a !== void 0 ? _a : _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__.IEditorMimeTypeService.defaultMimeType
            : mimeTypeFromModel;
        const contentsModel = this.editor.context.contentsModel;
        // when MIME type is not known it defaults to 'text/plain',
        // so if it is different we can accept it as it is
        if (codeMirrorMimeType != _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__.IEditorMimeTypeService.defaultMimeType) {
            return codeMirrorMimeType;
        }
        else if (contentsModel) {
            // a script that does not have a MIME type known by the editor
            // (no syntax highlight mode), can still be known by the document
            // registry (and this is arguably easier to extend).
            let fileType = this._docRegistry.getFileTypeForModel(contentsModel);
            return fileType.mimeTypes[0];
        }
        else {
            // "text/plain" this is
            return codeMirrorMimeType;
        }
    }
    /**
     * Get the file extension of the document.
     */
    get languageFileExtension() {
        let parts = this.documentPath.split('.');
        return parts[parts.length - 1];
    }
    /**
     * Get the CM editor
     */
    get ceEditor() {
        return this.editor.editor;
    }
    /**
     * Get the activated CM editor.
     */
    get activeEditor() {
        return this._virtualEditor;
    }
    /**
     * Get the inner HTMLElement of the document widget.
     */
    get wrapperElement() {
        return this.widget.node;
    }
    /**
     * Get current path of the document.
     */
    get path() {
        return this.widget.context.path;
    }
    /**
     *  Get the list of CM editors in the document, there is only one editor
     * in the case of file editor.
     */
    get editors() {
        var _a, _b;
        return [
            {
                ceEditor: this._virtualEditor,
                type: 'code',
                value: (_b = (_a = this.editor) === null || _a === void 0 ? void 0 : _a.model.sharedModel.getSource()) !== null && _b !== void 0 ? _b : ''
            }
        ];
    }
    /**
     * Dispose the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.editor.model.mimeTypeChanged.disconnect(this.reloadConnection);
        super.dispose();
    }
    /**
     * Generate the virtual document associated with the document.
     */
    createVirtualDocument() {
        return new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_1__.VirtualDocument({
            language: this.language,
            foreignCodeExtractors: this.options.foreignCodeExtractorsManager,
            path: this.documentPath,
            fileExtension: this.languageFileExtension,
            // notebooks are continuous, each cell is dependent on the previous one
            standalone: true,
            // notebooks are not supported by LSP servers
            hasLspSupportedFile: true
        });
    }
    /**
     * Get the index of editor from the cursor position in the virtual
     * document. Since there is only one editor, this method always return
     * 0
     * @deprecated This is error-prone and will be removed in JupyterLab 5.0, use `getEditorIndex()` with `virtualDocument.getEditorAtVirtualLine(position)` instead.
     *
     * @param position - the position of cursor in the virtual document.
     * @return  {number} - index of the virtual editor
     */
    getEditorIndexAt(position) {
        return 0;
    }
    /**
     * Get the index of input editor
     *
     * @param ceEditor - instance of the code editor
     */
    getEditorIndex(ceEditor) {
        return 0;
    }
    /**
     * Get the wrapper of input editor.
     *
     * @param ceEditor
     * @return  {HTMLElement}
     */
    getEditorWrapper(ceEditor) {
        return this.wrapperElement;
    }
    /**
     * Initialization function called once the editor and the LSP connection
     * manager is ready. This function will create the virtual document and
     * connect various signals.
     */
    async initOnceReady() {
        this.initVirtual();
        // connect the document, but do not open it as the adapter will handle this
        // after registering all features
        await this.connectDocument(this.virtualDocument, false);
        this.editor.model.mimeTypeChanged.connect(this.reloadConnection, this);
    }
}


/***/ }),

/***/ "../packages/fileeditor/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/fileeditor/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditorSyntaxStatus": () => (/* reexport safe */ _syntaxstatus__WEBPACK_IMPORTED_MODULE_2__.EditorSyntaxStatus),
/* harmony export */   "EditorTableOfContentsFactory": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_4__.EditorTableOfContentsFactory),
/* harmony export */   "FileEditor": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_6__.FileEditor),
/* harmony export */   "FileEditorAdapter": () => (/* reexport safe */ _fileeditorlspadapter__WEBPACK_IMPORTED_MODULE_0__.FileEditorAdapter),
/* harmony export */   "FileEditorFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_6__.FileEditorFactory),
/* harmony export */   "FileEditorSearchProvider": () => (/* reexport safe */ _searchprovider__WEBPACK_IMPORTED_MODULE_1__.FileEditorSearchProvider),
/* harmony export */   "IEditorTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_5__.IEditorTracker),
/* harmony export */   "LaTeXTableOfContentsFactory": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_4__.LaTeXTableOfContentsFactory),
/* harmony export */   "LaTeXTableOfContentsModel": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_4__.LaTeXTableOfContentsModel),
/* harmony export */   "MarkdownTableOfContentsFactory": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_4__.MarkdownTableOfContentsFactory),
/* harmony export */   "MarkdownTableOfContentsModel": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_4__.MarkdownTableOfContentsModel),
/* harmony export */   "PythonTableOfContentsFactory": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_4__.PythonTableOfContentsFactory),
/* harmony export */   "PythonTableOfContentsModel": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_4__.PythonTableOfContentsModel),
/* harmony export */   "TabSpaceStatus": () => (/* reexport safe */ _tabspacestatus__WEBPACK_IMPORTED_MODULE_3__.TabSpaceStatus)
/* harmony export */ });
/* harmony import */ var _fileeditorlspadapter__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./fileeditorlspadapter */ "../packages/fileeditor/lib/fileeditorlspadapter.js");
/* harmony import */ var _searchprovider__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./searchprovider */ "../packages/fileeditor/lib/searchprovider.js");
/* harmony import */ var _syntaxstatus__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./syntaxstatus */ "../packages/fileeditor/lib/syntaxstatus.js");
/* harmony import */ var _tabspacestatus__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tabspacestatus */ "../packages/fileeditor/lib/tabspacestatus.js");
/* harmony import */ var _toc__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./toc */ "../packages/fileeditor/lib/toc/index.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tokens */ "../packages/fileeditor/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "../packages/fileeditor/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module fileeditor
 */









/***/ }),

/***/ "../packages/fileeditor/lib/searchprovider.js":
/*!****************************************************!*\
  !*** ../packages/fileeditor/lib/searchprovider.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FileEditorSearchProvider": () => (/* binding */ FileEditorSearchProvider)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "../packages/fileeditor/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * File editor search provider
 */
class FileEditorSearchProvider extends _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__.EditorSearchProvider {
    /**
     * Constructor
     * @param widget File editor panel
     */
    constructor(widget) {
        super();
        this.widget = widget;
    }
    get isReadOnly() {
        return this.editor.getOption('readOnly');
    }
    /**
     * Support for options adjusting replacement behavior.
     */
    get replaceOptionsSupport() {
        return {
            preserveCase: true
        };
    }
    /**
     * Text editor
     */
    get editor() {
        return this.widget.content.editor;
    }
    /**
     * Editor content model
     */
    get model() {
        return this.widget.content.model;
    }
    async startQuery(query, filters) {
        await super.startQuery(query, filters);
        await this.highlightNext(true, {
            from: 'selection-start',
            scroll: false,
            select: false
        });
    }
    /**
     * Instantiate a search provider for the widget.
     *
     * #### Notes
     * The widget provided is always checked using `isApplicable` before calling
     * this factory.
     *
     * @param widget The widget to search on
     * @param translator [optional] The translator object
     *
     * @returns The search provider on the widget
     */
    static createNew(widget, translator) {
        return new FileEditorSearchProvider(widget);
    }
    /**
     * Report whether or not this provider has the ability to search on the given object
     */
    static isApplicable(domain) {
        return (domain instanceof _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget &&
            domain.content instanceof _widget__WEBPACK_IMPORTED_MODULE_2__.FileEditor &&
            domain.content.editor instanceof _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_1__.CodeMirrorEditor);
    }
    /**
     * Get an initial query value if applicable so that it can be entered
     * into the search box as an initial query
     *
     * @returns Initial value used to populate the search box.
     */
    getInitialQuery() {
        const cm = this.editor;
        const selection = cm.state.sliceDoc(cm.state.selection.main.from, cm.state.selection.main.to);
        return selection;
    }
}


/***/ }),

/***/ "../packages/fileeditor/lib/syntaxstatus.js":
/*!**************************************************!*\
  !*** ../packages/fileeditor/lib/syntaxstatus.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditorSyntaxStatus": () => (/* binding */ EditorSyntaxStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */






/**
 * A pure function that returns a tsx component for an editor syntax item.
 *
 * @param props: the props for the component.
 *
 * @returns an editor syntax component.
 */
function EditorSyntaxComponent(props) {
    return react__WEBPACK_IMPORTED_MODULE_5___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.TextItem, { source: props.language, onClick: props.handleClick });
}
/**
 * StatusBar item to change the language syntax highlighting of the file editor.
 */
class EditorSyntaxStatus extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.VDomRenderer {
    /**
     * Construct a new VDomRenderer for the status item.
     */
    constructor(options) {
        var _a;
        super(new EditorSyntaxStatus.Model(options.languages));
        /**
         * Create a menu for selecting the language of the editor.
         */
        this._handleClick = () => {
            const languageMenu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Menu({ commands: this._commands });
            const command = 'fileeditor:change-language';
            if (this._popup) {
                this._popup.dispose();
            }
            this.model.languages
                .getLanguages()
                .sort((a, b) => {
                var _a, _b;
                const aName = (_a = a.displayName) !== null && _a !== void 0 ? _a : a.name;
                const bName = (_b = b.displayName) !== null && _b !== void 0 ? _b : b.name;
                return aName.localeCompare(bName);
            })
                .forEach(spec => {
                var _a;
                if (spec.name.toLowerCase().indexOf('brainf') === 0) {
                    return;
                }
                const args = {
                    name: spec.name,
                    displayName: (_a = spec.displayName) !== null && _a !== void 0 ? _a : spec.name
                };
                languageMenu.addItem({
                    command,
                    args
                });
            });
            this._popup = (0,_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_1__.showPopup)({
                body: languageMenu,
                anchor: this,
                align: 'left'
            });
        };
        this._popup = null;
        this._commands = options.commands;
        this.translator = (_a = options.translator) !== null && _a !== void 0 ? _a : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        this.addClass('jp-mod-highlighted');
        this.title.caption = trans.__('Change text editor syntax highlighting');
    }
    /**
     * Render the status item.
     */
    render() {
        if (!this.model) {
            return null;
        }
        return (react__WEBPACK_IMPORTED_MODULE_5___default().createElement(EditorSyntaxComponent, { language: this.model.language, handleClick: this._handleClick }));
    }
}
/**
 * A namespace for EditorSyntax statics.
 */
(function (EditorSyntaxStatus) {
    /**
     * A VDomModel for the current editor/mode combination.
     */
    class Model extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.VDomModel {
        constructor(languages) {
            super();
            this.languages = languages;
            /**
             * If the editor mode changes, update the model.
             */
            this._onMIMETypeChange = (mode, change) => {
                var _a;
                const oldLanguage = this._language;
                const spec = this.languages.findByMIME(change.newValue);
                this._language = (_a = spec === null || spec === void 0 ? void 0 : spec.name) !== null && _a !== void 0 ? _a : _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__.IEditorMimeTypeService.defaultMimeType;
                this._triggerChange(oldLanguage, this._language);
            };
            this._language = '';
            this._editor = null;
        }
        /**
         * The current editor language. If no editor is present,
         * returns the empty string.
         */
        get language() {
            return this._language;
        }
        /**
         * The current editor for the application editor tracker.
         */
        get editor() {
            return this._editor;
        }
        set editor(editor) {
            var _a;
            const oldEditor = this._editor;
            if (oldEditor !== null) {
                oldEditor.model.mimeTypeChanged.disconnect(this._onMIMETypeChange);
            }
            const oldLanguage = this._language;
            this._editor = editor;
            if (this._editor === null) {
                this._language = '';
            }
            else {
                const spec = this.languages.findByMIME(this._editor.model.mimeType);
                this._language = (_a = spec === null || spec === void 0 ? void 0 : spec.name) !== null && _a !== void 0 ? _a : _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__.IEditorMimeTypeService.defaultMimeType;
                this._editor.model.mimeTypeChanged.connect(this._onMIMETypeChange);
            }
            this._triggerChange(oldLanguage, this._language);
        }
        /**
         * Trigger a rerender of the model.
         */
        _triggerChange(oldState, newState) {
            if (oldState !== newState) {
                this.stateChanged.emit(void 0);
            }
        }
    }
    EditorSyntaxStatus.Model = Model;
})(EditorSyntaxStatus || (EditorSyntaxStatus = {}));


/***/ }),

/***/ "../packages/fileeditor/lib/tabspacestatus.js":
/*!****************************************************!*\
  !*** ../packages/fileeditor/lib/tabspacestatus.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TabSpaceStatus": () => (/* binding */ TabSpaceStatus)
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
 * A pure functional component for rendering the TabSpace status.
 */
function TabSpaceComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    const description = typeof props.tabSpace === 'number'
        ? trans.__('Spaces')
        : trans.__('Tab Indent');
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__.TextItem, { onClick: props.handleClick, source: typeof props.tabSpace === 'number'
            ? `${description}: ${props.tabSpace}`
            : description, title: trans.__('Change the indentation…') }));
}
/**
 * A VDomRenderer for a tabs vs. spaces status item.
 */
class TabSpaceStatus extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomRenderer {
    /**
     * Create a new tab/space status item.
     */
    constructor(options) {
        super(new TabSpaceStatus.Model());
        this._popup = null;
        this._menu = options.menu;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this.addClass('jp-mod-highlighted');
    }
    /**
     * Render the TabSpace status item.
     */
    render() {
        var _a;
        if (!((_a = this.model) === null || _a === void 0 ? void 0 : _a.indentUnit)) {
            return null;
        }
        else {
            const tabSpace = this.model.indentUnit === 'Tab'
                ? null
                : parseInt(this.model.indentUnit, 10);
            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(TabSpaceComponent, { tabSpace: tabSpace, handleClick: () => this._handleClick(), translator: this.translator }));
        }
    }
    /**
     * Handle a click on the status item.
     */
    _handleClick() {
        const menu = this._menu;
        if (this._popup) {
            this._popup.dispose();
        }
        menu.aboutToClose.connect(this._menuClosed, this);
        this._popup = (0,_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__.showPopup)({
            body: menu,
            anchor: this,
            align: 'right'
        });
        // Update the menu items
        menu.update();
    }
    _menuClosed() {
        this.removeClass('jp-mod-clicked');
    }
}
/**
 * A namespace for TabSpace statics.
 */
(function (TabSpaceStatus) {
    /**
     * A VDomModel for the TabSpace status item.
     */
    class Model extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomModel {
        /**
         * Code editor indentation unit
         */
        get indentUnit() {
            return this._indentUnit;
        }
        set indentUnit(v) {
            if (v !== this._indentUnit) {
                this._indentUnit = v;
                this.stateChanged.emit();
            }
        }
    }
    TabSpaceStatus.Model = Model;
})(TabSpaceStatus || (TabSpaceStatus = {}));


/***/ }),

/***/ "../packages/fileeditor/lib/toc/factory.js":
/*!*************************************************!*\
  !*** ../packages/fileeditor/lib/toc/factory.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditorTableOfContentsFactory": () => (/* binding */ EditorTableOfContentsFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Base table of contents model factory for file editor
 */
class EditorTableOfContentsFactory extends _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsFactory {
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    createNew(widget, configuration) {
        const model = super.createNew(widget, configuration);
        const onActiveHeadingChanged = (model, heading) => {
            if (heading) {
                widget.content.editor.setCursorPosition({
                    line: heading.line,
                    column: 0
                });
            }
        };
        model.activeHeadingChanged.connect(onActiveHeadingChanged);
        widget.disposed.connect(() => {
            model.activeHeadingChanged.disconnect(onActiveHeadingChanged);
        });
        return model;
    }
}


/***/ }),

/***/ "../packages/fileeditor/lib/toc/index.js":
/*!***********************************************!*\
  !*** ../packages/fileeditor/lib/toc/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditorTableOfContentsFactory": () => (/* reexport safe */ _factory__WEBPACK_IMPORTED_MODULE_0__.EditorTableOfContentsFactory),
/* harmony export */   "LaTeXTableOfContentsFactory": () => (/* reexport safe */ _latex__WEBPACK_IMPORTED_MODULE_1__.LaTeXTableOfContentsFactory),
/* harmony export */   "LaTeXTableOfContentsModel": () => (/* reexport safe */ _latex__WEBPACK_IMPORTED_MODULE_1__.LaTeXTableOfContentsModel),
/* harmony export */   "MarkdownTableOfContentsFactory": () => (/* reexport safe */ _markdown__WEBPACK_IMPORTED_MODULE_2__.MarkdownTableOfContentsFactory),
/* harmony export */   "MarkdownTableOfContentsModel": () => (/* reexport safe */ _markdown__WEBPACK_IMPORTED_MODULE_2__.MarkdownTableOfContentsModel),
/* harmony export */   "PythonTableOfContentsFactory": () => (/* reexport safe */ _python__WEBPACK_IMPORTED_MODULE_3__.PythonTableOfContentsFactory),
/* harmony export */   "PythonTableOfContentsModel": () => (/* reexport safe */ _python__WEBPACK_IMPORTED_MODULE_3__.PythonTableOfContentsModel)
/* harmony export */ });
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./factory */ "../packages/fileeditor/lib/toc/factory.js");
/* harmony import */ var _latex__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./latex */ "../packages/fileeditor/lib/toc/latex.js");
/* harmony import */ var _markdown__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./markdown */ "../packages/fileeditor/lib/toc/markdown.js");
/* harmony import */ var _python__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./python */ "../packages/fileeditor/lib/toc/python.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/***/ }),

/***/ "../packages/fileeditor/lib/toc/latex.js":
/*!***********************************************!*\
  !*** ../packages/fileeditor/lib/toc/latex.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LaTeXTableOfContentsFactory": () => (/* binding */ LaTeXTableOfContentsFactory),
/* harmony export */   "LaTeXTableOfContentsModel": () => (/* binding */ LaTeXTableOfContentsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./factory */ "../packages/fileeditor/lib/toc/factory.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Maps LaTeX section headings to HTML header levels.
 *
 * ## Notes
 *
 * -   As `part` and `chapter` section headings appear to be less common, assign them to heading level 1.
 *
 * @private
 */
const LATEX_LEVELS = {
    part: 1,
    chapter: 1,
    section: 1,
    subsection: 2,
    subsubsection: 3,
    paragraph: 4,
    subparagraph: 5
};
/**
 * Regular expression to create the outline
 */
const SECTIONS = /^\s*\\(section|subsection|subsubsection){(.+)}/;
/**
 * Table of content model for LaTeX files.
 */
class LaTeXTableOfContentsModel extends _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsModel {
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'latex';
    }
    /**
     * List of configuration options supported by the model.
     */
    get supportedOptions() {
        return ['maximalDepth', 'numberHeaders'];
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    getHeadings() {
        if (!this.isActive) {
            return Promise.resolve(null);
        }
        // Split the text into lines:
        const lines = this.widget.content.model.sharedModel
            .getSource()
            .split('\n');
        const levels = new Array();
        let previousLevel = levels.length;
        const headings = new Array();
        for (let i = 0; i < lines.length; i++) {
            const match = lines[i].match(SECTIONS);
            if (match) {
                const level = LATEX_LEVELS[match[1]];
                if (level <= this.configuration.maximalDepth) {
                    const prefix = _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.getPrefix(level, previousLevel, levels, {
                        ...this.configuration,
                        // Force base numbering and numbering first level
                        baseNumbering: 1,
                        numberingH1: true
                    });
                    previousLevel = level;
                    headings.push({
                        text: match[2],
                        prefix: prefix,
                        level,
                        line: i
                    });
                }
            }
        }
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for LaTeX files.
 */
class LaTeXTableOfContentsFactory extends _factory__WEBPACK_IMPORTED_MODULE_1__.EditorTableOfContentsFactory {
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        var _a, _b;
        const isApplicable = super.isApplicable(widget);
        if (isApplicable) {
            let mime = (_b = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.mimeType;
            return mime && (mime === 'text/x-latex' || mime === 'text/x-stex');
        }
        return false;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        return new LaTeXTableOfContentsModel(widget, configuration);
    }
}


/***/ }),

/***/ "../packages/fileeditor/lib/toc/markdown.js":
/*!**************************************************!*\
  !*** ../packages/fileeditor/lib/toc/markdown.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MarkdownTableOfContentsFactory": () => (/* binding */ MarkdownTableOfContentsFactory),
/* harmony export */   "MarkdownTableOfContentsModel": () => (/* binding */ MarkdownTableOfContentsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./factory */ "../packages/fileeditor/lib/toc/factory.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Table of content model for Markdown files.
 */
class MarkdownTableOfContentsModel extends _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsModel {
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'markdown';
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    getHeadings() {
        if (!this.isActive) {
            return Promise.resolve(null);
        }
        const content = this.widget.content.model.sharedModel.getSource();
        const headings = _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.filterHeadings(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.Markdown.getHeadings(content), {
            ...this.configuration,
            // Force removing numbering as they cannot be displayed
            // in the document
            numberHeaders: false
        });
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for Markdown files.
 */
class MarkdownTableOfContentsFactory extends _factory__WEBPACK_IMPORTED_MODULE_1__.EditorTableOfContentsFactory {
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        var _a, _b;
        const isApplicable = super.isApplicable(widget);
        if (isApplicable) {
            let mime = (_b = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.mimeType;
            return mime && _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.Markdown.isMarkdown(mime);
        }
        return false;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        return new MarkdownTableOfContentsModel(widget, configuration);
    }
}


/***/ }),

/***/ "../packages/fileeditor/lib/toc/python.js":
/*!************************************************!*\
  !*** ../packages/fileeditor/lib/toc/python.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PythonTableOfContentsFactory": () => (/* binding */ PythonTableOfContentsFactory),
/* harmony export */   "PythonTableOfContentsModel": () => (/* binding */ PythonTableOfContentsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./factory */ "../packages/fileeditor/lib/toc/factory.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Regular expression to create the outline
 */
let KEYWORDS;
try {
    // https://github.com/tc39/proposal-regexp-match-indices was accepted
    // in May 2021 (https://github.com/tc39/proposals/blob/main/finished-proposals.md)
    // So we will fallback to the polyfill regexp-match-indices if not available
    KEYWORDS = new RegExp('^\\s*(class |def |from |import )', 'd');
}
catch (_a) {
    KEYWORDS = new RegExp('^\\s*(class |def |from |import )');
}
/**
 * Table of content model for Python files.
 */
class PythonTableOfContentsModel extends _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsModel {
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'python';
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    async getHeadings() {
        if (!this.isActive) {
            return Promise.resolve(null);
        }
        // Split the text into lines:
        const lines = this.widget.content.model.sharedModel
            .getSource()
            .split('\n');
        // Iterate over the lines to get the heading level and text for each line:
        let headings = new Array();
        let processingImports = false;
        let indent = 1;
        let lineIdx = -1;
        for (const line of lines) {
            lineIdx++;
            let hasKeyword;
            if (KEYWORDS.flags.includes('d')) {
                hasKeyword = KEYWORDS.exec(line);
            }
            else {
                const { default: execWithIndices } = await __webpack_require__.e(/*! import() */ "vendors-node_modules_regexp-match-indices_index_js").then(__webpack_require__.t.bind(__webpack_require__, /*! regexp-match-indices */ "../node_modules/regexp-match-indices/index.js", 23));
                hasKeyword = execWithIndices(KEYWORDS, line);
            }
            if (hasKeyword) {
                // Index 0 contains the spaces, index 1 is the keyword group
                const [start] = hasKeyword.indices[1];
                if (indent === 1 && start > 0) {
                    indent = start;
                }
                const isImport = ['from ', 'import '].includes(hasKeyword[1]);
                if (isImport && processingImports) {
                    continue;
                }
                processingImports = isImport;
                const level = 1 + start / indent;
                if (level > this.configuration.maximalDepth) {
                    continue;
                }
                headings.push({
                    text: line.slice(start),
                    level,
                    line: lineIdx
                });
            }
        }
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for Python files.
 */
class PythonTableOfContentsFactory extends _factory__WEBPACK_IMPORTED_MODULE_1__.EditorTableOfContentsFactory {
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        var _a, _b;
        const isApplicable = super.isApplicable(widget);
        if (isApplicable) {
            let mime = (_b = (_a = widget.content) === null || _a === void 0 ? void 0 : _a.model) === null || _b === void 0 ? void 0 : _b.mimeType;
            return (mime &&
                (mime === 'application/x-python-code' || mime === 'text/x-python'));
        }
        return false;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        return new PythonTableOfContentsModel(widget, configuration);
    }
}


/***/ }),

/***/ "../packages/fileeditor/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/fileeditor/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IEditorTracker": () => (/* binding */ IEditorTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The editor tracker token.
 */
const IEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/fileeditor:IEditorTracker', `A widget tracker for file editors.
  Use this if you want to be able to iterate over and interact with file editors
  created by the application.`);


/***/ }),

/***/ "../packages/fileeditor/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/fileeditor/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FileEditor": () => (/* binding */ FileEditor),
/* harmony export */   "FileEditorFactory": () => (/* binding */ FileEditorFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The data attribute added to a widget that can run code.
 */
const CODE_RUNNER = 'jpCodeRunner';
/**
 * The data attribute added to a widget that can undo.
 */
const UNDOER = 'jpUndoer';
/**
 * A widget for editors.
 */
class FileEditor extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new editor widget.
     */
    constructor(options) {
        super();
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        this.addClass('jp-FileEditor');
        const context = (this._context = options.context);
        this._mimeTypeService = options.mimeTypeService;
        const editorWidget = (this._editorWidget = new _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_0__.CodeEditorWrapper({
            factory: options.factory,
            model: context.model,
            editorOptions: {
                config: FileEditor.defaultEditorConfig
            }
        }));
        this._editorWidget.addClass('jp-FileEditorCodeWrapper');
        this._editorWidget.node.dataset[CODE_RUNNER] = 'true';
        this._editorWidget.node.dataset[UNDOER] = 'true';
        this.editor = editorWidget.editor;
        this.model = editorWidget.model;
        void context.ready.then(() => {
            this._onContextReady();
        });
        // Listen for changes to the path.
        this._onPathChanged();
        context.pathChanged.connect(this._onPathChanged, this);
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.StackedLayout());
        layout.addWidget(editorWidget);
    }
    /**
     * Get the context for the editor widget.
     */
    get context() {
        return this._context;
    }
    /**
     * A promise that resolves when the file editor is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the widget's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        if (!this.model) {
            return;
        }
        switch (event.type) {
            case 'mousedown':
                this._ensureFocus();
                break;
            default:
                break;
        }
    }
    /**
     * Handle `after-attach` messages for the widget.
     */
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        const node = this.node;
        node.addEventListener('mousedown', this);
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        const node = this.node;
        node.removeEventListener('mousedown', this);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this._ensureFocus();
    }
    /**
     * Ensure that the widget has focus.
     */
    _ensureFocus() {
        if (!this.editor.hasFocus()) {
            this.editor.focus();
        }
    }
    /**
     * Handle actions that should be taken when the context is ready.
     */
    _onContextReady() {
        if (this.isDisposed) {
            return;
        }
        // Prevent the initial loading from disk from being in the editor history.
        this.editor.clearHistory();
        // Resolve the ready promise.
        this._ready.resolve(undefined);
    }
    /**
     * Handle a change to the path.
     */
    _onPathChanged() {
        const editor = this.editor;
        const localPath = this._context.localPath;
        editor.model.mimeType =
            this._mimeTypeService.getMimeTypeByFilePath(localPath);
    }
}
/**
 * The namespace for editor widget statics.
 */
(function (FileEditor) {
    /**
     * File editor default configuration.
     */
    FileEditor.defaultEditorConfig = {
        lineNumbers: true,
        scrollPastEnd: true
    };
})(FileEditor || (FileEditor = {}));
/**
 * A widget factory for editors.
 */
class FileEditorFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Construct a new editor widget factory.
     */
    constructor(options) {
        super(options.factoryOptions);
        this._services = options.editorServices;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const func = this._services.factoryService.newDocumentEditor;
        const factory = options => {
            // Use same id as document factory
            return func(options);
        };
        const content = new FileEditor({
            factory,
            context,
            mimeTypeService: this._services.mimeTypeService
        });
        content.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.textEditorIcon;
        const widget = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget({ content, context });
        return widget;
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZmlsZWVkaXRvcl9saWJfaW5kZXhfanMuNzY2OThhNWJmMTM1ZDc2ZDVkOTEuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFSztBQVN2QztBQUMyQjtBQVc3QyxNQUFNLGlCQUFrQixTQUFRLDZEQUV0QztJQUNDLFlBQ0UsWUFBeUMsRUFDekMsT0FBa0M7UUFFbEMsTUFBTSxFQUFFLFdBQVcsRUFBRSxHQUFHLE1BQU0sRUFBRSxHQUFHLE9BQU8sQ0FBQztRQUMzQyxLQUFLLENBQUMsWUFBWSxFQUFFLE1BQU0sQ0FBQyxDQUFDO1FBaU10QixtQkFBYyxHQUFHLElBQUksOERBQWUsRUFBUSxDQUFDO1FBaE1uRCxJQUFJLENBQUMsTUFBTSxHQUFHLFlBQVksQ0FBQyxPQUFPLENBQUM7UUFDbkMsSUFBSSxDQUFDLFlBQVksR0FBRyxXQUFXLENBQUM7UUFFaEMsMkJBQTJCO1FBQzNCLElBQUksQ0FBQyxjQUFjLEdBQUcsTUFBTSxDQUFDLE1BQU0sQ0FBQztZQUNsQyxTQUFTLEVBQUUsR0FBRyxFQUFFLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxNQUFNO1lBQ25DLEtBQUssRUFBRSxHQUFHLEVBQUUsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsTUFBTSxDQUFDO1lBQ2hELE1BQU0sRUFBRSxHQUFHLEVBQUUsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxNQUFNLENBQUMsTUFBTSxDQUFDO1NBQ2xELENBQUMsQ0FBQztRQUVILE9BQU8sQ0FBQyxHQUFHLENBQUMsQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxLQUFLLEVBQUUsSUFBSSxDQUFDLGlCQUFpQixDQUFDLEtBQUssQ0FBQyxDQUFDO2FBQ25FLElBQUksQ0FBQyxLQUFLLElBQUksRUFBRTtZQUNmLE1BQU0sSUFBSSxDQUFDLGFBQWEsRUFBRSxDQUFDO1lBQzNC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cUJBQXFCLENBQUMsU0FBUyxDQUFDLENBQUM7SUFDM0QsQ0FBQztDQVFGO0FBRUQ7O0dBRUc7QUFDSCxXQUFpQixVQUFVO0lBcUJ6Qjs7T0FFRztJQUNVLDhCQUFtQixHQUF3QjtRQUN0RCxXQUFXLEVBQUUsSUFBSTtRQUNqQixhQUFhLEVBQUUsSUFBSTtLQUNwQixDQUFDO0FBQ0osQ0FBQyxFQTVCZ0IsVUFBVSxLQUFWLFVBQVUsUUE0QjFCO0FBRUQ7O0dBRUc7QUFDSSxNQUFNLGlCQUFrQixTQUFRLHFFQUd0QztJQUNDOztPQUVHO0lBQ0gsWUFBWSxPQUFtQztRQUM3QyxLQUFLLENBQUMsT0FBTyxDQUFDLGNBQWMsQ0FBQyxDQUFDO1FBQzlCLElBQUksQ0FBQyxTQUFTLEdBQUcsT0FBTyxDQUFDLGNBQWMsQ0FBQztJQUMxQyxDQUFDO0lBRUQ7O09BRUc7SUFDTyxlQUFlLENBQ3ZCLE9BQXFDO1FBRXJDLE1BQU0sSUFBSSxHQUFHLElBQUksQ0FBQyxTQUFTLENBQUMsY0FBYyxDQUFDLGlCQUFpQixDQUFDO1FBQzdELE1BQU0sT0FBTyxHQUF1QixPQUFPLENBQUMsRUFBRTtZQUM1QyxrQ0FBa0M7WUFDbEMsT0FBTyxJQUFJLENBQUMsT0FBTyxDQUFDLENBQUM7UUFDdkIsQ0FBQyxDQUFDO1FBQ0YsTUFBTSxPQUFPLEdBQUcsSUFBSSxVQUFVLENBQUM7WUFDN0IsT0FBTztZQUNQLE9BQU87WUFDUCxlQUFlLEVBQUUsSUFBSSxDQUFDLFNBQVMsQ0FBQyxlQUFlO1NBQ2hELENBQUMsQ0FBQztRQUVILE9BQU8sQ0FBQyxLQUFLLENBQUMsSUFBSSxHQUFHLHFFQUFjLENBQUM7UUFDcEMsTUFBTSxNQUFNLEdBQUcsSUFBSSxtRUFBYyxDQUFDLEVBQUUsT0FBTyxFQUFFLE9BQU8sRUFBRSxDQUFDLENBQUM7UUFDeEQsT0FBTyxNQUFNLENBQUM7SUFDaEIsQ0FBQztDQUdGIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVlZGl0b3Ivc3JjL2ZpbGVlZGl0b3Jsc3BhZGFwdGVyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9maWxlZWRpdG9yL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWVkaXRvci9zcmMvc2VhcmNocHJvdmlkZXIudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVlZGl0b3Ivc3JjL3N5bnRheHN0YXR1cy50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVlZGl0b3Ivc3JjL3RhYnNwYWNlc3RhdHVzLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWVkaXRvci9zcmMvdG9jL2ZhY3RvcnkudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVlZGl0b3Ivc3JjL3RvYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWVkaXRvci9zcmMvdG9jL2xhdGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9maWxlZWRpdG9yL3NyYy90b2MvbWFya2Rvd24udHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVlZGl0b3Ivc3JjL3RvYy9weXRob24udHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVlZGl0b3Ivc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZmlsZWVkaXRvci9zcmMvd2lkZ2V0LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSUVkaXRvck1pbWVUeXBlU2VydmljZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHsgQ29kZU1pcnJvckVkaXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVtaXJyb3InO1xuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSwgSURvY3VtZW50V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgRG9jdW1lbnQsXG4gIElBZGFwdGVyT3B0aW9ucyxcbiAgSVZpcnR1YWxQb3NpdGlvbixcbiAgVmlydHVhbERvY3VtZW50LFxuICBXaWRnZXRMU1BBZGFwdGVyXG59IGZyb20gJ0BqdXB5dGVybGFiL2xzcCc7XG5pbXBvcnQgeyBQcm9taXNlRGVsZWdhdGUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5cbmltcG9ydCB7IEZpbGVFZGl0b3IgfSBmcm9tICcuL3dpZGdldCc7XG5cbmV4cG9ydCBpbnRlcmZhY2UgSUZpbGVFZGl0b3JBZGFwdGVyT3B0aW9ucyBleHRlbmRzIElBZGFwdGVyT3B0aW9ucyB7XG4gIC8qKlxuICAgKiBUaGUgZG9jdW1lbnQgcmVnaXN0cnkgaW5zdGFuY2UuXG4gICAqL1xuICBkb2NSZWdpc3RyeTogRG9jdW1lbnRSZWdpc3RyeTtcbn1cblxuZXhwb3J0IGNsYXNzIEZpbGVFZGl0b3JBZGFwdGVyIGV4dGVuZHMgV2lkZ2V0TFNQQWRhcHRlcjxcbiAgSURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+XG4+IHtcbiAgY29uc3RydWN0b3IoXG4gICAgZWRpdG9yV2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4sXG4gICAgb3B0aW9uczogSUZpbGVFZGl0b3JBZGFwdGVyT3B0aW9uc1xuICApIHtcbiAgICBjb25zdCB7IGRvY1JlZ2lzdHJ5LCAuLi5vdGhlcnMgfSA9IG9wdGlvbnM7XG4gICAgc3VwZXIoZWRpdG9yV2lkZ2V0LCBvdGhlcnMpO1xuICAgIHRoaXMuZWRpdG9yID0gZWRpdG9yV2lkZ2V0LmNvbnRlbnQ7XG4gICAgdGhpcy5fZG9jUmVnaXN0cnkgPSBkb2NSZWdpc3RyeTtcblxuICAgIC8vIEVuc3VyZSBlZGl0b3IgdW5pcXVlbmVzc1xuICAgIHRoaXMuX3ZpcnR1YWxFZGl0b3IgPSBPYmplY3QuZnJlZXplKHtcbiAgICAgIGdldEVkaXRvcjogKCkgPT4gdGhpcy5lZGl0b3IuZWRpdG9yLFxuICAgICAgcmVhZHk6ICgpID0+IFByb21pc2UucmVzb2x2ZSh0aGlzLmVkaXRvci5lZGl0b3IpLFxuICAgICAgcmV2ZWFsOiAoKSA9PiBQcm9taXNlLnJlc29sdmUodGhpcy5lZGl0b3IuZWRpdG9yKVxuICAgIH0pO1xuXG4gICAgUHJvbWlzZS5hbGwoW3RoaXMuZWRpdG9yLmNvbnRleHQucmVhZHksIHRoaXMuY29ubmVjdGlvbk1hbmFnZXIucmVhZHldKVxuICAgICAgLnRoZW4oYXN5bmMgKCkgPT4ge1xuICAgICAgICBhd2FpdCB0aGlzLmluaXRPbmNlUmVhZHkoKTtcbiAgICAgICAgdGhpcy5fcmVhZHlEZWxlZ2F0ZS5yZXNvbHZlKCk7XG4gICAgICB9KVxuICAgICAgLmNhdGNoKGNvbnNvbGUuZXJyb3IpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSB3cmFwcGVkIGBGaWxlRWRpdG9yYCB3aWRnZXQuXG4gICAqL1xuICByZWFkb25seSBlZGl0b3I6IEZpbGVFZGl0b3I7XG5cbiAgLyoqXG4gICAqIFByb21pc2UgdGhhdCByZXNvbHZlcyBvbmNlIHRoZSBhZGFwdGVyIGlzIGluaXRpYWxpemVkXG4gICAqL1xuICBnZXQgcmVhZHkoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3JlYWR5RGVsZWdhdGUucHJvbWlzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgY3VycmVudCBwYXRoIG9mIHRoZSBkb2N1bWVudC5cbiAgICovXG4gIGdldCBkb2N1bWVudFBhdGgoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy53aWRnZXQuY29udGV4dC5wYXRoO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgbWltZSB0eXBlIG9mIHRoZSBkb2N1bWVudC5cbiAgICovXG4gIGdldCBtaW1lVHlwZSgpOiBzdHJpbmcge1xuICAgIGNvbnN0IG1pbWVUeXBlRnJvbU1vZGVsID0gdGhpcy5lZGl0b3IubW9kZWwubWltZVR5cGU7XG4gICAgY29uc3QgY29kZU1pcnJvck1pbWVUeXBlOiBzdHJpbmcgPSBBcnJheS5pc0FycmF5KG1pbWVUeXBlRnJvbU1vZGVsKVxuICAgICAgPyBtaW1lVHlwZUZyb21Nb2RlbFswXSA/PyBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlLmRlZmF1bHRNaW1lVHlwZVxuICAgICAgOiBtaW1lVHlwZUZyb21Nb2RlbDtcbiAgICBjb25zdCBjb250ZW50c01vZGVsID0gdGhpcy5lZGl0b3IuY29udGV4dC5jb250ZW50c01vZGVsO1xuXG4gICAgLy8gd2hlbiBNSU1FIHR5cGUgaXMgbm90IGtub3duIGl0IGRlZmF1bHRzIHRvICd0ZXh0L3BsYWluJyxcbiAgICAvLyBzbyBpZiBpdCBpcyBkaWZmZXJlbnQgd2UgY2FuIGFjY2VwdCBpdCBhcyBpdCBpc1xuICAgIGlmIChjb2RlTWlycm9yTWltZVR5cGUgIT0gSUVkaXRvck1pbWVUeXBlU2VydmljZS5kZWZhdWx0TWltZVR5cGUpIHtcbiAgICAgIHJldHVybiBjb2RlTWlycm9yTWltZVR5cGU7XG4gICAgfSBlbHNlIGlmIChjb250ZW50c01vZGVsKSB7XG4gICAgICAvLyBhIHNjcmlwdCB0aGF0IGRvZXMgbm90IGhhdmUgYSBNSU1FIHR5cGUga25vd24gYnkgdGhlIGVkaXRvclxuICAgICAgLy8gKG5vIHN5bnRheCBoaWdobGlnaHQgbW9kZSksIGNhbiBzdGlsbCBiZSBrbm93biBieSB0aGUgZG9jdW1lbnRcbiAgICAgIC8vIHJlZ2lzdHJ5IChhbmQgdGhpcyBpcyBhcmd1YWJseSBlYXNpZXIgdG8gZXh0ZW5kKS5cbiAgICAgIGxldCBmaWxlVHlwZSA9IHRoaXMuX2RvY1JlZ2lzdHJ5LmdldEZpbGVUeXBlRm9yTW9kZWwoY29udGVudHNNb2RlbCk7XG4gICAgICByZXR1cm4gZmlsZVR5cGUubWltZVR5cGVzWzBdO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBcInRleHQvcGxhaW5cIiB0aGlzIGlzXG4gICAgICByZXR1cm4gY29kZU1pcnJvck1pbWVUeXBlO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGZpbGUgZXh0ZW5zaW9uIG9mIHRoZSBkb2N1bWVudC5cbiAgICovXG4gIGdldCBsYW5ndWFnZUZpbGVFeHRlbnNpb24oKTogc3RyaW5nIHtcbiAgICBsZXQgcGFydHMgPSB0aGlzLmRvY3VtZW50UGF0aC5zcGxpdCgnLicpO1xuICAgIHJldHVybiBwYXJ0c1twYXJ0cy5sZW5ndGggLSAxXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIENNIGVkaXRvclxuICAgKi9cbiAgZ2V0IGNlRWRpdG9yKCk6IENvZGVNaXJyb3JFZGl0b3Ige1xuICAgIHJldHVybiB0aGlzLmVkaXRvci5lZGl0b3IgYXMgQ29kZU1pcnJvckVkaXRvcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGFjdGl2YXRlZCBDTSBlZGl0b3IuXG4gICAqL1xuICBnZXQgYWN0aXZlRWRpdG9yKCk6IERvY3VtZW50LklFZGl0b3Ige1xuICAgIHJldHVybiB0aGlzLl92aXJ0dWFsRWRpdG9yO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgaW5uZXIgSFRNTEVsZW1lbnQgb2YgdGhlIGRvY3VtZW50IHdpZGdldC5cbiAgICovXG4gIGdldCB3cmFwcGVyRWxlbWVudCgpOiBIVE1MRWxlbWVudCB7XG4gICAgcmV0dXJuIHRoaXMud2lkZ2V0Lm5vZGU7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGN1cnJlbnQgcGF0aCBvZiB0aGUgZG9jdW1lbnQuXG4gICAqL1xuICBnZXQgcGF0aCgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLndpZGdldC5jb250ZXh0LnBhdGg7XG4gIH1cblxuICAvKipcbiAgICogIEdldCB0aGUgbGlzdCBvZiBDTSBlZGl0b3JzIGluIHRoZSBkb2N1bWVudCwgdGhlcmUgaXMgb25seSBvbmUgZWRpdG9yXG4gICAqIGluIHRoZSBjYXNlIG9mIGZpbGUgZWRpdG9yLlxuICAgKi9cbiAgZ2V0IGVkaXRvcnMoKTogRG9jdW1lbnQuSUNvZGVCbG9ja09wdGlvbnNbXSB7XG4gICAgcmV0dXJuIFtcbiAgICAgIHtcbiAgICAgICAgY2VFZGl0b3I6IHRoaXMuX3ZpcnR1YWxFZGl0b3IsXG4gICAgICAgIHR5cGU6ICdjb2RlJyxcbiAgICAgICAgdmFsdWU6IHRoaXMuZWRpdG9yPy5tb2RlbC5zaGFyZWRNb2RlbC5nZXRTb3VyY2UoKSA/PyAnJ1xuICAgICAgfVxuICAgIF07XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuZWRpdG9yLm1vZGVsLm1pbWVUeXBlQ2hhbmdlZC5kaXNjb25uZWN0KHRoaXMucmVsb2FkQ29ubmVjdGlvbik7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdlbmVyYXRlIHRoZSB2aXJ0dWFsIGRvY3VtZW50IGFzc29jaWF0ZWQgd2l0aCB0aGUgZG9jdW1lbnQuXG4gICAqL1xuICBjcmVhdGVWaXJ0dWFsRG9jdW1lbnQoKTogVmlydHVhbERvY3VtZW50IHtcbiAgICByZXR1cm4gbmV3IFZpcnR1YWxEb2N1bWVudCh7XG4gICAgICBsYW5ndWFnZTogdGhpcy5sYW5ndWFnZSxcbiAgICAgIGZvcmVpZ25Db2RlRXh0cmFjdG9yczogdGhpcy5vcHRpb25zLmZvcmVpZ25Db2RlRXh0cmFjdG9yc01hbmFnZXIsXG4gICAgICBwYXRoOiB0aGlzLmRvY3VtZW50UGF0aCxcbiAgICAgIGZpbGVFeHRlbnNpb246IHRoaXMubGFuZ3VhZ2VGaWxlRXh0ZW5zaW9uLFxuICAgICAgLy8gbm90ZWJvb2tzIGFyZSBjb250aW51b3VzLCBlYWNoIGNlbGwgaXMgZGVwZW5kZW50IG9uIHRoZSBwcmV2aW91cyBvbmVcbiAgICAgIHN0YW5kYWxvbmU6IHRydWUsXG4gICAgICAvLyBub3RlYm9va3MgYXJlIG5vdCBzdXBwb3J0ZWQgYnkgTFNQIHNlcnZlcnNcbiAgICAgIGhhc0xzcFN1cHBvcnRlZEZpbGU6IHRydWVcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGluZGV4IG9mIGVkaXRvciBmcm9tIHRoZSBjdXJzb3IgcG9zaXRpb24gaW4gdGhlIHZpcnR1YWxcbiAgICogZG9jdW1lbnQuIFNpbmNlIHRoZXJlIGlzIG9ubHkgb25lIGVkaXRvciwgdGhpcyBtZXRob2QgYWx3YXlzIHJldHVyblxuICAgKiAwXG4gICAqIEBkZXByZWNhdGVkIFRoaXMgaXMgZXJyb3ItcHJvbmUgYW5kIHdpbGwgYmUgcmVtb3ZlZCBpbiBKdXB5dGVyTGFiIDUuMCwgdXNlIGBnZXRFZGl0b3JJbmRleCgpYCB3aXRoIGB2aXJ0dWFsRG9jdW1lbnQuZ2V0RWRpdG9yQXRWaXJ0dWFsTGluZShwb3NpdGlvbilgIGluc3RlYWQuXG4gICAqXG4gICAqIEBwYXJhbSBwb3NpdGlvbiAtIHRoZSBwb3NpdGlvbiBvZiBjdXJzb3IgaW4gdGhlIHZpcnR1YWwgZG9jdW1lbnQuXG4gICAqIEByZXR1cm4gIHtudW1iZXJ9IC0gaW5kZXggb2YgdGhlIHZpcnR1YWwgZWRpdG9yXG4gICAqL1xuICBnZXRFZGl0b3JJbmRleEF0KHBvc2l0aW9uOiBJVmlydHVhbFBvc2l0aW9uKTogbnVtYmVyIHtcbiAgICByZXR1cm4gMDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGluZGV4IG9mIGlucHV0IGVkaXRvclxuICAgKlxuICAgKiBAcGFyYW0gY2VFZGl0b3IgLSBpbnN0YW5jZSBvZiB0aGUgY29kZSBlZGl0b3JcbiAgICovXG4gIGdldEVkaXRvckluZGV4KGNlRWRpdG9yOiBEb2N1bWVudC5JRWRpdG9yKTogbnVtYmVyIHtcbiAgICByZXR1cm4gMDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHdyYXBwZXIgb2YgaW5wdXQgZWRpdG9yLlxuICAgKlxuICAgKiBAcGFyYW0gY2VFZGl0b3JcbiAgICogQHJldHVybiAge0hUTUxFbGVtZW50fVxuICAgKi9cbiAgZ2V0RWRpdG9yV3JhcHBlcihjZUVkaXRvcjogRG9jdW1lbnQuSUVkaXRvcik6IEhUTUxFbGVtZW50IHtcbiAgICByZXR1cm4gdGhpcy53cmFwcGVyRWxlbWVudDtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbml0aWFsaXphdGlvbiBmdW5jdGlvbiBjYWxsZWQgb25jZSB0aGUgZWRpdG9yIGFuZCB0aGUgTFNQIGNvbm5lY3Rpb25cbiAgICogbWFuYWdlciBpcyByZWFkeS4gVGhpcyBmdW5jdGlvbiB3aWxsIGNyZWF0ZSB0aGUgdmlydHVhbCBkb2N1bWVudCBhbmRcbiAgICogY29ubmVjdCB2YXJpb3VzIHNpZ25hbHMuXG4gICAqL1xuICBwcm90ZWN0ZWQgYXN5bmMgaW5pdE9uY2VSZWFkeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0aGlzLmluaXRWaXJ0dWFsKCk7XG5cbiAgICAvLyBjb25uZWN0IHRoZSBkb2N1bWVudCwgYnV0IGRvIG5vdCBvcGVuIGl0IGFzIHRoZSBhZGFwdGVyIHdpbGwgaGFuZGxlIHRoaXNcbiAgICAvLyBhZnRlciByZWdpc3RlcmluZyBhbGwgZmVhdHVyZXNcbiAgICBhd2FpdCB0aGlzLmNvbm5lY3REb2N1bWVudCh0aGlzLnZpcnR1YWxEb2N1bWVudCEsIGZhbHNlKTtcblxuICAgIHRoaXMuZWRpdG9yLm1vZGVsLm1pbWVUeXBlQ2hhbmdlZC5jb25uZWN0KHRoaXMucmVsb2FkQ29ubmVjdGlvbiwgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRvY3VtZW50IHJlZ2lzdHJ5IGluc3RhbmNlLlxuICAgKi9cbiAgcHJpdmF0ZSByZWFkb25seSBfZG9jUmVnaXN0cnk6IERvY3VtZW50UmVnaXN0cnk7XG4gIHByaXZhdGUgcmVhZG9ubHkgX3ZpcnR1YWxFZGl0b3I6IERvY3VtZW50LklFZGl0b3I7XG4gIHByaXZhdGUgX3JlYWR5RGVsZWdhdGUgPSBuZXcgUHJvbWlzZURlbGVnYXRlPHZvaWQ+KCk7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBmaWxlZWRpdG9yXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9maWxlZWRpdG9ybHNwYWRhcHRlcic7XG5leHBvcnQgKiBmcm9tICcuL3NlYXJjaHByb3ZpZGVyJztcbmV4cG9ydCAqIGZyb20gJy4vc3ludGF4c3RhdHVzJztcbmV4cG9ydCAqIGZyb20gJy4vdGFic3BhY2VzdGF0dXMnO1xuZXhwb3J0ICogZnJvbSAnLi90b2MnO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuZXhwb3J0ICogZnJvbSAnLi93aWRnZXQnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBNYWluQXJlYVdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IENvZGVNaXJyb3JFZGl0b3IsIEVkaXRvclNlYXJjaFByb3ZpZGVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZW1pcnJvcic7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQge1xuICBJRmlsdGVycyxcbiAgSVJlcGxhY2VPcHRpb25zU3VwcG9ydCxcbiAgSVNlYXJjaFByb3ZpZGVyXG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3VtZW50c2VhcmNoJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IEZpbGVFZGl0b3IgfSBmcm9tICcuL3dpZGdldCc7XG5cbi8qKlxuICogSGVscGVyIHR5cGVcbiAqL1xuZXhwb3J0IHR5cGUgRmlsZUVkaXRvclBhbmVsID0gTWFpbkFyZWFXaWRnZXQ8RmlsZUVkaXRvcj47XG5cbi8qKlxuICogRmlsZSBlZGl0b3Igc2VhcmNoIHByb3ZpZGVyXG4gKi9cbmV4cG9ydCBjbGFzcyBGaWxlRWRpdG9yU2VhcmNoUHJvdmlkZXJcbiAgZXh0ZW5kcyBFZGl0b3JTZWFyY2hQcm92aWRlcjxDb2RlRWRpdG9yLklNb2RlbD5cbiAgaW1wbGVtZW50cyBJU2VhcmNoUHJvdmlkZXJcbntcbiAgLyoqXG4gICAqIENvbnN0cnVjdG9yXG4gICAqIEBwYXJhbSB3aWRnZXQgRmlsZSBlZGl0b3IgcGFuZWxcbiAgICovXG4gIGNvbnN0cnVjdG9yKHByb3RlY3RlZCB3aWRnZXQ6IEZpbGVFZGl0b3JQYW5lbCkge1xuICAgIHN1cGVyKCk7XG4gIH1cblxuICBnZXQgaXNSZWFkT25seSgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5lZGl0b3IuZ2V0T3B0aW9uKCdyZWFkT25seScpIGFzIGJvb2xlYW47XG4gIH1cblxuICAvKipcbiAgICogU3VwcG9ydCBmb3Igb3B0aW9ucyBhZGp1c3RpbmcgcmVwbGFjZW1lbnQgYmVoYXZpb3IuXG4gICAqL1xuICBnZXQgcmVwbGFjZU9wdGlvbnNTdXBwb3J0KCk6IElSZXBsYWNlT3B0aW9uc1N1cHBvcnQge1xuICAgIHJldHVybiB7XG4gICAgICBwcmVzZXJ2ZUNhc2U6IHRydWVcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIFRleHQgZWRpdG9yXG4gICAqL1xuICBnZXQgZWRpdG9yKCkge1xuICAgIHJldHVybiB0aGlzLndpZGdldC5jb250ZW50LmVkaXRvciBhcyBDb2RlTWlycm9yRWRpdG9yO1xuICB9XG5cbiAgLyoqXG4gICAqIEVkaXRvciBjb250ZW50IG1vZGVsXG4gICAqL1xuICBnZXQgbW9kZWwoKTogQ29kZUVkaXRvci5JTW9kZWwge1xuICAgIHJldHVybiB0aGlzLndpZGdldC5jb250ZW50Lm1vZGVsO1xuICB9XG5cbiAgYXN5bmMgc3RhcnRRdWVyeShcbiAgICBxdWVyeTogUmVnRXhwLFxuICAgIGZpbHRlcnM6IElGaWx0ZXJzIHwgdW5kZWZpbmVkXG4gICk6IFByb21pc2U8dm9pZD4ge1xuICAgIGF3YWl0IHN1cGVyLnN0YXJ0UXVlcnkocXVlcnksIGZpbHRlcnMpO1xuICAgIGF3YWl0IHRoaXMuaGlnaGxpZ2h0TmV4dCh0cnVlLCB7XG4gICAgICBmcm9tOiAnc2VsZWN0aW9uLXN0YXJ0JyxcbiAgICAgIHNjcm9sbDogZmFsc2UsXG4gICAgICBzZWxlY3Q6IGZhbHNlXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogSW5zdGFudGlhdGUgYSBzZWFyY2ggcHJvdmlkZXIgZm9yIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIHdpZGdldCBwcm92aWRlZCBpcyBhbHdheXMgY2hlY2tlZCB1c2luZyBgaXNBcHBsaWNhYmxlYCBiZWZvcmUgY2FsbGluZ1xuICAgKiB0aGlzIGZhY3RvcnkuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgVGhlIHdpZGdldCB0byBzZWFyY2ggb25cbiAgICogQHBhcmFtIHRyYW5zbGF0b3IgW29wdGlvbmFsXSBUaGUgdHJhbnNsYXRvciBvYmplY3RcbiAgICpcbiAgICogQHJldHVybnMgVGhlIHNlYXJjaCBwcm92aWRlciBvbiB0aGUgd2lkZ2V0XG4gICAqL1xuICBzdGF0aWMgY3JlYXRlTmV3KFxuICAgIHdpZGdldDogRmlsZUVkaXRvclBhbmVsLFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiBJU2VhcmNoUHJvdmlkZXIge1xuICAgIHJldHVybiBuZXcgRmlsZUVkaXRvclNlYXJjaFByb3ZpZGVyKHdpZGdldCk7XG4gIH1cblxuICAvKipcbiAgICogUmVwb3J0IHdoZXRoZXIgb3Igbm90IHRoaXMgcHJvdmlkZXIgaGFzIHRoZSBhYmlsaXR5IHRvIHNlYXJjaCBvbiB0aGUgZ2l2ZW4gb2JqZWN0XG4gICAqL1xuICBzdGF0aWMgaXNBcHBsaWNhYmxlKGRvbWFpbjogV2lkZ2V0KTogZG9tYWluIGlzIEZpbGVFZGl0b3JQYW5lbCB7XG4gICAgcmV0dXJuIChcbiAgICAgIGRvbWFpbiBpbnN0YW5jZW9mIE1haW5BcmVhV2lkZ2V0ICYmXG4gICAgICBkb21haW4uY29udGVudCBpbnN0YW5jZW9mIEZpbGVFZGl0b3IgJiZcbiAgICAgIGRvbWFpbi5jb250ZW50LmVkaXRvciBpbnN0YW5jZW9mIENvZGVNaXJyb3JFZGl0b3JcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpbml0aWFsIHF1ZXJ5IHZhbHVlIGlmIGFwcGxpY2FibGUgc28gdGhhdCBpdCBjYW4gYmUgZW50ZXJlZFxuICAgKiBpbnRvIHRoZSBzZWFyY2ggYm94IGFzIGFuIGluaXRpYWwgcXVlcnlcbiAgICpcbiAgICogQHJldHVybnMgSW5pdGlhbCB2YWx1ZSB1c2VkIHRvIHBvcHVsYXRlIHRoZSBzZWFyY2ggYm94LlxuICAgKi9cbiAgZ2V0SW5pdGlhbFF1ZXJ5KCk6IHN0cmluZyB7XG4gICAgY29uc3QgY20gPSB0aGlzLmVkaXRvciBhcyBDb2RlTWlycm9yRWRpdG9yO1xuICAgIGNvbnN0IHNlbGVjdGlvbiA9IGNtLnN0YXRlLnNsaWNlRG9jKFxuICAgICAgY20uc3RhdGUuc2VsZWN0aW9uLm1haW4uZnJvbSxcbiAgICAgIGNtLnN0YXRlLnNlbGVjdGlvbi5tYWluLnRvXG4gICAgKTtcbiAgICByZXR1cm4gc2VsZWN0aW9uO1xuICB9XG59XG4iLCIvKlxuICogQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4gKiBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuICovXG5cbmltcG9ydCB7IENvZGVFZGl0b3IsIElFZGl0b3JNaW1lVHlwZVNlcnZpY2UgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IElFZGl0b3JMYW5ndWFnZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZW1pcnJvcic7XG5pbXBvcnQgeyBJQ2hhbmdlZEFyZ3MgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgUG9wdXAsIHNob3dQb3B1cCwgVGV4dEl0ZW0gfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgVkRvbU1vZGVsLCBWRG9tUmVuZGVyZXIgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgSlNPTk9iamVjdCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lbnUgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYEVkaXRvclN5bnRheENvbXBvbmVudFN0YXRpY3NgLlxuICovXG5uYW1lc3BhY2UgRWRpdG9yU3ludGF4Q29tcG9uZW50IHtcbiAgLyoqXG4gICAqIFRoZSBwcm9wcyBmb3IgdGhlIGBFZGl0b3JTeW50YXhDb21wb25lbnRgLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IENvZGVNaXJyb3IgbGFuZ3VhZ2UgZm9yIGFuIGVkaXRvci5cbiAgICAgKi9cbiAgICBsYW5ndWFnZTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0byBleGVjdXRlIG9uIGNsaWNraW5nIHRoZSBjb21wb25lbnQuXG4gICAgICogQnkgZGVmYXVsdCB3ZSBwcm92aWRlIGEgZnVuY3Rpb24gdGhhdCBvcGVucyBhIG1lbnVcbiAgICAgKiBmb3IgQ29kZU1pcnJvciBsYW5ndWFnZSBzZWxlY3Rpb24uXG4gICAgICovXG4gICAgaGFuZGxlQ2xpY2s6ICgpID0+IHZvaWQ7XG4gIH1cbn1cblxuLyoqXG4gKiBBIHB1cmUgZnVuY3Rpb24gdGhhdCByZXR1cm5zIGEgdHN4IGNvbXBvbmVudCBmb3IgYW4gZWRpdG9yIHN5bnRheCBpdGVtLlxuICpcbiAqIEBwYXJhbSBwcm9wczogdGhlIHByb3BzIGZvciB0aGUgY29tcG9uZW50LlxuICpcbiAqIEByZXR1cm5zIGFuIGVkaXRvciBzeW50YXggY29tcG9uZW50LlxuICovXG5mdW5jdGlvbiBFZGl0b3JTeW50YXhDb21wb25lbnQoXG4gIHByb3BzOiBFZGl0b3JTeW50YXhDb21wb25lbnQuSVByb3BzXG4pOiBSZWFjdC5SZWFjdEVsZW1lbnQ8RWRpdG9yU3ludGF4Q29tcG9uZW50LklQcm9wcz4ge1xuICByZXR1cm4gPFRleHRJdGVtIHNvdXJjZT17cHJvcHMubGFuZ3VhZ2V9IG9uQ2xpY2s9e3Byb3BzLmhhbmRsZUNsaWNrfSAvPjtcbn1cblxuLyoqXG4gKiBTdGF0dXNCYXIgaXRlbSB0byBjaGFuZ2UgdGhlIGxhbmd1YWdlIHN5bnRheCBoaWdobGlnaHRpbmcgb2YgdGhlIGZpbGUgZWRpdG9yLlxuICovXG5leHBvcnQgY2xhc3MgRWRpdG9yU3ludGF4U3RhdHVzIGV4dGVuZHMgVkRvbVJlbmRlcmVyPEVkaXRvclN5bnRheFN0YXR1cy5Nb2RlbD4ge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IFZEb21SZW5kZXJlciBmb3IgdGhlIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogRWRpdG9yU3ludGF4U3RhdHVzLklPcHRpb25zKSB7XG4gICAgc3VwZXIobmV3IEVkaXRvclN5bnRheFN0YXR1cy5Nb2RlbChvcHRpb25zLmxhbmd1YWdlcykpO1xuICAgIHRoaXMuX2NvbW1hbmRzID0gb3B0aW9ucy5jb21tYW5kcztcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgdGhpcy5hZGRDbGFzcygnanAtbW9kLWhpZ2hsaWdodGVkJyk7XG4gICAgdGhpcy50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ0NoYW5nZSB0ZXh0IGVkaXRvciBzeW50YXggaGlnaGxpZ2h0aW5nJyk7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIHRoZSBzdGF0dXMgaXRlbS5cbiAgICovXG4gIHJlbmRlcigpOiBKU1guRWxlbWVudCB8IG51bGwge1xuICAgIGlmICghdGhpcy5tb2RlbCkge1xuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuICAgIHJldHVybiAoXG4gICAgICA8RWRpdG9yU3ludGF4Q29tcG9uZW50XG4gICAgICAgIGxhbmd1YWdlPXt0aGlzLm1vZGVsLmxhbmd1YWdlfVxuICAgICAgICBoYW5kbGVDbGljaz17dGhpcy5faGFuZGxlQ2xpY2t9XG4gICAgICAvPlxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbWVudSBmb3Igc2VsZWN0aW5nIHRoZSBsYW5ndWFnZSBvZiB0aGUgZWRpdG9yLlxuICAgKi9cbiAgcHJpdmF0ZSBfaGFuZGxlQ2xpY2sgPSAoKSA9PiB7XG4gICAgY29uc3QgbGFuZ3VhZ2VNZW51ID0gbmV3IE1lbnUoeyBjb21tYW5kczogdGhpcy5fY29tbWFuZHMgfSk7XG4gICAgY29uc3QgY29tbWFuZCA9ICdmaWxlZWRpdG9yOmNoYW5nZS1sYW5ndWFnZSc7XG4gICAgaWYgKHRoaXMuX3BvcHVwKSB7XG4gICAgICB0aGlzLl9wb3B1cC5kaXNwb3NlKCk7XG4gICAgfVxuICAgIHRoaXMubW9kZWwubGFuZ3VhZ2VzXG4gICAgICAuZ2V0TGFuZ3VhZ2VzKClcbiAgICAgIC5zb3J0KChhLCBiKSA9PiB7XG4gICAgICAgIGNvbnN0IGFOYW1lID0gYS5kaXNwbGF5TmFtZSA/PyBhLm5hbWU7XG4gICAgICAgIGNvbnN0IGJOYW1lID0gYi5kaXNwbGF5TmFtZSA/PyBiLm5hbWU7XG4gICAgICAgIHJldHVybiBhTmFtZS5sb2NhbGVDb21wYXJlKGJOYW1lKTtcbiAgICAgIH0pXG4gICAgICAuZm9yRWFjaChzcGVjID0+IHtcbiAgICAgICAgaWYgKHNwZWMubmFtZS50b0xvd2VyQ2FzZSgpLmluZGV4T2YoJ2JyYWluZicpID09PSAwKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgYXJnczogSlNPTk9iamVjdCA9IHtcbiAgICAgICAgICBuYW1lOiBzcGVjLm5hbWUsXG4gICAgICAgICAgZGlzcGxheU5hbWU6IHNwZWMuZGlzcGxheU5hbWUgPz8gc3BlYy5uYW1lXG4gICAgICAgIH07XG5cbiAgICAgICAgbGFuZ3VhZ2VNZW51LmFkZEl0ZW0oe1xuICAgICAgICAgIGNvbW1hbmQsXG4gICAgICAgICAgYXJnc1xuICAgICAgICB9KTtcbiAgICAgIH0pO1xuICAgIHRoaXMuX3BvcHVwID0gc2hvd1BvcHVwKHtcbiAgICAgIGJvZHk6IGxhbmd1YWdlTWVudSxcbiAgICAgIGFuY2hvcjogdGhpcyxcbiAgICAgIGFsaWduOiAnbGVmdCdcbiAgICB9KTtcbiAgfTtcblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX2NvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnk7XG4gIHByaXZhdGUgX3BvcHVwOiBQb3B1cCB8IG51bGwgPSBudWxsO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBFZGl0b3JTeW50YXggc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBFZGl0b3JTeW50YXhTdGF0dXMge1xuICAvKipcbiAgICogQSBWRG9tTW9kZWwgZm9yIHRoZSBjdXJyZW50IGVkaXRvci9tb2RlIGNvbWJpbmF0aW9uLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIHtcbiAgICBjb25zdHJ1Y3RvcihwdWJsaWMgbGFuZ3VhZ2VzOiBJRWRpdG9yTGFuZ3VhZ2VSZWdpc3RyeSkge1xuICAgICAgc3VwZXIoKTtcbiAgICB9XG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgZWRpdG9yIGxhbmd1YWdlLiBJZiBubyBlZGl0b3IgaXMgcHJlc2VudCxcbiAgICAgKiByZXR1cm5zIHRoZSBlbXB0eSBzdHJpbmcuXG4gICAgICovXG4gICAgZ2V0IGxhbmd1YWdlKCk6IHN0cmluZyB7XG4gICAgICByZXR1cm4gdGhpcy5fbGFuZ3VhZ2U7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgZWRpdG9yIGZvciB0aGUgYXBwbGljYXRpb24gZWRpdG9yIHRyYWNrZXIuXG4gICAgICovXG4gICAgZ2V0IGVkaXRvcigpOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9lZGl0b3I7XG4gICAgfVxuICAgIHNldCBlZGl0b3IoZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsKSB7XG4gICAgICBjb25zdCBvbGRFZGl0b3IgPSB0aGlzLl9lZGl0b3I7XG4gICAgICBpZiAob2xkRWRpdG9yICE9PSBudWxsKSB7XG4gICAgICAgIG9sZEVkaXRvci5tb2RlbC5taW1lVHlwZUNoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9vbk1JTUVUeXBlQ2hhbmdlKTtcbiAgICAgIH1cbiAgICAgIGNvbnN0IG9sZExhbmd1YWdlID0gdGhpcy5fbGFuZ3VhZ2U7XG4gICAgICB0aGlzLl9lZGl0b3IgPSBlZGl0b3I7XG4gICAgICBpZiAodGhpcy5fZWRpdG9yID09PSBudWxsKSB7XG4gICAgICAgIHRoaXMuX2xhbmd1YWdlID0gJyc7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjb25zdCBzcGVjID0gdGhpcy5sYW5ndWFnZXMuZmluZEJ5TUlNRSh0aGlzLl9lZGl0b3IubW9kZWwubWltZVR5cGUpO1xuICAgICAgICB0aGlzLl9sYW5ndWFnZSA9IHNwZWM/Lm5hbWUgPz8gSUVkaXRvck1pbWVUeXBlU2VydmljZS5kZWZhdWx0TWltZVR5cGU7XG5cbiAgICAgICAgdGhpcy5fZWRpdG9yLm1vZGVsLm1pbWVUeXBlQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uTUlNRVR5cGVDaGFuZ2UpO1xuICAgICAgfVxuXG4gICAgICB0aGlzLl90cmlnZ2VyQ2hhbmdlKG9sZExhbmd1YWdlLCB0aGlzLl9sYW5ndWFnZSk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogSWYgdGhlIGVkaXRvciBtb2RlIGNoYW5nZXMsIHVwZGF0ZSB0aGUgbW9kZWwuXG4gICAgICovXG4gICAgcHJpdmF0ZSBfb25NSU1FVHlwZUNoYW5nZSA9IChcbiAgICAgIG1vZGU6IENvZGVFZGl0b3IuSU1vZGVsLFxuICAgICAgY2hhbmdlOiBJQ2hhbmdlZEFyZ3M8c3RyaW5nPlxuICAgICkgPT4ge1xuICAgICAgY29uc3Qgb2xkTGFuZ3VhZ2UgPSB0aGlzLl9sYW5ndWFnZTtcbiAgICAgIGNvbnN0IHNwZWMgPSB0aGlzLmxhbmd1YWdlcy5maW5kQnlNSU1FKGNoYW5nZS5uZXdWYWx1ZSk7XG4gICAgICB0aGlzLl9sYW5ndWFnZSA9IHNwZWM/Lm5hbWUgPz8gSUVkaXRvck1pbWVUeXBlU2VydmljZS5kZWZhdWx0TWltZVR5cGU7XG5cbiAgICAgIHRoaXMuX3RyaWdnZXJDaGFuZ2Uob2xkTGFuZ3VhZ2UsIHRoaXMuX2xhbmd1YWdlKTtcbiAgICB9O1xuXG4gICAgLyoqXG4gICAgICogVHJpZ2dlciBhIHJlcmVuZGVyIG9mIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICBwcml2YXRlIF90cmlnZ2VyQ2hhbmdlKG9sZFN0YXRlOiBzdHJpbmcsIG5ld1N0YXRlOiBzdHJpbmcpIHtcbiAgICAgIGlmIChvbGRTdGF0ZSAhPT0gbmV3U3RhdGUpIHtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgfVxuICAgIH1cblxuICAgIHByaXZhdGUgX2xhbmd1YWdlOiBzdHJpbmcgPSAnJztcbiAgICBwcml2YXRlIF9lZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvciB8IG51bGwgPSBudWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIE9wdGlvbnMgZm9yIHRoZSBFZGl0b3JTeW50YXggc3RhdHVzIGl0ZW0uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gY29tbWFuZCByZWdpc3RyeS5cbiAgICAgKi9cbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogRWRpdG9yIGxhbmd1YWdlcy5cbiAgICAgKi9cbiAgICBsYW5ndWFnZXM6IElFZGl0b3JMYW5ndWFnZVJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFBvcHVwLCBzaG93UG9wdXAsIFRleHRJdGVtIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFZEb21Nb2RlbCwgVkRvbVJlbmRlcmVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBNZW51IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFRhYlNwYWNlQ29tcG9uZW50IHN0YXRpY3MuXG4gKi9cbm5hbWVzcGFjZSBUYWJTcGFjZUNvbXBvbmVudCB7XG4gIC8qKlxuICAgKiBUaGUgcHJvcHMgZm9yIFRhYlNwYWNlQ29tcG9uZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIFRoZSBudW1iZXIgb2Ygc3BhY2VzIGZvciBpbmRlbnRhdGlvbi5cbiAgICAgKlxuICAgICAqIGBudWxsYCBtZWFucyB1c2UgdGFiIGNoYXJhY3RlciBmb3IgaW5kZW50YXRpb24uXG4gICAgICovXG4gICAgdGFiU3BhY2U6IG51bWJlciB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG5cbiAgICAvKipcbiAgICAgKiBBIGNsaWNrIGhhbmRsZXIgZm9yIHRoZSBUYWJTcGFjZSBjb21wb25lbnQuIEJ5IGRlZmF1bHRcbiAgICAgKiBvcGVucyBhIG1lbnUgYWxsb3dpbmcgdGhlIHVzZXIgdG8gc2VsZWN0IHRhYnMgdnMgc3BhY2VzLlxuICAgICAqL1xuICAgIGhhbmRsZUNsaWNrOiAoKSA9PiB2b2lkO1xuICB9XG59XG5cbi8qKlxuICogQSBwdXJlIGZ1bmN0aW9uYWwgY29tcG9uZW50IGZvciByZW5kZXJpbmcgdGhlIFRhYlNwYWNlIHN0YXR1cy5cbiAqL1xuZnVuY3Rpb24gVGFiU3BhY2VDb21wb25lbnQoXG4gIHByb3BzOiBUYWJTcGFjZUNvbXBvbmVudC5JUHJvcHNcbik6IFJlYWN0LlJlYWN0RWxlbWVudDxUYWJTcGFjZUNvbXBvbmVudC5JUHJvcHM+IHtcbiAgY29uc3QgdHJhbnNsYXRvciA9IHByb3BzLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IGRlc2NyaXB0aW9uID1cbiAgICB0eXBlb2YgcHJvcHMudGFiU3BhY2UgPT09ICdudW1iZXInXG4gICAgICA/IHRyYW5zLl9fKCdTcGFjZXMnKVxuICAgICAgOiB0cmFucy5fXygnVGFiIEluZGVudCcpO1xuICByZXR1cm4gKFxuICAgIDxUZXh0SXRlbVxuICAgICAgb25DbGljaz17cHJvcHMuaGFuZGxlQ2xpY2t9XG4gICAgICBzb3VyY2U9e1xuICAgICAgICB0eXBlb2YgcHJvcHMudGFiU3BhY2UgPT09ICdudW1iZXInXG4gICAgICAgICAgPyBgJHtkZXNjcmlwdGlvbn06ICR7cHJvcHMudGFiU3BhY2V9YFxuICAgICAgICAgIDogZGVzY3JpcHRpb25cbiAgICAgIH1cbiAgICAgIHRpdGxlPXt0cmFucy5fXygnQ2hhbmdlIHRoZSBpbmRlbnRhdGlvbuKApicpfVxuICAgIC8+XG4gICk7XG59XG5cbi8qKlxuICogQSBWRG9tUmVuZGVyZXIgZm9yIGEgdGFicyB2cy4gc3BhY2VzIHN0YXR1cyBpdGVtLlxuICovXG5leHBvcnQgY2xhc3MgVGFiU3BhY2VTdGF0dXMgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8VGFiU3BhY2VTdGF0dXMuTW9kZWw+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB0YWIvc3BhY2Ugc3RhdHVzIGl0ZW0uXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBUYWJTcGFjZVN0YXR1cy5JT3B0aW9ucykge1xuICAgIHN1cGVyKG5ldyBUYWJTcGFjZVN0YXR1cy5Nb2RlbCgpKTtcbiAgICB0aGlzLl9tZW51ID0gb3B0aW9ucy5tZW51O1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1tb2QtaGlnaGxpZ2h0ZWQnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgdGhlIFRhYlNwYWNlIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgcmVuZGVyKCk6IFJlYWN0LlJlYWN0RWxlbWVudDxUYWJTcGFjZUNvbXBvbmVudC5JUHJvcHM+IHwgbnVsbCB7XG4gICAgaWYgKCF0aGlzLm1vZGVsPy5pbmRlbnRVbml0KSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc3QgdGFiU3BhY2UgPVxuICAgICAgICB0aGlzLm1vZGVsLmluZGVudFVuaXQgPT09ICdUYWInXG4gICAgICAgICAgPyBudWxsXG4gICAgICAgICAgOiBwYXJzZUludCh0aGlzLm1vZGVsLmluZGVudFVuaXQsIDEwKTtcbiAgICAgIHJldHVybiAoXG4gICAgICAgIDxUYWJTcGFjZUNvbXBvbmVudFxuICAgICAgICAgIHRhYlNwYWNlPXt0YWJTcGFjZX1cbiAgICAgICAgICBoYW5kbGVDbGljaz17KCkgPT4gdGhpcy5faGFuZGxlQ2xpY2soKX1cbiAgICAgICAgICB0cmFuc2xhdG9yPXt0aGlzLnRyYW5zbGF0b3J9XG4gICAgICAgIC8+XG4gICAgICApO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjbGljayBvbiB0aGUgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICBwcml2YXRlIF9oYW5kbGVDbGljaygpOiB2b2lkIHtcbiAgICBjb25zdCBtZW51ID0gdGhpcy5fbWVudTtcbiAgICBpZiAodGhpcy5fcG9wdXApIHtcbiAgICAgIHRoaXMuX3BvcHVwLmRpc3Bvc2UoKTtcbiAgICB9XG5cbiAgICBtZW51LmFib3V0VG9DbG9zZS5jb25uZWN0KHRoaXMuX21lbnVDbG9zZWQsIHRoaXMpO1xuXG4gICAgdGhpcy5fcG9wdXAgPSBzaG93UG9wdXAoe1xuICAgICAgYm9keTogbWVudSxcbiAgICAgIGFuY2hvcjogdGhpcyxcbiAgICAgIGFsaWduOiAncmlnaHQnXG4gICAgfSk7XG4gICAgLy8gVXBkYXRlIHRoZSBtZW51IGl0ZW1zXG4gICAgbWVudS51cGRhdGUoKTtcbiAgfVxuXG4gIHByaXZhdGUgX21lbnVDbG9zZWQoKTogdm9pZCB7XG4gICAgdGhpcy5yZW1vdmVDbGFzcygnanAtbW9kLWNsaWNrZWQnKTtcbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfbWVudTogTWVudTtcbiAgcHJpdmF0ZSBfcG9wdXA6IFBvcHVwIHwgbnVsbCA9IG51bGw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIFRhYlNwYWNlIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgVGFiU3BhY2VTdGF0dXMge1xuICAvKipcbiAgICogQSBWRG9tTW9kZWwgZm9yIHRoZSBUYWJTcGFjZSBzdGF0dXMgaXRlbS5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBNb2RlbCBleHRlbmRzIFZEb21Nb2RlbCB7XG4gICAgLyoqXG4gICAgICogQ29kZSBlZGl0b3IgaW5kZW50YXRpb24gdW5pdFxuICAgICAqL1xuICAgIGdldCBpbmRlbnRVbml0KCk6IHN0cmluZyB8IG51bGwge1xuICAgICAgcmV0dXJuIHRoaXMuX2luZGVudFVuaXQ7XG4gICAgfVxuICAgIHNldCBpbmRlbnRVbml0KHY6IHN0cmluZyB8IG51bGwpIHtcbiAgICAgIGlmICh2ICE9PSB0aGlzLl9pbmRlbnRVbml0KSB7XG4gICAgICAgIHRoaXMuX2luZGVudFVuaXQgPSB2O1xuICAgICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KCk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfaW5kZW50VW5pdDogc3RyaW5nIHwgbnVsbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBjcmVhdGluZyBhIFRhYlNwYWNlIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogQSBtZW51IHRvIG9wZW4gd2hlbiBjbGlja2luZyBvbiB0aGUgc3RhdHVzIGl0ZW0uIFRoaXMgc2hvdWxkIGFsbG93XG4gICAgICogdGhlIHVzZXIgdG8gbWFrZSBhIGRpZmZlcmVudCBzZWxlY3Rpb24gYWJvdXQgdGFicy9zcGFjZXMuXG4gICAgICovXG4gICAgbWVudTogTWVudTtcblxuICAgIC8qKlxuICAgICAqIExhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IERvY3VtZW50UmVnaXN0cnksIElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIFRhYmxlT2ZDb250ZW50cyxcbiAgVGFibGVPZkNvbnRlbnRzRmFjdG9yeSxcbiAgVGFibGVPZkNvbnRlbnRzTW9kZWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdG9jJztcbmltcG9ydCB7IEZpbGVFZGl0b3IgfSBmcm9tICcuLi93aWRnZXQnO1xuXG4vKipcbiAqIEludGVyZmFjZSBkZXNjcmliaW5nIGEgZmlsZSBlZGl0b3IgaGVhZGluZy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRWRpdG9ySGVhZGluZyBleHRlbmRzIFRhYmxlT2ZDb250ZW50cy5JSGVhZGluZyB7XG4gIC8qKlxuICAgKiBIZWFkaW5nIGxpbmUgbnVtYmVyLlxuICAgKi9cbiAgbGluZTogbnVtYmVyO1xufVxuXG4vKipcbiAqIEJhc2UgdGFibGUgb2YgY29udGVudHMgbW9kZWwgZmFjdG9yeSBmb3IgZmlsZSBlZGl0b3JcbiAqL1xuZXhwb3J0IGFic3RyYWN0IGNsYXNzIEVkaXRvclRhYmxlT2ZDb250ZW50c0ZhY3RvcnkgZXh0ZW5kcyBUYWJsZU9mQ29udGVudHNGYWN0b3J5PFxuICBJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4sXG4gIElFZGl0b3JIZWFkaW5nXG4+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCBmb3IgdGhlIHdpZGdldFxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gd2lkZ2V0XG4gICAqIEBwYXJhbSBjb25maWd1cmF0aW9uIC0gVGFibGUgb2YgY29udGVudHMgY29uZmlndXJhdGlvblxuICAgKiBAcmV0dXJucyBUaGUgdGFibGUgb2YgY29udGVudHMgbW9kZWxcbiAgICovXG4gIGNyZWF0ZU5ldyhcbiAgICB3aWRnZXQ6IElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yLCBEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD4sXG4gICAgY29uZmlndXJhdGlvbj86IFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnXG4gICk6IFRhYmxlT2ZDb250ZW50c01vZGVsPFxuICAgIElFZGl0b3JIZWFkaW5nLFxuICAgIElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yLCBEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD5cbiAgPiB7XG4gICAgY29uc3QgbW9kZWwgPSBzdXBlci5jcmVhdGVOZXcod2lkZ2V0LCBjb25maWd1cmF0aW9uKTtcblxuICAgIGNvbnN0IG9uQWN0aXZlSGVhZGluZ0NoYW5nZWQgPSAoXG4gICAgICBtb2RlbDogVGFibGVPZkNvbnRlbnRzTW9kZWw8XG4gICAgICAgIElFZGl0b3JIZWFkaW5nLFxuICAgICAgICBJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvciwgRG9jdW1lbnRSZWdpc3RyeS5JTW9kZWw+XG4gICAgICA+LFxuICAgICAgaGVhZGluZzogSUVkaXRvckhlYWRpbmcgfCBudWxsXG4gICAgKSA9PiB7XG4gICAgICBpZiAoaGVhZGluZykge1xuICAgICAgICB3aWRnZXQuY29udGVudC5lZGl0b3Iuc2V0Q3Vyc29yUG9zaXRpb24oe1xuICAgICAgICAgIGxpbmU6IGhlYWRpbmcubGluZSxcbiAgICAgICAgICBjb2x1bW46IDBcbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfTtcblxuICAgIG1vZGVsLmFjdGl2ZUhlYWRpbmdDaGFuZ2VkLmNvbm5lY3Qob25BY3RpdmVIZWFkaW5nQ2hhbmdlZCk7XG4gICAgd2lkZ2V0LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgbW9kZWwuYWN0aXZlSGVhZGluZ0NoYW5nZWQuZGlzY29ubmVjdChvbkFjdGl2ZUhlYWRpbmdDaGFuZ2VkKTtcbiAgICB9KTtcblxuICAgIHJldHVybiBtb2RlbDtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5leHBvcnQgKiBmcm9tICcuL2ZhY3RvcnknO1xuZXhwb3J0ICogZnJvbSAnLi9sYXRleCc7XG5leHBvcnQgKiBmcm9tICcuL21hcmtkb3duJztcbmV4cG9ydCAqIGZyb20gJy4vcHl0aG9uJztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgRG9jdW1lbnRSZWdpc3RyeSwgSURvY3VtZW50V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgVGFibGVPZkNvbnRlbnRzLFxuICBUYWJsZU9mQ29udGVudHNNb2RlbCxcbiAgVGFibGVPZkNvbnRlbnRzVXRpbHNcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdG9jJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBGaWxlRWRpdG9yIH0gZnJvbSAnLi4vd2lkZ2V0JztcbmltcG9ydCB7IEVkaXRvclRhYmxlT2ZDb250ZW50c0ZhY3RvcnksIElFZGl0b3JIZWFkaW5nIH0gZnJvbSAnLi9mYWN0b3J5JztcblxuLyoqXG4gKiBNYXBzIExhVGVYIHNlY3Rpb24gaGVhZGluZ3MgdG8gSFRNTCBoZWFkZXIgbGV2ZWxzLlxuICpcbiAqICMjIE5vdGVzXG4gKlxuICogLSAgIEFzIGBwYXJ0YCBhbmQgYGNoYXB0ZXJgIHNlY3Rpb24gaGVhZGluZ3MgYXBwZWFyIHRvIGJlIGxlc3MgY29tbW9uLCBhc3NpZ24gdGhlbSB0byBoZWFkaW5nIGxldmVsIDEuXG4gKlxuICogQHByaXZhdGVcbiAqL1xuY29uc3QgTEFURVhfTEVWRUxTOiB7IFtsYWJlbDogc3RyaW5nXTogbnVtYmVyIH0gPSB7XG4gIHBhcnQ6IDEsIC8vIE9ubHkgYXZhaWxhYmxlIGZvciByZXBvcnQgYW5kIGJvb2sgY2xhc3Nlc1xuICBjaGFwdGVyOiAxLCAvLyBPbmx5IGF2YWlsYWJsZSBmb3IgcmVwb3J0IGFuZCBib29rIGNsYXNzZXNcbiAgc2VjdGlvbjogMSxcbiAgc3Vic2VjdGlvbjogMixcbiAgc3Vic3Vic2VjdGlvbjogMyxcbiAgcGFyYWdyYXBoOiA0LFxuICBzdWJwYXJhZ3JhcGg6IDVcbn07XG5cbi8qKlxuICogUmVndWxhciBleHByZXNzaW9uIHRvIGNyZWF0ZSB0aGUgb3V0bGluZVxuICovXG5jb25zdCBTRUNUSU9OUyA9IC9eXFxzKlxcXFwoc2VjdGlvbnxzdWJzZWN0aW9ufHN1YnN1YnNlY3Rpb24peyguKyl9LztcblxuLyoqXG4gKiBUYWJsZSBvZiBjb250ZW50IG1vZGVsIGZvciBMYVRlWCBmaWxlcy5cbiAqL1xuZXhwb3J0IGNsYXNzIExhVGVYVGFibGVPZkNvbnRlbnRzTW9kZWwgZXh0ZW5kcyBUYWJsZU9mQ29udGVudHNNb2RlbDxcbiAgSUVkaXRvckhlYWRpbmcsXG4gIElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yLCBEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD5cbj4ge1xuICAvKipcbiAgICogVHlwZSBvZiBkb2N1bWVudCBzdXBwb3J0ZWQgYnkgdGhlIG1vZGVsLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIEEgYGRhdGEtZG9jdW1lbnQtdHlwZWAgYXR0cmlidXRlIHdpdGggdGhpcyB2YWx1ZSB3aWxsIGJlIHNldFxuICAgKiBvbiB0aGUgdHJlZSB2aWV3IGAuanAtVGFibGVPZkNvbnRlbnRzLWNvbnRlbnRbZGF0YS1kb2N1bWVudC10eXBlPVwiLi4uXCJdYFxuICAgKi9cbiAgZ2V0IGRvY3VtZW50VHlwZSgpOiBzdHJpbmcge1xuICAgIHJldHVybiAnbGF0ZXgnO1xuICB9XG5cbiAgLyoqXG4gICAqIExpc3Qgb2YgY29uZmlndXJhdGlvbiBvcHRpb25zIHN1cHBvcnRlZCBieSB0aGUgbW9kZWwuXG4gICAqL1xuICBnZXQgc3VwcG9ydGVkT3B0aW9ucygpOiAoa2V5b2YgVGFibGVPZkNvbnRlbnRzLklDb25maWcpW10ge1xuICAgIHJldHVybiBbJ21heGltYWxEZXB0aCcsICdudW1iZXJIZWFkZXJzJ107XG4gIH1cblxuICAvKipcbiAgICogUHJvZHVjZSB0aGUgaGVhZGluZ3MgZm9yIGEgZG9jdW1lbnQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBsaXN0IG9mIG5ldyBoZWFkaW5ncyBvciBgbnVsbGAgaWYgbm90aGluZyBuZWVkcyB0byBiZSB1cGRhdGVkLlxuICAgKi9cbiAgcHJvdGVjdGVkIGdldEhlYWRpbmdzKCk6IFByb21pc2U8SUVkaXRvckhlYWRpbmdbXSB8IG51bGw+IHtcbiAgICBpZiAoIXRoaXMuaXNBY3RpdmUpIHtcbiAgICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUobnVsbCk7XG4gICAgfVxuXG4gICAgLy8gU3BsaXQgdGhlIHRleHQgaW50byBsaW5lczpcbiAgICBjb25zdCBsaW5lcyA9IHRoaXMud2lkZ2V0LmNvbnRlbnQubW9kZWwuc2hhcmVkTW9kZWxcbiAgICAgIC5nZXRTb3VyY2UoKVxuICAgICAgLnNwbGl0KCdcXG4nKSBhcyBBcnJheTxzdHJpbmc+O1xuXG4gICAgY29uc3QgbGV2ZWxzID0gbmV3IEFycmF5PG51bWJlcj4oKTtcbiAgICBsZXQgcHJldmlvdXNMZXZlbCA9IGxldmVscy5sZW5ndGg7XG4gICAgY29uc3QgaGVhZGluZ3MgPSBuZXcgQXJyYXk8SUVkaXRvckhlYWRpbmc+KCk7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBsaW5lcy5sZW5ndGg7IGkrKykge1xuICAgICAgY29uc3QgbWF0Y2ggPSBsaW5lc1tpXS5tYXRjaChTRUNUSU9OUyk7XG4gICAgICBpZiAobWF0Y2gpIHtcbiAgICAgICAgY29uc3QgbGV2ZWwgPSBMQVRFWF9MRVZFTFNbbWF0Y2hbMV1dO1xuICAgICAgICBpZiAobGV2ZWwgPD0gdGhpcy5jb25maWd1cmF0aW9uLm1heGltYWxEZXB0aCkge1xuICAgICAgICAgIGNvbnN0IHByZWZpeCA9IFRhYmxlT2ZDb250ZW50c1V0aWxzLmdldFByZWZpeChcbiAgICAgICAgICAgIGxldmVsLFxuICAgICAgICAgICAgcHJldmlvdXNMZXZlbCxcbiAgICAgICAgICAgIGxldmVscyxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgLi4udGhpcy5jb25maWd1cmF0aW9uLFxuICAgICAgICAgICAgICAvLyBGb3JjZSBiYXNlIG51bWJlcmluZyBhbmQgbnVtYmVyaW5nIGZpcnN0IGxldmVsXG4gICAgICAgICAgICAgIGJhc2VOdW1iZXJpbmc6IDEsXG4gICAgICAgICAgICAgIG51bWJlcmluZ0gxOiB0cnVlXG4gICAgICAgICAgICB9XG4gICAgICAgICAgKTtcbiAgICAgICAgICBwcmV2aW91c0xldmVsID0gbGV2ZWw7XG5cbiAgICAgICAgICBoZWFkaW5ncy5wdXNoKHtcbiAgICAgICAgICAgIHRleHQ6IG1hdGNoWzJdLFxuICAgICAgICAgICAgcHJlZml4OiBwcmVmaXgsXG4gICAgICAgICAgICBsZXZlbCxcbiAgICAgICAgICAgIGxpbmU6IGlcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKGhlYWRpbmdzKTtcbiAgfVxufVxuXG4vKipcbiAqIFRhYmxlIG9mIGNvbnRlbnQgbW9kZWwgZmFjdG9yeSBmb3IgTGFUZVggZmlsZXMuXG4gKi9cbmV4cG9ydCBjbGFzcyBMYVRlWFRhYmxlT2ZDb250ZW50c0ZhY3RvcnkgZXh0ZW5kcyBFZGl0b3JUYWJsZU9mQ29udGVudHNGYWN0b3J5IHtcbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGZhY3RvcnkgY2FuIGhhbmRsZSB0aGUgd2lkZ2V0IG9yIG5vdC5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCAtIHdpZGdldFxuICAgKiBAcmV0dXJucyBib29sZWFuIGluZGljYXRpbmcgYSBUb0MgY2FuIGJlIGdlbmVyYXRlZFxuICAgKi9cbiAgaXNBcHBsaWNhYmxlKHdpZGdldDogV2lkZ2V0KTogYm9vbGVhbiB7XG4gICAgY29uc3QgaXNBcHBsaWNhYmxlID0gc3VwZXIuaXNBcHBsaWNhYmxlKHdpZGdldCk7XG5cbiAgICBpZiAoaXNBcHBsaWNhYmxlKSB7XG4gICAgICBsZXQgbWltZSA9ICh3aWRnZXQgYXMgYW55KS5jb250ZW50Py5tb2RlbD8ubWltZVR5cGU7XG4gICAgICByZXR1cm4gbWltZSAmJiAobWltZSA9PT0gJ3RleHQveC1sYXRleCcgfHwgbWltZSA9PT0gJ3RleHQveC1zdGV4Jyk7XG4gICAgfVxuICAgIHJldHVybiBmYWxzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgdGFibGUgb2YgY29udGVudHMgbW9kZWwgZm9yIHRoZSB3aWRnZXRcbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCAtIHdpZGdldFxuICAgKiBAcGFyYW0gY29uZmlndXJhdGlvbiAtIFRhYmxlIG9mIGNvbnRlbnRzIGNvbmZpZ3VyYXRpb25cbiAgICogQHJldHVybnMgVGhlIHRhYmxlIG9mIGNvbnRlbnRzIG1vZGVsXG4gICAqL1xuICBwcm90ZWN0ZWQgX2NyZWF0ZU5ldyhcbiAgICB3aWRnZXQ6IElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yLCBEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD4sXG4gICAgY29uZmlndXJhdGlvbj86IFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnXG4gICk6IExhVGVYVGFibGVPZkNvbnRlbnRzTW9kZWwge1xuICAgIHJldHVybiBuZXcgTGFUZVhUYWJsZU9mQ29udGVudHNNb2RlbCh3aWRnZXQsIGNvbmZpZ3VyYXRpb24pO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IERvY3VtZW50UmVnaXN0cnksIElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIFRhYmxlT2ZDb250ZW50cyxcbiAgVGFibGVPZkNvbnRlbnRzTW9kZWwsXG4gIFRhYmxlT2ZDb250ZW50c1V0aWxzXG59IGZyb20gJ0BqdXB5dGVybGFiL3RvYyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgRmlsZUVkaXRvciB9IGZyb20gJy4uL3dpZGdldCc7XG5pbXBvcnQgeyBFZGl0b3JUYWJsZU9mQ29udGVudHNGYWN0b3J5LCBJRWRpdG9ySGVhZGluZyB9IGZyb20gJy4vZmFjdG9yeSc7XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudCBtb2RlbCBmb3IgTWFya2Rvd24gZmlsZXMuXG4gKi9cbmV4cG9ydCBjbGFzcyBNYXJrZG93blRhYmxlT2ZDb250ZW50c01vZGVsIGV4dGVuZHMgVGFibGVPZkNvbnRlbnRzTW9kZWw8XG4gIElFZGl0b3JIZWFkaW5nLFxuICBJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvciwgRG9jdW1lbnRSZWdpc3RyeS5JTW9kZWw+XG4+IHtcbiAgLyoqXG4gICAqIFR5cGUgb2YgZG9jdW1lbnQgc3VwcG9ydGVkIGJ5IHRoZSBtb2RlbC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBBIGBkYXRhLWRvY3VtZW50LXR5cGVgIGF0dHJpYnV0ZSB3aXRoIHRoaXMgdmFsdWUgd2lsbCBiZSBzZXRcbiAgICogb24gdGhlIHRyZWUgdmlldyBgLmpwLVRhYmxlT2ZDb250ZW50cy1jb250ZW50W2RhdGEtZG9jdW1lbnQtdHlwZT1cIi4uLlwiXWBcbiAgICovXG4gIGdldCBkb2N1bWVudFR5cGUoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gJ21hcmtkb3duJztcbiAgfVxuXG4gIC8qKlxuICAgKiBQcm9kdWNlIHRoZSBoZWFkaW5ncyBmb3IgYSBkb2N1bWVudC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGxpc3Qgb2YgbmV3IGhlYWRpbmdzIG9yIGBudWxsYCBpZiBub3RoaW5nIG5lZWRzIHRvIGJlIHVwZGF0ZWQuXG4gICAqL1xuICBwcm90ZWN0ZWQgZ2V0SGVhZGluZ3MoKTogUHJvbWlzZTxJRWRpdG9ySGVhZGluZ1tdIHwgbnVsbD4ge1xuICAgIGlmICghdGhpcy5pc0FjdGl2ZSkge1xuICAgICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShudWxsKTtcbiAgICB9XG5cbiAgICBjb25zdCBjb250ZW50ID0gdGhpcy53aWRnZXQuY29udGVudC5tb2RlbC5zaGFyZWRNb2RlbC5nZXRTb3VyY2UoKTtcblxuICAgIGNvbnN0IGhlYWRpbmdzID0gVGFibGVPZkNvbnRlbnRzVXRpbHMuZmlsdGVySGVhZGluZ3MoXG4gICAgICBUYWJsZU9mQ29udGVudHNVdGlscy5NYXJrZG93bi5nZXRIZWFkaW5ncyhjb250ZW50KSxcbiAgICAgIHtcbiAgICAgICAgLi4udGhpcy5jb25maWd1cmF0aW9uLFxuICAgICAgICAvLyBGb3JjZSByZW1vdmluZyBudW1iZXJpbmcgYXMgdGhleSBjYW5ub3QgYmUgZGlzcGxheWVkXG4gICAgICAgIC8vIGluIHRoZSBkb2N1bWVudFxuICAgICAgICBudW1iZXJIZWFkZXJzOiBmYWxzZVxuICAgICAgfVxuICAgICk7XG4gICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShoZWFkaW5ncyk7XG4gIH1cbn1cblxuLyoqXG4gKiBUYWJsZSBvZiBjb250ZW50IG1vZGVsIGZhY3RvcnkgZm9yIE1hcmtkb3duIGZpbGVzLlxuICovXG5leHBvcnQgY2xhc3MgTWFya2Rvd25UYWJsZU9mQ29udGVudHNGYWN0b3J5IGV4dGVuZHMgRWRpdG9yVGFibGVPZkNvbnRlbnRzRmFjdG9yeSB7XG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBmYWN0b3J5IGNhbiBoYW5kbGUgdGhlIHdpZGdldCBvciBub3QuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgLSB3aWRnZXRcbiAgICogQHJldHVybnMgYm9vbGVhbiBpbmRpY2F0aW5nIGEgVG9DIGNhbiBiZSBnZW5lcmF0ZWRcbiAgICovXG4gIGlzQXBwbGljYWJsZSh3aWRnZXQ6IFdpZGdldCk6IGJvb2xlYW4ge1xuICAgIGNvbnN0IGlzQXBwbGljYWJsZSA9IHN1cGVyLmlzQXBwbGljYWJsZSh3aWRnZXQpO1xuXG4gICAgaWYgKGlzQXBwbGljYWJsZSkge1xuICAgICAgbGV0IG1pbWUgPSAod2lkZ2V0IGFzIGFueSkuY29udGVudD8ubW9kZWw/Lm1pbWVUeXBlO1xuICAgICAgcmV0dXJuIG1pbWUgJiYgVGFibGVPZkNvbnRlbnRzVXRpbHMuTWFya2Rvd24uaXNNYXJrZG93bihtaW1lKTtcbiAgICB9XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCBmb3IgdGhlIHdpZGdldFxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gd2lkZ2V0XG4gICAqIEBwYXJhbSBjb25maWd1cmF0aW9uIC0gVGFibGUgb2YgY29udGVudHMgY29uZmlndXJhdGlvblxuICAgKiBAcmV0dXJucyBUaGUgdGFibGUgb2YgY29udGVudHMgbW9kZWxcbiAgICovXG4gIHByb3RlY3RlZCBfY3JlYXRlTmV3KFxuICAgIHdpZGdldDogSURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3IsIERvY3VtZW50UmVnaXN0cnkuSU1vZGVsPixcbiAgICBjb25maWd1cmF0aW9uPzogVGFibGVPZkNvbnRlbnRzLklDb25maWdcbiAgKTogTWFya2Rvd25UYWJsZU9mQ29udGVudHNNb2RlbCB7XG4gICAgcmV0dXJuIG5ldyBNYXJrZG93blRhYmxlT2ZDb250ZW50c01vZGVsKHdpZGdldCwgY29uZmlndXJhdGlvbik7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuLyplc2xpbnQgbm8taW52YWxpZC1yZWdleHA6IFtcImVycm9yXCIsIHsgXCJhbGxvd0NvbnN0cnVjdG9yRmxhZ3NcIjogW1wiZFwiXSB9XSovXG5cbmltcG9ydCB7IERvY3VtZW50UmVnaXN0cnksIElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IFRhYmxlT2ZDb250ZW50cywgVGFibGVPZkNvbnRlbnRzTW9kZWwgfSBmcm9tICdAanVweXRlcmxhYi90b2MnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IEZpbGVFZGl0b3IgfSBmcm9tICcuLi93aWRnZXQnO1xuaW1wb3J0IHsgRWRpdG9yVGFibGVPZkNvbnRlbnRzRmFjdG9yeSwgSUVkaXRvckhlYWRpbmcgfSBmcm9tICcuL2ZhY3RvcnknO1xuXG4vKipcbiAqIFJlZ3VsYXIgZXhwcmVzc2lvbiB0byBjcmVhdGUgdGhlIG91dGxpbmVcbiAqL1xubGV0IEtFWVdPUkRTOiBSZWdFeHA7XG50cnkge1xuICAvLyBodHRwczovL2dpdGh1Yi5jb20vdGMzOS9wcm9wb3NhbC1yZWdleHAtbWF0Y2gtaW5kaWNlcyB3YXMgYWNjZXB0ZWRcbiAgLy8gaW4gTWF5IDIwMjEgKGh0dHBzOi8vZ2l0aHViLmNvbS90YzM5L3Byb3Bvc2Fscy9ibG9iL21haW4vZmluaXNoZWQtcHJvcG9zYWxzLm1kKVxuICAvLyBTbyB3ZSB3aWxsIGZhbGxiYWNrIHRvIHRoZSBwb2x5ZmlsbCByZWdleHAtbWF0Y2gtaW5kaWNlcyBpZiBub3QgYXZhaWxhYmxlXG4gIEtFWVdPUkRTID0gbmV3IFJlZ0V4cCgnXlxcXFxzKihjbGFzcyB8ZGVmIHxmcm9tIHxpbXBvcnQgKScsICdkJyk7XG59IGNhdGNoIHtcbiAgS0VZV09SRFMgPSBuZXcgUmVnRXhwKCdeXFxcXHMqKGNsYXNzIHxkZWYgfGZyb20gfGltcG9ydCApJyk7XG59XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudCBtb2RlbCBmb3IgUHl0aG9uIGZpbGVzLlxuICovXG5leHBvcnQgY2xhc3MgUHl0aG9uVGFibGVPZkNvbnRlbnRzTW9kZWwgZXh0ZW5kcyBUYWJsZU9mQ29udGVudHNNb2RlbDxcbiAgSUVkaXRvckhlYWRpbmcsXG4gIElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yLCBEb2N1bWVudFJlZ2lzdHJ5LklNb2RlbD5cbj4ge1xuICAvKipcbiAgICogVHlwZSBvZiBkb2N1bWVudCBzdXBwb3J0ZWQgYnkgdGhlIG1vZGVsLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIEEgYGRhdGEtZG9jdW1lbnQtdHlwZWAgYXR0cmlidXRlIHdpdGggdGhpcyB2YWx1ZSB3aWxsIGJlIHNldFxuICAgKiBvbiB0aGUgdHJlZSB2aWV3IGAuanAtVGFibGVPZkNvbnRlbnRzLWNvbnRlbnRbZGF0YS1kb2N1bWVudC10eXBlPVwiLi4uXCJdYFxuICAgKi9cbiAgZ2V0IGRvY3VtZW50VHlwZSgpOiBzdHJpbmcge1xuICAgIHJldHVybiAncHl0aG9uJztcbiAgfVxuXG4gIC8qKlxuICAgKiBQcm9kdWNlIHRoZSBoZWFkaW5ncyBmb3IgYSBkb2N1bWVudC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGxpc3Qgb2YgbmV3IGhlYWRpbmdzIG9yIGBudWxsYCBpZiBub3RoaW5nIG5lZWRzIHRvIGJlIHVwZGF0ZWQuXG4gICAqL1xuICBwcm90ZWN0ZWQgYXN5bmMgZ2V0SGVhZGluZ3MoKTogUHJvbWlzZTxJRWRpdG9ySGVhZGluZ1tdIHwgbnVsbD4ge1xuICAgIGlmICghdGhpcy5pc0FjdGl2ZSkge1xuICAgICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShudWxsKTtcbiAgICB9XG5cbiAgICAvLyBTcGxpdCB0aGUgdGV4dCBpbnRvIGxpbmVzOlxuICAgIGNvbnN0IGxpbmVzID0gdGhpcy53aWRnZXQuY29udGVudC5tb2RlbC5zaGFyZWRNb2RlbFxuICAgICAgLmdldFNvdXJjZSgpXG4gICAgICAuc3BsaXQoJ1xcbicpIGFzIEFycmF5PHN0cmluZz47XG5cbiAgICAvLyBJdGVyYXRlIG92ZXIgdGhlIGxpbmVzIHRvIGdldCB0aGUgaGVhZGluZyBsZXZlbCBhbmQgdGV4dCBmb3IgZWFjaCBsaW5lOlxuICAgIGxldCBoZWFkaW5ncyA9IG5ldyBBcnJheTxJRWRpdG9ySGVhZGluZz4oKTtcbiAgICBsZXQgcHJvY2Vzc2luZ0ltcG9ydHMgPSBmYWxzZTtcblxuICAgIGxldCBpbmRlbnQgPSAxO1xuXG4gICAgbGV0IGxpbmVJZHggPSAtMTtcbiAgICBmb3IgKGNvbnN0IGxpbmUgb2YgbGluZXMpIHtcbiAgICAgIGxpbmVJZHgrKztcbiAgICAgIGxldCBoYXNLZXl3b3JkOiBSZWdFeHBFeGVjQXJyYXkgfCBudWxsO1xuICAgICAgaWYgKEtFWVdPUkRTLmZsYWdzLmluY2x1ZGVzKCdkJykpIHtcbiAgICAgICAgaGFzS2V5d29yZCA9IEtFWVdPUkRTLmV4ZWMobGluZSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBjb25zdCB7IGRlZmF1bHQ6IGV4ZWNXaXRoSW5kaWNlcyB9ID0gYXdhaXQgaW1wb3J0KFxuICAgICAgICAgICdyZWdleHAtbWF0Y2gtaW5kaWNlcydcbiAgICAgICAgKTtcbiAgICAgICAgaGFzS2V5d29yZCA9IGV4ZWNXaXRoSW5kaWNlcyhLRVlXT1JEUywgbGluZSk7XG4gICAgICB9XG4gICAgICBpZiAoaGFzS2V5d29yZCkge1xuICAgICAgICAvLyBJbmRleCAwIGNvbnRhaW5zIHRoZSBzcGFjZXMsIGluZGV4IDEgaXMgdGhlIGtleXdvcmQgZ3JvdXBcbiAgICAgICAgY29uc3QgW3N0YXJ0XSA9IChoYXNLZXl3b3JkIGFzIGFueSkuaW5kaWNlc1sxXTtcbiAgICAgICAgaWYgKGluZGVudCA9PT0gMSAmJiBzdGFydCA+IDApIHtcbiAgICAgICAgICBpbmRlbnQgPSBzdGFydDtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGlzSW1wb3J0ID0gWydmcm9tICcsICdpbXBvcnQgJ10uaW5jbHVkZXMoaGFzS2V5d29yZFsxXSk7XG4gICAgICAgIGlmIChpc0ltcG9ydCAmJiBwcm9jZXNzaW5nSW1wb3J0cykge1xuICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICB9XG4gICAgICAgIHByb2Nlc3NpbmdJbXBvcnRzID0gaXNJbXBvcnQ7XG5cbiAgICAgICAgY29uc3QgbGV2ZWwgPSAxICsgc3RhcnQgLyBpbmRlbnQ7XG5cbiAgICAgICAgaWYgKGxldmVsID4gdGhpcy5jb25maWd1cmF0aW9uLm1heGltYWxEZXB0aCkge1xuICAgICAgICAgIGNvbnRpbnVlO1xuICAgICAgICB9XG5cbiAgICAgICAgaGVhZGluZ3MucHVzaCh7XG4gICAgICAgICAgdGV4dDogbGluZS5zbGljZShzdGFydCksXG4gICAgICAgICAgbGV2ZWwsXG4gICAgICAgICAgbGluZTogbGluZUlkeFxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKGhlYWRpbmdzKTtcbiAgfVxufVxuXG4vKipcbiAqIFRhYmxlIG9mIGNvbnRlbnQgbW9kZWwgZmFjdG9yeSBmb3IgUHl0aG9uIGZpbGVzLlxuICovXG5leHBvcnQgY2xhc3MgUHl0aG9uVGFibGVPZkNvbnRlbnRzRmFjdG9yeSBleHRlbmRzIEVkaXRvclRhYmxlT2ZDb250ZW50c0ZhY3Rvcnkge1xuICAvKipcbiAgICogV2hldGhlciB0aGUgZmFjdG9yeSBjYW4gaGFuZGxlIHRoZSB3aWRnZXQgb3Igbm90LlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gd2lkZ2V0XG4gICAqIEByZXR1cm5zIGJvb2xlYW4gaW5kaWNhdGluZyBhIFRvQyBjYW4gYmUgZ2VuZXJhdGVkXG4gICAqL1xuICBpc0FwcGxpY2FibGUod2lkZ2V0OiBXaWRnZXQpOiBib29sZWFuIHtcbiAgICBjb25zdCBpc0FwcGxpY2FibGUgPSBzdXBlci5pc0FwcGxpY2FibGUod2lkZ2V0KTtcblxuICAgIGlmIChpc0FwcGxpY2FibGUpIHtcbiAgICAgIGxldCBtaW1lID0gKHdpZGdldCBhcyBhbnkpLmNvbnRlbnQ/Lm1vZGVsPy5taW1lVHlwZTtcbiAgICAgIHJldHVybiAoXG4gICAgICAgIG1pbWUgJiZcbiAgICAgICAgKG1pbWUgPT09ICdhcHBsaWNhdGlvbi94LXB5dGhvbi1jb2RlJyB8fCBtaW1lID09PSAndGV4dC94LXB5dGhvbicpXG4gICAgICApO1xuICAgIH1cbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHRhYmxlIG9mIGNvbnRlbnRzIG1vZGVsIGZvciB0aGUgd2lkZ2V0XG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgLSB3aWRnZXRcbiAgICogQHBhcmFtIGNvbmZpZ3VyYXRpb24gLSBUYWJsZSBvZiBjb250ZW50cyBjb25maWd1cmF0aW9uXG4gICAqIEByZXR1cm5zIFRoZSB0YWJsZSBvZiBjb250ZW50cyBtb2RlbFxuICAgKi9cbiAgcHJvdGVjdGVkIF9jcmVhdGVOZXcoXG4gICAgd2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4sXG4gICAgY29uZmlndXJhdGlvbj86IFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnXG4gICk6IFB5dGhvblRhYmxlT2ZDb250ZW50c01vZGVsIHtcbiAgICByZXR1cm4gbmV3IFB5dGhvblRhYmxlT2ZDb250ZW50c01vZGVsKHdpZGdldCwgY29uZmlndXJhdGlvbik7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVdpZGdldFRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJRG9jdW1lbnRXaWRnZXQgfSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IEZpbGVFZGl0b3IgfSBmcm9tICcuL3dpZGdldCc7XG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IHRyYWNrcyBlZGl0b3Igd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRWRpdG9yVHJhY2tlclxuICBleHRlbmRzIElXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPj4ge31cblxuLyoqXG4gKiBUaGUgZWRpdG9yIHRyYWNrZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJRWRpdG9yVHJhY2tlciA9IG5ldyBUb2tlbjxJRWRpdG9yVHJhY2tlcj4oXG4gICdAanVweXRlcmxhYi9maWxlZWRpdG9yOklFZGl0b3JUcmFja2VyJyxcbiAgYEEgd2lkZ2V0IHRyYWNrZXIgZm9yIGZpbGUgZWRpdG9ycy5cbiAgVXNlIHRoaXMgaWYgeW91IHdhbnQgdG8gYmUgYWJsZSB0byBpdGVyYXRlIG92ZXIgYW5kIGludGVyYWN0IHdpdGggZmlsZSBlZGl0b3JzXG4gIGNyZWF0ZWQgYnkgdGhlIGFwcGxpY2F0aW9uLmBcbik7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7XG4gIENvZGVFZGl0b3IsXG4gIENvZGVFZGl0b3JXcmFwcGVyLFxuICBJRWRpdG9yTWltZVR5cGVTZXJ2aWNlLFxuICBJRWRpdG9yU2VydmljZXNcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQge1xuICBBQkNXaWRnZXRGYWN0b3J5LFxuICBEb2N1bWVudFJlZ2lzdHJ5LFxuICBEb2N1bWVudFdpZGdldCxcbiAgSURvY3VtZW50V2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IHRleHRFZGl0b3JJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBQcm9taXNlRGVsZWdhdGUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgU3RhY2tlZExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgZGF0YSBhdHRyaWJ1dGUgYWRkZWQgdG8gYSB3aWRnZXQgdGhhdCBjYW4gcnVuIGNvZGUuXG4gKi9cbmNvbnN0IENPREVfUlVOTkVSID0gJ2pwQ29kZVJ1bm5lcic7XG5cbi8qKlxuICogVGhlIGRhdGEgYXR0cmlidXRlIGFkZGVkIHRvIGEgd2lkZ2V0IHRoYXQgY2FuIHVuZG8uXG4gKi9cbmNvbnN0IFVORE9FUiA9ICdqcFVuZG9lcic7XG5cbi8qKlxuICogQSB3aWRnZXQgZm9yIGVkaXRvcnMuXG4gKi9cbmV4cG9ydCBjbGFzcyBGaWxlRWRpdG9yIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBlZGl0b3Igd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogRmlsZUVkaXRvci5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtRmlsZUVkaXRvcicpO1xuXG4gICAgY29uc3QgY29udGV4dCA9ICh0aGlzLl9jb250ZXh0ID0gb3B0aW9ucy5jb250ZXh0KTtcbiAgICB0aGlzLl9taW1lVHlwZVNlcnZpY2UgPSBvcHRpb25zLm1pbWVUeXBlU2VydmljZTtcblxuICAgIGNvbnN0IGVkaXRvcldpZGdldCA9ICh0aGlzLl9lZGl0b3JXaWRnZXQgPSBuZXcgQ29kZUVkaXRvcldyYXBwZXIoe1xuICAgICAgZmFjdG9yeTogb3B0aW9ucy5mYWN0b3J5LFxuICAgICAgbW9kZWw6IGNvbnRleHQubW9kZWwsXG4gICAgICBlZGl0b3JPcHRpb25zOiB7XG4gICAgICAgIGNvbmZpZzogRmlsZUVkaXRvci5kZWZhdWx0RWRpdG9yQ29uZmlnXG4gICAgICB9XG4gICAgfSkpO1xuICAgIHRoaXMuX2VkaXRvcldpZGdldC5hZGRDbGFzcygnanAtRmlsZUVkaXRvckNvZGVXcmFwcGVyJyk7XG4gICAgdGhpcy5fZWRpdG9yV2lkZ2V0Lm5vZGUuZGF0YXNldFtDT0RFX1JVTk5FUl0gPSAndHJ1ZSc7XG4gICAgdGhpcy5fZWRpdG9yV2lkZ2V0Lm5vZGUuZGF0YXNldFtVTkRPRVJdID0gJ3RydWUnO1xuXG4gICAgdGhpcy5lZGl0b3IgPSBlZGl0b3JXaWRnZXQuZWRpdG9yO1xuICAgIHRoaXMubW9kZWwgPSBlZGl0b3JXaWRnZXQubW9kZWw7XG5cbiAgICB2b2lkIGNvbnRleHQucmVhZHkudGhlbigoKSA9PiB7XG4gICAgICB0aGlzLl9vbkNvbnRleHRSZWFkeSgpO1xuICAgIH0pO1xuXG4gICAgLy8gTGlzdGVuIGZvciBjaGFuZ2VzIHRvIHRoZSBwYXRoLlxuICAgIHRoaXMuX29uUGF0aENoYW5nZWQoKTtcbiAgICBjb250ZXh0LnBhdGhDaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25QYXRoQ2hhbmdlZCwgdGhpcyk7XG5cbiAgICBjb25zdCBsYXlvdXQgPSAodGhpcy5sYXlvdXQgPSBuZXcgU3RhY2tlZExheW91dCgpKTtcbiAgICBsYXlvdXQuYWRkV2lkZ2V0KGVkaXRvcldpZGdldCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBjb250ZXh0IGZvciB0aGUgZWRpdG9yIHdpZGdldC5cbiAgICovXG4gIGdldCBjb250ZXh0KCk6IERvY3VtZW50UmVnaXN0cnkuQ29udGV4dCB7XG4gICAgcmV0dXJuIHRoaXMuX2NvbnRleHQ7XG4gIH1cblxuICAvKipcbiAgICogQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgZmlsZSBlZGl0b3IgaXMgcmVhZHkuXG4gICAqL1xuICBnZXQgcmVhZHkoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3JlYWR5LnByb21pc2U7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBET00gZXZlbnRzIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIG1ldGhvZCBpbXBsZW1lbnRzIHRoZSBET00gYEV2ZW50TGlzdGVuZXJgIGludGVyZmFjZSBhbmQgaXNcbiAgICogY2FsbGVkIGluIHJlc3BvbnNlIHRvIGV2ZW50cyBvbiB0aGUgd2lkZ2V0J3Mgbm9kZS4gSXQgc2hvdWxkXG4gICAqIG5vdCBiZSBjYWxsZWQgZGlyZWN0bHkgYnkgdXNlciBjb2RlLlxuICAgKi9cbiAgaGFuZGxlRXZlbnQoZXZlbnQ6IEV2ZW50KTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLm1vZGVsKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHN3aXRjaCAoZXZlbnQudHlwZSkge1xuICAgICAgY2FzZSAnbW91c2Vkb3duJzpcbiAgICAgICAgdGhpcy5fZW5zdXJlRm9jdXMoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBhZnRlci1hdHRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgc3VwZXIub25BZnRlckF0dGFjaChtc2cpO1xuICAgIGNvbnN0IG5vZGUgPSB0aGlzLm5vZGU7XG4gICAgbm9kZS5hZGRFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGJlZm9yZS1kZXRhY2hgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQmVmb3JlRGV0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGNvbnN0IG5vZGUgPSB0aGlzLm5vZGU7XG4gICAgbm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhY3RpdmF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fZW5zdXJlRm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBFbnN1cmUgdGhhdCB0aGUgd2lkZ2V0IGhhcyBmb2N1cy5cbiAgICovXG4gIHByaXZhdGUgX2Vuc3VyZUZvY3VzKCk6IHZvaWQge1xuICAgIGlmICghdGhpcy5lZGl0b3IuaGFzRm9jdXMoKSkge1xuICAgICAgdGhpcy5lZGl0b3IuZm9jdXMoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFjdGlvbnMgdGhhdCBzaG91bGQgYmUgdGFrZW4gd2hlbiB0aGUgY29udGV4dCBpcyByZWFkeS5cbiAgICovXG4gIHByaXZhdGUgX29uQ29udGV4dFJlYWR5KCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBQcmV2ZW50IHRoZSBpbml0aWFsIGxvYWRpbmcgZnJvbSBkaXNrIGZyb20gYmVpbmcgaW4gdGhlIGVkaXRvciBoaXN0b3J5LlxuICAgIHRoaXMuZWRpdG9yLmNsZWFySGlzdG9yeSgpO1xuICAgIC8vIFJlc29sdmUgdGhlIHJlYWR5IHByb21pc2UuXG4gICAgdGhpcy5fcmVhZHkucmVzb2x2ZSh1bmRlZmluZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgcGF0aC5cbiAgICovXG4gIHByaXZhdGUgX29uUGF0aENoYW5nZWQoKTogdm9pZCB7XG4gICAgY29uc3QgZWRpdG9yID0gdGhpcy5lZGl0b3I7XG4gICAgY29uc3QgbG9jYWxQYXRoID0gdGhpcy5fY29udGV4dC5sb2NhbFBhdGg7XG5cbiAgICBlZGl0b3IubW9kZWwubWltZVR5cGUgPVxuICAgICAgdGhpcy5fbWltZVR5cGVTZXJ2aWNlLmdldE1pbWVUeXBlQnlGaWxlUGF0aChsb2NhbFBhdGgpO1xuICB9XG5cbiAgbW9kZWw6IENvZGVFZGl0b3IuSU1vZGVsO1xuICBlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvcjtcbiAgcHJpdmF0ZSBfY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0O1xuICBwcml2YXRlIF9lZGl0b3JXaWRnZXQ6IENvZGVFZGl0b3JXcmFwcGVyO1xuICBwcml2YXRlIF9taW1lVHlwZVNlcnZpY2U6IElFZGl0b3JNaW1lVHlwZVNlcnZpY2U7XG4gIHByaXZhdGUgX3JlYWR5ID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGVkaXRvciB3aWRnZXQgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBGaWxlRWRpdG9yIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGFuIGVkaXRvciB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIGNvZGUgZWRpdG9yIGZhY3RvcnkuXG4gICAgICovXG4gICAgZmFjdG9yeTogQ29kZUVkaXRvci5GYWN0b3J5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1pbWUgdHlwZSBzZXJ2aWNlIGZvciB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIG1pbWVUeXBlU2VydmljZTogSUVkaXRvck1pbWVUeXBlU2VydmljZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBkb2N1bWVudCBjb250ZXh0IGFzc29jaWF0ZWQgd2l0aCB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuQ29kZUNvbnRleHQ7XG4gIH1cblxuICAvKipcbiAgICogRmlsZSBlZGl0b3IgZGVmYXVsdCBjb25maWd1cmF0aW9uLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRFZGl0b3JDb25maWc6IFJlY29yZDxzdHJpbmcsIGFueT4gPSB7XG4gICAgbGluZU51bWJlcnM6IHRydWUsXG4gICAgc2Nyb2xsUGFzdEVuZDogdHJ1ZVxuICB9O1xufVxuXG4vKipcbiAqIEEgd2lkZ2V0IGZhY3RvcnkgZm9yIGVkaXRvcnMuXG4gKi9cbmV4cG9ydCBjbGFzcyBGaWxlRWRpdG9yRmFjdG9yeSBleHRlbmRzIEFCQ1dpZGdldEZhY3Rvcnk8XG4gIElEb2N1bWVudFdpZGdldDxGaWxlRWRpdG9yPixcbiAgRG9jdW1lbnRSZWdpc3RyeS5JQ29kZU1vZGVsXG4+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBlZGl0b3Igd2lkZ2V0IGZhY3RvcnkuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBGaWxlRWRpdG9yRmFjdG9yeS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMuZmFjdG9yeU9wdGlvbnMpO1xuICAgIHRoaXMuX3NlcnZpY2VzID0gb3B0aW9ucy5lZGl0b3JTZXJ2aWNlcztcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGdpdmVuIGEgY29udGV4dC5cbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVOZXdXaWRnZXQoXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db2RlQ29udGV4dFxuICApOiBJRG9jdW1lbnRXaWRnZXQ8RmlsZUVkaXRvcj4ge1xuICAgIGNvbnN0IGZ1bmMgPSB0aGlzLl9zZXJ2aWNlcy5mYWN0b3J5U2VydmljZS5uZXdEb2N1bWVudEVkaXRvcjtcbiAgICBjb25zdCBmYWN0b3J5OiBDb2RlRWRpdG9yLkZhY3RvcnkgPSBvcHRpb25zID0+IHtcbiAgICAgIC8vIFVzZSBzYW1lIGlkIGFzIGRvY3VtZW50IGZhY3RvcnlcbiAgICAgIHJldHVybiBmdW5jKG9wdGlvbnMpO1xuICAgIH07XG4gICAgY29uc3QgY29udGVudCA9IG5ldyBGaWxlRWRpdG9yKHtcbiAgICAgIGZhY3RvcnksXG4gICAgICBjb250ZXh0LFxuICAgICAgbWltZVR5cGVTZXJ2aWNlOiB0aGlzLl9zZXJ2aWNlcy5taW1lVHlwZVNlcnZpY2VcbiAgICB9KTtcblxuICAgIGNvbnRlbnQudGl0bGUuaWNvbiA9IHRleHRFZGl0b3JJY29uO1xuICAgIGNvbnN0IHdpZGdldCA9IG5ldyBEb2N1bWVudFdpZGdldCh7IGNvbnRlbnQsIGNvbnRleHQgfSk7XG4gICAgcmV0dXJuIHdpZGdldDtcbiAgfVxuXG4gIHByaXZhdGUgX3NlcnZpY2VzOiBJRWRpdG9yU2VydmljZXM7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgYEZpbGVFZGl0b3JGYWN0b3J5YCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIEZpbGVFZGl0b3JGYWN0b3J5IHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGFuIGVkaXRvciB3aWRnZXQgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBlZGl0b3Igc2VydmljZXMgdXNlZCBieSB0aGUgZmFjdG9yeS5cbiAgICAgKi9cbiAgICBlZGl0b3JTZXJ2aWNlczogSUVkaXRvclNlcnZpY2VzO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGZhY3Rvcnkgb3B0aW9ucyBhc3NvY2lhdGVkIHdpdGggdGhlIGZhY3RvcnkuXG4gICAgICovXG4gICAgZmFjdG9yeU9wdGlvbnM6IERvY3VtZW50UmVnaXN0cnkuSVdpZGdldEZhY3RvcnlPcHRpb25zPFxuICAgICAgSURvY3VtZW50V2lkZ2V0PEZpbGVFZGl0b3I+XG4gICAgPjtcbiAgfVxufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9