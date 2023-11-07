"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_logconsole_lib_index_js"],{

/***/ "../packages/logconsole/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/logconsole/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ILoggerRegistry": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_2__.ILoggerRegistry),
/* harmony export */   "LogConsolePanel": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.LogConsolePanel),
/* harmony export */   "LogOutputModel": () => (/* reexport safe */ _logger__WEBPACK_IMPORTED_MODULE_0__.LogOutputModel),
/* harmony export */   "Logger": () => (/* reexport safe */ _logger__WEBPACK_IMPORTED_MODULE_0__.Logger),
/* harmony export */   "LoggerOutputAreaModel": () => (/* reexport safe */ _logger__WEBPACK_IMPORTED_MODULE_0__.LoggerOutputAreaModel),
/* harmony export */   "LoggerRegistry": () => (/* reexport safe */ _registry__WEBPACK_IMPORTED_MODULE_1__.LoggerRegistry),
/* harmony export */   "ScrollingWidget": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_3__.ScrollingWidget)
/* harmony export */ });
/* harmony import */ var _logger__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./logger */ "../packages/logconsole/lib/logger.js");
/* harmony import */ var _registry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./registry */ "../packages/logconsole/lib/registry.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../packages/logconsole/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "../packages/logconsole/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module logconsole
 */






/***/ }),

/***/ "../packages/logconsole/lib/logger.js":
/*!********************************************!*\
  !*** ../packages/logconsole/lib/logger.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogOutputModel": () => (/* binding */ LogOutputModel),
/* harmony export */   "Logger": () => (/* binding */ Logger),
/* harmony export */   "LoggerOutputAreaModel": () => (/* binding */ LoggerOutputAreaModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Log Output Model with timestamp which provides
 * item information for Output Area Model.
 */
class LogOutputModel extends _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.OutputModel {
    /**
     * Construct a LogOutputModel.
     *
     * @param options - The model initialization options.
     */
    constructor(options) {
        super(options);
        this.timestamp = new Date(options.value.timestamp);
        this.level = options.value.level;
    }
}
/**
 * Implementation of `IContentFactory` for Output Area Model
 * which creates LogOutputModel instances.
 */
class LogConsoleModelContentFactory extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel.ContentFactory {
    /**
     * Create a rendermime output model from notebook output.
     */
    createOutputModel(options) {
        return new LogOutputModel(options);
    }
}
/**
 * Output Area Model implementation which is able to
 * limit number of outputs stored.
 */
class LoggerOutputAreaModel extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel {
    constructor({ maxLength, ...options }) {
        super(options);
        this.maxLength = maxLength;
    }
    /**
     * Add an output, which may be combined with previous output.
     *
     * @returns The total number of outputs.
     *
     * #### Notes
     * The output bundle is copied. Contiguous stream outputs of the same `name`
     * are combined. The oldest outputs are possibly removed to ensure the total
     * number of outputs is at most `.maxLength`.
     */
    add(output) {
        super.add(output);
        this._applyMaxLength();
        return this.length;
    }
    /**
     * Whether an output should combine with the previous output.
     *
     * We combine if the two outputs are in the same second, which is the
     * resolution for our time display.
     */
    shouldCombine(options) {
        const { value, lastModel } = options;
        const oldSeconds = Math.trunc(lastModel.timestamp.getTime() / 1000);
        const newSeconds = Math.trunc(value.timestamp / 1000);
        return oldSeconds === newSeconds;
    }
    /**
     * Get an item at the specified index.
     */
    get(index) {
        return super.get(index);
    }
    /**
     * Maximum number of outputs to store in the model.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._applyMaxLength();
    }
    /**
     * Manually apply length limit.
     */
    _applyMaxLength() {
        if (this.list.length > this._maxLength) {
            this.list.removeRange(0, this.list.length - this._maxLength);
        }
    }
}
/**
 * A concrete implementation of ILogger.
 */
class Logger {
    /**
     * Construct a Logger.
     *
     * @param source - The name of the log source.
     */
    constructor(options) {
        this._isDisposed = false;
        this._contentChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._rendermime = null;
        this._version = 0;
        this._level = 'warning';
        this.source = options.source;
        this.outputAreaModel = new LoggerOutputAreaModel({
            contentFactory: new LogConsoleModelContentFactory(),
            maxLength: options.maxLength
        });
    }
    /**
     * The maximum number of outputs stored.
     *
     * #### Notes
     * Oldest entries will be trimmed to ensure the length is at most
     * `.maxLength`.
     */
    get maxLength() {
        return this.outputAreaModel.maxLength;
    }
    set maxLength(value) {
        this.outputAreaModel.maxLength = value;
    }
    /**
     * The level of outputs logged
     */
    get level() {
        return this._level;
    }
    set level(newValue) {
        const oldValue = this._level;
        if (oldValue === newValue) {
            return;
        }
        this._level = newValue;
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/plain': `Log level set to ${newValue}`
                }
            },
            level: 'metadata'
        });
        this._stateChanged.emit({ name: 'level', oldValue, newValue });
    }
    /**
     * Number of outputs logged.
     */
    get length() {
        return this.outputAreaModel.length;
    }
    /**
     * A signal emitted when the list of log messages changes.
     */
    get contentChanged() {
        return this._contentChanged;
    }
    /**
     * A signal emitted when the log state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * Rendermime to use when rendering outputs logged.
     */
    get rendermime() {
        return this._rendermime;
    }
    set rendermime(value) {
        if (value !== this._rendermime) {
            const oldValue = this._rendermime;
            const newValue = (this._rendermime = value);
            this._stateChanged.emit({ name: 'rendermime', oldValue, newValue });
        }
    }
    /**
     * The number of messages that have ever been stored.
     */
    get version() {
        return this._version;
    }
    /**
     * Log an output to logger.
     *
     * @param log - The output to be logged.
     */
    log(log) {
        // Filter by our current log level
        if (Private.LogLevel[log.level] <
            Private.LogLevel[this._level]) {
            return;
        }
        let output = null;
        switch (log.type) {
            case 'text':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/plain': log.data
                    }
                };
                break;
            case 'html':
                output = {
                    output_type: 'display_data',
                    data: {
                        'text/html': log.data
                    }
                };
                break;
            case 'output':
                output = log.data;
                break;
            default:
                break;
        }
        if (output) {
            this._log({
                output,
                level: log.level
            });
        }
    }
    /**
     * Clear all outputs logged.
     */
    clear() {
        this.outputAreaModel.clear(false);
        this._contentChanged.emit('clear');
    }
    /**
     * Add a checkpoint to the log.
     */
    checkpoint() {
        this._log({
            output: {
                output_type: 'display_data',
                data: {
                    'text/html': '<hr/>'
                }
            },
            level: 'metadata'
        });
    }
    /**
     * Whether the logger is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the logger.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.clear();
        this._rendermime = null;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    _log(options) {
        // First, make sure our version reflects the new message so things
        // triggering from the signals below have the correct version.
        this._version++;
        // Next, trigger any displays of the message
        this.outputAreaModel.add({
            ...options.output,
            timestamp: Date.now(),
            level: options.level
        });
        // Finally, tell people that the message was appended (and possibly
        // already displayed).
        this._contentChanged.emit('append');
    }
}
var Private;
(function (Private) {
    let LogLevel;
    (function (LogLevel) {
        LogLevel[LogLevel["debug"] = 0] = "debug";
        LogLevel[LogLevel["info"] = 1] = "info";
        LogLevel[LogLevel["warning"] = 2] = "warning";
        LogLevel[LogLevel["error"] = 3] = "error";
        LogLevel[LogLevel["critical"] = 4] = "critical";
        LogLevel[LogLevel["metadata"] = 5] = "metadata";
    })(LogLevel = Private.LogLevel || (Private.LogLevel = {}));
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/logconsole/lib/registry.js":
/*!**********************************************!*\
  !*** ../packages/logconsole/lib/registry.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LoggerRegistry": () => (/* binding */ LoggerRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _logger__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./logger */ "../packages/logconsole/lib/logger.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A concrete implementation of ILoggerRegistry.
 */
class LoggerRegistry {
    /**
     * Construct a LoggerRegistry.
     *
     * @param defaultRendermime - Default rendermime to render outputs
     * with when logger is not supplied with one.
     */
    constructor(options) {
        this._loggers = new Map();
        this._registryChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._isDisposed = false;
        this._defaultRendermime = options.defaultRendermime;
        this._maxLength = options.maxLength;
    }
    /**
     * Get the logger for the specified source.
     *
     * @param source - The name of the log source.
     *
     * @returns The logger for the specified source.
     */
    getLogger(source) {
        const loggers = this._loggers;
        let logger = loggers.get(source);
        if (logger) {
            return logger;
        }
        logger = new _logger__WEBPACK_IMPORTED_MODULE_1__.Logger({ source, maxLength: this.maxLength });
        logger.rendermime = this._defaultRendermime;
        loggers.set(source, logger);
        this._registryChanged.emit('append');
        return logger;
    }
    /**
     * Get all loggers registered.
     *
     * @returns The array containing all registered loggers.
     */
    getLoggers() {
        return Array.from(this._loggers.values());
    }
    /**
     * A signal emitted when the logger registry changes.
     */
    get registryChanged() {
        return this._registryChanged;
    }
    /**
     * The max length for loggers.
     */
    get maxLength() {
        return this._maxLength;
    }
    set maxLength(value) {
        this._maxLength = value;
        this._loggers.forEach(logger => {
            logger.maxLength = value;
        });
    }
    /**
     * Whether the register is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose the registry and all loggers.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._loggers.forEach(x => x.dispose());
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
}


/***/ }),

/***/ "../packages/logconsole/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/logconsole/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ILoggerRegistry": () => (/* binding */ ILoggerRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The Logger Registry token.
 */
const ILoggerRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/logconsole:ILoggerRegistry', 'A service providing a logger infrastructure.');


/***/ }),

/***/ "../packages/logconsole/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/logconsole/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogConsolePanel": () => (/* binding */ LogConsolePanel),
/* harmony export */   "ScrollingWidget": () => (/* binding */ ScrollingWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




function toTitleCase(value) {
    return value.length === 0 ? value : value[0].toUpperCase() + value.slice(1);
}
/**
 * Log console output prompt implementation
 */
class LogConsoleOutputPrompt extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor() {
        super();
        this._timestampNode = document.createElement('div');
        this.node.append(this._timestampNode);
    }
    /**
     * Date & time when output is logged.
     */
    set timestamp(value) {
        this._timestamp = value;
        this._timestampNode.innerHTML = this._timestamp.toLocaleTimeString();
        this.update();
    }
    /**
     * Log level
     */
    set level(value) {
        this._level = value;
        this.node.dataset.logLevel = value;
        this.update();
    }
    update() {
        if (this._level !== undefined && this._timestamp !== undefined) {
            this.node.title = `${this._timestamp.toLocaleString()}; ${toTitleCase(this._level)} level`;
        }
    }
}
/**
 * Output Area implementation displaying log outputs
 * with prompts showing log timestamps.
 */
class LogConsoleOutputArea extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputArea {
    /**
     * Create an output item with a prompt and actual output
     */
    createOutputItem(model) {
        const panel = super.createOutputItem(model);
        if (panel === null) {
            // Could not render model
            return null;
        }
        // first widget in panel is prompt of type LoggerOutputPrompt
        const prompt = panel.widgets[0];
        prompt.timestamp = model.timestamp;
        prompt.level = model.level;
        return panel;
    }
    /**
     * Handle an input request from a kernel by doing nothing.
     */
    onInputRequest(msg, future) {
        return;
    }
}
/**
 * Implementation of `IContentFactory` for Output Area
 * which creates custom output prompts.
 */
class LogConsoleContentFactory extends _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputArea.ContentFactory {
    /**
     * Create the output prompt for the widget.
     */
    createOutputPrompt() {
        return new LogConsoleOutputPrompt();
    }
}
/**
 * Implements a panel which supports pinning the position to the end if it is
 * scrolled to the end.
 *
 * #### Notes
 * This is useful for log viewing components or chat components that append
 * elements at the end. We would like to automatically scroll when the user
 * has scrolled to the bottom, but not change the scrolling when the user has
 * changed the scroll position.
 */
class ScrollingWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    constructor({ content, ...options }) {
        super(options);
        this._observer = null;
        this.addClass('jp-Scrolling');
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.PanelLayout());
        layout.addWidget(content);
        this._content = content;
        this._sentinel = document.createElement('div');
        this.node.appendChild(this._sentinel);
    }
    /**
     * The content widget.
     */
    get content() {
        return this._content;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        // defer so content gets a chance to attach first
        requestAnimationFrame(() => {
            this._sentinel.scrollIntoView();
            this._scrollHeight = this.node.scrollHeight;
        });
        // Set up intersection observer for the sentinel
        if (typeof IntersectionObserver !== 'undefined') {
            this._observer = new IntersectionObserver(args => {
                this._handleScroll(args);
            }, { root: this.node, threshold: 1 });
            this._observer.observe(this._sentinel);
        }
    }
    onBeforeDetach(msg) {
        if (this._observer) {
            this._observer.disconnect();
        }
    }
    onAfterShow(msg) {
        if (this._tracking) {
            this._sentinel.scrollIntoView();
        }
    }
    _handleScroll([entry]) {
        if (entry.isIntersecting) {
            this._tracking = true;
        }
        else if (this.isVisible) {
            const currentHeight = this.node.scrollHeight;
            if (currentHeight === this._scrollHeight) {
                // Likely the user scrolled manually
                this._tracking = false;
            }
            else {
                // We assume we scrolled because our size changed, so scroll to the end.
                this._sentinel.scrollIntoView();
                this._scrollHeight = currentHeight;
                this._tracking = true;
            }
        }
    }
}
/**
 * A StackedPanel implementation that creates Output Areas
 * for each log source and activates as source is switched.
 */
class LogConsolePanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.StackedPanel {
    /**
     * Construct a LogConsolePanel instance.
     *
     * @param loggerRegistry - The logger registry that provides
     * logs to be displayed.
     */
    constructor(loggerRegistry, translator) {
        super();
        this._outputAreas = new Map();
        this._source = null;
        this._sourceChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._sourceDisplayed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._loggersWatched = new Set();
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._loggerRegistry = loggerRegistry;
        this.addClass('jp-LogConsolePanel');
        loggerRegistry.registryChanged.connect((sender, args) => {
            this._bindLoggerSignals();
        }, this);
        this._bindLoggerSignals();
        this._placeholder = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget();
        this._placeholder.addClass('jp-LogConsoleListPlaceholder');
        this.addWidget(this._placeholder);
    }
    /**
     * The logger registry providing the logs.
     */
    get loggerRegistry() {
        return this._loggerRegistry;
    }
    /**
     * The current logger.
     */
    get logger() {
        if (this.source === null) {
            return null;
        }
        return this.loggerRegistry.getLogger(this.source);
    }
    /**
     * The log source displayed
     */
    get source() {
        return this._source;
    }
    set source(name) {
        if (name === this._source) {
            return;
        }
        const oldValue = this._source;
        const newValue = (this._source = name);
        this._showOutputFromSource(newValue);
        this._handlePlaceholder();
        this._sourceChanged.emit({ oldValue, newValue, name: 'source' });
    }
    /**
     * The source version displayed.
     */
    get sourceVersion() {
        const source = this.source;
        return source !== null
            ? this._loggerRegistry.getLogger(source).version
            : null;
    }
    /**
     * Signal for source changes
     */
    get sourceChanged() {
        return this._sourceChanged;
    }
    /**
     * Signal for source changes
     */
    get sourceDisplayed() {
        return this._sourceDisplayed;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        this._updateOutputAreas();
        this._showOutputFromSource(this._source);
        this._handlePlaceholder();
    }
    onAfterShow(msg) {
        super.onAfterShow(msg);
        if (this.source !== null) {
            this._sourceDisplayed.emit({
                source: this.source,
                version: this.sourceVersion
            });
        }
    }
    _bindLoggerSignals() {
        const loggers = this._loggerRegistry.getLoggers();
        for (const logger of loggers) {
            if (this._loggersWatched.has(logger.source)) {
                continue;
            }
            logger.contentChanged.connect((sender, args) => {
                this._updateOutputAreas();
                this._handlePlaceholder();
            }, this);
            logger.stateChanged.connect((sender, change) => {
                if (change.name !== 'rendermime') {
                    return;
                }
                const viewId = `source:${sender.source}`;
                const outputArea = this._outputAreas.get(viewId);
                if (outputArea) {
                    if (change.newValue) {
                        // cast away readonly
                        outputArea.rendermime = change.newValue;
                    }
                    else {
                        outputArea.dispose();
                    }
                }
            }, this);
            this._loggersWatched.add(logger.source);
        }
    }
    _showOutputFromSource(source) {
        // If the source is null, pick a unique name so all output areas hide.
        const viewId = source === null ? 'null source' : `source:${source}`;
        this._outputAreas.forEach((outputArea, name) => {
            var _a, _b;
            // Show/hide the output area parents, the scrolling windows.
            if (outputArea.id === viewId) {
                (_a = outputArea.parent) === null || _a === void 0 ? void 0 : _a.show();
                if (outputArea.isVisible) {
                    this._sourceDisplayed.emit({
                        source: this.source,
                        version: this.sourceVersion
                    });
                }
            }
            else {
                (_b = outputArea.parent) === null || _b === void 0 ? void 0 : _b.hide();
            }
        });
        const title = source === null
            ? this._trans.__('Log Console')
            : this._trans.__('Log: %1', source);
        this.title.label = title;
        this.title.caption = title;
    }
    _handlePlaceholder() {
        if (this.source === null) {
            this._placeholder.node.textContent = this._trans.__('No source selected.');
            this._placeholder.show();
        }
        else if (this._loggerRegistry.getLogger(this.source).length === 0) {
            this._placeholder.node.textContent = this._trans.__('No log messages.');
            this._placeholder.show();
        }
        else {
            this._placeholder.hide();
            this._placeholder.node.textContent = '';
        }
    }
    _updateOutputAreas() {
        const loggerIds = new Set();
        const loggers = this._loggerRegistry.getLoggers();
        for (const logger of loggers) {
            const source = logger.source;
            const viewId = `source:${source}`;
            loggerIds.add(viewId);
            // add view for logger if not exist
            if (!this._outputAreas.has(viewId)) {
                const outputArea = new LogConsoleOutputArea({
                    rendermime: logger.rendermime,
                    contentFactory: new LogConsoleContentFactory(),
                    model: logger.outputAreaModel
                });
                outputArea.id = viewId;
                // Attach the output area so it is visible, so the accounting
                // functions below record the outputs actually displayed.
                const w = new ScrollingWidget({
                    content: outputArea
                });
                this.addWidget(w);
                this._outputAreas.set(viewId, outputArea);
                // This is where the source object is associated with the output area.
                // We capture the source from this environment in the closure.
                const outputUpdate = (sender) => {
                    // If the current log console panel source is the source associated
                    // with this output area, and the output area is visible, then emit
                    // the logConsolePanel source displayed signal.
                    if (this.source === source && sender.isVisible) {
                        // We assume that the output area has been updated to the current
                        // version of the source.
                        this._sourceDisplayed.emit({
                            source: this.source,
                            version: this.sourceVersion
                        });
                    }
                };
                // Notify messages were displayed any time the output area is updated
                // and update for any outputs rendered on construction.
                outputArea.outputLengthChanged.connect(outputUpdate, this);
                // Since the output area was attached above, we can rely on its
                // visibility to account for the messages displayed.
                outputUpdate(outputArea);
            }
        }
        // remove output areas that do not have corresponding loggers anymore
        const viewIds = this._outputAreas.keys();
        for (const viewId of viewIds) {
            if (!loggerIds.has(viewId)) {
                const outputArea = this._outputAreas.get(viewId);
                outputArea === null || outputArea === void 0 ? void 0 : outputArea.dispose();
                this._outputAreas.delete(viewId);
            }
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbG9nY29uc29sZV9saWJfaW5kZXhfanMuZjRjYmEwMGU1ZjJhZjBmNTQ3YzAuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUVzQjtBQUNFO0FBQ0Y7QUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNWekIsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUdnQjtBQUszQztBQUNvQjtBQTBDcEQ7OztHQUdHO0FBQ0ksTUFBTSxjQUFlLFNBQVEsK0RBQVc7SUFDN0M7Ozs7T0FJRztJQUNILFlBQVksT0FBZ0M7UUFDMUMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBRWYsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLElBQUksQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLFNBQVMsQ0FBQyxDQUFDO1FBQ25ELElBQUksQ0FBQyxLQUFLLEdBQUcsT0FBTyxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUM7SUFDbkMsQ0FBQztDQVdGO0FBV0Q7OztHQUdHO0FBQ0gsTUFBTSw2QkFBOEIsU0FBUSxrRkFBOEI7SUFDeEU7O09BRUc7SUFDSCxpQkFBaUIsQ0FBQyxPQUFnQztRQUNoRCxPQUFPLElBQUksY0FBYyxDQUFDLE9BQU8sQ0FBQyxDQUFDO0lBQ3JDLENBQUM7Q0FDRjtBQUVEOzs7R0FHRztBQUNJLE1BQU0scUJBQ1gsU0FBUSxtRUFBZTtJQUd2QixZQUFZLEVBQUUsU0FBUyxFQUFFLEdBQUcsT0FBTyxFQUFrQztRQUNuRSxLQUFLLENBQUMsT0FBTyxDQUFDLENBQUM7UUFDZixJQUFJLENBQUMsU0FBUyxHQUFHLFNBQVMsQ0FBQztJQUM3QixDQUFDO0lBRUQ7Ozs7Ozs7OztPQVNHO0lBQ0gsR0FBRyxDQUFDLE1BQWtCO1FBQ3BCLEtBQUssQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLENBQUM7UUFDbEIsSUFBSSxDQUFDLGVBQWUsRUFBRSxDQUFDO1FBQ3ZCLE9BQU8s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LENBQUMsQ0FBQzthQUNsQztTQUNGO0lBQ0gsQ0FBQztDQWNGIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2xvZ2NvbnNvbGUvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9sb2djb25zb2xlL3NyYy9sb2dnZXIudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2xvZ2NvbnNvbGUvc3JjL3JlZ2lzdHJ5LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9sb2djb25zb2xlL3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2xvZ2NvbnNvbGUvc3JjL3dpZGdldC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBsb2djb25zb2xlXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9sb2dnZXInO1xuZXhwb3J0ICogZnJvbSAnLi9yZWdpc3RyeSc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIG5iZm9ybWF0IGZyb20gJ0BqdXB5dGVybGFiL25iZm9ybWF0JztcbmltcG9ydCB7IElPdXRwdXRBcmVhTW9kZWwsIE91dHB1dEFyZWFNb2RlbCB9IGZyb20gJ0BqdXB5dGVybGFiL291dHB1dGFyZWEnO1xuaW1wb3J0IHtcbiAgSU91dHB1dE1vZGVsLFxuICBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICBPdXRwdXRNb2RlbFxufSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7XG4gIElDb250ZW50Q2hhbmdlLFxuICBJTG9nZ2VyLFxuICBJTG9nZ2VyT3V0cHV0QXJlYU1vZGVsLFxuICBJTG9nUGF5bG9hZCxcbiAgSVN0YXRlQ2hhbmdlLFxuICBMb2dMZXZlbFxufSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogQWxsIHNldmVyaXR5IGxldmVscywgaW5jbHVkaW5nIGFuIGludGVybmFsIG9uZSBmb3IgbWV0YWRhdGEuXG4gKi9cbnR5cGUgRnVsbExvZ0xldmVsID0gTG9nTGV2ZWwgfCAnbWV0YWRhdGEnO1xuXG4vKipcbiAqIEN1c3RvbSBOb3RlYm9vayBPdXRwdXQgd2l0aCBsb2cgaW5mby5cbiAqL1xudHlwZSBJTG9nT3V0cHV0ID0gbmJmb3JtYXQuSU91dHB1dCAmIHtcbiAgLyoqXG4gICAqIERhdGUgJiB0aW1lIHdoZW4gb3V0cHV0IGlzIGxvZ2dlZCBpbiBpbnRlZ2VyIHJlcHJlc2VudGF0aW9uLlxuICAgKi9cbiAgdGltZXN0YW1wOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIExvZyBsZXZlbFxuICAgKi9cbiAgbGV2ZWw6IEZ1bGxMb2dMZXZlbDtcbn07XG5cbmV4cG9ydCBpbnRlcmZhY2UgSUxvZ091dHB1dE1vZGVsIGV4dGVuZHMgSU91dHB1dE1vZGVsIHtcbiAgLyoqXG4gICAqIERhdGUgJiB0aW1lIHdoZW4gb3V0cHV0IGlzIGxvZ2dlZC5cbiAgICovXG4gIHJlYWRvbmx5IHRpbWVzdGFtcDogRGF0ZTtcblxuICAvKipcbiAgICogTG9nIGxldmVsXG4gICAqL1xuICByZWFkb25seSBsZXZlbDogRnVsbExvZ0xldmVsO1xufVxuXG4vKipcbiAqIExvZyBPdXRwdXQgTW9kZWwgd2l0aCB0aW1lc3RhbXAgd2hpY2ggcHJvdmlkZXNcbiAqIGl0ZW0gaW5mb3JtYXRpb24gZm9yIE91dHB1dCBBcmVhIE1vZGVsLlxuICovXG5leHBvcnQgY2xhc3MgTG9nT3V0cHV0TW9kZWwgZXh0ZW5kcyBPdXRwdXRNb2RlbCBpbXBsZW1lbnRzIElMb2dPdXRwdXRNb2RlbCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBMb2dPdXRwdXRNb2RlbC5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgbW9kZWwgaW5pdGlhbGl6YXRpb24gb3B0aW9ucy5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IExvZ091dHB1dE1vZGVsLklPcHRpb25zKSB7XG4gICAgc3VwZXIob3B0aW9ucyk7XG5cbiAgICB0aGlzLnRpbWVzdGFtcCA9IG5ldyBEYXRlKG9wdGlvbnMudmFsdWUudGltZXN0YW1wKTtcbiAgICB0aGlzLmxldmVsID0gb3B0aW9ucy52YWx1ZS5sZXZlbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEYXRlICYgdGltZSB3aGVuIG91dHB1dCBpcyBsb2dnZWQuXG4gICAqL1xuICByZWFkb25seSB0aW1lc3RhbXA6IERhdGU7XG5cbiAgLyoqXG4gICAqIExvZyBsZXZlbFxuICAgKi9cbiAgcmVhZG9ubHkgbGV2ZWw6IEZ1bGxMb2dMZXZlbDtcbn1cblxuLyoqXG4gKiBMb2cgT3V0cHV0IE1vZGVsIG5hbWVzcGFjZSB0aGF0IGRlZmluZXMgaW5pdGlhbGl6YXRpb24gb3B0aW9ucy5cbiAqL1xubmFtZXNwYWNlIExvZ091dHB1dE1vZGVsIHtcbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyBleHRlbmRzIElPdXRwdXRNb2RlbC5JT3B0aW9ucyB7XG4gICAgdmFsdWU6IElMb2dPdXRwdXQ7XG4gIH1cbn1cblxuLyoqXG4gKiBJbXBsZW1lbnRhdGlvbiBvZiBgSUNvbnRlbnRGYWN0b3J5YCBmb3IgT3V0cHV0IEFyZWEgTW9kZWxcbiAqIHdoaWNoIGNyZWF0ZXMgTG9nT3V0cHV0TW9kZWwgaW5zdGFuY2VzLlxuICovXG5jbGFzcyBMb2dDb25zb2xlTW9kZWxDb250ZW50RmFjdG9yeSBleHRlbmRzIE91dHB1dEFyZWFNb2RlbC5Db250ZW50RmFjdG9yeSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSByZW5kZXJtaW1lIG91dHB1dCBtb2RlbCBmcm9tIG5vdGVib29rIG91dHB1dC5cbiAgICovXG4gIGNyZWF0ZU91dHB1dE1vZGVsKG9wdGlvbnM6IExvZ091dHB1dE1vZGVsLklPcHRpb25zKTogTG9nT3V0cHV0TW9kZWwge1xuICAgIHJldHVybiBuZXcgTG9nT3V0cHV0TW9kZWwob3B0aW9ucyk7XG4gIH1cbn1cblxuLyoqXG4gKiBPdXRwdXQgQXJlYSBNb2RlbCBpbXBsZW1lbnRhdGlvbiB3aGljaCBpcyBhYmxlIHRvXG4gKiBsaW1pdCBudW1iZXIgb2Ygb3V0cHV0cyBzdG9yZWQuXG4gKi9cbmV4cG9ydCBjbGFzcyBMb2dnZXJPdXRwdXRBcmVhTW9kZWxcbiAgZXh0ZW5kcyBPdXRwdXRBcmVhTW9kZWxcbiAgaW1wbGVtZW50cyBJTG9nZ2VyT3V0cHV0QXJlYU1vZGVsXG57XG4gIGNvbnN0cnVjdG9yKHsgbWF4TGVuZ3RoLCAuLi5vcHRpb25zIH06IExvZ2dlck91dHB1dEFyZWFNb2RlbC5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIHRoaXMubWF4TGVuZ3RoID0gbWF4TGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhbiBvdXRwdXQsIHdoaWNoIG1heSBiZSBjb21iaW5lZCB3aXRoIHByZXZpb3VzIG91dHB1dC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIHRvdGFsIG51bWJlciBvZiBvdXRwdXRzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBvdXRwdXQgYnVuZGxlIGlzIGNvcGllZC4gQ29udGlndW91cyBzdHJlYW0gb3V0cHV0cyBvZiB0aGUgc2FtZSBgbmFtZWBcbiAgICogYXJlIGNvbWJpbmVkLiBUaGUgb2xkZXN0IG91dHB1dHMgYXJlIHBvc3NpYmx5IHJlbW92ZWQgdG8gZW5zdXJlIHRoZSB0b3RhbFxuICAgKiBudW1iZXIgb2Ygb3V0cHV0cyBpcyBhdCBtb3N0IGAubWF4TGVuZ3RoYC5cbiAgICovXG4gIGFkZChvdXRwdXQ6IElMb2dPdXRwdXQpOiBudW1iZXIge1xuICAgIHN1cGVyLmFkZChvdXRwdXQpO1xuICAgIHRoaXMuX2FwcGx5TWF4TGVuZ3RoKCk7XG4gICAgcmV0dXJuIHRoaXMubGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgYW4gb3V0cHV0IHNob3VsZCBjb21iaW5lIHdpdGggdGhlIHByZXZpb3VzIG91dHB1dC5cbiAgICpcbiAgICogV2UgY29tYmluZSBpZiB0aGUgdHdvIG91dHB1dHMgYXJlIGluIHRoZSBzYW1lIHNlY29uZCwgd2hpY2ggaXMgdGhlXG4gICAqIHJlc29sdXRpb24gZm9yIG91ciB0aW1lIGRpc3BsYXkuXG4gICAqL1xuICBwcm90ZWN0ZWQgc2hvdWxkQ29tYmluZShvcHRpb25zOiB7XG4gICAgdmFsdWU6IElMb2dPdXRwdXQ7XG4gICAgbGFzdE1vZGVsOiBJTG9nT3V0cHV0TW9kZWw7XG4gIH0pOiBib29sZWFuIHtcbiAgICBjb25zdCB7IHZhbHVlLCBsYXN0TW9kZWwgfSA9IG9wdGlvbnM7XG5cbiAgICBjb25zdCBvbGRTZWNvbmRzID0gTWF0aC50cnVuYyhsYXN0TW9kZWwudGltZXN0YW1wLmdldFRpbWUoKSAvIDEwMDApO1xuICAgIGNvbnN0IG5ld1NlY29uZHMgPSBNYXRoLnRydW5jKHZhbHVlLnRpbWVzdGFtcCAvIDEwMDApO1xuXG4gICAgcmV0dXJuIG9sZFNlY29uZHMgPT09IG5ld1NlY29uZHM7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGFuIGl0ZW0gYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICovXG4gIGdldChpbmRleDogbnVtYmVyKTogSUxvZ091dHB1dE1vZGVsIHtcbiAgICByZXR1cm4gc3VwZXIuZ2V0KGluZGV4KSBhcyBJTG9nT3V0cHV0TW9kZWw7XG4gIH1cblxuICAvKipcbiAgICogTWF4aW11bSBudW1iZXIgb2Ygb3V0cHV0cyB0byBzdG9yZSBpbiB0aGUgbW9kZWwuXG4gICAqL1xuICBnZXQgbWF4TGVuZ3RoKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX21heExlbmd0aDtcbiAgfVxuICBzZXQgbWF4TGVuZ3RoKHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLl9tYXhMZW5ndGggPSB2YWx1ZTtcbiAgICB0aGlzLl9hcHBseU1heExlbmd0aCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIE1hbnVhbGx5IGFwcGx5IGxlbmd0aCBsaW1pdC5cbiAgICovXG4gIHByaXZhdGUgX2FwcGx5TWF4TGVuZ3RoKCkge1xuICAgIGlmICh0aGlzLmxpc3QubGVuZ3RoID4gdGhpcy5fbWF4TGVuZ3RoKSB7XG4gICAgICB0aGlzLmxpc3QucmVtb3ZlUmFuZ2UoMCwgdGhpcy5saXN0Lmxlbmd0aCAtIHRoaXMuX21heExlbmd0aCk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfbWF4TGVuZ3RoOiBudW1iZXI7XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgTG9nZ2VyT3V0cHV0QXJlYU1vZGVsIHtcbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyBleHRlbmRzIElPdXRwdXRBcmVhTW9kZWwuSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBtYXhpbXVtIG51bWJlciBvZiBtZXNzYWdlcyBzdG9yZWQuXG4gICAgICovXG4gICAgbWF4TGVuZ3RoOiBudW1iZXI7XG4gIH1cbn1cblxuLyoqXG4gKiBBIGNvbmNyZXRlIGltcGxlbWVudGF0aW9uIG9mIElMb2dnZXIuXG4gKi9cbmV4cG9ydCBjbGFzcyBMb2dnZXIgaW1wbGVtZW50cyBJTG9nZ2VyIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIExvZ2dlci5cbiAgICpcbiAgICogQHBhcmFtIHNvdXJjZSAtIFRoZSBuYW1lIG9mIHRoZSBsb2cgc291cmNlLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTG9nZ2VyLklPcHRpb25zKSB7XG4gICAgdGhpcy5zb3VyY2UgPSBvcHRpb25zLnNvdXJjZTtcbiAgICB0aGlzLm91dHB1dEFyZWFNb2RlbCA9IG5ldyBMb2dnZXJPdXRwdXRBcmVhTW9kZWwoe1xuICAgICAgY29udGVudEZhY3Rvcnk6IG5ldyBMb2dDb25zb2xlTW9kZWxDb250ZW50RmFjdG9yeSgpLFxuICAgICAgbWF4TGVuZ3RoOiBvcHRpb25zLm1heExlbmd0aFxuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBtYXhpbXVtIG51bWJlciBvZiBvdXRwdXRzIHN0b3JlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBPbGRlc3QgZW50cmllcyB3aWxsIGJlIHRyaW1tZWQgdG8gZW5zdXJlIHRoZSBsZW5ndGggaXMgYXQgbW9zdFxuICAgKiBgLm1heExlbmd0aGAuXG4gICAqL1xuICBnZXQgbWF4TGVuZ3RoKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMub3V0cHV0QXJlYU1vZGVsLm1heExlbmd0aDtcbiAgfVxuICBzZXQgbWF4TGVuZ3RoKHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLm91dHB1dEFyZWFNb2RlbC5tYXhMZW5ndGggPSB2YWx1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbGV2ZWwgb2Ygb3V0cHV0cyBsb2dnZWRcbiAgICovXG4gIGdldCBsZXZlbCgpOiBMb2dMZXZlbCB7XG4gICAgcmV0dXJuIHRoaXMuX2xldmVsO1xuICB9XG4gIHNldCBsZXZlbChuZXdWYWx1ZTogTG9nTGV2ZWwpIHtcbiAgICBjb25zdCBvbGRWYWx1ZSA9IHRoaXMuX2xldmVsO1xuICAgIGlmIChvbGRWYWx1ZSA9PT0gbmV3VmFsdWUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fbGV2ZWwgPSBuZXdWYWx1ZTtcbiAgICB0aGlzLl9sb2coe1xuICAgICAgb3V0cHV0OiB7XG4gICAgICAgIG91dHB1dF90eXBlOiAnZGlzcGxheV9kYXRhJyxcbiAgICAgICAgZGF0YToge1xuICAgICAgICAgICd0ZXh0L3BsYWluJzogYExvZyBsZXZlbCBzZXQgdG8gJHtuZXdWYWx1ZX1gXG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBsZXZlbDogJ21ldGFkYXRhJ1xuICAgIH0pO1xuICAgIHRoaXMuX3N0YXRlQ2hhbmdlZC5lbWl0KHsgbmFtZTogJ2xldmVsJywgb2xkVmFsdWUsIG5ld1ZhbHVlIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIE51bWJlciBvZiBvdXRwdXRzIGxvZ2dlZC5cbiAgICovXG4gIGdldCBsZW5ndGgoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5vdXRwdXRBcmVhTW9kZWwubGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbGlzdCBvZiBsb2cgbWVzc2FnZXMgY2hhbmdlcy5cbiAgICovXG4gIGdldCBjb250ZW50Q2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElDb250ZW50Q2hhbmdlPiB7XG4gICAgcmV0dXJuIHRoaXMuX2NvbnRlbnRDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbG9nIHN0YXRlIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgc3RhdGVDaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgSVN0YXRlQ2hhbmdlPiB7XG4gICAgcmV0dXJuIHRoaXMuX3N0YXRlQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXJtaW1lIHRvIHVzZSB3aGVuIHJlbmRlcmluZyBvdXRwdXRzIGxvZ2dlZC5cbiAgICovXG4gIGdldCByZW5kZXJtaW1lKCk6IElSZW5kZXJNaW1lUmVnaXN0cnkgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fcmVuZGVybWltZTtcbiAgfVxuICBzZXQgcmVuZGVybWltZSh2YWx1ZTogSVJlbmRlck1pbWVSZWdpc3RyeSB8IG51bGwpIHtcbiAgICBpZiAodmFsdWUgIT09IHRoaXMuX3JlbmRlcm1pbWUpIHtcbiAgICAgIGNvbnN0IG9sZFZhbHVlID0gdGhpcy5fcmVuZGVybWltZTtcbiAgICAgIGNvbnN0IG5ld1ZhbHVlID0gKHRoaXMuX3JlbmRlcm1pbWUgPSB2YWx1ZSk7XG4gICAgICB0aGlzLl9zdGF0ZUNoYW5nZWQuZW1pdCh7IG5hbWU6ICdyZW5kZXJtaW1lJywgb2xkVmFsdWUsIG5ld1ZhbHVlIH0pO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbnVtYmVyIG9mIG1lc3NhZ2VzIHRoYXQgaGF2ZSBldmVyIGJlZW4gc3RvcmVkLlxuICAgKi9cbiAgZ2V0IHZlcnNpb24oKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5fdmVyc2lvbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc291cmNlIGZvciB0aGUgbG9nZ2VyLlxuICAgKi9cbiAgcmVhZG9ubHkgc291cmNlOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFRoZSBvdXRwdXQgYXJlYSBtb2RlbCB1c2VkIGZvciB0aGUgbG9nZ2VyLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgd2lsbCB1c3VhbGx5IG5vdCBiZSBhY2Nlc3NlZCBkaXJlY3RseS4gSXQgaXMgYSBwdWJsaWMgYXR0cmlidXRlIHNvXG4gICAqIHRoYXQgdGhlIHJlbmRlcmVyIGNhbiBhY2Nlc3MgaXQuXG4gICAqL1xuICByZWFkb25seSBvdXRwdXRBcmVhTW9kZWw6IExvZ2dlck91dHB1dEFyZWFNb2RlbDtcblxuICAvKipcbiAgICogTG9nIGFuIG91dHB1dCB0byBsb2dnZXIuXG4gICAqXG4gICAqIEBwYXJhbSBsb2cgLSBUaGUgb3V0cHV0IHRvIGJlIGxvZ2dlZC5cbiAgICovXG4gIGxvZyhsb2c6IElMb2dQYXlsb2FkKTogdm9pZCB7XG4gICAgLy8gRmlsdGVyIGJ5IG91ciBjdXJyZW50IGxvZyBsZXZlbFxuICAgIGlmIChcbiAgICAgIFByaXZhdGUuTG9nTGV2ZWxbbG9nLmxldmVsIGFzIGtleW9mIHR5cGVvZiBQcml2YXRlLkxvZ0xldmVsXSA8XG4gICAgICBQcml2YXRlLkxvZ0xldmVsW3RoaXMuX2xldmVsIGFzIGtleW9mIHR5cGVvZiBQcml2YXRlLkxvZ0xldmVsXVxuICAgICkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBsZXQgb3V0cHV0OiBuYmZvcm1hdC5JT3V0cHV0IHwgbnVsbCA9IG51bGw7XG4gICAgc3dpdGNoIChsb2cudHlwZSkge1xuICAgICAgY2FzZSAndGV4dCc6XG4gICAgICAgIG91dHB1dCA9IHtcbiAgICAgICAgICBvdXRwdXRfdHlwZTogJ2Rpc3BsYXlfZGF0YScsXG4gICAgICAgICAgZGF0YToge1xuICAgICAgICAgICAgJ3RleHQvcGxhaW4nOiBsb2cuZGF0YVxuICAgICAgICAgIH1cbiAgICAgICAgfTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdodG1sJzpcbiAgICAgICAgb3V0cHV0ID0ge1xuICAgICAgICAgIG91dHB1dF90eXBlOiAnZGlzcGxheV9kYXRhJyxcbiAgICAgICAgICBkYXRhOiB7XG4gICAgICAgICAgICAndGV4dC9odG1sJzogbG9nLmRhdGFcbiAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnb3V0cHV0JzpcbiAgICAgICAgb3V0cHV0ID0gbG9nLmRhdGE7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuXG4gICAgaWYgKG91dHB1dCkge1xuICAgICAgdGhpcy5fbG9nKHtcbiAgICAgICAgb3V0cHV0LFxuICAgICAgICBsZXZlbDogbG9nLmxldmVsXG4gICAgICB9KTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ2xlYXIgYWxsIG91dHB1dHMgbG9nZ2VkLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZCB7XG4gICAgdGhpcy5vdXRwdXRBcmVhTW9kZWwuY2xlYXIoZmFsc2UpO1xuICAgIHRoaXMuX2NvbnRlbnRDaGFuZ2VkLmVtaXQoJ2NsZWFyJyk7XG4gIH1cblxuICAvKipcbiAgICogQWRkIGEgY2hlY2twb2ludCB0byB0aGUgbG9nLlxuICAgKi9cbiAgY2hlY2twb2ludCgpOiB2b2lkIHtcbiAgICB0aGlzLl9sb2coe1xuICAgICAgb3V0cHV0OiB7XG4gICAgICAgIG91dHB1dF90eXBlOiAnZGlzcGxheV9kYXRhJyxcbiAgICAgICAgZGF0YToge1xuICAgICAgICAgICd0ZXh0L2h0bWwnOiAnPGhyLz4nXG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBsZXZlbDogJ21ldGFkYXRhJ1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGxvZ2dlciBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2UgdGhlIGxvZ2dlci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICB0aGlzLmNsZWFyKCk7XG4gICAgdGhpcy5fcmVuZGVybWltZSA9IG51bGwhO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICBwcml2YXRlIF9sb2cob3B0aW9uczogeyBvdXRwdXQ6IG5iZm9ybWF0LklPdXRwdXQ7IGxldmVsOiBGdWxsTG9nTGV2ZWwgfSkge1xuICAgIC8vIEZpcnN0LCBtYWtlIHN1cmUgb3VyIHZlcnNpb24gcmVmbGVjdHMgdGhlIG5ldyBtZXNzYWdlIHNvIHRoaW5nc1xuICAgIC8vIHRyaWdnZXJpbmcgZnJvbSB0aGUgc2lnbmFscyBiZWxvdyBoYXZlIHRoZSBjb3JyZWN0IHZlcnNpb24uXG4gICAgdGhpcy5fdmVyc2lvbisrO1xuXG4gICAgLy8gTmV4dCwgdHJpZ2dlciBhbnkgZGlzcGxheXMgb2YgdGhlIG1lc3NhZ2VcbiAgICB0aGlzLm91dHB1dEFyZWFNb2RlbC5hZGQoe1xuICAgICAgLi4ub3B0aW9ucy5vdXRwdXQsXG4gICAgICB0aW1lc3RhbXA6IERhdGUubm93KCksXG4gICAgICBsZXZlbDogb3B0aW9ucy5sZXZlbFxuICAgIH0pO1xuXG4gICAgLy8gRmluYWxseSwgdGVsbCBwZW9wbGUgdGhhdCB0aGUgbWVzc2FnZSB3YXMgYXBwZW5kZWQgKGFuZCBwb3NzaWJseVxuICAgIC8vIGFscmVhZHkgZGlzcGxheWVkKS5cbiAgICB0aGlzLl9jb250ZW50Q2hhbmdlZC5lbWl0KCdhcHBlbmQnKTtcbiAgfVxuXG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfY29udGVudENoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIElDb250ZW50Q2hhbmdlPih0aGlzKTtcbiAgcHJpdmF0ZSBfc3RhdGVDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBJU3RhdGVDaGFuZ2U+KHRoaXMpO1xuICBwcml2YXRlIF9yZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5IHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX3ZlcnNpb24gPSAwO1xuICBwcml2YXRlIF9sZXZlbDogTG9nTGV2ZWwgPSAnd2FybmluZyc7XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgTG9nZ2VyIHtcbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGxvZyBzb3VyY2UgaWRlbnRpZmllci5cbiAgICAgKi9cbiAgICBzb3VyY2U6IHN0cmluZztcbiAgICAvKipcbiAgICAgKiBUaGUgbWF4aW11bSBudW1iZXIgb2YgbWVzc2FnZXMgdG8gc3RvcmUuXG4gICAgICovXG4gICAgbWF4TGVuZ3RoOiBudW1iZXI7XG4gIH1cbn1cblxubmFtZXNwYWNlIFByaXZhdGUge1xuICBleHBvcnQgZW51bSBMb2dMZXZlbCB7XG4gICAgZGVidWcsXG4gICAgaW5mbyxcbiAgICB3YXJuaW5nLFxuICAgIGVycm9yLFxuICAgIGNyaXRpY2FsLFxuICAgIG1ldGFkYXRhXG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVJlbmRlck1pbWVSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgTG9nZ2VyIH0gZnJvbSAnLi9sb2dnZXInO1xuaW1wb3J0IHsgSUxvZ2dlciwgSUxvZ2dlclJlZ2lzdHJ5LCBJTG9nZ2VyUmVnaXN0cnlDaGFuZ2UgfSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogQSBjb25jcmV0ZSBpbXBsZW1lbnRhdGlvbiBvZiBJTG9nZ2VyUmVnaXN0cnkuXG4gKi9cbmV4cG9ydCBjbGFzcyBMb2dnZXJSZWdpc3RyeSBpbXBsZW1lbnRzIElMb2dnZXJSZWdpc3RyeSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBMb2dnZXJSZWdpc3RyeS5cbiAgICpcbiAgICogQHBhcmFtIGRlZmF1bHRSZW5kZXJtaW1lIC0gRGVmYXVsdCByZW5kZXJtaW1lIHRvIHJlbmRlciBvdXRwdXRzXG4gICAqIHdpdGggd2hlbiBsb2dnZXIgaXMgbm90IHN1cHBsaWVkIHdpdGggb25lLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogTG9nZ2VyUmVnaXN0cnkuSU9wdGlvbnMpIHtcbiAgICB0aGlzLl9kZWZhdWx0UmVuZGVybWltZSA9IG9wdGlvbnMuZGVmYXVsdFJlbmRlcm1pbWU7XG4gICAgdGhpcy5fbWF4TGVuZ3RoID0gb3B0aW9ucy5tYXhMZW5ndGg7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBsb2dnZXIgZm9yIHRoZSBzcGVjaWZpZWQgc291cmNlLlxuICAgKlxuICAgKiBAcGFyYW0gc291cmNlIC0gVGhlIG5hbWUgb2YgdGhlIGxvZyBzb3VyY2UuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBsb2dnZXIgZm9yIHRoZSBzcGVjaWZpZWQgc291cmNlLlxuICAgKi9cbiAgZ2V0TG9nZ2VyKHNvdXJjZTogc3RyaW5nKTogSUxvZ2dlciB7XG4gICAgY29uc3QgbG9nZ2VycyA9IHRoaXMuX2xvZ2dlcnM7XG4gICAgbGV0IGxvZ2dlciA9IGxvZ2dlcnMuZ2V0KHNvdXJjZSk7XG4gICAgaWYgKGxvZ2dlcikge1xuICAgICAgcmV0dXJuIGxvZ2dlcjtcbiAgICB9XG5cbiAgICBsb2dnZXIgPSBuZXcgTG9nZ2VyKHsgc291cmNlLCBtYXhMZW5ndGg6IHRoaXMubWF4TGVuZ3RoIH0pO1xuICAgIGxvZ2dlci5yZW5kZXJtaW1lID0gdGhpcy5fZGVmYXVsdFJlbmRlcm1pbWU7XG4gICAgbG9nZ2Vycy5zZXQoc291cmNlLCBsb2dnZXIpO1xuXG4gICAgdGhpcy5fcmVnaXN0cnlDaGFuZ2VkLmVtaXQoJ2FwcGVuZCcpO1xuXG4gICAgcmV0dXJuIGxvZ2dlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgYWxsIGxvZ2dlcnMgcmVnaXN0ZXJlZC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGFycmF5IGNvbnRhaW5pbmcgYWxsIHJlZ2lzdGVyZWQgbG9nZ2Vycy5cbiAgICovXG4gIGdldExvZ2dlcnMoKTogSUxvZ2dlcltdIHtcbiAgICByZXR1cm4gQXJyYXkuZnJvbSh0aGlzLl9sb2dnZXJzLnZhbHVlcygpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGxvZ2dlciByZWdpc3RyeSBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IHJlZ2lzdHJ5Q2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElMb2dnZXJSZWdpc3RyeUNoYW5nZT4ge1xuICAgIHJldHVybiB0aGlzLl9yZWdpc3RyeUNoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG1heCBsZW5ndGggZm9yIGxvZ2dlcnMuXG4gICAqL1xuICBnZXQgbWF4TGVuZ3RoKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX21heExlbmd0aDtcbiAgfVxuICBzZXQgbWF4TGVuZ3RoKHZhbHVlOiBudW1iZXIpIHtcbiAgICB0aGlzLl9tYXhMZW5ndGggPSB2YWx1ZTtcbiAgICB0aGlzLl9sb2dnZXJzLmZvckVhY2gobG9nZ2VyID0+IHtcbiAgICAgIGxvZ2dlci5tYXhMZW5ndGggPSB2YWx1ZTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSByZWdpc3RlciBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2UgdGhlIHJlZ2lzdHJ5IGFuZCBhbGwgbG9nZ2Vycy5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICB0aGlzLl9sb2dnZXJzLmZvckVhY2goeCA9PiB4LmRpc3Bvc2UoKSk7XG4gICAgU2lnbmFsLmNsZWFyRGF0YSh0aGlzKTtcbiAgfVxuXG4gIHByaXZhdGUgX2RlZmF1bHRSZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5O1xuICBwcml2YXRlIF9sb2dnZXJzID0gbmV3IE1hcDxzdHJpbmcsIElMb2dnZXI+KCk7XG4gIHByaXZhdGUgX21heExlbmd0aDogbnVtYmVyO1xuICBwcml2YXRlIF9yZWdpc3RyeUNoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIElMb2dnZXJSZWdpc3RyeUNoYW5nZT4odGhpcyk7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbn1cblxuZXhwb3J0IG5hbWVzcGFjZSBMb2dnZXJSZWdpc3RyeSB7XG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIGRlZmF1bHRSZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5O1xuICAgIG1heExlbmd0aDogbnVtYmVyO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElDaGFuZ2VkQXJncyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgKiBhcyBuYmZvcm1hdCBmcm9tICdAanVweXRlcmxhYi9uYmZvcm1hdCc7XG5pbXBvcnQgeyBJT3V0cHV0QXJlYU1vZGVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvb3V0cHV0YXJlYSc7XG5pbXBvcnQgeyBJUmVuZGVyTWltZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogVGhlIExvZ2dlciBSZWdpc3RyeSB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElMb2dnZXJSZWdpc3RyeSA9IG5ldyBUb2tlbjxJTG9nZ2VyUmVnaXN0cnk+KFxuICAnQGp1cHl0ZXJsYWIvbG9nY29uc29sZTpJTG9nZ2VyUmVnaXN0cnknLFxuICAnQSBzZXJ2aWNlIHByb3ZpZGluZyBhIGxvZ2dlciBpbmZyYXN0cnVjdHVyZS4nXG4pO1xuXG5leHBvcnQgdHlwZSBJTG9nZ2VyUmVnaXN0cnlDaGFuZ2UgPSAnYXBwZW5kJztcblxuLyoqXG4gKiBBIExvZ2dlciBSZWdpc3RyeSB0aGF0IHJlZ2lzdGVycyBhbmQgcHJvdmlkZXMgbG9nZ2VycyBieSBzb3VyY2UuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUxvZ2dlclJlZ2lzdHJ5IGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAvKipcbiAgICogR2V0IHRoZSBsb2dnZXIgZm9yIHRoZSBzcGVjaWZpZWQgc291cmNlLlxuICAgKlxuICAgKiBAcGFyYW0gc291cmNlIC0gVGhlIG5hbWUgb2YgdGhlIGxvZyBzb3VyY2UuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBsb2dnZXIgZm9yIHRoZSBzcGVjaWZpZWQgc291cmNlLlxuICAgKi9cbiAgZ2V0TG9nZ2VyKHNvdXJjZTogc3RyaW5nKTogSUxvZ2dlcjtcbiAgLyoqXG4gICAqIEdldCBhbGwgbG9nZ2VycyByZWdpc3RlcmVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgYXJyYXkgY29udGFpbmluZyBhbGwgcmVnaXN0ZXJlZCBsb2dnZXJzLlxuICAgKi9cbiAgZ2V0TG9nZ2VycygpOiBJTG9nZ2VyW107XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbG9nZ2VyIHJlZ2lzdHJ5IGNoYW5nZXMuXG4gICAqL1xuICByZWFkb25seSByZWdpc3RyeUNoYW5nZWQ6IElTaWduYWw8dGhpcywgSUxvZ2dlclJlZ2lzdHJ5Q2hhbmdlPjtcbn1cblxuLyoqXG4gKiBMb2cgc2V2ZXJpdHkgbGV2ZWxcbiAqL1xuZXhwb3J0IHR5cGUgTG9nTGV2ZWwgPSAnY3JpdGljYWwnIHwgJ2Vycm9yJyB8ICd3YXJuaW5nJyB8ICdpbmZvJyB8ICdkZWJ1Zyc7XG5cbi8qKlxuICogVGhlIGJhc2UgbG9nIHBheWxvYWQgdHlwZS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJTG9nUGF5bG9hZEJhc2Uge1xuICAvKipcbiAgICogVHlwZSBvZiBsb2cgZGF0YS5cbiAgICovXG4gIHR5cGU6IHN0cmluZztcblxuICAvKipcbiAgICogTG9nIGxldmVsXG4gICAqL1xuICBsZXZlbDogTG9nTGV2ZWw7XG5cbiAgLyoqXG4gICAqIERhdGFcbiAgICovXG4gIGRhdGE6IGFueTtcbn1cblxuLyoqXG4gKiBQbGFpbiB0ZXh0IGxvZyBwYXlsb2FkLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElUZXh0TG9nIGV4dGVuZHMgSUxvZ1BheWxvYWRCYXNlIHtcbiAgLyoqXG4gICAqIFR5cGUgb2YgbG9nIGRhdGEuXG4gICAqL1xuICB0eXBlOiAndGV4dCc7XG4gIC8qKlxuICAgKiBMb2cgZGF0YSBhcyBwbGFpbiB0ZXh0LlxuICAgKi9cbiAgZGF0YTogc3RyaW5nO1xufVxuXG4vKipcbiAqIEhUTUwgbG9nIHBheWxvYWQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUh0bWxMb2cgZXh0ZW5kcyBJTG9nUGF5bG9hZEJhc2Uge1xuICAvKipcbiAgICogVHlwZSBvZiBsb2cgZGF0YS5cbiAgICovXG4gIHR5cGU6ICdodG1sJztcbiAgLyoqXG4gICAqIExvZyBkYXRhIGFzIEhUTUwgc3RyaW5nLlxuICAgKi9cbiAgZGF0YTogc3RyaW5nO1xufVxuXG4vKipcbiAqIE5vdGVib29rIGtlcm5lbCBvdXRwdXQgbG9nIHBheWxvYWQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU91dHB1dExvZyBleHRlbmRzIElMb2dQYXlsb2FkQmFzZSB7XG4gIC8qKlxuICAgKiBUeXBlIG9mIGxvZyBkYXRhLlxuICAgKi9cbiAgdHlwZTogJ291dHB1dCc7XG4gIC8qKlxuICAgKiBMb2cgZGF0YSBhcyBOb3RlYm9vayBrZXJuZWwgb3V0cHV0LlxuICAgKi9cbiAgZGF0YTogbmJmb3JtYXQuSU91dHB1dDtcbn1cblxuLyoqXG4gKiBMb2cgcGF5bG9hZCB1bmlvbiB0eXBlLlxuICovXG5leHBvcnQgdHlwZSBJTG9nUGF5bG9hZCA9IElUZXh0TG9nIHwgSUh0bWxMb2cgfCBJT3V0cHV0TG9nO1xuXG5leHBvcnQgdHlwZSBJQ29udGVudENoYW5nZSA9ICdhcHBlbmQnIHwgJ2NsZWFyJztcblxuZXhwb3J0IHR5cGUgSVN0YXRlQ2hhbmdlID1cbiAgfCBJQ2hhbmdlZEFyZ3M8XG4gICAgICBJUmVuZGVyTWltZVJlZ2lzdHJ5IHwgbnVsbCxcbiAgICAgIElSZW5kZXJNaW1lUmVnaXN0cnkgfCBudWxsLFxuICAgICAgJ3JlbmRlcm1pbWUnXG4gICAgPlxuICB8IElDaGFuZ2VkQXJnczxMb2dMZXZlbCwgTG9nTGV2ZWwsICdsZXZlbCc+O1xuXG5leHBvcnQgaW50ZXJmYWNlIElMb2dnZXJPdXRwdXRBcmVhTW9kZWwgZXh0ZW5kcyBJT3V0cHV0QXJlYU1vZGVsIHtcbiAgLyoqXG4gICAqIFRoZSBtYXhpbXVtIG51bWJlciBvZiBvdXRwdXRzIHRvIHN0b3JlLlxuICAgKi9cbiAgbWF4TGVuZ3RoOiBudW1iZXI7XG59XG5cbi8qKlxuICogQSBMb2dnZXIgdGhhdCBtYW5hZ2VzIGxvZ3MgZnJvbSBhIHBhcnRpY3VsYXIgc291cmNlLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElMb2dnZXIgZXh0ZW5kcyBJRGlzcG9zYWJsZSB7XG4gIC8qKlxuICAgKiBOdW1iZXIgb2Ygb3V0cHV0cyBsb2dnZWQuXG4gICAqL1xuICByZWFkb25seSBsZW5ndGg6IG51bWJlcjtcbiAgLyoqXG4gICAqIE1heCBudW1iZXIgb2YgbWVzc2FnZXMuXG4gICAqL1xuICBtYXhMZW5ndGg6IG51bWJlcjtcbiAgLyoqXG4gICAqIExvZyBsZXZlbC5cbiAgICovXG4gIGxldmVsOiBMb2dMZXZlbDtcbiAgLyoqXG4gICAqIFJlbmRlcm1pbWUgdG8gdXNlIHdoZW4gcmVuZGVyaW5nIG91dHB1dHMgbG9nZ2VkLlxuICAgKi9cbiAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeSB8IG51bGw7XG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGxvZyBtb2RlbCBjaGFuZ2VzLlxuICAgKi9cbiAgcmVhZG9ubHkgY29udGVudENoYW5nZWQ6IElTaWduYWw8dGhpcywgSUNvbnRlbnRDaGFuZ2U+O1xuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSByZW5kZXJtaW1lIGNoYW5nZXMuXG4gICAqL1xuICByZWFkb25seSBzdGF0ZUNoYW5nZWQ6IElTaWduYWw8dGhpcywgSVN0YXRlQ2hhbmdlPjtcbiAgLyoqXG4gICAqIFRoZSBuYW1lIG9mIHRoZSBsb2cgc291cmNlLlxuICAgKi9cbiAgcmVhZG9ubHkgc291cmNlOiBzdHJpbmc7XG4gIC8qKlxuICAgKiBPdXRwdXQgQXJlYSBNb2RlbCB1c2VkIHRvIG1hbmFnZSBsb2cgc3RvcmFnZSBpbiBtZW1vcnkuXG4gICAqL1xuICByZWFkb25seSBvdXRwdXRBcmVhTW9kZWw6IElMb2dnZXJPdXRwdXRBcmVhTW9kZWw7XG4gIC8qKlxuICAgKiBUaGUgY3VtdWxhdGl2ZSBudW1iZXIgb2YgbWVzc2FnZXMgdGhlIGxvZyBoYXMgc3RvcmVkLlxuICAgKi9cbiAgcmVhZG9ubHkgdmVyc2lvbjogbnVtYmVyO1xuICAvKipcbiAgICogTG9nIGFuIG91dHB1dCB0byBsb2dnZXIuXG4gICAqXG4gICAqIEBwYXJhbSBsb2cgLSBUaGUgb3V0cHV0IHRvIGJlIGxvZ2dlZC5cbiAgICovXG4gIGxvZyhsb2c6IElMb2dQYXlsb2FkKTogdm9pZDtcbiAgLyoqXG4gICAqIEFkZCBhIGNoZWNrcG9pbnQgaW4gdGhlIGxvZy5cbiAgICovXG4gIGNoZWNrcG9pbnQoKTogdm9pZDtcbiAgLyoqXG4gICAqIENsZWFyIGFsbCBvdXRwdXRzIGxvZ2dlZC5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQ7XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElDaGFuZ2VkQXJncyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgKiBhcyBuYmZvcm1hdCBmcm9tICdAanVweXRlcmxhYi9uYmZvcm1hdCc7XG5pbXBvcnQgeyBJT3V0cHV0UHJvbXB0LCBPdXRwdXRBcmVhIH0gZnJvbSAnQGp1cHl0ZXJsYWIvb3V0cHV0YXJlYSc7XG5pbXBvcnQgeyBJUmVuZGVyTWltZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBLZXJuZWwsIEtlcm5lbE1lc3NhZ2UgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBQYW5lbCwgUGFuZWxMYXlvdXQsIFN0YWNrZWRQYW5lbCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IExvZ2dlck91dHB1dEFyZWFNb2RlbCwgTG9nT3V0cHV0TW9kZWwgfSBmcm9tICcuL2xvZ2dlcic7XG5pbXBvcnQge1xuICBJQ29udGVudENoYW5nZSxcbiAgSUxvZ2dlcixcbiAgSUxvZ2dlclJlZ2lzdHJ5LFxuICBJTG9nZ2VyUmVnaXN0cnlDaGFuZ2UsXG4gIElTdGF0ZUNoYW5nZSxcbiAgTG9nTGV2ZWxcbn0gZnJvbSAnLi90b2tlbnMnO1xuXG5mdW5jdGlvbiB0b1RpdGxlQ2FzZSh2YWx1ZTogc3RyaW5nKSB7XG4gIHJldHVybiB2YWx1ZS5sZW5ndGggPT09IDAgPyB2YWx1ZSA6IHZhbHVlWzBdLnRvVXBwZXJDYXNlKCkgKyB2YWx1ZS5zbGljZSgxKTtcbn1cblxuLyoqXG4gKiBBbGwgc2V2ZXJpdHkgbGV2ZWxzLCBpbmNsdWRpbmcgYW4gaW50ZXJuYWwgb25lIGZvciBtZXRhZGF0YS5cbiAqL1xudHlwZSBGdWxsTG9nTGV2ZWwgPSBMb2dMZXZlbCB8ICdtZXRhZGF0YSc7XG5cbi8qKlxuICogTG9nIGNvbnNvbGUgb3V0cHV0IHByb21wdCBpbXBsZW1lbnRhdGlvblxuICovXG5jbGFzcyBMb2dDb25zb2xlT3V0cHV0UHJvbXB0IGV4dGVuZHMgV2lkZ2V0IGltcGxlbWVudHMgSU91dHB1dFByb21wdCB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5fdGltZXN0YW1wTm9kZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIHRoaXMubm9kZS5hcHBlbmQodGhpcy5fdGltZXN0YW1wTm9kZSk7XG4gIH1cblxuICAvKipcbiAgICogRGF0ZSAmIHRpbWUgd2hlbiBvdXRwdXQgaXMgbG9nZ2VkLlxuICAgKi9cbiAgc2V0IHRpbWVzdGFtcCh2YWx1ZTogRGF0ZSkge1xuICAgIHRoaXMuX3RpbWVzdGFtcCA9IHZhbHVlO1xuICAgIHRoaXMuX3RpbWVzdGFtcE5vZGUuaW5uZXJIVE1MID0gdGhpcy5fdGltZXN0YW1wLnRvTG9jYWxlVGltZVN0cmluZygpO1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogTG9nIGxldmVsXG4gICAqL1xuICBzZXQgbGV2ZWwodmFsdWU6IEZ1bGxMb2dMZXZlbCkge1xuICAgIHRoaXMuX2xldmVsID0gdmFsdWU7XG4gICAgdGhpcy5ub2RlLmRhdGFzZXQubG9nTGV2ZWwgPSB2YWx1ZTtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgdXBkYXRlKCkge1xuICAgIGlmICh0aGlzLl9sZXZlbCAhPT0gdW5kZWZpbmVkICYmIHRoaXMuX3RpbWVzdGFtcCAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICB0aGlzLm5vZGUudGl0bGUgPSBgJHt0aGlzLl90aW1lc3RhbXAudG9Mb2NhbGVTdHJpbmcoKX07ICR7dG9UaXRsZUNhc2UoXG4gICAgICAgIHRoaXMuX2xldmVsXG4gICAgICApfSBsZXZlbGA7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBleGVjdXRpb24gY291bnQgZm9yIHRoZSBwcm9tcHQuXG4gICAqL1xuICBleGVjdXRpb25Db3VudDogbmJmb3JtYXQuRXhlY3V0aW9uQ291bnQ7XG5cbiAgcHJpdmF0ZSBfdGltZXN0YW1wOiBEYXRlO1xuICBwcml2YXRlIF9sZXZlbDogRnVsbExvZ0xldmVsO1xuICBwcml2YXRlIF90aW1lc3RhbXBOb2RlOiBIVE1MRGl2RWxlbWVudDtcbn1cblxuLyoqXG4gKiBPdXRwdXQgQXJlYSBpbXBsZW1lbnRhdGlvbiBkaXNwbGF5aW5nIGxvZyBvdXRwdXRzXG4gKiB3aXRoIHByb21wdHMgc2hvd2luZyBsb2cgdGltZXN0YW1wcy5cbiAqL1xuY2xhc3MgTG9nQ29uc29sZU91dHB1dEFyZWEgZXh0ZW5kcyBPdXRwdXRBcmVhIHtcbiAgLyoqXG4gICAqIE91dHB1dCBhcmVhIG1vZGVsIHVzZWQgYnkgdGhlIHdpZGdldC5cbiAgICovXG4gIHJlYWRvbmx5IG1vZGVsOiBMb2dnZXJPdXRwdXRBcmVhTW9kZWw7XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiBvdXRwdXQgaXRlbSB3aXRoIGEgcHJvbXB0IGFuZCBhY3R1YWwgb3V0cHV0XG4gICAqL1xuICBwcm90ZWN0ZWQgY3JlYXRlT3V0cHV0SXRlbShtb2RlbDogTG9nT3V0cHV0TW9kZWwpOiBXaWRnZXQgfCBudWxsIHtcbiAgICBjb25zdCBwYW5lbCA9IHN1cGVyLmNyZWF0ZU91dHB1dEl0ZW0obW9kZWwpIGFzIFBhbmVsO1xuICAgIGlmIChwYW5lbCA9PT0gbnVsbCkge1xuICAgICAgLy8gQ291bGQgbm90IHJlbmRlciBtb2RlbFxuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuXG4gICAgLy8gZmlyc3Qgd2lkZ2V0IGluIHBhbmVsIGlzIHByb21wdCBvZiB0eXBlIExvZ2dlck91dHB1dFByb21wdFxuICAgIGNvbnN0IHByb21wdCA9IHBhbmVsLndpZGdldHNbMF0gYXMgTG9nQ29uc29sZU91dHB1dFByb21wdDtcbiAgICBwcm9tcHQudGltZXN0YW1wID0gbW9kZWwudGltZXN0YW1wO1xuICAgIHByb21wdC5sZXZlbCA9IG1vZGVsLmxldmVsO1xuICAgIHJldHVybiBwYW5lbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYW4gaW5wdXQgcmVxdWVzdCBmcm9tIGEga2VybmVsIGJ5IGRvaW5nIG5vdGhpbmcuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25JbnB1dFJlcXVlc3QoXG4gICAgbXNnOiBLZXJuZWxNZXNzYWdlLklJbnB1dFJlcXVlc3RNc2csXG4gICAgZnV0dXJlOiBLZXJuZWwuSVNoZWxsRnV0dXJlXG4gICk6IHZvaWQge1xuICAgIHJldHVybjtcbiAgfVxufVxuXG4vKipcbiAqIEltcGxlbWVudGF0aW9uIG9mIGBJQ29udGVudEZhY3RvcnlgIGZvciBPdXRwdXQgQXJlYVxuICogd2hpY2ggY3JlYXRlcyBjdXN0b20gb3V0cHV0IHByb21wdHMuXG4gKi9cbmNsYXNzIExvZ0NvbnNvbGVDb250ZW50RmFjdG9yeSBleHRlbmRzIE91dHB1dEFyZWEuQ29udGVudEZhY3Rvcnkge1xuICAvKipcbiAgICogQ3JlYXRlIHRoZSBvdXRwdXQgcHJvbXB0IGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgY3JlYXRlT3V0cHV0UHJvbXB0KCk6IExvZ0NvbnNvbGVPdXRwdXRQcm9tcHQge1xuICAgIHJldHVybiBuZXcgTG9nQ29uc29sZU91dHB1dFByb21wdCgpO1xuICB9XG59XG5cbi8qKlxuICogSW1wbGVtZW50cyBhIHBhbmVsIHdoaWNoIHN1cHBvcnRzIHBpbm5pbmcgdGhlIHBvc2l0aW9uIHRvIHRoZSBlbmQgaWYgaXQgaXNcbiAqIHNjcm9sbGVkIHRvIHRoZSBlbmQuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhpcyBpcyB1c2VmdWwgZm9yIGxvZyB2aWV3aW5nIGNvbXBvbmVudHMgb3IgY2hhdCBjb21wb25lbnRzIHRoYXQgYXBwZW5kXG4gKiBlbGVtZW50cyBhdCB0aGUgZW5kLiBXZSB3b3VsZCBsaWtlIHRvIGF1dG9tYXRpY2FsbHkgc2Nyb2xsIHdoZW4gdGhlIHVzZXJcbiAqIGhhcyBzY3JvbGxlZCB0byB0aGUgYm90dG9tLCBidXQgbm90IGNoYW5nZSB0aGUgc2Nyb2xsaW5nIHdoZW4gdGhlIHVzZXIgaGFzXG4gKiBjaGFuZ2VkIHRoZSBzY3JvbGwgcG9zaXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBTY3JvbGxpbmdXaWRnZXQ8VCBleHRlbmRzIFdpZGdldD4gZXh0ZW5kcyBXaWRnZXQge1xuICBjb25zdHJ1Y3Rvcih7IGNvbnRlbnQsIC4uLm9wdGlvbnMgfTogU2Nyb2xsaW5nV2lkZ2V0LklPcHRpb25zPFQ+KSB7XG4gICAgc3VwZXIob3B0aW9ucyk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtU2Nyb2xsaW5nJyk7XG4gICAgY29uc3QgbGF5b3V0ID0gKHRoaXMubGF5b3V0ID0gbmV3IFBhbmVsTGF5b3V0KCkpO1xuICAgIGxheW91dC5hZGRXaWRnZXQoY29udGVudCk7XG5cbiAgICB0aGlzLl9jb250ZW50ID0gY29udGVudDtcbiAgICB0aGlzLl9zZW50aW5lbCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIHRoaXMubm9kZS5hcHBlbmRDaGlsZCh0aGlzLl9zZW50aW5lbCk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGNvbnRlbnQgd2lkZ2V0LlxuICAgKi9cbiAgZ2V0IGNvbnRlbnQoKTogVCB7XG4gICAgcmV0dXJuIHRoaXMuX2NvbnRlbnQ7XG4gIH1cblxuICBwcm90ZWN0ZWQgb25BZnRlckF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBzdXBlci5vbkFmdGVyQXR0YWNoKG1zZyk7XG4gICAgLy8gZGVmZXIgc28gY29udGVudCBnZXRzIGEgY2hhbmNlIHRvIGF0dGFjaCBmaXJzdFxuICAgIHJlcXVlc3RBbmltYXRpb25GcmFtZSgoKSA9PiB7XG4gICAgICB0aGlzLl9zZW50aW5lbC5zY3JvbGxJbnRvVmlldygpO1xuICAgICAgdGhpcy5fc2Nyb2xsSGVpZ2h0ID0gdGhpcy5ub2RlLnNjcm9sbEhlaWdodDtcbiAgICB9KTtcblxuICAgIC8vIFNldCB1cCBpbnRlcnNlY3Rpb24gb2JzZXJ2ZXIgZm9yIHRoZSBzZW50aW5lbFxuICAgIGlmICh0eXBlb2YgSW50ZXJzZWN0aW9uT2JzZXJ2ZXIgIT09ICd1bmRlZmluZWQnKSB7XG4gICAgICB0aGlzLl9vYnNlcnZlciA9IG5ldyBJbnRlcnNlY3Rpb25PYnNlcnZlcihcbiAgICAgICAgYXJncyA9PiB7XG4gICAgICAgICAgdGhpcy5faGFuZGxlU2Nyb2xsKGFyZ3MpO1xuICAgICAgICB9LFxuICAgICAgICB7IHJvb3Q6IHRoaXMubm9kZSwgdGhyZXNob2xkOiAxIH1cbiAgICAgICk7XG4gICAgICB0aGlzLl9vYnNlcnZlci5vYnNlcnZlKHRoaXMuX3NlbnRpbmVsKTtcbiAgICB9XG4gIH1cblxuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX29ic2VydmVyKSB7XG4gICAgICB0aGlzLl9vYnNlcnZlci5kaXNjb25uZWN0KCk7XG4gICAgfVxuICB9XG5cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJTaG93KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGlmICh0aGlzLl90cmFja2luZykge1xuICAgICAgdGhpcy5fc2VudGluZWwuc2Nyb2xsSW50b1ZpZXcoKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9oYW5kbGVTY3JvbGwoW2VudHJ5XTogSW50ZXJzZWN0aW9uT2JzZXJ2ZXJFbnRyeVtdKSB7XG4gICAgaWYgKGVudHJ5LmlzSW50ZXJzZWN0aW5nKSB7XG4gICAgICB0aGlzLl90cmFja2luZyA9IHRydWU7XG4gICAgfSBlbHNlIGlmICh0aGlzLmlzVmlzaWJsZSkge1xuICAgICAgY29uc3QgY3VycmVudEhlaWdodCA9IHRoaXMubm9kZS5zY3JvbGxIZWlnaHQ7XG4gICAgICBpZiAoY3VycmVudEhlaWdodCA9PT0gdGhpcy5fc2Nyb2xsSGVpZ2h0KSB7XG4gICAgICAgIC8vIExpa2VseSB0aGUgdXNlciBzY3JvbGxlZCBtYW51YWxseVxuICAgICAgICB0aGlzLl90cmFja2luZyA9IGZhbHNlO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgLy8gV2UgYXNzdW1lIHdlIHNjcm9sbGVkIGJlY2F1c2Ugb3VyIHNpemUgY2hhbmdlZCwgc28gc2Nyb2xsIHRvIHRoZSBlbmQuXG4gICAgICAgIHRoaXMuX3NlbnRpbmVsLnNjcm9sbEludG9WaWV3KCk7XG4gICAgICAgIHRoaXMuX3Njcm9sbEhlaWdodCA9IGN1cnJlbnRIZWlnaHQ7XG4gICAgICAgIHRoaXMuX3RyYWNraW5nID0gdHJ1ZTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9jb250ZW50OiBUO1xuICBwcml2YXRlIF9vYnNlcnZlcjogSW50ZXJzZWN0aW9uT2JzZXJ2ZXIgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfc2Nyb2xsSGVpZ2h0OiBudW1iZXI7XG4gIHByaXZhdGUgX3NlbnRpbmVsOiBIVE1MRGl2RWxlbWVudDtcbiAgcHJpdmF0ZSBfdHJhY2tpbmc6IGJvb2xlYW47XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgU2Nyb2xsaW5nV2lkZ2V0IHtcbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9uczxUIGV4dGVuZHMgV2lkZ2V0PiBleHRlbmRzIFdpZGdldC5JT3B0aW9ucyB7XG4gICAgY29udGVudDogVDtcbiAgfVxufVxuXG4vKipcbiAqIEEgU3RhY2tlZFBhbmVsIGltcGxlbWVudGF0aW9uIHRoYXQgY3JlYXRlcyBPdXRwdXQgQXJlYXNcbiAqIGZvciBlYWNoIGxvZyBzb3VyY2UgYW5kIGFjdGl2YXRlcyBhcyBzb3VyY2UgaXMgc3dpdGNoZWQuXG4gKi9cbmV4cG9ydCBjbGFzcyBMb2dDb25zb2xlUGFuZWwgZXh0ZW5kcyBTdGFja2VkUGFuZWwge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgTG9nQ29uc29sZVBhbmVsIGluc3RhbmNlLlxuICAgKlxuICAgKiBAcGFyYW0gbG9nZ2VyUmVnaXN0cnkgLSBUaGUgbG9nZ2VyIHJlZ2lzdHJ5IHRoYXQgcHJvdmlkZXNcbiAgICogbG9ncyB0byBiZSBkaXNwbGF5ZWQuXG4gICAqL1xuICBjb25zdHJ1Y3Rvcihsb2dnZXJSZWdpc3RyeTogSUxvZ2dlclJlZ2lzdHJ5LCB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3IpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IHRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIHRoaXMuX2xvZ2dlclJlZ2lzdHJ5ID0gbG9nZ2VyUmVnaXN0cnk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtTG9nQ29uc29sZVBhbmVsJyk7XG5cbiAgICBsb2dnZXJSZWdpc3RyeS5yZWdpc3RyeUNoYW5nZWQuY29ubmVjdChcbiAgICAgIChzZW5kZXI6IElMb2dnZXJSZWdpc3RyeSwgYXJnczogSUxvZ2dlclJlZ2lzdHJ5Q2hhbmdlKSA9PiB7XG4gICAgICAgIHRoaXMuX2JpbmRMb2dnZXJTaWduYWxzKCk7XG4gICAgICB9LFxuICAgICAgdGhpc1xuICAgICk7XG5cbiAgICB0aGlzLl9iaW5kTG9nZ2VyU2lnbmFscygpO1xuXG4gICAgdGhpcy5fcGxhY2Vob2xkZXIgPSBuZXcgV2lkZ2V0KCk7XG4gICAgdGhpcy5fcGxhY2Vob2xkZXIuYWRkQ2xhc3MoJ2pwLUxvZ0NvbnNvbGVMaXN0UGxhY2Vob2xkZXInKTtcbiAgICB0aGlzLmFkZFdpZGdldCh0aGlzLl9wbGFjZWhvbGRlcik7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGxvZ2dlciByZWdpc3RyeSBwcm92aWRpbmcgdGhlIGxvZ3MuXG4gICAqL1xuICBnZXQgbG9nZ2VyUmVnaXN0cnkoKTogSUxvZ2dlclJlZ2lzdHJ5IHtcbiAgICByZXR1cm4gdGhpcy5fbG9nZ2VyUmVnaXN0cnk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgbG9nZ2VyLlxuICAgKi9cbiAgZ2V0IGxvZ2dlcigpOiBJTG9nZ2VyIHwgbnVsbCB7XG4gICAgaWYgKHRoaXMuc291cmNlID09PSBudWxsKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXMubG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VyKHRoaXMuc291cmNlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbG9nIHNvdXJjZSBkaXNwbGF5ZWRcbiAgICovXG4gIGdldCBzb3VyY2UoKTogc3RyaW5nIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX3NvdXJjZTtcbiAgfVxuICBzZXQgc291cmNlKG5hbWU6IHN0cmluZyB8IG51bGwpIHtcbiAgICBpZiAobmFtZSA9PT0gdGhpcy5fc291cmNlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IG9sZFZhbHVlID0gdGhpcy5fc291cmNlO1xuICAgIGNvbnN0IG5ld1ZhbHVlID0gKHRoaXMuX3NvdXJjZSA9IG5hbWUpO1xuICAgIHRoaXMuX3Nob3dPdXRwdXRGcm9tU291cmNlKG5ld1ZhbHVlKTtcbiAgICB0aGlzLl9oYW5kbGVQbGFjZWhvbGRlcigpO1xuICAgIHRoaXMuX3NvdXJjZUNoYW5nZWQuZW1pdCh7IG9sZFZhbHVlLCBuZXdWYWx1ZSwgbmFtZTogJ3NvdXJjZScgfSk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNvdXJjZSB2ZXJzaW9uIGRpc3BsYXllZC5cbiAgICovXG4gIGdldCBzb3VyY2VWZXJzaW9uKCk6IG51bWJlciB8IG51bGwge1xuICAgIGNvbnN0IHNvdXJjZSA9IHRoaXMuc291cmNlO1xuICAgIHJldHVybiBzb3VyY2UgIT09IG51bGxcbiAgICAgID8gdGhpcy5fbG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VyKHNvdXJjZSkudmVyc2lvblxuICAgICAgOiBudWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIFNpZ25hbCBmb3Igc291cmNlIGNoYW5nZXNcbiAgICovXG4gIGdldCBzb3VyY2VDaGFuZ2VkKCk6IElTaWduYWw8XG4gICAgdGhpcyxcbiAgICBJQ2hhbmdlZEFyZ3M8c3RyaW5nIHwgbnVsbCwgc3RyaW5nIHwgbnVsbCwgJ3NvdXJjZSc+XG4gID4ge1xuICAgIHJldHVybiB0aGlzLl9zb3VyY2VDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFNpZ25hbCBmb3Igc291cmNlIGNoYW5nZXNcbiAgICovXG4gIGdldCBzb3VyY2VEaXNwbGF5ZWQoKTogSVNpZ25hbDx0aGlzLCBJU291cmNlRGlzcGxheWVkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3NvdXJjZURpc3BsYXllZDtcbiAgfVxuXG4gIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHN1cGVyLm9uQWZ0ZXJBdHRhY2gobXNnKTtcbiAgICB0aGlzLl91cGRhdGVPdXRwdXRBcmVhcygpO1xuICAgIHRoaXMuX3Nob3dPdXRwdXRGcm9tU291cmNlKHRoaXMuX3NvdXJjZSk7XG4gICAgdGhpcy5faGFuZGxlUGxhY2Vob2xkZXIoKTtcbiAgfVxuXG4gIHByb3RlY3RlZCBvbkFmdGVyU2hvdyhtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBzdXBlci5vbkFmdGVyU2hvdyhtc2cpO1xuICAgIGlmICh0aGlzLnNvdXJjZSAhPT0gbnVsbCkge1xuICAgICAgdGhpcy5fc291cmNlRGlzcGxheWVkLmVtaXQoe1xuICAgICAgICBzb3VyY2U6IHRoaXMuc291cmNlLFxuICAgICAgICB2ZXJzaW9uOiB0aGlzLnNvdXJjZVZlcnNpb25cbiAgICAgIH0pO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2JpbmRMb2dnZXJTaWduYWxzKCkge1xuICAgIGNvbnN0IGxvZ2dlcnMgPSB0aGlzLl9sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXJzKCk7XG4gICAgZm9yIChjb25zdCBsb2dnZXIgb2YgbG9nZ2Vycykge1xuICAgICAgaWYgKHRoaXMuX2xvZ2dlcnNXYXRjaGVkLmhhcyhsb2dnZXIuc291cmNlKSkge1xuICAgICAgICBjb250aW51ZTtcbiAgICAgIH1cblxuICAgICAgbG9nZ2VyLmNvbnRlbnRDaGFuZ2VkLmNvbm5lY3QoKHNlbmRlcjogSUxvZ2dlciwgYXJnczogSUNvbnRlbnRDaGFuZ2UpID0+IHtcbiAgICAgICAgdGhpcy5fdXBkYXRlT3V0cHV0QXJlYXMoKTtcbiAgICAgICAgdGhpcy5faGFuZGxlUGxhY2Vob2xkZXIoKTtcbiAgICAgIH0sIHRoaXMpO1xuXG4gICAgICBsb2dnZXIuc3RhdGVDaGFuZ2VkLmNvbm5lY3QoKHNlbmRlcjogSUxvZ2dlciwgY2hhbmdlOiBJU3RhdGVDaGFuZ2UpID0+IHtcbiAgICAgICAgaWYgKGNoYW5nZS5uYW1lICE9PSAncmVuZGVybWltZScpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3Qgdmlld0lkID0gYHNvdXJjZToke3NlbmRlci5zb3VyY2V9YDtcbiAgICAgICAgY29uc3Qgb3V0cHV0QXJlYSA9IHRoaXMuX291dHB1dEFyZWFzLmdldCh2aWV3SWQpO1xuICAgICAgICBpZiAob3V0cHV0QXJlYSkge1xuICAgICAgICAgIGlmIChjaGFuZ2UubmV3VmFsdWUpIHtcbiAgICAgICAgICAgIC8vIGNhc3QgYXdheSByZWFkb25seVxuICAgICAgICAgICAgKG91dHB1dEFyZWEucmVuZGVybWltZSBhcyBJUmVuZGVyTWltZVJlZ2lzdHJ5KSA9IGNoYW5nZS5uZXdWYWx1ZTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgb3V0cHV0QXJlYS5kaXNwb3NlKCk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9LCB0aGlzKTtcblxuICAgICAgdGhpcy5fbG9nZ2Vyc1dhdGNoZWQuYWRkKGxvZ2dlci5zb3VyY2UpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX3Nob3dPdXRwdXRGcm9tU291cmNlKHNvdXJjZTogc3RyaW5nIHwgbnVsbCkge1xuICAgIC8vIElmIHRoZSBzb3VyY2UgaXMgbnVsbCwgcGljayBhIHVuaXF1ZSBuYW1lIHNvIGFsbCBvdXRwdXQgYXJlYXMgaGlkZS5cbiAgICBjb25zdCB2aWV3SWQgPSBzb3VyY2UgPT09IG51bGwgPyAnbnVsbCBzb3VyY2UnIDogYHNvdXJjZToke3NvdXJjZX1gO1xuXG4gICAgdGhpcy5fb3V0cHV0QXJlYXMuZm9yRWFjaChcbiAgICAgIChvdXRwdXRBcmVhOiBMb2dDb25zb2xlT3V0cHV0QXJlYSwgbmFtZTogc3RyaW5nKSA9PiB7XG4gICAgICAgIC8vIFNob3cvaGlkZSB0aGUgb3V0cHV0IGFyZWEgcGFyZW50cywgdGhlIHNjcm9sbGluZyB3aW5kb3dzLlxuICAgICAgICBpZiAob3V0cHV0QXJlYS5pZCA9PT0gdmlld0lkKSB7XG4gICAgICAgICAgb3V0cHV0QXJlYS5wYXJlbnQ/LnNob3coKTtcbiAgICAgICAgICBpZiAob3V0cHV0QXJlYS5pc1Zpc2libGUpIHtcbiAgICAgICAgICAgIHRoaXMuX3NvdXJjZURpc3BsYXllZC5lbWl0KHtcbiAgICAgICAgICAgICAgc291cmNlOiB0aGlzLnNvdXJjZSxcbiAgICAgICAgICAgICAgdmVyc2lvbjogdGhpcy5zb3VyY2VWZXJzaW9uXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgb3V0cHV0QXJlYS5wYXJlbnQ/LmhpZGUoKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICk7XG5cbiAgICBjb25zdCB0aXRsZSA9XG4gICAgICBzb3VyY2UgPT09IG51bGxcbiAgICAgICAgPyB0aGlzLl90cmFucy5fXygnTG9nIENvbnNvbGUnKVxuICAgICAgICA6IHRoaXMuX3RyYW5zLl9fKCdMb2c6ICUxJywgc291cmNlKTtcbiAgICB0aGlzLnRpdGxlLmxhYmVsID0gdGl0bGU7XG4gICAgdGhpcy50aXRsZS5jYXB0aW9uID0gdGl0bGU7XG4gIH1cblxuICBwcml2YXRlIF9oYW5kbGVQbGFjZWhvbGRlcigpIHtcbiAgICBpZiAodGhpcy5zb3VyY2UgPT09IG51bGwpIHtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyLm5vZGUudGV4dENvbnRlbnQgPSB0aGlzLl90cmFucy5fXyhcbiAgICAgICAgJ05vIHNvdXJjZSBzZWxlY3RlZC4nXG4gICAgICApO1xuICAgICAgdGhpcy5fcGxhY2Vob2xkZXIuc2hvdygpO1xuICAgIH0gZWxzZSBpZiAodGhpcy5fbG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VyKHRoaXMuc291cmNlKS5sZW5ndGggPT09IDApIHtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyLm5vZGUudGV4dENvbnRlbnQgPSB0aGlzLl90cmFucy5fXygnTm8gbG9nIG1lc3NhZ2VzLicpO1xuICAgICAgdGhpcy5fcGxhY2Vob2xkZXIuc2hvdygpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9wbGFjZWhvbGRlci5oaWRlKCk7XG4gICAgICB0aGlzLl9wbGFjZWhvbGRlci5ub2RlLnRleHRDb250ZW50ID0gJyc7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfdXBkYXRlT3V0cHV0QXJlYXMoKSB7XG4gICAgY29uc3QgbG9nZ2VySWRzID0gbmV3IFNldDxzdHJpbmc+KCk7XG4gICAgY29uc3QgbG9nZ2VycyA9IHRoaXMuX2xvZ2dlclJlZ2lzdHJ5LmdldExvZ2dlcnMoKTtcblxuICAgIGZvciAoY29uc3QgbG9nZ2VyIG9mIGxvZ2dlcnMpIHtcbiAgICAgIGNvbnN0IHNvdXJjZSA9IGxvZ2dlci5zb3VyY2U7XG4gICAgICBjb25zdCB2aWV3SWQgPSBgc291cmNlOiR7c291cmNlfWA7XG4gICAgICBsb2dnZXJJZHMuYWRkKHZpZXdJZCk7XG5cbiAgICAgIC8vIGFkZCB2aWV3IGZvciBsb2dnZXIgaWYgbm90IGV4aXN0XG4gICAgICBpZiAoIXRoaXMuX291dHB1dEFyZWFzLmhhcyh2aWV3SWQpKSB7XG4gICAgICAgIGNvbnN0IG91dHB1dEFyZWEgPSBuZXcgTG9nQ29uc29sZU91dHB1dEFyZWEoe1xuICAgICAgICAgIHJlbmRlcm1pbWU6IGxvZ2dlci5yZW5kZXJtaW1lISxcbiAgICAgICAgICBjb250ZW50RmFjdG9yeTogbmV3IExvZ0NvbnNvbGVDb250ZW50RmFjdG9yeSgpLFxuICAgICAgICAgIG1vZGVsOiBsb2dnZXIub3V0cHV0QXJlYU1vZGVsXG4gICAgICAgIH0pO1xuICAgICAgICBvdXRwdXRBcmVhLmlkID0gdmlld0lkO1xuXG4gICAgICAgIC8vIEF0dGFjaCB0aGUgb3V0cHV0IGFyZWEgc28gaXQgaXMgdmlzaWJsZSwgc28gdGhlIGFjY291bnRpbmdcbiAgICAgICAgLy8gZnVuY3Rpb25zIGJlbG93IHJlY29yZCB0aGUgb3V0cHV0cyBhY3R1YWxseSBkaXNwbGF5ZWQuXG4gICAgICAgIGNvbnN0IHcgPSBuZXcgU2Nyb2xsaW5nV2lkZ2V0KHtcbiAgICAgICAgICBjb250ZW50OiBvdXRwdXRBcmVhXG4gICAgICAgIH0pO1xuICAgICAgICB0aGlzLmFkZFdpZGdldCh3KTtcbiAgICAgICAgdGhpcy5fb3V0cHV0QXJlYXMuc2V0KHZpZXdJZCwgb3V0cHV0QXJlYSk7XG5cbiAgICAgICAgLy8gVGhpcyBpcyB3aGVyZSB0aGUgc291cmNlIG9iamVjdCBpcyBhc3NvY2lhdGVkIHdpdGggdGhlIG91dHB1dCBhcmVhLlxuICAgICAgICAvLyBXZSBjYXB0dXJlIHRoZSBzb3VyY2UgZnJvbSB0aGlzIGVudmlyb25tZW50IGluIHRoZSBjbG9zdXJlLlxuICAgICAgICBjb25zdCBvdXRwdXRVcGRhdGUgPSAoc2VuZGVyOiBMb2dDb25zb2xlT3V0cHV0QXJlYSkgPT4ge1xuICAgICAgICAgIC8vIElmIHRoZSBjdXJyZW50IGxvZyBjb25zb2xlIHBhbmVsIHNvdXJjZSBpcyB0aGUgc291cmNlIGFzc29jaWF0ZWRcbiAgICAgICAgICAvLyB3aXRoIHRoaXMgb3V0cHV0IGFyZWEsIGFuZCB0aGUgb3V0cHV0IGFyZWEgaXMgdmlzaWJsZSwgdGhlbiBlbWl0XG4gICAgICAgICAgLy8gdGhlIGxvZ0NvbnNvbGVQYW5lbCBzb3VyY2UgZGlzcGxheWVkIHNpZ25hbC5cbiAgICAgICAgICBpZiAodGhpcy5zb3VyY2UgPT09IHNvdXJjZSAmJiBzZW5kZXIuaXNWaXNpYmxlKSB7XG4gICAgICAgICAgICAvLyBXZSBhc3N1bWUgdGhhdCB0aGUgb3V0cHV0IGFyZWEgaGFzIGJlZW4gdXBkYXRlZCB0byB0aGUgY3VycmVudFxuICAgICAgICAgICAgLy8gdmVyc2lvbiBvZiB0aGUgc291cmNlLlxuICAgICAgICAgICAgdGhpcy5fc291cmNlRGlzcGxheWVkLmVtaXQoe1xuICAgICAgICAgICAgICBzb3VyY2U6IHRoaXMuc291cmNlLFxuICAgICAgICAgICAgICB2ZXJzaW9uOiB0aGlzLnNvdXJjZVZlcnNpb25cbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfTtcbiAgICAgICAgLy8gTm90aWZ5IG1lc3NhZ2VzIHdlcmUgZGlzcGxheWVkIGFueSB0aW1lIHRoZSBvdXRwdXQgYXJlYSBpcyB1cGRhdGVkXG4gICAgICAgIC8vIGFuZCB1cGRhdGUgZm9yIGFueSBvdXRwdXRzIHJlbmRlcmVkIG9uIGNvbnN0cnVjdGlvbi5cbiAgICAgICAgb3V0cHV0QXJlYS5vdXRwdXRMZW5ndGhDaGFuZ2VkLmNvbm5lY3Qob3V0cHV0VXBkYXRlLCB0aGlzKTtcbiAgICAgICAgLy8gU2luY2UgdGhlIG91dHB1dCBhcmVhIHdhcyBhdHRhY2hlZCBhYm92ZSwgd2UgY2FuIHJlbHkgb24gaXRzXG4gICAgICAgIC8vIHZpc2liaWxpdHkgdG8gYWNjb3VudCBmb3IgdGhlIG1lc3NhZ2VzIGRpc3BsYXllZC5cbiAgICAgICAgb3V0cHV0VXBkYXRlKG91dHB1dEFyZWEpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8vIHJlbW92ZSBvdXRwdXQgYXJlYXMgdGhhdCBkbyBub3QgaGF2ZSBjb3JyZXNwb25kaW5nIGxvZ2dlcnMgYW55bW9yZVxuICAgIGNvbnN0IHZpZXdJZHMgPSB0aGlzLl9vdXRwdXRBcmVhcy5rZXlzKCk7XG5cbiAgICBmb3IgKGNvbnN0IHZpZXdJZCBvZiB2aWV3SWRzKSB7XG4gICAgICBpZiAoIWxvZ2dlcklkcy5oYXModmlld0lkKSkge1xuICAgICAgICBjb25zdCBvdXRwdXRBcmVhID0gdGhpcy5fb3V0cHV0QXJlYXMuZ2V0KHZpZXdJZCk7XG4gICAgICAgIG91dHB1dEFyZWE/LmRpc3Bvc2UoKTtcbiAgICAgICAgdGhpcy5fb3V0cHV0QXJlYXMuZGVsZXRlKHZpZXdJZCk7XG4gICAgICB9XG4gICAgfVxuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF90cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gIHByaXZhdGUgX2xvZ2dlclJlZ2lzdHJ5OiBJTG9nZ2VyUmVnaXN0cnk7XG4gIHByaXZhdGUgX291dHB1dEFyZWFzID0gbmV3IE1hcDxzdHJpbmcsIExvZ0NvbnNvbGVPdXRwdXRBcmVhPigpO1xuICBwcml2YXRlIF9zb3VyY2U6IHN0cmluZyB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9zb3VyY2VDaGFuZ2VkID0gbmV3IFNpZ25hbDxcbiAgICB0aGlzLFxuICAgIElDaGFuZ2VkQXJnczxzdHJpbmcgfCBudWxsLCBzdHJpbmcgfCBudWxsLCAnc291cmNlJz5cbiAgPih0aGlzKTtcbiAgcHJpdmF0ZSBfc291cmNlRGlzcGxheWVkID0gbmV3IFNpZ25hbDx0aGlzLCBJU291cmNlRGlzcGxheWVkPih0aGlzKTtcbiAgcHJpdmF0ZSBfcGxhY2Vob2xkZXI6IFdpZGdldDtcbiAgcHJpdmF0ZSBfbG9nZ2Vyc1dhdGNoZWQ6IFNldDxzdHJpbmc+ID0gbmV3IFNldCgpO1xufVxuXG5leHBvcnQgaW50ZXJmYWNlIElTb3VyY2VEaXNwbGF5ZWQge1xuICBzb3VyY2U6IHN0cmluZyB8IG51bGw7XG4gIHZlcnNpb246IG51bWJlciB8IG51bGw7XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=