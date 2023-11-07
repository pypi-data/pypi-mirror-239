"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_filebrowser-extension_lib_index_js"],{

/***/ "../packages/filebrowser-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/filebrowser-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "fileUploadStatus": () => (/* binding */ fileUploadStatus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_11__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module filebrowser-extension
 */












const FILE_BROWSER_FACTORY = 'FileBrowser';
const FILE_BROWSER_PLUGIN_ID = '@jupyterlab/filebrowser-extension:browser';
/**
 * The class name added to the filebrowser filterbox node.
 */
const FILTERBOX_CLASS = 'jp-FileBrowser-filterBox';
/**
 * The command IDs used by the file browser plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.copy = 'filebrowser:copy';
    CommandIDs.copyDownloadLink = 'filebrowser:copy-download-link';
    CommandIDs.cut = 'filebrowser:cut';
    CommandIDs.del = 'filebrowser:delete';
    CommandIDs.download = 'filebrowser:download';
    CommandIDs.duplicate = 'filebrowser:duplicate';
    // For main browser only.
    CommandIDs.hideBrowser = 'filebrowser:hide-main';
    CommandIDs.goToPath = 'filebrowser:go-to-path';
    CommandIDs.goUp = 'filebrowser:go-up';
    CommandIDs.openPath = 'filebrowser:open-path';
    CommandIDs.openUrl = 'filebrowser:open-url';
    CommandIDs.open = 'filebrowser:open';
    CommandIDs.openBrowserTab = 'filebrowser:open-browser-tab';
    CommandIDs.paste = 'filebrowser:paste';
    CommandIDs.createNewDirectory = 'filebrowser:create-new-directory';
    CommandIDs.createNewFile = 'filebrowser:create-new-file';
    CommandIDs.createNewMarkdownFile = 'filebrowser:create-new-markdown-file';
    CommandIDs.refresh = 'filebrowser:refresh';
    CommandIDs.rename = 'filebrowser:rename';
    // For main browser only.
    CommandIDs.copyShareableLink = 'filebrowser:share-main';
    // For main browser only.
    CommandIDs.copyPath = 'filebrowser:copy-path';
    CommandIDs.showBrowser = 'filebrowser:activate';
    CommandIDs.shutdown = 'filebrowser:shutdown';
    // For main browser only.
    CommandIDs.toggleBrowser = 'filebrowser:toggle-main';
    CommandIDs.toggleNavigateToCurrentDirectory = 'filebrowser:toggle-navigate-to-current-directory';
    CommandIDs.toggleLastModified = 'filebrowser:toggle-last-modified';
    CommandIDs.toggleFileSize = 'filebrowser:toggle-file-size';
    CommandIDs.toggleSortNotebooksFirst = 'filebrowser:toggle-sort-notebooks-first';
    CommandIDs.search = 'filebrowser:search';
    CommandIDs.toggleHiddenFiles = 'filebrowser:toggle-hidden-files';
    CommandIDs.toggleFileCheckboxes = 'filebrowser:toggle-file-checkboxes';
})(CommandIDs || (CommandIDs = {}));
/**
 * The file browser namespace token.
 */
const namespace = 'filebrowser';
/**
 * The default file browser extension.
 */
const browser = {
    id: FILE_BROWSER_PLUGIN_ID,
    description: 'Set up the default file browser (commands, settings,...).',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IDefaultFileBrowser, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ITreePathUpdater,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette
    ],
    provides: _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserCommands,
    autoStart: true,
    activate: async (app, defaultFileBrowser, factory, translator, restorer, settingRegistry, treePathUpdater, commandPalette) => {
        const browser = defaultFileBrowser;
        // Let the application restorer track the primary file browser (that is
        // automatically created) for restoration of application state (e.g. setting
        // the file browser as the current side bar widget).
        //
        // All other file browsers created by using the factory function are
        // responsible for their own restoration behavior, if any.
        if (restorer) {
            restorer.add(browser, namespace);
        }
        // Navigate to preferred-dir trait if found
        const preferredPath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('preferredPath');
        if (preferredPath) {
            await browser.model.cd(preferredPath);
        }
        addCommands(app, browser, factory, translator, settingRegistry, commandPalette);
        return void Promise.all([app.restored, browser.model.restored]).then(() => {
            if (treePathUpdater) {
                browser.model.pathChanged.connect((sender, args) => {
                    treePathUpdater(args.newValue);
                });
            }
            if (settingRegistry) {
                void settingRegistry.load(FILE_BROWSER_PLUGIN_ID).then(settings => {
                    /**
                     * File browser configuration.
                     */
                    const fileBrowserConfig = {
                        navigateToCurrentDirectory: false,
                        showLastModifiedColumn: true,
                        showFileSizeColumn: false,
                        showHiddenFiles: false,
                        showFileCheckboxes: false,
                        sortNotebooksFirst: false
                    };
                    const fileBrowserModelConfig = {
                        filterDirectories: true
                    };
                    function onSettingsChanged(settings) {
                        let key;
                        for (key in fileBrowserConfig) {
                            const value = settings.get(key).composite;
                            fileBrowserConfig[key] = value;
                            browser[key] = value;
                        }
                        const value = settings.get('filterDirectories')
                            .composite;
                        fileBrowserModelConfig.filterDirectories = value;
                        browser.model.filterDirectories = value;
                    }
                    settings.changed.connect(onSettingsChanged);
                    onSettingsChanged(settings);
                });
            }
        });
    }
};
/**
 * The default file browser factory provider.
 */
const factory = {
    id: '@jupyterlab/filebrowser-extension:factory',
    description: 'Provides the file browser factory.',
    provides: _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_6__.IStateDB, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab.IInfo],
    activate: async (app, docManager, translator, state, info) => {
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({ namespace });
        const createFileBrowser = (id, options = {}) => {
            var _a;
            const model = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.FilterFileBrowserModel({
                translator: translator,
                auto: (_a = options.auto) !== null && _a !== void 0 ? _a : true,
                manager: docManager,
                driveName: options.driveName || '',
                refreshInterval: options.refreshInterval,
                refreshStandby: () => {
                    if (info) {
                        return !info.isConnected || 'when-hidden';
                    }
                    return 'when-hidden';
                },
                state: options.state === null
                    ? undefined
                    : options.state || state || undefined
            });
            const restore = options.restore;
            const widget = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.FileBrowser({ id, model, restore, translator });
            // Track the newly created file browser.
            void tracker.add(widget);
            return widget;
        };
        return { createFileBrowser, tracker };
    }
};
/**
 * The default file browser factory provider.
 */
const defaultFileBrowser = {
    id: '@jupyterlab/filebrowser-extension:default-file-browser',
    description: 'Provides the default file browser',
    provides: _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IDefaultFileBrowser,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.ITreeResolver, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: async (app, fileBrowserFactory, router, tree, labShell) => {
        const { commands } = app;
        // Manually restore and load the default file browser.
        const defaultBrowser = fileBrowserFactory.createFileBrowser('filebrowser', {
            auto: false,
            restore: false
        });
        void Private.restoreBrowser(defaultBrowser, commands, router, tree, app, labShell);
        return defaultBrowser;
    }
};
/**
 * A plugin providing download + copy download link commands in the context menu.
 *
 * Disabling this plugin will NOT disable downloading files from the server.
 * Users will still be able to retrieve files from the file download URLs the
 * server provides.
 */
const downloadPlugin = {
    id: '@jupyterlab/filebrowser-extension:download',
    description: 'Adds the download file commands. Disabling this plugin will NOT disable downloading files from the server, if the user enters the appropriate download URLs.',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    autoStart: true,
    activate: (app, factory, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        const { tracker } = factory;
        commands.addCommand(CommandIDs.download, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (widget) {
                    return widget.download();
                }
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.downloadIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Download')
        });
        commands.addCommand(CommandIDs.copyDownloadLink, {
            execute: () => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                return widget.model.manager.services.contents
                    .getDownloadUrl(widget.selectedItems().next().value.path)
                    .then(url => {
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(url);
                });
            },
            isVisible: () => 
            // So long as this command only handles one file at time, don't show it
            // if multiple files are selected.
            !!tracker.currentWidget &&
                Array.from(tracker.currentWidget.selectedItems()).length === 1,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Copy Download Link'),
            mnemonic: 0
        });
    }
};
/**
 * A plugin to add the file browser widget to an ILabShell
 */
const browserWidget = {
    id: '@jupyterlab/filebrowser-extension:widget',
    description: 'Adds the file browser to the application shell.',
    requires: [
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IDefaultFileBrowser,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserCommands
    ],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true,
    activate: (app, docManager, browser, factory, settingRegistry, toolbarRegistry, translator, labShell, 
    // Wait until file browser commands are ready before activating file browser widget
    fileBrowserCommands, commandPalette) => {
        const { commands } = app;
        const { tracker } = factory;
        const trans = translator.load('jupyterlab');
        // Set attributes when adding the browser to the UI
        browser.node.setAttribute('role', 'region');
        browser.node.setAttribute('aria-label', trans.__('File Browser Section'));
        browser.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.folderIcon;
        // Show the current file browser shortcut in its title.
        const updateBrowserTitle = () => {
            const binding = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.find)(app.commands.keyBindings, b => b.command === CommandIDs.toggleBrowser);
            if (binding) {
                const ks = binding.keys.map(_lumino_commands__WEBPACK_IMPORTED_MODULE_11__.CommandRegistry.formatKeystroke).join(', ');
                browser.title.caption = trans.__('File Browser (%1)', ks);
            }
            else {
                browser.title.caption = trans.__('File Browser');
            }
        };
        updateBrowserTitle();
        app.commands.keyBindingChanged.connect(() => {
            updateBrowserTitle();
        });
        // Toolbar
        toolbarRegistry.addFactory(FILE_BROWSER_FACTORY, 'uploader', (browser) => new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.Uploader({ model: browser.model, translator }));
        toolbarRegistry.addFactory(FILE_BROWSER_FACTORY, 'fileNameSearcher', (browser) => {
            const searcher = (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.FilenameSearcher)({
                updateFilter: (filterFn, query) => {
                    browser.model.setFilter(value => {
                        return filterFn(value.name.toLowerCase());
                    });
                },
                useFuzzyFilter: true,
                placeholder: trans.__('Filter files by name'),
                forceRefresh: true
            });
            searcher.addClass(FILTERBOX_CLASS);
            return searcher;
        });
        (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.setToolbar)(browser, (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, FILE_BROWSER_FACTORY, browserWidget.id, translator));
        labShell.add(browser, 'left', { rank: 100, type: 'File Browser' });
        commands.addCommand(CommandIDs.toggleBrowser, {
            label: trans.__('File Browser'),
            execute: () => {
                if (browser.isHidden) {
                    return commands.execute(CommandIDs.showBrowser, void 0);
                }
                return commands.execute(CommandIDs.hideBrowser, void 0);
            }
        });
        commands.addCommand(CommandIDs.showBrowser, {
            label: trans.__('Open the file browser for the provided `path`.'),
            execute: args => {
                const path = args.path || '';
                const browserForPath = Private.getBrowserForPath(path, browser, factory);
                // Check for browser not found
                if (!browserForPath) {
                    return;
                }
                // Shortcut if we are using the main file browser
                if (browser === browserForPath) {
                    labShell.activateById(browser.id);
                    return;
                }
                else {
                    const areas = ['left', 'right'];
                    for (const area of areas) {
                        for (const widget of labShell.widgets(area)) {
                            if (widget.contains(browserForPath)) {
                                labShell.activateById(widget.id);
                                return;
                            }
                        }
                    }
                }
            }
        });
        commands.addCommand(CommandIDs.hideBrowser, {
            label: trans.__('Hide the file browser.'),
            execute: () => {
                const widget = tracker.currentWidget;
                if (widget && !widget.isHidden) {
                    labShell.collapseLeft();
                }
            }
        });
        commands.addCommand(CommandIDs.toggleNavigateToCurrentDirectory, {
            label: trans.__('Show Active File in File Browser'),
            isToggled: () => browser.navigateToCurrentDirectory,
            execute: () => {
                const value = !browser.navigateToCurrentDirectory;
                const key = 'navigateToCurrentDirectory';
                return settingRegistry
                    .set(FILE_BROWSER_PLUGIN_ID, key, value)
                    .catch((reason) => {
                    console.error(`Failed to set navigateToCurrentDirectory setting`);
                });
            }
        });
        if (commandPalette) {
            commandPalette.addItem({
                command: CommandIDs.toggleNavigateToCurrentDirectory,
                category: trans.__('File Operations')
            });
        }
        // If the layout is a fresh session without saved data and not in single document
        // mode, open file browser.
        void labShell.restored.then(layout => {
            if (layout.fresh && labShell.mode !== 'single-document') {
                void commands.execute(CommandIDs.showBrowser, void 0);
            }
        });
        void Promise.all([app.restored, browser.model.restored]).then(() => {
            // Whether to automatically navigate to a document's current directory
            labShell.currentChanged.connect(async (_, change) => {
                if (browser.navigateToCurrentDirectory && change.newValue) {
                    const { newValue } = change;
                    const context = docManager.contextForWidget(newValue);
                    if (context) {
                        const { path } = context;
                        try {
                            await Private.navigateToPath(path, browser, factory, translator);
                        }
                        catch (reason) {
                            console.warn(`${CommandIDs.goToPath} failed to open: ${path}`, reason);
                        }
                    }
                }
            });
        });
    }
};
/**
 * The default file browser share-file plugin
 *
 * This extension adds a "Copy Shareable Link" command that generates a copy-
 * pastable URL. This url can be used to open a particular file in JupyterLab,
 * handy for emailing links or bookmarking for reference.
 *
 * If you need to change how this link is generated (for instance, to copy a
 * /user-redirect URL for JupyterHub), disable this plugin and replace it
 * with another implementation.
 */
const shareFile = {
    id: '@jupyterlab/filebrowser-extension:share-file',
    description: 'Adds the "Copy Shareable Link" command; useful for JupyterHub deployment for example.',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    autoStart: true,
    activate: (app, factory, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        const { tracker } = factory;
        commands.addCommand(CommandIDs.copyShareableLink, {
            execute: () => {
                const widget = tracker.currentWidget;
                const model = widget === null || widget === void 0 ? void 0 : widget.selectedItems().next();
                if (model === undefined || model.done) {
                    return;
                }
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({
                    workspace: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.defaultWorkspace,
                    treePath: model.value.path,
                    toShare: true
                }));
            },
            isVisible: () => !!tracker.currentWidget &&
                Array.from(tracker.currentWidget.selectedItems()).length === 1,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.linkIcon.bindprops({ stylesheet: 'menuItem' }),
            label: trans.__('Copy Shareable Link')
        });
    }
};
/**
 * The "Open With" context menu.
 *
 * This is its own plugin in case you would like to disable this feature.
 * e.g. jupyter labextension disable @jupyterlab/filebrowser-extension:open-with
 */
const openWithPlugin = {
    id: '@jupyterlab/filebrowser-extension:open-with',
    description: 'Adds the open-with feature allowing an user to pick the non-preferred document viewer.',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory],
    autoStart: true,
    activate: (app, factory) => {
        const { docRegistry } = app;
        const { tracker } = factory;
        let items = [];
        function updateOpenWithMenu(contextMenu) {
            var _a, _b;
            const openWith = (_b = (_a = contextMenu.menu.items.find(item => {
                var _a;
                return item.type === 'submenu' &&
                    ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-contextmenu-open-with';
            })) === null || _a === void 0 ? void 0 : _a.submenu) !== null && _b !== void 0 ? _b : null;
            if (!openWith) {
                return; // Bail early if the open with menu is not displayed
            }
            // clear the current menu items
            items.forEach(item => item.dispose());
            items.length = 0;
            // Ensure that the menu is empty
            openWith.clearItems();
            // get the widget factories that could be used to open all of the items
            // in the current filebrowser selection
            const factories = tracker.currentWidget
                ? Private.OpenWith.intersection((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.map)(tracker.currentWidget.selectedItems(), i => {
                    return Private.OpenWith.getFactories(docRegistry, i);
                }))
                : new Set();
            // make new menu items from the widget factories
            items = [...factories].map(factory => openWith.addItem({
                args: { factory: factory.name, label: factory.label || factory.name },
                command: CommandIDs.open
            }));
        }
        app.contextMenu.opened.connect(updateOpenWithMenu);
    }
};
/**
 * The "Open in New Browser Tab" context menu.
 *
 * This is its own plugin in case you would like to disable this feature.
 * e.g. jupyter labextension disable @jupyterlab/filebrowser-extension:open-browser-tab
 *
 * Note: If disabling this, you may also want to disable:
 * @jupyterlab/docmanager-extension:open-browser-tab
 */
