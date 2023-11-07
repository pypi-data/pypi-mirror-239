"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_codemirror-extension_lib_index_js"],{

/***/ "../packages/codemirror-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/codemirror-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "lineColItem": () => (/* binding */ lineColItem)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _services__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./services */ "../packages/codemirror-extension/lib/services.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module codemirror-extension
 */





/**
 * A plugin providing a line/column status item to the application.
 */
const lineColItem = {
    id: '@jupyterlab/codemirror-extension:line-col-status',
    description: 'Provides the code editor cursor position model.',
    autoStart: true,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_2__.IStatusBar],
    provides: _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.IPositionModel,
    activate: (app, translator, labShell, statusBar) => {
        const item = new _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.LineCol(translator);
        const providers = new Set();
        if (statusBar) {
            // Add the status item to the status bar.
            statusBar.registerStatusItem(lineColItem.id, {
                item,
                align: 'right',
                rank: 2,
                isActive: () => !!item.model.editor
            });
        }
        const addEditorProvider = (provider) => {
            providers.add(provider);
            if (app.shell.currentWidget) {
                updateEditor(app.shell, {
                    newValue: app.shell.currentWidget,
                    oldValue: null
                });
            }
        };
        const update = () => {
            updateEditor(app.shell, {
                oldValue: app.shell.currentWidget,
                newValue: app.shell.currentWidget
            });
        };
        function updateEditor(shell, changes) {
            Promise.all([...providers].map(provider => provider(changes.newValue)))
                .then(editors => {
                var _a;
                item.model.editor =
                    (_a = editors.filter(editor => editor !== null)[0]) !== null && _a !== void 0 ? _a : null;
            })
                .catch(reason => {
                console.error('Get editors', reason);
            });
        }
        if (labShell) {
            labShell.currentChanged.connect(updateEditor);
        }
        return { addEditorProvider, update };
    }
};
/**
 * Export the plugins as default.
 */
const plugins = [
    _services__WEBPACK_IMPORTED_MODULE_4__.languagePlugin,
    _services__WEBPACK_IMPORTED_MODULE_4__.themePlugin,
    _services__WEBPACK_IMPORTED_MODULE_4__.bindingPlugin,
    _services__WEBPACK_IMPORTED_MODULE_4__.extensionPlugin,
    _services__WEBPACK_IMPORTED_MODULE_4__.servicesPlugin,
    lineColItem
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "../packages/codemirror-extension/lib/services.js":
/*!********************************************************!*\
  !*** ../packages/codemirror-extension/lib/services.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "bindingPlugin": () => (/* binding */ bindingPlugin),
/* harmony export */   "extensionPlugin": () => (/* binding */ extensionPlugin),
/* harmony export */   "languagePlugin": () => (/* binding */ languagePlugin),
/* harmony export */   "servicesPlugin": () => (/* binding */ servicesPlugin),
/* harmony export */   "themePlugin": () => (/* binding */ themePlugin)
/* harmony export */ });
/* harmony import */ var _codemirror_language__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @codemirror/language */ "webpack/sharing/consume/default/@codemirror/language/@codemirror/language");
/* harmony import */ var _codemirror_language__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_codemirror_language__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @rjsf/validator-ajv8 */ "webpack/sharing/consume/default/@rjsf/validator-ajv8/@rjsf/validator-ajv8");
/* harmony import */ var _rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_8__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */









/**
 * CodeMirror settings plugin ID
 */
const SETTINGS_ID = '@jupyterlab/codemirror-extension:plugin';
/**
 * CodeMirror language registry provider.
 */
const languagePlugin = {
    id: '@jupyterlab/codemirror-extension:languages',
    description: 'Provides the CodeMirror languages registry.',
    provides: _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorLanguageRegistry,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    activate: (app, translator) => {
        const languages = new _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.EditorLanguageRegistry();
        // Register default languages
        for (const language of _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.EditorLanguageRegistry.getDefaultLanguages(translator)) {
            languages.addLanguage(language);
        }
        // Add Jupyter Markdown flavor here to support
        // code block highlighting.
        languages.addLanguage({
            name: 'ipythongfm',
            mime: 'text/x-ipythongfm',
            load: async () => {
                const [m, tex] = await Promise.all([
                    __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_codemirror_lang-markdown_codemirror_lang-markdown").then(__webpack_require__.t.bind(__webpack_require__, /*! @codemirror/lang-markdown */ "webpack/sharing/consume/default/@codemirror/lang-markdown/@codemirror/lang-markdown", 23)),
                    __webpack_require__.e(/*! import() */ "node_modules_codemirror_legacy-modes_mode_stex_js").then(__webpack_require__.bind(__webpack_require__, /*! @codemirror/legacy-modes/mode/stex */ "../node_modules/@codemirror/legacy-modes/mode/stex.js"))
                ]);
                return m.markdown({
                    base: m.markdownLanguage,
                    codeLanguages: (info) => languages.findBest(info),
                    extensions: [
                        (0,_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.parseMathIPython)(_codemirror_language__WEBPACK_IMPORTED_MODULE_0__.StreamLanguage.define(tex.stexMath).parser)
                    ]
                });
            }
        });
        return languages;
    }
};
/**
 * CodeMirror theme registry provider.
 */
