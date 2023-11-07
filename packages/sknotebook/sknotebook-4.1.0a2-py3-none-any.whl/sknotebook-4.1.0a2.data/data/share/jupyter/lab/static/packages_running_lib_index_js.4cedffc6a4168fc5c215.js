"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_running_lib_index_js"],{

/***/ "../packages/running/lib/index.js":
/*!****************************************!*\
  !*** ../packages/running/lib/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IRunningSessionManagers": () => (/* binding */ IRunningSessionManagers),
/* harmony export */   "RunningSessionManagers": () => (/* binding */ RunningSessionManagers),
/* harmony export */   "RunningSessions": () => (/* binding */ RunningSessions)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module running
 */







/**
 * The class name added to a running widget.
 */
const RUNNING_CLASS = 'jp-RunningSessions';
/**
 * The class name added to the running terminal sessions section.
 */
const SECTION_CLASS = 'jp-RunningSessions-section';
/**
 * The class name added to a section container.
 */
const CONTAINER_CLASS = 'jp-RunningSessions-sectionContainer';
/**
 * The class name added to the running kernel sessions section list.
 */
const LIST_CLASS = 'jp-RunningSessions-sectionList';
/**
 * The class name added to the running sessions items.
 */
const ITEM_CLASS = 'jp-RunningSessions-item';
/**
 * The class name added to a running session item label.
 */
const ITEM_LABEL_CLASS = 'jp-RunningSessions-itemLabel';
/**
 * The class name added to a running session item detail.
 */
const ITEM_DETAIL_CLASS = 'jp-RunningSessions-itemDetail';
/**
 * The class name added to a running session item shutdown button.
 */
const SHUTDOWN_BUTTON_CLASS = 'jp-RunningSessions-itemShutdown';
/**
 * The class name added to a running session item shutdown button.
 */
const SHUTDOWN_ALL_BUTTON_CLASS = 'jp-RunningSessions-shutdownAll';
/**
 * The running sessions token.
 */
const IRunningSessionManagers = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.Token('@jupyterlab/running:IRunningSessionManagers', 'A service to add running session managers.');
class RunningSessionManagers {
    constructor() {
        this._added = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        this._managers = [];
    }
    /**
     * Signal emitted when a new manager is added.
     */
    get added() {
        return this._added;
    }
    /**
     * Add a running item manager.
     *
     * @param manager - The running item manager.
     *
     */
    add(manager) {
        this._managers.push(manager);
        this._added.emit(manager);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableDelegate(() => {
            const i = this._managers.indexOf(manager);
            if (i > -1) {
                this._managers.splice(i, 1);
            }
        });
    }
    /**
     * Return an iterator of launcher items.
     */
    items() {
        return this._managers;
    }
}
function Item(props) {
    var _a, _b;
    const { runningItem } = props;
    const classList = [ITEM_CLASS];
    const detail = (_a = runningItem.detail) === null || _a === void 0 ? void 0 : _a.call(runningItem);
    const icon = runningItem.icon();
    const title = runningItem.labelTitle ? runningItem.labelTitle() : '';
    const translator = props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    // Handle shutdown requests.
    let stopPropagation = false;
    const shutdownItemIcon = props.shutdownItemIcon || _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.closeIcon;
    const shutdownLabel = props.shutdownLabel || trans.__('Shut Down');
    const shutdown = () => {
        var _a;
        stopPropagation = true;
        (_a = runningItem.shutdown) === null || _a === void 0 ? void 0 : _a.call(runningItem);
    };
    // Manage collapsed state. Use the shutdown flag in lieu of `stopPropagation`.
    const [collapsed, collapse] = react__WEBPACK_IMPORTED_MODULE_6__.useState(false);
    const collapsible = !!((_b = runningItem.children) === null || _b === void 0 ? void 0 : _b.length);
    const onClick = collapsible
        ? () => !stopPropagation && collapse(!collapsed)
        : undefined;
    if (runningItem.className) {
        classList.push(runningItem.className);
    }
    if (props.child) {
        classList.push('jp-mod-running-child');
    }
    return (react__WEBPACK_IMPORTED_MODULE_6__.createElement(react__WEBPACK_IMPORTED_MODULE_6__.Fragment, null,
        react__WEBPACK_IMPORTED_MODULE_6__.createElement("li", null,
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: classList.join(' '), onClick: onClick, "data-context": runningItem.context || '' },
                collapsible &&
                    (collapsed ? (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretRightIcon.react, { tag: "span", stylesheet: "runningItem" })) : (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.caretDownIcon.react, { tag: "span", stylesheet: "runningItem" }))),
                typeof icon === 'string' ? (icon ? (react__WEBPACK_IMPORTED_MODULE_6__.createElement("img", { src: icon })) : undefined) : (react__WEBPACK_IMPORTED_MODULE_6__.createElement(icon.react, { tag: "span", stylesheet: "runningItem" })),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: ITEM_LABEL_CLASS, title: title, onClick: runningItem.open && (() => runningItem.open()) }, runningItem.label()),
                detail && react__WEBPACK_IMPORTED_MODULE_6__.createElement("span", { className: ITEM_DETAIL_CLASS }, detail),
                runningItem.shutdown && (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ToolbarButtonComponent, { className: SHUTDOWN_BUTTON_CLASS, icon: shutdownItemIcon, onClick: shutdown, tooltip: shutdownLabel }))),
            collapsible && !collapsed && (react__WEBPACK_IMPORTED_MODULE_6__.createElement(List, { child: true, runningItems: runningItem.children, shutdownItemIcon: shutdownItemIcon, translator: translator })))));
}
function List(props) {
    return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("ul", { className: LIST_CLASS }, props.runningItems.map((item, i) => (react__WEBPACK_IMPORTED_MODULE_6__.createElement(Item, { child: props.child, key: i, runningItem: item, shutdownLabel: props.shutdownLabel, shutdownItemIcon: props.shutdownItemIcon, translator: props.translator })))));
}
class ListWidget extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    constructor(_options) {
        super();
        this._options = _options;
        this._update = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(this);
        _options.manager.runningChanged.connect(this._emitUpdate, this);
    }
    dispose() {
        this._options.manager.runningChanged.disconnect(this._emitUpdate, this);
        super.dispose();
    }
    onBeforeShow(msg) {
        super.onBeforeShow(msg);
        this._update.emit();
    }
    render() {
        const options = this._options;
        let cached = true;
        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.UseSignal, { signal: this._update }, () => {
            // Cache the running items for the intial load and request from
            // the service every subsequent load.
            if (cached) {
                cached = false;
            }
            else {
                options.runningItems = options.manager.running();
            }
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: CONTAINER_CLASS },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement(List, { runningItems: options.runningItems, shutdownLabel: options.manager.shutdownLabel, shutdownAllLabel: options.shutdownAllLabel, shutdownItemIcon: options.manager.shutdownItemIcon, translator: options.translator })));
        }));
    }
    /**
     * Check if the widget or any of it's parents is hidden.
     *
     * Checking parents is necessary as lumino does not propagate visibility
     * changes from parents down to children (although it does notify parents
     * about changes to children visibility).
     */
    _isAnyHidden() {
        let isHidden = this.isHidden;
        if (isHidden) {
            return isHidden;
        }
        let parent = this.parent;
        while (parent != null) {
            if (parent.isHidden) {
                isHidden = true;
                break;
            }
            parent = parent.parent;
        }
        return isHidden;
    }
    _emitUpdate() {
        if (this._isAnyHidden()) {
            return;
        }
        this._update.emit();
    }
}
/**
 * The Section component contains the shared look and feel for an interactive
 * list of kernels and sessions.
 *
 * It is specialized for each based on its props.
 */
