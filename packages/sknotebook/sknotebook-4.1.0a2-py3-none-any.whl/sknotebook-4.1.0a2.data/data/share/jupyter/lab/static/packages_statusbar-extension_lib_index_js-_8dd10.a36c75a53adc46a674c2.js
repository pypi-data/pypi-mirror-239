"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_statusbar-extension_lib_index_js-_8dd10"],{

/***/ "../packages/statusbar-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/statusbar-extension/lib/index.js ***!
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
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module statusbar-extension
 */





const STATUSBAR_PLUGIN_ID = '@jupyterlab/statusbar-extension:plugin';
/**
 * Initialization data for the statusbar extension.
 */
const statusBar = {
    id: STATUSBAR_PLUGIN_ID,
    description: 'Provides the application status bar.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    provides: _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__.IStatusBar,
    autoStart: true,
    activate: (app, translator, labShell, settingRegistry, palette) => {
        const trans = translator.load('jupyterlab');
        const statusBar = new _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_3__.StatusBar();
        statusBar.id = 'jp-main-statusbar';
        app.shell.add(statusBar, 'bottom');
        // If available, connect to the shell's layout modified signal.
        if (labShell) {
            labShell.layoutModified.connect(() => {
                statusBar.update();
            });
        }
        const category = trans.__('Main Area');
        const command = 'statusbar:toggle';
        app.commands.addCommand(command, {
            label: trans.__('Show Status Bar'),
            execute: () => {
                statusBar.setHidden(statusBar.isVisible);
                if (settingRegistry) {
                    void settingRegistry.set(STATUSBAR_PLUGIN_ID, 'visible', statusBar.isVisible);
                }
            },
            isToggled: () => statusBar.isVisible
        });
        app.commands.commandExecuted.connect((registry, executed) => {
            if (executed.id === 'application:reset-layout' && !statusBar.isVisible) {
                app.commands.execute(command).catch(reason => {
                    console.error('Failed to show the status bar.', reason);
                });
            }
        });
        if (palette) {
            palette.addItem({ command, category });
        }
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(STATUSBAR_PLUGIN_ID);
            const updateSettings = (settings) => {
                const visible = settings.get('visible').composite;
                statusBar.setHidden(!visible);
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
        return statusBar;
    },
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette]
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (statusBar);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfc3RhdHVzYmFyLWV4dGVuc2lvbl9saWJfaW5kZXhfanMtXzhkZDEwLmEzNmM3NWE1M2FkYzQ2YTY3NGMyLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDc0I7QUFDUTtBQUNEO0FBQ1I7QUFFdEQsTUFBTSxtQkFBbUIsR0FBRyx3Q0FBd0MsQ0FBQztBQUVyRTs7R0FFRztBQUNILE1BQU0sU0FBUyxHQUFzQztJQUNuRCxFQUFFLEVBQUUsbUJBQW1CO0lBQ3ZCLFdBQVcsRUFBRSxzQ0FBc0M7SUFDbkQsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUUsNkRBQVU7SUFDcEIsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixVQUF1QixFQUN2QixRQUEwQixFQUMxQixlQUF3QyxFQUN4QyxPQUErQixFQUMvQixFQUFFO1FBQ0YsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxNQUFNLFNBQVMsR0FBRyxJQUFJLDREQUFTLEVBQUUsQ0FBQztRQUNsQyxTQUFTLENBQUMsRUFBRSxHQUFHLG1CQUFtQixDQUFDO1FBQ25DLEdBQUcsQ0FBQyxLQUFLLENBQUMsR0FBRyxDQUFDLFNBQVMsRUFBRSxRQUFRLENBQUMsQ0FBQztRQUVuQywrREFBK0Q7UUFDL0QsSUFBSSxRQUFRLEVBQUU7WUFDWixRQUFRLENBQUMsY0FBYyxDQUFDLE9BQU8sQ0FBQyxHQUFHLEVBQUU7Z0JBQ25DLFNBQVMsQ0FBQyxNQUFNLEVBQUUsQ0FBQztZQUNyQixDQUFDLENBQUMsQ0FBQztTQUNKO1FBRUQsTUFBTSxRQUFRLEdBQVcsS0FBSyxDQUFDLEVBQUUsQ0FBQyxXQUFXLENBQUMsQ0FBQztRQUMvQyxNQUFNLE9BQU8sR0FBVyxrQkFBa0IsQ0FBQztRQUUzQyxHQUFHLENBQUMsUUFBUSxDQUFDLFVBQVUsQ0FBQyxPQUFPLEVBQUU7WUFDL0IsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsaUJBQWlCLENBQUM7WUFDbEMsT0FBTyxFQUFFLEdBQUcsRUFBRTtnQkFDWixTQUFTLENBQUMsU0FBUyxDQUFDLFNBQVMsQ0FBQyxTQUFTLENBQUMsQ0FBQztnQkFDekMsSUFBSSxlQUFlLEVBQUU7b0JBQ25CLEtBQUssZUFBZSxDQUFDLEdBQUcsQ0FDdEIsbUJBQW1CLEVBQ25CLFNBQVMsRUFDVCxTQUFTLENBQUMsU0FBUyxDQUNwQixDQUFDO2lCQUNIO1lBQ0gsQ0FBQztZQUNELFNBQVMsRUFBRSxHQUFHLEVBQUUsQ0FBQyxTQUFTLENBQUMsU0FBUztTQUNyQyxDQUFDLENBQUM7UUFFSCxHQUFHLENBQUMsUUFBUSxDQUFDLGVBQWUsQ0FBQyxPQUFPLENBQUMsQ0FBQyxRQUFRLEVBQUUsUUFBUSxFQUFFLEVBQUU7WUFDMUQsSUFBSSxRQUFRLENBQUMsRUFBRSxLQUFLLDBCQUEwQixJQUFJLENBQUMsU0FBUyxDQUFDLFNBQVMsRUFBRTtnQkFDdEUsR0FBRyxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLENBQUMsS0FBSyxDQUFDLE1BQU0sQ0FBQyxFQUFFO29CQUMzQyxPQUFPLENBQUMsS0FBSyxDQUFDLGdDQUFnQyxFQUFFLE1BQU0sQ0FBQyxDQUFDO2dCQUMxRCxDQUFDLENBQUMsQ0FBQzthQUNKO1FBQ0gsQ0FBQyxDQUFDLENBQUM7UUFFSCxJQUFJLE9BQU8sRUFBRTtZQUNYLE9BQU8sQ0FBQyxPQUFPLENBQUMsRUFBRSxPQUFPLEVBQUUsUUFBUSxFQUFFLENBQUMsQ0FBQztTQUN4QztRQUVELElBQUksZUFBZSxFQUFFO1lBQ25CLE1BQU0sWUFBWSxHQUFHLGVBQWUsQ0FBQyxJQUFJLENBQUMsbUJBQW1CLENBQUMsQ0FBQztZQUMvRCxNQUFNLGNBQWMsR0FBRyxDQUFDLFFBQW9DLEVBQVEsRUFBRTtnQkFDcEUsTUFBTSxPQUFPLEdBQUcsUUFBUSxDQUFDLEdBQUcsQ0FBQyxTQUFTLENBQUMsQ0FBQyxTQUFvQixDQUFDO2dCQUM3RCxTQUFTLENBQUMsU0FBUyxDQUFDLENBQUMsT0FBTyxDQUFDLENBQUM7WUFDaEMsQ0FBQyxDQUFDO1lBRUYsT0FBTyxDQUFDLEdBQUcsQ0FBQyxDQUFDLFlBQVksRUFBRSxHQUFHLENBQUMsUUFBUSxDQUFDLENBQUM7aUJBQ3RDLElBQUksQ0FBQyxDQUFDLENBQUMsUUFBUSxDQUFDLEVBQUUsRUFBRTtnQkFDbkIsY0FBYyxDQUFDLFFBQVEsQ0FBQyxDQUFDO2dCQUN6QixRQUFRLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUMsRUFBRTtvQkFDbEMsY0FBYyxDQUFDLFFBQVEsQ0FBQyxDQUFDO2dCQUMzQixDQUFDLENBQUMsQ0FBQztZQUNMLENBQUMsQ0FBQztpQkFDRCxLQUFLLENBQUMsQ0FBQyxNQUFhLEVBQUUsRUFBRTtnQkFDdkIsT0FBTyxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLENBQUM7WUFDaEMsQ0FBQyxDQUFDLENBQUM7U0FDTjtRQUVELE9BQU8sU0FBUyxDQUFDO0lBQ25CLENBQUM7SUFDRCxRQUFRLEVBQUUsQ0FBQyw4REFBUyxFQUFFLHlFQUFnQixFQUFFLGlFQUFlLENBQUM7Q0FDekQsQ0FBQztBQUVGLGlFQUFlLFNBQVMsRUFBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBzdGF0dXNiYXItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlNoZWxsLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJQ29tbWFuZFBhbGV0dGUgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElTdGF0dXNCYXIsIFN0YXR1c0JhciB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXR1c2Jhcic7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxuY29uc3QgU1RBVFVTQkFSX1BMVUdJTl9JRCA9ICdAanVweXRlcmxhYi9zdGF0dXNiYXItZXh0ZW5zaW9uOnBsdWdpbic7XG5cbi8qKlxuICogSW5pdGlhbGl6YXRpb24gZGF0YSBmb3IgdGhlIHN0YXR1c2JhciBleHRlbnNpb24uXG4gKi9cbmNvbnN0IHN0YXR1c0JhcjogSnVweXRlckZyb250RW5kUGx1Z2luPElTdGF0dXNCYXI+ID0ge1xuICBpZDogU1RBVFVTQkFSX1BMVUdJTl9JRCxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgYXBwbGljYXRpb24gc3RhdHVzIGJhci4nLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgcHJvdmlkZXM6IElTdGF0dXNCYXIsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgICBsYWJTaGVsbDogSUxhYlNoZWxsIHwgbnVsbCxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBzdGF0dXNCYXIgPSBuZXcgU3RhdHVzQmFyKCk7XG4gICAgc3RhdHVzQmFyLmlkID0gJ2pwLW1haW4tc3RhdHVzYmFyJztcbiAgICBhcHAuc2hlbGwuYWRkKHN0YXR1c0JhciwgJ2JvdHRvbScpO1xuXG4gICAgLy8gSWYgYXZhaWxhYmxlLCBjb25uZWN0IHRvIHRoZSBzaGVsbCdzIGxheW91dCBtb2RpZmllZCBzaWduYWwuXG4gICAgaWYgKGxhYlNoZWxsKSB7XG4gICAgICBsYWJTaGVsbC5sYXlvdXRNb2RpZmllZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgc3RhdHVzQmFyLnVwZGF0ZSgpO1xuICAgICAgfSk7XG4gICAgfVxuXG4gICAgY29uc3QgY2F0ZWdvcnk6IHN0cmluZyA9IHRyYW5zLl9fKCdNYWluIEFyZWEnKTtcbiAgICBjb25zdCBjb21tYW5kOiBzdHJpbmcgPSAnc3RhdHVzYmFyOnRvZ2dsZSc7XG5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChjb21tYW5kLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgU3RhdHVzIEJhcicpLFxuICAgICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgICBzdGF0dXNCYXIuc2V0SGlkZGVuKHN0YXR1c0Jhci5pc1Zpc2libGUpO1xuICAgICAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICAgICAgdm9pZCBzZXR0aW5nUmVnaXN0cnkuc2V0KFxuICAgICAgICAgICAgU1RBVFVTQkFSX1BMVUdJTl9JRCxcbiAgICAgICAgICAgICd2aXNpYmxlJyxcbiAgICAgICAgICAgIHN0YXR1c0Jhci5pc1Zpc2libGVcbiAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgaXNUb2dnbGVkOiAoKSA9PiBzdGF0dXNCYXIuaXNWaXNpYmxlXG4gICAgfSk7XG5cbiAgICBhcHAuY29tbWFuZHMuY29tbWFuZEV4ZWN1dGVkLmNvbm5lY3QoKHJlZ2lzdHJ5LCBleGVjdXRlZCkgPT4ge1xuICAgICAgaWYgKGV4ZWN1dGVkLmlkID09PSAnYXBwbGljYXRpb246cmVzZXQtbGF5b3V0JyAmJiAhc3RhdHVzQmFyLmlzVmlzaWJsZSkge1xuICAgICAgICBhcHAuY29tbWFuZHMuZXhlY3V0ZShjb21tYW5kKS5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAgIGNvbnNvbGUuZXJyb3IoJ0ZhaWxlZCB0byBzaG93IHRoZSBzdGF0dXMgYmFyLicsIHJlYXNvbik7XG4gICAgICAgIH0pO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIHBhbGV0dGUuYWRkSXRlbSh7IGNvbW1hbmQsIGNhdGVnb3J5IH0pO1xuICAgIH1cblxuICAgIGlmIChzZXR0aW5nUmVnaXN0cnkpIHtcbiAgICAgIGNvbnN0IGxvYWRTZXR0aW5ncyA9IHNldHRpbmdSZWdpc3RyeS5sb2FkKFNUQVRVU0JBUl9QTFVHSU5fSUQpO1xuICAgICAgY29uc3QgdXBkYXRlU2V0dGluZ3MgPSAoc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzKTogdm9pZCA9PiB7XG4gICAgICAgIGNvbnN0IHZpc2libGUgPSBzZXR0aW5ncy5nZXQoJ3Zpc2libGUnKS5jb21wb3NpdGUgYXMgYm9vbGVhbjtcbiAgICAgICAgc3RhdHVzQmFyLnNldEhpZGRlbighdmlzaWJsZSk7XG4gICAgICB9O1xuXG4gICAgICBQcm9taXNlLmFsbChbbG9hZFNldHRpbmdzLCBhcHAucmVzdG9yZWRdKVxuICAgICAgICAudGhlbigoW3NldHRpbmdzXSkgPT4ge1xuICAgICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3Qoc2V0dGluZ3MgPT4ge1xuICAgICAgICAgICAgdXBkYXRlU2V0dGluZ3Moc2V0dGluZ3MpO1xuICAgICAgICAgIH0pO1xuICAgICAgICB9KVxuICAgICAgICAuY2F0Y2goKHJlYXNvbjogRXJyb3IpID0+IHtcbiAgICAgICAgICBjb25zb2xlLmVycm9yKHJlYXNvbi5tZXNzYWdlKTtcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgcmV0dXJuIHN0YXR1c0JhcjtcbiAgfSxcbiAgb3B0aW9uYWw6IFtJTGFiU2hlbGwsIElTZXR0aW5nUmVnaXN0cnksIElDb21tYW5kUGFsZXR0ZV1cbn07XG5cbmV4cG9ydCBkZWZhdWx0IHN0YXR1c0JhcjtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==