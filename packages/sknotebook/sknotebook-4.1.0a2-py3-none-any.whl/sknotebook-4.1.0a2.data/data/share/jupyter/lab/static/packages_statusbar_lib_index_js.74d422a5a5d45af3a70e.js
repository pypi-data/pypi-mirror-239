"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_statusbar_lib_index_js"],{

/***/ "../packages/statusbar/lib/components/group.js":
/*!*****************************************************!*\
  !*** ../packages/statusbar/lib/components/group.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GroupItem": () => (/* binding */ GroupItem)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A tsx component for a set of items logically grouped together.
 */
function GroupItem(props) {
    const { spacing, children, className, ...rest } = props;
    const numChildren = react__WEBPACK_IMPORTED_MODULE_0__.Children.count(children);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: `jp-StatusBar-GroupItem ${className || ''}`, ...rest }, react__WEBPACK_IMPORTED_MODULE_0__.Children.map(children, (child, i) => {
        if (i === 0) {
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { marginRight: `${spacing}px` } }, child);
        }
        else if (i === numChildren - 1) {
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { marginLeft: `${spacing}px` } }, child);
        }
        else {
            return react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: { margin: `0px ${spacing}px` } }, child);
        }
    })));
}


/***/ }),

/***/ "../packages/statusbar/lib/components/hover.js":
/*!*****************************************************!*\
  !*** ../packages/statusbar/lib/components/hover.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Popup": () => (/* binding */ Popup),
/* harmony export */   "showPopup": () => (/* binding */ showPopup)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * Create and show a popup component.
 *
 * @param options - options for the popup
 *
 * @returns the popup that was created.
 */
function showPopup(options) {
    const dialog = new Popup(options);
    if (!options.startHidden) {
        dialog.launch();
    }
    return dialog;
}
/**
 * A class for a Popup widget.
 */
class Popup extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget {
    /**
     * Construct a new Popup.
     */
    constructor(options) {
        super();
        this._body = options.body;
        this._body.addClass('jp-StatusBar-HoverItem');
        this._anchor = options.anchor;
        this._align = options.align;
        if (options.hasDynamicSize) {
            this._observer = new ResizeObserver(() => {
                this.update();
            });
        }
        const layout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.PanelLayout());
        layout.addWidget(options.body);
        this._body.node.addEventListener('resize', () => {
            this.update();
        });
    }
    /**
     * Attach the popup widget to the page.
     */
    launch() {
        this._setGeometry();
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Widget.attach(this, document.body);
        this.update();
        this._anchor.addClass('jp-mod-clicked');
        this._anchor.removeClass('jp-mod-highlight');
    }
    /**
     * Handle `'update'` messages for the widget.
     */
    onUpdateRequest(msg) {
        this._setGeometry();
        super.onUpdateRequest(msg);
    }
    /**
     * Handle `'after-attach'` messages for the widget.
     */
    onAfterAttach(msg) {
        var _a;
        document.addEventListener('click', this, false);
        this.node.addEventListener('keydown', this, false);
        window.addEventListener('resize', this, false);
        (_a = this._observer) === null || _a === void 0 ? void 0 : _a.observe(this._body.node);
    }
    /**
     * Handle `'before-detach'` messages for the widget.
     */
    onBeforeDetach(msg) {
        var _a;
        (_a = this._observer) === null || _a === void 0 ? void 0 : _a.disconnect();
        document.removeEventListener('click', this, false);
        this.node.removeEventListener('keydown', this, false);
        window.removeEventListener('resize', this, false);
    }
    /**
     * Handle `'resize'` messages for the widget.
     */
    onResize() {
        this.update();
    }
    /**
     * Dispose of the widget.
     */
    dispose() {
        var _a;
        (_a = this._observer) === null || _a === void 0 ? void 0 : _a.disconnect();
        super.dispose();
        this._anchor.removeClass('jp-mod-clicked');
        this._anchor.addClass('jp-mod-highlight');
    }
    /**
     * Handle DOM events for the widget.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'keydown':
                this._evtKeydown(event);
                break;
            case 'click':
                this._evtClick(event);
                break;
            case 'resize':
                this.onResize();
                break;
            default:
                break;
        }
    }
    _evtClick(event) {
        if (!!event.target &&
            !(this._body.node.contains(event.target) ||
                this._anchor.node.contains(event.target))) {
            this.dispose();
        }
    }
    _evtKeydown(event) {
        // Check for escape key
        switch (event.keyCode) {
            case 27: // Escape.
                event.stopPropagation();
                event.preventDefault();
                this.dispose();
                break;
            default:
                break;
        }
    }
    _setGeometry() {
        let aligned = 0;
        const anchorRect = this._anchor.node.getBoundingClientRect();
        const bodyRect = this._body.node.getBoundingClientRect();
        if (this._align === 'right') {
            aligned = -(bodyRect.width - anchorRect.width);
        }
        const style = window.getComputedStyle(this._body.node);
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.HoverBox.setGeometry({
            anchor: anchorRect,
            host: document.body,
            maxHeight: 500,
            minHeight: 20,
            node: this._body.node,
            offset: {
                horizontal: aligned
            },
            privilege: 'forceAbove',
            style
        });
    }
}


/***/ }),

/***/ "../packages/statusbar/lib/components/index.js":
/*!*****************************************************!*\
  !*** ../packages/statusbar/lib/components/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GroupItem": () => (/* reexport safe */ _group__WEBPACK_IMPORTED_MODULE_0__.GroupItem),
/* harmony export */   "Popup": () => (/* reexport safe */ _hover__WEBPACK_IMPORTED_MODULE_1__.Popup),
/* harmony export */   "ProgressBar": () => (/* reexport safe */ _progressBar__WEBPACK_IMPORTED_MODULE_2__.ProgressBar),
/* harmony export */   "ProgressCircle": () => (/* reexport safe */ _progressCircle__WEBPACK_IMPORTED_MODULE_4__.ProgressCircle),
/* harmony export */   "TextItem": () => (/* reexport safe */ _text__WEBPACK_IMPORTED_MODULE_3__.TextItem),
/* harmony export */   "showPopup": () => (/* reexport safe */ _hover__WEBPACK_IMPORTED_MODULE_1__.showPopup)
/* harmony export */ });
/* harmony import */ var _group__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./group */ "../packages/statusbar/lib/components/group.js");
/* harmony import */ var _hover__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./hover */ "../packages/statusbar/lib/components/hover.js");
/* harmony import */ var _progressBar__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./progressBar */ "../packages/statusbar/lib/components/progressBar.js");
/* harmony import */ var _text__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./text */ "../packages/statusbar/lib/components/text.js");
/* harmony import */ var _progressCircle__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./progressCircle */ "../packages/statusbar/lib/components/progressCircle.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/***/ }),

/***/ "../packages/statusbar/lib/components/progressBar.js":
/*!***********************************************************!*\
  !*** ../packages/statusbar/lib/components/progressBar.js ***!
  \***********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProgressBar": () => (/* binding */ ProgressBar)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A functional tsx component for a progress bar.
 */
function ProgressBar(props) {
    const { width, percentage, ...rest } = props;
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'jp-Statusbar-ProgressBar-progress-bar', role: "progressbar", "aria-valuemin": 0, "aria-valuemax": 100, "aria-valuenow": percentage },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement(Filler, { ...{ percentage, ...rest }, contentWidth: width })));
}
/**
 * A functional tsx component for a partially filled div.
 */
function Filler(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { style: {
            width: `${props.percentage}%`
        } },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, props.content)));
}


/***/ }),

/***/ "../packages/statusbar/lib/components/progressCircle.js":
/*!**************************************************************!*\
  !*** ../packages/statusbar/lib/components/progressCircle.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ProgressCircle": () => (/* binding */ ProgressCircle)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

function ProgressCircle(props) {
    const radius = 104;
    const d = (progress) => {
        const angle = Math.max(progress * 3.6, 0.1);
        const rad = (angle * Math.PI) / 180, x = Math.sin(rad) * radius, y = Math.cos(rad) * -radius, mid = angle < 180 ? 1 : 0, shape = `M 0 0 v -${radius} A ${radius} ${radius} 1 ` +
            mid +
            ' 0 ' +
            x.toFixed(4) +
            ' ' +
            y.toFixed(4) +
            ' z';
        return shape;
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'jp-Statusbar-ProgressCircle', role: "progressbar", "aria-label": props.label || 'Unlabelled progress circle', "aria-valuemin": 0, "aria-valuemax": 100, "aria-valuenow": props.progress },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("svg", { viewBox: "0 0 250 250" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("circle", { cx: "125", cy: "125", r: `${radius}`, stroke: "var(--jp-inverse-layout-color3)", strokeWidth: "20", fill: "none" }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("path", { transform: "translate(125,125) scale(.9)", d: d(props.progress), fill: 'var(--jp-inverse-layout-color3)' }))));
}


/***/ }),

/***/ "../packages/statusbar/lib/components/text.js":
/*!****************************************************!*\
  !*** ../packages/statusbar/lib/components/text.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TextItem": () => (/* binding */ TextItem)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A functional tsx component for a text item.
 */
function TextItem(props) {
    const { title, source, className, ...rest } = props;
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { className: `jp-StatusBar-TextItem ${className}`, title: title, ...rest }, source));
}


/***/ }),

/***/ "../packages/statusbar/lib/index.js":
/*!******************************************!*\
  !*** ../packages/statusbar/lib/index.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GroupItem": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.GroupItem),
/* harmony export */   "IStatusBar": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_2__.IStatusBar),
/* harmony export */   "Popup": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.Popup),
/* harmony export */   "ProgressBar": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.ProgressBar),
/* harmony export */   "ProgressCircle": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.ProgressCircle),
/* harmony export */   "StatusBar": () => (/* reexport safe */ _statusbar__WEBPACK_IMPORTED_MODULE_1__.StatusBar),
/* harmony export */   "TextItem": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.TextItem),
/* harmony export */   "showPopup": () => (/* reexport safe */ _components__WEBPACK_IMPORTED_MODULE_0__.showPopup)
/* harmony export */ });
/* harmony import */ var _components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./components */ "../packages/statusbar/lib/components/index.js");
/* harmony import */ var _statusbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./statusbar */ "../packages/statusbar/lib/statusbar.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../packages/statusbar/lib/tokens.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module statusbar
 */





/***/ }),

/***/ "../packages/statusbar/lib/statusbar.js":
/*!**********************************************!*\
  !*** ../packages/statusbar/lib/statusbar.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "StatusBar": () => (/* binding */ StatusBar)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Main status bar object which contains all items.
 */
