"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_hub-extension_lib_index_js-_92651"],{

/***/ "../packages/hub-extension/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/hub-extension/lib/index.js ***!
  \**********************************************/
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
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module hub-extension
 */




/**
 * The command IDs used by the plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.controlPanel = 'hub:control-panel';
    CommandIDs.logout = 'hub:logout';
    CommandIDs.restart = 'hub:restart';
})(CommandIDs || (CommandIDs = {}));
/**
 * Activate the jupyterhub extension.
 */
function activateHubExtension(app, paths, translator, palette) {
    const trans = translator.load('jupyterlab');
    const hubHost = paths.urls.hubHost || '';
    const hubPrefix = paths.urls.hubPrefix || '';
    const hubUser = paths.urls.hubUser || '';
    const hubServerName = paths.urls.hubServerName || '';
    const baseUrl = paths.urls.base;
    // Bail if not running on JupyterHub.
    if (!hubPrefix) {
        return;
    }
    console.debug('hub-extension: Found configuration ', {
        hubHost: hubHost,
        hubPrefix: hubPrefix
    });
    // If hubServerName is set, use JupyterHub 1.0 URL.
    const restartUrl = hubServerName
        ? hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'spawn', hubUser, hubServerName)
        : hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'spawn');
    const { commands } = app;
    commands.addCommand(CommandIDs.restart, {
        label: trans.__('Restart Server'),
        caption: trans.__('Request that the Hub restart this server'),
        execute: () => {
            window.open(restartUrl, '_blank');
        }
    });
    commands.addCommand(CommandIDs.controlPanel, {
        label: trans.__('Hub Control Panel'),
        caption: trans.__('Open the Hub control panel in a new browser tab'),
        execute: () => {
            window.open(hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(hubPrefix, 'home'), '_blank');
        }
    });
    commands.addCommand(CommandIDs.logout, {
        label: trans.__('Log Out'),
        caption: trans.__('Log out of the Hub'),
        execute: () => {
            window.location.href = hubHost + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(baseUrl, 'logout');
        }
    });
    // Add palette items.
    if (palette) {
        const category = trans.__('Hub');
        palette.addItem({ category, command: CommandIDs.controlPanel });
        palette.addItem({ category, command: CommandIDs.logout });
    }
}
/**
 * Initialization data for the hub-extension.
 */
const hubExtension = {
    activate: activateHubExtension,
    id: '@jupyterlab/hub-extension:plugin',
    description: 'Registers commands related to the hub server',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true
};
/**
 * Plugin to load menu description based on settings file
 */
const hubExtensionMenu = {
    activate: () => void 0,
    id: '@jupyterlab/hub-extension:menu',
    description: 'Adds hub related commands to the menu.',
    autoStart: true
};
/**
 * The default JupyterLab connection lost provider. This may be overridden
 * to provide custom behavior when a connection to the server is lost.
 *
 * If the application is being deployed within a JupyterHub context,
 * this will provide a dialog that prompts the user to restart the server.
 * Otherwise, it shows an error dialog.
 */
