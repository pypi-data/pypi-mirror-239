"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mainmenu-extension_lib_index_js"],{

/***/ "../packages/mainmenu-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/mainmenu-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_10__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mainmenu-extension
 */











const PLUGIN_ID = '@jupyterlab/mainmenu-extension:plugin';
/**
 * A namespace for command IDs of semantic extension points.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.openEdit = 'editmenu:open';
    CommandIDs.undo = 'editmenu:undo';
    CommandIDs.redo = 'editmenu:redo';
    CommandIDs.clearCurrent = 'editmenu:clear-current';
    CommandIDs.clearAll = 'editmenu:clear-all';
    CommandIDs.find = 'editmenu:find';
    CommandIDs.goToLine = 'editmenu:go-to-line';
    CommandIDs.openFile = 'filemenu:open';
    CommandIDs.closeAndCleanup = 'filemenu:close-and-cleanup';
    CommandIDs.createConsole = 'filemenu:create-console';
    CommandIDs.shutdown = 'filemenu:shutdown';
    CommandIDs.logout = 'filemenu:logout';
    CommandIDs.openKernel = 'kernelmenu:open';
    CommandIDs.interruptKernel = 'kernelmenu:interrupt';
    CommandIDs.reconnectToKernel = 'kernelmenu:reconnect-to-kernel';
    CommandIDs.restartKernel = 'kernelmenu:restart';
    CommandIDs.restartKernelAndClear = 'kernelmenu:restart-and-clear';
    CommandIDs.changeKernel = 'kernelmenu:change';
    CommandIDs.shutdownKernel = 'kernelmenu:shutdown';
    CommandIDs.shutdownAllKernels = 'kernelmenu:shutdownAll';
    CommandIDs.openView = 'viewmenu:open';
    CommandIDs.wordWrap = 'viewmenu:word-wrap';
    CommandIDs.lineNumbering = 'viewmenu:line-numbering';
    CommandIDs.matchBrackets = 'viewmenu:match-brackets';
    CommandIDs.openRun = 'runmenu:open';
    CommandIDs.run = 'runmenu:run';
    CommandIDs.runAll = 'runmenu:run-all';
    CommandIDs.restartAndRunAll = 'runmenu:restart-and-run-all';
    CommandIDs.runAbove = 'runmenu:run-above';
    CommandIDs.runBelow = 'runmenu:run-below';
    CommandIDs.openTabs = 'tabsmenu:open';
    CommandIDs.activateById = 'tabsmenu:activate-by-id';
    CommandIDs.activatePreviouslyUsedTab = 'tabsmenu:activate-previously-used-tab';
    CommandIDs.openSettings = 'settingsmenu:open';
    CommandIDs.openHelp = 'helpmenu:open';
    CommandIDs.getKernel = 'helpmenu:get-kernel';
    CommandIDs.openFirst = 'mainmenu:open-first';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing an interface to the main menu.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'Adds and provides the application main menu.',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry],
    provides: _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
    activate: async (app, router, translator, palette, labShell, registry) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const menu = new _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.MainMenu(commands);
        menu.id = 'jp-MainMenu';
        menu.addClass('jp-scrollbar-tiny');
        // Built menu from settings
        if (registry) {
            await Private.loadSettingsMenu(registry, (aMenu) => {
                menu.addMenu(aMenu, false, { rank: aMenu.rank });
            }, options => _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.MainMenu.generateMenu(commands, options, trans), translator);
            // Trigger single update
            menu.update();
        }
        // Only add quit button if the back-end supports it by checking page config.
        const quitButton = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('quitButton').toLowerCase();
        menu.fileMenu.quitEntry = quitButton === 'true';
        // Create the application menus.
        createEditMenu(app, menu.editMenu, trans);
        createFileMenu(app, menu.fileMenu, router, trans);
        createKernelMenu(app, menu.kernelMenu, trans);
        createRunMenu(app, menu.runMenu, trans);
        createViewMenu(app, menu.viewMenu, trans);
        createHelpMenu(app, menu.helpMenu, trans);
        // The tabs menu relies on lab shell functionality.
        if (labShell) {
            createTabsMenu(app, menu.tabsMenu, labShell, trans);
        }
        // Create commands to open the main application menus.
        const activateMenu = (item) => {
            menu.activeMenu = item;
            menu.openActiveMenu();
        };
        commands.addCommand(CommandIDs.openEdit, {
            label: trans.__('Open Edit Menu'),
            execute: () => activateMenu(menu.editMenu)
        });
        commands.addCommand(CommandIDs.openFile, {
            label: trans.__('Open File Menu'),
            execute: () => activateMenu(menu.fileMenu)
        });
        commands.addCommand(CommandIDs.openKernel, {
            label: trans.__('Open Kernel Menu'),
            execute: () => activateMenu(menu.kernelMenu)
        });
        commands.addCommand(CommandIDs.openRun, {
            label: trans.__('Open Run Menu'),
            execute: () => activateMenu(menu.runMenu)
        });
        commands.addCommand(CommandIDs.openView, {
            label: trans.__('Open View Menu'),
            execute: () => activateMenu(menu.viewMenu)
        });
        commands.addCommand(CommandIDs.openSettings, {
            label: trans.__('Open Settings Menu'),
            execute: () => activateMenu(menu.settingsMenu)
        });
        commands.addCommand(CommandIDs.openTabs, {
            label: trans.__('Open Tabs Menu'),
            execute: () => activateMenu(menu.tabsMenu)
        });
        commands.addCommand(CommandIDs.openHelp, {
            label: trans.__('Open Help Menu'),
            execute: () => activateMenu(menu.helpMenu)
        });
        commands.addCommand(CommandIDs.openFirst, {
            label: trans.__('Open First Menu'),
            execute: () => {
                menu.activeIndex = 0;
                menu.openActiveMenu();
            }
        });
        if (palette) {
            // Add some of the commands defined here to the command palette.
            palette.addItem({
                command: CommandIDs.shutdown,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: CommandIDs.logout,
                category: trans.__('Main Area')
            });
            palette.addItem({
                command: CommandIDs.shutdownAllKernels,
                category: trans.__('Kernel Operations')
            });
            palette.addItem({
                command: CommandIDs.activatePreviouslyUsedTab,
                category: trans.__('Main Area')
            });
        }
        app.shell.add(menu, 'menu', { rank: 100 });
        return menu;
    }
};
/**
 * Create the basic `Edit` menu.
 */
function createEditMenu(app, menu, trans) {
    const commands = app.commands;
    // Add the undo/redo commands the the Edit menu.
    commands.addCommand(CommandIDs.undo, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.undoers.undo, {
        label: trans.__('Undo')
    }, trans));
    commands.addCommand(CommandIDs.redo, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.undoers.redo, {
        label: trans.__('Redo')
    }, trans));
    // Add the clear commands to the Edit menu.
    commands.addCommand(CommandIDs.clearCurrent, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.clearers.clearCurrent, {
        label: trans.__('Clear')
    }, trans));
    commands.addCommand(CommandIDs.clearAll, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.clearers.clearAll, {
        label: trans.__('Clear All')
    }, trans));
    commands.addCommand(CommandIDs.goToLine, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.goToLiners, {
        label: trans.__('Go to Line…')
    }, trans));
}
/**
 * Create the basic `File` menu.
 */
function createFileMenu(app, menu, router, trans) {
    const commands = app.commands;
    // Add a delegator command for closing and cleaning up an activity.
    // This one is a bit different, in that we consider it enabled
    // even if it cannot find a delegate for the activity.
    // In that case, we instead call the application `close` command.
    commands.addCommand(CommandIDs.closeAndCleanup, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.closeAndCleaners, {
            execute: 'application:close',
            label: trans.__('Close and Shut Down'),
            isEnabled: true
        }, trans),
        isEnabled: () => !!app.shell.currentWidget && !!app.shell.currentWidget.title.closable
    });
    // Add a delegator command for creating a console for an activity.
    commands.addCommand(CommandIDs.createConsole, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.consoleCreators, {
        label: trans.__('New Console for Activity')
    }, trans));
    commands.addCommand(CommandIDs.shutdown, {
        label: trans.__('Shut Down'),
        caption: trans.__('Shut down JupyterLab'),
        isVisible: () => menu.quitEntry,
        isEnabled: () => menu.quitEntry,
        execute: () => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shutdown confirmation'),
                body: trans.__('Please confirm you want to shut down JupyterLab.'),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Shut Down') })
                ]
            }).then(async (result) => {
                if (result.button.accept) {
                    const setting = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.makeSettings();
                    const apiURL = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(setting.baseUrl, 'api/shutdown');
                    // Shutdown all kernel and terminal sessions before shutting down the server
                    // If this fails, we continue execution so we can post an api/shutdown request
                    try {
                        await Promise.all([
                            app.serviceManager.sessions.shutdownAll(),
                            app.serviceManager.terminals.shutdownAll()
                        ]);
                    }
                    catch (e) {
                        // Do nothing
                        console.log(`Failed to shutdown sessions and terminals: ${e}`);
                    }
                    return _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.makeRequest(apiURL, { method: 'POST' }, setting)
                        .then(result => {
                        if (result.ok) {
                            // Close this window if the shutdown request has been successful
                            const body = document.createElement('div');
                            const p1 = document.createElement('p');
                            p1.textContent = trans.__('You have shut down the Jupyter server. You can now close this tab.');
                            const p2 = document.createElement('p');
                            p2.textContent = trans.__('To use JupyterLab again, you will need to relaunch it.');
                            body.appendChild(p1);
                            body.appendChild(p2);
                            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                                title: trans.__('Server stopped'),
                                body: new _lumino_widgets__WEBPACK_IMPORTED_MODULE_10__.Widget({ node: body }),
                                buttons: []
                            });
                            window.close();
                        }
                        else {
                            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.ResponseError(result);
                        }
                    })
                        .catch(data => {
                        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_4__.ServerConnection.NetworkError(data);
                    });
                }
            });
        }
    });
    commands.addCommand(CommandIDs.logout, {
        label: trans.__('Log Out'),
        caption: trans.__('Log out of JupyterLab'),
        isVisible: () => menu.quitEntry,
        isEnabled: () => menu.quitEntry,
        execute: () => {
            router.navigate('/logout', { hard: true });
        }
    });
}
/**
 * Create the basic `Kernel` menu.
 */
function createKernelMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.interruptKernel, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.interruptKernel, {
            label: trans.__('Interrupt Kernel'),
            caption: trans.__('Interrupt the kernel')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.stopIcon : undefined)
    });
    commands.addCommand(CommandIDs.reconnectToKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.reconnectToKernel, {
        label: trans.__('Reconnect to Kernel')
    }, trans));
    commands.addCommand(CommandIDs.restartKernel, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.restartKernel, {
            label: trans.__('Restart Kernel…'),
            caption: trans.__('Restart the kernel')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.refreshIcon : undefined)
    });
    commands.addCommand(CommandIDs.restartKernelAndClear, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, [menu.kernelUsers.restartKernel, menu.kernelUsers.clearWidget], {
        label: trans.__('Restart Kernel and Clear…')
    }, trans));
    commands.addCommand(CommandIDs.changeKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.changeKernel, {
        label: trans.__('Change Kernel…')
    }, trans));
    commands.addCommand(CommandIDs.shutdownKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.kernelUsers.shutdownKernel, {
        label: trans.__('Shut Down Kernel'),
        caption: trans.__('Shut down kernel')
    }, trans));
    commands.addCommand(CommandIDs.shutdownAllKernels, {
        label: trans.__('Shut Down All Kernels…'),
        isEnabled: () => {
            return !app.serviceManager.sessions.running().next().done;
        },
        execute: () => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Shut Down All?'),
                body: trans.__('Shut down all kernels?'),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Dismiss') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Shut Down All') })
                ]
            }).then(result => {
                if (result.button.accept) {
                    return app.serviceManager.sessions.shutdownAll();
                }
            });
        }
    });
}
/**
 * Create the basic `View` menu.
 */
function createViewMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.lineNumbering, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.editorViewers.toggleLineNumbers, {
        label: trans.__('Show Line Numbers')
    }, trans));
    commands.addCommand(CommandIDs.matchBrackets, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.editorViewers.toggleMatchBrackets, {
        label: trans.__('Match Brackets')
    }, trans));
    commands.addCommand(CommandIDs.wordWrap, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.editorViewers.toggleWordWrap, {
        label: trans.__('Wrap Words')
    }, trans));
}
/**
 * Create the basic `Run` menu.
 */
function createRunMenu(app, menu, trans) {
    const commands = app.commands;
    commands.addCommand(CommandIDs.run, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.codeRunners.run, {
            label: trans.__('Run Selected'),
            caption: trans.__('Run Selected')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.runIcon : undefined)
    });
    commands.addCommand(CommandIDs.runAll, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.codeRunners.runAll, {
        label: trans.__('Run All'),
        caption: trans.__('Run All')
    }, trans));
    commands.addCommand(CommandIDs.restartAndRunAll, {
        ...(0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, [menu.codeRunners.restart, menu.codeRunners.runAll], {
            label: trans.__('Restart Kernel and Run All'),
            caption: trans.__('Restart Kernel and Run All')
        }, trans),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.fastForwardIcon : undefined)
    });
}
/**
 * Create the basic `Tabs` menu.
 */
function createTabsMenu(app, menu, labShell, trans) {
    const commands = app.commands;
    // A list of the active tabs in the main area.
    const tabGroup = [];
    // A disposable for getting rid of the out-of-date tabs list.
    let disposable;
    // Command to activate a widget by id.
    commands.addCommand(CommandIDs.activateById, {
        label: args => {
            if (args.id === undefined) {
                return trans.__('Activate a widget by its `id`.');
            }
            const id = args['id'] || '';
            const widget = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.find)(app.shell.widgets('main'), w => w.id === id);
            return (widget && widget.title.label) || '';
        },
        isToggled: args => {
            const id = args['id'] || '';
            return !!app.shell.currentWidget && app.shell.currentWidget.id === id;
        },
        execute: args => app.shell.activateById(args['id'] || '')
    });
    let previousId = '';
    // Command to toggle between the current
    // tab and the last modified tab.
    commands.addCommand(CommandIDs.activatePreviouslyUsedTab, {
        label: trans.__('Activate Previously Used Tab'),
        isEnabled: () => !!previousId,
        execute: () => commands.execute(CommandIDs.activateById, { id: previousId })
    });
    if (labShell) {
        void app.restored.then(() => {
            // Iterate over the current widgets in the
            // main area, and add them to the tab group
            // of the menu.
            const populateTabs = () => {
                // remove the previous tab list
                if (disposable && !disposable.isDisposed) {
                    disposable.dispose();
                }
                tabGroup.length = 0;
                let isPreviouslyUsedTabAttached = false;
                for (const widget of app.shell.widgets('main')) {
                    if (widget.id === previousId) {
                        isPreviouslyUsedTabAttached = true;
                    }
                    tabGroup.push({
                        command: CommandIDs.activateById,
                        args: { id: widget.id }
                    });
                }
                disposable = menu.addGroup(tabGroup, 1);
                previousId = isPreviouslyUsedTabAttached ? previousId : '';
            };
            populateTabs();
            labShell.layoutModified.connect(() => {
                populateTabs();
            });
            // Update the ID of the previous active tab if a new tab is selected.
            labShell.currentChanged.connect((_, args) => {
                const widget = args.oldValue;
                if (!widget) {
                    return;
                }
                previousId = widget.id;
            });
        });
    }
}
/**
 * Create the basic `Help` menu.
 */