const themePlugin = {
    id: '@jupyterlab/codemirror-extension:themes',
    description: 'Provides the CodeMirror theme registry',
    provides: _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorThemeRegistry,
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    activate: (app, translator) => {
        const themes = new _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.EditorThemeRegistry();
        // Register default themes
        for (const theme of _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.EditorThemeRegistry.getDefaultThemes(translator)) {
            themes.addTheme(theme);
        }
        return themes;
    }
};
/**
 * CodeMirror editor extensions registry provider.
 */
const extensionPlugin = {
    id: '@jupyterlab/codemirror-extension:extensions',
    description: 'Provides the CodeMirror extension factory registry.',
    provides: _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorExtensionRegistry,
    requires: [_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorThemeRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.IFormRendererRegistry],
    activate: (app, themes, translator, settingRegistry, formRegistry) => {
        const registry = new _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.EditorExtensionRegistry();
        // Register default extensions
        for (const extensionFactory of _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.EditorExtensionRegistry.getDefaultExtensions({
            themes,
            translator
        })) {
            registry.addExtension(extensionFactory);
        }
        if (settingRegistry) {
            const updateSettings = (settings) => {
                var _a;
                registry.baseConfiguration =
                    (_a = settings.get('defaultConfig').composite) !== null && _a !== void 0 ? _a : {};
            };
            void Promise.all([
                settingRegistry.load(SETTINGS_ID),
                app.restored
            ]).then(([settings]) => {
                updateSettings(settings);
                settings.changed.connect(updateSettings);
            });
            formRegistry === null || formRegistry === void 0 ? void 0 : formRegistry.addRenderer(`${SETTINGS_ID}.defaultConfig`, {
                fieldRenderer: (props) => {
                    const properties = react__WEBPACK_IMPORTED_MODULE_8___default().useMemo(() => registry.settingsSchema, []);
                    const defaultFormData = {};
                    // Only provide customizable options
                    for (const [key, value] of Object.entries(registry.defaultConfiguration)) {
                        if (typeof properties[key] !== 'undefined') {
                            defaultFormData[key] = value;
                        }
                    }
                    return (react__WEBPACK_IMPORTED_MODULE_8___default().createElement("div", { className: "jp-FormGroup-contentNormal" },
                        react__WEBPACK_IMPORTED_MODULE_8___default().createElement("h3", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, props.schema.title),
                        props.schema.description && (react__WEBPACK_IMPORTED_MODULE_8___default().createElement("div", { className: "jp-FormGroup-description" }, props.schema.description)),
                        react__WEBPACK_IMPORTED_MODULE_8___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.FormComponent, { schema: {
                                title: props.schema.title,
                                description: props.schema.description,
                                type: 'object',
                                properties,
                                additionalProperties: false
                            }, validator: (_rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_7___default()), formData: { ...defaultFormData, ...props.formData }, formContext: { defaultFormData }, liveValidate: true, onChange: e => {
                                var _a;
                                // Only save non-default values
                                const nonDefault = {};
                                for (const [property, value] of Object.entries((_a = e.formData) !== null && _a !== void 0 ? _a : {})) {
                                    const default_ = defaultFormData[property];
                                    if (default_ === undefined ||
                                        !_lumino_coreutils__WEBPACK_IMPORTED_MODULE_6__.JSONExt.deepEqual(value, default_)) {
                                        nonDefault[property] = value;
                                    }
                                }
                                props.onChange(nonDefault);
                            }, tagName: "div", translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.nullTranslator })));
                }
            });
        }
        return registry;
    }
};
/**
 * CodeMirror shared model binding provider.
 */
const bindingPlugin = {
    id: '@jupyterlab/codemirror-extension:binding',
    description: 'Register the CodeMirror extension factory binding the editor and the shared model.',
    autoStart: true,
    requires: [_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorExtensionRegistry],
    activate: (app, extensions) => {
        extensions.addExtension({
            name: 'shared-model-binding',
            factory: options => {
                var _a;
                const sharedModel = options.model.sharedModel;
                return _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.EditorExtensionRegistry.createImmutableExtension((0,_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.ybinding)({
                    ytext: sharedModel.ysource,
                    undoManager: (_a = sharedModel.undoManager) !== null && _a !== void 0 ? _a : undefined
                }));
            }
        });
    }
};
/**
 * The editor services.
 */
