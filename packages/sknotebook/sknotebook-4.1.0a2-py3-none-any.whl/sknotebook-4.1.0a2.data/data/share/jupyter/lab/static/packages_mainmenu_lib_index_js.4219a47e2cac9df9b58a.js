"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mainmenu_lib_index_js"],{

/***/ "../packages/mainmenu/lib/edit.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/edit.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditMenu": () => (/* binding */ EditMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Edit menu for the application.
 */
class EditMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the edit menu.
     */
    constructor(options) {
        super(options);
        this.undoers = {
            redo: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            undo: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand()
        };
        this.clearers = {
            clearAll: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            clearCurrent: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand()
        };
        this.goToLiners = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/file.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/file.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FileMenu": () => (/* binding */ FileMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * An extensible FileMenu for the application.
 */
class FileMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    constructor(options) {
        super(options);
        this.quitEntry = false;
        this.closeAndCleaners = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.SemanticCommand();
        this.consoleCreators = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.SemanticCommand();
    }
    /**
     * The New submenu.
     */
    get newMenu() {
        var _a, _b;
        if (!this._newMenu) {
            this._newMenu =
                (_b = (_a = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.find)(this.items, menu => { var _a; return ((_a = menu.submenu) === null || _a === void 0 ? void 0 : _a.id) === 'jp-mainmenu-file-new'; })) === null || _a === void 0 ? void 0 : _a.submenu) !== null && _b !== void 0 ? _b : new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu({
                    commands: this.commands
                });
        }
        return this._newMenu;
    }
    /**
     * Dispose of the resources held by the file menu.
     */
    dispose() {
        var _a;
        (_a = this._newMenu) === null || _a === void 0 ? void 0 : _a.dispose();
        super.dispose();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/help.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/help.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HelpMenu": () => (/* binding */ HelpMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Help menu for the application.
 */
class HelpMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the help menu.
     */
    constructor(options) {
        super(options);
        this.getKernel = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand();
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/index.js":
/*!*****************************************!*\
  !*** ../packages/mainmenu/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "EditMenu": () => (/* reexport safe */ _edit__WEBPACK_IMPORTED_MODULE_1__.EditMenu),
/* harmony export */   "FileMenu": () => (/* reexport safe */ _file__WEBPACK_IMPORTED_MODULE_2__.FileMenu),
/* harmony export */   "HelpMenu": () => (/* reexport safe */ _help__WEBPACK_IMPORTED_MODULE_3__.HelpMenu),
/* harmony export */   "IMainMenu": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_9__.IMainMenu),
/* harmony export */   "KernelMenu": () => (/* reexport safe */ _kernel__WEBPACK_IMPORTED_MODULE_4__.KernelMenu),
/* harmony export */   "MainMenu": () => (/* reexport safe */ _mainmenu__WEBPACK_IMPORTED_MODULE_0__.MainMenu),
/* harmony export */   "RunMenu": () => (/* reexport safe */ _run__WEBPACK_IMPORTED_MODULE_5__.RunMenu),
/* harmony export */   "SettingsMenu": () => (/* reexport safe */ _settings__WEBPACK_IMPORTED_MODULE_6__.SettingsMenu),
/* harmony export */   "TabsMenu": () => (/* reexport safe */ _tabs__WEBPACK_IMPORTED_MODULE_8__.TabsMenu),
/* harmony export */   "ViewMenu": () => (/* reexport safe */ _view__WEBPACK_IMPORTED_MODULE_7__.ViewMenu)
/* harmony export */ });
/* harmony import */ var _mainmenu__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./mainmenu */ "../packages/mainmenu/lib/mainmenu.js");
/* harmony import */ var _edit__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./edit */ "../packages/mainmenu/lib/edit.js");
/* harmony import */ var _file__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./file */ "../packages/mainmenu/lib/file.js");
/* harmony import */ var _help__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./help */ "../packages/mainmenu/lib/help.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./kernel */ "../packages/mainmenu/lib/kernel.js");
/* harmony import */ var _run__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./run */ "../packages/mainmenu/lib/run.js");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./settings */ "../packages/mainmenu/lib/settings.js");
/* harmony import */ var _view__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./view */ "../packages/mainmenu/lib/view.js");
/* harmony import */ var _tabs__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tabs */ "../packages/mainmenu/lib/tabs.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./tokens */ "../packages/mainmenu/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mainmenu
 */












/***/ }),

/***/ "../packages/mainmenu/lib/kernel.js":
/*!******************************************!*\
  !*** ../packages/mainmenu/lib/kernel.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelMenu": () => (/* binding */ KernelMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Kernel menu for the application.
 */
class KernelMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the kernel menu.
     */
    constructor(options) {
        super(options);
        this.kernelUsers = {
            changeKernel: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            clearWidget: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            interruptKernel: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            reconnectToKernel: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            restartKernel: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            shutdownKernel: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand()
        };
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/mainmenu.js":
/*!********************************************!*\
  !*** ../packages/mainmenu/lib/mainmenu.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MainMenu": () => (/* binding */ MainMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _edit__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./edit */ "../packages/mainmenu/lib/edit.js");
/* harmony import */ var _file__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./file */ "../packages/mainmenu/lib/file.js");
/* harmony import */ var _help__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./help */ "../packages/mainmenu/lib/help.js");
/* harmony import */ var _kernel__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./kernel */ "../packages/mainmenu/lib/kernel.js");
/* harmony import */ var _run__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./run */ "../packages/mainmenu/lib/run.js");
/* harmony import */ var _settings__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./settings */ "../packages/mainmenu/lib/settings.js");
/* harmony import */ var _tabs__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tabs */ "../packages/mainmenu/lib/tabs.js");
/* harmony import */ var _view__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./view */ "../packages/mainmenu/lib/view.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.











/**
 * The main menu class.  It is intended to be used as a singleton.
 */
