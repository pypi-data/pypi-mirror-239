"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_coreutils_lib_index_js"],{

/***/ "../packages/coreutils/lib/activitymonitor.js":
/*!****************************************************!*\
  !*** ../packages/coreutils/lib/activitymonitor.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.ActivityMonitor = void 0;
const signaling_1 = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/**
 * A class that monitors activity on a signal.
 */
class ActivityMonitor {
    /**
     * Construct a new activity monitor.
     */
    constructor(options) {
        this._timer = -1;
        this._timeout = -1;
        this._isDisposed = false;
        this._activityStopped = new signaling_1.Signal(this);
        options.signal.connect(this._onSignalFired, this);
        this._timeout = options.timeout || 1000;
    }
    /**
     * A signal emitted when activity has ceased.
     */
    get activityStopped() {
        return this._activityStopped;
    }
    /**
     * The timeout associated with the monitor, in milliseconds.
     */
    get timeout() {
        return this._timeout;
    }
    set timeout(value) {
        this._timeout = value;
    }
    /**
     * Test whether the monitor has been disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the activity monitor.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        signaling_1.Signal.clearData(this);
    }
    /**
     * A signal handler for the monitored signal.
     */
    _onSignalFired(sender, args) {
        clearTimeout(this._timer);
        this._sender = sender;
        this._args = args;
        this._timer = setTimeout(() => {
            this._activityStopped.emit({
                sender: this._sender,
                args: this._args
            });
        }, this._timeout);
    }
}
exports.ActivityMonitor = ActivityMonitor;


/***/ }),

/***/ "../packages/coreutils/lib/index.js":
/*!******************************************!*\
  !*** ../packages/coreutils/lib/index.js ***!
  \******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module coreutils
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./activitymonitor */ "../packages/coreutils/lib/activitymonitor.js"), exports);
__exportStar(__webpack_require__(/*! ./interfaces */ "../packages/coreutils/lib/interfaces.js"), exports);
__exportStar(__webpack_require__(/*! ./lru */ "../packages/coreutils/lib/lru.js"), exports);
__exportStar(__webpack_require__(/*! ./markdowncodeblocks */ "../packages/coreutils/lib/markdowncodeblocks.js"), exports);
__exportStar(__webpack_require__(/*! ./pageconfig */ "../packages/coreutils/lib/pageconfig.js"), exports);
__exportStar(__webpack_require__(/*! ./path */ "../packages/coreutils/lib/path.js"), exports);
__exportStar(__webpack_require__(/*! ./signal */ "../packages/coreutils/lib/signal.js"), exports);
__exportStar(__webpack_require__(/*! ./text */ "../packages/coreutils/lib/text.js"), exports);
__exportStar(__webpack_require__(/*! ./time */ "../packages/coreutils/lib/time.js"), exports);
__exportStar(__webpack_require__(/*! ./url */ "../packages/coreutils/lib/url.js"), exports);


/***/ }),

/***/ "../packages/coreutils/lib/interfaces.js":
/*!***********************************************!*\
  !*** ../packages/coreutils/lib/interfaces.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));


/***/ }),

/***/ "../packages/coreutils/lib/lru.js":
/*!****************************************!*\
  !*** ../packages/coreutils/lib/lru.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LruCache = void 0;
const DEFAULT_MAX_SIZE = 128;
/** A least-recently-used cache. */
class LruCache {
    constructor(options = {}) {
        this._map = new Map();
        this._maxSize = (options === null || options === void 0 ? void 0 : options.maxSize) || DEFAULT_MAX_SIZE;
    }
    /**
     * Return the current size of the cache.
     */
    get size() {
        return this._map.size;
    }
    /**
     * Clear the values in the cache.
     */
    clear() {
        this._map.clear();
    }
    /**
     * Get a value (or null) from the cache, pushing the item to the front of the cache.
     */
    get(key) {
        const item = this._map.get(key) || null;
        if (item != null) {
            this._map.delete(key);
            this._map.set(key, item);
        }
        return item;
    }
    /**
     * Set a value in the cache, potentially evicting an old item.
     */
    set(key, value) {
        if (this._map.size >= this._maxSize) {
            this._map.delete(this._map.keys().next().value);
        }
        this._map.set(key, value);
    }
}
exports.LruCache = LruCache;


/***/ }),

/***/ "../packages/coreutils/lib/markdowncodeblocks.js":
/*!*******************************************************!*\
  !*** ../packages/coreutils/lib/markdowncodeblocks.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MarkdownCodeBlocks = void 0;
/**
 * The namespace for code block functions which help
 * in extract code from markdown text
 */
var MarkdownCodeBlocks;
(function (MarkdownCodeBlocks) {
    MarkdownCodeBlocks.CODE_BLOCK_MARKER = '```';
    const markdownExtensions = [
        '.markdown',
        '.mdown',
        '.mkdn',
        '.md',
        '.mkd',
        '.mdwn',
        '.mdtxt',
        '.mdtext',
        '.text',
        '.txt',
        '.Rmd'
    ];
    class MarkdownCodeBlock {
        constructor(startLine) {
            this.startLine = startLine;
            this.code = '';
            this.endLine = -1;
        }
    }
    MarkdownCodeBlocks.MarkdownCodeBlock = MarkdownCodeBlock;
    /**
     * Check whether the given file extension is a markdown extension
     * @param extension - A file extension
     *
     * @returns true/false depending on whether this is a supported markdown extension
     */
    function isMarkdown(extension) {
        return markdownExtensions.indexOf(extension) > -1;
    }
    MarkdownCodeBlocks.isMarkdown = isMarkdown;
    /**
     * Construct all code snippets from current text
     * (this could be potentially optimized if we can cache and detect differences)
     * @param text - A string to parse codeblocks from
     *
     * @returns An array of MarkdownCodeBlocks.
     */
    function findMarkdownCodeBlocks(text) {
        if (!text || text === '') {
            return [];
        }
        const lines = text.split('\n');
        const codeBlocks = [];
        let currentBlock = null;
        for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
            const line = lines[lineIndex];
            const lineContainsMarker = line.indexOf(MarkdownCodeBlocks.CODE_BLOCK_MARKER) === 0;
            const constructingBlock = currentBlock != null;
            // Skip this line if it is not part of any code block and doesn't contain a marker.
            if (!lineContainsMarker && !constructingBlock) {
                continue;
            }
            // Check if we are already constructing a code block.
            if (!constructingBlock) {
                // Start constructing a new code block.
                currentBlock = new MarkdownCodeBlock(lineIndex);
                // Check whether this is a single line code block of the form ```a = 10```.
                const firstIndex = line.indexOf(MarkdownCodeBlocks.CODE_BLOCK_MARKER);
                const lastIndex = line.lastIndexOf(MarkdownCodeBlocks.CODE_BLOCK_MARKER);
                const isSingleLine = firstIndex !== lastIndex;
                if (isSingleLine) {
                    currentBlock.code = line.substring(firstIndex + MarkdownCodeBlocks.CODE_BLOCK_MARKER.length, lastIndex);
                    currentBlock.endLine = lineIndex;
                    codeBlocks.push(currentBlock);
                    currentBlock = null;
                }
            }
            else if (currentBlock) {
                if (lineContainsMarker) {
                    // End of block, finish it up.
                    currentBlock.endLine = lineIndex - 1;
                    codeBlocks.push(currentBlock);
                    currentBlock = null;
                }
                else {
                    // Append the current line.
                    currentBlock.code += line + '\n';
                }
            }
        }
        return codeBlocks;
    }
    MarkdownCodeBlocks.findMarkdownCodeBlocks = findMarkdownCodeBlocks;
})(MarkdownCodeBlocks = exports.MarkdownCodeBlocks || (exports.MarkdownCodeBlocks = {}));


/***/ }),

/***/ "../packages/coreutils/lib/pageconfig.js":
/*!***********************************************!*\
  !*** ../packages/coreutils/lib/pageconfig.js ***!
  \***********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

/* provided dependency */ var process = __webpack_require__(/*! process/browser */ "../node_modules/process/browser.js");

// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PageConfig = void 0;
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
const minimist_1 = __importDefault(__webpack_require__(/*! minimist */ "../node_modules/minimist/index.js"));
const url_1 = __webpack_require__(/*! ./url */ "../packages/coreutils/lib/url.js");
/**
 * The namespace for `PageConfig` functions.
 */
var PageConfig;
(function (PageConfig) {
    /**
     * Get global configuration data for the Jupyter application.
     *
     * @param name - The name of the configuration option.
     *
     * @returns The config value or an empty string if not found.
     *
     * #### Notes
     * All values are treated as strings.
     * For browser based applications, it is assumed that the page HTML
     * includes a script tag with the id `jupyter-config-data` containing the
     * configuration as valid JSON.  In order to support the classic Notebook,
     * we fall back on checking for `body` data of the given `name`.
     *
     * For node applications, it is assumed that the process was launched
     * with a `--jupyter-config-data` option pointing to a JSON settings
     * file.
     */
    function getOption(name) {
        if (configData) {
            return configData[name] || getBodyData(name);
        }
        configData = Object.create(null);
        let found = false;
        // Use script tag if available.
        if (typeof document !== 'undefined' && document) {
            const el = document.getElementById('jupyter-config-data');
            if (el) {
                configData = JSON.parse(el.textContent || '');
                found = true;
            }
        }
        // Otherwise use CLI if given.
        if (!found && typeof process !== 'undefined' && process.argv) {
            try {
                const cli = (0, minimist_1.default)(process.argv.slice(2));
                const path = __webpack_require__(/*! path */ "../node_modules/path-browserify/index.js");
                let fullPath = '';
                if ('jupyter-config-data' in cli) {
                    fullPath = path.resolve(cli['jupyter-config-data']);
                }
                else if ('JUPYTER_CONFIG_DATA' in process.env) {
                    fullPath = path.resolve(process.env['JUPYTER_CONFIG_DATA']);
                }
                if (fullPath) {
                    // Force Webpack to ignore this require.
                    // eslint-disable-next-line
                    configData = eval('require')(fullPath);
                }
            }
            catch (e) {
                console.error(e);
            }
        }
        if (!coreutils_1.JSONExt.isObject(configData)) {
            configData = Object.create(null);
        }
        else {
            for (const key in configData) {
                // PageConfig expects strings
                if (typeof configData[key] !== 'string') {
                    configData[key] = JSON.stringify(configData[key]);
                }
            }
        }
        return configData[name] || getBodyData(name);
    }
    PageConfig.getOption = getOption;
    /**
     * Set global configuration data for the Jupyter application.
     *
     * @param name - The name of the configuration option.
     * @param value - The value to set the option to.
     *
     * @returns The last config value or an empty string if it doesn't exist.
     */
    function setOption(name, value) {
        const last = getOption(name);
        configData[name] = value;
        return last;
    }
    PageConfig.setOption = setOption;
    /**
     * Get the base url for a Jupyter application, or the base url of the page.
     */
    function getBaseUrl() {
        return url_1.URLExt.normalize(getOption('baseUrl') || '/');
    }
    PageConfig.getBaseUrl = getBaseUrl;
    /**
     * Get the tree url for a JupyterLab application.
     */
    function getTreeUrl() {
        return url_1.URLExt.join(getBaseUrl(), getOption('treeUrl'));
    }
    PageConfig.getTreeUrl = getTreeUrl;
    /**
     * Get the base url for sharing links (usually baseUrl)
     */
    function getShareUrl() {
        return url_1.URLExt.normalize(getOption('shareUrl') || getBaseUrl());
    }
    PageConfig.getShareUrl = getShareUrl;
    /**
     * Get the tree url for shareable links.
     * Usually the same as treeUrl,
     * but overrideable e.g. when sharing with JupyterHub.
     */
    function getTreeShareUrl() {
        return url_1.URLExt.normalize(url_1.URLExt.join(getShareUrl(), getOption('treeUrl')));
    }
    PageConfig.getTreeShareUrl = getTreeShareUrl;
    /**
     * Create a new URL given an optional mode and tree path.
     *
     * This is used to create URLS when the mode or tree path change as the user
     * changes mode or the current document in the main area. If fields in
     * options are omitted, the value in PageConfig will be used.
     *
     * @param options - IGetUrlOptions for the new path.
     */
    function getUrl(options) {
        var _a, _b, _c, _d;
        let path = options.toShare ? getShareUrl() : getBaseUrl();
        const mode = (_a = options.mode) !== null && _a !== void 0 ? _a : getOption('mode');
        const workspace = (_b = options.workspace) !== null && _b !== void 0 ? _b : getOption('workspace');
        const labOrDoc = mode === 'single-document' ? 'doc' : 'lab';
        path = url_1.URLExt.join(path, labOrDoc);
        if (workspace !== PageConfig.defaultWorkspace) {
            path = url_1.URLExt.join(path, 'workspaces', encodeURIComponent((_c = getOption('workspace')) !== null && _c !== void 0 ? _c : PageConfig.defaultWorkspace));
        }
        const treePath = (_d = options.treePath) !== null && _d !== void 0 ? _d : getOption('treePath');
        if (treePath) {
            path = url_1.URLExt.join(path, 'tree', url_1.URLExt.encodeParts(treePath));
        }
        return path;
    }
    PageConfig.getUrl = getUrl;
    PageConfig.defaultWorkspace = 'default';
    /**
     * Get the base websocket url for a Jupyter application, or an empty string.
     */
    function getWsUrl(baseUrl) {
        let wsUrl = getOption('wsUrl');
        if (!wsUrl) {
            baseUrl = baseUrl ? url_1.URLExt.normalize(baseUrl) : getBaseUrl();
            if (baseUrl.indexOf('http') !== 0) {
                return '';
            }
            wsUrl = 'ws' + baseUrl.slice(4);
        }
        return url_1.URLExt.normalize(wsUrl);
    }
    PageConfig.getWsUrl = getWsUrl;
    /**
     * Returns the URL converting this notebook to a certain
     * format with nbconvert.
     */
    function getNBConvertURL({ path, format, download }) {
        const notebookPath = url_1.URLExt.encodeParts(path);
        const url = url_1.URLExt.join(getBaseUrl(), 'nbconvert', format, notebookPath);
        if (download) {
            return url + '?download=true';
        }
        return url;
    }
    PageConfig.getNBConvertURL = getNBConvertURL;
    /**
     * Get the authorization token for a Jupyter application.
     */
    function getToken() {
        return getOption('token') || getBodyData('jupyterApiToken');
    }
    PageConfig.getToken = getToken;
    /**
     * Get the Notebook version info [major, minor, patch].
     */
    function getNotebookVersion() {
        const notebookVersion = getOption('notebookVersion');
        if (notebookVersion === '') {
            return [0, 0, 0];
        }
        return JSON.parse(notebookVersion);
    }
    PageConfig.getNotebookVersion = getNotebookVersion;
    /**
     * Private page config data for the Jupyter application.
     */
    let configData = null;
    /**
     * Get a url-encoded item from `body.data` and decode it
     * We should never have any encoded URLs anywhere else in code
     * until we are building an actual request.
     */
    function getBodyData(key) {
        if (typeof document === 'undefined' || !document.body) {
            return '';
        }
        const val = document.body.dataset[key];
        if (typeof val === 'undefined') {
            return '';
        }
        return decodeURIComponent(val);
    }
    /**
     * The namespace for page config `Extension` functions.
     */
    let Extension;
    (function (Extension) {
        /**
         * Populate an array from page config.
         *
         * @param key - The page config key (e.g., `deferredExtensions`).
         *
         * #### Notes
         * This is intended for `deferredExtensions` and `disabledExtensions`.
         */
        function populate(key) {
            try {
                const raw = getOption(key);
                if (raw) {
                    return JSON.parse(raw);
                }
            }
            catch (error) {
                console.warn(`Unable to parse ${key}.`, error);
            }
            return [];
        }
        /**
         * The collection of deferred extensions in page config.
         */
        Extension.deferred = populate('deferredExtensions');
        /**
         * The collection of disabled extensions in page config.
         */
        Extension.disabled = populate('disabledExtensions');
        /**
         * Returns whether a plugin is deferred.
         *
         * @param id - The plugin ID.
         */
        function isDeferred(id) {
            // Check for either a full plugin id match or an extension
            // name match.
            const separatorIndex = id.indexOf(':');
            let extName = '';
            if (separatorIndex !== -1) {
                extName = id.slice(0, separatorIndex);
            }
            return Extension.deferred.some(val => val === id || (extName && val === extName));
        }
        Extension.isDeferred = isDeferred;
        /**
         * Returns whether a plugin is disabled.
         *
         * @param id - The plugin ID.
         */
        function isDisabled(id) {
            // Check for either a full plugin id match or an extension
            // name match.
            const separatorIndex = id.indexOf(':');
            let extName = '';
            if (separatorIndex !== -1) {
                extName = id.slice(0, separatorIndex);
            }
            return Extension.disabled.some(val => val === id || (extName && val === extName));
        }
        Extension.isDisabled = isDisabled;
    })(Extension = PageConfig.Extension || (PageConfig.Extension = {}));
})(PageConfig = exports.PageConfig || (exports.PageConfig = {}));


