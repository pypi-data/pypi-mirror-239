"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_application-extension_lib_index_js"],{

/***/ "../packages/application-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/application-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DEFAULT_CONTEXT_ITEM_RANK": () => (/* binding */ DEFAULT_CONTEXT_ITEM_RANK),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/property-inspector */ "webpack/sharing/consume/default/@jupyterlab/property-inspector/@jupyterlab/property-inspector");
/* harmony import */ var _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _topbar__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./topbar */ "../packages/application-extension/lib/topbar.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module application-extension
 */
















/**
 * Default context menu item rank
 */
const DEFAULT_CONTEXT_ITEM_RANK = 100;
/**
 * The command IDs used by the application plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.activateNextTab = 'application:activate-next-tab';
    CommandIDs.activatePreviousTab = 'application:activate-previous-tab';
    CommandIDs.activateNextTabBar = 'application:activate-next-tab-bar';
    CommandIDs.activatePreviousTabBar = 'application:activate-previous-tab-bar';
    CommandIDs.close = 'application:close';
    CommandIDs.closeOtherTabs = 'application:close-other-tabs';
    CommandIDs.closeRightTabs = 'application:close-right-tabs';
    CommandIDs.closeAll = 'application:close-all';
    CommandIDs.setMode = 'application:set-mode';
    CommandIDs.showPropertyPanel = 'property-inspector:show-panel';
    CommandIDs.resetLayout = 'application:reset-layout';
    CommandIDs.toggleHeader = 'application:toggle-header';
    CommandIDs.toggleMode = 'application:toggle-mode';
    CommandIDs.toggleLeftArea = 'application:toggle-left-area';
    CommandIDs.toggleRightArea = 'application:toggle-right-area';
    CommandIDs.toggleSideTabBar = 'application:toggle-side-tabbar';
    CommandIDs.togglePresentationMode = 'application:toggle-presentation-mode';
    CommandIDs.tree = 'router:tree';
    CommandIDs.switchSidebar = 'sidebar:switch';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin to register the commands for the main application.
 */
const mainCommands = {
    id: '@jupyterlab/application-extension:commands',
    description: 'Adds commands related to the shell.',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, labShell, palette) => {
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Main Area');
        // Add Command to override the JLab context menu.
        commands.addCommand(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEndContextMenu.contextMenu, {
            label: trans.__('Shift+Right Click for Browser Menu'),
            isEnabled: () => false,
            execute: () => void 0
        });
        // Returns the widget associated with the most recent contextmenu event.
        const contextMenuWidget = () => {
            const test = (node) => !!node.dataset.id;
            const node = app.contextMenuHitTest(test);
            if (!node) {
                // Fall back to active widget if path cannot be obtained from event.
                return shell.currentWidget;
            }
            return ((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__.find)(shell.widgets('main'), widget => widget.id === node.dataset.id) ||
                shell.currentWidget);
        };
        // Closes an array of widgets.
        const closeWidgets = (widgets) => {
            widgets.forEach(widget => widget.close());
        };
        // Find the tab area for a widget within a specific dock area.
        const findTab = (area, widget) => {
            if (area.type === 'tab-area') {
                return area.widgets.includes(widget) ? area : null;
            }
            if (area.type === 'split-area') {
                for (const child of area.children) {
                    const found = findTab(child, widget);
                    if (found) {
                        return found;
                    }
                }
            }
            return null;
        };
        // Find the tab area for a widget within the main dock area.
        const tabAreaFor = (widget) => {
            var _a;
            const layout = labShell === null || labShell === void 0 ? void 0 : labShell.saveLayout();
            const mainArea = layout === null || layout === void 0 ? void 0 : layout.mainArea;
            if (!mainArea || _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('mode') !== 'multiple-document') {
                return null;
            }
            const area = (_a = mainArea.dock) === null || _a === void 0 ? void 0 : _a.main;
            return area ? findTab(area, widget) : null;
        };
        // Returns an array of all widgets to the right of a widget in a tab area.
        const widgetsRightOf = (widget) => {
            const { id } = widget;
            const tabArea = tabAreaFor(widget);
            const widgets = tabArea ? tabArea.widgets || [] : [];
            const index = widgets.findIndex(widget => widget.id === id);
            if (index < 0) {
                return [];
            }
            return widgets.slice(index + 1);
        };
        commands.addCommand(CommandIDs.close, {
            label: () => trans.__('Close Tab'),
            isEnabled: () => {
                const widget = contextMenuWidget();
                return !!widget && widget.title.closable;
            },
            execute: () => {
                const widget = contextMenuWidget();
                if (widget) {
                    widget.close();
                }
            }
        });
        commands.addCommand(CommandIDs.closeOtherTabs, {
            label: () => trans.__('Close All Other Tabs'),
            isEnabled: () => {
                // Ensure there are at least two widgets.
                return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__.some)(shell.widgets('main'), (_, i) => i === 1);
            },
            execute: () => {
                const widget = contextMenuWidget();
                if (!widget) {
                    return;
                }
                const { id } = widget;
                for (const widget of shell.widgets('main')) {
                    if (widget.id !== id) {
                        widget.close();
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.closeRightTabs, {
            label: () => trans.__('Close Tabs to Right'),
            isEnabled: () => !!contextMenuWidget() &&
                widgetsRightOf(contextMenuWidget()).length > 0,
            execute: () => {
                const widget = contextMenuWidget();
                if (!widget) {
                    return;
                }
                closeWidgets(widgetsRightOf(widget));
            }
        });
        if (labShell) {
            commands.addCommand(CommandIDs.activateNextTab, {
                label: trans.__('Activate Next Tab'),
                execute: () => {
                    labShell.activateNextTab();
                }
            });
            commands.addCommand(CommandIDs.activatePreviousTab, {
                label: trans.__('Activate Previous Tab'),
                execute: () => {
                    labShell.activatePreviousTab();
                }
            });
            commands.addCommand(CommandIDs.activateNextTabBar, {
                label: trans.__('Activate Next Tab Bar'),
                execute: () => {
                    labShell.activateNextTabBar();
                }
            });
            commands.addCommand(CommandIDs.activatePreviousTabBar, {
                label: trans.__('Activate Previous Tab Bar'),
                execute: () => {
                    labShell.activatePreviousTabBar();
                }
            });
            commands.addCommand(CommandIDs.closeAll, {
                label: trans.__('Close All Tabs'),
                execute: () => {
                    labShell.closeAll();
                }
            });
            commands.addCommand(CommandIDs.toggleHeader, {
                label: trans.__('Show Header'),
                execute: () => {
                    if (labShell.mode === 'single-document') {
                        labShell.toggleTopInSimpleModeVisibility();
                    }
                },
                isToggled: () => labShell.isTopInSimpleModeVisible(),
                isVisible: () => labShell.mode === 'single-document'
            });
            commands.addCommand(CommandIDs.toggleLeftArea, {
                label: trans.__('Show Left Sidebar'),
                execute: () => {
                    if (labShell.leftCollapsed) {
                        labShell.expandLeft();
                    }
                    else {
                        labShell.collapseLeft();
                        if (labShell.currentWidget) {
                            labShell.activateById(labShell.currentWidget.id);
                        }
                    }
                },
                isToggled: () => !labShell.leftCollapsed,
                isEnabled: () => !labShell.isEmpty('left')
            });
            commands.addCommand(CommandIDs.toggleRightArea, {
                label: trans.__('Show Right Sidebar'),
                execute: () => {
                    if (labShell.rightCollapsed) {
                        labShell.expandRight();
                    }
                    else {
                        labShell.collapseRight();
                        if (labShell.currentWidget) {
                            labShell.activateById(labShell.currentWidget.id);
                        }
                    }
                },
                isToggled: () => !labShell.rightCollapsed,
                isEnabled: () => !labShell.isEmpty('right')
            });
            commands.addCommand(CommandIDs.toggleSideTabBar, {
                label: args => args.side === 'right'
                    ? trans.__('Show Right Activity Bar')
                    : trans.__('Show Left Activity Bar'),
                execute: args => {
                    if (args.side === 'right') {
                        labShell.toggleSideTabBarVisibility('right');
                    }
                    else {
                        labShell.toggleSideTabBarVisibility('left');
                    }
                },
                isToggled: args => args.side === 'right'
                    ? labShell.isSideTabBarVisible('right')
                    : labShell.isSideTabBarVisible('left'),
                isEnabled: args => args.side === 'right'
                    ? !labShell.isEmpty('right')
                    : !labShell.isEmpty('left')
            });
            commands.addCommand(CommandIDs.togglePresentationMode, {
                label: () => trans.__('Presentation Mode'),
                execute: () => {
                    labShell.presentationMode = !labShell.presentationMode;
                },
                isToggled: () => labShell.presentationMode,
                isVisible: () => true
            });
            commands.addCommand(CommandIDs.setMode, {
                label: args => args['mode']
                    ? trans.__('Set %1 mode.', args['mode'])
                    : trans.__('Set the layout `mode`.'),
                caption: trans.__('The layout `mode` can be "single-document" or "multiple-document".'),
                isVisible: args => {
                    const mode = args['mode'];
                    return mode === 'single-document' || mode === 'multiple-document';
                },
                execute: args => {
                    const mode = args['mode'];
                    if (mode === 'single-document' || mode === 'multiple-document') {
                        labShell.mode = mode;
                        return;
                    }
                    throw new Error(`Unsupported application shell mode: ${mode}`);
                }
            });
            commands.addCommand(CommandIDs.toggleMode, {
                label: trans.__('Simple Interface'),
                isToggled: () => labShell.mode === 'single-document',
                execute: () => {
                    const args = labShell.mode === 'multiple-document'
                        ? { mode: 'single-document' }
                        : { mode: 'multiple-document' };
                    return commands.execute(CommandIDs.setMode, args);
                }
            });
            commands.addCommand(CommandIDs.resetLayout, {
                label: trans.__('Reset Default Layout'),
                execute: () => {
                    // Turn off presentation mode
                    if (labShell.presentationMode) {
                        commands
                            .execute(CommandIDs.togglePresentationMode)
                            .catch(reason => {
                            console.error('Failed to undo presentation mode.', reason);
                        });
                    }
                    // Display top header
                    if (labShell.mode === 'single-document' &&
                        !labShell.isTopInSimpleModeVisible()) {
                        commands.execute(CommandIDs.toggleHeader).catch(reason => {
                            console.error('Failed to display title header.', reason);
                        });
                    }
                    // Display side tabbar
                    ['left', 'right'].forEach(side => {
                        if (!labShell.isSideTabBarVisible(side) &&
                            !labShell.isEmpty(side)) {
                            commands
                                .execute(CommandIDs.toggleSideTabBar, { side })
                                .catch(reason => {
                                console.error(`Failed to show ${side} activity bar.`, reason);
                            });
                        }
                    });
                    // Some actions are also trigger indirectly
                    // - by listening to this command execution.
                }
            });
        }
        if (palette) {
            [
                CommandIDs.activateNextTab,
                CommandIDs.activatePreviousTab,
                CommandIDs.activateNextTabBar,
                CommandIDs.activatePreviousTabBar,
                CommandIDs.close,
                CommandIDs.closeAll,
                CommandIDs.closeOtherTabs,
                CommandIDs.closeRightTabs,
                CommandIDs.toggleHeader,
                CommandIDs.toggleLeftArea,
                CommandIDs.toggleRightArea,
                CommandIDs.togglePresentationMode,
                CommandIDs.toggleMode,
                CommandIDs.resetLayout
            ].forEach(command => palette.addItem({ command, category }));
            ['right', 'left'].forEach(side => {
                palette.addItem({
                    command: CommandIDs.toggleSideTabBar,
                    category,
                    args: { side }
                });
            });
        }
    }
};
/**
 * The main extension.
 */
const main = {
    id: '@jupyterlab/application-extension:main',
    description: 'Initializes the application and provides the URL tree path handler.',
    requires: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IWindowResolver,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.ITreeResolver
    ],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IConnectionLost],
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ITreePathUpdater,
    activate: (app, router, resolver, translator, treeResolver, connectionLost) => {
        const trans = translator.load('jupyterlab');
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${main.id} must be activated in JupyterLab.`);
        }
        // These two internal state variables are used to manage the two source
        // of the tree part of the URL being updated: 1) path of the active document,
        // 2) path of the default browser if the active main area widget isn't a document.
        let _docTreePath = '';
        let _defaultBrowserTreePath = '';
        function updateTreePath(treePath) {
            // Wait for tree resolver to finish before updating the path because it use the PageConfig['treePath']
            void treeResolver.paths.then(() => {
                _defaultBrowserTreePath = treePath;
                if (!_docTreePath) {
                    const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({ treePath });
                    const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).pathname;
                    router.navigate(path, { skipRouting: true });
                    // Persist the new tree path to PageConfig as it is used elsewhere at runtime.
                    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.setOption('treePath', treePath);
                }
            });
        }
        // Requiring the window resolver guarantees that the application extension
        // only loads if there is a viable window name. Otherwise, the application
        // will short-circuit and ask the user to navigate away.
        const workspace = resolver.name;
        console.debug(`Starting application in workspace: "${workspace}"`);
        // If there were errors registering plugins, tell the user.
        if (app.registerPluginErrors.length !== 0) {
            const body = (react__WEBPACK_IMPORTED_MODULE_14__.createElement("pre", null, app.registerPluginErrors.map(e => e.message).join('\n')));
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Error Registering Plugins'), {
                message: body
            });
        }
        // If the application shell layout is modified,
        // trigger a refresh of the commands.
        app.shell.layoutModified.connect(() => {
            app.commands.notifyCommandChanged();
        });
        // Watch the mode and update the page URL to /lab or /doc to reflect the
        // change.
        app.shell.modeChanged.connect((_, args) => {
            const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({ mode: args });
            const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).pathname;
            router.navigate(path, { skipRouting: true });
            // Persist this mode change to PageConfig as it is used elsewhere at runtime.
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.setOption('mode', args);
        });
        // Wait for tree resolver to finish before updating the path because it use the PageConfig['treePath']
        void treeResolver.paths.then(() => {
            // Watch the path of the current widget in the main area and update the page
            // URL to reflect the change.
            app.shell.currentPathChanged.connect((_, args) => {
                const maybeTreePath = args.newValue;
                const treePath = maybeTreePath || _defaultBrowserTreePath;
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({ treePath: treePath });
                const path = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).pathname;
                router.navigate(path, { skipRouting: true });
                // Persist the new tree path to PageConfig as it is used elsewhere at runtime.
                _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.setOption('treePath', treePath);
                _docTreePath = maybeTreePath;
            });
        });
        // If the connection to the server is lost, handle it with the
        // connection lost handler.
        connectionLost = connectionLost || _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ConnectionLost;
        app.serviceManager.connectionFailure.connect((manager, error) => connectionLost(manager, error, translator));
        const builder = app.serviceManager.builder;
        const build = () => {
            return builder
                .build()
                .then(() => {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Build Complete'),
                    body: (react__WEBPACK_IMPORTED_MODULE_14__.createElement("div", null,
                        trans.__('Build successfully completed, reload page?'),
                        react__WEBPACK_IMPORTED_MODULE_14__.createElement("br", null),
                        trans.__('You will lose any unsaved changes.'))),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({
                            label: trans.__('Reload Without Saving'),
                            actions: ['reload']
                        }),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Save and Reload') })
                    ],
                    hasClose: true
                });
            })
                .then(({ button: { accept, actions } }) => {
                if (accept) {
                    void app.commands
                        .execute('docmanager:save')
                        .then(() => {
                        router.reload();
                    })
                        .catch(err => {
                        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Save Failed'), {
                            message: react__WEBPACK_IMPORTED_MODULE_14__.createElement("pre", null, err.message)
                        });
                    });
                }
                else if (actions.includes('reload')) {
                    router.reload();
                }
            })
                .catch(err => {
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Build Failed'), {
                    message: react__WEBPACK_IMPORTED_MODULE_14__.createElement("pre", null, err.message)
                });
            });
        };
        if (builder.isAvailable && builder.shouldCheck) {
            void builder.getStatus().then(response => {
                if (response.status === 'building') {
                    return build();
                }
                if (response.status !== 'needed') {
                    return;
                }
                const body = (react__WEBPACK_IMPORTED_MODULE_14__.createElement("div", null,
                    trans.__('JupyterLab build is suggested:'),
                    react__WEBPACK_IMPORTED_MODULE_14__.createElement("br", null),
                    react__WEBPACK_IMPORTED_MODULE_14__.createElement("pre", null, response.message)));
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Build Recommended'),
                    body,
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Build') })
                    ]
                }).then(result => (result.button.accept ? build() : undefined));
            });
        }
        return updateTreePath;
    },
    autoStart: true
};
/**
 * Plugin to build the context menu from the settings.
 */
const contextMenuPlugin = {
    id: '@jupyterlab/application-extension:context-menu',
    description: 'Populates the context menu.',
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    activate: (app, settingRegistry, translator) => {
        const trans = translator.load('jupyterlab');
        function createMenu(options) {
            const menu = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.RankedMenu({ ...options, commands: app.commands });
            if (options.label) {
                menu.title.label = trans.__(options.label);
            }
            return menu;
        }
        // Load the context menu lately so plugins are loaded.
        app.started
            .then(() => {
            return Private.loadSettingsContextMenu(app.contextMenu, settingRegistry, createMenu, translator);
        })
            .catch(reason => {
            console.error('Failed to load context menu items from settings registry.', reason);
        });
    }
};
/**
 * Check if the application is dirty before closing the browser tab.
 */
const dirty = {
    id: '@jupyterlab/application-extension:dirty',
    description: 'Adds safeguard dialog when closing the browser tab with unsaved modifications.',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    activate: (app, translator) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${dirty.id} must be activated in JupyterLab.`);
        }
        const trans = translator.load('jupyterlab');
        const message = trans.__('Are you sure you want to exit JupyterLab?\n\nAny unsaved changes will be lost.');
        // The spec for the `beforeunload` event is implemented differently by
        // the different browser vendors. Consequently, the `event.returnValue`
        // attribute needs to set in addition to a return value being returned.
        // For more information, see:
        // https://developer.mozilla.org/en/docs/Web/Events/beforeunload
        window.addEventListener('beforeunload', event => {
            if (app.status.isDirty) {
                return (event.returnValue = message);
            }
        });
    }
};
/**
 * The default layout restorer provider.
 */
