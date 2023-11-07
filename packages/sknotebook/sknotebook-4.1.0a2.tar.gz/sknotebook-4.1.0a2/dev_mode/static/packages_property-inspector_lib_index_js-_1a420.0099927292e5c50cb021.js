"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_property-inspector_lib_index_js-_1a420"],{

/***/ "../packages/property-inspector/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/property-inspector/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IPropertyInspectorProvider": () => (/* reexport safe */ _token__WEBPACK_IMPORTED_MODULE_4__.IPropertyInspectorProvider),
/* harmony export */   "SideBarPropertyInspectorProvider": () => (/* binding */ SideBarPropertyInspectorProvider)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _token__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./token */ "../packages/property-inspector/lib/token.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module property-inspector
 */






/**
 * The implementation of the PropertyInspector.
 */
class PropertyInspectorProvider extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget {
    /**
     * Construct a new Property Inspector.
     */
    constructor() {
        super();
        this._tracker = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.FocusTracker();
        this._inspectors = new Map();
        this.addClass('jp-PropertyInspector');
        this._tracker = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.FocusTracker();
        this._tracker.currentChanged.connect(this._onCurrentChanged, this);
    }
    /**
     * Register a widget in the property inspector provider.
     *
     * @param widget The owner widget to register.
     */
    register(widget) {
        if (this._inspectors.has(widget)) {
            throw new Error('Widget is already registered');
        }
        const inspector = new Private.PropertyInspector(widget);
        widget.disposed.connect(this._onWidgetDisposed, this);
        this._inspectors.set(widget, inspector);
        inspector.onAction.connect(this._onInspectorAction, this);
        this._tracker.add(widget);
        return inspector;
    }
    /**
     * The current widget being tracked by the inspector.
     */
    get currentWidget() {
        return this._tracker.currentWidget;
    }
    /**
     * Refresh the content for the current widget.
     */
    refresh() {
        const current = this._tracker.currentWidget;
        if (!current) {
            this.setContent(null);
            return;
        }
        const inspector = this._inspectors.get(current);
        if (inspector) {
            this.setContent(inspector.content);
        }
    }
    /**
     * Handle the disposal of a widget.
     */
    _onWidgetDisposed(sender) {
        const inspector = this._inspectors.get(sender);
        if (inspector) {
            inspector.dispose();
            this._inspectors.delete(sender);
        }
    }
    /**
     * Handle inspector actions.
     */
    _onInspectorAction(sender, action) {
        const owner = sender.owner;
        const current = this._tracker.currentWidget;
        switch (action) {
            case 'content':
                if (current === owner) {
                    this.setContent(sender.content);
                }
                break;
            case 'dispose':
                if (owner) {
                    this._tracker.remove(owner);
                    this._inspectors.delete(owner);
                }
                break;
            case 'show-panel':
                if (current === owner) {
                    this.showPanel();
                }
                break;
            default:
                throw new Error('Unsupported inspector action');
        }
    }
    /**
     * Handle a change to the current widget in the tracker.
     */
    _onCurrentChanged() {
        const current = this._tracker.currentWidget;
        if (current) {
            const inspector = this._inspectors.get(current);
            const content = inspector.content;
            this.setContent(content);
        }
        else {
            this.setContent(null);
        }
    }
}
/**
 * A class that adds a property inspector provider to the
 * JupyterLab sidebar.
 */
class SideBarPropertyInspectorProvider extends PropertyInspectorProvider {
    /**
     * Construct a new Side Bar Property Inspector.
     */
    constructor({ shell, placeholder, translator }) {
        super();
        this._labshell = shell;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.SingletonLayout());
        if (placeholder) {
            this._placeholder = placeholder;
        }
        else {
            const node = document.createElement('div');
            const content = document.createElement('div');
            content.textContent = this._trans.__('No properties to inspect.');
            content.className = 'jp-PropertyInspector-placeholderContent';
            node.appendChild(content);
            this._placeholder = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget({ node });
            this._placeholder.addClass('jp-PropertyInspector-placeholder');
        }
        layout.widget = this._placeholder;
        this._labshell.currentChanged.connect(this._onShellCurrentChanged, this);
        this._onShellCurrentChanged();
    }
    /**
     * Set the content of the sidebar panel.
     */
    setContent(content) {
        const layout = this.layout;
        if (layout.widget) {
            layout.widget.removeClass('jp-PropertyInspector-content');
            layout.removeWidget(layout.widget);
        }
        if (!content) {
            content = this._placeholder;
        }
        content.addClass('jp-PropertyInspector-content');
        layout.widget = content;
    }
    /**
     * Show the sidebar panel.
     */
    showPanel() {
        this._labshell.activateById(this.id);
    }
    /**
     * Handle the case when the current widget is not in our tracker.
     */
    _onShellCurrentChanged() {
        const current = this.currentWidget;
        if (!current) {
            this.setContent(null);
            return;
        }
        const currentShell = this._labshell.currentWidget;
        if (currentShell === null || currentShell === void 0 ? void 0 : currentShell.node.contains(current.node)) {
            this.refresh();
        }
        else {
            this.setContent(null);
        }
    }
}
/**
 * A namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * An implementation of the property inspector used by the
     * property inspector provider.
     */
    class PropertyInspector {
        /**
         * Construct a new property inspector.
         */
        constructor(owner) {
            this._isDisposed = false;
            this._content = null;
            this._owner = null;
            this._onAction = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
            this._owner = owner;
        }
        /**
         * The owner widget for the property inspector.
         */
        get owner() {
            return this._owner;
        }
        /**
         * The current content for the property inspector.
         */
        get content() {
            return this._content;
        }
        /**
         * Whether the property inspector is disposed.
         */
        get isDisposed() {
            return this._isDisposed;
        }
        /**
         * A signal used for actions related to the property inspector.
         */
        get onAction() {
            return this._onAction;
        }
        /**
         * Show the property inspector panel.
         */
        showPanel() {
            if (this._isDisposed) {
                return;
            }
            this._onAction.emit('show-panel');
        }
        /**
         * Render the property inspector content.
         */
        render(widget) {
            if (this._isDisposed) {
                return;
            }
            if (widget instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_3__.Widget) {
                this._content = widget;
            }
            else {
                this._content = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(widget);
            }
            this._onAction.emit('content');
        }
        /**
         * Dispose of the property inspector.
         */
        dispose() {
            if (this._isDisposed) {
                return;
            }
            this._isDisposed = true;
            this._content = null;
            this._owner = null;
            _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
        }
    }
    Private.PropertyInspector = PropertyInspector;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/property-inspector/lib/token.js":
