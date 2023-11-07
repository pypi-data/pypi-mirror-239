"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_csvviewer-extension_lib_index_js"],{

/***/ "../packages/csvviewer-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/csvviewer-extension/lib/index.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_csvviewer_lib_widget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/csvviewer/lib/widget */ "../packages/csvviewer/lib/widget.js");
/* harmony import */ var _jupyterlab_csvviewer_lib_toolbar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/csvviewer/lib/toolbar */ "../packages/csvviewer/lib/toolbar.js");
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/documentsearch */ "webpack/sharing/consume/default/@jupyterlab/documentsearch/@jupyterlab/documentsearch");
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module csvviewer-extension
 */








/**
 * The name of the factories that creates widgets.
 */
const FACTORY_CSV = 'CSVTable';
const FACTORY_TSV = 'TSVTable';
/**
 * The command IDs used by the csvviewer plugins.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.CSVGoToLine = 'csv:go-to-line';
    CommandIDs.TSVGoToLine = 'tsv:go-to-line';
})(CommandIDs || (CommandIDs = {}));
/**
 * The CSV file handler extension.
 */
const csv = {
    activate: activateCsv,
    id: '@jupyterlab/csvviewer-extension:csv',
    description: 'Adds viewer for CSV file types',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry
    ],
    autoStart: true
};
/**
 * The TSV file handler extension.
 */
const tsv = {
    activate: activateTsv,
    id: '@jupyterlab/csvviewer-extension:tsv',
    description: 'Adds viewer for TSV file types.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_5__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IThemeManager,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu,
        _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_4__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry
    ],
    autoStart: true
};
/**
 * Activate cssviewer extension for CSV files
 */
function activateCsv(app, translator, restorer, themeManager, mainMenu, searchRegistry, settingRegistry, toolbarRegistry) {
    const { commands, shell } = app;
    let toolbarFactory;
    if (toolbarRegistry) {
        toolbarRegistry.addFactory(FACTORY_CSV, 'delimiter', widget => new _jupyterlab_csvviewer_lib_toolbar__WEBPACK_IMPORTED_MODULE_6__.CSVDelimiter({
            widget: widget.content,
            translator
        }));
        if (settingRegistry) {
            toolbarFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, FACTORY_CSV, csv.id, translator);
        }
    }
    const trans = translator.load('jupyterlab');
    const factory = new _jupyterlab_csvviewer_lib_widget__WEBPACK_IMPORTED_MODULE_7__.CSVViewerFactory({
        name: FACTORY_CSV,
        label: trans.__('CSV Viewer'),
        fileTypes: ['csv'],
        defaultFor: ['csv'],
        readOnly: true,
        toolbarFactory,
        translator
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'csvviewer'
    });
    // The current styles for the data grids.
    let style = Private.LIGHT_STYLE;
    let rendererConfig = Private.LIGHT_TEXT_CONFIG;
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY_CSV }),
            name: widget => widget.context.path
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    const ft = app.docRegistry.getFileType('csv');
    let searchProviderInitialized = false;
    factory.widgetCreated.connect(async (sender, widget) => {
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        if (ft) {
            widget.title.icon = ft.icon;
            widget.title.iconClass = ft.iconClass;
            widget.title.iconLabel = ft.iconLabel;
        }
        // Delay await to execute `widget.title` setters (above) synchronously
        if (searchRegistry && !searchProviderInitialized) {
            const { CSVSearchProvider } = await __webpack_require__.e(/*! import() */ "packages_csvviewer-extension_lib_searchprovider_js").then(__webpack_require__.bind(__webpack_require__, /*! ./searchprovider */ "../packages/csvviewer-extension/lib/searchprovider.js"));
            searchRegistry.add('csv', CSVSearchProvider);
            searchProviderInitialized = true;
        }
        // Set the theme for the new widget; requires `.content` to be loaded.
        await widget.content.ready;
        widget.content.style = style;
        widget.content.rendererConfig = rendererConfig;
    });
    // Keep the themes up-to-date.
    const updateThemes = () => {
        const isLight = themeManager && themeManager.theme
            ? themeManager.isLight(themeManager.theme)
            : true;
        style = isLight ? Private.LIGHT_STYLE : Private.DARK_STYLE;
        rendererConfig = isLight
            ? Private.LIGHT_TEXT_CONFIG
            : Private.DARK_TEXT_CONFIG;
        tracker.forEach(async (grid) => {
            await grid.content.ready;
            grid.content.style = style;
            grid.content.rendererConfig = rendererConfig;
        });
    };
    if (themeManager) {
        themeManager.themeChanged.connect(updateThemes);
    }
    // Add commands
    const isEnabled = () => tracker.currentWidget !== null &&
        tracker.currentWidget === shell.currentWidget;
    commands.addCommand(CommandIDs.CSVGoToLine, {
        label: trans.__('Go to Line'),
        execute: async () => {
            const widget = tracker.currentWidget;
            if (widget === null) {
                return;
            }
            const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getNumber({
                title: trans.__('Go to Line'),
                value: 0
            });
            if (result.button.accept && result.value !== null) {
                widget.content.goToLine(result.value);
            }
        },
        isEnabled
    });
    if (mainMenu) {
        // Add go to line capability to the edit menu.
        mainMenu.editMenu.goToLiners.add({
            id: CommandIDs.CSVGoToLine,
            isEnabled
        });
    }
}
/**
 * Activate cssviewer extension for TSV files
 */
