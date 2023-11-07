"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_running-extension_lib_index_js-packages_running-extension_lib_kernels_js"],{

/***/ "../packages/running-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../packages/running-extension/lib/index.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/running */ "webpack/sharing/consume/default/@jupyterlab/running/@jupyterlab/running");
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _kernels__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./kernels */ "../packages/running-extension/lib/kernels.js");
/* harmony import */ var _opentabs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./opentabs */ "../packages/running-extension/lib/opentabs.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module running-extension
 */






/**
 * The command IDs used by the running plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.kernelNewConsole = 'running:kernel-new-console';
    CommandIDs.kernelNewNotebook = 'running:kernel-new-notebook';
    CommandIDs.kernelOpenSession = 'running:kernel-open-session';
    CommandIDs.kernelShutDown = 'running:kernel-shut-down';
    CommandIDs.showPanel = 'running:show-panel';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default running sessions extension.
 */
const plugin = {
    activate,
    id: '@jupyterlab/running-extension:plugin',
    description: 'Provides the running session managers.',
    provides: _jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__.IRunningSessionManagers,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the running plugin.
 */
function activate(app, translator, restorer, labShell) {
    const trans = translator.load('jupyterlab');
    const runningSessionManagers = new _jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__.RunningSessionManagers();
    const running = new _jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__.RunningSessions(runningSessionManagers, translator);
    running.id = 'jp-running-sessions';
    running.title.caption = trans.__('Running Terminals and Kernels');
    running.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.runningIcon;
    running.node.setAttribute('role', 'region');
    running.node.setAttribute('aria-label', trans.__('Running Sessions section'));
    // Let the application restorer track the running panel for restoration of
    // application state (e.g. setting the running panel as the current side bar
    // widget).
    if (restorer) {
        restorer.add(running, 'running-sessions');
    }
    if (labShell) {
        (0,_opentabs__WEBPACK_IMPORTED_MODULE_4__.addOpenTabsSessionManager)(runningSessionManagers, translator, labShell);
    }
    void (0,_kernels__WEBPACK_IMPORTED_MODULE_5__.addKernelRunningSessionManager)(runningSessionManagers, translator, app);
    // Rank has been chosen somewhat arbitrarily to give priority to the running
    // sessions widget in the sidebar.
    app.shell.add(running, 'left', { rank: 200, type: 'Sessions and Tabs' });
    app.commands.addCommand(CommandIDs.showPanel, {
        label: trans.__('Sessions and Tabs'),
        execute: () => {
            app.shell.activateById(running.id);
        }
    });
    return runningSessionManagers;
}


/***/ }),

/***/ "../packages/running-extension/lib/kernels.js":
/*!****************************************************!*\
  !*** ../packages/running-extension/lib/kernels.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "addKernelRunningSessionManager": () => (/* binding */ addKernelRunningSessionManager)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! . */ "../packages/running-extension/lib/index.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





const ITEM_CLASS = 'jp-mod-kernel';
/**
 * Add the running kernel manager (notebooks & consoles) to the running panel.
 */
