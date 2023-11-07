"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_imageviewer_lib_index_js-_2b931"],{

/***/ "../packages/imageviewer/lib/index.js":
/*!********************************************!*\
  !*** ../packages/imageviewer/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IImageTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.IImageTracker),
/* harmony export */   "ImageViewer": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.ImageViewer),
/* harmony export */   "ImageViewerFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.ImageViewerFactory)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/imageviewer/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/imageviewer/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module imageviewer
 */




/***/ }),

/***/ "../packages/imageviewer/lib/tokens.js":
/*!*********************************************!*\
  !*** ../packages/imageviewer/lib/tokens.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IImageTracker": () => (/* binding */ IImageTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The image tracker token.
 */
const IImageTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/imageviewer:IImageTracker', `A widget tracker for images.
  Use this if you want to be able to iterate over and interact with images
  viewed by the application.`);


/***/ }),

/***/ "../packages/imageviewer/lib/widget.js":
/*!*********************************************!*\
  !*** ../packages/imageviewer/lib/widget.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ImageViewer": () => (/* binding */ ImageViewer),
/* harmony export */   "ImageViewerFactory": () => (/* binding */ ImageViewerFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.





/**
 * The class name added to a imageviewer.
 */
const IMAGE_CLASS = 'jp-ImageViewer';
/**
 * A widget for images.
 */
class ImageViewer extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.Widget {
    /**
     * Construct a new image widget.
     */
    constructor(context) {
        super();
        this._scale = 1;
        this._matrix = [1, 0, 0, 1];
        this._colorinversion = 0;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        this.context = context;
        this.node.tabIndex = 0;
        this.addClass(IMAGE_CLASS);
        this._img = document.createElement('img');
        this.node.appendChild(this._img);
        this._onTitleChanged();
        context.pathChanged.connect(this._onTitleChanged, this);
        void context.ready.then(() => {
            if (this.isDisposed) {
                return;
            }
            const contents = context.contentsModel;
            this._mimeType = contents.mimetype;
            this._render();
            context.model.contentChanged.connect(this.update, this);
            context.fileChanged.connect(this.update, this);
            this._ready.resolve(void 0);
        });
    }
    /**
     * Print in iframe.
     */
    [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Printing.symbol]() {
        return () => _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Printing.printWidget(this);
    }
    /**
     * A promise that resolves when the image viewer is ready.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * The scale factor for the image.
     */
    get scale() {
        return this._scale;
    }
    set scale(value) {
        if (value === this._scale) {
            return;
        }
        this._scale = value;
        this._updateStyle();
    }
    /**
     * The color inversion of the image.
     */
    get colorinversion() {
        return this._colorinversion;
    }
    set colorinversion(value) {
        if (value === this._colorinversion) {
            return;
        }
        this._colorinversion = value;
        this._updateStyle();
    }
    /**
     * Dispose of resources held by the image viewer.
     */
    dispose() {
        if (this._img.src) {
            URL.revokeObjectURL(this._img.src || '');
        }
        super.dispose();
    }
    /**
     * Reset rotation and flip transformations.
     */
    resetRotationFlip() {
        this._matrix = [1, 0, 0, 1];
        this._updateStyle();
    }
    /**
     * Rotate the image counter-clockwise (left).
     */
    rotateCounterclockwise() {
        this._matrix = Private.prod(this._matrix, Private.rotateCounterclockwiseMatrix);
        this._updateStyle();
    }
    /**
     * Rotate the image clockwise (right).
     */
    rotateClockwise() {
        this._matrix = Private.prod(this._matrix, Private.rotateClockwiseMatrix);
        this._updateStyle();
    }
    /**
     * Flip the image horizontally.
     */
    flipHorizontal() {
        this._matrix = Private.prod(this._matrix, Private.flipHMatrix);
        this._updateStyle();
    }
    /**
     * Flip the image vertically.
     */
    flipVertical() {
        this._matrix = Private.prod(this._matrix, Private.flipVMatrix);
        this._updateStyle();
    }
    /**
     * Handle `update-request` messages for the widget.
     */
    onUpdateRequest(msg) {
        if (this.isDisposed || !this.context.isReady) {
            return;
        }
        this._render();
    }
    /**
     * Handle `'activate-request'` messages.
     */
    onActivateRequest(msg) {
        this.node.focus();
    }
    /**
     * Handle a change to the title.
     */
    _onTitleChanged() {
        this.title.label = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.basename(this.context.localPath);
    }
    /**
     * Render the widget content.
     */
    _render() {
        const context = this.context;
        const cm = context.contentsModel;
        if (!cm) {
            return;
        }
        const oldurl = this._img.src || '';
        let content = context.model.toString();
        if (cm.format === 'base64') {
            this._img.src = `data:${this._mimeType};base64,${content}`;
        }
        else {
            const a = new Blob([content], { type: this._mimeType });
            this._img.src = URL.createObjectURL(a);
        }
        URL.revokeObjectURL(oldurl);
    }
    /**
     * Update the image CSS style, including the transform and filter.
     */
    _updateStyle() {
        const [a, b, c, d] = this._matrix;
        const [tX, tY] = Private.prodVec(this._matrix, [1, 1]);
        const transform = `matrix(${a}, ${b}, ${c}, ${d}, 0, 0) translate(${tX < 0 ? -100 : 0}%, ${tY < 0 ? -100 : 0}%) `;
        this._img.style.transform = `scale(${this._scale}) ${transform}`;
        this._img.style.filter = `invert(${this._colorinversion})`;
    }
}
/**
 * A widget factory for images.
 */
class ImageViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        const content = new ImageViewer(context);
        const widget = new _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_2__.DocumentWidget({ content, context });
        return widget;
    }
}
/**
 * A namespace for image widget private data.
 */
var Private;
(function (Private) {
    /**
     * Multiply 2x2 matrices.
     */
    function prod([a11, a12, a21, a22], [b11, b12, b21, b22]) {
        return [
            a11 * b11 + a12 * b21,
            a11 * b12 + a12 * b22,
            a21 * b11 + a22 * b21,
            a21 * b12 + a22 * b22
        ];
    }
    Private.prod = prod;
    /**
     * Multiply a 2x2 matrix and a 2x1 vector.
     */
    function prodVec([a11, a12, a21, a22], [b1, b2]) {
        return [a11 * b1 + a12 * b2, a21 * b1 + a22 * b2];
    }
    Private.prodVec = prodVec;
    /**
     * Clockwise rotation transformation matrix.
     */
    Private.rotateClockwiseMatrix = [0, 1, -1, 0];
    /**
     * Counter-clockwise rotation transformation matrix.
     */
    Private.rotateCounterclockwiseMatrix = [0, -1, 1, 0];
    /**
     * Horizontal flip transformation matrix.
     */
    Private.flipHMatrix = [-1, 0, 0, 1];
    /**
     * Vertical flip transformation matrix.
     */
    Private.flipVMatrix = [1, 0, 0, -1];
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaW1hZ2V2aWV3ZXJfbGliX2luZGV4X2pzLV8yYjkzMS44YjcwODhhNmE2ZjgzMmJkMzM5ZC5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRXNCO0FBQ0E7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUnpCLDBDQUEwQztBQUMxQywyREFBMkQ7QUFNakI7QUFVMUM7O0dBRUc7QUFDSSxNQUFNLGFBQWEsR0FBRyxJQUFJLG9EQUFLLENBQ3BDLHVDQUF1QyxFQUN2Qzs7NkJBRTJCLENBQzVCLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDekJGLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFWDtBQUVBO0FBT2Y7QUFFbUI7QUFJWDtBQUV6Qzs7R0FFRztBQUNILE1BQU0sV0FBVyxHQUFHLGdCQUFnQixDQUFDO0FBRXJDOztHQUVHO0FBQ0ksTUFBTSxXQUFZLFNBQVEsbURBQU07SUFDckM7O09BRUc7SUFDSCxZQUFZLE9BQWlDO1FBQzNDLEtBQUssRUFBRSxDQUFDO1FBc0xGLFdBQU0sR0FBRyxDQUFDLENBQUM7UUFDWCxZQUFPLEdBQUcsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQztRQUN2QixvQkFBZSxHQUFHLENBQUMsQ0FBQztRQUNwQixXQUFNLEdBQUcsSUFBSSw4REFBZSxFQUFRLENBQUM7UUF4TDNDLElBQUksQ0FBQyxPQUFPLEdBQUcsT0FBTyxDQUFDO1FBQ3ZCLElBQUksQ0FBQyxJQUFJLENBQUMsUUFBUSxHQUFHLENBQUMsQ0FBQztRQUN2QixJQUFJLENBQUMsUUFBUSxDQUFDLFdBQVcsQ0FBQyxDQUFDO1FBRTNCLElBQUksQ0FBQyxJQUFJLEdBQUcsUUFBUSxDQUFDLGFBQWEsQ0FBQyxLQUFLLENBQUMsQ0FBQztRQUMxQyxJQUFJLENBQUMsSUFBSSxDQUFDLFdBQVcsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLENB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R0FBRyxHQUFHLEVBQUUsQ0FBQyxDQUFDO0lBQ3BELENBQUM7SUFMZSxlQUFPLFVBS3RCO0lBRUQ7O09BRUc7SUFDVSw2QkFBcUIsR0FBRyxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUM7SUFFbkQ7O09BRUc7SUFDVSxvQ0FBNEIsR0FBRyxDQUFDLENBQUMsRUFBRSxDQUFDLENBQUMsRUFBRSxDQUFDLEVBQUUsQ0FBQyxDQUFDLENBQUM7SUFFMUQ7O09BRUc7SUFDVSxtQkFBVyxHQUFHLENBQUMsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQztJQUV6Qzs7T0FFRztJQUNVLG1CQUFXLEdBQUcsQ0FBQyxDQUFDLEVBQUUsQ0FBQyxFQUFFLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxDQUFDO0FBQzNDLENBQUMsRUE3Q1MsT0FBTyxLQUFQLE9BQU8sUUE2Q2hCIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2ltYWdldmlld2VyL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW1hZ2V2aWV3ZXIvc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW1hZ2V2aWV3ZXIvc3JjL3dpZGdldC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBpbWFnZXZpZXdlclxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVdpZGdldFRyYWNrZXIgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5cbmltcG9ydCB7IElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcblxuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5cbmltcG9ydCB7IEltYWdlVmlld2VyIH0gZnJvbSAnLi93aWRnZXQnO1xuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgaW1hZ2Ugd2lkZ2V0cy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJSW1hZ2VUcmFja2VyXG4gIGV4dGVuZHMgSVdpZGdldFRyYWNrZXI8SURvY3VtZW50V2lkZ2V0PEltYWdlVmlld2VyPj4ge31cblxuLyoqXG4gKiBUaGUgaW1hZ2UgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElJbWFnZVRyYWNrZXIgPSBuZXcgVG9rZW48SUltYWdlVHJhY2tlcj4oXG4gICdAanVweXRlcmxhYi9pbWFnZXZpZXdlcjpJSW1hZ2VUcmFja2VyJyxcbiAgYEEgd2lkZ2V0IHRyYWNrZXIgZm9yIGltYWdlcy5cbiAgVXNlIHRoaXMgaWYgeW91IHdhbnQgdG8gYmUgYWJsZSB0byBpdGVyYXRlIG92ZXIgYW5kIGludGVyYWN0IHdpdGggaW1hZ2VzXG4gIHZpZXdlZCBieSB0aGUgYXBwbGljYXRpb24uYFxuKTtcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgUGF0aEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5cbmltcG9ydCB7IFByaW50aW5nIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuXG5pbXBvcnQge1xuICBBQkNXaWRnZXRGYWN0b3J5LFxuICBEb2N1bWVudFJlZ2lzdHJ5LFxuICBEb2N1bWVudFdpZGdldCxcbiAgSURvY3VtZW50V2lkZ2V0XG59IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcblxuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuXG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuXG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgaW1hZ2V2aWV3ZXIuXG4gKi9cbmNvbnN0IElNQUdFX0NMQVNTID0gJ2pwLUltYWdlVmlld2VyJztcblxuLyoqXG4gKiBBIHdpZGdldCBmb3IgaW1hZ2VzLlxuICovXG5leHBvcnQgY2xhc3MgSW1hZ2VWaWV3ZXIgZXh0ZW5kcyBXaWRnZXQgaW1wbGVtZW50cyBQcmludGluZy5JUHJpbnRhYmxlIHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBpbWFnZSB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3Rvcihjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuY29udGV4dCA9IGNvbnRleHQ7XG4gICAgdGhpcy5ub2RlLnRhYkluZGV4ID0gMDtcbiAgICB0aGlzLmFkZENsYXNzKElNQUdFX0NMQVNTKTtcblxuICAgIHRoaXMuX2ltZyA9IGRvY3VtZW50LmNyZWF0ZUVsZW1lbnQoJ2ltZycpO1xuICAgIHRoaXMubm9kZS5hcHBlbmRDaGlsZCh0aGlzLl9pbWcpO1xuXG4gICAgdGhpcy5fb25UaXRsZUNoYW5nZWQoKTtcbiAgICBjb250ZXh0LnBhdGhDaGFuZ2VkLmNvbm5lY3QodGhpcy5fb25UaXRsZUNoYW5nZWQsIHRoaXMpO1xuXG4gICAgdm9pZCBjb250ZXh0LnJlYWR5LnRoZW4oKCkgPT4ge1xuICAgICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICBjb25zdCBjb250ZW50cyA9IGNvbnRleHQuY29udGVudHNNb2RlbCE7XG4gICAgICB0aGlzLl9taW1lVHlwZSA9IGNvbnRlbnRzLm1pbWV0eXBlO1xuICAgICAgdGhpcy5fcmVuZGVyKCk7XG4gICAgICBjb250ZXh0Lm1vZGVsLmNvbnRlbnRDaGFuZ2VkLmNvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuICAgICAgY29udGV4dC5maWxlQ2hhbmdlZC5jb25uZWN0KHRoaXMudXBkYXRlLCB0aGlzKTtcbiAgICAgIHRoaXMuX3JlYWR5LnJlc29sdmUodm9pZCAwKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBQcmludCBpbiBpZnJhbWUuXG4gICAqL1xuICBbUHJpbnRpbmcuc3ltYm9sXSgpIHtcbiAgICByZXR1cm4gKCk6IFByb21pc2U8dm9pZD4gPT4gUHJpbnRpbmcucHJpbnRXaWRnZXQodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGltYWdlIHdpZGdldCdzIGNvbnRleHQuXG4gICAqL1xuICByZWFkb25seSBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQ7XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIGltYWdlIHZpZXdlciBpcyByZWFkeS5cbiAgICovXG4gIGdldCByZWFkeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fcmVhZHkucHJvbWlzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc2NhbGUgZmFjdG9yIGZvciB0aGUgaW1hZ2UuXG4gICAqL1xuICBnZXQgc2NhbGUoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5fc2NhbGU7XG4gIH1cbiAgc2V0IHNjYWxlKHZhbHVlOiBudW1iZXIpIHtcbiAgICBpZiAodmFsdWUgPT09IHRoaXMuX3NjYWxlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX3NjYWxlID0gdmFsdWU7XG4gICAgdGhpcy5fdXBkYXRlU3R5bGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29sb3IgaW52ZXJzaW9uIG9mIHRoZSBpbWFnZS5cbiAgICovXG4gIGdldCBjb2xvcmludmVyc2lvbigpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLl9jb2xvcmludmVyc2lvbjtcbiAgfVxuICBzZXQgY29sb3JpbnZlcnNpb24odmFsdWU6IG51bWJlcikge1xuICAgIGlmICh2YWx1ZSA9PT0gdGhpcy5fY29sb3JpbnZlcnNpb24pIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fY29sb3JpbnZlcnNpb24gPSB2YWx1ZTtcbiAgICB0aGlzLl91cGRhdGVTdHlsZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIGltYWdlIHZpZXdlci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2ltZy5zcmMpIHtcbiAgICAgIFVSTC5yZXZva2VPYmplY3RVUkwodGhpcy5faW1nLnNyYyB8fCAnJyk7XG4gICAgfVxuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXNldCByb3RhdGlvbiBhbmQgZmxpcCB0cmFuc2Zvcm1hdGlvbnMuXG4gICAqL1xuICByZXNldFJvdGF0aW9uRmxpcCgpOiB2b2lkIHtcbiAgICB0aGlzLl9tYXRyaXggPSBbMSwgMCwgMCwgMV07XG4gICAgdGhpcy5fdXBkYXRlU3R5bGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSb3RhdGUgdGhlIGltYWdlIGNvdW50ZXItY2xvY2t3aXNlIChsZWZ0KS5cbiAgICovXG4gIHJvdGF0ZUNvdW50ZXJjbG9ja3dpc2UoKTogdm9pZCB7XG4gICAgdGhpcy5fbWF0cml4ID0gUHJpdmF0ZS5wcm9kKFxuICAgICAgdGhpcy5fbWF0cml4LFxuICAgICAgUHJpdmF0ZS5yb3RhdGVDb3VudGVyY2xvY2t3aXNlTWF0cml4XG4gICAgKTtcbiAgICB0aGlzLl91cGRhdGVTdHlsZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJvdGF0ZSB0aGUgaW1hZ2UgY2xvY2t3aXNlIChyaWdodCkuXG4gICAqL1xuICByb3RhdGVDbG9ja3dpc2UoKTogdm9pZCB7XG4gICAgdGhpcy5fbWF0cml4ID0gUHJpdmF0ZS5wcm9kKHRoaXMuX21hdHJpeCwgUHJpdmF0ZS5yb3RhdGVDbG9ja3dpc2VNYXRyaXgpO1xuICAgIHRoaXMuX3VwZGF0ZVN0eWxlKCk7XG4gIH1cblxuICAvKipcbiAgICogRmxpcCB0aGUgaW1hZ2UgaG9yaXpvbnRhbGx5LlxuICAgKi9cbiAgZmxpcEhvcml6b250YWwoKTogdm9pZCB7XG4gICAgdGhpcy5fbWF0cml4ID0gUHJpdmF0ZS5wcm9kKHRoaXMuX21hdHJpeCwgUHJpdmF0ZS5mbGlwSE1hdHJpeCk7XG4gICAgdGhpcy5fdXBkYXRlU3R5bGUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGbGlwIHRoZSBpbWFnZSB2ZXJ0aWNhbGx5LlxuICAgKi9cbiAgZmxpcFZlcnRpY2FsKCk6IHZvaWQge1xuICAgIHRoaXMuX21hdHJpeCA9IFByaXZhdGUucHJvZCh0aGlzLl9tYXRyaXgsIFByaXZhdGUuZmxpcFZNYXRyaXgpO1xuICAgIHRoaXMuX3VwZGF0ZVN0eWxlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGB1cGRhdGUtcmVxdWVzdGAgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQgfHwgIXRoaXMuY29udGV4dC5pc1JlYWR5KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX3JlbmRlcigpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ2FjdGl2YXRlLXJlcXVlc3QnYCBtZXNzYWdlcy5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFjdGl2YXRlUmVxdWVzdChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLm5vZGUuZm9jdXMoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgdG8gdGhlIHRpdGxlLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25UaXRsZUNoYW5nZWQoKTogdm9pZCB7XG4gICAgdGhpcy50aXRsZS5sYWJlbCA9IFBhdGhFeHQuYmFzZW5hbWUodGhpcy5jb250ZXh0LmxvY2FsUGF0aCk7XG4gIH1cblxuICAvKipcbiAgICogUmVuZGVyIHRoZSB3aWRnZXQgY29udGVudC5cbiAgICovXG4gIHByaXZhdGUgX3JlbmRlcigpOiB2b2lkIHtcbiAgICBjb25zdCBjb250ZXh0ID0gdGhpcy5jb250ZXh0O1xuICAgIGNvbnN0IGNtID0gY29udGV4dC5jb250ZW50c01vZGVsO1xuICAgIGlmICghY20pIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3Qgb2xkdXJsID0gdGhpcy5faW1nLnNyYyB8fCAnJztcbiAgICBsZXQgY29udGVudCA9IGNvbnRleHQubW9kZWwudG9TdHJpbmcoKTtcbiAgICBpZiAoY20uZm9ybWF0ID09PSAnYmFzZTY0Jykge1xuICAgICAgdGhpcy5faW1nLnNyYyA9IGBkYXRhOiR7dGhpcy5fbWltZVR5cGV9O2Jhc2U2NCwke2NvbnRlbnR9YDtcbiAgICB9IGVsc2Uge1xuICAgICAgY29uc3QgYSA9IG5ldyBCbG9iKFtjb250ZW50XSwgeyB0eXBlOiB0aGlzLl9taW1lVHlwZSB9KTtcbiAgICAgIHRoaXMuX2ltZy5zcmMgPSBVUkwuY3JlYXRlT2JqZWN0VVJMKGEpO1xuICAgIH1cbiAgICBVUkwucmV2b2tlT2JqZWN0VVJMKG9sZHVybCk7XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBpbWFnZSBDU1Mgc3R5bGUsIGluY2x1ZGluZyB0aGUgdHJhbnNmb3JtIGFuZCBmaWx0ZXIuXG4gICAqL1xuICBwcml2YXRlIF91cGRhdGVTdHlsZSgpOiB2b2lkIHtcbiAgICBjb25zdCBbYSwgYiwgYywgZF0gPSB0aGlzLl9tYXRyaXg7XG4gICAgY29uc3QgW3RYLCB0WV0gPSBQcml2YXRlLnByb2RWZWModGhpcy5fbWF0cml4LCBbMSwgMV0pO1xuICAgIGNvbnN0IHRyYW5zZm9ybSA9IGBtYXRyaXgoJHthfSwgJHtifSwgJHtjfSwgJHtkfSwgMCwgMCkgdHJhbnNsYXRlKCR7XG4gICAgICB0WCA8IDAgPyAtMTAwIDogMFxuICAgIH0lLCAke3RZIDwgMCA/IC0xMDAgOiAwfSUpIGA7XG4gICAgdGhpcy5faW1nLnN0eWxlLnRyYW5zZm9ybSA9IGBzY2FsZSgke3RoaXMuX3NjYWxlfSkgJHt0cmFuc2Zvcm19YDtcbiAgICB0aGlzLl9pbWcuc3R5bGUuZmlsdGVyID0gYGludmVydCgke3RoaXMuX2NvbG9yaW52ZXJzaW9ufSlgO1xuICB9XG5cbiAgcHJpdmF0ZSBfbWltZVR5cGU6IHN0cmluZztcbiAgcHJpdmF0ZSBfc2NhbGUgPSAxO1xuICBwcml2YXRlIF9tYXRyaXggPSBbMSwgMCwgMCwgMV07XG4gIHByaXZhdGUgX2NvbG9yaW52ZXJzaW9uID0gMDtcbiAgcHJpdmF0ZSBfcmVhZHkgPSBuZXcgUHJvbWlzZURlbGVnYXRlPHZvaWQ+KCk7XG4gIHByaXZhdGUgX2ltZzogSFRNTEltYWdlRWxlbWVudDtcbn1cblxuLyoqXG4gKiBBIHdpZGdldCBmYWN0b3J5IGZvciBpbWFnZXMuXG4gKi9cbmV4cG9ydCBjbGFzcyBJbWFnZVZpZXdlckZhY3RvcnkgZXh0ZW5kcyBBQkNXaWRnZXRGYWN0b3J5PFxuICBJRG9jdW1lbnRXaWRnZXQ8SW1hZ2VWaWV3ZXI+XG4+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB3aWRnZXQgZ2l2ZW4gYSBjb250ZXh0LlxuICAgKi9cbiAgcHJvdGVjdGVkIGNyZWF0ZU5ld1dpZGdldChcbiAgICBjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LklDb250ZXh0PERvY3VtZW50UmVnaXN0cnkuSU1vZGVsPlxuICApOiBJRG9jdW1lbnRXaWRnZXQ8SW1hZ2VWaWV3ZXI+IHtcbiAgICBjb25zdCBjb250ZW50ID0gbmV3IEltYWdlVmlld2VyKGNvbnRleHQpO1xuICAgIGNvbnN0IHdpZGdldCA9IG5ldyBEb2N1bWVudFdpZGdldCh7IGNvbnRlbnQsIGNvbnRleHQgfSk7XG4gICAgcmV0dXJuIHdpZGdldDtcbiAgfVxufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBpbWFnZSB3aWRnZXQgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBNdWx0aXBseSAyeDIgbWF0cmljZXMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcHJvZChcbiAgICBbYTExLCBhMTIsIGEyMSwgYTIyXTogbnVtYmVyW10sXG4gICAgW2IxMSwgYjEyLCBiMjEsIGIyMl06IG51bWJlcltdXG4gICk6IG51bWJlcltdIHtcbiAgICByZXR1cm4gW1xuICAgICAgYTExICogYjExICsgYTEyICogYjIxLFxuICAgICAgYTExICogYjEyICsgYTEyICogYjIyLFxuICAgICAgYTIxICogYjExICsgYTIyICogYjIxLFxuICAgICAgYTIxICogYjEyICsgYTIyICogYjIyXG4gICAgXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBNdWx0aXBseSBhIDJ4MiBtYXRyaXggYW5kIGEgMngxIHZlY3Rvci5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBwcm9kVmVjKFxuICAgIFthMTEsIGExMiwgYTIxLCBhMjJdOiBudW1iZXJbXSxcbiAgICBbYjEsIGIyXTogbnVtYmVyW11cbiAgKTogbnVtYmVyW10ge1xuICAgIHJldHVybiBbYTExICogYjEgKyBhMTIgKiBiMiwgYTIxICogYjEgKyBhMjIgKiBiMl07XG4gIH1cblxuICAvKipcbiAgICogQ2xvY2t3aXNlIHJvdGF0aW9uIHRyYW5zZm9ybWF0aW9uIG1hdHJpeC5cbiAgICovXG4gIGV4cG9ydCBjb25zdCByb3RhdGVDbG9ja3dpc2VNYXRyaXggPSBbMCwgMSwgLTEsIDBdO1xuXG4gIC8qKlxuICAgKiBDb3VudGVyLWNsb2Nrd2lzZSByb3RhdGlvbiB0cmFuc2Zvcm1hdGlvbiBtYXRyaXguXG4gICAqL1xuICBleHBvcnQgY29uc3Qgcm90YXRlQ291bnRlcmNsb2Nrd2lzZU1hdHJpeCA9IFswLCAtMSwgMSwgMF07XG5cbiAgLyoqXG4gICAqIEhvcml6b250YWwgZmxpcCB0cmFuc2Zvcm1hdGlvbiBtYXRyaXguXG4gICAqL1xuICBleHBvcnQgY29uc3QgZmxpcEhNYXRyaXggPSBbLTEsIDAsIDAsIDFdO1xuXG4gIC8qKlxuICAgKiBWZXJ0aWNhbCBmbGlwIHRyYW5zZm9ybWF0aW9uIG1hdHJpeC5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBmbGlwVk1hdHJpeCA9IFsxLCAwLCAwLCAtMV07XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=