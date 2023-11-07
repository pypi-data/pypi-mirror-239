"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_tooltip_lib_index_js-_51c40"],{

/***/ "../packages/tooltip/lib/index.js":
/*!****************************************!*\
  !*** ../packages/tooltip/lib/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITooltipManager": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.ITooltipManager),
/* harmony export */   "Tooltip": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.Tooltip)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/tooltip/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/tooltip/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module tooltip
 */




/***/ }),

/***/ "../packages/tooltip/lib/tokens.js":
/*!*****************************************!*\
  !*** ../packages/tooltip/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITooltipManager": () => (/* binding */ ITooltipManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The tooltip manager token.
 */
const ITooltipManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/tooltip:ITooltipManager', 'A service for the tooltip manager for the application. Use this to allow your extension to invoke a tooltip.');


/***/ }),

/***/ "../packages/tooltip/lib/widget.js":
/*!*****************************************!*\
  !*** ../packages/tooltip/lib/widget.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Tooltip": () => (/* binding */ Tooltip)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * The class name added to each tooltip.
 */
const TOOLTIP_CLASS = 'jp-Tooltip';
/**
 * The class name added to the tooltip content.
 */
const CONTENT_CLASS = 'jp-Tooltip-content';
/**
 * The class added to the body when a tooltip exists on the page.
 */
const BODY_CLASS = 'jp-mod-tooltip';
/**
 * The minimum height of a tooltip widget.
 */
const MIN_HEIGHT = 20;
/**
 * The maximum height of a tooltip widget.
 */
const MAX_HEIGHT = 250;
/**
 * A flag to indicate that event handlers are caught in the capture phase.
 */
const USE_CAPTURE = true;
/**
 * A tooltip widget.
 */