const openBrowserTabPlugin = {
    id: '@jupyterlab/filebrowser-extension:open-browser-tab',
    description: 'Adds the open-in-new-browser-tab features.',
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    autoStart: true,
    activate: (app, factory, translator) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const { tracker } = factory;
        commands.addCommand(CommandIDs.openBrowserTab, {
            execute: args => {
                const widget = tracker.currentWidget;
                if (!widget) {
                    return;
                }
                const mode = args['mode'];
                return Promise.all(Array.from((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.map)(widget.selectedItems(), item => {
                    if (mode === 'single-document') {
                        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getUrl({
                            mode: 'single-document',
                            treePath: item.path
                        });
                        const opened = window.open();
                        if (opened) {
                            opened.opener = null;
                            opened.location.href = url;
                        }
                        else {
                            throw new Error('Failed to open new browser tab.');
                        }
                    }
                    else {
                        return commands.execute('docmanager:open-browser-tab', {
                            path: item.path
                        });
                    }
                })));
            },
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.addIcon.bindprops({ stylesheet: 'menuItem' }),
            label: args => args['mode'] === 'single-document'
                ? trans.__('Open in Simple Mode')
                : trans.__('Open in New Browser Tab'),
            mnemonic: 0
        });
    }
};
/**
 * A plugin providing file upload status.
 */
const fileUploadStatus = {
    id: '@jupyterlab/filebrowser-extension:file-upload-status',
    description: 'Adds a file upload status widget.',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IFileBrowserFactory, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_7__.IStatusBar],
    activate: (app, browser, translator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const item = new _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.FileUploadStatus({
            tracker: browser.tracker,
            translator
        });
        statusBar.registerStatusItem('@jupyterlab/filebrowser-extension:file-upload-status', {
            item,
            align: 'middle',
            isActive: () => {
                return !!item.model && item.model.items.length > 0;
            },
            activeStateChanged: item.model.stateChanged
        });
    }
};
/**
 * A plugin to open files from remote URLs
 */
const openUrlPlugin = {
    id: '@jupyterlab/filebrowser-extension:open-url',
    description: 'Adds the feature "Open files from remote URLs".',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_4__.IDefaultFileBrowser, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, browser, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const command = CommandIDs.openUrl;
        commands.addCommand(command, {
            label: args => args.url ? trans.__('Open %1', args.url) : trans.__('Open from URL…'),
            caption: args => args.url ? trans.__('Open %1', args.url) : trans.__('Open from URL'),
            execute: async (args) => {
                var _a, _b, _c;
                let url = (_a = args === null || args === void 0 ? void 0 : args.url) !== null && _a !== void 0 ? _a : '';
                if (!url) {
                    url =
                        (_b = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({
                            label: trans.__('URL'),
                            placeholder: 'https://example.com/path/to/file',
                            title: trans.__('Open URL'),
                            okLabel: trans.__('Open')
                        })).value) !== null && _b !== void 0 ? _b : undefined;
                }
                if (!url) {
                    return;
                }
                let type = '';
                let blob;
                // fetch the file from the URL
                try {
                    const req = await fetch(url);
                    blob = await req.blob();
                    type = (_c = req.headers.get('Content-Type')) !== null && _c !== void 0 ? _c : '';
                }
                catch (reason) {
                    if (reason.response && reason.response.status !== 200) {
                        reason.message = trans.__('Could not open URL: %1', url);
                    }
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Cannot fetch'), reason);
                }
                // upload the content of the file to the server
                try {
                    const name = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.basename(url);
                    const file = new File([blob], name, { type });
                    const model = await browser.model.upload(file);
                    return commands.execute('docmanager:open', {
                        path: model.path
                    });
                }
                catch (error) {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans._p('showErrorMessage', 'Upload Error'), error);
                }
            }
        });
        if (palette) {
            palette.addItem({
                command,
                category: trans.__('File Operations')
            });
        }
    }
};
/**
 * Add the main file browser commands to the application's command registry.
 */
function addCommands(app, browser, factory, translator, settingRegistry, commandPalette) {
    const trans = translator.load('jupyterlab');
    const { docRegistry: registry, commands } = app;
    const { tracker } = factory;
    commands.addCommand(CommandIDs.del, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.delete();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.closeIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Delete'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.copy, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.copy();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Copy'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.cut, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.cut();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.cutIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Cut')
    });
    commands.addCommand(CommandIDs.duplicate, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.duplicate();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.copyIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Duplicate')
    });
    commands.addCommand(CommandIDs.goToPath, {
        label: trans.__('Update the file browser to display the provided `path`.'),
        execute: async (args) => {
            var _a;
            const path = args.path || '';
            const showBrowser = !((_a = args === null || args === void 0 ? void 0 : args.dontShowBrowser) !== null && _a !== void 0 ? _a : false);
            try {
                const item = await Private.navigateToPath(path, browser, factory, translator);
                if (item.type !== 'directory' && showBrowser) {
                    const browserForPath = Private.getBrowserForPath(path, browser, factory);
                    if (browserForPath) {
                        browserForPath.clearSelectedItems();
                        const parts = path.split('/');
                        const name = parts[parts.length - 1];
                        if (name) {
                            await browserForPath.selectItemByName(name);
                        }
                    }
                }
            }
            catch (reason) {
                console.warn(`${CommandIDs.goToPath} failed to go to: ${path}`, reason);
            }
            if (showBrowser) {
                return commands.execute(CommandIDs.showBrowser, { path });
            }
        }
    });
    commands.addCommand(CommandIDs.goUp, {
        label: 'go up',
        execute: async () => {
            const browserForPath = Private.getBrowserForPath('', browser, factory);
            if (!browserForPath) {
                return;
            }
            const { model } = browserForPath;
            await model.restored;
            void browserForPath.goUp();
        }
    });
    commands.addCommand(CommandIDs.openPath, {
        label: args => args.path ? trans.__('Open %1', args.path) : trans.__('Open from Path…'),
        caption: args => args.path ? trans.__('Open %1', args.path) : trans.__('Open from path'),
        execute: async (args) => {
            var _a;
            let path;
            if (args === null || args === void 0 ? void 0 : args.path) {
                path = args.path;
            }
            else {
                path =
                    (_a = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({
                        label: trans.__('Path'),
                        placeholder: '/path/relative/to/jlab/root',
                        title: trans.__('Open Path'),
                        okLabel: trans.__('Open')
                    })).value) !== null && _a !== void 0 ? _a : undefined;
            }
            if (!path) {
                return;
            }
            try {
                const trailingSlash = path !== '/' && path.endsWith('/');
                if (trailingSlash) {
                    // The normal contents service errors on paths ending in slash
                    path = path.slice(0, path.length - 1);
                }
                const browserForPath = Private.getBrowserForPath(path, browser, factory);
                const { services } = browserForPath.model.manager;
                const item = await services.contents.get(path, {
                    content: false
                });
                if (trailingSlash && item.type !== 'directory') {
                    throw new Error(`Path ${path}/ is not a directory`);
                }
                await commands.execute(CommandIDs.goToPath, {
                    path,
                    dontShowBrowser: args.dontShowBrowser
                });
                if (item.type === 'directory') {
                    return;
                }
                return commands.execute('docmanager:open', { path });
            }
            catch (reason) {
                if (reason.response && reason.response.status === 404) {
                    reason.message = trans.__('Could not find path: %1', path);
                }
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('Cannot open'), reason);
            }
        }
    });
    // Add the openPath command to the command palette
    if (commandPalette) {
        commandPalette.addItem({
            command: CommandIDs.openPath,
            category: trans.__('File Operations')
        });
    }
    commands.addCommand(CommandIDs.open, {
        execute: args => {
            const factory = args['factory'] || void 0;
            const widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            const { contents } = widget.model.manager.services;
            return Promise.all(Array.from((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_10__.map)(widget.selectedItems(), item => {
                if (item.type === 'directory') {
                    const localPath = contents.localPath(item.path);
                    return widget.model.cd(`/${localPath}`);
                }
                return commands.execute('docmanager:open', {
                    factory: factory,
                    path: item.path
                });
            })));
        },
        icon: args => {
            var _a;
            const factory = args['factory'] || void 0;
            if (factory) {
                // if an explicit factory is passed...
                const ft = registry.getFileType(factory);
                // ...set an icon if the factory name corresponds to a file type name...
                // ...or leave the icon blank
                return (_a = ft === null || ft === void 0 ? void 0 : ft.icon) === null || _a === void 0 ? void 0 : _a.bindprops({ stylesheet: 'menuItem' });
            }
            else {
                return _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.folderIcon.bindprops({ stylesheet: 'menuItem' });
            }
        },
        label: args => (args['label'] || args['factory'] || trans.__('Open')),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.paste, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.paste();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.pasteIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Paste'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.createNewDirectory, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.createNewDirectory();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.newFolderIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('New Folder')
    });
    commands.addCommand(CommandIDs.createNewFile, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.createNewFile({ ext: 'txt' });
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.textEditorIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('New File')
    });
    commands.addCommand(CommandIDs.createNewMarkdownFile, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.createNewFile({ ext: 'md' });
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.markdownIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('New Markdown File')
    });
    commands.addCommand(CommandIDs.refresh, {
        execute: args => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.model.refresh();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.skRefreshIcon.bindprops({ stylesheet: 'menuItem' }),
        caption: trans.__('Refresh the file browser.'),
        label: trans.__('Refresh File List')
    });
    commands.addCommand(CommandIDs.rename, {
        execute: args => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.rename();
            }
        },
        isVisible: () => 
        // So long as this command only handles one file at time, don't show it
        // if multiple files are selected.
        !!tracker.currentWidget &&
            Array.from(tracker.currentWidget.selectedItems()).length === 1,
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.editIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Rename'),
        mnemonic: 0
    });
    commands.addCommand(CommandIDs.copyPath, {
        execute: () => {
            var _a;
            const widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            const item = widget.selectedItems().next();
            if (item.done) {
                return;
            }
            if (_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('copyAbsolutePath') === 'true') {
                const absolutePath = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.join((_a = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('serverRoot')) !== null && _a !== void 0 ? _a : '', item.value.path);
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(absolutePath);
            }
            else {
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Clipboard.copyToSystem(item.value.path);
            }
        },
        isVisible: () => 
        // So long as this command only handles one file at time, don't show it
        // if multiple files are selected.
        !!tracker.currentWidget &&
            Array.from(tracker.currentWidget.selectedItems()).length === 1,
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.fileIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Copy Path')
    });
    commands.addCommand(CommandIDs.shutdown, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (widget) {
                return widget.shutdownKernels();
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_9__.stopIcon.bindprops({ stylesheet: 'menuItem' }),
        label: trans.__('Shut Down Kernel')
    });
    commands.addCommand(CommandIDs.toggleLastModified, {
        label: trans.__('Show Last Modified Column'),
        isToggled: () => browser.showLastModifiedColumn,
        execute: () => {
            const value = !browser.showLastModifiedColumn;
            const key = 'showLastModifiedColumn';
            if (settingRegistry) {
                return settingRegistry
                    .set(FILE_BROWSER_PLUGIN_ID, key, value)
                    .catch((reason) => {
                    console.error(`Failed to set ${key} setting`);
                });
            }
        }
    });
    commands.addCommand(CommandIDs.toggleSortNotebooksFirst, {
        label: trans.__('Sort Notebooks Above Files'),
        isToggled: () => browser.sortNotebooksFirst,
        execute: () => {
            const value = !browser.sortNotebooksFirst;
            const key = 'sortNotebooksFirst';
            if (settingRegistry) {
                return settingRegistry
                    .set(FILE_BROWSER_PLUGIN_ID, key, value)
                    .catch((reason) => {
                    console.error(`Failed to set ${key} setting`);
                });
            }
        }
    });
    commands.addCommand(CommandIDs.toggleFileSize, {
        label: trans.__('Show File Size Column'),
        isToggled: () => browser.showFileSizeColumn,
        execute: () => {
            const value = !browser.showFileSizeColumn;
            const key = 'showFileSizeColumn';
            if (settingRegistry) {
                return settingRegistry
                    .set(FILE_BROWSER_PLUGIN_ID, key, value)
                    .catch((reason) => {
                    console.error(`Failed to set ${key} setting`);
                });
            }
        }
    });
    commands.addCommand(CommandIDs.toggleHiddenFiles, {
        label: trans.__('Show Hidden Files'),
        isToggled: () => browser.showHiddenFiles,
        isVisible: () => _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('allow_hidden_files') === 'true',
        execute: () => {
            const value = !browser.showHiddenFiles;
            const key = 'showHiddenFiles';
            if (settingRegistry) {
                return settingRegistry
                    .set(FILE_BROWSER_PLUGIN_ID, key, value)
                    .catch((reason) => {
                    console.error(`Failed to set showHiddenFiles setting`);
                });
            }
        }
    });
    commands.addCommand(CommandIDs.toggleFileCheckboxes, {
        label: trans.__('Show File Checkboxes'),
        isToggled: () => browser.showFileCheckboxes,
        execute: () => {
            const value = !browser.showFileCheckboxes;
            const key = 'showFileCheckboxes';
            if (settingRegistry) {
                return settingRegistry
                    .set(FILE_BROWSER_PLUGIN_ID, key, value)
                    .catch((reason) => {
                    console.error(`Failed to set showFileCheckboxes setting`);
                });
            }
        }
    });
    commands.addCommand(CommandIDs.search, {
        label: trans.__('Search on File Names'),
        execute: () => alert('search')
    });
}
/**
 * Export the plugins as default.
 */
