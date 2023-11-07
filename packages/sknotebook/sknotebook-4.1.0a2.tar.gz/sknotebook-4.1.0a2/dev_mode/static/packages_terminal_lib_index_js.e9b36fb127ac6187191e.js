"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_terminal_lib_index_js"],{

/***/ "../packages/terminal/lib/index.js":
/*!*****************************************!*\
  !*** ../packages/terminal/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITerminal": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.ITerminal),
/* harmony export */   "ITerminalTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.ITerminalTracker),
/* harmony export */   "Terminal": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.Terminal)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/terminal/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/terminal/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module terminal
 */




/***/ }),

/***/ "../packages/terminal/lib/tokens.js":
/*!******************************************!*\
  !*** ../packages/terminal/lib/tokens.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITerminal": () => (/* binding */ ITerminal),
/* harmony export */   "ITerminalTracker": () => (/* binding */ ITerminalTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The editor tracker token.
 */
const ITerminalTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/terminal:ITerminalTracker', `A widget tracker for terminals.
  Use this if you want to be able to iterate over and interact with terminals
  created by the application.`);
/**
 * The namespace for terminals. Separated from the widget so it can be lazy
 * loaded.
 */
var ITerminal;
(function (ITerminal) {
    /**
     * The default options used for creating terminals.
     */
    ITerminal.defaultOptions = {
        theme: 'inherit',
        fontFamily: 'Menlo, Consolas, "DejaVu Sans Mono", monospace',
        fontSize: 13,
        lineHeight: 1.0,
        scrollback: 1000,
        shutdownOnClose: false,
        closeOnExit: true,
        cursorBlink: true,
        initialCommand: '',
        screenReaderMode: false,
        pasteWithCtrlV: true,
        autoFit: true,
        macOptionIsMeta: false
    };
})(ITerminal || (ITerminal = {}));


/***/ }),

/***/ "../packages/terminal/lib/widget.js":
/*!******************************************!*\
  !*** ../packages/terminal/lib/widget.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Terminal": () => (/* binding */ Terminal)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! . */ "../packages/terminal/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.






/**
 * The class name added to a terminal widget.
 */
const TERMINAL_CLASS = 'jp-Terminal';
/**
 * The class name added to a terminal body.
 */
const TERMINAL_BODY_CLASS = 'jp-Terminal-body';
/**
 * A widget which manages a terminal session.
 */
class Terminal extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new terminal widget.
     *
     * @param session - The terminal session object.
     *
     * @param options - The terminal configuration options.
     *
     * @param translator - The language translator.
     */
    constructor(session, options = {}, translator) {
        super();
        this._needsResize = true;
        this._offsetWidth = -1;
        this._offsetHeight = -1;
        this._isReady = false;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.PromiseDelegate();
        this._termOpened = false;
        translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this._trans = translator.load('jupyterlab');
        this.session = session;
        // Initialize settings.
        this._options = { ...___WEBPACK_IMPORTED_MODULE_5__.ITerminal.defaultOptions, ...options };
        const { theme, ...other } = this._options;
        const xtermOptions = {
            theme: Private.getXTermTheme(theme),
            ...other
        };
        this.addClass(TERMINAL_CLASS);
        this._setThemeAttribute(theme);
        // Buffer session message while waiting for the terminal
        let buffer = '';
        const bufferMessage = (sender, msg) => {
            switch (msg.type) {
                case 'stdout':
                    if (msg.content) {
                        buffer += msg.content[0];
                    }
                    break;
                default:
                    break;
            }
        };
        session.messageReceived.connect(bufferMessage);
        session.disposed.connect(() => {
            if (this.getOption('closeOnExit')) {
                this.dispose();
            }
        }, this);
        // Create the xterm.
        Private.createTerminal(xtermOptions)
            .then(([term, fitAddon]) => {
            this._term = term;
            this._fitAddon = fitAddon;
            this._initializeTerm();
            this.id = `jp-Terminal-${Private.id++}`;
            this.title.label = this._trans.__('Terminal');
            this._isReady = true;
            this._ready.resolve();
            if (buffer) {
                this._term.write(buffer);
            }
            session.messageReceived.disconnect(bufferMessage);
            session.messageReceived.connect(this._onMessage, this);
            if (session.connectionStatus === 'connected') {
                this._initialConnection();
            }
            else {
                session.connectionStatusChanged.connect(this._initialConnection, this);
            }
            this.update();
        })
            .catch(reason => {
            console.error('Failed to create a terminal.\n', reason);
            this._ready.reject(reason);
        });
    }
    /**
     * A promise that is fulfilled when the terminal is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Get a config option for the terminal.
     */
    getOption(option) {
        return this._options[option];
    }
    /**
     * Set a config option for the terminal.
     */
    setOption(option, value) {
        if (option !== 'theme' &&
            (this._options[option] === value || option === 'initialCommand')) {
            return;
        }
        this._options[option] = value;
        switch (option) {
            case 'fontFamily':
                this._term.options.fontFamily = value;
                break;
            case 'fontSize':
                this._term.options.fontSize = value;
                break;
            case 'lineHeight':
                this._term.options.lineHeight = value;
                break;
            case 'screenReaderMode':
                this._term.options.screenReaderMode = value;
                break;
            case 'scrollback':
                this._term.options.scrollback = value;
                break;
            case 'theme':
                this._term.options.theme = {
                    ...Private.getXTermTheme(value)
                };
                this._setThemeAttribute(value);
                break;
            case 'macOptionIsMeta':
                this._term.options.macOptionIsMeta = value;
                break;
            default:
                // Do not transmit options not listed above to XTerm
                break;
        }
        this._needsResize = true;
        this.update();
    }
    /**
     * Dispose of the resources held by the terminal widget.
     */
    dispose() {
        if (!this.session.isDisposed) {
            if (this.getOption('shutdownOnClose')) {
                this.session.shutdown().catch(reason => {
                    console.error(`Terminal not shut down: ${reason}`);
                });
            }
        }
        void this.ready.then(() => {
            this._term.dispose();
        });
        super.dispose();
    }
    /**
     * Refresh the terminal session.
     *
     * #### Notes
     * Failure to reconnect to the session should be caught appropriately
     */
    async refresh() {
        if (!this.isDisposed && this._isReady) {
            await this.session.reconnect();
            this._term.clear();
        }
    }
    /**
     * Check if terminal has any text selected.
     */
    hasSelection() {
        if (!this.isDisposed && this._isReady) {
            return this._term.hasSelection();
        }
        return false;
    }
    /**
     * Paste text into terminal.
     */
    paste(data) {
        if (!this.isDisposed && this._isReady) {
            return this._term.paste(data);
        }
    }
    /**
     * Get selected text from terminal.
     */
    getSelection() {
        if (!this.isDisposed && this._isReady) {
            return this._term.getSelection();
        }
        return null;
    }
    /**
     * Process a message sent to the widget.
     *
     * @param msg - The message sent to the widget.
     *
     * #### Notes
     * Subclasses may reimplement this method as needed.
     */
    processMessage(msg) {
        super.processMessage(msg);
        switch (msg.type) {
            case 'fit-request':
                this.onFitRequest(msg);
                break;
            default:
                break;
        }
    }
    /**
     * Set the size of the terminal when attached if dirty.
     */
    onAfterAttach(msg) {
        this.update();
    }
    /**
     * Set the size of the terminal when shown if dirty.
     */
    onAfterShow(msg) {
        this.update();
    }
    /**
     * On resize, use the computed row and column sizes to resize the terminal.
     */
    onResize(msg) {
        this._offsetWidth = msg.width;
        this._offsetHeight = msg.height;
        this._needsResize = true;
        this.update();
    }
    /**
     * A message handler invoked on an `'update-request'` message.
     */
    onUpdateRequest(msg) {
        var _a;
        if (!this.isVisible || !this.isAttached || !this._isReady) {
            return;
        }
        // Open the terminal if necessary.
        if (!this._termOpened) {
            this._term.open(this.node);
            (_a = this._term.element) === null || _a === void 0 ? void 0 : _a.classList.add(TERMINAL_BODY_CLASS);
            this._termOpened = true;
        }
        if (this._needsResize) {
            this._resizeTerminal();
        }
    }
    /**
     * A message handler invoked on an `'fit-request'` message.
     */
    onFitRequest(msg) {
        const resize = _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget.ResizeMessage.UnknownSize;
        _lumino_messaging__WEBPACK_IMPORTED_MODULE_3__.MessageLoop.sendMessage(this, resize);
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        var _a;
        (_a = this._term) === null || _a === void 0 ? void 0 : _a.focus();
    }
    _initialConnection() {
        if (this.isDisposed) {
            return;
        }
        if (this.session.connectionStatus !== 'connected') {
            return;
        }
        this.title.label = this._trans.__('Terminal %1', this.session.name);
        this._setSessionSize();
        if (this._options.initialCommand) {
            this.session.send({
                type: 'stdin',
                content: [this._options.initialCommand + '\r']
            });
        }
        // Only run this initial connection logic once.
        this.session.connectionStatusChanged.disconnect(this._initialConnection, this);
    }
    /**
     * Initialize the terminal object.
     */
    _initializeTerm() {
        const term = this._term;
        term.onData((data) => {
            if (this.isDisposed) {
                return;
            }
            this.session.send({
                type: 'stdin',
                content: [data]
            });
        });
        term.onTitleChange((title) => {
            this.title.label = title;
        });
        // Do not add any Ctrl+C/Ctrl+V handling on macOS,
        // where Cmd+C/Cmd+V works as intended.
        if (_lumino_domutils__WEBPACK_IMPORTED_MODULE_2__.Platform.IS_MAC) {
            return;
        }
        term.attachCustomKeyEventHandler(event => {
            if (event.ctrlKey && event.key === 'c' && term.hasSelection()) {
                // Return so that the usual OS copy happens
                // instead of interrupt signal.
                return false;
            }
            if (event.ctrlKey && event.key === 'v' && this._options.pasteWithCtrlV) {
                // Return so that the usual paste happens.
                return false;
            }
            return true;
        });
    }
    /**
     * Handle a message from the terminal session.
     */
    _onMessage(sender, msg) {
        switch (msg.type) {
            case 'stdout':
                if (msg.content) {
                    this._term.write(msg.content[0]);
                }
                break;
            case 'disconnect':
                this._term.write('\r\n\r\n[Finished… Term Session]\r\n');
                break;
            default:
                break;
        }
    }
    /**
     * Resize the terminal based on computed geometry.
     */
    _resizeTerminal() {
        if (this._options.autoFit) {
            this._fitAddon.fit();
        }
        if (this._offsetWidth === -1) {
            this._offsetWidth = this.node.offsetWidth;
        }
        if (this._offsetHeight === -1) {
            this._offsetHeight = this.node.offsetHeight;
        }
        this._setSessionSize();
        this._needsResize = false;
    }
    /**
     * Set the size of the terminal in the session.
     */
    _setSessionSize() {
        const content = [
            this._term.rows,
            this._term.cols,
            this._offsetHeight,
            this._offsetWidth
        ];
        if (!this.isDisposed) {
            this.session.send({ type: 'set_size', content });
        }
    }
    _setThemeAttribute(theme) {
        if (this.isDisposed) {
            return;
        }
        this.node.setAttribute('data-term-theme', theme ? theme.toLowerCase() : 'inherit');
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An incrementing counter for ids.
     */
    Private.id = 0;
    /**
     * The light terminal theme.
     */
    Private.lightTheme = {
        foreground: '#000',
        background: '#fff',
        cursor: '#616161',
        cursorAccent: '#F5F5F5',
        selectionBackground: 'rgba(97, 97, 97, 0.3)',
        selectionInactiveBackground: 'rgba(189, 189, 189, 0.3)' // md-grey-400
    };
    /**
     * The dark terminal theme.
     */
    Private.darkTheme = {
        foreground: '#fff',
        background: '#000',
        cursor: '#fff',
        cursorAccent: '#000',
        selectionBackground: 'rgba(255, 255, 255, 0.3)',
        selectionInactiveBackground: 'rgba(238, 238, 238, 0.3)' // md-grey-200
    };
    /**
     * The current theme.
     */
    Private.inheritTheme = () => ({
        foreground: getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-font-color0')
            .trim(),
        background: getComputedStyle(document.body)
            .getPropertyValue('--jp-layout-color0')
            .trim(),
        cursor: getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-font-color1')
            .trim(),
        cursorAccent: getComputedStyle(document.body)
            .getPropertyValue('--jp-ui-inverse-font-color0')
            .trim(),
        selectionBackground: getComputedStyle(document.body)
            .getPropertyValue('--jp-layout-color3')
            .trim(),
        selectionInactiveBackground: getComputedStyle(document.body)
            .getPropertyValue('--jp-layout-color2')
            .trim()
    });
    function getXTermTheme(theme) {
        switch (theme) {
            case 'light':
                return Private.lightTheme;
            case 'dark':
                return Private.darkTheme;
            case 'inherit':
            default:
                return Private.inheritTheme();
        }
    }
    Private.getXTermTheme = getXTermTheme;
})(Private || (Private = {}));
/**
 * Utility functions for creating a Terminal widget
 */
(function (Private) {
    let supportWebGL = false;
    let Xterm_;
    let FitAddon_;
    let WeblinksAddon_;
    let Renderer_;
    /**
     * Detect if the browser supports WebGL or not.
     *
     * Reference: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/By_example/Detect_WebGL
     */
    function hasWebGLContext() {
        // Create canvas element. The canvas is not added to the
        // document itself, so it is never displayed in the
        // browser window.
        const canvas = document.createElement('canvas');
        // Get WebGLRenderingContext from canvas element.
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        // Report the result.
        try {
            return gl instanceof WebGLRenderingContext;
        }
        catch (error) {
            return false;
        }
    }
    function addRenderer(term) {
        let renderer = new Renderer_();
        term.loadAddon(renderer);
        if (supportWebGL) {
            renderer.onContextLoss(event => {
                console.debug('WebGL context lost - reinitialize Xtermjs renderer.');
                renderer.dispose();
                // If the Webgl context is lost, reinitialize the addon
                addRenderer(term);
            });
        }
    }
    /**
     * Create a xterm.js terminal asynchronously.
     */
    async function createTerminal(options) {
        var _a;
        if (!Xterm_) {
            supportWebGL = hasWebGLContext();
            const [xterm_, fitAddon_, renderer_, weblinksAddon_] = await Promise.all([
                __webpack_require__.e(/*! import() */ "vendors-node_modules_xterm_lib_xterm_js").then(__webpack_require__.t.bind(__webpack_require__, /*! xterm */ "../node_modules/xterm/lib/xterm.js", 23)),
                __webpack_require__.e(/*! import() */ "node_modules_xterm-addon-fit_lib_xterm-addon-fit_js").then(__webpack_require__.t.bind(__webpack_require__, /*! xterm-addon-fit */ "../node_modules/xterm-addon-fit/lib/xterm-addon-fit.js", 23)),
                supportWebGL
                    ? __webpack_require__.e(/*! import() */ "vendors-node_modules_xterm-addon-webgl_lib_xterm-addon-webgl_js").then(__webpack_require__.t.bind(__webpack_require__, /*! xterm-addon-webgl */ "../node_modules/xterm-addon-webgl/lib/xterm-addon-webgl.js", 23))
                    : __webpack_require__.e(/*! import() */ "vendors-node_modules_xterm-addon-canvas_lib_xterm-addon-canvas_js").then(__webpack_require__.t.bind(__webpack_require__, /*! xterm-addon-canvas */ "../node_modules/xterm-addon-canvas/lib/xterm-addon-canvas.js", 23)),
                __webpack_require__.e(/*! import() */ "node_modules_xterm-addon-web-links_lib_xterm-addon-web-links_js").then(__webpack_require__.t.bind(__webpack_require__, /*! xterm-addon-web-links */ "../node_modules/xterm-addon-web-links/lib/xterm-addon-web-links.js", 23))
            ]);
            Xterm_ = xterm_.Terminal;
            FitAddon_ = fitAddon_.FitAddon;
            Renderer_ =
                (_a = renderer_.WebglAddon) !== null && _a !== void 0 ? _a : renderer_.CanvasAddon;
            WeblinksAddon_ = weblinksAddon_.WebLinksAddon;
        }
        const term = new Xterm_(options);
        addRenderer(term);
        const fitAddon = new FitAddon_();
        term.loadAddon(fitAddon);
        term.loadAddon(new WeblinksAddon_());
        return [term, fitAddon];
    }
    Private.createTerminal = createTerminal;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdGVybWluYWxfbGliX2luZGV4X2pzLmU5YjM2ZmIxMjdhYzYxODcxOTFlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFFc0I7QUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUnpCLDBDQUEwQztBQUMxQywyREFBMkQ7QUFJakI7QUFTMUM7O0dBRUc7QUFDSSxNQUFNLGdCQUFnQixHQUFHLElBQUksb0RBQUssQ0FDdkMsdUNBQXVDLEVBQ3ZDOzs4QkFFNEIsQ0FDN0IsQ0FBQztBQUVGOzs7R0FHRztBQUNJLElBQVUsU0FBUyxDQWlKekI7QUFqSkQsV0FBaUIsU0FBUztJQThHeEI7O09BRUc7SUFDVSx3QkFBYyxHQUFhO1FBQ3RDLEtBQUssRUFBRSxTQUFTO1FBQ2hCLFVBQVUsRUFBRSxnREFBZ0Q7UUFDNUQsUUFBUSxFQUFFLEVBQUU7UUFDWixVQUFVLEVBQUUsR0FBRztRQUNmLFVBQVUsRUFBRSxJQUFJO1FBQ2hCLGVBQWUsRUFBRSxLQUFLO1FBQ3RCLFdBQVcsRUFBRSxJQUFJO1FBQ2pCLFdBQVcsRUFBRSxJQUFJO1FBQ2pCLGNBQWMsRUFBRSxFQUFFO1FBQ2xCLGdCQUFnQixFQUFFLEtBQUs7UUFDdkIsY0FBYyxFQUFFLElBQUk7UUFDcEIsT0FBTyxFQUFFLElBQUk7UUFDYixlQUFlLEVBQUUsS0FBSztLQUN2QixDQUFDO0FBa0JKLENBQUMsRUFqSmdCLFNBQVMsS0FBVCxTQUFTLFFBaUp6Qjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUM3S0QsMENBQTBDO0FBQzFDLDJEQUEyRDtBQU8xQjtBQUNtQjtBQUNSO0FBQ2E7QUFDaEI7QUFVWDtBQUU5Qjs7R0FFRztBQUNILE1BQU0sY0FBYyxHQUFHLGFBQWEsQ0FBQztBQUVyQzs7R0FFRztBQUNILE1BQU0sbUJBQW1CLEdBQUcsa0JBQWtCLENBQUM7QUFFL0M7O0dBRUc7QUFDSSxNQUFNLFFBQVMsU0FBUSxtREFB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U0FBUyxDQUFDLFFBQVEsQ0FBQztZQUMvQixTQUFTO2dCQUNQLE1BQUMsU0FBaUIsQ0FBQyxVQUFVLG1DQUFLLFNBQWlCLENBQUMsV0FBVyxDQUFDO1lBQ2xFLGNBQWMsR0FBRyxjQUFjLENBQUMsYUFBYSxDQUFDO1NBQy9DO1FBRUQsTUFBTSxJQUFJLEdBQUcsSUFBSSxNQUFNLENBQUMsT0FBTyxDQUFDLENBQUM7UUFDakMsV0FBVyxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ2xCLE1BQU0sUUFBUSxHQUFHLElBQUksU0FBUyxFQUFFLENBQUM7UUFDakMsSUFBSSxDQUFDLFNBQVMsQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUN6QixJQUFJLENBQUMsU0FBUyxDQUFDLElBQUksY0FBYyxFQUFFLENBQUMsQ0FBQztRQUNyQyxPQUFPLENBQUMsSUFBSSxFQUFFLFFBQVEsQ0FBQyxDQUFDO0lBQzFCLENBQUM7SUExQnFCLHNCQUFjLGlCQTBCbkM7QUFDSCxDQUFDLEVBekVTLE9BQU8sS0FBUCxPQUFPLFFBeUVoQiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90ZXJtaW5hbC9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3Rlcm1pbmFsL3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3Rlcm1pbmFsL3NyYy93aWRnZXQudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdGVybWluYWxcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG5leHBvcnQgKiBmcm9tICcuL3dpZGdldCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElXaWRnZXRUcmFja2VyLCBNYWluQXJlYVdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFRlcm1pbmFsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgZWRpdG9yIHdpZGdldHMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVRlcm1pbmFsVHJhY2tlclxuICBleHRlbmRzIElXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PElUZXJtaW5hbC5JVGVybWluYWw+PiB7fVxuXG4vKipcbiAqIFRoZSBlZGl0b3IgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElUZXJtaW5hbFRyYWNrZXIgPSBuZXcgVG9rZW48SVRlcm1pbmFsVHJhY2tlcj4oXG4gICdAanVweXRlcmxhYi90ZXJtaW5hbDpJVGVybWluYWxUcmFja2VyJyxcbiAgYEEgd2lkZ2V0IHRyYWNrZXIgZm9yIHRlcm1pbmFscy5cbiAgVXNlIHRoaXMgaWYgeW91IHdhbnQgdG8gYmUgYWJsZSB0byBpdGVyYXRlIG92ZXIgYW5kIGludGVyYWN0IHdpdGggdGVybWluYWxzXG4gIGNyZWF0ZWQgYnkgdGhlIGFwcGxpY2F0aW9uLmBcbik7XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgdGVybWluYWxzLiBTZXBhcmF0ZWQgZnJvbSB0aGUgd2lkZ2V0IHNvIGl0IGNhbiBiZSBsYXp5XG4gKiBsb2FkZWQuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVRlcm1pbmFsIHtcbiAgZXhwb3J0IGludGVyZmFjZSBJVGVybWluYWwgZXh0ZW5kcyBXaWRnZXQge1xuICAgIC8qKlxuICAgICAqIFRoZSB0ZXJtaW5hbCBzZXNzaW9uIGFzc29jaWF0ZWQgd2l0aCB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIHNlc3Npb246IFRlcm1pbmFsLklUZXJtaW5hbENvbm5lY3Rpb247XG5cbiAgICAvKipcbiAgICAgKiBHZXQgYSBjb25maWcgb3B0aW9uIGZvciB0aGUgdGVybWluYWwuXG4gICAgICovXG4gICAgZ2V0T3B0aW9uPEsgZXh0ZW5kcyBrZXlvZiBJT3B0aW9ucz4ob3B0aW9uOiBLKTogSU9wdGlvbnNbS107XG5cbiAgICAvKipcbiAgICAgKiBTZXQgYSBjb25maWcgb3B0aW9uIGZvciB0aGUgdGVybWluYWwuXG4gICAgICovXG4gICAgc2V0T3B0aW9uPEsgZXh0ZW5kcyBrZXlvZiBJT3B0aW9ucz4ob3B0aW9uOiBLLCB2YWx1ZTogSU9wdGlvbnNbS10pOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogUmVmcmVzaCB0aGUgdGVybWluYWwgc2Vzc2lvbi5cbiAgICAgKi9cbiAgICByZWZyZXNoKCk6IFByb21pc2U8dm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBDaGVjayBpZiB0ZXJtaW5hbCBoYXMgYW55IHRleHQgc2VsZWN0ZWQuXG4gICAgICovXG4gICAgaGFzU2VsZWN0aW9uKCk6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBQYXN0ZSB0ZXh0IGludG8gdGVybWluYWwuXG4gICAgICovXG4gICAgcGFzdGUoZGF0YTogc3RyaW5nKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIEdldCBzZWxlY3RlZCB0ZXh0IGZyb20gdGVybWluYWwuXG4gICAgICovXG4gICAgZ2V0U2VsZWN0aW9uKCk6IHN0cmluZyB8IG51bGw7XG4gIH1cbiAgLyoqXG4gICAqIE9wdGlvbnMgZm9yIHRoZSB0ZXJtaW5hbCB3aWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZm9udCBmYW1pbHkgdXNlZCB0byByZW5kZXIgdGV4dC5cbiAgICAgKi9cbiAgICBmb250RmFtaWx5Pzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGZvbnQgc2l6ZSBvZiB0aGUgdGVybWluYWwgaW4gcGl4ZWxzLlxuICAgICAqL1xuICAgIGZvbnRTaXplOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbGluZSBoZWlnaHQgdXNlZCB0byByZW5kZXIgdGV4dC5cbiAgICAgKi9cbiAgICBsaW5lSGVpZ2h0PzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHRoZW1lIG9mIHRoZSB0ZXJtaW5hbC5cbiAgICAgKi9cbiAgICB0aGVtZTogVGhlbWU7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYW1vdW50IG9mIGJ1ZmZlciBzY3JvbGxiYWNrIHRvIGJlIHVzZWRcbiAgICAgKiB3aXRoIHRoZSB0ZXJtaW5hbFxuICAgICAqL1xuICAgIHNjcm9sbGJhY2s/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIHNodXQgZG93biB0aGUgc2Vzc2lvbiB3aGVuIGNsb3NpbmcgYSB0ZXJtaW5hbCBvciBub3QuXG4gICAgICovXG4gICAgc2h1dGRvd25PbkNsb3NlOiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBjbG9zZSB0aGUgd2lkZ2V0IHdoZW4gZXhpdGluZyBhIHRlcm1pbmFsIG9yIG5vdC5cbiAgICAgKi9cbiAgICBjbG9zZU9uRXhpdDogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gYmxpbmsgdGhlIGN1cnNvci4gIENhbiBvbmx5IGJlIHNldCBhdCBzdGFydHVwLlxuICAgICAqL1xuICAgIGN1cnNvckJsaW5rOiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogQW4gb3B0aW9uYWwgY29tbWFuZCB0byBydW4gd2hlbiB0aGUgc2Vzc2lvbiBzdGFydHMuXG4gICAgICovXG4gICAgaW5pdGlhbENvbW1hbmQ6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gZW5hYmxlIHNjcmVlbiByZWFkZXIgc3VwcG9ydC5cbiAgICAgKi9cbiAgICBzY3JlZW5SZWFkZXJNb2RlOiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBlbmFibGUgdXNpbmcgQ3RybCtWIHRvIHBhc3RlLlxuICAgICAqXG4gICAgICogVGhpcyBzZXR0aW5nIGhhcyBubyBlZmZlY3Qgb24gbWFjT1MsIHdoZXJlIENtZCtWIGlzIGF2YWlsYWJsZS5cbiAgICAgKi9cbiAgICBwYXN0ZVdpdGhDdHJsVjogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gYXV0by1maXQgdGhlIHRlcm1pbmFsIHRvIGl0cyBob3N0IGVsZW1lbnQgc2l6ZS5cbiAgICAgKi9cbiAgICBhdXRvRml0PzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRyZWF0IG9wdGlvbiBhcyBtZXRhIGtleSBvbiBtYWNPUy5cbiAgICAgKi9cbiAgICBtYWNPcHRpb25Jc01ldGE/OiBib29sZWFuO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IG9wdGlvbnMgdXNlZCBmb3IgY3JlYXRpbmcgdGVybWluYWxzLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGRlZmF1bHRPcHRpb25zOiBJT3B0aW9ucyA9IHtcbiAgICB0aGVtZTogJ2luaGVyaXQnLFxuICAgIGZvbnRGYW1pbHk6ICdNZW5sbywgQ29uc29sYXMsIFwiRGVqYVZ1IFNhbnMgTW9ub1wiLCBtb25vc3BhY2UnLFxuICAgIGZvbnRTaXplOiAxMyxcbiAgICBsaW5lSGVpZ2h0OiAxLjAsXG4gICAgc2Nyb2xsYmFjazogMTAwMCxcbiAgICBzaHV0ZG93bk9uQ2xvc2U6IGZhbHNlLFxuICAgIGNsb3NlT25FeGl0OiB0cnVlLFxuICAgIGN1cnNvckJsaW5rOiB0cnVlLFxuICAgIGluaXRpYWxDb21tYW5kOiAnJyxcbiAgICBzY3JlZW5SZWFkZXJNb2RlOiBmYWxzZSwgLy8gRmFsc2UgYnkgZGVmYXVsdCwgY2FuIGNhdXNlIHNjcm9sbGJhciBtb3VzZSBpbnRlcmFjdGlvbiBpc3N1ZXMuXG4gICAgcGFzdGVXaXRoQ3RybFY6IHRydWUsXG4gICAgYXV0b0ZpdDogdHJ1ZSxcbiAgICBtYWNPcHRpb25Jc01ldGE6IGZhbHNlXG4gIH07XG5cbiAgLyoqXG4gICAqIEEgdHlwZSBmb3IgdGhlIHRlcm1pbmFsIHRoZW1lLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgVGhlbWUgPSAnbGlnaHQnIHwgJ2RhcmsnIHwgJ2luaGVyaXQnO1xuXG4gIC8qKlxuICAgKiBBIHR5cGUgZm9yIHRoZSB0ZXJtaW5hbCB0aGVtZS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVRoZW1lT2JqZWN0IHtcbiAgICBmb3JlZ3JvdW5kOiBzdHJpbmc7XG4gICAgYmFja2dyb3VuZDogc3RyaW5nO1xuICAgIGN1cnNvcjogc3RyaW5nO1xuICAgIGN1cnNvckFjY2VudDogc3RyaW5nO1xuICAgIHNlbGVjdGlvbkJhY2tncm91bmQ6IHN0cmluZztcbiAgICBzZWxlY3Rpb25JbmFjdGl2ZUJhY2tncm91bmQ6IHN0cmluZztcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUZXJtaW5hbCBhcyBUZXJtaW5hbE5TIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBQcm9taXNlRGVsZWdhdGUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBQbGF0Zm9ybSB9IGZyb20gJ0BsdW1pbm8vZG9tdXRpbHMnO1xuaW1wb3J0IHsgTWVzc2FnZSwgTWVzc2FnZUxvb3AgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0IHR5cGUge1xuICBJVGVybWluYWxJbml0T25seU9wdGlvbnMsXG4gIElUZXJtaW5hbE9wdGlvbnMsXG4gIFRlcm1pbmFsIGFzIFh0ZXJtXG59IGZyb20gJ3h0ZXJtJztcbmltcG9ydCB0eXBlIHsgQ2FudmFzQWRkb24gfSBmcm9tICd4dGVybS1hZGRvbi1jYW52YXMnO1xuaW1wb3J0IHR5cGUgeyBGaXRBZGRvbiB9IGZyb20gJ3h0ZXJtLWFkZG9uLWZpdCc7XG5pbXBvcnQgdHlwZSB7IFdlYkxpbmtzQWRkb24gfSBmcm9tICd4dGVybS1hZGRvbi13ZWItbGlua3MnO1xuaW1wb3J0IHR5cGUgeyBXZWJnbEFkZG9uIH0gZnJvbSAneHRlcm0tYWRkb24td2ViZ2wnO1xuaW1wb3J0IHsgSVRlcm1pbmFsIH0gZnJvbSAnLic7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYSB0ZXJtaW5hbCB3aWRnZXQuXG4gKi9cbmNvbnN0IFRFUk1JTkFMX0NMQVNTID0gJ2pwLVRlcm1pbmFsJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIHRlcm1pbmFsIGJvZHkuXG4gKi9cbmNvbnN0IFRFUk1JTkFMX0JPRFlfQ0xBU1MgPSAnanAtVGVybWluYWwtYm9keSc7XG5cbi8qKlxuICogQSB3aWRnZXQgd2hpY2ggbWFuYWdlcyBhIHRlcm1pbmFsIHNlc3Npb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBUZXJtaW5hbCBleHRlbmRzIFdpZGdldCBpbXBsZW1lbnRzIElUZXJtaW5hbC5JVGVybWluYWwge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IHRlcm1pbmFsIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIHNlc3Npb24gLSBUaGUgdGVybWluYWwgc2Vzc2lvbiBvYmplY3QuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIHRlcm1pbmFsIGNvbmZpZ3VyYXRpb24gb3B0aW9ucy5cbiAgICpcbiAgICogQHBhcmFtIHRyYW5zbGF0b3IgLSBUaGUgbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKFxuICAgIHNlc3Npb246IFRlcm1pbmFsTlMuSVRlcm1pbmFsQ29ubmVjdGlvbixcbiAgICBvcHRpb25zOiBQYXJ0aWFsPElUZXJtaW5hbC5JT3B0aW9ucz4gPSB7fSxcbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3JcbiAgKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIHRoaXMuc2Vzc2lvbiA9IHNlc3Npb247XG5cbiAgICAvLyBJbml0aWFsaXplIHNldHRpbmdzLlxuICAgIHRoaXMuX29wdGlvbnMgPSB7IC4uLklUZXJtaW5hbC5kZWZhdWx0T3B0aW9ucywgLi4ub3B0aW9ucyB9O1xuXG4gICAgY29uc3QgeyB0aGVtZSwgLi4ub3RoZXIgfSA9IHRoaXMuX29wdGlvbnM7XG4gICAgY29uc3QgeHRlcm1PcHRpb25zID0ge1xuICAgICAgdGhlbWU6IFByaXZhdGUuZ2V0WFRlcm1UaGVtZSh0aGVtZSksXG4gICAgICAuLi5vdGhlclxuICAgIH07XG5cbiAgICB0aGlzLmFkZENsYXNzKFRFUk1JTkFMX0NMQVNTKTtcblxuICAgIHRoaXMuX3NldFRoZW1lQXR0cmlidXRlKHRoZW1lKTtcblxuICAgIC8vIEJ1ZmZlciBzZXNzaW9uIG1lc3NhZ2Ugd2hpbGUgd2FpdGluZyBmb3IgdGhlIHRlcm1pbmFsXG4gICAgbGV0IGJ1ZmZlciA9ICcnO1xuICAgIGNvbnN0IGJ1ZmZlck1lc3NhZ2UgPSAoXG4gICAgICBzZW5kZXI6IFRlcm1pbmFsTlMuSVRlcm1pbmFsQ29ubmVjdGlvbixcbiAgICAgIG1zZzogVGVybWluYWxOUy5JTWVzc2FnZVxuICAgICk6IHZvaWQgPT4ge1xuICAgICAgc3dpdGNoIChtc2cudHlwZSkge1xuICAgICAgICBjYXNlICdzdGRvdXQnOlxuICAgICAgICAgIGlmIChtc2cuY29udGVudCkge1xuICAgICAgICAgICAgYnVmZmVyICs9IG1zZy5jb250ZW50WzBdIGFzIHN0cmluZztcbiAgICAgICAgICB9XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgYnJlYWs7XG4gICAgICB9XG4gICAgfTtcbiAgICBzZXNzaW9uLm1lc3NhZ2VSZWNlaXZlZC5jb25uZWN0KGJ1ZmZlck1lc3NhZ2UpO1xuICAgIHNlc3Npb24uZGlzcG9zZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICBpZiAodGhpcy5nZXRPcHRpb24oJ2Nsb3NlT25FeGl0JykpIHtcbiAgICAgICAgdGhpcy5kaXNwb3NlKCk7XG4gICAgICB9XG4gICAgfSwgdGhpcyk7XG5cbiAgICAvLyBDcmVhdGUgdGhlIHh0ZXJtLlxuICAgIFByaXZhdGUuY3JlYXRlVGVybWluYWwoeHRlcm1PcHRpb25zKVxuICAgICAgLnRoZW4oKFt0ZXJtLCBmaXRBZGRvbl0pID0+IHtcbiAgICAgICAgdGhpcy5fdGVybSA9IHRlcm07XG4gICAgICAgIHRoaXMuX2ZpdEFkZG9uID0gZml0QWRkb247XG4gICAgICAgIHRoaXMuX2luaXRpYWxpemVUZXJtKCk7XG5cbiAgICAgICAgdGhpcy5pZCA9IGBqcC1UZXJtaW5hbC0ke1ByaXZhdGUuaWQrK31gO1xuICAgICAgICB0aGlzLnRpdGxlLmxhYmVsID0gdGhpcy5fdHJhbnMuX18oJ1Rlcm1pbmFsJyk7XG4gICAgICAgIHRoaXMuX2lzUmVhZHkgPSB0cnVlO1xuICAgICAgICB0aGlzLl9yZWFkeS5yZXNvbHZlKCk7XG5cbiAgICAgICAgaWYgKGJ1ZmZlcikge1xuICAgICAgICAgIHRoaXMuX3Rlcm0ud3JpdGUoYnVmZmVyKTtcbiAgICAgICAgfVxuICAgICAgICBzZXNzaW9uLm1lc3NhZ2VSZWNlaXZlZC5kaXNjb25uZWN0KGJ1ZmZlck1lc3NhZ2UpO1xuICAgICAgICBzZXNzaW9uLm1lc3NhZ2VSZWNlaXZlZC5jb25uZWN0KHRoaXMuX29uTWVzc2FnZSwgdGhpcyk7XG5cbiAgICAgICAgaWYgKHNlc3Npb24uY29ubmVjdGlvblN0YXR1cyA9PT0gJ2Nvbm5lY3RlZCcpIHtcbiAgICAgICAgICB0aGlzLl9pbml0aWFsQ29ubmVjdGlvbigpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIHNlc3Npb24uY29ubmVjdGlvblN0YXR1c0NoYW5nZWQuY29ubmVjdChcbiAgICAgICAgICAgIHRoaXMuX2luaXRpYWxDb25uZWN0aW9uLFxuICAgICAgICAgICAgdGhpc1xuICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcignRmFpbGVkIHRvIGNyZWF0ZSBhIHRlcm1pbmFsLlxcbicsIHJlYXNvbik7XG4gICAgICAgIHRoaXMuX3JlYWR5LnJlamVjdChyZWFzb24pO1xuICAgICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogQSBwcm9taXNlIHRoYXQgaXMgZnVsZmlsbGVkIHdoZW4gdGhlIHRlcm1pbmFsIGlzIHJlYWR5LlxuICAgKi9cbiAgZ2V0IHJlYWR5KCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9yZWFkeS5wcm9taXNlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSB0ZXJtaW5hbCBzZXNzaW9uIGFzc29jaWF0ZWQgd2l0aCB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcmVhZG9ubHkgc2Vzc2lvbjogVGVybWluYWxOUy5JVGVybWluYWxDb25uZWN0aW9uO1xuXG4gIC8qKlxuICAgKiBHZXQgYSBjb25maWcgb3B0aW9uIGZvciB0aGUgdGVybWluYWwuXG4gICAqL1xuICBnZXRPcHRpb248SyBleHRlbmRzIGtleW9mIElUZXJtaW5hbC5JT3B0aW9ucz4oXG4gICAgb3B0aW9uOiBLXG4gICk6IElUZXJtaW5hbC5JT3B0aW9uc1tLXSB7XG4gICAgcmV0dXJuIHRoaXMuX29wdGlvbnNbb3B0aW9uXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgYSBjb25maWcgb3B0aW9uIGZvciB0aGUgdGVybWluYWwuXG4gICAqL1xuICBzZXRPcHRpb248SyBleHRlbmRzIGtleW9mIElUZXJtaW5hbC5JT3B0aW9ucz4oXG4gICAgb3B0aW9uOiBLLFxuICAgIHZhbHVlOiBJVGVybWluYWwuSU9wdGlvbnNbS11cbiAgKTogdm9pZCB7XG4gICAgaWYgKFxuICAgICAgb3B0aW9uICE9PSAndGhlbWUnICYmXG4gICAgICAodGhpcy5fb3B0aW9uc1tvcHRpb25dID09PSB2YWx1ZSB8fCBvcHRpb24gPT09ICdpbml0aWFsQ29tbWFuZCcpXG4gICAgKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgdGhpcy5fb3B0aW9uc1tvcHRpb25dID0gdmFsdWU7XG5cbiAgICBzd2l0Y2ggKG9wdGlvbikge1xuICAgICAgY2FzZSAnZm9udEZhbWlseSc6XG4gICAgICAgIHRoaXMuX3Rlcm0ub3B0aW9ucy5mb250RmFtaWx5ID0gdmFsdWUgYXMgc3RyaW5nIHwgdW5kZWZpbmVkO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2ZvbnRTaXplJzpcbiAgICAgICAgdGhpcy5fdGVybS5vcHRpb25zLmZvbnRTaXplID0gdmFsdWUgYXMgbnVtYmVyIHwgdW5kZWZpbmVkO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2xpbmVIZWlnaHQnOlxuICAgICAgICB0aGlzLl90ZXJtLm9wdGlvbnMubGluZUhlaWdodCA9IHZhbHVlIGFzIG51bWJlciB8IHVuZGVmaW5lZDtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdzY3JlZW5SZWFkZXJNb2RlJzpcbiAgICAgICAgdGhpcy5fdGVybS5vcHRpb25zLnNjcmVlblJlYWRlck1vZGUgPSB2YWx1ZSBhcyBib29sZWFuIHwgdW5kZWZpbmVkO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3Njcm9sbGJhY2snOlxuICAgICAgICB0aGlzLl90ZXJtLm9wdGlvbnMuc2Nyb2xsYmFjayA9IHZhbHVlIGFzIG51bWJlciB8IHVuZGVmaW5lZDtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICd0aGVtZSc6XG4gICAgICAgIHRoaXMuX3Rlcm0ub3B0aW9ucy50aGVtZSA9IHtcbiAgICAgICAgICAuLi5Qcml2YXRlLmdldFhUZXJtVGhlbWUodmFsdWUgYXMgSVRlcm1pbmFsLlRoZW1lKVxuICAgICAgICB9O1xuICAgICAgICB0aGlzLl9zZXRUaGVtZUF0dHJpYnV0ZSh2YWx1ZSBhcyBJVGVybWluYWwuVGhlbWUpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ21hY09wdGlvbklzTWV0YSc6XG4gICAgICAgIHRoaXMuX3Rlcm0ub3B0aW9ucy5tYWNPcHRpb25Jc01ldGEgPSB2YWx1ZSBhcyBib29sZWFuIHwgdW5kZWZpbmVkO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIC8vIERvIG5vdCB0cmFuc21pdCBvcHRpb25zIG5vdCBsaXN0ZWQgYWJvdmUgdG8gWFRlcm1cbiAgICAgICAgYnJlYWs7XG4gICAgfVxuXG4gICAgdGhpcy5fbmVlZHNSZXNpemUgPSB0cnVlO1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHRlcm1pbmFsIHdpZGdldC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLnNlc3Npb24uaXNEaXNwb3NlZCkge1xuICAgICAgaWYgKHRoaXMuZ2V0T3B0aW9uKCdzaHV0ZG93bk9uQ2xvc2UnKSkge1xuICAgICAgICB0aGlzLnNlc3Npb24uc2h1dGRvd24oKS5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYFRlcm1pbmFsIG5vdCBzaHV0IGRvd246ICR7cmVhc29ufWApO1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9XG4gICAgdm9pZCB0aGlzLnJlYWR5LnRoZW4oKCkgPT4ge1xuICAgICAgdGhpcy5fdGVybS5kaXNwb3NlKCk7XG4gICAgfSk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlZnJlc2ggdGhlIHRlcm1pbmFsIHNlc3Npb24uXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogRmFpbHVyZSB0byByZWNvbm5lY3QgdG8gdGhlIHNlc3Npb24gc2hvdWxkIGJlIGNhdWdodCBhcHByb3ByaWF0ZWx5XG4gICAqL1xuICBhc3luYyByZWZyZXNoKCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGlmICghdGhpcy5pc0Rpc3Bvc2VkICYmIHRoaXMuX2lzUmVhZHkpIHtcbiAgICAgIGF3YWl0IHRoaXMuc2Vzc2lvbi5yZWNvbm5lY3QoKTtcbiAgICAgIHRoaXMuX3Rlcm0uY2xlYXIoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ2hlY2sgaWYgdGVybWluYWwgaGFzIGFueSB0ZXh0IHNlbGVjdGVkLlxuICAgKi9cbiAgaGFzU2VsZWN0aW9uKCk6IGJvb2xlYW4ge1xuICAgIGlmICghdGhpcy5pc0Rpc3Bvc2VkICYmIHRoaXMuX2lzUmVhZHkpIHtcbiAgICAgIHJldHVybiB0aGlzLl90ZXJtLmhhc1NlbGVjdGlvbigpO1xuICAgIH1cbiAgICByZXR1cm4gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogUGFzdGUgdGV4dCBpbnRvIHRlcm1pbmFsLlxuICAgKi9cbiAgcGFzdGUoZGF0YTogc3RyaW5nKTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLmlzRGlzcG9zZWQgJiYgdGhpcy5faXNSZWFkeSkge1xuICAgICAgcmV0dXJuIHRoaXMuX3Rlcm0ucGFzdGUoZGF0YSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEdldCBzZWxlY3RlZCB0ZXh0IGZyb20gdGVybWluYWwuXG4gICAqL1xuICBnZXRTZWxlY3Rpb24oKTogc3RyaW5nIHwgbnVsbCB7XG4gICAgaWYgKCF0aGlzLmlzRGlzcG9zZWQgJiYgdGhpcy5faXNSZWFkeSkge1xuICAgICAgcmV0dXJuIHRoaXMuX3Rlcm0uZ2V0U2VsZWN0aW9uKCk7XG4gICAgfVxuICAgIHJldHVybiBudWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIFByb2Nlc3MgYSBtZXNzYWdlIHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIG1zZyAtIFRoZSBtZXNzYWdlIHNlbnQgdG8gdGhlIHdpZGdldC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBTdWJjbGFzc2VzIG1heSByZWltcGxlbWVudCB0aGlzIG1ldGhvZCBhcyBuZWVkZWQuXG4gICAqL1xuICBwcm9jZXNzTWVzc2FnZShtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBzdXBlci5wcm9jZXNzTWVzc2FnZShtc2cpO1xuICAgIHN3aXRjaCAobXNnLnR5cGUpIHtcbiAgICAgIGNhc2UgJ2ZpdC1yZXF1ZXN0JzpcbiAgICAgICAgdGhpcy5vbkZpdFJlcXVlc3QobXNnKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBzaXplIG9mIHRoZSB0ZXJtaW5hbCB3aGVuIGF0dGFjaGVkIGlmIGRpcnR5LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHNpemUgb2YgdGhlIHRlcm1pbmFsIHdoZW4gc2hvd24gaWYgZGlydHkuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlclNob3cobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBPbiByZXNpemUsIHVzZSB0aGUgY29tcHV0ZWQgcm93IGFuZCBjb2x1bW4gc2l6ZXMgdG8gcmVzaXplIHRoZSB0ZXJtaW5hbC5cbiAgICovXG4gIHByb3RlY3RlZCBvblJlc2l6ZShtc2c6IFdpZGdldC5SZXNpemVNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fb2Zmc2V0V2lkdGggPSBtc2cud2lkdGg7XG4gICAgdGhpcy5fb2Zmc2V0SGVpZ2h0ID0gbXNnLmhlaWdodDtcbiAgICB0aGlzLl9uZWVkc1Jlc2l6ZSA9IHRydWU7XG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIG1lc3NhZ2UgaGFuZGxlciBpbnZva2VkIG9uIGFuIGAndXBkYXRlLXJlcXVlc3QnYCBtZXNzYWdlLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uVXBkYXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAoIXRoaXMuaXNWaXNpYmxlIHx8ICF0aGlzLmlzQXR0YWNoZWQgfHwgIXRoaXMuX2lzUmVhZHkpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBPcGVuIHRoZSB0ZXJtaW5hbCBpZiBuZWNlc3NhcnkuXG4gICAgaWYgKCF0aGlzLl90ZXJtT3BlbmVkKSB7XG4gICAgICB0aGlzLl90ZXJtLm9wZW4odGhpcy5ub2RlKTtcbiAgICAgIHRoaXMuX3Rlcm0uZWxlbWVudD8uY2xhc3NMaXN0LmFkZChURVJNSU5BTF9CT0RZX0NMQVNTKTtcbiAgICAgIHRoaXMuX3Rlcm1PcGVuZWQgPSB0cnVlO1xuICAgIH1cblxuICAgIGlmICh0aGlzLl9uZWVkc1Jlc2l6ZSkge1xuICAgICAgdGhpcy5fcmVzaXplVGVybWluYWwoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBtZXNzYWdlIGhhbmRsZXIgaW52b2tlZCBvbiBhbiBgJ2ZpdC1yZXF1ZXN0J2AgbWVzc2FnZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkZpdFJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgY29uc3QgcmVzaXplID0gV2lkZ2V0LlJlc2l6ZU1lc3NhZ2UuVW5rbm93blNpemU7XG4gICAgTWVzc2FnZUxvb3Auc2VuZE1lc3NhZ2UodGhpcywgcmVzaXplKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhY3RpdmF0ZS1yZXF1ZXN0J2AgbWVzc2FnZXMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fdGVybT8uZm9jdXMoKTtcbiAgfVxuXG4gIHByaXZhdGUgX2luaXRpYWxDb25uZWN0aW9uKCkge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBpZiAodGhpcy5zZXNzaW9uLmNvbm5lY3Rpb25TdGF0dXMgIT09ICdjb25uZWN0ZWQnKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgdGhpcy50aXRsZS5sYWJlbCA9IHRoaXMuX3RyYW5zLl9fKCdUZXJtaW5hbCAlMScsIHRoaXMuc2Vzc2lvbi5uYW1lKTtcbiAgICB0aGlzLl9zZXRTZXNzaW9uU2l6ZSgpO1xuICAgIGlmICh0aGlzLl9vcHRpb25zLmluaXRpYWxDb21tYW5kKSB7XG4gICAgICB0aGlzLnNlc3Npb24uc2VuZCh7XG4gICAgICAgIHR5cGU6ICdzdGRpbicsXG4gICAgICAgIGNvbnRlbnQ6IFt0aGlzLl9vcHRpb25zLmluaXRpYWxDb21tYW5kICsgJ1xcciddXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvLyBPbmx5IHJ1biB0aGlzIGluaXRpYWwgY29ubmVjdGlvbiBsb2dpYyBvbmNlLlxuICAgIHRoaXMuc2Vzc2lvbi5jb25uZWN0aW9uU3RhdHVzQ2hhbmdlZC5kaXNjb25uZWN0KFxuICAgICAgdGhpcy5faW5pdGlhbENvbm5lY3Rpb24sXG4gICAgICB0aGlzXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbml0aWFsaXplIHRoZSB0ZXJtaW5hbCBvYmplY3QuXG4gICAqL1xuICBwcml2YXRlIF9pbml0aWFsaXplVGVybSgpOiB2b2lkIHtcbiAgICBjb25zdCB0ZXJtID0gdGhpcy5fdGVybTtcbiAgICB0ZXJtLm9uRGF0YSgoZGF0YTogc3RyaW5nKSA9PiB7XG4gICAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRoaXMuc2Vzc2lvbi5zZW5kKHtcbiAgICAgICAgdHlwZTogJ3N0ZGluJyxcbiAgICAgICAgY29udGVudDogW2RhdGFdXG4gICAgICB9KTtcbiAgICB9KTtcblxuICAgIHRlcm0ub25UaXRsZUNoYW5nZSgodGl0bGU6IHN0cmluZykgPT4ge1xuICAgICAgdGhpcy50aXRsZS5sYWJlbCA9IHRpdGxlO1xuICAgIH0pO1xuXG4gICAgLy8gRG8gbm90IGFkZCBhbnkgQ3RybCtDL0N0cmwrViBoYW5kbGluZyBvbiBtYWNPUyxcbiAgICAvLyB3aGVyZSBDbWQrQy9DbWQrViB3b3JrcyBhcyBpbnRlbmRlZC5cbiAgICBpZiAoUGxhdGZvcm0uSVNfTUFDKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgdGVybS5hdHRhY2hDdXN0b21LZXlFdmVudEhhbmRsZXIoZXZlbnQgPT4ge1xuICAgICAgaWYgKGV2ZW50LmN0cmxLZXkgJiYgZXZlbnQua2V5ID09PSAnYycgJiYgdGVybS5oYXNTZWxlY3Rpb24oKSkge1xuICAgICAgICAvLyBSZXR1cm4gc28gdGhhdCB0aGUgdXN1YWwgT1MgY29weSBoYXBwZW5zXG4gICAgICAgIC8vIGluc3RlYWQgb2YgaW50ZXJydXB0IHNpZ25hbC5cbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuXG4gICAgICBpZiAoZXZlbnQuY3RybEtleSAmJiBldmVudC5rZXkgPT09ICd2JyAmJiB0aGlzLl9vcHRpb25zLnBhc3RlV2l0aEN0cmxWKSB7XG4gICAgICAgIC8vIFJldHVybiBzbyB0aGF0IHRoZSB1c3VhbCBwYXN0ZSBoYXBwZW5zLlxuICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIG1lc3NhZ2UgZnJvbSB0aGUgdGVybWluYWwgc2Vzc2lvbi5cbiAgICovXG4gIHByaXZhdGUgX29uTWVzc2FnZShcbiAgICBzZW5kZXI6IFRlcm1pbmFsTlMuSVRlcm1pbmFsQ29ubmVjdGlvbixcbiAgICBtc2c6IFRlcm1pbmFsTlMuSU1lc3NhZ2VcbiAgKTogdm9pZCB7XG4gICAgc3dpdGNoIChtc2cudHlwZSkge1xuICAgICAgY2FzZSAnc3Rkb3V0JzpcbiAgICAgICAgaWYgKG1zZy5jb250ZW50KSB7XG4gICAgICAgICAgdGhpcy5fdGVybS53cml0ZShtc2cuY29udGVudFswXSBhcyBzdHJpbmcpO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnZGlzY29ubmVjdCc6XG4gICAgICAgIHRoaXMuX3Rlcm0ud3JpdGUoJ1xcclxcblxcclxcbltGaW5pc2hlZOKApiBUZXJtIFNlc3Npb25dXFxyXFxuJyk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFJlc2l6ZSB0aGUgdGVybWluYWwgYmFzZWQgb24gY29tcHV0ZWQgZ2VvbWV0cnkuXG4gICAqL1xuICBwcml2YXRlIF9yZXNpemVUZXJtaW5hbCgpIHtcbiAgICBpZiAodGhpcy5fb3B0aW9ucy5hdXRvRml0KSB7XG4gICAgICB0aGlzLl9maXRBZGRvbi5maXQoKTtcbiAgICB9XG4gICAgaWYgKHRoaXMuX29mZnNldFdpZHRoID09PSAtMSkge1xuICAgICAgdGhpcy5fb2Zmc2V0V2lkdGggPSB0aGlzLm5vZGUub2Zmc2V0V2lkdGg7XG4gICAgfVxuICAgIGlmICh0aGlzLl9vZmZzZXRIZWlnaHQgPT09IC0xKSB7XG4gICAgICB0aGlzLl9vZmZzZXRIZWlnaHQgPSB0aGlzLm5vZGUub2Zmc2V0SGVpZ2h0O1xuICAgIH1cbiAgICB0aGlzLl9zZXRTZXNzaW9uU2l6ZSgpO1xuICAgIHRoaXMuX25lZWRzUmVzaXplID0gZmFsc2U7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBzaXplIG9mIHRoZSB0ZXJtaW5hbCBpbiB0aGUgc2Vzc2lvbi5cbiAgICovXG4gIHByaXZhdGUgX3NldFNlc3Npb25TaXplKCk6IHZvaWQge1xuICAgIGNvbnN0IGNvbnRlbnQgPSBbXG4gICAgICB0aGlzLl90ZXJtLnJvd3MsXG4gICAgICB0aGlzLl90ZXJtLmNvbHMsXG4gICAgICB0aGlzLl9vZmZzZXRIZWlnaHQsXG4gICAgICB0aGlzLl9vZmZzZXRXaWR0aFxuICAgIF07XG4gICAgaWYgKCF0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHRoaXMuc2Vzc2lvbi5zZW5kKHsgdHlwZTogJ3NldF9zaXplJywgY29udGVudCB9KTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9zZXRUaGVtZUF0dHJpYnV0ZSh0aGVtZTogc3RyaW5nIHwgbnVsbCB8IHVuZGVmaW5lZCkge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLm5vZGUuc2V0QXR0cmlidXRlKFxuICAgICAgJ2RhdGEtdGVybS10aGVtZScsXG4gICAgICB0aGVtZSA/IHRoZW1lLnRvTG93ZXJDYXNlKCkgOiAnaW5oZXJpdCdcbiAgICApO1xuICB9XG5cbiAgcHJpdmF0ZSBfZml0QWRkb246IEZpdEFkZG9uO1xuICBwcml2YXRlIF9uZWVkc1Jlc2l6ZSA9IHRydWU7XG4gIHByaXZhdGUgX29mZnNldFdpZHRoID0gLTE7XG4gIHByaXZhdGUgX29mZnNldEhlaWdodCA9IC0xO1xuICBwcml2YXRlIF9vcHRpb25zOiBJVGVybWluYWwuSU9wdGlvbnM7XG4gIHByaXZhdGUgX2lzUmVhZHkgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfcmVhZHkgPSBuZXcgUHJvbWlzZURlbGVnYXRlPHZvaWQ+KCk7XG4gIHByaXZhdGUgX3Rlcm06IFh0ZXJtO1xuICBwcml2YXRlIF90ZXJtT3BlbmVkID0gZmFsc2U7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBbiBpbmNyZW1lbnRpbmcgY291bnRlciBmb3IgaWRzLlxuICAgKi9cbiAgZXhwb3J0IGxldCBpZCA9IDA7XG5cbiAgLyoqXG4gICAqIFRoZSBsaWdodCB0ZXJtaW5hbCB0aGVtZS5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBsaWdodFRoZW1lOiBJVGVybWluYWwuSVRoZW1lT2JqZWN0ID0ge1xuICAgIGZvcmVncm91bmQ6ICcjMDAwJyxcbiAgICBiYWNrZ3JvdW5kOiAnI2ZmZicsXG4gICAgY3Vyc29yOiAnIzYxNjE2MScsIC8vIG1kLWdyZXktNzAwXG4gICAgY3Vyc29yQWNjZW50OiAnI0Y1RjVGNScsIC8vIG1kLWdyZXktMTAwXG4gICAgc2VsZWN0aW9uQmFja2dyb3VuZDogJ3JnYmEoOTcsIDk3LCA5NywgMC4zKScsIC8vIG1kLWdyZXktNzAwXG4gICAgc2VsZWN0aW9uSW5hY3RpdmVCYWNrZ3JvdW5kOiAncmdiYSgxODksIDE4OSwgMTg5LCAwLjMpJyAvLyBtZC1ncmV5LTQwMFxuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgZGFyayB0ZXJtaW5hbCB0aGVtZS5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBkYXJrVGhlbWU6IElUZXJtaW5hbC5JVGhlbWVPYmplY3QgPSB7XG4gICAgZm9yZWdyb3VuZDogJyNmZmYnLFxuICAgIGJhY2tncm91bmQ6ICcjMDAwJyxcbiAgICBjdXJzb3I6ICcjZmZmJyxcbiAgICBjdXJzb3JBY2NlbnQ6ICcjMDAwJyxcbiAgICBzZWxlY3Rpb25CYWNrZ3JvdW5kOiAncmdiYSgyNTUsIDI1NSwgMjU1LCAwLjMpJyxcbiAgICBzZWxlY3Rpb25JbmFjdGl2ZUJhY2tncm91bmQ6ICdyZ2JhKDIzOCwgMjM4LCAyMzgsIDAuMyknIC8vIG1kLWdyZXktMjAwXG4gIH07XG5cbiAgLyoqXG4gICAqIFRoZSBjdXJyZW50IHRoZW1lLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGluaGVyaXRUaGVtZSA9ICgpOiBJVGVybWluYWwuSVRoZW1lT2JqZWN0ID0+ICh7XG4gICAgZm9yZWdyb3VuZDogZ2V0Q29tcHV0ZWRTdHlsZShkb2N1bWVudC5ib2R5KVxuICAgICAgLmdldFByb3BlcnR5VmFsdWUoJy0tanAtdWktZm9udC1jb2xvcjAnKVxuICAgICAgLnRyaW0oKSxcbiAgICBiYWNrZ3JvdW5kOiBnZXRDb21wdXRlZFN0eWxlKGRvY3VtZW50LmJvZHkpXG4gICAgICAuZ2V0UHJvcGVydHlWYWx1ZSgnLS1qcC1sYXlvdXQtY29sb3IwJylcbiAgICAgIC50cmltKCksXG4gICAgY3Vyc29yOiBnZXRDb21wdXRlZFN0eWxlKGRvY3VtZW50LmJvZHkpXG4gICAgICAuZ2V0UHJvcGVydHlWYWx1ZSgnLS1qcC11aS1mb250LWNvbG9yMScpXG4gICAgICAudHJpbSgpLFxuICAgIGN1cnNvckFjY2VudDogZ2V0Q29tcHV0ZWRTdHlsZShkb2N1bWVudC5ib2R5KVxuICAgICAgLmdldFByb3BlcnR5VmFsdWUoJy0tanAtdWktaW52ZXJzZS1mb250LWNvbG9yMCcpXG4gICAgICAudHJpbSgpLFxuICAgIHNlbGVjdGlvbkJhY2tncm91bmQ6IGdldENvbXB1dGVkU3R5bGUoZG9jdW1lbnQuYm9keSlcbiAgICAgIC5nZXRQcm9wZXJ0eVZhbHVlKCctLWpwLWxheW91dC1jb2xvcjMnKVxuICAgICAgLnRyaW0oKSxcbiAgICBzZWxlY3Rpb25JbmFjdGl2ZUJhY2tncm91bmQ6IGdldENvbXB1dGVkU3R5bGUoZG9jdW1lbnQuYm9keSlcbiAgICAgIC5nZXRQcm9wZXJ0eVZhbHVlKCctLWpwLWxheW91dC1jb2xvcjInKVxuICAgICAgLnRyaW0oKVxuICB9KTtcblxuICBleHBvcnQgZnVuY3Rpb24gZ2V0WFRlcm1UaGVtZShcbiAgICB0aGVtZTogSVRlcm1pbmFsLlRoZW1lXG4gICk6IElUZXJtaW5hbC5JVGhlbWVPYmplY3Qge1xuICAgIHN3aXRjaCAodGhlbWUpIHtcbiAgICAgIGNhc2UgJ2xpZ2h0JzpcbiAgICAgICAgcmV0dXJuIGxpZ2h0VGhlbWU7XG4gICAgICBjYXNlICdkYXJrJzpcbiAgICAgICAgcmV0dXJuIGRhcmtUaGVtZTtcbiAgICAgIGNhc2UgJ2luaGVyaXQnOlxuICAgICAgZGVmYXVsdDpcbiAgICAgICAgcmV0dXJuIGluaGVyaXRUaGVtZSgpO1xuICAgIH1cbiAgfVxufVxuXG4vKipcbiAqIFV0aWxpdHkgZnVuY3Rpb25zIGZvciBjcmVhdGluZyBhIFRlcm1pbmFsIHdpZGdldFxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGxldCBzdXBwb3J0V2ViR0w6IGJvb2xlYW4gPSBmYWxzZTtcbiAgbGV0IFh0ZXJtXzogdHlwZW9mIFh0ZXJtO1xuICBsZXQgRml0QWRkb25fOiB0eXBlb2YgRml0QWRkb247XG4gIGxldCBXZWJsaW5rc0FkZG9uXzogdHlwZW9mIFdlYkxpbmtzQWRkb247XG4gIGxldCBSZW5kZXJlcl86IHR5cGVvZiBDYW52YXNBZGRvbiB8IHR5cGVvZiBXZWJnbEFkZG9uO1xuXG4gIC8qKlxuICAgKiBEZXRlY3QgaWYgdGhlIGJyb3dzZXIgc3VwcG9ydHMgV2ViR0wgb3Igbm90LlxuICAgKlxuICAgKiBSZWZlcmVuY2U6IGh0dHBzOi8vZGV2ZWxvcGVyLm1vemlsbGEub3JnL2VuLVVTL2RvY3MvV2ViL0FQSS9XZWJHTF9BUEkvQnlfZXhhbXBsZS9EZXRlY3RfV2ViR0xcbiAgICovXG4gIGZ1bmN0aW9uIGhhc1dlYkdMQ29udGV4dCgpOiBib29sZWFuIHtcbiAgICAvLyBDcmVhdGUgY2FudmFzIGVsZW1lbnQuIFRoZSBjYW52YXMgaXMgbm90IGFkZGVkIHRvIHRoZVxuICAgIC8vIGRvY3VtZW50IGl0c2VsZiwgc28gaXQgaXMgbmV2ZXIgZGlzcGxheWVkIGluIHRoZVxuICAgIC8vIGJyb3dzZXIgd2luZG93LlxuICAgIGNvbnN0IGNhbnZhcyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2NhbnZhcycpO1xuXG4gICAgLy8gR2V0IFdlYkdMUmVuZGVyaW5nQ29udGV4dCBmcm9tIGNhbnZhcyBlbGVtZW50LlxuICAgIGNvbnN0IGdsID1cbiAgICAgIGNhbnZhcy5nZXRDb250ZXh0KCd3ZWJnbCcpIHx8IGNhbnZhcy5nZXRDb250ZXh0KCdleHBlcmltZW50YWwtd2ViZ2wnKTtcblxuICAgIC8vIFJlcG9ydCB0aGUgcmVzdWx0LlxuICAgIHRyeSB7XG4gICAgICByZXR1cm4gZ2wgaW5zdGFuY2VvZiBXZWJHTFJlbmRlcmluZ0NvbnRleHQ7XG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gIH1cblxuICBmdW5jdGlvbiBhZGRSZW5kZXJlcih0ZXJtOiBYdGVybSk6IHZvaWQge1xuICAgIGxldCByZW5kZXJlciA9IG5ldyBSZW5kZXJlcl8oKTtcbiAgICB0ZXJtLmxvYWRBZGRvbihyZW5kZXJlcik7XG4gICAgaWYgKHN1cHBvcnRXZWJHTCkge1xuICAgICAgKHJlbmRlcmVyIGFzIFdlYmdsQWRkb24pLm9uQ29udGV4dExvc3MoZXZlbnQgPT4ge1xuICAgICAgICBjb25zb2xlLmRlYnVnKCdXZWJHTCBjb250ZXh0IGxvc3QgLSByZWluaXRpYWxpemUgWHRlcm1qcyByZW5kZXJlci4nKTtcbiAgICAgICAgcmVuZGVyZXIuZGlzcG9zZSgpO1xuICAgICAgICAvLyBJZiB0aGUgV2ViZ2wgY29udGV4dCBpcyBsb3N0LCByZWluaXRpYWxpemUgdGhlIGFkZG9uXG4gICAgICAgIGFkZFJlbmRlcmVyKHRlcm0pO1xuICAgICAgfSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIHh0ZXJtLmpzIHRlcm1pbmFsIGFzeW5jaHJvbm91c2x5LlxuICAgKi9cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGNyZWF0ZVRlcm1pbmFsKFxuICAgIG9wdGlvbnM6IElUZXJtaW5hbE9wdGlvbnMgJiBJVGVybWluYWxJbml0T25seU9wdGlvbnNcbiAgKTogUHJvbWlzZTxbWHRlcm0sIEZpdEFkZG9uXT4ge1xuICAgIGlmICghWHRlcm1fKSB7XG4gICAgICBzdXBwb3J0V2ViR0wgPSBoYXNXZWJHTENvbnRleHQoKTtcbiAgICAgIGNvbnN0IFt4dGVybV8sIGZpdEFkZG9uXywgcmVuZGVyZXJfLCB3ZWJsaW5rc0FkZG9uX10gPSBhd2FpdCBQcm9taXNlLmFsbChbXG4gICAgICAgIGltcG9ydCgneHRlcm0nKSxcbiAgICAgICAgaW1wb3J0KCd4dGVybS1hZGRvbi1maXQnKSxcbiAgICAgICAgc3VwcG9ydFdlYkdMXG4gICAgICAgICAgPyBpbXBvcnQoJ3h0ZXJtLWFkZG9uLXdlYmdsJylcbiAgICAgICAgICA6IGltcG9ydCgneHRlcm0tYWRkb24tY2FudmFzJyksXG4gICAgICAgIGltcG9ydCgneHRlcm0tYWRkb24td2ViLWxpbmtzJylcbiAgICAgIF0pO1xuICAgICAgWHRlcm1fID0geHRlcm1fLlRlcm1pbmFsO1xuICAgICAgRml0QWRkb25fID0gZml0QWRkb25fLkZpdEFkZG9uO1xuICAgICAgUmVuZGVyZXJfID1cbiAgICAgICAgKHJlbmRlcmVyXyBhcyBhbnkpLldlYmdsQWRkb24gPz8gKHJlbmRlcmVyXyBhcyBhbnkpLkNhbnZhc0FkZG9uO1xuICAgICAgV2VibGlua3NBZGRvbl8gPSB3ZWJsaW5rc0FkZG9uXy5XZWJMaW5rc0FkZG9uO1xuICAgIH1cblxuICAgIGNvbnN0IHRlcm0gPSBuZXcgWHRlcm1fKG9wdGlvbnMpO1xuICAgIGFkZFJlbmRlcmVyKHRlcm0pO1xuICAgIGNvbnN0IGZpdEFkZG9uID0gbmV3IEZpdEFkZG9uXygpO1xuICAgIHRlcm0ubG9hZEFkZG9uKGZpdEFkZG9uKTtcbiAgICB0ZXJtLmxvYWRBZGRvbihuZXcgV2VibGlua3NBZGRvbl8oKSk7XG4gICAgcmV0dXJuIFt0ZXJtLCBmaXRBZGRvbl07XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==