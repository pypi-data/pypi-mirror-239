"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_logconsole-extension_lib_index_js"],{

/***/ "../packages/logconsole-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/logconsole-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogLevelSwitcher": () => (/* binding */ LogLevelSwitcher),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole/@jupyterlab/logconsole");
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _status__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./status */ "../packages/logconsole-extension/lib/status.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module logconsole-extension
 */











const LOG_CONSOLE_PLUGIN_ID = '@jupyterlab/logconsole-extension:plugin';
/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.addCheckpoint = 'logconsole:add-checkpoint';
    CommandIDs.clear = 'logconsole:clear';
    CommandIDs.open = 'logconsole:open';
    CommandIDs.setLevel = 'logconsole:set-level';
})(CommandIDs || (CommandIDs = {}));
/**
 * The Log Console extension.
 */
const logConsolePlugin = {
    activate: activateLogConsole,
    id: LOG_CONSOLE_PLUGIN_ID,
    description: 'Provides the logger registry.',
    provides: _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.ILoggerRegistry,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IRenderMimeRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__.IStatusBar],
    autoStart: true
};
/**
 * Activate the Log Console extension.
 */
function activateLogConsole(app, labShell, rendermime, translator, palette, restorer, settingRegistry, statusBar) {
    const trans = translator.load('jupyterlab');
    let logConsoleWidget = null;
    let logConsolePanel = null;
    const loggerRegistry = new _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.LoggerRegistry({
        defaultRendermime: rendermime,
        // The maxLength is reset below from settings
        maxLength: 1000
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'logconsole'
    });
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.open,
            name: () => 'logconsole'
        });
    }
    const status = new _status__WEBPACK_IMPORTED_MODULE_10__.LogConsoleStatus({
        loggerRegistry: loggerRegistry,
        handleClick: () => {
            var _a;
            if (!logConsoleWidget) {
                createLogConsoleWidget({
                    insertMode: 'split-bottom',
                    ref: (_a = app.shell.currentWidget) === null || _a === void 0 ? void 0 : _a.id
                });
            }
            else {
                app.shell.activateById(logConsoleWidget.id);
            }
        },
        translator
    });
    const createLogConsoleWidget = (options = {}) => {
        var _a, _b;
        logConsolePanel = new _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_2__.LogConsolePanel(loggerRegistry, translator);
        logConsolePanel.source = (_b = (_a = options.source) !== null && _a !== void 0 ? _a : labShell.currentPath) !== null && _b !== void 0 ? _b : null;
        logConsoleWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: logConsolePanel });
        logConsoleWidget.addClass('jp-LogConsole');
        logConsoleWidget.title.closable = true;
        logConsoleWidget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.listIcon;
        logConsoleWidget.title.label = trans.__('Log Console');
        const addCheckpointButton = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.CommandToolbarButton({
            commands: app.commands,
            id: CommandIDs.addCheckpoint
        });
        const clearButton = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.CommandToolbarButton({
            commands: app.commands,
            id: CommandIDs.clear
        });
        const notifyCommands = () => {
            app.commands.notifyCommandChanged(CommandIDs.addCheckpoint);
            app.commands.notifyCommandChanged(CommandIDs.clear);
            app.commands.notifyCommandChanged(CommandIDs.open);
            app.commands.notifyCommandChanged(CommandIDs.setLevel);
        };
        logConsoleWidget.toolbar.addItem('lab-log-console-add-checkpoint', addCheckpointButton);
        logConsoleWidget.toolbar.addItem('lab-log-console-clear', clearButton);
        logConsoleWidget.toolbar.addItem('level', new LogLevelSwitcher(logConsoleWidget.content, translator));
        logConsolePanel.sourceChanged.connect(() => {
            notifyCommands();
        });
        logConsolePanel.sourceDisplayed.connect((panel, { source, version }) => {
            status.model.sourceDisplayed(source, version);
        });
        logConsoleWidget.disposed.connect(() => {
            logConsoleWidget = null;
            logConsolePanel = null;
            notifyCommands();
        });
        app.shell.add(logConsoleWidget, 'down', {
            ref: options.ref,
            mode: options.insertMode,
            type: 'Log Console'
        });
        void tracker.add(logConsoleWidget);
        app.shell.activateById(logConsoleWidget.id);
        logConsoleWidget.update();
        notifyCommands();
    };
    app.commands.addCommand(CommandIDs.open, {
        label: trans.__('Show Log Console'),
        execute: (options = {}) => {
            // Toggle the display
            if (logConsoleWidget) {
                logConsoleWidget.dispose();
            }
            else {
                createLogConsoleWidget(options);
            }
        },
        isToggled: () => {
            return logConsoleWidget !== null;
        }
    });
    app.commands.addCommand(CommandIDs.addCheckpoint, {
        execute: () => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.checkpoint();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.addIcon,
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: trans.__('Add Checkpoint')
    });
    app.commands.addCommand(CommandIDs.clear, {
        execute: () => {
            var _a;
            (_a = logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) === null || _a === void 0 ? void 0 : _a.clear();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.clearIcon,
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: trans.__('Clear Log')
    });
    function toTitleCase(value) {
        return value.length === 0 ? value : value[0].toUpperCase() + value.slice(1);
    }
    app.commands.addCommand(CommandIDs.setLevel, {
        // TODO: find good icon class
        execute: (args) => {
            if (logConsolePanel === null || logConsolePanel === void 0 ? void 0 : logConsolePanel.logger) {
                logConsolePanel.logger.level = args.level;
            }
        },
        isEnabled: () => !!logConsolePanel && logConsolePanel.source !== null,
        label: args => args['level']
            ? trans.__('Set Log Level to %1', toTitleCase(args.level))
            : trans.__('Set log level to `level`.')
    });
    if (palette) {
        palette.addItem({
            command: CommandIDs.open,
            category: trans.__('Main Area')
        });
    }
    if (statusBar) {
        statusBar.registerStatusItem('@jupyterlab/logconsole-extension:status', {
            item: status,
            align: 'left',
            isActive: () => { var _a; return ((_a = status.model) === null || _a === void 0 ? void 0 : _a.version) > 0; },
            activeStateChanged: status.model.stateChanged
        });
    }
    function setSource(source) {
        if (logConsolePanel) {
            logConsolePanel.source = source;
        }
        status.model.source = source;
    }
    void app.restored.then(() => {
        var _a;
        // Set source only after app is restored in order to allow restorer to
        // restore previous source first, which may set the renderer
        labShell.currentPathChanged.connect((_, { newValue }) => setSource(newValue));
        setSource((_a = labShell.currentPath) !== null && _a !== void 0 ? _a : null);
    });
    if (settingRegistry) {
        const updateSettings = (settings) => {
            loggerRegistry.maxLength = settings.get('maxLogEntries')
                .composite;
            status.model.flashEnabled = settings.get('flash').composite;
        };
        Promise.all([settingRegistry.load(LOG_CONSOLE_PLUGIN_ID), app.restored])
            .then(([settings]) => {
            updateSettings(settings);
            settings.changed.connect(settings => {
                updateSettings(settings);
            });
        })
            .catch((reason) => {
            console.error(reason.message);
        });
    }
    return loggerRegistry;
}
/**
 * A toolbar widget that switches log levels.
 */
class LogLevelSwitcher extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.ReactWidget {
    /**
     * Construct a new log level switcher.
     */
    constructor(widget, translator) {
        super();
        /**
         * Handle `change` events for the HTMLSelect component.
         */
        this.handleChange = (event) => {
            if (this._logConsole.logger) {
                this._logConsole.logger.level = event.target.value;
            }
            this.update();
        };
        /**
         * Handle `keydown` events for the HTMLSelect component.
         */
        this.handleKeyDown = (event) => {
            if (event.keyCode === 13) {
                this._logConsole.activate();
            }
        };
        this._id = `level-${_lumino_coreutils__WEBPACK_IMPORTED_MODULE_8__.UUID.uuid4()}`;
        this.translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this.addClass('jp-LogConsole-toolbarLogLevel');
        this._logConsole = widget;
        if (widget.source) {
            this.update();
        }
        widget.sourceChanged.connect(this._updateSource, this);
    }
    _updateSource(sender, { oldValue, newValue }) {
        // Transfer stateChanged handler to new source logger
        if (oldValue !== null) {
            const logger = sender.loggerRegistry.getLogger(oldValue);
            logger.stateChanged.disconnect(this.update, this);
        }
        if (newValue !== null) {
            const logger = sender.loggerRegistry.getLogger(newValue);
            logger.stateChanged.connect(this.update, this);
        }
        this.update();
    }
    render() {
        const logger = this._logConsole.logger;
        return (react__WEBPACK_IMPORTED_MODULE_9__.createElement(react__WEBPACK_IMPORTED_MODULE_9__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("label", { htmlFor: this._id, className: logger === null
                    ? 'jp-LogConsole-toolbarLogLevel-disabled'
                    : undefined }, this._trans.__('Log Level:')),
            react__WEBPACK_IMPORTED_MODULE_9__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.HTMLSelect, { id: this._id, className: "jp-LogConsole-toolbarLogLevelDropdown", onChange: this.handleChange, onKeyDown: this.handleKeyDown, value: logger === null || logger === void 0 ? void 0 : logger.level, "aria-label": this._trans.__('Log level'), disabled: logger === null, options: logger === null
                    ? []
                    : [
                        [this._trans.__('Critical'), 'Critical'],
                        [this._trans.__('Error'), 'Error'],
                        [this._trans.__('Warning'), 'Warning'],
                        [this._trans.__('Info'), 'Info'],
                        [this._trans.__('Debug'), 'Debug']
                    ].map(data => ({
                        label: data[0],
                        value: data[1].toLowerCase()
                    })) })));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (logConsolePlugin);


/***/ }),

