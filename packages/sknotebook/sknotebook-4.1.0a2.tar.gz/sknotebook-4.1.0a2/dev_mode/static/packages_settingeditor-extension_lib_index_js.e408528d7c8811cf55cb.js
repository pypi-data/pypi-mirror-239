"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_settingeditor-extension_lib_index_js"],{

/***/ "../packages/settingeditor-extension/lib/index.js":
/*!********************************************************!*\
  !*** ../packages/settingeditor-extension/lib/index.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/settingeditor/lib/tokens */ "../packages/settingeditor/lib/tokens.js");
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/pluginmanager */ "webpack/sharing/consume/default/@jupyterlab/pluginmanager/@jupyterlab/pluginmanager");
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module settingeditor-extension
 */











/**
 * The command IDs used by the setting editor.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'settingeditor:open';
    CommandIDs.openJSON = 'settingeditor:open-json';
    CommandIDs.revert = 'settingeditor:revert';
    CommandIDs.save = 'settingeditor:save';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default setting editor extension.
 */
const plugin = {
    id: '@jupyterlab/settingeditor-extension:form-ui',
    description: 'Adds the interactive settings editor and provides its tracker.',
    requires: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry,
        _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__.IStateDB,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator,
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.IFormRendererRegistry,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus
    ],
    optional: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette,
        _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__.IJSONSettingEditorTracker,
        _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_5__.IPluginManager
    ],
    autoStart: true,
    provides: _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__.ISettingEditorTracker,
    activate
};
/**
 * Activate the setting editor extension.
 */
function activate(app, registry, state, translator, editorRegistry, status, restorer, palette, jsonEditor, pluginManager) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const namespace = 'setting-editor';
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.open,
            args: widget => ({}),
            name: widget => namespace
        });
    }
    const openUi = async (args) => {
        if (tracker.currentWidget && !tracker.currentWidget.isDisposed) {
            if (!tracker.currentWidget.isAttached) {
                shell.add(tracker.currentWidget, 'main', { type: 'Settings' });
            }
            shell.activateById(tracker.currentWidget.id);
            return;
        }
        const key = plugin.id;
        const { SettingsEditor } = await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_settingeditor_jupyterlab_settingeditor").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/settingeditor */ "webpack/sharing/consume/default/@jupyterlab/settingeditor/@jupyterlab/settingeditor", 23));
        const editor = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
            content: new SettingsEditor({
                editorRegistry,
                key,
                registry,
                state,
                commands,
                toSkip: [
                    '@jupyterlab/application-extension:context-menu',
                    '@jupyterlab/mainmenu-extension:plugin'
                ],
                translator,
                status,
                query: args.query
            })
        });
        editor.toolbar.addItem('spacer', _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.Toolbar.createSpacerItem());
        if (pluginManager) {
            editor.toolbar.addItem('open-plugin-manager', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.ToolbarButton({
                onClick: async () => {
                    await pluginManager.open();
                },
                icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.launchIcon,
                label: trans.__('Plugin Manager')
            }));
        }
        if (jsonEditor) {
            editor.toolbar.addItem('open-json-editor', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.CommandToolbarButton({
                commands,
                id: CommandIDs.openJSON,
                icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.launchIcon,
                label: trans.__('JSON Settings Editor')
            }));
        }
        editor.id = namespace;
        editor.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.settingsIcon;
        editor.title.label = trans.__('Settings');
        editor.title.closable = true;
        void tracker.add(editor);
        shell.add(editor, 'main', { type: 'Settings' });
    };
    commands.addCommand(CommandIDs.open, {
        execute: async (args) => {
            var _a;
            if (args.settingEditorType === 'ui') {
                void commands.execute(CommandIDs.open, { query: (_a = args.query) !== null && _a !== void 0 ? _a : '' });
            }
            else if (args.settingEditorType === 'json') {
                void commands.execute(CommandIDs.openJSON);
            }
            else {
                void registry.load(plugin.id).then(settings => {
                    var _a;
                    settings.get('settingEditorType').composite ===
                        'json'
                        ? void commands.execute(CommandIDs.openJSON)
                        : void openUi({ query: (_a = args.query) !== null && _a !== void 0 ? _a : '' });
                });
            }
        },
        label: args => {
            if (args.label) {
                return args.label;
            }
            return trans.__('Settings Editor');
        }
    });
    if (palette) {
        palette.addItem({
            category: trans.__('Settings'),
            command: CommandIDs.open,
            args: { settingEditorType: 'ui' }
        });
    }
    return tracker;
}
/**
 * The default setting editor extension.
 */
const jsonPlugin = {
    id: '@jupyterlab/settingeditor-extension:plugin',
    description: 'Adds the JSON settings editor and provides its tracker.',
    requires: [
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_6__.ISettingRegistry,
        _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_2__.IEditorServices,
        _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_7__.IStateDB,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_4__.IRenderMimeRegistry,
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabStatus,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_8__.ITranslator
    ],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    autoStart: true,
    provides: _jupyterlab_settingeditor_lib_tokens__WEBPACK_IMPORTED_MODULE_9__.IJSONSettingEditorTracker,
    activate: activateJSON
};
/**
 * Activate the setting editor extension.
 */
