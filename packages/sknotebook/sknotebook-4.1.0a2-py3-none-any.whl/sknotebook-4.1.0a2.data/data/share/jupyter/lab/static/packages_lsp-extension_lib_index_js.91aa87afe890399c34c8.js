"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_lsp-extension_lib_index_js"],{

/***/ "../packages/lsp-extension/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/lsp-extension/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunningLanguageServer": () => (/* binding */ RunningLanguageServer),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/lsp */ "webpack/sharing/consume/default/@jupyterlab/lsp/@jupyterlab/lsp");
/* harmony import */ var _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/running */ "webpack/sharing/consume/default/@jupyterlab/running/@jupyterlab/running");
/* harmony import */ var _jupyterlab_running__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _renderer__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./renderer */ "../packages/lsp-extension/lib/renderer.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module lsp-extension
 */







const plugin = {
    activate,
    id: '@jupyterlab/lsp-extension:plugin',
    description: 'Provides the language server connection manager.',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator, _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.IWidgetLSPAdapterTracker],
    optional: [_jupyterlab_running__WEBPACK_IMPORTED_MODULE_1__.IRunningSessionManagers],
    provides: _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.ILSPDocumentConnectionManager,
    autoStart: true
};
const featurePlugin = {
    id: '@jupyterlab/lsp-extension:feature',
    description: 'Provides the language server feature manager.',
    activate: () => new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.FeatureManager(),
    provides: _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.ILSPFeatureManager,
    autoStart: true
};
const settingsPlugin = {
    activate: activateSettings,
    id: '@jupyterlab/lsp-extension:settings',
    description: 'Provides the language server settings.',
    requires: [_jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.ILSPDocumentConnectionManager, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_2__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.IFormRendererRegistry],
    autoStart: true
};
const codeExtractorManagerPlugin = {
    id: _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.ILSPCodeExtractorsManager.name,
    description: 'Provides the code extractor manager.',
    activate: app => {
        const extractorManager = new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.CodeExtractorsManager();
        const markdownCellExtractor = new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.TextForeignCodeExtractor({
            language: 'markdown',
            isStandalone: false,
            file_extension: 'md',
            cellType: ['markdown']
        });
        extractorManager.register(markdownCellExtractor, null);
        const rawCellExtractor = new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.TextForeignCodeExtractor({
            language: 'text',
            isStandalone: false,
            file_extension: 'txt',
            cellType: ['raw']
        });
        extractorManager.register(rawCellExtractor, null);
        return extractorManager;
    },
    provides: _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.ILSPCodeExtractorsManager,
    autoStart: true
};
/**
 * Activate the lsp plugin.
 */
function activate(app, translator, tracker, runningSessionManagers) {
    const languageServerManager = new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.LanguageServerManager({
        settings: app.serviceManager.serverSettings
    });
    const connectionManager = new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.DocumentConnectionManager({
        languageServerManager,
        adapterTracker: tracker
    });
    // Add a sessions manager if the running extension is available
    if (runningSessionManagers) {
        addRunningSessionManager(runningSessionManagers, connectionManager, translator);
    }
    return connectionManager;
}
/**
 * Activate the lsp settings plugin.
 */
function activateSettings(app, connectionManager, settingRegistry, translator, settingRendererRegistry) {
    const LANGUAGE_SERVERS = 'languageServers';
    const languageServerManager = connectionManager.languageServerManager;
    const updateOptions = (settings) => {
        const options = settings.composite;
        const languageServerSettings = (options.languageServers ||
            {});
        if (options.activate === 'on' && !languageServerManager.isEnabled) {
            languageServerManager.enable().catch(console.error);
        }
        else if (options.activate === 'off' && languageServerManager.isEnabled) {
            languageServerManager.disable();
            return;
        }
        connectionManager.initialConfigurations = languageServerSettings;
        // TODO: if priorities changed reset connections
        connectionManager.updateConfiguration(languageServerSettings);
        connectionManager.updateServerConfigurations(languageServerSettings);
        connectionManager.updateLogging(options.logAllCommunication, options.setTrace);
    };
    settingRegistry.transform(plugin.id, {
        fetch: plugin => {
            const schema = plugin.schema.properties;
            const defaultValue = {};
            languageServerManager.sessions.forEach((_, key) => {
                defaultValue[key] = { rank: 50, configuration: {} };
            });
            schema[LANGUAGE_SERVERS]['default'] = defaultValue;
            return plugin;
        },
        compose: plugin => {
            const properties = plugin.schema.properties;
            const user = plugin.data.user;
            const serverDefaultSettings = properties[LANGUAGE_SERVERS]['default'];
            const serverUserSettings = user[LANGUAGE_SERVERS];
            let serverComposite = { ...serverDefaultSettings };
            if (serverUserSettings) {
                serverComposite = { ...serverComposite, ...serverUserSettings };
            }
            const composite = {
                [LANGUAGE_SERVERS]: serverComposite
            };
            Object.entries(properties).forEach(([key, value]) => {
                if (key !== LANGUAGE_SERVERS) {
                    if (key in user) {
                        composite[key] = user[key];
                    }
                    else {
                        composite[key] = value.default;
                    }
                }
            });
            plugin.data.composite = composite;
            return plugin;
        }
    });
    languageServerManager.sessionsChanged.connect(async () => {
        await settingRegistry.load(plugin.id, true);
    });
    settingRegistry
        .load(plugin.id)
        .then(settings => {
        updateOptions(settings);
        settings.changed.connect(() => {
            updateOptions(settings);
        });
        languageServerManager.disable();
    })
        .catch((reason) => {
        console.error(reason.message);
    });
    if (settingRendererRegistry) {
        const renderer = {
            fieldRenderer: (props) => {
                return (0,_renderer__WEBPACK_IMPORTED_MODULE_6__.renderServerSetting)(props, translator);
            }
        };
        settingRendererRegistry.addRenderer(`${plugin.id}.${LANGUAGE_SERVERS}`, renderer);
    }
}
class RunningLanguageServer {
    constructor(connection, manager) {
        this._connection = new WeakSet([connection]);
        this._manager = manager;
        this._serverIdentifier = connection.serverIdentifier;
        this._serverLanguage = connection.serverLanguage;
    }
    /**
     * This is no-op because we do not do anything on server click event
     */
    open() {
        /** no-op */
    }
    icon() {
        return _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.pythonIcon;
    }
    label() {
        var _a, _b;
        return `${(_a = this._serverIdentifier) !== null && _a !== void 0 ? _a : ''} (${(_b = this._serverLanguage) !== null && _b !== void 0 ? _b : ''})`;
    }
    shutdown() {
        for (const [key, value] of this._manager.connections.entries()) {
            if (this._connection.has(value)) {
                const { uri } = this._manager.documents.get(key);
                this._manager.unregisterDocument(uri);
            }
        }
        this._manager.disconnect(this._serverIdentifier);
    }
}
/**
 * Add the running terminal manager to the running panel.
 */
function addRunningSessionManager(managers, lsManager, translator) {
    const trans = translator.load('jupyterlab');
    const signal = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_5__.Signal(lsManager);
    lsManager.connected.connect(() => signal.emit(lsManager));
    lsManager.disconnected.connect(() => signal.emit(lsManager));
    lsManager.closed.connect(() => signal.emit(lsManager));
    lsManager.documentsChanged.connect(() => signal.emit(lsManager));
    let currentRunning = [];
    managers.add({
        name: trans.__('Language servers'),
        running: () => {
            const connections = new Set([...lsManager.connections.values()]);
            currentRunning = [...connections].map(conn => new RunningLanguageServer(conn, lsManager));
            return currentRunning;
        },
        shutdownAll: () => {
            currentRunning.forEach(item => {
                item.shutdown();
            });
        },
        refreshRunning: () => {
            return void 0;
        },
        runningChanged: signal,
        shutdownLabel: trans.__('Shut Down'),
        shutdownAllLabel: trans.__('Shut Down All'),
        shutdownAllConfirmationText: trans.__('Are you sure you want to permanently shut down all running language servers?')
    });
}
const adapterTrackerPlugin = {
    id: '@jupyterlab/lsp-extension:tracker',
    description: 'Provides the tracker of `WidgetLSPAdapter`.',
    autoStart: true,
    provides: _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.IWidgetLSPAdapterTracker,
    activate: (app) => {
        return new _jupyterlab_lsp__WEBPACK_IMPORTED_MODULE_0__.WidgetLSPAdapterTracker({ shell: app.shell });
    }
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
    plugin,
    featurePlugin,
    settingsPlugin,
    codeExtractorManagerPlugin,
    adapterTrackerPlugin
]);


/***/ }),

/***/ "../packages/lsp-extension/lib/renderer.js":
/*!*************************************************!*\
  !*** ../packages/lsp-extension/lib/renderer.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "renderServerSetting": () => (/* binding */ renderServerSetting)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/polling */ "webpack/sharing/consume/default/@lumino/polling/@lumino/polling");
/* harmony import */ var _lumino_polling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_polling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.




const SETTING_NAME = 'languageServers';
const SERVER_SETTINGS = 'configuration';
/**
 * The React component of the setting field
 */
