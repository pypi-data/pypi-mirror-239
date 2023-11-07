"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_console-extension_lib_index_js"],{

/***/ "../packages/console-extension/lib/foreign.js":
/*!****************************************************!*\
  !*** ../packages/console-extension/lib/foreign.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "foreign": () => (/* binding */ foreign)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The console foreign handler.
 */
const foreign = {
    id: '@jupyterlab/console-extension:foreign',
    description: 'Add foreign handler of IOPub messages to the console.',
    requires: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__.IConsoleTracker, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette],
    activate: activateForeign,
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (foreign);
function activateForeign(app, tracker, settingRegistry, translator, palette) {
    const trans = translator.load('jupyterlab');
    const { shell } = app;
    tracker.widgetAdded.connect((sender, widget) => {
        const console = widget.console;
        const handler = new _jupyterlab_console__WEBPACK_IMPORTED_MODULE_1__.ForeignHandler({
            sessionContext: console.sessionContext,
            parent: console
        });
        Private.foreignHandlerProperty.set(console, handler);
        // Property showAllKernelActivity configures foreign handler enabled on start.
        void settingRegistry
            .get('@jupyterlab/console-extension:tracker', 'showAllKernelActivity')
            .then(({ composite }) => {
            const showAllKernelActivity = composite;
            handler.enabled = showAllKernelActivity;
        });
        console.disposed.connect(() => {
            handler.dispose();
        });
    });
    const { commands } = app;
    const category = trans.__('Console');
    const toggleShowAllActivity = 'console:toggle-show-all-kernel-activity';
    // Get the current widget and activate unless the args specify otherwise.
    function getCurrent(args) {
        const widget = tracker.currentWidget;
        const activate = args['activate'] !== false;
        if (activate && widget) {
            shell.activateById(widget.id);
        }
        return widget;
    }
    commands.addCommand(toggleShowAllActivity, {
        label: args => trans.__('Show All Kernel Activity'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            const handler = Private.foreignHandlerProperty.get(current.console);
            if (handler) {
                handler.enabled = !handler.enabled;
            }
        },
        isToggled: () => {
            var _a;
            return tracker.currentWidget !== null &&
                !!((_a = Private.foreignHandlerProperty.get(tracker.currentWidget.console)) === null || _a === void 0 ? void 0 : _a.enabled);
        },
        isEnabled: () => tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget
    });
    if (palette) {
        palette.addItem({
            command: toggleShowAllActivity,
            category,
            args: { isPalette: true }
        });
    }
}
/*
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property for a console's foreign handler.
     */
    Private.foreignHandlerProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_4__.AttachedProperty({
        name: 'foreignHandler',
        create: () => undefined
    });
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/console-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../packages/console-extension/lib/index.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _foreign__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./foreign */ "../packages/console-extension/lib/foreign.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module console-extension
 */
















/**
 * The command IDs used by the console plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.autoClosingBrackets = 'console:toggle-autoclosing-brackets';
    CommandIDs.create = 'console:create';
    CommandIDs.clear = 'console:clear';
    CommandIDs.runUnforced = 'console:run-unforced';
    CommandIDs.runForced = 'console:run-forced';
    CommandIDs.linebreak = 'console:linebreak';
    CommandIDs.interrupt = 'console:interrupt-kernel';
    CommandIDs.restart = 'console:restart-kernel';
    CommandIDs.closeAndShutdown = 'console:close-and-shutdown';
    CommandIDs.open = 'console:open';
    CommandIDs.inject = 'console:inject';
    CommandIDs.changeKernel = 'console:change-kernel';
    CommandIDs.getKernel = 'console:get-kernel';
    CommandIDs.enterToExecute = 'console:enter-to-execute';
    CommandIDs.shiftEnterToExecute = 'console:shift-enter-to-execute';
    CommandIDs.interactionMode = 'console:interaction-mode';
    CommandIDs.replaceSelection = 'console:replace-selection';
    CommandIDs.shutdown = 'console:shutdown';
    CommandIDs.invokeCompleter = 'completer:invoke-console';
    CommandIDs.selectCompleter = 'completer:select-console';
})(CommandIDs || (CommandIDs = {}));
/**
 * The console widget tracker provider.
 */
const tracker = {
    id: '@jupyterlab/console-extension:tracker',
    description: 'Provides the console widget tracker.',
    provides: _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker,
    requires: [
        _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.ConsolePanel.IContentFactory,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_8__.IRenderMimeRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_9__.ISettingRegistry
    ],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_5__.IDefaultFileBrowser,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_7__.IMainMenu,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_6__.ILauncher,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs,
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.IFormRendererRegistry,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.ITranslator
    ],
    activate: activateConsole,
    autoStart: true
};
/**
 * The console widget content factory.
 */
const factory = {
    id: '@jupyterlab/console-extension:factory',
    description: 'Provides the console widget content factory.',
    provides: _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.ConsolePanel.IContentFactory,
    requires: [_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices],
    autoStart: true,
    activate: (app, editorServices) => {
        const editorFactory = editorServices.factoryService.newInlineEditor;
        return new _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.ConsolePanel.ContentFactory({ editorFactory });
    }
};
/**
 * Kernel status indicator.
 */
const kernelStatus = {
    id: '@jupyterlab/console-extension:kernel-status',
    description: 'Adds the console to the kernel status indicator model.',
    autoStart: true,
    requires: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IKernelStatusModel],
    activate: (app, tracker, kernelStatus) => {
        const provider = (widget) => {
            let session = null;
            if (widget && tracker.has(widget)) {
                return widget.sessionContext;
            }
            return session;
        };
        kernelStatus.addSessionProvider(provider);
    }
};
/**
 * Cursor position.
 */
const lineColStatus = {
    id: '@jupyterlab/console-extension:cursor-position',
    description: 'Adds the console to the code editor cursor position model.',
    autoStart: true,
    requires: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IPositionModel],
    activate: (app, tracker, positionModel) => {
        let previousWidget = null;
        const provider = async (widget) => {
            let editor = null;
            if (widget !== previousWidget) {
                previousWidget === null || previousWidget === void 0 ? void 0 : previousWidget.console.promptCellCreated.disconnect(positionModel.update);
                previousWidget = null;
                if (widget && tracker.has(widget)) {
                    widget.console.promptCellCreated.connect(positionModel.update);
                    const promptCell = widget.console.promptCell;
                    editor = null;
                    if (promptCell) {
                        await promptCell.ready;
                        editor = promptCell.editor;
                    }
                    previousWidget = widget;
                }
            }
            else if (widget) {
                const promptCell = widget.console.promptCell;
                editor = null;
                if (promptCell) {
                    await promptCell.ready;
                    editor = promptCell.editor;
                }
            }
            return editor;
        };
        positionModel.addEditorProvider(provider);
    }
};
const completerPlugin = {
    id: '@jupyterlab/console-extension:completer',
    description: 'Adds completion to the console.',
    autoStart: true,
    requires: [_jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.IConsoleTracker],
    optional: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_3__.ICompletionProviderManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.ITranslator, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISanitizer],
    activate: activateConsoleCompleterService
};
/**
 * Export the plugins as the default.
 */
