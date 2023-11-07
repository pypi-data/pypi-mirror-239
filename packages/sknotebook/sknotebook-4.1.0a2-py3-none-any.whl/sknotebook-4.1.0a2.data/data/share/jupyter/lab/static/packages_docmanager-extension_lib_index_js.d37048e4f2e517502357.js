"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_docmanager-extension_lib_index_js"],{

/***/ "../packages/docmanager-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/docmanager-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ToolbarItems": () => (/* binding */ ToolbarItems),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "downloadPlugin": () => (/* binding */ downloadPlugin),
/* harmony export */   "openBrowserTabPlugin": () => (/* binding */ openBrowserTabPlugin),
/* harmony export */   "pathStatusPlugin": () => (/* binding */ pathStatusPlugin),
/* harmony export */   "savingStatusPlugin": () => (/* binding */ savingStatusPlugin)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_12__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module docmanager-extension
 */













/**
 * The command IDs used by the document manager plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.clone = 'docmanager:clone';
    CommandIDs.deleteFile = 'docmanager:delete-file';
    CommandIDs.newUntitled = 'docmanager:new-untitled';
    CommandIDs.open = 'docmanager:open';
    CommandIDs.openBrowserTab = 'docmanager:open-browser-tab';
    CommandIDs.reload = 'docmanager:reload';
    CommandIDs.rename = 'docmanager:rename';
    CommandIDs.del = 'docmanager:delete';
    CommandIDs.duplicate = 'docmanager:duplicate';
    CommandIDs.restoreCheckpoint = 'docmanager:restore-checkpoint';
    CommandIDs.save = 'docmanager:save';
    CommandIDs.saveAll = 'docmanager:save-all';
    CommandIDs.saveAs = 'docmanager:save-as';
    CommandIDs.download = 'docmanager:download';
    CommandIDs.toggleAutosave = 'docmanager:toggle-autosave';
    CommandIDs.showInFileBrowser = 'docmanager:show-in-file-browser';
})(CommandIDs || (CommandIDs = {}));
/**
 * The id of the document manager plugin.
 */
const docManagerPluginId = '@jupyterlab/docmanager-extension:plugin';
/**
 * A plugin to open documents in the main area.
 *
 */
const openerPlugin = {
    id: '@jupyterlab/docmanager-extension:opener',
    description: 'Provides the widget opener.',
    autoStart: true,
    provides: _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener,
    activate: (app) => {
        const { shell } = app;
        return new (class {
            constructor() {
                this._opened = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_10__.Signal(this);
            }
            open(widget, options) {
                if (!widget.id) {
                    widget.id = `document-manager-${++Private.id}`;
                }
                widget.title.dataset = {
                    type: 'document-title',
                    ...widget.title.dataset
                };
                if (!widget.isAttached) {
                    shell.add(widget, 'main', options || {});
                }
                shell.activateById(widget.id);
                this._opened.emit(widget);
            }
            get opened() {
                return this._opened;
            }
        })();
    }
};
/**
 * A plugin to handle dirty states for open documents.
 */
const contextsPlugin = {
    id: '@jupyterlab/docmanager-extension:contexts',
    description: 'Adds the handling of opened documents dirty state.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus],
    activate: (app, docManager, widgetOpener, status) => {
        const contexts = new WeakSet();
        widgetOpener.opened.connect((_, widget) => {
            // Handle dirty state for open documents.
            const context = docManager.contextForWidget(widget);
            if (context && !contexts.has(context)) {
                if (status) {
                    handleContext(status, context);
                }
                contexts.add(context);
            }
        });
    }
};
/**
 * A plugin providing the default document manager.
 */
const manager = {
    id: '@jupyterlab/docmanager-extension:manager',
    description: 'Provides the document manager.',
    provides: _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ISessionContextDialogs, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab.IInfo],
    activate: (app, widgetOpener, translator_, status, sessionDialogs_, info) => {
        var _a;
        const { serviceManager: manager, docRegistry: registry } = app;
        const translator = translator_ !== null && translator_ !== void 0 ? translator_ : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator;
        const sessionDialogs = sessionDialogs_ !== null && sessionDialogs_ !== void 0 ? sessionDialogs_ : new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SessionContextDialogs({ translator });
        const when = app.restored.then(() => void 0);
        const docManager = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.DocumentManager({
            registry,
            manager,
            opener: widgetOpener,
            when,
            setBusy: (_a = (status && (() => status.setBusy()))) !== null && _a !== void 0 ? _a : undefined,
            sessionDialogs,
            translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator,
            isConnectedCallback: () => {
                if (info) {
                    return info.isConnected;
                }
                return true;
            }
        });
        return docManager;
    }
};
/**
 * The default document manager provider commands and settings.
 */
const docManagerPlugin = {
    id: docManagerPluginId,
    description: 'Adds commands and settings to the document manager.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentWidgetOpener, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: (app, docManager, widgetOpener, settingRegistry, translator, palette, labShell) => {
        translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const registry = app.docRegistry;
        // Register the file operations commands.
        addCommands(app, docManager, widgetOpener, settingRegistry, translator, labShell, palette);
        // Keep up to date with the settings registry.
        const onSettingsUpdated = (settings) => {
            // Handle whether to autosave
            const autosave = settings.get('autosave').composite;
            docManager.autosave =
                autosave === true || autosave === false ? autosave : true;
            app.commands.notifyCommandChanged(CommandIDs.toggleAutosave);
            const confirmClosingDocument = settings.get('confirmClosingDocument')
                .composite;
            docManager.confirmClosingDocument = confirmClosingDocument !== null && confirmClosingDocument !== void 0 ? confirmClosingDocument : true;
            // Handle autosave interval
            const autosaveInterval = settings.get('autosaveInterval').composite;
            docManager.autosaveInterval = autosaveInterval || 120;
            // Handle last modified timestamp check margin
            const lastModifiedCheckMargin = settings.get('lastModifiedCheckMargin')
                .composite;
            docManager.lastModifiedCheckMargin = lastModifiedCheckMargin || 500;
            const renameUntitledFile = settings.get('renameUntitledFileOnSave')
                .composite;
            docManager.renameUntitledFileOnSave = renameUntitledFile !== null && renameUntitledFile !== void 0 ? renameUntitledFile : true;
            // Handle default widget factory overrides.
            const defaultViewers = settings.get('defaultViewers').composite;
            const overrides = {};
            // Filter the defaultViewers and file types for existing ones.
            Object.keys(defaultViewers).forEach(ft => {
                if (!registry.getFileType(ft)) {
                    console.warn(`File Type ${ft} not found`);
                    return;
                }
                if (!registry.getWidgetFactory(defaultViewers[ft])) {
                    console.warn(`Document viewer ${defaultViewers[ft]} not found`);
                }
                overrides[ft] = defaultViewers[ft];
            });
            // Set the default factory overrides. If not provided, this has the
            // effect of unsetting any previous overrides.
            for (const ft of registry.fileTypes()) {
                try {
                    registry.setDefaultWidgetFactory(ft.name, overrides[ft.name]);
                }
                catch (_a) {
                    console.warn(`Failed to set default viewer ${overrides[ft.name]} for file type ${ft.name}`);
                }
            }
        };
        // Fetch the initial state of the settings.
        Promise.all([settingRegistry.load(docManagerPluginId), app.restored])
            .then(([settings]) => {
            settings.changed.connect(onSettingsUpdated);
            onSettingsUpdated(settings);
            const onStateChanged = (sender, change) => {
                if ([
                    'autosave',
                    'autosaveInterval',
                    'confirmClosingDocument',
                    'lastModifiedCheckMargin',
                    'renameUntitledFileOnSave'
                ].includes(change.name) &&
                    settings.get(change.name).composite !== change.newValue) {
                    settings.set(change.name, change.newValue).catch(reason => {
                        console.error(`Failed to set the setting '${change.name}':\n${reason}`);
                    });
                }
            };
            docManager.stateChanged.connect(onStateChanged);
        })
            .catch((reason) => {
            console.error(reason.message);
        });
        // Register a fetch transformer for the settings registry,
        // allowing us to dynamically populate a help string with the
        // available document viewers and file types for the default
        // viewer overrides.
        settingRegistry.transform(docManagerPluginId, {
            fetch: plugin => {
                // Get the available file types.
                const fileTypes = Array.from(registry.fileTypes())
                    .map(ft => ft.name)
                    .join('    \n');
                // Get the available widget factories.
                const factories = Array.from(registry.widgetFactories())
                    .map(f => f.name)
                    .join('    \n');
                // Generate the help string.
                const description = trans.__(`Overrides for the default viewers for file types.
Specify a mapping from file type name to document viewer name, for example:

defaultViewers: {
  markdown: "Markdown Preview"
}

If you specify non-existent file types or viewers, or if a viewer cannot
open a given file type, the override will not function.

Available viewers:
%1

Available file types:
%2`, factories, fileTypes);
                const schema = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_9__.JSONExt.deepCopy(plugin.schema);
                schema.properties.defaultViewers.description = description;
                return { ...plugin, schema };
            }
        });
        // If the document registry gains or loses a factory or file type,
        // regenerate the settings description with the available options.
        registry.changed.connect(() => settingRegistry.load(docManagerPluginId, true));
    }
};
/**
 * A plugin for adding a saving status item to the status bar.
 */
const savingStatusPlugin = {
    id: '@jupyterlab/docmanager-extension:saving-status',
    description: 'Adds a saving status indicator.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__.IStatusBar],
    activate: (_, docManager, labShell, translator, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const saving = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.SavingStatus({
            docManager,
            translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator
        });
        // Keep the currently active widget synchronized.
        saving.model.widget = labShell.currentWidget;
        labShell.currentChanged.connect(() => {
            saving.model.widget = labShell.currentWidget;
        });
        statusBar.registerStatusItem(savingStatusPlugin.id, {
            item: saving,
            align: 'middle',
            isActive: () => saving.model !== null && saving.model.status !== null,
            activeStateChanged: saving.model.stateChanged
        });
    }
};
/**
 * A plugin providing a file path widget to the status bar.
 */
const pathStatusPlugin = {
    id: '@jupyterlab/docmanager-extension:path-status',
    description: 'Adds a file path indicator in the status bar.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    optional: [_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_5__.IStatusBar],
    activate: (_, docManager, labShell, statusBar) => {
        if (!statusBar) {
            // Automatically disable if statusbar missing
            return;
        }
        const path = new _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.PathStatus({ docManager });
        // Keep the file path widget up-to-date with the application active widget.
        path.model.widget = labShell.currentWidget;
        labShell.currentChanged.connect(() => {
            path.model.widget = labShell.currentWidget;
        });
        statusBar.registerStatusItem(pathStatusPlugin.id, {
            item: path,
            align: 'right',
            rank: 0
        });
    }
};
/**
 * A plugin providing download commands in the file menu and command palette.
 */
const downloadPlugin = {
    id: '@jupyterlab/docmanager-extension:download',
    description: 'Adds command to download files.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, docManager, translator, palette) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        const { commands, shell } = app;
        const isEnabled = () => {
            const { currentWidget } = shell;
            return !!(currentWidget && docManager.contextForWidget(currentWidget));
        };
        commands.addCommand(CommandIDs.download, {
            label: trans.__('Download'),
            caption: trans.__('Download the file to your computer'),
            isEnabled,
            execute: () => {
                // Checks that shell.currentWidget is valid:
                if (isEnabled()) {
                    const context = docManager.contextForWidget(shell.currentWidget);
                    if (!context) {
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: trans.__('Cannot Download'),
                            body: trans.__('No context found for current widget!'),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                        });
                    }
                    return context.download();
                }
            }
        });
        const category = trans.__('File Operations');
        if (palette) {
            palette.addItem({ command: CommandIDs.download, category });
        }
    }
};
/**
 * A plugin providing open-browser-tab commands.
 *
 * This is its own plugin in case you would like to disable this feature.
 * e.g. jupyter labextension disable @jupyterlab/docmanager-extension:open-browser-tab
 *
 * Note: If disabling this, you may also want to disable:
 * @jupyterlab/filebrowser-extension:open-browser-tab
 */
const openBrowserTabPlugin = {
    id: '@jupyterlab/docmanager-extension:open-browser-tab',
    description: 'Adds command to open a browser tab.',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.IDocumentManager],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    activate: (app, docManager, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        const { commands } = app;
        commands.addCommand(CommandIDs.openBrowserTab, {
            execute: args => {
                const path = typeof args['path'] === 'undefined' ? '' : args['path'];
                if (!path) {
                    return;
                }
                return docManager.services.contents.getDownloadUrl(path).then(url => {
                    const opened = window.open();
                    if (opened) {
                        opened.opener = null;
                        opened.location.href = url;
                    }
                    else {
                        throw new Error('Failed to open new browser tab.');
                    }
                });
            },
            iconClass: args => args['icon'] || '',
            label: () => trans.__('Open in New Browser Tab')
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    manager,
    docManagerPlugin,
    contextsPlugin,
    pathStatusPlugin,
    savingStatusPlugin,
    downloadPlugin,
    openBrowserTabPlugin,
    openerPlugin
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * Toolbar item factory
 */
var ToolbarItems;
(function (ToolbarItems) {
    /**
     * Create save button toolbar item.
     *
     */
    function createSaveButton(commands, fileChanged) {
        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.addCommandToolbarButtonClass)(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_12__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.UseSignal, { signal: fileChanged }, () => (react__WEBPACK_IMPORTED_MODULE_12__.createElement(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.CommandToolbarButtonComponent, { commands: commands, id: CommandIDs.save, label: '', args: { toolbar: true } })))));
    }
    ToolbarItems.createSaveButton = createSaveButton;
})(ToolbarItems || (ToolbarItems = {}));
/* Widget to display the revert to checkpoint confirmation. */
class RevertConfirmWidget extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_11__.Widget {
    /**
     * Construct a new revert confirmation widget.
     */
    constructor(checkpoint, trans, fileType = 'notebook') {
        super({
            node: Private.createRevertConfirmNode(checkpoint, fileType, trans)
        });
    }
}
// Returns the file type for a widget.
function fileType(widget, docManager) {
    if (!widget) {
        return 'File';
    }
    const context = docManager.contextForWidget(widget);
    if (!context) {
        return '';
    }
    const fts = docManager.registry.getFileTypesForPath(context.path);
    return fts.length && fts[0].displayName ? fts[0].displayName : 'File';
}
/**
 * Add the file operations commands to the application's command registry.
 */