class Section extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.PanelWithToolbar {
    constructor(options) {
        super();
        this._manager = options.manager;
        const translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const shutdownAllLabel = options.manager.shutdownAllLabel || trans.__('Shut Down All');
        const shutdownTitle = `${shutdownAllLabel}?`;
        const shutdownAllConfirmationText = options.manager.shutdownAllConfirmationText ||
            `${shutdownAllLabel} ${options.manager.name}`;
        this.addClass(SECTION_CLASS);
        this.title.label = options.manager.name;
        function onShutdown() {
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: shutdownTitle,
                body: shutdownAllConfirmationText,
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton(),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: shutdownAllLabel })
                ]
            }).then(result => {
                if (result.button.accept) {
                    options.manager.shutdownAll();
                }
            });
        }
        let runningItems = options.manager.running();
        const enabled = runningItems.length > 0;
        this._button = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            label: shutdownAllLabel,
            className: `${SHUTDOWN_ALL_BUTTON_CLASS} jp-mod-styled ${!enabled && 'jp-mod-disabled'}`,
            enabled,
            onClick: onShutdown
        });
        this._manager.runningChanged.connect(this._updateButton, this);
        this.toolbar.addItem('shutdown-all', this._button);
        this.addWidget(new ListWidget({ runningItems, shutdownAllLabel, ...options }));
    }
    /**
     * Dispose the resources held by the widget
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._manager.runningChanged.disconnect(this._updateButton, this);
        super.dispose();
    }
    _updateButton() {
        var _a, _b;
        const button = this._button;
        button.enabled = this._manager.running().length > 0;
        if (button.enabled) {
            (_a = button.node.querySelector('button')) === null || _a === void 0 ? void 0 : _a.classList.remove('jp-mod-disabled');
        }
        else {
            (_b = button.node.querySelector('button')) === null || _b === void 0 ? void 0 : _b.classList.add('jp-mod-disabled');
        }
    }
}
/**
 * A class that exposes the running terminal and kernel sessions.
 */