/*!***************************************************!*\
  !*** ../packages/property-inspector/lib/token.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IPropertyInspectorProvider": () => (/* binding */ IPropertyInspectorProvider)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The property inspector provider token.
 */
const IPropertyInspectorProvider = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/property-inspector:IPropertyInspectorProvider', 'A service to registry new widget in the property inspector side panel.');


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfcHJvcGVydHktaW5zcGVjdG9yX2xpYl9pbmRleF9qcy1fMWE0MjAuMDA5OTkyNzI5MmU1YzUwY2IwMjEuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU84QjtBQUN1QjtBQUNKO0FBQ29CO0FBRUM7QUFFZjtBQUUxRDs7R0FFRztBQUNILE1BQWUseUJBQ2IsU0FBUSxtREFBTTtJQUdkOztPQUVHO0lBQ0g7UUFDRSxLQUFLLEVBQUUsQ0FBQztRQStHRixhQUFRLEdBQUcsSUFBSSx5REFBWSxFQUFFLENBQUM7UUFDOUIsZ0JBQVcsR0FBRyxJQUFJLEdBQUcsRUFBcUMsQ0FBQztRQS9HakUsSUFBSSxDQUFDLFFBQVEsQ0FBQyxzQkFBc0IsQ0FBQyxDQUFDO1FBQ3RDLElBQUksQ0FBQyxRQUFRLEdBQUcsSUFBSSx5REFBWSxFQUFFLENBQUM7UUFDbkMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxjQUFjLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxpQkFBaUIsRUFBRSxJQUFJLENBQUMsQ0FBQztJQUNyRSxDQUFDO0lBRUQ7Ozs7T0FJRztJQUNILFFBQVEsQ0FBQyxNQUFjO1FBQ3JCLElBQUksSUFBSSxDQUFDLFdBQVcsQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLEVBQUU7WUFDaEMsTUFBTSxJQUFJLEtBQUssQ0FBQyw4QkFBOEIsQ0FBQyxDQUFDO1NBQ2pEO1FBQ0QsTUFBTSxTQUFTLEdBQUcsSUFBSSxPQUFPLENBQUMsaUJBQWlCLENBQUMsTUFBTSxDQUFDLENBQUM7UUFDeEQsTUFBTSxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLGlCQUFpQixFQUFFLElBQUksQ0FBQyxDQUFDO1FBQ3RELElBQUksQ0FBQyxXQUFXLENBQUMsR0FBRyxDQUFDLE1BQU0sRUFBRSxTQUFTLENBQUMsQ0FBQztRQUN4QyxTQUFTLENBQUMsUUFBUSxDQUFDLE9BQU8s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LEdBQUcsSUFBSSxDQUFDO1lBQ3hCLElBQUksQ0FBQyxRQUFRLEdBQUcsSUFBSSxDQUFDO1lBQ3JCLElBQUksQ0FBQyxNQUFNLEdBQUcsSUFBSSxDQUFDO1lBQ25CLCtEQUFnQixDQUFDLElBQUksQ0FBQyxDQUFDO1FBQ3pCLENBQUM7S0FTRjtJQWpGWSx5QkFBaUIsb0JBaUY3QjtBQUNILENBQUMsRUE1RlMsT0FBTyxLQUFQLE9BQU8sUUE0RmhCOzs7Ozs7Ozs7Ozs7Ozs7OztBQ3BWRCwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRWpCO0FBa0QxQzs7R0FFRztBQUNJLE1BQU0sMEJBQTBCLEdBQUcsSUFBSSxvREFBSyxDQUNqRCwyREFBMkQsRUFDM0Qsd0VBQXdFLENBQ3pFLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcHJvcGVydHktaW5zcGVjdG9yL3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcHJvcGVydHktaW5zcGVjdG9yL3NyYy90b2tlbi50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBwcm9wZXJ0eS1pbnNwZWN0b3JcbiAqL1xuXG5pbXBvcnQgeyBJTGFiU2hlbGwgfSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQge1xuICBJVHJhbnNsYXRvcixcbiAgbnVsbFRyYW5zbGF0b3IsXG4gIFRyYW5zbGF0aW9uQnVuZGxlXG59IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFJlYWN0V2lkZ2V0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBGb2N1c1RyYWNrZXIsIFNpbmdsZXRvbkxheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IElQcm9wZXJ0eUluc3BlY3RvciwgSVByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXIgfSBmcm9tICcuL3Rva2VuJztcblxuZXhwb3J0IHsgSVByb3BlcnR5SW5zcGVjdG9yLCBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciB9O1xuXG4vKipcbiAqIFRoZSBpbXBsZW1lbnRhdGlvbiBvZiB0aGUgUHJvcGVydHlJbnNwZWN0b3IuXG4gKi9cbmFic3RyYWN0IGNsYXNzIFByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXJcbiAgZXh0ZW5kcyBXaWRnZXRcbiAgaW1wbGVtZW50cyBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlclxue1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IFByb3BlcnR5IEluc3BlY3Rvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtUHJvcGVydHlJbnNwZWN0b3InKTtcbiAgICB0aGlzLl90cmFja2VyID0gbmV3IEZvY3VzVHJhY2tlcigpO1xuICAgIHRoaXMuX3RyYWNrZXIuY3VycmVudENoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkN1cnJlbnRDaGFuZ2VkLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZWdpc3RlciBhIHdpZGdldCBpbiB0aGUgcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IFRoZSBvd25lciB3aWRnZXQgdG8gcmVnaXN0ZXIuXG4gICAqL1xuICByZWdpc3Rlcih3aWRnZXQ6IFdpZGdldCk6IElQcm9wZXJ0eUluc3BlY3RvciB7XG4gICAgaWYgKHRoaXMuX2luc3BlY3RvcnMuaGFzKHdpZGdldCkpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignV2lkZ2V0IGlzIGFscmVhZHkgcmVnaXN0ZXJlZCcpO1xuICAgIH1cbiAgICBjb25zdCBpbnNwZWN0b3IgPSBuZXcgUHJpdmF0ZS5Qcm9wZXJ0eUluc3BlY3Rvcih3aWRnZXQpO1xuICAgIHdpZGdldC5kaXNwb3NlZC5jb25uZWN0KHRoaXMuX29uV2lkZ2V0RGlzcG9zZWQsIHRoaXMpO1xuICAgIHRoaXMuX2luc3BlY3RvcnMuc2V0KHdpZGdldCwgaW5zcGVjdG9yKTtcbiAgICBpbnNwZWN0b3Iub25BY3Rpb24uY29ubmVjdCh0aGlzLl9vbkluc3BlY3RvckFjdGlvbiwgdGhpcyk7XG4gICAgdGhpcy5fdHJhY2tlci5hZGQod2lkZ2V0KTtcbiAgICByZXR1cm4gaW5zcGVjdG9yO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjdXJyZW50IHdpZGdldCBiZWluZyB0cmFja2VkIGJ5IHRoZSBpbnNwZWN0b3IuXG4gICAqL1xuICBwcm90ZWN0ZWQgZ2V0IGN1cnJlbnRXaWRnZXQoKTogV2lkZ2V0IHwgbnVsbCB7XG4gICAgcmV0dXJuIHRoaXMuX3RyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZWZyZXNoIHRoZSBjb250ZW50IGZvciB0aGUgY3VycmVudCB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgcmVmcmVzaCgpOiB2b2lkIHtcbiAgICBjb25zdCBjdXJyZW50ID0gdGhpcy5fdHJhY2tlci5jdXJyZW50V2lkZ2V0O1xuICAgIGlmICghY3VycmVudCkge1xuICAgICAgdGhpcy5zZXRDb250ZW50KG51bGwpO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBpbnNwZWN0b3IgPSB0aGlzLl9pbnNwZWN0b3JzLmdldChjdXJyZW50KTtcbiAgICBpZiAoaW5zcGVjdG9yKSB7XG4gICAgICB0aGlzLnNldENvbnRlbnQoaW5zcGVjdG9yLmNvbnRlbnQpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBTaG93IHRoZSBwcm92aWRlciBwYW5lbC5cbiAgICovXG4gIHByb3RlY3RlZCBhYnN0cmFjdCBzaG93UGFuZWwoKTogdm9pZDtcblxuICAvKipcbiAgICogU2V0IHRoZSBjb250ZW50IG9mIHRoZSBwcm92aWRlci5cbiAgICovXG4gIHByb3RlY3RlZCBhYnN0cmFjdCBzZXRDb250ZW50KGNvbnRlbnQ6IFdpZGdldCB8IG51bGwpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGRpc3Bvc2FsIG9mIGEgd2lkZ2V0LlxuICAgKi9cbiAgcHJpdmF0ZSBfb25XaWRnZXREaXNwb3NlZChzZW5kZXI6IFdpZGdldCk6IHZvaWQge1xuICAgIGNvbnN0IGluc3BlY3RvciA9IHRoaXMuX2luc3BlY3RvcnMuZ2V0KHNlbmRlcik7XG4gICAgaWYgKGluc3BlY3Rvcikge1xuICAgICAgaW5zcGVjdG9yLmRpc3Bvc2UoKTtcbiAgICAgIHRoaXMuX2luc3BlY3RvcnMuZGVsZXRlKHNlbmRlcik7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBpbnNwZWN0b3IgYWN0aW9ucy5cbiAgICovXG4gIHByaXZhdGUgX29uSW5zcGVjdG9yQWN0aW9uKFxuICAgIHNlbmRlcjogUHJpdmF0ZS5Qcm9wZXJ0eUluc3BlY3RvcixcbiAgICBhY3Rpb246IFByaXZhdGUuUHJvcGVydHlJbnNwZWN0b3JBY3Rpb25cbiAgKSB7XG4gICAgY29uc3Qgb3duZXIgPSBzZW5kZXIub3duZXI7XG4gICAgY29uc3QgY3VycmVudCA9IHRoaXMuX3RyYWNrZXIuY3VycmVudFdpZGdldDtcbiAgICBzd2l0Y2ggKGFjdGlvbikge1xuICAgICAgY2FzZSAnY29udGVudCc6XG4gICAgICAgIGlmIChjdXJyZW50ID09PSBvd25lcikge1xuICAgICAgICAgIHRoaXMuc2V0Q29udGVudChzZW5kZXIuY29udGVudCk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdkaXNwb3NlJzpcbiAgICAgICAgaWYgKG93bmVyKSB7XG4gICAgICAgICAgdGhpcy5fdHJhY2tlci5yZW1vdmUob3duZXIpO1xuICAgICAgICAgIHRoaXMuX2luc3BlY3RvcnMuZGVsZXRlKG93bmVyKTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3Nob3ctcGFuZWwnOlxuICAgICAgICBpZiAoY3VycmVudCA9PT0gb3duZXIpIHtcbiAgICAgICAgICB0aGlzLnNob3dQYW5lbCgpO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKCdVbnN1cHBvcnRlZCBpbnNwZWN0b3IgYWN0aW9uJyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBhIGNoYW5nZSB0byB0aGUgY3VycmVudCB3aWRnZXQgaW4gdGhlIHRyYWNrZXIuXG4gICAqL1xuICBwcml2YXRlIF9vbkN1cnJlbnRDaGFuZ2VkKCk6IHZvaWQge1xuICAgIGNvbnN0IGN1cnJlbnQgPSB0aGlzLl90cmFja2VyLmN1cnJlbnRXaWRnZXQ7XG4gICAgaWYgKGN1cnJlbnQpIHtcbiAgICAgIGNvbnN0IGluc3BlY3RvciA9IHRoaXMuX2luc3BlY3RvcnMuZ2V0KGN1cnJlbnQpO1xuICAgICAgY29uc3QgY29udGVudCA9IGluc3BlY3RvciEuY29udGVudDtcbiAgICAgIHRoaXMuc2V0Q29udGVudChjb250ZW50KTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5zZXRDb250ZW50KG51bGwpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX3RyYWNrZXIgPSBuZXcgRm9jdXNUcmFja2VyKCk7XG4gIHByaXZhdGUgX2luc3BlY3RvcnMgPSBuZXcgTWFwPFdpZGdldCwgUHJpdmF0ZS5Qcm9wZXJ0eUluc3BlY3Rvcj4oKTtcbn1cblxuLyoqXG4gKiB7QGxpbmsgU2lkZUJhclByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXJ9IGNvbnN0cnVjdG9yIG9wdGlvbnNcbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJTGFiUHJvcGVydHlJbnNwZWN0b3JPcHRpb25zIHtcbiAgLyoqXG4gICAqIEFwcGxpY2F0aW9uIHNoZWxsXG4gICAqL1xuICBzaGVsbDogSUxhYlNoZWxsO1xuICAvKipcbiAgICogV2lkZ2V0IHBsYWNlaG9sZGVyXG4gICAqL1xuICBwbGFjZWhvbGRlcj86IFdpZGdldDtcbiAgLyoqXG4gICAqIEFwcGxpY2F0aW9uIHRyYW5zbGF0aW9uXG4gICAqL1xuICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG59XG5cbi8qKlxuICogQSBjbGFzcyB0aGF0IGFkZHMgYSBwcm9wZXJ0eSBpbnNwZWN0b3IgcHJvdmlkZXIgdG8gdGhlXG4gKiBKdXB5dGVyTGFiIHNpZGViYXIuXG4gKi9cbmV4cG9ydCBjbGFzcyBTaWRlQmFyUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciBleHRlbmRzIFByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXIge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IFNpZGUgQmFyIFByb3BlcnR5IEluc3BlY3Rvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKHtcbiAgICBzaGVsbCxcbiAgICBwbGFjZWhvbGRlcixcbiAgICB0cmFuc2xhdG9yXG4gIH06IElMYWJQcm9wZXJ0eUluc3BlY3Rvck9wdGlvbnMpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX2xhYnNoZWxsID0gc2hlbGw7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl90cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgY29uc3QgbGF5b3V0ID0gKHRoaXMubGF5b3V0ID0gbmV3IFNpbmdsZXRvbkxheW91dCgpKTtcbiAgICBpZiAocGxhY2Vob2xkZXIpIHtcbiAgICAgIHRoaXMuX3BsYWNlaG9sZGVyID0gcGxhY2Vob2xkZXI7XG4gICAgfSBlbHNlIHtcbiAgICAgIGNvbnN0IG5vZGUgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICAgIGNvbnN0IGNvbnRlbnQgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICAgIGNvbnRlbnQudGV4dENvbnRlbnQgPSB0aGlzLl90cmFucy5fXygnTm8gcHJvcGVydGllcyB0byBpbnNwZWN0LicpO1xuICAgICAgY29udGVudC5jbGFzc05hbWUgPSAnanAtUHJvcGVydHlJbnNwZWN0b3ItcGxhY2Vob2xkZXJDb250ZW50JztcbiAgICAgIG5vZGUuYXBwZW5kQ2hpbGQoY29udGVudCk7XG4gICAgICB0aGlzLl9wbGFjZWhvbGRlciA9IG5ldyBXaWRnZXQoeyBub2RlIH0pO1xuICAgICAgdGhpcy5fcGxhY2Vob2xkZXIuYWRkQ2xhc3MoJ2pwLVByb3BlcnR5SW5zcGVjdG9yLXBsYWNlaG9sZGVyJyk7XG4gICAgfVxuICAgIGxheW91dC53aWRnZXQgPSB0aGlzLl9wbGFjZWhvbGRlcjtcbiAgICB0aGlzLl9sYWJzaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KHRoaXMuX29uU2hlbGxDdXJyZW50Q2hhbmdlZCwgdGhpcyk7XG4gICAgdGhpcy5fb25TaGVsbEN1cnJlbnRDaGFuZ2VkKCk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBjb250ZW50IG9mIHRoZSBzaWRlYmFyIHBhbmVsLlxuICAgKi9cbiAgcHJvdGVjdGVkIHNldENvbnRlbnQoY29udGVudDogV2lkZ2V0IHwgbnVsbCk6IHZvaWQge1xuICAgIGNvbnN0IGxheW91dCA9IHRoaXMubGF5b3V0IGFzIFNpbmdsZXRvbkxheW91dDtcbiAgICBpZiAobGF5b3V0LndpZGdldCkge1xuICAgICAgbGF5b3V0LndpZGdldC5yZW1vdmVDbGFzcygnanAtUHJvcGVydHlJbnNwZWN0b3ItY29udGVudCcpO1xuICAgICAgbGF5b3V0LnJlbW92ZVdpZGdldChsYXlvdXQud2lkZ2V0KTtcbiAgICB9XG4gICAgaWYgKCFjb250ZW50KSB7XG4gICAgICBjb250ZW50ID0gdGhpcy5fcGxhY2Vob2xkZXI7XG4gICAgfVxuICAgIGNvbnRlbnQuYWRkQ2xhc3MoJ2pwLVByb3BlcnR5SW5zcGVjdG9yLWNvbnRlbnQnKTtcbiAgICBsYXlvdXQud2lkZ2V0ID0gY29udGVudDtcbiAgfVxuXG4gIC8qKlxuICAgKiBTaG93IHRoZSBzaWRlYmFyIHBhbmVsLlxuICAgKi9cbiAgc2hvd1BhbmVsKCk6IHZvaWQge1xuICAgIHRoaXMuX2xhYnNoZWxsLmFjdGl2YXRlQnlJZCh0aGlzLmlkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIGNhc2Ugd2hlbiB0aGUgY3VycmVudCB3aWRnZXQgaXMgbm90IGluIG91ciB0cmFja2VyLlxuICAgKi9cbiAgcHJpdmF0ZSBfb25TaGVsbEN1cnJlbnRDaGFuZ2VkKCk6IHZvaWQge1xuICAgIGNvbnN0IGN1cnJlbnQgPSB0aGlzLmN1cnJlbnRXaWRnZXQ7XG4gICAgaWYgKCFjdXJyZW50KSB7XG4gICAgICB0aGlzLnNldENvbnRlbnQobnVsbCk7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGN1cnJlbnRTaGVsbCA9IHRoaXMuX2xhYnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgaWYgKGN1cnJlbnRTaGVsbD8ubm9kZS5jb250YWlucyhjdXJyZW50Lm5vZGUpKSB7XG4gICAgICB0aGlzLnJlZnJlc2goKTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5zZXRDb250ZW50KG51bGwpO1xuICAgIH1cbiAgfVxuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbiAgcHJpdmF0ZSBfdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9sYWJzaGVsbDogSUxhYlNoZWxsO1xuICBwcml2YXRlIF9wbGFjZWhvbGRlcjogV2lkZ2V0O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBtb2R1bGUgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBIHR5cGUgYWxpYXMgZm9yIHRoZSBhY3Rpb25zIGEgcHJvcGVydHkgaW5zcGVjdG9yIGNhbiB0YWtlLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgUHJvcGVydHlJbnNwZWN0b3JBY3Rpb24gPSAnY29udGVudCcgfCAnZGlzcG9zZScgfCAnc2hvdy1wYW5lbCc7XG5cbiAgLyoqXG4gICAqIEFuIGltcGxlbWVudGF0aW9uIG9mIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgdXNlZCBieSB0aGVcbiAgICogcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLlxuICAgKi9cbiAgZXhwb3J0IGNsYXNzIFByb3BlcnR5SW5zcGVjdG9yIGltcGxlbWVudHMgSVByb3BlcnR5SW5zcGVjdG9yIHtcbiAgICAvKipcbiAgICAgKiBDb25zdHJ1Y3QgYSBuZXcgcHJvcGVydHkgaW5zcGVjdG9yLlxuICAgICAqL1xuICAgIGNvbnN0cnVjdG9yKG93bmVyOiBXaWRnZXQpIHtcbiAgICAgIHRoaXMuX293bmVyID0gb3duZXI7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIG93bmVyIHdpZGdldCBmb3IgdGhlIHByb3BlcnR5IGluc3BlY3Rvci5cbiAgICAgKi9cbiAgICBnZXQgb3duZXIoKTogV2lkZ2V0IHwgbnVsbCB7XG4gICAgICByZXR1cm4gdGhpcy5fb3duZXI7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGN1cnJlbnQgY29udGVudCBmb3IgdGhlIHByb3BlcnR5IGluc3BlY3Rvci5cbiAgICAgKi9cbiAgICBnZXQgY29udGVudCgpOiBXaWRnZXQgfCBudWxsIHtcbiAgICAgIHJldHVybiB0aGlzLl9jb250ZW50O1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIHByb3BlcnR5IGluc3BlY3RvciBpcyBkaXNwb3NlZC5cbiAgICAgKi9cbiAgICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIHVzZWQgZm9yIGFjdGlvbnMgcmVsYXRlZCB0byB0aGUgcHJvcGVydHkgaW5zcGVjdG9yLlxuICAgICAqL1xuICAgIGdldCBvbkFjdGlvbigpOiBJU2lnbmFsPFByb3BlcnR5SW5zcGVjdG9yLCBQcm9wZXJ0eUluc3BlY3RvckFjdGlvbj4ge1xuICAgICAgcmV0dXJuIHRoaXMuX29uQWN0aW9uO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFNob3cgdGhlIHByb3BlcnR5IGluc3BlY3RvciBwYW5lbC5cbiAgICAgKi9cbiAgICBzaG93UGFuZWwoKTogdm9pZCB7XG4gICAgICBpZiAodGhpcy5faXNEaXNwb3NlZCkge1xuICAgICAgICByZXR1cm47XG4gICAgICB9XG4gICAgICB0aGlzLl9vbkFjdGlvbi5lbWl0KCdzaG93LXBhbmVsJyk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVuZGVyIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgY29udGVudC5cbiAgICAgKi9cbiAgICByZW5kZXIod2lkZ2V0OiBXaWRnZXQgfCBSZWFjdC5SZWFjdEVsZW1lbnQpOiB2b2lkIHtcbiAgICAgIGlmICh0aGlzLl9pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGlmICh3aWRnZXQgaW5zdGFuY2VvZiBXaWRnZXQpIHtcbiAgICAgICAgdGhpcy5fY29udGVudCA9IHdpZGdldDtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIHRoaXMuX2NvbnRlbnQgPSBSZWFjdFdpZGdldC5jcmVhdGUod2lkZ2V0KTtcbiAgICAgIH1cbiAgICAgIHRoaXMuX29uQWN0aW9uLmVtaXQoJ2NvbnRlbnQnKTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBEaXNwb3NlIG9mIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IuXG4gICAgICovXG4gICAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICAgIGlmICh0aGlzLl9pc0Rpc3Bvc2VkKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgICAgdGhpcy5fY29udGVudCA9IG51bGw7XG4gICAgICB0aGlzLl9vd25lciA9IG51bGw7XG4gICAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICAgIH1cblxuICAgIHByaXZhdGUgX2lzRGlzcG9zZWQgPSBmYWxzZTtcbiAgICBwcml2YXRlIF9jb250ZW50OiBXaWRnZXQgfCBudWxsID0gbnVsbDtcbiAgICBwcml2YXRlIF9vd25lcjogV2lkZ2V0IHwgbnVsbCA9IG51bGw7XG4gICAgcHJpdmF0ZSBfb25BY3Rpb24gPSBuZXcgU2lnbmFsPFxuICAgICAgUHJvcGVydHlJbnNwZWN0b3IsXG4gICAgICBQcml2YXRlLlByb3BlcnR5SW5zcGVjdG9yQWN0aW9uXG4gICAgPih0aGlzKTtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5cbi8qKlxuICogQSBwcm9wZXJ0eSBpbnNwZWN0b3IgaW50ZXJmYWNlIHByb3ZpZGVkIHdoZW4gcmVnaXN0ZXJpbmdcbiAqIHRvIGEgcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLiAgQWxsb3dzIGFuIG93bmVyIHdpZGdldFxuICogdG8gc2V0IHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgY29udGVudCBmb3IgaXRzZWxmLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElQcm9wZXJ0eUluc3BlY3RvciBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLypcbiAgICogUmVuZGVyIHRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgY29udGVudC5cbiAgICpcbiAgICogSWYgdGhlIG93bmVyIHdpZGdldCBpcyBub3QgdGhlIG1vc3QgcmVjZW50bHkgZm9jdXNlZCxcbiAgICogVGhlIGNvbnRlbnQgd2lsbCBub3QgYmUgc2hvd24gdW50aWwgdGhhdCB3aWRnZXRcbiAgICogaXMgZm9jdXNlZC5cbiAgICpcbiAgICogQHBhcmFtIGNvbnRlbnQgLSB0aGUgd2lkZ2V0IG9yIHJlYWN0IGVsZW1lbnQgdG8gcmVuZGVyLlxuICAgKi9cbiAgcmVuZGVyKGNvbnRlbnQ6IFdpZGdldCB8IFJlYWN0LlJlYWN0RWxlbWVudCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIFNob3cgdGhlIHByb3BlcnR5IGluc3BlY3RvciBwYW5lbC5cbiAgICpcbiAgICogSWYgdGhlIG93bmVyIHdpZGdldCBpcyBub3QgdGhlIG1vc3QgcmVjZW50bHkgZm9jdXNlZCxcbiAgICogdGhpcyBpcyBhIG5vLW9wLiAgSXQgc2hvdWxkIGJlIHRyaWdnZXJlZCBieSBhIHVzZXJcbiAgICogYWN0aW9uLlxuICAgKi9cbiAgc2hvd1BhbmVsKCk6IHZvaWQ7XG59XG5cbi8qKlxuICogQSBwcm92aWRlciBmb3IgcHJvcGVydHkgaW5zcGVjdG9ycy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciB7XG4gIC8qKlxuICAgKiBSZWdpc3RlciBhIHdpZGdldCBpbiB0aGUgcHJvcGVydHkgaW5zcGVjdG9yIHByb3ZpZGVyLlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IFRoZSBvd25lciB3aWRnZXQgd2hvc2UgcHJvcGVydGllcyB3aWxsIGJlIGluc3BlY3RlZC5cbiAgICpcbiAgICogIyMgTm90ZXNcbiAgICogT25seSBvbmUgcHJvcGVydHkgaW5zcGVjdG9yIGNhbiBiZSBwcm92aWRlZCBmb3IgZWFjaCB3aWRnZXQuXG4gICAqIFJlZ2lzdGVyaW5nIHRoZSBzYW1lIHdpZGdldCB0d2ljZSB3aWxsIHJlc3VsdCBpbiBhbiBlcnJvci5cbiAgICogQSB3aWRnZXQgY2FuIGJlIHVucmVnaXN0ZXJlZCBieSBkaXNwb3Npbmcgb2YgaXRzIHByb3BlcnR5XG4gICAqIGluc3BlY3Rvci5cbiAgICovXG4gIHJlZ2lzdGVyKHdpZGdldDogV2lkZ2V0KTogSVByb3BlcnR5SW5zcGVjdG9yO1xufVxuXG4vKipcbiAqIFRoZSBwcm9wZXJ0eSBpbnNwZWN0b3IgcHJvdmlkZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlciA9IG5ldyBUb2tlbjxJUHJvcGVydHlJbnNwZWN0b3JQcm92aWRlcj4oXG4gICdAanVweXRlcmxhYi9wcm9wZXJ0eS1pbnNwZWN0b3I6SVByb3BlcnR5SW5zcGVjdG9yUHJvdmlkZXInLFxuICAnQSBzZXJ2aWNlIHRvIHJlZ2lzdHJ5IG5ldyB3aWRnZXQgaW4gdGhlIHByb3BlcnR5IGluc3BlY3RvciBzaWRlIHBhbmVsLidcbik7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=