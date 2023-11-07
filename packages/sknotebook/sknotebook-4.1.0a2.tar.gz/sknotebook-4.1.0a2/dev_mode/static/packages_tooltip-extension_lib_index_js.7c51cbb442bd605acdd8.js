"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_tooltip-extension_lib_index_js"],{

/***/ "../packages/tooltip-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../packages/tooltip-extension/lib/index.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/tooltip */ "webpack/sharing/consume/default/@jupyterlab/tooltip/@jupyterlab/tooltip");
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_8__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module tooltip-extension
 */









/**
 * The command IDs used by the tooltip plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.dismiss = 'tooltip:dismiss';
    CommandIDs.launchConsole = 'tooltip:launch-console';
    CommandIDs.launchNotebook = 'tooltip:launch-notebook';
    CommandIDs.launchFile = 'tooltip:launch-file';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main tooltip manager plugin.
 */
const manager = {
    id: '@jupyterlab/tooltip-extension:manager',
    description: 'Provides the tooltip manager.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    provides: _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager,
    activate: (app, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        let tooltip = null;
        // Add tooltip dismiss command.
        app.commands.addCommand(CommandIDs.dismiss, {
            label: trans.__('Dismiss the tooltip'),
            execute: () => {
                if (tooltip) {
                    tooltip.dispose();
                    tooltip = null;
                }
            }
        });
        return {
            invoke(options) {
                const detail = 0;
                const { anchor, editor, kernel, rendermime } = options;
                if (tooltip) {
                    tooltip.dispose();
                    tooltip = null;
                }
                return Private.fetch({ detail, editor, kernel })
                    .then(bundle => {
                    tooltip = new _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.Tooltip({ anchor, bundle, editor, rendermime });
                    _lumino_widgets__WEBPACK_IMPORTED_MODULE_8__.Widget.attach(tooltip, document.body);
                })
                    .catch(() => {
                    /* Fails silently. */
                });
            }
        };
    }
};
/**
 * The console tooltip plugin.
 */
const consoles = {
    // FIXME This should be in @jupyterlab/console-extension
    id: '@jupyterlab/tooltip-extension:consoles',
    description: 'Adds the tooltip capability to consoles.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_0__.IConsoleTracker],
    activate: (app, manager, consoles, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchConsole, {
            label: trans.__('Open the tooltip'),
            execute: () => {
                var _a, _b;
                const parent = consoles.currentWidget;
                if (!parent) {
                    return;
                }
                const anchor = parent.console;
                const editor = (_a = anchor.promptCell) === null || _a === void 0 ? void 0 : _a.editor;
                const kernel = (_b = anchor.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
                const rendermime = anchor.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * The notebook tooltip plugin.
 */
const notebooks = {
    // FIXME This should be in @jupyterlab/notebook-extension
    id: '@jupyterlab/tooltip-extension:notebooks',
    description: 'Adds the tooltip capability to notebooks.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker],
    activate: (app, manager, notebooks, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchNotebook, {
            label: trans.__('Open the tooltip'),
            execute: () => {
                var _a, _b;
                const parent = notebooks.currentWidget;
                if (!parent) {
                    return;
                }
                const anchor = parent.content;
                const editor = (_a = anchor.activeCell) === null || _a === void 0 ? void 0 : _a.editor;
                const kernel = (_b = parent.sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel;
                const rendermime = anchor.rendermime;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * The file editor tooltip plugin.
 */
const files = {
    // FIXME This should be in @jupyterlab/fileeditor-extension
    id: '@jupyterlab/tooltip-extension:files',
    description: 'Adds the tooltip capability to file editors.',
    autoStart: true,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.ITranslator],
    requires: [_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_5__.ITooltipManager, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorTracker, _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry],
    activate: (app, manager, editorTracker, rendermime, translator) => {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
        // Keep a list of active ISessions so that we can
        // clean them up when they are no longer needed.
        const activeSessions = {};
        const sessions = app.serviceManager.sessions;
        // When the list of running sessions changes,
        // check to see if there are any kernels with a
        // matching path for the file editors.
        const onRunningChanged = (sender, models) => {
            editorTracker.forEach(file => {
                const model = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_7__.find)(models, m => file.context.path === m.path);
                if (model) {
                    const oldSession = activeSessions[file.id];
                    // If there is a matching path, but it is the same
                    // session as we previously had, do nothing.
                    if (oldSession && oldSession.id === model.id) {
                        return;
                    }
                    // Otherwise, dispose of the old session and reset to
                    // a new CompletionConnector.
                    if (oldSession) {
                        delete activeSessions[file.id];
                        oldSession.dispose();
                    }
                    const session = sessions.connectTo({ model });
                    activeSessions[file.id] = session;
                }
                else {
                    const session = activeSessions[file.id];
                    if (session) {
                        session.dispose();
                        delete activeSessions[file.id];
                    }
                }
            });
        };
        onRunningChanged(sessions, sessions.running());
        sessions.runningChanged.connect(onRunningChanged);
        // Clean up after a widget when it is disposed
        editorTracker.widgetAdded.connect((sender, widget) => {
            widget.disposed.connect(w => {
                const session = activeSessions[w.id];
                if (session) {
                    session.dispose();
                    delete activeSessions[w.id];
                }
            });
        });
        // Add tooltip launch command.
        app.commands.addCommand(CommandIDs.launchFile, {
            label: trans.__('Open the tooltip'),
            execute: async () => {
                const parent = editorTracker.currentWidget;
                const kernel = parent &&
                    activeSessions[parent.id] &&
                    activeSessions[parent.id].kernel;
                if (!kernel) {
                    return;
                }
                const anchor = parent.content;
                const editor = anchor === null || anchor === void 0 ? void 0 : anchor.editor;
                // If all components necessary for rendering exist, create a tooltip.
                if (!!editor && !!kernel && !!rendermime) {
                    return manager.invoke({ anchor, editor, kernel, rendermime });
                }
            }
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    manager,
    consoles,
    notebooks,
    files
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A counter for outstanding requests.
     */
    let pending = 0;
    /**
     * Fetch a tooltip's content from the API server.
     */
    function fetch(options) {
        const { detail, editor, kernel } = options;
        const code = editor.model.sharedModel.getSource();
        const position = editor.getCursorPosition();
        const offset = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.Text.jsIndexToCharIndex(editor.getOffsetAt(position), code);
        // Clear hints if the new text value is empty or kernel is unavailable.
        if (!code || !kernel) {
            return Promise.reject(void 0);
        }
        const contents = {
            code,
            cursor_pos: offset,
            detail_level: detail || 0
        };
        const current = ++pending;
        return kernel.requestInspect(contents).then(msg => {
            const value = msg.content;
            // If a newer request is pending, bail.
            if (current !== pending) {
                return Promise.reject(void 0);
            }
            // If request fails or returns negative results, bail.
            if (value.status !== 'ok' || !value.found) {
                return Promise.reject(void 0);
            }
            return Promise.resolve(value.data);
        });
    }
    Private.fetch = fetch;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdG9vbHRpcC1leHRlbnNpb25fbGliX2luZGV4X2pzLjdjNTFjYmI0NDJiZDYwNWFjZGQ4LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU9tRDtBQUNUO0FBQ1c7QUFDQTtBQUNLO0FBRUU7QUFDTztBQUM3QjtBQUVBO0FBRXpDOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBUW5CO0FBUkQsV0FBVSxVQUFVO0lBQ0wsa0JBQU8sR0FBRyxpQkFBaUIsQ0FBQztJQUU1Qix3QkFBYSxHQUFHLHdCQUF3QixDQUFDO0lBRXpDLHlCQUFjLEdBQUcseUJBQXlCLENBQUM7SUFFM0MscUJBQVUsR0FBRyxxQkFBcUIsQ0FBQztBQUNsRCxDQUFDLEVBUlMsVUFBVSxLQUFWLFVBQVUsUUFRbkI7QUFFRDs7R0FFRztBQUNILE1BQU0sT0FBTyxHQUEyQztJQUN0RCxFQUFFLEVBQUUsdUNBQXVDO0lBQzNDLFdBQVcsRUFBRSwrQkFBK0I7SUFDNUMsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FBQyxnRUFBVyxDQUFDO0lBQ3ZCLFFBQVEsRUFBRSxnRUFBZTtJQUN6QixRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixVQUE4QixFQUNiLEVBQUU7UUFDbkIsTUFBTSxLQUFLLEdBQUcsQ0FBQyxVQUFVLGFBQVYsVUFBVSxjQUFWLFVBQVUsR0FBSSxtRUFBYyxDQUFDLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQ2hFLElBQUksT0FBTyxHQUFtQixJQUFJLENBQUM7UUFFbkMsK0JBQStCO1FBQy9CLEdBQUcsQ0FBQyxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxPQUFPLEVBQUU7WUFDMUMsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMscUJBQXFCLENBQUM7WUFDdEMsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixJQUFJLE9B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Q3REO1lBRUQsT0FBTyxPQUFPLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUNyQyxDQUFDLENBQUMsQ0FBQztJQUNMLENBQUM7SUFqQ2UsYUFBSyxRQWlDcEI7QUFDSCxDQUFDLEVBaEVTLE9BQU8sS0FBUCxPQUFPLFFBZ0VoQiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90b29sdGlwLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdG9vbHRpcC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBJQ29uc29sZVRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9jb25zb2xlJztcbmltcG9ydCB7IFRleHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSUVkaXRvclRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9maWxlZWRpdG9yJztcbmltcG9ydCB7IElOb3RlYm9va1RyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9ub3RlYm9vayc7XG5pbXBvcnQgeyBJUmVuZGVyTWltZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBLZXJuZWwsIEtlcm5lbE1lc3NhZ2UsIFNlc3Npb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJVG9vbHRpcE1hbmFnZXIsIFRvb2x0aXAgfSBmcm9tICdAanVweXRlcmxhYi90b29sdGlwJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGZpbmQgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgdG9vbHRpcCBwbHVnaW4uXG4gKi9cbm5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IGRpc21pc3MgPSAndG9vbHRpcDpkaXNtaXNzJztcblxuICBleHBvcnQgY29uc3QgbGF1bmNoQ29uc29sZSA9ICd0b29sdGlwOmxhdW5jaC1jb25zb2xlJztcblxuICBleHBvcnQgY29uc3QgbGF1bmNoTm90ZWJvb2sgPSAndG9vbHRpcDpsYXVuY2gtbm90ZWJvb2snO1xuXG4gIGV4cG9ydCBjb25zdCBsYXVuY2hGaWxlID0gJ3Rvb2x0aXA6bGF1bmNoLWZpbGUnO1xufVxuXG4vKipcbiAqIFRoZSBtYWluIHRvb2x0aXAgbWFuYWdlciBwbHVnaW4uXG4gKi9cbmNvbnN0IG1hbmFnZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJVG9vbHRpcE1hbmFnZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3Rvb2x0aXAtZXh0ZW5zaW9uOm1hbmFnZXInLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSB0b29sdGlwIG1hbmFnZXIuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBvcHRpb25hbDogW0lUcmFuc2xhdG9yXSxcbiAgcHJvdmlkZXM6IElUb29sdGlwTWFuYWdlcixcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvciB8IG51bGxcbiAgKTogSVRvb2x0aXBNYW5hZ2VyID0+IHtcbiAgICBjb25zdCB0cmFucyA9ICh0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgbGV0IHRvb2x0aXA6IFRvb2x0aXAgfCBudWxsID0gbnVsbDtcblxuICAgIC8vIEFkZCB0b29sdGlwIGRpc21pc3MgY29tbWFuZC5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRpc21pc3MsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRGlzbWlzcyB0aGUgdG9vbHRpcCcpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBpZiAodG9vbHRpcCkge1xuICAgICAgICAgIHRvb2x0aXAuZGlzcG9zZSgpO1xuICAgICAgICAgIHRvb2x0aXAgPSBudWxsO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICByZXR1cm4ge1xuICAgICAgaW52b2tlKG9wdGlvbnM6IElUb29sdGlwTWFuYWdlci5JT3B0aW9ucyk6IFByb21pc2U8dm9pZD4ge1xuICAgICAgICBjb25zdCBkZXRhaWw6IDAgfCAxID0gMDtcbiAgICAgICAgY29uc3QgeyBhbmNob3IsIGVkaXRvciwga2VybmVsLCByZW5kZXJtaW1lIH0gPSBvcHRpb25zO1xuXG4gICAgICAgIGlmICh0b29sdGlwKSB7XG4gICAgICAgICAgdG9vbHRpcC5kaXNwb3NlKCk7XG4gICAgICAgICAgdG9vbHRpcCA9IG51bGw7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4gUHJpdmF0ZS5mZXRjaCh7IGRldGFpbCwgZWRpdG9yLCBrZXJuZWwgfSlcbiAgICAgICAgICAudGhlbihidW5kbGUgPT4ge1xuICAgICAgICAgICAgdG9vbHRpcCA9IG5ldyBUb29sdGlwKHsgYW5jaG9yLCBidW5kbGUsIGVkaXRvciwgcmVuZGVybWltZSB9KTtcbiAgICAgICAgICAgIFdpZGdldC5hdHRhY2godG9vbHRpcCwgZG9jdW1lbnQuYm9keSk7XG4gICAgICAgICAgfSlcbiAgICAgICAgICAuY2F0Y2goKCkgPT4ge1xuICAgICAgICAgICAgLyogRmFpbHMgc2lsZW50bHkuICovXG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgY29uc29sZSB0b29sdGlwIHBsdWdpbi5cbiAqL1xuY29uc3QgY29uc29sZXM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgLy8gRklYTUUgVGhpcyBzaG91bGQgYmUgaW4gQGp1cHl0ZXJsYWIvY29uc29sZS1leHRlbnNpb25cbiAgaWQ6ICdAanVweXRlcmxhYi90b29sdGlwLWV4dGVuc2lvbjpjb25zb2xlcycsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0aGUgdG9vbHRpcCBjYXBhYmlsaXR5IHRvIGNvbnNvbGVzLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgb3B0aW9uYWw6IFtJVHJhbnNsYXRvcl0sXG4gIHJlcXVpcmVzOiBbSVRvb2x0aXBNYW5hZ2VyLCBJQ29uc29sZVRyYWNrZXJdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElUb29sdGlwTWFuYWdlcixcbiAgICBjb25zb2xlczogSUNvbnNvbGVUcmFja2VyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbFxuICApOiB2b2lkID0+IHtcbiAgICBjb25zdCB0cmFucyA9ICh0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICAvLyBBZGQgdG9vbHRpcCBsYXVuY2ggY29tbWFuZC5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmxhdW5jaENvbnNvbGUsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnT3BlbiB0aGUgdG9vbHRpcCcpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBwYXJlbnQgPSBjb25zb2xlcy5jdXJyZW50V2lkZ2V0O1xuXG4gICAgICAgIGlmICghcGFyZW50KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgYW5jaG9yID0gcGFyZW50LmNvbnNvbGU7XG4gICAgICAgIGNvbnN0IGVkaXRvciA9IGFuY2hvci5wcm9tcHRDZWxsPy5lZGl0b3I7XG4gICAgICAgIGNvbnN0IGtlcm5lbCA9IGFuY2hvci5zZXNzaW9uQ29udGV4dC5zZXNzaW9uPy5rZXJuZWw7XG4gICAgICAgIGNvbnN0IHJlbmRlcm1pbWUgPSBhbmNob3IucmVuZGVybWltZTtcblxuICAgICAgICAvLyBJZiBhbGwgY29tcG9uZW50cyBuZWNlc3NhcnkgZm9yIHJlbmRlcmluZyBleGlzdCwgY3JlYXRlIGEgdG9vbHRpcC5cbiAgICAgICAgaWYgKCEhZWRpdG9yICYmICEha2VybmVsICYmICEhcmVuZGVybWltZSkge1xuICAgICAgICAgIHJldHVybiBtYW5hZ2VyLmludm9rZSh7IGFuY2hvciwgZWRpdG9yLCBrZXJuZWwsIHJlbmRlcm1pbWUgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgbm90ZWJvb2sgdG9vbHRpcCBwbHVnaW4uXG4gKi9cbmNvbnN0IG5vdGVib29rczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICAvLyBGSVhNRSBUaGlzIHNob3VsZCBiZSBpbiBAanVweXRlcmxhYi9ub3RlYm9vay1leHRlbnNpb25cbiAgaWQ6ICdAanVweXRlcmxhYi90b29sdGlwLWV4dGVuc2lvbjpub3RlYm9va3MnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgdGhlIHRvb2x0aXAgY2FwYWJpbGl0eSB0byBub3RlYm9va3MuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBvcHRpb25hbDogW0lUcmFuc2xhdG9yXSxcbiAgcmVxdWlyZXM6IFtJVG9vbHRpcE1hbmFnZXIsIElOb3RlYm9va1RyYWNrZXJdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1hbmFnZXI6IElUb29sdGlwTWFuYWdlcixcbiAgICBub3RlYm9va3M6IElOb3RlYm9va1RyYWNrZXIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IgfCBudWxsXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gKHRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3IpLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIC8vIEFkZCB0b29sdGlwIGxhdW5jaCBjb21tYW5kLlxuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubGF1bmNoTm90ZWJvb2ssIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnT3BlbiB0aGUgdG9vbHRpcCcpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBjb25zdCBwYXJlbnQgPSBub3RlYm9va3MuY3VycmVudFdpZGdldDtcblxuICAgICAgICBpZiAoIXBhcmVudCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGFuY2hvciA9IHBhcmVudC5jb250ZW50O1xuICAgICAgICBjb25zdCBlZGl0b3IgPSBhbmNob3IuYWN0aXZlQ2VsbD8uZWRpdG9yO1xuICAgICAgICBjb25zdCBrZXJuZWwgPSBwYXJlbnQuc2Vzc2lvbkNvbnRleHQuc2Vzc2lvbj8ua2VybmVsO1xuICAgICAgICBjb25zdCByZW5kZXJtaW1lID0gYW5jaG9yLnJlbmRlcm1pbWU7XG5cbiAgICAgICAgLy8gSWYgYWxsIGNvbXBvbmVudHMgbmVjZXNzYXJ5IGZvciByZW5kZXJpbmcgZXhpc3QsIGNyZWF0ZSBhIHRvb2x0aXAuXG4gICAgICAgIGlmICghIWVkaXRvciAmJiAhIWtlcm5lbCAmJiAhIXJlbmRlcm1pbWUpIHtcbiAgICAgICAgICByZXR1cm4gbWFuYWdlci5pbnZva2UoeyBhbmNob3IsIGVkaXRvciwga2VybmVsLCByZW5kZXJtaW1lIH0pO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogVGhlIGZpbGUgZWRpdG9yIHRvb2x0aXAgcGx1Z2luLlxuICovXG5jb25zdCBmaWxlczogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICAvLyBGSVhNRSBUaGlzIHNob3VsZCBiZSBpbiBAanVweXRlcmxhYi9maWxlZWRpdG9yLWV4dGVuc2lvblxuICBpZDogJ0BqdXB5dGVybGFiL3Rvb2x0aXAtZXh0ZW5zaW9uOmZpbGVzJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIHRoZSB0b29sdGlwIGNhcGFiaWxpdHkgdG8gZmlsZSBlZGl0b3JzLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgb3B0aW9uYWw6IFtJVHJhbnNsYXRvcl0sXG4gIHJlcXVpcmVzOiBbSVRvb2x0aXBNYW5hZ2VyLCBJRWRpdG9yVHJhY2tlciwgSVJlbmRlck1pbWVSZWdpc3RyeV0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbWFuYWdlcjogSVRvb2x0aXBNYW5hZ2VyLFxuICAgIGVkaXRvclRyYWNrZXI6IElFZGl0b3JUcmFja2VyLFxuICAgIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnksXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IgfCBudWxsXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gKHRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3IpLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIC8vIEtlZXAgYSBsaXN0IG9mIGFjdGl2ZSBJU2Vzc2lvbnMgc28gdGhhdCB3ZSBjYW5cbiAgICAvLyBjbGVhbiB0aGVtIHVwIHdoZW4gdGhleSBhcmUgbm8gbG9uZ2VyIG5lZWRlZC5cbiAgICBjb25zdCBhY3RpdmVTZXNzaW9uczoge1xuICAgICAgW2lkOiBzdHJpbmddOiBTZXNzaW9uLklTZXNzaW9uQ29ubmVjdGlvbjtcbiAgICB9ID0ge307XG5cbiAgICBjb25zdCBzZXNzaW9ucyA9IGFwcC5zZXJ2aWNlTWFuYWdlci5zZXNzaW9ucztcbiAgICAvLyBXaGVuIHRoZSBsaXN0IG9mIHJ1bm5pbmcgc2Vzc2lvbnMgY2hhbmdlcyxcbiAgICAvLyBjaGVjayB0byBzZWUgaWYgdGhlcmUgYXJlIGFueSBrZXJuZWxzIHdpdGggYVxuICAgIC8vIG1hdGNoaW5nIHBhdGggZm9yIHRoZSBmaWxlIGVkaXRvcnMuXG4gICAgY29uc3Qgb25SdW5uaW5nQ2hhbmdlZCA9IChcbiAgICAgIHNlbmRlcjogU2Vzc2lvbi5JTWFuYWdlcixcbiAgICAgIG1vZGVsczogSXRlcmFibGU8U2Vzc2lvbi5JTW9kZWw+XG4gICAgKSA9PiB7XG4gICAgICBlZGl0b3JUcmFja2VyLmZvckVhY2goZmlsZSA9PiB7XG4gICAgICAgIGNvbnN0IG1vZGVsID0gZmluZChtb2RlbHMsIG0gPT4gZmlsZS5jb250ZXh0LnBhdGggPT09IG0ucGF0aCk7XG4gICAgICAgIGlmIChtb2RlbCkge1xuICAgICAgICAgIGNvbnN0IG9sZFNlc3Npb24gPSBhY3RpdmVTZXNzaW9uc1tmaWxlLmlkXTtcbiAgICAgICAgICAvLyBJZiB0aGVyZSBpcyBhIG1hdGNoaW5nIHBhdGgsIGJ1dCBpdCBpcyB0aGUgc2FtZVxuICAgICAgICAgIC8vIHNlc3Npb24gYXMgd2UgcHJldmlvdXNseSBoYWQsIGRvIG5vdGhpbmcuXG4gICAgICAgICAgaWYgKG9sZFNlc3Npb24gJiYgb2xkU2Vzc2lvbi5pZCA9PT0gbW9kZWwuaWQpIHtcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICB9XG4gICAgICAgICAgLy8gT3RoZXJ3aXNlLCBkaXNwb3NlIG9mIHRoZSBvbGQgc2Vzc2lvbiBhbmQgcmVzZXQgdG9cbiAgICAgICAgICAvLyBhIG5ldyBDb21wbGV0aW9uQ29ubmVjdG9yLlxuICAgICAgICAgIGlmIChvbGRTZXNzaW9uKSB7XG4gICAgICAgICAgICBkZWxldGUgYWN0aXZlU2Vzc2lvbnNbZmlsZS5pZF07XG4gICAgICAgICAgICBvbGRTZXNzaW9uLmRpc3Bvc2UoKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgY29uc3Qgc2Vzc2lvbiA9IHNlc3Npb25zLmNvbm5lY3RUbyh7IG1vZGVsIH0pO1xuICAgICAgICAgIGFjdGl2ZVNlc3Npb25zW2ZpbGUuaWRdID0gc2Vzc2lvbjtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBjb25zdCBzZXNzaW9uID0gYWN0aXZlU2Vzc2lvbnNbZmlsZS5pZF07XG4gICAgICAgICAgaWYgKHNlc3Npb24pIHtcbiAgICAgICAgICAgIHNlc3Npb24uZGlzcG9zZSgpO1xuICAgICAgICAgICAgZGVsZXRlIGFjdGl2ZVNlc3Npb25zW2ZpbGUuaWRdO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfTtcbiAgICBvblJ1bm5pbmdDaGFuZ2VkKHNlc3Npb25zLCBzZXNzaW9ucy5ydW5uaW5nKCkpO1xuICAgIHNlc3Npb25zLnJ1bm5pbmdDaGFuZ2VkLmNvbm5lY3Qob25SdW5uaW5nQ2hhbmdlZCk7XG5cbiAgICAvLyBDbGVhbiB1cCBhZnRlciBhIHdpZGdldCB3aGVuIGl0IGlzIGRpc3Bvc2VkXG4gICAgZWRpdG9yVHJhY2tlci53aWRnZXRBZGRlZC5jb25uZWN0KChzZW5kZXIsIHdpZGdldCkgPT4ge1xuICAgICAgd2lkZ2V0LmRpc3Bvc2VkLmNvbm5lY3QodyA9PiB7XG4gICAgICAgIGNvbnN0IHNlc3Npb24gPSBhY3RpdmVTZXNzaW9uc1t3LmlkXTtcbiAgICAgICAgaWYgKHNlc3Npb24pIHtcbiAgICAgICAgICBzZXNzaW9uLmRpc3Bvc2UoKTtcbiAgICAgICAgICBkZWxldGUgYWN0aXZlU2Vzc2lvbnNbdy5pZF07XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgIH0pO1xuXG4gICAgLy8gQWRkIHRvb2x0aXAgbGF1bmNoIGNvbW1hbmQuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5sYXVuY2hGaWxlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ09wZW4gdGhlIHRvb2x0aXAnKSxcbiAgICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgICAgY29uc3QgcGFyZW50ID0gZWRpdG9yVHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgICAgICBjb25zdCBrZXJuZWwgPVxuICAgICAgICAgIHBhcmVudCAmJlxuICAgICAgICAgIGFjdGl2ZVNlc3Npb25zW3BhcmVudC5pZF0gJiZcbiAgICAgICAgICBhY3RpdmVTZXNzaW9uc1twYXJlbnQuaWRdLmtlcm5lbDtcbiAgICAgICAgaWYgKCFrZXJuZWwpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cbiAgICAgICAgY29uc3QgYW5jaG9yID0gcGFyZW50IS5jb250ZW50O1xuICAgICAgICBjb25zdCBlZGl0b3IgPSBhbmNob3I/LmVkaXRvcjtcblxuICAgICAgICAvLyBJZiBhbGwgY29tcG9uZW50cyBuZWNlc3NhcnkgZm9yIHJlbmRlcmluZyBleGlzdCwgY3JlYXRlIGEgdG9vbHRpcC5cbiAgICAgICAgaWYgKCEhZWRpdG9yICYmICEha2VybmVsICYmICEhcmVuZGVybWltZSkge1xuICAgICAgICAgIHJldHVybiBtYW5hZ2VyLmludm9rZSh7IGFuY2hvciwgZWRpdG9yLCBrZXJuZWwsIHJlbmRlcm1pbWUgfSk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbnMgYXMgZGVmYXVsdC5cbiAqL1xuY29uc3QgcGx1Z2luczogSnVweXRlckZyb250RW5kUGx1Z2luPGFueT5bXSA9IFtcbiAgbWFuYWdlcixcbiAgY29uc29sZXMsXG4gIG5vdGVib29rcyxcbiAgZmlsZXNcbl07XG5leHBvcnQgZGVmYXVsdCBwbHVnaW5zO1xuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBwcml2YXRlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEEgY291bnRlciBmb3Igb3V0c3RhbmRpbmcgcmVxdWVzdHMuXG4gICAqL1xuICBsZXQgcGVuZGluZyA9IDA7XG5cbiAgZXhwb3J0IGludGVyZmFjZSBJRmV0Y2hPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgZGV0YWlsIGxldmVsIHJlcXVlc3RlZCBmcm9tIHRoZSBBUEkuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhlIG9ubHkgYWNjZXB0YWJsZSB2YWx1ZXMgYXJlIDAgYW5kIDEuIFRoZSBkZWZhdWx0IHZhbHVlIGlzIDAuXG4gICAgICogQHNlZSBodHRwOi8vanVweXRlci1jbGllbnQucmVhZHRoZWRvY3MuaW8vZW4vbGF0ZXN0L21lc3NhZ2luZy5odG1sI2ludHJvc3BlY3Rpb25cbiAgICAgKi9cbiAgICBkZXRhaWw/OiAwIHwgMTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByZWZlcmVudCBlZGl0b3IgZm9yIHRoZSB0b29sdGlwLlxuICAgICAqL1xuICAgIGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGtlcm5lbCBhZ2FpbnN0IHdoaWNoIHRoZSBBUEkgcmVxdWVzdCB3aWxsIGJlIG1hZGUuXG4gICAgICovXG4gICAga2VybmVsOiBLZXJuZWwuSUtlcm5lbENvbm5lY3Rpb247XG4gIH1cblxuICAvKipcbiAgICogRmV0Y2ggYSB0b29sdGlwJ3MgY29udGVudCBmcm9tIHRoZSBBUEkgc2VydmVyLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGZldGNoKG9wdGlvbnM6IElGZXRjaE9wdGlvbnMpOiBQcm9taXNlPEpTT05PYmplY3Q+IHtcbiAgICBjb25zdCB7IGRldGFpbCwgZWRpdG9yLCBrZXJuZWwgfSA9IG9wdGlvbnM7XG4gICAgY29uc3QgY29kZSA9IGVkaXRvci5tb2RlbC5zaGFyZWRNb2RlbC5nZXRTb3VyY2UoKTtcbiAgICBjb25zdCBwb3NpdGlvbiA9IGVkaXRvci5nZXRDdXJzb3JQb3NpdGlvbigpO1xuICAgIGNvbnN0IG9mZnNldCA9IFRleHQuanNJbmRleFRvQ2hhckluZGV4KGVkaXRvci5nZXRPZmZzZXRBdChwb3NpdGlvbiksIGNvZGUpO1xuXG4gICAgLy8gQ2xlYXIgaGludHMgaWYgdGhlIG5ldyB0ZXh0IHZhbHVlIGlzIGVtcHR5IG9yIGtlcm5lbCBpcyB1bmF2YWlsYWJsZS5cbiAgICBpZiAoIWNvZGUgfHwgIWtlcm5lbCkge1xuICAgICAgcmV0dXJuIFByb21pc2UucmVqZWN0KHZvaWQgMCk7XG4gICAgfVxuXG4gICAgY29uc3QgY29udGVudHM6IEtlcm5lbE1lc3NhZ2UuSUluc3BlY3RSZXF1ZXN0TXNnWydjb250ZW50J10gPSB7XG4gICAgICBjb2RlLFxuICAgICAgY3Vyc29yX3Bvczogb2Zmc2V0LFxuICAgICAgZGV0YWlsX2xldmVsOiBkZXRhaWwgfHwgMFxuICAgIH07XG4gICAgY29uc3QgY3VycmVudCA9ICsrcGVuZGluZztcblxuICAgIHJldHVybiBrZXJuZWwucmVxdWVzdEluc3BlY3QoY29udGVudHMpLnRoZW4obXNnID0+IHtcbiAgICAgIGNvbnN0IHZhbHVlID0gbXNnLmNvbnRlbnQ7XG5cbiAgICAgIC8vIElmIGEgbmV3ZXIgcmVxdWVzdCBpcyBwZW5kaW5nLCBiYWlsLlxuICAgICAgaWYgKGN1cnJlbnQgIT09IHBlbmRpbmcpIHtcbiAgICAgICAgcmV0dXJuIFByb21pc2UucmVqZWN0KHZvaWQgMCkgYXMgUHJvbWlzZTxKU09OT2JqZWN0PjtcbiAgICAgIH1cblxuICAgICAgLy8gSWYgcmVxdWVzdCBmYWlscyBvciByZXR1cm5zIG5lZ2F0aXZlIHJlc3VsdHMsIGJhaWwuXG4gICAgICBpZiAodmFsdWUuc3RhdHVzICE9PSAnb2snIHx8ICF2YWx1ZS5mb3VuZCkge1xuICAgICAgICByZXR1cm4gUHJvbWlzZS5yZWplY3Qodm9pZCAwKSBhcyBQcm9taXNlPEpTT05PYmplY3Q+O1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKHZhbHVlLmRhdGEpO1xuICAgIH0pO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=