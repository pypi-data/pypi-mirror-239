"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_toc_lib_index_js"],{

/***/ "../packages/toc/lib/factory.js":
/*!**************************************!*\
  !*** ../packages/toc/lib/factory.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsFactory": () => (/* binding */ TableOfContentsFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Timeout for throttling ToC rendering following model changes.
 *
 * @private
 */
const RENDER_TIMEOUT = 1000;
/**
 * Abstract table of contents model factory for IDocumentWidget.
 */
class TableOfContentsFactory {
    /**
     * Constructor
     *
     * @param tracker Widget tracker
     */
    constructor(tracker) {
        this.tracker = tracker;
    }
    /**
     * Whether the factory can handle the widget or not.
     *
     * @param widget - widget
     * @returns boolean indicating a ToC can be generated
     */
    isApplicable(widget) {
        if (!this.tracker.has(widget)) {
            return false;
        }
        return true;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    createNew(widget, configuration) {
        const model = this._createNew(widget, configuration);
        const context = widget.context;
        const updateHeadings = () => {
            model.refresh().catch(reason => {
                console.error('Failed to update the table of contents.', reason);
            });
        };
        const monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.ActivityMonitor({
            signal: context.model.contentChanged,
            timeout: RENDER_TIMEOUT
        });
        monitor.activityStopped.connect(updateHeadings);
        const updateTitle = () => {
            model.title = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.basename(context.localPath);
        };
        context.pathChanged.connect(updateTitle);
        context.ready
            .then(() => {
            updateTitle();
            updateHeadings();
        })
            .catch(reason => {
            console.error(`Failed to initiate headings for ${context.localPath}.`);
        });
        widget.disposed.connect(() => {
            monitor.activityStopped.disconnect(updateHeadings);
            context.pathChanged.disconnect(updateTitle);
        });
        return model;
    }
}


/***/ }),

/***/ "../packages/toc/lib/index.js":
/*!************************************!*\
  !*** ../packages/toc/lib/index.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITableOfContentsRegistry": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_7__.ITableOfContentsRegistry),
/* harmony export */   "ITableOfContentsTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_7__.ITableOfContentsTracker),
/* harmony export */   "TableOfContents": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_7__.TableOfContents),
/* harmony export */   "TableOfContentsFactory": () => (/* reexport safe */ _factory__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsFactory),
/* harmony export */   "TableOfContentsItem": () => (/* reexport safe */ _tocitem__WEBPACK_IMPORTED_MODULE_5__.TableOfContentsItem),
/* harmony export */   "TableOfContentsModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_1__.TableOfContentsModel),
/* harmony export */   "TableOfContentsPanel": () => (/* reexport safe */ _panel__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsPanel),
/* harmony export */   "TableOfContentsRegistry": () => (/* reexport safe */ _registry__WEBPACK_IMPORTED_MODULE_3__.TableOfContentsRegistry),
/* harmony export */   "TableOfContentsTracker": () => (/* reexport safe */ _tracker__WEBPACK_IMPORTED_MODULE_8__.TableOfContentsTracker),
/* harmony export */   "TableOfContentsTree": () => (/* reexport safe */ _toctree__WEBPACK_IMPORTED_MODULE_6__.TableOfContentsTree),
/* harmony export */   "TableOfContentsUtils": () => (/* reexport module object */ _utils__WEBPACK_IMPORTED_MODULE_9__),
/* harmony export */   "TableOfContentsWidget": () => (/* reexport safe */ _treeview__WEBPACK_IMPORTED_MODULE_4__.TableOfContentsWidget)
/* harmony export */ });
/* harmony import */ var _factory__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./factory */ "../packages/toc/lib/factory.js");
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./model */ "../packages/toc/lib/model.js");
/* harmony import */ var _panel__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./panel */ "../packages/toc/lib/panel.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./registry */ "../packages/toc/lib/registry.js");
/* harmony import */ var _treeview__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./treeview */ "../packages/toc/lib/treeview.js");
/* harmony import */ var _tocitem__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./tocitem */ "../packages/toc/lib/tocitem.js");
/* harmony import */ var _toctree__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./toctree */ "../packages/toc/lib/toctree.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tokens */ "../packages/toc/lib/tokens.js");
/* harmony import */ var _tracker__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tracker */ "../packages/toc/lib/tracker.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./utils */ "../packages/toc/lib/utils/index.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module toc
 */









// Namespace the utils



/***/ }),

/***/ "../packages/toc/lib/model.js":
/*!************************************!*\
  !*** ../packages/toc/lib/model.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsModel": () => (/* binding */ TableOfContentsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "../packages/toc/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/**
 * Abstract table of contents model.
 */
class TableOfContentsModel extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.VDomModel {
    /**
     * Constructor
     *
     * @param widget The widget to search in
     * @param configuration Default model configuration
     */
    constructor(widget, configuration) {
        super();
        this.widget = widget;
        this._activeHeading = null;
        this._activeHeadingChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._collapseChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._configuration = configuration !== null && configuration !== void 0 ? configuration : { ..._tokens__WEBPACK_IMPORTED_MODULE_3__.TableOfContents.defaultConfig };
        this._headings = new Array();
        this._headingsChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._isActive = false;
        this._isRefreshing = false;
        this._needsRefreshing = false;
    }
    /**
     * Current active entry.
     *
     * @returns table of contents active entry
     */
    get activeHeading() {
        return this._activeHeading;
    }
    /**
     * Signal emitted when the active heading changes.
     */
    get activeHeadingChanged() {
        return this._activeHeadingChanged;
    }
    /**
     * Signal emitted when a table of content section collapse state changes.
     */
    get collapseChanged() {
        return this._collapseChanged;
    }
    /**
     * Model configuration
     */
    get configuration() {
        return this._configuration;
    }
    /**
     * List of headings.
     *
     * @returns table of contents list of headings
     */
    get headings() {
        return this._headings;
    }
    /**
     * Signal emitted when the headings changes.
     */
    get headingsChanged() {
        return this._headingsChanged;
    }
    /**
     * Whether the model is active or not.
     *
     * #### Notes
     * An active model means it is displayed in the table of contents.
     * This can be used by subclass to limit updating the headings.
     */
    get isActive() {
        return this._isActive;
    }
    set isActive(v) {
        this._isActive = v;
        // Refresh on activation expect if it is always active
        //  => a ToC model is always active e.g. when displaying numbering in the document
        if (this._isActive && !this.isAlwaysActive) {
            this.refresh().catch(reason => {
                console.error('Failed to refresh ToC model.', reason);
            });
        }
    }
    /**
     * Whether the model gets updated even if the table of contents panel
     * is hidden or not.
     *
     * #### Notes
     * For example, ToC models use to add title numbering will
     * set this to true.
     */
    get isAlwaysActive() {
        return false;
    }
    /**
     * List of configuration options supported by the model.
     */
    get supportedOptions() {
        return ['maximalDepth'];
    }
    /**
     * Document title
     */
    get title() {
        return this._title;
    }
    set title(v) {
        if (v !== this._title) {
            this._title = v;
            this.stateChanged.emit();
        }
    }
    /**
     * Refresh the headings list.
     */
    async refresh() {
        if (this._isRefreshing) {
            // Schedule a refresh if one is in progress
            this._needsRefreshing = true;
            return Promise.resolve();
        }
        this._isRefreshing = true;
        try {
            const newHeadings = await this.getHeadings();
            if (this._needsRefreshing) {
                this._needsRefreshing = false;
                this._isRefreshing = false;
                return this.refresh();
            }
            if (newHeadings &&
                !Private.areHeadingsEqual(newHeadings, this._headings)) {
                this._headings = newHeadings;
                this.stateChanged.emit();
                this._headingsChanged.emit();
            }
        }
        finally {
            this._isRefreshing = false;
        }
    }
    /**
     * Set a new active heading.
     *
     * @param heading The new active heading
     * @param emitSignal Whether to emit the activeHeadingChanged signal or not.
     */
    setActiveHeading(heading, emitSignal = true) {
        if (this._activeHeading !== heading) {
            this._activeHeading = heading;
            this.stateChanged.emit();
            if (emitSignal) {
                this._activeHeadingChanged.emit(heading);
            }
        }
    }
    /**
     * Model configuration setter.
     *
     * @param c New configuration
     */
    setConfiguration(c) {
        const newConfiguration = { ...this._configuration, ...c };
        if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepEqual(this._configuration, newConfiguration)) {
            this._configuration = newConfiguration;
            this.refresh().catch(reason => {
                console.error('Failed to update the table of contents.', reason);
            });
        }
    }
    /**
     * Callback on heading collapse.
     *
     * @param options.heading The heading to change state (all headings if not provided)
     * @param options.collapsed The new collapsed status (toggle existing status if not provided)
     */
    toggleCollapse(options) {
        var _a, _b;
        if (options.heading) {
            options.heading.collapsed =
                (_a = options.collapsed) !== null && _a !== void 0 ? _a : !options.heading.collapsed;
            this.stateChanged.emit();
            this._collapseChanged.emit(options.heading);
        }
        else {
            // Use the provided state or collapsed all except if all are collapsed
            const newState = (_b = options.collapsed) !== null && _b !== void 0 ? _b : !this.headings.some(h => { var _a; return !((_a = h.collapsed) !== null && _a !== void 0 ? _a : false); });
            this.headings.forEach(h => (h.collapsed = newState));
            this.stateChanged.emit();
            this._collapseChanged.emit(null);
        }
    }
}
/**
 * Private functions namespace
 */
var Private;
(function (Private) {
    /**
     * Test if two list of headings are equal or not.
     *
     * @param headings1 First list of headings
     * @param headings2 Second list of headings
     * @returns Whether the array are identical or not.
     */
    function areHeadingsEqual(headings1, headings2) {
        if (headings1.length === headings2.length) {
            for (let i = 0; i < headings1.length; i++) {
                if (headings1[i].level !== headings2[i].level ||
                    headings1[i].text !== headings2[i].text ||
                    headings1[i].prefix !== headings2[i].prefix) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    Private.areHeadingsEqual = areHeadingsEqual;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/toc/lib/panel.js":
/*!************************************!*\
  !*** ../packages/toc/lib/panel.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsPanel": () => (/* binding */ TableOfContentsPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _treeview__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./treeview */ "../packages/toc/lib/treeview.js");
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */



/**
 * Table of contents sidebar panel.
 */
class TableOfContentsPanel extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.SidePanel {
    /**
     * Constructor
     *
     * @param translator - Translator tool
     */
    constructor(translator) {
        super({ content: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Panel(), translator });
        this._model = null;
        this.addClass('jp-TableOfContents');
        this._title = new Private.Header(this._trans.__('Table of Contents'));
        this.header.addWidget(this._title);
        this._treeview = new _treeview__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsWidget({
            placeholderHeadline: this._trans.__('No Headings'),
            placeholderText: this._trans.__('The table of contents shows headings in notebooks and supported files.')
        });
        this._treeview.addClass('jp-TableOfContents-tree');
        this.content.addWidget(this._treeview);
    }
    /**
     * Get the current model.
     */
    get model() {
        return this._model;
    }
    set model(newValue) {
        var _a, _b;
        if (this._model !== newValue) {
            (_a = this._model) === null || _a === void 0 ? void 0 : _a.stateChanged.disconnect(this._onTitleChanged, this);
            this._model = newValue;
            if (this._model) {
                this._model.isActive = this.isVisible;
            }
            (_b = this._model) === null || _b === void 0 ? void 0 : _b.stateChanged.connect(this._onTitleChanged, this);
            this._onTitleChanged();
            this._treeview.model = this._model;
        }
    }
    onAfterHide(msg) {
        super.onAfterHide(msg);
        if (this._model) {
            this._model.isActive = false;
        }
    }
    onBeforeShow(msg) {
        super.onBeforeShow(msg);
        if (this._model) {
            this._model.isActive = true;
        }
    }
    _onTitleChanged() {
        var _a, _b;
        this._title.setTitle((_b = (_a = this._model) === null || _a === void 0 ? void 0 : _a.title) !== null && _b !== void 0 ? _b : this._trans.__('Table of Contents'));
    }
}
/**
 * Private helpers namespace
 */
var Private;
(function (Private) {
    /**
     * Panel header
     */
    class Header extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
        /**
         * Constructor
         *
         * @param title - Title text
         */
        constructor(title) {
            const node = document.createElement('h2');
            node.textContent = title;
            node.classList.add('jp-text-truncated');
            super({ node });
            this._title = node;
        }
        /**
         * Set the header title.
         */
        setTitle(title) {
            this._title.textContent = title;
        }
    }
    Private.Header = Header;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/toc/lib/registry.js":
/*!***************************************!*\
  !*** ../packages/toc/lib/registry.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsRegistry": () => (/* binding */ TableOfContentsRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Class for registering table of contents generators.
 */
class TableOfContentsRegistry {
    constructor() {
        this._generators = new Map();
        this._idCounter = 0;
    }
    /**
     * Finds a table of contents model for a widget.
     *
     * ## Notes
     *
     * -   If unable to find a table of contents model, the method return `undefined`.
     *
     * @param widget - widget
     * @param configuration - Default model configuration
     * @returns Table of contents model
     */
    getModel(widget, configuration) {
        for (const generator of this._generators.values()) {
            if (generator.isApplicable(widget)) {
                return generator.createNew(widget, configuration);
            }
        }
    }
    /**
     * Adds a table of contents generator to the registry.
     *
     * @param generator - table of contents generator
     */
    add(generator) {
        const id = this._idCounter++;
        this._generators.set(id, generator);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => {
            this._generators.delete(id);
        });
    }
}


/***/ }),

/***/ "../packages/toc/lib/tocitem.js":
/*!**************************************!*\
  !*** ../packages/toc/lib/tocitem.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsItem": () => (/* binding */ TableOfContentsItem)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * React component for a table of contents entry.
 */
class TableOfContentsItem extends react__WEBPACK_IMPORTED_MODULE_1__.PureComponent {
    /**
     * Renders a table of contents entry.
     *
     * @returns rendered entry
     */
    render() {
        const { children, isActive, heading, onCollapse, onMouseDown } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("li", { className: "jp-tocItem" },
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: `jp-tocItem-heading ${isActive ? 'jp-tocItem-active' : ''}`, onMouseDown: (event) => {
                    // React only on deepest item
                    if (!event.defaultPrevented) {
                        event.preventDefault();
                        onMouseDown(heading);
                    }
                } },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("button", { className: "jp-tocItem-collapser", onClick: (event) => {
                        event.preventDefault();
                        onCollapse(heading);
                    }, style: { visibility: children ? 'visible' : 'hidden' } }, heading.collapsed ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.caretRightIcon.react, { tag: "span", width: "20px" })) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.caretDownIcon.react, { tag: "span", width: "20px" }))),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("span", { className: "jp-tocItem-content", title: heading.text, ...heading.dataset },
                    heading.prefix,
                    heading.text)),
            children && !heading.collapsed && react__WEBPACK_IMPORTED_MODULE_1__.createElement("ol", null, children)));
    }
}


/***/ }),

/***/ "../packages/toc/lib/toctree.js":
/*!**************************************!*\
  !*** ../packages/toc/lib/toctree.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsTree": () => (/* binding */ TableOfContentsTree)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _tocitem__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tocitem */ "../packages/toc/lib/tocitem.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * React component for a table of contents tree.
 */
class TableOfContentsTree extends react__WEBPACK_IMPORTED_MODULE_0__.PureComponent {
    /**
     * Renders a table of contents tree.
     */
    render() {
        const { documentType } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("ol", { className: "jp-TableOfContents-content", ...{ 'data-document-type': documentType } }, this.buildTree()));
    }
    /**
     * Convert the flat headings list to a nested tree list
     */
    buildTree() {
        if (this.props.headings.length === 0) {
            return [];
        }
        const buildOneTree = (currentIndex) => {
            const items = this.props.headings;
            const children = new Array();
            const current = items[currentIndex];
            let nextCandidateIndex = currentIndex + 1;
            while (nextCandidateIndex < items.length) {
                const candidateItem = items[nextCandidateIndex];
                if (candidateItem.level <= current.level) {
                    break;
                }
                const [child, nextIndex] = buildOneTree(nextCandidateIndex);
                children.push(child);
                nextCandidateIndex = nextIndex;
            }
            const currentTree = (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_tocitem__WEBPACK_IMPORTED_MODULE_1__.TableOfContentsItem, { key: `${current.level}-${currentIndex}-${current.text}`, isActive: !!this.props.activeHeading && current === this.props.activeHeading, heading: current, onMouseDown: this.props.setActiveHeading, onCollapse: this.props.onCollapseChange }, children.length ? children : null));
            return [currentTree, nextCandidateIndex];
        };
        const trees = new Array();
        let currentIndex = 0;
        while (currentIndex < this.props.headings.length) {
            const [tree, nextIndex] = buildOneTree(currentIndex);
            trees.push(tree);
            currentIndex = nextIndex;
        }
        return trees;
    }
}


/***/ }),

/***/ "../packages/toc/lib/tokens.js":
/*!*************************************!*\
  !*** ../packages/toc/lib/tokens.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITableOfContentsRegistry": () => (/* binding */ ITableOfContentsRegistry),
/* harmony export */   "ITableOfContentsTracker": () => (/* binding */ ITableOfContentsTracker),
/* harmony export */   "TableOfContents": () => (/* binding */ TableOfContents)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Table of contents registry token.
 */
const ITableOfContentsRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/toc:ITableOfContentsRegistry', 'A service to register table of content factory.');
/**
 * Table of contents tracker token.
 */
const ITableOfContentsTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/toc:ITableOfContentsTracker', 'A widget tracker for table of contents.');
/**
 * Namespace for table of contents interface
 */
var TableOfContents;
(function (TableOfContents) {
    /**
     * Default table of content configuration
     */
    TableOfContents.defaultConfig = {
        baseNumbering: 1,
        maximalDepth: 4,
        numberingH1: true,
        numberHeaders: false,
        includeOutput: true,
        syncCollapseState: false
    };
})(TableOfContents || (TableOfContents = {}));


/***/ }),

/***/ "../packages/toc/lib/tracker.js":
/*!**************************************!*\
  !*** ../packages/toc/lib/tracker.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsTracker": () => (/* binding */ TableOfContentsTracker)
/* harmony export */ });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * Table of contents tracker
 */
