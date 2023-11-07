"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_extensionmanager_lib_index_js"],{

/***/ "../packages/extensionmanager/lib/dialog.js":
/*!**************************************************!*\
  !*** ../packages/extensionmanager/lib/dialog.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "reportInstallError": () => (/* binding */ reportInstallError)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Show a dialog box reporting an error during installation of an extension.
 *
 * @param name The name of the extension
 * @param errorMessage Any error message giving details about the failure.
 */
function reportInstallError(name, errorMessage, translator) {
    translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
    const trans = translator.load('jupyterlab');
    const entries = [];
    entries.push(react__WEBPACK_IMPORTED_MODULE_2__.createElement("p", null, trans.__(`An error occurred installing "${name}".`)));
    if (errorMessage) {
        entries.push(react__WEBPACK_IMPORTED_MODULE_2__.createElement("p", null,
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("span", { className: "jp-extensionmanager-dialog-subheader" }, trans.__('Error message:'))), react__WEBPACK_IMPORTED_MODULE_2__.createElement("pre", null, errorMessage.trim()));
    }
    const body = react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "jp-extensionmanager-dialog" }, entries);
    void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
        title: trans.__('Extension Installation Error'),
        body,
        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({ label: trans.__('Ok') })]
    });
}


/***/ }),

/***/ "../packages/extensionmanager/lib/index.js":
/*!*************************************************!*\
  !*** ../packages/extensionmanager/lib/index.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ExtensionsPanel": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.ExtensionsPanel),
/* harmony export */   "ListModel": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_0__.ListModel)
/* harmony export */ });
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./model */ "../packages/extensionmanager/lib/model.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/extensionmanager/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module extensionmanager
 */




/***/ }),

/***/ "../packages/extensionmanager/lib/model.js":
/*!*************************************************!*\
  !*** ../packages/extensionmanager/lib/model.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ListModel": () => (/* binding */ ListModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var semver__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! semver */ "../node_modules/semver/index.js");
/* harmony import */ var semver__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(semver__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _dialog__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./dialog */ "../packages/extensionmanager/lib/dialog.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/* global RequestInit */








/**
 * The server API path for querying/modifying installed extensions.
 */
const EXTENSION_API_PATH = 'lab/api/extensions';
/**
 * Model for an extension list.
 */
class ListModel extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.VDomModel {
    constructor(serviceManager, translator) {
        super();
        this.actionError = null;
        /**
         * Contains an error message if an error occurred when querying installed extensions.
         */
        this.installedError = null;
        /**
         * Contains an error message if an error occurred when searching for extensions.
         */
        this.searchError = null;
        /**
         * Whether a reload should be considered due to actions taken.
         */
        this.promptReload = false;
        this._isDisclaimed = false;
        this._isEnabled = false;
        this._isLoadingInstalledExtensions = false;
        this._isSearching = false;
        this._query = '';
        this._page = 1;
        this._pagination = 30;
        this._lastPage = 1;
        this._pendingActions = [];
        const metadata = JSON.parse(
        // The page config option may not be defined; e.g. in the federated example
        _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('extensionManager') || '{}');
        this.name = metadata.name;
        this.canInstall = metadata.can_install;
        this.installPath = metadata.install_path;
        this.translator = translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator;
        this._installed = [];
        this._lastSearchResult = [];
        this.serviceManager = serviceManager;
        this._debouncedSearch = new _lumino_polling__WEBPACK_IMPORTED_MODULE_5__.Debouncer(this.search.bind(this), 1000);
    }
    /**
     * A readonly array of the installed extensions.
     */
    get installed() {
        return this._installed;
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
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * Whether the extension manager is enabled or not.
     */
    get isEnabled() {
        return this._isEnabled;
    }
    set isEnabled(v) {
        if (v !== this._isEnabled) {
            this._isEnabled = v;
            this.stateChanged.emit();
        }
    }
    get isLoadingInstalledExtensions() {
        return this._isLoadingInstalledExtensions;
    }
    get isSearching() {
        return this._isSearching;
    }
    /**
     * A readonly array containing the latest search result
     */
    get searchResult() {
        return this._lastSearchResult;
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
            this._page = 1;
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * The current search page.
     *
     * Setting its value triggers a new search.
     *
     * ### Note
     * First page is 1.
     */
    get page() {
        return this._page;
    }
    set page(value) {
        if (this._page !== value) {
            this._page = value;
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * The search pagination.
     *
     * Setting its value triggers a new search.
     */
    get pagination() {
        return this._pagination;
    }
    set pagination(value) {
        if (this._pagination !== value) {
            this._pagination = value;
            void this._debouncedSearch.invoke();
        }
    }
    /**
     * The last page of results in the current search.
     */
    get lastPage() {
        return this._lastPage;
    }
    /**
     * Dispose the extensions list model.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._debouncedSearch.dispose();
        super.dispose();
    }
    /**
     * Whether there are currently any actions pending.
     */
    hasPendingActions() {
        return this._pendingActions.length > 0;
    }
    /**
     * Install an extension.
     *
     * @param entry An entry indicating which extension to install.
     */
    async install(entry) {
        await this.performAction('install', entry).then(data => {
            if (data.status !== 'ok') {
                (0,_dialog__WEBPACK_IMPORTED_MODULE_7__.reportInstallError)(entry.name, data.message, this.translator);
            }
            return this.update(true);
        });
    }
    /**
     * Uninstall an extension.
     *
     * @param entry An entry indicating which extension to uninstall.
     */
    async uninstall(entry) {
        if (!entry.installed) {
            throw new Error(`Not installed, cannot uninstall: ${entry.name}`);
        }
        await this.performAction('uninstall', entry);
        return this.update(true);
    }
    /**
     * Enable an extension.
     *
     * @param entry An entry indicating which extension to enable.
     */
    async enable(entry) {
        if (entry.enabled) {
            throw new Error(`Already enabled: ${entry.name}`);
        }
        await this.performAction('enable', entry);
        await this.refreshInstalled(true);
    }
    /**
     * Disable an extension.
     *
     * @param entry An entry indicating which extension to disable.
     */
    async disable(entry) {
        if (!entry.enabled) {
            throw new Error(`Already disabled: ${entry.name}`);
        }
        await this.performAction('disable', entry);
        await this.refreshInstalled(true);
    }
    /**
     * Refresh installed packages
     *
     * @param force Force refreshing the list of installed packages
     */
    async refreshInstalled(force = false) {
        this.installedError = null;
        this._isLoadingInstalledExtensions = true;
        this.stateChanged.emit();
        try {
            const [extensions] = await Private.requestAPI({
                refresh: force ? 1 : 0
            });
            this._installed = extensions.sort(Private.comparator);
        }
        catch (reason) {
            this.installedError = reason.toString();
        }
        finally {
            this._isLoadingInstalledExtensions = false;
            this.stateChanged.emit();
        }
    }
    /**
     * Search with current query.
     *
     * Sets searchError and totalEntries as appropriate.
     *
     * @returns The extensions matching the current query.
     */
    async search(force = false) {
        var _a, _b;
        if (!this.isDisclaimed) {
            return Promise.reject('Installation warning is not disclaimed.');
        }
        this.searchError = null;
        this._isSearching = true;
        this.stateChanged.emit();
        try {
            const [extensions, links] = await Private.requestAPI({
                query: (_a = this.query) !== null && _a !== void 0 ? _a : '',
                page: this.page,
                per_page: this.pagination,
                refresh: force ? 1 : 0
            });
            const lastURL = links['last'];
            if (lastURL) {
                const lastPage = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.queryStringToObject((_b = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.parse(lastURL).search) !== null && _b !== void 0 ? _b : '')['page'];
                if (lastPage) {
                    this._lastPage = parseInt(lastPage, 10);
                }
            }
            const installedNames = this._installed.map(pkg => pkg.name);
            this._lastSearchResult = extensions
                .filter(pkg => !installedNames.includes(pkg.name))
                .sort(Private.comparator);
        }
        catch (reason) {
            this.searchError = reason.toString();
        }
        finally {
            this._isSearching = false;
            this.stateChanged.emit();
        }
    }
    /**
     * Update the current model.
     *
     * This will query the packages repository, and the notebook server.
     *
     * Emits the `stateChanged` signal on successful completion.
     */
    async update(force = false) {
        if (this.isDisclaimed) {
            // First refresh the installed list - so the search results are correctly filtered
            await this.refreshInstalled(force);
            await this.search();
        }
    }
    /**
     * Send a request to the server to perform an action on an extension.
     *
     * @param action A valid action to perform.
     * @param entry The extension to perform the action on.
     */
    performAction(action, entry) {
        const actionRequest = Private.requestAPI({}, {
            method: 'POST',
            body: JSON.stringify({
                cmd: action,
                extension_name: entry.name
            })
        });
        actionRequest.then(([reply]) => {
            const trans = this.translator.load('jupyterlab');
            if (reply.needs_restart.includes('server')) {
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    title: trans.__('Information'),
                    body: trans.__('You will need to restart JupyterLab to apply the changes.'),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Ok') })]
                });
            }
            else {
                const followUps = [];
                if (reply.needs_restart.includes('frontend')) {
                    followUps.push(
                    // @ts-expect-error isElectron is not a standard attribute
                    window.isElectron
                        ? trans.__('reload JupyterLab')
                        : trans.__('refresh the web page'));
                }
                if (reply.needs_restart.includes('kernel')) {
                    followUps.push(trans.__('install the extension in all kernels and restart them'));
                }
                void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                    title: trans.__('Information'),
                    body: trans.__('You will need to %1 to apply the changes.', followUps.join(trans.__(' and '))),
                    buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({ label: trans.__('Ok') })]
                });
            }
            this.actionError = null;
        }, reason => {
            this.actionError = reason.toString();
        });
        this.addPendingAction(actionRequest);
        return actionRequest.then(([reply]) => reply);
    }
    /**
     * Add a pending action.
     *
     * @param pending A promise that resolves when the action is completed.
     */
    addPendingAction(pending) {
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
}
/**
 * ListModel statics.
 */
(function (ListModel) {
    /**
     * Utility function to check whether an entry can be updated.
     *
     * @param entry The entry to check.
     */
    function entryHasUpdate(entry) {
        if (!entry.installed || !entry.latest_version) {
            return false;
        }
        return semver__WEBPACK_IMPORTED_MODULE_6__.lt(entry.installed_version, entry.latest_version);
    }
    ListModel.entryHasUpdate = entryHasUpdate;
})(ListModel || (ListModel = {}));
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * A comparator function that sorts allowedExtensions orgs to the top.
     */
    function comparator(a, b) {
        if (a.name === b.name) {
            return 0;
        }
        else {
            return a.name > b.name ? 1 : -1;
        }
    }
    Private.comparator = comparator;
    const LINK_PARSER = /<([^>]+)>; rel="([^"]+)",?/g;
    /**
     * Call the API extension
     *
     * @param queryArgs Query arguments
     * @param init Initial values for the request
     * @returns The response body interpreted as JSON and the response link header
     */
    async function requestAPI(queryArgs = {}, init = {}) {
        var _a;
        // Make request to Jupyter API
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, EXTENSION_API_PATH // API Namespace
        );
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
        const link = (_a = response.headers.get('Link')) !== null && _a !== void 0 ? _a : '';
        const links = {};
        let match = null;
        while ((match = LINK_PARSER.exec(link)) !== null) {
            links[match[2]] = match[1];
        }
        return [data, links];
    }
    Private.requestAPI = requestAPI;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/extensionmanager/lib/widget.js":
/*!**************************************************!*\
  !*** ../packages/extensionmanager/lib/widget.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ExtensionsPanel": () => (/* binding */ ExtensionsPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_paginate__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-paginate */ "../node_modules/react-paginate/dist/react-paginate.js");
/* harmony import */ var react_paginate__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_paginate__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./model */ "../packages/extensionmanager/lib/model.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const BADGE_SIZE = 32;
const BADGE_QUERY_SIZE = Math.floor(devicePixelRatio * BADGE_SIZE);
function getExtensionGitHubUser(entry) {
    if (entry.homepage_url &&
        entry.homepage_url.startsWith('https://github.com/')) {
        return entry.homepage_url.split('/')[3];
    }
    else if (entry.repository_url &&
        entry.repository_url.startsWith('https://github.com/')) {
        return entry.repository_url.split('/')[3];
    }
    return null;
}
/**
 * VDOM for visualizing an extension entry.
 */
function ListEntry(props) {
    const { canFetch, entry, supportInstallation, trans } = props;
    const flagClasses = [];
    if (entry.status && ['ok', 'warning', 'error'].indexOf(entry.status) !== -1) {
        flagClasses.push(`jp-extensionmanager-entry-${entry.status}`);
    }
    const githubUser = canFetch ? getExtensionGitHubUser(entry) : null;
    if (!entry.allowed) {
        flagClasses.push(`jp-extensionmanager-entry-should-be-uninstalled`);
    }
    return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("li", { className: `jp-extensionmanager-entry ${flagClasses.join(' ')}`, style: { display: 'flex' } },
        react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { style: { marginRight: '8px' } }, githubUser ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement("img", { src: `https://github.com/${githubUser}.png?size=${BADGE_QUERY_SIZE}`, style: { width: '32px', height: '32px' } })) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { style: { width: `${BADGE_SIZE}px`, height: `${BADGE_SIZE}px` } }))),
        react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-entry-description" },
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-entry-title" },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-entry-name" }, entry.homepage_url ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement("a", { href: entry.homepage_url, target: "_blank", rel: "noopener noreferrer", title: trans.__('%1 extension home page', entry.name) }, entry.name)) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null, entry.name))),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-entry-version" },
                    react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { title: trans.__('Version: %1', entry.installed_version) }, entry.installed_version)),
                entry.installed && !entry.allowed && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ToolbarButtonComponent, { icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.infoIcon, iconLabel: trans.__('%1 extension is not allowed anymore. Please uninstall it immediately or contact your administrator.', entry.name), onClick: () => window.open('https://jupyterlab.readthedocs.io/en/latest/user/extensions.html') })),
                entry.approved && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.jupyterIcon.react, { className: "jp-extensionmanager-is-approved", top: "1px", height: "auto", width: "1em", title: trans.__('This extension is approved by your security team.') }))),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-entry-content" },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-entry-description" }, entry.description),
                props.performAction && (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-entry-buttons" }, entry.installed ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null,
                    supportInstallation && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null,
                        _model__WEBPACK_IMPORTED_MODULE_3__.ListModel.entryHasUpdate(entry) && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { onClick: () => props.performAction('install', entry), title: trans.__('Update "%1" to "%2"', entry.name, entry.latest_version), minimal: true, small: true }, trans.__('Update to %1', entry.latest_version))),
                        react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { onClick: () => props.performAction('uninstall', entry), title: trans.__('Uninstall "%1"', entry.name), minimal: true, small: true }, trans.__('Uninstall')))),
                    entry.enabled ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { onClick: () => props.performAction('disable', entry), title: trans.__('Disable "%1"', entry.name), minimal: true, small: true }, trans.__('Disable'))) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { onClick: () => props.performAction('enable', entry), title: trans.__('Enable "%1"', entry.name), minimal: true, small: true }, trans.__('Enable'))))) : (supportInstallation && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { onClick: () => props.performAction('install', entry), title: trans.__('Install "%1"', entry.name), minimal: true, small: true }, trans.__('Install'))))))))));
}
/**
 * List view widget for extensions
 */