const layout = {
    id: '@jupyterlab/application-extension:layout',
    description: 'Provides the shell layout restorer.',
    requires: [_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_5__.IStateDB, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    activate: (app, state, labShell, settingRegistry, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.nullTranslator).load('jupyterlab');
        const first = app.started;
        const registry = app.commands;
        const mode = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('mode');
        const restorer = new _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.LayoutRestorer({
            connector: state,
            first,
            registry,
            mode
        });
        settingRegistry
            .load(shell.id)
            .then(settings => {
            var _a, _b;
            // Add a layer of customization to support app shell mode
            const customizedLayout = settings.composite['layout'];
            // Restore the layout.
            void labShell
                .restoreLayout(mode, restorer, {
                'multiple-document': (_a = customizedLayout.multiple) !== null && _a !== void 0 ? _a : {},
                'single-document': (_b = customizedLayout.single) !== null && _b !== void 0 ? _b : {}
            })
                .then(() => {
                labShell.layoutModified.connect(() => {
                    void restorer.save(labShell.saveLayout());
                });
                settings.changed.connect(onSettingsChanged);
                Private.activateSidebarSwitcher(app, labShell, settings, trans);
            });
        })
            .catch(reason => {
            console.error('Fail to load settings for the layout restorer.');
            console.error(reason);
        });
        return restorer;
        async function onSettingsChanged(settings) {
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__.JSONExt.deepEqual(settings.composite['layout'], {
                single: labShell.userLayout['single-document'],
                multiple: labShell.userLayout['multiple-document']
            })) {
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Information'),
                    body: trans.__('User layout customization has changed. You may need to reload JupyterLab to see the changes.'),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Reload') })
                    ]
                });
                if (result.button.accept) {
                    location.reload();
                }
            }
        }
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer
};
/**
 * The default URL router provider.
 */
const router = {
    id: '@jupyterlab/application-extension:router',
    description: 'Provides the URL router',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths],
    activate: (app, paths) => {
        const { commands } = app;
        const base = paths.urls.base;
        const router = new _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.Router({ base, commands });
        void app.started.then(() => {
            // Route the very first request on load.
            void router.route();
            // Route all pop state events.
            window.addEventListener('popstate', () => {
                void router.route();
            });
        });
        return router;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter
};
/**
 * The default tree route resolver plugin.
 */
const tree = {
    id: '@jupyterlab/application-extension:tree-resolver',
    description: 'Provides the tree route resolver',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.ITreeResolver,
    activate: (app, router) => {
        const { commands } = app;
        const set = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_12__.DisposableSet();
        const delegate = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__.PromiseDelegate();
        const treePattern = new RegExp('/(lab|doc)(/workspaces/[a-zA-Z0-9-_]+)?(/tree/.*)?');
        set.add(commands.addCommand(CommandIDs.tree, {
            execute: async (args) => {
                var _a;
                if (set.isDisposed) {
                    return;
                }
                const query = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.queryStringToObject((_a = args.search) !== null && _a !== void 0 ? _a : '');
                const browser = query['file-browser-path'] || '';
                // Remove the file browser path from the query string.
                delete query['file-browser-path'];
                // Clean up artifacts immediately upon routing.
                set.dispose();
                delegate.resolve({ browser, file: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('treePath') });
            }
        }));
        set.add(router.register({ command: CommandIDs.tree, pattern: treePattern }));
        // If a route is handled by the router without the tree command being
        // invoked, resolve to `null` and clean up artifacts.
        const listener = () => {
            if (set.isDisposed) {
                return;
            }
            set.dispose();
            delegate.resolve(null);
        };
        router.routed.connect(listener);
        set.add(new _lumino_disposable__WEBPACK_IMPORTED_MODULE_12__.DisposableDelegate(() => {
            router.routed.disconnect(listener);
        }));
        return { paths: delegate.promise };
    }
};
/**
 * The default URL not found extension.
 */
const notfound = {
    id: '@jupyterlab/application-extension:notfound',
    description: 'Defines the behavior for not found URL (aka route).',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    activate: (_, paths, router, translator) => {
        const trans = translator.load('jupyterlab');
        const bad = paths.urls.notFound;
        if (!bad) {
            return;
        }
        const base = router.base;
        const message = trans.__('The path: %1 was not found. JupyterLab redirected to: %2', bad, base);
        // Change the URL back to the base application URL.
        router.navigate('');
        void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Path Not Found'), { message });
    },
    autoStart: true
};
/**
 * Change the favicon changing based on the busy status;
 */
const busy = {
    id: '@jupyterlab/application-extension:faviconbusy',
    description: 'Handles the favicon depending on the application status.',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus],
    activate: async (_, status) => {
        status.busySignal.connect((_, isBusy) => {
            const favicon = document.querySelector(`link[rel="icon"]${isBusy ? '.idle.favicon' : '.busy.favicon'}`);
            if (!favicon) {
                return;
            }
            const newFavicon = document.querySelector(`link${isBusy ? '.busy.favicon' : '.idle.favicon'}`);
            if (!newFavicon) {
                return;
            }
            // If we have the two icons with the special classes, then toggle them.
            if (favicon !== newFavicon) {
                favicon.rel = '';
                newFavicon.rel = 'icon';
                // Firefox doesn't seem to recognize just changing rel, so we also
                // reinsert the link into the DOM.
                newFavicon.parentNode.replaceChild(newFavicon, newFavicon);
            }
        });
    },
    autoStart: true
};
/**
 * The default JupyterLab application shell.
 */
const shell = {
    id: '@jupyterlab/application-extension:shell',
    description: 'Provides the JupyterLab shell. It has an extended API compared to `app.shell`.',
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    activate: (app, settingRegistry) => {
        if (!(app.shell instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.LabShell)) {
            throw new Error(`${shell.id} did not find a LabShell instance.`);
        }
        if (settingRegistry) {
            void settingRegistry.load(shell.id).then(settings => {
                app.shell.updateConfig(settings.composite);
                settings.changed.connect(() => {
                    app.shell.updateConfig(settings.composite);
                });
            });
        }
        return app.shell;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell
};
/**
 * The default JupyterLab application status provider.
 */
const status = {
    id: '@jupyterlab/application-extension:status',
    description: 'Provides the application status.',
    activate: (app) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${status.id} must be activated in JupyterLab.`);
        }
        return app.status;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus
};
/**
 * The default JupyterLab application-specific information provider.
 *
 * #### Notes
 * This plugin should only be used by plugins that specifically need to access
 * JupyterLab application information, e.g., listing extensions that have been
 * loaded or deferred within JupyterLab.
 */
const info = {
    id: '@jupyterlab/application-extension:info',
    description: 'Provides the application information.',
    activate: (app) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${info.id} must be activated in JupyterLab.`);
        }
        return app.info;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab.IInfo
};
/**
 * The default JupyterLab paths dictionary provider.
 */
const paths = {
    id: '@jupyterlab/application-extension:paths',
    description: 'Provides the application paths.',
    activate: (app) => {
        if (!(app instanceof _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab)) {
            throw new Error(`${paths.id} must be activated in JupyterLab.`);
        }
        return app.paths;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths
};
/**
 * The default property inspector provider.
 */
const propertyInspector = {
    id: '@jupyterlab/application-extension:property-inspector',
    description: 'Provides the property inspector.',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__.IPropertyInspectorProvider,
    activate: (app, labshell, translator, restorer) => {
        const trans = translator.load('jupyterlab');
        const widget = new _jupyterlab_property_inspector__WEBPACK_IMPORTED_MODULE_3__.SideBarPropertyInspectorProvider({
            shell: labshell,
            translator
        });
        widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.buildIcon;
        widget.title.caption = trans.__('Property Inspector');
        widget.id = 'jp-property-inspector';
        labshell.add(widget, 'right', { rank: 100, type: 'Property Inspector' });
        app.commands.addCommand(CommandIDs.showPropertyPanel, {
            label: trans.__('Property Inspector'),
            execute: () => {
                labshell.activateById(widget.id);
            }
        });
        if (restorer) {
            restorer.add(widget, 'jp-property-inspector');
        }
        return widget;
    }
};
const jupyterLogo = {
    id: '@jupyterlab/application-extension:logo',
    description: 'Sets the application logo.',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, shell) => {
        const logo = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_13__.Widget();
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.jupyterIcon.element({
            container: logo.node,
            elementPosition: 'center',
            margin: '2px 18px 2px 9px',
            height: 'auto',
            width: '32px'
        });
        logo.id = 'jp-MainLogo';
        shell.add(logo, 'top', { rank: 0 });
    }
};
/**
 * The simple interface mode switch in the status bar.
 */