class TableOfContentsTracker {
    /**
     * Constructor
     */
    constructor() {
        this.modelMapping = new WeakMap();
    }
    /**
     * Track a given model.
     *
     * @param widget Widget
     * @param model Table of contents model
     */
    add(widget, model) {
        this.modelMapping.set(widget, model);
    }
    /**
     * Get the table of contents model associated with a given widget.
     *
     * @param widget Widget
     * @returns The table of contents model
     */
    get(widget) {
        const model = this.modelMapping.get(widget);
        return !model || model.isDisposed ? null : model;
    }
}


/***/ }),

/***/ "../packages/toc/lib/treeview.js":
/*!***************************************!*\
  !*** ../packages/toc/lib/treeview.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TableOfContentsWidget": () => (/* binding */ TableOfContentsWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _toctree__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./toctree */ "../packages/toc/lib/toctree.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Table of contents widget.
 */
class TableOfContentsWidget extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    /**
     * Constructor
     *
     * @param options Widget options
     */
    constructor(options) {
        super(options.model);
        this._placeholderHeadline = options.placeholderHeadline;
        this._placeholderText = options.placeholderText;
    }
    /**
     * Render the content of this widget using the virtual DOM.
     *
     * This method will be called anytime the widget needs to be rendered, which
     * includes layout triggered rendering.
     */
    render() {
        if (!this.model || this.model.headings.length === 0) {
            return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-TableOfContents-placeholder" },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-TableOfContents-placeholderContent" },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("h3", null, this._placeholderHeadline),
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, this._placeholderText))));
        }
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_toctree__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsTree, { activeHeading: this.model.activeHeading, documentType: this.model.documentType, headings: this.model.headings, onCollapseChange: (heading) => {
                this.model.toggleCollapse({ heading });
            }, setActiveHeading: (heading) => {
                this.model.setActiveHeading(heading);
            } }));
    }
}


/***/ }),

/***/ "../packages/toc/lib/utils/common.js":
/*!*******************************************!*\
  !*** ../packages/toc/lib/utils/common.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NUMBERING_CLASS": () => (/* binding */ NUMBERING_CLASS),
/* harmony export */   "addPrefix": () => (/* binding */ addPrefix),
/* harmony export */   "clearNumbering": () => (/* binding */ clearNumbering),
/* harmony export */   "filterHeadings": () => (/* binding */ filterHeadings),
/* harmony export */   "getHTMLHeadings": () => (/* binding */ getHTMLHeadings),
/* harmony export */   "getPrefix": () => (/* binding */ getPrefix),
/* harmony export */   "isHTML": () => (/* binding */ isHTML)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../tokens */ "../packages/toc/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Class used to mark numbering prefix for headings in a document.
 */
const NUMBERING_CLASS = 'numbering-entry';
/**
 * Filter headings for table of contents and compute associated prefix
 *
 * @param headings Headings to process
 * @param options Options
 * @param initialLevels Initial levels for prefix computation
 * @returns Extracted headings
 */
function filterHeadings(headings, options, initialLevels = []) {
    const config = {
        ..._tokens__WEBPACK_IMPORTED_MODULE_0__.TableOfContents.defaultConfig,
        ...options
    };
    const levels = initialLevels;
    let previousLevel = levels.length;
    const filteredHeadings = new Array();
    for (const heading of headings) {
        if (heading.skip) {
            continue;
        }
        const level = heading.level;
        if (level > 0 && level <= config.maximalDepth) {
            const prefix = getPrefix(level, previousLevel, levels, config);
            previousLevel = level;
            filteredHeadings.push({
                ...heading,
                prefix
            });
        }
    }
    return filteredHeadings;
}
/**
 * Returns whether a MIME type corresponds to either HTML.
 *
 * @param mime - MIME type string
 * @returns boolean indicating whether a provided MIME type corresponds to either HTML
 *
 * @example
 * const bool = isHTML('text/html');
 * // returns true
 *
 * @example
 * const bool = isHTML('text/plain');
 * // returns false
 */
function isHTML(mime) {
    return mime === 'text/html';
}
/**
 * Parse a HTML string for headings.
 *
 * ### Notes
 * The html string is not sanitized - use with caution
 *
 * @param html HTML string to parse
 * @param force Whether to ignore HTML headings with class jp-toc-ignore and tocSkip or not
 * @returns Extracted headings
 */
function getHTMLHeadings(html, force = true) {
    var _a;
    const container = document.createElement('div');
    container.innerHTML = html;
    const headings = new Array();
    const headers = container.querySelectorAll('h1, h2, h3, h4, h5, h6');
    for (const h of headers) {
        const level = parseInt(h.tagName[1], 10);
        headings.push({
            text: (_a = h.textContent) !== null && _a !== void 0 ? _a : '',
            level,
            id: h === null || h === void 0 ? void 0 : h.getAttribute('id'),
            skip: h.classList.contains('jp-toc-ignore') || h.classList.contains('tocSkip')
        });
    }
    return headings;
}
/**
 * Add an heading prefix to a HTML node.
 *
 * @param container HTML node containing the heading
 * @param selector Heading selector
 * @param prefix Title prefix to add
 * @returns The modified HTML element
 */
function addPrefix(container, selector, prefix) {
    let element = container.querySelector(selector);
    if (!element) {
        return null;
    }
    if (!element.querySelector(`span.${NUMBERING_CLASS}`)) {
        addNumbering(element, prefix);
    }
    else {
        // There are likely multiple elements with the same selector
        //  => use the first one without prefix
        const allElements = container.querySelectorAll(selector);
        for (const el of allElements) {
            if (!el.querySelector(`span.${NUMBERING_CLASS}`)) {
                element = el;
                addNumbering(el, prefix);
                break;
            }
        }
    }
    return element;
}
/**
 * Update the levels and create the numbering prefix
 *
 * @param level Current level
 * @param previousLevel Previous level
 * @param levels Levels list
 * @param options Options
 * @returns The numbering prefix
 */
function getPrefix(level, previousLevel, levels, options) {
    const { baseNumbering, numberingH1, numberHeaders } = options;
    let prefix = '';
    if (numberHeaders) {
        const highestLevel = numberingH1 ? 1 : 2;
        if (level > previousLevel) {
            // Initialize the new levels
            for (let l = previousLevel; l < level - 1; l++) {
                levels[l] = 0;
            }
            levels[level - 1] = level === highestLevel ? baseNumbering : 1;
        }
        else {
            // Increment the current level
            levels[level - 1] += 1;
            // Drop higher levels
            if (level < previousLevel) {
                levels.splice(level);
            }
        }
        // If the header list skips some level, replace missing elements by 0
        if (numberingH1) {
            prefix = levels.map(level => level !== null && level !== void 0 ? level : 0).join('.') + '. ';
        }
        else {
            if (levels.length > 1) {
                prefix =
                    levels
                        .slice(1)
                        .map(level => level !== null && level !== void 0 ? level : 0)
                        .join('.') + '. ';
            }
        }
    }
    return prefix;
}
/**
 * Add a numbering prefix to a HTML element.
 *
 * @param el HTML element
 * @param numbering Numbering prefix to add
 */
function addNumbering(el, numbering) {
    el.insertAdjacentHTML('afterbegin', `<span class="${NUMBERING_CLASS}">${numbering}</span>`);
}
/**
 * Remove all numbering nodes from element
 * @param element Node to clear
 */
function clearNumbering(element) {
    element === null || element === void 0 ? void 0 : element.querySelectorAll(`span.${NUMBERING_CLASS}`).forEach(el => {
        el.remove();
    });
}


/***/ }),

/***/ "../packages/toc/lib/utils/index.js":
/*!******************************************!*\
  !*** ../packages/toc/lib/utils/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Markdown": () => (/* reexport module object */ _markdown__WEBPACK_IMPORTED_MODULE_1__),
/* harmony export */   "NUMBERING_CLASS": () => (/* reexport safe */ _common__WEBPACK_IMPORTED_MODULE_0__.NUMBERING_CLASS),
/* harmony export */   "addPrefix": () => (/* reexport safe */ _common__WEBPACK_IMPORTED_MODULE_0__.addPrefix),
/* harmony export */   "clearNumbering": () => (/* reexport safe */ _common__WEBPACK_IMPORTED_MODULE_0__.clearNumbering),
/* harmony export */   "filterHeadings": () => (/* reexport safe */ _common__WEBPACK_IMPORTED_MODULE_0__.filterHeadings),
/* harmony export */   "getHTMLHeadings": () => (/* reexport safe */ _common__WEBPACK_IMPORTED_MODULE_0__.getHTMLHeadings),
/* harmony export */   "getPrefix": () => (/* reexport safe */ _common__WEBPACK_IMPORTED_MODULE_0__.getPrefix),
/* harmony export */   "isHTML": () => (/* reexport safe */ _common__WEBPACK_IMPORTED_MODULE_0__.isHTML)
/* harmony export */ });
/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./common */ "../packages/toc/lib/utils/common.js");
/* harmony import */ var _markdown__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./markdown */ "../packages/toc/lib/utils/markdown.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




/***/ }),

/***/ "../packages/toc/lib/utils/markdown.js":
/*!*********************************************!*\
  !*** ../packages/toc/lib/utils/markdown.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getHeadingId": () => (/* binding */ getHeadingId),
/* harmony export */   "getHeadings": () => (/* binding */ getHeadings),
/* harmony export */   "isMarkdown": () => (/* binding */ isMarkdown)
/* harmony export */ });
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Build the heading html id.
 *
 * @param raw Raw markdown heading
 * @param level Heading level
 */
async function getHeadingId(parser, raw, level) {
    try {
        const innerHTML = await parser.render(raw);
        if (!innerHTML) {
            return null;
        }
        const container = document.createElement('div');
        container.innerHTML = innerHTML;
        const header = container.querySelector(`h${level}`);
        if (!header) {
            return null;
        }
        return _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_0__.renderMarkdown.createHeaderId(header);
    }
    catch (reason) {
        console.error('Failed to parse a heading.', reason);
    }
    return null;
}
/**
 * Parses the provided string and returns a list of headings.
 *
 * @param text - Input text
 * @returns List of headings
 */
function getHeadings(text) {
    // Split the text into lines:
    const lines = text.split('\n');
    // Iterate over the lines to get the header level and text for each line:
    const headings = new Array();
    let isCodeBlock;
    let lineIdx = 0;
    // Don't check for Markdown headings if in a YAML frontmatter block.
    // We can only start a frontmatter block on the first line of the file.
    // At other positions in a markdown file, '---' represents a horizontal rule.
    if (lines[lineIdx] === '---') {
        // Search for another '---' and treat that as the end of the frontmatter.
        // If we don't find one, treat the file as containing no frontmatter.
        for (let frontmatterEndLineIdx = lineIdx + 1; frontmatterEndLineIdx < lines.length; frontmatterEndLineIdx++) {
            if (lines[frontmatterEndLineIdx] === '---') {
                lineIdx = frontmatterEndLineIdx + 1;
                break;
            }
        }
    }
    for (; lineIdx < lines.length; lineIdx++) {
        const line = lines[lineIdx];
        if (line === '') {
            // Bail early
            continue;
        }
        // Don't check for Markdown headings if in a code block
        if (line.startsWith('```')) {
            isCodeBlock = !isCodeBlock;
        }
        if (isCodeBlock) {
            continue;
        }
        const heading = parseHeading(line, lines[lineIdx + 1]); // append the next line to capture alternative style Markdown headings
        if (heading) {
            headings.push({
                ...heading,
                line: lineIdx
            });
        }
    }
    return headings;
}
const MARKDOWN_MIME_TYPE = [
    'text/x-ipythongfm',
    'text/x-markdown',
    'text/x-gfm',
    'text/markdown'
];
/**
 * Returns whether a MIME type corresponds to a Markdown flavor.
 *
 * @param mime - MIME type string
 * @returns boolean indicating whether a provided MIME type corresponds to a Markdown flavor
 *
 * @example
 * const bool = isMarkdown('text/markdown');
 * // returns true
 *
 * @example
 * const bool = isMarkdown('text/plain');
 * // returns false
 */
function isMarkdown(mime) {
    return MARKDOWN_MIME_TYPE.includes(mime);
}
/**
 * Parses a heading, if one exists, from a provided string.
 *
 * ## Notes
 *
 * -   Heading examples:
 *
 *     -   Markdown heading:
 *
 *         ```
 *         # Foo
 *         ```
 *
 *     -   Markdown heading (alternative style):
 *
 *         ```
 *         Foo
 *         ===
 *         ```
 *
 *         ```
 *         Foo
 *         ---
 *         ```
 *
 *     -   HTML heading:
 *
 *         ```
 *         <h3>Foo</h3>
 *         ```
 *
 * @private
 * @param line - Line to parse
 * @param nextLine - The line after the one to parse
 * @returns heading info
 *
 * @example
 * const out = parseHeading('### Foo\n');
 * // returns {'text': 'Foo', 'level': 3}
 *
 * @example
 * const out = parseHeading('Foo\n===\n');
 * // returns {'text': 'Foo', 'level': 1}
 *
 * @example
 * const out = parseHeading('<h4>Foo</h4>\n');
 * // returns {'text': 'Foo', 'level': 4}
 *
 * @example
 * const out = parseHeading('Foo');
 * // returns null
 */
