"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mermaid_lib_index_js"],{

/***/ "../packages/mermaid/lib/index.js":
/*!****************************************!*\
  !*** ../packages/mermaid/lib/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DETAILS_CLASS": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.DETAILS_CLASS),
/* harmony export */   "IMermaidManager": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IMermaidManager),
/* harmony export */   "IMermaidMarkdown": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IMermaidMarkdown),
/* harmony export */   "MERMAID_CLASS": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.MERMAID_CLASS),
/* harmony export */   "MERMAID_CODE_CLASS": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.MERMAID_CODE_CLASS),
/* harmony export */   "MERMAID_DARK_THEME": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.MERMAID_DARK_THEME),
/* harmony export */   "MERMAID_DEFAULT_THEME": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.MERMAID_DEFAULT_THEME),
/* harmony export */   "MERMAID_FILE_EXTENSIONS": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.MERMAID_FILE_EXTENSIONS),
/* harmony export */   "MERMAID_MIME_TYPE": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.MERMAID_MIME_TYPE),
/* harmony export */   "MermaidManager": () => (/* reexport safe */ _manager__WEBPACK_IMPORTED_MODULE_0__.MermaidManager),
/* harmony export */   "MermaidMarkdown": () => (/* reexport safe */ _markdown__WEBPACK_IMPORTED_MODULE_1__.MermaidMarkdown),
/* harmony export */   "RenderedMermaid": () => (/* reexport safe */ _mime__WEBPACK_IMPORTED_MODULE_2__.RenderedMermaid),
/* harmony export */   "SUMMARY_CLASS": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.SUMMARY_CLASS),
/* harmony export */   "WARNING_CLASS": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.WARNING_CLASS),
/* harmony export */   "rendererFactory": () => (/* reexport safe */ _mime__WEBPACK_IMPORTED_MODULE_2__.rendererFactory)
/* harmony export */ });
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./manager */ "../packages/mermaid/lib/manager.js");
/* harmony import */ var _markdown__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./markdown */ "../packages/mermaid/lib/markdown.js");
/* harmony import */ var _mime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./mime */ "../packages/mermaid/lib/mime.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "../packages/mermaid/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mermaid
 */






/***/ }),

/***/ "../packages/mermaid/lib/manager.js":
/*!******************************************!*\
  !*** ../packages/mermaid/lib/manager.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MermaidManager": () => (/* binding */ MermaidManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../packages/mermaid/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A mermaid diagram manager with cache.
 */
class MermaidManager {
    constructor(options = {}) {
        this._diagrams = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.LruCache({ maxSize: options.maxCacheSize || null });
        // handle reacting to themes
        if (options.themes) {
            Private.initThemes(options.themes || null);
            options.themes.themeChanged.connect(this.initialize, this);
        }
    }
    /**
     * Handle (re)-initializing mermaid based on external values.
     */
    initialize() {
        this._diagrams.clear();
        Private.initMermaid();
    }
    /**
     * Get the underlying, potentially un-initialized mermaid module.
     */
    async getMermaid() {
        return await Private.ensureMermaid();
    }
    /**
     * Get the version of the currently-loaded mermaid module
     */
    getMermaidVersion() {
        return Private.version();
    }
    /**
     * Get a pre-cached mermaid figure.
     *
     * This primarily exists for the needs of `marked`, which supports async node
     * visitors, but not async rendering.
     */
    getCachedFigure(text) {
        return this._diagrams.get(text);
    }
    /**
     * Attempt a raw rendering of mermaid to an SVG string, extracting some metadata.
     */
    async renderSvg(text) {
        const _mermaid = await this.getMermaid();
        const id = `jp-mermaid-${Private.nextMermaidId()}`;
        // create temporary element into which to render
        const el = document.createElement('div');
        document.body.appendChild(el);
        try {
            const { svg } = await _mermaid.render(id, text, el);
            const parser = new DOMParser();
            const doc = parser.parseFromString(svg, 'image/svg+xml');
            const info = { text, svg };
            const svgEl = doc.querySelector('svg');
            const { maxWidth } = (svgEl === null || svgEl === void 0 ? void 0 : svgEl.style) || {};
            info.width = maxWidth ? parseFloat(maxWidth) : null;
            const firstTitle = doc.querySelector('title');
            const firstDesc = doc.querySelector('desc');
            if (firstTitle) {
                info.accessibleTitle = firstTitle.textContent;
            }
            if (firstDesc) {
                info.accessibleDescription = firstDesc.textContent;
            }
            return info;
        }
        finally {
            el.remove();
        }
    }
    /**
     * Provide and cache a fully-rendered element, checking the cache first.
     */
    async renderFigure(text) {
        // bail if already cached
        let output = this._diagrams.get(text);
        if (output != null) {
            return output;
        }
        let className = _tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_CLASS;
        let result = null;
        // the element that will be returned
        output = document.createElement('div');
        output.className = className;
        try {
            const response = await this.renderSvg(text);
            result = this.makeMermaidFigure(response);
        }
        catch (err) {
            output.classList.add(_tokens__WEBPACK_IMPORTED_MODULE_2__.WARNING_CLASS);
            result = await this.makeMermaidError(text);
        }
        let version = this.getMermaidVersion();
        if (version) {
            result.dataset.jpMermaidVersion = version;
        }
        output.appendChild(result);
        // update the cache for use when rendering synchronously
        this._diagrams.set(text, output);
        return output;
    }
    /**
     * Provide a code block with the mermaid source.
     */
    makeMermaidCode(text) {
        // append the source
        const pre = document.createElement('pre');
        const code = document.createElement('code');
        code.innerText = text;
        pre.appendChild(code);
        code.className = _tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_CODE_CLASS;
        code.textContent = text;
        return pre;
    }
    /**
     * Get the parser message element from a failed parse.
     *
     * This doesn't do much of anything if the text is successfully parsed.
     */
    async makeMermaidError(text) {
        const _mermaid = await this.getMermaid();
        let errorMessage = '';
        try {
            await _mermaid.parse(text);
        }
        catch (err) {
            errorMessage = `${err}`;
        }
        const result = document.createElement('details');
        result.className = _tokens__WEBPACK_IMPORTED_MODULE_2__.DETAILS_CLASS;
        const summary = document.createElement('summary');
        summary.className = _tokens__WEBPACK_IMPORTED_MODULE_2__.SUMMARY_CLASS;
        summary.appendChild(this.makeMermaidCode(text));
        result.appendChild(summary);
        const warning = document.createElement('pre');
        warning.innerText = errorMessage;
        result.appendChild(warning);
        return result;
    }
    /**
     * Extract extra attributes to add to a generated figure.
     */
    makeMermaidFigure(info) {
        const figure = document.createElement('figure');
        const img = document.createElement('img');
        figure.appendChild(img);
        img.setAttribute('src', `data:image/svg+xml,${encodeURIComponent(info.svg)}`);
        // add dimension information
        if (info.width) {
            img.width = info.width;
        }
        // add accessible alt title
        if (info.accessibleTitle) {
            img.setAttribute('alt', info.accessibleTitle);
        }
        figure.appendChild(this.makeMermaidCode(info.text));
        // add accessible caption, with fallback to raw mermaid source
        if (info.accessibleDescription) {
            const caption = document.createElement('figcaption');
            caption.className = 'sr-only';
            caption.textContent = info.accessibleDescription;
            figure.appendChild(caption);
        }
        return figure;
    }
}
/**
 * A namespace for global, private mermaid data.
 */
