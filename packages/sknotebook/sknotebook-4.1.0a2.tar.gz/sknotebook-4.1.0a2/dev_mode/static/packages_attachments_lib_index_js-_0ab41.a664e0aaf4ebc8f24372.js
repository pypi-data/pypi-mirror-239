"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_attachments_lib_index_js-_0ab41"],{

/***/ "../packages/attachments/lib/index.js":
/*!********************************************!*\
  !*** ../packages/attachments/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AttachmentsModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.AttachmentsModel),
/* harmony export */   "AttachmentsResolver": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.AttachmentsResolver)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./model */ "../packages/attachments/lib/model.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module attachments
 */



/***/ }),

/***/ "../packages/attachments/lib/model.js":
/*!********************************************!*\
  !*** ../packages/attachments/lib/model.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "AttachmentsModel": () => (/* binding */ AttachmentsModel),
/* harmony export */   "AttachmentsResolver": () => (/* binding */ AttachmentsResolver)
/* harmony export */ });
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/observables */ "webpack/sharing/consume/default/@jupyterlab/observables/@jupyterlab/observables");
/* harmony import */ var _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The default implementation of the IAttachmentsModel.
 */
class AttachmentsModel {
    /**
     * Construct a new observable outputs instance.
     */
    constructor(options) {
        var _a;
        this._map = new _jupyterlab_observables__WEBPACK_IMPORTED_MODULE_0__.ObservableMap();
        this._isDisposed = false;
        this._stateChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._serialized = null;
        this._changeGuard = false;
        this.contentFactory =
            (_a = options.contentFactory) !== null && _a !== void 0 ? _a : AttachmentsModel.defaultContentFactory;
        if (options.values) {
            for (const key of Object.keys(options.values)) {
                if (options.values[key] !== undefined) {
                    this.set(key, options.values[key]);
                }
            }
        }
        this._map.changed.connect(this._onMapChanged, this);
    }
    /**
     * A signal emitted when the model state changes.
     */
    get stateChanged() {
        return this._stateChanged;
    }
    /**
     * A signal emitted when the model changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The keys of the attachments in the model.
     */
    get keys() {
        return this._map.keys();
    }
    /**
     * Get the length of the items in the model.
     */
    get length() {
        return this._map.keys().length;
    }
    /**
     * Test whether the model is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._map.dispose();
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
    }
    /**
     * Whether the specified key is set.
     */
    has(key) {
        return this._map.has(key);
    }
    /**
     * Get an item at the specified key.
     */
    get(key) {
        return this._map.get(key);
    }
    /**
     * Set the value at the specified key.
     */
    set(key, value) {
        // Normalize stream data.
        const item = this._createItem({ value });
        this._map.set(key, item);
    }
    /**
     * Remove the attachment whose name is the specified key
     */
    remove(key) {
        this._map.delete(key);
    }
    /**
     * Clear all of the attachments.
     */
    clear() {
        this._map.values().forEach((item) => {
            item.dispose();
        });
        this._map.clear();
    }
    /**
     * Deserialize the model from JSON.
     *
     * #### Notes
     * This will clear any existing data.
     */
    fromJSON(values) {
        this.clear();
        Object.keys(values).forEach(key => {
            if (values[key] !== undefined) {
                this.set(key, values[key]);
            }
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        const ret = {};
        for (const key of this._map.keys()) {
            ret[key] = this._map.get(key).toJSON();
        }
        return ret;
    }
    /**
     * Create an attachment item and hook up its signals.
     */
    _createItem(options) {
        const factory = this.contentFactory;
        const item = factory.createAttachmentModel(options);
        item.changed.connect(this._onGenericChange, this);
        return item;
    }
    /**
     * Handle a change to the list.
     */
    _onMapChanged(sender, args) {
        if (this._serialized && !this._changeGuard) {
            this._changeGuard = true;
            this._serialized.set(this.toJSON());
            this._changeGuard = false;
        }
        this._changed.emit(args);
        this._stateChanged.emit(void 0);
    }
    /**
     * Handle a change to an item.
     */
    _onGenericChange() {
        this._stateChanged.emit(void 0);
    }
}
/**
 * The namespace for AttachmentsModel class statics.
 */
(function (AttachmentsModel) {
    /**
     * The default implementation of a `IAttachmentsModel.IContentFactory`.
     */
    class ContentFactory {
        /**
         * Create an attachment model.
         */
        createAttachmentModel(options) {
            return new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.AttachmentModel(options);
        }
    }
    AttachmentsModel.ContentFactory = ContentFactory;
    /**
     * The default attachment model factory.
     */
    AttachmentsModel.defaultContentFactory = new ContentFactory();
})(AttachmentsModel || (AttachmentsModel = {}));
/**
 * A resolver for cell attachments 'attachment:filename'.
 *
 * Will resolve to a data: url.
 */
class AttachmentsResolver {
    /**
     * Create an attachments resolver object.
     */
    constructor(options) {
        this._parent = options.parent || null;
        this._model = options.model;
    }
    /**
     * Resolve a relative url to a correct server path.
     */
    async resolveUrl(url) {
        if (this._parent && !url.startsWith('attachment:')) {
            return this._parent.resolveUrl(url);
        }
        return url;
    }
    /**
     * Get the download url of a given absolute server path.
     *
     * #### Notes
     * The returned URL may include a query parameter.
     */
    async getDownloadUrl(path) {
        if (this._parent && !path.startsWith('attachment:')) {
            return this._parent.getDownloadUrl(path);
        }
        // Return a data URL with the data of the url
        const key = path.slice('attachment:'.length);
        const attachment = this._model.get(key);
        if (attachment === undefined) {
            // Resolve with unprocessed path, to show as broken image
            return path;
        }
        const { data } = attachment;
        const mimeType = Object.keys(data)[0];
        // Only support known safe types:
        if (mimeType === undefined ||
            _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.imageRendererFactory.mimeTypes.indexOf(mimeType) === -1) {
            throw new Error(`Cannot render unknown image mime type "${mimeType}".`);
        }
        const dataUrl = `data:${mimeType};base64,${data[mimeType]}`;
        return dataUrl;
    }
    /**
     * Whether the URL should be handled by the resolver
     * or not.
     */
    isLocal(url) {
        var _a, _b, _c;
        if (this._parent && !url.startsWith('attachment:')) {
            return (_c = (_b = (_a = this._parent).isLocal) === null || _b === void 0 ? void 0 : _b.call(_a, url)) !== null && _c !== void 0 ? _c : true;
        }
        return true;
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfYXR0YWNobWVudHNfbGliX2luZGV4X2pzLV8wYWI0MS5hNjY0ZTBhYWY0ZWJjOGYyNDM3Mi5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFFcUI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNUeEIsMENBQTBDO0FBQzFDLDJEQUEyRDtBQU8xQjtBQUtEO0FBR29CO0FBNEdwRDs7R0FFRztBQUNJLE1BQU0sZ0JBQWdCO0lBQzNCOztPQUVHO0lBQ0gsWUFBWSxPQUFtQzs7UUFvS3ZDLFNBQUksR0FBRyxJQUFJLGtFQUFhLEVBQW9CLENBQUM7UUFDN0MsZ0JBQVcsR0FBRyxLQUFLLENBQUM7UUFDcEIsa0JBQWEsR0FBRyxJQUFJLHFEQUFNLENBQTBCLElBQUksQ0FBQyxDQUFDO1FBQzFELGFBQVEsR0FBRyxJQUFJLHFEQUFNLENBQXNDLElBQUksQ0FBQyxDQUFDO1FBQ2pFLGdCQUFXLEdBQTRCLElBQUksQ0FBQztRQUM1QyxpQkFBWSxHQUFHLEtBQUssQ0FBQztRQXhLM0IsSUFBSSxDQUFDLGNBQWM7WUFDakIsYUFBTyxDQUFDLGNBQWMsbUNBQUksZ0JBQWdCLENBQUMscUJBQXFCLENBQUM7UUFDbkUsSUFBSSxPQUFPLENBQUMsTUFBTSxFQUFFO1lBQ2xCLEtBQUssTUFBTSxHQUFHLElBQUksTUFBTSxDQUFDLElBQUksQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLEVBQUU7Z0JBQzdDLElBQUksT0FBTyxDQUFDLE1BQU0sQ0FBQyxHQUFHLENBQUMsS0FBSyxTQUFTLEVBQUU7b0JBQ3JDLElBQUksQ0FBQyxHQUFHLENBQUMsR0FBRyxFQUFFLE9BQU8sQ0FBQyxNQUFNLENBQUMsR0FBRyxDQUFFLENBQUMsQ0FBQztpQkFDckM7YUFDRjtTQUNGO1FBQ0QsSUFBSSxDQUFDLElBQUksQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxhQUFhLEVBQUUsSUFBSSxDQUFDLENBQUM7SUFDdEQs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QUFpQztRQUNqQyxJQUNFLFFBQVEsS0FBSyxTQUFTO1lBQ3RCLDBGQUFzQyxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsQ0FBQyxFQUN2RDtZQUNBLE1BQU0sSUFBSSxLQUFLLENBQUMsMENBQTBDLFFBQVEsSUFBSSxDQUFDLENBQUM7U0FDekU7UUFDRCxNQUFNLE9BQU8sR0FBRyxRQUFRLFFBQVEsV0FBVyxJQUFJLENBQUMsUUFBUSxDQUFDLEVBQUUsQ0FBQztRQUM1RCxPQUFPLE9BQU8sQ0FBQztJQUNqQixDQUFDO0lBRUQ7OztPQUdHO0lBQ0gsT0FBTyxDQUFDLEdBQVc7O1FBQ2pCLElBQUksSUFBSSxDQUFDLE9BQU8sSUFBSSxDQUFDLEdBQUcsQ0FBQyxVQUFVLENBQUMsYUFBYSxDQUFDLEVBQUU7WUFDbEQsT0FBTyxzQkFBSSxDQUFDLE9BQU8sRUFBQyxPQUFPLG1EQUFHLEdBQUcsQ0FBQyxtQ0FBSSxJQUFJLENBQUM7U0FDNUM7UUFDRCxPQUFPLElBQUksQ0FBQztJQUNkLENBQUM7Q0FJRiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9hdHRhY2htZW50cy9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2F0dGFjaG1lbnRzL3NyYy9tb2RlbC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGF0dGFjaG1lbnRzXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9tb2RlbCc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIG5iZm9ybWF0IGZyb20gJ0BqdXB5dGVybGFiL25iZm9ybWF0JztcbmltcG9ydCB7XG4gIElPYnNlcnZhYmxlTWFwLFxuICBJT2JzZXJ2YWJsZVZhbHVlLFxuICBPYnNlcnZhYmxlTWFwXG59IGZyb20gJ0BqdXB5dGVybGFiL29ic2VydmFibGVzJztcbmltcG9ydCB7XG4gIEF0dGFjaG1lbnRNb2RlbCxcbiAgSUF0dGFjaG1lbnRNb2RlbCxcbiAgaW1hZ2VSZW5kZXJlckZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJUmVuZGVyTWltZSB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUtaW50ZXJmYWNlcyc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogVGhlIG1vZGVsIGZvciBhdHRhY2htZW50cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJQXR0YWNobWVudHNNb2RlbCBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbW9kZWwgc3RhdGUgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IHN0YXRlQ2hhbmdlZDogSVNpZ25hbDxJQXR0YWNobWVudHNNb2RlbCwgdm9pZD47XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbW9kZWwgY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IGNoYW5nZWQ6IElTaWduYWw8SUF0dGFjaG1lbnRzTW9kZWwsIElBdHRhY2htZW50c01vZGVsLkNoYW5nZWRBcmdzPjtcblxuICAvKipcbiAgICogVGhlIGxlbmd0aCBvZiB0aGUgaXRlbXMgaW4gdGhlIG1vZGVsLlxuICAgKi9cbiAgcmVhZG9ubHkgbGVuZ3RoOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFRoZSBrZXlzIG9mIHRoZSBhdHRhY2htZW50cyBpbiB0aGUgbW9kZWwuXG4gICAqL1xuICByZWFkb25seSBrZXlzOiBSZWFkb25seUFycmF5PHN0cmluZz47XG5cbiAgLyoqXG4gICAqIFRoZSBhdHRhY2htZW50IGNvbnRlbnQgZmFjdG9yeSB1c2VkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIHJlYWRvbmx5IGNvbnRlbnRGYWN0b3J5OiBJQXR0YWNobWVudHNNb2RlbC5JQ29udGVudEZhY3Rvcnk7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIHNwZWNpZmllZCBrZXkgaXMgc2V0LlxuICAgKi9cbiAgaGFzKGtleTogc3RyaW5nKTogYm9vbGVhbjtcblxuICAvKipcbiAgICogR2V0IGFuIGl0ZW0gZm9yIHRoZSBzcGVjaWZpZWQga2V5LlxuICAgKi9cbiAgZ2V0KGtleTogc3RyaW5nKTogSUF0dGFjaG1lbnRNb2RlbCB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogU2V0IHRoZSB2YWx1ZSBvZiB0aGUgc3BlY2lmaWVkIGtleS5cbiAgICovXG4gIHNldChrZXk6IHN0cmluZywgYXR0YWNobWVudDogbmJmb3JtYXQuSU1pbWVCdW5kbGUpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgdGhlIGF0dGFjaG1lbnQgd2hvc2UgbmFtZSBpcyB0aGUgc3BlY2lmaWVkIGtleS5cbiAgICogTm90ZSB0aGF0IHRoaXMgaXMgb3B0aW9uYWwgb25seSB1bnRpbCBKdXB5dGVybGFiIDIuMCByZWxlYXNlLlxuICAgKi9cbiAgcmVtb3ZlOiAoa2V5OiBzdHJpbmcpID0+IHZvaWQ7XG5cbiAgLyoqXG4gICAqIENsZWFyIGFsbCBvZiB0aGUgYXR0YWNobWVudHMuXG4gICAqL1xuICBjbGVhcigpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBEZXNlcmlhbGl6ZSB0aGUgbW9kZWwgZnJvbSBKU09OLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgd2lsbCBjbGVhciBhbnkgZXhpc3RpbmcgZGF0YS5cbiAgICovXG4gIGZyb21KU09OKHZhbHVlczogbmJmb3JtYXQuSUF0dGFjaG1lbnRzKTogdm9pZDtcblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklBdHRhY2htZW50cztcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBJQXR0YWNobWVudHNNb2RlbCBpbnRlcmZhY2VzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElBdHRhY2htZW50c01vZGVsIHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGEgYXR0YWNobWVudHMgbW9kZWwuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgaW5pdGlhbCB2YWx1ZXMgZm9yIHRoZSBtb2RlbC5cbiAgICAgKi9cbiAgICB2YWx1ZXM/OiBuYmZvcm1hdC5JQXR0YWNobWVudHM7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXR0YWNobWVudCBjb250ZW50IGZhY3RvcnkgdXNlZCBieSB0aGUgbW9kZWwuXG4gICAgICpcbiAgICAgKiBJZiBub3QgZ2l2ZW4sIGEgZGVmYXVsdCBmYWN0b3J5IHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBjb250ZW50RmFjdG9yeT86IElDb250ZW50RmFjdG9yeTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHR5cGUgYWxpYXMgZm9yIGNoYW5nZWQgYXJncy5cbiAgICovXG4gIGV4cG9ydCB0eXBlIENoYW5nZWRBcmdzID0gSU9ic2VydmFibGVNYXAuSUNoYW5nZWRBcmdzPElBdHRhY2htZW50TW9kZWw+O1xuXG4gIC8qKlxuICAgKiBUaGUgaW50ZXJmYWNlIGZvciBhbiBhdHRhY2htZW50IGNvbnRlbnQgZmFjdG9yeS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUNvbnRlbnRGYWN0b3J5IHtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYW4gYXR0YWNobWVudCBtb2RlbC5cbiAgICAgKi9cbiAgICBjcmVhdGVBdHRhY2htZW50TW9kZWwob3B0aW9uczogSUF0dGFjaG1lbnRNb2RlbC5JT3B0aW9ucyk6IElBdHRhY2htZW50TW9kZWw7XG4gIH1cbn1cblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBpbXBsZW1lbnRhdGlvbiBvZiB0aGUgSUF0dGFjaG1lbnRzTW9kZWwuXG4gKi9cbmV4cG9ydCBjbGFzcyBBdHRhY2htZW50c01vZGVsIGltcGxlbWVudHMgSUF0dGFjaG1lbnRzTW9kZWwge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IG9ic2VydmFibGUgb3V0cHV0cyBpbnN0YW5jZS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElBdHRhY2htZW50c01vZGVsLklPcHRpb25zKSB7XG4gICAgdGhpcy5jb250ZW50RmFjdG9yeSA9XG4gICAgICBvcHRpb25zLmNvbnRlbnRGYWN0b3J5ID8/IEF0dGFjaG1lbnRzTW9kZWwuZGVmYXVsdENvbnRlbnRGYWN0b3J5O1xuICAgIGlmIChvcHRpb25zLnZhbHVlcykge1xuICAgICAgZm9yIChjb25zdCBrZXkgb2YgT2JqZWN0LmtleXMob3B0aW9ucy52YWx1ZXMpKSB7XG4gICAgICAgIGlmIChvcHRpb25zLnZhbHVlc1trZXldICE9PSB1bmRlZmluZWQpIHtcbiAgICAgICAgICB0aGlzLnNldChrZXksIG9wdGlvbnMudmFsdWVzW2tleV0hKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH1cbiAgICB0aGlzLl9tYXAuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uTWFwQ2hhbmdlZCwgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBtb2RlbCBzdGF0ZSBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IHN0YXRlQ2hhbmdlZCgpOiBJU2lnbmFsPElBdHRhY2htZW50c01vZGVsLCB2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX3N0YXRlQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIG1vZGVsIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElBdHRhY2htZW50c01vZGVsLkNoYW5nZWRBcmdzPiB7XG4gICAgcmV0dXJuIHRoaXMuX2NoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGtleXMgb2YgdGhlIGF0dGFjaG1lbnRzIGluIHRoZSBtb2RlbC5cbiAgICovXG4gIGdldCBrZXlzKCk6IFJlYWRvbmx5QXJyYXk8c3RyaW5nPiB7XG4gICAgcmV0dXJuIHRoaXMuX21hcC5rZXlzKCk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSBsZW5ndGggb2YgdGhlIGl0ZW1zIGluIHRoZSBtb2RlbC5cbiAgICovXG4gIGdldCBsZW5ndGgoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmtleXMoKS5sZW5ndGg7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGF0dGFjaG1lbnQgY29udGVudCBmYWN0b3J5IHVzZWQgYnkgdGhlIG1vZGVsLlxuICAgKi9cbiAgcmVhZG9ubHkgY29udGVudEZhY3Rvcnk6IElBdHRhY2htZW50c01vZGVsLklDb250ZW50RmFjdG9yeTtcblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSBtb2RlbCBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHJlc291cmNlcyB1c2VkIGJ5IHRoZSBtb2RlbC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICB0aGlzLl9tYXAuZGlzcG9zZSgpO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgc3BlY2lmaWVkIGtleSBpcyBzZXQuXG4gICAqL1xuICBoYXMoa2V5OiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmhhcyhrZXkpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpdGVtIGF0IHRoZSBzcGVjaWZpZWQga2V5LlxuICAgKi9cbiAgZ2V0KGtleTogc3RyaW5nKTogSUF0dGFjaG1lbnRNb2RlbCB8IHVuZGVmaW5lZCB7XG4gICAgcmV0dXJuIHRoaXMuX21hcC5nZXQoa2V5KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQga2V5LlxuICAgKi9cbiAgc2V0KGtleTogc3RyaW5nLCB2YWx1ZTogbmJmb3JtYXQuSU1pbWVCdW5kbGUpOiB2b2lkIHtcbiAgICAvLyBOb3JtYWxpemUgc3RyZWFtIGRhdGEuXG4gICAgY29uc3QgaXRlbSA9IHRoaXMuX2NyZWF0ZUl0ZW0oeyB2YWx1ZSB9KTtcbiAgICB0aGlzLl9tYXAuc2V0KGtleSwgaXRlbSk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIHRoZSBhdHRhY2htZW50IHdob3NlIG5hbWUgaXMgdGhlIHNwZWNpZmllZCBrZXlcbiAgICovXG4gIHJlbW92ZShrZXk6IHN0cmluZyk6IHZvaWQge1xuICAgIHRoaXMuX21hcC5kZWxldGUoa2V5KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciBhbGwgb2YgdGhlIGF0dGFjaG1lbnRzLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZCB7XG4gICAgdGhpcy5fbWFwLnZhbHVlcygpLmZvckVhY2goKGl0ZW06IElBdHRhY2htZW50TW9kZWwpID0+IHtcbiAgICAgIGl0ZW0uZGlzcG9zZSgpO1xuICAgIH0pO1xuICAgIHRoaXMuX21hcC5jbGVhcigpO1xuICB9XG5cbiAgLyoqXG4gICAqIERlc2VyaWFsaXplIHRoZSBtb2RlbCBmcm9tIEpTT04uXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyB3aWxsIGNsZWFyIGFueSBleGlzdGluZyBkYXRhLlxuICAgKi9cbiAgZnJvbUpTT04odmFsdWVzOiBuYmZvcm1hdC5JQXR0YWNobWVudHMpOiB2b2lkIHtcbiAgICB0aGlzLmNsZWFyKCk7XG4gICAgT2JqZWN0LmtleXModmFsdWVzKS5mb3JFYWNoKGtleSA9PiB7XG4gICAgICBpZiAodmFsdWVzW2tleV0gIT09IHVuZGVmaW5lZCkge1xuICAgICAgICB0aGlzLnNldChrZXksIHZhbHVlc1trZXldISk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IG5iZm9ybWF0LklBdHRhY2htZW50cyB7XG4gICAgY29uc3QgcmV0OiBuYmZvcm1hdC5JQXR0YWNobWVudHMgPSB7fTtcbiAgICBmb3IgKGNvbnN0IGtleSBvZiB0aGlzLl9tYXAua2V5cygpKSB7XG4gICAgICByZXRba2V5XSA9IHRoaXMuX21hcC5nZXQoa2V5KSEudG9KU09OKCk7XG4gICAgfVxuICAgIHJldHVybiByZXQ7XG4gIH1cblxuICAvKipcbiAgICogQ3JlYXRlIGFuIGF0dGFjaG1lbnQgaXRlbSBhbmQgaG9vayB1cCBpdHMgc2lnbmFscy5cbiAgICovXG4gIHByaXZhdGUgX2NyZWF0ZUl0ZW0ob3B0aW9uczogSUF0dGFjaG1lbnRNb2RlbC5JT3B0aW9ucyk6IElBdHRhY2htZW50TW9kZWwge1xuICAgIGNvbnN0IGZhY3RvcnkgPSB0aGlzLmNvbnRlbnRGYWN0b3J5O1xuICAgIGNvbnN0IGl0ZW0gPSBmYWN0b3J5LmNyZWF0ZUF0dGFjaG1lbnRNb2RlbChvcHRpb25zKTtcbiAgICBpdGVtLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkdlbmVyaWNDaGFuZ2UsIHRoaXMpO1xuICAgIHJldHVybiBpdGVtO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgbGlzdC5cbiAgICovXG4gIHByaXZhdGUgX29uTWFwQ2hhbmdlZChcbiAgICBzZW5kZXI6IElPYnNlcnZhYmxlTWFwPElBdHRhY2htZW50TW9kZWw+LFxuICAgIGFyZ3M6IElPYnNlcnZhYmxlTWFwLklDaGFuZ2VkQXJnczxJQXR0YWNobWVudE1vZGVsPlxuICApIHtcbiAgICBpZiAodGhpcy5fc2VyaWFsaXplZCAmJiAhdGhpcy5fY2hhbmdlR3VhcmQpIHtcbiAgICAgIHRoaXMuX2NoYW5nZUd1YXJkID0gdHJ1ZTtcbiAgICAgIHRoaXMuX3NlcmlhbGl6ZWQuc2V0KHRoaXMudG9KU09OKCkpO1xuICAgICAgdGhpcy5fY2hhbmdlR3VhcmQgPSBmYWxzZTtcbiAgICB9XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KGFyZ3MpO1xuICAgIHRoaXMuX3N0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGEgY2hhbmdlIHRvIGFuIGl0ZW0uXG4gICAqL1xuICBwcml2YXRlIF9vbkdlbmVyaWNDaGFuZ2UoKTogdm9pZCB7XG4gICAgdGhpcy5fc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgfVxuXG4gIHByaXZhdGUgX21hcCA9IG5ldyBPYnNlcnZhYmxlTWFwPElBdHRhY2htZW50TW9kZWw+KCk7XG4gIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfc3RhdGVDaGFuZ2VkID0gbmV3IFNpZ25hbDxJQXR0YWNobWVudHNNb2RlbCwgdm9pZD4odGhpcyk7XG4gIHByaXZhdGUgX2NoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIElBdHRhY2htZW50c01vZGVsLkNoYW5nZWRBcmdzPih0aGlzKTtcbiAgcHJpdmF0ZSBfc2VyaWFsaXplZDogSU9ic2VydmFibGVWYWx1ZSB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9jaGFuZ2VHdWFyZCA9IGZhbHNlO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIEF0dGFjaG1lbnRzTW9kZWwgY2xhc3Mgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBBdHRhY2htZW50c01vZGVsIHtcbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIGEgYElBdHRhY2htZW50c01vZGVsLklDb250ZW50RmFjdG9yeWAuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgQ29udGVudEZhY3RvcnkgaW1wbGVtZW50cyBJQXR0YWNobWVudHNNb2RlbC5JQ29udGVudEZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhbiBhdHRhY2htZW50IG1vZGVsLlxuICAgICAqL1xuICAgIGNyZWF0ZUF0dGFjaG1lbnRNb2RlbChcbiAgICAgIG9wdGlvbnM6IElBdHRhY2htZW50TW9kZWwuSU9wdGlvbnNcbiAgICApOiBJQXR0YWNobWVudE1vZGVsIHtcbiAgICAgIHJldHVybiBuZXcgQXR0YWNobWVudE1vZGVsKG9wdGlvbnMpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBhdHRhY2htZW50IG1vZGVsIGZhY3RvcnkuXG4gICAqL1xuICBleHBvcnQgY29uc3QgZGVmYXVsdENvbnRlbnRGYWN0b3J5ID0gbmV3IENvbnRlbnRGYWN0b3J5KCk7XG59XG5cbi8qKlxuICogQSByZXNvbHZlciBmb3IgY2VsbCBhdHRhY2htZW50cyAnYXR0YWNobWVudDpmaWxlbmFtZScuXG4gKlxuICogV2lsbCByZXNvbHZlIHRvIGEgZGF0YTogdXJsLlxuICovXG5leHBvcnQgY2xhc3MgQXR0YWNobWVudHNSZXNvbHZlciBpbXBsZW1lbnRzIElSZW5kZXJNaW1lLklSZXNvbHZlciB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYW4gYXR0YWNobWVudHMgcmVzb2x2ZXIgb2JqZWN0LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogQXR0YWNobWVudHNSZXNvbHZlci5JT3B0aW9ucykge1xuICAgIHRoaXMuX3BhcmVudCA9IG9wdGlvbnMucGFyZW50IHx8IG51bGw7XG4gICAgdGhpcy5fbW9kZWwgPSBvcHRpb25zLm1vZGVsO1xuICB9XG4gIC8qKlxuICAgKiBSZXNvbHZlIGEgcmVsYXRpdmUgdXJsIHRvIGEgY29ycmVjdCBzZXJ2ZXIgcGF0aC5cbiAgICovXG4gIGFzeW5jIHJlc29sdmVVcmwodXJsOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz4ge1xuICAgIGlmICh0aGlzLl9wYXJlbnQgJiYgIXVybC5zdGFydHNXaXRoKCdhdHRhY2htZW50OicpKSB7XG4gICAgICByZXR1cm4gdGhpcy5fcGFyZW50LnJlc29sdmVVcmwodXJsKTtcbiAgICB9XG4gICAgcmV0dXJuIHVybDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgdGhlIGRvd25sb2FkIHVybCBvZiBhIGdpdmVuIGFic29sdXRlIHNlcnZlciBwYXRoLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSByZXR1cm5lZCBVUkwgbWF5IGluY2x1ZGUgYSBxdWVyeSBwYXJhbWV0ZXIuXG4gICAqL1xuICBhc3luYyBnZXREb3dubG9hZFVybChwYXRoOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz4ge1xuICAgIGlmICh0aGlzLl9wYXJlbnQgJiYgIXBhdGguc3RhcnRzV2l0aCgnYXR0YWNobWVudDonKSkge1xuICAgICAgcmV0dXJuIHRoaXMuX3BhcmVudC5nZXREb3dubG9hZFVybChwYXRoKTtcbiAgICB9XG4gICAgLy8gUmV0dXJuIGEgZGF0YSBVUkwgd2l0aCB0aGUgZGF0YSBvZiB0aGUgdXJsXG4gICAgY29uc3Qga2V5ID0gcGF0aC5zbGljZSgnYXR0YWNobWVudDonLmxlbmd0aCk7XG4gICAgY29uc3QgYXR0YWNobWVudCA9IHRoaXMuX21vZGVsLmdldChrZXkpO1xuICAgIGlmIChhdHRhY2htZW50ID09PSB1bmRlZmluZWQpIHtcbiAgICAgIC8vIFJlc29sdmUgd2l0aCB1bnByb2Nlc3NlZCBwYXRoLCB0byBzaG93IGFzIGJyb2tlbiBpbWFnZVxuICAgICAgcmV0dXJuIHBhdGg7XG4gICAgfVxuICAgIGNvbnN0IHsgZGF0YSB9ID0gYXR0YWNobWVudDtcbiAgICBjb25zdCBtaW1lVHlwZSA9IE9iamVjdC5rZXlzKGRhdGEpWzBdO1xuICAgIC8vIE9ubHkgc3VwcG9ydCBrbm93biBzYWZlIHR5cGVzOlxuICAgIGlmIChcbiAgICAgIG1pbWVUeXBlID09PSB1bmRlZmluZWQgfHxcbiAgICAgIGltYWdlUmVuZGVyZXJGYWN0b3J5Lm1pbWVUeXBlcy5pbmRleE9mKG1pbWVUeXBlKSA9PT0gLTFcbiAgICApIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgQ2Fubm90IHJlbmRlciB1bmtub3duIGltYWdlIG1pbWUgdHlwZSBcIiR7bWltZVR5cGV9XCIuYCk7XG4gICAgfVxuICAgIGNvbnN0IGRhdGFVcmwgPSBgZGF0YToke21pbWVUeXBlfTtiYXNlNjQsJHtkYXRhW21pbWVUeXBlXX1gO1xuICAgIHJldHVybiBkYXRhVXJsO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIFVSTCBzaG91bGQgYmUgaGFuZGxlZCBieSB0aGUgcmVzb2x2ZXJcbiAgICogb3Igbm90LlxuICAgKi9cbiAgaXNMb2NhbCh1cmw6IHN0cmluZyk6IGJvb2xlYW4ge1xuICAgIGlmICh0aGlzLl9wYXJlbnQgJiYgIXVybC5zdGFydHNXaXRoKCdhdHRhY2htZW50OicpKSB7XG4gICAgICByZXR1cm4gdGhpcy5fcGFyZW50LmlzTG9jYWw/Lih1cmwpID8/IHRydWU7XG4gICAgfVxuICAgIHJldHVybiB0cnVlO1xuICB9XG5cbiAgcHJpdmF0ZSBfbW9kZWw6IElBdHRhY2htZW50c01vZGVsO1xuICBwcml2YXRlIF9wYXJlbnQ6IElSZW5kZXJNaW1lLklSZXNvbHZlciB8IG51bGw7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgYEF0dGFjaG1lbnRzUmVzb2x2ZXJgIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQXR0YWNobWVudHNSZXNvbHZlciB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGNyZWF0ZSBhbiBBdHRhY2htZW50c1Jlc29sdmVyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGF0dGFjaG1lbnRzIG1vZGVsIHRvIHJlc29sdmUgYWdhaW5zdC5cbiAgICAgKi9cbiAgICBtb2RlbDogSUF0dGFjaG1lbnRzTW9kZWw7XG5cbiAgICAvKipcbiAgICAgKiBBIHBhcmVudCByZXNvbHZlciB0byB1c2UgaWYgdGhlIFVSTC9wYXRoIGlzIG5vdCBmb3IgYW4gYXR0YWNobWVudC5cbiAgICAgKi9cbiAgICBwYXJlbnQ/OiBJUmVuZGVyTWltZS5JUmVzb2x2ZXI7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==