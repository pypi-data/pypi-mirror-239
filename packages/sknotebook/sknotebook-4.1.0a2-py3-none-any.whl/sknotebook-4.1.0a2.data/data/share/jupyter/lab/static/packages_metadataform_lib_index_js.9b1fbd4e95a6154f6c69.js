"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_metadataform_lib_index_js"],{

/***/ "../packages/metadataform/lib/form.js":
/*!********************************************!*\
  !*** ../packages/metadataform/lib/form.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FormWidget": () => (/* binding */ FormWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @rjsf/validator-ajv8 */ "webpack/sharing/consume/default/@rjsf/validator-ajv8/@rjsf/validator-ajv8");
/* harmony import */ var _rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */




/**
 * A ReactWidget with the form itself.
 */
class FormWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    /**
     * Constructs a new FormWidget.
     */
    constructor(props) {
        super();
        this.addClass('jp-FormWidget');
        this._props = props;
    }
    /**
     * Render the form.
     * @returns - The rendered form
     */
    render() {
        const formContext = {
            defaultFormData: this._props.settings.default(),
            updateMetadata: this._props.metadataFormWidget.updateMetadata
        };
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.FormComponent, { validator: (_rjsf_validator_ajv8__WEBPACK_IMPORTED_MODULE_2___default()), schema: this._props.properties, formData: this._props.formData, formContext: formContext, uiSchema: this._props.uiSchema, liveValidate: true, idPrefix: `jp-MetadataForm-${this._props.pluginId}`, onChange: (e) => {
                this._props.metadataFormWidget.updateMetadata(e.formData || {});
            }, compact: true, showModifiedFromDefault: this._props.showModified, translator: this._props.translator }));
    }
}


/***/ }),

/***/ "../packages/metadataform/lib/index.js":
/*!*********************************************!*\
  !*** ../packages/metadataform/lib/index.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FormWidget": () => (/* reexport safe */ _form__WEBPACK_IMPORTED_MODULE_0__.FormWidget),
/* harmony export */   "IMetadataFormProvider": () => (/* reexport safe */ _token__WEBPACK_IMPORTED_MODULE_3__.IMetadataFormProvider),
/* harmony export */   "MetadataFormProvider": () => (/* reexport safe */ _metadataformProvider__WEBPACK_IMPORTED_MODULE_2__.MetadataFormProvider),
/* harmony export */   "MetadataFormWidget": () => (/* reexport safe */ _metadataform__WEBPACK_IMPORTED_MODULE_1__.MetadataFormWidget)
/* harmony export */ });
/* harmony import */ var _form__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./form */ "../packages/metadataform/lib/form.js");
/* harmony import */ var _metadataform__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./metadataform */ "../packages/metadataform/lib/metadataform.js");
/* harmony import */ var _metadataformProvider__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./metadataformProvider */ "../packages/metadataform/lib/metadataformProvider.js");
/* harmony import */ var _token__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./token */ "../packages/metadataform/lib/token.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */






/***/ }),

/***/ "../packages/metadataform/lib/metadataform.js":
/*!****************************************************!*\
  !*** ../packages/metadataform/lib/metadataform.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MetadataFormWidget": () => (/* binding */ MetadataFormWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _form__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./form */ "../packages/metadataform/lib/form.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */






/**
 * A class that create a metadata form widget
 */
class MetadataFormWidget extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookTools.Tool {
    /**
     * Construct an empty widget.
     */
    constructor(options) {
        super();
        /**
         * Update the metadata of the current cell or notebook.
         *
         * @param formData - the cell metadata set in the form.
         * @param reload - whether to update the form after updating the metadata.
         *
         * ## Notes
         * Metadata are updated from root only. If some metadata is nested,
         * the whole root object must be updated.
         * This function build an object with all the root object to update
         * in metadata before performing update.
         * It uses an arrow function to allow using 'this' properly when called from a custom field.
         */
        this.updateMetadata = (formData, reload) => {
            var _a, _b, _c, _d, _e, _f, _g, _h;
            if (this.notebookTools == undefined)
                return;
            const notebook = this.notebookTools.activeNotebookPanel;
            const cell = this.notebookTools.activeCell;
            if (cell == null)
                return;
            this._updatingMetadata = true;
            // An object representing the cell metadata to modify.
            const cellMetadataObject = {};
            // An object representing the notebook metadata to modify.
            const notebookMetadataObject = {};
            for (let [metadataKey, value] of Object.entries(formData)) {
                // Continue if the metadataKey does not exist in schema.
                if (!this.metadataKeys.includes(metadataKey))
                    continue;
                // Continue if the metadataKey is a notebook level one and there is no NotebookModel.
                if (((_a = this._metaInformation[metadataKey]) === null || _a === void 0 ? void 0 : _a.level) === 'notebook' &&
                    this._notebookModelNull)
                    continue;
                // Continue if the metadataKey is not applicable to the cell type.
                if (((_b = this._metaInformation[metadataKey]) === null || _b === void 0 ? void 0 : _b.cellTypes) &&
                    !((_d = (_c = this._metaInformation[metadataKey]) === null || _c === void 0 ? void 0 : _c.cellTypes) === null || _d === void 0 ? void 0 : _d.includes(cell.model.type))) {
                    continue;
                }
                let currentMetadata;
                let metadataObject;
                // Linking the working variable to the corresponding metadata and representation.
                if (((_e = this._metaInformation[metadataKey]) === null || _e === void 0 ? void 0 : _e.level) === 'notebook') {
                    // Working on notebook metadata.
                    currentMetadata = notebook.model.metadata;
                    metadataObject = notebookMetadataObject;
                }
                else {
                    // Working on cell metadata.
                    currentMetadata = cell.model.metadata;
                    metadataObject = cellMetadataObject;
                }
                // Remove first and last '/' if necessary and split the path.
                let nestedKey = metadataKey
                    .replace(/^\/+/, '')
                    .replace(/\/+$/, '')
                    .split('/');
                let baseMetadataKey = nestedKey[0];
                if (baseMetadataKey == undefined)
                    continue;
                let writeFinalData = value !== undefined &&
                    (((_g = (_f = this._metaInformation[metadataKey]) === null || _f === void 0 ? void 0 : _f.writeDefault) !== null && _g !== void 0 ? _g : true) ||
                        value !== ((_h = this._metaInformation[metadataKey]) === null || _h === void 0 ? void 0 : _h.default));
                // If metadata key is at root of metadata no need to go further.
                if (nestedKey.length == 1) {
                    if (writeFinalData)
                        metadataObject[baseMetadataKey] = value;
                    else
                        metadataObject[baseMetadataKey] = undefined;
                    continue;
                }
                let intermediateMetadataKeys = nestedKey.slice(1, -1);
                let finalMetadataKey = nestedKey[nestedKey.length - 1];
                // Deep copy of the metadata if not already done.
                if (!(baseMetadataKey in metadataObject)) {
                    metadataObject[baseMetadataKey] = currentMetadata[baseMetadataKey];
                }
                if (metadataObject[baseMetadataKey] === undefined)
                    metadataObject[baseMetadataKey] = {};
                // Let's have an object which points to the nested key.
                let workingObject = metadataObject[baseMetadataKey];
                let finalObjectReached = true;
                for (let nested of intermediateMetadataKeys) {
                    // If one of the nested object does not exist, this object is created
                    // only if there is a final data to write.
                    if (!(nested in workingObject)) {
                        if (!writeFinalData) {
                            finalObjectReached = false;
                            break;
                        }
                        else
                            workingObject[nested] = {};
                    }
                    workingObject = workingObject[nested];
                }
                // Write the value to the nested key or remove all empty object before the nested key,
                // only if the final object has been reached.
                if (finalObjectReached) {
                    if (!writeFinalData)
                        delete workingObject[finalMetadataKey];
                    else
                        workingObject[finalMetadataKey] = value;
                }
                // If the final nested data has been deleted, let see if there is not remaining
                // empty objects to remove.
                if (!writeFinalData) {
                    metadataObject[baseMetadataKey] = Private.deleteEmptyNested(metadataObject[baseMetadataKey], nestedKey.slice(1));
                    if (!Object.keys(metadataObject[baseMetadataKey])
                        .length)
                        metadataObject[baseMetadataKey] = undefined;
                }
            }
            // Set the cell metadata or delete it if value is undefined or empty object.
            for (let [key, value] of Object.entries(cellMetadataObject)) {
                if (value === undefined)
                    cell.model.deleteMetadata(key);
                else
                    cell.model.setMetadata(key, value);
            }
            // Set the notebook metadata or delete it if value is undefined or empty object.
            if (!this._notebookModelNull) {
                for (let [key, value] of Object.entries(notebookMetadataObject)) {
                    if (value === undefined)
                        notebook.model.deleteMetadata(key);
                    else
                        notebook.model.setMetadata(key, value);
                }
            }
            this._updatingMetadata = false;
            if (reload) {
                this._update();
            }
        };
        this._notebookModelNull = false;
        this._metadataSchema = options.metadataSchema;
        this._metaInformation = options.metaInformation;
        this._uiSchema = options.uiSchema || {};
        this._pluginId = options.pluginId;
        this._showModified = options.showModified || false;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._updatingMetadata = false;
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.SingletonLayout());
        const node = document.createElement('div');
        const content = document.createElement('div');
        content.textContent = this._trans.__('No metadata.');
        content.className = 'jp-MetadataForm-placeholderContent';
        node.appendChild(content);
        this._placeholder = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget({ node });
        this._placeholder.addClass('jp-MetadataForm-placeholder');
        layout.widget = this._placeholder;
    }
    /**
     * Get the form object itself.
     */
    get form() {
        return this._form;
    }
    /**
     * Get the list of existing metadataKey (array of string).
     *
     * ## NOTE:
     * The list contains also the conditional fields, which are not necessary
     * displayed and filled.
     */
    get metadataKeys() {
        var _a;
        const metadataKeys = [];
        // MetadataKey from schema.
        for (let metadataKey of Object.keys(this._metadataSchema.properties)) {
            metadataKeys.push(metadataKey);
        }
        // Possible additional metadataKeys from conditional schema.
        (_a = this._metadataSchema.allOf) === null || _a === void 0 ? void 0 : _a.forEach(conditional => {
            if (conditional.then !== undefined) {
                if (conditional.then.properties !== undefined) {
                    let properties = conditional.then
                        .properties;
                    for (let metadataKey of Object.keys(properties)) {
                        if (!metadataKeys.includes(metadataKey))
                            metadataKeys.push(metadataKey);
                    }
                }
            }
            if (conditional.else !== undefined) {
                if (conditional.else.properties !== undefined) {
                    let properties = conditional.else
                        .properties;
                    for (let metadataKey of Object.keys(properties)) {
                        if (!metadataKeys.includes(metadataKey))
                            metadataKeys.push(metadataKey);
                    }
                }
            }
        });
        return metadataKeys;
    }
    /**
     * Get the properties of a MetadataKey.
     *
     * @param metadataKey - metadataKey (string).
     */
    getProperties(metadataKey) {
        return (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.JSONExt.deepCopy(this._metadataSchema.properties[metadataKey]) || null);
    }
    /**
     * Set properties to a metadataKey.
     *
     * @param metadataKey - metadataKey (string).
     * @param properties - the properties to add or modify.
     */
    setProperties(metadataKey, properties) {
        Object.entries(properties).forEach(([key, value]) => {
            this._metadataSchema.properties[metadataKey][key] = value;
        });
    }
    /**
     * Set the content of the widget.
     */
    setContent(content) {
        const layout = this.layout;
        if (layout.widget) {
            layout.widget.removeClass('jp-MetadataForm-content');
            layout.removeWidget(layout.widget);
        }
        if (!content) {
            content = this._placeholder;
        }
        content.addClass('jp-MetadataForm-content');
        layout.widget = content;
    }
    /**
     * Build widget.
     */
    buildWidget(props) {
        this._form = new _form__WEBPACK_IMPORTED_MODULE_5__.FormWidget(props);
        this._form.addClass('jp-MetadataForm');
        this.setContent(this._form);
    }
    /**
     * Update the form when the widget is displayed.
     */
    onAfterShow(msg) {
        this._update();
    }
    /**
     * Handle a change to the active cell.
     */
    onActiveCellChanged(msg) {
        if (this.isVisible)
            this._update();
    }
    /**
     * Handle a change to the active cell metadata.
     */
    onActiveCellMetadataChanged(_) {
        if (!this._updatingMetadata && this.isVisible)
            this._update();
    }
    /**
     * Handle when the active notebook panel changes.
     */
    onActiveNotebookPanelChanged(_) {
        const notebook = this.notebookTools.activeNotebookPanel;
        this._notebookModelNull = notebook === null || notebook.model === null;
        if (!this._updatingMetadata && this.isVisible)
            this._update();
    }
    /**
     * Handle a change to the active notebook metadata.
     */
    onActiveNotebookPanelMetadataChanged(msg) {
        if (!this._updatingMetadata && this.isVisible)
            this._update();
    }
    /**
     * Update the form with current cell metadata, and remove inconsistent fields.
     */
    _update() {
        var _a, _b, _c, _d, _e;
        const notebook = this.notebookTools.activeNotebookPanel;
        const cell = this.notebookTools.activeCell;
        if (cell == undefined)
            return;
        const formProperties = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.JSONExt.deepCopy(this._metadataSchema);
        const formData = {};
        for (let metadataKey of Object.keys(this._metadataSchema.properties || _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.JSONExt.emptyObject)) {
            // Do not display the field if it's Notebook metadata and the notebook model is null.
            if (((_a = this._metaInformation[metadataKey]) === null || _a === void 0 ? void 0 : _a.level) === 'notebook' &&
                this._notebookModelNull) {
                delete formProperties.properties[metadataKey];
                continue;
            }
            // Do not display the field if the active cell's type is not involved.
            if (((_b = this._metaInformation[metadataKey]) === null || _b === void 0 ? void 0 : _b.cellTypes) &&
                !((_d = (_c = this._metaInformation[metadataKey]) === null || _c === void 0 ? void 0 : _c.cellTypes) === null || _d === void 0 ? void 0 : _d.includes(cell.model.type))) {
                delete formProperties.properties[metadataKey];
                continue;
            }
            let workingObject;
            // Remove the first and last '/' if exist, nad split the path.
            let nestedKeys = metadataKey
                .replace(/^\/+/, '')
                .replace(/\/+$/, '')
                .split('/');
            // Associates the correct metadata object to the working object.
            if (((_e = this._metaInformation[metadataKey]) === null || _e === void 0 ? void 0 : _e.level) === 'notebook') {
                workingObject = notebook.model.metadata;
            }
            else {
                workingObject = cell.model.metadata;
            }
            let hasValue = true;
            // Navigate to the value.
            for (let nested of nestedKeys) {
                if (nested in workingObject)
                    workingObject = workingObject[nested];
                else {
                    hasValue = false;
                    break;
                }
            }
            // Fill the formData with the current metadata value.
            if (hasValue)
                formData[metadataKey] = workingObject;
        }
        this.buildWidget({
            properties: formProperties,
            settings: new _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.BaseSettings({
                schema: this._metadataSchema
            }),
            uiSchema: this._uiSchema,
            translator: this.translator || null,
            formData: formData,
            metadataFormWidget: this,
            showModified: this._showModified,
            pluginId: this._pluginId
        });
    }
}
var Private;
(function (Private) {
    /**
     * Recursive function to clean the empty nested metadata before updating real metadata.
     * this function is called when a nested metadata is undefined (or default), so maybe some
     * object are now empty.
     * @param metadataObject: PartialJSONObject representing the metadata to update.
     * @param metadataKeysList: Array<string> of the undefined nested metadata.
     * @returns PartialJSONObject without empty object.
     */
    function deleteEmptyNested(metadataObject, metadataKeysList) {
        let metadataKey = metadataKeysList.shift();
        if (metadataKey !== undefined && metadataKey in metadataObject) {
            if (Object.keys(metadataObject[metadataKey]).length)
                metadataObject[metadataKey] = deleteEmptyNested(metadataObject[metadataKey], metadataKeysList);
            if (!Object.keys(metadataObject[metadataKey]).length)
                delete metadataObject[metadataKey];
        }
        return metadataObject;
    }
    Private.deleteEmptyNested = deleteEmptyNested;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/metadataform/lib/metadataformProvider.js":
/*!************************************************************!*\
  !*** ../packages/metadataform/lib/metadataformProvider.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MetadataFormProvider": () => (/* binding */ MetadataFormProvider)
/* harmony export */ });
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
class MetadataFormProvider {
    constructor() {
        this._items = {};
    }
    add(id, widget) {
        if (!this._items[id]) {
            this._items[id] = widget;
        }
        else {
            console.warn(`A MetadataformWidget is already registered with id ${id}`);
        }
    }
    get(id) {
        if (this._items[id]) {
            return this._items[id];
        }
        else {
            console.warn(`There is no MetadataformWidget registered with id ${id}`);
        }
    }
}


