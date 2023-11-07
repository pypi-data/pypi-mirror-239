"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_terminal-extension_lib_index_js"],{

/***/ "../packages/terminal-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/terminal-extension/lib/index.js ***!
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
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/running */ "webpack/sharing/consume/default/@jupyterlab/running/@jupyterlab/running");
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_running__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/terminal */ "webpack/sharing/consume/default/@jupyterlab/terminal/@jupyterlab/terminal");
/* harmony import */ var _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_10__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module terminal-extension
 */











/**
 * The command IDs used by the terminal plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.copy = 'terminal:copy';
    CommandIDs.createNew = 'terminal:create-new';
    CommandIDs.open = 'terminal:open';
    CommandIDs.refresh = 'terminal:refresh';
    CommandIDs.increaseFont = 'terminal:increase-font';
    CommandIDs.decreaseFont = 'terminal:decrease-font';
    CommandIDs.paste = 'terminal:paste';
    CommandIDs.setTheme = 'terminal:set-theme';
    CommandIDs.shutdown = 'terminal:shut-down';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default terminal extension.
 */
const plugin = {
    activate,
    id: '@jupyterlab/terminal-extension:plugin',
    description: 'Adds terminal and provides its tracker.',
    provides: _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_7__.ITerminalTracker,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_running__WEBPACK_IMPORTED_MODULE_4__.IRunningSessionManagers
    ],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the terminal plugin.
 */
function activate(app, settingRegistry, translator, palette, launcher, restorer, mainMenu, themeManager, runningSessionManagers) {
    const trans = translator.load('jupyterlab');
    const { serviceManager, commands } = app;
    const category = trans.__('Terminal');
    const namespace = 'terminal';
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    // Bail if there are no terminals available.
    if (!serviceManager.terminals.isAvailable()) {
        console.warn('Disabling terminals plugin because they are not available on the server');
        return tracker;
    }
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.createNew,
            args: widget => ({ name: widget.content.session.name }),
            name: widget => widget.content.session.name
        });
    }
    // The cached terminal options from the setting editor.
    const options = {};
    /**
     * Update the cached option values.
     */
    function updateOptions(settings) {
        // Update the cached options by doing a shallow copy of key/values.
        // This is needed because options is passed and used in addcommand-palette and needs
        // to reflect the current cached values.
        Object.keys(settings.composite).forEach((key) => {
            options[key] = settings.composite[key];
        });
    }
    /**
     * Update terminal
     */
    function updateTerminal(widget) {
        const terminal = widget.content;
        if (!terminal) {
            return;
        }
        Object.keys(options).forEach((key) => {
            terminal.setOption(key, options[key]);
        });
    }
    /**
     * Update the settings of the current tracker instances.
     */
    function updateTracker() {
        tracker.forEach(widget => updateTerminal(widget));
    }
    // Fetch the initial state of the settings.
    settingRegistry
        .load(plugin.id)
        .then(settings => {
        updateOptions(settings);
        updateTracker();
        settings.changed.connect(() => {
            updateOptions(settings);
            updateTracker();
        });
    })
        .catch(Private.showErrorMessage);
    // Subscribe to changes in theme. This is needed as the theme
    // is computed dynamically based on the string value and DOM
    // properties.
    themeManager === null || themeManager === void 0 ? void 0 : themeManager.themeChanged.connect((sender, args) => {
        tracker.forEach(widget => {
            const terminal = widget.content;
            if (terminal.getOption('theme') === 'inherit') {
                terminal.setOption('theme', 'inherit');
            }
        });
    });
    addCommands(app, tracker, settingRegistry, translator, options);
    if (mainMenu) {
        // Add "Terminal Theme" menu below "Theme" menu.
        const themeMenu = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__.Menu({ commands });
        themeMenu.title.label = trans._p('menu', 'Terminal Theme');
        themeMenu.addItem({
            command: CommandIDs.setTheme,
            args: {
                theme: 'inherit',
                displayName: trans.__('Inherit'),
                isPalette: false
            }
        });
        themeMenu.addItem({
            command: CommandIDs.setTheme,
            args: {
                theme: 'light',
                displayName: trans.__('Light'),
                isPalette: false
            }
        });
        themeMenu.addItem({
            command: CommandIDs.setTheme,
            args: { theme: 'dark', displayName: trans.__('Dark'), isPalette: false }
        });
        // Add some commands to the "View" menu.
        mainMenu.settingsMenu.addGroup([
            { command: CommandIDs.increaseFont },
            { command: CommandIDs.decreaseFont },
            { type: 'submenu', submenu: themeMenu }
        ], 40);
        // Add terminal creation to the file menu.
        mainMenu.fileMenu.newMenu.addItem({
            command: CommandIDs.createNew,
            rank: 20
        });
        // Add terminal close-and-shutdown to the file menu.
        mainMenu.fileMenu.closeAndCleaners.add({
            id: CommandIDs.shutdown,
            isEnabled: (w) => tracker.currentWidget !== null && tracker.has(w)
        });
    }
    if (palette) {
        // Add command palette items.
        [
            CommandIDs.createNew,
            CommandIDs.refresh,
            CommandIDs.increaseFont,
            CommandIDs.decreaseFont
        ].forEach(command => {
            palette.addItem({ command, category, args: { isPalette: true } });
        });
        palette.addItem({
            command: CommandIDs.setTheme,
            category,
            args: {
                theme: 'inherit',
                displayName: trans.__('Inherit'),
                isPalette: true
            }
        });
        palette.addItem({
            command: CommandIDs.setTheme,
            category,
            args: { theme: 'light', displayName: trans.__('Light'), isPalette: true }
        });
        palette.addItem({
            command: CommandIDs.setTheme,
            category,
            args: { theme: 'dark', displayName: trans.__('Dark'), isPalette: true }
        });
    }
    // Add a launcher item if the launcher is available.
    if (launcher) {
        launcher.add({
            command: CommandIDs.createNew,
            category: trans.__('Other'),
            rank: 0
        });
    }
    // Add a sessions manager if the running extension is available
    if (runningSessionManagers) {
        addRunningSessionManager(runningSessionManagers, app, translator);
    }
    return tracker;
}
/**
 * Add the running terminal manager to the running panel.
 */
