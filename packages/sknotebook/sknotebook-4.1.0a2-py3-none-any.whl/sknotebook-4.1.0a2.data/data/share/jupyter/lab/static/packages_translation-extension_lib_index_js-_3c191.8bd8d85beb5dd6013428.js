"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_translation-extension_lib_index_js-_3c191"],{

/***/ "../packages/translation-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/translation-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* ----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module translation-extension
 */





/**
 * Translation plugins
 */
const PLUGIN_ID = '@jupyterlab/translation-extension:plugin';
const translator = {
    id: '@jupyterlab/translation:translator',
    description: 'Provides the application translation object.',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    provides: _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator,
    activate: async (app, paths, settings, labShell) => {
        const setting = await settings.load(PLUGIN_ID);
        const currentLocale = setting.get('locale').composite;
        let stringsPrefix = setting.get('stringsPrefix')
            .composite;
        const displayStringsPrefix = setting.get('displayStringsPrefix')
            .composite;
        stringsPrefix = displayStringsPrefix ? stringsPrefix : '';
        const serverSettings = app.serviceManager.serverSettings;
        const translationManager = new _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.TranslationManager(paths.urls.translations, stringsPrefix, serverSettings);
        await translationManager.fetch(currentLocale);
        // Set translator to UI
        if (labShell) {
            labShell.translator = translationManager;
        }
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.translator = translationManager;
        return translationManager;
    }
};
/**
 * Initialization data for the extension.
 */
const langMenu = {
    id: PLUGIN_ID,
    description: 'Adds translation commands and settings.',
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true,
    activate: (app, settings, translator, mainMenu, palette) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        let currentLocale;
        /**
         * Load the settings for this extension
         *
         * @param setting Extension settings
         */
        function loadSetting(setting) {
            // Read the settings and convert to the correct type
            currentLocale = setting.get('locale').composite;
        }
        settings
            .load(PLUGIN_ID)
            .then(setting => {
            var _a;
            // Read the settings
            loadSetting(setting);
            // Ensure currentLocale is not 'default' which is not a valid language code
            if (currentLocale !== 'default') {
                document.documentElement.lang = (currentLocale !== null && currentLocale !== void 0 ? currentLocale : '').replace('_', '-');
            }
            else {
                document.documentElement.lang = 'en-US';
            }
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
            // Create a languages menu
            const languagesMenu = mainMenu
                ? (_a = mainMenu.settingsMenu.items.find(item => {
                    var _a;
                    return item.type === 'submenu' &&
                        ((_a = item.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-settings-language';
                })) === null || _a === void 0 ? void 0 : _a.submenu
                : null;
            let command;
            const serverSettings = app.serviceManager.serverSettings;
            // Get list of available locales
            (0,_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.requestTranslationsAPI)('', '', {}, serverSettings)
                .then(data => {
                for (const locale in data['data']) {
                    const value = data['data'][locale];
                    const displayName = value.displayName;
                    const nativeName = value.nativeName;
                    const toggled = displayName === nativeName;
                    const label = toggled
                        ? `${displayName}`
                        : `${displayName} - ${nativeName}`;
                    // Add a command per language
                    command = `jupyterlab-translation:${locale}`;
                    commands.addCommand(command, {
                        label: label,
                        caption: label,
                        isEnabled: () => !toggled,
                        isVisible: () => true,
                        isToggled: () => toggled,
                        execute: () => {
                            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
                                title: trans.__('Change interface language?'),
                                body: trans.__('After changing the interface language to %1, you will need to reload JupyterLab to see the changes.', label),
                                buttons: [
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Cancel') }),
                                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: trans.__('Change and reload') })
                                ]
                            }).then(result => {
                                if (result.button.accept) {
                                    setting
                                        .set('locale', locale)
                                        .then(() => {
                                        window.location.reload();
                                    })
                                        .catch(reason => {
                                        console.error(reason);
                                    });
                                }
                            });
                        }
                    });
                    // Add the language command to the menu
                    if (languagesMenu) {
                        languagesMenu.addItem({
                            command,
                            args: {}
                        });
                    }
                    if (palette) {
                        palette.addItem({
                            category: trans.__('Display Languages'),
                            command
                        });
                    }
                }
            })
                .catch(reason => {
                console.error(`Available locales errored!\n${reason}`);
            });
        })
            .catch(reason => {
            console.error(`The jupyterlab translation extension appears to be missing.\n${reason}`);
        });
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [translator, langMenu];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdHJhbnNsYXRpb24tZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fM2MxOTEuOGJkOGQ4NWJlYjVkZDYwMTM0MjguanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFNOEI7QUFDMEM7QUFDMUI7QUFDYztBQUs5QjtBQUVqQzs7R0FFRztBQUNILE1BQU0sU0FBUyxHQUFHLDBDQUEwQyxDQUFDO0FBRTdELE1BQU0sVUFBVSxHQUF1QztJQUNyRCxFQUFFLEVBQUUsb0NBQW9DO0lBQ3hDLFdBQVcsRUFBRSw4Q0FBOEM7SUFDM0QsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FBQywyRUFBc0IsRUFBRSx5RUFBZ0IsQ0FBQztJQUNwRCxRQUFRLEVBQUUsQ0FBQyw4REFBUyxDQUFDO0lBQ3JCLFFBQVEsRUFBRSxnRUFBVztJQUNyQixRQUFRLEVBQUUsS0FBSyxFQUNiLEdBQW9CLEVBQ3BCLEtBQTZCLEVBQzdCLFFBQTBCLEVBQzFCLFFBQTBCLEVBQzFCLEVBQUU7UUFDRixNQUFNLE9BQU8sR0FBRyxNQUFNLFFBQVEsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLENBQUM7UUFDL0MsTUFBTSxhQUFhLEdBQVcsT0FBTyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQyxTQUFtQixDQUFDO1FBQ3hFLElBQUksYUFBYSxHQUFXLE9BQU8sQ0FBQyxHQUFHLENBQUMsZUFBZSxDQUFDO2FBQ3JELFNBQW1CLENBQUM7UUFDdkIsTUFBTSxvQkFBb0IsR0FBWSxPQUFPLENBQUMsR0FBRyxDQUFDLHNCQUFzQixDQUFDO2FBQ3RFLFNBQW9CLENBQUM7UUFDeEIsYUFBYSxHQUFHLG9CQUFvQixDQUFDLENBQUMsQ0FBQyxhQUFhLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQztRQUMxRCxNQUFNLGNBQWMsR0FBRyxHQUFHLENBQUMsY0FBYyxDQUFDLGNBQWMsQ0FBQztRQUN6RCxNQUFNLGtCQUFr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QUFRLENBQUMsTUFBTSxFQUFFLENBQUM7b0NBQzNCLENBQUMsQ0FBQzt5Q0FDRCxLQUFLLENBQUMsTUFBTSxDQUFDLEVBQUU7d0NBQ2QsT0FBTyxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUMsQ0FBQztvQ0FDeEIsQ0FBQyxDQUFDLENBQUM7aUNBQ047NEJBQ0gsQ0FBQyxDQUFDLENBQUM7d0JBQ0wsQ0FBQztxQkFDRixDQUFDLENBQUM7b0JBRUgsdUNBQXVDO29CQUN2QyxJQUFJLGFBQWEsRUFBRTt3QkFDakIsYUFBYSxDQUFDLE9BQU8sQ0FBQzs0QkFDcEIsT0FBTzs0QkFDUCxJQUFJLEVBQUUsRUFBRTt5QkFDVCxDQUFDLENBQUM7cUJBQ0o7b0JBRUQsSUFBSSxPQUFPLEVBQUU7d0JBQ1gsT0FBTyxDQUFDLE9BQU8sQ0FBQzs0QkFDZCxRQUFRLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxtQkFBbUIsQ0FBQzs0QkFDdkMsT0FBTzt5QkFDUixDQUFDLENBQUM7cUJBQ0o7aUJBQ0Y7WUFDSCxDQUFDLENBQUM7aUJBQ0QsS0FBSyxDQUFDLE1BQU0sQ0FBQyxFQUFFO2dCQUNkLE9BQU8sQ0FBQyxLQUFLLENBQUMsK0JBQStCLE1BQU0sRUFBRSxDQUFDLENBQUM7WUFDekQsQ0FBQyxDQUFDLENBQUM7UUFDUCxDQUFDLENBQUM7YUFDRCxLQUFLLENBQUMsTUFBTSxDQUFDLEVBQUU7WUFDZCxPQUFPLENBQUMsS0FBSyxDQUNYLGdFQUFnRSxNQUFNLEVBQUUsQ0FDekUsQ0FBQztRQUNKLENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQztDQUNGLENBQUM7QUFFRjs7R0FFRztBQUNILE1BQU0sT0FBTyxHQUFpQyxDQUFDLFVBQVUsRUFBRSxRQUFRLENBQUMsQ0FBQztBQUNyRSxpRUFBZSxPQUFPLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdHJhbnNsYXRpb24tZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdHJhbnNsYXRpb24tZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBEaWFsb2csIElDb21tYW5kUGFsZXR0ZSwgc2hvd0RpYWxvZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElNYWluTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL21haW5tZW51JztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIHJlcXVlc3RUcmFuc2xhdGlvbnNBUEksXG4gIFRyYW5zbGF0aW9uTWFuYWdlclxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogVHJhbnNsYXRpb24gcGx1Z2luc1xuICovXG5jb25zdCBQTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24tZXh0ZW5zaW9uOnBsdWdpbic7XG5cbmNvbnN0IHRyYW5zbGF0b3I6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJVHJhbnNsYXRvcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb246dHJhbnNsYXRvcicsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGFwcGxpY2F0aW9uIHRyYW5zbGF0aW9uIG9iamVjdC4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHJlcXVpcmVzOiBbSnVweXRlckZyb250RW5kLklQYXRocywgSVNldHRpbmdSZWdpc3RyeV0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsXSxcbiAgcHJvdmlkZXM6IElUcmFuc2xhdG9yLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHBhdGhzOiBKdXB5dGVyRnJvbnRFbmQuSVBhdGhzLFxuICAgIHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIGxhYlNoZWxsOiBJTGFiU2hlbGwgfCBudWxsXG4gICkgPT4ge1xuICAgIGNvbnN0IHNldHRpbmcgPSBhd2FpdCBzZXR0aW5ncy5sb2FkKFBMVUdJTl9JRCk7XG4gICAgY29uc3QgY3VycmVudExvY2FsZTogc3RyaW5nID0gc2V0dGluZy5nZXQoJ2xvY2FsZScpLmNvbXBvc2l0ZSBhcyBzdHJpbmc7XG4gICAgbGV0IHN0cmluZ3NQcmVmaXg6IHN0cmluZyA9IHNldHRpbmcuZ2V0KCdzdHJpbmdzUHJlZml4JylcbiAgICAgIC5jb21wb3NpdGUgYXMgc3RyaW5nO1xuICAgIGNvbnN0IGRpc3BsYXlTdHJpbmdzUHJlZml4OiBib29sZWFuID0gc2V0dGluZy5nZXQoJ2Rpc3BsYXlTdHJpbmdzUHJlZml4JylcbiAgICAgIC5jb21wb3NpdGUgYXMgYm9vbGVhbjtcbiAgICBzdHJpbmdzUHJlZml4ID0gZGlzcGxheVN0cmluZ3NQcmVmaXggPyBzdHJpbmdzUHJlZml4IDogJyc7XG4gICAgY29uc3Qgc2VydmVyU2V0dGluZ3MgPSBhcHAuc2VydmljZU1hbmFnZXIuc2VydmVyU2V0dGluZ3M7XG4gICAgY29uc3QgdHJhbnNsYXRpb25NYW5hZ2VyID0gbmV3IFRyYW5zbGF0aW9uTWFuYWdlcihcbiAgICAgIHBhdGhzLnVybHMudHJhbnNsYXRpb25zLFxuICAgICAgc3RyaW5nc1ByZWZpeCxcbiAgICAgIHNlcnZlclNldHRpbmdzXG4gICAgKTtcbiAgICBhd2FpdCB0cmFuc2xhdGlvbk1hbmFnZXIuZmV0Y2goY3VycmVudExvY2FsZSk7XG5cbiAgICAvLyBTZXQgdHJhbnNsYXRvciB0byBVSVxuICAgIGlmIChsYWJTaGVsbCkge1xuICAgICAgbGFiU2hlbGwudHJhbnNsYXRvciA9IHRyYW5zbGF0aW9uTWFuYWdlcjtcbiAgICB9XG5cbiAgICBEaWFsb2cudHJhbnNsYXRvciA9IHRyYW5zbGF0aW9uTWFuYWdlcjtcblxuICAgIHJldHVybiB0cmFuc2xhdGlvbk1hbmFnZXI7XG4gIH1cbn07XG5cbi8qKlxuICogSW5pdGlhbGl6YXRpb24gZGF0YSBmb3IgdGhlIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgbGFuZ01lbnU6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6IFBMVUdJTl9JRCxcbiAgZGVzY3JpcHRpb246ICdBZGRzIHRyYW5zbGF0aW9uIGNvbW1hbmRzIGFuZCBzZXR0aW5ncy4nLFxuICByZXF1aXJlczogW0lTZXR0aW5nUmVnaXN0cnksIElUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJTWFpbk1lbnUsIElDb21tYW5kUGFsZXR0ZV0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICBzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBtYWluTWVudTogSU1haW5NZW51IHwgbnVsbCxcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4gICkgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgeyBjb21tYW5kcyB9ID0gYXBwO1xuICAgIGxldCBjdXJyZW50TG9jYWxlOiBzdHJpbmc7XG4gICAgLyoqXG4gICAgICogTG9hZCB0aGUgc2V0dGluZ3MgZm9yIHRoaXMgZXh0ZW5zaW9uXG4gICAgICpcbiAgICAgKiBAcGFyYW0gc2V0dGluZyBFeHRlbnNpb24gc2V0dGluZ3NcbiAgICAgKi9cbiAgICBmdW5jdGlvbiBsb2FkU2V0dGluZyhzZXR0aW5nOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyk6IHZvaWQge1xuICAgICAgLy8gUmVhZCB0aGUgc2V0dGluZ3MgYW5kIGNvbnZlcnQgdG8gdGhlIGNvcnJlY3QgdHlwZVxuICAgICAgY3VycmVudExvY2FsZSA9IHNldHRpbmcuZ2V0KCdsb2NhbGUnKS5jb21wb3NpdGUgYXMgc3RyaW5nO1xuICAgIH1cblxuICAgIHNldHRpbmdzXG4gICAgICAubG9hZChQTFVHSU5fSUQpXG4gICAgICAudGhlbihzZXR0aW5nID0+IHtcbiAgICAgICAgLy8gUmVhZCB0aGUgc2V0dGluZ3NcbiAgICAgICAgbG9hZFNldHRpbmcoc2V0dGluZyk7XG5cbiAgICAgICAgLy8gRW5zdXJlIGN1cnJlbnRMb2NhbGUgaXMgbm90ICdkZWZhdWx0JyB3aGljaCBpcyBub3QgYSB2YWxpZCBsYW5ndWFnZSBjb2RlXG4gICAgICAgIGlmIChjdXJyZW50TG9jYWxlICE9PSAnZGVmYXVsdCcpIHtcbiAgICAgICAgICBkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQubGFuZyA9IChjdXJyZW50TG9jYWxlID8/ICcnKS5yZXBsYWNlKFxuICAgICAgICAgICAgJ18nLFxuICAgICAgICAgICAgJy0nXG4gICAgICAgICAgKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQubGFuZyA9ICdlbi1VUyc7XG4gICAgICAgIH1cblxuICAgICAgICAvLyBMaXN0ZW4gZm9yIHlvdXIgcGx1Z2luIHNldHRpbmcgY2hhbmdlcyB1c2luZyBTaWduYWxcbiAgICAgICAgc2V0dGluZy5jaGFuZ2VkLmNvbm5lY3QobG9hZFNldHRpbmcpO1xuXG4gICAgICAgIC8vIENyZWF0ZSBhIGxhbmd1YWdlcyBtZW51XG4gICAgICAgIGNvbnN0IGxhbmd1YWdlc01lbnUgPSBtYWluTWVudVxuICAgICAgICAgID8gbWFpbk1lbnUuc2V0dGluZ3NNZW51Lml0ZW1zLmZpbmQoXG4gICAgICAgICAgICAgIGl0ZW0gPT5cbiAgICAgICAgICAgICAgICBpdGVtLnR5cGUgPT09ICdzdWJtZW51JyAmJlxuICAgICAgICAgICAgICAgIGl0ZW0uc3VibWVudT8uaWQgPT09ICdqcC1tYWlubWVudS1zZXR0aW5ncy1sYW5ndWFnZSdcbiAgICAgICAgICAgICk/LnN1Ym1lbnVcbiAgICAgICAgICA6IG51bGw7XG5cbiAgICAgICAgbGV0IGNvbW1hbmQ6IHN0cmluZztcblxuICAgICAgICBjb25zdCBzZXJ2ZXJTZXR0aW5ncyA9IGFwcC5zZXJ2aWNlTWFuYWdlci5zZXJ2ZXJTZXR0aW5ncztcbiAgICAgICAgLy8gR2V0IGxpc3Qgb2YgYXZhaWxhYmxlIGxvY2FsZXNcbiAgICAgICAgcmVxdWVzdFRyYW5zbGF0aW9uc0FQSTxhbnk+KCcnLCAnJywge30sIHNlcnZlclNldHRpbmdzKVxuICAgICAgICAgIC50aGVuKGRhdGEgPT4ge1xuICAgICAgICAgICAgZm9yIChjb25zdCBsb2NhbGUgaW4gZGF0YVsnZGF0YSddKSB7XG4gICAgICAgICAgICAgIGNvbnN0IHZhbHVlID0gZGF0YVsnZGF0YSddW2xvY2FsZV07XG4gICAgICAgICAgICAgIGNvbnN0IGRpc3BsYXlOYW1lID0gdmFsdWUuZGlzcGxheU5hbWU7XG4gICAgICAgICAgICAgIGNvbnN0IG5hdGl2ZU5hbWUgPSB2YWx1ZS5uYXRpdmVOYW1lO1xuICAgICAgICAgICAgICBjb25zdCB0b2dnbGVkID0gZGlzcGxheU5hbWUgPT09IG5hdGl2ZU5hbWU7XG4gICAgICAgICAgICAgIGNvbnN0IGxhYmVsID0gdG9nZ2xlZFxuICAgICAgICAgICAgICAgID8gYCR7ZGlzcGxheU5hbWV9YFxuICAgICAgICAgICAgICAgIDogYCR7ZGlzcGxheU5hbWV9IC0gJHtuYXRpdmVOYW1lfWA7XG5cbiAgICAgICAgICAgICAgLy8gQWRkIGEgY29tbWFuZCBwZXIgbGFuZ3VhZ2VcbiAgICAgICAgICAgICAgY29tbWFuZCA9IGBqdXB5dGVybGFiLXRyYW5zbGF0aW9uOiR7bG9jYWxlfWA7XG4gICAgICAgICAgICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoY29tbWFuZCwge1xuICAgICAgICAgICAgICAgIGxhYmVsOiBsYWJlbCxcbiAgICAgICAgICAgICAgICBjYXB0aW9uOiBsYWJlbCxcbiAgICAgICAgICAgICAgICBpc0VuYWJsZWQ6ICgpID0+ICF0b2dnbGVkLFxuICAgICAgICAgICAgICAgIGlzVmlzaWJsZTogKCkgPT4gdHJ1ZSxcbiAgICAgICAgICAgICAgICBpc1RvZ2dsZWQ6ICgpID0+IHRvZ2dsZWQsXG4gICAgICAgICAgICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICAgICAgICAgICAgcmV0dXJuIHNob3dEaWFsb2coe1xuICAgICAgICAgICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0NoYW5nZSBpbnRlcmZhY2UgbGFuZ3VhZ2U/JyksXG4gICAgICAgICAgICAgICAgICAgIGJvZHk6IHRyYW5zLl9fKFxuICAgICAgICAgICAgICAgICAgICAgICdBZnRlciBjaGFuZ2luZyB0aGUgaW50ZXJmYWNlIGxhbmd1YWdlIHRvICUxLCB5b3Ugd2lsbCBuZWVkIHRvIHJlbG9hZCBKdXB5dGVyTGFiIHRvIHNlZSB0aGUgY2hhbmdlcy4nLFxuICAgICAgICAgICAgICAgICAgICAgIGxhYmVsXG4gICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICAgICAgICAgIGJ1dHRvbnM6IFtcbiAgICAgICAgICAgICAgICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdDYW5jZWwnKSB9KSxcbiAgICAgICAgICAgICAgICAgICAgICBEaWFsb2cub2tCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0NoYW5nZSBhbmQgcmVsb2FkJykgfSlcbiAgICAgICAgICAgICAgICAgICAgXVxuICAgICAgICAgICAgICAgICAgfSkudGhlbihyZXN1bHQgPT4ge1xuICAgICAgICAgICAgICAgICAgICBpZiAocmVzdWx0LmJ1dHRvbi5hY2NlcHQpIHtcbiAgICAgICAgICAgICAgICAgICAgICBzZXR0aW5nXG4gICAgICAgICAgICAgICAgICAgICAgICAuc2V0KCdsb2NhbGUnLCBsb2NhbGUpXG4gICAgICAgICAgICAgICAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5yZWxvYWQoKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgICAgICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5lcnJvcihyZWFzb24pO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfSk7XG5cbiAgICAgICAgICAgICAgLy8gQWRkIHRoZSBsYW5ndWFnZSBjb21tYW5kIHRvIHRoZSBtZW51XG4gICAgICAgICAgICAgIGlmIChsYW5ndWFnZXNNZW51KSB7XG4gICAgICAgICAgICAgICAgbGFuZ3VhZ2VzTWVudS5hZGRJdGVtKHtcbiAgICAgICAgICAgICAgICAgIGNvbW1hbmQsXG4gICAgICAgICAgICAgICAgICBhcmdzOiB7fVxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICB9XG5cbiAgICAgICAgICAgICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgICAgICAgICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICAgICAgICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdEaXNwbGF5IExhbmd1YWdlcycpLFxuICAgICAgICAgICAgICAgICAgY29tbWFuZFxuICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSlcbiAgICAgICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgICAgIGNvbnNvbGUuZXJyb3IoYEF2YWlsYWJsZSBsb2NhbGVzIGVycm9yZWQhXFxuJHtyZWFzb259YCk7XG4gICAgICAgICAgfSk7XG4gICAgICB9KVxuICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgIGNvbnNvbGUuZXJyb3IoXG4gICAgICAgICAgYFRoZSBqdXB5dGVybGFiIHRyYW5zbGF0aW9uIGV4dGVuc2lvbiBhcHBlYXJzIHRvIGJlIG1pc3NpbmcuXFxuJHtyZWFzb259YFxuICAgICAgICApO1xuICAgICAgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbdHJhbnNsYXRvciwgbGFuZ01lbnVdO1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2lucztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==