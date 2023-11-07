"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_markdownviewer-extension_lib_index_js-_83a21"],{

/***/ "../packages/markdownviewer-extension/lib/index.js":
/*!*********************************************************!*\
  !*** ../packages/markdownviewer-extension/lib/index.js ***!
  \*********************************************************/
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
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/markdownviewer */ "webpack/sharing/consume/default/@jupyterlab/markdownviewer/@jupyterlab/markdownviewer");
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module markdownviewer-extension
 */








/**
 * The command IDs used by the markdownviewer plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.markdownPreview = 'markdownviewer:open';
    CommandIDs.markdownEditor = 'markdownviewer:edit';
})(CommandIDs || (CommandIDs = {}));
/**
 * The name of the factory that creates markdown viewer widgets.
 */
const FACTORY = 'Markdown Preview';
/**
 * The markdown viewer plugin.
 */
const plugin = {
    activate,
    id: '@jupyterlab/markdownviewer-extension:plugin',
    description: 'Adds markdown file viewer and provides its tracker.',
    provides: _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.IMarkdownViewerTracker,
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_5__.ISettingRegistry, _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_6__.ITableOfContentsRegistry],
    autoStart: true
};
/**
 * Activate the markdown viewer plugin.
 */
function activate(app, rendermime, translator, restorer, settingRegistry, tocRegistry) {
    const trans = translator.load('jupyterlab');
    const { commands, docRegistry } = app;
    // Add the markdown renderer factory.
    rendermime.addFactory(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.markdownRendererFactory);
    const namespace = 'markdownviewer-widget';
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    let config = {
        ..._jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.MarkdownViewer.defaultConfig
    };
    /**
     * Update the settings of a widget.
     */
    function updateWidget(widget) {
        Object.keys(config).forEach((k) => {
            var _a;
            widget.setOption(k, (_a = config[k]) !== null && _a !== void 0 ? _a : null);
        });
    }
    if (settingRegistry) {
        const updateSettings = (settings) => {
            config = settings.composite;
            tracker.forEach(widget => {
                updateWidget(widget.content);
            });
        };
        // Fetch the initial state of the settings.
        settingRegistry
            .load(plugin.id)
            .then((settings) => {
            settings.changed.connect(() => {
                updateSettings(settings);
            });
            updateSettings(settings);
        })
            .catch((reason) => {
            console.error(reason.message);
        });
    }
    // Register the MarkdownViewer factory.
    const factory = new _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.MarkdownViewerFactory({
        rendermime,
        name: FACTORY,
        label: trans.__('Markdown Preview'),
        primaryFileType: docRegistry.getFileType('markdown'),
        fileTypes: ['markdown'],
        defaultRendered: ['markdown']
    });
    factory.widgetCreated.connect((sender, widget) => {
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        // Handle the settings of new widgets.
        updateWidget(widget.content);
        void tracker.add(widget);
    });
    docRegistry.addWidgetFactory(factory);
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({ path: widget.context.path, factory: FACTORY }),
            name: widget => widget.context.path
        });
    }
    commands.addCommand(CommandIDs.markdownPreview, {
        label: trans.__('Markdown Preview'),
        execute: args => {
            const path = args['path'];
            if (typeof path !== 'string') {
                return;
            }
            return commands.execute('docmanager:open', {
                path,
                factory: FACTORY,
                options: args['options']
            });
        }
    });
    commands.addCommand(CommandIDs.markdownEditor, {
        execute: () => {
            const widget = tracker.currentWidget;
            if (!widget) {
                return;
            }
            const path = widget.context.path;
            return commands.execute('docmanager:open', {
                path,
                factory: 'Editor',
                options: {
                    mode: 'split-right'
                }
            });
        },
        isVisible: () => {
            const widget = tracker.currentWidget;
            return ((widget && _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PathExt.extname(widget.context.path) === '.md') || false);
        },
        label: trans.__('Show Markdown Editor')
    });
    if (tocRegistry) {
        tocRegistry.add(new _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_3__.MarkdownViewerTableOfContentsFactory(tracker, rendermime.markdownParser));
    }
    return tracker;
}
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWFya2Rvd252aWV3ZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fODNhMjEuYTA5MTNjMDBiOTI5OTdlZGJiNDUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU04QjtBQUNvQjtBQUNMO0FBT1o7QUFJSjtBQUMrQjtBQUNKO0FBQ0w7QUFFdEQ7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FHbkI7QUFIRCxXQUFVLFVBQVU7SUFDTCwwQkFBZSxHQUFHLHFCQUFxQixDQUFDO0lBQ3hDLHlCQUFjLEdBQUcscUJBQXFCLENBQUM7QUFDdEQsQ0FBQyxFQUhTLFVBQVUsS0FBVixVQUFVLFFBR25CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE9BQU8sR0FBRyxrQkFBa0IsQ0FBQztBQUVuQzs7R0FFRztBQUNILE1BQU0sTUFBTSxHQUFrRDtJQUM1RCxRQUFRO0lBQ1IsRUFBRSxFQUFFLDZDQUE2QztJQUNqRCxXQUFXLEVBQUUscURBQXFEO0lBQ2xFLFFBQVEsRUFBRSw4RUFBc0I7SUFDaEMsUUFBUSxFQUFFLENBQUMsdUVBQW1CLEVBQUUsZ0VBQVcsQ0FBQztJQUM1QyxRQUFRLEVBQUUsQ0FBQyxvRUFBZSxFQUFFLHlFQUFnQixFQUFFLHFFQUF3QixDQUFDO0lBQ3ZFLFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7R0FFRztBQUNILFNBQVMsUUFBUSxDQUNmLEdBQW9CLEVBQ3BCLFVBQStCLEVBQy9CLFVBQXVCLEVBQ3ZCLFFBQWdDLEVBQ2hDLGVBQXdDLEVBQ3hDLFdBQTRDO0lBRTVDLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7SUFDNUMsTUFBTSxFQUFFLFFBQVEsRUFBRSxXQUFXLEVBQUUsR0FBRyxHQUFHLENBQUM7SUFFdEMscUNBQXFDO0lBQ3JDLFVBQVUsQ0FBQyxVQUFVLENBQUMsMkVBQXVC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LElBQUksQ0FBQyxLQUFLLEtBQUssQ0FBQyxJQUFJLEtBQUssQ0FDcEUsQ0FBQztRQUNKLENBQUM7UUFDRCxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxzQkFBc0IsQ0FBQztLQUN4QyxDQUFDLENBQUM7SUFFSCxJQUFJLFdBQVcsRUFBRTtRQUNmLFdBQVcsQ0FBQyxHQUFHLENBQ2IsSUFBSSw0RkFBb0MsQ0FDdEMsT0FBTyxFQUNQLFVBQVUsQ0FBQyxjQUFjLENBQzFCLENBQ0YsQ0FBQztLQUNIO0lBRUQsT0FBTyxPQUFPLENBQUM7QUFDakIsQ0FBQztBQUVEOztHQUVHO0FBQ0gsaUVBQWUsTUFBTSxFQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21hcmtkb3dudmlld2VyLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWFya2Rvd252aWV3ZXItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBXaWRnZXRUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgUGF0aEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBJTWFya2Rvd25WaWV3ZXJUcmFja2VyLFxuICBNYXJrZG93bkRvY3VtZW50LFxuICBNYXJrZG93blZpZXdlcixcbiAgTWFya2Rvd25WaWV3ZXJGYWN0b3J5LFxuICBNYXJrZG93blZpZXdlclRhYmxlT2ZDb250ZW50c0ZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvbWFya2Rvd252aWV3ZXInO1xuaW1wb3J0IHtcbiAgSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgbWFya2Rvd25SZW5kZXJlckZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUYWJsZU9mQ29udGVudHNSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3RvYyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgbWFya2Rvd252aWV3ZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBtYXJrZG93blByZXZpZXcgPSAnbWFya2Rvd252aWV3ZXI6b3Blbic7XG4gIGV4cG9ydCBjb25zdCBtYXJrZG93bkVkaXRvciA9ICdtYXJrZG93bnZpZXdlcjplZGl0Jztcbn1cblxuLyoqXG4gKiBUaGUgbmFtZSBvZiB0aGUgZmFjdG9yeSB0aGF0IGNyZWF0ZXMgbWFya2Rvd24gdmlld2VyIHdpZGdldHMuXG4gKi9cbmNvbnN0IEZBQ1RPUlkgPSAnTWFya2Rvd24gUHJldmlldyc7XG5cbi8qKlxuICogVGhlIG1hcmtkb3duIHZpZXdlciBwbHVnaW4uXG4gKi9cbmNvbnN0IHBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElNYXJrZG93blZpZXdlclRyYWNrZXI+ID0ge1xuICBhY3RpdmF0ZSxcbiAgaWQ6ICdAanVweXRlcmxhYi9tYXJrZG93bnZpZXdlci1leHRlbnNpb246cGx1Z2luJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIG1hcmtkb3duIGZpbGUgdmlld2VyIGFuZCBwcm92aWRlcyBpdHMgdHJhY2tlci4nLFxuICBwcm92aWRlczogSU1hcmtkb3duVmlld2VyVHJhY2tlcixcbiAgcmVxdWlyZXM6IFtJUmVuZGVyTWltZVJlZ2lzdHJ5LCBJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxheW91dFJlc3RvcmVyLCBJU2V0dGluZ1JlZ2lzdHJ5LCBJVGFibGVPZkNvbnRlbnRzUmVnaXN0cnldLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogQWN0aXZhdGUgdGhlIG1hcmtkb3duIHZpZXdlciBwbHVnaW4uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsLFxuICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsLFxuICB0b2NSZWdpc3RyeTogSVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5IHwgbnVsbFxuKTogSU1hcmtkb3duVmlld2VyVHJhY2tlciB7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IHsgY29tbWFuZHMsIGRvY1JlZ2lzdHJ5IH0gPSBhcHA7XG5cbiAgLy8gQWRkIHRoZSBtYXJrZG93biByZW5kZXJlciBmYWN0b3J5LlxuICByZW5kZXJtaW1lLmFkZEZhY3RvcnkobWFya2Rvd25SZW5kZXJlckZhY3RvcnkpO1xuXG4gIGNvbnN0IG5hbWVzcGFjZSA9ICdtYXJrZG93bnZpZXdlci13aWRnZXQnO1xuICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFya2Rvd25Eb2N1bWVudD4oe1xuICAgIG5hbWVzcGFjZVxuICB9KTtcblxuICBsZXQgY29uZmlnOiBQYXJ0aWFsPE1hcmtkb3duVmlld2VyLklDb25maWc+ID0ge1xuICAgIC4uLk1hcmtkb3duVmlld2VyLmRlZmF1bHRDb25maWdcbiAgfTtcblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBzZXR0aW5ncyBvZiBhIHdpZGdldC5cbiAgICovXG4gIGZ1bmN0aW9uIHVwZGF0ZVdpZGdldCh3aWRnZXQ6IE1hcmtkb3duVmlld2VyKTogdm9pZCB7XG4gICAgT2JqZWN0LmtleXMoY29uZmlnKS5mb3JFYWNoKChrOiBrZXlvZiBNYXJrZG93blZpZXdlci5JQ29uZmlnKSA9PiB7XG4gICAgICB3aWRnZXQuc2V0T3B0aW9uKGssIGNvbmZpZ1trXSA/PyBudWxsKTtcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICBjb25zdCB1cGRhdGVTZXR0aW5ncyA9IChzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpID0+IHtcbiAgICAgIGNvbmZpZyA9IHNldHRpbmdzLmNvbXBvc2l0ZSBhcyBQYXJ0aWFsPE1hcmtkb3duVmlld2VyLklDb25maWc+O1xuICAgICAgdHJhY2tlci5mb3JFYWNoKHdpZGdldCA9PiB7XG4gICAgICAgIHVwZGF0ZVdpZGdldCh3aWRnZXQuY29udGVudCk7XG4gICAgICB9KTtcbiAgICB9O1xuXG4gICAgLy8gRmV0Y2ggdGhlIGluaXRpYWwgc3RhdGUgb2YgdGhlIHNldHRpbmdzLlxuICAgIHNldHRpbmdSZWdpc3RyeVxuICAgICAgLmxvYWQocGx1Z2luLmlkKVxuICAgICAgLnRoZW4oKHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncykgPT4ge1xuICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgfSk7XG4gICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgICB9KTtcbiAgfVxuXG4gIC8vIFJlZ2lzdGVyIHRoZSBNYXJrZG93blZpZXdlciBmYWN0b3J5LlxuICBjb25zdCBmYWN0b3J5ID0gbmV3IE1hcmtkb3duVmlld2VyRmFjdG9yeSh7XG4gICAgcmVuZGVybWltZSxcbiAgICBuYW1lOiBGQUNUT1JZLFxuICAgIGxhYmVsOiB0cmFucy5fXygnTWFya2Rvd24gUHJldmlldycpLFxuICAgIHByaW1hcnlGaWxlVHlwZTogZG9jUmVnaXN0cnkuZ2V0RmlsZVR5cGUoJ21hcmtkb3duJyksXG4gICAgZmlsZVR5cGVzOiBbJ21hcmtkb3duJ10sXG4gICAgZGVmYXVsdFJlbmRlcmVkOiBbJ21hcmtkb3duJ11cbiAgfSk7XG4gIGZhY3Rvcnkud2lkZ2V0Q3JlYXRlZC5jb25uZWN0KChzZW5kZXIsIHdpZGdldCkgPT4ge1xuICAgIC8vIE5vdGlmeSB0aGUgd2lkZ2V0IHRyYWNrZXIgaWYgcmVzdG9yZSBkYXRhIG5lZWRzIHRvIHVwZGF0ZS5cbiAgICB3aWRnZXQuY29udGV4dC5wYXRoQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgIHZvaWQgdHJhY2tlci5zYXZlKHdpZGdldCk7XG4gICAgfSk7XG4gICAgLy8gSGFuZGxlIHRoZSBzZXR0aW5ncyBvZiBuZXcgd2lkZ2V0cy5cbiAgICB1cGRhdGVXaWRnZXQod2lkZ2V0LmNvbnRlbnQpO1xuICAgIHZvaWQgdHJhY2tlci5hZGQod2lkZ2V0KTtcbiAgfSk7XG4gIGRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG5cbiAgLy8gSGFuZGxlIHN0YXRlIHJlc3RvcmF0aW9uLlxuICBpZiAocmVzdG9yZXIpIHtcbiAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgY29tbWFuZDogJ2RvY21hbmFnZXI6b3BlbicsXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHsgcGF0aDogd2lkZ2V0LmNvbnRleHQucGF0aCwgZmFjdG9yeTogRkFDVE9SWSB9KSxcbiAgICAgIG5hbWU6IHdpZGdldCA9PiB3aWRnZXQuY29udGV4dC5wYXRoXG4gICAgfSk7XG4gIH1cblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubWFya2Rvd25QcmV2aWV3LCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdNYXJrZG93biBQcmV2aWV3JyksXG4gICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICBjb25zdCBwYXRoID0gYXJnc1sncGF0aCddO1xuICAgICAgaWYgKHR5cGVvZiBwYXRoICE9PSAnc3RyaW5nJykge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuJywge1xuICAgICAgICBwYXRoLFxuICAgICAgICBmYWN0b3J5OiBGQUNUT1JZLFxuICAgICAgICBvcHRpb25zOiBhcmdzWydvcHRpb25zJ11cbiAgICAgIH0pO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm1hcmtkb3duRWRpdG9yLCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgY29uc3QgcGF0aCA9IHdpZGdldC5jb250ZXh0LnBhdGg7XG4gICAgICByZXR1cm4gY29tbWFuZHMuZXhlY3V0ZSgnZG9jbWFuYWdlcjpvcGVuJywge1xuICAgICAgICBwYXRoLFxuICAgICAgICBmYWN0b3J5OiAnRWRpdG9yJyxcbiAgICAgICAgb3B0aW9uczoge1xuICAgICAgICAgIG1vZGU6ICdzcGxpdC1yaWdodCdcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfSxcbiAgICBpc1Zpc2libGU6ICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICAgIHJldHVybiAoXG4gICAgICAgICh3aWRnZXQgJiYgUGF0aEV4dC5leHRuYW1lKHdpZGdldC5jb250ZXh0LnBhdGgpID09PSAnLm1kJykgfHwgZmFsc2VcbiAgICAgICk7XG4gICAgfSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgTWFya2Rvd24gRWRpdG9yJylcbiAgfSk7XG5cbiAgaWYgKHRvY1JlZ2lzdHJ5KSB7XG4gICAgdG9jUmVnaXN0cnkuYWRkKFxuICAgICAgbmV3IE1hcmtkb3duVmlld2VyVGFibGVPZkNvbnRlbnRzRmFjdG9yeShcbiAgICAgICAgdHJhY2tlcixcbiAgICAgICAgcmVuZGVybWltZS5tYXJrZG93blBhcnNlclxuICAgICAgKVxuICAgICk7XG4gIH1cblxuICByZXR1cm4gdHJhY2tlcjtcbn1cblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbiBhcyBkZWZhdWx0LlxuICovXG5leHBvcnQgZGVmYXVsdCBwbHVnaW47XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=