function addRunningSessionManager(managers, app, translator) {
    const trans = translator.load('jupyterlab');
    const manager = app.serviceManager.terminals;
    class RunningTerminal {
        constructor(model) {
            this._model = model;
        }
        open() {
            void app.commands.execute('terminal:open', { name: this._model.name });
        }
        icon() {
            return _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.terminalIcon;
        }
        label() {
            return `terminals/${this._model.name}`;
        }
        shutdown() {
            return manager.shutdown(this._model.name);
        }
    }
    managers.add({
        name: trans.__('Terminals'),
        running: () => Array.from(manager.running()).map(model => new RunningTerminal(model)),
        shutdownAll: () => manager.shutdownAll(),
        refreshRunning: () => manager.refreshRunning(),
        runningChanged: manager.runningChanged,
        shutdownLabel: trans.__('Shut Down'),
        shutdownAllLabel: trans.__('Shut Down All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to permanently shut down all running terminals?')
    });
}
/**
 * Add the commands for the terminal.
 */
function addCommands(app, tracker, settingRegistry, translator, options) {
    const trans = translator.load('jupyterlab');
    const { commands, serviceManager } = app;
    const isEnabled = () => tracker.currentWidget !== null &&
        tracker.currentWidget === app.shell.currentWidget;
    // Add terminal commands.
    commands.addCommand(CommandIDs.createNew, {
        label: args => args['isPalette'] ? trans.__('New Terminal') : trans.__('Terminal'),
        caption: trans.__('Start a new terminal session'),
        icon: args => (args['isPalette'] ? undefined : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.terminalIcon),
        execute: async (args) => {
            const name = args['name'];
            const cwd = args['cwd'];
            const localPath = cwd
                ? serviceManager.contents.localPath(cwd)
                : undefined;
            let session;
            if (name) {
                const models = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_5__.TerminalAPI.listRunning();
                if (models.map(d => d.name).includes(name)) {
                    // we are restoring a terminal widget and the corresponding terminal exists
                    // let's connect to it
                    session = serviceManager.terminals.connectTo({ model: { name } });
                }
                else {
                    // we are restoring a terminal widget but the corresponding terminal was closed
                    // let's start a new terminal with the original name
                    session = await serviceManager.terminals.startNew({
                        name,
                        cwd: localPath
                    });
                }
            }
            else {
                // we are creating a new terminal widget with a new terminal
                // let the server choose the terminal name
                session = await serviceManager.terminals.startNew({ cwd: localPath });
            }
            const term = new _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_7__.Terminal(session, options, translator);
            term.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.terminalIcon;
            term.title.label = '...';
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: term, reveal: term.ready });
            app.shell.add(main, 'main', { type: 'Terminal' });
            void tracker.add(main);
            app.shell.activateById(main.id);
            return main;
        }
    });
    commands.addCommand(CommandIDs.open, {
        label: trans.__('Open a terminal by its `name`.'),
        execute: args => {
            const name = args['name'];
            // Check for a running terminal with the given name.
            const widget = tracker.find(value => {
                const content = value.content;
                return content.session.name === name || false;
            });
            if (widget) {
                app.shell.activateById(widget.id);
            }
            else {
                // Otherwise, create a new terminal with a given name.
                return commands.execute(CommandIDs.createNew, { name });
            }
        }
    });
    commands.addCommand(CommandIDs.refresh, {
        label: trans.__('Refresh Terminal'),
        caption: trans.__('Refresh the current terminal session'),
        execute: async () => {
            const current = tracker.currentWidget;
            if (!current) {
                return;
            }
            app.shell.activateById(current.id);
            try {
                await current.content.refresh();
                if (current) {
                    current.content.activate();
                }
            }
            catch (err) {
                Private.showErrorMessage(err);
            }
        },
        icon: args => args['isPalette']
            ? undefined
            : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.refreshIcon.bindprops({ stylesheet: 'menuItem' }),
        isEnabled
    });
    /**
     * Add copy command
     */
    commands.addCommand(CommandIDs.copy, {
        execute: () => {
            var _a;
            const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
            if (!widget) {
                return;
            }
            const text = widget.getSelection();
            if (text) {
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(text);
            }
        },
        isEnabled: () => {
            var _a;
            if (!isEnabled()) {
                return false;
            }
            const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
            if (!widget) {
                return false;
            }
            // Enable command if there is a text selection in the terminal
            return widget.hasSelection();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Copy')
    });
    /**
     * Add paste command
     */
    commands.addCommand(CommandIDs.paste, {
        execute: async () => {
            var _a;
            const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
            if (!widget) {
                return;
            }
            // Get data from clipboard
            const clipboard = window.navigator.clipboard;
            const clipboardData = await clipboard.readText();
            if (clipboardData) {
                // Paste data to the terminal
                widget.paste(clipboardData);
            }
        },
        isEnabled: () => { var _a; return Boolean(isEnabled() && ((_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content)); },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.pasteIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Paste')
    });
    commands.addCommand(CommandIDs.shutdown, {
        label: trans.__('Shutdown Terminal'),
        execute: () => {
            const current = tracker.currentWidget;
            if (!current) {
                return;
            }
            // The widget is automatically disposed upon session shutdown.
            return current.content.session.shutdown();
        },
        isEnabled
    });
    commands.addCommand(CommandIDs.increaseFont, {
        label: trans.__('Increase Terminal Font Size'),
        execute: async () => {
            const { fontSize } = options;
            if (fontSize && fontSize < 72) {
                try {
                    await settingRegistry.set(plugin.id, 'fontSize', fontSize + 1);
                }
                catch (err) {
                    Private.showErrorMessage(err);
                }
            }
        }
    });
    commands.addCommand(CommandIDs.decreaseFont, {
        label: trans.__('Decrease Terminal Font Size'),
        execute: async () => {
            const { fontSize } = options;
            if (fontSize && fontSize > 9) {
                try {
                    await settingRegistry.set(plugin.id, 'fontSize', fontSize - 1);
                }
                catch (err) {
                    Private.showErrorMessage(err);
                }
            }
        }
    });
    const themeDisplayedName = {
        inherit: trans.__('Inherit'),
        light: trans.__('Light'),
        dark: trans.__('Dark')
    };
    commands.addCommand(CommandIDs.setTheme, {
        label: args => {
            if (args.theme === undefined) {
                return trans.__('Set terminal theme to the provided `theme`.');
            }
            const theme = args['theme'];
            const displayName = theme in themeDisplayedName
                ? themeDisplayedName[theme]
                : trans.__(theme[0].toUpperCase() + theme.slice(1));
            return args['isPalette']
                ? trans.__('Use Terminal Theme: %1', displayName)
                : displayName;
        },
        caption: trans.__('Set the terminal theme'),
        isToggled: args => {
            const { theme } = options;
            return args['theme'] === theme;
        },
        execute: async (args) => {
            const theme = args['theme'];
            try {
                await settingRegistry.set(plugin.id, 'theme', theme);
                commands.notifyCommandChanged(CommandIDs.setTheme);
            }
            catch (err) {
                console.log(err);
                Private.showErrorMessage(err);
            }
        }
    });
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     *  Utility function for consistent error reporting
     */
    function showErrorMessage(error) {
        console.error(`Failed to configure ${plugin.id}: ${error.message}`);
    }
    Private.showErrorMessage = showErrorMessage;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdGVybWluYWwtZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy5jNGUzNjBmOWZiZmZkNTYwMDZiOS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTThCO0FBT0g7QUFDbUI7QUFDQTtBQUMrQjtBQUNuQjtBQUNFO0FBS2pDO0FBQ3dCO0FBTW5CO0FBQ1k7QUFFL0M7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FrQm5CO0FBbEJELFdBQVUsVUFBVTtJQUNMLGVBQUksR0FBRyxlQUFlLENBQUM7SUFFdkIsb0JBQVMsR0FBRyxxQkFBcUIsQ0FBQztJQUVsQyxlQUFJLEdBQUcsZUFBZSxDQUFDO0lBRXZCLGtCQUFPLEdBQUcsa0JBQWtCLENBQUM7SUFFN0IsdUJBQVksR0FBRyx3QkFBd0IsQ0FBQztJQUV4Qyx1QkFBWSxHQUFHLHdCQUF3QixDQUFDO0lBRXhDLGdCQUFLLEdBQUcsZ0JBQWdCLENBQUM7SUFFekIsbUJBQVEsR0FBRyxvQkFBb0IsQ0FBQztJQUVoQyxtQkFBUSxHQUFHLG9CQUFvQixDQUFDO0FBQy9DLENBQUMsRUFsQlMsVUFBVSxLQUFWLFVBQVUsUUFrQm5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBNEM7SUFDdEQsUUFBUTtJQUNSLEVBQUUsRUFBRSx1Q0FBdUM7SUFDM0MsV0FBVyxFQUFFLHlDQUF5QztJQUN0RCxRQUFRLEVBQUUsa0VBQWdCO0lBQzFCLFFBQVEsRUFBRSxDQUFDLHlFQUFnQixFQUFFLGdFQUFXLENBQUM7SUFDekMsUUFBUSxFQUFFO1FBQ1IsaUVBQWU7UUFDZiwyREFBUztRQUNULG9FQUFlO1FBQ2YsMkRBQVM7UUFDVCwrREFBYTtRQUNiLHdFQUF1QjtLQUN4QjtJQUNELFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7R0FFRztBQUNILGlFQUFlLE1BQU0sRUFBQztBQUV0Qjs7R0FFRztBQUNI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LE9BQU8sQ0FBQyxnQkFBZ0IsQ0FBQyxHQUFHLENBQUMsQ0FBQzthQUMvQjtRQUNILENBQUM7S0FDRixDQUFDLENBQUM7QUFDTCxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0FPaEI7QUFQRCxXQUFVLE9BQU87SUFDZjs7T0FFRztJQUNILFNBQWdCLGdCQUFnQixDQUFDLEtBQVk7UUFDM0MsT0FBTyxDQUFDLEtBQUssQ0FBQyx1QkFBdUIsTUFBTSxDQUFDLEVBQUUsS0FBSyxLQUFLLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztJQUN0RSxDQUFDO0lBRmUsd0JBQWdCLG1CQUUvQjtBQUNILENBQUMsRUFQUyxPQUFPLEtBQVAsT0FBTyxRQU9oQiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90ZXJtaW5hbC1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHRlcm1pbmFsLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYXlvdXRSZXN0b3JlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgQ2xpcGJvYXJkLFxuICBJQ29tbWFuZFBhbGV0dGUsXG4gIElUaGVtZU1hbmFnZXIsXG4gIE1haW5BcmVhV2lkZ2V0LFxuICBXaWRnZXRUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElMYXVuY2hlciB9IGZyb20gJ0BqdXB5dGVybGFiL2xhdW5jaGVyJztcbmltcG9ydCB7IElNYWluTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL21haW5tZW51JztcbmltcG9ydCB7IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLCBJUnVubmluZ1Nlc3Npb25zIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcnVubmluZyc7XG5pbXBvcnQgeyBUZXJtaW5hbCwgVGVybWluYWxBUEkgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElUZXJtaW5hbCxcbiAgSVRlcm1pbmFsVHJhY2tlcixcbiAgVGVybWluYWwgYXMgWFRlcm1cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdGVybWluYWwnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBjb3B5SWNvbixcbiAgcGFzdGVJY29uLFxuICByZWZyZXNoSWNvbixcbiAgdGVybWluYWxJY29uXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgTWVudSwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgdGVybWluYWwgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjb3B5ID0gJ3Rlcm1pbmFsOmNvcHknO1xuXG4gIGV4cG9ydCBjb25zdCBjcmVhdGVOZXcgPSAndGVybWluYWw6Y3JlYXRlLW5ldyc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW4gPSAndGVybWluYWw6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IHJlZnJlc2ggPSAndGVybWluYWw6cmVmcmVzaCc7XG5cbiAgZXhwb3J0IGNvbnN0IGluY3JlYXNlRm9udCA9ICd0ZXJtaW5hbDppbmNyZWFzZS1mb250JztcblxuICBleHBvcnQgY29uc3QgZGVjcmVhc2VGb250ID0gJ3Rlcm1pbmFsOmRlY3JlYXNlLWZvbnQnO1xuXG4gIGV4cG9ydCBjb25zdCBwYXN0ZSA9ICd0ZXJtaW5hbDpwYXN0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNldFRoZW1lID0gJ3Rlcm1pbmFsOnNldC10aGVtZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNodXRkb3duID0gJ3Rlcm1pbmFsOnNodXQtZG93bic7XG59XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgdGVybWluYWwgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJVGVybWluYWxUcmFja2VyPiA9IHtcbiAgYWN0aXZhdGUsXG4gIGlkOiAnQGp1cHl0ZXJsYWIvdGVybWluYWwtZXh0ZW5zaW9uOnBsdWdpbicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0ZXJtaW5hbCBhbmQgcHJvdmlkZXMgaXRzIHRyYWNrZXIuJyxcbiAgcHJvdmlkZXM6IElUZXJtaW5hbFRyYWNrZXIsXG4gIHJlcXVpcmVzOiBbSVNldHRpbmdSZWdpc3RyeSwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW1xuICAgIElDb21tYW5kUGFsZXR0ZSxcbiAgICBJTGF1bmNoZXIsXG4gICAgSUxheW91dFJlc3RvcmVyLFxuICAgIElNYWluTWVudSxcbiAgICBJVGhlbWVNYW5hZ2VyLFxuICAgIElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzXG4gIF0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbiBhcyBkZWZhdWx0LlxuICovXG5leHBvcnQgZGVmYXVsdCBwbHVnaW47XG5cbi8qKlxuICogQWN0aXZhdGUgdGhlIHRlcm1pbmFsIHBsdWdpbi5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICBsYXVuY2hlcjogSUxhdW5jaGVyIHwgbnVsbCxcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gIG1haW5NZW51OiBJTWFpbk1lbnUgfCBudWxsLFxuICB0aGVtZU1hbmFnZXI6IElUaGVtZU1hbmFnZXIgfCBudWxsLFxuICBydW5uaW5nU2Vzc2lvbk1hbmFnZXJzOiBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycyB8IG51bGxcbik6IElUZXJtaW5hbFRyYWNrZXIge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCB7IHNlcnZpY2VNYW5hZ2VyLCBjb21tYW5kcyB9ID0gYXBwO1xuICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdUZXJtaW5hbCcpO1xuICBjb25zdCBuYW1lc3BhY2UgPSAndGVybWluYWwnO1xuICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8SVRlcm1pbmFsLklUZXJtaW5hbD4+KHtcbiAgICBuYW1lc3BhY2VcbiAgfSk7XG5cbiAgLy8gQmFpbCBpZiB0aGVyZSBhcmUgbm8gdGVybWluYWxzIGF2YWlsYWJsZS5cbiAgaWYgKCFzZXJ2aWNlTWFuYWdlci50ZXJtaW5hbHMuaXNBdmFpbGFibGUoKSkge1xuICAgIGNvbnNvbGUud2FybihcbiAgICAgICdEaXNhYmxpbmcgdGVybWluYWxzIHBsdWdpbiBiZWNhdXNlIHRoZXkgYXJlIG5vdCBhdmFpbGFibGUgb24gdGhlIHNlcnZlcidcbiAgICApO1xuICAgIHJldHVybiB0cmFja2VyO1xuICB9XG5cbiAgLy8gSGFuZGxlIHN0YXRlIHJlc3RvcmF0aW9uLlxuICBpZiAocmVzdG9yZXIpIHtcbiAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5jcmVhdGVOZXcsXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHsgbmFtZTogd2lkZ2V0LmNvbnRlbnQuc2Vzc2lvbi5uYW1lIH0pLFxuICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb250ZW50LnNlc3Npb24ubmFtZVxuICAgIH0pO1xuICB9XG5cbiAgLy8gVGhlIGNhY2hlZCB0ZXJtaW5hbCBvcHRpb25zIGZyb20gdGhlIHNldHRpbmcgZWRpdG9yLlxuICBjb25zdCBvcHRpb25zOiBQYXJ0aWFsPElUZXJtaW5hbC5JT3B0aW9ucz4gPSB7fTtcblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBjYWNoZWQgb3B0aW9uIHZhbHVlcy5cbiAgICovXG4gIGZ1bmN0aW9uIHVwZGF0ZU9wdGlvbnMoc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzKTogdm9pZCB7XG4gICAgLy8gVXBkYXRlIHRoZSBjYWNoZWQgb3B0aW9ucyBieSBkb2luZyBhIHNoYWxsb3cgY29weSBvZiBrZXkvdmFsdWVzLlxuICAgIC8vIFRoaXMgaXMgbmVlZGVkIGJlY2F1c2Ugb3B0aW9ucyBpcyBwYXNzZWQgYW5kIHVzZWQgaW4gYWRkY29tbWFuZC1wYWxldHRlIGFuZCBuZWVkc1xuICAgIC8vIHRvIHJlZmxlY3QgdGhlIGN1cnJlbnQgY2FjaGVkIHZhbHVlcy5cbiAgICBPYmplY3Qua2V5cyhzZXR0aW5ncy5jb21wb3NpdGUpLmZvckVhY2goKGtleToga2V5b2YgSVRlcm1pbmFsLklPcHRpb25zKSA9PiB7XG4gICAgICAob3B0aW9ucyBhcyBhbnkpW2tleV0gPSBzZXR0aW5ncy5jb21wb3NpdGVba2V5XTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBVcGRhdGUgdGVybWluYWxcbiAgICovXG4gIGZ1bmN0aW9uIHVwZGF0ZVRlcm1pbmFsKHdpZGdldDogTWFpbkFyZWFXaWRnZXQ8SVRlcm1pbmFsLklUZXJtaW5hbD4pOiB2b2lkIHtcbiAgICBjb25zdCB0ZXJtaW5hbCA9IHdpZGdldC5jb250ZW50O1xuICAgIGlmICghdGVybWluYWwpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgT2JqZWN0LmtleXMob3B0aW9ucykuZm9yRWFjaCgoa2V5OiBrZXlvZiBJVGVybWluYWwuSU9wdGlvbnMpID0+IHtcbiAgICAgIHRlcm1pbmFsLnNldE9wdGlvbihrZXksIG9wdGlvbnNba2V5XSk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBzZXR0aW5ncyBvZiB0aGUgY3VycmVudCB0cmFja2VyIGluc3RhbmNlcy5cbiAgICovXG4gIGZ1bmN0aW9uIHVwZGF0ZVRyYWNrZXIoKTogdm9pZCB7XG4gICAgdHJhY2tlci5mb3JFYWNoKHdpZGdldCA9PiB1cGRhdGVUZXJtaW5hbCh3aWRnZXQpKTtcbiAgfVxuXG4gIC8vIEZldGNoIHRoZSBpbml0aWFsIHN0YXRlIG9mIHRoZSBzZXR0aW5ncy5cbiAgc2V0dGluZ1JlZ2lzdHJ5XG4gICAgLmxvYWQocGx1Z2luLmlkKVxuICAgIC50aGVuKHNldHRpbmdzID0+IHtcbiAgICAgIHVwZGF0ZU9wdGlvbnMoc2V0dGluZ3MpO1xuICAgICAgdXBkYXRlVHJhY2tlcigpO1xuICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgdXBkYXRlT3B0aW9ucyhzZXR0aW5ncyk7XG4gICAgICAgIHVwZGF0ZVRyYWNrZXIoKTtcbiAgICAgIH0pO1xuICAgIH0pXG4gICAgLmNhdGNoKFByaXZhdGUuc2hvd0Vycm9yTWVzc2FnZSk7XG5cbiAgLy8gU3Vic2NyaWJlIHRvIGNoYW5nZXMgaW4gdGhlbWUuIFRoaXMgaXMgbmVlZGVkIGFzIHRoZSB0aGVtZVxuICAvLyBpcyBjb21wdXRlZCBkeW5hbWljYWxseSBiYXNlZCBvbiB0aGUgc3RyaW5nIHZhbHVlIGFuZCBET01cbiAgLy8gcHJvcGVydGllcy5cbiAgdGhlbWVNYW5hZ2VyPy50aGVtZUNoYW5nZWQuY29ubmVjdCgoc2VuZGVyLCBhcmdzKSA9PiB7XG4gICAgdHJhY2tlci5mb3JFYWNoKHdpZGdldCA9PiB7XG4gICAgICBjb25zdCB0ZXJtaW5hbCA9IHdpZGdldC5jb250ZW50O1xuICAgICAgaWYgKHRlcm1pbmFsLmdldE9wdGlvbigndGhlbWUnKSA9PT0gJ2luaGVyaXQnKSB7XG4gICAgICAgIHRlcm1pbmFsLnNldE9wdGlvbigndGhlbWUnLCAnaW5oZXJpdCcpO1xuICAgICAgfVxuICAgIH0pO1xuICB9KTtcblxuICBhZGRDb21tYW5kcyhhcHAsIHRyYWNrZXIsIHNldHRpbmdSZWdpc3RyeSwgdHJhbnNsYXRvciwgb3B0aW9ucyk7XG5cbiAgaWYgKG1haW5NZW51KSB7XG4gICAgLy8gQWRkIFwiVGVybWluYWwgVGhlbWVcIiBtZW51IGJlbG93IFwiVGhlbWVcIiBtZW51LlxuICAgIGNvbnN0IHRoZW1lTWVudSA9IG5ldyBNZW51KHsgY29tbWFuZHMgfSk7XG4gICAgdGhlbWVNZW51LnRpdGxlLmxhYmVsID0gdHJhbnMuX3AoJ21lbnUnLCAnVGVybWluYWwgVGhlbWUnKTtcbiAgICB0aGVtZU1lbnUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLnNldFRoZW1lLFxuICAgICAgYXJnczoge1xuICAgICAgICB0aGVtZTogJ2luaGVyaXQnLFxuICAgICAgICBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0luaGVyaXQnKSxcbiAgICAgICAgaXNQYWxldHRlOiBmYWxzZVxuICAgICAgfVxuICAgIH0pO1xuICAgIHRoZW1lTWVudS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2V0VGhlbWUsXG4gICAgICBhcmdzOiB7XG4gICAgICAgIHRoZW1lOiAnbGlnaHQnLFxuICAgICAgICBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0xpZ2h0JyksXG4gICAgICAgIGlzUGFsZXR0ZTogZmFsc2VcbiAgICAgIH1cbiAgICB9KTtcbiAgICB0aGVtZU1lbnUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLnNldFRoZW1lLFxuICAgICAgYXJnczogeyB0aGVtZTogJ2RhcmsnLCBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0RhcmsnKSwgaXNQYWxldHRlOiBmYWxzZSB9XG4gICAgfSk7XG5cbiAgICAvLyBBZGQgc29tZSBjb21tYW5kcyB0byB0aGUgXCJWaWV3XCIgbWVudS5cbiAgICBtYWluTWVudS5zZXR0aW5nc01lbnUuYWRkR3JvdXAoXG4gICAgICBbXG4gICAgICAgIHsgY29tbWFuZDogQ29tbWFuZElEcy5pbmNyZWFzZUZvbnQgfSxcbiAgICAgICAgeyBjb21tYW5kOiBDb21tYW5kSURzLmRlY3JlYXNlRm9udCB9LFxuICAgICAgICB7IHR5cGU6ICdzdWJtZW51Jywgc3VibWVudTogdGhlbWVNZW51IH1cbiAgICAgIF0sXG4gICAgICA0MFxuICAgICk7XG5cbiAgICAvLyBBZGQgdGVybWluYWwgY3JlYXRpb24gdG8gdGhlIGZpbGUgbWVudS5cbiAgICBtYWluTWVudS5maWxlTWVudS5uZXdNZW51LmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5jcmVhdGVOZXcsXG4gICAgICByYW5rOiAyMFxuICAgIH0pO1xuXG4gICAgLy8gQWRkIHRlcm1pbmFsIGNsb3NlLWFuZC1zaHV0ZG93biB0byB0aGUgZmlsZSBtZW51LlxuICAgIG1haW5NZW51LmZpbGVNZW51LmNsb3NlQW5kQ2xlYW5lcnMuYWRkKHtcbiAgICAgIGlkOiBDb21tYW5kSURzLnNodXRkb3duLFxuICAgICAgaXNFbmFibGVkOiAodzogV2lkZ2V0KSA9PiB0cmFja2VyLmN1cnJlbnRXaWRnZXQgIT09IG51bGwgJiYgdHJhY2tlci5oYXModylcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgLy8gQWRkIGNvbW1hbmQgcGFsZXR0ZSBpdGVtcy5cbiAgICBbXG4gICAgICBDb21tYW5kSURzLmNyZWF0ZU5ldyxcbiAgICAgIENvbW1hbmRJRHMucmVmcmVzaCxcbiAgICAgIENvbW1hbmRJRHMuaW5jcmVhc2VGb250LFxuICAgICAgQ29tbWFuZElEcy5kZWNyZWFzZUZvbnRcbiAgICBdLmZvckVhY2goY29tbWFuZCA9PiB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSwgYXJnczogeyBpc1BhbGV0dGU6IHRydWUgfSB9KTtcbiAgICB9KTtcbiAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5zZXRUaGVtZSxcbiAgICAgIGNhdGVnb3J5LFxuICAgICAgYXJnczoge1xuICAgICAgICB0aGVtZTogJ2luaGVyaXQnLFxuICAgICAgICBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0luaGVyaXQnKSxcbiAgICAgICAgaXNQYWxldHRlOiB0cnVlXG4gICAgICB9XG4gICAgfSk7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuc2V0VGhlbWUsXG4gICAgICBjYXRlZ29yeSxcbiAgICAgIGFyZ3M6IHsgdGhlbWU6ICdsaWdodCcsIGRpc3BsYXlOYW1lOiB0cmFucy5fXygnTGlnaHQnKSwgaXNQYWxldHRlOiB0cnVlIH1cbiAgICB9KTtcbiAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5zZXRUaGVtZSxcbiAgICAgIGNhdGVnb3J5LFxuICAgICAgYXJnczogeyB0aGVtZTogJ2RhcmsnLCBkaXNwbGF5TmFtZTogdHJhbnMuX18oJ0RhcmsnKSwgaXNQYWxldHRlOiB0cnVlIH1cbiAgICB9KTtcbiAgfVxuXG4gIC8vIEFkZCBhIGxhdW5jaGVyIGl0ZW0gaWYgdGhlIGxhdW5jaGVyIGlzIGF2YWlsYWJsZS5cbiAgaWYgKGxhdW5jaGVyKSB7XG4gICAgbGF1bmNoZXIuYWRkKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlTmV3LFxuICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdPdGhlcicpLFxuICAgICAgcmFuazogMFxuICAgIH0pO1xuICB9XG5cbiAgLy8gQWRkIGEgc2Vzc2lvbnMgbWFuYWdlciBpZiB0aGUgcnVubmluZyBleHRlbnNpb24gaXMgYXZhaWxhYmxlXG4gIGlmIChydW5uaW5nU2Vzc2lvbk1hbmFnZXJzKSB7XG4gICAgYWRkUnVubmluZ1Nlc3Npb25NYW5hZ2VyKHJ1bm5pbmdTZXNzaW9uTWFuYWdlcnMsIGFwcCwgdHJhbnNsYXRvcik7XG4gIH1cblxuICByZXR1cm4gdHJhY2tlcjtcbn1cblxuLyoqXG4gKiBBZGQgdGhlIHJ1bm5pbmcgdGVybWluYWwgbWFuYWdlciB0byB0aGUgcnVubmluZyBwYW5lbC5cbiAqL1xuZnVuY3Rpb24gYWRkUnVubmluZ1Nlc3Npb25NYW5hZ2VyKFxuICBtYW5hZ2VyczogSVJ1bm5pbmdTZXNzaW9uTWFuYWdlcnMsXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuKSB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IG1hbmFnZXIgPSBhcHAuc2VydmljZU1hbmFnZXIudGVybWluYWxzO1xuXG4gIGNsYXNzIFJ1bm5pbmdUZXJtaW5hbCBpbXBsZW1lbnRzIElSdW5uaW5nU2Vzc2lvbnMuSVJ1bm5pbmdJdGVtIHtcbiAgICBjb25zdHJ1Y3Rvcihtb2RlbDogVGVybWluYWwuSU1vZGVsKSB7XG4gICAgICB0aGlzLl9tb2RlbCA9IG1vZGVsO1xuICAgIH1cbiAgICBvcGVuKCkge1xuICAgICAgdm9pZCBhcHAuY29tbWFuZHMuZXhlY3V0ZSgndGVybWluYWw6b3BlbicsIHsgbmFtZTogdGhpcy5fbW9kZWwubmFtZSB9KTtcbiAgICB9XG4gICAgaWNvbigpIHtcbiAgICAgIHJldHVybiB0ZXJtaW5hbEljb247XG4gICAgfVxuICAgIGxhYmVsKCkge1xuICAgICAgcmV0dXJuIGB0ZXJtaW5hbHMvJHt0aGlzLl9tb2RlbC5uYW1lfWA7XG4gICAgfVxuICAgIHNodXRkb3duKCkge1xuICAgICAgcmV0dXJuIG1hbmFnZXIuc2h1dGRvd24odGhpcy5fbW9kZWwubmFtZSk7XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfbW9kZWw6IFRlcm1pbmFsLklNb2RlbDtcbiAgfVxuXG4gIG1hbmFnZXJzLmFkZCh7XG4gICAgbmFtZTogdHJhbnMuX18oJ1Rlcm1pbmFscycpLFxuICAgIHJ1bm5pbmc6ICgpID0+XG4gICAgICBBcnJheS5mcm9tKG1hbmFnZXIucnVubmluZygpKS5tYXAobW9kZWwgPT4gbmV3IFJ1bm5pbmdUZXJtaW5hbChtb2RlbCkpLFxuICAgIHNodXRkb3duQWxsOiAoKSA9PiBtYW5hZ2VyLnNodXRkb3duQWxsKCksXG4gICAgcmVmcmVzaFJ1bm5pbmc6ICgpID0+IG1hbmFnZXIucmVmcmVzaFJ1bm5pbmcoKSxcbiAgICBydW5uaW5nQ2hhbmdlZDogbWFuYWdlci5ydW5uaW5nQ2hhbmdlZCxcbiAgICBzaHV0ZG93bkxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duJyksXG4gICAgc2h1dGRvd25BbGxMYWJlbDogdHJhbnMuX18oJ1NodXQgRG93biBBbGwnKSxcbiAgICBzaHV0ZG93bkFsbENvbmZpcm1hdGlvblRleHQ6IHRyYW5zLl9fKFxuICAgICAgJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byBwZXJtYW5lbnRseSBzaHV0IGRvd24gYWxsIHJ1bm5pbmcgdGVybWluYWxzPydcbiAgICApXG4gIH0pO1xufVxuXG4vKipcbiAqIEFkZCB0aGUgY29tbWFuZHMgZm9yIHRoZSB0ZXJtaW5hbC5cbiAqL1xuZnVuY3Rpb24gYWRkQ29tbWFuZHMoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFja2VyOiBXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PElUZXJtaW5hbC5JVGVybWluYWw+PixcbiAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgb3B0aW9uczogUGFydGlhbDxJVGVybWluYWwuSU9wdGlvbnM+XG4pOiB2b2lkIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgeyBjb21tYW5kcywgc2VydmljZU1hbmFnZXIgfSA9IGFwcDtcblxuICBjb25zdCBpc0VuYWJsZWQgPSAoKSA9PlxuICAgIHRyYWNrZXIuY3VycmVudFdpZGdldCAhPT0gbnVsbCAmJlxuICAgIHRyYWNrZXIuY3VycmVudFdpZGdldCA9PT0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG5cbiAgLy8gQWRkIHRlcm1pbmFsIGNvbW1hbmRzLlxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3JlYXRlTmV3LCB7XG4gICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgIGFyZ3NbJ2lzUGFsZXR0ZSddID8gdHJhbnMuX18oJ05ldyBUZXJtaW5hbCcpIDogdHJhbnMuX18oJ1Rlcm1pbmFsJyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ1N0YXJ0IGEgbmV3IHRlcm1pbmFsIHNlc3Npb24nKSxcbiAgICBpY29uOiBhcmdzID0+IChhcmdzWydpc1BhbGV0dGUnXSA/IHVuZGVmaW5lZCA6IHRlcm1pbmFsSWNvbiksXG4gICAgZXhlY3V0ZTogYXN5bmMgYXJncyA9PiB7XG4gICAgICBjb25zdCBuYW1lID0gYXJnc1snbmFtZSddIGFzIHN0cmluZztcbiAgICAgIGNvbnN0IGN3ZCA9IGFyZ3NbJ2N3ZCddIGFzIHN0cmluZztcbiAgICAgIGNvbnN0IGxvY2FsUGF0aCA9IGN3ZFxuICAgICAgICA/IHNlcnZpY2VNYW5hZ2VyLmNvbnRlbnRzLmxvY2FsUGF0aChjd2QpXG4gICAgICAgIDogdW5kZWZpbmVkO1xuXG4gICAgICBsZXQgc2Vzc2lvbjtcbiAgICAgIGlmIChuYW1lKSB7XG4gICAgICAgIGNvbnN0IG1vZGVscyA9IGF3YWl0IFRlcm1pbmFsQVBJLmxpc3RSdW5uaW5nKCk7XG4gICAgICAgIGlmIChtb2RlbHMubWFwKGQgPT4gZC5uYW1lKS5pbmNsdWRlcyhuYW1lKSkge1xuICAgICAgICAgIC8vIHdlIGFyZSByZXN0b3JpbmcgYSB0ZXJtaW5hbCB3aWRnZXQgYW5kIHRoZSBjb3JyZXNwb25kaW5nIHRlcm1pbmFsIGV4aXN0c1xuICAgICAgICAgIC8vIGxldCdzIGNvbm5lY3QgdG8gaXRcbiAgICAgICAgICBzZXNzaW9uID0gc2VydmljZU1hbmFnZXIudGVybWluYWxzLmNvbm5lY3RUbyh7IG1vZGVsOiB7IG5hbWUgfSB9KTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAvLyB3ZSBhcmUgcmVzdG9yaW5nIGEgdGVybWluYWwgd2lkZ2V0IGJ1dCB0aGUgY29ycmVzcG9uZGluZyB0ZXJtaW5hbCB3YXMgY2xvc2VkXG4gICAgICAgICAgLy8gbGV0J3Mgc3RhcnQgYSBuZXcgdGVybWluYWwgd2l0aCB0aGUgb3JpZ2luYWwgbmFtZVxuICAgICAgICAgIHNlc3Npb24gPSBhd2FpdCBzZXJ2aWNlTWFuYWdlci50ZXJtaW5hbHMuc3RhcnROZXcoe1xuICAgICAgICAgICAgbmFtZSxcbiAgICAgICAgICAgIGN3ZDogbG9jYWxQYXRoXG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIC8vIHdlIGFyZSBjcmVhdGluZyBhIG5ldyB0ZXJtaW5hbCB3aWRnZXQgd2l0aCBhIG5ldyB0ZXJtaW5hbFxuICAgICAgICAvLyBsZXQgdGhlIHNlcnZlciBjaG9vc2UgdGhlIHRlcm1pbmFsIG5hbWVcbiAgICAgICAgc2Vzc2lvbiA9IGF3YWl0IHNlcnZpY2VNYW5hZ2VyLnRlcm1pbmFscy5zdGFydE5ldyh7IGN3ZDogbG9jYWxQYXRoIH0pO1xuICAgICAgfVxuXG4gICAgICBjb25zdCB0ZXJtID0gbmV3IFhUZXJtKHNlc3Npb24sIG9wdGlvbnMsIHRyYW5zbGF0b3IpO1xuXG4gICAgICB0ZXJtLnRpdGxlLmljb24gPSB0ZXJtaW5hbEljb247XG4gICAgICB0ZXJtLnRpdGxlLmxhYmVsID0gJy4uLic7XG5cbiAgICAgIGNvbnN0IG1haW4gPSBuZXcgTWFpbkFyZWFXaWRnZXQoeyBjb250ZW50OiB0ZXJtLCByZXZlYWw6IHRlcm0ucmVhZHkgfSk7XG4gICAgICBhcHAuc2hlbGwuYWRkKG1haW4sICdtYWluJywgeyB0eXBlOiAnVGVybWluYWwnIH0pO1xuICAgICAgdm9pZCB0cmFja2VyLmFkZChtYWluKTtcbiAgICAgIGFwcC5zaGVsbC5hY3RpdmF0ZUJ5SWQobWFpbi5pZCk7XG4gICAgICByZXR1cm4gbWFpbjtcbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIGEgdGVybWluYWwgYnkgaXRzIGBuYW1lYC4nKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IG5hbWUgPSBhcmdzWyduYW1lJ10gYXMgc3RyaW5nO1xuICAgICAgLy8gQ2hlY2sgZm9yIGEgcnVubmluZyB0ZXJtaW5hbCB3aXRoIHRoZSBnaXZlbiBuYW1lLlxuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5maW5kKHZhbHVlID0+IHtcbiAgICAgICAgY29uc3QgY29udGVudCA9IHZhbHVlLmNvbnRlbnQ7XG4gICAgICAgIHJldHVybiBjb250ZW50LnNlc3Npb24ubmFtZSA9PT0gbmFtZSB8fCBmYWxzZTtcbiAgICAgIH0pO1xuICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICBhcHAuc2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvLyBPdGhlcndpc2UsIGNyZWF0ZSBhIG5ldyB0ZXJtaW5hbCB3aXRoIGEgZ2l2ZW4gbmFtZS5cbiAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5jcmVhdGVOZXcsIHsgbmFtZSB9KTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZWZyZXNoLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSZWZyZXNoIFRlcm1pbmFsJyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ1JlZnJlc2ggdGhlIGN1cnJlbnQgdGVybWluYWwgc2Vzc2lvbicpLFxuICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgYXBwLnNoZWxsLmFjdGl2YXRlQnlJZChjdXJyZW50LmlkKTtcbiAgICAgIHRyeSB7XG4gICAgICAgIGF3YWl0IGN1cnJlbnQuY29udGVudC5yZWZyZXNoKCk7XG4gICAgICAgIGlmIChjdXJyZW50KSB7XG4gICAgICAgICAgY3VycmVudC5jb250ZW50LmFjdGl2YXRlKCk7XG4gICAgICAgIH1cbiAgICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgICBQcml2YXRlLnNob3dFcnJvck1lc3NhZ2UoZXJyKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IGFyZ3MgPT5cbiAgICAgIGFyZ3NbJ2lzUGFsZXR0ZSddXG4gICAgICAgID8gdW5kZWZpbmVkXG4gICAgICAgIDogcmVmcmVzaEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgLyoqXG4gICAqIEFkZCBjb3B5IGNvbW1hbmRcbiAgICovXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5LCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IHRleHQgPSB3aWRnZXQuZ2V0U2VsZWN0aW9uKCk7XG5cbiAgICAgIGlmICh0ZXh0KSB7XG4gICAgICAgIENsaXBib2FyZC5jb3B5VG9TeXN0ZW0odGV4dCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgIGlmICghaXNFbmFibGVkKCkpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuXG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cblxuICAgICAgLy8gRW5hYmxlIGNvbW1hbmQgaWYgdGhlcmUgaXMgYSB0ZXh0IHNlbGVjdGlvbiBpbiB0aGUgdGVybWluYWxcbiAgICAgIHJldHVybiB3aWRnZXQuaGFzU2VsZWN0aW9uKCk7XG4gICAgfSxcbiAgICBpY29uOiBjb3B5SWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgIGxhYmVsOiB0cmFucy5fXygnQ29weScpXG4gIH0pO1xuXG4gIC8qKlxuICAgKiBBZGQgcGFzdGUgY29tbWFuZFxuICAgKi9cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnBhc3RlLCB7XG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIC8vIEdldCBkYXRhIGZyb20gY2xpcGJvYXJkXG4gICAgICBjb25zdCBjbGlwYm9hcmQgPSB3aW5kb3cubmF2aWdhdG9yLmNsaXBib2FyZDtcbiAgICAgIGNvbnN0IGNsaXBib2FyZERhdGE6IHN0cmluZyA9IGF3YWl0IGNsaXBib2FyZC5yZWFkVGV4dCgpO1xuXG4gICAgICBpZiAoY2xpcGJvYXJkRGF0YSkge1xuICAgICAgICAvLyBQYXN0ZSBkYXRhIHRvIHRoZSB0ZXJtaW5hbFxuICAgICAgICB3aWRnZXQucGFzdGUoY2xpcGJvYXJkRGF0YSk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IEJvb2xlYW4oaXNFbmFibGVkKCkgJiYgdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50KSxcbiAgICBpY29uOiBwYXN0ZUljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Bhc3RlJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNodXRkb3duLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTaHV0ZG93biBUZXJtaW5hbCcpLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICAvLyBUaGUgd2lkZ2V0IGlzIGF1dG9tYXRpY2FsbHkgZGlzcG9zZWQgdXBvbiBzZXNzaW9uIHNodXRkb3duLlxuICAgICAgcmV0dXJuIGN1cnJlbnQuY29udGVudC5zZXNzaW9uLnNodXRkb3duKCk7XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmluY3JlYXNlRm9udCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnSW5jcmVhc2UgVGVybWluYWwgRm9udCBTaXplJyksXG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3QgeyBmb250U2l6ZSB9ID0gb3B0aW9ucztcbiAgICAgIGlmIChmb250U2l6ZSAmJiBmb250U2l6ZSA8IDcyKSB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgYXdhaXQgc2V0dGluZ1JlZ2lzdHJ5LnNldChwbHVnaW4uaWQsICdmb250U2l6ZScsIGZvbnRTaXplICsgMSk7XG4gICAgICAgIH0gY2F0Y2ggKGVycikge1xuICAgICAgICAgIFByaXZhdGUuc2hvd0Vycm9yTWVzc2FnZShlcnIpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZGVjcmVhc2VGb250LCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdEZWNyZWFzZSBUZXJtaW5hbCBGb250IFNpemUnKSxcbiAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICBjb25zdCB7IGZvbnRTaXplIH0gPSBvcHRpb25zO1xuICAgICAgaWYgKGZvbnRTaXplICYmIGZvbnRTaXplID4gOSkge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIGF3YWl0IHNldHRpbmdSZWdpc3RyeS5zZXQocGx1Z2luLmlkLCAnZm9udFNpemUnLCBmb250U2l6ZSAtIDEpO1xuICAgICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgICBQcml2YXRlLnNob3dFcnJvck1lc3NhZ2UoZXJyKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29uc3QgdGhlbWVEaXNwbGF5ZWROYW1lID0ge1xuICAgIGluaGVyaXQ6IHRyYW5zLl9fKCdJbmhlcml0JyksXG4gICAgbGlnaHQ6IHRyYW5zLl9fKCdMaWdodCcpLFxuICAgIGRhcms6IHRyYW5zLl9fKCdEYXJrJylcbiAgfTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2V0VGhlbWUsIHtcbiAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICBpZiAoYXJncy50aGVtZSA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIHJldHVybiB0cmFucy5fXygnU2V0IHRlcm1pbmFsIHRoZW1lIHRvIHRoZSBwcm92aWRlZCBgdGhlbWVgLicpO1xuICAgICAgfVxuICAgICAgY29uc3QgdGhlbWUgPSBhcmdzWyd0aGVtZSddIGFzIHN0cmluZztcbiAgICAgIGNvbnN0IGRpc3BsYXlOYW1lID1cbiAgICAgICAgdGhlbWUgaW4gdGhlbWVEaXNwbGF5ZWROYW1lXG4gICAgICAgICAgPyB0aGVtZURpc3BsYXllZE5hbWVbdGhlbWUgYXMga2V5b2YgdHlwZW9mIHRoZW1lRGlzcGxheWVkTmFtZV1cbiAgICAgICAgICA6IHRyYW5zLl9fKHRoZW1lWzBdLnRvVXBwZXJDYXNlKCkgKyB0aGVtZS5zbGljZSgxKSk7XG4gICAgICByZXR1cm4gYXJnc1snaXNQYWxldHRlJ11cbiAgICAgICAgPyB0cmFucy5fXygnVXNlIFRlcm1pbmFsIFRoZW1lOiAlMScsIGRpc3BsYXlOYW1lKVxuICAgICAgICA6IGRpc3BsYXlOYW1lO1xuICAgIH0sXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ1NldCB0aGUgdGVybWluYWwgdGhlbWUnKSxcbiAgICBpc1RvZ2dsZWQ6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgeyB0aGVtZSB9ID0gb3B0aW9ucztcbiAgICAgIHJldHVybiBhcmdzWyd0aGVtZSddID09PSB0aGVtZTtcbiAgICB9LFxuICAgIGV4ZWN1dGU6IGFzeW5jIGFyZ3MgPT4ge1xuICAgICAgY29uc3QgdGhlbWUgPSBhcmdzWyd0aGVtZSddIGFzIElUZXJtaW5hbC5UaGVtZTtcbiAgICAgIHRyeSB7XG4gICAgICAgIGF3YWl0IHNldHRpbmdSZWdpc3RyeS5zZXQocGx1Z2luLmlkLCAndGhlbWUnLCB0aGVtZSk7XG4gICAgICAgIGNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMuc2V0VGhlbWUpO1xuICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgIGNvbnNvbGUubG9nKGVycik7XG4gICAgICAgIFByaXZhdGUuc2hvd0Vycm9yTWVzc2FnZShlcnIpO1xuICAgICAgfVxuICAgIH1cbiAgfSk7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogIFV0aWxpdHkgZnVuY3Rpb24gZm9yIGNvbnNpc3RlbnQgZXJyb3IgcmVwb3J0aW5nXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gc2hvd0Vycm9yTWVzc2FnZShlcnJvcjogRXJyb3IpOiB2b2lkIHtcbiAgICBjb25zb2xlLmVycm9yKGBGYWlsZWQgdG8gY29uZmlndXJlICR7cGx1Z2luLmlkfTogJHtlcnJvci5tZXNzYWdlfWApO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=