function BuildSettingForm(props) {
    const { [SERVER_SETTINGS]: serverSettingsSchema, ...otherSettingsSchema } = props.schema;
    const { [SERVER_SETTINGS]: serverSettings, serverName, ...otherSettings } = props.settings;
    const [currentServerName, setCurrentServerName] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(serverName);
    /**
     * Callback on server name field change event
     */
    const onServerNameChange = (e) => {
        props.updateSetting
            .invoke(props.serverHash, {
            serverName: e.target.value
        })
            .catch(console.error);
        setCurrentServerName(e.target.value);
    };
    const serverSettingWithType = {};
    Object.entries(serverSettings).forEach(([key, value]) => {
        const newProps = {
            property: key,
            type: typeof value,
            value
        };
        serverSettingWithType[_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4()] = newProps;
    });
    const [propertyMap, setPropertyMap] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(serverSettingWithType);
    const defaultOtherSettings = {};
    Object.entries(otherSettingsSchema).forEach(([key, value]) => {
        if (key in otherSettings) {
            defaultOtherSettings[key] = otherSettings[key];
        }
        else {
            defaultOtherSettings[key] = value['default'];
        }
    });
    const [otherSettingsComposite, setOtherSettingsComposite] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)(defaultOtherSettings);
    /**
     * Callback on additional setting field change event
     */
    const onOtherSettingsChange = (property, value, type) => {
        let settingValue = value;
        if (type === 'number') {
            settingValue = parseFloat(value);
        }
        const newProps = {
            ...otherSettingsComposite,
            [property]: settingValue
        };
        props.updateSetting.invoke(props.serverHash, newProps).catch(console.error);
        setOtherSettingsComposite(newProps);
    };
    /**
     * Callback on `Add property` button click event.
     */
    const addProperty = () => {
        const hash = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
        const newMap = {
            ...propertyMap,
            [hash]: { property: '', type: 'string', value: '' }
        };
        const payload = {};
        Object.values(newMap).forEach(value => {
            payload[value.property] = value.value;
        });
        props.updateSetting
            .invoke(props.serverHash, {
            [SERVER_SETTINGS]: payload
        })
            .catch(console.error);
        setPropertyMap(newMap);
    };
    /**
     * Callback on `Remove property` button click event.
     */
    const removeProperty = (entryHash) => {
        const newMap = {};
        Object.entries(propertyMap).forEach(([hash, value]) => {
            if (hash !== entryHash) {
                newMap[hash] = value;
            }
            const payload = {};
            Object.values(newMap).forEach(value => {
                payload[value.property] = value.value;
            });
            props.updateSetting
                .invoke(props.serverHash, {
                [SERVER_SETTINGS]: payload
            })
                .catch(console.error);
            setPropertyMap(newMap);
        });
    };
    /**
     * Save setting to the setting registry on field change event.
     */
    const setProperty = (hash, property) => {
        if (hash in propertyMap) {
            const newMap = { ...propertyMap, [hash]: property };
            const payload = {};
            Object.values(newMap).forEach(value => {
                payload[value.property] = value.value;
            });
            setPropertyMap(newMap);
            props.updateSetting
                .invoke(props.serverHash, {
                [SERVER_SETTINGS]: payload
            })
                .catch(console.error);
        }
    };
    const debouncedSetProperty = new _lumino_polling__WEBPACK_IMPORTED_MODULE_2__.Debouncer(setProperty);
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "array-item" },
        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "form-group " },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-FormGroup-content" },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-objectFieldWrapper" },
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("fieldset", null,
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "form-group small-field" },
                            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-modifiedIndicator jp-errorIndicator" }),
                            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-FormGroup-content" },
                                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("h3", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, props.trans.__('Server name:')),
                                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-inputFieldWrapper jp-FormGroup-contentItem" },
                                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { className: "form-control", type: "text", required: true, value: currentServerName, onChange: e => {
                                            onServerNameChange(e);
                                        } })),
                                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "validationErrors" },
                                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", null,
                                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("ul", { className: "error-detail bs-callout bs-callout-info" },
                                            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("li", { className: "text-danger" }, props.trans.__('is a required property'))))))),
                        Object.entries(otherSettingsSchema).map(([property, value], idx) => {
                            return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { key: `${idx}-${property}`, className: "form-group small-field" },
                                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-FormGroup-content" },
                                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("h3", { className: "jp-FormGroup-fieldLabel jp-FormGroup-contentItem" }, value.title),
                                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-inputFieldWrapper jp-FormGroup-contentItem" },
                                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { className: "form-control", placeholder: "", type: value.type, value: otherSettingsComposite[property], onChange: e => onOtherSettingsChange(property, e.target.value, value.type) })),
                                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-FormGroup-description" }, value.description),
                                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "validationErrors" }))));
                        }),
                        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("fieldset", null,
                            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("legend", null, serverSettingsSchema['title']),
                            Object.entries(propertyMap).map(([hash, property]) => {
                                return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(PropertyFrom, { key: hash, hash: hash, property: property, removeProperty: removeProperty, setProperty: debouncedSetProperty }));
                            }),
                            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("span", null, serverSettingsSchema['description'])))))),
        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-ArrayOperations" },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("button", { className: "jp-mod-styled jp-mod-reject", onClick: addProperty }, props.trans.__('Add property')),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("button", { className: "jp-mod-styled jp-mod-warn jp-FormGroup-removeButton", onClick: () => props.removeSetting(props.serverHash) }, props.trans.__('Remove server')))));
}
function PropertyFrom(props) {
    const [state, setState] = (0,react__WEBPACK_IMPORTED_MODULE_3__.useState)({ ...props.property });
    const TYPE_MAP = { string: 'text', number: 'number', boolean: 'checkbox' };
    const removeItem = () => {
        props.removeProperty(props.hash);
    };
    const changeName = (newName) => {
        const newState = { ...state, property: newName };
        props.setProperty.invoke(props.hash, newState).catch(console.error);
        setState(newState);
    };
    const changeValue = (newValue, type) => {
        let value = newValue;
        if (type === 'number') {
            value = parseFloat(newValue);
        }
        const newState = { ...state, value };
        props.setProperty.invoke(props.hash, newState).catch(console.error);
        setState(newState);
    };
    const changeType = (newType) => {
        let value;
        if (newType === 'boolean') {
            value = false;
        }
        else if (newType === 'number') {
            value = 0;
        }
        else {
            value = '';
        }
        const newState = { ...state, type: newType, value };
        setState(newState);
        props.setProperty.invoke(props.hash, newState).catch(console.error);
    };
    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { key: props.hash, className: "form-group small-field" },
        react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "jp-FormGroup-content jp-LSPExtension-FormGroup-content" },
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { className: "form-control", type: "text", required: true, placeholder: 'Property name', value: state.property, onChange: e => {
                    changeName(e.target.value);
                } }),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("select", { className: "form-control", value: state.type, onChange: e => changeType(e.target.value) },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("option", { value: "string" }, "String"),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("option", { value: "number" }, "Number"),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("option", { value: "boolean" }, "Boolean")),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("input", { className: "form-control", type: TYPE_MAP[state.type], required: false, placeholder: 'Property value', value: state.type !== 'boolean' ? state.value : undefined, checked: state.type === 'boolean' ? state.value : undefined, onChange: state.type !== 'boolean'
                    ? e => changeValue(e.target.value, state.type)
                    : e => changeValue(e.target.checked, state.type) }),
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("button", { className: "jp-mod-minimal jp-Button", onClick: removeItem },
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.closeIcon.react, null)))));
}
/**
 * React setting component
 */
class SettingRenderer extends (react__WEBPACK_IMPORTED_MODULE_3___default().Component) {
    constructor(props) {
        super(props);
        /**
         * Remove a setting item by its hash
         *
         * @param hash - hash of the item to be removed.
         */
        this.removeSetting = (hash) => {
            if (hash in this.state.items) {
                const items = {};
                for (const key in this.state.items) {
                    if (key !== hash) {
                        items[key] = this.state.items[key];
                    }
                }
                this.setState(old => {
                    return { ...old, items };
                }, () => {
                    this.saveServerSetting();
                });
            }
        };
        /**
         * Update a setting item by its hash
         *
         * @param hash - hash of the item to be updated.
         * @param newSetting - new setting value.
         */
        this.updateSetting = (hash, newSetting) => {
            if (hash in this.state.items) {
                const items = {};
                for (const key in this.state.items) {
                    if (key === hash) {
                        items[key] = { ...this.state.items[key], ...newSetting };
                    }
                    else {
                        items[key] = this.state.items[key];
                    }
                }
                this.setState(old => {
                    return { ...old, items };
                }, () => {
                    this.saveServerSetting();
                });
            }
        };
        /**
         * Add setting item to the setting component.
         */
        this.addServerSetting = () => {
            let index = 0;
            let key = 'newKey';
            while (Object.values(this.state.items)
                .map(val => val.serverName)
                .includes(key)) {
                index += 1;
                key = `newKey-${index}`;
            }
            this.setState(old => ({
                ...old,
                items: {
                    ...old.items,
                    [_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4()]: { ...this._defaultSetting, serverName: key }
                }
            }), () => {
                this.saveServerSetting();
            });
        };
        /**
         * Save the value of setting items to the setting registry.
         */
        this.saveServerSetting = () => {
            const settings = {};
            Object.values(this.state.items).forEach(item => {
                const { serverName, ...setting } = item;
                settings[serverName] = setting;
            });
            this._setting.set(SETTING_NAME, settings).catch(console.error);
        };
        this._setting = props.formContext.settings;
        this._trans = props.translator.load('jupyterlab');
        const schema = this._setting.schema['definitions'];
        this._defaultSetting = schema['languageServer']['default'];
        this._schema = schema['languageServer']['properties'];
        const title = props.schema.title;
        const desc = props.schema.description;
        const settings = props.formContext.settings;
        const compositeData = settings.get(SETTING_NAME).composite;
        let items = {};
        if (compositeData) {
            Object.entries(compositeData).forEach(([key, value]) => {
                if (value) {
                    const hash = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.UUID.uuid4();
                    items[hash] = { serverName: key, ...value };
                }
            });
        }
        this.state = { title, desc, items };
        this._debouncedUpdateSetting = new _lumino_polling__WEBPACK_IMPORTED_MODULE_2__.Debouncer(this.updateSetting.bind(this));
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_3___default().createElement("fieldset", null,
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("legend", null, this.state.title),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("p", { className: "field-description" }, this.state.desc),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", { className: "field field-array field-array-of-object" }, Object.entries(this.state.items).map(([hash, value], idx) => {
                    return (react__WEBPACK_IMPORTED_MODULE_3___default().createElement(BuildSettingForm, { key: `${idx}-${hash}`, trans: this._trans, removeSetting: this.removeSetting, updateSetting: this._debouncedUpdateSetting, serverHash: hash, settings: value, schema: this._schema }));
                })),
                react__WEBPACK_IMPORTED_MODULE_3___default().createElement("div", null,
                    react__WEBPACK_IMPORTED_MODULE_3___default().createElement("button", { style: { margin: 2 }, className: "jp-mod-styled jp-mod-reject", onClick: this.addServerSetting }, this._trans.__('Add server'))))));
    }
}
/**
 * Custom setting renderer for language server extension.
 */
