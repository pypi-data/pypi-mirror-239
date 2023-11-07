"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_debugger-extension_lib_index_js"],{

/***/ "../packages/debugger-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/debugger-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/debugger */ "webpack/sharing/consume/default/@jupyterlab/debugger/@jupyterlab/debugger");
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole/@jupyterlab/logconsole");
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module debugger-extension
 */














function notifyCommands(app) {
    Object.values(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs).forEach(command => {
        if (app.commands.hasCommand(command)) {
            app.commands.notifyCommandChanged(command);
        }
    });
}
/**
 * A plugin that provides visual debugging support for consoles.
 */
const consoles = {
    // FIXME This should be in @jupyterlab/console-extension
    id: '@jupyterlab/debugger-extension:consoles',
    description: 'Add debugger capability to the consoles.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, debug, consoleTracker, labShell) => {
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'console',
            shell: app.shell,
            service: debug
        });
        const updateHandlerAndCommands = async (widget) => {
            const { sessionContext } = widget;
            await sessionContext.ready;
            await handler.updateContext(widget, sessionContext);
            notifyCommands(app);
        };
        if (labShell) {
            labShell.currentChanged.connect((_, update) => {
                const widget = update.newValue;
                if (widget instanceof _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.ConsolePanel) {
                    void updateHandlerAndCommands(widget);
                }
            });
        }
        else {
            consoleTracker.currentChanged.connect((_, consolePanel) => {
                if (consolePanel) {
                    void updateHandlerAndCommands(consolePanel);
                }
            });
        }
    }
};
/**
 * A plugin that provides visual debugging support for file editors.
 */
const files = {
    // FIXME This should be in @jupyterlab/fileeditor-extension
    id: '@jupyterlab/debugger-extension:files',
    description: 'Adds debugger capabilities to files.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.IEditorTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, debug, editorTracker, labShell) => {
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'file',
            shell: app.shell,
            service: debug
        });
        const activeSessions = {};
        const updateHandlerAndCommands = async (widget) => {
            const sessions = app.serviceManager.sessions;
            try {
                const model = await sessions.findByPath(widget.context.path);
                if (!model) {
                    return;
                }
                let session = activeSessions[model.id];
                if (!session) {
                    // Use `connectTo` only if the session does not exist.
                    // `connectTo` sends a kernel_info_request on the shell
                    // channel, which blocks the debug session restore when waiting
                    // for the kernel to be ready
                    session = sessions.connectTo({ model });
                    activeSessions[model.id] = session;
                }
                await handler.update(widget, session);
                notifyCommands(app);
            }
            catch (_a) {
                return;
            }
        };
        if (labShell) {
            labShell.currentChanged.connect((_, update) => {
                const widget = update.newValue;
                if (widget instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_7__.DocumentWidget) {
                    const { content } = widget;
                    if (content instanceof _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.FileEditor) {
                        void updateHandlerAndCommands(widget);
                    }
                }
            });
        }
        else {
            editorTracker.currentChanged.connect((_, documentWidget) => {
                if (documentWidget) {
                    void updateHandlerAndCommands(documentWidget);
                }
            });
        }
    }
};
/**
 * A plugin that provides visual debugging support for notebooks.
 */
const notebooks = {
    // FIXME This should be in @jupyterlab/notebook-extension
    id: '@jupyterlab/debugger-extension:notebooks',
    description: 'Adds debugger capability to notebooks and provides the debugger notebook handler.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.INotebookTracker],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerHandler,
    activate: (app, service, notebookTracker, labShell, palette, sessionDialogs_, translator_) => {
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.nullTranslator;
        const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SessionContextDialogs({ translator });
        const handler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Handler({
            type: 'notebook',
            shell: app.shell,
            service
        });
        const trans = translator.load('jupyterlab');
        app.commands.addCommand(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs.restartDebug, {
            label: trans.__('Restart Kernel and Debug…'),
            caption: trans.__('Restart Kernel and Debug…'),
            isEnabled: () => service.isStarted,
            execute: async () => {
                const state = service.getDebuggerState();
                await service.stop();
                const widget = notebookTracker.currentWidget;
                if (!widget) {
                    return;
                }
                const { content, sessionContext } = widget;
                const restarted = await sessionDialogs.restart(sessionContext);
                if (!restarted) {
                    return;
                }
                await service.restoreDebuggerState(state);
                await handler.updateWidget(widget, sessionContext.session);
                await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookActions.runAll(content, sessionContext, sessionDialogs, translator);
            }
        });
        const updateHandlerAndCommands = async (widget) => {
            if (widget) {
                const { sessionContext } = widget;
                await sessionContext.ready;
                await handler.updateContext(widget, sessionContext);
            }
            notifyCommands(app);
        };
        if (labShell) {
            labShell.currentChanged.connect((_, update) => {
                const widget = update.newValue;
                if (widget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel) {
                    void updateHandlerAndCommands(widget);
                }
            });
        }
        else {
            notebookTracker.currentChanged.connect((_, notebookPanel) => {
                if (notebookPanel) {
                    void updateHandlerAndCommands(notebookPanel);
                }
            });
        }
        if (palette) {
            palette.addItem({
                category: 'Notebook Operations',
                command: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs.restartDebug
            });
        }
        return handler;
    }
};
/**
 * A plugin that provides a debugger service.
 */
const service = {
    id: '@jupyterlab/debugger-extension:service',
    description: 'Provides the debugger service.',
    autoStart: true,
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig],
    optional: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    activate: (app, config, debuggerSources, translator) => new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Service({
        config,
        debuggerSources,
        specsManager: app.serviceManager.kernelspecs,
        translator
    })
};
/**
 * A plugin that provides a configuration with hash method.
 */
const configuration = {
    id: '@jupyterlab/debugger-extension:config',
    description: 'Provides the debugger configuration',
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig,
    autoStart: true,
    activate: () => new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Config()
};
/**
 * A plugin that provides source/editor functionality for debugging.
 */
const sources = {
    id: '@jupyterlab/debugger-extension:sources',
    description: 'Provides the source feature for debugging',
    autoStart: true,
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerConfig, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices],
    optional: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.INotebookTracker, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_8__.IEditorTracker],
    activate: (app, config, editorServices, notebookTracker, consoleTracker, editorTracker) => {
        return new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Sources({
            config,
            shell: app.shell,
            editorServices,
            notebookTracker,
            consoleTracker,
            editorTracker
        });
    }
};
/*
 * A plugin to open detailed views for variables.
 */
const variables = {
    id: '@jupyterlab/debugger-extension:variables',
    description: 'Adds variables renderer and inspection in the debugger variable panel.',
    autoStart: true,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerHandler, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.IRenderMimeRegistry],
    activate: (app, service, handler, translator, themeManager, rendermime) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'debugger/inspect-variable'
        });
        const trackerMime = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: 'debugger/render-variable'
        });
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        // Add commands
        commands.addCommand(CommandIDs.inspectVariable, {
            label: trans.__('Inspect Variable'),
            caption: trans.__('Inspect Variable'),
            isEnabled: args => {
                var _a, _b, _c, _d;
                return !!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted) &&
                    Number((_d = (_b = args.variableReference) !== null && _b !== void 0 ? _b : (_c = service.model.variables.selectedVariable) === null || _c === void 0 ? void 0 : _c.variablesReference) !== null && _d !== void 0 ? _d : 0) > 0;
            },
            execute: async (args) => {
                var _a, _b, _c, _d;
                let { variableReference, name } = args;
                if (!variableReference) {
                    variableReference =
                        (_a = service.model.variables.selectedVariable) === null || _a === void 0 ? void 0 : _a.variablesReference;
                }
                if (!name) {
                    name = (_b = service.model.variables.selectedVariable) === null || _b === void 0 ? void 0 : _b.name;
                }
                const id = `jp-debugger-variable-${name}`;
                if (!name ||
                    !variableReference ||
                    tracker.find(widget => widget.id === id)) {
                    return;
                }
                const variables = await service.inspectVariable(variableReference);
                if (!variables || variables.length === 0) {
                    return;
                }
                const model = service.model.variables;
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                    content: new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.VariablesGrid({
                        model,
                        commands,
                        scopes: [{ name, variables }],
                        themeManager
                    })
                });
                widget.addClass('jp-DebuggerVariables');
                widget.id = id;
                widget.title.icon = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.variableIcon;
                widget.title.label = `${(_d = (_c = service.session) === null || _c === void 0 ? void 0 : _c.connection) === null || _d === void 0 ? void 0 : _d.name} - ${name}`;
                void tracker.add(widget);
                const disposeWidget = () => {
                    widget.dispose();
                    model.changed.disconnect(disposeWidget);
                };
                model.changed.connect(disposeWidget);
                shell.add(widget, 'main', {
                    mode: tracker.currentWidget ? 'split-right' : 'split-bottom',
                    activate: false,
                    type: 'Debugger Variables'
                });
            }
        });
        commands.addCommand(CommandIDs.renderMimeVariable, {
            label: trans.__('Render Variable'),
            caption: trans.__('Render variable according to its mime type'),
            isEnabled: () => { var _a; return !!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted); },
            isVisible: () => service.model.hasRichVariableRendering &&
                (rendermime !== null || handler.activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel),
            execute: args => {
                var _a, _b, _c, _d, _e, _f, _g, _h;
                let { name, frameId } = args;
                if (!name) {
                    name = (_a = service.model.variables.selectedVariable) === null || _a === void 0 ? void 0 : _a.name;
                }
                if (!frameId) {
                    frameId = (_b = service.model.callstack.frame) === null || _b === void 0 ? void 0 : _b.id;
                }
                const activeWidget = handler.activeWidget;
                let activeRendermime = activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel
                    ? activeWidget.content.rendermime
                    : rendermime;
                if (!activeRendermime) {
                    return;
                }
                const id = `jp-debugger-variable-mime-${name}-${(_d = (_c = service.session) === null || _c === void 0 ? void 0 : _c.connection) === null || _d === void 0 ? void 0 : _d.path.replace('/', '-')}`;
                if (!name || // Name is mandatory
                    trackerMime.find(widget => widget.id === id) || // Widget already exists
                    (!frameId && service.hasStoppedThreads()) // frame id missing on breakpoint
                ) {
                    return;
                }
                const variablesModel = service.model.variables;
                const widget = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.VariableRenderer({
                    dataLoader: () => service.inspectRichVariable(name, frameId),
                    rendermime: activeRendermime,
                    translator
                });
                widget.addClass('jp-DebuggerRichVariable');
                widget.id = id;
                widget.title.icon = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.variableIcon;
                widget.title.label = `${name} - ${(_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.name}`;
                widget.title.caption = `${name} - ${(_h = (_g = service.session) === null || _g === void 0 ? void 0 : _g.connection) === null || _h === void 0 ? void 0 : _h.path}`;
                void trackerMime.add(widget);
                const disposeWidget = () => {
                    widget.dispose();
                    variablesModel.changed.disconnect(refreshWidget);
                    activeWidget === null || activeWidget === void 0 ? void 0 : activeWidget.disposed.disconnect(disposeWidget);
                };
                const refreshWidget = () => {
                    // Refresh the widget only if the active element is the same.
                    if (handler.activeWidget === activeWidget) {
                        void widget.refresh();
                    }
                };
                widget.disposed.connect(disposeWidget);
                variablesModel.changed.connect(refreshWidget);
                activeWidget === null || activeWidget === void 0 ? void 0 : activeWidget.disposed.connect(disposeWidget);
                shell.add(widget, 'main', {
                    mode: trackerMime.currentWidget ? 'split-right' : 'split-bottom',
                    activate: false,
                    type: 'Debugger Variables'
                });
            }
        });
        commands.addCommand(CommandIDs.copyToClipboard, {
            label: trans.__('Copy to Clipboard'),
            caption: trans.__('Copy text representation of the value to clipboard'),
            isEnabled: () => {
                var _a, _b;
                return (!!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted) &&
                    !!((_b = service.model.variables.selectedVariable) === null || _b === void 0 ? void 0 : _b.value));
            },
            isVisible: () => handler.activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel,
            execute: async () => {
                const value = service.model.variables.selectedVariable.value;
                if (value) {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(value);
                }
            }
        });
        commands.addCommand(CommandIDs.copyToGlobals, {
            label: trans.__('Copy Variable to Globals'),
            caption: trans.__('Copy variable to globals scope'),
            isEnabled: () => { var _a; return !!((_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted); },
            isVisible: () => handler.activeWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_10__.NotebookPanel &&
                service.model.supportCopyToGlobals,
            execute: async (args) => {
                const name = service.model.variables.selectedVariable.name;
                await service.copyToGlobals(name);
            }
        });
    }
};
/**
 * Debugger sidebar provider plugin.
 */