var Private;
(function (Private) {
    let _themes = null;
    let _mermaid = null;
    let _loading = null;
    let _nextMermaidId = 0;
    let _version = null;
    /**
     * Cache a reference to the theme manager.
     */
    function initThemes(themes) {
        _themes = themes;
    }
    Private.initThemes = initThemes;
    /**
     * Get the version of mermaid used for rendering.
     */
    function version() {
        return _version;
    }
    Private.version = version;
    /**
     * (Re-)initialize mermaid with lab-specific theme information
     */
    function initMermaid() {
        if (!_mermaid) {
            return false;
        }
        let theme = _tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_DEFAULT_THEME;
        if (_themes) {
            const jpTheme = _themes.theme;
            theme =
                jpTheme && _themes.isLight(jpTheme)
                    ? _tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_DEFAULT_THEME
                    : _tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_DARK_THEME;
        }
        const fontFamily = window
            .getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-font-family');
        _mermaid.mermaidAPI.globalReset();
        _mermaid.mermaidAPI.initialize({
            theme,
            fontFamily,
            maxTextSize: 100000,
            startOnLoad: false
        });
        return true;
    }
    Private.initMermaid = initMermaid;
    /**
     * Determine whether mermaid has been loaded yet.
     */
    function getMermaid() {
        return _mermaid;
    }
    Private.getMermaid = getMermaid;
    /**
     * Provide a globally-unique, but unstable, ID for disambiguation.
     */
    function nextMermaidId() {
        return _nextMermaidId++;
    }
    Private.nextMermaidId = nextMermaidId;
    /**
     * Ensure mermaid has been lazily loaded once, initialized, and cached.
     */
    async function ensureMermaid() {
        if (_mermaid != null) {
            return _mermaid;
        }
        if (_loading) {
            return _loading.promise;
        }
        _loading = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        _version = (await __webpack_require__.e(/*! import() */ "node_modules_mermaid_package_json").then(__webpack_require__.t.bind(__webpack_require__, /*! mermaid/package.json */ "../node_modules/mermaid/package.json", 19))).version;
        _mermaid = (await Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_lodash-es__Stack_js-node_modules_lodash-es__baseKeys_js-node_modules_lod-963227"), __webpack_require__.e("vendors-node_modules_d3-array_src_deviation_js-node_modules_d3-array_src_intersection_js-node-18c317"), __webpack_require__.e("vendors-node_modules_mermaid_dist_mermaid_core_mjs")]).then(__webpack_require__.bind(__webpack_require__, /*! mermaid */ "../node_modules/mermaid/dist/mermaid.core.mjs"))).default;
        initMermaid();
        _loading.resolve(_mermaid);
        return _mermaid;
    }
    Private.ensureMermaid = ensureMermaid;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/mermaid/lib/markdown.js":
/*!*******************************************!*\
  !*** ../packages/mermaid/lib/markdown.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MermaidMarkdown": () => (/* binding */ MermaidMarkdown)
/* harmony export */ });
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * An implementation of mermaid fenced code blocks in markdown.
 */
class MermaidMarkdown {
    constructor(options) {
        this.languages = ['mermaid'];
        this.rank = 100;
        this._mermaid = options.mermaid;
    }
    /**
     * Pre-parse and cache the rendered text.
     */
    async walk(text) {
        await this._mermaid.renderFigure(text);
    }
    /**
     * Render the diagram.
     */
    render(text) {
        // handle pre-cached mermaid figures
        let cachedFigure = this._mermaid.getCachedFigure(text);
        if (cachedFigure) {
            return cachedFigure.outerHTML;
        }
        return null;
    }
}


/***/ }),

/***/ "../packages/mermaid/lib/mime.js":
/*!***************************************!*\
  !*** ../packages/mermaid/lib/mime.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedMermaid": () => (/* binding */ RenderedMermaid),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../packages/mermaid/lib/tokens.js");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module mermaid-extension
 */



const SVG_MIME = 'image/svg+xml';
/**
 * A widget for rendering mermaid text-based diagrams, for usage with rendermime.
 */
class RenderedMermaid extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Create a new widget for rendering Vega/Vega-Lite.
     */
    constructor(options) {
        super();
        this._lastRendered = null;
        this._mimeType = options.mimeType;
        this.addClass(_tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_CLASS);
    }
    static set manager(manager) {
        if (RenderedMermaid._manager) {
            console.warn('Mermaid manager may only be set once, and is already set.');
            return;
        }
        RenderedMermaid._manager = manager;
        RenderedMermaid._managerReady.resolve(manager);
    }
    /**
     * Render mermaid text-based diagrams into this widget's node.
     */
    async renderModel(model) {
        const manager = await RenderedMermaid._managerReady.promise;
        const text = model.data[this._mimeType];
        if (text == null || text === this._lastRendered) {
            return;
        }
        this._lastRendered = text;
        // get a div containing a figure or parser message
        const figure = await manager.renderFigure(text);
        if (figure.classList.contains(_tokens__WEBPACK_IMPORTED_MODULE_2__.WARNING_CLASS)) {
            this.node.classList.add(_tokens__WEBPACK_IMPORTED_MODULE_2__.WARNING_CLASS);
        }
        else {
            this.node.classList.remove(_tokens__WEBPACK_IMPORTED_MODULE_2__.WARNING_CLASS);
        }
        if (!figure.firstChild) {
            return;
        }
        if (this.node.innerHTML !== figure.innerHTML) {
            this.node.innerHTML = figure.innerHTML;
        }
        // capture the version of mermaid used
        const version = manager.getMermaidVersion();
        const mermaidMetadata = {
            ...(model.metadata[_tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_MIME_TYPE] || {}),
            version
        };
        const metadata = {
            ...model.metadata,
            [_tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_MIME_TYPE]: mermaidMetadata
        };
        // if available, set the fully-rendered SVG
        const img = figure.querySelector('img');
        if (img) {
            const svg = decodeURIComponent(img.src.split(',')[1]);
            const oldSvg = model.data[SVG_MIME];
            if (svg !== oldSvg) {
                model.setData({
                    data: { ...model.data, [SVG_MIME]: svg },
                    metadata
                });
            }
        }
        else {
            const dataWithoutSvg = { ...model.data };
            delete dataWithoutSvg[SVG_MIME];
            model.setData({ data: dataWithoutSvg, metadata });
        }
    }
}
RenderedMermaid._manager = null;
RenderedMermaid._managerReady = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();

/**
 * A mime renderer factory for mermaid text-based diagrams.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [_tokens__WEBPACK_IMPORTED_MODULE_2__.MERMAID_MIME_TYPE],
    createRenderer: options => new RenderedMermaid(options)
};


/***/ }),

/***/ "../packages/mermaid/lib/tokens.js":
/*!*****************************************!*\
  !*** ../packages/mermaid/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DETAILS_CLASS": () => (/* binding */ DETAILS_CLASS),
/* harmony export */   "IMermaidManager": () => (/* binding */ IMermaidManager),
/* harmony export */   "IMermaidMarkdown": () => (/* binding */ IMermaidMarkdown),
/* harmony export */   "MERMAID_CLASS": () => (/* binding */ MERMAID_CLASS),
/* harmony export */   "MERMAID_CODE_CLASS": () => (/* binding */ MERMAID_CODE_CLASS),
/* harmony export */   "MERMAID_DARK_THEME": () => (/* binding */ MERMAID_DARK_THEME),
/* harmony export */   "MERMAID_DEFAULT_THEME": () => (/* binding */ MERMAID_DEFAULT_THEME),
/* harmony export */   "MERMAID_FILE_EXTENSIONS": () => (/* binding */ MERMAID_FILE_EXTENSIONS),
/* harmony export */   "MERMAID_MIME_TYPE": () => (/* binding */ MERMAID_MIME_TYPE),
/* harmony export */   "SUMMARY_CLASS": () => (/* binding */ SUMMARY_CLASS),
/* harmony export */   "WARNING_CLASS": () => (/* binding */ WARNING_CLASS)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// documented upstream constants
const MERMAID_MIME_TYPE = 'text/vnd.mermaid';
const MERMAID_FILE_EXTENSIONS = ['.mmd', '.mermaid'];
// mermaid themes
const MERMAID_DEFAULT_THEME = 'default';
const MERMAID_DARK_THEME = 'dark';
// DOM
const MERMAID_CLASS = 'jp-RenderedMermaid';
const MERMAID_CODE_CLASS = 'mermaid';
const WARNING_CLASS = 'jp-mod-warning';
const DETAILS_CLASS = 'jp-RenderedMermaid-Details';
const SUMMARY_CLASS = 'jp-RenderedMermaid-Summary';
/**
 * The exported token for a mermaid manager
 */
const IMermaidManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/mermaid:IMermaidManager', `a manager for rendering mermaid text-based diagrams`);
/**
 * The exported token for a mermaid manager
 */
