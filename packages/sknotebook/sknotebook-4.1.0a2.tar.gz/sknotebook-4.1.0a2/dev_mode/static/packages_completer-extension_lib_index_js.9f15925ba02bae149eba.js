"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_completer-extension_lib_index_js"],{

/***/ "../packages/completer-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/completer-extension/lib/index.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _renderer__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./renderer */ "../packages/completer-extension/lib/renderer.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module completer-extension
 */




const COMPLETION_MANAGER_PLUGIN = '@jupyterlab/completer-extension:manager';
const defaultProvider = {
    id: '@jupyterlab/completer-extension:base-service',
    description: 'Adds context and kernel completion providers.',
    requires: [_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionProviderManager],
    autoStart: true,
    activate: (app, completionManager) => {
        completionManager.registerProvider(new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ContextCompleterProvider());
        completionManager.registerProvider(new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.KernelCompleterProvider());
    }
};
const manager = {
    id: COMPLETION_MANAGER_PLUGIN,
    description: 'Provides the completion provider manager.',
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    optional: [_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.IFormRendererRegistry],
    provides: _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionProviderManager,
    autoStart: true,
    activate: (app, settings, editorRegistry) => {
        const AVAILABLE_PROVIDERS = 'availableProviders';
        const PROVIDER_TIMEOUT = 'providerTimeout';
        const SHOW_DOCUMENT_PANEL = 'showDocumentationPanel';
        const CONTINUOUS_HINTING = 'autoCompletion';
        const manager = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.CompletionProviderManager();
        const updateSetting = (settingValues, availableProviders) => {
            var _a;
            const providersData = settingValues.get(AVAILABLE_PROVIDERS);
            const timeout = settingValues.get(PROVIDER_TIMEOUT);
            const showDoc = settingValues.get(SHOW_DOCUMENT_PANEL);
            const continuousHinting = settingValues.get(CONTINUOUS_HINTING);
            manager.setTimeout(timeout.composite);
            manager.setShowDocumentationPanel(showDoc.composite);
            manager.setContinuousHinting(continuousHinting.composite);
            const selectedProviders = (_a = providersData.user) !== null && _a !== void 0 ? _a : providersData.composite;
            const sortedProviders = Object.entries(selectedProviders !== null && selectedProviders !== void 0 ? selectedProviders : {})
                .filter(val => val[1] >= 0 && availableProviders.includes(val[0]))
                .sort(([, rank1], [, rank2]) => rank2 - rank1)
                .map(item => item[0]);
            manager.activateProvider(sortedProviders);
        };
        app.restored
            .then(() => {
            const availableProviders = [...manager.getProviders().entries()];
            const availableProviderIDs = availableProviders.map(([key, value]) => key);
            settings.transform(COMPLETION_MANAGER_PLUGIN, {
                fetch: plugin => {
                    const schema = plugin.schema.properties;
                    const defaultValue = {};
                    availableProviders.forEach(([key, value], index) => {
                        var _a;
                        defaultValue[key] = (_a = value.rank) !== null && _a !== void 0 ? _a : (index + 1) * 10;
                    });
                    schema[AVAILABLE_PROVIDERS]['default'] = defaultValue;
                    return plugin;
                }
            });
            const settingsPromise = settings.load(COMPLETION_MANAGER_PLUGIN);
            settingsPromise
                .then(settingValues => {
                updateSetting(settingValues, availableProviderIDs);
                settingValues.changed.connect(newSettings => {
                    updateSetting(newSettings, availableProviderIDs);
                });
            })
                .catch(console.error);
        })
            .catch(console.error);
        if (editorRegistry) {
            const renderer = {
                fieldRenderer: (props) => {
                    return (0,_renderer__WEBPACK_IMPORTED_MODULE_3__.renderAvailableProviders)(props);
                }
            };
            editorRegistry.addRenderer(`${COMPLETION_MANAGER_PLUGIN}.availableProviders`, renderer);
        }
        return manager;
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [manager, defaultProvider];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "../packages/completer-extension/lib/renderer.js":
/*!*******************************************************!*\
  !*** ../packages/completer-extension/lib/renderer.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "renderAvailableProviders": () => (/* binding */ renderAvailableProviders)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

const AVAILABLE_PROVIDERS = 'availableProviders';
/**
 * Custom setting renderer for provider rank.
 */
function renderAvailableProviders(props) {
    const { schema } = props;
    const title = schema.title;
    const desc = schema.description;
    const settings = props.formContext.settings;
    const userData = settings.get(AVAILABLE_PROVIDERS).user;
    const items = {
        ...schema.default
    };
    if (userData) {
        for (const key of Object.keys(items)) {
            if (key in userData) {
                items[key] = userData[key];
            }
            else {
                items[key] = -1;
            }
        }
    }
    const [settingValue, setValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(items);
    const onSettingChange = (key, e) => {
        const newValue = {
            ...settingValue,
            [key]: parseInt(e.target.value)
        };
        settings.set(AVAILABLE_PROVIDERS, newValue).catch(console.error);
        setValue(newValue);
    };
    return (
    //TODO Remove hard coded class names
    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("fieldset", null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("legend", null, title),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("p", { className: "field-description" }, desc),
            Object.keys(items).map(key => {
                return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { key: key, className: "form-group small-field" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", null,
                            " ",
                            key),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "inputFieldWrapper" },
                            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { className: "form-control", type: "number", value: settingValue[key], onChange: e => {
                                    onSettingChange(key, e);
                                } })))));
            }))));
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY29tcGxldGVyLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuOWYxNTkyNWJhMDJiYWUxNDllYmEuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQVc0QjtBQUNnQztBQUk1QjtBQUdtQjtBQUV0RCxNQUFNLHlCQUF5QixHQUFHLHlDQUF5QyxDQUFDO0FBRTVFLE1BQU0sZUFBZSxHQUFnQztJQUNuRCxFQUFFLEVBQUUsOENBQThDO0lBQ2xELFdBQVcsRUFBRSwrQ0FBK0M7SUFDNUQsUUFBUSxFQUFFLENBQUMsNkVBQTBCLENBQUM7SUFDdEMsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixpQkFBNkMsRUFDdkMsRUFBRTtRQUNSLGlCQUFpQixDQUFDLGdCQUFnQixDQUFDLElBQUksMkVBQXdCLEVBQUUsQ0FBQyxDQUFDO1FBQ25FLGlCQUFpQixDQUFDLGdCQUFnQixDQUFDLElBQUksMEVBQXVCLEVBQUUsQ0FBQyxDQUFDO0lBQ3BFLENBQUM7Q0FDRixDQUFDO0FBRUYsTUFBTSxPQUFPLEdBQXNEO0lBQ2pFLEVBQUUsRUFBRSx5QkFBeUI7SUFDN0IsV0FBVyxFQUFFLDJDQUEyQztJQUN4RCxRQUFRLEVBQUUsQ0FBQyx5RUFBZ0IsQ0FBQztJQUM1QixRQUFRLEVBQUUsQ0FBQyw0RUFBcUIsQ0FBQztJQUNqQyxRQUFRLEVBQUUsNkVBQTBCO0lBQ3BDLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQ1IsR0FBb0IsRUFDcEIsUUFBMEIsRUFDMUIsY0FBNEMsRUFDaEIsRUFBRTtRQUM5QixNQUFNLG1CQUFtQixHQUFHLG9CQUFvQixDQUFDO1FBQ2pELE1BQU0sZ0JBQWdCLEdBQUcsaUJBQWlCLENBQUM7UUFDM0MsTUFBTSxtQkFBbUIsR0FBRyx3QkFBd0IsQ0FBQztRQUNyRCxNQUFNLGtCQUFrQixHQUFHLGdCQUFnQixDQUFD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QUFLLEdBQUcsRUFBRSxHQUFHLEVBQUUsU0FBUyxFQUFDLHdCQUF3QjtvQkFDL0M7d0JBQ0U7OzRCQUFNLEdBQUcsQ0FBTTt3QkFDZixvRUFBSyxTQUFTLEVBQUMsbUJBQW1COzRCQUNoQyxzRUFDRSxTQUFTLEVBQUMsY0FBYyxFQUN4QixJQUFJLEVBQUMsUUFBUSxFQUNiLEtBQUssRUFBRSxZQUFZLENBQUMsR0FBRyxDQUFDLEVBQ3hCLFFBQVEsRUFBRSxDQUFDLENBQUMsRUFBRTtvQ0FDWixlQUFlLENBQUMsR0FBRyxFQUFFLENBQUMsQ0FBQyxDQUFDO2dDQUMxQixDQUFDLEdBQ0QsQ0FDRSxDQUNGLENBQ0YsQ0FDUCxDQUFDO1lBQ0osQ0FBQyxDQUFDLENBQ08sQ0FDUCxDQUNQLENBQUM7QUFDSixDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvbXBsZXRlci1leHRlbnNpb24vc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb21wbGV0ZXItZXh0ZW5zaW9uL3NyYy9yZW5kZXJlci50c3giXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY29tcGxldGVyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIENvbXBsZXRpb25Qcm92aWRlck1hbmFnZXIsXG4gIENvbnRleHRDb21wbGV0ZXJQcm92aWRlcixcbiAgSUNvbXBsZXRpb25Qcm92aWRlck1hbmFnZXIsXG4gIEtlcm5lbENvbXBsZXRlclByb3ZpZGVyXG59IGZyb20gJ0BqdXB5dGVybGFiL2NvbXBsZXRlcic7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElGb3JtUmVuZGVyZXIsXG4gIElGb3JtUmVuZGVyZXJSZWdpc3RyeVxufSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB0eXBlIHsgRmllbGRQcm9wcyB9IGZyb20gJ0ByanNmL3V0aWxzJztcblxuaW1wb3J0IHsgcmVuZGVyQXZhaWxhYmxlUHJvdmlkZXJzIH0gZnJvbSAnLi9yZW5kZXJlcic7XG5cbmNvbnN0IENPTVBMRVRJT05fTUFOQUdFUl9QTFVHSU4gPSAnQGp1cHl0ZXJsYWIvY29tcGxldGVyLWV4dGVuc2lvbjptYW5hZ2VyJztcblxuY29uc3QgZGVmYXVsdFByb3ZpZGVyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY29tcGxldGVyLWV4dGVuc2lvbjpiYXNlLXNlcnZpY2UnLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgY29udGV4dCBhbmQga2VybmVsIGNvbXBsZXRpb24gcHJvdmlkZXJzLicsXG4gIHJlcXVpcmVzOiBbSUNvbXBsZXRpb25Qcm92aWRlck1hbmFnZXJdLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgY29tcGxldGlvbk1hbmFnZXI6IElDb21wbGV0aW9uUHJvdmlkZXJNYW5hZ2VyXG4gICk6IHZvaWQgPT4ge1xuICAgIGNvbXBsZXRpb25NYW5hZ2VyLnJlZ2lzdGVyUHJvdmlkZXIobmV3IENvbnRleHRDb21wbGV0ZXJQcm92aWRlcigpKTtcbiAgICBjb21wbGV0aW9uTWFuYWdlci5yZWdpc3RlclByb3ZpZGVyKG5ldyBLZXJuZWxDb21wbGV0ZXJQcm92aWRlcigpKTtcbiAgfVxufTtcblxuY29uc3QgbWFuYWdlcjogSnVweXRlckZyb250RW5kUGx1Z2luPElDb21wbGV0aW9uUHJvdmlkZXJNYW5hZ2VyPiA9IHtcbiAgaWQ6IENPTVBMRVRJT05fTUFOQUdFUl9QTFVHSU4sXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGNvbXBsZXRpb24gcHJvdmlkZXIgbWFuYWdlci4nLFxuICByZXF1aXJlczogW0lTZXR0aW5nUmVnaXN0cnldLFxuICBvcHRpb25hbDogW0lGb3JtUmVuZGVyZXJSZWdpc3RyeV0sXG4gIHByb3ZpZGVzOiBJQ29tcGxldGlvblByb3ZpZGVyTWFuYWdlcixcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIGVkaXRvclJlZ2lzdHJ5OiBJRm9ybVJlbmRlcmVyUmVnaXN0cnkgfCBudWxsXG4gICk6IElDb21wbGV0aW9uUHJvdmlkZXJNYW5hZ2VyID0+IHtcbiAgICBjb25zdCBBVkFJTEFCTEVfUFJPVklERVJTID0gJ2F2YWlsYWJsZVByb3ZpZGVycyc7XG4gICAgY29uc3QgUFJPVklERVJfVElNRU9VVCA9ICdwcm92aWRlclRpbWVvdXQnO1xuICAgIGNvbnN0IFNIT1dfRE9DVU1FTlRfUEFORUwgPSAnc2hvd0RvY3VtZW50YXRpb25QYW5lbCc7XG4gICAgY29uc3QgQ09OVElOVU9VU19ISU5USU5HID0gJ2F1dG9Db21wbGV0aW9uJztcbiAgICBjb25zdCBtYW5hZ2VyID0gbmV3IENvbXBsZXRpb25Qcm92aWRlck1hbmFnZXIoKTtcbiAgICBjb25zdCB1cGRhdGVTZXR0aW5nID0gKFxuICAgICAgc2V0dGluZ1ZhbHVlczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MsXG4gICAgICBhdmFpbGFibGVQcm92aWRlcnM6IHN0cmluZ1tdXG4gICAgKTogdm9pZCA9PiB7XG4gICAgICBjb25zdCBwcm92aWRlcnNEYXRhID0gc2V0dGluZ1ZhbHVlcy5nZXQoQVZBSUxBQkxFX1BST1ZJREVSUyk7XG4gICAgICBjb25zdCB0aW1lb3V0ID0gc2V0dGluZ1ZhbHVlcy5nZXQoUFJPVklERVJfVElNRU9VVCk7XG4gICAgICBjb25zdCBzaG93RG9jID0gc2V0dGluZ1ZhbHVlcy5nZXQoU0hPV19ET0NVTUVOVF9QQU5FTCk7XG4gICAgICBjb25zdCBjb250aW51b3VzSGludGluZyA9IHNldHRpbmdWYWx1ZXMuZ2V0KENPTlRJTlVPVVNfSElOVElORyk7XG4gICAgICBtYW5hZ2VyLnNldFRpbWVvdXQodGltZW91dC5jb21wb3NpdGUgYXMgbnVtYmVyKTtcbiAgICAgIG1hbmFnZXIuc2V0U2hvd0RvY3VtZW50YXRpb25QYW5lbChzaG93RG9jLmNvbXBvc2l0ZSBhcyBib29sZWFuKTtcbiAgICAgIG1hbmFnZXIuc2V0Q29udGludW91c0hpbnRpbmcoY29udGludW91c0hpbnRpbmcuY29tcG9zaXRlIGFzIGJvb2xlYW4pO1xuICAgICAgY29uc3Qgc2VsZWN0ZWRQcm92aWRlcnMgPSBwcm92aWRlcnNEYXRhLnVzZXIgPz8gcHJvdmlkZXJzRGF0YS5jb21wb3NpdGU7XG4gICAgICBjb25zdCBzb3J0ZWRQcm92aWRlcnMgPSBPYmplY3QuZW50cmllcyhzZWxlY3RlZFByb3ZpZGVycyA/PyB7fSlcbiAgICAgICAgLmZpbHRlcih2YWwgPT4gdmFsWzFdID49IDAgJiYgYXZhaWxhYmxlUHJvdmlkZXJzLmluY2x1ZGVzKHZhbFswXSkpXG4gICAgICAgIC5zb3J0KChbLCByYW5rMV0sIFssIHJhbmsyXSkgPT4gcmFuazIgLSByYW5rMSlcbiAgICAgICAgLm1hcChpdGVtID0+IGl0ZW1bMF0pO1xuICAgICAgbWFuYWdlci5hY3RpdmF0ZVByb3ZpZGVyKHNvcnRlZFByb3ZpZGVycyk7XG4gICAgfTtcblxuICAgIGFwcC5yZXN0b3JlZFxuICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICBjb25zdCBhdmFpbGFibGVQcm92aWRlcnMgPSBbLi4ubWFuYWdlci5nZXRQcm92aWRlcnMoKS5lbnRyaWVzKCldO1xuICAgICAgICBjb25zdCBhdmFpbGFibGVQcm92aWRlcklEcyA9IGF2YWlsYWJsZVByb3ZpZGVycy5tYXAoXG4gICAgICAgICAgKFtrZXksIHZhbHVlXSkgPT4ga2V5XG4gICAgICAgICk7XG4gICAgICAgIHNldHRpbmdzLnRyYW5zZm9ybShDT01QTEVUSU9OX01BTkFHRVJfUExVR0lOLCB7XG4gICAgICAgICAgZmV0Y2g6IHBsdWdpbiA9PiB7XG4gICAgICAgICAgICBjb25zdCBzY2hlbWEgPSBwbHVnaW4uc2NoZW1hLnByb3BlcnRpZXMhO1xuICAgICAgICAgICAgY29uc3QgZGVmYXVsdFZhbHVlOiB7IFtrZXk6IHN0cmluZ106IG51bWJlciB9ID0ge307XG4gICAgICAgICAgICBhdmFpbGFibGVQcm92aWRlcnMuZm9yRWFjaCgoW2tleSwgdmFsdWVdLCBpbmRleCkgPT4ge1xuICAgICAgICAgICAgICBkZWZhdWx0VmFsdWVba2V5XSA9IHZhbHVlLnJhbmsgPz8gKGluZGV4ICsgMSkgKiAxMDtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgc2NoZW1hW0FWQUlMQUJMRV9QUk9WSURFUlNdWydkZWZhdWx0J10gPSBkZWZhdWx0VmFsdWU7XG4gICAgICAgICAgICByZXR1cm4gcGx1Z2luO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICAgIGNvbnN0IHNldHRpbmdzUHJvbWlzZSA9IHNldHRpbmdzLmxvYWQoQ09NUExFVElPTl9NQU5BR0VSX1BMVUdJTik7XG4gICAgICAgIHNldHRpbmdzUHJvbWlzZVxuICAgICAgICAgIC50aGVuKHNldHRpbmdWYWx1ZXMgPT4ge1xuICAgICAgICAgICAgdXBkYXRlU2V0dGluZyhzZXR0aW5nVmFsdWVzLCBhdmFpbGFibGVQcm92aWRlcklEcyk7XG4gICAgICAgICAgICBzZXR0aW5nVmFsdWVzLmNoYW5nZWQuY29ubmVjdChuZXdTZXR0aW5ncyA9PiB7XG4gICAgICAgICAgICAgIHVwZGF0ZVNldHRpbmcobmV3U2V0dGluZ3MsIGF2YWlsYWJsZVByb3ZpZGVySURzKTtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgIH0pXG4gICAgICAgICAgLmNhdGNoKGNvbnNvbGUuZXJyb3IpO1xuICAgICAgfSlcbiAgICAgIC5jYXRjaChjb25zb2xlLmVycm9yKTtcblxuICAgIGlmIChlZGl0b3JSZWdpc3RyeSkge1xuICAgICAgY29uc3QgcmVuZGVyZXI6IElGb3JtUmVuZGVyZXIgPSB7XG4gICAgICAgIGZpZWxkUmVuZGVyZXI6IChwcm9wczogRmllbGRQcm9wcykgPT4ge1xuICAgICAgICAgIHJldHVybiByZW5kZXJBdmFpbGFibGVQcm92aWRlcnMocHJvcHMpO1xuICAgICAgICB9XG4gICAgICB9O1xuICAgICAgZWRpdG9yUmVnaXN0cnkuYWRkUmVuZGVyZXIoXG4gICAgICAgIGAke0NPTVBMRVRJT05fTUFOQUdFUl9QTFVHSU59LmF2YWlsYWJsZVByb3ZpZGVyc2AsXG4gICAgICAgIHJlbmRlcmVyXG4gICAgICApO1xuICAgIH1cblxuICAgIHJldHVybiBtYW5hZ2VyO1xuICB9XG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2lucyBhcyBkZWZhdWx0LlxuICovXG5jb25zdCBwbHVnaW5zOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48YW55PltdID0gW21hbmFnZXIsIGRlZmF1bHRQcm92aWRlcl07XG5leHBvcnQgZGVmYXVsdCBwbHVnaW5zO1xuIiwiLypcbiAqIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuICogRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbiAqL1xuXG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgdHlwZSB7IEZpZWxkUHJvcHMgfSBmcm9tICdAcmpzZi91dGlscyc7XG5pbXBvcnQgUmVhY3QsIHsgdXNlU3RhdGUgfSBmcm9tICdyZWFjdCc7XG5cbmNvbnN0IEFWQUlMQUJMRV9QUk9WSURFUlMgPSAnYXZhaWxhYmxlUHJvdmlkZXJzJztcblxuLyoqXG4gKiBDdXN0b20gc2V0dGluZyByZW5kZXJlciBmb3IgcHJvdmlkZXIgcmFuay5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHJlbmRlckF2YWlsYWJsZVByb3ZpZGVycyhwcm9wczogRmllbGRQcm9wcyk6IEpTWC5FbGVtZW50IHtcbiAgY29uc3QgeyBzY2hlbWEgfSA9IHByb3BzO1xuICBjb25zdCB0aXRsZSA9IHNjaGVtYS50aXRsZTtcbiAgY29uc3QgZGVzYyA9IHNjaGVtYS5kZXNjcmlwdGlvbjtcbiAgY29uc3Qgc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzID0gcHJvcHMuZm9ybUNvbnRleHQuc2V0dGluZ3M7XG4gIGNvbnN0IHVzZXJEYXRhID0gc2V0dGluZ3MuZ2V0KEFWQUlMQUJMRV9QUk9WSURFUlMpLnVzZXIgYXNcbiAgICB8IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3RcbiAgICB8IHVuZGVmaW5lZDtcblxuICBjb25zdCBpdGVtcyA9IHtcbiAgICAuLi4oc2NoZW1hLmRlZmF1bHQgYXMgeyBba2V5OiBzdHJpbmddOiBudW1iZXIgfSlcbiAgfTtcbiAgaWYgKHVzZXJEYXRhKSB7XG4gICAgZm9yIChjb25zdCBrZXkgb2YgT2JqZWN0LmtleXMoaXRlbXMpKSB7XG4gICAgICBpZiAoa2V5IGluIHVzZXJEYXRhKSB7XG4gICAgICAgIGl0ZW1zW2tleV0gPSB1c2VyRGF0YVtrZXldIGFzIG51bWJlcjtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGl0ZW1zW2tleV0gPSAtMTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICBjb25zdCBbc2V0dGluZ1ZhbHVlLCBzZXRWYWx1ZV0gPSB1c2VTdGF0ZShpdGVtcyk7XG4gIGNvbnN0IG9uU2V0dGluZ0NoYW5nZSA9IChcbiAgICBrZXk6IHN0cmluZyxcbiAgICBlOiBSZWFjdC5DaGFuZ2VFdmVudDxIVE1MSW5wdXRFbGVtZW50PlxuICApID0+IHtcbiAgICBjb25zdCBuZXdWYWx1ZSA9IHtcbiAgICAgIC4uLnNldHRpbmdWYWx1ZSxcbiAgICAgIFtrZXldOiBwYXJzZUludChlLnRhcmdldC52YWx1ZSlcbiAgICB9O1xuXG4gICAgc2V0dGluZ3Muc2V0KEFWQUlMQUJMRV9QUk9WSURFUlMsIG5ld1ZhbHVlKS5jYXRjaChjb25zb2xlLmVycm9yKTtcblxuICAgIHNldFZhbHVlKG5ld1ZhbHVlKTtcbiAgfTtcbiAgcmV0dXJuIChcbiAgICAvL1RPRE8gUmVtb3ZlIGhhcmQgY29kZWQgY2xhc3MgbmFtZXNcbiAgICA8ZGl2PlxuICAgICAgPGZpZWxkc2V0PlxuICAgICAgICA8bGVnZW5kPnt0aXRsZX08L2xlZ2VuZD5cbiAgICAgICAgPHAgY2xhc3NOYW1lPVwiZmllbGQtZGVzY3JpcHRpb25cIj57ZGVzY308L3A+XG4gICAgICAgIHtPYmplY3Qua2V5cyhpdGVtcykubWFwKGtleSA9PiB7XG4gICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgIDxkaXYga2V5PXtrZXl9IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXAgc21hbGwtZmllbGRcIj5cbiAgICAgICAgICAgICAgPGRpdj5cbiAgICAgICAgICAgICAgICA8aDM+IHtrZXl9PC9oMz5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImlucHV0RmllbGRXcmFwcGVyXCI+XG4gICAgICAgICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICAgICAgICAgICAgdHlwZT1cIm51bWJlclwiXG4gICAgICAgICAgICAgICAgICAgIHZhbHVlPXtzZXR0aW5nVmFsdWVba2V5XX1cbiAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e2UgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgIG9uU2V0dGluZ0NoYW5nZShrZXksIGUpO1xuICAgICAgICAgICAgICAgICAgICB9fVxuICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICApO1xuICAgICAgICB9KX1cbiAgICAgIDwvZmllbGRzZXQ+XG4gICAgPC9kaXY+XG4gICk7XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=