/***/ "../packages/logconsole-extension/lib/status.js":
/*!******************************************************!*\
  !*** ../packages/logconsole-extension/lib/status.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LogConsoleStatus": () => (/* binding */ LogConsoleStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * A pure functional component for a Log Console status item.
 *
 * @param props - the props for the component.
 *
 * @returns a tsx component for rendering the Log Console status.
 */
function LogConsoleStatusComponent(props) {
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    let title = '';
    if (props.newMessages > 0) {
        title = trans.__('%1 new messages, %2 log entries for %3', props.newMessages, props.logEntries, props.source);
    }
    else {
        title += trans.__('%1 log entries for %2', props.logEntries, props.source);
    }
    return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__.GroupItem, { spacing: 0, onClick: props.handleClick, title: title },
        react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.listIcon.react, { top: '2px', stylesheet: 'statusBar' }),
        props.newMessages > 0 ? react__WEBPACK_IMPORTED_MODULE_4___default().createElement(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_0__.TextItem, { source: props.newMessages }) : react__WEBPACK_IMPORTED_MODULE_4___default().createElement((react__WEBPACK_IMPORTED_MODULE_4___default().Fragment), null)));
}
/**
 * A VDomRenderer widget for displaying the status of Log Console logs.
 */
class LogConsoleStatus extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomRenderer {
    /**
     * Construct the log console status widget.
     *
     * @param options - The status widget initialization options.
     */
    constructor(options) {
        super(new LogConsoleStatus.Model(options.loggerRegistry));
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._handleClick = options.handleClick;
        this.addClass('jp-mod-highlighted');
        this.addClass('jp-LogConsoleStatusItem');
    }
    /**
     * Render the log console status item.
     */
    render() {
        if (this.model === null || this.model.version === 0) {
            return null;
        }
        const { flashEnabled, messages, source, version, versionDisplayed, versionNotified } = this.model;
        if (source !== null && flashEnabled && version > versionNotified) {
            this._flashHighlight();
            this.model.sourceNotified(source, version);
        }
        else if (source !== null && flashEnabled && version > versionDisplayed) {
            this._showHighlighted();
        }
        else {
            this._clearHighlight();
        }
        return (react__WEBPACK_IMPORTED_MODULE_4___default().createElement(LogConsoleStatusComponent, { handleClick: this._handleClick, logEntries: messages, newMessages: version - versionDisplayed, source: this.model.source, translator: this.translator }));
    }
    _flashHighlight() {
        this._showHighlighted();
        // To make sure the browser triggers the animation, we remove the class,
        // wait for an animation frame, then add it back
        this.removeClass('jp-LogConsole-flash');
        requestAnimationFrame(() => {
            this.addClass('jp-LogConsole-flash');
        });
    }
    _showHighlighted() {
        this.addClass('jp-mod-selected');
    }
    _clearHighlight() {
        this.removeClass('jp-LogConsole-flash');
        this.removeClass('jp-mod-selected');
    }
}
/**
 * A namespace for Log Console log status.
 */
