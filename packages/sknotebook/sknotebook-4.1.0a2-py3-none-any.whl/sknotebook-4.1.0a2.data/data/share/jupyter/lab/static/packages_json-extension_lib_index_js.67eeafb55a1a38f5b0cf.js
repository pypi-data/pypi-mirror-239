"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_json-extension_lib_index_js"],{

/***/ "../node_modules/react-dom/client.js":
/*!*******************************************!*\
  !*** ../node_modules/react-dom/client.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {



var m = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom/react-dom");
if (false) {} else {
  var i = m.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;
  exports.createRoot = function(c, o) {
    i.usingClientEntryPoint = true;
    try {
      return m.createRoot(c, o);
    } finally {
      i.usingClientEntryPoint = false;
    }
  };
  exports.hydrateRoot = function(c, h, o) {
    i.usingClientEntryPoint = true;
    try {
      return m.hydrateRoot(c, h, o);
    } finally {
      i.usingClientEntryPoint = false;
    }
  };
}


/***/ }),

/***/ "../packages/json-extension/lib/index.js":
/*!***********************************************!*\
  !*** ../packages/json-extension/lib/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MIME_TYPE": () => (/* binding */ MIME_TYPE),
/* harmony export */   "MIME_TYPES_JSONL": () => (/* binding */ MIME_TYPES_JSONL),
/* harmony export */   "RenderedJSON": () => (/* binding */ RenderedJSON),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react_dom_client__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react-dom/client */ "../node_modules/react-dom/client.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module json-extension
 */





/**
 * The CSS class to add to the JSON Widget.
 */
const CSS_CLASS = 'jp-RenderedJSON';
/**
 * The MIME type for JSON.
 */
const MIME_TYPE = 'application/json';
// NOTE: not standardized yet
const MIME_TYPES_JSONL = [
    'text/jsonl',
    'application/jsonl',
    'application/json-lines'
];
/**
 * A renderer for JSON data.
 */
