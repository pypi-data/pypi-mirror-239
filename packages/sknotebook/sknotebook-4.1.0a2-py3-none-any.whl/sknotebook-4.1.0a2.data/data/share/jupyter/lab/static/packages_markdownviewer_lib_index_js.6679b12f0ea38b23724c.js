"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_markdownviewer_lib_index_js"],{

/***/ "../packages/markdownviewer/lib/index.js":
/*!***********************************************!*\
  !*** ../packages/markdownviewer/lib/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMarkdownViewerTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_1__.IMarkdownViewerTracker),
/* harmony export */   "MarkdownDocument": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.MarkdownDocument),
/* harmony export */   "MarkdownViewer": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.MarkdownViewer),
/* harmony export */   "MarkdownViewerFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_2__.MarkdownViewerFactory),
/* harmony export */   "MarkdownViewerTableOfContentsFactory": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_0__.MarkdownViewerTableOfContentsFactory),
/* harmony export */   "MarkdownViewerTableOfContentsModel": () => (/* reexport safe */ _toc__WEBPACK_IMPORTED_MODULE_0__.MarkdownViewerTableOfContentsModel)
/* harmony export */ });
/* harmony import */ var _toc__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./toc */ "../packages/markdownviewer/lib/toc.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../packages/markdownviewer/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "../packages/markdownviewer/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module markdownviewer
 */





/***/ }),

/***/ "../packages/markdownviewer/lib/toc.js":
/*!*********************************************!*\
  !*** ../packages/markdownviewer/lib/toc.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MarkdownViewerTableOfContentsFactory": () => (/* binding */ MarkdownViewerTableOfContentsFactory),
/* harmony export */   "MarkdownViewerTableOfContentsModel": () => (/* binding */ MarkdownViewerTableOfContentsModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * Table of content model for Markdown viewer files.
 */
class MarkdownViewerTableOfContentsModel extends _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsModel {
    /**
     * Constructor
     *
     * @param widget The widget to search in
     * @param parser Markdown parser
     * @param configuration Default model configuration
     */
    constructor(widget, parser, configuration) {
        super(widget, configuration);
        this.parser = parser;
    }
    /**
     * Type of document supported by the model.
     *
     * #### Notes
     * A `data-document-type` attribute with this value will be set
     * on the tree view `.jp-TableOfContents-content[data-document-type="..."]`
     */
    get documentType() {
        return 'markdown-viewer';
    }
    /**
     * Whether the model gets updated even if the table of contents panel
     * is hidden or not.
     */
    get isAlwaysActive() {
        return true;
    }
    /**
     * List of configuration options supported by the model.
     */
    get supportedOptions() {
        return ['maximalDepth', 'numberingH1', 'numberHeaders'];
    }
    /**
     * Produce the headings for a document.
     *
     * @returns The list of new headings or `null` if nothing needs to be updated.
     */
    getHeadings() {
        const content = this.widget.context.model.toString();
        const headings = _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.filterHeadings(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.Markdown.getHeadings(content), {
            ...this.configuration,
            // Force base number to be equal to 1
            baseNumbering: 1
        });
        return Promise.resolve(headings);
    }
}
/**
 * Table of content model factory for Markdown viewer files.
 */
class MarkdownViewerTableOfContentsFactory extends _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsFactory {
    /**
     * Constructor
     *
     * @param tracker Widget tracker
     * @param parser Markdown parser
     */
    constructor(tracker, parser) {
        super(tracker);
        this.parser = parser;
    }
    /**
     * Create a new table of contents model for the widget
     *
     * @param widget - widget
     * @param configuration - Table of contents configuration
     * @returns The table of contents model
     */
    _createNew(widget, configuration) {
        const model = new MarkdownViewerTableOfContentsModel(widget, this.parser, configuration);
        let headingToElement = new WeakMap();
        const onActiveHeadingChanged = (model, heading) => {
            if (heading) {
                const el = headingToElement.get(heading);
                if (el) {
                    const widgetBox = widget.content.node.getBoundingClientRect();
                    const elementBox = el.getBoundingClientRect();
                    if (elementBox.top > widgetBox.bottom ||
                        elementBox.bottom < widgetBox.top) {
                        el.scrollIntoView({ block: 'center' });
                    }
                }
                else {
                    console.warn('Heading element not found for heading', heading, 'in widget', widget);
                }
            }
        };
        const onHeadingsChanged = () => {
            if (!this.parser) {
                return;
            }
            // Clear all numbering items
            _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.clearNumbering(widget.content.node);
            // Create a new mapping
            headingToElement = new WeakMap();
            model.headings.forEach(async (heading) => {
                var _a;
                const elementId = await _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.Markdown.getHeadingId(this.parser, heading.raw, heading.level);
                if (!elementId) {
                    return;
                }
                const selector = `h${heading.level}[id="${elementId}"]`;
                headingToElement.set(heading, _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_0__.TableOfContentsUtils.addPrefix(widget.content.node, selector, (_a = heading.prefix) !== null && _a !== void 0 ? _a : ''));
            });
        };
        void widget.content.ready.then(() => {
            onHeadingsChanged();
            widget.content.rendered.connect(onHeadingsChanged);
            model.activeHeadingChanged.connect(onActiveHeadingChanged);
            model.headingsChanged.connect(onHeadingsChanged);
            widget.disposed.connect(() => {
                widget.content.rendered.disconnect(onHeadingsChanged);
                model.activeHeadingChanged.disconnect(onActiveHeadingChanged);
                model.headingsChanged.disconnect(onHeadingsChanged);
            });
        });
        return model;
    }
}


/***/ }),

/***/ "../packages/markdownviewer/lib/tokens.js":
/*!************************************************!*\
  !*** ../packages/markdownviewer/lib/tokens.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMarkdownViewerTracker": () => (/* binding */ IMarkdownViewerTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The markdownviewer tracker token.
 */
const IMarkdownViewerTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/markdownviewer:IMarkdownViewerTracker', `A widget tracker for markdown
  document viewers. Use this if you want to iterate over and interact with rendered markdown documents.`);


/***/ }),

/***/ "../packages/markdownviewer/lib/widget.js":
/*!************************************************!*\
  !*** ../packages/markdownviewer/lib/widget.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MarkdownDocument": () => (/* binding */ MarkdownDocument),
/* harmony export */   "MarkdownViewer": () => (/* binding */ MarkdownViewer),
/* harmony export */   "MarkdownViewerFactory": () => (/* binding */ MarkdownViewerFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to a markdown viewer.
 */
const MARKDOWNVIEWER_CLASS = 'jp-MarkdownViewer';
/**
 * The markdown MIME type.
 */
const MIMETYPE = 'text/markdown';
/**
 * A widget for markdown documents.
 */
class MarkdownViewer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__.Widget {
    /**
     * Construct a new markdown viewer widget.
     */
    constructor(options) {
        super();
        this._config = { ...MarkdownViewer.defaultConfig };
        this._fragment = '';
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.PromiseDelegate();
        this._isRendering = false;
        this._renderRequested = false;
        this._rendered = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_6__.Signal(this);
        this.context = options.context;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.renderer = options.renderer;
        this.node.tabIndex = 0;
        this.addClass(MARKDOWNVIEWER_CLASS);
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_7__.StackedLayout());
        layout.addWidget(this.renderer);
        void this.context.ready.then(async () => {
            await this._render();
            // Throttle the rendering rate of the widget.
            this._monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.ActivityMonitor({
                signal: this.context.model.contentChanged,
                timeout: this._config.renderTimeout
            });
            this._monitor.activityStopped.connect(this.update, this);
            this._ready.resolve(undefined);
        });
    }
    /**
     * A promise that resolves when the markdown viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Signal emitted when the content has been rendered.
     */
    get rendered() {
        return this._rendered;
    }
    /**
     * Set URI fragment identifier.
     */
    setFragment(fragment) {
        this._fragment = fragment;
        this.update();
    }
    /**
     * Set a config option for the markdown viewer.
     */
    setOption(option, value) {
        if (this._config[option] === value) {
            return;
        }
        this._config[option] = value;
        const { style } = this.renderer.node;
        switch (option) {
            case 'fontFamily':
                style.setProperty('font-family', value);
                break;
            case 'fontSize':
                style.setProperty('font-size', value ? value + 'px' : null);
                break;
            case 'hideFrontMatter':
                this.update();
                break;
            case 'lineHeight':
                style.setProperty('line-height', value ? value.toString() : null);
                break;
            case 'lineWidth': {
                const padding = value ? `calc(50% - ${value / 2}ch)` : null;
                style.setProperty('padding-left', padding);
                style.setProperty('padding-right', padding);
                break;
            }
            case 'renderTimeout':
                if (this._monitor) {
                    this._monitor.timeout = value;
                }
                break;
            default:
                break;
        }
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        if (this._monitor) {
            this._monitor.dispose();
        }
        this._monitor = null;
        super.dispose();
    }
    /**
     * Handle an `update-request` message to the widget.
     */
    onUpdateRequest(msg) {
        if (this.context.isReady && !this.isDisposed) {
            void this._render();
            this._fragment = '';
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.focus();
    }
    /**
     * Render the mime content.
     */
    async _render() {
        if (this.isDisposed) {
            return;
        }
        // Since rendering is async, we note render requests that happen while we
        // actually are rendering for a future rendering.
        if (this._isRendering) {
            this._renderRequested = true;
            return;
        }
        // Set up for this rendering pass.
        this._renderRequested = false;
        const { context } = this;
        const { model } = context;
        const source = model.toString();
        const data = {};
        // If `hideFrontMatter`is true remove front matter.
        data[MIMETYPE] = this._config.hideFrontMatter
            ? Private.removeFrontMatter(source)
            : source;
        const mimeModel = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.MimeModel({
            data,
            metadata: { fragment: this._fragment }
        });
        try {
            // Do the rendering asynchronously.
            this._isRendering = true;
            await this.renderer.renderModel(mimeModel);
            this._isRendering = false;
            // If there is an outstanding request to render, go ahead and render
            if (this._renderRequested) {
                return this._render();
            }
            else {
                this._rendered.emit();
            }
        }
        catch (reason) {
            // Dispose the document if rendering fails.
            requestAnimationFrame(() => {
                this.dispose();
            });
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)(this._trans.__('Renderer Failure: %1', context.path), reason);
        }
    }
}
/**
 * The namespace for MarkdownViewer class statics.
 */
(function (MarkdownViewer) {
    /**
     * The default configuration options for an editor.
     */
    MarkdownViewer.defaultConfig = {
        fontFamily: null,
        fontSize: null,
        lineHeight: null,
        lineWidth: null,
        hideFrontMatter: true,
        renderTimeout: 1000
    };
})(MarkdownViewer || (MarkdownViewer = {}));
/**
 * A document widget for markdown content.
 */
class MarkdownDocument extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.DocumentWidget {
    setFragment(fragment) {
        this.content.setFragment(fragment);
    }
}
/**
 * A widget factory for markdown viewers.
 */
class MarkdownViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.ABCWidgetFactory {
    /**
     * Construct a new markdown viewer widget factory.
     */
    constructor(options) {
        super(Private.createRegistryOptions(options));
        this._fileType = options.primaryFileType;
        this._rendermime = options.rendermime;
    }
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        var _a, _b, _c, _d, _e;
        const rendermime = this._rendermime.clone({
            resolver: context.urlResolver
        });
        const renderer = rendermime.createRenderer(MIMETYPE);
        const content = new MarkdownViewer({ context, renderer });
        content.title.icon = (_a = this._fileType) === null || _a === void 0 ? void 0 : _a.icon;
        content.title.iconClass = (_c = (_b = this._fileType) === null || _b === void 0 ? void 0 : _b.iconClass) !== null && _c !== void 0 ? _c : '';
        content.title.iconLabel = (_e = (_d = this._fileType) === null || _d === void 0 ? void 0 : _d.iconLabel) !== null && _e !== void 0 ? _e : '';
        content.title.caption = this.label;
        const widget = new MarkdownDocument({ content, context });
        return widget;
    }
}
/**
 * A namespace for markdown viewer widget private data.
 */
var Private;
(function (Private) {
    /**
     * Create the document registry options.
     */
    function createRegistryOptions(options) {
        return {
            ...options,
            readOnly: true
        };
    }
    Private.createRegistryOptions = createRegistryOptions;
    /**
     * Remove YAML front matter from source.
     */
    function removeFrontMatter(source) {
        const re = /^---\n[^]*?\n(---|...)\n/;
        const match = source.match(re);
        if (!match) {
            return source;
        }
        const { length } = match[0];
        return source.slice(length);
    }
    Private.removeFrontMatter = removeFrontMatter;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWFya2Rvd252aWV3ZXJfbGliX2luZGV4X2pzLjY2NzliMTJmMGVhMzhiMjM3MjRjLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRW1CO0FBQ0c7QUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDVHpCLDBDQUEwQztBQUMxQywyREFBMkQ7QUFTbEM7QUFTekI7O0dBRUc7QUFDSSxNQUFNLGtDQUFtQyxTQUFRLGlFQUd2RDtJQUNDOzs7Ozs7T0FNRztJQUNILFlBQ0UsTUFBd0IsRUFDZCxNQUE4QixFQUN4QyxhQUF1QztRQUV2QyxLQUFLLENBQUMsTUFBTSxFQUFFLGFBQWEsQ0FBQyxDQUFDO1FBSG5CLFdBQU0sR0FBTixNQUFNLENBQXdCO0lBSTFDLENBQUM7SUFFRDs7Ozs7O09BTUc7SUFDSCxJQUFJLFlBQVk7UUFDZCxPQUFPLGlCQUFpQixDQUFDO0lBQzNCLENBQUM7SUFFRDs7O09BR0c7SUFDSCxJQUFjLGNBQWM7UUFDMUIsT0FBTyxJQUFJLENBQUM7SUFDZCxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLGdCQUFnQjtRQUNsQixPQUFPLENBQUMsY0FBYyxFQUFFLGFBQWEsRUFBRSxlQUFlLENBQUMsQ0FBQztJQUMxRCxDQUFDO0lBRUQ7Ozs7T0FJRztJQUNPLFdBQVc7UUFDbkIsTUFBTSxPQUFPLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLFFBQVEsRUFBRSxDQUFDO1FBQ3JELE1BQU0sUUFBUSxHQUFHLGdGQUFtQyxDQUNsRCxzRkFBeUMsQ0FBQyxPQUFPLENBQUMsRUFDbEQ7WUFDRSxHQUFHLElBQUksQ0FBQyxhQUFhO1lBQ3JCLHFDQUFxQztZQUNyQyxhQUFhLEVBQUUsQ0FBQztTQUNqQixDQUNGLENBQUM7UUFDRixPQUFPLE9BQU8sQ0FBQyxPQUFPLENBQUMsUUFBUSxDQUFDLENBQUM7SUFDbkMsQ0FBQztDQUNG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Q0FBQztTQUNmO1FBQ0QsTUFBTSxFQUFFLE1BQU0sRUFBRSxHQUFHLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUM1QixPQUFPLE1BQU0sQ0FBQyxLQUFLLENBQUMsTUFBTSxDQUFDLENBQUM7SUFDOUIsQ0FBQztJQVJlLHlCQUFpQixvQkFRaEM7QUFDSCxDQUFDLEVBekJTLE9BQU8sS0FBUCxPQUFPLFFBeUJoQiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYXJrZG93bnZpZXdlci9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21hcmtkb3dudmlld2VyL3NyYy90b2MudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21hcmtkb3dudmlld2VyL3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21hcmtkb3dudmlld2VyL3NyYy93aWRnZXQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWFya2Rvd252aWV3ZXJcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL3RvYyc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSU1hcmtkb3duUGFyc2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQge1xuICBUYWJsZU9mQ29udGVudHMsXG4gIFRhYmxlT2ZDb250ZW50c0ZhY3RvcnksXG4gIFRhYmxlT2ZDb250ZW50c01vZGVsLFxuICBUYWJsZU9mQ29udGVudHNVdGlsc1xufSBmcm9tICdAanVweXRlcmxhYi90b2MnO1xuaW1wb3J0IHsgTWFya2Rvd25Eb2N1bWVudCB9IGZyb20gJy4vd2lkZ2V0JztcblxuLyoqXG4gKiBJbnRlcmZhY2UgZGVzY3JpYmluZyBhIE1hcmtkb3duIHZpZXdlciBoZWFkaW5nLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElNYXJrZG93blZpZXdlckhlYWRpbmdcbiAgZXh0ZW5kcyBUYWJsZU9mQ29udGVudHNVdGlscy5NYXJrZG93bi5JTWFya2Rvd25IZWFkaW5nIHt9XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudCBtb2RlbCBmb3IgTWFya2Rvd24gdmlld2VyIGZpbGVzLlxuICovXG5leHBvcnQgY2xhc3MgTWFya2Rvd25WaWV3ZXJUYWJsZU9mQ29udGVudHNNb2RlbCBleHRlbmRzIFRhYmxlT2ZDb250ZW50c01vZGVsPFxuICBJTWFya2Rvd25WaWV3ZXJIZWFkaW5nLFxuICBNYXJrZG93bkRvY3VtZW50XG4+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdG9yXG4gICAqXG4gICAqIEBwYXJhbSB3aWRnZXQgVGhlIHdpZGdldCB0byBzZWFyY2ggaW5cbiAgICogQHBhcmFtIHBhcnNlciBNYXJrZG93biBwYXJzZXJcbiAgICogQHBhcmFtIGNvbmZpZ3VyYXRpb24gRGVmYXVsdCBtb2RlbCBjb25maWd1cmF0aW9uXG4gICAqL1xuICBjb25zdHJ1Y3RvcihcbiAgICB3aWRnZXQ6IE1hcmtkb3duRG9jdW1lbnQsXG4gICAgcHJvdGVjdGVkIHBhcnNlcjogSU1hcmtkb3duUGFyc2VyIHwgbnVsbCxcbiAgICBjb25maWd1cmF0aW9uPzogVGFibGVPZkNvbnRlbnRzLklDb25maWdcbiAgKSB7XG4gICAgc3VwZXIod2lkZ2V0LCBjb25maWd1cmF0aW9uKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUeXBlIG9mIGRvY3VtZW50IHN1cHBvcnRlZCBieSB0aGUgbW9kZWwuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogQSBgZGF0YS1kb2N1bWVudC10eXBlYCBhdHRyaWJ1dGUgd2l0aCB0aGlzIHZhbHVlIHdpbGwgYmUgc2V0XG4gICAqIG9uIHRoZSB0cmVlIHZpZXcgYC5qcC1UYWJsZU9mQ29udGVudHMtY29udGVudFtkYXRhLWRvY3VtZW50LXR5cGU9XCIuLi5cIl1gXG4gICAqL1xuICBnZXQgZG9jdW1lbnRUeXBlKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuICdtYXJrZG93bi12aWV3ZXInO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG1vZGVsIGdldHMgdXBkYXRlZCBldmVuIGlmIHRoZSB0YWJsZSBvZiBjb250ZW50cyBwYW5lbFxuICAgKiBpcyBoaWRkZW4gb3Igbm90LlxuICAgKi9cbiAgcHJvdGVjdGVkIGdldCBpc0Fsd2F5c0FjdGl2ZSgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBMaXN0IG9mIGNvbmZpZ3VyYXRpb24gb3B0aW9ucyBzdXBwb3J0ZWQgYnkgdGhlIG1vZGVsLlxuICAgKi9cbiAgZ2V0IHN1cHBvcnRlZE9wdGlvbnMoKTogKGtleW9mIFRhYmxlT2ZDb250ZW50cy5JQ29uZmlnKVtdIHtcbiAgICByZXR1cm4gWydtYXhpbWFsRGVwdGgnLCAnbnVtYmVyaW5nSDEnLCAnbnVtYmVySGVhZGVycyddO1xuICB9XG5cbiAgLyoqXG4gICAqIFByb2R1Y2UgdGhlIGhlYWRpbmdzIGZvciBhIGRvY3VtZW50LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgbGlzdCBvZiBuZXcgaGVhZGluZ3Mgb3IgYG51bGxgIGlmIG5vdGhpbmcgbmVlZHMgdG8gYmUgdXBkYXRlZC5cbiAgICovXG4gIHByb3RlY3RlZCBnZXRIZWFkaW5ncygpOiBQcm9taXNlPElNYXJrZG93blZpZXdlckhlYWRpbmdbXSB8IG51bGw+IHtcbiAgICBjb25zdCBjb250ZW50ID0gdGhpcy53aWRnZXQuY29udGV4dC5tb2RlbC50b1N0cmluZygpO1xuICAgIGNvbnN0IGhlYWRpbmdzID0gVGFibGVPZkNvbnRlbnRzVXRpbHMuZmlsdGVySGVhZGluZ3MoXG4gICAgICBUYWJsZU9mQ29udGVudHNVdGlscy5NYXJrZG93bi5nZXRIZWFkaW5ncyhjb250ZW50KSxcbiAgICAgIHtcbiAgICAgICAgLi4udGhpcy5jb25maWd1cmF0aW9uLFxuICAgICAgICAvLyBGb3JjZSBiYXNlIG51bWJlciB0byBiZSBlcXVhbCB0byAxXG4gICAgICAgIGJhc2VOdW1iZXJpbmc6IDFcbiAgICAgIH1cbiAgICApO1xuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoaGVhZGluZ3MpO1xuICB9XG59XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudCBtb2RlbCBmYWN0b3J5IGZvciBNYXJrZG93biB2aWV3ZXIgZmlsZXMuXG4gKi9cbmV4cG9ydCBjbGFzcyBNYXJrZG93blZpZXdlclRhYmxlT2ZDb250ZW50c0ZhY3RvcnkgZXh0ZW5kcyBUYWJsZU9mQ29udGVudHNGYWN0b3J5PE1hcmtkb3duRG9jdW1lbnQ+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdG9yXG4gICAqXG4gICAqIEBwYXJhbSB0cmFja2VyIFdpZGdldCB0cmFja2VyXG4gICAqIEBwYXJhbSBwYXJzZXIgTWFya2Rvd24gcGFyc2VyXG4gICAqL1xuICBjb25zdHJ1Y3RvcihcbiAgICB0cmFja2VyOiBJV2lkZ2V0VHJhY2tlcjxNYXJrZG93bkRvY3VtZW50PixcbiAgICBwcm90ZWN0ZWQgcGFyc2VyOiBJTWFya2Rvd25QYXJzZXIgfCBudWxsXG4gICkge1xuICAgIHN1cGVyKHRyYWNrZXIpO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB0YWJsZSBvZiBjb250ZW50cyBtb2RlbCBmb3IgdGhlIHdpZGdldFxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IC0gd2lkZ2V0XG4gICAqIEBwYXJhbSBjb25maWd1cmF0aW9uIC0gVGFibGUgb2YgY29udGVudHMgY29uZmlndXJhdGlvblxuICAgKiBAcmV0dXJucyBUaGUgdGFibGUgb2YgY29udGVudHMgbW9kZWxcbiAgICovXG4gIHByb3RlY3RlZCBfY3JlYXRlTmV3KFxuICAgIHdpZGdldDogTWFya2Rvd25Eb2N1bWVudCxcbiAgICBjb25maWd1cmF0aW9uPzogVGFibGVPZkNvbnRlbnRzLklDb25maWdcbiAgKTogVGFibGVPZkNvbnRlbnRzTW9kZWw8VGFibGVPZkNvbnRlbnRzLklIZWFkaW5nLCBNYXJrZG93bkRvY3VtZW50PiB7XG4gICAgY29uc3QgbW9kZWwgPSBuZXcgTWFya2Rvd25WaWV3ZXJUYWJsZU9mQ29udGVudHNNb2RlbChcbiAgICAgIHdpZGdldCxcbiAgICAgIHRoaXMucGFyc2VyLFxuICAgICAgY29uZmlndXJhdGlvblxuICAgICk7XG5cbiAgICBsZXQgaGVhZGluZ1RvRWxlbWVudCA9IG5ldyBXZWFrTWFwPFxuICAgICAgSU1hcmtkb3duVmlld2VySGVhZGluZyxcbiAgICAgIEVsZW1lbnQgfCBudWxsXG4gICAgPigpO1xuXG4gICAgY29uc3Qgb25BY3RpdmVIZWFkaW5nQ2hhbmdlZCA9IChcbiAgICAgIG1vZGVsOiBUYWJsZU9mQ29udGVudHNNb2RlbDxJTWFya2Rvd25WaWV3ZXJIZWFkaW5nLCBNYXJrZG93bkRvY3VtZW50PixcbiAgICAgIGhlYWRpbmc6IElNYXJrZG93blZpZXdlckhlYWRpbmcgfCBudWxsXG4gICAgKSA9PiB7XG4gICAgICBpZiAoaGVhZGluZykge1xuICAgICAgICBjb25zdCBlbCA9IGhlYWRpbmdUb0VsZW1lbnQuZ2V0KGhlYWRpbmcpO1xuXG4gICAgICAgIGlmIChlbCkge1xuICAgICAgICAgIGNvbnN0IHdpZGdldEJveCA9IHdpZGdldC5jb250ZW50Lm5vZGUuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCk7XG4gICAgICAgICAgY29uc3QgZWxlbWVudEJveCA9IGVsLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xuXG4gICAgICAgICAgaWYgKFxuICAgICAgICAgICAgZWxlbWVudEJveC50b3AgPiB3aWRnZXRCb3guYm90dG9tIHx8XG4gICAgICAgICAgICBlbGVtZW50Qm94LmJvdHRvbSA8IHdpZGdldEJveC50b3BcbiAgICAgICAgICApIHtcbiAgICAgICAgICAgIGVsLnNjcm9sbEludG9WaWV3KHsgYmxvY2s6ICdjZW50ZXInIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBjb25zb2xlLndhcm4oXG4gICAgICAgICAgICAnSGVhZGluZyBlbGVtZW50IG5vdCBmb3VuZCBmb3IgaGVhZGluZycsXG4gICAgICAgICAgICBoZWFkaW5nLFxuICAgICAgICAgICAgJ2luIHdpZGdldCcsXG4gICAgICAgICAgICB3aWRnZXRcbiAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfTtcblxuICAgIGNvbnN0IG9uSGVhZGluZ3NDaGFuZ2VkID0gKCkgPT4ge1xuICAgICAgaWYgKCF0aGlzLnBhcnNlcikge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIC8vIENsZWFyIGFsbCBudW1iZXJpbmcgaXRlbXNcbiAgICAgIFRhYmxlT2ZDb250ZW50c1V0aWxzLmNsZWFyTnVtYmVyaW5nKHdpZGdldC5jb250ZW50Lm5vZGUpO1xuXG4gICAgICAvLyBDcmVhdGUgYSBuZXcgbWFwcGluZ1xuICAgICAgaGVhZGluZ1RvRWxlbWVudCA9IG5ldyBXZWFrTWFwPElNYXJrZG93blZpZXdlckhlYWRpbmcsIEVsZW1lbnQgfCBudWxsPigpO1xuICAgICAgbW9kZWwuaGVhZGluZ3MuZm9yRWFjaChhc3luYyBoZWFkaW5nID0+IHtcbiAgICAgICAgY29uc3QgZWxlbWVudElkID0gYXdhaXQgVGFibGVPZkNvbnRlbnRzVXRpbHMuTWFya2Rvd24uZ2V0SGVhZGluZ0lkKFxuICAgICAgICAgIHRoaXMucGFyc2VyISxcbiAgICAgICAgICBoZWFkaW5nLnJhdyxcbiAgICAgICAgICBoZWFkaW5nLmxldmVsXG4gICAgICAgICk7XG5cbiAgICAgICAgaWYgKCFlbGVtZW50SWQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3Qgc2VsZWN0b3IgPSBgaCR7aGVhZGluZy5sZXZlbH1baWQ9XCIke2VsZW1lbnRJZH1cIl1gO1xuXG4gICAgICAgIGhlYWRpbmdUb0VsZW1lbnQuc2V0KFxuICAgICAgICAgIGhlYWRpbmcsXG4gICAgICAgICAgVGFibGVPZkNvbnRlbnRzVXRpbHMuYWRkUHJlZml4KFxuICAgICAgICAgICAgd2lkZ2V0LmNvbnRlbnQubm9kZSxcbiAgICAgICAgICAgIHNlbGVjdG9yLFxuICAgICAgICAgICAgaGVhZGluZy5wcmVmaXggPz8gJydcbiAgICAgICAgICApXG4gICAgICAgICk7XG4gICAgICB9KTtcbiAgICB9O1xuXG4gICAgdm9pZCB3aWRnZXQuY29udGVudC5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgIG9uSGVhZGluZ3NDaGFuZ2VkKCk7XG5cbiAgICAgIHdpZGdldC5jb250ZW50LnJlbmRlcmVkLmNvbm5lY3Qob25IZWFkaW5nc0NoYW5nZWQpO1xuICAgICAgbW9kZWwuYWN0aXZlSGVhZGluZ0NoYW5nZWQuY29ubmVjdChvbkFjdGl2ZUhlYWRpbmdDaGFuZ2VkKTtcbiAgICAgIG1vZGVsLmhlYWRpbmdzQ2hhbmdlZC5jb25uZWN0KG9uSGVhZGluZ3NDaGFuZ2VkKTtcbiAgICAgIHdpZGdldC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgd2lkZ2V0LmNvbnRlbnQucmVuZGVyZWQuZGlzY29ubmVjdChvbkhlYWRpbmdzQ2hhbmdlZCk7XG4gICAgICAgIG1vZGVsLmFjdGl2ZUhlYWRpbmdDaGFuZ2VkLmRpc2Nvbm5lY3Qob25BY3RpdmVIZWFkaW5nQ2hhbmdlZCk7XG4gICAgICAgIG1vZGVsLmhlYWRpbmdzQ2hhbmdlZC5kaXNjb25uZWN0KG9uSGVhZGluZ3NDaGFuZ2VkKTtcbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgcmV0dXJuIG1vZGVsO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNYXJrZG93bkRvY3VtZW50IH0gZnJvbSAnLi93aWRnZXQnO1xuXG4vKipcbiAqIFRoZSBtYXJrZG93bnZpZXdlciB0cmFja2VyIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSU1hcmtkb3duVmlld2VyVHJhY2tlciA9IG5ldyBUb2tlbjxJTWFya2Rvd25WaWV3ZXJUcmFja2VyPihcbiAgJ0BqdXB5dGVybGFiL21hcmtkb3dudmlld2VyOklNYXJrZG93blZpZXdlclRyYWNrZXInLFxuICBgQSB3aWRnZXQgdHJhY2tlciBmb3IgbWFya2Rvd25cbiAgZG9jdW1lbnQgdmlld2Vycy4gVXNlIHRoaXMgaWYgeW91IHdhbnQgdG8gaXRlcmF0ZSBvdmVyIGFuZCBpbnRlcmFjdCB3aXRoIHJlbmRlcmVkIG1hcmtkb3duIGRvY3VtZW50cy5gXG4pO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgbWFya2Rvd24gdmlld2VyIHdpZGdldHMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU1hcmtkb3duVmlld2VyVHJhY2tlclxuICBleHRlbmRzIElXaWRnZXRUcmFja2VyPE1hcmtkb3duRG9jdW1lbnQ+IHt9XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IHNob3dFcnJvck1lc3NhZ2UgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBBY3Rpdml0eU1vbml0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHtcbiAgQUJDV2lkZ2V0RmFjdG9yeSxcbiAgRG9jdW1lbnRSZWdpc3RyeSxcbiAgRG9jdW1lbnRXaWRnZXRcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgSVJlbmRlck1pbWUsXG4gIElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIE1pbWVNb2RlbFxufSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgSlNPTk9iamVjdCwgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVzc2FnZSB9IGZyb20gJ0BsdW1pbm8vbWVzc2FnaW5nJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFN0YWNrZWRMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYSBtYXJrZG93biB2aWV3ZXIuXG4gKi9cbmNvbnN0IE1BUktET1dOVklFV0VSX0NMQVNTID0gJ2pwLU1hcmtkb3duVmlld2VyJztcblxuLyoqXG4gKiBUaGUgbWFya2Rvd24gTUlNRSB0eXBlLlxuICovXG5jb25zdCBNSU1FVFlQRSA9ICd0ZXh0L21hcmtkb3duJztcblxuLyoqXG4gKiBBIHdpZGdldCBmb3IgbWFya2Rvd24gZG9jdW1lbnRzLlxuICovXG5leHBvcnQgY2xhc3MgTWFya2Rvd25WaWV3ZXIgZXh0ZW5kcyBXaWRnZXQge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IG1hcmtkb3duIHZpZXdlciB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBNYXJrZG93blZpZXdlci5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5jb250ZXh0ID0gb3B0aW9ucy5jb250ZXh0O1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgdGhpcy5yZW5kZXJlciA9IG9wdGlvbnMucmVuZGVyZXI7XG4gICAgdGhpcy5ub2RlLnRhYkluZGV4ID0gMDtcbiAgICB0aGlzLmFkZENsYXNzKE1BUktET1dOVklFV0VSX0NMQVNTKTtcblxuICAgIGNvbnN0IGxheW91dCA9ICh0aGlzLmxheW91dCA9IG5ldyBTdGFja2VkTGF5b3V0KCkpO1xuICAgIGxheW91dC5hZGRXaWRnZXQodGhpcy5yZW5kZXJlcik7XG5cbiAgICB2b2lkIHRoaXMuY29udGV4dC5yZWFkeS50aGVuKGFzeW5jICgpID0+IHtcbiAgICAgIGF3YWl0IHRoaXMuX3JlbmRlcigpO1xuXG4gICAgICAvLyBUaHJvdHRsZSB0aGUgcmVuZGVyaW5nIHJhdGUgb2YgdGhlIHdpZGdldC5cbiAgICAgIHRoaXMuX21vbml0b3IgPSBuZXcgQWN0aXZpdHlNb25pdG9yKHtcbiAgICAgICAgc2lnbmFsOiB0aGlzLmNvbnRleHQubW9kZWwuY29udGVudENoYW5nZWQsXG4gICAgICAgIHRpbWVvdXQ6IHRoaXMuX2NvbmZpZy5yZW5kZXJUaW1lb3V0XG4gICAgICB9KTtcbiAgICAgIHRoaXMuX21vbml0b3IuYWN0aXZpdHlTdG9wcGVkLmNvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuXG4gICAgICB0aGlzLl9yZWFkeS5yZXNvbHZlKHVuZGVmaW5lZCk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgbWFya2Rvd24gdmlld2VyIGlzIHJlYWR5LlxuICAgKi9cbiAgZ2V0IHJlYWR5KCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9yZWFkeS5wcm9taXNlO1xuICB9XG5cbiAgLyoqXG4gICAqIFNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGNvbnRlbnQgaGFzIGJlZW4gcmVuZGVyZWQuXG4gICAqL1xuICBnZXQgcmVuZGVyZWQoKTogSVNpZ25hbDxNYXJrZG93blZpZXdlciwgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9yZW5kZXJlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgVVJJIGZyYWdtZW50IGlkZW50aWZpZXIuXG4gICAqL1xuICBzZXRGcmFnbWVudChmcmFnbWVudDogc3RyaW5nKTogdm9pZCB7XG4gICAgdGhpcy5fZnJhZ21lbnQgPSBmcmFnbWVudDtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIGNvbmZpZyBvcHRpb24gZm9yIHRoZSBtYXJrZG93biB2aWV3ZXIuXG4gICAqL1xuICBzZXRPcHRpb248SyBleHRlbmRzIGtleW9mIE1hcmtkb3duVmlld2VyLklDb25maWc+KFxuICAgIG9wdGlvbjogSyxcbiAgICB2YWx1ZTogTWFya2Rvd25WaWV3ZXIuSUNvbmZpZ1tLXVxuICApOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fY29uZmlnW29wdGlvbl0gPT09IHZhbHVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2NvbmZpZ1tvcHRpb25dID0gdmFsdWU7XG4gICAgY29uc3QgeyBzdHlsZSB9ID0gdGhpcy5yZW5kZXJlci5ub2RlO1xuICAgIHN3aXRjaCAob3B0aW9uKSB7XG4gICAgICBjYXNlICdmb250RmFtaWx5JzpcbiAgICAgICAgc3R5bGUuc2V0UHJvcGVydHkoJ2ZvbnQtZmFtaWx5JywgdmFsdWUgYXMgc3RyaW5nIHwgbnVsbCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnZm9udFNpemUnOlxuICAgICAgICBzdHlsZS5zZXRQcm9wZXJ0eSgnZm9udC1zaXplJywgdmFsdWUgPyB2YWx1ZSArICdweCcgOiBudWxsKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdoaWRlRnJvbnRNYXR0ZXInOlxuICAgICAgICB0aGlzLnVwZGF0ZSgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2xpbmVIZWlnaHQnOlxuICAgICAgICBzdHlsZS5zZXRQcm9wZXJ0eSgnbGluZS1oZWlnaHQnLCB2YWx1ZSA/IHZhbHVlLnRvU3RyaW5nKCkgOiBudWxsKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdsaW5lV2lkdGgnOiB7XG4gICAgICAgIGNvbnN0IHBhZGRpbmcgPSB2YWx1ZSA/IGBjYWxjKDUwJSAtICR7KHZhbHVlIGFzIG51bWJlcikgLyAyfWNoKWAgOiBudWxsO1xuICAgICAgICBzdHlsZS5zZXRQcm9wZXJ0eSgncGFkZGluZy1sZWZ0JywgcGFkZGluZyk7XG4gICAgICAgIHN0eWxlLnNldFByb3BlcnR5KCdwYWRkaW5nLXJpZ2h0JywgcGFkZGluZyk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgICAgY2FzZSAncmVuZGVyVGltZW91dCc6XG4gICAgICAgIGlmICh0aGlzLl9tb25pdG9yKSB7XG4gICAgICAgICAgdGhpcy5fbW9uaXRvci50aW1lb3V0ID0gdmFsdWUgYXMgbnVtYmVyO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyBoZWxkIGJ5IHRoZSB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKHRoaXMuX21vbml0b3IpIHtcbiAgICAgIHRoaXMuX21vbml0b3IuZGlzcG9zZSgpO1xuICAgIH1cbiAgICB0aGlzLl9tb25pdG9yID0gbnVsbDtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFuIGB1cGRhdGUtcmVxdWVzdGAgbWVzc2FnZSB0byB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5jb250ZXh0LmlzUmVhZHkgJiYgIXRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgdm9pZCB0aGlzLl9yZW5kZXIoKTtcbiAgICAgIHRoaXMuX2ZyYWdtZW50ID0gJyc7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FjdGl2YXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2YXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLm5vZGUuZm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgdGhlIG1pbWUgY29udGVudC5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3JlbmRlcigpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gU2luY2UgcmVuZGVyaW5nIGlzIGFzeW5jLCB3ZSBub3RlIHJlbmRlciByZXF1ZXN0cyB0aGF0IGhhcHBlbiB3aGlsZSB3ZVxuICAgIC8vIGFjdHVhbGx5IGFyZSByZW5kZXJpbmcgZm9yIGEgZnV0dXJlIHJlbmRlcmluZy5cbiAgICBpZiAodGhpcy5faXNSZW5kZXJpbmcpIHtcbiAgICAgIHRoaXMuX3JlbmRlclJlcXVlc3RlZCA9IHRydWU7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gU2V0IHVwIGZvciB0aGlzIHJlbmRlcmluZyBwYXNzLlxuICAgIHRoaXMuX3JlbmRlclJlcXVlc3RlZCA9IGZhbHNlO1xuICAgIGNvbnN0IHsgY29udGV4dCB9ID0gdGhpcztcbiAgICBjb25zdCB7IG1vZGVsIH0gPSBjb250ZXh0O1xuICAgIGNvbnN0IHNvdXJjZSA9IG1vZGVsLnRvU3RyaW5nKCk7XG4gICAgY29uc3QgZGF0YTogSlNPTk9iamVjdCA9IHt9O1xuICAgIC8vIElmIGBoaWRlRnJvbnRNYXR0ZXJgaXMgdHJ1ZSByZW1vdmUgZnJvbnQgbWF0dGVyLlxuICAgIGRhdGFbTUlNRVRZUEVdID0gdGhpcy5fY29uZmlnLmhpZGVGcm9udE1hdHRlclxuICAgICAgPyBQcml2YXRlLnJlbW92ZUZyb250TWF0dGVyKHNvdXJjZSlcbiAgICAgIDogc291cmNlO1xuICAgIGNvbnN0IG1pbWVNb2RlbCA9IG5ldyBNaW1lTW9kZWwoe1xuICAgICAgZGF0YSxcbiAgICAgIG1ldGFkYXRhOiB7IGZyYWdtZW50OiB0aGlzLl9mcmFnbWVudCB9XG4gICAgfSk7XG5cbiAgICB0cnkge1xuICAgICAgLy8gRG8gdGhlIHJlbmRlcmluZyBhc3luY2hyb25vdXNseS5cbiAgICAgIHRoaXMuX2lzUmVuZGVyaW5nID0gdHJ1ZTtcbiAgICAgIGF3YWl0IHRoaXMucmVuZGVyZXIucmVuZGVyTW9kZWwobWltZU1vZGVsKTtcbiAgICAgIHRoaXMuX2lzUmVuZGVyaW5nID0gZmFsc2U7XG5cbiAgICAgIC8vIElmIHRoZXJlIGlzIGFuIG91dHN0YW5kaW5nIHJlcXVlc3QgdG8gcmVuZGVyLCBnbyBhaGVhZCBhbmQgcmVuZGVyXG4gICAgICBpZiAodGhpcy5fcmVuZGVyUmVxdWVzdGVkKSB7XG4gICAgICAgIHJldHVybiB0aGlzLl9yZW5kZXIoKTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuX3JlbmRlcmVkLmVtaXQoKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChyZWFzb24pIHtcbiAgICAgIC8vIERpc3Bvc2UgdGhlIGRvY3VtZW50IGlmIHJlbmRlcmluZyBmYWlscy5cbiAgICAgIHJlcXVlc3RBbmltYXRpb25GcmFtZSgoKSA9PiB7XG4gICAgICAgIHRoaXMuZGlzcG9zZSgpO1xuICAgICAgfSk7XG4gICAgICB2b2lkIHNob3dFcnJvck1lc3NhZ2UoXG4gICAgICAgIHRoaXMuX3RyYW5zLl9fKCdSZW5kZXJlciBGYWlsdXJlOiAlMScsIGNvbnRleHQucGF0aCksXG4gICAgICAgIHJlYXNvblxuICAgICAgKTtcbiAgICB9XG4gIH1cblxuICByZWFkb25seSBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQ7XG4gIHJlYWRvbmx5IHJlbmRlcmVyOiBJUmVuZGVyTWltZS5JUmVuZGVyZXI7XG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9jb25maWcgPSB7IC4uLk1hcmtkb3duVmlld2VyLmRlZmF1bHRDb25maWcgfTtcbiAgcHJpdmF0ZSBfZnJhZ21lbnQgPSAnJztcbiAgcHJpdmF0ZSBfbW9uaXRvcjogQWN0aXZpdHlNb25pdG9yPERvY3VtZW50UmVnaXN0cnkuSU1vZGVsLCB2b2lkPiB8IG51bGw7XG4gIHByaXZhdGUgX3JlYWR5ID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xuICBwcml2YXRlIF9pc1JlbmRlcmluZyA9IGZhbHNlO1xuICBwcml2YXRlIF9yZW5kZXJSZXF1ZXN0ZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfcmVuZGVyZWQgPSBuZXcgU2lnbmFsPE1hcmtkb3duVmlld2VyLCB2b2lkPih0aGlzKTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBNYXJrZG93blZpZXdlciBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE1hcmtkb3duVmlld2VyIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhIE1hcmtkb3duVmlld2VyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogQ29udGV4dFxuICAgICAqL1xuICAgIGNvbnRleHQ6IERvY3VtZW50UmVnaXN0cnkuSUNvbnRleHQ8RG9jdW1lbnRSZWdpc3RyeS5JTW9kZWw+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlbmRlcmVyIGluc3RhbmNlLlxuICAgICAqL1xuICAgIHJlbmRlcmVyOiBJUmVuZGVyTWltZS5JUmVuZGVyZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cblxuICBleHBvcnQgaW50ZXJmYWNlIElDb25maWcge1xuICAgIC8qKlxuICAgICAqIFVzZXIgcHJlZmVycmVkIGZvbnQgZmFtaWx5IGZvciBtYXJrZG93biB2aWV3ZXIuXG4gICAgICovXG4gICAgZm9udEZhbWlseTogc3RyaW5nIHwgbnVsbDtcblxuICAgIC8qKlxuICAgICAqIFVzZXIgcHJlZmVycmVkIHNpemUgaW4gcGl4ZWwgb2YgdGhlIGZvbnQgdXNlZCBpbiBtYXJrZG93biB2aWV3ZXIuXG4gICAgICovXG4gICAgZm9udFNpemU6IG51bWJlciB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBVc2VyIHByZWZlcnJlZCB0ZXh0IGxpbmUgaGVpZ2h0LCBhcyBhIG11bHRpcGxpZXIgb2YgZm9udCBzaXplLlxuICAgICAqL1xuICAgIGxpbmVIZWlnaHQ6IG51bWJlciB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBVc2VyIHByZWZlcnJlZCB0ZXh0IGxpbmUgd2lkdGggZXhwcmVzc2VkIGluIENTUyBjaCB1bml0cy5cbiAgICAgKi9cbiAgICBsaW5lV2lkdGg6IG51bWJlciB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGhpZGUgdGhlIFlBTUwgZnJvbnQgbWF0dGVyLlxuICAgICAqL1xuICAgIGhpZGVGcm9udE1hdHRlcjogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZW5kZXIgdGltZW91dC5cbiAgICAgKi9cbiAgICByZW5kZXJUaW1lb3V0OiBudW1iZXI7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRlZmF1bHQgY29uZmlndXJhdGlvbiBvcHRpb25zIGZvciBhbiBlZGl0b3IuXG4gICAqL1xuICBleHBvcnQgY29uc3QgZGVmYXVsdENvbmZpZzogTWFya2Rvd25WaWV3ZXIuSUNvbmZpZyA9IHtcbiAgICBmb250RmFtaWx5OiBudWxsLFxuICAgIGZvbnRTaXplOiBudWxsLFxuICAgIGxpbmVIZWlnaHQ6IG51bGwsXG4gICAgbGluZVdpZHRoOiBudWxsLFxuICAgIGhpZGVGcm9udE1hdHRlcjogdHJ1ZSxcbiAgICByZW5kZXJUaW1lb3V0OiAxMDAwXG4gIH07XG59XG5cbi8qKlxuICogQSBkb2N1bWVudCB3aWRnZXQgZm9yIG1hcmtkb3duIGNvbnRlbnQuXG4gKi9cbmV4cG9ydCBjbGFzcyBNYXJrZG93bkRvY3VtZW50IGV4dGVuZHMgRG9jdW1lbnRXaWRnZXQ8TWFya2Rvd25WaWV3ZXI+IHtcbiAgc2V0RnJhZ21lbnQoZnJhZ21lbnQ6IHN0cmluZyk6IHZvaWQge1xuICAgIHRoaXMuY29udGVudC5zZXRGcmFnbWVudChmcmFnbWVudCk7XG4gIH1cbn1cblxuLyoqXG4gKiBBIHdpZGdldCBmYWN0b3J5IGZvciBtYXJrZG93biB2aWV3ZXJzLlxuICovXG5leHBvcnQgY2xhc3MgTWFya2Rvd25WaWV3ZXJGYWN0b3J5IGV4dGVuZHMgQUJDV2lkZ2V0RmFjdG9yeTxNYXJrZG93bkRvY3VtZW50PiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgbWFya2Rvd24gdmlld2VyIHdpZGdldCBmYWN0b3J5LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTWFya2Rvd25WaWV3ZXJGYWN0b3J5LklPcHRpb25zKSB7XG4gICAgc3VwZXIoUHJpdmF0ZS5jcmVhdGVSZWdpc3RyeU9wdGlvbnMob3B0aW9ucykpO1xuICAgIHRoaXMuX2ZpbGVUeXBlID0gb3B0aW9ucy5wcmltYXJ5RmlsZVR5cGU7XG4gICAgdGhpcy5fcmVuZGVybWltZSA9IG9wdGlvbnMucmVuZGVybWltZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGdpdmVuIGEgY29udGV4dC5cbiAgICovXG4gIHByb3RlY3RlZCBjcmVhdGVOZXdXaWRnZXQoXG4gICAgY29udGV4dDogRG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0XG4gICk6IE1hcmtkb3duRG9jdW1lbnQge1xuICAgIGNvbnN0IHJlbmRlcm1pbWUgPSB0aGlzLl9yZW5kZXJtaW1lLmNsb25lKHtcbiAgICAgIHJlc29sdmVyOiBjb250ZXh0LnVybFJlc29sdmVyXG4gICAgfSk7XG4gICAgY29uc3QgcmVuZGVyZXIgPSByZW5kZXJtaW1lLmNyZWF0ZVJlbmRlcmVyKE1JTUVUWVBFKTtcbiAgICBjb25zdCBjb250ZW50ID0gbmV3IE1hcmtkb3duVmlld2VyKHsgY29udGV4dCwgcmVuZGVyZXIgfSk7XG4gICAgY29udGVudC50aXRsZS5pY29uID0gdGhpcy5fZmlsZVR5cGU/Lmljb247XG4gICAgY29udGVudC50aXRsZS5pY29uQ2xhc3MgPSB0aGlzLl9maWxlVHlwZT8uaWNvbkNsYXNzID8/ICcnO1xuICAgIGNvbnRlbnQudGl0bGUuaWNvbkxhYmVsID0gdGhpcy5fZmlsZVR5cGU/Lmljb25MYWJlbCA/PyAnJztcbiAgICBjb250ZW50LnRpdGxlLmNhcHRpb24gPSB0aGlzLmxhYmVsO1xuICAgIGNvbnN0IHdpZGdldCA9IG5ldyBNYXJrZG93bkRvY3VtZW50KHsgY29udGVudCwgY29udGV4dCB9KTtcblxuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICBwcml2YXRlIF9maWxlVHlwZTogRG9jdW1lbnRSZWdpc3RyeS5JRmlsZVR5cGUgfCB1bmRlZmluZWQ7XG4gIHByaXZhdGUgX3JlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnk7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgTWFya2Rvd25WaWV3ZXJGYWN0b3J5IGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgTWFya2Rvd25WaWV3ZXJGYWN0b3J5IHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhIE1hcmtkb3duVmlld2VyRmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMgZXh0ZW5kcyBEb2N1bWVudFJlZ2lzdHJ5LklXaWRnZXRGYWN0b3J5T3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIHByaW1hcnkgZmlsZSB0eXBlIGFzc29jaWF0ZWQgd2l0aCB0aGUgZG9jdW1lbnQuXG4gICAgICovXG4gICAgcHJpbWFyeUZpbGVUeXBlOiBEb2N1bWVudFJlZ2lzdHJ5LklGaWxlVHlwZSB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZW5kZXJtaW1lIGluc3RhbmNlLlxuICAgICAqL1xuICAgIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnk7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgbWFya2Rvd24gdmlld2VyIHdpZGdldCBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIENyZWF0ZSB0aGUgZG9jdW1lbnQgcmVnaXN0cnkgb3B0aW9ucy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBjcmVhdGVSZWdpc3RyeU9wdGlvbnMoXG4gICAgb3B0aW9uczogTWFya2Rvd25WaWV3ZXJGYWN0b3J5LklPcHRpb25zXG4gICk6IERvY3VtZW50UmVnaXN0cnkuSVdpZGdldEZhY3RvcnlPcHRpb25zIHtcbiAgICByZXR1cm4ge1xuICAgICAgLi4ub3B0aW9ucyxcbiAgICAgIHJlYWRPbmx5OiB0cnVlXG4gICAgfSBhcyBEb2N1bWVudFJlZ2lzdHJ5LklXaWRnZXRGYWN0b3J5T3B0aW9ucztcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgWUFNTCBmcm9udCBtYXR0ZXIgZnJvbSBzb3VyY2UuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVtb3ZlRnJvbnRNYXR0ZXIoc291cmNlOiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIGNvbnN0IHJlID0gL14tLS1cXG5bXl0qP1xcbigtLS18Li4uKVxcbi87XG4gICAgY29uc3QgbWF0Y2ggPSBzb3VyY2UubWF0Y2gocmUpO1xuICAgIGlmICghbWF0Y2gpIHtcbiAgICAgIHJldHVybiBzb3VyY2U7XG4gICAgfVxuICAgIGNvbnN0IHsgbGVuZ3RoIH0gPSBtYXRjaFswXTtcbiAgICByZXR1cm4gc291cmNlLnNsaWNlKGxlbmd0aCk7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==