function activateJSON(app, registry, editorServices, state, rendermime, status, translator, restorer, palette) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    const namespace = 'json-setting-editor';
    const factoryService = editorServices.factoryService;
    const editorFactory = factoryService.newInlineEditor;
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    // Handle state restoration.
    if (restorer) {
        void restorer.restore(tracker, {
            command: CommandIDs.openJSON,
            args: widget => ({}),
            name: widget => namespace
        });
    }
    commands.addCommand(CommandIDs.openJSON, {
        execute: async () => {
            if (tracker.currentWidget && !tracker.currentWidget.isDisposed) {
                if (!tracker.currentWidget.isAttached) {
                    shell.add(tracker.currentWidget, 'main', {
                        type: 'Advanced Settings'
                    });
                }
                shell.activateById(tracker.currentWidget.id);
                return;
            }
            const key = plugin.id;
            const when = app.restored;
            const { JsonSettingEditor } = await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_settingeditor_jupyterlab_settingeditor").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/settingeditor */ "webpack/sharing/consume/default/@jupyterlab/settingeditor/@jupyterlab/settingeditor", 23));
            const editor = new JsonSettingEditor({
                commands: {
                    registry: commands,
                    revert: CommandIDs.revert,
                    save: CommandIDs.save
                },
                editorFactory,
                key,
                registry,
                rendermime,
                state,
                translator,
                when
            });
            let disposable = null;
            // Notify the command registry when the visibility status of the setting
            // editor's commands change. The setting editor toolbar listens for this
            // signal from the command registry.
            editor.commandsChanged.connect((sender, args) => {
                args.forEach(id => {
                    commands.notifyCommandChanged(id);
                });
                if (editor.canSaveRaw) {
                    if (!disposable) {
                        disposable = status.setDirty();
                    }
                }
                else if (disposable) {
                    disposable.dispose();
                    disposable = null;
                }
                editor.disposed.connect(() => {
                    if (disposable) {
                        disposable.dispose();
                    }
                });
            });
            const container = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({
                content: editor
            });
            container.id = namespace;
            container.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.settingsIcon;
            container.title.label = trans.__('Advanced Settings Editor');
            container.title.closable = true;
            void tracker.add(container);
            shell.add(container, 'main', { type: 'Advanced Settings' });
        },
        label: trans.__('Advanced Settings Editor')
    });
    if (palette) {
        palette.addItem({
            category: trans.__('Settings'),
            command: CommandIDs.openJSON
        });
    }
    commands.addCommand(CommandIDs.revert, {
        execute: () => {
            var _a;
            (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.revert();
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.undoIcon,
        label: trans.__('Revert User Settings'),
        isEnabled: () => { var _a, _b; return (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.canRevertRaw) !== null && _b !== void 0 ? _b : false; }
    });
    commands.addCommand(CommandIDs.save, {
        execute: () => { var _a; return (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.save(); },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.saveIcon,
        label: trans.__('Save User Settings'),
        isEnabled: () => { var _a, _b; return (_b = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.canSaveRaw) !== null && _b !== void 0 ? _b : false; }
    });
    return tracker;
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([plugin, jsonPlugin]);


/***/ }),

/***/ "../packages/settingeditor/lib/tokens.js":
/*!***********************************************!*\
  !*** ../packages/settingeditor/lib/tokens.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IJSONSettingEditorTracker": () => (/* binding */ IJSONSettingEditorTracker),