function activateTsv(app, translator, restorer, themeManager, mainMenu, searchRegistry, settingRegistry, toolbarRegistry) {
    const { commands, shell } = app;
    let toolbarFactory;
    if (toolbarRegistry) {
        toolbarRegistry.addFactory(FACTORY_TSV, 'delimiter', widget => new _jupyterlab_csvviewer_lib_toolbar__WEBPACK_IMPORTED_MODULE_6__.CSVDelimiter({
            widget: widget.content,
            translator
        }));
        if (settingRegistry) {
            toolbarFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, FACTORY_TSV, tsv.id, translator);
        }
    }
    const trans = translator.load('jupyterlab');
    const factory = new _jupyterlab_csvviewer_lib_widget__WEBPACK_IMPORTED_MODULE_7__.TSVViewerFactory({
        name: FACTORY_TSV,
        label: trans.__('TSV Viewer'),
        fileTypes: ['tsv'],
        defaultFor: ['tsv'],
        readOnly: true,
        toolbarFactory,
        translator
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'tsvviewer'
    });
    // The current styles for the data grids.
    let style = Private.LIGHT_STYLE;
    let rendererConfig = Private.LIGHT_TEXT_CONFIG;
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY_TSV }),
            name: widget => widget.context.path
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    const ft = app.docRegistry.getFileType('tsv');
    let searchProviderInitialized = false;
    factory.widgetCreated.connect(async (sender, widget) => {
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        if (ft) {
            widget.title.icon = ft.icon;
            widget.title.iconClass = ft.iconClass;
            widget.title.iconLabel = ft.iconLabel;
        }
        // Delay await to execute `widget.title` setters (above) synchronously
        if (searchRegistry && !searchProviderInitialized) {
            const { CSVSearchProvider } = await __webpack_require__.e(/*! import() */ "packages_csvviewer-extension_lib_searchprovider_js").then(__webpack_require__.bind(__webpack_require__, /*! ./searchprovider */ "../packages/csvviewer-extension/lib/searchprovider.js"));
            searchRegistry.add('tsv', CSVSearchProvider);
            searchProviderInitialized = true;
        }
        // Set the theme for the new widget; requires `.content` to be loaded.
        await widget.content.ready;
        widget.content.style = style;
        widget.content.rendererConfig = rendererConfig;
    });
    // Keep the themes up-to-date.
    const updateThemes = () => {
        const isLight = themeManager && themeManager.theme
            ? themeManager.isLight(themeManager.theme)
            : true;
        style = isLight ? Private.LIGHT_STYLE : Private.DARK_STYLE;
        rendererConfig = isLight
            ? Private.LIGHT_TEXT_CONFIG
            : Private.DARK_TEXT_CONFIG;
        tracker.forEach(async (grid) => {
            await grid.content.ready;
            grid.content.style = style;
            grid.content.rendererConfig = rendererConfig;
        });
    };
    if (themeManager) {
        themeManager.themeChanged.connect(updateThemes);
    }
    // Add commands
    const isEnabled = () => tracker.currentWidget !== null &&
        tracker.currentWidget === shell.currentWidget;
    commands.addCommand(CommandIDs.TSVGoToLine, {
        label: trans.__('Go to Line'),
        execute: async () => {
            const widget = tracker.currentWidget;
            if (widget === null) {
                return;
            }
            const result = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.InputDialog.getNumber({
                title: trans.__('Go to Line'),
                value: 0
            });
            if (result.button.accept && result.value !== null) {
                widget.content.goToLine(result.value);
            }
        },
        isEnabled
    });
    if (mainMenu) {
        // Add go to line capability to the edit menu.
        mainMenu.editMenu.goToLiners.add({
            id: CommandIDs.TSVGoToLine,
            isEnabled
        });
    }
}
/**
 * Export the plugins as default.
 */