const connectionlost = {
    id: '@jupyterlab/hub-extension:connectionlost',
    description: 'Provides a service to be notified when the connection to the hub server is lost.',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterLab.IInfo],
    activate: (app, paths, translator, info) => {
        const trans = translator.load('jupyterlab');
        const hubPrefix = paths.urls.hubPrefix || '';
        const baseUrl = paths.urls.base;
        // Return the default error message if not running on JupyterHub.
        if (!hubPrefix) {
            return _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ConnectionLost;
        }
        // If we are running on JupyterHub, return a dialog
        // that prompts the user to restart their server.
        let showingError = false;
        const onConnectionLost = async (manager, err) => {
            if (showingError) {
                return;
            }
            showingError = true;
            if (info) {
                info.isConnected = false;
            }
            const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                title: trans.__('Server unavailable or unreachable'),
                body: trans.__('Your server at %1 is not running.\nWould you like to restart it?', baseUrl),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Restart') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Dismiss') })
                ]
            });
            if (info) {
                info.isConnected = true;
            }
            showingError = false;
            if (result.button.accept) {
                await app.commands.execute(CommandIDs.restart);
            }
        };
        return onConnectionLost;
    },
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IConnectionLost
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    hubExtension,
    hubExtensionMenu,
    connectionlost
]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaHViLWV4dGVuc2lvbl9saWJfaW5kZXhfanMtXzkyNjUxLmQ2YjY3YTAwZmM2YWYxYjQ0OThlLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFROEI7QUFDMEM7QUFDNUI7QUFFTztBQUV0RDs7R0FFRztBQUNJLElBQVUsVUFBVSxDQU0xQjtBQU5ELFdBQWlCLFVBQVU7SUFDWix1QkFBWSxHQUFXLG1CQUFtQixDQUFDO0lBRTNDLGlCQUFNLEdBQVcsWUFBWSxDQUFDO0lBRTlCLGtCQUFPLEdBQVcsYUFBYSxDQUFDO0FBQy9DLENBQUMsRUFOZ0IsVUFBVSxLQUFWLFVBQVUsUUFNMUI7QUFFRDs7R0FFRztBQUNILFNBQVMsb0JBQW9CLENBQzNCLEdBQW9CLEVBQ3BCLEtBQTZCLEVBQzdCLFVBQXVCLEVBQ3ZCLE9BQStCO0lBRS9CLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7SUFDNUMsTUFBTSxPQUFPLEdBQUcsS0FBSyxDQUFDLElBQUksQ0FBQyxPQUFPLElBQUksRUFBRSxDQUFDO0lBQ3pDLE1BQU0sU0FBUyxHQUFHLEtBQUssQ0FBQyxJQUFJLENBQUMsU0FBUyxJQUFJLEVBQUUsQ0FBQztJQUM3QyxNQUFNLE9BQU8sR0FBRyxLQUFLLENBQUMsSUFBSSxDQUFDLE9BQU8sSUFBSSxFQUFFLENBQUM7SUFDekMsTUFBTSxhQUFhLEdBQUcsS0FBSyxDQUFDLElBQUksQ0FBQyxhQUFhLElBQUksRUFBRSxDQUFDO0lBQ3JELE1BQU0sT0FBTyxHQUFHLEtBQUssQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDO0lBRWhDLHFDQUFxQztJQUNyQyxJQUFJLENBQUMsU0FBUyxFQUFFO1FBQ2QsT0FBTztLQUNSO0lBRUQsT0FBTyxDQUFDLEtBQUssQ0FBQyxxQ0FBcUMsRUFBRTtRQUNuRCxPQUFPLEVBQUUsT0FBTztRQUNoQixTQUFTLEVBQUUsU0FB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O1lBRUgsSUFBSSxJQUFJLEVBQUU7Z0JBQ1IsSUFBSSxDQUFDLFdBQVcsR0FBRyxJQUFJLENBQUM7YUFDekI7WUFDRCxZQUFZLEdBQUcsS0FBSyxDQUFDO1lBRXJCLElBQUksTUFBTSxDQUFDLE1BQU0sQ0FBQyxNQUFNLEVBQUU7Z0JBQ3hCLE1BQU0sR0FBRyxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsVUFBVSxDQUFDLE9BQU8sQ0FBQyxDQUFDO2FBQ2hEO1FBQ0gsQ0FBQyxDQUFDO1FBQ0YsT0FBTyxnQkFBZ0IsQ0FBQztJQUMxQixDQUFDO0lBQ0QsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsb0VBQWU7Q0FDMUIsQ0FBQztBQUVGLGlFQUFlO0lBQ2IsWUFBWTtJQUNaLGdCQUFnQjtJQUNoQixjQUFjO0NBQ2lCLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaHViLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBodWItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgQ29ubmVjdGlvbkxvc3QsXG4gIElDb25uZWN0aW9uTG9zdCxcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW4sXG4gIEp1cHl0ZXJMYWJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgRGlhbG9nLCBJQ29tbWFuZFBhbGV0dGUsIHNob3dEaWFsb2cgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBVUkxFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgU2VydmVyQ29ubmVjdGlvbiwgU2VydmljZU1hbmFnZXIgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgcGx1Z2luLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgY29udHJvbFBhbmVsOiBzdHJpbmcgPSAnaHViOmNvbnRyb2wtcGFuZWwnO1xuXG4gIGV4cG9ydCBjb25zdCBsb2dvdXQ6IHN0cmluZyA9ICdodWI6bG9nb3V0JztcblxuICBleHBvcnQgY29uc3QgcmVzdGFydDogc3RyaW5nID0gJ2h1YjpyZXN0YXJ0Jztcbn1cblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUganVweXRlcmh1YiBleHRlbnNpb24uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlSHViRXh0ZW5zaW9uKFxuICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgcGF0aHM6IEp1cHl0ZXJGcm9udEVuZC5JUGF0aHMsXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4pOiB2b2lkIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgaHViSG9zdCA9IHBhdGhzLnVybHMuaHViSG9zdCB8fCAnJztcbiAgY29uc3QgaHViUHJlZml4ID0gcGF0aHMudXJscy5odWJQcmVmaXggfHwgJyc7XG4gIGNvbnN0IGh1YlVzZXIgPSBwYXRocy51cmxzLmh1YlVzZXIgfHwgJyc7XG4gIGNvbnN0IGh1YlNlcnZlck5hbWUgPSBwYXRocy51cmxzLmh1YlNlcnZlck5hbWUgfHwgJyc7XG4gIGNvbnN0IGJhc2VVcmwgPSBwYXRocy51cmxzLmJhc2U7XG5cbiAgLy8gQmFpbCBpZiBub3QgcnVubmluZyBvbiBKdXB5dGVySHViLlxuICBpZiAoIWh1YlByZWZpeCkge1xuICAgIHJldHVybjtcbiAgfVxuXG4gIGNvbnNvbGUuZGVidWcoJ2h1Yi1leHRlbnNpb246IEZvdW5kIGNvbmZpZ3VyYXRpb24gJywge1xuICAgIGh1Ykhvc3Q6IGh1Ykhvc3QsXG4gICAgaHViUHJlZml4OiBodWJQcmVmaXhcbiAgfSk7XG5cbiAgLy8gSWYgaHViU2VydmVyTmFtZSBpcyBzZXQsIHVzZSBKdXB5dGVySHViIDEuMCBVUkwuXG4gIGNvbnN0IHJlc3RhcnRVcmwgPSBodWJTZXJ2ZXJOYW1lXG4gICAgPyBodWJIb3N0ICsgVVJMRXh0LmpvaW4oaHViUHJlZml4LCAnc3Bhd24nLCBodWJVc2VyLCBodWJTZXJ2ZXJOYW1lKVxuICAgIDogaHViSG9zdCArIFVSTEV4dC5qb2luKGh1YlByZWZpeCwgJ3NwYXduJyk7XG5cbiAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5yZXN0YXJ0LCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSZXN0YXJ0IFNlcnZlcicpLFxuICAgIGNhcHRpb246IHRyYW5zLl9fKCdSZXF1ZXN0IHRoYXQgdGhlIEh1YiByZXN0YXJ0IHRoaXMgc2VydmVyJyksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgd2luZG93Lm9wZW4ocmVzdGFydFVybCwgJ19ibGFuaycpO1xuICAgIH1cbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmNvbnRyb2xQYW5lbCwge1xuICAgIGxhYmVsOiB0cmFucy5fXygnSHViIENvbnRyb2wgUGFuZWwnKSxcbiAgICBjYXB0aW9uOiB0cmFucy5fXygnT3BlbiB0aGUgSHViIGNvbnRyb2wgcGFuZWwgaW4gYSBuZXcgYnJvd3NlciB0YWInKSxcbiAgICBleGVjdXRlOiAoKSA9PiB7XG4gICAgICB3aW5kb3cub3BlbihodWJIb3N0ICsgVVJMRXh0LmpvaW4oaHViUHJlZml4LCAnaG9tZScpLCAnX2JsYW5rJyk7XG4gICAgfVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMubG9nb3V0LCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdMb2cgT3V0JyksXG4gICAgY2FwdGlvbjogdHJhbnMuX18oJ0xvZyBvdXQgb2YgdGhlIEh1YicpLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIHdpbmRvdy5sb2NhdGlvbi5ocmVmID0gaHViSG9zdCArIFVSTEV4dC5qb2luKGJhc2VVcmwsICdsb2dvdXQnKTtcbiAgICB9XG4gIH0pO1xuXG4gIC8vIEFkZCBwYWxldHRlIGl0ZW1zLlxuICBpZiAocGFsZXR0ZSkge1xuICAgIGNvbnN0IGNhdGVnb3J5ID0gdHJhbnMuX18oJ0h1YicpO1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNhdGVnb3J5LCBjb21tYW5kOiBDb21tYW5kSURzLmNvbnRyb2xQYW5lbCB9KTtcbiAgICBwYWxldHRlLmFkZEl0ZW0oeyBjYXRlZ29yeSwgY29tbWFuZDogQ29tbWFuZElEcy5sb2dvdXQgfSk7XG4gIH1cbn1cblxuLyoqXG4gKiBJbml0aWFsaXphdGlvbiBkYXRhIGZvciB0aGUgaHViLWV4dGVuc2lvbi5cbiAqL1xuY29uc3QgaHViRXh0ZW5zaW9uOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGFjdGl2YXRlOiBhY3RpdmF0ZUh1YkV4dGVuc2lvbixcbiAgaWQ6ICdAanVweXRlcmxhYi9odWItZXh0ZW5zaW9uOnBsdWdpbicsXG4gIGRlc2NyaXB0aW9uOiAnUmVnaXN0ZXJzIGNvbW1hbmRzIHJlbGF0ZWQgdG8gdGhlIGh1YiBzZXJ2ZXInLFxuICByZXF1aXJlczogW0p1cHl0ZXJGcm9udEVuZC5JUGF0aHMsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJQ29tbWFuZFBhbGV0dGVdLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogUGx1Z2luIHRvIGxvYWQgbWVudSBkZXNjcmlwdGlvbiBiYXNlZCBvbiBzZXR0aW5ncyBmaWxlXG4gKi9cbmNvbnN0IGh1YkV4dGVuc2lvbk1lbnU6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgYWN0aXZhdGU6ICgpID0+IHZvaWQgMCxcbiAgaWQ6ICdAanVweXRlcmxhYi9odWItZXh0ZW5zaW9uOm1lbnUnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgaHViIHJlbGF0ZWQgY29tbWFuZHMgdG8gdGhlIG1lbnUuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IEp1cHl0ZXJMYWIgY29ubmVjdGlvbiBsb3N0IHByb3ZpZGVyLiBUaGlzIG1heSBiZSBvdmVycmlkZGVuXG4gKiB0byBwcm92aWRlIGN1c3RvbSBiZWhhdmlvciB3aGVuIGEgY29ubmVjdGlvbiB0byB0aGUgc2VydmVyIGlzIGxvc3QuXG4gKlxuICogSWYgdGhlIGFwcGxpY2F0aW9uIGlzIGJlaW5nIGRlcGxveWVkIHdpdGhpbiBhIEp1cHl0ZXJIdWIgY29udGV4dCxcbiAqIHRoaXMgd2lsbCBwcm92aWRlIGEgZGlhbG9nIHRoYXQgcHJvbXB0cyB0aGUgdXNlciB0byByZXN0YXJ0IHRoZSBzZXJ2ZXIuXG4gKiBPdGhlcndpc2UsIGl0IHNob3dzIGFuIGVycm9yIGRpYWxvZy5cbiAqL1xuY29uc3QgY29ubmVjdGlvbmxvc3Q6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJQ29ubmVjdGlvbkxvc3Q+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2h1Yi1leHRlbnNpb246Y29ubmVjdGlvbmxvc3QnLFxuICBkZXNjcmlwdGlvbjpcbiAgICAnUHJvdmlkZXMgYSBzZXJ2aWNlIHRvIGJlIG5vdGlmaWVkIHdoZW4gdGhlIGNvbm5lY3Rpb24gdG8gdGhlIGh1YiBzZXJ2ZXIgaXMgbG9zdC4nLFxuICByZXF1aXJlczogW0p1cHl0ZXJGcm9udEVuZC5JUGF0aHMsIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtKdXB5dGVyTGFiLklJbmZvXSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBwYXRoczogSnVweXRlckZyb250RW5kLklQYXRocyxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBpbmZvOiBKdXB5dGVyTGFiLklJbmZvIHwgbnVsbFxuICApOiBJQ29ubmVjdGlvbkxvc3QgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgaHViUHJlZml4ID0gcGF0aHMudXJscy5odWJQcmVmaXggfHwgJyc7XG4gICAgY29uc3QgYmFzZVVybCA9IHBhdGhzLnVybHMuYmFzZTtcblxuICAgIC8vIFJldHVybiB0aGUgZGVmYXVsdCBlcnJvciBtZXNzYWdlIGlmIG5vdCBydW5uaW5nIG9uIEp1cHl0ZXJIdWIuXG4gICAgaWYgKCFodWJQcmVmaXgpIHtcbiAgICAgIHJldHVybiBDb25uZWN0aW9uTG9zdDtcbiAgICB9XG5cbiAgICAvLyBJZiB3ZSBhcmUgcnVubmluZyBvbiBKdXB5dGVySHViLCByZXR1cm4gYSBkaWFsb2dcbiAgICAvLyB0aGF0IHByb21wdHMgdGhlIHVzZXIgdG8gcmVzdGFydCB0aGVpciBzZXJ2ZXIuXG4gICAgbGV0IHNob3dpbmdFcnJvciA9IGZhbHNlO1xuICAgIGNvbnN0IG9uQ29ubmVjdGlvbkxvc3Q6IElDb25uZWN0aW9uTG9zdCA9IGFzeW5jIChcbiAgICAgIG1hbmFnZXI6IFNlcnZpY2VNYW5hZ2VyLklNYW5hZ2VyLFxuICAgICAgZXJyOiBTZXJ2ZXJDb25uZWN0aW9uLk5ldHdvcmtFcnJvclxuICAgICk6IFByb21pc2U8dm9pZD4gPT4ge1xuICAgICAgaWYgKHNob3dpbmdFcnJvcikge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG5cbiAgICAgIHNob3dpbmdFcnJvciA9IHRydWU7XG4gICAgICBpZiAoaW5mbykge1xuICAgICAgICBpbmZvLmlzQ29ubmVjdGVkID0gZmFsc2U7XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHNob3dEaWFsb2coe1xuICAgICAgICB0aXRsZTogdHJhbnMuX18oJ1NlcnZlciB1bmF2YWlsYWJsZSBvciB1bnJlYWNoYWJsZScpLFxuICAgICAgICBib2R5OiB0cmFucy5fXyhcbiAgICAgICAgICAnWW91ciBzZXJ2ZXIgYXQgJTEgaXMgbm90IHJ1bm5pbmcuXFxuV291bGQgeW91IGxpa2UgdG8gcmVzdGFydCBpdD8nLFxuICAgICAgICAgIGJhc2VVcmxcbiAgICAgICAgKSxcbiAgICAgICAgYnV0dG9uczogW1xuICAgICAgICAgIERpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnUmVzdGFydCcpIH0pLFxuICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0Rpc21pc3MnKSB9KVxuICAgICAgICBdXG4gICAgICB9KTtcblxuICAgICAgaWYgKGluZm8pIHtcbiAgICAgICAgaW5mby5pc0Nvbm5lY3RlZCA9IHRydWU7XG4gICAgICB9XG4gICAgICBzaG93aW5nRXJyb3IgPSBmYWxzZTtcblxuICAgICAgaWYgKHJlc3VsdC5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgIGF3YWl0IGFwcC5jb21tYW5kcy5leGVjdXRlKENvbW1hbmRJRHMucmVzdGFydCk7XG4gICAgICB9XG4gICAgfTtcbiAgICByZXR1cm4gb25Db25uZWN0aW9uTG9zdDtcbiAgfSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSUNvbm5lY3Rpb25Mb3N0XG59O1xuXG5leHBvcnQgZGVmYXVsdCBbXG4gIGh1YkV4dGVuc2lvbixcbiAgaHViRXh0ZW5zaW9uTWVudSxcbiAgY29ubmVjdGlvbmxvc3Rcbl0gYXMgSnVweXRlckZyb250RW5kUGx1Z2luPGFueT5bXTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==