/* harmony export */   "ISettingEditorTracker": () => (/* binding */ ISettingEditorTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The setting editor tracker token.
 */
const ISettingEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/settingeditor:ISettingEditorTracker', `A widget tracker for the interactive setting editor.
  Use this if you want to be able to iterate over and interact with setting editors
  created by the application.`);
/**
 * The setting editor tracker token.
 */
const IJSONSettingEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/settingeditor:IJSONSettingEditorTracker', `A widget tracker for the JSON setting editor.
  Use this if you want to be able to iterate over and interact with setting editors
  created by the application.`);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfc2V0dGluZ2VkaXRvci1leHRlbnNpb25fbGliX2luZGV4X2pzLmU0MDg1MjhkN2M4ODExY2Y1NWNiLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBTzhCO0FBS0g7QUFDMkI7QUFPdEI7QUFDMEI7QUFJZjtBQUthO0FBQ0k7QUFDaEI7QUFDTztBQUN1QjtBQUc3RTs7R0FFRztBQUNILElBQVUsVUFBVSxDQVFuQjtBQVJELFdBQVUsVUFBVTtJQUNMLGVBQUksR0FBRyxvQkFBb0IsQ0FBQztJQUU1QixtQkFBUSxHQUFHLHlCQUF5QixDQUFDO0lBRXJDLGlCQUFNLEdBQUcsc0JBQXNCLENBQUM7SUFFaEMsZUFBSSxHQUFHLG9CQUFvQixDQUFDO0FBQzNDLENBQUMsRUFSUyxVQUFVLEtBQVYsVUFBVSxRQVFuQjtBQUlEOztHQUVHO0FBQ0gsTUFBTSxNQUFNLEdBQWlEO0lBQzNELEVBQUUsRUFBRSw2Q0FBNkM7SUFDakQsV0FBVyxFQUFFLGdFQUFnRTtJQUM3RSxRQUFRLEVBQUU7UUFDUix5RUFBZ0I7UUFDaEIseURBQVE7UUFDUixnRUFBVztRQUNYLDRFQUFxQjtRQUNyQiwrREFBVTtLQUNYO0lBQ0QsUUFBUSxFQUFFO1FBQ1Isb0VBQWU7UUFDZixpRUFBZTtRQUNmLDJGQUF5QjtRQUN6QixxRUFBYztLQUNmO0lBQ0QsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsdUZBQXFCO0lBQy9CLFFBQVE7Q0FDVCxDQUFDO0FBRUY7O0dBRUc7QUFDSCxTQUFTLFFBQVEsQ0FDZixHQUFvQixFQUNwQixRQUEwQixFQUMxQixLQUFlLEVBQ2YsVUFBdUIsRUFDdkIsY0FBcUMsRUFDckMsTUFBa0IsRUFDbEIsUUFBZ0MsRUFDaEMsT0FBK0IsRUFDL0IsVUFBNEMsRUFDNUMsYUFBb0M7SUFFcEMsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENB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SSxFQUFFO1FBQ3BELElBQUksRUFBRSwrREFBUTtRQUNkLEtBQUssRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLG9CQUFvQixDQUFDO1FBQ3JDLFNBQVMsRUFBRSxHQUFHLEVBQUUsZUFBQywwQkFBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDLFVBQVUsbUNBQUksS0FBSztLQUNwRSxDQUFDLENBQUM7SUFFSCxPQUFPLE9BQU8sQ0FBQztBQUNqQixDQUFDO0FBRUQsaUVBQWUsQ0FBQyxNQUFNLEVBQUUsVUFBVSxDQUFDLEVBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQzFXcEMsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUdqQjtBQUkxQzs7R0FFRztBQUNJLE1BQU0scUJBQXFCLEdBQUcsSUFBSSxvREFBSyxDQUM1QyxpREFBaUQsRUFDakQ7OzhCQUU0QixDQUM3QixDQUFDO0FBRUY7O0dBRUc7QUFDSSxNQUFNLHlCQUF5QixHQUFHLElBQUksb0RBQUssQ0FDaEQscURBQXFELEVBQ3JEOzs4QkFFNEIsQ0FDN0IsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zZXR0aW5nZWRpdG9yLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3NldHRpbmdlZGl0b3Ivc3JjL3Rva2Vucy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHNldHRpbmdlZGl0b3ItZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSUxhYlN0YXR1cyxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBJQ29tbWFuZFBhbGV0dGUsXG4gIE1haW5BcmVhV2lkZ2V0LFxuICBXaWRnZXRUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElFZGl0b3JTZXJ2aWNlcyB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHtcbiAgQ29tbWFuZFRvb2xiYXJCdXR0b24sXG4gIElGb3JtUmVuZGVyZXJSZWdpc3RyeSxcbiAgbGF1bmNoSWNvbixcbiAgVG9vbGJhcixcbiAgVG9vbGJhckJ1dHRvblxufSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IElSZW5kZXJNaW1lUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7XG4gIElKU09OU2V0dGluZ0VkaXRvclRyYWNrZXIsXG4gIElTZXR0aW5nRWRpdG9yVHJhY2tlclxufSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5nZWRpdG9yL2xpYi90b2tlbnMnO1xuaW1wb3J0IHR5cGUge1xuICBKc29uU2V0dGluZ0VkaXRvcixcbiAgU2V0dGluZ3NFZGl0b3Jcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ2VkaXRvcic7XG5pbXBvcnQgeyBJUGx1Z2luTWFuYWdlciB9IGZyb20gJ0BqdXB5dGVybGFiL3BsdWdpbm1hbmFnZXInO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJU3RhdGVEQiB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXRlZGInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBzYXZlSWNvbiwgc2V0dGluZ3NJY29uLCB1bmRvSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBzZXR0aW5nIGVkaXRvci5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdzZXR0aW5nZWRpdG9yOm9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCBvcGVuSlNPTiA9ICdzZXR0aW5nZWRpdG9yOm9wZW4tanNvbic7XG5cbiAgZXhwb3J0IGNvbnN0IHJldmVydCA9ICdzZXR0aW5nZWRpdG9yOnJldmVydCc7XG5cbiAgZXhwb3J0IGNvbnN0IHNhdmUgPSAnc2V0dGluZ2VkaXRvcjpzYXZlJztcbn1cblxudHlwZSBTZXR0aW5nRWRpdG9yVHlwZSA9ICd1aScgfCAnanNvbic7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgc2V0dGluZyBlZGl0b3IgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJU2V0dGluZ0VkaXRvclRyYWNrZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3NldHRpbmdlZGl0b3ItZXh0ZW5zaW9uOmZvcm0tdWknLFxuICBkZXNjcmlwdGlvbjogJ0FkZHMgdGhlIGludGVyYWN0aXZlIHNldHRpbmdzIGVkaXRvciBhbmQgcHJvdmlkZXMgaXRzIHRyYWNrZXIuJyxcbiAgcmVxdWlyZXM6IFtcbiAgICBJU2V0dGluZ1JlZ2lzdHJ5LFxuICAgIElTdGF0ZURCLFxuICAgIElUcmFuc2xhdG9yLFxuICAgIElGb3JtUmVuZGVyZXJSZWdpc3RyeSxcbiAgICBJTGFiU3RhdHVzXG4gIF0sXG4gIG9wdGlvbmFsOiBbXG4gICAgSUxheW91dFJlc3RvcmVyLFxuICAgIElDb21tYW5kUGFsZXR0ZSxcbiAgICBJSlNPTlNldHRpbmdFZGl0b3JUcmFja2VyLFxuICAgIElQbHVnaW5NYW5hZ2VyXG4gIF0sXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcHJvdmlkZXM6IElTZXR0aW5nRWRpdG9yVHJhY2tlcixcbiAgYWN0aXZhdGVcbn07XG5cbi8qKlxuICogQWN0aXZhdGUgdGhlIHNldHRpbmcgZWRpdG9yIGV4dGVuc2lvbi5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICByZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgc3RhdGU6IElTdGF0ZURCLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgZWRpdG9yUmVnaXN0cnk6IElGb3JtUmVuZGVyZXJSZWdpc3RyeSxcbiAgc3RhdHVzOiBJTGFiU3RhdHVzLFxuICByZXN0b3JlcjogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAganNvbkVkaXRvcjogSUpTT05TZXR0aW5nRWRpdG9yVHJhY2tlciB8IG51bGwsXG4gIHBsdWdpbk1hbmFnZXI6IElQbHVnaW5NYW5hZ2VyIHwgbnVsbFxuKTogSVNldHRpbmdFZGl0b3JUcmFja2VyIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgY29uc3QgbmFtZXNwYWNlID0gJ3NldHRpbmctZWRpdG9yJztcbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PFNldHRpbmdzRWRpdG9yPj4oe1xuICAgIG5hbWVzcGFjZVxuICB9KTtcblxuICAvLyBIYW5kbGUgc3RhdGUgcmVzdG9yYXRpb24uXG4gIGlmIChyZXN0b3Jlcikge1xuICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLm9wZW4sXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHt9KSxcbiAgICAgIG5hbWU6IHdpZGdldCA9PiBuYW1lc3BhY2VcbiAgICB9KTtcbiAgfVxuXG4gIGNvbnN0IG9wZW5VaSA9IGFzeW5jIChhcmdzOiB7IHF1ZXJ5OiBzdHJpbmcgfSkgPT4ge1xuICAgIGlmICh0cmFja2VyLmN1cnJlbnRXaWRnZXQgJiYgIXRyYWNrZXIuY3VycmVudFdpZGdldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICBpZiAoIXRyYWNrZXIuY3VycmVudFdpZGdldC5pc0F0dGFjaGVkKSB7XG4gICAgICAgIHNoZWxsLmFkZCh0cmFja2VyLmN1cnJlbnRXaWRnZXQsICdtYWluJywgeyB0eXBlOiAnU2V0dGluZ3MnIH0pO1xuICAgICAgfVxuICAgICAgc2hlbGwuYWN0aXZhdGVCeUlkKHRyYWNrZXIuY3VycmVudFdpZGdldC5pZCk7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3Qga2V5ID0gcGx1Z2luLmlkO1xuXG4gICAgY29uc3QgeyBTZXR0aW5nc0VkaXRvciB9ID0gYXdhaXQgaW1wb3J0KCdAanVweXRlcmxhYi9zZXR0aW5nZWRpdG9yJyk7XG5cbiAgICBjb25zdCBlZGl0b3IgPSBuZXcgTWFpbkFyZWFXaWRnZXQ8U2V0dGluZ3NFZGl0b3I+KHtcbiAgICAgIGNvbnRlbnQ6IG5ldyBTZXR0aW5nc0VkaXRvcih7XG4gICAgICAgIGVkaXRvclJlZ2lzdHJ5LFxuICAgICAgICBrZXksXG4gICAgICAgIHJlZ2lzdHJ5LFxuICAgICAgICBzdGF0ZSxcbiAgICAgICAgY29tbWFuZHMsXG4gICAgICAgIHRvU2tpcDogW1xuICAgICAgICAgICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbi1leHRlbnNpb246Y29udGV4dC1tZW51JyxcbiAgICAgICAgICAnQGp1cHl0ZXJsYWIvbWFpbm1lbnUtZXh0ZW5zaW9uOnBsdWdpbidcbiAgICAgICAgXSxcbiAgICAgICAgdHJhbnNsYXRvcixcbiAgICAgICAgc3RhdHVzLFxuICAgICAgICBxdWVyeTogYXJncy5xdWVyeSBhcyBzdHJpbmdcbiAgICAgIH0pXG4gICAgfSk7XG5cbiAgICBlZGl0b3IudG9vbGJhci5hZGRJdGVtKCdzcGFjZXInLCBUb29sYmFyLmNyZWF0ZVNwYWNlckl0ZW0oKSk7XG4gICAgaWYgKHBsdWdpbk1hbmFnZXIpIHtcbiAgICAgIGVkaXRvci50b29sYmFyLmFkZEl0ZW0oXG4gICAgICAgICdvcGVuLXBsdWdpbi1tYW5hZ2VyJyxcbiAgICAgICAgbmV3IFRvb2xiYXJCdXR0b24oe1xuICAgICAgICAgIG9uQ2xpY2s6IGFzeW5jICgpID0+IHtcbiAgICAgICAgICAgIGF3YWl0IHBsdWdpbk1hbmFnZXIub3BlbigpO1xuICAgICAgICAgIH0sXG4gICAgICAgICAgaWNvbjogbGF1bmNoSWNvbixcbiAgICAgICAgICBsYWJlbDogdHJhbnMuX18oJ1BsdWdpbiBNYW5hZ2VyJylcbiAgICAgICAgfSlcbiAgICAgICk7XG4gICAgfVxuICAgIGlmIChqc29uRWRpdG9yKSB7XG4gICAgICBlZGl0b3IudG9vbGJhci5hZGRJdGVtKFxuICAgICAgICAnb3Blbi1qc29uLWVkaXRvcicsXG4gICAgICAgIG5ldyBDb21tYW5kVG9vbGJhckJ1dHRvbih7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgaWQ6IENvbW1hbmRJRHMub3BlbkpTT04sXG4gICAgICAgICAgaWNvbjogbGF1bmNoSWNvbixcbiAgICAgICAgICBsYWJlbDogdHJhbnMuX18oJ0pTT04gU2V0dGluZ3MgRWRpdG9yJylcbiAgICAgICAgfSlcbiAgICAgICk7XG4gICAgfVxuXG4gICAgZWRpdG9yLmlkID0gbmFtZXNwYWNlO1xuICAgIGVkaXRvci50aXRsZS5pY29uID0gc2V0dGluZ3NJY29uO1xuICAgIGVkaXRvci50aXRsZS5sYWJlbCA9IHRyYW5zLl9fKCdTZXR0aW5ncycpO1xuICAgIGVkaXRvci50aXRsZS5jbG9zYWJsZSA9IHRydWU7XG5cbiAgICB2b2lkIHRyYWNrZXIuYWRkKGVkaXRvcik7XG4gICAgc2hlbGwuYWRkKGVkaXRvciwgJ21haW4nLCB7IHR5cGU6ICdTZXR0aW5ncycgfSk7XG4gIH07XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLm9wZW4sIHtcbiAgICBleGVjdXRlOiBhc3luYyAoYXJnczoge1xuICAgICAgcXVlcnk/OiBzdHJpbmc7XG4gICAgICBzZXR0aW5nRWRpdG9yVHlwZT86IFNldHRpbmdFZGl0b3JUeXBlO1xuICAgIH0pID0+IHtcbiAgICAgIGlmIChhcmdzLnNldHRpbmdFZGl0b3JUeXBlID09PSAndWknKSB7XG4gICAgICAgIHZvaWQgY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLm9wZW4sIHsgcXVlcnk6IGFyZ3MucXVlcnkgPz8gJycgfSk7XG4gICAgICB9IGVsc2UgaWYgKGFyZ3Muc2V0dGluZ0VkaXRvclR5cGUgPT09ICdqc29uJykge1xuICAgICAgICB2b2lkIGNvbW1hbmRzLmV4ZWN1dGUoQ29tbWFuZElEcy5vcGVuSlNPTik7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICB2b2lkIHJlZ2lzdHJ5LmxvYWQocGx1Z2luLmlkKS50aGVuKHNldHRpbmdzID0+IHtcbiAgICAgICAgICAoc2V0dGluZ3MuZ2V0KCdzZXR0aW5nRWRpdG9yVHlwZScpLmNvbXBvc2l0ZSBhcyBTZXR0aW5nRWRpdG9yVHlwZSkgPT09XG4gICAgICAgICAgJ2pzb24nXG4gICAgICAgICAgICA/IHZvaWQgY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLm9wZW5KU09OKVxuICAgICAgICAgICAgOiB2b2lkIG9wZW5VaSh7IHF1ZXJ5OiBhcmdzLnF1ZXJ5ID8/ICcnIH0pO1xuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGxhYmVsOiBhcmdzID0+IHtcbiAgICAgIGlmIChhcmdzLmxhYmVsKSB7XG4gICAgICAgIHJldHVybiBhcmdzLmxhYmVsIGFzIHN0cmluZztcbiAgICAgIH1cbiAgICAgIHJldHVybiB0cmFucy5fXygnU2V0dGluZ3MgRWRpdG9yJyk7XG4gICAgfVxuICB9KTtcblxuICBpZiAocGFsZXR0ZSkge1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ1NldHRpbmdzJyksXG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLm9wZW4sXG4gICAgICBhcmdzOiB7IHNldHRpbmdFZGl0b3JUeXBlOiAndWknIH1cbiAgICB9KTtcbiAgfVxuXG4gIHJldHVybiB0cmFja2VyO1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHNldHRpbmcgZWRpdG9yIGV4dGVuc2lvbi5cbiAqL1xuY29uc3QganNvblBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElKU09OU2V0dGluZ0VkaXRvclRyYWNrZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3NldHRpbmdlZGl0b3ItZXh0ZW5zaW9uOnBsdWdpbicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyB0aGUgSlNPTiBzZXR0aW5ncyBlZGl0b3IgYW5kIHByb3ZpZGVzIGl0cyB0cmFja2VyLicsXG4gIHJlcXVpcmVzOiBbXG4gICAgSVNldHRpbmdSZWdpc3RyeSxcbiAgICBJRWRpdG9yU2VydmljZXMsXG4gICAgSVN0YXRlREIsXG4gICAgSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgICBJTGFiU3RhdHVzLFxuICAgIElUcmFuc2xhdG9yXG4gIF0sXG4gIG9wdGlvbmFsOiBbSUxheW91dFJlc3RvcmVyLCBJQ29tbWFuZFBhbGV0dGVdLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJSlNPTlNldHRpbmdFZGl0b3JUcmFja2VyLFxuICBhY3RpdmF0ZTogYWN0aXZhdGVKU09OXG59O1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBzZXR0aW5nIGVkaXRvciBleHRlbnNpb24uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlSlNPTihcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5LFxuICBlZGl0b3JTZXJ2aWNlczogSUVkaXRvclNlcnZpY2VzLFxuICBzdGF0ZTogSVN0YXRlREIsXG4gIHJlbmRlcm1pbWU6IElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIHN0YXR1czogSUxhYlN0YXR1cyxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHJlc3RvcmVyOiBJTGF5b3V0UmVzdG9yZXIgfCBudWxsLFxuICBwYWxldHRlOiBJQ29tbWFuZFBhbGV0dGUgfCBudWxsXG4pOiBJSlNPTlNldHRpbmdFZGl0b3JUcmFja2VyIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgY29uc3QgbmFtZXNwYWNlID0gJ2pzb24tc2V0dGluZy1lZGl0b3InO1xuICBjb25zdCBmYWN0b3J5U2VydmljZSA9IGVkaXRvclNlcnZpY2VzLmZhY3RvcnlTZXJ2aWNlO1xuICBjb25zdCBlZGl0b3JGYWN0b3J5ID0gZmFjdG9yeVNlcnZpY2UubmV3SW5saW5lRWRpdG9yO1xuICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8SnNvblNldHRpbmdFZGl0b3I+Pih7XG4gICAgbmFtZXNwYWNlXG4gIH0pO1xuXG4gIC8vIEhhbmRsZSBzdGF0ZSByZXN0b3JhdGlvbi5cbiAgaWYgKHJlc3RvcmVyKSB7XG4gICAgdm9pZCByZXN0b3Jlci5yZXN0b3JlKHRyYWNrZXIsIHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlbkpTT04sXG4gICAgICBhcmdzOiB3aWRnZXQgPT4gKHt9KSxcbiAgICAgIG5hbWU6IHdpZGdldCA9PiBuYW1lc3BhY2VcbiAgICB9KTtcbiAgfVxuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuSlNPTiwge1xuICAgIGV4ZWN1dGU6IGFzeW5jICgpID0+IHtcbiAgICAgIGlmICh0cmFja2VyLmN1cnJlbnRXaWRnZXQgJiYgIXRyYWNrZXIuY3VycmVudFdpZGdldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIGlmICghdHJhY2tlci5jdXJyZW50V2lkZ2V0LmlzQXR0YWNoZWQpIHtcbiAgICAgICAgICBzaGVsbC5hZGQodHJhY2tlci5jdXJyZW50V2lkZ2V0LCAnbWFpbicsIHtcbiAgICAgICAgICAgIHR5cGU6ICdBZHZhbmNlZCBTZXR0aW5ncydcbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgICBzaGVsbC5hY3RpdmF0ZUJ5SWQodHJhY2tlci5jdXJyZW50V2lkZ2V0LmlkKTtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuXG4gICAgICBjb25zdCBrZXkgPSBwbHVnaW4uaWQ7XG4gICAgICBjb25zdCB3aGVuID0gYXBwLnJlc3RvcmVkO1xuXG4gICAgICBjb25zdCB7IEpzb25TZXR0aW5nRWRpdG9yIH0gPSBhd2FpdCBpbXBvcnQoJ0BqdXB5dGVybGFiL3NldHRpbmdlZGl0b3InKTtcblxuICAgICAgY29uc3QgZWRpdG9yID0gbmV3IEpzb25TZXR0aW5nRWRpdG9yKHtcbiAgICAgICAgY29tbWFuZHM6IHtcbiAgICAgICAgICByZWdpc3RyeTogY29tbWFuZHMsXG4gICAgICAgICAgcmV2ZXJ0OiBDb21tYW5kSURzLnJldmVydCxcbiAgICAgICAgICBzYXZlOiBDb21tYW5kSURzLnNhdmVcbiAgICAgICAgfSxcbiAgICAgICAgZWRpdG9yRmFjdG9yeSxcbiAgICAgICAga2V5LFxuICAgICAgICByZWdpc3RyeSxcbiAgICAgICAgcmVuZGVybWltZSxcbiAgICAgICAgc3RhdGUsXG4gICAgICAgIHRyYW5zbGF0b3IsXG4gICAgICAgIHdoZW5cbiAgICAgIH0pO1xuXG4gICAgICBsZXQgZGlzcG9zYWJsZTogSURpc3Bvc2FibGUgfCBudWxsID0gbnVsbDtcbiAgICAgIC8vIE5vdGlmeSB0aGUgY29tbWFuZCByZWdpc3RyeSB3aGVuIHRoZSB2aXNpYmlsaXR5IHN0YXR1cyBvZiB0aGUgc2V0dGluZ1xuICAgICAgLy8gZWRpdG9yJ3MgY29tbWFuZHMgY2hhbmdlLiBUaGUgc2V0dGluZyBlZGl0b3IgdG9vbGJhciBsaXN0ZW5zIGZvciB0aGlzXG4gICAgICAvLyBzaWduYWwgZnJvbSB0aGUgY29tbWFuZCByZWdpc3RyeS5cbiAgICAgIGVkaXRvci5jb21tYW5kc0NoYW5nZWQuY29ubmVjdCgoc2VuZGVyOiBhbnksIGFyZ3M6IHN0cmluZ1tdKSA9PiB7XG4gICAgICAgIGFyZ3MuZm9yRWFjaChpZCA9PiB7XG4gICAgICAgICAgY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoaWQpO1xuICAgICAgICB9KTtcbiAgICAgICAgaWYgKGVkaXRvci5jYW5TYXZlUmF3KSB7XG4gICAgICAgICAgaWYgKCFkaXNwb3NhYmxlKSB7XG4gICAgICAgICAgICBkaXNwb3NhYmxlID0gc3RhdHVzLnNldERpcnR5KCk7XG4gICAgICAgICAgfVxuICAgICAgICB9IGVsc2UgaWYgKGRpc3Bvc2FibGUpIHtcbiAgICAgICAgICBkaXNwb3NhYmxlLmRpc3Bvc2UoKTtcbiAgICAgICAgICBkaXNwb3NhYmxlID0gbnVsbDtcbiAgICAgICAgfVxuICAgICAgICBlZGl0b3IuZGlzcG9zZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgICAgaWYgKGRpc3Bvc2FibGUpIHtcbiAgICAgICAgICAgIGRpc3Bvc2FibGUuZGlzcG9zZSgpO1xuICAgICAgICAgIH1cbiAgICAgICAgfSk7XG4gICAgICB9KTtcblxuICAgICAgY29uc3QgY29udGFpbmVyID0gbmV3IE1haW5BcmVhV2lkZ2V0PEpzb25TZXR0aW5nRWRpdG9yPih7XG4gICAgICAgIGNvbnRlbnQ6IGVkaXRvclxuICAgICAgfSk7XG5cbiAgICAgIGNvbnRhaW5lci5pZCA9IG5hbWVzcGFjZTtcbiAgICAgIGNvbnRhaW5lci50aXRsZS5pY29uID0gc2V0dGluZ3NJY29uO1xuICAgICAgY29udGFpbmVyLnRpdGxlLmxhYmVsID0gdHJhbnMuX18oJ0FkdmFuY2VkIFNldHRpbmdzIEVkaXRvcicpO1xuICAgICAgY29udGFpbmVyLnRpdGxlLmNsb3NhYmxlID0gdHJ1ZTtcblxuICAgICAgdm9pZCB0cmFja2VyLmFkZChjb250YWluZXIpO1xuICAgICAgc2hlbGwuYWRkKGNvbnRhaW5lciwgJ21haW4nLCB7IHR5cGU6ICdBZHZhbmNlZCBTZXR0aW5ncycgfSk7XG4gICAgfSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0FkdmFuY2VkIFNldHRpbmdzIEVkaXRvcicpXG4gIH0pO1xuICBpZiAocGFsZXR0ZSkge1xuICAgIHBhbGV0dGUuYWRkSXRlbSh7XG4gICAgICBjYXRlZ29yeTogdHJhbnMuX18oJ1NldHRpbmdzJyksXG4gICAgICBjb21tYW5kOiBDb21tYW5kSURzLm9wZW5KU09OXG4gICAgfSk7XG4gIH1cblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMucmV2ZXJ0LCB7XG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50LnJldmVydCgpO1xuICAgIH0sXG4gICAgaWNvbjogdW5kb0ljb24sXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSZXZlcnQgVXNlciBTZXR0aW5ncycpLFxuICAgIGlzRW5hYmxlZDogKCkgPT4gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50LmNhblJldmVydFJhdyA/PyBmYWxzZVxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2F2ZSwge1xuICAgIGV4ZWN1dGU6ICgpID0+IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudC5zYXZlKCksXG4gICAgaWNvbjogc2F2ZUljb24sXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTYXZlIFVzZXIgU2V0dGluZ3MnKSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudC5jYW5TYXZlUmF3ID8/IGZhbHNlXG4gIH0pO1xuXG4gIHJldHVybiB0cmFja2VyO1xufVxuXG5leHBvcnQgZGVmYXVsdCBbcGx1Z2luLCBqc29uUGx1Z2luXTtcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVdpZGdldFRyYWNrZXIsIE1haW5BcmVhV2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBKc29uU2V0dGluZ0VkaXRvciBhcyBKU09OU2V0dGluZ0VkaXRvciB9IGZyb20gJy4vanNvbnNldHRpbmdlZGl0b3InO1xuaW1wb3J0IHsgU2V0dGluZ3NFZGl0b3IgfSBmcm9tICcuL3NldHRpbmdzZWRpdG9yJztcblxuLyoqXG4gKiBUaGUgc2V0dGluZyBlZGl0b3IgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElTZXR0aW5nRWRpdG9yVHJhY2tlciA9IG5ldyBUb2tlbjxJU2V0dGluZ0VkaXRvclRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvc2V0dGluZ2VkaXRvcjpJU2V0dGluZ0VkaXRvclRyYWNrZXInLFxuICBgQSB3aWRnZXQgdHJhY2tlciBmb3IgdGhlIGludGVyYWN0aXZlIHNldHRpbmcgZWRpdG9yLlxuICBVc2UgdGhpcyBpZiB5b3Ugd2FudCB0byBiZSBhYmxlIHRvIGl0ZXJhdGUgb3ZlciBhbmQgaW50ZXJhY3Qgd2l0aCBzZXR0aW5nIGVkaXRvcnNcbiAgY3JlYXRlZCBieSB0aGUgYXBwbGljYXRpb24uYFxuKTtcblxuLyoqXG4gKiBUaGUgc2V0dGluZyBlZGl0b3IgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElKU09OU2V0dGluZ0VkaXRvclRyYWNrZXIgPSBuZXcgVG9rZW48SUpTT05TZXR0aW5nRWRpdG9yVHJhY2tlcj4oXG4gICdAanVweXRlcmxhYi9zZXR0aW5nZWRpdG9yOklKU09OU2V0dGluZ0VkaXRvclRyYWNrZXInLFxuICBgQSB3aWRnZXQgdHJhY2tlciBmb3IgdGhlIEpTT04gc2V0dGluZyBlZGl0b3IuXG4gIFVzZSB0aGlzIGlmIHlvdSB3YW50IHRvIGJlIGFibGUgdG8gaXRlcmF0ZSBvdmVyIGFuZCBpbnRlcmFjdCB3aXRoIHNldHRpbmcgZWRpdG9yc1xuICBjcmVhdGVkIGJ5IHRoZSBhcHBsaWNhdGlvbi5gXG4pO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgdGhlIHNldHRpbmcgZWRpdG9yLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElKU09OU2V0dGluZ0VkaXRvclRyYWNrZXJcbiAgZXh0ZW5kcyBJV2lkZ2V0VHJhY2tlcjxNYWluQXJlYVdpZGdldDxKU09OU2V0dGluZ0VkaXRvcj4+IHt9XG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IHRyYWNrcyB0aGUgc2V0dGluZyBlZGl0b3IuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVNldHRpbmdFZGl0b3JUcmFja2VyXG4gIGV4dGVuZHMgSVdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8U2V0dGluZ3NFZGl0b3I+PiB7fVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9