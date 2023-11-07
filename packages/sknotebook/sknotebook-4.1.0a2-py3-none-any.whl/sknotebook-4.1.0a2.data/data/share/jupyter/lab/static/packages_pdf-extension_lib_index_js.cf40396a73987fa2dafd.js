"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_pdf-extension_lib_index_js"],{

/***/ "../packages/pdf-extension/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/pdf-extension/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedPDF": () => (/* binding */ RenderedPDF),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module pdf-extension
 */



/**
 * The MIME type for PDF.
 */
const MIME_TYPE = 'application/pdf';
/**
 * A class for rendering a PDF document.
 */
class RenderedPDF extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor() {
        super();
        this._base64 = '';
        this._disposable = null;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        this.addClass('jp-PDFContainer');
        // We put the object in an iframe, which seems to have a better chance
        // of retaining its scroll position upon tab focusing, moving around etc.
        const iframe = document.createElement('iframe');
        this.node.appendChild(iframe);
        // The iframe content window is not available until the onload event.
        iframe.onload = () => {
            const body = iframe.contentWindow.document.createElement('body');
            body.style.margin = '0px';
            iframe.contentWindow.document.body = body;
            this._object = iframe.contentWindow.document.createElement('object');
            // work around for https://discussions.apple.com/thread/252247740
            // Detect if running on Desktop Safari
            if (!window.safari) {
                this._object.type = MIME_TYPE;
            }
            this._object.width = '100%';
            this._object.height = '100%';
            body.appendChild(this._object);
            this._ready.resolve(void 0);
        };
    }
    /**
     * Render PDF into this widget's node.
     */
    async renderModel(model) {
        await this._ready.promise;
        const data = model.data[MIME_TYPE];
        if (!data ||
            (data.length === this._base64.length && data === this._base64)) {
            // If there is no data, or if the string has not changed, we do not
            // need to re-parse the data and rerender. We do, however, check
            // for a fragment if the user wants to scroll the output.
            if (model.metadata.fragment && this._object.data) {
                const url = this._object.data;
                this._object.data = `${url.split('#')[0]}${model.metadata.fragment}`;
            }
            // For some opaque reason, Firefox seems to loose its scroll position
            // upon unhiding a PDF. But triggering a refresh of the URL makes it
            // find it again. No idea what the reason for this is.
            if (Private.IS_FIREFOX) {
                this._object.data = this._object.data; // eslint-disable-line
            }
            return Promise.resolve(void 0);
        }
        this._base64 = data;
        const blob = Private.b64toBlob(data, MIME_TYPE);
        // Release reference to any previous object url.
        if (this._disposable) {
            this._disposable.dispose();
        }
        let objectUrl = URL.createObjectURL(blob);
        if (model.metadata.fragment) {
            objectUrl += model.metadata.fragment;
        }
        this._object.data = objectUrl;
        // Set the disposable release the object URL.
        this._disposable = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            try {
                URL.revokeObjectURL(objectUrl);
            }
            catch (error) {
                /* no-op */
            }
        });
        return;
    }
    /**
     * Handle a `before-hide` message.
     */
    onBeforeHide() {
        // Dispose of any URL fragment before hiding the widget
        // so that it is not remembered upon show. Only Firefox
        // seems to have a problem with this.
        if (Private.IS_FIREFOX) {
            this._object.data = this._object.data.split('#')[0];
        }
    }
    /**
     * Dispose of the resources held by the pdf widget.
     */
    dispose() {
        if (this._disposable) {
            this._disposable.dispose();
        }
        super.dispose();
    }
}
/**
 * A mime renderer factory for PDF data.
 */