const modeSwitchPlugin = {
    id: '@jupyterlab/application-extension:mode-switch',
    description: 'Adds the interface mode switch',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_6__.IStatusBar, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    activate: (app, labShell, translator, statusBar, settingRegistry) => {
        if (statusBar === null) {
            // Bail early
            return;
        }
        const trans = translator.load('jupyterlab');
        const modeSwitch = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_8__.Switch();
        modeSwitch.id = 'jp-single-document-mode';
        modeSwitch.valueChanged.connect((_, args) => {
            labShell.mode = args.newValue ? 'single-document' : 'multiple-document';
        });
        labShell.modeChanged.connect((_, mode) => {
            modeSwitch.value = mode === 'single-document';
        });
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(shell.id);
            const updateSettings = (settings) => {
                const startMode = settings.get('startMode').composite;
                if (startMode) {
                    labShell.mode =
                        startMode === 'single' ? 'single-document' : 'multiple-document';
                }
            };
            Promise.all([loadSettings, app.restored])
                .then(([settings]) => {
                updateSettings(settings);
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        // Show the current file browser shortcut in its title.
        const updateModeSwitchTitle = () => {
            const binding = app.commands.keyBindings.find(b => b.command === 'application:toggle-mode');
            if (binding) {
                const ks = binding.keys.map(_lumino_commands__WEBPACK_IMPORTED_MODULE_11__.CommandRegistry.formatKeystroke).join(', ');
                modeSwitch.caption = trans.__('Simple Interface (%1)', ks);
            }
            else {
                modeSwitch.caption = trans.__('Simple Interface');
            }
        };
        updateModeSwitchTitle();
        app.commands.keyBindingChanged.connect(() => {
            updateModeSwitchTitle();
        });
        modeSwitch.label = trans.__('Simple');
        statusBar.registerStatusItem(modeSwitchPlugin.id, {
            item: modeSwitch,
            align: 'left',
            rank: -1
        });
    },
    autoStart: true
};
/**
 * Export the plugins as default.
 */
const plugins = [
    contextMenuPlugin,
    dirty,
    main,
    mainCommands,
    layout,
    router,
    tree,
    notfound,
    busy,
    shell,
    status,
    info,
    modeSwitchPlugin,
    paths,
    propertyInspector,
    jupyterLogo,
    _topbar__WEBPACK_IMPORTED_MODULE_15__.topbar
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
var Private;
(function (Private) {
    async function displayInformation(trans) {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Information'),
            body: trans.__('Context menu customization has changed. You will need to reload JupyterLab to see the changes.'),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Reload') })
            ]
        });
        if (result.button.accept) {
            location.reload();
        }
    }
    async function loadSettingsContextMenu(contextMenu, registry, menuFactory, translator) {
        var _a;
        const trans = translator.load('jupyterlab');
        const pluginId = contextMenuPlugin.id;
        let canonical = null;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         *
         * We keep track of disabled entries in case the plugin is loaded
         * after the menu initialization.
         */
        function populate(schema) {
            var _a, _b;
            loaded = {};
            const pluginDefaults = Object.keys(registry.plugins)
                .map(plugin => {
                var _a, _b;
                const items = (_b = (_a = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.context) !== null && _b !== void 0 ? _b : [];
                loaded[plugin] = items;
                return items;
            })
                .concat([(_b = (_a = schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.context) !== null && _b !== void 0 ? _b : []])
                .reduceRight((acc, val) => _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(acc, val, true), []);
            // Apply default value as last step to take into account overrides.json
            // The standard default being [] as the plugin must use `jupyter.lab.menus.context`
            // to define their default value.
            schema.properties.contextMenu.default = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(pluginDefaults, schema.properties.contextMenu.default, true)
                // flatten one level
                .sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(pluginId, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.contextMenu) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    ...plugin.data.user,
                    contextMenu: (_d = plugin.data.user.contextMenu) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    ...plugin.data.composite,
                    contextMenu: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(defaults, user.contextMenu, false)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        // Repopulate the canonical variable after the setting registry has
        // preloaded all initial plugins.
        const settings = await registry.load(pluginId);
        const contextItems = (_a = settings.composite.contextMenu) !== null && _a !== void 0 ? _a : [];
        // Create menu item for non-disabled element
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.filterDisabledItems(contextItems).forEach(item => {
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.addContextItem({
                // We have to set the default rank because Lumino is sorting the visible items
                rank: DEFAULT_CONTEXT_ITEM_RANK,
                ...item
            }, contextMenu, menuFactory);
        });
        settings.changed.connect(() => {
            var _a;
            // As extension may change the context menu through API,
            // prompt the user to reload if the menu has been updated.
            const newItems = (_a = settings.composite.contextMenu) !== null && _a !== void 0 ? _a : [];
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__.JSONExt.deepEqual(contextItems, newItems)) {
                void displayInformation(trans);
            }
        });
        registry.pluginChanged.connect(async (sender, plugin) => {
            var _a, _b, _c, _d;
            if (plugin !== pluginId) {
                // If the plugin changed its menu.
                const oldItems = (_a = loaded[plugin]) !== null && _a !== void 0 ? _a : [];
                const newItems = (_c = (_b = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _b === void 0 ? void 0 : _b.context) !== null && _c !== void 0 ? _c : [];
                if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__.JSONExt.deepEqual(oldItems, newItems)) {
                    if (loaded[plugin]) {
                        // The plugin has changed, request the user to reload the UI
                        await displayInformation(trans);
                    }
                    else {
                        // The plugin was not yet loaded when the menu was built => update the menu
                        loaded[plugin] = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_10__.JSONExt.deepCopy(newItems);
                        // Merge potential disabled state
                        const toAdd = (_d = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.reconcileItems(newItems, contextItems, false, false)) !== null && _d !== void 0 ? _d : [];
                        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.SettingRegistry.filterDisabledItems(toAdd).forEach(item => {
                            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.addContextItem({
                                // We have to set the default rank because Lumino is sorting the visible items
                                rank: DEFAULT_CONTEXT_ITEM_RANK,
                                ...item
                            }, contextMenu, menuFactory);
                        });
                    }
                }
            }
        });
    }
    Private.loadSettingsContextMenu = loadSettingsContextMenu;
    function activateSidebarSwitcher(app, labShell, settings, trans) {
        // Add a command to switch a side panels's side
        app.commands.addCommand(CommandIDs.switchSidebar, {
            label: trans.__('Switch Sidebar Side'),
            execute: () => {
                // First, try to find the correct panel based on the application
                // context menu click. Bail if we don't find a sidebar for the widget.
                const contextNode = app.contextMenuHitTest(node => !!node.dataset.id);
                if (!contextNode) {
                    return;
                }
                const id = contextNode.dataset['id'];
                const leftPanel = document.getElementById('jp-left-stack');
                const node = document.getElementById(id);
                let newLayout = null;
                // Move the panel to the other side.
                if (leftPanel && node && leftPanel.contains(node)) {
                    const widget = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__.find)(labShell.widgets('left'), w => w.id === id);
                    if (widget) {
                        newLayout = labShell.move(widget, 'right');
                        labShell.activateById(widget.id);
                    }
                }
                else {
                    const widget = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_9__.find)(labShell.widgets('right'), w => w.id === id);
                    if (widget) {
                        newLayout = labShell.move(widget, 'left');
                        labShell.activateById(widget.id);
                    }
                }
                if (newLayout) {
                    settings
                        .set('layout', {
                        single: newLayout['single-document'],
                        multiple: newLayout['multiple-document']
                    })
                        .catch(reason => {
                        console.error('Failed to save user layout customization.', reason);
                    });
                }
            }
        });
        app.commands.commandExecuted.connect((registry, executed) => {
            if (executed.id === CommandIDs.resetLayout) {
                settings.remove('layout').catch(reason => {
                    console.error('Failed to remove user layout customization.', reason);
                });
            }
        });
    }
    Private.activateSidebarSwitcher = activateSidebarSwitcher;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/application-extension/lib/topbar.js":
/*!*******************************************************!*\
  !*** ../packages/application-extension/lib/topbar.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "topbar": () => (/* binding */ topbar)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */




const TOPBAR_FACTORY = 'TopBar';
/**
 * A plugin adding a toolbar to the top area.
 */
const topbar = {
    id: '@jupyterlab/application-extension:top-bar',
    description: 'Adds a toolbar to the top area (next to the main menu bar).',
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IToolbarWidgetRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    activate: (app, settingRegistry, toolbarRegistry, translator) => {
        const toolbar = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.Toolbar();
        toolbar.id = 'jp-top-bar';
        // Set toolbar
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.setToolbar)(toolbar, (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.createToolbarFactory)(toolbarRegistry, settingRegistry, TOPBAR_FACTORY, topbar.id, translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator), toolbar);
        app.shell.add(toolbar, 'top', { rank: 900 });
    }
};


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfYXBwbGljYXRpb24tZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy5mZGQ4NjlkNTBmNDkwYmI1ODA1Yy5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQWlCOEI7QUFRSDtBQUM2QjtBQUluQjtBQUN3QztBQUNqQztBQUNJO0FBS2xCO0FBT0U7QUFDWTtBQUtwQjtBQUN3QjtBQUNvQjtBQUNQO0FBQ2pDO0FBQ0c7QUFFbEM7O0dBRUc7QUFDSSxNQUFNLHlCQUF5QixHQUFHLEdBQUcsQ0FBQztBQUU3Qzs7R0FFRztBQUNILElBQVUsVUFBVSxDQXlDbkI7QUF6Q0QsV0FBVSxVQUFVO0lBQ0wsMEJBQWUsR0FBVywrQkFBK0IsQ0FBQztJQUUxRCw4QkFBbUIsR0FDOUIsbUNBQW1DLENBQUM7SUFFekIsNkJBQWtCLEdBQVcsbUNBQW1DLENBQUM7SUFFakUsaUNBQXNCLEdBQ2pDLHVDQUF1QyxDQUFDO0lBRTdCLGdCQUFLLEdBQUcsbUJBQW1CLENBQUM7SUFFNUIseUJBQWMsR0FBRyw4QkFBOEIsQ0FBQztJQUVoRCx5QkFBYyxHQUFHLDhCQUE4QixDQUFDO0lBRWhELG1CQUFRLEdBQVcsdUJBQXVCLENBQUM7SUFFM0Msa0JBQU8sR0FBVyxzQkFBc0IsQ0FBQztJQUV6Qyw0QkFBaUIsR0FBVywrQkFBK0IsQ0FBQztJQUU1RCxzQkFBVyxHQUFXLDBCQUEwQixDQUFDO0lBRWpELHVCQUFZLEdBQVcsMkJBQTJCLENBQUM7SUFFbkQscUJBQVUsR0FBVyx5QkFBeUIsQ0FBQztJQUUvQyx5QkFBYyxHQUFXLDhCQUE4QixDQUFDO0lBRXhELDBCQUFlLEdBQVcsK0JBQStCLENBQUM7SUFFMUQsMkJBQWdCLEdBQVcsZ0NBQWdDLENBQUM7SUFFNUQsaUNBQXNCLEdBQ2pDLHNDQUFzQyxDQUFDO0lBRTVCLGVBQUksR0FBVyxhQUFhLENBQUM7SUFF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QiwwQkFpRXRDO0FBQ0gsQ0FBQyxFQW5QUyxPQUFPLEtBQVAsT0FBTyxRQW1QaEI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDbjdDRDs7O0dBR0c7QUFVMkI7QUFDaUM7QUFDTztBQUNsQjtBQUVwRCxNQUFNLGNBQWMsR0FBRyxRQUFRLENBQUM7QUFFaEM7O0dBRUc7QUFDSSxNQUFNLE1BQU0sR0FBZ0M7SUFDakQsRUFBRSxFQUFFLDJDQUEyQztJQUMvQyxXQUFXLEVBQUUsNkRBQTZEO0lBQzFFLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQUMseUVBQWdCLEVBQUUsd0VBQXNCLENBQUM7SUFDcEQsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixlQUFpQyxFQUNqQyxlQUF1QyxFQUN2QyxVQUE4QixFQUM5QixFQUFFO1FBQ0YsTUFBTSxPQUFPLEdBQUcsSUFBSSw4REFBTyxFQUFFLENBQUM7UUFDOUIsT0FBTyxDQUFDLEVBQUUsR0FBRyxZQUFZLENBQUM7UUFFMUIsY0FBYztRQUNkLGdFQUFVLENBQ1IsT0FBTyxFQUNQLDBFQUFvQixDQUNsQixlQUFlLEVBQ2YsZUFBZSxFQUNmLGNBQWMsRUFDZCxNQUFNLENBQUMsRUFBRSxFQUNULFVBQVUsYUFBVixVQUFVLGNBQVYsVUFBVSxHQUFJLG1FQUFjLENBQzdCLEVBQ0QsT0FBTyxDQUNSLENBQUM7UUFFRixHQUFHLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxPQUFPLEVBQUUsS0FBSyxFQUFFLEVBQUUsSUFBSSxFQUFFLEdBQUcsRUFBRSxDQUFDLENBQUM7SUFDL0MsQ0FBQztDQUNGLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvYXBwbGljYXRpb24tZXh0ZW5zaW9uL3NyYy9pbmRleC50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2FwcGxpY2F0aW9uLWV4dGVuc2lvbi9zcmMvdG9wYmFyLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGFwcGxpY2F0aW9uLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIENvbm5lY3Rpb25Mb3N0LFxuICBJQ29ubmVjdGlvbkxvc3QsXG4gIElMYWJTaGVsbCxcbiAgSUxhYlN0YXR1cyxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBJUm91dGVyLFxuICBJVHJlZVBhdGhVcGRhdGVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZENvbnRleHRNZW51LFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW4sXG4gIEp1cHl0ZXJMYWIsXG4gIExhYlNoZWxsLFxuICBMYXlvdXRSZXN0b3JlcixcbiAgUm91dGVyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIERpYWxvZyxcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBJV2luZG93UmVzb2x2ZXIsXG4gIE1lbnVGYWN0b3J5LFxuICBzaG93RGlhbG9nLFxuICBzaG93RXJyb3JNZXNzYWdlXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFBhZ2VDb25maWcsIFVSTEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlcixcbiAgU2lkZUJhclByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcHJvcGVydHktaW5zcGVjdG9yJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnksIFNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJU3RhdGVEQiB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXRlZGInO1xuaW1wb3J0IHsgSVN0YXR1c0JhciB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXR1c2Jhcic7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7XG4gIGJ1aWxkSWNvbixcbiAgQ29udGV4dE1lbnVTdmcsXG4gIGp1cHl0ZXJJY29uLFxuICBSYW5rZWRNZW51LFxuICBTd2l0Y2hcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBmaW5kLCBzb21lIH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHtcbiAgSlNPTkV4dCxcbiAgUHJvbWlzZURlbGVnYXRlLFxuICBSZWFkb25seVBhcnRpYWxKU09OVmFsdWVcbn0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgQ29tbWFuZFJlZ2lzdHJ5IH0gZnJvbSAnQGx1bWluby9jb21tYW5kcyc7XG5pbXBvcnQgeyBEaXNwb3NhYmxlRGVsZWdhdGUsIERpc3Bvc2FibGVTZXQgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgRG9ja0xheW91dCwgRG9ja1BhbmVsLCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgdG9wYmFyIH0gZnJvbSAnLi90b3BiYXInO1xuXG4vKipcbiAqIERlZmF1bHQgY29udGV4dCBtZW51IGl0ZW0gcmFua1xuICovXG5leHBvcnQgY29uc3QgREVGQVVMVF9DT05URVhUX0lURU1fUkFOSyA9IDEwMDtcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgYXBwbGljYXRpb24gcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBhY3RpdmF0ZU5leHRUYWI6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjphY3RpdmF0ZS1uZXh0LXRhYic7XG5cbiAgZXhwb3J0IGNvbnN0IGFjdGl2YXRlUHJldmlvdXNUYWI6IHN0cmluZyA9XG4gICAgJ2FwcGxpY2F0aW9uOmFjdGl2YXRlLXByZXZpb3VzLXRhYic7XG5cbiAgZXhwb3J0IGNvbnN0IGFjdGl2YXRlTmV4dFRhYkJhcjogc3RyaW5nID0gJ2FwcGxpY2F0aW9uOmFjdGl2YXRlLW5leHQtdGFiLWJhcic7XG5cbiAgZXhwb3J0IGNvbnN0IGFjdGl2YXRlUHJldmlvdXNUYWJCYXI6IHN0cmluZyA9XG4gICAgJ2FwcGxpY2F0aW9uOmFjdGl2YXRlLXByZXZpb3VzLXRhYi1iYXInO1xuXG4gIGV4cG9ydCBjb25zdCBjbG9zZSA9ICdhcHBsaWNhdGlvbjpjbG9zZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGNsb3NlT3RoZXJUYWJzID0gJ2FwcGxpY2F0aW9uOmNsb3NlLW90aGVyLXRhYnMnO1xuXG4gIGV4cG9ydCBjb25zdCBjbG9zZVJpZ2h0VGFicyA9ICdhcHBsaWNhdGlvbjpjbG9zZS1yaWdodC10YWJzJztcblxuICBleHBvcnQgY29uc3QgY2xvc2VBbGw6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjpjbG9zZS1hbGwnO1xuXG4gIGV4cG9ydCBjb25zdCBzZXRNb2RlOiBzdHJpbmcgPSAnYXBwbGljYXRpb246c2V0LW1vZGUnO1xuXG4gIGV4cG9ydCBjb25zdCBzaG93UHJvcGVydHlQYW5lbDogc3RyaW5nID0gJ3Byb3BlcnR5LWluc3BlY3RvcjpzaG93LXBhbmVsJztcblxuICBleHBvcnQgY29uc3QgcmVzZXRMYXlvdXQ6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjpyZXNldC1sYXlvdXQnO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVIZWFkZXI6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjp0b2dnbGUtaGVhZGVyJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlTW9kZTogc3RyaW5nID0gJ2FwcGxpY2F0aW9uOnRvZ2dsZS1tb2RlJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlTGVmdEFyZWE6IHN0cmluZyA9ICdhcHBsaWNhdGlvbjp0b2dnbGUtbGVmdC1hcmVhJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlUmlnaHRBcmVhOiBzdHJpbmcgPSAnYXBwbGljYXRpb246dG9nZ2xlLXJpZ2h0LWFyZWEnO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVTaWRlVGFiQmFyOiBzdHJpbmcgPSAnYXBwbGljYXRpb246dG9nZ2xlLXNpZGUtdGFiYmFyJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlUHJlc2VudGF0aW9uTW9kZTogc3RyaW5nID1cbiAgICAnYXBwbGljYXRpb246dG9nZ2xlLXByZXNlbnRhdGlvbi1tb2RlJztcblxuICBleHBvcnQgY29uc3QgdHJlZTogc3RyaW5nID0gJ3JvdXRlcjp0cmVlJztcblxuICBleHBvcnQgY29uc3Qgc3dpdGNoU2lkZWJhciA9ICdzaWRlYmFyOnN3aXRjaCc7XG59XG5cbi8qKlxuICogQSBwbHVnaW4gdG8gcmVnaXN0ZXIgdGhlIGNvbW1hbmRzIGZvciB0aGUgbWFpbiBhcHBsaWNhdGlvbi5cbiAqL1xuY29uc3QgbWFpbkNvbW1hbmRzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tZXh0ZW5zaW9uOmNvbW1hbmRzJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIGNvbW1hbmRzIHJlbGF0ZWQgdG8gdGhlIHNoZWxsLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsLCBJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ01haW4gQXJlYScpO1xuXG4gICAgLy8gQWRkIENvbW1hbmQgdG8gb3ZlcnJpZGUgdGhlIEpMYWIgY29udGV4dCBtZW51LlxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoSnVweXRlckZyb250RW5kQ29udGV4dE1lbnUuY29udGV4dE1lbnUsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnU2hpZnQrUmlnaHQgQ2xpY2sgZm9yIEJyb3dzZXIgTWVudScpLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiBmYWxzZSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHZvaWQgMFxuICAgIH0pO1xuXG4gICAgLy8gUmV0dXJucyB0aGUgd2lkZ2V0IGFzc29jaWF0ZWQgd2l0aCB0aGUgbW9zdCByZWNlbnQgY29udGV4dG1lbnUgZXZlbnQuXG4gICAgY29uc3QgY29udGV4dE1lbnVXaWRnZXQgPSAoKTogV2lkZ2V0IHwgbnVsbCA9PiB7XG4gICAgICBjb25zdCB0ZXN0ID0gKG5vZGU6IEhUTUxFbGVtZW50KSA9PiAhIW5vZGUuZGF0YXNldC5pZDtcbiAgICAgIGNvbnN0IG5vZGUgPSBhcHAuY29udGV4dE1lbnVIaXRUZXN0KHRlc3QpO1xuXG4gICAgICBpZiAoIW5vZGUpIHtcbiAgICAgICAgLy8gRmFsbCBiYWNrIHRvIGFjdGl2ZSB3aWRnZXQgaWYgcGF0aCBjYW5ub3QgYmUgb2J0YWluZWQgZnJvbSBldmVudC5cbiAgICAgICAgcmV0dXJuIHNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiAoXG4gICAgICAgIGZpbmQoc2hlbGwud2lkZ2V0cygnbWFpbicpLCB3aWRnZXQgPT4gd2lkZ2V0LmlkID09PSBub2RlLmRhdGFzZXQuaWQpIHx8XG4gICAgICAgIHNoZWxsLmN1cnJlbnRXaWRnZXRcbiAgICAgICk7XG4gICAgfTtcblxuICAgIC8vIENsb3NlcyBhbiBhcnJheSBvZiB3aWRnZXRzLlxuICAgIGNvbnN0IGNsb3NlV2lkZ2V0cyA9ICh3aWRnZXRzOiBBcnJheTxXaWRnZXQ+KTogdm9pZCA9PiB7XG4gICAgICB3aWRnZXRzLmZvckVhY2god2lkZ2V0ID0+IHdpZGdldC5jbG9zZSgpKTtcbiAgICB9O1xuXG4gICAgLy8gRmluZCB0aGUgdGFiIGFyZWEgZm9yIGEgd2lkZ2V0IHdpdGhpbiBhIHNwZWNpZmljIGRvY2sgYXJlYS5cbiAgICBjb25zdCBmaW5kVGFiID0gKFxuICAgICAgYXJlYTogRG9ja0xheW91dC5BcmVhQ29uZmlnLFxuICAgICAgd2lkZ2V0OiBXaWRnZXRcbiAgICApOiBEb2NrTGF5b3V0LklUYWJBcmVhQ29uZmlnIHwgbnVsbCA9PiB7XG4gICAgICBpZiAoYXJlYS50eXBlID09PSAndGFiLWFyZWEnKSB7XG4gICAgICAgIHJldHVybiBhcmVhLndpZGdldHMuaW5jbHVkZXMod2lkZ2V0KSA/IGFyZWEgOiBudWxsO1xuICAgICAgfVxuICAgICAgaWYgKGFyZWEudHlwZSA9PT0gJ3NwbGl0LWFyZWEnKSB7XG4gICAgICAgIGZvciAoY29uc3QgY2hpbGQgb2YgYXJlYS5jaGlsZHJlbikge1xuICAgICAgICAgIGNvbnN0IGZvdW5kID0gZmluZFRhYihjaGlsZCwgd2lkZ2V0KTtcbiAgICAgICAgICBpZiAoZm91bmQpIHtcbiAgICAgICAgICAgIHJldHVybiBmb3VuZDtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHJldHVybiBudWxsO1xuICAgIH07XG5cbiAgICAvLyBGaW5kIHRoZSB0YWIgYXJlYSBmb3IgYSB3aWRnZXQgd2l0aGluIHRoZSBtYWluIGRvY2sgYXJlYS5cbiAgICBjb25zdCB0YWJBcmVhRm9yID0gKHdpZGdldDogV2lkZ2V0KTogRG9ja0xheW91dC5JVGFiQXJlYUNvbmZpZyB8IG51bGwgPT4ge1xuICAgICAgY29uc3QgbGF5b3V0ID0gbGFiU2hlbGw/LnNhdmVMYXlvdXQoKTtcbiAgICAgIGNvbnN0IG1haW5BcmVhID0gbGF5b3V0Py5tYWluQXJlYTtcbiAgICAgIGlmICghbWFpbkFyZWEgfHwgUGFnZUNvbmZpZy5nZXRPcHRpb24oJ21vZGUnKSAhPT0gJ211bHRpcGxlLWRvY3VtZW50Jykge1xuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGFyZWEgPSBtYWluQXJlYS5kb2NrPy5tYWluO1xuICAgICAgcmV0dXJuIGFyZWEgPyBmaW5kVGFiKGFyZWEsIHdpZGdldCkgOiBudWxsO1xuICAgIH07XG5cbiAgICAvLyBSZXR1cm5zIGFuIGFycmF5IG9mIGFsbCB3aWRnZXRzIHRvIHRoZSByaWdodCBvZiBhIHdpZGdldCBpbiBhIHRhYiBhcmVhLlxuICAgIGNvbnN0IHdpZGdldHNSaWdodE9mID0gKHdpZGdldDogV2lkZ2V0KTogQXJyYXk8V2lkZ2V0PiA9PiB7XG4gICAgICBjb25zdCB7IGlkIH0gPSB3aWRnZXQ7XG4gICAgICBjb25zdCB0YWJBcmVhID0gdGFiQXJlYUZvcih3aWRnZXQpO1xuICAgICAgY29uc3Qgd2lkZ2V0cyA9IHRhYkFyZWEgPyB0YWJBcmVhLndpZGdldHMgfHwgW10gOiBbXTtcbiAgICAgIGNvbnN0IGluZGV4ID0gd2lkZ2V0cy5maW5kSW5kZXgod2lkZ2V0ID0+IHdpZGdldC5pZCA9PT0gaWQpO1xuICAgICAgaWYgKGluZGV4IDwgMCkge1xuICAgICAgICByZXR1cm4gW107XG4gICAgICB9XG4gICAgICByZXR1cm4gd2lkZ2V0cy5zbGljZShpbmRleCArIDEpO1xuICAgIH07XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2xvc2UsIHtcbiAgICAgIGxhYmVsOiAoKSA9PiB0cmFucy5fXygnQ2xvc2UgVGFiJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gY29udGV4dE1lbnVXaWRnZXQoKTtcbiAgICAgICAgcmV0dXJuICEhd2lkZ2V0ICYmIHdpZGdldC50aXRsZS5jbG9zYWJsZTtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IGNvbnRleHRNZW51V2lkZ2V0KCk7XG4gICAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgICB3aWRnZXQuY2xvc2UoKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNsb3NlT3RoZXJUYWJzLCB7XG4gICAgICBsYWJlbDogKCkgPT4gdHJhbnMuX18oJ0Nsb3NlIEFsbCBPdGhlciBUYWJzJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+IHtcbiAgICAgICAgLy8gRW5zdXJlIHRoZXJlIGFyZSBhdCBsZWFzdCB0d28gd2lkZ2V0cy5cbiAgICAgICAgcmV0dXJuIHNvbWUoc2hlbGwud2lkZ2V0cygnbWFpbicpLCAoXywgaSkgPT4gaSA9PT0gMSk7XG4gICAgICB9LFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSBjb250ZXh0TWVudVdpZGdldCgpO1xuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCB7IGlkIH0gPSB3aWRnZXQ7XG4gICAgICAgIGZvciAoY29uc3Qgd2lkZ2V0IG9mIHNoZWxsLndpZGdldHMoJ21haW4nKSkge1xuICAgICAgICAgIGlmICh3aWRnZXQuaWQgIT09IGlkKSB7XG4gICAgICAgICAgICB3aWRnZXQuY2xvc2UoKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbG9zZVJpZ2h0VGFicywge1xuICAgICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdDbG9zZSBUYWJzIHRvIFJpZ2h0JyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICAgICEhY29udGV4dE1lbnVXaWRnZXQoKSAmJlxuICAgICAgICB3aWRnZXRzUmlnaHRPZihjb250ZXh0TWVudVdpZGdldCgpISkubGVuZ3RoID4gMCxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gY29udGV4dE1lbnVXaWRnZXQoKTtcbiAgICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY2xvc2VXaWRnZXRzKHdpZGdldHNSaWdodE9mKHdpZGdldCkpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuYWN0aXZhdGVOZXh0VGFiLCB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnQWN0aXZhdGUgTmV4dCBUYWInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlTmV4dFRhYigpO1xuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFjdGl2YXRlUHJldmlvdXNUYWIsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBY3RpdmF0ZSBQcmV2aW91cyBUYWInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlUHJldmlvdXNUYWIoKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5hY3RpdmF0ZU5leHRUYWJCYXIsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBY3RpdmF0ZSBOZXh0IFRhYiBCYXInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlTmV4dFRhYkJhcigpO1xuICAgICAgICB9XG4gICAgICB9KTtcblxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFjdGl2YXRlUHJldmlvdXNUYWJCYXIsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBY3RpdmF0ZSBQcmV2aW91cyBUYWIgQmFyJyksXG4gICAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZVByZXZpb3VzVGFiQmFyKCk7XG4gICAgICAgIH1cbiAgICAgIH0pO1xuXG4gICAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY2xvc2VBbGwsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdDbG9zZSBBbGwgVGFicycpLFxuICAgICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgICAgbGFiU2hlbGwuY2xvc2VBbGwoKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVIZWFkZXIsIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IEhlYWRlcicpLFxuICAgICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgICAgaWYgKGxhYlNoZWxsLm1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnKSB7XG4gICAgICAgICAgICBsYWJTaGVsbC50b2dnbGVUb3BJblNpbXBsZU1vZGVWaXNpYmlsaXR5KCk7XG4gICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBpc1RvZ2dsZWQ6ICgpID0+IGxhYlNoZWxsLmlzVG9wSW5TaW1wbGVNb2RlVmlzaWJsZSgpLFxuICAgICAgICBpc1Zpc2libGU6ICgpID0+IGxhYlNoZWxsLm1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnXG4gICAgICB9KTtcblxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZUxlZnRBcmVhLCB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnU2hvdyBMZWZ0IFNpZGViYXInKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGlmIChsYWJTaGVsbC5sZWZ0Q29sbGFwc2VkKSB7XG4gICAgICAgICAgICBsYWJTaGVsbC5leHBhbmRMZWZ0KCk7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIGxhYlNoZWxsLmNvbGxhcHNlTGVmdCgpO1xuICAgICAgICAgICAgaWYgKGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgICAgICAgbGFiU2hlbGwuYWN0aXZhdGVCeUlkKGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQuaWQpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgaXNUb2dnbGVkOiAoKSA9PiAhbGFiU2hlbGwubGVmdENvbGxhcHNlZCxcbiAgICAgICAgaXNFbmFibGVkOiAoKSA9PiAhbGFiU2hlbGwuaXNFbXB0eSgnbGVmdCcpXG4gICAgICB9KTtcblxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZVJpZ2h0QXJlYSwge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgUmlnaHQgU2lkZWJhcicpLFxuICAgICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgICAgaWYgKGxhYlNoZWxsLnJpZ2h0Q29sbGFwc2VkKSB7XG4gICAgICAgICAgICBsYWJTaGVsbC5leHBhbmRSaWdodCgpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBsYWJTaGVsbC5jb2xsYXBzZVJpZ2h0KCk7XG4gICAgICAgICAgICBpZiAobGFiU2hlbGwuY3VycmVudFdpZGdldCkge1xuICAgICAgICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZUJ5SWQobGFiU2hlbGwuY3VycmVudFdpZGdldC5pZCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuICAgICAgICB9LFxuICAgICAgICBpc1RvZ2dsZWQ6ICgpID0+ICFsYWJTaGVsbC5yaWdodENvbGxhcHNlZCxcbiAgICAgICAgaXNFbmFibGVkOiAoKSA9PiAhbGFiU2hlbGwuaXNFbXB0eSgncmlnaHQnKVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVTaWRlVGFiQmFyLCB7XG4gICAgICAgIGxhYmVsOiBhcmdzID0+XG4gICAgICAgICAgYXJncy5zaWRlID09PSAncmlnaHQnXG4gICAgICAgICAgICA/IHRyYW5zLl9fKCdTaG93IFJpZ2h0IEFjdGl2aXR5IEJhcicpXG4gICAgICAgICAgICA6IHRyYW5zLl9fKCdTaG93IExlZnQgQWN0aXZpdHkgQmFyJyksXG4gICAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICAgIGlmIChhcmdzLnNpZGUgPT09ICdyaWdodCcpIHtcbiAgICAgICAgICAgIGxhYlNoZWxsLnRvZ2dsZVNpZGVUYWJCYXJWaXNpYmlsaXR5KCdyaWdodCcpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBsYWJTaGVsbC50b2dnbGVTaWRlVGFiQmFyVmlzaWJpbGl0eSgnbGVmdCcpO1xuICAgICAgICAgIH1cbiAgICAgICAgfSxcbiAgICAgICAgaXNUb2dnbGVkOiBhcmdzID0+XG4gICAgICAgICAgYXJncy5zaWRlID09PSAncmlnaHQnXG4gICAgICAgICAgICA/IGxhYlNoZWxsLmlzU2lkZVRhYkJhclZpc2libGUoJ3JpZ2h0JylcbiAgICAgICAgICAgIDogbGFiU2hlbGwuaXNTaWRlVGFiQmFyVmlzaWJsZSgnbGVmdCcpLFxuICAgICAgICBpc0VuYWJsZWQ6IGFyZ3MgPT5cbiAgICAgICAgICBhcmdzLnNpZGUgPT09ICdyaWdodCdcbiAgICAgICAgICAgID8gIWxhYlNoZWxsLmlzRW1wdHkoJ3JpZ2h0JylcbiAgICAgICAgICAgIDogIWxhYlNoZWxsLmlzRW1wdHkoJ2xlZnQnKVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVQcmVzZW50YXRpb25Nb2RlLCB7XG4gICAgICAgIGxhYmVsOiAoKSA9PiB0cmFucy5fXygnUHJlc2VudGF0aW9uIE1vZGUnKSxcbiAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgIGxhYlNoZWxsLnByZXNlbnRhdGlvbk1vZGUgPSAhbGFiU2hlbGwucHJlc2VudGF0aW9uTW9kZTtcbiAgICAgICAgfSxcbiAgICAgICAgaXNUb2dnbGVkOiAoKSA9PiBsYWJTaGVsbC5wcmVzZW50YXRpb25Nb2RlLFxuICAgICAgICBpc1Zpc2libGU6ICgpID0+IHRydWVcbiAgICAgIH0pO1xuXG4gICAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2V0TW9kZSwge1xuICAgICAgICBsYWJlbDogYXJncyA9PlxuICAgICAgICAgIGFyZ3NbJ21vZGUnXVxuICAgICAgICAgICAgPyB0cmFucy5fXygnU2V0ICUxIG1vZGUuJywgYXJnc1snbW9kZSddKVxuICAgICAgICAgICAgOiB0cmFucy5fXygnU2V0IHRoZSBsYXlvdXQgYG1vZGVgLicpLFxuICAgICAgICBjYXB0aW9uOiB0cmFucy5fXyhcbiAgICAgICAgICAnVGhlIGxheW91dCBgbW9kZWAgY2FuIGJlIFwic2luZ2xlLWRvY3VtZW50XCIgb3IgXCJtdWx0aXBsZS1kb2N1bWVudFwiLidcbiAgICAgICAgKSxcbiAgICAgICAgaXNWaXNpYmxlOiBhcmdzID0+IHtcbiAgICAgICAgICBjb25zdCBtb2RlID0gYXJnc1snbW9kZSddIGFzIHN0cmluZztcbiAgICAgICAgICByZXR1cm4gbW9kZSA9PT0gJ3NpbmdsZS1kb2N1bWVudCcgfHwgbW9kZSA9PT0gJ211bHRpcGxlLWRvY3VtZW50JztcbiAgICAgICAgfSxcbiAgICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgICAgY29uc3QgbW9kZSA9IGFyZ3NbJ21vZGUnXSBhcyBzdHJpbmc7XG4gICAgICAgICAgaWYgKG1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnIHx8IG1vZGUgPT09ICdtdWx0aXBsZS1kb2N1bWVudCcpIHtcbiAgICAgICAgICAgIGxhYlNoZWxsLm1vZGUgPSBtb2RlO1xuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYFVuc3VwcG9ydGVkIGFwcGxpY2F0aW9uIHNoZWxsIG1vZGU6ICR7bW9kZX1gKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVNb2RlLCB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnU2ltcGxlIEludGVyZmFjZScpLFxuICAgICAgICBpc1RvZ2dsZWQ6ICgpID0+IGxhYlNoZWxsLm1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnLFxuICAgICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgICAgY29uc3QgYXJncyA9XG4gICAgICAgICAgICBsYWJTaGVsbC5tb2RlID09PSAnbXVsdGlwbGUtZG9jdW1lbnQnXG4gICAgICAgICAgICAgID8geyBtb2RlOiAnc2luZ2xlLWRvY3VtZW50JyB9XG4gICAgICAgICAgICAgIDogeyBtb2RlOiAnbXVsdGlwbGUtZG9jdW1lbnQnIH07XG4gICAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5zZXRNb2RlLCBhcmdzKTtcbiAgICAgICAgfVxuICAgICAgfSk7XG5cbiAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZXNldExheW91dCwge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1Jlc2V0IERlZmF1bHQgTGF5b3V0JyksXG4gICAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgICAvLyBUdXJuIG9mZiBwcmVzZW50YXRpb24gbW9kZVxuICAgICAgICAgIGlmIChsYWJTaGVsbC5wcmVzZW50YXRpb25Nb2RlKSB7XG4gICAgICAgICAgICBjb21tYW5kc1xuICAgICAgICAgICAgICAuZXhlY3V0ZShDb21tYW5kSURzLnRvZ2dsZVByZXNlbnRhdGlvbk1vZGUpXG4gICAgICAgICAgICAgIC5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoJ0ZhaWxlZCB0byB1bmRvIHByZXNlbnRhdGlvbiBtb2RlLicsIHJlYXNvbik7XG4gICAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgICAvLyBEaXNwbGF5IHRvcCBoZWFkZXJcbiAgICAgICAgICBpZiAoXG4gICAgICAgICAgICBsYWJTaGVsbC5tb2RlID09PSAnc2luZ2xlLWRvY3VtZW50JyAmJlxuICAgICAgICAgICAgIWxhYlNoZWxsLmlzVG9wSW5TaW1wbGVNb2RlVmlzaWJsZSgpXG4gICAgICAgICAgKSB7XG4gICAgICAgICAgICBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMudG9nZ2xlSGVhZGVyKS5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAgICAgICBjb25zb2xlLmVycm9yKCdGYWlsZWQgdG8gZGlzcGxheSB0aXRsZSBoZWFkZXIuJywgcmVhc29uKTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgICAvLyBEaXNwbGF5IHNpZGUgdGFiYmFyXG4gICAgICAgICAgKFsnbGVmdCcsICdyaWdodCddIGFzICgnbGVmdCcgfCAncmlnaHQnKVtdKS5mb3JFYWNoKHNpZGUgPT4ge1xuICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAhbGFiU2hlbGwuaXNTaWRlVGFiQmFyVmlzaWJsZShzaWRlKSAmJlxuICAgICAgICAgICAgICAhbGFiU2hlbGwuaXNFbXB0eShzaWRlKVxuICAgICAgICAgICAgKSB7XG4gICAgICAgICAgICAgIGNvbW1hbmRzXG4gICAgICAgICAgICAgICAgLmV4ZWN1dGUoQ29tbWFuZElEcy50b2dnbGVTaWRlVGFiQmFyLCB7IHNpZGUgfSlcbiAgICAgICAgICAgICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYEZhaWxlZCB0byBzaG93ICR7c2lkZX0gYWN0aXZpdHkgYmFyLmAsIHJlYXNvbik7XG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSk7XG5cbiAgICAgICAgICAvLyBTb21lIGFjdGlvbnMgYXJlIGFsc28gdHJpZ2dlciBpbmRpcmVjdGx5XG4gICAgICAgICAgLy8gLSBieSBsaXN0ZW5pbmcgdG8gdGhpcyBjb21tYW5kIGV4ZWN1dGlvbi5cbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIFtcbiAgICAgICAgQ29tbWFuZElEcy5hY3RpdmF0ZU5leHRUYWIsXG4gICAgICAgIENvbW1hbmRJRHMuYWN0aXZhdGVQcmV2aW91c1RhYixcbiAgICAgICAgQ29tbWFuZElEcy5hY3RpdmF0ZU5leHRUYWJCYXIsXG4gICAgICAgIENvbW1hbmRJRHMuYWN0aXZhdGVQcmV2aW91c1RhYkJhcixcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZSxcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZUFsbCxcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZU90aGVyVGFicyxcbiAgICAgICAgQ29tbWFuZElEcy5jbG9zZVJpZ2h0VGFicyxcbiAgICAgICAgQ29tbWFuZElEcy50b2dnbGVIZWFkZXIsXG4gICAgICAgIENvbW1hbmRJRHMudG9nZ2xlTGVmdEFyZWEsXG4gICAgICAgIENvbW1hbmRJRHMudG9nZ2xlUmlnaHRBcmVhLFxuICAgICAgICBDb21tYW5kSURzLnRvZ2dsZVByZXNlbnRhdGlvbk1vZGUsXG4gICAgICAgIENvbW1hbmRJRHMudG9nZ2xlTW9kZSxcbiAgICAgICAgQ29tbWFuZElEcy5yZXNldExheW91dFxuICAgICAgXS5mb3JFYWNoKGNvbW1hbmQgPT4gcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZCwgY2F0ZWdvcnkgfSkpO1xuXG4gICAgICBbJ3JpZ2h0JywgJ2xlZnQnXS5mb3JFYWNoKHNpZGUgPT4ge1xuICAgICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMudG9nZ2xlU2lkZVRhYkJhcixcbiAgICAgICAgICBjYXRlZ29yeSxcbiAgICAgICAgICBhcmdzOiB7IHNpZGUgfVxuICAgICAgICB9KTtcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgbWFpbiBleHRlbnNpb24uXG4gKi9cbmNvbnN0IG1haW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJVHJlZVBhdGhVcGRhdGVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246bWFpbicsXG4gIGRlc2NyaXB0aW9uOlxuICAgICdJbml0aWFsaXplcyB0aGUgYXBwbGljYXRpb24gYW5kIHByb3ZpZGVzIHRoZSBVUkwgdHJlZSBwYXRoIGhhbmRsZXIuJyxcbiAgcmVxdWlyZXM6IFtcbiAgICBJUm91dGVyLFxuICAgIElXaW5kb3dSZXNvbHZlcixcbiAgICBJVHJhbnNsYXRvcixcbiAgICBKdXB5dGVyRnJvbnRFbmQuSVRyZWVSZXNvbHZlclxuICBdLFxuICBvcHRpb25hbDogW0lDb25uZWN0aW9uTG9zdF0sXG4gIHByb3ZpZGVzOiBJVHJlZVBhdGhVcGRhdGVyLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHJvdXRlcjogSVJvdXRlcixcbiAgICByZXNvbHZlcjogSVdpbmRvd1Jlc29sdmVyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHRyZWVSZXNvbHZlcjogSnVweXRlckZyb250RW5kLklUcmVlUmVzb2x2ZXIsXG4gICAgY29ubmVjdGlvbkxvc3Q6IElDb25uZWN0aW9uTG9zdCB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIGlmICghKGFwcCBpbnN0YW5jZW9mIEp1cHl0ZXJMYWIpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYCR7bWFpbi5pZH0gbXVzdCBiZSBhY3RpdmF0ZWQgaW4gSnVweXRlckxhYi5gKTtcbiAgICB9XG5cbiAgICAvLyBUaGVzZSB0d28gaW50ZXJuYWwgc3RhdGUgdmFyaWFibGVzIGFyZSB1c2VkIHRvIG1hbmFnZSB0aGUgdHdvIHNvdXJjZVxuICAgIC8vIG9mIHRoZSB0cmVlIHBhcnQgb2YgdGhlIFVSTCBiZWluZyB1cGRhdGVkOiAxKSBwYXRoIG9mIHRoZSBhY3RpdmUgZG9jdW1lbnQsXG4gICAgLy8gMikgcGF0aCBvZiB0aGUgZGVmYXVsdCBicm93c2VyIGlmIHRoZSBhY3RpdmUgbWFpbiBhcmVhIHdpZGdldCBpc24ndCBhIGRvY3VtZW50LlxuICAgIGxldCBfZG9jVHJlZVBhdGggPSAnJztcbiAgICBsZXQgX2RlZmF1bHRCcm93c2VyVHJlZVBhdGggPSAnJztcblxuICAgIGZ1bmN0aW9uIHVwZGF0ZVRyZWVQYXRoKHRyZWVQYXRoOiBzdHJpbmcpIHtcbiAgICAgIC8vIFdhaXQgZm9yIHRyZWUgcmVzb2x2ZXIgdG8gZmluaXNoIGJlZm9yZSB1cGRhdGluZyB0aGUgcGF0aCBiZWNhdXNlIGl0IHVzZSB0aGUgUGFnZUNvbmZpZ1sndHJlZVBhdGgnXVxuICAgICAgdm9pZCB0cmVlUmVzb2x2ZXIucGF0aHMudGhlbigoKSA9PiB7XG4gICAgICAgIF9kZWZhdWx0QnJvd3NlclRyZWVQYXRoID0gdHJlZVBhdGg7XG4gICAgICAgIGlmICghX2RvY1RyZWVQYXRoKSB7XG4gICAgICAgICAgY29uc3QgdXJsID0gUGFnZUNvbmZpZy5nZXRVcmwoeyB0cmVlUGF0aCB9KTtcbiAgICAgICAgICBjb25zdCBwYXRoID0gVVJMRXh0LnBhcnNlKHVybCkucGF0aG5hbWU7XG4gICAgICAgICAgcm91dGVyLm5hdmlnYXRlKHBhdGgsIHsgc2tpcFJvdXRpbmc6IHRydWUgfSk7XG4gICAgICAgICAgLy8gUGVyc2lzdCB0aGUgbmV3IHRyZWUgcGF0aCB0byBQYWdlQ29uZmlnIGFzIGl0IGlzIHVzZWQgZWxzZXdoZXJlIGF0IHJ1bnRpbWUuXG4gICAgICAgICAgUGFnZUNvbmZpZy5zZXRPcHRpb24oJ3RyZWVQYXRoJywgdHJlZVBhdGgpO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvLyBSZXF1aXJpbmcgdGhlIHdpbmRvdyByZXNvbHZlciBndWFyYW50ZWVzIHRoYXQgdGhlIGFwcGxpY2F0aW9uIGV4dGVuc2lvblxuICAgIC8vIG9ubHkgbG9hZHMgaWYgdGhlcmUgaXMgYSB2aWFibGUgd2luZG93IG5hbWUuIE90aGVyd2lzZSwgdGhlIGFwcGxpY2F0aW9uXG4gICAgLy8gd2lsbCBzaG9ydC1jaXJjdWl0IGFuZCBhc2sgdGhlIHVzZXIgdG8gbmF2aWdhdGUgYXdheS5cbiAgICBjb25zdCB3b3Jrc3BhY2UgPSByZXNvbHZlci5uYW1lO1xuXG4gICAgY29uc29sZS5kZWJ1ZyhgU3RhcnRpbmcgYXBwbGljYXRpb24gaW4gd29ya3NwYWNlOiBcIiR7d29ya3NwYWNlfVwiYCk7XG5cbiAgICAvLyBJZiB0aGVyZSB3ZXJlIGVycm9ycyByZWdpc3RlcmluZyBwbHVnaW5zLCB0ZWxsIHRoZSB1c2VyLlxuICAgIGlmIChhcHAucmVnaXN0ZXJQbHVnaW5FcnJvcnMubGVuZ3RoICE9PSAwKSB7XG4gICAgICBjb25zdCBib2R5ID0gKFxuICAgICAgICA8cHJlPnthcHAucmVnaXN0ZXJQbHVnaW5FcnJvcnMubWFwKGUgPT4gZS5tZXNzYWdlKS5qb2luKCdcXG4nKX08L3ByZT5cbiAgICAgICk7XG5cbiAgICAgIHZvaWQgc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnRXJyb3IgUmVnaXN0ZXJpbmcgUGx1Z2lucycpLCB7XG4gICAgICAgIG1lc3NhZ2U6IGJvZHlcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8vIElmIHRoZSBhcHBsaWNhdGlvbiBzaGVsbCBsYXlvdXQgaXMgbW9kaWZpZWQsXG4gICAgLy8gdHJpZ2dlciBhIHJlZnJlc2ggb2YgdGhlIGNvbW1hbmRzLlxuICAgIGFwcC5zaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZCgpO1xuICAgIH0pO1xuXG4gICAgLy8gV2F0Y2ggdGhlIG1vZGUgYW5kIHVwZGF0ZSB0aGUgcGFnZSBVUkwgdG8gL2xhYiBvciAvZG9jIHRvIHJlZmxlY3QgdGhlXG4gICAgLy8gY2hhbmdlLlxuICAgIGFwcC5zaGVsbC5tb2RlQ2hhbmdlZC5jb25uZWN0KChfLCBhcmdzOiBEb2NrUGFuZWwuTW9kZSkgPT4ge1xuICAgICAgY29uc3QgdXJsID0gUGFnZUNvbmZpZy5nZXRVcmwoeyBtb2RlOiBhcmdzIGFzIHN0cmluZyB9KTtcbiAgICAgIGNvbnN0IHBhdGggPSBVUkxFeHQucGFyc2UodXJsKS5wYXRobmFtZTtcbiAgICAgIHJvdXRlci5uYXZpZ2F0ZShwYXRoLCB7IHNraXBSb3V0aW5nOiB0cnVlIH0pO1xuICAgICAgLy8gUGVyc2lzdCB0aGlzIG1vZGUgY2hhbmdlIHRvIFBhZ2VDb25maWcgYXMgaXQgaXMgdXNlZCBlbHNld2hlcmUgYXQgcnVudGltZS5cbiAgICAgIFBhZ2VDb25maWcuc2V0T3B0aW9uKCdtb2RlJywgYXJncyBhcyBzdHJpbmcpO1xuICAgIH0pO1xuXG4gICAgLy8gV2FpdCBmb3IgdHJlZSByZXNvbHZlciB0byBmaW5pc2ggYmVmb3JlIHVwZGF0aW5nIHRoZSBwYXRoIGJlY2F1c2UgaXQgdXNlIHRoZSBQYWdlQ29uZmlnWyd0cmVlUGF0aCddXG4gICAgdm9pZCB0cmVlUmVzb2x2ZXIucGF0aHMudGhlbigoKSA9PiB7XG4gICAgICAvLyBXYXRjaCB0aGUgcGF0aCBvZiB0aGUgY3VycmVudCB3aWRnZXQgaW4gdGhlIG1haW4gYXJlYSBhbmQgdXBkYXRlIHRoZSBwYWdlXG4gICAgICAvLyBVUkwgdG8gcmVmbGVjdCB0aGUgY2hhbmdlLlxuICAgICAgYXBwLnNoZWxsLmN1cnJlbnRQYXRoQ2hhbmdlZC5jb25uZWN0KChfLCBhcmdzKSA9PiB7XG4gICAgICAgIGNvbnN0IG1heWJlVHJlZVBhdGggPSBhcmdzLm5ld1ZhbHVlIGFzIHN0cmluZztcbiAgICAgICAgY29uc3QgdHJlZVBhdGggPSBtYXliZVRyZWVQYXRoIHx8IF9kZWZhdWx0QnJvd3NlclRyZWVQYXRoO1xuICAgICAgICBjb25zdCB1cmwgPSBQYWdlQ29uZmlnLmdldFVybCh7IHRyZWVQYXRoOiB0cmVlUGF0aCB9KTtcbiAgICAgICAgY29uc3QgcGF0aCA9IFVSTEV4dC5wYXJzZSh1cmwpLnBhdGhuYW1lO1xuICAgICAgICByb3V0ZXIubmF2aWdhdGUocGF0aCwgeyBza2lwUm91dGluZzogdHJ1ZSB9KTtcbiAgICAgICAgLy8gUGVyc2lzdCB0aGUgbmV3IHRyZWUgcGF0aCB0byBQYWdlQ29uZmlnIGFzIGl0IGlzIHVzZWQgZWxzZXdoZXJlIGF0IHJ1bnRpbWUuXG4gICAgICAgIFBhZ2VDb25maWcuc2V0T3B0aW9uKCd0cmVlUGF0aCcsIHRyZWVQYXRoKTtcbiAgICAgICAgX2RvY1RyZWVQYXRoID0gbWF5YmVUcmVlUGF0aDtcbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgLy8gSWYgdGhlIGNvbm5lY3Rpb24gdG8gdGhlIHNlcnZlciBpcyBsb3N0LCBoYW5kbGUgaXQgd2l0aCB0aGVcbiAgICAvLyBjb25uZWN0aW9uIGxvc3QgaGFuZGxlci5cbiAgICBjb25uZWN0aW9uTG9zdCA9IGNvbm5lY3Rpb25Mb3N0IHx8IENvbm5lY3Rpb25Mb3N0O1xuICAgIGFwcC5zZXJ2aWNlTWFuYWdlci5jb25uZWN0aW9uRmFpbHVyZS5jb25uZWN0KChtYW5hZ2VyLCBlcnJvcikgPT5cbiAgICAgIGNvbm5lY3Rpb25Mb3N0IShtYW5hZ2VyLCBlcnJvciwgdHJhbnNsYXRvcilcbiAgICApO1xuXG4gICAgY29uc3QgYnVpbGRlciA9IGFwcC5zZXJ2aWNlTWFuYWdlci5idWlsZGVyO1xuICAgIGNvbnN0IGJ1aWxkID0gKCkgPT4ge1xuICAgICAgcmV0dXJuIGJ1aWxkZXJcbiAgICAgICAgLmJ1aWxkKClcbiAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnQnVpbGQgQ29tcGxldGUnKSxcbiAgICAgICAgICAgIGJvZHk6IChcbiAgICAgICAgICAgICAgPGRpdj5cbiAgICAgICAgICAgICAgICB7dHJhbnMuX18oJ0J1aWxkIHN1Y2Nlc3NmdWxseSBjb21wbGV0ZWQsIHJlbG9hZCBwYWdlPycpfVxuICAgICAgICAgICAgICAgIDxiciAvPlxuICAgICAgICAgICAgICAgIHt0cmFucy5fXygnWW91IHdpbGwgbG9zZSBhbnkgdW5zYXZlZCBjaGFuZ2VzLicpfVxuICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICksXG4gICAgICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oe1xuICAgICAgICAgICAgICAgIGxhYmVsOiB0cmFucy5fXygnUmVsb2FkIFdpdGhvdXQgU2F2aW5nJyksXG4gICAgICAgICAgICAgICAgYWN0aW9uczogWydyZWxvYWQnXVxuICAgICAgICAgICAgICB9KSxcbiAgICAgICAgICAgICAgRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdTYXZlIGFuZCBSZWxvYWQnKSB9KVxuICAgICAgICAgICAgXSxcbiAgICAgICAgICAgIGhhc0Nsb3NlOiB0cnVlXG4gICAgICAgICAgfSk7XG4gICAgICAgIH0pXG4gICAgICAgIC50aGVuKCh7IGJ1dHRvbjogeyBhY2NlcHQsIGFjdGlvbnMgfSB9KSA9PiB7XG4gICAgICAgICAgaWYgKGFjY2VwdCkge1xuICAgICAgICAgICAgdm9pZCBhcHAuY29tbWFuZHNcbiAgICAgICAgICAgICAgLmV4ZWN1dGUoJ2RvY21hbmFnZXI6c2F2ZScpXG4gICAgICAgICAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgICAgICAgICByb3V0ZXIucmVsb2FkKCk7XG4gICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgIC5jYXRjaChlcnIgPT4ge1xuICAgICAgICAgICAgICAgIHZvaWQgc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnU2F2ZSBGYWlsZWQnKSwge1xuICAgICAgICAgICAgICAgICAgbWVzc2FnZTogPHByZT57ZXJyLm1lc3NhZ2V9PC9wcmU+XG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH0gZWxzZSBpZiAoYWN0aW9ucy5pbmNsdWRlcygncmVsb2FkJykpIHtcbiAgICAgICAgICAgIHJvdXRlci5yZWxvYWQoKTtcbiAgICAgICAgICB9XG4gICAgICAgIH0pXG4gICAgICAgIC5jYXRjaChlcnIgPT4ge1xuICAgICAgICAgIHZvaWQgc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnQnVpbGQgRmFpbGVkJyksIHtcbiAgICAgICAgICAgIG1lc3NhZ2U6IDxwcmU+e2Vyci5tZXNzYWdlfTwvcHJlPlxuICAgICAgICAgIH0pO1xuICAgICAgICB9KTtcbiAgICB9O1xuXG4gICAgaWYgKGJ1aWxkZXIuaXNBdmFpbGFibGUgJiYgYnVpbGRlci5zaG91bGRDaGVjaykge1xuICAgICAgdm9pZCBidWlsZGVyLmdldFN0YXR1cygpLnRoZW4ocmVzcG9uc2UgPT4ge1xuICAgICAgICBpZiAocmVzcG9uc2Uuc3RhdHVzID09PSAnYnVpbGRpbmcnKSB7XG4gICAgICAgICAgcmV0dXJuIGJ1aWxkKCk7XG4gICAgICAgIH1cblxuICAgICAgICBpZiAocmVzcG9uc2Uuc3RhdHVzICE9PSAnbmVlZGVkJykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGJvZHkgPSAoXG4gICAgICAgICAgPGRpdj5cbiAgICAgICAgICAgIHt0cmFucy5fXygnSnVweXRlckxhYiBidWlsZCBpcyBzdWdnZXN0ZWQ6Jyl9XG4gICAgICAgICAgICA8YnIgLz5cbiAgICAgICAgICAgIDxwcmU+e3Jlc3BvbnNlLm1lc3NhZ2V9PC9wcmU+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG5cbiAgICAgICAgdm9pZCBzaG93RGlhbG9nKHtcbiAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0J1aWxkIFJlY29tbWVuZGVkJyksXG4gICAgICAgICAgYm9keSxcbiAgICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKCksXG4gICAgICAgICAgICBEaWFsb2cub2tCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0J1aWxkJykgfSlcbiAgICAgICAgICBdXG4gICAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IChyZXN1bHQuYnV0dG9uLmFjY2VwdCA/IGJ1aWxkKCkgOiB1bmRlZmluZWQpKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdXBkYXRlVHJlZVBhdGg7XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBQbHVnaW4gdG8gYnVpbGQgdGhlIGNvbnRleHQgbWVudSBmcm9tIHRoZSBzZXR0aW5ncy5cbiAqL1xuY29uc3QgY29udGV4dE1lbnVQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246Y29udGV4dC1tZW51JyxcbiAgZGVzY3JpcHRpb246ICdQb3B1bGF0ZXMgdGhlIGNvbnRleHQgbWVudS4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSVNldHRpbmdSZWdpc3RyeSwgSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApOiB2b2lkID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgZnVuY3Rpb24gY3JlYXRlTWVudShvcHRpb25zOiBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51KTogUmFua2VkTWVudSB7XG4gICAgICBjb25zdCBtZW51ID0gbmV3IFJhbmtlZE1lbnUoeyAuLi5vcHRpb25zLCBjb21tYW5kczogYXBwLmNvbW1hbmRzIH0pO1xuICAgICAgaWYgKG9wdGlvbnMubGFiZWwpIHtcbiAgICAgICAgbWVudS50aXRsZS5sYWJlbCA9IHRyYW5zLl9fKG9wdGlvbnMubGFiZWwpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIG1lbnU7XG4gICAgfVxuXG4gICAgLy8gTG9hZCB0aGUgY29udGV4dCBtZW51IGxhdGVseSBzbyBwbHVnaW5zIGFyZSBsb2FkZWQuXG4gICAgYXBwLnN0YXJ0ZWRcbiAgICAgIC50aGVuKCgpID0+IHtcbiAgICAgICAgcmV0dXJuIFByaXZhdGUubG9hZFNldHRpbmdzQ29udGV4dE1lbnUoXG4gICAgICAgICAgYXBwLmNvbnRleHRNZW51LFxuICAgICAgICAgIHNldHRpbmdSZWdpc3RyeSxcbiAgICAgICAgICBjcmVhdGVNZW51LFxuICAgICAgICAgIHRyYW5zbGF0b3JcbiAgICAgICAgKTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICAnRmFpbGVkIHRvIGxvYWQgY29udGV4dCBtZW51IGl0ZW1zIGZyb20gc2V0dGluZ3MgcmVnaXN0cnkuJyxcbiAgICAgICAgICByZWFzb25cbiAgICAgICAgKTtcbiAgICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIENoZWNrIGlmIHRoZSBhcHBsaWNhdGlvbiBpcyBkaXJ0eSBiZWZvcmUgY2xvc2luZyB0aGUgYnJvd3NlciB0YWIuXG4gKi9cbmNvbnN0IGRpcnR5OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tZXh0ZW5zaW9uOmRpcnR5JyxcbiAgZGVzY3JpcHRpb246XG4gICAgJ0FkZHMgc2FmZWd1YXJkIGRpYWxvZyB3aGVuIGNsb3NpbmcgdGhlIGJyb3dzZXIgdGFiIHdpdGggdW5zYXZlZCBtb2RpZmljYXRpb25zLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yKTogdm9pZCA9PiB7XG4gICAgaWYgKCEoYXBwIGluc3RhbmNlb2YgSnVweXRlckxhYikpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgJHtkaXJ0eS5pZH0gbXVzdCBiZSBhY3RpdmF0ZWQgaW4gSnVweXRlckxhYi5gKTtcbiAgICB9XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBtZXNzYWdlID0gdHJhbnMuX18oXG4gICAgICAnQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIGV4aXQgSnVweXRlckxhYj9cXG5cXG5BbnkgdW5zYXZlZCBjaGFuZ2VzIHdpbGwgYmUgbG9zdC4nXG4gICAgKTtcblxuICAgIC8vIFRoZSBzcGVjIGZvciB0aGUgYGJlZm9yZXVubG9hZGAgZXZlbnQgaXMgaW1wbGVtZW50ZWQgZGlmZmVyZW50bHkgYnlcbiAgICAvLyB0aGUgZGlmZmVyZW50IGJyb3dzZXIgdmVuZG9ycy4gQ29uc2VxdWVudGx5LCB0aGUgYGV2ZW50LnJldHVyblZhbHVlYFxuICAgIC8vIGF0dHJpYnV0ZSBuZWVkcyB0byBzZXQgaW4gYWRkaXRpb24gdG8gYSByZXR1cm4gdmFsdWUgYmVpbmcgcmV0dXJuZWQuXG4gICAgLy8gRm9yIG1vcmUgaW5mb3JtYXRpb24sIHNlZTpcbiAgICAvLyBodHRwczovL2RldmVsb3Blci5tb3ppbGxhLm9yZy9lbi9kb2NzL1dlYi9FdmVudHMvYmVmb3JldW5sb2FkXG4gICAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ2JlZm9yZXVubG9hZCcsIGV2ZW50ID0+IHtcbiAgICAgIGlmIChhcHAuc3RhdHVzLmlzRGlydHkpIHtcbiAgICAgICAgcmV0dXJuICgoZXZlbnQgYXMgYW55KS5yZXR1cm5WYWx1ZSA9IG1lc3NhZ2UpO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGxheW91dCByZXN0b3JlciBwcm92aWRlci5cbiAqL1xuY29uc3QgbGF5b3V0OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUxheW91dFJlc3RvcmVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246bGF5b3V0JyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgc2hlbGwgbGF5b3V0IHJlc3RvcmVyLicsXG4gIHJlcXVpcmVzOiBbSVN0YXRlREIsIElMYWJTaGVsbCwgSVNldHRpbmdSZWdpc3RyeV0sXG4gIG9wdGlvbmFsOiBbSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHN0YXRlOiBJU3RhdGVEQixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsLFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvciB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSAodHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvcikubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGZpcnN0ID0gYXBwLnN0YXJ0ZWQ7XG4gICAgY29uc3QgcmVnaXN0cnkgPSBhcHAuY29tbWFuZHM7XG5cbiAgICBjb25zdCBtb2RlID0gUGFnZUNvbmZpZy5nZXRPcHRpb24oJ21vZGUnKSBhcyBEb2NrUGFuZWwuTW9kZTtcbiAgICBjb25zdCByZXN0b3JlciA9IG5ldyBMYXlvdXRSZXN0b3Jlcih7XG4gICAgICBjb25uZWN0b3I6IHN0YXRlLFxuICAgICAgZmlyc3QsXG4gICAgICByZWdpc3RyeSxcbiAgICAgIG1vZGVcbiAgICB9KTtcbiAgICBzZXR0aW5nUmVnaXN0cnlcbiAgICAgIC5sb2FkKHNoZWxsLmlkKVxuICAgICAgLnRoZW4oc2V0dGluZ3MgPT4ge1xuICAgICAgICAvLyBBZGQgYSBsYXllciBvZiBjdXN0b21pemF0aW9uIHRvIHN1cHBvcnQgYXBwIHNoZWxsIG1vZGVcbiAgICAgICAgY29uc3QgY3VzdG9taXplZExheW91dCA9IHNldHRpbmdzLmNvbXBvc2l0ZVsnbGF5b3V0J10gYXMgYW55O1xuXG4gICAgICAgIC8vIFJlc3RvcmUgdGhlIGxheW91dC5cbiAgICAgICAgdm9pZCBsYWJTaGVsbFxuICAgICAgICAgIC5yZXN0b3JlTGF5b3V0KG1vZGUsIHJlc3RvcmVyLCB7XG4gICAgICAgICAgICAnbXVsdGlwbGUtZG9jdW1lbnQnOiBjdXN0b21pemVkTGF5b3V0Lm11bHRpcGxlID8/IHt9LFxuICAgICAgICAgICAgJ3NpbmdsZS1kb2N1bWVudCc6IGN1c3RvbWl6ZWRMYXlvdXQuc2luZ2xlID8/IHt9XG4gICAgICAgICAgfSlcbiAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICBsYWJTaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICAgICAgdm9pZCByZXN0b3Jlci5zYXZlKGxhYlNoZWxsLnNhdmVMYXlvdXQoKSk7XG4gICAgICAgICAgICB9KTtcblxuICAgICAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KG9uU2V0dGluZ3NDaGFuZ2VkKTtcbiAgICAgICAgICAgIFByaXZhdGUuYWN0aXZhdGVTaWRlYmFyU3dpdGNoZXIoYXBwLCBsYWJTaGVsbCwgc2V0dGluZ3MsIHRyYW5zKTtcbiAgICAgICAgICB9KTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcignRmFpbCB0byBsb2FkIHNldHRpbmdzIGZvciB0aGUgbGF5b3V0IHJlc3RvcmVyLicpO1xuICAgICAgICBjb25zb2xlLmVycm9yKHJlYXNvbik7XG4gICAgICB9KTtcblxuICAgIHJldHVybiByZXN0b3JlcjtcblxuICAgIGFzeW5jIGZ1bmN0aW9uIG9uU2V0dGluZ3NDaGFuZ2VkKFxuICAgICAgc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzXG4gICAgKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICBpZiAoXG4gICAgICAgICFKU09ORXh0LmRlZXBFcXVhbChcbiAgICAgICAgICBzZXR0aW5ncy5jb21wb3NpdGVbJ2xheW91dCddIGFzIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSxcbiAgICAgICAgICB7XG4gICAgICAgICAgICBzaW5nbGU6IGxhYlNoZWxsLnVzZXJMYXlvdXRbJ3NpbmdsZS1kb2N1bWVudCddLFxuICAgICAgICAgICAgbXVsdGlwbGU6IGxhYlNoZWxsLnVzZXJMYXlvdXRbJ211bHRpcGxlLWRvY3VtZW50J11cbiAgICAgICAgICB9IGFzIGFueVxuICAgICAgICApXG4gICAgICApIHtcbiAgICAgICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgc2hvd0RpYWxvZyh7XG4gICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdJbmZvcm1hdGlvbicpLFxuICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAgICAgJ1VzZXIgbGF5b3V0IGN1c3RvbWl6YXRpb24gaGFzIGNoYW5nZWQuIFlvdSBtYXkgbmVlZCB0byByZWxvYWQgSnVweXRlckxhYiB0byBzZWUgdGhlIGNoYW5nZXMuJ1xuICAgICAgICAgICksXG4gICAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbigpLFxuICAgICAgICAgICAgRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdSZWxvYWQnKSB9KVxuICAgICAgICAgIF1cbiAgICAgICAgfSk7XG5cbiAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgICAgbG9jYXRpb24ucmVsb2FkKCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcHJvdmlkZXM6IElMYXlvdXRSZXN0b3JlclxufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBVUkwgcm91dGVyIHByb3ZpZGVyLlxuICovXG5jb25zdCByb3V0ZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJUm91dGVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246cm91dGVyJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgVVJMIHJvdXRlcicsXG4gIHJlcXVpcmVzOiBbSnVweXRlckZyb250RW5kLklQYXRoc10sXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIHBhdGhzOiBKdXB5dGVyRnJvbnRFbmQuSVBhdGhzKSA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IGJhc2UgPSBwYXRocy51cmxzLmJhc2U7XG4gICAgY29uc3Qgcm91dGVyID0gbmV3IFJvdXRlcih7IGJhc2UsIGNvbW1hbmRzIH0pO1xuXG4gICAgdm9pZCBhcHAuc3RhcnRlZC50aGVuKCgpID0+IHtcbiAgICAgIC8vIFJvdXRlIHRoZSB2ZXJ5IGZpcnN0IHJlcXVlc3Qgb24gbG9hZC5cbiAgICAgIHZvaWQgcm91dGVyLnJvdXRlKCk7XG5cbiAgICAgIC8vIFJvdXRlIGFsbCBwb3Agc3RhdGUgZXZlbnRzLlxuICAgICAgd2luZG93LmFkZEV2ZW50TGlzdGVuZXIoJ3BvcHN0YXRlJywgKCkgPT4ge1xuICAgICAgICB2b2lkIHJvdXRlci5yb3V0ZSgpO1xuICAgICAgfSk7XG4gICAgfSk7XG5cbiAgICByZXR1cm4gcm91dGVyO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJUm91dGVyXG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHRyZWUgcm91dGUgcmVzb2x2ZXIgcGx1Z2luLlxuICovXG5jb25zdCB0cmVlOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SnVweXRlckZyb250RW5kLklUcmVlUmVzb2x2ZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjp0cmVlLXJlc29sdmVyJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgdHJlZSByb3V0ZSByZXNvbHZlcicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJUm91dGVyXSxcbiAgcHJvdmlkZXM6IEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHJvdXRlcjogSVJvdXRlclxuICApOiBKdXB5dGVyRnJvbnRFbmQuSVRyZWVSZXNvbHZlciA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbnN0IHNldCA9IG5ldyBEaXNwb3NhYmxlU2V0KCk7XG4gICAgY29uc3QgZGVsZWdhdGUgPSBuZXcgUHJvbWlzZURlbGVnYXRlPEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyLlBhdGhzPigpO1xuXG4gICAgY29uc3QgdHJlZVBhdHRlcm4gPSBuZXcgUmVnRXhwKFxuICAgICAgJy8obGFifGRvYykoL3dvcmtzcGFjZXMvW2EtekEtWjAtOS1fXSspPygvdHJlZS8uKik/J1xuICAgICk7XG5cbiAgICBzZXQuYWRkKFxuICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRyZWUsIHtcbiAgICAgICAgZXhlY3V0ZTogYXN5bmMgKGFyZ3M6IElSb3V0ZXIuSUxvY2F0aW9uKSA9PiB7XG4gICAgICAgICAgaWYgKHNldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgY29uc3QgcXVlcnkgPSBVUkxFeHQucXVlcnlTdHJpbmdUb09iamVjdChhcmdzLnNlYXJjaCA/PyAnJyk7XG4gICAgICAgICAgY29uc3QgYnJvd3NlciA9IHF1ZXJ5WydmaWxlLWJyb3dzZXItcGF0aCddIHx8ICcnO1xuXG4gICAgICAgICAgLy8gUmVtb3ZlIHRoZSBmaWxlIGJyb3dzZXIgcGF0aCBmcm9tIHRoZSBxdWVyeSBzdHJpbmcuXG4gICAgICAgICAgZGVsZXRlIHF1ZXJ5WydmaWxlLWJyb3dzZXItcGF0aCddO1xuXG4gICAgICAgICAgLy8gQ2xlYW4gdXAgYXJ0aWZhY3RzIGltbWVkaWF0ZWx5IHVwb24gcm91dGluZy5cbiAgICAgICAgICBzZXQuZGlzcG9zZSgpO1xuXG4gICAgICAgICAgZGVsZWdhdGUucmVzb2x2ZSh7IGJyb3dzZXIsIGZpbGU6IFBhZ2VDb25maWcuZ2V0T3B0aW9uKCd0cmVlUGF0aCcpIH0pO1xuICAgICAgICB9XG4gICAgICB9KVxuICAgICk7XG4gICAgc2V0LmFkZChcbiAgICAgIHJvdXRlci5yZWdpc3Rlcih7IGNvbW1hbmQ6IENvbW1hbmRJRHMudHJlZSwgcGF0dGVybjogdHJlZVBhdHRlcm4gfSlcbiAgICApO1xuXG4gICAgLy8gSWYgYSByb3V0ZSBpcyBoYW5kbGVkIGJ5IHRoZSByb3V0ZXIgd2l0aG91dCB0aGUgdHJlZSBjb21tYW5kIGJlaW5nXG4gICAgLy8gaW52b2tlZCwgcmVzb2x2ZSB0byBgbnVsbGAgYW5kIGNsZWFuIHVwIGFydGlmYWN0cy5cbiAgICBjb25zdCBsaXN0ZW5lciA9ICgpID0+IHtcbiAgICAgIGlmIChzZXQuaXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBzZXQuZGlzcG9zZSgpO1xuICAgICAgZGVsZWdhdGUucmVzb2x2ZShudWxsKTtcbiAgICB9O1xuICAgIHJvdXRlci5yb3V0ZWQuY29ubmVjdChsaXN0ZW5lcik7XG4gICAgc2V0LmFkZChcbiAgICAgIG5ldyBEaXNwb3NhYmxlRGVsZWdhdGUoKCkgPT4ge1xuICAgICAgICByb3V0ZXIucm91dGVkLmRpc2Nvbm5lY3QobGlzdGVuZXIpO1xuICAgICAgfSlcbiAgICApO1xuXG4gICAgcmV0dXJuIHsgcGF0aHM6IGRlbGVnYXRlLnByb21pc2UgfTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBVUkwgbm90IGZvdW5kIGV4dGVuc2lvbi5cbiAqL1xuY29uc3Qgbm90Zm91bmQ6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246bm90Zm91bmQnLFxuICBkZXNjcmlwdGlvbjogJ0RlZmluZXMgdGhlIGJlaGF2aW9yIGZvciBub3QgZm91bmQgVVJMIChha2Egcm91dGUpLicsXG4gIHJlcXVpcmVzOiBbSnVweXRlckZyb250RW5kLklQYXRocywgSVJvdXRlciwgSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIF86IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBwYXRoczogSnVweXRlckZyb250RW5kLklQYXRocyxcbiAgICByb3V0ZXI6IElSb3V0ZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBiYWQgPSBwYXRocy51cmxzLm5vdEZvdW5kO1xuXG4gICAgaWYgKCFiYWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBiYXNlID0gcm91dGVyLmJhc2U7XG4gICAgY29uc3QgbWVzc2FnZSA9IHRyYW5zLl9fKFxuICAgICAgJ1RoZSBwYXRoOiAlMSB3YXMgbm90IGZvdW5kLiBKdXB5dGVyTGFiIHJlZGlyZWN0ZWQgdG86ICUyJyxcbiAgICAgIGJhZCxcbiAgICAgIGJhc2VcbiAgICApO1xuXG4gICAgLy8gQ2hhbmdlIHRoZSBVUkwgYmFjayB0byB0aGUgYmFzZSBhcHBsaWNhdGlvbiBVUkwuXG4gICAgcm91dGVyLm5hdmlnYXRlKCcnKTtcblxuICAgIHZvaWQgc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnUGF0aCBOb3QgRm91bmQnKSwgeyBtZXNzYWdlIH0pO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogQ2hhbmdlIHRoZSBmYXZpY29uIGNoYW5naW5nIGJhc2VkIG9uIHRoZSBidXN5IHN0YXR1cztcbiAqL1xuY29uc3QgYnVzeTogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpmYXZpY29uYnVzeScsXG4gIGRlc2NyaXB0aW9uOiAnSGFuZGxlcyB0aGUgZmF2aWNvbiBkZXBlbmRpbmcgb24gdGhlIGFwcGxpY2F0aW9uIHN0YXR1cy4nLFxuICByZXF1aXJlczogW0lMYWJTdGF0dXNdLFxuICBhY3RpdmF0ZTogYXN5bmMgKF86IEp1cHl0ZXJGcm9udEVuZCwgc3RhdHVzOiBJTGFiU3RhdHVzKSA9PiB7XG4gICAgc3RhdHVzLmJ1c3lTaWduYWwuY29ubmVjdCgoXywgaXNCdXN5KSA9PiB7XG4gICAgICBjb25zdCBmYXZpY29uID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcbiAgICAgICAgYGxpbmtbcmVsPVwiaWNvblwiXSR7aXNCdXN5ID8gJy5pZGxlLmZhdmljb24nIDogJy5idXN5LmZhdmljb24nfWBcbiAgICAgICkgYXMgSFRNTExpbmtFbGVtZW50O1xuICAgICAgaWYgKCFmYXZpY29uKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IG5ld0Zhdmljb24gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFxuICAgICAgICBgbGluayR7aXNCdXN5ID8gJy5idXN5LmZhdmljb24nIDogJy5pZGxlLmZhdmljb24nfWBcbiAgICAgICkgYXMgSFRNTExpbmtFbGVtZW50O1xuICAgICAgaWYgKCFuZXdGYXZpY29uKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIC8vIElmIHdlIGhhdmUgdGhlIHR3byBpY29ucyB3aXRoIHRoZSBzcGVjaWFsIGNsYXNzZXMsIHRoZW4gdG9nZ2xlIHRoZW0uXG4gICAgICBpZiAoZmF2aWNvbiAhPT0gbmV3RmF2aWNvbikge1xuICAgICAgICBmYXZpY29uLnJlbCA9ICcnO1xuICAgICAgICBuZXdGYXZpY29uLnJlbCA9ICdpY29uJztcblxuICAgICAgICAvLyBGaXJlZm94IGRvZXNuJ3Qgc2VlbSB0byByZWNvZ25pemUganVzdCBjaGFuZ2luZyByZWwsIHNvIHdlIGFsc29cbiAgICAgICAgLy8gcmVpbnNlcnQgdGhlIGxpbmsgaW50byB0aGUgRE9NLlxuICAgICAgICBuZXdGYXZpY29uLnBhcmVudE5vZGUhLnJlcGxhY2VDaGlsZChuZXdGYXZpY29uLCBuZXdGYXZpY29uKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IEp1cHl0ZXJMYWIgYXBwbGljYXRpb24gc2hlbGwuXG4gKi9cbmNvbnN0IHNoZWxsOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUxhYlNoZWxsPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246c2hlbGwnLFxuICBkZXNjcmlwdGlvbjpcbiAgICAnUHJvdmlkZXMgdGhlIEp1cHl0ZXJMYWIgc2hlbGwuIEl0IGhhcyBhbiBleHRlbmRlZCBBUEkgY29tcGFyZWQgdG8gYGFwcC5zaGVsbGAuJyxcbiAgb3B0aW9uYWw6IFtJU2V0dGluZ1JlZ2lzdHJ5XSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsXG4gICkgPT4ge1xuICAgIGlmICghKGFwcC5zaGVsbCBpbnN0YW5jZW9mIExhYlNoZWxsKSkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKGAke3NoZWxsLmlkfSBkaWQgbm90IGZpbmQgYSBMYWJTaGVsbCBpbnN0YW5jZS5gKTtcbiAgICB9XG4gICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgdm9pZCBzZXR0aW5nUmVnaXN0cnkubG9hZChzaGVsbC5pZCkudGhlbihzZXR0aW5ncyA9PiB7XG4gICAgICAgIChhcHAuc2hlbGwgYXMgTGFiU2hlbGwpLnVwZGF0ZUNvbmZpZyhzZXR0aW5ncy5jb21wb3NpdGUpO1xuICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICAgIChhcHAuc2hlbGwgYXMgTGFiU2hlbGwpLnVwZGF0ZUNvbmZpZyhzZXR0aW5ncy5jb21wb3NpdGUpO1xuICAgICAgICB9KTtcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gYXBwLnNoZWxsO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJTGFiU2hlbGxcbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgSnVweXRlckxhYiBhcHBsaWNhdGlvbiBzdGF0dXMgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHN0YXR1czogSnVweXRlckZyb250RW5kUGx1Z2luPElMYWJTdGF0dXM+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpzdGF0dXMnLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBhcHBsaWNhdGlvbiBzdGF0dXMuJyxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCkgPT4ge1xuICAgIGlmICghKGFwcCBpbnN0YW5jZW9mIEp1cHl0ZXJMYWIpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYCR7c3RhdHVzLmlkfSBtdXN0IGJlIGFjdGl2YXRlZCBpbiBKdXB5dGVyTGFiLmApO1xuICAgIH1cbiAgICByZXR1cm4gYXBwLnN0YXR1cztcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSUxhYlN0YXR1c1xufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBKdXB5dGVyTGFiIGFwcGxpY2F0aW9uLXNwZWNpZmljIGluZm9ybWF0aW9uIHByb3ZpZGVyLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoaXMgcGx1Z2luIHNob3VsZCBvbmx5IGJlIHVzZWQgYnkgcGx1Z2lucyB0aGF0IHNwZWNpZmljYWxseSBuZWVkIHRvIGFjY2Vzc1xuICogSnVweXRlckxhYiBhcHBsaWNhdGlvbiBpbmZvcm1hdGlvbiwgZS5nLiwgbGlzdGluZyBleHRlbnNpb25zIHRoYXQgaGF2ZSBiZWVuXG4gKiBsb2FkZWQgb3IgZGVmZXJyZWQgd2l0aGluIEp1cHl0ZXJMYWIuXG4gKi9cbmNvbnN0IGluZm86IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxKdXB5dGVyTGFiLklJbmZvPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246aW5mbycsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGFwcGxpY2F0aW9uIGluZm9ybWF0aW9uLicsXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQpID0+IHtcbiAgICBpZiAoIShhcHAgaW5zdGFuY2VvZiBKdXB5dGVyTGFiKSkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKGAke2luZm8uaWR9IG11c3QgYmUgYWN0aXZhdGVkIGluIEp1cHl0ZXJMYWIuYCk7XG4gICAgfVxuICAgIHJldHVybiBhcHAuaW5mbztcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSnVweXRlckxhYi5JSW5mb1xufTtcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBKdXB5dGVyTGFiIHBhdGhzIGRpY3Rpb25hcnkgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IHBhdGhzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SnVweXRlckZyb250RW5kLklQYXRocz4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tZXh0ZW5zaW9uOnBhdGhzJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgYXBwbGljYXRpb24gcGF0aHMuJyxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCk6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHMgPT4ge1xuICAgIGlmICghKGFwcCBpbnN0YW5jZW9mIEp1cHl0ZXJMYWIpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYCR7cGF0aHMuaWR9IG11c3QgYmUgYWN0aXZhdGVkIGluIEp1cHl0ZXJMYWIuYCk7XG4gICAgfVxuICAgIHJldHVybiBhcHAucGF0aHM7XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcHJvdmlkZXM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHNcbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLlxuICovXG5jb25zdCBwcm9wZXJ0eUluc3BlY3RvcjogSnVweXRlckZyb250RW5kUGx1Z2luPElQcm9wZXJ0eUluc3BlY3RvclByb3ZpZGVyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246cHJvcGVydHktaW5zcGVjdG9yJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgcHJvcGVydHkgaW5zcGVjdG9yLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJTGFiU2hlbGwsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJTGF5b3V0UmVzdG9yZXJdLFxuICBwcm92aWRlczogSVByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXIsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbGFic2hlbGw6IElMYWJTaGVsbCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHdpZGdldCA9IG5ldyBTaWRlQmFyUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlcih7XG4gICAgICBzaGVsbDogbGFic2hlbGwsXG4gICAgICB0cmFuc2xhdG9yXG4gICAgfSk7XG4gICAgd2lkZ2V0LnRpdGxlLmljb24gPSBidWlsZEljb247XG4gICAgd2lkZ2V0LnRpdGxlLmNhcHRpb24gPSB0cmFucy5fXygnUHJvcGVydHkgSW5zcGVjdG9yJyk7XG4gICAgd2lkZ2V0LmlkID0gJ2pwLXByb3BlcnR5LWluc3BlY3Rvcic7XG4gICAgbGFic2hlbGwuYWRkKHdpZGdldCwgJ3JpZ2h0JywgeyByYW5rOiAxMDAsIHR5cGU6ICdQcm9wZXJ0eSBJbnNwZWN0b3InIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaG93UHJvcGVydHlQYW5lbCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdQcm9wZXJ0eSBJbnNwZWN0b3InKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgbGFic2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBpZiAocmVzdG9yZXIpIHtcbiAgICAgIHJlc3RvcmVyLmFkZCh3aWRnZXQsICdqcC1wcm9wZXJ0eS1pbnNwZWN0b3InKTtcbiAgICB9XG4gICAgcmV0dXJuIHdpZGdldDtcbiAgfVxufTtcblxuY29uc3QganVweXRlckxvZ286IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246bG9nbycsXG4gIGRlc2NyaXB0aW9uOiAnU2V0cyB0aGUgYXBwbGljYXRpb24gbG9nby4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSUxhYlNoZWxsXSxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCwgc2hlbGw6IElMYWJTaGVsbCkgPT4ge1xuICAgIGNvbnN0IGxvZ28gPSBuZXcgV2lkZ2V0KCk7XG4gICAganVweXRlckljb24uZWxlbWVudCh7XG4gICAgICBjb250YWluZXI6IGxvZ28ubm9kZSxcbiAgICAgIGVsZW1lbnRQb3NpdGlvbjogJ2NlbnRlcicsXG4gICAgICBtYXJnaW46ICcycHggMThweCAycHggOXB4JyxcbiAgICAgIGhlaWdodDogJ2F1dG8nLFxuICAgICAgd2lkdGg6ICczMnB4J1xuICAgIH0pO1xuICAgIGxvZ28uaWQgPSAnanAtTWFpbkxvZ28nO1xuICAgIHNoZWxsLmFkZChsb2dvLCAndG9wJywgeyByYW5rOiAwIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBzaW1wbGUgaW50ZXJmYWNlIG1vZGUgc3dpdGNoIGluIHRoZSBzdGF0dXMgYmFyLlxuICovXG5jb25zdCBtb2RlU3dpdGNoUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tZXh0ZW5zaW9uOm1vZGUtc3dpdGNoJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIHRoZSBpbnRlcmZhY2UgbW9kZSBzd2l0Y2gnLFxuICByZXF1aXJlczogW0lMYWJTaGVsbCwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lTdGF0dXNCYXIsIElTZXR0aW5nUmVnaXN0cnldLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgc3RhdHVzQmFyOiBJU3RhdHVzQmFyIHwgbnVsbCxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsXG4gICkgPT4ge1xuICAgIGlmIChzdGF0dXNCYXIgPT09IG51bGwpIHtcbiAgICAgIC8vIEJhaWwgZWFybHlcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBtb2RlU3dpdGNoID0gbmV3IFN3aXRjaCgpO1xuICAgIG1vZGVTd2l0Y2guaWQgPSAnanAtc2luZ2xlLWRvY3VtZW50LW1vZGUnO1xuXG4gICAgbW9kZVN3aXRjaC52YWx1ZUNoYW5nZWQuY29ubmVjdCgoXywgYXJncykgPT4ge1xuICAgICAgbGFiU2hlbGwubW9kZSA9IGFyZ3MubmV3VmFsdWUgPyAnc2luZ2xlLWRvY3VtZW50JyA6ICdtdWx0aXBsZS1kb2N1bWVudCc7XG4gICAgfSk7XG4gICAgbGFiU2hlbGwubW9kZUNoYW5nZWQuY29ubmVjdCgoXywgbW9kZSkgPT4ge1xuICAgICAgbW9kZVN3aXRjaC52YWx1ZSA9IG1vZGUgPT09ICdzaW5nbGUtZG9jdW1lbnQnO1xuICAgIH0pO1xuXG4gICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgY29uc3QgbG9hZFNldHRpbmdzID0gc2V0dGluZ1JlZ2lzdHJ5LmxvYWQoc2hlbGwuaWQpO1xuICAgICAgY29uc3QgdXBkYXRlU2V0dGluZ3MgPSAoc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzKTogdm9pZCA9PiB7XG4gICAgICAgIGNvbnN0IHN0YXJ0TW9kZSA9IHNldHRpbmdzLmdldCgnc3RhcnRNb2RlJykuY29tcG9zaXRlIGFzIHN0cmluZztcbiAgICAgICAgaWYgKHN0YXJ0TW9kZSkge1xuICAgICAgICAgIGxhYlNoZWxsLm1vZGUgPVxuICAgICAgICAgICAgc3RhcnRNb2RlID09PSAnc2luZ2xlJyA/ICdzaW5nbGUtZG9jdW1lbnQnIDogJ211bHRpcGxlLWRvY3VtZW50JztcbiAgICAgICAgfVxuICAgICAgfTtcblxuICAgICAgUHJvbWlzZS5hbGwoW2xvYWRTZXR0aW5ncywgYXBwLnJlc3RvcmVkXSlcbiAgICAgICAgLnRoZW4oKFtzZXR0aW5nc10pID0+IHtcbiAgICAgICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICAgIH0pXG4gICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgIGNvbnNvbGUuZXJyb3IocmVhc29uLm1lc3NhZ2UpO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICAvLyBTaG93IHRoZSBjdXJyZW50IGZpbGUgYnJvd3NlciBzaG9ydGN1dCBpbiBpdHMgdGl0bGUuXG4gICAgY29uc3QgdXBkYXRlTW9kZVN3aXRjaFRpdGxlID0gKCkgPT4ge1xuICAgICAgY29uc3QgYmluZGluZyA9IGFwcC5jb21tYW5kcy5rZXlCaW5kaW5ncy5maW5kKFxuICAgICAgICBiID0+IGIuY29tbWFuZCA9PT0gJ2FwcGxpY2F0aW9uOnRvZ2dsZS1tb2RlJ1xuICAgICAgKTtcbiAgICAgIGlmIChiaW5kaW5nKSB7XG4gICAgICAgIGNvbnN0IGtzID0gYmluZGluZy5rZXlzLm1hcChDb21tYW5kUmVnaXN0cnkuZm9ybWF0S2V5c3Ryb2tlKS5qb2luKCcsICcpO1xuICAgICAgICBtb2RlU3dpdGNoLmNhcHRpb24gPSB0cmFucy5fXygnU2ltcGxlIEludGVyZmFjZSAoJTEpJywga3MpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgbW9kZVN3aXRjaC5jYXB0aW9uID0gdHJhbnMuX18oJ1NpbXBsZSBJbnRlcmZhY2UnKTtcbiAgICAgIH1cbiAgICB9O1xuICAgIHVwZGF0ZU1vZGVTd2l0Y2hUaXRsZSgpO1xuICAgIGFwcC5jb21tYW5kcy5rZXlCaW5kaW5nQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHVwZGF0ZU1vZGVTd2l0Y2hUaXRsZSgpO1xuICAgIH0pO1xuXG4gICAgbW9kZVN3aXRjaC5sYWJlbCA9IHRyYW5zLl9fKCdTaW1wbGUnKTtcblxuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0obW9kZVN3aXRjaFBsdWdpbi5pZCwge1xuICAgICAgaXRlbTogbW9kZVN3aXRjaCxcbiAgICAgIGFsaWduOiAnbGVmdCcsXG4gICAgICByYW5rOiAtMVxuICAgIH0pO1xuICB9LFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIGNvbnRleHRNZW51UGx1Z2luLFxuICBkaXJ0eSxcbiAgbWFpbixcbiAgbWFpbkNvbW1hbmRzLFxuICBsYXlvdXQsXG4gIHJvdXRlcixcbiAgdHJlZSxcbiAgbm90Zm91bmQsXG4gIGJ1c3ksXG4gIHNoZWxsLFxuICBzdGF0dXMsXG4gIGluZm8sXG4gIG1vZGVTd2l0Y2hQbHVnaW4sXG4gIHBhdGhzLFxuICBwcm9wZXJ0eUluc3BlY3RvcixcbiAganVweXRlckxvZ28sXG4gIHRvcGJhclxuXTtcblxuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcblxubmFtZXNwYWNlIFByaXZhdGUge1xuICBhc3luYyBmdW5jdGlvbiBkaXNwbGF5SW5mb3JtYXRpb24odHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgc2hvd0RpYWxvZyh7XG4gICAgICB0aXRsZTogdHJhbnMuX18oJ0luZm9ybWF0aW9uJyksXG4gICAgICBib2R5OiB0cmFucy5fXyhcbiAgICAgICAgJ0NvbnRleHQgbWVudSBjdXN0b21pemF0aW9uIGhhcyBjaGFuZ2VkLiBZb3Ugd2lsbCBuZWVkIHRvIHJlbG9hZCBKdXB5dGVyTGFiIHRvIHNlZSB0aGUgY2hhbmdlcy4nXG4gICAgICApLFxuICAgICAgYnV0dG9uczogW1xuICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKCksXG4gICAgICAgIERpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnUmVsb2FkJykgfSlcbiAgICAgIF1cbiAgICB9KTtcblxuICAgIGlmIChyZXN1bHQuYnV0dG9uLmFjY2VwdCkge1xuICAgICAgbG9jYXRpb24ucmVsb2FkKCk7XG4gICAgfVxuICB9XG5cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGxvYWRTZXR0aW5nc0NvbnRleHRNZW51KFxuICAgIGNvbnRleHRNZW51OiBDb250ZXh0TWVudVN2ZyxcbiAgICByZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICBtZW51RmFjdG9yeTogKG9wdGlvbnM6IElTZXR0aW5nUmVnaXN0cnkuSU1lbnUpID0+IFJhbmtlZE1lbnUsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBwbHVnaW5JZCA9IGNvbnRleHRNZW51UGx1Z2luLmlkO1xuICAgIGxldCBjYW5vbmljYWw6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYSB8IG51bGwgPSBudWxsO1xuICAgIGxldCBsb2FkZWQ6IHsgW25hbWU6IHN0cmluZ106IElTZXR0aW5nUmVnaXN0cnkuSUNvbnRleHRNZW51SXRlbVtdIH0gPSB7fTtcblxuICAgIC8qKlxuICAgICAqIFBvcHVsYXRlIHRoZSBwbHVnaW4ncyBzY2hlbWEgZGVmYXVsdHMuXG4gICAgICpcbiAgICAgKiBXZSBrZWVwIHRyYWNrIG9mIGRpc2FibGVkIGVudHJpZXMgaW4gY2FzZSB0aGUgcGx1Z2luIGlzIGxvYWRlZFxuICAgICAqIGFmdGVyIHRoZSBtZW51IGluaXRpYWxpemF0aW9uLlxuICAgICAqL1xuICAgIGZ1bmN0aW9uIHBvcHVsYXRlKHNjaGVtYTogSVNldHRpbmdSZWdpc3RyeS5JU2NoZW1hKSB7XG4gICAgICBsb2FkZWQgPSB7fTtcbiAgICAgIGNvbnN0IHBsdWdpbkRlZmF1bHRzID0gT2JqZWN0LmtleXMocmVnaXN0cnkucGx1Z2lucylcbiAgICAgICAgLm1hcChwbHVnaW4gPT4ge1xuICAgICAgICAgIGNvbnN0IGl0ZW1zID1cbiAgICAgICAgICAgIHJlZ2lzdHJ5LnBsdWdpbnNbcGx1Z2luXSEuc2NoZW1hWydqdXB5dGVyLmxhYi5tZW51cyddPy5jb250ZXh0ID8/XG4gICAgICAgICAgICBbXTtcbiAgICAgICAgICBsb2FkZWRbcGx1Z2luXSA9IGl0ZW1zO1xuICAgICAgICAgIHJldHVybiBpdGVtcztcbiAgICAgICAgfSlcbiAgICAgICAgLmNvbmNhdChbc2NoZW1hWydqdXB5dGVyLmxhYi5tZW51cyddPy5jb250ZXh0ID8/IFtdXSlcbiAgICAgICAgLnJlZHVjZVJpZ2h0KFxuICAgICAgICAgIChcbiAgICAgICAgICAgIGFjYzogSVNldHRpbmdSZWdpc3RyeS5JQ29udGV4dE1lbnVJdGVtW10sXG4gICAgICAgICAgICB2YWw6IElTZXR0aW5nUmVnaXN0cnkuSUNvbnRleHRNZW51SXRlbVtdXG4gICAgICAgICAgKSA9PiBTZXR0aW5nUmVnaXN0cnkucmVjb25jaWxlSXRlbXMoYWNjLCB2YWwsIHRydWUpLFxuICAgICAgICAgIFtdXG4gICAgICAgICkhO1xuXG4gICAgICAvLyBBcHBseSBkZWZhdWx0IHZhbHVlIGFzIGxhc3Qgc3RlcCB0byB0YWtlIGludG8gYWNjb3VudCBvdmVycmlkZXMuanNvblxuICAgICAgLy8gVGhlIHN0YW5kYXJkIGRlZmF1bHQgYmVpbmcgW10gYXMgdGhlIHBsdWdpbiBtdXN0IHVzZSBganVweXRlci5sYWIubWVudXMuY29udGV4dGBcbiAgICAgIC8vIHRvIGRlZmluZSB0aGVpciBkZWZhdWx0IHZhbHVlLlxuICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLmNvbnRleHRNZW51LmRlZmF1bHQgPSBTZXR0aW5nUmVnaXN0cnkucmVjb25jaWxlSXRlbXMoXG4gICAgICAgIHBsdWdpbkRlZmF1bHRzLFxuICAgICAgICBzY2hlbWEucHJvcGVydGllcyEuY29udGV4dE1lbnUuZGVmYXVsdCBhcyBhbnlbXSxcbiAgICAgICAgdHJ1ZVxuICAgICAgKSFcbiAgICAgICAgLy8gZmxhdHRlbiBvbmUgbGV2ZWxcbiAgICAgICAgLnNvcnQoKGEsIGIpID0+IChhLnJhbmsgPz8gSW5maW5pdHkpIC0gKGIucmFuayA/PyBJbmZpbml0eSkpO1xuICAgIH1cblxuICAgIC8vIFRyYW5zZm9ybSB0aGUgcGx1Z2luIG9iamVjdCB0byByZXR1cm4gZGlmZmVyZW50IHNjaGVtYSB0aGFuIHRoZSBkZWZhdWx0LlxuICAgIHJlZ2lzdHJ5LnRyYW5zZm9ybShwbHVnaW5JZCwge1xuICAgICAgY29tcG9zZTogcGx1Z2luID0+IHtcbiAgICAgICAgLy8gT25seSBvdmVycmlkZSB0aGUgY2Fub25pY2FsIHNjaGVtYSB0aGUgZmlyc3QgdGltZS5cbiAgICAgICAgaWYgKCFjYW5vbmljYWwpIHtcbiAgICAgICAgICBjYW5vbmljYWwgPSBKU09ORXh0LmRlZXBDb3B5KHBsdWdpbi5zY2hlbWEpO1xuICAgICAgICAgIHBvcHVsYXRlKGNhbm9uaWNhbCk7XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBkZWZhdWx0cyA9IGNhbm9uaWNhbC5wcm9wZXJ0aWVzPy5jb250ZXh0TWVudT8uZGVmYXVsdCA/PyBbXTtcbiAgICAgICAgY29uc3QgdXNlciA9IHtcbiAgICAgICAgICAuLi5wbHVnaW4uZGF0YS51c2VyLFxuICAgICAgICAgIGNvbnRleHRNZW51OiBwbHVnaW4uZGF0YS51c2VyLmNvbnRleHRNZW51ID8/IFtdXG4gICAgICAgIH07XG4gICAgICAgIGNvbnN0IGNvbXBvc2l0ZSA9IHtcbiAgICAgICAgICAuLi5wbHVnaW4uZGF0YS5jb21wb3NpdGUsXG4gICAgICAgICAgY29udGV4dE1lbnU6IFNldHRpbmdSZWdpc3RyeS5yZWNvbmNpbGVJdGVtcyhcbiAgICAgICAgICAgIGRlZmF1bHRzIGFzIElTZXR0aW5nUmVnaXN0cnkuSUNvbnRleHRNZW51SXRlbVtdLFxuICAgICAgICAgICAgdXNlci5jb250ZXh0TWVudSBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklDb250ZXh0TWVudUl0ZW1bXSxcbiAgICAgICAgICAgIGZhbHNlXG4gICAgICAgICAgKVxuICAgICAgICB9O1xuXG4gICAgICAgIHBsdWdpbi5kYXRhID0geyBjb21wb3NpdGUsIHVzZXIgfTtcblxuICAgICAgICByZXR1cm4gcGx1Z2luO1xuICAgICAgfSxcbiAgICAgIGZldGNoOiBwbHVnaW4gPT4ge1xuICAgICAgICAvLyBPbmx5IG92ZXJyaWRlIHRoZSBjYW5vbmljYWwgc2NoZW1hIHRoZSBmaXJzdCB0aW1lLlxuICAgICAgICBpZiAoIWNhbm9uaWNhbCkge1xuICAgICAgICAgIGNhbm9uaWNhbCA9IEpTT05FeHQuZGVlcENvcHkocGx1Z2luLnNjaGVtYSk7XG4gICAgICAgICAgcG9wdWxhdGUoY2Fub25pY2FsKTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgZGF0YTogcGx1Z2luLmRhdGEsXG4gICAgICAgICAgaWQ6IHBsdWdpbi5pZCxcbiAgICAgICAgICByYXc6IHBsdWdpbi5yYXcsXG4gICAgICAgICAgc2NoZW1hOiBjYW5vbmljYWwsXG4gICAgICAgICAgdmVyc2lvbjogcGx1Z2luLnZlcnNpb25cbiAgICAgICAgfTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIFJlcG9wdWxhdGUgdGhlIGNhbm9uaWNhbCB2YXJpYWJsZSBhZnRlciB0aGUgc2V0dGluZyByZWdpc3RyeSBoYXNcbiAgICAvLyBwcmVsb2FkZWQgYWxsIGluaXRpYWwgcGx1Z2lucy5cbiAgICBjb25zdCBzZXR0aW5ncyA9IGF3YWl0IHJlZ2lzdHJ5LmxvYWQocGx1Z2luSWQpO1xuXG4gICAgY29uc3QgY29udGV4dEl0ZW1zOiBJU2V0dGluZ1JlZ2lzdHJ5LklDb250ZXh0TWVudUl0ZW1bXSA9XG4gICAgICAoc2V0dGluZ3MuY29tcG9zaXRlLmNvbnRleHRNZW51IGFzIGFueSkgPz8gW107XG5cbiAgICAvLyBDcmVhdGUgbWVudSBpdGVtIGZvciBub24tZGlzYWJsZWQgZWxlbWVudFxuICAgIFNldHRpbmdSZWdpc3RyeS5maWx0ZXJEaXNhYmxlZEl0ZW1zKGNvbnRleHRJdGVtcykuZm9yRWFjaChpdGVtID0+IHtcbiAgICAgIE1lbnVGYWN0b3J5LmFkZENvbnRleHRJdGVtKFxuICAgICAgICB7XG4gICAgICAgICAgLy8gV2UgaGF2ZSB0byBzZXQgdGhlIGRlZmF1bHQgcmFuayBiZWNhdXNlIEx1bWlubyBpcyBzb3J0aW5nIHRoZSB2aXNpYmxlIGl0ZW1zXG4gICAgICAgICAgcmFuazogREVGQVVMVF9DT05URVhUX0lURU1fUkFOSyxcbiAgICAgICAgICAuLi5pdGVtXG4gICAgICAgIH0sXG4gICAgICAgIGNvbnRleHRNZW51LFxuICAgICAgICBtZW51RmFjdG9yeVxuICAgICAgKTtcbiAgICB9KTtcblxuICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAvLyBBcyBleHRlbnNpb24gbWF5IGNoYW5nZSB0aGUgY29udGV4dCBtZW51IHRocm91Z2ggQVBJLFxuICAgICAgLy8gcHJvbXB0IHRoZSB1c2VyIHRvIHJlbG9hZCBpZiB0aGUgbWVudSBoYXMgYmVlbiB1cGRhdGVkLlxuICAgICAgY29uc3QgbmV3SXRlbXMgPSAoc2V0dGluZ3MuY29tcG9zaXRlLmNvbnRleHRNZW51IGFzIGFueSkgPz8gW107XG4gICAgICBpZiAoIUpTT05FeHQuZGVlcEVxdWFsKGNvbnRleHRJdGVtcywgbmV3SXRlbXMpKSB7XG4gICAgICAgIHZvaWQgZGlzcGxheUluZm9ybWF0aW9uKHRyYW5zKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHJlZ2lzdHJ5LnBsdWdpbkNoYW5nZWQuY29ubmVjdChhc3luYyAoc2VuZGVyLCBwbHVnaW4pID0+IHtcbiAgICAgIGlmIChwbHVnaW4gIT09IHBsdWdpbklkKSB7XG4gICAgICAgIC8vIElmIHRoZSBwbHVnaW4gY2hhbmdlZCBpdHMgbWVudS5cbiAgICAgICAgY29uc3Qgb2xkSXRlbXMgPSBsb2FkZWRbcGx1Z2luXSA/PyBbXTtcbiAgICAgICAgY29uc3QgbmV3SXRlbXMgPVxuICAgICAgICAgIHJlZ2lzdHJ5LnBsdWdpbnNbcGx1Z2luXSEuc2NoZW1hWydqdXB5dGVyLmxhYi5tZW51cyddPy5jb250ZXh0ID8/IFtdO1xuICAgICAgICBpZiAoIUpTT05FeHQuZGVlcEVxdWFsKG9sZEl0ZW1zLCBuZXdJdGVtcykpIHtcbiAgICAgICAgICBpZiAobG9hZGVkW3BsdWdpbl0pIHtcbiAgICAgICAgICAgIC8vIFRoZSBwbHVnaW4gaGFzIGNoYW5nZWQsIHJlcXVlc3QgdGhlIHVzZXIgdG8gcmVsb2FkIHRoZSBVSVxuICAgICAgICAgICAgYXdhaXQgZGlzcGxheUluZm9ybWF0aW9uKHRyYW5zKTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgLy8gVGhlIHBsdWdpbiB3YXMgbm90IHlldCBsb2FkZWQgd2hlbiB0aGUgbWVudSB3YXMgYnVpbHQgPT4gdXBkYXRlIHRoZSBtZW51XG4gICAgICAgICAgICBsb2FkZWRbcGx1Z2luXSA9IEpTT05FeHQuZGVlcENvcHkobmV3SXRlbXMpO1xuICAgICAgICAgICAgLy8gTWVyZ2UgcG90ZW50aWFsIGRpc2FibGVkIHN0YXRlXG4gICAgICAgICAgICBjb25zdCB0b0FkZCA9XG4gICAgICAgICAgICAgIFNldHRpbmdSZWdpc3RyeS5yZWNvbmNpbGVJdGVtcyhcbiAgICAgICAgICAgICAgICBuZXdJdGVtcyxcbiAgICAgICAgICAgICAgICBjb250ZXh0SXRlbXMsXG4gICAgICAgICAgICAgICAgZmFsc2UsXG4gICAgICAgICAgICAgICAgZmFsc2VcbiAgICAgICAgICAgICAgKSA/PyBbXTtcbiAgICAgICAgICAgIFNldHRpbmdSZWdpc3RyeS5maWx0ZXJEaXNhYmxlZEl0ZW1zKHRvQWRkKS5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgICAgICAgICBNZW51RmFjdG9yeS5hZGRDb250ZXh0SXRlbShcbiAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAvLyBXZSBoYXZlIHRvIHNldCB0aGUgZGVmYXVsdCByYW5rIGJlY2F1c2UgTHVtaW5vIGlzIHNvcnRpbmcgdGhlIHZpc2libGUgaXRlbXNcbiAgICAgICAgICAgICAgICAgIHJhbms6IERFRkFVTFRfQ09OVEVYVF9JVEVNX1JBTkssXG4gICAgICAgICAgICAgICAgICAuLi5pdGVtXG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICBjb250ZXh0TWVudSxcbiAgICAgICAgICAgICAgICBtZW51RmFjdG9yeVxuICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICBleHBvcnQgZnVuY3Rpb24gYWN0aXZhdGVTaWRlYmFyU3dpdGNoZXIoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCxcbiAgICBzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MsXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICk6IHZvaWQge1xuICAgIC8vIEFkZCBhIGNvbW1hbmQgdG8gc3dpdGNoIGEgc2lkZSBwYW5lbHMncyBzaWRlXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zd2l0Y2hTaWRlYmFyLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1N3aXRjaCBTaWRlYmFyIFNpZGUnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgLy8gRmlyc3QsIHRyeSB0byBmaW5kIHRoZSBjb3JyZWN0IHBhbmVsIGJhc2VkIG9uIHRoZSBhcHBsaWNhdGlvblxuICAgICAgICAvLyBjb250ZXh0IG1lbnUgY2xpY2suIEJhaWwgaWYgd2UgZG9uJ3QgZmluZCBhIHNpZGViYXIgZm9yIHRoZSB3aWRnZXQuXG4gICAgICAgIGNvbnN0IGNvbnRleHROb2RlOiBIVE1MRWxlbWVudCB8IHVuZGVmaW5lZCA9IGFwcC5jb250ZXh0TWVudUhpdFRlc3QoXG4gICAgICAgICAgbm9kZSA9PiAhIW5vZGUuZGF0YXNldC5pZFxuICAgICAgICApO1xuICAgICAgICBpZiAoIWNvbnRleHROb2RlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgaWQgPSBjb250ZXh0Tm9kZS5kYXRhc2V0WydpZCddITtcbiAgICAgICAgY29uc3QgbGVmdFBhbmVsID0gZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ2pwLWxlZnQtc3RhY2snKTtcbiAgICAgICAgY29uc3Qgbm9kZSA9IGRvY3VtZW50LmdldEVsZW1lbnRCeUlkKGlkKTtcblxuICAgICAgICBsZXQgbmV3TGF5b3V0OiB7XG4gICAgICAgICAgJ3NpbmdsZS1kb2N1bWVudCc6IElMYWJTaGVsbC5JVXNlckxheW91dDtcbiAgICAgICAgICAnbXVsdGlwbGUtZG9jdW1lbnQnOiBJTGFiU2hlbGwuSVVzZXJMYXlvdXQ7XG4gICAgICAgIH0gfCBudWxsID0gbnVsbDtcbiAgICAgICAgLy8gTW92ZSB0aGUgcGFuZWwgdG8gdGhlIG90aGVyIHNpZGUuXG4gICAgICAgIGlmIChsZWZ0UGFuZWwgJiYgbm9kZSAmJiBsZWZ0UGFuZWwuY29udGFpbnMobm9kZSkpIHtcbiAgICAgICAgICBjb25zdCB3aWRnZXQgPSBmaW5kKGxhYlNoZWxsLndpZGdldHMoJ2xlZnQnKSwgdyA9PiB3LmlkID09PSBpZCk7XG4gICAgICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICAgICAgbmV3TGF5b3V0ID0gbGFiU2hlbGwubW92ZSh3aWRnZXQsICdyaWdodCcpO1xuICAgICAgICAgICAgbGFiU2hlbGwuYWN0aXZhdGVCeUlkKHdpZGdldC5pZCk7XG4gICAgICAgICAgfVxuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGNvbnN0IHdpZGdldCA9IGZpbmQobGFiU2hlbGwud2lkZ2V0cygncmlnaHQnKSwgdyA9PiB3LmlkID09PSBpZCk7XG4gICAgICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICAgICAgbmV3TGF5b3V0ID0gbGFiU2hlbGwubW92ZSh3aWRnZXQsICdsZWZ0Jyk7XG4gICAgICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICBpZiAobmV3TGF5b3V0KSB7XG4gICAgICAgICAgc2V0dGluZ3NcbiAgICAgICAgICAgIC5zZXQoJ2xheW91dCcsIHtcbiAgICAgICAgICAgICAgc2luZ2xlOiBuZXdMYXlvdXRbJ3NpbmdsZS1kb2N1bWVudCddLFxuICAgICAgICAgICAgICBtdWx0aXBsZTogbmV3TGF5b3V0WydtdWx0aXBsZS1kb2N1bWVudCddXG4gICAgICAgICAgICB9IGFzIGFueSlcbiAgICAgICAgICAgIC5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAgICAgICBjb25zb2xlLmVycm9yKFxuICAgICAgICAgICAgICAgICdGYWlsZWQgdG8gc2F2ZSB1c2VyIGxheW91dCBjdXN0b21pemF0aW9uLicsXG4gICAgICAgICAgICAgICAgcmVhc29uXG4gICAgICAgICAgICAgICk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmNvbW1hbmRFeGVjdXRlZC5jb25uZWN0KChyZWdpc3RyeSwgZXhlY3V0ZWQpID0+IHtcbiAgICAgIGlmIChleGVjdXRlZC5pZCA9PT0gQ29tbWFuZElEcy5yZXNldExheW91dCkge1xuICAgICAgICBzZXR0aW5ncy5yZW1vdmUoJ2xheW91dCcpLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgICAgY29uc29sZS5lcnJvcignRmFpbGVkIHRvIHJlbW92ZSB1c2VyIGxheW91dCBjdXN0b21pemF0aW9uLicsIHJlYXNvbik7XG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuICB9XG59XG4iLCIvKlxuICogQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4gKiBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuICovXG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIGNyZWF0ZVRvb2xiYXJGYWN0b3J5LFxuICBJVG9vbGJhcldpZGdldFJlZ2lzdHJ5LFxuICBzZXRUb29sYmFyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgVG9vbGJhciB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG5jb25zdCBUT1BCQVJfRkFDVE9SWSA9ICdUb3BCYXInO1xuXG4vKipcbiAqIEEgcGx1Z2luIGFkZGluZyBhIHRvb2xiYXIgdG8gdGhlIHRvcCBhcmVhLlxuICovXG5leHBvcnQgY29uc3QgdG9wYmFyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tZXh0ZW5zaW9uOnRvcC1iYXInLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgYSB0b29sYmFyIHRvIHRoZSB0b3AgYXJlYSAobmV4dCB0byB0aGUgbWFpbiBtZW51IGJhcikuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lTZXR0aW5nUmVnaXN0cnksIElUb29sYmFyV2lkZ2V0UmVnaXN0cnldLFxuICBvcHRpb25hbDogW0lUcmFuc2xhdG9yXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgdG9vbGJhclJlZ2lzdHJ5OiBJVG9vbGJhcldpZGdldFJlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0b29sYmFyID0gbmV3IFRvb2xiYXIoKTtcbiAgICB0b29sYmFyLmlkID0gJ2pwLXRvcC1iYXInO1xuXG4gICAgLy8gU2V0IHRvb2xiYXJcbiAgICBzZXRUb29sYmFyKFxuICAgICAgdG9vbGJhcixcbiAgICAgIGNyZWF0ZVRvb2xiYXJGYWN0b3J5KFxuICAgICAgICB0b29sYmFyUmVnaXN0cnksXG4gICAgICAgIHNldHRpbmdSZWdpc3RyeSxcbiAgICAgICAgVE9QQkFSX0ZBQ1RPUlksXG4gICAgICAgIHRvcGJhci5pZCxcbiAgICAgICAgdHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvclxuICAgICAgKSxcbiAgICAgIHRvb2xiYXJcbiAgICApO1xuXG4gICAgYXBwLnNoZWxsLmFkZCh0b29sYmFyLCAndG9wJywgeyByYW5rOiA5MDAgfSk7XG4gIH1cbn07XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=