const plugins = [
    factory,
    defaultFileBrowser,
    browser,
    shareFile,
    fileUploadStatus,
    downloadPlugin,
    browserWidget,
    openWithPlugin,
    openBrowserTabPlugin,
    openUrlPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Get browser object given file path.
     */
    function getBrowserForPath(path, browser, factory) {
        const { tracker } = factory;
        const driveName = browser.model.manager.services.contents.driveName(path);
        if (driveName) {
            const browserForPath = tracker.find(_path => _path.model.driveName === driveName);
            if (!browserForPath) {
                // warn that no filebrowser could be found for this driveName
                console.warn(`${CommandIDs.goToPath} failed to find filebrowser for path: ${path}`);
                return;
            }
            return browserForPath;
        }
        // if driveName is empty, assume the main filebrowser
        return browser;
    }
    Private.getBrowserForPath = getBrowserForPath;
    /**
     * Navigate to a path or the path containing a file.
     */
    async function navigateToPath(path, browser, factory, translator) {
        const trans = translator.load('jupyterlab');
        const browserForPath = Private.getBrowserForPath(path, browser, factory);
        if (!browserForPath) {
            throw new Error(trans.__('No browser for path'));
        }
        const { services } = browserForPath.model.manager;
        const localPath = services.contents.localPath(path);
        await services.ready;
        const item = await services.contents.get(path, { content: false });
        const { model } = browserForPath;
        await model.restored;
        if (item.type === 'directory') {
            await model.cd(`/${localPath}`);
        }
        else {
            await model.cd(`/${_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.dirname(localPath)}`);
        }
        return item;
    }
    Private.navigateToPath = navigateToPath;
    /**
     * Restores file browser state and overrides state if tree resolver resolves.
     */
    async function restoreBrowser(browser, commands, router, tree, app, labShell) {
        const restoring = 'jp-mod-restoring';
        browser.addClass(restoring);
        if (!router) {
            await browser.model.restore(browser.id);
            await browser.model.refresh();
            browser.removeClass(restoring);
            return;
        }
        const listener = async () => {
            router.routed.disconnect(listener);
            const paths = await (tree === null || tree === void 0 ? void 0 : tree.paths);
            if ((paths === null || paths === void 0 ? void 0 : paths.file) || (paths === null || paths === void 0 ? void 0 : paths.browser)) {
                // Restore the model without populating it.
                await browser.model.restore(browser.id, false);
                if (paths.file) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.file,
                        dontShowBrowser: true
                    });
                }
                if (paths.browser) {
                    await commands.execute(CommandIDs.openPath, {
                        path: paths.browser,
                        dontShowBrowser: true
                    });
                }
            }
            else {
                await browser.model.restore(browser.id);
                await browser.model.refresh();
            }
            browser.removeClass(restoring);
            if (labShell === null || labShell === void 0 ? void 0 : labShell.isEmpty('main')) {
                void commands.execute('launcher:create');
            }
        };
        router.routed.connect(listener);
    }
    Private.restoreBrowser = restoreBrowser;
    let OpenWith;
    (function (OpenWith) {
        /**
         * Get the factories for the selected item
         *
         * @param docRegistry Application document registry
         * @param item Selected item model
         * @returns Available factories for the model
         */
        function getFactories(docRegistry, item) {
            const factories = docRegistry.preferredWidgetFactories(item.path);
            const notebookFactory = docRegistry.getWidgetFactory('notebook');
            if (notebookFactory &&
                item.type === 'notebook' &&
                factories.indexOf(notebookFactory) === -1) {
                factories.unshift(notebookFactory);
            }
            return factories;
        }
        OpenWith.getFactories = getFactories;
        /**
         * Return the intersection of multiple iterables.
         *
         * @param iterables Iterator of iterables
         * @returns Set of common elements to all iterables
         */
        function intersection(iterables) {
            let accumulator = undefined;
            for (const current of iterables) {
                // Initialize accumulator.
                if (accumulator === undefined) {
                    accumulator = new Set(current);
                    continue;
                }
                // Return early if empty.
                if (accumulator.size === 0) {
                    return accumulator;
                }
                // Keep the intersection of accumulator and current.
                let intersection = new Set();
                for (const value of current) {
                    if (accumulator.has(value)) {
                        intersection.add(value);
                    }
                }
                accumulator = intersection;
            }
            return accumulator !== null && accumulator !== void 0 ? accumulator : new Set();
        }
        OpenWith.intersection = intersection;
    })(OpenWith = Private.OpenWith || (Private.OpenWith = {}));
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZmlsZWJyb3dzZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy45NmI5NzNjMTIzM2RlYjVlNWZmMi5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBVThCO0FBVUg7QUFDOEI7QUFDRjtBQVV6QjtBQUU4QjtBQUNoQjtBQUNJO0FBQ0c7QUFxQm5CO0FBQ1c7QUFDSztBQUduRCxNQUFNLG9CQUFvQixHQUFHLGFBQWEsQ0FBQztBQUMzQyxNQUFNLHNCQUFzQixHQUFHLDJDQUEyQyxDQUFDO0FBRTNFOztHQUVHO0FBQ0gsTUFBTSxlQUFlLEdBQUcsMEJBQTBCLENBQUM7QUFFbkQ7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FvRW5CO0FBcEVELFdBQVUsVUFBVTtJQUNMLGVBQUksR0FBRyxrQkFBa0IsQ0FBQztJQUUxQiwyQkFBZ0IsR0FBRyxnQ0FBZ0MsQ0FBQztJQUVwRCxjQUFHLEdBQUcsaUJBQWlCLENBQUM7SUFFeEIsY0FBRyxHQUFHLG9CQUFvQixDQUFDO0lBRTNCLG1CQUFRLEdBQUcsc0JBQXNCLENBQUM7SUFFbEMsb0JBQVMsR0FBRyx1QkFBdUIsQ0FBQztJQUVqRCx5QkFBeUI7SUFDWixzQkFBVyxHQUFHLHVCQUF1QixDQUFDO0lBRXRDLG1CQUFRLEdBQUcsd0JBQXdCLENBQUM7SUFFcEMsZUFBSSxHQUFHLG1CQUFtQixDQUFDO0lBRTNCLG1CQUFRLEdBQUcsdUJBQXVCLENBQUM7SUFFbkMsa0JBQU8sR0FBRyxzQkFBc0IsQ0FBQztJQUVqQyxlQUFJLEdBQUcsa0JBQWtCLENBQUM7SUFFMUIseUJBQWMsR0FBRyw4QkFBOEIsQ0FBQztJQUVoRCxnQkFBSyxHQUFHLG1CQUFtQixDQUFDO0lBRTVCLDZCQUFrQixHQUFHLGtDQUFrQyxDQUFDO0lBRXhELHdCQUFhLEdBQUcsNkJBQTZCLENBQUM7SUFFOUMsZ0NBQXFCLEdBQUcsc0NB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TUFBTSxPQUFPLElBQUksU0FBUyxFQUFFO2dCQUMvQiwwQkFBMEI7Z0JBQzFCLElBQUksV0FBVyxLQUFLLFNBQVMsRUFBRTtvQkFDN0IsV0FBVyxHQUFHLElBQUksR0FBRyxDQUFDLE9BQU8sQ0FBQyxDQUFDO29CQUMvQixTQUFTO2lCQUNWO2dCQUNELHlCQUF5QjtnQkFDekIsSUFBSSxXQUFXLENBQUMsSUFBSSxLQUFLLENBQUMsRUFBRTtvQkFDMUIsT0FBTyxXQUFXLENBQUM7aUJBQ3BCO2dCQUNELG9EQUFvRDtnQkFDcEQsSUFBSSxZQUFZLEdBQUcsSUFBSSxHQUFHLEVBQUssQ0FBQztnQkFDaEMsS0FBSyxNQUFNLEtBQUssSUFBSSxPQUFPLEVBQUU7b0JBQzNCLElBQUksV0FBVyxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsRUFBRTt3QkFDMUIsWUFBWSxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsQ0FBQztxQkFDekI7aUJBQ0Y7Z0JBQ0QsV0FBVyxHQUFHLFlBQVksQ0FBQzthQUM1QjtZQUNELE9BQU8sV0FBVyxhQUFYLFdBQVcsY0FBWCxXQUFXLEdBQUksSUFBSSxHQUFHLEVBQUUsQ0FBQztRQUNsQyxDQUFDO1FBdEJlLHFCQUFZLGVBc0IzQjtJQUNILENBQUMsRUF0RGdCLFFBQVEsR0FBUixnQkFBUSxLQUFSLGdCQUFRLFFBc0R4QjtBQUNILENBQUMsRUExS1MsT0FBTyxLQUFQLE9BQU8sUUEwS2hCIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ZpbGVicm93c2VyLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgZmlsZWJyb3dzZXItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBJTGF5b3V0UmVzdG9yZXIsXG4gIElSb3V0ZXIsXG4gIElUcmVlUGF0aFVwZGF0ZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luLFxuICBKdXB5dGVyTGFiXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIENsaXBib2FyZCxcbiAgY3JlYXRlVG9vbGJhckZhY3RvcnksXG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSW5wdXREaWFsb2csXG4gIElUb29sYmFyV2lkZ2V0UmVnaXN0cnksXG4gIHNldFRvb2xiYXIsXG4gIHNob3dFcnJvck1lc3NhZ2UsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgUGFnZUNvbmZpZywgUGF0aEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJRG9jdW1lbnRNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlcic7XG5pbXBvcnQgeyBEb2N1bWVudFJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgRmlsZUJyb3dzZXIsXG4gIEZpbGVVcGxvYWRTdGF0dXMsXG4gIEZpbHRlckZpbGVCcm93c2VyTW9kZWwsXG4gIElEZWZhdWx0RmlsZUJyb3dzZXIsXG4gIElGaWxlQnJvd3NlckNvbW1hbmRzLFxuICBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICBVcGxvYWRlclxufSBmcm9tICdAanVweXRlcmxhYi9maWxlYnJvd3Nlcic7XG5pbXBvcnQgeyBDb250ZW50cyB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVN0YXRlREIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IElTdGF0dXNCYXIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBhZGRJY29uLFxuICBjbG9zZUljb24sXG4gIGNvcHlJY29uLFxuICBjdXRJY29uLFxuICBkb3dubG9hZEljb24sXG4gIGVkaXRJY29uLFxuICBmaWxlSWNvbixcbiAgRmlsZW5hbWVTZWFyY2hlcixcbiAgZm9sZGVySWNvbixcbiAgSURpc3Bvc2FibGVNZW51SXRlbSxcbiAgSVNjb3JlLFxuICBsaW5rSWNvbixcbiAgbWFya2Rvd25JY29uLFxuICBuZXdGb2xkZXJJY29uLFxuICBwYXN0ZUljb24sXG4gIFJhbmtlZE1lbnUsXG4gIHNrUmVmcmVzaEljb24sXG4gIHN0b3BJY29uLFxuICB0ZXh0RWRpdG9ySWNvblxufSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IGZpbmQsIG1hcCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgQ29udGV4dE1lbnUgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG5jb25zdCBGSUxFX0JST1dTRVJfRkFDVE9SWSA9ICdGaWxlQnJvd3Nlcic7XG5jb25zdCBGSUxFX0JST1dTRVJfUExVR0lOX0lEID0gJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpicm93c2VyJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byB0aGUgZmlsZWJyb3dzZXIgZmlsdGVyYm94IG5vZGUuXG4gKi9cbmNvbnN0IEZJTFRFUkJPWF9DTEFTUyA9ICdqcC1GaWxlQnJvd3Nlci1maWx0ZXJCb3gnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBmaWxlIGJyb3dzZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjb3B5ID0gJ2ZpbGVicm93c2VyOmNvcHknO1xuXG4gIGV4cG9ydCBjb25zdCBjb3B5RG93bmxvYWRMaW5rID0gJ2ZpbGVicm93c2VyOmNvcHktZG93bmxvYWQtbGluayc7XG5cbiAgZXhwb3J0IGNvbnN0IGN1dCA9ICdmaWxlYnJvd3NlcjpjdXQnO1xuXG4gIGV4cG9ydCBjb25zdCBkZWwgPSAnZmlsZWJyb3dzZXI6ZGVsZXRlJztcblxuICBleHBvcnQgY29uc3QgZG93bmxvYWQgPSAnZmlsZWJyb3dzZXI6ZG93bmxvYWQnO1xuXG4gIGV4cG9ydCBjb25zdCBkdXBsaWNhdGUgPSAnZmlsZWJyb3dzZXI6ZHVwbGljYXRlJztcblxuICAvLyBGb3IgbWFpbiBicm93c2VyIG9ubHkuXG4gIGV4cG9ydCBjb25zdCBoaWRlQnJvd3NlciA9ICdmaWxlYnJvd3NlcjpoaWRlLW1haW4nO1xuXG4gIGV4cG9ydCBjb25zdCBnb1RvUGF0aCA9ICdmaWxlYnJvd3Nlcjpnby10by1wYXRoJztcblxuICBleHBvcnQgY29uc3QgZ29VcCA9ICdmaWxlYnJvd3Nlcjpnby11cCc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5QYXRoID0gJ2ZpbGVicm93c2VyOm9wZW4tcGF0aCc7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5VcmwgPSAnZmlsZWJyb3dzZXI6b3Blbi11cmwnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuID0gJ2ZpbGVicm93c2VyOm9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuQnJvd3NlclRhYiA9ICdmaWxlYnJvd3NlcjpvcGVuLWJyb3dzZXItdGFiJztcblxuICBleHBvcnQgY29uc3QgcGFzdGUgPSAnZmlsZWJyb3dzZXI6cGFzdGUnO1xuXG4gIGV4cG9ydCBjb25zdCBjcmVhdGVOZXdEaXJlY3RvcnkgPSAnZmlsZWJyb3dzZXI6Y3JlYXRlLW5ldy1kaXJlY3RvcnknO1xuXG4gIGV4cG9ydCBjb25zdCBjcmVhdGVOZXdGaWxlID0gJ2ZpbGVicm93c2VyOmNyZWF0ZS1uZXctZmlsZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGNyZWF0ZU5ld01hcmtkb3duRmlsZSA9ICdmaWxlYnJvd3NlcjpjcmVhdGUtbmV3LW1hcmtkb3duLWZpbGUnO1xuXG4gIGV4cG9ydCBjb25zdCByZWZyZXNoID0gJ2ZpbGVicm93c2VyOnJlZnJlc2gnO1xuXG4gIGV4cG9ydCBjb25zdCByZW5hbWUgPSAnZmlsZWJyb3dzZXI6cmVuYW1lJztcblxuICAvLyBGb3IgbWFpbiBicm93c2VyIG9ubHkuXG4gIGV4cG9ydCBjb25zdCBjb3B5U2hhcmVhYmxlTGluayA9ICdmaWxlYnJvd3NlcjpzaGFyZS1tYWluJztcblxuICAvLyBGb3IgbWFpbiBicm93c2VyIG9ubHkuXG4gIGV4cG9ydCBjb25zdCBjb3B5UGF0aCA9ICdmaWxlYnJvd3Nlcjpjb3B5LXBhdGgnO1xuXG4gIGV4cG9ydCBjb25zdCBzaG93QnJvd3NlciA9ICdmaWxlYnJvd3NlcjphY3RpdmF0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHNodXRkb3duID0gJ2ZpbGVicm93c2VyOnNodXRkb3duJztcblxuICAvLyBGb3IgbWFpbiBicm93c2VyIG9ubHkuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVCcm93c2VyID0gJ2ZpbGVicm93c2VyOnRvZ2dsZS1tYWluJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlTmF2aWdhdGVUb0N1cnJlbnREaXJlY3RvcnkgPVxuICAgICdmaWxlYnJvd3Nlcjp0b2dnbGUtbmF2aWdhdGUtdG8tY3VycmVudC1kaXJlY3RvcnknO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVMYXN0TW9kaWZpZWQgPSAnZmlsZWJyb3dzZXI6dG9nZ2xlLWxhc3QtbW9kaWZpZWQnO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVGaWxlU2l6ZSA9ICdmaWxlYnJvd3Nlcjp0b2dnbGUtZmlsZS1zaXplJztcblxuICBleHBvcnQgY29uc3QgdG9nZ2xlU29ydE5vdGVib29rc0ZpcnN0ID1cbiAgICAnZmlsZWJyb3dzZXI6dG9nZ2xlLXNvcnQtbm90ZWJvb2tzLWZpcnN0JztcblxuICBleHBvcnQgY29uc3Qgc2VhcmNoID0gJ2ZpbGVicm93c2VyOnNlYXJjaCc7XG5cbiAgZXhwb3J0IGNvbnN0IHRvZ2dsZUhpZGRlbkZpbGVzID0gJ2ZpbGVicm93c2VyOnRvZ2dsZS1oaWRkZW4tZmlsZXMnO1xuXG4gIGV4cG9ydCBjb25zdCB0b2dnbGVGaWxlQ2hlY2tib3hlcyA9ICdmaWxlYnJvd3Nlcjp0b2dnbGUtZmlsZS1jaGVja2JveGVzJztcbn1cblxuLyoqXG4gKiBUaGUgZmlsZSBicm93c2VyIG5hbWVzcGFjZSB0b2tlbi5cbiAqL1xuY29uc3QgbmFtZXNwYWNlID0gJ2ZpbGVicm93c2VyJztcblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBmaWxlIGJyb3dzZXIgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBicm93c2VyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiBGSUxFX0JST1dTRVJfUExVR0lOX0lELFxuICBkZXNjcmlwdGlvbjogJ1NldCB1cCB0aGUgZGVmYXVsdCBmaWxlIGJyb3dzZXIgKGNvbW1hbmRzLCBzZXR0aW5ncywuLi4pLicsXG4gIHJlcXVpcmVzOiBbSURlZmF1bHRGaWxlQnJvd3NlciwgSUZpbGVCcm93c2VyRmFjdG9yeSwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW1xuICAgIElMYXlvdXRSZXN0b3JlcixcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIElUcmVlUGF0aFVwZGF0ZXIsXG4gICAgSUNvbW1hbmRQYWxldHRlXG4gIF0sXG4gIHByb3ZpZGVzOiBJRmlsZUJyb3dzZXJDb21tYW5kcyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGRlZmF1bHRGaWxlQnJvd3NlcjogSURlZmF1bHRGaWxlQnJvd3NlcixcbiAgICBmYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsLFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGwsXG4gICAgdHJlZVBhdGhVcGRhdGVyOiBJVHJlZVBhdGhVcGRhdGVyIHwgbnVsbCxcbiAgICBjb21tYW5kUGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuICApOiBQcm9taXNlPHZvaWQ+ID0+IHtcbiAgICBjb25zdCBicm93c2VyID0gZGVmYXVsdEZpbGVCcm93c2VyO1xuXG4gICAgLy8gTGV0IHRoZSBhcHBsaWNhdGlvbiByZXN0b3JlciB0cmFjayB0aGUgcHJpbWFyeSBmaWxlIGJyb3dzZXIgKHRoYXQgaXNcbiAgICAvLyBhdXRvbWF0aWNhbGx5IGNyZWF0ZWQpIGZvciByZXN0b3JhdGlvbiBvZiBhcHBsaWNhdGlvbiBzdGF0ZSAoZS5nLiBzZXR0aW5nXG4gICAgLy8gdGhlIGZpbGUgYnJvd3NlciBhcyB0aGUgY3VycmVudCBzaWRlIGJhciB3aWRnZXQpLlxuICAgIC8vXG4gICAgLy8gQWxsIG90aGVyIGZpbGUgYnJvd3NlcnMgY3JlYXRlZCBieSB1c2luZyB0aGUgZmFjdG9yeSBmdW5jdGlvbiBhcmVcbiAgICAvLyByZXNwb25zaWJsZSBmb3IgdGhlaXIgb3duIHJlc3RvcmF0aW9uIGJlaGF2aW9yLCBpZiBhbnkuXG4gICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICByZXN0b3Jlci5hZGQoYnJvd3NlciwgbmFtZXNwYWNlKTtcbiAgICB9XG5cbiAgICAvLyBOYXZpZ2F0ZSB0byBwcmVmZXJyZWQtZGlyIHRyYWl0IGlmIGZvdW5kXG4gICAgY29uc3QgcHJlZmVycmVkUGF0aCA9IFBhZ2VDb25maWcuZ2V0T3B0aW9uKCdwcmVmZXJyZWRQYXRoJyk7XG4gICAgaWYgKHByZWZlcnJlZFBhdGgpIHtcbiAgICAgIGF3YWl0IGJyb3dzZXIubW9kZWwuY2QocHJlZmVycmVkUGF0aCk7XG4gICAgfVxuXG4gICAgYWRkQ29tbWFuZHMoXG4gICAgICBhcHAsXG4gICAgICBicm93c2VyLFxuICAgICAgZmFjdG9yeSxcbiAgICAgIHRyYW5zbGF0b3IsXG4gICAgICBzZXR0aW5nUmVnaXN0cnksXG4gICAgICBjb21tYW5kUGFsZXR0ZVxuICAgICk7XG5cbiAgICByZXR1cm4gdm9pZCBQcm9taXNlLmFsbChbYXBwLnJlc3RvcmVkLCBicm93c2VyLm1vZGVsLnJlc3RvcmVkXSkudGhlbigoKSA9PiB7XG4gICAgICBpZiAodHJlZVBhdGhVcGRhdGVyKSB7XG4gICAgICAgIGJyb3dzZXIubW9kZWwucGF0aENoYW5nZWQuY29ubmVjdCgoc2VuZGVyLCBhcmdzKSA9PiB7XG4gICAgICAgICAgdHJlZVBhdGhVcGRhdGVyKGFyZ3MubmV3VmFsdWUpO1xuICAgICAgICB9KTtcbiAgICAgIH1cblxuICAgICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgICB2b2lkIHNldHRpbmdSZWdpc3RyeS5sb2FkKEZJTEVfQlJPV1NFUl9QTFVHSU5fSUQpLnRoZW4oc2V0dGluZ3MgPT4ge1xuICAgICAgICAgIC8qKlxuICAgICAgICAgICAqIEZpbGUgYnJvd3NlciBjb25maWd1cmF0aW9uLlxuICAgICAgICAgICAqL1xuICAgICAgICAgIGNvbnN0IGZpbGVCcm93c2VyQ29uZmlnID0ge1xuICAgICAgICAgICAgbmF2aWdhdGVUb0N1cnJlbnREaXJlY3Rvcnk6IGZhbHNlLFxuICAgICAgICAgICAgc2hvd0xhc3RNb2RpZmllZENvbHVtbjogdHJ1ZSxcbiAgICAgICAgICAgIHNob3dGaWxlU2l6ZUNvbHVtbjogZmFsc2UsXG4gICAgICAgICAgICBzaG93SGlkZGVuRmlsZXM6IGZhbHNlLFxuICAgICAgICAgICAgc2hvd0ZpbGVDaGVja2JveGVzOiBmYWxzZSxcbiAgICAgICAgICAgIHNvcnROb3RlYm9va3NGaXJzdDogZmFsc2VcbiAgICAgICAgICB9O1xuICAgICAgICAgIGNvbnN0IGZpbGVCcm93c2VyTW9kZWxDb25maWcgPSB7XG4gICAgICAgICAgICBmaWx0ZXJEaXJlY3RvcmllczogdHJ1ZVxuICAgICAgICAgIH07XG5cbiAgICAgICAgICBmdW5jdGlvbiBvblNldHRpbmdzQ2hhbmdlZChcbiAgICAgICAgICAgIHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5nc1xuICAgICAgICAgICk6IHZvaWQge1xuICAgICAgICAgICAgbGV0IGtleToga2V5b2YgdHlwZW9mIGZpbGVCcm93c2VyQ29uZmlnO1xuICAgICAgICAgICAgZm9yIChrZXkgaW4gZmlsZUJyb3dzZXJDb25maWcpIHtcbiAgICAgICAgICAgICAgY29uc3QgdmFsdWUgPSBzZXR0aW5ncy5nZXQoa2V5KS5jb21wb3NpdGUgYXMgYm9vbGVhbjtcbiAgICAgICAgICAgICAgZmlsZUJyb3dzZXJDb25maWdba2V5XSA9IHZhbHVlO1xuICAgICAgICAgICAgICBicm93c2VyW2tleV0gPSB2YWx1ZTtcbiAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgY29uc3QgdmFsdWUgPSBzZXR0aW5ncy5nZXQoJ2ZpbHRlckRpcmVjdG9yaWVzJylcbiAgICAgICAgICAgICAgLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICAgICAgZmlsZUJyb3dzZXJNb2RlbENvbmZpZy5maWx0ZXJEaXJlY3RvcmllcyA9IHZhbHVlO1xuICAgICAgICAgICAgYnJvd3Nlci5tb2RlbC5maWx0ZXJEaXJlY3RvcmllcyA9IHZhbHVlO1xuICAgICAgICAgIH1cbiAgICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3Qob25TZXR0aW5nc0NoYW5nZWQpO1xuICAgICAgICAgIG9uU2V0dGluZ3NDaGFuZ2VkKHNldHRpbmdzKTtcbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgZmlsZSBicm93c2VyIGZhY3RvcnkgcHJvdmlkZXIuXG4gKi9cbmNvbnN0IGZhY3Rvcnk6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJRmlsZUJyb3dzZXJGYWN0b3J5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246ZmFjdG9yeScsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGZpbGUgYnJvd3NlciBmYWN0b3J5LicsXG4gIHByb3ZpZGVzOiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICByZXF1aXJlczogW0lEb2N1bWVudE1hbmFnZXIsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJU3RhdGVEQiwgSnVweXRlckxhYi5JSW5mb10sXG4gIGFjdGl2YXRlOiBhc3luYyAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBzdGF0ZTogSVN0YXRlREIgfCBudWxsLFxuICAgIGluZm86IEp1cHl0ZXJMYWIuSUluZm8gfCBudWxsXG4gICk6IFByb21pc2U8SUZpbGVCcm93c2VyRmFjdG9yeT4gPT4ge1xuICAgIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxGaWxlQnJvd3Nlcj4oeyBuYW1lc3BhY2UgfSk7XG4gICAgY29uc3QgY3JlYXRlRmlsZUJyb3dzZXIgPSAoXG4gICAgICBpZDogc3RyaW5nLFxuICAgICAgb3B0aW9uczogSUZpbGVCcm93c2VyRmFjdG9yeS5JT3B0aW9ucyA9IHt9XG4gICAgKSA9PiB7XG4gICAgICBjb25zdCBtb2RlbCA9IG5ldyBGaWx0ZXJGaWxlQnJvd3Nlck1vZGVsKHtcbiAgICAgICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvcixcbiAgICAgICAgYXV0bzogb3B0aW9ucy5hdXRvID8/IHRydWUsXG4gICAgICAgIG1hbmFnZXI6IGRvY01hbmFnZXIsXG4gICAgICAgIGRyaXZlTmFtZTogb3B0aW9ucy5kcml2ZU5hbWUgfHwgJycsXG4gICAgICAgIHJlZnJlc2hJbnRlcnZhbDogb3B0aW9ucy5yZWZyZXNoSW50ZXJ2YWwsXG4gICAgICAgIHJlZnJlc2hTdGFuZGJ5OiAoKSA9PiB7XG4gICAgICAgICAgaWYgKGluZm8pIHtcbiAgICAgICAgICAgIHJldHVybiAhaW5mby5pc0Nvbm5lY3RlZCB8fCAnd2hlbi1oaWRkZW4nO1xuICAgICAgICAgIH1cbiAgICAgICAgICByZXR1cm4gJ3doZW4taGlkZGVuJztcbiAgICAgICAgfSxcbiAgICAgICAgc3RhdGU6XG4gICAgICAgICAgb3B0aW9ucy5zdGF0ZSA9PT0gbnVsbFxuICAgICAgICAgICAgPyB1bmRlZmluZWRcbiAgICAgICAgICAgIDogb3B0aW9ucy5zdGF0ZSB8fCBzdGF0ZSB8fCB1bmRlZmluZWRcbiAgICAgIH0pO1xuICAgICAgY29uc3QgcmVzdG9yZSA9IG9wdGlvbnMucmVzdG9yZTtcbiAgICAgIGNvbnN0IHdpZGdldCA9IG5ldyBGaWxlQnJvd3Nlcih7IGlkLCBtb2RlbCwgcmVzdG9yZSwgdHJhbnNsYXRvciB9KTtcblxuICAgICAgLy8gVHJhY2sgdGhlIG5ld2x5IGNyZWF0ZWQgZmlsZSBicm93c2VyLlxuICAgICAgdm9pZCB0cmFja2VyLmFkZCh3aWRnZXQpO1xuXG4gICAgICByZXR1cm4gd2lkZ2V0O1xuICAgIH07XG5cbiAgICByZXR1cm4geyBjcmVhdGVGaWxlQnJvd3NlciwgdHJhY2tlciB9O1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGZpbGUgYnJvd3NlciBmYWN0b3J5IHByb3ZpZGVyLlxuICovXG5jb25zdCBkZWZhdWx0RmlsZUJyb3dzZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJRGVmYXVsdEZpbGVCcm93c2VyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246ZGVmYXVsdC1maWxlLWJyb3dzZXInLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBkZWZhdWx0IGZpbGUgYnJvd3NlcicsXG4gIHByb3ZpZGVzOiBJRGVmYXVsdEZpbGVCcm93c2VyLFxuICByZXF1aXJlczogW0lGaWxlQnJvd3NlckZhY3RvcnldLFxuICBvcHRpb25hbDogW0lSb3V0ZXIsIEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyLCBJTGFiU2hlbGxdLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGZpbGVCcm93c2VyRmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgICByb3V0ZXI6IElSb3V0ZXIgfCBudWxsLFxuICAgIHRyZWU6IEp1cHl0ZXJGcm9udEVuZC5JVHJlZVJlc29sdmVyIHwgbnVsbCxcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbFxuICApOiBQcm9taXNlPElEZWZhdWx0RmlsZUJyb3dzZXI+ID0+IHtcbiAgICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG5cbiAgICAvLyBNYW51YWxseSByZXN0b3JlIGFuZCBsb2FkIHRoZSBkZWZhdWx0IGZpbGUgYnJvd3Nlci5cbiAgICBjb25zdCBkZWZhdWx0QnJvd3NlciA9IGZpbGVCcm93c2VyRmFjdG9yeS5jcmVhdGVGaWxlQnJvd3NlcignZmlsZWJyb3dzZXInLCB7XG4gICAgICBhdXRvOiBmYWxzZSxcbiAgICAgIHJlc3RvcmU6IGZhbHNlXG4gICAgfSk7XG4gICAgdm9pZCBQcml2YXRlLnJlc3RvcmVCcm93c2VyKFxuICAgICAgZGVmYXVsdEJyb3dzZXIsXG4gICAgICBjb21tYW5kcyxcbiAgICAgIHJvdXRlcixcbiAgICAgIHRyZWUsXG4gICAgICBhcHAsXG4gICAgICBsYWJTaGVsbFxuICAgICk7XG4gICAgcmV0dXJuIGRlZmF1bHRCcm93c2VyO1xuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHByb3ZpZGluZyBkb3dubG9hZCArIGNvcHkgZG93bmxvYWQgbGluayBjb21tYW5kcyBpbiB0aGUgY29udGV4dCBtZW51LlxuICpcbiAqIERpc2FibGluZyB0aGlzIHBsdWdpbiB3aWxsIE5PVCBkaXNhYmxlIGRvd25sb2FkaW5nIGZpbGVzIGZyb20gdGhlIHNlcnZlci5cbiAqIFVzZXJzIHdpbGwgc3RpbGwgYmUgYWJsZSB0byByZXRyaWV2ZSBmaWxlcyBmcm9tIHRoZSBmaWxlIGRvd25sb2FkIFVSTHMgdGhlXG4gKiBzZXJ2ZXIgcHJvdmlkZXMuXG4gKi9cbmNvbnN0IGRvd25sb2FkUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOmRvd25sb2FkJyxcbiAgZGVzY3JpcHRpb246XG4gICAgJ0FkZHMgdGhlIGRvd25sb2FkIGZpbGUgY29tbWFuZHMuIERpc2FibGluZyB0aGlzIHBsdWdpbiB3aWxsIE5PVCBkaXNhYmxlIGRvd25sb2FkaW5nIGZpbGVzIGZyb20gdGhlIHNlcnZlciwgaWYgdGhlIHVzZXIgZW50ZXJzIHRoZSBhcHByb3ByaWF0ZSBkb3dubG9hZCBVUkxzLicsXG4gIHJlcXVpcmVzOiBbSUZpbGVCcm93c2VyRmFjdG9yeSwgSVRyYW5zbGF0b3JdLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApOiB2b2lkID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCB7IHRyYWNrZXIgfSA9IGZhY3Rvcnk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZG93bmxvYWQsIHtcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgICByZXR1cm4gd2lkZ2V0LmRvd25sb2FkKCk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBpY29uOiBkb3dubG9hZEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRG93bmxvYWQnKVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNvcHlEb3dubG9hZExpbmssIHtcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiB3aWRnZXQubW9kZWwubWFuYWdlci5zZXJ2aWNlcy5jb250ZW50c1xuICAgICAgICAgIC5nZXREb3dubG9hZFVybCh3aWRnZXQuc2VsZWN0ZWRJdGVtcygpLm5leHQoKSEudmFsdWUucGF0aClcbiAgICAgICAgICAudGhlbih1cmwgPT4ge1xuICAgICAgICAgICAgQ2xpcGJvYXJkLmNvcHlUb1N5c3RlbSh1cmwpO1xuICAgICAgICAgIH0pO1xuICAgICAgfSxcbiAgICAgIGlzVmlzaWJsZTogKCkgPT5cbiAgICAgICAgLy8gU28gbG9uZyBhcyB0aGlzIGNvbW1hbmQgb25seSBoYW5kbGVzIG9uZSBmaWxlIGF0IHRpbWUsIGRvbid0IHNob3cgaXRcbiAgICAgICAgLy8gaWYgbXVsdGlwbGUgZmlsZXMgYXJlIHNlbGVjdGVkLlxuICAgICAgICAhIXRyYWNrZXIuY3VycmVudFdpZGdldCAmJlxuICAgICAgICBBcnJheS5mcm9tKHRyYWNrZXIuY3VycmVudFdpZGdldC5zZWxlY3RlZEl0ZW1zKCkpLmxlbmd0aCA9PT0gMSxcbiAgICAgIGljb246IGNvcHlJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0NvcHkgRG93bmxvYWQgTGluaycpLFxuICAgICAgbW5lbW9uaWM6IDBcbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0byBhZGQgdGhlIGZpbGUgYnJvd3NlciB3aWRnZXQgdG8gYW4gSUxhYlNoZWxsXG4gKi9cbmNvbnN0IGJyb3dzZXJXaWRnZXQ6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246d2lkZ2V0JyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIHRoZSBmaWxlIGJyb3dzZXIgdG8gdGhlIGFwcGxpY2F0aW9uIHNoZWxsLicsXG4gIHJlcXVpcmVzOiBbXG4gICAgSURvY3VtZW50TWFuYWdlcixcbiAgICBJRGVmYXVsdEZpbGVCcm93c2VyLFxuICAgIElGaWxlQnJvd3NlckZhY3RvcnksXG4gICAgSVNldHRpbmdSZWdpc3RyeSxcbiAgICBJVG9vbGJhcldpZGdldFJlZ2lzdHJ5LFxuICAgIElUcmFuc2xhdG9yLFxuICAgIElMYWJTaGVsbCxcbiAgICBJRmlsZUJyb3dzZXJDb21tYW5kc1xuICBdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZV0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICAgIGJyb3dzZXI6IElEZWZhdWx0RmlsZUJyb3dzZXIsXG4gICAgZmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgdG9vbGJhclJlZ2lzdHJ5OiBJVG9vbGJhcldpZGdldFJlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwsXG4gICAgLy8gV2FpdCB1bnRpbCBmaWxlIGJyb3dzZXIgY29tbWFuZHMgYXJlIHJlYWR5IGJlZm9yZSBhY3RpdmF0aW5nIGZpbGUgYnJvd3NlciB3aWRnZXRcbiAgICBmaWxlQnJvd3NlckNvbW1hbmRzOiBudWxsLFxuICAgIGNvbW1hbmRQYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCB7IHRyYWNrZXIgfSA9IGZhY3Rvcnk7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIC8vIFNldCBhdHRyaWJ1dGVzIHdoZW4gYWRkaW5nIHRoZSBicm93c2VyIHRvIHRoZSBVSVxuICAgIGJyb3dzZXIubm9kZS5zZXRBdHRyaWJ1dGUoJ3JvbGUnLCAncmVnaW9uJyk7XG4gICAgYnJvd3Nlci5ub2RlLnNldEF0dHJpYnV0ZSgnYXJpYS1sYWJlbCcsIHRyYW5zLl9fKCdGaWxlIEJyb3dzZXIgU2VjdGlvbicpKTtcbiAgICBicm93c2VyLnRpdGxlLmljb24gPSBmb2xkZXJJY29uO1xuXG4gICAgLy8gU2hvdyB0aGUgY3VycmVudCBmaWxlIGJyb3dzZXIgc2hvcnRjdXQgaW4gaXRzIHRpdGxlLlxuICAgIGNvbnN0IHVwZGF0ZUJyb3dzZXJUaXRsZSA9ICgpID0+IHtcbiAgICAgIGNvbnN0IGJpbmRpbmcgPSBmaW5kKFxuICAgICAgICBhcHAuY29tbWFuZHMua2V5QmluZGluZ3MsXG4gICAgICAgIGIgPT4gYi5jb21tYW5kID09PSBDb21tYW5kSURzLnRvZ2dsZUJyb3dzZXJcbiAgICAgICk7XG4gICAgICBpZiAoYmluZGluZykge1xuICAgICAgICBjb25zdCBrcyA9IGJpbmRpbmcua2V5cy5tYXAoQ29tbWFuZFJlZ2lzdHJ5LmZvcm1hdEtleXN0cm9rZSkuam9pbignLCAnKTtcbiAgICAgICAgYnJvd3Nlci50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ0ZpbGUgQnJvd3NlciAoJTEpJywga3MpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgYnJvd3Nlci50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ0ZpbGUgQnJvd3NlcicpO1xuICAgICAgfVxuICAgIH07XG4gICAgdXBkYXRlQnJvd3NlclRpdGxlKCk7XG4gICAgYXBwLmNvbW1hbmRzLmtleUJpbmRpbmdDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgdXBkYXRlQnJvd3NlclRpdGxlKCk7XG4gICAgfSk7XG5cbiAgICAvLyBUb29sYmFyXG4gICAgdG9vbGJhclJlZ2lzdHJ5LmFkZEZhY3RvcnkoXG4gICAgICBGSUxFX0JST1dTRVJfRkFDVE9SWSxcbiAgICAgICd1cGxvYWRlcicsXG4gICAgICAoYnJvd3NlcjogRmlsZUJyb3dzZXIpID0+XG4gICAgICAgIG5ldyBVcGxvYWRlcih7IG1vZGVsOiBicm93c2VyLm1vZGVsLCB0cmFuc2xhdG9yIH0pXG4gICAgKTtcblxuICAgIHRvb2xiYXJSZWdpc3RyeS5hZGRGYWN0b3J5KFxuICAgICAgRklMRV9CUk9XU0VSX0ZBQ1RPUlksXG4gICAgICAnZmlsZU5hbWVTZWFyY2hlcicsXG4gICAgICAoYnJvd3NlcjogRmlsZUJyb3dzZXIpID0+IHtcbiAgICAgICAgY29uc3Qgc2VhcmNoZXIgPSBGaWxlbmFtZVNlYXJjaGVyKHtcbiAgICAgICAgICB1cGRhdGVGaWx0ZXI6IChcbiAgICAgICAgICAgIGZpbHRlckZuOiAoaXRlbTogc3RyaW5nKSA9PiBQYXJ0aWFsPElTY29yZT4gfCBudWxsLFxuICAgICAgICAgICAgcXVlcnk/OiBzdHJpbmdcbiAgICAgICAgICApID0+IHtcbiAgICAgICAgICAgIGJyb3dzZXIubW9kZWwuc2V0RmlsdGVyKHZhbHVlID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIGZpbHRlckZuKHZhbHVlLm5hbWUudG9Mb3dlckNhc2UoKSk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9LFxuICAgICAgICAgIHVzZUZ1enp5RmlsdGVyOiB0cnVlLFxuICAgICAgICAgIHBsYWNlaG9sZGVyOiB0cmFucy5fXygnRmlsdGVyIGZpbGVzIGJ5IG5hbWUnKSxcbiAgICAgICAgICBmb3JjZVJlZnJlc2g6IHRydWVcbiAgICAgICAgfSk7XG4gICAgICAgIHNlYXJjaGVyLmFkZENsYXNzKEZJTFRFUkJPWF9DTEFTUyk7XG4gICAgICAgIHJldHVybiBzZWFyY2hlcjtcbiAgICAgIH1cbiAgICApO1xuXG4gICAgc2V0VG9vbGJhcihcbiAgICAgIGJyb3dzZXIsXG4gICAgICBjcmVhdGVUb29sYmFyRmFjdG9yeShcbiAgICAgICAgdG9vbGJhclJlZ2lzdHJ5LFxuICAgICAgICBzZXR0aW5nUmVnaXN0cnksXG4gICAgICAgIEZJTEVfQlJPV1NFUl9GQUNUT1JZLFxuICAgICAgICBicm93c2VyV2lkZ2V0LmlkLFxuICAgICAgICB0cmFuc2xhdG9yXG4gICAgICApXG4gICAgKTtcblxuICAgIGxhYlNoZWxsLmFkZChicm93c2VyLCAnbGVmdCcsIHsgcmFuazogMTAwLCB0eXBlOiAnRmlsZSBCcm93c2VyJyB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVCcm93c2VyLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0ZpbGUgQnJvd3NlcicpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBpZiAoYnJvd3Nlci5pc0hpZGRlbikge1xuICAgICAgICAgIHJldHVybiBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuc2hvd0Jyb3dzZXIsIHZvaWQgMCk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLmhpZGVCcm93c2VyLCB2b2lkIDApO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNob3dCcm93c2VyLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gdGhlIGZpbGUgYnJvd3NlciBmb3IgdGhlIHByb3ZpZGVkIGBwYXRoYC4nKSxcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCBwYXRoID0gKGFyZ3MucGF0aCBhcyBzdHJpbmcpIHx8ICcnO1xuICAgICAgICBjb25zdCBicm93c2VyRm9yUGF0aCA9IFByaXZhdGUuZ2V0QnJvd3NlckZvclBhdGgoXG4gICAgICAgICAgcGF0aCxcbiAgICAgICAgICBicm93c2VyLFxuICAgICAgICAgIGZhY3RvcnlcbiAgICAgICAgKTtcblxuICAgICAgICAvLyBDaGVjayBmb3IgYnJvd3NlciBub3QgZm91bmRcbiAgICAgICAgaWYgKCFicm93c2VyRm9yUGF0aCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICAvLyBTaG9ydGN1dCBpZiB3ZSBhcmUgdXNpbmcgdGhlIG1haW4gZmlsZSBicm93c2VyXG4gICAgICAgIGlmIChicm93c2VyID09PSBicm93c2VyRm9yUGF0aCkge1xuICAgICAgICAgIGxhYlNoZWxsLmFjdGl2YXRlQnlJZChicm93c2VyLmlkKTtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgY29uc3QgYXJlYXM6IElMYWJTaGVsbC5BcmVhW10gPSBbJ2xlZnQnLCAncmlnaHQnXTtcbiAgICAgICAgICBmb3IgKGNvbnN0IGFyZWEgb2YgYXJlYXMpIHtcbiAgICAgICAgICAgIGZvciAoY29uc3Qgd2lkZ2V0IG9mIGxhYlNoZWxsLndpZGdldHMoYXJlYSkpIHtcbiAgICAgICAgICAgICAgaWYgKHdpZGdldC5jb250YWlucyhicm93c2VyRm9yUGF0aCkpIHtcbiAgICAgICAgICAgICAgICBsYWJTaGVsbC5hY3RpdmF0ZUJ5SWQod2lkZ2V0LmlkKTtcbiAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5oaWRlQnJvd3Nlciwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdIaWRlIHRoZSBmaWxlIGJyb3dzZXIuJyksXG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgICAgaWYgKHdpZGdldCAmJiAhd2lkZ2V0LmlzSGlkZGVuKSB7XG4gICAgICAgICAgbGFiU2hlbGwuY29sbGFwc2VMZWZ0KCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVOYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IEFjdGl2ZSBGaWxlIGluIEZpbGUgQnJvd3NlcicpLFxuICAgICAgaXNUb2dnbGVkOiAoKSA9PiBicm93c2VyLm5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5LFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCB2YWx1ZSA9ICFicm93c2VyLm5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5O1xuICAgICAgICBjb25zdCBrZXkgPSAnbmF2aWdhdGVUb0N1cnJlbnREaXJlY3RvcnknO1xuICAgICAgICByZXR1cm4gc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLnNldChGSUxFX0JST1dTRVJfUExVR0lOX0lELCBrZXksIHZhbHVlKVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCBuYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSBzZXR0aW5nYCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBpZiAoY29tbWFuZFBhbGV0dGUpIHtcbiAgICAgIGNvbW1hbmRQYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLnRvZ2dsZU5hdmlnYXRlVG9DdXJyZW50RGlyZWN0b3J5LFxuICAgICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ0ZpbGUgT3BlcmF0aW9ucycpXG4gICAgICB9KTtcbiAgICB9XG5cbiAgICAvLyBJZiB0aGUgbGF5b3V0IGlzIGEgZnJlc2ggc2Vzc2lvbiB3aXRob3V0IHNhdmVkIGRhdGEgYW5kIG5vdCBpbiBzaW5nbGUgZG9jdW1lbnRcbiAgICAvLyBtb2RlLCBvcGVuIGZpbGUgYnJvd3Nlci5cbiAgICB2b2lkIGxhYlNoZWxsLnJlc3RvcmVkLnRoZW4obGF5b3V0ID0+IHtcbiAgICAgIGlmIChsYXlvdXQuZnJlc2ggJiYgbGFiU2hlbGwubW9kZSAhPT0gJ3NpbmdsZS1kb2N1bWVudCcpIHtcbiAgICAgICAgdm9pZCBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuc2hvd0Jyb3dzZXIsIHZvaWQgMCk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICB2b2lkIFByb21pc2UuYWxsKFthcHAucmVzdG9yZWQsIGJyb3dzZXIubW9kZWwucmVzdG9yZWRdKS50aGVuKCgpID0+IHtcbiAgICAgIC8vIFdoZXRoZXIgdG8gYXV0b21hdGljYWxseSBuYXZpZ2F0ZSB0byBhIGRvY3VtZW50J3MgY3VycmVudCBkaXJlY3RvcnlcbiAgICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoYXN5bmMgKF8sIGNoYW5nZSkgPT4ge1xuICAgICAgICBpZiAoYnJvd3Nlci5uYXZpZ2F0ZVRvQ3VycmVudERpcmVjdG9yeSAmJiBjaGFuZ2UubmV3VmFsdWUpIHtcbiAgICAgICAgICBjb25zdCB7IG5ld1ZhbHVlIH0gPSBjaGFuZ2U7XG4gICAgICAgICAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldChuZXdWYWx1ZSk7XG4gICAgICAgICAgaWYgKGNvbnRleHQpIHtcbiAgICAgICAgICAgIGNvbnN0IHsgcGF0aCB9ID0gY29udGV4dDtcbiAgICAgICAgICAgIHRyeSB7XG4gICAgICAgICAgICAgIGF3YWl0IFByaXZhdGUubmF2aWdhdGVUb1BhdGgocGF0aCwgYnJvd3NlciwgZmFjdG9yeSwgdHJhbnNsYXRvcik7XG4gICAgICAgICAgICB9IGNhdGNoIChyZWFzb24pIHtcbiAgICAgICAgICAgICAgY29uc29sZS53YXJuKFxuICAgICAgICAgICAgICAgIGAke0NvbW1hbmRJRHMuZ29Ub1BhdGh9IGZhaWxlZCB0byBvcGVuOiAke3BhdGh9YCxcbiAgICAgICAgICAgICAgICByZWFzb25cbiAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGZpbGUgYnJvd3NlciBzaGFyZS1maWxlIHBsdWdpblxuICpcbiAqIFRoaXMgZXh0ZW5zaW9uIGFkZHMgYSBcIkNvcHkgU2hhcmVhYmxlIExpbmtcIiBjb21tYW5kIHRoYXQgZ2VuZXJhdGVzIGEgY29weS1cbiAqIHBhc3RhYmxlIFVSTC4gVGhpcyB1cmwgY2FuIGJlIHVzZWQgdG8gb3BlbiBhIHBhcnRpY3VsYXIgZmlsZSBpbiBKdXB5dGVyTGFiLFxuICogaGFuZHkgZm9yIGVtYWlsaW5nIGxpbmtzIG9yIGJvb2ttYXJraW5nIGZvciByZWZlcmVuY2UuXG4gKlxuICogSWYgeW91IG5lZWQgdG8gY2hhbmdlIGhvdyB0aGlzIGxpbmsgaXMgZ2VuZXJhdGVkIChmb3IgaW5zdGFuY2UsIHRvIGNvcHkgYVxuICogL3VzZXItcmVkaXJlY3QgVVJMIGZvciBKdXB5dGVySHViKSwgZGlzYWJsZSB0aGlzIHBsdWdpbiBhbmQgcmVwbGFjZSBpdFxuICogd2l0aCBhbm90aGVyIGltcGxlbWVudGF0aW9uLlxuICovXG5jb25zdCBzaGFyZUZpbGU6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246c2hhcmUtZmlsZScsXG4gIGRlc2NyaXB0aW9uOlxuICAgICdBZGRzIHRoZSBcIkNvcHkgU2hhcmVhYmxlIExpbmtcIiBjb21tYW5kOyB1c2VmdWwgZm9yIEp1cHl0ZXJIdWIgZGVwbG95bWVudCBmb3IgZXhhbXBsZS4nLFxuICByZXF1aXJlczogW0lGaWxlQnJvd3NlckZhY3RvcnksIElUcmFuc2xhdG9yXSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnksXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3JcbiAgKTogdm9pZCA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG4gICAgY29uc3QgeyB0cmFja2VyIH0gPSBmYWN0b3J5O1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNvcHlTaGFyZWFibGVMaW5rLCB7XG4gICAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgICAgY29uc3QgbW9kZWwgPSB3aWRnZXQ/LnNlbGVjdGVkSXRlbXMoKS5uZXh0KCk7XG4gICAgICAgIGlmIChtb2RlbCA9PT0gdW5kZWZpbmVkIHx8IG1vZGVsLmRvbmUpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBDbGlwYm9hcmQuY29weVRvU3lzdGVtKFxuICAgICAgICAgIFBhZ2VDb25maWcuZ2V0VXJsKHtcbiAgICAgICAgICAgIHdvcmtzcGFjZTogUGFnZUNvbmZpZy5kZWZhdWx0V29ya3NwYWNlLFxuICAgICAgICAgICAgdHJlZVBhdGg6IG1vZGVsLnZhbHVlLnBhdGgsXG4gICAgICAgICAgICB0b1NoYXJlOiB0cnVlXG4gICAgICAgICAgfSlcbiAgICAgICAgKTtcbiAgICAgIH0sXG4gICAgICBpc1Zpc2libGU6ICgpID0+XG4gICAgICAgICEhdHJhY2tlci5jdXJyZW50V2lkZ2V0ICYmXG4gICAgICAgIEFycmF5LmZyb20odHJhY2tlci5jdXJyZW50V2lkZ2V0LnNlbGVjdGVkSXRlbXMoKSkubGVuZ3RoID09PSAxLFxuICAgICAgaWNvbjogbGlua0ljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnQ29weSBTaGFyZWFibGUgTGluaycpXG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIFwiT3BlbiBXaXRoXCIgY29udGV4dCBtZW51LlxuICpcbiAqIFRoaXMgaXMgaXRzIG93biBwbHVnaW4gaW4gY2FzZSB5b3Ugd291bGQgbGlrZSB0byBkaXNhYmxlIHRoaXMgZmVhdHVyZS5cbiAqIGUuZy4ganVweXRlciBsYWJleHRlbnNpb24gZGlzYWJsZSBAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246b3Blbi13aXRoXG4gKi9cbmNvbnN0IG9wZW5XaXRoUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOm9wZW4td2l0aCcsXG4gIGRlc2NyaXB0aW9uOlxuICAgICdBZGRzIHRoZSBvcGVuLXdpdGggZmVhdHVyZSBhbGxvd2luZyBhbiB1c2VyIHRvIHBpY2sgdGhlIG5vbi1wcmVmZXJyZWQgZG9jdW1lbnQgdmlld2VyLicsXG4gIHJlcXVpcmVzOiBbSUZpbGVCcm93c2VyRmFjdG9yeV0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZCwgZmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHsgZG9jUmVnaXN0cnkgfSA9IGFwcDtcbiAgICBjb25zdCB7IHRyYWNrZXIgfSA9IGZhY3Rvcnk7XG5cbiAgICBsZXQgaXRlbXM6IElEaXNwb3NhYmxlTWVudUl0ZW1bXSA9IFtdO1xuXG4gICAgZnVuY3Rpb24gdXBkYXRlT3BlbldpdGhNZW51KGNvbnRleHRNZW51OiBDb250ZXh0TWVudSkge1xuICAgICAgY29uc3Qgb3BlbldpdGggPVxuICAgICAgICAoY29udGV4dE1lbnUubWVudS5pdGVtcy5maW5kKFxuICAgICAgICAgIGl0ZW0gPT5cbiAgICAgICAgICAgIGl0ZW0udHlwZSA9PT0gJ3N1Ym1lbnUnICYmXG4gICAgICAgICAgICBpdGVtLnN1Ym1lbnU/LmlkID09PSAnanAtY29udGV4dG1lbnUtb3Blbi13aXRoJ1xuICAgICAgICApPy5zdWJtZW51IGFzIFJhbmtlZE1lbnUpID8/IG51bGw7XG5cbiAgICAgIGlmICghb3BlbldpdGgpIHtcbiAgICAgICAgcmV0dXJuOyAvLyBCYWlsIGVhcmx5IGlmIHRoZSBvcGVuIHdpdGggbWVudSBpcyBub3QgZGlzcGxheWVkXG4gICAgICB9XG5cbiAgICAgIC8vIGNsZWFyIHRoZSBjdXJyZW50IG1lbnUgaXRlbXNcbiAgICAgIGl0ZW1zLmZvckVhY2goaXRlbSA9PiBpdGVtLmRpc3Bvc2UoKSk7XG4gICAgICBpdGVtcy5sZW5ndGggPSAwO1xuICAgICAgLy8gRW5zdXJlIHRoYXQgdGhlIG1lbnUgaXMgZW1wdHlcbiAgICAgIG9wZW5XaXRoLmNsZWFySXRlbXMoKTtcblxuICAgICAgLy8gZ2V0IHRoZSB3aWRnZXQgZmFjdG9yaWVzIHRoYXQgY291bGQgYmUgdXNlZCB0byBvcGVuIGFsbCBvZiB0aGUgaXRlbXNcbiAgICAgIC8vIGluIHRoZSBjdXJyZW50IGZpbGVicm93c2VyIHNlbGVjdGlvblxuICAgICAgY29uc3QgZmFjdG9yaWVzID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0XG4gICAgICAgID8gUHJpdmF0ZS5PcGVuV2l0aC5pbnRlcnNlY3Rpb248RG9jdW1lbnRSZWdpc3RyeS5XaWRnZXRGYWN0b3J5PihcbiAgICAgICAgICAgIG1hcCh0cmFja2VyLmN1cnJlbnRXaWRnZXQuc2VsZWN0ZWRJdGVtcygpLCBpID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIFByaXZhdGUuT3BlbldpdGguZ2V0RmFjdG9yaWVzKGRvY1JlZ2lzdHJ5LCBpKTtcbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgKVxuICAgICAgICA6IG5ldyBTZXQ8RG9jdW1lbnRSZWdpc3RyeS5XaWRnZXRGYWN0b3J5PigpO1xuXG4gICAgICAvLyBtYWtlIG5ldyBtZW51IGl0ZW1zIGZyb20gdGhlIHdpZGdldCBmYWN0b3JpZXNcbiAgICAgIGl0ZW1zID0gWy4uLmZhY3Rvcmllc10ubWFwKGZhY3RvcnkgPT5cbiAgICAgICAgb3BlbldpdGguYWRkSXRlbSh7XG4gICAgICAgICAgYXJnczogeyBmYWN0b3J5OiBmYWN0b3J5Lm5hbWUsIGxhYmVsOiBmYWN0b3J5LmxhYmVsIHx8IGZhY3RvcnkubmFtZSB9LFxuICAgICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlblxuICAgICAgICB9KVxuICAgICAgKTtcbiAgICB9XG5cbiAgICBhcHAuY29udGV4dE1lbnUub3BlbmVkLmNvbm5lY3QodXBkYXRlT3BlbldpdGhNZW51KTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgXCJPcGVuIGluIE5ldyBCcm93c2VyIFRhYlwiIGNvbnRleHQgbWVudS5cbiAqXG4gKiBUaGlzIGlzIGl0cyBvd24gcGx1Z2luIGluIGNhc2UgeW91IHdvdWxkIGxpa2UgdG8gZGlzYWJsZSB0aGlzIGZlYXR1cmUuXG4gKiBlLmcuIGp1cHl0ZXIgbGFiZXh0ZW5zaW9uIGRpc2FibGUgQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOm9wZW4tYnJvd3Nlci10YWJcbiAqXG4gKiBOb3RlOiBJZiBkaXNhYmxpbmcgdGhpcywgeW91IG1heSBhbHNvIHdhbnQgdG8gZGlzYWJsZTpcbiAqIEBqdXB5dGVybGFiL2RvY21hbmFnZXItZXh0ZW5zaW9uOm9wZW4tYnJvd3Nlci10YWJcbiAqL1xuY29uc3Qgb3BlbkJyb3dzZXJUYWJQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246b3Blbi1icm93c2VyLXRhYicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0aGUgb3Blbi1pbi1uZXctYnJvd3Nlci10YWIgZmVhdHVyZXMuJyxcbiAgcmVxdWlyZXM6IFtJRmlsZUJyb3dzZXJGYWN0b3J5LCBJVHJhbnNsYXRvcl0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBmYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgdHJhY2tlciB9ID0gZmFjdG9yeTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuQnJvd3NlclRhYiwge1xuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcblxuICAgICAgICBpZiAoIXdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IG1vZGUgPSBhcmdzWydtb2RlJ10gYXMgc3RyaW5nIHwgdW5kZWZpbmVkO1xuXG4gICAgICAgIHJldHVybiBQcm9taXNlLmFsbChcbiAgICAgICAgICBBcnJheS5mcm9tKFxuICAgICAgICAgICAgbWFwKHdpZGdldC5zZWxlY3RlZEl0ZW1zKCksIGl0ZW0gPT4ge1xuICAgICAgICAgICAgICBpZiAobW9kZSA9PT0gJ3NpbmdsZS1kb2N1bWVudCcpIHtcbiAgICAgICAgICAgICAgICBjb25zdCB1cmwgPSBQYWdlQ29uZmlnLmdldFVybCh7XG4gICAgICAgICAgICAgICAgICBtb2RlOiAnc2luZ2xlLWRvY3VtZW50JyxcbiAgICAgICAgICAgICAgICAgIHRyZWVQYXRoOiBpdGVtLnBhdGhcbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICBjb25zdCBvcGVuZWQgPSB3aW5kb3cub3BlbigpO1xuICAgICAgICAgICAgICAgIGlmIChvcGVuZWQpIHtcbiAgICAgICAgICAgICAgICAgIG9wZW5lZC5vcGVuZXIgPSBudWxsO1xuICAgICAgICAgICAgICAgICAgb3BlbmVkLmxvY2F0aW9uLmhyZWYgPSB1cmw7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgIHRocm93IG5ldyBFcnJvcignRmFpbGVkIHRvIG9wZW4gbmV3IGJyb3dzZXIgdGFiLicpO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuLWJyb3dzZXItdGFiJywge1xuICAgICAgICAgICAgICAgICAgcGF0aDogaXRlbS5wYXRoXG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgKVxuICAgICAgICApO1xuICAgICAgfSxcbiAgICAgIGljb246IGFkZEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICAgIGxhYmVsOiBhcmdzID0+XG4gICAgICAgIGFyZ3NbJ21vZGUnXSA9PT0gJ3NpbmdsZS1kb2N1bWVudCdcbiAgICAgICAgICA/IHRyYW5zLl9fKCdPcGVuIGluIFNpbXBsZSBNb2RlJylcbiAgICAgICAgICA6IHRyYW5zLl9fKCdPcGVuIGluIE5ldyBCcm93c2VyIFRhYicpLFxuICAgICAgbW5lbW9uaWM6IDBcbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiBwcm92aWRpbmcgZmlsZSB1cGxvYWQgc3RhdHVzLlxuICovXG5leHBvcnQgY29uc3QgZmlsZVVwbG9hZFN0YXR1czogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpmaWxlLXVwbG9hZC1zdGF0dXMnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgYSBmaWxlIHVwbG9hZCBzdGF0dXMgd2lkZ2V0LicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJRmlsZUJyb3dzZXJGYWN0b3J5LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSVN0YXR1c0Jhcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgYnJvd3NlcjogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBzdGF0dXNCYXI6IElTdGF0dXNCYXIgfCBudWxsXG4gICkgPT4ge1xuICAgIGlmICghc3RhdHVzQmFyKSB7XG4gICAgICAvLyBBdXRvbWF0aWNhbGx5IGRpc2FibGUgaWYgc3RhdHVzYmFyIG1pc3NpbmdcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgaXRlbSA9IG5ldyBGaWxlVXBsb2FkU3RhdHVzKHtcbiAgICAgIHRyYWNrZXI6IGJyb3dzZXIudHJhY2tlcixcbiAgICAgIHRyYW5zbGF0b3JcbiAgICB9KTtcblxuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0oXG4gICAgICAnQGp1cHl0ZXJsYWIvZmlsZWJyb3dzZXItZXh0ZW5zaW9uOmZpbGUtdXBsb2FkLXN0YXR1cycsXG4gICAgICB7XG4gICAgICAgIGl0ZW0sXG4gICAgICAgIGFsaWduOiAnbWlkZGxlJyxcbiAgICAgICAgaXNBY3RpdmU6ICgpID0+IHtcbiAgICAgICAgICByZXR1cm4gISFpdGVtLm1vZGVsICYmIGl0ZW0ubW9kZWwuaXRlbXMubGVuZ3RoID4gMDtcbiAgICAgICAgfSxcbiAgICAgICAgYWN0aXZlU3RhdGVDaGFuZ2VkOiBpdGVtLm1vZGVsLnN0YXRlQ2hhbmdlZFxuICAgICAgfVxuICAgICk7XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdG8gb3BlbiBmaWxlcyBmcm9tIHJlbW90ZSBVUkxzXG4gKi9cbmNvbnN0IG9wZW5VcmxQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9maWxlYnJvd3Nlci1leHRlbnNpb246b3Blbi11cmwnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgdGhlIGZlYXR1cmUgXCJPcGVuIGZpbGVzIGZyb20gcmVtb3RlIFVSTHNcIi4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSURlZmF1bHRGaWxlQnJvd3NlciwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZV0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgYnJvd3NlcjogRmlsZUJyb3dzZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB7IGNvbW1hbmRzIH0gPSBhcHA7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBjb21tYW5kID0gQ29tbWFuZElEcy5vcGVuVXJsO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChjb21tYW5kLCB7XG4gICAgICBsYWJlbDogYXJncyA9PlxuICAgICAgICBhcmdzLnVybCA/IHRyYW5zLl9fKCdPcGVuICUxJywgYXJncy51cmwpIDogdHJhbnMuX18oJ09wZW4gZnJvbSBVUkzigKYnKSxcbiAgICAgIGNhcHRpb246IGFyZ3MgPT5cbiAgICAgICAgYXJncy51cmwgPyB0cmFucy5fXygnT3BlbiAlMScsIGFyZ3MudXJsKSA6IHRyYW5zLl9fKCdPcGVuIGZyb20gVVJMJyksXG4gICAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgICAgbGV0IHVybDogc3RyaW5nIHwgdW5kZWZpbmVkID0gKGFyZ3M/LnVybCBhcyBzdHJpbmcpID8/ICcnO1xuICAgICAgICBpZiAoIXVybCkge1xuICAgICAgICAgIHVybCA9XG4gICAgICAgICAgICAoXG4gICAgICAgICAgICAgIGF3YWl0IElucHV0RGlhbG9nLmdldFRleHQoe1xuICAgICAgICAgICAgICAgIGxhYmVsOiB0cmFucy5fXygnVVJMJyksXG4gICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI6ICdodHRwczovL2V4YW1wbGUuY29tL3BhdGgvdG8vZmlsZScsXG4gICAgICAgICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdPcGVuIFVSTCcpLFxuICAgICAgICAgICAgICAgIG9rTGFiZWw6IHRyYW5zLl9fKCdPcGVuJylcbiAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICkudmFsdWUgPz8gdW5kZWZpbmVkO1xuICAgICAgICB9XG4gICAgICAgIGlmICghdXJsKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgbGV0IHR5cGUgPSAnJztcbiAgICAgICAgbGV0IGJsb2I7XG5cbiAgICAgICAgLy8gZmV0Y2ggdGhlIGZpbGUgZnJvbSB0aGUgVVJMXG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgY29uc3QgcmVxID0gYXdhaXQgZmV0Y2godXJsKTtcbiAgICAgICAgICBibG9iID0gYXdhaXQgcmVxLmJsb2IoKTtcbiAgICAgICAgICB0eXBlID0gcmVxLmhlYWRlcnMuZ2V0KCdDb250ZW50LVR5cGUnKSA/PyAnJztcbiAgICAgICAgfSBjYXRjaCAocmVhc29uKSB7XG4gICAgICAgICAgaWYgKHJlYXNvbi5yZXNwb25zZSAmJiByZWFzb24ucmVzcG9uc2Uuc3RhdHVzICE9PSAyMDApIHtcbiAgICAgICAgICAgIHJlYXNvbi5tZXNzYWdlID0gdHJhbnMuX18oJ0NvdWxkIG5vdCBvcGVuIFVSTDogJTEnLCB1cmwpO1xuICAgICAgICAgIH1cbiAgICAgICAgICByZXR1cm4gc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnQ2Fubm90IGZldGNoJyksIHJlYXNvbik7XG4gICAgICAgIH1cblxuICAgICAgICAvLyB1cGxvYWQgdGhlIGNvbnRlbnQgb2YgdGhlIGZpbGUgdG8gdGhlIHNlcnZlclxuICAgICAgICB0cnkge1xuICAgICAgICAgIGNvbnN0IG5hbWUgPSBQYXRoRXh0LmJhc2VuYW1lKHVybCk7XG4gICAgICAgICAgY29uc3QgZmlsZSA9IG5ldyBGaWxlKFtibG9iXSwgbmFtZSwgeyB0eXBlIH0pO1xuICAgICAgICAgIGNvbnN0IG1vZGVsID0gYXdhaXQgYnJvd3Nlci5tb2RlbC51cGxvYWQoZmlsZSk7XG4gICAgICAgICAgcmV0dXJuIGNvbW1hbmRzLmV4ZWN1dGUoJ2RvY21hbmFnZXI6b3BlbicsIHtcbiAgICAgICAgICAgIHBhdGg6IG1vZGVsLnBhdGhcbiAgICAgICAgICB9KTtcbiAgICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgICByZXR1cm4gc2hvd0Vycm9yTWVzc2FnZShcbiAgICAgICAgICAgIHRyYW5zLl9wKCdzaG93RXJyb3JNZXNzYWdlJywgJ1VwbG9hZCBFcnJvcicpLFxuICAgICAgICAgICAgZXJyb3JcbiAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgY29tbWFuZCxcbiAgICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdGaWxlIE9wZXJhdGlvbnMnKVxuICAgICAgfSk7XG4gICAgfVxuICB9XG59O1xuXG4vKipcbiAqIEFkZCB0aGUgbWFpbiBmaWxlIGJyb3dzZXIgY29tbWFuZHMgdG8gdGhlIGFwcGxpY2F0aW9uJ3MgY29tbWFuZCByZWdpc3RyeS5cbiAqL1xuZnVuY3Rpb24gYWRkQ29tbWFuZHMoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBicm93c2VyOiBGaWxlQnJvd3NlcixcbiAgZmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGwsXG4gIGNvbW1hbmRQYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4pOiB2b2lkIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgeyBkb2NSZWdpc3RyeTogcmVnaXN0cnksIGNvbW1hbmRzIH0gPSBhcHA7XG4gIGNvbnN0IHsgdHJhY2tlciB9ID0gZmFjdG9yeTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZGVsLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiB3aWRnZXQuZGVsZXRlKCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpY29uOiBjbG9zZUljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0RlbGV0ZScpLFxuICAgIG1uZW1vbmljOiAwXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5LCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiB3aWRnZXQuY29weSgpO1xuICAgICAgfVxuICAgIH0sXG4gICAgaWNvbjogY29weUljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0NvcHknKSxcbiAgICBtbmVtb25pYzogMFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3V0LCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiB3aWRnZXQuY3V0KCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpY29uOiBjdXRJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdDdXQnKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZHVwbGljYXRlLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICBpZiAod2lkZ2V0KSB7XG4gICAgICAgIHJldHVybiB3aWRnZXQuZHVwbGljYXRlKCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpY29uOiBjb3B5SWNvbi5iaW5kcHJvcHMoeyBzdHlsZXNoZWV0OiAnbWVudUl0ZW0nIH0pLFxuICAgIGxhYmVsOiB0cmFucy5fXygnRHVwbGljYXRlJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmdvVG9QYXRoLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdVcGRhdGUgdGhlIGZpbGUgYnJvd3NlciB0byBkaXNwbGF5IHRoZSBwcm92aWRlZCBgcGF0aGAuJyksXG4gICAgZXhlY3V0ZTogYXN5bmMgYXJncyA9PiB7XG4gICAgICBjb25zdCBwYXRoID0gKGFyZ3MucGF0aCBhcyBzdHJpbmcpIHx8ICcnO1xuICAgICAgY29uc3Qgc2hvd0Jyb3dzZXIgPSAhKGFyZ3M/LmRvbnRTaG93QnJvd3NlciA/PyBmYWxzZSk7XG4gICAgICB0cnkge1xuICAgICAgICBjb25zdCBpdGVtID0gYXdhaXQgUHJpdmF0ZS5uYXZpZ2F0ZVRvUGF0aChcbiAgICAgICAgICBwYXRoLFxuICAgICAgICAgIGJyb3dzZXIsXG4gICAgICAgICAgZmFjdG9yeSxcbiAgICAgICAgICB0cmFuc2xhdG9yXG4gICAgICAgICk7XG4gICAgICAgIGlmIChpdGVtLnR5cGUgIT09ICdkaXJlY3RvcnknICYmIHNob3dCcm93c2VyKSB7XG4gICAgICAgICAgY29uc3QgYnJvd3NlckZvclBhdGggPSBQcml2YXRlLmdldEJyb3dzZXJGb3JQYXRoKFxuICAgICAgICAgICAgcGF0aCxcbiAgICAgICAgICAgIGJyb3dzZXIsXG4gICAgICAgICAgICBmYWN0b3J5XG4gICAgICAgICAgKTtcbiAgICAgICAgICBpZiAoYnJvd3NlckZvclBhdGgpIHtcbiAgICAgICAgICAgIGJyb3dzZXJGb3JQYXRoLmNsZWFyU2VsZWN0ZWRJdGVtcygpO1xuICAgICAgICAgICAgY29uc3QgcGFydHMgPSBwYXRoLnNwbGl0KCcvJyk7XG4gICAgICAgICAgICBjb25zdCBuYW1lID0gcGFydHNbcGFydHMubGVuZ3RoIC0gMV07XG4gICAgICAgICAgICBpZiAobmFtZSkge1xuICAgICAgICAgICAgICBhd2FpdCBicm93c2VyRm9yUGF0aC5zZWxlY3RJdGVtQnlOYW1lKG5hbWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSBjYXRjaCAocmVhc29uKSB7XG4gICAgICAgIGNvbnNvbGUud2FybihgJHtDb21tYW5kSURzLmdvVG9QYXRofSBmYWlsZWQgdG8gZ28gdG86ICR7cGF0aH1gLCByZWFzb24pO1xuICAgICAgfVxuICAgICAgaWYgKHNob3dCcm93c2VyKSB7XG4gICAgICAgIHJldHVybiBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuc2hvd0Jyb3dzZXIsIHsgcGF0aCB9KTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5nb1VwLCB7XG4gICAgbGFiZWw6ICdnbyB1cCcsXG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3QgYnJvd3NlckZvclBhdGggPSBQcml2YXRlLmdldEJyb3dzZXJGb3JQYXRoKCcnLCBicm93c2VyLCBmYWN0b3J5KTtcbiAgICAgIGlmICghYnJvd3NlckZvclBhdGgpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgeyBtb2RlbCB9ID0gYnJvd3NlckZvclBhdGg7XG4gICAgICBhd2FpdCBtb2RlbC5yZXN0b3JlZDtcbiAgICAgIHZvaWQgYnJvd3NlckZvclBhdGguZ29VcCgpO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW5QYXRoLCB7XG4gICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgIGFyZ3MucGF0aCA/IHRyYW5zLl9fKCdPcGVuICUxJywgYXJncy5wYXRoKSA6IHRyYW5zLl9fKCdPcGVuIGZyb20gUGF0aOKApicpLFxuICAgIGNhcHRpb246IGFyZ3MgPT5cbiAgICAgIGFyZ3MucGF0aCA/IHRyYW5zLl9fKCdPcGVuICUxJywgYXJncy5wYXRoKSA6IHRyYW5zLl9fKCdPcGVuIGZyb20gcGF0aCcpLFxuICAgIGV4ZWN1dGU6IGFzeW5jIGFyZ3MgPT4ge1xuICAgICAgbGV0IHBhdGg6IHN0cmluZyB8IHVuZGVmaW5lZDtcbiAgICAgIGlmIChhcmdzPy5wYXRoKSB7XG4gICAgICAgIHBhdGggPSBhcmdzLnBhdGggYXMgc3RyaW5nO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgcGF0aCA9XG4gICAgICAgICAgKFxuICAgICAgICAgICAgYXdhaXQgSW5wdXREaWFsb2cuZ2V0VGV4dCh7XG4gICAgICAgICAgICAgIGxhYmVsOiB0cmFucy5fXygnUGF0aCcpLFxuICAgICAgICAgICAgICBwbGFjZWhvbGRlcjogJy9wYXRoL3JlbGF0aXZlL3RvL2psYWIvcm9vdCcsXG4gICAgICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnT3BlbiBQYXRoJyksXG4gICAgICAgICAgICAgIG9rTGFiZWw6IHRyYW5zLl9fKCdPcGVuJylcbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgKS52YWx1ZSA/PyB1bmRlZmluZWQ7XG4gICAgICB9XG4gICAgICBpZiAoIXBhdGgpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3QgdHJhaWxpbmdTbGFzaCA9IHBhdGggIT09ICcvJyAmJiBwYXRoLmVuZHNXaXRoKCcvJyk7XG4gICAgICAgIGlmICh0cmFpbGluZ1NsYXNoKSB7XG4gICAgICAgICAgLy8gVGhlIG5vcm1hbCBjb250ZW50cyBzZXJ2aWNlIGVycm9ycyBvbiBwYXRocyBlbmRpbmcgaW4gc2xhc2hcbiAgICAgICAgICBwYXRoID0gcGF0aC5zbGljZSgwLCBwYXRoLmxlbmd0aCAtIDEpO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IGJyb3dzZXJGb3JQYXRoID0gUHJpdmF0ZS5nZXRCcm93c2VyRm9yUGF0aChcbiAgICAgICAgICBwYXRoLFxuICAgICAgICAgIGJyb3dzZXIsXG4gICAgICAgICAgZmFjdG9yeVxuICAgICAgICApITtcbiAgICAgICAgY29uc3QgeyBzZXJ2aWNlcyB9ID0gYnJvd3NlckZvclBhdGgubW9kZWwubWFuYWdlcjtcbiAgICAgICAgY29uc3QgaXRlbSA9IGF3YWl0IHNlcnZpY2VzLmNvbnRlbnRzLmdldChwYXRoLCB7XG4gICAgICAgICAgY29udGVudDogZmFsc2VcbiAgICAgICAgfSk7XG4gICAgICAgIGlmICh0cmFpbGluZ1NsYXNoICYmIGl0ZW0udHlwZSAhPT0gJ2RpcmVjdG9yeScpIHtcbiAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYFBhdGggJHtwYXRofS8gaXMgbm90IGEgZGlyZWN0b3J5YCk7XG4gICAgICAgIH1cbiAgICAgICAgYXdhaXQgY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLmdvVG9QYXRoLCB7XG4gICAgICAgICAgcGF0aCxcbiAgICAgICAgICBkb250U2hvd0Jyb3dzZXI6IGFyZ3MuZG9udFNob3dCcm93c2VyXG4gICAgICAgIH0pO1xuICAgICAgICBpZiAoaXRlbS50eXBlID09PSAnZGlyZWN0b3J5Jykge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuJywgeyBwYXRoIH0pO1xuICAgICAgfSBjYXRjaCAocmVhc29uKSB7XG4gICAgICAgIGlmIChyZWFzb24ucmVzcG9uc2UgJiYgcmVhc29uLnJlc3BvbnNlLnN0YXR1cyA9PT0gNDA0KSB7XG4gICAgICAgICAgcmVhc29uLm1lc3NhZ2UgPSB0cmFucy5fXygnQ291bGQgbm90IGZpbmQgcGF0aDogJTEnLCBwYXRoKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gc2hvd0Vycm9yTWVzc2FnZSh0cmFucy5fXygnQ2Fubm90IG9wZW4nKSwgcmVhc29uKTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIC8vIEFkZCB0aGUgb3BlblBhdGggY29tbWFuZCB0byB0aGUgY29tbWFuZCBwYWxldHRlXG4gIGlmIChjb21tYW5kUGFsZXR0ZSkge1xuICAgIGNvbW1hbmRQYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5vcGVuUGF0aCxcbiAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnRmlsZSBPcGVyYXRpb25zJylcbiAgICB9KTtcbiAgfVxuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuLCB7XG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBmYWN0b3J5ID0gKGFyZ3NbJ2ZhY3RvcnknXSBhcyBzdHJpbmcpIHx8IHZvaWQgMDtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcblxuICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICBjb25zdCB7IGNvbnRlbnRzIH0gPSB3aWRnZXQubW9kZWwubWFuYWdlci5zZXJ2aWNlcztcbiAgICAgIHJldHVybiBQcm9taXNlLmFsbChcbiAgICAgICAgQXJyYXkuZnJvbShcbiAgICAgICAgICBtYXAod2lkZ2V0LnNlbGVjdGVkSXRlbXMoKSwgaXRlbSA9PiB7XG4gICAgICAgICAgICBpZiAoaXRlbS50eXBlID09PSAnZGlyZWN0b3J5Jykge1xuICAgICAgICAgICAgICBjb25zdCBsb2NhbFBhdGggPSBjb250ZW50cy5sb2NhbFBhdGgoaXRlbS5wYXRoKTtcbiAgICAgICAgICAgICAgcmV0dXJuIHdpZGdldC5tb2RlbC5jZChgLyR7bG9jYWxQYXRofWApO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuJywge1xuICAgICAgICAgICAgICBmYWN0b3J5OiBmYWN0b3J5LFxuICAgICAgICAgICAgICBwYXRoOiBpdGVtLnBhdGhcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH0pXG4gICAgICAgIClcbiAgICAgICk7XG4gICAgfSxcbiAgICBpY29uOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IGZhY3RvcnkgPSAoYXJnc1snZmFjdG9yeSddIGFzIHN0cmluZykgfHwgdm9pZCAwO1xuICAgICAgaWYgKGZhY3RvcnkpIHtcbiAgICAgICAgLy8gaWYgYW4gZXhwbGljaXQgZmFjdG9yeSBpcyBwYXNzZWQuLi5cbiAgICAgICAgY29uc3QgZnQgPSByZWdpc3RyeS5nZXRGaWxlVHlwZShmYWN0b3J5KTtcbiAgICAgICAgLy8gLi4uc2V0IGFuIGljb24gaWYgdGhlIGZhY3RvcnkgbmFtZSBjb3JyZXNwb25kcyB0byBhIGZpbGUgdHlwZSBuYW1lLi4uXG4gICAgICAgIC8vIC4uLm9yIGxlYXZlIHRoZSBpY29uIGJsYW5rXG4gICAgICAgIHJldHVybiBmdD8uaWNvbj8uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHJldHVybiBmb2xkZXJJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSk7XG4gICAgICB9XG4gICAgfSxcbiAgICBsYWJlbDogYXJncyA9PlxuICAgICAgKGFyZ3NbJ2xhYmVsJ10gfHwgYXJnc1snZmFjdG9yeSddIHx8IHRyYW5zLl9fKCdPcGVuJykpIGFzIHN0cmluZyxcbiAgICBtbmVtb25pYzogMFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucGFzdGUsIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5wYXN0ZSgpO1xuICAgICAgfVxuICAgIH0sXG4gICAgaWNvbjogcGFzdGVJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdQYXN0ZScpLFxuICAgIG1uZW1vbmljOiAwXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jcmVhdGVOZXdEaXJlY3RvcnksIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5jcmVhdGVOZXdEaXJlY3RvcnkoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IG5ld0ZvbGRlckljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ05ldyBGb2xkZXInKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3JlYXRlTmV3RmlsZSwge1xuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcblxuICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICByZXR1cm4gd2lkZ2V0LmNyZWF0ZU5ld0ZpbGUoeyBleHQ6ICd0eHQnIH0pO1xuICAgICAgfVxuICAgIH0sXG4gICAgaWNvbjogdGV4dEVkaXRvckljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ05ldyBGaWxlJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNyZWF0ZU5ld01hcmtkb3duRmlsZSwge1xuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcblxuICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICByZXR1cm4gd2lkZ2V0LmNyZWF0ZU5ld0ZpbGUoeyBleHQ6ICdtZCcgfSk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpY29uOiBtYXJrZG93bkljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ05ldyBNYXJrZG93biBGaWxlJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlZnJlc2gsIHtcbiAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcblxuICAgICAgaWYgKHdpZGdldCkge1xuICAgICAgICByZXR1cm4gd2lkZ2V0Lm1vZGVsLnJlZnJlc2goKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IHNrUmVmcmVzaEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBjYXB0aW9uOiB0cmFucy5fXygnUmVmcmVzaCB0aGUgZmlsZSBicm93c2VyLicpLFxuICAgIGxhYmVsOiB0cmFucy5fXygnUmVmcmVzaCBGaWxlIExpc3QnKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVuYW1lLCB7XG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5yZW5hbWUoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGlzVmlzaWJsZTogKCkgPT5cbiAgICAgIC8vIFNvIGxvbmcgYXMgdGhpcyBjb21tYW5kIG9ubHkgaGFuZGxlcyBvbmUgZmlsZSBhdCB0aW1lLCBkb24ndCBzaG93IGl0XG4gICAgICAvLyBpZiBtdWx0aXBsZSBmaWxlcyBhcmUgc2VsZWN0ZWQuXG4gICAgICAhIXRyYWNrZXIuY3VycmVudFdpZGdldCAmJlxuICAgICAgQXJyYXkuZnJvbSh0cmFja2VyLmN1cnJlbnRXaWRnZXQuc2VsZWN0ZWRJdGVtcygpKS5sZW5ndGggPT09IDEsXG4gICAgaWNvbjogZWRpdEljb24uYmluZHByb3BzKHsgc3R5bGVzaGVldDogJ21lbnVJdGVtJyB9KSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1JlbmFtZScpLFxuICAgIG1uZW1vbmljOiAwXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5UGF0aCwge1xuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGl0ZW0gPSB3aWRnZXQuc2VsZWN0ZWRJdGVtcygpLm5leHQoKTtcbiAgICAgIGlmIChpdGVtLmRvbmUpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICBpZiAoUGFnZUNvbmZpZy5nZXRPcHRpb24oJ2NvcHlBYnNvbHV0ZVBhdGgnKSA9PT0gJ3RydWUnKSB7XG4gICAgICAgIGNvbnN0IGFic29sdXRlUGF0aCA9IFBhdGhFeHQuam9pbihcbiAgICAgICAgICBQYWdlQ29uZmlnLmdldE9wdGlvbignc2VydmVyUm9vdCcpID8/ICcnLFxuICAgICAgICAgIGl0ZW0udmFsdWUucGF0aFxuICAgICAgICApO1xuICAgICAgICBDbGlwYm9hcmQuY29weVRvU3lzdGVtKGFic29sdXRlUGF0aCk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBDbGlwYm9hcmQuY29weVRvU3lzdGVtKGl0ZW0udmFsdWUucGF0aCk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc1Zpc2libGU6ICgpID0+XG4gICAgICAvLyBTbyBsb25nIGFzIHRoaXMgY29tbWFuZCBvbmx5IGhhbmRsZXMgb25lIGZpbGUgYXQgdGltZSwgZG9uJ3Qgc2hvdyBpdFxuICAgICAgLy8gaWYgbXVsdGlwbGUgZmlsZXMgYXJlIHNlbGVjdGVkLlxuICAgICAgISF0cmFja2VyLmN1cnJlbnRXaWRnZXQgJiZcbiAgICAgIEFycmF5LmZyb20odHJhY2tlci5jdXJyZW50V2lkZ2V0LnNlbGVjdGVkSXRlbXMoKSkubGVuZ3RoID09PSAxLFxuICAgIGljb246IGZpbGVJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdDb3B5IFBhdGgnKVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2h1dGRvd24sIHtcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG5cbiAgICAgIGlmICh3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIHdpZGdldC5zaHV0ZG93bktlcm5lbHMoKTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGljb246IHN0b3BJY29uLmJpbmRwcm9wcyh7IHN0eWxlc2hlZXQ6ICdtZW51SXRlbScgfSksXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTaHV0IERvd24gS2VybmVsJylcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZUxhc3RNb2RpZmllZCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2hvdyBMYXN0IE1vZGlmaWVkIENvbHVtbicpLFxuICAgIGlzVG9nZ2xlZDogKCkgPT4gYnJvd3Nlci5zaG93TGFzdE1vZGlmaWVkQ29sdW1uLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHZhbHVlID0gIWJyb3dzZXIuc2hvd0xhc3RNb2RpZmllZENvbHVtbjtcbiAgICAgIGNvbnN0IGtleSA9ICdzaG93TGFzdE1vZGlmaWVkQ29sdW1uJztcbiAgICAgIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICAgICAgcmV0dXJuIHNldHRpbmdSZWdpc3RyeVxuICAgICAgICAgIC5zZXQoRklMRV9CUk9XU0VSX1BMVUdJTl9JRCwga2V5LCB2YWx1ZSlcbiAgICAgICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYEZhaWxlZCB0byBzZXQgJHtrZXl9IHNldHRpbmdgKTtcbiAgICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVTb3J0Tm90ZWJvb2tzRmlyc3QsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1NvcnQgTm90ZWJvb2tzIEFib3ZlIEZpbGVzJyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBicm93c2VyLnNvcnROb3RlYm9va3NGaXJzdCxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB2YWx1ZSA9ICFicm93c2VyLnNvcnROb3RlYm9va3NGaXJzdDtcbiAgICAgIGNvbnN0IGtleSA9ICdzb3J0Tm90ZWJvb2tzRmlyc3QnO1xuICAgICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgICByZXR1cm4gc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLnNldChGSUxFX0JST1dTRVJfUExVR0lOX0lELCBrZXksIHZhbHVlKVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCAke2tleX0gc2V0dGluZ2ApO1xuICAgICAgICAgIH0pO1xuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZUZpbGVTaXplLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IEZpbGUgU2l6ZSBDb2x1bW4nKSxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+IGJyb3dzZXIuc2hvd0ZpbGVTaXplQ29sdW1uLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHZhbHVlID0gIWJyb3dzZXIuc2hvd0ZpbGVTaXplQ29sdW1uO1xuICAgICAgY29uc3Qga2V5ID0gJ3Nob3dGaWxlU2l6ZUNvbHVtbic7XG4gICAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICAgIHJldHVybiBzZXR0aW5nUmVnaXN0cnlcbiAgICAgICAgICAuc2V0KEZJTEVfQlJPV1NFUl9QTFVHSU5fSUQsIGtleSwgdmFsdWUpXG4gICAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmVycm9yKGBGYWlsZWQgdG8gc2V0ICR7a2V5fSBzZXR0aW5nYCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMudG9nZ2xlSGlkZGVuRmlsZXMsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgSGlkZGVuIEZpbGVzJyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBicm93c2VyLnNob3dIaWRkZW5GaWxlcyxcbiAgICBpc1Zpc2libGU6ICgpID0+IFBhZ2VDb25maWcuZ2V0T3B0aW9uKCdhbGxvd19oaWRkZW5fZmlsZXMnKSA9PT0gJ3RydWUnLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHZhbHVlID0gIWJyb3dzZXIuc2hvd0hpZGRlbkZpbGVzO1xuICAgICAgY29uc3Qga2V5ID0gJ3Nob3dIaWRkZW5GaWxlcyc7XG4gICAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICAgIHJldHVybiBzZXR0aW5nUmVnaXN0cnlcbiAgICAgICAgICAuc2V0KEZJTEVfQlJPV1NFUl9QTFVHSU5fSUQsIGtleSwgdmFsdWUpXG4gICAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgICBjb25zb2xlLmVycm9yKGBGYWlsZWQgdG8gc2V0IHNob3dIaWRkZW5GaWxlcyBzZXR0aW5nYCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMudG9nZ2xlRmlsZUNoZWNrYm94ZXMsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgRmlsZSBDaGVja2JveGVzJyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBicm93c2VyLnNob3dGaWxlQ2hlY2tib3hlcyxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCB2YWx1ZSA9ICFicm93c2VyLnNob3dGaWxlQ2hlY2tib3hlcztcbiAgICAgIGNvbnN0IGtleSA9ICdzaG93RmlsZUNoZWNrYm94ZXMnO1xuICAgICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgICByZXR1cm4gc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgLnNldChGSUxFX0JST1dTRVJfUExVR0lOX0lELCBrZXksIHZhbHVlKVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCBzaG93RmlsZUNoZWNrYm94ZXMgc2V0dGluZ2ApO1xuICAgICAgICAgIH0pO1xuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNlYXJjaCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnU2VhcmNoIG9uIEZpbGUgTmFtZXMnKSxcbiAgICBleGVjdXRlOiAoKSA9PiBhbGVydCgnc2VhcmNoJylcbiAgfSk7XG59XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIGZhY3RvcnksXG4gIGRlZmF1bHRGaWxlQnJvd3NlcixcbiAgYnJvd3NlcixcbiAgc2hhcmVGaWxlLFxuICBmaWxlVXBsb2FkU3RhdHVzLFxuICBkb3dubG9hZFBsdWdpbixcbiAgYnJvd3NlcldpZGdldCxcbiAgb3BlbldpdGhQbHVnaW4sXG4gIG9wZW5Ccm93c2VyVGFiUGx1Z2luLFxuICBvcGVuVXJsUGx1Z2luXG5dO1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBtb2R1bGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogR2V0IGJyb3dzZXIgb2JqZWN0IGdpdmVuIGZpbGUgcGF0aC5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBnZXRCcm93c2VyRm9yUGF0aChcbiAgICBwYXRoOiBzdHJpbmcsXG4gICAgYnJvd3NlcjogRmlsZUJyb3dzZXIsXG4gICAgZmFjdG9yeTogSUZpbGVCcm93c2VyRmFjdG9yeVxuICApOiBGaWxlQnJvd3NlciB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgeyB0cmFja2VyIH0gPSBmYWN0b3J5O1xuICAgIGNvbnN0IGRyaXZlTmFtZSA9IGJyb3dzZXIubW9kZWwubWFuYWdlci5zZXJ2aWNlcy5jb250ZW50cy5kcml2ZU5hbWUocGF0aCk7XG5cbiAgICBpZiAoZHJpdmVOYW1lKSB7XG4gICAgICBjb25zdCBicm93c2VyRm9yUGF0aCA9IHRyYWNrZXIuZmluZChcbiAgICAgICAgX3BhdGggPT4gX3BhdGgubW9kZWwuZHJpdmVOYW1lID09PSBkcml2ZU5hbWVcbiAgICAgICk7XG5cbiAgICAgIGlmICghYnJvd3NlckZvclBhdGgpIHtcbiAgICAgICAgLy8gd2FybiB0aGF0IG5vIGZpbGVicm93c2VyIGNvdWxkIGJlIGZvdW5kIGZvciB0aGlzIGRyaXZlTmFtZVxuICAgICAgICBjb25zb2xlLndhcm4oXG4gICAgICAgICAgYCR7Q29tbWFuZElEcy5nb1RvUGF0aH0gZmFpbGVkIHRvIGZpbmQgZmlsZWJyb3dzZXIgZm9yIHBhdGg6ICR7cGF0aH1gXG4gICAgICAgICk7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIGJyb3dzZXJGb3JQYXRoO1xuICAgIH1cblxuICAgIC8vIGlmIGRyaXZlTmFtZSBpcyBlbXB0eSwgYXNzdW1lIHRoZSBtYWluIGZpbGVicm93c2VyXG4gICAgcmV0dXJuIGJyb3dzZXI7XG4gIH1cblxuICAvKipcbiAgICogTmF2aWdhdGUgdG8gYSBwYXRoIG9yIHRoZSBwYXRoIGNvbnRhaW5pbmcgYSBmaWxlLlxuICAgKi9cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIG5hdmlnYXRlVG9QYXRoKFxuICAgIHBhdGg6IHN0cmluZyxcbiAgICBicm93c2VyOiBGaWxlQnJvd3NlcixcbiAgICBmYWN0b3J5OiBJRmlsZUJyb3dzZXJGYWN0b3J5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IFByb21pc2U8Q29udGVudHMuSU1vZGVsPiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBicm93c2VyRm9yUGF0aCA9IFByaXZhdGUuZ2V0QnJvd3NlckZvclBhdGgocGF0aCwgYnJvd3NlciwgZmFjdG9yeSk7XG4gICAgaWYgKCFicm93c2VyRm9yUGF0aCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKHRyYW5zLl9fKCdObyBicm93c2VyIGZvciBwYXRoJykpO1xuICAgIH1cbiAgICBjb25zdCB7IHNlcnZpY2VzIH0gPSBicm93c2VyRm9yUGF0aC5tb2RlbC5tYW5hZ2VyO1xuICAgIGNvbnN0IGxvY2FsUGF0aCA9IHNlcnZpY2VzLmNvbnRlbnRzLmxvY2FsUGF0aChwYXRoKTtcblxuICAgIGF3YWl0IHNlcnZpY2VzLnJlYWR5O1xuICAgIGNvbnN0IGl0ZW0gPSBhd2FpdCBzZXJ2aWNlcy5jb250ZW50cy5nZXQocGF0aCwgeyBjb250ZW50OiBmYWxzZSB9KTtcbiAgICBjb25zdCB7IG1vZGVsIH0gPSBicm93c2VyRm9yUGF0aDtcbiAgICBhd2FpdCBtb2RlbC5yZXN0b3JlZDtcbiAgICBpZiAoaXRlbS50eXBlID09PSAnZGlyZWN0b3J5Jykge1xuICAgICAgYXdhaXQgbW9kZWwuY2QoYC8ke2xvY2FsUGF0aH1gKTtcbiAgICB9IGVsc2Uge1xuICAgICAgYXdhaXQgbW9kZWwuY2QoYC8ke1BhdGhFeHQuZGlybmFtZShsb2NhbFBhdGgpfWApO1xuICAgIH1cbiAgICByZXR1cm4gaXRlbTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXN0b3JlcyBmaWxlIGJyb3dzZXIgc3RhdGUgYW5kIG92ZXJyaWRlcyBzdGF0ZSBpZiB0cmVlIHJlc29sdmVyIHJlc29sdmVzLlxuICAgKi9cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIHJlc3RvcmVCcm93c2VyKFxuICAgIGJyb3dzZXI6IEZpbGVCcm93c2VyLFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gICAgcm91dGVyOiBJUm91dGVyIHwgbnVsbCxcbiAgICB0cmVlOiBKdXB5dGVyRnJvbnRFbmQuSVRyZWVSZXNvbHZlciB8IG51bGwsXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGxcbiAgKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgcmVzdG9yaW5nID0gJ2pwLW1vZC1yZXN0b3JpbmcnO1xuXG4gICAgYnJvd3Nlci5hZGRDbGFzcyhyZXN0b3JpbmcpO1xuXG4gICAgaWYgKCFyb3V0ZXIpIHtcbiAgICAgIGF3YWl0IGJyb3dzZXIubW9kZWwucmVzdG9yZShicm93c2VyLmlkKTtcbiAgICAgIGF3YWl0IGJyb3dzZXIubW9kZWwucmVmcmVzaCgpO1xuICAgICAgYnJvd3Nlci5yZW1vdmVDbGFzcyhyZXN0b3JpbmcpO1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IGxpc3RlbmVyID0gYXN5bmMgKCkgPT4ge1xuICAgICAgcm91dGVyLnJvdXRlZC5kaXNjb25uZWN0KGxpc3RlbmVyKTtcblxuICAgICAgY29uc3QgcGF0aHMgPSBhd2FpdCB0cmVlPy5wYXRocztcbiAgICAgIGlmIChwYXRocz8uZmlsZSB8fCBwYXRocz8uYnJvd3Nlcikge1xuICAgICAgICAvLyBSZXN0b3JlIHRoZSBtb2RlbCB3aXRob3V0IHBvcHVsYXRpbmcgaXQuXG4gICAgICAgIGF3YWl0IGJyb3dzZXIubW9kZWwucmVzdG9yZShicm93c2VyLmlkLCBmYWxzZSk7XG4gICAgICAgIGlmIChwYXRocy5maWxlKSB7XG4gICAgICAgICAgYXdhaXQgY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLm9wZW5QYXRoLCB7XG4gICAgICAgICAgICBwYXRoOiBwYXRocy5maWxlLFxuICAgICAgICAgICAgZG9udFNob3dCcm93c2VyOiB0cnVlXG4gICAgICAgICAgfSk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHBhdGhzLmJyb3dzZXIpIHtcbiAgICAgICAgICBhd2FpdCBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMub3BlblBhdGgsIHtcbiAgICAgICAgICAgIHBhdGg6IHBhdGhzLmJyb3dzZXIsXG4gICAgICAgICAgICBkb250U2hvd0Jyb3dzZXI6IHRydWVcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgfSBlbHNlIHtcbiAgICAgICAgYXdhaXQgYnJvd3Nlci5tb2RlbC5yZXN0b3JlKGJyb3dzZXIuaWQpO1xuICAgICAgICBhd2FpdCBicm93c2VyLm1vZGVsLnJlZnJlc2goKTtcbiAgICAgIH1cbiAgICAgIGJyb3dzZXIucmVtb3ZlQ2xhc3MocmVzdG9yaW5nKTtcblxuICAgICAgaWYgKGxhYlNoZWxsPy5pc0VtcHR5KCdtYWluJykpIHtcbiAgICAgICAgdm9pZCBjb21tYW5kcy5leGVjdXRlKCdsYXVuY2hlcjpjcmVhdGUnKTtcbiAgICAgIH1cbiAgICB9O1xuICAgIHJvdXRlci5yb3V0ZWQuY29ubmVjdChsaXN0ZW5lcik7XG4gIH1cblxuICBleHBvcnQgbmFtZXNwYWNlIE9wZW5XaXRoIHtcbiAgICAvKipcbiAgICAgKiBHZXQgdGhlIGZhY3RvcmllcyBmb3IgdGhlIHNlbGVjdGVkIGl0ZW1cbiAgICAgKlxuICAgICAqIEBwYXJhbSBkb2NSZWdpc3RyeSBBcHBsaWNhdGlvbiBkb2N1bWVudCByZWdpc3RyeVxuICAgICAqIEBwYXJhbSBpdGVtIFNlbGVjdGVkIGl0ZW0gbW9kZWxcbiAgICAgKiBAcmV0dXJucyBBdmFpbGFibGUgZmFjdG9yaWVzIGZvciB0aGUgbW9kZWxcbiAgICAgKi9cbiAgICBleHBvcnQgZnVuY3Rpb24gZ2V0RmFjdG9yaWVzKFxuICAgICAgZG9jUmVnaXN0cnk6IERvY3VtZW50UmVnaXN0cnksXG4gICAgICBpdGVtOiBDb250ZW50cy5JTW9kZWxcbiAgICApOiBBcnJheTxEb2N1bWVudFJlZ2lzdHJ5LldpZGdldEZhY3Rvcnk+IHtcbiAgICAgIGNvbnN0IGZhY3RvcmllcyA9IGRvY1JlZ2lzdHJ5LnByZWZlcnJlZFdpZGdldEZhY3RvcmllcyhpdGVtLnBhdGgpO1xuICAgICAgY29uc3Qgbm90ZWJvb2tGYWN0b3J5ID0gZG9jUmVnaXN0cnkuZ2V0V2lkZ2V0RmFjdG9yeSgnbm90ZWJvb2snKTtcbiAgICAgIGlmIChcbiAgICAgICAgbm90ZWJvb2tGYWN0b3J5ICYmXG4gICAgICAgIGl0ZW0udHlwZSA9PT0gJ25vdGVib29rJyAmJlxuICAgICAgICBmYWN0b3JpZXMuaW5kZXhPZihub3RlYm9va0ZhY3RvcnkpID09PSAtMVxuICAgICAgKSB7XG4gICAgICAgIGZhY3Rvcmllcy51bnNoaWZ0KG5vdGVib29rRmFjdG9yeSk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBmYWN0b3JpZXM7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmV0dXJuIHRoZSBpbnRlcnNlY3Rpb24gb2YgbXVsdGlwbGUgaXRlcmFibGVzLlxuICAgICAqXG4gICAgICogQHBhcmFtIGl0ZXJhYmxlcyBJdGVyYXRvciBvZiBpdGVyYWJsZXNcbiAgICAgKiBAcmV0dXJucyBTZXQgb2YgY29tbW9uIGVsZW1lbnRzIHRvIGFsbCBpdGVyYWJsZXNcbiAgICAgKi9cbiAgICBleHBvcnQgZnVuY3Rpb24gaW50ZXJzZWN0aW9uPFQ+KGl0ZXJhYmxlczogSXRlcmFibGU8SXRlcmFibGU8VD4+KTogU2V0PFQ+IHtcbiAgICAgIGxldCBhY2N1bXVsYXRvcjogU2V0PFQ+IHwgdW5kZWZpbmVkID0gdW5kZWZpbmVkO1xuICAgICAgZm9yIChjb25zdCBjdXJyZW50IG9mIGl0ZXJhYmxlcykge1xuICAgICAgICAvLyBJbml0aWFsaXplIGFjY3VtdWxhdG9yLlxuICAgICAgICBpZiAoYWNjdW11bGF0b3IgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgIGFjY3VtdWxhdG9yID0gbmV3IFNldChjdXJyZW50KTtcbiAgICAgICAgICBjb250aW51ZTtcbiAgICAgICAgfVxuICAgICAgICAvLyBSZXR1cm4gZWFybHkgaWYgZW1wdHkuXG4gICAgICAgIGlmIChhY2N1bXVsYXRvci5zaXplID09PSAwKSB7XG4gICAgICAgICAgcmV0dXJuIGFjY3VtdWxhdG9yO1xuICAgICAgICB9XG4gICAgICAgIC8vIEtlZXAgdGhlIGludGVyc2VjdGlvbiBvZiBhY2N1bXVsYXRvciBhbmQgY3VycmVudC5cbiAgICAgICAgbGV0IGludGVyc2VjdGlvbiA9IG5ldyBTZXQ8VD4oKTtcbiAgICAgICAgZm9yIChjb25zdCB2YWx1ZSBvZiBjdXJyZW50KSB7XG4gICAgICAgICAgaWYgKGFjY3VtdWxhdG9yLmhhcyh2YWx1ZSkpIHtcbiAgICAgICAgICAgIGludGVyc2VjdGlvbi5hZGQodmFsdWUpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgICBhY2N1bXVsYXRvciA9IGludGVyc2VjdGlvbjtcbiAgICAgIH1cbiAgICAgIHJldHVybiBhY2N1bXVsYXRvciA/PyBuZXcgU2V0KCk7XG4gICAgfVxuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=