/***/ }),

/***/ "../packages/coreutils/lib/path.js":
/*!*****************************************!*\
  !*** ../packages/coreutils/lib/path.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PathExt = void 0;
const path_1 = __webpack_require__(/*! path */ "../node_modules/path-browserify/index.js");
/**
 * The namespace for path-related functions.
 *
 * Note that Jupyter server paths do not start with a leading slash.
 */
var PathExt;
(function (PathExt) {
    /**
     * Join all arguments together and normalize the resulting path.
     * Arguments must be strings. In v0.8, non-string arguments were silently ignored. In v0.10 and up, an exception is thrown.
     *
     * @param paths - The string paths to join.
     */
    function join(...paths) {
        const path = path_1.posix.join(...paths);
        return path === '.' ? '' : removeSlash(path);
    }
    PathExt.join = join;
    /**
     * Return the last portion of a path. Similar to the Unix basename command.
     * Often used to extract the file name from a fully qualified path.
     *
     * @param path - The path to evaluate.
     *
     * @param ext - An extension to remove from the result.
     */
    function basename(path, ext) {
        return path_1.posix.basename(path, ext);
    }
    PathExt.basename = basename;
    /**
     * Get the directory name of a path, similar to the Unix dirname command.
     * When an empty path is given, returns the root path.
     *
     * @param path - The file path.
     */
    function dirname(path) {
        const dir = removeSlash(path_1.posix.dirname(path));
        return dir === '.' ? '' : dir;
    }
    PathExt.dirname = dirname;
    /**
     * Get the extension of the path.
     *
     * @param path - The file path.
     *
     * @returns the extension of the file.
     *
     * #### Notes
     * The extension is the string from the last occurrence of the `.`
     * character to end of string in the last portion of the path, inclusive.
     * If there is no `.` in the last portion of the path, or if the first
     * character of the basename of path [[basename]] is `.`, then an
     * empty string is returned.
     */
    function extname(path) {
        return path_1.posix.extname(path);
    }
    PathExt.extname = extname;
    /**
     * Normalize a string path, reducing '..' and '.' parts.
     * When multiple slashes are found, they're replaced by a single one; when the path contains a trailing slash, it is preserved. On Windows backslashes are used.
     * When an empty path is given, returns the root path.
     *
     * @param path - The string path to normalize.
     */
    function normalize(path) {
        if (path === '') {
            return '';
        }
        return removeSlash(path_1.posix.normalize(path));
    }
    PathExt.normalize = normalize;
    /**
     * Resolve a sequence of paths or path segments into an absolute path.
     * The root path in the application has no leading slash, so it is removed.
     *
     * @param parts - The paths to join.
     *
     * #### Notes
     * The right-most parameter is considered \{to\}.  Other parameters are considered an array of \{from\}.
     *
     * Starting from leftmost \{from\} parameter, resolves \{to\} to an absolute path.
     *
     * If \{to\} isn't already absolute, \{from\} arguments are prepended in right to left order, until an absolute path is found. If after using all \{from\} paths still no absolute path is found, the current working directory is used as well. The resulting path is normalized, and trailing slashes are removed unless the path gets resolved to the root directory.
     */
    function resolve(...parts) {
        return removeSlash(path_1.posix.resolve(...parts));
    }
    PathExt.resolve = resolve;
    /**
     * Solve the relative path from \{from\} to \{to\}.
     *
     * @param from - The source path.
     *
     * @param to - The target path.
     *
     * #### Notes
     * If from and to each resolve to the same path (after calling
     * path.resolve() on each), a zero-length string is returned.
     * If a zero-length string is passed as from or to, `/`
     * will be used instead of the zero-length strings.
     */
    function relative(from, to) {
        return removeSlash(path_1.posix.relative(from, to));
    }
    PathExt.relative = relative;
    /**
     * Normalize a file extension to be of the type `'.foo'`.
     *
     * @param extension - the file extension.
     *
     * #### Notes
     * Adds a leading dot if not present and converts to lower case.
     */
    function normalizeExtension(extension) {
        if (extension.length > 0 && extension.indexOf('.') !== 0) {
            extension = `.${extension}`;
        }
        return extension;
    }
    PathExt.normalizeExtension = normalizeExtension;
    /**
     * Remove the leading slash from a path.
     *
     * @param path: the path from which to remove a leading slash.
     */
    function removeSlash(path) {
        if (path.indexOf('/') === 0) {
            path = path.slice(1);
        }
        return path;
    }
    PathExt.removeSlash = removeSlash;
})(PathExt = exports.PathExt || (exports.PathExt = {}));


/***/ }),

/***/ "../packages/coreutils/lib/signal.js":
/*!*******************************************!*\
  !*** ../packages/coreutils/lib/signal.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.signalToPromise = void 0;
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/**
 * Convert a signal into a promise for the first emitted value.
 *
 * @param signal - The signal we are listening to.
 * @param timeout - Timeout to wait for signal in ms (not timeout if not defined or 0)
 *
 * @returns a Promise that resolves with a `(sender, args)` pair.
 */
function signalToPromise(signal, timeout) {
    const waitForSignal = new coreutils_1.PromiseDelegate();
    function cleanup() {
        signal.disconnect(slot);
    }
    function slot(sender, args) {
        cleanup();
        waitForSignal.resolve([sender, args]);
    }
    signal.connect(slot);
    if ((timeout !== null && timeout !== void 0 ? timeout : 0) > 0) {
        setTimeout(() => {
            cleanup();
            waitForSignal.reject(`Signal not emitted within ${timeout} ms.`);
        }, timeout);
    }
    return waitForSignal.promise;
}
exports.signalToPromise = signalToPromise;


/***/ }),

/***/ "../packages/coreutils/lib/text.js":
/*!*****************************************!*\
  !*** ../packages/coreutils/lib/text.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Text = void 0;
/**
 * The namespace for text-related functions.
 */
var Text;
(function (Text) {
    // javascript stores text as utf16 and string indices use "code units",
    // which stores high-codepoint characters as "surrogate pairs",
    // which occupy two indices in the javascript string.
    // We need to translate cursor_pos in the Jupyter protocol (in characters)
    // to js offset (with surrogate pairs taking two spots).
    const HAS_SURROGATES = '𝐚'.length > 1;
    /**
     * Convert a javascript string index into a unicode character offset
     *
     * @param jsIdx - The javascript string index (counting surrogate pairs)
     *
     * @param text - The text in which the offset is calculated
     *
     * @returns The unicode character offset
     */
    function jsIndexToCharIndex(jsIdx, text) {
        if (HAS_SURROGATES) {
            // not using surrogates, nothing to do
            return jsIdx;
        }
        let charIdx = jsIdx;
        for (let i = 0; i + 1 < text.length && i < jsIdx; i++) {
            const charCode = text.charCodeAt(i);
            // check for surrogate pair
            if (charCode >= 0xd800 && charCode <= 0xdbff) {
                const nextCharCode = text.charCodeAt(i + 1);
                if (nextCharCode >= 0xdc00 && nextCharCode <= 0xdfff) {
                    charIdx--;
                    i++;
                }
            }
        }
        return charIdx;
    }
    Text.jsIndexToCharIndex = jsIndexToCharIndex;
    /**
     * Convert a unicode character offset to a javascript string index.
     *
     * @param charIdx - The index in unicode characters
     *
     * @param text - The text in which the offset is calculated
     *
     * @returns The js-native index
     */
    function charIndexToJsIndex(charIdx, text) {
        if (HAS_SURROGATES) {
            // not using surrogates, nothing to do
            return charIdx;
        }
        let jsIdx = charIdx;
        for (let i = 0; i + 1 < text.length && i < jsIdx; i++) {
            const charCode = text.charCodeAt(i);
            // check for surrogate pair
            if (charCode >= 0xd800 && charCode <= 0xdbff) {
                const nextCharCode = text.charCodeAt(i + 1);
                if (nextCharCode >= 0xdc00 && nextCharCode <= 0xdfff) {
                    jsIdx++;
                    i++;
                }
            }
        }
        return jsIdx;
    }
    Text.charIndexToJsIndex = charIndexToJsIndex;
    /**
     * Given a 'snake-case', 'snake_case', 'snake:case', or
     * 'snake case' string, will return the camel case version: 'snakeCase'.
     *
     * @param str: the snake-case input string.
     *
     * @param upper: default = false. If true, the first letter of the
     * returned string will be capitalized.
     *
     * @returns the camel case version of the input string.
     */
    function camelCase(str, upper = false) {
        return str.replace(/^(\w)|[\s-_:]+(\w)/g, function (match, p1, p2) {
            if (p2) {
                return p2.toUpperCase();
            }
            else {
                return upper ? p1.toUpperCase() : p1.toLowerCase();
            }
        });
    }
    Text.camelCase = camelCase;
    /**
     * Given a string, title case the words in the string.
     *
     * @param str: the string to title case.
     *
     * @returns the same string, but with each word capitalized.
     */
    function titleCase(str) {
        return (str || '')
            .toLowerCase()
            .split(' ')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }
    Text.titleCase = titleCase;
})(Text = exports.Text || (exports.Text = {}));


/***/ }),

/***/ "../packages/coreutils/lib/time.js":
/*!*****************************************!*\
  !*** ../packages/coreutils/lib/time.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Time = void 0;
/**
 * A list of time units with their associated value in milliseconds.
 */
const UNITS = [
    { name: 'years', milliseconds: 365 * 24 * 60 * 60 * 1000 },
    { name: 'months', milliseconds: 30 * 24 * 60 * 60 * 1000 },
    { name: 'days', milliseconds: 24 * 60 * 60 * 1000 },
    { name: 'hours', milliseconds: 60 * 60 * 1000 },
    { name: 'minutes', milliseconds: 60 * 1000 },
    { name: 'seconds', milliseconds: 1000 }
];
/**
 * The namespace for date functions.
 */
var Time;
(function (Time) {
    /**
     * Convert a timestring to a human readable string (e.g. 'two minutes ago').
     *
     * @param value - The date timestring or date object.
     *
     * @returns A formatted date.
     */
    function formatHuman(value) {
        const lang = document.documentElement.lang || 'en';
        const formatter = new Intl.RelativeTimeFormat(lang, { numeric: 'auto' });
        const delta = new Date(value).getTime() - Date.now();
        for (let unit of UNITS) {
            const amount = Math.ceil(delta / unit.milliseconds);
            if (amount === 0) {
                continue;
            }
            return formatter.format(amount, unit.name);
        }
        return formatter.format(0, 'seconds');
    }
    Time.formatHuman = formatHuman;
    /**
     * Convenient helper to convert a timestring to a date format.
     *
     * @param value - The date timestring or date object.
     *
     * @returns A formatted date.
     */
    function format(value) {
        const lang = document.documentElement.lang || 'en';
        const formatter = new Intl.DateTimeFormat(lang, {
            dateStyle: 'short',
            timeStyle: 'short'
        });
        return formatter.format(new Date(value));
    }
    Time.format = format;
})(Time = exports.Time || (exports.Time = {}));


/***/ }),

/***/ "../packages/coreutils/lib/url.js":
/*!****************************************!*\
  !*** ../packages/coreutils/lib/url.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.URLExt = void 0;
const path_1 = __webpack_require__(/*! path */ "../node_modules/path-browserify/index.js");
const url_parse_1 = __importDefault(__webpack_require__(/*! url-parse */ "../node_modules/url-parse/index.js"));
/**
 * The namespace for URL-related functions.
 */