class RenderedJSON extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Create a new widget for rendering JSON.
     */
    constructor(options) {
        super();
        this._rootDOM = null;
        this.addClass(CSS_CLASS);
        this.addClass('CodeMirror');
        this._mimeType = options.mimeType;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    }
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.printWidget(this);
    }
    /**
     * Render JSON into this widget's node.
     */
    async renderModel(model) {
        const { Component } = await Promise.all(/*! import() */[__webpack_require__.e("webpack_sharing_consume_default_lumino_coreutils_lumino_coreutils"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_ui-components_jupyterlab_ui-components"), __webpack_require__.e("webpack_sharing_consume_default_jupyterlab_codemirror_jupyterlab_codemirror"), __webpack_require__.e("webpack_sharing_consume_default_lezer_highlight_lezer_highlight"), __webpack_require__.e("webpack_sharing_consume_default_style-mod_style-mod"), __webpack_require__.e("packages_json-extension_lib_component_js")]).then(__webpack_require__.bind(__webpack_require__, /*! ./component */ "../packages/json-extension/lib/component.js"));
        let data;
        // handle if json-lines format
        if (MIME_TYPES_JSONL.indexOf(this._mimeType) >= 0) {
            // convert into proper json
            const lines = (model.data[this._mimeType] || '')
                .trim()
                .split(/\n/);
            data = JSON.parse(`[${lines.join(',')}]`);
        }
        else {
            data = (model.data[this._mimeType] || {});
        }
        const metadata = (model.metadata[this._mimeType] || {});
        if (this._rootDOM === null) {
            this._rootDOM = (0,react_dom_client__WEBPACK_IMPORTED_MODULE_4__.createRoot)(this.node);
        }
        return new Promise((resolve, reject) => {
            this._rootDOM.render(react__WEBPACK_IMPORTED_MODULE_3__.createElement(Component, { data: data, metadata: metadata, translator: this.translator, forwardedRef: () => resolve() }));
        });
    }
    /**
     * Called before the widget is detached from the DOM.
     */
    onBeforeDetach(msg) {
        // Unmount the component so it can tear down.
        if (this._rootDOM) {
            this._rootDOM.unmount();
            this._rootDOM = null;
        }
    }
}
/**
 * A mime renderer factory for JSON data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [MIME_TYPE, ...MIME_TYPES_JSONL],
    createRenderer: options => new RenderedJSON(options)
};
const extensions = [
    {
        id: '@jupyterlab/json-extension:factory',
        description: 'Adds renderer for JSON content.',
        rendererFactory,
        rank: 0,
        dataType: 'json',
        documentWidgetFactoryOptions: {
            name: 'JSON',
            // TODO: how to translate label of the factory?
            primaryFileType: 'json',
            fileTypes: ['json', 'notebook', 'geojson'],
            defaultFor: ['json']
        }
    },
    {
        id: '@jupyterlab/json-lines-extension:factory',
        description: 'Adds renderer for JSONLines content.',
        rendererFactory,
        rank: 0,
        dataType: 'string',
        documentWidgetFactoryOptions: {
            name: 'JSONLines',
            primaryFileType: 'jsonl',
            fileTypes: ['jsonl', 'ndjson'],
            defaultFor: ['jsonl', 'ndjson']
        }
    }
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extensions);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfanNvbi1leHRlbnNpb25fbGliX2luZGV4X2pzLjY3ZWVhZmI1NWExYTM4ZjViMGNmLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7OztBQUFhOztBQUViLFFBQVEsbUJBQU8sQ0FBQyxzRUFBVztBQUMzQixJQUFJLEtBQXFDLEVBQUUsRUFHMUMsQ0FBQztBQUNGO0FBQ0EsRUFBRSxrQkFBa0I7QUFDcEI7QUFDQTtBQUNBO0FBQ0EsTUFBTTtBQUNOO0FBQ0E7QUFDQTtBQUNBLEVBQUUsbUJBQW1CO0FBQ3JCO0FBQ0E7QUFDQTtBQUNBLE1BQU07QUFDTjtBQUNBO0FBQ0E7QUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ3hCQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUU2QztBQUVzQjtBQUc3QjtBQUNWO0FBQ3FCO0FBRXBEOztHQUVHO0FBQ0gsTUFBTSxTQUFTLEdBQUcsaUJBQWlCLENBQUM7QUFFcEM7O0dBRUc7QUFDSSxNQUFNLFNBQVMsR0FBRyxrQkFBa0IsQ0FBQztBQUM1Qyw2QkFBNkI7QUFDdEIsTUFBTSxnQkFBZ0IsR0FBRztJQUM5QixZQUFZO0lBQ1osbUJBQW1CO0lBQ25CLHdCQUF3QjtDQUN6QixDQUFDO0FBRUY7O0dBRUc7QUFDSSxNQUFNLFlBQ1gsU0FBUSxtREFBTTtJQUdkOztPQUVHO0lBQ0gsWUFBWSxPQUFxQztRQUMvQyxLQUFLLEVBQUUsQ0FBQztRQTJERixhQUFRLEdBQWdCLElBQUksQ0FBQztRQTFEbkMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxTQUFTLENBQUMsQ0FBQztRQUN6QixJQUFJLENBQUMsUUFBUSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQzVCLElBQUksQ0FBQyxTQUFTLEdBQUcsT0FBTyxDQUFDLFFBQVEsQ0FBQztRQUNsQyxJQUFJLENBQUMsVUFBVSxHQUFHLE9BQU8sQ0FBQyxVQUFVLElBQUksbUVBQWMsQ0FBQztJQUN6RCxDQUFDO0lBRUQsQ0FBQyxpRUFBZSxDQUFDO1FBQ2YsT0FB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QVc7WUFDakIsZUFBZSxFQUFFLE9BQU87WUFDeEIsU0FBUyxFQUFFLENBQUMsT0FBTyxFQUFFLFFBQVEsQ0FBQztZQUM5QixVQUFVLEVBQUUsQ0FBQyxPQUFPLEVBQUUsUUFBUSxDQUFDO1NBQ2hDO0tBQ0Y7Q0FDRixDQUFDO0FBRUYsaUVBQWUsVUFBVSxFQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL25vZGVfbW9kdWxlcy9yZWFjdC1kb20vY2xpZW50LmpzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9qc29uLWV4dGVuc2lvbi9zcmMvaW5kZXgudHN4Il0sInNvdXJjZXNDb250ZW50IjpbIid1c2Ugc3RyaWN0JztcblxudmFyIG0gPSByZXF1aXJlKCdyZWFjdC1kb20nKTtcbmlmIChwcm9jZXNzLmVudi5OT0RFX0VOViA9PT0gJ3Byb2R1Y3Rpb24nKSB7XG4gIGV4cG9ydHMuY3JlYXRlUm9vdCA9IG0uY3JlYXRlUm9vdDtcbiAgZXhwb3J0cy5oeWRyYXRlUm9vdCA9IG0uaHlkcmF0ZVJvb3Q7XG59IGVsc2Uge1xuICB2YXIgaSA9IG0uX19TRUNSRVRfSU5URVJOQUxTX0RPX05PVF9VU0VfT1JfWU9VX1dJTExfQkVfRklSRUQ7XG4gIGV4cG9ydHMuY3JlYXRlUm9vdCA9IGZ1bmN0aW9uKGMsIG8pIHtcbiAgICBpLnVzaW5nQ2xpZW50RW50cnlQb2ludCA9IHRydWU7XG4gICAgdHJ5IHtcbiAgICAgIHJldHVybiBtLmNyZWF0ZVJvb3QoYywgbyk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGkudXNpbmdDbGllbnRFbnRyeVBvaW50ID0gZmFsc2U7XG4gICAgfVxuICB9O1xuICBleHBvcnRzLmh5ZHJhdGVSb290ID0gZnVuY3Rpb24oYywgaCwgbykge1xuICAgIGkudXNpbmdDbGllbnRFbnRyeVBvaW50ID0gdHJ1ZTtcbiAgICB0cnkge1xuICAgICAgcmV0dXJuIG0uaHlkcmF0ZVJvb3QoYywgaCwgbyk7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGkudXNpbmdDbGllbnRFbnRyeVBvaW50ID0gZmFsc2U7XG4gICAgfVxuICB9O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUganNvbi1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQgeyBQcmludGluZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IEpTT05PYmplY3QsIEpTT05WYWx1ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHsgY3JlYXRlUm9vdCwgUm9vdCB9IGZyb20gJ3JlYWN0LWRvbS9jbGllbnQnO1xuXG4vKipcbiAqIFRoZSBDU1MgY2xhc3MgdG8gYWRkIHRvIHRoZSBKU09OIFdpZGdldC5cbiAqL1xuY29uc3QgQ1NTX0NMQVNTID0gJ2pwLVJlbmRlcmVkSlNPTic7XG5cbi8qKlxuICogVGhlIE1JTUUgdHlwZSBmb3IgSlNPTi5cbiAqL1xuZXhwb3J0IGNvbnN0IE1JTUVfVFlQRSA9ICdhcHBsaWNhdGlvbi9qc29uJztcbi8vIE5PVEU6IG5vdCBzdGFuZGFyZGl6ZWQgeWV0XG5leHBvcnQgY29uc3QgTUlNRV9UWVBFU19KU09OTCA9IFtcbiAgJ3RleHQvanNvbmwnLFxuICAnYXBwbGljYXRpb24vanNvbmwnLFxuICAnYXBwbGljYXRpb24vanNvbi1saW5lcydcbl07XG5cbi8qKlxuICogQSByZW5kZXJlciBmb3IgSlNPTiBkYXRhLlxuICovXG5leHBvcnQgY2xhc3MgUmVuZGVyZWRKU09OXG4gIGV4dGVuZHMgV2lkZ2V0XG4gIGltcGxlbWVudHMgSVJlbmRlck1pbWUuSVJlbmRlcmVyLCBQcmludGluZy5JUHJpbnRhYmxlXG57XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGZvciByZW5kZXJpbmcgSlNPTi5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElSZW5kZXJNaW1lLklSZW5kZXJlck9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuYWRkQ2xhc3MoQ1NTX0NMQVNTKTtcbiAgICB0aGlzLmFkZENsYXNzKCdDb2RlTWlycm9yJyk7XG4gICAgdGhpcy5fbWltZVR5cGUgPSBvcHRpb25zLm1pbWVUeXBlO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgfVxuXG4gIFtQcmludGluZy5zeW1ib2xdKCkge1xuICAgIHJldHVybiAoKTogUHJvbWlzZTx2b2lkPiA9PiBQcmludGluZy5wcmludFdpZGdldCh0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgSlNPTiBpbnRvIHRoaXMgd2lkZ2V0J3Mgbm9kZS5cbiAgICovXG4gIGFzeW5jIHJlbmRlck1vZGVsKG1vZGVsOiBJUmVuZGVyTWltZS5JTWltZU1vZGVsKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgY29uc3QgeyBDb21wb25lbnQgfSA9IGF3YWl0IGltcG9ydCgnLi9jb21wb25lbnQnKTtcblxuICAgIGxldCBkYXRhOiBOb25OdWxsYWJsZTxKU09OVmFsdWU+O1xuXG4gICAgLy8gaGFuZGxlIGlmIGpzb24tbGluZXMgZm9ybWF0XG4gICAgaWYgKE1JTUVfVFlQRVNfSlNPTkwuaW5kZXhPZih0aGlzLl9taW1lVHlwZSkgPj0gMCkge1xuICAgICAgLy8gY29udmVydCBpbnRvIHByb3BlciBqc29uXG4gICAgICBjb25zdCBsaW5lcyA9ICgobW9kZWwuZGF0YVt0aGlzLl9taW1lVHlwZV0gfHwgJycpIGFzIHN0cmluZylcbiAgICAgICAgLnRyaW0oKVxuICAgICAgICAuc3BsaXQoL1xcbi8pO1xuICAgICAgZGF0YSA9IEpTT04ucGFyc2UoYFske2xpbmVzLmpvaW4oJywnKX1dYCk7XG4gICAgfSBlbHNlIHtcbiAgICAgIGRhdGEgPSAobW9kZWwuZGF0YVt0aGlzLl9taW1lVHlwZV0gfHwge30pIGFzIE5vbk51bGxhYmxlPEpTT05WYWx1ZT47XG4gICAgfVxuXG4gICAgY29uc3QgbWV0YWRhdGEgPSAobW9kZWwubWV0YWRhdGFbdGhpcy5fbWltZVR5cGVdIHx8IHt9KSBhcyBKU09OT2JqZWN0O1xuICAgIGlmICh0aGlzLl9yb290RE9NID09PSBudWxsKSB7XG4gICAgICB0aGlzLl9yb290RE9NID0gY3JlYXRlUm9vdCh0aGlzLm5vZGUpO1xuICAgIH1cbiAgICByZXR1cm4gbmV3IFByb21pc2U8dm9pZD4oKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgdGhpcy5fcm9vdERPTSEucmVuZGVyKFxuICAgICAgICA8Q29tcG9uZW50XG4gICAgICAgICAgZGF0YT17ZGF0YX1cbiAgICAgICAgICBtZXRhZGF0YT17bWV0YWRhdGF9XG4gICAgICAgICAgdHJhbnNsYXRvcj17dGhpcy50cmFuc2xhdG9yfVxuICAgICAgICAgIGZvcndhcmRlZFJlZj17KCkgPT4gcmVzb2x2ZSgpfVxuICAgICAgICAvPlxuICAgICAgKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDYWxsZWQgYmVmb3JlIHRoZSB3aWRnZXQgaXMgZGV0YWNoZWQgZnJvbSB0aGUgRE9NLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQmVmb3JlRGV0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIC8vIFVubW91bnQgdGhlIGNvbXBvbmVudCBzbyBpdCBjYW4gdGVhciBkb3duLlxuICAgIGlmICh0aGlzLl9yb290RE9NKSB7XG4gICAgICB0aGlzLl9yb290RE9NLnVubW91bnQoKTtcbiAgICAgIHRoaXMuX3Jvb3RET00gPSBudWxsO1xuICAgIH1cbiAgfVxuXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICBwcml2YXRlIF9taW1lVHlwZTogc3RyaW5nO1xuICBwcml2YXRlIF9yb290RE9NOiBSb290IHwgbnVsbCA9IG51bGw7XG59XG5cbi8qKlxuICogQSBtaW1lIHJlbmRlcmVyIGZhY3RvcnkgZm9yIEpTT04gZGF0YS5cbiAqL1xuZXhwb3J0IGNvbnN0IHJlbmRlcmVyRmFjdG9yeTogSVJlbmRlck1pbWUuSVJlbmRlcmVyRmFjdG9yeSA9IHtcbiAgc2FmZTogdHJ1ZSxcbiAgbWltZVR5cGVzOiBbTUlNRV9UWVBFLCAuLi5NSU1FX1RZUEVTX0pTT05MXSxcbiAgY3JlYXRlUmVuZGVyZXI6IG9wdGlvbnMgPT4gbmV3IFJlbmRlcmVkSlNPTihvcHRpb25zKVxufTtcblxuY29uc3QgZXh0ZW5zaW9uczogSVJlbmRlck1pbWUuSUV4dGVuc2lvbiB8IElSZW5kZXJNaW1lLklFeHRlbnNpb25bXSA9IFtcbiAge1xuICAgIGlkOiAnQGp1cHl0ZXJsYWIvanNvbi1leHRlbnNpb246ZmFjdG9yeScsXG4gICAgZGVzY3JpcHRpb246ICdBZGRzIHJlbmRlcmVyIGZvciBKU09OIGNvbnRlbnQuJyxcbiAgICByZW5kZXJlckZhY3RvcnksXG4gICAgcmFuazogMCxcbiAgICBkYXRhVHlwZTogJ2pzb24nLFxuICAgIGRvY3VtZW50V2lkZ2V0RmFjdG9yeU9wdGlvbnM6IHtcbiAgICAgIG5hbWU6ICdKU09OJyxcbiAgICAgIC8vIFRPRE86IGhvdyB0byB0cmFuc2xhdGUgbGFiZWwgb2YgdGhlIGZhY3Rvcnk/XG4gICAgICBwcmltYXJ5RmlsZVR5cGU6ICdqc29uJyxcbiAgICAgIGZpbGVUeXBlczogWydqc29uJywgJ25vdGVib29rJywgJ2dlb2pzb24nXSxcbiAgICAgIGRlZmF1bHRGb3I6IFsnanNvbiddXG4gICAgfVxuICB9LFxuICB7XG4gICAgaWQ6ICdAanVweXRlcmxhYi9qc29uLWxpbmVzLWV4dGVuc2lvbjpmYWN0b3J5JyxcbiAgICBkZXNjcmlwdGlvbjogJ0FkZHMgcmVuZGVyZXIgZm9yIEpTT05MaW5lcyBjb250ZW50LicsXG4gICAgcmVuZGVyZXJGYWN0b3J5LFxuICAgIHJhbms6IDAsXG4gICAgZGF0YVR5cGU6ICdzdHJpbmcnLFxuICAgIGRvY3VtZW50V2lkZ2V0RmFjdG9yeU9wdGlvbnM6IHtcbiAgICAgIG5hbWU6ICdKU09OTGluZXMnLFxuICAgICAgcHJpbWFyeUZpbGVUeXBlOiAnanNvbmwnLFxuICAgICAgZmlsZVR5cGVzOiBbJ2pzb25sJywgJ25kanNvbiddLFxuICAgICAgZGVmYXVsdEZvcjogWydqc29ubCcsICduZGpzb24nXVxuICAgIH1cbiAgfVxuXTtcblxuZXhwb3J0IGRlZmF1bHQgZXh0ZW5zaW9ucztcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==