/***/ }),

/***/ "../packages/metadataform/lib/token.js":
/*!*********************************************!*\
  !*** ../packages/metadataform/lib/token.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMetadataFormProvider": () => (/* binding */ IMetadataFormProvider)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module metadataform
 */

/**
 * The metadata form provider token.
 */
const IMetadataFormProvider = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/metadataform:IMetadataFormProvider', `A service to register new metadata editor widgets.`);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWV0YWRhdGFmb3JtX2xpYl9pbmRleF9qcy45YjFmYmQ0ZTk1YTYxNTRmNmM2OS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUVnRDtBQUNPO0FBR1Q7QUFFdkI7QUFJMUI7O0dBRUc7QUFDSSxNQUFNLFVBQVcsU0FBUSw2REFBVztJQUN6Qzs7T0FFRztJQUNILFlBQVksS0FBMEI7UUFDcEMsS0FBSyxFQUFFLENBQUM7UUFDUixJQUFJLENBQUMsUUFBUSxDQUFDLGVBQWUsQ0FBQyxDQUFDO1FBQy9CLElBQUksQ0FBQyxNQUFNLEdBQUcsS0FBSyxDQUFDO0lBQ3RCLENBQUM7SUFFRDs7O09BR0c7SUFDSCxNQUFNO1FBQ0osTUFBTSxXQUFXLEdBQUc7WUFDbEIsZUFBZSxFQUFFLElBQUksQ0FBQyxNQUFNLENBQUMsUUFBUSxDQUFDLE9BQU8sRUFBRTtZQUMvQyxjQUFjLEVBQUUsSUFBSSxDQUFDLE1BQU0sQ0FBQyxrQkFBa0IsQ0FBQyxjQUFjO1NBQzlELENBQUM7UUFDRixPQUFPLENBQ0wsMkRBQUMsb0VBQWEsSUFDWixTQUFTLEVBQUUsNkRBQWEsRUFDeEIsTUFBTSxFQUFFLElBQUksQ0FBQyxNQUFNLENBQUMsVUFBeUIsRUFDN0MsUUFBUSxFQUFFLElBQUksQ0FBQyxNQUFNLENBQUMsUUFBK0IsRUFDckQsV0FBVyxFQUFFLFdBQVcsRUFDeEIsUUFBUSxFQUFFLElBQUksQ0FBQyxNQUFNLENBQUMsUUFBUSxFQUM5QixZQUFZLFFBQ1osUUFBUSxFQUFFLG1CQUFtQixJQUFJLENBQUMsTUFBTSxDQUFDLFFBQVEsRUFBRSxFQUNuRCxRQUFRLEVBQUUsQ0FBQyxDQUEwQyxFQUFFLEVBQUU7Z0JBQ3ZELElBQUksQ0FBQyxNQUFNLENBQUMsa0JBQWtCLENBQUMsY0FBYyxDQUFDLENBQUMsQ0FBQyxRQUFRLElBQUksRUFBRSxDQUFDLENBQUM7WUFDbEUsQ0FBQyxF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LENBQUMsRUFoQ1MsT0FBTyxLQUFQLE9BQU8sUUFnQ2hCOzs7Ozs7Ozs7Ozs7Ozs7QUNyZUQ7OztHQUdHO0FBSUksTUFBTSxvQkFBb0I7SUFBakM7UUFpQkUsV0FBTSxHQUFpRCxFQUFFLENBQUM7SUFDNUQsQ0FBQztJQWpCQyxHQUFHLENBQUMsRUFBVSxFQUFFLE1BQWtDO1FBQ2hELElBQUksQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FBQyxFQUFFO1lBQ3BCLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLEdBQUcsTUFBTSxDQUFDO1NBQzFCO2FBQU07WUFDTCxPQUFPLENBQUMsSUFBSSxDQUFDLHNEQUFzRCxFQUFFLEVBQUUsQ0FBQyxDQUFDO1NBQzFFO0lBQ0gsQ0FBQztJQUVELEdBQUcsQ0FBQyxFQUFVO1FBQ1osSUFBSSxJQUFJLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FBQyxFQUFFO1lBQ25CLE9BQU8sSUFBSSxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsQ0FBQztTQUN4QjthQUFNO1lBQ0wsT0FBTyxDQUFDLElBQUksQ0FBQyxxREFBcUQsRUFBRSxFQUFFLENBQUMsQ0FBQztTQUN6RTtJQUNILENBQUM7Q0FHRjs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN6QkQsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFVd0I7QUF1TTNCOztHQUVHO0FBQ0ksTUFBTSxxQkFBcUIsR0FBRyxJQUFJLG9EQUFLLENBQzVDLGdEQUFnRCxFQUNoRCxvREFBb0QsQ0FDckQsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tZXRhZGF0YWZvcm0vc3JjL2Zvcm0udHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tZXRhZGF0YWZvcm0vc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tZXRhZGF0YWZvcm0vc3JjL21ldGFkYXRhZm9ybS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWV0YWRhdGFmb3JtL3NyYy9tZXRhZGF0YWZvcm1Qcm92aWRlci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWV0YWRhdGFmb3JtL3NyYy90b2tlbi50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBtZXRhZGF0YWZvcm1cbiAqL1xuXG5pbXBvcnQgeyBSZWFjdFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IEZvcm1Db21wb25lbnQgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJQ2hhbmdlRXZlbnQgfSBmcm9tICdAcmpzZi9jb3JlJztcbmltcG9ydCB2YWxpZGF0b3JBanY4IGZyb20gJ0ByanNmL3ZhbGlkYXRvci1hanY4JztcbmltcG9ydCB7IEpTT05TY2hlbWE3IH0gZnJvbSAnanNvbi1zY2hlbWEnO1xuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcblxuaW1wb3J0IHsgTWV0YWRhdGFGb3JtIH0gZnJvbSAnLi90b2tlbic7XG5cbi8qKlxuICogQSBSZWFjdFdpZGdldCB3aXRoIHRoZSBmb3JtIGl0c2VsZi5cbiAqL1xuZXhwb3J0IGNsYXNzIEZvcm1XaWRnZXQgZXh0ZW5kcyBSZWFjdFdpZGdldCB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3RzIGEgbmV3IEZvcm1XaWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3Rvcihwcm9wczogTWV0YWRhdGFGb3JtLklQcm9wcykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtRm9ybVdpZGdldCcpO1xuICAgIHRoaXMuX3Byb3BzID0gcHJvcHM7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIHRoZSBmb3JtLlxuICAgKiBAcmV0dXJucyAtIFRoZSByZW5kZXJlZCBmb3JtXG4gICAqL1xuICByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgIGNvbnN0IGZvcm1Db250ZXh0ID0ge1xuICAgICAgZGVmYXVsdEZvcm1EYXRhOiB0aGlzLl9wcm9wcy5zZXR0aW5ncy5kZWZhdWx0KCksXG4gICAgICB1cGRhdGVNZXRhZGF0YTogdGhpcy5fcHJvcHMubWV0YWRhdGFGb3JtV2lkZ2V0LnVwZGF0ZU1ldGFkYXRhXG4gICAgfTtcbiAgICByZXR1cm4gKFxuICAgICAgPEZvcm1Db21wb25lbnRcbiAgICAgICAgdmFsaWRhdG9yPXt2YWxpZGF0b3JBanY4fVxuICAgICAgICBzY2hlbWE9e3RoaXMuX3Byb3BzLnByb3BlcnRpZXMgYXMgSlNPTlNjaGVtYTd9XG4gICAgICAgIGZvcm1EYXRhPXt0aGlzLl9wcm9wcy5mb3JtRGF0YSBhcyBSZWNvcmQ8c3RyaW5nLCBhbnk+fVxuICAgICAgICBmb3JtQ29udGV4dD17Zm9ybUNvbnRleHR9XG4gICAgICAgIHVpU2NoZW1hPXt0aGlzLl9wcm9wcy51aVNjaGVtYX1cbiAgICAgICAgbGl2ZVZhbGlkYXRlXG4gICAgICAgIGlkUHJlZml4PXtganAtTWV0YWRhdGFGb3JtLSR7dGhpcy5fcHJvcHMucGx1Z2luSWR9YH1cbiAgICAgICAgb25DaGFuZ2U9eyhlOiBJQ2hhbmdlRXZlbnQ8UmVhZG9ubHlQYXJ0aWFsSlNPTk9iamVjdD4pID0+IHtcbiAgICAgICAgICB0aGlzLl9wcm9wcy5tZXRhZGF0YUZvcm1XaWRnZXQudXBkYXRlTWV0YWRhdGEoZS5mb3JtRGF0YSB8fCB7fSk7XG4gICAgICAgIH19XG4gICAgICAgIGNvbXBhY3Q9e3RydWV9XG4gICAgICAgIHNob3dNb2RpZmllZEZyb21EZWZhdWx0PXt0aGlzLl9wcm9wcy5zaG93TW9kaWZpZWR9XG4gICAgICAgIHRyYW5zbGF0b3I9e3RoaXMuX3Byb3BzLnRyYW5zbGF0b3J9XG4gICAgICAvPlxuICAgICk7XG4gIH1cblxuICBwcml2YXRlIF9wcm9wczogTWV0YWRhdGFGb3JtLklQcm9wcztcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG1ldGFkYXRhZm9ybVxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vZm9ybSc7XG5leHBvcnQgKiBmcm9tICcuL21ldGFkYXRhZm9ybSc7XG5leHBvcnQgKiBmcm9tICcuL21ldGFkYXRhZm9ybVByb3ZpZGVyJztcbmV4cG9ydCAqIGZyb20gJy4vdG9rZW4nO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWV0YWRhdGFmb3JtXG4gKi9cblxuaW1wb3J0IHsgTm90ZWJvb2tUb29scyB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7IEJhc2VTZXR0aW5ncyB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7XG4gIEpTT05FeHQsXG4gIEpTT05PYmplY3QsXG4gIEpTT05WYWx1ZSxcbiAgUGFydGlhbEpTT05PYmplY3QsXG4gIFBhcnRpYWxKU09OVmFsdWUsXG4gIFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3QsXG4gIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZVxufSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgU2luZ2xldG9uTGF5b3V0LCBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG5pbXBvcnQgeyBNZXRhZGF0YUZvcm0gfSBmcm9tICcuL3Rva2VuJztcbmltcG9ydCB7IEZvcm1XaWRnZXQgfSBmcm9tICcuL2Zvcm0nO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCBjcmVhdGUgYSBtZXRhZGF0YSBmb3JtIHdpZGdldFxuICovXG5leHBvcnQgY2xhc3MgTWV0YWRhdGFGb3JtV2lkZ2V0XG4gIGV4dGVuZHMgTm90ZWJvb2tUb29scy5Ub29sXG4gIGltcGxlbWVudHMgTWV0YWRhdGFGb3JtLklNZXRhZGF0YUZvcm1cbntcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhbiBlbXB0eSB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBNZXRhZGF0YUZvcm0uSU9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX21ldGFkYXRhU2NoZW1hID0gb3B0aW9ucy5tZXRhZGF0YVNjaGVtYTtcbiAgICB0aGlzLl9tZXRhSW5mb3JtYXRpb24gPSBvcHRpb25zLm1ldGFJbmZvcm1hdGlvbjtcbiAgICB0aGlzLl91aVNjaGVtYSA9IG9wdGlvbnMudWlTY2hlbWEgfHwge307XG4gICAgdGhpcy5fcGx1Z2luSWQgPSBvcHRpb25zLnBsdWdpbklkO1xuICAgIHRoaXMuX3Nob3dNb2RpZmllZCA9IG9wdGlvbnMuc2hvd01vZGlmaWVkIHx8IGZhbHNlO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgdGhpcy5fdXBkYXRpbmdNZXRhZGF0YSA9IGZhbHNlO1xuICAgIGNvbnN0IGxheW91dCA9ICh0aGlzLmxheW91dCA9IG5ldyBTaW5nbGV0b25MYXlvdXQoKSk7XG5cbiAgICBjb25zdCBub2RlID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG4gICAgY29uc3QgY29udGVudCA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2RpdicpO1xuICAgIGNvbnRlbnQudGV4dENvbnRlbnQgPSB0aGlzLl90cmFucy5fXygnTm8gbWV0YWRhdGEuJyk7XG4gICAgY29udGVudC5jbGFzc05hbWUgPSAnanAtTWV0YWRhdGFGb3JtLXBsYWNlaG9sZGVyQ29udGVudCc7XG4gICAgbm9kZS5hcHBlbmRDaGlsZChjb250ZW50KTtcbiAgICB0aGlzLl9wbGFjZWhvbGRlciA9IG5ldyBXaWRnZXQoeyBub2RlIH0pO1xuICAgIHRoaXMuX3BsYWNlaG9sZGVyLmFkZENsYXNzKCdqcC1NZXRhZGF0YUZvcm0tcGxhY2Vob2xkZXInKTtcbiAgICBsYXlvdXQud2lkZ2V0ID0gdGhpcy5fcGxhY2Vob2xkZXI7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBmb3JtIG9iamVjdCBpdHNlbGYuXG4gICAqL1xuICBnZXQgZm9ybSgpOiBGb3JtV2lkZ2V0IHwgdW5kZWZpbmVkIHtcbiAgICByZXR1cm4gdGhpcy5fZm9ybTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGxpc3Qgb2YgZXhpc3RpbmcgbWV0YWRhdGFLZXkgKGFycmF5IG9mIHN0cmluZykuXG4gICAqXG4gICAqICMjIE5PVEU6XG4gICAqIFRoZSBsaXN0IGNvbnRhaW5zIGFsc28gdGhlIGNvbmRpdGlvbmFsIGZpZWxkcywgd2hpY2ggYXJlIG5vdCBuZWNlc3NhcnlcbiAgICogZGlzcGxheWVkIGFuZCBmaWxsZWQuXG4gICAqL1xuICBnZXQgbWV0YWRhdGFLZXlzKCk6IHN0cmluZ1tdIHtcbiAgICBjb25zdCBtZXRhZGF0YUtleXM6IHN0cmluZ1tdID0gW107XG5cbiAgICAvLyBNZXRhZGF0YUtleSBmcm9tIHNjaGVtYS5cbiAgICBmb3IgKGxldCBtZXRhZGF0YUtleSBvZiBPYmplY3Qua2V5cyh0aGlzLl9tZXRhZGF0YVNjaGVtYS5wcm9wZXJ0aWVzKSkge1xuICAgICAgbWV0YWRhdGFLZXlzLnB1c2gobWV0YWRhdGFLZXkpO1xuICAgIH1cblxuICAgIC8vIFBvc3NpYmxlIGFkZGl0aW9uYWwgbWV0YWRhdGFLZXlzIGZyb20gY29uZGl0aW9uYWwgc2NoZW1hLlxuICAgIHRoaXMuX21ldGFkYXRhU2NoZW1hLmFsbE9mPy5mb3JFYWNoKGNvbmRpdGlvbmFsID0+IHtcbiAgICAgIGlmIChjb25kaXRpb25hbC50aGVuICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgaWYgKChjb25kaXRpb25hbC50aGVuIGFzIFBhcnRpYWxKU09OT2JqZWN0KS5wcm9wZXJ0aWVzICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICBsZXQgcHJvcGVydGllcyA9IChjb25kaXRpb25hbC50aGVuIGFzIFBhcnRpYWxKU09OT2JqZWN0KVxuICAgICAgICAgICAgLnByb3BlcnRpZXMgYXMgUGFydGlhbEpTT05PYmplY3Q7XG4gICAgICAgICAgZm9yIChsZXQgbWV0YWRhdGFLZXkgb2YgT2JqZWN0LmtleXMocHJvcGVydGllcykpIHtcbiAgICAgICAgICAgIGlmICghbWV0YWRhdGFLZXlzLmluY2x1ZGVzKG1ldGFkYXRhS2V5KSlcbiAgICAgICAgICAgICAgbWV0YWRhdGFLZXlzLnB1c2gobWV0YWRhdGFLZXkpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfVxuXG4gICAgICBpZiAoY29uZGl0aW9uYWwuZWxzZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIGlmICgoY29uZGl0aW9uYWwuZWxzZSBhcyBQYXJ0aWFsSlNPTk9iamVjdCkucHJvcGVydGllcyAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgbGV0IHByb3BlcnRpZXMgPSAoY29uZGl0aW9uYWwuZWxzZSBhcyBQYXJ0aWFsSlNPTk9iamVjdClcbiAgICAgICAgICAgIC5wcm9wZXJ0aWVzIGFzIFBhcnRpYWxKU09OT2JqZWN0O1xuICAgICAgICAgIGZvciAobGV0IG1ldGFkYXRhS2V5IG9mIE9iamVjdC5rZXlzKHByb3BlcnRpZXMpKSB7XG4gICAgICAgICAgICBpZiAoIW1ldGFkYXRhS2V5cy5pbmNsdWRlcyhtZXRhZGF0YUtleSkpXG4gICAgICAgICAgICAgIG1ldGFkYXRhS2V5cy5wdXNoKG1ldGFkYXRhS2V5KTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHJldHVybiBtZXRhZGF0YUtleXM7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBwcm9wZXJ0aWVzIG9mIGEgTWV0YWRhdGFLZXkuXG4gICAqXG4gICAqIEBwYXJhbSBtZXRhZGF0YUtleSAtIG1ldGFkYXRhS2V5IChzdHJpbmcpLlxuICAgKi9cbiAgZ2V0UHJvcGVydGllcyhtZXRhZGF0YUtleTogc3RyaW5nKTogUGFydGlhbEpTT05PYmplY3QgfCBudWxsIHtcbiAgICByZXR1cm4gKFxuICAgICAgSlNPTkV4dC5kZWVwQ29weSh0aGlzLl9tZXRhZGF0YVNjaGVtYS5wcm9wZXJ0aWVzW21ldGFkYXRhS2V5XSkgfHwgbnVsbFxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHByb3BlcnRpZXMgdG8gYSBtZXRhZGF0YUtleS5cbiAgICpcbiAgICogQHBhcmFtIG1ldGFkYXRhS2V5IC0gbWV0YWRhdGFLZXkgKHN0cmluZykuXG4gICAqIEBwYXJhbSBwcm9wZXJ0aWVzIC0gdGhlIHByb3BlcnRpZXMgdG8gYWRkIG9yIG1vZGlmeS5cbiAgICovXG4gIHNldFByb3BlcnRpZXMobWV0YWRhdGFLZXk6IHN0cmluZywgcHJvcGVydGllczogUGFydGlhbEpTT05PYmplY3QpOiB2b2lkIHtcbiAgICBPYmplY3QuZW50cmllcyhwcm9wZXJ0aWVzKS5mb3JFYWNoKChba2V5LCB2YWx1ZV0pID0+IHtcbiAgICAgIHRoaXMuX21ldGFkYXRhU2NoZW1hLnByb3BlcnRpZXNbbWV0YWRhdGFLZXldW2tleV0gPSB2YWx1ZTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBVcGRhdGUgdGhlIG1ldGFkYXRhIG9mIHRoZSBjdXJyZW50IGNlbGwgb3Igbm90ZWJvb2suXG4gICAqXG4gICAqIEBwYXJhbSBmb3JtRGF0YSAtIHRoZSBjZWxsIG1ldGFkYXRhIHNldCBpbiB0aGUgZm9ybS5cbiAgICogQHBhcmFtIHJlbG9hZCAtIHdoZXRoZXIgdG8gdXBkYXRlIHRoZSBmb3JtIGFmdGVyIHVwZGF0aW5nIHRoZSBtZXRhZGF0YS5cbiAgICpcbiAgICogIyMgTm90ZXNcbiAgICogTWV0YWRhdGEgYXJlIHVwZGF0ZWQgZnJvbSByb290IG9ubHkuIElmIHNvbWUgbWV0YWRhdGEgaXMgbmVzdGVkLFxuICAgKiB0aGUgd2hvbGUgcm9vdCBvYmplY3QgbXVzdCBiZSB1cGRhdGVkLlxuICAgKiBUaGlzIGZ1bmN0aW9uIGJ1aWxkIGFuIG9iamVjdCB3aXRoIGFsbCB0aGUgcm9vdCBvYmplY3QgdG8gdXBkYXRlXG4gICAqIGluIG1ldGFkYXRhIGJlZm9yZSBwZXJmb3JtaW5nIHVwZGF0ZS5cbiAgICogSXQgdXNlcyBhbiBhcnJvdyBmdW5jdGlvbiB0byBhbGxvdyB1c2luZyAndGhpcycgcHJvcGVybHkgd2hlbiBjYWxsZWQgZnJvbSBhIGN1c3RvbSBmaWVsZC5cbiAgICovXG4gIHVwZGF0ZU1ldGFkYXRhID0gKFxuICAgIGZvcm1EYXRhOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICAgIHJlbG9hZD86IGJvb2xlYW5cbiAgKTogdm9pZCA9PiB7XG4gICAgaWYgKHRoaXMubm90ZWJvb2tUb29scyA9PSB1bmRlZmluZWQpIHJldHVybjtcblxuICAgIGNvbnN0IG5vdGVib29rID0gdGhpcy5ub3RlYm9va1Rvb2xzLmFjdGl2ZU5vdGVib29rUGFuZWw7XG5cbiAgICBjb25zdCBjZWxsID0gdGhpcy5ub3RlYm9va1Rvb2xzLmFjdGl2ZUNlbGw7XG4gICAgaWYgKGNlbGwgPT0gbnVsbCkgcmV0dXJuO1xuXG4gICAgdGhpcy5fdXBkYXRpbmdNZXRhZGF0YSA9IHRydWU7XG5cbiAgICAvLyBBbiBvYmplY3QgcmVwcmVzZW50aW5nIHRoZSBjZWxsIG1ldGFkYXRhIHRvIG1vZGlmeS5cbiAgICBjb25zdCBjZWxsTWV0YWRhdGFPYmplY3Q6IFByaXZhdGUuSU1ldGFkYXRhUmVwcmVzZW50YXRpb24gPSB7fTtcblxuICAgIC8vIEFuIG9iamVjdCByZXByZXNlbnRpbmcgdGhlIG5vdGVib29rIG1ldGFkYXRhIHRvIG1vZGlmeS5cbiAgICBjb25zdCBub3RlYm9va01ldGFkYXRhT2JqZWN0OiBQcml2YXRlLklNZXRhZGF0YVJlcHJlc2VudGF0aW9uID0ge307XG5cbiAgICBmb3IgKGxldCBbbWV0YWRhdGFLZXksIHZhbHVlXSBvZiBPYmplY3QuZW50cmllcyhmb3JtRGF0YSkpIHtcbiAgICAgIC8vIENvbnRpbnVlIGlmIHRoZSBtZXRhZGF0YUtleSBkb2VzIG5vdCBleGlzdCBpbiBzY2hlbWEuXG4gICAgICBpZiAoIXRoaXMubWV0YWRhdGFLZXlzLmluY2x1ZGVzKG1ldGFkYXRhS2V5KSkgY29udGludWU7XG5cbiAgICAgIC8vIENvbnRpbnVlIGlmIHRoZSBtZXRhZGF0YUtleSBpcyBhIG5vdGVib29rIGxldmVsIG9uZSBhbmQgdGhlcmUgaXMgbm8gTm90ZWJvb2tNb2RlbC5cbiAgICAgIGlmIChcbiAgICAgICAgdGhpcy5fbWV0YUluZm9ybWF0aW9uW21ldGFkYXRhS2V5XT8ubGV2ZWwgPT09ICdub3RlYm9vaycgJiZcbiAgICAgICAgdGhpcy5fbm90ZWJvb2tNb2RlbE51bGxcbiAgICAgIClcbiAgICAgICAgY29udGludWU7XG5cbiAgICAgIC8vIENvbnRpbnVlIGlmIHRoZSBtZXRhZGF0YUtleSBpcyBub3QgYXBwbGljYWJsZSB0byB0aGUgY2VsbCB0eXBlLlxuICAgICAgaWYgKFxuICAgICAgICB0aGlzLl9tZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldPy5jZWxsVHlwZXMgJiZcbiAgICAgICAgIXRoaXMuX21ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0/LmNlbGxUeXBlcz8uaW5jbHVkZXMoXG4gICAgICAgICAgY2VsbC5tb2RlbC50eXBlXG4gICAgICAgIClcbiAgICAgICkge1xuICAgICAgICBjb250aW51ZTtcbiAgICAgIH1cbiAgICAgIGxldCBjdXJyZW50TWV0YWRhdGE6IFBhcnRpYWxKU09OT2JqZWN0O1xuICAgICAgbGV0IG1ldGFkYXRhT2JqZWN0OiBQcml2YXRlLklNZXRhZGF0YVJlcHJlc2VudGF0aW9uO1xuXG4gICAgICAvLyBMaW5raW5nIHRoZSB3b3JraW5nIHZhcmlhYmxlIHRvIHRoZSBjb3JyZXNwb25kaW5nIG1ldGFkYXRhIGFuZCByZXByZXNlbnRhdGlvbi5cbiAgICAgIGlmICh0aGlzLl9tZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldPy5sZXZlbCA9PT0gJ25vdGVib29rJykge1xuICAgICAgICAvLyBXb3JraW5nIG9uIG5vdGVib29rIG1ldGFkYXRhLlxuICAgICAgICBjdXJyZW50TWV0YWRhdGEgPSBub3RlYm9vayEubW9kZWwhLm1ldGFkYXRhO1xuICAgICAgICBtZXRhZGF0YU9iamVjdCA9IG5vdGVib29rTWV0YWRhdGFPYmplY3Q7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICAvLyBXb3JraW5nIG9uIGNlbGwgbWV0YWRhdGEuXG4gICAgICAgIGN1cnJlbnRNZXRhZGF0YSA9IGNlbGwubW9kZWwubWV0YWRhdGE7XG4gICAgICAgIG1ldGFkYXRhT2JqZWN0ID0gY2VsbE1ldGFkYXRhT2JqZWN0O1xuICAgICAgfVxuXG4gICAgICAvLyBSZW1vdmUgZmlyc3QgYW5kIGxhc3QgJy8nIGlmIG5lY2Vzc2FyeSBhbmQgc3BsaXQgdGhlIHBhdGguXG4gICAgICBsZXQgbmVzdGVkS2V5ID0gbWV0YWRhdGFLZXlcbiAgICAgICAgLnJlcGxhY2UoL15cXC8rLywgJycpXG4gICAgICAgIC5yZXBsYWNlKC9cXC8rJC8sICcnKVxuICAgICAgICAuc3BsaXQoJy8nKTtcblxuICAgICAgbGV0IGJhc2VNZXRhZGF0YUtleSA9IG5lc3RlZEtleVswXTtcbiAgICAgIGlmIChiYXNlTWV0YWRhdGFLZXkgPT0gdW5kZWZpbmVkKSBjb250aW51ZTtcblxuICAgICAgbGV0IHdyaXRlRmluYWxEYXRhID1cbiAgICAgICAgdmFsdWUgIT09IHVuZGVmaW5lZCAmJlxuICAgICAgICAoKHRoaXMuX21ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0/LndyaXRlRGVmYXVsdCA/PyB0cnVlKSB8fFxuICAgICAgICAgIHZhbHVlICE9PSB0aGlzLl9tZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldPy5kZWZhdWx0KTtcblxuICAgICAgLy8gSWYgbWV0YWRhdGEga2V5IGlzIGF0IHJvb3Qgb2YgbWV0YWRhdGEgbm8gbmVlZCB0byBnbyBmdXJ0aGVyLlxuICAgICAgaWYgKG5lc3RlZEtleS5sZW5ndGggPT0gMSkge1xuICAgICAgICBpZiAod3JpdGVGaW5hbERhdGEpXG4gICAgICAgICAgbWV0YWRhdGFPYmplY3RbYmFzZU1ldGFkYXRhS2V5XSA9IHZhbHVlIGFzIFBhcnRpYWxKU09OVmFsdWU7XG4gICAgICAgIGVsc2UgbWV0YWRhdGFPYmplY3RbYmFzZU1ldGFkYXRhS2V5XSA9IHVuZGVmaW5lZDtcbiAgICAgICAgY29udGludWU7XG4gICAgICB9XG5cbiAgICAgIGxldCBpbnRlcm1lZGlhdGVNZXRhZGF0YUtleXMgPSBuZXN0ZWRLZXkuc2xpY2UoMSwgLTEpO1xuICAgICAgbGV0IGZpbmFsTWV0YWRhdGFLZXkgPSBuZXN0ZWRLZXlbbmVzdGVkS2V5Lmxlbmd0aCAtIDFdO1xuXG4gICAgICAvLyBEZWVwIGNvcHkgb2YgdGhlIG1ldGFkYXRhIGlmIG5vdCBhbHJlYWR5IGRvbmUuXG4gICAgICBpZiAoIShiYXNlTWV0YWRhdGFLZXkgaW4gbWV0YWRhdGFPYmplY3QpKSB7XG4gICAgICAgIG1ldGFkYXRhT2JqZWN0W2Jhc2VNZXRhZGF0YUtleV0gPSBjdXJyZW50TWV0YWRhdGFbYmFzZU1ldGFkYXRhS2V5XTtcbiAgICAgIH1cbiAgICAgIGlmIChtZXRhZGF0YU9iamVjdFtiYXNlTWV0YWRhdGFLZXldID09PSB1bmRlZmluZWQpXG4gICAgICAgIG1ldGFkYXRhT2JqZWN0W2Jhc2VNZXRhZGF0YUtleV0gPSB7fTtcblxuICAgICAgLy8gTGV0J3MgaGF2ZSBhbiBvYmplY3Qgd2hpY2ggcG9pbnRzIHRvIHRoZSBuZXN0ZWQga2V5LlxuICAgICAgbGV0IHdvcmtpbmdPYmplY3Q6IFBhcnRpYWxKU09OT2JqZWN0ID0gbWV0YWRhdGFPYmplY3RbXG4gICAgICAgIGJhc2VNZXRhZGF0YUtleVxuICAgICAgXSBhcyBQYXJ0aWFsSlNPTk9iamVjdDtcblxuICAgICAgbGV0IGZpbmFsT2JqZWN0UmVhY2hlZCA9IHRydWU7XG5cbiAgICAgIGZvciAobGV0IG5lc3RlZCBvZiBpbnRlcm1lZGlhdGVNZXRhZGF0YUtleXMpIHtcbiAgICAgICAgLy8gSWYgb25lIG9mIHRoZSBuZXN0ZWQgb2JqZWN0IGRvZXMgbm90IGV4aXN0LCB0aGlzIG9iamVjdCBpcyBjcmVhdGVkXG4gICAgICAgIC8vIG9ubHkgaWYgdGhlcmUgaXMgYSBmaW5hbCBkYXRhIHRvIHdyaXRlLlxuICAgICAgICBpZiAoIShuZXN0ZWQgaW4gd29ya2luZ09iamVjdCkpIHtcbiAgICAgICAgICBpZiAoIXdyaXRlRmluYWxEYXRhKSB7XG4gICAgICAgICAgICBmaW5hbE9iamVjdFJlYWNoZWQgPSBmYWxzZTtcbiAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgIH0gZWxzZSB3b3JraW5nT2JqZWN0W25lc3RlZF0gPSB7fTtcbiAgICAgICAgfVxuICAgICAgICB3b3JraW5nT2JqZWN0ID0gd29ya2luZ09iamVjdFtuZXN0ZWRdIGFzIFBhcnRpYWxKU09OT2JqZWN0O1xuICAgICAgfVxuXG4gICAgICAvLyBXcml0ZSB0aGUgdmFsdWUgdG8gdGhlIG5lc3RlZCBrZXkgb3IgcmVtb3ZlIGFsbCBlbXB0eSBvYmplY3QgYmVmb3JlIHRoZSBuZXN0ZWQga2V5LFxuICAgICAgLy8gb25seSBpZiB0aGUgZmluYWwgb2JqZWN0IGhhcyBiZWVuIHJlYWNoZWQuXG4gICAgICBpZiAoZmluYWxPYmplY3RSZWFjaGVkKSB7XG4gICAgICAgIGlmICghd3JpdGVGaW5hbERhdGEpIGRlbGV0ZSB3b3JraW5nT2JqZWN0W2ZpbmFsTWV0YWRhdGFLZXldO1xuICAgICAgICBlbHNlIHdvcmtpbmdPYmplY3RbZmluYWxNZXRhZGF0YUtleV0gPSB2YWx1ZSBhcyBQYXJ0aWFsSlNPTlZhbHVlO1xuICAgICAgfVxuXG4gICAgICAvLyBJZiB0aGUgZmluYWwgbmVzdGVkIGRhdGEgaGFzIGJlZW4gZGVsZXRlZCwgbGV0IHNlZSBpZiB0aGVyZSBpcyBub3QgcmVtYWluaW5nXG4gICAgICAvLyBlbXB0eSBvYmplY3RzIHRvIHJlbW92ZS5cbiAgICAgIGlmICghd3JpdGVGaW5hbERhdGEpIHtcbiAgICAgICAgbWV0YWRhdGFPYmplY3RbYmFzZU1ldGFkYXRhS2V5XSA9IFByaXZhdGUuZGVsZXRlRW1wdHlOZXN0ZWQoXG4gICAgICAgICAgbWV0YWRhdGFPYmplY3RbYmFzZU1ldGFkYXRhS2V5XSBhcyBQYXJ0aWFsSlNPTk9iamVjdCxcbiAgICAgICAgICBuZXN0ZWRLZXkuc2xpY2UoMSlcbiAgICAgICAgKTtcbiAgICAgICAgaWYgKFxuICAgICAgICAgICFPYmplY3Qua2V5cyhtZXRhZGF0YU9iamVjdFtiYXNlTWV0YWRhdGFLZXldIGFzIFBhcnRpYWxKU09OT2JqZWN0KVxuICAgICAgICAgICAgLmxlbmd0aFxuICAgICAgICApXG4gICAgICAgICAgbWV0YWRhdGFPYmplY3RbYmFzZU1ldGFkYXRhS2V5XSA9IHVuZGVmaW5lZDtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBTZXQgdGhlIGNlbGwgbWV0YWRhdGEgb3IgZGVsZXRlIGl0IGlmIHZhbHVlIGlzIHVuZGVmaW5lZCBvciBlbXB0eSBvYmplY3QuXG4gICAgZm9yIChsZXQgW2tleSwgdmFsdWVdIG9mIE9iamVjdC5lbnRyaWVzKGNlbGxNZXRhZGF0YU9iamVjdCkpIHtcbiAgICAgIGlmICh2YWx1ZSA9PT0gdW5kZWZpbmVkKSBjZWxsLm1vZGVsLmRlbGV0ZU1ldGFkYXRhKGtleSk7XG4gICAgICBlbHNlIGNlbGwubW9kZWwuc2V0TWV0YWRhdGEoa2V5LCB2YWx1ZSBhcyBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUpO1xuICAgIH1cblxuICAgIC8vIFNldCB0aGUgbm90ZWJvb2sgbWV0YWRhdGEgb3IgZGVsZXRlIGl0IGlmIHZhbHVlIGlzIHVuZGVmaW5lZCBvciBlbXB0eSBvYmplY3QuXG4gICAgaWYgKCF0aGlzLl9ub3RlYm9va01vZGVsTnVsbCkge1xuICAgICAgZm9yIChsZXQgW2tleSwgdmFsdWVdIG9mIE9iamVjdC5lbnRyaWVzKG5vdGVib29rTWV0YWRhdGFPYmplY3QpKSB7XG4gICAgICAgIGlmICh2YWx1ZSA9PT0gdW5kZWZpbmVkKSBub3RlYm9vayEubW9kZWwhLmRlbGV0ZU1ldGFkYXRhKGtleSk7XG4gICAgICAgIGVsc2VcbiAgICAgICAgICBub3RlYm9vayEubW9kZWwhLnNldE1ldGFkYXRhKGtleSwgdmFsdWUgYXMgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICB0aGlzLl91cGRhdGluZ01ldGFkYXRhID0gZmFsc2U7XG5cbiAgICBpZiAocmVsb2FkKSB7XG4gICAgICB0aGlzLl91cGRhdGUoKTtcbiAgICB9XG4gIH07XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgY29udGVudCBvZiB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIHNldENvbnRlbnQoY29udGVudDogV2lkZ2V0IHwgbnVsbCk6IHZvaWQge1xuICAgIGNvbnN0IGxheW91dCA9IHRoaXMubGF5b3V0IGFzIFNpbmdsZXRvbkxheW91dDtcbiAgICBpZiAobGF5b3V0LndpZGdldCkge1xuICAgICAgbGF5b3V0LndpZGdldC5yZW1vdmVDbGFzcygnanAtTWV0YWRhdGFGb3JtLWNvbnRlbnQnKTtcbiAgICAgIGxheW91dC5yZW1vdmVXaWRnZXQobGF5b3V0LndpZGdldCk7XG4gICAgfVxuICAgIGlmICghY29udGVudCkge1xuICAgICAgY29udGVudCA9IHRoaXMuX3BsYWNlaG9sZGVyO1xuICAgIH1cbiAgICBjb250ZW50LmFkZENsYXNzKCdqcC1NZXRhZGF0YUZvcm0tY29udGVudCcpO1xuICAgIGxheW91dC53aWRnZXQgPSBjb250ZW50O1xuICB9XG5cbiAgLyoqXG4gICAqIEJ1aWxkIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBidWlsZFdpZGdldChwcm9wczogTWV0YWRhdGFGb3JtLklQcm9wcyk6IHZvaWQge1xuICAgIHRoaXMuX2Zvcm0gPSBuZXcgRm9ybVdpZGdldChwcm9wcyk7XG4gICAgdGhpcy5fZm9ybS5hZGRDbGFzcygnanAtTWV0YWRhdGFGb3JtJyk7XG4gICAgdGhpcy5zZXRDb250ZW50KHRoaXMuX2Zvcm0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwZGF0ZSB0aGUgZm9ybSB3aGVuIHRoZSB3aWRnZXQgaXMgZGlzcGxheWVkLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJTaG93KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIHRoaXMuX3VwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgYWN0aXZlIGNlbGwuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmVDZWxsQ2hhbmdlZChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc1Zpc2libGUpIHRoaXMuX3VwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgYWN0aXZlIGNlbGwgbWV0YWRhdGEuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmVDZWxsTWV0YWRhdGFDaGFuZ2VkKF86IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBpZiAoIXRoaXMuX3VwZGF0aW5nTWV0YWRhdGEgJiYgdGhpcy5pc1Zpc2libGUpIHRoaXMuX3VwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB3aGVuIHRoZSBhY3RpdmUgbm90ZWJvb2sgcGFuZWwgY2hhbmdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2ZU5vdGVib29rUGFuZWxDaGFuZ2VkKF86IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBjb25zdCBub3RlYm9vayA9IHRoaXMubm90ZWJvb2tUb29scy5hY3RpdmVOb3RlYm9va1BhbmVsO1xuICAgIHRoaXMuX25vdGVib29rTW9kZWxOdWxsID0gbm90ZWJvb2sgPT09IG51bGwgfHwgbm90ZWJvb2subW9kZWwgPT09IG51bGw7XG4gICAgaWYgKCF0aGlzLl91cGRhdGluZ01ldGFkYXRhICYmIHRoaXMuaXNWaXNpYmxlKSB0aGlzLl91cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIGFjdGl2ZSBub3RlYm9vayBtZXRhZGF0YS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2ZU5vdGVib29rUGFuZWxNZXRhZGF0YUNoYW5nZWQobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLl91cGRhdGluZ01ldGFkYXRhICYmIHRoaXMuaXNWaXNpYmxlKSB0aGlzLl91cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBVcGRhdGUgdGhlIGZvcm0gd2l0aCBjdXJyZW50IGNlbGwgbWV0YWRhdGEsIGFuZCByZW1vdmUgaW5jb25zaXN0ZW50IGZpZWxkcy5cbiAgICovXG4gIHByaXZhdGUgX3VwZGF0ZSgpOiB2b2lkIHtcbiAgICBjb25zdCBub3RlYm9vayA9IHRoaXMubm90ZWJvb2tUb29scy5hY3RpdmVOb3RlYm9va1BhbmVsO1xuXG4gICAgY29uc3QgY2VsbCA9IHRoaXMubm90ZWJvb2tUb29scy5hY3RpdmVDZWxsO1xuICAgIGlmIChjZWxsID09IHVuZGVmaW5lZCkgcmV0dXJuO1xuXG4gICAgY29uc3QgZm9ybVByb3BlcnRpZXM6IE1ldGFkYXRhRm9ybS5JTWV0YWRhdGFTY2hlbWEgPSBKU09ORXh0LmRlZXBDb3B5KFxuICAgICAgdGhpcy5fbWV0YWRhdGFTY2hlbWFcbiAgICApO1xuXG4gICAgY29uc3QgZm9ybURhdGEgPSB7fSBhcyBKU09OT2JqZWN0O1xuXG4gICAgZm9yIChsZXQgbWV0YWRhdGFLZXkgb2YgT2JqZWN0LmtleXMoXG4gICAgICB0aGlzLl9tZXRhZGF0YVNjaGVtYS5wcm9wZXJ0aWVzIHx8IEpTT05FeHQuZW1wdHlPYmplY3RcbiAgICApKSB7XG4gICAgICAvLyBEbyBub3QgZGlzcGxheSB0aGUgZmllbGQgaWYgaXQncyBOb3RlYm9vayBtZXRhZGF0YSBhbmQgdGhlIG5vdGVib29rIG1vZGVsIGlzIG51bGwuXG4gICAgICBpZiAoXG4gICAgICAgIHRoaXMuX21ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0/LmxldmVsID09PSAnbm90ZWJvb2snICYmXG4gICAgICAgIHRoaXMuX25vdGVib29rTW9kZWxOdWxsXG4gICAgICApIHtcbiAgICAgICAgZGVsZXRlIGZvcm1Qcm9wZXJ0aWVzLnByb3BlcnRpZXMhW21ldGFkYXRhS2V5XTtcbiAgICAgICAgY29udGludWU7XG4gICAgICB9XG5cbiAgICAgIC8vIERvIG5vdCBkaXNwbGF5IHRoZSBmaWVsZCBpZiB0aGUgYWN0aXZlIGNlbGwncyB0eXBlIGlzIG5vdCBpbnZvbHZlZC5cbiAgICAgIGlmIChcbiAgICAgICAgdGhpcy5fbWV0YUluZm9ybWF0aW9uW21ldGFkYXRhS2V5XT8uY2VsbFR5cGVzICYmXG4gICAgICAgICF0aGlzLl9tZXRhSW5mb3JtYXRpb25bbWV0YWRhdGFLZXldPy5jZWxsVHlwZXM/LmluY2x1ZGVzKFxuICAgICAgICAgIGNlbGwubW9kZWwudHlwZVxuICAgICAgICApXG4gICAgICApIHtcbiAgICAgICAgZGVsZXRlIGZvcm1Qcm9wZXJ0aWVzLnByb3BlcnRpZXMhW21ldGFkYXRhS2V5XTtcbiAgICAgICAgY29udGludWU7XG4gICAgICB9XG5cbiAgICAgIGxldCB3b3JraW5nT2JqZWN0OiBQYXJ0aWFsSlNPTk9iamVjdDtcblxuICAgICAgLy8gUmVtb3ZlIHRoZSBmaXJzdCBhbmQgbGFzdCAnLycgaWYgZXhpc3QsIG5hZCBzcGxpdCB0aGUgcGF0aC5cbiAgICAgIGxldCBuZXN0ZWRLZXlzID0gbWV0YWRhdGFLZXlcbiAgICAgICAgLnJlcGxhY2UoL15cXC8rLywgJycpXG4gICAgICAgIC5yZXBsYWNlKC9cXC8rJC8sICcnKVxuICAgICAgICAuc3BsaXQoJy8nKTtcblxuICAgICAgLy8gQXNzb2NpYXRlcyB0aGUgY29ycmVjdCBtZXRhZGF0YSBvYmplY3QgdG8gdGhlIHdvcmtpbmcgb2JqZWN0LlxuICAgICAgaWYgKHRoaXMuX21ldGFJbmZvcm1hdGlvblttZXRhZGF0YUtleV0/LmxldmVsID09PSAnbm90ZWJvb2snKSB7XG4gICAgICAgIHdvcmtpbmdPYmplY3QgPSBub3RlYm9vayEubW9kZWwhLm1ldGFkYXRhO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgd29ya2luZ09iamVjdCA9IGNlbGwubW9kZWwubWV0YWRhdGE7XG4gICAgICB9XG5cbiAgICAgIGxldCBoYXNWYWx1ZSA9IHRydWU7XG5cbiAgICAgIC8vIE5hdmlnYXRlIHRvIHRoZSB2YWx1ZS5cbiAgICAgIGZvciAobGV0IG5lc3RlZCBvZiBuZXN0ZWRLZXlzKSB7XG4gICAgICAgIGlmIChuZXN0ZWQgaW4gd29ya2luZ09iamVjdClcbiAgICAgICAgICB3b3JraW5nT2JqZWN0ID0gd29ya2luZ09iamVjdFtuZXN0ZWRdIGFzIEpTT05PYmplY3Q7XG4gICAgICAgIGVsc2Uge1xuICAgICAgICAgIGhhc1ZhbHVlID0gZmFsc2U7XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgLy8gRmlsbCB0aGUgZm9ybURhdGEgd2l0aCB0aGUgY3VycmVudCBtZXRhZGF0YSB2YWx1ZS5cbiAgICAgIGlmIChoYXNWYWx1ZSkgZm9ybURhdGFbbWV0YWRhdGFLZXldID0gd29ya2luZ09iamVjdCBhcyBKU09OVmFsdWU7XG4gICAgfVxuXG4gICAgdGhpcy5idWlsZFdpZGdldCh7XG4gICAgICBwcm9wZXJ0aWVzOiBmb3JtUHJvcGVydGllcyxcbiAgICAgIHNldHRpbmdzOiBuZXcgQmFzZVNldHRpbmdzKHtcbiAgICAgICAgc2NoZW1hOiB0aGlzLl9tZXRhZGF0YVNjaGVtYSBhcyBQYXJ0aWFsSlNPTk9iamVjdFxuICAgICAgfSksXG4gICAgICB1aVNjaGVtYTogdGhpcy5fdWlTY2hlbWEsXG4gICAgICB0cmFuc2xhdG9yOiB0aGlzLnRyYW5zbGF0b3IgfHwgbnVsbCxcbiAgICAgIGZvcm1EYXRhOiBmb3JtRGF0YSxcbiAgICAgIG1ldGFkYXRhRm9ybVdpZGdldDogdGhpcyxcbiAgICAgIHNob3dNb2RpZmllZDogdGhpcy5fc2hvd01vZGlmaWVkLFxuICAgICAgcGx1Z2luSWQ6IHRoaXMuX3BsdWdpbklkXG4gICAgfSk7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX2Zvcm06IEZvcm1XaWRnZXQgfCB1bmRlZmluZWQ7XG4gIHByaXZhdGUgX21ldGFkYXRhU2NoZW1hOiBNZXRhZGF0YUZvcm0uSU1ldGFkYXRhU2NoZW1hO1xuICBwcml2YXRlIF9tZXRhSW5mb3JtYXRpb246IE1ldGFkYXRhRm9ybS5JTWV0YUluZm9ybWF0aW9uO1xuICBwcml2YXRlIF91aVNjaGVtYTogTWV0YWRhdGFGb3JtLklVaVNjaGVtYTtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9wbGFjZWhvbGRlcjogV2lkZ2V0O1xuICBwcml2YXRlIF91cGRhdGluZ01ldGFkYXRhOiBib29sZWFuO1xuICBwcml2YXRlIF9wbHVnaW5JZDogc3RyaW5nIHwgdW5kZWZpbmVkO1xuICBwcml2YXRlIF9zaG93TW9kaWZpZWQ6IGJvb2xlYW47XG4gIHByaXZhdGUgX25vdGVib29rTW9kZWxOdWxsOiBib29sZWFuID0gZmFsc2U7XG59XG5cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIFRoZSBtZXRhZGF0YSByZXByZXNlbnRhdGlvbiBvYmplY3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNZXRhZGF0YVJlcHJlc2VudGF0aW9uIHtcbiAgICBbbWV0YWRhdGE6IHN0cmluZ106IFBhcnRpYWxKU09OT2JqZWN0IHwgUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZWN1cnNpdmUgZnVuY3Rpb24gdG8gY2xlYW4gdGhlIGVtcHR5IG5lc3RlZCBtZXRhZGF0YSBiZWZvcmUgdXBkYXRpbmcgcmVhbCBtZXRhZGF0YS5cbiAgICogdGhpcyBmdW5jdGlvbiBpcyBjYWxsZWQgd2hlbiBhIG5lc3RlZCBtZXRhZGF0YSBpcyB1bmRlZmluZWQgKG9yIGRlZmF1bHQpLCBzbyBtYXliZSBzb21lXG4gICAqIG9iamVjdCBhcmUgbm93IGVtcHR5LlxuICAgKiBAcGFyYW0gbWV0YWRhdGFPYmplY3Q6IFBhcnRpYWxKU09OT2JqZWN0IHJlcHJlc2VudGluZyB0aGUgbWV0YWRhdGEgdG8gdXBkYXRlLlxuICAgKiBAcGFyYW0gbWV0YWRhdGFLZXlzTGlzdDogQXJyYXk8c3RyaW5nPiBvZiB0aGUgdW5kZWZpbmVkIG5lc3RlZCBtZXRhZGF0YS5cbiAgICogQHJldHVybnMgUGFydGlhbEpTT05PYmplY3Qgd2l0aG91dCBlbXB0eSBvYmplY3QuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZGVsZXRlRW1wdHlOZXN0ZWQoXG4gICAgbWV0YWRhdGFPYmplY3Q6IFBhcnRpYWxKU09OT2JqZWN0LFxuICAgIG1ldGFkYXRhS2V5c0xpc3Q6IEFycmF5PHN0cmluZz5cbiAgKTogUGFydGlhbEpTT05PYmplY3Qge1xuICAgIGxldCBtZXRhZGF0YUtleSA9IG1ldGFkYXRhS2V5c0xpc3Quc2hpZnQoKTtcbiAgICBpZiAobWV0YWRhdGFLZXkgIT09IHVuZGVmaW5lZCAmJiBtZXRhZGF0YUtleSBpbiBtZXRhZGF0YU9iamVjdCkge1xuICAgICAgaWYgKE9iamVjdC5rZXlzKG1ldGFkYXRhT2JqZWN0W21ldGFkYXRhS2V5XSBhcyBQYXJ0aWFsSlNPTk9iamVjdCkubGVuZ3RoKVxuICAgICAgICBtZXRhZGF0YU9iamVjdFttZXRhZGF0YUtleV0gPSBkZWxldGVFbXB0eU5lc3RlZChcbiAgICAgICAgICBtZXRhZGF0YU9iamVjdFttZXRhZGF0YUtleV0gYXMgUGFydGlhbEpTT05PYmplY3QsXG4gICAgICAgICAgbWV0YWRhdGFLZXlzTGlzdFxuICAgICAgICApO1xuICAgICAgaWYgKCFPYmplY3Qua2V5cyhtZXRhZGF0YU9iamVjdFttZXRhZGF0YUtleV0gYXMgUGFydGlhbEpTT05PYmplY3QpLmxlbmd0aClcbiAgICAgICAgZGVsZXRlIG1ldGFkYXRhT2JqZWN0W21ldGFkYXRhS2V5XTtcbiAgICB9XG4gICAgcmV0dXJuIG1ldGFkYXRhT2JqZWN0O1xuICB9XG59XG4iLCIvKlxuICogQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4gKiBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuICovXG5cbmltcG9ydCB7IElNZXRhZGF0YUZvcm1Qcm92aWRlciwgTWV0YWRhdGFGb3JtIH0gZnJvbSAnLi90b2tlbic7XG5cbmV4cG9ydCBjbGFzcyBNZXRhZGF0YUZvcm1Qcm92aWRlciBpbXBsZW1lbnRzIElNZXRhZGF0YUZvcm1Qcm92aWRlciB7XG4gIGFkZChpZDogc3RyaW5nLCB3aWRnZXQ6IE1ldGFkYXRhRm9ybS5JTWV0YWRhdGFGb3JtKSB7XG4gICAgaWYgKCF0aGlzLl9pdGVtc1tpZF0pIHtcbiAgICAgIHRoaXMuX2l0ZW1zW2lkXSA9IHdpZGdldDtcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc29sZS53YXJuKGBBIE1ldGFkYXRhZm9ybVdpZGdldCBpcyBhbHJlYWR5IHJlZ2lzdGVyZWQgd2l0aCBpZCAke2lkfWApO1xuICAgIH1cbiAgfVxuXG4gIGdldChpZDogc3RyaW5nKTogTWV0YWRhdGFGb3JtLklNZXRhZGF0YUZvcm0gfCB1bmRlZmluZWQge1xuICAgIGlmICh0aGlzLl9pdGVtc1tpZF0pIHtcbiAgICAgIHJldHVybiB0aGlzLl9pdGVtc1tpZF07XG4gICAgfSBlbHNlIHtcbiAgICAgIGNvbnNvbGUud2FybihgVGhlcmUgaXMgbm8gTWV0YWRhdGFmb3JtV2lkZ2V0IHJlZ2lzdGVyZWQgd2l0aCBpZCAke2lkfWApO1xuICAgIH1cbiAgfVxuXG4gIF9pdGVtczogeyBbaWQ6IHN0cmluZ106IE1ldGFkYXRhRm9ybS5JTWV0YWRhdGFGb3JtIH0gPSB7fTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG1ldGFkYXRhZm9ybVxuICovXG5cbmltcG9ydCB7IENlbGxUeXBlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgTm90ZWJvb2tUb29scyB9IGZyb20gJ0BqdXB5dGVybGFiL25vdGVib29rJztcbmltcG9ydCB7IEJhc2VTZXR0aW5ncywgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7XG4gIFBhcnRpYWxKU09OT2JqZWN0LFxuICBSZWFkb25seUpTT05PYmplY3QsXG4gIFRva2VuXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1ldGFkYXRhRm9ybVdpZGdldCB9IGZyb20gJy4vbWV0YWRhdGFmb3JtJztcblxuZXhwb3J0IG5hbWVzcGFjZSBNZXRhZGF0YUZvcm0ge1xuICAvKipcbiAgICogVGhlIG1ldGFkYXRhIHNjaGVtYSBhcyBkZWZpbmVkIGluIEpTT04gc2NoZW1hLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgSU1ldGFkYXRhU2NoZW1hID0gSVNldHRpbmdSZWdpc3RyeS5JTWV0YWRhdGFTY2hlbWE7XG5cbiAgLyoqXG4gICAqIFRoZSBtZXRhIGluZm9ybWF0aW9uIGFzc29jaWF0ZWQgdG8gYWxsIHByb3BlcnRpZXMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNZXRhSW5mb3JtYXRpb24ge1xuICAgIFttZXRhZGF0YUtleTogc3RyaW5nXTogSVNpbmdsZU1ldGFJbmZvcm1hdGlvbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbWV0YSBpbmZvcm1hdGlvbiBhc3NvY2lhdGVkIHRvIGEgcHJvcGVydHkuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElTaW5nbGVNZXRhSW5mb3JtYXRpb24ge1xuICAgIC8qKlxuICAgICAqIFRoZSBtZXRhZGF0YSBsZXZlbCwgJ2NlbGwnIG9yICdub3RlYm9vaycuXG4gICAgICovXG4gICAgbGV2ZWw/OiAnY2VsbCcgfCAnbm90ZWJvb2snO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNlbGwgdHlwZXMgdG8gZGlzcGxheSB0aGlzIG1ldGFkYXRhIGZpZWxkLlxuICAgICAqL1xuICAgIGNlbGxUeXBlcz86IENlbGxUeXBlW107XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZGVmYXVsdCB2YWx1ZSBmb3IgdGhpcyBtZXRhZGF0YS5cbiAgICAgKi9cbiAgICBkZWZhdWx0PzogYW55O1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBhdm9pZCB3cml0aW5nIGRlZmF1bHQgdmFsdWUgaW4gbWV0YWRhdGEuXG4gICAgICovXG4gICAgd3JpdGVEZWZhdWx0PzogYm9vbGVhbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBSSlNGIHVpOnNjaGVtYS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVVpU2NoZW1hIHtcbiAgICBbbWV0YWRhdGFLZXk6IHN0cmluZ106IElVaVNjaGVtYU9wdGlvbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBSSlNGIHVpOnNjaGVtYSBvcHRpb25zLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJVWlTY2hlbWFPcHRpb24ge1xuICAgIFtvcHRpb246IHN0cmluZ106IGFueTtcbiAgfVxuXG4gIC8qKlxuICAgKiBPcHRpb25zIHBhc3NlZCB0byBNZXRhZGF0YUZvcm1XaWRnZXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBNZXRhZGF0YVNjaGVtYSBkZWZpbmVkIGZyb20gdGhlIHNldHRpbmdzLlxuICAgICAqL1xuICAgIG1ldGFkYXRhU2NoZW1hOiBJTWV0YWRhdGFTY2hlbWE7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbWV0YSBpbmZvcm1hdGlvbiBhc3NvY2lhdGVkIHRvIGFsbCBwcm9wZXJ0aWVzLlxuICAgICAqL1xuICAgIG1ldGFJbmZvcm1hdGlvbjogSU1ldGFJbmZvcm1hdGlvbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSB1aVNjaGVtYSBidWlsdCB3aGVuIGxvYWRpbmcgc2NoZW1hcy5cbiAgICAgKi9cbiAgICB1aVNjaGVtYT86IElVaVNjaGVtYTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBwbHVnaW4gSUQuXG4gICAgICovXG4gICAgcGx1Z2luSWQ/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUcmFuc2xhdG9yIG9iamVjdC5cbiAgICAgKi9cbiAgICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIHNob3cgdGhlIG1vZGlmaWVkIGZpZWxkIGZyb20gZGVmYXVsdCB2YWx1ZS5cbiAgICAgKi9cbiAgICBzaG93TW9kaWZpZWQ/OiBib29sZWFuO1xuICB9XG5cbiAgLyoqXG4gICAqIFByb3BzIHBhc3NlZCB0byB0aGUgRm9ybVdpZGdldCBjb21wb25lbnQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgLyoqXG4gICAgICogUHJvcGVydGllcyBkZWZpbmVkIGZyb20gdGhlIHNldHRpbmdzLlxuICAgICAqL1xuICAgIHByb3BlcnRpZXM6IElNZXRhZGF0YVNjaGVtYTtcblxuICAgIC8qKlxuICAgICAqIE1ldGEgaW5mb3JtYXRpb24gYXNzb2NpYXRlZCB0byBwcm9wZXJ0aWVzLlxuICAgICAqL1xuICAgIHNldHRpbmdzOiBCYXNlU2V0dGluZ3M7XG5cbiAgICAvKipcbiAgICAgKiBDdXJyZW50IGRhdGEgb2YgdGhlIGZvcm0uXG4gICAgICovXG4gICAgZm9ybURhdGE6IFJlYWRvbmx5SlNPTk9iamVjdDtcblxuICAgIC8qKlxuICAgICAqIFRyYW5zbGF0b3Igb2JqZWN0LlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHBhcmVudCBvYmplY3Qgb2YgdGhlIGZvcm0uXG4gICAgICovXG4gICAgbWV0YWRhdGFGb3JtV2lkZ2V0OiBNZXRhZGF0YUZvcm1XaWRnZXQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdWlTY2hlbWEgYnVpbHQgd2hlbiBsb2FkaW5nIHNjaGVtYXMuXG4gICAgICovXG4gICAgdWlTY2hlbWE6IElVaVNjaGVtYTtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gc2hvdyB0aGUgbW9kaWZpZWQgZmllbGQgZnJvbSBkZWZhdWx0IHZhbHVlLlxuICAgICAqL1xuICAgIHNob3dNb2RpZmllZDogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBwbHVnaW4gSUQuXG4gICAgICovXG4gICAgcGx1Z2luSWQ/OiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogQSBtZXRhZGF0YSBmb3JtIGludGVyZmFjZSBwcm92aWRlZCB3aGVuIHJlZ2lzdGVyaW5nXG4gICAqIHRvIGEgbWV0YWRhdGEgZm9ybSBwcm92aWRlci4gIEFsbG93cyBhbiBvd25lciB3aWRnZXRcbiAgICogdG8gc2V0IHRoZSBtZXRhZGF0YSBmb3JtIGNvbnRlbnQgZm9yIGl0c2VsZi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU1ldGFkYXRhRm9ybSBleHRlbmRzIE5vdGVib29rVG9vbHMuVG9vbCB7XG4gICAgLyoqXG4gICAgICogR2V0IHRoZSBsaXN0IG9mIGV4aXN0aW5nIG1ldGFkYXRhS2V5IChhcnJheSBvZiBzdHJpbmcpLlxuICAgICAqXG4gICAgICogIyMgTk9URTpcbiAgICAgKiBUaGUgbGlzdCBjb250YWlucyBhbHNvIHRoZSBjb25kaXRpb25hbCBmaWVsZHMsIHdoaWNoIGFyZSBub3QgbmVjZXNzYXJ5XG4gICAgICogZGlzcGxheWVkIGFuZCBmaWxsZWQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgbWV0YWRhdGFLZXlzOiBzdHJpbmdbXTtcblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgcHJvcGVydGllcyBvZiBhIE1ldGFkYXRhS2V5LlxuICAgICAqIEBwYXJhbSBtZXRhZGF0YUtleSAtIG1ldGFkYXRhS2V5IChhcnJheSBvZiBzdHJpbmcpLlxuICAgICAqL1xuICAgIGdldFByb3BlcnRpZXMobWV0YWRhdGFLZXk6IHN0cmluZyk6IFBhcnRpYWxKU09OT2JqZWN0IHwgbnVsbDtcblxuICAgIC8qKlxuICAgICAqIFNldCBwcm9wZXJ0aWVzIHRvIGEgbWV0YWRhdGFLZXkuXG4gICAgICogQHBhcmFtIG1ldGFkYXRhS2V5IC0gbWV0YWRhdGFLZXkgKGFycmF5IG9mIHN0cmluZykuXG4gICAgICogQHBhcmFtIHByb3BlcnRpZXMgLSB0aGUgcHJvcGVydGllcyB0byBhZGQgb3IgbW9kaWZ5LlxuICAgICAqL1xuICAgIHNldFByb3BlcnRpZXMobWV0YWRhdGFLZXk6IHN0cmluZywgcHJvcGVydGllczogUGFydGlhbEpTT05PYmplY3QpOiB2b2lkO1xuXG4gICAgLyoqXG4gICAgICogVXBkYXRlIHRoZSBtZXRhZGF0YSBvZiB0aGUgY3VycmVudCBjZWxsIG9yIG5vdGVib29rLlxuICAgICAqXG4gICAgICogQHBhcmFtIGZvcm1EYXRhOiB0aGUgY2VsbCBtZXRhZGF0YSBzZXQgaW4gdGhlIGZvcm0uXG4gICAgICogQHBhcmFtIHJlbG9hZDogd2hldGhlciB0byB1cGRhdGUgdGhlIGZvcm0gYWZ0ZXIgdXBkYXRpbmcgdGhlIG1ldGFkYXRhLlxuICAgICAqXG4gICAgICogIyMgTm90ZXNcbiAgICAgKiBNZXRhZGF0YSBhcmUgdXBkYXRlZCBmcm9tIHJvb3Qgb25seS4gSWYgc29tZSBtZXRhZGF0YSBpcyBuZXN0ZWQsXG4gICAgICogdGhlIHdob2xlIHJvb3Qgb2JqZWN0IG11c3QgYmUgdXBkYXRlZC5cbiAgICAgKiBUaGlzIGZ1bmN0aW9uIGJ1aWxkIGFuIG9iamVjdCB3aXRoIGFsbCB0aGUgcm9vdCBvYmplY3QgdG8gdXBkYXRlXG4gICAgICogaW4gbWV0YWRhdGEgYmVmb3JlIHBlcmZvcm1pbmcgdXBkYXRlLlxuICAgICAqL1xuICAgIHVwZGF0ZU1ldGFkYXRhKGZvcm1EYXRhOiBSZWFkb25seUpTT05PYmplY3QsIHJlbG9hZD86IGJvb2xlYW4pOiB2b2lkO1xuICB9XG59XG5cbi8qKlxuICogQSBwcm92aWRlciBmb3IgbWV0YWRhdGEgZm9ybS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJTWV0YWRhdGFGb3JtUHJvdmlkZXIge1xuICAvKipcbiAgICogQWRkIGEgTWV0YWRhdGFGb3JtV2lkZ2V0IHRvIHRoZSBwcm92aWRlci5cbiAgICovXG4gIGFkZChpZDogc3RyaW5nLCB3aWRnZXQ6IE1ldGFkYXRhRm9ybS5JTWV0YWRhdGFGb3JtKTogdm9pZDtcblxuICAvKipcbiAgICogR2V0IGEgTWV0YWRhdGFGb3JtV2lkZ2V0IGZyb20gaWQuXG4gICAqL1xuICBnZXQoaWQ6IHN0cmluZyk6IE1ldGFkYXRhRm9ybS5JTWV0YWRhdGFGb3JtIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBFYWNoIElEIG11c3QgYmUgZGVzY3JpYmVkIGluIHNjaGVtYS5cbiAgICovXG4gIF9pdGVtczogeyBbaWQ6IHN0cmluZ106IE1ldGFkYXRhRm9ybS5JTWV0YWRhdGFGb3JtIH07XG59XG5cbi8qKlxuICogVGhlIG1ldGFkYXRhIGZvcm0gcHJvdmlkZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJTWV0YWRhdGFGb3JtUHJvdmlkZXIgPSBuZXcgVG9rZW48SU1ldGFkYXRhRm9ybVByb3ZpZGVyPihcbiAgJ0BqdXB5dGVybGFiL21ldGFkYXRhZm9ybTpJTWV0YWRhdGFGb3JtUHJvdmlkZXInLFxuICBgQSBzZXJ2aWNlIHRvIHJlZ2lzdGVyIG5ldyBtZXRhZGF0YSBlZGl0b3Igd2lkZ2V0cy5gXG4pO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9