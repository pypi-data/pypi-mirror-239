"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_help-extension_lib_index_js"],{

/***/ "../packages/help-extension/lib/index.js":
/*!***********************************************!*\
  !*** ../packages/help-extension/lib/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
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
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _licenses__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./licenses */ "../packages/help-extension/lib/licenses.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module help-extension
 */








/**
 * The command IDs used by the help plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'help:open';
    CommandIDs.about = 'help:about';
    CommandIDs.activate = 'help:activate';
    CommandIDs.close = 'help:close';
    CommandIDs.show = 'help:show';
    CommandIDs.hide = 'help:hide';
    CommandIDs.jupyterForum = 'help:jupyter-forum';
    CommandIDs.licenses = 'help:licenses';
    CommandIDs.licenseReport = 'help:license-report';
    CommandIDs.refreshLicenses = 'help:licenses-refresh';
})(CommandIDs || (CommandIDs = {}));
/**
 * A flag denoting whether the application is loaded over HTTPS.
 */
const LAB_IS_SECURE = window.location.protocol === 'https:';
/**
 * The class name added to the help widget.
 */
const HELP_CLASS = 'jp-Help';
/**
 * Add a command to show an About dialog.
 */
const about = {
    id: '@jupyterlab/help-extension:about',
    description: 'Adds a "About" dialog feature.',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.about, {
            label: trans.__('About %1', app.name),
            execute: () => {
                // Create the header of the about dialog
                const versionNumber = trans.__('Version %1', app.version);
                const versionInfo = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-version-info" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-version" }, versionNumber)));
                const title = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-header" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.jupyterIcon.react, { margin: "7px 9.5px", height: "auto", width: "58px" }),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-header-info" },
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.jupyterlabWordmarkIcon.react, { height: "auto", width: "196px" }),
                        versionInfo)));
                // Create the body of the about dialog
                const jupyterURL = 'https://jupyter.org/about.html';
                const contributorsURL = 'https://github.com/jupyterlab/jupyterlab/graphs/contributors';
                const externalLinks = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-externalLinks" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("a", { href: contributorsURL, target: "_blank", rel: "noopener noreferrer", className: "jp-Button-flat" }, trans.__('CONTRIBUTOR LIST')),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("a", { href: jupyterURL, target: "_blank", rel: "noopener noreferrer", className: "jp-Button-flat" }, trans.__('ABOUT PROJECT JUPYTER'))));
                const copyright = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-copyright" }, trans.__('© 2015-2023 Project Jupyter Contributors')));
                const body = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-body" },
                    externalLinks,
                    copyright));
                return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                    title,
                    body,
                    buttons: [
                        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.createButton({
                            label: trans.__('Dismiss'),
                            className: 'jp-About-button jp-mod-reject jp-mod-styled'
                        })
                    ]
                });
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.about, category });
        }
    }
};
/**
 * A plugin to add a command to open the Jupyter Forum.
 */
const jupyterForum = {
    id: '@jupyterlab/help-extension:jupyter-forum',
    description: 'Adds command to open the Jupyter Forum website.',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, translator, palette) => {
        const { commands } = app;
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        commands.addCommand(CommandIDs.jupyterForum, {
            label: trans.__('Jupyter Forum'),
            execute: () => {
                window.open('https://discourse.jupyter.org/c/jupyterlab');
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.jupyterForum, category });
        }
    }
};
/**
 * A plugin to open resources in IFrames or new browser tabs.
 */
const open = {
    id: '@jupyterlab/help-extension:open',
    description: 'Add command to open websites as panel or browser tab.',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, translator, restorer) => {
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        const namespace = 'help-doc';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({ namespace });
        let counter = 0;
        /**
         * Create a new HelpWidget widget.
         */
        function newHelpWidget(url, text) {
            // Allow scripts and forms so that things like
            // readthedocs can use their search functionality.
            // We *don't* allow same origin requests, which
            // can prevent some content from being loaded onto the
            // help pages.
            const content = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.IFrame({
                sandbox: ['allow-scripts', 'allow-forms']
            });
            content.url = url;
            content.addClass(HELP_CLASS);
            content.title.label = text;
            content.id = `${namespace}-${++counter}`;
            const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
            widget.addClass('jp-Help');
            return widget;
        }
        commands.addCommand(CommandIDs.open, {
            label: args => {
                var _a;
                return (_a = args['text']) !== null && _a !== void 0 ? _a : trans.__('Open the provided `url` in a tab.');
            },
            execute: args => {
                const url = args['url'];
                const text = args['text'];
                const newBrowserTab = args['newBrowserTab'] || false;
                // If help resource will generate a mixed content error, load externally.
                if (newBrowserTab ||
                    (LAB_IS_SECURE && _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.parse(url).protocol !== 'https:')) {
                    window.open(url);
                    return;
                }
                const widget = newHelpWidget(url, text);
                void tracker.add(widget);
                shell.add(widget, 'main');
                return widget;
            }
        });
        // Handle state restoration.
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.open,
                args: widget => ({
                    url: widget.content.url,
                    text: widget.content.title.label
                }),
                name: widget => widget.content.url
            });
        }
    }
};
/**
 * A plugin to add a list of resources to the help menu.
 */
const resources = {
    id: '@jupyterlab/help-extension:resources',
    description: 'Adds menu entries to Jupyter reference documentation websites.',
    autoStart: true,
    requires: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, mainMenu, translator, labShell, palette) => {
        const trans = translator.load('jupyterlab');
        const category = trans.__('Help');
        const { commands, serviceManager } = app;
        const resources = [
            {
                text: trans.__('JupyterLab Reference'),
                url: 'https://jupyterlab.readthedocs.io/en/latest/'
            },
            {
                text: trans.__('JupyterLab FAQ'),
                url: 'https://jupyterlab.readthedocs.io/en/latest/getting_started/faq.html'
            },
            {
                text: trans.__('Jupyter Reference'),
                url: 'https://jupyter.org/documentation'
            },
            {
                text: trans.__('Markdown Reference'),
                url: 'https://commonmark.org/help/'
            }
        ];
        resources.sort((a, b) => {
            return a.text.localeCompare(b.text);
        });
        // Populate the Help menu.
        const helpMenu = mainMenu.helpMenu;
        const resourcesGroup = resources.map(args => ({
            args,
            command: CommandIDs.open
        }));
        helpMenu.addGroup(resourcesGroup, 10);
        // Generate a cache of the kernel help links.
        const kernelInfoCache = new Map();
        const onSessionRunningChanged = (m, sessions) => {
            var _a;
            // If a new session has been added, it is at the back
            // of the session list. If one has changed or stopped,
            // it does not hurt to check it.
            if (!sessions.length) {
                return;
            }
            const sessionModel = sessions[sessions.length - 1];
            if (!sessionModel.kernel ||
                kernelInfoCache.has(sessionModel.kernel.name)) {
                return;
            }
            const session = serviceManager.sessions.connectTo({
                model: sessionModel,
                kernelConnectionOptions: { handleComms: false }
            });
            void ((_a = session.kernel) === null || _a === void 0 ? void 0 : _a.info.then(kernelInfo => {
                var _a, _b;
                const name = session.kernel.name;
                // Check the cache second time so that, if two callbacks get scheduled,
                // they don't try to add the same commands.
                if (kernelInfoCache.has(name)) {
                    return;
                }
                const spec = (_b = (_a = serviceManager.kernelspecs) === null || _a === void 0 ? void 0 : _a.specs) === null || _b === void 0 ? void 0 : _b.kernelspecs[name];
                if (!spec) {
                    return;
                }
                // Set the Kernel Info cache.
                kernelInfoCache.set(name, kernelInfo);
                // Utility function to check if the current widget
                // has registered itself with the help menu.
                let usesKernel = false;
                const onCurrentChanged = async () => {
                    const kernel = await commands.execute('helpmenu:get-kernel');
                    usesKernel = (kernel === null || kernel === void 0 ? void 0 : kernel.name) === name;
                };
                // Set the status for the current widget
                onCurrentChanged().catch(error => {
                    console.error('Failed to get the kernel for the current widget.', error);
                });
                if (labShell) {
                    // Update status when current widget changes
                    labShell.currentChanged.connect(onCurrentChanged);
                }
                const isEnabled = () => usesKernel;
                // Add the kernel banner to the Help Menu.
                const bannerCommand = `help-menu-${name}:banner`;
                const kernelName = spec.display_name;
                const kernelIconUrl = spec.resources['logo-svg'] || spec.resources['logo-64x64'];
                commands.addCommand(bannerCommand, {
                    label: trans.__('About the %1 Kernel', kernelName),
                    isVisible: isEnabled,
                    isEnabled,
                    execute: () => {
                        // Create the header of the about dialog
                        const headerLogo = react__WEBPACK_IMPORTED_MODULE_6__.createElement("img", { src: kernelIconUrl });
                        const title = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: "jp-About-header" },
                            headerLogo,
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-header-info" }, kernelName)));
                        const banner = react__WEBPACK_IMPORTED_MODULE_6__.createElement("pre", null, kernelInfo.banner);
                        const body = react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "jp-About-body" }, banner);
                        return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                            title,
                            body,
                            buttons: [
                                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.createButton({
                                    label: trans.__('Dismiss'),
                                    className: 'jp-About-button jp-mod-reject jp-mod-styled'
                                })
                            ]
                        });
                    }
                });
                helpMenu.addGroup([{ command: bannerCommand }], 20);
                // Add the kernel info help_links to the Help menu.
                const kernelGroup = [];
                (kernelInfo.help_links || []).forEach(link => {
                    const commandId = `help-menu-${name}:${link.text}`;
                    commands.addCommand(commandId, {
                        label: commands.label(CommandIDs.open, link),
                        isVisible: isEnabled,
                        isEnabled,
                        execute: () => {
                            return commands.execute(CommandIDs.open, link);
                        }
                    });
                    kernelGroup.push({ command: commandId });
                });
                helpMenu.addGroup(kernelGroup, 21);
            }).then(() => {
                // Dispose of the session object since we no longer need it.
                session.dispose();
            }));
        };
        // Create menu items for currently running sessions
        for (const model of serviceManager.sessions.running()) {
            onSessionRunningChanged(serviceManager.sessions, [model]);
        }
        serviceManager.sessions.runningChanged.connect(onSessionRunningChanged);
        if (palette) {
            resources.forEach(args => {
                palette.addItem({ args, command: CommandIDs.open, category });
            });
            palette.addItem({
                args: { reload: true },
                command: 'apputils:reset',
                category
            });
        }
    }
};
/**
 * A plugin to add a licenses reporting tools.
 */
const licenses = {
    id: '@jupyterlab/help-extension:licenses',
    description: 'Adds licenses used report tools.',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    activate: (app, translator, menu, palette, restorer) => {
        // bail if no license API is available from the server
        if (!_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('licensesUrl')) {
            return;
        }
        const { commands, shell } = app;
        const trans = translator.load('jupyterlab');
        // translation strings
        const category = trans.__('Help');
        const downloadAsText = trans.__('Download All Licenses as');
        const licensesText = trans.__('Licenses');
        const refreshLicenses = trans.__('Refresh Licenses');
        // an incrementer for license widget ids
        let counter = 0;
        const licensesUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getBaseUrl(), _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getOption('licensesUrl')) + '/';
        const licensesNamespace = 'help-licenses';
        const licensesTracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: licensesNamespace
        });
        /**
         * Return a full license report format based on a format name
         */
        function formatOrDefault(format) {
            return (_licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.REPORT_FORMATS[format] ||
                _licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.REPORT_FORMATS[_licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.DEFAULT_FORMAT]);
        }
        /**
         * Create a MainAreaWidget for a license viewer
         */
        function createLicenseWidget(args) {
            const licensesModel = new _licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.Model({
                ...args,
                licensesUrl,
                trans,
                serverSettings: app.serviceManager.serverSettings
            });
            const content = new _licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses({ model: licensesModel });
            content.id = `${licensesNamespace}-${++counter}`;
            content.title.label = licensesText;
            content.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.copyrightIcon;
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                content,
                reveal: licensesModel.licensesReady
            });
            main.toolbar.addItem('refresh-licenses', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.CommandToolbarButton({
                id: CommandIDs.refreshLicenses,
                args: { noLabel: 1 },
                commands
            }));
            main.toolbar.addItem('spacer', _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.Toolbar.createSpacerItem());
            for (const format of Object.keys(_licenses__WEBPACK_IMPORTED_MODULE_7__.Licenses.REPORT_FORMATS)) {
                const button = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.CommandToolbarButton({
                    id: CommandIDs.licenseReport,
                    args: { format, noLabel: 1 },
                    commands
                });
                main.toolbar.addItem(`download-${format}`, button);
            }
            return main;
        }
        // register license-related commands
        commands.addCommand(CommandIDs.licenses, {
            label: licensesText,
            execute: (args) => {
                const licenseMain = createLicenseWidget(args);
                shell.add(licenseMain, 'main', { type: 'Licenses' });
                // add to tracker so it can be restored, and update when choices change
                void licensesTracker.add(licenseMain);
                licenseMain.content.model.trackerDataChanged.connect(() => {
                    void licensesTracker.save(licenseMain);
                });
                return licenseMain;
            }
        });
        commands.addCommand(CommandIDs.refreshLicenses, {
            label: args => (args.noLabel ? '' : refreshLicenses),
            caption: refreshLicenses,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.refreshIcon,
            execute: async () => {
                var _a;
                return (_a = licensesTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.initLicenses();
            }
        });
        commands.addCommand(CommandIDs.licenseReport, {
            label: args => {
                if (args.noLabel) {
                    return '';
                }
                const format = formatOrDefault(`${args.format}`);
                return `${downloadAsText} ${format.title}`;
            },
            caption: args => {
                const format = formatOrDefault(`${args.format}`);
                return `${downloadAsText} ${format.title}`;
            },
            icon: args => {
                const format = formatOrDefault(`${args.format}`);
                return format.icon;
            },
            execute: async (args) => {
                var _a;
                const format = formatOrDefault(`${args.format}`);
                return await ((_a = licensesTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.download({
                    format: format.id
                }));
            }
        });
        // handle optional integrations
        if (palette) {
            palette.addItem({ command: CommandIDs.licenses, category });
        }
        if (menu) {
            const helpMenu = menu.helpMenu;
            helpMenu.addGroup([{ command: CommandIDs.licenses }], 0);
        }
        if (restorer) {
            void restorer.restore(licensesTracker, {
                command: CommandIDs.licenses,
                name: widget => 'licenses',
                args: widget => {
                    const { currentBundleName, currentPackageIndex, packageFilter } = widget.content.model;
                    const args = {
                        currentBundleName,
                        currentPackageIndex,
                        packageFilter
                    };
                    return args;
                }
            });
        }
    }
};
const plugins = [
    about,
    jupyterForum,
    open,
    resources,
    licenses
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "../packages/help-extension/lib/licenses.js":
/*!**************************************************!*\
  !*** ../packages/help-extension/lib/licenses.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Licenses": () => (/* binding */ Licenses)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/virtualdom */ "webpack/sharing/consume/default/@lumino/virtualdom/@lumino/virtualdom");
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_virtualdom__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







const FILTER_SECTION_TITLE_CLASS = 'jp-Licenses-Filters-title';
/**
 * A license viewer
 */