async function addKernelRunningSessionManager(managers, translator, app) {
    const { commands, contextMenu, serviceManager } = app;
    const { kernels, kernelspecs, sessions } = serviceManager;
    const { runningChanged, RunningKernel } = Private;
    const throttler = new _lumino_polling__WEBPACK_IMPORTED_MODULE_2__.Throttler(() => runningChanged.emit(undefined), 100);
    const trans = translator.load('jupyterlab');
    // Throttle signal emissions from the kernel and session managers.
    kernels.runningChanged.connect(() => void throttler.invoke());
    sessions.runningChanged.connect(() => void throttler.invoke());
    // Wait until the relevant services are ready.
    await Promise.all([kernels.ready, kernelspecs.ready, sessions.ready]);
    // Add the kernels pane to the running sidebar.
    managers.add({
        name: trans.__('Kernels'),
        running: () => Array.from(kernels.running()).map(kernel => {
            var _a;
            return new RunningKernel({
                commands,
                kernel,
                kernels,
                sessions,
                spec: (_a = kernelspecs.specs) === null || _a === void 0 ? void 0 : _a.kernelspecs[kernel.name],
                trans
            });
        }),
        shutdownAll: () => kernels.shutdownAll(),
        refreshRunning: () => Promise.all([kernels.refreshRunning(), sessions.refreshRunning()]),
        runningChanged,
        shutdownLabel: trans.__('Shut Down Kernel'),
        shutdownAllLabel: trans.__('Shut Down All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to permanently shut down all running kernels?')
    });
    // Add running kernels commands to the registry.
    const test = (node) => node.classList.contains(ITEM_CLASS);
    commands.addCommand(___WEBPACK_IMPORTED_MODULE_4__.CommandIDs.kernelNewConsole, {
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.consoleIcon,
        label: trans.__('New Console for Kernel'),
        execute: args => {
            var _a;
            const node = app.contextMenuHitTest(test);
            const id = (_a = args.id) !== null && _a !== void 0 ? _a : node === null || node === void 0 ? void 0 : node.dataset['context'];
            if (id) {
                return commands.execute('console:create', { kernelPreference: { id } });
            }
        }
    });
    commands.addCommand(___WEBPACK_IMPORTED_MODULE_4__.CommandIDs.kernelNewNotebook, {
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.notebookIcon,
        label: trans.__('New Notebook for Kernel'),
        execute: args => {
            var _a;
            const node = app.contextMenuHitTest(test);
            const id = (_a = args.id) !== null && _a !== void 0 ? _a : node === null || node === void 0 ? void 0 : node.dataset['context'];
            if (id) {
                return commands.execute('notebook:create-new', { kernelId: id });
            }
        }
    });
    commands.addCommand(___WEBPACK_IMPORTED_MODULE_4__.CommandIDs.kernelOpenSession, {
        icon: args => args.type === 'console'
            ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.consoleIcon
            : args.type === 'notebook'
                ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.notebookIcon
                : undefined,
        isEnabled: ({ path, type }) => !!type || path !== undefined,
        label: ({ name, path }) => name ||
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.basename(path || trans.__('Unknown Session')),
        execute: ({ path, type }) => {
            if (!type || path === undefined) {
                return;
            }
            const command = type === 'console' ? 'console:open' : 'docmanager:open';
            return commands.execute(command, { path });
        }
    });
    commands.addCommand(___WEBPACK_IMPORTED_MODULE_4__.CommandIDs.kernelShutDown, {
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.closeIcon,
        label: trans.__('Shut Down Kernel'),
        execute: args => {
            var _a;
            const node = app.contextMenuHitTest(test);
            const id = (_a = args.id) !== null && _a !== void 0 ? _a : node === null || node === void 0 ? void 0 : node.dataset['context'];
            if (id) {
                return kernels.shutdown(id);
            }
        }
    });
    const sessionsItems = [];
    // Populate connected sessions submenu when context menu is opened.
    contextMenu.opened.connect(async () => {
        var _a, _b, _c;
        const submenu = (_b = (_a = contextMenu.menu.items.find(item => {
            var _a;
            return item.type === 'submenu' &&
                ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-contextmenu-connected-sessions';
        })) === null || _a === void 0 ? void 0 : _a.submenu) !== null && _b !== void 0 ? _b : null;
        if (!submenu) {
            // Bail early if the connected session menu is not found
            return;
        }
        // Empty the connected sessions submenu.
        sessionsItems.forEach(item => item.dispose());
        sessionsItems.length = 0;
        submenu.clearItems();
        const node = app.contextMenuHitTest(test);
        const id = node === null || node === void 0 ? void 0 : node.dataset['context'];
        if (!id) {
            return;
        }
        // Populate the submenu with sessions connected to this kernel.
        const command = ___WEBPACK_IMPORTED_MODULE_4__.CommandIDs.kernelOpenSession;
        for (const session of sessions.running()) {
            if (id === ((_c = session.kernel) === null || _c === void 0 ? void 0 : _c.id)) {
                const { name, path, type } = session;
                sessionsItems.push(submenu.addItem({ command, args: { name, path, type } }));
            }
        }
    });
}
var Private;
(function (Private) {
    class RunningKernel {
        constructor(options) {
            this.className = ITEM_CLASS;
            this.commands = options.commands;
            this.kernel = options.kernel;
            this.context = this.kernel.id;
            this.kernels = options.kernels;
            this.sessions = options.sessions;
            this.spec = options.spec || null;
            this.trans = options.trans;
        }
        get children() {
            var _a;
            const children = [];
            const open = ___WEBPACK_IMPORTED_MODULE_4__.CommandIDs.kernelOpenSession;
            const { commands } = this;
            for (const session of this.sessions.running()) {
                if (this.kernel.id === ((_a = session.kernel) === null || _a === void 0 ? void 0 : _a.id)) {
                    const { name, path, type } = session;
                    children.push({
                        className: ITEM_CLASS,
                        context: this.kernel.id,
                        open: () => void commands.execute(open, { name, path, type }),
                        icon: () => type === 'console'
                            ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.consoleIcon
                            : type === 'notebook'
                                ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.notebookIcon
                                : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.jupyterIcon,
                        label: () => name,
                        labelTitle: () => path
                    });
                }
            }
            return children;
        }
        shutdown() {
            return this.kernels.shutdown(this.kernel.id);
        }
        icon() {
            const { spec } = this;
            if (!spec || !spec.resources) {
                return _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.jupyterIcon;
            }
            return (spec.resources['logo-svg'] ||
                spec.resources['logo-64x64'] ||
                spec.resources['logo-32x32']);
        }
        label() {
            const { kernel, spec } = this;
            return (spec === null || spec === void 0 ? void 0 : spec.display_name) || kernel.name;
        }
        labelTitle() {
            var _a;
            const { trans } = this;
            const { id } = this.kernel;
            const title = [`${this.label()}: ${id}`];
            for (const session of this.sessions.running()) {
                if (this.kernel.id === ((_a = session.kernel) === null || _a === void 0 ? void 0 : _a.id)) {
                    const { path, type } = session;
                    title.push(trans.__(`%1\nPath: %2`, type, path));
                }
            }
            return title.join('\n\n');
        }
    }
    Private.RunningKernel = RunningKernel;
    Private.runningChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal({});
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/running-extension/lib/opentabs.js":
/*!*****************************************************!*\
  !*** ../packages/running-extension/lib/opentabs.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "addOpenTabsSessionManager": () => (/* binding */ addOpenTabsSessionManager)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A class used to consolidate the signals used to rerender the open tabs section.
 */
class OpenTabsSignaler {
    constructor(labShell) {
        this._tabsChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._widgets = [];
        this._labShell = labShell;
        this._labShell.layoutModified.connect(this._emitTabsChanged, this);
    }
    /**
     * A signal that fires when the open tabs section should be rerendered.
     */
    get tabsChanged() {
        return this._tabsChanged;
    }
    /**
     * Add a widget to watch for title changing.
     *
     * @param widget A widget whose title may change.
     */
    addWidget(widget) {
        widget.title.changed.connect(this._emitTabsChanged, this);
        this._widgets.push(widget);
    }
    /**
     * Emit the main signal that indicates the open tabs should be rerendered.
     */
    _emitTabsChanged() {
        this._widgets.forEach(widget => {
            widget.title.changed.disconnect(this._emitTabsChanged, this);
        });
        this._widgets = [];
        this._tabsChanged.emit(void 0);
    }
}
/**
 * Add the open tabs section to the running panel.
 *
 * @param managers - The IRunningSessionManagers used to register this section.
 * @param translator - The translator to use.
 * @param labShell - The ILabShell.
 */
function addOpenTabsSessionManager(managers, translator, labShell) {
    const signaler = new OpenTabsSignaler(labShell);
    const trans = translator.load('jupyterlab');
    managers.add({
        name: trans.__('Open Tabs'),
        running: () => {
            return Array.from(labShell.widgets('main')).map((widget) => {
                signaler.addWidget(widget);
                return new OpenTab(widget);
            });
        },
        shutdownAll: () => {
            for (const widget of labShell.widgets('main')) {
                widget.close();
            }
        },
        refreshRunning: () => {
            return void 0;
        },
        runningChanged: signaler.tabsChanged,
        shutdownLabel: trans.__('Close'),
        shutdownAllLabel: trans.__('Close All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to close all open tabs?')
    });
    class OpenTab {
        constructor(widget) {
            this._widget = widget;
        }
        open() {
            labShell.activateById(this._widget.id);
        }
        shutdown() {
            this._widget.close();
        }
        icon() {
            const widgetIcon = this._widget.title.icon;
            return widgetIcon instanceof _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.LabIcon ? widgetIcon : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.fileIcon;
        }
        label() {
            return this._widget.title.label;
        }
        labelTitle() {
            let labelTitle;
            if (this._widget instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.DocumentWidget) {
                labelTitle = this._widget.context.path;
            }
            else {
                labelTitle = this._widget.title.label;
            }
            return labelTitle;
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfcnVubmluZy1leHRlbnNpb25fbGliX2luZGV4X2pzLXBhY2thZ2VzX3J1bm5pbmctZXh0ZW5zaW9uX2xpYl9rZXJuZWxzX2pzLjJlMmI5NTMyZjRiYjhjMjIxYTMzLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTzhCO0FBS0o7QUFDeUI7QUFDRTtBQUNHO0FBQ0o7QUFFdkQ7O0dBRUc7QUFDSSxJQUFVLFVBQVUsQ0FNMUI7QUFORCxXQUFpQixVQUFVO0lBQ1osMkJBQWdCLEdBQUcsNEJBQTRCLENBQUM7SUFDaEQsNEJBQWlCLEdBQUcsNkJBQTZCLENBQUM7SUFDbEQsNEJBQWlCLEdBQUcsNkJBQTZCLENBQUM7SUFDbEQseUJBQWMsR0FBRywwQkFBMEIsQ0FBQztJQUM1QyxvQkFBUyxHQUFHLG9CQUFvQixDQUFDO0FBQ2hELENBQUMsRUFOZ0IsVUFBVSxLQUFWLFVBQVUsUUFNMUI7QUFFRDs7R0FFRztBQUNILE1BQU0sTUFBTSxHQUFtRDtJQUM3RCxRQUFRO0lBQ1IsRUFBRSxFQUFFLHNDQUFzQztJQUMxQyxXQUFXLEVBQUUsd0NBQXdDO0lBQ3JELFFBQVEsRUFBRSx3RUFBdUI7SUFDakMsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUUsQ0FBQyxvRUFBZSxFQUFFLDhEQUFTLENBQUM7SUFDdEMsU0FBUyxFQUFFLElBQUk7Q0FDaEIsQ0FBQztBQUVGOztHQUVHO0FBQ0gsaUVBQWUsTUFBTSxFQUFDO0FBRXRCOztHQUVHO0FBQ0gsU0FBUyxRQUFRLENBQ2YsR0FBb0IsRUFDcEIsVUFBdUIsRUFDdkIsUUFBZ0MsRUFDaEMsUUFBMEI7SUFFMUIsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUM1QyxNQUFNLHNCQUFzQixHQUFHLElBQUksdUVBQXNCLEVBQUUsQ0FBQztJQUM1RCxN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Q0FBQyxFQUFFLENBQUMsQ0FBQztRQUN6QyxDQUFDO1FBQ0QsUUFBUTtZQUNOLElBQUksQ0FBQyxPQUFPLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDdkIsQ0FBQztRQUNELElBQUk7WUFDRixNQUFNLFVBQVUsR0FBRyxJQUFJLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUM7WUFDM0MsT0FBTyxVQUFVLFlBQVksOERBQU8sQ0FBQyxDQUFDLENBQUMsVUFBVSxDQUFDLENBQUMsQ0FBQywrREFBUSxDQUFDO1FBQy9ELENBQUM7UUFDRCxLQUFLO1lBQ0gsT0FBTyxJQUFJLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxLQUFLLENBQUM7UUFDbEMsQ0FBQztRQUNELFVBQVU7WUFDUixJQUFJLFVBQWtCLENBQUM7WUFDdkIsSUFBSSxJQUFJLENBQUMsT0FBTyxZQUFZLG1FQUFjLEVBQUU7Z0JBQzFDLFVBQVUsR0FBRyxJQUFJLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUM7YUFDeEM7aUJBQU07Z0JBQ0wsVUFBVSxHQUFHLElBQUksQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLEtBQUssQ0FBQzthQUN2QztZQUNELE9BQU8sVUFBVSxDQUFDO1FBQ3BCLENBQUM7S0FHRjtBQUNILENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcnVubmluZy1leHRlbnNpb24vc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9ydW5uaW5nLWV4dGVuc2lvbi9zcmMva2VybmVscy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcnVubmluZy1leHRlbnNpb24vc3JjL29wZW50YWJzLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHJ1bm5pbmctZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLFxuICBSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLFxuICBSdW5uaW5nU2Vzc2lvbnNcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcnVubmluZyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IHJ1bm5pbmdJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBhZGRLZXJuZWxSdW5uaW5nU2Vzc2lvbk1hbmFnZXIgfSBmcm9tICcuL2tlcm5lbHMnO1xuaW1wb3J0IHsgYWRkT3BlblRhYnNTZXNzaW9uTWFuYWdlciB9IGZyb20gJy4vb3BlbnRhYnMnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBydW5uaW5nIHBsdWdpbi5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IGtlcm5lbE5ld0NvbnNvbGUgPSAncnVubmluZzprZXJuZWwtbmV3LWNvbnNvbGUnO1xuICBleHBvcnQgY29uc3Qga2VybmVsTmV3Tm90ZWJvb2sgPSAncnVubmluZzprZXJuZWwtbmV3LW5vdGVib29rJztcbiAgZXhwb3J0IGNvbnN0IGtlcm5lbE9wZW5TZXNzaW9uID0gJ3J1bm5pbmc6a2VybmVsLW9wZW4tc2Vzc2lvbic7XG4gIGV4cG9ydCBjb25zdCBrZXJuZWxTaHV0RG93biA9ICdydW5uaW5nOmtlcm5lbC1zaHV0LWRvd24nO1xuICBleHBvcnQgY29uc3Qgc2hvd1BhbmVsID0gJ3J1bm5pbmc6c2hvdy1wYW5lbCc7XG59XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgcnVubmluZyBzZXNzaW9ucyBleHRlbnNpb24uXG4gKi9cbmNvbnN0IHBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzPiA9IHtcbiAgYWN0aXZhdGUsXG4gIGlkOiAnQGp1cHl0ZXJsYWIvcnVubmluZy1leHRlbnNpb246cGx1Z2luJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgcnVubmluZyBzZXNzaW9uIG1hbmFnZXJzLicsXG4gIHByb3ZpZGVzOiBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycyxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxheW91dFJlc3RvcmVyLCBJTGFiU2hlbGxdLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW4gYXMgZGVmYXVsdC5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2luO1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBydW5uaW5nIHBsdWdpbi5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsXG4pOiBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycyB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHJ1bm5pbmdTZXNzaW9uTWFuYWdlcnMgPSBuZXcgUnVubmluZ1Nlc3Npb25NYW5hZ2VycygpO1xuICBjb25zdCBydW5uaW5nID0gbmV3IFJ1bm5pbmdTZXNzaW9ucyhydW5uaW5nU2Vzc2lvbk1hbmFnZXJzLCB0cmFuc2xhdG9yKTtcbiAgcnVubmluZy5pZCA9ICdqcC1ydW5uaW5nLXNlc3Npb25zJztcbiAgcnVubmluZy50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ1J1bm5pbmcgVGVybWluYWxzIGFuZCBLZXJuZWxzJyk7XG4gIHJ1bm5pbmcudGl0bGUuaWNvbiA9IHJ1bm5pbmdJY29uO1xuICBydW5uaW5nLm5vZGUuc2V0QXR0cmlidXRlKCdyb2xlJywgJ3JlZ2lvbicpO1xuICBydW5uaW5nLm5vZGUuc2V0QXR0cmlidXRlKCdhcmlhLWxhYmVsJywgdHJhbnMuX18oJ1J1bm5pbmcgU2Vzc2lvbnMgc2VjdGlvbicpKTtcblxuICAvLyBMZXQgdGhlIGFwcGxpY2F0aW9uIHJlc3RvcmVyIHRyYWNrIHRoZSBydW5uaW5nIHBhbmVsIGZvciByZXN0b3JhdGlvbiBvZlxuICAvLyBhcHBsaWNhdGlvbiBzdGF0ZSAoZS5nLiBzZXR0aW5nIHRoZSBydW5uaW5nIHBhbmVsIGFzIHRoZSBjdXJyZW50IHNpZGUgYmFyXG4gIC8vIHdpZGdldCkuXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIHJlc3RvcmVyLmFkZChydW5uaW5nLCAncnVubmluZy1zZXNzaW9ucycpO1xuICB9XG4gIGlmIChsYWJTaGVsbCkge1xuICAgIGFkZE9wZW5UYWJzU2Vzc2lvbk1hbmFnZXIocnVubmluZ1Nlc3Npb25NYW5hZ2VycywgdHJhbnNsYXRvciwgbGFiU2hlbGwpO1xuICB9XG4gIHZvaWQgYWRkS2VybmVsUnVubmluZ1Nlc3Npb25NYW5hZ2VyKHJ1bm5pbmdTZXNzaW9uTWFuYWdlcnMsIHRyYW5zbGF0b3IsIGFwcCk7XG4gIC8vIFJhbmsgaGFzIGJlZW4gY2hvc2VuIHNvbWV3aGF0IGFyYml0cmFyaWx5IHRvIGdpdmUgcHJpb3JpdHkgdG8gdGhlIHJ1bm5pbmdcbiAgLy8gc2Vzc2lvbnMgd2lkZ2V0IGluIHRoZSBzaWRlYmFyLlxuICBhcHAuc2hlbGwuYWRkKHJ1bm5pbmcsICdsZWZ0JywgeyByYW5rOiAyMDAsIHR5cGU6ICdTZXNzaW9ucyBhbmQgVGFicycgfSk7XG5cbiAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaG93UGFuZWwsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nlc3Npb25zIGFuZCBUYWJzJyksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgYXBwLnNoZWxsLmFjdGl2YXRlQnlJZChydW5uaW5nLmlkKTtcbiAgICB9XG4gIH0pO1xuXG4gIHJldHVybiBydW5uaW5nU2Vzc2lvbk1hbmFnZXJzO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBKdXB5dGVyRnJvbnRFbmQgfSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBQYXRoRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcbmltcG9ydCB7IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLCBJUnVubmluZ1Nlc3Npb25zIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcnVubmluZyc7XG5pbXBvcnQgeyBLZXJuZWwsIEtlcm5lbFNwZWMsIFNlc3Npb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7XG4gIGNsb3NlSWNvbixcbiAgY29uc29sZUljb24sXG4gIElEaXNwb3NhYmxlTWVudUl0ZW0sXG4gIGp1cHl0ZXJJY29uLFxuICBMYWJJY29uLFxuICBub3RlYm9va0ljb24sXG4gIFJhbmtlZE1lbnVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBDb21tYW5kUmVnaXN0cnkgfSBmcm9tICdAbHVtaW5vL2NvbW1hbmRzJztcbmltcG9ydCB7IFRocm90dGxlciB9IGZyb20gJ0BsdW1pbm8vcG9sbGluZyc7XG5pbXBvcnQgeyBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBDb21tYW5kSURzIH0gZnJvbSAnLic7XG5cbmNvbnN0IElURU1fQ0xBU1MgPSAnanAtbW9kLWtlcm5lbCc7XG5cbi8qKlxuICogQWRkIHRoZSBydW5uaW5nIGtlcm5lbCBtYW5hZ2VyIChub3RlYm9va3MgJiBjb25zb2xlcykgdG8gdGhlIHJ1bm5pbmcgcGFuZWwuXG4gKi9cbmV4cG9ydCBhc3luYyBmdW5jdGlvbiBhZGRLZXJuZWxSdW5uaW5nU2Vzc2lvbk1hbmFnZXIoXG4gIG1hbmFnZXJzOiBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycyxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIGFwcDogSnVweXRlckZyb250RW5kXG4pOiBQcm9taXNlPHZvaWQ+IHtcbiAgY29uc3QgeyBjb21tYW5kcywgY29udGV4dE1lbnUsIHNlcnZpY2VNYW5hZ2VyIH0gPSBhcHA7XG4gIGNvbnN0IHsga2VybmVscywga2VybmVsc3BlY3MsIHNlc3Npb25zIH0gPSBzZXJ2aWNlTWFuYWdlcjtcbiAgY29uc3QgeyBydW5uaW5nQ2hhbmdlZCwgUnVubmluZ0tlcm5lbCB9ID0gUHJpdmF0ZTtcbiAgY29uc3QgdGhyb3R0bGVyID0gbmV3IFRocm90dGxlcigoKSA9PiBydW5uaW5nQ2hhbmdlZC5lbWl0KHVuZGVmaW5lZCksIDEwMCk7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgLy8gVGhyb3R0bGUgc2lnbmFsIGVtaXNzaW9ucyBmcm9tIHRoZSBrZXJuZWwgYW5kIHNlc3Npb24gbWFuYWdlcnMuXG4gIGtlcm5lbHMucnVubmluZ0NoYW5nZWQuY29ubmVjdCgoKSA9PiB2b2lkIHRocm90dGxlci5pbnZva2UoKSk7XG4gIHNlc3Npb25zLnJ1bm5pbmdDaGFuZ2VkLmNvbm5lY3QoKCkgPT4gdm9pZCB0aHJvdHRsZXIuaW52b2tlKCkpO1xuXG4gIC8vIFdhaXQgdW50aWwgdGhlIHJlbGV2YW50IHNlcnZpY2VzIGFyZSByZWFkeS5cbiAgYXdhaXQgUHJvbWlzZS5hbGwoW2tlcm5lbHMucmVhZHksIGtlcm5lbHNwZWNzLnJlYWR5LCBzZXNzaW9ucy5yZWFkeV0pO1xuXG4gIC8vIEFkZCB0aGUga2VybmVscyBwYW5lIHRvIHRoZSBydW5uaW5nIHNpZGViYXIuXG4gIG1hbmFnZXJzLmFkZCh7XG4gICAgbmFtZTogdHJhbnMuX18oJ0tlcm5lbHMnKSxcbiAgICBydW5uaW5nOiAoKSA9PlxuICAgICAgQXJyYXkuZnJvbShrZXJuZWxzLnJ1bm5pbmcoKSkubWFwKFxuICAgICAgICBrZXJuZWwgPT5cbiAgICAgICAgICBuZXcgUnVubmluZ0tlcm5lbCh7XG4gICAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICAgIGtlcm5lbCxcbiAgICAgICAgICAgIGtlcm5lbHMsXG4gICAgICAgICAgICBzZXNzaW9ucyxcbiAgICAgICAgICAgIHNwZWM6IGtlcm5lbHNwZWNzLnNwZWNzPy5rZXJuZWxzcGVjc1trZXJuZWwubmFtZV0sXG4gICAgICAgICAgICB0cmFuc1xuICAgICAgICAgIH0pXG4gICAgICApLFxuICAgIHNodXRkb3duQWxsOiAoKSA9PiBrZXJuZWxzLnNodXRkb3duQWxsKCksXG4gICAgcmVmcmVzaFJ1bm5pbmc6ICgpID0+XG4gICAgICBQcm9taXNlLmFsbChba2VybmVscy5yZWZyZXNoUnVubmluZygpLCBzZXNzaW9ucy5yZWZyZXNoUnVubmluZygpXSksXG4gICAgcnVubmluZ0NoYW5nZWQsXG4gICAgc2h1dGRvd25MYWJlbDogdHJhbnMuX18oJ1NodXQgRG93biBLZXJuZWwnKSxcbiAgICBzaHV0ZG93bkFsbExhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duIEFsbCcpLFxuICAgIHNodXRkb3duQWxsQ29uZmlybWF0aW9uVGV4dDogdHJhbnMuX18oXG4gICAgICAnQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIHBlcm1hbmVudGx5IHNodXQgZG93biBhbGwgcnVubmluZyBrZXJuZWxzPydcbiAgICApXG4gIH0pO1xuXG4gIC8vIEFkZCBydW5uaW5nIGtlcm5lbHMgY29tbWFuZHMgdG8gdGhlIHJlZ2lzdHJ5LlxuICBjb25zdCB0ZXN0ID0gKG5vZGU6IEhUTUxFbGVtZW50KSA9PiBub2RlLmNsYXNzTGlzdC5jb250YWlucyhJVEVNX0NMQVNTKTtcbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmtlcm5lbE5ld0NvbnNvbGUsIHtcbiAgICBpY29uOiBjb25zb2xlSWNvbixcbiAgICBsYWJlbDogdHJhbnMuX18oJ05ldyBDb25zb2xlIGZvciBLZXJuZWwnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IG5vZGUgPSBhcHAuY29udGV4dE1lbnVIaXRUZXN0KHRlc3QpO1xuICAgICAgY29uc3QgaWQgPSAoYXJncy5pZCBhcyBzdHJpbmcpID8/IG5vZGU/LmRhdGFzZXRbJ2NvbnRleHQnXTtcbiAgICAgIGlmIChpZCkge1xuICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnY29uc29sZTpjcmVhdGUnLCB7IGtlcm5lbFByZWZlcmVuY2U6IHsgaWQgfSB9KTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMua2VybmVsTmV3Tm90ZWJvb2ssIHtcbiAgICBpY29uOiBub3RlYm9va0ljb24sXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdOZXcgTm90ZWJvb2sgZm9yIEtlcm5lbCcpLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3Qgbm9kZSA9IGFwcC5jb250ZXh0TWVudUhpdFRlc3QodGVzdCk7XG4gICAgICBjb25zdCBpZCA9IChhcmdzLmlkIGFzIHN0cmluZykgPz8gbm9kZT8uZGF0YXNldFsnY29udGV4dCddO1xuICAgICAgaWYgKGlkKSB7XG4gICAgICAgIHJldHVybiBjb21tYW5kcy5leGVjdXRlKCdub3RlYm9vazpjcmVhdGUtbmV3JywgeyBrZXJuZWxJZDogaWQgfSk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmtlcm5lbE9wZW5TZXNzaW9uLCB7XG4gICAgaWNvbjogYXJncyA9PlxuICAgICAgYXJncy50eXBlID09PSAnY29uc29sZSdcbiAgICAgICAgPyBjb25zb2xlSWNvblxuICAgICAgICA6IGFyZ3MudHlwZSA9PT0gJ25vdGVib29rJ1xuICAgICAgICA/IG5vdGVib29rSWNvblxuICAgICAgICA6IHVuZGVmaW5lZCxcbiAgICBpc0VuYWJsZWQ6ICh7IHBhdGgsIHR5cGUgfSkgPT4gISF0eXBlIHx8IHBhdGggIT09IHVuZGVmaW5lZCxcbiAgICBsYWJlbDogKHsgbmFtZSwgcGF0aCB9KSA9PlxuICAgICAgKG5hbWUgYXMgc3RyaW5nKSB8fFxuICAgICAgUGF0aEV4dC5iYXNlbmFtZSgocGF0aCBhcyBzdHJpbmcpIHx8IHRyYW5zLl9fKCdVbmtub3duIFNlc3Npb24nKSksXG4gICAgZXhlY3V0ZTogKHsgcGF0aCwgdHlwZSB9KSA9PiB7XG4gICAgICBpZiAoIXR5cGUgfHwgcGF0aCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGNvbW1hbmQgPSB0eXBlID09PSAnY29uc29sZScgPyAnY29uc29sZTpvcGVuJyA6ICdkb2NtYW5hZ2VyOm9wZW4nO1xuICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoY29tbWFuZCwgeyBwYXRoIH0pO1xuICAgIH1cbiAgfSk7XG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5rZXJuZWxTaHV0RG93biwge1xuICAgIGljb246IGNsb3NlSWNvbixcbiAgICBsYWJlbDogdHJhbnMuX18oJ1NodXQgRG93biBLZXJuZWwnKSxcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IG5vZGUgPSBhcHAuY29udGV4dE1lbnVIaXRUZXN0KHRlc3QpO1xuICAgICAgY29uc3QgaWQgPSAoYXJncy5pZCBhcyBzdHJpbmcpID8/IG5vZGU/LmRhdGFzZXRbJ2NvbnRleHQnXTtcbiAgICAgIGlmIChpZCkge1xuICAgICAgICByZXR1cm4ga2VybmVscy5zaHV0ZG93bihpZCk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb25zdCBzZXNzaW9uc0l0ZW1zOiBJRGlzcG9zYWJsZU1lbnVJdGVtW10gPSBbXTtcblxuICAvLyBQb3B1bGF0ZSBjb25uZWN0ZWQgc2Vzc2lvbnMgc3VibWVudSB3aGVuIGNvbnRleHQgbWVudSBpcyBvcGVuZWQuXG4gIGNvbnRleHRNZW51Lm9wZW5lZC5jb25uZWN0KGFzeW5jICgpID0+IHtcbiAgICBjb25zdCBzdWJtZW51ID1cbiAgICAgIChjb250ZXh0TWVudS5tZW51Lml0ZW1zLmZpbmQoXG4gICAgICAgIGl0ZW0gPT5cbiAgICAgICAgICBpdGVtLnR5cGUgPT09ICdzdWJtZW51JyAmJlxuICAgICAgICAgIGl0ZW0uc3VibWVudT8uaWQgPT09ICdqcC1jb250ZXh0bWVudS1jb25uZWN0ZWQtc2Vzc2lvbnMnXG4gICAgICApPy5zdWJtZW51IGFzIFJhbmtlZE1lbnUpID8/IG51bGw7XG5cbiAgICBpZiAoIXN1Ym1lbnUpIHtcbiAgICAgIC8vIEJhaWwgZWFybHkgaWYgdGhlIGNvbm5lY3RlZCBzZXNzaW9uIG1lbnUgaXMgbm90IGZvdW5kXG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gRW1wdHkgdGhlIGNvbm5lY3RlZCBzZXNzaW9ucyBzdWJtZW51LlxuICAgIHNlc3Npb25zSXRlbXMuZm9yRWFjaChpdGVtID0+IGl0ZW0uZGlzcG9zZSgpKTtcbiAgICBzZXNzaW9uc0l0ZW1zLmxlbmd0aCA9IDA7XG4gICAgc3VibWVudS5jbGVhckl0ZW1zKCk7XG5cbiAgICBjb25zdCBub2RlID0gYXBwLmNvbnRleHRNZW51SGl0VGVzdCh0ZXN0KTtcbiAgICBjb25zdCBpZCA9IG5vZGU/LmRhdGFzZXRbJ2NvbnRleHQnXTtcbiAgICBpZiAoIWlkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgLy8gUG9wdWxhdGUgdGhlIHN1Ym1lbnUgd2l0aCBzZXNzaW9ucyBjb25uZWN0ZWQgdG8gdGhpcyBrZXJuZWwuXG4gICAgY29uc3QgY29tbWFuZCA9IENvbW1hbmRJRHMua2VybmVsT3BlblNlc3Npb247XG4gICAgZm9yIChjb25zdCBzZXNzaW9uIG9mIHNlc3Npb25zLnJ1bm5pbmcoKSkge1xuICAgICAgaWYgKGlkID09PSBzZXNzaW9uLmtlcm5lbD8uaWQpIHtcbiAgICAgICAgY29uc3QgeyBuYW1lLCBwYXRoLCB0eXBlIH0gPSBzZXNzaW9uO1xuICAgICAgICBzZXNzaW9uc0l0ZW1zLnB1c2goXG4gICAgICAgICAgc3VibWVudS5hZGRJdGVtKHsgY29tbWFuZCwgYXJnczogeyBuYW1lLCBwYXRoLCB0eXBlIH0gfSlcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xufVxuXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGV4cG9ydCBjbGFzcyBSdW5uaW5nS2VybmVsIGltcGxlbWVudHMgSVJ1bm5pbmdTZXNzaW9ucy5JUnVubmluZ0l0ZW0ge1xuICAgIGNvbnN0cnVjdG9yKG9wdGlvbnM6IFJ1bm5pbmdLZXJuZWwuSU9wdGlvbnMpIHtcbiAgICAgIHRoaXMuY2xhc3NOYW1lID0gSVRFTV9DTEFTUztcbiAgICAgIHRoaXMuY29tbWFuZHMgPSBvcHRpb25zLmNvbW1hbmRzO1xuICAgICAgdGhpcy5rZXJuZWwgPSBvcHRpb25zLmtlcm5lbDtcbiAgICAgIHRoaXMuY29udGV4dCA9IHRoaXMua2VybmVsLmlkO1xuICAgICAgdGhpcy5rZXJuZWxzID0gb3B0aW9ucy5rZXJuZWxzO1xuICAgICAgdGhpcy5zZXNzaW9ucyA9IG9wdGlvbnMuc2Vzc2lvbnM7XG4gICAgICB0aGlzLnNwZWMgPSBvcHRpb25zLnNwZWMgfHwgbnVsbDtcbiAgICAgIHRoaXMudHJhbnMgPSBvcHRpb25zLnRyYW5zO1xuICAgIH1cblxuICAgIHJlYWRvbmx5IGNsYXNzTmFtZTogc3RyaW5nO1xuXG4gICAgcmVhZG9ubHkgY29udGV4dDogc3RyaW5nO1xuXG4gICAgcmVhZG9ubHkgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeTtcblxuICAgIHJlYWRvbmx5IGtlcm5lbDogS2VybmVsLklNb2RlbDtcblxuICAgIHJlYWRvbmx5IGtlcm5lbHM6IEtlcm5lbC5JTWFuYWdlcjtcblxuICAgIHJlYWRvbmx5IHNlc3Npb25zOiBTZXNzaW9uLklNYW5hZ2VyO1xuXG4gICAgcmVhZG9ubHkgc3BlYzogS2VybmVsU3BlYy5JU3BlY01vZGVsIHwgbnVsbDtcblxuICAgIHJlYWRvbmx5IHRyYW5zOiBJUmVuZGVyTWltZS5UcmFuc2xhdGlvbkJ1bmRsZTtcblxuICAgIGdldCBjaGlsZHJlbigpOiBJUnVubmluZ1Nlc3Npb25zLklSdW5uaW5nSXRlbVtdIHtcbiAgICAgIGNvbnN0IGNoaWxkcmVuOiBJUnVubmluZ1Nlc3Npb25zLklSdW5uaW5nSXRlbVtdID0gW107XG4gICAgICBjb25zdCBvcGVuID0gQ29tbWFuZElEcy5rZXJuZWxPcGVuU2Vzc2lvbjtcbiAgICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IHRoaXM7XG4gICAgICBmb3IgKGNvbnN0IHNlc3Npb24gb2YgdGhpcy5zZXNzaW9ucy5ydW5uaW5nKCkpIHtcbiAgICAgICAgaWYgKHRoaXMua2VybmVsLmlkID09PSBzZXNzaW9uLmtlcm5lbD8uaWQpIHtcbiAgICAgICAgICBjb25zdCB7IG5hbWUsIHBhdGgsIHR5cGUgfSA9IHNlc3Npb247XG4gICAgICAgICAgY2hpbGRyZW4ucHVzaCh7XG4gICAgICAgICAgICBjbGFzc05hbWU6IElURU1fQ0xBU1MsXG4gICAgICAgICAgICBjb250ZXh0OiB0aGlzLmtlcm5lbC5pZCxcbiAgICAgICAgICAgIG9wZW46ICgpID0+IHZvaWQgY29tbWFuZHMuZXhlY3V0ZShvcGVuLCB7IG5hbWUsIHBhdGgsIHR5cGUgfSksXG4gICAgICAgICAgICBpY29uOiAoKSA9PlxuICAgICAgICAgICAgICB0eXBlID09PSAnY29uc29sZSdcbiAgICAgICAgICAgICAgICA/IGNvbnNvbGVJY29uXG4gICAgICAgICAgICAgICAgOiB0eXBlID09PSAnbm90ZWJvb2snXG4gICAgICAgICAgICAgICAgPyBub3RlYm9va0ljb25cbiAgICAgICAgICAgICAgICA6IGp1cHl0ZXJJY29uLFxuICAgICAgICAgICAgbGFiZWw6ICgpID0+IG5hbWUsXG4gICAgICAgICAgICBsYWJlbFRpdGxlOiAoKSA9PiBwYXRoXG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHJldHVybiBjaGlsZHJlbjtcbiAgICB9XG5cbiAgICBzaHV0ZG93bigpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAgIHJldHVybiB0aGlzLmtlcm5lbHMuc2h1dGRvd24odGhpcy5rZXJuZWwuaWQpO1xuICAgIH1cblxuICAgIGljb24oKTogTGFiSWNvbiB8IHN0cmluZyB7XG4gICAgICBjb25zdCB7IHNwZWMgfSA9IHRoaXM7XG4gICAgICBpZiAoIXNwZWMgfHwgIXNwZWMucmVzb3VyY2VzKSB7XG4gICAgICAgIHJldHVybiBqdXB5dGVySWNvbjtcbiAgICAgIH1cbiAgICAgIHJldHVybiAoXG4gICAgICAgIHNwZWMucmVzb3VyY2VzWydsb2dvLXN2ZyddIHx8XG4gICAgICAgIHNwZWMucmVzb3VyY2VzWydsb2dvLTY0eDY0J10gfHxcbiAgICAgICAgc3BlYy5yZXNvdXJjZXNbJ2xvZ28tMzJ4MzInXVxuICAgICAgKTtcbiAgICB9XG5cbiAgICBsYWJlbCgpOiBzdHJpbmcge1xuICAgICAgY29uc3QgeyBrZXJuZWwsIHNwZWMgfSA9IHRoaXM7XG4gICAgICByZXR1cm4gc3BlYz8uZGlzcGxheV9uYW1lIHx8IGtlcm5lbC5uYW1lO1xuICAgIH1cblxuICAgIGxhYmVsVGl0bGUoKTogc3RyaW5nIHtcbiAgICAgIGNvbnN0IHsgdHJhbnMgfSA9IHRoaXM7XG4gICAgICBjb25zdCB7IGlkIH0gPSB0aGlzLmtlcm5lbDtcbiAgICAgIGNvbnN0IHRpdGxlID0gW2Ake3RoaXMubGFiZWwoKX06ICR7aWR9YF07XG4gICAgICBmb3IgKGNvbnN0IHNlc3Npb24gb2YgdGhpcy5zZXNzaW9ucy5ydW5uaW5nKCkpIHtcbiAgICAgICAgaWYgKHRoaXMua2VybmVsLmlkID09PSBzZXNzaW9uLmtlcm5lbD8uaWQpIHtcbiAgICAgICAgICBjb25zdCB7IHBhdGgsIHR5cGUgfSA9IHNlc3Npb247XG4gICAgICAgICAgdGl0bGUucHVzaCh0cmFucy5fXyhgJTFcXG5QYXRoOiAlMmAsIHR5cGUsIHBhdGgpKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgcmV0dXJuIHRpdGxlLmpvaW4oJ1xcblxcbicpO1xuICAgIH1cbiAgfVxuXG4gIGV4cG9ydCBuYW1lc3BhY2UgUnVubmluZ0tlcm5lbCB7XG4gICAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5O1xuICAgICAga2VybmVsOiBLZXJuZWwuSU1vZGVsO1xuICAgICAga2VybmVsczogS2VybmVsLklNYW5hZ2VyO1xuICAgICAgc2Vzc2lvbnM6IFNlc3Npb24uSU1hbmFnZXI7XG4gICAgICBzcGVjPzogS2VybmVsU3BlYy5JU3BlY01vZGVsO1xuICAgICAgdHJhbnM6IElSZW5kZXJNaW1lLlRyYW5zbGF0aW9uQnVuZGxlO1xuICAgIH1cbiAgfVxuXG4gIGV4cG9ydCBjb25zdCBydW5uaW5nQ2hhbmdlZCA9IG5ldyBTaWduYWw8dW5rbm93biwgdW5rbm93bj4oe30pO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJTGFiU2hlbGwgfSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLCBJUnVubmluZ1Nlc3Npb25zIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcnVubmluZyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGZpbGVJY29uLCBMYWJJY29uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIEEgY2xhc3MgdXNlZCB0byBjb25zb2xpZGF0ZSB0aGUgc2lnbmFscyB1c2VkIHRvIHJlcmVuZGVyIHRoZSBvcGVuIHRhYnMgc2VjdGlvbi5cbiAqL1xuY2xhc3MgT3BlblRhYnNTaWduYWxlciB7XG4gIGNvbnN0cnVjdG9yKGxhYlNoZWxsOiBJTGFiU2hlbGwpIHtcbiAgICB0aGlzLl9sYWJTaGVsbCA9IGxhYlNoZWxsO1xuICAgIHRoaXMuX2xhYlNoZWxsLmxheW91dE1vZGlmaWVkLmNvbm5lY3QodGhpcy5fZW1pdFRhYnNDaGFuZ2VkLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCB0aGF0IGZpcmVzIHdoZW4gdGhlIG9wZW4gdGFicyBzZWN0aW9uIHNob3VsZCBiZSByZXJlbmRlcmVkLlxuICAgKi9cbiAgZ2V0IHRhYnNDaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl90YWJzQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSB3aWRnZXQgdG8gd2F0Y2ggZm9yIHRpdGxlIGNoYW5naW5nLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IEEgd2lkZ2V0IHdob3NlIHRpdGxlIG1heSBjaGFuZ2UuXG4gICAqL1xuICBhZGRXaWRnZXQod2lkZ2V0OiBXaWRnZXQpOiB2b2lkIHtcbiAgICB3aWRnZXQudGl0bGUuY2hhbmdlZC5jb25uZWN0KHRoaXMuX2VtaXRUYWJzQ2hhbmdlZCwgdGhpcyk7XG4gICAgdGhpcy5fd2lkZ2V0cy5wdXNoKHdpZGdldCk7XG4gIH1cblxuICAvKipcbiAgICogRW1pdCB0aGUgbWFpbiBzaWduYWwgdGhhdCBpbmRpY2F0ZXMgdGhlIG9wZW4gdGFicyBzaG91bGQgYmUgcmVyZW5kZXJlZC5cbiAgICovXG4gIHByaXZhdGUgX2VtaXRUYWJzQ2hhbmdlZCgpOiB2b2lkIHtcbiAgICB0aGlzLl93aWRnZXRzLmZvckVhY2god2lkZ2V0ID0+IHtcbiAgICAgIHdpZGdldC50aXRsZS5jaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5fZW1pdFRhYnNDaGFuZ2VkLCB0aGlzKTtcbiAgICB9KTtcbiAgICB0aGlzLl93aWRnZXRzID0gW107XG4gICAgdGhpcy5fdGFic0NoYW5nZWQuZW1pdCh2b2lkIDApO1xuICB9XG5cbiAgcHJpdmF0ZSBfdGFic0NoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIHZvaWQ+KHRoaXMpO1xuICBwcml2YXRlIF9sYWJTaGVsbDogSUxhYlNoZWxsO1xuICBwcml2YXRlIF93aWRnZXRzOiBXaWRnZXRbXSA9IFtdO1xufVxuXG4vKipcbiAqIEFkZCB0aGUgb3BlbiB0YWJzIHNlY3Rpb24gdG8gdGhlIHJ1bm5pbmcgcGFuZWwuXG4gKlxuICogQHBhcmFtIG1hbmFnZXJzIC0gVGhlIElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzIHVzZWQgdG8gcmVnaXN0ZXIgdGhpcyBzZWN0aW9uLlxuICogQHBhcmFtIHRyYW5zbGF0b3IgLSBUaGUgdHJhbnNsYXRvciB0byB1c2UuXG4gKiBAcGFyYW0gbGFiU2hlbGwgLSBUaGUgSUxhYlNoZWxsLlxuICovXG5leHBvcnQgZnVuY3Rpb24gYWRkT3BlblRhYnNTZXNzaW9uTWFuYWdlcihcbiAgbWFuYWdlcnM6IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgbGFiU2hlbGw6IElMYWJTaGVsbFxuKTogdm9pZCB7XG4gIGNvbnN0IHNpZ25hbGVyID0gbmV3IE9wZW5UYWJzU2lnbmFsZXIobGFiU2hlbGwpO1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gIG1hbmFnZXJzLmFkZCh7XG4gICAgbmFtZTogdHJhbnMuX18oJ09wZW4gVGFicycpLFxuICAgIHJ1bm5pbmc6ICgpID0+IHtcbiAgICAgIHJldHVybiBBcnJheS5mcm9tKGxhYlNoZWxsLndpZGdldHMoJ21haW4nKSkubWFwKCh3aWRnZXQ6IFdpZGdldCkgPT4ge1xuICAgICAgICBzaWduYWxlci5hZGRXaWRnZXQod2lkZ2V0KTtcbiAgICAgICAgcmV0dXJuIG5ldyBPcGVuVGFiKHdpZGdldCk7XG4gICAgICB9KTtcbiAgICB9LFxuICAgIHNodXRkb3duQWxsOiAoKSA9PiB7XG4gICAgICBmb3IgKGNvbnN0IHdpZGdldCBvZiBsYWJTaGVsbC53aWRnZXRzKCdtYWluJykpIHtcbiAgICAgICAgd2lkZ2V0LmNsb3NlKCk7XG4gICAgICB9XG4gICAgfSxcbiAgICByZWZyZXNoUnVubmluZzogKCkgPT4ge1xuICAgICAgcmV0dXJuIHZvaWQgMDtcbiAgICB9LFxuICAgIHJ1bm5pbmdDaGFuZ2VkOiBzaWduYWxlci50YWJzQ2hhbmdlZCxcbiAgICBzaHV0ZG93bkxhYmVsOiB0cmFucy5fXygnQ2xvc2UnKSxcbiAgICBzaHV0ZG93bkFsbExhYmVsOiB0cmFucy5fXygnQ2xvc2UgQWxsJyksXG4gICAgc2h1dGRvd25BbGxDb25maXJtYXRpb25UZXh0OiB0cmFucy5fXyhcbiAgICAgICdBcmUgeW91IHN1cmUgeW91IHdhbnQgdG8gY2xvc2UgYWxsIG9wZW4gdGFicz8nXG4gICAgKVxuICB9KTtcblxuICBjbGFzcyBPcGVuVGFiIGltcGxlbWVudHMgSVJ1bm5pbmdTZXNzaW9ucy5JUnVubmluZ0l0ZW0ge1xuICAgIGNvbnN0cnVjdG9yKHdpZGdldDogV2lkZ2V0KSB7XG4gICAgICB0aGlzLl93aWRnZXQgPSB3aWRnZXQ7XG4gICAgfVxuICAgIG9wZW4oKSB7XG4gICAgICBsYWJTaGVsbC5hY3RpdmF0ZUJ5SWQodGhpcy5fd2lkZ2V0LmlkKTtcbiAgICB9XG4gICAgc2h1dGRvd24oKSB7XG4gICAgICB0aGlzLl93aWRnZXQuY2xvc2UoKTtcbiAgICB9XG4gICAgaWNvbigpIHtcbiAgICAgIGNvbnN0IHdpZGdldEljb24gPSB0aGlzLl93aWRnZXQudGl0bGUuaWNvbjtcbiAgICAgIHJldHVybiB3aWRnZXRJY29uIGluc3RhbmNlb2YgTGFiSWNvbiA/IHdpZGdldEljb24gOiBmaWxlSWNvbjtcbiAgICB9XG4gICAgbGFiZWwoKSB7XG4gICAgICByZXR1cm4gdGhpcy5fd2lkZ2V0LnRpdGxlLmxhYmVsO1xuICAgIH1cbiAgICBsYWJlbFRpdGxlKCkge1xuICAgICAgbGV0IGxhYmVsVGl0bGU6IHN0cmluZztcbiAgICAgIGlmICh0aGlzLl93aWRnZXQgaW5zdGFuY2VvZiBEb2N1bWVudFdpZGdldCkge1xuICAgICAgICBsYWJlbFRpdGxlID0gdGhpcy5fd2lkZ2V0LmNvbnRleHQucGF0aDtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGxhYmVsVGl0bGUgPSB0aGlzLl93aWRnZXQudGl0bGUubGFiZWw7XG4gICAgICB9XG4gICAgICByZXR1cm4gbGFiZWxUaXRsZTtcbiAgICB9XG5cbiAgICBwcml2YXRlIF93aWRnZXQ6IFdpZGdldDtcbiAgfVxufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9