class StatusBar extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor() {
        super();
        this._leftRankItems = [];
        this._rightRankItems = [];
        this._statusItems = {};
        this._disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableSet();
        this.addClass('jp-StatusBar-Widget');
        const rootLayout = (this.layout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.PanelLayout());
        const leftPanel = (this._leftSide = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel());
        const middlePanel = (this._middlePanel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel());
        const rightPanel = (this._rightSide = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel());
        leftPanel.addClass('jp-StatusBar-Left');
        middlePanel.addClass('jp-StatusBar-Middle');
        rightPanel.addClass('jp-StatusBar-Right');
        rootLayout.addWidget(leftPanel);
        rootLayout.addWidget(middlePanel);
        rootLayout.addWidget(rightPanel);
    }
    /**
     * Register a new status item.
     *
     * @param id - a unique id for the status item.
     *
     * @param statusItem - The item to add to the status bar.
     */
    registerStatusItem(id, statusItem) {
        if (id in this._statusItems) {
            throw new Error(`Status item ${id} already registered.`);
        }
        // Populate defaults for the optional properties of the status item.
        const fullStatusItem = {
            ...Private.statusItemDefaults,
            ...statusItem
        };
        const { align, item, rank } = fullStatusItem;
        // Connect the activeStateChanged signal to refreshing the status item,
        // if the signal was provided.
        const onActiveStateChanged = () => {
            this._refreshItem(id);
        };
        if (fullStatusItem.activeStateChanged) {
            fullStatusItem.activeStateChanged.connect(onActiveStateChanged);
        }
        const rankItem = { id, rank };
        fullStatusItem.item.addClass('jp-StatusBar-Item');
        this._statusItems[id] = fullStatusItem;
        if (align === 'left') {
            const insertIndex = this._findInsertIndex(this._leftRankItems, rankItem);
            if (insertIndex === -1) {
                this._leftSide.addWidget(item);
                this._leftRankItems.push(rankItem);
            }
            else {
                _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._leftRankItems, insertIndex, rankItem);
                this._leftSide.insertWidget(insertIndex, item);
            }
        }
        else if (align === 'right') {
            const insertIndex = this._findInsertIndex(this._rightRankItems, rankItem);
            if (insertIndex === -1) {
                this._rightSide.addWidget(item);
                this._rightRankItems.push(rankItem);
            }
            else {
                _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._rightRankItems, insertIndex, rankItem);
                this._rightSide.insertWidget(insertIndex, item);
            }
        }
        else {
            this._middlePanel.addWidget(item);
        }
        this._refreshItem(id); // Initially refresh the status item.
        const disposable = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableDelegate(() => {
            delete this._statusItems[id];
            if (fullStatusItem.activeStateChanged) {
                fullStatusItem.activeStateChanged.disconnect(onActiveStateChanged);
            }
            item.parent = null;
            item.dispose();
        });
        this._disposables.add(disposable);
        return disposable;
    }
    /**
     * Dispose of the status bar.
     */
    dispose() {
        this._leftRankItems.length = 0;
        this._rightRankItems.length = 0;
        this._disposables.dispose();
        super.dispose();
    }
    /**
     * Handle an 'update-request' message to the status bar.
     */
    onUpdateRequest(msg) {
        this._refreshAll();
        super.onUpdateRequest(msg);
    }
    _findInsertIndex(side, newItem) {
        return _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.findFirstIndex(side, item => item.rank > newItem.rank);
    }
    _refreshItem(id) {
        const statusItem = this._statusItems[id];
        if (statusItem.isActive()) {
            statusItem.item.show();
            statusItem.item.update();
        }
        else {
            statusItem.item.hide();
        }
    }
    _refreshAll() {
        Object.keys(this._statusItems).forEach(id => {
            this._refreshItem(id);
        });
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Default options for a status item, less the item itself.
     */
    Private.statusItemDefaults = {
        align: 'left',
        rank: 0,
        isActive: () => true,
        activeStateChanged: undefined
    };
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/statusbar/lib/tokens.js":
/*!*******************************************!*\
  !*** ../packages/statusbar/lib/tokens.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IStatusBar": () => (/* binding */ IStatusBar)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// tslint:disable-next-line:variable-name
