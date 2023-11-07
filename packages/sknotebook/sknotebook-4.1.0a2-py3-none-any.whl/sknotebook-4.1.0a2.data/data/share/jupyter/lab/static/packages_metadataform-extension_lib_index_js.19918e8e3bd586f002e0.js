"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_metadataform-extension_lib_index_js"],{

/***/ "../packages/metadataform-extension/lib/index.js":
/*!*******************************************************!*\
  !*** ../packages/metadataform-extension/lib/index.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/metadataform */ "webpack/sharing/consume/default/@jupyterlab/metadataform/@jupyterlab/metadataform");
/* harmony import */ var _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform-extension
 */






const PLUGIN_ID = '@jupyterlab/metadataform-extension:metadataforms';
var Private;
(function (Private) {
    async function loadSettingsMetadataForm(app, registry, notebookTools, translator, formComponentRegistry) {
        var _a;
        let canonical;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         */
        function populate(schema) {
            loaded = {};
            schema.properties.metadataforms.default = Object.keys(registry.plugins)
                .map(plugin => {
                var _a;
                const metadataForms = (_a = registry.plugins[plugin].schema['jupyter.lab.metadataforms']) !== null && _a !== void 0 ? _a : [];
                metadataForms.forEach(metadataForm => {
                    metadataForm._origin = plugin;
                });
                loaded[plugin] = metadataForms;
                return metadataForms;
            })
                .concat([schema['jupyter.lab.metadataforms']])
                .reduce((acc, val) => {
                // If a MetadataForm with the same ID already exists,
                // the metadataKeys will be concatenated to this MetadataForm's metadataKeys .
                // Otherwise, the whole MetadataForm will be pushed as a new form.
                val.forEach(value => {
                    const metadataForm = acc.find(addedValue => {
                        return addedValue.id === value.id;
                    });
                    if (metadataForm) {
                        // TODO do insertion of metadataSchema properties in a generic way.
                        // Currently this only support 'properties', 'allOf' and 'required'.
                        //  - add or replace entries if it is an object.
                        //  - concat if it is an array.
                        //  - replace if it is a primitive ?
                        // Includes new metadataKey in the existing metadataSchema.
                        // Overwrites if the metadataKey already exists.
                        for (let [metadataKey, properties] of Object.entries(value.metadataSchema.properties)) {
                            metadataForm.metadataSchema.properties[metadataKey] =
                                properties;
                        }
                        // Includes required fields.
                        if (value.metadataSchema.required) {
                            if (!metadataForm.metadataSchema.required) {
                                metadataForm.metadataSchema.required =
                                    value.metadataSchema.required;
                            }
                            else {
                                metadataForm.metadataSchema.required.concat(value.metadataSchema.required);
                            }
                        }
                        // Includes allOf array in the existing metadataSchema.
                        if (value.metadataSchema.allOf) {
                            if (!metadataForm.metadataSchema.allOf) {
                                metadataForm.metadataSchema.allOf =
                                    value.metadataSchema.allOf;
                            }
                            else {
                                metadataForm.metadataSchema.allOf.concat(value.metadataSchema.allOf);
                            }
                        }
                        // Includes uiSchema in the existing uiSchema.
                        // Overwrites if the uiSchema already exists for that metadataKey.
                        if (value.uiSchema) {
                            if (!metadataForm.uiSchema)
                                metadataForm.uiSchema = {};
                            for (let [metadataKey, ui] of Object.entries(value.uiSchema)) {
                                metadataForm.uiSchema[metadataKey] = ui;
                            }
                        }
                        // Includes metadataOptions in the existing uiSchema.
                        // Overwrites if options already exists for that metadataKey.
                        if (value.metadataOptions) {
                            if (!metadataForm.metadataOptions)
                                metadataForm.metadataOptions = {};
                            for (let [metadataKey, options] of Object.entries(value.metadataOptions)) {
                                metadataForm.metadataOptions[metadataKey] = options;
                            }
                        }
                    }
                    else {
                        acc.push(value);
                    }
                });
                return acc;
            }, []); // flatten one level;
        }
        // Transform the plugin object to return different schema than the default.
        registry.transform(PLUGIN_ID, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.metadataforms) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    metadataforms: (_d = plugin.data.user.metadataforms) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    metadataforms: defaults.concat(user.metadataforms)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        // Repopulate the canonical variable after the setting registry has
        // preloaded all initial plugins.
        canonical = null;
        const settings = await registry.load(PLUGIN_ID);
        const metadataForms = new _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__.MetadataFormProvider();
        // Creates all the forms from extensions settings.
        for (let schema of settings.composite
            .metadataforms) {
            let metaInformation = {};
            let metadataSchema = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(schema.metadataSchema);
            let uiSchema = {};
            if (schema.uiSchema) {
                uiSchema = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.deepCopy(schema.uiSchema);
            }
            for (let [metadataKey, properties] of Object.entries(metadataSchema.properties)) {
                if (properties.default) {
                    if (!metaInformation[metadataKey])
                        metaInformation[metadataKey] = {};
                    metaInformation[metadataKey].default = properties.default;
                }
            }
            if (schema.metadataOptions) {
                for (let [metadataKey, options] of Object.entries(schema.metadataOptions)) {
                    // Optionally links key to cell type.
                    if (options.cellTypes) {
                        if (!metaInformation[metadataKey])
                            metaInformation[metadataKey] = {};
                        metaInformation[metadataKey].cellTypes = options.cellTypes;
                    }
                    // Optionally links key to metadata level.
                    if (options.metadataLevel) {
                        if (!metaInformation[metadataKey])
                            metaInformation[metadataKey] = {};
                        metaInformation[metadataKey].level = options.metadataLevel;
                    }
                    // Optionally set the writeDefault flag.
                    if (options.writeDefault !== undefined) {
                        if (!metaInformation[metadataKey])
                            metaInformation[metadataKey] = {};
                        metaInformation[metadataKey].writeDefault = options.writeDefault;
                    }
                    // Optionally links key to a custom widget.
                    if (options.customRenderer) {
                        const component = formComponentRegistry.getRenderer(options.customRenderer);
                        // If renderer is defined (custom widget has been registered), set it as used widget.
                        if (component !== undefined) {
                            if (!uiSchema[metadataKey])
                                uiSchema[metadataKey] = {};
                            if (component.fieldRenderer) {
                                uiSchema[metadataKey]['ui:field'] = component.fieldRenderer;
                            }
                            else {
                                uiSchema[metadataKey]['ui:widget'] = component.widgetRenderer;
                            }
                        }
                    }
                }
            }
            // Adds a section to notebookTools.
            notebookTools.addSection({
                sectionName: schema.id,
                rank: schema.rank,
                label: (_a = schema.label) !== null && _a !== void 0 ? _a : schema.id
            });
            // Creates the tool.
            const tool = new _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__.MetadataFormWidget({
                metadataSchema: metadataSchema,
                metaInformation: metaInformation,
                uiSchema: uiSchema,
                pluginId: schema._origin,
                translator: translator,
                showModified: schema.showModified
            });
            // Adds the form to the section.
            notebookTools.addItem({ section: schema.id, tool: tool });
            metadataForms.add(schema.id, tool);
        }
        return metadataForms;
    }
    Private.loadSettingsMetadataForm = loadSettingsMetadataForm;
})(Private || (Private = {}));
/**
 * The metadata form plugin.
 */