function addCommands(app, docManager, widgetOpener, settingRegistry, translator, labShell, palette) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const category = trans.__('File Operations');
    const isEnabled = () => {
        const { currentWidget } = shell;
        return !!(currentWidget && docManager.contextForWidget(currentWidget));
    };
    const isWritable = () => {
        var _a;
        const { currentWidget } = shell;
        if (!currentWidget) {
            return false;
        }
        const context = docManager.contextForWidget(currentWidget);
        return !!((_a = context === null || context === void 0 ? void 0 : context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable);
    };
    // If inside a rich application like JupyterLab, add additional functionality.
    if (labShell) {
        addLabCommands(app, docManager, labShell, widgetOpener, translator);
    }
    commands.addCommand(CommandIDs.deleteFile, {
        label: () => `Delete ${fileType(shell.currentWidget, docManager)}`,
        execute: args => {
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            if (!path) {
                const command = CommandIDs.deleteFile;
                throw new Error(`A non-empty path is required for ${command}.`);
            }
            return docManager.deleteFile(path);
        }
    });
    commands.addCommand(CommandIDs.newUntitled, {
        execute: args => {
            const errorTitle = args['error'] || trans.__('Error');
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            const options = {
                type: args['type'],
                path
            };
            if (args['type'] === 'file') {
                options.ext = args['ext'] || '.txt';
            }
            return docManager.services.contents
                .newUntitled(options)
                .catch(error => (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(errorTitle, error));
        },
        label: args => args['label'] || `New ${args['type']}`
    });
    commands.addCommand(CommandIDs.open, {
        execute: args => {
            const path = typeof args['path'] === 'undefined' ? '' : args['path'];
            const factory = args['factory'] || void 0;
            const kernel = args === null || args === void 0 ? void 0 : args.kernel;
            const options = args['options'] || void 0;
            return docManager.services.contents
                .get(path, { content: false })
                .then(() => docManager.openOrReveal(path, factory, kernel, options));
        },
        iconClass: args => args['icon'] || '',
        label: args => {
            var _a;
            return ((_a = (args['label'] || args['factory'])) !== null && _a !== void 0 ? _a : trans.__('Open the provided `path`.'));
        },
        mnemonic: args => args['mnemonic'] || -1
    });
    commands.addCommand(CommandIDs.reload, {
        label: () => trans.__('Reload %1 from Disk', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Reload contents from disk'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (!isEnabled()) {
                return;
            }
            const context = docManager.contextForWidget(shell.currentWidget);
            const type = fileType(shell.currentWidget, docManager);
            if (!context) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Cannot Reload'),
                    body: trans.__('No context found for current widget!'),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                });
            }
            if (context.model.dirty) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Reload %1 from Disk', type),
                    body: trans.__('Are you sure you want to reload the %1 from the disk?', type),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Reload') })
                    ]
                }).then(result => {
                    if (result.button.accept && !context.isDisposed) {
                        return context.revert();
                    }
                });
            }
            else {
                if (!context.isDisposed) {
                    return context.revert();
                }
            }
        }
    });
    commands.addCommand(CommandIDs.restoreCheckpoint, {
        label: () => trans.__('Revert %1 to Checkpoint…', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Revert contents to previous checkpoint'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (!isEnabled()) {
                return;
            }
            const context = docManager.contextForWidget(shell.currentWidget);
            if (!context) {
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Cannot Revert'),
                    body: trans.__('No context found for current widget!'),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                });
            }
            return context.listCheckpoints().then(async (checkpoints) => {
                const type = fileType(shell.currentWidget, docManager);
                if (checkpoints.length < 1) {
                    await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)(trans.__('No checkpoints'), trans.__('No checkpoints are available for this %1.', type));
                    return;
                }
                const targetCheckpoint = checkpoints.length === 1
                    ? checkpoints[0]
                    : await Private.getTargetCheckpoint(checkpoints.reverse(), trans);
                if (!targetCheckpoint) {
                    return;
                }
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Revert %1 to checkpoint', type),
                    body: new RevertConfirmWidget(targetCheckpoint, trans, type),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({
                            label: trans.__('Revert'),
                            ariaLabel: trans.__('Revert to Checkpoint')
                        })
                    ]
                }).then(result => {
                    if (context.isDisposed) {
                        return;
                    }
                    if (result.button.accept) {
                        if (context.model.readOnly) {
                            return context.revert();
                        }
                        return context
                            .restoreCheckpoint(targetCheckpoint.id)
                            .then(() => context.revert());
                    }
                });
            });
        }
    });
    const caption = () => {
        if (shell.currentWidget) {
            const context = docManager.contextForWidget(shell.currentWidget);
            if (context === null || context === void 0 ? void 0 : context.model.collaborative) {
                return trans.__('In collaborative mode, the document is saved automatically after every change');
            }
            if (!isWritable()) {
                return trans.__(`document is permissioned readonly; "save" is disabled, use "save as..." instead`);
            }
        }
        return trans.__('Save and create checkpoint');
    };
    const saveInProgress = new WeakSet();
    commands.addCommand(CommandIDs.save, {
        label: () => trans.__('Save %1', fileType(shell.currentWidget, docManager)),
        caption,
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.saveIcon : undefined),
        isEnabled: isWritable,
        execute: async () => {
            var _a, _b, _c;
            // Checks that shell.currentWidget is valid:
            const widget = shell.currentWidget;
            const context = docManager.contextForWidget(widget);
            if (isEnabled()) {
                if (!context) {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: trans.__('Cannot Save'),
                        body: trans.__('No context found for current widget!'),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                    });
                }
                else {
                    if (saveInProgress.has(context)) {
                        return;
                    }
                    if (context.model.readOnly) {
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title: trans.__('Cannot Save'),
                            body: trans.__('Document is read-only'),
                            buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                        });
                    }
                    saveInProgress.add(context);
                    const oldName = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.basename((_b = (_a = context.contentsModel) === null || _a === void 0 ? void 0 : _a.path) !== null && _b !== void 0 ? _b : '');
                    let newName = oldName;
                    if (docManager.renameUntitledFileOnSave &&
                        widget.isUntitled === true) {
                        const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getText({
                            title: trans.__('Rename file'),
                            okLabel: trans.__('Rename'),
                            placeholder: trans.__('File name'),
                            text: oldName,
                            selectionRange: oldName.length - _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.extname(oldName).length,
                            checkbox: {
                                label: trans.__('Do not ask me again.'),
                                caption: trans.__('If checked, you will not be asked to rename future untitled files when saving them.')
                            }
                        });
                        if (result.button.accept) {
                            newName = (_c = result.value) !== null && _c !== void 0 ? _c : oldName;
                            widget.isUntitled = false;
                            if (typeof result.isChecked === 'boolean') {
                                const currentSetting = (await settingRegistry.get(docManagerPluginId, 'renameUntitledFileOnSave')).composite;
                                if (result.isChecked === currentSetting) {
                                    settingRegistry
                                        .set(docManagerPluginId, 'renameUntitledFileOnSave', !result.isChecked)
                                        .catch(reason => {
                                        console.error(`Fail to set 'renameUntitledFileOnSave:\n${reason}`);
                                    });
                                }
                            }
                        }
                    }
                    try {
                        await context.save();
                        if (!(widget === null || widget === void 0 ? void 0 : widget.isDisposed)) {
                            return context.createCheckpoint();
                        }
                    }
                    catch (err) {
                        // If the save was canceled by user-action, do nothing.
                        if (err.name === 'ModalCancelError') {
                            return;
                        }
                        throw err;
                    }
                    finally {
                        saveInProgress.delete(context);
                        if (newName !== oldName) {
                            await context.rename(newName);
                        }
                    }
                }
            }
        }
    });
    commands.addCommand(CommandIDs.saveAll, {
        label: () => trans.__('Save All'),
        caption: trans.__('Save all open documents'),
        isEnabled: () => {
            return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_8__.some)(shell.widgets('main'), w => { var _a, _b, _c; return (_c = (_b = (_a = docManager.contextForWidget(w)) === null || _a === void 0 ? void 0 : _a.contentsModel) === null || _b === void 0 ? void 0 : _b.writable) !== null && _c !== void 0 ? _c : false; });
        },
        execute: () => {
            var _a;
            const promises = [];
            const paths = new Set(); // Cache so we don't double save files.
            for (const widget of shell.widgets('main')) {
                const context = docManager.contextForWidget(widget);
                if (context && !paths.has(context.path)) {
                    if ((_a = context.contentsModel) === null || _a === void 0 ? void 0 : _a.writable) {
                        paths.add(context.path);
                        promises.push(context.save());
                    }
                    else {
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Notification.warning(trans.__(`%1 is permissioned as readonly. Use "save as..." instead.`, context.path), { autoClose: 5000 });
                    }
                }
            }
            return Promise.all(promises);
        }
    });
    commands.addCommand(CommandIDs.saveAs, {
        label: () => trans.__('Save %1 As…', fileType(shell.currentWidget, docManager)),
        caption: trans.__('Save with new path'),
        isEnabled,
        execute: () => {
            // Checks that shell.currentWidget is valid:
            if (isEnabled()) {
                const context = docManager.contextForWidget(shell.currentWidget);
                if (!context) {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                        title: trans.__('Cannot Save'),
                        body: trans.__('No context found for current widget!'),
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton()]
                    });
                }
                const onChange = (sender, args) => {
                    if (args.type === 'save' &&
                        args.newValue &&
                        args.newValue.path !== context.path) {
                        void docManager.closeFile(context.path);
                        void commands.execute(CommandIDs.open, {
                            path: args.newValue.path
                        });
                    }
                };
                docManager.services.contents.fileChanged.connect(onChange);
                context
                    .saveAs()
                    .finally(() => docManager.services.contents.fileChanged.disconnect(onChange));
            }
        }
    });
    commands.addCommand(CommandIDs.toggleAutosave, {
        label: trans.__('Autosave Documents'),
        isToggled: () => docManager.autosave,
        execute: () => {
            const value = !docManager.autosave;
            const key = 'autosave';
            return settingRegistry
                .set(docManagerPluginId, key, value)
                .catch((reason) => {
                console.error(`Failed to set ${docManagerPluginId}:${key} - ${reason.message}`);
            });
        }
    });
    if (palette) {
        [
            CommandIDs.reload,
            CommandIDs.restoreCheckpoint,
            CommandIDs.save,
            CommandIDs.saveAs,
            CommandIDs.toggleAutosave,
            CommandIDs.duplicate
        ].forEach(command => {
            palette.addItem({ command, category });
        });
    }
}
function addLabCommands(app, docManager, labShell, widgetOpener, translator) {
    const trans = translator.load('jupyterlab');
    const { commands } = app;
    // Returns the doc widget associated with the most recent contextmenu event.
    const contextMenuWidget = () => {
        var _a;
        const pathRe = /[Pp]ath:\s?(.*)\n?/;
        const test = (node) => { var _a; return !!((_a = node['title']) === null || _a === void 0 ? void 0 : _a.match(pathRe)); };
        const node = app.contextMenuHitTest(test);
        const pathMatch = node === null || node === void 0 ? void 0 : node['title'].match(pathRe);
        return ((_a = (pathMatch && docManager.findWidget(pathMatch[1], null))) !== null && _a !== void 0 ? _a : 
        // Fall back to active doc widget if path cannot be obtained from event.
        labShell.currentWidget);
    };
    // Returns `true` if the current widget has a document context.
    const isEnabled = () => {
        const { currentWidget } = labShell;
        return !!(currentWidget && docManager.contextForWidget(currentWidget));
    };
    commands.addCommand(CommandIDs.clone, {
        label: () => trans.__('New View for %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: args => {
            const widget = contextMenuWidget();
            const options = args['options'] || {
                mode: 'split-right'
            };
            if (!widget) {
                return;
            }
            // Clone the widget.
            const child = docManager.cloneWidget(widget);
            if (child) {
                widgetOpener.open(child, options);
            }
        }
    });
    commands.addCommand(CommandIDs.rename, {
        label: () => {
            let t = fileType(contextMenuWidget(), docManager);
            if (t) {
                t = ' ' + t;
            }
            return trans.__('Rename%1…', t);
        },
        isEnabled,
        execute: () => {
            // Implies contextMenuWidget() !== null
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                return (0,_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_3__.renameDialog)(docManager, context);
            }
        }
    });
    commands.addCommand(CommandIDs.duplicate, {
        label: () => trans.__('Duplicate %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: () => {
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                if (!context) {
                    return;
                }
                return docManager.duplicate(context.path);
            }
        }
    });
    commands.addCommand(CommandIDs.del, {
        label: () => trans.__('Delete %1', fileType(contextMenuWidget(), docManager)),
        isEnabled,
        execute: async () => {
            // Implies contextMenuWidget() !== null
            if (isEnabled()) {
                const context = docManager.contextForWidget(contextMenuWidget());
                if (!context) {
                    return;
                }
                const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title: trans.__('Delete'),
                    body: trans.__('Are you sure you want to delete %1', context.path),
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton(),
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Delete') })
                    ]
                });
                if (result.button.accept) {
                    await app.commands.execute('docmanager:delete-file', {
                        path: context.path
                    });
                }
            }
        }
    });
    commands.addCommand(CommandIDs.showInFileBrowser, {
        label: () => trans.__('Show in File Browser'),
        isEnabled,
        execute: async () => {
            const widget = contextMenuWidget();
            const context = widget && docManager.contextForWidget(widget);
            if (!context) {
                return;
            }
            // 'activate' is needed if this command is selected in the "open tabs" sidebar
            await commands.execute('filebrowser:activate', { path: context.path });
            await commands.execute('filebrowser:go-to-path', { path: context.path });
        }
    });
}
/**
 * Handle dirty state for a context.
 */