class MainMenu extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.MenuBar {
    /**
     * Construct the main menu bar.
     */
    constructor(commands) {
        let options = { forceItemsPosition: { forceX: false, forceY: true } };
        super(options);
        this._items = [];
        this._commands = commands;
    }
    /**
     * The application "Edit" menu.
     */
    get editMenu() {
        if (!this._editMenu) {
            this._editMenu = new _edit__WEBPACK_IMPORTED_MODULE_3__.EditMenu({
                commands: this._commands,
                rank: 2,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._editMenu;
    }
    /**
     * The application "File" menu.
     */
    get fileMenu() {
        if (!this._fileMenu) {
            this._fileMenu = new _file__WEBPACK_IMPORTED_MODULE_4__.FileMenu({
                commands: this._commands,
                rank: 1,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._fileMenu;
    }
    /**
     * The application "Help" menu.
     */
    get helpMenu() {
        if (!this._helpMenu) {
            this._helpMenu = new _help__WEBPACK_IMPORTED_MODULE_5__.HelpMenu({
                commands: this._commands,
                rank: 1000,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._helpMenu;
    }
    /**
     * The application "Kernel" menu.
     */
    get kernelMenu() {
        if (!this._kernelMenu) {
            this._kernelMenu = new _kernel__WEBPACK_IMPORTED_MODULE_6__.KernelMenu({
                commands: this._commands,
                rank: 5,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._kernelMenu;
    }
    /**
     * The application "Run" menu.
     */
    get runMenu() {
        if (!this._runMenu) {
            this._runMenu = new _run__WEBPACK_IMPORTED_MODULE_7__.RunMenu({
                commands: this._commands,
                rank: 4,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._runMenu;
    }
    /**
     * The application "Settings" menu.
     */
    get settingsMenu() {
        if (!this._settingsMenu) {
            this._settingsMenu = new _settings__WEBPACK_IMPORTED_MODULE_8__.SettingsMenu({
                commands: this._commands,
                rank: 999,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._settingsMenu;
    }
    /**
     * The application "View" menu.
     */
    get viewMenu() {
        if (!this._viewMenu) {
            this._viewMenu = new _view__WEBPACK_IMPORTED_MODULE_9__.ViewMenu({
                commands: this._commands,
                rank: 3,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._viewMenu;
    }
    /**
     * The application "Tabs" menu.
     */
    get tabsMenu() {
        if (!this._tabsMenu) {
            this._tabsMenu = new _tabs__WEBPACK_IMPORTED_MODULE_10__.TabsMenu({
                commands: this._commands,
                rank: 500,
                renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
            });
        }
        return this._tabsMenu;
    }
    /**
     * Add a new menu to the main menu bar.
     */
    addMenu(menu, update = true, options = {}) {
        if (_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.firstIndexOf(this.menus, menu) > -1) {
            return;
        }
        // override default renderer with svg-supporting renderer
        _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.overrideDefaultRenderer(menu);
        const rank = 'rank' in options
            ? options.rank
            : 'rank' in menu
                ? menu.rank
                : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.IRankedMenu.DEFAULT_RANK;
        const rankItem = { menu, rank };
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.upperBound(this._items, rankItem, Private.itemCmp);
        // Upon disposal, remove the menu and its rank reference.
        menu.disposed.connect(this._onMenuDisposed, this);
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.insert(this._items, index, rankItem);
        /**
         * Create a new menu.
         */
        this.insertMenu(index, menu);
        // Link the menu to the API - backward compatibility when switching to menu description in settings
        switch (menu.id) {
            case 'jp-mainmenu-file':
                if (!this._fileMenu && menu instanceof _file__WEBPACK_IMPORTED_MODULE_4__.FileMenu) {
                    this._fileMenu = menu;
                }
                break;
            case 'jp-mainmenu-edit':
                if (!this._editMenu && menu instanceof _edit__WEBPACK_IMPORTED_MODULE_3__.EditMenu) {
                    this._editMenu = menu;
                }
                break;
            case 'jp-mainmenu-view':
                if (!this._viewMenu && menu instanceof _view__WEBPACK_IMPORTED_MODULE_9__.ViewMenu) {
                    this._viewMenu = menu;
                }
                break;
            case 'jp-mainmenu-run':
                if (!this._runMenu && menu instanceof _run__WEBPACK_IMPORTED_MODULE_7__.RunMenu) {
                    this._runMenu = menu;
                }
                break;
            case 'jp-mainmenu-kernel':
                if (!this._kernelMenu && menu instanceof _kernel__WEBPACK_IMPORTED_MODULE_6__.KernelMenu) {
                    this._kernelMenu = menu;
                }
                break;
            case 'jp-mainmenu-tabs':
                if (!this._tabsMenu && menu instanceof _tabs__WEBPACK_IMPORTED_MODULE_10__.TabsMenu) {
                    this._tabsMenu = menu;
                }
                break;
            case 'jp-mainmenu-settings':
                if (!this._settingsMenu && menu instanceof _settings__WEBPACK_IMPORTED_MODULE_8__.SettingsMenu) {
                    this._settingsMenu = menu;
                }
                break;
            case 'jp-mainmenu-help':
                if (!this._helpMenu && menu instanceof _help__WEBPACK_IMPORTED_MODULE_5__.HelpMenu) {
                    this._helpMenu = menu;
                }
                break;
        }
    }
    /**
     * Dispose of the resources held by the menu bar.
     */
    dispose() {
        var _a, _b, _c, _d, _e, _f, _g, _h;
        (_a = this._editMenu) === null || _a === void 0 ? void 0 : _a.dispose();
        (_b = this._fileMenu) === null || _b === void 0 ? void 0 : _b.dispose();
        (_c = this._helpMenu) === null || _c === void 0 ? void 0 : _c.dispose();
        (_d = this._kernelMenu) === null || _d === void 0 ? void 0 : _d.dispose();
        (_e = this._runMenu) === null || _e === void 0 ? void 0 : _e.dispose();
        (_f = this._settingsMenu) === null || _f === void 0 ? void 0 : _f.dispose();
        (_g = this._viewMenu) === null || _g === void 0 ? void 0 : _g.dispose();
        (_h = this._tabsMenu) === null || _h === void 0 ? void 0 : _h.dispose();
        super.dispose();
    }
    /**
     * Generate the menu.
     *
     * @param commands The command registry
     * @param options The main menu options.
     * @param trans - The application language translator.
     */
    static generateMenu(commands, options, trans) {
        let menu;
        const { id, label, rank } = options;
        switch (id) {
            case 'jp-mainmenu-file':
                menu = new _file__WEBPACK_IMPORTED_MODULE_4__.FileMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-edit':
                menu = new _edit__WEBPACK_IMPORTED_MODULE_3__.EditMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-view':
                menu = new _view__WEBPACK_IMPORTED_MODULE_9__.ViewMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-run':
                menu = new _run__WEBPACK_IMPORTED_MODULE_7__.RunMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-kernel':
                menu = new _kernel__WEBPACK_IMPORTED_MODULE_6__.KernelMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-tabs':
                menu = new _tabs__WEBPACK_IMPORTED_MODULE_10__.TabsMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-settings':
                menu = new _settings__WEBPACK_IMPORTED_MODULE_8__.SettingsMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            case 'jp-mainmenu-help':
                menu = new _help__WEBPACK_IMPORTED_MODULE_5__.HelpMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
                break;
            default:
                menu = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu({
                    commands,
                    rank,
                    renderer: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.MenuSvg.defaultRenderer
                });
        }
        if (label) {
            menu.title.label = trans._p('menu', label);
        }
        return menu;
    }
    /**
     * Handle the disposal of a menu.
     */
    _onMenuDisposed(menu) {
        this.removeMenu(menu);
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.findFirstIndex(this._items, item => item.menu === menu);
        if (index !== -1) {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.removeAt(this._items, index);
        }
    }
}
/**
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * A comparator function for menu rank items.
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/mainmenu/lib/run.js":
/*!***************************************!*\
  !*** ../packages/mainmenu/lib/run.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunMenu": () => (/* binding */ RunMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible Run menu for the application.
 */
class RunMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the run menu.
     */
    constructor(options) {
        super(options);
        this.codeRunners = {
            restart: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            run: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            runAll: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand()
        };
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/settings.js":
/*!********************************************!*\
  !*** ../packages/mainmenu/lib/settings.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SettingsMenu": () => (/* binding */ SettingsMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Settings menu for the application.
 */
class SettingsMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the settings menu.
     */
    constructor(options) {
        super(options);
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/tabs.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/tabs.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TabsMenu": () => (/* binding */ TabsMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * An extensible Tabs menu for the application.
 */
class TabsMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the tabs menu.
     */
    constructor(options) {
        super(options);
    }
}


/***/ }),

/***/ "../packages/mainmenu/lib/tokens.js":
/*!******************************************!*\
  !*** ../packages/mainmenu/lib/tokens.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMainMenu": () => (/* binding */ IMainMenu)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The main menu token.
 */
const IMainMenu = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/mainmenu:IMainMenu', `A service for the main menu bar for the application.
  Use this if you want to add your own menu items or provide implementations for standardized menu items for specific activities.`);


/***/ }),

/***/ "../packages/mainmenu/lib/view.js":
/*!****************************************!*\
  !*** ../packages/mainmenu/lib/view.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ViewMenu": () => (/* binding */ ViewMenu)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * An extensible View menu for the application.
 */
class ViewMenu extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.RankedMenu {
    /**
     * Construct the view menu.
     */
    constructor(options) {
        super(options);
        this.editorViewers = {
            toggleLineNumbers: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            toggleMatchBrackets: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand(),
            toggleWordWrap: new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.SemanticCommand()
        };
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWFpbm1lbnVfbGliX2luZGV4X2pzLjQyMTlhNDdlMmNhYzlkZjliNThhLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVTO0FBQ2I7QUFzQnZEOztHQUVHO0FBQ0ksTUFBTSxRQUFTLFNBQVEsaUVBQVU7SUFDdEM7O09BRUc7SUFDSCxZQUFZLE9BQTZCO1FBQ3ZDLEtBQUssQ0FBQyxPQUFPLENBQUMsQ0FBQztRQUVmLElBQUksQ0FBQyxPQUFPLEdBQUc7WUFDYixJQUFJLEVBQUUsSUFBSSxpRUFBZSxFQUFFO1lBQzNCLElBQUksRUFBRSxJQUFJLGlFQUFlLEVBQUU7U0FDNUIsQ0FBQztRQUVGLElBQUksQ0FBQyxRQUFRLEdBQUc7WUFDZCxRQUFRLEVBQUUsSUFBSSxpRUFBZSxFQUFFO1lBQy9CLFlBQVksRUFBRSxJQUFJLGlFQUFlLEVBQUU7U0FDcEMsQ0FBQztRQUVGLElBQUksQ0FBQyxVQUFVLEdBQUcsSUFBSSxpRUFBZSxFQUFFLENBQUM7SUFDMUMsQ0FBQztDQWdCRjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDL0RELDBDQUEwQztBQUMxQywyREFBMkQ7QUFFUztBQUMzQjtBQUNjO0FBMkJ2RDs7R0FFRztBQUNJLE1BQU0sUUFBUyxTQUFRLGlFQUFVO0lBQ3RDLFlBQVksT0FBNkI7UUFDdkMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBQ2YsSUFBSSxDQUFDLFNBQVMsR0FBRyxLQUFLLENBQUM7UUFFdkIsSUFBSSxDQUFDLGdCQUFnQixHQUFHLElBQUksaUVBQWUsRUFBRSxDQUFDO1FBQzlDLElBQUksQ0FBQyxlQUFlLEdBQUcsSUFBSSxpRUFBZSxFQUFFLENBQUM7SUFDL0MsQ0FBQztJQUVEOztPQUVHO0lBQ0gsSUFBSSxPQUFPOztRQUNULElBQUksQ0FBQyxJQUFJLENBQUMsUUFBUSxFQUFFO1lBQ2xCLElBQUksQ0FBQyxRQUFRO2dCQUNYLE1BQUMsNkRBQUksQ0FBQyxJQUFJ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Ozs7Ozs7Ozs7Ozs7OztBQ3BCRCwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBR2pCO0FBVzFDOztHQUVHO0FBQ0ksTUFBTSxTQUFTLEdBQUcsSUFBSSxvREFBSyxDQUNoQyxnQ0FBZ0MsRUFDaEM7a0lBQ2dJLENBQ2pJLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN0QkYsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVTO0FBQ2I7QUFZdkQ7O0dBRUc7QUFDSSxNQUFNLFFBQVMsU0FBUSxpRUFBVTtJQUN0Qzs7T0FFRztJQUNILFlBQVksT0FBNkI7UUFDdkMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBQ2YsSUFBSSxDQUFDLGFBQWEsR0FBRztZQUNuQixpQkFBaUIsRUFBRSxJQUFJLGlFQUFlLEVBQUU7WUFDeEMsbUJBQW1CLEVBQUUsSUFBSSxpRUFBZSxFQUFFO1lBQzFDLGNBQWMsRUFBRSxJQUFJLGlFQUFlLEVBQUU7U0FDdEMsQ0FBQztJQUNKLENBQUM7Q0FNRiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYWlubWVudS9zcmMvZWRpdC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL2ZpbGUudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy9oZWxwLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYWlubWVudS9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy9rZXJuZWwudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21haW5tZW51L3NyYy9tYWlubWVudS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL3J1bi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL3NldHRpbmdzLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYWlubWVudS9zcmMvdGFicy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL3Rva2Vucy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWFpbm1lbnUvc3JjL3ZpZXcudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJUmFua2VkTWVudSwgUmFua2VkTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgU2VtYW50aWNDb21tYW5kIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYW4gRWRpdCBtZW51LlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElFZGl0TWVudSBleHRlbmRzIElSYW5rZWRNZW51IHtcbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElVbmRvZXJzIGZvciB0aGUgRWRpdCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgdW5kb2VyczogSUVkaXRNZW51LklVbmRvZXI7XG5cbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElDbGVhcmVycyBmb3IgdGhlIEVkaXQgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGNsZWFyZXJzOiBJRWRpdE1lbnUuSUNsZWFyZXI7XG5cbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElHb1RvTGluZXJzIGZvciB0aGUgRWRpdCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgZ29Ub0xpbmVyczogU2VtYW50aWNDb21tYW5kO1xufVxuXG4vKipcbiAqIEFuIGV4dGVuc2libGUgRWRpdCBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBFZGl0TWVudSBleHRlbmRzIFJhbmtlZE1lbnUgaW1wbGVtZW50cyBJRWRpdE1lbnUge1xuICAvKipcbiAgICogQ29uc3RydWN0IHRoZSBlZGl0IG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuXG4gICAgdGhpcy51bmRvZXJzID0ge1xuICAgICAgcmVkbzogbmV3IFNlbWFudGljQ29tbWFuZCgpLFxuICAgICAgdW5kbzogbmV3IFNlbWFudGljQ29tbWFuZCgpXG4gICAgfTtcblxuICAgIHRoaXMuY2xlYXJlcnMgPSB7XG4gICAgICBjbGVhckFsbDogbmV3IFNlbWFudGljQ29tbWFuZCgpLFxuICAgICAgY2xlYXJDdXJyZW50OiBuZXcgU2VtYW50aWNDb21tYW5kKClcbiAgICB9O1xuXG4gICAgdGhpcy5nb1RvTGluZXJzID0gbmV3IFNlbWFudGljQ29tbWFuZCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElVbmRvZXJzIGZvciB0aGUgRWRpdCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgdW5kb2VyczogSUVkaXRNZW51LklVbmRvZXI7XG5cbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElDbGVhcmVycyBmb3IgdGhlIEVkaXQgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGNsZWFyZXJzOiBJRWRpdE1lbnUuSUNsZWFyZXI7XG5cbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElHb1RvTGluZXJzIGZvciB0aGUgRWRpdCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgZ29Ub0xpbmVyczogU2VtYW50aWNDb21tYW5kO1xufVxuXG4vKipcbiAqIE5hbWVzcGFjZSBmb3IgSUVkaXRNZW51XG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSUVkaXRNZW51IHtcbiAgLyoqXG4gICAqIEludGVyZmFjZSBmb3IgYW4gYWN0aXZpdHkgdGhhdCB1c2VzIFVuZG8vUmVkby5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVVuZG9lciB7XG4gICAgLyoqXG4gICAgICogQSBzZW1hbnRpYyBjb21tYW5kIHRvIGV4ZWN1dGUgYW4gdW5kbyBjb21tYW5kIGZvciB0aGUgYWN0aXZpdHkuXG4gICAgICovXG4gICAgdW5kbzogU2VtYW50aWNDb21tYW5kO1xuXG4gICAgLyoqXG4gICAgICogQSBzZW1hbnRpYyBjb21tYW5kIHRvIGV4ZWN1dGUgYSByZWRvIGNvbW1hbmQgZm9yIHRoZSBhY3Rpdml0eS5cbiAgICAgKi9cbiAgICByZWRvOiBTZW1hbnRpY0NvbW1hbmQ7XG4gIH1cblxuICAvKipcbiAgICogSW50ZXJmYWNlIGZvciBhbiBhY3Rpdml0eSB0aGF0IHdhbnRzIHRvIHJlZ2lzdGVyIGEgJ0NsZWFyLi4uJyBtZW51IGl0ZW1cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUNsZWFyZXIge1xuICAgIC8qKlxuICAgICAqIEEgc2VtYW50aWMgY29tbWFuZCB0byBjbGVhciB0aGUgY3VycmVudGx5IHBvcnRpb24gb2YgYWN0aXZpdHkuXG4gICAgICovXG4gICAgY2xlYXJDdXJyZW50OiBTZW1hbnRpY0NvbW1hbmQ7XG5cbiAgICAvKipcbiAgICAgKiBBIHNlbWFudGljIGNvbW1hbmQgdG8gY2xlYXIgYWxsIG9mIGFuIGFjdGl2aXR5LlxuICAgICAqL1xuICAgIGNsZWFyQWxsOiBTZW1hbnRpY0NvbW1hbmQ7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVJhbmtlZE1lbnUsIFJhbmtlZE1lbnUgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IGZpbmQgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBTZW1hbnRpY0NvbW1hbmQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIEZpbGUgbWVudS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRmlsZU1lbnUgZXh0ZW5kcyBJUmFua2VkTWVudSB7XG4gIC8qKlxuICAgKiBPcHRpb24gdG8gYWRkIGEgYFF1aXRgIGVudHJ5IGluIHRoZSBGaWxlIG1lbnVcbiAgICovXG4gIHF1aXRFbnRyeTogYm9vbGVhbjtcblxuICAvKipcbiAgICogQSBzdWJtZW51IGZvciBjcmVhdGluZyBuZXcgZmlsZXMvbGF1bmNoaW5nIG5ldyBhY3Rpdml0aWVzLlxuICAgKi9cbiAgcmVhZG9ubHkgbmV3TWVudTogSVJhbmtlZE1lbnU7XG5cbiAgLyoqXG4gICAqIFRoZSBjbG9zZSBhbmQgY2xlYW51cCBzZW1hbnRpYyBjb21tYW5kLlxuICAgKi9cbiAgcmVhZG9ubHkgY2xvc2VBbmRDbGVhbmVyczogU2VtYW50aWNDb21tYW5kO1xuXG4gIC8qKlxuICAgKiBUaGUgY29uc29sZSBjcmVhdG9yIHNlbWFudGljIGNvbW1hbmQuXG4gICAqL1xuICByZWFkb25seSBjb25zb2xlQ3JlYXRvcnM6IFNlbWFudGljQ29tbWFuZDtcbn1cblxuLyoqXG4gKiBBbiBleHRlbnNpYmxlIEZpbGVNZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBGaWxlTWVudSBleHRlbmRzIFJhbmtlZE1lbnUgaW1wbGVtZW50cyBJRmlsZU1lbnUge1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIHRoaXMucXVpdEVudHJ5ID0gZmFsc2U7XG5cbiAgICB0aGlzLmNsb3NlQW5kQ2xlYW5lcnMgPSBuZXcgU2VtYW50aWNDb21tYW5kKCk7XG4gICAgdGhpcy5jb25zb2xlQ3JlYXRvcnMgPSBuZXcgU2VtYW50aWNDb21tYW5kKCk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIE5ldyBzdWJtZW51LlxuICAgKi9cbiAgZ2V0IG5ld01lbnUoKTogUmFua2VkTWVudSB7XG4gICAgaWYgKCF0aGlzLl9uZXdNZW51KSB7XG4gICAgICB0aGlzLl9uZXdNZW51ID1cbiAgICAgICAgKGZpbmQodGhpcy5pdGVtcywgbWVudSA9PiBtZW51LnN1Ym1lbnU/LmlkID09PSAnanAtbWFpbm1lbnUtZmlsZS1uZXcnKVxuICAgICAgICAgID8uc3VibWVudSBhcyBSYW5rZWRNZW51KSA/P1xuICAgICAgICBuZXcgUmFua2VkTWVudSh7XG4gICAgICAgICAgY29tbWFuZHM6IHRoaXMuY29tbWFuZHNcbiAgICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9uZXdNZW51O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjbG9zZSBhbmQgY2xlYW51cCBzZW1hbnRpYyBjb21tYW5kLlxuICAgKi9cbiAgcmVhZG9ubHkgY2xvc2VBbmRDbGVhbmVyczogU2VtYW50aWNDb21tYW5kO1xuXG4gIC8qKlxuICAgKiBUaGUgY29uc29sZSBjcmVhdG9yIHNlbWFudGljIGNvbW1hbmQuXG4gICAqL1xuICByZWFkb25seSBjb25zb2xlQ3JlYXRvcnM6IFNlbWFudGljQ29tbWFuZDtcblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIGZpbGUgbWVudS5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgdGhpcy5fbmV3TWVudT8uZGlzcG9zZSgpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBPcHRpb24gdG8gYWRkIGEgYFF1aXRgIGVudHJ5IGluIEZpbGUgbWVudVxuICAgKi9cbiAgcHVibGljIHF1aXRFbnRyeTogYm9vbGVhbjtcblxuICBwcml2YXRlIF9uZXdNZW51OiBSYW5rZWRNZW51O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJUmFua2VkTWVudSwgUmFua2VkTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgU2VtYW50aWNDb21tYW5kIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYSBIZWxwIG1lbnUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUhlbHBNZW51IGV4dGVuZHMgSVJhbmtlZE1lbnUge1xuICAvKipcbiAgICogQSBzZW1hbnRpYyBjb21tYW5kIHRvIGdldCB0aGUga2VybmVsIGZvciB0aGUgaGVscCBtZW51LlxuICAgKiBUaGlzIGlzIHVzZWQgdG8gcG9wdWxhdGUgYWRkaXRpb25hbCBoZWxwXG4gICAqIGxpbmtzIHByb3ZpZGVkIGJ5IHRoZSBrZXJuZWwgb2YgYSB3aWRnZXQuXG4gICAqXG4gICAqICMjIyMgTm90ZVxuICAgKiBUaGUgY29tbWFuZCBtdXN0IHJldHVybiBhIEtlcm5lbC5JS2VybmVsQ29ubmVjdGlvbiBvYmplY3RcbiAgICovXG4gIHJlYWRvbmx5IGdldEtlcm5lbDogU2VtYW50aWNDb21tYW5kO1xufVxuXG4vKipcbiAqIEFuIGV4dGVuc2libGUgSGVscCBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBIZWxwTWVudSBleHRlbmRzIFJhbmtlZE1lbnUgaW1wbGVtZW50cyBJSGVscE1lbnUge1xuICAvKipcbiAgICogQ29uc3RydWN0IHRoZSBoZWxwIG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIHRoaXMuZ2V0S2VybmVsID0gbmV3IFNlbWFudGljQ29tbWFuZCgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2VtYW50aWMgY29tbWFuZCB0byBnZXQgdGhlIGtlcm5lbCBmb3IgdGhlIGhlbHAgbWVudS5cbiAgICogVGhpcyBpcyB1c2VkIHRvIHBvcHVsYXRlIGFkZGl0aW9uYWwgaGVscFxuICAgKiBsaW5rcyBwcm92aWRlZCBieSB0aGUga2VybmVsIG9mIGEgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVcbiAgICogVGhlIGNvbW1hbmQgbXVzdCByZXR1cm4gYSBLZXJuZWwuSUtlcm5lbENvbm5lY3Rpb24gb2JqZWN0XG4gICAqL1xuICByZWFkb25seSBnZXRLZXJuZWw6IFNlbWFudGljQ29tbWFuZDtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG1haW5tZW51XG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9tYWlubWVudSc7XG5leHBvcnQgKiBmcm9tICcuL2VkaXQnO1xuZXhwb3J0ICogZnJvbSAnLi9maWxlJztcbmV4cG9ydCAqIGZyb20gJy4vaGVscCc7XG5leHBvcnQgKiBmcm9tICcuL2tlcm5lbCc7XG5leHBvcnQgKiBmcm9tICcuL3J1bic7XG5leHBvcnQgKiBmcm9tICcuL3NldHRpbmdzJztcbmV4cG9ydCAqIGZyb20gJy4vdmlldyc7XG5leHBvcnQgKiBmcm9tICcuL3RhYnMnO1xuZXhwb3J0ICogZnJvbSAnLi90b2tlbnMnO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJUmFua2VkTWVudSwgUmFua2VkTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgU2VtYW50aWNDb21tYW5kIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYSBLZXJuZWwgbWVudS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJS2VybmVsTWVudSBleHRlbmRzIElSYW5rZWRNZW51IHtcbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElLZXJuZWxVc2VycyBmb3IgdGhlIEtlcm5lbCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkga2VybmVsVXNlcnM6IElLZXJuZWxNZW51LklLZXJuZWxVc2VyO1xufVxuXG4vKipcbiAqIEFuIGV4dGVuc2libGUgS2VybmVsIG1lbnUgZm9yIHRoZSBhcHBsaWNhdGlvbi5cbiAqL1xuZXhwb3J0IGNsYXNzIEtlcm5lbE1lbnUgZXh0ZW5kcyBSYW5rZWRNZW51IGltcGxlbWVudHMgSUtlcm5lbE1lbnUge1xuICAvKipcbiAgICogQ29uc3RydWN0IHRoZSBrZXJuZWwgbWVudS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IElSYW5rZWRNZW51LklPcHRpb25zKSB7XG4gICAgc3VwZXIob3B0aW9ucyk7XG4gICAgdGhpcy5rZXJuZWxVc2VycyA9IHtcbiAgICAgIGNoYW5nZUtlcm5lbDogbmV3IFNlbWFudGljQ29tbWFuZCgpLFxuICAgICAgY2xlYXJXaWRnZXQ6IG5ldyBTZW1hbnRpY0NvbW1hbmQoKSxcbiAgICAgIGludGVycnVwdEtlcm5lbDogbmV3IFNlbWFudGljQ29tbWFuZCgpLFxuICAgICAgcmVjb25uZWN0VG9LZXJuZWw6IG5ldyBTZW1hbnRpY0NvbW1hbmQoKSxcbiAgICAgIHJlc3RhcnRLZXJuZWw6IG5ldyBTZW1hbnRpY0NvbW1hbmQoKSxcbiAgICAgIHNodXRkb3duS2VybmVsOiBuZXcgU2VtYW50aWNDb21tYW5kKClcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElLZXJuZWxVc2VycyBmb3IgdGhlIEtlcm5lbCBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkga2VybmVsVXNlcnM6IElLZXJuZWxNZW51LklLZXJuZWxVc2VyO1xufVxuXG4vKipcbiAqIE5hbWVzcGFjZSBmb3IgSUtlcm5lbE1lbnVcbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJS2VybmVsTWVudSB7XG4gIC8qKlxuICAgKiBJbnRlcmZhY2UgZm9yIGEgS2VybmVsIHVzZXIgdG8gcmVnaXN0ZXIgaXRzZWxmXG4gICAqIHdpdGggdGhlIElLZXJuZWxNZW51J3Mgc2VtYW50aWMgZXh0ZW5zaW9uIHBvaW50cy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUtlcm5lbFVzZXIge1xuICAgIC8qKlxuICAgICAqIEEgc2VtYW50aWMgY29tbWFuZCB0byBpbnRlcnJ1cHQgdGhlIGtlcm5lbC5cbiAgICAgKi9cbiAgICBpbnRlcnJ1cHRLZXJuZWw6IFNlbWFudGljQ29tbWFuZDtcblxuICAgIC8qKlxuICAgICAqIEEgc2VtYW50aWMgY29tbWFuZCB0byByZWNvbm5lY3QgdG8gdGhlIGtlcm5lbFxuICAgICAqL1xuICAgIHJlY29ubmVjdFRvS2VybmVsOiBTZW1hbnRpY0NvbW1hbmQ7XG5cbiAgICAvKipcbiAgICAgKiBBIHNlbWFudGljIGNvbW1hbmQgdG8gcmVzdGFydCB0aGUga2VybmVsLCB3aGljaFxuICAgICAqIHJldHVybnMgYSBwcm9taXNlIG9mIHdoZXRoZXIgdGhlIGtlcm5lbCB3YXMgcmVzdGFydGVkLlxuICAgICAqL1xuICAgIHJlc3RhcnRLZXJuZWw6IFNlbWFudGljQ29tbWFuZDtcblxuICAgIC8qKlxuICAgICAqIEEgc2VtYW50aWMgY29tbWFuZCB0byBjbGVhciB0aGUgd2lkZ2V0LlxuICAgICAqL1xuICAgIGNsZWFyV2lkZ2V0OiBTZW1hbnRpY0NvbW1hbmQ7XG5cbiAgICAvKipcbiAgICAgKiBBIHNlbWFudGljIGNvbW1hbmQgdG8gY2hhbmdlIHRoZSBrZXJuZWwuXG4gICAgICovXG4gICAgY2hhbmdlS2VybmVsOiBTZW1hbnRpY0NvbW1hbmQ7XG5cbiAgICAvKipcbiAgICAgKiBBIHNlbWFudGljIGNvbW1hbmQgdG8gc2h1dCBkb3duIHRoZSBrZXJuZWwuXG4gICAgICovXG4gICAgc2h1dGRvd25LZXJuZWw6IFNlbWFudGljQ29tbWFuZDtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUcmFuc2xhdGlvbkJ1bmRsZSB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IElSYW5rZWRNZW51LCBNZW51U3ZnLCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBBcnJheUV4dCB9IGZyb20gJ0BsdW1pbm8vYWxnb3JpdGhtJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgTWVudSwgTWVudUJhciB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgeyBFZGl0TWVudSB9IGZyb20gJy4vZWRpdCc7XG5pbXBvcnQgeyBGaWxlTWVudSB9IGZyb20gJy4vZmlsZSc7XG5pbXBvcnQgeyBIZWxwTWVudSB9IGZyb20gJy4vaGVscCc7XG5pbXBvcnQgeyBLZXJuZWxNZW51IH0gZnJvbSAnLi9rZXJuZWwnO1xuaW1wb3J0IHsgUnVuTWVudSB9IGZyb20gJy4vcnVuJztcbmltcG9ydCB7IFNldHRpbmdzTWVudSB9IGZyb20gJy4vc2V0dGluZ3MnO1xuaW1wb3J0IHsgVGFic01lbnUgfSBmcm9tICcuL3RhYnMnO1xuaW1wb3J0IHsgSU1haW5NZW51IH0gZnJvbSAnLi90b2tlbnMnO1xuaW1wb3J0IHsgVmlld01lbnUgfSBmcm9tICcuL3ZpZXcnO1xuXG4vKipcbiAqIFRoZSBtYWluIG1lbnUgY2xhc3MuICBJdCBpcyBpbnRlbmRlZCB0byBiZSB1c2VkIGFzIGEgc2luZ2xldG9uLlxuICovXG5leHBvcnQgY2xhc3MgTWFpbk1lbnUgZXh0ZW5kcyBNZW51QmFyIGltcGxlbWVudHMgSU1haW5NZW51IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCB0aGUgbWFpbiBtZW51IGJhci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnkpIHtcbiAgICBsZXQgb3B0aW9ucyA9IHsgZm9yY2VJdGVtc1Bvc2l0aW9uOiB7IGZvcmNlWDogZmFsc2UsIGZvcmNlWTogdHJ1ZSB9IH07XG4gICAgc3VwZXIob3B0aW9ucyk7XG4gICAgdGhpcy5fY29tbWFuZHMgPSBjb21tYW5kcztcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJFZGl0XCIgbWVudS5cbiAgICovXG4gIGdldCBlZGl0TWVudSgpOiBFZGl0TWVudSB7XG4gICAgaWYgKCF0aGlzLl9lZGl0TWVudSkge1xuICAgICAgdGhpcy5fZWRpdE1lbnUgPSBuZXcgRWRpdE1lbnUoe1xuICAgICAgICBjb21tYW5kczogdGhpcy5fY29tbWFuZHMsXG4gICAgICAgIHJhbms6IDIsXG4gICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9lZGl0TWVudTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJGaWxlXCIgbWVudS5cbiAgICovXG4gIGdldCBmaWxlTWVudSgpOiBGaWxlTWVudSB7XG4gICAgaWYgKCF0aGlzLl9maWxlTWVudSkge1xuICAgICAgdGhpcy5fZmlsZU1lbnUgPSBuZXcgRmlsZU1lbnUoe1xuICAgICAgICBjb21tYW5kczogdGhpcy5fY29tbWFuZHMsXG4gICAgICAgIHJhbms6IDEsXG4gICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9maWxlTWVudTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJIZWxwXCIgbWVudS5cbiAgICovXG4gIGdldCBoZWxwTWVudSgpOiBIZWxwTWVudSB7XG4gICAgaWYgKCF0aGlzLl9oZWxwTWVudSkge1xuICAgICAgdGhpcy5faGVscE1lbnUgPSBuZXcgSGVscE1lbnUoe1xuICAgICAgICBjb21tYW5kczogdGhpcy5fY29tbWFuZHMsXG4gICAgICAgIHJhbms6IDEwMDAsXG4gICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9oZWxwTWVudTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJLZXJuZWxcIiBtZW51LlxuICAgKi9cbiAgZ2V0IGtlcm5lbE1lbnUoKTogS2VybmVsTWVudSB7XG4gICAgaWYgKCF0aGlzLl9rZXJuZWxNZW51KSB7XG4gICAgICB0aGlzLl9rZXJuZWxNZW51ID0gbmV3IEtlcm5lbE1lbnUoe1xuICAgICAgICBjb21tYW5kczogdGhpcy5fY29tbWFuZHMsXG4gICAgICAgIHJhbms6IDUsXG4gICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9rZXJuZWxNZW51O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIlJ1blwiIG1lbnUuXG4gICAqL1xuICBnZXQgcnVuTWVudSgpOiBSdW5NZW51IHtcbiAgICBpZiAoIXRoaXMuX3J1bk1lbnUpIHtcbiAgICAgIHRoaXMuX3J1bk1lbnUgPSBuZXcgUnVuTWVudSh7XG4gICAgICAgIGNvbW1hbmRzOiB0aGlzLl9jb21tYW5kcyxcbiAgICAgICAgcmFuazogNCxcbiAgICAgICAgcmVuZGVyZXI6IE1lbnVTdmcuZGVmYXVsdFJlbmRlcmVyXG4gICAgICB9KTtcbiAgICB9XG4gICAgcmV0dXJuIHRoaXMuX3J1bk1lbnU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiU2V0dGluZ3NcIiBtZW51LlxuICAgKi9cbiAgZ2V0IHNldHRpbmdzTWVudSgpOiBTZXR0aW5nc01lbnUge1xuICAgIGlmICghdGhpcy5fc2V0dGluZ3NNZW51KSB7XG4gICAgICB0aGlzLl9zZXR0aW5nc01lbnUgPSBuZXcgU2V0dGluZ3NNZW51KHtcbiAgICAgICAgY29tbWFuZHM6IHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICByYW5rOiA5OTksXG4gICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl9zZXR0aW5nc01lbnU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiVmlld1wiIG1lbnUuXG4gICAqL1xuICBnZXQgdmlld01lbnUoKTogVmlld01lbnUge1xuICAgIGlmICghdGhpcy5fdmlld01lbnUpIHtcbiAgICAgIHRoaXMuX3ZpZXdNZW51ID0gbmV3IFZpZXdNZW51KHtcbiAgICAgICAgY29tbWFuZHM6IHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICByYW5rOiAzLFxuICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgIH0pO1xuICAgIH1cbiAgICByZXR1cm4gdGhpcy5fdmlld01lbnU7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiVGFic1wiIG1lbnUuXG4gICAqL1xuICBnZXQgdGFic01lbnUoKTogVGFic01lbnUge1xuICAgIGlmICghdGhpcy5fdGFic01lbnUpIHtcbiAgICAgIHRoaXMuX3RhYnNNZW51ID0gbmV3IFRhYnNNZW51KHtcbiAgICAgICAgY29tbWFuZHM6IHRoaXMuX2NvbW1hbmRzLFxuICAgICAgICByYW5rOiA1MDAsXG4gICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB0aGlzLl90YWJzTWVudTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSBuZXcgbWVudSB0byB0aGUgbWFpbiBtZW51IGJhci5cbiAgICovXG4gIGFkZE1lbnUoXG4gICAgbWVudTogTWVudSxcbiAgICB1cGRhdGU6IGJvb2xlYW4gPSB0cnVlLFxuICAgIG9wdGlvbnM6IElNYWluTWVudS5JQWRkT3B0aW9ucyA9IHt9XG4gICk6IHZvaWQge1xuICAgIGlmIChBcnJheUV4dC5maXJzdEluZGV4T2YodGhpcy5tZW51cywgbWVudSkgPiAtMSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIC8vIG92ZXJyaWRlIGRlZmF1bHQgcmVuZGVyZXIgd2l0aCBzdmctc3VwcG9ydGluZyByZW5kZXJlclxuICAgIE1lbnVTdmcub3ZlcnJpZGVEZWZhdWx0UmVuZGVyZXIobWVudSk7XG5cbiAgICBjb25zdCByYW5rID1cbiAgICAgICdyYW5rJyBpbiBvcHRpb25zXG4gICAgICAgID8gb3B0aW9ucy5yYW5rXG4gICAgICAgIDogJ3JhbmsnIGluIG1lbnVcbiAgICAgICAgPyAobWVudSBhcyBhbnkpLnJhbmtcbiAgICAgICAgOiBJUmFua2VkTWVudS5ERUZBVUxUX1JBTks7XG4gICAgY29uc3QgcmFua0l0ZW0gPSB7IG1lbnUsIHJhbmsgfTtcbiAgICBjb25zdCBpbmRleCA9IEFycmF5RXh0LnVwcGVyQm91bmQodGhpcy5faXRlbXMsIHJhbmtJdGVtLCBQcml2YXRlLml0ZW1DbXApO1xuXG4gICAgLy8gVXBvbiBkaXNwb3NhbCwgcmVtb3ZlIHRoZSBtZW51IGFuZCBpdHMgcmFuayByZWZlcmVuY2UuXG4gICAgbWVudS5kaXNwb3NlZC5jb25uZWN0KHRoaXMuX29uTWVudURpc3Bvc2VkLCB0aGlzKTtcblxuICAgIEFycmF5RXh0Lmluc2VydCh0aGlzLl9pdGVtcywgaW5kZXgsIHJhbmtJdGVtKTtcbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBuZXcgbWVudS5cbiAgICAgKi9cbiAgICB0aGlzLmluc2VydE1lbnUoaW5kZXgsIG1lbnUpO1xuXG4gICAgLy8gTGluayB0aGUgbWVudSB0byB0aGUgQVBJIC0gYmFja3dhcmQgY29tcGF0aWJpbGl0eSB3aGVuIHN3aXRjaGluZyB0byBtZW51IGRlc2NyaXB0aW9uIGluIHNldHRpbmdzXG4gICAgc3dpdGNoIChtZW51LmlkKSB7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1maWxlJzpcbiAgICAgICAgaWYgKCF0aGlzLl9maWxlTWVudSAmJiBtZW51IGluc3RhbmNlb2YgRmlsZU1lbnUpIHtcbiAgICAgICAgICB0aGlzLl9maWxlTWVudSA9IG1lbnU7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1lZGl0JzpcbiAgICAgICAgaWYgKCF0aGlzLl9lZGl0TWVudSAmJiBtZW51IGluc3RhbmNlb2YgRWRpdE1lbnUpIHtcbiAgICAgICAgICB0aGlzLl9lZGl0TWVudSA9IG1lbnU7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS12aWV3JzpcbiAgICAgICAgaWYgKCF0aGlzLl92aWV3TWVudSAmJiBtZW51IGluc3RhbmNlb2YgVmlld01lbnUpIHtcbiAgICAgICAgICB0aGlzLl92aWV3TWVudSA9IG1lbnU7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1ydW4nOlxuICAgICAgICBpZiAoIXRoaXMuX3J1bk1lbnUgJiYgbWVudSBpbnN0YW5jZW9mIFJ1bk1lbnUpIHtcbiAgICAgICAgICB0aGlzLl9ydW5NZW51ID0gbWVudTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LWtlcm5lbCc6XG4gICAgICAgIGlmICghdGhpcy5fa2VybmVsTWVudSAmJiBtZW51IGluc3RhbmNlb2YgS2VybmVsTWVudSkge1xuICAgICAgICAgIHRoaXMuX2tlcm5lbE1lbnUgPSBtZW51O1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtdGFicyc6XG4gICAgICAgIGlmICghdGhpcy5fdGFic01lbnUgJiYgbWVudSBpbnN0YW5jZW9mIFRhYnNNZW51KSB7XG4gICAgICAgICAgdGhpcy5fdGFic01lbnUgPSBtZW51O1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtc2V0dGluZ3MnOlxuICAgICAgICBpZiAoIXRoaXMuX3NldHRpbmdzTWVudSAmJiBtZW51IGluc3RhbmNlb2YgU2V0dGluZ3NNZW51KSB7XG4gICAgICAgICAgdGhpcy5fc2V0dGluZ3NNZW51ID0gbWVudTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LWhlbHAnOlxuICAgICAgICBpZiAoIXRoaXMuX2hlbHBNZW51ICYmIG1lbnUgaW5zdGFuY2VvZiBIZWxwTWVudSkge1xuICAgICAgICAgIHRoaXMuX2hlbHBNZW51ID0gbWVudTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIG1lbnUgYmFyLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICB0aGlzLl9lZGl0TWVudT8uZGlzcG9zZSgpO1xuICAgIHRoaXMuX2ZpbGVNZW51Py5kaXNwb3NlKCk7XG4gICAgdGhpcy5faGVscE1lbnU/LmRpc3Bvc2UoKTtcbiAgICB0aGlzLl9rZXJuZWxNZW51Py5kaXNwb3NlKCk7XG4gICAgdGhpcy5fcnVuTWVudT8uZGlzcG9zZSgpO1xuICAgIHRoaXMuX3NldHRpbmdzTWVudT8uZGlzcG9zZSgpO1xuICAgIHRoaXMuX3ZpZXdNZW51Py5kaXNwb3NlKCk7XG4gICAgdGhpcy5fdGFic01lbnU/LmRpc3Bvc2UoKTtcbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICAvKipcbiAgICogR2VuZXJhdGUgdGhlIG1lbnUuXG4gICAqXG4gICAqIEBwYXJhbSBjb21tYW5kcyBUaGUgY29tbWFuZCByZWdpc3RyeVxuICAgKiBAcGFyYW0gb3B0aW9ucyBUaGUgbWFpbiBtZW51IG9wdGlvbnMuXG4gICAqIEBwYXJhbSB0cmFucyAtIFRoZSBhcHBsaWNhdGlvbiBsYW5ndWFnZSB0cmFuc2xhdG9yLlxuICAgKi9cbiAgc3RhdGljIGdlbmVyYXRlTWVudShcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIG9wdGlvbnM6IElNYWluTWVudS5JTWVudU9wdGlvbnMsXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICk6IFJhbmtlZE1lbnUge1xuICAgIGxldCBtZW51OiBSYW5rZWRNZW51O1xuICAgIGNvbnN0IHsgaWQsIGxhYmVsLCByYW5rIH0gPSBvcHRpb25zO1xuICAgIHN3aXRjaCAoaWQpIHtcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LWZpbGUnOlxuICAgICAgICBtZW51ID0gbmV3IEZpbGVNZW51KHtcbiAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICByYW5rLFxuICAgICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS1lZGl0JzpcbiAgICAgICAgbWVudSA9IG5ldyBFZGl0TWVudSh7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgcmFuayxcbiAgICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgICAgfSk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtdmlldyc6XG4gICAgICAgIG1lbnUgPSBuZXcgVmlld01lbnUoe1xuICAgICAgICAgIGNvbW1hbmRzLFxuICAgICAgICAgIHJhbmssXG4gICAgICAgICAgcmVuZGVyZXI6IE1lbnVTdmcuZGVmYXVsdFJlbmRlcmVyXG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ2pwLW1haW5tZW51LXJ1bic6XG4gICAgICAgIG1lbnUgPSBuZXcgUnVuTWVudSh7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgcmFuayxcbiAgICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgICAgfSk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUta2VybmVsJzpcbiAgICAgICAgbWVudSA9IG5ldyBLZXJuZWxNZW51KHtcbiAgICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgICByYW5rLFxuICAgICAgICAgIHJlbmRlcmVyOiBNZW51U3ZnLmRlZmF1bHRSZW5kZXJlclxuICAgICAgICB9KTtcbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdqcC1tYWlubWVudS10YWJzJzpcbiAgICAgICAgbWVudSA9IG5ldyBUYWJzTWVudSh7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgcmFuayxcbiAgICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgICAgfSk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtc2V0dGluZ3MnOlxuICAgICAgICBtZW51ID0gbmV3IFNldHRpbmdzTWVudSh7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgcmFuayxcbiAgICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgICAgfSk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnanAtbWFpbm1lbnUtaGVscCc6XG4gICAgICAgIG1lbnUgPSBuZXcgSGVscE1lbnUoe1xuICAgICAgICAgIGNvbW1hbmRzLFxuICAgICAgICAgIHJhbmssXG4gICAgICAgICAgcmVuZGVyZXI6IE1lbnVTdmcuZGVmYXVsdFJlbmRlcmVyXG4gICAgICAgIH0pO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIG1lbnUgPSBuZXcgUmFua2VkTWVudSh7XG4gICAgICAgICAgY29tbWFuZHMsXG4gICAgICAgICAgcmFuayxcbiAgICAgICAgICByZW5kZXJlcjogTWVudVN2Zy5kZWZhdWx0UmVuZGVyZXJcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgaWYgKGxhYmVsKSB7XG4gICAgICBtZW51LnRpdGxlLmxhYmVsID0gdHJhbnMuX3AoJ21lbnUnLCBsYWJlbCk7XG4gICAgfVxuXG4gICAgcmV0dXJuIG1lbnU7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHRoZSBkaXNwb3NhbCBvZiBhIG1lbnUuXG4gICAqL1xuICBwcml2YXRlIF9vbk1lbnVEaXNwb3NlZChtZW51OiBNZW51KTogdm9pZCB7XG4gICAgdGhpcy5yZW1vdmVNZW51KG1lbnUpO1xuICAgIGNvbnN0IGluZGV4ID0gQXJyYXlFeHQuZmluZEZpcnN0SW5kZXgoXG4gICAgICB0aGlzLl9pdGVtcyxcbiAgICAgIGl0ZW0gPT4gaXRlbS5tZW51ID09PSBtZW51XG4gICAgKTtcbiAgICBpZiAoaW5kZXggIT09IC0xKSB7XG4gICAgICBBcnJheUV4dC5yZW1vdmVBdCh0aGlzLl9pdGVtcywgaW5kZXgpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2NvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnk7XG4gIHByaXZhdGUgX2l0ZW1zOiBQcml2YXRlLklSYW5rSXRlbVtdID0gW107XG4gIHByaXZhdGUgX2VkaXRNZW51OiBFZGl0TWVudTtcbiAgcHJpdmF0ZSBfZmlsZU1lbnU6IEZpbGVNZW51O1xuICBwcml2YXRlIF9oZWxwTWVudTogSGVscE1lbnU7XG4gIHByaXZhdGUgX2tlcm5lbE1lbnU6IEtlcm5lbE1lbnU7XG4gIHByaXZhdGUgX3J1bk1lbnU6IFJ1bk1lbnU7XG4gIHByaXZhdGUgX3NldHRpbmdzTWVudTogU2V0dGluZ3NNZW51O1xuICBwcml2YXRlIF92aWV3TWVudTogVmlld01lbnU7XG4gIHByaXZhdGUgX3RhYnNNZW51OiBUYWJzTWVudTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBbiBvYmplY3Qgd2hpY2ggaG9sZHMgYSBtZW51IGFuZCBpdHMgc29ydCByYW5rLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUmFua0l0ZW0ge1xuICAgIC8qKlxuICAgICAqIFRoZSBtZW51IGZvciB0aGUgaXRlbS5cbiAgICAgKi9cbiAgICBtZW51OiBNZW51O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHNvcnQgcmFuayBvZiB0aGUgbWVudS5cbiAgICAgKi9cbiAgICByYW5rOiBudW1iZXI7XG4gIH1cblxuICAvKipcbiAgICogQSBjb21wYXJhdG9yIGZ1bmN0aW9uIGZvciBtZW51IHJhbmsgaXRlbXMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gaXRlbUNtcChmaXJzdDogSVJhbmtJdGVtLCBzZWNvbmQ6IElSYW5rSXRlbSk6IG51bWJlciB7XG4gICAgcmV0dXJuIGZpcnN0LnJhbmsgLSBzZWNvbmQucmFuaztcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJUmFua2VkTWVudSwgUmFua2VkTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgU2VtYW50aWNDb21tYW5kIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYSBSdW4gbWVudS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJUnVuTWVudSBleHRlbmRzIElSYW5rZWRNZW51IHtcbiAgLyoqXG4gICAqIFNlbWFudGljIGNvbW1hbmRzIElDb2RlUnVubmVyIGZvciB0aGUgUnVuIG1lbnUuXG4gICAqL1xuICByZWFkb25seSBjb2RlUnVubmVyczogSVJ1bk1lbnUuSUNvZGVSdW5uZXI7XG59XG5cbi8qKlxuICogQW4gZXh0ZW5zaWJsZSBSdW4gbWVudSBmb3IgdGhlIGFwcGxpY2F0aW9uLlxuICovXG5leHBvcnQgY2xhc3MgUnVuTWVudSBleHRlbmRzIFJhbmtlZE1lbnUgaW1wbGVtZW50cyBJUnVuTWVudSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgdGhlIHJ1biBtZW51LlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogSVJhbmtlZE1lbnUuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihvcHRpb25zKTtcbiAgICB0aGlzLmNvZGVSdW5uZXJzID0ge1xuICAgICAgcmVzdGFydDogbmV3IFNlbWFudGljQ29tbWFuZCgpLFxuICAgICAgcnVuOiBuZXcgU2VtYW50aWNDb21tYW5kKCksXG4gICAgICBydW5BbGw6IG5ldyBTZW1hbnRpY0NvbW1hbmQoKVxuICAgIH07XG4gIH1cblxuICAvKipcbiAgICogU2VtYW50aWMgY29tbWFuZHMgSUNvZGVSdW5uZXIgZm9yIHRoZSBSdW4gbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGNvZGVSdW5uZXJzOiBJUnVuTWVudS5JQ29kZVJ1bm5lcjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgUnVuTWVudSBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElSdW5NZW51IHtcbiAgLyoqXG4gICAqIEFuIG9iamVjdCB0aGF0IHJ1bnMgY29kZSwgd2hpY2ggbWF5IGJlXG4gICAqIHJlZ2lzdGVyZWQgd2l0aCB0aGUgUnVuIG1lbnUuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElDb2RlUnVubmVyIHtcbiAgICAvKipcbiAgICAgKiBBIHNlbWFudGljIGNvbW1hbmQgdG8gcnVuIGEgc3VicGFydCBvZiBhIGRvY3VtZW50LlxuICAgICAqL1xuICAgIHJ1bjogU2VtYW50aWNDb21tYW5kO1xuICAgIC8qKlxuICAgICAqIEEgc2VtYW50aWMgY29tbWFuZCB0byBydW4gYSB3aG9sZSBkb2N1bWVudFxuICAgICAqL1xuICAgIHJ1bkFsbDogU2VtYW50aWNDb21tYW5kO1xuICAgIC8qKlxuICAgICAqIEEgc2VtYW50aWMgY29tbWFuZCB0byByZXN0YXJ0IGEga2VybmVsXG4gICAgICovXG4gICAgcmVzdGFydDogU2VtYW50aWNDb21tYW5kO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIFNldHRpbmdzIG1lbnUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVNldHRpbmdzTWVudSBleHRlbmRzIElSYW5rZWRNZW51IHt9XG5cbi8qKlxuICogQW4gZXh0ZW5zaWJsZSBTZXR0aW5ncyBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBTZXR0aW5nc01lbnUgZXh0ZW5kcyBSYW5rZWRNZW51IGltcGxlbWVudHMgSVNldHRpbmdzTWVudSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgdGhlIHNldHRpbmdzIG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElSYW5rZWRNZW51LCBSYW5rZWRNZW51IH0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIFRhYnMgbWVudS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJVGFic01lbnUgZXh0ZW5kcyBJUmFua2VkTWVudSB7fVxuXG4vKipcbiAqIEFuIGV4dGVuc2libGUgVGFicyBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBUYWJzTWVudSBleHRlbmRzIFJhbmtlZE1lbnUgaW1wbGVtZW50cyBJVGFic01lbnUge1xuICAvKipcbiAgICogQ29uc3RydWN0IHRoZSB0YWJzIG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IE1lbnVGYWN0b3J5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBNZW51IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCB7IElFZGl0TWVudSB9IGZyb20gJy4vZWRpdCc7XG5pbXBvcnQgeyBJRmlsZU1lbnUgfSBmcm9tICcuL2ZpbGUnO1xuaW1wb3J0IHsgSUhlbHBNZW51IH0gZnJvbSAnLi9oZWxwJztcbmltcG9ydCB7IElLZXJuZWxNZW51IH0gZnJvbSAnLi9rZXJuZWwnO1xuaW1wb3J0IHsgSVJ1bk1lbnUgfSBmcm9tICcuL3J1bic7XG5pbXBvcnQgeyBJU2V0dGluZ3NNZW51IH0gZnJvbSAnLi9zZXR0aW5ncyc7XG5pbXBvcnQgeyBJVGFic01lbnUgfSBmcm9tICcuL3RhYnMnO1xuaW1wb3J0IHsgSVZpZXdNZW51IH0gZnJvbSAnLi92aWV3JztcblxuLyoqXG4gKiBUaGUgbWFpbiBtZW51IHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSU1haW5NZW51ID0gbmV3IFRva2VuPElNYWluTWVudT4oXG4gICdAanVweXRlcmxhYi9tYWlubWVudTpJTWFpbk1lbnUnLFxuICBgQSBzZXJ2aWNlIGZvciB0aGUgbWFpbiBtZW51IGJhciBmb3IgdGhlIGFwcGxpY2F0aW9uLlxuICBVc2UgdGhpcyBpZiB5b3Ugd2FudCB0byBhZGQgeW91ciBvd24gbWVudSBpdGVtcyBvciBwcm92aWRlIGltcGxlbWVudGF0aW9ucyBmb3Igc3RhbmRhcmRpemVkIG1lbnUgaXRlbXMgZm9yIHNwZWNpZmljIGFjdGl2aXRpZXMuYFxuKTtcblxuLyoqXG4gKiBUaGUgbWFpbiBtZW51IGludGVyZmFjZS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJTWFpbk1lbnUge1xuICAvKipcbiAgICogQWRkIGEgbmV3IG1lbnUgdG8gdGhlIG1haW4gbWVudSBiYXIuXG4gICAqXG4gICAqIEBwYXJhbSBtZW51IFRoZSBtZW51IHRvIGFkZFxuICAgKiBAcGFyYW0gdXBkYXRlIFdoZXRoZXIgdG8gdXBkYXRlIHRoZSBtZW51IGJhciBvciBub3RcbiAgICogQHBhcmFtIG9wdGlvbnMgT3B0aW9ucyBmb3IgYWRkaW5nIHRoZSBtZW51XG4gICAqL1xuICBhZGRNZW51KG1lbnU6IE1lbnUsIHVwZGF0ZT86IGJvb2xlYW4sIG9wdGlvbnM/OiBJTWFpbk1lbnUuSUFkZE9wdGlvbnMpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJGaWxlXCIgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGZpbGVNZW51OiBJRmlsZU1lbnU7XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIkVkaXRcIiBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgZWRpdE1lbnU6IElFZGl0TWVudTtcblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiVmlld1wiIG1lbnUuXG4gICAqL1xuICByZWFkb25seSB2aWV3TWVudTogSVZpZXdNZW51O1xuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJIZWxwXCIgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGhlbHBNZW51OiBJSGVscE1lbnU7XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIktlcm5lbFwiIG1lbnUuXG4gICAqL1xuICByZWFkb25seSBrZXJuZWxNZW51OiBJS2VybmVsTWVudTtcblxuICAvKipcbiAgICogVGhlIGFwcGxpY2F0aW9uIFwiUnVuXCIgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IHJ1bk1lbnU6IElSdW5NZW51O1xuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gXCJTZXR0aW5nc1wiIG1lbnUuXG4gICAqL1xuICByZWFkb25seSBzZXR0aW5nc01lbnU6IElTZXR0aW5nc01lbnU7XG5cbiAgLyoqXG4gICAqIFRoZSBhcHBsaWNhdGlvbiBcIlRhYnNcIiBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgdGFic01lbnU6IElUYWJzTWVudTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBJTWFpbk1lbnUgYXR0YWNoZWQgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJTWFpbk1lbnUge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBhZGQgYSBtZW51IHRvIHRoZSBtYWluIG1lbnUuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElBZGRPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgcmFuayBvcmRlciBvZiB0aGUgbWVudSBhbW9uZyBpdHMgc2libGluZ3MuXG4gICAgICovXG4gICAgcmFuaz86IG51bWJlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhbiBJTWFpbk1lbnUuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNZW51T3B0aW9ucyBleHRlbmRzIE1lbnVGYWN0b3J5LklNZW51T3B0aW9ucyB7fVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJUmFua2VkTWVudSwgUmFua2VkTWVudSB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgU2VtYW50aWNDb21tYW5kIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYSBWaWV3IG1lbnUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVZpZXdNZW51IGV4dGVuZHMgSVJhbmtlZE1lbnUge1xuICAvKipcbiAgICogU2VtYW50aWMgY29tbWFuZHMgSUVkaXRvclZpZXdlciBmb3IgdGhlIFZpZXcgbWVudS5cbiAgICovXG4gIHJlYWRvbmx5IGVkaXRvclZpZXdlcnM6IElWaWV3TWVudS5JRWRpdG9yVmlld2VyO1xufVxuXG4vKipcbiAqIEFuIGV4dGVuc2libGUgVmlldyBtZW51IGZvciB0aGUgYXBwbGljYXRpb24uXG4gKi9cbmV4cG9ydCBjbGFzcyBWaWV3TWVudSBleHRlbmRzIFJhbmtlZE1lbnUgaW1wbGVtZW50cyBJVmlld01lbnUge1xuICAvKipcbiAgICogQ29uc3RydWN0IHRoZSB2aWV3IG1lbnUuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJUmFua2VkTWVudS5JT3B0aW9ucykge1xuICAgIHN1cGVyKG9wdGlvbnMpO1xuICAgIHRoaXMuZWRpdG9yVmlld2VycyA9IHtcbiAgICAgIHRvZ2dsZUxpbmVOdW1iZXJzOiBuZXcgU2VtYW50aWNDb21tYW5kKCksXG4gICAgICB0b2dnbGVNYXRjaEJyYWNrZXRzOiBuZXcgU2VtYW50aWNDb21tYW5kKCksXG4gICAgICB0b2dnbGVXb3JkV3JhcDogbmV3IFNlbWFudGljQ29tbWFuZCgpXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZW1hbnRpYyBjb21tYW5kcyBJRWRpdG9yVmlld2VyIGZvciB0aGUgVmlldyBtZW51LlxuICAgKi9cbiAgcmVhZG9ubHkgZWRpdG9yVmlld2VyczogSVZpZXdNZW51LklFZGl0b3JWaWV3ZXI7XG59XG5cbi8qKlxuICogTmFtZXNwYWNlIGZvciBJVmlld01lbnUuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVZpZXdNZW51IHtcbiAgLyoqXG4gICAqIEludGVyZmFjZSBmb3IgYSB0ZXh0IGVkaXRvciB2aWV3ZXIgdG8gcmVnaXN0ZXJcbiAgICogaXRzZWxmIHdpdGggdGhlIHRleHQgZWRpdG9yIHNlbWFudGljIGNvbW1hbmRzLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJRWRpdG9yVmlld2VyIHtcbiAgICAvKipcbiAgICAgKiBBIHNlbWFudGljIGNvbW1hbmQgdG8gc2hvdyBsaW5lIG51bWJlcnMgaW4gdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICB0b2dnbGVMaW5lTnVtYmVyczogU2VtYW50aWNDb21tYW5kO1xuXG4gICAgLyoqXG4gICAgICogQSBzZW1hbnRpYyBjb21tYW5kIHRvIHdvcmQtd3JhcCB0aGUgZWRpdG9yLlxuICAgICAqL1xuICAgIHRvZ2dsZVdvcmRXcmFwOiBTZW1hbnRpY0NvbW1hbmQ7XG5cbiAgICAvKipcbiAgICAgKiBBIHNlbWFudGljIGNvbW1hbmQgdG8gbWF0Y2ggYnJhY2tldHMgaW4gdGhlIGVkaXRvci5cbiAgICAgKi9cbiAgICB0b2dnbGVNYXRjaEJyYWNrZXRzOiBTZW1hbnRpY0NvbW1hbmQ7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==