const sidebar = {
    id: '@jupyterlab/debugger-extension:sidebar',
    description: 'Provides the debugger sidebar.',
    provides: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSidebar,
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry],
    autoStart: true,
    activate: async (app, service, editorServices, translator, themeManager, settingRegistry) => {
        const { commands } = app;
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        const callstackCommands = {
            registry: commands,
            continue: CommandIDs.debugContinue,
            terminate: CommandIDs.terminate,
            next: CommandIDs.next,
            stepIn: CommandIDs.stepIn,
            stepOut: CommandIDs.stepOut,
            evaluate: CommandIDs.evaluate
        };
        const breakpointsCommands = {
            registry: commands,
            pauseOnExceptions: CommandIDs.pauseOnExceptions
        };
        const sidebar = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Sidebar({
            service,
            callstackCommands,
            breakpointsCommands,
            editorServices,
            themeManager,
            translator
        });
        if (settingRegistry) {
            const setting = await settingRegistry.load(main.id);
            const updateSettings = () => {
                var _a, _b, _c, _d;
                const filters = setting.get('variableFilters').composite;
                const kernel = (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '';
                if (kernel && filters[kernel]) {
                    sidebar.variables.filter = new Set(filters[kernel]);
                }
                const kernelSourcesFilter = setting.get('defaultKernelSourcesFilter')
                    .composite;
                sidebar.kernelSources.filter = kernelSourcesFilter;
            };
            updateSettings();
            setting.changed.connect(updateSettings);
            service.sessionChanged.connect(updateSettings);
        }
        return sidebar;
    }
};
/**
 * The main debugger UI plugin.
 */