function handleContext(status, context) {
    let disposable = null;
    const onStateChanged = (sender, args) => {
        if (args.name === 'dirty') {
            if (args.newValue === true) {
                if (!disposable) {
                    disposable = status.setDirty();
                }
            }
            else if (disposable) {
                disposable.dispose();
                disposable = null;
            }
        }
    };
    void context.ready.then(() => {
        context.model.stateChanged.connect(onStateChanged);
        if (context.model.dirty) {
            disposable = status.setDirty();
        }
    });
    context.disposed.connect(() => {
        if (disposable) {
            disposable.dispose();
        }
    });
}
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * A counter for unique IDs.
     */
    Private.id = 0;
    function createRevertConfirmNode(checkpoint, fileType, trans) {
        const body = document.createElement('div');
        const confirmMessage = document.createElement('p');
        const confirmText = document.createTextNode(trans.__('Are you sure you want to revert the %1 to checkpoint? ', fileType));
        const cannotUndoText = document.createElement('strong');
        cannotUndoText.textContent = trans.__('This cannot be undone.');
        confirmMessage.appendChild(confirmText);
        confirmMessage.appendChild(cannotUndoText);
        const lastCheckpointMessage = document.createElement('p');
        const lastCheckpointText = document.createTextNode(trans.__('The checkpoint was last updated at: '));
        const lastCheckpointDate = document.createElement('p');
        const date = new Date(checkpoint.last_modified);
        lastCheckpointDate.style.textAlign = 'center';
        lastCheckpointDate.textContent =
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.format(date) + ' (' + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.formatHuman(date) + ')';
        lastCheckpointMessage.appendChild(lastCheckpointText);
        lastCheckpointMessage.appendChild(lastCheckpointDate);
        body.appendChild(confirmMessage);
        body.appendChild(lastCheckpointMessage);
        return body;
    }
    Private.createRevertConfirmNode = createRevertConfirmNode;
    /**
     * Ask user for a checkpoint to revert to.
     */
    async function getTargetCheckpoint(checkpoints, trans) {
        // the id could be too long to show so use the index instead
        const indexSeparator = '.';
        const items = checkpoints.map((checkpoint, index) => {
            const isoDate = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.format(checkpoint.last_modified);
            const humanDate = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.Time.formatHuman(checkpoint.last_modified);
            return `${index}${indexSeparator} ${isoDate} (${humanDate})`;
        });
        const selectedItem = (await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getItem({
            items: items,
            title: trans.__('Choose a checkpoint')
        })).value;
        if (!selectedItem) {
            return;
        }
        const selectedIndex = selectedItem.split(indexSeparator, 1)[0];
        return checkpoints[parseInt(selectedIndex, 10)];
    }
    Private.getTargetCheckpoint = getTargetCheckpoint;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZG9jbWFuYWdlci1leHRlbnNpb25fbGliX2luZGV4X2pzLmQzNzA0OGU0ZjJlNTE3NTAyMzU3LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFROEI7QUFjSDtBQUNzQztBQVFwQztBQUcrQjtBQUNaO0FBS2xCO0FBQ29CO0FBQ1o7QUFFRztBQUVRO0FBQ1g7QUFDVjtBQUUvQjs7R0FFRztBQUNILElBQVUsVUFBVSxDQWdDbkI7QUFoQ0QsV0FBVSxVQUFVO0lBQ0wsZ0JBQUssR0FBRyxrQkFBa0IsQ0FBQztJQUUzQixxQkFBVSxHQUFHLHdCQUF3QixDQUFDO0lBRXRDLHNCQUFXLEdBQUcseUJBQXlCLENBQUM7SUFFeEMsZUFBSSxHQUFHLGlCQUFpQixDQUFDO0lBRXpCLHlCQUFjLEdBQUcsNkJBQTZCLENBQUM7SUFFL0MsaUJBQU0sR0FBRyxtQkFBbUIsQ0FBQztJQUU3QixpQkFBTSxHQUFHLG1CQUFtQixDQUFDO0lBRTdCLGNBQUcsR0FBRyxtQkFBbUIsQ0FBQztJQUUxQixvQkFBUyxHQUFHLHNCQUFzQixDQUFDO0lBRW5DLDRCQUFpQixHQUFHLCtCQUErQixDQUFDO0lBRXBELGVBQUksR0FBRyxpQkFBaUIsQ0FBQztJQUV6QixrQkFBTyxHQUFHLHFCQUFxQixDQUFDO0lBRWhDLGlCQUFNLEdBQUcsb0JBQW9CLENBQUM7SUFFOUIsbUJBQVEsR0FBRyxxQkFBcUIsQ0FBQztJQUVqQyx5QkFBYyxHQUFHLDRCQUE0QixDQUFDO0lBRTlDLDRCQUFpQixHQUFHLGlDQUFpQyxDQUFDO0FBQ3JFLENBQUMsRUFoQ1MsVUFBVSxLQUFWLFVBQVUsUUFnQ25CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLGtCQUFrQixHQUFHLHlDQUF5QyxDQUFDO0FBRXJFOzs7R0FHRztBQUNILE1BQU0sWUFBWSxHQUFpRDtJQUNqRSxFQUFFLEVBQUUs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WUFDakIsT0FBTztTQUNSO1FBQ0QsTUFBTSxhQUFhLEdBQUcsWUFBWSxDQUFDLEtBQUssQ0FBQyxjQUFjLEVBQUUsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7UUFDL0QsT0FBTyxXQUFXLENBQUMsUUFBUSxDQUFDLGFBQWEsRUFBRSxFQUFFLENBQUMsQ0FBQyxDQUFDO0lBQ2xELENBQUM7SUF4QnFCLDJCQUFtQixzQkF3QnhDO0FBQ0gsQ0FBQyxFQXZFUyxPQUFPLEtBQVAsT0FBTyxRQXVFaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jbWFuYWdlci1leHRlbnNpb24vc3JjL2luZGV4LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBkb2NtYW5hZ2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxhYlN0YXR1cyxcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW4sXG4gIEp1cHl0ZXJMYWJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgYWRkQ29tbWFuZFRvb2xiYXJCdXR0b25DbGFzcyxcbiAgQ29tbWFuZFRvb2xiYXJCdXR0b25Db21wb25lbnQsXG4gIERpYWxvZyxcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBJbnB1dERpYWxvZyxcbiAgSVNlc3Npb25Db250ZXh0RGlhbG9ncyxcbiAgTm90aWZpY2F0aW9uLFxuICBSZWFjdFdpZGdldCxcbiAgU2Vzc2lvbkNvbnRleHREaWFsb2dzLFxuICBzaG93RGlhbG9nLFxuICBzaG93RXJyb3JNZXNzYWdlLFxuICBVc2VTaWduYWxcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSUNoYW5nZWRBcmdzLCBQYXRoRXh0LCBUaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIERvY3VtZW50TWFuYWdlcixcbiAgSURvY3VtZW50TWFuYWdlcixcbiAgSURvY3VtZW50V2lkZ2V0T3BlbmVyLFxuICBQYXRoU3RhdHVzLFxuICByZW5hbWVEaWFsb2csXG4gIFNhdmluZ1N0YXR1c1xufSBmcm9tICdAanVweXRlcmxhYi9kb2NtYW5hZ2VyJztcbmltcG9ydCB7IERvY3VtZW50UmVnaXN0cnksIElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IENvbnRlbnRzLCBLZXJuZWwgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElTdGF0dXNCYXIgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0dXNiYXInO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBzYXZlSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgc29tZSB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgSlNPTkV4dCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIGRvY3VtZW50IG1hbmFnZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjbG9uZSA9ICdkb2NtYW5hZ2VyOmNsb25lJztcblxuICBleHBvcnQgY29uc3QgZGVsZXRlRmlsZSA9ICdkb2NtYW5hZ2VyOmRlbGV0ZS1maWxlJztcblxuICBleHBvcnQgY29uc3QgbmV3VW50aXRsZWQgPSAnZG9jbWFuYWdlcjpuZXctdW50aXRsZWQnO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuID0gJ2RvY21hbmFnZXI6b3Blbic7XG5cbiAgZXhwb3J0IGNvbnN0IG9wZW5Ccm93c2VyVGFiID0gJ2RvY21hbmFnZXI6b3Blbi1icm93c2VyLXRhYic7XG5cbiAgZXhwb3J0IGNvbnN0IHJlbG9hZCA9ICdkb2NtYW5hZ2VyOnJlbG9hZCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlbmFtZSA9ICdkb2NtYW5hZ2VyOnJlbmFtZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGRlbCA9ICdkb2NtYW5hZ2VyOmRlbGV0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGR1cGxpY2F0ZSA9ICdkb2NtYW5hZ2VyOmR1cGxpY2F0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IHJlc3RvcmVDaGVja3BvaW50ID0gJ2RvY21hbmFnZXI6cmVzdG9yZS1jaGVja3BvaW50JztcblxuICBleHBvcnQgY29uc3Qgc2F2ZSA9ICdkb2NtYW5hZ2VyOnNhdmUnO1xuXG4gIGV4cG9ydCBjb25zdCBzYXZlQWxsID0gJ2RvY21hbmFnZXI6c2F2ZS1hbGwnO1xuXG4gIGV4cG9ydCBjb25zdCBzYXZlQXMgPSAnZG9jbWFuYWdlcjpzYXZlLWFzJztcblxuICBleHBvcnQgY29uc3QgZG93bmxvYWQgPSAnZG9jbWFuYWdlcjpkb3dubG9hZCc7XG5cbiAgZXhwb3J0IGNvbnN0IHRvZ2dsZUF1dG9zYXZlID0gJ2RvY21hbmFnZXI6dG9nZ2xlLWF1dG9zYXZlJztcblxuICBleHBvcnQgY29uc3Qgc2hvd0luRmlsZUJyb3dzZXIgPSAnZG9jbWFuYWdlcjpzaG93LWluLWZpbGUtYnJvd3Nlcic7XG59XG5cbi8qKlxuICogVGhlIGlkIG9mIHRoZSBkb2N1bWVudCBtYW5hZ2VyIHBsdWdpbi5cbiAqL1xuY29uc3QgZG9jTWFuYWdlclBsdWdpbklkID0gJ0BqdXB5dGVybGFiL2RvY21hbmFnZXItZXh0ZW5zaW9uOnBsdWdpbic7XG5cbi8qKlxuICogQSBwbHVnaW4gdG8gb3BlbiBkb2N1bWVudHMgaW4gdGhlIG1haW4gYXJlYS5cbiAqXG4gKi9cbmNvbnN0IG9wZW5lclBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElEb2N1bWVudFdpZGdldE9wZW5lcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlci1leHRlbnNpb246b3BlbmVyJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgd2lkZ2V0IG9wZW5lci4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJRG9jdW1lbnRXaWRnZXRPcGVuZXIsXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQpID0+IHtcbiAgICBjb25zdCB7IHNoZWxsIH0gPSBhcHA7XG4gICAgcmV0dXJuIG5ldyAoY2xhc3Mge1xuICAgICAgb3Blbih3aWRnZXQ6IElEb2N1bWVudFdpZGdldCwgb3B0aW9ucz86IERvY3VtZW50UmVnaXN0cnkuSU9wZW5PcHRpb25zKSB7XG4gICAgICAgIGlmICghd2lkZ2V0LmlkKSB7XG4gICAgICAgICAgd2lkZ2V0LmlkID0gYGRvY3VtZW50LW1hbmFnZXItJHsrK1ByaXZhdGUuaWR9YDtcbiAgICAgICAgfVxuICAgICAgICB3aWRnZXQudGl0bGUuZGF0YXNldCA9IHtcbiAgICAgICAgICB0eXBlOiAnZG9jdW1lbnQtdGl0bGUnLFxuICAgICAgICAgIC4uLndpZGdldC50aXRsZS5kYXRhc2V0XG4gICAgICAgIH07XG4gICAgICAgIGlmICghd2lkZ2V0LmlzQXR0YWNoZWQpIHtcbiAgICAgICAgICBzaGVsbC5hZGQod2lkZ2V0LCAnbWFpbicsIG9wdGlvbnMgfHwge30pO1xuICAgICAgICB9XG4gICAgICAgIHNoZWxsLmFjdGl2YXRlQnlJZCh3aWRnZXQuaWQpO1xuICAgICAgICB0aGlzLl9vcGVuZWQuZW1pdCh3aWRnZXQpO1xuICAgICAgfVxuXG4gICAgICBnZXQgb3BlbmVkKCkge1xuICAgICAgICByZXR1cm4gdGhpcy5fb3BlbmVkO1xuICAgICAgfVxuXG4gICAgICBwcml2YXRlIF9vcGVuZWQgPSBuZXcgU2lnbmFsPHRoaXMsIElEb2N1bWVudFdpZGdldD4odGhpcyk7XG4gICAgfSkoKTtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0byBoYW5kbGUgZGlydHkgc3RhdGVzIGZvciBvcGVuIGRvY3VtZW50cy5cbiAqL1xuY29uc3QgY29udGV4dHNQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kb2NtYW5hZ2VyLWV4dGVuc2lvbjpjb250ZXh0cycsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0aGUgaGFuZGxpbmcgb2Ygb3BlbmVkIGRvY3VtZW50cyBkaXJ0eSBzdGF0ZS4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSURvY3VtZW50TWFuYWdlciwgSURvY3VtZW50V2lkZ2V0T3BlbmVyXSxcbiAgb3B0aW9uYWw6IFtJTGFiU3RhdHVzXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICAgIHdpZGdldE9wZW5lcjogSURvY3VtZW50V2lkZ2V0T3BlbmVyLFxuICAgIHN0YXR1czogSUxhYlN0YXR1c1xuICApID0+IHtcbiAgICBjb25zdCBjb250ZXh0cyA9IG5ldyBXZWFrU2V0PERvY3VtZW50UmVnaXN0cnkuQ29udGV4dD4oKTtcbiAgICB3aWRnZXRPcGVuZXIub3BlbmVkLmNvbm5lY3QoKF8sIHdpZGdldCkgPT4ge1xuICAgICAgLy8gSGFuZGxlIGRpcnR5IHN0YXRlIGZvciBvcGVuIGRvY3VtZW50cy5cbiAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQod2lkZ2V0KTtcbiAgICAgIGlmIChjb250ZXh0ICYmICFjb250ZXh0cy5oYXMoY29udGV4dCkpIHtcbiAgICAgICAgaWYgKHN0YXR1cykge1xuICAgICAgICAgIGhhbmRsZUNvbnRleHQoc3RhdHVzLCBjb250ZXh0KTtcbiAgICAgICAgfVxuICAgICAgICBjb250ZXh0cy5hZGQoY29udGV4dCk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIHRoZSBkZWZhdWx0IGRvY3VtZW50IG1hbmFnZXIuXG4gKi9cbmNvbnN0IG1hbmFnZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJRG9jdW1lbnRNYW5hZ2VyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kb2NtYW5hZ2VyLWV4dGVuc2lvbjptYW5hZ2VyJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgZG9jdW1lbnQgbWFuYWdlci4nLFxuICBwcm92aWRlczogSURvY3VtZW50TWFuYWdlcixcbiAgcmVxdWlyZXM6IFtJRG9jdW1lbnRXaWRnZXRPcGVuZXJdLFxuICBvcHRpb25hbDogW0lUcmFuc2xhdG9yLCBJTGFiU3RhdHVzLCBJU2Vzc2lvbkNvbnRleHREaWFsb2dzLCBKdXB5dGVyTGFiLklJbmZvXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB3aWRnZXRPcGVuZXI6IElEb2N1bWVudFdpZGdldE9wZW5lcixcbiAgICB0cmFuc2xhdG9yXzogSVRyYW5zbGF0b3IgfCBudWxsLFxuICAgIHN0YXR1czogSUxhYlN0YXR1cyB8IG51bGwsXG4gICAgc2Vzc2lvbkRpYWxvZ3NfOiBJU2Vzc2lvbkNvbnRleHREaWFsb2dzIHwgbnVsbCxcbiAgICBpbmZvOiBKdXB5dGVyTGFiLklJbmZvIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB7IHNlcnZpY2VNYW5hZ2VyOiBtYW5hZ2VyLCBkb2NSZWdpc3RyeTogcmVnaXN0cnkgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFuc2xhdG9yID0gdHJhbnNsYXRvcl8gPz8gbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3Qgc2Vzc2lvbkRpYWxvZ3MgPVxuICAgICAgc2Vzc2lvbkRpYWxvZ3NfID8/IG5ldyBTZXNzaW9uQ29udGV4dERpYWxvZ3MoeyB0cmFuc2xhdG9yIH0pO1xuICAgIGNvbnN0IHdoZW4gPSBhcHAucmVzdG9yZWQudGhlbigoKSA9PiB2b2lkIDApO1xuXG4gICAgY29uc3QgZG9jTWFuYWdlciA9IG5ldyBEb2N1bWVudE1hbmFnZXIoe1xuICAgICAgcmVnaXN0cnksXG4gICAgICBtYW5hZ2VyLFxuICAgICAgb3BlbmVyOiB3aWRnZXRPcGVuZXIsXG4gICAgICB3aGVuLFxuICAgICAgc2V0QnVzeTogKHN0YXR1cyAmJiAoKCkgPT4gc3RhdHVzLnNldEJ1c3koKSkpID8/IHVuZGVmaW5lZCxcbiAgICAgIHNlc3Npb25EaWFsb2dzLFxuICAgICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvcixcbiAgICAgIGlzQ29ubmVjdGVkQ2FsbGJhY2s6ICgpID0+IHtcbiAgICAgICAgaWYgKGluZm8pIHtcbiAgICAgICAgICByZXR1cm4gaW5mby5pc0Nvbm5lY3RlZDtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHJldHVybiBkb2NNYW5hZ2VyO1xuICB9XG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGRvY3VtZW50IG1hbmFnZXIgcHJvdmlkZXIgY29tbWFuZHMgYW5kIHNldHRpbmdzLlxuICovXG5jb25zdCBkb2NNYW5hZ2VyUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiBkb2NNYW5hZ2VyUGx1Z2luSWQsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyBjb21tYW5kcyBhbmQgc2V0dGluZ3MgdG8gdGhlIGRvY3VtZW50IG1hbmFnZXIuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lEb2N1bWVudE1hbmFnZXIsIElEb2N1bWVudFdpZGdldE9wZW5lciwgSVNldHRpbmdSZWdpc3RyeV0sXG4gIG9wdGlvbmFsOiBbSVRyYW5zbGF0b3IsIElDb21tYW5kUGFsZXR0ZSwgSUxhYlNoZWxsXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICAgIHdpZGdldE9wZW5lcjogSURvY3VtZW50V2lkZ2V0T3BlbmVyLFxuICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvciB8IG51bGwsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbFxuICApOiB2b2lkID0+IHtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHJlZ2lzdHJ5ID0gYXBwLmRvY1JlZ2lzdHJ5O1xuXG4gICAgLy8gUmVnaXN0ZXIgdGhlIGZpbGUgb3BlcmF0aW9ucyBjb21tYW5kcy5cbiAgICBhZGRDb21tYW5kcyhcbiAgICAgIGFwcCxcbiAgICAgIGRvY01hbmFnZXIsXG4gICAgICB3aWRnZXRPcGVuZXIsXG4gICAgICBzZXR0aW5nUmVnaXN0cnksXG4gICAgICB0cmFuc2xhdG9yLFxuICAgICAgbGFiU2hlbGwsXG4gICAgICBwYWxldHRlXG4gICAgKTtcblxuICAgIC8vIEtlZXAgdXAgdG8gZGF0ZSB3aXRoIHRoZSBzZXR0aW5ncyByZWdpc3RyeS5cbiAgICBjb25zdCBvblNldHRpbmdzVXBkYXRlZCA9IChzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpID0+IHtcbiAgICAgIC8vIEhhbmRsZSB3aGV0aGVyIHRvIGF1dG9zYXZlXG4gICAgICBjb25zdCBhdXRvc2F2ZSA9IHNldHRpbmdzLmdldCgnYXV0b3NhdmUnKS5jb21wb3NpdGUgYXMgYm9vbGVhbiB8IG51bGw7XG4gICAgICBkb2NNYW5hZ2VyLmF1dG9zYXZlID1cbiAgICAgICAgYXV0b3NhdmUgPT09IHRydWUgfHwgYXV0b3NhdmUgPT09IGZhbHNlID8gYXV0b3NhdmUgOiB0cnVlO1xuICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMudG9nZ2xlQXV0b3NhdmUpO1xuXG4gICAgICBjb25zdCBjb25maXJtQ2xvc2luZ0RvY3VtZW50ID0gc2V0dGluZ3MuZ2V0KCdjb25maXJtQ2xvc2luZ0RvY3VtZW50JylcbiAgICAgICAgLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgZG9jTWFuYWdlci5jb25maXJtQ2xvc2luZ0RvY3VtZW50ID0gY29uZmlybUNsb3NpbmdEb2N1bWVudCA/PyB0cnVlO1xuXG4gICAgICAvLyBIYW5kbGUgYXV0b3NhdmUgaW50ZXJ2YWxcbiAgICAgIGNvbnN0IGF1dG9zYXZlSW50ZXJ2YWwgPSBzZXR0aW5ncy5nZXQoJ2F1dG9zYXZlSW50ZXJ2YWwnKS5jb21wb3NpdGUgYXNcbiAgICAgICAgfCBudW1iZXJcbiAgICAgICAgfCBudWxsO1xuICAgICAgZG9jTWFuYWdlci5hdXRvc2F2ZUludGVydmFsID0gYXV0b3NhdmVJbnRlcnZhbCB8fCAxMjA7XG5cbiAgICAgIC8vIEhhbmRsZSBsYXN0IG1vZGlmaWVkIHRpbWVzdGFtcCBjaGVjayBtYXJnaW5cbiAgICAgIGNvbnN0IGxhc3RNb2RpZmllZENoZWNrTWFyZ2luID0gc2V0dGluZ3MuZ2V0KCdsYXN0TW9kaWZpZWRDaGVja01hcmdpbicpXG4gICAgICAgIC5jb21wb3NpdGUgYXMgbnVtYmVyIHwgbnVsbDtcbiAgICAgIGRvY01hbmFnZXIubGFzdE1vZGlmaWVkQ2hlY2tNYXJnaW4gPSBsYXN0TW9kaWZpZWRDaGVja01hcmdpbiB8fCA1MDA7XG5cbiAgICAgIGNvbnN0IHJlbmFtZVVudGl0bGVkRmlsZSA9IHNldHRpbmdzLmdldCgncmVuYW1lVW50aXRsZWRGaWxlT25TYXZlJylcbiAgICAgICAgLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgZG9jTWFuYWdlci5yZW5hbWVVbnRpdGxlZEZpbGVPblNhdmUgPSByZW5hbWVVbnRpdGxlZEZpbGUgPz8gdHJ1ZTtcblxuICAgICAgLy8gSGFuZGxlIGRlZmF1bHQgd2lkZ2V0IGZhY3Rvcnkgb3ZlcnJpZGVzLlxuICAgICAgY29uc3QgZGVmYXVsdFZpZXdlcnMgPSBzZXR0aW5ncy5nZXQoJ2RlZmF1bHRWaWV3ZXJzJykuY29tcG9zaXRlIGFzIHtcbiAgICAgICAgW2Z0OiBzdHJpbmddOiBzdHJpbmc7XG4gICAgICB9O1xuICAgICAgY29uc3Qgb3ZlcnJpZGVzOiB7IFtmdDogc3RyaW5nXTogc3RyaW5nIH0gPSB7fTtcbiAgICAgIC8vIEZpbHRlciB0aGUgZGVmYXVsdFZpZXdlcnMgYW5kIGZpbGUgdHlwZXMgZm9yIGV4aXN0aW5nIG9uZXMuXG4gICAgICBPYmplY3Qua2V5cyhkZWZhdWx0Vmlld2VycykuZm9yRWFjaChmdCA9PiB7XG4gICAgICAgIGlmICghcmVnaXN0cnkuZ2V0RmlsZVR5cGUoZnQpKSB7XG4gICAgICAgICAgY29uc29sZS53YXJuKGBGaWxlIFR5cGUgJHtmdH0gbm90IGZvdW5kYCk7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGlmICghcmVnaXN0cnkuZ2V0V2lkZ2V0RmFjdG9yeShkZWZhdWx0Vmlld2Vyc1tmdF0pKSB7XG4gICAgICAgICAgY29uc29sZS53YXJuKGBEb2N1bWVudCB2aWV3ZXIgJHtkZWZhdWx0Vmlld2Vyc1tmdF19IG5vdCBmb3VuZGApO1xuICAgICAgICB9XG4gICAgICAgIG92ZXJyaWRlc1tmdF0gPSBkZWZhdWx0Vmlld2Vyc1tmdF07XG4gICAgICB9KTtcbiAgICAgIC8vIFNldCB0aGUgZGVmYXVsdCBmYWN0b3J5IG92ZXJyaWRlcy4gSWYgbm90IHByb3ZpZGVkLCB0aGlzIGhhcyB0aGVcbiAgICAgIC8vIGVmZmVjdCBvZiB1bnNldHRpbmcgYW55IHByZXZpb3VzIG92ZXJyaWRlcy5cbiAgICAgIGZvciAoY29uc3QgZnQgb2YgcmVnaXN0cnkuZmlsZVR5cGVzKCkpIHtcbiAgICAgICAgdHJ5IHtcbiAgICAgICAgICByZWdpc3RyeS5zZXREZWZhdWx0V2lkZ2V0RmFjdG9yeShmdC5uYW1lLCBvdmVycmlkZXNbZnQubmFtZV0pO1xuICAgICAgICB9IGNhdGNoIHtcbiAgICAgICAgICBjb25zb2xlLndhcm4oXG4gICAgICAgICAgICBgRmFpbGVkIHRvIHNldCBkZWZhdWx0IHZpZXdlciAke292ZXJyaWRlc1tmdC5uYW1lXX0gZm9yIGZpbGUgdHlwZSAke1xuICAgICAgICAgICAgICBmdC5uYW1lXG4gICAgICAgICAgICB9YFxuICAgICAgICAgICk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9O1xuXG4gICAgLy8gRmV0Y2ggdGhlIGluaXRpYWwgc3RhdGUgb2YgdGhlIHNldHRpbmdzLlxuICAgIFByb21pc2UuYWxsKFtzZXR0aW5nUmVnaXN0cnkubG9hZChkb2NNYW5hZ2VyUGx1Z2luSWQpLCBhcHAucmVzdG9yZWRdKVxuICAgICAgLnRoZW4oKFtzZXR0aW5nc10pID0+IHtcbiAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KG9uU2V0dGluZ3NVcGRhdGVkKTtcbiAgICAgICAgb25TZXR0aW5nc1VwZGF0ZWQoc2V0dGluZ3MpO1xuXG4gICAgICAgIGNvbnN0IG9uU3RhdGVDaGFuZ2VkID0gKFxuICAgICAgICAgIHNlbmRlcjogSURvY3VtZW50TWFuYWdlcixcbiAgICAgICAgICBjaGFuZ2U6IElDaGFuZ2VkQXJnczxhbnk+XG4gICAgICAgICk6IHZvaWQgPT4ge1xuICAgICAgICAgIGlmIChcbiAgICAgICAgICAgIFtcbiAgICAgICAgICAgICAgJ2F1dG9zYXZlJyxcbiAgICAgICAgICAgICAgJ2F1dG9zYXZlSW50ZXJ2YWwnLFxuICAgICAgICAgICAgICAnY29uZmlybUNsb3NpbmdEb2N1bWVudCcsXG4gICAgICAgICAgICAgICdsYXN0TW9kaWZpZWRDaGVja01hcmdpbicsXG4gICAgICAgICAgICAgICdyZW5hbWVVbnRpdGxlZEZpbGVPblNhdmUnXG4gICAgICAgICAgICBdLmluY2x1ZGVzKGNoYW5nZS5uYW1lKSAmJlxuICAgICAgICAgICAgc2V0dGluZ3MuZ2V0KGNoYW5nZS5uYW1lKS5jb21wb3NpdGUgIT09IGNoYW5nZS5uZXdWYWx1ZVxuICAgICAgICAgICkge1xuICAgICAgICAgICAgc2V0dGluZ3Muc2V0KGNoYW5nZS5uYW1lLCBjaGFuZ2UubmV3VmFsdWUpLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoXG4gICAgICAgICAgICAgICAgYEZhaWxlZCB0byBzZXQgdGhlIHNldHRpbmcgJyR7Y2hhbmdlLm5hbWV9JzpcXG4ke3JlYXNvbn1gXG4gICAgICAgICAgICAgICk7XG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH07XG4gICAgICAgIGRvY01hbmFnZXIuc3RhdGVDaGFuZ2VkLmNvbm5lY3Qob25TdGF0ZUNoYW5nZWQpO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICBjb25zb2xlLmVycm9yKHJlYXNvbi5tZXNzYWdlKTtcbiAgICAgIH0pO1xuXG4gICAgLy8gUmVnaXN0ZXIgYSBmZXRjaCB0cmFuc2Zvcm1lciBmb3IgdGhlIHNldHRpbmdzIHJlZ2lzdHJ5LFxuICAgIC8vIGFsbG93aW5nIHVzIHRvIGR5bmFtaWNhbGx5IHBvcHVsYXRlIGEgaGVscCBzdHJpbmcgd2l0aCB0aGVcbiAgICAvLyBhdmFpbGFibGUgZG9jdW1lbnQgdmlld2VycyBhbmQgZmlsZSB0eXBlcyBmb3IgdGhlIGRlZmF1bHRcbiAgICAvLyB2aWV3ZXIgb3ZlcnJpZGVzLlxuICAgIHNldHRpbmdSZWdpc3RyeS50cmFuc2Zvcm0oZG9jTWFuYWdlclBsdWdpbklkLCB7XG4gICAgICBmZXRjaDogcGx1Z2luID0+IHtcbiAgICAgICAgLy8gR2V0IHRoZSBhdmFpbGFibGUgZmlsZSB0eXBlcy5cbiAgICAgICAgY29uc3QgZmlsZVR5cGVzID0gQXJyYXkuZnJvbShyZWdpc3RyeS5maWxlVHlwZXMoKSlcbiAgICAgICAgICAubWFwKGZ0ID0+IGZ0Lm5hbWUpXG4gICAgICAgICAgLmpvaW4oJyAgICBcXG4nKTtcbiAgICAgICAgLy8gR2V0IHRoZSBhdmFpbGFibGUgd2lkZ2V0IGZhY3Rvcmllcy5cbiAgICAgICAgY29uc3QgZmFjdG9yaWVzID0gQXJyYXkuZnJvbShyZWdpc3RyeS53aWRnZXRGYWN0b3JpZXMoKSlcbiAgICAgICAgICAubWFwKGYgPT4gZi5uYW1lKVxuICAgICAgICAgIC5qb2luKCcgICAgXFxuJyk7XG4gICAgICAgIC8vIEdlbmVyYXRlIHRoZSBoZWxwIHN0cmluZy5cbiAgICAgICAgY29uc3QgZGVzY3JpcHRpb24gPSB0cmFucy5fXyhcbiAgICAgICAgICBgT3ZlcnJpZGVzIGZvciB0aGUgZGVmYXVsdCB2aWV3ZXJzIGZvciBmaWxlIHR5cGVzLlxuU3BlY2lmeSBhIG1hcHBpbmcgZnJvbSBmaWxlIHR5cGUgbmFtZSB0byBkb2N1bWVudCB2aWV3ZXIgbmFtZSwgZm9yIGV4YW1wbGU6XG5cbmRlZmF1bHRWaWV3ZXJzOiB7XG4gIG1hcmtkb3duOiBcIk1hcmtkb3duIFByZXZpZXdcIlxufVxuXG5JZiB5b3Ugc3BlY2lmeSBub24tZXhpc3RlbnQgZmlsZSB0eXBlcyBvciB2aWV3ZXJzLCBvciBpZiBhIHZpZXdlciBjYW5ub3Rcbm9wZW4gYSBnaXZlbiBmaWxlIHR5cGUsIHRoZSBvdmVycmlkZSB3aWxsIG5vdCBmdW5jdGlvbi5cblxuQXZhaWxhYmxlIHZpZXdlcnM6XG4lMVxuXG5BdmFpbGFibGUgZmlsZSB0eXBlczpcbiUyYCxcbiAgICAgICAgICBmYWN0b3JpZXMsXG4gICAgICAgICAgZmlsZVR5cGVzXG4gICAgICAgICk7XG4gICAgICAgIGNvbnN0IHNjaGVtYSA9IEpTT05FeHQuZGVlcENvcHkocGx1Z2luLnNjaGVtYSk7XG4gICAgICAgIHNjaGVtYS5wcm9wZXJ0aWVzIS5kZWZhdWx0Vmlld2Vycy5kZXNjcmlwdGlvbiA9IGRlc2NyaXB0aW9uO1xuICAgICAgICByZXR1cm4geyAuLi5wbHVnaW4sIHNjaGVtYSB9O1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gSWYgdGhlIGRvY3VtZW50IHJlZ2lzdHJ5IGdhaW5zIG9yIGxvc2VzIGEgZmFjdG9yeSBvciBmaWxlIHR5cGUsXG4gICAgLy8gcmVnZW5lcmF0ZSB0aGUgc2V0dGluZ3MgZGVzY3JpcHRpb24gd2l0aCB0aGUgYXZhaWxhYmxlIG9wdGlvbnMuXG4gICAgcmVnaXN0cnkuY2hhbmdlZC5jb25uZWN0KCgpID0+XG4gICAgICBzZXR0aW5nUmVnaXN0cnkubG9hZChkb2NNYW5hZ2VyUGx1Z2luSWQsIHRydWUpXG4gICAgKTtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiBmb3IgYWRkaW5nIGEgc2F2aW5nIHN0YXR1cyBpdGVtIHRvIHRoZSBzdGF0dXMgYmFyLlxuICovXG5leHBvcnQgY29uc3Qgc2F2aW5nU3RhdHVzUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlci1leHRlbnNpb246c2F2aW5nLXN0YXR1cycsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyBhIHNhdmluZyBzdGF0dXMgaW5kaWNhdG9yLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJRG9jdW1lbnRNYW5hZ2VyLCBJTGFiU2hlbGxdLFxuICBvcHRpb25hbDogW0lUcmFuc2xhdG9yLCBJU3RhdHVzQmFyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBfOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbCxcbiAgICBzdGF0dXNCYXI6IElTdGF0dXNCYXIgfCBudWxsXG4gICkgPT4ge1xuICAgIGlmICghc3RhdHVzQmFyKSB7XG4gICAgICAvLyBBdXRvbWF0aWNhbGx5IGRpc2FibGUgaWYgc3RhdHVzYmFyIG1pc3NpbmdcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3Qgc2F2aW5nID0gbmV3IFNhdmluZ1N0YXR1cyh7XG4gICAgICBkb2NNYW5hZ2VyLFxuICAgICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvclxuICAgIH0pO1xuXG4gICAgLy8gS2VlcCB0aGUgY3VycmVudGx5IGFjdGl2ZSB3aWRnZXQgc3luY2hyb25pemVkLlxuICAgIHNhdmluZy5tb2RlbCEud2lkZ2V0ID0gbGFiU2hlbGwuY3VycmVudFdpZGdldDtcbiAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHNhdmluZy5tb2RlbCEud2lkZ2V0ID0gbGFiU2hlbGwuY3VycmVudFdpZGdldDtcbiAgICB9KTtcblxuICAgIHN0YXR1c0Jhci5yZWdpc3RlclN0YXR1c0l0ZW0oc2F2aW5nU3RhdHVzUGx1Z2luLmlkLCB7XG4gICAgICBpdGVtOiBzYXZpbmcsXG4gICAgICBhbGlnbjogJ21pZGRsZScsXG4gICAgICBpc0FjdGl2ZTogKCkgPT4gc2F2aW5nLm1vZGVsICE9PSBudWxsICYmIHNhdmluZy5tb2RlbC5zdGF0dXMgIT09IG51bGwsXG4gICAgICBhY3RpdmVTdGF0ZUNoYW5nZWQ6IHNhdmluZy5tb2RlbCEuc3RhdGVDaGFuZ2VkXG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIGEgZmlsZSBwYXRoIHdpZGdldCB0byB0aGUgc3RhdHVzIGJhci5cbiAqL1xuZXhwb3J0IGNvbnN0IHBhdGhTdGF0dXNQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kb2NtYW5hZ2VyLWV4dGVuc2lvbjpwYXRoLXN0YXR1cycsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyBhIGZpbGUgcGF0aCBpbmRpY2F0b3IgaW4gdGhlIHN0YXR1cyBiYXIuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lEb2N1bWVudE1hbmFnZXIsIElMYWJTaGVsbF0sXG4gIG9wdGlvbmFsOiBbSVN0YXR1c0Jhcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgXzogSnVweXRlckZyb250RW5kLFxuICAgIGRvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXIsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCxcbiAgICBzdGF0dXNCYXI6IElTdGF0dXNCYXIgfCBudWxsXG4gICkgPT4ge1xuICAgIGlmICghc3RhdHVzQmFyKSB7XG4gICAgICAvLyBBdXRvbWF0aWNhbGx5IGRpc2FibGUgaWYgc3RhdHVzYmFyIG1pc3NpbmdcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgcGF0aCA9IG5ldyBQYXRoU3RhdHVzKHsgZG9jTWFuYWdlciB9KTtcblxuICAgIC8vIEtlZXAgdGhlIGZpbGUgcGF0aCB3aWRnZXQgdXAtdG8tZGF0ZSB3aXRoIHRoZSBhcHBsaWNhdGlvbiBhY3RpdmUgd2lkZ2V0LlxuICAgIHBhdGgubW9kZWwhLndpZGdldCA9IGxhYlNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgbGFiU2hlbGwuY3VycmVudENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICBwYXRoLm1vZGVsIS53aWRnZXQgPSBsYWJTaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgIH0pO1xuXG4gICAgc3RhdHVzQmFyLnJlZ2lzdGVyU3RhdHVzSXRlbShwYXRoU3RhdHVzUGx1Z2luLmlkLCB7XG4gICAgICBpdGVtOiBwYXRoLFxuICAgICAgYWxpZ246ICdyaWdodCcsXG4gICAgICByYW5rOiAwXG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIGRvd25sb2FkIGNvbW1hbmRzIGluIHRoZSBmaWxlIG1lbnUgYW5kIGNvbW1hbmQgcGFsZXR0ZS5cbiAqL1xuZXhwb3J0IGNvbnN0IGRvd25sb2FkUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZG9jbWFuYWdlci1leHRlbnNpb246ZG93bmxvYWQnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgY29tbWFuZCB0byBkb3dubG9hZCBmaWxlcy4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSURvY3VtZW50TWFuYWdlcl0sXG4gIG9wdGlvbmFsOiBbSVRyYW5zbGF0b3IsIElDb21tYW5kUGFsZXR0ZV0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgZG9jTWFuYWdlcjogSURvY3VtZW50TWFuYWdlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvciB8IG51bGwsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9ICh0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgICBjb25zdCBpc0VuYWJsZWQgPSAoKSA9PiB7XG4gICAgICBjb25zdCB7IGN1cnJlbnRXaWRnZXQgfSA9IHNoZWxsO1xuICAgICAgcmV0dXJuICEhKGN1cnJlbnRXaWRnZXQgJiYgZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KGN1cnJlbnRXaWRnZXQpKTtcbiAgICB9O1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kb3dubG9hZCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdEb3dubG9hZCcpLFxuICAgICAgY2FwdGlvbjogdHJhbnMuX18oJ0Rvd25sb2FkIHRoZSBmaWxlIHRvIHlvdXIgY29tcHV0ZXInKSxcbiAgICAgIGlzRW5hYmxlZCxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgLy8gQ2hlY2tzIHRoYXQgc2hlbGwuY3VycmVudFdpZGdldCBpcyB2YWxpZDpcbiAgICAgICAgaWYgKGlzRW5hYmxlZCgpKSB7XG4gICAgICAgICAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldChzaGVsbC5jdXJyZW50V2lkZ2V0ISk7XG4gICAgICAgICAgaWYgKCFjb250ZXh0KSB7XG4gICAgICAgICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnQ2Fubm90IERvd25sb2FkJyksXG4gICAgICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKCdObyBjb250ZXh0IGZvdW5kIGZvciBjdXJyZW50IHdpZGdldCEnKSxcbiAgICAgICAgICAgICAgYnV0dG9uczogW0RpYWxvZy5va0J1dHRvbigpXVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHJldHVybiBjb250ZXh0LmRvd25sb2FkKCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0ZpbGUgT3BlcmF0aW9ucycpO1xuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kOiBDb21tYW5kSURzLmRvd25sb2FkLCBjYXRlZ29yeSB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gcHJvdmlkaW5nIG9wZW4tYnJvd3Nlci10YWIgY29tbWFuZHMuXG4gKlxuICogVGhpcyBpcyBpdHMgb3duIHBsdWdpbiBpbiBjYXNlIHlvdSB3b3VsZCBsaWtlIHRvIGRpc2FibGUgdGhpcyBmZWF0dXJlLlxuICogZS5nLiBqdXB5dGVyIGxhYmV4dGVuc2lvbiBkaXNhYmxlIEBqdXB5dGVybGFiL2RvY21hbmFnZXItZXh0ZW5zaW9uOm9wZW4tYnJvd3Nlci10YWJcbiAqXG4gKiBOb3RlOiBJZiBkaXNhYmxpbmcgdGhpcywgeW91IG1heSBhbHNvIHdhbnQgdG8gZGlzYWJsZTpcbiAqIEBqdXB5dGVybGFiL2ZpbGVicm93c2VyLWV4dGVuc2lvbjpvcGVuLWJyb3dzZXItdGFiXG4gKi9cbmV4cG9ydCBjb25zdCBvcGVuQnJvd3NlclRhYlBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2RvY21hbmFnZXItZXh0ZW5zaW9uOm9wZW4tYnJvd3Nlci10YWInLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgY29tbWFuZCB0byBvcGVuIGEgYnJvd3NlciB0YWIuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lEb2N1bWVudE1hbmFnZXJdLFxuICBvcHRpb25hbDogW0lUcmFuc2xhdG9yXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9ICh0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuQnJvd3NlclRhYiwge1xuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHBhdGggPVxuICAgICAgICAgIHR5cGVvZiBhcmdzWydwYXRoJ10gPT09ICd1bmRlZmluZWQnID8gJycgOiAoYXJnc1sncGF0aCddIGFzIHN0cmluZyk7XG5cbiAgICAgICAgaWYgKCFwYXRoKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIGRvY01hbmFnZXIuc2VydmljZXMuY29udGVudHMuZ2V0RG93bmxvYWRVcmwocGF0aCkudGhlbih1cmwgPT4ge1xuICAgICAgICAgIGNvbnN0IG9wZW5lZCA9IHdpbmRvdy5vcGVuKCk7XG4gICAgICAgICAgaWYgKG9wZW5lZCkge1xuICAgICAgICAgICAgb3BlbmVkLm9wZW5lciA9IG51bGw7XG4gICAgICAgICAgICBvcGVuZWQubG9jYXRpb24uaHJlZiA9IHVybDtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKCdGYWlsZWQgdG8gb3BlbiBuZXcgYnJvd3NlciB0YWIuJyk7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH0sXG4gICAgICBpY29uQ2xhc3M6IGFyZ3MgPT4gKGFyZ3NbJ2ljb24nXSBhcyBzdHJpbmcpIHx8ICcnLFxuICAgICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdPcGVuIGluIE5ldyBCcm93c2VyIFRhYicpXG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIG1hbmFnZXIsXG4gIGRvY01hbmFnZXJQbHVnaW4sXG4gIGNvbnRleHRzUGx1Z2luLFxuICBwYXRoU3RhdHVzUGx1Z2luLFxuICBzYXZpbmdTdGF0dXNQbHVnaW4sXG4gIGRvd25sb2FkUGx1Z2luLFxuICBvcGVuQnJvd3NlclRhYlBsdWdpbixcbiAgb3BlbmVyUGx1Z2luXG5dO1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcblxuLyoqXG4gKiBUb29sYmFyIGl0ZW0gZmFjdG9yeVxuICovXG5leHBvcnQgbmFtZXNwYWNlIFRvb2xiYXJJdGVtcyB7XG4gIC8qKlxuICAgKiBDcmVhdGUgc2F2ZSBidXR0b24gdG9vbGJhciBpdGVtLlxuICAgKlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZVNhdmVCdXR0b24oXG4gICAgY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeSxcbiAgICBmaWxlQ2hhbmdlZDogSVNpZ25hbDxhbnksIE9taXQ8Q29udGVudHMuSU1vZGVsLCAnY29udGVudCc+PlxuICApOiBXaWRnZXQge1xuICAgIHJldHVybiBhZGRDb21tYW5kVG9vbGJhckJ1dHRvbkNsYXNzKFxuICAgICAgUmVhY3RXaWRnZXQuY3JlYXRlKFxuICAgICAgICA8VXNlU2lnbmFsIHNpZ25hbD17ZmlsZUNoYW5nZWR9PlxuICAgICAgICAgIHsoKSA9PiAoXG4gICAgICAgICAgICA8Q29tbWFuZFRvb2xiYXJCdXR0b25Db21wb25lbnRcbiAgICAgICAgICAgICAgY29tbWFuZHM9e2NvbW1hbmRzfVxuICAgICAgICAgICAgICBpZD17Q29tbWFuZElEcy5zYXZlfVxuICAgICAgICAgICAgICBsYWJlbD17Jyd9XG4gICAgICAgICAgICAgIGFyZ3M9e3sgdG9vbGJhcjogdHJ1ZSB9fVxuICAgICAgICAgICAgLz5cbiAgICAgICAgICApfVxuICAgICAgICA8L1VzZVNpZ25hbD5cbiAgICAgIClcbiAgICApO1xuICB9XG59XG5cbi8qIFdpZGdldCB0byBkaXNwbGF5IHRoZSByZXZlcnQgdG8gY2hlY2twb2ludCBjb25maXJtYXRpb24uICovXG5jbGFzcyBSZXZlcnRDb25maXJtV2lkZ2V0IGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyByZXZlcnQgY29uZmlybWF0aW9uIHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKFxuICAgIGNoZWNrcG9pbnQ6IENvbnRlbnRzLklDaGVja3BvaW50TW9kZWwsXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIGZpbGVUeXBlOiBzdHJpbmcgPSAnbm90ZWJvb2snXG4gICkge1xuICAgIHN1cGVyKHtcbiAgICAgIG5vZGU6IFByaXZhdGUuY3JlYXRlUmV2ZXJ0Q29uZmlybU5vZGUoY2hlY2twb2ludCwgZmlsZVR5cGUsIHRyYW5zKVxuICAgIH0pO1xuICB9XG59XG5cbi8vIFJldHVybnMgdGhlIGZpbGUgdHlwZSBmb3IgYSB3aWRnZXQuXG5mdW5jdGlvbiBmaWxlVHlwZSh3aWRnZXQ6IFdpZGdldCB8IG51bGwsIGRvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXIpOiBzdHJpbmcge1xuICBpZiAoIXdpZGdldCkge1xuICAgIHJldHVybiAnRmlsZSc7XG4gIH1cbiAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldCh3aWRnZXQpO1xuICBpZiAoIWNvbnRleHQpIHtcbiAgICByZXR1cm4gJyc7XG4gIH1cbiAgY29uc3QgZnRzID0gZG9jTWFuYWdlci5yZWdpc3RyeS5nZXRGaWxlVHlwZXNGb3JQYXRoKGNvbnRleHQucGF0aCk7XG4gIHJldHVybiBmdHMubGVuZ3RoICYmIGZ0c1swXS5kaXNwbGF5TmFtZSA/IGZ0c1swXS5kaXNwbGF5TmFtZSA6ICdGaWxlJztcbn1cblxuLyoqXG4gKiBBZGQgdGhlIGZpbGUgb3BlcmF0aW9ucyBjb21tYW5kcyB0byB0aGUgYXBwbGljYXRpb24ncyBjb21tYW5kIHJlZ2lzdHJ5LlxuICovXG5mdW5jdGlvbiBhZGRDb21tYW5kcyhcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIGRvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXIsXG4gIHdpZGdldE9wZW5lcjogSURvY3VtZW50V2lkZ2V0T3BlbmVyLFxuICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbCxcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuKTogdm9pZCB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsIH0gPSBhcHA7XG4gIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0ZpbGUgT3BlcmF0aW9ucycpO1xuICBjb25zdCBpc0VuYWJsZWQgPSAoKSA9PiB7XG4gICAgY29uc3QgeyBjdXJyZW50V2lkZ2V0IH0gPSBzaGVsbDtcbiAgICByZXR1cm4gISEoY3VycmVudFdpZGdldCAmJiBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoY3VycmVudFdpZGdldCkpO1xuICB9O1xuXG4gIGNvbnN0IGlzV3JpdGFibGUgPSAoKSA9PiB7XG4gICAgY29uc3QgeyBjdXJyZW50V2lkZ2V0IH0gPSBzaGVsbDtcbiAgICBpZiAoIWN1cnJlbnRXaWRnZXQpIHtcbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9XG4gICAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldChjdXJyZW50V2lkZ2V0KTtcbiAgICByZXR1cm4gISFjb250ZXh0Py5jb250ZW50c01vZGVsPy53cml0YWJsZTtcbiAgfTtcblxuICAvLyBJZiBpbnNpZGUgYSByaWNoIGFwcGxpY2F0aW9uIGxpa2UgSnVweXRlckxhYiwgYWRkIGFkZGl0aW9uYWwgZnVuY3Rpb25hbGl0eS5cbiAgaWYgKGxhYlNoZWxsKSB7XG4gICAgYWRkTGFiQ29tbWFuZHMoYXBwLCBkb2NNYW5hZ2VyLCBsYWJTaGVsbCwgd2lkZ2V0T3BlbmVyLCB0cmFuc2xhdG9yKTtcbiAgfVxuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kZWxldGVGaWxlLCB7XG4gICAgbGFiZWw6ICgpID0+IGBEZWxldGUgJHtmaWxlVHlwZShzaGVsbC5jdXJyZW50V2lkZ2V0LCBkb2NNYW5hZ2VyKX1gLFxuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgcGF0aCA9XG4gICAgICAgIHR5cGVvZiBhcmdzWydwYXRoJ10gPT09ICd1bmRlZmluZWQnID8gJycgOiAoYXJnc1sncGF0aCddIGFzIHN0cmluZyk7XG5cbiAgICAgIGlmICghcGF0aCkge1xuICAgICAgICBjb25zdCBjb21tYW5kID0gQ29tbWFuZElEcy5kZWxldGVGaWxlO1xuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYEEgbm9uLWVtcHR5IHBhdGggaXMgcmVxdWlyZWQgZm9yICR7Y29tbWFuZH0uYCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gZG9jTWFuYWdlci5kZWxldGVGaWxlKHBhdGgpO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm5ld1VudGl0bGVkLCB7XG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBlcnJvclRpdGxlID0gKGFyZ3NbJ2Vycm9yJ10gYXMgc3RyaW5nKSB8fCB0cmFucy5fXygnRXJyb3InKTtcbiAgICAgIGNvbnN0IHBhdGggPVxuICAgICAgICB0eXBlb2YgYXJnc1sncGF0aCddID09PSAndW5kZWZpbmVkJyA/ICcnIDogKGFyZ3NbJ3BhdGgnXSBhcyBzdHJpbmcpO1xuICAgICAgY29uc3Qgb3B0aW9uczogUGFydGlhbDxDb250ZW50cy5JQ3JlYXRlT3B0aW9ucz4gPSB7XG4gICAgICAgIHR5cGU6IGFyZ3NbJ3R5cGUnXSBhcyBDb250ZW50cy5Db250ZW50VHlwZSxcbiAgICAgICAgcGF0aFxuICAgICAgfTtcblxuICAgICAgaWYgKGFyZ3NbJ3R5cGUnXSA9PT0gJ2ZpbGUnKSB7XG4gICAgICAgIG9wdGlvbnMuZXh0ID0gKGFyZ3NbJ2V4dCddIGFzIHN0cmluZykgfHwgJy50eHQnO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gZG9jTWFuYWdlci5zZXJ2aWNlcy5jb250ZW50c1xuICAgICAgICAubmV3VW50aXRsZWQob3B0aW9ucylcbiAgICAgICAgLmNhdGNoKGVycm9yID0+IHNob3dFcnJvck1lc3NhZ2UoZXJyb3JUaXRsZSwgZXJyb3IpKTtcbiAgICB9LFxuICAgIGxhYmVsOiBhcmdzID0+IChhcmdzWydsYWJlbCddIGFzIHN0cmluZykgfHwgYE5ldyAke2FyZ3NbJ3R5cGUnXSBhcyBzdHJpbmd9YFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbiwge1xuICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgY29uc3QgcGF0aCA9XG4gICAgICAgIHR5cGVvZiBhcmdzWydwYXRoJ10gPT09ICd1bmRlZmluZWQnID8gJycgOiAoYXJnc1sncGF0aCddIGFzIHN0cmluZyk7XG4gICAgICBjb25zdCBmYWN0b3J5ID0gKGFyZ3NbJ2ZhY3RvcnknXSBhcyBzdHJpbmcpIHx8IHZvaWQgMDtcbiAgICAgIGNvbnN0IGtlcm5lbCA9IGFyZ3M/Lmtlcm5lbCBhcyB1bmtub3duIGFzIEtlcm5lbC5JTW9kZWwgfCB1bmRlZmluZWQ7XG4gICAgICBjb25zdCBvcHRpb25zID1cbiAgICAgICAgKGFyZ3NbJ29wdGlvbnMnXSBhcyBEb2N1bWVudFJlZ2lzdHJ5LklPcGVuT3B0aW9ucykgfHwgdm9pZCAwO1xuICAgICAgcmV0dXJuIGRvY01hbmFnZXIuc2VydmljZXMuY29udGVudHNcbiAgICAgICAgLmdldChwYXRoLCB7IGNvbnRlbnQ6IGZhbHNlIH0pXG4gICAgICAgIC50aGVuKCgpID0+IGRvY01hbmFnZXIub3Blbk9yUmV2ZWFsKHBhdGgsIGZhY3RvcnksIGtlcm5lbCwgb3B0aW9ucykpO1xuICAgIH0sXG4gICAgaWNvbkNsYXNzOiBhcmdzID0+IChhcmdzWydpY29uJ10gYXMgc3RyaW5nKSB8fCAnJyxcbiAgICBsYWJlbDogYXJncyA9PlxuICAgICAgKChhcmdzWydsYWJlbCddIHx8IGFyZ3NbJ2ZhY3RvcnknXSkgPz9cbiAgICAgICAgdHJhbnMuX18oJ09wZW4gdGhlIHByb3ZpZGVkIGBwYXRoYC4nKSkgYXMgc3RyaW5nLFxuICAgIG1uZW1vbmljOiBhcmdzID0+IChhcmdzWydtbmVtb25pYyddIGFzIG51bWJlcikgfHwgLTFcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlbG9hZCwge1xuICAgIGxhYmVsOiAoKSA9PlxuICAgICAgdHJhbnMuX18oXG4gICAgICAgICdSZWxvYWQgJTEgZnJvbSBEaXNrJyxcbiAgICAgICAgZmlsZVR5cGUoc2hlbGwuY3VycmVudFdpZGdldCwgZG9jTWFuYWdlcilcbiAgICAgICksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ1JlbG9hZCBjb250ZW50cyBmcm9tIGRpc2snKSxcbiAgICBpc0VuYWJsZWQsXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgLy8gQ2hlY2tzIHRoYXQgc2hlbGwuY3VycmVudFdpZGdldCBpcyB2YWxpZDpcbiAgICAgIGlmICghaXNFbmFibGVkKCkpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldChzaGVsbC5jdXJyZW50V2lkZ2V0ISk7XG4gICAgICBjb25zdCB0eXBlID0gZmlsZVR5cGUoc2hlbGwuY3VycmVudFdpZGdldCEsIGRvY01hbmFnZXIpO1xuICAgICAgaWYgKCFjb250ZXh0KSB7XG4gICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0Nhbm5vdCBSZWxvYWQnKSxcbiAgICAgICAgICBib2R5OiB0cmFucy5fXygnTm8gY29udGV4dCBmb3VuZCBmb3IgY3VycmVudCB3aWRnZXQhJyksXG4gICAgICAgICAgYnV0dG9uczogW0RpYWxvZy5va0J1dHRvbigpXVxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICAgIGlmIChjb250ZXh0Lm1vZGVsLmRpcnR5KSB7XG4gICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ1JlbG9hZCAlMSBmcm9tIERpc2snLCB0eXBlKSxcbiAgICAgICAgICBib2R5OiB0cmFucy5fXyhcbiAgICAgICAgICAgICdBcmUgeW91IHN1cmUgeW91IHdhbnQgdG8gcmVsb2FkIHRoZSAlMSBmcm9tIHRoZSBkaXNrPycsXG4gICAgICAgICAgICB0eXBlXG4gICAgICAgICAgKSxcbiAgICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKCksXG4gICAgICAgICAgICBEaWFsb2cud2FybkJ1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnUmVsb2FkJykgfSlcbiAgICAgICAgICBdXG4gICAgICAgIH0pLnRoZW4ocmVzdWx0ID0+IHtcbiAgICAgICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQgJiYgIWNvbnRleHQuaXNEaXNwb3NlZCkge1xuICAgICAgICAgICAgcmV0dXJuIGNvbnRleHQucmV2ZXJ0KCk7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGlmICghY29udGV4dC5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgcmV0dXJuIGNvbnRleHQucmV2ZXJ0KCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZXN0b3JlQ2hlY2twb2ludCwge1xuICAgIGxhYmVsOiAoKSA9PlxuICAgICAgdHJhbnMuX18oXG4gICAgICAgICdSZXZlcnQgJTEgdG8gQ2hlY2twb2ludOKApicsXG4gICAgICAgIGZpbGVUeXBlKHNoZWxsLmN1cnJlbnRXaWRnZXQsIGRvY01hbmFnZXIpXG4gICAgICApLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdSZXZlcnQgY29udGVudHMgdG8gcHJldmlvdXMgY2hlY2twb2ludCcpLFxuICAgIGlzRW5hYmxlZCxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAvLyBDaGVja3MgdGhhdCBzaGVsbC5jdXJyZW50V2lkZ2V0IGlzIHZhbGlkOlxuICAgICAgaWYgKCFpc0VuYWJsZWQoKSkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHNoZWxsLmN1cnJlbnRXaWRnZXQhKTtcbiAgICAgIGlmICghY29udGV4dCkge1xuICAgICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdDYW5ub3QgUmV2ZXJ0JyksXG4gICAgICAgICAgYm9keTogdHJhbnMuX18oJ05vIGNvbnRleHQgZm91bmQgZm9yIGN1cnJlbnQgd2lkZ2V0IScpLFxuICAgICAgICAgIGJ1dHRvbnM6IFtEaWFsb2cub2tCdXR0b24oKV1cbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgICByZXR1cm4gY29udGV4dC5saXN0Q2hlY2twb2ludHMoKS50aGVuKGFzeW5jIGNoZWNrcG9pbnRzID0+IHtcbiAgICAgICAgY29uc3QgdHlwZSA9IGZpbGVUeXBlKHNoZWxsLmN1cnJlbnRXaWRnZXQsIGRvY01hbmFnZXIpO1xuICAgICAgICBpZiAoY2hlY2twb2ludHMubGVuZ3RoIDwgMSkge1xuICAgICAgICAgIGF3YWl0IHNob3dFcnJvck1lc3NhZ2UoXG4gICAgICAgICAgICB0cmFucy5fXygnTm8gY2hlY2twb2ludHMnKSxcbiAgICAgICAgICAgIHRyYW5zLl9fKCdObyBjaGVja3BvaW50cyBhcmUgYXZhaWxhYmxlIGZvciB0aGlzICUxLicsIHR5cGUpXG4gICAgICAgICAgKTtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgdGFyZ2V0Q2hlY2twb2ludCA9XG4gICAgICAgICAgY2hlY2twb2ludHMubGVuZ3RoID09PSAxXG4gICAgICAgICAgICA/IGNoZWNrcG9pbnRzWzBdXG4gICAgICAgICAgICA6IGF3YWl0IFByaXZhdGUuZ2V0VGFyZ2V0Q2hlY2twb2ludChjaGVja3BvaW50cy5yZXZlcnNlKCksIHRyYW5zKTtcblxuICAgICAgICBpZiAoIXRhcmdldENoZWNrcG9pbnQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnUmV2ZXJ0ICUxIHRvIGNoZWNrcG9pbnQnLCB0eXBlKSxcbiAgICAgICAgICBib2R5OiBuZXcgUmV2ZXJ0Q29uZmlybVdpZGdldCh0YXJnZXRDaGVja3BvaW50LCB0cmFucywgdHlwZSksXG4gICAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbigpLFxuICAgICAgICAgICAgRGlhbG9nLndhcm5CdXR0b24oe1xuICAgICAgICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1JldmVydCcpLFxuICAgICAgICAgICAgICBhcmlhTGFiZWw6IHRyYW5zLl9fKCdSZXZlcnQgdG8gQ2hlY2twb2ludCcpXG4gICAgICAgICAgICB9KVxuICAgICAgICAgIF1cbiAgICAgICAgfSkudGhlbihyZXN1bHQgPT4ge1xuICAgICAgICAgIGlmIChjb250ZXh0LmlzRGlzcG9zZWQpIHtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICB9XG4gICAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgICAgICBpZiAoY29udGV4dC5tb2RlbC5yZWFkT25seSkge1xuICAgICAgICAgICAgICByZXR1cm4gY29udGV4dC5yZXZlcnQoKTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHJldHVybiBjb250ZXh0XG4gICAgICAgICAgICAgIC5yZXN0b3JlQ2hlY2twb2ludCh0YXJnZXRDaGVja3BvaW50LmlkKVxuICAgICAgICAgICAgICAudGhlbigoKSA9PiBjb250ZXh0LnJldmVydCgpKTtcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgfSk7XG4gICAgfVxuICB9KTtcblxuICBjb25zdCBjYXB0aW9uID0gKCkgPT4ge1xuICAgIGlmIChzaGVsbC5jdXJyZW50V2lkZ2V0KSB7XG4gICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHNoZWxsLmN1cnJlbnRXaWRnZXQpO1xuICAgICAgaWYgKGNvbnRleHQ/Lm1vZGVsLmNvbGxhYm9yYXRpdmUpIHtcbiAgICAgICAgcmV0dXJuIHRyYW5zLl9fKFxuICAgICAgICAgICdJbiBjb2xsYWJvcmF0aXZlIG1vZGUsIHRoZSBkb2N1bWVudCBpcyBzYXZlZCBhdXRvbWF0aWNhbGx5IGFmdGVyIGV2ZXJ5IGNoYW5nZSdcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICAgIGlmICghaXNXcml0YWJsZSgpKSB7XG4gICAgICAgIHJldHVybiB0cmFucy5fXyhcbiAgICAgICAgICBgZG9jdW1lbnQgaXMgcGVybWlzc2lvbmVkIHJlYWRvbmx5OyBcInNhdmVcIiBpcyBkaXNhYmxlZCwgdXNlIFwic2F2ZSBhcy4uLlwiIGluc3RlYWRgXG4gICAgICAgICk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgcmV0dXJuIHRyYW5zLl9fKCdTYXZlIGFuZCBjcmVhdGUgY2hlY2twb2ludCcpO1xuICB9O1xuXG4gIGNvbnN0IHNhdmVJblByb2dyZXNzID0gbmV3IFdlYWtTZXQ8RG9jdW1lbnRSZWdpc3RyeS5Db250ZXh0PigpO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zYXZlLCB7XG4gICAgbGFiZWw6ICgpID0+IHRyYW5zLl9fKCdTYXZlICUxJywgZmlsZVR5cGUoc2hlbGwuY3VycmVudFdpZGdldCwgZG9jTWFuYWdlcikpLFxuICAgIGNhcHRpb24sXG4gICAgaWNvbjogYXJncyA9PiAoYXJncy50b29sYmFyID8gc2F2ZUljb24gOiB1bmRlZmluZWQpLFxuICAgIGlzRW5hYmxlZDogaXNXcml0YWJsZSxcbiAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAvLyBDaGVja3MgdGhhdCBzaGVsbC5jdXJyZW50V2lkZ2V0IGlzIHZhbGlkOlxuICAgICAgY29uc3Qgd2lkZ2V0ID0gc2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQod2lkZ2V0ISk7XG4gICAgICBpZiAoaXNFbmFibGVkKCkpIHtcbiAgICAgICAgaWYgKCFjb250ZXh0KSB7XG4gICAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdDYW5ub3QgU2F2ZScpLFxuICAgICAgICAgICAgYm9keTogdHJhbnMuX18oJ05vIGNvbnRleHQgZm91bmQgZm9yIGN1cnJlbnQgd2lkZ2V0IScpLFxuICAgICAgICAgICAgYnV0dG9uczogW0RpYWxvZy5va0J1dHRvbigpXVxuICAgICAgICAgIH0pO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGlmIChzYXZlSW5Qcm9ncmVzcy5oYXMoY29udGV4dCkpIHtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICB9XG5cbiAgICAgICAgICBpZiAoY29udGV4dC5tb2RlbC5yZWFkT25seSkge1xuICAgICAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0Nhbm5vdCBTYXZlJyksXG4gICAgICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKCdEb2N1bWVudCBpcyByZWFkLW9ubHknKSxcbiAgICAgICAgICAgICAgYnV0dG9uczogW0RpYWxvZy5va0J1dHRvbigpXVxuICAgICAgICAgICAgfSk7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgc2F2ZUluUHJvZ3Jlc3MuYWRkKGNvbnRleHQpO1xuXG4gICAgICAgICAgY29uc3Qgb2xkTmFtZSA9IFBhdGhFeHQuYmFzZW5hbWUoY29udGV4dC5jb250ZW50c01vZGVsPy5wYXRoID8/ICcnKTtcbiAgICAgICAgICBsZXQgbmV3TmFtZSA9IG9sZE5hbWU7XG5cbiAgICAgICAgICBpZiAoXG4gICAgICAgICAgICBkb2NNYW5hZ2VyLnJlbmFtZVVudGl0bGVkRmlsZU9uU2F2ZSAmJlxuICAgICAgICAgICAgKHdpZGdldCBhcyBJRG9jdW1lbnRXaWRnZXQpLmlzVW50aXRsZWQgPT09IHRydWVcbiAgICAgICAgICApIHtcbiAgICAgICAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IElucHV0RGlhbG9nLmdldFRleHQoe1xuICAgICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ1JlbmFtZSBmaWxlJyksXG4gICAgICAgICAgICAgIG9rTGFiZWw6IHRyYW5zLl9fKCdSZW5hbWUnKSxcbiAgICAgICAgICAgICAgcGxhY2Vob2xkZXI6IHRyYW5zLl9fKCdGaWxlIG5hbWUnKSxcbiAgICAgICAgICAgICAgdGV4dDogb2xkTmFtZSxcbiAgICAgICAgICAgICAgc2VsZWN0aW9uUmFuZ2U6IG9sZE5hbWUubGVuZ3RoIC0gUGF0aEV4dC5leHRuYW1lKG9sZE5hbWUpLmxlbmd0aCxcbiAgICAgICAgICAgICAgY2hlY2tib3g6IHtcbiAgICAgICAgICAgICAgICBsYWJlbDogdHJhbnMuX18oJ0RvIG5vdCBhc2sgbWUgYWdhaW4uJyksXG4gICAgICAgICAgICAgICAgY2FwdGlvbjogdHJhbnMuX18oXG4gICAgICAgICAgICAgICAgICAnSWYgY2hlY2tlZCwgeW91IHdpbGwgbm90IGJlIGFza2VkIHRvIHJlbmFtZSBmdXR1cmUgdW50aXRsZWQgZmlsZXMgd2hlbiBzYXZpbmcgdGhlbS4nXG4gICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9KTtcblxuICAgICAgICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgICAgICAgIG5ld05hbWUgPSByZXN1bHQudmFsdWUgPz8gb2xkTmFtZTtcbiAgICAgICAgICAgICAgKHdpZGdldCBhcyBJRG9jdW1lbnRXaWRnZXQpLmlzVW50aXRsZWQgPSBmYWxzZTtcbiAgICAgICAgICAgICAgaWYgKHR5cGVvZiByZXN1bHQuaXNDaGVja2VkID09PSAnYm9vbGVhbicpIHtcbiAgICAgICAgICAgICAgICBjb25zdCBjdXJyZW50U2V0dGluZyA9IChcbiAgICAgICAgICAgICAgICAgIGF3YWl0IHNldHRpbmdSZWdpc3RyeS5nZXQoXG4gICAgICAgICAgICAgICAgICAgIGRvY01hbmFnZXJQbHVnaW5JZCxcbiAgICAgICAgICAgICAgICAgICAgJ3JlbmFtZVVudGl0bGVkRmlsZU9uU2F2ZSdcbiAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICApLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICAgICAgICAgIGlmIChyZXN1bHQuaXNDaGVja2VkID09PSBjdXJyZW50U2V0dGluZykge1xuICAgICAgICAgICAgICAgICAgc2V0dGluZ1JlZ2lzdHJ5XG4gICAgICAgICAgICAgICAgICAgIC5zZXQoXG4gICAgICAgICAgICAgICAgICAgICAgZG9jTWFuYWdlclBsdWdpbklkLFxuICAgICAgICAgICAgICAgICAgICAgICdyZW5hbWVVbnRpdGxlZEZpbGVPblNhdmUnLFxuICAgICAgICAgICAgICAgICAgICAgICFyZXN1bHQuaXNDaGVja2VkXG4gICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICAgICAgICAgICAgICAgIGBGYWlsIHRvIHNldCAncmVuYW1lVW50aXRsZWRGaWxlT25TYXZlOlxcbiR7cmVhc29ufWBcbiAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG5cbiAgICAgICAgICB0cnkge1xuICAgICAgICAgICAgYXdhaXQgY29udGV4dC5zYXZlKCk7XG5cbiAgICAgICAgICAgIGlmICghd2lkZ2V0Py5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgICAgIHJldHVybiBjb250ZXh0IS5jcmVhdGVDaGVja3BvaW50KCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICAgICAgICAvLyBJZiB0aGUgc2F2ZSB3YXMgY2FuY2VsZWQgYnkgdXNlci1hY3Rpb24sIGRvIG5vdGhpbmcuXG4gICAgICAgICAgICBpZiAoZXJyLm5hbWUgPT09ICdNb2RhbENhbmNlbEVycm9yJykge1xuICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICB0aHJvdyBlcnI7XG4gICAgICAgICAgfSBmaW5hbGx5IHtcbiAgICAgICAgICAgIHNhdmVJblByb2dyZXNzLmRlbGV0ZShjb250ZXh0KTtcbiAgICAgICAgICAgIGlmIChuZXdOYW1lICE9PSBvbGROYW1lKSB7XG4gICAgICAgICAgICAgIGF3YWl0IGNvbnRleHQucmVuYW1lKG5ld05hbWUpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNhdmVBbGwsIHtcbiAgICBsYWJlbDogKCkgPT4gdHJhbnMuX18oJ1NhdmUgQWxsJyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ1NhdmUgYWxsIG9wZW4gZG9jdW1lbnRzJyksXG4gICAgaXNFbmFibGVkOiAoKSA9PiB7XG4gICAgICByZXR1cm4gc29tZShcbiAgICAgICAgc2hlbGwud2lkZ2V0cygnbWFpbicpLFxuICAgICAgICB3ID0+IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldCh3KT8uY29udGVudHNNb2RlbD8ud3JpdGFibGUgPz8gZmFsc2VcbiAgICAgICk7XG4gICAgfSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBjb25zdCBwcm9taXNlczogUHJvbWlzZTx2b2lkPltdID0gW107XG4gICAgICBjb25zdCBwYXRocyA9IG5ldyBTZXQ8c3RyaW5nPigpOyAvLyBDYWNoZSBzbyB3ZSBkb24ndCBkb3VibGUgc2F2ZSBmaWxlcy5cbiAgICAgIGZvciAoY29uc3Qgd2lkZ2V0IG9mIHNoZWxsLndpZGdldHMoJ21haW4nKSkge1xuICAgICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KHdpZGdldCk7XG4gICAgICAgIGlmIChjb250ZXh0ICYmICFwYXRocy5oYXMoY29udGV4dC5wYXRoKSkge1xuICAgICAgICAgIGlmIChjb250ZXh0LmNvbnRlbnRzTW9kZWw/LndyaXRhYmxlKSB7XG4gICAgICAgICAgICBwYXRocy5hZGQoY29udGV4dC5wYXRoKTtcbiAgICAgICAgICAgIHByb21pc2VzLnB1c2goY29udGV4dC5zYXZlKCkpO1xuICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICBOb3RpZmljYXRpb24ud2FybmluZyhcbiAgICAgICAgICAgICAgdHJhbnMuX18oXG4gICAgICAgICAgICAgICAgYCUxIGlzIHBlcm1pc3Npb25lZCBhcyByZWFkb25seS4gVXNlIFwic2F2ZSBhcy4uLlwiIGluc3RlYWQuYCxcbiAgICAgICAgICAgICAgICBjb250ZXh0LnBhdGhcbiAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgICAgeyBhdXRvQ2xvc2U6IDUwMDAgfVxuICAgICAgICAgICAgKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHJldHVybiBQcm9taXNlLmFsbChwcm9taXNlcyk7XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2F2ZUFzLCB7XG4gICAgbGFiZWw6ICgpID0+XG4gICAgICB0cmFucy5fXygnU2F2ZSAlMSBBc+KApicsIGZpbGVUeXBlKHNoZWxsLmN1cnJlbnRXaWRnZXQsIGRvY01hbmFnZXIpKSxcbiAgICBjYXB0aW9uOiB0cmFucy5fXygnU2F2ZSB3aXRoIG5ldyBwYXRoJyksXG4gICAgaXNFbmFibGVkLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIC8vIENoZWNrcyB0aGF0IHNoZWxsLmN1cnJlbnRXaWRnZXQgaXMgdmFsaWQ6XG4gICAgICBpZiAoaXNFbmFibGVkKCkpIHtcbiAgICAgICAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldChzaGVsbC5jdXJyZW50V2lkZ2V0ISk7XG4gICAgICAgIGlmICghY29udGV4dCkge1xuICAgICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICAgIHRpdGxlOiB0cmFucy5fXygnQ2Fubm90IFNhdmUnKSxcbiAgICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKCdObyBjb250ZXh0IGZvdW5kIGZvciBjdXJyZW50IHdpZGdldCEnKSxcbiAgICAgICAgICAgIGJ1dHRvbnM6IFtEaWFsb2cub2tCdXR0b24oKV1cbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IG9uQ2hhbmdlID0gKFxuICAgICAgICAgIHNlbmRlcjogQ29udGVudHMuSU1hbmFnZXIsXG4gICAgICAgICAgYXJnczogQ29udGVudHMuSUNoYW5nZWRBcmdzXG4gICAgICAgICkgPT4ge1xuICAgICAgICAgIGlmIChcbiAgICAgICAgICAgIGFyZ3MudHlwZSA9PT0gJ3NhdmUnICYmXG4gICAgICAgICAgICBhcmdzLm5ld1ZhbHVlICYmXG4gICAgICAgICAgICBhcmdzLm5ld1ZhbHVlLnBhdGggIT09IGNvbnRleHQucGF0aFxuICAgICAgICAgICkge1xuICAgICAgICAgICAgdm9pZCBkb2NNYW5hZ2VyLmNsb3NlRmlsZShjb250ZXh0LnBhdGgpO1xuICAgICAgICAgICAgdm9pZCBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMub3Blbiwge1xuICAgICAgICAgICAgICBwYXRoOiBhcmdzLm5ld1ZhbHVlLnBhdGhcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfTtcbiAgICAgICAgZG9jTWFuYWdlci5zZXJ2aWNlcy5jb250ZW50cy5maWxlQ2hhbmdlZC5jb25uZWN0KG9uQ2hhbmdlKTtcbiAgICAgICAgY29udGV4dFxuICAgICAgICAgIC5zYXZlQXMoKVxuICAgICAgICAgIC5maW5hbGx5KCgpID0+XG4gICAgICAgICAgICBkb2NNYW5hZ2VyLnNlcnZpY2VzLmNvbnRlbnRzLmZpbGVDaGFuZ2VkLmRpc2Nvbm5lY3Qob25DaGFuZ2UpXG4gICAgICAgICAgKTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVBdXRvc2F2ZSwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnQXV0b3NhdmUgRG9jdW1lbnRzJyksXG4gICAgaXNUb2dnbGVkOiAoKSA9PiBkb2NNYW5hZ2VyLmF1dG9zYXZlLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHZhbHVlID0gIWRvY01hbmFnZXIuYXV0b3NhdmU7XG4gICAgICBjb25zdCBrZXkgPSAnYXV0b3NhdmUnO1xuICAgICAgcmV0dXJuIHNldHRpbmdSZWdpc3RyeVxuICAgICAgICAuc2V0KGRvY01hbmFnZXJQbHVnaW5JZCwga2V5LCB2YWx1ZSlcbiAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICAgIGBGYWlsZWQgdG8gc2V0ICR7ZG9jTWFuYWdlclBsdWdpbklkfToke2tleX0gLSAke3JlYXNvbi5tZXNzYWdlfWBcbiAgICAgICAgICApO1xuICAgICAgICB9KTtcbiAgICB9XG4gIH0pO1xuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgW1xuICAgICAgQ29tbWFuZElEcy5yZWxvYWQsXG4gICAgICBDb21tYW5kSURzLnJlc3RvcmVDaGVja3BvaW50LFxuICAgICAgQ29tbWFuZElEcy5zYXZlLFxuICAgICAgQ29tbWFuZElEcy5zYXZlQXMsXG4gICAgICBDb21tYW5kSURzLnRvZ2dsZUF1dG9zYXZlLFxuICAgICAgQ29tbWFuZElEcy5kdXBsaWNhdGVcbiAgICBdLmZvckVhY2goY29tbWFuZCA9PiB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kLCBjYXRlZ29yeSB9KTtcbiAgICB9KTtcbiAgfVxufVxuXG5mdW5jdGlvbiBhZGRMYWJDb21tYW5kcyhcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIGRvY01hbmFnZXI6IElEb2N1bWVudE1hbmFnZXIsXG4gIGxhYlNoZWxsOiBJTGFiU2hlbGwsXG4gIHdpZGdldE9wZW5lcjogSURvY3VtZW50V2lkZ2V0T3BlbmVyLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuKTogdm9pZCB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcblxuICAvLyBSZXR1cm5zIHRoZSBkb2Mgd2lkZ2V0IGFzc29jaWF0ZWQgd2l0aCB0aGUgbW9zdCByZWNlbnQgY29udGV4dG1lbnUgZXZlbnQuXG4gIGNvbnN0IGNvbnRleHRNZW51V2lkZ2V0ID0gKCk6IFdpZGdldCB8IG51bGwgPT4ge1xuICAgIGNvbnN0IHBhdGhSZSA9IC9bUHBdYXRoOlxccz8oLiopXFxuPy87XG4gICAgY29uc3QgdGVzdCA9IChub2RlOiBIVE1MRWxlbWVudCkgPT4gISFub2RlWyd0aXRsZSddPy5tYXRjaChwYXRoUmUpO1xuICAgIGNvbnN0IG5vZGUgPSBhcHAuY29udGV4dE1lbnVIaXRUZXN0KHRlc3QpO1xuXG4gICAgY29uc3QgcGF0aE1hdGNoID0gbm9kZT8uWyd0aXRsZSddLm1hdGNoKHBhdGhSZSk7XG4gICAgcmV0dXJuIChcbiAgICAgIChwYXRoTWF0Y2ggJiYgZG9jTWFuYWdlci5maW5kV2lkZ2V0KHBhdGhNYXRjaFsxXSwgbnVsbCkpID8/XG4gICAgICAvLyBGYWxsIGJhY2sgdG8gYWN0aXZlIGRvYyB3aWRnZXQgaWYgcGF0aCBjYW5ub3QgYmUgb2J0YWluZWQgZnJvbSBldmVudC5cbiAgICAgIGxhYlNoZWxsLmN1cnJlbnRXaWRnZXRcbiAgICApO1xuICB9O1xuXG4gIC8vIFJldHVybnMgYHRydWVgIGlmIHRoZSBjdXJyZW50IHdpZGdldCBoYXMgYSBkb2N1bWVudCBjb250ZXh0LlxuICBjb25zdCBpc0VuYWJsZWQgPSAoKSA9PiB7XG4gICAgY29uc3QgeyBjdXJyZW50V2lkZ2V0IH0gPSBsYWJTaGVsbDtcbiAgICByZXR1cm4gISEoY3VycmVudFdpZGdldCAmJiBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoY3VycmVudFdpZGdldCkpO1xuICB9O1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jbG9uZSwge1xuICAgIGxhYmVsOiAoKSA9PlxuICAgICAgdHJhbnMuX18oJ05ldyBWaWV3IGZvciAlMScsIGZpbGVUeXBlKGNvbnRleHRNZW51V2lkZ2V0KCksIGRvY01hbmFnZXIpKSxcbiAgICBpc0VuYWJsZWQsXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSBjb250ZXh0TWVudVdpZGdldCgpO1xuICAgICAgY29uc3Qgb3B0aW9ucyA9IChhcmdzWydvcHRpb25zJ10gYXMgRG9jdW1lbnRSZWdpc3RyeS5JT3Blbk9wdGlvbnMpIHx8IHtcbiAgICAgICAgbW9kZTogJ3NwbGl0LXJpZ2h0J1xuICAgICAgfTtcbiAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIC8vIENsb25lIHRoZSB3aWRnZXQuXG4gICAgICBjb25zdCBjaGlsZCA9IGRvY01hbmFnZXIuY2xvbmVXaWRnZXQod2lkZ2V0KTtcbiAgICAgIGlmIChjaGlsZCkge1xuICAgICAgICB3aWRnZXRPcGVuZXIub3BlbihjaGlsZCwgb3B0aW9ucyk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVuYW1lLCB7XG4gICAgbGFiZWw6ICgpID0+IHtcbiAgICAgIGxldCB0ID0gZmlsZVR5cGUoY29udGV4dE1lbnVXaWRnZXQoKSwgZG9jTWFuYWdlcik7XG4gICAgICBpZiAodCkge1xuICAgICAgICB0ID0gJyAnICsgdDtcbiAgICAgIH1cbiAgICAgIHJldHVybiB0cmFucy5fXygnUmVuYW1lJTHigKYnLCB0KTtcbiAgICB9LFxuICAgIGlzRW5hYmxlZCxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICAvLyBJbXBsaWVzIGNvbnRleHRNZW51V2lkZ2V0KCkgIT09IG51bGxcbiAgICAgIGlmIChpc0VuYWJsZWQoKSkge1xuICAgICAgICBjb25zdCBjb250ZXh0ID0gZG9jTWFuYWdlci5jb250ZXh0Rm9yV2lkZ2V0KGNvbnRleHRNZW51V2lkZ2V0KCkhKTtcbiAgICAgICAgcmV0dXJuIHJlbmFtZURpYWxvZyhkb2NNYW5hZ2VyLCBjb250ZXh0ISk7XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZHVwbGljYXRlLCB7XG4gICAgbGFiZWw6ICgpID0+XG4gICAgICB0cmFucy5fXygnRHVwbGljYXRlICUxJywgZmlsZVR5cGUoY29udGV4dE1lbnVXaWRnZXQoKSwgZG9jTWFuYWdlcikpLFxuICAgIGlzRW5hYmxlZCxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICBpZiAoaXNFbmFibGVkKCkpIHtcbiAgICAgICAgY29uc3QgY29udGV4dCA9IGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldChjb250ZXh0TWVudVdpZGdldCgpISk7XG4gICAgICAgIGlmICghY29udGV4dCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gZG9jTWFuYWdlci5kdXBsaWNhdGUoY29udGV4dC5wYXRoKTtcbiAgICAgIH1cbiAgICB9XG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5kZWwsIHtcbiAgICBsYWJlbDogKCkgPT5cbiAgICAgIHRyYW5zLl9fKCdEZWxldGUgJTEnLCBmaWxlVHlwZShjb250ZXh0TWVudVdpZGdldCgpLCBkb2NNYW5hZ2VyKSksXG4gICAgaXNFbmFibGVkLFxuICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgIC8vIEltcGxpZXMgY29udGV4dE1lbnVXaWRnZXQoKSAhPT0gbnVsbFxuICAgICAgaWYgKGlzRW5hYmxlZCgpKSB7XG4gICAgICAgIGNvbnN0IGNvbnRleHQgPSBkb2NNYW5hZ2VyLmNvbnRleHRGb3JXaWRnZXQoY29udGV4dE1lbnVXaWRnZXQoKSEpO1xuICAgICAgICBpZiAoIWNvbnRleHQpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgcmVzdWx0ID0gYXdhaXQgc2hvd0RpYWxvZyh7XG4gICAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdEZWxldGUnKSxcbiAgICAgICAgICBib2R5OiB0cmFucy5fXygnQXJlIHlvdSBzdXJlIHlvdSB3YW50IHRvIGRlbGV0ZSAlMScsIGNvbnRleHQucGF0aCksXG4gICAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgICAgRGlhbG9nLmNhbmNlbEJ1dHRvbigpLFxuICAgICAgICAgICAgRGlhbG9nLndhcm5CdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0RlbGV0ZScpIH0pXG4gICAgICAgICAgXVxuICAgICAgICB9KTtcblxuICAgICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQpIHtcbiAgICAgICAgICBhd2FpdCBhcHAuY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpkZWxldGUtZmlsZScsIHtcbiAgICAgICAgICAgIHBhdGg6IGNvbnRleHQucGF0aFxuICAgICAgICAgIH0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2hvd0luRmlsZUJyb3dzZXIsIHtcbiAgICBsYWJlbDogKCkgPT4gdHJhbnMuX18oJ1Nob3cgaW4gRmlsZSBCcm93c2VyJyksXG4gICAgaXNFbmFibGVkLFxuICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IGNvbnRleHRNZW51V2lkZ2V0KCk7XG4gICAgICBjb25zdCBjb250ZXh0ID0gd2lkZ2V0ICYmIGRvY01hbmFnZXIuY29udGV4dEZvcldpZGdldCh3aWRnZXQpO1xuICAgICAgaWYgKCFjb250ZXh0KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cblxuICAgICAgLy8gJ2FjdGl2YXRlJyBpcyBuZWVkZWQgaWYgdGhpcyBjb21tYW5kIGlzIHNlbGVjdGVkIGluIHRoZSBcIm9wZW4gdGFic1wiIHNpZGViYXJcbiAgICAgIGF3YWl0IGNvbW1hbmRzLmV4ZWN1dGUoJ2ZpbGVicm93c2VyOmFjdGl2YXRlJywgeyBwYXRoOiBjb250ZXh0LnBhdGggfSk7XG4gICAgICBhd2FpdCBjb21tYW5kcy5leGVjdXRlKCdmaWxlYnJvd3Nlcjpnby10by1wYXRoJywgeyBwYXRoOiBjb250ZXh0LnBhdGggfSk7XG4gICAgfVxuICB9KTtcbn1cblxuLyoqXG4gKiBIYW5kbGUgZGlydHkgc3RhdGUgZm9yIGEgY29udGV4dC5cbiAqL1xuZnVuY3Rpb24gaGFuZGxlQ29udGV4dChcbiAgc3RhdHVzOiBJTGFiU3RhdHVzLFxuICBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHRcbik6IHZvaWQge1xuICBsZXQgZGlzcG9zYWJsZTogSURpc3Bvc2FibGUgfCBudWxsID0gbnVsbDtcbiAgY29uc3Qgb25TdGF0ZUNoYW5nZWQgPSAoc2VuZGVyOiBhbnksIGFyZ3M6IElDaGFuZ2VkQXJnczxhbnk+KSA9PiB7XG4gICAgaWYgKGFyZ3MubmFtZSA9PT0gJ2RpcnR5Jykge1xuICAgICAgaWYgKGFyZ3MubmV3VmFsdWUgPT09IHRydWUpIHtcbiAgICAgICAgaWYgKCFkaXNwb3NhYmxlKSB7XG4gICAgICAgICAgZGlzcG9zYWJsZSA9IHN0YXR1cy5zZXREaXJ0eSgpO1xuICAgICAgICB9XG4gICAgICB9IGVsc2UgaWYgKGRpc3Bvc2FibGUpIHtcbiAgICAgICAgZGlzcG9zYWJsZS5kaXNwb3NlKCk7XG4gICAgICAgIGRpc3Bvc2FibGUgPSBudWxsO1xuICAgICAgfVxuICAgIH1cbiAgfTtcbiAgdm9pZCBjb250ZXh0LnJlYWR5LnRoZW4oKCkgPT4ge1xuICAgIGNvbnRleHQubW9kZWwuc3RhdGVDaGFuZ2VkLmNvbm5lY3Qob25TdGF0ZUNoYW5nZWQpO1xuICAgIGlmIChjb250ZXh0Lm1vZGVsLmRpcnR5KSB7XG4gICAgICBkaXNwb3NhYmxlID0gc3RhdHVzLnNldERpcnR5KCk7XG4gICAgfVxuICB9KTtcbiAgY29udGV4dC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICBpZiAoZGlzcG9zYWJsZSkge1xuICAgICAgZGlzcG9zYWJsZS5kaXNwb3NlKCk7XG4gICAgfVxuICB9KTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBtb2R1bGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQSBjb3VudGVyIGZvciB1bmlxdWUgSURzLlxuICAgKi9cbiAgZXhwb3J0IGxldCBpZCA9IDA7XG5cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZVJldmVydENvbmZpcm1Ob2RlKFxuICAgIGNoZWNrcG9pbnQ6IENvbnRlbnRzLklDaGVja3BvaW50TW9kZWwsXG4gICAgZmlsZVR5cGU6IHN0cmluZyxcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGVcbiAgKTogSFRNTEVsZW1lbnQge1xuICAgIGNvbnN0IGJvZHkgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICBjb25zdCBjb25maXJtTWVzc2FnZSA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ3AnKTtcbiAgICBjb25zdCBjb25maXJtVGV4dCA9IGRvY3VtZW50LmNyZWF0ZVRleHROb2RlKFxuICAgICAgdHJhbnMuX18oXG4gICAgICAgICdBcmUgeW91IHN1cmUgeW91IHdhbnQgdG8gcmV2ZXJ0IHRoZSAlMSB0byBjaGVja3BvaW50PyAnLFxuICAgICAgICBmaWxlVHlwZVxuICAgICAgKVxuICAgICk7XG4gICAgY29uc3QgY2Fubm90VW5kb1RleHQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdzdHJvbmcnKTtcbiAgICBjYW5ub3RVbmRvVGV4dC50ZXh0Q29udGVudCA9IHRyYW5zLl9fKCdUaGlzIGNhbm5vdCBiZSB1bmRvbmUuJyk7XG5cbiAgICBjb25maXJtTWVzc2FnZS5hcHBlbmRDaGlsZChjb25maXJtVGV4dCk7XG4gICAgY29uZmlybU1lc3NhZ2UuYXBwZW5kQ2hpbGQoY2Fubm90VW5kb1RleHQpO1xuXG4gICAgY29uc3QgbGFzdENoZWNrcG9pbnRNZXNzYWdlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgncCcpO1xuICAgIGNvbnN0IGxhc3RDaGVja3BvaW50VGV4dCA9IGRvY3VtZW50LmNyZWF0ZVRleHROb2RlKFxuICAgICAgdHJhbnMuX18oJ1RoZSBjaGVja3BvaW50IHdhcyBsYXN0IHVwZGF0ZWQgYXQ6ICcpXG4gICAgKTtcbiAgICBjb25zdCBsYXN0Q2hlY2twb2ludERhdGUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdwJyk7XG4gICAgY29uc3QgZGF0ZSA9IG5ldyBEYXRlKGNoZWNrcG9pbnQubGFzdF9tb2RpZmllZCk7XG4gICAgbGFzdENoZWNrcG9pbnREYXRlLnN0eWxlLnRleHRBbGlnbiA9ICdjZW50ZXInO1xuICAgIGxhc3RDaGVja3BvaW50RGF0ZS50ZXh0Q29udGVudCA9XG4gICAgICBUaW1lLmZvcm1hdChkYXRlKSArICcgKCcgKyBUaW1lLmZvcm1hdEh1bWFuKGRhdGUpICsgJyknO1xuXG4gICAgbGFzdENoZWNrcG9pbnRNZXNzYWdlLmFwcGVuZENoaWxkKGxhc3RDaGVja3BvaW50VGV4dCk7XG4gICAgbGFzdENoZWNrcG9pbnRNZXNzYWdlLmFwcGVuZENoaWxkKGxhc3RDaGVja3BvaW50RGF0ZSk7XG5cbiAgICBib2R5LmFwcGVuZENoaWxkKGNvbmZpcm1NZXNzYWdlKTtcbiAgICBib2R5LmFwcGVuZENoaWxkKGxhc3RDaGVja3BvaW50TWVzc2FnZSk7XG4gICAgcmV0dXJuIGJvZHk7XG4gIH1cblxuICAvKipcbiAgICogQXNrIHVzZXIgZm9yIGEgY2hlY2twb2ludCB0byByZXZlcnQgdG8uXG4gICAqL1xuICBleHBvcnQgYXN5bmMgZnVuY3Rpb24gZ2V0VGFyZ2V0Q2hlY2twb2ludChcbiAgICBjaGVja3BvaW50czogQ29udGVudHMuSUNoZWNrcG9pbnRNb2RlbFtdLFxuICAgIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApOiBQcm9taXNlPENvbnRlbnRzLklDaGVja3BvaW50TW9kZWwgfCB1bmRlZmluZWQ+IHtcbiAgICAvLyB0aGUgaWQgY291bGQgYmUgdG9vIGxvbmcgdG8gc2hvdyBzbyB1c2UgdGhlIGluZGV4IGluc3RlYWRcbiAgICBjb25zdCBpbmRleFNlcGFyYXRvciA9ICcuJztcbiAgICBjb25zdCBpdGVtcyA9IGNoZWNrcG9pbnRzLm1hcCgoY2hlY2twb2ludCwgaW5kZXgpID0+IHtcbiAgICAgIGNvbnN0IGlzb0RhdGUgPSBUaW1lLmZvcm1hdChjaGVja3BvaW50Lmxhc3RfbW9kaWZpZWQpO1xuICAgICAgY29uc3QgaHVtYW5EYXRlID0gVGltZS5mb3JtYXRIdW1hbihjaGVja3BvaW50Lmxhc3RfbW9kaWZpZWQpO1xuICAgICAgcmV0dXJuIGAke2luZGV4fSR7aW5kZXhTZXBhcmF0b3J9ICR7aXNvRGF0ZX0gKCR7aHVtYW5EYXRlfSlgO1xuICAgIH0pO1xuXG4gICAgY29uc3Qgc2VsZWN0ZWRJdGVtID0gKFxuICAgICAgYXdhaXQgSW5wdXREaWFsb2cuZ2V0SXRlbSh7XG4gICAgICAgIGl0ZW1zOiBpdGVtcyxcbiAgICAgICAgdGl0bGU6IHRyYW5zLl9fKCdDaG9vc2UgYSBjaGVja3BvaW50JylcbiAgICAgIH0pXG4gICAgKS52YWx1ZTtcblxuICAgIGlmICghc2VsZWN0ZWRJdGVtKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHNlbGVjdGVkSW5kZXggPSBzZWxlY3RlZEl0ZW0uc3BsaXQoaW5kZXhTZXBhcmF0b3IsIDEpWzBdO1xuICAgIHJldHVybiBjaGVja3BvaW50c1twYXJzZUludChzZWxlY3RlZEluZGV4LCAxMCldO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=