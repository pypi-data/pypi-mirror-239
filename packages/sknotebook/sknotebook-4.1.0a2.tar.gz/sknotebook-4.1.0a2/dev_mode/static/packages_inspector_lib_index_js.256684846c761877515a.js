"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_inspector_lib_index_js"],{

/***/ "../packages/inspector/lib/handler.js":
/*!********************************************!*\
  !*** ../packages/inspector/lib/handler.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InspectionHandler": () => (/* binding */ InspectionHandler)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * An object that handles code inspection.
 */
class InspectionHandler {
    /**
     * Construct a new inspection handler for a widget.
     */
    constructor(options) {
        this._cleared = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._editor = null;
        this._inspected = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._isDisposed = false;
        this._pending = 0;
        this._standby = true;
        this._lastInspectedReply = null;
        this._connector = options.connector;
        this._rendermime = options.rendermime;
        this._debouncer = new _lumino_polling__WEBPACK_IMPORTED_MODULE_3__.Debouncer(this.onEditorChange.bind(this), 250);
    }
    /**
     * A signal emitted when the inspector should clear all items.
     */
    get cleared() {
        return this._cleared;
    }
    /**
     * A signal emitted when the handler is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    /**
     * A signal emitted when an inspector value is generated.
     */
    get inspected() {
        return this._inspected;
    }
    /**
     * The editor widget used by the inspection handler.
     */
    get editor() {
        return this._editor;
    }
    set editor(newValue) {
        if (newValue === this._editor) {
            return;
        }
        // Remove all of our listeners.
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.disconnectReceiver(this);
        const editor = (this._editor = newValue);
        if (editor) {
            // Clear the inspector in preparation for a new editor.
            this._cleared.emit(void 0);
            // Call onEditorChange to cover the case where the user changes
            // the active cell
            this.onEditorChange();
            editor.model.selections.changed.connect(this._onChange, this);
            editor.model.sharedModel.changed.connect(this._onChange, this);
        }
    }
    /**
     * Indicates whether the handler makes API inspection requests or stands by.
     *
     * #### Notes
     * The use case for this attribute is to limit the API traffic when no
     * inspector is visible.
     */
    get standby() {
        return this._standby;
    }
    set standby(value) {
        this._standby = value;
    }
    /**
     * Get whether the inspection handler is disposed.
     *
     * #### Notes
     * This is a read-only property.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources used by the handler.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._debouncer.dispose();
        this._disposed.emit(void 0);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal.clearData(this);
    }
    /**
     * Handle a text changed signal from an editor.
     *
     * #### Notes
     * Update the hints inspector based on a text change.
     */
    onEditorChange(customText) {
        // If the handler is in standby mode, bail.
        if (this._standby) {
            return;
        }
        const editor = this.editor;
        if (!editor) {
            return;
        }
        const text = customText ? customText : editor.model.sharedModel.getSource();
        const position = editor.getCursorPosition();
        const offset = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.Text.jsIndexToCharIndex(editor.getOffsetAt(position), text);
        const update = { content: null };
        const pending = ++this._pending;
        void this._connector
            .fetch({ offset, text })
            .then(reply => {
            // If handler has been disposed or a newer request is pending, bail.
            if (!reply || this.isDisposed || pending !== this._pending) {
                this._lastInspectedReply = null;
                this._inspected.emit(update);
                return;
            }
            const { data } = reply;
            // Do not update if there would be no change.
            if (this._lastInspectedReply &&
                _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(this._lastInspectedReply, data)) {
                return;
            }
            const mimeType = this._rendermime.preferredMimeType(data);
            if (mimeType) {
                const widget = this._rendermime.createRenderer(mimeType);
                const model = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.MimeModel({ data });
                void widget.renderModel(model);
                update.content = widget;
            }
            this._lastInspectedReply = reply.data;
            this._inspected.emit(update);
        })
            .catch(reason => {
            // Since almost all failures are benign, fail silently.
            this._lastInspectedReply = null;
            this._inspected.emit(update);
        });
    }
    /**
     * Handle changes to the editor state, debouncing.
     */
    _onChange() {
        void this._debouncer.invoke();
    }
}


/***/ }),

/***/ "../packages/inspector/lib/index.js":
/*!******************************************!*\
  !*** ../packages/inspector/lib/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IInspector": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_3__.IInspector),
/* harmony export */   "InspectionHandler": () => (/* reexport safe */ _handler__WEBPACK_IMPORTED_MODULE_0__.InspectionHandler),
/* harmony export */   "InspectorPanel": () => (/* reexport safe */ _inspector__WEBPACK_IMPORTED_MODULE_1__.InspectorPanel),
/* harmony export */   "KernelConnector": () => (/* reexport safe */ _kernelconnector__WEBPACK_IMPORTED_MODULE_2__.KernelConnector)
/* harmony export */ });
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./handler */ "../packages/inspector/lib/handler.js");
/* harmony import */ var _inspector__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./inspector */ "../packages/inspector/lib/inspector.js");
/* harmony import */ var _kernelconnector__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./kernelconnector */ "../packages/inspector/lib/kernelconnector.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./tokens */ "../packages/inspector/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module inspector
 */






/***/ }),

/***/ "../packages/inspector/lib/inspector.js":
/*!**********************************************!*\
  !*** ../packages/inspector/lib/inspector.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InspectorPanel": () => (/* binding */ InspectorPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to inspector panels.
 */
const PANEL_CLASS = 'jp-Inspector';
/**
 * The class name added to inspector content.
 */
const CONTENT_CLASS = 'jp-Inspector-content';
/**
 * The class name added to default inspector content.
 */
const DEFAULT_CONTENT_CLASS = 'jp-Inspector-default-content';
/**
 * A panel which contains a set of inspectors.
 */
class InspectorPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel {
    /**
     * Construct an inspector.
     */
    constructor(options = {}) {
        super();
        this._source = null;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        if (options.initialContent instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget) {
            this._content = options.initialContent;
        }
        else if (typeof options.initialContent === 'string') {
            this._content = InspectorPanel._generateContentWidget(`<p>${options.initialContent}</p>`);
        }
        else {
            this._content = InspectorPanel._generateContentWidget('<p>' +
                this._trans.__('Click on a function to see documentation.') +
                '</p>');
        }
        this.addClass(PANEL_CLASS);
        this.layout.addWidget(this._content);
    }
    /**
     * Print in iframe
     */
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Printing.printWidget(this);
    }
    /**
     * The source of events the inspector panel listens for.
     */
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            return;
        }
        // Disconnect old signal handler.
        if (this._source) {
            this._source.standby = true;
            this._source.inspected.disconnect(this.onInspectorUpdate, this);
            this._source.disposed.disconnect(this.onSourceDisposed, this);
        }
        // Reject a source that is already disposed.
        if (source && source.isDisposed) {
            source = null;
        }
        // Update source.
        this._source = source;
        // Connect new signal handler.
        if (this._source) {
            this._source.standby = false;
            this._source.inspected.connect(this.onInspectorUpdate, this);
            this._source.disposed.connect(this.onSourceDisposed, this);
        }
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.source = null;
        super.dispose();
    }
    /**
     * Handle inspector update signals.
     */
    onInspectorUpdate(sender, args) {
        const { content } = args;
        // Update the content of the inspector widget.
        if (!content || content === this._content) {
            return;
        }
        this._content.dispose();
        this._content = content;
        content.addClass(CONTENT_CLASS);
        this.layout.addWidget(content);
    }
    /**
     * Handle source disposed signals.
     */
    onSourceDisposed(sender, args) {
        this.source = null;
    }
    /**
     * Generate content widget from string
     */
    static _generateContentWidget(message) {
        const widget = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget();
        widget.node.innerHTML = message;
        widget.addClass(CONTENT_CLASS);
        widget.addClass(DEFAULT_CONTENT_CLASS);
        return widget;
    }
}


/***/ }),

/***/ "../packages/inspector/lib/kernelconnector.js":
/*!****************************************************!*\
  !*** ../packages/inspector/lib/kernelconnector.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelConnector": () => (/* binding */ KernelConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The default connector for making inspection requests from the Jupyter API.
 */
class KernelConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new kernel connector for inspection requests.
     *
     * @param options - The instantiation options for the kernel connector.
     */
    constructor(options) {
        super();
        this._sessionContext = options.sessionContext;
    }
    /**
     * Fetch inspection requests.
     *
     * @param request - The inspection request text and details.
     */
    fetch(request) {
        var _a;
        const kernel = (_a = this._sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
        if (!kernel) {
            return Promise.reject(new Error('Inspection fetch requires a kernel.'));
        }
        const contents = {
            code: request.text,
            cursor_pos: request.offset,
            detail_level: 1
        };
        return kernel.requestInspect(contents).then(msg => {
            const response = msg.content;
            if (response.status !== 'ok' || !response.found) {
                throw new Error('Inspection fetch failed to return successfully.');
            }
            return { data: response.data, metadata: response.metadata };
        });
    }
}


/***/ }),

/***/ "../packages/inspector/lib/tokens.js":
/*!*******************************************!*\
  !*** ../packages/inspector/lib/tokens.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IInspector": () => (/* binding */ IInspector)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The inspector panel token.
 */