var URLExt;
(function (URLExt) {
    /**
     * Parse a url into a URL object.
     *
     * @param urlString - The URL string to parse.
     *
     * @returns A URL object.
     */
    function parse(url) {
        if (typeof document !== 'undefined' && document) {
            const a = document.createElement('a');
            a.href = url;
            return a;
        }
        return (0, url_parse_1.default)(url);
    }
    URLExt.parse = parse;
    /**
     * Parse URL and retrieve hostname
     *
     * @param url - The URL string to parse
     *
     * @returns a hostname string value
     */
    function getHostName(url) {
        return (0, url_parse_1.default)(url).hostname;
    }
    URLExt.getHostName = getHostName;
    function normalize(url) {
        return url && parse(url).toString();
    }
    URLExt.normalize = normalize;
    /**
     * Join a sequence of url components and normalizes as in node `path.join`.
     *
     * @param parts - The url components.
     *
     * @returns the joined url.
     */
    function join(...parts) {
        let u = (0, url_parse_1.default)(parts[0], {});
        // Schema-less URL can be only parsed as relative to a base URL
        // see https://github.com/unshiftio/url-parse/issues/219#issuecomment-1002219326
        const isSchemaLess = u.protocol === '' && u.slashes;
        if (isSchemaLess) {
            u = (0, url_parse_1.default)(parts[0], 'https:' + parts[0]);
        }
        const prefix = `${isSchemaLess ? '' : u.protocol}${u.slashes ? '//' : ''}${u.auth}${u.auth ? '@' : ''}${u.host}`;
        // If there was a prefix, then the first path must start at the root.
        const path = path_1.posix.join(`${!!prefix && u.pathname[0] !== '/' ? '/' : ''}${u.pathname}`, ...parts.slice(1));
        return `${prefix}${path === '.' ? '' : path}`;
    }
    URLExt.join = join;
    /**
     * Encode the components of a multi-segment url.
     *
     * @param url - The url to encode.
     *
     * @returns the encoded url.
     *
     * #### Notes
     * Preserves the `'/'` separators.
     * Should not include the base url, since all parts are escaped.
     */
    function encodeParts(url) {
        return join(...url.split('/').map(encodeURIComponent));
    }
    URLExt.encodeParts = encodeParts;
    /**
     * Return a serialized object string suitable for a query.
     *
     * @param object - The source object.
     *
     * @returns an encoded url query.
     *
     * #### Notes
     * Modified version of [stackoverflow](http://stackoverflow.com/a/30707423).
     */
    function objectToQueryString(value) {
        const keys = Object.keys(value).filter(key => key.length > 0);
        if (!keys.length) {
            return '';
        }
        return ('?' +
            keys
                .map(key => {
                const content = encodeURIComponent(String(value[key]));
                return key + (content ? '=' + content : '');
            })
                .join('&'));
    }
    URLExt.objectToQueryString = objectToQueryString;
    /**
     * Return a parsed object that represents the values in a query string.
     */
    function queryStringToObject(value) {
        return value
            .replace(/^\?/, '')
            .split('&')
            .reduce((acc, val) => {
            const [key, value] = val.split('=');
            if (key.length > 0) {
                acc[key] = decodeURIComponent(value || '');
            }
            return acc;
        }, {});
    }
    URLExt.queryStringToObject = queryStringToObject;
    /**
     * Test whether the url is a local url.
     *
     * #### Notes
     * This function returns `false` for any fully qualified url, including
     * `data:`, `file:`, and `//` protocol URLs.
     */
    function isLocal(url) {
        const { protocol } = parse(url);
        return ((!protocol || url.toLowerCase().indexOf(protocol) !== 0) &&
            url.indexOf('/') !== 0);
    }
    URLExt.isLocal = isLocal;
})(URLExt = exports.URLExt || (exports.URLExt = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY29yZXV0aWxzX2xpYl9pbmRleF9qcy5mZDBlNzVhZmJlMTg2YTRjZjQ5OC5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDs7O0FBRzNELHdJQUFvRDtBQUVwRDs7R0FFRztBQUNILE1BQWEsZUFBZTtJQUMxQjs7T0FFRztJQUNILFlBQVksT0FBK0M7UUE2RG5ELFdBQU0sR0FBUSxDQUFDLENBQUMsQ0FBQztRQUNqQixhQUFRLEdBQUcsQ0FBQyxDQUFDLENBQUM7UUFHZCxnQkFBVyxHQUFHLEtBQUssQ0FBQztRQUNwQixxQkFBZ0IsR0FBRyxJQUFJLGtCQUFNLENBR25DLElBQUksQ0FBQyxDQUFDO1FBcEVOLE9BQU8sQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxjQUFjLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFDbEQsSUFBSSxDQUFDLFFBQVEsR0FBRyxPQUFPLENBQUMsT0FBTyxJQUFJLElBQUksQ0FBQztJQUMxQyxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLGVBQWU7UUFJakIsT0FBTyxJQUFJLENBQUMsZ0JBQWdCLENBQUM7SUFDL0IsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxPQUFPO1FBQ1QsT0FBTyxJQUFJLENBQUMsUUFBUSxDQUFDO0lBQ3ZCLENBQUM7SUFDRCxJQUFJLE9BQU8sQ0FBQyxLQUFhO1FBQ3ZCLElBQUksQ0FBQyxRQUFRLEdBQUcsS0FBSyxDQUFDO0lBQ3hCLENBQUM7SUFFRDs7Ozs7T0FLRztJQUNILElBQUksVUFBVTtRQUNaLE9BQU8sSUFBSSxDQUFDLFdBQVcsQ0FBQztJQUMxQixDQUFDO0lBRUQ7O09BRUc7SUFDSCxPQUFPO1FBQ0wsSUFBSSxJQUFJLENBQUMsV0FBVyxFQUFFO1lBQ3BCLE9BQU87U0FDUjtRQUNELElBQUksQ0FBQyxXQUFXLEdBQUcsSUFBSSxDQUFDO1FBQ3hCLGtCQUFNLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxDQUFDO0lBQ3pC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Q0gsU0FBZ0IsbUJBQW1CLENBQUMsS0FBYTtRQUcvQyxPQUFPLEtBQUs7YUFDVCxPQUFPLENBQUMsS0FBSyxFQUFFLEVBQUUsQ0FBQzthQUNsQixLQUFLLENBQUMsR0FBRyxDQUFDO2FBQ1YsTUFBTSxDQUNMLENBQUMsR0FBRyxFQUFFLEdBQUcsRUFBRSxFQUFFO1lBQ1gsTUFBTSxDQUFDLEdBQUcsRUFBRSxLQUFLLENBQUMsR0FBRyxHQUFHLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDO1lBRXBDLElBQUksR0FBRyxDQUFDLE1BQU0sR0FBRyxDQUFDLEVBQUU7Z0JBQ2xCLEdBQUcsQ0FBQyxHQUFHLENBQUMsR0FBRyxrQkFBa0IsQ0FBQyxLQUFLLElBQUksRUFBRSxDQUFDLENBQUM7YUFDNUM7WUFFRCxPQUFPLEdBQUcsQ0FBQztRQUNiLENBQUMsRUFDRCxFQUErQixDQUNoQyxDQUFDO0lBQ04sQ0FBQztJQWxCZSwwQkFBbUIsc0JBa0JsQztJQUVEOzs7Ozs7T0FNRztJQUNILFNBQWdCLE9BQU8sQ0FBQyxHQUFXO1FBQ2pDLE1BQU0sRUFBRSxRQUFRLEVBQUUsR0FBRyxLQUFLLENBQUMsR0FBRyxDQUFDLENBQUM7UUFFaEMsT0FBTyxDQUNMLENBQUMsQ0FBQyxRQUFRLElBQUksR0FBRyxDQUFDLFdBQVcsRUFBRSxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLENBQUM7WUFDeEQsR0FBRyxDQUFDLE9BQU8sQ0FBQyxHQUFHLENBQUMsS0FBSyxDQUFDLENBQ3ZCLENBQUM7SUFDSixDQUFDO0lBUGUsY0FBTyxVQU90QjtBQW1ESCxDQUFDLEVBbk1nQixNQUFNLEdBQU4sY0FBTSxLQUFOLGNBQU0sUUFtTXRCIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvcmV1dGlscy9zcmMvYWN0aXZpdHltb25pdG9yLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb3JldXRpbHMvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb3JldXRpbHMvc3JjL2ludGVyZmFjZXMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvcmV1dGlscy9zcmMvbHJ1LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb3JldXRpbHMvc3JjL21hcmtkb3duY29kZWJsb2Nrcy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29yZXV0aWxzL3NyYy9wYWdlY29uZmlnLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb3JldXRpbHMvc3JjL3BhdGgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvcmV1dGlscy9zcmMvc2lnbmFsLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb3JldXRpbHMvc3JjL3RleHQudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvcmV1dGlscy9zcmMvdGltZS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvY29yZXV0aWxzL3NyYy91cmwudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IG1vbml0b3JzIGFjdGl2aXR5IG9uIGEgc2lnbmFsLlxuICovXG5leHBvcnQgY2xhc3MgQWN0aXZpdHlNb25pdG9yPFNlbmRlciwgQXJncz4gaW1wbGVtZW50cyBJRGlzcG9zYWJsZSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgYWN0aXZpdHkgbW9uaXRvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEFjdGl2aXR5TW9uaXRvci5JT3B0aW9uczxTZW5kZXIsIEFyZ3M+KSB7XG4gICAgb3B0aW9ucy5zaWduYWwuY29ubmVjdCh0aGlzLl9vblNpZ25hbEZpcmVkLCB0aGlzKTtcbiAgICB0aGlzLl90aW1lb3V0ID0gb3B0aW9ucy50aW1lb3V0IHx8IDEwMDA7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGFjdGl2aXR5IGhhcyBjZWFzZWQuXG4gICAqL1xuICBnZXQgYWN0aXZpdHlTdG9wcGVkKCk6IElTaWduYWw8XG4gICAgdGhpcyxcbiAgICBBY3Rpdml0eU1vbml0b3IuSUFyZ3VtZW50czxTZW5kZXIsIEFyZ3M+XG4gID4ge1xuICAgIHJldHVybiB0aGlzLl9hY3Rpdml0eVN0b3BwZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHRpbWVvdXQgYXNzb2NpYXRlZCB3aXRoIHRoZSBtb25pdG9yLCBpbiBtaWxsaXNlY29uZHMuXG4gICAqL1xuICBnZXQgdGltZW91dCgpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLl90aW1lb3V0O1xuICB9XG4gIHNldCB0aW1lb3V0KHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLl90aW1lb3V0ID0gdmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSBtb25pdG9yIGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgaXMgYSByZWFkLW9ubHkgcHJvcGVydHkuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgdXNlZCBieSB0aGUgYWN0aXZpdHkgbW9uaXRvci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2lzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgU2lnbmFsLmNsZWFyRGF0YSh0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBoYW5kbGVyIGZvciB0aGUgbW9uaXRvcmVkIHNpZ25hbC5cbiAgICovXG4gIHByaXZhdGUgX29uU2lnbmFsRmlyZWQoc2VuZGVyOiBTZW5kZXIsIGFyZ3M6IEFyZ3MpOiB2b2lkIHtcbiAgICBjbGVhclRpbWVvdXQodGhpcy5fdGltZXIpO1xuICAgIHRoaXMuX3NlbmRlciA9IHNlbmRlcjtcbiAgICB0aGlzLl9hcmdzID0gYXJncztcbiAgICB0aGlzLl90aW1lciA9IHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgdGhpcy5fYWN0aXZpdHlTdG9wcGVkLmVtaXQoe1xuICAgICAgICBzZW5kZXI6IHRoaXMuX3NlbmRlcixcbiAgICAgICAgYXJnczogdGhpcy5fYXJnc1xuICAgICAgfSk7XG4gICAgfSwgdGhpcy5fdGltZW91dCk7XG4gIH1cblxuICBwcml2YXRlIF90aW1lcjogYW55ID0gLTE7XG4gIHByaXZhdGUgX3RpbWVvdXQgPSAtMTtcbiAgcHJpdmF0ZSBfc2VuZGVyOiBTZW5kZXI7XG4gIHByaXZhdGUgX2FyZ3M6IEFyZ3M7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfYWN0aXZpdHlTdG9wcGVkID0gbmV3IFNpZ25hbDxcbiAgICB0aGlzLFxuICAgIEFjdGl2aXR5TW9uaXRvci5JQXJndW1lbnRzPFNlbmRlciwgQXJncz5cbiAgPih0aGlzKTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBgQWN0aXZpdHlNb25pdG9yYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIEFjdGl2aXR5TW9uaXRvciB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGNvbnN0cnVjdCBhIG5ldyBgQWN0aXZpdHlNb25pdG9yYC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnM8U2VuZGVyLCBBcmdzPiB7XG4gICAgLyoqXG4gICAgICogVGhlIHNpZ25hbCB0byBtb25pdG9yLlxuICAgICAqL1xuICAgIHNpZ25hbDogSVNpZ25hbDxTZW5kZXIsIEFyZ3M+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFjdGl2aXR5IHRpbWVvdXQgaW4gbWlsbGlzZWNvbmRzLlxuICAgICAqXG4gICAgICogVGhlIGRlZmF1bHQgaXMgMSBzZWNvbmQuXG4gICAgICovXG4gICAgdGltZW91dD86IG51bWJlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgYXJndW1lbnQgb2JqZWN0IGZvciBhbiBhY3Rpdml0eSB0aW1lb3V0LlxuICAgKlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQXJndW1lbnRzPFNlbmRlciwgQXJncz4ge1xuICAgIC8qKlxuICAgICAqIFRoZSBtb3N0IHJlY2VudCBzZW5kZXIgb2JqZWN0LlxuICAgICAqL1xuICAgIHNlbmRlcjogU2VuZGVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1vc3QgcmVjZW50IGFyZ3VtZW50IG9iamVjdC5cbiAgICAgKi9cbiAgICBhcmdzOiBBcmdzO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBjb3JldXRpbHNcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL2FjdGl2aXR5bW9uaXRvcic7XG5leHBvcnQgKiBmcm9tICcuL2ludGVyZmFjZXMnO1xuZXhwb3J0ICogZnJvbSAnLi9scnUnO1xuZXhwb3J0ICogZnJvbSAnLi9tYXJrZG93bmNvZGVibG9ja3MnO1xuZXhwb3J0ICogZnJvbSAnLi9wYWdlY29uZmlnJztcbmV4cG9ydCAqIGZyb20gJy4vcGF0aCc7XG5leHBvcnQgKiBmcm9tICcuL3NpZ25hbCc7XG5leHBvcnQgKiBmcm9tICcuL3RleHQnO1xuZXhwb3J0ICogZnJvbSAnLi90aW1lJztcbmV4cG9ydCAqIGZyb20gJy4vdXJsJztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuLyoqXG4gKiBBIGdlbmVyaWMgaW50ZXJmYWNlIGZvciBjaGFuZ2UgZW1pdHRlciBwYXlsb2Fkcy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJQ2hhbmdlZEFyZ3M8VCwgT2xkVCA9IFQsIFUgZXh0ZW5kcyBzdHJpbmcgPSBzdHJpbmc+IHtcbiAgLyoqXG4gICAqIFRoZSBuYW1lIG9mIHRoZSBjaGFuZ2VkIGF0dHJpYnV0ZS5cbiAgICovXG4gIG5hbWU6IFU7XG5cbiAgLyoqXG4gICAqIFRoZSBvbGQgdmFsdWUgb2YgdGhlIGNoYW5nZWQgYXR0cmlidXRlLlxuICAgKi9cbiAgb2xkVmFsdWU6IE9sZFQ7XG5cbiAgLyoqXG4gICAqIFRoZSBuZXcgdmFsdWUgb2YgdGhlIGNoYW5nZWQgYXR0cmlidXRlLlxuICAgKi9cbiAgbmV3VmFsdWU6IFQ7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmNvbnN0IERFRkFVTFRfTUFYX1NJWkUgPSAxMjg7XG5cbi8qKiBBIGxlYXN0LXJlY2VudGx5LXVzZWQgY2FjaGUuICovXG5leHBvcnQgY2xhc3MgTHJ1Q2FjaGU8VCwgVT4ge1xuICBwcm90ZWN0ZWQgX21hcCA9IG5ldyBNYXA8VCwgVT4oKTtcbiAgcHJvdGVjdGVkIF9tYXhTaXplOiBudW1iZXI7XG5cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTHJ1Q2FjaGUuSU9wdGlvbnMgPSB7fSkge1xuICAgIHRoaXMuX21heFNpemUgPSBvcHRpb25zPy5tYXhTaXplIHx8IERFRkFVTFRfTUFYX1NJWkU7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJuIHRoZSBjdXJyZW50IHNpemUgb2YgdGhlIGNhY2hlLlxuICAgKi9cbiAgZ2V0IHNpemUoKSB7XG4gICAgcmV0dXJuIHRoaXMuX21hcC5zaXplO1xuICB9XG5cbiAgLyoqXG4gICAqIENsZWFyIHRoZSB2YWx1ZXMgaW4gdGhlIGNhY2hlLlxuICAgKi9cbiAgY2xlYXIoKSB7XG4gICAgdGhpcy5fbWFwLmNsZWFyKCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGEgdmFsdWUgKG9yIG51bGwpIGZyb20gdGhlIGNhY2hlLCBwdXNoaW5nIHRoZSBpdGVtIHRvIHRoZSBmcm9udCBvZiB0aGUgY2FjaGUuXG4gICAqL1xuICBnZXQoa2V5OiBUKTogVSB8IG51bGwge1xuICAgIGNvbnN0IGl0ZW0gPSB0aGlzLl9tYXAuZ2V0KGtleSkgfHwgbnVsbDtcbiAgICBpZiAoaXRlbSAhPSBudWxsKSB7XG4gICAgICB0aGlzLl9tYXAuZGVsZXRlKGtleSk7XG4gICAgICB0aGlzLl9tYXAuc2V0KGtleSwgaXRlbSk7XG4gICAgfVxuICAgIHJldHVybiBpdGVtO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIHZhbHVlIGluIHRoZSBjYWNoZSwgcG90ZW50aWFsbHkgZXZpY3RpbmcgYW4gb2xkIGl0ZW0uXG4gICAqL1xuICBzZXQoa2V5OiBULCB2YWx1ZTogVSk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9tYXAuc2l6ZSA+PSB0aGlzLl9tYXhTaXplKSB7XG4gICAgICB0aGlzLl9tYXAuZGVsZXRlKHRoaXMuX21hcC5rZXlzKCkubmV4dCgpLnZhbHVlKTtcbiAgICB9XG4gICAgdGhpcy5fbWFwLnNldChrZXksIHZhbHVlKTtcbiAgfVxufVxuXG5leHBvcnQgbmFtZXNwYWNlIExydUNhY2hlIHtcbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgbWF4U2l6ZT86IG51bWJlciB8IG51bGw7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBjb2RlIGJsb2NrIGZ1bmN0aW9ucyB3aGljaCBoZWxwXG4gKiBpbiBleHRyYWN0IGNvZGUgZnJvbSBtYXJrZG93biB0ZXh0XG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgTWFya2Rvd25Db2RlQmxvY2tzIHtcbiAgZXhwb3J0IGNvbnN0IENPREVfQkxPQ0tfTUFSS0VSID0gJ2BgYCc7XG4gIGNvbnN0IG1hcmtkb3duRXh0ZW5zaW9uczogc3RyaW5nW10gPSBbXG4gICAgJy5tYXJrZG93bicsXG4gICAgJy5tZG93bicsXG4gICAgJy5ta2RuJyxcbiAgICAnLm1kJyxcbiAgICAnLm1rZCcsXG4gICAgJy5tZHduJyxcbiAgICAnLm1kdHh0JyxcbiAgICAnLm1kdGV4dCcsXG4gICAgJy50ZXh0JyxcbiAgICAnLnR4dCcsXG4gICAgJy5SbWQnXG4gIF07XG5cbiAgZXhwb3J0IGNsYXNzIE1hcmtkb3duQ29kZUJsb2NrIHtcbiAgICBzdGFydExpbmU6IG51bWJlcjtcbiAgICBlbmRMaW5lOiBudW1iZXI7XG4gICAgY29kZTogc3RyaW5nO1xuICAgIGNvbnN0cnVjdG9yKHN0YXJ0TGluZTogbnVtYmVyKSB7XG4gICAgICB0aGlzLnN0YXJ0TGluZSA9IHN0YXJ0TGluZTtcbiAgICAgIHRoaXMuY29kZSA9ICcnO1xuICAgICAgdGhpcy5lbmRMaW5lID0gLTE7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIENoZWNrIHdoZXRoZXIgdGhlIGdpdmVuIGZpbGUgZXh0ZW5zaW9uIGlzIGEgbWFya2Rvd24gZXh0ZW5zaW9uXG4gICAqIEBwYXJhbSBleHRlbnNpb24gLSBBIGZpbGUgZXh0ZW5zaW9uXG4gICAqXG4gICAqIEByZXR1cm5zIHRydWUvZmFsc2UgZGVwZW5kaW5nIG9uIHdoZXRoZXIgdGhpcyBpcyBhIHN1cHBvcnRlZCBtYXJrZG93biBleHRlbnNpb25cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBpc01hcmtkb3duKGV4dGVuc2lvbjogc3RyaW5nKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIG1hcmtkb3duRXh0ZW5zaW9ucy5pbmRleE9mKGV4dGVuc2lvbikgPiAtMTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYWxsIGNvZGUgc25pcHBldHMgZnJvbSBjdXJyZW50IHRleHRcbiAgICogKHRoaXMgY291bGQgYmUgcG90ZW50aWFsbHkgb3B0aW1pemVkIGlmIHdlIGNhbiBjYWNoZSBhbmQgZGV0ZWN0IGRpZmZlcmVuY2VzKVxuICAgKiBAcGFyYW0gdGV4dCAtIEEgc3RyaW5nIHRvIHBhcnNlIGNvZGVibG9ja3MgZnJvbVxuICAgKlxuICAgKiBAcmV0dXJucyBBbiBhcnJheSBvZiBNYXJrZG93bkNvZGVCbG9ja3MuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZmluZE1hcmtkb3duQ29kZUJsb2Nrcyh0ZXh0OiBzdHJpbmcpOiBNYXJrZG93bkNvZGVCbG9ja1tdIHtcbiAgICBpZiAoIXRleHQgfHwgdGV4dCA9PT0gJycpIHtcbiAgICAgIHJldHVybiBbXTtcbiAgICB9XG5cbiAgICBjb25zdCBsaW5lcyA9IHRleHQuc3BsaXQoJ1xcbicpO1xuICAgIGNvbnN0IGNvZGVCbG9ja3M6IE1hcmtkb3duQ29kZUJsb2NrW10gPSBbXTtcbiAgICBsZXQgY3VycmVudEJsb2NrID0gbnVsbDtcbiAgICBmb3IgKGxldCBsaW5lSW5kZXggPSAwOyBsaW5lSW5kZXggPCBsaW5lcy5sZW5ndGg7IGxpbmVJbmRleCsrKSB7XG4gICAgICBjb25zdCBsaW5lID0gbGluZXNbbGluZUluZGV4XTtcbiAgICAgIGNvbnN0IGxpbmVDb250YWluc01hcmtlciA9IGxpbmUuaW5kZXhPZihDT0RFX0JMT0NLX01BUktFUikgPT09IDA7XG4gICAgICBjb25zdCBjb25zdHJ1Y3RpbmdCbG9jayA9IGN1cnJlbnRCbG9jayAhPSBudWxsO1xuICAgICAgLy8gU2tpcCB0aGlzIGxpbmUgaWYgaXQgaXMgbm90IHBhcnQgb2YgYW55IGNvZGUgYmxvY2sgYW5kIGRvZXNuJ3QgY29udGFpbiBhIG1hcmtlci5cbiAgICAgIGlmICghbGluZUNvbnRhaW5zTWFya2VyICYmICFjb25zdHJ1Y3RpbmdCbG9jaykge1xuICAgICAgICBjb250aW51ZTtcbiAgICAgIH1cblxuICAgICAgLy8gQ2hlY2sgaWYgd2UgYXJlIGFscmVhZHkgY29uc3RydWN0aW5nIGEgY29kZSBibG9jay5cbiAgICAgIGlmICghY29uc3RydWN0aW5nQmxvY2spIHtcbiAgICAgICAgLy8gU3RhcnQgY29uc3RydWN0aW5nIGEgbmV3IGNvZGUgYmxvY2suXG4gICAgICAgIGN1cnJlbnRCbG9jayA9IG5ldyBNYXJrZG93bkNvZGVCbG9jayhsaW5lSW5kZXgpO1xuXG4gICAgICAgIC8vIENoZWNrIHdoZXRoZXIgdGhpcyBpcyBhIHNpbmdsZSBsaW5lIGNvZGUgYmxvY2sgb2YgdGhlIGZvcm0gYGBgYSA9IDEwYGBgLlxuICAgICAgICBjb25zdCBmaXJzdEluZGV4ID0gbGluZS5pbmRleE9mKENPREVfQkxPQ0tfTUFSS0VSKTtcbiAgICAgICAgY29uc3QgbGFzdEluZGV4ID0gbGluZS5sYXN0SW5kZXhPZihDT0RFX0JMT0NLX01BUktFUik7XG4gICAgICAgIGNvbnN0IGlzU2luZ2xlTGluZSA9IGZpcnN0SW5kZXggIT09IGxhc3RJbmRleDtcbiAgICAgICAgaWYgKGlzU2luZ2xlTGluZSkge1xuICAgICAgICAgIGN1cnJlbnRCbG9jay5jb2RlID0gbGluZS5zdWJzdHJpbmcoXG4gICAgICAgICAgICBmaXJzdEluZGV4ICsgQ09ERV9CTE9DS19NQVJLRVIubGVuZ3RoLFxuICAgICAgICAgICAgbGFzdEluZGV4XG4gICAgICAgICAgKTtcbiAgICAgICAgICBjdXJyZW50QmxvY2suZW5kTGluZSA9IGxpbmVJbmRleDtcbiAgICAgICAgICBjb2RlQmxvY2tzLnB1c2goY3VycmVudEJsb2NrKTtcbiAgICAgICAgICBjdXJyZW50QmxvY2sgPSBudWxsO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKGN1cnJlbnRCbG9jaykge1xuICAgICAgICBpZiAobGluZUNvbnRhaW5zTWFya2VyKSB7XG4gICAgICAgICAgLy8gRW5kIG9mIGJsb2NrLCBmaW5pc2ggaXQgdXAuXG4gICAgICAgICAgY3VycmVudEJsb2NrLmVuZExpbmUgPSBsaW5lSW5kZXggLSAxO1xuICAgICAgICAgIGNvZGVCbG9ja3MucHVzaChjdXJyZW50QmxvY2spO1xuICAgICAgICAgIGN1cnJlbnRCbG9jayA9IG51bGw7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgLy8gQXBwZW5kIHRoZSBjdXJyZW50IGxpbmUuXG4gICAgICAgICAgY3VycmVudEJsb2NrLmNvZGUgKz0gbGluZSArICdcXG4nO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBjb2RlQmxvY2tzO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IEpTT05FeHQgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgbWluaW1pc3QgZnJvbSAnbWluaW1pc3QnO1xuaW1wb3J0IHsgVVJMRXh0IH0gZnJvbSAnLi91cmwnO1xuXG4vKipcbiAqIERlY2xhcmUgc3R1YnMgZm9yIHRoZSBub2RlIHZhcmlhYmxlcy5cbiAqL1xuZGVjbGFyZSBsZXQgcHJvY2VzczogYW55O1xuZGVjbGFyZSBsZXQgcmVxdWlyZTogYW55O1xuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGBQYWdlQ29uZmlnYCBmdW5jdGlvbnMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgUGFnZUNvbmZpZyB7XG4gIC8qKlxuICAgKiBHZXQgZ2xvYmFsIGNvbmZpZ3VyYXRpb24gZGF0YSBmb3IgdGhlIEp1cHl0ZXIgYXBwbGljYXRpb24uXG4gICAqXG4gICAqIEBwYXJhbSBuYW1lIC0gVGhlIG5hbWUgb2YgdGhlIGNvbmZpZ3VyYXRpb24gb3B0aW9uLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY29uZmlnIHZhbHVlIG9yIGFuIGVtcHR5IHN0cmluZyBpZiBub3QgZm91bmQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogQWxsIHZhbHVlcyBhcmUgdHJlYXRlZCBhcyBzdHJpbmdzLlxuICAgKiBGb3IgYnJvd3NlciBiYXNlZCBhcHBsaWNhdGlvbnMsIGl0IGlzIGFzc3VtZWQgdGhhdCB0aGUgcGFnZSBIVE1MXG4gICAqIGluY2x1ZGVzIGEgc2NyaXB0IHRhZyB3aXRoIHRoZSBpZCBganVweXRlci1jb25maWctZGF0YWAgY29udGFpbmluZyB0aGVcbiAgICogY29uZmlndXJhdGlvbiBhcyB2YWxpZCBKU09OLiAgSW4gb3JkZXIgdG8gc3VwcG9ydCB0aGUgY2xhc3NpYyBOb3RlYm9vayxcbiAgICogd2UgZmFsbCBiYWNrIG9uIGNoZWNraW5nIGZvciBgYm9keWAgZGF0YSBvZiB0aGUgZ2l2ZW4gYG5hbWVgLlxuICAgKlxuICAgKiBGb3Igbm9kZSBhcHBsaWNhdGlvbnMsIGl0IGlzIGFzc3VtZWQgdGhhdCB0aGUgcHJvY2VzcyB3YXMgbGF1bmNoZWRcbiAgICogd2l0aCBhIGAtLWp1cHl0ZXItY29uZmlnLWRhdGFgIG9wdGlvbiBwb2ludGluZyB0byBhIEpTT04gc2V0dGluZ3NcbiAgICogZmlsZS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXRPcHRpb24obmFtZTogc3RyaW5nKTogc3RyaW5nIHtcbiAgICBpZiAoY29uZmlnRGF0YSkge1xuICAgICAgcmV0dXJuIGNvbmZpZ0RhdGFbbmFtZV0gfHwgZ2V0Qm9keURhdGEobmFtZSk7XG4gICAgfVxuICAgIGNvbmZpZ0RhdGEgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuICAgIGxldCBmb3VuZCA9IGZhbHNlO1xuXG4gICAgLy8gVXNlIHNjcmlwdCB0YWcgaWYgYXZhaWxhYmxlLlxuICAgIGlmICh0eXBlb2YgZG9jdW1lbnQgIT09ICd1bmRlZmluZWQnICYmIGRvY3VtZW50KSB7XG4gICAgICBjb25zdCBlbCA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCdqdXB5dGVyLWNvbmZpZy1kYXRhJyk7XG5cbiAgICAgIGlmIChlbCkge1xuICAgICAgICBjb25maWdEYXRhID0gSlNPTi5wYXJzZShlbC50ZXh0Q29udGVudCB8fCAnJykgYXMge1xuICAgICAgICAgIFtrZXk6IHN0cmluZ106IHN0cmluZztcbiAgICAgICAgfTtcbiAgICAgICAgZm91bmQgPSB0cnVlO1xuICAgICAgfVxuICAgIH1cbiAgICAvLyBPdGhlcndpc2UgdXNlIENMSSBpZiBnaXZlbi5cbiAgICBpZiAoIWZvdW5kICYmIHR5cGVvZiBwcm9jZXNzICE9PSAndW5kZWZpbmVkJyAmJiBwcm9jZXNzLmFyZ3YpIHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGNvbnN0IGNsaSA9IG1pbmltaXN0KHByb2Nlc3MuYXJndi5zbGljZSgyKSk7XG4gICAgICAgIGNvbnN0IHBhdGg6IGFueSA9IHJlcXVpcmUoJ3BhdGgnKTtcbiAgICAgICAgbGV0IGZ1bGxQYXRoID0gJyc7XG4gICAgICAgIGlmICgnanVweXRlci1jb25maWctZGF0YScgaW4gY2xpKSB7XG4gICAgICAgICAgZnVsbFBhdGggPSBwYXRoLnJlc29sdmUoY2xpWydqdXB5dGVyLWNvbmZpZy1kYXRhJ10pO1xuICAgICAgICB9IGVsc2UgaWYgKCdKVVBZVEVSX0NPTkZJR19EQVRBJyBpbiBwcm9jZXNzLmVudikge1xuICAgICAgICAgIGZ1bGxQYXRoID0gcGF0aC5yZXNvbHZlKHByb2Nlc3MuZW52WydKVVBZVEVSX0NPTkZJR19EQVRBJ10pO1xuICAgICAgICB9XG4gICAgICAgIGlmIChmdWxsUGF0aCkge1xuICAgICAgICAgIC8vIEZvcmNlIFdlYnBhY2sgdG8gaWdub3JlIHRoaXMgcmVxdWlyZS5cbiAgICAgICAgICAvLyBlc2xpbnQtZGlzYWJsZS1uZXh0LWxpbmVcbiAgICAgICAgICBjb25maWdEYXRhID0gZXZhbCgncmVxdWlyZScpKGZ1bGxQYXRoKSBhcyB7IFtrZXk6IHN0cmluZ106IHN0cmluZyB9O1xuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlKSB7XG4gICAgICAgIGNvbnNvbGUuZXJyb3IoZSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgaWYgKCFKU09ORXh0LmlzT2JqZWN0KGNvbmZpZ0RhdGEpKSB7XG4gICAgICBjb25maWdEYXRhID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiAgICB9IGVsc2Uge1xuICAgICAgZm9yIChjb25zdCBrZXkgaW4gY29uZmlnRGF0YSkge1xuICAgICAgICAvLyBQYWdlQ29uZmlnIGV4cGVjdHMgc3RyaW5nc1xuICAgICAgICBpZiAodHlwZW9mIGNvbmZpZ0RhdGFba2V5XSAhPT0gJ3N0cmluZycpIHtcbiAgICAgICAgICBjb25maWdEYXRhW2tleV0gPSBKU09OLnN0cmluZ2lmeShjb25maWdEYXRhW2tleV0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBjb25maWdEYXRhIVtuYW1lXSB8fCBnZXRCb2R5RGF0YShuYW1lKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgZ2xvYmFsIGNvbmZpZ3VyYXRpb24gZGF0YSBmb3IgdGhlIEp1cHl0ZXIgYXBwbGljYXRpb24uXG4gICAqXG4gICAqIEBwYXJhbSBuYW1lIC0gVGhlIG5hbWUgb2YgdGhlIGNvbmZpZ3VyYXRpb24gb3B0aW9uLlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgdG8gc2V0IHRoZSBvcHRpb24gdG8uXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBsYXN0IGNvbmZpZyB2YWx1ZSBvciBhbiBlbXB0eSBzdHJpbmcgaWYgaXQgZG9lc24ndCBleGlzdC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBzZXRPcHRpb24obmFtZTogc3RyaW5nLCB2YWx1ZTogc3RyaW5nKTogc3RyaW5nIHtcbiAgICBjb25zdCBsYXN0ID0gZ2V0T3B0aW9uKG5hbWUpO1xuXG4gICAgY29uZmlnRGF0YSFbbmFtZV0gPSB2YWx1ZTtcbiAgICByZXR1cm4gbGFzdDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGJhc2UgdXJsIGZvciBhIEp1cHl0ZXIgYXBwbGljYXRpb24sIG9yIHRoZSBiYXNlIHVybCBvZiB0aGUgcGFnZS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXRCYXNlVXJsKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIFVSTEV4dC5ub3JtYWxpemUoZ2V0T3B0aW9uKCdiYXNlVXJsJykgfHwgJy8nKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHRyZWUgdXJsIGZvciBhIEp1cHl0ZXJMYWIgYXBwbGljYXRpb24uXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZ2V0VHJlZVVybCgpOiBzdHJpbmcge1xuICAgIHJldHVybiBVUkxFeHQuam9pbihnZXRCYXNlVXJsKCksIGdldE9wdGlvbigndHJlZVVybCcpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGJhc2UgdXJsIGZvciBzaGFyaW5nIGxpbmtzICh1c3VhbGx5IGJhc2VVcmwpXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZ2V0U2hhcmVVcmwoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gVVJMRXh0Lm5vcm1hbGl6ZShnZXRPcHRpb24oJ3NoYXJlVXJsJykgfHwgZ2V0QmFzZVVybCgpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHRyZWUgdXJsIGZvciBzaGFyZWFibGUgbGlua3MuXG4gICAqIFVzdWFsbHkgdGhlIHNhbWUgYXMgdHJlZVVybCxcbiAgICogYnV0IG92ZXJyaWRlYWJsZSBlLmcuIHdoZW4gc2hhcmluZyB3aXRoIEp1cHl0ZXJIdWIuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZ2V0VHJlZVNoYXJlVXJsKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIFVSTEV4dC5ub3JtYWxpemUoVVJMRXh0LmpvaW4oZ2V0U2hhcmVVcmwoKSwgZ2V0T3B0aW9uKCd0cmVlVXJsJykpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgVVJMIGdpdmVuIGFuIG9wdGlvbmFsIG1vZGUgYW5kIHRyZWUgcGF0aC5cbiAgICpcbiAgICogVGhpcyBpcyB1c2VkIHRvIGNyZWF0ZSBVUkxTIHdoZW4gdGhlIG1vZGUgb3IgdHJlZSBwYXRoIGNoYW5nZSBhcyB0aGUgdXNlclxuICAgKiBjaGFuZ2VzIG1vZGUgb3IgdGhlIGN1cnJlbnQgZG9jdW1lbnQgaW4gdGhlIG1haW4gYXJlYS4gSWYgZmllbGRzIGluXG4gICAqIG9wdGlvbnMgYXJlIG9taXR0ZWQsIHRoZSB2YWx1ZSBpbiBQYWdlQ29uZmlnIHdpbGwgYmUgdXNlZC5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBJR2V0VXJsT3B0aW9ucyBmb3IgdGhlIG5ldyBwYXRoLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGdldFVybChvcHRpb25zOiBJR2V0VXJsT3B0aW9ucyk6IHN0cmluZyB7XG4gICAgbGV0IHBhdGggPSBvcHRpb25zLnRvU2hhcmUgPyBnZXRTaGFyZVVybCgpIDogZ2V0QmFzZVVybCgpO1xuICAgIGNvbnN0IG1vZGUgPSBvcHRpb25zLm1vZGUgPz8gZ2V0T3B0aW9uKCdtb2RlJyk7XG4gICAgY29uc3Qgd29ya3NwYWNlID0gb3B0aW9ucy53b3Jrc3BhY2UgPz8gZ2V0T3B0aW9uKCd3b3Jrc3BhY2UnKTtcbiAgICBjb25zdCBsYWJPckRvYyA9IG1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnID8gJ2RvYycgOiAnbGFiJztcbiAgICBwYXRoID0gVVJMRXh0LmpvaW4ocGF0aCwgbGFiT3JEb2MpO1xuICAgIGlmICh3b3Jrc3BhY2UgIT09IGRlZmF1bHRXb3Jrc3BhY2UpIHtcbiAgICAgIHBhdGggPSBVUkxFeHQuam9pbihcbiAgICAgICAgcGF0aCxcbiAgICAgICAgJ3dvcmtzcGFjZXMnLFxuICAgICAgICBlbmNvZGVVUklDb21wb25lbnQoZ2V0T3B0aW9uKCd3b3Jrc3BhY2UnKSA/PyBkZWZhdWx0V29ya3NwYWNlKVxuICAgICAgKTtcbiAgICB9XG4gICAgY29uc3QgdHJlZVBhdGggPSBvcHRpb25zLnRyZWVQYXRoID8/IGdldE9wdGlvbigndHJlZVBhdGgnKTtcbiAgICBpZiAodHJlZVBhdGgpIHtcbiAgICAgIHBhdGggPSBVUkxFeHQuam9pbihwYXRoLCAndHJlZScsIFVSTEV4dC5lbmNvZGVQYXJ0cyh0cmVlUGF0aCkpO1xuICAgIH1cbiAgICByZXR1cm4gcGF0aDtcbiAgfVxuXG4gIGV4cG9ydCBjb25zdCBkZWZhdWx0V29ya3NwYWNlOiBzdHJpbmcgPSAnZGVmYXVsdCc7XG5cbiAgLyoqXG4gICAqIE9wdGlvbnMgZm9yIGdldFVybFxuICAgKi9cblxuICBleHBvcnQgaW50ZXJmYWNlIElHZXRVcmxPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgb3B0aW9uYWwgbW9kZSBhcyBhIHN0cmluZyAnc2luZ2xlLWRvY3VtZW50JyBvciAnbXVsdGlwbGUtZG9jdW1lbnQnLiBJZlxuICAgICAqIHRoZSBtb2RlIGFyZ3VtZW50IGlzIG1pc3NpbmcsIGl0IHdpbGwgYmUgcHJvdmlkZWQgZnJvbSB0aGUgUGFnZUNvbmZpZy5cbiAgICAgKi9cbiAgICBtb2RlPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG9wdGlvbmFsIHdvcmtzcGFjZSBhcyBhIHN0cmluZy4gSWYgdGhpcyBhcmd1bWVudCBpcyBtaXNzaW5nLCB0aGUgdmFsdWUgd2lsbFxuICAgICAqIGJlIHB1bGxlZCBmcm9tIFBhZ2VDb25maWcuIFRvIHVzZSB0aGUgZGVmYXVsdCB3b3Jrc3BhY2UgKG5vIC93b3Jrc3BhY2VzLzxuYW1lPlxuICAgICAqIFVSTCBzZWdtZW50IHdpbGwgYmUgaW5jbHVkZWQpIHBhc3MgdGhlIHN0cmluZyBQYWdlQ29uZmlnLmRlZmF1bHRXb3Jrc3BhY2UuXG4gICAgICovXG4gICAgd29ya3NwYWNlPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgdXJsIGlzIG1lYW50IHRvIGJlIHNoYXJlZCBvciBub3Q7IGRlZmF1bHQgZmFsc2UuXG4gICAgICovXG4gICAgdG9TaGFyZT86IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgb3B0aW9uYWwgdHJlZSBwYXRoIGFzIGFzIHN0cmluZy4gSWYgdHJlZVBhdGggaXMgbm90IHByb3ZpZGVkIGl0IHdpbGwgYmVcbiAgICAgKiBwcm92aWRlZCBmcm9tIHRoZSBQYWdlQ29uZmlnLiBJZiBhbiBlbXB0eSBzdHJpbmcsIHRoZSByZXN1bHRpbmcgcGF0aCB3aWxsIG5vdFxuICAgICAqIGNvbnRhaW4gYSB0cmVlIHBvcnRpb24uXG4gICAgICovXG4gICAgdHJlZVBhdGg/OiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBiYXNlIHdlYnNvY2tldCB1cmwgZm9yIGEgSnVweXRlciBhcHBsaWNhdGlvbiwgb3IgYW4gZW1wdHkgc3RyaW5nLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGdldFdzVXJsKGJhc2VVcmw/OiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIGxldCB3c1VybCA9IGdldE9wdGlvbignd3NVcmwnKTtcbiAgICBpZiAoIXdzVXJsKSB7XG4gICAgICBiYXNlVXJsID0gYmFzZVVybCA/IFVSTEV4dC5ub3JtYWxpemUoYmFzZVVybCkgOiBnZXRCYXNlVXJsKCk7XG4gICAgICBpZiAoYmFzZVVybC5pbmRleE9mKCdodHRwJykgIT09IDApIHtcbiAgICAgICAgcmV0dXJuICcnO1xuICAgICAgfVxuICAgICAgd3NVcmwgPSAnd3MnICsgYmFzZVVybC5zbGljZSg0KTtcbiAgICB9XG4gICAgcmV0dXJuIFVSTEV4dC5ub3JtYWxpemUod3NVcmwpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybnMgdGhlIFVSTCBjb252ZXJ0aW5nIHRoaXMgbm90ZWJvb2sgdG8gYSBjZXJ0YWluXG4gICAqIGZvcm1hdCB3aXRoIG5iY29udmVydC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXROQkNvbnZlcnRVUkwoe1xuICAgIHBhdGgsXG4gICAgZm9ybWF0LFxuICAgIGRvd25sb2FkXG4gIH06IHtcbiAgICBwYXRoOiBzdHJpbmc7XG4gICAgZm9ybWF0OiBzdHJpbmc7XG4gICAgZG93bmxvYWQ6IGJvb2xlYW47XG4gIH0pOiBzdHJpbmcge1xuICAgIGNvbnN0IG5vdGVib29rUGF0aCA9IFVSTEV4dC5lbmNvZGVQYXJ0cyhwYXRoKTtcbiAgICBjb25zdCB1cmwgPSBVUkxFeHQuam9pbihnZXRCYXNlVXJsKCksICduYmNvbnZlcnQnLCBmb3JtYXQsIG5vdGVib29rUGF0aCk7XG4gICAgaWYgKGRvd25sb2FkKSB7XG4gICAgICByZXR1cm4gdXJsICsgJz9kb3dubG9hZD10cnVlJztcbiAgICB9XG4gICAgcmV0dXJuIHVybDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGF1dGhvcml6YXRpb24gdG9rZW4gZm9yIGEgSnVweXRlciBhcHBsaWNhdGlvbi5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXRUb2tlbigpOiBzdHJpbmcge1xuICAgIHJldHVybiBnZXRPcHRpb24oJ3Rva2VuJykgfHwgZ2V0Qm9keURhdGEoJ2p1cHl0ZXJBcGlUb2tlbicpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgTm90ZWJvb2sgdmVyc2lvbiBpbmZvIFttYWpvciwgbWlub3IsIHBhdGNoXS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXROb3RlYm9va1ZlcnNpb24oKTogW251bWJlciwgbnVtYmVyLCBudW1iZXJdIHtcbiAgICBjb25zdCBub3RlYm9va1ZlcnNpb24gPSBnZXRPcHRpb24oJ25vdGVib29rVmVyc2lvbicpO1xuICAgIGlmIChub3RlYm9va1ZlcnNpb24gPT09ICcnKSB7XG4gICAgICByZXR1cm4gWzAsIDAsIDBdO1xuICAgIH1cbiAgICByZXR1cm4gSlNPTi5wYXJzZShub3RlYm9va1ZlcnNpb24pO1xuICB9XG5cbiAgLyoqXG4gICAqIFByaXZhdGUgcGFnZSBjb25maWcgZGF0YSBmb3IgdGhlIEp1cHl0ZXIgYXBwbGljYXRpb24uXG4gICAqL1xuICBsZXQgY29uZmlnRGF0YTogeyBba2V5OiBzdHJpbmddOiBzdHJpbmcgfSB8IG51bGwgPSBudWxsO1xuXG4gIC8qKlxuICAgKiBHZXQgYSB1cmwtZW5jb2RlZCBpdGVtIGZyb20gYGJvZHkuZGF0YWAgYW5kIGRlY29kZSBpdFxuICAgKiBXZSBzaG91bGQgbmV2ZXIgaGF2ZSBhbnkgZW5jb2RlZCBVUkxzIGFueXdoZXJlIGVsc2UgaW4gY29kZVxuICAgKiB1bnRpbCB3ZSBhcmUgYnVpbGRpbmcgYW4gYWN0dWFsIHJlcXVlc3QuXG4gICAqL1xuICBmdW5jdGlvbiBnZXRCb2R5RGF0YShrZXk6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgaWYgKHR5cGVvZiBkb2N1bWVudCA9PT0gJ3VuZGVmaW5lZCcgfHwgIWRvY3VtZW50LmJvZHkpIHtcbiAgICAgIHJldHVybiAnJztcbiAgICB9XG4gICAgY29uc3QgdmFsID0gZG9jdW1lbnQuYm9keS5kYXRhc2V0W2tleV07XG4gICAgaWYgKHR5cGVvZiB2YWwgPT09ICd1bmRlZmluZWQnKSB7XG4gICAgICByZXR1cm4gJyc7XG4gICAgfVxuICAgIHJldHVybiBkZWNvZGVVUklDb21wb25lbnQodmFsKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbmFtZXNwYWNlIGZvciBwYWdlIGNvbmZpZyBgRXh0ZW5zaW9uYCBmdW5jdGlvbnMuXG4gICAqL1xuICBleHBvcnQgbmFtZXNwYWNlIEV4dGVuc2lvbiB7XG4gICAgLyoqXG4gICAgICogUG9wdWxhdGUgYW4gYXJyYXkgZnJvbSBwYWdlIGNvbmZpZy5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBrZXkgLSBUaGUgcGFnZSBjb25maWcga2V5IChlLmcuLCBgZGVmZXJyZWRFeHRlbnNpb25zYCkuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyBpcyBpbnRlbmRlZCBmb3IgYGRlZmVycmVkRXh0ZW5zaW9uc2AgYW5kIGBkaXNhYmxlZEV4dGVuc2lvbnNgLlxuICAgICAqL1xuICAgIGZ1bmN0aW9uIHBvcHVsYXRlKGtleTogc3RyaW5nKTogc3RyaW5nW10ge1xuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3QgcmF3ID0gZ2V0T3B0aW9uKGtleSk7XG4gICAgICAgIGlmIChyYXcpIHtcbiAgICAgICAgICByZXR1cm4gSlNPTi5wYXJzZShyYXcpO1xuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICBjb25zb2xlLndhcm4oYFVuYWJsZSB0byBwYXJzZSAke2tleX0uYCwgZXJyb3IpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFtdO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBjb2xsZWN0aW9uIG9mIGRlZmVycmVkIGV4dGVuc2lvbnMgaW4gcGFnZSBjb25maWcuXG4gICAgICovXG4gICAgZXhwb3J0IGNvbnN0IGRlZmVycmVkID0gcG9wdWxhdGUoJ2RlZmVycmVkRXh0ZW5zaW9ucycpO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbGxlY3Rpb24gb2YgZGlzYWJsZWQgZXh0ZW5zaW9ucyBpbiBwYWdlIGNvbmZpZy5cbiAgICAgKi9cbiAgICBleHBvcnQgY29uc3QgZGlzYWJsZWQgPSBwb3B1bGF0ZSgnZGlzYWJsZWRFeHRlbnNpb25zJyk7XG5cbiAgICAvKipcbiAgICAgKiBSZXR1cm5zIHdoZXRoZXIgYSBwbHVnaW4gaXMgZGVmZXJyZWQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gaWQgLSBUaGUgcGx1Z2luIElELlxuICAgICAqL1xuICAgIGV4cG9ydCBmdW5jdGlvbiBpc0RlZmVycmVkKGlkOiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICAgIC8vIENoZWNrIGZvciBlaXRoZXIgYSBmdWxsIHBsdWdpbiBpZCBtYXRjaCBvciBhbiBleHRlbnNpb25cbiAgICAgIC8vIG5hbWUgbWF0Y2guXG4gICAgICBjb25zdCBzZXBhcmF0b3JJbmRleCA9IGlkLmluZGV4T2YoJzonKTtcbiAgICAgIGxldCBleHROYW1lID0gJyc7XG4gICAgICBpZiAoc2VwYXJhdG9ySW5kZXggIT09IC0xKSB7XG4gICAgICAgIGV4dE5hbWUgPSBpZC5zbGljZSgwLCBzZXBhcmF0b3JJbmRleCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gZGVmZXJyZWQuc29tZSh2YWwgPT4gdmFsID09PSBpZCB8fCAoZXh0TmFtZSAmJiB2YWwgPT09IGV4dE5hbWUpKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZXR1cm5zIHdoZXRoZXIgYSBwbHVnaW4gaXMgZGlzYWJsZWQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gaWQgLSBUaGUgcGx1Z2luIElELlxuICAgICAqL1xuICAgIGV4cG9ydCBmdW5jdGlvbiBpc0Rpc2FibGVkKGlkOiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICAgIC8vIENoZWNrIGZvciBlaXRoZXIgYSBmdWxsIHBsdWdpbiBpZCBtYXRjaCBvciBhbiBleHRlbnNpb25cbiAgICAgIC8vIG5hbWUgbWF0Y2guXG4gICAgICBjb25zdCBzZXBhcmF0b3JJbmRleCA9IGlkLmluZGV4T2YoJzonKTtcbiAgICAgIGxldCBleHROYW1lID0gJyc7XG4gICAgICBpZiAoc2VwYXJhdG9ySW5kZXggIT09IC0xKSB7XG4gICAgICAgIGV4dE5hbWUgPSBpZC5zbGljZSgwLCBzZXBhcmF0b3JJbmRleCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gZGlzYWJsZWQuc29tZSh2YWwgPT4gdmFsID09PSBpZCB8fCAoZXh0TmFtZSAmJiB2YWwgPT09IGV4dE5hbWUpKTtcbiAgICB9XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgcG9zaXggfSBmcm9tICdwYXRoJztcblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBwYXRoLXJlbGF0ZWQgZnVuY3Rpb25zLlxuICpcbiAqIE5vdGUgdGhhdCBKdXB5dGVyIHNlcnZlciBwYXRocyBkbyBub3Qgc3RhcnQgd2l0aCBhIGxlYWRpbmcgc2xhc2guXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgUGF0aEV4dCB7XG4gIC8qKlxuICAgKiBKb2luIGFsbCBhcmd1bWVudHMgdG9nZXRoZXIgYW5kIG5vcm1hbGl6ZSB0aGUgcmVzdWx0aW5nIHBhdGguXG4gICAqIEFyZ3VtZW50cyBtdXN0IGJlIHN0cmluZ3MuIEluIHYwLjgsIG5vbi1zdHJpbmcgYXJndW1lbnRzIHdlcmUgc2lsZW50bHkgaWdub3JlZC4gSW4gdjAuMTAgYW5kIHVwLCBhbiBleGNlcHRpb24gaXMgdGhyb3duLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aHMgLSBUaGUgc3RyaW5nIHBhdGhzIHRvIGpvaW4uXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gam9pbiguLi5wYXRoczogc3RyaW5nW10pOiBzdHJpbmcge1xuICAgIGNvbnN0IHBhdGggPSBwb3NpeC5qb2luKC4uLnBhdGhzKTtcbiAgICByZXR1cm4gcGF0aCA9PT0gJy4nID8gJycgOiByZW1vdmVTbGFzaChwYXRoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm4gdGhlIGxhc3QgcG9ydGlvbiBvZiBhIHBhdGguIFNpbWlsYXIgdG8gdGhlIFVuaXggYmFzZW5hbWUgY29tbWFuZC5cbiAgICogT2Z0ZW4gdXNlZCB0byBleHRyYWN0IHRoZSBmaWxlIG5hbWUgZnJvbSBhIGZ1bGx5IHF1YWxpZmllZCBwYXRoLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aCAtIFRoZSBwYXRoIHRvIGV2YWx1YXRlLlxuICAgKlxuICAgKiBAcGFyYW0gZXh0IC0gQW4gZXh0ZW5zaW9uIHRvIHJlbW92ZSBmcm9tIHRoZSByZXN1bHQuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYmFzZW5hbWUocGF0aDogc3RyaW5nLCBleHQ/OiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIHJldHVybiBwb3NpeC5iYXNlbmFtZShwYXRoLCBleHQpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgZGlyZWN0b3J5IG5hbWUgb2YgYSBwYXRoLCBzaW1pbGFyIHRvIHRoZSBVbml4IGRpcm5hbWUgY29tbWFuZC5cbiAgICogV2hlbiBhbiBlbXB0eSBwYXRoIGlzIGdpdmVuLCByZXR1cm5zIHRoZSByb290IHBhdGguXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoIC0gVGhlIGZpbGUgcGF0aC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBkaXJuYW1lKHBhdGg6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgY29uc3QgZGlyID0gcmVtb3ZlU2xhc2gocG9zaXguZGlybmFtZShwYXRoKSk7XG4gICAgcmV0dXJuIGRpciA9PT0gJy4nID8gJycgOiBkaXI7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBleHRlbnNpb24gb2YgdGhlIHBhdGguXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoIC0gVGhlIGZpbGUgcGF0aC5cbiAgICpcbiAgICogQHJldHVybnMgdGhlIGV4dGVuc2lvbiBvZiB0aGUgZmlsZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgZXh0ZW5zaW9uIGlzIHRoZSBzdHJpbmcgZnJvbSB0aGUgbGFzdCBvY2N1cnJlbmNlIG9mIHRoZSBgLmBcbiAgICogY2hhcmFjdGVyIHRvIGVuZCBvZiBzdHJpbmcgaW4gdGhlIGxhc3QgcG9ydGlvbiBvZiB0aGUgcGF0aCwgaW5jbHVzaXZlLlxuICAgKiBJZiB0aGVyZSBpcyBubyBgLmAgaW4gdGhlIGxhc3QgcG9ydGlvbiBvZiB0aGUgcGF0aCwgb3IgaWYgdGhlIGZpcnN0XG4gICAqIGNoYXJhY3RlciBvZiB0aGUgYmFzZW5hbWUgb2YgcGF0aCBbW2Jhc2VuYW1lXV0gaXMgYC5gLCB0aGVuIGFuXG4gICAqIGVtcHR5IHN0cmluZyBpcyByZXR1cm5lZC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBleHRuYW1lKHBhdGg6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHBvc2l4LmV4dG5hbWUocGF0aCk7XG4gIH1cblxuICAvKipcbiAgICogTm9ybWFsaXplIGEgc3RyaW5nIHBhdGgsIHJlZHVjaW5nICcuLicgYW5kICcuJyBwYXJ0cy5cbiAgICogV2hlbiBtdWx0aXBsZSBzbGFzaGVzIGFyZSBmb3VuZCwgdGhleSdyZSByZXBsYWNlZCBieSBhIHNpbmdsZSBvbmU7IHdoZW4gdGhlIHBhdGggY29udGFpbnMgYSB0cmFpbGluZyBzbGFzaCwgaXQgaXMgcHJlc2VydmVkLiBPbiBXaW5kb3dzIGJhY2tzbGFzaGVzIGFyZSB1c2VkLlxuICAgKiBXaGVuIGFuIGVtcHR5IHBhdGggaXMgZ2l2ZW4sIHJldHVybnMgdGhlIHJvb3QgcGF0aC5cbiAgICpcbiAgICogQHBhcmFtIHBhdGggLSBUaGUgc3RyaW5nIHBhdGggdG8gbm9ybWFsaXplLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIG5vcm1hbGl6ZShwYXRoOiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIGlmIChwYXRoID09PSAnJykge1xuICAgICAgcmV0dXJuICcnO1xuICAgIH1cbiAgICByZXR1cm4gcmVtb3ZlU2xhc2gocG9zaXgubm9ybWFsaXplKHBhdGgpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXNvbHZlIGEgc2VxdWVuY2Ugb2YgcGF0aHMgb3IgcGF0aCBzZWdtZW50cyBpbnRvIGFuIGFic29sdXRlIHBhdGguXG4gICAqIFRoZSByb290IHBhdGggaW4gdGhlIGFwcGxpY2F0aW9uIGhhcyBubyBsZWFkaW5nIHNsYXNoLCBzbyBpdCBpcyByZW1vdmVkLlxuICAgKlxuICAgKiBAcGFyYW0gcGFydHMgLSBUaGUgcGF0aHMgdG8gam9pbi5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgcmlnaHQtbW9zdCBwYXJhbWV0ZXIgaXMgY29uc2lkZXJlZCBcXHt0b1xcfS4gIE90aGVyIHBhcmFtZXRlcnMgYXJlIGNvbnNpZGVyZWQgYW4gYXJyYXkgb2YgXFx7ZnJvbVxcfS5cbiAgICpcbiAgICogU3RhcnRpbmcgZnJvbSBsZWZ0bW9zdCBcXHtmcm9tXFx9IHBhcmFtZXRlciwgcmVzb2x2ZXMgXFx7dG9cXH0gdG8gYW4gYWJzb2x1dGUgcGF0aC5cbiAgICpcbiAgICogSWYgXFx7dG9cXH0gaXNuJ3QgYWxyZWFkeSBhYnNvbHV0ZSwgXFx7ZnJvbVxcfSBhcmd1bWVudHMgYXJlIHByZXBlbmRlZCBpbiByaWdodCB0byBsZWZ0IG9yZGVyLCB1bnRpbCBhbiBhYnNvbHV0ZSBwYXRoIGlzIGZvdW5kLiBJZiBhZnRlciB1c2luZyBhbGwgXFx7ZnJvbVxcfSBwYXRocyBzdGlsbCBubyBhYnNvbHV0ZSBwYXRoIGlzIGZvdW5kLCB0aGUgY3VycmVudCB3b3JraW5nIGRpcmVjdG9yeSBpcyB1c2VkIGFzIHdlbGwuIFRoZSByZXN1bHRpbmcgcGF0aCBpcyBub3JtYWxpemVkLCBhbmQgdHJhaWxpbmcgc2xhc2hlcyBhcmUgcmVtb3ZlZCB1bmxlc3MgdGhlIHBhdGggZ2V0cyByZXNvbHZlZCB0byB0aGUgcm9vdCBkaXJlY3RvcnkuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVzb2x2ZSguLi5wYXJ0czogc3RyaW5nW10pOiBzdHJpbmcge1xuICAgIHJldHVybiByZW1vdmVTbGFzaChwb3NpeC5yZXNvbHZlKC4uLnBhcnRzKSk7XG4gIH1cblxuICAvKipcbiAgICogU29sdmUgdGhlIHJlbGF0aXZlIHBhdGggZnJvbSBcXHtmcm9tXFx9IHRvIFxce3RvXFx9LlxuICAgKlxuICAgKiBAcGFyYW0gZnJvbSAtIFRoZSBzb3VyY2UgcGF0aC5cbiAgICpcbiAgICogQHBhcmFtIHRvIC0gVGhlIHRhcmdldCBwYXRoLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIElmIGZyb20gYW5kIHRvIGVhY2ggcmVzb2x2ZSB0byB0aGUgc2FtZSBwYXRoIChhZnRlciBjYWxsaW5nXG4gICAqIHBhdGgucmVzb2x2ZSgpIG9uIGVhY2gpLCBhIHplcm8tbGVuZ3RoIHN0cmluZyBpcyByZXR1cm5lZC5cbiAgICogSWYgYSB6ZXJvLWxlbmd0aCBzdHJpbmcgaXMgcGFzc2VkIGFzIGZyb20gb3IgdG8sIGAvYFxuICAgKiB3aWxsIGJlIHVzZWQgaW5zdGVhZCBvZiB0aGUgemVyby1sZW5ndGggc3RyaW5ncy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiByZWxhdGl2ZShmcm9tOiBzdHJpbmcsIHRvOiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIHJldHVybiByZW1vdmVTbGFzaChwb3NpeC5yZWxhdGl2ZShmcm9tLCB0bykpO1xuICB9XG5cbiAgLyoqXG4gICAqIE5vcm1hbGl6ZSBhIGZpbGUgZXh0ZW5zaW9uIHRvIGJlIG9mIHRoZSB0eXBlIGAnLmZvbydgLlxuICAgKlxuICAgKiBAcGFyYW0gZXh0ZW5zaW9uIC0gdGhlIGZpbGUgZXh0ZW5zaW9uLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIEFkZHMgYSBsZWFkaW5nIGRvdCBpZiBub3QgcHJlc2VudCBhbmQgY29udmVydHMgdG8gbG93ZXIgY2FzZS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBub3JtYWxpemVFeHRlbnNpb24oZXh0ZW5zaW9uOiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIGlmIChleHRlbnNpb24ubGVuZ3RoID4gMCAmJiBleHRlbnNpb24uaW5kZXhPZignLicpICE9PSAwKSB7XG4gICAgICBleHRlbnNpb24gPSBgLiR7ZXh0ZW5zaW9ufWA7XG4gICAgfVxuICAgIHJldHVybiBleHRlbnNpb247XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIHRoZSBsZWFkaW5nIHNsYXNoIGZyb20gYSBwYXRoLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZnJvbSB3aGljaCB0byByZW1vdmUgYSBsZWFkaW5nIHNsYXNoLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHJlbW92ZVNsYXNoKHBhdGg6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgaWYgKHBhdGguaW5kZXhPZignLycpID09PSAwKSB7XG4gICAgICBwYXRoID0gcGF0aC5zbGljZSgxKTtcbiAgICB9XG4gICAgcmV0dXJuIHBhdGg7XG4gIH1cbn1cbiIsIi8qXG4gKiBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbiAqIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4gKi9cblxuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSVNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcblxuLyoqXG4gKiBDb252ZXJ0IGEgc2lnbmFsIGludG8gYSBwcm9taXNlIGZvciB0aGUgZmlyc3QgZW1pdHRlZCB2YWx1ZS5cbiAqXG4gKiBAcGFyYW0gc2lnbmFsIC0gVGhlIHNpZ25hbCB3ZSBhcmUgbGlzdGVuaW5nIHRvLlxuICogQHBhcmFtIHRpbWVvdXQgLSBUaW1lb3V0IHRvIHdhaXQgZm9yIHNpZ25hbCBpbiBtcyAobm90IHRpbWVvdXQgaWYgbm90IGRlZmluZWQgb3IgMClcbiAqXG4gKiBAcmV0dXJucyBhIFByb21pc2UgdGhhdCByZXNvbHZlcyB3aXRoIGEgYChzZW5kZXIsIGFyZ3MpYCBwYWlyLlxuICovXG5leHBvcnQgZnVuY3Rpb24gc2lnbmFsVG9Qcm9taXNlPFQsIFU+KFxuICBzaWduYWw6IElTaWduYWw8VCwgVT4sXG4gIHRpbWVvdXQ/OiBudW1iZXJcbik6IFByb21pc2U8W1QsIFVdPiB7XG4gIGNvbnN0IHdhaXRGb3JTaWduYWwgPSBuZXcgUHJvbWlzZURlbGVnYXRlPFtULCBVXT4oKTtcblxuICBmdW5jdGlvbiBjbGVhbnVwKCkge1xuICAgIHNpZ25hbC5kaXNjb25uZWN0KHNsb3QpO1xuICB9XG5cbiAgZnVuY3Rpb24gc2xvdChzZW5kZXI6IFQsIGFyZ3M6IFUpIHtcbiAgICBjbGVhbnVwKCk7XG4gICAgd2FpdEZvclNpZ25hbC5yZXNvbHZlKFtzZW5kZXIsIGFyZ3NdKTtcbiAgfVxuICBzaWduYWwuY29ubmVjdChzbG90KTtcblxuICBpZiAoKHRpbWVvdXQgPz8gMCkgPiAwKSB7XG4gICAgc2V0VGltZW91dCgoKSA9PiB7XG4gICAgICBjbGVhbnVwKCk7XG4gICAgICB3YWl0Rm9yU2lnbmFsLnJlamVjdChgU2lnbmFsIG5vdCBlbWl0dGVkIHdpdGhpbiAke3RpbWVvdXR9IG1zLmApO1xuICAgIH0sIHRpbWVvdXQpO1xuICB9XG4gIHJldHVybiB3YWl0Rm9yU2lnbmFsLnByb21pc2U7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgdGV4dC1yZWxhdGVkIGZ1bmN0aW9ucy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBUZXh0IHtcbiAgLy8gamF2YXNjcmlwdCBzdG9yZXMgdGV4dCBhcyB1dGYxNiBhbmQgc3RyaW5nIGluZGljZXMgdXNlIFwiY29kZSB1bml0c1wiLFxuICAvLyB3aGljaCBzdG9yZXMgaGlnaC1jb2RlcG9pbnQgY2hhcmFjdGVycyBhcyBcInN1cnJvZ2F0ZSBwYWlyc1wiLFxuICAvLyB3aGljaCBvY2N1cHkgdHdvIGluZGljZXMgaW4gdGhlIGphdmFzY3JpcHQgc3RyaW5nLlxuICAvLyBXZSBuZWVkIHRvIHRyYW5zbGF0ZSBjdXJzb3JfcG9zIGluIHRoZSBKdXB5dGVyIHByb3RvY29sIChpbiBjaGFyYWN0ZXJzKVxuICAvLyB0byBqcyBvZmZzZXQgKHdpdGggc3Vycm9nYXRlIHBhaXJzIHRha2luZyB0d28gc3BvdHMpLlxuXG4gIGNvbnN0IEhBU19TVVJST0dBVEVTOiBib29sZWFuID0gJ/CdkJonLmxlbmd0aCA+IDE7XG5cbiAgLyoqXG4gICAqIENvbnZlcnQgYSBqYXZhc2NyaXB0IHN0cmluZyBpbmRleCBpbnRvIGEgdW5pY29kZSBjaGFyYWN0ZXIgb2Zmc2V0XG4gICAqXG4gICAqIEBwYXJhbSBqc0lkeCAtIFRoZSBqYXZhc2NyaXB0IHN0cmluZyBpbmRleCAoY291bnRpbmcgc3Vycm9nYXRlIHBhaXJzKVxuICAgKlxuICAgKiBAcGFyYW0gdGV4dCAtIFRoZSB0ZXh0IGluIHdoaWNoIHRoZSBvZmZzZXQgaXMgY2FsY3VsYXRlZFxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgdW5pY29kZSBjaGFyYWN0ZXIgb2Zmc2V0XG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24ganNJbmRleFRvQ2hhckluZGV4KGpzSWR4OiBudW1iZXIsIHRleHQ6IHN0cmluZyk6IG51bWJlciB7XG4gICAgaWYgKEhBU19TVVJST0dBVEVTKSB7XG4gICAgICAvLyBub3QgdXNpbmcgc3Vycm9nYXRlcywgbm90aGluZyB0byBkb1xuICAgICAgcmV0dXJuIGpzSWR4O1xuICAgIH1cbiAgICBsZXQgY2hhcklkeCA9IGpzSWR4O1xuICAgIGZvciAobGV0IGkgPSAwOyBpICsgMSA8IHRleHQubGVuZ3RoICYmIGkgPCBqc0lkeDsgaSsrKSB7XG4gICAgICBjb25zdCBjaGFyQ29kZSA9IHRleHQuY2hhckNvZGVBdChpKTtcbiAgICAgIC8vIGNoZWNrIGZvciBzdXJyb2dhdGUgcGFpclxuICAgICAgaWYgKGNoYXJDb2RlID49IDB4ZDgwMCAmJiBjaGFyQ29kZSA8PSAweGRiZmYpIHtcbiAgICAgICAgY29uc3QgbmV4dENoYXJDb2RlID0gdGV4dC5jaGFyQ29kZUF0KGkgKyAxKTtcbiAgICAgICAgaWYgKG5leHRDaGFyQ29kZSA+PSAweGRjMDAgJiYgbmV4dENoYXJDb2RlIDw9IDB4ZGZmZikge1xuICAgICAgICAgIGNoYXJJZHgtLTtcbiAgICAgICAgICBpKys7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGNoYXJJZHg7XG4gIH1cblxuICAvKipcbiAgICogQ29udmVydCBhIHVuaWNvZGUgY2hhcmFjdGVyIG9mZnNldCB0byBhIGphdmFzY3JpcHQgc3RyaW5nIGluZGV4LlxuICAgKlxuICAgKiBAcGFyYW0gY2hhcklkeCAtIFRoZSBpbmRleCBpbiB1bmljb2RlIGNoYXJhY3RlcnNcbiAgICpcbiAgICogQHBhcmFtIHRleHQgLSBUaGUgdGV4dCBpbiB3aGljaCB0aGUgb2Zmc2V0IGlzIGNhbGN1bGF0ZWRcbiAgICpcbiAgICogQHJldHVybnMgVGhlIGpzLW5hdGl2ZSBpbmRleFxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNoYXJJbmRleFRvSnNJbmRleChjaGFySWR4OiBudW1iZXIsIHRleHQ6IHN0cmluZyk6IG51bWJlciB7XG4gICAgaWYgKEhBU19TVVJST0dBVEVTKSB7XG4gICAgICAvLyBub3QgdXNpbmcgc3Vycm9nYXRlcywgbm90aGluZyB0byBkb1xuICAgICAgcmV0dXJuIGNoYXJJZHg7XG4gICAgfVxuICAgIGxldCBqc0lkeCA9IGNoYXJJZHg7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgKyAxIDwgdGV4dC5sZW5ndGggJiYgaSA8IGpzSWR4OyBpKyspIHtcbiAgICAgIGNvbnN0IGNoYXJDb2RlID0gdGV4dC5jaGFyQ29kZUF0KGkpO1xuICAgICAgLy8gY2hlY2sgZm9yIHN1cnJvZ2F0ZSBwYWlyXG4gICAgICBpZiAoY2hhckNvZGUgPj0gMHhkODAwICYmIGNoYXJDb2RlIDw9IDB4ZGJmZikge1xuICAgICAgICBjb25zdCBuZXh0Q2hhckNvZGUgPSB0ZXh0LmNoYXJDb2RlQXQoaSArIDEpO1xuICAgICAgICBpZiAobmV4dENoYXJDb2RlID49IDB4ZGMwMCAmJiBuZXh0Q2hhckNvZGUgPD0gMHhkZmZmKSB7XG4gICAgICAgICAganNJZHgrKztcbiAgICAgICAgICBpKys7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIGpzSWR4O1xuICB9XG5cbiAgLyoqXG4gICAqIEdpdmVuIGEgJ3NuYWtlLWNhc2UnLCAnc25ha2VfY2FzZScsICdzbmFrZTpjYXNlJywgb3JcbiAgICogJ3NuYWtlIGNhc2UnIHN0cmluZywgd2lsbCByZXR1cm4gdGhlIGNhbWVsIGNhc2UgdmVyc2lvbjogJ3NuYWtlQ2FzZScuXG4gICAqXG4gICAqIEBwYXJhbSBzdHI6IHRoZSBzbmFrZS1jYXNlIGlucHV0IHN0cmluZy5cbiAgICpcbiAgICogQHBhcmFtIHVwcGVyOiBkZWZhdWx0ID0gZmFsc2UuIElmIHRydWUsIHRoZSBmaXJzdCBsZXR0ZXIgb2YgdGhlXG4gICAqIHJldHVybmVkIHN0cmluZyB3aWxsIGJlIGNhcGl0YWxpemVkLlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgY2FtZWwgY2FzZSB2ZXJzaW9uIG9mIHRoZSBpbnB1dCBzdHJpbmcuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gY2FtZWxDYXNlKHN0cjogc3RyaW5nLCB1cHBlcjogYm9vbGVhbiA9IGZhbHNlKTogc3RyaW5nIHtcbiAgICByZXR1cm4gc3RyLnJlcGxhY2UoL14oXFx3KXxbXFxzLV86XSsoXFx3KS9nLCBmdW5jdGlvbiAobWF0Y2gsIHAxLCBwMikge1xuICAgICAgaWYgKHAyKSB7XG4gICAgICAgIHJldHVybiBwMi50b1VwcGVyQ2FzZSgpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcmV0dXJuIHVwcGVyID8gcDEudG9VcHBlckNhc2UoKSA6IHAxLnRvTG93ZXJDYXNlKCk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogR2l2ZW4gYSBzdHJpbmcsIHRpdGxlIGNhc2UgdGhlIHdvcmRzIGluIHRoZSBzdHJpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBzdHI6IHRoZSBzdHJpbmcgdG8gdGl0bGUgY2FzZS5cbiAgICpcbiAgICogQHJldHVybnMgdGhlIHNhbWUgc3RyaW5nLCBidXQgd2l0aCBlYWNoIHdvcmQgY2FwaXRhbGl6ZWQuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gdGl0bGVDYXNlKHN0cjogc3RyaW5nKTogc3RyaW5nIHtcbiAgICByZXR1cm4gKHN0ciB8fCAnJylcbiAgICAgIC50b0xvd2VyQ2FzZSgpXG4gICAgICAuc3BsaXQoJyAnKVxuICAgICAgLm1hcCh3b3JkID0+IHdvcmQuY2hhckF0KDApLnRvVXBwZXJDYXNlKCkgKyB3b3JkLnNsaWNlKDEpKVxuICAgICAgLmpvaW4oJyAnKTtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG4vKipcbiAqIEEgbGlzdCBvZiB0aW1lIHVuaXRzIHdpdGggdGhlaXIgYXNzb2NpYXRlZCB2YWx1ZSBpbiBtaWxsaXNlY29uZHMuXG4gKi9cbmNvbnN0IFVOSVRTOiB7IG5hbWU6IEludGwuUmVsYXRpdmVUaW1lRm9ybWF0VW5pdDsgbWlsbGlzZWNvbmRzOiBudW1iZXIgfVtdID0gW1xuICB7IG5hbWU6ICd5ZWFycycsIG1pbGxpc2Vjb25kczogMzY1ICogMjQgKiA2MCAqIDYwICogMTAwMCB9LFxuICB7IG5hbWU6ICdtb250aHMnLCBtaWxsaXNlY29uZHM6IDMwICogMjQgKiA2MCAqIDYwICogMTAwMCB9LFxuICB7IG5hbWU6ICdkYXlzJywgbWlsbGlzZWNvbmRzOiAyNCAqIDYwICogNjAgKiAxMDAwIH0sXG4gIHsgbmFtZTogJ2hvdXJzJywgbWlsbGlzZWNvbmRzOiA2MCAqIDYwICogMTAwMCB9LFxuICB7IG5hbWU6ICdtaW51dGVzJywgbWlsbGlzZWNvbmRzOiA2MCAqIDEwMDAgfSxcbiAgeyBuYW1lOiAnc2Vjb25kcycsIG1pbGxpc2Vjb25kczogMTAwMCB9XG5dO1xuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGRhdGUgZnVuY3Rpb25zLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFRpbWUge1xuICAvKipcbiAgICogQ29udmVydCBhIHRpbWVzdHJpbmcgdG8gYSBodW1hbiByZWFkYWJsZSBzdHJpbmcgKGUuZy4gJ3R3byBtaW51dGVzIGFnbycpLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgZGF0ZSB0aW1lc3RyaW5nIG9yIGRhdGUgb2JqZWN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGZvcm1hdHRlZCBkYXRlLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGZvcm1hdEh1bWFuKHZhbHVlOiBzdHJpbmcgfCBEYXRlKTogc3RyaW5nIHtcbiAgICBjb25zdCBsYW5nID0gZG9jdW1lbnQuZG9jdW1lbnRFbGVtZW50LmxhbmcgfHwgJ2VuJztcbiAgICBjb25zdCBmb3JtYXR0ZXIgPSBuZXcgSW50bC5SZWxhdGl2ZVRpbWVGb3JtYXQobGFuZywgeyBudW1lcmljOiAnYXV0bycgfSk7XG4gICAgY29uc3QgZGVsdGEgPSBuZXcgRGF0ZSh2YWx1ZSkuZ2V0VGltZSgpIC0gRGF0ZS5ub3coKTtcbiAgICBmb3IgKGxldCB1bml0IG9mIFVOSVRTKSB7XG4gICAgICBjb25zdCBhbW91bnQgPSBNYXRoLmNlaWwoZGVsdGEgLyB1bml0Lm1pbGxpc2Vjb25kcyk7XG4gICAgICBpZiAoYW1vdW50ID09PSAwKSB7XG4gICAgICAgIGNvbnRpbnVlO1xuICAgICAgfVxuICAgICAgcmV0dXJuIGZvcm1hdHRlci5mb3JtYXQoYW1vdW50LCB1bml0Lm5hbWUpO1xuICAgIH1cbiAgICByZXR1cm4gZm9ybWF0dGVyLmZvcm1hdCgwLCAnc2Vjb25kcycpO1xuICB9XG5cbiAgLyoqXG4gICAqIENvbnZlbmllbnQgaGVscGVyIHRvIGNvbnZlcnQgYSB0aW1lc3RyaW5nIHRvIGEgZGF0ZSBmb3JtYXQuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSBkYXRlIHRpbWVzdHJpbmcgb3IgZGF0ZSBvYmplY3QuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgZm9ybWF0dGVkIGRhdGUuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZm9ybWF0KHZhbHVlOiBzdHJpbmcgfCBEYXRlKTogc3RyaW5nIHtcbiAgICBjb25zdCBsYW5nID0gZG9jdW1lbnQuZG9jdW1lbnRFbGVtZW50LmxhbmcgfHwgJ2VuJztcbiAgICBjb25zdCBmb3JtYXR0ZXIgPSBuZXcgSW50bC5EYXRlVGltZUZvcm1hdChsYW5nLCB7XG4gICAgICBkYXRlU3R5bGU6ICdzaG9ydCcsXG4gICAgICB0aW1lU3R5bGU6ICdzaG9ydCdcbiAgICB9KTtcbiAgICByZXR1cm4gZm9ybWF0dGVyLmZvcm1hdChuZXcgRGF0ZSh2YWx1ZSkpO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFBhcnRpYWxKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgcG9zaXggfSBmcm9tICdwYXRoJztcbmltcG9ydCB1cmxwYXJzZSBmcm9tICd1cmwtcGFyc2UnO1xuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIFVSTC1yZWxhdGVkIGZ1bmN0aW9ucy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBVUkxFeHQge1xuICAvKipcbiAgICogUGFyc2UgYSB1cmwgaW50byBhIFVSTCBvYmplY3QuXG4gICAqXG4gICAqIEBwYXJhbSB1cmxTdHJpbmcgLSBUaGUgVVJMIHN0cmluZyB0byBwYXJzZS5cbiAgICpcbiAgICogQHJldHVybnMgQSBVUkwgb2JqZWN0LlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHBhcnNlKHVybDogc3RyaW5nKTogSVVybCB7XG4gICAgaWYgKHR5cGVvZiBkb2N1bWVudCAhPT0gJ3VuZGVmaW5lZCcgJiYgZG9jdW1lbnQpIHtcbiAgICAgIGNvbnN0IGEgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdhJyk7XG4gICAgICBhLmhyZWYgPSB1cmw7XG4gICAgICByZXR1cm4gYTtcbiAgICB9XG4gICAgcmV0dXJuIHVybHBhcnNlKHVybCk7XG4gIH1cblxuICAvKipcbiAgICogUGFyc2UgVVJMIGFuZCByZXRyaWV2ZSBob3N0bmFtZVxuICAgKlxuICAgKiBAcGFyYW0gdXJsIC0gVGhlIFVSTCBzdHJpbmcgdG8gcGFyc2VcbiAgICpcbiAgICogQHJldHVybnMgYSBob3N0bmFtZSBzdHJpbmcgdmFsdWVcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXRIb3N0TmFtZSh1cmw6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHVybHBhcnNlKHVybCkuaG9zdG5hbWU7XG4gIH1cbiAgLyoqXG4gICAqIE5vcm1hbGl6ZSBhIHVybC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBub3JtYWxpemUodXJsOiBzdHJpbmcpOiBzdHJpbmc7XG4gIGV4cG9ydCBmdW5jdGlvbiBub3JtYWxpemUodXJsOiB1bmRlZmluZWQpOiB1bmRlZmluZWQ7XG4gIGV4cG9ydCBmdW5jdGlvbiBub3JtYWxpemUodXJsOiBzdHJpbmcgfCB1bmRlZmluZWQpOiBzdHJpbmcgfCB1bmRlZmluZWQ7XG4gIGV4cG9ydCBmdW5jdGlvbiBub3JtYWxpemUodXJsOiBzdHJpbmcgfCB1bmRlZmluZWQpOiBzdHJpbmcgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiB1cmwgJiYgcGFyc2UodXJsKS50b1N0cmluZygpO1xuICB9XG5cbiAgLyoqXG4gICAqIEpvaW4gYSBzZXF1ZW5jZSBvZiB1cmwgY29tcG9uZW50cyBhbmQgbm9ybWFsaXplcyBhcyBpbiBub2RlIGBwYXRoLmpvaW5gLlxuICAgKlxuICAgKiBAcGFyYW0gcGFydHMgLSBUaGUgdXJsIGNvbXBvbmVudHMuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBqb2luZWQgdXJsLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGpvaW4oLi4ucGFydHM6IHN0cmluZ1tdKTogc3RyaW5nIHtcbiAgICBsZXQgdSA9IHVybHBhcnNlKHBhcnRzWzBdLCB7fSk7XG4gICAgLy8gU2NoZW1hLWxlc3MgVVJMIGNhbiBiZSBvbmx5IHBhcnNlZCBhcyByZWxhdGl2ZSB0byBhIGJhc2UgVVJMXG4gICAgLy8gc2VlIGh0dHBzOi8vZ2l0aHViLmNvbS91bnNoaWZ0aW8vdXJsLXBhcnNlL2lzc3Vlcy8yMTkjaXNzdWVjb21tZW50LTEwMDIyMTkzMjZcbiAgICBjb25zdCBpc1NjaGVtYUxlc3MgPSB1LnByb3RvY29sID09PSAnJyAmJiB1LnNsYXNoZXM7XG4gICAgaWYgKGlzU2NoZW1hTGVzcykge1xuICAgICAgdSA9IHVybHBhcnNlKHBhcnRzWzBdLCAnaHR0cHM6JyArIHBhcnRzWzBdKTtcbiAgICB9XG4gICAgY29uc3QgcHJlZml4ID0gYCR7aXNTY2hlbWFMZXNzID8gJycgOiB1LnByb3RvY29sfSR7dS5zbGFzaGVzID8gJy8vJyA6ICcnfSR7XG4gICAgICB1LmF1dGhcbiAgICB9JHt1LmF1dGggPyAnQCcgOiAnJ30ke3UuaG9zdH1gO1xuICAgIC8vIElmIHRoZXJlIHdhcyBhIHByZWZpeCwgdGhlbiB0aGUgZmlyc3QgcGF0aCBtdXN0IHN0YXJ0IGF0IHRoZSByb290LlxuICAgIGNvbnN0IHBhdGggPSBwb3NpeC5qb2luKFxuICAgICAgYCR7ISFwcmVmaXggJiYgdS5wYXRobmFtZVswXSAhPT0gJy8nID8gJy8nIDogJyd9JHt1LnBhdGhuYW1lfWAsXG4gICAgICAuLi5wYXJ0cy5zbGljZSgxKVxuICAgICk7XG4gICAgcmV0dXJuIGAke3ByZWZpeH0ke3BhdGggPT09ICcuJyA/ICcnIDogcGF0aH1gO1xuICB9XG5cbiAgLyoqXG4gICAqIEVuY29kZSB0aGUgY29tcG9uZW50cyBvZiBhIG11bHRpLXNlZ21lbnQgdXJsLlxuICAgKlxuICAgKiBAcGFyYW0gdXJsIC0gVGhlIHVybCB0byBlbmNvZGUuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBlbmNvZGVkIHVybC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBQcmVzZXJ2ZXMgdGhlIGAnLydgIHNlcGFyYXRvcnMuXG4gICAqIFNob3VsZCBub3QgaW5jbHVkZSB0aGUgYmFzZSB1cmwsIHNpbmNlIGFsbCBwYXJ0cyBhcmUgZXNjYXBlZC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBlbmNvZGVQYXJ0cyh1cmw6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgcmV0dXJuIGpvaW4oLi4udXJsLnNwbGl0KCcvJykubWFwKGVuY29kZVVSSUNvbXBvbmVudCkpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybiBhIHNlcmlhbGl6ZWQgb2JqZWN0IHN0cmluZyBzdWl0YWJsZSBmb3IgYSBxdWVyeS5cbiAgICpcbiAgICogQHBhcmFtIG9iamVjdCAtIFRoZSBzb3VyY2Ugb2JqZWN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBhbiBlbmNvZGVkIHVybCBxdWVyeS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBNb2RpZmllZCB2ZXJzaW9uIG9mIFtzdGFja292ZXJmbG93XShodHRwOi8vc3RhY2tvdmVyZmxvdy5jb20vYS8zMDcwNzQyMykuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gb2JqZWN0VG9RdWVyeVN0cmluZyh2YWx1ZTogUGFydGlhbEpTT05PYmplY3QpOiBzdHJpbmcge1xuICAgIGNvbnN0IGtleXMgPSBPYmplY3Qua2V5cyh2YWx1ZSkuZmlsdGVyKGtleSA9PiBrZXkubGVuZ3RoID4gMCk7XG5cbiAgICBpZiAoIWtleXMubGVuZ3RoKSB7XG4gICAgICByZXR1cm4gJyc7XG4gICAgfVxuXG4gICAgcmV0dXJuIChcbiAgICAgICc/JyArXG4gICAgICBrZXlzXG4gICAgICAgIC5tYXAoa2V5ID0+IHtcbiAgICAgICAgICBjb25zdCBjb250ZW50ID0gZW5jb2RlVVJJQ29tcG9uZW50KFN0cmluZyh2YWx1ZVtrZXldKSk7XG5cbiAgICAgICAgICByZXR1cm4ga2V5ICsgKGNvbnRlbnQgPyAnPScgKyBjb250ZW50IDogJycpO1xuICAgICAgICB9KVxuICAgICAgICAuam9pbignJicpXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm4gYSBwYXJzZWQgb2JqZWN0IHRoYXQgcmVwcmVzZW50cyB0aGUgdmFsdWVzIGluIGEgcXVlcnkgc3RyaW5nLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHF1ZXJ5U3RyaW5nVG9PYmplY3QodmFsdWU6IHN0cmluZyk6IHtcbiAgICBba2V5OiBzdHJpbmddOiBzdHJpbmcgfCB1bmRlZmluZWQ7XG4gIH0ge1xuICAgIHJldHVybiB2YWx1ZVxuICAgICAgLnJlcGxhY2UoL15cXD8vLCAnJylcbiAgICAgIC5zcGxpdCgnJicpXG4gICAgICAucmVkdWNlKFxuICAgICAgICAoYWNjLCB2YWwpID0+IHtcbiAgICAgICAgICBjb25zdCBba2V5LCB2YWx1ZV0gPSB2YWwuc3BsaXQoJz0nKTtcblxuICAgICAgICAgIGlmIChrZXkubGVuZ3RoID4gMCkge1xuICAgICAgICAgICAgYWNjW2tleV0gPSBkZWNvZGVVUklDb21wb25lbnQodmFsdWUgfHwgJycpO1xuICAgICAgICAgIH1cblxuICAgICAgICAgIHJldHVybiBhY2M7XG4gICAgICAgIH0sXG4gICAgICAgIHt9IGFzIHsgW2tleTogc3RyaW5nXTogc3RyaW5nIH1cbiAgICAgICk7XG4gIH1cblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSB1cmwgaXMgYSBsb2NhbCB1cmwuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBmdW5jdGlvbiByZXR1cm5zIGBmYWxzZWAgZm9yIGFueSBmdWxseSBxdWFsaWZpZWQgdXJsLCBpbmNsdWRpbmdcbiAgICogYGRhdGE6YCwgYGZpbGU6YCwgYW5kIGAvL2AgcHJvdG9jb2wgVVJMcy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBpc0xvY2FsKHVybDogc3RyaW5nKTogYm9vbGVhbiB7XG4gICAgY29uc3QgeyBwcm90b2NvbCB9ID0gcGFyc2UodXJsKTtcblxuICAgIHJldHVybiAoXG4gICAgICAoIXByb3RvY29sIHx8IHVybC50b0xvd2VyQ2FzZSgpLmluZGV4T2YocHJvdG9jb2wpICE9PSAwKSAmJlxuICAgICAgdXJsLmluZGV4T2YoJy8nKSAhPT0gMFxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGludGVyZmFjZSBmb3IgYSBVUkwgb2JqZWN0XG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElVcmwge1xuICAgIC8qKlxuICAgICAqIFRoZSBmdWxsIFVSTCBzdHJpbmcgdGhhdCB3YXMgcGFyc2VkIHdpdGggYm90aCB0aGUgcHJvdG9jb2wgYW5kIGhvc3RcbiAgICAgKiBjb21wb25lbnRzIGNvbnZlcnRlZCB0byBsb3dlci1jYXNlLlxuICAgICAqL1xuICAgIGhyZWY6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIElkZW50aWZpZXMgdGhlIFVSTCdzIGxvd2VyLWNhc2VkIHByb3RvY29sIHNjaGVtZS5cbiAgICAgKi9cbiAgICBwcm90b2NvbDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGZ1bGwgbG93ZXItY2FzZWQgaG9zdCBwb3J0aW9uIG9mIHRoZSBVUkwsIGluY2x1ZGluZyB0aGUgcG9ydCBpZlxuICAgICAqIHNwZWNpZmllZC5cbiAgICAgKi9cbiAgICBob3N0OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbG93ZXItY2FzZWQgaG9zdCBuYW1lIHBvcnRpb24gb2YgdGhlIGhvc3QgY29tcG9uZW50IHdpdGhvdXQgdGhlXG4gICAgICogcG9ydCBpbmNsdWRlZC5cbiAgICAgKi9cbiAgICBob3N0bmFtZTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG51bWVyaWMgcG9ydCBwb3J0aW9uIG9mIHRoZSBob3N0IGNvbXBvbmVudC5cbiAgICAgKi9cbiAgICBwb3J0OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZW50aXJlIHBhdGggc2VjdGlvbiBvZiB0aGUgVVJMLlxuICAgICAqL1xuICAgIHBhdGhuYW1lOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgXCJmcmFnbWVudFwiIHBvcnRpb24gb2YgdGhlIFVSTCBpbmNsdWRpbmcgdGhlIGxlYWRpbmcgQVNDSUkgaGFzaFxuICAgICAqIGAoIylgIGNoYXJhY3RlclxuICAgICAqL1xuICAgIGhhc2g6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBzZWFyY2ggZWxlbWVudCwgaW5jbHVkaW5nIGxlYWRpbmcgcXVlc3Rpb24gbWFyayAoYCc/J2ApLCBpZiBhbnksXG4gICAgICogb2YgdGhlIFVSTC5cbiAgICAgKi9cbiAgICBzZWFyY2g/OiBzdHJpbmc7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==