function ListView(props) {
    var _a;
    const { canFetch, performAction, supportInstallation, trans } = props;
    return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-listview-wrapper" },
        props.entries.length > 0 ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement("ul", { className: "jp-extensionmanager-listview" }, props.entries.map(entry => (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ListEntry, { key: entry.name, canFetch: canFetch, entry: entry, performAction: performAction, supportInstallation: supportInstallation, trans: trans }))))) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { key: "message", className: "jp-extensionmanager-listview-message" }, trans.__('No entries'))),
        props.numPages > 1 && (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-pagination" },
            react__WEBPACK_IMPORTED_MODULE_1__.createElement((react_paginate__WEBPACK_IMPORTED_MODULE_2___default()), { previousLabel: '<', nextLabel: '>', breakLabel: "...", breakClassName: 'break', initialPage: ((_a = props.initialPage) !== null && _a !== void 0 ? _a : 1) - 1, pageCount: props.numPages, marginPagesDisplayed: 2, pageRangeDisplayed: 3, onPageChange: (data) => props.onPage(data.selected + 1), activeClassName: 'active' })))));
}
function ErrorMessage(props) {
    return react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-error" }, props.children);
}
class Header extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(model, trans, searchInputRef) {
        super();
        this.model = model;
        this.trans = trans;
        this.searchInputRef = searchInputRef;
        model.stateChanged.connect(this.update, this);
        this.addClass('jp-extensionmanager-header');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-title" },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("span", null, this.trans.__('%1 Manager', this.model.name)),
                this.model.installPath && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.infoIcon.react, { className: "jp-extensionmanager-path", tag: "span", title: this.trans.__('Extension installation path: %1', this.model.installPath) }))),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.FilterBox, { placeholder: this.trans.__('Search'), disabled: !this.model.isDisclaimed, updateFilter: (fn, query) => {
                    this.model.query = query !== null && query !== void 0 ? query : '';
                }, useFuzzyFilter: false, inputRef: this.searchInputRef }),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: `jp-extensionmanager-pending ${this.model.hasPendingActions() ? 'jp-mod-hasPending' : ''}` }),
            this.model.actionError && (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ErrorMessage, null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, this.trans.__('Error when performing an action.')),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null, this.trans.__('Reason given:')),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("pre", null, this.model.actionError)))));
    }
}
class Warning extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(model, trans) {
        super();
        this.model = model;
        this.trans = trans;
        this.addClass('jp-extensionmanager-disclaimer');
        model.stateChanged.connect(this.update, this);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", null,
                this.trans
                    .__(`The JupyterLab development team is excited to have a robust
third-party extension community. However, we do not review
third-party extensions, and some extensions may introduce security
risks or contain malicious code that runs on your machine. Moreover in order
to work, this panel needs to fetch data from web services. Do you agree to
activate this feature?`),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("br", null),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("a", { href: "https://jupyterlab.readthedocs.io/en/latest/privacy_policies.html", target: "_blank", rel: "noreferrer" }, this.trans.__('Please read the privacy policy.'))),
            this.model.isDisclaimed ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { className: "jp-extensionmanager-disclaimer-disable", onClick: (e) => {
                    this.model.isDisclaimed = false;
                }, title: this.trans.__('This will withdraw your consent.') }, this.trans.__('No'))) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { className: "jp-extensionmanager-disclaimer-enable", onClick: () => {
                        this.model.isDisclaimed = true;
                    } }, this.trans.__('Yes')),
                react__WEBPACK_IMPORTED_MODULE_1__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.Button, { className: "jp-extensionmanager-disclaimer-disable", onClick: () => {
                        this.model.isEnabled = false;
                    }, title: this.trans.__('This will disable the extension manager panel; including the listing of installed extension.') }, this.trans.__('No, disable'))))));
    }
}
class InstalledList extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(model, trans) {
        super();
        this.model = model;
        this.trans = trans;
        model.stateChanged.connect(this.update, this);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null, this.model.installedError !== null ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ErrorMessage, null, `Error querying installed extensions${this.model.installedError ? `: ${this.model.installedError}` : '.'}`)) : this.model.isLoadingInstalledExtensions ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-loader" }, this.trans.__('Updating extensions list…'))) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ListView, { canFetch: this.model.isDisclaimed, entries: this.model.installed.filter(pkg => new RegExp(this.model.query.toLowerCase()).test(pkg.name)), numPages: 1, trans: this.trans, onPage: value => {
                /* no-op */
            }, performAction: this.model.isDisclaimed ? this.onAction.bind(this) : null, supportInstallation: this.model.canInstall && this.model.isDisclaimed }))));
    }
    /**
     * Callback handler for when the user wants to perform an action on an extension.
     *
     * @param action The action to perform.
     * @param entry The entry to perform the action on.
     */
    onAction(action, entry) {
        switch (action) {
            case 'install':
                return this.model.install(entry);
            case 'uninstall':
                return this.model.uninstall(entry);
            case 'enable':
                return this.model.enable(entry);
            case 'disable':
                return this.model.disable(entry);
            default:
                throw new Error(`Invalid action: ${action}`);
        }
    }
}
class SearchResult extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(model, trans) {
        super();
        this.model = model;
        this.trans = trans;
        model.stateChanged.connect(this.update, this);
    }
    /**
     * Callback handler for the user changes the page of the search result pagination.
     *
     * @param value The pagination page number.
     */
    onPage(value) {
        this.model.page = value;
    }
    /**
     * Callback handler for when the user wants to perform an action on an extension.
     *
     * @param action The action to perform.
     * @param entry The entry to perform the action on.
     */
    onAction(action, entry) {
        switch (action) {
            case 'install':
                return this.model.install(entry);
            case 'uninstall':
                return this.model.uninstall(entry);
            case 'enable':
                return this.model.enable(entry);
            case 'disable':
                return this.model.disable(entry);
            default:
                throw new Error(`Invalid action: ${action}`);
        }
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null, this.model.searchError !== null ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ErrorMessage, null, `Error searching for extensions${this.model.searchError ? `: ${this.model.searchError}` : '.'}`)) : this.model.isSearching ? (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "jp-extensionmanager-loader" }, this.trans.__('Updating extensions list…'))) : (react__WEBPACK_IMPORTED_MODULE_1__.createElement(ListView, { canFetch: this.model.isDisclaimed, entries: this.model.searchResult, initialPage: this.model.page, numPages: this.model.lastPage, onPage: value => {
                this.onPage(value);
            }, performAction: this.model.isDisclaimed ? this.onAction.bind(this) : null, supportInstallation: this.model.canInstall && this.model.isDisclaimed, trans: this.trans }))));
    }
    update() {
        this.title.label = this.model.query
            ? this.trans.__('Search Results')
            : this.trans.__('Discover');
        super.update();
    }
}
class ExtensionsPanel extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.SidePanel {
    constructor(options) {
        const { model, translator } = options;
        super({ translator });
        this._wasInitialized = false;
        this._wasDisclaimed = true;
        this.model = model;
        this._searchInputRef = react__WEBPACK_IMPORTED_MODULE_1__.createRef();
        this.addClass('jp-extensionmanager-view');
        this.trans = translator.load('jupyterlab');
        this.header.addWidget(new Header(model, this.trans, this._searchInputRef));
        const warning = new Warning(model, this.trans);
        warning.title.label = this.trans.__('Warning');
        this.addWidget(warning);
        const installed = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.PanelWithToolbar();
        installed.addClass('jp-extensionmanager-installedlist');
        installed.title.label = this.trans.__('Installed');
        installed.toolbar.addItem('refresh', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ToolbarButton({
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.refreshIcon,
            onClick: () => {
                model.refreshInstalled(true).catch(reason => {
                    console.error(`Failed to refresh the installed extensions list:\n${reason}`);
                });
            },
            tooltip: this.trans.__('Refresh extensions list')
        }));
        installed.addWidget(new InstalledList(model, this.trans));
        this.addWidget(installed);
        if (this.model.canInstall) {
            const searchResults = new SearchResult(model, this.trans);
            searchResults.addClass('jp-extensionmanager-searchresults');
            this.addWidget(searchResults);
        }
        this._wasDisclaimed = this.model.isDisclaimed;
        if (this.model.isDisclaimed) {
            this.content.collapse(0);
            this.content.layout.setRelativeSizes([0, 1, 1]);
        }
        else {
            // If warning is not disclaimed expand only the warning panel
            this.content.expand(0);
            this.content.collapse(1);
            this.content.collapse(2);
        }
        this.model.stateChanged.connect(this._onStateChanged, this);
    }
    /**
     * Dispose of the widget and its descendant widgets.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.model.stateChanged.disconnect(this._onStateChanged, this);
        super.dispose();
    }
    /**
     * Handle the DOM events for the extension manager search bar.
     *
     * @param event - The DOM event sent to the extension manager search bar.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the search bar's DOM node.
     * It should not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'focus':
            case 'blur':
                this._toggleFocused();
                break;
            default:
                break;
        }
    }
    /**
     * A message handler invoked on a `'before-attach'` message.
     */
    onBeforeAttach(msg) {
        this.node.addEventListener('focus', this, true);
        this.node.addEventListener('blur', this, true);
        super.onBeforeAttach(msg);
    }
    onBeforeShow(msg) {
        if (!this._wasInitialized) {
            this._wasInitialized = true;
            this.model.refreshInstalled().catch(reason => {
                console.log(`Failed to refresh installed extension list:\n${reason}`);
            });
        }
    }
    /**
     * A message handler invoked on an `'after-detach'` message.
     */
    onAfterDetach(msg) {
        super.onAfterDetach(msg);
        this.node.removeEventListener('focus', this, true);
        this.node.removeEventListener('blur', this, true);
    }
    /**
     * A message handler invoked on an `'activate-request'` message.
     */
    onActivateRequest(msg) {
        if (this.isAttached) {
            const input = this._searchInputRef.current;
            if (input) {
                input.focus();
                input.select();
            }
        }
        super.onActivateRequest(msg);
    }
    _onStateChanged() {
        if (!this._wasDisclaimed && this.model.isDisclaimed) {
            this.content.collapse(0);
            this.content.expand(1);
            this.content.expand(2);
        }
        this._wasDisclaimed = this.model.isDisclaimed;
    }
    /**
     * Toggle the focused modifier based on the input node focus state.
     */
    _toggleFocused() {
        const focused = document.activeElement === this._searchInputRef.current;
        this.toggleClass('lm-mod-focused', focused);
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZXh0ZW5zaW9ubWFuYWdlcl9saWJfaW5kZXhfanMuYTdhY2NkNTIxMmM4Y2UxODBmZDcuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFRDtBQUNZO0FBQ3ZDO0FBRS9COzs7OztHQUtHO0FBQ0ksU0FBUyxrQkFBa0IsQ0FDaEMsSUFBWSxFQUNaLFlBQXFCLEVBQ3JCLFVBQXdCO0lBRXhCLFVBQVUsR0FBRyxVQUFVLElBQUksbUVBQWMsQ0FBQztJQUMxQyxNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQzVDLE1BQU0sT0FBTyxHQUFHLEVBQUUsQ0FBQztJQUNuQixPQUFPLENBQUMsSUFBSSxDQUFDLDREQUFJLEtBQUssQ0FBQyxFQUFFLENBQUMsaUNBQWlDLElBQUksSUFBSSxDQUFDLENBQUssQ0FBQyxDQUFDO0lBQzNFLElBQUksWUFBWSxFQUFFO1FBQ2hCLE9BQU8sQ0FBQyxJQUFJLENBQ1Y7WUFDRSwyREFBTSxTQUFTLEVBQUMsc0NBQXNDLElBQ25ELEtBQUssQ0FBQyxFQUFFLENBQUMsZ0JBQWdCLENBQUMsQ0FDdEIsQ0FDTCxFQUNKLDhEQUFNLFlBQVksQ0FBQyxJQUFJLEVBQUUsQ0FBTyxDQUNqQyxDQUFDO0tBQ0g7SUFDRCxNQUFNLElBQUksR0FBRywwREFBSyxTQUFTLEVBQUMsNEJBQTRCLElBQUUsT0FBTyxDQUFPLENBQUM7SUFDekUsS0FBSyxnRUFBVSxDQUFDO1FBQ2QsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsOEJBQThCLENBQUM7UUFDL0MsSUFBSTtRQUNKLE9BQU8sRUFBRSxDQUFDLG1FQUFpQixDQUFDLEVBQUUsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsSUFBSSxDQUFDLEVBQUUsQ0FBQyxDQUFDO0tBQ3hELENBQUMsQ0FBQztBQUNMLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ3RDRCwwQ0FB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U0FDRjtRQUNELEtBQUssQ0FBQyxpQkFBaUIsQ0FBQyxHQUFHLENBQUMsQ0FBQztJQUMvQixDQUFDO0lBRU8sZUFBZTtRQUNyQixJQUFJLENBQUMsSUFBSSxDQUFDLGNBQWMsSUFBSSxJQUFJLENBQUMsS0FBSyxDQUFDLFlBQVksRUFBRTtZQUNsRCxJQUFJLENBQUMsT0FBMEIsQ0FBQyxRQUFRLENBQUMsQ0FBQyxDQUFDLENBQUM7WUFDNUMsSUFBSSxDQUFDLE9BQTBCLENBQUMsTUFBTSxDQUFDLENBQUMsQ0FBQyxDQUFDO1lBQzFDLElBQUksQ0FBQyxPQUEwQixDQUFDLE1BQU0sQ0FBQyxDQUFDLENBQUMsQ0FBQztTQUM1QztRQUNELElBQUksQ0FBQyxjQUFjLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxZQUFZLENBQUM7SUFDaEQsQ0FBQztJQUVEOztPQUVHO0lBQ0ssY0FBYztRQUNwQixNQUFNLE9BQU8sR0FBRyxRQUFRLENBQUMsYUFBYSxLQUFLLElBQUksQ0FBQyxlQUFlLENBQUMsT0FBTyxDQUFDO1FBQ3hFLElBQUksQ0FBQyxXQUFXLENBQUMsZ0JBQWdCLEVBQUUsT0FBTyxDQUFDLENBQUM7SUFDOUMsQ0FBQztDQU9GIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2V4dGVuc2lvbm1hbmFnZXIvc3JjL2RpYWxvZy50c3giLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2V4dGVuc2lvbm1hbmFnZXIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9leHRlbnNpb25tYW5hZ2VyL3NyYy9tb2RlbC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZXh0ZW5zaW9ubWFuYWdlci9zcmMvd2lkZ2V0LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IERpYWxvZywgc2hvd0RpYWxvZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcblxuLyoqXG4gKiBTaG93IGEgZGlhbG9nIGJveCByZXBvcnRpbmcgYW4gZXJyb3IgZHVyaW5nIGluc3RhbGxhdGlvbiBvZiBhbiBleHRlbnNpb24uXG4gKlxuICogQHBhcmFtIG5hbWUgVGhlIG5hbWUgb2YgdGhlIGV4dGVuc2lvblxuICogQHBhcmFtIGVycm9yTWVzc2FnZSBBbnkgZXJyb3IgbWVzc2FnZSBnaXZpbmcgZGV0YWlscyBhYm91dCB0aGUgZmFpbHVyZS5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHJlcG9ydEluc3RhbGxFcnJvcihcbiAgbmFtZTogc3RyaW5nLFxuICBlcnJvck1lc3NhZ2U/OiBzdHJpbmcsXG4gIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuKTogdm9pZCB7XG4gIHRyYW5zbGF0b3IgPSB0cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBlbnRyaWVzID0gW107XG4gIGVudHJpZXMucHVzaCg8cD57dHJhbnMuX18oYEFuIGVycm9yIG9jY3VycmVkIGluc3RhbGxpbmcgXCIke25hbWV9XCIuYCl9PC9wPik7XG4gIGlmIChlcnJvck1lc3NhZ2UpIHtcbiAgICBlbnRyaWVzLnB1c2goXG4gICAgICA8cD5cbiAgICAgICAgPHNwYW4gY2xhc3NOYW1lPVwianAtZXh0ZW5zaW9ubWFuYWdlci1kaWFsb2ctc3ViaGVhZGVyXCI+XG4gICAgICAgICAge3RyYW5zLl9fKCdFcnJvciBtZXNzYWdlOicpfVxuICAgICAgICA8L3NwYW4+XG4gICAgICA8L3A+LFxuICAgICAgPHByZT57ZXJyb3JNZXNzYWdlLnRyaW0oKX08L3ByZT5cbiAgICApO1xuICB9XG4gIGNvbnN0IGJvZHkgPSA8ZGl2IGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItZGlhbG9nXCI+e2VudHJpZXN9PC9kaXY+O1xuICB2b2lkIHNob3dEaWFsb2coe1xuICAgIHRpdGxlOiB0cmFucy5fXygnRXh0ZW5zaW9uIEluc3RhbGxhdGlvbiBFcnJvcicpLFxuICAgIGJvZHksXG4gICAgYnV0dG9uczogW0RpYWxvZy53YXJuQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdPaycpIH0pXVxuICB9KTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIGV4dGVuc2lvbm1hbmFnZXJcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL21vZGVsJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuLyogZ2xvYmFsIFJlcXVlc3RJbml0ICovXG5cbmltcG9ydCB7IERpYWxvZywgc2hvd0RpYWxvZyB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFBhZ2VDb25maWcsIFVSTEV4dCB9IGZyb20gJ0BqdXB5dGVybGFiL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBTZXJ2ZXJDb25uZWN0aW9uLCBTZXJ2aWNlTWFuYWdlciB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFZEb21Nb2RlbCB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgRGVib3VuY2VyIH0gZnJvbSAnQGx1bWluby9wb2xsaW5nJztcbmltcG9ydCAqIGFzIHNlbXZlciBmcm9tICdzZW12ZXInO1xuaW1wb3J0IHsgcmVwb3J0SW5zdGFsbEVycm9yIH0gZnJvbSAnLi9kaWFsb2cnO1xuXG4vKipcbiAqIEluZm9ybWF0aW9uIGFib3V0IGFuIGV4dGVuc2lvbi5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJRW50cnkge1xuICAvKipcbiAgICogVGhlIG5hbWUgb2YgdGhlIGV4dGVuc2lvbi5cbiAgICovXG4gIG5hbWU6IHN0cmluZztcblxuICAvKipcbiAgICogQSBzaG9ydCBkZXNjcmlwdGlvbiBvZiB0aGUgZXh0ZW5zaW9uLlxuICAgKi9cbiAgZGVzY3JpcHRpb246IHN0cmluZztcblxuICAvKipcbiAgICogQSByZXByZXNlbnRhdGl2ZSBsaW5rIG9mIHRoZSBwYWNrYWdlLlxuICAgKi9cbiAgaG9tZXBhZ2VfdXJsOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGV4dGVuc2lvbiBpcyBjdXJyZW50bHkgaW5zdGFsbGVkLlxuICAgKi9cbiAgaW5zdGFsbGVkPzogYm9vbGVhbiB8IG51bGw7XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGV4dGVuc2lvbiBpcyBhbGxvd2VkIG9yIG5vdC5cbiAgICovXG4gIGFsbG93ZWQ6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGV4dGVuc2lvbiBpcyBhcHByb3ZlZCBieSB0aGUgc3lzdGVtIGFkbWluaXN0cmF0b3JzLlxuICAgKi9cbiAgYXBwcm92ZWQ6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGV4dGVuc2lvbiBpcyBjdXJyZW50bHkgZW5hYmxlZC5cbiAgICovXG4gIGVuYWJsZWQ6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIFRoZSBsYXRlc3QgdmVyc2lvbiBvZiB0aGUgZXh0ZW5zaW9uLlxuICAgKi9cbiAgbGF0ZXN0X3ZlcnNpb246IHN0cmluZztcblxuICAvKipcbiAgICogVGhlIGluc3RhbGxlZCB2ZXJzaW9uIG9mIHRoZSBleHRlbnNpb24uXG4gICAqL1xuICBpbnN0YWxsZWRfdmVyc2lvbjogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBBIGZsYWcgaW5kaWNhdGluZyB0aGUgc3RhdHVzIG9mIGFuIGluc3RhbGxlZCBleHRlbnNpb24uXG4gICAqL1xuICBzdGF0dXM6ICdvaycgfCAnd2FybmluZycgfCAnZXJyb3InIHwgJ2RlcHJlY2F0ZWQnIHwgbnVsbDtcblxuICAvKipcbiAgICogVGhlIHBhY2thZ2UgdHlwZSAocHJlYnVpbHQgb3Igc291cmNlKS5cbiAgICovXG4gIHBrZ190eXBlOiAncHJlYnVpbHQnIHwgJ3NvdXJjZSc7XG5cbiAgLyoqXG4gICAqIFRoZSBpbmZvcm1hdGlvbiBhYm91dCBleHRlbnNpb24gaW5zdGFsbGF0aW9uLlxuICAgKi9cbiAgaW5zdGFsbD86IElJbnN0YWxsIHwgbnVsbDtcblxuICAvKipcbiAgICogUGFja2FnZSBhdXRob3IuXG4gICAqL1xuICBhdXRob3I/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFBhY2thZ2UgbGljZW5zZS5cbiAgICovXG4gIGxpY2Vuc2U/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFVSTCB0byB0aGUgcGFja2FnZSBidWcgdHJhY2tlci5cbiAgICovXG4gIGJ1Z190cmFja2VyX3VybD86IHN0cmluZztcblxuICAvKipcbiAgICogVVJMIHRvIHRoZSBwYWNrYWdlIGRvY3VtZW50YXRpb24uXG4gICAqL1xuICBkb2N1bWVudGF0aW9uX3VybD86IHN0cmluZztcblxuICAvKipcbiAgICogVVJMIHRvIHRoZSBwYWNrYWdlIFVSTCBpbiB0aGUgcGFja2FnZXIgd2Vic2l0ZS5cbiAgICovXG4gIHBhY2thZ2VfbWFuYWdlcl91cmw/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFVSTCB0byB0aGUgcGFja2FnZSBjb2RlIHNvdXJjZS5cbiAgICovXG4gIHJlcG9zaXRvcnlfdXJsPzogc3RyaW5nO1xufVxuXG4vKipcbiAqIEluZm9ybWF0aW9uIGFib3V0IGV4dGVuc2lvbiBpbnN0YWxsYXRpb24uXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUluc3RhbGwge1xuICAvKipcbiAgICogVGhlIHVzZWQgcGFja2FnZSBtYW5hZ2VyIChlLmcuIHBpcCwgY29uZGEuLi4pXG4gICAqL1xuICBwYWNrYWdlTWFuYWdlcjogc3RyaW5nIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBUaGUgcGFja2FnZSBuYW1lIGFzIGtub3duIGJ5IHRoZSBwYWNrYWdlIG1hbmFnZXIuXG4gICAqL1xuICBwYWNrYWdlTmFtZTogc3RyaW5nIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBUaGUgdW5pbnN0YWxsYXRpb24gaW5zdHJ1Y3Rpb25zIGFzIGEgY29tcHJlaGVuc2l2ZVxuICAgKiB0ZXh0IGZvciB0aGUgZW5kIHVzZXIuXG4gICAqL1xuICB1bmluc3RhbGxJbnN0cnVjdGlvbnM6IHN0cmluZyB8IHVuZGVmaW5lZDtcbn1cblxuLyoqXG4gKiBBbiBvYmplY3QgcmVwcmVzZW50aW5nIGEgc2VydmVyIHJlcGx5IHRvIHBlcmZvcm1pbmcgYW4gYWN0aW9uLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElBY3Rpb25SZXBseSB7XG4gIC8qKlxuICAgKiBUaGUgc3RhdHVzIGNhdGVnb3J5IG9mIHRoZSByZXBseS5cbiAgICovXG4gIHN0YXR1czogJ29rJyB8ICd3YXJuaW5nJyB8ICdlcnJvcicgfCBudWxsO1xuXG4gIC8qKlxuICAgKiBBbiBvcHRpb25hbCBtZXNzYWdlIHdoZW4gdGhlIHN0YXR1cyBpcyBub3QgJ29rJy5cbiAgICovXG4gIG1lc3NhZ2U/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIEZvbGxvdy11cCByZXN0YXJ0IG5lZWRlZCBieSB0aGUgYWN0aW9uXG4gICAqL1xuICBuZWVkc19yZXN0YXJ0OiAoJ2Zyb250ZW5kJyB8ICdrZXJuZWwnIHwgJ3NlcnZlcicpW107XG59XG5cbi8qKlxuICogRXh0ZW5zaW9uIG1hbmFnZXIgbWV0YWRhdGFcbiAqL1xuaW50ZXJmYWNlIElFeHRlbnNpb25NYW5hZ2VyTWV0YWRhdGEge1xuICAvKipcbiAgICogRXh0ZW5zaW9uIG1hbmFnZXIgbmFtZS5cbiAgICovXG4gIG5hbWU6IHN0cmluZztcbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGV4dGVuc2lvbiBtYW5hZ2VyIGNhbiB1bi0vaW5zdGFsbCBleHRlbnNpb25zLlxuICAgKi9cbiAgY2FuX2luc3RhbGw6IGJvb2xlYW47XG4gIC8qKlxuICAgKiBFeHRlbnNpb25zIGluc3RhbGxhdGlvbiBwYXRoLlxuICAgKi9cbiAgaW5zdGFsbF9wYXRoOiBzdHJpbmcgfCBudWxsO1xufVxuXG4vKipcbiAqIFRoZSBzZXJ2ZXIgQVBJIHBhdGggZm9yIHF1ZXJ5aW5nL21vZGlmeWluZyBpbnN0YWxsZWQgZXh0ZW5zaW9ucy5cbiAqL1xuY29uc3QgRVhURU5TSU9OX0FQSV9QQVRIID0gJ2xhYi9hcGkvZXh0ZW5zaW9ucyc7XG5cbi8qKlxuICogRXh0ZW5zaW9uIGFjdGlvbnMgdGhhdCB0aGUgc2VydmVyIEFQSSBhY2NlcHRzXG4gKi9cbmV4cG9ydCB0eXBlIEFjdGlvbiA9ICdpbnN0YWxsJyB8ICd1bmluc3RhbGwnIHwgJ2VuYWJsZScgfCAnZGlzYWJsZSc7XG5cbi8qKlxuICogTW9kZWwgZm9yIGFuIGV4dGVuc2lvbiBsaXN0LlxuICovXG5leHBvcnQgY2xhc3MgTGlzdE1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIHtcbiAgY29uc3RydWN0b3IoXG4gICAgc2VydmljZU1hbmFnZXI6IFNlcnZpY2VNYW5hZ2VyLklNYW5hZ2VyLFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApIHtcbiAgICBzdXBlcigpO1xuXG4gICAgY29uc3QgbWV0YWRhdGEgPSBKU09OLnBhcnNlKFxuICAgICAgLy8gVGhlIHBhZ2UgY29uZmlnIG9wdGlvbiBtYXkgbm90IGJlIGRlZmluZWQ7IGUuZy4gaW4gdGhlIGZlZGVyYXRlZCBleGFtcGxlXG4gICAgICBQYWdlQ29uZmlnLmdldE9wdGlvbignZXh0ZW5zaW9uTWFuYWdlcicpIHx8ICd7fSdcbiAgICApIGFzIElFeHRlbnNpb25NYW5hZ2VyTWV0YWRhdGE7XG5cbiAgICB0aGlzLm5hbWUgPSBtZXRhZGF0YS5uYW1lO1xuICAgIHRoaXMuY2FuSW5zdGFsbCA9IG1ldGFkYXRhLmNhbl9pbnN0YWxsO1xuICAgIHRoaXMuaW5zdGFsbFBhdGggPSBtZXRhZGF0YS5pbnN0YWxsX3BhdGg7XG4gICAgdGhpcy50cmFuc2xhdG9yID0gdHJhbnNsYXRvciB8fCBudWxsVHJhbnNsYXRvcjtcbiAgICB0aGlzLl9pbnN0YWxsZWQgPSBbXTtcbiAgICB0aGlzLl9sYXN0U2VhcmNoUmVzdWx0ID0gW107XG4gICAgdGhpcy5zZXJ2aWNlTWFuYWdlciA9IHNlcnZpY2VNYW5hZ2VyO1xuICAgIHRoaXMuX2RlYm91bmNlZFNlYXJjaCA9IG5ldyBEZWJvdW5jZXIodGhpcy5zZWFyY2guYmluZCh0aGlzKSwgMTAwMCk7XG4gIH1cblxuICAvKipcbiAgICogRXh0ZW5zaW9uIG1hbmFnZXIgbmFtZS5cbiAgICovXG4gIHJlYWRvbmx5IG5hbWU6IHN0cmluZztcblxuICAvKipcbiAgICogV2hldGhlciB0aGUgZXh0ZW5zaW9uIG1hbmFnZXIgc3VwcG9ydCBpbnN0YWxsYXRpb24gbWV0aG9kcyBvciBub3QuXG4gICAqL1xuICByZWFkb25seSBjYW5JbnN0YWxsOiBib29sZWFuO1xuXG4gIC8qKlxuICAgKiBFeHRlbnNpb25zIGluc3RhbGxhdGlvbiBwYXRoLlxuICAgKi9cbiAgaW5zdGFsbFBhdGg6IHN0cmluZyB8IG51bGw7XG5cbiAgLyoqXG4gICAqIEEgcmVhZG9ubHkgYXJyYXkgb2YgdGhlIGluc3RhbGxlZCBleHRlbnNpb25zLlxuICAgKi9cbiAgZ2V0IGluc3RhbGxlZCgpOiBSZWFkb25seUFycmF5PElFbnRyeT4ge1xuICAgIHJldHVybiB0aGlzLl9pbnN0YWxsZWQ7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgd2FybmluZyBpcyBkaXNjbGFpbWVkIG9yIG5vdC5cbiAgICovXG4gIGdldCBpc0Rpc2NsYWltZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzY2xhaW1lZDtcbiAgfVxuICBzZXQgaXNEaXNjbGFpbWVkKHY6IGJvb2xlYW4pIHtcbiAgICBpZiAodiAhPT0gdGhpcy5faXNEaXNjbGFpbWVkKSB7XG4gICAgICB0aGlzLl9pc0Rpc2NsYWltZWQgPSB2O1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgICAgdm9pZCB0aGlzLl9kZWJvdW5jZWRTZWFyY2guaW52b2tlKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGV4dGVuc2lvbiBtYW5hZ2VyIGlzIGVuYWJsZWQgb3Igbm90LlxuICAgKi9cbiAgZ2V0IGlzRW5hYmxlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNFbmFibGVkO1xuICB9XG4gIHNldCBpc0VuYWJsZWQodjogYm9vbGVhbikge1xuICAgIGlmICh2ICE9PSB0aGlzLl9pc0VuYWJsZWQpIHtcbiAgICAgIHRoaXMuX2lzRW5hYmxlZCA9IHY7XG4gICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KCk7XG4gICAgfVxuICB9XG5cbiAgZ2V0IGlzTG9hZGluZ0luc3RhbGxlZEV4dGVuc2lvbnMoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzTG9hZGluZ0luc3RhbGxlZEV4dGVuc2lvbnM7XG4gIH1cblxuICBnZXQgaXNTZWFyY2hpbmcoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzU2VhcmNoaW5nO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgcmVhZG9ubHkgYXJyYXkgY29udGFpbmluZyB0aGUgbGF0ZXN0IHNlYXJjaCByZXN1bHRcbiAgICovXG4gIGdldCBzZWFyY2hSZXN1bHQoKTogUmVhZG9ubHlBcnJheTxJRW50cnk+IHtcbiAgICByZXR1cm4gdGhpcy5fbGFzdFNlYXJjaFJlc3VsdDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgc2VhcmNoIHF1ZXJ5LlxuICAgKlxuICAgKiBTZXR0aW5nIGl0cyB2YWx1ZSB0cmlnZ2VycyBhIG5ldyBzZWFyY2guXG4gICAqL1xuICBnZXQgcXVlcnkoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fcXVlcnk7XG4gIH1cbiAgc2V0IHF1ZXJ5KHZhbHVlOiBzdHJpbmcpIHtcbiAgICBpZiAodGhpcy5fcXVlcnkgIT09IHZhbHVlKSB7XG4gICAgICB0aGlzLl9xdWVyeSA9IHZhbHVlO1xuICAgICAgdGhpcy5fcGFnZSA9IDE7XG4gICAgICB2b2lkIHRoaXMuX2RlYm91bmNlZFNlYXJjaC5pbnZva2UoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIGN1cnJlbnQgc2VhcmNoIHBhZ2UuXG4gICAqXG4gICAqIFNldHRpbmcgaXRzIHZhbHVlIHRyaWdnZXJzIGEgbmV3IHNlYXJjaC5cbiAgICpcbiAgICogIyMjIE5vdGVcbiAgICogRmlyc3QgcGFnZSBpcyAxLlxuICAgKi9cbiAgZ2V0IHBhZ2UoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5fcGFnZTtcbiAgfVxuICBzZXQgcGFnZSh2YWx1ZTogbnVtYmVyKSB7XG4gICAgaWYgKHRoaXMuX3BhZ2UgIT09IHZhbHVlKSB7XG4gICAgICB0aGlzLl9wYWdlID0gdmFsdWU7XG4gICAgICB2b2lkIHRoaXMuX2RlYm91bmNlZFNlYXJjaC5pbnZva2UoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNlYXJjaCBwYWdpbmF0aW9uLlxuICAgKlxuICAgKiBTZXR0aW5nIGl0cyB2YWx1ZSB0cmlnZ2VycyBhIG5ldyBzZWFyY2guXG4gICAqL1xuICBnZXQgcGFnaW5hdGlvbigpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLl9wYWdpbmF0aW9uO1xuICB9XG4gIHNldCBwYWdpbmF0aW9uKHZhbHVlOiBudW1iZXIpIHtcbiAgICBpZiAodGhpcy5fcGFnaW5hdGlvbiAhPT0gdmFsdWUpIHtcbiAgICAgIHRoaXMuX3BhZ2luYXRpb24gPSB2YWx1ZTtcbiAgICAgIHZvaWQgdGhpcy5fZGVib3VuY2VkU2VhcmNoLmludm9rZSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbGFzdCBwYWdlIG9mIHJlc3VsdHMgaW4gdGhlIGN1cnJlbnQgc2VhcmNoLlxuICAgKi9cbiAgZ2V0IGxhc3RQYWdlKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX2xhc3RQYWdlO1xuICB9XG5cbiAgLyoqXG4gICAqIERpc3Bvc2UgdGhlIGV4dGVuc2lvbnMgbGlzdCBtb2RlbC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9kZWJvdW5jZWRTZWFyY2guZGlzcG9zZSgpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZXJlIGFyZSBjdXJyZW50bHkgYW55IGFjdGlvbnMgcGVuZGluZy5cbiAgICovXG4gIGhhc1BlbmRpbmdBY3Rpb25zKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9wZW5kaW5nQWN0aW9ucy5sZW5ndGggPiAwO1xuICB9XG5cbiAgLyoqXG4gICAqIEluc3RhbGwgYW4gZXh0ZW5zaW9uLlxuICAgKlxuICAgKiBAcGFyYW0gZW50cnkgQW4gZW50cnkgaW5kaWNhdGluZyB3aGljaCBleHRlbnNpb24gdG8gaW5zdGFsbC5cbiAgICovXG4gIGFzeW5jIGluc3RhbGwoZW50cnk6IElFbnRyeSk6IFByb21pc2U8dm9pZD4ge1xuICAgIGF3YWl0IHRoaXMucGVyZm9ybUFjdGlvbignaW5zdGFsbCcsIGVudHJ5KS50aGVuKGRhdGEgPT4ge1xuICAgICAgaWYgKGRhdGEuc3RhdHVzICE9PSAnb2snKSB7XG4gICAgICAgIHJlcG9ydEluc3RhbGxFcnJvcihlbnRyeS5uYW1lLCBkYXRhLm1lc3NhZ2UsIHRoaXMudHJhbnNsYXRvcik7XG4gICAgICB9XG4gICAgICByZXR1cm4gdGhpcy51cGRhdGUodHJ1ZSk7XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogVW5pbnN0YWxsIGFuIGV4dGVuc2lvbi5cbiAgICpcbiAgICogQHBhcmFtIGVudHJ5IEFuIGVudHJ5IGluZGljYXRpbmcgd2hpY2ggZXh0ZW5zaW9uIHRvIHVuaW5zdGFsbC5cbiAgICovXG4gIGFzeW5jIHVuaW5zdGFsbChlbnRyeTogSUVudHJ5KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKCFlbnRyeS5pbnN0YWxsZWQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgTm90IGluc3RhbGxlZCwgY2Fubm90IHVuaW5zdGFsbDogJHtlbnRyeS5uYW1lfWApO1xuICAgIH1cbiAgICBhd2FpdCB0aGlzLnBlcmZvcm1BY3Rpb24oJ3VuaW5zdGFsbCcsIGVudHJ5KTtcbiAgICByZXR1cm4gdGhpcy51cGRhdGUodHJ1ZSk7XG4gIH1cblxuICAvKipcbiAgICogRW5hYmxlIGFuIGV4dGVuc2lvbi5cbiAgICpcbiAgICogQHBhcmFtIGVudHJ5IEFuIGVudHJ5IGluZGljYXRpbmcgd2hpY2ggZXh0ZW5zaW9uIHRvIGVuYWJsZS5cbiAgICovXG4gIGFzeW5jIGVuYWJsZShlbnRyeTogSUVudHJ5KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKGVudHJ5LmVuYWJsZWQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgQWxyZWFkeSBlbmFibGVkOiAke2VudHJ5Lm5hbWV9YCk7XG4gICAgfVxuICAgIGF3YWl0IHRoaXMucGVyZm9ybUFjdGlvbignZW5hYmxlJywgZW50cnkpO1xuICAgIGF3YWl0IHRoaXMucmVmcmVzaEluc3RhbGxlZCh0cnVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNhYmxlIGFuIGV4dGVuc2lvbi5cbiAgICpcbiAgICogQHBhcmFtIGVudHJ5IEFuIGVudHJ5IGluZGljYXRpbmcgd2hpY2ggZXh0ZW5zaW9uIHRvIGRpc2FibGUuXG4gICAqL1xuICBhc3luYyBkaXNhYmxlKGVudHJ5OiBJRW50cnkpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBpZiAoIWVudHJ5LmVuYWJsZWQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgQWxyZWFkeSBkaXNhYmxlZDogJHtlbnRyeS5uYW1lfWApO1xuICAgIH1cbiAgICBhd2FpdCB0aGlzLnBlcmZvcm1BY3Rpb24oJ2Rpc2FibGUnLCBlbnRyeSk7XG4gICAgYXdhaXQgdGhpcy5yZWZyZXNoSW5zdGFsbGVkKHRydWUpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlZnJlc2ggaW5zdGFsbGVkIHBhY2thZ2VzXG4gICAqXG4gICAqIEBwYXJhbSBmb3JjZSBGb3JjZSByZWZyZXNoaW5nIHRoZSBsaXN0IG9mIGluc3RhbGxlZCBwYWNrYWdlc1xuICAgKi9cbiAgYXN5bmMgcmVmcmVzaEluc3RhbGxlZChmb3JjZSA9IGZhbHNlKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgdGhpcy5pbnN0YWxsZWRFcnJvciA9IG51bGw7XG4gICAgdGhpcy5faXNMb2FkaW5nSW5zdGFsbGVkRXh0ZW5zaW9ucyA9IHRydWU7XG4gICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgIHRyeSB7XG4gICAgICBjb25zdCBbZXh0ZW5zaW9uc10gPSBhd2FpdCBQcml2YXRlLnJlcXVlc3RBUEk8SUVudHJ5W10+KHtcbiAgICAgICAgcmVmcmVzaDogZm9yY2UgPyAxIDogMFxuICAgICAgfSk7XG4gICAgICB0aGlzLl9pbnN0YWxsZWQgPSBleHRlbnNpb25zLnNvcnQoUHJpdmF0ZS5jb21wYXJhdG9yKTtcbiAgICB9IGNhdGNoIChyZWFzb24pIHtcbiAgICAgIHRoaXMuaW5zdGFsbGVkRXJyb3IgPSByZWFzb24udG9TdHJpbmcoKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdGhpcy5faXNMb2FkaW5nSW5zdGFsbGVkRXh0ZW5zaW9ucyA9IGZhbHNlO1xuICAgICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBTZWFyY2ggd2l0aCBjdXJyZW50IHF1ZXJ5LlxuICAgKlxuICAgKiBTZXRzIHNlYXJjaEVycm9yIGFuZCB0b3RhbEVudHJpZXMgYXMgYXBwcm9wcmlhdGUuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBleHRlbnNpb25zIG1hdGNoaW5nIHRoZSBjdXJyZW50IHF1ZXJ5LlxuICAgKi9cbiAgcHJvdGVjdGVkIGFzeW5jIHNlYXJjaChmb3JjZSA9IGZhbHNlKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKCF0aGlzLmlzRGlzY2xhaW1lZCkge1xuICAgICAgcmV0dXJuIFByb21pc2UucmVqZWN0KCdJbnN0YWxsYXRpb24gd2FybmluZyBpcyBub3QgZGlzY2xhaW1lZC4nKTtcbiAgICB9XG5cbiAgICB0aGlzLnNlYXJjaEVycm9yID0gbnVsbDtcbiAgICB0aGlzLl9pc1NlYXJjaGluZyA9IHRydWU7XG4gICAgdGhpcy5zdGF0ZUNoYW5nZWQuZW1pdCgpO1xuICAgIHRyeSB7XG4gICAgICBjb25zdCBbZXh0ZW5zaW9ucywgbGlua3NdID0gYXdhaXQgUHJpdmF0ZS5yZXF1ZXN0QVBJPElFbnRyeVtdPih7XG4gICAgICAgIHF1ZXJ5OiB0aGlzLnF1ZXJ5ID8/ICcnLFxuICAgICAgICBwYWdlOiB0aGlzLnBhZ2UsXG4gICAgICAgIHBlcl9wYWdlOiB0aGlzLnBhZ2luYXRpb24sXG4gICAgICAgIHJlZnJlc2g6IGZvcmNlID8gMSA6IDBcbiAgICAgIH0pO1xuXG4gICAgICBjb25zdCBsYXN0VVJMID0gbGlua3NbJ2xhc3QnXTtcbiAgICAgIGlmIChsYXN0VVJMKSB7XG4gICAgICAgIGNvbnN0IGxhc3RQYWdlID0gVVJMRXh0LnF1ZXJ5U3RyaW5nVG9PYmplY3QoXG4gICAgICAgICAgVVJMRXh0LnBhcnNlKGxhc3RVUkwpLnNlYXJjaCA/PyAnJ1xuICAgICAgICApWydwYWdlJ107XG5cbiAgICAgICAgaWYgKGxhc3RQYWdlKSB7XG4gICAgICAgICAgdGhpcy5fbGFzdFBhZ2UgPSBwYXJzZUludChsYXN0UGFnZSwgMTApO1xuICAgICAgICB9XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IGluc3RhbGxlZE5hbWVzID0gdGhpcy5faW5zdGFsbGVkLm1hcChwa2cgPT4gcGtnLm5hbWUpO1xuICAgICAgdGhpcy5fbGFzdFNlYXJjaFJlc3VsdCA9IGV4dGVuc2lvbnNcbiAgICAgICAgLmZpbHRlcihwa2cgPT4gIWluc3RhbGxlZE5hbWVzLmluY2x1ZGVzKHBrZy5uYW1lKSlcbiAgICAgICAgLnNvcnQoUHJpdmF0ZS5jb21wYXJhdG9yKTtcbiAgICB9IGNhdGNoIChyZWFzb24pIHtcbiAgICAgIHRoaXMuc2VhcmNoRXJyb3IgPSByZWFzb24udG9TdHJpbmcoKTtcbiAgICB9IGZpbmFsbHkge1xuICAgICAgdGhpcy5faXNTZWFyY2hpbmcgPSBmYWxzZTtcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQoKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVXBkYXRlIHRoZSBjdXJyZW50IG1vZGVsLlxuICAgKlxuICAgKiBUaGlzIHdpbGwgcXVlcnkgdGhlIHBhY2thZ2VzIHJlcG9zaXRvcnksIGFuZCB0aGUgbm90ZWJvb2sgc2VydmVyLlxuICAgKlxuICAgKiBFbWl0cyB0aGUgYHN0YXRlQ2hhbmdlZGAgc2lnbmFsIG9uIHN1Y2Nlc3NmdWwgY29tcGxldGlvbi5cbiAgICovXG4gIHByb3RlY3RlZCBhc3luYyB1cGRhdGUoZm9yY2UgPSBmYWxzZSk6IFByb21pc2U8dm9pZD4ge1xuICAgIGlmICh0aGlzLmlzRGlzY2xhaW1lZCkge1xuICAgICAgLy8gRmlyc3QgcmVmcmVzaCB0aGUgaW5zdGFsbGVkIGxpc3QgLSBzbyB0aGUgc2VhcmNoIHJlc3VsdHMgYXJlIGNvcnJlY3RseSBmaWx0ZXJlZFxuICAgICAgYXdhaXQgdGhpcy5yZWZyZXNoSW5zdGFsbGVkKGZvcmNlKTtcbiAgICAgIGF3YWl0IHRoaXMuc2VhcmNoKCk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFNlbmQgYSByZXF1ZXN0IHRvIHRoZSBzZXJ2ZXIgdG8gcGVyZm9ybSBhbiBhY3Rpb24gb24gYW4gZXh0ZW5zaW9uLlxuICAgKlxuICAgKiBAcGFyYW0gYWN0aW9uIEEgdmFsaWQgYWN0aW9uIHRvIHBlcmZvcm0uXG4gICAqIEBwYXJhbSBlbnRyeSBUaGUgZXh0ZW5zaW9uIHRvIHBlcmZvcm0gdGhlIGFjdGlvbiBvbi5cbiAgICovXG4gIHByb3RlY3RlZCBwZXJmb3JtQWN0aW9uKFxuICAgIGFjdGlvbjogc3RyaW5nLFxuICAgIGVudHJ5OiBJRW50cnlcbiAgKTogUHJvbWlzZTxJQWN0aW9uUmVwbHk+IHtcbiAgICBjb25zdCBhY3Rpb25SZXF1ZXN0ID0gUHJpdmF0ZS5yZXF1ZXN0QVBJPElBY3Rpb25SZXBseT4oXG4gICAgICB7fSxcbiAgICAgIHtcbiAgICAgICAgbWV0aG9kOiAnUE9TVCcsXG4gICAgICAgIGJvZHk6IEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICBjbWQ6IGFjdGlvbixcbiAgICAgICAgICBleHRlbnNpb25fbmFtZTogZW50cnkubmFtZVxuICAgICAgICB9KVxuICAgICAgfVxuICAgICk7XG5cbiAgICBhY3Rpb25SZXF1ZXN0LnRoZW4oXG4gICAgICAoW3JlcGx5XSkgPT4ge1xuICAgICAgICBjb25zdCB0cmFucyA9IHRoaXMudHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgICAgIGlmIChyZXBseS5uZWVkc19yZXN0YXJ0LmluY2x1ZGVzKCdzZXJ2ZXInKSkge1xuICAgICAgICAgIHZvaWQgc2hvd0RpYWxvZyh7XG4gICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0luZm9ybWF0aW9uJyksXG4gICAgICAgICAgICBib2R5OiB0cmFucy5fXyhcbiAgICAgICAgICAgICAgJ1lvdSB3aWxsIG5lZWQgdG8gcmVzdGFydCBKdXB5dGVyTGFiIHRvIGFwcGx5IHRoZSBjaGFuZ2VzLidcbiAgICAgICAgICAgICksXG4gICAgICAgICAgICBidXR0b25zOiBbRGlhbG9nLm9rQnV0dG9uKHsgbGFiZWw6IHRyYW5zLl9fKCdPaycpIH0pXVxuICAgICAgICAgIH0pO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGNvbnN0IGZvbGxvd1Vwczogc3RyaW5nW10gPSBbXTtcbiAgICAgICAgICBpZiAocmVwbHkubmVlZHNfcmVzdGFydC5pbmNsdWRlcygnZnJvbnRlbmQnKSkge1xuICAgICAgICAgICAgZm9sbG93VXBzLnB1c2goXG4gICAgICAgICAgICAgIC8vIEB0cy1leHBlY3QtZXJyb3IgaXNFbGVjdHJvbiBpcyBub3QgYSBzdGFuZGFyZCBhdHRyaWJ1dGVcbiAgICAgICAgICAgICAgd2luZG93LmlzRWxlY3Ryb25cbiAgICAgICAgICAgICAgICA/IHRyYW5zLl9fKCdyZWxvYWQgSnVweXRlckxhYicpXG4gICAgICAgICAgICAgICAgOiB0cmFucy5fXygncmVmcmVzaCB0aGUgd2ViIHBhZ2UnKVxuICAgICAgICAgICAgKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgaWYgKHJlcGx5Lm5lZWRzX3Jlc3RhcnQuaW5jbHVkZXMoJ2tlcm5lbCcpKSB7XG4gICAgICAgICAgICBmb2xsb3dVcHMucHVzaChcbiAgICAgICAgICAgICAgdHJhbnMuX18oJ2luc3RhbGwgdGhlIGV4dGVuc2lvbiBpbiBhbGwga2VybmVscyBhbmQgcmVzdGFydCB0aGVtJylcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgfVxuICAgICAgICAgIHZvaWQgc2hvd0RpYWxvZyh7XG4gICAgICAgICAgICB0aXRsZTogdHJhbnMuX18oJ0luZm9ybWF0aW9uJyksXG4gICAgICAgICAgICBib2R5OiB0cmFucy5fXyhcbiAgICAgICAgICAgICAgJ1lvdSB3aWxsIG5lZWQgdG8gJTEgdG8gYXBwbHkgdGhlIGNoYW5nZXMuJyxcbiAgICAgICAgICAgICAgZm9sbG93VXBzLmpvaW4odHJhbnMuX18oJyBhbmQgJykpXG4gICAgICAgICAgICApLFxuICAgICAgICAgICAgYnV0dG9uczogW0RpYWxvZy5va0J1dHRvbih7IGxhYmVsOiB0cmFucy5fXygnT2snKSB9KV1cbiAgICAgICAgICB9KTtcbiAgICAgICAgfVxuICAgICAgICB0aGlzLmFjdGlvbkVycm9yID0gbnVsbDtcbiAgICAgIH0sXG4gICAgICByZWFzb24gPT4ge1xuICAgICAgICB0aGlzLmFjdGlvbkVycm9yID0gcmVhc29uLnRvU3RyaW5nKCk7XG4gICAgICB9XG4gICAgKTtcbiAgICB0aGlzLmFkZFBlbmRpbmdBY3Rpb24oYWN0aW9uUmVxdWVzdCk7XG4gICAgcmV0dXJuIGFjdGlvblJlcXVlc3QudGhlbigoW3JlcGx5XSkgPT4gcmVwbHkpO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIHBlbmRpbmcgYWN0aW9uLlxuICAgKlxuICAgKiBAcGFyYW0gcGVuZGluZyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBhY3Rpb24gaXMgY29tcGxldGVkLlxuICAgKi9cbiAgcHJvdGVjdGVkIGFkZFBlbmRpbmdBY3Rpb24ocGVuZGluZzogUHJvbWlzZTxhbnk+KTogdm9pZCB7XG4gICAgLy8gQWRkIHRvIHBlbmRpbmcgYWN0aW9ucyBjb2xsZWN0aW9uXG4gICAgdGhpcy5fcGVuZGluZ0FjdGlvbnMucHVzaChwZW5kaW5nKTtcblxuICAgIC8vIEVuc3VyZSBhY3Rpb24gaXMgcmVtb3ZlZCB3aGVuIHJlc29sdmVkXG4gICAgY29uc3QgcmVtb3ZlID0gKCkgPT4ge1xuICAgICAgY29uc3QgaSA9IHRoaXMuX3BlbmRpbmdBY3Rpb25zLmluZGV4T2YocGVuZGluZyk7XG4gICAgICB0aGlzLl9wZW5kaW5nQWN0aW9ucy5zcGxpY2UoaSwgMSk7XG4gICAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHVuZGVmaW5lZCk7XG4gICAgfTtcbiAgICBwZW5kaW5nLnRoZW4ocmVtb3ZlLCByZW1vdmUpO1xuXG4gICAgLy8gU2lnbmFsIGNoYW5nZWQgc3RhdGVcbiAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHVuZGVmaW5lZCk7XG4gIH1cblxuICBhY3Rpb25FcnJvcjogc3RyaW5nIHwgbnVsbCA9IG51bGw7XG5cbiAgLyoqXG4gICAqIENvbnRhaW5zIGFuIGVycm9yIG1lc3NhZ2UgaWYgYW4gZXJyb3Igb2NjdXJyZWQgd2hlbiBxdWVyeWluZyBpbnN0YWxsZWQgZXh0ZW5zaW9ucy5cbiAgICovXG4gIGluc3RhbGxlZEVycm9yOiBzdHJpbmcgfCBudWxsID0gbnVsbDtcblxuICAvKipcbiAgICogQ29udGFpbnMgYW4gZXJyb3IgbWVzc2FnZSBpZiBhbiBlcnJvciBvY2N1cnJlZCB3aGVuIHNlYXJjaGluZyBmb3IgZXh0ZW5zaW9ucy5cbiAgICovXG4gIHNlYXJjaEVycm9yOiBzdHJpbmcgfCBudWxsID0gbnVsbDtcblxuICAvKipcbiAgICogV2hldGhlciBhIHJlbG9hZCBzaG91bGQgYmUgY29uc2lkZXJlZCBkdWUgdG8gYWN0aW9ucyB0YWtlbi5cbiAgICovXG4gIHByb21wdFJlbG9hZCA9IGZhbHNlO1xuXG4gIC8qKlxuICAgKiBUaGUgc2VydmljZSBtYW5hZ2VyIHRvIHVzZSBmb3IgYnVpbGRpbmcuXG4gICAqL1xuICBwcm90ZWN0ZWQgc2VydmljZU1hbmFnZXI6IFNlcnZpY2VNYW5hZ2VyLklNYW5hZ2VyO1xuXG4gIHByb3RlY3RlZCB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcjtcblxuICBwcml2YXRlIF9pc0Rpc2NsYWltZWQgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfaXNFbmFibGVkID0gZmFsc2U7XG4gIHByaXZhdGUgX2lzTG9hZGluZ0luc3RhbGxlZEV4dGVuc2lvbnMgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfaXNTZWFyY2hpbmcgPSBmYWxzZTtcblxuICBwcml2YXRlIF9xdWVyeTogc3RyaW5nID0gJyc7XG4gIHByaXZhdGUgX3BhZ2U6IG51bWJlciA9IDE7XG4gIHByaXZhdGUgX3BhZ2luYXRpb246IG51bWJlciA9IDMwO1xuICBwcml2YXRlIF9sYXN0UGFnZTogbnVtYmVyID0gMTtcblxuICBwcml2YXRlIF9pbnN0YWxsZWQ6IElFbnRyeVtdO1xuICBwcml2YXRlIF9sYXN0U2VhcmNoUmVzdWx0OiBJRW50cnlbXTtcbiAgcHJpdmF0ZSBfcGVuZGluZ0FjdGlvbnM6IFByb21pc2U8YW55PltdID0gW107XG4gIHByaXZhdGUgX2RlYm91bmNlZFNlYXJjaDogRGVib3VuY2VyPHZvaWQsIHZvaWQ+O1xufVxuXG4vKipcbiAqIExpc3RNb2RlbCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIExpc3RNb2RlbCB7XG4gIC8qKlxuICAgKiBVdGlsaXR5IGZ1bmN0aW9uIHRvIGNoZWNrIHdoZXRoZXIgYW4gZW50cnkgY2FuIGJlIHVwZGF0ZWQuXG4gICAqXG4gICAqIEBwYXJhbSBlbnRyeSBUaGUgZW50cnkgdG8gY2hlY2suXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZW50cnlIYXNVcGRhdGUoZW50cnk6IElFbnRyeSk6IGJvb2xlYW4ge1xuICAgIGlmICghZW50cnkuaW5zdGFsbGVkIHx8ICFlbnRyeS5sYXRlc3RfdmVyc2lvbikge1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH1cbiAgICByZXR1cm4gc2VtdmVyLmx0KGVudHJ5Lmluc3RhbGxlZF92ZXJzaW9uLCBlbnRyeS5sYXRlc3RfdmVyc2lvbik7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBmdW5jdGlvbmFsaXR5LlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBIGNvbXBhcmF0b3IgZnVuY3Rpb24gdGhhdCBzb3J0cyBhbGxvd2VkRXh0ZW5zaW9ucyBvcmdzIHRvIHRoZSB0b3AuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gY29tcGFyYXRvcihhOiBJRW50cnksIGI6IElFbnRyeSk6IG51bWJlciB7XG4gICAgaWYgKGEubmFtZSA9PT0gYi5uYW1lKSB7XG4gICAgICByZXR1cm4gMDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIGEubmFtZSA+IGIubmFtZSA/IDEgOiAtMTtcbiAgICB9XG4gIH1cblxuICBjb25zdCBMSU5LX1BBUlNFUiA9IC88KFtePl0rKT47IHJlbD1cIihbXlwiXSspXCIsPy9nO1xuXG4gIC8qKlxuICAgKiBDYWxsIHRoZSBBUEkgZXh0ZW5zaW9uXG4gICAqXG4gICAqIEBwYXJhbSBxdWVyeUFyZ3MgUXVlcnkgYXJndW1lbnRzXG4gICAqIEBwYXJhbSBpbml0IEluaXRpYWwgdmFsdWVzIGZvciB0aGUgcmVxdWVzdFxuICAgKiBAcmV0dXJucyBUaGUgcmVzcG9uc2UgYm9keSBpbnRlcnByZXRlZCBhcyBKU09OIGFuZCB0aGUgcmVzcG9uc2UgbGluayBoZWFkZXJcbiAgICovXG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiByZXF1ZXN0QVBJPFQ+KFxuICAgIHF1ZXJ5QXJnczogeyBbazogc3RyaW5nXTogYW55IH0gPSB7fSxcbiAgICBpbml0OiBSZXF1ZXN0SW5pdCA9IHt9XG4gICk6IFByb21pc2U8W1QsIHsgW2tleTogc3RyaW5nXTogc3RyaW5nIH1dPiB7XG4gICAgLy8gTWFrZSByZXF1ZXN0IHRvIEp1cHl0ZXIgQVBJXG4gICAgY29uc3Qgc2V0dGluZ3MgPSBTZXJ2ZXJDb25uZWN0aW9uLm1ha2VTZXR0aW5ncygpO1xuICAgIGNvbnN0IHJlcXVlc3RVcmwgPSBVUkxFeHQuam9pbihcbiAgICAgIHNldHRpbmdzLmJhc2VVcmwsXG4gICAgICBFWFRFTlNJT05fQVBJX1BBVEggLy8gQVBJIE5hbWVzcGFjZVxuICAgICk7XG5cbiAgICBsZXQgcmVzcG9uc2U6IFJlc3BvbnNlO1xuICAgIHRyeSB7XG4gICAgICByZXNwb25zZSA9IGF3YWl0IFNlcnZlckNvbm5lY3Rpb24ubWFrZVJlcXVlc3QoXG4gICAgICAgIHJlcXVlc3RVcmwgKyBVUkxFeHQub2JqZWN0VG9RdWVyeVN0cmluZyhxdWVyeUFyZ3MpLFxuICAgICAgICBpbml0LFxuICAgICAgICBzZXR0aW5nc1xuICAgICAgKTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uTmV0d29ya0Vycm9yKGVycm9yKTtcbiAgICB9XG5cbiAgICBsZXQgZGF0YTogYW55ID0gYXdhaXQgcmVzcG9uc2UudGV4dCgpO1xuXG4gICAgaWYgKGRhdGEubGVuZ3RoID4gMCkge1xuICAgICAgdHJ5IHtcbiAgICAgICAgZGF0YSA9IEpTT04ucGFyc2UoZGF0YSk7XG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICBjb25zb2xlLmxvZygnTm90IGEgSlNPTiByZXNwb25zZSBib2R5LicsIHJlc3BvbnNlKTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICBpZiAoIXJlc3BvbnNlLm9rKSB7XG4gICAgICB0aHJvdyBuZXcgU2VydmVyQ29ubmVjdGlvbi5SZXNwb25zZUVycm9yKHJlc3BvbnNlLCBkYXRhLm1lc3NhZ2UgfHwgZGF0YSk7XG4gICAgfVxuXG4gICAgY29uc3QgbGluayA9IHJlc3BvbnNlLmhlYWRlcnMuZ2V0KCdMaW5rJykgPz8gJyc7XG5cbiAgICBjb25zdCBsaW5rczogeyBba2V5OiBzdHJpbmddOiBzdHJpbmcgfSA9IHt9O1xuICAgIGxldCBtYXRjaDogUmVnRXhwRXhlY0FycmF5IHwgbnVsbCA9IG51bGw7XG4gICAgd2hpbGUgKChtYXRjaCA9IExJTktfUEFSU0VSLmV4ZWMobGluaykpICE9PSBudWxsKSB7XG4gICAgICBsaW5rc1ttYXRjaFsyXV0gPSBtYXRjaFsxXTtcbiAgICB9XG4gICAgcmV0dXJuIFtkYXRhLCBsaW5rc107XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgQnV0dG9uLFxuICBGaWx0ZXJCb3gsXG4gIGluZm9JY29uLFxuICBqdXB5dGVySWNvbixcbiAgUGFuZWxXaXRoVG9vbGJhcixcbiAgUmVhY3RXaWRnZXQsXG4gIHJlZnJlc2hJY29uLFxuICBTaWRlUGFuZWwsXG4gIFRvb2xiYXJCdXR0b24sXG4gIFRvb2xiYXJCdXR0b25Db21wb25lbnRcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBNZXNzYWdlIH0gZnJvbSAnQGx1bWluby9tZXNzYWdpbmcnO1xuaW1wb3J0IHsgQWNjb3JkaW9uTGF5b3V0LCBBY2NvcmRpb25QYW5lbCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgUmVhY3RQYWdpbmF0ZSBmcm9tICdyZWFjdC1wYWdpbmF0ZSc7XG5pbXBvcnQgeyBBY3Rpb24sIElFbnRyeSwgTGlzdE1vZGVsIH0gZnJvbSAnLi9tb2RlbCc7XG5cbmNvbnN0IEJBREdFX1NJWkUgPSAzMjtcbmNvbnN0IEJBREdFX1FVRVJZX1NJWkUgPSBNYXRoLmZsb29yKGRldmljZVBpeGVsUmF0aW8gKiBCQURHRV9TSVpFKTtcblxuZnVuY3Rpb24gZ2V0RXh0ZW5zaW9uR2l0SHViVXNlcihlbnRyeTogSUVudHJ5KSB7XG4gIGlmIChcbiAgICBlbnRyeS5ob21lcGFnZV91cmwgJiZcbiAgICBlbnRyeS5ob21lcGFnZV91cmwuc3RhcnRzV2l0aCgnaHR0cHM6Ly9naXRodWIuY29tLycpXG4gICkge1xuICAgIHJldHVybiBlbnRyeS5ob21lcGFnZV91cmwuc3BsaXQoJy8nKVszXTtcbiAgfSBlbHNlIGlmIChcbiAgICBlbnRyeS5yZXBvc2l0b3J5X3VybCAmJlxuICAgIGVudHJ5LnJlcG9zaXRvcnlfdXJsLnN0YXJ0c1dpdGgoJ2h0dHBzOi8vZ2l0aHViLmNvbS8nKVxuICApIHtcbiAgICByZXR1cm4gZW50cnkucmVwb3NpdG9yeV91cmwuc3BsaXQoJy8nKVszXTtcbiAgfVxuICByZXR1cm4gbnVsbDtcbn1cblxuLyoqXG4gKiBWRE9NIGZvciB2aXN1YWxpemluZyBhbiBleHRlbnNpb24gZW50cnkuXG4gKi9cbmZ1bmN0aW9uIExpc3RFbnRyeShwcm9wczogTGlzdEVudHJ5LklQcm9wZXJ0aWVzKTogUmVhY3QuUmVhY3RFbGVtZW50PGFueT4ge1xuICBjb25zdCB7IGNhbkZldGNoLCBlbnRyeSwgc3VwcG9ydEluc3RhbGxhdGlvbiwgdHJhbnMgfSA9IHByb3BzO1xuICBjb25zdCBmbGFnQ2xhc3NlcyA9IFtdO1xuICBpZiAoZW50cnkuc3RhdHVzICYmIFsnb2snLCAnd2FybmluZycsICdlcnJvciddLmluZGV4T2YoZW50cnkuc3RhdHVzKSAhPT0gLTEpIHtcbiAgICBmbGFnQ2xhc3Nlcy5wdXNoKGBqcC1leHRlbnNpb25tYW5hZ2VyLWVudHJ5LSR7ZW50cnkuc3RhdHVzfWApO1xuICB9XG4gIGNvbnN0IGdpdGh1YlVzZXIgPSBjYW5GZXRjaCA/IGdldEV4dGVuc2lvbkdpdEh1YlVzZXIoZW50cnkpIDogbnVsbDtcblxuICBpZiAoIWVudHJ5LmFsbG93ZWQpIHtcbiAgICBmbGFnQ2xhc3Nlcy5wdXNoKGBqcC1leHRlbnNpb25tYW5hZ2VyLWVudHJ5LXNob3VsZC1iZS11bmluc3RhbGxlZGApO1xuICB9XG5cbiAgcmV0dXJuIChcbiAgICA8bGlcbiAgICAgIGNsYXNzTmFtZT17YGpwLWV4dGVuc2lvbm1hbmFnZXItZW50cnkgJHtmbGFnQ2xhc3Nlcy5qb2luKCcgJyl9YH1cbiAgICAgIHN0eWxlPXt7IGRpc3BsYXk6ICdmbGV4JyB9fVxuICAgID5cbiAgICAgIDxkaXYgc3R5bGU9e3sgbWFyZ2luUmlnaHQ6ICc4cHgnIH19PlxuICAgICAgICB7Z2l0aHViVXNlciA/IChcbiAgICAgICAgICA8aW1nXG4gICAgICAgICAgICBzcmM9e2BodHRwczovL2dpdGh1Yi5jb20vJHtnaXRodWJVc2VyfS5wbmc/c2l6ZT0ke0JBREdFX1FVRVJZX1NJWkV9YH1cbiAgICAgICAgICAgIHN0eWxlPXt7IHdpZHRoOiAnMzJweCcsIGhlaWdodDogJzMycHgnIH19XG4gICAgICAgICAgLz5cbiAgICAgICAgKSA6IChcbiAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICBzdHlsZT17eyB3aWR0aDogYCR7QkFER0VfU0laRX1weGAsIGhlaWdodDogYCR7QkFER0VfU0laRX1weGAgfX1cbiAgICAgICAgICAvPlxuICAgICAgICApfVxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItZW50cnktZGVzY3JpcHRpb25cIj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWVudHJ5LXRpdGxlXCI+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWVudHJ5LW5hbWVcIj5cbiAgICAgICAgICAgIHtlbnRyeS5ob21lcGFnZV91cmwgPyAoXG4gICAgICAgICAgICAgIDxhXG4gICAgICAgICAgICAgICAgaHJlZj17ZW50cnkuaG9tZXBhZ2VfdXJsfVxuICAgICAgICAgICAgICAgIHRhcmdldD1cIl9ibGFua1wiXG4gICAgICAgICAgICAgICAgcmVsPVwibm9vcGVuZXIgbm9yZWZlcnJlclwiXG4gICAgICAgICAgICAgICAgdGl0bGU9e3RyYW5zLl9fKCclMSBleHRlbnNpb24gaG9tZSBwYWdlJywgZW50cnkubmFtZSl9XG4gICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICB7ZW50cnkubmFtZX1cbiAgICAgICAgICAgICAgPC9hPlxuICAgICAgICAgICAgKSA6IChcbiAgICAgICAgICAgICAgPGRpdj57ZW50cnkubmFtZX08L2Rpdj5cbiAgICAgICAgICAgICl9XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWVudHJ5LXZlcnNpb25cIj5cbiAgICAgICAgICAgIDxkaXYgdGl0bGU9e3RyYW5zLl9fKCdWZXJzaW9uOiAlMScsIGVudHJ5Lmluc3RhbGxlZF92ZXJzaW9uKX0+XG4gICAgICAgICAgICAgIHtlbnRyeS5pbnN0YWxsZWRfdmVyc2lvbn1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgIHtlbnRyeS5pbnN0YWxsZWQgJiYgIWVudHJ5LmFsbG93ZWQgJiYgKFxuICAgICAgICAgICAgPFRvb2xiYXJCdXR0b25Db21wb25lbnRcbiAgICAgICAgICAgICAgaWNvbj17aW5mb0ljb259XG4gICAgICAgICAgICAgIGljb25MYWJlbD17dHJhbnMuX18oXG4gICAgICAgICAgICAgICAgJyUxIGV4dGVuc2lvbiBpcyBub3QgYWxsb3dlZCBhbnltb3JlLiBQbGVhc2UgdW5pbnN0YWxsIGl0IGltbWVkaWF0ZWx5IG9yIGNvbnRhY3QgeW91ciBhZG1pbmlzdHJhdG9yLicsXG4gICAgICAgICAgICAgICAgZW50cnkubmFtZVxuICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgICBvbkNsaWNrPXsoKSA9PlxuICAgICAgICAgICAgICAgIHdpbmRvdy5vcGVuKFxuICAgICAgICAgICAgICAgICAgJ2h0dHBzOi8vanVweXRlcmxhYi5yZWFkdGhlZG9jcy5pby9lbi9sYXRlc3QvdXNlci9leHRlbnNpb25zLmh0bWwnXG4gICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAvPlxuICAgICAgICAgICl9XG4gICAgICAgICAge2VudHJ5LmFwcHJvdmVkICYmIChcbiAgICAgICAgICAgIDxqdXB5dGVySWNvbi5yZWFjdFxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWlzLWFwcHJvdmVkXCJcbiAgICAgICAgICAgICAgdG9wPVwiMXB4XCJcbiAgICAgICAgICAgICAgaGVpZ2h0PVwiYXV0b1wiXG4gICAgICAgICAgICAgIHdpZHRoPVwiMWVtXCJcbiAgICAgICAgICAgICAgdGl0bGU9e3RyYW5zLl9fKFxuICAgICAgICAgICAgICAgICdUaGlzIGV4dGVuc2lvbiBpcyBhcHByb3ZlZCBieSB5b3VyIHNlY3VyaXR5IHRlYW0uJ1xuICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgLz5cbiAgICAgICAgICApfVxuICAgICAgICA8L2Rpdj5cbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWVudHJ5LWNvbnRlbnRcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItZW50cnktZGVzY3JpcHRpb25cIj5cbiAgICAgICAgICAgIHtlbnRyeS5kZXNjcmlwdGlvbn1cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICB7cHJvcHMucGVyZm9ybUFjdGlvbiAmJiAoXG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItZW50cnktYnV0dG9uc1wiPlxuICAgICAgICAgICAgICB7ZW50cnkuaW5zdGFsbGVkID8gKFxuICAgICAgICAgICAgICAgIDw+XG4gICAgICAgICAgICAgICAgICB7c3VwcG9ydEluc3RhbGxhdGlvbiAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDw+XG4gICAgICAgICAgICAgICAgICAgICAge0xpc3RNb2RlbC5lbnRyeUhhc1VwZGF0ZShlbnRyeSkgJiYgKFxuICAgICAgICAgICAgICAgICAgICAgICAgPEJ1dHRvblxuICAgICAgICAgICAgICAgICAgICAgICAgICBvbkNsaWNrPXsoKSA9PiBwcm9wcy5wZXJmb3JtQWN0aW9uISgnaW5zdGFsbCcsIGVudHJ5KX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgdGl0bGU9e3RyYW5zLl9fKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICdVcGRhdGUgXCIlMVwiIHRvIFwiJTJcIicsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgZW50cnkubmFtZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlbnRyeS5sYXRlc3RfdmVyc2lvblxuICAgICAgICAgICAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgICAgICAgICAgICAgICBtaW5pbWFsXG4gICAgICAgICAgICAgICAgICAgICAgICAgIHNtYWxsXG4gICAgICAgICAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHt0cmFucy5fXygnVXBkYXRlIHRvICUxJywgZW50cnkubGF0ZXN0X3ZlcnNpb24pfVxuICAgICAgICAgICAgICAgICAgICAgICAgPC9CdXR0b24+XG4gICAgICAgICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgICAgICAgICAgICA8QnV0dG9uXG4gICAgICAgICAgICAgICAgICAgICAgICBvbkNsaWNrPXsoKSA9PiBwcm9wcy5wZXJmb3JtQWN0aW9uISgndW5pbnN0YWxsJywgZW50cnkpfVxuICAgICAgICAgICAgICAgICAgICAgICAgdGl0bGU9e3RyYW5zLl9fKCdVbmluc3RhbGwgXCIlMVwiJywgZW50cnkubmFtZSl9XG4gICAgICAgICAgICAgICAgICAgICAgICBtaW5pbWFsXG4gICAgICAgICAgICAgICAgICAgICAgICBzbWFsbFxuICAgICAgICAgICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICAgICAgICAgIHt0cmFucy5fXygnVW5pbnN0YWxsJyl9XG4gICAgICAgICAgICAgICAgICAgICAgPC9CdXR0b24+XG4gICAgICAgICAgICAgICAgICAgIDwvPlxuICAgICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgICAgICAgIHtlbnRyeS5lbmFibGVkID8gKFxuICAgICAgICAgICAgICAgICAgICA8QnV0dG9uXG4gICAgICAgICAgICAgICAgICAgICAgb25DbGljaz17KCkgPT4gcHJvcHMucGVyZm9ybUFjdGlvbiEoJ2Rpc2FibGUnLCBlbnRyeSl9XG4gICAgICAgICAgICAgICAgICAgICAgdGl0bGU9e3RyYW5zLl9fKCdEaXNhYmxlIFwiJTFcIicsIGVudHJ5Lm5hbWUpfVxuICAgICAgICAgICAgICAgICAgICAgIG1pbmltYWxcbiAgICAgICAgICAgICAgICAgICAgICBzbWFsbFxuICAgICAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgICAge3RyYW5zLl9fKCdEaXNhYmxlJyl9XG4gICAgICAgICAgICAgICAgICAgIDwvQnV0dG9uPlxuICAgICAgICAgICAgICAgICAgKSA6IChcbiAgICAgICAgICAgICAgICAgICAgPEJ1dHRvblxuICAgICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9eygpID0+IHByb3BzLnBlcmZvcm1BY3Rpb24hKCdlbmFibGUnLCBlbnRyeSl9XG4gICAgICAgICAgICAgICAgICAgICAgdGl0bGU9e3RyYW5zLl9fKCdFbmFibGUgXCIlMVwiJywgZW50cnkubmFtZSl9XG4gICAgICAgICAgICAgICAgICAgICAgbWluaW1hbFxuICAgICAgICAgICAgICAgICAgICAgIHNtYWxsXG4gICAgICAgICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICAgICAgICB7dHJhbnMuX18oJ0VuYWJsZScpfVxuICAgICAgICAgICAgICAgICAgICA8L0J1dHRvbj5cbiAgICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgPC8+XG4gICAgICAgICAgICAgICkgOiAoXG4gICAgICAgICAgICAgICAgc3VwcG9ydEluc3RhbGxhdGlvbiAmJiAoXG4gICAgICAgICAgICAgICAgICA8QnV0dG9uXG4gICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9eygpID0+IHByb3BzLnBlcmZvcm1BY3Rpb24hKCdpbnN0YWxsJywgZW50cnkpfVxuICAgICAgICAgICAgICAgICAgICB0aXRsZT17dHJhbnMuX18oJ0luc3RhbGwgXCIlMVwiJywgZW50cnkubmFtZSl9XG4gICAgICAgICAgICAgICAgICAgIG1pbmltYWxcbiAgICAgICAgICAgICAgICAgICAgc21hbGxcbiAgICAgICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICAgICAge3RyYW5zLl9fKCdJbnN0YWxsJyl9XG4gICAgICAgICAgICAgICAgICA8L0J1dHRvbj5cbiAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICl9XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICApfVxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgIDwvbGk+XG4gICk7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgZXh0ZW5zaW9uIGVudHJ5IHN0YXRpY3MuXG4gKi9cbm5hbWVzcGFjZSBMaXN0RW50cnkge1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wZXJ0aWVzIHtcbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRodW1ibmFpbHMgY2FuIGJlIGZldGNoZWQgZnJvbSBleHRlcm5hbCB3ZWJzZXJ2aWNlcyBvciBub3QuXG4gICAgICovXG4gICAgY2FuRmV0Y2g6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZW50cnkgdG8gdmlzdWFsaXplLlxuICAgICAqL1xuICAgIGVudHJ5OiBJRW50cnk7XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBleHRlbnNpb24gY2FuIGJlICh1bi0paW5zdGFsbCBvciBub3QuXG4gICAgICovXG4gICAgc3VwcG9ydEluc3RhbGxhdGlvbjogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIENhbGxiYWNrIHRvIHVzZSBmb3IgcGVyZm9ybWluZyBhbiBhY3Rpb24gb24gdGhlIGVudHJ5LlxuICAgICAqXG4gICAgICogTm90IHByb3ZpZGVkIGlmIGFjdGlvbnMgYXJlIG5vdCBhbGxvd2VkLlxuICAgICAqL1xuICAgIHBlcmZvcm1BY3Rpb24/OiAoYWN0aW9uOiBBY3Rpb24sIGVudHJ5OiBJRW50cnkpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICAgKi9cbiAgICB0cmFuczogVHJhbnNsYXRpb25CdW5kbGU7XG4gIH1cbn1cblxuLyoqXG4gKiBMaXN0IHZpZXcgd2lkZ2V0IGZvciBleHRlbnNpb25zXG4gKi9cbmZ1bmN0aW9uIExpc3RWaWV3KHByb3BzOiBMaXN0Vmlldy5JUHJvcGVydGllcyk6IFJlYWN0LlJlYWN0RWxlbWVudDxhbnk+IHtcbiAgY29uc3QgeyBjYW5GZXRjaCwgcGVyZm9ybUFjdGlvbiwgc3VwcG9ydEluc3RhbGxhdGlvbiwgdHJhbnMgfSA9IHByb3BzO1xuXG4gIHJldHVybiAoXG4gICAgPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWxpc3R2aWV3LXdyYXBwZXJcIj5cbiAgICAgIHtwcm9wcy5lbnRyaWVzLmxlbmd0aCA+IDAgPyAoXG4gICAgICAgIDx1bCBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWxpc3R2aWV3XCI+XG4gICAgICAgICAge3Byb3BzLmVudHJpZXMubWFwKGVudHJ5ID0+IChcbiAgICAgICAgICAgIDxMaXN0RW50cnlcbiAgICAgICAgICAgICAga2V5PXtlbnRyeS5uYW1lfVxuICAgICAgICAgICAgICBjYW5GZXRjaD17Y2FuRmV0Y2h9XG4gICAgICAgICAgICAgIGVudHJ5PXtlbnRyeX1cbiAgICAgICAgICAgICAgcGVyZm9ybUFjdGlvbj17cGVyZm9ybUFjdGlvbn1cbiAgICAgICAgICAgICAgc3VwcG9ydEluc3RhbGxhdGlvbj17c3VwcG9ydEluc3RhbGxhdGlvbn1cbiAgICAgICAgICAgICAgdHJhbnM9e3RyYW5zfVxuICAgICAgICAgICAgLz5cbiAgICAgICAgICApKX1cbiAgICAgICAgPC91bD5cbiAgICAgICkgOiAoXG4gICAgICAgIDxkaXYga2V5PVwibWVzc2FnZVwiIGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItbGlzdHZpZXctbWVzc2FnZVwiPlxuICAgICAgICAgIHt0cmFucy5fXygnTm8gZW50cmllcycpfVxuICAgICAgICA8L2Rpdj5cbiAgICAgICl9XG4gICAgICB7cHJvcHMubnVtUGFnZXMgPiAxICYmIChcbiAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLXBhZ2luYXRpb25cIj5cbiAgICAgICAgICA8UmVhY3RQYWdpbmF0ZVxuICAgICAgICAgICAgcHJldmlvdXNMYWJlbD17JzwnfVxuICAgICAgICAgICAgbmV4dExhYmVsPXsnPid9XG4gICAgICAgICAgICBicmVha0xhYmVsPVwiLi4uXCJcbiAgICAgICAgICAgIGJyZWFrQ2xhc3NOYW1lPXsnYnJlYWsnfVxuICAgICAgICAgICAgaW5pdGlhbFBhZ2U9eyhwcm9wcy5pbml0aWFsUGFnZSA/PyAxKSAtIDF9XG4gICAgICAgICAgICBwYWdlQ291bnQ9e3Byb3BzLm51bVBhZ2VzfVxuICAgICAgICAgICAgbWFyZ2luUGFnZXNEaXNwbGF5ZWQ9ezJ9XG4gICAgICAgICAgICBwYWdlUmFuZ2VEaXNwbGF5ZWQ9ezN9XG4gICAgICAgICAgICBvblBhZ2VDaGFuZ2U9eyhkYXRhOiB7IHNlbGVjdGVkOiBudW1iZXIgfSkgPT5cbiAgICAgICAgICAgICAgcHJvcHMub25QYWdlKGRhdGEuc2VsZWN0ZWQgKyAxKVxuICAgICAgICAgICAgfVxuICAgICAgICAgICAgYWN0aXZlQ2xhc3NOYW1lPXsnYWN0aXZlJ31cbiAgICAgICAgICAvPlxuICAgICAgICA8L2Rpdj5cbiAgICAgICl9XG4gICAgPC9kaXY+XG4gICk7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgbGlzdCB2aWV3IHdpZGdldCBzdGF0aWNzLlxuICovXG5uYW1lc3BhY2UgTGlzdFZpZXcge1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wZXJ0aWVzIHtcbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRodW1ibmFpbHMgY2FuIGJlIGZldGNoZWQgZnJvbSBleHRlcm5hbCB3ZWJzZXJ2aWNlcyBvciBub3QuXG4gICAgICovXG4gICAgY2FuRmV0Y2g6IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZXh0ZW5zaW9uIGVudHJpZXMgdG8gZGlzcGxheS5cbiAgICAgKi9cbiAgICBlbnRyaWVzOiBSZWFkb25seUFycmF5PElFbnRyeT47XG5cbiAgICAvKipcbiAgICAgKiBBY3RpdmUgcGFnZVxuICAgICAqL1xuICAgIGluaXRpYWxQYWdlPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG51bWJlciBvZiBwYWdlcyB0aGF0IGNhbiBiZSB2aWV3ZWQgdmlhIHBhZ2luYXRpb24uXG4gICAgICovXG4gICAgbnVtUGFnZXM6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIGV4dGVuc2lvbiBjYW4gYmUgKHVuLSlpbnN0YWxsIG9yIG5vdC5cbiAgICAgKi9cbiAgICBzdXBwb3J0SW5zdGFsbGF0aW9uOiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGxhbmd1YWdlIHRyYW5zbGF0b3IuXG4gICAgICovXG4gICAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNhbGxiYWNrIHRvIHVzZSBmb3IgY2hhbmdpbmcgdGhlIHBhZ2VcbiAgICAgKi9cbiAgICBvblBhZ2U6IChwYWdlOiBudW1iZXIpID0+IHZvaWQ7XG5cbiAgICAvKipcbiAgICAgKiBDYWxsYmFjayB0byB1c2UgZm9yIHBlcmZvcm1pbmcgYW4gYWN0aW9uIG9uIGFuIGVudHJ5LlxuICAgICAqXG4gICAgICogTm90IHByb3ZpZGVkIGlmIGFjdGlvbnMgYXJlIG5vdCBhbGxvd2VkLlxuICAgICAqL1xuICAgIHBlcmZvcm1BY3Rpb24/OiAoYWN0aW9uOiBBY3Rpb24sIGVudHJ5OiBJRW50cnkpID0+IHZvaWQ7XG4gIH1cbn1cblxuZnVuY3Rpb24gRXJyb3JNZXNzYWdlKHByb3BzOiBSZWFjdC5Qcm9wc1dpdGhDaGlsZHJlbikge1xuICByZXR1cm4gPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWVycm9yXCI+e3Byb3BzLmNoaWxkcmVufTwvZGl2Pjtcbn1cblxuY2xhc3MgSGVhZGVyIGV4dGVuZHMgUmVhY3RXaWRnZXQge1xuICBjb25zdHJ1Y3RvcihcbiAgICBwcm90ZWN0ZWQgbW9kZWw6IExpc3RNb2RlbCxcbiAgICBwcm90ZWN0ZWQgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlLFxuICAgIHByb3RlY3RlZCBzZWFyY2hJbnB1dFJlZjogUmVhY3QuUmVmT2JqZWN0PEhUTUxJbnB1dEVsZW1lbnQ+XG4gICkge1xuICAgIHN1cGVyKCk7XG4gICAgbW9kZWwuc3RhdGVDaGFuZ2VkLmNvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLWV4dGVuc2lvbm1hbmFnZXItaGVhZGVyJyk7XG4gIH1cblxuICByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgIHJldHVybiAoXG4gICAgICA8PlxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItdGl0bGVcIj5cbiAgICAgICAgICA8c3Bhbj57dGhpcy50cmFucy5fXygnJTEgTWFuYWdlcicsIHRoaXMubW9kZWwubmFtZSl9PC9zcGFuPlxuICAgICAgICAgIHt0aGlzLm1vZGVsLmluc3RhbGxQYXRoICYmIChcbiAgICAgICAgICAgIDxpbmZvSWNvbi5yZWFjdFxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLXBhdGhcIlxuICAgICAgICAgICAgICB0YWc9XCJzcGFuXCJcbiAgICAgICAgICAgICAgdGl0bGU9e3RoaXMudHJhbnMuX18oXG4gICAgICAgICAgICAgICAgJ0V4dGVuc2lvbiBpbnN0YWxsYXRpb24gcGF0aDogJTEnLFxuICAgICAgICAgICAgICAgIHRoaXMubW9kZWwuaW5zdGFsbFBhdGhcbiAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgID48L2luZm9JY29uLnJlYWN0PlxuICAgICAgICAgICl9XG4gICAgICAgIDwvZGl2PlxuICAgICAgICA8RmlsdGVyQm94XG4gICAgICAgICAgcGxhY2Vob2xkZXI9e3RoaXMudHJhbnMuX18oJ1NlYXJjaCcpfVxuICAgICAgICAgIGRpc2FibGVkPXshdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWR9XG4gICAgICAgICAgdXBkYXRlRmlsdGVyPXsoZm4sIHF1ZXJ5KSA9PiB7XG4gICAgICAgICAgICB0aGlzLm1vZGVsLnF1ZXJ5ID0gcXVlcnkgPz8gJyc7XG4gICAgICAgICAgfX1cbiAgICAgICAgICB1c2VGdXp6eUZpbHRlcj17ZmFsc2V9XG4gICAgICAgICAgaW5wdXRSZWY9e3RoaXMuc2VhcmNoSW5wdXRSZWZ9XG4gICAgICAgIC8+XG5cbiAgICAgICAgPGRpdlxuICAgICAgICAgIGNsYXNzTmFtZT17YGpwLWV4dGVuc2lvbm1hbmFnZXItcGVuZGluZyAke1xuICAgICAgICAgICAgdGhpcy5tb2RlbC5oYXNQZW5kaW5nQWN0aW9ucygpID8gJ2pwLW1vZC1oYXNQZW5kaW5nJyA6ICcnXG4gICAgICAgICAgfWB9XG4gICAgICAgIC8+XG4gICAgICAgIHt0aGlzLm1vZGVsLmFjdGlvbkVycm9yICYmIChcbiAgICAgICAgICA8RXJyb3JNZXNzYWdlPlxuICAgICAgICAgICAgPHA+e3RoaXMudHJhbnMuX18oJ0Vycm9yIHdoZW4gcGVyZm9ybWluZyBhbiBhY3Rpb24uJyl9PC9wPlxuICAgICAgICAgICAgPHA+e3RoaXMudHJhbnMuX18oJ1JlYXNvbiBnaXZlbjonKX08L3A+XG4gICAgICAgICAgICA8cHJlPnt0aGlzLm1vZGVsLmFjdGlvbkVycm9yfTwvcHJlPlxuICAgICAgICAgIDwvRXJyb3JNZXNzYWdlPlxuICAgICAgICApfVxuICAgICAgPC8+XG4gICAgKTtcbiAgfVxufVxuXG5jbGFzcyBXYXJuaW5nIGV4dGVuZHMgUmVhY3RXaWRnZXQge1xuICBjb25zdHJ1Y3RvcihcbiAgICBwcm90ZWN0ZWQgbW9kZWw6IExpc3RNb2RlbCxcbiAgICBwcm90ZWN0ZWQgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlXG4gICkge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5hZGRDbGFzcygnanAtZXh0ZW5zaW9ubWFuYWdlci1kaXNjbGFpbWVyJyk7XG4gICAgbW9kZWwuc3RhdGVDaGFuZ2VkLmNvbm5lY3QodGhpcy51cGRhdGUsIHRoaXMpO1xuICB9XG5cbiAgcmVuZGVyKCk6IEpTWC5FbGVtZW50IHtcbiAgICByZXR1cm4gKFxuICAgICAgPD5cbiAgICAgICAgPHA+XG4gICAgICAgICAge3RoaXMudHJhbnNcbiAgICAgICAgICAgIC5fXyhgVGhlIEp1cHl0ZXJMYWIgZGV2ZWxvcG1lbnQgdGVhbSBpcyBleGNpdGVkIHRvIGhhdmUgYSByb2J1c3RcbnRoaXJkLXBhcnR5IGV4dGVuc2lvbiBjb21tdW5pdHkuIEhvd2V2ZXIsIHdlIGRvIG5vdCByZXZpZXdcbnRoaXJkLXBhcnR5IGV4dGVuc2lvbnMsIGFuZCBzb21lIGV4dGVuc2lvbnMgbWF5IGludHJvZHVjZSBzZWN1cml0eVxucmlza3Mgb3IgY29udGFpbiBtYWxpY2lvdXMgY29kZSB0aGF0IHJ1bnMgb24geW91ciBtYWNoaW5lLiBNb3Jlb3ZlciBpbiBvcmRlclxudG8gd29yaywgdGhpcyBwYW5lbCBuZWVkcyB0byBmZXRjaCBkYXRhIGZyb20gd2ViIHNlcnZpY2VzLiBEbyB5b3UgYWdyZWUgdG9cbmFjdGl2YXRlIHRoaXMgZmVhdHVyZT9gKX1cbiAgICAgICAgICA8YnIgLz5cbiAgICAgICAgICA8YVxuICAgICAgICAgICAgaHJlZj1cImh0dHBzOi8vanVweXRlcmxhYi5yZWFkdGhlZG9jcy5pby9lbi9sYXRlc3QvcHJpdmFjeV9wb2xpY2llcy5odG1sXCJcbiAgICAgICAgICAgIHRhcmdldD1cIl9ibGFua1wiXG4gICAgICAgICAgICByZWw9XCJub3JlZmVycmVyXCJcbiAgICAgICAgICA+XG4gICAgICAgICAgICB7dGhpcy50cmFucy5fXygnUGxlYXNlIHJlYWQgdGhlIHByaXZhY3kgcG9saWN5LicpfVxuICAgICAgICAgIDwvYT5cbiAgICAgICAgPC9wPlxuICAgICAgICB7dGhpcy5tb2RlbC5pc0Rpc2NsYWltZWQgPyAoXG4gICAgICAgICAgPEJ1dHRvblxuICAgICAgICAgICAgY2xhc3NOYW1lPVwianAtZXh0ZW5zaW9ubWFuYWdlci1kaXNjbGFpbWVyLWRpc2FibGVcIlxuICAgICAgICAgICAgb25DbGljaz17KGU6IFJlYWN0Lk1vdXNlRXZlbnQ8RWxlbWVudCwgTW91c2VFdmVudD4pID0+IHtcbiAgICAgICAgICAgICAgdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWQgPSBmYWxzZTtcbiAgICAgICAgICAgIH19XG4gICAgICAgICAgICB0aXRsZT17dGhpcy50cmFucy5fXygnVGhpcyB3aWxsIHdpdGhkcmF3IHlvdXIgY29uc2VudC4nKX1cbiAgICAgICAgICA+XG4gICAgICAgICAgICB7dGhpcy50cmFucy5fXygnTm8nKX1cbiAgICAgICAgICA8L0J1dHRvbj5cbiAgICAgICAgKSA6IChcbiAgICAgICAgICA8ZGl2PlxuICAgICAgICAgICAgPEJ1dHRvblxuICAgICAgICAgICAgICBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWRpc2NsYWltZXItZW5hYmxlXCJcbiAgICAgICAgICAgICAgb25DbGljaz17KCkgPT4ge1xuICAgICAgICAgICAgICAgIHRoaXMubW9kZWwuaXNEaXNjbGFpbWVkID0gdHJ1ZTtcbiAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAge3RoaXMudHJhbnMuX18oJ1llcycpfVxuICAgICAgICAgICAgPC9CdXR0b24+XG4gICAgICAgICAgICA8QnV0dG9uXG4gICAgICAgICAgICAgIGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItZGlzY2xhaW1lci1kaXNhYmxlXCJcbiAgICAgICAgICAgICAgb25DbGljaz17KCkgPT4ge1xuICAgICAgICAgICAgICAgIHRoaXMubW9kZWwuaXNFbmFibGVkID0gZmFsc2U7XG4gICAgICAgICAgICAgIH19XG4gICAgICAgICAgICAgIHRpdGxlPXt0aGlzLnRyYW5zLl9fKFxuICAgICAgICAgICAgICAgICdUaGlzIHdpbGwgZGlzYWJsZSB0aGUgZXh0ZW5zaW9uIG1hbmFnZXIgcGFuZWw7IGluY2x1ZGluZyB0aGUgbGlzdGluZyBvZiBpbnN0YWxsZWQgZXh0ZW5zaW9uLidcbiAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAge3RoaXMudHJhbnMuX18oJ05vLCBkaXNhYmxlJyl9XG4gICAgICAgICAgICA8L0J1dHRvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKX1cbiAgICAgIDwvPlxuICAgICk7XG4gIH1cbn1cblxuY2xhc3MgSW5zdGFsbGVkTGlzdCBleHRlbmRzIFJlYWN0V2lkZ2V0IHtcbiAgY29uc3RydWN0b3IoXG4gICAgcHJvdGVjdGVkIG1vZGVsOiBMaXN0TW9kZWwsXG4gICAgcHJvdGVjdGVkIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApIHtcbiAgICBzdXBlcigpO1xuICAgIG1vZGVsLnN0YXRlQ2hhbmdlZC5jb25uZWN0KHRoaXMudXBkYXRlLCB0aGlzKTtcbiAgfVxuXG4gIHJlbmRlcigpOiBKU1guRWxlbWVudCB7XG4gICAgcmV0dXJuIChcbiAgICAgIDw+XG4gICAgICAgIHt0aGlzLm1vZGVsLmluc3RhbGxlZEVycm9yICE9PSBudWxsID8gKFxuICAgICAgICAgIDxFcnJvck1lc3NhZ2U+XG4gICAgICAgICAgICB7YEVycm9yIHF1ZXJ5aW5nIGluc3RhbGxlZCBleHRlbnNpb25zJHtcbiAgICAgICAgICAgICAgdGhpcy5tb2RlbC5pbnN0YWxsZWRFcnJvciA/IGA6ICR7dGhpcy5tb2RlbC5pbnN0YWxsZWRFcnJvcn1gIDogJy4nXG4gICAgICAgICAgICB9YH1cbiAgICAgICAgICA8L0Vycm9yTWVzc2FnZT5cbiAgICAgICAgKSA6IHRoaXMubW9kZWwuaXNMb2FkaW5nSW5zdGFsbGVkRXh0ZW5zaW9ucyA/IChcbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLWV4dGVuc2lvbm1hbmFnZXItbG9hZGVyXCI+XG4gICAgICAgICAgICB7dGhpcy50cmFucy5fXygnVXBkYXRpbmcgZXh0ZW5zaW9ucyBsaXN04oCmJyl9XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICkgOiAoXG4gICAgICAgICAgPExpc3RWaWV3XG4gICAgICAgICAgICBjYW5GZXRjaD17dGhpcy5tb2RlbC5pc0Rpc2NsYWltZWR9XG4gICAgICAgICAgICBlbnRyaWVzPXt0aGlzLm1vZGVsLmluc3RhbGxlZC5maWx0ZXIocGtnID0+XG4gICAgICAgICAgICAgIG5ldyBSZWdFeHAodGhpcy5tb2RlbC5xdWVyeS50b0xvd2VyQ2FzZSgpKS50ZXN0KHBrZy5uYW1lKVxuICAgICAgICAgICAgKX1cbiAgICAgICAgICAgIG51bVBhZ2VzPXsxfVxuICAgICAgICAgICAgdHJhbnM9e3RoaXMudHJhbnN9XG4gICAgICAgICAgICBvblBhZ2U9e3ZhbHVlID0+IHtcbiAgICAgICAgICAgICAgLyogbm8tb3AgKi9cbiAgICAgICAgICAgIH19XG4gICAgICAgICAgICBwZXJmb3JtQWN0aW9uPXtcbiAgICAgICAgICAgICAgdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWQgPyB0aGlzLm9uQWN0aW9uLmJpbmQodGhpcykgOiBudWxsXG4gICAgICAgICAgICB9XG4gICAgICAgICAgICBzdXBwb3J0SW5zdGFsbGF0aW9uPXtcbiAgICAgICAgICAgICAgdGhpcy5tb2RlbC5jYW5JbnN0YWxsICYmIHRoaXMubW9kZWwuaXNEaXNjbGFpbWVkXG4gICAgICAgICAgICB9XG4gICAgICAgICAgLz5cbiAgICAgICAgKX1cbiAgICAgIDwvPlxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogQ2FsbGJhY2sgaGFuZGxlciBmb3Igd2hlbiB0aGUgdXNlciB3YW50cyB0byBwZXJmb3JtIGFuIGFjdGlvbiBvbiBhbiBleHRlbnNpb24uXG4gICAqXG4gICAqIEBwYXJhbSBhY3Rpb24gVGhlIGFjdGlvbiB0byBwZXJmb3JtLlxuICAgKiBAcGFyYW0gZW50cnkgVGhlIGVudHJ5IHRvIHBlcmZvcm0gdGhlIGFjdGlvbiBvbi5cbiAgICovXG4gIG9uQWN0aW9uKGFjdGlvbjogQWN0aW9uLCBlbnRyeTogSUVudHJ5KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgc3dpdGNoIChhY3Rpb24pIHtcbiAgICAgIGNhc2UgJ2luc3RhbGwnOlxuICAgICAgICByZXR1cm4gdGhpcy5tb2RlbC5pbnN0YWxsKGVudHJ5KTtcbiAgICAgIGNhc2UgJ3VuaW5zdGFsbCc6XG4gICAgICAgIHJldHVybiB0aGlzLm1vZGVsLnVuaW5zdGFsbChlbnRyeSk7XG4gICAgICBjYXNlICdlbmFibGUnOlxuICAgICAgICByZXR1cm4gdGhpcy5tb2RlbC5lbmFibGUoZW50cnkpO1xuICAgICAgY2FzZSAnZGlzYWJsZSc6XG4gICAgICAgIHJldHVybiB0aGlzLm1vZGVsLmRpc2FibGUoZW50cnkpO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBJbnZhbGlkIGFjdGlvbjogJHthY3Rpb259YCk7XG4gICAgfVxuICB9XG59XG5cbmNsYXNzIFNlYXJjaFJlc3VsdCBleHRlbmRzIFJlYWN0V2lkZ2V0IHtcbiAgY29uc3RydWN0b3IoXG4gICAgcHJvdGVjdGVkIG1vZGVsOiBMaXN0TW9kZWwsXG4gICAgcHJvdGVjdGVkIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZVxuICApIHtcbiAgICBzdXBlcigpO1xuICAgIG1vZGVsLnN0YXRlQ2hhbmdlZC5jb25uZWN0KHRoaXMudXBkYXRlLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDYWxsYmFjayBoYW5kbGVyIGZvciB0aGUgdXNlciBjaGFuZ2VzIHRoZSBwYWdlIG9mIHRoZSBzZWFyY2ggcmVzdWx0IHBhZ2luYXRpb24uXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSBUaGUgcGFnaW5hdGlvbiBwYWdlIG51bWJlci5cbiAgICovXG4gIG9uUGFnZSh2YWx1ZTogbnVtYmVyKTogdm9pZCB7XG4gICAgdGhpcy5tb2RlbC5wYWdlID0gdmFsdWU7XG4gIH1cblxuICAvKipcbiAgICogQ2FsbGJhY2sgaGFuZGxlciBmb3Igd2hlbiB0aGUgdXNlciB3YW50cyB0byBwZXJmb3JtIGFuIGFjdGlvbiBvbiBhbiBleHRlbnNpb24uXG4gICAqXG4gICAqIEBwYXJhbSBhY3Rpb24gVGhlIGFjdGlvbiB0byBwZXJmb3JtLlxuICAgKiBAcGFyYW0gZW50cnkgVGhlIGVudHJ5IHRvIHBlcmZvcm0gdGhlIGFjdGlvbiBvbi5cbiAgICovXG4gIG9uQWN0aW9uKGFjdGlvbjogQWN0aW9uLCBlbnRyeTogSUVudHJ5KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgc3dpdGNoIChhY3Rpb24pIHtcbiAgICAgIGNhc2UgJ2luc3RhbGwnOlxuICAgICAgICByZXR1cm4gdGhpcy5tb2RlbC5pbnN0YWxsKGVudHJ5KTtcbiAgICAgIGNhc2UgJ3VuaW5zdGFsbCc6XG4gICAgICAgIHJldHVybiB0aGlzLm1vZGVsLnVuaW5zdGFsbChlbnRyeSk7XG4gICAgICBjYXNlICdlbmFibGUnOlxuICAgICAgICByZXR1cm4gdGhpcy5tb2RlbC5lbmFibGUoZW50cnkpO1xuICAgICAgY2FzZSAnZGlzYWJsZSc6XG4gICAgICAgIHJldHVybiB0aGlzLm1vZGVsLmRpc2FibGUoZW50cnkpO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBJbnZhbGlkIGFjdGlvbjogJHthY3Rpb259YCk7XG4gICAgfVxuICB9XG5cbiAgcmVuZGVyKCk6IEpTWC5FbGVtZW50IHtcbiAgICByZXR1cm4gKFxuICAgICAgPD5cbiAgICAgICAge3RoaXMubW9kZWwuc2VhcmNoRXJyb3IgIT09IG51bGwgPyAoXG4gICAgICAgICAgPEVycm9yTWVzc2FnZT5cbiAgICAgICAgICAgIHtgRXJyb3Igc2VhcmNoaW5nIGZvciBleHRlbnNpb25zJHtcbiAgICAgICAgICAgICAgdGhpcy5tb2RlbC5zZWFyY2hFcnJvciA/IGA6ICR7dGhpcy5tb2RlbC5zZWFyY2hFcnJvcn1gIDogJy4nXG4gICAgICAgICAgICB9YH1cbiAgICAgICAgICA8L0Vycm9yTWVzc2FnZT5cbiAgICAgICAgKSA6IHRoaXMubW9kZWwuaXNTZWFyY2hpbmcgPyAoXG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1leHRlbnNpb25tYW5hZ2VyLWxvYWRlclwiPlxuICAgICAgICAgICAge3RoaXMudHJhbnMuX18oJ1VwZGF0aW5nIGV4dGVuc2lvbnMgbGlzdOKApicpfVxuICAgICAgICAgIDwvZGl2PlxuICAgICAgICApIDogKFxuICAgICAgICAgIDxMaXN0Vmlld1xuICAgICAgICAgICAgY2FuRmV0Y2g9e3RoaXMubW9kZWwuaXNEaXNjbGFpbWVkfVxuICAgICAgICAgICAgZW50cmllcz17dGhpcy5tb2RlbC5zZWFyY2hSZXN1bHR9XG4gICAgICAgICAgICBpbml0aWFsUGFnZT17dGhpcy5tb2RlbC5wYWdlfVxuICAgICAgICAgICAgbnVtUGFnZXM9e3RoaXMubW9kZWwubGFzdFBhZ2V9XG4gICAgICAgICAgICBvblBhZ2U9e3ZhbHVlID0+IHtcbiAgICAgICAgICAgICAgdGhpcy5vblBhZ2UodmFsdWUpO1xuICAgICAgICAgICAgfX1cbiAgICAgICAgICAgIHBlcmZvcm1BY3Rpb249e1xuICAgICAgICAgICAgICB0aGlzLm1vZGVsLmlzRGlzY2xhaW1lZCA/IHRoaXMub25BY3Rpb24uYmluZCh0aGlzKSA6IG51bGxcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHN1cHBvcnRJbnN0YWxsYXRpb249e1xuICAgICAgICAgICAgICB0aGlzLm1vZGVsLmNhbkluc3RhbGwgJiYgdGhpcy5tb2RlbC5pc0Rpc2NsYWltZWRcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHRyYW5zPXt0aGlzLnRyYW5zfVxuICAgICAgICAgIC8+XG4gICAgICAgICl9XG4gICAgICA8Lz5cbiAgICApO1xuICB9XG5cbiAgdXBkYXRlKCk6IHZvaWQge1xuICAgIHRoaXMudGl0bGUubGFiZWwgPSB0aGlzLm1vZGVsLnF1ZXJ5XG4gICAgICA/IHRoaXMudHJhbnMuX18oJ1NlYXJjaCBSZXN1bHRzJylcbiAgICAgIDogdGhpcy50cmFucy5fXygnRGlzY292ZXInKTtcbiAgICBzdXBlci51cGRhdGUoKTtcbiAgfVxufVxuXG5leHBvcnQgbmFtZXNwYWNlIEV4dGVuc2lvbnNQYW5lbCB7XG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIG1vZGVsOiBMaXN0TW9kZWw7XG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIEV4dGVuc2lvbnNQYW5lbCBleHRlbmRzIFNpZGVQYW5lbCB7XG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IEV4dGVuc2lvbnNQYW5lbC5JT3B0aW9ucykge1xuICAgIGNvbnN0IHsgbW9kZWwsIHRyYW5zbGF0b3IgfSA9IG9wdGlvbnM7XG4gICAgc3VwZXIoeyB0cmFuc2xhdG9yIH0pO1xuICAgIHRoaXMubW9kZWwgPSBtb2RlbDtcbiAgICB0aGlzLl9zZWFyY2hJbnB1dFJlZiA9IFJlYWN0LmNyZWF0ZVJlZjxIVE1MSW5wdXRFbGVtZW50PigpO1xuICAgIHRoaXMuYWRkQ2xhc3MoJ2pwLWV4dGVuc2lvbm1hbmFnZXItdmlldycpO1xuXG4gICAgdGhpcy50cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgdGhpcy5oZWFkZXIuYWRkV2lkZ2V0KG5ldyBIZWFkZXIobW9kZWwsIHRoaXMudHJhbnMsIHRoaXMuX3NlYXJjaElucHV0UmVmKSk7XG5cbiAgICBjb25zdCB3YXJuaW5nID0gbmV3IFdhcm5pbmcobW9kZWwsIHRoaXMudHJhbnMpO1xuICAgIHdhcm5pbmcudGl0bGUubGFiZWwgPSB0aGlzLnRyYW5zLl9fKCdXYXJuaW5nJyk7XG5cbiAgICB0aGlzLmFkZFdpZGdldCh3YXJuaW5nKTtcblxuICAgIGNvbnN0IGluc3RhbGxlZCA9IG5ldyBQYW5lbFdpdGhUb29sYmFyKCk7XG4gICAgaW5zdGFsbGVkLmFkZENsYXNzKCdqcC1leHRlbnNpb25tYW5hZ2VyLWluc3RhbGxlZGxpc3QnKTtcbiAgICBpbnN0YWxsZWQudGl0bGUubGFiZWwgPSB0aGlzLnRyYW5zLl9fKCdJbnN0YWxsZWQnKTtcblxuICAgIGluc3RhbGxlZC50b29sYmFyLmFkZEl0ZW0oXG4gICAgICAncmVmcmVzaCcsXG4gICAgICBuZXcgVG9vbGJhckJ1dHRvbih7XG4gICAgICAgIGljb246IHJlZnJlc2hJY29uLFxuICAgICAgICBvbkNsaWNrOiAoKSA9PiB7XG4gICAgICAgICAgbW9kZWwucmVmcmVzaEluc3RhbGxlZCh0cnVlKS5jYXRjaChyZWFzb24gPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICAgICAgYEZhaWxlZCB0byByZWZyZXNoIHRoZSBpbnN0YWxsZWQgZXh0ZW5zaW9ucyBsaXN0OlxcbiR7cmVhc29ufWBcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgfSk7XG4gICAgICAgIH0sXG4gICAgICAgIHRvb2x0aXA6IHRoaXMudHJhbnMuX18oJ1JlZnJlc2ggZXh0ZW5zaW9ucyBsaXN0JylcbiAgICAgIH0pXG4gICAgKTtcblxuICAgIGluc3RhbGxlZC5hZGRXaWRnZXQobmV3IEluc3RhbGxlZExpc3QobW9kZWwsIHRoaXMudHJhbnMpKTtcblxuICAgIHRoaXMuYWRkV2lkZ2V0KGluc3RhbGxlZCk7XG5cbiAgICBpZiAodGhpcy5tb2RlbC5jYW5JbnN0YWxsKSB7XG4gICAgICBjb25zdCBzZWFyY2hSZXN1bHRzID0gbmV3IFNlYXJjaFJlc3VsdChtb2RlbCwgdGhpcy50cmFucyk7XG4gICAgICBzZWFyY2hSZXN1bHRzLmFkZENsYXNzKCdqcC1leHRlbnNpb25tYW5hZ2VyLXNlYXJjaHJlc3VsdHMnKTtcbiAgICAgIHRoaXMuYWRkV2lkZ2V0KHNlYXJjaFJlc3VsdHMpO1xuICAgIH1cblxuICAgIHRoaXMuX3dhc0Rpc2NsYWltZWQgPSB0aGlzLm1vZGVsLmlzRGlzY2xhaW1lZDtcbiAgICBpZiAodGhpcy5tb2RlbC5pc0Rpc2NsYWltZWQpIHtcbiAgICAgICh0aGlzLmNvbnRlbnQgYXMgQWNjb3JkaW9uUGFuZWwpLmNvbGxhcHNlKDApO1xuICAgICAgKHRoaXMuY29udGVudC5sYXlvdXQgYXMgQWNjb3JkaW9uTGF5b3V0KS5zZXRSZWxhdGl2ZVNpemVzKFswLCAxLCAxXSk7XG4gICAgfSBlbHNlIHtcbiAgICAgIC8vIElmIHdhcm5pbmcgaXMgbm90IGRpc2NsYWltZWQgZXhwYW5kIG9ubHkgdGhlIHdhcm5pbmcgcGFuZWxcbiAgICAgICh0aGlzLmNvbnRlbnQgYXMgQWNjb3JkaW9uUGFuZWwpLmV4cGFuZCgwKTtcbiAgICAgICh0aGlzLmNvbnRlbnQgYXMgQWNjb3JkaW9uUGFuZWwpLmNvbGxhcHNlKDEpO1xuICAgICAgKHRoaXMuY29udGVudCBhcyBBY2NvcmRpb25QYW5lbCkuY29sbGFwc2UoMik7XG4gICAgfVxuXG4gICAgdGhpcy5tb2RlbC5zdGF0ZUNoYW5nZWQuY29ubmVjdCh0aGlzLl9vblN0YXRlQ2hhbmdlZCwgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgd2lkZ2V0IGFuZCBpdHMgZGVzY2VuZGFudCB3aWRnZXRzLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMubW9kZWwuc3RhdGVDaGFuZ2VkLmRpc2Nvbm5lY3QodGhpcy5fb25TdGF0ZUNoYW5nZWQsIHRoaXMpO1xuICAgIHN1cGVyLmRpc3Bvc2UoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgdGhlIERPTSBldmVudHMgZm9yIHRoZSBleHRlbnNpb24gbWFuYWdlciBzZWFyY2ggYmFyLlxuICAgKlxuICAgKiBAcGFyYW0gZXZlbnQgLSBUaGUgRE9NIGV2ZW50IHNlbnQgdG8gdGhlIGV4dGVuc2lvbiBtYW5hZ2VyIHNlYXJjaCBiYXIuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgaW1wbGVtZW50cyB0aGUgRE9NIGBFdmVudExpc3RlbmVyYCBpbnRlcmZhY2UgYW5kIGlzXG4gICAqIGNhbGxlZCBpbiByZXNwb25zZSB0byBldmVudHMgb24gdGhlIHNlYXJjaCBiYXIncyBET00gbm9kZS5cbiAgICogSXQgc2hvdWxkIG5vdCBiZSBjYWxsZWQgZGlyZWN0bHkgYnkgdXNlciBjb2RlLlxuICAgKi9cbiAgaGFuZGxlRXZlbnQoZXZlbnQ6IEV2ZW50KTogdm9pZCB7XG4gICAgc3dpdGNoIChldmVudC50eXBlKSB7XG4gICAgICBjYXNlICdmb2N1cyc6XG4gICAgICBjYXNlICdibHVyJzpcbiAgICAgICAgdGhpcy5fdG9nZ2xlRm9jdXNlZCgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIGJyZWFrO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBIG1lc3NhZ2UgaGFuZGxlciBpbnZva2VkIG9uIGEgYCdiZWZvcmUtYXR0YWNoJ2AgbWVzc2FnZS5cbiAgICovXG4gIHByb3RlY3RlZCBvbkJlZm9yZUF0dGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICB0aGlzLm5vZGUuYWRkRXZlbnRMaXN0ZW5lcignZm9jdXMnLCB0aGlzLCB0cnVlKTtcbiAgICB0aGlzLm5vZGUuYWRkRXZlbnRMaXN0ZW5lcignYmx1cicsIHRoaXMsIHRydWUpO1xuICAgIHN1cGVyLm9uQmVmb3JlQXR0YWNoKG1zZyk7XG4gIH1cblxuICBwcm90ZWN0ZWQgb25CZWZvcmVTaG93KG1zZzogTWVzc2FnZSk6IHZvaWQge1xuICAgIGlmICghdGhpcy5fd2FzSW5pdGlhbGl6ZWQpIHtcbiAgICAgIHRoaXMuX3dhc0luaXRpYWxpemVkID0gdHJ1ZTtcbiAgICAgIHRoaXMubW9kZWwucmVmcmVzaEluc3RhbGxlZCgpLmNhdGNoKHJlYXNvbiA9PiB7XG4gICAgICAgIGNvbnNvbGUubG9nKGBGYWlsZWQgdG8gcmVmcmVzaCBpbnN0YWxsZWQgZXh0ZW5zaW9uIGxpc3Q6XFxuJHtyZWFzb259YCk7XG4gICAgICB9KTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBtZXNzYWdlIGhhbmRsZXIgaW52b2tlZCBvbiBhbiBgJ2FmdGVyLWRldGFjaCdgIG1lc3NhZ2UuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BZnRlckRldGFjaChtc2c6IE1lc3NhZ2UpOiB2b2lkIHtcbiAgICBzdXBlci5vbkFmdGVyRGV0YWNoKG1zZyk7XG4gICAgdGhpcy5ub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2ZvY3VzJywgdGhpcywgdHJ1ZSk7XG4gICAgdGhpcy5ub2RlLnJlbW92ZUV2ZW50TGlzdGVuZXIoJ2JsdXInLCB0aGlzLCB0cnVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIG1lc3NhZ2UgaGFuZGxlciBpbnZva2VkIG9uIGFuIGAnYWN0aXZhdGUtcmVxdWVzdCdgIG1lc3NhZ2UuXG4gICAqL1xuICBwcm90ZWN0ZWQgb25BY3RpdmF0ZVJlcXVlc3QobXNnOiBNZXNzYWdlKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNBdHRhY2hlZCkge1xuICAgICAgY29uc3QgaW5wdXQgPSB0aGlzLl9zZWFyY2hJbnB1dFJlZi5jdXJyZW50O1xuICAgICAgaWYgKGlucHV0KSB7XG4gICAgICAgIGlucHV0LmZvY3VzKCk7XG4gICAgICAgIGlucHV0LnNlbGVjdCgpO1xuICAgICAgfVxuICAgIH1cbiAgICBzdXBlci5vbkFjdGl2YXRlUmVxdWVzdChtc2cpO1xuICB9XG5cbiAgcHJpdmF0ZSBfb25TdGF0ZUNoYW5nZWQoKTogdm9pZCB7XG4gICAgaWYgKCF0aGlzLl93YXNEaXNjbGFpbWVkICYmIHRoaXMubW9kZWwuaXNEaXNjbGFpbWVkKSB7XG4gICAgICAodGhpcy5jb250ZW50IGFzIEFjY29yZGlvblBhbmVsKS5jb2xsYXBzZSgwKTtcbiAgICAgICh0aGlzLmNvbnRlbnQgYXMgQWNjb3JkaW9uUGFuZWwpLmV4cGFuZCgxKTtcbiAgICAgICh0aGlzLmNvbnRlbnQgYXMgQWNjb3JkaW9uUGFuZWwpLmV4cGFuZCgyKTtcbiAgICB9XG4gICAgdGhpcy5fd2FzRGlzY2xhaW1lZCA9IHRoaXMubW9kZWwuaXNEaXNjbGFpbWVkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRvZ2dsZSB0aGUgZm9jdXNlZCBtb2RpZmllciBiYXNlZCBvbiB0aGUgaW5wdXQgbm9kZSBmb2N1cyBzdGF0ZS5cbiAgICovXG4gIHByaXZhdGUgX3RvZ2dsZUZvY3VzZWQoKTogdm9pZCB7XG4gICAgY29uc3QgZm9jdXNlZCA9IGRvY3VtZW50LmFjdGl2ZUVsZW1lbnQgPT09IHRoaXMuX3NlYXJjaElucHV0UmVmLmN1cnJlbnQ7XG4gICAgdGhpcy50b2dnbGVDbGFzcygnbG0tbW9kLWZvY3VzZWQnLCBmb2N1c2VkKTtcbiAgfVxuXG4gIHByb3RlY3RlZCBtb2RlbDogTGlzdE1vZGVsO1xuICBwcm90ZWN0ZWQgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICBwcml2YXRlIF9zZWFyY2hJbnB1dFJlZjogUmVhY3QuUmVmT2JqZWN0PEhUTUxJbnB1dEVsZW1lbnQ+O1xuICBwcml2YXRlIF93YXNJbml0aWFsaXplZCA9IGZhbHNlO1xuICBwcml2YXRlIF93YXNEaXNjbGFpbWVkID0gdHJ1ZTtcbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==