const main = {
    id: '@jupyterlab/debugger-extension:main',
    description: 'Initialize the debugger user interface.',
    requires: [_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebugger, _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSidebar, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_13__.ITranslator],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.IDebuggerSources,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_9__.ILoggerRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_12__.ISettingRegistry
    ],
    autoStart: true,
    activate: async (app, service, sidebar, editorServices, translator, palette, debuggerSources, labShell, restorer, loggerRegistry, settingRegistry) => {
        var _a;
        const trans = translator.load('jupyterlab');
        const { commands, shell, serviceManager } = app;
        const { kernelspecs } = serviceManager;
        const CommandIDs = _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.CommandIDs;
        // First check if there is a PageConfig override for the extension visibility
        const alwaysShowDebuggerExtension = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PageConfig.getOption('alwaysShowDebuggerExtension').toLowerCase() ===
            'true';
        if (!alwaysShowDebuggerExtension) {
            // hide the debugger sidebar if no kernel with support for debugging is available
            await kernelspecs.ready;
            const specs = (_a = kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs;
            if (!specs) {
                return;
            }
            const enabled = Object.keys(specs).some(name => { var _a, _b, _c; return !!((_c = (_b = (_a = specs[name]) === null || _a === void 0 ? void 0 : _a.metadata) === null || _b === void 0 ? void 0 : _b['debugger']) !== null && _c !== void 0 ? _c : false); });
            if (!enabled) {
                return;
            }
        }
        // get the mime type of the kernel language for the current debug session
        const getMimeType = async () => {
            var _a, _b, _c;
            const kernel = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel;
            if (!kernel) {
                return '';
            }
            const info = (await kernel.info).language_info;
            const name = info.name;
            const mimeType = (_c = editorServices.mimeTypeService.getMimeTypeByLanguage({ name })) !== null && _c !== void 0 ? _c : '';
            return mimeType;
        };
        const rendermime = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.RenderMimeRegistry({ initialFactories: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_11__.standardRendererFactories });
        commands.addCommand(CommandIDs.evaluate, {
            label: trans.__('Evaluate Code'),
            caption: trans.__('Evaluate Code'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.evaluateIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                var _a, _b, _c;
                const mimeType = await getMimeType();
                const result = await _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Dialogs.getCode({
                    title: trans.__('Evaluate Code'),
                    okLabel: trans.__('Evaluate'),
                    cancelLabel: trans.__('Cancel'),
                    mimeType,
                    contentFactory: new _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_2__.CodeCell.ContentFactory({
                        editorFactory: options => editorServices.factoryService.newInlineEditor(options)
                    }),
                    rendermime
                });
                const code = result.value;
                if (!result.button.accept || !code) {
                    return;
                }
                const reply = await service.evaluate(code);
                if (reply) {
                    const data = reply.result;
                    const path = (_b = (_a = service === null || service === void 0 ? void 0 : service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.path;
                    const logger = path ? (_c = loggerRegistry === null || loggerRegistry === void 0 ? void 0 : loggerRegistry.getLogger) === null || _c === void 0 ? void 0 : _c.call(loggerRegistry, path) : undefined;
                    if (logger) {
                        // print to log console of the notebook currently being debugged
                        logger.log({ type: 'text', data, level: logger.level });
                    }
                    else {
                        // fallback to printing to devtools console
                        console.debug(data);
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.debugContinue, {
            label: () => {
                return service.hasStoppedThreads()
                    ? trans.__('Continue')
                    : trans.__('Pause');
            },
            caption: () => {
                return service.hasStoppedThreads()
                    ? trans.__('Continue')
                    : trans.__('Pause');
            },
            icon: () => {
                return service.hasStoppedThreads()
                    ? _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.continueIcon
                    : _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.pauseIcon;
            },
            isEnabled: () => { var _a, _b; return (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.isStarted) !== null && _b !== void 0 ? _b : false; },
            execute: async () => {
                if (service.hasStoppedThreads()) {
                    await service.continue();
                }
                else {
                    await service.pause();
                }
                commands.notifyCommandChanged(CommandIDs.debugContinue);
            }
        });
        commands.addCommand(CommandIDs.terminate, {
            label: trans.__('Terminate'),
            caption: trans.__('Terminate'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.terminateIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.restart();
                notifyCommands(app);
            }
        });
        commands.addCommand(CommandIDs.next, {
            label: trans.__('Next'),
            caption: trans.__('Next'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepOverIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.next();
            }
        });
        commands.addCommand(CommandIDs.stepIn, {
            label: trans.__('Step In'),
            caption: trans.__('Step In'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepIntoIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.stepIn();
            }
        });
        commands.addCommand(CommandIDs.stepOut, {
            label: trans.__('Step Out'),
            caption: trans.__('Step Out'),
            icon: _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.Icons.stepOutIcon,
            isEnabled: () => service.hasStoppedThreads(),
            execute: async () => {
                await service.stepOut();
            }
        });
        commands.addCommand(CommandIDs.pauseOnExceptions, {
            label: args => args.filter || 'Breakpoints on exception',
            caption: args => args.description,
            isToggled: args => { var _a; return ((_a = service.session) === null || _a === void 0 ? void 0 : _a.isPausingOnException(args.filter)) || false; },
            isEnabled: () => service.pauseOnExceptionsIsValid(),
            execute: async (args) => {
                var _a, _b, _c;
                if (args === null || args === void 0 ? void 0 : args.filter) {
                    let filter = args.filter;
                    await service.pauseOnExceptionsFilter(filter);
                }
                else {
                    let items = [];
                    (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.exceptionBreakpointFilters) === null || _b === void 0 ? void 0 : _b.forEach(availableFilter => {
                        items.push(availableFilter.filter);
                    });
                    const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getMultipleItems({
                        title: trans.__('Select a filter for breakpoints on exception'),
                        items: items,
                        defaults: ((_c = service.session) === null || _c === void 0 ? void 0 : _c.currentExceptionFilters) || []
                    });
                    let filters = result.button.accept ? result.value : null;
                    if (filters !== null) {
                        await service.pauseOnExceptions(filters);
                    }
                }
            }
        });
        let autoCollapseSidebar = false;
        if (settingRegistry) {
            const setting = await settingRegistry.load(main.id);
            const updateSettings = () => {
                autoCollapseSidebar = setting.get('autoCollapseDebuggerSidebar')
                    .composite;
            };
            updateSettings();
            setting.changed.connect(updateSettings);
        }
        service.eventMessage.connect((_, event) => {
            notifyCommands(app);
            if (labShell && event.event === 'initialized') {
                labShell.activateById(sidebar.id);
            }
            else if (labShell &&
                sidebar.isVisible &&
                event.event === 'terminated' &&
                autoCollapseSidebar) {
                labShell.collapseRight();
            }
        });
        service.sessionChanged.connect(_ => {
            notifyCommands(app);
        });
        if (restorer) {
            restorer.add(sidebar, 'debugger-sidebar');
        }
        sidebar.node.setAttribute('role', 'region');
        sidebar.node.setAttribute('aria-label', trans.__('Debugger section'));
        sidebar.title.caption = trans.__('Debugger');
        shell.add(sidebar, 'right', { type: 'Debugger' });
        commands.addCommand(CommandIDs.showPanel, {
            label: trans.__('Debugger Panel'),
            execute: () => {
                shell.activateById(sidebar.id);
            }
        });
        if (palette) {
            const category = trans.__('Debugger');
            [
                CommandIDs.debugContinue,
                CommandIDs.terminate,
                CommandIDs.next,
                CommandIDs.stepIn,
                CommandIDs.stepOut,
                CommandIDs.evaluate,
                CommandIDs.pauseOnExceptions
            ].forEach(command => {
                palette.addItem({ command, category });
            });
        }
        if (debuggerSources) {
            const { model } = service;
            const readOnlyEditorFactory = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.ReadOnlyEditorFactory({
                editorServices
            });
            const onCurrentFrameChanged = (_, frame) => {
                var _a, _b, _c, _d, _e, _f, _g, _h, _j;
                debuggerSources
                    .find({
                    focus: true,
                    kernel: (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: (_j = (_h = frame === null || frame === void 0 ? void 0 : frame.source) === null || _h === void 0 ? void 0 : _h.path) !== null && _j !== void 0 ? _j : ''
                })
                    .forEach(editor => {
                    requestAnimationFrame(() => {
                        void editor.reveal().then(() => {
                            const edit = editor.get();
                            if (edit) {
                                _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler.showCurrentLine(edit, frame.line);
                            }
                        });
                    });
                });
            };
            const onSourceOpened = (_, source, breakpoint) => {
                var _a, _b, _c, _d, _e, _f, _g;
                if (!source) {
                    return;
                }
                const { content, mimeType, path } = source;
                const results = debuggerSources.find({
                    focus: true,
                    kernel: (_d = (_c = (_b = (_a = service.session) === null || _a === void 0 ? void 0 : _a.connection) === null || _b === void 0 ? void 0 : _b.kernel) === null || _c === void 0 ? void 0 : _c.name) !== null && _d !== void 0 ? _d : '',
                    path: (_g = (_f = (_e = service.session) === null || _e === void 0 ? void 0 : _e.connection) === null || _f === void 0 ? void 0 : _f.path) !== null && _g !== void 0 ? _g : '',
                    source: path
                });
                if (results.length > 0) {
                    if (breakpoint && typeof breakpoint.line !== 'undefined') {
                        results.forEach(editor => {
                            void editor.reveal().then(() => {
                                var _a;
                                (_a = editor.get()) === null || _a === void 0 ? void 0 : _a.revealPosition({
                                    line: breakpoint.line - 1,
                                    column: breakpoint.column || 0
                                });
                            });
                        });
                    }
                    return;
                }
                const editorWrapper = readOnlyEditorFactory.createNewEditor({
                    content,
                    mimeType,
                    path
                });
                const editor = editorWrapper.editor;
                const editorHandler = new _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler({
                    debuggerService: service,
                    editorReady: () => Promise.resolve(editor),
                    getEditor: () => editor,
                    path,
                    src: editor.model.sharedModel
                });
                editorWrapper.disposed.connect(() => editorHandler.dispose());
                debuggerSources.open({
                    label: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_5__.PathExt.basename(path),
                    caption: path,
                    editorWrapper
                });
                const frame = service.model.callstack.frame;
                if (frame) {
                    _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_6__.Debugger.EditorHandler.showCurrentLine(editor, frame.line);
                }
            };
            const onKernelSourceOpened = (_, source, breakpoint) => {
                if (!source) {
                    return;
                }
                onSourceOpened(null, source, breakpoint);
            };
            model.callstack.currentFrameChanged.connect(onCurrentFrameChanged);
            model.sources.currentSourceOpened.connect(onSourceOpened);
            model.kernelSources.kernelSourceOpened.connect(onKernelSourceOpened);
            model.breakpoints.clicked.connect(async (_, breakpoint) => {
                var _a;
                const path = (_a = breakpoint.source) === null || _a === void 0 ? void 0 : _a.path;
                const source = await service.getSource({
                    sourceReference: 0,
                    path
                });
                onSourceOpened(null, source, breakpoint);
            });
        }
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    service,
    consoles,
    files,
    notebooks,
    variables,
    sidebar,
    main,
    sources,
    configuration
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZGVidWdnZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy4yMThiOGExZTRmNjAzYWI3N2Y4ZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTzhCO0FBVUg7QUFDZTtBQUNZO0FBQ1c7QUFDUjtBQVE5QjtBQUMyQjtBQUNXO0FBQ1g7QUFLM0I7QUFLRTtBQUUrQjtBQUNPO0FBRXRFLFNBQVMsY0FBYyxDQUFDLEdBQW9CO0lBQzFDLE1BQU0sQ0FBQyxNQUFNLENBQUMscUVBQW1CLENBQUMsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLEVBQUU7UUFDbkQsSUFBSSxHQUFHLENBQUMsUUFBUSxDQUFDLFVBQVUsQ0FBQyxPQUFPLENBQUMsRUFBRTtZQUNwQyxHQUFHLENBQUMsUUFBUSxDQUFDLG9CQUFvQixDQUFDLE9BQU8sQ0FBQyxDQUFDO1NBQzVDO0lBQ0gsQ0FBQyxDQUFDLENBQUM7QUFDTCxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLFFBQVEsR0FBZ0M7SUFDNUMsd0RBQXdEO0lBQ3hELEVBQUUsRUFBRSx5Q0FBeUM7SUFDN0MsV0FBVyxFQUFFLDBDQUEwQztJQUN2RCxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLDJEQUFTLEVBQUUsZ0VBQWUsQ0FBQztJQUN0QyxRQUFRLEVBQUUsQ0FBQyw4REFBUyxDQUFDO0lBQ3JCLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLEtBQWdCLEVBQ2hCLGNBQStCLEVBQy9CLFFBQTBCLEVBQzFCLEVBQUU7UUFDRixNQUFNLE9BQU8sR0FBRyxJQUFJLGtFQUFnQixDQUFDO1lBQ25DLElBQUksRUFBRSxTQUFTO1lBQ2YsS0FBSyxFQUFFLEdBQUcsQ0FBQyxLQUFLO1lBQ2hCLE9BQU8sRUFBRSxLQUFLO1NBQ2YsQ0FBQyxDQUFDO1FBRUgsTUFBTSx3QkFBd0IsR0FBRyxL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LGtCQUFrQixDQUFDLE9BQU8sQ0FBQyxvQkFBb0IsQ0FBQyxDQUFDO1lBQ3JFLEtBQUssQ0FBQyxXQUFXLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxLQUFLLEVBQUUsQ0FBQyxFQUFFLFVBQVUsRUFBRSxFQUFFOztnQkFDeEQsTUFBTSxJQUFJLEdBQUcsZ0JBQVUsQ0FBQyxNQUFNLDBDQUFFLElBQUksQ0FBQztnQkFDckMsTUFBTSxNQUFNLEdBQUcsTUFBTSxPQUFPLENBQUMsU0FBUyxDQUFDO29CQUNyQyxlQUFlLEVBQUUsQ0FBQztvQkFDbEIsSUFBSTtpQkFDTCxDQUFDLENBQUM7Z0JBQ0gsY0FBYyxDQUFDLElBQUksRUFBRSxNQUFNLEVBQUUsVUFBVSxDQUFDLENBQUM7WUFDM0MsQ0FBQyxDQUFDLENBQUM7U0FDSjtJQUNILENBQUM7Q0FDRixDQUFDO0FBRUY7O0dBRUc7QUFDSCxNQUFNLE9BQU8sR0FBaUM7SUFDNUMsT0FBTztJQUNQLFFBQVE7SUFDUixLQUFLO0lBQ0wsU0FBUztJQUNULFNBQVM7SUFDVCxPQUFPO0lBQ1AsSUFBSTtJQUNKLE9BQU87SUFDUCxhQUFhO0NBQ2QsQ0FBQztBQUVGLGlFQUFlLE9BQU8sRUFBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9kZWJ1Z2dlci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGRlYnVnZ2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBDbGlwYm9hcmQsXG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSW5wdXREaWFsb2csXG4gIElTZXNzaW9uQ29udGV4dERpYWxvZ3MsXG4gIElUaGVtZU1hbmFnZXIsXG4gIE1haW5BcmVhV2lkZ2V0LFxuICBTZXNzaW9uQ29udGV4dERpYWxvZ3MsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgQ29kZUNlbGwgfSBmcm9tICdAanVweXRlcmxhYi9jZWxscyc7XG5pbXBvcnQgeyBJRWRpdG9yU2VydmljZXMgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IENvbnNvbGVQYW5lbCwgSUNvbnNvbGVUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29uc29sZSc7XG5pbXBvcnQgeyBQYWdlQ29uZmlnLCBQYXRoRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIERlYnVnZ2VyLFxuICBJRGVidWdnZXIsXG4gIElEZWJ1Z2dlckNvbmZpZyxcbiAgSURlYnVnZ2VySGFuZGxlcixcbiAgSURlYnVnZ2VyU2lkZWJhcixcbiAgSURlYnVnZ2VyU291cmNlc1xufSBmcm9tICdAanVweXRlcmxhYi9kZWJ1Z2dlcic7XG5pbXBvcnQgeyBEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IEZpbGVFZGl0b3IsIElFZGl0b3JUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZmlsZWVkaXRvcic7XG5pbXBvcnQgeyBJTG9nZ2VyUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9sb2djb25zb2xlJztcbmltcG9ydCB7XG4gIElOb3RlYm9va1RyYWNrZXIsXG4gIE5vdGVib29rQWN0aW9ucyxcbiAgTm90ZWJvb2tQYW5lbFxufSBmcm9tICdAanVweXRlcmxhYi9ub3RlYm9vayc7XG5pbXBvcnQge1xuICBzdGFuZGFyZFJlbmRlcmVyRmFjdG9yaWVzIGFzIGluaXRpYWxGYWN0b3JpZXMsXG4gIElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIFJlbmRlck1pbWVSZWdpc3RyeVxufSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IFNlc3Npb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxuZnVuY3Rpb24gbm90aWZ5Q29tbWFuZHMoYXBwOiBKdXB5dGVyRnJvbnRFbmQpOiB2b2lkIHtcbiAgT2JqZWN0LnZhbHVlcyhEZWJ1Z2dlci5Db21tYW5kSURzKS5mb3JFYWNoKGNvbW1hbmQgPT4ge1xuICAgIGlmIChhcHAuY29tbWFuZHMuaGFzQ29tbWFuZChjb21tYW5kKSkge1xuICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKGNvbW1hbmQpO1xuICAgIH1cbiAgfSk7XG59XG5cbi8qKlxuICogQSBwbHVnaW4gdGhhdCBwcm92aWRlcyB2aXN1YWwgZGVidWdnaW5nIHN1cHBvcnQgZm9yIGNvbnNvbGVzLlxuICovXG5jb25zdCBjb25zb2xlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICAvLyBGSVhNRSBUaGlzIHNob3VsZCBiZSBpbiBAanVweXRlcmxhYi9jb25zb2xlLWV4dGVuc2lvblxuICBpZDogJ0BqdXB5dGVybGFiL2RlYnVnZ2VyLWV4dGVuc2lvbjpjb25zb2xlcycsXG4gIGRlc2NyaXB0aW9uOiAnQWRkIGRlYnVnZ2VyIGNhcGFiaWxpdHkgdG8gdGhlIGNvbnNvbGVzLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJRGVidWdnZXIsIElDb25zb2xlVHJhY2tlcl0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkZWJ1ZzogSURlYnVnZ2VyLFxuICAgIGNvbnNvbGVUcmFja2VyOiBJQ29uc29sZVRyYWNrZXIsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgaGFuZGxlciA9IG5ldyBEZWJ1Z2dlci5IYW5kbGVyKHtcbiAgICAgIHR5cGU6ICdjb25zb2xlJyxcbiAgICAgIHNoZWxsOiBhcHAuc2hlbGwsXG4gICAgICBzZXJ2aWNlOiBkZWJ1Z1xuICAgIH0pO1xuXG4gICAgY29uc3QgdXBkYXRlSGFuZGxlckFuZENvbW1hbmRzID0gYXN5bmMgKFxuICAgICAgd2lkZ2V0OiBDb25zb2xlUGFuZWxcbiAgICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICAgIGNvbnN0IHsgc2Vzc2lvbkNvbnRleHQgfSA9IHdpZGdldDtcbiAgICAgIGF3YWl0IHNlc3Npb25Db250ZXh0LnJlYWR5O1xuICAgICAgYXdhaXQgaGFuZGxlci51cGRhdGVDb250ZXh0KHdpZGdldCwgc2Vzc2lvbkNvbnRleHQpO1xuICAgICAgbm90aWZ5Q29tbWFuZHMoYXBwKTtcbiAgICB9O1xuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KChfLCB1cGRhdGUpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdXBkYXRlLm5ld1ZhbHVlO1xuICAgICAgICBpZiAod2lkZ2V0IGluc3RhbmNlb2YgQ29uc29sZVBhbmVsKSB7XG4gICAgICAgICAgdm9pZCB1cGRhdGVIYW5kbGVyQW5kQ29tbWFuZHMod2lkZ2V0KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIGNvbnNvbGVUcmFja2VyLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoKF8sIGNvbnNvbGVQYW5lbCkgPT4ge1xuICAgICAgICBpZiAoY29uc29sZVBhbmVsKSB7XG4gICAgICAgICAgdm9pZCB1cGRhdGVIYW5kbGVyQW5kQ29tbWFuZHMoY29uc29sZVBhbmVsKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHRoYXQgcHJvdmlkZXMgdmlzdWFsIGRlYnVnZ2luZyBzdXBwb3J0IGZvciBmaWxlIGVkaXRvcnMuXG4gKi9cbmNvbnN0IGZpbGVzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIC8vIEZJWE1FIFRoaXMgc2hvdWxkIGJlIGluIEBqdXB5dGVybGFiL2ZpbGVlZGl0b3ItZXh0ZW5zaW9uXG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOmZpbGVzJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIGRlYnVnZ2VyIGNhcGFiaWxpdGllcyB0byBmaWxlcy4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSURlYnVnZ2VyLCBJRWRpdG9yVHJhY2tlcl0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkZWJ1ZzogSURlYnVnZ2VyLFxuICAgIGVkaXRvclRyYWNrZXI6IElFZGl0b3JUcmFja2VyLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsXG4gICkgPT4ge1xuICAgIGNvbnN0IGhhbmRsZXIgPSBuZXcgRGVidWdnZXIuSGFuZGxlcih7XG4gICAgICB0eXBlOiAnZmlsZScsXG4gICAgICBzaGVsbDogYXBwLnNoZWxsLFxuICAgICAgc2VydmljZTogZGVidWdcbiAgICB9KTtcblxuICAgIGNvbnN0IGFjdGl2ZVNlc3Npb25zOiB7XG4gICAgICBbaWQ6IHN0cmluZ106IFNlc3Npb24uSVNlc3Npb25Db25uZWN0aW9uO1xuICAgIH0gPSB7fTtcblxuICAgIGNvbnN0IHVwZGF0ZUhhbmRsZXJBbmRDb21tYW5kcyA9IGFzeW5jIChcbiAgICAgIHdpZGdldDogRG9jdW1lbnRXaWRnZXRcbiAgICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICAgIGNvbnN0IHNlc3Npb25zID0gYXBwLnNlcnZpY2VNYW5hZ2VyLnNlc3Npb25zO1xuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3QgbW9kZWwgPSBhd2FpdCBzZXNzaW9ucy5maW5kQnlQYXRoKHdpZGdldC5jb250ZXh0LnBhdGgpO1xuICAgICAgICBpZiAoIW1vZGVsKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGxldCBzZXNzaW9uID0gYWN0aXZlU2Vzc2lvbnNbbW9kZWwuaWRdO1xuICAgICAgICBpZiAoIXNlc3Npb24pIHtcbiAgICAgICAgICAvLyBVc2UgYGNvbm5lY3RUb2Agb25seSBpZiB0aGUgc2Vzc2lvbiBkb2VzIG5vdCBleGlzdC5cbiAgICAgICAgICAvLyBgY29ubmVjdFRvYCBzZW5kcyBhIGtlcm5lbF9pbmZvX3JlcXVlc3Qgb24gdGhlIHNoZWxsXG4gICAgICAgICAgLy8gY2hhbm5lbCwgd2hpY2ggYmxvY2tzIHRoZSBkZWJ1ZyBzZXNzaW9uIHJlc3RvcmUgd2hlbiB3YWl0aW5nXG4gICAgICAgICAgLy8gZm9yIHRoZSBrZXJuZWwgdG8gYmUgcmVhZHlcbiAgICAgICAgICBzZXNzaW9uID0gc2Vzc2lvbnMuY29ubmVjdFRvKHsgbW9kZWwgfSk7XG4gICAgICAgICAgYWN0aXZlU2Vzc2lvbnNbbW9kZWwuaWRdID0gc2Vzc2lvbjtcbiAgICAgICAgfVxuICAgICAgICBhd2FpdCBoYW5kbGVyLnVwZGF0ZSh3aWRnZXQsIHNlc3Npb24pO1xuICAgICAgICBub3RpZnlDb21tYW5kcyhhcHApO1xuICAgICAgfSBjYXRjaCB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICB9O1xuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KChfLCB1cGRhdGUpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdXBkYXRlLm5ld1ZhbHVlO1xuICAgICAgICBpZiAod2lkZ2V0IGluc3RhbmNlb2YgRG9jdW1lbnRXaWRnZXQpIHtcbiAgICAgICAgICBjb25zdCB7IGNvbnRlbnQgfSA9IHdpZGdldDtcbiAgICAgICAgICBpZiAoY29udGVudCBpbnN0YW5jZW9mIEZpbGVFZGl0b3IpIHtcbiAgICAgICAgICAgIHZvaWQgdXBkYXRlSGFuZGxlckFuZENvbW1hbmRzKHdpZGdldCk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9IGVsc2Uge1xuICAgICAgZWRpdG9yVHJhY2tlci5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KChfLCBkb2N1bWVudFdpZGdldCkgPT4ge1xuICAgICAgICBpZiAoZG9jdW1lbnRXaWRnZXQpIHtcbiAgICAgICAgICB2b2lkIHVwZGF0ZUhhbmRsZXJBbmRDb21tYW5kcyhcbiAgICAgICAgICAgIGRvY3VtZW50V2lkZ2V0IGFzIHVua25vd24gYXMgRG9jdW1lbnRXaWRnZXRcbiAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdGhhdCBwcm92aWRlcyB2aXN1YWwgZGVidWdnaW5nIHN1cHBvcnQgZm9yIG5vdGVib29rcy5cbiAqL1xuY29uc3Qgbm90ZWJvb2tzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SURlYnVnZ2VyLklIYW5kbGVyPiA9IHtcbiAgLy8gRklYTUUgVGhpcyBzaG91bGQgYmUgaW4gQGp1cHl0ZXJsYWIvbm90ZWJvb2stZXh0ZW5zaW9uXG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOm5vdGVib29rcycsXG4gIGRlc2NyaXB0aW9uOlxuICAgICdBZGRzIGRlYnVnZ2VyIGNhcGFiaWxpdHkgdG8gbm90ZWJvb2tzIGFuZCBwcm92aWRlcyB0aGUgZGVidWdnZXIgbm90ZWJvb2sgaGFuZGxlci4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSURlYnVnZ2VyLCBJTm90ZWJvb2tUcmFja2VyXSxcbiAgb3B0aW9uYWw6IFtJTGFiU2hlbGwsIElDb21tYW5kUGFsZXR0ZSwgSVNlc3Npb25Db250ZXh0RGlhbG9ncywgSVRyYW5zbGF0b3JdLFxuICBwcm92aWRlczogSURlYnVnZ2VySGFuZGxlcixcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzZXJ2aWNlOiBJRGVidWdnZXIsXG4gICAgbm90ZWJvb2tUcmFja2VyOiBJTm90ZWJvb2tUcmFja2VyLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGwsXG4gICAgc2Vzc2lvbkRpYWxvZ3NfOiBJU2Vzc2lvbkNvbnRleHREaWFsb2dzIHwgbnVsbCxcbiAgICB0cmFuc2xhdG9yXzogSVRyYW5zbGF0b3IgfCBudWxsXG4gICk6IERlYnVnZ2VyLkhhbmRsZXIgPT4ge1xuICAgIGNvbnN0IHRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yXyA/PyBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCBzZXNzaW9uRGlhbG9ncyA9XG4gICAgICBzZXNzaW9uRGlhbG9nc18gPz8gbmV3IFNlc3Npb25Db250ZXh0RGlhbG9ncyh7IHRyYW5zbGF0b3IgfSk7XG4gICAgY29uc3QgaGFuZGxlciA9IG5ldyBEZWJ1Z2dlci5IYW5kbGVyKHtcbiAgICAgIHR5cGU6ICdub3RlYm9vaycsXG4gICAgICBzaGVsbDogYXBwLnNoZWxsLFxuICAgICAgc2VydmljZVxuICAgIH0pO1xuXG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChEZWJ1Z2dlci5Db21tYW5kSURzLnJlc3RhcnREZWJ1Zywge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdSZXN0YXJ0IEtlcm5lbCBhbmQgRGVidWfigKYnKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdSZXN0YXJ0IEtlcm5lbCBhbmQgRGVidWfigKYnKSxcbiAgICAgIGlzRW5hYmxlZDogKCkgPT4gc2VydmljZS5pc1N0YXJ0ZWQsXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHN0YXRlID0gc2VydmljZS5nZXREZWJ1Z2dlclN0YXRlKCk7XG4gICAgICAgIGF3YWl0IHNlcnZpY2Uuc3RvcCgpO1xuXG4gICAgICAgIGNvbnN0IHdpZGdldCA9IG5vdGVib29rVHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IHsgY29udGVudCwgc2Vzc2lvbkNvbnRleHQgfSA9IHdpZGdldDtcbiAgICAgICAgY29uc3QgcmVzdGFydGVkID0gYXdhaXQgc2Vzc2lvbkRpYWxvZ3MucmVzdGFydChzZXNzaW9uQ29udGV4dCk7XG4gICAgICAgIGlmICghcmVzdGFydGVkKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgYXdhaXQgc2VydmljZS5yZXN0b3JlRGVidWdnZXJTdGF0ZShzdGF0ZSk7XG4gICAgICAgIGF3YWl0IGhhbmRsZXIudXBkYXRlV2lkZ2V0KHdpZGdldCwgc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbik7XG4gICAgICAgIGF3YWl0IE5vdGVib29rQWN0aW9ucy5ydW5BbGwoXG4gICAgICAgICAgY29udGVudCxcbiAgICAgICAgICBzZXNzaW9uQ29udGV4dCxcbiAgICAgICAgICBzZXNzaW9uRGlhbG9ncyxcbiAgICAgICAgICB0cmFuc2xhdG9yXG4gICAgICAgICk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBjb25zdCB1cGRhdGVIYW5kbGVyQW5kQ29tbWFuZHMgPSBhc3luYyAoXG4gICAgICB3aWRnZXQ6IE5vdGVib29rUGFuZWxcbiAgICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgY29uc3QgeyBzZXNzaW9uQ29udGV4dCB9ID0gd2lkZ2V0O1xuICAgICAgICBhd2FpdCBzZXNzaW9uQ29udGV4dC5yZWFkeTtcbiAgICAgICAgYXdhaXQgaGFuZGxlci51cGRhdGVDb250ZXh0KHdpZGdldCwgc2Vzc2lvbkNvbnRleHQpO1xuICAgICAgfVxuICAgICAgbm90aWZ5Q29tbWFuZHMoYXBwKTtcbiAgICB9O1xuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KChfLCB1cGRhdGUpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdXBkYXRlLm5ld1ZhbHVlO1xuICAgICAgICBpZiAod2lkZ2V0IGluc3RhbmNlb2YgTm90ZWJvb2tQYW5lbCkge1xuICAgICAgICAgIHZvaWQgdXBkYXRlSGFuZGxlckFuZENvbW1hbmRzKHdpZGdldCk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH0gZWxzZSB7XG4gICAgICBub3RlYm9va1RyYWNrZXIuY3VycmVudENoYW5nZWQuY29ubmVjdCgoXywgbm90ZWJvb2tQYW5lbCkgPT4ge1xuICAgICAgICBpZiAobm90ZWJvb2tQYW5lbCkge1xuICAgICAgICAgIHZvaWQgdXBkYXRlSGFuZGxlckFuZENvbW1hbmRzKG5vdGVib29rUGFuZWwpO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgY2F0ZWdvcnk6ICdOb3RlYm9vayBPcGVyYXRpb25zJyxcbiAgICAgICAgY29tbWFuZDogRGVidWdnZXIuQ29tbWFuZElEcy5yZXN0YXJ0RGVidWdcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIHJldHVybiBoYW5kbGVyO1xuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHRoYXQgcHJvdmlkZXMgYSBkZWJ1Z2dlciBzZXJ2aWNlLlxuICovXG5jb25zdCBzZXJ2aWNlOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SURlYnVnZ2VyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kZWJ1Z2dlci1leHRlbnNpb246c2VydmljZScsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGRlYnVnZ2VyIHNlcnZpY2UuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSURlYnVnZ2VyLFxuICByZXF1aXJlczogW0lEZWJ1Z2dlckNvbmZpZ10sXG4gIG9wdGlvbmFsOiBbSURlYnVnZ2VyU291cmNlcywgSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGNvbmZpZzogSURlYnVnZ2VyLklDb25maWcsXG4gICAgZGVidWdnZXJTb3VyY2VzOiBJRGVidWdnZXIuSVNvdXJjZXMgfCBudWxsLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbFxuICApID0+XG4gICAgbmV3IERlYnVnZ2VyLlNlcnZpY2Uoe1xuICAgICAgY29uZmlnLFxuICAgICAgZGVidWdnZXJTb3VyY2VzLFxuICAgICAgc3BlY3NNYW5hZ2VyOiBhcHAuc2VydmljZU1hbmFnZXIua2VybmVsc3BlY3MsXG4gICAgICB0cmFuc2xhdG9yXG4gICAgfSlcbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdGhhdCBwcm92aWRlcyBhIGNvbmZpZ3VyYXRpb24gd2l0aCBoYXNoIG1ldGhvZC5cbiAqL1xuY29uc3QgY29uZmlndXJhdGlvbjogSnVweXRlckZyb250RW5kUGx1Z2luPElEZWJ1Z2dlci5JQ29uZmlnPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kZWJ1Z2dlci1leHRlbnNpb246Y29uZmlnJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgZGVidWdnZXIgY29uZmlndXJhdGlvbicsXG4gIHByb3ZpZGVzOiBJRGVidWdnZXJDb25maWcsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6ICgpID0+IG5ldyBEZWJ1Z2dlci5Db25maWcoKVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0aGF0IHByb3ZpZGVzIHNvdXJjZS9lZGl0b3IgZnVuY3Rpb25hbGl0eSBmb3IgZGVidWdnaW5nLlxuICovXG5jb25zdCBzb3VyY2VzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SURlYnVnZ2VyLklTb3VyY2VzPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kZWJ1Z2dlci1leHRlbnNpb246c291cmNlcycsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIHNvdXJjZSBmZWF0dXJlIGZvciBkZWJ1Z2dpbmcnLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJRGVidWdnZXJTb3VyY2VzLFxuICByZXF1aXJlczogW0lEZWJ1Z2dlckNvbmZpZywgSUVkaXRvclNlcnZpY2VzXSxcbiAgb3B0aW9uYWw6IFtJTm90ZWJvb2tUcmFja2VyLCBJQ29uc29sZVRyYWNrZXIsIElFZGl0b3JUcmFja2VyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBjb25maWc6IElEZWJ1Z2dlci5JQ29uZmlnLFxuICAgIGVkaXRvclNlcnZpY2VzOiBJRWRpdG9yU2VydmljZXMsXG4gICAgbm90ZWJvb2tUcmFja2VyOiBJTm90ZWJvb2tUcmFja2VyIHwgbnVsbCxcbiAgICBjb25zb2xlVHJhY2tlcjogSUNvbnNvbGVUcmFja2VyIHwgbnVsbCxcbiAgICBlZGl0b3JUcmFja2VyOiBJRWRpdG9yVHJhY2tlciB8IG51bGxcbiAgKTogSURlYnVnZ2VyLklTb3VyY2VzID0+IHtcbiAgICByZXR1cm4gbmV3IERlYnVnZ2VyLlNvdXJjZXMoe1xuICAgICAgY29uZmlnLFxuICAgICAgc2hlbGw6IGFwcC5zaGVsbCxcbiAgICAgIGVkaXRvclNlcnZpY2VzLFxuICAgICAgbm90ZWJvb2tUcmFja2VyLFxuICAgICAgY29uc29sZVRyYWNrZXIsXG4gICAgICBlZGl0b3JUcmFja2VyXG4gICAgfSk7XG4gIH1cbn07XG4vKlxuICogQSBwbHVnaW4gdG8gb3BlbiBkZXRhaWxlZCB2aWV3cyBmb3IgdmFyaWFibGVzLlxuICovXG5jb25zdCB2YXJpYWJsZXM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kZWJ1Z2dlci1leHRlbnNpb246dmFyaWFibGVzJyxcbiAgZGVzY3JpcHRpb246XG4gICAgJ0FkZHMgdmFyaWFibGVzIHJlbmRlcmVyIGFuZCBpbnNwZWN0aW9uIGluIHRoZSBkZWJ1Z2dlciB2YXJpYWJsZSBwYW5lbC4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSURlYnVnZ2VyLCBJRGVidWdnZXJIYW5kbGVyLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSVRoZW1lTWFuYWdlciwgSVJlbmRlck1pbWVSZWdpc3RyeV0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgc2VydmljZTogSURlYnVnZ2VyLFxuICAgIGhhbmRsZXI6IERlYnVnZ2VyLkhhbmRsZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgdGhlbWVNYW5hZ2VyOiBJVGhlbWVNYW5hZ2VyIHwgbnVsbCxcbiAgICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5IHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsIH0gPSBhcHA7XG4gICAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PERlYnVnZ2VyLlZhcmlhYmxlc0dyaWQ+Pih7XG4gICAgICBuYW1lc3BhY2U6ICdkZWJ1Z2dlci9pbnNwZWN0LXZhcmlhYmxlJ1xuICAgIH0pO1xuICAgIGNvbnN0IHRyYWNrZXJNaW1lID0gbmV3IFdpZGdldFRyYWNrZXI8RGVidWdnZXIuVmFyaWFibGVSZW5kZXJlcj4oe1xuICAgICAgbmFtZXNwYWNlOiAnZGVidWdnZXIvcmVuZGVyLXZhcmlhYmxlJ1xuICAgIH0pO1xuICAgIGNvbnN0IENvbW1hbmRJRHMgPSBEZWJ1Z2dlci5Db21tYW5kSURzO1xuXG4gICAgLy8gQWRkIGNvbW1hbmRzXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmluc3BlY3RWYXJpYWJsZSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdJbnNwZWN0IFZhcmlhYmxlJyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnSW5zcGVjdCBWYXJpYWJsZScpLFxuICAgICAgaXNFbmFibGVkOiBhcmdzID0+XG4gICAgICAgICEhc2VydmljZS5zZXNzaW9uPy5pc1N0YXJ0ZWQgJiZcbiAgICAgICAgTnVtYmVyKFxuICAgICAgICAgIGFyZ3MudmFyaWFibGVSZWZlcmVuY2UgPz9cbiAgICAgICAgICAgIHNlcnZpY2UubW9kZWwudmFyaWFibGVzLnNlbGVjdGVkVmFyaWFibGU/LnZhcmlhYmxlc1JlZmVyZW5jZSA/P1xuICAgICAgICAgICAgMFxuICAgICAgICApID4gMCxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jIGFyZ3MgPT4ge1xuICAgICAgICBsZXQgeyB2YXJpYWJsZVJlZmVyZW5jZSwgbmFtZSB9ID0gYXJncyBhcyB7XG4gICAgICAgICAgdmFyaWFibGVSZWZlcmVuY2U/OiBudW1iZXI7XG4gICAgICAgICAgbmFtZT86IHN0cmluZztcbiAgICAgICAgfTtcblxuICAgICAgICBpZiAoIXZhcmlhYmxlUmVmZXJlbmNlKSB7XG4gICAgICAgICAgdmFyaWFibGVSZWZlcmVuY2UgPVxuICAgICAgICAgICAgc2VydmljZS5tb2RlbC52YXJpYWJsZXMuc2VsZWN0ZWRWYXJpYWJsZT8udmFyaWFibGVzUmVmZXJlbmNlO1xuICAgICAgICB9XG4gICAgICAgIGlmICghbmFtZSkge1xuICAgICAgICAgIG5hbWUgPSBzZXJ2aWNlLm1vZGVsLnZhcmlhYmxlcy5zZWxlY3RlZFZhcmlhYmxlPy5uYW1lO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgaWQgPSBganAtZGVidWdnZXItdmFyaWFibGUtJHtuYW1lfWA7XG4gICAgICAgIGlmIChcbiAgICAgICAgICAhbmFtZSB8fFxuICAgICAgICAgICF2YXJpYWJsZVJlZmVyZW5jZSB8fFxuICAgICAgICAgIHRyYWNrZXIuZmluZCh3aWRnZXQgPT4gd2lkZ2V0LmlkID09PSBpZClcbiAgICAgICAgKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgdmFyaWFibGVzID0gYXdhaXQgc2VydmljZS5pbnNwZWN0VmFyaWFibGUoXG4gICAgICAgICAgdmFyaWFibGVSZWZlcmVuY2UgYXMgbnVtYmVyXG4gICAgICAgICk7XG4gICAgICAgIGlmICghdmFyaWFibGVzIHx8IHZhcmlhYmxlcy5sZW5ndGggPT09IDApIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBtb2RlbCA9IHNlcnZpY2UubW9kZWwudmFyaWFibGVzO1xuICAgICAgICBjb25zdCB3aWRnZXQgPSBuZXcgTWFpbkFyZWFXaWRnZXQ8RGVidWdnZXIuVmFyaWFibGVzR3JpZD4oe1xuICAgICAgICAgIGNvbnRlbnQ6IG5ldyBEZWJ1Z2dlci5WYXJpYWJsZXNHcmlkKHtcbiAgICAgICAgICAgIG1vZGVsLFxuICAgICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgICBzY29wZXM6IFt7IG5hbWUsIHZhcmlhYmxlcyB9XSxcbiAgICAgICAgICAgIHRoZW1lTWFuYWdlclxuICAgICAgICAgIH0pXG4gICAgICAgIH0pO1xuICAgICAgICB3aWRnZXQuYWRkQ2xhc3MoJ2pwLURlYnVnZ2VyVmFyaWFibGVzJyk7XG4gICAgICAgIHdpZGdldC5pZCA9IGlkO1xuICAgICAgICB3aWRnZXQudGl0bGUuaWNvbiA9IERlYnVnZ2VyLkljb25zLnZhcmlhYmxlSWNvbjtcbiAgICAgICAgd2lkZ2V0LnRpdGxlLmxhYmVsID0gYCR7c2VydmljZS5zZXNzaW9uPy5jb25uZWN0aW9uPy5uYW1lfSAtICR7bmFtZX1gO1xuICAgICAgICB2b2lkIHRyYWNrZXIuYWRkKHdpZGdldCk7XG4gICAgICAgIGNvbnN0IGRpc3Bvc2VXaWRnZXQgPSAoKSA9PiB7XG4gICAgICAgICAgd2lkZ2V0LmRpc3Bvc2UoKTtcbiAgICAgICAgICBtb2RlbC5jaGFuZ2VkLmRpc2Nvbm5lY3QoZGlzcG9zZVdpZGdldCk7XG4gICAgICAgIH07XG4gICAgICAgIG1vZGVsLmNoYW5nZWQuY29ubmVjdChkaXNwb3NlV2lkZ2V0KTtcbiAgICAgICAgc2hlbGwuYWRkKHdpZGdldCwgJ21haW4nLCB7XG4gICAgICAgICAgbW9kZTogdHJhY2tlci5jdXJyZW50V2lkZ2V0ID8gJ3NwbGl0LXJpZ2h0JyA6ICdzcGxpdC1ib3R0b20nLFxuICAgICAgICAgIGFjdGl2YXRlOiBmYWxzZSxcbiAgICAgICAgICB0eXBlOiAnRGVidWdnZXIgVmFyaWFibGVzJ1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZW5kZXJNaW1lVmFyaWFibGUsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnUmVuZGVyIFZhcmlhYmxlJyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnUmVuZGVyIHZhcmlhYmxlIGFjY29yZGluZyB0byBpdHMgbWltZSB0eXBlJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+ICEhc2VydmljZS5zZXNzaW9uPy5pc1N0YXJ0ZWQsXG4gICAgICBpc1Zpc2libGU6ICgpID0+XG4gICAgICAgIHNlcnZpY2UubW9kZWwuaGFzUmljaFZhcmlhYmxlUmVuZGVyaW5nICYmXG4gICAgICAgIChyZW5kZXJtaW1lICE9PSBudWxsIHx8IGhhbmRsZXIuYWN0aXZlV2lkZ2V0IGluc3RhbmNlb2YgTm90ZWJvb2tQYW5lbCksXG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgbGV0IHsgbmFtZSwgZnJhbWVJZCB9ID0gYXJncyBhcyB7XG4gICAgICAgICAgZnJhbWVJZD86IG51bWJlcjtcbiAgICAgICAgICBuYW1lPzogc3RyaW5nO1xuICAgICAgICB9O1xuXG4gICAgICAgIGlmICghbmFtZSkge1xuICAgICAgICAgIG5hbWUgPSBzZXJ2aWNlLm1vZGVsLnZhcmlhYmxlcy5zZWxlY3RlZFZhcmlhYmxlPy5uYW1lO1xuICAgICAgICB9XG4gICAgICAgIGlmICghZnJhbWVJZCkge1xuICAgICAgICAgIGZyYW1lSWQgPSBzZXJ2aWNlLm1vZGVsLmNhbGxzdGFjay5mcmFtZT8uaWQ7XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBhY3RpdmVXaWRnZXQgPSBoYW5kbGVyLmFjdGl2ZVdpZGdldDtcbiAgICAgICAgbGV0IGFjdGl2ZVJlbmRlcm1pbWUgPVxuICAgICAgICAgIGFjdGl2ZVdpZGdldCBpbnN0YW5jZW9mIE5vdGVib29rUGFuZWxcbiAgICAgICAgICAgID8gYWN0aXZlV2lkZ2V0LmNvbnRlbnQucmVuZGVybWltZVxuICAgICAgICAgICAgOiByZW5kZXJtaW1lO1xuXG4gICAgICAgIGlmICghYWN0aXZlUmVuZGVybWltZSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGlkID0gYGpwLWRlYnVnZ2VyLXZhcmlhYmxlLW1pbWUtJHtuYW1lfS0ke3NlcnZpY2Uuc2Vzc2lvbj8uY29ubmVjdGlvbj8ucGF0aC5yZXBsYWNlKFxuICAgICAgICAgICcvJyxcbiAgICAgICAgICAnLSdcbiAgICAgICAgKX1gO1xuICAgICAgICBpZiAoXG4gICAgICAgICAgIW5hbWUgfHwgLy8gTmFtZSBpcyBtYW5kYXRvcnlcbiAgICAgICAgICB0cmFja2VyTWltZS5maW5kKHdpZGdldCA9PiB3aWRnZXQuaWQgPT09IGlkKSB8fCAvLyBXaWRnZXQgYWxyZWFkeSBleGlzdHNcbiAgICAgICAgICAoIWZyYW1lSWQgJiYgc2VydmljZS5oYXNTdG9wcGVkVGhyZWFkcygpKSAvLyBmcmFtZSBpZCBtaXNzaW5nIG9uIGJyZWFrcG9pbnRcbiAgICAgICAgKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgdmFyaWFibGVzTW9kZWwgPSBzZXJ2aWNlLm1vZGVsLnZhcmlhYmxlcztcblxuICAgICAgICBjb25zdCB3aWRnZXQgPSBuZXcgRGVidWdnZXIuVmFyaWFibGVSZW5kZXJlcih7XG4gICAgICAgICAgZGF0YUxvYWRlcjogKCkgPT4gc2VydmljZS5pbnNwZWN0UmljaFZhcmlhYmxlKG5hbWUhLCBmcmFtZUlkKSxcbiAgICAgICAgICByZW5kZXJtaW1lOiBhY3RpdmVSZW5kZXJtaW1lLFxuICAgICAgICAgIHRyYW5zbGF0b3JcbiAgICAgICAgfSk7XG4gICAgICAgIHdpZGdldC5hZGRDbGFzcygnanAtRGVidWdnZXJSaWNoVmFyaWFibGUnKTtcbiAgICAgICAgd2lkZ2V0LmlkID0gaWQ7XG4gICAgICAgIHdpZGdldC50aXRsZS5pY29uID0gRGVidWdnZXIuSWNvbnMudmFyaWFibGVJY29uO1xuICAgICAgICB3aWRnZXQudGl0bGUubGFiZWwgPSBgJHtuYW1lfSAtICR7c2VydmljZS5zZXNzaW9uPy5jb25uZWN0aW9uPy5uYW1lfWA7XG4gICAgICAgIHdpZGdldC50aXRsZS5jYXB0aW9uID0gYCR7bmFtZX0gLSAke3NlcnZpY2Uuc2Vzc2lvbj8uY29ubmVjdGlvbj8ucGF0aH1gO1xuICAgICAgICB2b2lkIHRyYWNrZXJNaW1lLmFkZCh3aWRnZXQpO1xuICAgICAgICBjb25zdCBkaXNwb3NlV2lkZ2V0ID0gKCkgPT4ge1xuICAgICAgICAgIHdpZGdldC5kaXNwb3NlKCk7XG4gICAgICAgICAgdmFyaWFibGVzTW9kZWwuY2hhbmdlZC5kaXNjb25uZWN0KHJlZnJlc2hXaWRnZXQpO1xuICAgICAgICAgIGFjdGl2ZVdpZGdldD8uZGlzcG9zZWQuZGlzY29ubmVjdChkaXNwb3NlV2lkZ2V0KTtcbiAgICAgICAgfTtcbiAgICAgICAgY29uc3QgcmVmcmVzaFdpZGdldCA9ICgpID0+IHtcbiAgICAgICAgICAvLyBSZWZyZXNoIHRoZSB3aWRnZXQgb25seSBpZiB0aGUgYWN0aXZlIGVsZW1lbnQgaXMgdGhlIHNhbWUuXG4gICAgICAgICAgaWYgKGhhbmRsZXIuYWN0aXZlV2lkZ2V0ID09PSBhY3RpdmVXaWRnZXQpIHtcbiAgICAgICAgICAgIHZvaWQgd2lkZ2V0LnJlZnJlc2goKTtcbiAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIHdpZGdldC5kaXNwb3NlZC5jb25uZWN0KGRpc3Bvc2VXaWRnZXQpO1xuICAgICAgICB2YXJpYWJsZXNNb2RlbC5jaGFuZ2VkLmNvbm5lY3QocmVmcmVzaFdpZGdldCk7XG4gICAgICAgIGFjdGl2ZVdpZGdldD8uZGlzcG9zZWQuY29ubmVjdChkaXNwb3NlV2lkZ2V0KTtcblxuICAgICAgICBzaGVsbC5hZGQod2lkZ2V0LCAnbWFpbicsIHtcbiAgICAgICAgICBtb2RlOiB0cmFja2VyTWltZS5jdXJyZW50V2lkZ2V0ID8gJ3NwbGl0LXJpZ2h0JyA6ICdzcGxpdC1ib3R0b20nLFxuICAgICAgICAgIGFjdGl2YXRlOiBmYWxzZSxcbiAgICAgICAgICB0eXBlOiAnRGVidWdnZXIgVmFyaWFibGVzJ1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5VG9DbGlwYm9hcmQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnQ29weSB0byBDbGlwYm9hcmQnKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdDb3B5IHRleHQgcmVwcmVzZW50YXRpb24gb2YgdGhlIHZhbHVlIHRvIGNsaXBib2FyZCcpLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiB7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgISFzZXJ2aWNlLnNlc3Npb24/LmlzU3RhcnRlZCAmJlxuICAgICAgICAgICEhc2VydmljZS5tb2RlbC52YXJpYWJsZXMuc2VsZWN0ZWRWYXJpYWJsZT8udmFsdWVcbiAgICAgICAgKTtcbiAgICAgIH0sXG4gICAgICBpc1Zpc2libGU6ICgpID0+IGhhbmRsZXIuYWN0aXZlV2lkZ2V0IGluc3RhbmNlb2YgTm90ZWJvb2tQYW5lbCxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgY29uc3QgdmFsdWUgPSBzZXJ2aWNlLm1vZGVsLnZhcmlhYmxlcy5zZWxlY3RlZFZhcmlhYmxlIS52YWx1ZTtcbiAgICAgICAgaWYgKHZhbHVlKSB7XG4gICAgICAgICAgQ2xpcGJvYXJkLmNvcHlUb1N5c3RlbSh2YWx1ZSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5VG9HbG9iYWxzLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0NvcHkgVmFyaWFibGUgdG8gR2xvYmFscycpLFxuICAgICAgY2FwdGlvbjogdHJhbnMuX18oJ0NvcHkgdmFyaWFibGUgdG8gZ2xvYmFscyBzY29wZScpLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiAhIXNlcnZpY2Uuc2Vzc2lvbj8uaXNTdGFydGVkLFxuICAgICAgaXNWaXNpYmxlOiAoKSA9PlxuICAgICAgICBoYW5kbGVyLmFjdGl2ZVdpZGdldCBpbnN0YW5jZW9mIE5vdGVib29rUGFuZWwgJiZcbiAgICAgICAgc2VydmljZS5tb2RlbC5zdXBwb3J0Q29weVRvR2xvYmFscyxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jIGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCBuYW1lID0gc2VydmljZS5tb2RlbC52YXJpYWJsZXMuc2VsZWN0ZWRWYXJpYWJsZSEubmFtZTtcbiAgICAgICAgYXdhaXQgc2VydmljZS5jb3B5VG9HbG9iYWxzKG5hbWUpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIERlYnVnZ2VyIHNpZGViYXIgcHJvdmlkZXIgcGx1Z2luLlxuICovXG5jb25zdCBzaWRlYmFyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SURlYnVnZ2VyLklTaWRlYmFyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kZWJ1Z2dlci1leHRlbnNpb246c2lkZWJhcicsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGRlYnVnZ2VyIHNpZGViYXIuJyxcbiAgcHJvdmlkZXM6IElEZWJ1Z2dlclNpZGViYXIsXG4gIHJlcXVpcmVzOiBbSURlYnVnZ2VyLCBJRWRpdG9yU2VydmljZXMsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJVGhlbWVNYW5hZ2VyLCBJU2V0dGluZ1JlZ2lzdHJ5XSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHNlcnZpY2U6IElEZWJ1Z2dlcixcbiAgICBlZGl0b3JTZXJ2aWNlczogSUVkaXRvclNlcnZpY2VzLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHRoZW1lTWFuYWdlcjogSVRoZW1lTWFuYWdlciB8IG51bGwsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbFxuICApOiBQcm9taXNlPElEZWJ1Z2dlci5JU2lkZWJhcj4gPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCBDb21tYW5kSURzID0gRGVidWdnZXIuQ29tbWFuZElEcztcblxuICAgIGNvbnN0IGNhbGxzdGFja0NvbW1hbmRzID0ge1xuICAgICAgcmVnaXN0cnk6IGNvbW1hbmRzLFxuICAgICAgY29udGludWU6IENvbW1hbmRJRHMuZGVidWdDb250aW51ZSxcbiAgICAgIHRlcm1pbmF0ZTogQ29tbWFuZElEcy50ZXJtaW5hdGUsXG4gICAgICBuZXh0OiBDb21tYW5kSURzLm5leHQsXG4gICAgICBzdGVwSW46IENvbW1hbmRJRHMuc3RlcEluLFxuICAgICAgc3RlcE91dDogQ29tbWFuZElEcy5zdGVwT3V0LFxuICAgICAgZXZhbHVhdGU6IENvbW1hbmRJRHMuZXZhbHVhdGVcbiAgICB9O1xuXG4gICAgY29uc3QgYnJlYWtwb2ludHNDb21tYW5kcyA9IHtcbiAgICAgIHJlZ2lzdHJ5OiBjb21tYW5kcyxcbiAgICAgIHBhdXNlT25FeGNlcHRpb25zOiBDb21tYW5kSURzLnBhdXNlT25FeGNlcHRpb25zXG4gICAgfTtcblxuICAgIGNvbnN0IHNpZGViYXIgPSBuZXcgRGVidWdnZXIuU2lkZWJhcih7XG4gICAgICBzZXJ2aWNlLFxuICAgICAgY2FsbHN0YWNrQ29tbWFuZHMsXG4gICAgICBicmVha3BvaW50c0NvbW1hbmRzLFxuICAgICAgZWRpdG9yU2VydmljZXMsXG4gICAgICB0aGVtZU1hbmFnZXIsXG4gICAgICB0cmFuc2xhdG9yXG4gICAgfSk7XG5cbiAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICBjb25zdCBzZXR0aW5nID0gYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LmxvYWQobWFpbi5pZCk7XG4gICAgICBjb25zdCB1cGRhdGVTZXR0aW5ncyA9ICgpOiB2b2lkID0+IHtcbiAgICAgICAgY29uc3QgZmlsdGVycyA9IHNldHRpbmcuZ2V0KCd2YXJpYWJsZUZpbHRlcnMnKS5jb21wb3NpdGUgYXMge1xuICAgICAgICAgIFtrZXk6IHN0cmluZ106IHN0cmluZ1tdO1xuICAgICAgICB9O1xuICAgICAgICBjb25zdCBrZXJuZWwgPSBzZXJ2aWNlLnNlc3Npb24/LmNvbm5lY3Rpb24/Lmtlcm5lbD8ubmFtZSA/PyAnJztcbiAgICAgICAgaWYgKGtlcm5lbCAmJiBmaWx0ZXJzW2tlcm5lbF0pIHtcbiAgICAgICAgICBzaWRlYmFyLnZhcmlhYmxlcy5maWx0ZXIgPSBuZXcgU2V0PHN0cmluZz4oZmlsdGVyc1trZXJuZWxdKTtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBrZXJuZWxTb3VyY2VzRmlsdGVyID0gc2V0dGluZy5nZXQoJ2RlZmF1bHRLZXJuZWxTb3VyY2VzRmlsdGVyJylcbiAgICAgICAgICAuY29tcG9zaXRlIGFzIHN0cmluZztcbiAgICAgICAgc2lkZWJhci5rZXJuZWxTb3VyY2VzLmZpbHRlciA9IGtlcm5lbFNvdXJjZXNGaWx0ZXI7XG4gICAgICB9O1xuICAgICAgdXBkYXRlU2V0dGluZ3MoKTtcbiAgICAgIHNldHRpbmcuY2hhbmdlZC5jb25uZWN0KHVwZGF0ZVNldHRpbmdzKTtcbiAgICAgIHNlcnZpY2Uuc2Vzc2lvbkNoYW5nZWQuY29ubmVjdCh1cGRhdGVTZXR0aW5ncyk7XG4gICAgfVxuXG4gICAgcmV0dXJuIHNpZGViYXI7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIG1haW4gZGVidWdnZXIgVUkgcGx1Z2luLlxuICovXG5jb25zdCBtYWluOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZGVidWdnZXItZXh0ZW5zaW9uOm1haW4nLFxuICBkZXNjcmlwdGlvbjogJ0luaXRpYWxpemUgdGhlIGRlYnVnZ2VyIHVzZXIgaW50ZXJmYWNlLicsXG4gIHJlcXVpcmVzOiBbSURlYnVnZ2VyLCBJRGVidWdnZXJTaWRlYmFyLCBJRWRpdG9yU2VydmljZXMsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtcbiAgICBJQ29tbWFuZFBhbGV0dGUsXG4gICAgSURlYnVnZ2VyU291cmNlcyxcbiAgICBJTGFiU2hlbGwsXG4gICAgSUxheW91dFJlc3RvcmVyLFxuICAgIElMb2dnZXJSZWdpc3RyeSxcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5XG4gIF0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IGFzeW5jIChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzZXJ2aWNlOiBJRGVidWdnZXIsXG4gICAgc2lkZWJhcjogSURlYnVnZ2VyLklTaWRlYmFyLFxuICAgIGVkaXRvclNlcnZpY2VzOiBJRWRpdG9yU2VydmljZXMsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgICBkZWJ1Z2dlclNvdXJjZXM6IElEZWJ1Z2dlci5JU291cmNlcyB8IG51bGwsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGwsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gICAgbG9nZ2VyUmVnaXN0cnk6IElMb2dnZXJSZWdpc3RyeSB8IG51bGwsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbFxuICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsLCBzZXJ2aWNlTWFuYWdlciB9ID0gYXBwO1xuICAgIGNvbnN0IHsga2VybmVsc3BlY3MgfSA9IHNlcnZpY2VNYW5hZ2VyO1xuICAgIGNvbnN0IENvbW1hbmRJRHMgPSBEZWJ1Z2dlci5Db21tYW5kSURzO1xuXG4gICAgLy8gRmlyc3QgY2hlY2sgaWYgdGhlcmUgaXMgYSBQYWdlQ29uZmlnIG92ZXJyaWRlIGZvciB0aGUgZXh0ZW5zaW9uIHZpc2liaWxpdHlcbiAgICBjb25zdCBhbHdheXNTaG93RGVidWdnZXJFeHRlbnNpb24gPVxuICAgICAgUGFnZUNvbmZpZy5nZXRPcHRpb24oJ2Fsd2F5c1Nob3dEZWJ1Z2dlckV4dGVuc2lvbicpLnRvTG93ZXJDYXNlKCkgPT09XG4gICAgICAndHJ1ZSc7XG4gICAgaWYgKCFhbHdheXNTaG93RGVidWdnZXJFeHRlbnNpb24pIHtcbiAgICAgIC8vIGhpZGUgdGhlIGRlYnVnZ2VyIHNpZGViYXIgaWYgbm8ga2VybmVsIHdpdGggc3VwcG9ydCBmb3IgZGVidWdnaW5nIGlzIGF2YWlsYWJsZVxuICAgICAgYXdhaXQga2VybmVsc3BlY3MucmVhZHk7XG4gICAgICBjb25zdCBzcGVjcyA9IGtlcm5lbHNwZWNzLnNwZWNzPy5rZXJuZWxzcGVjcztcbiAgICAgIGlmICghc3BlY3MpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgZW5hYmxlZCA9IE9iamVjdC5rZXlzKHNwZWNzKS5zb21lKFxuICAgICAgICBuYW1lID0+ICEhKHNwZWNzW25hbWVdPy5tZXRhZGF0YT8uWydkZWJ1Z2dlciddID8/IGZhbHNlKVxuICAgICAgKTtcbiAgICAgIGlmICghZW5hYmxlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gZ2V0IHRoZSBtaW1lIHR5cGUgb2YgdGhlIGtlcm5lbCBsYW5ndWFnZSBmb3IgdGhlIGN1cnJlbnQgZGVidWcgc2Vzc2lvblxuICAgIGNvbnN0IGdldE1pbWVUeXBlID0gYXN5bmMgKCk6IFByb21pc2U8c3RyaW5nPiA9PiB7XG4gICAgICBjb25zdCBrZXJuZWwgPSBzZXJ2aWNlLnNlc3Npb24/LmNvbm5lY3Rpb24/Lmtlcm5lbDtcbiAgICAgIGlmICgha2VybmVsKSB7XG4gICAgICAgIHJldHVybiAnJztcbiAgICAgIH1cbiAgICAgIGNvbnN0IGluZm8gPSAoYXdhaXQga2VybmVsLmluZm8pLmxhbmd1YWdlX2luZm87XG4gICAgICBjb25zdCBuYW1lID0gaW5mby5uYW1lO1xuICAgICAgY29uc3QgbWltZVR5cGUgPVxuICAgICAgICBlZGl0b3JTZXJ2aWNlcy5taW1lVHlwZVNlcnZpY2UuZ2V0TWltZVR5cGVCeUxhbmd1YWdlKHsgbmFtZSB9KSA/PyAnJztcbiAgICAgIHJldHVybiBtaW1lVHlwZTtcbiAgICB9O1xuXG4gICAgY29uc3QgcmVuZGVybWltZSA9IG5ldyBSZW5kZXJNaW1lUmVnaXN0cnkoeyBpbml0aWFsRmFjdG9yaWVzIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmV2YWx1YXRlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0V2YWx1YXRlIENvZGUnKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdFdmFsdWF0ZSBDb2RlJyksXG4gICAgICBpY29uOiBEZWJ1Z2dlci5JY29ucy5ldmFsdWF0ZUljb24sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHNlcnZpY2UuaGFzU3RvcHBlZFRocmVhZHMoKSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgY29uc3QgbWltZVR5cGUgPSBhd2FpdCBnZXRNaW1lVHlwZSgpO1xuICAgICAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBEZWJ1Z2dlci5EaWFsb2dzLmdldENvZGUoe1xuICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnRXZhbHVhdGUgQ29kZScpLFxuICAgICAgICAgIG9rTGFiZWw6IHRyYW5zLl9fKCdFdmFsdWF0ZScpLFxuICAgICAgICAgIGNhbmNlbExhYmVsOiB0cmFucy5fXygnQ2FuY2VsJyksXG4gICAgICAgICAgbWltZVR5cGUsXG4gICAgICAgICAgY29udGVudEZhY3Rvcnk6IG5ldyBDb2RlQ2VsbC5Db250ZW50RmFjdG9yeSh7XG4gICAgICAgICAgICBlZGl0b3JGYWN0b3J5OiBvcHRpb25zID0+XG4gICAgICAgICAgICAgIGVkaXRvclNlcnZpY2VzLmZhY3RvcnlTZXJ2aWNlLm5ld0lubGluZUVkaXRvcihvcHRpb25zKVxuICAgICAgICAgIH0pLFxuICAgICAgICAgIHJlbmRlcm1pbWVcbiAgICAgICAgfSk7XG4gICAgICAgIGNvbnN0IGNvZGUgPSByZXN1bHQudmFsdWU7XG4gICAgICAgIGlmICghcmVzdWx0LmJ1dHRvbi5hY2NlcHQgfHwgIWNvZGUpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgcmVwbHkgPSBhd2FpdCBzZXJ2aWNlLmV2YWx1YXRlKGNvZGUpO1xuICAgICAgICBpZiAocmVwbHkpIHtcbiAgICAgICAgICBjb25zdCBkYXRhID0gcmVwbHkucmVzdWx0O1xuICAgICAgICAgIGNvbnN0IHBhdGggPSBzZXJ2aWNlPy5zZXNzaW9uPy5jb25uZWN0aW9uPy5wYXRoO1xuICAgICAgICAgIGNvbnN0IGxvZ2dlciA9IHBhdGggPyBsb2dnZXJSZWdpc3RyeT8uZ2V0TG9nZ2VyPy4ocGF0aCkgOiB1bmRlZmluZWQ7XG5cbiAgICAgICAgICBpZiAobG9nZ2VyKSB7XG4gICAgICAgICAgICAvLyBwcmludCB0byBsb2cgY29uc29sZSBvZiB0aGUgbm90ZWJvb2sgY3VycmVudGx5IGJlaW5nIGRlYnVnZ2VkXG4gICAgICAgICAgICBsb2dnZXIubG9nKHsgdHlwZTogJ3RleHQnLCBkYXRhLCBsZXZlbDogbG9nZ2VyLmxldmVsIH0pO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAvLyBmYWxsYmFjayB0byBwcmludGluZyB0byBkZXZ0b29scyBjb25zb2xlXG4gICAgICAgICAgICBjb25zb2xlLmRlYnVnKGRhdGEpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRlYnVnQ29udGludWUsIHtcbiAgICAgIGxhYmVsOiAoKSA9PiB7XG4gICAgICAgIHJldHVybiBzZXJ2aWNlLmhhc1N0b3BwZWRUaHJlYWRzKClcbiAgICAgICAgICA/IHRyYW5zLl9fKCdDb250aW51ZScpXG4gICAgICAgICAgOiB0cmFucy5fXygnUGF1c2UnKTtcbiAgICAgIH0sXG4gICAgICBjYXB0aW9uOiAoKSA9PiB7XG4gICAgICAgIHJldHVybiBzZXJ2aWNlLmhhc1N0b3BwZWRUaHJlYWRzKClcbiAgICAgICAgICA/IHRyYW5zLl9fKCdDb250aW51ZScpXG4gICAgICAgICAgOiB0cmFucy5fXygnUGF1c2UnKTtcbiAgICAgIH0sXG4gICAgICBpY29uOiAoKSA9PiB7XG4gICAgICAgIHJldHVybiBzZXJ2aWNlLmhhc1N0b3BwZWRUaHJlYWRzKClcbiAgICAgICAgICA/IERlYnVnZ2VyLkljb25zLmNvbnRpbnVlSWNvblxuICAgICAgICAgIDogRGVidWdnZXIuSWNvbnMucGF1c2VJY29uO1xuICAgICAgfSxcbiAgICAgIGlzRW5hYmxlZDogKCkgPT4gc2VydmljZS5zZXNzaW9uPy5pc1N0YXJ0ZWQgPz8gZmFsc2UsXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGlmIChzZXJ2aWNlLmhhc1N0b3BwZWRUaHJlYWRzKCkpIHtcbiAgICAgICAgICBhd2FpdCBzZXJ2aWNlLmNvbnRpbnVlKCk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgYXdhaXQgc2VydmljZS5wYXVzZSgpO1xuICAgICAgICB9XG4gICAgICAgIGNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMuZGVidWdDb250aW51ZSk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMudGVybWluYXRlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1Rlcm1pbmF0ZScpLFxuICAgICAgY2FwdGlvbjogdHJhbnMuX18oJ1Rlcm1pbmF0ZScpLFxuICAgICAgaWNvbjogRGVidWdnZXIuSWNvbnMudGVybWluYXRlSWNvbixcbiAgICAgIGlzRW5hYmxlZDogKCkgPT4gc2VydmljZS5oYXNTdG9wcGVkVGhyZWFkcygpLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBhd2FpdCBzZXJ2aWNlLnJlc3RhcnQoKTtcbiAgICAgICAgbm90aWZ5Q29tbWFuZHMoYXBwKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5uZXh0LCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ05leHQnKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdOZXh0JyksXG4gICAgICBpY29uOiBEZWJ1Z2dlci5JY29ucy5zdGVwT3Zlckljb24sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHNlcnZpY2UuaGFzU3RvcHBlZFRocmVhZHMoKSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgYXdhaXQgc2VydmljZS5uZXh0KCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc3RlcEluLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1N0ZXAgSW4nKSxcbiAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdTdGVwIEluJyksXG4gICAgICBpY29uOiBEZWJ1Z2dlci5JY29ucy5zdGVwSW50b0ljb24sXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHNlcnZpY2UuaGFzU3RvcHBlZFRocmVhZHMoKSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgYXdhaXQgc2VydmljZS5zdGVwSW4oKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zdGVwT3V0LCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1N0ZXAgT3V0JyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnU3RlcCBPdXQnKSxcbiAgICAgIGljb246IERlYnVnZ2VyLkljb25zLnN0ZXBPdXRJY29uLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiBzZXJ2aWNlLmhhc1N0b3BwZWRUaHJlYWRzKCksXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGF3YWl0IHNlcnZpY2Uuc3RlcE91dCgpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnBhdXNlT25FeGNlcHRpb25zLCB7XG4gICAgICBsYWJlbDogYXJncyA9PiAoYXJncy5maWx0ZXIgYXMgc3RyaW5nKSB8fCAnQnJlYWtwb2ludHMgb24gZXhjZXB0aW9uJyxcbiAgICAgIGNhcHRpb246IGFyZ3MgPT4gYXJncy5kZXNjcmlwdGlvbiBhcyBzdHJpbmcsXG4gICAgICBpc1RvZ2dsZWQ6IGFyZ3MgPT5cbiAgICAgICAgc2VydmljZS5zZXNzaW9uPy5pc1BhdXNpbmdPbkV4Y2VwdGlvbihhcmdzLmZpbHRlciBhcyBzdHJpbmcpIHx8IGZhbHNlLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiBzZXJ2aWNlLnBhdXNlT25FeGNlcHRpb25zSXNWYWxpZCgpLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgYXJncyA9PiB7XG4gICAgICAgIGlmIChhcmdzPy5maWx0ZXIpIHtcbiAgICAgICAgICBsZXQgZmlsdGVyID0gYXJncy5maWx0ZXIgYXMgc3RyaW5nO1xuICAgICAgICAgIGF3YWl0IHNlcnZpY2UucGF1c2VPbkV4Y2VwdGlvbnNGaWx0ZXIoZmlsdGVyIGFzIHN0cmluZyk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgbGV0IGl0ZW1zOiBzdHJpbmdbXSA9IFtdO1xuICAgICAgICAgIHNlcnZpY2Uuc2Vzc2lvbj8uZXhjZXB0aW9uQnJlYWtwb2ludEZpbHRlcnM/LmZvckVhY2goXG4gICAgICAgICAgICBhdmFpbGFibGVGaWx0ZXIgPT4ge1xuICAgICAgICAgICAgICBpdGVtcy5wdXNoKGF2YWlsYWJsZUZpbHRlci5maWx0ZXIpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICk7XG4gICAgICAgICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgSW5wdXREaWFsb2cuZ2V0TXVsdGlwbGVJdGVtcyh7XG4gICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ1NlbGVjdCBhIGZpbHRlciBmb3IgYnJlYWtwb2ludHMgb24gZXhjZXB0aW9uJyksXG4gICAgICAgICAgICBpdGVtczogaXRlbXMsXG4gICAgICAgICAgICBkZWZhdWx0czogc2VydmljZS5zZXNzaW9uPy5jdXJyZW50RXhjZXB0aW9uRmlsdGVycyB8fCBbXVxuICAgICAgICAgIH0pO1xuXG4gICAgICAgICAgbGV0IGZpbHRlcnMgPSByZXN1bHQuYnV0dG9uLmFjY2VwdCA/IHJlc3VsdC52YWx1ZSA6IG51bGw7XG4gICAgICAgICAgaWYgKGZpbHRlcnMgIT09IG51bGwpIHtcbiAgICAgICAgICAgIGF3YWl0IHNlcnZpY2UucGF1c2VPbkV4Y2VwdGlvbnMoZmlsdGVycyk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBsZXQgYXV0b0NvbGxhcHNlU2lkZWJhciA9IGZhbHNlO1xuXG4gICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgY29uc3Qgc2V0dGluZyA9IGF3YWl0IHNldHRpbmdSZWdpc3RyeS5sb2FkKG1haW4uaWQpO1xuICAgICAgY29uc3QgdXBkYXRlU2V0dGluZ3MgPSAoKTogdm9pZCA9PiB7XG4gICAgICAgIGF1dG9Db2xsYXBzZVNpZGViYXIgPSBzZXR0aW5nLmdldCgnYXV0b0NvbGxhcHNlRGVidWdnZXJTaWRlYmFyJylcbiAgICAgICAgICAuY29tcG9zaXRlIGFzIGJvb2xlYW47XG4gICAgICB9O1xuICAgICAgdXBkYXRlU2V0dGluZ3MoKTtcbiAgICAgIHNldHRpbmcuY2hhbmdlZC5jb25uZWN0KHVwZGF0ZVNldHRpbmdzKTtcbiAgICB9XG5cbiAgICBzZXJ2aWNlLmV2ZW50TWVzc2FnZS5jb25uZWN0KChfLCBldmVudCk6IHZvaWQgPT4ge1xuICAgICAgbm90aWZ5Q29tbWFuZHMoYXBwKTtcbiAgICAgIGlmIChsYWJTaGVsbCAmJiBldmVudC5ldmVudCA9PT0gJ2luaXRpYWxpemVkJykge1xuICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZUJ5SWQoc2lkZWJhci5pZCk7XG4gICAgICB9IGVsc2UgaWYgKFxuICAgICAgICBsYWJTaGVsbCAmJlxuICAgICAgICBzaWRlYmFyLmlzVmlzaWJsZSAmJlxuICAgICAgICBldmVudC5ldmVudCA9PT0gJ3Rlcm1pbmF0ZWQnICYmXG4gICAgICAgIGF1dG9Db2xsYXBzZVNpZGViYXJcbiAgICAgICkge1xuICAgICAgICBsYWJTaGVsbC5jb2xsYXBzZVJpZ2h0KCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBzZXJ2aWNlLnNlc3Npb25DaGFuZ2VkLmNvbm5lY3QoXyA9PiB7XG4gICAgICBub3RpZnlDb21tYW5kcyhhcHApO1xuICAgIH0pO1xuXG4gICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICByZXN0b3Jlci5hZGQoc2lkZWJhciwgJ2RlYnVnZ2VyLXNpZGViYXInKTtcbiAgICB9XG5cbiAgICBzaWRlYmFyLm5vZGUuc2V0QXR0cmlidXRlKCdyb2xlJywgJ3JlZ2lvbicpO1xuICAgIHNpZGViYXIubm9kZS5zZXRBdHRyaWJ1dGUoJ2FyaWEtbGFiZWwnLCB0cmFucy5fXygnRGVidWdnZXIgc2VjdGlvbicpKTtcblxuICAgIHNpZGViYXIudGl0bGUuY2FwdGlvbiA9IHRyYW5zLl9fKCdEZWJ1Z2dlcicpO1xuXG4gICAgc2hlbGwuYWRkKHNpZGViYXIsICdyaWdodCcsIHsgdHlwZTogJ0RlYnVnZ2VyJyB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaG93UGFuZWwsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRGVidWdnZXIgUGFuZWwnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgc2hlbGwuYWN0aXZhdGVCeUlkKHNpZGViYXIuaWQpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0RlYnVnZ2VyJyk7XG4gICAgICBbXG4gICAgICAgIENvbW1hbmRJRHMuZGVidWdDb250aW51ZSxcbiAgICAgICAgQ29tbWFuZElEcy50ZXJtaW5hdGUsXG4gICAgICAgIENvbW1hbmRJRHMubmV4dCxcbiAgICAgICAgQ29tbWFuZElEcy5zdGVwSW4sXG4gICAgICAgIENvbW1hbmRJRHMuc3RlcE91dCxcbiAgICAgICAgQ29tbWFuZElEcy5ldmFsdWF0ZSxcbiAgICAgICAgQ29tbWFuZElEcy5wYXVzZU9uRXhjZXB0aW9uc1xuICAgICAgXS5mb3JFYWNoKGNvbW1hbmQgPT4ge1xuICAgICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSB9KTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGlmIChkZWJ1Z2dlclNvdXJjZXMpIHtcbiAgICAgIGNvbnN0IHsgbW9kZWwgfSA9IHNlcnZpY2U7XG4gICAgICBjb25zdCByZWFkT25seUVkaXRvckZhY3RvcnkgPSBuZXcgRGVidWdnZXIuUmVhZE9ubHlFZGl0b3JGYWN0b3J5KHtcbiAgICAgICAgZWRpdG9yU2VydmljZXNcbiAgICAgIH0pO1xuXG4gICAgICBjb25zdCBvbkN1cnJlbnRGcmFtZUNoYW5nZWQgPSAoXG4gICAgICAgIF86IElEZWJ1Z2dlci5Nb2RlbC5JQ2FsbHN0YWNrLFxuICAgICAgICBmcmFtZTogSURlYnVnZ2VyLklTdGFja0ZyYW1lXG4gICAgICApOiB2b2lkID0+IHtcbiAgICAgICAgZGVidWdnZXJTb3VyY2VzXG4gICAgICAgICAgLmZpbmQoe1xuICAgICAgICAgICAgZm9jdXM6IHRydWUsXG4gICAgICAgICAgICBrZXJuZWw6IHNlcnZpY2Uuc2Vzc2lvbj8uY29ubmVjdGlvbj8ua2VybmVsPy5uYW1lID8/ICcnLFxuICAgICAgICAgICAgcGF0aDogc2VydmljZS5zZXNzaW9uPy5jb25uZWN0aW9uPy5wYXRoID8/ICcnLFxuICAgICAgICAgICAgc291cmNlOiBmcmFtZT8uc291cmNlPy5wYXRoID8/ICcnXG4gICAgICAgICAgfSlcbiAgICAgICAgICAuZm9yRWFjaChlZGl0b3IgPT4ge1xuICAgICAgICAgICAgcmVxdWVzdEFuaW1hdGlvbkZyYW1lKCgpID0+IHtcbiAgICAgICAgICAgICAgdm9pZCBlZGl0b3IucmV2ZWFsKCkudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgY29uc3QgZWRpdCA9IGVkaXRvci5nZXQoKTtcbiAgICAgICAgICAgICAgICBpZiAoZWRpdCkge1xuICAgICAgICAgICAgICAgICAgRGVidWdnZXIuRWRpdG9ySGFuZGxlci5zaG93Q3VycmVudExpbmUoZWRpdCwgZnJhbWUubGluZSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH0pO1xuICAgICAgfTtcblxuICAgICAgY29uc3Qgb25Tb3VyY2VPcGVuZWQgPSAoXG4gICAgICAgIF86IElEZWJ1Z2dlci5Nb2RlbC5JU291cmNlcyB8IG51bGwsXG4gICAgICAgIHNvdXJjZTogSURlYnVnZ2VyLlNvdXJjZSxcbiAgICAgICAgYnJlYWtwb2ludD86IElEZWJ1Z2dlci5JQnJlYWtwb2ludFxuICAgICAgKTogdm9pZCA9PiB7XG4gICAgICAgIGlmICghc291cmNlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IHsgY29udGVudCwgbWltZVR5cGUsIHBhdGggfSA9IHNvdXJjZTtcbiAgICAgICAgY29uc3QgcmVzdWx0cyA9IGRlYnVnZ2VyU291cmNlcy5maW5kKHtcbiAgICAgICAgICBmb2N1czogdHJ1ZSxcbiAgICAgICAgICBrZXJuZWw6IHNlcnZpY2Uuc2Vzc2lvbj8uY29ubmVjdGlvbj8ua2VybmVsPy5uYW1lID8/ICcnLFxuICAgICAgICAgIHBhdGg6IHNlcnZpY2Uuc2Vzc2lvbj8uY29ubmVjdGlvbj8ucGF0aCA/PyAnJyxcbiAgICAgICAgICBzb3VyY2U6IHBhdGhcbiAgICAgICAgfSk7XG4gICAgICAgIGlmIChyZXN1bHRzLmxlbmd0aCA+IDApIHtcbiAgICAgICAgICBpZiAoYnJlYWtwb2ludCAmJiB0eXBlb2YgYnJlYWtwb2ludC5saW5lICE9PSAndW5kZWZpbmVkJykge1xuICAgICAgICAgICAgcmVzdWx0cy5mb3JFYWNoKGVkaXRvciA9PiB7XG4gICAgICAgICAgICAgIHZvaWQgZWRpdG9yLnJldmVhbCgpLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgIGVkaXRvci5nZXQoKT8ucmV2ZWFsUG9zaXRpb24oe1xuICAgICAgICAgICAgICAgICAgbGluZTogKGJyZWFrcG9pbnQubGluZSBhcyBudW1iZXIpIC0gMSxcbiAgICAgICAgICAgICAgICAgIGNvbHVtbjogYnJlYWtwb2ludC5jb2x1bW4gfHwgMFxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgZWRpdG9yV3JhcHBlciA9IHJlYWRPbmx5RWRpdG9yRmFjdG9yeS5jcmVhdGVOZXdFZGl0b3Ioe1xuICAgICAgICAgIGNvbnRlbnQsXG4gICAgICAgICAgbWltZVR5cGUsXG4gICAgICAgICAgcGF0aFxuICAgICAgICB9KTtcbiAgICAgICAgY29uc3QgZWRpdG9yID0gZWRpdG9yV3JhcHBlci5lZGl0b3I7XG4gICAgICAgIGNvbnN0IGVkaXRvckhhbmRsZXIgPSBuZXcgRGVidWdnZXIuRWRpdG9ySGFuZGxlcih7XG4gICAgICAgICAgZGVidWdnZXJTZXJ2aWNlOiBzZXJ2aWNlLFxuICAgICAgICAgIGVkaXRvclJlYWR5OiAoKSA9PiBQcm9taXNlLnJlc29sdmUoZWRpdG9yKSxcbiAgICAgICAgICBnZXRFZGl0b3I6ICgpID0+IGVkaXRvcixcbiAgICAgICAgICBwYXRoLFxuICAgICAgICAgIHNyYzogZWRpdG9yLm1vZGVsLnNoYXJlZE1vZGVsXG4gICAgICAgIH0pO1xuICAgICAgICBlZGl0b3JXcmFwcGVyLmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4gZWRpdG9ySGFuZGxlci5kaXNwb3NlKCkpO1xuXG4gICAgICAgIGRlYnVnZ2VyU291cmNlcy5vcGVuKHtcbiAgICAgICAgICBsYWJlbDogUGF0aEV4dC5iYXNlbmFtZShwYXRoKSxcbiAgICAgICAgICBjYXB0aW9uOiBwYXRoLFxuICAgICAgICAgIGVkaXRvcldyYXBwZXJcbiAgICAgICAgfSk7XG5cbiAgICAgICAgY29uc3QgZnJhbWUgPSBzZXJ2aWNlLm1vZGVsLmNhbGxzdGFjay5mcmFtZTtcbiAgICAgICAgaWYgKGZyYW1lKSB7XG4gICAgICAgICAgRGVidWdnZXIuRWRpdG9ySGFuZGxlci5zaG93Q3VycmVudExpbmUoZWRpdG9yLCBmcmFtZS5saW5lKTtcbiAgICAgICAgfVxuICAgICAgfTtcblxuICAgICAgY29uc3Qgb25LZXJuZWxTb3VyY2VPcGVuZWQgPSAoXG4gICAgICAgIF86IElEZWJ1Z2dlci5Nb2RlbC5JS2VybmVsU291cmNlcyB8IG51bGwsXG4gICAgICAgIHNvdXJjZTogSURlYnVnZ2VyLlNvdXJjZSxcbiAgICAgICAgYnJlYWtwb2ludD86IElEZWJ1Z2dlci5JQnJlYWtwb2ludFxuICAgICAgKTogdm9pZCA9PiB7XG4gICAgICAgIGlmICghc291cmNlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIG9uU291cmNlT3BlbmVkKG51bGwsIHNvdXJjZSwgYnJlYWtwb2ludCk7XG4gICAgICB9O1xuXG4gICAgICBtb2RlbC5jYWxsc3RhY2suY3VycmVudEZyYW1lQ2hhbmdlZC5jb25uZWN0KG9uQ3VycmVudEZyYW1lQ2hhbmdlZCk7XG4gICAgICBtb2RlbC5zb3VyY2VzLmN1cnJlbnRTb3VyY2VPcGVuZWQuY29ubmVjdChvblNvdXJjZU9wZW5lZCk7XG4gICAgICBtb2RlbC5rZXJuZWxTb3VyY2VzLmtlcm5lbFNvdXJjZU9wZW5lZC5jb25uZWN0KG9uS2VybmVsU291cmNlT3BlbmVkKTtcbiAgICAgIG1vZGVsLmJyZWFrcG9pbnRzLmNsaWNrZWQuY29ubmVjdChhc3luYyAoXywgYnJlYWtwb2ludCkgPT4ge1xuICAgICAgICBjb25zdCBwYXRoID0gYnJlYWtwb2ludC5zb3VyY2U/LnBhdGg7XG4gICAgICAgIGNvbnN0IHNvdXJjZSA9IGF3YWl0IHNlcnZpY2UuZ2V0U291cmNlKHtcbiAgICAgICAgICBzb3VyY2VSZWZlcmVuY2U6IDAsXG4gICAgICAgICAgcGF0aFxuICAgICAgICB9KTtcbiAgICAgICAgb25Tb3VyY2VPcGVuZWQobnVsbCwgc291cmNlLCBicmVha3BvaW50KTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgZGVmYXVsdC5cbiAqL1xuY29uc3QgcGx1Z2luczogSnVweXRlckZyb250RW5kUGx1Z2luPGFueT5bXSA9IFtcbiAgc2VydmljZSxcbiAgY29uc29sZXMsXG4gIGZpbGVzLFxuICBub3RlYm9va3MsXG4gIHZhcmlhYmxlcyxcbiAgc2lkZWJhcixcbiAgbWFpbixcbiAgc291cmNlcyxcbiAgY29uZmlndXJhdGlvblxuXTtcblxuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==