function parseHeading(line, nextLine) {
    // Case: Markdown heading
    let match = line.match(/^([#]{1,6}) (.*)/);
    if (match) {
        return {
            text: cleanTitle(match[2]),
            level: match[1].length,
            raw: line,
            skip: skipHeading.test(match[0])
        };
    }
    // Case: Markdown heading (alternative style)
    if (nextLine) {
        match = nextLine.match(/^ {0,3}([=]{2,}|[-]{2,})\s*$/);
        if (match) {
            return {
                text: cleanTitle(line),
                level: match[1][0] === '=' ? 1 : 2,
                raw: [line, nextLine].join('\n'),
                skip: skipHeading.test(line)
            };
        }
    }
    // Case: HTML heading (WARNING: this is not particularly robust, as HTML headings can span multiple lines)
    match = line.match(/<h([1-6]).*>(.*)<\/h\1>/i);
    if (match) {
        return {
            text: match[2],
            level: parseInt(match[1], 10),
            skip: skipHeading.test(match[0]),
            raw: line
        };
    }
    return null;
}
function cleanTitle(heading) {
    // take special care to parse Markdown links into raw text
    return heading.replace(/\[(.+)\]\(.+\)/g, '$1');
}
/**
 * Ignore title with html tag with a class name equal to `jp-toc-ignore` or `tocSkip`
 */
const skipHeading = /<\w+\s(.*?\s)?class="(.*?\s)?(jp-toc-ignore|tocSkip)(\s.*?)?"(\s.*?)?>/;


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdG9jX2xpYl9pbmRleF9qcy4xZjU2MWEzMzQ0MDM0MDM5NTlkZC5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBR007QUFNakU7Ozs7R0FJRztBQUNILE1BQU0sY0FBYyxHQUFHLElBQUksQ0FBQztBQUU1Qjs7R0FFRztBQUNJLE1BQWUsc0JBQXNCO0lBSzFDOzs7O09BSUc7SUFDSCxZQUFzQixPQUEwQjtRQUExQixZQUFPLEdBQVAsT0FBTyxDQUFtQjtJQUFHLENBQUM7SUFFcEQ7Ozs7O09BS0c7SUFDSCxZQUFZLENBQUMsTUFBYztRQUN6QixJQUFJLENBQUMsSUFBSSxDQUFDLE9BQU8sQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLEVBQUU7WUFDN0IsT0FBTyxLQUFLLENBQUM7U0FDZDtRQUVELE9BQU8sSUFBSSxDQUFDO0lBQ2QsQ0FBQztJQUVEOzs7Ozs7T0FNRztJQUNILFNBQVMsQ0FDUCxNQUFTLEVBQ1QsYUFBdUM7UUFFdkMsTUFBTSxLQUFLLEdBQUcsSUFBSSxDQUFDLFVBQVUsQ0FBQyxNQUFNLEVBQUUsYUFBYSxDQUFDLENBQUM7UUFFckQsTUFBTSxPQUFPLEdBQUcsTUFBTSxDQUFDLE9BQU8sQ0FBQztRQUUvQixNQUFNLGNBQWMsR0FBRyxHQUFHLEVBQUU7WUFDMUIsS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUMsRUFBRTtnQkFDN0IsT0FBTyxDQUFDLEtBQUssQ0FBQyx5Q0FBeUMsRUFBRSxNQUFNLENBQUMsQ0FBQztZQUNuRSxDQUFDLENBQUMsQ0FBQztRQUNMLENBQUMsQ0FBQztRQUNGLE1BQU0sT0FBTyxHQUFHLElBQUksa0VBQWUsQ0FBQztZQUNsQyxNQUFNLEVBQUUsT0FBTyxDQUFDLEtBQUssQ0FBQyxjQUFjO1lBQ3BDLE9BQU8sRUFBRSxjQUFjO1NBQ3hCLENBQUMsQ0FBQztRQUNILE9BQU8sQ0FBQyxlQUFlLENBQUMsT0FBTyxDQUFD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Q0FBQzthQUM3QixDQUFDO1NBQ0g7S0FDRjtJQUNELDBHQUEwRztJQUMxRyxLQUFLLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQywwQkFBMEIsQ0FBQyxDQUFDO0lBQy9DLElBQUksS0FBSyxFQUFFO1FBQ1QsT0FBTztZQUNMLElBQUksRUFBRSxLQUFLLENBQUMsQ0FBQyxDQUFDO1lBQ2QsS0FBSyxFQUFFLFFBQVEsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLEVBQUUsRUFBRSxDQUFDO1lBQzdCLElBQUksRUFBRSxXQUFXLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQztZQUNoQyxHQUFHLEVBQUUsSUFBSTtTQUNWLENBQUM7S0FDSDtJQUVELE9BQU8sSUFBSSxDQUFDO0FBQ2QsQ0FBQztBQUVELFNBQVMsVUFBVSxDQUFDLE9BQWU7SUFDakMsMERBQTBEO0lBQzFELE9BQU8sT0FBTyxDQUFDLE9BQU8sQ0FBQyxpQkFBaUIsRUFBRSxJQUFJLENBQUMsQ0FBQztBQUNsRCxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLFdBQVcsR0FDZix3RUFBd0UsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90b2Mvc3JjL2ZhY3RvcnkudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvbW9kZWwudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvcGFuZWwudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvcmVnaXN0cnkudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvdG9jaXRlbS50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvdG9jdHJlZS50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90b2Mvc3JjL3RyYWNrZXIudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RvYy9zcmMvdHJlZXZpZXcudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90b2Mvc3JjL3V0aWxzL2NvbW1vbi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdG9jL3NyYy91dGlscy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdG9jL3NyYy91dGlscy9tYXJrZG93bi50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQWN0aXZpdHlNb25pdG9yLCBQYXRoRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBUYWJsZU9mQ29udGVudHNNb2RlbCB9IGZyb20gJy4vbW9kZWwnO1xuaW1wb3J0IHsgVGFibGVPZkNvbnRlbnRzIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIFRpbWVvdXQgZm9yIHRocm90dGxpbmcgVG9DIHJlbmRlcmluZyBmb2xsb3dpbmcgbW9kZWwgY2hhbmdlcy5cbiAqXG4gKiBAcHJpdmF0ZVxuICovXG5jb25zdCBSRU5ERVJfVElNRU9VVCA9IDEwMDA7XG5cbi8qKlxuICogQWJzdHJhY3QgdGFibGUgb2YgY29udGVudHMgbW9kZWwgZmFjdG9yeSBmb3IgSURvY3VtZW50V2lkZ2V0LlxuICovXG5leHBvcnQgYWJzdHJhY3QgY2xhc3MgVGFibGVPZkNvbnRlbnRzRmFjdG9yeTxcbiAgVyBleHRlbmRzIElEb2N1bWVudFdpZGdldCxcbiAgSCBleHRlbmRzIFRhYmxlT2ZDb250ZW50cy5JSGVhZGluZyA9IFRhYmxlT2ZDb250ZW50cy5JSGVhZGluZ1xuPiBpbXBsZW1lbnRzIFRhYmxlT2ZDb250ZW50cy5JRmFjdG9yeTxXLCBIPlxue1xuICAvKipcbiAgICogQ29uc3RydWN0b3JcbiAgICpcbiAgICogQHBhcmFtIHRyYWNrZXIgV2lkZ2V0IHRyYWNrZXJcbiAgICovXG4gIGNvbnN0cnVjdG9yKHByb3RlY3RlZCB0cmFja2VyOiBJV2lkZ2V0VHJhY2tlcjxXPikge31cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgZmFjdG9yeSBjYW4gaGFuZGxlIHRoZSB3aWRnZXQgb3Igbm90LlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gd2lkZ2V0XG4gICAqIEByZXR1cm5zIGJvb2xlYW4gaW5kaWNhdGluZyBhIFRvQyBjYW4gYmUgZ2VuZXJhdGVkXG4gICAqL1xuICBpc0FwcGxpY2FibGUod2lkZ2V0OiBXaWRnZXQpOiBib29sZWFuIHtcbiAgICBpZiAoIXRoaXMudHJhY2tlci5oYXMod2lkZ2V0KSkge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cblxuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCBmb3IgdGhlIHdpZGdldFxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gd2lkZ2V0XG4gICAqIEBwYXJhbSBjb25maWd1cmF0aW9uIC0gVGFibGUgb2YgY29udGVudHMgY29uZmlndXJhdGlvblxuICAgKiBAcmV0dXJucyBUaGUgdGFibGUgb2YgY29udGVudHMgbW9kZWxcbiAgICovXG4gIGNyZWF0ZU5ldyhcbiAgICB3aWRnZXQ6IFcsXG4gICAgY29uZmlndXJhdGlvbj86IFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnXG4gICk6IFRhYmxlT2ZDb250ZW50c01vZGVsPEgsIFc+IHtcbiAgICBjb25zdCBtb2RlbCA9IHRoaXMuX2NyZWF0ZU5ldyh3aWRnZXQsIGNvbmZpZ3VyYXRpb24pO1xuXG4gICAgY29uc3QgY29udGV4dCA9IHdpZGdldC5jb250ZXh0O1xuXG4gICAgY29uc3QgdXBkYXRlSGVhZGluZ3MgPSAoKSA9PiB7XG4gICAgICBtb2RlbC5yZWZyZXNoKCkuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcignRmFpbGVkIHRvIHVwZGF0ZSB0aGUgdGFibGUgb2YgY29udGVudHMuJywgcmVhc29uKTtcbiAgICAgIH0pO1xuICAgIH07XG4gICAgY29uc3QgbW9uaXRvciA9IG5ldyBBY3Rpdml0eU1vbml0b3Ioe1xuICAgICAgc2lnbmFsOiBjb250ZXh0Lm1vZGVsLmNvbnRlbnRDaGFuZ2VkLFxuICAgICAgdGltZW91dDogUkVOREVSX1RJTUVPVVRcbiAgICB9KTtcbiAgICBtb25pdG9yLmFjdGl2aXR5U3RvcHBlZC5jb25uZWN0KHVwZGF0ZUhlYWRpbmdzKTtcblxuICAgIGNvbnN0IHVwZGF0ZVRpdGxlID0gKCkgPT4ge1xuICAgICAgbW9kZWwudGl0bGUgPSBQYXRoRXh0LmJhc2VuYW1lKGNvbnRleHQubG9jYWxQYXRoKTtcbiAgICB9O1xuICAgIGNvbnRleHQucGF0aENoYW5nZWQuY29ubmVjdCh1cGRhdGVUaXRsZSk7XG5cbiAgICBjb250ZXh0LnJlYWR5XG4gICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgIHVwZGF0ZVRpdGxlKCk7XG4gICAgICAgIHVwZGF0ZUhlYWRpbmdzKCk7XG4gICAgICB9KVxuICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgIGNvbnNvbGUuZXJyb3IoYEZhaWxlZCB0byBpbml0aWF0ZSBoZWFkaW5ncyBmb3IgJHtjb250ZXh0LmxvY2FsUGF0aH0uYCk7XG4gICAgICB9KTtcblxuICAgIHdpZGdldC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIG1vbml0b3IuYWN0aXZpdHlTdG9wcGVkLmRpc2Nvbm5lY3QodXBkYXRlSGVhZGluZ3MpO1xuICAgICAgY29udGV4dC5wYXRoQ2hhbmdlZC5kaXNjb25uZWN0KHVwZGF0ZVRpdGxlKTtcbiAgICB9KTtcblxuICAgIHJldHVybiBtb2RlbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBYnN0cmFjdCB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCBpbnN0YW50aWF0aW9uIHRvIGFsbG93XG4gICAqIG92ZXJyaWRlIGJ5IHJlYWwgaW1wbGVtZW50YXRpb24gdG8gY3VzdG9taXplIGl0LiBUaGUgcHVibGljXG4gICAqIGBjcmVhdGVOZXdgIGNvbnRhaW5zIHRoZSBzaWduYWwgY29ubmVjdGlvbnMgc3RhbmRhcmRzIGZvciBJRG9jdW1lbnRXaWRnZXRcbiAgICogd2hlbiB0aGUgbW9kZWwgaGFzIGJlZW4gaW5zdGFudGlhdGVkLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0XG4gICAqIEBwYXJhbSBjb25maWd1cmF0aW9uXG4gICAqL1xuICBwcm90ZWN0ZWQgYWJzdHJhY3QgX2NyZWF0ZU5ldyhcbiAgICB3aWRnZXQ6IFcsXG4gICAgY29uZmlndXJhdGlvbj86IFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnXG4gICk6IFRhYmxlT2ZDb250ZW50c01vZGVsPEgsIFc+O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdG9jXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9mYWN0b3J5JztcbmV4cG9ydCAqIGZyb20gJy4vbW9kZWwnO1xuZXhwb3J0ICogZnJvbSAnLi9wYW5lbCc7XG5leHBvcnQgKiBmcm9tICcuL3JlZ2lzdHJ5JztcbmV4cG9ydCAqIGZyb20gJy4vdHJlZXZpZXcnO1xuZXhwb3J0ICogZnJvbSAnLi90b2NpdGVtJztcbmV4cG9ydCAqIGZyb20gJy4vdG9jdHJlZSc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3RyYWNrZXInO1xuLy8gTmFtZXNwYWNlIHRoZSB1dGlsc1xuZXhwb3J0ICogYXMgVGFibGVPZkNvbnRlbnRzVXRpbHMgZnJvbSAnLi91dGlscyc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFZEb21Nb2RlbCB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgSlNPTkV4dCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBUYWJsZU9mQ29udGVudHMgfSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogQWJzdHJhY3QgdGFibGUgb2YgY29udGVudHMgbW9kZWwuXG4gKi9cbmV4cG9ydCBhYnN0cmFjdCBjbGFzcyBUYWJsZU9mQ29udGVudHNNb2RlbDxcbiAgICBIIGV4dGVuZHMgVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nLFxuICAgIFQgZXh0ZW5kcyBXaWRnZXQgPSBXaWRnZXRcbiAgPlxuICBleHRlbmRzIFZEb21Nb2RlbFxuICBpbXBsZW1lbnRzIFRhYmxlT2ZDb250ZW50cy5JTW9kZWw8SD5cbntcbiAgLyoqXG4gICAqIENvbnN0cnVjdG9yXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgVGhlIHdpZGdldCB0byBzZWFyY2ggaW5cbiAgICogQHBhcmFtIGNvbmZpZ3VyYXRpb24gRGVmYXVsdCBtb2RlbCBjb25maWd1cmF0aW9uXG4gICAqL1xuICBjb25zdHJ1Y3RvcihcbiAgICBwcm90ZWN0ZWQgd2lkZ2V0OiBULFxuICAgIGNvbmZpZ3VyYXRpb24/OiBUYWJsZU9mQ29udGVudHMuSUNvbmZpZ1xuICApIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX2FjdGl2ZUhlYWRpbmcgPSBudWxsO1xuICAgIHRoaXMuX2FjdGl2ZUhlYWRpbmdDaGFuZ2VkID0gbmV3IFNpZ25hbDxcbiAgICAgIFRhYmxlT2ZDb250ZW50c01vZGVsPEgsIFQ+LFxuICAgICAgSCB8IG51bGxcbiAgICA+KHRoaXMpO1xuICAgIHRoaXMuX2NvbGxhcHNlQ2hhbmdlZCA9IG5ldyBTaWduYWw8VGFibGVPZkNvbnRlbnRzTW9kZWw8SCwgVD4sIEg+KHRoaXMpO1xuICAgIHRoaXMuX2NvbmZpZ3VyYXRpb24gPSBjb25maWd1cmF0aW9uID8/IHsgLi4uVGFibGVPZkNvbnRlbnRzLmRlZmF1bHRDb25maWcgfTtcbiAgICB0aGlzLl9oZWFkaW5ncyA9IG5ldyBBcnJheTxIPigpO1xuICAgIHRoaXMuX2hlYWRpbmdzQ2hhbmdlZCA9IG5ldyBTaWduYWw8VGFibGVPZkNvbnRlbnRzTW9kZWw8SCwgVD4sIHZvaWQ+KHRoaXMpO1xuICAgIHRoaXMuX2lzQWN0aXZlID0gZmFsc2U7XG4gICAgdGhpcy5faXNSZWZyZXNoaW5nID0gZmFsc2U7XG4gICAgdGhpcy5fbmVlZHNSZWZyZXNoaW5nID0gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogQ3VycmVudCBhY3RpdmUgZW50cnkuXG4gICAqXG4gICAqIEByZXR1cm5zIHRhYmxlIG9mIGNvbnRlbnRzIGFjdGl2ZSBlbnRyeVxuICAgKi9cbiAgZ2V0IGFjdGl2ZUhlYWRpbmcoKTogSCB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLl9hY3RpdmVIZWFkaW5nO1xuICB9XG5cbiAgLyoqXG4gICAqIFNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGFjdGl2ZSBoZWFkaW5nIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgYWN0aXZlSGVhZGluZ0NoYW5nZWQoKTogSVNpZ25hbDxUYWJsZU9mQ29udGVudHMuSU1vZGVsPEg+LCBIIHwgbnVsbD4ge1xuICAgIHJldHVybiB0aGlzLl9hY3RpdmVIZWFkaW5nQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBTaWduYWwgZW1pdHRlZCB3aGVuIGEgdGFibGUgb2YgY29udGVudCBzZWN0aW9uIGNvbGxhcHNlIHN0YXRlIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY29sbGFwc2VDaGFuZ2VkKCk6IElTaWduYWw8VGFibGVPZkNvbnRlbnRzLklNb2RlbDxIPiwgSCB8IG51bGw+IHtcbiAgICByZXR1cm4gdGhpcy5fY29sbGFwc2VDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIE1vZGVsIGNvbmZpZ3VyYXRpb25cbiAgICovXG4gIGdldCBjb25maWd1cmF0aW9uKCk6IFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnIHtcbiAgICByZXR1cm4gdGhpcy5fY29uZmlndXJhdGlvbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUeXBlIG9mIGRvY3VtZW50IHN1cHBvcnRlZCBieSB0aGUgbW9kZWwuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogQSBgZGF0YS1kb2N1bWVudC10eXBlYCBhdHRyaWJ1dGUgd2l0aCB0aGlzIHZhbHVlIHdpbGwgYmUgc2V0XG4gICAqIG9uIHRoZSB0cmVlIHZpZXcgYC5qcC1UYWJsZU9mQ29udGVudHMtY29udGVudFtkYXRhLWRvY3VtZW50LXR5cGU9XCIuLi5cIl1gXG4gICAqL1xuICBhYnN0cmFjdCByZWFkb25seSBkb2N1bWVudFR5cGU6IHN0cmluZztcblxuICAvKipcbiAgICogTGlzdCBvZiBoZWFkaW5ncy5cbiAgICpcbiAgICogQHJldHVybnMgdGFibGUgb2YgY29udGVudHMgbGlzdCBvZiBoZWFkaW5nc1xuICAgKi9cbiAgZ2V0IGhlYWRpbmdzKCk6IEhbXSB7XG4gICAgcmV0dXJuIHRoaXMuX2hlYWRpbmdzO1xuICB9XG5cbiAgLyoqXG4gICAqIFNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGhlYWRpbmdzIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgaGVhZGluZ3NDaGFuZ2VkKCk6IElTaWduYWw8VGFibGVPZkNvbnRlbnRzLklNb2RlbDxIPiwgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9oZWFkaW5nc0NoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgbW9kZWwgaXMgYWN0aXZlIG9yIG5vdC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBBbiBhY3RpdmUgbW9kZWwgbWVhbnMgaXQgaXMgZGlzcGxheWVkIGluIHRoZSB0YWJsZSBvZiBjb250ZW50cy5cbiAgICogVGhpcyBjYW4gYmUgdXNlZCBieSBzdWJjbGFzcyB0byBsaW1pdCB1cGRhdGluZyB0aGUgaGVhZGluZ3MuXG4gICAqL1xuICBnZXQgaXNBY3RpdmUoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzQWN0aXZlO1xuICB9XG4gIHNldCBpc0FjdGl2ZSh2OiBib29sZWFuKSB7XG4gICAgdGhpcy5faXNBY3RpdmUgPSB2O1xuICAgIC8vIFJlZnJlc2ggb24gYWN0aXZhdGlvbiBleHBlY3QgaWYgaXQgaXMgYWx3YXlzIGFjdGl2ZVxuICAgIC8vICA9PiBhIFRvQyBtb2RlbCBpcyBhbHdheXMgYWN0aXZlIGUuZy4gd2hlbiBkaXNwbGF5aW5nIG51bWJlcmluZyBpbiB0aGUgZG9jdW1lbnRcbiAgICBpZiAodGhpcy5faXNBY3RpdmUgJiYgIXRoaXMuaXNBbHdheXNBY3RpdmUpIHtcbiAgICAgIHRoaXMucmVmcmVzaCgpLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgIGNvbnNvbGUuZXJyb3IoJ0ZhaWxlZCB0byByZWZyZXNoIFRvQyBtb2RlbC4nLCByZWFzb24pO1xuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG1vZGVsIGdldHMgdXBkYXRlZCBldmVuIGlmIHRoZSB0YWJsZSBvZiBjb250ZW50cyBwYW5lbFxuICAgKiBpcyBoaWRkZW4gb3Igbm90LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIEZvciBleGFtcGxlLCBUb0MgbW9kZWxzIHVzZSB0byBhZGQgdGl0bGUgbnVtYmVyaW5nIHdpbGxcbiAgICogc2V0IHRoaXMgdG8gdHJ1ZS5cbiAgICovXG4gIHByb3RlY3RlZCBnZXQgaXNBbHdheXNBY3RpdmUoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG5cbiAgLyoqXG4gICAqIExpc3Qgb2YgY29uZmlndXJhdGlvbiBvcHRpb25zIHN1cHBvcnRlZCBieSB0aGUgbW9kZWwuXG4gICAqL1xuICBnZXQgc3VwcG9ydGVkT3B0aW9ucygpOiAoa2V5b2YgVGFibGVPZkNvbnRlbnRzLklDb25maWcpW10ge1xuICAgIHJldHVybiBbJ21heGltYWxEZXB0aCddO1xuICB9XG5cbiAgLyoqXG4gICAqIERvY3VtZW50IHRpdGxlXG4gICAqL1xuICBnZXQgdGl0bGUoKTogc3RyaW5nIHwgdW5kZWZpbmVkIHtcbiAgICByZXR1cm4gdGhpcy5fdGl0bGU7XG4gIH1cbiAgc2V0IHRpdGxlKHY6IHN0cmluZyB8IHVuZGVmaW5lZCkge1xuICAgIGlmICh2ICE9PSB0aGlzLl90aXRsZSkge1xuICAgICAgdGhpcy5fdGl0bGUgPSB2O1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBYnN0cmFjdCBmdW5jdGlvbiB0aGF0IHdpbGwgcHJvZHVjZSB0aGUgaGVhZGluZ3MgZm9yIGEgZG9jdW1lbnQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBsaXN0IG9mIG5ldyBoZWFkaW5ncyBvciBgbnVsbGAgaWYgbm90aGluZyBuZWVkcyB0byBiZSB1cGRhdGVkLlxuICAgKi9cbiAgcHJvdGVjdGVkIGFic3RyYWN0IGdldEhlYWRpbmdzKCk6IFByb21pc2U8SFtdIHwgbnVsbD47XG5cbiAgLyoqXG4gICAqIFJlZnJlc2ggdGhlIGhlYWRpbmdzIGxpc3QuXG4gICAqL1xuICBhc3luYyByZWZyZXNoKCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGlmICh0aGlzLl9pc1JlZnJlc2hpbmcpIHtcbiAgICAgIC8vIFNjaGVkdWxlIGEgcmVmcmVzaCBpZiBvbmUgaXMgaW4gcHJvZ3Jlc3NcbiAgICAgIHRoaXMuX25lZWRzUmVmcmVzaGluZyA9IHRydWU7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKCk7XG4gICAgfVxuXG4gICAgdGhpcy5faXNSZWZyZXNoaW5nID0gdHJ1ZTtcbiAgICB0cnkge1xuICAgICAgY29uc3QgbmV3SGVhZGluZ3MgPSBhd2FpdCB0aGlzLmdldEhlYWRpbmdzKCk7XG5cbiAgICAgIGlmICh0aGlzLl9uZWVkc1JlZnJlc2hpbmcpIHtcbiAgICAgICAgdGhpcy5fbmVlZHNSZWZyZXNoaW5nID0gZmFsc2U7XG4gICAgICAgIHRoaXMuX2lzUmVmcmVzaGluZyA9IGZhbHNlO1xuICAgICAgICByZXR1cm4gdGhpcy5yZWZyZXNoKCk7XG4gICAgICB9XG5cbiAgICAgIGlmIChcbiAgICAgICAgbmV3SGVhZGluZ3MgJiZcbiAgICAgICAgIVByaXZhdGUuYXJlSGVhZGluZ3NFcXVhbChuZXdIZWFkaW5ncywgdGhpcy5faGVhZGluZ3MpXG4gICAgICApIHtcbiAgICAgICAgdGhpcy5faGVhZGluZ3MgPSBuZXdIZWFkaW5ncztcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgICB0aGlzLl9oZWFkaW5nc0NoYW5nZWQuZW1pdCgpO1xuICAgICAgfVxuICAgIH0gZmluYWxseSB7XG4gICAgICB0aGlzLl9pc1JlZnJlc2hpbmcgPSBmYWxzZTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU2V0IGEgbmV3IGFjdGl2ZSBoZWFkaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gaGVhZGluZyBUaGUgbmV3IGFjdGl2ZSBoZWFkaW5nXG4gICAqIEBwYXJhbSBlbWl0U2lnbmFsIFdoZXRoZXIgdG8gZW1pdCB0aGUgYWN0aXZlSGVhZGluZ0NoYW5nZWQgc2lnbmFsIG9yIG5vdC5cbiAgICovXG4gIHNldEFjdGl2ZUhlYWRpbmcoaGVhZGluZzogSCB8IG51bGwsIGVtaXRTaWduYWwgPSB0cnVlKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2FjdGl2ZUhlYWRpbmcgIT09IGhlYWRpbmcpIHtcbiAgICAgIHRoaXMuX2FjdGl2ZUhlYWRpbmcgPSBoZWFkaW5nO1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgaWYgKGVtaXRTaWduYWwpIHtcbiAgICAgICAgdGhpcy5fYWN0aXZlSGVhZGluZ0NoYW5nZWQuZW1pdChoZWFkaW5nKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogTW9kZWwgY29uZmlndXJhdGlvbiBzZXR0ZXIuXG4gICAqXG4gICAqIEBwYXJhbSBjIE5ldyBjb25maWd1cmF0aW9uXG4gICAqL1xuICBzZXRDb25maWd1cmF0aW9uKGM6IFBhcnRpYWw8VGFibGVPZkNvbnRlbnRzLklDb25maWc+KTogdm9pZCB7XG4gICAgY29uc3QgbmV3Q29uZmlndXJhdGlvbiA9IHsgLi4udGhpcy5fY29uZmlndXJhdGlvbiwgLi4uYyB9O1xuICAgIGlmICghSlNPTkV4dC5kZWVwRXF1YWwodGhpcy5fY29uZmlndXJhdGlvbiwgbmV3Q29uZmlndXJhdGlvbikpIHtcbiAgICAgIHRoaXMuX2NvbmZpZ3VyYXRpb24gPSBuZXdDb25maWd1cmF0aW9uIGFzIFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnO1xuICAgICAgdGhpcy5yZWZyZXNoKCkuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcignRmFpbGVkIHRvIHVwZGF0ZSB0aGUgdGFibGUgb2YgY29udGVudHMuJywgcmVhc29uKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBDYWxsYmFjayBvbiBoZWFkaW5nIGNvbGxhcHNlLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucy5oZWFkaW5nIFRoZSBoZWFkaW5nIHRvIGNoYW5nZSBzdGF0ZSAoYWxsIGhlYWRpbmdzIGlmIG5vdCBwcm92aWRlZClcbiAgICogQHBhcmFtIG9wdGlvbnMuY29sbGFwc2VkIFRoZSBuZXcgY29sbGFwc2VkIHN0YXR1cyAodG9nZ2xlIGV4aXN0aW5nIHN0YXR1cyBpZiBub3QgcHJvdmlkZWQpXG4gICAqL1xuICB0b2dnbGVDb2xsYXBzZShvcHRpb25zOiB7IGhlYWRpbmc/OiBIOyBjb2xsYXBzZWQ/OiBib29sZWFuIH0pOiB2b2lkIHtcbiAgICBpZiAob3B0aW9ucy5oZWFkaW5nKSB7XG4gICAgICBvcHRpb25zLmhlYWRpbmcuY29sbGFwc2VkID1cbiAgICAgICAgb3B0aW9ucy5jb2xsYXBzZWQgPz8gIW9wdGlvbnMuaGVhZGluZy5jb2xsYXBzZWQ7XG4gICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KCk7XG4gICAgICB0aGlzLl9jb2xsYXBzZUNoYW5nZWQuZW1pdChvcHRpb25zLmhlYWRpbmcpO1xuICAgIH0gZWxzZSB7XG4gICAgICAvLyBVc2UgdGhlIHByb3ZpZGVkIHN0YXRlIG9yIGNvbGxhcHNlZCBhbGwgZXhjZXB0IGlmIGFsbCBhcmUgY29sbGFwc2VkXG4gICAgICBjb25zdCBuZXdTdGF0ZSA9XG4gICAgICAgIG9wdGlvbnMuY29sbGFwc2VkID8/ICF0aGlzLmhlYWRpbmdzLnNvbWUoaCA9PiAhKGguY29sbGFwc2VkID8/IGZhbHNlKSk7XG4gICAgICB0aGlzLmhlYWRpbmdzLmZvckVhY2goaCA9PiAoaC5jb2xsYXBzZWQgPSBuZXdTdGF0ZSkpO1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgdGhpcy5fY29sbGFwc2VDaGFuZ2VkLmVtaXQobnVsbCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfYWN0aXZlSGVhZGluZzogSCB8IG51bGw7XG4gIHByaXZhdGUgX2FjdGl2ZUhlYWRpbmdDaGFuZ2VkOiBTaWduYWw8VGFibGVPZkNvbnRlbnRzTW9kZWw8SCwgVD4sIEggfCBudWxsPjtcbiAgcHJpdmF0ZSBfY29sbGFwc2VDaGFuZ2VkOiBTaWduYWw8VGFibGVPZkNvbnRlbnRzTW9kZWw8SCwgVD4sIEggfCBudWxsPjtcbiAgcHJpdmF0ZSBfY29uZmlndXJhdGlvbjogVGFibGVPZkNvbnRlbnRzLklDb25maWc7XG4gIHByaXZhdGUgX2hlYWRpbmdzOiBIW107XG4gIHByaXZhdGUgX2hlYWRpbmdzQ2hhbmdlZDogU2lnbmFsPFRhYmxlT2ZDb250ZW50c01vZGVsPEgsIFQ+LCB2b2lkPjtcbiAgcHJpdmF0ZSBfaXNBY3RpdmU6IGJvb2xlYW47XG4gIHByaXZhdGUgX2lzUmVmcmVzaGluZzogYm9vbGVhbjtcbiAgcHJpdmF0ZSBfbmVlZHNSZWZyZXNoaW5nOiBib29sZWFuO1xuICBwcml2YXRlIF90aXRsZT86IHN0cmluZztcbn1cblxuLyoqXG4gKiBQcml2YXRlIGZ1bmN0aW9ucyBuYW1lc3BhY2VcbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogVGVzdCBpZiB0d28gbGlzdCBvZiBoZWFkaW5ncyBhcmUgZXF1YWwgb3Igbm90LlxuICAgKlxuICAgKiBAcGFyYW0gaGVhZGluZ3MxIEZpcnN0IGxpc3Qgb2YgaGVhZGluZ3NcbiAgICogQHBhcmFtIGhlYWRpbmdzMiBTZWNvbmQgbGlzdCBvZiBoZWFkaW5nc1xuICAgKiBAcmV0dXJucyBXaGV0aGVyIHRoZSBhcnJheSBhcmUgaWRlbnRpY2FsIG9yIG5vdC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhcmVIZWFkaW5nc0VxdWFsKFxuICAgIGhlYWRpbmdzMTogVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nW10sXG4gICAgaGVhZGluZ3MyOiBUYWJsZU9mQ29udGVudHMuSUhlYWRpbmdbXVxuICApOiBib29sZWFuIHtcbiAgICBpZiAoaGVhZGluZ3MxLmxlbmd0aCA9PT0gaGVhZGluZ3MyLmxlbmd0aCkge1xuICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBoZWFkaW5nczEubGVuZ3RoOyBpKyspIHtcbiAgICAgICAgaWYgKFxuICAgICAgICAgIGhlYWRpbmdzMVtpXS5sZXZlbCAhPT0gaGVhZGluZ3MyW2ldLmxldmVsIHx8XG4gICAgICAgICAgaGVhZGluZ3MxW2ldLnRleHQgIT09IGhlYWRpbmdzMltpXS50ZXh0IHx8XG4gICAgICAgICAgaGVhZGluZ3MxW2ldLnByZWZpeCAhPT0gaGVhZGluZ3MyW2ldLnByZWZpeFxuICAgICAgICApIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cblxuICAgIHJldHVybiBmYWxzZTtcbiAgfVxufVxuIiwiLypcbiAqIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuICogRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbiAqL1xuXG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFNpZGVQYW5lbCB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgUGFuZWwsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBUYWJsZU9mQ29udGVudHNXaWRnZXQgfSBmcm9tICcuL3RyZWV2aWV3JztcbmltcG9ydCB7IFRhYmxlT2ZDb250ZW50cyB9IGZyb20gJy4vdG9rZW5zJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudHMgc2lkZWJhciBwYW5lbC5cbiAqL1xuZXhwb3J0IGNsYXNzIFRhYmxlT2ZDb250ZW50c1BhbmVsIGV4dGVuZHMgU2lkZVBhbmVsIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdG9yXG4gICAqXG4gICAqIEBwYXJhbSB0cmFuc2xhdG9yIC0gVHJhbnNsYXRvciB0b29sXG4gICAqL1xuICBjb25zdHJ1Y3Rvcih0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3IpIHtcbiAgICBzdXBlcih7IGNvbnRlbnQ6IG5ldyBQYW5lbCgpLCB0cmFuc2xhdG9yIH0pO1xuICAgIHRoaXMuX21vZGVsID0gbnVsbDtcblxuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVRhYmxlT2ZDb250ZW50cycpO1xuXG4gICAgdGhpcy5fdGl0bGUgPSBuZXcgUHJpdmF0ZS5IZWFkZXIodGhpcy5fdHJhbnMuX18oJ1RhYmxlIG9mIENvbnRlbnRzJykpO1xuICAgIHRoaXMuaGVhZGVyLmFkZFdpZGdldCh0aGlzLl90aXRsZSk7XG5cbiAgICB0aGlzLl90cmVldmlldyA9IG5ldyBUYWJsZU9mQ29udGVudHNXaWRnZXQoe1xuICAgICAgcGxhY2Vob2xkZXJIZWFkbGluZTogdGhpcy5fdHJhbnMuX18oJ05vIEhlYWRpbmdzJyksXG4gICAgICBwbGFjZWhvbGRlclRleHQ6IHRoaXMuX3RyYW5zLl9fKFxuICAgICAgICAnVGhlIHRhYmxlIG9mIGNvbnRlbnRzIHNob3dzIGhlYWRpbmdzIGluIG5vdGVib29rcyBhbmQgc3VwcG9ydGVkIGZpbGVzLidcbiAgICAgIClcbiAgICB9KTtcbiAgICB0aGlzLl90cmVldmlldy5hZGRDbGFzcygnanAtVGFibGVPZkNvbnRlbnRzLXRyZWUnKTtcbiAgICB0aGlzLmNvbnRlbnQuYWRkV2lkZ2V0KHRoaXMuX3RyZWV2aWV3KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGN1cnJlbnQgbW9kZWwuXG4gICAqL1xuICBnZXQgbW9kZWwoKTogVGFibGVPZkNvbnRlbnRzLk1vZGVsIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX21vZGVsO1xuICB9XG4gIHNldCBtb2RlbChuZXdWYWx1ZTogVGFibGVPZkNvbnRlbnRzLk1vZGVsIHwgbnVsbCkge1xuICAgIGlmICh0aGlzLl9tb2RlbCAhPT0gbmV3VmFsdWUpIHtcbiAgICAgIHRoaXMuX21vZGVsPy5zdGF0ZUNoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl9vblRpdGxlQ2hhbmdlZCwgdGhpcyk7XG5cbiAgICAgIHRoaXMuX21vZGVsID0gbmV3VmFsdWU7XG4gICAgICBpZiAodGhpcy5fbW9kZWwpIHtcbiAgICAgICAgdGhpcy5fbW9kZWwuaXNBY3RpdmUgPSB0aGlzLmlzVmlzaWJsZTtcbiAgICAgIH1cblxuICAgICAgdGhpcy5fbW9kZWw/LnN0YXRlQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uVGl0bGVDaGFuZ2VkLCB0aGlzKTtcbiAgICAgIHRoaXMuX29uVGl0bGVDaGFuZ2VkKCk7XG5cbiAgICAgIHRoaXMuX3RyZWV2aWV3Lm1vZGVsID0gdGhpcy5fbW9kZWw7XG4gICAgfVxuICB9XG5cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJIaWRlKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHN1cGVyLm9uQWZ0ZXJIaWRlKG1zZyk7XG4gICAgaWYgKHRoaXMuX21vZGVsKSB7XG4gICAgICB0aGlzLl9tb2RlbC5pc0FjdGl2ZSA9IGZhbHNlO1xuICAgIH1cbiAgfVxuXG4gIHByb3RlY3RlZCBvbkJlZm9yZVNob3cobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgc3VwZXIub25CZWZvcmVTaG93KG1zZyk7XG4gICAgaWYgKHRoaXMuX21vZGVsKSB7XG4gICAgICB0aGlzLl9tb2RlbC5pc0FjdGl2ZSA9IHRydWU7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfb25UaXRsZUNoYW5nZWQoKTogdm9pZCB7XG4gICAgdGhpcy5fdGl0bGUuc2V0VGl0bGUoXG4gICAgICB0aGlzLl9tb2RlbD8udGl0bGUgPz8gdGhpcy5fdHJhbnMuX18oJ1RhYmxlIG9mIENvbnRlbnRzJylcbiAgICApO1xuICB9XG5cbiAgcHJpdmF0ZSBfbW9kZWw6IFRhYmxlT2ZDb250ZW50cy5Nb2RlbCB8IG51bGw7XG4gIHByaXZhdGUgX3RpdGxlOiBQcml2YXRlLkhlYWRlcjtcbiAgcHJpdmF0ZSBfdHJlZXZpZXc6IFRhYmxlT2ZDb250ZW50c1dpZGdldDtcbn1cblxuLyoqXG4gKiBQcml2YXRlIGhlbHBlcnMgbmFtZXNwYWNlXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIFBhbmVsIGhlYWRlclxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIEhlYWRlciBleHRlbmRzIFdpZGdldCB7XG4gICAgLyoqXG4gICAgICogQ29uc3RydWN0b3JcbiAgICAgKlxuICAgICAqIEBwYXJhbSB0aXRsZSAtIFRpdGxlIHRleHRcbiAgICAgKi9cbiAgICBjb25zdHJ1Y3Rvcih0aXRsZTogc3RyaW5nKSB7XG4gICAgICBjb25zdCBub2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaDInKTtcbiAgICAgIG5vZGUudGV4dENvbnRlbnQgPSB0aXRsZTtcbiAgICAgIG5vZGUuY2xhc3NMaXN0LmFkZCgnanAtdGV4dC10cnVuY2F0ZWQnKTtcbiAgICAgIHN1cGVyKHsgbm9kZSB9KTtcbiAgICAgIHRoaXMuX3RpdGxlID0gbm9kZTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBTZXQgdGhlIGhlYWRlciB0aXRsZS5cbiAgICAgKi9cbiAgICBzZXRUaXRsZSh0aXRsZTogc3RyaW5nKTogdm9pZCB7XG4gICAgICB0aGlzLl90aXRsZS50ZXh0Q29udGVudCA9IHRpdGxlO1xuICAgIH1cblxuICAgIHByaXZhdGUgX3RpdGxlOiBIVE1MRWxlbWVudDtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBEaXNwb3NhYmxlRGVsZWdhdGUsIElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBJVGFibGVPZkNvbnRlbnRzUmVnaXN0cnksIFRhYmxlT2ZDb250ZW50cyB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBDbGFzcyBmb3IgcmVnaXN0ZXJpbmcgdGFibGUgb2YgY29udGVudHMgZ2VuZXJhdG9ycy5cbiAqL1xuZXhwb3J0IGNsYXNzIFRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5IGltcGxlbWVudHMgSVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5IHtcbiAgLyoqXG4gICAqIEZpbmRzIGEgdGFibGUgb2YgY29udGVudHMgbW9kZWwgZm9yIGEgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyBOb3Rlc1xuICAgKlxuICAgKiAtICAgSWYgdW5hYmxlIHRvIGZpbmQgYSB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCwgdGhlIG1ldGhvZCByZXR1cm4gYHVuZGVmaW5lZGAuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgLSB3aWRnZXRcbiAgICogQHBhcmFtIGNvbmZpZ3VyYXRpb24gLSBEZWZhdWx0IG1vZGVsIGNvbmZpZ3VyYXRpb25cbiAgICogQHJldHVybnMgVGFibGUgb2YgY29udGVudHMgbW9kZWxcbiAgICovXG4gIGdldE1vZGVsKFxuICAgIHdpZGdldDogV2lkZ2V0LFxuICAgIGNvbmZpZ3VyYXRpb24/OiBUYWJsZU9mQ29udGVudHMuSUNvbmZpZ1xuICApOiBUYWJsZU9mQ29udGVudHMuTW9kZWwgfCB1bmRlZmluZWQge1xuICAgIGZvciAoY29uc3QgZ2VuZXJhdG9yIG9mIHRoaXMuX2dlbmVyYXRvcnMudmFsdWVzKCkpIHtcbiAgICAgIGlmIChnZW5lcmF0b3IuaXNBcHBsaWNhYmxlKHdpZGdldCkpIHtcbiAgICAgICAgcmV0dXJuIGdlbmVyYXRvci5jcmVhdGVOZXcod2lkZ2V0LCBjb25maWd1cmF0aW9uKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQWRkcyBhIHRhYmxlIG9mIGNvbnRlbnRzIGdlbmVyYXRvciB0byB0aGUgcmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBnZW5lcmF0b3IgLSB0YWJsZSBvZiBjb250ZW50cyBnZW5lcmF0b3JcbiAgICovXG4gIGFkZChnZW5lcmF0b3I6IFRhYmxlT2ZDb250ZW50cy5JRmFjdG9yeSk6IElEaXNwb3NhYmxlIHtcbiAgICBjb25zdCBpZCA9IHRoaXMuX2lkQ291bnRlcisrO1xuICAgIHRoaXMuX2dlbmVyYXRvcnMuc2V0KGlkLCBnZW5lcmF0b3IpO1xuXG4gICAgcmV0dXJuIG5ldyBEaXNwb3NhYmxlRGVsZWdhdGUoKCkgPT4ge1xuICAgICAgdGhpcy5fZ2VuZXJhdG9ycy5kZWxldGUoaWQpO1xuICAgIH0pO1xuICB9XG5cbiAgcHJpdmF0ZSBfZ2VuZXJhdG9ycyA9IG5ldyBNYXA8bnVtYmVyLCBUYWJsZU9mQ29udGVudHMuSUZhY3Rvcnk+KCk7XG4gIHByaXZhdGUgX2lkQ291bnRlciA9IDA7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IGNhcmV0RG93bkljb24sIGNhcmV0UmlnaHRJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBUYWJsZU9mQ29udGVudHMgfSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogSW50ZXJmYWNlIGRlc2NyaWJpbmcgY29tcG9uZW50IHByb3BlcnRpZXMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVRhYmxlT2ZDb250ZW50c0l0ZW1zUHJvcHMge1xuICAvKipcbiAgICogV2hldGhlciB0aGlzIGl0ZW0gaXMgYWN0aXZlIG9yIG5vdC5cbiAgICovXG4gIGlzQWN0aXZlOiBib29sZWFuO1xuICAvKipcbiAgICogSGVhZGluZyB0byByZW5kZXIuXG4gICAqL1xuICBoZWFkaW5nOiBUYWJsZU9mQ29udGVudHMuSUhlYWRpbmc7XG5cbiAgLyoqXG4gICAqIE9uIGBtb3VzZS1kb3duYCBldmVudCBjYWxsYmFjay5cbiAgICovXG4gIG9uTW91c2VEb3duOiAoaGVhZGluZzogVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nKSA9PiB2b2lkO1xuXG4gIC8qKlxuICAgKiBDb2xsYXBzZSBldmVudCBjYWxsYmFjay5cbiAgICovXG4gIG9uQ29sbGFwc2U6IChoZWFkaW5nOiBUYWJsZU9mQ29udGVudHMuSUhlYWRpbmcpID0+IHZvaWQ7XG59XG5cbi8qKlxuICogUmVhY3QgY29tcG9uZW50IGZvciBhIHRhYmxlIG9mIGNvbnRlbnRzIGVudHJ5LlxuICovXG5leHBvcnQgY2xhc3MgVGFibGVPZkNvbnRlbnRzSXRlbSBleHRlbmRzIFJlYWN0LlB1cmVDb21wb25lbnQ8XG4gIFJlYWN0LlByb3BzV2l0aENoaWxkcmVuPElUYWJsZU9mQ29udGVudHNJdGVtc1Byb3BzPlxuPiB7XG4gIC8qKlxuICAgKiBSZW5kZXJzIGEgdGFibGUgb2YgY29udGVudHMgZW50cnkuXG4gICAqXG4gICAqIEByZXR1cm5zIHJlbmRlcmVkIGVudHJ5XG4gICAqL1xuICByZW5kZXIoKTogSlNYLkVsZW1lbnQgfCBudWxsIHtcbiAgICBjb25zdCB7IGNoaWxkcmVuLCBpc0FjdGl2ZSwgaGVhZGluZywgb25Db2xsYXBzZSwgb25Nb3VzZURvd24gfSA9IHRoaXMucHJvcHM7XG5cbiAgICByZXR1cm4gKFxuICAgICAgPGxpIGNsYXNzTmFtZT1cImpwLXRvY0l0ZW1cIj5cbiAgICAgICAgPGRpdlxuICAgICAgICAgIGNsYXNzTmFtZT17YGpwLXRvY0l0ZW0taGVhZGluZyAke1xuICAgICAgICAgICAgaXNBY3RpdmUgPyAnanAtdG9jSXRlbS1hY3RpdmUnIDogJydcbiAgICAgICAgICB9YH1cbiAgICAgICAgICBvbk1vdXNlRG93bj17KGV2ZW50OiBSZWFjdC5TeW50aGV0aWNFdmVudDxIVE1MRGl2RWxlbWVudD4pID0+IHtcbiAgICAgICAgICAgIC8vIFJlYWN0IG9ubHkgb24gZGVlcGVzdCBpdGVtXG4gICAgICAgICAgICBpZiAoIWV2ZW50LmRlZmF1bHRQcmV2ZW50ZWQpIHtcbiAgICAgICAgICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgICAgICAgb25Nb3VzZURvd24oaGVhZGluZyk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfX1cbiAgICAgICAgPlxuICAgICAgICAgIDxidXR0b25cbiAgICAgICAgICAgIGNsYXNzTmFtZT1cImpwLXRvY0l0ZW0tY29sbGFwc2VyXCJcbiAgICAgICAgICAgIG9uQ2xpY2s9eyhldmVudDogUmVhY3QuTW91c2VFdmVudCkgPT4ge1xuICAgICAgICAgICAgICBldmVudC5wcmV2ZW50RGVmYXVsdCgpO1xuICAgICAgICAgICAgICBvbkNvbGxhcHNlKGhlYWRpbmcpO1xuICAgICAgICAgICAgfX1cbiAgICAgICAgICAgIHN0eWxlPXt7IHZpc2liaWxpdHk6IGNoaWxkcmVuID8gJ3Zpc2libGUnIDogJ2hpZGRlbicgfX1cbiAgICAgICAgICA+XG4gICAgICAgICAgICB7aGVhZGluZy5jb2xsYXBzZWQgPyAoXG4gICAgICAgICAgICAgIDxjYXJldFJpZ2h0SWNvbi5yZWFjdCB0YWc9XCJzcGFuXCIgd2lkdGg9XCIyMHB4XCIgLz5cbiAgICAgICAgICAgICkgOiAoXG4gICAgICAgICAgICAgIDxjYXJldERvd25JY29uLnJlYWN0IHRhZz1cInNwYW5cIiB3aWR0aD1cIjIwcHhcIiAvPlxuICAgICAgICAgICAgKX1cbiAgICAgICAgICA8L2J1dHRvbj5cbiAgICAgICAgICA8c3BhblxuICAgICAgICAgICAgY2xhc3NOYW1lPVwianAtdG9jSXRlbS1jb250ZW50XCJcbiAgICAgICAgICAgIHRpdGxlPXtoZWFkaW5nLnRleHR9XG4gICAgICAgICAgICB7Li4uaGVhZGluZy5kYXRhc2V0fVxuICAgICAgICAgID5cbiAgICAgICAgICAgIHtoZWFkaW5nLnByZWZpeH1cbiAgICAgICAgICAgIHtoZWFkaW5nLnRleHR9XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICAge2NoaWxkcmVuICYmICFoZWFkaW5nLmNvbGxhcHNlZCAmJiA8b2w+e2NoaWxkcmVufTwvb2w+fVxuICAgICAgPC9saT5cbiAgICApO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IFRhYmxlT2ZDb250ZW50c0l0ZW0gfSBmcm9tICcuL3RvY2l0ZW0nO1xuaW1wb3J0IHsgVGFibGVPZkNvbnRlbnRzIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEludGVyZmFjZSBkZXNjcmliaW5nIGNvbXBvbmVudCBwcm9wZXJ0aWVzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElUYWJsZU9mQ29udGVudHNUcmVlUHJvcHMge1xuICAvKipcbiAgICogQ3VycmVudGx5IGFjdGl2ZSBoZWFkaW5nLlxuICAgKi9cbiAgYWN0aXZlSGVhZGluZzogVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nIHwgbnVsbDtcbiAgLyoqXG4gICAqIFR5cGUgb2YgZG9jdW1lbnQgc3VwcG9ydGVkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIGRvY3VtZW50VHlwZTogc3RyaW5nO1xuICAvKipcbiAgICogTGlzdCBvZiBoZWFkaW5ncyB0byByZW5kZXIuXG4gICAqL1xuICBoZWFkaW5nczogVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nW107XG4gIC8qKlxuICAgKiBTZXQgYWN0aXZlIGhlYWRpbmcuXG4gICAqL1xuICBzZXRBY3RpdmVIZWFkaW5nOiAoaGVhZGluZzogVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nKSA9PiB2b2lkO1xuICAvKipcbiAgICogQ29sbGFwc2UgaGVhZGluZyBjYWxsYmFjay5cbiAgICovXG4gIG9uQ29sbGFwc2VDaGFuZ2U6IChoZWFkaW5nOiBUYWJsZU9mQ29udGVudHMuSUhlYWRpbmcpID0+IHZvaWQ7XG59XG5cbi8qKlxuICogUmVhY3QgY29tcG9uZW50IGZvciBhIHRhYmxlIG9mIGNvbnRlbnRzIHRyZWUuXG4gKi9cbmV4cG9ydCBjbGFzcyBUYWJsZU9mQ29udGVudHNUcmVlIGV4dGVuZHMgUmVhY3QuUHVyZUNvbXBvbmVudDxJVGFibGVPZkNvbnRlbnRzVHJlZVByb3BzPiB7XG4gIC8qKlxuICAgKiBSZW5kZXJzIGEgdGFibGUgb2YgY29udGVudHMgdHJlZS5cbiAgICovXG4gIHJlbmRlcigpOiBKU1guRWxlbWVudCB7XG4gICAgY29uc3QgeyBkb2N1bWVudFR5cGUgfSA9IHRoaXMucHJvcHM7XG4gICAgcmV0dXJuIChcbiAgICAgIDxvbFxuICAgICAgICBjbGFzc05hbWU9XCJqcC1UYWJsZU9mQ29udGVudHMtY29udGVudFwiXG4gICAgICAgIHsuLi57ICdkYXRhLWRvY3VtZW50LXR5cGUnOiBkb2N1bWVudFR5cGUgfX1cbiAgICAgID5cbiAgICAgICAge3RoaXMuYnVpbGRUcmVlKCl9XG4gICAgICA8L29sPlxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQ29udmVydCB0aGUgZmxhdCBoZWFkaW5ncyBsaXN0IHRvIGEgbmVzdGVkIHRyZWUgbGlzdFxuICAgKi9cbiAgcHJvdGVjdGVkIGJ1aWxkVHJlZSgpOiBKU1guRWxlbWVudFtdIHtcbiAgICBpZiAodGhpcy5wcm9wcy5oZWFkaW5ncy5sZW5ndGggPT09IDApIHtcbiAgICAgIHJldHVybiBbXTtcbiAgICB9XG5cbiAgICBjb25zdCBidWlsZE9uZVRyZWUgPSAoY3VycmVudEluZGV4OiBudW1iZXIpOiBbSlNYLkVsZW1lbnQsIG51bWJlcl0gPT4ge1xuICAgICAgY29uc3QgaXRlbXMgPSB0aGlzLnByb3BzLmhlYWRpbmdzO1xuICAgICAgY29uc3QgY2hpbGRyZW4gPSBuZXcgQXJyYXk8SlNYLkVsZW1lbnQ+KCk7XG4gICAgICBjb25zdCBjdXJyZW50ID0gaXRlbXNbY3VycmVudEluZGV4XTtcbiAgICAgIGxldCBuZXh0Q2FuZGlkYXRlSW5kZXggPSBjdXJyZW50SW5kZXggKyAxO1xuXG4gICAgICB3aGlsZSAobmV4dENhbmRpZGF0ZUluZGV4IDwgaXRlbXMubGVuZ3RoKSB7XG4gICAgICAgIGNvbnN0IGNhbmRpZGF0ZUl0ZW0gPSBpdGVtc1tuZXh0Q2FuZGlkYXRlSW5kZXhdO1xuICAgICAgICBpZiAoY2FuZGlkYXRlSXRlbS5sZXZlbCA8PSBjdXJyZW50LmxldmVsKSB7XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgW2NoaWxkLCBuZXh0SW5kZXhdID0gYnVpbGRPbmVUcmVlKG5leHRDYW5kaWRhdGVJbmRleCk7XG4gICAgICAgIGNoaWxkcmVuLnB1c2goY2hpbGQpO1xuICAgICAgICBuZXh0Q2FuZGlkYXRlSW5kZXggPSBuZXh0SW5kZXg7XG4gICAgICB9XG4gICAgICBjb25zdCBjdXJyZW50VHJlZSA9IChcbiAgICAgICAgPFRhYmxlT2ZDb250ZW50c0l0ZW1cbiAgICAgICAgICBrZXk9e2Ake2N1cnJlbnQubGV2ZWx9LSR7Y3VycmVudEluZGV4fS0ke2N1cnJlbnQudGV4dH1gfVxuICAgICAgICAgIGlzQWN0aXZlPXtcbiAgICAgICAgICAgICEhdGhpcy5wcm9wcy5hY3RpdmVIZWFkaW5nICYmIGN1cnJlbnQgPT09IHRoaXMucHJvcHMuYWN0aXZlSGVhZGluZ1xuICAgICAgICAgIH1cbiAgICAgICAgICBoZWFkaW5nPXtjdXJyZW50fVxuICAgICAgICAgIG9uTW91c2VEb3duPXt0aGlzLnByb3BzLnNldEFjdGl2ZUhlYWRpbmd9XG4gICAgICAgICAgb25Db2xsYXBzZT17dGhpcy5wcm9wcy5vbkNvbGxhcHNlQ2hhbmdlfVxuICAgICAgICA+XG4gICAgICAgICAge2NoaWxkcmVuLmxlbmd0aCA/IGNoaWxkcmVuIDogbnVsbH1cbiAgICAgICAgPC9UYWJsZU9mQ29udGVudHNJdGVtPlxuICAgICAgKTtcbiAgICAgIHJldHVybiBbY3VycmVudFRyZWUsIG5leHRDYW5kaWRhdGVJbmRleF07XG4gICAgfTtcblxuICAgIGNvbnN0IHRyZWVzID0gbmV3IEFycmF5PEpTWC5FbGVtZW50PigpO1xuICAgIGxldCBjdXJyZW50SW5kZXggPSAwO1xuICAgIHdoaWxlIChjdXJyZW50SW5kZXggPCB0aGlzLnByb3BzLmhlYWRpbmdzLmxlbmd0aCkge1xuICAgICAgY29uc3QgW3RyZWUsIG5leHRJbmRleF0gPSBidWlsZE9uZVRyZWUoY3VycmVudEluZGV4KTtcbiAgICAgIHRyZWVzLnB1c2godHJlZSk7XG4gICAgICBjdXJyZW50SW5kZXggPSBuZXh0SW5kZXg7XG4gICAgfVxuXG4gICAgcmV0dXJuIHRyZWVzO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB0eXBlIHsgVG9vbGJhclJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHR5cGUgeyBJT2JzZXJ2YWJsZUxpc3QgfSBmcm9tICdAanVweXRlcmxhYi9vYnNlcnZhYmxlcyc7XG5pbXBvcnQgdHlwZSB7IFZEb21SZW5kZXJlciB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHR5cGUgeyBKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgdHlwZSB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB0eXBlIHsgSVNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB0eXBlIHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBJbnRlcmZhY2UgZGVzY3JpYmluZyB0aGUgdGFibGUgb2YgY29udGVudHMgcmVnaXN0cnkuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5IHtcbiAgLyoqXG4gICAqIEZpbmRzIGEgdGFibGUgb2YgY29udGVudHMgbW9kZWwgZm9yIGEgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyBOb3Rlc1xuICAgKlxuICAgKiAtICAgSWYgdW5hYmxlIHRvIGZpbmQgYSB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCwgdGhlIG1ldGhvZCByZXR1cm4gYHVuZGVmaW5lZGAuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgLSB3aWRnZXRcbiAgICogQHBhcmFtIGNvbmZpZ3VyYXRpb24gLSBUYWJsZSBvZiBjb250ZW50cyBjb25maWd1cmF0aW9uXG4gICAqIEByZXR1cm5zIFRhYmxlIG9mIGNvbnRlbnRzIG1vZGVsIG9yIHVuZGVmaW5lZCBpZiBub3QgZm91bmRcbiAgICovXG4gIGdldE1vZGVsKFxuICAgIHdpZGdldDogV2lkZ2V0LFxuICAgIGNvbmZpZ3VyYXRpb24/OiBUYWJsZU9mQ29udGVudHMuSUNvbmZpZ1xuICApOiBUYWJsZU9mQ29udGVudHMuTW9kZWwgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIEFkZHMgYSB0YWJsZSBvZiBjb250ZW50cyBmYWN0b3J5IHRvIHRoZSByZWdpc3RyeS5cbiAgICpcbiAgICogQHBhcmFtIGZhY3RvcnkgLSB0YWJsZSBvZiBjb250ZW50cyBmYWN0b3J5XG4gICAqL1xuICBhZGQoZmFjdG9yeTogVGFibGVPZkNvbnRlbnRzLklGYWN0b3J5KTogSURpc3Bvc2FibGU7XG59XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudHMgcmVnaXN0cnkgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJVGFibGVPZkNvbnRlbnRzUmVnaXN0cnkgPSBuZXcgVG9rZW48SVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5PihcbiAgJ0BqdXB5dGVybGFiL3RvYzpJVGFibGVPZkNvbnRlbnRzUmVnaXN0cnknLFxuICAnQSBzZXJ2aWNlIHRvIHJlZ2lzdGVyIHRhYmxlIG9mIGNvbnRlbnQgZmFjdG9yeS4nXG4pO1xuXG4vKipcbiAqIEludGVyZmFjZSBmb3IgdGhlIHRhYmxlIG9mIGNvbnRlbnRzIHRyYWNrZXJcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJVGFibGVPZkNvbnRlbnRzVHJhY2tlciB7XG4gIC8qKlxuICAgKiBHZXQgdGhlIG1vZGVsIGFzc29jaWF0ZWQgd2l0aCBhIGdpdmVuIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCBXaWRnZXRcbiAgICovXG4gIGdldCh3aWRnZXQ6IFdpZGdldCk6IFRhYmxlT2ZDb250ZW50cy5JTW9kZWw8VGFibGVPZkNvbnRlbnRzLklIZWFkaW5nPiB8IG51bGw7XG59XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudHMgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElUYWJsZU9mQ29udGVudHNUcmFja2VyID0gbmV3IFRva2VuPElUYWJsZU9mQ29udGVudHNUcmFja2VyPihcbiAgJ0BqdXB5dGVybGFiL3RvYzpJVGFibGVPZkNvbnRlbnRzVHJhY2tlcicsXG4gICdBIHdpZGdldCB0cmFja2VyIGZvciB0YWJsZSBvZiBjb250ZW50cy4nXG4pO1xuXG4vKipcbiAqIE5hbWVzcGFjZSBmb3IgdGFibGUgb2YgY29udGVudHMgaW50ZXJmYWNlXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgVGFibGVPZkNvbnRlbnRzIHtcbiAgLyoqXG4gICAqIFRhYmxlIG9mIGNvbnRlbnQgbW9kZWwgZmFjdG9yeSBpbnRlcmZhY2VcbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUZhY3Rvcnk8XG4gICAgVyBleHRlbmRzIFdpZGdldCA9IFdpZGdldCxcbiAgICBIIGV4dGVuZHMgSUhlYWRpbmcgPSBJSGVhZGluZ1xuICA+IHtcbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBmYWN0b3J5IGNhbiBoYW5kbGUgdGhlIHdpZGdldCBvciBub3QuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gd2lkZ2V0IC0gd2lkZ2V0XG4gICAgICogQHJldHVybnMgYm9vbGVhbiBpbmRpY2F0aW5nIGEgVG9DIGNhbiBiZSBnZW5lcmF0ZWRcbiAgICAgKi9cbiAgICBpc0FwcGxpY2FibGU6ICh3aWRnZXQ6IFcpID0+IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgdGFibGUgb2YgY29udGVudHMgbW9kZWwgZm9yIHRoZSB3aWRnZXRcbiAgICAgKlxuICAgICAqIEBwYXJhbSB3aWRnZXQgLSB3aWRnZXRcbiAgICAgKiBAcGFyYW0gY29uZmlndXJhdGlvbiAtIFRhYmxlIG9mIGNvbnRlbnRzIGNvbmZpZ3VyYXRpb25cbiAgICAgKiBAcmV0dXJucyBUaGUgdGFibGUgb2YgY29udGVudHMgbW9kZWxcbiAgICAgKi9cbiAgICBjcmVhdGVOZXc6IChcbiAgICAgIHdpZGdldDogVyxcbiAgICAgIGNvbmZpZ3VyYXRpb24/OiBUYWJsZU9mQ29udGVudHMuSUNvbmZpZ1xuICAgICkgPT4gSU1vZGVsPEg+O1xuICB9XG5cbiAgLyoqXG4gICAqIFRhYmxlIG9mIENvbnRlbnRzIGNvbmZpZ3VyYXRpb25cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBBIGRvY3VtZW50IG1vZGVsIG1heSBpZ25vcmUgc29tZSBvZiB0aG9zZSBvcHRpb25zLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29uZmlnIGV4dGVuZHMgSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogQmFzZSBsZXZlbCBmb3IgdGhlIGhpZ2hlc3QgaGVhZGluZ3NcbiAgICAgKi9cbiAgICBiYXNlTnVtYmVyaW5nOiBudW1iZXI7XG4gICAgLyoqXG4gICAgICogTWF4aW1hbCBkZXB0aCBvZiBoZWFkaW5ncyB0byBkaXNwbGF5XG4gICAgICovXG4gICAgbWF4aW1hbERlcHRoOiBudW1iZXI7XG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBudW1iZXIgZmlyc3QtbGV2ZWwgaGVhZGluZ3Mgb3Igbm90LlxuICAgICAqL1xuICAgIG51bWJlcmluZ0gxOiBib29sZWFuO1xuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gbnVtYmVyIGhlYWRpbmdzIGluIGRvY3VtZW50IG9yIG5vdC5cbiAgICAgKi9cbiAgICBudW1iZXJIZWFkZXJzOiBib29sZWFuO1xuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gaW5jbHVkZSBjZWxsIG91dHB1dHMgaW4gaGVhZGluZ3Mgb3Igbm90LlxuICAgICAqL1xuICAgIGluY2x1ZGVPdXRwdXQ6IGJvb2xlYW47XG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBzeW5jaHJvbml6ZSBoZWFkaW5nIGNvbGxhcHNlIHN0YXRlIGJldHdlZW4gdGhlIFRvQyBhbmQgdGhlIGRvY3VtZW50IG9yIG5vdC5cbiAgICAgKi9cbiAgICBzeW5jQ29sbGFwc2VTdGF0ZTogYm9vbGVhbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBEZWZhdWx0IHRhYmxlIG9mIGNvbnRlbnQgY29uZmlndXJhdGlvblxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRDb25maWc6IElDb25maWcgPSB7XG4gICAgYmFzZU51bWJlcmluZzogMSxcbiAgICBtYXhpbWFsRGVwdGg6IDQsXG4gICAgbnVtYmVyaW5nSDE6IHRydWUsXG4gICAgbnVtYmVySGVhZGVyczogZmFsc2UsXG4gICAgaW5jbHVkZU91dHB1dDogdHJ1ZSxcbiAgICBzeW5jQ29sbGFwc2VTdGF0ZTogZmFsc2VcbiAgfTtcblxuICAvKipcbiAgICogSW50ZXJmYWNlIGRlc2NyaWJpbmcgYSBoZWFkaW5nLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJSGVhZGluZyB7XG4gICAgLyoqXG4gICAgICogSGVhZGluZyB0ZXh0LlxuICAgICAqL1xuICAgIHRleHQ6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEhUTUwgaGVhZGluZyBsZXZlbC5cbiAgICAgKi9cbiAgICBsZXZlbDogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogSGVhZGluZyBwcmVmaXguXG4gICAgICovXG4gICAgcHJlZml4Pzogc3RyaW5nIHwgbnVsbDtcblxuICAgIC8qKlxuICAgICAqIERhdGFzZXQgdG8gYWRkIHRvIHRoZSBpdGVtIG5vZGVcbiAgICAgKi9cbiAgICBkYXRhc2V0PzogUmVjb3JkPHN0cmluZywgc3RyaW5nPjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIGhlYWRpbmcgaXMgY29sbGFwc2VkIG9yIG5vdFxuICAgICAqL1xuICAgIGNvbGxhcHNlZD86IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBoZWFkaW5nIGlzIG1hcmtlZCB0byBza2lwIG9yIG5vdFxuICAgICAqL1xuICAgIHNraXA/OiBib29sZWFuO1xuICB9XG5cbiAgLyoqXG4gICAqIEludGVyZmFjZSBkZXNjcmliaW5nIGEgd2lkZ2V0IHRhYmxlIG9mIGNvbnRlbnRzIG1vZGVsLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTW9kZWw8SCBleHRlbmRzIElIZWFkaW5nPiBleHRlbmRzIFZEb21SZW5kZXJlci5JTW9kZWwge1xuICAgIC8qKlxuICAgICAqIEFjdGl2ZSBoZWFkaW5nXG4gICAgICovXG4gICAgcmVhZG9ubHkgYWN0aXZlSGVhZGluZzogSCB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBTaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBhY3RpdmUgaGVhZGluZyBjaGFuZ2VzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGFjdGl2ZUhlYWRpbmdDaGFuZ2VkOiBJU2lnbmFsPElNb2RlbDxIPiwgSCB8IG51bGw+O1xuXG4gICAgLyoqXG4gICAgICogU2lnbmFsIGVtaXR0ZWQgd2hlbiBhIHRhYmxlIG9mIGNvbnRlbnQgc2VjdGlvbiBjb2xsYXBzZSBzdGF0ZSBjaGFuZ2VzLlxuICAgICAqXG4gICAgICogSWYgYWxsIGhlYWRpbmdzIHN0YXRlIGFyZSBzZXQgYXQgdGhlIHNhbWUgdGltZSwgdGhlIGFyZ3VtZW50IGlzIG51bGwuXG4gICAgICovXG4gICAgcmVhZG9ubHkgY29sbGFwc2VDaGFuZ2VkOiBJU2lnbmFsPElNb2RlbDxIPiwgSCB8IG51bGw+O1xuXG4gICAgLyoqXG4gICAgICogTW9kZWwgY29uZmlndXJhdGlvblxuICAgICAqL1xuICAgIHJlYWRvbmx5IGNvbmZpZ3VyYXRpb246IElDb25maWc7XG5cbiAgICAvKipcbiAgICAgKiBUeXBlIG9mIGRvY3VtZW50IHN1cHBvcnRlZCBieSB0aGUgbW9kZWwuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogQSBgZGF0YS1kb2N1bWVudC10eXBlYCBhdHRyaWJ1dGUgd2l0aCB0aGlzIHZhbHVlIHdpbGwgYmUgc2V0XG4gICAgICogb24gdGhlIHRyZWUgdmlldyBgLmpwLVRhYmxlT2ZDb250ZW50cy1jb250ZW50W2RhdGEtZG9jdW1lbnQtdHlwZT1cIi4uLlwiXWBcbiAgICAgKi9cbiAgICByZWFkb25seSBkb2N1bWVudFR5cGU6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFJldHVybnMgdGhlIGxpc3Qgb2YgaGVhZGluZ3MuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBsaXN0IG9mIGhlYWRpbmdzXG4gICAgICovXG4gICAgcmVhZG9ubHkgaGVhZGluZ3M6IEhbXTtcblxuICAgIC8qKlxuICAgICAqIFNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGhlYWRpbmdzIGNoYW5nZXMuXG4gICAgICovXG4gICAgcmVhZG9ubHkgaGVhZGluZ3NDaGFuZ2VkOiBJU2lnbmFsPElNb2RlbDxIPiwgdm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBtb2RlbCBuZWVkcyB0byBiZSBrZXB0IHVwIHRvIGRhdGUgb3Igbm90LlxuICAgICAqXG4gICAgICogIyMjIE5vdGVzXG4gICAgICogVGhpcyBpcyBzZXQgdG8gYHRydWVgIGlmIHRoZSBUb0MgcGFuZWwgaXMgdmlzaWJsZSBhbmRcbiAgICAgKiB0byBgZmFsc2VgIGlmIGl0IGlzIGhpZGRlbi4gQnV0IHNvbWUgbW9kZWxzIG1heSByZXF1aXJlXG4gICAgICogdG8gYmUgYWx3YXlzIGFjdGl2ZTsgZS5nLiB0byBhZGQgbnVtYmVyaW5nIGluIHRoZSBkb2N1bWVudC5cbiAgICAgKi9cbiAgICBpc0FjdGl2ZTogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFNldCBhIG5ldyBhY3RpdmUgaGVhZGluZy5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBoZWFkaW5nIFRoZSBuZXcgYWN0aXZlIGhlYWRpbmdcbiAgICAgKiBAcGFyYW0gZW1pdFNpZ25hbCBXaGV0aGVyIHRvIGVtaXQgdGhlIGFjdGl2ZUhlYWRpbmdDaGFuZ2VkIHNpZ25hbCBvciBub3QuXG4gICAgICovXG4gICAgc2V0QWN0aXZlSGVhZGluZyhoZWFkaW5nOiBIIHwgbnVsbCwgZW1pdFNpZ25hbD86IGJvb2xlYW4pOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogTW9kZWwgY29uZmlndXJhdGlvbiBzZXR0ZXIuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gYyBOZXcgY29uZmlndXJhdGlvblxuICAgICAqL1xuICAgIHNldENvbmZpZ3VyYXRpb24oYzogUGFydGlhbDxJQ29uZmlnPik6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBMaXN0IG9mIGNvbmZpZ3VyYXRpb24gb3B0aW9ucyBzdXBwb3J0ZWQgYnkgdGhlIG1vZGVsLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHN1cHBvcnRlZE9wdGlvbnM6IChrZXlvZiBJQ29uZmlnKVtdO1xuXG4gICAgLyoqXG4gICAgICogRG9jdW1lbnQgdGl0bGVcbiAgICAgKi9cbiAgICB0aXRsZT86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIENhbGxiYWNrIG9uIGhlYWRpbmcgY29sbGFwc2UuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gb3B0aW9ucy5oZWFkaW5nIFRoZSBoZWFkaW5nIHRvIGNoYW5nZSBzdGF0ZSAoYWxsIGhlYWRpbmdzIGlmIG5vdCBwcm92aWRlZClcbiAgICAgKiBAcGFyYW0gb3B0aW9ucy5jb2xsYXBzZWQgVGhlIG5ldyBjb2xsYXBzZWQgc3RhdHVzICh0b2dnbGUgZXhpc3Rpbmcgc3RhdHVzIGlmIG5vdCBwcm92aWRlZClcbiAgICAgKi9cbiAgICB0b2dnbGVDb2xsYXBzZTogKG9wdGlvbnM6IHsgaGVhZGluZz86IEg7IGNvbGxhcHNlZD86IGJvb2xlYW4gfSkgPT4gdm9pZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZW5lcmljIHRhYmxlIG9mIGNvbnRlbnRzIHR5cGVcbiAgICovXG4gIGV4cG9ydCB0eXBlIE1vZGVsID0gSU1vZGVsPElIZWFkaW5nPjtcblxuICAvKipcbiAgICogSW50ZXJmYWNlIGRlc2NyaWJpbmcgdGFibGUgb2YgY29udGVudHMgd2lkZ2V0IG9wdGlvbnMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUYWJsZSBvZiBjb250ZW50cyBtb2RlbC5cbiAgICAgKi9cbiAgICBtb2RlbD86IElNb2RlbDxJSGVhZGluZz47XG5cbiAgICAvKipcbiAgICAgKiBJZiBubyBoZWFkaW5ncyBhcmUgcHJlc2VudCwgYSBoZWFkbGluZSB0byBkaXNwbGF5IGFzIGEgcGxhY2Vob2xkZXJcbiAgICAgKi9cbiAgICBwbGFjZWhvbGRlckhlYWRsaW5lOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBJZiBubyBoZWFkaW5ncyBhcmUgcHJlc2VudCwgdGV4dCB0byBkaXNwbGF5IGFzIGEgcGxhY2Vob2xkZXJcbiAgICAgKi9cbiAgICBwbGFjZWhvbGRlclRleHQ6IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBJbnRlcmZhY2UgZGVzY3JpYmluZyBhIHRvb2xiYXIgaXRlbSBsaXN0XG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElUb29sYmFySXRlbXNcbiAgICBleHRlbmRzIElPYnNlcnZhYmxlTGlzdDxUb29sYmFyUmVnaXN0cnkuSVRvb2xiYXJJdGVtPiB7fVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHsgSVRhYmxlT2ZDb250ZW50c1RyYWNrZXIsIFRhYmxlT2ZDb250ZW50cyB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBUYWJsZSBvZiBjb250ZW50cyB0cmFja2VyXG4gKi9cbmV4cG9ydCBjbGFzcyBUYWJsZU9mQ29udGVudHNUcmFja2VyIGltcGxlbWVudHMgSVRhYmxlT2ZDb250ZW50c1RyYWNrZXIge1xuICAvKipcbiAgICogQ29uc3RydWN0b3JcbiAgICovXG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMubW9kZWxNYXBwaW5nID0gbmV3IFdlYWtNYXA8V2lkZ2V0LCBUYWJsZU9mQ29udGVudHMuTW9kZWw+KCk7XG4gIH1cblxuICAvKipcbiAgICogVHJhY2sgYSBnaXZlbiBtb2RlbC5cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCBXaWRnZXRcbiAgICogQHBhcmFtIG1vZGVsIFRhYmxlIG9mIGNvbnRlbnRzIG1vZGVsXG4gICAqL1xuICBhZGQod2lkZ2V0OiBXaWRnZXQsIG1vZGVsOiBUYWJsZU9mQ29udGVudHMuTW9kZWwpOiB2b2lkIHtcbiAgICB0aGlzLm1vZGVsTWFwcGluZy5zZXQod2lkZ2V0LCBtb2RlbCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCBhc3NvY2lhdGVkIHdpdGggYSBnaXZlbiB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgV2lkZ2V0XG4gICAqIEByZXR1cm5zIFRoZSB0YWJsZSBvZiBjb250ZW50cyBtb2RlbFxuICAgKi9cbiAgZ2V0KHdpZGdldDogV2lkZ2V0KTogVGFibGVPZkNvbnRlbnRzLk1vZGVsIHwgbnVsbCB7XG4gICAgY29uc3QgbW9kZWwgPSB0aGlzLm1vZGVsTWFwcGluZy5nZXQod2lkZ2V0KTtcblxuICAgIHJldHVybiAhbW9kZWwgfHwgbW9kZWwuaXNEaXNwb3NlZCA/IG51bGwgOiBtb2RlbDtcbiAgfVxuXG4gIHByb3RlY3RlZCBtb2RlbE1hcHBpbmc6IFdlYWtNYXA8V2lkZ2V0LCBUYWJsZU9mQ29udGVudHMuTW9kZWw+O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBWRG9tUmVuZGVyZXIgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IFRhYmxlT2ZDb250ZW50c1RyZWUgfSBmcm9tICcuL3RvY3RyZWUnO1xuaW1wb3J0IHsgVGFibGVPZkNvbnRlbnRzIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIFRhYmxlIG9mIGNvbnRlbnRzIHdpZGdldC5cbiAqL1xuZXhwb3J0IGNsYXNzIFRhYmxlT2ZDb250ZW50c1dpZGdldCBleHRlbmRzIFZEb21SZW5kZXJlcjxUYWJsZU9mQ29udGVudHMuSU1vZGVsPFRhYmxlT2ZDb250ZW50cy5JSGVhZGluZz4gfCBudWxsPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3RvclxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyBXaWRnZXQgb3B0aW9uc1xuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogVGFibGVPZkNvbnRlbnRzLklPcHRpb25zKSB7XG4gICAgc3VwZXIob3B0aW9ucy5tb2RlbCk7XG4gICAgdGhpcy5fcGxhY2Vob2xkZXJIZWFkbGluZSA9IG9wdGlvbnMucGxhY2Vob2xkZXJIZWFkbGluZTtcbiAgICB0aGlzLl9wbGFjZWhvbGRlclRleHQgPSBvcHRpb25zLnBsYWNlaG9sZGVyVGV4dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgdGhlIGNvbnRlbnQgb2YgdGhpcyB3aWRnZXQgdXNpbmcgdGhlIHZpcnR1YWwgRE9NLlxuICAgKlxuICAgKiBUaGlzIG1ldGhvZCB3aWxsIGJlIGNhbGxlZCBhbnl0aW1lIHRoZSB3aWRnZXQgbmVlZHMgdG8gYmUgcmVuZGVyZWQsIHdoaWNoXG4gICAqIGluY2x1ZGVzIGxheW91dCB0cmlnZ2VyZWQgcmVuZGVyaW5nLlxuICAgKi9cbiAgcmVuZGVyKCk6IEpTWC5FbGVtZW50IHwgbnVsbCB7XG4gICAgaWYgKCF0aGlzLm1vZGVsIHx8IHRoaXMubW9kZWwuaGVhZGluZ3MubGVuZ3RoID09PSAwKSB7XG4gICAgICByZXR1cm4gKFxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLVRhYmxlT2ZDb250ZW50cy1wbGFjZWhvbGRlclwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtVGFibGVPZkNvbnRlbnRzLXBsYWNlaG9sZGVyQ29udGVudFwiPlxuICAgICAgICAgICAgPGgzPnt0aGlzLl9wbGFjZWhvbGRlckhlYWRsaW5lfTwvaDM+XG4gICAgICAgICAgICA8cD57dGhpcy5fcGxhY2Vob2xkZXJUZXh0fTwvcD5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICApO1xuICAgIH1cblxuICAgIHJldHVybiAoXG4gICAgICA8VGFibGVPZkNvbnRlbnRzVHJlZVxuICAgICAgICBhY3RpdmVIZWFkaW5nPXt0aGlzLm1vZGVsLmFjdGl2ZUhlYWRpbmd9XG4gICAgICAgIGRvY3VtZW50VHlwZT17dGhpcy5tb2RlbC5kb2N1bWVudFR5cGV9XG4gICAgICAgIGhlYWRpbmdzPXt0aGlzLm1vZGVsLmhlYWRpbmdzfVxuICAgICAgICBvbkNvbGxhcHNlQ2hhbmdlPXsoaGVhZGluZzogVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nKSA9PiB7XG4gICAgICAgICAgdGhpcy5tb2RlbCEudG9nZ2xlQ29sbGFwc2UoeyBoZWFkaW5nIH0pO1xuICAgICAgICB9fVxuICAgICAgICBzZXRBY3RpdmVIZWFkaW5nPXsoaGVhZGluZzogVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nKSA9PiB7XG4gICAgICAgICAgdGhpcy5tb2RlbCEuc2V0QWN0aXZlSGVhZGluZyhoZWFkaW5nKTtcbiAgICAgICAgfX1cbiAgICAgID48L1RhYmxlT2ZDb250ZW50c1RyZWU+XG4gICAgKTtcbiAgfVxuXG4gIHJlYWRvbmx5IF9wbGFjZWhvbGRlckhlYWRsaW5lOiBzdHJpbmc7XG4gIHJlYWRvbmx5IF9wbGFjZWhvbGRlclRleHQ6IHN0cmluZztcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgVGFibGVPZkNvbnRlbnRzIH0gZnJvbSAnLi4vdG9rZW5zJztcblxuLyoqXG4gKiBDbGFzcyB1c2VkIHRvIG1hcmsgbnVtYmVyaW5nIHByZWZpeCBmb3IgaGVhZGluZ3MgaW4gYSBkb2N1bWVudC5cbiAqL1xuZXhwb3J0IGNvbnN0IE5VTUJFUklOR19DTEFTUyA9ICdudW1iZXJpbmctZW50cnknO1xuXG4vKipcbiAqIEhUTUwgaGVhZGluZ1xuICovXG5leHBvcnQgaW50ZXJmYWNlIElIVE1MSGVhZGluZyBleHRlbmRzIFRhYmxlT2ZDb250ZW50cy5JSGVhZGluZyB7XG4gIC8qKlxuICAgKiBIVE1MIGlkXG4gICAqL1xuICBpZD86IHN0cmluZyB8IG51bGw7XG59XG5cbi8qKlxuICogRmlsdGVyIGhlYWRpbmdzIGZvciB0YWJsZSBvZiBjb250ZW50cyBhbmQgY29tcHV0ZSBhc3NvY2lhdGVkIHByZWZpeFxuICpcbiAqIEBwYXJhbSBoZWFkaW5ncyBIZWFkaW5ncyB0byBwcm9jZXNzXG4gKiBAcGFyYW0gb3B0aW9ucyBPcHRpb25zXG4gKiBAcGFyYW0gaW5pdGlhbExldmVscyBJbml0aWFsIGxldmVscyBmb3IgcHJlZml4IGNvbXB1dGF0aW9uXG4gKiBAcmV0dXJucyBFeHRyYWN0ZWQgaGVhZGluZ3NcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGZpbHRlckhlYWRpbmdzPFxuICBUIGV4dGVuZHMgVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nID0gVGFibGVPZkNvbnRlbnRzLklIZWFkaW5nXG4+KFxuICBoZWFkaW5nczogVFtdLFxuICBvcHRpb25zPzogUGFydGlhbDxUYWJsZU9mQ29udGVudHMuSUNvbmZpZz4sXG4gIGluaXRpYWxMZXZlbHM6IG51bWJlcltdID0gW11cbik6IFRbXSB7XG4gIGNvbnN0IGNvbmZpZyA9IHtcbiAgICAuLi5UYWJsZU9mQ29udGVudHMuZGVmYXVsdENvbmZpZyxcbiAgICAuLi5vcHRpb25zXG4gIH0gYXMgVGFibGVPZkNvbnRlbnRzLklDb25maWc7XG5cbiAgY29uc3QgbGV2ZWxzID0gaW5pdGlhbExldmVscztcbiAgbGV0IHByZXZpb3VzTGV2ZWwgPSBsZXZlbHMubGVuZ3RoO1xuICBjb25zdCBmaWx0ZXJlZEhlYWRpbmdzID0gbmV3IEFycmF5PFQ+KCk7XG4gIGZvciAoY29uc3QgaGVhZGluZyBvZiBoZWFkaW5ncykge1xuICAgIGlmIChoZWFkaW5nLnNraXApIHtcbiAgICAgIGNvbnRpbnVlO1xuICAgIH1cbiAgICBjb25zdCBsZXZlbCA9IGhlYWRpbmcubGV2ZWw7XG5cbiAgICBpZiAobGV2ZWwgPiAwICYmIGxldmVsIDw9IGNvbmZpZy5tYXhpbWFsRGVwdGgpIHtcbiAgICAgIGNvbnN0IHByZWZpeCA9IGdldFByZWZpeChsZXZlbCwgcHJldmlvdXNMZXZlbCwgbGV2ZWxzLCBjb25maWcpO1xuICAgICAgcHJldmlvdXNMZXZlbCA9IGxldmVsO1xuXG4gICAgICBmaWx0ZXJlZEhlYWRpbmdzLnB1c2goe1xuICAgICAgICAuLi5oZWFkaW5nLFxuICAgICAgICBwcmVmaXhcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxuICByZXR1cm4gZmlsdGVyZWRIZWFkaW5ncztcbn1cblxuLyoqXG4gKiBSZXR1cm5zIHdoZXRoZXIgYSBNSU1FIHR5cGUgY29ycmVzcG9uZHMgdG8gZWl0aGVyIEhUTUwuXG4gKlxuICogQHBhcmFtIG1pbWUgLSBNSU1FIHR5cGUgc3RyaW5nXG4gKiBAcmV0dXJucyBib29sZWFuIGluZGljYXRpbmcgd2hldGhlciBhIHByb3ZpZGVkIE1JTUUgdHlwZSBjb3JyZXNwb25kcyB0byBlaXRoZXIgSFRNTFxuICpcbiAqIEBleGFtcGxlXG4gKiBjb25zdCBib29sID0gaXNIVE1MKCd0ZXh0L2h0bWwnKTtcbiAqIC8vIHJldHVybnMgdHJ1ZVxuICpcbiAqIEBleGFtcGxlXG4gKiBjb25zdCBib29sID0gaXNIVE1MKCd0ZXh0L3BsYWluJyk7XG4gKiAvLyByZXR1cm5zIGZhbHNlXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBpc0hUTUwobWltZTogc3RyaW5nKTogYm9vbGVhbiB7XG4gIHJldHVybiBtaW1lID09PSAndGV4dC9odG1sJztcbn1cblxuLyoqXG4gKiBQYXJzZSBhIEhUTUwgc3RyaW5nIGZvciBoZWFkaW5ncy5cbiAqXG4gKiAjIyMgTm90ZXNcbiAqIFRoZSBodG1sIHN0cmluZyBpcyBub3Qgc2FuaXRpemVkIC0gdXNlIHdpdGggY2F1dGlvblxuICpcbiAqIEBwYXJhbSBodG1sIEhUTUwgc3RyaW5nIHRvIHBhcnNlXG4gKiBAcGFyYW0gZm9yY2UgV2hldGhlciB0byBpZ25vcmUgSFRNTCBoZWFkaW5ncyB3aXRoIGNsYXNzIGpwLXRvYy1pZ25vcmUgYW5kIHRvY1NraXAgb3Igbm90XG4gKiBAcmV0dXJucyBFeHRyYWN0ZWQgaGVhZGluZ3NcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGdldEhUTUxIZWFkaW5ncyhodG1sOiBzdHJpbmcsIGZvcmNlID0gdHJ1ZSk6IElIVE1MSGVhZGluZ1tdIHtcbiAgY29uc3QgY29udGFpbmVyOiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICBjb250YWluZXIuaW5uZXJIVE1MID0gaHRtbDtcblxuICBjb25zdCBoZWFkaW5ncyA9IG5ldyBBcnJheTxJSFRNTEhlYWRpbmc+KCk7XG4gIGNvbnN0IGhlYWRlcnMgPSBjb250YWluZXIucXVlcnlTZWxlY3RvckFsbCgnaDEsIGgyLCBoMywgaDQsIGg1LCBoNicpO1xuICBmb3IgKGNvbnN0IGggb2YgaGVhZGVycykge1xuICAgIGNvbnN0IGxldmVsID0gcGFyc2VJbnQoaC50YWdOYW1lWzFdLCAxMCk7XG5cbiAgICBoZWFkaW5ncy5wdXNoKHtcbiAgICAgIHRleHQ6IGgudGV4dENvbnRlbnQgPz8gJycsXG4gICAgICBsZXZlbCxcbiAgICAgIGlkOiBoPy5nZXRBdHRyaWJ1dGUoJ2lkJyksXG4gICAgICBza2lwOlxuICAgICAgICBoLmNsYXNzTGlzdC5jb250YWlucygnanAtdG9jLWlnbm9yZScpIHx8IGguY2xhc3NMaXN0LmNvbnRhaW5zKCd0b2NTa2lwJylcbiAgICB9KTtcbiAgfVxuICByZXR1cm4gaGVhZGluZ3M7XG59XG5cbi8qKlxuICogQWRkIGFuIGhlYWRpbmcgcHJlZml4IHRvIGEgSFRNTCBub2RlLlxuICpcbiAqIEBwYXJhbSBjb250YWluZXIgSFRNTCBub2RlIGNvbnRhaW5pbmcgdGhlIGhlYWRpbmdcbiAqIEBwYXJhbSBzZWxlY3RvciBIZWFkaW5nIHNlbGVjdG9yXG4gKiBAcGFyYW0gcHJlZml4IFRpdGxlIHByZWZpeCB0byBhZGRcbiAqIEByZXR1cm5zIFRoZSBtb2RpZmllZCBIVE1MIGVsZW1lbnRcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGFkZFByZWZpeChcbiAgY29udGFpbmVyOiBFbGVtZW50LFxuICBzZWxlY3Rvcjogc3RyaW5nLFxuICBwcmVmaXg6IHN0cmluZ1xuKTogRWxlbWVudCB8IG51bGwge1xuICBsZXQgZWxlbWVudCA9IGNvbnRhaW5lci5xdWVyeVNlbGVjdG9yKHNlbGVjdG9yKSBhcyBFbGVtZW50IHwgbnVsbDtcblxuICBpZiAoIWVsZW1lbnQpIHtcbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIGlmICghZWxlbWVudC5xdWVyeVNlbGVjdG9yKGBzcGFuLiR7TlVNQkVSSU5HX0NMQVNTfWApKSB7XG4gICAgYWRkTnVtYmVyaW5nKGVsZW1lbnQsIHByZWZpeCk7XG4gIH0gZWxzZSB7XG4gICAgLy8gVGhlcmUgYXJlIGxpa2VseSBtdWx0aXBsZSBlbGVtZW50cyB3aXRoIHRoZSBzYW1lIHNlbGVjdG9yXG4gICAgLy8gID0+IHVzZSB0aGUgZmlyc3Qgb25lIHdpdGhvdXQgcHJlZml4XG4gICAgY29uc3QgYWxsRWxlbWVudHMgPSBjb250YWluZXIucXVlcnlTZWxlY3RvckFsbChzZWxlY3Rvcik7XG4gICAgZm9yIChjb25zdCBlbCBvZiBhbGxFbGVtZW50cykge1xuICAgICAgaWYgKCFlbC5xdWVyeVNlbGVjdG9yKGBzcGFuLiR7TlVNQkVSSU5HX0NMQVNTfWApKSB7XG4gICAgICAgIGVsZW1lbnQgPSBlbDtcbiAgICAgICAgYWRkTnVtYmVyaW5nKGVsLCBwcmVmaXgpO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICByZXR1cm4gZWxlbWVudDtcbn1cblxuLyoqXG4gKiBVcGRhdGUgdGhlIGxldmVscyBhbmQgY3JlYXRlIHRoZSBudW1iZXJpbmcgcHJlZml4XG4gKlxuICogQHBhcmFtIGxldmVsIEN1cnJlbnQgbGV2ZWxcbiAqIEBwYXJhbSBwcmV2aW91c0xldmVsIFByZXZpb3VzIGxldmVsXG4gKiBAcGFyYW0gbGV2ZWxzIExldmVscyBsaXN0XG4gKiBAcGFyYW0gb3B0aW9ucyBPcHRpb25zXG4gKiBAcmV0dXJucyBUaGUgbnVtYmVyaW5nIHByZWZpeFxuICovXG5leHBvcnQgZnVuY3Rpb24gZ2V0UHJlZml4KFxuICBsZXZlbDogbnVtYmVyLFxuICBwcmV2aW91c0xldmVsOiBudW1iZXIsXG4gIGxldmVsczogbnVtYmVyW10sXG4gIG9wdGlvbnM6IFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnXG4pOiBzdHJpbmcge1xuICBjb25zdCB7IGJhc2VOdW1iZXJpbmcsIG51bWJlcmluZ0gxLCBudW1iZXJIZWFkZXJzIH0gPSBvcHRpb25zO1xuICBsZXQgcHJlZml4ID0gJyc7XG4gIGlmIChudW1iZXJIZWFkZXJzKSB7XG4gICAgY29uc3QgaGlnaGVzdExldmVsID0gbnVtYmVyaW5nSDEgPyAxIDogMjtcbiAgICBpZiAobGV2ZWwgPiBwcmV2aW91c0xldmVsKSB7XG4gICAgICAvLyBJbml0aWFsaXplIHRoZSBuZXcgbGV2ZWxzXG4gICAgICBmb3IgKGxldCBsID0gcHJldmlvdXNMZXZlbDsgbCA8IGxldmVsIC0gMTsgbCsrKSB7XG4gICAgICAgIGxldmVsc1tsXSA9IDA7XG4gICAgICB9XG4gICAgICBsZXZlbHNbbGV2ZWwgLSAxXSA9IGxldmVsID09PSBoaWdoZXN0TGV2ZWwgPyBiYXNlTnVtYmVyaW5nIDogMTtcbiAgICB9IGVsc2Uge1xuICAgICAgLy8gSW5jcmVtZW50IHRoZSBjdXJyZW50IGxldmVsXG4gICAgICBsZXZlbHNbbGV2ZWwgLSAxXSArPSAxO1xuXG4gICAgICAvLyBEcm9wIGhpZ2hlciBsZXZlbHNcbiAgICAgIGlmIChsZXZlbCA8IHByZXZpb3VzTGV2ZWwpIHtcbiAgICAgICAgbGV2ZWxzLnNwbGljZShsZXZlbCk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gSWYgdGhlIGhlYWRlciBsaXN0IHNraXBzIHNvbWUgbGV2ZWwsIHJlcGxhY2UgbWlzc2luZyBlbGVtZW50cyBieSAwXG4gICAgaWYgKG51bWJlcmluZ0gxKSB7XG4gICAgICBwcmVmaXggPSBsZXZlbHMubWFwKGxldmVsID0+IGxldmVsID8/IDApLmpvaW4oJy4nKSArICcuICc7XG4gICAgfSBlbHNlIHtcbiAgICAgIGlmIChsZXZlbHMubGVuZ3RoID4gMSkge1xuICAgICAgICBwcmVmaXggPVxuICAgICAgICAgIGxldmVsc1xuICAgICAgICAgICAgLnNsaWNlKDEpXG4gICAgICAgICAgICAubWFwKGxldmVsID0+IGxldmVsID8/IDApXG4gICAgICAgICAgICAuam9pbignLicpICsgJy4gJztcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgcmV0dXJuIHByZWZpeDtcbn1cblxuLyoqXG4gKiBBZGQgYSBudW1iZXJpbmcgcHJlZml4IHRvIGEgSFRNTCBlbGVtZW50LlxuICpcbiAqIEBwYXJhbSBlbCBIVE1MIGVsZW1lbnRcbiAqIEBwYXJhbSBudW1iZXJpbmcgTnVtYmVyaW5nIHByZWZpeCB0byBhZGRcbiAqL1xuZnVuY3Rpb24gYWRkTnVtYmVyaW5nKGVsOiBFbGVtZW50LCBudW1iZXJpbmc6IHN0cmluZyk6IHZvaWQge1xuICBlbC5pbnNlcnRBZGphY2VudEhUTUwoXG4gICAgJ2FmdGVyYmVnaW4nLFxuICAgIGA8c3BhbiBjbGFzcz1cIiR7TlVNQkVSSU5HX0NMQVNTfVwiPiR7bnVtYmVyaW5nfTwvc3Bhbj5gXG4gICk7XG59XG5cbi8qKlxuICogUmVtb3ZlIGFsbCBudW1iZXJpbmcgbm9kZXMgZnJvbSBlbGVtZW50XG4gKiBAcGFyYW0gZWxlbWVudCBOb2RlIHRvIGNsZWFyXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBjbGVhck51bWJlcmluZyhlbGVtZW50OiBFbGVtZW50KTogdm9pZCB7XG4gIGVsZW1lbnQ/LnF1ZXJ5U2VsZWN0b3JBbGwoYHNwYW4uJHtOVU1CRVJJTkdfQ0xBU1N9YCkuZm9yRWFjaChlbCA9PiB7XG4gICAgZWwucmVtb3ZlKCk7XG4gIH0pO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5leHBvcnQgKiBmcm9tICcuL2NvbW1vbic7XG5leHBvcnQgKiBhcyBNYXJrZG93biBmcm9tICcuL21hcmtkb3duJztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSU1hcmtkb3duUGFyc2VyLCByZW5kZXJNYXJrZG93biB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgVGFibGVPZkNvbnRlbnRzIH0gZnJvbSAnLi4vdG9rZW5zJztcblxuLyoqXG4gKiBNYXJrZG93biBoZWFkaW5nXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU1hcmtkb3duSGVhZGluZyBleHRlbmRzIFRhYmxlT2ZDb250ZW50cy5JSGVhZGluZyB7XG4gIC8qKlxuICAgKiBIZWFkaW5nIGxpbmVcbiAgICovXG4gIGxpbmU6IG51bWJlcjtcblxuICAvKipcbiAgICogUmF3IHN0cmluZyBjb250YWluaW5nIHRoZSBoZWFkaW5nXG4gICAqL1xuICByYXc6IHN0cmluZztcbn1cblxuLyoqXG4gKiBCdWlsZCB0aGUgaGVhZGluZyBodG1sIGlkLlxuICpcbiAqIEBwYXJhbSByYXcgUmF3IG1hcmtkb3duIGhlYWRpbmdcbiAqIEBwYXJhbSBsZXZlbCBIZWFkaW5nIGxldmVsXG4gKi9cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBnZXRIZWFkaW5nSWQoXG4gIHBhcnNlcjogSU1hcmtkb3duUGFyc2VyLFxuICByYXc6IHN0cmluZyxcbiAgbGV2ZWw6IG51bWJlclxuKTogUHJvbWlzZTxzdHJpbmcgfCBudWxsPiB7XG4gIHRyeSB7XG4gICAgY29uc3QgaW5uZXJIVE1MID0gYXdhaXQgcGFyc2VyLnJlbmRlcihyYXcpO1xuXG4gICAgaWYgKCFpbm5lckhUTUwpIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cblxuICAgIGNvbnN0IGNvbnRhaW5lciA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIGNvbnRhaW5lci5pbm5lckhUTUwgPSBpbm5lckhUTUw7XG4gICAgY29uc3QgaGVhZGVyID0gY29udGFpbmVyLnF1ZXJ5U2VsZWN0b3IoYGgke2xldmVsfWApO1xuICAgIGlmICghaGVhZGVyKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICByZXR1cm4gcmVuZGVyTWFya2Rvd24uY3JlYXRlSGVhZGVySWQoaGVhZGVyKTtcbiAgfSBjYXRjaCAocmVhc29uKSB7XG4gICAgY29uc29sZS5lcnJvcignRmFpbGVkIHRvIHBhcnNlIGEgaGVhZGluZy4nLCByZWFzb24pO1xuICB9XG5cbiAgcmV0dXJuIG51bGw7XG59XG5cbi8qKlxuICogUGFyc2VzIHRoZSBwcm92aWRlZCBzdHJpbmcgYW5kIHJldHVybnMgYSBsaXN0IG9mIGhlYWRpbmdzLlxuICpcbiAqIEBwYXJhbSB0ZXh0IC0gSW5wdXQgdGV4dFxuICogQHJldHVybnMgTGlzdCBvZiBoZWFkaW5nc1xuICovXG5leHBvcnQgZnVuY3Rpb24gZ2V0SGVhZGluZ3ModGV4dDogc3RyaW5nKTogSU1hcmtkb3duSGVhZGluZ1tdIHtcbiAgLy8gU3BsaXQgdGhlIHRleHQgaW50byBsaW5lczpcbiAgY29uc3QgbGluZXMgPSB0ZXh0LnNwbGl0KCdcXG4nKTtcblxuICAvLyBJdGVyYXRlIG92ZXIgdGhlIGxpbmVzIHRvIGdldCB0aGUgaGVhZGVyIGxldmVsIGFuZCB0ZXh0IGZvciBlYWNoIGxpbmU6XG4gIGNvbnN0IGhlYWRpbmdzID0gbmV3IEFycmF5PElNYXJrZG93bkhlYWRpbmc+KCk7XG4gIGxldCBpc0NvZGVCbG9jaztcbiAgbGV0IGxpbmVJZHggPSAwO1xuXG4gIC8vIERvbid0IGNoZWNrIGZvciBNYXJrZG93biBoZWFkaW5ncyBpZiBpbiBhIFlBTUwgZnJvbnRtYXR0ZXIgYmxvY2suXG4gIC8vIFdlIGNhbiBvbmx5IHN0YXJ0IGEgZnJvbnRtYXR0ZXIgYmxvY2sgb24gdGhlIGZpcnN0IGxpbmUgb2YgdGhlIGZpbGUuXG4gIC8vIEF0IG90aGVyIHBvc2l0aW9ucyBpbiBhIG1hcmtkb3duIGZpbGUsICctLS0nIHJlcHJlc2VudHMgYSBob3Jpem9udGFsIHJ1bGUuXG4gIGlmIChsaW5lc1tsaW5lSWR4XSA9PT0gJy0tLScpIHtcbiAgICAvLyBTZWFyY2ggZm9yIGFub3RoZXIgJy0tLScgYW5kIHRyZWF0IHRoYXQgYXMgdGhlIGVuZCBvZiB0aGUgZnJvbnRtYXR0ZXIuXG4gICAgLy8gSWYgd2UgZG9uJ3QgZmluZCBvbmUsIHRyZWF0IHRoZSBmaWxlIGFzIGNvbnRhaW5pbmcgbm8gZnJvbnRtYXR0ZXIuXG4gICAgZm9yIChcbiAgICAgIGxldCBmcm9udG1hdHRlckVuZExpbmVJZHggPSBsaW5lSWR4ICsgMTtcbiAgICAgIGZyb250bWF0dGVyRW5kTGluZUlkeCA8IGxpbmVzLmxlbmd0aDtcbiAgICAgIGZyb250bWF0dGVyRW5kTGluZUlkeCsrXG4gICAgKSB7XG4gICAgICBpZiAobGluZXNbZnJvbnRtYXR0ZXJFbmRMaW5lSWR4XSA9PT0gJy0tLScpIHtcbiAgICAgICAgbGluZUlkeCA9IGZyb250bWF0dGVyRW5kTGluZUlkeCArIDE7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgIH1cbiAgfVxuXG4gIGZvciAoOyBsaW5lSWR4IDwgbGluZXMubGVuZ3RoOyBsaW5lSWR4KyspIHtcbiAgICBjb25zdCBsaW5lID0gbGluZXNbbGluZUlkeF07XG5cbiAgICBpZiAobGluZSA9PT0gJycpIHtcbiAgICAgIC8vIEJhaWwgZWFybHlcbiAgICAgIGNvbnRpbnVlO1xuICAgIH1cblxuICAgIC8vIERvbid0IGNoZWNrIGZvciBNYXJrZG93biBoZWFkaW5ncyBpZiBpbiBhIGNvZGUgYmxvY2tcbiAgICBpZiAobGluZS5zdGFydHNXaXRoKCdgYGAnKSkge1xuICAgICAgaXNDb2RlQmxvY2sgPSAhaXNDb2RlQmxvY2s7XG4gICAgfVxuICAgIGlmIChpc0NvZGVCbG9jaykge1xuICAgICAgY29udGludWU7XG4gICAgfVxuXG4gICAgY29uc3QgaGVhZGluZyA9IHBhcnNlSGVhZGluZyhsaW5lLCBsaW5lc1tsaW5lSWR4ICsgMV0pOyAvLyBhcHBlbmQgdGhlIG5leHQgbGluZSB0byBjYXB0dXJlIGFsdGVybmF0aXZlIHN0eWxlIE1hcmtkb3duIGhlYWRpbmdzXG5cbiAgICBpZiAoaGVhZGluZykge1xuICAgICAgaGVhZGluZ3MucHVzaCh7XG4gICAgICAgIC4uLmhlYWRpbmcsXG4gICAgICAgIGxpbmU6IGxpbmVJZHhcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxuICByZXR1cm4gaGVhZGluZ3M7XG59XG5cbmNvbnN0IE1BUktET1dOX01JTUVfVFlQRSA9IFtcbiAgJ3RleHQveC1pcHl0aG9uZ2ZtJyxcbiAgJ3RleHQveC1tYXJrZG93bicsXG4gICd0ZXh0L3gtZ2ZtJyxcbiAgJ3RleHQvbWFya2Rvd24nXG5dO1xuXG4vKipcbiAqIFJldHVybnMgd2hldGhlciBhIE1JTUUgdHlwZSBjb3JyZXNwb25kcyB0byBhIE1hcmtkb3duIGZsYXZvci5cbiAqXG4gKiBAcGFyYW0gbWltZSAtIE1JTUUgdHlwZSBzdHJpbmdcbiAqIEByZXR1cm5zIGJvb2xlYW4gaW5kaWNhdGluZyB3aGV0aGVyIGEgcHJvdmlkZWQgTUlNRSB0eXBlIGNvcnJlc3BvbmRzIHRvIGEgTWFya2Rvd24gZmxhdm9yXG4gKlxuICogQGV4YW1wbGVcbiAqIGNvbnN0IGJvb2wgPSBpc01hcmtkb3duKCd0ZXh0L21hcmtkb3duJyk7XG4gKiAvLyByZXR1cm5zIHRydWVcbiAqXG4gKiBAZXhhbXBsZVxuICogY29uc3QgYm9vbCA9IGlzTWFya2Rvd24oJ3RleHQvcGxhaW4nKTtcbiAqIC8vIHJldHVybnMgZmFsc2VcbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIGlzTWFya2Rvd24obWltZTogc3RyaW5nKTogYm9vbGVhbiB7XG4gIHJldHVybiBNQVJLRE9XTl9NSU1FX1RZUEUuaW5jbHVkZXMobWltZSk7XG59XG5cbi8qKlxuICogSW50ZXJmYWNlIGRlc2NyaWJpbmcgYSBwYXJzZWQgaGVhZGluZyByZXN1bHQuXG4gKlxuICogQHByaXZhdGVcbiAqL1xuaW50ZXJmYWNlIElIZWFkZXIge1xuICAvKipcbiAgICogSGVhZGluZyB0ZXh0LlxuICAgKi9cbiAgdGV4dDogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBIZWFkaW5nIGxldmVsLlxuICAgKi9cbiAgbGV2ZWw6IG51bWJlcjtcblxuICAvKipcbiAgICogUmF3IHN0cmluZyBjb250YWluaW5nIHRoZSBoZWFkaW5nXG4gICAqL1xuICByYXc6IHN0cmluZztcblxuICAvKipcbiAgICogV2hldGhlciB0aGUgaGVhZGluZyBpcyBtYXJrZWQgdG8gc2tpcCBvciBub3RcbiAgICovXG4gIHNraXA6IGJvb2xlYW47XG59XG5cbi8qKlxuICogUGFyc2VzIGEgaGVhZGluZywgaWYgb25lIGV4aXN0cywgZnJvbSBhIHByb3ZpZGVkIHN0cmluZy5cbiAqXG4gKiAjIyBOb3Rlc1xuICpcbiAqIC0gICBIZWFkaW5nIGV4YW1wbGVzOlxuICpcbiAqICAgICAtICAgTWFya2Rvd24gaGVhZGluZzpcbiAqXG4gKiAgICAgICAgIGBgYFxuICogICAgICAgICAjIEZvb1xuICogICAgICAgICBgYGBcbiAqXG4gKiAgICAgLSAgIE1hcmtkb3duIGhlYWRpbmcgKGFsdGVybmF0aXZlIHN0eWxlKTpcbiAqXG4gKiAgICAgICAgIGBgYFxuICogICAgICAgICBGb29cbiAqICAgICAgICAgPT09XG4gKiAgICAgICAgIGBgYFxuICpcbiAqICAgICAgICAgYGBgXG4gKiAgICAgICAgIEZvb1xuICogICAgICAgICAtLS1cbiAqICAgICAgICAgYGBgXG4gKlxuICogICAgIC0gICBIVE1MIGhlYWRpbmc6XG4gKlxuICogICAgICAgICBgYGBcbiAqICAgICAgICAgPGgzPkZvbzwvaDM+XG4gKiAgICAgICAgIGBgYFxuICpcbiAqIEBwcml2YXRlXG4gKiBAcGFyYW0gbGluZSAtIExpbmUgdG8gcGFyc2VcbiAqIEBwYXJhbSBuZXh0TGluZSAtIFRoZSBsaW5lIGFmdGVyIHRoZSBvbmUgdG8gcGFyc2VcbiAqIEByZXR1cm5zIGhlYWRpbmcgaW5mb1xuICpcbiAqIEBleGFtcGxlXG4gKiBjb25zdCBvdXQgPSBwYXJzZUhlYWRpbmcoJyMjIyBGb29cXG4nKTtcbiAqIC8vIHJldHVybnMgeyd0ZXh0JzogJ0ZvbycsICdsZXZlbCc6IDN9XG4gKlxuICogQGV4YW1wbGVcbiAqIGNvbnN0IG91dCA9IHBhcnNlSGVhZGluZygnRm9vXFxuPT09XFxuJyk7XG4gKiAvLyByZXR1cm5zIHsndGV4dCc6ICdGb28nLCAnbGV2ZWwnOiAxfVxuICpcbiAqIEBleGFtcGxlXG4gKiBjb25zdCBvdXQgPSBwYXJzZUhlYWRpbmcoJzxoND5Gb288L2g0PlxcbicpO1xuICogLy8gcmV0dXJucyB7J3RleHQnOiAnRm9vJywgJ2xldmVsJzogNH1cbiAqXG4gKiBAZXhhbXBsZVxuICogY29uc3Qgb3V0ID0gcGFyc2VIZWFkaW5nKCdGb28nKTtcbiAqIC8vIHJldHVybnMgbnVsbFxuICovXG5mdW5jdGlvbiBwYXJzZUhlYWRpbmcobGluZTogc3RyaW5nLCBuZXh0TGluZT86IHN0cmluZyk6IElIZWFkZXIgfCBudWxsIHtcbiAgLy8gQ2FzZTogTWFya2Rvd24gaGVhZGluZ1xuICBsZXQgbWF0Y2ggPSBsaW5lLm1hdGNoKC9eKFsjXXsxLDZ9KSAoLiopLyk7XG4gIGlmIChtYXRjaCkge1xuICAgIHJldHVybiB7XG4gICAgICB0ZXh0OiBjbGVhblRpdGxlKG1hdGNoWzJdKSxcbiAgICAgIGxldmVsOiBtYXRjaFsxXS5sZW5ndGgsXG4gICAgICByYXc6IGxpbmUsXG4gICAgICBza2lwOiBza2lwSGVhZGluZy50ZXN0KG1hdGNoWzBdKVxuICAgIH07XG4gIH1cbiAgLy8gQ2FzZTogTWFya2Rvd24gaGVhZGluZyAoYWx0ZXJuYXRpdmUgc3R5bGUpXG4gIGlmIChuZXh0TGluZSkge1xuICAgIG1hdGNoID0gbmV4dExpbmUubWF0Y2goL14gezAsM30oWz1dezIsfXxbLV17Mix9KVxccyokLyk7XG4gICAgaWYgKG1hdGNoKSB7XG4gICAgICByZXR1cm4ge1xuICAgICAgICB0ZXh0OiBjbGVhblRpdGxlKGxpbmUpLFxuICAgICAgICBsZXZlbDogbWF0Y2hbMV1bMF0gPT09ICc9JyA/IDEgOiAyLFxuICAgICAgICByYXc6IFtsaW5lLCBuZXh0TGluZV0uam9pbignXFxuJyksXG4gICAgICAgIHNraXA6IHNraXBIZWFkaW5nLnRlc3QobGluZSlcbiAgICAgIH07XG4gICAgfVxuICB9XG4gIC8vIENhc2U6IEhUTUwgaGVhZGluZyAoV0FSTklORzogdGhpcyBpcyBub3QgcGFydGljdWxhcmx5IHJvYnVzdCwgYXMgSFRNTCBoZWFkaW5ncyBjYW4gc3BhbiBtdWx0aXBsZSBsaW5lcylcbiAgbWF0Y2ggPSBsaW5lLm1hdGNoKC88aChbMS02XSkuKj4oLiopPFxcL2hcXDE+L2kpO1xuICBpZiAobWF0Y2gpIHtcbiAgICByZXR1cm4ge1xuICAgICAgdGV4dDogbWF0Y2hbMl0sXG4gICAgICBsZXZlbDogcGFyc2VJbnQobWF0Y2hbMV0sIDEwKSxcbiAgICAgIHNraXA6IHNraXBIZWFkaW5nLnRlc3QobWF0Y2hbMF0pLFxuICAgICAgcmF3OiBsaW5lXG4gICAgfTtcbiAgfVxuXG4gIHJldHVybiBudWxsO1xufVxuXG5mdW5jdGlvbiBjbGVhblRpdGxlKGhlYWRpbmc6IHN0cmluZyk6IHN0cmluZyB7XG4gIC8vIHRha2Ugc3BlY2lhbCBjYXJlIHRvIHBhcnNlIE1hcmtkb3duIGxpbmtzIGludG8gcmF3IHRleHRcbiAgcmV0dXJuIGhlYWRpbmcucmVwbGFjZSgvXFxbKC4rKVxcXVxcKC4rXFwpL2csICckMScpO1xufVxuXG4vKipcbiAqIElnbm9yZSB0aXRsZSB3aXRoIGh0bWwgdGFnIHdpdGggYSBjbGFzcyBuYW1lIGVxdWFsIHRvIGBqcC10b2MtaWdub3JlYCBvciBgdG9jU2tpcGBcbiAqL1xuY29uc3Qgc2tpcEhlYWRpbmcgPVxuICAvPFxcdytcXHMoLio/XFxzKT9jbGFzcz1cIiguKj9cXHMpPyhqcC10b2MtaWdub3JlfHRvY1NraXApKFxccy4qPyk/XCIoXFxzLio/KT8+LztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==