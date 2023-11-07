"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_inspector-extension_lib_index_js"],{

/***/ "../packages/inspector-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/inspector-extension/lib/index.js ***!
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
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/inspector */ "webpack/sharing/consume/default/@jupyterlab/inspector/@jupyterlab/inspector");
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module inspector-extension
 */








/**
 * The command IDs used by the inspector plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'inspector:open';
    CommandIDs.close = 'inspector:close';
    CommandIDs.toggle = 'inspector:toggle';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing code introspection.
 */
const inspector = {
    id: '@jupyterlab/inspector-extension:inspector',
    description: 'Provides the code introspection widget.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector,
    autoStart: true,
    activate: (app, translator, palette, launcher, restorer) => {
        const trans = translator.load('jupyterlab');
        const { commands, shell } = app;
        const caption = trans.__('Live updating code documentation from the active kernel');
        const openedLabel = trans.__('Contextual Help');
        const namespace = 'inspector';
        const datasetKey = 'jpInspector';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace
        });
        function isInspectorOpen() {
            return inspector && !inspector.isDisposed;
        }
        let source = null;
        let inspector;
        function openInspector(args) {
            var _a;
            if (!isInspectorOpen()) {
                inspector = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                    content: new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectorPanel({ translator })
                });
                inspector.id = 'jp-inspector';
                inspector.title.label = openedLabel;
                inspector.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon;
                void tracker.add(inspector);
                source = source && !source.isDisposed ? source : null;
                inspector.content.source = source;
                (_a = inspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(args);
            }
            if (!inspector.isAttached) {
                shell.add(inspector, 'main', {
                    activate: false,
                    mode: 'split-right',
                    type: 'Inspector'
                });
            }
            shell.activateById(inspector.id);
            document.body.dataset[datasetKey] = 'open';
            return inspector;
        }
        function closeInspector() {
            inspector.dispose();
            delete document.body.dataset[datasetKey];
        }
        // Add inspector:open command to registry.
        const showLabel = trans.__('Show Contextual Help');
        commands.addCommand(CommandIDs.open, {
            caption,
            isEnabled: () => !inspector ||
                inspector.isDisposed ||
                !inspector.isAttached ||
                !inspector.isVisible,
            label: showLabel,
            icon: args => (args.isLauncher ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon : undefined),
            execute: args => {
                var _a;
                const text = args && args.text;
                const refresh = args && args.refresh;
                // if inspector is open, see if we need a refresh
                if (isInspectorOpen() && refresh)
                    (_a = inspector.content.source) === null || _a === void 0 ? void 0 : _a.onEditorChange(text);
                else
                    openInspector(text);
            }
        });
        // Add inspector:close command to registry.
        const closeLabel = trans.__('Hide Contextual Help');
        commands.addCommand(CommandIDs.close, {
            caption,
            isEnabled: () => isInspectorOpen(),
            label: closeLabel,
            icon: args => (args.isLauncher ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_7__.inspectorIcon : undefined),
            execute: () => closeInspector()
        });
        // Add inspector:toggle command to registry.
        const toggleLabel = trans.__('Show Contextual Help');
        commands.addCommand(CommandIDs.toggle, {
            caption,
            label: toggleLabel,
            isToggled: () => isInspectorOpen(),
            execute: args => {
                if (isInspectorOpen()) {
                    closeInspector();
                }
                else {
                    const text = args && args.text;
                    openInspector(text);
                }
            }
        });
        // Add open command to launcher if possible.
        if (launcher) {
            launcher.add({ command: CommandIDs.open, args: { isLauncher: true } });
        }
        // Add toggle command to command palette if possible.
        if (palette) {
            palette.addItem({ command: CommandIDs.toggle, category: toggleLabel });
        }
        // Handle state restoration.
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.toggle,
                name: () => 'inspector'
            });
        }
        // Create a proxy to pass the `source` to the current inspector.
        const proxy = Object.defineProperty({}, 'source', {
            get: () => !inspector || inspector.isDisposed ? null : inspector.content.source,
            set: (src) => {
                source = src && !src.isDisposed ? src : null;
                if (inspector && !inspector.isDisposed) {
                    inspector.content.source = source;
                }
            }
        });
        return proxy;
    }
};
/**
 * An extension that registers consoles for inspection.
 */