const IMermaidMarkdown = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/mermaid:IMermaidMarkdown', `a manager for rendering mermaid text-based diagrams in markdown fenced code blocks`);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWVybWFpZF9saWJfaW5kZXhfanMuNTA3MmIyNGRhNjA4MDdmNGFlZGMuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRXVCO0FBQ0M7QUFDSjtBQUNFOzs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1Z6QiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBSVA7QUFFSDtBQWEvQjtBQUVsQjs7R0FFRztBQUNJLE1BQU0sY0FBYztJQUl6QixZQUFZLFVBQW1DLEVBQUU7UUFDL0MsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLDJEQUFRLENBQUMsRUFBRSxPQUFPLEVBQUUsT0FBTyxDQUFDLFlBQVksSUFBSSxJQUFJLEVBQUUsQ0FBQyxDQUFDO1FBRXpFLDRCQUE0QjtRQUM1QixJQUFJLE9BQU8sQ0FBQyxNQUFNLEVBQUU7WUFDbEIsT0FBTyxDQUFDLFVBQVUsQ0FBQyxPQUFPLENBQUMsTUFBTSxJQUFJLElBQUksQ0FBQyxDQUFDO1lBQzNDLE9BQU8sQ0FBQyxNQUFNLENBQUMsWUFBWSxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsVUFBVSxFQUFFLElBQUksQ0FBQyxDQUFDO1NBQzVEO0lBQ0gsQ0FBQztJQUVEOztPQUVHO0lBQ0gsVUFBVTtRQUNSLElBQUksQ0FBQyxTQUFTLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDdkIsT0FBTyxDQUFDLFdBQVcsRUFBRSxDQUFDO0lBQ3hCLENBQUM7SUFFRDs7T0FFRztJQUNILEtBQUssQ0FBQyxVQUFVO1FBQ2QsT0FBTyxNQUFNLE9BQU8sQ0FBQyxhQUFhLEVBQUUsQ0FBQztJQUN2QyxDQUFDO0lBRUQ7O09BRUc7SUFDSCxpQkFBaUI7UUFDZixPQUFPLE9BQU8sQ0FBQyxPQUFPLEVBQUUsQ0FBQztJQUMzQixDQUFDO0lBRUQ7Ozs7O09BS0c7SUFDSCxlQUFlLENBQUMsSUFBWTtRQUMxQixPQUFPLElBQUksQ0FBQyxTQUFT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QUFJLDhEQUFlLEVBQW1CLENBQUM7QUFGOUM7QUFzRjVCOztHQUVHO0FBQ0ksTUFBTSxlQUFlLEdBQWlDO0lBQzNELElBQUksRUFBRSxJQUFJO0lBQ1YsU0FBUyxFQUFFLENBQUMsc0RBQWlCLENBQUM7SUFDOUIsY0FBYyxFQUFFLE9BQU8sQ0FBQyxFQUFFLENBQUMsSUFBSSxlQUFlLENBQUMsT0FBTyxDQUFDO0NBQ3hELENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ3JIRiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRWpCO0FBRzFDLGdDQUFnQztBQUN6QixNQUFNLGlCQUFpQixHQUFHLGtCQUFrQixDQUFDO0FBQzdDLE1BQU0sdUJBQXVCLEdBQUcsQ0FBQyxNQUFNLEVBQUUsVUFBVSxDQUFDLENBQUM7QUFFNUQsaUJBQWlCO0FBQ1YsTUFBTSxxQkFBcUIsR0FBRyxTQUFTLENBQUM7QUFDeEMsTUFBTSxrQkFBa0IsR0FBRyxNQUFNLENBQUM7QUFFekMsTUFBTTtBQUNDLE1BQU0sYUFBYSxHQUFHLG9CQUFvQixDQUFDO0FBQzNDLE1BQU0sa0JBQWtCLEdBQUcsU0FBUyxDQUFDO0FBQ3JDLE1BQU0sYUFBYSxHQUFHLGdCQUFnQixDQUFDO0FBQ3ZDLE1BQU0sYUFBYSxHQUFHLDRCQUE0QixDQUFDO0FBQ25ELE1BQU0sYUFBYSxHQUFHLDRCQUE0QixDQUFDO0FBRTFEOztHQUVHO0FBQ0ksTUFBTSxlQUFlLEdBQUcsSUFBSSxvREFBSyxDQUN0QyxxQ0FBcUMsRUFDckMscURBQXFELENBQ3RELENBQUM7QUFxREY7O0dBRUc7QUFDSSxNQUFNLGdCQUFnQixHQUFHLElBQUksb0RBQUssQ0FDdkMsc0NBQXNDLEVBQ3RDLG9GQUFvRixDQUNyRixDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21lcm1haWQvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tZXJtYWlkL3NyYy9tYW5hZ2VyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tZXJtYWlkL3NyYy9tYXJrZG93bi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWVybWFpZC9zcmMvbWltZS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWVybWFpZC9zcmMvdG9rZW5zLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG1lcm1haWRcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL21hbmFnZXInO1xuZXhwb3J0ICogZnJvbSAnLi9tYXJrZG93bic7XG5leHBvcnQgKiBmcm9tICcuL21pbWUnO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgdHlwZSBNZXJtYWlkVHlwZSBmcm9tICdtZXJtYWlkJztcblxuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuXG5pbXBvcnQgeyBMcnVDYWNoZSB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5cbmltcG9ydCB7IElUaGVtZU1hbmFnZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5cbmltcG9ydCB7XG4gIERFVEFJTFNfQ0xBU1MsXG4gIElNZXJtYWlkTWFuYWdlcixcbiAgTUVSTUFJRF9DTEFTUyxcbiAgTUVSTUFJRF9DT0RFX0NMQVNTLFxuICBNRVJNQUlEX0RBUktfVEhFTUUsXG4gIE1FUk1BSURfREVGQVVMVF9USEVNRSxcbiAgU1VNTUFSWV9DTEFTUyxcbiAgV0FSTklOR19DTEFTU1xufSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogQSBtZXJtYWlkIGRpYWdyYW0gbWFuYWdlciB3aXRoIGNhY2hlLlxuICovXG5leHBvcnQgY2xhc3MgTWVybWFpZE1hbmFnZXIgaW1wbGVtZW50cyBJTWVybWFpZE1hbmFnZXIge1xuICBwcm90ZWN0ZWQgX2RpYWdyYW1zOiBMcnVDYWNoZTxzdHJpbmcsIEhUTUxFbGVtZW50PjtcbiAgcHJvdGVjdGVkIF90aGVtZXM6IElUaGVtZU1hbmFnZXIgfCBudWxsO1xuXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IE1lcm1haWRNYW5hZ2VyLklPcHRpb25zID0ge30pIHtcbiAgICB0aGlzLl9kaWFncmFtcyA9IG5ldyBMcnVDYWNoZSh7IG1heFNpemU6IG9wdGlvbnMubWF4Q2FjaGVTaXplIHx8IG51bGwgfSk7XG5cbiAgICAvLyBoYW5kbGUgcmVhY3RpbmcgdG8gdGhlbWVzXG4gICAgaWYgKG9wdGlvbnMudGhlbWVzKSB7XG4gICAgICBQcml2YXRlLmluaXRUaGVtZXMob3B0aW9ucy50aGVtZXMgfHwgbnVsbCk7XG4gICAgICBvcHRpb25zLnRoZW1lcy50aGVtZUNoYW5nZWQuY29ubmVjdCh0aGlzLmluaXRpYWxpemUsIHRoaXMpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgKHJlKS1pbml0aWFsaXppbmcgbWVybWFpZCBiYXNlZCBvbiBleHRlcm5hbCB2YWx1ZXMuXG4gICAqL1xuICBpbml0aWFsaXplKCkge1xuICAgIHRoaXMuX2RpYWdyYW1zLmNsZWFyKCk7XG4gICAgUHJpdmF0ZS5pbml0TWVybWFpZCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgdW5kZXJseWluZywgcG90ZW50aWFsbHkgdW4taW5pdGlhbGl6ZWQgbWVybWFpZCBtb2R1bGUuXG4gICAqL1xuICBhc3luYyBnZXRNZXJtYWlkKCk6IFByb21pc2U8dHlwZW9mIE1lcm1haWRUeXBlPiB7XG4gICAgcmV0dXJuIGF3YWl0IFByaXZhdGUuZW5zdXJlTWVybWFpZCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgdmVyc2lvbiBvZiB0aGUgY3VycmVudGx5LWxvYWRlZCBtZXJtYWlkIG1vZHVsZVxuICAgKi9cbiAgZ2V0TWVybWFpZFZlcnNpb24oKTogc3RyaW5nIHwgbnVsbCB7XG4gICAgcmV0dXJuIFByaXZhdGUudmVyc2lvbigpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhIHByZS1jYWNoZWQgbWVybWFpZCBmaWd1cmUuXG4gICAqXG4gICAqIFRoaXMgcHJpbWFyaWx5IGV4aXN0cyBmb3IgdGhlIG5lZWRzIG9mIGBtYXJrZWRgLCB3aGljaCBzdXBwb3J0cyBhc3luYyBub2RlXG4gICAqIHZpc2l0b3JzLCBidXQgbm90IGFzeW5jIHJlbmRlcmluZy5cbiAgICovXG4gIGdldENhY2hlZEZpZ3VyZSh0ZXh0OiBzdHJpbmcpOiBIVE1MRWxlbWVudCB8IG51bGwge1xuICAgIHJldHVybiB0aGlzLl9kaWFncmFtcy5nZXQodGV4dCk7XG4gIH1cblxuICAvKipcbiAgICogQXR0ZW1wdCBhIHJhdyByZW5kZXJpbmcgb2YgbWVybWFpZCB0byBhbiBTVkcgc3RyaW5nLCBleHRyYWN0aW5nIHNvbWUgbWV0YWRhdGEuXG4gICAqL1xuICBhc3luYyByZW5kZXJTdmcodGV4dDogc3RyaW5nKTogUHJvbWlzZTxJTWVybWFpZE1hbmFnZXIuSVJlbmRlckluZm8+IHtcbiAgICBjb25zdCBfbWVybWFpZCA9IGF3YWl0IHRoaXMuZ2V0TWVybWFpZCgpO1xuXG4gICAgY29uc3QgaWQgPSBganAtbWVybWFpZC0ke1ByaXZhdGUubmV4dE1lcm1haWRJZCgpfWA7XG5cbiAgICAvLyBjcmVhdGUgdGVtcG9yYXJ5IGVsZW1lbnQgaW50byB3aGljaCB0byByZW5kZXJcbiAgICBjb25zdCBlbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoZWwpO1xuICAgIHRyeSB7XG4gICAgICBjb25zdCB7IHN2ZyB9ID0gYXdhaXQgX21lcm1haWQucmVuZGVyKGlkLCB0ZXh0LCBlbCk7XG4gICAgICBjb25zdCBwYXJzZXIgPSBuZXcgRE9NUGFyc2VyKCk7XG4gICAgICBjb25zdCBkb2MgPSBwYXJzZXIucGFyc2VGcm9tU3RyaW5nKHN2ZywgJ2ltYWdlL3N2Zyt4bWwnKTtcblxuICAgICAgY29uc3QgaW5mbzogSU1lcm1haWRNYW5hZ2VyLklSZW5kZXJJbmZvID0geyB0ZXh0LCBzdmcgfTtcbiAgICAgIGNvbnN0IHN2Z0VsID0gZG9jLnF1ZXJ5U2VsZWN0b3IoJ3N2ZycpO1xuICAgICAgY29uc3QgeyBtYXhXaWR0aCB9ID0gc3ZnRWw/LnN0eWxlIHx8IHt9O1xuICAgICAgaW5mby53aWR0aCA9IG1heFdpZHRoID8gcGFyc2VGbG9hdChtYXhXaWR0aCkgOiBudWxsO1xuICAgICAgY29uc3QgZmlyc3RUaXRsZSA9IGRvYy5xdWVyeVNlbGVjdG9yKCd0aXRsZScpO1xuICAgICAgY29uc3QgZmlyc3REZXNjID0gZG9jLnF1ZXJ5U2VsZWN0b3IoJ2Rlc2MnKTtcbiAgICAgIGlmIChmaXJzdFRpdGxlKSB7XG4gICAgICAgIGluZm8uYWNjZXNzaWJsZVRpdGxlID0gZmlyc3RUaXRsZS50ZXh0Q29udGVudDtcbiAgICAgIH1cbiAgICAgIGlmIChmaXJzdERlc2MpIHtcbiAgICAgICAgaW5mby5hY2Nlc3NpYmxlRGVzY3JpcHRpb24gPSBmaXJzdERlc2MudGV4dENvbnRlbnQ7XG4gICAgICB9XG4gICAgICByZXR1cm4gaW5mbztcbiAgICB9IGZpbmFsbHkge1xuICAgICAgZWwucmVtb3ZlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFByb3ZpZGUgYW5kIGNhY2hlIGEgZnVsbHktcmVuZGVyZWQgZWxlbWVudCwgY2hlY2tpbmcgdGhlIGNhY2hlIGZpcnN0LlxuICAgKi9cbiAgYXN5bmMgcmVuZGVyRmlndXJlKHRleHQ6IHN0cmluZyk6IFByb21pc2U8SFRNTEVsZW1lbnQ+IHtcbiAgICAvLyBiYWlsIGlmIGFscmVhZHkgY2FjaGVkXG4gICAgbGV0IG91dHB1dDogSFRNTEVsZW1lbnQgfCBudWxsID0gdGhpcy5fZGlhZ3JhbXMuZ2V0KHRleHQpO1xuXG4gICAgaWYgKG91dHB1dCAhPSBudWxsKSB7XG4gICAgICByZXR1cm4gb3V0cHV0O1xuICAgIH1cblxuICAgIGxldCBjbGFzc05hbWUgPSBNRVJNQUlEX0NMQVNTO1xuXG4gICAgbGV0IHJlc3VsdDogSFRNTEVsZW1lbnQgfCBudWxsID0gbnVsbDtcblxuICAgIC8vIHRoZSBlbGVtZW50IHRoYXQgd2lsbCBiZSByZXR1cm5lZFxuICAgIG91dHB1dCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIG91dHB1dC5jbGFzc05hbWUgPSBjbGFzc05hbWU7XG5cbiAgICB0cnkge1xuICAgICAgY29uc3QgcmVzcG9uc2UgPSBhd2FpdCB0aGlzLnJlbmRlclN2Zyh0ZXh0KTtcbiAgICAgIHJlc3VsdCA9IHRoaXMubWFrZU1lcm1haWRGaWd1cmUocmVzcG9uc2UpO1xuICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgb3V0cHV0LmNsYXNzTGlzdC5hZGQoV0FSTklOR19DTEFTUyk7XG4gICAgICByZXN1bHQgPSBhd2FpdCB0aGlzLm1ha2VNZXJtYWlkRXJyb3IodGV4dCk7XG4gICAgfVxuXG4gICAgbGV0IHZlcnNpb24gPSB0aGlzLmdldE1lcm1haWRWZXJzaW9uKCk7XG5cbiAgICBpZiAodmVyc2lvbikge1xuICAgICAgcmVzdWx0LmRhdGFzZXQuanBNZXJtYWlkVmVyc2lvbiA9IHZlcnNpb247XG4gICAgfVxuXG4gICAgb3V0cHV0LmFwcGVuZENoaWxkKHJlc3VsdCk7XG5cbiAgICAvLyB1cGRhdGUgdGhlIGNhY2hlIGZvciB1c2Ugd2hlbiByZW5kZXJpbmcgc3luY2hyb25vdXNseVxuICAgIHRoaXMuX2RpYWdyYW1zLnNldCh0ZXh0LCBvdXRwdXQpO1xuXG4gICAgcmV0dXJuIG91dHB1dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBQcm92aWRlIGEgY29kZSBibG9jayB3aXRoIHRoZSBtZXJtYWlkIHNvdXJjZS5cbiAgICovXG4gIG1ha2VNZXJtYWlkQ29kZSh0ZXh0OiBzdHJpbmcpOiBIVE1MRWxlbWVudCB7XG4gICAgLy8gYXBwZW5kIHRoZSBzb3VyY2VcbiAgICBjb25zdCBwcmUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdwcmUnKTtcbiAgICBjb25zdCBjb2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnY29kZScpO1xuICAgIGNvZGUuaW5uZXJUZXh0ID0gdGV4dDtcbiAgICBwcmUuYXBwZW5kQ2hpbGQoY29kZSk7XG4gICAgY29kZS5jbGFzc05hbWUgPSBNRVJNQUlEX0NPREVfQ0xBU1M7XG4gICAgY29kZS50ZXh0Q29udGVudCA9IHRleHQ7XG4gICAgcmV0dXJuIHByZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHBhcnNlciBtZXNzYWdlIGVsZW1lbnQgZnJvbSBhIGZhaWxlZCBwYXJzZS5cbiAgICpcbiAgICogVGhpcyBkb2Vzbid0IGRvIG11Y2ggb2YgYW55dGhpbmcgaWYgdGhlIHRleHQgaXMgc3VjY2Vzc2Z1bGx5IHBhcnNlZC5cbiAgICovXG4gIGFzeW5jIG1ha2VNZXJtYWlkRXJyb3IodGV4dDogc3RyaW5nKTogUHJvbWlzZTxIVE1MRWxlbWVudD4ge1xuICAgIGNvbnN0IF9tZXJtYWlkID0gYXdhaXQgdGhpcy5nZXRNZXJtYWlkKCk7XG4gICAgbGV0IGVycm9yTWVzc2FnZSA9ICcnO1xuICAgIHRyeSB7XG4gICAgICBhd2FpdCBfbWVybWFpZC5wYXJzZSh0ZXh0KTtcbiAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgIGVycm9yTWVzc2FnZSA9IGAke2Vycn1gO1xuICAgIH1cblxuICAgIGNvbnN0IHJlc3VsdCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RldGFpbHMnKTtcbiAgICByZXN1bHQuY2xhc3NOYW1lID0gREVUQUlMU19DTEFTUztcbiAgICBjb25zdCBzdW1tYXJ5ID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnc3VtbWFyeScpO1xuICAgIHN1bW1hcnkuY2xhc3NOYW1lID0gU1VNTUFSWV9DTEFTUztcbiAgICBzdW1tYXJ5LmFwcGVuZENoaWxkKHRoaXMubWFrZU1lcm1haWRDb2RlKHRleHQpKTtcbiAgICByZXN1bHQuYXBwZW5kQ2hpbGQoc3VtbWFyeSk7XG5cbiAgICBjb25zdCB3YXJuaW5nID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncHJlJyk7XG4gICAgd2FybmluZy5pbm5lclRleHQgPSBlcnJvck1lc3NhZ2U7XG4gICAgcmVzdWx0LmFwcGVuZENoaWxkKHdhcm5pbmcpO1xuICAgIHJldHVybiByZXN1bHQ7XG4gIH1cblxuICAvKipcbiAgICogRXh0cmFjdCBleHRyYSBhdHRyaWJ1dGVzIHRvIGFkZCB0byBhIGdlbmVyYXRlZCBmaWd1cmUuXG4gICAqL1xuICBtYWtlTWVybWFpZEZpZ3VyZShpbmZvOiBJTWVybWFpZE1hbmFnZXIuSVJlbmRlckluZm8pOiBIVE1MRWxlbWVudCB7XG4gICAgY29uc3QgZmlndXJlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZmlndXJlJyk7XG4gICAgY29uc3QgaW1nID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaW1nJyk7XG5cbiAgICBmaWd1cmUuYXBwZW5kQ2hpbGQoaW1nKTtcbiAgICBpbWcuc2V0QXR0cmlidXRlKFxuICAgICAgJ3NyYycsXG4gICAgICBgZGF0YTppbWFnZS9zdmcreG1sLCR7ZW5jb2RlVVJJQ29tcG9uZW50KGluZm8uc3ZnKX1gXG4gICAgKTtcblxuICAgIC8vIGFkZCBkaW1lbnNpb24gaW5mb3JtYXRpb25cbiAgICBpZiAoaW5mby53aWR0aCkge1xuICAgICAgaW1nLndpZHRoID0gaW5mby53aWR0aDtcbiAgICB9XG5cbiAgICAvLyBhZGQgYWNjZXNzaWJsZSBhbHQgdGl0bGVcbiAgICBpZiAoaW5mby5hY2Nlc3NpYmxlVGl0bGUpIHtcbiAgICAgIGltZy5zZXRBdHRyaWJ1dGUoJ2FsdCcsIGluZm8uYWNjZXNzaWJsZVRpdGxlKTtcbiAgICB9XG5cbiAgICBmaWd1cmUuYXBwZW5kQ2hpbGQodGhpcy5tYWtlTWVybWFpZENvZGUoaW5mby50ZXh0KSk7XG5cbiAgICAvLyBhZGQgYWNjZXNzaWJsZSBjYXB0aW9uLCB3aXRoIGZhbGxiYWNrIHRvIHJhdyBtZXJtYWlkIHNvdXJjZVxuICAgIGlmIChpbmZvLmFjY2Vzc2libGVEZXNjcmlwdGlvbikge1xuICAgICAgY29uc3QgY2FwdGlvbiA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2ZpZ2NhcHRpb24nKTtcbiAgICAgIGNhcHRpb24uY2xhc3NOYW1lID0gJ3NyLW9ubHknO1xuICAgICAgY2FwdGlvbi50ZXh0Q29udGVudCA9IGluZm8uYWNjZXNzaWJsZURlc2NyaXB0aW9uO1xuICAgICAgZmlndXJlLmFwcGVuZENoaWxkKGNhcHRpb24pO1xuICAgIH1cblxuICAgIHJldHVybiBmaWd1cmU7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgaW1wbGVtZW50YXRpb24tc3BlY2lmaWMgZGV0YWlscyBvZiB0aGlzIG1lcm1haWQgbWFuYWdlci5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBNZXJtYWlkTWFuYWdlciB7XG4gIC8qKlxuICAgKiBJbml0aWFsaXphdGlvbiBvcHRpb25zIGZvciB0aGUgbWVybWFpZCBtYW5hZ2VyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgbWF4Q2FjaGVTaXplPzogbnVtYmVyIHwgbnVsbDtcbiAgICB0aGVtZXM/OiBJVGhlbWVNYW5hZ2VyIHwgbnVsbDtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBnbG9iYWwsIHByaXZhdGUgbWVybWFpZCBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGxldCBfdGhlbWVzOiBJVGhlbWVNYW5hZ2VyIHwgbnVsbCA9IG51bGw7XG4gIGxldCBfbWVybWFpZDogdHlwZW9mIE1lcm1haWRUeXBlIHwgbnVsbCA9IG51bGw7XG4gIGxldCBfbG9hZGluZzogUHJvbWlzZURlbGVnYXRlPHR5cGVvZiBNZXJtYWlkVHlwZT4gfCBudWxsID0gbnVsbDtcbiAgbGV0IF9uZXh0TWVybWFpZElkID0gMDtcbiAgbGV0IF92ZXJzaW9uOiBzdHJpbmcgfCBudWxsID0gbnVsbDtcblxuICAvKipcbiAgICogQ2FjaGUgYSByZWZlcmVuY2UgdG8gdGhlIHRoZW1lIG1hbmFnZXIuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gaW5pdFRoZW1lcyh0aGVtZXM6IElUaGVtZU1hbmFnZXIgfCBudWxsKSB7XG4gICAgX3RoZW1lcyA9IHRoZW1lcztcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHZlcnNpb24gb2YgbWVybWFpZCB1c2VkIGZvciByZW5kZXJpbmcuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gdmVyc2lvbigpOiBzdHJpbmcgfCBudWxsIHtcbiAgICByZXR1cm4gX3ZlcnNpb247XG4gIH1cblxuICAvKipcbiAgICogKFJlLSlpbml0aWFsaXplIG1lcm1haWQgd2l0aCBsYWItc3BlY2lmaWMgdGhlbWUgaW5mb3JtYXRpb25cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBpbml0TWVybWFpZCgpOiBib29sZWFuIHtcbiAgICBpZiAoIV9tZXJtYWlkKSB7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfVxuXG4gICAgbGV0IHRoZW1lID0gTUVSTUFJRF9ERUZBVUxUX1RIRU1FO1xuXG4gICAgaWYgKF90aGVtZXMpIHtcbiAgICAgIGNvbnN0IGpwVGhlbWUgPSBfdGhlbWVzLnRoZW1lO1xuICAgICAgdGhlbWUgPVxuICAgICAgICBqcFRoZW1lICYmIF90aGVtZXMuaXNMaWdodChqcFRoZW1lKVxuICAgICAgICAgID8gTUVSTUFJRF9ERUZBVUxUX1RIRU1FXG4gICAgICAgICAgOiBNRVJNQUlEX0RBUktfVEhFTUU7XG4gICAgfVxuXG4gICAgY29uc3QgZm9udEZhbWlseSA9IHdpbmRvd1xuICAgICAgLmdldENvbXB1dGVkU3R5bGUoZG9jdW1lbnQuYm9keSlcbiAgICAgIC5nZXRQcm9wZXJ0eVZhbHVlKCctLWpwLXVpLWZvbnQtZmFtaWx5Jyk7XG5cbiAgICBfbWVybWFpZC5tZXJtYWlkQVBJLmdsb2JhbFJlc2V0KCk7XG4gICAgX21lcm1haWQubWVybWFpZEFQSS5pbml0aWFsaXplKHtcbiAgICAgIHRoZW1lLFxuICAgICAgZm9udEZhbWlseSxcbiAgICAgIG1heFRleHRTaXplOiAxMDAwMDAsXG4gICAgICBzdGFydE9uTG9hZDogZmFsc2VcbiAgICB9KTtcbiAgICByZXR1cm4gdHJ1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEZXRlcm1pbmUgd2hldGhlciBtZXJtYWlkIGhhcyBiZWVuIGxvYWRlZCB5ZXQuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZ2V0TWVybWFpZCgpOiB0eXBlb2YgTWVybWFpZFR5cGUgfCBudWxsIHtcbiAgICByZXR1cm4gX21lcm1haWQ7XG4gIH1cblxuICAvKipcbiAgICogUHJvdmlkZSBhIGdsb2JhbGx5LXVuaXF1ZSwgYnV0IHVuc3RhYmxlLCBJRCBmb3IgZGlzYW1iaWd1YXRpb24uXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gbmV4dE1lcm1haWRJZCgpIHtcbiAgICByZXR1cm4gX25leHRNZXJtYWlkSWQrKztcbiAgfVxuXG4gIC8qKlxuICAgKiBFbnN1cmUgbWVybWFpZCBoYXMgYmVlbiBsYXppbHkgbG9hZGVkIG9uY2UsIGluaXRpYWxpemVkLCBhbmQgY2FjaGVkLlxuICAgKi9cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGVuc3VyZU1lcm1haWQoKTogUHJvbWlzZTx0eXBlb2YgTWVybWFpZFR5cGU+IHtcbiAgICBpZiAoX21lcm1haWQgIT0gbnVsbCkge1xuICAgICAgcmV0dXJuIF9tZXJtYWlkO1xuICAgIH1cbiAgICBpZiAoX2xvYWRpbmcpIHtcbiAgICAgIHJldHVybiBfbG9hZGluZy5wcm9taXNlO1xuICAgIH1cbiAgICBfbG9hZGluZyA9IG5ldyBQcm9taXNlRGVsZWdhdGUoKTtcbiAgICBfdmVyc2lvbiA9IChhd2FpdCBpbXBvcnQoJ21lcm1haWQvcGFja2FnZS5qc29uJykpLnZlcnNpb247XG4gICAgX21lcm1haWQgPSAoYXdhaXQgaW1wb3J0KCdtZXJtYWlkJykpLmRlZmF1bHQ7XG4gICAgaW5pdE1lcm1haWQoKTtcbiAgICBfbG9hZGluZy5yZXNvbHZlKF9tZXJtYWlkKTtcbiAgICByZXR1cm4gX21lcm1haWQ7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSU1lcm1haWRNYW5hZ2VyLCBJTWVybWFpZE1hcmtkb3duIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEFuIGltcGxlbWVudGF0aW9uIG9mIG1lcm1haWQgZmVuY2VkIGNvZGUgYmxvY2tzIGluIG1hcmtkb3duLlxuICovXG5leHBvcnQgY2xhc3MgTWVybWFpZE1hcmtkb3duIGltcGxlbWVudHMgSU1lcm1haWRNYXJrZG93biB7XG4gIHByb3RlY3RlZCBfbWVybWFpZDogSU1lcm1haWRNYW5hZ2VyO1xuICByZWFkb25seSBsYW5ndWFnZXMgPSBbJ21lcm1haWQnXTtcbiAgcmVhZG9ubHkgcmFuayA9IDEwMDtcblxuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBNZXJtYWlkTWFya2Rvd24uSU9wdGlvbnMpIHtcbiAgICB0aGlzLl9tZXJtYWlkID0gb3B0aW9ucy5tZXJtYWlkO1xuICB9XG5cbiAgLyoqXG4gICAqIFByZS1wYXJzZSBhbmQgY2FjaGUgdGhlIHJlbmRlcmVkIHRleHQuXG4gICAqL1xuICBhc3luYyB3YWxrKHRleHQ6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIGF3YWl0IHRoaXMuX21lcm1haWQucmVuZGVyRmlndXJlKHRleHQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUgZGlhZ3JhbS5cbiAgICovXG4gIHJlbmRlcih0ZXh0OiBzdHJpbmcpOiBzdHJpbmcgfCBudWxsIHtcbiAgICAvLyBoYW5kbGUgcHJlLWNhY2hlZCBtZXJtYWlkIGZpZ3VyZXNcbiAgICBsZXQgY2FjaGVkRmlndXJlOiBIVE1MRWxlbWVudCB8IG51bGwgPSB0aGlzLl9tZXJtYWlkLmdldENhY2hlZEZpZ3VyZSh0ZXh0KTtcbiAgICBpZiAoY2FjaGVkRmlndXJlKSB7XG4gICAgICByZXR1cm4gY2FjaGVkRmlndXJlLm91dGVySFRNTDtcbiAgICB9XG4gICAgcmV0dXJuIG51bGw7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgbWVybWFpZCBtYXJrZG93blxuICovXG5leHBvcnQgbmFtZXNwYWNlIE1lcm1haWRNYXJrZG93biB7XG4gIC8qKlxuICAgKiBJbml0aWFsaXphdGlvbiBvcHRpb25zIGZvciBtZXJtYWlkIG1hcmtkb3duXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICBtZXJtYWlkOiBJTWVybWFpZE1hbmFnZXI7XG4gIH1cbn1cbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWVybWFpZC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTWVybWFpZE1hbmFnZXIsXG4gIE1FUk1BSURfQ0xBU1MsXG4gIE1FUk1BSURfTUlNRV9UWVBFLFxuICBXQVJOSU5HX0NMQVNTXG59IGZyb20gJy4vdG9rZW5zJztcbmltcG9ydCB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcbmltcG9ydCB7IFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbmNvbnN0IFNWR19NSU1FID0gJ2ltYWdlL3N2Zyt4bWwnO1xuXG4vKipcbiAqIEEgd2lkZ2V0IGZvciByZW5kZXJpbmcgbWVybWFpZCB0ZXh0LWJhc2VkIGRpYWdyYW1zLCBmb3IgdXNhZ2Ugd2l0aCByZW5kZXJtaW1lLlxuICovXG5leHBvcnQgY2xhc3MgUmVuZGVyZWRNZXJtYWlkIGV4dGVuZHMgV2lkZ2V0IGltcGxlbWVudHMgSVJlbmRlck1pbWUuSVJlbmRlcmVyIHtcbiAgcHJvdGVjdGVkIHN0YXRpYyBfbWFuYWdlcjogSU1lcm1haWRNYW5hZ2VyIHwgbnVsbCA9IG51bGw7XG4gIHByb3RlY3RlZCBzdGF0aWMgX21hbmFnZXJSZWFkeSA9IG5ldyBQcm9taXNlRGVsZWdhdGU8SU1lcm1haWRNYW5hZ2VyPigpO1xuICBwcm90ZWN0ZWQgX2xhc3RSZW5kZXJlZDogc3RyaW5nIHwgbnVsbCA9IG51bGw7XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB3aWRnZXQgZm9yIHJlbmRlcmluZyBWZWdhL1ZlZ2EtTGl0ZS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElSZW5kZXJNaW1lLklSZW5kZXJlck9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX21pbWVUeXBlID0gb3B0aW9ucy5taW1lVHlwZTtcbiAgICB0aGlzLmFkZENsYXNzKE1FUk1BSURfQ0xBU1MpO1xuICB9XG5cbiAgc3RhdGljIHNldCBtYW5hZ2VyKG1hbmFnZXI6IElNZXJtYWlkTWFuYWdlcikge1xuICAgIGlmIChSZW5kZXJlZE1lcm1haWQuX21hbmFnZXIpIHtcbiAgICAgIGNvbnNvbGUud2FybignTWVybWFpZCBtYW5hZ2VyIG1heSBvbmx5IGJlIHNldCBvbmNlLCBhbmQgaXMgYWxyZWFkeSBzZXQuJyk7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIFJlbmRlcmVkTWVybWFpZC5fbWFuYWdlciA9IG1hbmFnZXI7XG4gICAgUmVuZGVyZWRNZXJtYWlkLl9tYW5hZ2VyUmVhZHkucmVzb2x2ZShtYW5hZ2VyKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgbWVybWFpZCB0ZXh0LWJhc2VkIGRpYWdyYW1zIGludG8gdGhpcyB3aWRnZXQncyBub2RlLlxuICAgKi9cbiAgYXN5bmMgcmVuZGVyTW9kZWwobW9kZWw6IElSZW5kZXJNaW1lLklNaW1lTW9kZWwpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCBtYW5hZ2VyID0gYXdhaXQgUmVuZGVyZWRNZXJtYWlkLl9tYW5hZ2VyUmVhZHkucHJvbWlzZTtcblxuICAgIGNvbnN0IHRleHQgPSBtb2RlbC5kYXRhW3RoaXMuX21pbWVUeXBlXSBhcyBzdHJpbmcgfCB1bmRlZmluZWQ7XG4gICAgaWYgKHRleHQgPT0gbnVsbCB8fCB0ZXh0ID09PSB0aGlzLl9sYXN0UmVuZGVyZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl9sYXN0UmVuZGVyZWQgPSB0ZXh0O1xuXG4gICAgLy8gZ2V0IGEgZGl2IGNvbnRhaW5pbmcgYSBmaWd1cmUgb3IgcGFyc2VyIG1lc3NhZ2VcbiAgICBjb25zdCBmaWd1cmUgPSBhd2FpdCBtYW5hZ2VyLnJlbmRlckZpZ3VyZSh0ZXh0KTtcblxuICAgIGlmIChmaWd1cmUuY2xhc3NMaXN0LmNvbnRhaW5zKFdBUk5JTkdfQ0xBU1MpKSB7XG4gICAgICB0aGlzLm5vZGUuY2xhc3NMaXN0LmFkZChXQVJOSU5HX0NMQVNTKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5ub2RlLmNsYXNzTGlzdC5yZW1vdmUoV0FSTklOR19DTEFTUyk7XG4gICAgfVxuXG4gICAgaWYgKCFmaWd1cmUuZmlyc3RDaGlsZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGlmICh0aGlzLm5vZGUuaW5uZXJIVE1MICE9PSBmaWd1cmUuaW5uZXJIVE1MKSB7XG4gICAgICB0aGlzLm5vZGUuaW5uZXJIVE1MID0gZmlndXJlLmlubmVySFRNTDtcbiAgICB9XG5cbiAgICAvLyBjYXB0dXJlIHRoZSB2ZXJzaW9uIG9mIG1lcm1haWQgdXNlZFxuICAgIGNvbnN0IHZlcnNpb24gPSBtYW5hZ2VyLmdldE1lcm1haWRWZXJzaW9uKCk7XG4gICAgY29uc3QgbWVybWFpZE1ldGFkYXRhID0ge1xuICAgICAgLi4uKChtb2RlbC5tZXRhZGF0YVtNRVJNQUlEX01JTUVfVFlQRV0gYXMgUmVjb3JkPHN0cmluZywgYW55PikgfHwge30pLFxuICAgICAgdmVyc2lvblxuICAgIH07XG4gICAgY29uc3QgbWV0YWRhdGEgPSB7XG4gICAgICAuLi5tb2RlbC5tZXRhZGF0YSxcbiAgICAgIFtNRVJNQUlEX01JTUVfVFlQRV06IG1lcm1haWRNZXRhZGF0YVxuICAgIH07XG5cbiAgICAvLyBpZiBhdmFpbGFibGUsIHNldCB0aGUgZnVsbHktcmVuZGVyZWQgU1ZHXG4gICAgY29uc3QgaW1nID0gZmlndXJlLnF1ZXJ5U2VsZWN0b3IoJ2ltZycpO1xuXG4gICAgaWYgKGltZykge1xuICAgICAgY29uc3Qgc3ZnID0gZGVjb2RlVVJJQ29tcG9uZW50KGltZy5zcmMuc3BsaXQoJywnKVsxXSk7XG4gICAgICBjb25zdCBvbGRTdmcgPSBtb2RlbC5kYXRhW1NWR19NSU1FXTtcbiAgICAgIGlmIChzdmcgIT09IG9sZFN2Zykge1xuICAgICAgICBtb2RlbC5zZXREYXRhKHtcbiAgICAgICAgICBkYXRhOiB7IC4uLm1vZGVsLmRhdGEsIFtTVkdfTUlNRV06IHN2ZyB9LFxuICAgICAgICAgIG1ldGFkYXRhXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICBjb25zdCBkYXRhV2l0aG91dFN2ZyA9IHsgLi4ubW9kZWwuZGF0YSB9O1xuICAgICAgZGVsZXRlIGRhdGFXaXRob3V0U3ZnW1NWR19NSU1FXTtcbiAgICAgIG1vZGVsLnNldERhdGEoeyBkYXRhOiBkYXRhV2l0aG91dFN2ZywgbWV0YWRhdGEgfSk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfbWltZVR5cGU6IHN0cmluZztcbn1cblxuLyoqXG4gKiBBIG1pbWUgcmVuZGVyZXIgZmFjdG9yeSBmb3IgbWVybWFpZCB0ZXh0LWJhc2VkIGRpYWdyYW1zLlxuICovXG5leHBvcnQgY29uc3QgcmVuZGVyZXJGYWN0b3J5OiBJUmVuZGVyTWltZS5JUmVuZGVyZXJGYWN0b3J5ID0ge1xuICBzYWZlOiB0cnVlLFxuICBtaW1lVHlwZXM6IFtNRVJNQUlEX01JTUVfVFlQRV0sXG4gIGNyZWF0ZVJlbmRlcmVyOiBvcHRpb25zID0+IG5ldyBSZW5kZXJlZE1lcm1haWQob3B0aW9ucylcbn07XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHR5cGUgTWVybWFpZFR5cGUgZnJvbSAnbWVybWFpZCc7XG5cbi8vIGRvY3VtZW50ZWQgdXBzdHJlYW0gY29uc3RhbnRzXG5leHBvcnQgY29uc3QgTUVSTUFJRF9NSU1FX1RZUEUgPSAndGV4dC92bmQubWVybWFpZCc7XG5leHBvcnQgY29uc3QgTUVSTUFJRF9GSUxFX0VYVEVOU0lPTlMgPSBbJy5tbWQnLCAnLm1lcm1haWQnXTtcblxuLy8gbWVybWFpZCB0aGVtZXNcbmV4cG9ydCBjb25zdCBNRVJNQUlEX0RFRkFVTFRfVEhFTUUgPSAnZGVmYXVsdCc7XG5leHBvcnQgY29uc3QgTUVSTUFJRF9EQVJLX1RIRU1FID0gJ2RhcmsnO1xuXG4vLyBET01cbmV4cG9ydCBjb25zdCBNRVJNQUlEX0NMQVNTID0gJ2pwLVJlbmRlcmVkTWVybWFpZCc7XG5leHBvcnQgY29uc3QgTUVSTUFJRF9DT0RFX0NMQVNTID0gJ21lcm1haWQnO1xuZXhwb3J0IGNvbnN0IFdBUk5JTkdfQ0xBU1MgPSAnanAtbW9kLXdhcm5pbmcnO1xuZXhwb3J0IGNvbnN0IERFVEFJTFNfQ0xBU1MgPSAnanAtUmVuZGVyZWRNZXJtYWlkLURldGFpbHMnO1xuZXhwb3J0IGNvbnN0IFNVTU1BUllfQ0xBU1MgPSAnanAtUmVuZGVyZWRNZXJtYWlkLVN1bW1hcnknO1xuXG4vKipcbiAqIFRoZSBleHBvcnRlZCB0b2tlbiBmb3IgYSBtZXJtYWlkIG1hbmFnZXJcbiAqL1xuZXhwb3J0IGNvbnN0IElNZXJtYWlkTWFuYWdlciA9IG5ldyBUb2tlbjxJTWVybWFpZE1hbmFnZXI+KFxuICAnQGp1cHl0ZXJsYWIvbWVybWFpZDpJTWVybWFpZE1hbmFnZXInLFxuICBgYSBtYW5hZ2VyIGZvciByZW5kZXJpbmcgbWVybWFpZCB0ZXh0LWJhc2VkIGRpYWdyYW1zYFxuKTtcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHVibGljIG1lcm1haWQgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJTWVybWFpZE1hbmFnZXIge1xuICAvKipcbiAgICogR2V0IHRoZSAocG90ZW50aWFsbHkgdW5pbml0aWFsaXplZCkgbWVybWFpZCBtb2R1bGUuXG4gICAqL1xuICBnZXRNZXJtYWlkKCk6IFByb21pc2U8dHlwZW9mIE1lcm1haWRUeXBlPjtcblxuICAvKipcbiAgICogR2V0IHRoZSB2ZXJzaW9uIG9mIHRoZSBjdXJyZW50bHktbG9hZGVkIG1lcm1haWQgbW9kdWxlXG4gICAqL1xuICBnZXRNZXJtYWlkVmVyc2lvbigpOiBzdHJpbmcgfCBudWxsO1xuXG4gIC8qKlxuICAgKiBSZW5kZXIgbWVybWFpZCBzb3VyY2UgdG8gYW4gU1ZHIHN0cmluZyB3aXRoIGV4dHJhY2VkIG1ldGFkYXRhLlxuICAgKi9cbiAgcmVuZGVyU3ZnKHRleHQ6IHN0cmluZyk6IFByb21pc2U8SU1lcm1haWRNYW5hZ2VyLklSZW5kZXJJbmZvPjtcblxuICAvKipcbiAgICogUmVuZGVyIGFuZCBjYWNoZSBtZXJtYWlkIHNvdXJjZSBhcyBhIGZpZ3VyZSBvZiBhbiBpbWFnZSwgb3IgYSB1bnN1Y2Nlc3NmdWwgcGFyc2VyIG1lc3NhZ2UuXG4gICAqL1xuICByZW5kZXJGaWd1cmUodGV4dDogc3RyaW5nKTogUHJvbWlzZTxIVE1MRWxlbWVudD47XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgcHJlLWNhY2hlZCBlbGVtZW50IGZvciBhIG1lcm1haWQgc3RyaW5nLCBpZiBhdmFpbGFibGUuXG4gICAqL1xuICBnZXRDYWNoZWRGaWd1cmUodGV4dDogc3RyaW5nKTogSFRNTEVsZW1lbnQgfCBudWxsO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciB0aGUgbWVybWFpZCBtYW5hZ2VyLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElNZXJtYWlkTWFuYWdlciB7XG4gIC8qKlxuICAgKiBUaGUgcmVzdWx0cyBvZiBhIHN1Y2Nlc3NmdWwgcmVuZGVyaW5nIG9mIGEgbWVybWFpZCB0ZXh0LWJhc2VkIGRpYWdyYW0uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElSZW5kZXJJbmZvIHtcbiAgICAvKiogdGhlIG9yaWdpbmFsIHNvdXJjZSBvZiB0aGUgZGlhZ3JhbS4gKi9cbiAgICB0ZXh0OiBzdHJpbmc7XG4gICAgLyoqIFRoZSByYXcgcmVuZGVyZWQgU1ZHLiAqL1xuICAgIHN2Zzogc3RyaW5nO1xuICAgIC8qKiBUaGUgZXh0cmFjdGVkIGFjY2Vzc2libGUgZGVzY3JpcHRpb24sIGlmIGZvdW5kLiAqL1xuICAgIGFjY2Vzc2libGVEZXNjcmlwdGlvbj86IHN0cmluZyB8IG51bGw7XG4gICAgLyoqIFRoZSBleHRyYWN0ZWQgYWNjZXNzaWJsZSB0aXRsZSwgaWYgZm91bmQuICovXG4gICAgYWNjZXNzaWJsZVRpdGxlPzogc3RyaW5nIHwgbnVsbDtcbiAgICAvKiogVGhlIGV4dHJhY3RlZCB3aWR0aCBvZiB0aGUgZGlnYXJhbSwgaWYgZm91bmQuICovXG4gICAgd2lkdGg/OiBudW1iZXIgfCBudWxsO1xuICB9XG59XG5cbi8qKlxuICogVGhlIGV4cG9ydGVkIHRva2VuIGZvciBhIG1lcm1haWQgbWFuYWdlclxuICovXG5leHBvcnQgY29uc3QgSU1lcm1haWRNYXJrZG93biA9IG5ldyBUb2tlbjxJTWVybWFpZE1hcmtkb3duPihcbiAgJ0BqdXB5dGVybGFiL21lcm1haWQ6SU1lcm1haWRNYXJrZG93bicsXG4gIGBhIG1hbmFnZXIgZm9yIHJlbmRlcmluZyBtZXJtYWlkIHRleHQtYmFzZWQgZGlhZ3JhbXMgaW4gbWFya2Rvd24gZmVuY2VkIGNvZGUgYmxvY2tzYFxuKTtcblxuLyoqXG4gKiBBIGhhbmRsZXIgZm9yIG1lcm1haWQgZmVuY2VkIGNvZGUgYmxvY2tzIGluIG1hcmtkb3duXG4gKlxuICogVGhpcyBkdXBsaWNhdGVzIHRoZSAoY3VycmVudGx5KSBwcml2YXRlIGBJRmVuY2VkQmxvY2tSZW5kZXJlcmAgaW5cbiAqIGBAanVweXRlcmxhYi9tYXJrZWRwYXJzZXItZXh0ZW5zaW9uYC5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJTWVybWFpZE1hcmtkb3duIHtcbiAgLyoqXG4gICAqIFRoZSBsYW5ndWFnZXMgdGhpcyBibG9jayBhY2NlcHRzLlxuICAgKi9cbiAgbGFuZ3VhZ2VzOiBzdHJpbmdbXTtcbiAgLyoqXG4gICAqIFRoZSBvcmRlciBpbiB3aGljaCB0aGUgYmxvY2sgd291bGQgYmUgcHJvY2Vzc2VkXG4gICAqL1xuICByYW5rOiBudW1iZXI7XG4gIC8qKlxuICAgKiBIYW5kbGUgdXAtZnJvbnQgbG9hZGluZy9wYXJzaW5nIG1lcm1haWRcbiAgICovXG4gIHdhbGs6ICh0ZXh0OiBzdHJpbmcpID0+IFByb21pc2U8dm9pZD47XG4gIC8qKlxuICAgKiBQcm92aWRlIHByZS1yZW5kZXJlZCBkaWFncmFtIGNvbnRlbnRcbiAgICovXG4gIHJlbmRlcjogKHRleHQ6IHN0cmluZykgPT4gc3RyaW5nIHwgbnVsbDtcbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==