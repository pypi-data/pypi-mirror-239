"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_extensionmanager-extension_lib_index_js-_9e3d0"],{

/***/ "../packages/extensionmanager-extension/lib/index.js":
/*!***********************************************************!*\
  !*** ../packages/extensionmanager-extension/lib/index.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/extensionmanager */ "webpack/sharing/consume/default/@jupyterlab/extensionmanager/@jupyterlab/extensionmanager");
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module extensionmanager-extension
 */






const PLUGIN_ID = '@jupyterlab/extensionmanager-extension:plugin';
/**
 * IDs of the commands added by this extension.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.showPanel = 'extensionmanager:show-panel';
    CommandIDs.toggle = 'extensionmanager:toggle';
})(CommandIDs || (CommandIDs = {}));
/**
 * The extension manager plugin.
 */
const plugin = {
    id: PLUGIN_ID,
    description: 'Adds the extension manager plugin.',
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: async (app, registry, translator, restorer, palette) => {
        const { commands, shell, serviceManager } = app;
        translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const model = new _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__.ListModel(serviceManager, translator);
        const createView = () => {
            const v = new _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_2__.ExtensionsPanel({ model, translator: translator });
            v.id = 'extensionmanager.main-view';
            v.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.extensionIcon;
            v.title.caption = trans.__('Extension Manager');
            v.node.setAttribute('role', 'region');
            v.node.setAttribute('aria-label', trans.__('Extension Manager section'));
            if (restorer) {
                restorer.add(v, v.id);
            }
            shell.add(v, 'left', { rank: 1000 });
            return v;
        };
        // Create a view by default, so it can be restored when loading the workspace.
        let view = createView();
        // If the extension is enabled or disabled,
        // add or remove it from the left area.
        Promise.all([app.restored, registry.load(PLUGIN_ID)])
            .then(([, settings]) => {
            model.isDisclaimed = settings.get('disclaimed').composite;
            model.isEnabled = settings.get('enabled').composite;
            model.stateChanged.connect(() => {
                if (model.isDisclaimed !==
                    settings.get('disclaimed').composite) {
                    settings.set('disclaimed', model.isDisclaimed).catch(reason => {
                        console.error(`Failed to set setting 'disclaimed'.\n${reason}`);
                    });
                }
                if (model.isEnabled !== settings.get('enabled').composite) {
                    settings.set('enabled', model.isEnabled).catch(reason => {
                        console.error(`Failed to set setting 'enabled'.\n${reason}`);
                    });
                }
            });
            if (model.isEnabled) {
                view = view !== null && view !== void 0 ? view : createView();
            }
            else {
                view === null || view === void 0 ? void 0 : view.dispose();
                view = null;
            }
            settings.changed.connect(async () => {
                model.isDisclaimed = settings.get('disclaimed').composite;
                model.isEnabled = settings.get('enabled').composite;
                app.commands.notifyCommandChanged(CommandIDs.toggle);
                if (model.isEnabled) {
                    if (view === null || !view.isAttached) {
                        const accepted = await Private.showWarning(trans);
                        if (!accepted) {
                            void settings.set('enabled', false);
                            return;
                        }
                    }
                    view = view !== null && view !== void 0 ? view : createView();
                }
                else {
                    view === null || view === void 0 ? void 0 : view.dispose();
                    view = null;
                }
            });
        })
            .catch(reason => {
            console.error(`Something went wrong when reading the settings.\n${reason}`);
        });
        commands.addCommand(CommandIDs.showPanel, {
            label: trans.__('Extension Manager'),
            execute: () => {
                if (view) {
                    shell.activateById(view.id);
                }
            },
            isVisible: () => model.isEnabled
        });
        commands.addCommand(CommandIDs.toggle, {
            label: trans.__('Enable Extension Manager'),
            execute: () => {
                if (registry) {
                    void registry.set(plugin.id, 'enabled', !model.isEnabled);
                }
            },
            isToggled: () => model.isEnabled
        });
        if (palette) {
            palette.addItem({
                command: CommandIDs.toggle,
                category: trans.__('Extension Manager')
            });
        }
    }
};
/**
 * Export the plugin as the default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for module-private functions.
 */
