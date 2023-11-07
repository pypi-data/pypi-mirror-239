"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_htmlviewer_lib_index_js"],{

/***/ "../packages/htmlviewer/lib/index.js":
/*!*******************************************!*\
  !*** ../packages/htmlviewer/lib/index.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HTMLViewer": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.HTMLViewer),
/* harmony export */   "HTMLViewerFactory": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.HTMLViewerFactory),
/* harmony export */   "IHTMLViewerTracker": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.IHTMLViewerTracker),
/* harmony export */   "ToolbarItems": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.ToolbarItems)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/htmlviewer/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/htmlviewer/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module htmlviewer
 */




/***/ }),

/***/ "../packages/htmlviewer/lib/tokens.js":
/*!********************************************!*\
  !*** ../packages/htmlviewer/lib/tokens.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IHTMLViewerTracker": () => (/* binding */ IHTMLViewerTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * The HTML viewer tracker token.
 */
const IHTMLViewerTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/htmlviewer:IHTMLViewerTracker', `A widget tracker for rendered HTML documents.
  Use this if you want to be able to iterate over and interact with HTML documents
  viewed by the application.`);


/***/ }),

/***/ "../packages/htmlviewer/lib/widget.js":
/*!********************************************!*\
  !*** ../packages/htmlviewer/lib/widget.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HTMLViewer": () => (/* binding */ HTMLViewer),
/* harmony export */   "HTMLViewerFactory": () => (/* binding */ HTMLViewerFactory),
/* harmony export */   "ToolbarItems": () => (/* binding */ ToolbarItems)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/






/**
 * The timeout to wait for change activity to have ceased before rendering.
 */
const RENDER_TIMEOUT = 1000;
/**
 * The CSS class to add to the HTMLViewer Widget.
 */
const CSS_CLASS = 'jp-HTMLViewer';
const UNTRUSTED_LINK_STYLE = (options) => `<style>
a[target="_blank"],
area[target="_blank"],
form[target="_blank"],
button[formtarget="_blank"],
input[formtarget="_blank"][type="image"],
input[formtarget="_blank"][type="submit"] {
  cursor: not-allowed !important;
}
a[target="_blank"]:hover::after,
area[target="_blank"]:hover::after,
form[target="_blank"]:hover::after,
button[formtarget="_blank"]:hover::after,
input[formtarget="_blank"][type="image"]:hover::after,
input[formtarget="_blank"][type="submit"]:hover::after {
  content: "${options.warning}";
  box-sizing: border-box;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  border: 2px solid #e65100;
  background-color: #ffb74d;
  color: black;
  font-family: system-ui, -apple-system, blinkmacsystemfont, 'Segoe UI', helvetica, arial, sans-serif;
  text-align: center;
}
</style>`;
/**
 * A viewer widget for HTML documents.
 *
 * #### Notes
 * The iframed HTML document can pose a potential security risk,
 * since it can execute Javascript, and make same-origin requests
 * to the server, thereby executing arbitrary Javascript.
 *
 * Here, we sandbox the iframe so that it can't execute Javascript
 * or launch any popups. We allow one exception: 'allow-same-origin'
 * requests, so that local HTML documents can access CSS, images,
 * etc from the files system.
 */
class HTMLViewer extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget {
    /**
     * Create a new widget for rendering HTML.
     */
    constructor(options) {
        super({
            ...options,
            content: new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.IFrame({ sandbox: ['allow-same-origin'] })
        });
        this._renderPending = false;
        this._parser = new DOMParser();
        this._monitor = null;
        this._objectUrl = '';
        this._trustedChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        this.content.addClass(CSS_CLASS);
        void this.context.ready.then(() => {
            this.update();
            // Throttle the rendering rate of the widget.
            this._monitor = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.ActivityMonitor({
                signal: this.context.model.contentChanged,
                timeout: RENDER_TIMEOUT
            });
            this._monitor.activityStopped.connect(this.update, this);
        });
    }
    /**
     * Whether the HTML document is trusted. If trusted,
     * it can execute Javascript in the iframe sandbox.
     */
    get trusted() {
        return this.content.sandbox.indexOf('allow-scripts') !== -1;
    }
    set trusted(value) {
        if (this.trusted === value) {
            return;
        }
        if (value) {
            this.content.sandbox = Private.trusted;
        }
        else {
            this.content.sandbox = Private.untrusted;
        }
        this.update(); // Force a refresh.
        this._trustedChanged.emit(value);
    }
    /**
     * Emitted when the trust state of the document changes.
     */
    get trustedChanged() {
        return this._trustedChanged;
    }
    /**
     * Dispose of resources held by the html viewer.
     */
    dispose() {
        if (this._objectUrl) {
            try {
                URL.revokeObjectURL(this._objectUrl);
            }
            catch (error) {
                /* no-op */
            }
        }
        super.dispose();
    }
    /**
     * Handle and update request.
     */
    onUpdateRequest() {
        if (this._renderPending) {
            return;
        }
        this._renderPending = true;
        void this._renderModel().then(() => (this._renderPending = false));
    }
    /**
     * Render HTML in IFrame into this widget's node.
     */
    async _renderModel() {
        let data = this.context.model.toString();
        data = await this._setupDocument(data);
        // Set the new iframe url.
        const blob = new Blob([data], { type: 'text/html' });
        const oldUrl = this._objectUrl;
        this._objectUrl = URL.createObjectURL(blob);
        this.content.url = this._objectUrl;
        // Release reference to any previous object url.
        if (oldUrl) {
            try {
                URL.revokeObjectURL(oldUrl);
            }
            catch (error) {
                /* no-op */
            }
        }
        return;
    }
    /**
     * Set a <base> element in the HTML string so that the iframe
     * can correctly dereference relative links.
     */
    async _setupDocument(data) {
        const doc = this._parser.parseFromString(data, 'text/html');
        let base = doc.querySelector('base');
        if (!base) {
            base = doc.createElement('base');
            doc.head.insertBefore(base, doc.head.firstChild);
        }
        const path = this.context.path;
        const baseUrl = await this.context.urlResolver.getDownloadUrl(path);
        // Set the base href, plus a fake name for the url of this
        // document. The fake name doesn't really matter, as long
        // as the document can dereference relative links to resources
        // (e.g. CSS and scripts).
        base.href = baseUrl;
        base.target = '_self';
        // Inject dynamic style for links if the document is not trusted
        if (!this.trusted) {
            const trans = this.translator.load('jupyterlab');
            const warning = trans.__('Action disabled as the file is not trusted.');
            doc.body.insertAdjacentHTML('beforeend', UNTRUSTED_LINK_STYLE({ warning }));
        }
        return doc.documentElement.innerHTML;
    }
}
/**
 * A widget factory for HTMLViewers.
 */
class HTMLViewerFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.ABCWidgetFactory {
    /**
     * Create a new widget given a context.
     */
    createNewWidget(context) {
        return new HTMLViewer({ context });
    }
    /**
     * Default factory for toolbar items to be added after the widget is created.
     */
    defaultToolbarFactory(widget) {
        return [
            // Make a refresh button for the toolbar.
            {
                name: 'refresh',
                widget: ToolbarItems.createRefreshButton(widget, this.translator)
            },
            // Make a trust button for the toolbar.
            {
                name: 'trust',
                widget: ToolbarItems.createTrustButton(widget, this.translator)
            }
        ];
    }
}
/**
 * A namespace for toolbar items generator
 */
var ToolbarItems;
(function (ToolbarItems) {
    /**
     * Create the refresh button
     *
     * @param widget HTML viewer widget
     * @param translator Application translator object
     * @returns Toolbar item button
     */
    function createRefreshButton(widget, translator) {
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator).load('jupyterlab');
        return new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.refreshIcon,
            onClick: async () => {
                if (!widget.context.model.dirty) {
                    await widget.context.revert();
                    widget.update();
                }
            },
            tooltip: trans.__('Rerender HTML Document')
        });
    }
    ToolbarItems.createRefreshButton = createRefreshButton;
    /**
     * Create the trust button
     *
     * @param document HTML viewer widget
     * @param translator Application translator object
     * @returns Toolbar item button
     */
    function createTrustButton(document, translator) {
        return _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_5__.createElement(Private.TrustButtonComponent, { htmlDocument: document, translator: translator }));
    }
    ToolbarItems.createTrustButton = createTrustButton;
})(ToolbarItems || (ToolbarItems = {}));
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * Sandbox exceptions for untrusted HTML.
     */
    Private.untrusted = [];
    /**
     * Sandbox exceptions for trusted HTML.
     */
    Private.trusted = [
        'allow-scripts',
        'allow-popups'
    ];
    /**
     * React component for a trusted button.
     *
     * This wraps the ToolbarButtonComponent and watches for trust changes.
     */
    function TrustButtonComponent(props) {
        const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        return (react__WEBPACK_IMPORTED_MODULE_5__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.UseSignal, { signal: props.htmlDocument.trustedChanged, initialSender: props.htmlDocument }, () => (react__WEBPACK_IMPORTED_MODULE_5__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.ToolbarButtonComponent, { className: "", onClick: () => (props.htmlDocument.trusted = !props.htmlDocument.trusted), tooltip: trans.__(`Whether the HTML file is trusted.