const servicesPlugin = {
    id: '@jupyterlab/codemirror-extension:services',
    description: 'Provides the service to instantiate CodeMirror editors.',
    provides: _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_1__.IEditorServices,
    requires: [
        _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorLanguageRegistry,
        _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorExtensionRegistry,
        _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorThemeRegistry
    ],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    activate: (app, languages, extensions, translator) => {
        const factory = new _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.CodeMirrorEditorFactory({
            extensions,
            languages,
            translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.nullTranslator
        });
        return {
            factoryService: factory,
            mimeTypeService: new _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.CodeMirrorMimeTypeService(languages)
        };
    }
};


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY29kZW1pcnJvci1leHRlbnNpb25fbGliX2luZGV4X2pzLmU2M2QwY2QzZWE3Y2JmMTIzMjRjLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDNEM7QUFDMUI7QUFDRztBQVFsQztBQUVwQjs7R0FFRztBQUNJLE1BQU0sV0FBVyxHQUEwQztJQUNoRSxFQUFFLEVBQUUsa0RBQWtEO0lBQ3RELFdBQVcsRUFBRSxpREFBaUQ7SUFDOUQsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FBQyxnRUFBVyxDQUFDO0lBQ3ZCLFFBQVEsRUFBRSxDQUFDLDhEQUFTLEVBQUUsNkRBQVUsQ0FBQztJQUNqQyxRQUFRLEVBQUUsa0VBQWM7SUFDeEIsUUFBUSxFQUFFLENBQ1IsR0FBb0IsRUFDcEIsVUFBdUIsRUFDdkIsUUFBMEIsRUFDMUIsU0FBNEIsRUFDWixFQUFFO1FBQ2xCLE1BQU0sSUFBSSxHQUFHLElBQUksMkRBQU8sQ0FBQyxVQUFVLENBQUMsQ0FBQztRQUVyQyxNQUFNLFNBQVMsR0FBRyxJQUFJLEdBQUcsRUFFdEIsQ0FBQztRQUVKLElBQUksU0FBUyxFQUFFO1lBQ2IseUNBQXlDO1lBQ3pDLFNBQVMsQ0FBQyxrQkFBa0IsQ0FBQyxXQUFXLENBQUMsRUFBRSxFQUFFO2dCQUMzQyxJQUFJO2dCQUNKLEtBQUssRUFBRSxPQUFPO2dCQUNkLElBQUksRUFBRSxDQUFDO2dCQUNQLFFBQVEsRUFBRSxHQUFHLEVBQUUsQ0FBQyxDQUFDLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNO2FBQ3BDLENBQUMsQ0FBQztTQUNKO1FBRUQsTUFBTSxpQkFBaUIsR0FBRyxDQUN4QixRQUF1RSxFQUNqRSxFQUFFO1lBQ1IsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQztZQUV4QixJQUFJLEdBQUcsQ0FBQyxLQUFLLENBQUMsYUFBYSxFQUFF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LFdBQVcsRUFBRSx5REFBeUQ7SUFDdEUsUUFBUSxFQUFFLG1FQUFlO0lBQ3pCLFFBQVEsRUFBRTtRQUNSLDJFQUF1QjtRQUN2Qiw0RUFBd0I7UUFDeEIsd0VBQW9CO0tBQ3JCO0lBQ0QsUUFBUSxFQUFFLENBQUMsZ0VBQVcsQ0FBQztJQUN2QixRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixTQUFrQyxFQUNsQyxVQUFvQyxFQUNwQyxVQUE4QixFQUNiLEVBQUU7UUFDbkIsTUFBTSxPQUFPLEdBQUcsSUFBSSwyRUFBdUIsQ0FBQztZQUMxQyxVQUFVO1lBQ1YsU0FBUztZQUNULFVBQVUsRUFBRSxVQUFVLGFBQVYsVUFBVSxjQUFWLFVBQVUsR0FBSSxtRUFBYztTQUN6QyxDQUFDLENBQUM7UUFDSCxPQUFPO1lBQ0wsY0FBYyxFQUFFLE9BQU87WUFDdkIsZUFBZSxFQUFFLElBQUksNkVBQXlCLENBQUMsU0FBUyxDQUFDO1NBQzFELENBQUM7SUFDSixDQUFDO0NBQ0YsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9jb2RlbWlycm9yLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NvZGVtaXJyb3ItZXh0ZW5zaW9uL3NyYy9zZXJ2aWNlcy50c3giXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY29kZW1pcnJvci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU2hlbGwsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IENvZGVFZGl0b3IsIElQb3NpdGlvbk1vZGVsLCBMaW5lQ29sIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBJU3RhdHVzQmFyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdHVzYmFyJztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7XG4gIGJpbmRpbmdQbHVnaW4sXG4gIGV4dGVuc2lvblBsdWdpbixcbiAgbGFuZ3VhZ2VQbHVnaW4sXG4gIHNlcnZpY2VzUGx1Z2luLFxuICB0aGVtZVBsdWdpblxufSBmcm9tICcuL3NlcnZpY2VzJztcblxuLyoqXG4gKiBBIHBsdWdpbiBwcm92aWRpbmcgYSBsaW5lL2NvbHVtbiBzdGF0dXMgaXRlbSB0byB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjb25zdCBsaW5lQ29sSXRlbTogSnVweXRlckZyb250RW5kUGx1Z2luPElQb3NpdGlvbk1vZGVsPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9jb2RlbWlycm9yLWV4dGVuc2lvbjpsaW5lLWNvbC1zdGF0dXMnLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBjb2RlIGVkaXRvciBjdXJzb3IgcG9zaXRpb24gbW9kZWwuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yXSxcbiAgb3B0aW9uYWw6IFtJTGFiU2hlbGwsIElTdGF0dXNCYXJdLFxuICBwcm92aWRlczogSVBvc2l0aW9uTW9kZWwsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGwsXG4gICAgc3RhdHVzQmFyOiBJU3RhdHVzQmFyIHwgbnVsbFxuICApOiBJUG9zaXRpb25Nb2RlbCA9PiB7XG4gICAgY29uc3QgaXRlbSA9IG5ldyBMaW5lQ29sKHRyYW5zbGF0b3IpO1xuXG4gICAgY29uc3QgcHJvdmlkZXJzID0gbmV3IFNldDxcbiAgICAgICh3aWRnZXQ6IFdpZGdldCB8IG51bGwpID0+IFByb21pc2U8Q29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbD5cbiAgICA+KCk7XG5cbiAgICBpZiAoc3RhdHVzQmFyKSB7XG4gICAgICAvLyBBZGQgdGhlIHN0YXR1cyBpdGVtIHRvIHRoZSBzdGF0dXMgYmFyLlxuICAgICAgc3RhdHVzQmFyLnJlZ2lzdGVyU3RhdHVzSXRlbShsaW5lQ29sSXRlbS5pZCwge1xuICAgICAgICBpdGVtLFxuICAgICAgICBhbGlnbjogJ3JpZ2h0JyxcbiAgICAgICAgcmFuazogMixcbiAgICAgICAgaXNBY3RpdmU6ICgpID0+ICEhaXRlbS5tb2RlbC5lZGl0b3JcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGNvbnN0IGFkZEVkaXRvclByb3ZpZGVyID0gKFxuICAgICAgcHJvdmlkZXI6ICh3aWRnZXQ6IFdpZGdldCB8IG51bGwpID0+IFByb21pc2U8Q29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbD5cbiAgICApOiB2b2lkID0+IHtcbiAgICAgIHByb3ZpZGVycy5hZGQocHJvdmlkZXIpO1xuXG4gICAgICBpZiAoYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgdXBkYXRlRWRpdG9yKGFwcC5zaGVsbCwge1xuICAgICAgICAgIG5ld1ZhbHVlOiBhcHAuc2hlbGwuY3VycmVudFdpZGdldCxcbiAgICAgICAgICBvbGRWYWx1ZTogbnVsbFxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9O1xuXG4gICAgY29uc3QgdXBkYXRlID0gKCk6IHZvaWQgPT4ge1xuICAgICAgdXBkYXRlRWRpdG9yKGFwcC5zaGVsbCwge1xuICAgICAgICBvbGRWYWx1ZTogYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQsXG4gICAgICAgIG5ld1ZhbHVlOiBhcHAuc2hlbGwuY3VycmVudFdpZGdldFxuICAgICAgfSk7XG4gICAgfTtcblxuICAgIGZ1bmN0aW9uIHVwZGF0ZUVkaXRvcihcbiAgICAgIHNoZWxsOiBKdXB5dGVyRnJvbnRFbmQuSVNoZWxsLFxuICAgICAgY2hhbmdlczogSUxhYlNoZWxsLklDaGFuZ2VkQXJnc1xuICAgICkge1xuICAgICAgUHJvbWlzZS5hbGwoWy4uLnByb3ZpZGVyc10ubWFwKHByb3ZpZGVyID0+IHByb3ZpZGVyKGNoYW5nZXMubmV3VmFsdWUpKSlcbiAgICAgICAgLnRoZW4oZWRpdG9ycyA9PiB7XG4gICAgICAgICAgaXRlbS5tb2RlbC5lZGl0b3IgPVxuICAgICAgICAgICAgZWRpdG9ycy5maWx0ZXIoZWRpdG9yID0+IGVkaXRvciAhPT0gbnVsbClbMF0gPz8gbnVsbDtcbiAgICAgICAgfSlcbiAgICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgICAgY29uc29sZS5lcnJvcignR2V0IGVkaXRvcnMnLCByZWFzb24pO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBpZiAobGFiU2hlbGwpIHtcbiAgICAgIGxhYlNoZWxsLmN1cnJlbnRDaGFuZ2VkLmNvbm5lY3QodXBkYXRlRWRpdG9yKTtcbiAgICB9XG5cbiAgICByZXR1cm4geyBhZGRFZGl0b3JQcm92aWRlciwgdXBkYXRlIH07XG4gIH1cbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW5zIGFzIGRlZmF1bHQuXG4gKi9cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbXG4gIGxhbmd1YWdlUGx1Z2luLFxuICB0aGVtZVBsdWdpbixcbiAgYmluZGluZ1BsdWdpbixcbiAgZXh0ZW5zaW9uUGx1Z2luLFxuICBzZXJ2aWNlc1BsdWdpbixcbiAgbGluZUNvbEl0ZW1cbl07XG5leHBvcnQgZGVmYXVsdCBwbHVnaW5zO1xuIiwiLypcbiAqIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuICogRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbiAqL1xuXG5pbXBvcnQgeyBTdHJlYW1MYW5ndWFnZSB9IGZyb20gJ0Bjb2RlbWlycm9yL2xhbmd1YWdlJztcbmltcG9ydCB7IElZVGV4dCB9IGZyb20gJ0BqdXB5dGVyL3lkb2MnO1xuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgSUVkaXRvclNlcnZpY2VzIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQge1xuICBDb2RlTWlycm9yRWRpdG9yRmFjdG9yeSxcbiAgQ29kZU1pcnJvck1pbWVUeXBlU2VydmljZSxcbiAgRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnksXG4gIEVkaXRvckxhbmd1YWdlUmVnaXN0cnksXG4gIEVkaXRvclRoZW1lUmVnaXN0cnksXG4gIElFZGl0b3JFeHRlbnNpb25SZWdpc3RyeSxcbiAgSUVkaXRvckxhbmd1YWdlUmVnaXN0cnksXG4gIElFZGl0b3JUaGVtZVJlZ2lzdHJ5LFxuICBwYXJzZU1hdGhJUHl0aG9uLFxuICB5YmluZGluZ1xufSBmcm9tICdAanVweXRlcmxhYi9jb2RlbWlycm9yJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgRm9ybUNvbXBvbmVudCxcbiAgSUZvcm1SZW5kZXJlclJlZ2lzdHJ5XG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgSlNPTkV4dCwgUmVhZG9ubHlKU09OVmFsdWUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgdHlwZSB7IEZpZWxkUHJvcHMgfSBmcm9tICdAcmpzZi91dGlscyc7XG5pbXBvcnQgdmFsaWRhdG9yQWp2OCBmcm9tICdAcmpzZi92YWxpZGF0b3ItYWp2OCc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG4vKipcbiAqIENvZGVNaXJyb3Igc2V0dGluZ3MgcGx1Z2luIElEXG4gKi9cbmNvbnN0IFNFVFRJTkdTX0lEID0gJ0BqdXB5dGVybGFiL2NvZGVtaXJyb3ItZXh0ZW5zaW9uOnBsdWdpbic7XG5cbi8qKlxuICogQ29kZU1pcnJvciBsYW5ndWFnZSByZWdpc3RyeSBwcm92aWRlci5cbiAqL1xuZXhwb3J0IGNvbnN0IGxhbmd1YWdlUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUVkaXRvckxhbmd1YWdlUmVnaXN0cnk+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvZGVtaXJyb3ItZXh0ZW5zaW9uOmxhbmd1YWdlcycsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIENvZGVNaXJyb3IgbGFuZ3VhZ2VzIHJlZ2lzdHJ5LicsXG4gIHByb3ZpZGVzOiBJRWRpdG9yTGFuZ3VhZ2VSZWdpc3RyeSxcbiAgb3B0aW9uYWw6IFtJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbCkgPT4ge1xuICAgIGNvbnN0IGxhbmd1YWdlcyA9IG5ldyBFZGl0b3JMYW5ndWFnZVJlZ2lzdHJ5KCk7XG5cbiAgICAvLyBSZWdpc3RlciBkZWZhdWx0IGxhbmd1YWdlc1xuICAgIGZvciAoY29uc3QgbGFuZ3VhZ2Ugb2YgRWRpdG9yTGFuZ3VhZ2VSZWdpc3RyeS5nZXREZWZhdWx0TGFuZ3VhZ2VzKFxuICAgICAgdHJhbnNsYXRvclxuICAgICkpIHtcbiAgICAgIGxhbmd1YWdlcy5hZGRMYW5ndWFnZShsYW5ndWFnZSk7XG4gICAgfVxuXG4gICAgLy8gQWRkIEp1cHl0ZXIgTWFya2Rvd24gZmxhdm9yIGhlcmUgdG8gc3VwcG9ydFxuICAgIC8vIGNvZGUgYmxvY2sgaGlnaGxpZ2h0aW5nLlxuICAgIGxhbmd1YWdlcy5hZGRMYW5ndWFnZSh7XG4gICAgICBuYW1lOiAnaXB5dGhvbmdmbScsXG4gICAgICBtaW1lOiAndGV4dC94LWlweXRob25nZm0nLFxuICAgICAgbG9hZDogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCBbbSwgdGV4XSA9IGF3YWl0IFByb21pc2UuYWxsKFtcbiAgICAgICAgICBpbXBvcnQoJ0Bjb2RlbWlycm9yL2xhbmctbWFya2Rvd24nKSxcbiAgICAgICAgICBpbXBvcnQoJ0Bjb2RlbWlycm9yL2xlZ2FjeS1tb2Rlcy9tb2RlL3N0ZXgnKVxuICAgICAgICBdKTtcbiAgICAgICAgcmV0dXJuIG0ubWFya2Rvd24oe1xuICAgICAgICAgIGJhc2U6IG0ubWFya2Rvd25MYW5ndWFnZSxcbiAgICAgICAgICBjb2RlTGFuZ3VhZ2VzOiAoaW5mbzogc3RyaW5nKSA9PiBsYW5ndWFnZXMuZmluZEJlc3QoaW5mbykgYXMgYW55LFxuICAgICAgICAgIGV4dGVuc2lvbnM6IFtcbiAgICAgICAgICAgIHBhcnNlTWF0aElQeXRob24oU3RyZWFtTGFuZ3VhZ2UuZGVmaW5lKHRleC5zdGV4TWF0aCkucGFyc2VyKVxuICAgICAgICAgIF1cbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG4gICAgcmV0dXJuIGxhbmd1YWdlcztcbiAgfVxufTtcblxuLyoqXG4gKiBDb2RlTWlycm9yIHRoZW1lIHJlZ2lzdHJ5IHByb3ZpZGVyLlxuICovXG5leHBvcnQgY29uc3QgdGhlbWVQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJRWRpdG9yVGhlbWVSZWdpc3RyeT4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY29kZW1pcnJvci1leHRlbnNpb246dGhlbWVzJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgQ29kZU1pcnJvciB0aGVtZSByZWdpc3RyeScsXG4gIHByb3ZpZGVzOiBJRWRpdG9yVGhlbWVSZWdpc3RyeSxcbiAgb3B0aW9uYWw6IFtJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbCkgPT4ge1xuICAgIGNvbnN0IHRoZW1lcyA9IG5ldyBFZGl0b3JUaGVtZVJlZ2lzdHJ5KCk7XG4gICAgLy8gUmVnaXN0ZXIgZGVmYXVsdCB0aGVtZXNcbiAgICBmb3IgKGNvbnN0IHRoZW1lIG9mIEVkaXRvclRoZW1lUmVnaXN0cnkuZ2V0RGVmYXVsdFRoZW1lcyh0cmFuc2xhdG9yKSkge1xuICAgICAgdGhlbWVzLmFkZFRoZW1lKHRoZW1lKTtcbiAgICB9XG4gICAgcmV0dXJuIHRoZW1lcztcbiAgfVxufTtcblxuLyoqXG4gKiBDb2RlTWlycm9yIGVkaXRvciBleHRlbnNpb25zIHJlZ2lzdHJ5IHByb3ZpZGVyLlxuICovXG5leHBvcnQgY29uc3QgZXh0ZW5zaW9uUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUVkaXRvckV4dGVuc2lvblJlZ2lzdHJ5PiA9XG4gIHtcbiAgICBpZDogJ0BqdXB5dGVybGFiL2NvZGVtaXJyb3ItZXh0ZW5zaW9uOmV4dGVuc2lvbnMnLFxuICAgIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIENvZGVNaXJyb3IgZXh0ZW5zaW9uIGZhY3RvcnkgcmVnaXN0cnkuJyxcbiAgICBwcm92aWRlczogSUVkaXRvckV4dGVuc2lvblJlZ2lzdHJ5LFxuICAgIHJlcXVpcmVzOiBbSUVkaXRvclRoZW1lUmVnaXN0cnldLFxuICAgIG9wdGlvbmFsOiBbSVRyYW5zbGF0b3IsIElTZXR0aW5nUmVnaXN0cnksIElGb3JtUmVuZGVyZXJSZWdpc3RyeV0sXG4gICAgYWN0aXZhdGU6IChcbiAgICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgICAgdGhlbWVzOiBJRWRpdG9yVGhlbWVSZWdpc3RyeSxcbiAgICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbCxcbiAgICAgIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSB8IG51bGwsXG4gICAgICBmb3JtUmVnaXN0cnk6IElGb3JtUmVuZGVyZXJSZWdpc3RyeSB8IG51bGxcbiAgICApOiBJRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnkgPT4ge1xuICAgICAgY29uc3QgcmVnaXN0cnkgPSBuZXcgRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnkoKTtcblxuICAgICAgLy8gUmVnaXN0ZXIgZGVmYXVsdCBleHRlbnNpb25zXG4gICAgICBmb3IgKGNvbnN0IGV4dGVuc2lvbkZhY3Rvcnkgb2YgRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnkuZ2V0RGVmYXVsdEV4dGVuc2lvbnMoXG4gICAgICAgIHtcbiAgICAgICAgICB0aGVtZXMsXG4gICAgICAgICAgdHJhbnNsYXRvclxuICAgICAgICB9XG4gICAgICApKSB7XG4gICAgICAgIHJlZ2lzdHJ5LmFkZEV4dGVuc2lvbihleHRlbnNpb25GYWN0b3J5KTtcbiAgICAgIH1cblxuICAgICAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgICAgICBjb25zdCB1cGRhdGVTZXR0aW5ncyA9IChzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpID0+IHtcbiAgICAgICAgICByZWdpc3RyeS5iYXNlQ29uZmlndXJhdGlvbiA9XG4gICAgICAgICAgICAoc2V0dGluZ3MuZ2V0KCdkZWZhdWx0Q29uZmlnJykuY29tcG9zaXRlIGFzIFJlY29yZDxzdHJpbmcsIGFueT4pID8/XG4gICAgICAgICAgICB7fTtcbiAgICAgICAgfTtcbiAgICAgICAgdm9pZCBQcm9taXNlLmFsbChbXG4gICAgICAgICAgc2V0dGluZ1JlZ2lzdHJ5LmxvYWQoU0VUVElOR1NfSUQpLFxuICAgICAgICAgIGFwcC5yZXN0b3JlZFxuICAgICAgICBdKS50aGVuKChbc2V0dGluZ3NdKSA9PiB7XG4gICAgICAgICAgdXBkYXRlU2V0dGluZ3Moc2V0dGluZ3MpO1xuICAgICAgICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdCh1cGRhdGVTZXR0aW5ncyk7XG4gICAgICAgIH0pO1xuXG4gICAgICAgIGZvcm1SZWdpc3RyeT8uYWRkUmVuZGVyZXIoYCR7U0VUVElOR1NfSUR9LmRlZmF1bHRDb25maWdgLCB7XG4gICAgICAgICAgZmllbGRSZW5kZXJlcjogKHByb3BzOiBGaWVsZFByb3BzKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBwcm9wZXJ0aWVzID0gUmVhY3QudXNlTWVtbyhcbiAgICAgICAgICAgICAgKCkgPT4gcmVnaXN0cnkuc2V0dGluZ3NTY2hlbWEsXG4gICAgICAgICAgICAgIFtdXG4gICAgICAgICAgICApIGFzIGFueTtcbiAgICAgICAgICAgIGNvbnN0IGRlZmF1bHRGb3JtRGF0YTogUmVjb3JkPHN0cmluZywgYW55PiA9IHt9O1xuICAgICAgICAgICAgLy8gT25seSBwcm92aWRlIGN1c3RvbWl6YWJsZSBvcHRpb25zXG4gICAgICAgICAgICBmb3IgKGNvbnN0IFtrZXksIHZhbHVlXSBvZiBPYmplY3QuZW50cmllcyhcbiAgICAgICAgICAgICAgcmVnaXN0cnkuZGVmYXVsdENvbmZpZ3VyYXRpb25cbiAgICAgICAgICAgICkpIHtcbiAgICAgICAgICAgICAgaWYgKHR5cGVvZiBwcm9wZXJ0aWVzW2tleV0gIT09ICd1bmRlZmluZWQnKSB7XG4gICAgICAgICAgICAgICAgZGVmYXVsdEZvcm1EYXRhW2tleV0gPSB2YWx1ZTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUZvcm1Hcm91cC1jb250ZW50Tm9ybWFsXCI+XG4gICAgICAgICAgICAgICAgPGgzIGNsYXNzTmFtZT1cImpwLUZvcm1Hcm91cC1maWVsZExhYmVsIGpwLUZvcm1Hcm91cC1jb250ZW50SXRlbVwiPlxuICAgICAgICAgICAgICAgICAge3Byb3BzLnNjaGVtYS50aXRsZX1cbiAgICAgICAgICAgICAgICA8L2gzPlxuICAgICAgICAgICAgICAgIHtwcm9wcy5zY2hlbWEuZGVzY3JpcHRpb24gJiYgKFxuICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1Gb3JtR3JvdXAtZGVzY3JpcHRpb25cIj5cbiAgICAgICAgICAgICAgICAgICAge3Byb3BzLnNjaGVtYS5kZXNjcmlwdGlvbn1cbiAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgPEZvcm1Db21wb25lbnRcbiAgICAgICAgICAgICAgICAgIHNjaGVtYT17e1xuICAgICAgICAgICAgICAgICAgICB0aXRsZTogcHJvcHMuc2NoZW1hLnRpdGxlLFxuICAgICAgICAgICAgICAgICAgICBkZXNjcmlwdGlvbjogcHJvcHMuc2NoZW1hLmRlc2NyaXB0aW9uLFxuICAgICAgICAgICAgICAgICAgICB0eXBlOiAnb2JqZWN0JyxcbiAgICAgICAgICAgICAgICAgICAgcHJvcGVydGllcyxcbiAgICAgICAgICAgICAgICAgICAgYWRkaXRpb25hbFByb3BlcnRpZXM6IGZhbHNlXG4gICAgICAgICAgICAgICAgICB9fVxuICAgICAgICAgICAgICAgICAgdmFsaWRhdG9yPXt2YWxpZGF0b3JBanY4fVxuICAgICAgICAgICAgICAgICAgZm9ybURhdGE9e3sgLi4uZGVmYXVsdEZvcm1EYXRhLCAuLi5wcm9wcy5mb3JtRGF0YSB9fVxuICAgICAgICAgICAgICAgICAgZm9ybUNvbnRleHQ9e3sgZGVmYXVsdEZvcm1EYXRhIH19XG4gICAgICAgICAgICAgICAgICBsaXZlVmFsaWRhdGVcbiAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXtlID0+IHtcbiAgICAgICAgICAgICAgICAgICAgLy8gT25seSBzYXZlIG5vbi1kZWZhdWx0IHZhbHVlc1xuICAgICAgICAgICAgICAgICAgICBjb25zdCBub25EZWZhdWx0OiBSZWNvcmQ8c3RyaW5nLCBSZWFkb25seUpTT05WYWx1ZT4gPSB7fTtcbiAgICAgICAgICAgICAgICAgICAgZm9yIChjb25zdCBbcHJvcGVydHksIHZhbHVlXSBvZiBPYmplY3QuZW50cmllcyhcbiAgICAgICAgICAgICAgICAgICAgICBlLmZvcm1EYXRhID8/IHt9XG4gICAgICAgICAgICAgICAgICAgICkpIHtcbiAgICAgICAgICAgICAgICAgICAgICBjb25zdCBkZWZhdWx0XyA9IGRlZmF1bHRGb3JtRGF0YVtwcm9wZXJ0eV07XG4gICAgICAgICAgICAgICAgICAgICAgaWYgKFxuICAgICAgICAgICAgICAgICAgICAgICAgZGVmYXVsdF8gPT09IHVuZGVmaW5lZCB8fFxuICAgICAgICAgICAgICAgICAgICAgICAgIUpTT05FeHQuZGVlcEVxdWFsKHZhbHVlLCBkZWZhdWx0XylcbiAgICAgICAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIG5vbkRlZmF1bHRbcHJvcGVydHldID0gdmFsdWU7XG4gICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIHByb3BzLm9uQ2hhbmdlKG5vbkRlZmF1bHQpO1xuICAgICAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgICAgICAgIHRhZ05hbWU9XCJkaXZcIlxuICAgICAgICAgICAgICAgICAgdHJhbnNsYXRvcj17dHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvcn1cbiAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICk7XG4gICAgICAgICAgfVxuICAgICAgICB9KTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHJlZ2lzdHJ5O1xuICAgIH1cbiAgfTtcblxuLyoqXG4gKiBDb2RlTWlycm9yIHNoYXJlZCBtb2RlbCBiaW5kaW5nIHByb3ZpZGVyLlxuICovXG5leHBvcnQgY29uc3QgYmluZGluZ1BsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvZGVtaXJyb3ItZXh0ZW5zaW9uOmJpbmRpbmcnLFxuICBkZXNjcmlwdGlvbjpcbiAgICAnUmVnaXN0ZXIgdGhlIENvZGVNaXJyb3IgZXh0ZW5zaW9uIGZhY3RvcnkgYmluZGluZyB0aGUgZWRpdG9yIGFuZCB0aGUgc2hhcmVkIG1vZGVsLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtJRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnldLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kLCBleHRlbnNpb25zOiBJRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnkpID0+IHtcbiAgICBleHRlbnNpb25zLmFkZEV4dGVuc2lvbih7XG4gICAgICBuYW1lOiAnc2hhcmVkLW1vZGVsLWJpbmRpbmcnLFxuICAgICAgZmFjdG9yeTogb3B0aW9ucyA9PiB7XG4gICAgICAgIGNvbnN0IHNoYXJlZE1vZGVsID0gb3B0aW9ucy5tb2RlbC5zaGFyZWRNb2RlbCBhcyBJWVRleHQ7XG4gICAgICAgIHJldHVybiBFZGl0b3JFeHRlbnNpb25SZWdpc3RyeS5jcmVhdGVJbW11dGFibGVFeHRlbnNpb24oXG4gICAgICAgICAgeWJpbmRpbmcoe1xuICAgICAgICAgICAgeXRleHQ6IHNoYXJlZE1vZGVsLnlzb3VyY2UsXG4gICAgICAgICAgICB1bmRvTWFuYWdlcjogc2hhcmVkTW9kZWwudW5kb01hbmFnZXIgPz8gdW5kZWZpbmVkXG4gICAgICAgICAgfSlcbiAgICAgICAgKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBUaGUgZWRpdG9yIHNlcnZpY2VzLlxuICovXG5leHBvcnQgY29uc3Qgc2VydmljZXNQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJRWRpdG9yU2VydmljZXM+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2NvZGVtaXJyb3ItZXh0ZW5zaW9uOnNlcnZpY2VzJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgc2VydmljZSB0byBpbnN0YW50aWF0ZSBDb2RlTWlycm9yIGVkaXRvcnMuJyxcbiAgcHJvdmlkZXM6IElFZGl0b3JTZXJ2aWNlcyxcbiAgcmVxdWlyZXM6IFtcbiAgICBJRWRpdG9yTGFuZ3VhZ2VSZWdpc3RyeSxcbiAgICBJRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnksXG4gICAgSUVkaXRvclRoZW1lUmVnaXN0cnlcbiAgXSxcbiAgb3B0aW9uYWw6IFtJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbGFuZ3VhZ2VzOiBJRWRpdG9yTGFuZ3VhZ2VSZWdpc3RyeSxcbiAgICBleHRlbnNpb25zOiBJRWRpdG9yRXh0ZW5zaW9uUmVnaXN0cnksXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IgfCBudWxsXG4gICk6IElFZGl0b3JTZXJ2aWNlcyA9PiB7XG4gICAgY29uc3QgZmFjdG9yeSA9IG5ldyBDb2RlTWlycm9yRWRpdG9yRmFjdG9yeSh7XG4gICAgICBleHRlbnNpb25zLFxuICAgICAgbGFuZ3VhZ2VzLFxuICAgICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvclxuICAgIH0pO1xuICAgIHJldHVybiB7XG4gICAgICBmYWN0b3J5U2VydmljZTogZmFjdG9yeSxcbiAgICAgIG1pbWVUeXBlU2VydmljZTogbmV3IENvZGVNaXJyb3JNaW1lVHlwZVNlcnZpY2UobGFuZ3VhZ2VzKVxuICAgIH07XG4gIH1cbn07XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=