function renderServerSetting(props, translator) {
    return react__WEBPACK_IMPORTED_MODULE_3___default().createElement(SettingRenderer, { ...props, translator: translator });
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbHNwLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuOTFhYTg3YWZlODkwMzk5YzM0YzguanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFzQnNCO0FBQ3VEO0FBQ2pCO0FBQ1Q7QUFNbkI7QUFFUTtBQUVNO0FBSWpELE1BQU0sTUFBTSxHQUF5RDtJQUNuRSxRQUFRO0lBQ1IsRUFBRSxFQUFFLGtDQUFrQztJQUN0QyxXQUFXLEVBQUUsa0RBQWtEO0lBQy9ELFFBQVEsRUFBRSxDQUFDLGdFQUFXLEVBQUUscUVBQXdCLENBQUM7SUFDakQsUUFBUSxFQUFFLENBQUMsd0VBQXVCLENBQUM7SUFDbkMsUUFBUSxFQUFFLDBFQUE2QjtJQUN2QyxTQUFTLEVBQUUsSUFBSTtDQUNoQixDQUFDO0FBRUYsTUFBTSxhQUFhLEdBQThDO0lBQy9ELEVBQUUsRUFBRSxtQ0FBbUM7SUFDdkMsV0FBVyxFQUFFLCtDQUErQztJQUM1RCxRQUFRLEVBQUUsR0FBRyxFQUFFLENBQUMsSUFBSSwyREFBYyxFQUFFO0lBQ3BDLFFBQVEsRUFBRSwrREFBa0I7SUFDNUIsU0FBUyxFQUFFLElBQUk7Q0FDaEIsQ0FBQztBQUVGLE1BQU0sY0FBYyxHQUFnQztJQUNsRCxRQUFRLEVBQUUsZ0JBQWdCO0lBQzFCLEVBQUUsRUFBRSxvQ0FBb0M7SUFDeEMsV0FBVyxFQUFFLHdDQUF3QztJQUNyRCxRQUFRLEVBQUUsQ0FBQywwRUFBNkIsRUFBRSx5RUFBZ0IsRUFBRSxnRUFBVyxDQUFDO0lBQ3hFLFFBQVEsRUFBRSxDQUFDLDRFQUFxQixDQUFDO0lBQ2pDLFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRixNQUFNLDBCQUEwQixHQUM5QjtJQUNFLEVBQUUsRUFBRSwyRUFBOEI7SUFDbEMsV0FBVyxFQUFFLHNDQUFzQztJQUNuRCxRQUFRLEVBQUUsR0FBRyxDQUFDLEVBQUU7UUFDZCxNQUFNLGdC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LENBQUMsRUFBRSxHQUFHLEVBQUUsRUFBRTtvQkFDM0QsT0FBTyxDQUNMLDJEQUFDLGdCQUFnQixJQUNmLEdBQUcsRUFBRSxHQUFHLEdBQUcsSUFBSSxJQUFJLEVBQUUsRUFDckIsS0FBSyxFQUFFLElBQUksQ0FBQyxNQUFNLEVBQ2xCLGFBQWEsRUFBRSxJQUFJLENBQUMsYUFBYSxFQUNqQyxhQUFhLEVBQUUsSUFBSSxDQUFDLHVCQUF1QixFQUMzQyxVQUFVLEVBQUUsSUFBSSxFQUNoQixRQUFRLEVBQUUsS0FBSyxFQUNmLE1BQU0sRUFBRSxJQUFJLENBQUMsT0FBTyxHQUNwQixDQUNILENBQUM7Z0JBQ0osQ0FBQyxDQUFDLENBQ0U7Z0JBQ047b0JBQ0UsdUVBQ0UsS0FBSyxFQUFFLEVBQUUsTUFBTSxFQUFFLENBQUMsRUFBRSxFQUNwQixTQUFTLEVBQUMsNkJBQTZCLEVBQ3ZDLE9BQU8sRUFBRSxJQUFJLENBQUMsZ0JBQWdCLElBRTdCLElBQUksQ0FBQyxNQUFNLENBQUMsRUFBRSxDQUFDLFlBQVksQ0FBQyxDQUN0QixDQUNMLENBQ0csQ0FDUCxDQUNQLENBQUM7SUFDSixDQUFDO0NBMkJGO0FBRUQ7O0dBRUc7QUFDSSxTQUFTLG1CQUFtQixDQUNqQyxLQUFpQixFQUNqQixVQUF1QjtJQUV2QixPQUFPLDJEQUFDLGVBQWUsT0FBSyxLQUFLLEVBQUUsVUFBVSxFQUFFLFVBQVUsR0FBSSxDQUFDO0FBQ2hFLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbHNwLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2xzcC1leHRlbnNpb24vc3JjL3JlbmRlcmVyLnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBsc3AtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW4sXG4gIExhYlNoZWxsXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7XG4gIENvZGVFeHRyYWN0b3JzTWFuYWdlcixcbiAgRG9jdW1lbnRDb25uZWN0aW9uTWFuYWdlcixcbiAgRmVhdHVyZU1hbmFnZXIsXG4gIElMU1BDb2RlRXh0cmFjdG9yc01hbmFnZXIsXG4gIElMU1BDb25uZWN0aW9uLFxuICBJTFNQRG9jdW1lbnRDb25uZWN0aW9uTWFuYWdlcixcbiAgSUxTUEZlYXR1cmVNYW5hZ2VyLFxuICBJV2lkZ2V0TFNQQWRhcHRlclRyYWNrZXIsXG4gIExhbmd1YWdlU2VydmVyTWFuYWdlcixcbiAgTGFuZ3VhZ2VTZXJ2ZXJzRXhwZXJpbWVudGFsLFxuICBUZXh0Rm9yZWlnbkNvZGVFeHRyYWN0b3IsXG4gIFRMYW5ndWFnZVNlcnZlckNvbmZpZ3VyYXRpb25zLFxuICBUTGFuZ3VhZ2VTZXJ2ZXJJZCxcbiAgV2lkZ2V0TFNQQWRhcHRlclRyYWNrZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvbHNwJztcbmltcG9ydCB7IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzLCBJUnVubmluZ1Nlc3Npb25zIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcnVubmluZyc7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgSUZvcm1SZW5kZXJlcixcbiAgSUZvcm1SZW5kZXJlclJlZ2lzdHJ5LFxuICBMYWJJY29uLFxuICBweXRob25JY29uXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgUGFydGlhbEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbmltcG9ydCB7IHJlbmRlclNlcnZlclNldHRpbmcgfSBmcm9tICcuL3JlbmRlcmVyJztcblxuaW1wb3J0IHR5cGUgeyBGaWVsZFByb3BzIH0gZnJvbSAnQHJqc2YvdXRpbHMnO1xuXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTFNQRG9jdW1lbnRDb25uZWN0aW9uTWFuYWdlcj4gPSB7XG4gIGFjdGl2YXRlLFxuICBpZDogJ0BqdXB5dGVybGFiL2xzcC1leHRlbnNpb246cGx1Z2luJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgbGFuZ3VhZ2Ugc2VydmVyIGNvbm5lY3Rpb24gbWFuYWdlci4nLFxuICByZXF1aXJlczogW0lUcmFuc2xhdG9yLCBJV2lkZ2V0TFNQQWRhcHRlclRyYWNrZXJdLFxuICBvcHRpb25hbDogW0lSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzXSxcbiAgcHJvdmlkZXM6IElMU1BEb2N1bWVudENvbm5lY3Rpb25NYW5hZ2VyLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbmNvbnN0IGZlYXR1cmVQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTFNQRmVhdHVyZU1hbmFnZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2xzcC1leHRlbnNpb246ZmVhdHVyZScsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGxhbmd1YWdlIHNlcnZlciBmZWF0dXJlIG1hbmFnZXIuJyxcbiAgYWN0aXZhdGU6ICgpID0+IG5ldyBGZWF0dXJlTWFuYWdlcigpLFxuICBwcm92aWRlczogSUxTUEZlYXR1cmVNYW5hZ2VyLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbmNvbnN0IHNldHRpbmdzUGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGFjdGl2YXRlOiBhY3RpdmF0ZVNldHRpbmdzLFxuICBpZDogJ0BqdXB5dGVybGFiL2xzcC1leHRlbnNpb246c2V0dGluZ3MnLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBsYW5ndWFnZSBzZXJ2ZXIgc2V0dGluZ3MuJyxcbiAgcmVxdWlyZXM6IFtJTFNQRG9jdW1lbnRDb25uZWN0aW9uTWFuYWdlciwgSVNldHRpbmdSZWdpc3RyeSwgSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lGb3JtUmVuZGVyZXJSZWdpc3RyeV0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuY29uc3QgY29kZUV4dHJhY3Rvck1hbmFnZXJQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTFNQQ29kZUV4dHJhY3RvcnNNYW5hZ2VyPiA9XG4gIHtcbiAgICBpZDogSUxTUENvZGVFeHRyYWN0b3JzTWFuYWdlci5uYW1lLFxuICAgIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIGNvZGUgZXh0cmFjdG9yIG1hbmFnZXIuJyxcbiAgICBhY3RpdmF0ZTogYXBwID0+IHtcbiAgICAgIGNvbnN0IGV4dHJhY3Rvck1hbmFnZXIgPSBuZXcgQ29kZUV4dHJhY3RvcnNNYW5hZ2VyKCk7XG5cbiAgICAgIGNvbnN0IG1hcmtkb3duQ2VsbEV4dHJhY3RvciA9IG5ldyBUZXh0Rm9yZWlnbkNvZGVFeHRyYWN0b3Ioe1xuICAgICAgICBsYW5ndWFnZTogJ21hcmtkb3duJyxcbiAgICAgICAgaXNTdGFuZGFsb25lOiBmYWxzZSxcbiAgICAgICAgZmlsZV9leHRlbnNpb246ICdtZCcsXG4gICAgICAgIGNlbGxUeXBlOiBbJ21hcmtkb3duJ11cbiAgICAgIH0pO1xuICAgICAgZXh0cmFjdG9yTWFuYWdlci5yZWdpc3RlcihtYXJrZG93bkNlbGxFeHRyYWN0b3IsIG51bGwpO1xuICAgICAgY29uc3QgcmF3Q2VsbEV4dHJhY3RvciA9IG5ldyBUZXh0Rm9yZWlnbkNvZGVFeHRyYWN0b3Ioe1xuICAgICAgICBsYW5ndWFnZTogJ3RleHQnLFxuICAgICAgICBpc1N0YW5kYWxvbmU6IGZhbHNlLFxuICAgICAgICBmaWxlX2V4dGVuc2lvbjogJ3R4dCcsXG4gICAgICAgIGNlbGxUeXBlOiBbJ3JhdyddXG4gICAgICB9KTtcbiAgICAgIGV4dHJhY3Rvck1hbmFnZXIucmVnaXN0ZXIocmF3Q2VsbEV4dHJhY3RvciwgbnVsbCk7XG4gICAgICByZXR1cm4gZXh0cmFjdG9yTWFuYWdlcjtcbiAgICB9LFxuICAgIHByb3ZpZGVzOiBJTFNQQ29kZUV4dHJhY3RvcnNNYW5hZ2VyLFxuICAgIGF1dG9TdGFydDogdHJ1ZVxuICB9O1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBsc3AgcGx1Z2luLlxuICovXG5mdW5jdGlvbiBhY3RpdmF0ZShcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICB0cmFja2VyOiBJV2lkZ2V0TFNQQWRhcHRlclRyYWNrZXIsXG4gIHJ1bm5pbmdTZXNzaW9uTWFuYWdlcnM6IElSdW5uaW5nU2Vzc2lvbk1hbmFnZXJzIHwgbnVsbFxuKTogSUxTUERvY3VtZW50Q29ubmVjdGlvbk1hbmFnZXIge1xuICBjb25zdCBsYW5ndWFnZVNlcnZlck1hbmFnZXIgPSBuZXcgTGFuZ3VhZ2VTZXJ2ZXJNYW5hZ2VyKHtcbiAgICBzZXR0aW5nczogYXBwLnNlcnZpY2VNYW5hZ2VyLnNlcnZlclNldHRpbmdzXG4gIH0pO1xuICBjb25zdCBjb25uZWN0aW9uTWFuYWdlciA9IG5ldyBEb2N1bWVudENvbm5lY3Rpb25NYW5hZ2VyKHtcbiAgICBsYW5ndWFnZVNlcnZlck1hbmFnZXIsXG4gICAgYWRhcHRlclRyYWNrZXI6IHRyYWNrZXJcbiAgfSk7XG5cbiAgLy8gQWRkIGEgc2Vzc2lvbnMgbWFuYWdlciBpZiB0aGUgcnVubmluZyBleHRlbnNpb24gaXMgYXZhaWxhYmxlXG4gIGlmIChydW5uaW5nU2Vzc2lvbk1hbmFnZXJzKSB7XG4gICAgYWRkUnVubmluZ1Nlc3Npb25NYW5hZ2VyKFxuICAgICAgcnVubmluZ1Nlc3Npb25NYW5hZ2VycyxcbiAgICAgIGNvbm5lY3Rpb25NYW5hZ2VyLFxuICAgICAgdHJhbnNsYXRvclxuICAgICk7XG4gIH1cblxuICByZXR1cm4gY29ubmVjdGlvbk1hbmFnZXI7XG59XG5cbi8qKlxuICogQWN0aXZhdGUgdGhlIGxzcCBzZXR0aW5ncyBwbHVnaW4uXG4gKi9cbmZ1bmN0aW9uIGFjdGl2YXRlU2V0dGluZ3MoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBjb25uZWN0aW9uTWFuYWdlcjogSUxTUERvY3VtZW50Q29ubmVjdGlvbk1hbmFnZXIsXG4gIHNldHRpbmdSZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IsXG4gIHNldHRpbmdSZW5kZXJlclJlZ2lzdHJ5OiBJRm9ybVJlbmRlcmVyUmVnaXN0cnkgfCBudWxsXG4pOiB2b2lkIHtcbiAgY29uc3QgTEFOR1VBR0VfU0VSVkVSUyA9ICdsYW5ndWFnZVNlcnZlcnMnO1xuICBjb25zdCBsYW5ndWFnZVNlcnZlck1hbmFnZXIgPSBjb25uZWN0aW9uTWFuYWdlci5sYW5ndWFnZVNlcnZlck1hbmFnZXI7XG5cbiAgY29uc3QgdXBkYXRlT3B0aW9ucyA9IChzZXR0aW5nczogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpID0+IHtcbiAgICBjb25zdCBvcHRpb25zID0gc2V0dGluZ3MuY29tcG9zaXRlIGFzIFJlcXVpcmVkPExhbmd1YWdlU2VydmVyc0V4cGVyaW1lbnRhbD47XG4gICAgY29uc3QgbGFuZ3VhZ2VTZXJ2ZXJTZXR0aW5ncyA9IChvcHRpb25zLmxhbmd1YWdlU2VydmVycyB8fFxuICAgICAge30pIGFzIFRMYW5ndWFnZVNlcnZlckNvbmZpZ3VyYXRpb25zO1xuICAgIGlmIChvcHRpb25zLmFjdGl2YXRlID09PSAnb24nICYmICFsYW5ndWFnZVNlcnZlck1hbmFnZXIuaXNFbmFibGVkKSB7XG4gICAgICBsYW5ndWFnZVNlcnZlck1hbmFnZXIuZW5hYmxlKCkuY2F0Y2goY29uc29sZS5lcnJvcik7XG4gICAgfSBlbHNlIGlmIChvcHRpb25zLmFjdGl2YXRlID09PSAnb2ZmJyAmJiBsYW5ndWFnZVNlcnZlck1hbmFnZXIuaXNFbmFibGVkKSB7XG4gICAgICBsYW5ndWFnZVNlcnZlck1hbmFnZXIuZGlzYWJsZSgpO1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25uZWN0aW9uTWFuYWdlci5pbml0aWFsQ29uZmlndXJhdGlvbnMgPSBsYW5ndWFnZVNlcnZlclNldHRpbmdzO1xuICAgIC8vIFRPRE86IGlmIHByaW9yaXRpZXMgY2hhbmdlZCByZXNldCBjb25uZWN0aW9uc1xuICAgIGNvbm5lY3Rpb25NYW5hZ2VyLnVwZGF0ZUNvbmZpZ3VyYXRpb24obGFuZ3VhZ2VTZXJ2ZXJTZXR0aW5ncyk7XG4gICAgY29ubmVjdGlvbk1hbmFnZXIudXBkYXRlU2VydmVyQ29uZmlndXJhdGlvbnMobGFuZ3VhZ2VTZXJ2ZXJTZXR0aW5ncyk7XG4gICAgY29ubmVjdGlvbk1hbmFnZXIudXBkYXRlTG9nZ2luZyhcbiAgICAgIG9wdGlvbnMubG9nQWxsQ29tbXVuaWNhdGlvbixcbiAgICAgIG9wdGlvbnMuc2V0VHJhY2VcbiAgICApO1xuICB9O1xuXG4gIHNldHRpbmdSZWdpc3RyeS50cmFuc2Zvcm0ocGx1Z2luLmlkLCB7XG4gICAgZmV0Y2g6IHBsdWdpbiA9PiB7XG4gICAgICBjb25zdCBzY2hlbWEgPSBwbHVnaW4uc2NoZW1hLnByb3BlcnRpZXMhO1xuICAgICAgY29uc3QgZGVmYXVsdFZhbHVlOiB7IFtrZXk6IHN0cmluZ106IGFueSB9ID0ge307XG4gICAgICBsYW5ndWFnZVNlcnZlck1hbmFnZXIuc2Vzc2lvbnMuZm9yRWFjaCgoXywga2V5KSA9PiB7XG4gICAgICAgIGRlZmF1bHRWYWx1ZVtrZXldID0geyByYW5rOiA1MCwgY29uZmlndXJhdGlvbjoge30gfTtcbiAgICAgIH0pO1xuXG4gICAgICBzY2hlbWFbTEFOR1VBR0VfU0VSVkVSU11bJ2RlZmF1bHQnXSA9IGRlZmF1bHRWYWx1ZTtcbiAgICAgIHJldHVybiBwbHVnaW47XG4gICAgfSxcbiAgICBjb21wb3NlOiBwbHVnaW4gPT4ge1xuICAgICAgY29uc3QgcHJvcGVydGllcyA9IHBsdWdpbi5zY2hlbWEucHJvcGVydGllcyE7XG4gICAgICBjb25zdCB1c2VyID0gcGx1Z2luLmRhdGEudXNlcjtcblxuICAgICAgY29uc3Qgc2VydmVyRGVmYXVsdFNldHRpbmdzID0gcHJvcGVydGllc1tMQU5HVUFHRV9TRVJWRVJTXVtcbiAgICAgICAgJ2RlZmF1bHQnXG4gICAgICBdIGFzIFBhcnRpYWxKU09OT2JqZWN0O1xuICAgICAgY29uc3Qgc2VydmVyVXNlclNldHRpbmdzID0gdXNlcltMQU5HVUFHRV9TRVJWRVJTXSBhc1xuICAgICAgICB8IFBhcnRpYWxKU09OT2JqZWN0XG4gICAgICAgIHwgdW5kZWZpbmVkO1xuICAgICAgbGV0IHNlcnZlckNvbXBvc2l0ZSA9IHsgLi4uc2VydmVyRGVmYXVsdFNldHRpbmdzIH07XG4gICAgICBpZiAoc2VydmVyVXNlclNldHRpbmdzKSB7XG4gICAgICAgIHNlcnZlckNvbXBvc2l0ZSA9IHsgLi4uc2VydmVyQ29tcG9zaXRlLCAuLi5zZXJ2ZXJVc2VyU2V0dGluZ3MgfTtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGNvbXBvc2l0ZTogeyBba2V5OiBzdHJpbmddOiBhbnkgfSA9IHtcbiAgICAgICAgW0xBTkdVQUdFX1NFUlZFUlNdOiBzZXJ2ZXJDb21wb3NpdGVcbiAgICAgIH07XG4gICAgICBPYmplY3QuZW50cmllcyhwcm9wZXJ0aWVzKS5mb3JFYWNoKChba2V5LCB2YWx1ZV0pID0+IHtcbiAgICAgICAgaWYgKGtleSAhPT0gTEFOR1VBR0VfU0VSVkVSUykge1xuICAgICAgICAgIGlmIChrZXkgaW4gdXNlcikge1xuICAgICAgICAgICAgY29tcG9zaXRlW2tleV0gPSB1c2VyW2tleV07XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIGNvbXBvc2l0ZVtrZXldID0gdmFsdWUuZGVmYXVsdDtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0pO1xuICAgICAgcGx1Z2luLmRhdGEuY29tcG9zaXRlID0gY29tcG9zaXRlO1xuICAgICAgcmV0dXJuIHBsdWdpbjtcbiAgICB9XG4gIH0pO1xuICBsYW5ndWFnZVNlcnZlck1hbmFnZXIuc2Vzc2lvbnNDaGFuZ2VkLmNvbm5lY3QoYXN5bmMgKCkgPT4ge1xuICAgIGF3YWl0IHNldHRpbmdSZWdpc3RyeS5sb2FkKHBsdWdpbi5pZCwgdHJ1ZSk7XG4gIH0pO1xuXG4gIHNldHRpbmdSZWdpc3RyeVxuICAgIC5sb2FkKHBsdWdpbi5pZClcbiAgICAudGhlbihzZXR0aW5ncyA9PiB7XG4gICAgICB1cGRhdGVPcHRpb25zKHNldHRpbmdzKTtcbiAgICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgIHVwZGF0ZU9wdGlvbnMoc2V0dGluZ3MpO1xuICAgICAgfSk7XG4gICAgICBsYW5ndWFnZVNlcnZlck1hbmFnZXIuZGlzYWJsZSgpO1xuICAgIH0pXG4gICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICBjb25zb2xlLmVycm9yKHJlYXNvbi5tZXNzYWdlKTtcbiAgICB9KTtcblxuICBpZiAoc2V0dGluZ1JlbmRlcmVyUmVnaXN0cnkpIHtcbiAgICBjb25zdCByZW5kZXJlcjogSUZvcm1SZW5kZXJlciA9IHtcbiAgICAgIGZpZWxkUmVuZGVyZXI6IChwcm9wczogRmllbGRQcm9wcykgPT4ge1xuICAgICAgICByZXR1cm4gcmVuZGVyU2VydmVyU2V0dGluZyhwcm9wcywgdHJhbnNsYXRvcik7XG4gICAgICB9XG4gICAgfTtcbiAgICBzZXR0aW5nUmVuZGVyZXJSZWdpc3RyeS5hZGRSZW5kZXJlcihcbiAgICAgIGAke3BsdWdpbi5pZH0uJHtMQU5HVUFHRV9TRVJWRVJTfWAsXG4gICAgICByZW5kZXJlclxuICAgICk7XG4gIH1cbn1cblxuZXhwb3J0IGNsYXNzIFJ1bm5pbmdMYW5ndWFnZVNlcnZlciBpbXBsZW1lbnRzIElSdW5uaW5nU2Vzc2lvbnMuSVJ1bm5pbmdJdGVtIHtcbiAgY29uc3RydWN0b3IoXG4gICAgY29ubmVjdGlvbjogSUxTUENvbm5lY3Rpb24sXG4gICAgbWFuYWdlcjogSUxTUERvY3VtZW50Q29ubmVjdGlvbk1hbmFnZXJcbiAgKSB7XG4gICAgdGhpcy5fY29ubmVjdGlvbiA9IG5ldyBXZWFrU2V0KFtjb25uZWN0aW9uXSk7XG4gICAgdGhpcy5fbWFuYWdlciA9IG1hbmFnZXI7XG4gICAgdGhpcy5fc2VydmVySWRlbnRpZmllciA9IGNvbm5lY3Rpb24uc2VydmVySWRlbnRpZmllcjtcbiAgICB0aGlzLl9zZXJ2ZXJMYW5ndWFnZSA9IGNvbm5lY3Rpb24uc2VydmVyTGFuZ3VhZ2U7XG4gIH1cbiAgLyoqXG4gICAqIFRoaXMgaXMgbm8tb3AgYmVjYXVzZSB3ZSBkbyBub3QgZG8gYW55dGhpbmcgb24gc2VydmVyIGNsaWNrIGV2ZW50XG4gICAqL1xuICBvcGVuKCk6IHZvaWQge1xuICAgIC8qKiBuby1vcCAqL1xuICB9XG4gIGljb24oKTogTGFiSWNvbiB7XG4gICAgcmV0dXJuIHB5dGhvbkljb247XG4gIH1cbiAgbGFiZWwoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gYCR7dGhpcy5fc2VydmVySWRlbnRpZmllciA/PyAnJ30gKCR7dGhpcy5fc2VydmVyTGFuZ3VhZ2UgPz8gJyd9KWA7XG4gIH1cbiAgc2h1dGRvd24oKTogdm9pZCB7XG4gICAgZm9yIChjb25zdCBba2V5LCB2YWx1ZV0gb2YgdGhpcy5fbWFuYWdlci5jb25uZWN0aW9ucy5lbnRyaWVzKCkpIHtcbiAgICAgIGlmICh0aGlzLl9jb25uZWN0aW9uLmhhcyh2YWx1ZSkpIHtcbiAgICAgICAgY29uc3QgeyB1cmkgfSA9IHRoaXMuX21hbmFnZXIuZG9jdW1lbnRzLmdldChrZXkpITtcbiAgICAgICAgdGhpcy5fbWFuYWdlci51bnJlZ2lzdGVyRG9jdW1lbnQodXJpKTtcbiAgICAgIH1cbiAgICB9XG4gICAgdGhpcy5fbWFuYWdlci5kaXNjb25uZWN0KHRoaXMuX3NlcnZlcklkZW50aWZpZXIgYXMgVExhbmd1YWdlU2VydmVySWQpO1xuICB9XG4gIHByaXZhdGUgX2Nvbm5lY3Rpb246IFdlYWtTZXQ8SUxTUENvbm5lY3Rpb24+O1xuICBwcml2YXRlIF9tYW5hZ2VyOiBJTFNQRG9jdW1lbnRDb25uZWN0aW9uTWFuYWdlcjtcbiAgcHJpdmF0ZSBfc2VydmVySWRlbnRpZmllcjogc3RyaW5nIHwgdW5kZWZpbmVkO1xuICBwcml2YXRlIF9zZXJ2ZXJMYW5ndWFnZTogc3RyaW5nIHwgdW5kZWZpbmVkO1xufVxuXG4vKipcbiAqIEFkZCB0aGUgcnVubmluZyB0ZXJtaW5hbCBtYW5hZ2VyIHRvIHRoZSBydW5uaW5nIHBhbmVsLlxuICovXG5mdW5jdGlvbiBhZGRSdW5uaW5nU2Vzc2lvbk1hbmFnZXIoXG4gIG1hbmFnZXJzOiBJUnVubmluZ1Nlc3Npb25NYW5hZ2VycyxcbiAgbHNNYW5hZ2VyOiBJTFNQRG9jdW1lbnRDb25uZWN0aW9uTWFuYWdlcixcbiAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3Jcbikge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBzaWduYWwgPSBuZXcgU2lnbmFsPGFueSwgYW55Pihsc01hbmFnZXIpO1xuICBsc01hbmFnZXIuY29ubmVjdGVkLmNvbm5lY3QoKCkgPT4gc2lnbmFsLmVtaXQobHNNYW5hZ2VyKSk7XG4gIGxzTWFuYWdlci5kaXNjb25uZWN0ZWQuY29ubmVjdCgoKSA9PiBzaWduYWwuZW1pdChsc01hbmFnZXIpKTtcbiAgbHNNYW5hZ2VyLmNsb3NlZC5jb25uZWN0KCgpID0+IHNpZ25hbC5lbWl0KGxzTWFuYWdlcikpO1xuICBsc01hbmFnZXIuZG9jdW1lbnRzQ2hhbmdlZC5jb25uZWN0KCgpID0+IHNpZ25hbC5lbWl0KGxzTWFuYWdlcikpO1xuICBsZXQgY3VycmVudFJ1bm5pbmc6IFJ1bm5pbmdMYW5ndWFnZVNlcnZlcltdID0gW107XG4gIG1hbmFnZXJzLmFkZCh7XG4gICAgbmFtZTogdHJhbnMuX18oJ0xhbmd1YWdlIHNlcnZlcnMnKSxcbiAgICBydW5uaW5nOiAoKSA9PiB7XG4gICAgICBjb25zdCBjb25uZWN0aW9ucyA9IG5ldyBTZXQoWy4uLmxzTWFuYWdlci5jb25uZWN0aW9ucy52YWx1ZXMoKV0pO1xuXG4gICAgICBjdXJyZW50UnVubmluZyA9IFsuLi5jb25uZWN0aW9uc10ubWFwKFxuICAgICAgICBjb25uID0+IG5ldyBSdW5uaW5nTGFuZ3VhZ2VTZXJ2ZXIoY29ubiwgbHNNYW5hZ2VyKVxuICAgICAgKTtcbiAgICAgIHJldHVybiBjdXJyZW50UnVubmluZztcbiAgICB9LFxuICAgIHNodXRkb3duQWxsOiAoKSA9PiB7XG4gICAgICBjdXJyZW50UnVubmluZy5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgICBpdGVtLnNodXRkb3duKCk7XG4gICAgICB9KTtcbiAgICB9LFxuICAgIHJlZnJlc2hSdW5uaW5nOiAoKSA9PiB7XG4gICAgICByZXR1cm4gdm9pZCAwO1xuICAgIH0sXG4gICAgcnVubmluZ0NoYW5nZWQ6IHNpZ25hbCxcbiAgICBzaHV0ZG93bkxhYmVsOiB0cmFucy5fXygnU2h1dCBEb3duJyksXG4gICAgc2h1dGRvd25BbGxMYWJlbDogdHJhbnMuX18oJ1NodXQgRG93biBBbGwnKSxcbiAgICBzaHV0ZG93bkFsbENvbmZpcm1hdGlvblRleHQ6IHRyYW5zLl9fKFxuICAgICAgJ0FyZSB5b3Ugc3VyZSB5b3Ugd2FudCB0byBwZXJtYW5lbnRseSBzaHV0IGRvd24gYWxsIHJ1bm5pbmcgbGFuZ3VhZ2Ugc2VydmVycz8nXG4gICAgKVxuICB9KTtcbn1cblxuY29uc3QgYWRhcHRlclRyYWNrZXJQbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJV2lkZ2V0TFNQQWRhcHRlclRyYWNrZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL2xzcC1leHRlbnNpb246dHJhY2tlcicsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIHRyYWNrZXIgb2YgYFdpZGdldExTUEFkYXB0ZXJgLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcHJvdmlkZXM6IElXaWRnZXRMU1BBZGFwdGVyVHJhY2tlcixcbiAgYWN0aXZhdGU6IChhcHA6IEp1cHl0ZXJGcm9udEVuZDxMYWJTaGVsbD4pOiBJV2lkZ2V0TFNQQWRhcHRlclRyYWNrZXIgPT4ge1xuICAgIHJldHVybiBuZXcgV2lkZ2V0TFNQQWRhcHRlclRyYWNrZXIoeyBzaGVsbDogYXBwLnNoZWxsIH0pO1xuICB9XG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2luIGFzIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IFtcbiAgcGx1Z2luLFxuICBmZWF0dXJlUGx1Z2luLFxuICBzZXR0aW5nc1BsdWdpbixcbiAgY29kZUV4dHJhY3Rvck1hbmFnZXJQbHVnaW4sXG4gIGFkYXB0ZXJUcmFja2VyUGx1Z2luXG5dO1xuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBUcmFuc2xhdGlvbkJ1bmRsZSB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IGNsb3NlSWNvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuaW1wb3J0IHsgVVVJRCB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERlYm91bmNlciB9IGZyb20gJ0BsdW1pbm8vcG9sbGluZyc7XG5pbXBvcnQgUmVhY3QsIHsgdXNlU3RhdGUgfSBmcm9tICdyZWFjdCc7XG5cbmltcG9ydCB0eXBlIHsgRmllbGRQcm9wcyB9IGZyb20gJ0ByanNmL3V0aWxzJztcbnR5cGUgVERpY3QgPSB7IFtrZXk6IHN0cmluZ106IGFueSB9O1xuXG5pbnRlcmZhY2UgSVNldHRpbmdQcm9wZXJ0eU1hcCB7XG4gIFtrZXk6IHN0cmluZ106IElTZXR0aW5nUHJvcGVydHk7XG59XG5pbnRlcmZhY2UgSVNldHRpbmdQcm9wZXJ0eSB7XG4gIC8qKlxuICAgKiBOYW1lIG9mIHNldHRpbmcgcHJvcGVydHlcbiAgICovXG4gIHByb3BlcnR5OiBzdHJpbmc7XG4gIC8qKlxuICAgKiBUeXBlIG9mIHNldHRpbmcgcHJvcGVydHlcbiAgICovXG4gIHR5cGU6ICdib29sZWFuJyB8ICdzdHJpbmcnIHwgJ251bWJlcic7XG4gIC8qKlxuICAgKiBWYWx1ZSBvZiBzZXR0aW5nIHByb3BlcnR5XG4gICAqL1xuICB2YWx1ZTogYW55O1xufVxuY29uc3QgU0VUVElOR19OQU1FID0gJ2xhbmd1YWdlU2VydmVycyc7XG5jb25zdCBTRVJWRVJfU0VUVElOR1MgPSAnY29uZmlndXJhdGlvbic7XG5cbmludGVyZmFjZSBJU2V0dGluZ0Zvcm1Qcm9wcyB7XG4gIC8qKlxuICAgKiBUaGUgdHJhbnNsYXRpb24gYnVuZGxlLlxuICAgKi9cbiAgdHJhbnM6IFRyYW5zbGF0aW9uQnVuZGxlO1xuXG4gIC8qKlxuICAgKiBDYWxsYmFjayB0byByZW1vdmUgc2V0dGluZyBpdGVtLlxuICAgKi9cbiAgcmVtb3ZlU2V0dGluZzogKGtleTogc3RyaW5nKSA9PiB2b2lkO1xuXG4gIC8qKlxuICAgKiBDYWxsYmFjayB0byB1cGRhdGUgdGhlIHNldHRpbmcgaXRlbS5cbiAgICovXG4gIHVwZGF0ZVNldHRpbmc6IERlYm91bmNlcjx2b2lkLCBhbnksIFtoYXNoOiBzdHJpbmcsIG5ld1NldHRpbmc6IFREaWN0XT47XG5cbiAgLyoqXG4gICAqIEhhc2ggdG8gZGlmZmVyZW50aWF0ZSB0aGUgc2V0dGluZyBmaWVsZHMuXG4gICAqL1xuICBzZXJ2ZXJIYXNoOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqICBTZXR0aW5nIHZhbHVlLlxuICAgKi9cbiAgc2V0dGluZ3M6IFREaWN0O1xuXG4gIC8qKlxuICAgKiBTZXR0aW5nIHNjaGVtYS5cbiAgICovXG4gIHNjaGVtYTogVERpY3Q7XG59XG5cbi8qKlxuICogVGhlIFJlYWN0IGNvbXBvbmVudCBvZiB0aGUgc2V0dGluZyBmaWVsZFxuICovXG5mdW5jdGlvbiBCdWlsZFNldHRpbmdGb3JtKHByb3BzOiBJU2V0dGluZ0Zvcm1Qcm9wcyk6IEpTWC5FbGVtZW50IHtcbiAgY29uc3QgeyBbU0VSVkVSX1NFVFRJTkdTXTogc2VydmVyU2V0dGluZ3NTY2hlbWEsIC4uLm90aGVyU2V0dGluZ3NTY2hlbWEgfSA9XG4gICAgcHJvcHMuc2NoZW1hO1xuICBjb25zdCB7XG4gICAgW1NFUlZFUl9TRVRUSU5HU106IHNlcnZlclNldHRpbmdzLFxuICAgIHNlcnZlck5hbWUsXG4gICAgLi4ub3RoZXJTZXR0aW5nc1xuICB9ID0gcHJvcHMuc2V0dGluZ3M7XG5cbiAgY29uc3QgW2N1cnJlbnRTZXJ2ZXJOYW1lLCBzZXRDdXJyZW50U2VydmVyTmFtZV0gPVxuICAgIHVzZVN0YXRlPHN0cmluZz4oc2VydmVyTmFtZSk7XG5cbiAgLyoqXG4gICAqIENhbGxiYWNrIG9uIHNlcnZlciBuYW1lIGZpZWxkIGNoYW5nZSBldmVudFxuICAgKi9cbiAgY29uc3Qgb25TZXJ2ZXJOYW1lQ2hhbmdlID0gKGU6IFJlYWN0LkNoYW5nZUV2ZW50PEhUTUxJbnB1dEVsZW1lbnQ+KSA9PiB7XG4gICAgcHJvcHMudXBkYXRlU2V0dGluZ1xuICAgICAgLmludm9rZShwcm9wcy5zZXJ2ZXJIYXNoLCB7XG4gICAgICAgIHNlcnZlck5hbWU6IGUudGFyZ2V0LnZhbHVlXG4gICAgICB9KVxuICAgICAgLmNhdGNoKGNvbnNvbGUuZXJyb3IpO1xuICAgIHNldEN1cnJlbnRTZXJ2ZXJOYW1lKGUudGFyZ2V0LnZhbHVlKTtcbiAgfTtcblxuICBjb25zdCBzZXJ2ZXJTZXR0aW5nV2l0aFR5cGU6IElTZXR0aW5nUHJvcGVydHlNYXAgPSB7fTtcbiAgT2JqZWN0LmVudHJpZXMoc2VydmVyU2V0dGluZ3MpLmZvckVhY2goKFtrZXksIHZhbHVlXSkgPT4ge1xuICAgIGNvbnN0IG5ld1Byb3BzOiBJU2V0dGluZ1Byb3BlcnR5ID0ge1xuICAgICAgcHJvcGVydHk6IGtleSxcbiAgICAgIHR5cGU6IHR5cGVvZiB2YWx1ZSBhcyAnc3RyaW5nJyB8ICdudW1iZXInIHwgJ2Jvb2xlYW4nLFxuICAgICAgdmFsdWVcbiAgICB9O1xuICAgIHNlcnZlclNldHRpbmdXaXRoVHlwZVtVVUlELnV1aWQ0KCldID0gbmV3UHJvcHM7XG4gIH0pO1xuXG4gIGNvbnN0IFtwcm9wZXJ0eU1hcCwgc2V0UHJvcGVydHlNYXBdID0gdXNlU3RhdGU8SVNldHRpbmdQcm9wZXJ0eU1hcD4oXG4gICAgc2VydmVyU2V0dGluZ1dpdGhUeXBlXG4gICk7XG5cbiAgY29uc3QgZGVmYXVsdE90aGVyU2V0dGluZ3M6IFREaWN0ID0ge307XG5cbiAgT2JqZWN0LmVudHJpZXMob3RoZXJTZXR0aW5nc1NjaGVtYSkuZm9yRWFjaCgoW2tleSwgdmFsdWVdKSA9PiB7XG4gICAgaWYgKGtleSBpbiBvdGhlclNldHRpbmdzKSB7XG4gICAgICBkZWZhdWx0T3RoZXJTZXR0aW5nc1trZXldID0gb3RoZXJTZXR0aW5nc1trZXldO1xuICAgIH0gZWxzZSB7XG4gICAgICBkZWZhdWx0T3RoZXJTZXR0aW5nc1trZXldID0gdmFsdWVbJ2RlZmF1bHQnXTtcbiAgICB9XG4gIH0pO1xuXG4gIGNvbnN0IFtvdGhlclNldHRpbmdzQ29tcG9zaXRlLCBzZXRPdGhlclNldHRpbmdzQ29tcG9zaXRlXSA9XG4gICAgdXNlU3RhdGU8VERpY3Q+KGRlZmF1bHRPdGhlclNldHRpbmdzKTtcblxuICAvKipcbiAgICogQ2FsbGJhY2sgb24gYWRkaXRpb25hbCBzZXR0aW5nIGZpZWxkIGNoYW5nZSBldmVudFxuICAgKi9cbiAgY29uc3Qgb25PdGhlclNldHRpbmdzQ2hhbmdlID0gKFxuICAgIHByb3BlcnR5OiBzdHJpbmcsXG4gICAgdmFsdWU6IGFueSxcbiAgICB0eXBlOiBzdHJpbmdcbiAgKSA9PiB7XG4gICAgbGV0IHNldHRpbmdWYWx1ZSA9IHZhbHVlO1xuICAgIGlmICh0eXBlID09PSAnbnVtYmVyJykge1xuICAgICAgc2V0dGluZ1ZhbHVlID0gcGFyc2VGbG9hdCh2YWx1ZSk7XG4gICAgfVxuICAgIGNvbnN0IG5ld1Byb3BzID0ge1xuICAgICAgLi4ub3RoZXJTZXR0aW5nc0NvbXBvc2l0ZSxcbiAgICAgIFtwcm9wZXJ0eV06IHNldHRpbmdWYWx1ZVxuICAgIH07XG4gICAgcHJvcHMudXBkYXRlU2V0dGluZy5pbnZva2UocHJvcHMuc2VydmVySGFzaCwgbmV3UHJvcHMpLmNhdGNoKGNvbnNvbGUuZXJyb3IpO1xuICAgIHNldE90aGVyU2V0dGluZ3NDb21wb3NpdGUobmV3UHJvcHMpO1xuICB9O1xuXG4gIC8qKlxuICAgKiBDYWxsYmFjayBvbiBgQWRkIHByb3BlcnR5YCBidXR0b24gY2xpY2sgZXZlbnQuXG4gICAqL1xuICBjb25zdCBhZGRQcm9wZXJ0eSA9ICgpID0+IHtcbiAgICBjb25zdCBoYXNoID0gVVVJRC51dWlkNCgpO1xuICAgIGNvbnN0IG5ld01hcDogSVNldHRpbmdQcm9wZXJ0eU1hcCA9IHtcbiAgICAgIC4uLnByb3BlcnR5TWFwLFxuICAgICAgW2hhc2hdOiB7IHByb3BlcnR5OiAnJywgdHlwZTogJ3N0cmluZycsIHZhbHVlOiAnJyB9XG4gICAgfTtcbiAgICBjb25zdCBwYXlsb2FkOiBURGljdCA9IHt9O1xuICAgIE9iamVjdC52YWx1ZXMobmV3TWFwKS5mb3JFYWNoKHZhbHVlID0+IHtcbiAgICAgIHBheWxvYWRbdmFsdWUucHJvcGVydHldID0gdmFsdWUudmFsdWU7XG4gICAgfSk7XG4gICAgcHJvcHMudXBkYXRlU2V0dGluZ1xuICAgICAgLmludm9rZShwcm9wcy5zZXJ2ZXJIYXNoLCB7XG4gICAgICAgIFtTRVJWRVJfU0VUVElOR1NdOiBwYXlsb2FkXG4gICAgICB9KVxuICAgICAgLmNhdGNoKGNvbnNvbGUuZXJyb3IpO1xuICAgIHNldFByb3BlcnR5TWFwKG5ld01hcCk7XG4gIH07XG5cbiAgLyoqXG4gICAqIENhbGxiYWNrIG9uIGBSZW1vdmUgcHJvcGVydHlgIGJ1dHRvbiBjbGljayBldmVudC5cbiAgICovXG4gIGNvbnN0IHJlbW92ZVByb3BlcnR5ID0gKGVudHJ5SGFzaDogc3RyaW5nKSA9PiB7XG4gICAgY29uc3QgbmV3TWFwOiBJU2V0dGluZ1Byb3BlcnR5TWFwID0ge307XG4gICAgT2JqZWN0LmVudHJpZXMocHJvcGVydHlNYXApLmZvckVhY2goKFtoYXNoLCB2YWx1ZV0pID0+IHtcbiAgICAgIGlmIChoYXNoICE9PSBlbnRyeUhhc2gpIHtcbiAgICAgICAgbmV3TWFwW2hhc2hdID0gdmFsdWU7XG4gICAgICB9XG4gICAgICBjb25zdCBwYXlsb2FkOiBURGljdCA9IHt9O1xuICAgICAgT2JqZWN0LnZhbHVlcyhuZXdNYXApLmZvckVhY2godmFsdWUgPT4ge1xuICAgICAgICBwYXlsb2FkW3ZhbHVlLnByb3BlcnR5XSA9IHZhbHVlLnZhbHVlO1xuICAgICAgfSk7XG4gICAgICBwcm9wcy51cGRhdGVTZXR0aW5nXG4gICAgICAgIC5pbnZva2UocHJvcHMuc2VydmVySGFzaCwge1xuICAgICAgICAgIFtTRVJWRVJfU0VUVElOR1NdOiBwYXlsb2FkXG4gICAgICAgIH0pXG4gICAgICAgIC5jYXRjaChjb25zb2xlLmVycm9yKTtcbiAgICAgIHNldFByb3BlcnR5TWFwKG5ld01hcCk7XG4gICAgfSk7XG4gIH07XG5cbiAgLyoqXG4gICAqIFNhdmUgc2V0dGluZyB0byB0aGUgc2V0dGluZyByZWdpc3RyeSBvbiBmaWVsZCBjaGFuZ2UgZXZlbnQuXG4gICAqL1xuICBjb25zdCBzZXRQcm9wZXJ0eSA9IChoYXNoOiBzdHJpbmcsIHByb3BlcnR5OiBJU2V0dGluZ1Byb3BlcnR5KTogdm9pZCA9PiB7XG4gICAgaWYgKGhhc2ggaW4gcHJvcGVydHlNYXApIHtcbiAgICAgIGNvbnN0IG5ld01hcDogSVNldHRpbmdQcm9wZXJ0eU1hcCA9IHsgLi4ucHJvcGVydHlNYXAsIFtoYXNoXTogcHJvcGVydHkgfTtcbiAgICAgIGNvbnN0IHBheWxvYWQ6IFREaWN0ID0ge307XG4gICAgICBPYmplY3QudmFsdWVzKG5ld01hcCkuZm9yRWFjaCh2YWx1ZSA9PiB7XG4gICAgICAgIHBheWxvYWRbdmFsdWUucHJvcGVydHldID0gdmFsdWUudmFsdWU7XG4gICAgICB9KTtcbiAgICAgIHNldFByb3BlcnR5TWFwKG5ld01hcCk7XG4gICAgICBwcm9wcy51cGRhdGVTZXR0aW5nXG4gICAgICAgIC5pbnZva2UocHJvcHMuc2VydmVySGFzaCwge1xuICAgICAgICAgIFtTRVJWRVJfU0VUVElOR1NdOiBwYXlsb2FkXG4gICAgICAgIH0pXG4gICAgICAgIC5jYXRjaChjb25zb2xlLmVycm9yKTtcbiAgICB9XG4gIH07XG4gIGNvbnN0IGRlYm91bmNlZFNldFByb3BlcnR5ID0gbmV3IERlYm91bmNlcjxcbiAgICB2b2lkLFxuICAgIGFueSxcbiAgICBbaGFzaDogc3RyaW5nLCBwcm9wZXJ0eTogSVNldHRpbmdQcm9wZXJ0eV1cbiAgPihzZXRQcm9wZXJ0eSk7XG4gIHJldHVybiAoXG4gICAgPGRpdiBjbGFzc05hbWU9XCJhcnJheS1pdGVtXCI+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXAgXCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtRm9ybUdyb3VwLWNvbnRlbnRcIj5cbiAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLW9iamVjdEZpZWxkV3JhcHBlclwiPlxuICAgICAgICAgICAgPGZpZWxkc2V0PlxuICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImZvcm0tZ3JvdXAgc21hbGwtZmllbGRcIj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLW1vZGlmaWVkSW5kaWNhdG9yIGpwLWVycm9ySW5kaWNhdG9yXCI+PC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1Gb3JtR3JvdXAtY29udGVudFwiPlxuICAgICAgICAgICAgICAgICAgPGgzIGNsYXNzTmFtZT1cImpwLUZvcm1Hcm91cC1maWVsZExhYmVsIGpwLUZvcm1Hcm91cC1jb250ZW50SXRlbVwiPlxuICAgICAgICAgICAgICAgICAgICB7cHJvcHMudHJhbnMuX18oJ1NlcnZlciBuYW1lOicpfVxuICAgICAgICAgICAgICAgICAgPC9oMz5cbiAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtaW5wdXRGaWVsZFdyYXBwZXIganAtRm9ybUdyb3VwLWNvbnRlbnRJdGVtXCI+XG4gICAgICAgICAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgICAgICAgICAgICAgdHlwZT1cInRleHRcIlxuICAgICAgICAgICAgICAgICAgICAgIHJlcXVpcmVkPXt0cnVlfVxuICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXtjdXJyZW50U2VydmVyTmFtZX1cbiAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17ZSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBvblNlcnZlck5hbWVDaGFuZ2UoZSk7XG4gICAgICAgICAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ2YWxpZGF0aW9uRXJyb3JzXCI+XG4gICAgICAgICAgICAgICAgICAgIDxkaXY+XG4gICAgICAgICAgICAgICAgICAgICAgPHVsIGNsYXNzTmFtZT1cImVycm9yLWRldGFpbCBicy1jYWxsb3V0IGJzLWNhbGxvdXQtaW5mb1wiPlxuICAgICAgICAgICAgICAgICAgICAgICAgPGxpIGNsYXNzTmFtZT1cInRleHQtZGFuZ2VyXCI+XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHtwcm9wcy50cmFucy5fXygnaXMgYSByZXF1aXJlZCBwcm9wZXJ0eScpfVxuICAgICAgICAgICAgICAgICAgICAgICAgPC9saT5cbiAgICAgICAgICAgICAgICAgICAgICA8L3VsPlxuICAgICAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAge09iamVjdC5lbnRyaWVzKG90aGVyU2V0dGluZ3NTY2hlbWEpLm1hcChcbiAgICAgICAgICAgICAgICAoW3Byb3BlcnR5LCB2YWx1ZV0sIGlkeCkgPT4ge1xuICAgICAgICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgICAgICAgPGRpdlxuICAgICAgICAgICAgICAgICAgICAgIGtleT17YCR7aWR4fS0ke3Byb3BlcnR5fWB9XG4gICAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwiZm9ybS1ncm91cCBzbWFsbC1maWVsZFwiXG4gICAgICAgICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUZvcm1Hcm91cC1jb250ZW50XCI+XG4gICAgICAgICAgICAgICAgICAgICAgICA8aDMgY2xhc3NOYW1lPVwianAtRm9ybUdyb3VwLWZpZWxkTGFiZWwganAtRm9ybUdyb3VwLWNvbnRlbnRJdGVtXCI+XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHt2YWx1ZS50aXRsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIDwvaDM+XG4gICAgICAgICAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLWlucHV0RmllbGRXcmFwcGVyIGpwLUZvcm1Hcm91cC1jb250ZW50SXRlbVwiPlxuICAgICAgICAgICAgICAgICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJmb3JtLWNvbnRyb2xcIlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPVwiXCJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0eXBlPXt2YWx1ZS50eXBlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlPXtvdGhlclNldHRpbmdzQ29tcG9zaXRlW3Byb3BlcnR5XX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17ZSA9PlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgb25PdGhlclNldHRpbmdzQ2hhbmdlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBwcm9wZXJ0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZS50YXJnZXQudmFsdWUsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlLnR5cGVcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtRm9ybUdyb3VwLWRlc2NyaXB0aW9uXCI+XG4gICAgICAgICAgICAgICAgICAgICAgICAgIHt2YWx1ZS5kZXNjcmlwdGlvbn1cbiAgICAgICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJ2YWxpZGF0aW9uRXJyb3JzXCI+PC9kaXY+XG4gICAgICAgICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgIDxmaWVsZHNldD5cbiAgICAgICAgICAgICAgICA8bGVnZW5kPntzZXJ2ZXJTZXR0aW5nc1NjaGVtYVsndGl0bGUnXX08L2xlZ2VuZD5cbiAgICAgICAgICAgICAgICB7T2JqZWN0LmVudHJpZXMocHJvcGVydHlNYXApLm1hcCgoW2hhc2gsIHByb3BlcnR5XSkgPT4ge1xuICAgICAgICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgICAgICAgPFByb3BlcnR5RnJvbVxuICAgICAgICAgICAgICAgICAgICAgIGtleT17aGFzaH1cbiAgICAgICAgICAgICAgICAgICAgICBoYXNoPXtoYXNofVxuICAgICAgICAgICAgICAgICAgICAgIHByb3BlcnR5PXtwcm9wZXJ0eX1cbiAgICAgICAgICAgICAgICAgICAgICByZW1vdmVQcm9wZXJ0eT17cmVtb3ZlUHJvcGVydHl9XG4gICAgICAgICAgICAgICAgICAgICAgc2V0UHJvcGVydHk9e2RlYm91bmNlZFNldFByb3BlcnR5fVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9KX1cbiAgICAgICAgICAgICAgICA8c3Bhbj57c2VydmVyU2V0dGluZ3NTY2hlbWFbJ2Rlc2NyaXB0aW9uJ119PC9zcGFuPlxuICAgICAgICAgICAgICA8L2ZpZWxkc2V0PlxuICAgICAgICAgICAgPC9maWVsZHNldD5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgICA8L2Rpdj5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtQXJyYXlPcGVyYXRpb25zXCI+XG4gICAgICAgIDxidXR0b24gY2xhc3NOYW1lPVwianAtbW9kLXN0eWxlZCBqcC1tb2QtcmVqZWN0XCIgb25DbGljaz17YWRkUHJvcGVydHl9PlxuICAgICAgICAgIHtwcm9wcy50cmFucy5fXygnQWRkIHByb3BlcnR5Jyl9XG4gICAgICAgIDwvYnV0dG9uPlxuICAgICAgICA8YnV0dG9uXG4gICAgICAgICAgY2xhc3NOYW1lPVwianAtbW9kLXN0eWxlZCBqcC1tb2Qtd2FybiBqcC1Gb3JtR3JvdXAtcmVtb3ZlQnV0dG9uXCJcbiAgICAgICAgICBvbkNsaWNrPXsoKSA9PiBwcm9wcy5yZW1vdmVTZXR0aW5nKHByb3BzLnNlcnZlckhhc2gpfVxuICAgICAgICA+XG4gICAgICAgICAge3Byb3BzLnRyYW5zLl9fKCdSZW1vdmUgc2VydmVyJyl9XG4gICAgICAgIDwvYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gICk7XG59XG5cbmZ1bmN0aW9uIFByb3BlcnR5RnJvbShwcm9wczoge1xuICBoYXNoOiBzdHJpbmc7XG4gIHByb3BlcnR5OiBJU2V0dGluZ1Byb3BlcnR5O1xuICByZW1vdmVQcm9wZXJ0eTogKGhhc2g6IHN0cmluZykgPT4gdm9pZDtcbiAgc2V0UHJvcGVydHk6IERlYm91bmNlcjx2b2lkLCBhbnksIFtoYXNoOiBzdHJpbmcsIHByb3BlcnR5OiBJU2V0dGluZ1Byb3BlcnR5XT47XG59KTogSlNYLkVsZW1lbnQge1xuICBjb25zdCBbc3RhdGUsIHNldFN0YXRlXSA9IHVzZVN0YXRlPHtcbiAgICBwcm9wZXJ0eTogc3RyaW5nO1xuICAgIHR5cGU6ICdib29sZWFuJyB8ICdzdHJpbmcnIHwgJ251bWJlcic7XG4gICAgdmFsdWU6IGFueTtcbiAgfT4oeyAuLi5wcm9wcy5wcm9wZXJ0eSB9KTtcbiAgY29uc3QgVFlQRV9NQVAgPSB7IHN0cmluZzogJ3RleHQnLCBudW1iZXI6ICdudW1iZXInLCBib29sZWFuOiAnY2hlY2tib3gnIH07XG5cbiAgY29uc3QgcmVtb3ZlSXRlbSA9ICgpID0+IHtcbiAgICBwcm9wcy5yZW1vdmVQcm9wZXJ0eShwcm9wcy5oYXNoKTtcbiAgfTtcblxuICBjb25zdCBjaGFuZ2VOYW1lID0gKG5ld05hbWU6IHN0cmluZykgPT4ge1xuICAgIGNvbnN0IG5ld1N0YXRlID0geyAuLi5zdGF0ZSwgcHJvcGVydHk6IG5ld05hbWUgfTtcbiAgICBwcm9wcy5zZXRQcm9wZXJ0eS5pbnZva2UocHJvcHMuaGFzaCwgbmV3U3RhdGUpLmNhdGNoKGNvbnNvbGUuZXJyb3IpO1xuICAgIHNldFN0YXRlKG5ld1N0YXRlKTtcbiAgfTtcblxuICBjb25zdCBjaGFuZ2VWYWx1ZSA9IChcbiAgICBuZXdWYWx1ZTogYW55LFxuICAgIHR5cGU6ICdzdHJpbmcnIHwgJ2Jvb2xlYW4nIHwgJ251bWJlcidcbiAgKSA9PiB7XG4gICAgbGV0IHZhbHVlID0gbmV3VmFsdWU7XG4gICAgaWYgKHR5cGUgPT09ICdudW1iZXInKSB7XG4gICAgICB2YWx1ZSA9IHBhcnNlRmxvYXQobmV3VmFsdWUpO1xuICAgIH1cbiAgICBjb25zdCBuZXdTdGF0ZSA9IHsgLi4uc3RhdGUsIHZhbHVlIH07XG4gICAgcHJvcHMuc2V0UHJvcGVydHkuaW52b2tlKHByb3BzLmhhc2gsIG5ld1N0YXRlKS5jYXRjaChjb25zb2xlLmVycm9yKTtcbiAgICBzZXRTdGF0ZShuZXdTdGF0ZSk7XG4gIH07XG5cbiAgY29uc3QgY2hhbmdlVHlwZSA9IChuZXdUeXBlOiAnYm9vbGVhbicgfCAnc3RyaW5nJyB8ICdudW1iZXInKSA9PiB7XG4gICAgbGV0IHZhbHVlOiBzdHJpbmcgfCBib29sZWFuIHwgbnVtYmVyO1xuICAgIGlmIChuZXdUeXBlID09PSAnYm9vbGVhbicpIHtcbiAgICAgIHZhbHVlID0gZmFsc2U7XG4gICAgfSBlbHNlIGlmIChuZXdUeXBlID09PSAnbnVtYmVyJykge1xuICAgICAgdmFsdWUgPSAwO1xuICAgIH0gZWxzZSB7XG4gICAgICB2YWx1ZSA9ICcnO1xuICAgIH1cbiAgICBjb25zdCBuZXdTdGF0ZSA9IHsgLi4uc3RhdGUsIHR5cGU6IG5ld1R5cGUsIHZhbHVlIH07XG4gICAgc2V0U3RhdGUobmV3U3RhdGUpO1xuICAgIHByb3BzLnNldFByb3BlcnR5Lmludm9rZShwcm9wcy5oYXNoLCBuZXdTdGF0ZSkuY2F0Y2goY29uc29sZS5lcnJvcik7XG4gIH07XG5cbiAgcmV0dXJuIChcbiAgICA8ZGl2IGtleT17cHJvcHMuaGFzaH0gY2xhc3NOYW1lPVwiZm9ybS1ncm91cCBzbWFsbC1maWVsZFwiPlxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1Gb3JtR3JvdXAtY29udGVudCBqcC1MU1BFeHRlbnNpb24tRm9ybUdyb3VwLWNvbnRlbnRcIj5cbiAgICAgICAgPGlucHV0XG4gICAgICAgICAgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICB0eXBlPVwidGV4dFwiXG4gICAgICAgICAgcmVxdWlyZWQ9e3RydWV9XG4gICAgICAgICAgcGxhY2Vob2xkZXI9eydQcm9wZXJ0eSBuYW1lJ31cbiAgICAgICAgICB2YWx1ZT17c3RhdGUucHJvcGVydHl9XG4gICAgICAgICAgb25DaGFuZ2U9e2UgPT4ge1xuICAgICAgICAgICAgY2hhbmdlTmFtZShlLnRhcmdldC52YWx1ZSk7XG4gICAgICAgICAgfX1cbiAgICAgICAgLz5cbiAgICAgICAgPHNlbGVjdFxuICAgICAgICAgIGNsYXNzTmFtZT1cImZvcm0tY29udHJvbFwiXG4gICAgICAgICAgdmFsdWU9e3N0YXRlLnR5cGV9XG4gICAgICAgICAgb25DaGFuZ2U9e2UgPT5cbiAgICAgICAgICAgIGNoYW5nZVR5cGUoZS50YXJnZXQudmFsdWUgYXMgJ2Jvb2xlYW4nIHwgJ3N0cmluZycgfCAnbnVtYmVyJylcbiAgICAgICAgICB9XG4gICAgICAgID5cbiAgICAgICAgICA8b3B0aW9uIHZhbHVlPVwic3RyaW5nXCI+U3RyaW5nPC9vcHRpb24+XG4gICAgICAgICAgPG9wdGlvbiB2YWx1ZT1cIm51bWJlclwiPk51bWJlcjwvb3B0aW9uPlxuICAgICAgICAgIDxvcHRpb24gdmFsdWU9XCJib29sZWFuXCI+Qm9vbGVhbjwvb3B0aW9uPlxuICAgICAgICA8L3NlbGVjdD5cbiAgICAgICAgPGlucHV0XG4gICAgICAgICAgY2xhc3NOYW1lPVwiZm9ybS1jb250cm9sXCJcbiAgICAgICAgICB0eXBlPXtUWVBFX01BUFtzdGF0ZS50eXBlXX1cbiAgICAgICAgICByZXF1aXJlZD17ZmFsc2V9XG4gICAgICAgICAgcGxhY2Vob2xkZXI9eydQcm9wZXJ0eSB2YWx1ZSd9XG4gICAgICAgICAgdmFsdWU9e3N0YXRlLnR5cGUgIT09ICdib29sZWFuJyA/IHN0YXRlLnZhbHVlIDogdW5kZWZpbmVkfVxuICAgICAgICAgIGNoZWNrZWQ9e3N0YXRlLnR5cGUgPT09ICdib29sZWFuJyA/IHN0YXRlLnZhbHVlIDogdW5kZWZpbmVkfVxuICAgICAgICAgIG9uQ2hhbmdlPXtcbiAgICAgICAgICAgIHN0YXRlLnR5cGUgIT09ICdib29sZWFuJ1xuICAgICAgICAgICAgICA/IGUgPT4gY2hhbmdlVmFsdWUoZS50YXJnZXQudmFsdWUsIHN0YXRlLnR5cGUpXG4gICAgICAgICAgICAgIDogZSA9PiBjaGFuZ2VWYWx1ZShlLnRhcmdldC5jaGVja2VkLCBzdGF0ZS50eXBlKVxuICAgICAgICAgIH1cbiAgICAgICAgLz5cbiAgICAgICAgPGJ1dHRvbiBjbGFzc05hbWU9XCJqcC1tb2QtbWluaW1hbCBqcC1CdXR0b25cIiBvbkNsaWNrPXtyZW1vdmVJdGVtfT5cbiAgICAgICAgICA8Y2xvc2VJY29uLnJlYWN0IC8+XG4gICAgICAgIDwvYnV0dG9uPlxuICAgICAgPC9kaXY+XG4gICAgPC9kaXY+XG4gICk7XG59XG5cbi8qKlxuICogSW50ZXJuYWwgc3RhdGUgb2YgdGhlIHNldHRpbmcgY29tcG9uZW50XG4gKi9cbmludGVyZmFjZSBJU3RhdGUge1xuICAvKipcbiAgICogVGl0bGUgb2YgdGhlIHNldHRpbmcgc2VjdGlvblxuICAgKi9cbiAgdGl0bGU/OiBzdHJpbmc7XG4gIC8qKlxuICAgKiBEZXNjcmlwdGlvbiBvZiB0aGUgc2V0dGluZyBzZWN0aW9uXG4gICAqL1xuICBkZXNjPzogc3RyaW5nO1xuICAvKipcbiAgICogSXRlbXMgb2Ygc2V0dGluZyBzZWN0aW9uXG4gICAqL1xuICBpdGVtczogVERpY3Q7XG59XG5pbnRlcmZhY2UgSVByb3BzIGV4dGVuZHMgRmllbGRQcm9wcyB7XG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yO1xufVxuXG4vKipcbiAqIFJlYWN0IHNldHRpbmcgY29tcG9uZW50XG4gKi9cbmNsYXNzIFNldHRpbmdSZW5kZXJlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudDxJUHJvcHMsIElTdGF0ZT4ge1xuICBjb25zdHJ1Y3Rvcihwcm9wczogSVByb3BzKSB7XG4gICAgc3VwZXIocHJvcHMpO1xuICAgIHRoaXMuX3NldHRpbmcgPSBwcm9wcy5mb3JtQ29udGV4dC5zZXR0aW5ncztcbiAgICB0aGlzLl90cmFucyA9IHByb3BzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgY29uc3Qgc2NoZW1hID0gdGhpcy5fc2V0dGluZy5zY2hlbWFbJ2RlZmluaXRpb25zJ10gYXMgVERpY3Q7XG5cbiAgICB0aGlzLl9kZWZhdWx0U2V0dGluZyA9IHNjaGVtYVsnbGFuZ3VhZ2VTZXJ2ZXInXVsnZGVmYXVsdCddO1xuICAgIHRoaXMuX3NjaGVtYSA9IHNjaGVtYVsnbGFuZ3VhZ2VTZXJ2ZXInXVsncHJvcGVydGllcyddO1xuICAgIGNvbnN0IHRpdGxlID0gcHJvcHMuc2NoZW1hLnRpdGxlO1xuICAgIGNvbnN0IGRlc2MgPSBwcm9wcy5zY2hlbWEuZGVzY3JpcHRpb247XG4gICAgY29uc3Qgc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzID0gcHJvcHMuZm9ybUNvbnRleHQuc2V0dGluZ3M7XG4gICAgY29uc3QgY29tcG9zaXRlRGF0YSA9IHNldHRpbmdzLmdldChTRVRUSU5HX05BTUUpLmNvbXBvc2l0ZSBhcyBURGljdDtcblxuICAgIGxldCBpdGVtczogVERpY3QgPSB7fTtcbiAgICBpZiAoY29tcG9zaXRlRGF0YSkge1xuICAgICAgT2JqZWN0LmVudHJpZXMoY29tcG9zaXRlRGF0YSkuZm9yRWFjaCgoW2tleSwgdmFsdWVdKSA9PiB7XG4gICAgICAgIGlmICh2YWx1ZSkge1xuICAgICAgICAgIGNvbnN0IGhhc2ggPSBVVUlELnV1aWQ0KCk7XG4gICAgICAgICAgaXRlbXNbaGFzaF0gPSB7IHNlcnZlck5hbWU6IGtleSwgLi4udmFsdWUgfTtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICAgIHRoaXMuc3RhdGUgPSB7IHRpdGxlLCBkZXNjLCBpdGVtcyB9O1xuICAgIHRoaXMuX2RlYm91bmNlZFVwZGF0ZVNldHRpbmcgPSBuZXcgRGVib3VuY2VyKHRoaXMudXBkYXRlU2V0dGluZy5iaW5kKHRoaXMpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBzZXR0aW5nIGl0ZW0gYnkgaXRzIGhhc2hcbiAgICpcbiAgICogQHBhcmFtIGhhc2ggLSBoYXNoIG9mIHRoZSBpdGVtIHRvIGJlIHJlbW92ZWQuXG4gICAqL1xuICByZW1vdmVTZXR0aW5nID0gKGhhc2g6IHN0cmluZyk6IHZvaWQgPT4ge1xuICAgIGlmIChoYXNoIGluIHRoaXMuc3RhdGUuaXRlbXMpIHtcbiAgICAgIGNvbnN0IGl0ZW1zOiBURGljdCA9IHt9O1xuICAgICAgZm9yIChjb25zdCBrZXkgaW4gdGhpcy5zdGF0ZS5pdGVtcykge1xuICAgICAgICBpZiAoa2V5ICE9PSBoYXNoKSB7XG4gICAgICAgICAgaXRlbXNba2V5XSA9IHRoaXMuc3RhdGUuaXRlbXNba2V5XTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgICAgdGhpcy5zZXRTdGF0ZShcbiAgICAgICAgb2xkID0+IHtcbiAgICAgICAgICByZXR1cm4geyAuLi5vbGQsIGl0ZW1zIH07XG4gICAgICAgIH0sXG4gICAgICAgICgpID0+IHtcbiAgICAgICAgICB0aGlzLnNhdmVTZXJ2ZXJTZXR0aW5nKCk7XG4gICAgICAgIH1cbiAgICAgICk7XG4gICAgfVxuICB9O1xuXG4gIC8qKlxuICAgKiBVcGRhdGUgYSBzZXR0aW5nIGl0ZW0gYnkgaXRzIGhhc2hcbiAgICpcbiAgICogQHBhcmFtIGhhc2ggLSBoYXNoIG9mIHRoZSBpdGVtIHRvIGJlIHVwZGF0ZWQuXG4gICAqIEBwYXJhbSBuZXdTZXR0aW5nIC0gbmV3IHNldHRpbmcgdmFsdWUuXG4gICAqL1xuICB1cGRhdGVTZXR0aW5nID0gKGhhc2g6IHN0cmluZywgbmV3U2V0dGluZzogVERpY3QpOiB2b2lkID0+IHtcbiAgICBpZiAoaGFzaCBpbiB0aGlzLnN0YXRlLml0ZW1zKSB7XG4gICAgICBjb25zdCBpdGVtczogVERpY3QgPSB7fTtcbiAgICAgIGZvciAoY29uc3Qga2V5IGluIHRoaXMuc3RhdGUuaXRlbXMpIHtcbiAgICAgICAgaWYgKGtleSA9PT0gaGFzaCkge1xuICAgICAgICAgIGl0ZW1zW2tleV0gPSB7IC4uLnRoaXMuc3RhdGUuaXRlbXNba2V5XSwgLi4ubmV3U2V0dGluZyB9O1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgIGl0ZW1zW2tleV0gPSB0aGlzLnN0YXRlLml0ZW1zW2tleV07XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICAgIHRoaXMuc2V0U3RhdGUoXG4gICAgICAgIG9sZCA9PiB7XG4gICAgICAgICAgcmV0dXJuIHsgLi4ub2xkLCBpdGVtcyB9O1xuICAgICAgICB9LFxuICAgICAgICAoKSA9PiB7XG4gICAgICAgICAgdGhpcy5zYXZlU2VydmVyU2V0dGluZygpO1xuICAgICAgICB9XG4gICAgICApO1xuICAgIH1cbiAgfTtcblxuICAvKipcbiAgICogQWRkIHNldHRpbmcgaXRlbSB0byB0aGUgc2V0dGluZyBjb21wb25lbnQuXG4gICAqL1xuICBhZGRTZXJ2ZXJTZXR0aW5nID0gKCk6IHZvaWQgPT4ge1xuICAgIGxldCBpbmRleCA9IDA7XG4gICAgbGV0IGtleSA9ICduZXdLZXknO1xuICAgIHdoaWxlIChcbiAgICAgIE9iamVjdC52YWx1ZXModGhpcy5zdGF0ZS5pdGVtcylcbiAgICAgICAgLm1hcCh2YWwgPT4gdmFsLnNlcnZlck5hbWUpXG4gICAgICAgIC5pbmNsdWRlcyhrZXkpXG4gICAgKSB7XG4gICAgICBpbmRleCArPSAxO1xuICAgICAga2V5ID0gYG5ld0tleS0ke2luZGV4fWA7XG4gICAgfVxuICAgIHRoaXMuc2V0U3RhdGUoXG4gICAgICBvbGQgPT4gKHtcbiAgICAgICAgLi4ub2xkLFxuICAgICAgICBpdGVtczoge1xuICAgICAgICAgIC4uLm9sZC5pdGVtcyxcbiAgICAgICAgICBbVVVJRC51dWlkNCgpXTogeyAuLi50aGlzLl9kZWZhdWx0U2V0dGluZywgc2VydmVyTmFtZToga2V5IH1cbiAgICAgICAgfVxuICAgICAgfSksXG4gICAgICAoKSA9PiB7XG4gICAgICAgIHRoaXMuc2F2ZVNlcnZlclNldHRpbmcoKTtcbiAgICAgIH1cbiAgICApO1xuICB9O1xuXG4gIC8qKlxuICAgKiBTYXZlIHRoZSB2YWx1ZSBvZiBzZXR0aW5nIGl0ZW1zIHRvIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgc2F2ZVNlcnZlclNldHRpbmcgPSAoKSA9PiB7XG4gICAgY29uc3Qgc2V0dGluZ3M6IFREaWN0ID0ge307XG4gICAgT2JqZWN0LnZhbHVlcyh0aGlzLnN0YXRlLml0ZW1zKS5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgY29uc3QgeyBzZXJ2ZXJOYW1lLCAuLi5zZXR0aW5nIH0gPSBpdGVtO1xuICAgICAgc2V0dGluZ3Nbc2VydmVyTmFtZV0gPSBzZXR0aW5nO1xuICAgIH0pO1xuICAgIHRoaXMuX3NldHRpbmcuc2V0KFNFVFRJTkdfTkFNRSwgc2V0dGluZ3MpLmNhdGNoKGNvbnNvbGUuZXJyb3IpO1xuICB9O1xuICByZW5kZXIoKTogSlNYLkVsZW1lbnQge1xuICAgIHJldHVybiAoXG4gICAgICA8ZGl2PlxuICAgICAgICA8ZmllbGRzZXQ+XG4gICAgICAgICAgPGxlZ2VuZD57dGhpcy5zdGF0ZS50aXRsZX08L2xlZ2VuZD5cbiAgICAgICAgICA8cCBjbGFzc05hbWU9XCJmaWVsZC1kZXNjcmlwdGlvblwiPnt0aGlzLnN0YXRlLmRlc2N9PC9wPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZmllbGQgZmllbGQtYXJyYXkgZmllbGQtYXJyYXktb2Ytb2JqZWN0XCI+XG4gICAgICAgICAgICB7T2JqZWN0LmVudHJpZXModGhpcy5zdGF0ZS5pdGVtcykubWFwKChbaGFzaCwgdmFsdWVdLCBpZHgpID0+IHtcbiAgICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgICA8QnVpbGRTZXR0aW5nRm9ybVxuICAgICAgICAgICAgICAgICAga2V5PXtgJHtpZHh9LSR7aGFzaH1gfVxuICAgICAgICAgICAgICAgICAgdHJhbnM9e3RoaXMuX3RyYW5zfVxuICAgICAgICAgICAgICAgICAgcmVtb3ZlU2V0dGluZz17dGhpcy5yZW1vdmVTZXR0aW5nfVxuICAgICAgICAgICAgICAgICAgdXBkYXRlU2V0dGluZz17dGhpcy5fZGVib3VuY2VkVXBkYXRlU2V0dGluZ31cbiAgICAgICAgICAgICAgICAgIHNlcnZlckhhc2g9e2hhc2h9XG4gICAgICAgICAgICAgICAgICBzZXR0aW5ncz17dmFsdWV9XG4gICAgICAgICAgICAgICAgICBzY2hlbWE9e3RoaXMuX3NjaGVtYX1cbiAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfSl9XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgPGRpdj5cbiAgICAgICAgICAgIDxidXR0b25cbiAgICAgICAgICAgICAgc3R5bGU9e3sgbWFyZ2luOiAyIH19XG4gICAgICAgICAgICAgIGNsYXNzTmFtZT1cImpwLW1vZC1zdHlsZWQganAtbW9kLXJlamVjdFwiXG4gICAgICAgICAgICAgIG9uQ2xpY2s9e3RoaXMuYWRkU2VydmVyU2V0dGluZ31cbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAge3RoaXMuX3RyYW5zLl9fKCdBZGQgc2VydmVyJyl9XG4gICAgICAgICAgICA8L2J1dHRvbj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9maWVsZHNldD5cbiAgICAgIDwvZGl2PlxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAqL1xuICBwcml2YXRlIF9zZXR0aW5nOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncztcblxuICAvKipcbiAgICogVGhlIHRyYW5zbGF0aW9uIGJ1bmRsZS5cbiAgICovXG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcblxuICAvKipcbiAgICogRGVmYXVsdCBzZXR0aW5nIHZhbHVlLlxuICAgKi9cbiAgcHJpdmF0ZSBfZGVmYXVsdFNldHRpbmc6IFREaWN0O1xuXG4gIC8qKlxuICAgKiBUaGUgc2V0dGluZyBzY2hlbWEuXG4gICAqL1xuICBwcml2YXRlIF9zY2hlbWE6IFREaWN0O1xuXG4gIHByaXZhdGUgX2RlYm91bmNlZFVwZGF0ZVNldHRpbmc6IERlYm91bmNlcjxcbiAgICB2b2lkLFxuICAgIGFueSxcbiAgICBbaGFzaDogc3RyaW5nLCBuZXdTZXR0aW5nOiBURGljdF1cbiAgPjtcbn1cblxuLyoqXG4gKiBDdXN0b20gc2V0dGluZyByZW5kZXJlciBmb3IgbGFuZ3VhZ2Ugc2VydmVyIGV4dGVuc2lvbi5cbiAqL1xuZXhwb3J0IGZ1bmN0aW9uIHJlbmRlclNlcnZlclNldHRpbmcoXG4gIHByb3BzOiBGaWVsZFByb3BzLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuKTogSlNYLkVsZW1lbnQge1xuICByZXR1cm4gPFNldHRpbmdSZW5kZXJlciB7Li4ucHJvcHN9IHRyYW5zbGF0b3I9e3RyYW5zbGF0b3J9IC8+O1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9