const consoles = {
    // FIXME This should be in @jupyterlab/console-extension
    id: '@jupyterlab/inspector-extension:consoles',
    description: 'Adds code introspection support to consoles.',
    requires: [_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, consoles, labShell, translator) => {
        // Maintain association of new consoles with their respective handlers.
        const handlers = {};
        // Create a handler for each console that is created.
        consoles.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.console.sessionContext;
            const rendermime = parent.console.rendermime;
            const connector = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.KernelConnector({ sessionContext });
            const handler = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.console.promptCell;
            handler.editor = cell && cell.editor;
            // Listen for prompt creation.
            parent.console.promptCellCreated.connect((sender, cell) => {
                handler.editor = cell && cell.editor;
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of console instances and set inspector source.
        const setSource = (widget) => {
            if (widget && consoles.has(widget) && handlers[widget.id]) {
                manager.source = handlers[widget.id];
            }
        };
        labShell.currentChanged.connect((_, args) => setSource(args.newValue));
        void app.restored.then(() => setSource(labShell.currentWidget));
    }
};
/**
 * An extension that registers notebooks for inspection.
 */
const notebooks = {
    // FIXME This should be in @jupyterlab/notebook-extension
    id: '@jupyterlab/inspector-extension:notebooks',
    description: 'Adds code introspection to notebooks.',
    requires: [_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.IInspector, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_5__.INotebookTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    autoStart: true,
    activate: (app, manager, notebooks, labShell) => {
        // Maintain association of new notebooks with their respective handlers.
        const handlers = {};
        // Create a handler for each notebook that is created.
        notebooks.widgetAdded.connect((sender, parent) => {
            const sessionContext = parent.sessionContext;
            const rendermime = parent.content.rendermime;
            const connector = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.KernelConnector({ sessionContext });
            const handler = new _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_3__.InspectionHandler({ connector, rendermime });
            // Associate the handler to the widget.
            handlers[parent.id] = handler;
            // Set the initial editor.
            const cell = parent.content.activeCell;
            handler.editor = cell && cell.editor;
            // Listen for active cell changes.
            parent.content.activeCellChanged.connect((sender, cell) => {
                void (cell === null || cell === void 0 ? void 0 : cell.ready.then(() => {
                    if (cell === parent.content.activeCell) {
                        handler.editor = cell.editor;
                    }
                }));
            });
            // Listen for parent disposal.
            parent.disposed.connect(() => {
                delete handlers[parent.id];
                handler.dispose();
            });
        });
        // Keep track of notebook instances and set inspector source.
        const setSource = (widget) => {
            if (widget && notebooks.has(widget) && handlers[widget.id]) {
                manager.source = handlers[widget.id];
            }
        };
        labShell.currentChanged.connect((_, args) => setSource(args.newValue));
        void app.restored.then(() => setSource(labShell.currentWidget));
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [inspector, consoles, notebooks];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaW5zcGVjdG9yLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuOGM3YjQzMzQyNWMzY2Y2NDNlZWEuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU84QjtBQUtIO0FBQ3dCO0FBTXZCO0FBQ2tCO0FBQ087QUFDRjtBQUNJO0FBRzFEOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBSW5CO0FBSkQsV0FBVSxVQUFVO0lBQ0wsZUFBSSxHQUFHLGdCQUFnQixDQUFDO0lBQ3hCLGdCQUFLLEdBQUcsaUJBQWlCLENBQUM7SUFDMUIsaUJBQU0sR0FBRyxrQkFBa0IsQ0FBQztBQUMzQyxDQUFDLEVBSlMsVUFBVSxLQUFWLFVBQVUsUUFJbkI7QUFFRDs7R0FFRztBQUNILE1BQU0sU0FBUyxHQUFzQztJQUNuRCxFQUFFLEVBQUUsMkNBQTJDO0lBQy9DLFdBQVcsRUFBRSx5Q0FBeUM7SUFDdEQsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUUsQ0FBQyxpRUFBZSxFQUFFLDJEQUFTLEVBQUUsb0VBQWUsQ0FBQztJQUN2RCxRQUFRLEVBQUUsNkRBQVU7SUFDcEIsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixVQUF1QixFQUN2QixPQUErQixFQUMvQixRQUEwQixFQUMxQixRQUFnQyxFQUNwQixFQUFFO1FBQ2QsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxNQUFNLEVBQUUsUUFBUSxFQUFFLEtBQUssRUFBRSxHQUFHLEdBQUcsQ0FBQztRQUNoQyxNQUFNLE9BQU8sR0FBRyxLQUFLLENBQUMsRUFBRSxDQUN0Qix5REFBeUQsQ0FDMUQsQ0FBQztRQUNGLE1BQU0sV0FBVyxHQUFHLEtBQUssQ0FBQyxFQUFFLENBQUMsaUJBQWlCLENBQUMsQ0FBQztRQUNo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RTtnQkFDM0IsT0FBTyxRQUFRLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FBQyxDQUFDO2dCQUMzQixPQUFPLENBQUMsT0FBTyxFQUFFLENBQUM7WUFDcEIsQ0FBQyxDQUFDLENBQUM7UUFDTCxDQUFDLENBQUMsQ0FBQztRQUVILDZEQUE2RDtRQUM3RCxNQUFNLFNBQVMsR0FBRyxDQUFDLE1BQXFCLEVBQVEsRUFBRTtZQUNoRCxJQUFJLE1BQU0sSUFBSSxTQUFTLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxJQUFJLFFBQVEsQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLEVBQUU7Z0JBQzFELE9BQU8sQ0FBQyxNQUFNLEdBQUcsUUFBUSxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsQ0FBQzthQUN0QztRQUNILENBQUMsQ0FBQztRQUNGLFFBQVEsQ0FBQyxjQUFjLENBQUMsT0FBTyxDQUFDLENBQUMsQ0FBQyxFQUFFLElBQUksRUFBRSxFQUFFLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsQ0FBQyxDQUFDO1FBQ3ZFLEtBQUssR0FBRyxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsR0FBRyxFQUFFLENBQUMsU0FBUyxDQUFDLFFBQVEsQ0FBQyxhQUFhLENBQUMsQ0FBQyxDQUFDO0lBQ2xFLENBQUM7Q0FDRixDQUFDO0FBRUY7O0dBRUc7QUFDSCxNQUFNLE9BQU8sR0FBaUMsQ0FBQyxTQUFTLEVBQUUsUUFBUSxFQUFFLFNBQVMsQ0FBQyxDQUFDO0FBQy9FLGlFQUFlLE9BQU8sRUFBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9pbnNwZWN0b3ItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBpbnNwZWN0b3ItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIElDb21tYW5kUGFsZXR0ZSxcbiAgTWFpbkFyZWFXaWRnZXQsXG4gIFdpZGdldFRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSUNvbnNvbGVUcmFja2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29uc29sZSc7XG5pbXBvcnQge1xuICBJSW5zcGVjdG9yLFxuICBJbnNwZWN0aW9uSGFuZGxlcixcbiAgSW5zcGVjdG9yUGFuZWwsXG4gIEtlcm5lbENvbm5lY3RvclxufSBmcm9tICdAanVweXRlcmxhYi9pbnNwZWN0b3InO1xuaW1wb3J0IHsgSUxhdW5jaGVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbGF1bmNoZXInO1xuaW1wb3J0IHsgSU5vdGVib29rVHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgaW5zcGVjdG9ySWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgaW5zcGVjdG9yIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdpbnNwZWN0b3I6b3Blbic7XG4gIGV4cG9ydCBjb25zdCBjbG9zZSA9ICdpbnNwZWN0b3I6Y2xvc2UnO1xuICBleHBvcnQgY29uc3QgdG9nZ2xlID0gJ2luc3BlY3Rvcjp0b2dnbGUnO1xufVxuXG4vKipcbiAqIEEgc2VydmljZSBwcm92aWRpbmcgY29kZSBpbnRyb3NwZWN0aW9uLlxuICovXG5jb25zdCBpbnNwZWN0b3I6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJSW5zcGVjdG9yPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9pbnNwZWN0b3ItZXh0ZW5zaW9uOmluc3BlY3RvcicsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGNvZGUgaW50cm9zcGVjdGlvbiB3aWRnZXQuJyxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlLCBJTGF1bmNoZXIsIElMYXlvdXRSZXN0b3Jlcl0sXG4gIHByb3ZpZGVzOiBJSW5zcGVjdG9yLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgICBsYXVuY2hlcjogSUxhdW5jaGVyIHwgbnVsbCxcbiAgICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbFxuICApOiBJSW5zcGVjdG9yID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsIH0gPSBhcHA7XG4gICAgY29uc3QgY2FwdGlvbiA9IHRyYW5zLl9fKFxuICAgICAgJ0xpdmUgdXBkYXRpbmcgY29kZSBkb2N1bWVudGF0aW9uIGZyb20gdGhlIGFjdGl2ZSBrZXJuZWwnXG4gICAgKTtcbiAgICBjb25zdCBvcGVuZWRMYWJlbCA9IHRyYW5zLl9fKCdDb250ZXh0dWFsIEhlbHAnKTtcbiAgICBjb25zdCBuYW1lc3BhY2UgPSAnaW5zcGVjdG9yJztcbiAgICBjb25zdCBkYXRhc2V0S2V5ID0gJ2pwSW5zcGVjdG9yJztcbiAgICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8SW5zcGVjdG9yUGFuZWw+Pih7XG4gICAgICBuYW1lc3BhY2VcbiAgICB9KTtcblxuICAgIGZ1bmN0aW9uIGlzSW5zcGVjdG9yT3BlbigpIHtcbiAgICAgIHJldHVybiBpbnNwZWN0b3IgJiYgIWluc3BlY3Rvci5pc0Rpc3Bvc2VkO1xuICAgIH1cblxuICAgIGxldCBzb3VyY2U6IElJbnNwZWN0b3IuSUluc3BlY3RhYmxlIHwgbnVsbCA9IG51bGw7XG4gICAgbGV0IGluc3BlY3RvcjogTWFpbkFyZWFXaWRnZXQ8SW5zcGVjdG9yUGFuZWw+O1xuICAgIGZ1bmN0aW9uIG9wZW5JbnNwZWN0b3IoYXJnczogc3RyaW5nKTogTWFpbkFyZWFXaWRnZXQ8SW5zcGVjdG9yUGFuZWw+IHtcbiAgICAgIGlmICghaXNJbnNwZWN0b3JPcGVuKCkpIHtcbiAgICAgICAgaW5zcGVjdG9yID0gbmV3IE1haW5BcmVhV2lkZ2V0KHtcbiAgICAgICAgICBjb250ZW50OiBuZXcgSW5zcGVjdG9yUGFuZWwoeyB0cmFuc2xhdG9yIH0pXG4gICAgICAgIH0pO1xuICAgICAgICBpbnNwZWN0b3IuaWQgPSAnanAtaW5zcGVjdG9yJztcbiAgICAgICAgaW5zcGVjdG9yLnRpdGxlLmxhYmVsID0gb3BlbmVkTGFiZWw7XG4gICAgICAgIGluc3BlY3Rvci50aXRsZS5pY29uID0gaW5zcGVjdG9ySWNvbjtcbiAgICAgICAgdm9pZCB0cmFja2VyLmFkZChpbnNwZWN0b3IpO1xuICAgICAgICBzb3VyY2UgPSBzb3VyY2UgJiYgIXNvdXJjZS5pc0Rpc3Bvc2VkID8gc291cmNlIDogbnVsbDtcbiAgICAgICAgaW5zcGVjdG9yLmNvbnRlbnQuc291cmNlID0gc291cmNlO1xuICAgICAgICBpbnNwZWN0b3IuY29udGVudC5zb3VyY2U/Lm9uRWRpdG9yQ2hhbmdlKGFyZ3MpO1xuICAgICAgfVxuICAgICAgaWYgKCFpbnNwZWN0b3IuaXNBdHRhY2hlZCkge1xuICAgICAgICBzaGVsbC5hZGQoaW5zcGVjdG9yLCAnbWFpbicsIHtcbiAgICAgICAgICBhY3RpdmF0ZTogZmFsc2UsXG4gICAgICAgICAgbW9kZTogJ3NwbGl0LXJpZ2h0JyxcbiAgICAgICAgICB0eXBlOiAnSW5zcGVjdG9yJ1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICAgIHNoZWxsLmFjdGl2YXRlQnlJZChpbnNwZWN0b3IuaWQpO1xuICAgICAgZG9jdW1lbnQuYm9keS5kYXRhc2V0W2RhdGFzZXRLZXldID0gJ29wZW4nO1xuICAgICAgcmV0dXJuIGluc3BlY3RvcjtcbiAgICB9XG4gICAgZnVuY3Rpb24gY2xvc2VJbnNwZWN0b3IoKTogdm9pZCB7XG4gICAgICBpbnNwZWN0b3IuZGlzcG9zZSgpO1xuICAgICAgZGVsZXRlIGRvY3VtZW50LmJvZHkuZGF0YXNldFtkYXRhc2V0S2V5XTtcbiAgICB9XG5cbiAgICAvLyBBZGQgaW5zcGVjdG9yOm9wZW4gY29tbWFuZCB0byByZWdpc3RyeS5cbiAgICBjb25zdCBzaG93TGFiZWwgPSB0cmFucy5fXygnU2hvdyBDb250ZXh0dWFsIEhlbHAnKTtcbiAgICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMub3Blbiwge1xuICAgICAgY2FwdGlvbixcbiAgICAgIGlzRW5hYmxlZDogKCkgPT5cbiAgICAgICAgIWluc3BlY3RvciB8fFxuICAgICAgICBpbnNwZWN0b3IuaXNEaXNwb3NlZCB8fFxuICAgICAgICAhaW5zcGVjdG9yLmlzQXR0YWNoZWQgfHxcbiAgICAgICAgIWluc3BlY3Rvci5pc1Zpc2libGUsXG4gICAgICBsYWJlbDogc2hvd0xhYmVsLFxuICAgICAgaWNvbjogYXJncyA9PiAoYXJncy5pc0xhdW5jaGVyID8gaW5zcGVjdG9ySWNvbiA6IHVuZGVmaW5lZCksXG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgdGV4dCA9IGFyZ3MgJiYgKGFyZ3MudGV4dCBhcyBzdHJpbmcpO1xuICAgICAgICBjb25zdCByZWZyZXNoID0gYXJncyAmJiAoYXJncy5yZWZyZXNoIGFzIGJvb2xlYW4pO1xuICAgICAgICAvLyBpZiBpbnNwZWN0b3IgaXMgb3Blbiwgc2VlIGlmIHdlIG5lZWQgYSByZWZyZXNoXG4gICAgICAgIGlmIChpc0luc3BlY3Rvck9wZW4oKSAmJiByZWZyZXNoKVxuICAgICAgICAgIGluc3BlY3Rvci5jb250ZW50LnNvdXJjZT8ub25FZGl0b3JDaGFuZ2UodGV4dCk7XG4gICAgICAgIGVsc2Ugb3Blbkluc3BlY3Rvcih0ZXh0KTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIEFkZCBpbnNwZWN0b3I6Y2xvc2UgY29tbWFuZCB0byByZWdpc3RyeS5cbiAgICBjb25zdCBjbG9zZUxhYmVsID0gdHJhbnMuX18oJ0hpZGUgQ29udGV4dHVhbCBIZWxwJyk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNsb3NlLCB7XG4gICAgICBjYXB0aW9uLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PiBpc0luc3BlY3Rvck9wZW4oKSxcbiAgICAgIGxhYmVsOiBjbG9zZUxhYmVsLFxuICAgICAgaWNvbjogYXJncyA9PiAoYXJncy5pc0xhdW5jaGVyID8gaW5zcGVjdG9ySWNvbiA6IHVuZGVmaW5lZCksXG4gICAgICBleGVjdXRlOiAoKSA9PiBjbG9zZUluc3BlY3RvcigpXG4gICAgfSk7XG5cbiAgICAvLyBBZGQgaW5zcGVjdG9yOnRvZ2dsZSBjb21tYW5kIHRvIHJlZ2lzdHJ5LlxuICAgIGNvbnN0IHRvZ2dsZUxhYmVsID0gdHJhbnMuX18oJ1Nob3cgQ29udGV4dHVhbCBIZWxwJyk7XG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZSwge1xuICAgICAgY2FwdGlvbixcbiAgICAgIGxhYmVsOiB0b2dnbGVMYWJlbCxcbiAgICAgIGlzVG9nZ2xlZDogKCkgPT4gaXNJbnNwZWN0b3JPcGVuKCksXG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgaWYgKGlzSW5zcGVjdG9yT3BlbigpKSB7XG4gICAgICAgICAgY2xvc2VJbnNwZWN0b3IoKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBjb25zdCB0ZXh0ID0gYXJncyAmJiAoYXJncy50ZXh0IGFzIHN0cmluZyk7XG4gICAgICAgICAgb3Blbkluc3BlY3Rvcih0ZXh0KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgLy8gQWRkIG9wZW4gY29tbWFuZCB0byBsYXVuY2hlciBpZiBwb3NzaWJsZS5cbiAgICBpZiAobGF1bmNoZXIpIHtcbiAgICAgIGxhdW5jaGVyLmFkZCh7IGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlbiwgYXJnczogeyBpc0xhdW5jaGVyOiB0cnVlIH0gfSk7XG4gICAgfVxuXG4gICAgLy8gQWRkIHRvZ2dsZSBjb21tYW5kIHRvIGNvbW1hbmQgcGFsZXR0ZSBpZiBwb3NzaWJsZS5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZDogQ29tbWFuZElEcy50b2dnbGUsIGNhdGVnb3J5OiB0b2dnbGVMYWJlbCB9KTtcbiAgICB9XG5cbiAgICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICB2b2lkIHJlc3RvcmVyLnJlc3RvcmUodHJhY2tlciwge1xuICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLnRvZ2dsZSxcbiAgICAgICAgbmFtZTogKCkgPT4gJ2luc3BlY3RvcidcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8vIENyZWF0ZSBhIHByb3h5IHRvIHBhc3MgdGhlIGBzb3VyY2VgIHRvIHRoZSBjdXJyZW50IGluc3BlY3Rvci5cbiAgICBjb25zdCBwcm94eSA9IE9iamVjdC5kZWZpbmVQcm9wZXJ0eSh7fSBhcyBJSW5zcGVjdG9yLCAnc291cmNlJywge1xuICAgICAgZ2V0OiAoKTogSUluc3BlY3Rvci5JSW5zcGVjdGFibGUgfCBudWxsID0+XG4gICAgICAgICFpbnNwZWN0b3IgfHwgaW5zcGVjdG9yLmlzRGlzcG9zZWQgPyBudWxsIDogaW5zcGVjdG9yLmNvbnRlbnQuc291cmNlLFxuICAgICAgc2V0OiAoc3JjOiBJSW5zcGVjdG9yLklJbnNwZWN0YWJsZSB8IG51bGwpID0+IHtcbiAgICAgICAgc291cmNlID0gc3JjICYmICFzcmMuaXNEaXNwb3NlZCA/IHNyYyA6IG51bGw7XG4gICAgICAgIGlmIChpbnNwZWN0b3IgJiYgIWluc3BlY3Rvci5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgaW5zcGVjdG9yLmNvbnRlbnQuc291cmNlID0gc291cmNlO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICByZXR1cm4gcHJveHk7XG4gIH1cbn07XG5cbi8qKlxuICogQW4gZXh0ZW5zaW9uIHRoYXQgcmVnaXN0ZXJzIGNvbnNvbGVzIGZvciBpbnNwZWN0aW9uLlxuICovXG5jb25zdCBjb25zb2xlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICAvLyBGSVhNRSBUaGlzIHNob3VsZCBiZSBpbiBAanVweXRlcmxhYi9jb25zb2xlLWV4dGVuc2lvblxuICBpZDogJ0BqdXB5dGVybGFiL2luc3BlY3Rvci1leHRlbnNpb246Y29uc29sZXMnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgY29kZSBpbnRyb3NwZWN0aW9uIHN1cHBvcnQgdG8gY29uc29sZXMuJyxcbiAgcmVxdWlyZXM6IFtJSW5zcGVjdG9yLCBJQ29uc29sZVRyYWNrZXIsIElMYWJTaGVsbF0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBtYW5hZ2VyOiBJSW5zcGVjdG9yLFxuICAgIGNvbnNvbGVzOiBJQ29uc29sZVRyYWNrZXIsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApOiB2b2lkID0+IHtcbiAgICAvLyBNYWludGFpbiBhc3NvY2lhdGlvbiBvZiBuZXcgY29uc29sZXMgd2l0aCB0aGVpciByZXNwZWN0aXZlIGhhbmRsZXJzLlxuICAgIGNvbnN0IGhhbmRsZXJzOiB7IFtpZDogc3RyaW5nXTogSW5zcGVjdGlvbkhhbmRsZXIgfSA9IHt9O1xuXG4gICAgLy8gQ3JlYXRlIGEgaGFuZGxlciBmb3IgZWFjaCBjb25zb2xlIHRoYXQgaXMgY3JlYXRlZC5cbiAgICBjb25zb2xlcy53aWRnZXRBZGRlZC5jb25uZWN0KChzZW5kZXIsIHBhcmVudCkgPT4ge1xuICAgICAgY29uc3Qgc2Vzc2lvbkNvbnRleHQgPSBwYXJlbnQuY29uc29sZS5zZXNzaW9uQ29udGV4dDtcbiAgICAgIGNvbnN0IHJlbmRlcm1pbWUgPSBwYXJlbnQuY29uc29sZS5yZW5kZXJtaW1lO1xuICAgICAgY29uc3QgY29ubmVjdG9yID0gbmV3IEtlcm5lbENvbm5lY3Rvcih7IHNlc3Npb25Db250ZXh0IH0pO1xuICAgICAgY29uc3QgaGFuZGxlciA9IG5ldyBJbnNwZWN0aW9uSGFuZGxlcih7IGNvbm5lY3RvciwgcmVuZGVybWltZSB9KTtcblxuICAgICAgLy8gQXNzb2NpYXRlIHRoZSBoYW5kbGVyIHRvIHRoZSB3aWRnZXQuXG4gICAgICBoYW5kbGVyc1twYXJlbnQuaWRdID0gaGFuZGxlcjtcblxuICAgICAgLy8gU2V0IHRoZSBpbml0aWFsIGVkaXRvci5cbiAgICAgIGNvbnN0IGNlbGwgPSBwYXJlbnQuY29uc29sZS5wcm9tcHRDZWxsO1xuICAgICAgaGFuZGxlci5lZGl0b3IgPSBjZWxsICYmIGNlbGwuZWRpdG9yO1xuXG4gICAgICAvLyBMaXN0ZW4gZm9yIHByb21wdCBjcmVhdGlvbi5cbiAgICAgIHBhcmVudC5jb25zb2xlLnByb21wdENlbGxDcmVhdGVkLmNvbm5lY3QoKHNlbmRlciwgY2VsbCkgPT4ge1xuICAgICAgICBoYW5kbGVyLmVkaXRvciA9IGNlbGwgJiYgY2VsbC5lZGl0b3I7XG4gICAgICB9KTtcblxuICAgICAgLy8gTGlzdGVuIGZvciBwYXJlbnQgZGlzcG9zYWwuXG4gICAgICBwYXJlbnQuZGlzcG9zZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgIGRlbGV0ZSBoYW5kbGVyc1twYXJlbnQuaWRdO1xuICAgICAgICBoYW5kbGVyLmRpc3Bvc2UoKTtcbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgLy8gS2VlcCB0cmFjayBvZiBjb25zb2xlIGluc3RhbmNlcyBhbmQgc2V0IGluc3BlY3RvciBzb3VyY2UuXG4gICAgY29uc3Qgc2V0U291cmNlID0gKHdpZGdldDogV2lkZ2V0IHwgbnVsbCk6IHZvaWQgPT4ge1xuICAgICAgaWYgKHdpZGdldCAmJiBjb25zb2xlcy5oYXMod2lkZ2V0KSAmJiBoYW5kbGVyc1t3aWRnZXQuaWRdKSB7XG4gICAgICAgIG1hbmFnZXIuc291cmNlID0gaGFuZGxlcnNbd2lkZ2V0LmlkXTtcbiAgICAgIH1cbiAgICB9O1xuICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoKF8sIGFyZ3MpID0+IHNldFNvdXJjZShhcmdzLm5ld1ZhbHVlKSk7XG4gICAgdm9pZCBhcHAucmVzdG9yZWQudGhlbigoKSA9PiBzZXRTb3VyY2UobGFiU2hlbGwuY3VycmVudFdpZGdldCkpO1xuICB9XG59O1xuXG4vKipcbiAqIEFuIGV4dGVuc2lvbiB0aGF0IHJlZ2lzdGVycyBub3RlYm9va3MgZm9yIGluc3BlY3Rpb24uXG4gKi9cbmNvbnN0IG5vdGVib29rczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICAvLyBGSVhNRSBUaGlzIHNob3VsZCBiZSBpbiBAanVweXRlcmxhYi9ub3RlYm9vay1leHRlbnNpb25cbiAgaWQ6ICdAanVweXRlcmxhYi9pbnNwZWN0b3ItZXh0ZW5zaW9uOm5vdGVib29rcycsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyBjb2RlIGludHJvc3BlY3Rpb24gdG8gbm90ZWJvb2tzLicsXG4gIHJlcXVpcmVzOiBbSUluc3BlY3RvciwgSU5vdGVib29rVHJhY2tlciwgSUxhYlNoZWxsXSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElJbnNwZWN0b3IsXG4gICAgbm90ZWJvb2tzOiBJTm90ZWJvb2tUcmFja2VyLFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGxcbiAgKTogdm9pZCA9PiB7XG4gICAgLy8gTWFpbnRhaW4gYXNzb2NpYXRpb24gb2YgbmV3IG5vdGVib29rcyB3aXRoIHRoZWlyIHJlc3BlY3RpdmUgaGFuZGxlcnMuXG4gICAgY29uc3QgaGFuZGxlcnM6IHsgW2lkOiBzdHJpbmddOiBJbnNwZWN0aW9uSGFuZGxlciB9ID0ge307XG5cbiAgICAvLyBDcmVhdGUgYSBoYW5kbGVyIGZvciBlYWNoIG5vdGVib29rIHRoYXQgaXMgY3JlYXRlZC5cbiAgICBub3RlYm9va3Mud2lkZ2V0QWRkZWQuY29ubmVjdCgoc2VuZGVyLCBwYXJlbnQpID0+IHtcbiAgICAgIGNvbnN0IHNlc3Npb25Db250ZXh0ID0gcGFyZW50LnNlc3Npb25Db250ZXh0O1xuICAgICAgY29uc3QgcmVuZGVybWltZSA9IHBhcmVudC5jb250ZW50LnJlbmRlcm1pbWU7XG4gICAgICBjb25zdCBjb25uZWN0b3IgPSBuZXcgS2VybmVsQ29ubmVjdG9yKHsgc2Vzc2lvbkNvbnRleHQgfSk7XG4gICAgICBjb25zdCBoYW5kbGVyID0gbmV3IEluc3BlY3Rpb25IYW5kbGVyKHsgY29ubmVjdG9yLCByZW5kZXJtaW1lIH0pO1xuXG4gICAgICAvLyBBc3NvY2lhdGUgdGhlIGhhbmRsZXIgdG8gdGhlIHdpZGdldC5cbiAgICAgIGhhbmRsZXJzW3BhcmVudC5pZF0gPSBoYW5kbGVyO1xuXG4gICAgICAvLyBTZXQgdGhlIGluaXRpYWwgZWRpdG9yLlxuICAgICAgY29uc3QgY2VsbCA9IHBhcmVudC5jb250ZW50LmFjdGl2ZUNlbGw7XG4gICAgICBoYW5kbGVyLmVkaXRvciA9IGNlbGwgJiYgY2VsbC5lZGl0b3I7XG5cbiAgICAgIC8vIExpc3RlbiBmb3IgYWN0aXZlIGNlbGwgY2hhbmdlcy5cbiAgICAgIHBhcmVudC5jb250ZW50LmFjdGl2ZUNlbGxDaGFuZ2VkLmNvbm5lY3QoKHNlbmRlciwgY2VsbCkgPT4ge1xuICAgICAgICB2b2lkIGNlbGw/LnJlYWR5LnRoZW4oKCkgPT4ge1xuICAgICAgICAgIGlmIChjZWxsID09PSBwYXJlbnQuY29udGVudC5hY3RpdmVDZWxsKSB7XG4gICAgICAgICAgICBoYW5kbGVyLmVkaXRvciA9IGNlbGwhLmVkaXRvcjtcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgICAgfSk7XG5cbiAgICAgIC8vIExpc3RlbiBmb3IgcGFyZW50IGRpc3Bvc2FsLlxuICAgICAgcGFyZW50LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICBkZWxldGUgaGFuZGxlcnNbcGFyZW50LmlkXTtcbiAgICAgICAgaGFuZGxlci5kaXNwb3NlKCk7XG4gICAgICB9KTtcbiAgICB9KTtcblxuICAgIC8vIEtlZXAgdHJhY2sgb2Ygbm90ZWJvb2sgaW5zdGFuY2VzIGFuZCBzZXQgaW5zcGVjdG9yIHNvdXJjZS5cbiAgICBjb25zdCBzZXRTb3VyY2UgPSAod2lkZ2V0OiBXaWRnZXQgfCBudWxsKTogdm9pZCA9PiB7XG4gICAgICBpZiAod2lkZ2V0ICYmIG5vdGVib29rcy5oYXMod2lkZ2V0KSAmJiBoYW5kbGVyc1t3aWRnZXQuaWRdKSB7XG4gICAgICAgIG1hbmFnZXIuc291cmNlID0gaGFuZGxlcnNbd2lkZ2V0LmlkXTtcbiAgICAgIH1cbiAgICB9O1xuICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QoKF8sIGFyZ3MpID0+IHNldFNvdXJjZShhcmdzLm5ld1ZhbHVlKSk7XG4gICAgdm9pZCBhcHAucmVzdG9yZWQudGhlbigoKSA9PiBzZXRTb3VyY2UobGFiU2hlbGwuY3VycmVudFdpZGdldCkpO1xuICB9XG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2lucyBhcyBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW2luc3BlY3RvciwgY29uc29sZXMsIG5vdGVib29rc107XG5leHBvcnQgZGVmYXVsdCBwbHVnaW5zO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9