var Private;
(function (Private) {
    /**
     * Show a warning dialog about extension security.
     *
     * @returns whether the user accepted the dialog.
     */
    async function showWarning(trans) {
        const result = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: trans.__('Enable Extension Manager?'),
            body: trans.__(`Thanks for trying out JupyterLab's extension manager.
The JupyterLab development team is excited to have a robust
third-party extension community.
However, we cannot vouch for every extension,
and some may introduce security risks.
Do you want to continue?`),
            buttons: [
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: trans.__('Disable') }),
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.warnButton({ label: trans.__('Enable') })
            ]
        });
        return result.button.accept;
    }
    Private.showWarning = showWarning;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZXh0ZW5zaW9ubWFuYWdlci1leHRlbnNpb25fbGliX2luZGV4X2pzLV85ZTNkMC4zN2I5MDQwYzFlYmQ1MmY5ZTExMS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDMEM7QUFDRDtBQUNYO0FBSzlCO0FBQ3lCO0FBRTFELE1BQU0sU0FBUyxHQUFHLCtDQUErQyxDQUFDO0FBRWxFOztHQUVHO0FBQ0gsSUFBVSxVQUFVLENBR25CO0FBSEQsV0FBVSxVQUFVO0lBQ0wsb0JBQVMsR0FBRyw2QkFBNkIsQ0FBQztJQUMxQyxpQkFBTSxHQUFHLHlCQUF5QixDQUFDO0FBQ2xELENBQUMsRUFIUyxVQUFVLEtBQVYsVUFBVSxRQUduQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxNQUFNLEdBQWdDO0lBQzFDLEVBQUUsRUFBRSxTQUFTO0lBQ2IsV0FBVyxFQUFFLG9DQUFvQztJQUNqRCxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLHlFQUFnQixDQUFDO0lBQzVCLFFBQVEsRUFBRSxDQUFDLGdFQUFXLEVBQUUsb0VBQWUsRUFBRSxpRUFBZSxDQUFDO0lBQ3pELFFBQVEsRUFBRSxLQUFLLEVBQ2IsR0FBb0IsRUFDcEIsUUFBMEIsRUFDMUIsVUFBOEIsRUFDOUIsUUFBZ0MsRUFDaEMsT0FBK0IsRUFDL0IsRUFBRTtRQUNGLE1BQU0sRUFBRSxRQUFRLEVBQUUsS0FBSyxFQUFFLGNBQWMsRUFBRSxHQUFHLEdBQUcsQ0FBQztRQUNoRCxVQUFVLEdBQUcsVUFBVSxhQUFWLFVBQVUsY0FBVixVQUFVLEdBQUksbUVBQWMsQ0FBQztRQUMxQyxNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBRTVDLE1BQU0sS0FBSyxHQUFHLElBQUksbUVBQVMsQ0FBQyxjQUFjLEVBQUUsVUFBVSxDQUFDLENBQUM7UUFFeEQs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QUFLLENBQUMsRUFBRSxDQUFDLFNBQVMsQ0FBQyxFQUFFLENBQUM7Z0JBQ25ELG1FQUFpQixDQUFDLEVBQUUsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsUUFBUSxDQUFDLEVBQUUsQ0FBQzthQUNqRDtTQUNGLENBQUMsQ0FBQztRQUVILE9BQU8sTUFBTSxDQUFDLE1BQU0sQ0FBQyxNQUFNLENBQUM7SUFDOUIsQ0FBQztJQWxCcUIsbUJBQVcsY0FrQmhDO0FBQ0gsQ0FBQyxFQXpCUyxPQUFPLEtBQVAsT0FBTyxRQXlCaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZXh0ZW5zaW9ubWFuYWdlci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGV4dGVuc2lvbm1hbmFnZXItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBEaWFsb2csIElDb21tYW5kUGFsZXR0ZSwgc2hvd0RpYWxvZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IEV4dGVuc2lvbnNQYW5lbCwgTGlzdE1vZGVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvZXh0ZW5zaW9ubWFuYWdlcic7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgZXh0ZW5zaW9uSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG5jb25zdCBQTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvZXh0ZW5zaW9ubWFuYWdlci1leHRlbnNpb246cGx1Z2luJztcblxuLyoqXG4gKiBJRHMgb2YgdGhlIGNvbW1hbmRzIGFkZGVkIGJ5IHRoaXMgZXh0ZW5zaW9uLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBzaG93UGFuZWwgPSAnZXh0ZW5zaW9ubWFuYWdlcjpzaG93LXBhbmVsJztcbiAgZXhwb3J0IGNvbnN0IHRvZ2dsZSA9ICdleHRlbnNpb25tYW5hZ2VyOnRvZ2dsZSc7XG59XG5cbi8qKlxuICogVGhlIGV4dGVuc2lvbiBtYW5hZ2VyIHBsdWdpbi5cbiAqL1xuY29uc3QgcGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiBQTFVHSU5fSUQsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0aGUgZXh0ZW5zaW9uIG1hbmFnZXIgcGx1Z2luLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJU2V0dGluZ1JlZ2lzdHJ5XSxcbiAgb3B0aW9uYWw6IFtJVHJhbnNsYXRvciwgSUxheW91dFJlc3RvcmVyLCBJQ29tbWFuZFBhbGV0dGVdLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbCxcbiAgICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4gICkgPT4ge1xuICAgIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsLCBzZXJ2aWNlTWFuYWdlciB9ID0gYXBwO1xuICAgIHRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICBjb25zdCBtb2RlbCA9IG5ldyBMaXN0TW9kZWwoc2VydmljZU1hbmFnZXIsIHRyYW5zbGF0b3IpO1xuXG4gICAgY29uc3QgY3JlYXRlVmlldyA9ICgpID0+IHtcbiAgICAgIGNvbnN0IHYgPSBuZXcgRXh0ZW5zaW9uc1BhbmVsKHsgbW9kZWwsIHRyYW5zbGF0b3I6IHRyYW5zbGF0b3IhIH0pO1xuICAgICAgdi5pZCA9ICdleHRlbnNpb25tYW5hZ2VyLm1haW4tdmlldyc7XG4gICAgICB2LnRpdGxlLmljb24gPSBleHRlbnNpb25JY29uO1xuICAgICAgdi50aXRsZS5jYXB0aW9uID0gdHJhbnMuX18oJ0V4dGVuc2lvbiBNYW5hZ2VyJyk7XG4gICAgICB2Lm5vZGUuc2V0QXR0cmlidXRlKCdyb2xlJywgJ3JlZ2lvbicpO1xuICAgICAgdi5ub2RlLnNldEF0dHJpYnV0ZSgnYXJpYS1sYWJlbCcsIHRyYW5zLl9fKCdFeHRlbnNpb24gTWFuYWdlciBzZWN0aW9uJykpO1xuICAgICAgaWYgKHJlc3RvcmVyKSB7XG4gICAgICAgIHJlc3RvcmVyLmFkZCh2LCB2LmlkKTtcbiAgICAgIH1cbiAgICAgIHNoZWxsLmFkZCh2LCAnbGVmdCcsIHsgcmFuazogMTAwMCB9KTtcblxuICAgICAgcmV0dXJuIHY7XG4gICAgfTtcblxuICAgIC8vIENyZWF0ZSBhIHZpZXcgYnkgZGVmYXVsdCwgc28gaXQgY2FuIGJlIHJlc3RvcmVkIHdoZW4gbG9hZGluZyB0aGUgd29ya3NwYWNlLlxuICAgIGxldCB2aWV3OiBFeHRlbnNpb25zUGFuZWwgfCBudWxsID0gY3JlYXRlVmlldygpO1xuXG4gICAgLy8gSWYgdGhlIGV4dGVuc2lvbiBpcyBlbmFibGVkIG9yIGRpc2FibGVkLFxuICAgIC8vIGFkZCBvciByZW1vdmUgaXQgZnJvbSB0aGUgbGVmdCBhcmVhLlxuICAgIFByb21pc2UuYWxsKFthcHAucmVzdG9yZWQsIHJlZ2lzdHJ5LmxvYWQoUExVR0lOX0lEKV0pXG4gICAgICAudGhlbigoWywgc2V0dGluZ3NdKSA9PiB7XG4gICAgICAgIG1vZGVsLmlzRGlzY2xhaW1lZCA9IHNldHRpbmdzLmdldCgnZGlzY2xhaW1lZCcpLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICBtb2RlbC5pc0VuYWJsZWQgPSBzZXR0aW5ncy5nZXQoJ2VuYWJsZWQnKS5jb21wb3NpdGUgYXMgYm9vbGVhbjtcbiAgICAgICAgbW9kZWwuc3RhdGVDaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICAgIGlmIChcbiAgICAgICAgICAgIG1vZGVsLmlzRGlzY2xhaW1lZCAhPT1cbiAgICAgICAgICAgIChzZXR0aW5ncy5nZXQoJ2Rpc2NsYWltZWQnKS5jb21wb3NpdGUgYXMgYm9vbGVhbilcbiAgICAgICAgICApIHtcbiAgICAgICAgICAgIHNldHRpbmdzLnNldCgnZGlzY2xhaW1lZCcsIG1vZGVsLmlzRGlzY2xhaW1lZCkuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCBzZXR0aW5nICdkaXNjbGFpbWVkJy5cXG4ke3JlYXNvbn1gKTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgICBpZiAoXG4gICAgICAgICAgICBtb2RlbC5pc0VuYWJsZWQgIT09IChzZXR0aW5ncy5nZXQoJ2VuYWJsZWQnKS5jb21wb3NpdGUgYXMgYm9vbGVhbilcbiAgICAgICAgICApIHtcbiAgICAgICAgICAgIHNldHRpbmdzLnNldCgnZW5hYmxlZCcsIG1vZGVsLmlzRW5hYmxlZCkuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgICAgICAgY29uc29sZS5lcnJvcihgRmFpbGVkIHRvIHNldCBzZXR0aW5nICdlbmFibGVkJy5cXG4ke3JlYXNvbn1gKTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG5cbiAgICAgICAgaWYgKG1vZGVsLmlzRW5hYmxlZCkge1xuICAgICAgICAgIHZpZXcgPSB2aWV3ID8/IGNyZWF0ZVZpZXcoKTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICB2aWV3Py5kaXNwb3NlKCk7XG4gICAgICAgICAgdmlldyA9IG51bGw7XG4gICAgICAgIH1cblxuICAgICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QoYXN5bmMgKCkgPT4ge1xuICAgICAgICAgIG1vZGVsLmlzRGlzY2xhaW1lZCA9IHNldHRpbmdzLmdldCgnZGlzY2xhaW1lZCcpLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICAgIG1vZGVsLmlzRW5hYmxlZCA9IHNldHRpbmdzLmdldCgnZW5hYmxlZCcpLmNvbXBvc2l0ZSBhcyBib29sZWFuO1xuICAgICAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZChDb21tYW5kSURzLnRvZ2dsZSk7XG5cbiAgICAgICAgICBpZiAobW9kZWwuaXNFbmFibGVkKSB7XG4gICAgICAgICAgICBpZiAodmlldyA9PT0gbnVsbCB8fCAhdmlldy5pc0F0dGFjaGVkKSB7XG4gICAgICAgICAgICAgIGNvbnN0IGFjY2VwdGVkID0gYXdhaXQgUHJpdmF0ZS5zaG93V2FybmluZyh0cmFucyk7XG4gICAgICAgICAgICAgIGlmICghYWNjZXB0ZWQpIHtcbiAgICAgICAgICAgICAgICB2b2lkIHNldHRpbmdzLnNldCgnZW5hYmxlZCcsIGZhbHNlKTtcbiAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHZpZXcgPSB2aWV3ID8/IGNyZWF0ZVZpZXcoKTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgdmlldz8uZGlzcG9zZSgpO1xuICAgICAgICAgICAgdmlldyA9IG51bGw7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH0pXG4gICAgICAuY2F0Y2gocmVhc29uID0+IHtcbiAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICBgU29tZXRoaW5nIHdlbnQgd3Jvbmcgd2hlbiByZWFkaW5nIHRoZSBzZXR0aW5ncy5cXG4ke3JlYXNvbn1gXG4gICAgICAgICk7XG4gICAgICB9KTtcblxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zaG93UGFuZWwsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRXh0ZW5zaW9uIE1hbmFnZXInKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgaWYgKHZpZXcpIHtcbiAgICAgICAgICBzaGVsbC5hY3RpdmF0ZUJ5SWQodmlldy5pZCk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICBpc1Zpc2libGU6ICgpID0+IG1vZGVsLmlzRW5hYmxlZFxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZSwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdFbmFibGUgRXh0ZW5zaW9uIE1hbmFnZXInKSxcbiAgICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgICAgaWYgKHJlZ2lzdHJ5KSB7XG4gICAgICAgICAgdm9pZCByZWdpc3RyeS5zZXQocGx1Z2luLmlkLCAnZW5hYmxlZCcsICFtb2RlbC5pc0VuYWJsZWQpO1xuICAgICAgICB9XG4gICAgICB9LFxuICAgICAgaXNUb2dnbGVkOiAoKSA9PiBtb2RlbC5pc0VuYWJsZWRcbiAgICB9KTtcblxuICAgIGlmIChwYWxldHRlKSB7XG4gICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICBjb21tYW5kOiBDb21tYW5kSURzLnRvZ2dsZSxcbiAgICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdFeHRlbnNpb24gTWFuYWdlcicpXG4gICAgICB9KTtcbiAgICB9XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW4gYXMgdGhlIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgbW9kdWxlLXByaXZhdGUgZnVuY3Rpb25zLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBTaG93IGEgd2FybmluZyBkaWFsb2cgYWJvdXQgZXh0ZW5zaW9uIHNlY3VyaXR5LlxuICAgKlxuICAgKiBAcmV0dXJucyB3aGV0aGVyIHRoZSB1c2VyIGFjY2VwdGVkIHRoZSBkaWFsb2cuXG4gICAqL1xuICBleHBvcnQgYXN5bmMgZnVuY3Rpb24gc2hvd1dhcm5pbmcoXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICk6IFByb21pc2U8Ym9vbGVhbj4ge1xuICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IHNob3dEaWFsb2coe1xuICAgICAgdGl0bGU6IHRyYW5zLl9fKCdFbmFibGUgRXh0ZW5zaW9uIE1hbmFnZXI/JyksXG4gICAgICBib2R5OiB0cmFucy5fXyhgVGhhbmtzIGZvciB0cnlpbmcgb3V0IEp1cHl0ZXJMYWIncyBleHRlbnNpb24gbWFuYWdlci5cblRoZSBKdXB5dGVyTGFiIGRldmVsb3BtZW50IHRlYW0gaXMgZXhjaXRlZCB0byBoYXZlIGEgcm9idXN0XG50aGlyZC1wYXJ0eSBleHRlbnNpb24gY29tbXVuaXR5LlxuSG93ZXZlciwgd2UgY2Fubm90IHZvdWNoIGZvciBldmVyeSBleHRlbnNpb24sXG5hbmQgc29tZSBtYXkgaW50cm9kdWNlIHNlY3VyaXR5IHJpc2tzLlxuRG8geW91IHdhbnQgdG8gY29udGludWU/YCksXG4gICAgICBidXR0b25zOiBbXG4gICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0Rpc2FibGUnKSB9KSxcbiAgICAgICAgRGlhbG9nLndhcm5CdXR0b24oeyBsYWJlbDogdHJhbnMuX18oJ0VuYWJsZScpIH0pXG4gICAgICBdXG4gICAgfSk7XG5cbiAgICByZXR1cm4gcmVzdWx0LmJ1dHRvbi5hY2NlcHQ7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==