const IInspector = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/inspector:IInspector', `A service for adding contextual help to widgets (visible using "Show Contextual Help" from the Help menu).
  Use this to hook into the contextual help system in your extension.`);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaW5zcGVjdG9yX2xpYl9pbmRleF9qcy4yNTY2ODQ4NDZjNzYxODc3NTE1YS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFHZDtBQUMyQjtBQUVSO0FBRXBCO0FBQ1E7QUFHcEQ7O0dBRUc7QUFDSSxNQUFNLGlCQUFpQjtJQUM1Qjs7T0FFRztJQUNILFlBQVksT0FBbUM7UUErSnZDLGFBQVEsR0FBRyxJQUFJLHFEQUFNLENBQTBCLElBQUksQ0FBQyxDQUFDO1FBTXJELGNBQVMsR0FBRyxJQUFJLHFEQUFNLENBQWEsSUFBSSxDQUFDLENBQUM7UUFDekMsWUFBTyxHQUE4QixJQUFJLENBQUM7UUFDMUMsZUFBVSxHQUFHLElBQUkscURBQU0sQ0FBb0MsSUFBSSxDQUFDLENBQUM7UUFDakUsZ0JBQVcsR0FBRyxLQUFLLENBQUM7UUFDcEIsYUFBUSxHQUFHLENBQUMsQ0FBQztRQUViLGFBQVEsR0FBRyxJQUFJLENBQUM7UUFFaEIsd0JBQW1CLEdBQTRDLElBQUksQ0FBQztRQTVLMUUsSUFBSSxDQUFDLFVBQVUsR0FBRyxPQUFPLENBQUMsU0FBUyxDQUFDO1FBQ3BDLElBQUksQ0FBQyxXQUFXLEdBQUcsT0FBTyxDQUFDLFVBQVUsQ0FBQztRQUN0QyxJQUFJLENBQUMsVUFBVSxHQUFHLElBQUksc0RBQVMsQ0FBQyxJQUFJLENBQUMsY0FBYyxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsRUFBRSxHQUFHLENBQUMsQ0FBQztJQUN2RSxDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLE9BQU87UUFDVCxPQUFPLElBQUksQ0FBQyxRQUFRLENBQUM7SUFDdkIsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxRQUFRO1FBQ1YsT0FBTyxJQUFJLENBQUMsU0FBUyxDQUFDO0lBQ3hCLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksU0FBUztRQUNYLE9BQU8sSUFBSSxDQUFDLFVBQVUsQ0FBQztJQUN6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QUMxREQsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVqQjtBQUkxQzs7R0FFRztBQUNJLE1BQU0sVUFBVSxHQUFHLElBQUksb0RBQUssQ0FDakMsa0NBQWtDLEVBQ2xDO3NFQUNvRSxDQUNyRSxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2luc3BlY3Rvci9zcmMvaGFuZGxlci50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW5zcGVjdG9yL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW5zcGVjdG9yL3NyYy9pbnNwZWN0b3IudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2luc3BlY3Rvci9zcmMva2VybmVsY29ubmVjdG9yLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9pbnNwZWN0b3Ivc3JjL3Rva2Vucy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IENvZGVFZGl0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlZWRpdG9yJztcbmltcG9ydCB7IFRleHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSVJlbmRlck1pbWVSZWdpc3RyeSwgTWltZU1vZGVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBJRGF0YUNvbm5lY3RvciB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXRlZGInO1xuaW1wb3J0IHsgSlNPTkV4dCwgUmVhZG9ubHlKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgRGVib3VuY2VyIH0gZnJvbSAnQGx1bWluby9wb2xsaW5nJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IElJbnNwZWN0b3IgfSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogQW4gb2JqZWN0IHRoYXQgaGFuZGxlcyBjb2RlIGluc3BlY3Rpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBJbnNwZWN0aW9uSGFuZGxlciBpbXBsZW1lbnRzIElEaXNwb3NhYmxlLCBJSW5zcGVjdG9yLklJbnNwZWN0YWJsZSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgaW5zcGVjdGlvbiBoYW5kbGVyIGZvciBhIHdpZGdldC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEluc3BlY3Rpb25IYW5kbGVyLklPcHRpb25zKSB7XG4gICAgdGhpcy5fY29ubmVjdG9yID0gb3B0aW9ucy5jb25uZWN0b3I7XG4gICAgdGhpcy5fcmVuZGVybWltZSA9IG9wdGlvbnMucmVuZGVybWltZTtcbiAgICB0aGlzLl9kZWJvdW5jZXIgPSBuZXcgRGVib3VuY2VyKHRoaXMub25FZGl0b3JDaGFuZ2UuYmluZCh0aGlzKSwgMjUwKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGluc3BlY3RvciBzaG91bGQgY2xlYXIgYWxsIGl0ZW1zLlxuICAgKi9cbiAgZ2V0IGNsZWFyZWQoKTogSVNpZ25hbDxJbnNwZWN0aW9uSGFuZGxlciwgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9jbGVhcmVkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgaGFuZGxlciBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBkaXNwb3NlZCgpOiBJU2lnbmFsPEluc3BlY3Rpb25IYW5kbGVyLCB2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX2Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhbiBpbnNwZWN0b3IgdmFsdWUgaXMgZ2VuZXJhdGVkLlxuICAgKi9cbiAgZ2V0IGluc3BlY3RlZCgpOiBJU2lnbmFsPEluc3BlY3Rpb25IYW5kbGVyLCBJSW5zcGVjdG9yLklJbnNwZWN0b3JVcGRhdGU+IHtcbiAgICByZXR1cm4gdGhpcy5faW5zcGVjdGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBlZGl0b3Igd2lkZ2V0IHVzZWQgYnkgdGhlIGluc3BlY3Rpb24gaGFuZGxlci5cbiAgICovXG4gIGdldCBlZGl0b3IoKTogQ29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX2VkaXRvcjtcbiAgfVxuICBzZXQgZWRpdG9yKG5ld1ZhbHVlOiBDb2RlRWRpdG9yLklFZGl0b3IgfCBudWxsKSB7XG4gICAgaWYgKG5ld1ZhbHVlID09PSB0aGlzLl9lZGl0b3IpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgLy8gUmVtb3ZlIGFsbCBvZiBvdXIgbGlzdGVuZXJzLlxuICAgIFNpZ25hbC5kaXNjb25uZWN0UmVjZWl2ZXIodGhpcyk7XG5cbiAgICBjb25zdCBlZGl0b3IgPSAodGhpcy5fZWRpdG9yID0gbmV3VmFsdWUpO1xuICAgIGlmIChlZGl0b3IpIHtcbiAgICAgIC8vIENsZWFyIHRoZSBpbnNwZWN0b3IgaW4gcHJlcGFyYXRpb24gZm9yIGEgbmV3IGVkaXRvci5cbiAgICAgIHRoaXMuX2NsZWFyZWQuZW1pdCh2b2lkIDApO1xuICAgICAgLy8gQ2FsbCBvbkVkaXRvckNoYW5nZSB0byBjb3ZlciB0aGUgY2FzZSB3aGVyZSB0aGUgdXNlciBjaGFuZ2VzXG4gICAgICAvLyB0aGUgYWN0aXZlIGNlbGxcbiAgICAgIHRoaXMub25FZGl0b3JDaGFuZ2UoKTtcbiAgICAgIGVkaXRvci5tb2RlbC5zZWxlY3Rpb25zLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkNoYW5nZSwgdGhpcyk7XG4gICAgICBlZGl0b3IubW9kZWwuc2hhcmVkTW9kZWwuY2hhbmdlZC5jb25uZWN0KHRoaXMuX29uQ2hhbmdlLCB0aGlzKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogSW5kaWNhdGVzIHdoZXRoZXIgdGhlIGhhbmRsZXIgbWFrZXMgQVBJIGluc3BlY3Rpb24gcmVxdWVzdHMgb3Igc3RhbmRzIGJ5LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSB1c2UgY2FzZSBmb3IgdGhpcyBhdHRyaWJ1dGUgaXMgdG8gbGltaXQgdGhlIEFQSSB0cmFmZmljIHdoZW4gbm9cbiAgICogaW5zcGVjdG9yIGlzIHZpc2libGUuXG4gICAqL1xuICBnZXQgc3RhbmRieSgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fc3RhbmRieTtcbiAgfVxuICBzZXQgc3RhbmRieSh2YWx1ZTogYm9vbGVhbikge1xuICAgIHRoaXMuX3N0YW5kYnkgPSB2YWx1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgd2hldGhlciB0aGUgaW5zcGVjdGlvbiBoYW5kbGVyIGlzIGRpc3Bvc2VkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgaXMgYSByZWFkLW9ubHkgcHJvcGVydHkuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgdXNlZCBieSB0aGUgaGFuZGxlci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICB0aGlzLl9kZWJvdW5jZXIuZGlzcG9zZSgpO1xuICAgIHRoaXMuX2Rpc3Bvc2VkLmVtaXQodm9pZCAwKTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIHRleHQgY2hhbmdlZCBzaWduYWwgZnJvbSBhbiBlZGl0b3IuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVXBkYXRlIHRoZSBoaW50cyBpbnNwZWN0b3IgYmFzZWQgb24gYSB0ZXh0IGNoYW5nZS5cbiAgICovXG4gIG9uRWRpdG9yQ2hhbmdlKGN1c3RvbVRleHQ/OiBzdHJpbmcpOiB2b2lkIHtcbiAgICAvLyBJZiB0aGUgaGFuZGxlciBpcyBpbiBzdGFuZGJ5IG1vZGUsIGJhaWwuXG4gICAgaWYgKHRoaXMuX3N0YW5kYnkpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBlZGl0b3IgPSB0aGlzLmVkaXRvcjtcblxuICAgIGlmICghZWRpdG9yKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IHRleHQgPSBjdXN0b21UZXh0ID8gY3VzdG9tVGV4dCA6IGVkaXRvci5tb2RlbC5zaGFyZWRNb2RlbC5nZXRTb3VyY2UoKTtcbiAgICBjb25zdCBwb3NpdGlvbiA9IGVkaXRvci5nZXRDdXJzb3JQb3NpdGlvbigpO1xuICAgIGNvbnN0IG9mZnNldCA9IFRleHQuanNJbmRleFRvQ2hhckluZGV4KGVkaXRvci5nZXRPZmZzZXRBdChwb3NpdGlvbiksIHRleHQpO1xuICAgIGNvbnN0IHVwZGF0ZTogSUluc3BlY3Rvci5JSW5zcGVjdG9yVXBkYXRlID0geyBjb250ZW50OiBudWxsIH07XG5cbiAgICBjb25zdCBwZW5kaW5nID0gKyt0aGlzLl9wZW5kaW5nO1xuXG4gICAgdm9pZCB0aGlzLl9jb25uZWN0b3JcbiAgICAgIC5mZXRjaCh7IG9mZnNldCwgdGV4dCB9KVxuICAgICAgLnRoZW4ocmVwbHkgPT4ge1xuICAgICAgICAvLyBJZiBoYW5kbGVyIGhhcyBiZWVuIGRpc3Bvc2VkIG9yIGEgbmV3ZXIgcmVxdWVzdCBpcyBwZW5kaW5nLCBiYWlsLlxuICAgICAgICBpZiAoIXJlcGx5IHx8IHRoaXMuaXNEaXNwb3NlZCB8fCBwZW5kaW5nICE9PSB0aGlzLl9wZW5kaW5nKSB7XG4gICAgICAgICAgdGhpcy5fbGFzdEluc3BlY3RlZFJlcGx5ID0gbnVsbDtcbiAgICAgICAgICB0aGlzLl9pbnNwZWN0ZWQuZW1pdCh1cGRhdGUpO1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IHsgZGF0YSB9ID0gcmVwbHk7XG5cbiAgICAgICAgLy8gRG8gbm90IHVwZGF0ZSBpZiB0aGVyZSB3b3VsZCBiZSBubyBjaGFuZ2UuXG4gICAgICAgIGlmIChcbiAgICAgICAgICB0aGlzLl9sYXN0SW5zcGVjdGVkUmVwbHkgJiZcbiAgICAgICAgICBKU09ORXh0LmRlZXBFcXVhbCh0aGlzLl9sYXN0SW5zcGVjdGVkUmVwbHksIGRhdGEpXG4gICAgICAgICkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IG1pbWVUeXBlID0gdGhpcy5fcmVuZGVybWltZS5wcmVmZXJyZWRNaW1lVHlwZShkYXRhKTtcbiAgICAgICAgaWYgKG1pbWVUeXBlKSB7XG4gICAgICAgICAgY29uc3Qgd2lkZ2V0ID0gdGhpcy5fcmVuZGVybWltZS5jcmVhdGVSZW5kZXJlcihtaW1lVHlwZSk7XG4gICAgICAgICAgY29uc3QgbW9kZWwgPSBuZXcgTWltZU1vZGVsKHsgZGF0YSB9KTtcblxuICAgICAgICAgIHZvaWQgd2lkZ2V0LnJlbmRlck1vZGVsKG1vZGVsKTtcbiAgICAgICAgICB1cGRhdGUuY29udGVudCA9IHdpZGdldDtcbiAgICAgICAgfVxuXG4gICAgICAgIHRoaXMuX2xhc3RJbnNwZWN0ZWRSZXBseSA9IHJlcGx5LmRhdGE7XG4gICAgICAgIHRoaXMuX2luc3BlY3RlZC5lbWl0KHVwZGF0ZSk7XG4gICAgICB9KVxuICAgICAgLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgIC8vIFNpbmNlIGFsbW9zdCBhbGwgZmFpbHVyZXMgYXJlIGJlbmlnbiwgZmFpbCBzaWxlbnRseS5cbiAgICAgICAgdGhpcy5fbGFzdEluc3BlY3RlZFJlcGx5ID0gbnVsbDtcbiAgICAgICAgdGhpcy5faW5zcGVjdGVkLmVtaXQodXBkYXRlKTtcbiAgICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBjaGFuZ2VzIHRvIHRoZSBlZGl0b3Igc3RhdGUsIGRlYm91bmNpbmcuXG4gICAqL1xuICBwcml2YXRlIF9vbkNoYW5nZSgpOiB2b2lkIHtcbiAgICB2b2lkIHRoaXMuX2RlYm91bmNlci5pbnZva2UoKTtcbiAgfVxuXG4gIHByaXZhdGUgX2NsZWFyZWQgPSBuZXcgU2lnbmFsPEluc3BlY3Rpb25IYW5kbGVyLCB2b2lkPih0aGlzKTtcbiAgcHJpdmF0ZSBfY29ubmVjdG9yOiBJRGF0YUNvbm5lY3RvcjxcbiAgICBJbnNwZWN0aW9uSGFuZGxlci5JUmVwbHksXG4gICAgdm9pZCxcbiAgICBJbnNwZWN0aW9uSGFuZGxlci5JUmVxdWVzdFxuICA+O1xuICBwcml2YXRlIF9kaXNwb3NlZCA9IG5ldyBTaWduYWw8dGhpcywgdm9pZD4odGhpcyk7XG4gIHByaXZhdGUgX2VkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yIHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX2luc3BlY3RlZCA9IG5ldyBTaWduYWw8dGhpcywgSUluc3BlY3Rvci5JSW5zcGVjdG9yVXBkYXRlPih0aGlzKTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9wZW5kaW5nID0gMDtcbiAgcHJpdmF0ZSBfcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbiAgcHJpdmF0ZSBfc3RhbmRieSA9IHRydWU7XG4gIHByaXZhdGUgX2RlYm91bmNlcjogRGVib3VuY2VyO1xuICBwcml2YXRlIF9sYXN0SW5zcGVjdGVkUmVwbHk6IEluc3BlY3Rpb25IYW5kbGVyLklSZXBseVsnZGF0YSddIHwgbnVsbCA9IG51bGw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGluc3BlY3Rpb24gaGFuZGxlciBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIEluc3BlY3Rpb25IYW5kbGVyIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGFuIGluc3BlY3Rpb24gaGFuZGxlci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBjb25uZWN0b3IgdXNlZCB0byBtYWtlIGluc3BlY3Rpb24gcmVxdWVzdHMuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhlIG9ubHkgbWV0aG9kIG9mIHRoaXMgY29ubmVjdG9yIHRoYXQgd2lsbCBldmVyIGJlIGNhbGxlZCBpcyBgZmV0Y2hgLCBzb1xuICAgICAqIGl0IGlzIGFjY2VwdGFibGUgZm9yIHRoZSBvdGhlciBtZXRob2RzIHRvIGJlIHNpbXBsZSBmdW5jdGlvbnMgdGhhdCByZXR1cm5cbiAgICAgKiByZWplY3RlZCBwcm9taXNlcy5cbiAgICAgKi9cbiAgICBjb25uZWN0b3I6IElEYXRhQ29ubmVjdG9yPElSZXBseSwgdm9pZCwgSVJlcXVlc3Q+O1xuXG4gICAgLyoqXG4gICAgICogVGhlIG1pbWUgcmVuZGVyZXIgZm9yIHRoZSBpbnNwZWN0aW9uIGhhbmRsZXIuXG4gICAgICovXG4gICAgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHJlcGx5IHRvIGFuIGluc3BlY3Rpb24gcmVxdWVzdC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVJlcGx5IHtcbiAgICAvKipcbiAgICAgKiBUaGUgTUlNRSBidW5kbGUgZGF0YSByZXR1cm5lZCBmcm9tIGFuIGluc3BlY3Rpb24gcmVxdWVzdC5cbiAgICAgKi9cbiAgICBkYXRhOiBSZWFkb25seUpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBBbnkgbWV0YWRhdGEgdGhhdCBhY2NvbXBhbmllcyB0aGUgTUlNRSBidW5kbGUgcmV0dXJuaW5nIGZyb20gYSByZXF1ZXN0LlxuICAgICAqL1xuICAgIG1ldGFkYXRhOiBSZWFkb25seUpTT05PYmplY3Q7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRldGFpbHMgb2YgYW4gaW5zcGVjdGlvbiByZXF1ZXN0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUmVxdWVzdCB7XG4gICAgLyoqXG4gICAgICogVGhlIGN1cnNvciBvZmZzZXQgcG9zaXRpb24gd2l0aGluIHRoZSB0ZXh0IGJlaW5nIGluc3BlY3RlZC5cbiAgICAgKi9cbiAgICBvZmZzZXQ6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSB0ZXh0IGJlaW5nIGluc3BlY3RlZC5cbiAgICAgKi9cbiAgICB0ZXh0OiBzdHJpbmc7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGluc3BlY3RvclxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vaGFuZGxlcic7XG5leHBvcnQgKiBmcm9tICcuL2luc3BlY3Rvcic7XG5leHBvcnQgKiBmcm9tICcuL2tlcm5lbGNvbm5lY3Rvcic7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFByaW50aW5nIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgSVRyYW5zbGF0b3IsXG4gIG51bGxUcmFuc2xhdG9yLFxuICBUcmFuc2xhdGlvbkJ1bmRsZVxufSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBQYW5lbCwgUGFuZWxMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBJSW5zcGVjdG9yIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGluc3BlY3RvciBwYW5lbHMuXG4gKi9cbmNvbnN0IFBBTkVMX0NMQVNTID0gJ2pwLUluc3BlY3Rvcic7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gaW5zcGVjdG9yIGNvbnRlbnQuXG4gKi9cbmNvbnN0IENPTlRFTlRfQ0xBU1MgPSAnanAtSW5zcGVjdG9yLWNvbnRlbnQnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGRlZmF1bHQgaW5zcGVjdG9yIGNvbnRlbnQuXG4gKi9cbmNvbnN0IERFRkFVTFRfQ09OVEVOVF9DTEFTUyA9ICdqcC1JbnNwZWN0b3ItZGVmYXVsdC1jb250ZW50JztcblxuLyoqXG4gKiBBIHBhbmVsIHdoaWNoIGNvbnRhaW5zIGEgc2V0IG9mIGluc3BlY3RvcnMuXG4gKi9cbmV4cG9ydCBjbGFzcyBJbnNwZWN0b3JQYW5lbFxuICBleHRlbmRzIFBhbmVsXG4gIGltcGxlbWVudHMgSUluc3BlY3RvciwgUHJpbnRpbmcuSVByaW50YWJsZVxue1xuICAvKipcbiAgICogQ29uc3RydWN0IGFuIGluc3BlY3Rvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEluc3BlY3RvclBhbmVsLklPcHRpb25zID0ge30pIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMudHJhbnNsYXRvciA9IG9wdGlvbnMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICBpZiAob3B0aW9ucy5pbml0aWFsQ29udGVudCBpbnN0YW5jZW9mIFdpZGdldCkge1xuICAgICAgdGhpcy5fY29udGVudCA9IG9wdGlvbnMuaW5pdGlhbENvbnRlbnQ7XG4gICAgfSBlbHNlIGlmICh0eXBlb2Ygb3B0aW9ucy5pbml0aWFsQ29udGVudCA9PT0gJ3N0cmluZycpIHtcbiAgICAgIHRoaXMuX2NvbnRlbnQgPSBJbnNwZWN0b3JQYW5lbC5fZ2VuZXJhdGVDb250ZW50V2lkZ2V0KFxuICAgICAgICBgPHA+JHtvcHRpb25zLmluaXRpYWxDb250ZW50fTwvcD5gXG4gICAgICApO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9jb250ZW50ID0gSW5zcGVjdG9yUGFuZWwuX2dlbmVyYXRlQ29udGVudFdpZGdldChcbiAgICAgICAgJzxwPicgK1xuICAgICAgICAgIHRoaXMuX3RyYW5zLl9fKCdDbGljayBvbiBhIGZ1bmN0aW9uIHRvIHNlZSBkb2N1bWVudGF0aW9uLicpICtcbiAgICAgICAgICAnPC9wPidcbiAgICAgICk7XG4gICAgfVxuXG4gICAgdGhpcy5hZGRDbGFzcyhQQU5FTF9DTEFTUyk7XG4gICAgKHRoaXMubGF5b3V0IGFzIFBhbmVsTGF5b3V0KS5hZGRXaWRnZXQodGhpcy5fY29udGVudCk7XG4gIH1cblxuICAvKipcbiAgICogUHJpbnQgaW4gaWZyYW1lXG4gICAqL1xuICBbUHJpbnRpbmcuc3ltYm9sXSgpIHtcbiAgICByZXR1cm4gKCk6IFByb21pc2U8dm9pZD4gPT4gUHJpbnRpbmcucHJpbnRXaWRnZXQodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNvdXJjZSBvZiBldmVudHMgdGhlIGluc3BlY3RvciBwYW5lbCBsaXN0ZW5zIGZvci5cbiAgICovXG4gIGdldCBzb3VyY2UoKTogSUluc3BlY3Rvci5JSW5zcGVjdGFibGUgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fc291cmNlO1xuICB9XG4gIHNldCBzb3VyY2Uoc291cmNlOiBJSW5zcGVjdG9yLklJbnNwZWN0YWJsZSB8IG51bGwpIHtcbiAgICBpZiAodGhpcy5fc291cmNlID09PSBzb3VyY2UpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBEaXNjb25uZWN0IG9sZCBzaWduYWwgaGFuZGxlci5cbiAgICBpZiAodGhpcy5fc291cmNlKSB7XG4gICAgICB0aGlzLl9zb3VyY2Uuc3RhbmRieSA9IHRydWU7XG4gICAgICB0aGlzLl9zb3VyY2UuaW5zcGVjdGVkLmRpc2Nvbm5lY3QodGhpcy5vbkluc3BlY3RvclVwZGF0ZSwgdGhpcyk7XG4gICAgICB0aGlzLl9zb3VyY2UuZGlzcG9zZWQuZGlzY29ubmVjdCh0aGlzLm9uU291cmNlRGlzcG9zZWQsIHRoaXMpO1xuICAgIH1cblxuICAgIC8vIFJlamVjdCBhIHNvdXJjZSB0aGF0IGlzIGFscmVhZHkgZGlzcG9zZWQuXG4gICAgaWYgKHNvdXJjZSAmJiBzb3VyY2UuaXNEaXNwb3NlZCkge1xuICAgICAgc291cmNlID0gbnVsbDtcbiAgICB9XG5cbiAgICAvLyBVcGRhdGUgc291cmNlLlxuICAgIHRoaXMuX3NvdXJjZSA9IHNvdXJjZTtcblxuICAgIC8vIENvbm5lY3QgbmV3IHNpZ25hbCBoYW5kbGVyLlxuICAgIGlmICh0aGlzLl9zb3VyY2UpIHtcbiAgICAgIHRoaXMuX3NvdXJjZS5zdGFuZGJ5ID0gZmFsc2U7XG4gICAgICB0aGlzLl9zb3VyY2UuaW5zcGVjdGVkLmNvbm5lY3QodGhpcy5vbkluc3BlY3RvclVwZGF0ZSwgdGhpcyk7XG4gICAgICB0aGlzLl9zb3VyY2UuZGlzcG9zZWQuY29ubmVjdCh0aGlzLm9uU291cmNlRGlzcG9zZWQsIHRoaXMpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuc291cmNlID0gbnVsbDtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGluc3BlY3RvciB1cGRhdGUgc2lnbmFscy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkluc3BlY3RvclVwZGF0ZShcbiAgICBzZW5kZXI6IGFueSxcbiAgICBhcmdzOiBJSW5zcGVjdG9yLklJbnNwZWN0b3JVcGRhdGVcbiAgKTogdm9pZCB7XG4gICAgY29uc3QgeyBjb250ZW50IH0gPSBhcmdzO1xuXG4gICAgLy8gVXBkYXRlIHRoZSBjb250ZW50IG9mIHRoZSBpbnNwZWN0b3Igd2lkZ2V0LlxuICAgIGlmICghY29udGVudCB8fCBjb250ZW50ID09PSB0aGlzLl9jb250ZW50KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2NvbnRlbnQuZGlzcG9zZSgpO1xuXG4gICAgdGhpcy5fY29udGVudCA9IGNvbnRlbnQ7XG4gICAgY29udGVudC5hZGRDbGFzcyhDT05URU5UX0NMQVNTKTtcbiAgICAodGhpcy5sYXlvdXQgYXMgUGFuZWxMYXlvdXQpLmFkZFdpZGdldChjb250ZW50KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgc291cmNlIGRpc3Bvc2VkIHNpZ25hbHMuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25Tb3VyY2VEaXNwb3NlZChzZW5kZXI6IGFueSwgYXJnczogdm9pZCk6IHZvaWQge1xuICAgIHRoaXMuc291cmNlID0gbnVsbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZW5lcmF0ZSBjb250ZW50IHdpZGdldCBmcm9tIHN0cmluZ1xuICAgKi9cbiAgcHJpdmF0ZSBzdGF0aWMgX2dlbmVyYXRlQ29udGVudFdpZGdldChtZXNzYWdlOiBzdHJpbmcpOiBXaWRnZXQge1xuICAgIGNvbnN0IHdpZGdldCA9IG5ldyBXaWRnZXQoKTtcbiAgICB3aWRnZXQubm9kZS5pbm5lckhUTUwgPSBtZXNzYWdlO1xuICAgIHdpZGdldC5hZGRDbGFzcyhDT05URU5UX0NMQVNTKTtcbiAgICB3aWRnZXQuYWRkQ2xhc3MoREVGQVVMVF9DT05URU5UX0NMQVNTKTtcblxuICAgIHJldHVybiB3aWRnZXQ7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfY29udGVudDogV2lkZ2V0O1xuICBwcml2YXRlIF9zb3VyY2U6IElJbnNwZWN0b3IuSUluc3BlY3RhYmxlIHwgbnVsbCA9IG51bGw7XG59XG5cbmV4cG9ydCBuYW1lc3BhY2UgSW5zcGVjdG9yUGFuZWwge1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICBpbml0aWFsQ29udGVudD86IFdpZGdldCB8IHN0cmluZyB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2Vzc2lvbkNvbnRleHQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBLZXJuZWxNZXNzYWdlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgRGF0YUNvbm5lY3RvciB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXRlZGInO1xuaW1wb3J0IHsgSW5zcGVjdGlvbkhhbmRsZXIgfSBmcm9tICcuL2hhbmRsZXInO1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGNvbm5lY3RvciBmb3IgbWFraW5nIGluc3BlY3Rpb24gcmVxdWVzdHMgZnJvbSB0aGUgSnVweXRlciBBUEkuXG4gKi9cbmV4cG9ydCBjbGFzcyBLZXJuZWxDb25uZWN0b3IgZXh0ZW5kcyBEYXRhQ29ubmVjdG9yPFxuICBJbnNwZWN0aW9uSGFuZGxlci5JUmVwbHksXG4gIHZvaWQsXG4gIEluc3BlY3Rpb25IYW5kbGVyLklSZXF1ZXN0XG4+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyBrZXJuZWwgY29ubmVjdG9yIGZvciBpbnNwZWN0aW9uIHJlcXVlc3RzLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIHRoZSBrZXJuZWwgY29ubmVjdG9yLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogS2VybmVsQ29ubmVjdG9yLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9zZXNzaW9uQ29udGV4dCA9IG9wdGlvbnMuc2Vzc2lvbkNvbnRleHQ7XG4gIH1cblxuICAvKipcbiAgICogRmV0Y2ggaW5zcGVjdGlvbiByZXF1ZXN0cy5cbiAgICpcbiAgICogQHBhcmFtIHJlcXVlc3QgLSBUaGUgaW5zcGVjdGlvbiByZXF1ZXN0IHRleHQgYW5kIGRldGFpbHMuXG4gICAqL1xuICBmZXRjaChcbiAgICByZXF1ZXN0OiBJbnNwZWN0aW9uSGFuZGxlci5JUmVxdWVzdFxuICApOiBQcm9taXNlPEluc3BlY3Rpb25IYW5kbGVyLklSZXBseT4ge1xuICAgIGNvbnN0IGtlcm5lbCA9IHRoaXMuX3Nlc3Npb25Db250ZXh0LnNlc3Npb24/Lmtlcm5lbDtcblxuICAgIGlmICgha2VybmVsKSB7XG4gICAgICByZXR1cm4gUHJvbWlzZS5yZWplY3QobmV3IEVycm9yKCdJbnNwZWN0aW9uIGZldGNoIHJlcXVpcmVzIGEga2VybmVsLicpKTtcbiAgICB9XG5cbiAgICBjb25zdCBjb250ZW50czogS2VybmVsTWVzc2FnZS5JSW5zcGVjdFJlcXVlc3RNc2dbJ2NvbnRlbnQnXSA9IHtcbiAgICAgIGNvZGU6IHJlcXVlc3QudGV4dCxcbiAgICAgIGN1cnNvcl9wb3M6IHJlcXVlc3Qub2Zmc2V0LFxuICAgICAgZGV0YWlsX2xldmVsOiAxXG4gICAgfTtcblxuICAgIHJldHVybiBrZXJuZWwucmVxdWVzdEluc3BlY3QoY29udGVudHMpLnRoZW4obXNnID0+IHtcbiAgICAgIGNvbnN0IHJlc3BvbnNlID0gbXNnLmNvbnRlbnQ7XG5cbiAgICAgIGlmIChyZXNwb25zZS5zdGF0dXMgIT09ICdvaycgfHwgIXJlc3BvbnNlLmZvdW5kKSB7XG4gICAgICAgIHRocm93IG5ldyBFcnJvcignSW5zcGVjdGlvbiBmZXRjaCBmYWlsZWQgdG8gcmV0dXJuIHN1Y2Nlc3NmdWxseS4nKTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHsgZGF0YTogcmVzcG9uc2UuZGF0YSwgbWV0YWRhdGE6IHJlc3BvbnNlLm1ldGFkYXRhIH07XG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9zZXNzaW9uQ29udGV4dDogSVNlc3Npb25Db250ZXh0O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBrZXJuZWwgY29ubmVjdG9yIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgS2VybmVsQ29ubmVjdG9yIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGFuIGluc3BlY3Rpb24gaGFuZGxlci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBzZXNzaW9uIGNvbnRleHQgdXNlZCB0byBtYWtlIEFQSSByZXF1ZXN0cyB0byB0aGUga2VybmVsLlxuICAgICAqL1xuICAgIHNlc3Npb25Db250ZXh0OiBJU2Vzc2lvbkNvbnRleHQ7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgaW5zcGVjdG9yIHBhbmVsIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSUluc3BlY3RvciA9IG5ldyBUb2tlbjxJSW5zcGVjdG9yPihcbiAgJ0BqdXB5dGVybGFiL2luc3BlY3RvcjpJSW5zcGVjdG9yJyxcbiAgYEEgc2VydmljZSBmb3IgYWRkaW5nIGNvbnRleHR1YWwgaGVscCB0byB3aWRnZXRzICh2aXNpYmxlIHVzaW5nIFwiU2hvdyBDb250ZXh0dWFsIEhlbHBcIiBmcm9tIHRoZSBIZWxwIG1lbnUpLlxuICBVc2UgdGhpcyB0byBob29rIGludG8gdGhlIGNvbnRleHR1YWwgaGVscCBzeXN0ZW0gaW4geW91ciBleHRlbnNpb24uYFxuKTtcblxuLyoqXG4gKiBBbiBpbnRlcmZhY2UgZm9yIGFuIGluc3BlY3Rvci5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJSW5zcGVjdG9yIHtcbiAgLyoqXG4gICAqIFRoZSBzb3VyY2Ugb2YgZXZlbnRzIHRoZSBpbnNwZWN0b3IgbGlzdGVucyBmb3IuXG4gICAqL1xuICBzb3VyY2U6IElJbnNwZWN0b3IuSUluc3BlY3RhYmxlIHwgbnVsbDtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgaW5zcGVjdG9yIGludGVyZmFjZXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSUluc3BlY3RvciB7XG4gIC8qKlxuICAgKiBUaGUgZGVmaW5pdGlvbiBvZiBhbiBpbnNwZWN0YWJsZSBzb3VyY2UuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElJbnNwZWN0YWJsZSB7XG4gICAgLyoqXG4gICAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBpbnNwZWN0b3Igc2hvdWxkIGNsZWFyIGFsbCBpdGVtcy5cbiAgICAgKi9cbiAgICBjbGVhcmVkOiBJU2lnbmFsPGFueSwgdm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGluc3BlY3RhYmxlIGlzIGRpc3Bvc2VkLlxuICAgICAqL1xuICAgIGRpc3Bvc2VkOiBJU2lnbmFsPGFueSwgdm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gYW4gaW5zcGVjdG9yIHZhbHVlIGlzIGdlbmVyYXRlZC5cbiAgICAgKi9cbiAgICBpbnNwZWN0ZWQ6IElTaWduYWw8YW55LCBJSW5zcGVjdG9yVXBkYXRlPjtcblxuICAgIC8qKlxuICAgICAqIFRlc3Qgd2hldGhlciB0aGUgaW5zcGVjdGFibGUgaGFzIGJlZW4gZGlzcG9zZWQuXG4gICAgICovXG4gICAgaXNEaXNwb3NlZDogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIEluZGljYXRlcyB3aGV0aGVyIHRoZSBpbnNwZWN0YWJsZSBzb3VyY2UgZW1pdHMgc2lnbmFscy5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgdXNlIGNhc2UgZm9yIHRoaXMgYXR0cmlidXRlIGlzIHRvIGxpbWl0IHRoZSBBUEkgdHJhZmZpYyB3aGVuIG5vXG4gICAgICogaW5zcGVjdG9yIGlzIHZpc2libGUuIEl0IGNhbiBiZSBtb2RpZmllZCBieSB0aGUgY29uc3VtZXIgb2YgdGhlIHNvdXJjZS5cbiAgICAgKi9cbiAgICBzdGFuZGJ5OiBib29sZWFuO1xuICAgIC8qKlxuICAgICAqIEhhbmRsZSBhIHRleHQgY2hhbmdlZCBzaWduYWwgZnJvbSBhbiBlZGl0b3IuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVXBkYXRlIHRoZSBoaW50cyBpbnNwZWN0b3IgYmFzZWQgb24gYSB0ZXh0IGNoYW5nZS5cbiAgICAgKi9cbiAgICBvbkVkaXRvckNoYW5nZShjdXN0b21UZXh0Pzogc3RyaW5nKTogdm9pZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiB1cGRhdGUgdmFsdWUgZm9yIGNvZGUgaW5zcGVjdG9ycy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUluc3BlY3RvclVwZGF0ZSB7XG4gICAgLyoqXG4gICAgICogVGhlIGNvbnRlbnQgYmVpbmcgc2VudCB0byB0aGUgaW5zcGVjdG9yIGZvciBkaXNwbGF5LlxuICAgICAqL1xuICAgIGNvbnRlbnQ6IFdpZGdldCB8IG51bGw7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==