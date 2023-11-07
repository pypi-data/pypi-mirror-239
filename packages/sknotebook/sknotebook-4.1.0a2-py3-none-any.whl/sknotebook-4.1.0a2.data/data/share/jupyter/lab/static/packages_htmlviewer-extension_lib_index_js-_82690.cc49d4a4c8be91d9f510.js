"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_htmlviewer-extension_lib_index_js-_82690"],{

/***/ "../packages/htmlviewer-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/htmlviewer-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/htmlviewer */ "webpack/sharing/consume/default/@jupyterlab/htmlviewer/@jupyterlab/htmlviewer");
/* harmony import */ var _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module htmlviewer-extension
 */






const HTML_VIEWER_PLUGIN_ID = '@jupyterlab/htmlviewer-extension:plugin';
/**
 * Factory name
 */
const FACTORY = 'HTML Viewer';
/**
 * Command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.trustHTML = 'htmlviewer:trust-html';
})(CommandIDs || (CommandIDs = {}));
/**
 * The HTML file handler extension.
 */
const htmlPlugin = {
    activate: activateHTMLViewer,
    id: HTML_VIEWER_PLUGIN_ID,
    description: 'Adds HTML file viewer and provides its tracker.',
    provides: _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.IHTMLViewerTracker,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.IToolbarWidgetRegistry
    ],
    autoStart: true
};
/**
 * Activate the HTMLViewer extension.
 */