Trusting the file allows opening pop-ups and running scripts
which may result in security risks.
Only enable for files you trust.`), label: props.htmlDocument.trusted
                ? trans.__('Distrust HTML')
                : trans.__('Trust HTML') }))));
    }
    Private.TrustButtonComponent = TrustButtonComponent;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaHRtbHZpZXdlcl9saWJfaW5kZXhfanMuMGZmNjI2ZDRhYjc0ZjRjMDEyMGEuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFFc0I7QUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNSekI7OztHQUdHO0FBR3VDO0FBUTFDOztHQUVHO0FBQ0ksTUFBTSxrQkFBa0IsR0FBRyxJQUFJLG9EQUFLLENBQ3pDLDJDQUEyQyxFQUMzQzs7NkJBRTJCLENBQzVCLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDdEJGOzs7K0VBRytFO0FBRXZCO0FBTXZCO0FBQ3FDO0FBUW5DO0FBQ2lCO0FBRXJCO0FBRS9COztHQUVHO0FBQ0gsTUFBTSxjQUFjLEdBQUcsSUFBSSxDQUFDO0FBRTVCOztHQUVHO0FBQ0gsTUFBTSxTQUFTLEdBQUcsZUFBZSxDQUFDO0FBRWxDLE1BQU0sb0JBQW9CLEdBQUcsQ0FBQyxPQUE0QixFQUFFLEVBQUUsQ0FBQzs7Ozs7Ozs7Ozs7Ozs7O2NBZWpELE9BQU8sQ0FBQyxPQUFPOzs7Ozs7Ozs7Ozs7O1NBYXBCLENBQUM7QUFFVjs7Ozs7Ozs7Ozs7O0dBWUc7QUFDSSxNQUFNLFVBQ1gsU0FBUSxtRUFBc0I7SUFHOUI7O09BRUc7SUFDSCxZQUFZLE9BQStDO1FBQ3pELEtBQUssQ0FBQztZQUNKLEdBQUcsT0FBTztZQUNWLE9BQU8sRUFBRSxJQUFJLDZEQUFNLENBQUMsRUFBRSxPQUFPLEVBQUUsQ0FBQyxtQkFBbUIsQ0FBQyxFQUFFLENBQUM7U0FDeEQsQ0FBQyxDQUFDO1FBNkhHLG1CQUFjLEdBQUcsS0FBSyxDQUFDO1FBQ3ZCLFlBQU8sR0FBRyxJQUFJLFNBQVMsRUFBRSxDQUFDO1FBQzFCLGFBQVEsR0FDZCxJQUFJLENBQUM7UUFDQyxlQUFVLEdBQVcsRUFBRSxDQUFDO1FBQ3hCLG9CQUFlLEdBQUcsSUFBSSxxREFBTSxDQUFnQixJQUFJLENBQUMs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LGlEQUFDLDZFQUFzQixJQUNyQixTQUFTLEVBQUMsRUFBRSxFQUNaLE9BQU8sRUFBRSxHQUFHLEVBQUUsQ0FDWixDQUFDLEtBQUssQ0FBQyxZQUFZLENBQUMsT0FBTyxHQUFHLENBQUMsS0FBSyxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsRUFFNUQsT0FBTyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUM7OztpQ0FHRyxDQUFDLEVBQ3RCLEtBQUssRUFDSCxLQUFLLENBQUMsWUFBWSxDQUFDLE9BQU87Z0JBQ3hCLENBQUMsQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUFDLGVBQWUsQ0FBQztnQkFDM0IsQ0FBQyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsWUFBWSxDQUFDLEdBRTVCLENBQ0gsQ0FDUyxDQUNiLENBQUM7SUFDSixDQUFDO0lBN0JlLDRCQUFvQix1QkE2Qm5DO0FBQ0gsQ0FBQyxFQWxFUyxPQUFPLEtBQVAsT0FBTyxRQWtFaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaHRtbHZpZXdlci9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2h0bWx2aWV3ZXIvc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaHRtbHZpZXdlci9zcmMvd2lkZ2V0LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBodG1sdmlld2VyXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuZXhwb3J0ICogZnJvbSAnLi93aWRnZXQnO1xuIiwiLypcbiAqIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuICogRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbiAqL1xuXG5pbXBvcnQgeyBJV2lkZ2V0VHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSFRNTFZpZXdlciB9IGZyb20gJy4vd2lkZ2V0JztcblxuLyoqXG4gKiBBIGNsYXNzIHRoYXQgdHJhY2tzIEhUTUwgdmlld2VyIHdpZGdldHMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUhUTUxWaWV3ZXJUcmFja2VyIGV4dGVuZHMgSVdpZGdldFRyYWNrZXI8SFRNTFZpZXdlcj4ge31cblxuLyoqXG4gKiBUaGUgSFRNTCB2aWV3ZXIgdHJhY2tlciB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElIVE1MVmlld2VyVHJhY2tlciA9IG5ldyBUb2tlbjxJSFRNTFZpZXdlclRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvaHRtbHZpZXdlcjpJSFRNTFZpZXdlclRyYWNrZXInLFxuICBgQSB3aWRnZXQgdHJhY2tlciBmb3IgcmVuZGVyZWQgSFRNTCBkb2N1bWVudHMuXG4gIFVzZSB0aGlzIGlmIHlvdSB3YW50IHRvIGJlIGFibGUgdG8gaXRlcmF0ZSBvdmVyIGFuZCBpbnRlcmFjdCB3aXRoIEhUTUwgZG9jdW1lbnRzXG4gIHZpZXdlZCBieSB0aGUgYXBwbGljYXRpb24uYFxuKTtcbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuXG5pbXBvcnQgeyBBY3Rpdml0eU1vbml0b3IgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHtcbiAgQUJDV2lkZ2V0RmFjdG9yeSxcbiAgRG9jdW1lbnRSZWdpc3RyeSxcbiAgRG9jdW1lbnRXaWRnZXQsXG4gIElEb2N1bWVudFdpZGdldFxufSBmcm9tICdAanVweXRlcmxhYi9kb2NyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBJRnJhbWUsXG4gIFJlYWN0V2lkZ2V0LFxuICByZWZyZXNoSWNvbixcbiAgVG9vbGJhckJ1dHRvbixcbiAgVG9vbGJhckJ1dHRvbkNvbXBvbmVudCxcbiAgVXNlU2lnbmFsXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoqXG4gKiBUaGUgdGltZW91dCB0byB3YWl0IGZvciBjaGFuZ2UgYWN0aXZpdHkgdG8gaGF2ZSBjZWFzZWQgYmVmb3JlIHJlbmRlcmluZy5cbiAqL1xuY29uc3QgUkVOREVSX1RJTUVPVVQgPSAxMDAwO1xuXG4vKipcbiAqIFRoZSBDU1MgY2xhc3MgdG8gYWRkIHRvIHRoZSBIVE1MVmlld2VyIFdpZGdldC5cbiAqL1xuY29uc3QgQ1NTX0NMQVNTID0gJ2pwLUhUTUxWaWV3ZXInO1xuXG5jb25zdCBVTlRSVVNURURfTElOS19TVFlMRSA9IChvcHRpb25zOiB7IHdhcm5pbmc6IHN0cmluZyB9KSA9PiBgPHN0eWxlPlxuYVt0YXJnZXQ9XCJfYmxhbmtcIl0sXG5hcmVhW3RhcmdldD1cIl9ibGFua1wiXSxcbmZvcm1bdGFyZ2V0PVwiX2JsYW5rXCJdLFxuYnV0dG9uW2Zvcm10YXJnZXQ9XCJfYmxhbmtcIl0sXG5pbnB1dFtmb3JtdGFyZ2V0PVwiX2JsYW5rXCJdW3R5cGU9XCJpbWFnZVwiXSxcbmlucHV0W2Zvcm10YXJnZXQ9XCJfYmxhbmtcIl1bdHlwZT1cInN1Ym1pdFwiXSB7XG4gIGN1cnNvcjogbm90LWFsbG93ZWQgIWltcG9ydGFudDtcbn1cbmFbdGFyZ2V0PVwiX2JsYW5rXCJdOmhvdmVyOjphZnRlcixcbmFyZWFbdGFyZ2V0PVwiX2JsYW5rXCJdOmhvdmVyOjphZnRlcixcbmZvcm1bdGFyZ2V0PVwiX2JsYW5rXCJdOmhvdmVyOjphZnRlcixcbmJ1dHRvbltmb3JtdGFyZ2V0PVwiX2JsYW5rXCJdOmhvdmVyOjphZnRlcixcbmlucHV0W2Zvcm10YXJnZXQ9XCJfYmxhbmtcIl1bdHlwZT1cImltYWdlXCJdOmhvdmVyOjphZnRlcixcbmlucHV0W2Zvcm10YXJnZXQ9XCJfYmxhbmtcIl1bdHlwZT1cInN1Ym1pdFwiXTpob3Zlcjo6YWZ0ZXIge1xuICBjb250ZW50OiBcIiR7b3B0aW9ucy53YXJuaW5nfVwiO1xuICBib3gtc2l6aW5nOiBib3JkZXItYm94O1xuICBwb3NpdGlvbjogZml4ZWQ7XG4gIHRvcDogMDtcbiAgbGVmdDogMDtcbiAgd2lkdGg6IDEwMCU7XG4gIHotaW5kZXg6IDEwMDA7XG4gIGJvcmRlcjogMnB4IHNvbGlkICNlNjUxMDA7XG4gIGJhY2tncm91bmQtY29sb3I6ICNmZmI3NGQ7XG4gIGNvbG9yOiBibGFjaztcbiAgZm9udC1mYW1pbHk6IHN5c3RlbS11aSwgLWFwcGxlLXN5c3RlbSwgYmxpbmttYWNzeXN0ZW1mb250LCAnU2Vnb2UgVUknLCBoZWx2ZXRpY2EsIGFyaWFsLCBzYW5zLXNlcmlmO1xuICB0ZXh0LWFsaWduOiBjZW50ZXI7XG59XG48L3N0eWxlPmA7XG5cbi8qKlxuICogQSB2aWV3ZXIgd2lkZ2V0IGZvciBIVE1MIGRvY3VtZW50cy5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGUgaWZyYW1lZCBIVE1MIGRvY3VtZW50IGNhbiBwb3NlIGEgcG90ZW50aWFsIHNlY3VyaXR5IHJpc2ssXG4gKiBzaW5jZSBpdCBjYW4gZXhlY3V0ZSBKYXZhc2NyaXB0LCBhbmQgbWFrZSBzYW1lLW9yaWdpbiByZXF1ZXN0c1xuICogdG8gdGhlIHNlcnZlciwgdGhlcmVieSBleGVjdXRpbmcgYXJiaXRyYXJ5IEphdmFzY3JpcHQuXG4gKlxuICogSGVyZSwgd2Ugc2FuZGJveCB0aGUgaWZyYW1lIHNvIHRoYXQgaXQgY2FuJ3QgZXhlY3V0ZSBKYXZhc2NyaXB0XG4gKiBvciBsYXVuY2ggYW55IHBvcHVwcy4gV2UgYWxsb3cgb25lIGV4Y2VwdGlvbjogJ2FsbG93LXNhbWUtb3JpZ2luJ1xuICogcmVxdWVzdHMsIHNvIHRoYXQgbG9jYWwgSFRNTCBkb2N1bWVudHMgY2FuIGFjY2VzcyBDU1MsIGltYWdlcyxcbiAqIGV0YyBmcm9tIHRoZSBmaWxlcyBzeXN0ZW0uXG4gKi9cbmV4cG9ydCBjbGFzcyBIVE1MVmlld2VyXG4gIGV4dGVuZHMgRG9jdW1lbnRXaWRnZXQ8SUZyYW1lPlxuICBpbXBsZW1lbnRzIElEb2N1bWVudFdpZGdldDxJRnJhbWU+XG57XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgd2lkZ2V0IGZvciByZW5kZXJpbmcgSFRNTC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IERvY3VtZW50V2lkZ2V0LklPcHRpb25zT3B0aW9uYWxDb250ZW50KSB7XG4gICAgc3VwZXIoe1xuICAgICAgLi4ub3B0aW9ucyxcbiAgICAgIGNvbnRlbnQ6IG5ldyBJRnJhbWUoeyBzYW5kYm94OiBbJ2FsbG93LXNhbWUtb3JpZ2luJ10gfSlcbiAgICB9KTtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5jb250ZW50LmFkZENsYXNzKENTU19DTEFTUyk7XG5cbiAgICB2b2lkIHRoaXMuY29udGV4dC5yZWFkeS50aGVuKCgpID0+IHtcbiAgICAgIHRoaXMudXBkYXRlKCk7XG4gICAgICAvLyBUaHJvdHRsZSB0aGUgcmVuZGVyaW5nIHJhdGUgb2YgdGhlIHdpZGdldC5cbiAgICAgIHRoaXMuX21vbml0b3IgPSBuZXcgQWN0aXZpdHlNb25pdG9yKHtcbiAgICAgICAgc2lnbmFsOiB0aGlzLmNvbnRleHQubW9kZWwuY29udGVudENoYW5nZWQsXG4gICAgICAgIHRpbWVvdXQ6IFJFTkRFUl9USU1FT1VUXG4gICAgICB9KTtcbiAgICAgIHRoaXMuX21vbml0b3IuYWN0aXZpdHlTdG9wcGVkLmNvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIEhUTUwgZG9jdW1lbnQgaXMgdHJ1c3RlZC4gSWYgdHJ1c3RlZCxcbiAgICogaXQgY2FuIGV4ZWN1dGUgSmF2YXNjcmlwdCBpbiB0aGUgaWZyYW1lIHNhbmRib3guXG4gICAqL1xuICBnZXQgdHJ1c3RlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5jb250ZW50LnNhbmRib3guaW5kZXhPZignYWxsb3ctc2NyaXB0cycpICE9PSAtMTtcbiAgfVxuICBzZXQgdHJ1c3RlZCh2YWx1ZTogYm9vbGVhbikge1xuICAgIGlmICh0aGlzLnRydXN0ZWQgPT09IHZhbHVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGlmICh2YWx1ZSkge1xuICAgICAgdGhpcy5jb250ZW50LnNhbmRib3ggPSBQcml2YXRlLnRydXN0ZWQ7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuY29udGVudC5zYW5kYm94ID0gUHJpdmF0ZS51bnRydXN0ZWQ7XG4gICAgfVxuICAgIHRoaXMudXBkYXRlKCk7IC8vIEZvcmNlIGEgcmVmcmVzaC5cbiAgICB0aGlzLl90cnVzdGVkQ2hhbmdlZC5lbWl0KHZhbHVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBFbWl0dGVkIHdoZW4gdGhlIHRydXN0IHN0YXRlIG9mIHRoZSBkb2N1bWVudCBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IHRydXN0ZWRDaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgYm9vbGVhbj4ge1xuICAgIHJldHVybiB0aGlzLl90cnVzdGVkQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHJlc291cmNlcyBoZWxkIGJ5IHRoZSBodG1sIHZpZXdlci5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX29iamVjdFVybCkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgVVJMLnJldm9rZU9iamVjdFVSTCh0aGlzLl9vYmplY3RVcmwpO1xuICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgLyogbm8tb3AgKi9cbiAgICAgIH1cbiAgICB9XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhbmQgdXBkYXRlIHJlcXVlc3QuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25VcGRhdGVSZXF1ZXN0KCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9yZW5kZXJQZW5kaW5nKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX3JlbmRlclBlbmRpbmcgPSB0cnVlO1xuICAgIHZvaWQgdGhpcy5fcmVuZGVyTW9kZWwoKS50aGVuKCgpID0+ICh0aGlzLl9yZW5kZXJQZW5kaW5nID0gZmFsc2UpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgSFRNTCBpbiBJRnJhbWUgaW50byB0aGlzIHdpZGdldCdzIG5vZGUuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9yZW5kZXJNb2RlbCgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBsZXQgZGF0YSA9IHRoaXMuY29udGV4dC5tb2RlbC50b1N0cmluZygpO1xuICAgIGRhdGEgPSBhd2FpdCB0aGlzLl9zZXR1cERvY3VtZW50KGRhdGEpO1xuXG4gICAgLy8gU2V0IHRoZSBuZXcgaWZyYW1lIHVybC5cbiAgICBjb25zdCBibG9iID0gbmV3IEJsb2IoW2RhdGFdLCB7IHR5cGU6ICd0ZXh0L2h0bWwnIH0pO1xuICAgIGNvbnN0IG9sZFVybCA9IHRoaXMuX29iamVjdFVybDtcbiAgICB0aGlzLl9vYmplY3RVcmwgPSBVUkwuY3JlYXRlT2JqZWN0VVJMKGJsb2IpO1xuICAgIHRoaXMuY29udGVudC51cmwgPSB0aGlzLl9vYmplY3RVcmw7XG5cbiAgICAvLyBSZWxlYXNlIHJlZmVyZW5jZSB0byBhbnkgcHJldmlvdXMgb2JqZWN0IHVybC5cbiAgICBpZiAob2xkVXJsKSB7XG4gICAgICB0cnkge1xuICAgICAgICBVUkwucmV2b2tlT2JqZWN0VVJMKG9sZFVybCk7XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICAvKiBuby1vcCAqL1xuICAgICAgfVxuICAgIH1cbiAgICByZXR1cm47XG4gIH1cblxuICAvKipcbiAgICogU2V0IGEgPGJhc2U+IGVsZW1lbnQgaW4gdGhlIEhUTUwgc3RyaW5nIHNvIHRoYXQgdGhlIGlmcmFtZVxuICAgKiBjYW4gY29ycmVjdGx5IGRlcmVmZXJlbmNlIHJlbGF0aXZlIGxpbmtzLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfc2V0dXBEb2N1bWVudChkYXRhOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz4ge1xuICAgIGNvbnN0IGRvYyA9IHRoaXMuX3BhcnNlci5wYXJzZUZyb21TdHJpbmcoZGF0YSwgJ3RleHQvaHRtbCcpO1xuICAgIGxldCBiYXNlID0gZG9jLnF1ZXJ5U2VsZWN0b3IoJ2Jhc2UnKTtcbiAgICBpZiAoIWJhc2UpIHtcbiAgICAgIGJhc2UgPSBkb2MuY3JlYXRlRWxlbWVudCgnYmFzZScpO1xuICAgICAgZG9jLmhlYWQuaW5zZXJ0QmVmb3JlKGJhc2UsIGRvYy5oZWFkLmZpcnN0Q2hpbGQpO1xuICAgIH1cbiAgICBjb25zdCBwYXRoID0gdGhpcy5jb250ZXh0LnBhdGg7XG4gICAgY29uc3QgYmFzZVVybCA9IGF3YWl0IHRoaXMuY29udGV4dC51cmxSZXNvbHZlci5nZXREb3dubG9hZFVybChwYXRoKTtcblxuICAgIC8vIFNldCB0aGUgYmFzZSBocmVmLCBwbHVzIGEgZmFrZSBuYW1lIGZvciB0aGUgdXJsIG9mIHRoaXNcbiAgICAvLyBkb2N1bWVudC4gVGhlIGZha2UgbmFtZSBkb2Vzbid0IHJlYWxseSBtYXR0ZXIsIGFzIGxvbmdcbiAgICAvLyBhcyB0aGUgZG9jdW1lbnQgY2FuIGRlcmVmZXJlbmNlIHJlbGF0aXZlIGxpbmtzIHRvIHJlc291cmNlc1xuICAgIC8vIChlLmcuIENTUyBhbmQgc2NyaXB0cykuXG4gICAgYmFzZS5ocmVmID0gYmFzZVVybDtcbiAgICBiYXNlLnRhcmdldCA9ICdfc2VsZic7XG5cbiAgICAvLyBJbmplY3QgZHluYW1pYyBzdHlsZSBmb3IgbGlua3MgaWYgdGhlIGRvY3VtZW50IGlzIG5vdCB0cnVzdGVkXG4gICAgaWYgKCF0aGlzLnRydXN0ZWQpIHtcbiAgICAgIGNvbnN0IHRyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICAgIGNvbnN0IHdhcm5pbmcgPSB0cmFucy5fXygnQWN0aW9uIGRpc2FibGVkIGFzIHRoZSBmaWxlIGlzIG5vdCB0cnVzdGVkLicpO1xuICAgICAgZG9jLmJvZHkuaW5zZXJ0QWRqYWNlbnRIVE1MKFxuICAgICAgICAnYmVmb3JlZW5kJyxcbiAgICAgICAgVU5UUlVTVEVEX0xJTktfU1RZTEUoeyB3YXJuaW5nIH0pXG4gICAgICApO1xuICAgIH1cbiAgICByZXR1cm4gZG9jLmRvY3VtZW50RWxlbWVudC5pbm5lckhUTUw7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3JlbmRlclBlbmRpbmcgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfcGFyc2VyID0gbmV3IERPTVBhcnNlcigpO1xuICBwcml2YXRlIF9tb25pdG9yOiBBY3Rpdml0eU1vbml0b3I8RG9jdW1lbnRSZWdpc3RyeS5JTW9kZWwsIHZvaWQ+IHwgbnVsbCA9XG4gICAgbnVsbDtcbiAgcHJpdmF0ZSBfb2JqZWN0VXJsOiBzdHJpbmcgPSAnJztcbiAgcHJpdmF0ZSBfdHJ1c3RlZENoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIGJvb2xlYW4+KHRoaXMpO1xufVxuXG4vKipcbiAqIEEgd2lkZ2V0IGZhY3RvcnkgZm9yIEhUTUxWaWV3ZXJzLlxuICovXG5leHBvcnQgY2xhc3MgSFRNTFZpZXdlckZhY3RvcnkgZXh0ZW5kcyBBQkNXaWRnZXRGYWN0b3J5PEhUTUxWaWV3ZXI+IHtcbiAgLyoqXG4gICAqIENyZWF0ZSBhIG5ldyB3aWRnZXQgZ2l2ZW4gYSBjb250ZXh0LlxuICAgKi9cbiAgcHJvdGVjdGVkIGNyZWF0ZU5ld1dpZGdldChjb250ZXh0OiBEb2N1bWVudFJlZ2lzdHJ5LkNvbnRleHQpOiBIVE1MVmlld2VyIHtcbiAgICByZXR1cm4gbmV3IEhUTUxWaWV3ZXIoeyBjb250ZXh0IH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIERlZmF1bHQgZmFjdG9yeSBmb3IgdG9vbGJhciBpdGVtcyB0byBiZSBhZGRlZCBhZnRlciB0aGUgd2lkZ2V0IGlzIGNyZWF0ZWQuXG4gICAqL1xuICBwcm90ZWN0ZWQgZGVmYXVsdFRvb2xiYXJGYWN0b3J5KFxuICAgIHdpZGdldDogSFRNTFZpZXdlclxuICApOiBEb2N1bWVudFJlZ2lzdHJ5LklUb29sYmFySXRlbVtdIHtcbiAgICByZXR1cm4gW1xuICAgICAgLy8gTWFrZSBhIHJlZnJlc2ggYnV0dG9uIGZvciB0aGUgdG9vbGJhci5cbiAgICAgIHtcbiAgICAgICAgbmFtZTogJ3JlZnJlc2gnLFxuICAgICAgICB3aWRnZXQ6IFRvb2xiYXJJdGVtcy5jcmVhdGVSZWZyZXNoQnV0dG9uKHdpZGdldCwgdGhpcy50cmFuc2xhdG9yKVxuICAgICAgfSxcbiAgICAgIC8vIE1ha2UgYSB0cnVzdCBidXR0b24gZm9yIHRoZSB0b29sYmFyLlxuICAgICAge1xuICAgICAgICBuYW1lOiAndHJ1c3QnLFxuICAgICAgICB3aWRnZXQ6IFRvb2xiYXJJdGVtcy5jcmVhdGVUcnVzdEJ1dHRvbih3aWRnZXQsIHRoaXMudHJhbnNsYXRvcilcbiAgICAgIH1cbiAgICBdO1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHRvb2xiYXIgaXRlbXMgZ2VuZXJhdG9yXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgVG9vbGJhckl0ZW1zIHtcbiAgLyoqXG4gICAqIENyZWF0ZSB0aGUgcmVmcmVzaCBidXR0b25cbiAgICpcbiAgICogQHBhcmFtIHdpZGdldCBIVE1MIHZpZXdlciB3aWRnZXRcbiAgICogQHBhcmFtIHRyYW5zbGF0b3IgQXBwbGljYXRpb24gdHJhbnNsYXRvciBvYmplY3RcbiAgICogQHJldHVybnMgVG9vbGJhciBpdGVtIGJ1dHRvblxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZVJlZnJlc2hCdXR0b24oXG4gICAgd2lkZ2V0OiBIVE1MVmlld2VyLFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiBXaWRnZXQge1xuICAgIGNvbnN0IHRyYW5zID0gKHRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3IpLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICByZXR1cm4gbmV3IFRvb2xiYXJCdXR0b24oe1xuICAgICAgaWNvbjogcmVmcmVzaEljb24sXG4gICAgICBvbkNsaWNrOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGlmICghd2lkZ2V0LmNvbnRleHQubW9kZWwuZGlydHkpIHtcbiAgICAgICAgICBhd2FpdCB3aWRnZXQuY29udGV4dC5yZXZlcnQoKTtcbiAgICAgICAgICB3aWRnZXQudXBkYXRlKCk7XG4gICAgICAgIH1cbiAgICAgIH0sXG4gICAgICB0b29sdGlwOiB0cmFucy5fXygnUmVyZW5kZXIgSFRNTCBEb2N1bWVudCcpXG4gICAgfSk7XG4gIH1cbiAgLyoqXG4gICAqIENyZWF0ZSB0aGUgdHJ1c3QgYnV0dG9uXG4gICAqXG4gICAqIEBwYXJhbSBkb2N1bWVudCBIVE1MIHZpZXdlciB3aWRnZXRcbiAgICogQHBhcmFtIHRyYW5zbGF0b3IgQXBwbGljYXRpb24gdHJhbnNsYXRvciBvYmplY3RcbiAgICogQHJldHVybnMgVG9vbGJhciBpdGVtIGJ1dHRvblxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGNyZWF0ZVRydXN0QnV0dG9uKFxuICAgIGRvY3VtZW50OiBIVE1MVmlld2VyLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4gICk6IFdpZGdldCB7XG4gICAgcmV0dXJuIFJlYWN0V2lkZ2V0LmNyZWF0ZShcbiAgICAgIDxQcml2YXRlLlRydXN0QnV0dG9uQ29tcG9uZW50XG4gICAgICAgIGh0bWxEb2N1bWVudD17ZG9jdW1lbnR9XG4gICAgICAgIHRyYW5zbGF0b3I9e3RyYW5zbGF0b3J9XG4gICAgICAvPlxuICAgICk7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBTYW5kYm94IGV4Y2VwdGlvbnMgZm9yIHVudHJ1c3RlZCBIVE1MLlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IHVudHJ1c3RlZDogSUZyYW1lLlNhbmRib3hFeGNlcHRpb25zW10gPSBbXTtcblxuICAvKipcbiAgICogU2FuZGJveCBleGNlcHRpb25zIGZvciB0cnVzdGVkIEhUTUwuXG4gICAqL1xuICBleHBvcnQgY29uc3QgdHJ1c3RlZDogSUZyYW1lLlNhbmRib3hFeGNlcHRpb25zW10gPSBbXG4gICAgJ2FsbG93LXNjcmlwdHMnLFxuICAgICdhbGxvdy1wb3B1cHMnXG4gIF07XG5cbiAgLyoqXG4gICAqIE5hbWVzcGFjZSBmb3IgVHJ1c3RlZEJ1dHRvbi5cbiAgICovXG4gIGV4cG9ydCBuYW1lc3BhY2UgVHJ1c3RCdXR0b25Db21wb25lbnQge1xuICAgIC8qKlxuICAgICAqIEludGVyZmFjZSBmb3IgVHJ1c3RlZEJ1dHRvbiBwcm9wcy5cbiAgICAgKi9cbiAgICBleHBvcnQgaW50ZXJmYWNlIElQcm9wcyB7XG4gICAgICBodG1sRG9jdW1lbnQ6IEhUTUxWaWV3ZXI7XG5cbiAgICAgIC8qKlxuICAgICAgICogTGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgICAqL1xuICAgICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBSZWFjdCBjb21wb25lbnQgZm9yIGEgdHJ1c3RlZCBidXR0b24uXG4gICAqXG4gICAqIFRoaXMgd3JhcHMgdGhlIFRvb2xiYXJCdXR0b25Db21wb25lbnQgYW5kIHdhdGNoZXMgZm9yIHRydXN0IGNoYW5nZXMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gVHJ1c3RCdXR0b25Db21wb25lbnQoXG4gICAgcHJvcHM6IFRydXN0QnV0dG9uQ29tcG9uZW50LklQcm9wc1xuICApOiBKU1guRWxlbWVudCB7XG4gICAgY29uc3QgdHJhbnNsYXRvciA9IHByb3BzLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICByZXR1cm4gKFxuICAgICAgPFVzZVNpZ25hbFxuICAgICAgICBzaWduYWw9e3Byb3BzLmh0bWxEb2N1bWVudC50cnVzdGVkQ2hhbmdlZH1cbiAgICAgICAgaW5pdGlhbFNlbmRlcj17cHJvcHMuaHRtbERvY3VtZW50fVxuICAgICAgPlxuICAgICAgICB7KCkgPT4gKFxuICAgICAgICAgIDxUb29sYmFyQnV0dG9uQ29tcG9uZW50XG4gICAgICAgICAgICBjbGFzc05hbWU9XCJcIlxuICAgICAgICAgICAgb25DbGljaz17KCkgPT5cbiAgICAgICAgICAgICAgKHByb3BzLmh0bWxEb2N1bWVudC50cnVzdGVkID0gIXByb3BzLmh0bWxEb2N1bWVudC50cnVzdGVkKVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgdG9vbHRpcD17dHJhbnMuX18oYFdoZXRoZXIgdGhlIEhUTUwgZmlsZSBpcyB0cnVzdGVkLlxuVHJ1c3RpbmcgdGhlIGZpbGUgYWxsb3dzIG9wZW5pbmcgcG9wLXVwcyBhbmQgcnVubmluZyBzY3JpcHRzXG53aGljaCBtYXkgcmVzdWx0IGluIHNlY3VyaXR5IHJpc2tzLlxuT25seSBlbmFibGUgZm9yIGZpbGVzIHlvdSB0cnVzdC5gKX1cbiAgICAgICAgICAgIGxhYmVsPXtcbiAgICAgICAgICAgICAgcHJvcHMuaHRtbERvY3VtZW50LnRydXN0ZWRcbiAgICAgICAgICAgICAgICA/IHRyYW5zLl9fKCdEaXN0cnVzdCBIVE1MJylcbiAgICAgICAgICAgICAgICA6IHRyYW5zLl9fKCdUcnVzdCBIVE1MJylcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAvPlxuICAgICAgICApfVxuICAgICAgPC9Vc2VTaWduYWw+XG4gICAgKTtcbiAgfVxufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9