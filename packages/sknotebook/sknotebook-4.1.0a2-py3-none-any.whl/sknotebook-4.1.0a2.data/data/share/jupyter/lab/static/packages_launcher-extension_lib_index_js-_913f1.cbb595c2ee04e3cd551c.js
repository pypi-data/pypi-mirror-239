"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_launcher-extension_lib_index_js-_913f1"],{

/***/ "../packages/launcher-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/launcher-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module launcher-extension
 */







/**
 * The command IDs used by the launcher plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'launcher:create';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing an interface to the the launcher.
 */
const plugin = {
    activate,
    id: '@jupyterlab/launcher-extension:plugin',
    description: 'Provides the launcher tab service.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IDefaultFileBrowser,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory
    ],
    provides: _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.ILauncher,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the launcher.
 */
function activate(app, translator, labShell, palette, defaultBrowser, factory) {
    const { commands, shell } = app;
    const trans = translator.load('jupyterlab');
    const model = new _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.LauncherModel();
    commands.addCommand(CommandIDs.create, {
        label: trans.__('New Launcher'),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.skAddIcon : undefined),
        execute: (args) => {
            var _a, _b;
            const cwd = (_b = (_a = args['cwd']) !== null && _a !== void 0 ? _a : defaultBrowser === null || defaultBrowser === void 0 ? void 0 : defaultBrowser.model.path) !== null && _b !== void 0 ? _b : '';
            const id = `launcher-${Private.id++}`;
            const callback = (item) => {
                // If widget is attached to the main area replace the launcher
                if ((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_6__.find)(shell.widgets('main'), w => w === item)) {
                    shell.add(item, 'main', { ref: id });
                    launcher.dispose();
                }
            };
            const launcher = new _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_3__.Launcher({
                model,
                cwd,
                callback,
                commands,
                translator
            });
            launcher.model = model;
            launcher.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.launcherIcon;
            launcher.title.label = trans.__('Launcher');
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: launcher });
            // If there are any other widgets open, remove the launcher close icon.
            main.title.closable = !!Array.from(shell.widgets('main')).length;
            main.id = id;
            shell.add(main, 'main', {
                activate: args['activate'],
                ref: args['ref']
            });
            if (labShell) {
                labShell.layoutModified.connect(() => {
                    // If there is only a launcher open, remove the close icon.
                    main.title.closable = Array.from(labShell.widgets('main')).length > 1;
                }, main);
            }
            if (defaultBrowser) {
                const onPathChanged = (model) => {
                    launcher.cwd = model.path;
                };
                defaultBrowser.model.pathChanged.connect(onPathChanged);
                launcher.disposed.connect(() => {
                    defaultBrowser.model.pathChanged.disconnect(onPathChanged);
                });
            }
            return main;
        }
    });
    if (labShell) {
        void Promise.all([app.restored, defaultBrowser === null || defaultBrowser === void 0 ? void 0 : defaultBrowser.model.restored]).then(() => {
            function maybeCreate() {
                // Create a launcher if there are no open items.
                if (labShell.isEmpty('main')) {
                    void commands.execute(CommandIDs.create);
                }
            }
            // When layout is modified, create a launcher if there are no open items.
            labShell.layoutModified.connect(() => {
                maybeCreate();
            });
        });
    }
    if (palette) {
        palette.addItem({
            command: CommandIDs.create,
            category: trans.__('Launcher')
        });
    }
    if (labShell) {
        labShell.addButtonEnabled = true;
        labShell.addRequested.connect((sender, arg) => {
            var _a;
            // Get the ref for the current tab of the tabbar which the add button was clicked
            const ref = ((_a = arg.currentTitle) === null || _a === void 0 ? void 0 : _a.owner.id) ||
                arg.titles[arg.titles.length - 1].owner.id;
            return commands.execute(CommandIDs.create, { ref });
        });
    }
    return model;
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The incrementing id used for launcher widgets.
     */
    Private.id = 0;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbGF1bmNoZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fOTEzZjEuY2JiNTk1YzJlZTA0ZTNjZDU1MWMuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDc0M7QUFLdEM7QUFDeUM7QUFDcEI7QUFDYztBQUMzQjtBQUl6Qzs7R0FFRztBQUNILElBQVUsVUFBVSxDQUVuQjtBQUZELFdBQVUsVUFBVTtJQUNMLGlCQUFNLEdBQUcsaUJBQWlCLENBQUM7QUFDMUMsQ0FBQyxFQUZTLFVBQVUsS0FBVixVQUFVLFFBRW5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBcUM7SUFDL0MsUUFBUTtJQUNSLEVBQUUsRUFBRSx1Q0FBdUM7SUFDM0MsV0FBVyxFQUFFLG9DQUFvQztJQUNqRCxRQUFRLEVBQUUsQ0FBQyxnRUFBVyxDQUFDO0lBQ3ZCLFFBQVEsRUFBRTtRQUNSLDhEQUFTO1FBQ1QsaUVBQWU7UUFDZix3RUFBbUI7UUFDbkIsd0VBQW1CO0tBQ3BCO0lBQ0QsUUFBUSxFQUFFLDJEQUFTO0lBQ25CLFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7R0FFRztBQUNILGlFQUFlLE1BQU0sRUFBQztBQUV0Qjs7R0FFRztBQUNILFNBQVMsUUFBUSxDQUNmLEdBQW9CLEVBQ3BCLFVBQXVCLEVBQ3ZCLFFBQTBCLEVBQzFCLE9BQStCLEVBQy9CLGNBQTBDLEVBQzFDLE9BQW1DO0lBRW5DLE1BQU0sRUFBRSxRQUFRLEVBQUUsS0FBSyxFQUFFLEdBQUcsR0FBRyxDQUFDO0lBQ2hDLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7SUFDNUMsTUFBTSxLQUFLLEdBQUcsSUFBSSwrREFBYSxFQUFFLENBQUM7SUFFbEMsUUFBUSxDQUFDLFVBQVUsQ0FBQyxVQUFVLENBQUMsTUFBTSxFQUFFO1FBQ3JDLEtB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R0FBRyxDQUFDLENBQUMsQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDO1lBRTdDLE9BQU8sUUFBUSxDQUFDLE9BQU8sQ0FBQyxVQUFVLENBQUMsTUFBTSxFQUFFLEVBQUUsR0FBRyxFQUFFLENBQUMsQ0FBQztRQUN0RCxDQUFDLENBQUMsQ0FBQztLQUNKO0lBRUQsT0FBTyxLQUFLLENBQUM7QUFDZixDQUFDO0FBRUQ7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0FLaEI7QUFMRCxXQUFVLE9BQU87SUFDZjs7T0FFRztJQUNRLFVBQUUsR0FBRyxDQUFDLENBQUM7QUFDcEIsQ0FBQyxFQUxTLE9BQU8sS0FBUCxPQUFPLFFBS2hCIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2xhdW5jaGVyLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbGF1bmNoZXItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJQ29tbWFuZFBhbGV0dGUsIE1haW5BcmVhV2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgRmlsZUJyb3dzZXJNb2RlbCxcbiAgSURlZmF1bHRGaWxlQnJvd3NlcixcbiAgSUZpbGVCcm93c2VyRmFjdG9yeVxufSBmcm9tICdAanVweXRlcmxhYi9maWxlYnJvd3Nlcic7XG5pbXBvcnQgeyBJTGF1bmNoZXIsIExhdW5jaGVyLCBMYXVuY2hlck1vZGVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbGF1bmNoZXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBza0FkZEljb24sIGxhdW5jaGVySWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgZmluZCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBEb2NrUGFuZWwsIFRhYkJhciwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgbGF1bmNoZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjcmVhdGUgPSAnbGF1bmNoZXI6Y3JlYXRlJztcbn1cblxuLyoqXG4gKiBBIHNlcnZpY2UgcHJvdmlkaW5nIGFuIGludGVyZmFjZSB0byB0aGUgdGhlIGxhdW5jaGVyLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTGF1bmNoZXI+ID0ge1xuICBhY3RpdmF0ZSxcbiAgaWQ6ICdAanVweXRlcmxhYi9sYXVuY2hlci1leHRlbnNpb246cGx1Z2luJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgbGF1bmNoZXIgdGFiIHNlcnZpY2UuJyxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUxhYlNoZWxsLFxuICAgIElDb21tYW5kUGFsZXR0ZSxcbiAgICBJRGVmYXVsdEZpbGVCcm93c2VyLFxuICAgIElGaWxlQnJvd3NlckZhY3RvcnlcbiAgXSxcbiAgcHJvdmlkZXM6IElMYXVuY2hlcixcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2luIGFzIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUgbGF1bmNoZXIuXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsLFxuICBkZWZhdWx0QnJvd3NlcjogSURlZmF1bHRGaWxlQnJvd3NlciB8IG51bGwsXG4gIGZhY3Rvcnk6IElGaWxlQnJvd3NlckZhY3RvcnkgfCBudWxsXG4pOiBJTGF1bmNoZXIge1xuICBjb25zdCB7IGNvbW1hbmRzLCBzaGVsbCB9ID0gYXBwO1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBtb2RlbCA9IG5ldyBMYXVuY2hlck1vZGVsKCk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNyZWF0ZSwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnTmV3IExhdW5jaGVyJyksXG4gICAgaWNvbjogYXJncyA9PiAoYXJncy50b29sYmFyID8gc2tBZGRJY29uIDogdW5kZWZpbmVkKSxcbiAgICBleGVjdXRlOiAoYXJnczogSlNPTk9iamVjdCkgPT4ge1xuICAgICAgY29uc3QgY3dkID0gKGFyZ3NbJ2N3ZCddIGFzIHN0cmluZykgPz8gZGVmYXVsdEJyb3dzZXI/Lm1vZGVsLnBhdGggPz8gJyc7XG4gICAgICBjb25zdCBpZCA9IGBsYXVuY2hlci0ke1ByaXZhdGUuaWQrK31gO1xuICAgICAgY29uc3QgY2FsbGJhY2sgPSAoaXRlbTogV2lkZ2V0KSA9PiB7XG4gICAgICAgIC8vIElmIHdpZGdldCBpcyBhdHRhY2hlZCB0byB0aGUgbWFpbiBhcmVhIHJlcGxhY2UgdGhlIGxhdW5jaGVyXG4gICAgICAgIGlmIChmaW5kKHNoZWxsLndpZGdldHMoJ21haW4nKSwgdyA9PiB3ID09PSBpdGVtKSkge1xuICAgICAgICAgIHNoZWxsLmFkZChpdGVtLCAnbWFpbicsIHsgcmVmOiBpZCB9KTtcbiAgICAgICAgICBsYXVuY2hlci5kaXNwb3NlKCk7XG4gICAgICAgIH1cbiAgICAgIH07XG4gICAgICBjb25zdCBsYXVuY2hlciA9IG5ldyBMYXVuY2hlcih7XG4gICAgICAgIG1vZGVsLFxuICAgICAgICBjd2QsXG4gICAgICAgIGNhbGxiYWNrLFxuICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgdHJhbnNsYXRvclxuICAgICAgfSk7XG5cbiAgICAgIGxhdW5jaGVyLm1vZGVsID0gbW9kZWw7XG4gICAgICBsYXVuY2hlci50aXRsZS5pY29uID0gbGF1bmNoZXJJY29uO1xuICAgICAgbGF1bmNoZXIudGl0bGUubGFiZWwgPSB0cmFucy5fXygnTGF1bmNoZXInKTtcblxuICAgICAgY29uc3QgbWFpbiA9IG5ldyBNYWluQXJlYVdpZGdldCh7IGNvbnRlbnQ6IGxhdW5jaGVyIH0pO1xuXG4gICAgICAvLyBJZiB0aGVyZSBhcmUgYW55IG90aGVyIHdpZGdldHMgb3BlbiwgcmVtb3ZlIHRoZSBsYXVuY2hlciBjbG9zZSBpY29uLlxuICAgICAgbWFpbi50aXRsZS5jbG9zYWJsZSA9ICEhQXJyYXkuZnJvbShzaGVsbC53aWRnZXRzKCdtYWluJykpLmxlbmd0aDtcbiAgICAgIG1haW4uaWQgPSBpZDtcblxuICAgICAgc2hlbGwuYWRkKG1haW4sICdtYWluJywge1xuICAgICAgICBhY3RpdmF0ZTogYXJnc1snYWN0aXZhdGUnXSBhcyBib29sZWFuLFxuICAgICAgICByZWY6IGFyZ3NbJ3JlZiddIGFzIHN0cmluZ1xuICAgICAgfSk7XG5cbiAgICAgIGlmIChsYWJTaGVsbCkge1xuICAgICAgICBsYWJTaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICAvLyBJZiB0aGVyZSBpcyBvbmx5IGEgbGF1bmNoZXIgb3BlbiwgcmVtb3ZlIHRoZSBjbG9zZSBpY29uLlxuICAgICAgICAgIG1haW4udGl0bGUuY2xvc2FibGUgPSBBcnJheS5mcm9tKGxhYlNoZWxsLndpZGdldHMoJ21haW4nKSkubGVuZ3RoID4gMTtcbiAgICAgICAgfSwgbWFpbik7XG4gICAgICB9XG5cbiAgICAgIGlmIChkZWZhdWx0QnJvd3Nlcikge1xuICAgICAgICBjb25zdCBvblBhdGhDaGFuZ2VkID0gKG1vZGVsOiBGaWxlQnJvd3Nlck1vZGVsKSA9PiB7XG4gICAgICAgICAgbGF1bmNoZXIuY3dkID0gbW9kZWwucGF0aDtcbiAgICAgICAgfTtcbiAgICAgICAgZGVmYXVsdEJyb3dzZXIubW9kZWwucGF0aENoYW5nZWQuY29ubmVjdChvblBhdGhDaGFuZ2VkKTtcbiAgICAgICAgbGF1bmNoZXIuZGlzcG9zZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgICAgZGVmYXVsdEJyb3dzZXIubW9kZWwucGF0aENoYW5nZWQuZGlzY29ubmVjdChvblBhdGhDaGFuZ2VkKTtcbiAgICAgICAgfSk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBtYWluO1xuICAgIH1cbiAgfSk7XG5cbiAgaWYgKGxhYlNoZWxsKSB7XG4gICAgdm9pZCBQcm9taXNlLmFsbChbYXBwLnJlc3RvcmVkLCBkZWZhdWx0QnJvd3Nlcj8ubW9kZWwucmVzdG9yZWRdKS50aGVuKFxuICAgICAgKCkgPT4ge1xuICAgICAgICBmdW5jdGlvbiBtYXliZUNyZWF0ZSgpIHtcbiAgICAgICAgICAvLyBDcmVhdGUgYSBsYXVuY2hlciBpZiB0aGVyZSBhcmUgbm8gb3BlbiBpdGVtcy5cbiAgICAgICAgICBpZiAobGFiU2hlbGwhLmlzRW1wdHkoJ21haW4nKSkge1xuICAgICAgICAgICAgdm9pZCBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuY3JlYXRlKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgLy8gV2hlbiBsYXlvdXQgaXMgbW9kaWZpZWQsIGNyZWF0ZSBhIGxhdW5jaGVyIGlmIHRoZXJlIGFyZSBubyBvcGVuIGl0ZW1zLlxuICAgICAgICBsYWJTaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICBtYXliZUNyZWF0ZSgpO1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICApO1xuICB9XG5cbiAgaWYgKHBhbGV0dGUpIHtcbiAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgY29tbWFuZDogQ29tbWFuZElEcy5jcmVhdGUsXG4gICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ0xhdW5jaGVyJylcbiAgICB9KTtcbiAgfVxuXG4gIGlmIChsYWJTaGVsbCkge1xuICAgIGxhYlNoZWxsLmFkZEJ1dHRvbkVuYWJsZWQgPSB0cnVlO1xuICAgIGxhYlNoZWxsLmFkZFJlcXVlc3RlZC5jb25uZWN0KChzZW5kZXI6IERvY2tQYW5lbCwgYXJnOiBUYWJCYXI8V2lkZ2V0PikgPT4ge1xuICAgICAgLy8gR2V0IHRoZSByZWYgZm9yIHRoZSBjdXJyZW50IHRhYiBvZiB0aGUgdGFiYmFyIHdoaWNoIHRoZSBhZGQgYnV0dG9uIHdhcyBjbGlja2VkXG4gICAgICBjb25zdCByZWYgPVxuICAgICAgICBhcmcuY3VycmVudFRpdGxlPy5vd25lci5pZCB8fFxuICAgICAgICBhcmcudGl0bGVzW2FyZy50aXRsZXMubGVuZ3RoIC0gMV0ub3duZXIuaWQ7XG5cbiAgICAgIHJldHVybiBjb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMuY3JlYXRlLCB7IHJlZiB9KTtcbiAgICB9KTtcbiAgfVxuXG4gIHJldHVybiBtb2RlbDtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBtb2R1bGUgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBUaGUgaW5jcmVtZW50aW5nIGlkIHVzZWQgZm9yIGxhdW5jaGVyIHdpZGdldHMuXG4gICAqL1xuICBleHBvcnQgbGV0IGlkID0gMDtcbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==