class RunningSessions extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.SidePanel {
    /**
     * Construct a new running widget.
     */
    constructor(managers, translator) {
        super();
        this.managers = managers;
        this.translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = this.translator.load('jupyterlab');
        this.addClass(RUNNING_CLASS);
        this.toolbar.addItem('refresh', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.ToolbarButton({
            tooltip: trans.__('Refresh List'),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.refreshIcon,
            onClick: () => managers.items().forEach(manager => manager.refreshRunning())
        }));
        managers.items().forEach(manager => this.addSection(managers, manager));
        managers.added.connect(this.addSection, this);
    }
    /**
     * Dispose the resources held by the widget
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.managers.added.disconnect(this.addSection, this);
        super.dispose();
    }
    /**
     * Add a section for a new manager.
     *
     * @param managers Managers
     * @param manager New manager
     */
    addSection(_, manager) {
        this.addWidget(new Section({ manager, translator: this.translator }));
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfcnVubmluZ19saWJfaW5kZXhfanMuNGNlZGZmYzZhNDE2OGZjNWMyMTUuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQUV1RDtBQUNZO0FBYW5DO0FBQ087QUFDMkI7QUFFakI7QUFFckI7QUFFL0I7O0dBRUc7QUFDSCxNQUFNLGFBQWEsR0FBRyxvQkFBb0IsQ0FBQztBQUUzQzs7R0FFRztBQUNILE1BQU0sYUFBYSxHQUFHLDRCQUE0QixDQUFDO0FBRW5EOztHQUVHO0FBQ0gsTUFBTSxlQUFlLEdBQUcscUNBQXFDLENBQUM7QUFFOUQ7O0dBRUc7QUFDSCxNQUFNLFVBQVUsR0FBRyxnQ0FBZ0MsQ0FBQztBQUVwRDs7R0FFRztBQUNILE1BQU0sVUFBVSxHQUFHLHlCQUF5QixDQUFDO0FBRTdDOztHQUVHO0FBQ0gsTUFBTSxnQkFBZ0IsR0FBRyw4QkFBOEIsQ0FBQztBQUV4RDs7R0FFRztBQUNILE1BQU0saUJBQWlCLEdBQUcsK0JBQStCLENBQUM7QUFFMUQ7O0dBRUc7QUFDSCxNQUFNLHFCQUFxQixHQUFHLGlDQUFpQyxDQUFDO0FBRWhFOztHQUVHO0FBQ0gsTUFBTSx5QkFBeUIsR0FBRyxnQ0FBZ0MsQ0FBQztBQUVuRTs7R0FFRztBQUNJLE1BQU0sdUJBQXVCLEdBQUcsSUFBSSxvREFBSyxDQUM5Qyw2Q0FBNkMsRUFDN0MsNENBQTRDLENBQzdDLENBQUM7QUF5QkssTUFBTSxzQkFBc0I7SUFBbkM7UUFpQ1UsV0FBTSxHQUFHLElBQUkscURBQU0sQ0FBa0MsSUFBSSxDQUFDLENBQUM7UUFDM0QsY0FBUyxHQUFnQyxFQUFFLENBQUM7SUFDdEQsQ0FBQztJQWxDQzs7T0FFRztJQUNILElBQUksS0FBSztRQUNQLE9BQU8sSUFBSSxDQUFDLE1BQU0sQ0FBQztJQUNyQixDQUFDO0lBRUQ7Ozs7O09BS0c7SUFDSCxHQUFHLENBQUMsT0FBa0M7UUFDcEMs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eEUsUUFBUSxDQUFDLEtBQUssQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLFVBQVUsRUFBRSxJQUFJLENBQUMsQ0FBQztJQUNoRCxDQUFDO0lBRUQ7O09BRUc7SUFDSCxPQUFPO1FBQ0wsSUFBSSxJQUFJLENBQUMsVUFBVSxFQUFFO1lBQ25CLE9BQU87U0FDUjtRQUNELElBQUksQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLFVBQVUsQ0FBQyxJQUFJLENBQUMsVUFBVSxFQUFFLElBQUksQ0FBQyxDQUFDO1FBQ3RELEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQztJQUNsQixDQUFDO0lBRUQ7Ozs7O09BS0c7SUFDTyxVQUFVLENBQUMsQ0FBVSxFQUFFLE9BQWtDO1FBQ2pFLElBQUksQ0FBQyxTQUFTLENBQUMsSUFBSSxPQUFPLENBQUMsRUFBRSxPQUFPLEVBQUUsVUFBVSxFQUFFLElBQUksQ0FBQyxVQUFVLEVBQUUsQ0FBQyxDQUFDLENBQUM7SUFDeEUsQ0FBQztDQUlGIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3J1bm5pbmcvc3JjL2luZGV4LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBydW5uaW5nXG4gKi9cblxuaW1wb3J0IHsgRGlhbG9nLCBzaG93RGlhbG9nIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIG51bGxUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgY2FyZXREb3duSWNvbixcbiAgY2FyZXRSaWdodEljb24sXG4gIGNsb3NlSWNvbixcbiAgTGFiSWNvbixcbiAgUGFuZWxXaXRoVG9vbGJhcixcbiAgUmVhY3RXaWRnZXQsXG4gIHJlZnJlc2hJY29uLFxuICBTaWRlUGFuZWwsXG4gIFRvb2xiYXJCdXR0b24sXG4gIFRvb2xiYXJCdXR0b25Db21wb25lbnQsXG4gIFVzZVNpZ25hbFxufSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRGlzcG9zYWJsZURlbGVnYXRlLCBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIHJ1bm5pbmcgd2lkZ2V0LlxuICovXG5jb25zdCBSVU5OSU5HX0NMQVNTID0gJ2pwLVJ1bm5pbmdTZXNzaW9ucyc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gdGhlIHJ1bm5pbmcgdGVybWluYWwgc2Vzc2lvbnMgc2VjdGlvbi5cbiAqL1xuY29uc3QgU0VDVElPTl9DTEFTUyA9ICdqcC1SdW5uaW5nU2Vzc2lvbnMtc2VjdGlvbic7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYSBzZWN0aW9uIGNvbnRhaW5lci5cbiAqL1xuY29uc3QgQ09OVEFJTkVSX0NMQVNTID0gJ2pwLVJ1bm5pbmdTZXNzaW9ucy1zZWN0aW9uQ29udGFpbmVyJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byB0aGUgcnVubmluZyBrZXJuZWwgc2Vzc2lvbnMgc2VjdGlvbiBsaXN0LlxuICovXG5jb25zdCBMSVNUX0NMQVNTID0gJ2pwLVJ1bm5pbmdTZXNzaW9ucy1zZWN0aW9uTGlzdCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gdGhlIHJ1bm5pbmcgc2Vzc2lvbnMgaXRlbXMuXG4gKi9cbmNvbnN0IElURU1fQ0xBU1MgPSAnanAtUnVubmluZ1Nlc3Npb25zLWl0ZW0nO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgcnVubmluZyBzZXNzaW9uIGl0ZW0gbGFiZWwuXG4gKi9cbmNvbnN0IElURU1fTEFCRUxfQ0xBU1MgPSAnanAtUnVubmluZ1Nlc3Npb25zLWl0ZW1MYWJlbCc7XG5cbi8qKlxuICogVGhlIGNsYXNzIG5hbWUgYWRkZWQgdG8gYSBydW5uaW5nIHNlc3Npb24gaXRlbSBkZXRhaWwuXG4gKi9cbmNvbnN0IElURU1fREVUQUlMX0NMQVNTID0gJ2pwLVJ1bm5pbmdTZXNzaW9ucy1pdGVtRGV0YWlsJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBhIHJ1bm5pbmcgc2Vzc2lvbiBpdGVtIHNodXRkb3duIGJ1dHRvbi5cbiAqL1xuY29uc3QgU0hVVERPV05fQlVUVE9OX0NMQVNTID0gJ2pwLVJ1bm5pbmdTZXNzaW9ucy1pdGVtU2h1dGRvd24nO1xuXG4vKipcbiAqIFRoZSBjbGFzcyBuYW1lIGFkZGVkIHRvIGEgcnVubmluZyBzZXNzaW9uIGl0ZW0gc2h1dGRvd24gYnV0dG9uLlxuICovXG5jb25zdCBTSFVURE9XTl9BTExfQlVUVE9OX0NMQVNTID0gJ2pwLVJ1bm5pbmdTZXNzaW9ucy1zaHV0ZG93bkFsbCc7XG5cbi8qKlxuICogVGhlIHJ1bm5pbmcgc2Vzc2lvbnMgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycyA9IG5ldyBUb2tlbjxJUnVubmluZ1Nlc3Npb25NYW5hZ2Vycz4oXG4gICdAanVweXRlcmxhYi9ydW5uaW5nOklSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzJyxcbiAgJ0Egc2VydmljZSB0byBhZGQgcnVubmluZyBzZXNzaW9uIG1hbmFnZXJzLidcbik7XG5cbi8qKlxuICogVGhlIHJ1bm5pbmcgaW50ZXJmYWNlLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzIHtcbiAgLyoqXG4gICAqIEFkZCBhIHJ1bm5pbmcgaXRlbSBtYW5hZ2VyLlxuICAgKlxuICAgKiBAcGFyYW0gbWFuYWdlciAtIFRoZSBydW5uaW5nIGl0ZW0gbWFuYWdlci5cbiAgICpcbiAgICovXG4gIGFkZChtYW5hZ2VyOiBJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyKTogSURpc3Bvc2FibGU7XG5cbiAgLyoqXG4gICAqIFNpZ25hbCBlbWl0dGVkIHdoZW4gYSBuZXcgbWFuYWdlciBpcyBhZGRlZC5cbiAgICovXG4gIGFkZGVkOiBJU2lnbmFsPElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLCBJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyPjtcblxuICAvKipcbiAgICogUmV0dXJuIGFuIGFycmF5IG9mIG1hbmFnZXJzLlxuICAgKi9cbiAgaXRlbXMoKTogUmVhZG9ubHlBcnJheTxJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyPjtcbn1cblxuZXhwb3J0IGNsYXNzIFJ1bm5pbmdTZXNzaW9uTWFuYWdlcnMgaW1wbGVtZW50cyBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycyB7XG4gIC8qKlxuICAgKiBTaWduYWwgZW1pdHRlZCB3aGVuIGEgbmV3IG1hbmFnZXIgaXMgYWRkZWQuXG4gICAqL1xuICBnZXQgYWRkZWQoKTogSVNpZ25hbDx0aGlzLCBJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyPiB7XG4gICAgcmV0dXJuIHRoaXMuX2FkZGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIHJ1bm5pbmcgaXRlbSBtYW5hZ2VyLlxuICAgKlxuICAgKiBAcGFyYW0gbWFuYWdlciAtIFRoZSBydW5uaW5nIGl0ZW0gbWFuYWdlci5cbiAgICpcbiAgICovXG4gIGFkZChtYW5hZ2VyOiBJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyKTogSURpc3Bvc2FibGUge1xuICAgIHRoaXMuX21hbmFnZXJzLnB1c2gobWFuYWdlcik7XG4gICAgdGhpcy5fYWRkZWQuZW1pdChtYW5hZ2VyKTtcbiAgICByZXR1cm4gbmV3IERpc3Bvc2FibGVEZWxlZ2F0ZSgoKSA9PiB7XG4gICAgICBjb25zdCBpID0gdGhpcy5fbWFuYWdlcnMuaW5kZXhPZihtYW5hZ2VyKTtcblxuICAgICAgaWYgKGkgPiAtMSkge1xuICAgICAgICB0aGlzLl9tYW5hZ2Vycy5zcGxpY2UoaSwgMSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJuIGFuIGl0ZXJhdG9yIG9mIGxhdW5jaGVyIGl0ZW1zLlxuICAgKi9cbiAgaXRlbXMoKTogUmVhZG9ubHlBcnJheTxJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyPiB7XG4gICAgcmV0dXJuIHRoaXMuX21hbmFnZXJzO1xuICB9XG5cbiAgcHJpdmF0ZSBfYWRkZWQgPSBuZXcgU2lnbmFsPHRoaXMsIElSdW5uaW5nU2Vzc2lvbnMuSU1hbmFnZXI+KHRoaXMpO1xuICBwcml2YXRlIF9tYW5hZ2VyczogSVJ1bm5pbmdTZXNzaW9ucy5JTWFuYWdlcltdID0gW107XG59XG5cbmZ1bmN0aW9uIEl0ZW0ocHJvcHM6IHtcbiAgY2hpbGQ/OiBib29sZWFuO1xuICBydW5uaW5nSXRlbTogSVJ1bm5pbmdTZXNzaW9ucy5JUnVubmluZ0l0ZW07XG4gIHNodXRkb3duTGFiZWw/OiBzdHJpbmc7XG4gIHNodXRkb3duSXRlbUljb24/OiBMYWJJY29uO1xuICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG59KSB7XG4gIGNvbnN0IHsgcnVubmluZ0l0ZW0gfSA9IHByb3BzO1xuICBjb25zdCBjbGFzc0xpc3QgPSBbSVRFTV9DTEFTU107XG4gIGNvbnN0IGRldGFpbCA9IHJ1bm5pbmdJdGVtLmRldGFpbD8uKCk7XG4gIGNvbnN0IGljb24gPSBydW5uaW5nSXRlbS5pY29uKCk7XG4gIGNvbnN0IHRpdGxlID0gcnVubmluZ0l0ZW0ubGFiZWxUaXRsZSA/IHJ1bm5pbmdJdGVtLmxhYmVsVGl0bGUoKSA6ICcnO1xuICBjb25zdCB0cmFuc2xhdG9yID0gcHJvcHMudHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAvLyBIYW5kbGUgc2h1dGRvd24gcmVxdWVzdHMuXG4gIGxldCBzdG9wUHJvcGFnYXRpb24gPSBmYWxzZTtcbiAgY29uc3Qgc2h1dGRvd25JdGVtSWNvbiA9IHByb3BzLnNodXRkb3duSXRlbUljb24gfHwgY2xvc2VJY29uO1xuICBjb25zdCBzaHV0ZG93bkxhYmVsID0gcHJvcHMuc2h1dGRvd25MYWJlbCB8fCB0cmFucy5fXygnU2h1dCBEb3duJyk7XG4gIGNvbnN0IHNodXRkb3duID0gKCkgPT4ge1xuICAgIHN0b3BQcm9wYWdhdGlvbiA9IHRydWU7XG4gICAgcnVubmluZ0l0ZW0uc2h1dGRvd24/LigpO1xuICB9O1xuXG4gIC8vIE1hbmFnZSBjb2xsYXBzZWQgc3RhdGUuIFVzZSB0aGUgc2h1dGRvd24gZmxhZyBpbiBsaWV1IG9mIGBzdG9wUHJvcGFnYXRpb25gLlxuICBjb25zdCBbY29sbGFwc2VkLCBjb2xsYXBzZV0gPSBSZWFjdC51c2VTdGF0ZShmYWxzZSk7XG4gIGNvbnN0IGNvbGxhcHNpYmxlID0gISFydW5uaW5nSXRlbS5jaGlsZHJlbj8ubGVuZ3RoO1xuICBjb25zdCBvbkNsaWNrID0gY29sbGFwc2libGVcbiAgICA/ICgpID0+ICFzdG9wUHJvcGFnYXRpb24gJiYgY29sbGFwc2UoIWNvbGxhcHNlZClcbiAgICA6IHVuZGVmaW5lZDtcblxuICBpZiAocnVubmluZ0l0ZW0uY2xhc3NOYW1lKSB7XG4gICAgY2xhc3NMaXN0LnB1c2gocnVubmluZ0l0ZW0uY2xhc3NOYW1lKTtcbiAgfVxuICBpZiAocHJvcHMuY2hpbGQpIHtcbiAgICBjbGFzc0xpc3QucHVzaCgnanAtbW9kLXJ1bm5pbmctY2hpbGQnKTtcbiAgfVxuXG4gIHJldHVybiAoXG4gICAgPD5cbiAgICAgIDxsaT5cbiAgICAgICAgPGRpdlxuICAgICAgICAgIGNsYXNzTmFtZT17Y2xhc3NMaXN0LmpvaW4oJyAnKX1cbiAgICAgICAgICBvbkNsaWNrPXtvbkNsaWNrfVxuICAgICAgICAgIGRhdGEtY29udGV4dD17cnVubmluZ0l0ZW0uY29udGV4dCB8fCAnJ31cbiAgICAgICAgPlxuICAgICAgICAgIHtjb2xsYXBzaWJsZSAmJlxuICAgICAgICAgICAgKGNvbGxhcHNlZCA/IChcbiAgICAgICAgICAgICAgPGNhcmV0UmlnaHRJY29uLnJlYWN0IHRhZz1cInNwYW5cIiBzdHlsZXNoZWV0PVwicnVubmluZ0l0ZW1cIiAvPlxuICAgICAgICAgICAgKSA6IChcbiAgICAgICAgICAgICAgPGNhcmV0RG93bkljb24ucmVhY3QgdGFnPVwic3BhblwiIHN0eWxlc2hlZXQ9XCJydW5uaW5nSXRlbVwiIC8+XG4gICAgICAgICAgICApKX1cbiAgICAgICAgICB7dHlwZW9mIGljb24gPT09ICdzdHJpbmcnID8gKFxuICAgICAgICAgICAgaWNvbiA/IChcbiAgICAgICAgICAgICAgPGltZyBzcmM9e2ljb259IC8+XG4gICAgICAgICAgICApIDogdW5kZWZpbmVkXG4gICAgICAgICAgKSA6IChcbiAgICAgICAgICAgIDxpY29uLnJlYWN0IHRhZz1cInNwYW5cIiBzdHlsZXNoZWV0PVwicnVubmluZ0l0ZW1cIiAvPlxuICAgICAgICAgICl9XG4gICAgICAgICAgPHNwYW5cbiAgICAgICAgICAgIGNsYXNzTmFtZT17SVRFTV9MQUJFTF9DTEFTU31cbiAgICAgICAgICAgIHRpdGxlPXt0aXRsZX1cbiAgICAgICAgICAgIG9uQ2xpY2s9e3J1bm5pbmdJdGVtLm9wZW4gJiYgKCgpID0+IHJ1bm5pbmdJdGVtLm9wZW4hKCkpfVxuICAgICAgICAgID5cbiAgICAgICAgICAgIHtydW5uaW5nSXRlbS5sYWJlbCgpfVxuICAgICAgICAgIDwvc3Bhbj5cbiAgICAgICAgICB7ZGV0YWlsICYmIDxzcGFuIGNsYXNzTmFtZT17SVRFTV9ERVRBSUxfQ0xBU1N9PntkZXRhaWx9PC9zcGFuPn1cbiAgICAgICAgICB7cnVubmluZ0l0ZW0uc2h1dGRvd24gJiYgKFxuICAgICAgICAgICAgPFRvb2xiYXJCdXR0b25Db21wb25lbnRcbiAgICAgICAgICAgICAgY2xhc3NOYW1lPXtTSFVURE9XTl9CVVRUT05fQ0xBU1N9XG4gICAgICAgICAgICAgIGljb249e3NodXRkb3duSXRlbUljb259XG4gICAgICAgICAgICAgIG9uQ2xpY2s9e3NodXRkb3dufVxuICAgICAgICAgICAgICB0b29sdGlwPXtzaHV0ZG93bkxhYmVsfVxuICAgICAgICAgICAgLz5cbiAgICAgICAgICApfVxuICAgICAgICA8L2Rpdj5cbiAgICAgICAge2NvbGxhcHNpYmxlICYmICFjb2xsYXBzZWQgJiYgKFxuICAgICAgICAgIDxMaXN0XG4gICAgICAgICAgICBjaGlsZD17dHJ1ZX1cbiAgICAgICAgICAgIHJ1bm5pbmdJdGVtcz17cnVubmluZ0l0ZW0uY2hpbGRyZW4hfVxuICAgICAgICAgICAgc2h1dGRvd25JdGVtSWNvbj17c2h1dGRvd25JdGVtSWNvbn1cbiAgICAgICAgICAgIHRyYW5zbGF0b3I9e3RyYW5zbGF0b3J9XG4gICAgICAgICAgLz5cbiAgICAgICAgKX1cbiAgICAgIDwvbGk+XG4gICAgPC8+XG4gICk7XG59XG5cbmZ1bmN0aW9uIExpc3QocHJvcHM6IHtcbiAgY2hpbGQ/OiBib29sZWFuO1xuICBydW5uaW5nSXRlbXM6IElSdW5uaW5nU2Vzc2lvbnMuSVJ1bm5pbmdJdGVtW107XG4gIHNodXRkb3duTGFiZWw/OiBzdHJpbmc7XG4gIHNodXRkb3duQWxsTGFiZWw/OiBzdHJpbmc7XG4gIHNodXRkb3duSXRlbUljb24/OiBMYWJJY29uO1xuICB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3I7XG59KSB7XG4gIHJldHVybiAoXG4gICAgPHVsIGNsYXNzTmFtZT17TElTVF9DTEFTU30+XG4gICAgICB7cHJvcHMucnVubmluZ0l0ZW1zLm1hcCgoaXRlbSwgaSkgPT4gKFxuICAgICAgICA8SXRlbVxuICAgICAgICAgIGNoaWxkPXtwcm9wcy5jaGlsZH1cbiAgICAgICAgICBrZXk9e2l9XG4gICAgICAgICAgcnVubmluZ0l0ZW09e2l0ZW19XG4gICAgICAgICAgc2h1dGRvd25MYWJlbD17cHJvcHMuc2h1dGRvd25MYWJlbH1cbiAgICAgICAgICBzaHV0ZG93bkl0ZW1JY29uPXtwcm9wcy5zaHV0ZG93bkl0ZW1JY29ufVxuICAgICAgICAgIHRyYW5zbGF0b3I9e3Byb3BzLnRyYW5zbGF0b3J9XG4gICAgICAgIC8+XG4gICAgICApKX1cbiAgICA8L3VsPlxuICApO1xufVxuXG5jbGFzcyBMaXN0V2lkZ2V0IGV4dGVuZHMgUmVhY3RXaWRnZXQge1xuICBjb25zdHJ1Y3RvcihcbiAgICBwcml2YXRlIF9vcHRpb25zOiB7XG4gICAgICBtYW5hZ2VyOiBJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyO1xuICAgICAgcnVubmluZ0l0ZW1zOiBJUnVubmluZ1Nlc3Npb25zLklSdW5uaW5nSXRlbVtdO1xuICAgICAgc2h1dGRvd25BbGxMYWJlbDogc3RyaW5nO1xuICAgICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICAgIH1cbiAgKSB7XG4gICAgc3VwZXIoKTtcbiAgICBfb3B0aW9ucy5tYW5hZ2VyLnJ1bm5pbmdDaGFuZ2VkLmNvbm5lY3QodGhpcy5fZW1pdFVwZGF0ZSwgdGhpcyk7XG4gIH1cblxuICBkaXNwb3NlKCkge1xuICAgIHRoaXMuX29wdGlvbnMubWFuYWdlci5ydW5uaW5nQ2hhbmdlZC5kaXNjb25uZWN0KHRoaXMuX2VtaXRVcGRhdGUsIHRoaXMpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIHByb3RlY3RlZCBvbkJlZm9yZVNob3cobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgc3VwZXIub25CZWZvcmVTaG93KG1zZyk7XG4gICAgdGhpcy5fdXBkYXRlLmVtaXQoKTtcbiAgfVxuXG4gIHJlbmRlcigpOiBKU1guRWxlbWVudCB7XG4gICAgY29uc3Qgb3B0aW9ucyA9IHRoaXMuX29wdGlvbnM7XG4gICAgbGV0IGNhY2hlZCA9IHRydWU7XG4gICAgcmV0dXJuIChcbiAgICAgIDxVc2VTaWduYWwgc2lnbmFsPXt0aGlzLl91cGRhdGV9PlxuICAgICAgICB7KCkgPT4ge1xuICAgICAgICAgIC8vIENhY2hlIHRoZSBydW5uaW5nIGl0ZW1zIGZvciB0aGUgaW50aWFsIGxvYWQgYW5kIHJlcXVlc3QgZnJvbVxuICAgICAgICAgIC8vIHRoZSBzZXJ2aWNlIGV2ZXJ5IHN1YnNlcXVlbnQgbG9hZC5cbiAgICAgICAgICBpZiAoY2FjaGVkKSB7XG4gICAgICAgICAgICBjYWNoZWQgPSBmYWxzZTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgb3B0aW9ucy5ydW5uaW5nSXRlbXMgPSBvcHRpb25zLm1hbmFnZXIucnVubmluZygpO1xuICAgICAgICAgIH1cbiAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9e0NPTlRBSU5FUl9DTEFTU30+XG4gICAgICAgICAgICAgIDxMaXN0XG4gICAgICAgICAgICAgICAgcnVubmluZ0l0ZW1zPXtvcHRpb25zLnJ1bm5pbmdJdGVtc31cbiAgICAgICAgICAgICAgICBzaHV0ZG93bkxhYmVsPXtvcHRpb25zLm1hbmFnZXIuc2h1dGRvd25MYWJlbH1cbiAgICAgICAgICAgICAgICBzaHV0ZG93bkFsbExhYmVsPXtvcHRpb25zLnNodXRkb3duQWxsTGFiZWx9XG4gICAgICAgICAgICAgICAgc2h1dGRvd25JdGVtSWNvbj17b3B0aW9ucy5tYW5hZ2VyLnNodXRkb3duSXRlbUljb259XG4gICAgICAgICAgICAgICAgdHJhbnNsYXRvcj17b3B0aW9ucy50cmFuc2xhdG9yfVxuICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgKTtcbiAgICAgICAgfX1cbiAgICAgIDwvVXNlU2lnbmFsPlxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQ2hlY2sgaWYgdGhlIHdpZGdldCBvciBhbnkgb2YgaXQncyBwYXJlbnRzIGlzIGhpZGRlbi5cbiAgICpcbiAgICogQ2hlY2tpbmcgcGFyZW50cyBpcyBuZWNlc3NhcnkgYXMgbHVtaW5vIGRvZXMgbm90IHByb3BhZ2F0ZSB2aXNpYmlsaXR5XG4gICAqIGNoYW5nZXMgZnJvbSBwYXJlbnRzIGRvd24gdG8gY2hpbGRyZW4gKGFsdGhvdWdoIGl0IGRvZXMgbm90aWZ5IHBhcmVudHNcbiAgICogYWJvdXQgY2hhbmdlcyB0byBjaGlsZHJlbiB2aXNpYmlsaXR5KS5cbiAgICovXG4gIHByaXZhdGUgX2lzQW55SGlkZGVuKCkge1xuICAgIGxldCBpc0hpZGRlbiA9IHRoaXMuaXNIaWRkZW47XG4gICAgaWYgKGlzSGlkZGVuKSB7XG4gICAgICByZXR1cm4gaXNIaWRkZW47XG4gICAgfVxuICAgIGxldCBwYXJlbnQ6IFdpZGdldCB8IG51bGwgPSB0aGlzLnBhcmVudDtcbiAgICB3aGlsZSAocGFyZW50ICE9IG51bGwpIHtcbiAgICAgIGlmIChwYXJlbnQuaXNIaWRkZW4pIHtcbiAgICAgICAgaXNIaWRkZW4gPSB0cnVlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICAgIHBhcmVudCA9IHBhcmVudC5wYXJlbnQ7XG4gICAgfVxuICAgIHJldHVybiBpc0hpZGRlbjtcbiAgfVxuXG4gIHByaXZhdGUgX2VtaXRVcGRhdGUoKSB7XG4gICAgaWYgKHRoaXMuX2lzQW55SGlkZGVuKCkpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fdXBkYXRlLmVtaXQoKTtcbiAgfVxuXG4gIHByaXZhdGUgX3VwZGF0ZTogU2lnbmFsPExpc3RXaWRnZXQsIHZvaWQ+ID0gbmV3IFNpZ25hbCh0aGlzKTtcbn1cblxuLyoqXG4gKiBUaGUgU2VjdGlvbiBjb21wb25lbnQgY29udGFpbnMgdGhlIHNoYXJlZCBsb29rIGFuZCBmZWVsIGZvciBhbiBpbnRlcmFjdGl2ZVxuICogbGlzdCBvZiBrZXJuZWxzIGFuZCBzZXNzaW9ucy5cbiAqXG4gKiBJdCBpcyBzcGVjaWFsaXplZCBmb3IgZWFjaCBiYXNlZCBvbiBpdHMgcHJvcHMuXG4gKi9cbmNsYXNzIFNlY3Rpb24gZXh0ZW5kcyBQYW5lbFdpdGhUb29sYmFyIHtcbiAgY29uc3RydWN0b3Iob3B0aW9uczoge1xuICAgIG1hbmFnZXI6IElSdW5uaW5nU2Vzc2lvbnMuSU1hbmFnZXI7XG4gICAgdHJhbnNsYXRvcj86IElUcmFuc2xhdG9yO1xuICB9KSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9tYW5hZ2VyID0gb3B0aW9ucy5tYW5hZ2VyO1xuICAgIGNvbnN0IHRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgICBjb25zdCBzaHV0ZG93bkFsbExhYmVsID1cbiAgICAgIG9wdGlvbnMubWFuYWdlci5zaHV0ZG93bkFsbExhYmVsIHx8IHRyYW5zLl9fKCdTaHV0IERvd24gQWxsJyk7XG4gICAgY29uc3Qgc2h1dGRvd25UaXRsZSA9IGAke3NodXRkb3duQWxsTGFiZWx9P2A7XG4gICAgY29uc3Qgc2h1dGRvd25BbGxDb25maXJtYXRpb25UZXh0ID1cbiAgICAgIG9wdGlvbnMubWFuYWdlci5zaHV0ZG93bkFsbENvbmZpcm1hdGlvblRleHQgfHxcbiAgICAgIGAke3NodXRkb3duQWxsTGFiZWx9ICR7b3B0aW9ucy5tYW5hZ2VyLm5hbWV9YDtcblxuICAgIHRoaXMuYWRkQ2xhc3MoU0VDVElPTl9DTEFTUyk7XG4gICAgdGhpcy50aXRsZS5sYWJlbCA9IG9wdGlvbnMubWFuYWdlci5uYW1lO1xuXG4gICAgZnVuY3Rpb24gb25TaHV0ZG93bigpIHtcbiAgICAgIHZvaWQgc2hvd0RpYWxvZyh7XG4gICAgICAgIHRpdGxlOiBzaHV0ZG93blRpdGxlLFxuICAgICAgICBib2R5OiBzaHV0ZG93bkFsbENvbmZpcm1hdGlvblRleHQsXG4gICAgICAgIGJ1dHRvbnM6IFtcbiAgICAgICAgICBEaWFsb2cuY2FuY2VsQnV0dG9uKCksXG4gICAgICAgICAgRGlhbG9nLndhcm5CdXR0b24oeyBsYWJlbDogc2h1dGRvd25BbGxMYWJlbCB9KVxuICAgICAgICBdXG4gICAgICB9KS50aGVuKHJlc3VsdCA9PiB7XG4gICAgICAgIGlmIChyZXN1bHQuYnV0dG9uLmFjY2VwdCkge1xuICAgICAgICAgIG9wdGlvbnMubWFuYWdlci5zaHV0ZG93bkFsbCgpO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG5cbiAgICBsZXQgcnVubmluZ0l0ZW1zID0gb3B0aW9ucy5tYW5hZ2VyLnJ1bm5pbmcoKTtcbiAgICBjb25zdCBlbmFibGVkID0gcnVubmluZ0l0ZW1zLmxlbmd0aCA+IDA7XG4gICAgdGhpcy5fYnV0dG9uID0gbmV3IFRvb2xiYXJCdXR0b24oe1xuICAgICAgbGFiZWw6IHNodXRkb3duQWxsTGFiZWwsXG4gICAgICBjbGFzc05hbWU6IGAke1NIVVRET1dOX0FMTF9CVVRUT05fQ0xBU1N9IGpwLW1vZC1zdHlsZWQgJHtcbiAgICAgICAgIWVuYWJsZWQgJiYgJ2pwLW1vZC1kaXNhYmxlZCdcbiAgICAgIH1gLFxuICAgICAgZW5hYmxlZCxcbiAgICAgIG9uQ2xpY2s6IG9uU2h1dGRvd25cbiAgICB9KTtcbiAgICB0aGlzLl9tYW5hZ2VyLnJ1bm5pbmdDaGFuZ2VkLmNvbm5lY3QodGhpcy5fdXBkYXRlQnV0dG9uLCB0aGlzKTtcblxuICAgIHRoaXMudG9vbGJhci5hZGRJdGVtKCdzaHV0ZG93bi1hbGwnLCB0aGlzLl9idXR0b24pO1xuXG4gICAgdGhpcy5hZGRXaWRnZXQoXG4gICAgICBuZXcgTGlzdFdpZGdldCh7IHJ1bm5pbmdJdGVtcywgc2h1dGRvd25BbGxMYWJlbCwgLi4ub3B0aW9ucyB9KVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHdpZGdldFxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX21hbmFnZXIucnVubmluZ0NoYW5nZWQuZGlzY29ubmVjdCh0aGlzLl91cGRhdGVCdXR0b24sIHRoaXMpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIHByaXZhdGUgX3VwZGF0ZUJ1dHRvbigpOiB2b2lkIHtcbiAgICBjb25zdCBidXR0b24gPSB0aGlzLl9idXR0b247XG4gICAgYnV0dG9uLmVuYWJsZWQgPSB0aGlzLl9tYW5hZ2VyLnJ1bm5pbmcoKS5sZW5ndGggPiAwO1xuICAgIGlmIChidXR0b24uZW5hYmxlZCkge1xuICAgICAgYnV0dG9uLm5vZGUucXVlcnlTZWxlY3RvcignYnV0dG9uJyk/LmNsYXNzTGlzdC5yZW1vdmUoJ2pwLW1vZC1kaXNhYmxlZCcpO1xuICAgIH0gZWxzZSB7XG4gICAgICBidXR0b24ubm9kZS5xdWVyeVNlbGVjdG9yKCdidXR0b24nKT8uY2xhc3NMaXN0LmFkZCgnanAtbW9kLWRpc2FibGVkJyk7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfYnV0dG9uOiBUb29sYmFyQnV0dG9uO1xuICBwcml2YXRlIF9tYW5hZ2VyOiBJUnVubmluZ1Nlc3Npb25zLklNYW5hZ2VyO1xufVxuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCBleHBvc2VzIHRoZSBydW5uaW5nIHRlcm1pbmFsIGFuZCBrZXJuZWwgc2Vzc2lvbnMuXG4gKi9cbmV4cG9ydCBjbGFzcyBSdW5uaW5nU2Vzc2lvbnMgZXh0ZW5kcyBTaWRlUGFuZWwge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IHJ1bm5pbmcgd2lkZ2V0LlxuICAgKi9cbiAgY29uc3RydWN0b3IobWFuYWdlcnM6IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLCB0cmFuc2xhdG9yPzogSVRyYW5zbGF0b3IpIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMubWFuYWdlcnMgPSBtYW5hZ2VycztcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdGhpcy50cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcblxuICAgIHRoaXMuYWRkQ2xhc3MoUlVOTklOR19DTEFTUyk7XG5cbiAgICB0aGlzLnRvb2xiYXIuYWRkSXRlbShcbiAgICAgICdyZWZyZXNoJyxcbiAgICAgIG5ldyBUb29sYmFyQnV0dG9uKHtcbiAgICAgICAgdG9vbHRpcDogdHJhbnMuX18oJ1JlZnJlc2ggTGlzdCcpLFxuICAgICAgICBpY29uOiByZWZyZXNoSWNvbixcbiAgICAgICAgb25DbGljazogKCkgPT5cbiAgICAgICAgICBtYW5hZ2Vycy5pdGVtcygpLmZvckVhY2gobWFuYWdlciA9PiBtYW5hZ2VyLnJlZnJlc2hSdW5uaW5nKCkpXG4gICAgICB9KVxuICAgICk7XG5cbiAgICBtYW5hZ2Vycy5pdGVtcygpLmZvckVhY2gobWFuYWdlciA9PiB0aGlzLmFkZFNlY3Rpb24obWFuYWdlcnMsIG1hbmFnZXIpKTtcblxuICAgIG1hbmFnZXJzLmFkZGVkLmNvbm5lY3QodGhpcy5hZGRTZWN0aW9uLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgd2lkZ2V0XG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5tYW5hZ2Vycy5hZGRlZC5kaXNjb25uZWN0KHRoaXMuYWRkU2VjdGlvbiwgdGhpcyk7XG4gICAgc3VwZXIuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIHNlY3Rpb24gZm9yIGEgbmV3IG1hbmFnZXIuXG4gICAqXG4gICAqIEBwYXJhbSBtYW5hZ2VycyBNYW5hZ2Vyc1xuICAgKiBAcGFyYW0gbWFuYWdlciBOZXcgbWFuYWdlclxuICAgKi9cbiAgcHJvdGVjdGVkIGFkZFNlY3Rpb24oXzogdW5rbm93biwgbWFuYWdlcjogSVJ1bm5pbmdTZXNzaW9ucy5JTWFuYWdlcikge1xuICAgIHRoaXMuYWRkV2lkZ2V0KG5ldyBTZWN0aW9uKHsgbWFuYWdlciwgdHJhbnNsYXRvcjogdGhpcy50cmFuc2xhdG9yIH0pKTtcbiAgfVxuXG4gIHByb3RlY3RlZCBtYW5hZ2VyczogSVJ1bm5pbmdTZXNzaW9uTWFuYWdlcnM7XG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciB0aGUgYElSdW5uaW5nU2Vzc2lvbnNgIGNsYXNzIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVJ1bm5pbmdTZXNzaW9ucyB7XG4gIC8qKlxuICAgKiBBIG1hbmFnZXIgb2YgcnVubmluZyBpdGVtcyBncm91cGVkIHVuZGVyIGEgc2luZ2xlIHNlY3Rpb24uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNYW5hZ2VyIHtcbiAgICAvKipcbiAgICAgKiBOYW1lIHRoYXQgaXMgc2hvd24gdG8gdGhlIHVzZXIgaW4gcGx1cmFsLlxuICAgICAqL1xuICAgIG5hbWU6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIENhbGxlZCB3aGVuIHRoZSBzaHV0ZG93biBhbGwgYnV0dG9uIGlzIHByZXNzZWQuXG4gICAgICovXG4gICAgc2h1dGRvd25BbGwoKTogdm9pZDtcblxuICAgIC8qKlxuICAgICAqIExpc3QgdGhlIHJ1bm5pbmcgbW9kZWxzLlxuICAgICAqL1xuICAgIHJ1bm5pbmcoKTogSVJ1bm5pbmdJdGVtW107XG5cbiAgICAvKipcbiAgICAgKiBGb3JjZSBhIHJlZnJlc2ggb2YgdGhlIHJ1bm5pbmcgbW9kZWxzLlxuICAgICAqL1xuICAgIHJlZnJlc2hSdW5uaW5nKCk6IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBBIHNpZ25hbCB0aGF0IHNob3VsZCBiZSBlbWl0dGVkIHdoZW4gdGhlIGl0ZW0gbGlzdCBoYXMgY2hhbmdlZC5cbiAgICAgKi9cbiAgICBydW5uaW5nQ2hhbmdlZDogSVNpZ25hbDxhbnksIGFueT47XG5cbiAgICAvKipcbiAgICAgKiBBIHN0cmluZyB1c2VkIHRvIGRlc2NyaWJlIHRoZSBzaHV0ZG93biBhY3Rpb24uXG4gICAgICovXG4gICAgc2h1dGRvd25MYWJlbD86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEEgc3RyaW5nIHVzZWQgdG8gZGVzY3JpYmUgdGhlIHNodXRkb3duIGFsbCBhY3Rpb24uXG4gICAgICovXG4gICAgc2h1dGRvd25BbGxMYWJlbD86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEEgc3RyaW5nIHVzZWQgYXMgdGhlIGJvZHkgdGV4dCBpbiB0aGUgc2h1dGRvd24gYWxsIGNvbmZpcm1hdGlvbiBkaWFsb2cuXG4gICAgICovXG4gICAgc2h1dGRvd25BbGxDb25maXJtYXRpb25UZXh0Pzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGljb24gdG8gc2hvdyBmb3Igc2h1dHRpbmcgZG93biBhbiBpbmRpdmlkdWFsIGl0ZW0gaW4gdGhpcyBzZWN0aW9uLlxuICAgICAqL1xuICAgIHNodXRkb3duSXRlbUljb24/OiBMYWJJY29uO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcnVubmluZyBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUnVubmluZ0l0ZW0ge1xuICAgIC8qKlxuICAgICAqIE9wdGlvbmFsIGNoaWxkIG5vZGVzIHRoYXQgYmVsb25nIHRvIGEgdG9wLWxldmVsIHJ1bm5pbmcgaXRlbS5cbiAgICAgKi9cbiAgICBjaGlsZHJlbj86IElSdW5uaW5nSXRlbVtdO1xuXG4gICAgLyoqXG4gICAgICogT3B0aW9uYWwgQ1NTIGNsYXNzIG5hbWUgdG8gYWRkIHRvIHRoZSBydW5uaW5nIGl0ZW0uXG4gICAgICovXG4gICAgY2xhc3NOYW1lPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogT3B0aW9uYWwgY29udGV4dCBoaW50IHRvIGFkZCB0byB0aGUgYGRhdGEtY29udGV4dGAgYXR0cmlidXRlIG9mIGFuIGl0ZW0uXG4gICAgICovXG4gICAgY29udGV4dD86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIENhbGxlZCB3aGVuIHRoZSBydW5uaW5nIGl0ZW0gaXMgY2xpY2tlZC5cbiAgICAgKi9cbiAgICBvcGVuPzogKCkgPT4gdm9pZDtcblxuICAgIC8qKlxuICAgICAqIENhbGxlZCB3aGVuIHRoZSBzaHV0ZG93biBidXR0b24gaXMgcHJlc3NlZCBvbiBhIHBhcnRpY3VsYXIgaXRlbS5cbiAgICAgKi9cbiAgICBzaHV0ZG93bj86ICgpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYExhYkljb25gIHRvIHVzZSBhcyB0aGUgaWNvbiBmb3IgdGhlIHJ1bm5pbmcgaXRlbSBvciB0aGUgc3RyaW5nXG4gICAgICogYHNyY2AgVVJMLlxuICAgICAqL1xuICAgIGljb246ICgpID0+IExhYkljb24gfCBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBDYWxsZWQgdG8gZGV0ZXJtaW5lIHRoZSBsYWJlbCBmb3IgZWFjaCBpdGVtLlxuICAgICAqL1xuICAgIGxhYmVsOiAoKSA9PiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBDYWxsZWQgdG8gZGV0ZXJtaW5lIHRoZSBgdGl0bGVgIGF0dHJpYnV0ZSBmb3IgZWFjaCBpdGVtLCB3aGljaCBpc1xuICAgICAqIHJldmVhbGVkIG9uIGhvdmVyLlxuICAgICAqL1xuICAgIGxhYmVsVGl0bGU/OiAoKSA9PiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBDYWxsZWQgdG8gZGV0ZXJtaW5lIHRoZSBgZGV0YWlsYCBhdHRyaWJ1dGUsIHdoaWNoIGlzIHNob3duIG9wdGlvbmFsbHkgaW5cbiAgICAgKiBhIGNvbHVtbiBhZnRlciB0aGUgbGFiZWwuXG4gICAgICovXG4gICAgZGV0YWlsPzogKCkgPT4gc3RyaW5nO1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=