const plugins = [csv, tsv];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * The light theme for the data grid.
     */
    Private.LIGHT_STYLE = {
        voidColor: '#F3F3F3',
        backgroundColor: 'white',
        headerBackgroundColor: '#EEEEEE',
        gridLineColor: 'rgba(20, 20, 20, 0.15)',
        headerGridLineColor: 'rgba(20, 20, 20, 0.25)',
        rowBackgroundColor: i => (i % 2 === 0 ? '#F5F5F5' : 'white')
    };
    /**
     * The dark theme for the data grid.
     */
    Private.DARK_STYLE = {
        voidColor: 'black',
        backgroundColor: '#111111',
        headerBackgroundColor: '#424242',
        gridLineColor: 'rgba(235, 235, 235, 0.15)',
        headerGridLineColor: 'rgba(235, 235, 235, 0.25)',
        rowBackgroundColor: i => (i % 2 === 0 ? '#212121' : '#111111')
    };
    /**
     * The light config for the data grid renderer.
     */
    Private.LIGHT_TEXT_CONFIG = {
        textColor: '#111111',
        matchBackgroundColor: '#FFFFE0',
        currentMatchBackgroundColor: '#FFFF00',
        horizontalAlignment: 'right'
    };
    /**
     * The dark config for the data grid renderer.
     */
    Private.DARK_TEXT_CONFIG = {
        textColor: '#F5F5F5',
        matchBackgroundColor: '#838423',
        currentMatchBackgroundColor: '#A3807A',
        horizontalAlignment: 'right'
    };
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY3N2dmlld2VyLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuYTI5OWI2OWUxODFiNTQ4OGQ3Y2EuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFPSDtBQUlZO0FBQ3VCO0FBSUk7QUFDcEI7QUFFYztBQUNUO0FBR3REOztHQUVHO0FBQ0gsTUFBTSxXQUFXLEdBQUcsVUFBVSxDQUFDO0FBQy9CLE1BQU0sV0FBVyxHQUFHLFVBQVUsQ0FBQztBQUUvQjs7R0FFRztBQUNILElBQVUsVUFBVSxDQUluQjtBQUpELFdBQVUsVUFBVTtJQUNMLHNCQUFXLEdBQUcsZ0JBQWdCLENBQUM7SUFFL0Isc0JBQVcsR0FBRyxnQkFBZ0IsQ0FBQztBQUM5QyxDQUFDLEVBSlMsVUFBVSxLQUFWLFVBQVUsUUFJbkI7QUFFRDs7R0FFRztBQUNILE1BQU0sR0FBRyxHQUFnQztJQUN2QyxRQUFRLEVBQUUsV0FBVztJQUNyQixFQUFFLEVBQUUscUNBQXFDO0lBQ3pDLFdBQVcsRUFBRSxnQ0FBZ0M7SUFDN0MsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUU7UUFDUixvRUFBZTtRQUNmLCtEQUFhO1FBQ2IsMkRBQVM7UUFDVCwrRUFBdUI7UUFDdkIseUVBQWdCO1FBQ2hCLHdFQUFzQjtLQUN2QjtJQUNELFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7R0FFRztBQUNILE1BQU0sR0FBRyxHQUFnQztJQUN2QyxRQUFRLEVBQUUsV0FBVztJQUNyQixFQUFFLEVBQUUscUNBQXFDO0lBQ3pDLFdBQVcsRUFBRSxpQ0FBaUM7SUFDOUMsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUU7UUFDUixvRUFBZTtRQUNmLCtEQUFhO1FBQ2IsMkRBQVM7UUFDVCwrRUFBdUI7UUFDdkIseUVBQWdCO1FBQ2hCLHdFQUFzQjtLQUN2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LFNBQVM7UUFDL0IsMkJBQTJCLEVBQUUsU0FBUztRQUN0QyxtQkFBbUIsRUFBRSxPQUFPO0tBQzdCLENBQUM7QUFDSixDQUFDLEVBNUNTLE9BQU8sS0FBUCxPQUFPLFFBNENoQiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jc3Z2aWV3ZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBjc3Z2aWV3ZXItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBjcmVhdGVUb29sYmFyRmFjdG9yeSxcbiAgSW5wdXREaWFsb2csXG4gIElUaGVtZU1hbmFnZXIsXG4gIElUb29sYmFyV2lkZ2V0UmVnaXN0cnksXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgQ1NWVmlld2VyRmFjdG9yeSxcbiAgVFNWVmlld2VyRmFjdG9yeVxufSBmcm9tICdAanVweXRlcmxhYi9jc3Z2aWV3ZXIvbGliL3dpZGdldCc7XG5pbXBvcnQgeyBDU1ZEZWxpbWl0ZXIgfSBmcm9tICdAanVweXRlcmxhYi9jc3Z2aWV3ZXIvbGliL3Rvb2xiYXInO1xuaW1wb3J0IHR5cGUgeyBDU1ZWaWV3ZXIgfSBmcm9tICdAanVweXRlcmxhYi9jc3Z2aWV3ZXInO1xuaW1wb3J0IHR5cGUgeyBUZXh0UmVuZGVyQ29uZmlnIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY3N2dmlld2VyJztcbmltcG9ydCB7IERvY3VtZW50UmVnaXN0cnksIElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IElTZWFyY2hQcm92aWRlclJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jdW1lbnRzZWFyY2gnO1xuaW1wb3J0IHsgSU1haW5NZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvbWFpbm1lbnUnO1xuaW1wb3J0IHsgSU9ic2VydmFibGVMaXN0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvb2JzZXJ2YWJsZXMnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB0eXBlIHsgRGF0YUdyaWQgfSBmcm9tICdAbHVtaW5vL2RhdGFncmlkJztcblxuLyoqXG4gKiBUaGUgbmFtZSBvZiB0aGUgZmFjdG9yaWVzIHRoYXQgY3JlYXRlcyB3aWRnZXRzLlxuICovXG5jb25zdCBGQUNUT1JZX0NTViA9ICdDU1ZUYWJsZSc7XG5jb25zdCBGQUNUT1JZX1RTViA9ICdUU1ZUYWJsZSc7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIGNzdnZpZXdlciBwbHVnaW5zLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBDU1ZHb1RvTGluZSA9ICdjc3Y6Z28tdG8tbGluZSc7XG5cbiAgZXhwb3J0IGNvbnN0IFRTVkdvVG9MaW5lID0gJ3Rzdjpnby10by1saW5lJztcbn1cblxuLyoqXG4gKiBUaGUgQ1NWIGZpbGUgaGFuZGxlciBleHRlbnNpb24uXG4gKi9cbmNvbnN0IGNzdjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBhY3RpdmF0ZTogYWN0aXZhdGVDc3YsXG4gIGlkOiAnQGp1cHl0ZXJsYWIvY3N2dmlld2VyLWV4dGVuc2lvbjpjc3YnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgdmlld2VyIGZvciBDU1YgZmlsZSB0eXBlcycsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW1xuICAgIElMYXlvdXRSZXN0b3JlcixcbiAgICBJVGhlbWVNYW5hZ2VyLFxuICAgIElNYWluTWVudSxcbiAgICBJU2VhcmNoUHJvdmlkZXJSZWdpc3RyeSxcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIElUb29sYmFyV2lkZ2V0UmVnaXN0cnlcbiAgXSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIFRoZSBUU1YgZmlsZSBoYW5kbGVyIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgdHN2OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGFjdGl2YXRlOiBhY3RpdmF0ZVRzdixcbiAgaWQ6ICdAanVweXRlcmxhYi9jc3Z2aWV3ZXItZXh0ZW5zaW9uOnRzdicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB2aWV3ZXIgZm9yIFRTViBmaWxlIHR5cGVzLicsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW1xuICAgIElMYXlvdXRSZXN0b3JlcixcbiAgICBJVGhlbWVNYW5hZ2VyLFxuICAgIElNYWluTWVudSxcbiAgICBJU2VhcmNoUHJvdmlkZXJSZWdpc3RyeSxcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIElUb29sYmFyV2lkZ2V0UmVnaXN0cnlcbiAgXSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEFjdGl2YXRlIGNzc3ZpZXdlciBleHRlbnNpb24gZm9yIENTViBmaWxlc1xuICovXG5mdW5jdGlvbiBhY3RpdmF0ZUNzdihcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgdGhlbWVNYW5hZ2VyOiBJVGhlbWVNYW5hZ2VyIHwgbnVsbCxcbiAgbWFpbk1lbnU6IElNYWluTWVudSB8IG51bGwsXG4gIHNlYXJjaFJlZ2lzdHJ5OiBJU2VhcmNoUHJvdmlkZXJSZWdpc3RyeSB8IG51bGwsXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGwsXG4gIHRvb2xiYXJSZWdpc3RyeTogSVRvb2xiYXJXaWRnZXRSZWdpc3RyeSB8IG51bGxcbik6IHZvaWQge1xuICBjb25zdCB7IGNvbW1hbmRzLCBzaGVsbCB9ID0gYXBwO1xuICBsZXQgdG9vbGJhckZhY3Rvcnk6XG4gICAgfCAoKFxuICAgICAgICB3aWRnZXQ6IElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+XG4gICAgICApID0+IElPYnNlcnZhYmxlTGlzdDxEb2N1bWVudFJlZ2lzdHJ5LklUb29sYmFySXRlbT4pXG4gICAgfCB1bmRlZmluZWQ7XG5cbiAgaWYgKHRvb2xiYXJSZWdpc3RyeSkge1xuICAgIHRvb2xiYXJSZWdpc3RyeS5hZGRGYWN0b3J5PElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+PihcbiAgICAgIEZBQ1RPUllfQ1NWLFxuICAgICAgJ2RlbGltaXRlcicsXG4gICAgICB3aWRnZXQgPT5cbiAgICAgICAgbmV3IENTVkRlbGltaXRlcih7XG4gICAgICAgICAgd2lkZ2V0OiB3aWRnZXQuY29udGVudCxcbiAgICAgICAgICB0cmFuc2xhdG9yXG4gICAgICAgIH0pXG4gICAgKTtcblxuICAgIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICAgIHRvb2xiYXJGYWN0b3J5ID0gY3JlYXRlVG9vbGJhckZhY3RvcnkoXG4gICAgICAgIHRvb2xiYXJSZWdpc3RyeSxcbiAgICAgICAgc2V0dGluZ1JlZ2lzdHJ5LFxuICAgICAgICBGQUNUT1JZX0NTVixcbiAgICAgICAgY3N2LmlkLFxuICAgICAgICB0cmFuc2xhdG9yXG4gICAgICApO1xuICAgIH1cbiAgfVxuXG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgY29uc3QgZmFjdG9yeSA9IG5ldyBDU1ZWaWV3ZXJGYWN0b3J5KHtcbiAgICBuYW1lOiBGQUNUT1JZX0NTVixcbiAgICBsYWJlbDogdHJhbnMuX18oJ0NTViBWaWV3ZXInKSxcbiAgICBmaWxlVHlwZXM6IFsnY3N2J10sXG4gICAgZGVmYXVsdEZvcjogWydjc3YnXSxcbiAgICByZWFkT25seTogdHJ1ZSxcbiAgICB0b29sYmFyRmFjdG9yeSxcbiAgICB0cmFuc2xhdG9yXG4gIH0pO1xuICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PENTVlZpZXdlcj4+KHtcbiAgICBuYW1lc3BhY2U6ICdjc3Z2aWV3ZXInXG4gIH0pO1xuXG4gIC8vIFRoZSBjdXJyZW50IHN0eWxlcyBmb3IgdGhlIGRhdGEgZ3JpZHMuXG4gIGxldCBzdHlsZTogRGF0YUdyaWQuU3R5bGUgPSBQcml2YXRlLkxJR0hUX1NUWUxFO1xuICBsZXQgcmVuZGVyZXJDb25maWc6IFRleHRSZW5kZXJDb25maWcgPSBQcml2YXRlLkxJR0hUX1RFWFRfQ09ORklHO1xuXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIC8vIEhhbmRsZSBzdGF0ZSByZXN0b3JhdGlvbi5cbiAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgY29tbWFuZDogJ2RvY21hbmFnZXI6b3BlbicsXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHsgcGF0aDogd2lkZ2V0LmNvbnRleHQucGF0aCwgZmFjdG9yeTogRkFDVE9SWV9DU1YgfSksXG4gICAgICBuYW1lOiB3aWRnZXQgPT4gd2lkZ2V0LmNvbnRleHQucGF0aFxuICAgIH0pO1xuICB9XG5cbiAgYXBwLmRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG4gIGNvbnN0IGZ0ID0gYXBwLmRvY1JlZ2lzdHJ5LmdldEZpbGVUeXBlKCdjc3YnKTtcblxuICBsZXQgc2VhcmNoUHJvdmlkZXJJbml0aWFsaXplZCA9IGZhbHNlO1xuXG4gIGZhY3Rvcnkud2lkZ2V0Q3JlYXRlZC5jb25uZWN0KGFzeW5jIChzZW5kZXIsIHdpZGdldCkgPT4ge1xuICAgIC8vIFRyYWNrIHRoZSB3aWRnZXQuXG4gICAgdm9pZCB0cmFja2VyLmFkZCh3aWRnZXQpO1xuICAgIC8vIE5vdGlmeSB0aGUgd2lkZ2V0IHRyYWNrZXIgaWYgcmVzdG9yZSBkYXRhIG5lZWRzIHRvIHVwZGF0ZS5cbiAgICB3aWRnZXQuY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHZvaWQgdHJhY2tlci5zYXZlKHdpZGdldCk7XG4gICAgfSk7XG5cbiAgICBpZiAoZnQpIHtcbiAgICAgIHdpZGdldC50aXRsZS5pY29uID0gZnQuaWNvbiE7XG4gICAgICB3aWRnZXQudGl0bGUuaWNvbkNsYXNzID0gZnQuaWNvbkNsYXNzITtcbiAgICAgIHdpZGdldC50aXRsZS5pY29uTGFiZWwgPSBmdC5pY29uTGFiZWwhO1xuICAgIH1cblxuICAgIC8vIERlbGF5IGF3YWl0IHRvIGV4ZWN1dGUgYHdpZGdldC50aXRsZWAgc2V0dGVycyAoYWJvdmUpIHN5bmNocm9ub3VzbHlcbiAgICBpZiAoc2VhcmNoUmVnaXN0cnkgJiYgIXNlYXJjaFByb3ZpZGVySW5pdGlhbGl6ZWQpIHtcbiAgICAgIGNvbnN0IHsgQ1NWU2VhcmNoUHJvdmlkZXIgfSA9IGF3YWl0IGltcG9ydCgnLi9zZWFyY2hwcm92aWRlcicpO1xuICAgICAgc2VhcmNoUmVnaXN0cnkuYWRkKCdjc3YnLCBDU1ZTZWFyY2hQcm92aWRlcik7XG4gICAgICBzZWFyY2hQcm92aWRlckluaXRpYWxpemVkID0gdHJ1ZTtcbiAgICB9XG5cbiAgICAvLyBTZXQgdGhlIHRoZW1lIGZvciB0aGUgbmV3IHdpZGdldDsgcmVxdWlyZXMgYC5jb250ZW50YCB0byBiZSBsb2FkZWQuXG4gICAgYXdhaXQgd2lkZ2V0LmNvbnRlbnQucmVhZHk7XG4gICAgd2lkZ2V0LmNvbnRlbnQuc3R5bGUgPSBzdHlsZTtcbiAgICB3aWRnZXQuY29udGVudC5yZW5kZXJlckNvbmZpZyA9IHJlbmRlcmVyQ29uZmlnO1xuICB9KTtcblxuICAvLyBLZWVwIHRoZSB0aGVtZXMgdXAtdG8tZGF0ZS5cbiAgY29uc3QgdXBkYXRlVGhlbWVzID0gKCkgPT4ge1xuICAgIGNvbnN0IGlzTGlnaHQgPVxuICAgICAgdGhlbWVNYW5hZ2VyICYmIHRoZW1lTWFuYWdlci50aGVtZVxuICAgICAgICA/IHRoZW1lTWFuYWdlci5pc0xpZ2h0KHRoZW1lTWFuYWdlci50aGVtZSlcbiAgICAgICAgOiB0cnVlO1xuICAgIHN0eWxlID0gaXNMaWdodCA/IFByaXZhdGUuTElHSFRfU1RZTEUgOiBQcml2YXRlLkRBUktfU1RZTEU7XG4gICAgcmVuZGVyZXJDb25maWcgPSBpc0xpZ2h0XG4gICAgICA/IFByaXZhdGUuTElHSFRfVEVYVF9DT05GSUdcbiAgICAgIDogUHJpdmF0ZS5EQVJLX1RFWFRfQ09ORklHO1xuICAgIHRyYWNrZXIuZm9yRWFjaChhc3luYyBncmlkID0+IHtcbiAgICAgIGF3YWl0IGdyaWQuY29udGVudC5yZWFkeTtcbiAgICAgIGdyaWQuY29udGVudC5zdHlsZSA9IHN0eWxlO1xuICAgICAgZ3JpZC5jb250ZW50LnJlbmRlcmVyQ29uZmlnID0gcmVuZGVyZXJDb25maWc7XG4gICAgfSk7XG4gIH07XG4gIGlmICh0aGVtZU1hbmFnZXIpIHtcbiAgICB0aGVtZU1hbmFnZXIudGhlbWVDaGFuZ2VkLmNvbm5lY3QodXBkYXRlVGhlbWVzKTtcbiAgfVxuXG4gIC8vIEFkZCBjb21tYW5kc1xuICBjb25zdCBpc0VuYWJsZWQgPSAoKSA9PlxuICAgIHRyYWNrZXIuY3VycmVudFdpZGdldCAhPT0gbnVsbCAmJlxuICAgIHRyYWNrZXIuY3VycmVudFdpZGdldCA9PT0gc2hlbGwuY3VycmVudFdpZGdldDtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuQ1NWR29Ub0xpbmUsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ0dvIHRvIExpbmUnKSxcbiAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAod2lkZ2V0ID09PSBudWxsKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IElucHV0RGlhbG9nLmdldE51bWJlcih7XG4gICAgICAgIHRpdGxlOiB0cmFucy5fXygnR28gdG8gTGluZScpLFxuICAgICAgICB2YWx1ZTogMFxuICAgICAgfSk7XG4gICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQgJiYgcmVzdWx0LnZhbHVlICE9PSBudWxsKSB7XG4gICAgICAgIHdpZGdldC5jb250ZW50LmdvVG9MaW5lKHJlc3VsdC52YWx1ZSk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgaWYgKG1haW5NZW51KSB7XG4gICAgLy8gQWRkIGdvIHRvIGxpbmUgY2FwYWJpbGl0eSB0byB0aGUgZWRpdCBtZW51LlxuICAgIG1haW5NZW51LmVkaXRNZW51LmdvVG9MaW5lcnMuYWRkKHtcbiAgICAgIGlkOiBDb21tYW5kSURzLkNTVkdvVG9MaW5lLFxuICAgICAgaXNFbmFibGVkXG4gICAgfSk7XG4gIH1cbn1cblxuLyoqXG4gKiBBY3RpdmF0ZSBjc3N2aWV3ZXIgZXh0ZW5zaW9uIGZvciBUU1YgZmlsZXNcbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGVUc3YoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGwsXG4gIHRoZW1lTWFuYWdlcjogSVRoZW1lTWFuYWdlciB8IG51bGwsXG4gIG1haW5NZW51OiBJTWFpbk1lbnUgfCBudWxsLFxuICBzZWFyY2hSZWdpc3RyeTogSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnkgfCBudWxsLFxuICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsLFxuICB0b29sYmFyUmVnaXN0cnk6IElUb29sYmFyV2lkZ2V0UmVnaXN0cnkgfCBudWxsXG4pOiB2b2lkIHtcbiAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgbGV0IHRvb2xiYXJGYWN0b3J5OlxuICAgIHwgKChcbiAgICAgICAgd2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXQ8Q1NWVmlld2VyPlxuICAgICAgKSA9PiBJT2JzZXJ2YWJsZUxpc3Q8RG9jdW1lbnRSZWdpc3RyeS5JVG9vbGJhckl0ZW0+KVxuICAgIHwgdW5kZWZpbmVkO1xuXG4gIGlmICh0b29sYmFyUmVnaXN0cnkpIHtcbiAgICB0b29sYmFyUmVnaXN0cnkuYWRkRmFjdG9yeTxJRG9jdW1lbnRXaWRnZXQ8Q1NWVmlld2VyPj4oXG4gICAgICBGQUNUT1JZX1RTVixcbiAgICAgICdkZWxpbWl0ZXInLFxuICAgICAgd2lkZ2V0ID0+XG4gICAgICAgIG5ldyBDU1ZEZWxpbWl0ZXIoe1xuICAgICAgICAgIHdpZGdldDogd2lkZ2V0LmNvbnRlbnQsXG4gICAgICAgICAgdHJhbnNsYXRvclxuICAgICAgICB9KVxuICAgICk7XG5cbiAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICB0b29sYmFyRmFjdG9yeSA9IGNyZWF0ZVRvb2xiYXJGYWN0b3J5KFxuICAgICAgICB0b29sYmFyUmVnaXN0cnksXG4gICAgICAgIHNldHRpbmdSZWdpc3RyeSxcbiAgICAgICAgRkFDVE9SWV9UU1YsXG4gICAgICAgIHRzdi5pZCxcbiAgICAgICAgdHJhbnNsYXRvclxuICAgICAgKTtcbiAgICB9XG4gIH1cblxuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gIGNvbnN0IGZhY3RvcnkgPSBuZXcgVFNWVmlld2VyRmFjdG9yeSh7XG4gICAgbmFtZTogRkFDVE9SWV9UU1YsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdUU1YgVmlld2VyJyksXG4gICAgZmlsZVR5cGVzOiBbJ3RzdiddLFxuICAgIGRlZmF1bHRGb3I6IFsndHN2J10sXG4gICAgcmVhZE9ubHk6IHRydWUsXG4gICAgdG9vbGJhckZhY3RvcnksXG4gICAgdHJhbnNsYXRvclxuICB9KTtcbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxDU1ZWaWV3ZXI+Pih7XG4gICAgbmFtZXNwYWNlOiAndHN2dmlld2VyJ1xuICB9KTtcblxuICAvLyBUaGUgY3VycmVudCBzdHlsZXMgZm9yIHRoZSBkYXRhIGdyaWRzLlxuICBsZXQgc3R5bGU6IERhdGFHcmlkLlN0eWxlID0gUHJpdmF0ZS5MSUdIVF9TVFlMRTtcbiAgbGV0IHJlbmRlcmVyQ29uZmlnOiBUZXh0UmVuZGVyQ29uZmlnID0gUHJpdmF0ZS5MSUdIVF9URVhUX0NPTkZJRztcblxuICBpZiAocmVzdG9yZXIpIHtcbiAgICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gICAgdm9pZCByZXN0b3Jlci5yZXN0b3JlKHRyYWNrZXIsIHtcbiAgICAgIGNvbW1hbmQ6ICdkb2NtYW5hZ2VyOm9wZW4nLFxuICAgICAgYXJnczogd2lkZ2V0ID0+ICh7IHBhdGg6IHdpZGdldC5jb250ZXh0LnBhdGgsIGZhY3Rvcnk6IEZBQ1RPUllfVFNWIH0pLFxuICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb250ZXh0LnBhdGhcbiAgICB9KTtcbiAgfVxuXG4gIGFwcC5kb2NSZWdpc3RyeS5hZGRXaWRnZXRGYWN0b3J5KGZhY3RvcnkpO1xuICBjb25zdCBmdCA9IGFwcC5kb2NSZWdpc3RyeS5nZXRGaWxlVHlwZSgndHN2Jyk7XG5cbiAgbGV0IHNlYXJjaFByb3ZpZGVySW5pdGlhbGl6ZWQgPSBmYWxzZTtcblxuICBmYWN0b3J5LndpZGdldENyZWF0ZWQuY29ubmVjdChhc3luYyAoc2VuZGVyLCB3aWRnZXQpID0+IHtcbiAgICAvLyBUcmFjayB0aGUgd2lkZ2V0LlxuICAgIHZvaWQgdHJhY2tlci5hZGQod2lkZ2V0KTtcbiAgICAvLyBOb3RpZnkgdGhlIHdpZGdldCB0cmFja2VyIGlmIHJlc3RvcmUgZGF0YSBuZWVkcyB0byB1cGRhdGUuXG4gICAgd2lkZ2V0LmNvbnRleHQucGF0aENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB2b2lkIHRyYWNrZXIuc2F2ZSh3aWRnZXQpO1xuICAgIH0pO1xuXG4gICAgaWYgKGZ0KSB7XG4gICAgICB3aWRnZXQudGl0bGUuaWNvbiA9IGZ0Lmljb24hO1xuICAgICAgd2lkZ2V0LnRpdGxlLmljb25DbGFzcyA9IGZ0Lmljb25DbGFzcyE7XG4gICAgICB3aWRnZXQudGl0bGUuaWNvbkxhYmVsID0gZnQuaWNvbkxhYmVsITtcbiAgICB9XG5cbiAgICAvLyBEZWxheSBhd2FpdCB0byBleGVjdXRlIGB3aWRnZXQudGl0bGVgIHNldHRlcnMgKGFib3ZlKSBzeW5jaHJvbm91c2x5XG4gICAgaWYgKHNlYXJjaFJlZ2lzdHJ5ICYmICFzZWFyY2hQcm92aWRlckluaXRpYWxpemVkKSB7XG4gICAgICBjb25zdCB7IENTVlNlYXJjaFByb3ZpZGVyIH0gPSBhd2FpdCBpbXBvcnQoJy4vc2VhcmNocHJvdmlkZXInKTtcbiAgICAgIHNlYXJjaFJlZ2lzdHJ5LmFkZCgndHN2JywgQ1NWU2VhcmNoUHJvdmlkZXIpO1xuICAgICAgc2VhcmNoUHJvdmlkZXJJbml0aWFsaXplZCA9IHRydWU7XG4gICAgfVxuXG4gICAgLy8gU2V0IHRoZSB0aGVtZSBmb3IgdGhlIG5ldyB3aWRnZXQ7IHJlcXVpcmVzIGAuY29udGVudGAgdG8gYmUgbG9hZGVkLlxuICAgIGF3YWl0IHdpZGdldC5jb250ZW50LnJlYWR5O1xuICAgIHdpZGdldC5jb250ZW50LnN0eWxlID0gc3R5bGU7XG4gICAgd2lkZ2V0LmNvbnRlbnQucmVuZGVyZXJDb25maWcgPSByZW5kZXJlckNvbmZpZztcbiAgfSk7XG5cbiAgLy8gS2VlcCB0aGUgdGhlbWVzIHVwLXRvLWRhdGUuXG4gIGNvbnN0IHVwZGF0ZVRoZW1lcyA9ICgpID0+IHtcbiAgICBjb25zdCBpc0xpZ2h0ID1cbiAgICAgIHRoZW1lTWFuYWdlciAmJiB0aGVtZU1hbmFnZXIudGhlbWVcbiAgICAgICAgPyB0aGVtZU1hbmFnZXIuaXNMaWdodCh0aGVtZU1hbmFnZXIudGhlbWUpXG4gICAgICAgIDogdHJ1ZTtcbiAgICBzdHlsZSA9IGlzTGlnaHQgPyBQcml2YXRlLkxJR0hUX1NUWUxFIDogUHJpdmF0ZS5EQVJLX1NUWUxFO1xuICAgIHJlbmRlcmVyQ29uZmlnID0gaXNMaWdodFxuICAgICAgPyBQcml2YXRlLkxJR0hUX1RFWFRfQ09ORklHXG4gICAgICA6IFByaXZhdGUuREFSS19URVhUX0NPTkZJRztcbiAgICB0cmFja2VyLmZvckVhY2goYXN5bmMgZ3JpZCA9PiB7XG4gICAgICBhd2FpdCBncmlkLmNvbnRlbnQucmVhZHk7XG4gICAgICBncmlkLmNvbnRlbnQuc3R5bGUgPSBzdHlsZTtcbiAgICAgIGdyaWQuY29udGVudC5yZW5kZXJlckNvbmZpZyA9IHJlbmRlcmVyQ29uZmlnO1xuICAgIH0pO1xuICB9O1xuICBpZiAodGhlbWVNYW5hZ2VyKSB7XG4gICAgdGhlbWVNYW5hZ2VyLnRoZW1lQ2hhbmdlZC5jb25uZWN0KHVwZGF0ZVRoZW1lcyk7XG4gIH1cblxuICAvLyBBZGQgY29tbWFuZHNcbiAgY29uc3QgaXNFbmFibGVkID0gKCkgPT5cbiAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgIT09IG51bGwgJiZcbiAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgPT09IHNoZWxsLmN1cnJlbnRXaWRnZXQ7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLlRTVkdvVG9MaW5lLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdHbyB0byBMaW5lJyksXG4gICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgICAgaWYgKHdpZGdldCA9PT0gbnVsbCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjb25zdCByZXN1bHQgPSBhd2FpdCBJbnB1dERpYWxvZy5nZXROdW1iZXIoe1xuICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0dvIHRvIExpbmUnKSxcbiAgICAgICAgdmFsdWU6IDBcbiAgICAgIH0pO1xuICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0ICYmIHJlc3VsdC52YWx1ZSAhPT0gbnVsbCkge1xuICAgICAgICB3aWRnZXQuY29udGVudC5nb1RvTGluZShyZXN1bHQudmFsdWUpO1xuICAgICAgfVxuICAgIH0sXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGlmIChtYWluTWVudSkge1xuICAgIC8vIEFkZCBnbyB0byBsaW5lIGNhcGFiaWxpdHkgdG8gdGhlIGVkaXQgbWVudS5cbiAgICBtYWluTWVudS5lZGl0TWVudS5nb1RvTGluZXJzLmFkZCh7XG4gICAgICBpZDogQ29tbWFuZElEcy5UU1ZHb1RvTGluZSxcbiAgICAgIGlzRW5hYmxlZFxuICAgIH0pO1xuICB9XG59XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbY3N2LCB0c3ZdO1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBUaGUgbGlnaHQgdGhlbWUgZm9yIHRoZSBkYXRhIGdyaWQuXG4gICAqL1xuICBleHBvcnQgY29uc3QgTElHSFRfU1RZTEU6IERhdGFHcmlkLlN0eWxlID0ge1xuICAgIHZvaWRDb2xvcjogJyNGM0YzRjMnLFxuICAgIGJhY2tncm91bmRDb2xvcjogJ3doaXRlJyxcbiAgICBoZWFkZXJCYWNrZ3JvdW5kQ29sb3I6ICcjRUVFRUVFJyxcbiAgICBncmlkTGluZUNvbG9yOiAncmdiYSgyMCwgMjAsIDIwLCAwLjE1KScsXG4gICAgaGVhZGVyR3JpZExpbmVDb2xvcjogJ3JnYmEoMjAsIDIwLCAyMCwgMC4yNSknLFxuICAgIHJvd0JhY2tncm91bmRDb2xvcjogaSA9PiAoaSAlIDIgPT09IDAgPyAnI0Y1RjVGNScgOiAnd2hpdGUnKVxuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgZGFyayB0aGVtZSBmb3IgdGhlIGRhdGEgZ3JpZC5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBEQVJLX1NUWUxFOiBEYXRhR3JpZC5TdHlsZSA9IHtcbiAgICB2b2lkQ29sb3I6ICdibGFjaycsXG4gICAgYmFja2dyb3VuZENvbG9yOiAnIzExMTExMScsXG4gICAgaGVhZGVyQmFja2dyb3VuZENvbG9yOiAnIzQyNDI0MicsXG4gICAgZ3JpZExpbmVDb2xvcjogJ3JnYmEoMjM1LCAyMzUsIDIzNSwgMC4xNSknLFxuICAgIGhlYWRlckdyaWRMaW5lQ29sb3I6ICdyZ2JhKDIzNSwgMjM1LCAyMzUsIDAuMjUpJyxcbiAgICByb3dCYWNrZ3JvdW5kQ29sb3I6IGkgPT4gKGkgJSAyID09PSAwID8gJyMyMTIxMjEnIDogJyMxMTExMTEnKVxuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgbGlnaHQgY29uZmlnIGZvciB0aGUgZGF0YSBncmlkIHJlbmRlcmVyLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IExJR0hUX1RFWFRfQ09ORklHOiBUZXh0UmVuZGVyQ29uZmlnID0ge1xuICAgIHRleHRDb2xvcjogJyMxMTExMTEnLFxuICAgIG1hdGNoQmFja2dyb3VuZENvbG9yOiAnI0ZGRkZFMCcsXG4gICAgY3VycmVudE1hdGNoQmFja2dyb3VuZENvbG9yOiAnI0ZGRkYwMCcsXG4gICAgaG9yaXpvbnRhbEFsaWdubWVudDogJ3JpZ2h0J1xuICB9O1xuXG4gIC8qKlxuICAgKiBUaGUgZGFyayBjb25maWcgZm9yIHRoZSBkYXRhIGdyaWQgcmVuZGVyZXIuXG4gICAqL1xuICBleHBvcnQgY29uc3QgREFSS19URVhUX0NPTkZJRzogVGV4dFJlbmRlckNvbmZpZyA9IHtcbiAgICB0ZXh0Q29sb3I6ICcjRjVGNUY1JyxcbiAgICBtYXRjaEJhY2tncm91bmRDb2xvcjogJyM4Mzg0MjMnLFxuICAgIGN1cnJlbnRNYXRjaEJhY2tncm91bmRDb2xvcjogJyNBMzgwN0EnLFxuICAgIGhvcml6b250YWxBbGlnbm1lbnQ6ICdyaWdodCdcbiAgfTtcbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==