function activateHTMLViewer(app, translator, palette, restorer, settingRegistry, toolbarRegistry) {
    let toolbarFactory;
    const trans = translator.load('jupyterlab');
    if (toolbarRegistry) {
        toolbarRegistry.addFactory(FACTORY, 'refresh', widget => _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.ToolbarItems.createRefreshButton(widget, translator));
        toolbarRegistry.addFactory(FACTORY, 'trust', widget => _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.ToolbarItems.createTrustButton(widget, translator));
        if (settingRegistry) {
            toolbarFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createToolbarFactory)(toolbarRegistry, settingRegistry, FACTORY, htmlPlugin.id, translator);
        }
    }
    // Add an HTML file type to the docregistry.
    const ft = {
        name: 'html',
        contentType: 'file',
        fileFormat: 'text',
        displayName: trans.__('HTML File'),
        extensions: ['.html'],
        mimeTypes: ['text/html'],
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.html5Icon
    };
    app.docRegistry.addFileType(ft);
    // Create a new viewer factory.
    const factory = new _jupyterlab_htmlviewer__WEBPACK_IMPORTED_MODULE_2__.HTMLViewerFactory({
        name: FACTORY,
        label: trans.__('HTML Viewer'),
        fileTypes: ['html'],
        defaultFor: ['html'],
        readOnly: true,
        toolbarFactory,
        translator
    });
    // Create a widget tracker for HTML documents.
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace: 'htmlviewer'
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: 'HTML Viewer' }),
            name: widget => widget.context.path
        });
    }
    let trustByDefault = false;
    if (settingRegistry) {
        const loadSettings = settingRegistry.load(HTML_VIEWER_PLUGIN_ID);
        const updateSettings = (settings) => {
            trustByDefault = settings.get('trustByDefault').composite;
        };
        Promise.all([loadSettings, app.restored])
            .then(([settings]) => {
            updateSettings(settings);
            settings.changed.connect(settings => {
                updateSettings(settings);
            });
        })
            .catch((reason) => {
            console.error(reason.message);
        });
    }
    app.docRegistry.addWidgetFactory(factory);
    factory.widgetCreated.connect((sender, widget) => {
        var _a, _b;
        // Track the widget.
        void tracker.add(widget);
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        // Notify the application when the trust state changes so it
        // can update any renderings of the trust command.
        widget.trustedChanged.connect(() => {
            app.commands.notifyCommandChanged(CommandIDs.trustHTML);
        });
        widget.trusted = trustByDefault;
        widget.title.icon = ft.icon;
        widget.title.iconClass = (_a = ft.iconClass) !== null && _a !== void 0 ? _a : '';
        widget.title.iconLabel = (_b = ft.iconLabel) !== null && _b !== void 0 ? _b : '';
    });
    // Add a command to trust the active HTML document,
    // allowing script executions in its context.
    app.commands.addCommand(CommandIDs.trustHTML, {
        label: trans.__('Trust HTML File'),
        caption: trans.__(`Whether the HTML file is trusted.
    Trusting the file allows scripts to run in it,
    which may result in security risks.
    Only enable for files you trust.`),
        isEnabled: () => !!tracker.currentWidget,
        isToggled: () => {
            const current = tracker.currentWidget;
            if (!current) {
                return false;
            }
            const sandbox = current.content.sandbox;
            return sandbox.indexOf('allow-scripts') !== -1;
        },
        execute: () => {
            const current = tracker.currentWidget;
            if (!current) {
                return;
            }
            current.trusted = !current.trusted;
        }
    });
    if (palette) {
        palette.addItem({
            command: CommandIDs.trustHTML,
            category: trans.__('File Operations')
        });
    }
    return tracker;
}
/**
 * Export the plugins as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (htmlPlugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaHRtbHZpZXdlci1leHRlbnNpb25fbGliX2luZGV4X2pzLV84MjY5MC5jYzQ5ZDRhNGM4YmU5MWQ5ZjUxMC5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBTThCO0FBTUg7QUFPRTtBQUUrQjtBQUNUO0FBQ0E7QUFFdEQsTUFBTSxxQkFBcUIsR0FBRyx5Q0FBeUMsQ0FBQztBQUV4RTs7R0FFRztBQUNILE1BQU0sT0FBTyxHQUFHLGFBQWEsQ0FBQztBQUU5Qjs7R0FFRztBQUNILElBQVUsVUFBVSxDQUVuQjtBQUZELFdBQVUsVUFBVTtJQUNMLG9CQUFTLEdBQUcsdUJBQXVCLENBQUM7QUFDbkQsQ0FBQyxFQUZTLFVBQVUsS0FBVixVQUFVLFFBRW5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBOEM7SUFDNUQsUUFBUSxFQUFFLGtCQUFrQjtJQUM1QixFQUFFLEVBQUUscUJBQXFCO0lBQ3pCLFdBQVcsRUFBRSxpREFBaUQ7SUFDOUQsUUFBUSxFQUFFLHNFQUFrQjtJQUM1QixRQUFRLEVBQUUsQ0FBQyxnRUFBVyxDQUFDO0lBQ3ZCLFFBQVEsRUFBRTtRQUNSLGlFQUFlO1FBQ2Ysb0VBQWU7UUFDZix5RUFBZ0I7UUFDaEIsd0VBQXNCO0tBQ3ZCO0lBQ0QsU0FBUyxFQUFFLElBQUk7Q0FDaEIsQ0FBQztBQUVGOztHQUVHO0FBQ0gsU0FBUyxrQkFBa0IsQ0FDekIsR0FBb0IsRUFDcEIsVUFBdUIsRUFDdkIsT0FBK0IsRUFDL0IsUUFBZ0MsRUFDaEMsZUFBd0MsRUFDeEMsZUFBOEM7SUFFOUMsSUFBSSxjQUVTLENBQUM7SUFDZCxNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBRTVDLElBQUksZUFBZSxFQUFFO1FBQ25CLGVBQWUsQ0FBQyxVQUFVLENBQWEsT0FBTyxFQUFFLFNBQVMsRUFBRSxNQUFNLENBQUMsRUFBRSxDQUNs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QUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxhQUFhO1FBQ3hDLFNBQVMsRUFBRSxHQUFHLEVBQUU7WUFDZCxNQUFNLE9BQU8sR0FBRyxPQUFPLENBQUMsYUFBYSxDQUFDO1lBQ3RDLElBQUksQ0FBQyxPQUFPLEVBQUU7Z0JBQ1osT0FBTyxLQUFLLENBQUM7YUFDZDtZQUNELE1BQU0sT0FBTyxHQUFHLE9BQU8sQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDO1lBQ3hDLE9BQU8sT0FBTyxDQUFDLE9BQU8sQ0FBQyxlQUFlLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQztRQUNqRCxDQUFDO1FBQ0QsT0FBTyxFQUFFLEdBQUcsRUFBRTtZQUNaLE1BQU0sT0FBTyxHQUFHLE9BQU8sQ0FBQyxhQUFhLENBQUM7WUFDdEMsSUFBSSxDQUFDLE9BQU8sRUFBRTtnQkFDWixPQUFPO2FBQ1I7WUFDRCxPQUFPLENBQUMsT0FBTyxHQUFHLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQztRQUNyQyxDQUFDO0tBQ0YsQ0FBQyxDQUFDO0lBQ0gsSUFBSSxPQUFPLEVBQUU7UUFDWCxPQUFPLENBQUMsT0FBTyxDQUFDO1lBQ2QsT0FBTyxFQUFFLFVBQVUsQ0FBQyxTQUFTO1lBQzdCLFFBQVEsRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGlCQUFpQixDQUFDO1NBQ3RDLENBQUMsQ0FBQztLQUNKO0lBRUQsT0FBTyxPQUFPLENBQUM7QUFDakIsQ0FBQztBQUNEOztHQUVHO0FBQ0gsaUVBQWUsVUFBVSxFQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2h0bWx2aWV3ZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBodG1sdmlld2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYXlvdXRSZXN0b3JlcixcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgY3JlYXRlVG9vbGJhckZhY3RvcnksXG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgSVRvb2xiYXJXaWRnZXRSZWdpc3RyeSxcbiAgV2lkZ2V0VHJhY2tlclxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBEb2N1bWVudFJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jcmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgSFRNTFZpZXdlcixcbiAgSFRNTFZpZXdlckZhY3RvcnksXG4gIElIVE1MVmlld2VyVHJhY2tlcixcbiAgVG9vbGJhckl0ZW1zXG59IGZyb20gJ0BqdXB5dGVybGFiL2h0bWx2aWV3ZXInO1xuaW1wb3J0IHsgSU9ic2VydmFibGVMaXN0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvb2JzZXJ2YWJsZXMnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGh0bWw1SWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG5jb25zdCBIVE1MX1ZJRVdFUl9QTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvaHRtbHZpZXdlci1leHRlbnNpb246cGx1Z2luJztcblxuLyoqXG4gKiBGYWN0b3J5IG5hbWVcbiAqL1xuY29uc3QgRkFDVE9SWSA9ICdIVE1MIFZpZXdlcic7XG5cbi8qKlxuICogQ29tbWFuZCBJRHMgdXNlZCBieSB0aGUgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCB0cnVzdEhUTUwgPSAnaHRtbHZpZXdlcjp0cnVzdC1odG1sJztcbn1cblxuLyoqXG4gKiBUaGUgSFRNTCBmaWxlIGhhbmRsZXIgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBodG1sUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUhUTUxWaWV3ZXJUcmFja2VyPiA9IHtcbiAgYWN0aXZhdGU6IGFjdGl2YXRlSFRNTFZpZXdlcixcbiAgaWQ6IEhUTUxfVklFV0VSX1BMVUdJTl9JRCxcbiAgZGVzY3JpcHRpb246ICdBZGRzIEhUTUwgZmlsZSB2aWV3ZXIgYW5kIHByb3ZpZGVzIGl0cyB0cmFja2VyLicsXG4gIHByb3ZpZGVzOiBJSFRNTFZpZXdlclRyYWNrZXIsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW1xuICAgIElDb21tYW5kUGFsZXR0ZSxcbiAgICBJTGF5b3V0UmVzdG9yZXIsXG4gICAgSVNldHRpbmdSZWdpc3RyeSxcbiAgICBJVG9vbGJhcldpZGdldFJlZ2lzdHJ5XG4gIF0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUgSFRNTFZpZXdlciBleHRlbnNpb24uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlSFRNTFZpZXdlcihcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbCxcbiAgdG9vbGJhclJlZ2lzdHJ5OiBJVG9vbGJhcldpZGdldFJlZ2lzdHJ5IHwgbnVsbFxuKTogSUhUTUxWaWV3ZXJUcmFja2VyIHtcbiAgbGV0IHRvb2xiYXJGYWN0b3J5OlxuICAgIHwgKCh3aWRnZXQ6IEhUTUxWaWV3ZXIpID0+IElPYnNlcnZhYmxlTGlzdDxEb2N1bWVudFJlZ2lzdHJ5LklUb29sYmFySXRlbT4pXG4gICAgfCB1bmRlZmluZWQ7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgaWYgKHRvb2xiYXJSZWdpc3RyeSkge1xuICAgIHRvb2xiYXJSZWdpc3RyeS5hZGRGYWN0b3J5PEhUTUxWaWV3ZXI+KEZBQ1RPUlksICdyZWZyZXNoJywgd2lkZ2V0ID0+XG4gICAgICBUb29sYmFySXRlbXMuY3JlYXRlUmVmcmVzaEJ1dHRvbih3aWRnZXQsIHRyYW5zbGF0b3IpXG4gICAgKTtcbiAgICB0b29sYmFyUmVnaXN0cnkuYWRkRmFjdG9yeTxIVE1MVmlld2VyPihGQUNUT1JZLCAndHJ1c3QnLCB3aWRnZXQgPT5cbiAgICAgIFRvb2xiYXJJdGVtcy5jcmVhdGVUcnVzdEJ1dHRvbih3aWRnZXQsIHRyYW5zbGF0b3IpXG4gICAgKTtcblxuICAgIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICAgIHRvb2xiYXJGYWN0b3J5ID0gY3JlYXRlVG9vbGJhckZhY3RvcnkoXG4gICAgICAgIHRvb2xiYXJSZWdpc3RyeSxcbiAgICAgICAgc2V0dGluZ1JlZ2lzdHJ5LFxuICAgICAgICBGQUNUT1JZLFxuICAgICAgICBodG1sUGx1Z2luLmlkLFxuICAgICAgICB0cmFuc2xhdG9yXG4gICAgICApO1xuICAgIH1cbiAgfVxuXG4gIC8vIEFkZCBhbiBIVE1MIGZpbGUgdHlwZSB0byB0aGUgZG9jcmVnaXN0cnkuXG4gIGNvbnN0IGZ0OiBEb2N1bWVudFJlZ2lzdHJ5LklGaWxlVHlwZSA9IHtcbiAgICBuYW1lOiAnaHRtbCcsXG4gICAgY29udGVudFR5cGU6ICdmaWxlJyxcbiAgICBmaWxlRm9ybWF0OiAndGV4dCcsXG4gICAgZGlzcGxheU5hbWU6IHRyYW5zLl9fKCdIVE1MIEZpbGUnKSxcbiAgICBleHRlbnNpb25zOiBbJy5odG1sJ10sXG4gICAgbWltZVR5cGVzOiBbJ3RleHQvaHRtbCddLFxuICAgIGljb246IGh0bWw1SWNvblxuICB9O1xuICBhcHAuZG9jUmVnaXN0cnkuYWRkRmlsZVR5cGUoZnQpO1xuXG4gIC8vIENyZWF0ZSBhIG5ldyB2aWV3ZXIgZmFjdG9yeS5cbiAgY29uc3QgZmFjdG9yeSA9IG5ldyBIVE1MVmlld2VyRmFjdG9yeSh7XG4gICAgbmFtZTogRkFDVE9SWSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0hUTUwgVmlld2VyJyksXG4gICAgZmlsZVR5cGVzOiBbJ2h0bWwnXSxcbiAgICBkZWZhdWx0Rm9yOiBbJ2h0bWwnXSxcbiAgICByZWFkT25seTogdHJ1ZSxcbiAgICB0b29sYmFyRmFjdG9yeSxcbiAgICB0cmFuc2xhdG9yXG4gIH0pO1xuXG4gIC8vIENyZWF0ZSBhIHdpZGdldCB0cmFja2VyIGZvciBIVE1MIGRvY3VtZW50cy5cbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPEhUTUxWaWV3ZXI+KHtcbiAgICBuYW1lc3BhY2U6ICdodG1sdmlld2VyJ1xuICB9KTtcblxuICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICBjb21tYW5kOiAnZG9jbWFuYWdlcjpvcGVuJyxcbiAgICAgIGFyZ3M6IHdpZGdldCA9PiAoeyBwYXRoOiB3aWRnZXQuY29udGV4dC5wYXRoLCBmYWN0b3J5OiAnSFRNTCBWaWV3ZXInIH0pLFxuICAgICAgbmFtZTogd2lkZ2V0ID0+IHdpZGdldC5jb250ZXh0LnBhdGhcbiAgICB9KTtcbiAgfVxuXG4gIGxldCB0cnVzdEJ5RGVmYXVsdCA9IGZhbHNlO1xuXG4gIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICBjb25zdCBsb2FkU2V0dGluZ3MgPSBzZXR0aW5nUmVnaXN0cnkubG9hZChIVE1MX1ZJRVdFUl9QTFVHSU5fSUQpO1xuICAgIGNvbnN0IHVwZGF0ZVNldHRpbmdzID0gKHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyk6IHZvaWQgPT4ge1xuICAgICAgdHJ1c3RCeURlZmF1bHQgPSBzZXR0aW5ncy5nZXQoJ3RydXN0QnlEZWZhdWx0JykuY29tcG9zaXRlIGFzIGJvb2xlYW47XG4gICAgfTtcblxuICAgIFByb21pc2UuYWxsKFtsb2FkU2V0dGluZ3MsIGFwcC5yZXN0b3JlZF0pXG4gICAgICAudGhlbigoW3NldHRpbmdzXSkgPT4ge1xuICAgICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdChzZXR0aW5ncyA9PiB7XG4gICAgICAgICAgdXBkYXRlU2V0dGluZ3Moc2V0dGluZ3MpO1xuICAgICAgICB9KTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgICB9KTtcbiAgfVxuXG4gIGFwcC5kb2NSZWdpc3RyeS5hZGRXaWRnZXRGYWN0b3J5KGZhY3RvcnkpO1xuICBmYWN0b3J5LndpZGdldENyZWF0ZWQuY29ubmVjdCgoc2VuZGVyLCB3aWRnZXQpID0+IHtcbiAgICAvLyBUcmFjayB0aGUgd2lkZ2V0LlxuICAgIHZvaWQgdHJhY2tlci5hZGQod2lkZ2V0KTtcbiAgICAvLyBOb3RpZnkgdGhlIHdpZGdldCB0cmFja2VyIGlmIHJlc3RvcmUgZGF0YSBuZWVkcyB0byB1cGRhdGUuXG4gICAgd2lkZ2V0LmNvbnRleHQucGF0aENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB2b2lkIHRyYWNrZXIuc2F2ZSh3aWRnZXQpO1xuICAgIH0pO1xuICAgIC8vIE5vdGlmeSB0aGUgYXBwbGljYXRpb24gd2hlbiB0aGUgdHJ1c3Qgc3RhdGUgY2hhbmdlcyBzbyBpdFxuICAgIC8vIGNhbiB1cGRhdGUgYW55IHJlbmRlcmluZ3Mgb2YgdGhlIHRydXN0IGNvbW1hbmQuXG4gICAgd2lkZ2V0LnRydXN0ZWRDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMudHJ1c3RIVE1MKTtcbiAgICB9KTtcblxuICAgIHdpZGdldC50cnVzdGVkID0gdHJ1c3RCeURlZmF1bHQ7XG5cbiAgICB3aWRnZXQudGl0bGUuaWNvbiA9IGZ0Lmljb24hO1xuICAgIHdpZGdldC50aXRsZS5pY29uQ2xhc3MgPSBmdC5pY29uQ2xhc3MgPz8gJyc7XG4gICAgd2lkZ2V0LnRpdGxlLmljb25MYWJlbCA9IGZ0Lmljb25MYWJlbCA/PyAnJztcbiAgfSk7XG5cbiAgLy8gQWRkIGEgY29tbWFuZCB0byB0cnVzdCB0aGUgYWN0aXZlIEhUTUwgZG9jdW1lbnQsXG4gIC8vIGFsbG93aW5nIHNjcmlwdCBleGVjdXRpb25zIGluIGl0cyBjb250ZXh0LlxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRydXN0SFRNTCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnVHJ1c3QgSFRNTCBGaWxlJyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oYFdoZXRoZXIgdGhlIEhUTUwgZmlsZSBpcyB0cnVzdGVkLlxuICAgIFRydXN0aW5nIHRoZSBmaWxlIGFsbG93cyBzY3JpcHRzIHRvIHJ1biBpbiBpdCxcbiAgICB3aGljaCBtYXkgcmVzdWx0IGluIHNlY3VyaXR5IHJpc2tzLlxuICAgIE9ubHkgZW5hYmxlIGZvciBmaWxlcyB5b3UgdHJ1c3QuYCksXG4gICAgaXNFbmFibGVkOiAoKSA9PiAhIXRyYWNrZXIuY3VycmVudFdpZGdldCxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgY29uc3Qgc2FuZGJveCA9IGN1cnJlbnQuY29udGVudC5zYW5kYm94O1xuICAgICAgcmV0dXJuIHNhbmRib3guaW5kZXhPZignYWxsb3ctc2NyaXB0cycpICE9PSAtMTtcbiAgICB9LFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IGN1cnJlbnQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgICBpZiAoIWN1cnJlbnQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY3VycmVudC50cnVzdGVkID0gIWN1cnJlbnQudHJ1c3RlZDtcbiAgICB9XG4gIH0pO1xuICBpZiAocGFsZXR0ZSkge1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLnRydXN0SFRNTCxcbiAgICAgIGNhdGVnb3J5OiB0cmFucy5fXygnRmlsZSBPcGVyYXRpb25zJylcbiAgICB9KTtcbiAgfVxuXG4gIHJldHVybiB0cmFja2VyO1xufVxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgZGVmYXVsdC5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgaHRtbFBsdWdpbjtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==