const IStatusBar = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/statusbar:IStatusBar', 'A service for the status bar on the application. Use this if you want to add new status bar items.');


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfc3RhdHVzYmFyX2xpYl9pbmRleF9qcy43NGQ0MjJhNWE1ZDQ1YWYzYTcwZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRTVCO0FBRS9COztHQUVHO0FBQ0ksU0FBUyxTQUFTLENBQ3ZCLEtBQThEO0lBRTlELE1BQU0sRUFBRSxPQUFPLEVBQUUsUUFBUSxFQUFFLFNBQVMsRUFBRSxHQUFHLElBQUksRUFBRSxHQUFHLEtBQUssQ0FBQztJQUN4RCxNQUFNLFdBQVcsR0FBRyxpREFBb0IsQ0FBQyxRQUFRLENBQUMsQ0FBQztJQUVuRCxPQUFPLENBQ0wsMERBQUssU0FBUyxFQUFFLDBCQUEwQixTQUFTLElBQUksRUFBRSxFQUFFLEtBQU0sSUFBSSxJQUNsRSwrQ0FBa0IsQ0FBQyxRQUFRLEVBQUUsQ0FBQyxLQUFLLEVBQUUsQ0FBQyxFQUFFLEVBQUU7UUFDekMsSUFBSSxDQUFDLEtBQUssQ0FBQyxFQUFFO1lBQ1gsT0FBTywwREFBSyxLQUFLLEVBQUUsRUFBRSxXQUFXLEVBQUUsR0FBRyxPQUFPLElBQUksRUFBRSxJQUFHLEtBQUssQ0FBTyxDQUFDO1NBQ25FO2FBQU0sSUFBSSxDQUFDLEtBQUssV0FBVyxHQUFHLENBQUMsRUFBRTtZQUNoQyxPQUFPLDBEQUFLLEtBQUssRUFBRSxFQUFFLFVBQVUsRUFBRSxHQUFHLE9BQU8sSUFBSSxFQUFFLElBQUcsS0FBSyxDQUFPLENBQUM7U0FDbEU7YUFBTTtZQUNMLE9BQU8sMERBQUssS0FBSyxFQUFFLEVBQUUsTUFBTSxFQUFFLE9BQU8sT0FBTyxJQUFJLEVBQUUsSUFBRyxLQUFLLENBQU8sQ0FBQztTQUNsRTtJQUNILENBQUMsQ0FBQyxDQUNFLENBQ1AsQ0FBQztBQUNKLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDM0JELDBDQUEwQztBQUMxQywyREFBMkQ7QUFFTjtBQUVDO0FBRXREOzs7Ozs7R0FNRztBQUNJLFNBQVMsU0FBUyxDQUFDLE9BQXVCO0lBQy9DLE1BQU0sTUFBTSxHQUFHLElBQUksS0FBSyxDQUFDLE9BQU8sQ0FBQyxDQUFDO0lBQ2xDLElBQUksQ0FBQyxPQUFPLENBQUMsV0FBVyxFQUFFO1FBQ3hCLE1BQU0sQ0FBQyxNQUFNLEVBQUUsQ0FBQztLQUNqQjtJQUNELE9BQU8sTUFBTSxDQUFDO0FBQ2hCLENBQUM7QUFFRDs7R0FFRztBQUNJLE1BQU0sS0FBTSxTQUFRLG1EQUFNO0lBQy9COztPQUVHO0lBQ0gsWUFBWSxPQUE0QztRQUN0RCxLQUFLLEVBQUUsQ0FBQztRQUNSLElBQUksQ0FBQyxLQUFLLEdBQUcsT0FBTyxDQUFDLElBQUksQ0FBQztRQUMxQixJQUFJLENBQUMsS0FBSyxDQUFDLFFBQVEsQ0FBQyx3QkFBd0IsQ0FBQyxDQUFDO1FBQzlDLElBQUksQ0FBQyxPQUFPLEdBQUcsT0FBTyxDQUFDLE1BQU0sQ0FBQztRQUM5QixJQUFJLENBQUMsTUFBTSxHQUFHLE9BQU8sQ0FBQyxLQUFLLENBQUM7UUFDNUIsSUFBSSxPQUFPLENBQUMsY0FBYyxFQUFFO1lBQzFCLElBQUksQ0FBQyxTQUFTLEdBQUcsSUFBSSxjQUFjLENBQUMsR0FBRyxFQUFFO2dCQUN2QyxJQUFJLENBQUMsTUFBTSxFQUFFLENBQUM7WUFDaEIsQ0FBQyxDQUFDLENBQUM7U0FDSjtRQUNELE1BQU0sTUFBTSxHQUFHLENBQUMsSUFBSSxDQUFDLE1BQU0sR0FBRyxJQUFJLHdEQUFXLEVBQUUsQ0FBQyxDQUFDO1FBQ2pELE1BQU0sQ0FBQyxTQUFTLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQy9CLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLGdCQUFnQixDQUFDLFFBQVEsRUFBRSxHQUFHLEVBQUU7WUFDOUMsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO1FBQ2hCLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUVEOztPQUVHO0lBQ0gsTUFBTTtRQUNKLElBQUksQ0FBQyxZQUFZLEVBQUUsQ0FBQztRQUNwQiwwREFBYSxDQUFDLElBQUksRUFBRSxRQUFRLENBQUMsSUFBSSxDQUFDLENBQUM7UUFDbkMsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO1FBQ2QsSUFBSSxDQUFDLE9BQU8sQ0FBQyxRQUFRLENBQUMsZ0JBQWdCLENBQUMsQ0FBQztRQUN4QyxJQUFJLENBQUMsT0FBTyxDQUFDLFdBQVcsQ0FBQyxrQkFBa0IsQ0FBQyxDQUFDO0lBQy9DLENBQUM7SUFFRDs7T0FFRztJQUNPLGVBQWUsQ0FBQyxHQUFZO1FBQ3BDLElBQUksQ0FBQyxZQUFZLEVBQUUsQ0FBQztRQUNwQixLQUFLLENBQUMsZUFBZSxDQUFDLEdBQUcsQ0FBQyxDQUFDO0lBQzdCLENBQUM7SUFFRDs7T0FFRztJQUNPLGFBQWEsQ0FBQyxHQUFZOztRQUNsQyxRQUFRLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFLElBQUksRUFBRSxLQUFLLENBQUMsQ0FBQztRQUNoRCxJQUFJLENBQUMsSUFBSSxDQUFDLGdCQUFnQixDQUFDLFNBQVMsRUFBRSxJQUFJLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFDbkQsTUFBTSxDQUFDLGdCQUFnQixDQUFDLFFBQVEsRUFBRSxJQUFJLEVBQUUsS0FBSyxDQUFDLENBQUM7UUFDL0MsVUFBSSxDQUFDLFNBQVMsMENBQUUsT0FBTyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDM0MsQ0FBQztJQUVEOztPQUVHO0lBQ08sY0FBYyxDQUFDLEdBQVk7O1FBQ25DLFVBQUksQ0FBQyxTQUFTLDBDQUFFLFVBQVUsRUFBRSxDQUFDO1FBQzdCLFFBQVEsQ0FBQyxtQkFBbUIsQ0FBQyxPQUFPLEVBQUUsSUFBSSxFQUFFLEtBQUssQ0FBQyxDQUFDO1FBQ25ELElBQUksQ0FBQyxJQUFJLENBQUMsbUJBQW1CLENBQUMsU0FBUyxFQUFFLElBQUksRUFBRSxLQUFLLENBQUMsQ0FBQztRQUN0RCxNQUFNLENBQUMsbUJBQW1CLENBQUMsUUFBUSxFQUFFLElBQUksRUFBRSxLQUFLLENBQUMsQ0FBQztJQUNwRCxDQUFDO0lBRUQ7O09BRUc7SUFDTyxRQUFRO1FBQ2hCLElBQUksQ0FBQyxNQUFNLEVBQUUsQ0FBQztJQUNoQixDQUFDO0lBRUQ7O09BRUc7SUFDSCxPQUFPOztRQUNMLFVBQUksQ0FBQyxTQUFTLDBDQUFFLFVBQVUsRUFBRSxDQUFDO1FBQzdCLEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUNoQixJQUFJLENBQUMsT0FBTyxDQUFDLFdBQVcsQ0FBQyxnQkFBZ0IsQ0FBQyxDQUFDO1FBQzNDLElBQUksQ0FBQyxPQUFPLENBQUMsUUFBUSxDQUFDLGtCQUFrQixDQUFDLENBQUM7SUFDNUMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsV0FBVyxDQUFDLEtBQVk7UUFDdEIsUUFBUSxLQUFLLENBQUMsSUFBSSxFQUFFO1lBQ2xCLEtBQUssU0FBUztnQkFDWixJQUFJLENBQUMsV0FBVyxDQUFDLEtBQXNCLENBQUMsQ0FBQztnQkFDekMsTUFBTTtZQUNSLEtBQUssT0FBTztnQkFDVixJQUFJLENBQUMsU0FBUyxDQUFDLEtBQW1CLENBQUMsQ0FBQztnQkFDcEMsTUFBTTtZQUNSLEtBQUssUUFBUTtnQkFDWCxJQUFJLENBQUMsUUFBUSxFQUFFLENBQUM7Z0JBQ2hCLE1BQU07WUFDUjtnQkFDRSxNQUFNO1NBQ1Q7SUFDSCxDQUFDO0lBRU8sU0FBUyxDQUFDLEtBQWlCO1FBQ2pDLElBQ0UsQ0FBQyxDQUFDLEtBQUssQ0FBQyxNQUFNO1lBQ2QsQ0FBQyxDQUNDLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsTUFBcUIsQ0FBQztnQkFDckQsSUFBSSxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsUUFBUSxDQUFDLEtBQUssQ0FBQyxNQUFxQixDQUFDLENBQ3hELEVBQ0Q7WUFDQSxJQUFJLENBQUMsT0FBTyxFQUFFLENBQUM7U0FDaEI7SUFDSCxDQUFDO0lBRU8sV0FBVyxDQUFDLEtBQW9CO1FBQ3RDLHVCQUF1QjtRQUN2QixRQUFRLEtBQUssQ0FBQyxPQUFPLEVBQUU7WUFDckIsS0FBSyxFQUFFLEVBQUUsVUFBVTtnQkFDakIsS0FBSyxDQUFDLGVBQWUsRUFBRSxDQUFDO2dCQUN4QixLQUFLLENBQUMsY0FBYyxFQUFFLENBQUM7Z0JBQ3ZCLElBQUksQ0FBQyxPQUFPLEVBQUUsQ0FBQztnQkFDZixNQUFNO1lBQ1I7Z0JBQ0UsTUFBTTtTQUNUO0lBQ0gsQ0FBQztJQUVPLFlBQVk7UUFDbEIsSUFBSSxPQUFPLEdBQUcsQ0FBQyxDQUFDO1FBQ2hCLE1BQU0sVUFBVSxHQUFHLElBQUksQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLHFCQUFxQixFQUFFLENBQUM7UUFDN0QsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMscUJBQXFCLEVBQUUsQ0FBQztRQUN6RCxJQUFJLElBQUksQ0FBQyxNQUFNLEtBQUssT0FBTyxFQUFFO1lBQzNCLE9BQU8sR0FBRyxDQUFDLENBQUMsUUFBUSxDQUFDLEtBQUssR0FBRyxVQUFVLENBQUMsS0FBSyxDQUFDLENBQUM7U0FDaEQ7UUFDRCxNQUFNLEtBQUssR0FBRyxNQUFNLENBQUMsZ0JBQWdCLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUN2RCwyRUFBb0IsQ0FBQztZQUNuQixNQUFNLEVBQUUsVUFBVTtZQUNsQixJQUFJLEVBQUUsUUFBUSxDQUFDLElBQUk7WUFDbkIsU0FBUyxFQUFFLEdBQUc7WUFDZCxTQUFTLEVBQUUsRUFBRTtZQUNiLElBQUksRUFBRSxJQUFJLENBQUMsS0FBSyxDQUFDLElBQUk7WUFDckIsTUFBTSxFQUFFO2dCQUNOLFVBQVUsRUFBRSxPQUFPO2FBQ3BCO1lBQ0QsU0FBUyxFQUFFLFlBQVk7WUFDdkIsS0FBSztTQUNOLENBQUMsQ0FBQztJQUNMLENBQUM7Q0FNRjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQzdLRCwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRW5DO0FBQ0E7QUFDTTtBQUNQO0FBQ1U7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUGpDLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFNUI7QUEyQi9COztHQUVHO0FBQ0ksU0FBUyxXQUFXLENBQUMsS0FBeUI7SUFDbkQsTUFBTSxFQUFFLEtBQUssRUFBRSxVQUFVLEVBQUUsR0FBRyxJQUFJLEVBQUUsR0FBRyxLQUFLLENBQUM7SUFDN0MsT0FBTyxDQUNMLDBEQUNFLFNBQVMsRUFBRSx1Q0FBdUMsRUFDbEQsSUFBSSxFQUFDLGFBQWEsbUJBQ0gsQ0FBQyxtQkFDRCxHQUFHLG1CQUNILFVBQVU7UUFFekIsaURBQUMsTUFBTSxPQUFLLEVBQUUsVUFBVSxFQUFFLEdBQUcsSUFBSSxFQUFFLEVBQUUsWUFBWSxFQUFFLEtBQUssR0FBSSxDQUN4RCxDQUNQLENBQUM7QUFDSixDQUFDO0FBMkJEOztHQUVHO0FBQ0gsU0FBUyxNQUFNLENBQUMsS0FBb0I7SUFDbEMsT0FBTyxDQUNMLDBEQUNFLEtBQUssRUFBRTtZQUNMLEtBQUssRUFBRSxHQUFHLEtBQUssQ0FBQyxVQUFVLEdBQUc7U0FDOUI7UUFFRCw0REFBSSxLQUFLLENBQUMsT0FBTyxDQUFLLENBQ2xCLENBQ1AsQ0FBQztBQUNKLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDdEZEOzs7R0FHRztBQUV1QjtBQXlCbkIsU0FBUyxjQUFjLENBQUMsS0FBNEI7SUFDekQsTUFBTSxNQUFNLEdBQUcsR0FBRyxDQUFDO0lBQ25CLE1BQU0sQ0FBQyxHQUFHLENBQUMsUUFBZ0IsRUFBVSxFQUFFO1FBQ3JDLE1BQU0sS0FBSyxHQUFHLElBQUksQ0FBQyxHQUFHLENBQUMsUUFBUSxHQUFHLEdBQUcsRUFBRSxHQUFHLENBQUMsQ0FBQztRQUM1QyxNQUFNLEdBQUcsR0FBRyxDQUFDLEtBQUssR0FBRyxJQUFJLENBQUMsRUFBRSxDQUFDLEdBQUcsR0FBRyxFQUNqQyxDQUFDLEdBQUcsSUFBSSxDQUFDLEdBQUcsQ0FBQyxHQUFHLENBQUMsR0FBRyxNQUFNLEVBQzFCLENBQUMsR0FBRyxJQUFJLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQyxHQUFHLENBQUMsTUFBTSxFQUMzQixHQUFHLEdBQUcsS0FBSyxHQUFHLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLEVBQ3pCLEtBQUssR0FDSCxZQUFZLE1BQU0sTUFBTSxNQUFNLElBQUksTUFBTSxLQUFLO1lBQzdDLEdBQUc7WUFDSCxLQUFLO1lBQ0wsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUM7WUFDWixHQUFHO1lBQ0gsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUM7WUFDWixJQUFJLENBQUM7UUFDVCxPQUFPLEtBQUssQ0FBQztJQUNmLENBQUMsQ0FBQztJQUNGLE9BQU8sQ0FDTCxvRUFDRSxTQUFTLEVBQUUsNkJBQTZCLEVBQ3hDLElBQUksRUFBQyxhQUFhLGdCQUNOLEtBQUssQ0FBQyxLQUFLLElBQUksNEJBQTRCLG1CQUN4QyxDQUFDLG1CQUNELEdBQUcsbUJBQ0gsS0FBSyxDQUFDLFFBQVE7UUFFN0Isb0VBQUssT0FBTyxFQUFDLGFBQWE7WUFDeEIsdUVBQ0UsRUFBRSxFQUFDLEtBQUssRUFDUixFQUFFLEVBQUMsS0FBSyxFQUNSLENBQUMsRUFBRSxHQUFHLE1BQU0sRUFBRSxFQUNkLE1BQU0sRUFBQyxpQ0FBaUMsRUFDeEMsV0FBVyxFQUFDLElBQUksRUFDaEIsSUFBSSxFQUFDLE1BQU0sR0FDWDtZQUNGLHFFQUNFLFNBQVMsRUFBQyw4QkFBOEIsRUFDeEMsQ0FBQyxFQUFFLENBQUMsQ0FBQyxLQUFLLENBQUMsUUFBUSxDQUFDLEVBQ3BCLElBQUksRUFBRSxpQ0FBaUMsR0FDdkMsQ0FDRSxDQUNGLENBQ1AsQ0FBQztBQUNKLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDMUVELDBDQUEwQztBQUMxQywyREFBMkQ7QUFFNUI7QUFzQi9COztHQUVHO0FBQ0ksU0FBUyxRQUFRLENBQ3RCLEtBQThEO0lBRTlELE1BQU0sRUFBRSxLQUFLLEVBQUUsTUFBTSxFQUFFLFNBQVMsRUFBRSxHQUFHLElBQUksRUFBRSxHQUFHLEtBQUssQ0FBQztJQUNwRCxPQUFPLENBQ0wsMkRBQ0UsU0FBUyxFQUFFLHlCQUF5QixTQUFTLEVBQUUsRUFDL0MsS0FBSyxFQUFFLEtBQUssS0FDUixJQUFJLElBRVAsTUFBTSxDQUNGLENBQ1IsQ0FBQztBQUNKLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN6Q0Q7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBRTBCO0FBQ0Q7QUFDSDs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDWHpCLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFZDtBQUtqQjtBQUVpQztBQUc3RDs7R0FFRztBQUNJLE1BQU0sU0FBVSxTQUFRLG1EQUFNO0lBQ25DO1FBQ0UsS0FBSyxFQUFFLENBQUM7UUErSEYsbUJBQWMsR0FBd0IsRUFBRSxDQUFDO1FBQ3pDLG9CQUFlLEdBQXdCLEVBQUUsQ0FBQztRQUMxQyxpQkFBWSxHQUF3QyxFQUFFLENBQUM7UUFDdkQsaUJBQVksR0FBRyxJQUFJLDZEQUFhLEVBQUUsQ0FBQztRQWpJekMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDO1FBRXJDLE1BQU0sVUFBVSxHQUFHLENBQUMsSUFBSSxDQUFDLE1BQU0sR0FBRyxJQUFJLHdEQUFXLEVBQUUsQ0FBQyxDQUFDO1FBRXJELE1BQU0sU0FBUyxHQUFHLENBQUMsSUFBSSxDQUFDLFNBQVMsR0FBRyxJQUFJLGtEQUFLLEVBQUUsQ0FBQyxDQUFDO1FBQ2pELE1BQU0sV0FBVyxHQUFHLENBQUMsSUFBSSxDQUFDLFlBQVksR0FBRyxJQUFJLGtEQUFLLEVBQUUsQ0FBQyxDQUFDO1FBQ3RELE1BQU0sVUFBVSxHQUFHLENBQUMsSUFBSSxDQUFDLFVBQVUsR0FBRyxJQUFJLGtEQUFLLEVBQUUsQ0FBQyxDQUFDO1FBRW5ELFNBQVMsQ0FBQyxRQUFRLENBQUMsbUJBQW1CLENBQUMsQ0FBQztRQUN4QyxXQUFXLENBQUMsUUFBUSxDQUFDLHFCQUFxQixDQUFDLENBQUM7UUFDNUMsVUFBVSxDQUFDLFFBQVEsQ0FBQyxvQkFBb0IsQ0FBQyxDQUFDO1FBRTFDLFVBQVUsQ0FBQyxTQUFTLENBQUMsU0FBUyxDQUFDLENBQUM7UUFDaEMsVUFBVSxDQUFDLFNBQVMsQ0FBQyxXQUFXLENBQUMsQ0FBQztRQUNsQyxVQUFVLENBQUMsU0FBUyxDQUFDLFVBQVUsQ0FBQyxDQUFDO0lBQ25DLENBQUM7SUFFRDs7Ozs7O09BTUc7SUFDSCxrQkFBa0IsQ0FBQyxFQUFVLEVBQUUsVUFBNEI7UUFDekQsSUFBSSxFQUFFLElBQUksSUFBSSxDQUFDLFlBQVksRUFBRTtZQUMzQixNQUFNLElBQUksS0FBSyxDQUFDLGVBQWUsRUFBRSxzQkFBc0IsQ0FBQyxDQUFDO1NBQzFEO1FBRUQsb0VBQW9FO1FBQ3BFLE1BQU0sY0FBYyxHQUFHO1lBQ3JCLEdBQUcsT0FBTyxDQUFDLGtCQUFrQjtZQUM3QixHQUFHLFVBQVU7U0FDTyxDQUFDO1FBQ3ZCLE1BQU0sRUFBRSxLQUFLLEVBQUUsSUFBSSxFQUFFLElBQUksRUFBRSxHQUFHLGNBQWMsQ0FBQztRQUU3Qyx1RUFBdUU7UUFDdkUsOEJBQThCO1FBQzlCLE1BQU0sb0JBQW9CLEdBQUcsR0FBRyxFQUFFO1lBQ2hDLElBQUksQ0FBQyxZQUFZLENBQUMsRUFBRSxDQUFDLENBQUM7UUFDeEIsQ0FBQyxDQUFDO1FBQ0YsSUFBSSxjQUFjLENBQUMsa0JBQWtCLEVBQUU7WUFDckMsY0FBYyxDQUFDLGtCQUFrQixDQUFDLE9BQU8sQ0FBQyxvQkFBb0IsQ0FBQyxDQUFDO1NBQ2pFO1FBRUQsTUFBTSxRQUFRLEdBQUcsRUFBRSxFQUFFLEVBQUUsSUFBSSxFQUFFLENBQUM7UUFFOUIsY0FBYyxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsbUJBQW1CLENBQUMsQ0FBQztRQUNsRCxJQUFJLENBQUMsWUFBWSxDQUFDLEVBQUUsQ0FBQyxHQUFHLGNBQWMsQ0FBQztRQUV2QyxJQUFJLEtBQUssS0FBSyxNQUFNLEVBQUU7WUFDcEIsTUFBTSxXQUFXLEdBQUcsSUFBSSxDQUFDLGdCQUFnQixDQUFDLElBQUksQ0FBQyxjQUFjLEVBQUUsUUFBUSxDQUFDLENBQUM7WUFDekUsSUFBSSxXQUFXLEtBQUssQ0FBQyxDQUFDLEVBQUU7Z0JBQ3RCLElBQUksQ0FBQyxTQUFTLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxDQUFDO2dCQUMvQixJQUFJLENBQUMsY0FBYyxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsQ0FBQzthQUNwQztpQkFBTTtnQkFDTCw4REFBZSxDQUFDLElBQUksQ0FBQyxjQUFjLEVBQUUsV0FBVyxFQUFFLFFBQVEsQ0FBQyxDQUFDO2dCQUM1RCxJQUFJLENBQUMsU0FBUyxDQUFDLFlBQVksQ0FBQyxXQUFXLEVBQUUsSUFBSSxDQUFDLENBQUM7YUFDaEQ7U0FDRjthQUFNLElBQUksS0FBSyxLQUFLLE9BQU8sRUFBRTtZQUM1QixNQUFNLFdBQVcsR0FBRyxJQUFJLENBQUMsZ0JBQWdCLENBQUMsSUFBSSxDQUFDLGVBQWUsRUFBRSxRQUFRLENBQUMsQ0FBQztZQUMxRSxJQUFJLFdBQVcsS0FBSyxDQUFDLENBQUMsRUFBRTtnQkFDdEIsSUFBSSxDQUFDLFVBQVUsQ0FBQyxTQUFTLENBQUMsSUFBSSxDQUFDLENBQUM7Z0JBQ2hDLElBQUksQ0FBQyxlQUFlLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxDQUFDO2FBQ3JDO2lCQUFNO2dCQUNMLDhEQUFlLENBQUMsSUFBSSxDQUFDLGVBQWUsRUFBRSxXQUFXLEVBQUUsUUFBUSxDQUFDLENBQUM7Z0JBQzdELElBQUksQ0FBQyxVQUFVLENBQUMsWUFBWSxDQUFDLFdBQVcsRUFBRSxJQUFJLENBQUMsQ0FBQzthQUNqRDtTQUNGO2FBQU07WUFDTCxJQUFJLENBQUMsWUFBWSxDQUFDLFNBQVMsQ0FBQyxJQUFJLENBQUMsQ0FBQztTQUNuQztRQUNELElBQUksQ0FBQyxZQUFZLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxxQ0FBcUM7UUFFNUQsTUFBTSxVQUFVLEdBQUcsSUFBSSxrRUFBa0IsQ0FBQyxHQUFHLEVBQUU7WUFDN0MsT0FBTyxJQUFJLENBQUMsWUFBWSxDQUFDLEVBQUUsQ0FBQyxDQUFDO1lBQzdCLElBQUksY0FBYyxDQUFDLGtCQUFrQixFQUFFO2dCQUNyQyxjQUFjLENBQUMsa0JBQWtCLENBQUMsVUFBVSxDQUFDLG9CQUFvQixDQUFDLENBQUM7YUFDcEU7WUFDRCxJQUFJLENBQUMsTUFBTSxHQUFHLElBQUksQ0FBQztZQUNuQixJQUFJLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDakIsQ0FBQyxDQUFDLENBQUM7UUFDSCxJQUFJLENBQUMsWUFBWSxDQUFDLEdBQUcsQ0FBQyxVQUFVLENBQUMsQ0FBQztRQUNsQyxPQUFPLFVBQVUsQ0FBQztJQUNwQixDQUFDO0lBRUQ7O09BRUc7SUFDSCxPQUFPO1FBQ0wsSUFBSSxDQUFDLGNBQWMsQ0FBQyxNQUFNLEdBQUcsQ0FBQyxDQUFDO1FBQy9CLElBQUksQ0FBQyxlQUFlLENBQUMsTUFBTSxHQUFHLENBQUMsQ0FBQztRQUNoQyxJQUFJLENBQUMsWUFBWSxDQUFDLE9BQU8sRUFBRSxDQUFDO1FBQzVCLEtBQUssQ0FBQyxPQUFPLEVBQUUsQ0FBQztJQUNsQixDQUFDO0lBRUQ7O09BRUc7SUFDTyxlQUFlLENBQUMsR0FBWTtRQUNwQyxJQUFJLENBQUMsV0FBVyxFQUFFLENBQUM7UUFDbkIsS0FBSyxDQUFDLGVBQWUsQ0FBQyxHQUFHLENBQUMsQ0FBQztJQUM3QixDQUFDO0lBRU8sZ0JBQWdCLENBQ3RCLElBQXlCLEVBQ3pCLE9BQTBCO1FBRTFCLE9BQU8sc0VBQXVCLENBQUMsSUFBSSxFQUFFLElBQUksQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDLElBQUksR0FBRyxPQUFPLENBQUMsSUFBSSxDQUFDLENBQUM7SUFDekUsQ0FBQztJQUVPLFlBQVksQ0FBQyxFQUFVO1FBQzdCLE1BQU0sVUFBVSxHQUFHLElBQUksQ0FBQyxZQUFZLENBQUMsRUFBRSxDQUFDLENBQUM7UUFDekMsSUFBSSxVQUFVLENBQUMsUUFBUSxFQUFFLEVBQUU7WUFDekIsVUFBVSxDQUFDLElBQUksQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUN2QixVQUFVLENBQUMsSUFBSSxDQUFDLE1BQU0sRUFBRSxDQUFDO1NBQzFCO2FBQU07WUFDTCxVQUFVLENBQUMsSUFBSSxDQUFDLElBQUksRUFBRSxDQUFDO1NBQ3hCO0lBQ0gsQ0FBQztJQUVPLFdBQVc7UUFDakIsTUFBTSxDQUFDLElBQUksQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUMsT0FBTyxDQUFDLEVBQUUsQ0FBQyxFQUFFO1lBQzFDLElBQUksQ0FBQyxZQUFZLENBQUMsRUFBRSxDQUFDLENBQUM7UUFDeEIsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDO0NBU0Y7QUFFRDs7R0FFRztBQUNILElBQVUsT0FBTyxDQTJCaEI7QUEzQkQsV0FBVSxPQUFPO0lBRWY7O09BRUc7SUFDVSwwQkFBa0IsR0FBbUM7UUFDaEUsS0FBSyxFQUFFLE1BQU07UUFDYixJQUFJLEVBQUUsQ0FBQztRQUNQLFFBQVEsRUFBRSxHQUFHLEVBQUUsQ0FBQyxJQUFJO1FBQ3BCLGtCQUFrQixFQUFFLFNBQVM7S0FDOUIsQ0FBQztBQWlCSixDQUFDLEVBM0JTLE9BQU8sS0FBUCxPQUFPLFFBMkJoQjs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN4TEQsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVqQjtBQUsxQyx5Q0FBeUM7QUFDbEMsTUFBTSxVQUFVLEdBQUcsSUFBSSxvREFBSyxDQUNqQyxrQ0FBa0MsRUFDbEMsb0dBQW9HLENBQ3JHLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9jb21wb25lbnRzL2dyb3VwLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9jb21wb25lbnRzL2hvdmVyLnRzeCIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdHVzYmFyL3NyYy9jb21wb25lbnRzL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL2NvbXBvbmVudHMvcHJvZ3Jlc3NCYXIudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL2NvbXBvbmVudHMvcHJvZ3Jlc3NDaXJjbGUudHN4Iiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL2NvbXBvbmVudHMvdGV4dC50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXR1c2Jhci9zcmMvc3RhdHVzYmFyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0dXNiYXIvc3JjL3Rva2Vucy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoqXG4gKiBBIHRzeCBjb21wb25lbnQgZm9yIGEgc2V0IG9mIGl0ZW1zIGxvZ2ljYWxseSBncm91cGVkIHRvZ2V0aGVyLlxuICovXG5leHBvcnQgZnVuY3Rpb24gR3JvdXBJdGVtKFxuICBwcm9wczogR3JvdXBJdGVtLklQcm9wcyAmIFJlYWN0LkhUTUxBdHRyaWJ1dGVzPEhUTUxEaXZFbGVtZW50PlxuKTogUmVhY3QuUmVhY3RFbGVtZW50PEdyb3VwSXRlbS5JUHJvcHM+IHtcbiAgY29uc3QgeyBzcGFjaW5nLCBjaGlsZHJlbiwgY2xhc3NOYW1lLCAuLi5yZXN0IH0gPSBwcm9wcztcbiAgY29uc3QgbnVtQ2hpbGRyZW4gPSBSZWFjdC5DaGlsZHJlbi5jb3VudChjaGlsZHJlbik7XG5cbiAgcmV0dXJuIChcbiAgICA8ZGl2IGNsYXNzTmFtZT17YGpwLVN0YXR1c0Jhci1Hcm91cEl0ZW0gJHtjbGFzc05hbWUgfHwgJyd9YH0gey4uLnJlc3R9PlxuICAgICAge1JlYWN0LkNoaWxkcmVuLm1hcChjaGlsZHJlbiwgKGNoaWxkLCBpKSA9PiB7XG4gICAgICAgIGlmIChpID09PSAwKSB7XG4gICAgICAgICAgcmV0dXJuIDxkaXYgc3R5bGU9e3sgbWFyZ2luUmlnaHQ6IGAke3NwYWNpbmd9cHhgIH19PntjaGlsZH08L2Rpdj47XG4gICAgICAgIH0gZWxzZSBpZiAoaSA9PT0gbnVtQ2hpbGRyZW4gLSAxKSB7XG4gICAgICAgICAgcmV0dXJuIDxkaXYgc3R5bGU9e3sgbWFyZ2luTGVmdDogYCR7c3BhY2luZ31weGAgfX0+e2NoaWxkfTwvZGl2PjtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXR1cm4gPGRpdiBzdHlsZT17eyBtYXJnaW46IGAwcHggJHtzcGFjaW5nfXB4YCB9fT57Y2hpbGR9PC9kaXY+O1xuICAgICAgICB9XG4gICAgICB9KX1cbiAgICA8L2Rpdj5cbiAgKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgR3JvdXBJdGVtIHN0YXRpY3MuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgR3JvdXBJdGVtIHtcbiAgLyoqXG4gICAqIFByb3BzIGZvciB0aGUgR3JvdXBJdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIFRoZSBzcGFjaW5nLCBpbiBweCwgYmV0d2VlbiB0aGUgaXRlbXMgaW4gdGhlIGdyb3VwLlxuICAgICAqL1xuICAgIHNwYWNpbmc6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBpdGVtcyB0byBhcnJhbmdlIGluIGEgZ3JvdXAuXG4gICAgICovXG4gICAgY2hpbGRyZW46IEpTWC5FbGVtZW50W107XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSG92ZXJCb3ggfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBQYW5lbExheW91dCwgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBDcmVhdGUgYW5kIHNob3cgYSBwb3B1cCBjb21wb25lbnQuXG4gKlxuICogQHBhcmFtIG9wdGlvbnMgLSBvcHRpb25zIGZvciB0aGUgcG9wdXBcbiAqXG4gKiBAcmV0dXJucyB0aGUgcG9wdXAgdGhhdCB3YXMgY3JlYXRlZC5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHNob3dQb3B1cChvcHRpb25zOiBQb3B1cC5JT3B0aW9ucyk6IFBvcHVwIHtcbiAgY29uc3QgZGlhbG9nID0gbmV3IFBvcHVwKG9wdGlvbnMpO1xuICBpZiAoIW9wdGlvbnMuc3RhcnRIaWRkZW4pIHtcbiAgICBkaWFsb2cubGF1bmNoKCk7XG4gIH1cbiAgcmV0dXJuIGRpYWxvZztcbn1cblxuLyoqXG4gKiBBIGNsYXNzIGZvciBhIFBvcHVwIHdpZGdldC5cbiAqL1xuZXhwb3J0IGNsYXNzIFBvcHVwIGV4dGVuZHMgV2lkZ2V0IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBQb3B1cC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IE9taXQ8UG9wdXAuSU9wdGlvbnMsICdzdGFydEhpZGRlbic+KSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9ib2R5ID0gb3B0aW9ucy5ib2R5O1xuICAgIHRoaXMuX2JvZHkuYWRkQ2xhc3MoJ2pwLVN0YXR1c0Jhci1Ib3Zlckl0ZW0nKTtcbiAgICB0aGlzLl9hbmNob3IgPSBvcHRpb25zLmFuY2hvcjtcbiAgICB0aGlzLl9hbGlnbiA9IG9wdGlvbnMuYWxpZ247XG4gICAgaWYgKG9wdGlvbnMuaGFzRHluYW1pY1NpemUpIHtcbiAgICAgIHRoaXMuX29ic2VydmVyID0gbmV3IFJlc2l6ZU9ic2VydmVyKCgpID0+IHtcbiAgICAgICAgdGhpcy51cGRhdGUoKTtcbiAgICAgIH0pO1xuICAgIH1cbiAgICBjb25zdCBsYXlvdXQgPSAodGhpcy5sYXlvdXQgPSBuZXcgUGFuZWxMYXlvdXQoKSk7XG4gICAgbGF5b3V0LmFkZFdpZGdldChvcHRpb25zLmJvZHkpO1xuICAgIHRoaXMuX2JvZHkubm9kZS5hZGRFdmVudExpc3RlbmVyKCdyZXNpemUnLCAoKSA9PiB7XG4gICAgICB0aGlzLnVwZGF0ZSgpO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIEF0dGFjaCB0aGUgcG9wdXAgd2lkZ2V0IHRvIHRoZSBwYWdlLlxuICAgKi9cbiAgbGF1bmNoKCk6IHZvaWQge1xuICAgIHRoaXMuX3NldEdlb21ldHJ5KCk7XG4gICAgV2lkZ2V0LmF0dGFjaCh0aGlzLCBkb2N1bWVudC5ib2R5KTtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICAgIHRoaXMuX2FuY2hvci5hZGRDbGFzcygnanAtbW9kLWNsaWNrZWQnKTtcbiAgICB0aGlzLl9hbmNob3IucmVtb3ZlQ2xhc3MoJ2pwLW1vZC1oaWdobGlnaHQnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCd1cGRhdGUnYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvblVwZGF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fc2V0R2VvbWV0cnkoKTtcbiAgICBzdXBlci5vblVwZGF0ZVJlcXVlc3QobXNnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdhZnRlci1hdHRhY2gnYCBtZXNzYWdlcyBmb3IgdGhlIHdpZGdldC5cbiAgICovXG4gIHByb3RlY3RlZCBvbkFmdGVyQXR0YWNoKG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGRvY3VtZW50LmFkZEV2ZW50TGlzdGVuZXIoJ2NsaWNrJywgdGhpcywgZmFsc2UpO1xuICAgIHRoaXMubm9kZS5hZGRFdmVudExpc3RlbmVyKCdrZXlkb3duJywgdGhpcywgZmFsc2UpO1xuICAgIHdpbmRvdy5hZGRFdmVudExpc3RlbmVyKCdyZXNpemUnLCB0aGlzLCBmYWxzZSk7XG4gICAgdGhpcy5fb2JzZXJ2ZXI/Lm9ic2VydmUodGhpcy5fYm9keS5ub2RlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYCdiZWZvcmUtZGV0YWNoJ2AgbWVzc2FnZXMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25CZWZvcmVEZXRhY2gobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fb2JzZXJ2ZXI/LmRpc2Nvbm5lY3QoKTtcbiAgICBkb2N1bWVudC5yZW1vdmVFdmVudExpc3RlbmVyKCdjbGljaycsIHRoaXMsIGZhbHNlKTtcbiAgICB0aGlzLm5vZGUucmVtb3ZlRXZlbnRMaXN0ZW5lcigna2V5ZG93bicsIHRoaXMsIGZhbHNlKTtcbiAgICB3aW5kb3cucmVtb3ZlRXZlbnRMaXN0ZW5lcigncmVzaXplJywgdGhpcywgZmFsc2UpO1xuICB9XG5cbiAgLyoqXG4gICAqIEhhbmRsZSBgJ3Jlc2l6ZSdgIG1lc3NhZ2VzIGZvciB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgcHJvdGVjdGVkIG9uUmVzaXplKCk6IHZvaWQge1xuICAgIHRoaXMudXBkYXRlKCk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgd2lkZ2V0LlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICB0aGlzLl9vYnNlcnZlcj8uZGlzY29ubmVjdCgpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgICB0aGlzLl9hbmNob3IucmVtb3ZlQ2xhc3MoJ2pwLW1vZC1jbGlja2VkJyk7XG4gICAgdGhpcy5fYW5jaG9yLmFkZENsYXNzKCdqcC1tb2QtaGlnaGxpZ2h0Jyk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIERPTSBldmVudHMgZm9yIHRoZSB3aWRnZXQuXG4gICAqL1xuICBoYW5kbGVFdmVudChldmVudDogRXZlbnQpOiB2b2lkIHtcbiAgICBzd2l0Y2ggKGV2ZW50LnR5cGUpIHtcbiAgICAgIGNhc2UgJ2tleWRvd24nOlxuICAgICAgICB0aGlzLl9ldnRLZXlkb3duKGV2ZW50IGFzIEtleWJvYXJkRXZlbnQpO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2NsaWNrJzpcbiAgICAgICAgdGhpcy5fZXZ0Q2xpY2soZXZlbnQgYXMgTW91c2VFdmVudCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAncmVzaXplJzpcbiAgICAgICAgdGhpcy5vblJlc2l6ZSgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2V2dENsaWNrKGV2ZW50OiBNb3VzZUV2ZW50KTogdm9pZCB7XG4gICAgaWYgKFxuICAgICAgISFldmVudC50YXJnZXQgJiZcbiAgICAgICEoXG4gICAgICAgIHRoaXMuX2JvZHkubm9kZS5jb250YWlucyhldmVudC50YXJnZXQgYXMgSFRNTEVsZW1lbnQpIHx8XG4gICAgICAgIHRoaXMuX2FuY2hvci5ub2RlLmNvbnRhaW5zKGV2ZW50LnRhcmdldCBhcyBIVE1MRWxlbWVudClcbiAgICAgIClcbiAgICApIHtcbiAgICAgIHRoaXMuZGlzcG9zZSgpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2V2dEtleWRvd24oZXZlbnQ6IEtleWJvYXJkRXZlbnQpOiB2b2lkIHtcbiAgICAvLyBDaGVjayBmb3IgZXNjYXBlIGtleVxuICAgIHN3aXRjaCAoZXZlbnQua2V5Q29kZSkge1xuICAgICAgY2FzZSAyNzogLy8gRXNjYXBlLlxuICAgICAgICBldmVudC5zdG9wUHJvcGFnYXRpb24oKTtcbiAgICAgICAgZXZlbnQucHJldmVudERlZmF1bHQoKTtcbiAgICAgICAgdGhpcy5kaXNwb3NlKCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgYnJlYWs7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfc2V0R2VvbWV0cnkoKTogdm9pZCB7XG4gICAgbGV0IGFsaWduZWQgPSAwO1xuICAgIGNvbnN0IGFuY2hvclJlY3QgPSB0aGlzLl9hbmNob3Iubm9kZS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKTtcbiAgICBjb25zdCBib2R5UmVjdCA9IHRoaXMuX2JvZHkubm9kZS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKTtcbiAgICBpZiAodGhpcy5fYWxpZ24gPT09ICdyaWdodCcpIHtcbiAgICAgIGFsaWduZWQgPSAtKGJvZHlSZWN0LndpZHRoIC0gYW5jaG9yUmVjdC53aWR0aCk7XG4gICAgfVxuICAgIGNvbnN0IHN0eWxlID0gd2luZG93LmdldENvbXB1dGVkU3R5bGUodGhpcy5fYm9keS5ub2RlKTtcbiAgICBIb3ZlckJveC5zZXRHZW9tZXRyeSh7XG4gICAgICBhbmNob3I6IGFuY2hvclJlY3QsXG4gICAgICBob3N0OiBkb2N1bWVudC5ib2R5LFxuICAgICAgbWF4SGVpZ2h0OiA1MDAsXG4gICAgICBtaW5IZWlnaHQ6IDIwLFxuICAgICAgbm9kZTogdGhpcy5fYm9keS5ub2RlLFxuICAgICAgb2Zmc2V0OiB7XG4gICAgICAgIGhvcml6b250YWw6IGFsaWduZWRcbiAgICAgIH0sXG4gICAgICBwcml2aWxlZ2U6ICdmb3JjZUFib3ZlJyxcbiAgICAgIHN0eWxlXG4gICAgfSk7XG4gIH1cblxuICBwcml2YXRlIF9ib2R5OiBXaWRnZXQ7XG4gIHByaXZhdGUgX2FuY2hvcjogV2lkZ2V0O1xuICBwcml2YXRlIF9hbGlnbjogJ2xlZnQnIHwgJ3JpZ2h0JyB8IHVuZGVmaW5lZDtcbiAgcHJpdmF0ZSBfb2JzZXJ2ZXI6IFJlc2l6ZU9ic2VydmVyIHwgbnVsbDtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgUG9wdXAgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBQb3B1cCB7XG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBjcmVhdGluZyBhIFBvcHVwIHdpZGdldC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBjb250ZW50IG9mIHRoZSBwb3B1cC5cbiAgICAgKi9cbiAgICBib2R5OiBXaWRnZXQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgd2lkZ2V0IHRvIHdoaWNoIHdlIGFyZSBhdHRhY2hpbmcgdGhlIHBvcHVwLlxuICAgICAqL1xuICAgIGFuY2hvcjogV2lkZ2V0O1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBhbGlnbiB0aGUgcG9wdXAgdG8gdGhlIGxlZnQgb3IgdGhlIHJpZ2h0IG9mIHRoZSBhbmNob3IuXG4gICAgICovXG4gICAgYWxpZ24/OiAnbGVmdCcgfCAncmlnaHQnO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgYm9keSBoYXMgZHluYW1pYyBzaXplIG9yIG5vdC5cbiAgICAgKiBCeSBkZWZhdWx0LCB0aGlzIGlzIGBmYWxzZWAuXG4gICAgICovXG4gICAgaGFzRHluYW1pY1NpemU/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0byBzdGFydCB0aGUgcG9wdXAgaW4gaGlkZGVuIG1vZGUgb3Igbm90LlxuICAgICAqIEJ5IGRlZmF1bHQsIHRoaXMgaXMgYGZhbHNlYC5cbiAgICAgKlxuICAgICAqICMjIyBOb3RlXG4gICAgICogVGhlIHBvcHVwIGNhbiBiZSBkaXNwbGF5ZWQgdXNpbmcgYGxhdW5jaGAgbWV0aG9kLlxuICAgICAqL1xuICAgIHN0YXJ0SGlkZGVuPzogYm9vbGVhbjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5leHBvcnQgKiBmcm9tICcuL2dyb3VwJztcbmV4cG9ydCAqIGZyb20gJy4vaG92ZXInO1xuZXhwb3J0ICogZnJvbSAnLi9wcm9ncmVzc0Jhcic7XG5leHBvcnQgKiBmcm9tICcuL3RleHQnO1xuZXhwb3J0ICogZnJvbSAnLi9wcm9ncmVzc0NpcmNsZSc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgUHJvZ3Jlc3NCYXIgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBQcm9ncmVzc0JhciB7XG4gIC8qKlxuICAgKiBQcm9wcyBmb3IgdGhlIFByb2dyZXNzQmFyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIFRoZSBjdXJyZW50IHByb2dyZXNzIHBlcmNlbnRhZ2UsIGZyb20gMCB0byAxMDBcbiAgICAgKi9cbiAgICBwZXJjZW50YWdlOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBXaWR0aCBvZiBwcm9ncmVzcyBiYXIgaW4gcGl4ZWwuXG4gICAgICovXG4gICAgd2lkdGg/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUZXh0IHRvIHNob3cgaW5zaWRlIHByb2dyZXNzIGJhci5cbiAgICAgKi9cbiAgICBjb250ZW50Pzogc3RyaW5nO1xuICB9XG59XG5cbi8qKlxuICogQSBmdW5jdGlvbmFsIHRzeCBjb21wb25lbnQgZm9yIGEgcHJvZ3Jlc3MgYmFyLlxuICovXG5leHBvcnQgZnVuY3Rpb24gUHJvZ3Jlc3NCYXIocHJvcHM6IFByb2dyZXNzQmFyLklQcm9wcyk6IEpTWC5FbGVtZW50IHtcbiAgY29uc3QgeyB3aWR0aCwgcGVyY2VudGFnZSwgLi4ucmVzdCB9ID0gcHJvcHM7XG4gIHJldHVybiAoXG4gICAgPGRpdlxuICAgICAgY2xhc3NOYW1lPXsnanAtU3RhdHVzYmFyLVByb2dyZXNzQmFyLXByb2dyZXNzLWJhcid9XG4gICAgICByb2xlPVwicHJvZ3Jlc3NiYXJcIlxuICAgICAgYXJpYS12YWx1ZW1pbj17MH1cbiAgICAgIGFyaWEtdmFsdWVtYXg9ezEwMH1cbiAgICAgIGFyaWEtdmFsdWVub3c9e3BlcmNlbnRhZ2V9XG4gICAgPlxuICAgICAgPEZpbGxlciB7Li4ueyBwZXJjZW50YWdlLCAuLi5yZXN0IH19IGNvbnRlbnRXaWR0aD17d2lkdGh9IC8+XG4gICAgPC9kaXY+XG4gICk7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIEZpbGxlciBzdGF0aWNzLlxuICovXG5uYW1lc3BhY2UgRmlsbGVyIHtcbiAgLyoqXG4gICAqIFByb3BzIGZvciB0aGUgRmlsbGVyIGNvbXBvbmVudC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBwZXJjZW50YWdlIGZpbGxlZCwgZnJvbSAwIHRvIDEwMFxuICAgICAqL1xuICAgIHBlcmNlbnRhZ2U6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFdpZHRoIG9mIGNvbnRlbnQgaW5zaWRlIGZpbGxlci5cbiAgICAgKi9cbiAgICBjb250ZW50V2lkdGg/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUZXh0IHRvIHNob3cgaW5zaWRlIGZpbGxlci5cbiAgICAgKi9cbiAgICBjb250ZW50Pzogc3RyaW5nO1xuICB9XG59XG5cbi8qKlxuICogQSBmdW5jdGlvbmFsIHRzeCBjb21wb25lbnQgZm9yIGEgcGFydGlhbGx5IGZpbGxlZCBkaXYuXG4gKi9cbmZ1bmN0aW9uIEZpbGxlcihwcm9wczogRmlsbGVyLklQcm9wcykge1xuICByZXR1cm4gKFxuICAgIDxkaXZcbiAgICAgIHN0eWxlPXt7XG4gICAgICAgIHdpZHRoOiBgJHtwcm9wcy5wZXJjZW50YWdlfSVgXG4gICAgICB9fVxuICAgID5cbiAgICAgIDxwPntwcm9wcy5jb250ZW50fTwvcD5cbiAgICA8L2Rpdj5cbiAgKTtcbn1cbiIsIi8qXG4gKiBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbiAqIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4gKi9cblxuaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmV4cG9ydCBuYW1lc3BhY2UgUHJvZ3Jlc3NDaXJjbGUge1xuICAvKipcbiAgICogUHJvcHMgZm9yIHRoZSBQcm9ncmVzc0Jhci5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY3VycmVudCBwcm9ncmVzcyBwZXJjZW50YWdlLCBmcm9tIDAgdG8gMTAwXG4gICAgICovXG4gICAgcHJvZ3Jlc3M6IG51bWJlcjtcbiAgICAvKipcbiAgICAgKiBUaGUgYXJpYS1sYWJlbCBmb3IgdGhlIHdpZGdldFxuICAgICAqL1xuICAgIGxhYmVsPzogc3RyaW5nO1xuICAgIC8qKlxuICAgICAqIEVsZW1lbnQgd2lkdGhcbiAgICAgKi9cbiAgICB3aWR0aD86IG51bWJlcjtcbiAgICAvKipcbiAgICAgKiBFbGVtZW50IGhlaWdodFxuICAgICAqL1xuICAgIGhlaWdodD86IG51bWJlcjtcbiAgfVxufVxuXG5leHBvcnQgZnVuY3Rpb24gUHJvZ3Jlc3NDaXJjbGUocHJvcHM6IFByb2dyZXNzQ2lyY2xlLklQcm9wcyk6IEpTWC5FbGVtZW50IHtcbiAgY29uc3QgcmFkaXVzID0gMTA0O1xuICBjb25zdCBkID0gKHByb2dyZXNzOiBudW1iZXIpOiBzdHJpbmcgPT4ge1xuICAgIGNvbnN0IGFuZ2xlID0gTWF0aC5tYXgocHJvZ3Jlc3MgKiAzLjYsIDAuMSk7XG4gICAgY29uc3QgcmFkID0gKGFuZ2xlICogTWF0aC5QSSkgLyAxODAsXG4gICAgICB4ID0gTWF0aC5zaW4ocmFkKSAqIHJhZGl1cyxcbiAgICAgIHkgPSBNYXRoLmNvcyhyYWQpICogLXJhZGl1cyxcbiAgICAgIG1pZCA9IGFuZ2xlIDwgMTgwID8gMSA6IDAsXG4gICAgICBzaGFwZSA9XG4gICAgICAgIGBNIDAgMCB2IC0ke3JhZGl1c30gQSAke3JhZGl1c30gJHtyYWRpdXN9IDEgYCArXG4gICAgICAgIG1pZCArXG4gICAgICAgICcgMCAnICtcbiAgICAgICAgeC50b0ZpeGVkKDQpICtcbiAgICAgICAgJyAnICtcbiAgICAgICAgeS50b0ZpeGVkKDQpICtcbiAgICAgICAgJyB6JztcbiAgICByZXR1cm4gc2hhcGU7XG4gIH07XG4gIHJldHVybiAoXG4gICAgPGRpdlxuICAgICAgY2xhc3NOYW1lPXsnanAtU3RhdHVzYmFyLVByb2dyZXNzQ2lyY2xlJ31cbiAgICAgIHJvbGU9XCJwcm9ncmVzc2JhclwiXG4gICAgICBhcmlhLWxhYmVsPXtwcm9wcy5sYWJlbCB8fCAnVW5sYWJlbGxlZCBwcm9ncmVzcyBjaXJjbGUnfVxuICAgICAgYXJpYS12YWx1ZW1pbj17MH1cbiAgICAgIGFyaWEtdmFsdWVtYXg9ezEwMH1cbiAgICAgIGFyaWEtdmFsdWVub3c9e3Byb3BzLnByb2dyZXNzfVxuICAgID5cbiAgICAgIDxzdmcgdmlld0JveD1cIjAgMCAyNTAgMjUwXCI+XG4gICAgICAgIDxjaXJjbGVcbiAgICAgICAgICBjeD1cIjEyNVwiXG4gICAgICAgICAgY3k9XCIxMjVcIlxuICAgICAgICAgIHI9e2Ake3JhZGl1c31gfVxuICAgICAgICAgIHN0cm9rZT1cInZhcigtLWpwLWludmVyc2UtbGF5b3V0LWNvbG9yMylcIlxuICAgICAgICAgIHN0cm9rZVdpZHRoPVwiMjBcIlxuICAgICAgICAgIGZpbGw9XCJub25lXCJcbiAgICAgICAgLz5cbiAgICAgICAgPHBhdGhcbiAgICAgICAgICB0cmFuc2Zvcm09XCJ0cmFuc2xhdGUoMTI1LDEyNSkgc2NhbGUoLjkpXCJcbiAgICAgICAgICBkPXtkKHByb3BzLnByb2dyZXNzKX1cbiAgICAgICAgICBmaWxsPXsndmFyKC0tanAtaW52ZXJzZS1sYXlvdXQtY29sb3IzKSd9XG4gICAgICAgIC8+XG4gICAgICA8L3N2Zz5cbiAgICA8L2Rpdj5cbiAgKTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBUZXh0SXRlbSBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFRleHRJdGVtIHtcbiAgLyoqXG4gICAqIFByb3BzIGZvciBhIFRleHRJdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcHMge1xuICAgIC8qKlxuICAgICAqIFRoZSBjb250ZW50IG9mIHRoZSB0ZXh0IGl0ZW0uXG4gICAgICovXG4gICAgc291cmNlOiBzdHJpbmcgfCBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBIb3ZlciB0ZXh0IHRvIGdpdmUgdG8gdGhlIG5vZGUuXG4gICAgICovXG4gICAgdGl0bGU/OiBzdHJpbmc7XG4gIH1cbn1cblxuLyoqXG4gKiBBIGZ1bmN0aW9uYWwgdHN4IGNvbXBvbmVudCBmb3IgYSB0ZXh0IGl0ZW0uXG4gKi9cbmV4cG9ydCBmdW5jdGlvbiBUZXh0SXRlbShcbiAgcHJvcHM6IFRleHRJdGVtLklQcm9wcyAmIFJlYWN0LkhUTUxBdHRyaWJ1dGVzPEhUTUxTcGFuRWxlbWVudD5cbik6IFJlYWN0LlJlYWN0RWxlbWVudDxUZXh0SXRlbS5JUHJvcHM+IHtcbiAgY29uc3QgeyB0aXRsZSwgc291cmNlLCBjbGFzc05hbWUsIC4uLnJlc3QgfSA9IHByb3BzO1xuICByZXR1cm4gKFxuICAgIDxzcGFuXG4gICAgICBjbGFzc05hbWU9e2BqcC1TdGF0dXNCYXItVGV4dEl0ZW0gJHtjbGFzc05hbWV9YH1cbiAgICAgIHRpdGxlPXt0aXRsZX1cbiAgICAgIHsuLi5yZXN0fVxuICAgID5cbiAgICAgIHtzb3VyY2V9XG4gICAgPC9zcGFuPlxuICApO1xufVxuIiwiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBzdGF0dXNiYXJcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL2NvbXBvbmVudHMnO1xuZXhwb3J0ICogZnJvbSAnLi9zdGF0dXNiYXInO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBBcnJheUV4dCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7XG4gIERpc3Bvc2FibGVEZWxlZ2F0ZSxcbiAgRGlzcG9zYWJsZVNldCxcbiAgSURpc3Bvc2FibGVcbn0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBQYW5lbCwgUGFuZWxMYXlvdXQsIFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBJU3RhdHVzQmFyIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIE1haW4gc3RhdHVzIGJhciBvYmplY3Qgd2hpY2ggY29udGFpbnMgYWxsIGl0ZW1zLlxuICovXG5leHBvcnQgY2xhc3MgU3RhdHVzQmFyIGV4dGVuZHMgV2lkZ2V0IGltcGxlbWVudHMgSVN0YXR1c0JhciB7XG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtU3RhdHVzQmFyLVdpZGdldCcpO1xuXG4gICAgY29uc3Qgcm9vdExheW91dCA9ICh0aGlzLmxheW91dCA9IG5ldyBQYW5lbExheW91dCgpKTtcblxuICAgIGNvbnN0IGxlZnRQYW5lbCA9ICh0aGlzLl9sZWZ0U2lkZSA9IG5ldyBQYW5lbCgpKTtcbiAgICBjb25zdCBtaWRkbGVQYW5lbCA9ICh0aGlzLl9taWRkbGVQYW5lbCA9IG5ldyBQYW5lbCgpKTtcbiAgICBjb25zdCByaWdodFBhbmVsID0gKHRoaXMuX3JpZ2h0U2lkZSA9IG5ldyBQYW5lbCgpKTtcblxuICAgIGxlZnRQYW5lbC5hZGRDbGFzcygnanAtU3RhdHVzQmFyLUxlZnQnKTtcbiAgICBtaWRkbGVQYW5lbC5hZGRDbGFzcygnanAtU3RhdHVzQmFyLU1pZGRsZScpO1xuICAgIHJpZ2h0UGFuZWwuYWRkQ2xhc3MoJ2pwLVN0YXR1c0Jhci1SaWdodCcpO1xuXG4gICAgcm9vdExheW91dC5hZGRXaWRnZXQobGVmdFBhbmVsKTtcbiAgICByb290TGF5b3V0LmFkZFdpZGdldChtaWRkbGVQYW5lbCk7XG4gICAgcm9vdExheW91dC5hZGRXaWRnZXQocmlnaHRQYW5lbCk7XG4gIH1cblxuICAvKipcbiAgICogUmVnaXN0ZXIgYSBuZXcgc3RhdHVzIGl0ZW0uXG4gICAqXG4gICAqIEBwYXJhbSBpZCAtIGEgdW5pcXVlIGlkIGZvciB0aGUgc3RhdHVzIGl0ZW0uXG4gICAqXG4gICAqIEBwYXJhbSBzdGF0dXNJdGVtIC0gVGhlIGl0ZW0gdG8gYWRkIHRvIHRoZSBzdGF0dXMgYmFyLlxuICAgKi9cbiAgcmVnaXN0ZXJTdGF0dXNJdGVtKGlkOiBzdHJpbmcsIHN0YXR1c0l0ZW06IElTdGF0dXNCYXIuSUl0ZW0pOiBJRGlzcG9zYWJsZSB7XG4gICAgaWYgKGlkIGluIHRoaXMuX3N0YXR1c0l0ZW1zKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYFN0YXR1cyBpdGVtICR7aWR9IGFscmVhZHkgcmVnaXN0ZXJlZC5gKTtcbiAgICB9XG5cbiAgICAvLyBQb3B1bGF0ZSBkZWZhdWx0cyBmb3IgdGhlIG9wdGlvbmFsIHByb3BlcnRpZXMgb2YgdGhlIHN0YXR1cyBpdGVtLlxuICAgIGNvbnN0IGZ1bGxTdGF0dXNJdGVtID0ge1xuICAgICAgLi4uUHJpdmF0ZS5zdGF0dXNJdGVtRGVmYXVsdHMsXG4gICAgICAuLi5zdGF0dXNJdGVtXG4gICAgfSBhcyBQcml2YXRlLklGdWxsSXRlbTtcbiAgICBjb25zdCB7IGFsaWduLCBpdGVtLCByYW5rIH0gPSBmdWxsU3RhdHVzSXRlbTtcblxuICAgIC8vIENvbm5lY3QgdGhlIGFjdGl2ZVN0YXRlQ2hhbmdlZCBzaWduYWwgdG8gcmVmcmVzaGluZyB0aGUgc3RhdHVzIGl0ZW0sXG4gICAgLy8gaWYgdGhlIHNpZ25hbCB3YXMgcHJvdmlkZWQuXG4gICAgY29uc3Qgb25BY3RpdmVTdGF0ZUNoYW5nZWQgPSAoKSA9PiB7XG4gICAgICB0aGlzLl9yZWZyZXNoSXRlbShpZCk7XG4gICAgfTtcbiAgICBpZiAoZnVsbFN0YXR1c0l0ZW0uYWN0aXZlU3RhdGVDaGFuZ2VkKSB7XG4gICAgICBmdWxsU3RhdHVzSXRlbS5hY3RpdmVTdGF0ZUNoYW5nZWQuY29ubmVjdChvbkFjdGl2ZVN0YXRlQ2hhbmdlZCk7XG4gICAgfVxuXG4gICAgY29uc3QgcmFua0l0ZW0gPSB7IGlkLCByYW5rIH07XG5cbiAgICBmdWxsU3RhdHVzSXRlbS5pdGVtLmFkZENsYXNzKCdqcC1TdGF0dXNCYXItSXRlbScpO1xuICAgIHRoaXMuX3N0YXR1c0l0ZW1zW2lkXSA9IGZ1bGxTdGF0dXNJdGVtO1xuXG4gICAgaWYgKGFsaWduID09PSAnbGVmdCcpIHtcbiAgICAgIGNvbnN0IGluc2VydEluZGV4ID0gdGhpcy5fZmluZEluc2VydEluZGV4KHRoaXMuX2xlZnRSYW5rSXRlbXMsIHJhbmtJdGVtKTtcbiAgICAgIGlmIChpbnNlcnRJbmRleCA9PT0gLTEpIHtcbiAgICAgICAgdGhpcy5fbGVmdFNpZGUuYWRkV2lkZ2V0KGl0ZW0pO1xuICAgICAgICB0aGlzLl9sZWZ0UmFua0l0ZW1zLnB1c2gocmFua0l0ZW0pO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgQXJyYXlFeHQuaW5zZXJ0KHRoaXMuX2xlZnRSYW5rSXRlbXMsIGluc2VydEluZGV4LCByYW5rSXRlbSk7XG4gICAgICAgIHRoaXMuX2xlZnRTaWRlLmluc2VydFdpZGdldChpbnNlcnRJbmRleCwgaXRlbSk7XG4gICAgICB9XG4gICAgfSBlbHNlIGlmIChhbGlnbiA9PT0gJ3JpZ2h0Jykge1xuICAgICAgY29uc3QgaW5zZXJ0SW5kZXggPSB0aGlzLl9maW5kSW5zZXJ0SW5kZXgodGhpcy5fcmlnaHRSYW5rSXRlbXMsIHJhbmtJdGVtKTtcbiAgICAgIGlmIChpbnNlcnRJbmRleCA9PT0gLTEpIHtcbiAgICAgICAgdGhpcy5fcmlnaHRTaWRlLmFkZFdpZGdldChpdGVtKTtcbiAgICAgICAgdGhpcy5fcmlnaHRSYW5rSXRlbXMucHVzaChyYW5rSXRlbSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBBcnJheUV4dC5pbnNlcnQodGhpcy5fcmlnaHRSYW5rSXRlbXMsIGluc2VydEluZGV4LCByYW5rSXRlbSk7XG4gICAgICAgIHRoaXMuX3JpZ2h0U2lkZS5pbnNlcnRXaWRnZXQoaW5zZXJ0SW5kZXgsIGl0ZW0pO1xuICAgICAgfVxuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9taWRkbGVQYW5lbC5hZGRXaWRnZXQoaXRlbSk7XG4gICAgfVxuICAgIHRoaXMuX3JlZnJlc2hJdGVtKGlkKTsgLy8gSW5pdGlhbGx5IHJlZnJlc2ggdGhlIHN0YXR1cyBpdGVtLlxuXG4gICAgY29uc3QgZGlzcG9zYWJsZSA9IG5ldyBEaXNwb3NhYmxlRGVsZWdhdGUoKCkgPT4ge1xuICAgICAgZGVsZXRlIHRoaXMuX3N0YXR1c0l0ZW1zW2lkXTtcbiAgICAgIGlmIChmdWxsU3RhdHVzSXRlbS5hY3RpdmVTdGF0ZUNoYW5nZWQpIHtcbiAgICAgICAgZnVsbFN0YXR1c0l0ZW0uYWN0aXZlU3RhdGVDaGFuZ2VkLmRpc2Nvbm5lY3Qob25BY3RpdmVTdGF0ZUNoYW5nZWQpO1xuICAgICAgfVxuICAgICAgaXRlbS5wYXJlbnQgPSBudWxsO1xuICAgICAgaXRlbS5kaXNwb3NlKCk7XG4gICAgfSk7XG4gICAgdGhpcy5fZGlzcG9zYWJsZXMuYWRkKGRpc3Bvc2FibGUpO1xuICAgIHJldHVybiBkaXNwb3NhYmxlO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2Ugb2YgdGhlIHN0YXR1cyBiYXIuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIHRoaXMuX2xlZnRSYW5rSXRlbXMubGVuZ3RoID0gMDtcbiAgICB0aGlzLl9yaWdodFJhbmtJdGVtcy5sZW5ndGggPSAwO1xuICAgIHRoaXMuX2Rpc3Bvc2FibGVzLmRpc3Bvc2UoKTtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIGFuICd1cGRhdGUtcmVxdWVzdCcgbWVzc2FnZSB0byB0aGUgc3RhdHVzIGJhci5cbiAgICovXG4gIHByb3RlY3RlZCBvblVwZGF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgdGhpcy5fcmVmcmVzaEFsbCgpO1xuICAgIHN1cGVyLm9uVXBkYXRlUmVxdWVzdChtc2cpO1xuICB9XG5cbiAgcHJpdmF0ZSBfZmluZEluc2VydEluZGV4KFxuICAgIHNpZGU6IFByaXZhdGUuSVJhbmtJdGVtW10sXG4gICAgbmV3SXRlbTogUHJpdmF0ZS5JUmFua0l0ZW1cbiAgKTogbnVtYmVyIHtcbiAgICByZXR1cm4gQXJyYXlFeHQuZmluZEZpcnN0SW5kZXgoc2lkZSwgaXRlbSA9PiBpdGVtLnJhbmsgPiBuZXdJdGVtLnJhbmspO1xuICB9XG5cbiAgcHJpdmF0ZSBfcmVmcmVzaEl0ZW0oaWQ6IHN0cmluZykge1xuICAgIGNvbnN0IHN0YXR1c0l0ZW0gPSB0aGlzLl9zdGF0dXNJdGVtc1tpZF07XG4gICAgaWYgKHN0YXR1c0l0ZW0uaXNBY3RpdmUoKSkge1xuICAgICAgc3RhdHVzSXRlbS5pdGVtLnNob3coKTtcbiAgICAgIHN0YXR1c0l0ZW0uaXRlbS51cGRhdGUoKTtcbiAgICB9IGVsc2Uge1xuICAgICAgc3RhdHVzSXRlbS5pdGVtLmhpZGUoKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9yZWZyZXNoQWxsKCk6IHZvaWQge1xuICAgIE9iamVjdC5rZXlzKHRoaXMuX3N0YXR1c0l0ZW1zKS5mb3JFYWNoKGlkID0+IHtcbiAgICAgIHRoaXMuX3JlZnJlc2hJdGVtKGlkKTtcbiAgICB9KTtcbiAgfVxuXG4gIHByaXZhdGUgX2xlZnRSYW5rSXRlbXM6IFByaXZhdGUuSVJhbmtJdGVtW10gPSBbXTtcbiAgcHJpdmF0ZSBfcmlnaHRSYW5rSXRlbXM6IFByaXZhdGUuSVJhbmtJdGVtW10gPSBbXTtcbiAgcHJpdmF0ZSBfc3RhdHVzSXRlbXM6IHsgW2lkOiBzdHJpbmddOiBQcml2YXRlLklGdWxsSXRlbSB9ID0ge307XG4gIHByaXZhdGUgX2Rpc3Bvc2FibGVzID0gbmV3IERpc3Bvc2FibGVTZXQoKTtcbiAgcHJpdmF0ZSBfbGVmdFNpZGU6IFBhbmVsO1xuICBwcml2YXRlIF9taWRkbGVQYW5lbDogUGFuZWw7XG4gIHByaXZhdGUgX3JpZ2h0U2lkZTogUGFuZWw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgZnVuY3Rpb25hbGl0eS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICB0eXBlIE9taXQ8VCwgSyBleHRlbmRzIGtleW9mIFQ+ID0gUGljazxULCBFeGNsdWRlPGtleW9mIFQsIEs+PjtcbiAgLyoqXG4gICAqIERlZmF1bHQgb3B0aW9ucyBmb3IgYSBzdGF0dXMgaXRlbSwgbGVzcyB0aGUgaXRlbSBpdHNlbGYuXG4gICAqL1xuICBleHBvcnQgY29uc3Qgc3RhdHVzSXRlbURlZmF1bHRzOiBPbWl0PElTdGF0dXNCYXIuSUl0ZW0sICdpdGVtJz4gPSB7XG4gICAgYWxpZ246ICdsZWZ0JyxcbiAgICByYW5rOiAwLFxuICAgIGlzQWN0aXZlOiAoKSA9PiB0cnVlLFxuICAgIGFjdGl2ZVN0YXRlQ2hhbmdlZDogdW5kZWZpbmVkXG4gIH07XG5cbiAgLyoqXG4gICAqIEFuIGludGVyZmFjZSBmb3Igc3RvcmluZyB0aGUgcmFuayBvZiBhIHN0YXR1cyBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUmFua0l0ZW0ge1xuICAgIGlkOiBzdHJpbmc7XG4gICAgcmFuazogbnVtYmVyO1xuICB9XG5cbiAgZXhwb3J0IHR5cGUgRGVmYXVsdEtleXMgPSAnYWxpZ24nIHwgJ3JhbmsnIHwgJ2lzQWN0aXZlJztcblxuICAvKipcbiAgICogVHlwZSBvZiBzdGF0dXNiYXIgaXRlbSB3aXRoIGRlZmF1bHRzIGZpbGxlZCBpbi5cbiAgICovXG4gIGV4cG9ydCB0eXBlIElGdWxsSXRlbSA9IFJlcXVpcmVkPFBpY2s8SVN0YXR1c0Jhci5JSXRlbSwgRGVmYXVsdEtleXM+PiAmXG4gICAgT21pdDxJU3RhdHVzQmFyLklJdGVtLCBEZWZhdWx0S2V5cz47XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgSVNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8vIHRzbGludDpkaXNhYmxlLW5leHQtbGluZTp2YXJpYWJsZS1uYW1lXG5leHBvcnQgY29uc3QgSVN0YXR1c0JhciA9IG5ldyBUb2tlbjxJU3RhdHVzQmFyPihcbiAgJ0BqdXB5dGVybGFiL3N0YXR1c2JhcjpJU3RhdHVzQmFyJyxcbiAgJ0Egc2VydmljZSBmb3IgdGhlIHN0YXR1cyBiYXIgb24gdGhlIGFwcGxpY2F0aW9uLiBVc2UgdGhpcyBpZiB5b3Ugd2FudCB0byBhZGQgbmV3IHN0YXR1cyBiYXIgaXRlbXMuJ1xuKTtcblxuLyoqXG4gKiBNYWluIHN0YXR1cyBiYXIgb2JqZWN0IHdoaWNoIGNvbnRhaW5zIGFsbCB3aWRnZXRzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElTdGF0dXNCYXIge1xuICAvKipcbiAgICogUmVnaXN0ZXIgYSBuZXcgc3RhdHVzIGl0ZW0uXG4gICAqXG4gICAqIEBwYXJhbSBpZCAtIGEgdW5pcXVlIGlkIGZvciB0aGUgc3RhdHVzIGl0ZW0uXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIG9wdGlvbnMgZm9yIGhvdyB0byBhZGQgdGhlIHN0YXR1cyBpdGVtLlxuICAgKlxuICAgKiBAcmV0dXJucyBhbiBgSURpc3Bvc2FibGVgIHRoYXQgY2FuIGJlIGRpc3Bvc2VkIHRvIHJlbW92ZSB0aGUgaXRlbS5cbiAgICovXG4gIHJlZ2lzdGVyU3RhdHVzSXRlbShpZDogc3RyaW5nLCBzdGF0dXNJdGVtOiBJU3RhdHVzQmFyLklJdGVtKTogSURpc3Bvc2FibGU7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHN0YXR1cyBiYXIgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJU3RhdHVzQmFyIHtcbiAgZXhwb3J0IHR5cGUgQWxpZ25tZW50ID0gJ3JpZ2h0JyB8ICdsZWZ0JyB8ICdtaWRkbGUnO1xuXG4gIC8qKlxuICAgKiBPcHRpb25zIGZvciBzdGF0dXMgYmFyIGl0ZW1zLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJSXRlbSB7XG4gICAgLyoqXG4gICAgICogVGhlIGl0ZW0gdG8gYWRkIHRvIHRoZSBzdGF0dXMgYmFyLlxuICAgICAqL1xuICAgIGl0ZW06IFdpZGdldDtcblxuICAgIC8qKlxuICAgICAqIFdoaWNoIHNpZGUgdG8gcGxhY2UgaXRlbS5cbiAgICAgKiBQZXJtYW5lbnQgaXRlbXMgYXJlIGludGVuZGVkIGZvciB0aGUgcmlnaHQgYW5kIGxlZnQgc2lkZSxcbiAgICAgKiB3aXRoIG1vcmUgdHJhbnNpZW50IGl0ZW1zIGluIHRoZSBtaWRkbGUuXG4gICAgICovXG4gICAgYWxpZ24/OiBBbGlnbm1lbnQ7XG5cbiAgICAvKipcbiAgICAgKiAgT3JkZXJpbmcgb2YgSXRlbXMgLS0gaGlnaGVyIHJhbmsgaXRlbXMgYXJlIGNsb3NlciB0byB0aGUgbWlkZGxlLlxuICAgICAqL1xuICAgIHJhbms/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBpdGVtIGlzIHNob3duIG9yIGhpZGRlbi5cbiAgICAgKi9cbiAgICBpc0FjdGl2ZT86ICgpID0+IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBBIHNpZ25hbCB0aGF0IGlzIGZpcmVkIHdoZW4gdGhlIGl0ZW0gYWN0aXZlIHN0YXRlIGNoYW5nZXMuXG4gICAgICovXG4gICAgYWN0aXZlU3RhdGVDaGFuZ2VkPzogSVNpZ25hbDxhbnksIHZvaWQ+O1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=