function createHelpMenu(app, menu, trans) {
    app.commands.addCommand(CommandIDs.getKernel, (0,_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.createSemanticCommand)(app, menu.getKernel, {
        label: trans.__('Get Kernel'),
        isVisible: false
    }, trans));
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for Private data.
 */
var Private;
(function (Private) {
    async function displayInformation(trans) {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Information'),
            body: trans.__('Menu customization has changed. You will need to reload JupyterLab to see the changes.'),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Reload') })
            ]
        });
        if (result.button.accept) {
            location.reload();
        }
    }
    async function loadSettingsMenu(registry, addMenu, menuFactory, translator) {
        var _a;
        const trans = translator.load('jupyterlab');
        let canonical = null;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         */
        function populate(schema) {
            var _a, _b;
            loaded = {};
            const pluginDefaults = Object.keys(registry.plugins)
                .map(plugin => {
                var _a, _b;
                const menus = (_b = (_a = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.main) !== null && _b !== void 0 ? _b : [];
                loaded[plugin] = menus;
                return menus;
            })
                .concat([(_b = (_a = schema['jupyter.lab.menus']) === null || _a === void 0 ? void 0 : _a.main) !== null && _b !== void 0 ? _b : []])
                .reduceRight((acc, val) => _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(acc, val, true), schema.properties.menus.default);
            // Apply default value as last step to take into account overrides.json
            // The standard default being [] as the plugin must use `jupyter.lab.menus.main`
            // to define their default value.
            schema.properties.menus.default = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(pluginDefaults, schema.properties.menus.default, true)
                // flatten one level
                .sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(PLUGIN_ID, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.menus) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    ...plugin.data.user,
                    menus: (_d = plugin.data.user.menus) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    ...plugin.data.composite,
                    menus: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(defaults, user.menus)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
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
        const settings = await registry.load(PLUGIN_ID);
        const currentMenus = (_a = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(settings.composite.menus)) !== null && _a !== void 0 ? _a : [];
        const menus = new Array();
        // Create menu for non-disabled element
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.createMenus(currentMenus
            .filter(menu => !menu.disabled)
            .map(menu => {
            var _a;
            return {
                ...menu,
                items: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.filterDisabledItems((_a = menu.items) !== null && _a !== void 0 ? _a : [])
            };
        }), menuFactory).forEach(menu => {
            menus.push(menu);
            addMenu(menu);
        });
        settings.changed.connect(() => {
            var _a;
            // As extension may change menu through API, prompt the user to reload if the
            // menu has been updated.
            const newMenus = (_a = settings.composite.menus) !== null && _a !== void 0 ? _a : [];
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepEqual(currentMenus, newMenus)) {
                void displayInformation(trans);
            }
        });
        registry.pluginChanged.connect(async (sender, plugin) => {
            var _a, _b, _c;
            if (plugin !== PLUGIN_ID) {
                // If the plugin changed its menu.
                const oldMenus = (_a = loaded[plugin]) !== null && _a !== void 0 ? _a : [];
                const newMenus = (_c = (_b = registry.plugins[plugin].schema['jupyter.lab.menus']) === null || _b === void 0 ? void 0 : _b.main) !== null && _c !== void 0 ? _c : [];
                if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepEqual(oldMenus, newMenus)) {
                    if (loaded[plugin]) {
                        // The plugin has changed, request the user to reload the UI - this should not happen
                        await displayInformation(trans);
                    }
                    else {
                        // The plugin was not yet loaded when the menu was built => update the menu
                        loaded[plugin] = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(newMenus);
                        // Merge potential disabled state
                        const toAdd = _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.reconcileMenus(newMenus, currentMenus, false, false)
                            .filter(menu => !menu.disabled)
                            .map(menu => {
                            var _a;
                            return {
                                ...menu,
                                items: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.SettingRegistry.filterDisabledItems((_a = menu.items) !== null && _a !== void 0 ? _a : [])
                            };
                        });
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MenuFactory.updateMenus(menus, toAdd, menuFactory).forEach(menu => {
                            addMenu(menu);
                        });
                    }
                }
            }
        });
    }
    Private.loadSettingsMenu = loadSettingsMenu;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWFpbm1lbnUtZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy4xOWM1ZTdhY2I5ODU2NDI0NmI5MS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQVE4QjtBQU1IO0FBQzZCO0FBVzdCO0FBQzBCO0FBQ3dCO0FBQ1A7QUFPdEM7QUFDTTtBQUNHO0FBRUc7QUFFL0MsTUFBTSxTQUFTLEdBQUcsdUNBQXVDLENBQUM7QUFFMUQ7O0dBRUc7QUFDSSxJQUFVLFVBQVUsQ0EyRTFCO0FBM0VELFdBQWlCLFVBQVU7SUFDWixtQkFBUSxHQUFHLGVBQWUsQ0FBQztJQUUzQixlQUFJLEdBQUcsZUFBZSxDQUFDO0lBRXZCLGVBQUksR0FBRyxlQUFlLENBQUM7SUFFdkIsdUJBQVksR0FBRyx3QkFBd0IsQ0FBQztJQUV4QyxtQkFBUSxHQUFHLG9CQUFvQixDQUFDO0lBRWhDLGVBQUksR0FBRyxlQUFlLENBQUM7SUFFdkIsbUJBQVEsR0FBRyxxQkFBcUIsQ0FBQztJQUVqQyxtQkFBUSxHQUFHLGVBQWUsQ0FBQztJQUUzQiwwQkFBZSxHQUFHLDRCQUE0QixDQUFDO0lBRS9DLHdCQUFhLEdBQUcseUJBQXlCLENBQUM7SUFFMUMsbUJBQVEsR0FBRyxtQkFBbUIsQ0FBQztJQUUvQixpQkFBTSxHQUFHLGlCQUFpQixDQUFDO0lBRTNCLHFCQUFVLEdBQUcsaUJBQWlCLENBQUM7SUFFL0IsMEJBQWUsR0FBRyxzQkFBc0IsQ0FBQztJQUV6Qyw0QkFBaUIsR0FBRyxnQ0FBZ0MsQ0FBQztJQUVyRCx3QkFBYSxHQUFHLG9CQUFvQixDQUFDO0lBRXJDLGdDQUFxQixHQUFHLDhCQUE4QixDQUFDO0lBRXZELHVCQUFZLEdBQUcsbUJBQW1CLENBQUM7SUFFbkMseUJBQWMsR0FBRyxxQkFBcUIsQ0FBQztJQUV2Qyw2QkFBa0IsR0FBRyx3QkFBd0IsQ0FBQztJQUU5QyxtQkFBUSxHQUFHLGVBQWUsQ0FBQztJQUUzQixtQkFBUSxHQUFHLG9CQUFvQixDQUFDO0lBRWhDLHdCQUFhLEdBQUcseUJBQXlCLENBQUM7SUFFMUMsd0JBQWEsR0FBRyx5QkFBeUIsQ0FBQztJQUUxQyxrQkFBTyxHQUFHLGNBQWMsQ0FBQztJQUV6QixjQUFHLEdBQUcsYUFBYSxDQUFDO0lBRXBCLGlCQUFNLEdBQUcsaUJBQWlCLENBQUM7SUFFM0IsMkJBQWdCLEdBQUcsNkJBQTZCLENBQUM7SUFFakQsbUJBQVEsR0FBRyxtQkFBbUIsQ0FBQztJQUUvQixtQkFBUSxHQUFHLG1CQUFtQixDQUFDO0lBRS9CLG1CQUFRLEdBQUcsZUFBZSxDQUFDO0lBRTNCLHVCQUFZLEdBQUcseUJBQXlCLENBQUM7SUFFekMsb0NBQXlCLEdBQ3BDLHVDQUF1QyxDQUFDO0lBRTdCLHVCQUFZLEdBQUcsbUJBQW1CLENBQUM7SUFFbkMsbUJBQVEsR0FBRyxlQUFlLENBQUM7SUFFM0Isb0JBQVMsR0FBRyxxQkFBcUIsQ0FBQztJQUVsQyxvQkFBUyxHQUFHLHFCQUFxQixDQUFDO0FBQ2pELENBQUMsRUEzRWdCLFVBQVUsS0FBVixVQUFVLFFBMkUxQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxNQUFNLEdBQXFDO0lBQy9DLEVBQUUsRUFBRSxTQUFTO0lBQ2IsV0FBVyxFQUFFLDhDQUE4QztJQUMzRCxRQUFRLEVBQUUsQ0FBQyw0REFBTyxFQUFFLGdFQUFXLENBQUM7SUFDaEMsUUFBUSxFQUFFLENBQUMsaUVBQWUsRUFBRSw4REFBUyxFQUFFLHlFQUFnQixDQUFDO0lBQ3hELFFBQVEsRUFBRSwyREFBUztJQUNuQixRQUFRLEVBQUUsS0FBSyxFQUNiLEdBQW9CLEVBQ3BCLE1BQWUsRUFDZixVQUF1QixFQUN2QixPQUErQixFQUMvQixRQUEwQixFQUMxQixRQUFpQyxFQUNiLEVBQUU7UUFDdEIsTUFBTSxFQUFFLFFBQVEsRUFBRSxHQUFHLEdBQUcsQ0FBQztRQUN6QixNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBRTVDLE1BQU0sSUFBSSxHQUFHLElBQUksMERBQVEsQ0FBQyxRQUFRLENBQUMsQ0FBQztRQUNwQyxJQUFJLENBQUMsRUFBRSxHQUFHLGFBQWEsQ0FBQztRQUN4QixJQUFJLENBQUMsUUFBUSxDQUFDLG1CQUFtQixDQUFDLENBQUM7UUFFbkMsMkJBQTJCO1FBQzNCLElBQUksUUFBUSxFQUFFO1lBQ1osTUFBTSxPQUFPLENBQUMsZ0JBQWdCLENBQzVCLFFBQVEsRUFDUixDQUFDLEtBQWlCLEVBQUUsRUFBRTtnQkFDcEIsSUFBSSxDQUFDLE9BQU8sQ0FBQyxLQUFLLEVBQUUsS0FBSyxFQUFFLEVBQUUsSUFBSSxFQUFFLEtBQUssQ0FBQyxJQUFJLEVBQUUsQ0FBQyxDQUFDO1lBQ25ELENBQUMsRUFDRCxPQUFPLENBQUMsRUFBRSxDQUFDLHVFQUFxQixDQUFDLFFBQVEsRUFBRSxPQUFPLEVBQUUsS0FBSyxDQUFDLEVBQzFELFVBQVUsQ0FDWCxDQUFDO1lBRUYsd0JBQXdCO1lBQ3hCLElBQUksQ0FBQyxNQUFNLEVBQUUsQ0FBQztTQUNmO1FBRUQsNEVBQTRFO1FBQzVFLE1BQU0sVUFBVSxHQUFHLHVFQUFvQixDQUFDLFlBQVksQ0FBQyxDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ3BFLElBQUksQ0FBQyxRQUFRLENBQUMsU0FBUyxHQUFHLFVBQVUsS0FBSyxNQUFNLENBQUM7UUFFaEQsZ0NBQWdDO1FBQ2hDLGNBQWMsQ0FBQyxHQUFHLEVBQUUsSUFBSSxDQUFDLFFBQVEsRUFBRSxLQUFLLENBQUMsQ0FBQztRQUMxQyxjQUFjLENBQUMsR0FBRyxFQUFFLElBQUksQ0FBQyxRQUFRLEVBQUUsTUFBTSxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBQ2xELGdCQUFnQixDQUFDLEdBQUcsRUFBRSxJQUFJLENBQUMsVUFBVSxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBQzlDLGFBQWEsQ0FBQyxHQUFHLEVBQUUsSUFBSSxDQUFDLE9BQU8sRUFBRSxLQUFLLENBQUMsQ0FBQztRQUN4QyxjQUFjLENBQUMsR0FBRyxFQUFFLElBQUksQ0FBQyxRQUFRLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFDMUMsY0FBYyxDQUFDLEdBQUcsRUFBRSxJQUFJLENBQUMsUUFBUSxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBRTFDLG1EQUFtRDtRQUNuRCxJQUFJLFFBQVEsRUFBRTtZQUNaLGNBQWMsQ0FBQyxHQUFHLEVBQUUsSUFBSSxDQUFDLFFBQVEsRUFBRSxRQUFRLEVBQUUsS0FBSyxDQUFDLENBQUM7U0FDckQ7UUFFRCxzREFBc0Q7UUFDdEQsTUFBTSxZQUFZLEdBQUcsQ0FBQyxJQUFVLEVBQUUsRUFBRTtZQUNsQyxJQUFJLENBQUMsVUFBVSxHQUFHLElBQUksQ0FBQztZQUN2QixJQUFJLENBQUMsY0FBYyxFQUFFLENBQUM7UUFDeEIsQ0FBQyxDQUFDO1FBRUYsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsUUFBUSxFQUFFO1lBQ3ZDLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGdCQUFnQixDQUFDO1lBQ2pDLE9BQU8sRUFBRSxHQUFHLEVBQUUsQ0FBQyxZQUFZLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQztTQUMzQyxDQUFDLENBQUM7UUFDSCxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxRQUFRLEVBQUU7WUFDdkMsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsZ0JBQWdCLENBQUM7WUFDakMsT0FBTyxFQUFFLEdBQUcsRUFBRSxDQUFDLFlBQVksQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDO1NBQzNDLENBQUMsQ0FBQztRQUNILFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLFVBQVUsRUFBRTtZQUN6QyxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxrQkFBa0IsQ0FBQztZQUNuQyxPQUFPLEVBQUUsR0FBRyxFQUFFLENBQUMsWUFBWSxDQUFDLElBQUksQ0FBQyxVQUFVLENBQUM7U0FDN0MsQ0FBQyxDQUFDO1FBQ0gsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsT0FBTyxFQUFFO1lBQ3RDLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGVBQWUsQ0FBQztZQUNoQyxPQUFPLEVBQUUsR0FBRyxFQUFFLENBQUMsWUFBWSxDQUFDLElBQUksQ0FBQyxPQUFPLENBQUM7U0FDMUMsQ0FBQyxDQUFDO1FBQ0gsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsUUFBUSxFQUFFO1lBQ3ZDLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGdCQUFnQixDQUFDO1lBQ2pDLE9BQU8sRUFBRSxHQUFHLEVBQUUsQ0FBQyxZQUFZLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQztTQUMzQyxDQUFDLENBQUM7UUFDSCxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxZQUFZLEVBQUU7WUFDM0MsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsb0JBQW9CLENBQUM7WUFDckMsT0FBTyxFQUFFLEdBQUcsRUFBRSxDQUFDLFlBQVksQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDO1NBQy9DLENBQUMsQ0FBQztRQUNILFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLFFBQVEsRUFBRTtZQUN2QyxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxnQkFBZ0IsQ0FBQztZQUNqQyxPQUFPLEVBQUUsR0FBRyxFQUFFLENBQUMsWUFBWSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUM7U0FDM0MsQ0FBQyxDQUFDO1FBQ0gsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsUUFBUSxFQUFFO1lBQ3ZDLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGdCQUFnQixDQUFDO1lBQ2pDLE9BQU8sRUFBRSxHQUFHLEVBQUUsQ0FBQyxZQUFZLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQztTQUMzQyxDQUFDLENBQUM7UUFDSCxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxTQUFTLEVBQUU7WUFDeEMsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsaUJBQWlCLENBQUM7WUFDbEMsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixJQUFJLENBQUMsV0FBVyxHQUFHLENBQUMsQ0FBQztnQkFDckIsSUFBSSxDQUFDLGNBQWMsRUFBRSxDQUFDO1lBQ3hCLENBQUM7U0FDRixDQUFDLENBQUM7UUFFSCxJQUFJLE9BQU8sRUFBRTtZQUNYLGdFQUFnRTtZQUNoRSxPQUFPLENBQUMsT0FBTyxDQUFDO2dCQUNkLE9BQU8sRUFBRSxVQUFVLENBQUMsUUFBUTtnQkFDNUIsUUFBUSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsV0FBVyxDQUFDO2FBQ2hDLENBQUMsQ0FBQztZQUNILE9BQU8sQ0FBQyxPQUFPLENBQUM7Z0JBQ2QsT0FBTyxFQUFFLFVBQVUsQ0FBQyxNQUFNO2dCQUMxQixRQUFRLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxXQUFXLENBQUM7YUFDaEMsQ0FBQyxDQUFDO1lBRUgsT0FBTyxDQUFDLE9BQU8sQ0FBQztnQkFDZCxPQUFPLEVBQUUsVUFBVSxDQUFDLGtCQUFrQjtnQkFDdEMsUUFBUSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsbUJBQW1CLENBQUM7YUFDeEMsQ0FBQyxDQUFDO1lBRUgsT0FBTyxDQUFDLE9BQU8sQ0FBQztnQkFDZCxPQUFPLEVBQUUsVUFBVSxDQUFDLHlCQUF5QjtnQkFDN0MsUUFBUSxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsV0FBVyxDQUFDO2FBQ2hDLENBQUMsQ0FBQztTQUNKO1FBRUQsR0FBRyxDQUFDLEtBQUssQ0FBQyxHQUFHLENBQUMsSUFBSSxFQUFFLE1BQU0sRUFBRSxFQUFFLElBQUksRUFBRSxHQUFHLEVBQUUsQ0FBQyxDQUFDO1FBRTNDLE9BQU8sSUFBSSxDQUFDO0lBQ2QsQ0FBQztDQUNGLENBQUM7QUFFRjs7R0FFRztBQUNILFNBQVMsY0FBYyxDQUNyQixHQUFvQixFQUNwQixJQUFlLEVBQ2YsS0FBd0I7SUFFeEIsTUFBTSxRQUFRLEdBQUcsR0FBRyxDQUFDLFFBQVEsQ0FBQztJQUU5QixnREFBZ0Q7SUFDaEQsUUFBUSxDQUFDLFVBQVUsQ0FDakIsVUFBVSxDQUFDLElBQUksRUFDZiw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILElBQUksQ0FBQyxPQUFPLENBQUMsSUFBSSxFQUNqQjtRQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLE1BQU0sQ0FBQztLQUN4QixFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7SUFDRixRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsSUFBSSxFQUNmLDhFQUFxQixDQUNuQixHQUFHLEVBQ0gsSUFBSSxDQUFDLE9BQU8sQ0FBQyxJQUFJLEVBQ2pCO1FBQ0UsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsTUFBTSxDQUFDO0tBQ3hCLEVBQ0QsS0FBSyxDQUNOLENBQ0YsQ0FBQztJQUVGLDJDQUEyQztJQUMzQyxRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsWUFBWSxFQUN2Qiw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILElBQUksQ0FBQyxRQUFRLENBQUMsWUFBWSxFQUMxQjtRQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLE9BQU8sQ0FBQztLQUN6QixFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7SUFDRixRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsUUFBUSxFQUNuQiw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILElBQUksQ0FBQyxRQUFRLENBQUMsUUFBUSxFQUN0QjtRQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFdBQVcsQ0FBQztLQUM3QixFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7SUFFRixRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsUUFBUSxFQUNuQiw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILElBQUksQ0FBQyxVQUFVLEVBQ2Y7UUFDRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxhQUFhLENBQUM7S0FDL0IsRUFDRCxLQUFLLENBQ04sQ0FDRixDQUFDO0FBQ0osQ0FBQztBQUVEOztHQUVHO0FBQ0gsU0FBUyxjQUFjLENBQ3JCLEdBQW9CLEVBQ3BCLElBQWUsRUFDZixNQUFlLEVBQ2YsS0FBd0I7SUFFeEIsTUFBTSxRQUFRLEdBQUcsR0FBRyxDQUFDLFFBQVEsQ0FBQztJQUU5QixtRUFBbUU7SUFDbkUsOERBQThEO0lBQzlELHNEQUFzRDtJQUN0RCxpRUFBaUU7SUFDakUsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsZUFBZSxFQUFFO1FBQzlDLEdBQUcsOEVBQXFCLENBQ3RCLEdBQUcsRUFDSCxJQUFJLENBQUMsZ0JBQWdCLEVBQ3JCO1lBQ0UsT0FBTyxFQUFFLG1CQUFtQjtZQUM1QixLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxxQkFBcUIsQ0FBQztZQUN0QyxTQUFTLEVBQUUsSUFBSTtTQUNoQixFQUNELEtBQUssQ0FDTjtRQUNELFNBQVMsRUFBRSxHQUFHLEVBQUUsQ0FDZCxDQUFDLENBQUMsR0FBRyxDQUFDLEtBQUssQ0FBQyxhQUFhLElBQUksQ0FBQyxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsYUFBYSxDQUFDLEtBQUssQ0FBQyxRQUFRO0tBQ3hFLENBQUMsQ0FBQztJQUVILGtFQUFrRTtJQUNsRSxRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsYUFBYSxFQUN4Qiw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILElBQUksQ0FBQyxlQUFlLEVBQ3BCO1FBQ0UsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsMEJBQTBCLENBQUM7S0FDNUMsRUFDRCxLQUFLLENBQ04sQ0FDRixDQUFDO0lBRUYsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsUUFBUSxFQUFFO1FBQ3ZDLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFdBQVcsQ0FBQztRQUM1QixPQUFPLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxzQkFBc0IsQ0FBQztRQUN6QyxTQUFTLEVBQUUsR0FBRyxFQUFFLENBQUMsSUFBSSxDQUFDLFNBQVM7UUFDL0IsU0FBUyxFQUFFLEdBQUcsRUFBRSxDQUFDLElBQUksQ0FBQyxTQUFTO1FBQy9CLE9BQU8sRUFBRSxHQUFHLEVBQUU7WUFDWixPQUFPLGdFQUFVLENBQUM7Z0JBQ2hCLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLHVCQUF1QixDQUFDO2dCQUN4QyxJQUFJLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxrREFBa0QsQ0FBQztnQkFDbEUsT0FBTyxFQUFFO29CQUNQLHFFQUFtQixFQUFFO29CQUNyQixtRUFBaUIsQ0FBQyxFQUFFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFdBQVcsQ0FBQyxFQUFFLENBQUM7aUJBQ3BEO2FBQ0YsQ0FBQyxDQUFDLElBQUksQ0FBQyxLQUFLLEVBQUMsTUFBTSxFQUFDLEVBQUU7Z0JBQ3JCLElBQUksTUFBTSxDQUFDLE1BQU0sQ0FBQyxNQUFNLEVBQUU7b0JBQ3hCLE1BQU0sT0FBTyxHQUFHLCtFQUE2QixFQUFFLENBQUM7b0JBQ2hELE1BQU0sTUFBTSxHQUFHLDhEQUFXLENBQUMsT0FBTyxDQUFDLE9BQU8sRUFBRSxjQUFjLENBQUMsQ0FBQztvQkFFNUQsNEVBQTRFO29CQUM1RSw4RUFBOEU7b0JBQzlFLElBQUk7d0JBQ0YsTUFBTSxPQUFPLENBQUMsR0FBRyxDQUFDOzRCQUNoQixHQUFHLENBQUMsY0FBYyxDQUFDLFFBQVEsQ0FBQyxXQUFXLEVBQUU7NEJBQ3pDLEdBQUcsQ0FBQyxjQUFjLENBQUMsU0FBUyxDQUFDLFdBQVcsRUFBRTt5QkFDM0MsQ0FBQyxDQUFDO3FCQUNKO29CQUFDLE9BQU8sQ0FBQyxFQUFFO3dCQUNWLGFBQWE7d0JBQ2IsT0FBTyxDQUFDLEdBQUcsQ0FBQyw4Q0FBOEMsQ0FBQyxFQUFFLENBQUMsQ0FBQztxQkFDaEU7b0JBRUQsT0FBTyw4RUFBNEIsQ0FDakMsTUFBTSxFQUNOLEVBQUUsTUFBTSxFQUFFLE1BQU0sRUFBRSxFQUNsQixPQUFPLENBQ1I7eUJBQ0UsSUFBSSxDQUFDLE1BQU0sQ0FBQyxFQUFFO3dCQUNiLElBQUksTUFBTSxDQUFDLEVBQUUsRUFBRTs0QkFDYixnRUFBZ0U7NEJBQ2hFLE1BQU0sSUFBSSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsS0FBSyxDQUFDLENBQUM7NEJBQzNDLE1BQU0sRUFBRSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsR0FBRyxDQUFDLENBQUM7NEJBQ3ZDLEVBQUUsQ0FBQyxXQUFXLEdBQUcsS0FBSyxDQUFDLEVBQUUsQ0FDdkIsb0VBQW9FLENBQ3JFLENBQUM7NEJBQ0YsTUFBTSxFQUFFLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxHQUFHLENBQUMsQ0FBQzs0QkFDdkMsRUFBRSxDQUFDLFdBQVcsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUN2Qix3REFBd0QsQ0FDekQsQ0FBQzs0QkFFRixJQUFJLENBQUMsV0FBVyxDQUFDLEVBQUUsQ0FBQyxDQUFDOzRCQUNyQixJQUFJLENBQUMsV0FBVyxDQUFDLEVBQUUsQ0FBQyxDQUFDOzRCQUNyQixLQUFLLGdFQUFVLENBQUM7Z0NBQ2QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsZ0JBQWdCLENBQUM7Z0NBQ2pDLElBQUksRUFBRSxJQUFJLG9EQUFNLENBQUMsRUFBRSxJQUFJLEVBQUUsSUFBSSxFQUFFLENBQUM7Z0NBQ2hDLE9BQU8sRUFBRSxFQUFFOzZCQUNaLENBQUMsQ0FBQzs0QkFDSCxNQUFNLENBQUMsS0FBSyxFQUFFLENBQUM7eUJBQ2hCOzZCQUFNOzRCQUNMLE1BQU0sSUFBSSxnRkFBOEIsQ0FBQyxNQUFNLENBQUMsQ0FBQzt5QkFDbEQ7b0JBQ0gsQ0FBQyxDQUFDO3lCQUNELEtBQUssQ0FBQyxJQUFJLENBQUMsRUFBRTt3QkFDWixNQUFNLElBQUksK0VBQTZCLENBQUMsSUFBSSxDQUFDLENBQUM7b0JBQ2hELENBQUMsQ0FBQyxDQUFDO2lCQUNOO1lBQ0gsQ0FBQyxDQUFDLENBQUM7UUFDTCxDQUFDO0tBQ0YsQ0FBQyxDQUFDO0lBRUgsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsTUFBTSxFQUFFO1FBQ3JDLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFNBQVMsQ0FBQztRQUMxQixPQUFPLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyx1QkFBdUIsQ0FBQztRQUMxQyxTQUFTLEVBQUUsR0FBRyxFQUFFLENBQUMsSUFBSSxDQUFDLFNBQVM7UUFDL0IsU0FBUyxFQUFFLEdBQUcsRUFBRSxDQUFDLElBQUksQ0FBQyxTQUFTO1FBQy9CLE9BQU8sRUFBRSxHQUFHLEVBQUU7WUFDWixNQUFNLENBQUMsUUFBUSxDQUFDLFNBQVMsRUFBRSxFQUFFLElBQUksRUFBRSxJQUFJLEVBQUUsQ0FBQyxDQUFDO1FBQzdDLENBQUM7S0FDRixDQUFDLENBQUM7QUFDTCxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxTQUFTLGdCQUFnQixDQUN2QixHQUFvQixFQUNwQixJQUFpQixFQUNqQixLQUF3QjtJQUV4QixNQUFNLFFBQVEsR0FBRyxHQUFHLENBQUMsUUFBUSxDQUFDO0lBRTlCLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLGVBQWUsRUFBRTtRQUM5QyxHQUFHLDhFQUFxQixDQUN0QixHQUFHLEVBQ0gsSUFBSSxDQUFDLFdBQVcsQ0FBQyxlQUFlLEVBQ2hDO1lBQ0UsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsa0JBQWtCLENBQUM7WUFDbkMsT0FBTyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsc0JBQXNCLENBQUM7U0FDMUMsRUFDRCxLQUFLLENBQ047UUFDRCxJQUFJLEVBQUUsSUFBSSxDQUFDLEVBQUUsQ0FBQyxDQUFDLElBQUksQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLCtEQUFRLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQztLQUNwRCxDQUFDLENBQUM7SUFFSCxRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsaUJBQWlCLEVBQzVCLDhFQUFxQixDQUNuQixHQUFHLEVBQ0gsSUFBSSxDQUFDLFdBQVcsQ0FBQyxpQkFBaUIsRUFDbEM7UUFDRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxxQkFBcUIsQ0FBQztLQUN2QyxFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7SUFFRixRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxhQUFhLEVBQUU7UUFDNUMsR0FBRyw4RUFBcUIsQ0FDdEIsR0FBRyxFQUNILElBQUksQ0FBQyxXQUFXLENBQUMsYUFBYSxFQUM5QjtZQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGlCQUFpQixDQUFDO1lBQ2xDLE9BQU8sRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLG9CQUFvQixDQUFDO1NBQ3hDLEVBQ0QsS0FBSyxDQUNOO1FBQ0QsSUFBSSxFQUFFLElBQUksQ0FBQyxFQUFFLENBQUMsQ0FBQyxJQUFJLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxrRUFBVyxDQUFDLENBQUMsQ0FBQyxTQUFTLENBQUM7S0FDdkQsQ0FBQyxDQUFDO0lBRUgsUUFBUSxDQUFDLFVBQVUsQ0FDakIsVUFBVSxDQUFDLHFCQUFxQixFQUNoQyw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILENBQUMsSUFBSSxDQUFDLFdBQVcsQ0FBQyxhQUFhLEVBQUUsSUFBSSxDQUFDLFdBQVcsQ0FBQyxXQUFXLENBQUMsRUFDOUQ7UUFDRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQywyQkFBMkIsQ0FBQztLQUM3QyxFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7SUFFRixRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsWUFBWSxFQUN2Qiw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILElBQUksQ0FBQyxXQUFXLENBQUMsWUFBWSxFQUM3QjtRQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGdCQUFnQixDQUFDO0tBQ2xDLEVBQ0QsS0FBSyxDQUNOLENBQ0YsQ0FBQztJQUVGLFFBQVEsQ0FBQyxVQUFVLENBQ2pCLFVBQVUsQ0FBQyxjQUFjLEVBQ3pCLDhFQUFxQixDQUNuQixHQUFHLEVBQ0gsSUFBSSxDQUFDLFdBQVcsQ0FBQyxjQUFjLEVBQy9CO1FBQ0UsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsa0JBQWtCLENBQUM7UUFDbkMsT0FBTyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsa0JBQWtCLENBQUM7S0FDdEMsRUFDRCxLQUFLLENBQ04sQ0FDRixDQUFDO0lBRUYsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsa0JBQWtCLEVBQUU7UUFDakQsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsd0JBQXdCLENBQUM7UUFDekMsU0FBUyxFQUFFLEdBQUcsRUFBRTtZQUNkLE9BQU8sQ0FBQyxHQUFHLENBQUMsY0FBYyxDQUFDLFFBQVEsQ0FBQyxPQUFPLEVBQUUsQ0FBQyxJQUFJLEVBQUUsQ0FBQyxJQUFJLENBQUM7UUFDNUQsQ0FBQztRQUNELE9BQU8sRUFBRSxHQUFHLEVBQUU7WUFDWixPQUFPLGdFQUFVLENBQUM7Z0JBQ2hCLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGdCQUFnQixDQUFDO2dCQUNqQyxJQUFJLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyx3QkFBd0IsQ0FBQztnQkFDeEMsT0FBTyxFQUFFO29CQUNQLHFFQUFtQixDQUFDLEVBQUUsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsU0FBUyxDQUFDLEVBQUUsQ0FBQztvQkFDbkQsbUVBQWlCLENBQUMsRUFBRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxlQUFlLENBQUMsRUFBRSxDQUFDO2lCQUN4RDthQUNGLENBQUMsQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUU7Z0JBQ2YsSUFBSSxNQUFNLENBQUMsTUFBTSxDQUFDLE1BQU0sRUFBRTtvQkFDeEIsT0FBTyxHQUFHLENBQUMsY0FBYyxDQUFDLFFBQVEsQ0FBQyxXQUFXLEVBQUUsQ0FBQztpQkFDbEQ7WUFDSCxDQUFDLENBQUMsQ0FBQztRQUNMLENBQUM7S0FDRixDQUFDLENBQUM7QUFDTCxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxTQUFTLGNBQWMsQ0FDckIsR0FBb0IsRUFDcEIsSUFBZSxFQUNmLEtBQXdCO0lBRXhCLE1BQU0sUUFBUSxHQUFHLEdBQUcsQ0FBQyxRQUFRLENBQUM7SUFFOUIsUUFBUSxDQUFDLFVBQVUsQ0FDakIsVUFBVSxDQUFDLGFBQWEsRUFDeEIsOEVBQXFCLENBQ25CLEdBQUcsRUFDSCxJQUFJLENBQUMsYUFBYSxDQUFDLGlCQUFpQixFQUNwQztRQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLG1CQUFtQixDQUFDO0tBQ3JDLEVBQ0QsS0FBSyxDQUNOLENBQ0YsQ0FBQztJQUVGLFFBQVEsQ0FBQyxVQUFVLENBQ2pCLFVBQVUsQ0FBQyxhQUFhLEVBQ3hCLDhFQUFxQixDQUNuQixHQUFHLEVBQ0gsSUFBSSxDQUFDLGFBQWEsQ0FBQyxtQkFBbUIsRUFDdEM7UUFDRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxnQkFBZ0IsQ0FBQztLQUNsQyxFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7SUFFRixRQUFRLENBQUMsVUFBVSxDQUNqQixVQUFVLENBQUMsUUFBUSxFQUNuQiw4RUFBcUIsQ0FDbkIsR0FBRyxFQUNILElBQUksQ0FBQyxhQUFhLENBQUMsY0FBYyxFQUNqQztRQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFlBQVksQ0FBQztLQUM5QixFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7QUFDSixDQUFDO0FBRUQ7O0dBRUc7QUFDSCxTQUFTLGFBQWEsQ0FDcEIsR0FBb0IsRUFDcEIsSUFBYyxFQUNkLEtBQXdCO0lBRXhCLE1BQU0sUUFBUSxHQUFHLEdBQUcsQ0FBQyxRQUFRLENBQUM7SUFFOUIsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsR0FBRyxFQUFFO1FBQ2xDLEdBQUcsOEVBQXFCLENBQ3RCLEdBQUcsRUFDSCxJQUFJLENBQUMsV0FBVyxDQUFDLEdBQUcsRUFDcEI7WUFDRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxjQUFjLENBQUM7WUFDL0IsT0FBTyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsY0FBYyxDQUFDO1NBQ2xDLEVBQ0QsS0FBSyxDQUNOO1FBQ0QsSUFBSSxFQUFFLElBQUksQ0FBQyxFQUFFLENBQUMsQ0FBQyxJQUFJLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyw4REFBTyxDQUFDLENBQUMsQ0FBQyxTQUFTLENBQUM7S0FDbkQsQ0FBQyxDQUFDO0lBRUgsUUFBUSxDQUFDLFVBQVUsQ0FDakIsVUFBVSxDQUFDLE1BQU0sRUFDakIsOEVBQXFCLENBQ25CLEdBQUcsRUFDSCxJQUFJLENBQUMsV0FBVyxDQUFDLE1BQU0sRUFDdkI7UUFDRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxTQUFTLENBQUM7UUFDMUIsT0FBTyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsU0FBUyxDQUFDO0tBQzdCLEVBQ0QsS0FBSyxDQUNOLENBQ0YsQ0FBQztJQUVGLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLGdCQUFnQixFQUFFO1FBQy9DLEdBQUcsOEVBQXFCLENBQ3RCLEdBQUcsRUFDSCxDQUFDLElBQUksQ0FBQyxXQUFXLENBQUMsT0FBTyxFQUFFLElBQUksQ0FBQyxXQUFXLENBQUMsTUFBTSxDQUFDLEVBQ25EO1lBQ0UsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsNEJBQTRCLENBQUM7WUFDN0MsT0FBTyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsNEJBQTRCLENBQUM7U0FDaEQsRUFDRCxLQUFLLENBQ047UUFDRCxJQUFJLEVBQUUsSUFBSSxDQUFDLEVBQUUsQ0FBQyxDQUFDLElBQUksQ0FBQyxPQUFPLENBQUMsQ0FBQyxDQUFDLHNFQUFlLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQztLQUMzRCxDQUFDLENBQUM7QUFDTCxDQUFDO0FBRUQ7O0dBRUc7QUFDSCxTQUFTLGNBQWMsQ0FDckIsR0FBb0IsRUFDcEIsSUFBZSxFQUNmLFFBQTBCLEVBQzFCLEtBQXdCO0lBRXhCLE1BQU0sUUFBUSxHQUFHLEdBQUcsQ0FBQyxRQUFRLENBQUM7SUFFOUIsOENBQThDO0lBQzlDLE1BQU0sUUFBUSxHQUF3QixFQUFFLENBQUM7SUFDekMsNkRBQTZEO0lBQzdELElBQUksVUFBdUIsQ0FBQztJQUU1QixzQ0FBc0M7SUFDdEMsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsWUFBWSxFQUFFO1FBQzNDLEtBQUssRUFBRSxJQUFJLENBQUMsRUFBRTtZQUNaLElBQUksSUFBSSxDQUFDLEVBQUUsS0FBSyxTQUFTLEVBQUU7Z0JBQ3pCLE9BQU8sS0FBSyxDQUFDLEVBQUUsQ0FBQyxnQ0FBZ0MsQ0FBQyxDQUFDO2FBQ25EO1lBQ0QsTUFBTSxFQUFFLEdBQUcsSUFBSSxDQUFDLElBQUksQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUM1QixNQUFNLE1BQU0sR0FBRyx1REFBSSxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsT0FBTyxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxDQUFDLEVBQUUsS0FBSyxFQUFFLENBQUMsQ0FBQztZQUNqRSxPQUFPLENBQUMsTUFBTSxJQUFJLE1BQU0sQ0FBQyxLQUFLLENBQUMsS0FBSyxDQUFDLElBQUksRUFBRSxDQUFDO1FBQzlDLENBQUM7UUFDRCxTQUFTLEVBQUUsSUFBSSxDQUFDLEVBQUU7WUFDaEIsTUFBTSxFQUFFLEdBQUcsSUFBSSxDQUFDLElBQUksQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUM1QixPQUFPLENBQUMsQ0FBQyxHQUFHLENBQUMsS0FBSyxDQUFDLGFBQWEsSUFBSSxHQUFHLENBQUMsS0FBSyxDQUFDLGFBQWEsQ0FBQyxFQUFFLEtBQUssRUFBRSxDQUFDO1FBQ3hFLENBQUM7UUFDRCxPQUFPLEVBQUUsSUFBSSxDQUFDLEVBQUUsQ0FBQyxHQUFHLENBQUMsS0FBSyxDQUFDLFlBQVksQ0FBRSxJQUFJLENBQUMsSUFBSSxDQUFZLElBQUksRUFBRSxDQUFDO0tBQ3RFLENBQUMsQ0FBQztJQUVILElBQUksVUFBVSxHQUFHLEVBQUUsQ0FBQztJQUNwQix3Q0FBd0M7SUFDeEMsaUNBQWlDO0lBQ2pDLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLHlCQUF5QixFQUFFO1FBQ3hELEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLDhCQUE4QixDQUFDO1FBQy9DLFNBQVMsRUFBRSxHQUFHLEVBQUUsQ0FBQyxDQUFDLENBQUMsVUFBVTtRQUM3QixPQUFPLEVBQUUsR0FBRyxFQUFFLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsWUFBWSxFQUFFLEVBQUUsRUFBRSxFQUFFLFVBQVUsRUFBRSxDQUFDO0tBQzdFLENBQUMsQ0FBQztJQUVILElBQUksUUFBUSxFQUFFO1FBQ1osS0FBSyxHQUFHLENBQUMsUUFBUSxDQUFDLElBQUksQ0FBQyxHQUFHLEVBQUU7WUFDMUIsMENBQTBDO1lBQzFDLDJDQUEyQztZQUMzQyxlQUFlO1lBQ2YsTUFBTSxZQUFZLEdBQUcsR0FBRyxFQUFFO2dCQUN4QiwrQkFBK0I7Z0JBQy9CLElBQUksVUFBVSxJQUFJLENBQUMsVUFBVSxDQUFDLFVBQVUsRUFBRTtvQkFDeEMsVUFBVSxDQUFDLE9BQU8sRUFBRSxDQUFDO2lCQUN0QjtnQkFDRCxRQUFRLENBQUMsTUFBTSxHQUFHLENBQUMsQ0FBQztnQkFFcEIsSUFBSSwyQkFBMkIsR0FBRyxLQUFLLENBQUM7Z0JBQ3hDLEtBQUssTUFBTSxNQUFNLElBQUksR0FBRyxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLEVBQUU7b0JBQzlDLElBQUksTUFBTSxDQUFDLEVBQUUsS0FBSyxVQUFVLEVBQUU7d0JBQzVCLDJCQUEyQixHQUFHLElBQUksQ0FBQztxQkFDcEM7b0JBQ0QsUUFBUSxDQUFDLElBQUksQ0FBQzt3QkFDWixPQUFPLEVBQUUsVUFBVSxDQUFDLFlBQVk7d0JBQ2hDLElBQUksRUFBRSxFQUFFLEVBQUUsRUFBRSxNQUFNLENBQUMsRUFBRSxFQUFFO3FCQUN4QixDQUFDLENBQUM7aUJBQ0o7Z0JBQ0QsVUFBVSxHQUFHLElBQUksQ0FBQyxRQUFRLENBQUMsUUFBUSxFQUFFLENBQUMsQ0FBQyxDQUFDO2dCQUN4QyxVQUFVLEdBQUcsMkJBQTJCLENBQUMsQ0FBQyxDQUFDLFVBQVUsQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDO1lBQzdELENBQUMsQ0FBQztZQUNGLFlBQVksRUFBRSxDQUFDO1lBQ2YsUUFBUSxDQUFDLGNBQWMsQ0FBQyxPQUFPLENBQUMsR0FBRyxFQUFFO2dCQUNuQyxZQUFZLEVBQUUsQ0FBQztZQUNqQixDQUFDLENBQUMsQ0FBQztZQUNILHFFQUFxRTtZQUNyRSxRQUFRLENBQUMsY0FBYyxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUMsRUFBRSxJQUFJLEVBQUUsRUFBRTtnQkFDMUMsTUFBTSxNQUFNLEdBQUcsSUFBSSxDQUFDLFFBQVEsQ0FBQztnQkFDN0IsSUFBSSxDQUFDLE1BQU0sRUFBRTtvQkFDWCxPQUFPO2lCQUNSO2dCQUNELFVBQVUsR0FBRyxNQUFNLENBQUMsRUFBRSxDQUFDO1lBQ3pCLENBQUMsQ0FBQyxDQUFDO1FBQ0wsQ0FBQyxDQUFDLENBQUM7S0FDSjtBQUNILENBQUM7QUFFRDs7R0FFRztBQUNILFNBQVMsY0FBYyxDQUNyQixHQUFvQixFQUNwQixJQUFlLEVBQ2YsS0FBd0I7SUFFeEIsR0FBRyxDQUFDLFFBQVEsQ0FBQyxVQUFVLENBQ3JCLFVBQVUsQ0FBQyxTQUFTLEVBQ3BCLDhFQUFxQixDQUNuQixHQUFHLEVBQ0gsSUFBSSxDQUFDLFNBQVMsRUFDZDtRQUNFLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFlBQVksQ0FBQztRQUM3QixTQUFTLEVBQUUsS0FBSztLQUNqQixFQUNELEtBQUssQ0FDTixDQUNGLENBQUM7QUFDSixDQUFDO0FBRUQsaUVBQWUsTUFBTSxFQUFDO0FBRXRCOztHQUVHO0FBQ0gsSUFBVSxPQUFPLENBeUtoQjtBQXpLRCxXQUFVLE9BQU87SUFDZixLQUFLLFVBQVUsa0JBQWtCLENBQUMsS0FBd0I7UUFDeEQsTUFBTSxNQUFNLEdBQUcsTUFBTSxnRUFBVSxDQUFDO1lBQzlCLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGFBQWEsQ0FBQztZQUM5QixJQUFJLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FDWix3RkFBd0YsQ0FDekY7WUFDRCxPQUFPLEVBQUU7Z0JBQ1AscUVBQW1CLEVBQUU7Z0JBQ3JCLGlFQUFlLENBQUMsRUFBRSxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxRQUFRLENBQUMsRUFBRSxDQUFDO2FBQy9DO1NBQ0YsQ0FBQyxDQUFDO1FBRUgsSUFBSSxNQUFNLENBQUMsTUFBTSxDQUFDLE1BQU0sRUFBRTtZQUN4QixRQUFRLENBQUMsTUFBTSxFQUFFLENBQUM7U0FDbkI7SUFDSCxDQUFDO0lBRU0sS0FBSyxVQUFVLGdCQUFnQixDQUNwQyxRQUEwQixFQUMxQixPQUE2QixFQUM3QixXQUE0RCxFQUM1RCxVQUF1Qjs7UUFFdkIsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxJQUFJLFNBQVMsR0FBb0MsSUFBSSxDQUFDO1FBQ3RELElBQUksTUFBTSxHQUFpRCxFQUFFLENBQUM7UUFFOUQ7O1dBRUc7UUFDSCxTQUFTLFFBQVEsQ0FBQyxNQUFnQzs7WUFDaEQsTUFBTSxHQUFHLEVBQUUsQ0FBQztZQUNaLE1BQU0sY0FBYyxHQUFHLE1BQU0sQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQztpQkFDakQsR0FBRyxDQUFDLE1BQU0sQ0FBQyxFQUFFOztnQkFDWixNQUFNLEtBQUssR0FDVCxvQkFBUSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUUsQ0FBQyxNQUFNLENBQUMsbUJBQW1CLENBQUMsMENBQUUsSUFBSSxtQ0FBSSxFQUFFLENBQUM7Z0JBQ3BFLE1BQU0sQ0FBQyxNQUFNLENBQUMsR0FBRyxLQUFLLENBQUM7Z0JBQ3ZCLE9BQU8sS0FBSyxDQUFDO1lBQ2YsQ0FBQyxDQUFDO2lCQUNELE1BQU0sQ0FBQyxDQUFDLGtCQUFNLENBQUMsbUJBQW1CLENBQUMsMENBQUUsSUFBSSxtQ0FBSSxFQUFFLENBQUMsQ0FBQztpQkFDakQsV0FBVyxDQUNWLENBQUMsR0FBRyxFQUFFLEdBQUcsRUFBRSxFQUFFLENBQUMsdUZBQThCLENBQUMsR0FBRyxFQUFFLEdBQUcsRUFBRSxJQUFJLENBQUMsRUFDNUQsTUFBTSxDQUFDLFVBQVcsQ0FBQyxLQUFLLENBQUMsT0FBZ0IsQ0FDMUMsQ0FBQztZQUVKLHVFQUF1RTtZQUN2RSxnRkFBZ0Y7WUFDaEYsaUNBQWlDO1lBQ2pDLE1BQU0sQ0FBQyxVQUFXLENBQUMsS0FBSyxDQUFDLE9BQU8sR0FBRyx1RkFBOEIsQ0FDL0QsY0FBYyxFQUNkLE1BQU0sQ0FBQyxVQUFXLENBQUMsS0FBSyxDQUFDLE9BQWdCLEVBQ3pDLElBQUksQ0FDTDtnQkFDQyxvQkFBb0I7aUJBQ25CLElBQUksQ0FBQyxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQUUsRUFBRSxlQUFDLFFBQUMsT0FBQyxDQUFDLElBQUksbUNBQUksUUFBUSxDQUFDLEdBQUcsQ0FBQyxPQUFDLENBQUMsSUFBSSxtQ0FBSSxRQUFRLENBQUMsSUFBQyxDQUFDO1FBQ2pFLENBQUM7UUFFRCwyRUFBMkU7UUFDM0UsUUFBUSxDQUFDLFNBQVMsQ0FBQyxTQUFTLEVBQUU7WUFDNUIsT0FBTyxFQUFFLE1BQU0sQ0FBQyxFQUFFOztnQkFDaEIscURBQXFEO2dCQUNyRCxJQUFJLENBQUMsU0FBUyxFQUFFO29CQUNkLFNBQVMsR0FBRywrREFBZ0IsQ0FBQyxNQUFNLENBQUMsTUFBTSxDQUFDLENBQUM7b0JBQzVDLFFBQVEsQ0FBQyxTQUFTLENBQUMsQ0FBQztpQkFDckI7Z0JBRUQsTUFBTSxRQUFRLEdBQUcsMkJBQVMsQ0FBQyxVQUFVLDBDQUFFLEtBQUssMENBQUUsT0FBTyxtQ0FBSSxFQUFFLENBQUM7Z0JBQzVELE1BQU0sSUFBSSxHQUFHO29CQUNYLEdBQUcsTUFBTSxDQUFDLElBQUksQ0FBQyxJQUFJO29CQUNuQixLQUFLLEVBQUUsWUFBTSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsS0FBSyxtQ0FBSSxFQUFFO2lCQUNwQyxDQUFDO2dCQUNGLE1BQU0sU0FBUyxHQUFHO29CQUNoQixHQUFHLE1BQU0sQ0FBQyxJQUFJLENBQUMsU0FBUztvQkFDeEIsS0FBSyxFQUFFLHVGQUE4QixDQUNuQyxRQUFvQyxFQUNwQyxJQUFJLENBQUMsS0FBaUMsQ0FDdkM7aUJBQ0YsQ0FBQztnQkFFRixNQUFNLENBQUMsSUFBSSxHQUFHLEVBQUUsU0FBUyxFQUFFLElBQUksRUFBRSxDQUFDO2dCQUVsQyxPQUFPLE1BQU0sQ0FBQztZQUNoQixDQUFDO1lBQ0QsS0FBSyxFQUFFLE1BQU0sQ0FBQyxFQUFFO2dCQUNkLHFEQUFxRDtnQkFDckQsSUFBSSxDQUFDLFNBQVMsRUFBRTtvQkFDZCxTQUFTLEdBQUcsK0RBQWdCLENBQUMsTUFBTSxDQUFDLE1BQU0sQ0FBQyxDQUFDO29CQUM1QyxRQUFRLENBQUMsU0FBUyxDQUFDLENBQUM7aUJBQ3JCO2dCQUVELE9BQU87b0JBQ0wsSUFBSSxFQUFFLE1BQU0sQ0FBQyxJQUFJO29CQUNqQixFQUFFLEVBQUUsTUFBTSxDQUFDLEVBQUU7b0JBQ2IsR0FBRyxFQUFFLE1BQU0sQ0FBQyxHQUFHO29CQUNmLE1BQU0sRUFBRSxTQUFTO29CQUNqQixPQUFPLEVBQUUsTUFBTSxDQUFDLE9BQU87aUJBQ3hCLENBQUM7WUFDSixDQUFDO1NBQ0YsQ0FBQyxDQUFDO1FBRUgsbUVBQW1FO1FBQ25FLGlDQUFpQztRQUNqQyxNQUFNLFFBQVEsR0FBRyxNQUFNLFFBQVEsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLENBQUM7UUFFaEQsTUFBTSxZQUFZLEdBQ2hCLHFFQUFnQixDQUFDLFFBQVEsQ0FBQyxTQUFTLENBQUMsS0FBWSxDQUFDLG1DQUFJLEVBQUUsQ0FBQztRQUMxRCxNQUFNLEtBQUssR0FBRyxJQUFJLEtBQUssRUFBUSxDQUFDO1FBQ2hDLHVDQUF1QztRQUN2Qyx5RUFBdUIsQ0FDckIsWUFBWTthQUNULE1BQU0sQ0FBQyxJQUFJLENBQUMsRUFBRSxDQUFDLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQzthQUM5QixHQUFHLENBQUMsSUFBSSxDQUFDLEVBQUU7O1lBQ1YsT0FBTztnQkFDTCxHQUFHLElBQUk7Z0JBQ1AsS0FBSyxFQUFFLDRGQUFtQyxDQUFDLFVBQUksQ0FBQyxLQUFLLG1DQUFJLEVBQUUsQ0FBQzthQUM3RCxDQUFDO1FBQ0osQ0FBQyxDQUFDLEVBQ0osV0FBVyxDQUNaLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxFQUFFO1lBQ2YsS0FBSyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUNqQixPQUFPLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDaEIsQ0FBQyxDQUFDLENBQUM7UUFFSCxRQUFRLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxHQUFHLEVBQUU7O1lBQzVCLDZFQUE2RTtZQUM3RSx5QkFBeUI7WUFDekIsTUFBTSxRQUFRLEdBQUcsTUFBQyxRQUFRLENBQUMsU0FBUyxDQUFDLEtBQWEsbUNBQUksRUFBRSxDQUFDO1lBQ3pELElBQUksQ0FBQyxnRUFBaUIsQ0FBQyxZQUFZLEVBQUUsUUFBUSxDQUFDLEVBQUU7Z0JBQzlDLEtBQUssa0JBQWtCLENBQUMsS0FBSyxDQUFDLENBQUM7YUFDaEM7UUFDSCxDQUFDLENBQUMsQ0FBQztRQUVILFFBQVEsQ0FBQyxhQUFhLENBQUMsT0FBTyxDQUFDLEtBQUssRUFBRSxNQUFNLEVBQUUsTUFBTSxFQUFFLEVBQUU7O1lBQ3RELElBQUksTUFBTSxLQUFLLFNBQVMsRUFBRTtnQkFDeEIsa0NBQWtDO2dCQUNsQyxNQUFNLFFBQVEsR0FBRyxZQUFNLENBQUMsTUFBTSxDQUFDLG1DQUFJLEVBQUUsQ0FBQztnQkFDdEMsTUFBTSxRQUFRLEdBQ1osb0JBQVEsQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFFLENBQUMsTUFBTSxDQUFDLG1CQUFtQixDQUFDLDBDQUFFLElBQUksbUNBQUksRUFBRSxDQUFDO2dCQUNwRSxJQUFJLENBQUMsZ0VBQWlCLENBQUMsUUFBUSxFQUFFLFFBQVEsQ0FBQyxFQUFFO29CQUMxQyxJQUFJLE1BQU0sQ0FBQyxNQUFNLENBQUMsRUFBRTt3QkFDbEIscUZBQXFGO3dCQUNyRixNQUFNLGtCQUFrQixDQUFDLEtBQUssQ0FBQyxDQUFDO3FCQUNqQzt5QkFBTTt3QkFDTCwyRUFBMkU7d0JBQzNFLE1BQU0sQ0FBQyxNQUFNLENBQUMsR0FBRywrREFBZ0IsQ0FBQyxRQUFRLENBQUMsQ0FBQzt3QkFDNUMsaUNBQWlDO3dCQUNqQyxNQUFNLEtBQUssR0FBRyx1RkFBOEIsQ0FDMUMsUUFBUSxFQUNSLFlBQVksRUFDWixLQUFLLEVBQ0wsS0FBSyxDQUNOOzZCQUNFLE1BQU0sQ0FBQyxJQUFJLENBQUMsRUFBRSxDQUFDLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQzs2QkFDOUIsR0FBRyxDQUFDLElBQUksQ0FBQyxFQUFFOzs0QkFDVixPQUFPO2dDQUNMLEdBQUcsSUFBSTtnQ0FDUCxLQUFLLEVBQUUsNEZBQW1DLENBQUMsVUFBSSxDQUFDLEtBQUssbUNBQUksRUFBRSxDQUFDOzZCQUM3RCxDQUFDO3dCQUNKLENBQUMsQ0FBQyxDQUFDO3dCQUVMLHlFQUF1QixDQUFDLEtBQUssRUFBRSxLQUFLLEVBQUUsV0FBVyxDQUFDLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxFQUFFOzRCQUNoRSxPQUFPLENBQUMsSUFBSSxDQUFDLENBQUM7d0JBQ2hCLENBQUMsQ0FBQyxDQUFDO3FCQUNKO2lCQUNGO2FBQ0Y7UUFDSCxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUM7SUF0SnFCLHdCQUFnQixtQkFzSnJDO0FBQ0gsQ0FBQyxFQXpLUyxPQUFPLEtBQVAsT0FBTyxRQXlLaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBtYWlubWVudS1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBjcmVhdGVTZW1hbnRpY0NvbW1hbmQsXG4gIElMYWJTaGVsbCxcbiAgSVJvdXRlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgRGlhbG9nLFxuICBJQ29tbWFuZFBhbGV0dGUsXG4gIE1lbnVGYWN0b3J5LFxuICBzaG93RGlhbG9nXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFBhZ2VDb25maWcsIFVSTEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBJRWRpdE1lbnUsXG4gIElGaWxlTWVudSxcbiAgSUhlbHBNZW51LFxuICBJS2VybmVsTWVudSxcbiAgSU1haW5NZW51LFxuICBJUnVuTWVudSxcbiAgSVRhYnNNZW51LFxuICBJVmlld01lbnUsXG4gIE1haW5NZW51XG59IGZyb20gJ0BqdXB5dGVybGFiL21haW5tZW51JztcbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5LCBTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgZmFzdEZvcndhcmRJY29uLFxuICBSYW5rZWRNZW51LFxuICByZWZyZXNoSWNvbixcbiAgcnVuSWNvbixcbiAgc3RvcEljb25cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBmaW5kIH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgSlNPTkV4dCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IE1lbnUsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbmNvbnN0IFBMVUdJTl9JRCA9ICdAanVweXRlcmxhYi9tYWlubWVudS1leHRlbnNpb246cGx1Z2luJztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgY29tbWFuZCBJRHMgb2Ygc2VtYW50aWMgZXh0ZW5zaW9uIHBvaW50cy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IG9wZW5FZGl0ID0gJ2VkaXRtZW51Om9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCB1bmRvID0gJ2VkaXRtZW51OnVuZG8nO1xuXG4gIGV4cG9ydCBjb25zdCByZWRvID0gJ2VkaXRtZW51OnJlZG8nO1xuXG4gIGV4cG9ydCBjb25zdCBjbGVhckN1cnJlbnQgPSAnZWRpdG1lbnU6Y2xlYXItY3VycmVudCc7XG5cbiAgZXhwb3J0IGNvbnN0IGNsZWFyQWxsID0gJ2VkaXRtZW51OmNsZWFyLWFsbCc7XG5cbiAgZXhwb3J0IGNvbnN0IGZpbmQgPSAnZWRpdG1lbnU6ZmluZCc7XG5cbiAgZXhwb3J0IGNvbnN0IGdvVG9MaW5lID0gJ2VkaXRtZW51OmdvLXRvLWxpbmUnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuRmlsZSA9ICdmaWxlbWVudTpvcGVuJztcblxuICBleHBvcnQgY29uc3QgY2xvc2VBbmRDbGVhbnVwID0gJ2ZpbGVtZW51OmNsb3NlLWFuZC1jbGVhbnVwJztcblxuICBleHBvcnQgY29uc3QgY3JlYXRlQ29uc29sZSA9ICdmaWxlbWVudTpjcmVhdGUtY29uc29sZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNodXRkb3duID0gJ2ZpbGVtZW51OnNodXRkb3duJztcblxuICBleHBvcnQgY29uc3QgbG9nb3V0ID0gJ2ZpbGVtZW51OmxvZ291dCc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5LZXJuZWwgPSAna2VybmVsbWVudTpvcGVuJztcblxuICBleHBvcnQgY29uc3QgaW50ZXJydXB0S2VybmVsID0gJ2tlcm5lbG1lbnU6aW50ZXJydXB0JztcblxuICBleHBvcnQgY29uc3QgcmVjb25uZWN0VG9LZXJuZWwgPSAna2VybmVsbWVudTpyZWNvbm5lY3QtdG8ta2VybmVsJztcblxuICBleHBvcnQgY29uc3QgcmVzdGFydEtlcm5lbCA9ICdrZXJuZWxtZW51OnJlc3RhcnQnO1xuXG4gIGV4cG9ydCBjb25zdCByZXN0YXJ0S2VybmVsQW5kQ2xlYXIgPSAna2VybmVsbWVudTpyZXN0YXJ0LWFuZC1jbGVhcic7XG5cbiAgZXhwb3J0IGNvbnN0IGNoYW5nZUtlcm5lbCA9ICdrZXJuZWxtZW51OmNoYW5nZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNodXRkb3duS2VybmVsID0gJ2tlcm5lbG1lbnU6c2h1dGRvd24nO1xuXG4gIGV4cG9ydCBjb25zdCBzaHV0ZG93bkFsbEtlcm5lbHMgPSAna2VybmVsbWVudTpzaHV0ZG93bkFsbCc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5WaWV3ID0gJ3ZpZXdtZW51Om9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCB3b3JkV3JhcCA9ICd2aWV3bWVudTp3b3JkLXdyYXAnO1xuXG4gIGV4cG9ydCBjb25zdCBsaW5lTnVtYmVyaW5nID0gJ3ZpZXdtZW51OmxpbmUtbnVtYmVyaW5nJztcblxuICBleHBvcnQgY29uc3QgbWF0Y2hCcmFja2V0cyA9ICd2aWV3bWVudTptYXRjaC1icmFja2V0cyc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5SdW4gPSAncnVubWVudTpvcGVuJztcblxuICBleHBvcnQgY29uc3QgcnVuID0gJ3J1bm1lbnU6cnVuJztcblxuICBleHBvcnQgY29uc3QgcnVuQWxsID0gJ3J1bm1lbnU6cnVuLWFsbCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlc3RhcnRBbmRSdW5BbGwgPSAncnVubWVudTpyZXN0YXJ0LWFuZC1ydW4tYWxsJztcblxuICBleHBvcnQgY29uc3QgcnVuQWJvdmUgPSAncnVubWVudTpydW4tYWJvdmUnO1xuXG4gIGV4cG9ydCBjb25zdCBydW5CZWxvdyA9ICdydW5tZW51OnJ1bi1iZWxvdyc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5UYWJzID0gJ3RhYnNtZW51Om9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBhY3RpdmF0ZUJ5SWQgPSAndGFic21lbnU6YWN0aXZhdGUtYnktaWQnO1xuXG4gIGV4cG9ydCBjb25zdCBhY3RpdmF0ZVByZXZpb3VzbHlVc2VkVGFiID1cbiAgICAndGFic21lbnU6YWN0aXZhdGUtcHJldmlvdXNseS11c2VkLXRhYic7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5TZXR0aW5ncyA9ICdzZXR0aW5nc21lbnU6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5IZWxwID0gJ2hlbHBtZW51Om9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBnZXRLZXJuZWwgPSAnaGVscG1lbnU6Z2V0LWtlcm5lbCc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5GaXJzdCA9ICdtYWlubWVudTpvcGVuLWZpcnN0Jztcbn1cblxuLyoqXG4gKiBBIHNlcnZpY2UgcHJvdmlkaW5nIGFuIGludGVyZmFjZSB0byB0aGUgbWFpbiBtZW51LlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTWFpbk1lbnU+ID0ge1xuICBpZDogUExVR0lOX0lELFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgYW5kIHByb3ZpZGVzIHRoZSBhcHBsaWNhdGlvbiBtYWluIG1lbnUuJyxcbiAgcmVxdWlyZXM6IFtJUm91dGVyLCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlLCBJTGFiU2hlbGwsIElTZXR0aW5nUmVnaXN0cnldLFxuICBwcm92aWRlczogSU1haW5NZW51LFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHJvdXRlcjogSVJvdXRlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbFxuICApOiBQcm9taXNlPElNYWluTWVudT4gPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgY29uc3QgbWVudSA9IG5ldyBNYWluTWVudShjb21tYW5kcyk7XG4gICAgbWVudS5pZCA9ICdqcC1NYWluTWVudSc7XG4gICAgbWVudS5hZGRDbGFzcygnanAtc2Nyb2xsYmFyLXRpbnknKTtcblxuICAgIC8vIEJ1aWx0IG1lbnUgZnJvbSBzZXR0aW5nc1xuICAgIGlmIChyZWdpc3RyeSkge1xuICAgICAgYXdhaXQgUHJpdmF0ZS5sb2FkU2V0dGluZ3NNZW51KFxuICAgICAgICByZWdpc3RyeSxcbiAgICAgICAgKGFNZW51OiBSYW5rZWRNZW51KSA9PiB7XG4gICAgICAgICAgbWVudS5hZGRNZW51KGFNZW51LCBmYWxzZSwgeyByYW5rOiBhTWVudS5yYW5rIH0pO1xuICAgICAgICB9LFxuICAgICAgICBvcHRpb25zID0+IE1haW5NZW51LmdlbmVyYXRlTWVudShjb21tYW5kcywgb3B0aW9ucywgdHJhbnMpLFxuICAgICAgICB0cmFuc2xhdG9yXG4gICAgICApO1xuXG4gICAgICAvLyBUcmlnZ2VyIHNpbmdsZSB1cGRhdGVcbiAgICAgIG1lbnUudXBkYXRlKCk7XG4gICAgfVxuXG4gICAgLy8gT25seSBhZGQgcXVpdCBidXR0b24gaWYgdGhlIGJhY2stZW5kIHN1cHBvcnRzIGl0IGJ5IGNoZWNraW5nIHBhZ2UgY29uZmlnLlxuICAgIGNvbnN0IHF1aXRCdXR0b24gPSBQYWdlQ29uZmlnLmdldE9wdGlvbigncXVpdEJ1dHRvbicpLnRvTG93ZXJDYXNlKCk7XG4gICAgbWVudS5maWxlTWVudS5xdWl0RW50cnkgPSBxdWl0QnV0dG9uID09PSAndHJ1ZSc7XG5cbiAgICAvLyBDcmVhdGUgdGhlIGFwcGxpY2F0aW9uIG1lbnVzLlxuICAgIGNyZWF0ZUVkaXRNZW51KGFwcCwgbWVudS5lZGl0TWVudSwgdHJhbnMpO1xuICAgIGNyZWF0ZUZpbGVNZW51KGFwcCwgbWVudS5maWxlTWVudSwgcm91dGVyLCB0cmFucyk7XG4gICAgY3JlYXRlS2VybmVsTWVudShhcHAsIG1lbnUua2VybmVsTWVudSwgdHJhbnMpO1xuICAgIGNyZWF0ZVJ1bk1lbnUoYXBwLCBtZW51LnJ1bk1lbnUsIHRyYW5zKTtcbiAgICBjcmVhdGVWaWV3TWVudShhcHAsIG1lbnUudmlld01lbnUsIHRyYW5zKTtcbiAgICBjcmVhdGVIZWxwTWVudShhcHAsIG1lbnUuaGVscE1lbnUsIHRyYW5zKTtcblxuICAgIC8vIFRoZSB0YWJzIG1lbnUgcmVsaWVzIG9uIGxhYiBzaGVsbCBmdW5jdGlvbmFsaXR5LlxuICAgIGlmIChsYWJTaGVsbCkge1xuICAgICAgY3JlYXRlVGFic01lbnUoYXBwLCBtZW51LnRhYnNNZW51LCBsYWJTaGVsbCwgdHJhbnMpO1xuICAgIH1cblxuICAgIC8vIENyZWF0ZSBjb21tYW5kcyB0byBvcGVuIHRoZSBtYWluIGFwcGxpY2F0aW9uIG1lbnVzLlxuICAgIGNvbnN0IGFjdGl2YXRlTWVudSA9IChpdGVtOiBNZW51KSA9PiB7XG4gICAgICBtZW51LmFjdGl2ZU1lbnUgPSBpdGVtO1xuICAgICAgbWVudS5vcGVuQWN0aXZlTWVudSgpO1xuICAgIH07XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3BlbkVkaXQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnT3BlbiBFZGl0IE1lbnUnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IGFjdGl2YXRlTWVudShtZW51LmVkaXRNZW51KVxuICAgIH0pO1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuRmlsZSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIEZpbGUgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gYWN0aXZhdGVNZW51KG1lbnUuZmlsZU1lbnUpXG4gICAgfSk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5LZXJuZWwsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnT3BlbiBLZXJuZWwgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gYWN0aXZhdGVNZW51KG1lbnUua2VybmVsTWVudSlcbiAgICB9KTtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3BlblJ1biwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIFJ1biBNZW51JyksXG4gICAgICBleGVjdXRlOiAoKSA9PiBhY3RpdmF0ZU1lbnUobWVudS5ydW5NZW51KVxuICAgIH0pO1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuVmlldywge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIFZpZXcgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gYWN0aXZhdGVNZW51KG1lbnUudmlld01lbnUpXG4gICAgfSk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5TZXR0aW5ncywge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIFNldHRpbmdzIE1lbnUnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IGFjdGl2YXRlTWVudShtZW51LnNldHRpbmdzTWVudSlcbiAgICB9KTtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3BlblRhYnMsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnT3BlbiBUYWJzIE1lbnUnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IGFjdGl2YXRlTWVudShtZW51LnRhYnNNZW51KVxuICAgIH0pO1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuSGVscCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIEhlbHAgTWVudScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4gYWN0aXZhdGVNZW51KG1lbnUuaGVscE1lbnUpXG4gICAgfSk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5GaXJzdCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdPcGVuIEZpcnN0IE1lbnUnKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgbWVudS5hY3RpdmVJbmRleCA9IDA7XG4gICAgICAgIG1lbnUub3BlbkFjdGl2ZU1lbnUoKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICAvLyBBZGQgc29tZSBvZiB0aGUgY29tbWFuZHMgZGVmaW5lZCBoZXJlIHRvIHRoZSBjb21tYW5kIHBhbGV0dGUuXG4gICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLnNodXRkb3duLFxuICAgICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ01haW4gQXJlYScpXG4gICAgICB9KTtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMubG9nb3V0LFxuICAgICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ01haW4gQXJlYScpXG4gICAgICB9KTtcblxuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5zaHV0ZG93bkFsbEtlcm5lbHMsXG4gICAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnS2VybmVsIE9wZXJhdGlvbnMnKVxuICAgICAgfSk7XG5cbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuYWN0aXZhdGVQcmV2aW91c2x5VXNlZFRhYixcbiAgICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdNYWluIEFyZWEnKVxuICAgICAgfSk7XG4gICAgfVxuXG4gICAgYXBwLnNoZWxsLmFkZChtZW51LCAnbWVudScsIHsgcmFuazogMTAwIH0pO1xuXG4gICAgcmV0dXJuIG1lbnU7XG4gIH1cbn07XG5cbi8qKlxuICogQ3JlYXRlIHRoZSBiYXNpYyBgRWRpdGAgbWVudS5cbiAqL1xuZnVuY3Rpb24gY3JlYXRlRWRpdE1lbnUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBtZW51OiBJRWRpdE1lbnUsXG4gIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuKTogdm9pZCB7XG4gIGNvbnN0IGNvbW1hbmRzID0gYXBwLmNvbW1hbmRzO1xuXG4gIC8vIEFkZCB0aGUgdW5kby9yZWRvIGNvbW1hbmRzIHRoZSB0aGUgRWRpdCBtZW51LlxuICBjb21tYW5kcy5hZGRDb21tYW5kKFxuICAgIENvbW1hbmRJRHMudW5kbyxcbiAgICBjcmVhdGVTZW1hbnRpY0NvbW1hbmQoXG4gICAgICBhcHAsXG4gICAgICBtZW51LnVuZG9lcnMudW5kbyxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdVbmRvJylcbiAgICAgIH0sXG4gICAgICB0cmFuc1xuICAgIClcbiAgKTtcbiAgY29tbWFuZHMuYWRkQ29tbWFuZChcbiAgICBDb21tYW5kSURzLnJlZG8sXG4gICAgY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgbWVudS51bmRvZXJzLnJlZG8sXG4gICAgICB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnUmVkbycpXG4gICAgICB9LFxuICAgICAgdHJhbnNcbiAgICApXG4gICk7XG5cbiAgLy8gQWRkIHRoZSBjbGVhciBjb21tYW5kcyB0byB0aGUgRWRpdCBtZW51LlxuICBjb21tYW5kcy5hZGRDb21tYW5kKFxuICAgIENvbW1hbmRJRHMuY2xlYXJDdXJyZW50LFxuICAgIGNyZWF0ZVNlbWFudGljQ29tbWFuZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUuY2xlYXJlcnMuY2xlYXJDdXJyZW50LFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ0NsZWFyJylcbiAgICAgIH0sXG4gICAgICB0cmFuc1xuICAgIClcbiAgKTtcbiAgY29tbWFuZHMuYWRkQ29tbWFuZChcbiAgICBDb21tYW5kSURzLmNsZWFyQWxsLFxuICAgIGNyZWF0ZVNlbWFudGljQ29tbWFuZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUuY2xlYXJlcnMuY2xlYXJBbGwsXG4gICAgICB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnQ2xlYXIgQWxsJylcbiAgICAgIH0sXG4gICAgICB0cmFuc1xuICAgIClcbiAgKTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKFxuICAgIENvbW1hbmRJRHMuZ29Ub0xpbmUsXG4gICAgY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5nb1RvTGluZXJzLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ0dvIHRvIExpbmXigKYnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKVxuICApO1xufVxuXG4vKipcbiAqIENyZWF0ZSB0aGUgYmFzaWMgYEZpbGVgIG1lbnUuXG4gKi9cbmZ1bmN0aW9uIGNyZWF0ZUZpbGVNZW51KFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgbWVudTogSUZpbGVNZW51LFxuICByb3V0ZXI6IElSb3V0ZXIsXG4gIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuKTogdm9pZCB7XG4gIGNvbnN0IGNvbW1hbmRzID0gYXBwLmNvbW1hbmRzO1xuXG4gIC8vIEFkZCBhIGRlbGVnYXRvciBjb21tYW5kIGZvciBjbG9zaW5nIGFuZCBjbGVhbmluZyB1cCBhbiBhY3Rpdml0eS5cbiAgLy8gVGhpcyBvbmUgaXMgYSBiaXQgZGlmZmVyZW50LCBpbiB0aGF0IHdlIGNvbnNpZGVyIGl0IGVuYWJsZWRcbiAgLy8gZXZlbiBpZiBpdCBjYW5ub3QgZmluZCBhIGRlbGVnYXRlIGZvciB0aGUgYWN0aXZpdHkuXG4gIC8vIEluIHRoYXQgY2FzZSwgd2UgaW5zdGVhZCBjYWxsIHRoZSBhcHBsaWNhdGlvbiBgY2xvc2VgIGNvbW1hbmQuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbG9zZUFuZENsZWFudXAsIHtcbiAgICAuLi5jcmVhdGVTZW1hbnRpY0NvbW1hbmQoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmNsb3NlQW5kQ2xlYW5lcnMsXG4gICAgICB7XG4gICAgICAgIGV4ZWN1dGU6ICdhcHBsaWNhdGlvbjpjbG9zZScsXG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnQ2xvc2UgYW5kIFNodXQgRG93bicpLFxuICAgICAgICBpc0VuYWJsZWQ6IHRydWVcbiAgICAgIH0sXG4gICAgICB0cmFuc1xuICAgICksXG4gICAgaXNFbmFibGVkOiAoKSA9PlxuICAgICAgISFhcHAuc2hlbGwuY3VycmVudFdpZGdldCAmJiAhIWFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0LnRpdGxlLmNsb3NhYmxlXG4gIH0pO1xuXG4gIC8vIEFkZCBhIGRlbGVnYXRvciBjb21tYW5kIGZvciBjcmVhdGluZyBhIGNvbnNvbGUgZm9yIGFuIGFjdGl2aXR5LlxuICBjb21tYW5kcy5hZGRDb21tYW5kKFxuICAgIENvbW1hbmRJRHMuY3JlYXRlQ29uc29sZSxcbiAgICBjcmVhdGVTZW1hbnRpY0NvbW1hbmQoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmNvbnNvbGVDcmVhdG9ycyxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdOZXcgQ29uc29sZSBmb3IgQWN0aXZpdHknKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKVxuICApO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaHV0ZG93biwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duJyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ1NodXQgZG93biBKdXB5dGVyTGFiJyksXG4gICAgaXNWaXNpYmxlOiAoKSA9PiBtZW51LnF1aXRFbnRyeSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IG1lbnUucXVpdEVudHJ5LFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdTaHV0ZG93biBjb25maXJtYXRpb24nKSxcbiAgICAgICAgYm9keTogdHJhbnMuX18oJ1BsZWFzZSBjb25maXJtIHlvdSB3YW50IHRvIHNodXQgZG93biBKdXB5dGVyTGFiLicpLFxuICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbigpLFxuICAgICAgICAgIERpYWxvZy53YXJuQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdTaHV0IERvd24nKSB9KVxuICAgICAgICBdXG4gICAgICB9KS50aGVuKGFzeW5jIHJlc3VsdCA9PiB7XG4gICAgICAgIGlmIChyZXN1bHQuYnV0dG9uLmFjY2VwdCkge1xuICAgICAgICAgIGNvbnN0IHNldHRpbmcgPSBTZXJ2ZXJDb25uZWN0aW9uLm1ha2VTZXR0aW5ncygpO1xuICAgICAgICAgIGNvbnN0IGFwaVVSTCA9IFVSTEV4dC5qb2luKHNldHRpbmcuYmFzZVVybCwgJ2FwaS9zaHV0ZG93bicpO1xuXG4gICAgICAgICAgLy8gU2h1dGRvd24gYWxsIGtlcm5lbCBhbmQgdGVybWluYWwgc2Vzc2lvbnMgYmVmb3JlIHNodXR0aW5nIGRvd24gdGhlIHNlcnZlclxuICAgICAgICAgIC8vIElmIHRoaXMgZmFpbHMsIHdlIGNvbnRpbnVlIGV4ZWN1dGlvbiBzbyB3ZSBjYW4gcG9zdCBhbiBhcGkvc2h1dGRvd24gcmVxdWVzdFxuICAgICAgICAgIHRyeSB7XG4gICAgICAgICAgICBhd2FpdCBQcm9taXNlLmFsbChbXG4gICAgICAgICAgICAgIGFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5zaHV0ZG93bkFsbCgpLFxuICAgICAgICAgICAgICBhcHAuc2VydmljZU1hbmFnZXIudGVybWluYWxzLnNodXRkb3duQWxsKClcbiAgICAgICAgICAgIF0pO1xuICAgICAgICAgIH0gY2F0Y2ggKGUpIHtcbiAgICAgICAgICAgIC8vIERvIG5vdGhpbmdcbiAgICAgICAgICAgIGNvbnNvbGUubG9nKGBGYWlsZWQgdG8gc2h1dGRvd24gc2Vzc2lvbnMgYW5kIHRlcm1pbmFsczogJHtlfWApO1xuICAgICAgICAgIH1cblxuICAgICAgICAgIHJldHVybiBTZXJ2ZXJDb25uZWN0aW9uLm1ha2VSZXF1ZXN0KFxuICAgICAgICAgICAgYXBpVVJMLFxuICAgICAgICAgICAgeyBtZXRob2Q6ICdQT1NUJyB9LFxuICAgICAgICAgICAgc2V0dGluZ1xuICAgICAgICAgIClcbiAgICAgICAgICAgIC50aGVuKHJlc3VsdCA9PiB7XG4gICAgICAgICAgICAgIGlmIChyZXN1bHQub2spIHtcbiAgICAgICAgICAgICAgICAvLyBDbG9zZSB0aGlzIHdpbmRvdyBpZiB0aGUgc2h1dGRvd24gcmVxdWVzdCBoYXMgYmVlbiBzdWNjZXNzZnVsXG4gICAgICAgICAgICAgICAgY29uc3QgYm9keSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgICAgICAgICAgICAgIGNvbnN0IHAxID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncCcpO1xuICAgICAgICAgICAgICAgIHAxLnRleHRDb250ZW50ID0gdHJhbnMuX18oXG4gICAgICAgICAgICAgICAgICAnWW91IGhhdmUgc2h1dCBkb3duIHRoZSBKdXB5dGVyIHNlcnZlci4gWW91IGNhbiBub3cgY2xvc2UgdGhpcyB0YWIuJ1xuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgY29uc3QgcDIgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdwJyk7XG4gICAgICAgICAgICAgICAgcDIudGV4dENvbnRlbnQgPSB0cmFucy5fXyhcbiAgICAgICAgICAgICAgICAgICdUbyB1c2UgSnVweXRlckxhYiBhZ2FpbiwgeW91IHdpbGwgbmVlZCB0byByZWxhdW5jaCBpdC4nXG4gICAgICAgICAgICAgICAgKTtcblxuICAgICAgICAgICAgICAgIGJvZHkuYXBwZW5kQ2hpbGQocDEpO1xuICAgICAgICAgICAgICAgIGJvZHkuYXBwZW5kQ2hpbGQocDIpO1xuICAgICAgICAgICAgICAgIHZvaWQgc2hvd0RpYWxvZyh7XG4gICAgICAgICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ1NlcnZlciBzdG9wcGVkJyksXG4gICAgICAgICAgICAgICAgICBib2R5OiBuZXcgV2lkZ2V0KHsgbm9kZTogYm9keSB9KSxcbiAgICAgICAgICAgICAgICAgIGJ1dHRvbnM6IFtdXG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgd2luZG93LmNsb3NlKCk7XG4gICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uUmVzcG9uc2VFcnJvcihyZXN1bHQpO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9KVxuICAgICAgICAgICAgLmNhdGNoKGRhdGEgPT4ge1xuICAgICAgICAgICAgICB0aHJvdyBuZXcgU2VydmVyQ29ubmVjdGlvbi5OZXR3b3JrRXJyb3IoZGF0YSk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubG9nb3V0LCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdMb2cgT3V0JyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ0xvZyBvdXQgb2YgSnVweXRlckxhYicpLFxuICAgIGlzVmlzaWJsZTogKCkgPT4gbWVudS5xdWl0RW50cnksXG4gICAgaXNFbmFibGVkOiAoKSA9PiBtZW51LnF1aXRFbnRyeSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICByb3V0ZXIubmF2aWdhdGUoJy9sb2dvdXQnLCB7IGhhcmQ6IHRydWUgfSk7XG4gICAgfVxuICB9KTtcbn1cblxuLyoqXG4gKiBDcmVhdGUgdGhlIGJhc2ljIGBLZXJuZWxgIG1lbnUuXG4gKi9cbmZ1bmN0aW9uIGNyZWF0ZUtlcm5lbE1lbnUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBtZW51OiBJS2VybmVsTWVudSxcbiAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4pOiB2b2lkIHtcbiAgY29uc3QgY29tbWFuZHMgPSBhcHAuY29tbWFuZHM7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmludGVycnVwdEtlcm5lbCwge1xuICAgIC4uLmNyZWF0ZVNlbWFudGljQ29tbWFuZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUua2VybmVsVXNlcnMuaW50ZXJydXB0S2VybmVsLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ0ludGVycnVwdCBLZXJuZWwnKSxcbiAgICAgICAgY2FwdGlvbjogdHJhbnMuX18oJ0ludGVycnVwdCB0aGUga2VybmVsJylcbiAgICAgIH0sXG4gICAgICB0cmFuc1xuICAgICksXG4gICAgaWNvbjogYXJncyA9PiAoYXJncy50b29sYmFyID8gc3RvcEljb24gOiB1bmRlZmluZWQpXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoXG4gICAgQ29tbWFuZElEcy5yZWNvbm5lY3RUb0tlcm5lbCxcbiAgICBjcmVhdGVTZW1hbnRpY0NvbW1hbmQoXG4gICAgICBhcHAsXG4gICAgICBtZW51Lmtlcm5lbFVzZXJzLnJlY29ubmVjdFRvS2VybmVsLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1JlY29ubmVjdCB0byBLZXJuZWwnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKVxuICApO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZXN0YXJ0S2VybmVsLCB7XG4gICAgLi4uY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5rZXJuZWxVc2Vycy5yZXN0YXJ0S2VybmVsLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1Jlc3RhcnQgS2VybmVs4oCmJyksXG4gICAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdSZXN0YXJ0IHRoZSBrZXJuZWwnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKSxcbiAgICBpY29uOiBhcmdzID0+IChhcmdzLnRvb2xiYXIgPyByZWZyZXNoSWNvbiA6IHVuZGVmaW5lZClcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChcbiAgICBDb21tYW5kSURzLnJlc3RhcnRLZXJuZWxBbmRDbGVhcixcbiAgICBjcmVhdGVTZW1hbnRpY0NvbW1hbmQoXG4gICAgICBhcHAsXG4gICAgICBbbWVudS5rZXJuZWxVc2Vycy5yZXN0YXJ0S2VybmVsLCBtZW51Lmtlcm5lbFVzZXJzLmNsZWFyV2lkZ2V0XSxcbiAgICAgIHtcbiAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdSZXN0YXJ0IEtlcm5lbCBhbmQgQ2xlYXLigKYnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKVxuICApO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoXG4gICAgQ29tbWFuZElEcy5jaGFuZ2VLZXJuZWwsXG4gICAgY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5rZXJuZWxVc2Vycy5jaGFuZ2VLZXJuZWwsXG4gICAgICB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnQ2hhbmdlIEtlcm5lbOKApicpXG4gICAgICB9LFxuICAgICAgdHJhbnNcbiAgICApXG4gICk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChcbiAgICBDb21tYW5kSURzLnNodXRkb3duS2VybmVsLFxuICAgIGNyZWF0ZVNlbWFudGljQ29tbWFuZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUua2VybmVsVXNlcnMuc2h1dGRvd25LZXJuZWwsXG4gICAgICB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duIEtlcm5lbCcpLFxuICAgICAgICBjYXB0aW9uOiB0cmFucy5fXygnU2h1dCBkb3duIGtlcm5lbCcpXG4gICAgICB9LFxuICAgICAgdHJhbnNcbiAgICApXG4gICk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNodXRkb3duQWxsS2VybmVscywge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duIEFsbCBLZXJuZWxz4oCmJyksXG4gICAgaXNFbmFibGVkOiAoKSA9PiB7XG4gICAgICByZXR1cm4gIWFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5ydW5uaW5nKCkubmV4dCgpLmRvbmU7XG4gICAgfSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgIHRpdGxlOiB0cmFucy5fXygnU2h1dCBEb3duIEFsbD8nKSxcbiAgICAgICAgYm9keTogdHJhbnMuX18oJ1NodXQgZG93biBhbGwga2VybmVscz8nKSxcbiAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0Rpc21pc3MnKSB9KSxcbiAgICAgICAgICBEaWFsb2cud2FybkJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duIEFsbCcpIH0pXG4gICAgICAgIF1cbiAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgICAgcmV0dXJuIGFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5zaHV0ZG93bkFsbCgpO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG4gIH0pO1xufVxuXG4vKipcbiAqIENyZWF0ZSB0aGUgYmFzaWMgYFZpZXdgIG1lbnUuXG4gKi9cbmZ1bmN0aW9uIGNyZWF0ZVZpZXdNZW51KFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgbWVudTogSVZpZXdNZW51LFxuICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbik6IHZvaWQge1xuICBjb25zdCBjb21tYW5kcyA9IGFwcC5jb21tYW5kcztcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKFxuICAgIENvbW1hbmRJRHMubGluZU51bWJlcmluZyxcbiAgICBjcmVhdGVTZW1hbnRpY0NvbW1hbmQoXG4gICAgICBhcHAsXG4gICAgICBtZW51LmVkaXRvclZpZXdlcnMudG9nZ2xlTGluZU51bWJlcnMsXG4gICAgICB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnU2hvdyBMaW5lIE51bWJlcnMnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKVxuICApO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoXG4gICAgQ29tbWFuZElEcy5tYXRjaEJyYWNrZXRzLFxuICAgIGNyZWF0ZVNlbWFudGljQ29tbWFuZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUuZWRpdG9yVmlld2Vycy50b2dnbGVNYXRjaEJyYWNrZXRzLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ01hdGNoIEJyYWNrZXRzJylcbiAgICAgIH0sXG4gICAgICB0cmFuc1xuICAgIClcbiAgKTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKFxuICAgIENvbW1hbmRJRHMud29yZFdyYXAsXG4gICAgY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5lZGl0b3JWaWV3ZXJzLnRvZ2dsZVdvcmRXcmFwLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1dyYXAgV29yZHMnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKVxuICApO1xufVxuXG4vKipcbiAqIENyZWF0ZSB0aGUgYmFzaWMgYFJ1bmAgbWVudS5cbiAqL1xuZnVuY3Rpb24gY3JlYXRlUnVuTWVudShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIG1lbnU6IElSdW5NZW51LFxuICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbik6IHZvaWQge1xuICBjb25zdCBjb21tYW5kcyA9IGFwcC5jb21tYW5kcztcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucnVuLCB7XG4gICAgLi4uY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5jb2RlUnVubmVycy5ydW4sXG4gICAgICB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnUnVuIFNlbGVjdGVkJyksXG4gICAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdSdW4gU2VsZWN0ZWQnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKSxcbiAgICBpY29uOiBhcmdzID0+IChhcmdzLnRvb2xiYXIgPyBydW5JY29uIDogdW5kZWZpbmVkKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKFxuICAgIENvbW1hbmRJRHMucnVuQWxsLFxuICAgIGNyZWF0ZVNlbWFudGljQ29tbWFuZChcbiAgICAgIGFwcCxcbiAgICAgIG1lbnUuY29kZVJ1bm5lcnMucnVuQWxsLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1J1biBBbGwnKSxcbiAgICAgICAgY2FwdGlvbjogdHJhbnMuX18oJ1J1biBBbGwnKVxuICAgICAgfSxcbiAgICAgIHRyYW5zXG4gICAgKVxuICApO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZXN0YXJ0QW5kUnVuQWxsLCB7XG4gICAgLi4uY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgW21lbnUuY29kZVJ1bm5lcnMucmVzdGFydCwgbWVudS5jb2RlUnVubmVycy5ydW5BbGxdLFxuICAgICAge1xuICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1Jlc3RhcnQgS2VybmVsIGFuZCBSdW4gQWxsJyksXG4gICAgICAgIGNhcHRpb246IHRyYW5zLl9fKCdSZXN0YXJ0IEtlcm5lbCBhbmQgUnVuIEFsbCcpXG4gICAgICB9LFxuICAgICAgdHJhbnNcbiAgICApLFxuICAgIGljb246IGFyZ3MgPT4gKGFyZ3MudG9vbGJhciA/IGZhc3RGb3J3YXJkSWNvbiA6IHVuZGVmaW5lZClcbiAgfSk7XG59XG5cbi8qKlxuICogQ3JlYXRlIHRoZSBiYXNpYyBgVGFic2AgbWVudS5cbiAqL1xuZnVuY3Rpb24gY3JlYXRlVGFic01lbnUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBtZW51OiBJVGFic01lbnUsXG4gIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbik6IHZvaWQge1xuICBjb25zdCBjb21tYW5kcyA9IGFwcC5jb21tYW5kcztcblxuICAvLyBBIGxpc3Qgb2YgdGhlIGFjdGl2ZSB0YWJzIGluIHRoZSBtYWluIGFyZWEuXG4gIGNvbnN0IHRhYkdyb3VwOiBNZW51LklJdGVtT3B0aW9uc1tdID0gW107XG4gIC8vIEEgZGlzcG9zYWJsZSBmb3IgZ2V0dGluZyByaWQgb2YgdGhlIG91dC1vZi1kYXRlIHRhYnMgbGlzdC5cbiAgbGV0IGRpc3Bvc2FibGU6IElEaXNwb3NhYmxlO1xuXG4gIC8vIENvbW1hbmQgdG8gYWN0aXZhdGUgYSB3aWRnZXQgYnkgaWQuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5hY3RpdmF0ZUJ5SWQsIHtcbiAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICBpZiAoYXJncy5pZCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIHJldHVybiB0cmFucy5fXygnQWN0aXZhdGUgYSB3aWRnZXQgYnkgaXRzIGBpZGAuJyk7XG4gICAgICB9XG4gICAgICBjb25zdCBpZCA9IGFyZ3NbJ2lkJ10gfHwgJyc7XG4gICAgICBjb25zdCB3aWRnZXQgPSBmaW5kKGFwcC5zaGVsbC53aWRnZXRzKCdtYWluJyksIHcgPT4gdy5pZCA9PT0gaWQpO1xuICAgICAgcmV0dXJuICh3aWRnZXQgJiYgd2lkZ2V0LnRpdGxlLmxhYmVsKSB8fCAnJztcbiAgICB9LFxuICAgIGlzVG9nZ2xlZDogYXJncyA9PiB7XG4gICAgICBjb25zdCBpZCA9IGFyZ3NbJ2lkJ10gfHwgJyc7XG4gICAgICByZXR1cm4gISFhcHAuc2hlbGwuY3VycmVudFdpZGdldCAmJiBhcHAuc2hlbGwuY3VycmVudFdpZGdldC5pZCA9PT0gaWQ7XG4gICAgfSxcbiAgICBleGVjdXRlOiBhcmdzID0+IGFwcC5zaGVsbC5hY3RpdmF0ZUJ5SWQoKGFyZ3NbJ2lkJ10gYXMgc3RyaW5nKSB8fCAnJylcbiAgfSk7XG5cbiAgbGV0IHByZXZpb3VzSWQgPSAnJztcbiAgLy8gQ29tbWFuZCB0byB0b2dnbGUgYmV0d2VlbiB0aGUgY3VycmVudFxuICAvLyB0YWIgYW5kIHRoZSBsYXN0IG1vZGlmaWVkIHRhYi5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmFjdGl2YXRlUHJldmlvdXNseVVzZWRUYWIsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0FjdGl2YXRlIFByZXZpb3VzbHkgVXNlZCBUYWInKSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+ICEhcHJldmlvdXNJZCxcbiAgICBleGVjdXRlOiAoKSA9PiBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuYWN0aXZhdGVCeUlkLCB7IGlkOiBwcmV2aW91c0lkIH0pXG4gIH0pO1xuXG4gIGlmIChsYWJTaGVsbCkge1xuICAgIHZvaWQgYXBwLnJlc3RvcmVkLnRoZW4oKCkgPT4ge1xuICAgICAgLy8gSXRlcmF0ZSBvdmVyIHRoZSBjdXJyZW50IHdpZGdldHMgaW4gdGhlXG4gICAgICAvLyBtYWluIGFyZWEsIGFuZCBhZGQgdGhlbSB0byB0aGUgdGFiIGdyb3VwXG4gICAgICAvLyBvZiB0aGUgbWVudS5cbiAgICAgIGNvbnN0IHBvcHVsYXRlVGFicyA9ICgpID0+IHtcbiAgICAgICAgLy8gcmVtb3ZlIHRoZSBwcmV2aW91cyB0YWIgbGlzdFxuICAgICAgICBpZiAoZGlzcG9zYWJsZSAmJiAhZGlzcG9zYWJsZS5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgZGlzcG9zYWJsZS5kaXNwb3NlKCk7XG4gICAgICAgIH1cbiAgICAgICAgdGFiR3JvdXAubGVuZ3RoID0gMDtcblxuICAgICAgICBsZXQgaXNQcmV2aW91c2x5VXNlZFRhYkF0dGFjaGVkID0gZmFsc2U7XG4gICAgICAgIGZvciAoY29uc3Qgd2lkZ2V0IG9mIGFwcC5zaGVsbC53aWRnZXRzKCdtYWluJykpIHtcbiAgICAgICAgICBpZiAod2lkZ2V0LmlkID09PSBwcmV2aW91c0lkKSB7XG4gICAgICAgICAgICBpc1ByZXZpb3VzbHlVc2VkVGFiQXR0YWNoZWQgPSB0cnVlO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0YWJHcm91cC5wdXNoKHtcbiAgICAgICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuYWN0aXZhdGVCeUlkLFxuICAgICAgICAgICAgYXJnczogeyBpZDogd2lkZ2V0LmlkIH1cbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgICBkaXNwb3NhYmxlID0gbWVudS5hZGRHcm91cCh0YWJHcm91cCwgMSk7XG4gICAgICAgIHByZXZpb3VzSWQgPSBpc1ByZXZpb3VzbHlVc2VkVGFiQXR0YWNoZWQgPyBwcmV2aW91c0lkIDogJyc7XG4gICAgICB9O1xuICAgICAgcG9wdWxhdGVUYWJzKCk7XG4gICAgICBsYWJTaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgcG9wdWxhdGVUYWJzKCk7XG4gICAgICB9KTtcbiAgICAgIC8vIFVwZGF0ZSB0aGUgSUQgb2YgdGhlIHByZXZpb3VzIGFjdGl2ZSB0YWIgaWYgYSBuZXcgdGFiIGlzIHNlbGVjdGVkLlxuICAgICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdCgoXywgYXJncykgPT4ge1xuICAgICAgICBjb25zdCB3aWRnZXQgPSBhcmdzLm9sZFZhbHVlO1xuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBwcmV2aW91c0lkID0gd2lkZ2V0LmlkO1xuICAgICAgfSk7XG4gICAgfSk7XG4gIH1cbn1cblxuLyoqXG4gKiBDcmVhdGUgdGhlIGJhc2ljIGBIZWxwYCBtZW51LlxuICovXG5mdW5jdGlvbiBjcmVhdGVIZWxwTWVudShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIG1lbnU6IElIZWxwTWVudSxcbiAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4pOiB2b2lkIHtcbiAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoXG4gICAgQ29tbWFuZElEcy5nZXRLZXJuZWwsXG4gICAgY3JlYXRlU2VtYW50aWNDb21tYW5kKFxuICAgICAgYXBwLFxuICAgICAgbWVudS5nZXRLZXJuZWwsXG4gICAgICB7XG4gICAgICAgIGxhYmVsOiB0cmFucy5fXygnR2V0IEtlcm5lbCcpLFxuICAgICAgICBpc1Zpc2libGU6IGZhbHNlXG4gICAgICB9LFxuICAgICAgdHJhbnNcbiAgICApXG4gICk7XG59XG5cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgUHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGFzeW5jIGZ1bmN0aW9uIGRpc3BsYXlJbmZvcm1hdGlvbih0cmFuczogVHJhbnNsYXRpb25CdW5kbGUpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBzaG93RGlhbG9nKHtcbiAgICAgIHRpdGxlOiB0cmFucy5fXygnSW5mb3JtYXRpb24nKSxcbiAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAnTWVudSBjdXN0b21pemF0aW9uIGhhcyBjaGFuZ2VkLiBZb3Ugd2lsbCBuZWVkIHRvIHJlbG9hZCBKdXB5dGVyTGFiIHRvIHNlZSB0aGUgY2hhbmdlcy4nXG4gICAgICApLFxuICAgICAgYnV0dG9uczogW1xuICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKCksXG4gICAgICAgIERpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnUmVsb2FkJykgfSlcbiAgICAgIF1cbiAgICB9KTtcblxuICAgIGlmIChyZXN1bHQuYnV0dG9uLmFjY2VwdCkge1xuICAgICAgbG9jYXRpb24ucmVsb2FkKCk7XG4gICAgfVxuICB9XG5cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGxvYWRTZXR0aW5nc01lbnUoXG4gICAgcmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgYWRkTWVudTogKG1lbnU6IE1lbnUpID0+IHZvaWQsXG4gICAgbWVudUZhY3Rvcnk6IChvcHRpb25zOiBJTWFpbk1lbnUuSU1lbnVPcHRpb25zKSA9PiBSYW5rZWRNZW51LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgbGV0IGNhbm9uaWNhbDogSVNldHRpbmdSZWdpc3RyeS5JU2NoZW1hIHwgbnVsbCA9IG51bGw7XG4gICAgbGV0IGxvYWRlZDogeyBbbmFtZTogc3RyaW5nXTogSVNldHRpbmdSZWdpc3RyeS5JTWVudVtdIH0gPSB7fTtcblxuICAgIC8qKlxuICAgICAqIFBvcHVsYXRlIHRoZSBwbHVnaW4ncyBzY2hlbWEgZGVmYXVsdHMuXG4gICAgICovXG4gICAgZnVuY3Rpb24gcG9wdWxhdGUoc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEpIHtcbiAgICAgIGxvYWRlZCA9IHt9O1xuICAgICAgY29uc3QgcGx1Z2luRGVmYXVsdHMgPSBPYmplY3Qua2V5cyhyZWdpc3RyeS5wbHVnaW5zKVxuICAgICAgICAubWFwKHBsdWdpbiA9PiB7XG4gICAgICAgICAgY29uc3QgbWVudXMgPVxuICAgICAgICAgICAgcmVnaXN0cnkucGx1Z2luc1twbHVnaW5dIS5zY2hlbWFbJ2p1cHl0ZXIubGFiLm1lbnVzJ10/Lm1haW4gPz8gW107XG4gICAgICAgICAgbG9hZGVkW3BsdWdpbl0gPSBtZW51cztcbiAgICAgICAgICByZXR1cm4gbWVudXM7XG4gICAgICAgIH0pXG4gICAgICAgIC5jb25jYXQoW3NjaGVtYVsnanVweXRlci5sYWIubWVudXMnXT8ubWFpbiA/PyBbXV0pXG4gICAgICAgIC5yZWR1Y2VSaWdodChcbiAgICAgICAgICAoYWNjLCB2YWwpID0+IFNldHRpbmdSZWdpc3RyeS5yZWNvbmNpbGVNZW51cyhhY2MsIHZhbCwgdHJ1ZSksXG4gICAgICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLm1lbnVzLmRlZmF1bHQgYXMgYW55W11cbiAgICAgICAgKTtcblxuICAgICAgLy8gQXBwbHkgZGVmYXVsdCB2YWx1ZSBhcyBsYXN0IHN0ZXAgdG8gdGFrZSBpbnRvIGFjY291bnQgb3ZlcnJpZGVzLmpzb25cbiAgICAgIC8vIFRoZSBzdGFuZGFyZCBkZWZhdWx0IGJlaW5nIFtdIGFzIHRoZSBwbHVnaW4gbXVzdCB1c2UgYGp1cHl0ZXIubGFiLm1lbnVzLm1haW5gXG4gICAgICAvLyB0byBkZWZpbmUgdGhlaXIgZGVmYXVsdCB2YWx1ZS5cbiAgICAgIHNjaGVtYS5wcm9wZXJ0aWVzIS5tZW51cy5kZWZhdWx0ID0gU2V0dGluZ1JlZ2lzdHJ5LnJlY29uY2lsZU1lbnVzKFxuICAgICAgICBwbHVnaW5EZWZhdWx0cyxcbiAgICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLm1lbnVzLmRlZmF1bHQgYXMgYW55W10sXG4gICAgICAgIHRydWVcbiAgICAgIClcbiAgICAgICAgLy8gZmxhdHRlbiBvbmUgbGV2ZWxcbiAgICAgICAgLnNvcnQoKGEsIGIpID0+IChhLnJhbmsgPz8gSW5maW5pdHkpIC0gKGIucmFuayA/PyBJbmZpbml0eSkpO1xuICAgIH1cblxuICAgIC8vIFRyYW5zZm9ybSB0aGUgcGx1Z2luIG9iamVjdCB0byByZXR1cm4gZGlmZmVyZW50IHNjaGVtYSB0aGFuIHRoZSBkZWZhdWx0LlxuICAgIHJlZ2lzdHJ5LnRyYW5zZm9ybShQTFVHSU5fSUQsIHtcbiAgICAgIGNvbXBvc2U6IHBsdWdpbiA9PiB7XG4gICAgICAgIC8vIE9ubHkgb3ZlcnJpZGUgdGhlIGNhbm9uaWNhbCBzY2hlbWEgdGhlIGZpcnN0IHRpbWUuXG4gICAgICAgIGlmICghY2Fub25pY2FsKSB7XG4gICAgICAgICAgY2Fub25pY2FsID0gSlNPTkV4dC5kZWVwQ29weShwbHVnaW4uc2NoZW1hKTtcbiAgICAgICAgICBwb3B1bGF0ZShjYW5vbmljYWwpO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgZGVmYXVsdHMgPSBjYW5vbmljYWwucHJvcGVydGllcz8ubWVudXM/LmRlZmF1bHQgPz8gW107XG4gICAgICAgIGNvbnN0IHVzZXIgPSB7XG4gICAgICAgICAgLi4ucGx1Z2luLmRhdGEudXNlcixcbiAgICAgICAgICBtZW51czogcGx1Z2luLmRhdGEudXNlci5tZW51cyA/PyBbXVxuICAgICAgICB9O1xuICAgICAgICBjb25zdCBjb21wb3NpdGUgPSB7XG4gICAgICAgICAgLi4ucGx1Z2luLmRhdGEuY29tcG9zaXRlLFxuICAgICAgICAgIG1lbnVzOiBTZXR0aW5nUmVnaXN0cnkucmVjb25jaWxlTWVudXMoXG4gICAgICAgICAgICBkZWZhdWx0cyBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51W10sXG4gICAgICAgICAgICB1c2VyLm1lbnVzIGFzIElTZXR0aW5nUmVnaXN0cnkuSU1lbnVbXVxuICAgICAgICAgIClcbiAgICAgICAgfTtcblxuICAgICAgICBwbHVnaW4uZGF0YSA9IHsgY29tcG9zaXRlLCB1c2VyIH07XG5cbiAgICAgICAgcmV0dXJuIHBsdWdpbjtcbiAgICAgIH0sXG4gICAgICBmZXRjaDogcGx1Z2luID0+IHtcbiAgICAgICAgLy8gT25seSBvdmVycmlkZSB0aGUgY2Fub25pY2FsIHNjaGVtYSB0aGUgZmlyc3QgdGltZS5cbiAgICAgICAgaWYgKCFjYW5vbmljYWwpIHtcbiAgICAgICAgICBjYW5vbmljYWwgPSBKU09ORXh0LmRlZXBDb3B5KHBsdWdpbi5zY2hlbWEpO1xuICAgICAgICAgIHBvcHVsYXRlKGNhbm9uaWNhbCk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIGRhdGE6IHBsdWdpbi5kYXRhLFxuICAgICAgICAgIGlkOiBwbHVnaW4uaWQsXG4gICAgICAgICAgcmF3OiBwbHVnaW4ucmF3LFxuICAgICAgICAgIHNjaGVtYTogY2Fub25pY2FsLFxuICAgICAgICAgIHZlcnNpb246IHBsdWdpbi52ZXJzaW9uXG4gICAgICAgIH07XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBSZXBvcHVsYXRlIHRoZSBjYW5vbmljYWwgdmFyaWFibGUgYWZ0ZXIgdGhlIHNldHRpbmcgcmVnaXN0cnkgaGFzXG4gICAgLy8gcHJlbG9hZGVkIGFsbCBpbml0aWFsIHBsdWdpbnMuXG4gICAgY29uc3Qgc2V0dGluZ3MgPSBhd2FpdCByZWdpc3RyeS5sb2FkKFBMVUdJTl9JRCk7XG5cbiAgICBjb25zdCBjdXJyZW50TWVudXM6IElTZXR0aW5nUmVnaXN0cnkuSU1lbnVbXSA9XG4gICAgICBKU09ORXh0LmRlZXBDb3B5KHNldHRpbmdzLmNvbXBvc2l0ZS5tZW51cyBhcyBhbnkpID8/IFtdO1xuICAgIGNvbnN0IG1lbnVzID0gbmV3IEFycmF5PE1lbnU+KCk7XG4gICAgLy8gQ3JlYXRlIG1lbnUgZm9yIG5vbi1kaXNhYmxlZCBlbGVtZW50XG4gICAgTWVudUZhY3RvcnkuY3JlYXRlTWVudXMoXG4gICAgICBjdXJyZW50TWVudXNcbiAgICAgICAgLmZpbHRlcihtZW51ID0+ICFtZW51LmRpc2FibGVkKVxuICAgICAgICAubWFwKG1lbnUgPT4ge1xuICAgICAgICAgIHJldHVybiB7XG4gICAgICAgICAgICAuLi5tZW51LFxuICAgICAgICAgICAgaXRlbXM6IFNldHRpbmdSZWdpc3RyeS5maWx0ZXJEaXNhYmxlZEl0ZW1zKG1lbnUuaXRlbXMgPz8gW10pXG4gICAgICAgICAgfTtcbiAgICAgICAgfSksXG4gICAgICBtZW51RmFjdG9yeVxuICAgICkuZm9yRWFjaChtZW51ID0+IHtcbiAgICAgIG1lbnVzLnB1c2gobWVudSk7XG4gICAgICBhZGRNZW51KG1lbnUpO1xuICAgIH0pO1xuXG4gICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIC8vIEFzIGV4dGVuc2lvbiBtYXkgY2hhbmdlIG1lbnUgdGhyb3VnaCBBUEksIHByb21wdCB0aGUgdXNlciB0byByZWxvYWQgaWYgdGhlXG4gICAgICAvLyBtZW51IGhhcyBiZWVuIHVwZGF0ZWQuXG4gICAgICBjb25zdCBuZXdNZW51cyA9IChzZXR0aW5ncy5jb21wb3NpdGUubWVudXMgYXMgYW55KSA/PyBbXTtcbiAgICAgIGlmICghSlNPTkV4dC5kZWVwRXF1YWwoY3VycmVudE1lbnVzLCBuZXdNZW51cykpIHtcbiAgICAgICAgdm9pZCBkaXNwbGF5SW5mb3JtYXRpb24odHJhbnMpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgcmVnaXN0cnkucGx1Z2luQ2hhbmdlZC5jb25uZWN0KGFzeW5jIChzZW5kZXIsIHBsdWdpbikgPT4ge1xuICAgICAgaWYgKHBsdWdpbiAhPT0gUExVR0lOX0lEKSB7XG4gICAgICAgIC8vIElmIHRoZSBwbHVnaW4gY2hhbmdlZCBpdHMgbWVudS5cbiAgICAgICAgY29uc3Qgb2xkTWVudXMgPSBsb2FkZWRbcGx1Z2luXSA/PyBbXTtcbiAgICAgICAgY29uc3QgbmV3TWVudXMgPVxuICAgICAgICAgIHJlZ2lzdHJ5LnBsdWdpbnNbcGx1Z2luXSEuc2NoZW1hWydqdXB5dGVyLmxhYi5tZW51cyddPy5tYWluID8/IFtdO1xuICAgICAgICBpZiAoIUpTT05FeHQuZGVlcEVxdWFsKG9sZE1lbnVzLCBuZXdNZW51cykpIHtcbiAgICAgICAgICBpZiAobG9hZGVkW3BsdWdpbl0pIHtcbiAgICAgICAgICAgIC8vIFRoZSBwbHVnaW4gaGFzIGNoYW5nZWQsIHJlcXVlc3QgdGhlIHVzZXIgdG8gcmVsb2FkIHRoZSBVSSAtIHRoaXMgc2hvdWxkIG5vdCBoYXBwZW5cbiAgICAgICAgICAgIGF3YWl0IGRpc3BsYXlJbmZvcm1hdGlvbih0cmFucyk7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIC8vIFRoZSBwbHVnaW4gd2FzIG5vdCB5ZXQgbG9hZGVkIHdoZW4gdGhlIG1lbnUgd2FzIGJ1aWx0ID0+IHVwZGF0ZSB0aGUgbWVudVxuICAgICAgICAgICAgbG9hZGVkW3BsdWdpbl0gPSBKU09ORXh0LmRlZXBDb3B5KG5ld01lbnVzKTtcbiAgICAgICAgICAgIC8vIE1lcmdlIHBvdGVudGlhbCBkaXNhYmxlZCBzdGF0ZVxuICAgICAgICAgICAgY29uc3QgdG9BZGQgPSBTZXR0aW5nUmVnaXN0cnkucmVjb25jaWxlTWVudXMoXG4gICAgICAgICAgICAgIG5ld01lbnVzLFxuICAgICAgICAgICAgICBjdXJyZW50TWVudXMsXG4gICAgICAgICAgICAgIGZhbHNlLFxuICAgICAgICAgICAgICBmYWxzZVxuICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAuZmlsdGVyKG1lbnUgPT4gIW1lbnUuZGlzYWJsZWQpXG4gICAgICAgICAgICAgIC5tYXAobWVudSA9PiB7XG4gICAgICAgICAgICAgICAgcmV0dXJuIHtcbiAgICAgICAgICAgICAgICAgIC4uLm1lbnUsXG4gICAgICAgICAgICAgICAgICBpdGVtczogU2V0dGluZ1JlZ2lzdHJ5LmZpbHRlckRpc2FibGVkSXRlbXMobWVudS5pdGVtcyA/PyBbXSlcbiAgICAgICAgICAgICAgICB9O1xuICAgICAgICAgICAgICB9KTtcblxuICAgICAgICAgICAgTWVudUZhY3RvcnkudXBkYXRlTWVudXMobWVudXMsIHRvQWRkLCBtZW51RmFjdG9yeSkuZm9yRWFjaChtZW51ID0+IHtcbiAgICAgICAgICAgICAgYWRkTWVudShtZW51KTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=