const plugins = [
    factory,
    tracker,
    _foreign__WEBPACK_IMPORTED_MODULE_15__["default"],
    kernelStatus,
    lineColStatus,
    completerPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * Activate the console extension.
 */
async function activateConsole(app, contentFactory, editorServices, rendermime, settingRegistry, restorer, filebrowser, mainMenu, palette, launcher, status, sessionDialogs_, formRegistry, translator_) {
    const translator = translator_ !== null && translator_ !== void 0 ? translator_ : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.nullTranslator;
    const trans = translator.load('jupyterlab');
    const manager = app.serviceManager;
    const { commands, shell } = app;
    const category = trans.__('Console');
    const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SessionContextDialogs({ translator });
    // Create a widget tracker for all console panels.
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'console'
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.create,
            args: widget => {
                const { path, name, kernelPreference } = widget.console.sessionContext;
                return {
                    path,
                    name,
                    kernelPreference: { ...kernelPreference }
                };
            },
            name: widget => { var _a; return (_a = widget.console.sessionContext.path) !== null && _a !== void 0 ? _a : _lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__.UUID.uuid4(); },
            when: manager.ready
        });
    }
    // Add a launcher item if the launcher is available.
    if (launcher) {
        void manager.ready.then(() => {
            let disposables = null;
            const onSpecsChanged = () => {
                if (disposables) {
                    disposables.dispose();
                    disposables = null;
                }
                const specs = manager.kernelspecs.specs;
                if (!specs) {
                    return;
                }
                disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_14__.DisposableSet();
                for (const name in specs.kernelspecs) {
                    const rank = name === specs.default ? 0 : Infinity;
                    const spec = specs.kernelspecs[name];
                    const kernelIconUrl = spec.resources['logo-svg'] || spec.resources['logo-64x64'];
                    disposables.add(launcher.add({
                        command: CommandIDs.create,
                        args: { isLauncher: true, kernelPreference: { name } },
                        category: trans.__('Console'),
                        rank,
                        kernelIconUrl,
                        metadata: {
                            kernel: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_13__.JSONExt.deepCopy(spec.metadata || {})
                        }
                    }));
                }
            };
            onSpecsChanged();
            manager.kernelspecs.specsChanged.connect(onSpecsChanged);
        });
    }
    /**
     * Create a console for a given path.
     */
    async function createConsole(options) {
        var _a, _b;
        await manager.ready;
        const panel = new _jupyterlab_console__WEBPACK_IMPORTED_MODULE_4__.ConsolePanel({
            manager,
            contentFactory,
            mimeTypeService: editorServices.mimeTypeService,
            rendermime,
            sessionDialogs,
            translator,
            setBusy: (_a = (status && (() => status.setBusy()))) !== null && _a !== void 0 ? _a : undefined,
            ...options
        });
        const interactionMode = (await settingRegistry.get('@jupyterlab/console-extension:tracker', 'interactionMode')).composite;
        panel.console.node.dataset.jpInteractionMode = interactionMode;
        // Add the console panel to the tracker. We want the panel to show up before
        // any kernel selection dialog, so we do not await panel.session.ready;
        await tracker.add(panel);
        panel.sessionContext.propertyChanged.connect(() => {
            void tracker.save(panel);
        });
        shell.add(panel, 'main', {
            ref: options.ref,
            mode: options.insertMode,
            activate: options.activate !== false,
            type: (_b = options.type) !== null && _b !== void 0 ? _b : 'Console'
        });
        return panel;
    }
    const pluginId = '@jupyterlab/console-extension:tracker';
    let interactionMode;
    let promptCellConfig = {};
    /**
     * Update settings for one console or all consoles.
     *
     * @param panel Optional - single console to update.
     */
    async function updateSettings(panel) {
        interactionMode = (await settingRegistry.get(pluginId, 'interactionMode'))
            .composite;
        promptCellConfig = (await settingRegistry.get(pluginId, 'promptCellConfig'))
            .composite;
        const setWidgetOptions = (widget) => {
            var _a, _b;
            widget.console.node.dataset.jpInteractionMode = interactionMode;
            // Update future promptCells
            widget.console.editorConfig = promptCellConfig;
            // Update promptCell already on screen
            (_b = (_a = widget.console.promptCell) === null || _a === void 0 ? void 0 : _a.editor) === null || _b === void 0 ? void 0 : _b.setOptions(promptCellConfig);
        };
        if (panel) {
            setWidgetOptions(panel);
        }
        else {
            tracker.forEach(setWidgetOptions);
        }
    }
    settingRegistry.pluginChanged.connect((sender, plugin) => {
        if (plugin === pluginId) {
            void updateSettings();
        }
    });
    await updateSettings();
    if (formRegistry) {
        const CMRenderer = formRegistry.getRenderer('@jupyterlab/codemirror-extension:plugin.defaultConfig');
        if (CMRenderer) {
            formRegistry.addRenderer('@jupyterlab/console-extension:tracker.promptCellConfig', CMRenderer);
        }
    }
    // Apply settings when a console is created.
    tracker.widgetAdded.connect((sender, panel) => {
        void updateSettings(panel);
    });
    commands.addCommand(CommandIDs.autoClosingBrackets, {
        execute: async (args) => {
            var _a;
            promptCellConfig.autoClosingBrackets = !!((_a = args['force']) !== null && _a !== void 0 ? _a : !promptCellConfig.autoClosingBrackets);
            await settingRegistry.set(pluginId, 'promptCellConfig', promptCellConfig);
        },
        label: trans.__('Auto Close Brackets for Code Console Prompt'),
        isToggled: () => promptCellConfig.autoClosingBrackets
    });
    /**
     * Whether there is an active console.
     */
    function isEnabled() {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    let command = CommandIDs.open;
    commands.addCommand(command, {
        label: trans.__('Open a console for the provided `path`.'),
        execute: (args) => {
            const path = args['path'];
            const widget = tracker.find(value => {
                var _a;
                return ((_a = value.console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === path;
            });
            if (widget) {
                if (args.activate !== false) {
                    shell.activateById(widget.id);
                }
                return widget;
            }
            else {
                return manager.ready.then(() => {
                    const model = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_12__.find)(manager.sessions.running(), item => {
                        return item.path === path;
                    });
                    if (model) {
                        return createConsole(args);
                    }
                    return Promise.reject(`No running kernel session for path: ${path}`);
                });
            }
        }
    });
    command = CommandIDs.create;
    commands.addCommand(command, {
        label: args => {
            var _a, _b, _c, _d;
            if (args['isPalette']) {
                return trans.__('New Console');
            }
            else if (args['isLauncher'] && args['kernelPreference']) {
                const kernelPreference = args['kernelPreference'];
                // TODO: Lumino command functions should probably be allowed to return undefined?
                return ((_d = (_c = (_b = (_a = manager.kernelspecs) === null || _a === void 0 ? void 0 : _a.specs) === null || _b === void 0 ? void 0 : _b.kernelspecs[kernelPreference.name || '']) === null || _c === void 0 ? void 0 : _c.display_name) !== null && _d !== void 0 ? _d : '');
            }
            return trans.__('Console');
        },
        icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_11__.consoleIcon),
        execute: args => {
            var _a;
            const basePath = (_a = (args['basePath'] ||
                args['cwd'] ||
                (filebrowser === null || filebrowser === void 0 ? void 0 : filebrowser.model.path))) !== null && _a !== void 0 ? _a : '';
            return createConsole({ basePath, ...args });
        }
    });
    // Get the current widget and activate unless the args specify otherwise.
    function getCurrent(args) {
        const widget = tracker.currentWidget;
        const activate = args['activate'] !== false;
        if (activate && widget) {
            shell.activateById(widget.id);
        }
        return widget !== null && widget !== void 0 ? widget : null;
    }
    commands.addCommand(CommandIDs.clear, {
        label: trans.__('Clear Console Cells'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            current.console.clear();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runUnforced, {
        label: trans.__('Run Cell (unforced)'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.execute();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.runForced, {
        label: trans.__('Run Cell (forced)'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.execute(true);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.linebreak, {
        label: trans.__('Insert Line Break'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            current.console.insertLinebreak();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.replaceSelection, {
        label: trans.__('Replace Selection in Console'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            const text = args['text'] || '';
            current.console.replaceSelection(text);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.interrupt, {
        label: trans.__('Interrupt Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Kernel…'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return sessionDialogs.restart(current.console.sessionContext);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.shutdown, {
        label: trans.__('Shut Down'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return current.console.sessionContext.shutdown();
        }
    });
    commands.addCommand(CommandIDs.closeAndShutdown, {
        label: trans.__('Close and Shut Down…'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut down the console?'),
                body: trans.__('Are you sure you want to close "%1"?', current.title.label),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({
                        ariaLabel: trans.__('Cancel console Shut Down')
                    }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({
                        ariaLabel: trans.__('Confirm console Shut Down')
                    })
                ]
            }).then(result => {
                if (result.button.accept) {
                    return commands
                        .execute(CommandIDs.shutdown, { activate: false })
                        .then(() => {
                        current.dispose();
                        return true;
                    });
                }
                else {
                    return false;
                }
            });
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.inject, {
        label: trans.__('Inject some code in a console.'),
        execute: args => {
            const path = args['path'];
            tracker.find(widget => {
                var _a;
                if (((_a = widget.console.sessionContext.session) === null || _a === void 0 ? void 0 : _a.path) === path) {
                    if (args['activate'] !== false) {
                        shell.activateById(widget.id);
                    }
                    void widget.console.inject(args['code'], args['metadata']);
                    return true;
                }
                return false;
            });
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.changeKernel, {
        label: trans.__('Change Kernel…'),
        execute: args => {
            const current = getCurrent(args);
            if (!current) {
                return;
            }
            return sessionDialogs.selectKernel(current.console.sessionContext);
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.getKernel, {
        label: trans.__('Get Kernel'),
        execute: args => {
            var _a;
            const current = getCurrent({ activate: false, ...args });
            if (!current) {
                return;
            }
            return (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        },
        isEnabled
    });
    if (palette) {
        // Add command palette items
        [
            CommandIDs.create,
            CommandIDs.linebreak,
            CommandIDs.clear,
            CommandIDs.runUnforced,
            CommandIDs.runForced,
            CommandIDs.restart,
            CommandIDs.interrupt,
            CommandIDs.changeKernel,
            CommandIDs.closeAndShutdown
        ].forEach(command => {
            palette.addItem({ command, category, args: { isPalette: true } });
        });
    }
    if (mainMenu) {
        // Add a close and shutdown command to the file menu.
        mainMenu.fileMenu.closeAndCleaners.add({
            id: CommandIDs.closeAndShutdown,
            isEnabled
        });
        // Add a kernel user to the Kernel menu
        mainMenu.kernelMenu.kernelUsers.changeKernel.add({
            id: CommandIDs.changeKernel,
            isEnabled
        });
        mainMenu.kernelMenu.kernelUsers.clearWidget.add({
            id: CommandIDs.clear,
            isEnabled
        });
        mainMenu.kernelMenu.kernelUsers.interruptKernel.add({
            id: CommandIDs.interrupt,
            isEnabled
        });
        mainMenu.kernelMenu.kernelUsers.restartKernel.add({
            id: CommandIDs.restart,
            isEnabled
        });
        mainMenu.kernelMenu.kernelUsers.shutdownKernel.add({
            id: CommandIDs.shutdown,
            isEnabled
        });
        // Add a code runner to the Run menu.
        mainMenu.runMenu.codeRunners.run.add({
            id: CommandIDs.runForced,
            isEnabled
        });
        // Add a clearer to the edit menu
        mainMenu.editMenu.clearers.clearCurrent.add({
            id: CommandIDs.clear,
            isEnabled
        });
        // Add kernel information to the application help menu.
        mainMenu.helpMenu.getKernel.add({
            id: CommandIDs.getKernel,
            isEnabled
        });
    }
    // For backwards compatibility and clarity, we explicitly label the run
    // keystroke with the actual effected change, rather than the generic
    // "notebook" or "terminal" interaction mode. When this interaction mode
    // affects more than just the run keystroke, we can make this menu title more
    // generic.
    const runShortcutTitles = {
        notebook: trans.__('Execute with Shift+Enter'),
        terminal: trans.__('Execute with Enter')
    };
    // Add the execute keystroke setting submenu.
    commands.addCommand(CommandIDs.interactionMode, {
        label: args => {
            var _a;
            return (_a = runShortcutTitles[args['interactionMode']]) !== null && _a !== void 0 ? _a : 'Set the console interaction mode.';
        },
        execute: async (args) => {
            const key = 'keyMap';
            try {
                await settingRegistry.set(pluginId, 'interactionMode', args['interactionMode']);
            }
            catch (reason) {
                console.error(`Failed to set ${pluginId}:${key} - ${reason.message}`);
            }
        },
        isToggled: args => args['interactionMode'] === interactionMode
    });
    return tracker;
}
/**
 * Activate the completer service for console.
 */
function activateConsoleCompleterService(app, consoles, manager, translator, appSanitizer) {
    if (!manager) {
        return;
    }
    const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_10__.nullTranslator).load('jupyterlab');
    const sanitizer = appSanitizer !== null && appSanitizer !== void 0 ? appSanitizer : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Sanitizer();
    app.commands.addCommand(CommandIDs.invokeCompleter, {
        label: trans.__('Display the completion helper.'),
        execute: () => {
            const id = consoles.currentWidget && consoles.currentWidget.id;
            if (id) {
                return manager.invoke(id);
            }
        }
    });
    app.commands.addCommand(CommandIDs.selectCompleter, {
        label: trans.__('Select the completion suggestion.'),
        execute: () => {
            const id = consoles.currentWidget && consoles.currentWidget.id;
            if (id) {
                return manager.select(id);
            }
        }
    });
    app.commands.addKeyBinding({
        command: CommandIDs.selectCompleter,
        keys: ['Enter'],
        selector: '.jp-ConsolePanel .jp-mod-completer-active'
    });
    const updateCompleter = async (_, consolePanel) => {
        var _a, _b;
        const completerContext = {
            editor: (_b = (_a = consolePanel.console.promptCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null,
            session: consolePanel.console.sessionContext.session,
            widget: consolePanel
        };
        await manager.updateCompleter(completerContext);
        consolePanel.console.promptCellCreated.connect((codeConsole, cell) => {
            const newContext = {
                editor: cell.editor,
                session: codeConsole.sessionContext.session,
                widget: consolePanel,
                sanitzer: sanitizer
            };
            manager.updateCompleter(newContext).catch(console.error);
        });
        consolePanel.console.sessionContext.sessionChanged.connect(() => {
            var _a, _b;
            const newContext = {
                editor: (_b = (_a = consolePanel.console.promptCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null,
                session: consolePanel.console.sessionContext.session,
                widget: consolePanel,
                sanitizer: sanitizer
            };
            manager.updateCompleter(newContext).catch(console.error);
        });
    };
    consoles.widgetAdded.connect(updateCompleter);
    manager.activeProvidersChanged.connect(() => {
        consoles.forEach(consoleWidget => {
            updateCompleter(undefined, consoleWidget).catch(e => console.error(e));
        });
    });
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY29uc29sZS1leHRlbnNpb25fbGliX2luZGV4X2pzLmY5ZTk2Y2I0MDliOTljZmQwOGE5LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFNSjtBQU0xQjtBQUNrQztBQUNUO0FBRUE7QUFFdEQ7O0dBRUc7QUFDSSxNQUFNLE9BQU8sR0FBZ0M7SUFDbEQsRUFBRSxFQUFFLHVDQUF1QztJQUMzQyxXQUFXLEVBQUUsdURBQXVEO0lBQ3BFLFFBQVEsRUFBRSxDQUFDLGdFQUFlLEVBQUUseUVBQWdCLEVBQUUsZ0VBQVcsQ0FBQztJQUMxRCxRQUFRLEVBQUUsQ0FBQyxpRUFBZSxDQUFDO0lBQzNCLFFBQVEsRUFBRSxlQUFlO0lBQ3pCLFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRixpRUFBZSxPQUFPLEVBQUM7QUFFdkIsU0FBUyxlQUFlLENBQ3RCLEdBQW9CLEVBQ3BCLE9BQXdCLEVBQ3hCLGVBQWlDLEVBQ2pDLFVBQXVCLEVBQ3ZCLE9BQStCO0lBRS9CLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7SUFDNUMsTUFBTSxFQUFFLEtBQUssRUFBRSxHQUFHLEdBQUcsQ0FBQztJQUN0QixPQUFPLENBQUMsV0FBVyxDQUFDLE9BQU8sQ0FBQyxDQUFDLE1BQU0sRUFBRSxNQUFNLEVBQUUsRUFBRTtRQUM3QyxNQUFNLE9BQU8sR0FBRyxNQUFNLENBQUMsT0FBTyxDQUFDO1FBRS9CLE1BQU0sT0FBTyxHQUFHLElBQUksK0RBQWMsQ0FBQztZQUNqQyxjQUFjLEVBQUUsT0FBTyxDQUFDLGNBQWM7WUFDdEMsTUFBTSxFQUFFLE9BQU87U0FDaEIsQ0FBQyxDQUFDO1FBQ0gsT0FBTyxDQUFDLHNCQUFzQixDQUFDLEdBQUcsQ0FBQyxPQUFPLEVBQUUsT0FBTyxDQUFDLENBQUM7UUFFckQsOEVBQThFO1FBQzlFLEtBQUssZUFBZTthQUNqQixHQUFH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QUFFLFlBQVk7Z0JBQ3BCLFNBQVMsRUFBRSxTQUFTO2FBQ3JCLENBQUM7WUFDRixPQUFPLENBQUMsZUFBZSxDQUFDLFVBQVUsQ0FBQyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLENBQUM7UUFDM0QsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDLENBQUM7SUFDRixRQUFRLENBQUMsV0FBVyxDQUFDLE9BQU8sQ0FBQyxlQUFlLENBQUMsQ0FBQztJQUM5QyxPQUFPLENBQUMsc0JBQXNCLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFBRTtRQUMxQyxRQUFRLENBQUMsT0FBTyxDQUFDLGFBQWEsQ0FBQyxFQUFFO1lBQy9CLGVBQWUsQ0FBQyxTQUFTLEVBQUUsYUFBYSxDQUFDLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO1FBQ3pFLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxDQUFDLENBQUM7QUFDTCxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvbnNvbGUtZXh0ZW5zaW9uL3NyYy9mb3JlaWduLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb25zb2xlLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJQ29tbWFuZFBhbGV0dGUgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQge1xuICBDb2RlQ29uc29sZSxcbiAgQ29uc29sZVBhbmVsLFxuICBGb3JlaWduSGFuZGxlcixcbiAgSUNvbnNvbGVUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2NvbnNvbGUnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBBdHRhY2hlZFByb3BlcnR5IH0gZnJvbSAnQGx1bWluby9wcm9wZXJ0aWVzJztcblxuLyoqXG4gKiBUaGUgY29uc29sZSBmb3JlaWduIGhhbmRsZXIuXG4gKi9cbmV4cG9ydCBjb25zdCBmb3JlaWduOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY29uc29sZS1leHRlbnNpb246Zm9yZWlnbicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkIGZvcmVpZ24gaGFuZGxlciBvZiBJT1B1YiBtZXNzYWdlcyB0byB0aGUgY29uc29sZS4nLFxuICByZXF1aXJlczogW0lDb25zb2xlVHJhY2tlciwgSVNldHRpbmdSZWdpc3RyeSwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZV0sXG4gIGFjdGl2YXRlOiBhY3RpdmF0ZUZvcmVpZ24sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuZXhwb3J0IGRlZmF1bHQgZm9yZWlnbjtcblxuZnVuY3Rpb24gYWN0aXZhdGVGb3JlaWduKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgdHJhY2tlcjogSUNvbnNvbGVUcmFja2VyLFxuICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4pOiB2b2lkIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgeyBzaGVsbCB9ID0gYXBwO1xuICB0cmFja2VyLndpZGdldEFkZGVkLmNvbm5lY3QoKHNlbmRlciwgd2lkZ2V0KSA9PiB7XG4gICAgY29uc3QgY29uc29sZSA9IHdpZGdldC5jb25zb2xlO1xuXG4gICAgY29uc3QgaGFuZGxlciA9IG5ldyBGb3JlaWduSGFuZGxlcih7XG4gICAgICBzZXNzaW9uQ29udGV4dDogY29uc29sZS5zZXNzaW9uQ29udGV4dCxcbiAgICAgIHBhcmVudDogY29uc29sZVxuICAgIH0pO1xuICAgIFByaXZhdGUuZm9yZWlnbkhhbmRsZXJQcm9wZXJ0eS5zZXQoY29uc29sZSwgaGFuZGxlcik7XG5cbiAgICAvLyBQcm9wZXJ0eSBzaG93QWxsS2VybmVsQWN0aXZpdHkgY29uZmlndXJlcyBmb3JlaWduIGhhbmRsZXIgZW5hYmxlZCBvbiBzdGFydC5cbiAgICB2b2lkIHNldHRpbmdSZWdpc3RyeVxuICAgICAgLmdldCgnQGp1cHl0ZXJsYWIvY29uc29sZS1leHRlbnNpb246dHJhY2tlcicsICdzaG93QWxsS2VybmVsQWN0aXZpdHknKVxuICAgICAgLnRoZW4oKHsgY29tcG9zaXRlIH0pID0+IHtcbiAgICAgICAgY29uc3Qgc2hvd0FsbEtlcm5lbEFjdGl2aXR5ID0gY29tcG9zaXRlIGFzIGJvb2xlYW47XG4gICAgICAgIGhhbmRsZXIuZW5hYmxlZCA9IHNob3dBbGxLZXJuZWxBY3Rpdml0eTtcbiAgICAgIH0pO1xuXG4gICAgY29uc29sZS5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIGhhbmRsZXIuZGlzcG9zZSgpO1xuICAgIH0pO1xuICB9KTtcblxuICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG4gIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0NvbnNvbGUnKTtcbiAgY29uc3QgdG9nZ2xlU2hvd0FsbEFjdGl2aXR5ID0gJ2NvbnNvbGU6dG9nZ2xlLXNob3ctYWxsLWtlcm5lbC1hY3Rpdml0eSc7XG5cbiAgLy8gR2V0IHRoZSBjdXJyZW50IHdpZGdldCBhbmQgYWN0aXZhdGUgdW5sZXNzIHRoZSBhcmdzIHNwZWNpZnkgb3RoZXJ3aXNlLlxuICBmdW5jdGlvbiBnZXRDdXJyZW50KGFyZ3M6IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QpOiBDb25zb2xlUGFuZWwgfCBudWxsIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgY29uc3QgYWN0aXZhdGUgPSBhcmdzWydhY3RpdmF0ZSddICE9PSBmYWxzZTtcbiAgICBpZiAoYWN0aXZhdGUgJiYgd2lkZ2V0KSB7XG4gICAgICBzaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICB9XG4gICAgcmV0dXJuIHdpZGdldDtcbiAgfVxuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQodG9nZ2xlU2hvd0FsbEFjdGl2aXR5LCB7XG4gICAgbGFiZWw6IGFyZ3MgPT4gdHJhbnMuX18oJ1Nob3cgQWxsIEtlcm5lbCBBY3Rpdml0eScpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IGdldEN1cnJlbnQoYXJncyk7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgaGFuZGxlciA9IFByaXZhdGUuZm9yZWlnbkhhbmRsZXJQcm9wZXJ0eS5nZXQoY3VycmVudC5jb25zb2xlKTtcbiAgICAgIGlmIChoYW5kbGVyKSB7XG4gICAgICAgIGhhbmRsZXIuZW5hYmxlZCA9ICFoYW5kbGVyLmVuYWJsZWQ7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+XG4gICAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgIT09IG51bGwgJiZcbiAgICAgICEhUHJpdmF0ZS5mb3JlaWduSGFuZGxlclByb3BlcnR5LmdldCh0cmFja2VyLmN1cnJlbnRXaWRnZXQuY29uc29sZSlcbiAgICAgICAgPy5lbmFibGVkLFxuICAgIGlzRW5hYmxlZDogKCkgPT5cbiAgICAgIHRyYWNrZXIuY3VycmVudFdpZGdldCAhPT0gbnVsbCAmJlxuICAgICAgdHJhY2tlci5jdXJyZW50V2lkZ2V0ID09PSBzaGVsbC5jdXJyZW50V2lkZ2V0XG4gIH0pO1xuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IHRvZ2dsZVNob3dBbGxBY3Rpdml0eSxcbiAgICAgIGNhdGVnb3J5LFxuICAgICAgYXJnczogeyBpc1BhbGV0dGU6IHRydWUgfVxuICAgIH0pO1xuICB9XG59XG5cbi8qXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBbiBhdHRhY2hlZCBwcm9wZXJ0eSBmb3IgYSBjb25zb2xlJ3MgZm9yZWlnbiBoYW5kbGVyLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGZvcmVpZ25IYW5kbGVyUHJvcGVydHkgPSBuZXcgQXR0YWNoZWRQcm9wZXJ0eTxcbiAgICBDb2RlQ29uc29sZSxcbiAgICBGb3JlaWduSGFuZGxlciB8IHVuZGVmaW5lZFxuICA+KHtcbiAgICBuYW1lOiAnZm9yZWlnbkhhbmRsZXInLFxuICAgIGNyZWF0ZTogKCkgPT4gdW5kZWZpbmVkXG4gIH0pO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY29uc29sZS1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU3RhdHVzLFxuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIERpYWxvZyxcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBJS2VybmVsU3RhdHVzTW9kZWwsXG4gIElTYW5pdGl6ZXIsXG4gIElTZXNzaW9uQ29udGV4dCxcbiAgSVNlc3Npb25Db250ZXh0RGlhbG9ncyxcbiAgU2FuaXRpemVyLFxuICBTZXNzaW9uQ29udGV4dERpYWxvZ3MsXG4gIHNob3dEaWFsb2csXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgQ29kZUVkaXRvcixcbiAgSUVkaXRvclNlcnZpY2VzLFxuICBJUG9zaXRpb25Nb2RlbFxufSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IElDb21wbGV0aW9uUHJvdmlkZXJNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29tcGxldGVyJztcbmltcG9ydCB7IENvbnNvbGVQYW5lbCwgSUNvbnNvbGVUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29uc29sZSc7XG5pbXBvcnQgeyBJRGVmYXVsdEZpbGVCcm93c2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXInO1xuaW1wb3J0IHsgSUxhdW5jaGVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbGF1bmNoZXInO1xuaW1wb3J0IHsgSU1haW5NZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvbWFpbm1lbnUnO1xuaW1wb3J0IHsgSVJlbmRlck1pbWUsIElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgY29uc29sZUljb24sIElGb3JtUmVuZGVyZXJSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgZmluZCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7XG4gIEpTT05FeHQsXG4gIEpTT05PYmplY3QsXG4gIFJlYWRvbmx5SlNPTlZhbHVlLFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBVVUlEXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERpc3Bvc2FibGVTZXQgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgRG9ja0xheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCBmb3JlaWduIGZyb20gJy4vZm9yZWlnbic7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIGNvbnNvbGUgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBhdXRvQ2xvc2luZ0JyYWNrZXRzID0gJ2NvbnNvbGU6dG9nZ2xlLWF1dG9jbG9zaW5nLWJyYWNrZXRzJztcblxuICBleHBvcnQgY29uc3QgY3JlYXRlID0gJ2NvbnNvbGU6Y3JlYXRlJztcblxuICBleHBvcnQgY29uc3QgY2xlYXIgPSAnY29uc29sZTpjbGVhcic7XG5cbiAgZXhwb3J0IGNvbnN0IHJ1blVuZm9yY2VkID0gJ2NvbnNvbGU6cnVuLXVuZm9yY2VkJztcblxuICBleHBvcnQgY29uc3QgcnVuRm9yY2VkID0gJ2NvbnNvbGU6cnVuLWZvcmNlZCc7XG5cbiAgZXhwb3J0IGNvbnN0IGxpbmVicmVhayA9ICdjb25zb2xlOmxpbmVicmVhayc7XG5cbiAgZXhwb3J0IGNvbnN0IGludGVycnVwdCA9ICdjb25zb2xlOmludGVycnVwdC1rZXJuZWwnO1xuXG4gIGV4cG9ydCBjb25zdCByZXN0YXJ0ID0gJ2NvbnNvbGU6cmVzdGFydC1rZXJuZWwnO1xuXG4gIGV4cG9ydCBjb25zdCBjbG9zZUFuZFNodXRkb3duID0gJ2NvbnNvbGU6Y2xvc2UtYW5kLXNodXRkb3duJztcblxuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdjb25zb2xlOm9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBpbmplY3QgPSAnY29uc29sZTppbmplY3QnO1xuXG4gIGV4cG9ydCBjb25zdCBjaGFuZ2VLZXJuZWwgPSAnY29uc29sZTpjaGFuZ2Uta2VybmVsJztcblxuICBleHBvcnQgY29uc3QgZ2V0S2VybmVsID0gJ2NvbnNvbGU6Z2V0LWtlcm5lbCc7XG5cbiAgZXhwb3J0IGNvbnN0IGVudGVyVG9FeGVjdXRlID0gJ2NvbnNvbGU6ZW50ZXItdG8tZXhlY3V0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNoaWZ0RW50ZXJUb0V4ZWN1dGUgPSAnY29uc29sZTpzaGlmdC1lbnRlci10by1leGVjdXRlJztcblxuICBleHBvcnQgY29uc3QgaW50ZXJhY3Rpb25Nb2RlID0gJ2NvbnNvbGU6aW50ZXJhY3Rpb24tbW9kZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlcGxhY2VTZWxlY3Rpb24gPSAnY29uc29sZTpyZXBsYWNlLXNlbGVjdGlvbic7XG5cbiAgZXhwb3J0IGNvbnN0IHNodXRkb3duID0gJ2NvbnNvbGU6c2h1dGRvd24nO1xuXG4gIGV4cG9ydCBjb25zdCBpbnZva2VDb21wbGV0ZXIgPSAnY29tcGxldGVyOmludm9rZS1jb25zb2xlJztcblxuICBleHBvcnQgY29uc3Qgc2VsZWN0Q29tcGxldGVyID0gJ2NvbXBsZXRlcjpzZWxlY3QtY29uc29sZSc7XG59XG5cbi8qKlxuICogVGhlIGNvbnNvbGUgd2lkZ2V0IHRyYWNrZXIgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHRyYWNrZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJQ29uc29sZVRyYWNrZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOnRyYWNrZXInLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBjb25zb2xlIHdpZGdldCB0cmFja2VyLicsXG4gIHByb3ZpZGVzOiBJQ29uc29sZVRyYWNrZXIsXG4gIHJlcXVpcmVzOiBbXG4gICAgQ29uc29sZVBhbmVsLklDb250ZW50RmFjdG9yeSxcbiAgICBJRWRpdG9yU2VydmljZXMsXG4gICAgSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5XG4gIF0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUxheW91dFJlc3RvcmVyLFxuICAgIElEZWZhdWx0RmlsZUJyb3dzZXIsXG4gICAgSU1haW5NZW51LFxuICAgIElDb21tYW5kUGFsZXR0ZSxcbiAgICBJTGF1bmNoZXIsXG4gICAgSUxhYlN0YXR1cyxcbiAgICBJU2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICAgIElGb3JtUmVuZGVyZXJSZWdpc3RyeSxcbiAgICBJVHJhbnNsYXRvclxuICBdLFxuICBhY3RpdmF0ZTogYWN0aXZhdGVDb25zb2xlLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogVGhlIGNvbnNvbGUgd2lkZ2V0IGNvbnRlbnQgZmFjdG9yeS5cbiAqL1xuY29uc3QgZmFjdG9yeTogSnVweXRlckZyb250RW5kUGx1Z2luPENvbnNvbGVQYW5lbC5JQ29udGVudEZhY3Rvcnk+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOmZhY3RvcnknLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBjb25zb2xlIHdpZGdldCBjb250ZW50IGZhY3RvcnkuJyxcbiAgcHJvdmlkZXM6IENvbnNvbGVQYW5lbC5JQ29udGVudEZhY3RvcnksXG4gIHJlcXVpcmVzOiBbSUVkaXRvclNlcnZpY2VzXSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kLCBlZGl0b3JTZXJ2aWNlczogSUVkaXRvclNlcnZpY2VzKSA9PiB7XG4gICAgY29uc3QgZWRpdG9yRmFjdG9yeSA9IGVkaXRvclNlcnZpY2VzLmZhY3RvcnlTZXJ2aWNlLm5ld0lubGluZUVkaXRvcjtcbiAgICByZXR1cm4gbmV3IENvbnNvbGVQYW5lbC5Db250ZW50RmFjdG9yeSh7IGVkaXRvckZhY3RvcnkgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogS2VybmVsIHN0YXR1cyBpbmRpY2F0b3IuXG4gKi9cbmNvbnN0IGtlcm5lbFN0YXR1czogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOmtlcm5lbC1zdGF0dXMnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgdGhlIGNvbnNvbGUgdG8gdGhlIGtlcm5lbCBzdGF0dXMgaW5kaWNhdG9yIG1vZGVsLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJQ29uc29sZVRyYWNrZXIsIElLZXJuZWxTdGF0dXNNb2RlbF0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgdHJhY2tlcjogSUNvbnNvbGVUcmFja2VyLFxuICAgIGtlcm5lbFN0YXR1czogSUtlcm5lbFN0YXR1c01vZGVsXG4gICkgPT4ge1xuICAgIGNvbnN0IHByb3ZpZGVyID0gKHdpZGdldDogV2lkZ2V0IHwgbnVsbCkgPT4ge1xuICAgICAgbGV0IHNlc3Npb246IElTZXNzaW9uQ29udGV4dCB8IG51bGwgPSBudWxsO1xuXG4gICAgICBpZiAod2lkZ2V0ICYmIHRyYWNrZXIuaGFzKHdpZGdldCkpIHtcbiAgICAgICAgcmV0dXJuICh3aWRnZXQgYXMgQ29uc29sZVBhbmVsKS5zZXNzaW9uQ29udGV4dDtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHNlc3Npb247XG4gICAgfTtcblxuICAgIGtlcm5lbFN0YXR1cy5hZGRTZXNzaW9uUHJvdmlkZXIocHJvdmlkZXIpO1xuICB9XG59O1xuXG4vKipcbiAqIEN1cnNvciBwb3NpdGlvbi5cbiAqL1xuY29uc3QgbGluZUNvbFN0YXR1czogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvbnNvbGUtZXh0ZW5zaW9uOmN1cnNvci1wb3NpdGlvbicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0aGUgY29uc29sZSB0byB0aGUgY29kZSBlZGl0b3IgY3Vyc29yIHBvc2l0aW9uIG1vZGVsLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJQ29uc29sZVRyYWNrZXIsIElQb3NpdGlvbk1vZGVsXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFja2VyOiBJQ29uc29sZVRyYWNrZXIsXG4gICAgcG9zaXRpb25Nb2RlbDogSVBvc2l0aW9uTW9kZWxcbiAgKSA9PiB7XG4gICAgbGV0IHByZXZpb3VzV2lkZ2V0OiBDb25zb2xlUGFuZWwgfCBudWxsID0gbnVsbDtcblxuICAgIGNvbnN0IHByb3ZpZGVyID0gYXN5bmMgKHdpZGdldDogV2lkZ2V0IHwgbnVsbCkgPT4ge1xuICAgICAgbGV0IGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbCA9IG51bGw7XG4gICAgICBpZiAod2lkZ2V0ICE9PSBwcmV2aW91c1dpZGdldCkge1xuICAgICAgICBwcmV2aW91c1dpZGdldD8uY29uc29sZS5wcm9tcHRDZWxsQ3JlYXRlZC5kaXNjb25uZWN0KFxuICAgICAgICAgIHBvc2l0aW9uTW9kZWwudXBkYXRlXG4gICAgICAgICk7XG5cbiAgICAgICAgcHJldmlvdXNXaWRnZXQgPSBudWxsO1xuICAgICAgICBpZiAod2lkZ2V0ICYmIHRyYWNrZXIuaGFzKHdpZGdldCkpIHtcbiAgICAgICAgICAod2lkZ2V0IGFzIENvbnNvbGVQYW5lbCkuY29uc29sZS5wcm9tcHRDZWxsQ3JlYXRlZC5jb25uZWN0KFxuICAgICAgICAgICAgcG9zaXRpb25Nb2RlbC51cGRhdGVcbiAgICAgICAgICApO1xuICAgICAgICAgIGNvbnN0IHByb21wdENlbGwgPSAod2lkZ2V0IGFzIENvbnNvbGVQYW5lbCkuY29uc29sZS5wcm9tcHRDZWxsO1xuICAgICAgICAgIGVkaXRvciA9IG51bGw7XG4gICAgICAgICAgaWYgKHByb21wdENlbGwpIHtcbiAgICAgICAgICAgIGF3YWl0IHByb21wdENlbGwucmVhZHk7XG4gICAgICAgICAgICBlZGl0b3IgPSBwcm9tcHRDZWxsLmVkaXRvcjtcbiAgICAgICAgICB9XG4gICAgICAgICAgcHJldmlvdXNXaWRnZXQgPSB3aWRnZXQgYXMgQ29uc29sZVBhbmVsO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKHdpZGdldCkge1xuICAgICAgICBjb25zdCBwcm9tcHRDZWxsID0gKHdpZGdldCBhcyBDb25zb2xlUGFuZWwpLmNvbnNvbGUucHJvbXB0Q2VsbDtcbiAgICAgICAgZWRpdG9yID0gbnVsbDtcbiAgICAgICAgaWYgKHByb21wdENlbGwpIHtcbiAgICAgICAgICBhd2FpdCBwcm9tcHRDZWxsLnJlYWR5O1xuICAgICAgICAgIGVkaXRvciA9IHByb21wdENlbGwuZWRpdG9yO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gZWRpdG9yO1xuICAgIH07XG5cbiAgICBwb3NpdGlvbk1vZGVsLmFkZEVkaXRvclByb3ZpZGVyKHByb3ZpZGVyKTtcbiAgfVxufTtcblxuY29uc3QgY29tcGxldGVyUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY29uc29sZS1leHRlbnNpb246Y29tcGxldGVyJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIGNvbXBsZXRpb24gdG8gdGhlIGNvbnNvbGUuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lDb25zb2xlVHJhY2tlcl0sXG4gIG9wdGlvbmFsOiBbSUNvbXBsZXRpb25Qcm92aWRlck1hbmFnZXIsIElUcmFuc2xhdG9yLCBJU2FuaXRpemVyXSxcbiAgYWN0aXZhdGU6IGFjdGl2YXRlQ29uc29sZUNvbXBsZXRlclNlcnZpY2Vcbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIHRoZSBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW1xuICBmYWN0b3J5LFxuICB0cmFja2VyLFxuICBmb3JlaWduLFxuICBrZXJuZWxTdGF0dXMsXG4gIGxpbmVDb2xTdGF0dXMsXG4gIGNvbXBsZXRlclBsdWdpblxuXTtcbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG5cbi8qKlxuICogQWN0aXZhdGUgdGhlIGNvbnNvbGUgZXh0ZW5zaW9uLlxuICovXG5hc3luYyBmdW5jdGlvbiBhY3RpdmF0ZUNvbnNvbGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBjb250ZW50RmFjdG9yeTogQ29uc29sZVBhbmVsLklDb250ZW50RmFjdG9yeSxcbiAgZWRpdG9yU2VydmljZXM6IElFZGl0b3JTZXJ2aWNlcyxcbiAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgZmlsZWJyb3dzZXI6IElEZWZhdWx0RmlsZUJyb3dzZXIgfCBudWxsLFxuICBtYWluTWVudTogSU1haW5NZW51IHwgbnVsbCxcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgbGF1bmNoZXI6IElMYXVuY2hlciB8IG51bGwsXG4gIHN0YXR1czogSUxhYlN0YXR1cyB8IG51bGwsXG4gIHNlc3Npb25EaWFsb2dzXzogSVNlc3Npb25Db250ZXh0RGlhbG9ncyB8IG51bGwsXG4gIGZvcm1SZWdpc3RyeTogSUZvcm1SZW5kZXJlclJlZ2lzdHJ5IHwgbnVsbCxcbiAgdHJhbnNsYXRvcl86IElUcmFuc2xhdG9yIHwgbnVsbFxuKTogUHJvbWlzZTxJQ29uc29sZVRyYWNrZXI+IHtcbiAgY29uc3QgdHJhbnNsYXRvciA9IHRyYW5zbGF0b3JfID8/IG51bGxUcmFuc2xhdG9yO1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBtYW5hZ2VyID0gYXBwLnNlcnZpY2VNYW5hZ2VyO1xuICBjb25zdCB7IGNvbW1hbmRzLCBzaGVsbCB9ID0gYXBwO1xuICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdDb25zb2xlJyk7XG4gIGNvbnN0IHNlc3Npb25EaWFsb2dzID1cbiAgICBzZXNzaW9uRGlhbG9nc18gPz8gbmV3IFNlc3Npb25Db250ZXh0RGlhbG9ncyh7IHRyYW5zbGF0b3IgfSk7XG5cbiAgLy8gQ3JlYXRlIGEgd2lkZ2V0IHRyYWNrZXIgZm9yIGFsbCBjb25zb2xlIHBhbmVscy5cbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPENvbnNvbGVQYW5lbD4oe1xuICAgIG5hbWVzcGFjZTogJ2NvbnNvbGUnXG4gIH0pO1xuXG4gIC8vIEhhbmRsZSBzdGF0ZSByZXN0b3JhdGlvbi5cbiAgaWYgKHJlc3RvcmVyKSB7XG4gICAgdm9pZCByZXN0b3Jlci5yZXN0b3JlKHRyYWNrZXIsIHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlLFxuICAgICAgYXJnczogd2lkZ2V0ID0+IHtcbiAgICAgICAgY29uc3QgeyBwYXRoLCBuYW1lLCBrZXJuZWxQcmVmZXJlbmNlIH0gPSB3aWRnZXQuY29uc29sZS5zZXNzaW9uQ29udGV4dDtcbiAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICBwYXRoLFxuICAgICAgICAgIG5hbWUsXG4gICAgICAgICAga2VybmVsUHJlZmVyZW5jZTogeyAuLi5rZXJuZWxQcmVmZXJlbmNlIH1cbiAgICAgICAgfTtcbiAgICAgIH0sXG4gICAgICBuYW1lOiB3aWRnZXQgPT4gd2lkZ2V0LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQucGF0aCA/PyBVVUlELnV1aWQ0KCksXG4gICAgICB3aGVuOiBtYW5hZ2VyLnJlYWR5XG4gICAgfSk7XG4gIH1cblxuICAvLyBBZGQgYSBsYXVuY2hlciBpdGVtIGlmIHRoZSBsYXVuY2hlciBpcyBhdmFpbGFibGUuXG4gIGlmIChsYXVuY2hlcikge1xuICAgIHZvaWQgbWFuYWdlci5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgIGxldCBkaXNwb3NhYmxlczogRGlzcG9zYWJsZVNldCB8IG51bGwgPSBudWxsO1xuICAgICAgY29uc3Qgb25TcGVjc0NoYW5nZWQgPSAoKSA9PiB7XG4gICAgICAgIGlmIChkaXNwb3NhYmxlcykge1xuICAgICAgICAgIGRpc3Bvc2FibGVzLmRpc3Bvc2UoKTtcbiAgICAgICAgICBkaXNwb3NhYmxlcyA9IG51bGw7XG4gICAgICAgIH1cbiAgICAgICAgY29uc3Qgc3BlY3MgPSBtYW5hZ2VyLmtlcm5lbHNwZWNzLnNwZWNzO1xuICAgICAgICBpZiAoIXNwZWNzKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGRpc3Bvc2FibGVzID0gbmV3IERpc3Bvc2FibGVTZXQoKTtcbiAgICAgICAgZm9yIChjb25zdCBuYW1lIGluIHNwZWNzLmtlcm5lbHNwZWNzKSB7XG4gICAgICAgICAgY29uc3QgcmFuayA9IG5hbWUgPT09IHNwZWNzLmRlZmF1bHQgPyAwIDogSW5maW5pdHk7XG4gICAgICAgICAgY29uc3Qgc3BlYyA9IHNwZWNzLmtlcm5lbHNwZWNzW25hbWVdITtcbiAgICAgICAgICBjb25zdCBrZXJuZWxJY29uVXJsID1cbiAgICAgICAgICAgIHNwZWMucmVzb3VyY2VzWydsb2dvLXN2ZyddIHx8IHNwZWMucmVzb3VyY2VzWydsb2dvLTY0eDY0J107XG4gICAgICAgICAgZGlzcG9zYWJsZXMuYWRkKFxuICAgICAgICAgICAgbGF1bmNoZXIuYWRkKHtcbiAgICAgICAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5jcmVhdGUsXG4gICAgICAgICAgICAgIGFyZ3M6IHsgaXNMYXVuY2hlcjogdHJ1ZSwga2VybmVsUHJlZmVyZW5jZTogeyBuYW1lIH0gfSxcbiAgICAgICAgICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdDb25zb2xlJyksXG4gICAgICAgICAgICAgIHJhbmssXG4gICAgICAgICAgICAgIGtlcm5lbEljb25VcmwsXG4gICAgICAgICAgICAgIG1ldGFkYXRhOiB7XG4gICAgICAgICAgICAgICAga2VybmVsOiBKU09ORXh0LmRlZXBDb3B5KFxuICAgICAgICAgICAgICAgICAgc3BlYy5tZXRhZGF0YSB8fCB7fVxuICAgICAgICAgICAgICAgICkgYXMgUmVhZG9ubHlKU09OVmFsdWVcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSlcbiAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICB9O1xuICAgICAgb25TcGVjc0NoYW5nZWQoKTtcbiAgICAgIG1hbmFnZXIua2VybmVsc3BlY3Muc3BlY3NDaGFuZ2VkLmNvbm5lY3Qob25TcGVjc0NoYW5nZWQpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGEgd2lkZ2V0LlxuICAgKi9cbiAgaW50ZXJmYWNlIElDcmVhdGVPcHRpb25zIGV4dGVuZHMgUGFydGlhbDxDb25zb2xlUGFuZWwuSU9wdGlvbnM+IHtcbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGFjdGl2YXRlIHRoZSB3aWRnZXQuICBEZWZhdWx0cyB0byBgdHJ1ZWAuXG4gICAgICovXG4gICAgYWN0aXZhdGU/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlZmVyZW5jZSB3aWRnZXQgaWQgZm9yIHRoZSBpbnNlcnQgbG9jYXRpb24uXG4gICAgICpcbiAgICAgKiBUaGUgZGVmYXVsdCBpcyBgbnVsbGAuXG4gICAgICovXG4gICAgcmVmPzogc3RyaW5nIHwgbnVsbDtcblxuICAgIC8qKlxuICAgICAqIFRoZSB0YWIgaW5zZXJ0IG1vZGUuXG4gICAgICpcbiAgICAgKiBBbiBpbnNlcnQgbW9kZSBpcyB1c2VkIHRvIHNwZWNpZnkgaG93IGEgd2lkZ2V0IHNob3VsZCBiZSBhZGRlZFxuICAgICAqIHRvIHRoZSBtYWluIGFyZWEgcmVsYXRpdmUgdG8gYSByZWZlcmVuY2Ugd2lkZ2V0LlxuICAgICAqL1xuICAgIGluc2VydE1vZGU/OiBEb2NrTGF5b3V0Lkluc2VydE1vZGU7XG5cbiAgICAvKipcbiAgICAgKiBUeXBlIG9mIHdpZGdldCB0byBvcGVuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyBpcyB0aGUga2V5IHVzZWQgdG8gbG9hZCB1c2VyIGxheW91dCBjdXN0b21pemF0aW9uLlxuICAgICAqIEl0cyB0eXBpY2FsIHZhbHVlIGlzOiBhIGZhY3RvcnkgbmFtZSBvciB0aGUgd2lkZ2V0IGlkIChpZiBzaW5nbGV0b24pXG4gICAgICovXG4gICAgdHlwZT86IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBjb25zb2xlIGZvciBhIGdpdmVuIHBhdGguXG4gICAqL1xuICBhc3luYyBmdW5jdGlvbiBjcmVhdGVDb25zb2xlKG9wdGlvbnM6IElDcmVhdGVPcHRpb25zKTogUHJvbWlzZTxDb25zb2xlUGFuZWw+IHtcbiAgICBhd2FpdCBtYW5hZ2VyLnJlYWR5O1xuXG4gICAgY29uc3QgcGFuZWwgPSBuZXcgQ29uc29sZVBhbmVsKHtcbiAgICAgIG1hbmFnZXIsXG4gICAgICBjb250ZW50RmFjdG9yeSxcbiAgICAgIG1pbWVUeXBlU2VydmljZTogZWRpdG9yU2VydmljZXMubWltZVR5cGVTZXJ2aWNlLFxuICAgICAgcmVuZGVybWltZSxcbiAgICAgIHNlc3Npb25EaWFsb2dzLFxuICAgICAgdHJhbnNsYXRvcixcbiAgICAgIHNldEJ1c3k6IChzdGF0dXMgJiYgKCgpID0+IHN0YXR1cy5zZXRCdXN5KCkpKSA/PyB1bmRlZmluZWQsXG4gICAgICAuLi4ob3B0aW9ucyBhcyBQYXJ0aWFsPENvbnNvbGVQYW5lbC5JT3B0aW9ucz4pXG4gICAgfSk7XG5cbiAgICBjb25zdCBpbnRlcmFjdGlvbk1vZGU6IHN0cmluZyA9IChcbiAgICAgIGF3YWl0IHNldHRpbmdSZWdpc3RyeS5nZXQoXG4gICAgICAgICdAanVweXRlcmxhYi9jb25zb2xlLWV4dGVuc2lvbjp0cmFja2VyJyxcbiAgICAgICAgJ2ludGVyYWN0aW9uTW9kZSdcbiAgICAgIClcbiAgICApLmNvbXBvc2l0ZSBhcyBzdHJpbmc7XG4gICAgcGFuZWwuY29uc29sZS5ub2RlLmRhdGFzZXQuanBJbnRlcmFjdGlvbk1vZGUgPSBpbnRlcmFjdGlvbk1vZGU7XG5cbiAgICAvLyBBZGQgdGhlIGNvbnNvbGUgcGFuZWwgdG8gdGhlIHRyYWNrZXIuIFdlIHdhbnQgdGhlIHBhbmVsIHRvIHNob3cgdXAgYmVmb3JlXG4gICAgLy8gYW55IGtlcm5lbCBzZWxlY3Rpb24gZGlhbG9nLCBzbyB3ZSBkbyBub3QgYXdhaXQgcGFuZWwuc2Vzc2lvbi5yZWFkeTtcbiAgICBhd2FpdCB0cmFja2VyLmFkZChwYW5lbCk7XG4gICAgcGFuZWwuc2Vzc2lvbkNvbnRleHQucHJvcGVydHlDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgdm9pZCB0cmFja2VyLnNhdmUocGFuZWwpO1xuICAgIH0pO1xuXG4gICAgc2hlbGwuYWRkKHBhbmVsLCAnbWFpbicsIHtcbiAgICAgIHJlZjogb3B0aW9ucy5yZWYsXG4gICAgICBtb2RlOiBvcHRpb25zLmluc2VydE1vZGUsXG4gICAgICBhY3RpdmF0ZTogb3B0aW9ucy5hY3RpdmF0ZSAhPT0gZmFsc2UsXG4gICAgICB0eXBlOiBvcHRpb25zLnR5cGUgPz8gJ0NvbnNvbGUnXG4gICAgfSk7XG4gICAgcmV0dXJuIHBhbmVsO1xuICB9XG5cbiAgY29uc3QgcGx1Z2luSWQgPSAnQGp1cHl0ZXJsYWIvY29uc29sZS1leHRlbnNpb246dHJhY2tlcic7XG4gIGxldCBpbnRlcmFjdGlvbk1vZGU6IHN0cmluZztcbiAgbGV0IHByb21wdENlbGxDb25maWc6IEpTT05PYmplY3QgPSB7fTtcblxuICAvKipcbiAgICogVXBkYXRlIHNldHRpbmdzIGZvciBvbmUgY29uc29sZSBvciBhbGwgY29uc29sZXMuXG4gICAqXG4gICAqIEBwYXJhbSBwYW5lbCBPcHRpb25hbCAtIHNpbmdsZSBjb25zb2xlIHRvIHVwZGF0ZS5cbiAgICovXG4gIGFzeW5jIGZ1bmN0aW9uIHVwZGF0ZVNldHRpbmdzKHBhbmVsPzogQ29uc29sZVBhbmVsKSB7XG4gICAgaW50ZXJhY3Rpb25Nb2RlID0gKGF3YWl0IHNldHRpbmdSZWdpc3RyeS5nZXQocGx1Z2luSWQsICdpbnRlcmFjdGlvbk1vZGUnKSlcbiAgICAgIC5jb21wb3NpdGUgYXMgc3RyaW5nO1xuICAgIHByb21wdENlbGxDb25maWcgPSAoYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LmdldChwbHVnaW5JZCwgJ3Byb21wdENlbGxDb25maWcnKSlcbiAgICAgIC5jb21wb3NpdGUgYXMgSlNPTk9iamVjdDtcblxuICAgIGNvbnN0IHNldFdpZGdldE9wdGlvbnMgPSAod2lkZ2V0OiBDb25zb2xlUGFuZWwpID0+IHtcbiAgICAgIHdpZGdldC5jb25zb2xlLm5vZGUuZGF0YXNldC5qcEludGVyYWN0aW9uTW9kZSA9IGludGVyYWN0aW9uTW9kZTtcbiAgICAgIC8vIFVwZGF0ZSBmdXR1cmUgcHJvbXB0Q2VsbHNcbiAgICAgIHdpZGdldC5jb25zb2xlLmVkaXRvckNvbmZpZyA9IHByb21wdENlbGxDb25maWc7XG4gICAgICAvLyBVcGRhdGUgcHJvbXB0Q2VsbCBhbHJlYWR5IG9uIHNjcmVlblxuICAgICAgd2lkZ2V0LmNvbnNvbGUucHJvbXB0Q2VsbD8uZWRpdG9yPy5zZXRPcHRpb25zKHByb21wdENlbGxDb25maWcpO1xuICAgIH07XG5cbiAgICBpZiAocGFuZWwpIHtcbiAgICAgIHNldFdpZGdldE9wdGlvbnMocGFuZWwpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0cmFja2VyLmZvckVhY2goc2V0V2lkZ2V0T3B0aW9ucyk7XG4gICAgfVxuICB9XG5cbiAgc2V0dGluZ1JlZ2lzdHJ5LnBsdWdpbkNoYW5nZWQuY29ubmVjdCgoc2VuZGVyLCBwbHVnaW4pID0+IHtcbiAgICBpZiAocGx1Z2luID09PSBwbHVnaW5JZCkge1xuICAgICAgdm9pZCB1cGRhdGVTZXR0aW5ncygpO1xuICAgIH1cbiAgfSk7XG4gIGF3YWl0IHVwZGF0ZVNldHRpbmdzKCk7XG5cbiAgaWYgKGZvcm1SZWdpc3RyeSkge1xuICAgIGNvbnN0IENNUmVuZGVyZXIgPSBmb3JtUmVnaXN0cnkuZ2V0UmVuZGVyZXIoXG4gICAgICAnQGp1cHl0ZXJsYWIvY29kZW1pcnJvci1leHRlbnNpb246cGx1Z2luLmRlZmF1bHRDb25maWcnXG4gICAgKTtcbiAgICBpZiAoQ01SZW5kZXJlcikge1xuICAgICAgZm9ybVJlZ2lzdHJ5LmFkZFJlbmRlcmVyKFxuICAgICAgICAnQGp1cHl0ZXJsYWIvY29uc29sZS1leHRlbnNpb246dHJhY2tlci5wcm9tcHRDZWxsQ29uZmlnJyxcbiAgICAgICAgQ01SZW5kZXJlclxuICAgICAgKTtcbiAgICB9XG4gIH1cblxuICAvLyBBcHBseSBzZXR0aW5ncyB3aGVuIGEgY29uc29sZSBpcyBjcmVhdGVkLlxuICB0cmFja2VyLndpZGdldEFkZGVkLmNvbm5lY3QoKHNlbmRlciwgcGFuZWwpID0+IHtcbiAgICB2b2lkIHVwZGF0ZVNldHRpbmdzKHBhbmVsKTtcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmF1dG9DbG9zaW5nQnJhY2tldHMsIHtcbiAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgIHByb21wdENlbGxDb25maWcuYXV0b0Nsb3NpbmdCcmFja2V0cyA9ICEhKFxuICAgICAgICBhcmdzWydmb3JjZSddID8/ICFwcm9tcHRDZWxsQ29uZmlnLmF1dG9DbG9zaW5nQnJhY2tldHNcbiAgICAgICk7XG4gICAgICBhd2FpdCBzZXR0aW5nUmVnaXN0cnkuc2V0KHBsdWdpbklkLCAncHJvbXB0Q2VsbENvbmZpZycsIHByb21wdENlbGxDb25maWcpO1xuICAgIH0sXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdBdXRvIENsb3NlIEJyYWNrZXRzIGZvciBDb2RlIENvbnNvbGUgUHJvbXB0JyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBwcm9tcHRDZWxsQ29uZmlnLmF1dG9DbG9zaW5nQnJhY2tldHMgYXMgYm9vbGVhblxuICB9KTtcblxuICAvKipcbiAgICogV2hldGhlciB0aGVyZSBpcyBhbiBhY3RpdmUgY29uc29sZS5cbiAgICovXG4gIGZ1bmN0aW9uIGlzRW5hYmxlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gKFxuICAgICAgdHJhY2tlci5jdXJyZW50V2lkZ2V0ICE9PSBudWxsICYmXG4gICAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgPT09IHNoZWxsLmN1cnJlbnRXaWRnZXRcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gb3BlbiBhIGNvbnNvbGUuXG4gICAqL1xuICBpbnRlcmZhY2UgSU9wZW5PcHRpb25zIGV4dGVuZHMgUGFydGlhbDxDb25zb2xlUGFuZWwuSU9wdGlvbnM+IHtcbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGFjdGl2YXRlIHRoZSBjb25zb2xlLiAgRGVmYXVsdHMgdG8gYHRydWVgLlxuICAgICAqL1xuICAgIGFjdGl2YXRlPzogYm9vbGVhbjtcbiAgfVxuXG4gIGxldCBjb21tYW5kID0gQ29tbWFuZElEcy5vcGVuO1xuICBjb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmQsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gYSBjb25zb2xlIGZvciB0aGUgcHJvdmlkZWQgYHBhdGhgLicpLFxuICAgIGV4ZWN1dGU6IChhcmdzOiBJT3Blbk9wdGlvbnMpID0+IHtcbiAgICAgIGNvbnN0IHBhdGggPSBhcmdzWydwYXRoJ107XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmZpbmQodmFsdWUgPT4ge1xuICAgICAgICByZXR1cm4gdmFsdWUuY29uc29sZS5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5wYXRoID09PSBwYXRoO1xuICAgICAgfSk7XG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIGlmIChhcmdzLmFjdGl2YXRlICE9PSBmYWxzZSkge1xuICAgICAgICAgIHNoZWxsLmFjdGl2YXRlQnlJZCh3aWRnZXQuaWQpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB3aWRnZXQ7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICByZXR1cm4gbWFuYWdlci5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgICAgICBjb25zdCBtb2RlbCA9IGZpbmQobWFuYWdlci5zZXNzaW9ucy5ydW5uaW5nKCksIGl0ZW0gPT4ge1xuICAgICAgICAgICAgcmV0dXJuIGl0ZW0ucGF0aCA9PT0gcGF0aDtcbiAgICAgICAgICB9KTtcbiAgICAgICAgICBpZiAobW9kZWwpIHtcbiAgICAgICAgICAgIHJldHVybiBjcmVhdGVDb25zb2xlKGFyZ3MpO1xuICAgICAgICAgIH1cbiAgICAgICAgICByZXR1cm4gUHJvbWlzZS5yZWplY3QoYE5vIHJ1bm5pbmcga2VybmVsIHNlc3Npb24gZm9yIHBhdGg6ICR7cGF0aH1gKTtcbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kID0gQ29tbWFuZElEcy5jcmVhdGU7XG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoY29tbWFuZCwge1xuICAgIGxhYmVsOiBhcmdzID0+IHtcbiAgICAgIGlmIChhcmdzWydpc1BhbGV0dGUnXSkge1xuICAgICAgICByZXR1cm4gdHJhbnMuX18oJ05ldyBDb25zb2xlJyk7XG4gICAgICB9IGVsc2UgaWYgKGFyZ3NbJ2lzTGF1bmNoZXInXSAmJiBhcmdzWydrZXJuZWxQcmVmZXJlbmNlJ10pIHtcbiAgICAgICAgY29uc3Qga2VybmVsUHJlZmVyZW5jZSA9IGFyZ3NbXG4gICAgICAgICAgJ2tlcm5lbFByZWZlcmVuY2UnXG4gICAgICAgIF0gYXMgSVNlc3Npb25Db250ZXh0LklLZXJuZWxQcmVmZXJlbmNlO1xuICAgICAgICAvLyBUT0RPOiBMdW1pbm8gY29tbWFuZCBmdW5jdGlvbnMgc2hvdWxkIHByb2JhYmx5IGJlIGFsbG93ZWQgdG8gcmV0dXJuIHVuZGVmaW5lZD9cbiAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICBtYW5hZ2VyLmtlcm5lbHNwZWNzPy5zcGVjcz8ua2VybmVsc3BlY3Nba2VybmVsUHJlZmVyZW5jZS5uYW1lIHx8ICcnXVxuICAgICAgICAgICAgPy5kaXNwbGF5X25hbWUgPz8gJydcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiB0cmFucy5fXygnQ29uc29sZScpO1xuICAgIH0sXG4gICAgaWNvbjogYXJncyA9PiAoYXJnc1snaXNQYWxldHRlJ10gPyB1bmRlZmluZWQgOiBjb25zb2xlSWNvbiksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBiYXNlUGF0aCA9XG4gICAgICAgICgoYXJnc1snYmFzZVBhdGgnXSBhcyBzdHJpbmcpIHx8XG4gICAgICAgICAgKGFyZ3NbJ2N3ZCddIGFzIHN0cmluZykgfHxcbiAgICAgICAgICBmaWxlYnJvd3Nlcj8ubW9kZWwucGF0aCkgPz9cbiAgICAgICAgJyc7XG4gICAgICByZXR1cm4gY3JlYXRlQ29uc29sZSh7IGJhc2VQYXRoLCAuLi5hcmdzIH0pO1xuICAgIH1cbiAgfSk7XG5cbiAgLy8gR2V0IHRoZSBjdXJyZW50IHdpZGdldCBhbmQgYWN0aXZhdGUgdW5sZXNzIHRoZSBhcmdzIHNwZWNpZnkgb3RoZXJ3aXNlLlxuICBmdW5jdGlvbiBnZXRDdXJyZW50KGFyZ3M6IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QpOiBDb25zb2xlUGFuZWwgfCBudWxsIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgY29uc3QgYWN0aXZhdGUgPSBhcmdzWydhY3RpdmF0ZSddICE9PSBmYWxzZTtcbiAgICBpZiAoYWN0aXZhdGUgJiYgd2lkZ2V0KSB7XG4gICAgICBzaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICB9XG4gICAgcmV0dXJuIHdpZGdldCA/PyBudWxsO1xuICB9XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNsZWFyLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdDbGVhciBDb25zb2xlIENlbGxzJyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50ID0gZ2V0Q3VycmVudChhcmdzKTtcbiAgICAgIGlmICghY3VycmVudCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjdXJyZW50LmNvbnNvbGUuY2xlYXIoKTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucnVuVW5mb3JjZWQsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1J1biBDZWxsICh1bmZvcmNlZCknKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBjdXJyZW50LmNvbnNvbGUuZXhlY3V0ZSgpO1xuICAgIH0sXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5ydW5Gb3JjZWQsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1J1biBDZWxsIChmb3JjZWQpJyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBjdXJyZW50ID0gZ2V0Q3VycmVudChhcmdzKTtcbiAgICAgIGlmICghY3VycmVudCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICByZXR1cm4gY3VycmVudC5jb25zb2xlLmV4ZWN1dGUodHJ1ZSk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxpbmVicmVhaywge1xuICAgIGxhYmVsOiB0cmFucy5fXygnSW5zZXJ0IExpbmUgQnJlYWsnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGN1cnJlbnQuY29uc29sZS5pbnNlcnRMaW5lYnJlYWsoKTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVwbGFjZVNlbGVjdGlvbiwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnUmVwbGFjZSBTZWxlY3Rpb24gaW4gQ29uc29sZScpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IGdldEN1cnJlbnQoYXJncyk7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgdGV4dDogc3RyaW5nID0gKGFyZ3NbJ3RleHQnXSBhcyBzdHJpbmcpIHx8ICcnO1xuICAgICAgY3VycmVudC5jb25zb2xlLnJlcGxhY2VTZWxlY3Rpb24odGV4dCk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmludGVycnVwdCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnSW50ZXJydXB0IEtlcm5lbCcpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IGdldEN1cnJlbnQoYXJncyk7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3Qga2VybmVsID0gY3VycmVudC5jb25zb2xlLnNlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbDtcbiAgICAgIGlmIChrZXJuZWwpIHtcbiAgICAgICAgcmV0dXJuIGtlcm5lbC5pbnRlcnJ1cHQoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVzdGFydCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnUmVzdGFydCBLZXJuZWzigKYnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBzZXNzaW9uRGlhbG9ncy5yZXN0YXJ0KGN1cnJlbnQuY29uc29sZS5zZXNzaW9uQ29udGV4dCk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNodXRkb3duLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTaHV0IERvd24nKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIGN1cnJlbnQuY29uc29sZS5zZXNzaW9uQ29udGV4dC5zaHV0ZG93bigpO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNsb3NlQW5kU2h1dGRvd24sIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0Nsb3NlIGFuZCBTaHV0IERvd27igKYnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KGFyZ3MpO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdTaHV0IGRvd24gdGhlIGNvbnNvbGU/JyksXG4gICAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAgICdBcmUgeW91IHN1cmUgeW91IHdhbnQgdG8gY2xvc2UgXCIlMVwiPycsXG4gICAgICAgICAgY3VycmVudC50aXRsZS5sYWJlbFxuICAgICAgICApLFxuICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbih7XG4gICAgICAgICAgICBhcmlhTGFiZWw6IHRyYW5zLl9fKCdDYW5jZWwgY29uc29sZSBTaHV0IERvd24nKVxuICAgICAgICAgIH0pLFxuICAgICAgICAgIERpYWxvZy53YXJuQnV0dG9uKHtcbiAgICAgICAgICAgIGFyaWFMYWJlbDogdHJhbnMuX18oJ0NvbmZpcm0gY29uc29sZSBTaHV0IERvd24nKVxuICAgICAgICAgIH0pXG4gICAgICAgIF1cbiAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgICAgcmV0dXJuIGNvbW1hbmRzXG4gICAgICAgICAgICAuZXhlY3V0ZShDb21tYW5kSURzLnNodXRkb3duLCB7IGFjdGl2YXRlOiBmYWxzZSB9KVxuICAgICAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICBjdXJyZW50LmRpc3Bvc2UoKTtcbiAgICAgICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH0sXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5pbmplY3QsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0luamVjdCBzb21lIGNvZGUgaW4gYSBjb25zb2xlLicpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgcGF0aCA9IGFyZ3NbJ3BhdGgnXTtcbiAgICAgIHRyYWNrZXIuZmluZCh3aWRnZXQgPT4ge1xuICAgICAgICBpZiAod2lkZ2V0LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbj8ucGF0aCA9PT0gcGF0aCkge1xuICAgICAgICAgIGlmIChhcmdzWydhY3RpdmF0ZSddICE9PSBmYWxzZSkge1xuICAgICAgICAgICAgc2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHZvaWQgd2lkZ2V0LmNvbnNvbGUuaW5qZWN0KFxuICAgICAgICAgICAgYXJnc1snY29kZSddIGFzIHN0cmluZyxcbiAgICAgICAgICAgIGFyZ3NbJ21ldGFkYXRhJ10gYXMgSlNPTk9iamVjdFxuICAgICAgICAgICk7XG4gICAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfSk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNoYW5nZUtlcm5lbCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnQ2hhbmdlIEtlcm5lbOKApicpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgY3VycmVudCA9IGdldEN1cnJlbnQoYXJncyk7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHNlc3Npb25EaWFsb2dzLnNlbGVjdEtlcm5lbChjdXJyZW50LmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQpO1xuICAgIH0sXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5nZXRLZXJuZWwsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0dldCBLZXJuZWwnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSBnZXRDdXJyZW50KHsgYWN0aXZhdGU6IGZhbHNlLCAuLi5hcmdzIH0pO1xuICAgICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBjdXJyZW50LnNlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbDtcbiAgICB9LFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBpZiAocGFsZXR0ZSkge1xuICAgIC8vIEFkZCBjb21tYW5kIHBhbGV0dGUgaXRlbXNcbiAgICBbXG4gICAgICBDb21tYW5kSURzLmNyZWF0ZSxcbiAgICAgIENvbW1hbmRJRHMubGluZWJyZWFrLFxuICAgICAgQ29tbWFuZElEcy5jbGVhcixcbiAgICAgIENvbW1hbmRJRHMucnVuVW5mb3JjZWQsXG4gICAgICBDb21tYW5kSURzLnJ1bkZvcmNlZCxcbiAgICAgIENvbW1hbmRJRHMucmVzdGFydCxcbiAgICAgIENvbW1hbmRJRHMuaW50ZXJydXB0LFxuICAgICAgQ29tbWFuZElEcy5jaGFuZ2VLZXJuZWwsXG4gICAgICBDb21tYW5kSURzLmNsb3NlQW5kU2h1dGRvd25cbiAgICBdLmZvckVhY2goY29tbWFuZCA9PiB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSwgYXJnczogeyBpc1BhbGV0dGU6IHRydWUgfSB9KTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChtYWluTWVudSkge1xuICAgIC8vIEFkZCBhIGNsb3NlIGFuZCBzaHV0ZG93biBjb21tYW5kIHRvIHRoZSBmaWxlIG1lbnUuXG4gICAgbWFpbk1lbnUuZmlsZU1lbnUuY2xvc2VBbmRDbGVhbmVycy5hZGQoe1xuICAgICAgaWQ6IENvbW1hbmRJRHMuY2xvc2VBbmRTaHV0ZG93bixcbiAgICAgIGlzRW5hYmxlZFxuICAgIH0pO1xuXG4gICAgLy8gQWRkIGEga2VybmVsIHVzZXIgdG8gdGhlIEtlcm5lbCBtZW51XG4gICAgbWFpbk1lbnUua2VybmVsTWVudS5rZXJuZWxVc2Vycy5jaGFuZ2VLZXJuZWwuYWRkKHtcbiAgICAgIGlkOiBDb21tYW5kSURzLmNoYW5nZUtlcm5lbCxcbiAgICAgIGlzRW5hYmxlZFxuICAgIH0pO1xuICAgIG1haW5NZW51Lmtlcm5lbE1lbnUua2VybmVsVXNlcnMuY2xlYXJXaWRnZXQuYWRkKHtcbiAgICAgIGlkOiBDb21tYW5kSURzLmNsZWFyLFxuICAgICAgaXNFbmFibGVkXG4gICAgfSk7XG4gICAgbWFpbk1lbnUua2VybmVsTWVudS5rZXJuZWxVc2Vycy5pbnRlcnJ1cHRLZXJuZWwuYWRkKHtcbiAgICAgIGlkOiBDb21tYW5kSURzLmludGVycnVwdCxcbiAgICAgIGlzRW5hYmxlZFxuICAgIH0pO1xuICAgIG1haW5NZW51Lmtlcm5lbE1lbnUua2VybmVsVXNlcnMucmVzdGFydEtlcm5lbC5hZGQoe1xuICAgICAgaWQ6IENvbW1hbmRJRHMucmVzdGFydCxcbiAgICAgIGlzRW5hYmxlZFxuICAgIH0pO1xuICAgIG1haW5NZW51Lmtlcm5lbE1lbnUua2VybmVsVXNlcnMuc2h1dGRvd25LZXJuZWwuYWRkKHtcbiAgICAgIGlkOiBDb21tYW5kSURzLnNodXRkb3duLFxuICAgICAgaXNFbmFibGVkXG4gICAgfSk7XG5cbiAgICAvLyBBZGQgYSBjb2RlIHJ1bm5lciB0byB0aGUgUnVuIG1lbnUuXG4gICAgbWFpbk1lbnUucnVuTWVudS5jb2RlUnVubmVycy5ydW4uYWRkKHtcbiAgICAgIGlkOiBDb21tYW5kSURzLnJ1bkZvcmNlZCxcbiAgICAgIGlzRW5hYmxlZFxuICAgIH0pO1xuXG4gICAgLy8gQWRkIGEgY2xlYXJlciB0byB0aGUgZWRpdCBtZW51XG4gICAgbWFpbk1lbnUuZWRpdE1lbnUuY2xlYXJlcnMuY2xlYXJDdXJyZW50LmFkZCh7XG4gICAgICBpZDogQ29tbWFuZElEcy5jbGVhcixcbiAgICAgIGlzRW5hYmxlZFxuICAgIH0pO1xuXG4gICAgLy8gQWRkIGtlcm5lbCBpbmZvcm1hdGlvbiB0byB0aGUgYXBwbGljYXRpb24gaGVscCBtZW51LlxuICAgIG1haW5NZW51LmhlbHBNZW51LmdldEtlcm5lbC5hZGQoe1xuICAgICAgaWQ6IENvbW1hbmRJRHMuZ2V0S2VybmVsLFxuICAgICAgaXNFbmFibGVkXG4gICAgfSk7XG4gIH1cblxuICAvLyBGb3IgYmFja3dhcmRzIGNvbXBhdGliaWxpdHkgYW5kIGNsYXJpdHksIHdlIGV4cGxpY2l0bHkgbGFiZWwgdGhlIHJ1blxuICAvLyBrZXlzdHJva2Ugd2l0aCB0aGUgYWN0dWFsIGVmZmVjdGVkIGNoYW5nZSwgcmF0aGVyIHRoYW4gdGhlIGdlbmVyaWNcbiAgLy8gXCJub3RlYm9va1wiIG9yIFwidGVybWluYWxcIiBpbnRlcmFjdGlvbiBtb2RlLiBXaGVuIHRoaXMgaW50ZXJhY3Rpb24gbW9kZVxuICAvLyBhZmZlY3RzIG1vcmUgdGhhbiBqdXN0IHRoZSBydW4ga2V5c3Ryb2tlLCB3ZSBjYW4gbWFrZSB0aGlzIG1lbnUgdGl0bGUgbW9yZVxuICAvLyBnZW5lcmljLlxuICBjb25zdCBydW5TaG9ydGN1dFRpdGxlczogeyBbaW5kZXg6IHN0cmluZ106IHN0cmluZyB9ID0ge1xuICAgIG5vdGVib29rOiB0cmFucy5fXygnRXhlY3V0ZSB3aXRoIFNoaWZ0K0VudGVyJyksXG4gICAgdGVybWluYWw6IHRyYW5zLl9fKCdFeGVjdXRlIHdpdGggRW50ZXInKVxuICB9O1xuXG4gIC8vIEFkZCB0aGUgZXhlY3V0ZSBrZXlzdHJva2Ugc2V0dGluZyBzdWJtZW51LlxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW50ZXJhY3Rpb25Nb2RlLCB7XG4gICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgIHJ1blNob3J0Y3V0VGl0bGVzW2FyZ3NbJ2ludGVyYWN0aW9uTW9kZSddIGFzIHN0cmluZ10gPz9cbiAgICAgICdTZXQgdGhlIGNvbnNvbGUgaW50ZXJhY3Rpb24gbW9kZS4nLFxuICAgIGV4ZWN1dGU6IGFzeW5jIGFyZ3MgPT4ge1xuICAgICAgY29uc3Qga2V5ID0gJ2tleU1hcCc7XG4gICAgICB0cnkge1xuICAgICAgICBhd2FpdCBzZXR0aW5nUmVnaXN0cnkuc2V0KFxuICAgICAgICAgIHBsdWdpbklkLFxuICAgICAgICAgICdpbnRlcmFjdGlvbk1vZGUnLFxuICAgICAgICAgIGFyZ3NbJ2ludGVyYWN0aW9uTW9kZSddIGFzIHN0cmluZ1xuICAgICAgICApO1xuICAgICAgfSBjYXRjaCAocmVhc29uKSB7XG4gICAgICAgIGNvbnNvbGUuZXJyb3IoYEZhaWxlZCB0byBzZXQgJHtwbHVnaW5JZH06JHtrZXl9IC0gJHtyZWFzb24ubWVzc2FnZX1gKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGlzVG9nZ2xlZDogYXJncyA9PiBhcmdzWydpbnRlcmFjdGlvbk1vZGUnXSA9PT0gaW50ZXJhY3Rpb25Nb2RlXG4gIH0pO1xuXG4gIHJldHVybiB0cmFja2VyO1xufVxuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBjb21wbGV0ZXIgc2VydmljZSBmb3IgY29uc29sZS5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGVDb25zb2xlQ29tcGxldGVyU2VydmljZShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIGNvbnNvbGVzOiBJQ29uc29sZVRyYWNrZXIsXG4gIG1hbmFnZXI6IElDb21wbGV0aW9uUHJvdmlkZXJNYW5hZ2VyIHwgbnVsbCxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IgfCBudWxsLFxuICBhcHBTYW5pdGl6ZXI6IElSZW5kZXJNaW1lLklTYW5pdGl6ZXIgfCBudWxsXG4pOiB2b2lkIHtcbiAgaWYgKCFtYW5hZ2VyKSB7XG4gICAgcmV0dXJuO1xuICB9XG5cbiAgY29uc3QgdHJhbnMgPSAodHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvcikubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBzYW5pdGl6ZXIgPSBhcHBTYW5pdGl6ZXIgPz8gbmV3IFNhbml0aXplcigpO1xuXG4gIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaW52b2tlQ29tcGxldGVyLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdEaXNwbGF5IHRoZSBjb21wbGV0aW9uIGhlbHBlci4nKSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCBpZCA9IGNvbnNvbGVzLmN1cnJlbnRXaWRnZXQgJiYgY29uc29sZXMuY3VycmVudFdpZGdldC5pZDtcblxuICAgICAgaWYgKGlkKSB7XG4gICAgICAgIHJldHVybiBtYW5hZ2VyLmludm9rZShpZCk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNlbGVjdENvbXBsZXRlciwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2VsZWN0IHRoZSBjb21wbGV0aW9uIHN1Z2dlc3Rpb24uJyksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3QgaWQgPSBjb25zb2xlcy5jdXJyZW50V2lkZ2V0ICYmIGNvbnNvbGVzLmN1cnJlbnRXaWRnZXQuaWQ7XG5cbiAgICAgIGlmIChpZCkge1xuICAgICAgICByZXR1cm4gbWFuYWdlci5zZWxlY3QoaWQpO1xuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgYXBwLmNvbW1hbmRzLmFkZEtleUJpbmRpbmcoe1xuICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2VsZWN0Q29tcGxldGVyLFxuICAgIGtleXM6IFsnRW50ZXInXSxcbiAgICBzZWxlY3RvcjogJy5qcC1Db25zb2xlUGFuZWwgLmpwLW1vZC1jb21wbGV0ZXItYWN0aXZlJ1xuICB9KTtcbiAgY29uc3QgdXBkYXRlQ29tcGxldGVyID0gYXN5bmMgKF86IGFueSwgY29uc29sZVBhbmVsOiBDb25zb2xlUGFuZWwpID0+IHtcbiAgICBjb25zdCBjb21wbGV0ZXJDb250ZXh0ID0ge1xuICAgICAgZWRpdG9yOiBjb25zb2xlUGFuZWwuY29uc29sZS5wcm9tcHRDZWxsPy5lZGl0b3IgPz8gbnVsbCxcbiAgICAgIHNlc3Npb246IGNvbnNvbGVQYW5lbC5jb25zb2xlLnNlc3Npb25Db250ZXh0LnNlc3Npb24sXG4gICAgICB3aWRnZXQ6IGNvbnNvbGVQYW5lbFxuICAgIH07XG4gICAgYXdhaXQgbWFuYWdlci51cGRhdGVDb21wbGV0ZXIoY29tcGxldGVyQ29udGV4dCk7XG4gICAgY29uc29sZVBhbmVsLmNvbnNvbGUucHJvbXB0Q2VsbENyZWF0ZWQuY29ubmVjdCgoY29kZUNvbnNvbGUsIGNlbGwpID0+IHtcbiAgICAgIGNvbnN0IG5ld0NvbnRleHQgPSB7XG4gICAgICAgIGVkaXRvcjogY2VsbC5lZGl0b3IsXG4gICAgICAgIHNlc3Npb246IGNvZGVDb25zb2xlLnNlc3Npb25Db250ZXh0LnNlc3Npb24sXG4gICAgICAgIHdpZGdldDogY29uc29sZVBhbmVsLFxuICAgICAgICBzYW5pdHplcjogc2FuaXRpemVyXG4gICAgICB9O1xuICAgICAgbWFuYWdlci51cGRhdGVDb21wbGV0ZXIobmV3Q29udGV4dCkuY2F0Y2goY29uc29sZS5lcnJvcik7XG4gICAgfSk7XG4gICAgY29uc29sZVBhbmVsLmNvbnNvbGUuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbkNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICBjb25zdCBuZXdDb250ZXh0ID0ge1xuICAgICAgICBlZGl0b3I6IGNvbnNvbGVQYW5lbC5jb25zb2xlLnByb21wdENlbGw/LmVkaXRvciA/PyBudWxsLFxuICAgICAgICBzZXNzaW9uOiBjb25zb2xlUGFuZWwuY29uc29sZS5zZXNzaW9uQ29udGV4dC5zZXNzaW9uLFxuICAgICAgICB3aWRnZXQ6IGNvbnNvbGVQYW5lbCxcbiAgICAgICAgc2FuaXRpemVyOiBzYW5pdGl6ZXJcbiAgICAgIH07XG4gICAgICBtYW5hZ2VyLnVwZGF0ZUNvbXBsZXRlcihuZXdDb250ZXh0KS5jYXRjaChjb25zb2xlLmVycm9yKTtcbiAgICB9KTtcbiAgfTtcbiAgY29uc29sZXMud2lkZ2V0QWRkZWQuY29ubmVjdCh1cGRhdGVDb21wbGV0ZXIpO1xuICBtYW5hZ2VyLmFjdGl2ZVByb3ZpZGVyc0NoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgY29uc29sZXMuZm9yRWFjaChjb25zb2xlV2lkZ2V0ID0+IHtcbiAgICAgIHVwZGF0ZUNvbXBsZXRlcih1bmRlZmluZWQsIGNvbnNvbGVXaWRnZXQpLmNhdGNoKGUgPT4gY29uc29sZS5lcnJvcihlKSk7XG4gICAgfSk7XG4gIH0pO1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9