class Tooltip extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    /**
     * Instantiate a tooltip.
     */
    constructor(options) {
        super();
        this._content = null;
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout());
        const model = new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.MimeModel({ data: options.bundle });
        this.anchor = options.anchor;
        this.addClass(TOOLTIP_CLASS);
        this.hide();
        this._editor = options.editor;
        this._position = options.position;
        this._rendermime = options.rendermime;
        const mimeType = this._rendermime.preferredMimeType(options.bundle, 'any');
        if (!mimeType) {
            return;
        }
        this._content = this._rendermime.createRenderer(mimeType);
        this._content
            .renderModel(model)
            .then(() => this._setGeometry())
            .catch(error => console.error('tooltip rendering failed', error));
        this._content.addClass(CONTENT_CLASS);
        layout.addWidget(this._content);
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this._content) {
            this._content.dispose();
            this._content = null;
        }
        super.dispose();
    }
    /**
     * Handle the DOM events for the widget.
     *
     * @param event - The DOM event sent to the widget.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the dock panel's node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        if (this.isHidden || this.isDisposed) {
            return;
        }
        const { node } = this;
        const target = event.target;
        switch (event.type) {
            case 'keydown':
                if (node.contains(target)) {
                    return;
                }
                this.dispose();
                break;
            case 'mousedown':
                if (node.contains(target)) {
                    this.activate();
                    return;
                }
                this.dispose();
                break;
            case 'scroll':
                this._evtScroll(event);
                break;
            default:
                break;
        }
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.tabIndex = 0;
        this.node.focus();
    }
    /**
     * Handle `'after-attach'` messages.
     */
    onAfterAttach(msg) {
        document.body.classList.add(BODY_CLASS);
        document.addEventListener('keydown', this, USE_CAPTURE);
        document.addEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.addEventListener('scroll', this, USE_CAPTURE);
        this.update();
    }
    /**
     * Handle `before-detach` messages for the widget.
     */
    onBeforeDetach(msg) {
        document.body.classList.remove(BODY_CLASS);
        document.removeEventListener('keydown', this, USE_CAPTURE);
        document.removeEventListener('mousedown', this, USE_CAPTURE);
        this.anchor.node.removeEventListener('scroll', this, USE_CAPTURE);
    }
    /**
     * Handle `'update-request'` messages.
     */
    onUpdateRequest(msg) {
        if (this.isHidden) {
            this.show();
        }
        this._setGeometry();
        super.onUpdateRequest(msg);
    }
    /**
     * Handle scroll events for the widget
     */
    _evtScroll(event) {
        // All scrolls except scrolls in the actual hover box node may cause the
        // referent editor that anchors the node to move, so the only scroll events
        // that can safely be ignored are ones that happen inside the hovering node.
        if (this.node.contains(event.target)) {
            return;
        }
        this.update();
    }
    /**
     * Find the position of the first character of the current token.
     */
    _getTokenPosition() {
        const editor = this._editor;
        const cursor = editor.getCursorPosition();
        const end = editor.getOffsetAt(cursor);
        const line = editor.getLine(cursor.line);
        if (!line) {
            return;
        }
        const tokens = line.substring(0, end).split(/\W+/);
        const last = tokens[tokens.length - 1];
        const start = last ? end - last.length : end;
        return editor.getPositionAt(start);
    }
    /**
     * Set the geometry of the tooltip widget.
     */
    _setGeometry() {
        // determine position for hover box placement
        const position = this._position ? this._position : this._getTokenPosition();
        if (!position) {
            return;
        }
        const editor = this._editor;
        const anchor = editor.getCoordinateForPosition(position);
        const style = window.getComputedStyle(this.node);
        const paddingLeft = parseInt(style.paddingLeft, 10) || 0;
        const host = editor.host.closest('.jp-MainAreaWidget > .lm-Widget') ||
            editor.host;
        // Calculate the geometry of the tooltip.
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.HoverBox.setGeometry({
            anchor,
            host,
            maxHeight: MAX_HEIGHT,
            minHeight: MIN_HEIGHT,
            node: this.node,
            offset: { horizontal: -1 * paddingLeft },
            privilege: 'below',
            outOfViewDisplay: {
                top: 'stick-inside',
                bottom: 'stick-inside'
            },
            style: style
        });
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdG9vbHRpcF9saWJfaW5kZXhfanMtXzUxYzQwLjZkODVhZmQ2OGY3ZTUwZjFlOTc1LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUVzQjtBQUNBOzs7Ozs7Ozs7Ozs7Ozs7OztBQ1J6QiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBS2pCO0FBRzFDOztHQUVHO0FBQ0ksTUFBTSxlQUFlLEdBQUcsSUFBSSxvREFBSyxDQUN0QyxxQ0FBcUMsRUFDckMsOEdBQThHLENBQy9HLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ2ZGLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFTjtBQU1yQjtBQUdzQjtBQUV0RDs7R0FFRztBQUNILE1BQU0sYUFBYSxHQUFHLFlBQVksQ0FBQztBQUVuQzs7R0FFRztBQUNILE1BQU0sYUFBYSxHQUFHLG9CQUFvQixDQUFDO0FBRTNDOztHQUVHO0FBQ0gsTUFBTSxVQUFVLEdBQUcsZ0JBQWdCLENBQUM7QUFFcEM7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBRyxFQUFFLENBQUM7QUFFdEI7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBRyxHQUFHLENBQUM7QUFFdkI7O0dBRUc7QUFDSCxNQUFNLFdBQVcsR0FBRyxJQUFJLENBQUM7QUFFekI7O0dBRUc7QUFDSSxNQUFNLE9BQVEsU0FBUSxtREFBTTtJQUNqQzs7T0FFRztJQUNILFlBQVksT0FBeUI7UUFDbkMsS0FBSyxFQUFFLENBQUM7UUFrTUYsYUFBUSxHQUFpQyxJQUFJLENBQUM7UUFoTXBELE1BQU0sTUFBTSxHQUFHLENBQUMsSUFBSSxDQUFDLE1BQU0sR0FBRyxJQUFJLHdEQUFXLEVBQUUsQ0FBQyxDQUFDO1FBQ2pELE1BQU0sS0FBSyxHQUFHLElBQUksNkRBQVMsQ0FBQyxFQUFFLElBQUksRUFBRSxPQUFPLENBQUMsTUFBTSxFQUFFLENBQUMsQ0FBQztRQUV0RCxJQUFJLENBQUMsTUFBTSxHQUFH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V0FBVyxHQUFHLFFBQVEsQ0FBQyxLQUFLLENBQUMsV0FBWSxFQUFFLEVBQUUsQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUUxRCxNQUFNLElBQUksR0FDUCxNQUFNLENBQUMsSUFBSSxDQUFDLE9BQU8sQ0FBQyxpQ0FBaUMsQ0FBaUI7WUFDdkUsTUFBTSxDQUFDLElBQUksQ0FBQztRQUVkLHlDQUF5QztRQUN6QywyRUFBb0IsQ0FBQztZQUNuQixNQUFNO1lBQ04sSUFBSTtZQUNKLFNBQVMsRUFBRSxVQUFVO1lBQ3JCLFNBQVMsRUFBRSxVQUFVO1lBQ3JCLElBQUksRUFBRSxJQUFJLENBQUMsSUFBSTtZQUNmLE1BQU0sRUFBRSxFQUFFLFVBQVUsRUFBRSxDQUFDLENBQUMsR0FBRyxXQUFXLEVBQUU7WUFDeEMsU0FBUyxFQUFFLE9BQU87WUFDbEIsZ0JBQWdCLEVBQUU7Z0JBQ2hCLEdBQUcsRUFBRSxjQUFjO2dCQUNuQixNQUFNLEVBQUUsY0FBYzthQUN2QjtZQUNELEtBQUssRUFBRSxLQUFLO1NBQ2IsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztDQU1GIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3Rvb2x0aXAvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90b29sdGlwL3NyYy90b2tlbnMudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3Rvb2x0aXAvc3JjL3dpZGdldC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSB0b29sdGlwXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuZXhwb3J0ICogZnJvbSAnLi93aWRnZXQnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBDb2RlRWRpdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29kZWVkaXRvcic7XG5pbXBvcnQgeyBJUmVuZGVyTWltZVJlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZSc7XG5pbXBvcnQgeyBLZXJuZWwgfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIHRvb2x0aXAgbWFuYWdlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElUb29sdGlwTWFuYWdlciA9IG5ldyBUb2tlbjxJVG9vbHRpcE1hbmFnZXI+KFxuICAnQGp1cHl0ZXJsYWIvdG9vbHRpcDpJVG9vbHRpcE1hbmFnZXInLFxuICAnQSBzZXJ2aWNlIGZvciB0aGUgdG9vbHRpcCBtYW5hZ2VyIGZvciB0aGUgYXBwbGljYXRpb24uIFVzZSB0aGlzIHRvIGFsbG93IHlvdXIgZXh0ZW5zaW9uIHRvIGludm9rZSBhIHRvb2x0aXAuJ1xuKTtcblxuLyoqXG4gKiBBIG1hbmFnZXIgdG8gcmVnaXN0ZXIgdG9vbHRpcHMgd2l0aCBwYXJlbnQgd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJVG9vbHRpcE1hbmFnZXIge1xuICAvKipcbiAgICogSW52b2tlIGEgdG9vbHRpcC5cbiAgICovXG4gIGludm9rZShvcHRpb25zOiBJVG9vbHRpcE1hbmFnZXIuSU9wdGlvbnMpOiB2b2lkO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgSVRvb2x0aXBNYW5hZ2VyYCBpbnRlcmZhY2Ugc3BlY2lmaWNhdGlvbnMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVRvb2x0aXBNYW5hZ2VyIHtcbiAgLyoqXG4gICAqIEFuIGludGVyZmFjZSBmb3IgdG9vbHRpcC1jb21wYXRpYmxlIG9iamVjdHMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgcmVmZXJlbnQgYW5jaG9yIHRoZSB0b29sdGlwIGZvbGxvd3MuXG4gICAgICovXG4gICAgcmVhZG9ubHkgYW5jaG9yOiBXaWRnZXQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcmVmZXJlbnQgZWRpdG9yIGZvciB0aGUgdG9vbHRpcC5cbiAgICAgKi9cbiAgICByZWFkb25seSBlZGl0b3I6IENvZGVFZGl0b3IuSUVkaXRvcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBrZXJuZWwgdGhlIHRvb2x0aXAgY29tbXVuaWNhdGVzIHdpdGggdG8gcG9wdWxhdGUgaXRzZWxmLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGtlcm5lbDogS2VybmVsLklLZXJuZWxDb25uZWN0aW9uO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlbmRlcmVyIHRoZSB0b29sdGlwIHVzZXMgdG8gcmVuZGVyIEFQSSByZXNwb25zZXMuXG4gICAgICovXG4gICAgcmVhZG9ubHkgcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBIb3ZlckJveCB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgQ29kZUVkaXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL2NvZGVlZGl0b3InO1xuaW1wb3J0IHtcbiAgSVJlbmRlck1pbWUsXG4gIElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIE1pbWVNb2RlbFxufSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgUGFuZWxMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gZWFjaCB0b29sdGlwLlxuICovXG5jb25zdCBUT09MVElQX0NMQVNTID0gJ2pwLVRvb2x0aXAnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIHRoZSB0b29sdGlwIGNvbnRlbnQuXG4gKi9cbmNvbnN0IENPTlRFTlRfQ0xBU1MgPSAnanAtVG9vbHRpcC1jb250ZW50JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgYWRkZWQgdG8gdGhlIGJvZHkgd2hlbiBhIHRvb2x0aXAgZXhpc3RzIG9uIHRoZSBwYWdlLlxuICovXG5jb25zdCBCT0RZX0NMQVNTID0gJ2pwLW1vZC10b29sdGlwJztcblxuLyoqXG4gKiBUaGUgbWluaW11bSBoZWlnaHQgb2YgYSB0b29sdGlwIHdpZGdldC5cbiAqL1xuY29uc3QgTUlOX0hFSUdIVCA9IDIwO1xuXG4vKipcbiAqIFRoZSBtYXhpbXVtIGhlaWdodCBvZiBhIHRvb2x0aXAgd2lkZ2V0LlxuICovXG5jb25zdCBNQVhfSEVJR0hUID0gMjUwO1xuXG4vKipcbiAqIEEgZmxhZyB0byBpbmRpY2F0ZSB0aGF0IGV2ZW50IGhhbmRsZXJzIGFyZSBjYXVnaHQgaW4gdGhlIGNhcHR1cmUgcGhhc2UuXG4gKi9cbmNvbnN0IFVTRV9DQVBUVVJFID0gdHJ1ZTtcblxuLyoqXG4gKiBBIHRvb2x0aXAgd2lkZ2V0LlxuICovXG5leHBvcnQgY2xhc3MgVG9vbHRpcCBleHRlbmRzIFdpZGdldCB7XG4gIC8qKlxuICAgKiBJbnN0YW50aWF0ZSBhIHRvb2x0aXAuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBUb29sdGlwLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcblxuICAgIGNvbnN0IGxheW91dCA9ICh0aGlzLmxheW91dCA9IG5ldyBQYW5lbExheW91dCgpKTtcbiAgICBjb25zdCBtb2RlbCA9IG5ldyBNaW1lTW9kZWwoeyBkYXRhOiBvcHRpb25zLmJ1bmRsZSB9KTtcblxuICAgIHRoaXMuYW5jaG9yID0gb3B0aW9ucy5hbmNob3I7XG4gICAgdGhpcy5hZGRDbGFzcyhUT09MVElQX0NMQVNTKTtcbiAgICB0aGlzLmhpZGUoKTtcbiAgICB0aGlzLl9lZGl0b3IgPSBvcHRpb25zLmVkaXRvcjtcbiAgICB0aGlzLl9wb3NpdGlvbiA9IG9wdGlvbnMucG9zaXRpb247XG4gICAgdGhpcy5fcmVuZGVybWltZSA9IG9wdGlvbnMucmVuZGVybWltZTtcblxuICAgIGNvbnN0IG1pbWVUeXBlID0gdGhpcy5fcmVuZGVybWltZS5wcmVmZXJyZWRNaW1lVHlwZShvcHRpb25zLmJ1bmRsZSwgJ2FueScpO1xuXG4gICAgaWYgKCFtaW1lVHlwZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMuX2NvbnRlbnQgPSB0aGlzLl9yZW5kZXJtaW1lLmNyZWF0ZVJlbmRlcmVyKG1pbWVUeXBlKTtcbiAgICB0aGlzLl9jb250ZW50XG4gICAgICAucmVuZGVyTW9kZWwobW9kZWwpXG4gICAgICAudGhlbigoKSA9PiB0aGlzLl9zZXRHZW9tZXRyeSgpKVxuICAgICAgLmNhdGNoKGVycm9yID0+IGNvbnNvbGUuZXJyb3IoJ3Rvb2x0aXAgcmVuZGVyaW5nIGZhaWxlZCcsIGVycm9yKSk7XG4gICAgdGhpcy5fY29udGVudC5hZGRDbGFzcyhDT05URU5UX0NMQVNTKTtcbiAgICBsYXlvdXQuYWRkV2lkZ2V0KHRoaXMuX2NvbnRlbnQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBhbmNob3Igd2lkZ2V0IHRoYXQgdGhlIHRvb2x0aXAgd2lkZ2V0IHRyYWNrcy5cbiAgICovXG4gIHJlYWRvbmx5IGFuY2hvcjogV2lkZ2V0O1xuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5fY29udGVudCkge1xuICAgICAgdGhpcy5fY29udGVudC5kaXNwb3NlKCk7XG4gICAgICB0aGlzLl9jb250ZW50ID0gbnVsbDtcbiAgICB9XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSB0aGUgRE9NIGV2ZW50cyBmb3IgdGhlIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIGV2ZW50IC0gVGhlIERPTSBldmVudCBzZW50IHRvIHRoZSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaW1wbGVtZW50cyB0aGUgRE9NIGBFdmVudExpc3RlbmVyYCBpbnRlcmZhY2UgYW5kIGlzXG4gICAqIGNhbGxlZCBpbiByZXNwb25zZSB0byBldmVudHMgb24gdGhlIGRvY2sgcGFuZWwncyBub2RlLiBJdCBzaG91bGRcbiAgICogbm90IGJlIGNhbGxlZCBkaXJlY3RseSBieSB1c2VyIGNvZGUuXG4gICAqL1xuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0hpZGRlbiB8fCB0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCB7IG5vZGUgfSA9IHRoaXM7XG4gICAgY29uc3QgdGFyZ2V0ID0gZXZlbnQudGFyZ2V0IGFzIEhUTUxFbGVtZW50O1xuXG4gICAgc3dpdGNoIChldmVudC50eXBlKSB7XG4gICAgICBjYXNlICdrZXlkb3duJzpcbiAgICAgICAgaWYgKG5vZGUuY29udGFpbnModGFyZ2V0KSkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLmRpc3Bvc2UoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdtb3VzZWRvd24nOlxuICAgICAgICBpZiAobm9kZS5jb250YWlucyh0YXJnZXQpKSB7XG4gICAgICAgICAgdGhpcy5hY3RpdmF0ZSgpO1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLmRpc3Bvc2UoKTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdzY3JvbGwnOlxuICAgICAgICB0aGlzLl9ldnRTY3JvbGwoZXZlbnQgYXMgTW91c2VFdmVudCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FjdGl2YXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2YXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLm5vZGUudGFiSW5kZXggPSAwO1xuICAgIHRoaXMubm9kZS5mb2N1cygpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FmdGVyLWF0dGFjaCdgIG1lc3NhZ2VzLlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uQWZ0ZXJBdHRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgZG9jdW1lbnQuYm9keS5jbGFzc0xpc3QuYWRkKEJPRFlfQ0xBU1MpO1xuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2tleWRvd24nLCB0aGlzLCBVU0VfQ0FQVFVSRSk7XG4gICAgZG9jdW1lbnQuYWRkRXZlbnRMaXN0ZW5lcignbW91c2Vkb3duJywgdGhpcywgVVNFX0NBUFRVUkUpO1xuICAgIHRoaXMuYW5jaG9yLm5vZGUuYWRkRXZlbnRMaXN0ZW5lcignc2Nyb2xsJywgdGhpcywgVVNFX0NBUFRVUkUpO1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGBiZWZvcmUtZGV0YWNoYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkJlZm9yZURldGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBkb2N1bWVudC5ib2R5LmNsYXNzTGlzdC5yZW1vdmUoQk9EWV9DTEFTUyk7XG4gICAgZG9jdW1lbnQucmVtb3ZlRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIHRoaXMsIFVTRV9DQVBUVVJFKTtcbiAgICBkb2N1bWVudC5yZW1vdmVFdmVudExpc3RlbmVyKCdtb3VzZWRvd24nLCB0aGlzLCBVU0VfQ0FQVFVSRSk7XG4gICAgdGhpcy5hbmNob3Iubm9kZS5yZW1vdmVFdmVudExpc3RlbmVyKCdzY3JvbGwnLCB0aGlzLCBVU0VfQ0FQVFVSRSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGAndXBkYXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvblVwZGF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNIaWRkZW4pIHtcbiAgICAgIHRoaXMuc2hvdygpO1xuICAgIH1cbiAgICB0aGlzLl9zZXRHZW9tZXRyeSgpO1xuICAgIHN1cGVyLm9uVXBkYXRlUmVxdWVzdChtc2cpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBzY3JvbGwgZXZlbnRzIGZvciB0aGUgd2lkZ2V0XG4gICAqL1xuICBwcml2YXRlIF9ldnRTY3JvbGwoZXZlbnQ6IE1vdXNlRXZlbnQpIHtcbiAgICAvLyBBbGwgc2Nyb2xscyBleGNlcHQgc2Nyb2xscyBpbiB0aGUgYWN0dWFsIGhvdmVyIGJveCBub2RlIG1heSBjYXVzZSB0aGVcbiAgICAvLyByZWZlcmVudCBlZGl0b3IgdGhhdCBhbmNob3JzIHRoZSBub2RlIHRvIG1vdmUsIHNvIHRoZSBvbmx5IHNjcm9sbCBldmVudHNcbiAgICAvLyB0aGF0IGNhbiBzYWZlbHkgYmUgaWdub3JlZCBhcmUgb25lcyB0aGF0IGhhcHBlbiBpbnNpZGUgdGhlIGhvdmVyaW5nIG5vZGUuXG4gICAgaWYgKHRoaXMubm9kZS5jb250YWlucyhldmVudC50YXJnZXQgYXMgSFRNTEVsZW1lbnQpKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgdGhpcy51cGRhdGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGaW5kIHRoZSBwb3NpdGlvbiBvZiB0aGUgZmlyc3QgY2hhcmFjdGVyIG9mIHRoZSBjdXJyZW50IHRva2VuLlxuICAgKi9cbiAgcHJpdmF0ZSBfZ2V0VG9rZW5Qb3NpdGlvbigpOiBDb2RlRWRpdG9yLklQb3NpdGlvbiB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgZWRpdG9yID0gdGhpcy5fZWRpdG9yO1xuICAgIGNvbnN0IGN1cnNvciA9IGVkaXRvci5nZXRDdXJzb3JQb3NpdGlvbigpO1xuICAgIGNvbnN0IGVuZCA9IGVkaXRvci5nZXRPZmZzZXRBdChjdXJzb3IpO1xuICAgIGNvbnN0IGxpbmUgPSBlZGl0b3IuZ2V0TGluZShjdXJzb3IubGluZSk7XG5cbiAgICBpZiAoIWxpbmUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCB0b2tlbnMgPSBsaW5lLnN1YnN0cmluZygwLCBlbmQpLnNwbGl0KC9cXFcrLyk7XG4gICAgY29uc3QgbGFzdCA9IHRva2Vuc1t0b2tlbnMubGVuZ3RoIC0gMV07XG4gICAgY29uc3Qgc3RhcnQgPSBsYXN0ID8gZW5kIC0gbGFzdC5sZW5ndGggOiBlbmQ7XG4gICAgcmV0dXJuIGVkaXRvci5nZXRQb3NpdGlvbkF0KHN0YXJ0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIGdlb21ldHJ5IG9mIHRoZSB0b29sdGlwIHdpZGdldC5cbiAgICovXG4gIHByaXZhdGUgX3NldEdlb21ldHJ5KCk6IHZvaWQge1xuICAgIC8vIGRldGVybWluZSBwb3NpdGlvbiBmb3IgaG92ZXIgYm94IHBsYWNlbWVudFxuICAgIGNvbnN0IHBvc2l0aW9uID0gdGhpcy5fcG9zaXRpb24gPyB0aGlzLl9wb3NpdGlvbiA6IHRoaXMuX2dldFRva2VuUG9zaXRpb24oKTtcblxuICAgIGlmICghcG9zaXRpb24pIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCBlZGl0b3IgPSB0aGlzLl9lZGl0b3I7XG5cbiAgICBjb25zdCBhbmNob3IgPSBlZGl0b3IuZ2V0Q29vcmRpbmF0ZUZvclBvc2l0aW9uKHBvc2l0aW9uKTtcbiAgICBjb25zdCBzdHlsZSA9IHdpbmRvdy5nZXRDb21wdXRlZFN0eWxlKHRoaXMubm9kZSk7XG4gICAgY29uc3QgcGFkZGluZ0xlZnQgPSBwYXJzZUludChzdHlsZS5wYWRkaW5nTGVmdCEsIDEwKSB8fCAwO1xuXG4gICAgY29uc3QgaG9zdCA9XG4gICAgICAoZWRpdG9yLmhvc3QuY2xvc2VzdCgnLmpwLU1haW5BcmVhV2lkZ2V0ID4gLmxtLVdpZGdldCcpIGFzIEhUTUxFbGVtZW50KSB8fFxuICAgICAgZWRpdG9yLmhvc3Q7XG5cbiAgICAvLyBDYWxjdWxhdGUgdGhlIGdlb21ldHJ5IG9mIHRoZSB0b29sdGlwLlxuICAgIEhvdmVyQm94LnNldEdlb21ldHJ5KHtcbiAgICAgIGFuY2hvcixcbiAgICAgIGhvc3QsXG4gICAgICBtYXhIZWlnaHQ6IE1BWF9IRUlHSFQsXG4gICAgICBtaW5IZWlnaHQ6IE1JTl9IRUlHSFQsXG4gICAgICBub2RlOiB0aGlzLm5vZGUsXG4gICAgICBvZmZzZXQ6IHsgaG9yaXpvbnRhbDogLTEgKiBwYWRkaW5nTGVmdCB9LFxuICAgICAgcHJpdmlsZWdlOiAnYmVsb3cnLFxuICAgICAgb3V0T2ZWaWV3RGlzcGxheToge1xuICAgICAgICB0b3A6ICdzdGljay1pbnNpZGUnLFxuICAgICAgICBib3R0b206ICdzdGljay1pbnNpZGUnXG4gICAgICB9LFxuICAgICAgc3R5bGU6IHN0eWxlXG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9jb250ZW50OiBJUmVuZGVyTWltZS5JUmVuZGVyZXIgfCBudWxsID0gbnVsbDtcbiAgcHJpdmF0ZSBfZWRpdG9yOiBDb2RlRWRpdG9yLklFZGl0b3I7XG4gIHByaXZhdGUgX3Bvc2l0aW9uOiBDb2RlRWRpdG9yLklQb3NpdGlvbiB8IHVuZGVmaW5lZDtcbiAgcHJpdmF0ZSBfcmVuZGVybWltZTogSVJlbmRlck1pbWVSZWdpc3RyeTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgdG9vbHRpcCB3aWRnZXQgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBUb29sdGlwIHtcbiAgLyoqXG4gICAqIEluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSB0b29sdGlwIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBhbmNob3Igd2lkZ2V0IHRoYXQgdGhlIHRvb2x0aXAgd2lkZ2V0IHRyYWNrcy5cbiAgICAgKi9cbiAgICBhbmNob3I6IFdpZGdldDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBkYXRhIHRoYXQgcG9wdWxhdGVzIHRoZSB0b29sdGlwIHdpZGdldC5cbiAgICAgKi9cbiAgICBidW5kbGU6IEpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZWRpdG9yIHJlZmVyZW50IG9mIHRoZSB0b29sdGlwIG1vZGVsLlxuICAgICAqL1xuICAgIGVkaXRvcjogQ29kZUVkaXRvci5JRWRpdG9yO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJlbmRlcm1pbWUgaW5zdGFuY2UgdXNlZCBieSB0aGUgdG9vbHRpcCBtb2RlbC5cbiAgICAgKi9cbiAgICByZW5kZXJtaW1lOiBJUmVuZGVyTWltZVJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogUG9zaXRpb24gYXQgd2hpY2ggdGhlIHRvb2x0aXAgc2hvdWxkIGJlIHBsYWNlZC5cbiAgICAgKlxuICAgICAqIElmIG5vdCBnaXZlbiwgdGhlIHBvc2l0aW9uIG9mIHRoZSBmaXJzdCBjaGFyYWN0ZXJcbiAgICAgKiBpbiB0aGUgY3VycmVudCB0b2tlbiB3aWxsIGJlIHVzZWQuXG4gICAgICovXG4gICAgcG9zaXRpb24/OiBDb2RlRWRpdG9yLklQb3NpdGlvbjtcbiAgfVxufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9