(function (LogConsoleStatus) {
    /**
     * A VDomModel for the LogConsoleStatus item.
     */
    class Model extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomModel {
        /**
         * Create a new LogConsoleStatus model.
         *
         * @param loggerRegistry - The logger registry providing the logs.
         */
        constructor(loggerRegistry) {
            super();
            /**
             * A signal emitted when the flash enablement changes.
             */
            this.flashEnabledChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
            this._flashEnabled = true;
            this._source = null;
            /**
             * The view status of each source.
             *
             * #### Notes
             * Keys are source names, value is a list of two numbers. The first
             * represents the version of the messages that was last displayed to the
             * user, the second represents the version that we last notified the user
             * about.
             */
            this._sourceVersion = new Map();
            this._loggerRegistry = loggerRegistry;
            this._loggerRegistry.registryChanged.connect(this._handleLogRegistryChange, this);
            this._handleLogRegistryChange();
        }
        /**
         * Number of messages currently in the current source.
         */
        get messages() {
            if (this._source === null) {
                return 0;
            }
            const logger = this._loggerRegistry.getLogger(this._source);
            return logger.length;
        }
        /**
         * The number of messages ever stored by the current source.
         */
        get version() {
            if (this._source === null) {
                return 0;
            }
            const logger = this._loggerRegistry.getLogger(this._source);
            return logger.version;
        }
        /**
         * The name of the active log source
         */
        get source() {
            return this._source;
        }
        set source(name) {
            if (this._source === name) {
                return;
            }
            this._source = name;
            // refresh rendering
            this.stateChanged.emit();
        }
        /**
         * The last source version that was displayed.
         */
        get versionDisplayed() {
            var _a, _b;
            if (this._source === null) {
                return 0;
            }
            return (_b = (_a = this._sourceVersion.get(this._source)) === null || _a === void 0 ? void 0 : _a.lastDisplayed) !== null && _b !== void 0 ? _b : 0;
        }
        /**
         * The last source version we notified the user about.
         */
        get versionNotified() {
            var _a, _b;
            if (this._source === null) {
                return 0;
            }
            return (_b = (_a = this._sourceVersion.get(this._source)) === null || _a === void 0 ? void 0 : _a.lastNotified) !== null && _b !== void 0 ? _b : 0;
        }
        /**
         * Flag to toggle flashing when new logs added.
         */
        get flashEnabled() {
            return this._flashEnabled;
        }
        set flashEnabled(enabled) {
            if (this._flashEnabled === enabled) {
                return;
            }
            this._flashEnabled = enabled;
            this.flashEnabledChanged.emit();
            // refresh rendering
            this.stateChanged.emit();
        }
        /**
         * Record the last source version displayed to the user.
         *
         * @param source - The name of the log source.
         * @param version - The version of the log that was displayed.
         *
         * #### Notes
         * This will also update the last notified version so that the last
         * notified version is always at least the last displayed version.
         */
        sourceDisplayed(source, version) {
            if (source === null || version === null) {
                return;
            }
            const versions = this._sourceVersion.get(source);
            let change = false;
            if (versions.lastDisplayed < version) {
                versions.lastDisplayed = version;
                change = true;
            }
            if (versions.lastNotified < version) {
                versions.lastNotified = version;
                change = true;
            }
            if (change && source === this._source) {
                this.stateChanged.emit();
            }
        }
        /**
         * Record a source version we notified the user about.
         *
         * @param source - The name of the log source.
         * @param version - The version of the log.
         */
        sourceNotified(source, version) {
            if (source === null) {
                return;
            }
            const versions = this._sourceVersion.get(source);
            if (versions.lastNotified < version) {
                versions.lastNotified = version;
                if (source === this._source) {
                    this.stateChanged.emit();
                }
            }
        }
        _handleLogRegistryChange() {
            const loggers = this._loggerRegistry.getLoggers();
            for (const logger of loggers) {
                if (!this._sourceVersion.has(logger.source)) {
                    logger.contentChanged.connect(this._handleLogContentChange, this);
                    this._sourceVersion.set(logger.source, {
                        lastDisplayed: 0,
                        lastNotified: 0
                    });
                }
            }
        }
        _handleLogContentChange({ source }, change) {
            if (source === this._source) {
                this.stateChanged.emit();
            }
        }
    }
    LogConsoleStatus.Model = Model;
})(LogConsoleStatus || (LogConsoleStatus = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbG9nY29uc29sZS1leHRlbnNpb25fbGliX2luZGV4X2pzLjFmMzNmOTY2MjA0ODIzOWI0NzY0LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFPOEI7QUFLSDtBQU9FO0FBQzZCO0FBQ0U7QUFDWjtBQUtsQjtBQVFFO0FBQ007QUFFVjtBQUNhO0FBRTVDLE1BQU0scUJBQXFCLEdBQUcseUNBQXlDLENBQUM7QUFFeEU7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FLbkI7QUFMRCxXQUFVLFVBQVU7SUFDTCx3QkFBYSxHQUFHLDJCQUEyQixDQUFDO0lBQzVDLGdCQUFLLEdBQUcsa0JBQWtCLENBQUM7SUFDM0IsZUFBSSxHQUFHLGlCQUFpQixDQUFDO0lBQ3pCLG1CQUFRLEdBQUcsc0JBQXNCLENBQUM7QUFDakQsQ0FBQyxFQUxTLFVBQVUsS0FBVixVQUFVLFFBS25CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLGdCQUFnQixHQUEyQztJQUMvRCxRQUFRLEVBQUUsa0JBQWtCO0lBQzVCLEVBQUUsRUFBRSxxQkFBcUI7SUFDekIsV0FBVyxFQUFFLCtCQUErQjtJQUM1QyxRQUFRLEVBQUUsbUVBQWU7SUFDekIsUUFBUSxFQUFFLENBQUMsOERBQVMsRUFBRSx1RUFBbUIsRUFBRSxnRUFBVyxDQUFDO0lBQ3ZELFFBQVEsRUFBRSxDQUFDLGlFQUFlLEVBQUUsb0VBQWUsRUFBRSx5RUFBZ0IsRUFBRSw2REFBVSxDQUFDO0lBQzFFLFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7R0FFRztBQUNILFNBQVMsa0JBQWtCLENBQ3pCLEdBQW9CLEVBQ3BCLFFBQW1CLEVBQ25CLFVBQStCLEVBQy9CLFVBQXVCLEVBQ3ZCLE9BQStCLEVBQy9CLFFBQWdDLEVBQ2hDLGVBQXdDLEVBQ3hDLFNBQTRCO0lBRTVCLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJ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LE9BQU8sQ0FBQyxJQUFJLENBQUMsdUJBQXVCLEVBQUUsSUFBSSxDQUFDLENBQUM7b0JBQ2xFLElBQUksQ0FBQyxjQUFjLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxNQUFNLEVBQUU7d0JBQ3JDLGFBQWEsRUFBRSxDQUFDO3dCQUNoQixZQUFZLEVBQUUsQ0FBQztxQkFDaEIsQ0FBQyxDQUFDO2lCQUNKO2FBQ0Y7UUFDSCxDQUFDO1FBRU8sdUJBQXVCLENBQzdCLEVBQUUsTUFBTSxFQUFXLEVBQ25CLE1BQXNCO1lBRXRCLElBQUksTUFBTSxLQUFLLElBQUksQ0FBQyxPQUFPLEVBQUU7Z0JBQzNCLElBQUksQ0FBQyxZQUFZLENBQUMsSUFBSSxFQUFFLENBQUM7YUFDMUI7UUFDSCxDQUFDO0tBbUJGO0lBdkxZLHNCQUFLLFFBdUxqQjtBQTJCSCxDQUFDLEVBdE5nQixnQkFBZ0IsS0FBaEIsZ0JBQWdCLFFBc05oQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9sb2djb25zb2xlLWV4dGVuc2lvbi9zcmMvaW5kZXgudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9sb2djb25zb2xlLWV4dGVuc2lvbi9zcmMvc3RhdHVzLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBsb2djb25zb2xlLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBJQ29tbWFuZFBhbGV0dGUsXG4gIE1haW5BcmVhV2lkZ2V0LFxuICBXaWRnZXRUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElDaGFuZ2VkQXJncyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBJTG9nZ2VyUmVnaXN0cnksXG4gIExvZ0NvbnNvbGVQYW5lbCxcbiAgTG9nZ2VyUmVnaXN0cnksXG4gIExvZ0xldmVsXG59IGZyb20gJ0BqdXB5dGVybGFiL2xvZ2NvbnNvbGUnO1xuaW1wb3J0IHsgSVJlbmRlck1pbWVSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJU3RhdHVzQmFyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgYWRkSWNvbixcbiAgY2xlYXJJY29uLFxuICBDb21tYW5kVG9vbGJhckJ1dHRvbixcbiAgSFRNTFNlbGVjdCxcbiAgbGlzdEljb24sXG4gIFJlYWN0V2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgVVVJRCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERvY2tMYXlvdXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgTG9nQ29uc29sZVN0YXR1cyB9IGZyb20gJy4vc3RhdHVzJztcblxuY29uc3QgTE9HX0NPTlNPTEVfUExVR0lOX0lEID0gJ0BqdXB5dGVybGFiL2xvZ2NvbnNvbGUtZXh0ZW5zaW9uOnBsdWdpbic7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgYWRkQ2hlY2twb2ludCA9ICdsb2djb25zb2xlOmFkZC1jaGVja3BvaW50JztcbiAgZXhwb3J0IGNvbnN0IGNsZWFyID0gJ2xvZ2NvbnNvbGU6Y2xlYXInO1xuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdsb2djb25zb2xlOm9wZW4nO1xuICBleHBvcnQgY29uc3Qgc2V0TGV2ZWwgPSAnbG9nY29uc29sZTpzZXQtbGV2ZWwnO1xufVxuXG4vKipcbiAqIFRoZSBMb2cgQ29uc29sZSBleHRlbnNpb24uXG4gKi9cbmNvbnN0IGxvZ0NvbnNvbGVQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTG9nZ2VyUmVnaXN0cnk+ID0ge1xuICBhY3RpdmF0ZTogYWN0aXZhdGVMb2dDb25zb2xlLFxuICBpZDogTE9HX0NPTlNPTEVfUExVR0lOX0lELFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBsb2dnZXIgcmVnaXN0cnkuJyxcbiAgcHJvdmlkZXM6IElMb2dnZXJSZWdpc3RyeSxcbiAgcmVxdWlyZXM6IFtJTGFiU2hlbGwsIElSZW5kZXJNaW1lUmVnaXN0cnksIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGUsIElMYXlvdXRSZXN0b3JlciwgSVNldHRpbmdSZWdpc3RyeSwgSVN0YXR1c0Jhcl0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUgTG9nIENvbnNvbGUgZXh0ZW5zaW9uLlxuICovXG5mdW5jdGlvbiBhY3RpdmF0ZUxvZ0NvbnNvbGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBsYWJTaGVsbDogSUxhYlNoZWxsLFxuICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5LFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGwsXG4gIHN0YXR1c0JhcjogSVN0YXR1c0JhciB8IG51bGxcbik6IElMb2dnZXJSZWdpc3RyeSB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGxldCBsb2dDb25zb2xlV2lkZ2V0OiBNYWluQXJlYVdpZGdldDxMb2dDb25zb2xlUGFuZWw+IHwgbnVsbCA9IG51bGw7XG4gIGxldCBsb2dDb25zb2xlUGFuZWw6IExvZ0NvbnNvbGVQYW5lbCB8IG51bGwgPSBudWxsO1xuXG4gIGNvbnN0IGxvZ2dlclJlZ2lzdHJ5ID0gbmV3IExvZ2dlclJlZ2lzdHJ5KHtcbiAgICBkZWZhdWx0UmVuZGVybWltZTogcmVuZGVybWltZSxcbiAgICAvLyBUaGUgbWF4TGVuZ3RoIGlzIHJlc2V0IGJlbG93IGZyb20gc2V0dGluZ3NcbiAgICBtYXhMZW5ndGg6IDEwMDBcbiAgfSk7XG5cbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PExvZ0NvbnNvbGVQYW5lbD4+KHtcbiAgICBuYW1lc3BhY2U6ICdsb2djb25zb2xlJ1xuICB9KTtcblxuICBpZiAocmVzdG9yZXIpIHtcbiAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5vcGVuLFxuICAgICAgbmFtZTogKCkgPT4gJ2xvZ2NvbnNvbGUnXG4gICAgfSk7XG4gIH1cblxuICBjb25zdCBzdGF0dXMgPSBuZXcgTG9nQ29uc29sZVN0YXR1cyh7XG4gICAgbG9nZ2VyUmVnaXN0cnk6IGxvZ2dlclJlZ2lzdHJ5LFxuICAgIGhhbmRsZUNsaWNrOiAoKSA9PiB7XG4gICAgICBpZiAoIWxvZ0NvbnNvbGVXaWRnZXQpIHtcbiAgICAgICAgY3JlYXRlTG9nQ29uc29sZVdpZGdldCh7XG4gICAgICAgICAgaW5zZXJ0TW9kZTogJ3NwbGl0LWJvdHRvbScsXG4gICAgICAgICAgcmVmOiBhcHAuc2hlbGwuY3VycmVudFdpZGdldD8uaWRcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBhcHAuc2hlbGwuYWN0aXZhdGVCeUlkKGxvZ0NvbnNvbGVXaWRnZXQuaWQpO1xuICAgICAgfVxuICAgIH0sXG4gICAgdHJhbnNsYXRvclxuICB9KTtcblxuICBpbnRlcmZhY2UgSUxvZ0NvbnNvbGVPcHRpb25zIHtcbiAgICBzb3VyY2U/OiBzdHJpbmc7XG4gICAgaW5zZXJ0TW9kZT86IERvY2tMYXlvdXQuSW5zZXJ0TW9kZTtcbiAgICByZWY/OiBzdHJpbmc7XG4gIH1cblxuICBjb25zdCBjcmVhdGVMb2dDb25zb2xlV2lkZ2V0ID0gKG9wdGlvbnM6IElMb2dDb25zb2xlT3B0aW9ucyA9IHt9KSA9PiB7XG4gICAgbG9nQ29uc29sZVBhbmVsID0gbmV3IExvZ0NvbnNvbGVQYW5lbChsb2dnZXJSZWdpc3RyeSwgdHJhbnNsYXRvcik7XG5cbiAgICBsb2dDb25zb2xlUGFuZWwuc291cmNlID0gb3B0aW9ucy5zb3VyY2UgPz8gbGFiU2hlbGwuY3VycmVudFBhdGggPz8gbnVsbDtcblxuICAgIGxvZ0NvbnNvbGVXaWRnZXQgPSBuZXcgTWFpbkFyZWFXaWRnZXQoeyBjb250ZW50OiBsb2dDb25zb2xlUGFuZWwgfSk7XG4gICAgbG9nQ29uc29sZVdpZGdldC5hZGRDbGFzcygnanAtTG9nQ29uc29sZScpO1xuICAgIGxvZ0NvbnNvbGVXaWRnZXQudGl0bGUuY2xvc2FibGUgPSB0cnVlO1xuICAgIGxvZ0NvbnNvbGVXaWRnZXQudGl0bGUuaWNvbiA9IGxpc3RJY29uO1xuICAgIGxvZ0NvbnNvbGVXaWRnZXQudGl0bGUubGFiZWwgPSB0cmFucy5fXygnTG9nIENvbnNvbGUnKTtcblxuICAgIGNvbnN0IGFkZENoZWNrcG9pbnRCdXR0b24gPSBuZXcgQ29tbWFuZFRvb2xiYXJCdXR0b24oe1xuICAgICAgY29tbWFuZHM6IGFwcC5jb21tYW5kcyxcbiAgICAgIGlkOiBDb21tYW5kSURzLmFkZENoZWNrcG9pbnRcbiAgICB9KTtcblxuICAgIGNvbnN0IGNsZWFyQnV0dG9uID0gbmV3IENvbW1hbmRUb29sYmFyQnV0dG9uKHtcbiAgICAgIGNvbW1hbmRzOiBhcHAuY29tbWFuZHMsXG4gICAgICBpZDogQ29tbWFuZElEcy5jbGVhclxuICAgIH0pO1xuXG4gICAgY29uc3Qgbm90aWZ5Q29tbWFuZHMgPSAoKSA9PiB7XG4gICAgICBhcHAuY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoQ29tbWFuZElEcy5hZGRDaGVja3BvaW50KTtcbiAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZChDb21tYW5kSURzLmNsZWFyKTtcbiAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZChDb21tYW5kSURzLm9wZW4pO1xuICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMuc2V0TGV2ZWwpO1xuICAgIH07XG5cbiAgICBsb2dDb25zb2xlV2lkZ2V0LnRvb2xiYXIuYWRkSXRlbShcbiAgICAgICdsYWItbG9nLWNvbnNvbGUtYWRkLWNoZWNrcG9pbnQnLFxuICAgICAgYWRkQ2hlY2twb2ludEJ1dHRvblxuICAgICk7XG4gICAgbG9nQ29uc29sZVdpZGdldC50b29sYmFyLmFkZEl0ZW0oJ2xhYi1sb2ctY29uc29sZS1jbGVhcicsIGNsZWFyQnV0dG9uKTtcblxuICAgIGxvZ0NvbnNvbGVXaWRnZXQudG9vbGJhci5hZGRJdGVtKFxuICAgICAgJ2xldmVsJyxcbiAgICAgIG5ldyBMb2dMZXZlbFN3aXRjaGVyKGxvZ0NvbnNvbGVXaWRnZXQuY29udGVudCwgdHJhbnNsYXRvcilcbiAgICApO1xuXG4gICAgbG9nQ29uc29sZVBhbmVsLnNvdXJjZUNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICBub3RpZnlDb21tYW5kcygpO1xuICAgIH0pO1xuXG4gICAgbG9nQ29uc29sZVBhbmVsLnNvdXJjZURpc3BsYXllZC5jb25uZWN0KChwYW5lbCwgeyBzb3VyY2UsIHZlcnNpb24gfSkgPT4ge1xuICAgICAgc3RhdHVzLm1vZGVsLnNvdXJjZURpc3BsYXllZChzb3VyY2UsIHZlcnNpb24pO1xuICAgIH0pO1xuXG4gICAgbG9nQ29uc29sZVdpZGdldC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIGxvZ0NvbnNvbGVXaWRnZXQgPSBudWxsO1xuICAgICAgbG9nQ29uc29sZVBhbmVsID0gbnVsbDtcbiAgICAgIG5vdGlmeUNvbW1hbmRzKCk7XG4gICAgfSk7XG5cbiAgICBhcHAuc2hlbGwuYWRkKGxvZ0NvbnNvbGVXaWRnZXQsICdkb3duJywge1xuICAgICAgcmVmOiBvcHRpb25zLnJlZixcbiAgICAgIG1vZGU6IG9wdGlvbnMuaW5zZXJ0TW9kZSxcbiAgICAgIHR5cGU6ICdMb2cgQ29uc29sZSdcbiAgICB9KTtcbiAgICB2b2lkIHRyYWNrZXIuYWRkKGxvZ0NvbnNvbGVXaWRnZXQpO1xuICAgIGFwcC5zaGVsbC5hY3RpdmF0ZUJ5SWQobG9nQ29uc29sZVdpZGdldC5pZCk7XG5cbiAgICBsb2dDb25zb2xlV2lkZ2V0LnVwZGF0ZSgpO1xuICAgIG5vdGlmeUNvbW1hbmRzKCk7XG4gIH07XG5cbiAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IExvZyBDb25zb2xlJyksXG4gICAgZXhlY3V0ZTogKG9wdGlvbnM6IElMb2dDb25zb2xlT3B0aW9ucyA9IHt9KSA9PiB7XG4gICAgICAvLyBUb2dnbGUgdGhlIGRpc3BsYXlcbiAgICAgIGlmIChsb2dDb25zb2xlV2lkZ2V0KSB7XG4gICAgICAgIGxvZ0NvbnNvbGVXaWRnZXQuZGlzcG9zZSgpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgY3JlYXRlTG9nQ29uc29sZVdpZGdldChvcHRpb25zKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGlzVG9nZ2xlZDogKCkgPT4ge1xuICAgICAgcmV0dXJuIGxvZ0NvbnNvbGVXaWRnZXQgIT09IG51bGw7XG4gICAgfVxuICB9KTtcblxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFkZENoZWNrcG9pbnQsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBsb2dDb25zb2xlUGFuZWw/LmxvZ2dlcj8uY2hlY2twb2ludCgpO1xuICAgIH0sXG4gICAgaWNvbjogYWRkSWNvbixcbiAgICBpc0VuYWJsZWQ6ICgpID0+ICEhbG9nQ29uc29sZVBhbmVsICYmIGxvZ0NvbnNvbGVQYW5lbC5zb3VyY2UgIT09IG51bGwsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdBZGQgQ2hlY2twb2ludCcpXG4gIH0pO1xuXG4gIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2xlYXIsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBsb2dDb25zb2xlUGFuZWw/LmxvZ2dlcj8uY2xlYXIoKTtcbiAgICB9LFxuICAgIGljb246IGNsZWFySWNvbixcbiAgICBpc0VuYWJsZWQ6ICgpID0+ICEhbG9nQ29uc29sZVBhbmVsICYmIGxvZ0NvbnNvbGVQYW5lbC5zb3VyY2UgIT09IG51bGwsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdDbGVhciBMb2cnKVxuICB9KTtcblxuICBmdW5jdGlvbiB0b1RpdGxlQ2FzZSh2YWx1ZTogc3RyaW5nKSB7XG4gICAgcmV0dXJuIHZhbHVlLmxlbmd0aCA9PT0gMCA/IHZhbHVlIDogdmFsdWVbMF0udG9VcHBlckNhc2UoKSArIHZhbHVlLnNsaWNlKDEpO1xuICB9XG5cbiAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zZXRMZXZlbCwge1xuICAgIC8vIFRPRE86IGZpbmQgZ29vZCBpY29uIGNsYXNzXG4gICAgZXhlY3V0ZTogKGFyZ3M6IHsgbGV2ZWw6IExvZ0xldmVsIH0pID0+IHtcbiAgICAgIGlmIChsb2dDb25zb2xlUGFuZWw/LmxvZ2dlcikge1xuICAgICAgICBsb2dDb25zb2xlUGFuZWwubG9nZ2VyLmxldmVsID0gYXJncy5sZXZlbDtcbiAgICAgIH1cbiAgICB9LFxuICAgIGlzRW5hYmxlZDogKCkgPT4gISFsb2dDb25zb2xlUGFuZWwgJiYgbG9nQ29uc29sZVBhbmVsLnNvdXJjZSAhPT0gbnVsbCxcbiAgICBsYWJlbDogYXJncyA9PlxuICAgICAgYXJnc1snbGV2ZWwnXVxuICAgICAgICA/IHRyYW5zLl9fKCdTZXQgTG9nIExldmVsIHRvICUxJywgdG9UaXRsZUNhc2UoYXJncy5sZXZlbCBhcyBzdHJpbmcpKVxuICAgICAgICA6IHRyYW5zLl9fKCdTZXQgbG9nIGxldmVsIHRvIGBsZXZlbGAuJylcbiAgfSk7XG5cbiAgaWYgKHBhbGV0dGUpIHtcbiAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5vcGVuLFxuICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdNYWluIEFyZWEnKVxuICAgIH0pO1xuICB9XG4gIGlmIChzdGF0dXNCYXIpIHtcbiAgICBzdGF0dXNCYXIucmVnaXN0ZXJTdGF0dXNJdGVtKCdAanVweXRlcmxhYi9sb2djb25zb2xlLWV4dGVuc2lvbjpzdGF0dXMnLCB7XG4gICAgICBpdGVtOiBzdGF0dXMsXG4gICAgICBhbGlnbjogJ2xlZnQnLFxuICAgICAgaXNBY3RpdmU6ICgpID0+IHN0YXR1cy5tb2RlbD8udmVyc2lvbiA+IDAsXG4gICAgICBhY3RpdmVTdGF0ZUNoYW5nZWQ6IHN0YXR1cy5tb2RlbCEuc3RhdGVDaGFuZ2VkXG4gICAgfSk7XG4gIH1cblxuICBmdW5jdGlvbiBzZXRTb3VyY2Uoc291cmNlOiBzdHJpbmcgfCBudWxsKSB7XG4gICAgaWYgKGxvZ0NvbnNvbGVQYW5lbCkge1xuICAgICAgbG9nQ29uc29sZVBhbmVsLnNvdXJjZSA9IHNvdXJjZTtcbiAgICB9XG4gICAgc3RhdHVzLm1vZGVsLnNvdXJjZSA9IHNvdXJjZTtcbiAgfVxuICB2b2lkIGFwcC5yZXN0b3JlZC50aGVuKCgpID0+IHtcbiAgICAvLyBTZXQgc291cmNlIG9ubHkgYWZ0ZXIgYXBwIGlzIHJlc3RvcmVkIGluIG9yZGVyIHRvIGFsbG93IHJlc3RvcmVyIHRvXG4gICAgLy8gcmVzdG9yZSBwcmV2aW91cyBzb3VyY2UgZmlyc3QsIHdoaWNoIG1heSBzZXQgdGhlIHJlbmRlcmVyXG4gICAgbGFiU2hlbGwuY3VycmVudFBhdGhDaGFuZ2VkLmNvbm5lY3QoKF8sIHsgbmV3VmFsdWUgfSkgPT5cbiAgICAgIHNldFNvdXJjZShuZXdWYWx1ZSlcbiAgICApO1xuICAgIHNldFNvdXJjZShsYWJTaGVsbC5jdXJyZW50UGF0aCA/PyBudWxsKTtcbiAgfSk7XG5cbiAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgIGNvbnN0IHVwZGF0ZVNldHRpbmdzID0gKHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyk6IHZvaWQgPT4ge1xuICAgICAgbG9nZ2VyUmVnaXN0cnkubWF4TGVuZ3RoID0gc2V0dGluZ3MuZ2V0KCdtYXhMb2dFbnRyaWVzJylcbiAgICAgICAgLmNvbXBvc2l0ZSBhcyBudW1iZXI7XG4gICAgICBzdGF0dXMubW9kZWwuZmxhc2hFbmFibGVkID0gc2V0dGluZ3MuZ2V0KCdmbGFzaCcpLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgIH07XG5cbiAgICBQcm9taXNlLmFsbChbc2V0dGluZ1JlZ2lzdHJ5LmxvYWQoTE9HX0NPTlNPTEVfUExVR0lOX0lEKSwgYXBwLnJlc3RvcmVkXSlcbiAgICAgIC50aGVuKChbc2V0dGluZ3NdKSA9PiB7XG4gICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KHNldHRpbmdzID0+IHtcbiAgICAgICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICAgIH0pO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICBjb25zb2xlLmVycm9yKHJlYXNvbi5tZXNzYWdlKTtcbiAgICAgIH0pO1xuICB9XG5cbiAgcmV0dXJuIGxvZ2dlclJlZ2lzdHJ5O1xufVxuXG4vKipcbiAqIEEgdG9vbGJhciB3aWRnZXQgdGhhdCBzd2l0Y2hlcyBsb2cgbGV2ZWxzLlxuICovXG5leHBvcnQgY2xhc3MgTG9nTGV2ZWxTd2l0Y2hlciBleHRlbmRzIFJlYWN0V2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBsb2cgbGV2ZWwgc3dpdGNoZXIuXG4gICAqL1xuICBjb25zdHJ1Y3Rvcih3aWRnZXQ6IExvZ0NvbnNvbGVQYW5lbCwgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX3RyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1Mb2dDb25zb2xlLXRvb2xiYXJMb2dMZXZlbCcpO1xuICAgIHRoaXMuX2xvZ0NvbnNvbGUgPSB3aWRnZXQ7XG4gICAgaWYgKHdpZGdldC5zb3VyY2UpIHtcbiAgICAgIHRoaXMudXBkYXRlKCk7XG4gICAgfVxuICAgIHdpZGdldC5zb3VyY2VDaGFuZ2VkLmNvbm5lY3QodGhpcy5fdXBkYXRlU291cmNlLCB0aGlzKTtcbiAgfVxuXG4gIHByaXZhdGUgX3VwZGF0ZVNvdXJjZShcbiAgICBzZW5kZXI6IExvZ0NvbnNvbGVQYW5lbCxcbiAgICB7IG9sZFZhbHVlLCBuZXdWYWx1ZSB9OiBJQ2hhbmdlZEFyZ3M8c3RyaW5nIHwgbnVsbD5cbiAgKSB7XG4gICAgLy8gVHJhbnNmZXIgc3RhdGVDaGFuZ2VkIGhhbmRsZXIgdG8gbmV3IHNvdXJjZSBsb2dnZXJcbiAgICBpZiAob2xkVmFsdWUgIT09IG51bGwpIHtcbiAgICAgIGNvbnN0IGxvZ2dlciA9IHNlbmRlci5sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXIob2xkVmFsdWUpO1xuICAgICAgbG9nZ2VyLnN0YXRlQ2hhbmdlZC5kaXNjb25uZWN0KHRoaXMudXBkYXRlLCB0aGlzKTtcbiAgICB9XG4gICAgaWYgKG5ld1ZhbHVlICE9PSBudWxsKSB7XG4gICAgICBjb25zdCBsb2dnZXIgPSBzZW5kZXIubG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VyKG5ld1ZhbHVlKTtcbiAgICAgIGxvZ2dlci5zdGF0ZUNoYW5nZWQuY29ubmVjdCh0aGlzLnVwZGF0ZSwgdGhpcyk7XG4gICAgfVxuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBjaGFuZ2VgIGV2ZW50cyBmb3IgdGhlIEhUTUxTZWxlY3QgY29tcG9uZW50LlxuICAgKi9cbiAgaGFuZGxlQ2hhbmdlID0gKGV2ZW50OiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MU2VsZWN0RWxlbWVudD4pOiB2b2lkID0+IHtcbiAgICBpZiAodGhpcy5fbG9nQ29uc29sZS5sb2dnZXIpIHtcbiAgICAgIHRoaXMuX2xvZ0NvbnNvbGUubG9nZ2VyLmxldmVsID0gZXZlbnQudGFyZ2V0LnZhbHVlIGFzIExvZ0xldmVsO1xuICAgIH1cbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9O1xuXG4gIC8qKlxuICAgKiBIYW5kbGUgYGtleWRvd25gIGV2ZW50cyBmb3IgdGhlIEhUTUxTZWxlY3QgY29tcG9uZW50LlxuICAgKi9cbiAgaGFuZGxlS2V5RG93biA9IChldmVudDogUmVhY3QuS2V5Ym9hcmRFdmVudCk6IHZvaWQgPT4ge1xuICAgIGlmIChldmVudC5rZXlDb2RlID09PSAxMykge1xuICAgICAgdGhpcy5fbG9nQ29uc29sZS5hY3RpdmF0ZSgpO1xuICAgIH1cbiAgfTtcblxuICByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgIGNvbnN0IGxvZ2dlciA9IHRoaXMuX2xvZ0NvbnNvbGUubG9nZ2VyO1xuICAgIHJldHVybiAoXG4gICAgICA8PlxuICAgICAgICA8bGFiZWxcbiAgICAgICAgICBodG1sRm9yPXt0aGlzLl9pZH1cbiAgICAgICAgICBjbGFzc05hbWU9e1xuICAgICAgICAgICAgbG9nZ2VyID09PSBudWxsXG4gICAgICAgICAgICAgID8gJ2pwLUxvZ0NvbnNvbGUtdG9vbGJhckxvZ0xldmVsLWRpc2FibGVkJ1xuICAgICAgICAgICAgICA6IHVuZGVmaW5lZFxuICAgICAgICAgIH1cbiAgICAgICAgPlxuICAgICAgICAgIHt0aGlzLl90cmFucy5fXygnTG9nIExldmVsOicpfVxuICAgICAgICA8L2xhYmVsPlxuICAgICAgICA8SFRNTFNlbGVjdFxuICAgICAgICAgIGlkPXt0aGlzLl9pZH1cbiAgICAgICAgICBjbGFzc05hbWU9XCJqcC1Mb2dDb25zb2xlLXRvb2xiYXJMb2dMZXZlbERyb3Bkb3duXCJcbiAgICAgICAgICBvbkNoYW5nZT17dGhpcy5oYW5kbGVDaGFuZ2V9XG4gICAgICAgICAgb25LZXlEb3duPXt0aGlzLmhhbmRsZUtleURvd259XG4gICAgICAgICAgdmFsdWU9e2xvZ2dlcj8ubGV2ZWx9XG4gICAgICAgICAgYXJpYS1sYWJlbD17dGhpcy5fdHJhbnMuX18oJ0xvZyBsZXZlbCcpfVxuICAgICAgICAgIGRpc2FibGVkPXtsb2dnZXIgPT09IG51bGx9XG4gICAgICAgICAgb3B0aW9ucz17XG4gICAgICAgICAgICBsb2dnZXIgPT09IG51bGxcbiAgICAgICAgICAgICAgPyBbXVxuICAgICAgICAgICAgICA6IFtcbiAgICAgICAgICAgICAgICAgIFt0aGlzLl90cmFucy5fXygnQ3JpdGljYWwnKSwgJ0NyaXRpY2FsJ10sXG4gICAgICAgICAgICAgICAgICBbdGhpcy5fdHJhbnMuX18oJ0Vycm9yJyksICdFcnJvciddLFxuICAgICAgICAgICAgICAgICAgW3RoaXMuX3RyYW5zLl9fKCdXYXJuaW5nJyksICdXYXJuaW5nJ10sXG4gICAgICAgICAgICAgICAgICBbdGhpcy5fdHJhbnMuX18oJ0luZm8nKSwgJ0luZm8nXSxcbiAgICAgICAgICAgICAgICAgIFt0aGlzLl90cmFucy5fXygnRGVidWcnKSwgJ0RlYnVnJ11cbiAgICAgICAgICAgICAgICBdLm1hcChkYXRhID0+ICh7XG4gICAgICAgICAgICAgICAgICBsYWJlbDogZGF0YVswXSxcbiAgICAgICAgICAgICAgICAgIHZhbHVlOiBkYXRhWzFdLnRvTG93ZXJDYXNlKClcbiAgICAgICAgICAgICAgICB9KSlcbiAgICAgICAgICB9XG4gICAgICAgIC8+XG4gICAgICA8Lz5cbiAgICApO1xuICB9XG5cbiAgcHJvdGVjdGVkIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF90cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gIHByaXZhdGUgX2xvZ0NvbnNvbGU6IExvZ0NvbnNvbGVQYW5lbDtcbiAgcHJpdmF0ZSBfaWQgPSBgbGV2ZWwtJHtVVUlELnV1aWQ0KCl9YDtcbn1cblxuZXhwb3J0IGRlZmF1bHQgbG9nQ29uc29sZVBsdWdpbjtcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHtcbiAgSUNvbnRlbnRDaGFuZ2UsXG4gIElMb2dnZXIsXG4gIElMb2dnZXJSZWdpc3RyeVxufSBmcm9tICdAanVweXRlcmxhYi9sb2djb25zb2xlJztcbmltcG9ydCB7IEdyb3VwSXRlbSwgVGV4dEl0ZW0gfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgbGlzdEljb24sIFZEb21Nb2RlbCwgVkRvbVJlbmRlcmVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG4vKipcbiAqIEEgcHVyZSBmdW5jdGlvbmFsIGNvbXBvbmVudCBmb3IgYSBMb2cgQ29uc29sZSBzdGF0dXMgaXRlbS5cbiAqXG4gKiBAcGFyYW0gcHJvcHMgLSB0aGUgcHJvcHMgZm9yIHRoZSBjb21wb25lbnQuXG4gKlxuICogQHJldHVybnMgYSB0c3ggY29tcG9uZW50IGZvciByZW5kZXJpbmcgdGhlIExvZyBDb25zb2xlIHN0YXR1cy5cbiAqL1xuZnVuY3Rpb24gTG9nQ29uc29sZVN0YXR1c0NvbXBvbmVudChcbiAgcHJvcHM6IExvZ0NvbnNvbGVTdGF0dXNDb21wb25lbnQuSVByb3BzXG4pOiBSZWFjdC5SZWFjdEVsZW1lbnQ8TG9nQ29uc29sZVN0YXR1c0NvbXBvbmVudC5JUHJvcHM+IHtcbiAgY29uc3QgdHJhbnNsYXRvciA9IHByb3BzLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGxldCB0aXRsZSA9ICcnO1xuICBpZiAocHJvcHMubmV3TWVzc2FnZXMgPiAwKSB7XG4gICAgdGl0bGUgPSB0cmFucy5fXyhcbiAgICAgICclMSBuZXcgbWVzc2FnZXMsICUyIGxvZyBlbnRyaWVzIGZvciAlMycsXG4gICAgICBwcm9wcy5uZXdNZXNzYWdlcyxcbiAgICAgIHByb3BzLmxvZ0VudHJpZXMsXG4gICAgICBwcm9wcy5zb3VyY2VcbiAgICApO1xuICB9IGVsc2Uge1xuICAgIHRpdGxlICs9IHRyYW5zLl9fKCclMSBsb2cgZW50cmllcyBmb3IgJTInLCBwcm9wcy5sb2dFbnRyaWVzLCBwcm9wcy5zb3VyY2UpO1xuICB9XG4gIHJldHVybiAoXG4gICAgPEdyb3VwSXRlbSBzcGFjaW5nPXswfSBvbkNsaWNrPXtwcm9wcy5oYW5kbGVDbGlja30gdGl0bGU9e3RpdGxlfT5cbiAgICAgIDxsaXN0SWNvbi5yZWFjdCB0b3A9eycycHgnfSBzdHlsZXNoZWV0PXsnc3RhdHVzQmFyJ30gLz5cbiAgICAgIHtwcm9wcy5uZXdNZXNzYWdlcyA+IDAgPyA8VGV4dEl0ZW0gc291cmNlPXtwcm9wcy5uZXdNZXNzYWdlc30gLz4gOiA8PjwvPn1cbiAgICA8L0dyb3VwSXRlbT5cbiAgKTtcbn1cblxuLypcbiAqIEEgbmFtZXNwYWNlIGZvciBMb2dDb25zb2xlU3RhdHVzQ29tcG9uZW50LlxuICovXG5uYW1lc3BhY2UgTG9nQ29uc29sZVN0YXR1c0NvbXBvbmVudCB7XG4gIC8qKlxuICAgKiBUaGUgcHJvcHMgZm9yIHRoZSBMb2dDb25zb2xlU3RhdHVzQ29tcG9uZW50LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIEEgY2xpY2sgaGFuZGxlciBmb3IgdGhlIGl0ZW0uIEJ5IGRlZmF1bHRcbiAgICAgKiBMb2cgQ29uc29sZSBwYW5lbCBpcyBsYXVuY2hlZC5cbiAgICAgKi9cbiAgICBoYW5kbGVDbGljazogKCkgPT4gdm9pZDtcblxuICAgIC8qKlxuICAgICAqIE51bWJlciBvZiBsb2cgZW50cmllcy5cbiAgICAgKi9cbiAgICBsb2dFbnRyaWVzOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBOdW1iZXIgb2YgbmV3IGxvZyBtZXNzYWdlcy5cbiAgICAgKi9cbiAgICBuZXdNZXNzYWdlczogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogTG9nIHNvdXJjZSBuYW1lXG4gICAgICovXG4gICAgc291cmNlOiBzdHJpbmcgfCBudWxsO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0b3JcbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG4gIH1cbn1cblxuLyoqXG4gKiBBIFZEb21SZW5kZXJlciB3aWRnZXQgZm9yIGRpc3BsYXlpbmcgdGhlIHN0YXR1cyBvZiBMb2cgQ29uc29sZSBsb2dzLlxuICovXG5leHBvcnQgY2xhc3MgTG9nQ29uc29sZVN0YXR1cyBleHRlbmRzIFZEb21SZW5kZXJlcjxMb2dDb25zb2xlU3RhdHVzLk1vZGVsPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgdGhlIGxvZyBjb25zb2xlIHN0YXR1cyB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIHN0YXR1cyB3aWRnZXQgaW5pdGlhbGl6YXRpb24gb3B0aW9ucy5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IExvZ0NvbnNvbGVTdGF0dXMuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihuZXcgTG9nQ29uc29sZVN0YXR1cy5Nb2RlbChvcHRpb25zLmxvZ2dlclJlZ2lzdHJ5KSk7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gb3B0aW9ucy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIHRoaXMuX2hhbmRsZUNsaWNrID0gb3B0aW9ucy5oYW5kbGVDbGljaztcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1tb2QtaGlnaGxpZ2h0ZWQnKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1Mb2dDb25zb2xlU3RhdHVzSXRlbScpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciB0aGUgbG9nIGNvbnNvbGUgc3RhdHVzIGl0ZW0uXG4gICAqL1xuICByZW5kZXIoKTogSlNYLkVsZW1lbnQgfCBudWxsIHtcbiAgICBpZiAodGhpcy5tb2RlbCA9PT0gbnVsbCB8fCB0aGlzLm1vZGVsLnZlcnNpb24gPT09IDApIHtcbiAgICAgIHJldHVybiBudWxsO1xuICAgIH1cblxuICAgIGNvbnN0IHtcbiAgICAgIGZsYXNoRW5hYmxlZCxcbiAgICAgIG1lc3NhZ2VzLFxuICAgICAgc291cmNlLFxuICAgICAgdmVyc2lvbixcbiAgICAgIHZlcnNpb25EaXNwbGF5ZWQsXG4gICAgICB2ZXJzaW9uTm90aWZpZWRcbiAgICB9ID0gdGhpcy5tb2RlbDtcbiAgICBpZiAoc291cmNlICE9PSBudWxsICYmIGZsYXNoRW5hYmxlZCAmJiB2ZXJzaW9uID4gdmVyc2lvbk5vdGlmaWVkKSB7XG4gICAgICB0aGlzLl9mbGFzaEhpZ2hsaWdodCgpO1xuICAgICAgdGhpcy5tb2RlbC5zb3VyY2VOb3RpZmllZChzb3VyY2UsIHZlcnNpb24pO1xuICAgIH0gZWxzZSBpZiAoc291cmNlICE9PSBudWxsICYmIGZsYXNoRW5hYmxlZCAmJiB2ZXJzaW9uID4gdmVyc2lvbkRpc3BsYXllZCkge1xuICAgICAgdGhpcy5fc2hvd0hpZ2hsaWdodGVkKCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2NsZWFySGlnaGxpZ2h0KCk7XG4gICAgfVxuXG4gICAgcmV0dXJuIChcbiAgICAgIDxMb2dDb25zb2xlU3RhdHVzQ29tcG9uZW50XG4gICAgICAgIGhhbmRsZUNsaWNrPXt0aGlzLl9oYW5kbGVDbGlja31cbiAgICAgICAgbG9nRW50cmllcz17bWVzc2FnZXN9XG4gICAgICAgIG5ld01lc3NhZ2VzPXt2ZXJzaW9uIC0gdmVyc2lvbkRpc3BsYXllZH1cbiAgICAgICAgc291cmNlPXt0aGlzLm1vZGVsLnNvdXJjZX1cbiAgICAgICAgdHJhbnNsYXRvcj17dGhpcy50cmFuc2xhdG9yfVxuICAgICAgLz5cbiAgICApO1xuICB9XG5cbiAgcHJpdmF0ZSBfZmxhc2hIaWdobGlnaHQoKSB7XG4gICAgdGhpcy5fc2hvd0hpZ2hsaWdodGVkKCk7XG5cbiAgICAvLyBUbyBtYWtlIHN1cmUgdGhlIGJyb3dzZXIgdHJpZ2dlcnMgdGhlIGFuaW1hdGlvbiwgd2UgcmVtb3ZlIHRoZSBjbGFzcyxcbiAgICAvLyB3YWl0IGZvciBhbiBhbmltYXRpb24gZnJhbWUsIHRoZW4gYWRkIGl0IGJhY2tcbiAgICB0aGlzLnJlbW92ZUNsYXNzKCdqcC1Mb2dDb25zb2xlLWZsYXNoJyk7XG4gICAgcmVxdWVzdEFuaW1hdGlvbkZyYW1lKCgpID0+IHtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLUxvZ0NvbnNvbGUtZmxhc2gnKTtcbiAgICB9KTtcbiAgfVxuXG4gIHByaXZhdGUgX3Nob3dIaWdobGlnaHRlZCgpIHtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1tb2Qtc2VsZWN0ZWQnKTtcbiAgfVxuXG4gIHByaXZhdGUgX2NsZWFySGlnaGxpZ2h0KCkge1xuICAgIHRoaXMucmVtb3ZlQ2xhc3MoJ2pwLUxvZ0NvbnNvbGUtZmxhc2gnKTtcbiAgICB0aGlzLnJlbW92ZUNsYXNzKCdqcC1tb2Qtc2VsZWN0ZWQnKTtcbiAgfVxuXG4gIHJlYWRvbmx5IHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9oYW5kbGVDbGljazogKCkgPT4gdm9pZDtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgTG9nIENvbnNvbGUgbG9nIHN0YXR1cy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBMb2dDb25zb2xlU3RhdHVzIHtcbiAgLyoqXG4gICAqIEEgVkRvbU1vZGVsIGZvciB0aGUgTG9nQ29uc29sZVN0YXR1cyBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgTG9nQ29uc29sZVN0YXR1cyBtb2RlbC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBsb2dnZXJSZWdpc3RyeSAtIFRoZSBsb2dnZXIgcmVnaXN0cnkgcHJvdmlkaW5nIHRoZSBsb2dzLlxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKGxvZ2dlclJlZ2lzdHJ5OiBJTG9nZ2VyUmVnaXN0cnkpIHtcbiAgICAgIHN1cGVyKCk7XG5cbiAgICAgIHRoaXMuX2xvZ2dlclJlZ2lzdHJ5ID0gbG9nZ2VyUmVnaXN0cnk7XG4gICAgICB0aGlzLl9sb2dnZXJSZWdpc3RyeS5yZWdpc3RyeUNoYW5nZWQuY29ubmVjdChcbiAgICAgICAgdGhpcy5faGFuZGxlTG9nUmVnaXN0cnlDaGFuZ2UsXG4gICAgICAgIHRoaXNcbiAgICAgICk7XG4gICAgICB0aGlzLl9oYW5kbGVMb2dSZWdpc3RyeUNoYW5nZSgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIE51bWJlciBvZiBtZXNzYWdlcyBjdXJyZW50bHkgaW4gdGhlIGN1cnJlbnQgc291cmNlLlxuICAgICAqL1xuICAgIGdldCBtZXNzYWdlcygpOiBudW1iZXIge1xuICAgICAgaWYgKHRoaXMuX3NvdXJjZSA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm4gMDtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGxvZ2dlciA9IHRoaXMuX2xvZ2dlclJlZ2lzdHJ5LmdldExvZ2dlcih0aGlzLl9zb3VyY2UpO1xuICAgICAgcmV0dXJuIGxvZ2dlci5sZW5ndGg7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIG51bWJlciBvZiBtZXNzYWdlcyBldmVyIHN0b3JlZCBieSB0aGUgY3VycmVudCBzb3VyY2UuXG4gICAgICovXG4gICAgZ2V0IHZlcnNpb24oKTogbnVtYmVyIHtcbiAgICAgIGlmICh0aGlzLl9zb3VyY2UgPT09IG51bGwpIHtcbiAgICAgICAgcmV0dXJuIDA7XG4gICAgICB9XG4gICAgICBjb25zdCBsb2dnZXIgPSB0aGlzLl9sb2dnZXJSZWdpc3RyeS5nZXRMb2dnZXIodGhpcy5fc291cmNlKTtcbiAgICAgIHJldHVybiBsb2dnZXIudmVyc2lvbjtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZSBvZiB0aGUgYWN0aXZlIGxvZyBzb3VyY2VcbiAgICAgKi9cbiAgICBnZXQgc291cmNlKCk6IHN0cmluZyB8IG51bGwge1xuICAgICAgcmV0dXJuIHRoaXMuX3NvdXJjZTtcbiAgICB9XG5cbiAgICBzZXQgc291cmNlKG5hbWU6IHN0cmluZyB8IG51bGwpIHtcbiAgICAgIGlmICh0aGlzLl9zb3VyY2UgPT09IG5hbWUpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICB0aGlzLl9zb3VyY2UgPSBuYW1lO1xuXG4gICAgICAvLyByZWZyZXNoIHJlbmRlcmluZ1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBsYXN0IHNvdXJjZSB2ZXJzaW9uIHRoYXQgd2FzIGRpc3BsYXllZC5cbiAgICAgKi9cbiAgICBnZXQgdmVyc2lvbkRpc3BsYXllZCgpOiBudW1iZXIge1xuICAgICAgaWYgKHRoaXMuX3NvdXJjZSA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm4gMDtcbiAgICAgIH1cbiAgICAgIHJldHVybiB0aGlzLl9zb3VyY2VWZXJzaW9uLmdldCh0aGlzLl9zb3VyY2UpPy5sYXN0RGlzcGxheWVkID8/IDA7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGxhc3Qgc291cmNlIHZlcnNpb24gd2Ugbm90aWZpZWQgdGhlIHVzZXIgYWJvdXQuXG4gICAgICovXG4gICAgZ2V0IHZlcnNpb25Ob3RpZmllZCgpOiBudW1iZXIge1xuICAgICAgaWYgKHRoaXMuX3NvdXJjZSA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm4gMDtcbiAgICAgIH1cbiAgICAgIHJldHVybiB0aGlzLl9zb3VyY2VWZXJzaW9uLmdldCh0aGlzLl9zb3VyY2UpPy5sYXN0Tm90aWZpZWQgPz8gMDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBGbGFnIHRvIHRvZ2dsZSBmbGFzaGluZyB3aGVuIG5ldyBsb2dzIGFkZGVkLlxuICAgICAqL1xuICAgIGdldCBmbGFzaEVuYWJsZWQoKTogYm9vbGVhbiB7XG4gICAgICByZXR1cm4gdGhpcy5fZmxhc2hFbmFibGVkO1xuICAgIH1cblxuICAgIHNldCBmbGFzaEVuYWJsZWQoZW5hYmxlZDogYm9vbGVhbikge1xuICAgICAgaWYgKHRoaXMuX2ZsYXNoRW5hYmxlZCA9PT0gZW5hYmxlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIHRoaXMuX2ZsYXNoRW5hYmxlZCA9IGVuYWJsZWQ7XG4gICAgICB0aGlzLmZsYXNoRW5hYmxlZENoYW5nZWQuZW1pdCgpO1xuXG4gICAgICAvLyByZWZyZXNoIHJlbmRlcmluZ1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlY29yZCB0aGUgbGFzdCBzb3VyY2UgdmVyc2lvbiBkaXNwbGF5ZWQgdG8gdGhlIHVzZXIuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gc291cmNlIC0gVGhlIG5hbWUgb2YgdGhlIGxvZyBzb3VyY2UuXG4gICAgICogQHBhcmFtIHZlcnNpb24gLSBUaGUgdmVyc2lvbiBvZiB0aGUgbG9nIHRoYXQgd2FzIGRpc3BsYXllZC5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIHdpbGwgYWxzbyB1cGRhdGUgdGhlIGxhc3Qgbm90aWZpZWQgdmVyc2lvbiBzbyB0aGF0IHRoZSBsYXN0XG4gICAgICogbm90aWZpZWQgdmVyc2lvbiBpcyBhbHdheXMgYXQgbGVhc3QgdGhlIGxhc3QgZGlzcGxheWVkIHZlcnNpb24uXG4gICAgICovXG4gICAgc291cmNlRGlzcGxheWVkKHNvdXJjZTogc3RyaW5nIHwgbnVsbCwgdmVyc2lvbjogbnVtYmVyIHwgbnVsbCk6IHZvaWQge1xuICAgICAgaWYgKHNvdXJjZSA9PT0gbnVsbCB8fCB2ZXJzaW9uID09PSBudWxsKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHZlcnNpb25zID0gdGhpcy5fc291cmNlVmVyc2lvbi5nZXQoc291cmNlKSE7XG4gICAgICBsZXQgY2hhbmdlID0gZmFsc2U7XG4gICAgICBpZiAodmVyc2lvbnMubGFzdERpc3BsYXllZCA8IHZlcnNpb24pIHtcbiAgICAgICAgdmVyc2lvbnMubGFzdERpc3BsYXllZCA9IHZlcnNpb247XG4gICAgICAgIGNoYW5nZSA9IHRydWU7XG4gICAgICB9XG4gICAgICBpZiAodmVyc2lvbnMubGFzdE5vdGlmaWVkIDwgdmVyc2lvbikge1xuICAgICAgICB2ZXJzaW9ucy5sYXN0Tm90aWZpZWQgPSB2ZXJzaW9uO1xuICAgICAgICBjaGFuZ2UgPSB0cnVlO1xuICAgICAgfVxuICAgICAgaWYgKGNoYW5nZSAmJiBzb3VyY2UgPT09IHRoaXMuX3NvdXJjZSkge1xuICAgICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KCk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVjb3JkIGEgc291cmNlIHZlcnNpb24gd2Ugbm90aWZpZWQgdGhlIHVzZXIgYWJvdXQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gc291cmNlIC0gVGhlIG5hbWUgb2YgdGhlIGxvZyBzb3VyY2UuXG4gICAgICogQHBhcmFtIHZlcnNpb24gLSBUaGUgdmVyc2lvbiBvZiB0aGUgbG9nLlxuICAgICAqL1xuICAgIHNvdXJjZU5vdGlmaWVkKHNvdXJjZTogc3RyaW5nIHwgbnVsbCwgdmVyc2lvbjogbnVtYmVyKTogdm9pZCB7XG4gICAgICBpZiAoc291cmNlID09PSBudWxsKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHZlcnNpb25zID0gdGhpcy5fc291cmNlVmVyc2lvbi5nZXQoc291cmNlKTtcbiAgICAgIGlmICh2ZXJzaW9ucyEubGFzdE5vdGlmaWVkIDwgdmVyc2lvbikge1xuICAgICAgICB2ZXJzaW9ucyEubGFzdE5vdGlmaWVkID0gdmVyc2lvbjtcbiAgICAgICAgaWYgKHNvdXJjZSA9PT0gdGhpcy5fc291cmNlKSB7XG4gICAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfaGFuZGxlTG9nUmVnaXN0cnlDaGFuZ2UoKSB7XG4gICAgICBjb25zdCBsb2dnZXJzID0gdGhpcy5fbG9nZ2VyUmVnaXN0cnkuZ2V0TG9nZ2VycygpO1xuICAgICAgZm9yIChjb25zdCBsb2dnZXIgb2YgbG9nZ2Vycykge1xuICAgICAgICBpZiAoIXRoaXMuX3NvdXJjZVZlcnNpb24uaGFzKGxvZ2dlci5zb3VyY2UpKSB7XG4gICAgICAgICAgbG9nZ2VyLmNvbnRlbnRDaGFuZ2VkLmNvbm5lY3QodGhpcy5faGFuZGxlTG9nQ29udGVudENoYW5nZSwgdGhpcyk7XG4gICAgICAgICAgdGhpcy5fc291cmNlVmVyc2lvbi5zZXQobG9nZ2VyLnNvdXJjZSwge1xuICAgICAgICAgICAgbGFzdERpc3BsYXllZDogMCxcbiAgICAgICAgICAgIGxhc3ROb3RpZmllZDogMFxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfaGFuZGxlTG9nQ29udGVudENoYW5nZShcbiAgICAgIHsgc291cmNlIH06IElMb2dnZXIsXG4gICAgICBjaGFuZ2U6IElDb250ZW50Q2hhbmdlXG4gICAgKSB7XG4gICAgICBpZiAoc291cmNlID09PSB0aGlzLl9zb3VyY2UpIHtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgZmxhc2ggZW5hYmxlbWVudCBjaGFuZ2VzLlxuICAgICAqL1xuICAgIHB1YmxpYyBmbGFzaEVuYWJsZWRDaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCB2b2lkPih0aGlzKTtcbiAgICBwcml2YXRlIF9mbGFzaEVuYWJsZWQ6IGJvb2xlYW4gPSB0cnVlO1xuICAgIHByaXZhdGUgX2xvZ2dlclJlZ2lzdHJ5OiBJTG9nZ2VyUmVnaXN0cnk7XG4gICAgcHJpdmF0ZSBfc291cmNlOiBzdHJpbmcgfCBudWxsID0gbnVsbDtcbiAgICAvKipcbiAgICAgKiBUaGUgdmlldyBzdGF0dXMgb2YgZWFjaCBzb3VyY2UuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogS2V5cyBhcmUgc291cmNlIG5hbWVzLCB2YWx1ZSBpcyBhIGxpc3Qgb2YgdHdvIG51bWJlcnMuIFRoZSBmaXJzdFxuICAgICAqIHJlcHJlc2VudHMgdGhlIHZlcnNpb24gb2YgdGhlIG1lc3NhZ2VzIHRoYXQgd2FzIGxhc3QgZGlzcGxheWVkIHRvIHRoZVxuICAgICAqIHVzZXIsIHRoZSBzZWNvbmQgcmVwcmVzZW50cyB0aGUgdmVyc2lvbiB0aGF0IHdlIGxhc3Qgbm90aWZpZWQgdGhlIHVzZXJcbiAgICAgKiBhYm91dC5cbiAgICAgKi9cbiAgICBwcml2YXRlIF9zb3VyY2VWZXJzaW9uOiBNYXA8c3RyaW5nLCBJVmVyc2lvbkluZm8+ID0gbmV3IE1hcCgpO1xuICB9XG5cbiAgaW50ZXJmYWNlIElWZXJzaW9uSW5mbyB7XG4gICAgbGFzdERpc3BsYXllZDogbnVtYmVyO1xuICAgIGxhc3ROb3RpZmllZDogbnVtYmVyO1xuICB9XG5cbiAgLyoqXG4gICAqIE9wdGlvbnMgZm9yIGNyZWF0aW5nIGEgbmV3IExvZ0NvbnNvbGVTdGF0dXMgaXRlbVxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGxvZ2dlciByZWdpc3RyeSBwcm92aWRpbmcgdGhlIGxvZ3MuXG4gICAgICovXG4gICAgbG9nZ2VyUmVnaXN0cnk6IElMb2dnZXJSZWdpc3RyeTtcblxuICAgIC8qKlxuICAgICAqIEEgY2xpY2sgaGFuZGxlciBmb3IgdGhlIGl0ZW0uIEJ5IGRlZmF1bHRcbiAgICAgKiBMb2cgQ29uc29sZSBwYW5lbCBpcyBsYXVuY2hlZC5cbiAgICAgKi9cbiAgICBoYW5kbGVDbGljazogKCkgPT4gdm9pZDtcblxuICAgIC8qKlxuICAgICAqIExhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=