class Licenses extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.SplitPanel {
    constructor(options) {
        super();
        this.addClass('jp-Licenses');
        this.model = options.model;
        this.initLeftPanel();
        this.initFilters();
        this.initBundles();
        this.initGrid();
        this.initLicenseText();
        this.setRelativeSizes([1, 2, 3]);
        void this.model.initLicenses().then(() => this._updateBundles());
        this.model.trackerDataChanged.connect(() => {
            this.title.label = this.model.title;
        });
    }
    /**
     * Handle disposing of the widget
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._bundles.currentChanged.disconnect(this.onBundleSelected, this);
        this.model.dispose();
        super.dispose();
    }
    /**
     * Initialize the left area for filters and bundles
     */
    initLeftPanel() {
        this._leftPanel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Panel();
        this._leftPanel.addClass('jp-Licenses-FormArea');
        this.addWidget(this._leftPanel);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.SplitPanel.setStretch(this._leftPanel, 1);
    }
    /**
     * Initialize the filters
     */
    initFilters() {
        this._filters = new Licenses.Filters(this.model);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.SplitPanel.setStretch(this._filters, 1);
        this._leftPanel.addWidget(this._filters);
    }
    /**
     * Initialize the listing of available bundles
     */
    initBundles() {
        this._bundles = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.TabBar({
            orientation: 'vertical',
            renderer: new Licenses.BundleTabRenderer(this.model)
        });
        this._bundles.addClass('jp-Licenses-Bundles');
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.SplitPanel.setStretch(this._bundles, 1);
        this._leftPanel.addWidget(this._bundles);
        this._bundles.currentChanged.connect(this.onBundleSelected, this);
        this.model.stateChanged.connect(() => this._bundles.update());
    }
    /**
     * Initialize the listing of packages within the current bundle
     */
    initGrid() {
        this._grid = new Licenses.Grid(this.model);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.SplitPanel.setStretch(this._grid, 1);
        this.addWidget(this._grid);
    }
    /**
     * Initialize the full text of the current package
     */
    initLicenseText() {
        this._licenseText = new Licenses.FullText(this.model);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.SplitPanel.setStretch(this._grid, 1);
        this.addWidget(this._licenseText);
    }
    /**
     * Event handler for updating the model with the current bundle
     */
    onBundleSelected() {
        var _a;
        if ((_a = this._bundles.currentTitle) === null || _a === void 0 ? void 0 : _a.label) {
            this.model.currentBundleName = this._bundles.currentTitle.label;
        }
    }
    /**
     * Update the bundle tabs.
     */
    _updateBundles() {
        this._bundles.clearTabs();
        let i = 0;
        const { currentBundleName } = this.model;
        let currentIndex = 0;
        for (const bundle of this.model.bundleNames) {
            const tab = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget();
            tab.title.label = bundle;
            if (bundle === currentBundleName) {
                currentIndex = i;
            }
            this._bundles.insertTab(++i, tab.title);
        }
        this._bundles.currentIndex = currentIndex;
    }
}
/** A namespace for license components */
(function (Licenses) {
    /**
     * License report formats understood by the server (once lower-cased)
     */
    Licenses.REPORT_FORMATS = {
        markdown: {
            id: 'markdown',
            title: 'Markdown',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.markdownIcon
        },
        csv: {
            id: 'csv',
            title: 'CSV',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.spreadsheetIcon
        },
        json: {
            id: 'csv',
            title: 'JSON',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.jsonIcon
        }
    };
    /**
     * The default format (most human-readable)
     */
    Licenses.DEFAULT_FORMAT = 'markdown';
    /**
     * A model for license data
     */
    class Model extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.VDomModel {
        constructor(options) {
            super();
            this._selectedPackageChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
            this._trackerDataChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
            this._currentPackageIndex = 0;
            this._licensesReady = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.PromiseDelegate();
            this._packageFilter = {};
            this._trans = options.trans;
            this._licensesUrl = options.licensesUrl;
            this._serverSettings =
                options.serverSettings || _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
            if (options.currentBundleName) {
                this._currentBundleName = options.currentBundleName;
            }
            if (options.packageFilter) {
                this._packageFilter = options.packageFilter;
            }
            if (options.currentPackageIndex) {
                this._currentPackageIndex = options.currentPackageIndex;
            }
        }
        /**
         * Handle the initial request for the licenses from the server.
         */
        async initLicenses() {
            try {
                const response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(this._licensesUrl, {}, this._serverSettings);
                this._serverResponse = await response.json();
                this._licensesReady.resolve();
                this.stateChanged.emit(void 0);
            }
            catch (err) {
                this._licensesReady.reject(err);
            }
        }
        /**
         * Create a temporary download link, and emulate clicking it to trigger a named
         * file download.
         */
        async download(options) {
            const url = `${this._licensesUrl}?format=${options.format}&download=1`;
            const element = document.createElement('a');
            element.href = url;
            element.download = '';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            return void 0;
        }
        /**
         * A promise that resolves when the licenses from the server change
         */
        get selectedPackageChanged() {
            return this._selectedPackageChanged;
        }
        /**
         * A promise that resolves when the trackable data changes
         */
        get trackerDataChanged() {
            return this._trackerDataChanged;
        }
        /**
         * The names of the license bundles available
         */
        get bundleNames() {
            var _a;
            return Object.keys(((_a = this._serverResponse) === null || _a === void 0 ? void 0 : _a.bundles) || {});
        }
        /**
         * The current license bundle
         */
        get currentBundleName() {
            if (this._currentBundleName) {
                return this._currentBundleName;
            }
            if (this.bundleNames.length) {
                return this.bundleNames[0];
            }
            return null;
        }
        /**
         * Set the current license bundle, and reset the selected index
         */
        set currentBundleName(currentBundleName) {
            if (this._currentBundleName !== currentBundleName) {
                this._currentBundleName = currentBundleName;
                this.stateChanged.emit(void 0);
                this._trackerDataChanged.emit(void 0);
            }
        }
        /**
         * A promise that resolves when the licenses are available from the server
         */
        get licensesReady() {
            return this._licensesReady.promise;
        }
        /**
         * All the license bundles, keyed by the distributing packages
         */
        get bundles() {
            var _a;
            return ((_a = this._serverResponse) === null || _a === void 0 ? void 0 : _a.bundles) || {};
        }
        /**
         * The index of the currently-selected package within its license bundle
         */
        get currentPackageIndex() {
            return this._currentPackageIndex;
        }
        /**
         * Update the currently-selected package within its license bundle
         */
        set currentPackageIndex(currentPackageIndex) {
            if (this._currentPackageIndex === currentPackageIndex) {
                return;
            }
            this._currentPackageIndex = currentPackageIndex;
            this._selectedPackageChanged.emit(void 0);
            this.stateChanged.emit(void 0);
            this._trackerDataChanged.emit(void 0);
        }
        /**
         * The license data for the currently-selected package
         */
        get currentPackage() {
            var _a;
            if (this.currentBundleName &&
                this.bundles &&
                this._currentPackageIndex != null) {
                return this.getFilteredPackages(((_a = this.bundles[this.currentBundleName]) === null || _a === void 0 ? void 0 : _a.packages) || [])[this._currentPackageIndex];
            }
            return null;
        }
        /**
         * A translation bundle
         */
        get trans() {
            return this._trans;
        }
        get title() {
            return `${this._currentBundleName || ''} ${this._trans.__('Licenses')}`.trim();
        }
        /**
         * The current package filter
         */
        get packageFilter() {
            return this._packageFilter;
        }
        set packageFilter(packageFilter) {
            this._packageFilter = packageFilter;
            this.stateChanged.emit(void 0);
            this._trackerDataChanged.emit(void 0);
        }
        /**
         * Get filtered packages from current bundle where at least one token of each
         * key is present.
         */
        getFilteredPackages(allRows) {
            let rows = [];
            let filters = Object.entries(this._packageFilter)
                .filter(([k, v]) => v && `${v}`.trim().length)
                .map(([k, v]) => [k, `${v}`.toLowerCase().trim().split(' ')]);
            for (const row of allRows) {
                let keyHits = 0;
                for (const [key, bits] of filters) {
                    let bitHits = 0;
                    let rowKeyValue = `${row[key]}`.toLowerCase();
                    for (const bit of bits) {
                        if (rowKeyValue.includes(bit)) {
                            bitHits += 1;
                        }
                    }
                    if (bitHits) {
                        keyHits += 1;
                    }
                }
                if (keyHits === filters.length) {
                    rows.push(row);
                }
            }
            return Object.values(rows);
        }
    }
    Licenses.Model = Model;
    /**
     * A filter form for limiting the packages displayed
     */
    class Filters extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.VDomRenderer {
        constructor(model) {
            super(model);
            /**
             * Render a filter input
             */
            this.renderFilter = (key) => {
                const value = this.model.packageFilter[key] || '';
                return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("input", { type: "text", name: key, defaultValue: value, className: "jp-mod-styled", onInput: this.onFilterInput }));
            };
            /**
             * Handle a filter input changing
             */
            this.onFilterInput = (evt) => {
                const input = evt.currentTarget;
                const { name, value } = input;
                this.model.packageFilter = { ...this.model.packageFilter, [name]: value };
            };
            this.addClass('jp-Licenses-Filters');
            this.addClass('jp-RenderedHTMLCommon');
        }
        render() {
            const { trans } = this.model;
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("strong", { className: FILTER_SECTION_TITLE_CLASS }, trans.__('Filter Licenses By'))),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("ul", null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("li", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null, trans.__('Package')),
                        this.renderFilter('name')),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("li", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null, trans.__('Version')),
                        this.renderFilter('versionInfo')),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("li", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null, trans.__('License')),
                        this.renderFilter('licenseId'))),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("strong", { className: FILTER_SECTION_TITLE_CLASS }, trans.__('Distributions')))));
        }
    }
    Licenses.Filters = Filters;
    /**
     * A fancy bundle renderer with the package count
     */
    class BundleTabRenderer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.TabBar.Renderer {
        constructor(model) {
            super();
            this.closeIconSelector = '.lm-TabBar-tabCloseIcon';
            this.model = model;
        }
        /**
         * Render a full bundle
         */
        renderTab(data) {
            let title = data.title.caption;
            let key = this.createTabKey(data);
            let style = this.createTabStyle(data);
            let className = this.createTabClass(data);
            let dataset = this.createTabDataset(data);
            return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_4__.h.li({ key, className, title, style, dataset }, this.renderIcon(data), this.renderLabel(data), this.renderCountBadge(data));
        }
        /**
         * Render the package count
         */
        renderCountBadge(data) {
            const bundle = data.title.label;
            const { bundles } = this.model;
            const packages = this.model.getFilteredPackages((bundles && bundle ? bundles[bundle].packages : []) || []);
            return _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_4__.h.label({}, `${packages.length}`);
        }
    }
    Licenses.BundleTabRenderer = BundleTabRenderer;
    /**
     * A grid of licenses
     */
    class Grid extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.VDomRenderer {
        constructor(model) {
            super(model);
            /**
             * Render a single package's license information
             */
            this.renderRow = (row, index) => {
                const selected = index === this.model.currentPackageIndex;
                const onCheck = () => (this.model.currentPackageIndex = index);
                return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", { key: row.name, className: selected ? 'jp-mod-selected' : '', onClick: onCheck },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("input", { type: "radio", name: "show-package-license", value: index, onChange: onCheck, checked: selected })),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, row.name),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("code", null, row.versionInfo)),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("code", null, row.licenseId))));
            };
            this.addClass('jp-Licenses-Grid');
            this.addClass('jp-RenderedHTMLCommon');
        }
        /**
         * Render a grid of package license information
         */
        render() {
            var _a;
            const { bundles, currentBundleName, trans } = this.model;
            const filteredPackages = this.model.getFilteredPackages(bundles && currentBundleName
                ? ((_a = bundles[currentBundleName]) === null || _a === void 0 ? void 0 : _a.packages) || []
                : []);
            if (!filteredPackages.length) {
                return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("blockquote", null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("em", null, trans.__('No Packages found'))));
            }
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("form", null,
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("table", null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("thead", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", null,
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null),
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, trans.__('Package')),
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, trans.__('Version')),
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, trans.__('License')))),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("tbody", null, filteredPackages.map(this.renderRow)))));
        }
    }
    Licenses.Grid = Grid;
    /**
     * A package's full license text
     */
    class FullText extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.VDomRenderer {
        constructor(model) {
            super(model);
            this.addClass('jp-Licenses-Text');
            this.addClass('jp-RenderedHTMLCommon');
            this.addClass('jp-RenderedMarkdown');
        }
        /**
         * Render the license text, or a null state if no package is selected
         */
        render() {
            const { currentPackage, trans } = this.model;
            let head = '';
            let quote = trans.__('No Package selected');
            let code = '';
            if (currentPackage) {
                const { name, versionInfo, licenseId, extractedText } = currentPackage;
                head = `${name} v${versionInfo}`;
                quote = `${trans.__('License')}: ${licenseId || trans.__('No License ID found')}`;
                code = extractedText || trans.__('No License Text found');
            }
            return [
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("h1", { key: "h1" }, head),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("blockquote", { key: "quote" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("em", null, quote)),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("code", { key: "code" }, code)
            ];
        }
    }
    Licenses.FullText = FullText;
})(Licenses || (Licenses = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaGVscC1leHRlbnNpb25fbGliX2luZGV4X2pzLjlkNjM3OTg3YmYyMzU4ZDMzMzllLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU84QjtBQU9IO0FBQzZCO0FBQ1Y7QUFFSztBQVNuQjtBQUdKO0FBQ087QUFFdEM7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FvQm5CO0FBcEJELFdBQVUsVUFBVTtJQUNMLGVBQUksR0FBRyxXQUFXLENBQUM7SUFFbkIsZ0JBQUssR0FBRyxZQUFZLENBQUM7SUFFckIsbUJBQVEsR0FBRyxlQUFlLENBQUM7SUFFM0IsZ0JBQUssR0FBRyxZQUFZLENBQUM7SUFFckIsZUFBSSxHQUFHLFdBQVcsQ0FBQztJQUVuQixlQUFJLEdBQUcsV0FBVyxDQUFDO0lBRW5CLHVCQUFZLEdBQUcsb0JBQW9CLENBQUM7SUFFcEMsbUJBQVEsR0FBRyxlQUFlLENBQUM7SUFFM0Isd0JBQWEsR0FBRyxxQkFBcUIsQ0FBQztJQUV0QywwQkFBZSxHQUFHLHVCQUF1QixDQUFDO0FBQ3pELENBQUMsRUFwQlMsVUFBVSxLQUFWLFVBQVUsUUFvQm5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLGFBQWEsR0FBRyxNQUFNLENBQUMsUUFBUSxDQUFDLFFBQVEsS0FBSyxRQUFRLENBQUM7QUFFNUQ7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBRyxTQUFTLENBQUM7QUFFN0I7O0dBRUc7QUFDSCxNQUFNLEtBQUssR0FBZ0M7SUFDekMsRUFBRSxFQUFFLGtDQUFrQztJQUN0QyxXQUFXLEVBQUUsZ0NBQWdDO0lBQzdDLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUUsQ0FBQyxpRUFBZSxDQUFDO0lBQzNCLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLFVBQXVCLEVBQ3ZCLE9BQStCLEVBQ3pCLEVB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LGFBQWEsRUFBRSxHQUFHLGNBQWMsQ0FBQztnQkFDdkUsSUFBSSxHQUFHLEdBQUcsSUFBSSxLQUFLLFdBQVcsRUFBRSxDQUFDO2dCQUNqQyxLQUFLLEdBQUcsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUFDLFNBQVMsQ0FBQyxLQUM1QixTQUFTLElBQUksS0FBSyxDQUFDLEVBQUUsQ0FBQyxxQkFBcUIsQ0FDN0MsRUFBRSxDQUFDO2dCQUNILElBQUksR0FBRyxhQUFhLElBQUksS0FBSyxDQUFDLEVBQUUsQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDO2FBQzNEO1lBQ0QsT0FBTztnQkFDTCx5REFBSSxHQUFHLEVBQUMsSUFBSSxJQUFFLElBQUksQ0FBTTtnQkFDeEIsaUVBQVksR0FBRyxFQUFDLE9BQU87b0JBQ3JCLDZEQUFLLEtBQUssQ0FBTSxDQUNMO2dCQUNiLDJEQUFNLEdBQUcsRUFBQyxNQUFNLElBQUUsSUFBSSxDQUFRO2FBQy9CLENBQUM7UUFDSixDQUFDO0tBQ0Y7SUFoQ1ksaUJBQVEsV0FnQ3BCO0FBQ0gsQ0FBQyxFQTFqQmdCLFFBQVEsS0FBUixRQUFRLFFBMGpCeEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaGVscC1leHRlbnNpb24vc3JjL2luZGV4LnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaGVscC1leHRlbnNpb24vc3JjL2xpY2Vuc2VzLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBoZWxwLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBEaWFsb2csXG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgTWFpbkFyZWFXaWRnZXQsXG4gIHNob3dEaWFsb2csXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgUGFnZUNvbmZpZywgVVJMRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IElNYWluTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL21haW5tZW51JztcbmltcG9ydCB7IEtlcm5lbCwgS2VybmVsTWVzc2FnZSwgU2Vzc2lvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgQ29tbWFuZFRvb2xiYXJCdXR0b24sXG4gIGNvcHlyaWdodEljb24sXG4gIElGcmFtZSxcbiAganVweXRlckljb24sXG4gIGp1cHl0ZXJsYWJXb3JkbWFya0ljb24sXG4gIHJlZnJlc2hJY29uLFxuICBUb29sYmFyXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgUmVhZG9ubHlKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgTWVudSB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgeyBMaWNlbnNlcyB9IGZyb20gJy4vbGljZW5zZXMnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBoZWxwIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdoZWxwOm9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBhYm91dCA9ICdoZWxwOmFib3V0JztcblxuICBleHBvcnQgY29uc3QgYWN0aXZhdGUgPSAnaGVscDphY3RpdmF0ZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGNsb3NlID0gJ2hlbHA6Y2xvc2UnO1xuXG4gIGV4cG9ydCBjb25zdCBzaG93ID0gJ2hlbHA6c2hvdyc7XG5cbiAgZXhwb3J0IGNvbnN0IGhpZGUgPSAnaGVscDpoaWRlJztcblxuICBleHBvcnQgY29uc3QganVweXRlckZvcnVtID0gJ2hlbHA6anVweXRlci1mb3J1bSc7XG5cbiAgZXhwb3J0IGNvbnN0IGxpY2Vuc2VzID0gJ2hlbHA6bGljZW5zZXMnO1xuXG4gIGV4cG9ydCBjb25zdCBsaWNlbnNlUmVwb3J0ID0gJ2hlbHA6bGljZW5zZS1yZXBvcnQnO1xuXG4gIGV4cG9ydCBjb25zdCByZWZyZXNoTGljZW5zZXMgPSAnaGVscDpsaWNlbnNlcy1yZWZyZXNoJztcbn1cblxuLyoqXG4gKiBBIGZsYWcgZGVub3Rpbmcgd2hldGhlciB0aGUgYXBwbGljYXRpb24gaXMgbG9hZGVkIG92ZXIgSFRUUFMuXG4gKi9cbmNvbnN0IExBQl9JU19TRUNVUkUgPSB3aW5kb3cubG9jYXRpb24ucHJvdG9jb2wgPT09ICdodHRwczonO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSBoZWxwIHdpZGdldC5cbiAqL1xuY29uc3QgSEVMUF9DTEFTUyA9ICdqcC1IZWxwJztcblxuLyoqXG4gKiBBZGQgYSBjb21tYW5kIHRvIHNob3cgYW4gQWJvdXQgZGlhbG9nLlxuICovXG5jb25zdCBhYm91dDogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2hlbHAtZXh0ZW5zaW9uOmFib3V0JyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIGEgXCJBYm91dFwiIGRpYWxvZyBmZWF0dXJlLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0hlbHAnKTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5hYm91dCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdBYm91dCAlMScsIGFwcC5uYW1lKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgLy8gQ3JlYXRlIHRoZSBoZWFkZXIgb2YgdGhlIGFib3V0IGRpYWxvZ1xuICAgICAgICBjb25zdCB2ZXJzaW9uTnVtYmVyID0gdHJhbnMuX18oJ1ZlcnNpb24gJTEnLCBhcHAudmVyc2lvbik7XG4gICAgICAgIGNvbnN0IHZlcnNpb25JbmZvID0gKFxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cImpwLUFib3V0LXZlcnNpb24taW5mb1wiPlxuICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwianAtQWJvdXQtdmVyc2lvblwiPnt2ZXJzaW9uTnVtYmVyfTwvc3Bhbj5cbiAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICk7XG4gICAgICAgIGNvbnN0IHRpdGxlID0gKFxuICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cImpwLUFib3V0LWhlYWRlclwiPlxuICAgICAgICAgICAgPGp1cHl0ZXJJY29uLnJlYWN0IG1hcmdpbj1cIjdweCA5LjVweFwiIGhlaWdodD1cImF1dG9cIiB3aWR0aD1cIjU4cHhcIiAvPlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1BYm91dC1oZWFkZXItaW5mb1wiPlxuICAgICAgICAgICAgICA8anVweXRlcmxhYldvcmRtYXJrSWNvbi5yZWFjdCBoZWlnaHQ9XCJhdXRvXCIgd2lkdGg9XCIxOTZweFwiIC8+XG4gICAgICAgICAgICAgIHt2ZXJzaW9uSW5mb31cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgKTtcblxuICAgICAgICAvLyBDcmVhdGUgdGhlIGJvZHkgb2YgdGhlIGFib3V0IGRpYWxvZ1xuICAgICAgICBjb25zdCBqdXB5dGVyVVJMID0gJ2h0dHBzOi8vanVweXRlci5vcmcvYWJvdXQuaHRtbCc7XG4gICAgICAgIGNvbnN0IGNvbnRyaWJ1dG9yc1VSTCA9XG4gICAgICAgICAgJ2h0dHBzOi8vZ2l0aHViLmNvbS9qdXB5dGVybGFiL2p1cHl0ZXJsYWIvZ3JhcGhzL2NvbnRyaWJ1dG9ycyc7XG4gICAgICAgIGNvbnN0IGV4dGVybmFsTGlua3MgPSAoXG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwianAtQWJvdXQtZXh0ZXJuYWxMaW5rc1wiPlxuICAgICAgICAgICAgPGFcbiAgICAgICAgICAgICAgaHJlZj17Y29udHJpYnV0b3JzVVJMfVxuICAgICAgICAgICAgICB0YXJnZXQ9XCJfYmxhbmtcIlxuICAgICAgICAgICAgICByZWw9XCJub29wZW5lciBub3JlZmVycmVyXCJcbiAgICAgICAgICAgICAgY2xhc3NOYW1lPVwianAtQnV0dG9uLWZsYXRcIlxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICB7dHJhbnMuX18oJ0NPTlRSSUJVVE9SIExJU1QnKX1cbiAgICAgICAgICAgIDwvYT5cbiAgICAgICAgICAgIDxhXG4gICAgICAgICAgICAgIGhyZWY9e2p1cHl0ZXJVUkx9XG4gICAgICAgICAgICAgIHRhcmdldD1cIl9ibGFua1wiXG4gICAgICAgICAgICAgIHJlbD1cIm5vb3BlbmVyIG5vcmVmZXJyZXJcIlxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1CdXR0b24tZmxhdFwiXG4gICAgICAgICAgICA+XG4gICAgICAgICAgICAgIHt0cmFucy5fXygnQUJPVVQgUFJPSkVDVCBKVVBZVEVSJyl9XG4gICAgICAgICAgICA8L2E+XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICApO1xuICAgICAgICBjb25zdCBjb3B5cmlnaHQgPSAoXG4gICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwianAtQWJvdXQtY29weXJpZ2h0XCI+XG4gICAgICAgICAgICB7dHJhbnMuX18oJ8KpIDIwMTUtMjAyMyBQcm9qZWN0IEp1cHl0ZXIgQ29udHJpYnV0b3JzJyl9XG4gICAgICAgICAgPC9zcGFuPlxuICAgICAgICApO1xuICAgICAgICBjb25zdCBib2R5ID0gKFxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtQWJvdXQtYm9keVwiPlxuICAgICAgICAgICAge2V4dGVybmFsTGlua3N9XG4gICAgICAgICAgICB7Y29weXJpZ2h0fVxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuXG4gICAgICAgIHJldHVybiBzaG93RGlhbG9nKHtcbiAgICAgICAgICB0aXRsZSxcbiAgICAgICAgICBib2R5LFxuICAgICAgICAgIGJ1dHRvbnM6IFtcbiAgICAgICAgICAgIERpYWxvZy5jcmVhdGVCdXR0b24oe1xuICAgICAgICAgICAgICBsYWJlbDogdHJhbnMuX18oJ0Rpc21pc3MnKSxcbiAgICAgICAgICAgICAgY2xhc3NOYW1lOiAnanAtQWJvdXQtYnV0dG9uIGpwLW1vZC1yZWplY3QganAtbW9kLXN0eWxlZCdcbiAgICAgICAgICAgIH0pXG4gICAgICAgICAgXVxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kOiBDb21tYW5kSURzLmFib3V0LCBjYXRlZ29yeSB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogQSBwbHVnaW4gdG8gYWRkIGEgY29tbWFuZCB0byBvcGVuIHRoZSBKdXB5dGVyIEZvcnVtLlxuICovXG5jb25zdCBqdXB5dGVyRm9ydW06IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9oZWxwLWV4dGVuc2lvbjpqdXB5dGVyLWZvcnVtJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIGNvbW1hbmQgdG8gb3BlbiB0aGUgSnVweXRlciBGb3J1bSB3ZWJzaXRlLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0hlbHAnKTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5qdXB5dGVyRm9ydW0sIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnSnVweXRlciBGb3J1bScpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICB3aW5kb3cub3BlbignaHR0cHM6Ly9kaXNjb3Vyc2UuanVweXRlci5vcmcvYy9qdXB5dGVybGFiJyk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZDogQ29tbWFuZElEcy5qdXB5dGVyRm9ydW0sIGNhdGVnb3J5IH0pO1xuICAgIH1cbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0byBvcGVuIHJlc291cmNlcyBpbiBJRnJhbWVzIG9yIG5ldyBicm93c2VyIHRhYnMuXG4gKi9cbmNvbnN0IG9wZW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9oZWxwLWV4dGVuc2lvbjpvcGVuJyxcbiAgZGVzY3JpcHRpb246ICdBZGQgY29tbWFuZCB0byBvcGVuIHdlYnNpdGVzIGFzIHBhbmVsIG9yIGJyb3dzZXIgdGFiLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxheW91dFJlc3RvcmVyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbFxuICApOiB2b2lkID0+IHtcbiAgICBjb25zdCB7IGNvbW1hbmRzLCBzaGVsbCB9ID0gYXBwO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgbmFtZXNwYWNlID0gJ2hlbHAtZG9jJztcblxuICAgIGNvbnN0IHRyYWNrZXIgPSBuZXcgV2lkZ2V0VHJhY2tlcjxNYWluQXJlYVdpZGdldDxJRnJhbWU+Pih7IG5hbWVzcGFjZSB9KTtcbiAgICBsZXQgY291bnRlciA9IDA7XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgSGVscFdpZGdldCB3aWRnZXQuXG4gICAgICovXG4gICAgZnVuY3Rpb24gbmV3SGVscFdpZGdldCh1cmw6IHN0cmluZywgdGV4dDogc3RyaW5nKTogTWFpbkFyZWFXaWRnZXQ8SUZyYW1lPiB7XG4gICAgICAvLyBBbGxvdyBzY3JpcHRzIGFuZCBmb3JtcyBzbyB0aGF0IHRoaW5ncyBsaWtlXG4gICAgICAvLyByZWFkdGhlZG9jcyBjYW4gdXNlIHRoZWlyIHNlYXJjaCBmdW5jdGlvbmFsaXR5LlxuICAgICAgLy8gV2UgKmRvbid0KiBhbGxvdyBzYW1lIG9yaWdpbiByZXF1ZXN0cywgd2hpY2hcbiAgICAgIC8vIGNhbiBwcmV2ZW50IHNvbWUgY29udGVudCBmcm9tIGJlaW5nIGxvYWRlZCBvbnRvIHRoZVxuICAgICAgLy8gaGVscCBwYWdlcy5cbiAgICAgIGNvbnN0IGNvbnRlbnQgPSBuZXcgSUZyYW1lKHtcbiAgICAgICAgc2FuZGJveDogWydhbGxvdy1zY3JpcHRzJywgJ2FsbG93LWZvcm1zJ11cbiAgICAgIH0pO1xuICAgICAgY29udGVudC51cmwgPSB1cmw7XG4gICAgICBjb250ZW50LmFkZENsYXNzKEhFTFBfQ0xBU1MpO1xuICAgICAgY29udGVudC50aXRsZS5sYWJlbCA9IHRleHQ7XG4gICAgICBjb250ZW50LmlkID0gYCR7bmFtZXNwYWNlfS0keysrY291bnRlcn1gO1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gbmV3IE1haW5BcmVhV2lkZ2V0KHsgY29udGVudCB9KTtcbiAgICAgIHdpZGdldC5hZGRDbGFzcygnanAtSGVscCcpO1xuICAgICAgcmV0dXJuIHdpZGdldDtcbiAgICB9XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbiwge1xuICAgICAgbGFiZWw6IGFyZ3MgPT5cbiAgICAgICAgKGFyZ3NbJ3RleHQnXSBhcyBzdHJpbmcpID8/XG4gICAgICAgIHRyYW5zLl9fKCdPcGVuIHRoZSBwcm92aWRlZCBgdXJsYCBpbiBhIHRhYi4nKSxcbiAgICAgIGV4ZWN1dGU6IGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCB1cmwgPSBhcmdzWyd1cmwnXSBhcyBzdHJpbmc7XG4gICAgICAgIGNvbnN0IHRleHQgPSBhcmdzWyd0ZXh0J10gYXMgc3RyaW5nO1xuICAgICAgICBjb25zdCBuZXdCcm93c2VyVGFiID0gKGFyZ3NbJ25ld0Jyb3dzZXJUYWInXSBhcyBib29sZWFuKSB8fCBmYWxzZTtcblxuICAgICAgICAvLyBJZiBoZWxwIHJlc291cmNlIHdpbGwgZ2VuZXJhdGUgYSBtaXhlZCBjb250ZW50IGVycm9yLCBsb2FkIGV4dGVybmFsbHkuXG4gICAgICAgIGlmIChcbiAgICAgICAgICBuZXdCcm93c2VyVGFiIHx8XG4gICAgICAgICAgKExBQl9JU19TRUNVUkUgJiYgVVJMRXh0LnBhcnNlKHVybCkucHJvdG9jb2wgIT09ICdodHRwczonKVxuICAgICAgICApIHtcbiAgICAgICAgICB3aW5kb3cub3Blbih1cmwpO1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IHdpZGdldCA9IG5ld0hlbHBXaWRnZXQodXJsLCB0ZXh0KTtcbiAgICAgICAgdm9pZCB0cmFja2VyLmFkZCh3aWRnZXQpO1xuICAgICAgICBzaGVsbC5hZGQod2lkZ2V0LCAnbWFpbicpO1xuICAgICAgICByZXR1cm4gd2lkZ2V0O1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gSGFuZGxlIHN0YXRlIHJlc3RvcmF0aW9uLlxuICAgIGlmIChyZXN0b3Jlcikge1xuICAgICAgdm9pZCByZXN0b3Jlci5yZXN0b3JlKHRyYWNrZXIsIHtcbiAgICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5vcGVuLFxuICAgICAgICBhcmdzOiB3aWRnZXQgPT4gKHtcbiAgICAgICAgICB1cmw6IHdpZGdldC5jb250ZW50LnVybCxcbiAgICAgICAgICB0ZXh0OiB3aWRnZXQuY29udGVudC50aXRsZS5sYWJlbFxuICAgICAgICB9KSxcbiAgICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb250ZW50LnVybFxuICAgICAgfSk7XG4gICAgfVxuICB9XG59O1xuXG4vKipcbiAqIEEgcGx1Z2luIHRvIGFkZCBhIGxpc3Qgb2YgcmVzb3VyY2VzIHRvIHRoZSBoZWxwIG1lbnUuXG4gKi9cbmNvbnN0IHJlc291cmNlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2hlbHAtZXh0ZW5zaW9uOnJlc291cmNlcycsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyBtZW51IGVudHJpZXMgdG8gSnVweXRlciByZWZlcmVuY2UgZG9jdW1lbnRhdGlvbiB3ZWJzaXRlcy4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSU1haW5NZW51LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsLCBJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1haW5NZW51OiBJTWFpbk1lbnUsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGwsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbFxuICApOiB2b2lkID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0hlbHAnKTtcbiAgICBjb25zdCB7IGNvbW1hbmRzLCBzZXJ2aWNlTWFuYWdlciB9ID0gYXBwO1xuICAgIGNvbnN0IHJlc291cmNlcyA9IFtcbiAgICAgIHtcbiAgICAgICAgdGV4dDogdHJhbnMuX18oJ0p1cHl0ZXJMYWIgUmVmZXJlbmNlJyksXG4gICAgICAgIHVybDogJ2h0dHBzOi8vanVweXRlcmxhYi5yZWFkdGhlZG9jcy5pby9lbi9sYXRlc3QvJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdGV4dDogdHJhbnMuX18oJ0p1cHl0ZXJMYWIgRkFRJyksXG4gICAgICAgIHVybDogJ2h0dHBzOi8vanVweXRlcmxhYi5yZWFkdGhlZG9jcy5pby9lbi9sYXRlc3QvZ2V0dGluZ19zdGFydGVkL2ZhcS5odG1sJ1xuICAgICAgfSxcbiAgICAgIHtcbiAgICAgICAgdGV4dDogdHJhbnMuX18oJ0p1cHl0ZXIgUmVmZXJlbmNlJyksXG4gICAgICAgIHVybDogJ2h0dHBzOi8vanVweXRlci5vcmcvZG9jdW1lbnRhdGlvbidcbiAgICAgIH0sXG4gICAgICB7XG4gICAgICAgIHRleHQ6IHRyYW5zLl9fKCdNYXJrZG93biBSZWZlcmVuY2UnKSxcbiAgICAgICAgdXJsOiAnaHR0cHM6Ly9jb21tb25tYXJrLm9yZy9oZWxwLydcbiAgICAgIH1cbiAgICBdO1xuXG4gICAgcmVzb3VyY2VzLnNvcnQoKGE6IGFueSwgYjogYW55KSA9PiB7XG4gICAgICByZXR1cm4gYS50ZXh0LmxvY2FsZUNvbXBhcmUoYi50ZXh0KTtcbiAgICB9KTtcblxuICAgIC8vIFBvcHVsYXRlIHRoZSBIZWxwIG1lbnUuXG4gICAgY29uc3QgaGVscE1lbnUgPSBtYWluTWVudS5oZWxwTWVudTtcblxuICAgIGNvbnN0IHJlc291cmNlc0dyb3VwID0gcmVzb3VyY2VzLm1hcChhcmdzID0+ICh7XG4gICAgICBhcmdzLFxuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5vcGVuXG4gICAgfSkpO1xuICAgIGhlbHBNZW51LmFkZEdyb3VwKHJlc291cmNlc0dyb3VwLCAxMCk7XG5cbiAgICAvLyBHZW5lcmF0ZSBhIGNhY2hlIG9mIHRoZSBrZXJuZWwgaGVscCBsaW5rcy5cbiAgICBjb25zdCBrZXJuZWxJbmZvQ2FjaGUgPSBuZXcgTWFwPFxuICAgICAgc3RyaW5nLFxuICAgICAgS2VybmVsTWVzc2FnZS5JSW5mb1JlcGx5TXNnWydjb250ZW50J11cbiAgICA+KCk7XG5cbiAgICBjb25zdCBvblNlc3Npb25SdW5uaW5nQ2hhbmdlZCA9IChcbiAgICAgIG06IFNlc3Npb24uSU1hbmFnZXIsXG4gICAgICBzZXNzaW9uczogU2Vzc2lvbi5JTW9kZWxbXVxuICAgICkgPT4ge1xuICAgICAgLy8gSWYgYSBuZXcgc2Vzc2lvbiBoYXMgYmVlbiBhZGRlZCwgaXQgaXMgYXQgdGhlIGJhY2tcbiAgICAgIC8vIG9mIHRoZSBzZXNzaW9uIGxpc3QuIElmIG9uZSBoYXMgY2hhbmdlZCBvciBzdG9wcGVkLFxuICAgICAgLy8gaXQgZG9lcyBub3QgaHVydCB0byBjaGVjayBpdC5cbiAgICAgIGlmICghc2Vzc2lvbnMubGVuZ3RoKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHNlc3Npb25Nb2RlbCA9IHNlc3Npb25zW3Nlc3Npb25zLmxlbmd0aCAtIDFdO1xuICAgICAgaWYgKFxuICAgICAgICAhc2Vzc2lvbk1vZGVsLmtlcm5lbCB8fFxuICAgICAgICBrZXJuZWxJbmZvQ2FjaGUuaGFzKHNlc3Npb25Nb2RlbC5rZXJuZWwubmFtZSlcbiAgICAgICkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjb25zdCBzZXNzaW9uID0gc2VydmljZU1hbmFnZXIuc2Vzc2lvbnMuY29ubmVjdFRvKHtcbiAgICAgICAgbW9kZWw6IHNlc3Npb25Nb2RlbCxcbiAgICAgICAga2VybmVsQ29ubmVjdGlvbk9wdGlvbnM6IHsgaGFuZGxlQ29tbXM6IGZhbHNlIH1cbiAgICAgIH0pO1xuXG4gICAgICB2b2lkIHNlc3Npb24ua2VybmVsPy5pbmZvXG4gICAgICAgIC50aGVuKGtlcm5lbEluZm8gPT4ge1xuICAgICAgICAgIGNvbnN0IG5hbWUgPSBzZXNzaW9uLmtlcm5lbCEubmFtZTtcblxuICAgICAgICAgIC8vIENoZWNrIHRoZSBjYWNoZSBzZWNvbmQgdGltZSBzbyB0aGF0LCBpZiB0d28gY2FsbGJhY2tzIGdldCBzY2hlZHVsZWQsXG4gICAgICAgICAgLy8gdGhleSBkb24ndCB0cnkgdG8gYWRkIHRoZSBzYW1lIGNvbW1hbmRzLlxuICAgICAgICAgIGlmIChrZXJuZWxJbmZvQ2FjaGUuaGFzKG5hbWUpKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgY29uc3Qgc3BlYyA9IHNlcnZpY2VNYW5hZ2VyLmtlcm5lbHNwZWNzPy5zcGVjcz8ua2VybmVsc3BlY3NbbmFtZV07XG4gICAgICAgICAgaWYgKCFzcGVjKSB7XG4gICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgLy8gU2V0IHRoZSBLZXJuZWwgSW5mbyBjYWNoZS5cbiAgICAgICAgICBrZXJuZWxJbmZvQ2FjaGUuc2V0KG5hbWUsIGtlcm5lbEluZm8pO1xuXG4gICAgICAgICAgLy8gVXRpbGl0eSBmdW5jdGlvbiB0byBjaGVjayBpZiB0aGUgY3VycmVudCB3aWRnZXRcbiAgICAgICAgICAvLyBoYXMgcmVnaXN0ZXJlZCBpdHNlbGYgd2l0aCB0aGUgaGVscCBtZW51LlxuICAgICAgICAgIGxldCB1c2VzS2VybmVsID0gZmFsc2U7XG4gICAgICAgICAgY29uc3Qgb25DdXJyZW50Q2hhbmdlZCA9IGFzeW5jICgpID0+IHtcbiAgICAgICAgICAgIGNvbnN0IGtlcm5lbDogS2VybmVsLklLZXJuZWxDb25uZWN0aW9uIHwgbnVsbCA9XG4gICAgICAgICAgICAgIGF3YWl0IGNvbW1hbmRzLmV4ZWN1dGUoJ2hlbHBtZW51OmdldC1rZXJuZWwnKTtcbiAgICAgICAgICAgIHVzZXNLZXJuZWwgPSBrZXJuZWw/Lm5hbWUgPT09IG5hbWU7XG4gICAgICAgICAgfTtcbiAgICAgICAgICAvLyBTZXQgdGhlIHN0YXR1cyBmb3IgdGhlIGN1cnJlbnQgd2lkZ2V0XG4gICAgICAgICAgb25DdXJyZW50Q2hhbmdlZCgpLmNhdGNoKGVycm9yID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoXG4gICAgICAgICAgICAgICdGYWlsZWQgdG8gZ2V0IHRoZSBrZXJuZWwgZm9yIHRoZSBjdXJyZW50IHdpZGdldC4nLFxuICAgICAgICAgICAgICBlcnJvclxuICAgICAgICAgICAgKTtcbiAgICAgICAgICB9KTtcbiAgICAgICAgICBpZiAobGFiU2hlbGwpIHtcbiAgICAgICAgICAgIC8vIFVwZGF0ZSBzdGF0dXMgd2hlbiBjdXJyZW50IHdpZGdldCBjaGFuZ2VzXG4gICAgICAgICAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KG9uQ3VycmVudENoYW5nZWQpO1xuICAgICAgICAgIH1cbiAgICAgICAgICBjb25zdCBpc0VuYWJsZWQgPSAoKSA9PiB1c2VzS2VybmVsO1xuXG4gICAgICAgICAgLy8gQWRkIHRoZSBrZXJuZWwgYmFubmVyIHRvIHRoZSBIZWxwIE1lbnUuXG4gICAgICAgICAgY29uc3QgYmFubmVyQ29tbWFuZCA9IGBoZWxwLW1lbnUtJHtuYW1lfTpiYW5uZXJgO1xuICAgICAgICAgIGNvbnN0IGtlcm5lbE5hbWUgPSBzcGVjLmRpc3BsYXlfbmFtZTtcbiAgICAgICAgICBjb25zdCBrZXJuZWxJY29uVXJsID1cbiAgICAgICAgICAgIHNwZWMucmVzb3VyY2VzWydsb2dvLXN2ZyddIHx8IHNwZWMucmVzb3VyY2VzWydsb2dvLTY0eDY0J107XG4gICAgICAgICAgY29tbWFuZHMuYWRkQ29tbWFuZChiYW5uZXJDb21tYW5kLCB7XG4gICAgICAgICAgICBsYWJlbDogdHJhbnMuX18oJ0Fib3V0IHRoZSAlMSBLZXJuZWwnLCBrZXJuZWxOYW1lKSxcbiAgICAgICAgICAgIGlzVmlzaWJsZTogaXNFbmFibGVkLFxuICAgICAgICAgICAgaXNFbmFibGVkLFxuICAgICAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgICAgICAvLyBDcmVhdGUgdGhlIGhlYWRlciBvZiB0aGUgYWJvdXQgZGlhbG9nXG4gICAgICAgICAgICAgIGNvbnN0IGhlYWRlckxvZ28gPSA8aW1nIHNyYz17a2VybmVsSWNvblVybH0gLz47XG4gICAgICAgICAgICAgIGNvbnN0IHRpdGxlID0gKFxuICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cImpwLUFib3V0LWhlYWRlclwiPlxuICAgICAgICAgICAgICAgICAge2hlYWRlckxvZ299XG4gICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUFib3V0LWhlYWRlci1pbmZvXCI+e2tlcm5lbE5hbWV9PC9kaXY+XG4gICAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICBjb25zdCBiYW5uZXIgPSA8cHJlPntrZXJuZWxJbmZvLmJhbm5lcn08L3ByZT47XG4gICAgICAgICAgICAgIGNvbnN0IGJvZHkgPSA8ZGl2IGNsYXNzTmFtZT1cImpwLUFib3V0LWJvZHlcIj57YmFubmVyfTwvZGl2PjtcblxuICAgICAgICAgICAgICByZXR1cm4gc2hvd0RpYWxvZyh7XG4gICAgICAgICAgICAgICAgdGl0bGUsXG4gICAgICAgICAgICAgICAgYm9keSxcbiAgICAgICAgICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgICAgICAgICBEaWFsb2cuY3JlYXRlQnV0dG9uKHtcbiAgICAgICAgICAgICAgICAgICAgbGFiZWw6IHRyYW5zLl9fKCdEaXNtaXNzJyksXG4gICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZTogJ2pwLUFib3V0LWJ1dHRvbiBqcC1tb2QtcmVqZWN0IGpwLW1vZC1zdHlsZWQnXG4gICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgIF1cbiAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSk7XG4gICAgICAgICAgaGVscE1lbnUuYWRkR3JvdXAoW3sgY29tbWFuZDogYmFubmVyQ29tbWFuZCB9XSwgMjApO1xuXG4gICAgICAgICAgLy8gQWRkIHRoZSBrZXJuZWwgaW5mbyBoZWxwX2xpbmtzIHRvIHRoZSBIZWxwIG1lbnUuXG4gICAgICAgICAgY29uc3Qga2VybmVsR3JvdXA6IE1lbnUuSUl0ZW1PcHRpb25zW10gPSBbXTtcbiAgICAgICAgICAoa2VybmVsSW5mby5oZWxwX2xpbmtzIHx8IFtdKS5mb3JFYWNoKGxpbmsgPT4ge1xuICAgICAgICAgICAgY29uc3QgY29tbWFuZElkID0gYGhlbHAtbWVudS0ke25hbWV9OiR7bGluay50ZXh0fWA7XG4gICAgICAgICAgICBjb21tYW5kcy5hZGRDb21tYW5kKGNvbW1hbmRJZCwge1xuICAgICAgICAgICAgICBsYWJlbDogY29tbWFuZHMubGFiZWwoQ29tbWFuZElEcy5vcGVuLCBsaW5rKSxcbiAgICAgICAgICAgICAgaXNWaXNpYmxlOiBpc0VuYWJsZWQsXG4gICAgICAgICAgICAgIGlzRW5hYmxlZCxcbiAgICAgICAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgICAgICAgIHJldHVybiBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMub3BlbiwgbGluayk7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAga2VybmVsR3JvdXAucHVzaCh7IGNvbW1hbmQ6IGNvbW1hbmRJZCB9KTtcbiAgICAgICAgICB9KTtcbiAgICAgICAgICBoZWxwTWVudS5hZGRHcm91cChrZXJuZWxHcm91cCwgMjEpO1xuICAgICAgICB9KVxuICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgLy8gRGlzcG9zZSBvZiB0aGUgc2Vzc2lvbiBvYmplY3Qgc2luY2Ugd2Ugbm8gbG9uZ2VyIG5lZWQgaXQuXG4gICAgICAgICAgc2Vzc2lvbi5kaXNwb3NlKCk7XG4gICAgICAgIH0pO1xuICAgIH07XG5cbiAgICAvLyBDcmVhdGUgbWVudSBpdGVtcyBmb3IgY3VycmVudGx5IHJ1bm5pbmcgc2Vzc2lvbnNcbiAgICBmb3IgKGNvbnN0IG1vZGVsIG9mIHNlcnZpY2VNYW5hZ2VyLnNlc3Npb25zLnJ1bm5pbmcoKSkge1xuICAgICAgb25TZXNzaW9uUnVubmluZ0NoYW5nZWQoc2VydmljZU1hbmFnZXIuc2Vzc2lvbnMsIFttb2RlbF0pO1xuICAgIH1cbiAgICBzZXJ2aWNlTWFuYWdlci5zZXNzaW9ucy5ydW5uaW5nQ2hhbmdlZC5jb25uZWN0KG9uU2Vzc2lvblJ1bm5pbmdDaGFuZ2VkKTtcblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICByZXNvdXJjZXMuZm9yRWFjaChhcmdzID0+IHtcbiAgICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgYXJncywgY29tbWFuZDogQ29tbWFuZElEcy5vcGVuLCBjYXRlZ29yeSB9KTtcbiAgICAgIH0pO1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgICAgYXJnczogeyByZWxvYWQ6IHRydWUgfSxcbiAgICAgICAgY29tbWFuZDogJ2FwcHV0aWxzOnJlc2V0JyxcbiAgICAgICAgY2F0ZWdvcnlcbiAgICAgIH0pO1xuICAgIH1cbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiB0byBhZGQgYSBsaWNlbnNlcyByZXBvcnRpbmcgdG9vbHMuXG4gKi9cbmNvbnN0IGxpY2Vuc2VzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvaGVscC1leHRlbnNpb246bGljZW5zZXMnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgbGljZW5zZXMgdXNlZCByZXBvcnQgdG9vbHMuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJTWFpbk1lbnUsIElDb21tYW5kUGFsZXR0ZSwgSUxheW91dFJlc3RvcmVyXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBtZW51OiBJTWFpbk1lbnUgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGwsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbiAgKSA9PiB7XG4gICAgLy8gYmFpbCBpZiBubyBsaWNlbnNlIEFQSSBpcyBhdmFpbGFibGUgZnJvbSB0aGUgc2VydmVyXG4gICAgaWYgKCFQYWdlQ29uZmlnLmdldE9wdGlvbignbGljZW5zZXNVcmwnKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsIH0gPSBhcHA7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIC8vIHRyYW5zbGF0aW9uIHN0cmluZ3NcbiAgICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdIZWxwJyk7XG4gICAgY29uc3QgZG93bmxvYWRBc1RleHQgPSB0cmFucy5fXygnRG93bmxvYWQgQWxsIExpY2Vuc2VzIGFzJyk7XG4gICAgY29uc3QgbGljZW5zZXNUZXh0ID0gdHJhbnMuX18oJ0xpY2Vuc2VzJyk7XG4gICAgY29uc3QgcmVmcmVzaExpY2Vuc2VzID0gdHJhbnMuX18oJ1JlZnJlc2ggTGljZW5zZXMnKTtcblxuICAgIC8vIGFuIGluY3JlbWVudGVyIGZvciBsaWNlbnNlIHdpZGdldCBpZHNcbiAgICBsZXQgY291bnRlciA9IDA7XG5cbiAgICBjb25zdCBsaWNlbnNlc1VybCA9XG4gICAgICBVUkxFeHQuam9pbihcbiAgICAgICAgUGFnZUNvbmZpZy5nZXRCYXNlVXJsKCksXG4gICAgICAgIFBhZ2VDb25maWcuZ2V0T3B0aW9uKCdsaWNlbnNlc1VybCcpXG4gICAgICApICsgJy8nO1xuXG4gICAgY29uc3QgbGljZW5zZXNOYW1lc3BhY2UgPSAnaGVscC1saWNlbnNlcyc7XG4gICAgY29uc3QgbGljZW5zZXNUcmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8TGljZW5zZXM+Pih7XG4gICAgICBuYW1lc3BhY2U6IGxpY2Vuc2VzTmFtZXNwYWNlXG4gICAgfSk7XG5cbiAgICAvKipcbiAgICAgKiBSZXR1cm4gYSBmdWxsIGxpY2Vuc2UgcmVwb3J0IGZvcm1hdCBiYXNlZCBvbiBhIGZvcm1hdCBuYW1lXG4gICAgICovXG4gICAgZnVuY3Rpb24gZm9ybWF0T3JEZWZhdWx0KGZvcm1hdDogc3RyaW5nKTogTGljZW5zZXMuSVJlcG9ydEZvcm1hdCB7XG4gICAgICByZXR1cm4gKFxuICAgICAgICBMaWNlbnNlcy5SRVBPUlRfRk9STUFUU1tmb3JtYXRdIHx8XG4gICAgICAgIExpY2Vuc2VzLlJFUE9SVF9GT1JNQVRTW0xpY2Vuc2VzLkRFRkFVTFRfRk9STUFUXVxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBNYWluQXJlYVdpZGdldCBmb3IgYSBsaWNlbnNlIHZpZXdlclxuICAgICAqL1xuICAgIGZ1bmN0aW9uIGNyZWF0ZUxpY2Vuc2VXaWRnZXQoYXJnczogTGljZW5zZXMuSUNyZWF0ZUFyZ3MpIHtcbiAgICAgIGNvbnN0IGxpY2Vuc2VzTW9kZWwgPSBuZXcgTGljZW5zZXMuTW9kZWwoe1xuICAgICAgICAuLi5hcmdzLFxuICAgICAgICBsaWNlbnNlc1VybCxcbiAgICAgICAgdHJhbnMsXG4gICAgICAgIHNlcnZlclNldHRpbmdzOiBhcHAuc2VydmljZU1hbmFnZXIuc2VydmVyU2V0dGluZ3NcbiAgICAgIH0pO1xuICAgICAgY29uc3QgY29udGVudCA9IG5ldyBMaWNlbnNlcyh7IG1vZGVsOiBsaWNlbnNlc01vZGVsIH0pO1xuICAgICAgY29udGVudC5pZCA9IGAke2xpY2Vuc2VzTmFtZXNwYWNlfS0keysrY291bnRlcn1gO1xuICAgICAgY29udGVudC50aXRsZS5sYWJlbCA9IGxpY2Vuc2VzVGV4dDtcbiAgICAgIGNvbnRlbnQudGl0bGUuaWNvbiA9IGNvcHlyaWdodEljb247XG4gICAgICBjb25zdCBtYWluID0gbmV3IE1haW5BcmVhV2lkZ2V0KHtcbiAgICAgICAgY29udGVudCxcbiAgICAgICAgcmV2ZWFsOiBsaWNlbnNlc01vZGVsLmxpY2Vuc2VzUmVhZHlcbiAgICAgIH0pO1xuXG4gICAgICBtYWluLnRvb2xiYXIuYWRkSXRlbShcbiAgICAgICAgJ3JlZnJlc2gtbGljZW5zZXMnLFxuICAgICAgICBuZXcgQ29tbWFuZFRvb2xiYXJCdXR0b24oe1xuICAgICAgICAgIGlkOiBDb21tYW5kSURzLnJlZnJlc2hMaWNlbnNlcyxcbiAgICAgICAgICBhcmdzOiB7IG5vTGFiZWw6IDEgfSxcbiAgICAgICAgICBjb21tYW5kc1xuICAgICAgICB9KVxuICAgICAgKTtcblxuICAgICAgbWFpbi50b29sYmFyLmFkZEl0ZW0oJ3NwYWNlcicsIFRvb2xiYXIuY3JlYXRlU3BhY2VySXRlbSgpKTtcblxuICAgICAgZm9yIChjb25zdCBmb3JtYXQgb2YgT2JqZWN0LmtleXMoTGljZW5zZXMuUkVQT1JUX0ZPUk1BVFMpKSB7XG4gICAgICAgIGNvbnN0IGJ1dHRvbiA9IG5ldyBDb21tYW5kVG9vbGJhckJ1dHRvbih7XG4gICAgICAgICAgaWQ6IENvbW1hbmRJRHMubGljZW5zZVJlcG9ydCxcbiAgICAgICAgICBhcmdzOiB7IGZvcm1hdCwgbm9MYWJlbDogMSB9LFxuICAgICAgICAgIGNvbW1hbmRzXG4gICAgICAgIH0pO1xuICAgICAgICBtYWluLnRvb2xiYXIuYWRkSXRlbShgZG93bmxvYWQtJHtmb3JtYXR9YCwgYnV0dG9uKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIG1haW47XG4gICAgfVxuXG4gICAgLy8gcmVnaXN0ZXIgbGljZW5zZS1yZWxhdGVkIGNvbW1hbmRzXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxpY2Vuc2VzLCB7XG4gICAgICBsYWJlbDogbGljZW5zZXNUZXh0LFxuICAgICAgZXhlY3V0ZTogKGFyZ3M6IGFueSkgPT4ge1xuICAgICAgICBjb25zdCBsaWNlbnNlTWFpbiA9IGNyZWF0ZUxpY2Vuc2VXaWRnZXQoYXJncyBhcyBMaWNlbnNlcy5JQ3JlYXRlQXJncyk7XG4gICAgICAgIHNoZWxsLmFkZChsaWNlbnNlTWFpbiwgJ21haW4nLCB7IHR5cGU6ICdMaWNlbnNlcycgfSk7XG5cbiAgICAgICAgLy8gYWRkIHRvIHRyYWNrZXIgc28gaXQgY2FuIGJlIHJlc3RvcmVkLCBhbmQgdXBkYXRlIHdoZW4gY2hvaWNlcyBjaGFuZ2VcbiAgICAgICAgdm9pZCBsaWNlbnNlc1RyYWNrZXIuYWRkKGxpY2Vuc2VNYWluKTtcbiAgICAgICAgbGljZW5zZU1haW4uY29udGVudC5tb2RlbC50cmFja2VyRGF0YUNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgICAgdm9pZCBsaWNlbnNlc1RyYWNrZXIuc2F2ZShsaWNlbnNlTWFpbik7XG4gICAgICAgIH0pO1xuICAgICAgICByZXR1cm4gbGljZW5zZU1haW47XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmVmcmVzaExpY2Vuc2VzLCB7XG4gICAgICBsYWJlbDogYXJncyA9PiAoYXJncy5ub0xhYmVsID8gJycgOiByZWZyZXNoTGljZW5zZXMpLFxuICAgICAgY2FwdGlvbjogcmVmcmVzaExpY2Vuc2VzLFxuICAgICAgaWNvbjogcmVmcmVzaEljb24sXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIHJldHVybiBsaWNlbnNlc1RyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudC5tb2RlbC5pbml0TGljZW5zZXMoKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5saWNlbnNlUmVwb3J0LCB7XG4gICAgICBsYWJlbDogYXJncyA9PiB7XG4gICAgICAgIGlmIChhcmdzLm5vTGFiZWwpIHtcbiAgICAgICAgICByZXR1cm4gJyc7XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgZm9ybWF0ID0gZm9ybWF0T3JEZWZhdWx0KGAke2FyZ3MuZm9ybWF0fWApO1xuICAgICAgICByZXR1cm4gYCR7ZG93bmxvYWRBc1RleHR9ICR7Zm9ybWF0LnRpdGxlfWA7XG4gICAgICB9LFxuICAgICAgY2FwdGlvbjogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IGZvcm1hdCA9IGZvcm1hdE9yRGVmYXVsdChgJHthcmdzLmZvcm1hdH1gKTtcbiAgICAgICAgcmV0dXJuIGAke2Rvd25sb2FkQXNUZXh0fSAke2Zvcm1hdC50aXRsZX1gO1xuICAgICAgfSxcbiAgICAgIGljb246IGFyZ3MgPT4ge1xuICAgICAgICBjb25zdCBmb3JtYXQgPSBmb3JtYXRPckRlZmF1bHQoYCR7YXJncy5mb3JtYXR9YCk7XG4gICAgICAgIHJldHVybiBmb3JtYXQuaWNvbjtcbiAgICAgIH0sXG4gICAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgZm9ybWF0ID0gZm9ybWF0T3JEZWZhdWx0KGAke2FyZ3MuZm9ybWF0fWApO1xuICAgICAgICByZXR1cm4gYXdhaXQgbGljZW5zZXNUcmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQubW9kZWwuZG93bmxvYWQoe1xuICAgICAgICAgIGZvcm1hdDogZm9ybWF0LmlkXG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gaGFuZGxlIG9wdGlvbmFsIGludGVncmF0aW9uc1xuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oeyBjb21tYW5kOiBDb21tYW5kSURzLmxpY2Vuc2VzLCBjYXRlZ29yeSB9KTtcbiAgICB9XG5cbiAgICBpZiAobWVudSkge1xuICAgICAgY29uc3QgaGVscE1lbnUgPSBtZW51LmhlbHBNZW51O1xuICAgICAgaGVscE1lbnUuYWRkR3JvdXAoW3sgY29tbWFuZDogQ29tbWFuZElEcy5saWNlbnNlcyB9XSwgMCk7XG4gICAgfVxuXG4gICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUobGljZW5zZXNUcmFja2VyLCB7XG4gICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMubGljZW5zZXMsXG4gICAgICAgIG5hbWU6IHdpZGdldCA9PiAnbGljZW5zZXMnLFxuICAgICAgICBhcmdzOiB3aWRnZXQgPT4ge1xuICAgICAgICAgIGNvbnN0IHsgY3VycmVudEJ1bmRsZU5hbWUsIGN1cnJlbnRQYWNrYWdlSW5kZXgsIHBhY2thZ2VGaWx0ZXIgfSA9XG4gICAgICAgICAgICB3aWRnZXQuY29udGVudC5tb2RlbDtcblxuICAgICAgICAgIGNvbnN0IGFyZ3M6IExpY2Vuc2VzLklDcmVhdGVBcmdzID0ge1xuICAgICAgICAgICAgY3VycmVudEJ1bmRsZU5hbWUsXG4gICAgICAgICAgICBjdXJyZW50UGFja2FnZUluZGV4LFxuICAgICAgICAgICAgcGFja2FnZUZpbHRlclxuICAgICAgICAgIH07XG4gICAgICAgICAgcmV0dXJuIGFyZ3MgYXMgUmVhZG9ubHlKU09OT2JqZWN0O1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG4gIH1cbn07XG5cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIGFib3V0LFxuICBqdXB5dGVyRm9ydW0sXG4gIG9wZW4sXG4gIHJlc291cmNlcyxcbiAgbGljZW5zZXNcbl07XG5cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBUcmFuc2xhdGlvbkJ1bmRsZSB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7XG4gIGpzb25JY29uLFxuICBMYWJJY29uLFxuICBtYXJrZG93bkljb24sXG4gIHNwcmVhZHNoZWV0SWNvbixcbiAgVkRvbU1vZGVsLFxuICBWRG9tUmVuZGVyZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBQcm9taXNlRGVsZWdhdGUsIFJlYWRvbmx5SlNPTk9iamVjdCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IGgsIFZpcnR1YWxFbGVtZW50IH0gZnJvbSAnQGx1bWluby92aXJ0dWFsZG9tJztcbmltcG9ydCB7IFBhbmVsLCBTcGxpdFBhbmVsLCBUYWJCYXIsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbmNvbnN0IEZJTFRFUl9TRUNUSU9OX1RJVExFX0NMQVNTID0gJ2pwLUxpY2Vuc2VzLUZpbHRlcnMtdGl0bGUnO1xuXG4vKipcbiAqIEEgbGljZW5zZSB2aWV3ZXJcbiAqL1xuZXhwb3J0IGNsYXNzIExpY2Vuc2VzIGV4dGVuZHMgU3BsaXRQYW5lbCB7XG4gIHJlYWRvbmx5IG1vZGVsOiBMaWNlbnNlcy5Nb2RlbDtcblxuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBMaWNlbnNlcy5JT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtTGljZW5zZXMnKTtcbiAgICB0aGlzLm1vZGVsID0gb3B0aW9ucy5tb2RlbDtcbiAgICB0aGlzLmluaXRMZWZ0UGFuZWwoKTtcbiAgICB0aGlzLmluaXRGaWx0ZXJzKCk7XG4gICAgdGhpcy5pbml0QnVuZGxlcygpO1xuICAgIHRoaXMuaW5pdEdyaWQoKTtcbiAgICB0aGlzLmluaXRMaWNlbnNlVGV4dCgpO1xuICAgIHRoaXMuc2V0UmVsYXRpdmVTaXplcyhbMSwgMiwgM10pO1xuICAgIHZvaWQgdGhpcy5tb2RlbC5pbml0TGljZW5zZXMoKS50aGVuKCgpID0+IHRoaXMuX3VwZGF0ZUJ1bmRsZXMoKSk7XG4gICAgdGhpcy5tb2RlbC50cmFja2VyRGF0YUNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB0aGlzLnRpdGxlLmxhYmVsID0gdGhpcy5tb2RlbC50aXRsZTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgZGlzcG9zaW5nIG9mIHRoZSB3aWRnZXRcbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9idW5kbGVzLmN1cnJlbnRDaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5vbkJ1bmRsZVNlbGVjdGVkLCB0aGlzKTtcbiAgICB0aGlzLm1vZGVsLmRpc3Bvc2UoKTtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSW5pdGlhbGl6ZSB0aGUgbGVmdCBhcmVhIGZvciBmaWx0ZXJzIGFuZCBidW5kbGVzXG4gICAqL1xuICBwcm90ZWN0ZWQgaW5pdExlZnRQYW5lbCgpOiB2b2lkIHtcbiAgICB0aGlzLl9sZWZ0UGFuZWwgPSBuZXcgUGFuZWwoKTtcbiAgICB0aGlzLl9sZWZ0UGFuZWwuYWRkQ2xhc3MoJ2pwLUxpY2Vuc2VzLUZvcm1BcmVhJyk7XG4gICAgdGhpcy5hZGRXaWRnZXQodGhpcy5fbGVmdFBhbmVsKTtcbiAgICBTcGxpdFBhbmVsLnNldFN0cmV0Y2godGhpcy5fbGVmdFBhbmVsLCAxKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbml0aWFsaXplIHRoZSBmaWx0ZXJzXG4gICAqL1xuICBwcm90ZWN0ZWQgaW5pdEZpbHRlcnMoKTogdm9pZCB7XG4gICAgdGhpcy5fZmlsdGVycyA9IG5ldyBMaWNlbnNlcy5GaWx0ZXJzKHRoaXMubW9kZWwpO1xuICAgIFNwbGl0UGFuZWwuc2V0U3RyZXRjaCh0aGlzLl9maWx0ZXJzLCAxKTtcbiAgICB0aGlzLl9sZWZ0UGFuZWwuYWRkV2lkZ2V0KHRoaXMuX2ZpbHRlcnMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEluaXRpYWxpemUgdGhlIGxpc3Rpbmcgb2YgYXZhaWxhYmxlIGJ1bmRsZXNcbiAgICovXG4gIHByb3RlY3RlZCBpbml0QnVuZGxlcygpOiB2b2lkIHtcbiAgICB0aGlzLl9idW5kbGVzID0gbmV3IFRhYkJhcih7XG4gICAgICBvcmllbnRhdGlvbjogJ3ZlcnRpY2FsJyxcbiAgICAgIHJlbmRlcmVyOiBuZXcgTGljZW5zZXMuQnVuZGxlVGFiUmVuZGVyZXIodGhpcy5tb2RlbClcbiAgICB9KTtcbiAgICB0aGlzLl9idW5kbGVzLmFkZENsYXNzKCdqcC1MaWNlbnNlcy1CdW5kbGVzJyk7XG4gICAgU3BsaXRQYW5lbC5zZXRTdHJldGNoKHRoaXMuX2J1bmRsZXMsIDEpO1xuICAgIHRoaXMuX2xlZnRQYW5lbC5hZGRXaWRnZXQodGhpcy5fYnVuZGxlcyk7XG4gICAgdGhpcy5fYnVuZGxlcy5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMub25CdW5kbGVTZWxlY3RlZCwgdGhpcyk7XG4gICAgdGhpcy5tb2RlbC5zdGF0ZUNoYW5nZWQuY29ubmVjdCgoKSA9PiB0aGlzLl9idW5kbGVzLnVwZGF0ZSgpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbml0aWFsaXplIHRoZSBsaXN0aW5nIG9mIHBhY2thZ2VzIHdpdGhpbiB0aGUgY3VycmVudCBidW5kbGVcbiAgICovXG4gIHByb3RlY3RlZCBpbml0R3JpZCgpOiB2b2lkIHtcbiAgICB0aGlzLl9ncmlkID0gbmV3IExpY2Vuc2VzLkdyaWQodGhpcy5tb2RlbCk7XG4gICAgU3BsaXRQYW5lbC5zZXRTdHJldGNoKHRoaXMuX2dyaWQsIDEpO1xuICAgIHRoaXMuYWRkV2lkZ2V0KHRoaXMuX2dyaWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIEluaXRpYWxpemUgdGhlIGZ1bGwgdGV4dCBvZiB0aGUgY3VycmVudCBwYWNrYWdlXG4gICAqL1xuICBwcm90ZWN0ZWQgaW5pdExpY2Vuc2VUZXh0KCk6IHZvaWQge1xuICAgIHRoaXMuX2xpY2Vuc2VUZXh0ID0gbmV3IExpY2Vuc2VzLkZ1bGxUZXh0KHRoaXMubW9kZWwpO1xuICAgIFNwbGl0UGFuZWwuc2V0U3RyZXRjaCh0aGlzLl9ncmlkLCAxKTtcbiAgICB0aGlzLmFkZFdpZGdldCh0aGlzLl9saWNlbnNlVGV4dCk7XG4gIH1cblxuICAvKipcbiAgICogRXZlbnQgaGFuZGxlciBmb3IgdXBkYXRpbmcgdGhlIG1vZGVsIHdpdGggdGhlIGN1cnJlbnQgYnVuZGxlXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CdW5kbGVTZWxlY3RlZCgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fYnVuZGxlcy5jdXJyZW50VGl0bGU/LmxhYmVsKSB7XG4gICAgICB0aGlzLm1vZGVsLmN1cnJlbnRCdW5kbGVOYW1lID0gdGhpcy5fYnVuZGxlcy5jdXJyZW50VGl0bGUubGFiZWw7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgYnVuZGxlIHRhYnMuXG4gICAqL1xuICBwcm90ZWN0ZWQgX3VwZGF0ZUJ1bmRsZXMoKTogdm9pZCB7XG4gICAgdGhpcy5fYnVuZGxlcy5jbGVhclRhYnMoKTtcbiAgICBsZXQgaSA9IDA7XG4gICAgY29uc3QgeyBjdXJyZW50QnVuZGxlTmFtZSB9ID0gdGhpcy5tb2RlbDtcbiAgICBsZXQgY3VycmVudEluZGV4ID0gMDtcbiAgICBmb3IgKGNvbnN0IGJ1bmRsZSBvZiB0aGlzLm1vZGVsLmJ1bmRsZU5hbWVzKSB7XG4gICAgICBjb25zdCB0YWIgPSBuZXcgV2lkZ2V0KCk7XG4gICAgICB0YWIudGl0bGUubGFiZWwgPSBidW5kbGU7XG4gICAgICBpZiAoYnVuZGxlID09PSBjdXJyZW50QnVuZGxlTmFtZSkge1xuICAgICAgICBjdXJyZW50SW5kZXggPSBpO1xuICAgICAgfVxuICAgICAgdGhpcy5fYnVuZGxlcy5pbnNlcnRUYWIoKytpLCB0YWIudGl0bGUpO1xuICAgIH1cbiAgICB0aGlzLl9idW5kbGVzLmN1cnJlbnRJbmRleCA9IGN1cnJlbnRJbmRleDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiBhcmVhIGZvciBzZWxlY3RpbmcgbGljZW5zZXMgYnkgYnVuZGxlIGFuZCBmaWx0ZXJzXG4gICAqL1xuICBwcm90ZWN0ZWQgX2xlZnRQYW5lbDogUGFuZWw7XG5cbiAgLyoqXG4gICAqIEZpbHRlcnMgb24gdmlzaWJsZSBsaWNlbnNlc1xuICAgKi9cbiAgcHJvdGVjdGVkIF9maWx0ZXJzOiBMaWNlbnNlcy5GaWx0ZXJzO1xuXG4gIC8qKlxuICAgKiBUYWJzIHJlZmxlY3RpbmcgYXZhaWxhYmxlIGJ1bmRsZXNcbiAgICovXG4gIHByb3RlY3RlZCBfYnVuZGxlczogVGFiQmFyPFdpZGdldD47XG5cbiAgLyoqXG4gICAqIEEgZ3JpZCBvZiB0aGUgY3VycmVudCBidW5kbGUncyBwYWNrYWdlcycgbGljZW5zZSBtZXRhZGF0YVxuICAgKi9cbiAgcHJvdGVjdGVkIF9ncmlkOiBMaWNlbnNlcy5HcmlkO1xuXG4gIC8qKlxuICAgKiBUaGUgY3VycmVudGx5LXNlbGVjdGVkIHBhY2thZ2UncyBmdWxsIGxpY2Vuc2UgdGV4dFxuICAgKi9cbiAgcHJvdGVjdGVkIF9saWNlbnNlVGV4dDogTGljZW5zZXMuRnVsbFRleHQ7XG59XG5cbi8qKiBBIG5hbWVzcGFjZSBmb3IgbGljZW5zZSBjb21wb25lbnRzICovXG5leHBvcnQgbmFtZXNwYWNlIExpY2Vuc2VzIHtcbiAgLyoqIFRoZSBpbmZvcm1hdGlvbiBhYm91dCBhIGxpY2Vuc2UgcmVwb3J0IGZvcm1hdCAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUmVwb3J0Rm9ybWF0IHtcbiAgICB0aXRsZTogc3RyaW5nO1xuICAgIGljb246IExhYkljb247XG4gICAgaWQ6IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBMaWNlbnNlIHJlcG9ydCBmb3JtYXRzIHVuZGVyc3Rvb2QgYnkgdGhlIHNlcnZlciAob25jZSBsb3dlci1jYXNlZClcbiAgICovXG4gIGV4cG9ydCBjb25zdCBSRVBPUlRfRk9STUFUUzogUmVjb3JkPHN0cmluZywgSVJlcG9ydEZvcm1hdD4gPSB7XG4gICAgbWFya2Rvd246IHtcbiAgICAgIGlkOiAnbWFya2Rvd24nLFxuICAgICAgdGl0bGU6ICdNYXJrZG93bicsXG4gICAgICBpY29uOiBtYXJrZG93bkljb25cbiAgICB9LFxuICAgIGNzdjoge1xuICAgICAgaWQ6ICdjc3YnLFxuICAgICAgdGl0bGU6ICdDU1YnLFxuICAgICAgaWNvbjogc3ByZWFkc2hlZXRJY29uXG4gICAgfSxcbiAgICBqc29uOiB7XG4gICAgICBpZDogJ2NzdicsXG4gICAgICB0aXRsZTogJ0pTT04nLFxuICAgICAgaWNvbjoganNvbkljb25cbiAgICB9XG4gIH07XG5cbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGZvcm1hdCAobW9zdCBodW1hbi1yZWFkYWJsZSlcbiAgICovXG4gIGV4cG9ydCBjb25zdCBERUZBVUxUX0ZPUk1BVCA9ICdtYXJrZG93bic7XG5cbiAgLyoqXG4gICAqIE9wdGlvbnMgZm9yIGluc3RhbnRpYXRpbmcgYSBsaWNlbnNlIHZpZXdlclxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgbW9kZWw6IE1vZGVsO1xuICB9XG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBpbnN0YW50aWF0aW5nIGEgbGljZW5zZSBtb2RlbFxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTW9kZWxPcHRpb25zIGV4dGVuZHMgSUNyZWF0ZUFyZ3Mge1xuICAgIGxpY2Vuc2VzVXJsOiBzdHJpbmc7XG4gICAgc2VydmVyU2V0dGluZ3M/OiBTZXJ2ZXJDb25uZWN0aW9uLklTZXR0aW5ncztcbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIEpTT04gcmVzcG9uc2UgZnJvbSB0aGUgQVBJXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElMaWNlbnNlUmVzcG9uc2Uge1xuICAgIGJ1bmRsZXM6IHtcbiAgICAgIFtrZXk6IHN0cmluZ106IElMaWNlbnNlQnVuZGxlO1xuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogQSB0b3AtbGV2ZWwgcmVwb3J0IG9mIHRoZSBsaWNlbnNlcyBmb3IgYWxsIGNvZGUgaW5jbHVkZWQgaW4gYSBidW5kbGVcbiAgICpcbiAgICogIyMjIE5vdGVcbiAgICpcbiAgICogVGhpcyBpcyByb3VnaGx5IGluZm9ybWVkIGJ5IHRoZSB0ZXJtcyBkZWZpbmVkIGluIHRoZSBTUERYIHNwZWMsIHRob3VnaCBpcyBub3RcbiAgICogYW4gU1BEWCBEb2N1bWVudCwgc2luY2UgdGhlcmUgc2VlbSB0byBiZSBzZXZlcmFsIChpbmNvbXBhdGlibGUpIHNwZWNzXG4gICAqIGluIHRoYXQgcmVwby5cbiAgICpcbiAgICogQHNlZSBodHRwczovL2dpdGh1Yi5jb20vc3BkeC9zcGR4LXNwZWMvYmxvYi9kZXZlbG9wbWVudC92Mi4yLjEvc2NoZW1hcy9zcGR4LXNjaGVtYS5qc29uXG4gICAqKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTGljZW5zZUJ1bmRsZSBleHRlbmRzIFJlYWRvbmx5SlNPTk9iamVjdCB7XG4gICAgcGFja2FnZXM6IElQYWNrYWdlTGljZW5zZUluZm9bXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIGJlc3QtZWZmb3J0IHNpbmdsZSBidW5kbGVkIHBhY2thZ2UncyBpbmZvcm1hdGlvbi5cbiAgICpcbiAgICogIyMjIE5vdGVcbiAgICpcbiAgICogVGhpcyBpcyByb3VnaGx5IGluZm9ybWVkIGJ5IFNQRFggYHBhY2thZ2VzYCBhbmQgYGhhc0V4dHJhY3RlZExpY2Vuc2VJbmZvc2AsXG4gICAqIGFzIG1ha2luZyBpdCBjb25mb3JtYW50IHdvdWxkIHZhc3RseSBjb21wbGljYXRlIHRoZSBzdHJ1Y3R1cmUuXG4gICAqXG4gICAqIEBzZWUgaHR0cHM6Ly9naXRodWIuY29tL3NwZHgvc3BkeC1zcGVjL2Jsb2IvZGV2ZWxvcG1lbnQvdjIuMi4xL3NjaGVtYXMvc3BkeC1zY2hlbWEuanNvblxuICAgKiovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVBhY2thZ2VMaWNlbnNlSW5mbyBleHRlbmRzIFJlYWRvbmx5SlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogdGhlIG5hbWUgb2YgdGhlIHBhY2thZ2UgYXMgaXQgYXBwZWFycyBpbiBwYWNrYWdlLmpzb25cbiAgICAgKi9cbiAgICBuYW1lOiBzdHJpbmc7XG4gICAgLyoqXG4gICAgICogdGhlIHZlcnNpb24gb2YgdGhlIHBhY2thZ2UsIG9yIGFuIGVtcHR5IHN0cmluZyBpZiB1bmtub3duXG4gICAgICovXG4gICAgdmVyc2lvbkluZm86IHN0cmluZztcbiAgICAvKipcbiAgICAgKiBhbiBTUERYIGxpY2Vuc2UgaWRlbnRpZmllciBvciBMaWNlbnNlUmVmLCBvciBhbiBlbXB0eSBzdHJpbmcgaWYgdW5rbm93blxuICAgICAqL1xuICAgIGxpY2Vuc2VJZDogc3RyaW5nO1xuICAgIC8qKlxuICAgICAqIHRoZSB2ZXJiYXRpbSBleHRyYWN0ZWQgdGV4dCBvZiB0aGUgbGljZW5zZSwgb3IgYW4gZW1wdHkgc3RyaW5nIGlmIHVua25vd25cbiAgICAgKi9cbiAgICBleHRyYWN0ZWRUZXh0OiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGZvcm1hdCBpbmZvcm1hdGlvbiBmb3IgYSBkb3dubG9hZFxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJRG93bmxvYWRPcHRpb25zIHtcbiAgICBmb3JtYXQ6IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZmllbGRzIHdoaWNoIGNhbiBiZSBmaWx0ZXJlZFxuICAgKi9cbiAgZXhwb3J0IHR5cGUgVEZpbHRlcktleSA9ICduYW1lJyB8ICd2ZXJzaW9uSW5mbycgfCAnbGljZW5zZUlkJztcblxuICBleHBvcnQgaW50ZXJmYWNlIElDcmVhdGVBcmdzIHtcbiAgICBjdXJyZW50QnVuZGxlTmFtZT86IHN0cmluZyB8IG51bGw7XG4gICAgcGFja2FnZUZpbHRlcj86IFBhcnRpYWw8SVBhY2thZ2VMaWNlbnNlSW5mbz4gfCBudWxsO1xuICAgIGN1cnJlbnRQYWNrYWdlSW5kZXg/OiBudW1iZXIgfCBudWxsO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgbW9kZWwgZm9yIGxpY2Vuc2UgZGF0YVxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIGltcGxlbWVudHMgSUNyZWF0ZUFyZ3Mge1xuICAgIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElNb2RlbE9wdGlvbnMpIHtcbiAgICAgIHN1cGVyKCk7XG4gICAgICB0aGlzLl90cmFucyA9IG9wdGlvbnMudHJhbnM7XG4gICAgICB0aGlzLl9saWNlbnNlc1VybCA9IG9wdGlvbnMubGljZW5zZXNVcmw7XG4gICAgICB0aGlzLl9zZXJ2ZXJTZXR0aW5ncyA9XG4gICAgICAgIG9wdGlvbnMuc2VydmVyU2V0dGluZ3MgfHwgU2VydmVyQ29ubmVjdGlvbi5tYWtlU2V0dGluZ3MoKTtcbiAgICAgIGlmIChvcHRpb25zLmN1cnJlbnRCdW5kbGVOYW1lKSB7XG4gICAgICAgIHRoaXMuX2N1cnJlbnRCdW5kbGVOYW1lID0gb3B0aW9ucy5jdXJyZW50QnVuZGxlTmFtZTtcbiAgICAgIH1cbiAgICAgIGlmIChvcHRpb25zLnBhY2thZ2VGaWx0ZXIpIHtcbiAgICAgICAgdGhpcy5fcGFja2FnZUZpbHRlciA9IG9wdGlvbnMucGFja2FnZUZpbHRlcjtcbiAgICAgIH1cbiAgICAgIGlmIChvcHRpb25zLmN1cnJlbnRQYWNrYWdlSW5kZXgpIHtcbiAgICAgICAgdGhpcy5fY3VycmVudFBhY2thZ2VJbmRleCA9IG9wdGlvbnMuY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBIYW5kbGUgdGhlIGluaXRpYWwgcmVxdWVzdCBmb3IgdGhlIGxpY2Vuc2VzIGZyb20gdGhlIHNlcnZlci5cbiAgICAgKi9cbiAgICBhc3luYyBpbml0TGljZW5zZXMoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICB0cnkge1xuICAgICAgICBjb25zdCByZXNwb25zZSA9IGF3YWl0IFNlcnZlckNvbm5lY3Rpb24ubWFrZVJlcXVlc3QoXG4gICAgICAgICAgdGhpcy5fbGljZW5zZXNVcmwsXG4gICAgICAgICAge30sXG4gICAgICAgICAgdGhpcy5fc2VydmVyU2V0dGluZ3NcbiAgICAgICAgKTtcbiAgICAgICAgdGhpcy5fc2VydmVyUmVzcG9uc2UgPSBhd2FpdCByZXNwb25zZS5qc29uKCk7XG4gICAgICAgIHRoaXMuX2xpY2Vuc2VzUmVhZHkucmVzb2x2ZSgpO1xuICAgICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgICB9IGNhdGNoIChlcnIpIHtcbiAgICAgICAgdGhpcy5fbGljZW5zZXNSZWFkeS5yZWplY3QoZXJyKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSB0ZW1wb3JhcnkgZG93bmxvYWQgbGluaywgYW5kIGVtdWxhdGUgY2xpY2tpbmcgaXQgdG8gdHJpZ2dlciBhIG5hbWVkXG4gICAgICogZmlsZSBkb3dubG9hZC5cbiAgICAgKi9cbiAgICBhc3luYyBkb3dubG9hZChvcHRpb25zOiBJRG93bmxvYWRPcHRpb25zKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICBjb25zdCB1cmwgPSBgJHt0aGlzLl9saWNlbnNlc1VybH0/Zm9ybWF0PSR7b3B0aW9ucy5mb3JtYXR9JmRvd25sb2FkPTFgO1xuICAgICAgY29uc3QgZWxlbWVudCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2EnKTtcbiAgICAgIGVsZW1lbnQuaHJlZiA9IHVybDtcbiAgICAgIGVsZW1lbnQuZG93bmxvYWQgPSAnJztcbiAgICAgIGRvY3VtZW50LmJvZHkuYXBwZW5kQ2hpbGQoZWxlbWVudCk7XG4gICAgICBlbGVtZW50LmNsaWNrKCk7XG4gICAgICBkb2N1bWVudC5ib2R5LnJlbW92ZUNoaWxkKGVsZW1lbnQpO1xuICAgICAgcmV0dXJuIHZvaWQgMDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBsaWNlbnNlcyBmcm9tIHRoZSBzZXJ2ZXIgY2hhbmdlXG4gICAgICovXG4gICAgZ2V0IHNlbGVjdGVkUGFja2FnZUNoYW5nZWQoKTogSVNpZ25hbDxNb2RlbCwgdm9pZD4ge1xuICAgICAgcmV0dXJuIHRoaXMuX3NlbGVjdGVkUGFja2FnZUNoYW5nZWQ7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgdHJhY2thYmxlIGRhdGEgY2hhbmdlc1xuICAgICAqL1xuICAgIGdldCB0cmFja2VyRGF0YUNoYW5nZWQoKTogSVNpZ25hbDxNb2RlbCwgdm9pZD4ge1xuICAgICAgcmV0dXJuIHRoaXMuX3RyYWNrZXJEYXRhQ2hhbmdlZDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZXMgb2YgdGhlIGxpY2Vuc2UgYnVuZGxlcyBhdmFpbGFibGVcbiAgICAgKi9cbiAgICBnZXQgYnVuZGxlTmFtZXMoKTogc3RyaW5nW10ge1xuICAgICAgcmV0dXJuIE9iamVjdC5rZXlzKHRoaXMuX3NlcnZlclJlc3BvbnNlPy5idW5kbGVzIHx8IHt9KTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBsaWNlbnNlIGJ1bmRsZVxuICAgICAqL1xuICAgIGdldCBjdXJyZW50QnVuZGxlTmFtZSgpOiBzdHJpbmcgfCBudWxsIHtcbiAgICAgIGlmICh0aGlzLl9jdXJyZW50QnVuZGxlTmFtZSkge1xuICAgICAgICByZXR1cm4gdGhpcy5fY3VycmVudEJ1bmRsZU5hbWU7XG4gICAgICB9XG4gICAgICBpZiAodGhpcy5idW5kbGVOYW1lcy5sZW5ndGgpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuYnVuZGxlTmFtZXNbMF07XG4gICAgICB9XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBTZXQgdGhlIGN1cnJlbnQgbGljZW5zZSBidW5kbGUsIGFuZCByZXNldCB0aGUgc2VsZWN0ZWQgaW5kZXhcbiAgICAgKi9cbiAgICBzZXQgY3VycmVudEJ1bmRsZU5hbWUoY3VycmVudEJ1bmRsZU5hbWU6IHN0cmluZyB8IG51bGwpIHtcbiAgICAgIGlmICh0aGlzLl9jdXJyZW50QnVuZGxlTmFtZSAhPT0gY3VycmVudEJ1bmRsZU5hbWUpIHtcbiAgICAgICAgdGhpcy5fY3VycmVudEJ1bmRsZU5hbWUgPSBjdXJyZW50QnVuZGxlTmFtZTtcbiAgICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgICB0aGlzLl90cmFja2VyRGF0YUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgfVxuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIGxpY2Vuc2VzIGFyZSBhdmFpbGFibGUgZnJvbSB0aGUgc2VydmVyXG4gICAgICovXG4gICAgZ2V0IGxpY2Vuc2VzUmVhZHkoKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICByZXR1cm4gdGhpcy5fbGljZW5zZXNSZWFkeS5wcm9taXNlO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEFsbCB0aGUgbGljZW5zZSBidW5kbGVzLCBrZXllZCBieSB0aGUgZGlzdHJpYnV0aW5nIHBhY2thZ2VzXG4gICAgICovXG4gICAgZ2V0IGJ1bmRsZXMoKTogbnVsbCB8IHsgW2tleTogc3RyaW5nXTogSUxpY2Vuc2VCdW5kbGUgfSB7XG4gICAgICByZXR1cm4gdGhpcy5fc2VydmVyUmVzcG9uc2U/LmJ1bmRsZXMgfHwge307XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGluZGV4IG9mIHRoZSBjdXJyZW50bHktc2VsZWN0ZWQgcGFja2FnZSB3aXRoaW4gaXRzIGxpY2Vuc2UgYnVuZGxlXG4gICAgICovXG4gICAgZ2V0IGN1cnJlbnRQYWNrYWdlSW5kZXgoKTogbnVtYmVyIHwgbnVsbCB7XG4gICAgICByZXR1cm4gdGhpcy5fY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBVcGRhdGUgdGhlIGN1cnJlbnRseS1zZWxlY3RlZCBwYWNrYWdlIHdpdGhpbiBpdHMgbGljZW5zZSBidW5kbGVcbiAgICAgKi9cbiAgICBzZXQgY3VycmVudFBhY2thZ2VJbmRleChjdXJyZW50UGFja2FnZUluZGV4OiBudW1iZXIgfCBudWxsKSB7XG4gICAgICBpZiAodGhpcy5fY3VycmVudFBhY2thZ2VJbmRleCA9PT0gY3VycmVudFBhY2thZ2VJbmRleCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLl9jdXJyZW50UGFja2FnZUluZGV4ID0gY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICAgIHRoaXMuX3NlbGVjdGVkUGFja2FnZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCh2b2lkIDApO1xuICAgICAgdGhpcy5fdHJhY2tlckRhdGFDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbGljZW5zZSBkYXRhIGZvciB0aGUgY3VycmVudGx5LXNlbGVjdGVkIHBhY2thZ2VcbiAgICAgKi9cbiAgICBnZXQgY3VycmVudFBhY2thZ2UoKTogSVBhY2thZ2VMaWNlbnNlSW5mbyB8IG51bGwge1xuICAgICAgaWYgKFxuICAgICAgICB0aGlzLmN1cnJlbnRCdW5kbGVOYW1lICYmXG4gICAgICAgIHRoaXMuYnVuZGxlcyAmJlxuICAgICAgICB0aGlzLl9jdXJyZW50UGFja2FnZUluZGV4ICE9IG51bGxcbiAgICAgICkge1xuICAgICAgICByZXR1cm4gdGhpcy5nZXRGaWx0ZXJlZFBhY2thZ2VzKFxuICAgICAgICAgIHRoaXMuYnVuZGxlc1t0aGlzLmN1cnJlbnRCdW5kbGVOYW1lXT8ucGFja2FnZXMgfHwgW11cbiAgICAgICAgKVt0aGlzLl9jdXJyZW50UGFja2FnZUluZGV4XTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIG51bGw7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogQSB0cmFuc2xhdGlvbiBidW5kbGVcbiAgICAgKi9cbiAgICBnZXQgdHJhbnMoKTogVHJhbnNsYXRpb25CdW5kbGUge1xuICAgICAgcmV0dXJuIHRoaXMuX3RyYW5zO1xuICAgIH1cblxuICAgIGdldCB0aXRsZSgpOiBzdHJpbmcge1xuICAgICAgcmV0dXJuIGAke3RoaXMuX2N1cnJlbnRCdW5kbGVOYW1lIHx8ICcnfSAke3RoaXMuX3RyYW5zLl9fKFxuICAgICAgICAnTGljZW5zZXMnXG4gICAgICApfWAudHJpbSgpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IHBhY2thZ2UgZmlsdGVyXG4gICAgICovXG4gICAgZ2V0IHBhY2thZ2VGaWx0ZXIoKTogUGFydGlhbDxJUGFja2FnZUxpY2Vuc2VJbmZvPiB7XG4gICAgICByZXR1cm4gdGhpcy5fcGFja2FnZUZpbHRlcjtcbiAgICB9XG5cbiAgICBzZXQgcGFja2FnZUZpbHRlcihwYWNrYWdlRmlsdGVyOiBQYXJ0aWFsPElQYWNrYWdlTGljZW5zZUluZm8+KSB7XG4gICAgICB0aGlzLl9wYWNrYWdlRmlsdGVyID0gcGFja2FnZUZpbHRlcjtcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICAgIHRoaXMuX3RyYWNrZXJEYXRhQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogR2V0IGZpbHRlcmVkIHBhY2thZ2VzIGZyb20gY3VycmVudCBidW5kbGUgd2hlcmUgYXQgbGVhc3Qgb25lIHRva2VuIG9mIGVhY2hcbiAgICAgKiBrZXkgaXMgcHJlc2VudC5cbiAgICAgKi9cbiAgICBnZXRGaWx0ZXJlZFBhY2thZ2VzKGFsbFJvd3M6IElQYWNrYWdlTGljZW5zZUluZm9bXSk6IElQYWNrYWdlTGljZW5zZUluZm9bXSB7XG4gICAgICBsZXQgcm93czogSVBhY2thZ2VMaWNlbnNlSW5mb1tdID0gW107XG4gICAgICBsZXQgZmlsdGVyczogW3N0cmluZywgc3RyaW5nW11dW10gPSBPYmplY3QuZW50cmllcyh0aGlzLl9wYWNrYWdlRmlsdGVyKVxuICAgICAgICAuZmlsdGVyKChbaywgdl0pID0+IHYgJiYgYCR7dn1gLnRyaW0oKS5sZW5ndGgpXG4gICAgICAgIC5tYXAoKFtrLCB2XSkgPT4gW2ssIGAke3Z9YC50b0xvd2VyQ2FzZSgpLnRyaW0oKS5zcGxpdCgnICcpXSk7XG4gICAgICBmb3IgKGNvbnN0IHJvdyBvZiBhbGxSb3dzKSB7XG4gICAgICAgIGxldCBrZXlIaXRzID0gMDtcbiAgICAgICAgZm9yIChjb25zdCBba2V5LCBiaXRzXSBvZiBmaWx0ZXJzKSB7XG4gICAgICAgICAgbGV0IGJpdEhpdHMgPSAwO1xuICAgICAgICAgIGxldCByb3dLZXlWYWx1ZSA9IGAke3Jvd1trZXldfWAudG9Mb3dlckNhc2UoKTtcbiAgICAgICAgICBmb3IgKGNvbnN0IGJpdCBvZiBiaXRzKSB7XG4gICAgICAgICAgICBpZiAocm93S2V5VmFsdWUuaW5jbHVkZXMoYml0KSkge1xuICAgICAgICAgICAgICBiaXRIaXRzICs9IDE7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuICAgICAgICAgIGlmIChiaXRIaXRzKSB7XG4gICAgICAgICAgICBrZXlIaXRzICs9IDE7XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGlmIChrZXlIaXRzID09PSBmaWx0ZXJzLmxlbmd0aCkge1xuICAgICAgICAgIHJvd3MucHVzaChyb3cpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gT2JqZWN0LnZhbHVlcyhyb3dzKTtcbiAgICB9XG5cbiAgICBwcml2YXRlIF9zZWxlY3RlZFBhY2thZ2VDaGFuZ2VkOiBTaWduYWw8TW9kZWwsIHZvaWQ+ID0gbmV3IFNpZ25hbCh0aGlzKTtcbiAgICBwcml2YXRlIF90cmFja2VyRGF0YUNoYW5nZWQ6IFNpZ25hbDxNb2RlbCwgdm9pZD4gPSBuZXcgU2lnbmFsKHRoaXMpO1xuICAgIHByaXZhdGUgX3NlcnZlclJlc3BvbnNlOiBJTGljZW5zZVJlc3BvbnNlIHwgbnVsbDtcbiAgICBwcml2YXRlIF9saWNlbnNlc1VybDogc3RyaW5nO1xuICAgIHByaXZhdGUgX3NlcnZlclNldHRpbmdzOiBTZXJ2ZXJDb25uZWN0aW9uLklTZXR0aW5ncztcbiAgICBwcml2YXRlIF9jdXJyZW50QnVuZGxlTmFtZTogc3RyaW5nIHwgbnVsbDtcbiAgICBwcml2YXRlIF90cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gICAgcHJpdmF0ZSBfY3VycmVudFBhY2thZ2VJbmRleDogbnVtYmVyIHwgbnVsbCA9IDA7XG4gICAgcHJpdmF0ZSBfbGljZW5zZXNSZWFkeSA9IG5ldyBQcm9taXNlRGVsZWdhdGU8dm9pZD4oKTtcbiAgICBwcml2YXRlIF9wYWNrYWdlRmlsdGVyOiBQYXJ0aWFsPElQYWNrYWdlTGljZW5zZUluZm8+ID0ge307XG4gIH1cblxuICAvKipcbiAgICogQSBmaWx0ZXIgZm9ybSBmb3IgbGltaXRpbmcgdGhlIHBhY2thZ2VzIGRpc3BsYXllZFxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIEZpbHRlcnMgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8TW9kZWw+IHtcbiAgICBjb25zdHJ1Y3Rvcihtb2RlbDogTW9kZWwpIHtcbiAgICAgIHN1cGVyKG1vZGVsKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLUxpY2Vuc2VzLUZpbHRlcnMnKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVJlbmRlcmVkSFRNTENvbW1vbicpO1xuICAgIH1cblxuICAgIHByb3RlY3RlZCByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgICAgY29uc3QgeyB0cmFucyB9ID0gdGhpcy5tb2RlbDtcbiAgICAgIHJldHVybiAoXG4gICAgICAgIDxkaXY+XG4gICAgICAgICAgPGxhYmVsPlxuICAgICAgICAgICAgPHN0cm9uZyBjbGFzc05hbWU9e0ZJTFRFUl9TRUNUSU9OX1RJVExFX0NMQVNTfT5cbiAgICAgICAgICAgICAge3RyYW5zLl9fKCdGaWx0ZXIgTGljZW5zZXMgQnknKX1cbiAgICAgICAgICAgIDwvc3Ryb25nPlxuICAgICAgICAgIDwvbGFiZWw+XG4gICAgICAgICAgPHVsPlxuICAgICAgICAgICAgPGxpPlxuICAgICAgICAgICAgICA8bGFiZWw+e3RyYW5zLl9fKCdQYWNrYWdlJyl9PC9sYWJlbD5cbiAgICAgICAgICAgICAge3RoaXMucmVuZGVyRmlsdGVyKCduYW1lJyl9XG4gICAgICAgICAgICA8L2xpPlxuICAgICAgICAgICAgPGxpPlxuICAgICAgICAgICAgICA8bGFiZWw+e3RyYW5zLl9fKCdWZXJzaW9uJyl9PC9sYWJlbD5cbiAgICAgICAgICAgICAge3RoaXMucmVuZGVyRmlsdGVyKCd2ZXJzaW9uSW5mbycpfVxuICAgICAgICAgICAgPC9saT5cbiAgICAgICAgICAgIDxsaT5cbiAgICAgICAgICAgICAgPGxhYmVsPnt0cmFucy5fXygnTGljZW5zZScpfTwvbGFiZWw+XG4gICAgICAgICAgICAgIHt0aGlzLnJlbmRlckZpbHRlcignbGljZW5zZUlkJyl9XG4gICAgICAgICAgICA8L2xpPlxuICAgICAgICAgIDwvdWw+XG4gICAgICAgICAgPGxhYmVsPlxuICAgICAgICAgICAgPHN0cm9uZyBjbGFzc05hbWU9e0ZJTFRFUl9TRUNUSU9OX1RJVExFX0NMQVNTfT5cbiAgICAgICAgICAgICAge3RyYW5zLl9fKCdEaXN0cmlidXRpb25zJyl9XG4gICAgICAgICAgICA8L3N0cm9uZz5cbiAgICAgICAgICA8L2xhYmVsPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVuZGVyIGEgZmlsdGVyIGlucHV0XG4gICAgICovXG4gICAgcHJvdGVjdGVkIHJlbmRlckZpbHRlciA9IChrZXk6IFRGaWx0ZXJLZXkpOiBKU1guRWxlbWVudCA9PiB7XG4gICAgICBjb25zdCB2YWx1ZSA9IHRoaXMubW9kZWwucGFja2FnZUZpbHRlcltrZXldIHx8ICcnO1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPGlucHV0XG4gICAgICAgICAgdHlwZT1cInRleHRcIlxuICAgICAgICAgIG5hbWU9e2tleX1cbiAgICAgICAgICBkZWZhdWx0VmFsdWU9e3ZhbHVlfVxuICAgICAgICAgIGNsYXNzTmFtZT1cImpwLW1vZC1zdHlsZWRcIlxuICAgICAgICAgIG9uSW5wdXQ9e3RoaXMub25GaWx0ZXJJbnB1dH1cbiAgICAgICAgLz5cbiAgICAgICk7XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIEhhbmRsZSBhIGZpbHRlciBpbnB1dCBjaGFuZ2luZ1xuICAgICAqL1xuICAgIHByb3RlY3RlZCBvbkZpbHRlcklucHV0ID0gKFxuICAgICAgZXZ0OiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MSW5wdXRFbGVtZW50PlxuICAgICk6IHZvaWQgPT4ge1xuICAgICAgY29uc3QgaW5wdXQgPSBldnQuY3VycmVudFRhcmdldDtcbiAgICAgIGNvbnN0IHsgbmFtZSwgdmFsdWUgfSA9IGlucHV0O1xuICAgICAgdGhpcy5tb2RlbC5wYWNrYWdlRmlsdGVyID0geyAuLi50aGlzLm1vZGVsLnBhY2thZ2VGaWx0ZXIsIFtuYW1lXTogdmFsdWUgfTtcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgZmFuY3kgYnVuZGxlIHJlbmRlcmVyIHdpdGggdGhlIHBhY2thZ2UgY291bnRcbiAgICovXG4gIGV4cG9ydCBjbGFzcyBCdW5kbGVUYWJSZW5kZXJlciBleHRlbmRzIFRhYkJhci5SZW5kZXJlciB7XG4gICAgLyoqXG4gICAgICogQSBtb2RlbCBvZiB0aGUgc3RhdGUgb2YgbGljZW5zZSB2aWV3aW5nIGFzIHdlbGwgYXMgdGhlIHVuZGVybHlpbmcgZGF0YVxuICAgICAqL1xuICAgIG1vZGVsOiBNb2RlbDtcblxuICAgIHJlYWRvbmx5IGNsb3NlSWNvblNlbGVjdG9yID0gJy5sbS1UYWJCYXItdGFiQ2xvc2VJY29uJztcblxuICAgIGNvbnN0cnVjdG9yKG1vZGVsOiBNb2RlbCkge1xuICAgICAgc3VwZXIoKTtcbiAgICAgIHRoaXMubW9kZWwgPSBtb2RlbDtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgYSBmdWxsIGJ1bmRsZVxuICAgICAqL1xuICAgIHJlbmRlclRhYihkYXRhOiBUYWJCYXIuSVJlbmRlckRhdGE8V2lkZ2V0Pik6IFZpcnR1YWxFbGVtZW50IHtcbiAgICAgIGxldCB0aXRsZSA9IGRhdGEudGl0bGUuY2FwdGlvbjtcbiAgICAgIGxldCBrZXkgPSB0aGlzLmNyZWF0ZVRhYktleShkYXRhKTtcbiAgICAgIGxldCBzdHlsZSA9IHRoaXMuY3JlYXRlVGFiU3R5bGUoZGF0YSk7XG4gICAgICBsZXQgY2xhc3NOYW1lID0gdGhpcy5jcmVhdGVUYWJDbGFzcyhkYXRhKTtcbiAgICAgIGxldCBkYXRhc2V0ID0gdGhpcy5jcmVhdGVUYWJEYXRhc2V0KGRhdGEpO1xuICAgICAgcmV0dXJuIGgubGkoXG4gICAgICAgIHsga2V5LCBjbGFzc05hbWUsIHRpdGxlLCBzdHlsZSwgZGF0YXNldCB9LFxuICAgICAgICB0aGlzLnJlbmRlckljb24oZGF0YSksXG4gICAgICAgIHRoaXMucmVuZGVyTGFiZWwoZGF0YSksXG4gICAgICAgIHRoaXMucmVuZGVyQ291bnRCYWRnZShkYXRhKVxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgdGhlIHBhY2thZ2UgY291bnRcbiAgICAgKi9cbiAgICByZW5kZXJDb3VudEJhZGdlKGRhdGE6IFRhYkJhci5JUmVuZGVyRGF0YTxXaWRnZXQ+KTogVmlydHVhbEVsZW1lbnQge1xuICAgICAgY29uc3QgYnVuZGxlID0gZGF0YS50aXRsZS5sYWJlbDtcbiAgICAgIGNvbnN0IHsgYnVuZGxlcyB9ID0gdGhpcy5tb2RlbDtcbiAgICAgIGNvbnN0IHBhY2thZ2VzID0gdGhpcy5tb2RlbC5nZXRGaWx0ZXJlZFBhY2thZ2VzKFxuICAgICAgICAoYnVuZGxlcyAmJiBidW5kbGUgPyBidW5kbGVzW2J1bmRsZV0ucGFja2FnZXMgOiBbXSkgfHwgW11cbiAgICAgICk7XG4gICAgICByZXR1cm4gaC5sYWJlbCh7fSwgYCR7cGFja2FnZXMubGVuZ3RofWApO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBIGdyaWQgb2YgbGljZW5zZXNcbiAgICovXG4gIGV4cG9ydCBjbGFzcyBHcmlkIGV4dGVuZHMgVkRvbVJlbmRlcmVyPExpY2Vuc2VzLk1vZGVsPiB7XG4gICAgY29uc3RydWN0b3IobW9kZWw6IExpY2Vuc2VzLk1vZGVsKSB7XG4gICAgICBzdXBlcihtb2RlbCk7XG4gICAgICB0aGlzLmFkZENsYXNzKCdqcC1MaWNlbnNlcy1HcmlkJyk7XG4gICAgICB0aGlzLmFkZENsYXNzKCdqcC1SZW5kZXJlZEhUTUxDb21tb24nKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgYSBncmlkIG9mIHBhY2thZ2UgbGljZW5zZSBpbmZvcm1hdGlvblxuICAgICAqL1xuICAgIHByb3RlY3RlZCByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgICAgY29uc3QgeyBidW5kbGVzLCBjdXJyZW50QnVuZGxlTmFtZSwgdHJhbnMgfSA9IHRoaXMubW9kZWw7XG4gICAgICBjb25zdCBmaWx0ZXJlZFBhY2thZ2VzID0gdGhpcy5tb2RlbC5nZXRGaWx0ZXJlZFBhY2thZ2VzKFxuICAgICAgICBidW5kbGVzICYmIGN1cnJlbnRCdW5kbGVOYW1lXG4gICAgICAgICAgPyBidW5kbGVzW2N1cnJlbnRCdW5kbGVOYW1lXT8ucGFja2FnZXMgfHwgW11cbiAgICAgICAgICA6IFtdXG4gICAgICApO1xuICAgICAgaWYgKCFmaWx0ZXJlZFBhY2thZ2VzLmxlbmd0aCkge1xuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgIDxibG9ja3F1b3RlPlxuICAgICAgICAgICAgPGVtPnt0cmFucy5fXygnTm8gUGFja2FnZXMgZm91bmQnKX08L2VtPlxuICAgICAgICAgIDwvYmxvY2txdW90ZT5cbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICAgIHJldHVybiAoXG4gICAgICAgIDxmb3JtPlxuICAgICAgICAgIDx0YWJsZT5cbiAgICAgICAgICAgIDx0aGVhZD5cbiAgICAgICAgICAgICAgPHRyPlxuICAgICAgICAgICAgICAgIDx0ZD48L3RkPlxuICAgICAgICAgICAgICAgIDx0aD57dHJhbnMuX18oJ1BhY2thZ2UnKX08L3RoPlxuICAgICAgICAgICAgICAgIDx0aD57dHJhbnMuX18oJ1ZlcnNpb24nKX08L3RoPlxuICAgICAgICAgICAgICAgIDx0aD57dHJhbnMuX18oJ0xpY2Vuc2UnKX08L3RoPlxuICAgICAgICAgICAgICA8L3RyPlxuICAgICAgICAgICAgPC90aGVhZD5cbiAgICAgICAgICAgIDx0Ym9keT57ZmlsdGVyZWRQYWNrYWdlcy5tYXAodGhpcy5yZW5kZXJSb3cpfTwvdGJvZHk+XG4gICAgICAgICAgPC90YWJsZT5cbiAgICAgICAgPC9mb3JtPlxuICAgICAgKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBSZW5kZXIgYSBzaW5nbGUgcGFja2FnZSdzIGxpY2Vuc2UgaW5mb3JtYXRpb25cbiAgICAgKi9cbiAgICBwcm90ZWN0ZWQgcmVuZGVyUm93ID0gKFxuICAgICAgcm93OiBMaWNlbnNlcy5JUGFja2FnZUxpY2Vuc2VJbmZvLFxuICAgICAgaW5kZXg6IG51bWJlclxuICAgICk6IEpTWC5FbGVtZW50ID0+IHtcbiAgICAgIGNvbnN0IHNlbGVjdGVkID0gaW5kZXggPT09IHRoaXMubW9kZWwuY3VycmVudFBhY2thZ2VJbmRleDtcbiAgICAgIGNvbnN0IG9uQ2hlY2sgPSAoKSA9PiAodGhpcy5tb2RlbC5jdXJyZW50UGFja2FnZUluZGV4ID0gaW5kZXgpO1xuICAgICAgcmV0dXJuIChcbiAgICAgICAgPHRyXG4gICAgICAgICAga2V5PXtyb3cubmFtZX1cbiAgICAgICAgICBjbGFzc05hbWU9e3NlbGVjdGVkID8gJ2pwLW1vZC1zZWxlY3RlZCcgOiAnJ31cbiAgICAgICAgICBvbkNsaWNrPXtvbkNoZWNrfVxuICAgICAgICA+XG4gICAgICAgICAgPHRkPlxuICAgICAgICAgICAgPGlucHV0XG4gICAgICAgICAgICAgIHR5cGU9XCJyYWRpb1wiXG4gICAgICAgICAgICAgIG5hbWU9XCJzaG93LXBhY2thZ2UtbGljZW5zZVwiXG4gICAgICAgICAgICAgIHZhbHVlPXtpbmRleH1cbiAgICAgICAgICAgICAgb25DaGFuZ2U9e29uQ2hlY2t9XG4gICAgICAgICAgICAgIGNoZWNrZWQ9e3NlbGVjdGVkfVxuICAgICAgICAgICAgLz5cbiAgICAgICAgICA8L3RkPlxuICAgICAgICAgIDx0aD57cm93Lm5hbWV9PC90aD5cbiAgICAgICAgICA8dGQ+XG4gICAgICAgICAgICA8Y29kZT57cm93LnZlcnNpb25JbmZvfTwvY29kZT5cbiAgICAgICAgICA8L3RkPlxuICAgICAgICAgIDx0ZD5cbiAgICAgICAgICAgIDxjb2RlPntyb3cubGljZW5zZUlkfTwvY29kZT5cbiAgICAgICAgICA8L3RkPlxuICAgICAgICA8L3RyPlxuICAgICAgKTtcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcGFja2FnZSdzIGZ1bGwgbGljZW5zZSB0ZXh0XG4gICAqL1xuICBleHBvcnQgY2xhc3MgRnVsbFRleHQgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8TW9kZWw+IHtcbiAgICBjb25zdHJ1Y3Rvcihtb2RlbDogTW9kZWwpIHtcbiAgICAgIHN1cGVyKG1vZGVsKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLUxpY2Vuc2VzLVRleHQnKTtcbiAgICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVJlbmRlcmVkSFRNTENvbW1vbicpO1xuICAgICAgdGhpcy5hZGRDbGFzcygnanAtUmVuZGVyZWRNYXJrZG93bicpO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJlbmRlciB0aGUgbGljZW5zZSB0ZXh0LCBvciBhIG51bGwgc3RhdGUgaWYgbm8gcGFja2FnZSBpcyBzZWxlY3RlZFxuICAgICAqL1xuICAgIHByb3RlY3RlZCByZW5kZXIoKTogSlNYLkVsZW1lbnRbXSB7XG4gICAgICBjb25zdCB7IGN1cnJlbnRQYWNrYWdlLCB0cmFucyB9ID0gdGhpcy5tb2RlbDtcbiAgICAgIGxldCBoZWFkID0gJyc7XG4gICAgICBsZXQgcXVvdGUgPSB0cmFucy5fXygnTm8gUGFja2FnZSBzZWxlY3RlZCcpO1xuICAgICAgbGV0IGNvZGUgPSAnJztcbiAgICAgIGlmIChjdXJyZW50UGFja2FnZSkge1xuICAgICAgICBjb25zdCB7IG5hbWUsIHZlcnNpb25JbmZvLCBsaWNlbnNlSWQsIGV4dHJhY3RlZFRleHQgfSA9IGN1cnJlbnRQYWNrYWdlO1xuICAgICAgICBoZWFkID0gYCR7bmFtZX0gdiR7dmVyc2lvbkluZm99YDtcbiAgICAgICAgcXVvdGUgPSBgJHt0cmFucy5fXygnTGljZW5zZScpfTogJHtcbiAgICAgICAgICBsaWNlbnNlSWQgfHwgdHJhbnMuX18oJ05vIExpY2Vuc2UgSUQgZm91bmQnKVxuICAgICAgICB9YDtcbiAgICAgICAgY29kZSA9IGV4dHJhY3RlZFRleHQgfHwgdHJhbnMuX18oJ05vIExpY2Vuc2UgVGV4dCBmb3VuZCcpO1xuICAgICAgfVxuICAgICAgcmV0dXJuIFtcbiAgICAgICAgPGgxIGtleT1cImgxXCI+e2hlYWR9PC9oMT4sXG4gICAgICAgIDxibG9ja3F1b3RlIGtleT1cInF1b3RlXCI+XG4gICAgICAgICAgPGVtPntxdW90ZX08L2VtPlxuICAgICAgICA8L2Jsb2NrcXVvdGU+LFxuICAgICAgICA8Y29kZSBrZXk9XCJjb2RlXCI+e2NvZGV9PC9jb2RlPlxuICAgICAgXTtcbiAgICB9XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==