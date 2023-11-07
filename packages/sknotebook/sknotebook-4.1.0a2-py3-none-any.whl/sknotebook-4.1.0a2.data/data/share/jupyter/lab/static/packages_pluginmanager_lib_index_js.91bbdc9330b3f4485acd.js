"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_pluginmanager_lib_index_js"],{

/***/ "../packages/pluginmanager/lib/dialogs.js":
/*!************************************************!*\
  !*** ../packages/pluginmanager/lib/dialogs.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PluginInUseMessage": () => (/* binding */ PluginInUseMessage),
/* harmony export */   "PluginRequiredMessage": () => (/* binding */ PluginRequiredMessage)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

function PluginRequiredMessage(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
        props.trans.__('The plugin "%1" cannot be disabled as it is required by other plugins:', props.plugin.id),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("ul", null, props.dependants.map(plugin => (react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { key: 'dependantsDialog-' + plugin.id }, plugin.id)))),
        props.trans.__('Please disable the dependant plugins first.')));
}
function PluginInUseMessage(props) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'jp-pluginmanager-PluginInUseMessage' },
        props.trans.__('While the plugin "%1" is not required by other enabled plugins, some plugins provide optional features depending on it. These plugins are:', props.plugin.id),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("ul", null, props.optionalDependants.map(plugin => (react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { key: 'optionalDependantsDialog-' + plugin.id }, plugin.id)))),
        props.trans.__('Do you want to disable it anyway?')));
}


/***/ }),

/***/ "../packages/pluginmanager/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/pluginmanager/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IPluginManager": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_2__.IPluginManager),
/* harmony export */   "PluginListModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.PluginListModel),
/* harmony export */   "Plugins": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.Plugins)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./model */ "../packages/pluginmanager/lib/model.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/pluginmanager/lib/widget.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./tokens */ "../packages/pluginmanager/lib/tokens.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module pluginmanager
 */





/***/ }),

/***/ "../packages/pluginmanager/lib/model.js":
/*!**********************************************!*\
  !*** ../packages/pluginmanager/lib/model.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PluginListModel": () => (/* binding */ PluginListModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _dialogs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./dialogs */ "../packages/pluginmanager/lib/dialogs.js");
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */








/**
 * The server API path for querying/modifying available plugins.
 */
const PLUGIN_API_PATH = 'lab/api/plugins';
/**
 * The model representing plugin list.
 */
class PluginListModel extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.VDomModel {
    constructor(options) {
        var _a, _b, _c;
        super();
        /**
         * Contains an error message if an error occurred when querying plugin status.
         */
        this.statusError = null;
        /**
         * Contains an error message if an error occurred when enabling/disabling plugin.
         */
        this.actionError = null;
        this._trackerDataChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_4__.Signal(this);
        this._isLoading = false;
        this._pendingActions = [];
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_5__.PromiseDelegate();
        this._pluginData = options.pluginData;
        this._serverSettings =
            options.serverSettings || _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        this._query = options.query || '';
        this._isDisclaimed = (_a = options.isDisclaimed) !== null && _a !== void 0 ? _a : false;
        this._extraLockedPlugins = (_b = options.extraLockedPlugins) !== null && _b !== void 0 ? _b : [];
        this.refresh()
            .then(() => this._ready.resolve())
            .catch(e => this._ready.reject(e));
        this._trans = ((_c = options.translator) !== null && _c !== void 0 ? _c : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_6__.nullTranslator).load('jupyterlab');
    }
    get available() {
        return [...this._available.values()];
    }
    /**
     * Whether plugin data is still getting loaded.
     */
    get isLoading() {
        return this._isLoading;
    }
    /**
     * Whether the warning is disclaimed or not.
     */
    get isDisclaimed() {
        return this._isDisclaimed;
    }
    set isDisclaimed(v) {
        if (v !== this._isDisclaimed) {
            this._isDisclaimed = v;
            this.stateChanged.emit();
            this._trackerDataChanged.emit(void 0);
        }
    }
    /**
     * The search query.
     *
     * Setting its value triggers a new search.
     */
    get query() {
        return this._query;
    }
    set query(value) {
        if (this._query !== value) {
            this._query = value;
            this.stateChanged.emit();
            this._trackerDataChanged.emit(void 0);
        }
    }
    /**
     * A promise that resolves when the trackable data changes
     */
    get trackerDataChanged() {
        return this._trackerDataChanged;
    }
    /**
     * A promise that resolves when the plugins were fetched from the server
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Enable a plugin.
     *
     * @param entry An entry indicating which plugin to enable.
     */
    async enable(entry) {
        if (!this.isDisclaimed) {
            throw new Error('User has not confirmed the disclaimer');
        }
        await this._performAction('enable', entry);
        entry.enabled = true;
    }
    /**
     * Disable a plugin.
     *
     * @param entry An entry indicating which plugin to disable.
     * @returns Whether the plugin was disabled
     */
    async disable(entry) {
        if (!this.isDisclaimed) {
            throw new Error('User has not confirmed the disclaimer');
        }
        const { dependants, optionalDependants } = this.getDependants(entry);
        if (dependants.length > 0) {
            // We require user to disable plugins one-by-one as each of them may have
            // further dependencies (or optional dependencies) and we want the user to
            // take a pause to think about those.
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: this._trans.__('This plugin is required by other plugins'),
                body: (0,_dialogs__WEBPACK_IMPORTED_MODULE_7__.PluginRequiredMessage)({
                    plugin: entry,
                    dependants,
                    trans: this._trans
                }),
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()]
            });
            return;
        }
        if (optionalDependants.length > 0) {
            const userConfirmation = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: this._trans.__('This plugin is used by other plugins'),
                body: (0,_dialogs__WEBPACK_IMPORTED_MODULE_7__.PluginInUseMessage)({
                    plugin: entry,
                    optionalDependants,
                    trans: this._trans
                }),
                buttons: [
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: this._trans.__('Disable anyway') }),
                    _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton()
                ]
            });
            if (!userConfirmation.button.accept) {
                return;
            }
        }
        await this._performAction('disable', entry);
        if (this.actionError) {
            return;
        }
        entry.enabled = false;
    }
    getDependants(entry) {
        const dependants = [];
        const optionalDependants = [];
        if (entry.provides) {
            const tokenName = entry.provides.name;
            for (const plugin of this._available.values()) {
                if (!plugin.enabled) {
                    continue;
                }
                if (plugin.requires
                    .filter(token => !!token)
                    .some(token => token.name === tokenName)) {
                    dependants.push(plugin);
                }
                if (plugin.optional
                    .filter(token => !!token)
                    .some(token => token.name === tokenName)) {
                    optionalDependants.push(plugin);
                }
            }
        }
        return {
            dependants,
            optionalDependants
        };
    }
    /**
     * Whether there are currently any actions pending.
     */
    hasPendingActions() {
        return this._pendingActions.length > 0;
    }
    /**
     * Send a request to the server to perform an action on a plugin.
     *
     * @param action A valid action to perform.
     * @param entry The plugin to perform the action on.
     */
    _performAction(action, entry) {
        this.actionError = null;
        const actionRequest = this._requestAPI({}, {
            method: 'POST',
            body: JSON.stringify({
                cmd: action,
                plugin_name: entry.id
            })
        });
        actionRequest.catch(reason => {
            this.actionError = reason.toString();
        });
        this._addPendingAction(actionRequest);
        return actionRequest;
    }
    /**
     * Add a pending action.
     *
     * @param pending A promise that resolves when the action is completed.
     */
    _addPendingAction(pending) {
        // Add to pending actions collection
        this._pendingActions.push(pending);
        // Ensure action is removed when resolved
        const remove = () => {
            const i = this._pendingActions.indexOf(pending);
            this._pendingActions.splice(i, 1);
            this.stateChanged.emit(undefined);
        };
        pending.then(remove, remove);
        // Signal changed state
        this.stateChanged.emit(undefined);
    }
    /**
     * Refresh plugin lock statuses
     */
    async refresh() {
        var _a;
        this.statusError = null;
        this._isLoading = true;
        this.stateChanged.emit();
        try {
            // Get the lock status from backend; if backend is not available,
            // we assume that all plugins are locked.
            const fallback = {
                allLocked: true,
                lockRules: []
            };
            const status = (_a = (await this._requestAPI())) !== null && _a !== void 0 ? _a : fallback;
            this._available = new Map(this._pluginData.availablePlugins.map(plugin => {
                let tokenLabel = plugin.provides
                    ? plugin.provides.name.split(':')[1]
                    : undefined;
                if (plugin.provides && !tokenLabel) {
                    tokenLabel = plugin.provides.name;
                }
                return [
                    plugin.id,
                    {
                        ...plugin,
                        locked: this._isLocked(plugin.id, status),
                        tokenLabel
                    }
                ];
            }));
        }
        catch (reason) {
            this.statusError = reason.toString();
        }
        finally {
            this._isLoading = false;
            this.stateChanged.emit();
        }
    }
    _isLocked(pluginId, status) {
        if (status.allLocked) {
            // All plugins are locked.
            return true;
        }
        if (this._extraLockedPlugins.includes(pluginId)) {
            // Plugin is locked on client side.
            return true;
        }
        const extension = pluginId.split(':')[0];
        if (status.lockRules.includes(extension)) {
            // Entire extension is locked.
            return true;
        }
        if (status.lockRules.includes(pluginId)) {
            // This plugin specifically is locked.
            return true;
        }
        return false;
    }
    /**
     * Call the plugin API
     *
     * @param endPoint API REST end point for the plugin
     * @param init Initial values for the request
     * @returns The response body interpreted as JSON
     */
    async _requestAPI(queryArgs = {}, init = {}) {
        // Make request to Jupyter API
        const settings = this._serverSettings;
        const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, PLUGIN_API_PATH);
        let response;
        try {
            response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeRequest(requestUrl + _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.objectToQueryString(queryArgs), init, settings);
        }
        catch (error) {
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.NetworkError(error);
        }
        let data = await response.text();
        if (data.length > 0) {
            try {
                data = JSON.parse(data);
            }
            catch (error) {
                console.log('Not a JSON response body.', response);
            }
        }
        if (!response.ok) {
            throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.ResponseError(response, data.message || data);
        }
        return data;
    }
}


/***/ }),

/***/ "../packages/pluginmanager/lib/tokens.js":
/*!***********************************************!*\
  !*** ../packages/pluginmanager/lib/tokens.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IPluginManager": () => (/* binding */ IPluginManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The plugin manager token.
 */
const IPluginManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/pluginmanager:IPluginManager', `A canary for plugin manager presence, with a method to open the plugin manager widget.`);


/***/ }),

/***/ "../packages/pluginmanager/lib/widget.js":
/*!***********************************************!*\
  !*** ../packages/pluginmanager/lib/widget.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Plugins": () => (/* binding */ Plugins)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */




/**
 * Panel with a table of available plugins allowing to enable/disable each.
 */
class Plugins extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel {
    constructor(options) {
        const { model, translator } = options;
        super();
        this.model = model;
        this.addClass('jp-pluginmanager');
        this.trans = translator.load('jupyterlab');
        this.addWidget(new Disclaimer(model, this.trans));
        const header = new Header(model, this.trans);
        this.addWidget(header);
        const availableList = new AvailableList(model, this.trans);
        this.addWidget(availableList);
    }
}
class AvailableList extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    constructor(model, trans) {
        super(model);
        this.trans = trans;
        this.addClass('jp-pluginmanager-AvailableList');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null, this.model.statusError !== null ? (react__WEBPACK_IMPORTED_MODULE_3__.createElement(ErrorMessage, null, this.trans.__('Error querying installed extensions%1', this.model.statusError ? `: ${this.model.statusError}` : '.'))) : this.model.isLoading ? (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "jp-pluginmanager-loader" }, this.trans.__('Updating plugin list…'))) : (react__WEBPACK_IMPORTED_MODULE_3__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.Table, { blankIndicator: () => {
                return react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", null, this.trans.__('No entries'));
            }, sortKey: 'plugin-id', rows: this.model.available
                .filter(pkg => {
                const pattern = new RegExp(this.model.query, 'i');
                return (pattern.test(pkg.id) ||
                    pattern.test(pkg.extension) ||
                    (pkg.tokenLabel && pattern.test(pkg.tokenLabel)));
            })
                .map(data => {
                return {
                    data: data,
                    key: data.id
                };
            }), columns: [
                {
                    id: 'plugin-id',
                    label: this.trans.__('Plugin'),
                    renderCell: (row) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null,
                        react__WEBPACK_IMPORTED_MODULE_3__.createElement("code", null, row.id),
                        react__WEBPACK_IMPORTED_MODULE_3__.createElement("br", null),
                        row.description)),
                    sort: (a, b) => a.id.localeCompare(b.id)
                },
                {
                    id: 'description',
                    label: this.trans.__('Description'),
                    renderCell: (row) => react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null, row.description),
                    sort: (a, b) => a.description && b.description
                        ? a.description.localeCompare(b.description)
                        : undefined,
                    isHidden: true
                },
                {
                    id: 'autostart',
                    label: this.trans.__('Autostart?'),
                    renderCell: (row) => {
                        switch (row.autoStart) {
                            case 'defer':
                                return this.trans.__('Defer');
                            case true:
                                return this.trans.__('Yes');
                            case false:
                            case undefined: // The default is `false`.
                                return this.trans.__('No');
                            default:
                                const leftover = row.autoStart;
                                throw new Error(`Unknown value: ${leftover}`);
                        }
                    },
                    sort: (a, b) => a.autoStart === b.autoStart ? 0 : a.autoStart ? -1 : 1
                },
                {
                    id: 'requires',
                    label: this.trans.__('Depends on'),
                    renderCell: (row) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null, row.requires.map(v => v.name).join('\n'))),
                    sort: (a, b) => (a.requires || []).length - (b.requires || []).length,
                    isHidden: true
                },
                {
                    id: 'extension',
                    label: this.trans.__('Extension'),
                    renderCell: (row) => react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null, row.extension),
                    sort: (a, b) => a.extension.localeCompare(b.extension)
                },
                {
                    id: 'provides',
                    label: this.trans.__('Provides'),
                    renderCell: (row) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null, row.provides ? (react__WEBPACK_IMPORTED_MODULE_3__.createElement("code", { title: row.provides.name }, row.tokenLabel)) : ('-'))),
                    sort: (a, b) => (a.tokenLabel || '').localeCompare(b.tokenLabel || '')
                },
                {
                    id: 'enabled',
                    label: this.trans.__('Enabled'),
                    renderCell: (row) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null,
                        react__WEBPACK_IMPORTED_MODULE_3__.createElement("input", { type: "checkbox", checked: row.enabled, disabled: row.locked || !this.model.isDisclaimed, title: row.locked || !this.model.isDisclaimed
                                ? row.locked
                                    ? this.trans.__('This plugin is locked.')
                                    : this.trans.__('To enable/disable, please acknowledge the disclaimer.')
                                : row.enabled
                                    ? this.trans.__('Disable %1 plugin', row.id)
                                    : this.trans.__('Enable %1 plugin', row.id), onChange: (event) => {
                                if (!this.model.isDisclaimed) {
                                    return;
                                }
                                if (event.target.checked) {
                                    void this.onAction('enable', row);
                                }
                                else {
                                    void this.onAction('disable', row);
                                }
                            } }),
                        row.locked ? (react__WEBPACK_IMPORTED_MODULE_3__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.lockIcon.react, { tag: "span", title: this.trans.__('This plugin was locked by system administrator or is a critical dependency and cannot be enabled/disabled.') })) : (''))),
                    sort: (a, b) => +a.enabled - +b.enabled
                }
            ] }))));
    }
    /**
     * Callback handler for when the user wants to perform an action on an extension.
     *
     * @param action The action to perform.
     * @param entry The entry to perform the action on.
     */
    onAction(action, entry) {
        switch (action) {
            case 'enable':
                return this.model.enable(entry);
            case 'disable':
                return this.model.disable(entry);
            default:
                throw new Error(`Invalid action: ${action}`);
        }
    }
}
class Disclaimer extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    constructor(model, trans) {
        super(model);
        this.trans = trans;
        this.addClass('jp-pluginmanager-Disclaimer');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", null, this.trans.__('Customise your experience/improve performance by disabling plugins you do not need. To disable or uninstall an entire extension use the Extension Manager instead. Changes will apply after reloading JupyterLab.')),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("label", null,
                react__WEBPACK_IMPORTED_MODULE_3__.createElement("input", { type: "checkbox", className: "jp-mod-styled jp-pluginmanager-Disclaimer-checkbox", defaultChecked: this.model.isDisclaimed, onChange: event => {
                        this.model.isDisclaimed = event.target.checked;
                    } }),
                this.trans.__('I understand that disabling core application plugins may render features and parts of the user interface unavailable and recovery using `jupyter labextension enable <plugin-name>` command may be required'))));
    }
}
class Header extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.VDomRenderer {
    constructor(model, trans) {
        super(model);
        this.trans = trans;
        this.addClass('jp-pluginmanager-Header');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_3__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.FilterBox, { placeholder: this.trans.__('Filter'), updateFilter: (fn, query) => {
                    this.model.query = query !== null && query !== void 0 ? query : '';
                }, initialQuery: this.model.query, useFuzzyFilter: false }),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: `jp-pluginmanager-pending ${this.model.hasPendingActions() ? 'jp-mod-hasPending' : ''}` }),
            this.model.actionError && (react__WEBPACK_IMPORTED_MODULE_3__.createElement(ErrorMessage, null,
                react__WEBPACK_IMPORTED_MODULE_3__.createElement("p", null, this.trans.__('Error when performing an action.')),
                react__WEBPACK_IMPORTED_MODULE_3__.createElement("p", null, this.trans.__('Reason given:')),
                react__WEBPACK_IMPORTED_MODULE_3__.createElement("pre", null, this.model.actionError)))));
    }
}
function ErrorMessage(props) {
    return react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "jp-pluginmanager-error" }, props.children);
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfcGx1Z2lubWFuYWdlcl9saWJfaW5kZXhfanMuOTFiYmRjOTMzMGIzZjQ0ODVhY2QuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7OztBQUkrQjtBQUV4QixTQUFTLHFCQUFxQixDQUFDLEtBSXJDO0lBQ0MsT0FBTyxDQUNMO1FBQ0csS0FBSyxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQ2Isd0VBQXdFLEVBQ3hFLEtBQUssQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUNoQjtRQUNELDZEQUNHLEtBQUssQ0FBQyxVQUFVLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsQ0FDOUIseURBQUksR0FBRyxFQUFFLG1CQUFtQixHQUFHLE1BQU0sQ0FBQyxFQUFFLElBQUcsTUFBTSxDQUFDLEVBQUUsQ0FBTSxDQUMzRCxDQUFDLENBQ0M7UUFDSixLQUFLLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyw2Q0FBNkMsQ0FBQyxDQUM3RCxDQUNKLENBQUM7QUFDSixDQUFDO0FBRU0sU0FBUyxrQkFBa0IsQ0FBQyxLQUlsQztJQUNDLE9BQU8sQ0FDTCwwREFBSyxTQUFTLEVBQUUscUNBQXFDO1FBQ2xELEtBQUssQ0FBQyxLQUFLLENBQUMsRUFBRSxDQUNiLDRJQUE0SSxFQUM1SSxLQUFLLENBQUMsTUFBTSxDQUFDLEVBQUUsQ0FDaEI7UUFDRCw2REFDRyxLQUFLLENBQUMsa0JBQWtCLENBQUMsR0FBRyxDQUFDLE1BQU0sQ0FBQyxFQUFFLENBQUMsQ0FDdEMseURBQUksR0FBRyxFQUFFLDJCQUEyQixHQUFHLE1BQU0sQ0FBQyxFQUFFLElBQUcsTUFBTSxDQUFDLEVBQUUsQ0FBTSxDQUNuRSxDQUFDLENBQ0M7UUFDSixLQUFLLENBQUMsS0FBSyxDQUFDLEVBQUUsQ0FBQyxtQ0FBbUMsQ0FBQyxDQUNoRCxDQUNQLENBQUM7QUFDSixDQUFDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQzlDRDs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFDcUI7QUFDQztBQUNBOzs7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QyxDQUFDLENBQUMsbUJBQW1CLENBQUMsQ0FBQyxDQUFDLEVBQ3pELEVBQUUsR0FDRjtZQUNELElBQUksQ0FBQyxLQUFLLENBQUMsV0FBVyxJQUFJLENBQ3pCLGlEQUFDLFlBQVk7Z0JBQ1gsNERBQUksSUFBSSxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsa0NBQWtDLENBQUMsQ0FBSztnQkFDMUQsNERBQUksSUFBSSxDQUFDLEtBQUssQ0FBQyxFQUFFLENBQUMsZUFBZSxDQUFDLENBQUs7Z0JBQ3ZDLDhEQUFNLElBQUksQ0FBQyxLQUFLLENBQUMsV0FBVyxDQUFPLENBQ3RCLENBQ2hCLENBQ0EsQ0FDSixDQUFDO0lBQ0osQ0FBQztDQUNGO0FBRUQsU0FBUyxZQUFZLENBQUMsS0FBOEI7SUFDbEQsT0FBTywwREFBSyxTQUFTLEVBQUMsd0JBQXdCLElBQUUsS0FBSyxDQUFDLFFBQVEsQ0FBTyxDQUFDO0FBQ3hFLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcGx1Z2lubWFuYWdlci9zcmMvZGlhbG9ncy50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3BsdWdpbm1hbmFnZXIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9wbHVnaW5tYW5hZ2VyL3NyYy9tb2RlbC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcGx1Z2lubWFuYWdlci9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9wbHVnaW5tYW5hZ2VyL3NyYy93aWRnZXQudHN4Il0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbmltcG9ydCB0eXBlIHsgSnVweXRlckxhYiB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0ICogYXMgUmVhY3QgZnJvbSAncmVhY3QnO1xuXG5leHBvcnQgZnVuY3Rpb24gUGx1Z2luUmVxdWlyZWRNZXNzYWdlKHByb3BzOiB7XG4gIHBsdWdpbjogSnVweXRlckxhYi5JUGx1Z2luSW5mbztcbiAgZGVwZW5kYW50czogSnVweXRlckxhYi5JUGx1Z2luSW5mb1tdO1xuICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG59KTogUmVhY3QuUmVhY3RFbGVtZW50PGFueT4ge1xuICByZXR1cm4gKFxuICAgIDw+XG4gICAgICB7cHJvcHMudHJhbnMuX18oXG4gICAgICAgICdUaGUgcGx1Z2luIFwiJTFcIiBjYW5ub3QgYmUgZGlzYWJsZWQgYXMgaXQgaXMgcmVxdWlyZWQgYnkgb3RoZXIgcGx1Z2luczonLFxuICAgICAgICBwcm9wcy5wbHVnaW4uaWRcbiAgICAgICl9XG4gICAgICA8dWw+XG4gICAgICAgIHtwcm9wcy5kZXBlbmRhbnRzLm1hcChwbHVnaW4gPT4gKFxuICAgICAgICAgIDxsaSBrZXk9eydkZXBlbmRhbnRzRGlhbG9nLScgKyBwbHVnaW4uaWR9PntwbHVnaW4uaWR9PC9saT5cbiAgICAgICAgKSl9XG4gICAgICA8L3VsPlxuICAgICAge3Byb3BzLnRyYW5zLl9fKCdQbGVhc2UgZGlzYWJsZSB0aGUgZGVwZW5kYW50IHBsdWdpbnMgZmlyc3QuJyl9XG4gICAgPC8+XG4gICk7XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBQbHVnaW5JblVzZU1lc3NhZ2UocHJvcHM6IHtcbiAgcGx1Z2luOiBKdXB5dGVyTGFiLklQbHVnaW5JbmZvO1xuICBvcHRpb25hbERlcGVuZGFudHM6IEp1cHl0ZXJMYWIuSVBsdWdpbkluZm9bXTtcbiAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xufSk6IFJlYWN0LlJlYWN0RWxlbWVudDxhbnk+IHtcbiAgcmV0dXJuIChcbiAgICA8ZGl2IGNsYXNzTmFtZT17J2pwLXBsdWdpbm1hbmFnZXItUGx1Z2luSW5Vc2VNZXNzYWdlJ30+XG4gICAgICB7cHJvcHMudHJhbnMuX18oXG4gICAgICAgICdXaGlsZSB0aGUgcGx1Z2luIFwiJTFcIiBpcyBub3QgcmVxdWlyZWQgYnkgb3RoZXIgZW5hYmxlZCBwbHVnaW5zLCBzb21lIHBsdWdpbnMgcHJvdmlkZSBvcHRpb25hbCBmZWF0dXJlcyBkZXBlbmRpbmcgb24gaXQuIFRoZXNlIHBsdWdpbnMgYXJlOicsXG4gICAgICAgIHByb3BzLnBsdWdpbi5pZFxuICAgICAgKX1cbiAgICAgIDx1bD5cbiAgICAgICAge3Byb3BzLm9wdGlvbmFsRGVwZW5kYW50cy5tYXAocGx1Z2luID0+IChcbiAgICAgICAgICA8bGkga2V5PXsnb3B0aW9uYWxEZXBlbmRhbnRzRGlhbG9nLScgKyBwbHVnaW4uaWR9PntwbHVnaW4uaWR9PC9saT5cbiAgICAgICAgKSl9XG4gICAgICA8L3VsPlxuICAgICAge3Byb3BzLnRyYW5zLl9fKCdEbyB5b3Ugd2FudCB0byBkaXNhYmxlIGl0IGFueXdheT8nKX1cbiAgICA8L2Rpdj5cbiAgKTtcbn1cbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgcGx1Z2lubWFuYWdlclxuICovXG5leHBvcnQgKiBmcm9tICcuL21vZGVsJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbiIsIi8qXG4gKiBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbiAqIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4gKi9cblxuaW1wb3J0IHR5cGUgeyBKdXB5dGVyTGFiIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgRGlhbG9nLCBzaG93RGlhbG9nIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgVVJMRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBWRG9tTW9kZWwgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuXG5pbXBvcnQgeyBQbHVnaW5JblVzZU1lc3NhZ2UsIFBsdWdpblJlcXVpcmVkTWVzc2FnZSB9IGZyb20gJy4vZGlhbG9ncyc7XG5cbi8qKlxuICogVGhlIHNlcnZlciBBUEkgcGF0aCBmb3IgcXVlcnlpbmcvbW9kaWZ5aW5nIGF2YWlsYWJsZSBwbHVnaW5zLlxuICovXG5jb25zdCBQTFVHSU5fQVBJX1BBVEggPSAnbGFiL2FwaS9wbHVnaW5zJztcblxuLyoqXG4gKiBFeHRlbnNpb24gYWN0aW9ucyB0aGF0IHRoZSBzZXJ2ZXIgQVBJIGFjY2VwdHMuXG4gKi9cbmV4cG9ydCB0eXBlIEFjdGlvbiA9ICdlbmFibGUnIHwgJ2Rpc2FibGUnO1xuXG4vKipcbiAqIEluZm9ybWF0aW9uIGFib3V0IGEgcGx1Z2luLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElFbnRyeSBleHRlbmRzIEp1cHl0ZXJMYWIuSVBsdWdpbkluZm8ge1xuICAvKipcbiAgICogV2hldGhlciB0aGUgcGx1Z2luIGlzIGxvY2tlZCAoY2Fubm90IGJlIGVuYWJsZWQvZGlzYWJsZWQpLlxuICAgKlxuICAgKiBBZG1pbmlzdHJhdG9ycyBjYW4gbG9jayBwbHVnaW5zIHByZXZlbnRpbmcgdXNlcnMgZnJvbSBpbnRyb2R1Y2luZyBtb2RpZmljYXRpb25zLlxuICAgKiBUaGUgY2hlY2sgaXMgcGVyZm9ybWVkIG9uIHRoZSBzZXJ2ZXIgc2lkZSwgdGhpcyBmaWVsZCBpcyBvbmx5IHRvIHNob3cgdXNlcnNcbiAgICogYW4gaW5kaWNhdG9yIG9mIHRoZSBsb2NrIHN0YXR1cy5cbiAgICovXG4gIHJlYWRvbmx5IGxvY2tlZDogYm9vbGVhbjtcblxuICAvKipcbiAgICogVG9rZW4gbmFtZSAoaWYgYW55KSBleGNsdWRpbmcgdGhlIHBsdWdpbiBwcmVmaXggKHVubGVzcyBub25lKVxuICAgKi9cbiAgdG9rZW5MYWJlbD86IHN0cmluZztcbn1cblxuaW50ZXJmYWNlIElQbHVnaW5NYW5hZ2VyU3RhdHVzIHtcbiAgLyoqXG4gICAqIFdoZXRoZXIgdG8gbG9jayAocHJldmVudCBlbmFibGluZy9kaXNhYmxpbmcpIGFsbCBwbHVnaW5zLlxuICAgKi9cbiAgcmVhZG9ubHkgYWxsTG9ja2VkOiBib29sZWFuO1xuICAvKipcbiAgICogQSBsaXN0IG9mIHBsdWdpbnMgb3IgZXh0ZW5zaW9ucyB0aGF0IGNhbm5vdCBiZSB0b2dnbGVkLlxuICAgKlxuICAgKiBJZiBleHRlbnNpb24gbmFtZSBpcyBwcm92aWRlZCwgYWxsIGl0cyBwbHVnaW5zIHdpbGwgYmUgZGlzYWJsZWQuXG4gICAqIFRoZSBwbHVnaW4gbmFtZXMgbmVlZCB0byBmb2xsb3cgY29sb24tc2VwYXJhdGVkIGZvcm1hdCBvZiBgZXh0ZW5zaW9uOnBsdWdpbmAuXG4gICAqL1xuICByZWFkb25seSBsb2NrUnVsZXM6IHN0cmluZ1tdO1xufVxuXG4vKipcbiAqIEFuIG9iamVjdCByZXByZXNlbnRpbmcgYSBzZXJ2ZXIgcmVwbHkgdG8gcGVyZm9ybWluZyBhbiBhY3Rpb24uXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUFjdGlvblJlcGx5IHtcbiAgLyoqXG4gICAqIFRoZSBzdGF0dXMgY2F0ZWdvcnkgb2YgdGhlIHJlcGx5LlxuICAgKi9cbiAgc3RhdHVzOiAnb2snIHwgJ3dhcm5pbmcnIHwgJ2Vycm9yJyB8IG51bGw7XG5cbiAgLyoqXG4gICAqIEFuIG9wdGlvbmFsIG1lc3NhZ2Ugd2hlbiB0aGUgc3RhdHVzIGlzIG5vdCAnb2snLlxuICAgKi9cbiAgbWVzc2FnZT86IHN0cmluZztcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBQbHVnaW5MaXN0TW9kZWwuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgUGx1Z2luTGlzdE1vZGVsIHtcbiAgZXhwb3J0IGludGVyZmFjZSBJQ29uZmlndXJhYmxlU3RhdGUge1xuICAgIC8qKlxuICAgICAqIFRoZSBwbHVnaW4gbGlzdCBzZWFyY2ggcXVlcnkuXG4gICAgICovXG4gICAgcXVlcnk/OiBzdHJpbmc7XG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgd2FybmluZyBpcyBkaXNjbGFpbWVkIG9yIG5vdC5cbiAgICAgKi9cbiAgICBpc0Rpc2NsYWltZWQ/OiBib29sZWFuO1xuICB9XG4gIC8qKiBBIHN1YnNldCBvZiBgSnVweXRlckxhYi5JSW5mb2AgaW50ZXJmYWNlIChkZWZpbmVkIHRvIHJlZHVjZSBBUEkgc3VyZmFjZSkgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUGx1Z2luRGF0YSB7XG4gICAgcmVhZG9ubHkgYXZhaWxhYmxlUGx1Z2luczogSnVweXRlckxhYi5JUGx1Z2luSW5mb1tdO1xuICB9XG4gIC8qKlxuICAgKiBUaGUgaW5pdGlhbGl6YXRpb24gb3B0aW9ucyBmb3IgYSBwbHVnaW5zIGxpc3QgbW9kZWwuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIGV4dGVuZHMgSUNvbmZpZ3VyYWJsZVN0YXRlIHtcbiAgICAvKipcbiAgICAgKiBQbHVnaW4gZGF0YS5cbiAgICAgKi9cbiAgICBwbHVnaW5EYXRhOiBJUGx1Z2luRGF0YTtcbiAgICAvKipcbiAgICAgKiBUcmFuc2xhdG9yLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgICAvKipcbiAgICAgKiBTZXJ2ZXIgY29ubmVjdGlvbiBzZXR0aW5ncy5cbiAgICAgKi9cbiAgICBzZXJ2ZXJTZXR0aW5ncz86IFNlcnZlckNvbm5lY3Rpb24uSVNldHRpbmdzO1xuICAgIC8qKlxuICAgICAqIEFkZGl0aW9uYWwgcGx1Z2lucyB0byBsb2NrIGluIGFkZGl0aW9uIHRvIHBsdWdpbnMgbG9ja2VkIG9uIHRoZSBzZXJ2ZXItc2lkZS5cbiAgICAgKlxuICAgICAqIFRoaXMgaXMgaW50ZW5kZWQgZXhjbHVzaXZlbHkgdG8gcHJvdGVjdCB1c2VyIGZyb20gc2hvb3RpbmcgdGhlbXNlbHZlcyBpblxuICAgICAqIHRoZSBmb290IGJ5IGFjY2lkZW50YWxseSBkaXNhYmxpbmcgdGhlIHBsdWdpbiBtYW5hZ2VyIG9yIG90aGVyIGNvcmUgcGx1Z2luc1xuICAgICAqICh3aGljaCB3b3VsZCBtZWFuIHRoZXkgY2Fubm90IHJlY292ZXIpIGFuZCBpcyBub3QgZW5mb3JjZWQgb24gc2VydmVyIHNpZGUuXG4gICAgICovXG4gICAgZXh0cmFMb2NrZWRQbHVnaW5zPzogc3RyaW5nW107XG4gIH1cbn1cblxuLyoqXG4gKiBUaGUgbW9kZWwgcmVwcmVzZW50aW5nIHBsdWdpbiBsaXN0LlxuICovXG5leHBvcnQgY2xhc3MgUGx1Z2luTGlzdE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIHtcbiAgY29uc3RydWN0b3Iob3B0aW9uczogUGx1Z2luTGlzdE1vZGVsLklPcHRpb25zKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9wbHVnaW5EYXRhID0gb3B0aW9ucy5wbHVnaW5EYXRhO1xuICAgIHRoaXMuX3NlcnZlclNldHRpbmdzID1cbiAgICAgIG9wdGlvbnMuc2VydmVyU2V0dGluZ3MgfHwgU2VydmVyQ29ubmVjdGlvbi5tYWtlU2V0dGluZ3MoKTtcbiAgICB0aGlzLl9xdWVyeSA9IG9wdGlvbnMucXVlcnkgfHwgJyc7XG4gICAgdGhpcy5faXNEaXNjbGFpbWVkID0gb3B0aW9ucy5pc0Rpc2NsYWltZWQgPz8gZmFsc2U7XG4gICAgdGhpcy5fZXh0cmFMb2NrZWRQbHVnaW5zID0gb3B0aW9ucy5leHRyYUxvY2tlZFBsdWdpbnMgPz8gW107XG4gICAgdGhpcy5yZWZyZXNoKClcbiAgICAgIC50aGVuKCgpID0+IHRoaXMuX3JlYWR5LnJlc29sdmUoKSlcbiAgICAgIC5jYXRjaChlID0+IHRoaXMuX3JlYWR5LnJlamVjdChlKSk7XG4gICAgdGhpcy5fdHJhbnMgPSAob3B0aW9ucy50cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIH1cblxuICBnZXQgYXZhaWxhYmxlKCk6IFJlYWRvbmx5QXJyYXk8SUVudHJ5PiB7XG4gICAgcmV0dXJuIFsuLi50aGlzLl9hdmFpbGFibGUudmFsdWVzKCldO1xuICB9XG5cbiAgLyoqXG4gICAqIENvbnRhaW5zIGFuIGVycm9yIG1lc3NhZ2UgaWYgYW4gZXJyb3Igb2NjdXJyZWQgd2hlbiBxdWVyeWluZyBwbHVnaW4gc3RhdHVzLlxuICAgKi9cbiAgc3RhdHVzRXJyb3I6IHN0cmluZyB8IG51bGwgPSBudWxsO1xuICAvKipcbiAgICogQ29udGFpbnMgYW4gZXJyb3IgbWVzc2FnZSBpZiBhbiBlcnJvciBvY2N1cnJlZCB3aGVuIGVuYWJsaW5nL2Rpc2FibGluZyBwbHVnaW4uXG4gICAqL1xuICBhY3Rpb25FcnJvcjogc3RyaW5nIHwgbnVsbCA9IG51bGw7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgcGx1Z2luIGRhdGEgaXMgc3RpbGwgZ2V0dGluZyBsb2FkZWQuXG4gICAqL1xuICBnZXQgaXNMb2FkaW5nKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0xvYWRpbmc7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgd2FybmluZyBpcyBkaXNjbGFpbWVkIG9yIG5vdC5cbiAgICovXG4gIGdldCBpc0Rpc2NsYWltZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzY2xhaW1lZDtcbiAgfVxuICBzZXQgaXNEaXNjbGFpbWVkKHY6IGJvb2xlYW4pIHtcbiAgICBpZiAodiAhPT0gdGhpcy5faXNEaXNjbGFpbWVkKSB7XG4gICAgICB0aGlzLl9pc0Rpc2NsYWltZWQgPSB2O1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgdGhpcy5fdHJhY2tlckRhdGFDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNlYXJjaCBxdWVyeS5cbiAgICpcbiAgICogU2V0dGluZyBpdHMgdmFsdWUgdHJpZ2dlcnMgYSBuZXcgc2VhcmNoLlxuICAgKi9cbiAgZ2V0IHF1ZXJ5KCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX3F1ZXJ5O1xuICB9XG4gIHNldCBxdWVyeSh2YWx1ZTogc3RyaW5nKSB7XG4gICAgaWYgKHRoaXMuX3F1ZXJ5ICE9PSB2YWx1ZSkge1xuICAgICAgdGhpcy5fcXVlcnkgPSB2YWx1ZTtcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICAgIHRoaXMuX3RyYWNrZXJEYXRhQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHRyYWNrYWJsZSBkYXRhIGNoYW5nZXNcbiAgICovXG4gIGdldCB0cmFja2VyRGF0YUNoYW5nZWQoKTogSVNpZ25hbDxQbHVnaW5MaXN0TW9kZWwsIHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fdHJhY2tlckRhdGFDaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHBsdWdpbnMgd2VyZSBmZXRjaGVkIGZyb20gdGhlIHNlcnZlclxuICAgKi9cbiAgZ2V0IHJlYWR5KCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9yZWFkeS5wcm9taXNlO1xuICB9XG5cbiAgLyoqXG4gICAqIEVuYWJsZSBhIHBsdWdpbi5cbiAgICpcbiAgICogQHBhcmFtIGVudHJ5IEFuIGVudHJ5IGluZGljYXRpbmcgd2hpY2ggcGx1Z2luIHRvIGVuYWJsZS5cbiAgICovXG4gIGFzeW5jIGVuYWJsZShlbnRyeTogSUVudHJ5KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKCF0aGlzLmlzRGlzY2xhaW1lZCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdVc2VyIGhhcyBub3QgY29uZmlybWVkIHRoZSBkaXNjbGFpbWVyJyk7XG4gICAgfVxuICAgIGF3YWl0IHRoaXMuX3BlcmZvcm1BY3Rpb24oJ2VuYWJsZScsIGVudHJ5KTtcbiAgICBlbnRyeS5lbmFibGVkID0gdHJ1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNhYmxlIGEgcGx1Z2luLlxuICAgKlxuICAgKiBAcGFyYW0gZW50cnkgQW4gZW50cnkgaW5kaWNhdGluZyB3aGljaCBwbHVnaW4gdG8gZGlzYWJsZS5cbiAgICogQHJldHVybnMgV2hldGhlciB0aGUgcGx1Z2luIHdhcyBkaXNhYmxlZFxuICAgKi9cbiAgYXN5bmMgZGlzYWJsZShlbnRyeTogSUVudHJ5KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKCF0aGlzLmlzRGlzY2xhaW1lZCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdVc2VyIGhhcyBub3QgY29uZmlybWVkIHRoZSBkaXNjbGFpbWVyJyk7XG4gICAgfVxuICAgIGNvbnN0IHsgZGVwZW5kYW50cywgb3B0aW9uYWxEZXBlbmRhbnRzIH0gPSB0aGlzLmdldERlcGVuZGFudHMoZW50cnkpO1xuICAgIGlmIChkZXBlbmRhbnRzLmxlbmd0aCA+IDApIHtcbiAgICAgIC8vIFdlIHJlcXVpcmUgdXNlciB0byBkaXNhYmxlIHBsdWdpbnMgb25lLWJ5LW9uZSBhcyBlYWNoIG9mIHRoZW0gbWF5IGhhdmVcbiAgICAgIC8vIGZ1cnRoZXIgZGVwZW5kZW5jaWVzIChvciBvcHRpb25hbCBkZXBlbmRlbmNpZXMpIGFuZCB3ZSB3YW50IHRoZSB1c2VyIHRvXG4gICAgICAvLyB0YWtlIGEgcGF1c2UgdG8gdGhpbmsgYWJvdXQgdGhvc2UuXG4gICAgICB2b2lkIHNob3dEaWFsb2coe1xuICAgICAgICB0aXRsZTogdGhpcy5fdHJhbnMuX18oJ1RoaXMgcGx1Z2luIGlzIHJlcXVpcmVkIGJ5IG90aGVyIHBsdWdpbnMnKSxcbiAgICAgICAgYm9keTogUGx1Z2luUmVxdWlyZWRNZXNzYWdlKHtcbiAgICAgICAgICBwbHVnaW46IGVudHJ5LFxuICAgICAgICAgIGRlcGVuZGFudHMsXG4gICAgICAgICAgdHJhbnM6IHRoaXMuX3RyYW5zXG4gICAgICAgIH0pLFxuICAgICAgICBidXR0b25zOiBbRGlhbG9nLm9rQnV0dG9uKCldXG4gICAgICB9KTtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgaWYgKG9wdGlvbmFsRGVwZW5kYW50cy5sZW5ndGggPiAwKSB7XG4gICAgICBjb25zdCB1c2VyQ29uZmlybWF0aW9uID0gYXdhaXQgc2hvd0RpYWxvZyh7XG4gICAgICAgIHRpdGxlOiB0aGlzLl90cmFucy5fXygnVGhpcyBwbHVnaW4gaXMgdXNlZCBieSBvdGhlciBwbHVnaW5zJyksXG4gICAgICAgIGJvZHk6IFBsdWdpbkluVXNlTWVzc2FnZSh7XG4gICAgICAgICAgcGx1Z2luOiBlbnRyeSxcbiAgICAgICAgICBvcHRpb25hbERlcGVuZGFudHMsXG4gICAgICAgICAgdHJhbnM6IHRoaXMuX3RyYW5zXG4gICAgICAgIH0pLFxuICAgICAgICBidXR0b25zOiBbXG4gICAgICAgICAgRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRoaXMuX3RyYW5zLl9fKCdEaXNhYmxlIGFueXdheScpIH0pLFxuICAgICAgICAgIERpYWxvZy5jYW5jZWxCdXR0b24oKVxuICAgICAgICBdXG4gICAgICB9KTtcbiAgICAgIGlmICghdXNlckNvbmZpcm1hdGlvbi5idXR0b24uYWNjZXB0KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBhd2FpdCB0aGlzLl9wZXJmb3JtQWN0aW9uKCdkaXNhYmxlJywgZW50cnkpO1xuICAgIGlmICh0aGlzLmFjdGlvbkVycm9yKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGVudHJ5LmVuYWJsZWQgPSBmYWxzZTtcbiAgfVxuXG4gIHByb3RlY3RlZCBnZXREZXBlbmRhbnRzKGVudHJ5OiBJRW50cnkpOiB7XG4gICAgZGVwZW5kYW50czogSUVudHJ5W107XG4gICAgb3B0aW9uYWxEZXBlbmRhbnRzOiBJRW50cnlbXTtcbiAgfSB7XG4gICAgY29uc3QgZGVwZW5kYW50cyA9IFtdO1xuICAgIGNvbnN0IG9wdGlvbmFsRGVwZW5kYW50cyA9IFtdO1xuICAgIGlmIChlbnRyeS5wcm92aWRlcykge1xuICAgICAgY29uc3QgdG9rZW5OYW1lID0gZW50cnkucHJvdmlkZXMubmFtZTtcbiAgICAgIGZvciAoY29uc3QgcGx1Z2luIG9mIHRoaXMuX2F2YWlsYWJsZS52YWx1ZXMoKSkge1xuICAgICAgICBpZiAoIXBsdWdpbi5lbmFibGVkKSB7XG4gICAgICAgICAgY29udGludWU7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKFxuICAgICAgICAgIHBsdWdpbi5yZXF1aXJlc1xuICAgICAgICAgICAgLmZpbHRlcih0b2tlbiA9PiAhIXRva2VuKVxuICAgICAgICAgICAgLnNvbWUodG9rZW4gPT4gdG9rZW4ubmFtZSA9PT0gdG9rZW5OYW1lKVxuICAgICAgICApIHtcbiAgICAgICAgICBkZXBlbmRhbnRzLnB1c2gocGx1Z2luKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoXG4gICAgICAgICAgcGx1Z2luLm9wdGlvbmFsXG4gICAgICAgICAgICAuZmlsdGVyKHRva2VuID0+ICEhdG9rZW4pXG4gICAgICAgICAgICAuc29tZSh0b2tlbiA9PiB0b2tlbi5uYW1lID09PSB0b2tlbk5hbWUpXG4gICAgICAgICkge1xuICAgICAgICAgIG9wdGlvbmFsRGVwZW5kYW50cy5wdXNoKHBsdWdpbik7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHtcbiAgICAgIGRlcGVuZGFudHMsXG4gICAgICBvcHRpb25hbERlcGVuZGFudHNcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlcmUgYXJlIGN1cnJlbnRseSBhbnkgYWN0aW9ucyBwZW5kaW5nLlxuICAgKi9cbiAgaGFzUGVuZGluZ0FjdGlvbnMoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX3BlbmRpbmdBY3Rpb25zLmxlbmd0aCA+IDA7XG4gIH1cblxuICAvKipcbiAgICogU2VuZCBhIHJlcXVlc3QgdG8gdGhlIHNlcnZlciB0byBwZXJmb3JtIGFuIGFjdGlvbiBvbiBhIHBsdWdpbi5cbiAgICpcbiAgICogQHBhcmFtIGFjdGlvbiBBIHZhbGlkIGFjdGlvbiB0byBwZXJmb3JtLlxuICAgKiBAcGFyYW0gZW50cnkgVGhlIHBsdWdpbiB0byBwZXJmb3JtIHRoZSBhY3Rpb24gb24uXG4gICAqL1xuICBwcml2YXRlIF9wZXJmb3JtQWN0aW9uKGFjdGlvbjogc3RyaW5nLCBlbnRyeTogSUVudHJ5KTogUHJvbWlzZTxJQWN0aW9uUmVwbHk+IHtcbiAgICB0aGlzLmFjdGlvbkVycm9yID0gbnVsbDtcblxuICAgIGNvbnN0IGFjdGlvblJlcXVlc3QgPSB0aGlzLl9yZXF1ZXN0QVBJPElBY3Rpb25SZXBseT4oXG4gICAgICB7fSxcbiAgICAgIHtcbiAgICAgICAgbWV0aG9kOiAnUE9TVCcsXG4gICAgICAgIGJvZHk6IEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICBjbWQ6IGFjdGlvbixcbiAgICAgICAgICBwbHVnaW5fbmFtZTogZW50cnkuaWRcbiAgICAgICAgfSlcbiAgICAgIH1cbiAgICApO1xuXG4gICAgYWN0aW9uUmVxdWVzdC5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgdGhpcy5hY3Rpb25FcnJvciA9IHJlYXNvbi50b1N0cmluZygpO1xuICAgIH0pO1xuXG4gICAgdGhpcy5fYWRkUGVuZGluZ0FjdGlvbihhY3Rpb25SZXF1ZXN0KTtcbiAgICByZXR1cm4gYWN0aW9uUmVxdWVzdDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSBwZW5kaW5nIGFjdGlvbi5cbiAgICpcbiAgICogQHBhcmFtIHBlbmRpbmcgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgYWN0aW9uIGlzIGNvbXBsZXRlZC5cbiAgICovXG4gIHByaXZhdGUgX2FkZFBlbmRpbmdBY3Rpb24ocGVuZGluZzogUHJvbWlzZTxhbnk+KTogdm9pZCB7XG4gICAgLy8gQWRkIHRvIHBlbmRpbmcgYWN0aW9ucyBjb2xsZWN0aW9uXG4gICAgdGhpcy5fcGVuZGluZ0FjdGlvbnMucHVzaChwZW5kaW5nKTtcblxuICAgIC8vIEVuc3VyZSBhY3Rpb24gaXMgcmVtb3ZlZCB3aGVuIHJlc29sdmVkXG4gICAgY29uc3QgcmVtb3ZlID0gKCkgPT4ge1xuICAgICAgY29uc3QgaSA9IHRoaXMuX3BlbmRpbmdBY3Rpb25zLmluZGV4T2YocGVuZGluZyk7XG4gICAgICB0aGlzLl9wZW5kaW5nQWN0aW9ucy5zcGxpY2UoaSwgMSk7XG4gICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHVuZGVmaW5lZCk7XG4gICAgfTtcbiAgICBwZW5kaW5nLnRoZW4ocmVtb3ZlLCByZW1vdmUpO1xuXG4gICAgLy8gU2lnbmFsIGNoYW5nZWQgc3RhdGVcbiAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHVuZGVmaW5lZCk7XG4gIH1cblxuICAvKipcbiAgICogUmVmcmVzaCBwbHVnaW4gbG9jayBzdGF0dXNlc1xuICAgKi9cbiAgYXN5bmMgcmVmcmVzaCgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0aGlzLnN0YXR1c0Vycm9yID0gbnVsbDtcbiAgICB0aGlzLl9pc0xvYWRpbmcgPSB0cnVlO1xuICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICB0cnkge1xuICAgICAgLy8gR2V0IHRoZSBsb2NrIHN0YXR1cyBmcm9tIGJhY2tlbmQ7IGlmIGJhY2tlbmQgaXMgbm90IGF2YWlsYWJsZSxcbiAgICAgIC8vIHdlIGFzc3VtZSB0aGF0IGFsbCBwbHVnaW5zIGFyZSBsb2NrZWQuXG4gICAgICBjb25zdCBmYWxsYmFjazogSVBsdWdpbk1hbmFnZXJTdGF0dXMgPSB7XG4gICAgICAgIGFsbExvY2tlZDogdHJ1ZSxcbiAgICAgICAgbG9ja1J1bGVzOiBbXVxuICAgICAgfTtcbiAgICAgIGNvbnN0IHN0YXR1cyA9XG4gICAgICAgIChhd2FpdCB0aGlzLl9yZXF1ZXN0QVBJPElQbHVnaW5NYW5hZ2VyU3RhdHVzPigpKSA/PyBmYWxsYmFjaztcblxuICAgICAgdGhpcy5fYXZhaWxhYmxlID0gbmV3IE1hcChcbiAgICAgICAgdGhpcy5fcGx1Z2luRGF0YS5hdmFpbGFibGVQbHVnaW5zLm1hcChwbHVnaW4gPT4ge1xuICAgICAgICAgIGxldCB0b2tlbkxhYmVsID0gcGx1Z2luLnByb3ZpZGVzXG4gICAgICAgICAgICA/IHBsdWdpbi5wcm92aWRlcy5uYW1lLnNwbGl0KCc6JylbMV1cbiAgICAgICAgICAgIDogdW5kZWZpbmVkO1xuICAgICAgICAgIGlmIChwbHVnaW4ucHJvdmlkZXMgJiYgIXRva2VuTGFiZWwpIHtcbiAgICAgICAgICAgIHRva2VuTGFiZWwgPSBwbHVnaW4ucHJvdmlkZXMubmFtZTtcbiAgICAgICAgICB9XG4gICAgICAgICAgcmV0dXJuIFtcbiAgICAgICAgICAgIHBsdWdpbi5pZCxcbiAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgLi4ucGx1Z2luLFxuICAgICAgICAgICAgICBsb2NrZWQ6IHRoaXMuX2lzTG9ja2VkKHBsdWdpbi5pZCwgc3RhdHVzKSxcbiAgICAgICAgICAgICAgdG9rZW5MYWJlbFxuICAgICAgICAgICAgfVxuICAgICAgICAgIF07XG4gICAgICAgIH0pXG4gICAgICApO1xuICAgIH0gY2F0Y2ggKHJlYXNvbikge1xuICAgICAgdGhpcy5zdGF0dXNFcnJvciA9IHJlYXNvbi50b1N0cmluZygpO1xuICAgIH0gZmluYWxseSB7XG4gICAgICB0aGlzLl9pc0xvYWRpbmcgPSBmYWxzZTtcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9pc0xvY2tlZChwbHVnaW5JZDogc3RyaW5nLCBzdGF0dXM6IElQbHVnaW5NYW5hZ2VyU3RhdHVzKTogYm9vbGVhbiB7XG4gICAgaWYgKHN0YXR1cy5hbGxMb2NrZWQpIHtcbiAgICAgIC8vIEFsbCBwbHVnaW5zIGFyZSBsb2NrZWQuXG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9XG4gICAgaWYgKHRoaXMuX2V4dHJhTG9ja2VkUGx1Z2lucy5pbmNsdWRlcyhwbHVnaW5JZCkpIHtcbiAgICAgIC8vIFBsdWdpbiBpcyBsb2NrZWQgb24gY2xpZW50IHNpZGUuXG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9XG4gICAgY29uc3QgZXh0ZW5zaW9uID0gcGx1Z2luSWQuc3BsaXQoJzonKVswXTtcbiAgICBpZiAoc3RhdHVzLmxvY2tSdWxlcy5pbmNsdWRlcyhleHRlbnNpb24pKSB7XG4gICAgICAvLyBFbnRpcmUgZXh0ZW5zaW9uIGlzIGxvY2tlZC5cbiAgICAgIHJldHVybiB0cnVlO1xuICAgIH1cbiAgICBpZiAoc3RhdHVzLmxvY2tSdWxlcy5pbmNsdWRlcyhwbHVnaW5JZCkpIHtcbiAgICAgIC8vIFRoaXMgcGx1Z2luIHNwZWNpZmljYWxseSBpcyBsb2NrZWQuXG4gICAgICByZXR1cm4gdHJ1ZTtcbiAgICB9XG4gICAgcmV0dXJuIGZhbHNlO1xuICB9XG5cbiAgLyoqXG4gICAqIENhbGwgdGhlIHBsdWdpbiBBUElcbiAgICpcbiAgICogQHBhcmFtIGVuZFBvaW50IEFQSSBSRVNUIGVuZCBwb2ludCBmb3IgdGhlIHBsdWdpblxuICAgKiBAcGFyYW0gaW5pdCBJbml0aWFsIHZhbHVlcyBmb3IgdGhlIHJlcXVlc3RcbiAgICogQHJldHVybnMgVGhlIHJlc3BvbnNlIGJvZHkgaW50ZXJwcmV0ZWQgYXMgSlNPTlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfcmVxdWVzdEFQSTxUPihcbiAgICBxdWVyeUFyZ3M6IHsgW2s6IHN0cmluZ106IGFueSB9ID0ge30sXG4gICAgaW5pdDogUmVxdWVzdEluaXQgPSB7fVxuICApOiBQcm9taXNlPFQ+IHtcbiAgICAvLyBNYWtlIHJlcXVlc3QgdG8gSnVweXRlciBBUElcbiAgICBjb25zdCBzZXR0aW5ncyA9IHRoaXMuX3NlcnZlclNldHRpbmdzO1xuICAgIGNvbnN0IHJlcXVlc3RVcmwgPSBVUkxFeHQuam9pbihzZXR0aW5ncy5iYXNlVXJsLCBQTFVHSU5fQVBJX1BBVEgpO1xuXG4gICAgbGV0IHJlc3BvbnNlOiBSZXNwb25zZTtcbiAgICB0cnkge1xuICAgICAgcmVzcG9uc2UgPSBhd2FpdCBTZXJ2ZXJDb25uZWN0aW9uLm1ha2VSZXF1ZXN0KFxuICAgICAgICByZXF1ZXN0VXJsICsgVVJMRXh0Lm9iamVjdFRvUXVlcnlTdHJpbmcocXVlcnlBcmdzKSxcbiAgICAgICAgaW5pdCxcbiAgICAgICAgc2V0dGluZ3NcbiAgICAgICk7XG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgIHRocm93IG5ldyBTZXJ2ZXJDb25uZWN0aW9uLk5ldHdvcmtFcnJvcihlcnJvcik7XG4gICAgfVxuXG4gICAgbGV0IGRhdGE6IGFueSA9IGF3YWl0IHJlc3BvbnNlLnRleHQoKTtcblxuICAgIGlmIChkYXRhLmxlbmd0aCA+IDApIHtcbiAgICAgIHRyeSB7XG4gICAgICAgIGRhdGEgPSBKU09OLnBhcnNlKGRhdGEpO1xuICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgY29uc29sZS5sb2coJ05vdCBhIEpTT04gcmVzcG9uc2UgYm9keS4nLCByZXNwb25zZSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgaWYgKCFyZXNwb25zZS5vaykge1xuICAgICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uUmVzcG9uc2VFcnJvcihyZXNwb25zZSwgZGF0YS5tZXNzYWdlIHx8IGRhdGEpO1xuICAgIH1cblxuICAgIHJldHVybiBkYXRhO1xuICB9XG5cbiAgcHJpdmF0ZSBfdHJhY2tlckRhdGFDaGFuZ2VkOiBTaWduYWw8UGx1Z2luTGlzdE1vZGVsLCB2b2lkPiA9IG5ldyBTaWduYWwodGhpcyk7XG4gIHByaXZhdGUgX2F2YWlsYWJsZTogTWFwPHN0cmluZywgSUVudHJ5PjtcbiAgcHJpdmF0ZSBfaXNMb2FkaW5nID0gZmFsc2U7XG4gIHByaXZhdGUgX3BlbmRpbmdBY3Rpb25zOiBQcm9taXNlPGFueT5bXSA9IFtdO1xuICBwcml2YXRlIF9zZXJ2ZXJTZXR0aW5nczogU2VydmVyQ29ubmVjdGlvbi5JU2V0dGluZ3M7XG4gIHByaXZhdGUgX3JlYWR5ID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xuICBwcml2YXRlIF9xdWVyeTogc3RyaW5nO1xuICBwcml2YXRlIF9wbHVnaW5EYXRhOiBQbHVnaW5MaXN0TW9kZWwuSVBsdWdpbkRhdGE7XG4gIHByaXZhdGUgX2V4dHJhTG9ja2VkUGx1Z2luczogc3RyaW5nW107XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfaXNEaXNjbGFpbWVkOiBib29sZWFuO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcblxuLyoqXG4gKiBUaGUgcGx1Z2luIG1hbmFnZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJUGx1Z2luTWFuYWdlciA9IG5ldyBUb2tlbjxJUGx1Z2luTWFuYWdlcj4oXG4gICdAanVweXRlcmxhYi9wbHVnaW5tYW5hZ2VyOklQbHVnaW5NYW5hZ2VyJyxcbiAgYEEgY2FuYXJ5IGZvciBwbHVnaW4gbWFuYWdlciBwcmVzZW5jZSwgd2l0aCBhIG1ldGhvZCB0byBvcGVuIHRoZSBwbHVnaW4gbWFuYWdlciB3aWRnZXQuYFxuKTtcblxuLyoqXG4gKiBBIGNsYXNzIHRoYXQgZXhwb3NlcyBhIGNvbW1hbmQgdG8gb3BlbiBwbHVnaW4gbWFuYWdlci5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJUGx1Z2luTWFuYWdlciB7XG4gIC8qKlxuICAgKiBPcGVuIHRoZSBwbHVnaW4gbWFuYWdlci5cbiAgICovXG4gIG9wZW4oKTogUHJvbWlzZTx2b2lkPjtcbn1cbiIsIi8qXG4gKiBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbiAqIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4gKi9cblxuaW1wb3J0IHsgVkRvbVJlbmRlcmVyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgRmlsdGVyQm94LCBsb2NrSWNvbiwgVGFibGUgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFBhbmVsIH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IEFjdGlvbiwgSUVudHJ5LCBQbHVnaW5MaXN0TW9kZWwgfSBmcm9tICcuL21vZGVsJztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcGx1Z2lucyBwYW5lbC5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBQbHVnaW5zIHtcbiAgLyoqXG4gICAqIFRoZSBpbml0aWFsaXphdGlvbiBvcHRpb25zIGZvciBhIHBsdWdpbnMgcGFuZWwuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICBtb2RlbDogUGx1Z2luTGlzdE1vZGVsO1xuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xuICB9XG59XG5cbi8qKlxuICogUGFuZWwgd2l0aCBhIHRhYmxlIG9mIGF2YWlsYWJsZSBwbHVnaW5zIGFsbG93aW5nIHRvIGVuYWJsZS9kaXNhYmxlIGVhY2guXG4gKi9cbmV4cG9ydCBjbGFzcyBQbHVnaW5zIGV4dGVuZHMgUGFuZWwge1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBQbHVnaW5zLklPcHRpb25zKSB7XG4gICAgY29uc3QgeyBtb2RlbCwgdHJhbnNsYXRvciB9ID0gb3B0aW9ucztcbiAgICBzdXBlcigpO1xuICAgIHRoaXMubW9kZWwgPSBtb2RlbDtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1wbHVnaW5tYW5hZ2VyJyk7XG5cbiAgICB0aGlzLnRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICB0aGlzLmFkZFdpZGdldChuZXcgRGlzY2xhaW1lcihtb2RlbCwgdGhpcy50cmFucykpO1xuXG4gICAgY29uc3QgaGVhZGVyID0gbmV3IEhlYWRlcihtb2RlbCwgdGhpcy50cmFucyk7XG4gICAgdGhpcy5hZGRXaWRnZXQoaGVhZGVyKTtcblxuICAgIGNvbnN0IGF2YWlsYWJsZUxpc3QgPSBuZXcgQXZhaWxhYmxlTGlzdChtb2RlbCwgdGhpcy50cmFucyk7XG4gICAgdGhpcy5hZGRXaWRnZXQoYXZhaWxhYmxlTGlzdCk7XG4gIH1cbiAgcmVhZG9ubHkgbW9kZWw6IFBsdWdpbkxpc3RNb2RlbDtcbiAgcHJvdGVjdGVkIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbn1cblxuY2xhc3MgQXZhaWxhYmxlTGlzdCBleHRlbmRzIFZEb21SZW5kZXJlcjxQbHVnaW5MaXN0TW9kZWw+IHtcbiAgY29uc3RydWN0b3IoXG4gICAgbW9kZWw6IFBsdWdpbkxpc3RNb2RlbCxcbiAgICBwcm90ZWN0ZWQgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICkge1xuICAgIHN1cGVyKG1vZGVsKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1wbHVnaW5tYW5hZ2VyLUF2YWlsYWJsZUxpc3QnKTtcbiAgfVxuXG4gIHJlbmRlcigpOiBKU1guRWxlbWVudCB7XG4gICAgcmV0dXJuIChcbiAgICAgIDw+XG4gICAgICAgIHt0aGlzLm1vZGVsLnN0YXR1c0Vycm9yICE9PSBudWxsID8gKFxuICAgICAgICAgIDxFcnJvck1lc3NhZ2U+XG4gICAgICAgICAgICB7dGhpcy50cmFucy5fXyhcbiAgICAgICAgICAgICAgJ0Vycm9yIHF1ZXJ5aW5nIGluc3RhbGxlZCBleHRlbnNpb25zJTEnLFxuICAgICAgICAgICAgICB0aGlzLm1vZGVsLnN0YXR1c0Vycm9yID8gYDogJHt0aGlzLm1vZGVsLnN0YXR1c0Vycm9yfWAgOiAnLidcbiAgICAgICAgICAgICl9XG4gICAgICAgICAgPC9FcnJvck1lc3NhZ2U+XG4gICAgICAgICkgOiB0aGlzLm1vZGVsLmlzTG9hZGluZyA/IChcbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLXBsdWdpbm1hbmFnZXItbG9hZGVyXCI+XG4gICAgICAgICAgICB7dGhpcy50cmFucy5fXygnVXBkYXRpbmcgcGx1Z2luIGxpc3TigKYnKX1cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKSA6IChcbiAgICAgICAgICA8VGFibGU8SUVudHJ5PlxuICAgICAgICAgICAgYmxhbmtJbmRpY2F0b3I9eygpID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIDxkaXY+e3RoaXMudHJhbnMuX18oJ05vIGVudHJpZXMnKX08L2Rpdj47XG4gICAgICAgICAgICB9fVxuICAgICAgICAgICAgc29ydEtleT17J3BsdWdpbi1pZCd9XG4gICAgICAgICAgICByb3dzPXt0aGlzLm1vZGVsLmF2YWlsYWJsZVxuICAgICAgICAgICAgICAuZmlsdGVyKHBrZyA9PiB7XG4gICAgICAgICAgICAgICAgY29uc3QgcGF0dGVybiA9IG5ldyBSZWdFeHAodGhpcy5tb2RlbC5xdWVyeSwgJ2knKTtcbiAgICAgICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgICAgcGF0dGVybi50ZXN0KHBrZy5pZCkgfHxcbiAgICAgICAgICAgICAgICAgIHBhdHRlcm4udGVzdChwa2cuZXh0ZW5zaW9uKSB8fFxuICAgICAgICAgICAgICAgICAgKHBrZy50b2tlbkxhYmVsICYmIHBhdHRlcm4udGVzdChwa2cudG9rZW5MYWJlbCkpXG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgLm1hcChkYXRhID0+IHtcbiAgICAgICAgICAgICAgICByZXR1cm4ge1xuICAgICAgICAgICAgICAgICAgZGF0YTogZGF0YSxcbiAgICAgICAgICAgICAgICAgIGtleTogZGF0YS5pZFxuICAgICAgICAgICAgICAgIH07XG4gICAgICAgICAgICAgIH0pfVxuICAgICAgICAgICAgY29sdW1ucz17W1xuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgaWQ6ICdwbHVnaW4taWQnLFxuICAgICAgICAgICAgICAgIGxhYmVsOiB0aGlzLnRyYW5zLl9fKCdQbHVnaW4nKSxcbiAgICAgICAgICAgICAgICByZW5kZXJDZWxsOiAocm93OiBJRW50cnkpID0+IChcbiAgICAgICAgICAgICAgICAgIDw+XG4gICAgICAgICAgICAgICAgICAgIDxjb2RlPntyb3cuaWR9PC9jb2RlPlxuICAgICAgICAgICAgICAgICAgICA8YnIgLz5cbiAgICAgICAgICAgICAgICAgICAge3Jvdy5kZXNjcmlwdGlvbn1cbiAgICAgICAgICAgICAgICAgIDwvPlxuICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICAgICAgc29ydDogKGE6IElFbnRyeSwgYjogSUVudHJ5KSA9PiBhLmlkLmxvY2FsZUNvbXBhcmUoYi5pZClcbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGlkOiAnZGVzY3JpcHRpb24nLFxuICAgICAgICAgICAgICAgIGxhYmVsOiB0aGlzLnRyYW5zLl9fKCdEZXNjcmlwdGlvbicpLFxuICAgICAgICAgICAgICAgIHJlbmRlckNlbGw6IChyb3c6IElFbnRyeSkgPT4gPD57cm93LmRlc2NyaXB0aW9ufTwvPixcbiAgICAgICAgICAgICAgICBzb3J0OiAoYTogSUVudHJ5LCBiOiBJRW50cnkpID0+XG4gICAgICAgICAgICAgICAgICBhLmRlc2NyaXB0aW9uICYmIGIuZGVzY3JpcHRpb25cbiAgICAgICAgICAgICAgICAgICAgPyBhLmRlc2NyaXB0aW9uLmxvY2FsZUNvbXBhcmUoYi5kZXNjcmlwdGlvbilcbiAgICAgICAgICAgICAgICAgICAgOiB1bmRlZmluZWQsXG4gICAgICAgICAgICAgICAgaXNIaWRkZW46IHRydWVcbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGlkOiAnYXV0b3N0YXJ0JyxcbiAgICAgICAgICAgICAgICBsYWJlbDogdGhpcy50cmFucy5fXygnQXV0b3N0YXJ0PycpLFxuICAgICAgICAgICAgICAgIHJlbmRlckNlbGw6IChyb3c6IElFbnRyeSkgPT4ge1xuICAgICAgICAgICAgICAgICAgc3dpdGNoIChyb3cuYXV0b1N0YXJ0KSB7XG4gICAgICAgICAgICAgICAgICAgIGNhc2UgJ2RlZmVyJzpcbiAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gdGhpcy50cmFucy5fXygnRGVmZXInKTtcbiAgICAgICAgICAgICAgICAgICAgY2FzZSB0cnVlOlxuICAgICAgICAgICAgICAgICAgICAgIHJldHVybiB0aGlzLnRyYW5zLl9fKCdZZXMnKTtcbiAgICAgICAgICAgICAgICAgICAgY2FzZSBmYWxzZTpcbiAgICAgICAgICAgICAgICAgICAgY2FzZSB1bmRlZmluZWQ6IC8vIFRoZSBkZWZhdWx0IGlzIGBmYWxzZWAuXG4gICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHRoaXMudHJhbnMuX18oJ05vJyk7XG4gICAgICAgICAgICAgICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICAgICAgICAgICAgY29uc3QgbGVmdG92ZXI6IG5ldmVyID0gcm93LmF1dG9TdGFydDtcbiAgICAgICAgICAgICAgICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYFVua25vd24gdmFsdWU6ICR7bGVmdG92ZXJ9YCk7XG4gICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICBzb3J0OiAoYTogSUVudHJ5LCBiOiBJRW50cnkpID0+XG4gICAgICAgICAgICAgICAgICBhLmF1dG9TdGFydCA9PT0gYi5hdXRvU3RhcnQgPyAwIDogYS5hdXRvU3RhcnQgPyAtMSA6IDFcbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGlkOiAncmVxdWlyZXMnLFxuICAgICAgICAgICAgICAgIGxhYmVsOiB0aGlzLnRyYW5zLl9fKCdEZXBlbmRzIG9uJyksXG4gICAgICAgICAgICAgICAgcmVuZGVyQ2VsbDogKHJvdzogSUVudHJ5KSA9PiAoXG4gICAgICAgICAgICAgICAgICA8Pntyb3cucmVxdWlyZXMubWFwKHYgPT4gdi5uYW1lKS5qb2luKCdcXG4nKX08Lz5cbiAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgICAgIHNvcnQ6IChhOiBJRW50cnksIGI6IElFbnRyeSkgPT5cbiAgICAgICAgICAgICAgICAgIChhLnJlcXVpcmVzIHx8IFtdKS5sZW5ndGggLSAoYi5yZXF1aXJlcyB8fCBbXSkubGVuZ3RoLFxuICAgICAgICAgICAgICAgIGlzSGlkZGVuOiB0cnVlXG4gICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICBpZDogJ2V4dGVuc2lvbicsXG4gICAgICAgICAgICAgICAgbGFiZWw6IHRoaXMudHJhbnMuX18oJ0V4dGVuc2lvbicpLFxuICAgICAgICAgICAgICAgIHJlbmRlckNlbGw6IChyb3c6IElFbnRyeSkgPT4gPD57cm93LmV4dGVuc2lvbn08Lz4sXG4gICAgICAgICAgICAgICAgc29ydDogKGE6IElFbnRyeSwgYjogSUVudHJ5KSA9PlxuICAgICAgICAgICAgICAgICAgYS5leHRlbnNpb24ubG9jYWxlQ29tcGFyZShiLmV4dGVuc2lvbilcbiAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAge1xuICAgICAgICAgICAgICAgIGlkOiAncHJvdmlkZXMnLFxuICAgICAgICAgICAgICAgIGxhYmVsOiB0aGlzLnRyYW5zLl9fKCdQcm92aWRlcycpLFxuICAgICAgICAgICAgICAgIHJlbmRlckNlbGw6IChyb3c6IElFbnRyeSkgPT4gKFxuICAgICAgICAgICAgICAgICAgPD5cbiAgICAgICAgICAgICAgICAgICAge3Jvdy5wcm92aWRlcyA/IChcbiAgICAgICAgICAgICAgICAgICAgICA8Y29kZSB0aXRsZT17cm93LnByb3ZpZGVzLm5hbWV9Pntyb3cudG9rZW5MYWJlbH08L2NvZGU+XG4gICAgICAgICAgICAgICAgICAgICkgOiAoXG4gICAgICAgICAgICAgICAgICAgICAgJy0nXG4gICAgICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgICA8Lz5cbiAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgICAgIHNvcnQ6IChhOiBJRW50cnksIGI6IElFbnRyeSkgPT5cbiAgICAgICAgICAgICAgICAgIChhLnRva2VuTGFiZWwgfHwgJycpLmxvY2FsZUNvbXBhcmUoYi50b2tlbkxhYmVsIHx8ICcnKVxuICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgaWQ6ICdlbmFibGVkJyxcbiAgICAgICAgICAgICAgICBsYWJlbDogdGhpcy50cmFucy5fXygnRW5hYmxlZCcpLFxuICAgICAgICAgICAgICAgIHJlbmRlckNlbGw6IChyb3c6IElFbnRyeSkgPT4gKFxuICAgICAgICAgICAgICAgICAgPD5cbiAgICAgICAgICAgICAgICAgICAgPGlucHV0XG4gICAgICAgICAgICAgICAgICAgICAgdHlwZT1cImNoZWNrYm94XCJcbiAgICAgICAgICAgICAgICAgICAgICBjaGVja2VkPXtyb3cuZW5hYmxlZH1cbiAgICAgICAgICAgICAgICAgICAgICBkaXNhYmxlZD17cm93LmxvY2tlZCB8fCAhdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWR9XG4gICAgICAgICAgICAgICAgICAgICAgdGl0bGU9e1xuICAgICAgICAgICAgICAgICAgICAgICAgcm93LmxvY2tlZCB8fCAhdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWRcbiAgICAgICAgICAgICAgICAgICAgICAgICAgPyByb3cubG9ja2VkXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgPyB0aGlzLnRyYW5zLl9fKCdUaGlzIHBsdWdpbiBpcyBsb2NrZWQuJylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICA6IHRoaXMudHJhbnMuX18oXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICdUbyBlbmFibGUvZGlzYWJsZSwgcGxlYXNlIGFja25vd2xlZGdlIHRoZSBkaXNjbGFpbWVyLidcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgICAgICAgOiByb3cuZW5hYmxlZFxuICAgICAgICAgICAgICAgICAgICAgICAgICA/IHRoaXMudHJhbnMuX18oJ0Rpc2FibGUgJTEgcGx1Z2luJywgcm93LmlkKVxuICAgICAgICAgICAgICAgICAgICAgICAgICA6IHRoaXMudHJhbnMuX18oJ0VuYWJsZSAlMSBwbHVnaW4nLCByb3cuaWQpXG4gICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXsoXG4gICAgICAgICAgICAgICAgICAgICAgICBldmVudDogUmVhY3QuQ2hhbmdlRXZlbnQ8SFRNTElucHV0RWxlbWVudD5cbiAgICAgICAgICAgICAgICAgICAgICApID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmICghdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWQpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICAgICAgaWYgKGV2ZW50LnRhcmdldC5jaGVja2VkKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHZvaWQgdGhpcy5vbkFjdGlvbignZW5hYmxlJywgcm93KTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHZvaWQgdGhpcy5vbkFjdGlvbignZGlzYWJsZScsIHJvdyk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICAgICAge3Jvdy5sb2NrZWQgPyAoXG4gICAgICAgICAgICAgICAgICAgICAgPGxvY2tJY29uLnJlYWN0XG4gICAgICAgICAgICAgICAgICAgICAgICB0YWc9XCJzcGFuXCJcbiAgICAgICAgICAgICAgICAgICAgICAgIHRpdGxlPXt0aGlzLnRyYW5zLl9fKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAnVGhpcyBwbHVnaW4gd2FzIGxvY2tlZCBieSBzeXN0ZW0gYWRtaW5pc3RyYXRvciBvciBpcyBhIGNyaXRpY2FsIGRlcGVuZGVuY3kgYW5kIGNhbm5vdCBiZSBlbmFibGVkL2Rpc2FibGVkLidcbiAgICAgICAgICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICAgICAgKSA6IChcbiAgICAgICAgICAgICAgICAgICAgICAnJ1xuICAgICAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgICAgICAgPC8+XG4gICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgICAgICBzb3J0OiAoYTogSUVudHJ5LCBiOiBJRW50cnkpID0+ICthLmVuYWJsZWQgLSArYi5lbmFibGVkXG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIF19XG4gICAgICAgICAgLz5cbiAgICAgICAgKX1cbiAgICAgIDwvPlxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQ2FsbGJhY2sgaGFuZGxlciBmb3Igd2hlbiB0aGUgdXNlciB3YW50cyB0byBwZXJmb3JtIGFuIGFjdGlvbiBvbiBhbiBleHRlbnNpb24uXG4gICAqXG4gICAqIEBwYXJhbSBhY3Rpb24gVGhlIGFjdGlvbiB0byBwZXJmb3JtLlxuICAgKiBAcGFyYW0gZW50cnkgVGhlIGVudHJ5IHRvIHBlcmZvcm0gdGhlIGFjdGlvbiBvbi5cbiAgICovXG4gIG9uQWN0aW9uKGFjdGlvbjogQWN0aW9uLCBlbnRyeTogSUVudHJ5KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgc3dpdGNoIChhY3Rpb24pIHtcbiAgICAgIGNhc2UgJ2VuYWJsZSc6XG4gICAgICAgIHJldHVybiB0aGlzLm1vZGVsLmVuYWJsZShlbnRyeSk7XG4gICAgICBjYXNlICdkaXNhYmxlJzpcbiAgICAgICAgcmV0dXJuIHRoaXMubW9kZWwuZGlzYWJsZShlbnRyeSk7XG4gICAgICBkZWZhdWx0OlxuICAgICAgICB0aHJvdyBuZXcgRXJyb3IoYEludmFsaWQgYWN0aW9uOiAke2FjdGlvbn1gKTtcbiAgICB9XG4gIH1cbn1cblxuY2xhc3MgRGlzY2xhaW1lciBleHRlbmRzIFZEb21SZW5kZXJlcjxQbHVnaW5MaXN0TW9kZWw+IHtcbiAgY29uc3RydWN0b3IoXG4gICAgbW9kZWw6IFBsdWdpbkxpc3RNb2RlbCxcbiAgICBwcm90ZWN0ZWQgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICkge1xuICAgIHN1cGVyKG1vZGVsKTtcbiAgICB0aGlzLmFkZENsYXNzKCdqcC1wbHVnaW5tYW5hZ2VyLURpc2NsYWltZXInKTtcbiAgfVxuICByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgIHJldHVybiAoXG4gICAgICA8ZGl2PlxuICAgICAgICA8ZGl2PlxuICAgICAgICAgIHt0aGlzLnRyYW5zLl9fKFxuICAgICAgICAgICAgJ0N1c3RvbWlzZSB5b3VyIGV4cGVyaWVuY2UvaW1wcm92ZSBwZXJmb3JtYW5jZSBieSBkaXNhYmxpbmcgcGx1Z2lucyB5b3UgZG8gbm90IG5lZWQuIFRvIGRpc2FibGUgb3IgdW5pbnN0YWxsIGFuIGVudGlyZSBleHRlbnNpb24gdXNlIHRoZSBFeHRlbnNpb24gTWFuYWdlciBpbnN0ZWFkLiBDaGFuZ2VzIHdpbGwgYXBwbHkgYWZ0ZXIgcmVsb2FkaW5nIEp1cHl0ZXJMYWIuJ1xuICAgICAgICAgICl9XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8bGFiZWw+XG4gICAgICAgICAgPGlucHV0XG4gICAgICAgICAgICB0eXBlPVwiY2hlY2tib3hcIlxuICAgICAgICAgICAgY2xhc3NOYW1lPVwianAtbW9kLXN0eWxlZCBqcC1wbHVnaW5tYW5hZ2VyLURpc2NsYWltZXItY2hlY2tib3hcIlxuICAgICAgICAgICAgZGVmYXVsdENoZWNrZWQ9e3RoaXMubW9kZWwuaXNEaXNjbGFpbWVkfVxuICAgICAgICAgICAgb25DaGFuZ2U9e2V2ZW50ID0+IHtcbiAgICAgICAgICAgICAgdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWQgPSBldmVudC50YXJnZXQuY2hlY2tlZDtcbiAgICAgICAgICAgIH19XG4gICAgICAgICAgLz5cbiAgICAgICAgICB7dGhpcy50cmFucy5fXyhcbiAgICAgICAgICAgICdJIHVuZGVyc3RhbmQgdGhhdCBkaXNhYmxpbmcgY29yZSBhcHBsaWNhdGlvbiBwbHVnaW5zIG1heSByZW5kZXIgZmVhdHVyZXMgYW5kIHBhcnRzIG9mIHRoZSB1c2VyIGludGVyZmFjZSB1bmF2YWlsYWJsZSBhbmQgcmVjb3ZlcnkgdXNpbmcgYGp1cHl0ZXIgbGFiZXh0ZW5zaW9uIGVuYWJsZSA8cGx1Z2luLW5hbWU+YCBjb21tYW5kIG1heSBiZSByZXF1aXJlZCdcbiAgICAgICAgICApfVxuICAgICAgICA8L2xhYmVsPlxuICAgICAgPC9kaXY+XG4gICAgKTtcbiAgfVxufVxuXG5jbGFzcyBIZWFkZXIgZXh0ZW5kcyBWRG9tUmVuZGVyZXI8UGx1Z2luTGlzdE1vZGVsPiB7XG4gIGNvbnN0cnVjdG9yKFxuICAgIG1vZGVsOiBQbHVnaW5MaXN0TW9kZWwsXG4gICAgcHJvdGVjdGVkIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApIHtcbiAgICBzdXBlcihtb2RlbCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtcGx1Z2lubWFuYWdlci1IZWFkZXInKTtcbiAgfVxuXG4gIHJlbmRlcigpOiBKU1guRWxlbWVudCB7XG4gICAgcmV0dXJuIChcbiAgICAgIDw+XG4gICAgICAgIDxGaWx0ZXJCb3hcbiAgICAgICAgICBwbGFjZWhvbGRlcj17dGhpcy50cmFucy5fXygnRmlsdGVyJyl9XG4gICAgICAgICAgdXBkYXRlRmlsdGVyPXsoZm4sIHF1ZXJ5KSA9PiB7XG4gICAgICAgICAgICB0aGlzLm1vZGVsLnF1ZXJ5ID0gcXVlcnkgPz8gJyc7XG4gICAgICAgICAgfX1cbiAgICAgICAgICBpbml0aWFsUXVlcnk9e3RoaXMubW9kZWwucXVlcnl9XG4gICAgICAgICAgdXNlRnV6enlGaWx0ZXI9e2ZhbHNlfVxuICAgICAgICAvPlxuICAgICAgICA8ZGl2XG4gICAgICAgICAgY2xhc3NOYW1lPXtganAtcGx1Z2lubWFuYWdlci1wZW5kaW5nICR7XG4gICAgICAgICAgICB0aGlzLm1vZGVsLmhhc1BlbmRpbmdBY3Rpb25zKCkgPyAnanAtbW9kLWhhc1BlbmRpbmcnIDogJydcbiAgICAgICAgICB9YH1cbiAgICAgICAgLz5cbiAgICAgICAge3RoaXMubW9kZWwuYWN0aW9uRXJyb3IgJiYgKFxuICAgICAgICAgIDxFcnJvck1lc3NhZ2U+XG4gICAgICAgICAgICA8cD57dGhpcy50cmFucy5fXygnRXJyb3Igd2hlbiBwZXJmb3JtaW5nIGFuIGFjdGlvbi4nKX08L3A+XG4gICAgICAgICAgICA8cD57dGhpcy50cmFucy5fXygnUmVhc29uIGdpdmVuOicpfTwvcD5cbiAgICAgICAgICAgIDxwcmU+e3RoaXMubW9kZWwuYWN0aW9uRXJyb3J9PC9wcmU+XG4gICAgICAgICAgPC9FcnJvck1lc3NhZ2U+XG4gICAgICAgICl9XG4gICAgICA8Lz5cbiAgICApO1xuICB9XG59XG5cbmZ1bmN0aW9uIEVycm9yTWVzc2FnZShwcm9wczogUmVhY3QuUHJvcHNXaXRoQ2hpbGRyZW4pIHtcbiAgcmV0dXJuIDxkaXYgY2xhc3NOYW1lPVwianAtcGx1Z2lubWFuYWdlci1lcnJvclwiPntwcm9wcy5jaGlsZHJlbn08L2Rpdj47XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=