const metadataForm = {
    id: PLUGIN_ID,
    description: 'Provides the metadata form registry.',
    autoStart: true,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTools,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator,
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.IFormRendererRegistry,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry
    ],
    provides: _jupyterlab_metadataform__WEBPACK_IMPORTED_MODULE_5__.IMetadataFormProvider,
    activate: async (app, notebookTools, translator, componentsRegistry, settings) => {
        return await Private.loadSettingsMetadataForm(app, settings, notebookTools, translator, componentsRegistry);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (metadataForm);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWV0YWRhdGFmb3JtLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuMTk5MThlOGUzYmQ1ODZmMDAyZTAuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTW1EO0FBQ1M7QUFDVDtBQUNZO0FBQ0o7QUFPNUI7QUFFbEMsTUFBTSxTQUFTLEdBQUcsa0RBQWtELENBQUM7QUFFckUsSUFBVSxPQUFPLENBK09oQjtBQS9PRCxXQUFVLE9BQU87SUFDUixLQUFLLFVBQVUsd0JBQXdCLENBQzVDLEdBQW9CLEVBQ3BCLFFBQTBCLEVBQzFCLGFBQTZCLEVBQzdCLFVBQXVCLEVBQ3ZCLHFCQUE0Qzs7UUFFNUMsSUFBSSxTQUEwQyxDQUFDO1FBQy9DLElBQUksTUFBTSxHQUF5RCxFQUFFLENBQUM7UUFFdEU7O1dBRUc7UUFDSCxTQUFTLFFBQVEsQ0FBQyxNQUFnQztZQUNoRCxNQUFNLEdBQUcsRUFBRSxDQUFDO1lBQ1osTUFBTSxDQUFDLFVBQVcsQ0FBQyxhQUFhLENBQUMsT0FBTyxHQUFHLE1BQU0sQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLE9BQU8sQ0FBQztpQkFDckUsR0FBRyxDQUFDLE1BQU0sQ0FBQyxFQUFFOztnQkFDWixNQUFNLGFBQWEsR0FDakIsY0FBUSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUUsQ0FBQyxNQUFNLENBQUMsMkJBQTJCLENBQUMsbUNBQUksRUFBRSxDQUFDO2dCQUV0RSxhQUFhLENBQUMsT0FBTyxDQUFDLFlBQVksQ0FBQyxFQUFFO29CQUNuQyxZQUFZLENBQUMsT0FBTyxHQUFHLE1BQU0sQ0FBQztnQkFDaEMsQ0FBQyxDQUFDLENBQUM7Z0JBQ0gsTUFBTSxDQUFDLE1BQU0sQ0FBQyxHQUFHLGFBQWEsQ0FBQztnQkFDL0IsT0FBTyxhQUFhLENBQUM7WUFDdkIsQ0FBQyxDQUFDO2lCQUNELE1BQU0sQ0FBQyxDQUFDLE1BQU0sQ0FBQywyQkFB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LElBQUk7SUFDZixRQUFRLEVBQUU7UUFDUixnRUFBYztRQUNkLGdFQUFXO1FBQ1gsNEVBQXFCO1FBQ3JCLHlFQUFnQjtLQUNqQjtJQUNELFFBQVEsRUFBRSwyRUFBcUI7SUFDL0IsUUFBUSxFQUFFLEtBQUssRUFDYixHQUFvQixFQUNwQixhQUE2QixFQUM3QixVQUF1QixFQUN2QixrQkFBeUMsRUFDekMsUUFBMEIsRUFDTSxFQUFFO1FBQ2xDLE9BQU8sTUFBTSxPQUFPLENBQUMsd0JBQXdCLENBQzNDLEdBQUcsRUFDSCxRQUFRLEVBQ1IsYUFBYSxFQUNiLFVBQVUsRUFDVixrQkFBa0IsQ0FDbkIsQ0FBQztJQUNKLENBQUM7Q0FDRixDQUFDO0FBRUYsaUVBQWUsWUFBWSxFQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21ldGFkYXRhZm9ybS1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG1ldGFkYXRhZm9ybS1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJTm90ZWJvb2tUb29scyB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBJRm9ybVJlbmRlcmVyUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IEpTT05FeHQsIFBhcnRpYWxKU09OQXJyYXkgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5cbmltcG9ydCB7XG4gIElNZXRhZGF0YUZvcm1Qcm92aWRlcixcbiAgTWV0YWRhdGFGb3JtLFxuICBNZXRhZGF0YUZvcm1Qcm92aWRlcixcbiAgTWV0YWRhdGFGb3JtV2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL21ldGFkYXRhZm9ybSc7XG5cbmNvbnN0IFBMVUdJTl9JRCA9ICdAanVweXRlcmxhYi9tZXRhZGF0YWZvcm0tZXh0ZW5zaW9uOm1ldGFkYXRhZm9ybXMnO1xuXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiBsb2FkU2V0dGluZ3NNZXRhZGF0YUZvcm0oXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgcmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnksXG4gICAgbm90ZWJvb2tUb29sczogSU5vdGVib29rVG9vbHMsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gICAgZm9ybUNvbXBvbmVudFJlZ2lzdHJ5OiBJRm9ybVJlbmRlcmVyUmVnaXN0cnlcbiAgKTogUHJvbWlzZTxJTWV0YWRhdGFGb3JtUHJvdmlkZXI+IHtcbiAgICBsZXQgY2Fub25pY2FsOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEgfCBudWxsO1xuICAgIGxldCBsb2FkZWQ6IHsgW25hbWU6IHN0cmluZ106IElTZXR0aW5nUmVnaXN0cnkuSU1ldGFkYXRhRm9ybVtdIH0gPSB7fTtcblxuICAgIC8qKlxuICAgICAqIFBvcHVsYXRlIHRoZSBwbHVnaW4ncyBzY2hlbWEgZGVmYXVsdHMuXG4gICAgICovXG4gICAgZnVuY3Rpb24gcG9wdWxhdGUoc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEpIHtcbiAgICAgIGxvYWRlZCA9IHt9O1xuICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLm1ldGFkYXRhZm9ybXMuZGVmYXVsdCA9IE9iamVjdC5rZXlzKHJlZ2lzdHJ5LnBsdWdpbnMpXG4gICAgICAgIC5tYXAocGx1Z2luID0+IHtcbiAgICAgICAgICBjb25zdCBtZXRhZGF0YUZvcm1zID1cbiAgICAgICAgICAgIHJlZ2lzdHJ5LnBsdWdpbnNbcGx1Z2luXSEuc2NoZW1hWydqdXB5dGVyLmxhYi5tZXRhZGF0YWZvcm1zJ10gPz8gW107XG5cbiAgICAgICAgICBtZXRhZGF0YUZvcm1zLmZvckVhY2gobWV0YWRhdGFGb3JtID0+IHtcbiAgICAgICAgICAgIG1ldGFkYXRhRm9ybS5fb3JpZ2luID0gcGx1Z2luO1xuICAgICAgICAgIH0pO1xuICAgICAgICAgIGxvYWRlZFtwbHVnaW5dID0gbWV0YWRhdGFGb3JtcztcbiAgICAgICAgICByZXR1cm4gbWV0YWRhdGFGb3JtcztcbiAgICAgICAgfSlcbiAgICAgICAgLmNvbmNhdChbc2NoZW1hWydqdXB5dGVyLmxhYi5tZXRhZGF0YWZvcm1zJ10gYXMgYW55W11dKVxuICAgICAgICAucmVkdWNlKChhY2MsIHZhbCkgPT4ge1xuICAgICAgICAgIC8vIElmIGEgTWV0YWRhdGFGb3JtIHdpdGggdGhlIHNhbWUgSUQgYWxyZWFkeSBleGlzdHMsXG4gICAgICAgICAgLy8gdGhlIG1ldGFkYXRhS2V5cyB3aWxsIGJlIGNvbmNhdGVuYXRlZCB0byB0aGlzIE1ldGFkYXRhRm9ybSdzIG1ldGFkYXRhS2V5cyAuXG4gICAgICAgICAgLy8gT3RoZXJ3aXNlLCB0aGUgd2hvbGUgTWV0YWRhdGFGb3JtIHdpbGwgYmUgcHVzaGVkIGFzIGEgbmV3IGZvcm0uXG4gICAgICAgICAgdmFsLmZvckVhY2godmFsdWUgPT4ge1xuICAgICAgICAgICAgY29uc3QgbWV0YWRhdGFGb3JtID0gYWNjLmZpbmQoYWRkZWRWYWx1ZSA9PiB7XG4gICAgICAgICAgICAgIHJldHVybiBhZGRlZFZhbHVlLmlkID09PSB2YWx1ZS5pZDtcbiAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgaWYgKG1ldGFkYXRhRm9ybSkge1xuICAgICAgICAgICAgICAvLyBUT0RPIGRvIGluc2VydGlvbiBvZiBtZXRhZGF0YVNjaGVtYSBwcm9wZXJ0aWVzIGluIGEgZ2VuZXJpYyB3YXkuXG4gICAgICAgICAgICAgIC8vIEN1cnJlbnRseSB0aGlzIG9ubHkgc3VwcG9ydCAncHJvcGVydGllcycsICdhbGxPZicgYW5kICdyZXF1aXJlZCcuXG4gICAgICAgICAgICAgIC8vICAtIGFkZCBvciByZXBsYWNlIGVudHJpZXMgaWYgaXQgaXMgYW4gb2JqZWN0LlxuICAgICAgICAgICAgICAvLyAgLSBjb25jYXQgaWYgaXQgaXMgYW4gYXJyYXkuXG4gICAgICAgICAgICAgIC8vICAtIHJlcGxhY2UgaWYgaXQgaXMgYSBwcmltaXRpdmUgP1xuXG4gICAgICAgICAgICAgIC8vIEluY2x1ZGVzIG5ldyBtZXRhZGF0YUtleSBpbiB0aGUgZXhpc3RpbmcgbWV0YWRhdGFTY2hlbWEuXG4gICAgICAgICAgICAgIC8vIE92ZXJ3cml0ZXMgaWYgdGhlIG1ldGFkYXRhS2V5IGFscmVhZHkgZXhpc3RzLlxuICAgICAgICAgICAgICBmb3IgKGxldCBbbWV0YWRhdGFLZXksIHByb3BlcnRpZXNdIG9mIE9iamVjdC5lbnRyaWVzKFxuICAgICAgICAgICAgICAgIHZhbHVlLm1ldGFkYXRhU2NoZW1hLnByb3BlcnRpZXNcbiAgICAgICAgICAgICAgKSkge1xuICAgICAgICAgICAgICAgIG1ldGFkYXRhRm9ybS5tZXRhZGF0YVNjaGVtYS5wcm9wZXJ0aWVzW21ldGFkYXRhS2V5XSA9XG4gICAgICAgICAgICAgICAgICBwcm9wZXJ0aWVzO1xuICAgICAgICAgICAgICB9XG5cbiAgICAgICAgICAgICAgLy8gSW5jbHVkZXMgcmVxdWlyZWQgZmllbGRzLlxuICAgICAgICAgICAgICBpZiAodmFsdWUubWV0YWRhdGFTY2hlbWEucmVxdWlyZWQpIHtcbiAgICAgICAgICAgICAgICBpZiAoIW1ldGFkYXRhRm9ybS5tZXRhZGF0YVNjaGVtYS5yZXF1aXJlZCkge1xuICAgICAgICAgICAgICAgICAgbWV0YWRhdGFGb3JtLm1ldGFkYXRhU2NoZW1hLnJlcXVpcmVkID1cbiAgICAgICAgICAgICAgICAgICAgdmFsdWUubWV0YWRhdGFTY2hlbWEucmVxdWlyZWQ7XG4gICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgIG1ldGFkYXRhRm9ybS5tZXRhZGF0YVNjaGVtYS5yZXF1aXJlZC5jb25jYXQoXG4gICAgICAgICAgICAgICAgICAgIHZhbHVlLm1ldGFkYXRhU2NoZW1hLnJlcXVpcmVkXG4gICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICAgIC8vIEluY2x1ZGVzIGFsbE9mIGFycmF5IGluIHRoZSBleGlzdGluZyBtZXRhZGF0YVNjaGVtYS5cbiAgICAgICAgICAgICAgaWYgKHZhbHVlLm1ldGFkYXRhU2NoZW1hLmFsbE9mKSB7XG4gICAgICAgICAgICAgICAgaWYgKCFtZXRhZGF0YUZvcm0ubWV0YWRhdGFTY2hlbWEuYWxsT2YpIHtcbiAgICAgICAgICAgICAgICAgIG1ldGFkYXRhRm9ybS5tZXRhZGF0YVNjaGVtYS5hbGxPZiA9XG4gICAgICAgICAgICAgICAgICAgIHZhbHVlLm1ldGFkYXRhU2NoZW1hLmFsbE9mO1xuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICBtZXRhZGF0YUZvcm0ubWV0YWRhdGFTY2hlbWEuYWxsT2YuY29uY2F0KFxuICAgICAgICAgICAgICAgICAgICB2YWx1ZS5tZXRhZGF0YVNjaGVtYS5hbGxPZlxuICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgIH1cblxuICAgICAgICAgICAgICAvLyBJbmNsdWRlcyB1aVNjaGVtYSBpbiB0aGUgZXhpc3RpbmcgdWlTY2hlbWEuXG4gICAgICAgICAgICAgIC8vIE92ZXJ3cml0ZXMgaWYgdGhlIHVpU2NoZW1hIGFscmVhZHkgZXhpc3RzIGZvciB0aGF0IG1ldGFkYXRhS2V5LlxuICAgICAgICAgICAgICBpZiAodmFsdWUudWlTY2hlbWEpIHtcbiAgICAgICAgICAgICAgICBpZiAoIW1ldGFkYXRhRm9ybS51aVNjaGVtYSkgbWV0YWRhdGFGb3JtLnVpU2NoZW1hID0ge307XG4gICAgICAgICAgICAgICAgZm9yIChsZXQgW21ldGFkYXRhS2V5LCB1aV0gb2YgT2JqZWN0LmVudHJpZXModmFsdWUudWlTY2hlbWEpKSB7XG4gICAgICAgICAgICAgICAgICBtZXRhZGF0YUZvcm0udWlTY2hlbWFbbWV0YWRhdGFLZXldID0gdWk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB9XG5cbiAgICAgICAgICAgICAgLy8gSW5jbHVkZXMgbWV0YWRhdGFPcHRpb25zIGluIHRoZSBleGlzdGluZyB1aVNjaGVtYS5cbiAgICAgICAgICAgICAgLy8gT3ZlcndyaXRlcyBpZiBvcHRpb25zIGFscmVhZHkgZXhpc3RzIGZvciB0aGF0IG1ldGFkYXRhS2V5LlxuICAgICAgICAgICAgICBpZiAodmFsdWUubWV0YWRhdGFPcHRpb25zKSB7XG4gICAgICAgICAgICAgICAgaWYgKCFtZXRhZGF0YUZvcm0ubWV0YWRhdGFPcHRpb25zKVxuICAgICAgICAgICAgICAgICAgbWV0YWRhdGFGb3JtLm1ldGFkYXRhT3B0aW9ucyA9IHt9O1xuICAgICAgICAgICAgICAgIGZvciAobGV0IFttZXRhZGF0YUtleSwgb3B0aW9uc10gb2YgT2JqZWN0LmVudHJpZXMoXG4gICAgICAgICAgICAgICAgICB2YWx1ZS5tZXRhZGF0YU9wdGlvbnNcbiAgICAgICAgICAgICAgICApKSB7XG4gICAgICAgICAgICAgICAgICBtZXRhZGF0YUZvcm0ubWV0YWRhdGFPcHRpb25zW21ldGFkYXRhS2V5XSA9IG9wdGlvbnM7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICBhY2MucHVzaCh2YWx1ZSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSk7XG4gICAgICAgICAgcmV0dXJuIGFjYztcbiAgICAgICAgfSwgW10pOyAvLyBmbGF0dGVuIG9uZSBsZXZlbDtcbiAgICB9XG5cbiAgICAvLyBUcmFuc2Zvcm0gdGhlIHBsdWdpbiBvYmplY3QgdG8gcmV0dXJuIGRpZmZlcmVudCBzY2hlbWEgdGhhbiB0aGUgZGVmYXVsdC5cbiAgICByZWdpc3RyeS50cmFuc2Zvcm0oUExVR0lOX0lELCB7XG4gICAgICBjb21wb3NlOiBwbHVnaW4gPT4ge1xuICAgICAgICAvLyBPbmx5IG92ZXJyaWRlIHRoZSBjYW5vbmljYWwgc2NoZW1hIHRoZSBmaXJzdCB0aW1lLlxuICAgICAgICBpZiAoIWNhbm9uaWNhbCkge1xuICAgICAgICAgIGNhbm9uaWNhbCA9IEpTT05FeHQuZGVlcENvcHkocGx1Z2luLnNjaGVtYSk7XG4gICAgICAgICAgcG9wdWxhdGUoY2Fub25pY2FsKTtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBkZWZhdWx0cyA9XG4gICAgICAgICAgKGNhbm9uaWNhbC5wcm9wZXJ0aWVzPy5tZXRhZGF0YWZvcm1zPy5kZWZhdWx0IGFzIFBhcnRpYWxKU09OQXJyYXkpID8/XG4gICAgICAgICAgW107XG4gICAgICAgIGNvbnN0IHVzZXIgPSB7XG4gICAgICAgICAgbWV0YWRhdGFmb3JtczogcGx1Z2luLmRhdGEudXNlci5tZXRhZGF0YWZvcm1zID8/IFtdXG4gICAgICAgIH07XG4gICAgICAgIGNvbnN0IGNvbXBvc2l0ZSA9IHtcbiAgICAgICAgICBtZXRhZGF0YWZvcm1zOiBkZWZhdWx0cy5jb25jYXQodXNlci5tZXRhZGF0YWZvcm1zKVxuICAgICAgICB9O1xuXG4gICAgICAgIHBsdWdpbi5kYXRhID0geyBjb21wb3NpdGUsIHVzZXIgfTtcbiAgICAgICAgcmV0dXJuIHBsdWdpbjtcbiAgICAgIH0sXG4gICAgICBmZXRjaDogcGx1Z2luID0+IHtcbiAgICAgICAgLy8gT25seSBvdmVycmlkZSB0aGUgY2Fub25pY2FsIHNjaGVtYSB0aGUgZmlyc3QgdGltZS5cbiAgICAgICAgaWYgKCFjYW5vbmljYWwpIHtcbiAgICAgICAgICBjYW5vbmljYWwgPSBKU09ORXh0LmRlZXBDb3B5KHBsdWdpbi5zY2hlbWEpO1xuICAgICAgICAgIHBvcHVsYXRlKGNhbm9uaWNhbCk7XG4gICAgICAgIH1cblxuICAgICAgICByZXR1cm4ge1xuICAgICAgICAgIGRhdGE6IHBsdWdpbi5kYXRhLFxuICAgICAgICAgIGlkOiBwbHVnaW4uaWQsXG4gICAgICAgICAgcmF3OiBwbHVnaW4ucmF3LFxuICAgICAgICAgIHNjaGVtYTogY2Fub25pY2FsLFxuICAgICAgICAgIHZlcnNpb246IHBsdWdpbi52ZXJzaW9uXG4gICAgICAgIH07XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBSZXBvcHVsYXRlIHRoZSBjYW5vbmljYWwgdmFyaWFibGUgYWZ0ZXIgdGhlIHNldHRpbmcgcmVnaXN0cnkgaGFzXG4gICAgLy8gcHJlbG9hZGVkIGFsbCBpbml0aWFsIHBsdWdpbnMuXG4gICAgY2Fub25pY2FsID0gbnVsbDtcblxuICAgIGNvbnN0IHNldHRpbmdzID0gYXdhaXQgcmVnaXN0cnkubG9hZChQTFVHSU5fSUQpO1xuICAgIGNvbnN0IG1ldGFkYXRhRm9ybXM6IElNZXRhZGF0YUZvcm1Qcm92aWRlciA9IG5ldyBNZXRhZGF0YUZvcm1Qcm92aWRlcigpO1xuXG4gICAgLy8gQ3JlYXRlcyBhbGwgdGhlIGZvcm1zIGZyb20gZXh0ZW5zaW9ucyBzZXR0aW5ncy5cbiAgICBmb3IgKGxldCBzY2hlbWEgb2Ygc2V0dGluZ3MuY29tcG9zaXRlXG4gICAgICAubWV0YWRhdGFmb3JtcyBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklNZXRhZGF0YUZvcm1bXSkge1xuICAgICAgbGV0IG1ldGFJbmZvcm1hdGlvbjogTWV0YWRhdGFGb3JtLklNZXRhSW5mb3JtYXRpb24gPSB7fTtcbiAgICAgIGxldCBtZXRhZGF0YVNjaGVtYTogSVNldHRpbmdSZWdpc3RyeS5JTWV0YWRhdGFTY2hlbWEgPSBKU09ORXh0LmRlZXBDb3B5KFxuICAgICAgICBzY2hlbWEubWV0YWRhdGFTY2hlbWFcbiAgICAgICk7XG4gICAgICBsZXQgdWlTY2hlbWE6IE1ldGFkYXRhRm9ybS5JVWlTY2hlbWEgPSB7fTtcblxuICAgICAgaWYgKHNjaGVtYS51aVNjaGVtYSkge1xuICAgICAgICB1aVNjaGVtYSA9IEpTT05FeHQuZGVlcENvcHkoc2NoZW1hLnVpU2NoZW1hKSBhcyBNZXRhZGF0YUZvcm0uSVVpU2NoZW1hO1xuICAgICAgfVxuXG4gICAgICBmb3IgKGxldCBbbWV0YWRhdGFLZXksIHByb3BlcnRpZXNdIG9mIE9iamVjdC5lbnRyaWVzKFxuICAgICAgICBtZXRhZGF0YVNjaGVtYS5wcm9wZXJ0aWVzXG4gICAgICApKSB7XG4gICAgICAgIGlmIChwcm9wZXJ0aWVzLmRlZmF1bHQpIHtcbiAgICAgICAgICBpZiAoIW1ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0pIG1ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0gPSB7fTtcbiAgICAgICAgICBtZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldLmRlZmF1bHQgPSBwcm9wZXJ0aWVzLmRlZmF1bHQ7XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgaWYgKHNjaGVtYS5tZXRhZGF0YU9wdGlvbnMpIHtcbiAgICAgICAgZm9yIChsZXQgW21ldGFkYXRhS2V5LCBvcHRpb25zXSBvZiBPYmplY3QuZW50cmllcyhcbiAgICAgICAgICBzY2hlbWEubWV0YWRhdGFPcHRpb25zXG4gICAgICAgICkpIHtcbiAgICAgICAgICAvLyBPcHRpb25hbGx5IGxpbmtzIGtleSB0byBjZWxsIHR5cGUuXG4gICAgICAgICAgaWYgKG9wdGlvbnMuY2VsbFR5cGVzKSB7XG4gICAgICAgICAgICBpZiAoIW1ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0pXG4gICAgICAgICAgICAgIG1ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0gPSB7fTtcbiAgICAgICAgICAgIG1ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0uY2VsbFR5cGVzID0gb3B0aW9ucy5jZWxsVHlwZXM7XG4gICAgICAgICAgfVxuXG4gICAgICAgICAgLy8gT3B0aW9uYWxseSBsaW5rcyBrZXkgdG8gbWV0YWRhdGEgbGV2ZWwuXG4gICAgICAgICAgaWYgKG9wdGlvbnMubWV0YWRhdGFMZXZlbCkge1xuICAgICAgICAgICAgaWYgKCFtZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldKVxuICAgICAgICAgICAgICBtZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldID0ge307XG4gICAgICAgICAgICBtZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldLmxldmVsID0gb3B0aW9ucy5tZXRhZGF0YUxldmVsO1xuICAgICAgICAgIH1cblxuICAgICAgICAgIC8vIE9wdGlvbmFsbHkgc2V0IHRoZSB3cml0ZURlZmF1bHQgZmxhZy5cbiAgICAgICAgICBpZiAob3B0aW9ucy53cml0ZURlZmF1bHQgIT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgICAgaWYgKCFtZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldKVxuICAgICAgICAgICAgICBtZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldID0ge307XG4gICAgICAgICAgICBtZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldLndyaXRlRGVmYXVsdCA9IG9wdGlvbnMud3JpdGVEZWZhdWx0O1xuICAgICAgICAgIH1cblxuICAgICAgICAgIC8vIE9wdGlvbmFsbHkgbGlua3Mga2V5IHRvIGEgY3VzdG9tIHdpZGdldC5cbiAgICAgICAgICBpZiAob3B0aW9ucy5jdXN0b21SZW5kZXJlcikge1xuICAgICAgICAgICAgY29uc3QgY29tcG9uZW50ID0gZm9ybUNvbXBvbmVudFJlZ2lzdHJ5LmdldFJlbmRlcmVyKFxuICAgICAgICAgICAgICBvcHRpb25zLmN1c3RvbVJlbmRlcmVyIGFzIHN0cmluZ1xuICAgICAgICAgICAgKTtcblxuICAgICAgICAgICAgLy8gSWYgcmVuZGVyZXIgaXMgZGVmaW5lZCAoY3VzdG9tIHdpZGdldCBoYXMgYmVlbiByZWdpc3RlcmVkKSwgc2V0IGl0IGFzIHVzZWQgd2lkZ2V0LlxuICAgICAgICAgICAgaWYgKGNvbXBvbmVudCAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICAgIGlmICghdWlTY2hlbWFbbWV0YWRhdGFLZXldKSB1aVNjaGVtYVttZXRhZGF0YUtleV0gPSB7fTtcbiAgICAgICAgICAgICAgaWYgKGNvbXBvbmVudC5maWVsZFJlbmRlcmVyKSB7XG4gICAgICAgICAgICAgICAgdWlTY2hlbWFbbWV0YWRhdGFLZXldWyd1aTpmaWVsZCddID0gY29tcG9uZW50LmZpZWxkUmVuZGVyZXI7XG4gICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgdWlTY2hlbWFbbWV0YWRhdGFLZXldWyd1aTp3aWRnZXQnXSA9IGNvbXBvbmVudC53aWRnZXRSZW5kZXJlcjtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuXG4gICAgICAvLyBBZGRzIGEgc2VjdGlvbiB0byBub3RlYm9va1Rvb2xzLlxuICAgICAgbm90ZWJvb2tUb29scy5hZGRTZWN0aW9uKHtcbiAgICAgICAgc2VjdGlvbk5hbWU6IHNjaGVtYS5pZCxcbiAgICAgICAgcmFuazogc2NoZW1hLnJhbmssXG4gICAgICAgIGxhYmVsOiBzY2hlbWEubGFiZWwgPz8gc2NoZW1hLmlkXG4gICAgICB9KTtcblxuICAgICAgLy8gQ3JlYXRlcyB0aGUgdG9vbC5cbiAgICAgIGNvbnN0IHRvb2wgPSBuZXcgTWV0YWRhdGFGb3JtV2lkZ2V0KHtcbiAgICAgICAgbWV0YWRhdGFTY2hlbWE6IG1ldGFkYXRhU2NoZW1hLFxuICAgICAgICBtZXRhSW5mb3JtYXRpb246IG1ldGFJbmZvcm1hdGlvbixcbiAgICAgICAgdWlTY2hlbWE6IHVpU2NoZW1hLFxuICAgICAgICBwbHVnaW5JZDogc2NoZW1hLl9vcmlnaW4sXG4gICAgICAgIHRyYW5zbGF0b3I6IHRyYW5zbGF0b3IsXG4gICAgICAgIHNob3dNb2RpZmllZDogc2NoZW1hLnNob3dNb2RpZmllZFxuICAgICAgfSk7XG5cbiAgICAgIC8vIEFkZHMgdGhlIGZvcm0gdG8gdGhlIHNlY3Rpb24uXG4gICAgICBub3RlYm9va1Rvb2xzLmFkZEl0ZW0oeyBzZWN0aW9uOiBzY2hlbWEuaWQsIHRvb2w6IHRvb2wgfSk7XG5cbiAgICAgIG1ldGFkYXRhRm9ybXMuYWRkKHNjaGVtYS5pZCwgdG9vbCk7XG4gICAgfVxuICAgIHJldHVybiBtZXRhZGF0YUZvcm1zO1xuICB9XG59XG5cbi8qKlxuICogVGhlIG1ldGFkYXRhIGZvcm0gcGx1Z2luLlxuICovXG5jb25zdCBtZXRhZGF0YUZvcm06IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTWV0YWRhdGFGb3JtUHJvdmlkZXI+ID0ge1xuICBpZDogUExVR0lOX0lELFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBtZXRhZGF0YSBmb3JtIHJlZ2lzdHJ5LicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtcbiAgICBJTm90ZWJvb2tUb29scyxcbiAgICBJVHJhbnNsYXRvcixcbiAgICBJRm9ybVJlbmRlcmVyUmVnaXN0cnksXG4gICAgSVNldHRpbmdSZWdpc3RyeVxuICBdLFxuICBwcm92aWRlczogSU1ldGFkYXRhRm9ybVByb3ZpZGVyLFxuICBhY3RpdmF0ZTogYXN5bmMgKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG5vdGVib29rVG9vbHM6IElOb3RlYm9va1Rvb2xzLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIGNvbXBvbmVudHNSZWdpc3RyeTogSUZvcm1SZW5kZXJlclJlZ2lzdHJ5LFxuICAgIHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5XG4gICk6IFByb21pc2U8SU1ldGFkYXRhRm9ybVByb3ZpZGVyPiA9PiB7XG4gICAgcmV0dXJuIGF3YWl0IFByaXZhdGUubG9hZFNldHRpbmdzTWV0YWRhdGFGb3JtKFxuICAgICAgYXBwLFxuICAgICAgc2V0dGluZ3MsXG4gICAgICBub3RlYm9va1Rvb2xzLFxuICAgICAgdHJhbnNsYXRvcixcbiAgICAgIGNvbXBvbmVudHNSZWdpc3RyeVxuICAgICk7XG4gIH1cbn07XG5cbmV4cG9ydCBkZWZhdWx0IG1ldGFkYXRhRm9ybTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==