const rendererFactory = {
    safe: false,
    mimeTypes: [MIME_TYPE],
    defaultRank: 100,
    createRenderer: options => new RenderedPDF()
};
const extensions = [
    {
        id: '@jupyterlab/pdf-extension:factory',
        description: 'Adds renderer for PDF content.',
        rendererFactory,
        dataType: 'string',
        documentWidgetFactoryOptions: {
            name: 'PDF',
            // TODO: translate label
            modelName: 'base64',
            primaryFileType: 'PDF',
            fileTypes: ['PDF'],
            defaultFor: ['PDF']
        }
    }
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extensions);
/**
 * A namespace for PDF widget private data.
 */
var Private;
(function (Private) {
    /**
     * A flag for determining whether the user is using Firefox.
     * There are some different PDF viewer behaviors on Firefox,
     * and we try to address them with this. User agent string parsing
     * is *not* reliable, so this should be considered a best-effort test.
     */
    Private.IS_FIREFOX = /Firefox/.test(navigator.userAgent);
    /**
     * Convert a base64 encoded string to a Blob object.
     * Modified from a snippet found here:
     * https://stackoverflow.com/questions/16245767/creating-a-blob-from-a-base64-string-in-javascript
     *
     * @param b64Data - The base64 encoded data.
     *
     * @param contentType - The mime type of the data.
     *
     * @param sliceSize - The size to chunk the data into for processing.
     *
     * @returns a Blob for the data.
     */
    function b64toBlob(b64Data, contentType = '', sliceSize = 512) {
        const byteCharacters = atob(b64Data);
        const byteArrays = [];
        for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
            const slice = byteCharacters.slice(offset, offset + sliceSize);
            const byteNumbers = new Array(slice.length);
            for (let i = 0; i < slice.length; i++) {
                byteNumbers[i] = slice.charCodeAt(i);
            }
            const byteArray = new Uint8Array(byteNumbers);
            byteArrays.push(byteArray);
        }
        return new Blob(byteArrays, { type: contentType });
    }
    Private.b64toBlob = b64toBlob;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfcGRmLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuY2Y0MDM5NmE3Mzk4N2ZhMmRhZmQuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFHaUQ7QUFDSTtBQUNmO0FBRXpDOztHQUVHO0FBQ0gsTUFBTSxTQUFTLEdBQUcsaUJBQWlCLENBQUM7QUFFcEM7O0dBRUc7QUFDSSxNQUFNLFdBQVksU0FBUSxtREFBTTtJQUNyQztRQUNFLEtBQUssRUFBRSxDQUFDO1FBK0ZGLFlBQU8sR0FBRyxFQUFFLENBQUM7UUFDYixnQkFBVyxHQUE4QixJQUFJLENBQUM7UUFFOUMsV0FBTSxHQUFHLElBQUksOERBQWUsRUFBUSxDQUFDO1FBakczQyxJQUFJLENBQUMsUUFBUSxDQUFDLGlCQUFpQixDQUFDLENBQUM7UUFDakMsc0VBQXNFO1FBQ3RFLHlFQUF5RTtRQUN6RSxNQUFNLE1BQU0sR0FBRyxRQUFRLENBQUMsYUFBYSxDQUFDLFFBQVEsQ0FBQyxDQUFDO1FBQ2hELElBQUksQ0FBQyxJQUFJLENBQUMsV0FBVyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1FBQzlCLHFFQUFxRTtRQUNyRSxNQUFNLENBQUMsTUFBTSxHQUFHLEdBQUcsRUFBRTtZQUNuQixNQUFNLElBQUksR0FBRyxNQUFNLENBQUMsYUFBYyxDQUFDLFFBQVEsQ0FBQyxhQUFhLENBQUMsTUFBTSxDQUFDLENBQUM7WUFDbEUsSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNLEdBQUcsS0FBSyxDQUFDO1lBQzFCLE1BQU0sQ0FBQyxhQUFjLENBQUMsUUFBUSxDQUFDLElBQUksR0FBRyxJQUFJLENBQUM7WUFDM0MsSUFBSSxDQUFDLE9BQU8sR0FBRyxNQUFNLENBQUMsYUFBYyxDQUFDLFFBQVEsQ0FBQyxhQUFhLENBQUMsUUFBUSxDQUFDLENBQUM7WUFDdEUsaUVBQWlFO1lBQ2pFLHNDQUFzQztZQUN0QyxJQUFJLENBQUUsTUFBYyxD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QU8sQ0FBQyxDQUFDO1FBQ3JDLE1BQU0sVUFBVSxHQUFpQixFQUFFLENBQUM7UUFFcEMsS0FBSyxJQUFJLE1BQU0sR0FBRyxDQUFDLEVBQUUsTUFBTSxHQUFHLGNBQWMsQ0FBQyxNQUFNLEVBQUUsTUFBTSxJQUFJLFNBQVMsRUFBRTtZQUN4RSxNQUFNLEtBQUssR0FBRyxjQUFjLENBQUMsS0FBSyxDQUFDLE1BQU0sRUFBRSxNQUFNLEdBQUcsU0FBUyxDQUFDLENBQUM7WUFFL0QsTUFBTSxXQUFXLEdBQUcsSUFBSSxLQUFLLENBQUMsS0FBSyxDQUFDLE1BQU0sQ0FBQyxDQUFDO1lBQzVDLEtBQUssSUFBSSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsR0FBRyxLQUFLLENBQUMsTUFBTSxFQUFFLENBQUMsRUFBRSxFQUFFO2dCQUNyQyxXQUFXLENBQUMsQ0FBQyxDQUFDLEdBQUcsS0FBSyxDQUFDLFVBQVUsQ0FBQyxDQUFDLENBQUMsQ0FBQzthQUN0QztZQUNELE1BQU0sU0FBUyxHQUFHLElBQUksVUFBVSxDQUFDLFdBQVcsQ0FBQyxDQUFDO1lBQzlDLFVBQVUsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUFDLENBQUM7U0FDNUI7UUFFRCxPQUFPLElBQUksSUFBSSxDQUFDLFVBQVUsRUFBRSxFQUFFLElBQUksRUFBRSxXQUFXLEVBQUUsQ0FBQyxDQUFDO0lBQ3JELENBQUM7SUFwQmUsaUJBQVMsWUFvQnhCO0FBQ0gsQ0FBQyxFQTNDUyxPQUFPLEtBQVAsT0FBTyxRQTJDaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcGRmLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgcGRmLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcbmltcG9ydCB7IFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERpc3Bvc2FibGVEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuXG4vKipcbiAqIFRoZSBNSU1FIHR5cGUgZm9yIFBERi5cbiAqL1xuY29uc3QgTUlNRV9UWVBFID0gJ2FwcGxpY2F0aW9uL3BkZic7XG5cbi8qKlxuICogQSBjbGFzcyBmb3IgcmVuZGVyaW5nIGEgUERGIGRvY3VtZW50LlxuICovXG5leHBvcnQgY2xhc3MgUmVuZGVyZWRQREYgZXh0ZW5kcyBXaWRnZXQgaW1wbGVtZW50cyBJUmVuZGVyTWltZS5JUmVuZGVyZXIge1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLVBERkNvbnRhaW5lcicpO1xuICAgIC8vIFdlIHB1dCB0aGUgb2JqZWN0IGluIGFuIGlmcmFtZSwgd2hpY2ggc2VlbXMgdG8gaGF2ZSBhIGJldHRlciBjaGFuY2VcbiAgICAvLyBvZiByZXRhaW5pbmcgaXRzIHNjcm9sbCBwb3NpdGlvbiB1cG9uIHRhYiBmb2N1c2luZywgbW92aW5nIGFyb3VuZCBldGMuXG4gICAgY29uc3QgaWZyYW1lID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnaWZyYW1lJyk7XG4gICAgdGhpcy5ub2RlLmFwcGVuZENoaWxkKGlmcmFtZSk7XG4gICAgLy8gVGhlIGlmcmFtZSBjb250ZW50IHdpbmRvdyBpcyBub3QgYXZhaWxhYmxlIHVudGlsIHRoZSBvbmxvYWQgZXZlbnQuXG4gICAgaWZyYW1lLm9ubG9hZCA9ICgpID0+IHtcbiAgICAgIGNvbnN0IGJvZHkgPSBpZnJhbWUuY29udGVudFdpbmRvdyEuZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnYm9keScpO1xuICAgICAgYm9keS5zdHlsZS5tYXJnaW4gPSAnMHB4JztcbiAgICAgIGlmcmFtZS5jb250ZW50V2luZG93IS5kb2N1bWVudC5ib2R5ID0gYm9keTtcbiAgICAgIHRoaXMuX29iamVjdCA9IGlmcmFtZS5jb250ZW50V2luZG93IS5kb2N1bWVudC5jcmVhdGVFbGVtZW50KCdvYmplY3QnKTtcbiAgICAgIC8vIHdvcmsgYXJvdW5kIGZvciBodHRwczovL2Rpc2N1c3Npb25zLmFwcGxlLmNvbS90aHJlYWQvMjUyMjQ3NzQwXG4gICAgICAvLyBEZXRlY3QgaWYgcnVubmluZyBvbiBEZXNrdG9wIFNhZmFyaVxuICAgICAgaWYgKCEod2luZG93IGFzIGFueSkuc2FmYXJpKSB7XG4gICAgICAgIHRoaXMuX29iamVjdC50eXBlID0gTUlNRV9UWVBFO1xuICAgICAgfVxuICAgICAgdGhpcy5fb2JqZWN0LndpZHRoID0gJzEwMCUnO1xuICAgICAgdGhpcy5fb2JqZWN0LmhlaWdodCA9ICcxMDAlJztcbiAgICAgIGJvZHkuYXBwZW5kQ2hpbGQodGhpcy5fb2JqZWN0KTtcbiAgICAgIHRoaXMuX3JlYWR5LnJlc29sdmUodm9pZCAwKTtcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbmRlciBQREYgaW50byB0aGlzIHdpZGdldCdzIG5vZGUuXG4gICAqL1xuICBhc3luYyByZW5kZXJNb2RlbChtb2RlbDogSVJlbmRlck1pbWUuSU1pbWVNb2RlbCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGF3YWl0IHRoaXMuX3JlYWR5LnByb21pc2U7XG4gICAgY29uc3QgZGF0YSA9IG1vZGVsLmRhdGFbTUlNRV9UWVBFXSBhcyBzdHJpbmcgfCB1bmRlZmluZWQ7XG4gICAgaWYgKFxuICAgICAgIWRhdGEgfHxcbiAgICAgIChkYXRhLmxlbmd0aCA9PT0gdGhpcy5fYmFzZTY0Lmxlbmd0aCAmJiBkYXRhID09PSB0aGlzLl9iYXNlNjQpXG4gICAgKSB7XG4gICAgICAvLyBJZiB0aGVyZSBpcyBubyBkYXRhLCBvciBpZiB0aGUgc3RyaW5nIGhhcyBub3QgY2hhbmdlZCwgd2UgZG8gbm90XG4gICAgICAvLyBuZWVkIHRvIHJlLXBhcnNlIHRoZSBkYXRhIGFuZCByZXJlbmRlci4gV2UgZG8sIGhvd2V2ZXIsIGNoZWNrXG4gICAgICAvLyBmb3IgYSBmcmFnbWVudCBpZiB0aGUgdXNlciB3YW50cyB0byBzY3JvbGwgdGhlIG91dHB1dC5cbiAgICAgIGlmIChtb2RlbC5tZXRhZGF0YS5mcmFnbWVudCAmJiB0aGlzLl9vYmplY3QuZGF0YSkge1xuICAgICAgICBjb25zdCB1cmwgPSB0aGlzLl9vYmplY3QuZGF0YTtcbiAgICAgICAgdGhpcy5fb2JqZWN0LmRhdGEgPSBgJHt1cmwuc3BsaXQoJyMnKVswXX0ke21vZGVsLm1ldGFkYXRhLmZyYWdtZW50fWA7XG4gICAgICB9XG4gICAgICAvLyBGb3Igc29tZSBvcGFxdWUgcmVhc29uLCBGaXJlZm94IHNlZW1zIHRvIGxvb3NlIGl0cyBzY3JvbGwgcG9zaXRpb25cbiAgICAgIC8vIHVwb24gdW5oaWRpbmcgYSBQREYuIEJ1dCB0cmlnZ2VyaW5nIGEgcmVmcmVzaCBvZiB0aGUgVVJMIG1ha2VzIGl0XG4gICAgICAvLyBmaW5kIGl0IGFnYWluLiBObyBpZGVhIHdoYXQgdGhlIHJlYXNvbiBmb3IgdGhpcyBpcy5cbiAgICAgIGlmIChQcml2YXRlLklTX0ZJUkVGT1gpIHtcbiAgICAgICAgdGhpcy5fb2JqZWN0LmRhdGEgPSB0aGlzLl9vYmplY3QuZGF0YTsgLy8gZXNsaW50LWRpc2FibGUtbGluZVxuICAgICAgfVxuICAgICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZSh2b2lkIDApO1xuICAgIH1cbiAgICB0aGlzLl9iYXNlNjQgPSBkYXRhO1xuICAgIGNvbnN0IGJsb2IgPSBQcml2YXRlLmI2NHRvQmxvYihkYXRhLCBNSU1FX1RZUEUpO1xuXG4gICAgLy8gUmVsZWFzZSByZWZlcmVuY2UgdG8gYW55IHByZXZpb3VzIG9iamVjdCB1cmwuXG4gICAgaWYgKHRoaXMuX2Rpc3Bvc2FibGUpIHtcbiAgICAgIHRoaXMuX2Rpc3Bvc2FibGUuZGlzcG9zZSgpO1xuICAgIH1cbiAgICBsZXQgb2JqZWN0VXJsID0gVVJMLmNyZWF0ZU9iamVjdFVSTChibG9iKTtcbiAgICBpZiAobW9kZWwubWV0YWRhdGEuZnJhZ21lbnQpIHtcbiAgICAgIG9iamVjdFVybCArPSBtb2RlbC5tZXRhZGF0YS5mcmFnbWVudDtcbiAgICB9XG4gICAgdGhpcy5fb2JqZWN0LmRhdGEgPSBvYmplY3RVcmw7XG5cbiAgICAvLyBTZXQgdGhlIGRpc3Bvc2FibGUgcmVsZWFzZSB0aGUgb2JqZWN0IFVSTC5cbiAgICB0aGlzLl9kaXNwb3NhYmxlID0gbmV3IERpc3Bvc2FibGVEZWxlZ2F0ZSgoKSA9PiB7XG4gICAgICB0cnkge1xuICAgICAgICBVUkwucmV2b2tlT2JqZWN0VVJMKG9iamVjdFVybCk7XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICAvKiBuby1vcCAqL1xuICAgICAgfVxuICAgIH0pO1xuICAgIHJldHVybjtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBgYmVmb3JlLWhpZGVgIG1lc3NhZ2UuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVIaWRlKCk6IHZvaWQge1xuICAgIC8vIERpc3Bvc2Ugb2YgYW55IFVSTCBmcmFnbWVudCBiZWZvcmUgaGlkaW5nIHRoZSB3aWRnZXRcbiAgICAvLyBzbyB0aGF0IGl0IGlzIG5vdCByZW1lbWJlcmVkIHVwb24gc2hvdy4gT25seSBGaXJlZm94XG4gICAgLy8gc2VlbXMgdG8gaGF2ZSBhIHByb2JsZW0gd2l0aCB0aGlzLlxuICAgIGlmIChQcml2YXRlLklTX0ZJUkVGT1gpIHtcbiAgICAgIHRoaXMuX29iamVjdC5kYXRhID0gdGhpcy5fb2JqZWN0LmRhdGEuc3BsaXQoJyMnKVswXTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHBkZiB3aWRnZXQuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9kaXNwb3NhYmxlKSB7XG4gICAgICB0aGlzLl9kaXNwb3NhYmxlLmRpc3Bvc2UoKTtcbiAgICB9XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgcHJpdmF0ZSBfYmFzZTY0ID0gJyc7XG4gIHByaXZhdGUgX2Rpc3Bvc2FibGU6IERpc3Bvc2FibGVEZWxlZ2F0ZSB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9vYmplY3Q6IEhUTUxPYmplY3RFbGVtZW50O1xuICBwcml2YXRlIF9yZWFkeSA9IG5ldyBQcm9taXNlRGVsZWdhdGU8dm9pZD4oKTtcbn1cblxuLyoqXG4gKiBBIG1pbWUgcmVuZGVyZXIgZmFjdG9yeSBmb3IgUERGIGRhdGEuXG4gKi9cbmV4cG9ydCBjb25zdCByZW5kZXJlckZhY3Rvcnk6IElSZW5kZXJNaW1lLklSZW5kZXJlckZhY3RvcnkgPSB7XG4gIHNhZmU6IGZhbHNlLFxuICBtaW1lVHlwZXM6IFtNSU1FX1RZUEVdLFxuICBkZWZhdWx0UmFuazogMTAwLFxuICBjcmVhdGVSZW5kZXJlcjogb3B0aW9ucyA9PiBuZXcgUmVuZGVyZWRQREYoKVxufTtcblxuY29uc3QgZXh0ZW5zaW9uczogSVJlbmRlck1pbWUuSUV4dGVuc2lvbiB8IElSZW5kZXJNaW1lLklFeHRlbnNpb25bXSA9IFtcbiAge1xuICAgIGlkOiAnQGp1cHl0ZXJsYWIvcGRmLWV4dGVuc2lvbjpmYWN0b3J5JyxcbiAgICBkZXNjcmlwdGlvbjogJ0FkZHMgcmVuZGVyZXIgZm9yIFBERiBjb250ZW50LicsXG4gICAgcmVuZGVyZXJGYWN0b3J5LFxuICAgIGRhdGFUeXBlOiAnc3RyaW5nJyxcbiAgICBkb2N1bWVudFdpZGdldEZhY3RvcnlPcHRpb25zOiB7XG4gICAgICBuYW1lOiAnUERGJyxcbiAgICAgIC8vIFRPRE86IHRyYW5zbGF0ZSBsYWJlbFxuICAgICAgbW9kZWxOYW1lOiAnYmFzZTY0JyxcbiAgICAgIHByaW1hcnlGaWxlVHlwZTogJ1BERicsXG4gICAgICBmaWxlVHlwZXM6IFsnUERGJ10sXG4gICAgICBkZWZhdWx0Rm9yOiBbJ1BERiddXG4gICAgfVxuICB9XG5dO1xuXG5leHBvcnQgZGVmYXVsdCBleHRlbnNpb25zO1xuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBQREYgd2lkZ2V0IHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQSBmbGFnIGZvciBkZXRlcm1pbmluZyB3aGV0aGVyIHRoZSB1c2VyIGlzIHVzaW5nIEZpcmVmb3guXG4gICAqIFRoZXJlIGFyZSBzb21lIGRpZmZlcmVudCBQREYgdmlld2VyIGJlaGF2aW9ycyBvbiBGaXJlZm94LFxuICAgKiBhbmQgd2UgdHJ5IHRvIGFkZHJlc3MgdGhlbSB3aXRoIHRoaXMuIFVzZXIgYWdlbnQgc3RyaW5nIHBhcnNpbmdcbiAgICogaXMgKm5vdCogcmVsaWFibGUsIHNvIHRoaXMgc2hvdWxkIGJlIGNvbnNpZGVyZWQgYSBiZXN0LWVmZm9ydCB0ZXN0LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IElTX0ZJUkVGT1g6IGJvb2xlYW4gPSAvRmlyZWZveC8udGVzdChuYXZpZ2F0b3IudXNlckFnZW50KTtcblxuICAvKipcbiAgICogQ29udmVydCBhIGJhc2U2NCBlbmNvZGVkIHN0cmluZyB0byBhIEJsb2Igb2JqZWN0LlxuICAgKiBNb2RpZmllZCBmcm9tIGEgc25pcHBldCBmb3VuZCBoZXJlOlxuICAgKiBodHRwczovL3N0YWNrb3ZlcmZsb3cuY29tL3F1ZXN0aW9ucy8xNjI0NTc2Ny9jcmVhdGluZy1hLWJsb2ItZnJvbS1hLWJhc2U2NC1zdHJpbmctaW4tamF2YXNjcmlwdFxuICAgKlxuICAgKiBAcGFyYW0gYjY0RGF0YSAtIFRoZSBiYXNlNjQgZW5jb2RlZCBkYXRhLlxuICAgKlxuICAgKiBAcGFyYW0gY29udGVudFR5cGUgLSBUaGUgbWltZSB0eXBlIG9mIHRoZSBkYXRhLlxuICAgKlxuICAgKiBAcGFyYW0gc2xpY2VTaXplIC0gVGhlIHNpemUgdG8gY2h1bmsgdGhlIGRhdGEgaW50byBmb3IgcHJvY2Vzc2luZy5cbiAgICpcbiAgICogQHJldHVybnMgYSBCbG9iIGZvciB0aGUgZGF0YS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBiNjR0b0Jsb2IoXG4gICAgYjY0RGF0YTogc3RyaW5nLFxuICAgIGNvbnRlbnRUeXBlOiBzdHJpbmcgPSAnJyxcbiAgICBzbGljZVNpemU6IG51bWJlciA9IDUxMlxuICApOiBCbG9iIHtcbiAgICBjb25zdCBieXRlQ2hhcmFjdGVycyA9IGF0b2IoYjY0RGF0YSk7XG4gICAgY29uc3QgYnl0ZUFycmF5czogVWludDhBcnJheVtdID0gW107XG5cbiAgICBmb3IgKGxldCBvZmZzZXQgPSAwOyBvZmZzZXQgPCBieXRlQ2hhcmFjdGVycy5sZW5ndGg7IG9mZnNldCArPSBzbGljZVNpemUpIHtcbiAgICAgIGNvbnN0IHNsaWNlID0gYnl0ZUNoYXJhY3RlcnMuc2xpY2Uob2Zmc2V0LCBvZmZzZXQgKyBzbGljZVNpemUpO1xuXG4gICAgICBjb25zdCBieXRlTnVtYmVycyA9IG5ldyBBcnJheShzbGljZS5sZW5ndGgpO1xuICAgICAgZm9yIChsZXQgaSA9IDA7IGkgPCBzbGljZS5sZW5ndGg7IGkrKykge1xuICAgICAgICBieXRlTnVtYmVyc1tpXSA9IHNsaWNlLmNoYXJDb2RlQXQoaSk7XG4gICAgICB9XG4gICAgICBjb25zdCBieXRlQXJyYXkgPSBuZXcgVWludDhBcnJheShieXRlTnVtYmVycyk7XG4gICAgICBieXRlQXJyYXlzLnB1c2goYnl0ZUFycmF5KTtcbiAgICB9XG5cbiAgICByZXR1cm4gbmV3IEJsb2IoYnl0ZUFycmF5cywgeyB0eXBlOiBjb250ZW50VHlwZSB9KTtcbiAgfVxufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9