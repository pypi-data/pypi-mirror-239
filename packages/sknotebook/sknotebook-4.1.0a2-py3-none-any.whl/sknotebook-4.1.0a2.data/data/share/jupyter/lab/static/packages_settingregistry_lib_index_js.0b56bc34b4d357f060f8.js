"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_settingregistry_lib_index_js"],{

/***/ "../packages/settingregistry/lib/index.js":
/*!************************************************!*\
  !*** ../packages/settingregistry/lib/index.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BaseSettings": () => (/* reexport safe */ _settingregistry__WEBPACK_IMPORTED_MODULE_0__.BaseSettings),
/* harmony export */   "DefaultSchemaValidator": () => (/* reexport safe */ _settingregistry__WEBPACK_IMPORTED_MODULE_0__.DefaultSchemaValidator),
/* harmony export */   "ISettingRegistry": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry),
/* harmony export */   "SettingRegistry": () => (/* reexport safe */ _settingregistry__WEBPACK_IMPORTED_MODULE_0__.SettingRegistry),
/* harmony export */   "Settings": () => (/* reexport safe */ _settingregistry__WEBPACK_IMPORTED_MODULE_0__.Settings)
/* harmony export */ });
/* harmony import */ var _settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./settingregistry */ "../packages/settingregistry/lib/settingregistry.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../packages/settingregistry/lib/tokens.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module settingregistry
 */




/***/ }),

/***/ "../packages/settingregistry/lib/settingregistry.js":
/*!**********************************************************!*\
  !*** ../packages/settingregistry/lib/settingregistry.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BaseSettings": () => (/* binding */ BaseSettings),
/* harmony export */   "DefaultSchemaValidator": () => (/* binding */ DefaultSchemaValidator),
/* harmony export */   "SettingRegistry": () => (/* binding */ SettingRegistry),
/* harmony export */   "Settings": () => (/* binding */ Settings)
/* harmony export */ });
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var ajv__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ajv */ "../node_modules/ajv/dist/ajv.js");
/* harmony import */ var ajv__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(ajv__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var json5__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! json5 */ "../node_modules/json5/dist/index.js");
/* harmony import */ var json5__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(json5__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./plugin-schema.json */ "../packages/settingregistry/lib/plugin-schema.json");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * An alias for the JSON deep copy function.
 */
const copy = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy;
/** Default arguments for Ajv instances.
 *
 * https://ajv.js.org/options.html
 */
const AJV_DEFAULT_OPTIONS = {
    /**
     * @todo the implications of enabling strict mode are beyond the scope of
     *       the initial PR
     */
    strict: false
};
/**
 * The ASCII record separator character.
 */
const RECORD_SEPARATOR = String.fromCharCode(30);
/**
 * The default implementation of a schema validator.
 */
class DefaultSchemaValidator {
    /**
     * Instantiate a schema validator.
     */
    constructor() {
        this._composer = new (ajv__WEBPACK_IMPORTED_MODULE_4___default())({
            useDefaults: true,
            ...AJV_DEFAULT_OPTIONS
        });
        this._validator = new (ajv__WEBPACK_IMPORTED_MODULE_4___default())({ ...AJV_DEFAULT_OPTIONS });
        this._composer.addSchema(_plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__, 'jupyterlab-plugin-schema');
        this._validator.addSchema(_plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__, 'jupyterlab-plugin-schema');
    }
    /**
     * Validate a plugin's schema and user data; populate the `composite` data.
     *
     * @param plugin - The plugin being validated. Its `composite` data will be
     * populated by reference.
     *
     * @param populate - Whether plugin data should be populated, defaults to
     * `true`.
     *
     * @returns A list of errors if either the schema or data fail to validate or
     * `null` if there are no errors.
     */
    validateData(plugin, populate = true) {
        const validate = this._validator.getSchema(plugin.id);
        const compose = this._composer.getSchema(plugin.id);
        // If the schemas do not exist, add them to the validator and continue.
        if (!validate || !compose) {
            if (plugin.schema.type !== 'object') {
                const keyword = 'schema';
                const message = `Setting registry schemas' root-level type must be ` +
                    `'object', rejecting type: ${plugin.schema.type}`;
                return [{ instancePath: 'type', keyword, schemaPath: '', message }];
            }
            const errors = this._addSchema(plugin.id, plugin.schema);
            return errors || this.validateData(plugin);
        }
        // Parse the raw commented JSON into a user map.
        let user;
        try {
            user = json5__WEBPACK_IMPORTED_MODULE_5__.parse(plugin.raw);
        }
        catch (error) {
            if (error instanceof SyntaxError) {
                return [
                    {
                        instancePath: '',
                        keyword: 'syntax',
                        schemaPath: '',
                        message: error.message
                    }
                ];
            }
            const { column, description } = error;
            const line = error.lineNumber;
            return [
                {
                    instancePath: '',
                    keyword: 'parse',
                    schemaPath: '',
                    message: `${description} (line ${line} column ${column})`
                }
            ];
        }
        if (!validate(user)) {
            return validate.errors;
        }
        // Copy the user data before merging defaults into composite map.
        const composite = copy(user);
        if (!compose(composite)) {
            return compose.errors;
        }
        if (populate) {
            plugin.data = { composite, user };
        }
        return null;
    }
    /**
     * Add a schema to the validator.
     *
     * @param plugin - The plugin ID.
     *
     * @param schema - The schema being added.
     *
     * @returns A list of errors if the schema fails to validate or `null` if there
     * are no errors.
     *
     * #### Notes
     * It is safe to call this function multiple times with the same plugin name.
     */
    _addSchema(plugin, schema) {
        const composer = this._composer;
        const validator = this._validator;
        const validate = validator.getSchema('jupyterlab-plugin-schema');
        // Validate against the main schema.
        if (!validate(schema)) {
            return validate.errors;
        }
        // Validate against the JSON schema meta-schema.
        if (!validator.validateSchema(schema)) {
            return validator.errors;
        }
        // Remove if schema already exists.
        composer.removeSchema(plugin);
        validator.removeSchema(plugin);
        // Add schema to the validator and composer.
        composer.addSchema(schema, plugin);
        validator.addSchema(schema, plugin);
        return null;
    }
}
/**
 * The default concrete implementation of a setting registry.
 */
class SettingRegistry {
    /**
     * Create a new setting registry.
     */
    constructor(options) {
        /**
         * The schema of the setting registry.
         */
        this.schema = _plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__;
        /**
         * The collection of setting registry plugins.
         */
        this.plugins = Object.create(null);
        this._pluginChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._ready = Promise.resolve();
        this._transformers = Object.create(null);
        this._unloadedPlugins = new Map();
        this.connector = options.connector;
        this.validator = options.validator || new DefaultSchemaValidator();
        // Plugins with transformation may not be loaded if the transformation function is
        // not yet available. To avoid fetching again the associated data when the transformation
        // function is available, the plugin data is kept in cache.
        if (options.plugins) {
            options.plugins
                .filter(plugin => plugin.schema['jupyter.lab.transform'])
                .forEach(plugin => this._unloadedPlugins.set(plugin.id, plugin));
            // Preload with any available data at instantiation-time.
            this._ready = this._preload(options.plugins);
        }
    }
    /**
     * A signal that emits the name of a plugin when its settings change.
     */
    get pluginChanged() {
        return this._pluginChanged;
    }
    /**
     * Get an individual setting.
     *
     * @param plugin - The name of the plugin whose settings are being retrieved.
     *
     * @param key - The name of the setting being retrieved.
     *
     * @returns A promise that resolves when the setting is retrieved.
     */
    async get(plugin, key) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (plugin in plugins) {
            const { composite, user } = plugins[plugin].data;
            return {
                composite: composite[key] !== undefined ? copy(composite[key]) : undefined,
                user: user[key] !== undefined ? copy(user[key]) : undefined
            };
        }
        return this.load(plugin).then(() => this.get(plugin, key));
    }
    /**
     * Load a plugin's settings into the setting registry.
     *
     * @param plugin - The name of the plugin whose settings are being loaded.
     *
     * @param forceTransform - An optional parameter to force replay the transforms methods.
     *
     * @returns A promise that resolves with a plugin settings object or rejects
     * if the plugin is not found.
     */
    async load(plugin, forceTransform = false) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        const registry = this; // eslint-disable-line
        // If the plugin exists, resolve.
        if (plugin in plugins) {
            // Force replaying the transform function if expected.
            if (forceTransform) {
                // Empty the composite and user data before replaying the transforms.
                plugins[plugin].data = { composite: {}, user: {} };
                await this._load(await this._transform('fetch', plugins[plugin]));
                this._pluginChanged.emit(plugin);
            }
            return new Settings({ plugin: plugins[plugin], registry });
        }
        // If the plugin is not loaded but has already been fetched.
        if (this._unloadedPlugins.has(plugin) && plugin in this._transformers) {
            await this._load(await this._transform('fetch', this._unloadedPlugins.get(plugin)));
            if (plugin in plugins) {
                this._pluginChanged.emit(plugin);
                this._unloadedPlugins.delete(plugin);
                return new Settings({ plugin: plugins[plugin], registry });
            }
        }
        // If the plugin needs to be loaded from the data connector, fetch.
        return this.reload(plugin);
    }
    /**
     * Reload a plugin's settings into the registry even if they already exist.
     *
     * @param plugin - The name of the plugin whose settings are being reloaded.
     *
     * @returns A promise that resolves with a plugin settings object or rejects
     * with a list of `ISchemaValidator.IError` objects if it fails.
     */
    async reload(plugin) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const fetched = await this.connector.fetch(plugin);
        const plugins = this.plugins; // eslint-disable-line
        const registry = this; // eslint-disable-line
        if (fetched === undefined) {
            throw [
                {
                    instancePath: '',
                    keyword: 'id',
                    message: `Could not fetch settings for ${plugin}.`,
                    schemaPath: ''
                }
            ];
        }
        await this._load(await this._transform('fetch', fetched));
        this._pluginChanged.emit(plugin);
        return new Settings({ plugin: plugins[plugin], registry });
    }
    /**
     * Remove a single setting in the registry.
     *
     * @param plugin - The name of the plugin whose setting is being removed.
     *
     * @param key - The name of the setting being removed.
     *
     * @returns A promise that resolves when the setting is removed.
     */
    async remove(plugin, key) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            return;
        }
        const raw = json5__WEBPACK_IMPORTED_MODULE_5__.parse(plugins[plugin].raw);
        // Delete both the value and any associated comment.
        delete raw[key];
        delete raw[`// ${key}`];
        plugins[plugin].raw = Private.annotatedPlugin(plugins[plugin], raw);
        return this._save(plugin);
    }
    /**
     * Set a single setting in the registry.
     *
     * @param plugin - The name of the plugin whose setting is being set.
     *
     * @param key - The name of the setting being set.
     *
     * @param value - The value of the setting being set.
     *
     * @returns A promise that resolves when the setting has been saved.
     *
     */
    async set(plugin, key, value) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            return this.load(plugin).then(() => this.set(plugin, key, value));
        }
        // Parse the raw JSON string removing all comments and return an object.
        const raw = json5__WEBPACK_IMPORTED_MODULE_5__.parse(plugins[plugin].raw);
        plugins[plugin].raw = Private.annotatedPlugin(plugins[plugin], {
            ...raw,
            [key]: value
        });
        return this._save(plugin);
    }
    /**
     * Register a plugin transform function to act on a specific plugin.
     *
     * @param plugin - The name of the plugin whose settings are transformed.
     *
     * @param transforms - The transform functions applied to the plugin.
     *
     * @returns A disposable that removes the transforms from the registry.
     *
     * #### Notes
     * - `compose` transformations: The registry automatically overwrites a
     * plugin's default values with user overrides, but a plugin may instead wish
     * to merge values. This behavior can be accomplished in a `compose`
     * transformation.
     * - `fetch` transformations: The registry uses the plugin data that is
     * fetched from its connector. If a plugin wants to override, e.g. to update
     * its schema with dynamic defaults, a `fetch` transformation can be applied.
     */
    transform(plugin, transforms) {
        const transformers = this._transformers;
        if (plugin in transformers) {
            const error = new Error(`${plugin} already has a transformer.`);
            error.name = 'TransformError';
            throw error;
        }
        transformers[plugin] = {
            fetch: transforms.fetch || (plugin => plugin),
            compose: transforms.compose || (plugin => plugin)
        };
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(() => {
            delete transformers[plugin];
        });
    }
    /**
     * Upload a plugin's settings.
     *
     * @param plugin - The name of the plugin whose settings are being set.
     *
     * @param raw - The raw plugin settings being uploaded.
     *
     * @returns A promise that resolves when the settings have been saved.
     */
    async upload(plugin, raw) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            return this.load(plugin).then(() => this.upload(plugin, raw));
        }
        // Set the local copy.
        plugins[plugin].raw = raw;
        return this._save(plugin);
    }
    /**
     * Load a plugin into the registry.
     */
    async _load(data) {
        const plugin = data.id;
        // Validate and preload the item.
        try {
            await this._validate(data);
        }
        catch (errors) {
            const output = [`Validating ${plugin} failed:`];
            errors.forEach((error, index) => {
                const { instancePath, schemaPath, keyword, message } = error;
                if (instancePath || schemaPath) {
                    output.push(`${index} - schema @ ${schemaPath}, data @ ${instancePath}`);
                }
                output.push(`{${keyword}} ${message}`);
            });
            console.warn(output.join('\n'));
            throw errors;
        }
    }
    /**
     * Preload a list of plugins and fail gracefully.
     */
    async _preload(plugins) {
        await Promise.all(plugins.map(async (plugin) => {
            var _a;
            try {
                // Apply a transformation to the plugin if necessary.
                await this._load(await this._transform('fetch', plugin));
            }
            catch (errors) {
                /* Ignore silently if no transformers. */
                if (((_a = errors[0]) === null || _a === void 0 ? void 0 : _a.keyword) !== 'unset') {
                    console.warn('Ignored setting registry preload errors.', errors);
                }
            }
        }));
    }
    /**
     * Save a plugin in the registry.
     */
    async _save(plugin) {
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            throw new Error(`${plugin} does not exist in setting registry.`);
        }
        try {
            await this._validate(plugins[plugin]);
        }
        catch (errors) {
            console.warn(`${plugin} validation errors:`, errors);
            throw new Error(`${plugin} failed to validate; check console.`);
        }
        await this.connector.save(plugin, plugins[plugin].raw);
        // Fetch and reload the data to guarantee server and client are in sync.
        const fetched = await this.connector.fetch(plugin);
        if (fetched === undefined) {
            throw [
                {
                    instancePath: '',
                    keyword: 'id',
                    message: `Could not fetch settings for ${plugin}.`,
                    schemaPath: ''
                }
            ];
        }
        await this._load(await this._transform('fetch', fetched));
        this._pluginChanged.emit(plugin);
    }
    /**
     * Transform the plugin if necessary.
     */
    async _transform(phase, plugin) {
        const id = plugin.id;
        const transformers = this._transformers;
        if (!plugin.schema['jupyter.lab.transform']) {
            return plugin;
        }
        if (id in transformers) {
            const transformed = transformers[id][phase].call(null, plugin);
            if (transformed.id !== id) {
                throw [
                    {
                        instancePath: '',
                        keyword: 'id',
                        message: 'Plugin transformations cannot change plugin IDs.',
                        schemaPath: ''
                    }
                ];
            }
            return transformed;
        }
        // If the plugin has no transformers, throw an error and bail.
        throw [
            {
                instancePath: '',
                keyword: 'unset',
                message: `${plugin.id} has no transformers yet.`,
                schemaPath: ''
            }
        ];
    }
    /**
     * Validate and preload a plugin, compose the `composite` data.
     */
    async _validate(plugin) {
        // Validate the user data and create the composite data.
        const errors = this.validator.validateData(plugin);
        if (errors) {
            throw errors;
        }
        // Apply a transformation if necessary and set the local copy.
        this.plugins[plugin.id] = await this._transform('compose', plugin);
    }
}
/**
 * Base settings specified by a JSON schema.
 */
class BaseSettings {
    constructor(options) {
        this._schema = options.schema;
    }
    /**
     * The plugin's schema.
     */
    get schema() {
        return this._schema;
    }
    /**
     * Checks if any fields are different from the default value.
     */
    isDefault(user) {
        for (const key in this.schema.properties) {
            const value = user[key];
            const defaultValue = this.default(key);
            if (value === undefined ||
                defaultValue === undefined ||
                _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepEqual(value, _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.emptyObject) ||
                _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepEqual(value, _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.emptyArray)) {
                continue;
            }
            if (!_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepEqual(value, defaultValue)) {
                return false;
            }
        }
        return true;
    }
    /**
     * Calculate the default value of a setting by iterating through the schema.
     *
     * @param key - The name of the setting whose default value is calculated.
     *
     * @returns A calculated default JSON value for a specific setting.
     */
    default(key) {
        return Private.reifyDefault(this.schema, key);
    }
}
/**
 * A manager for a specific plugin's settings.
 */
class Settings extends BaseSettings {
    /**
     * Instantiate a new plugin settings manager.
     */
    constructor(options) {
        super({ schema: options.plugin.schema });
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._isDisposed = false;
        this.id = options.plugin.id;
        this.registry = options.registry;
        this.registry.pluginChanged.connect(this._onPluginChanged, this);
    }
    /**
     * A signal that emits when the plugin's settings have changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The composite of user settings and extension defaults.
     */
    get composite() {
        return this.plugin.data.composite;
    }
    /**
     * Test whether the plugin settings manager disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    get plugin() {
        return this.registry.plugins[this.id];
    }
    /**
     * The plugin settings raw text value.
     */
    get raw() {
        return this.plugin.raw;
    }
    /**
     * Whether the settings have been modified by the user or not.
     */
    get isModified() {
        return !this.isDefault(this.user);
    }
    /**
     * The user settings.
     */
    get user() {
        return this.plugin.data.user;
    }
    /**
     * The published version of the NPM package containing these settings.
     */
    get version() {
        return this.plugin.version;
    }
    /**
     * Return the defaults in a commented JSON format.
     */
    annotatedDefaults() {
        return Private.annotatedDefaults(this.schema, this.id);
    }
    /**
     * Dispose of the plugin settings resources.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
    }
    /**
     * Get an individual setting.
     *
     * @param key - The name of the setting being retrieved.
     *
     * @returns The setting value.
     *
     * #### Notes
     * This method returns synchronously because it uses a cached copy of the
     * plugin settings that is synchronized with the registry.
     */
    get(key) {
        const { composite, user } = this;
        return {
            composite: composite[key] !== undefined ? copy(composite[key]) : undefined,
            user: user[key] !== undefined ? copy(user[key]) : undefined
        };
    }
    /**
     * Remove a single setting.
     *
     * @param key - The name of the setting being removed.
     *
     * @returns A promise that resolves when the setting is removed.
     *
     * #### Notes
     * This function is asynchronous because it writes to the setting registry.
     */
    remove(key) {
        return this.registry.remove(this.plugin.id, key);
    }
    /**
     * Save all of the plugin's user settings at once.
     */
    save(raw) {
        return this.registry.upload(this.plugin.id, raw);
    }
    /**
     * Set a single setting.
     *
     * @param key - The name of the setting being set.
     *
     * @param value - The value of the setting.
     *
     * @returns A promise that resolves when the setting has been saved.
     *
     * #### Notes
     * This function is asynchronous because it writes to the setting registry.
     */
    set(key, value) {
        return this.registry.set(this.plugin.id, key, value);
    }
    /**
     * Validates raw settings with comments.
     *
     * @param raw - The JSON with comments string being validated.
     *
     * @returns A list of errors or `null` if valid.
     */
    validate(raw) {
        const data = { composite: {}, user: {} };
        const { id, schema } = this.plugin;
        const validator = this.registry.validator;
        const version = this.version;
        return validator.validateData({ data, id, raw, schema, version }, false);
    }
    /**
     * Handle plugin changes in the setting registry.
     */
    _onPluginChanged(sender, plugin) {
        if (plugin === this.plugin.id) {
            this._changed.emit(undefined);
        }
    }
}
/**
 * A namespace for `SettingRegistry` statics.
 */
(function (SettingRegistry) {
    /**
     * Reconcile the menus.
     *
     * @param reference The reference list of menus.
     * @param addition The list of menus to add.
     * @param warn Warn if the command items are duplicated within the same menu.
     * @returns The reconciled list of menus.
     */
    function reconcileMenus(reference, addition, warn = false, addNewItems = true) {
        if (!reference) {
            return addition && addNewItems ? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(addition) : [];
        }
        if (!addition) {
            return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        }
        const merged = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        addition.forEach(menu => {
            const refIndex = merged.findIndex(ref => ref.id === menu.id);
            if (refIndex >= 0) {
                merged[refIndex] = {
                    ...merged[refIndex],
                    ...menu,
                    items: reconcileItems(merged[refIndex].items, menu.items, warn, addNewItems)
                };
            }
            else {
                if (addNewItems) {
                    merged.push(menu);
                }
            }
        });
        return merged;
    }
    SettingRegistry.reconcileMenus = reconcileMenus;
    /**
     * Merge two set of menu items.
     *
     * @param reference Reference set of menu items
     * @param addition New items to add
     * @param warn Whether to warn if item is duplicated; default to false
     * @returns The merged set of items
     */
    function reconcileItems(reference, addition, warn = false, addNewItems = true) {
        if (!reference) {
            return addition ? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(addition) : undefined;
        }
        if (!addition) {
            return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        }
        const items = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        // Merge array element depending on the type
        addition.forEach(item => {
            var _a;
            switch ((_a = item.type) !== null && _a !== void 0 ? _a : 'command') {
                case 'separator':
                    if (addNewItems) {
                        items.push({ ...item });
                    }
                    break;
                case 'submenu':
                    if (item.submenu) {
                        const refIndex = items.findIndex(ref => { var _a, _b; return ref.type === 'submenu' && ((_a = ref.submenu) === null || _a === void 0 ? void 0 : _a.id) === ((_b = item.submenu) === null || _b === void 0 ? void 0 : _b.id); });
                        if (refIndex < 0) {
                            if (addNewItems) {
                                items.push(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(item));
                            }
                        }
                        else {
                            items[refIndex] = {
                                ...items[refIndex],
                                ...item,
                                submenu: reconcileMenus(items[refIndex].submenu
                                    ? [items[refIndex].submenu]
                                    : null, [item.submenu], warn, addNewItems)[0]
                            };
                        }
                    }
                    break;
                case 'command':
                    if (item.command) {
                        const refIndex = items.findIndex(ref => {
                            var _a, _b;
                            return ref.command === item.command &&
                                ref.selector === item.selector &&
                                _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepEqual((_a = ref.args) !== null && _a !== void 0 ? _a : {}, (_b = item.args) !== null && _b !== void 0 ? _b : {});
                        });
                        if (refIndex < 0) {
                            if (addNewItems) {
                                items.push({ ...item });
                            }
                        }
                        else {
                            if (warn) {
                                console.warn(`Menu entry for command '${item.command}' is duplicated.`);
                            }
                            items[refIndex] = { ...items[refIndex], ...item };
                        }
                    }
            }
        });
        return items;
    }
    SettingRegistry.reconcileItems = reconcileItems;
    /**
     * Remove disabled entries from menu items
     *
     * @param items Menu items
     * @returns Filtered menu items
     */
    function filterDisabledItems(items) {
        return items.reduce((final, value) => {
            var _a;
            const copy = { ...value };
            if (!copy.disabled) {
                if (copy.type === 'submenu') {
                    const { submenu } = copy;
                    if (submenu && !submenu.disabled) {
                        copy.submenu = {
                            ...submenu,
                            items: filterDisabledItems((_a = submenu.items) !== null && _a !== void 0 ? _a : [])
                        };
                    }
                }
                final.push(copy);
            }
            return final;
        }, []);
    }
    SettingRegistry.filterDisabledItems = filterDisabledItems;
    /**
     * Reconcile default and user shortcuts and return the composite list.
     *
     * @param defaults - The list of default shortcuts.
     *
     * @param user - The list of user shortcut overrides and additions.
     *
     * @returns A loadable list of shortcuts (omitting disabled and overridden).
     */
    function reconcileShortcuts(defaults, user) {
        const memo = {};
        // If a user shortcut collides with another user shortcut warn and filter.
        user = user.filter(shortcut => {
            const keys = _lumino_commands__WEBPACK_IMPORTED_MODULE_0__.CommandRegistry.normalizeKeys(shortcut).join(RECORD_SEPARATOR);
            if (!keys) {
                console.warn('Skipping this shortcut because there are no actionable keys on this platform', shortcut);
                return false;
            }
            if (!(keys in memo)) {
                memo[keys] = {};
            }
            const { selector } = shortcut;
            if (!(selector in memo[keys])) {
                memo[keys][selector] = false; // Do not warn if a default shortcut conflicts.
                return true;
            }
            console.warn('Skipping this shortcut because it collides with another shortcut.', shortcut);
            return false;
        });
        // If a default shortcut collides with another default, warn and filter,
        // unless one of the shortcuts is a disabling shortcut (so look through
        // disabled shortcuts first). If a shortcut has already been added by the
        // user preferences, filter it out too (this includes shortcuts that are
        // disabled by user preferences).
        defaults = [
            ...defaults.filter(s => !!s.disabled),
            ...defaults.filter(s => !s.disabled)
        ].filter(shortcut => {
            const keys = _lumino_commands__WEBPACK_IMPORTED_MODULE_0__.CommandRegistry.normalizeKeys(shortcut).join(RECORD_SEPARATOR);
            if (!keys) {
                return false;
            }
            if (!(keys in memo)) {
                memo[keys] = {};
            }
            const { disabled, selector } = shortcut;
            if (!(selector in memo[keys])) {
                // Warn of future conflicts if the default shortcut is not disabled.
                memo[keys][selector] = !disabled;
                return true;
            }
            // We have a conflict now. Warn the user if we need to do so.
            if (memo[keys][selector]) {
                console.warn('Skipping this default shortcut because it collides with another default shortcut.', shortcut);
            }
            return false;
        });
        // Return all the shortcuts that should be registered
        return (user
            .concat(defaults)
            .filter(shortcut => !shortcut.disabled)
            // Fix shortcuts comparison in rjsf Form to avoid polluting the user settings
            .map(shortcut => {
            return { args: {}, ...shortcut };
        }));
    }
    SettingRegistry.reconcileShortcuts = reconcileShortcuts;
    /**
     * Merge two set of toolbar items.
     *
     * @param reference Reference set of toolbar items
     * @param addition New items to add
     * @param warn Whether to warn if item is duplicated; default to false
     * @returns The merged set of items
     */
    function reconcileToolbarItems(reference, addition, warn = false) {
        if (!reference) {
            return addition ? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(addition) : undefined;
        }
        if (!addition) {
            return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        }
        const items = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        // Merge array element depending on the type
        addition.forEach(item => {
            // Name must be unique so it's sufficient to only compare it
            const refIndex = items.findIndex(ref => ref.name === item.name);
            if (refIndex < 0) {
                items.push({ ...item });
            }
            else {
                if (warn &&
                    _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepEqual(Object.keys(item), Object.keys(items[refIndex]))) {
                    console.warn(`Toolbar item '${item.name}' is duplicated.`);
                }
                items[refIndex] = { ...items[refIndex], ...item };
            }
        });
        return items;
    }
    SettingRegistry.reconcileToolbarItems = reconcileToolbarItems;
})(SettingRegistry || (SettingRegistry = {}));
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * The default indentation level, uses spaces instead of tabs.
     */
    const indent = '    ';
    /**
     * Replacement text for schema properties missing a `description` field.
     */
    const nondescript = '[missing schema description]';
    /**
     * Replacement text for schema properties missing a `title` field.
     */
    const untitled = '[missing schema title]';
    /**
     * Returns an annotated (JSON with comments) version of a schema's defaults.
     */
    function annotatedDefaults(schema, plugin) {
        const { description, properties, title } = schema;
        const keys = properties
            ? Object.keys(properties).sort((a, b) => a.localeCompare(b))
            : [];
        const length = Math.max((description || nondescript).length, plugin.length);
        return [
            '{',
            prefix(`${title || untitled}`),
            prefix(plugin),
            prefix(description || nondescript),
            prefix('*'.repeat(length)),
            '',
            join(keys.map(key => defaultDocumentedValue(schema, key))),
            '}'
        ].join('\n');
    }
    Private.annotatedDefaults = annotatedDefaults;
    /**
     * Returns an annotated (JSON with comments) version of a plugin's
     * setting data.
     */
    function annotatedPlugin(plugin, data) {
        const { description, title } = plugin.schema;
        const keys = Object.keys(data).sort((a, b) => a.localeCompare(b));
        const length = Math.max((description || nondescript).length, plugin.id.length);
        return [
            '{',
            prefix(`${title || untitled}`),
            prefix(plugin.id),
            prefix(description || nondescript),
            prefix('*'.repeat(length)),
            '',
            join(keys.map(key => documentedValue(plugin.schema, key, data[key]))),
            '}'
        ].join('\n');
    }
    Private.annotatedPlugin = annotatedPlugin;
    /**
     * Returns the default value-with-documentation-string for a
     * specific schema property.
     */
    function defaultDocumentedValue(schema, key) {
        const props = (schema.properties && schema.properties[key]) || {};
        const type = props['type'];
        const description = props['description'] || nondescript;
        const title = props['title'] || '';
        const reified = reifyDefault(schema, key);
        const spaces = indent.length;
        const defaults = reified !== undefined
            ? prefix(`"${key}": ${JSON.stringify(reified, null, spaces)}`, indent)
            : prefix(`"${key}": ${type}`);
        return [prefix(title), prefix(description), defaults]
            .filter(str => str.length)
            .join('\n');
    }
    /**
     * Returns a value-with-documentation-string for a specific schema property.
     */
    function documentedValue(schema, key, value) {
        const props = schema.properties && schema.properties[key];
        const description = (props && props['description']) || nondescript;
        const title = (props && props['title']) || untitled;
        const spaces = indent.length;
        const attribute = prefix(`"${key}": ${JSON.stringify(value, null, spaces)}`, indent);
        return [prefix(title), prefix(description), attribute].join('\n');
    }
    /**
     * Returns a joined string with line breaks and commas where appropriate.
     */
    function join(body) {
        return body.reduce((acc, val, idx) => {
            const rows = val.split('\n');
            const last = rows[rows.length - 1];
            const comment = last.trim().indexOf('//') === 0;
            const comma = comment || idx === body.length - 1 ? '' : ',';
            const separator = idx === body.length - 1 ? '' : '\n\n';
            return acc + val + comma + separator;
        }, '');
    }
    /**
     * Returns a documentation string with a comment prefix added on every line.
     */
    function prefix(source, pre = `${indent}// `) {
        return pre + source.split('\n').join(`\n${pre}`);
    }
    /**
     * Create a fully extrapolated default value for a root key in a schema.
     */
    function reifyDefault(schema, root, definitions) {
        var _a, _b, _c, _d;
        definitions = definitions !== null && definitions !== void 0 ? definitions : schema.definitions;
        // If the property is at the root level, traverse its schema.
        schema = (root ? (_a = schema.properties) === null || _a === void 0 ? void 0 : _a[root] : schema) || {};
        if (schema.type === 'object') {
            // Make a copy of the default value to populate.
            const result = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(schema.default);
            // Iterate through and populate each child property.
            const props = schema.properties || {};
            for (const property in props) {
                result[property] = reifyDefault(props[property], undefined, definitions);
            }
            return result;
        }
        else if (schema.type === 'array') {
            // Make a copy of the default value to populate.
            const result = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(schema.default);
            // Items defines the properties of each item in the array
            let props = schema.items || {};
            // Use referenced definition if one exists
            if (props['$ref'] && definitions) {
                const ref = props['$ref'].replace('#/definitions/', '');
                props = (_b = definitions[ref]) !== null && _b !== void 0 ? _b : {};
            }
            // Iterate through the items in the array and fill in defaults
            for (const item in result) {
                // Use the values that are hard-coded in the default array over the defaults for each field.
                const reified = (_c = reifyDefault(props, undefined, definitions)) !== null && _c !== void 0 ? _c : {};
                for (const prop in reified) {
                    if ((_d = result[item]) === null || _d === void 0 ? void 0 : _d[prop]) {
                        reified[prop] = result[item][prop];
                    }
                }
                result[item] = reified;
            }
            return result;
        }
        else {
            return schema.default;
        }
    }
    Private.reifyDefault = reifyDefault;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/settingregistry/lib/tokens.js":
/*!*************************************************!*\
  !*** ../packages/settingregistry/lib/tokens.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ISettingRegistry": () => (/* binding */ ISettingRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

/**
 * The setting registry token.
 */
const ISettingRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/coreutils:ISettingRegistry', `A service for the JupyterLab settings system.
  Use this if you want to store settings for your application.
  See "schemaDir" for more information.`);


/***/ }),

/***/ "../packages/settingregistry/lib/plugin-schema.json":
/*!**********************************************************!*\
  !*** ../packages/settingregistry/lib/plugin-schema.json ***!
  \**********************************************************/
/***/ ((module) => {

module.exports = JSON.parse('{"$schema":"http://json-schema.org/draft-07/schema","title":"JupyterLab Plugin Settings/Preferences Schema","description":"JupyterLab plugin settings/preferences schema","version":"1.0.0","type":"object","additionalProperties":true,"properties":{"jupyter.lab.internationalization":{"type":"object","properties":{"selectors":{"type":"array","items":{"type":"string","minLength":1}},"domain":{"type":"string","minLength":1}}},"jupyter.lab.menus":{"type":"object","properties":{"main":{"title":"Main menu entries","description":"List of menu items to add to the main menubar.","items":{"$ref":"#/definitions/menu"},"type":"array","default":[]},"context":{"title":"The application context menu.","description":"List of context menu items.","items":{"allOf":[{"$ref":"#/definitions/menuItem"},{"properties":{"selector":{"description":"The CSS selector for the context menu item.","type":"string"}}}]},"type":"array","default":[]}},"additionalProperties":false},"jupyter.lab.metadataforms":{"items":{"$ref":"#/definitions/metadataForm"},"type":"array","default":[]},"jupyter.lab.setting-deprecated":{"type":"boolean","default":false},"jupyter.lab.setting-icon":{"type":"string","default":""},"jupyter.lab.setting-icon-class":{"type":"string","default":""},"jupyter.lab.setting-icon-label":{"type":"string","default":"Plugin"},"jupyter.lab.shortcuts":{"items":{"$ref":"#/definitions/shortcut"},"type":"array","default":[]},"jupyter.lab.toolbars":{"properties":{"^\\\\w[\\\\w-\\\\.]*$":{"items":{"$ref":"#/definitions/toolbarItem"},"type":"array","default":[]}},"type":"object","default":{}},"jupyter.lab.transform":{"type":"boolean","default":false}},"definitions":{"menu":{"properties":{"disabled":{"description":"Whether the menu is disabled or not","type":"boolean","default":false},"icon":{"description":"Menu icon id","type":"string"},"id":{"description":"Menu unique id","oneOf":[{"type":"string","enum":["jp-menu-file","jp-menu-file-new","jp-menu-edit","jp-menu-help","jp-menu-kernel","jp-menu-run","jp-menu-settings","jp-menu-view","jp-menu-tabs"]},{"type":"string","pattern":"[a-z][a-z0-9\\\\-_]+"}]},"items":{"description":"Menu items","type":"array","items":{"$ref":"#/definitions/menuItem"}},"label":{"description":"Menu label","type":"string"},"mnemonic":{"description":"Mnemonic index for the label","type":"number","minimum":-1,"default":-1},"rank":{"description":"Menu rank","type":"number","minimum":0}},"required":["id"],"type":"object"},"menuItem":{"properties":{"args":{"description":"Command arguments","type":"object"},"command":{"description":"Command id","type":"string"},"disabled":{"description":"Whether the item is disabled or not","type":"boolean","default":false},"type":{"description":"Item type","type":"string","enum":["command","submenu","separator"],"default":"command"},"rank":{"description":"Item rank","type":"number","minimum":0},"submenu":{"oneOf":[{"$ref":"#/definitions/menu"},{"type":"null"}]}},"type":"object"},"shortcut":{"properties":{"args":{"title":"The arguments for the command","type":"object"},"command":{"title":"The command id","description":"The command executed when the binding is matched.","type":"string"},"disabled":{"description":"Whether this shortcut is disabled or not.","type":"boolean","default":false},"keys":{"title":"The key sequence for the binding","description":"The key shortcut like `Accel A` or the sequence of shortcuts to press like [`Accel A`, `B`]","items":{"type":"string"},"type":"array"},"macKeys":{"title":"The key sequence for the binding on macOS","description":"The key shortcut like `Cmd A` or the sequence of shortcuts to press like [`Cmd A`, `B`]","items":{"type":"string"},"type":"array"},"winKeys":{"title":"The key sequence for the binding on Windows","description":"The key shortcut like `Ctrl A` or the sequence of shortcuts to press like [`Ctrl A`, `B`]","items":{"type":"string"},"type":"array"},"linuxKeys":{"title":"The key sequence for the binding on Linux","description":"The key shortcut like `Ctrl A` or the sequence of shortcuts to press like [`Ctrl A`, `B`]","items":{"type":"string"},"type":"array"},"selector":{"title":"CSS selector","type":"string"}},"required":["command","keys","selector"],"type":"object"},"toolbarItem":{"properties":{"name":{"title":"Unique name","type":"string"},"args":{"title":"Command arguments","type":"object"},"command":{"title":"Command id","type":"string","default":""},"disabled":{"title":"Whether the item is ignored or not","type":"boolean","default":false},"icon":{"title":"Item icon id","description":"If defined, it will override the command icon","type":"string"},"label":{"title":"Item label","description":"If defined, it will override the command label","type":"string"},"caption":{"title":"Item caption","description":"If defined, it will override the command caption","type":"string"},"type":{"title":"Item type","type":"string","enum":["command","spacer"]},"rank":{"title":"Item rank","type":"number","minimum":0,"default":50}},"required":["name"],"additionalProperties":false,"type":"object"},"metadataForm":{"type":"object","properties":{"id":{"type":"string","description":"The section ID"},"metadataSchema":{"type":"object","items":{"$ref":"#/definitions/metadataSchema"}},"uiSchema":{"type":"object"},"metadataOptions":{"type":"object","items":{"$ref":"#/definitions/metadataOptions"}},"label":{"type":"string","description":"The section label"},"rank":{"type":"integer","description":"The rank of the section in the right panel"},"showModified":{"type":"boolean","description":"Whether to show modified values from defaults"}},"required":["id","metadataSchema"]},"metadataSchema":{"properties":{"properties":{"type":"object","description":"The property set up by extension","properties":{"title":{"type":"string"},"description":{"type":"string"},"type":{"type":"string"}}}},"type":"object","required":["properties"]},"metadataOptions":{"properties":{"customRenderer":{"type":"string"},"metadataLevel":{"type":"string","enum":["cell","notebook"],"default":"cell"},"cellTypes":{"type":"array","items":{"type":"string","enum":["code","markdown","raw"]}},"writeDefault":{"type":"boolean"}},"type":"object"}}}');

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfc2V0dGluZ3JlZ2lzdHJ5X2xpYl9pbmRleF9qcy4wYjU2YmMzNGI0ZDM1N2YwNjBmOC5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBRStCO0FBQ1Q7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNWekIsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUdSO0FBV3hCO0FBQzBDO0FBQ2pCO0FBQ0g7QUFDbEI7QUFDVztBQUcxQzs7R0FFRztBQUNILE1BQU0sSUFBSSxHQUFHLCtEQUFnQixDQUFDO0FBRTlCOzs7R0FHRztBQUNILE1BQU0sbUJBQW1CLEdBQXdCO0lBQy9DOzs7T0FHRztJQUNILE1BQU0sRUFBRSxLQUFLO0NBQ2QsQ0FBQztBQUVGOztHQUVHO0FBQ0gsTUFBTSxnQkFBZ0IsR0FBRyxNQUFNLENBQUMsWUFBWSxDQUFDLEVBQUUsQ0FBQyxDQUFDO0FBK0VqRDs7R0FFRztBQUNJLE1BQU0sc0JBQXNCO0lBQ2pDOztPQUVHO0lBQ0g7UUFpSVEsY0FBUyxHQUFRLElBQUksNENBQUcsQ0FBQztZQUMvQixXQUFXLEVBQUUsSUFBSTtZQUNqQixHQUFHLG1CQUFtQjtTQUN2QixDQUFDLENBQUM7UUFDSyxlQUFVLEdBQVEsSUFBSSw0Q0FBRyxDQUFDLEVBQUUsR0FBRyxtQkFBbUIsRUFBRSxDQUFDLENBQUM7UUFwSTVELElBQUksQ0FBQyxTQUFTLENBQUMsU0FBUyxDQUFDLGdEQUFNLEVBQUUsMEJBQTBCLENBQUMsQ0FBQztRQUM3RCxJQUFJLENBQUMsVUFBVSxDQUFDLFNBQVMsQ0FBQyxnREFBTSxFQUFFLDBCQUEwQixDQUFDLENBQUM7SUFDaEUsQ0FBQztJQUVEOzs7Ozs7Ozs7OztPQVdHO0lBQ0gsWUFBWSxDQUNWLE1BQWdDLEVBQ2hDLFFBQVEsR0FBRyxJQUFJO1FBRWYsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLFVBQVUsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLEVB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YUFDeEI7WUFFRCxPQUFPLE1BQU0sQ0FBQztTQUNmO2FBQU07WUFDTCxPQUFPLE1BQU0sQ0FBQyxPQUFPLENBQUM7U0FDdkI7SUFDSCxDQUFDO0lBeERlLG9CQUFZLGVBd0QzQjtBQUNILENBQUMsRUFsTVMsT0FBTyxLQUFQLE9BQU8sUUFrTWhCOzs7Ozs7Ozs7Ozs7Ozs7OztBQ3o5Q0Q7OzsrRUFHK0U7QUFVcEQ7QUFNM0I7O0dBRUc7QUFDSSxNQUFNLGdCQUFnQixHQUFHLElBQUksb0RBQUssQ0FDdkMsd0NBQXdDLEVBQ3hDOzt3Q0FFc0MsQ0FDdkMsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zZXR0aW5ncmVnaXN0cnkvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zZXR0aW5ncmVnaXN0cnkvc3JjL3NldHRpbmdyZWdpc3RyeS50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ3JlZ2lzdHJ5L3NyYy90b2tlbnMudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBzZXR0aW5ncmVnaXN0cnlcbiAqL1xuXG5leHBvcnQgKiBmcm9tICcuL3NldHRpbmdyZWdpc3RyeSc7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElEYXRhQ29ubmVjdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc3RhdGVkYic7XG5pbXBvcnQgeyBDb21tYW5kUmVnaXN0cnkgfSBmcm9tICdAbHVtaW5vL2NvbW1hbmRzJztcbmltcG9ydCB7XG4gIEpTT05FeHQsXG4gIEpTT05PYmplY3QsXG4gIEpTT05WYWx1ZSxcbiAgUGFydGlhbEpTT05BcnJheSxcbiAgUGFydGlhbEpTT05PYmplY3QsXG4gIFBhcnRpYWxKU09OVmFsdWUsXG4gIFJlYWRvbmx5SlNPTk9iamVjdCxcbiAgUmVhZG9ubHlQYXJ0aWFsSlNPTk9iamVjdCxcbiAgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERpc3Bvc2FibGVEZWxlZ2F0ZSwgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IEFqdiwgeyBPcHRpb25zIGFzIEFqdk9wdGlvbnMgfSBmcm9tICdhanYnO1xuaW1wb3J0ICogYXMganNvbjUgZnJvbSAnanNvbjUnO1xuaW1wb3J0IFNDSEVNQSBmcm9tICcuL3BsdWdpbi1zY2hlbWEuanNvbic7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEFuIGFsaWFzIGZvciB0aGUgSlNPTiBkZWVwIGNvcHkgZnVuY3Rpb24uXG4gKi9cbmNvbnN0IGNvcHkgPSBKU09ORXh0LmRlZXBDb3B5O1xuXG4vKiogRGVmYXVsdCBhcmd1bWVudHMgZm9yIEFqdiBpbnN0YW5jZXMuXG4gKlxuICogaHR0cHM6Ly9hanYuanMub3JnL29wdGlvbnMuaHRtbFxuICovXG5jb25zdCBBSlZfREVGQVVMVF9PUFRJT05TOiBQYXJ0aWFsPEFqdk9wdGlvbnM+ID0ge1xuICAvKipcbiAgICogQHRvZG8gdGhlIGltcGxpY2F0aW9ucyBvZiBlbmFibGluZyBzdHJpY3QgbW9kZSBhcmUgYmV5b25kIHRoZSBzY29wZSBvZlxuICAgKiAgICAgICB0aGUgaW5pdGlhbCBQUlxuICAgKi9cbiAgc3RyaWN0OiBmYWxzZVxufTtcblxuLyoqXG4gKiBUaGUgQVNDSUkgcmVjb3JkIHNlcGFyYXRvciBjaGFyYWN0ZXIuXG4gKi9cbmNvbnN0IFJFQ09SRF9TRVBBUkFUT1IgPSBTdHJpbmcuZnJvbUNoYXJDb2RlKDMwKTtcblxuLyoqXG4gKiBBbiBpbXBsZW1lbnRhdGlvbiBvZiBhIHNjaGVtYSB2YWxpZGF0b3IuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVNjaGVtYVZhbGlkYXRvciB7XG4gIC8qKlxuICAgKiBWYWxpZGF0ZSBhIHBsdWdpbidzIHNjaGVtYSBhbmQgdXNlciBkYXRhOyBwb3B1bGF0ZSB0aGUgYGNvbXBvc2l0ZWAgZGF0YS5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBwbHVnaW4gYmVpbmcgdmFsaWRhdGVkLiBJdHMgYGNvbXBvc2l0ZWAgZGF0YSB3aWxsIGJlXG4gICAqIHBvcHVsYXRlZCBieSByZWZlcmVuY2UuXG4gICAqXG4gICAqIEBwYXJhbSBwb3B1bGF0ZSAtIFdoZXRoZXIgcGx1Z2luIGRhdGEgc2hvdWxkIGJlIHBvcHVsYXRlZCwgZGVmYXVsdHMgdG9cbiAgICogYHRydWVgLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGxpc3Qgb2YgZXJyb3JzIGlmIGVpdGhlciB0aGUgc2NoZW1hIG9yIGRhdGEgZmFpbCB0byB2YWxpZGF0ZSBvclxuICAgKiBgbnVsbGAgaWYgdGhlcmUgYXJlIG5vIGVycm9ycy5cbiAgICovXG4gIHZhbGlkYXRlRGF0YShcbiAgICBwbHVnaW46IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbixcbiAgICBwb3B1bGF0ZT86IGJvb2xlYW5cbiAgKTogSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXSB8IG51bGw7XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHNjaGVtYSB2YWxpZGF0b3IgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJU2NoZW1hVmFsaWRhdG9yIHtcbiAgLyoqXG4gICAqIEEgc2NoZW1hIHZhbGlkYXRpb24gZXJyb3IgZGVmaW5pdGlvbi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUVycm9yIHtcbiAgICAvKipcbiAgICAgKiBUaGUga2V5d29yZCB3aG9zZSB2YWxpZGF0aW9uIGZhaWxlZC5cbiAgICAgKi9cbiAgICBrZXl3b3JkOiBzdHJpbmcgfCBzdHJpbmdbXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBlcnJvciBtZXNzYWdlLlxuICAgICAqL1xuICAgIG1lc3NhZ2U/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBPcHRpb25hbCBwYXJhbWV0ZXIgbWV0YWRhdGEgdGhhdCBtaWdodCBiZSBpbmNsdWRlZCBpbiBhbiBlcnJvci5cbiAgICAgKi9cbiAgICBwYXJhbXM/OiBSZWFkb25seUpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcGF0aCBpbiB0aGUgc2NoZW1hIHdoZXJlIHRoZSBlcnJvciBvY2N1cnJlZC5cbiAgICAgKi9cbiAgICBzY2hlbWFQYXRoOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBAdG9kbyBoYW5kbGUgbmV3IGZpZWxkcyBmcm9tIGFqdjhcbiAgICAgKiovXG4gICAgc2NoZW1hPzogdW5rbm93bjtcblxuICAgIC8qKlxuICAgICAqIEB0b2RvIGhhbmRsZSBuZXcgZmllbGRzIGZyb20gYWp2OFxuICAgICAqKi9cbiAgICBpbnN0YW5jZVBhdGg6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEB0b2RvIGhhbmRsZSBuZXcgZmllbGRzIGZyb20gYWp2OFxuICAgICAqKi9cbiAgICBwcm9wZXJ0eU5hbWU/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBAdG9kbyBoYW5kbGUgbmV3IGZpZWxkcyBmcm9tIGFqdjhcbiAgICAgKiovXG4gICAgZGF0YT86IHVua25vd247XG5cbiAgICAvKipcbiAgICAgKiBAdG9kbyBoYW5kbGUgbmV3IGZpZWxkcyBmcm9tIGFqdjhcbiAgICAgKiovXG4gICAgcGFyZW50U2NoZW1hPzogdW5rbm93bjtcbiAgfVxufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGltcGxlbWVudGF0aW9uIG9mIGEgc2NoZW1hIHZhbGlkYXRvci5cbiAqL1xuZXhwb3J0IGNsYXNzIERlZmF1bHRTY2hlbWFWYWxpZGF0b3IgaW1wbGVtZW50cyBJU2NoZW1hVmFsaWRhdG9yIHtcbiAgLyoqXG4gICAqIEluc3RhbnRpYXRlIGEgc2NoZW1hIHZhbGlkYXRvci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKCkge1xuICAgIHRoaXMuX2NvbXBvc2VyLmFkZFNjaGVtYShTQ0hFTUEsICdqdXB5dGVybGFiLXBsdWdpbi1zY2hlbWEnKTtcbiAgICB0aGlzLl92YWxpZGF0b3IuYWRkU2NoZW1hKFNDSEVNQSwgJ2p1cHl0ZXJsYWItcGx1Z2luLXNjaGVtYScpO1xuICB9XG5cbiAgLyoqXG4gICAqIFZhbGlkYXRlIGEgcGx1Z2luJ3Mgc2NoZW1hIGFuZCB1c2VyIGRhdGE7IHBvcHVsYXRlIHRoZSBgY29tcG9zaXRlYCBkYXRhLlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIHBsdWdpbiBiZWluZyB2YWxpZGF0ZWQuIEl0cyBgY29tcG9zaXRlYCBkYXRhIHdpbGwgYmVcbiAgICogcG9wdWxhdGVkIGJ5IHJlZmVyZW5jZS5cbiAgICpcbiAgICogQHBhcmFtIHBvcHVsYXRlIC0gV2hldGhlciBwbHVnaW4gZGF0YSBzaG91bGQgYmUgcG9wdWxhdGVkLCBkZWZhdWx0cyB0b1xuICAgKiBgdHJ1ZWAuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgbGlzdCBvZiBlcnJvcnMgaWYgZWl0aGVyIHRoZSBzY2hlbWEgb3IgZGF0YSBmYWlsIHRvIHZhbGlkYXRlIG9yXG4gICAqIGBudWxsYCBpZiB0aGVyZSBhcmUgbm8gZXJyb3JzLlxuICAgKi9cbiAgdmFsaWRhdGVEYXRhKFxuICAgIHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLFxuICAgIHBvcHVsYXRlID0gdHJ1ZVxuICApOiBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdIHwgbnVsbCB7XG4gICAgY29uc3QgdmFsaWRhdGUgPSB0aGlzLl92YWxpZGF0b3IuZ2V0U2NoZW1hKHBsdWdpbi5pZCk7XG4gICAgY29uc3QgY29tcG9zZSA9IHRoaXMuX2NvbXBvc2VyLmdldFNjaGVtYShwbHVnaW4uaWQpO1xuXG4gICAgLy8gSWYgdGhlIHNjaGVtYXMgZG8gbm90IGV4aXN0LCBhZGQgdGhlbSB0byB0aGUgdmFsaWRhdG9yIGFuZCBjb250aW51ZS5cbiAgICBpZiAoIXZhbGlkYXRlIHx8ICFjb21wb3NlKSB7XG4gICAgICBpZiAocGx1Z2luLnNjaGVtYS50eXBlICE9PSAnb2JqZWN0Jykge1xuICAgICAgICBjb25zdCBrZXl3b3JkID0gJ3NjaGVtYSc7XG4gICAgICAgIGNvbnN0IG1lc3NhZ2UgPVxuICAgICAgICAgIGBTZXR0aW5nIHJlZ2lzdHJ5IHNjaGVtYXMnIHJvb3QtbGV2ZWwgdHlwZSBtdXN0IGJlIGAgK1xuICAgICAgICAgIGAnb2JqZWN0JywgcmVqZWN0aW5nIHR5cGU6ICR7cGx1Z2luLnNjaGVtYS50eXBlfWA7XG5cbiAgICAgICAgcmV0dXJuIFt7IGluc3RhbmNlUGF0aDogJ3R5cGUnLCBrZXl3b3JkLCBzY2hlbWFQYXRoOiAnJywgbWVzc2FnZSB9XTtcbiAgICAgIH1cblxuICAgICAgY29uc3QgZXJyb3JzID0gdGhpcy5fYWRkU2NoZW1hKHBsdWdpbi5pZCwgcGx1Z2luLnNjaGVtYSk7XG5cbiAgICAgIHJldHVybiBlcnJvcnMgfHwgdGhpcy52YWxpZGF0ZURhdGEocGx1Z2luKTtcbiAgICB9XG5cbiAgICAvLyBQYXJzZSB0aGUgcmF3IGNvbW1lbnRlZCBKU09OIGludG8gYSB1c2VyIG1hcC5cbiAgICBsZXQgdXNlcjogSlNPTk9iamVjdDtcbiAgICB0cnkge1xuICAgICAgdXNlciA9IGpzb241LnBhcnNlKHBsdWdpbi5yYXcpIGFzIEpTT05PYmplY3Q7XG4gICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgIGlmIChlcnJvciBpbnN0YW5jZW9mIFN5bnRheEVycm9yKSB7XG4gICAgICAgIHJldHVybiBbXG4gICAgICAgICAge1xuICAgICAgICAgICAgaW5zdGFuY2VQYXRoOiAnJyxcbiAgICAgICAgICAgIGtleXdvcmQ6ICdzeW50YXgnLFxuICAgICAgICAgICAgc2NoZW1hUGF0aDogJycsXG4gICAgICAgICAgICBtZXNzYWdlOiBlcnJvci5tZXNzYWdlXG4gICAgICAgICAgfVxuICAgICAgICBdO1xuICAgICAgfVxuXG4gICAgICBjb25zdCB7IGNvbHVtbiwgZGVzY3JpcHRpb24gfSA9IGVycm9yO1xuICAgICAgY29uc3QgbGluZSA9IGVycm9yLmxpbmVOdW1iZXI7XG5cbiAgICAgIHJldHVybiBbXG4gICAgICAgIHtcbiAgICAgICAgICBpbnN0YW5jZVBhdGg6ICcnLFxuICAgICAgICAgIGtleXdvcmQ6ICdwYXJzZScsXG4gICAgICAgICAgc2NoZW1hUGF0aDogJycsXG4gICAgICAgICAgbWVzc2FnZTogYCR7ZGVzY3JpcHRpb259IChsaW5lICR7bGluZX0gY29sdW1uICR7Y29sdW1ufSlgXG4gICAgICAgIH1cbiAgICAgIF07XG4gICAgfVxuXG4gICAgaWYgKCF2YWxpZGF0ZSh1c2VyKSkge1xuICAgICAgcmV0dXJuIHZhbGlkYXRlLmVycm9ycyBhcyBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdO1xuICAgIH1cblxuICAgIC8vIENvcHkgdGhlIHVzZXIgZGF0YSBiZWZvcmUgbWVyZ2luZyBkZWZhdWx0cyBpbnRvIGNvbXBvc2l0ZSBtYXAuXG4gICAgY29uc3QgY29tcG9zaXRlID0gY29weSh1c2VyKTtcblxuICAgIGlmICghY29tcG9zZShjb21wb3NpdGUpKSB7XG4gICAgICByZXR1cm4gY29tcG9zZS5lcnJvcnMgYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXTtcbiAgICB9XG5cbiAgICBpZiAocG9wdWxhdGUpIHtcbiAgICAgIHBsdWdpbi5kYXRhID0geyBjb21wb3NpdGUsIHVzZXIgfTtcbiAgICB9XG5cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSBzY2hlbWEgdG8gdGhlIHZhbGlkYXRvci5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBwbHVnaW4gSUQuXG4gICAqXG4gICAqIEBwYXJhbSBzY2hlbWEgLSBUaGUgc2NoZW1hIGJlaW5nIGFkZGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGxpc3Qgb2YgZXJyb3JzIGlmIHRoZSBzY2hlbWEgZmFpbHMgdG8gdmFsaWRhdGUgb3IgYG51bGxgIGlmIHRoZXJlXG4gICAqIGFyZSBubyBlcnJvcnMuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogSXQgaXMgc2FmZSB0byBjYWxsIHRoaXMgZnVuY3Rpb24gbXVsdGlwbGUgdGltZXMgd2l0aCB0aGUgc2FtZSBwbHVnaW4gbmFtZS5cbiAgICovXG4gIHByaXZhdGUgX2FkZFNjaGVtYShcbiAgICBwbHVnaW46IHN0cmluZyxcbiAgICBzY2hlbWE6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYVxuICApOiBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdIHwgbnVsbCB7XG4gICAgY29uc3QgY29tcG9zZXIgPSB0aGlzLl9jb21wb3NlcjtcbiAgICBjb25zdCB2YWxpZGF0b3IgPSB0aGlzLl92YWxpZGF0b3I7XG4gICAgY29uc3QgdmFsaWRhdGUgPSB2YWxpZGF0b3IuZ2V0U2NoZW1hKCdqdXB5dGVybGFiLXBsdWdpbi1zY2hlbWEnKSE7XG5cbiAgICAvLyBWYWxpZGF0ZSBhZ2FpbnN0IHRoZSBtYWluIHNjaGVtYS5cbiAgICBpZiAoISh2YWxpZGF0ZSEoc2NoZW1hKSBhcyBib29sZWFuKSkge1xuICAgICAgcmV0dXJuIHZhbGlkYXRlIS5lcnJvcnMgYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXTtcbiAgICB9XG5cbiAgICAvLyBWYWxpZGF0ZSBhZ2FpbnN0IHRoZSBKU09OIHNjaGVtYSBtZXRhLXNjaGVtYS5cbiAgICBpZiAoISh2YWxpZGF0b3IudmFsaWRhdGVTY2hlbWEoc2NoZW1hKSBhcyBib29sZWFuKSkge1xuICAgICAgcmV0dXJuIHZhbGlkYXRvci5lcnJvcnMgYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXTtcbiAgICB9XG5cbiAgICAvLyBSZW1vdmUgaWYgc2NoZW1hIGFscmVhZHkgZXhpc3RzLlxuICAgIGNvbXBvc2VyLnJlbW92ZVNjaGVtYShwbHVnaW4pO1xuICAgIHZhbGlkYXRvci5yZW1vdmVTY2hlbWEocGx1Z2luKTtcblxuICAgIC8vIEFkZCBzY2hlbWEgdG8gdGhlIHZhbGlkYXRvciBhbmQgY29tcG9zZXIuXG4gICAgY29tcG9zZXIuYWRkU2NoZW1hKHNjaGVtYSwgcGx1Z2luKTtcbiAgICB2YWxpZGF0b3IuYWRkU2NoZW1hKHNjaGVtYSwgcGx1Z2luKTtcblxuICAgIHJldHVybiBudWxsO1xuICB9XG5cbiAgcHJpdmF0ZSBfY29tcG9zZXI6IEFqdiA9IG5ldyBBanYoe1xuICAgIHVzZURlZmF1bHRzOiB0cnVlLFxuICAgIC4uLkFKVl9ERUZBVUxUX09QVElPTlNcbiAgfSk7XG4gIHByaXZhdGUgX3ZhbGlkYXRvcjogQWp2ID0gbmV3IEFqdih7IC4uLkFKVl9ERUZBVUxUX09QVElPTlMgfSk7XG59XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgY29uY3JldGUgaW1wbGVtZW50YXRpb24gb2YgYSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICovXG5leHBvcnQgY2xhc3MgU2V0dGluZ1JlZ2lzdHJ5IGltcGxlbWVudHMgSVNldHRpbmdSZWdpc3RyeSB7XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IFNldHRpbmdSZWdpc3RyeS5JT3B0aW9ucykge1xuICAgIHRoaXMuY29ubmVjdG9yID0gb3B0aW9ucy5jb25uZWN0b3I7XG4gICAgdGhpcy52YWxpZGF0b3IgPSBvcHRpb25zLnZhbGlkYXRvciB8fCBuZXcgRGVmYXVsdFNjaGVtYVZhbGlkYXRvcigpO1xuXG4gICAgLy8gUGx1Z2lucyB3aXRoIHRyYW5zZm9ybWF0aW9uIG1heSBub3QgYmUgbG9hZGVkIGlmIHRoZSB0cmFuc2Zvcm1hdGlvbiBmdW5jdGlvbiBpc1xuICAgIC8vIG5vdCB5ZXQgYXZhaWxhYmxlLiBUbyBhdm9pZCBmZXRjaGluZyBhZ2FpbiB0aGUgYXNzb2NpYXRlZCBkYXRhIHdoZW4gdGhlIHRyYW5zZm9ybWF0aW9uXG4gICAgLy8gZnVuY3Rpb24gaXMgYXZhaWxhYmxlLCB0aGUgcGx1Z2luIGRhdGEgaXMga2VwdCBpbiBjYWNoZS5cbiAgICBpZiAob3B0aW9ucy5wbHVnaW5zKSB7XG4gICAgICBvcHRpb25zLnBsdWdpbnNcbiAgICAgICAgLmZpbHRlcihwbHVnaW4gPT4gcGx1Z2luLnNjaGVtYVsnanVweXRlci5sYWIudHJhbnNmb3JtJ10pXG4gICAgICAgIC5mb3JFYWNoKHBsdWdpbiA9PiB0aGlzLl91bmxvYWRlZFBsdWdpbnMuc2V0KHBsdWdpbi5pZCwgcGx1Z2luKSk7XG5cbiAgICAgIC8vIFByZWxvYWQgd2l0aCBhbnkgYXZhaWxhYmxlIGRhdGEgYXQgaW5zdGFudGlhdGlvbi10aW1lLlxuICAgICAgdGhpcy5fcmVhZHkgPSB0aGlzLl9wcmVsb2FkKG9wdGlvbnMucGx1Z2lucyk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBkYXRhIGNvbm5lY3RvciB1c2VkIGJ5IHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcmVhZG9ubHkgY29ubmVjdG9yOiBJRGF0YUNvbm5lY3RvcjxJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4sIHN0cmluZywgc3RyaW5nPjtcblxuICAvKipcbiAgICogVGhlIHNjaGVtYSBvZiB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIHJlYWRvbmx5IHNjaGVtYSA9IFNDSEVNQSBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWE7XG5cbiAgLyoqXG4gICAqIFRoZSBzY2hlbWEgdmFsaWRhdG9yIHVzZWQgYnkgdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAqL1xuICByZWFkb25seSB2YWxpZGF0b3I6IElTY2hlbWFWYWxpZGF0b3I7XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIHRoYXQgZW1pdHMgdGhlIG5hbWUgb2YgYSBwbHVnaW4gd2hlbiBpdHMgc2V0dGluZ3MgY2hhbmdlLlxuICAgKi9cbiAgZ2V0IHBsdWdpbkNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBzdHJpbmc+IHtcbiAgICByZXR1cm4gdGhpcy5fcGx1Z2luQ2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29sbGVjdGlvbiBvZiBzZXR0aW5nIHJlZ2lzdHJ5IHBsdWdpbnMuXG4gICAqL1xuICByZWFkb25seSBwbHVnaW5zOiB7XG4gICAgW25hbWU6IHN0cmluZ106IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbjtcbiAgfSA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpbmRpdmlkdWFsIHNldHRpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyByZXRyaWV2ZWQuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSBUaGUgbmFtZSBvZiB0aGUgc2V0dGluZyBiZWluZyByZXRyaWV2ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmV0cmlldmVkLlxuICAgKi9cbiAgYXN5bmMgZ2V0KFxuICAgIHBsdWdpbjogc3RyaW5nLFxuICAgIGtleTogc3RyaW5nXG4gICk6IFByb21pc2U8e1xuICAgIGNvbXBvc2l0ZTogUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgICB1c2VyOiBQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkO1xuICB9PiB7XG4gICAgLy8gV2FpdCBmb3IgZGF0YSBwcmVsb2FkIGJlZm9yZSBhbGxvd2luZyBub3JtYWwgb3BlcmF0aW9uLlxuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuXG4gICAgY29uc3QgcGx1Z2lucyA9IHRoaXMucGx1Z2lucztcblxuICAgIGlmIChwbHVnaW4gaW4gcGx1Z2lucykge1xuICAgICAgY29uc3QgeyBjb21wb3NpdGUsIHVzZXIgfSA9IHBsdWdpbnNbcGx1Z2luXS5kYXRhO1xuXG4gICAgICByZXR1cm4ge1xuICAgICAgICBjb21wb3NpdGU6XG4gICAgICAgICAgY29tcG9zaXRlW2tleV0gIT09IHVuZGVmaW5lZCA/IGNvcHkoY29tcG9zaXRlW2tleV0hKSA6IHVuZGVmaW5lZCxcbiAgICAgICAgdXNlcjogdXNlcltrZXldICE9PSB1bmRlZmluZWQgPyBjb3B5KHVzZXJba2V5XSEpIDogdW5kZWZpbmVkXG4gICAgICB9O1xuICAgIH1cblxuICAgIHJldHVybiB0aGlzLmxvYWQocGx1Z2luKS50aGVuKCgpID0+IHRoaXMuZ2V0KHBsdWdpbiwga2V5KSk7XG4gIH1cblxuICAvKipcbiAgICogTG9hZCBhIHBsdWdpbidzIHNldHRpbmdzIGludG8gdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyBsb2FkZWQuXG4gICAqXG4gICAqIEBwYXJhbSBmb3JjZVRyYW5zZm9ybSAtIEFuIG9wdGlvbmFsIHBhcmFtZXRlciB0byBmb3JjZSByZXBsYXkgdGhlIHRyYW5zZm9ybXMgbWV0aG9kcy5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2l0aCBhIHBsdWdpbiBzZXR0aW5ncyBvYmplY3Qgb3IgcmVqZWN0c1xuICAgKiBpZiB0aGUgcGx1Z2luIGlzIG5vdCBmb3VuZC5cbiAgICovXG4gIGFzeW5jIGxvYWQoXG4gICAgcGx1Z2luOiBzdHJpbmcsXG4gICAgZm9yY2VUcmFuc2Zvcm06IGJvb2xlYW4gPSBmYWxzZVxuICApOiBQcm9taXNlPElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzPiB7XG4gICAgLy8gV2FpdCBmb3IgZGF0YSBwcmVsb2FkIGJlZm9yZSBhbGxvd2luZyBub3JtYWwgb3BlcmF0aW9uLlxuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuXG4gICAgY29uc3QgcGx1Z2lucyA9IHRoaXMucGx1Z2lucztcbiAgICBjb25zdCByZWdpc3RyeSA9IHRoaXM7IC8vIGVzbGludC1kaXNhYmxlLWxpbmVcblxuICAgIC8vIElmIHRoZSBwbHVnaW4gZXhpc3RzLCByZXNvbHZlLlxuICAgIGlmIChwbHVnaW4gaW4gcGx1Z2lucykge1xuICAgICAgLy8gRm9yY2UgcmVwbGF5aW5nIHRoZSB0cmFuc2Zvcm0gZnVuY3Rpb24gaWYgZXhwZWN0ZWQuXG4gICAgICBpZiAoZm9yY2VUcmFuc2Zvcm0pIHtcbiAgICAgICAgLy8gRW1wdHkgdGhlIGNvbXBvc2l0ZSBhbmQgdXNlciBkYXRhIGJlZm9yZSByZXBsYXlpbmcgdGhlIHRyYW5zZm9ybXMuXG4gICAgICAgIHBsdWdpbnNbcGx1Z2luXS5kYXRhID0geyBjb21wb3NpdGU6IHt9LCB1c2VyOiB7fSB9O1xuICAgICAgICBhd2FpdCB0aGlzLl9sb2FkKGF3YWl0IHRoaXMuX3RyYW5zZm9ybSgnZmV0Y2gnLCBwbHVnaW5zW3BsdWdpbl0pKTtcbiAgICAgICAgdGhpcy5fcGx1Z2luQ2hhbmdlZC5lbWl0KHBsdWdpbik7XG4gICAgICB9XG4gICAgICByZXR1cm4gbmV3IFNldHRpbmdzKHsgcGx1Z2luOiBwbHVnaW5zW3BsdWdpbl0sIHJlZ2lzdHJ5IH0pO1xuICAgIH1cblxuICAgIC8vIElmIHRoZSBwbHVnaW4gaXMgbm90IGxvYWRlZCBidXQgaGFzIGFscmVhZHkgYmVlbiBmZXRjaGVkLlxuICAgIGlmICh0aGlzLl91bmxvYWRlZFBsdWdpbnMuaGFzKHBsdWdpbikgJiYgcGx1Z2luIGluIHRoaXMuX3RyYW5zZm9ybWVycykge1xuICAgICAgYXdhaXQgdGhpcy5fbG9hZChcbiAgICAgICAgYXdhaXQgdGhpcy5fdHJhbnNmb3JtKCdmZXRjaCcsIHRoaXMuX3VubG9hZGVkUGx1Z2lucy5nZXQocGx1Z2luKSEpXG4gICAgICApO1xuICAgICAgaWYgKHBsdWdpbiBpbiBwbHVnaW5zKSB7XG4gICAgICAgIHRoaXMuX3BsdWdpbkNoYW5nZWQuZW1pdChwbHVnaW4pO1xuICAgICAgICB0aGlzLl91bmxvYWRlZFBsdWdpbnMuZGVsZXRlKHBsdWdpbik7XG4gICAgICAgIHJldHVybiBuZXcgU2V0dGluZ3MoeyBwbHVnaW46IHBsdWdpbnNbcGx1Z2luXSwgcmVnaXN0cnkgfSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gSWYgdGhlIHBsdWdpbiBuZWVkcyB0byBiZSBsb2FkZWQgZnJvbSB0aGUgZGF0YSBjb25uZWN0b3IsIGZldGNoLlxuICAgIHJldHVybiB0aGlzLnJlbG9hZChwbHVnaW4pO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbG9hZCBhIHBsdWdpbidzIHNldHRpbmdzIGludG8gdGhlIHJlZ2lzdHJ5IGV2ZW4gaWYgdGhleSBhbHJlYWR5IGV4aXN0LlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIG5hbWUgb2YgdGhlIHBsdWdpbiB3aG9zZSBzZXR0aW5ncyBhcmUgYmVpbmcgcmVsb2FkZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdpdGggYSBwbHVnaW4gc2V0dGluZ3Mgb2JqZWN0IG9yIHJlamVjdHNcbiAgICogd2l0aCBhIGxpc3Qgb2YgYElTY2hlbWFWYWxpZGF0b3IuSUVycm9yYCBvYmplY3RzIGlmIGl0IGZhaWxzLlxuICAgKi9cbiAgYXN5bmMgcmVsb2FkKHBsdWdpbjogc3RyaW5nKTogUHJvbWlzZTxJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncz4ge1xuICAgIC8vIFdhaXQgZm9yIGRhdGEgcHJlbG9hZCBiZWZvcmUgYWxsb3dpbmcgbm9ybWFsIG9wZXJhdGlvbi5cbiAgICBhd2FpdCB0aGlzLl9yZWFkeTtcblxuICAgIGNvbnN0IGZldGNoZWQgPSBhd2FpdCB0aGlzLmNvbm5lY3Rvci5mZXRjaChwbHVnaW4pO1xuICAgIGNvbnN0IHBsdWdpbnMgPSB0aGlzLnBsdWdpbnM7IC8vIGVzbGludC1kaXNhYmxlLWxpbmVcbiAgICBjb25zdCByZWdpc3RyeSA9IHRoaXM7IC8vIGVzbGludC1kaXNhYmxlLWxpbmVcblxuICAgIGlmIChmZXRjaGVkID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHRocm93IFtcbiAgICAgICAge1xuICAgICAgICAgIGluc3RhbmNlUGF0aDogJycsXG4gICAgICAgICAga2V5d29yZDogJ2lkJyxcbiAgICAgICAgICBtZXNzYWdlOiBgQ291bGQgbm90IGZldGNoIHNldHRpbmdzIGZvciAke3BsdWdpbn0uYCxcbiAgICAgICAgICBzY2hlbWFQYXRoOiAnJ1xuICAgICAgICB9IGFzIElTY2hlbWFWYWxpZGF0b3IuSUVycm9yXG4gICAgICBdO1xuICAgIH1cbiAgICBhd2FpdCB0aGlzLl9sb2FkKGF3YWl0IHRoaXMuX3RyYW5zZm9ybSgnZmV0Y2gnLCBmZXRjaGVkKSk7XG4gICAgdGhpcy5fcGx1Z2luQ2hhbmdlZC5lbWl0KHBsdWdpbik7XG5cbiAgICByZXR1cm4gbmV3IFNldHRpbmdzKHsgcGx1Z2luOiBwbHVnaW5zW3BsdWdpbl0sIHJlZ2lzdHJ5IH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIHNpbmdsZSBzZXR0aW5nIGluIHRoZSByZWdpc3RyeS5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZyBpcyBiZWluZyByZW1vdmVkLlxuICAgKlxuICAgKiBAcGFyYW0ga2V5IC0gVGhlIG5hbWUgb2YgdGhlIHNldHRpbmcgYmVpbmcgcmVtb3ZlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgc2V0dGluZyBpcyByZW1vdmVkLlxuICAgKi9cbiAgYXN5bmMgcmVtb3ZlKHBsdWdpbjogc3RyaW5nLCBrZXk6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIC8vIFdhaXQgZm9yIGRhdGEgcHJlbG9hZCBiZWZvcmUgYWxsb3dpbmcgbm9ybWFsIG9wZXJhdGlvbi5cbiAgICBhd2FpdCB0aGlzLl9yZWFkeTtcblxuICAgIGNvbnN0IHBsdWdpbnMgPSB0aGlzLnBsdWdpbnM7XG5cbiAgICBpZiAoIShwbHVnaW4gaW4gcGx1Z2lucykpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCByYXcgPSBqc29uNS5wYXJzZShwbHVnaW5zW3BsdWdpbl0ucmF3KTtcblxuICAgIC8vIERlbGV0ZSBib3RoIHRoZSB2YWx1ZSBhbmQgYW55IGFzc29jaWF0ZWQgY29tbWVudC5cbiAgICBkZWxldGUgcmF3W2tleV07XG4gICAgZGVsZXRlIHJhd1tgLy8gJHtrZXl9YF07XG4gICAgcGx1Z2luc1twbHVnaW5dLnJhdyA9IFByaXZhdGUuYW5ub3RhdGVkUGx1Z2luKHBsdWdpbnNbcGx1Z2luXSwgcmF3KTtcblxuICAgIHJldHVybiB0aGlzLl9zYXZlKHBsdWdpbik7XG4gIH1cblxuICAvKipcbiAgICogU2V0IGEgc2luZ2xlIHNldHRpbmcgaW4gdGhlIHJlZ2lzdHJ5LlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIG5hbWUgb2YgdGhlIHBsdWdpbiB3aG9zZSBzZXR0aW5nIGlzIGJlaW5nIHNldC5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHNldC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIHZhbHVlIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHNldC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgc2V0dGluZyBoYXMgYmVlbiBzYXZlZC5cbiAgICpcbiAgICovXG4gIGFzeW5jIHNldChwbHVnaW46IHN0cmluZywga2V5OiBzdHJpbmcsIHZhbHVlOiBKU09OVmFsdWUpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAvLyBXYWl0IGZvciBkYXRhIHByZWxvYWQgYmVmb3JlIGFsbG93aW5nIG5vcm1hbCBvcGVyYXRpb24uXG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG5cbiAgICBjb25zdCBwbHVnaW5zID0gdGhpcy5wbHVnaW5zO1xuXG4gICAgaWYgKCEocGx1Z2luIGluIHBsdWdpbnMpKSB7XG4gICAgICByZXR1cm4gdGhpcy5sb2FkKHBsdWdpbikudGhlbigoKSA9PiB0aGlzLnNldChwbHVnaW4sIGtleSwgdmFsdWUpKTtcbiAgICB9XG5cbiAgICAvLyBQYXJzZSB0aGUgcmF3IEpTT04gc3RyaW5nIHJlbW92aW5nIGFsbCBjb21tZW50cyBhbmQgcmV0dXJuIGFuIG9iamVjdC5cbiAgICBjb25zdCByYXcgPSBqc29uNS5wYXJzZShwbHVnaW5zW3BsdWdpbl0ucmF3KTtcblxuICAgIHBsdWdpbnNbcGx1Z2luXS5yYXcgPSBQcml2YXRlLmFubm90YXRlZFBsdWdpbihwbHVnaW5zW3BsdWdpbl0sIHtcbiAgICAgIC4uLnJhdyxcbiAgICAgIFtrZXldOiB2YWx1ZVxuICAgIH0pO1xuXG4gICAgcmV0dXJuIHRoaXMuX3NhdmUocGx1Z2luKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZWdpc3RlciBhIHBsdWdpbiB0cmFuc2Zvcm0gZnVuY3Rpb24gdG8gYWN0IG9uIGEgc3BlY2lmaWMgcGx1Z2luLlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIG5hbWUgb2YgdGhlIHBsdWdpbiB3aG9zZSBzZXR0aW5ncyBhcmUgdHJhbnNmb3JtZWQuXG4gICAqXG4gICAqIEBwYXJhbSB0cmFuc2Zvcm1zIC0gVGhlIHRyYW5zZm9ybSBmdW5jdGlvbnMgYXBwbGllZCB0byB0aGUgcGx1Z2luLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGRpc3Bvc2FibGUgdGhhdCByZW1vdmVzIHRoZSB0cmFuc2Zvcm1zIGZyb20gdGhlIHJlZ2lzdHJ5LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIC0gYGNvbXBvc2VgIHRyYW5zZm9ybWF0aW9uczogVGhlIHJlZ2lzdHJ5IGF1dG9tYXRpY2FsbHkgb3ZlcndyaXRlcyBhXG4gICAqIHBsdWdpbidzIGRlZmF1bHQgdmFsdWVzIHdpdGggdXNlciBvdmVycmlkZXMsIGJ1dCBhIHBsdWdpbiBtYXkgaW5zdGVhZCB3aXNoXG4gICAqIHRvIG1lcmdlIHZhbHVlcy4gVGhpcyBiZWhhdmlvciBjYW4gYmUgYWNjb21wbGlzaGVkIGluIGEgYGNvbXBvc2VgXG4gICAqIHRyYW5zZm9ybWF0aW9uLlxuICAgKiAtIGBmZXRjaGAgdHJhbnNmb3JtYXRpb25zOiBUaGUgcmVnaXN0cnkgdXNlcyB0aGUgcGx1Z2luIGRhdGEgdGhhdCBpc1xuICAgKiBmZXRjaGVkIGZyb20gaXRzIGNvbm5lY3Rvci4gSWYgYSBwbHVnaW4gd2FudHMgdG8gb3ZlcnJpZGUsIGUuZy4gdG8gdXBkYXRlXG4gICAqIGl0cyBzY2hlbWEgd2l0aCBkeW5hbWljIGRlZmF1bHRzLCBhIGBmZXRjaGAgdHJhbnNmb3JtYXRpb24gY2FuIGJlIGFwcGxpZWQuXG4gICAqL1xuICB0cmFuc2Zvcm0oXG4gICAgcGx1Z2luOiBzdHJpbmcsXG4gICAgdHJhbnNmb3Jtczoge1xuICAgICAgW3BoYXNlIGluIElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5QaGFzZV0/OiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4uVHJhbnNmb3JtO1xuICAgIH1cbiAgKTogSURpc3Bvc2FibGUge1xuICAgIGNvbnN0IHRyYW5zZm9ybWVycyA9IHRoaXMuX3RyYW5zZm9ybWVycztcblxuICAgIGlmIChwbHVnaW4gaW4gdHJhbnNmb3JtZXJzKSB7XG4gICAgICBjb25zdCBlcnJvciA9IG5ldyBFcnJvcihgJHtwbHVnaW59IGFscmVhZHkgaGFzIGEgdHJhbnNmb3JtZXIuYCk7XG4gICAgICBlcnJvci5uYW1lID0gJ1RyYW5zZm9ybUVycm9yJztcbiAgICAgIHRocm93IGVycm9yO1xuICAgIH1cblxuICAgIHRyYW5zZm9ybWVyc1twbHVnaW5dID0ge1xuICAgICAgZmV0Y2g6IHRyYW5zZm9ybXMuZmV0Y2ggfHwgKHBsdWdpbiA9PiBwbHVnaW4pLFxuICAgICAgY29tcG9zZTogdHJhbnNmb3Jtcy5jb21wb3NlIHx8IChwbHVnaW4gPT4gcGx1Z2luKVxuICAgIH07XG5cbiAgICByZXR1cm4gbmV3IERpc3Bvc2FibGVEZWxlZ2F0ZSgoKSA9PiB7XG4gICAgICBkZWxldGUgdHJhbnNmb3JtZXJzW3BsdWdpbl07XG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogVXBsb2FkIGEgcGx1Z2luJ3Mgc2V0dGluZ3MuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyBzZXQuXG4gICAqXG4gICAqIEBwYXJhbSByYXcgLSBUaGUgcmF3IHBsdWdpbiBzZXR0aW5ncyBiZWluZyB1cGxvYWRlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgc2V0dGluZ3MgaGF2ZSBiZWVuIHNhdmVkLlxuICAgKi9cbiAgYXN5bmMgdXBsb2FkKHBsdWdpbjogc3RyaW5nLCByYXc6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIC8vIFdhaXQgZm9yIGRhdGEgcHJlbG9hZCBiZWZvcmUgYWxsb3dpbmcgbm9ybWFsIG9wZXJhdGlvbi5cbiAgICBhd2FpdCB0aGlzLl9yZWFkeTtcblxuICAgIGNvbnN0IHBsdWdpbnMgPSB0aGlzLnBsdWdpbnM7XG5cbiAgICBpZiAoIShwbHVnaW4gaW4gcGx1Z2lucykpIHtcbiAgICAgIHJldHVybiB0aGlzLmxvYWQocGx1Z2luKS50aGVuKCgpID0+IHRoaXMudXBsb2FkKHBsdWdpbiwgcmF3KSk7XG4gICAgfVxuXG4gICAgLy8gU2V0IHRoZSBsb2NhbCBjb3B5LlxuICAgIHBsdWdpbnNbcGx1Z2luXS5yYXcgPSByYXc7XG5cbiAgICByZXR1cm4gdGhpcy5fc2F2ZShwbHVnaW4pO1xuICB9XG5cbiAgLyoqXG4gICAqIExvYWQgYSBwbHVnaW4gaW50byB0aGUgcmVnaXN0cnkuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9sb2FkKGRhdGE6IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbik6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHBsdWdpbiA9IGRhdGEuaWQ7XG5cbiAgICAvLyBWYWxpZGF0ZSBhbmQgcHJlbG9hZCB0aGUgaXRlbS5cbiAgICB0cnkge1xuICAgICAgYXdhaXQgdGhpcy5fdmFsaWRhdGUoZGF0YSk7XG4gICAgfSBjYXRjaCAoZXJyb3JzKSB7XG4gICAgICBjb25zdCBvdXRwdXQgPSBbYFZhbGlkYXRpbmcgJHtwbHVnaW59IGZhaWxlZDpgXTtcblxuICAgICAgKGVycm9ycyBhcyBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdKS5mb3JFYWNoKChlcnJvciwgaW5kZXgpID0+IHtcbiAgICAgICAgY29uc3QgeyBpbnN0YW5jZVBhdGgsIHNjaGVtYVBhdGgsIGtleXdvcmQsIG1lc3NhZ2UgfSA9IGVycm9yO1xuXG4gICAgICAgIGlmIChpbnN0YW5jZVBhdGggfHwgc2NoZW1hUGF0aCkge1xuICAgICAgICAgIG91dHB1dC5wdXNoKFxuICAgICAgICAgICAgYCR7aW5kZXh9IC0gc2NoZW1hIEAgJHtzY2hlbWFQYXRofSwgZGF0YSBAICR7aW5zdGFuY2VQYXRofWBcbiAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICAgIG91dHB1dC5wdXNoKGB7JHtrZXl3b3JkfX0gJHttZXNzYWdlfWApO1xuICAgICAgfSk7XG4gICAgICBjb25zb2xlLndhcm4ob3V0cHV0LmpvaW4oJ1xcbicpKTtcblxuICAgICAgdGhyb3cgZXJyb3JzO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBQcmVsb2FkIGEgbGlzdCBvZiBwbHVnaW5zIGFuZCBmYWlsIGdyYWNlZnVsbHkuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9wcmVsb2FkKHBsdWdpbnM6IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbltdKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgUHJvbWlzZS5hbGwoXG4gICAgICBwbHVnaW5zLm1hcChhc3luYyBwbHVnaW4gPT4ge1xuICAgICAgICB0cnkge1xuICAgICAgICAgIC8vIEFwcGx5IGEgdHJhbnNmb3JtYXRpb24gdG8gdGhlIHBsdWdpbiBpZiBuZWNlc3NhcnkuXG4gICAgICAgICAgYXdhaXQgdGhpcy5fbG9hZChhd2FpdCB0aGlzLl90cmFuc2Zvcm0oJ2ZldGNoJywgcGx1Z2luKSk7XG4gICAgICAgIH0gY2F0Y2ggKGVycm9ycykge1xuICAgICAgICAgIC8qIElnbm9yZSBzaWxlbnRseSBpZiBubyB0cmFuc2Zvcm1lcnMuICovXG4gICAgICAgICAgaWYgKGVycm9yc1swXT8ua2V5d29yZCAhPT0gJ3Vuc2V0Jykge1xuICAgICAgICAgICAgY29uc29sZS53YXJuKCdJZ25vcmVkIHNldHRpbmcgcmVnaXN0cnkgcHJlbG9hZCBlcnJvcnMuJywgZXJyb3JzKTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH0pXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTYXZlIGEgcGx1Z2luIGluIHRoZSByZWdpc3RyeS5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3NhdmUocGx1Z2luOiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCBwbHVnaW5zID0gdGhpcy5wbHVnaW5zO1xuXG4gICAgaWYgKCEocGx1Z2luIGluIHBsdWdpbnMpKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoYCR7cGx1Z2lufSBkb2VzIG5vdCBleGlzdCBpbiBzZXR0aW5nIHJlZ2lzdHJ5LmApO1xuICAgIH1cblxuICAgIHRyeSB7XG4gICAgICBhd2FpdCB0aGlzLl92YWxpZGF0ZShwbHVnaW5zW3BsdWdpbl0pO1xuICAgIH0gY2F0Y2ggKGVycm9ycykge1xuICAgICAgY29uc29sZS53YXJuKGAke3BsdWdpbn0gdmFsaWRhdGlvbiBlcnJvcnM6YCwgZXJyb3JzKTtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgJHtwbHVnaW59IGZhaWxlZCB0byB2YWxpZGF0ZTsgY2hlY2sgY29uc29sZS5gKTtcbiAgICB9XG4gICAgYXdhaXQgdGhpcy5jb25uZWN0b3Iuc2F2ZShwbHVnaW4sIHBsdWdpbnNbcGx1Z2luXS5yYXcpO1xuXG4gICAgLy8gRmV0Y2ggYW5kIHJlbG9hZCB0aGUgZGF0YSB0byBndWFyYW50ZWUgc2VydmVyIGFuZCBjbGllbnQgYXJlIGluIHN5bmMuXG4gICAgY29uc3QgZmV0Y2hlZCA9IGF3YWl0IHRoaXMuY29ubmVjdG9yLmZldGNoKHBsdWdpbik7XG4gICAgaWYgKGZldGNoZWQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgdGhyb3cgW1xuICAgICAgICB7XG4gICAgICAgICAgaW5zdGFuY2VQYXRoOiAnJyxcbiAgICAgICAgICBrZXl3b3JkOiAnaWQnLFxuICAgICAgICAgIG1lc3NhZ2U6IGBDb3VsZCBub3QgZmV0Y2ggc2V0dGluZ3MgZm9yICR7cGx1Z2lufS5gLFxuICAgICAgICAgIHNjaGVtYVBhdGg6ICcnXG4gICAgICAgIH0gYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JcbiAgICAgIF07XG4gICAgfVxuICAgIGF3YWl0IHRoaXMuX2xvYWQoYXdhaXQgdGhpcy5fdHJhbnNmb3JtKCdmZXRjaCcsIGZldGNoZWQpKTtcbiAgICB0aGlzLl9wbHVnaW5DaGFuZ2VkLmVtaXQocGx1Z2luKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUcmFuc2Zvcm0gdGhlIHBsdWdpbiBpZiBuZWNlc3NhcnkuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF90cmFuc2Zvcm0oXG4gICAgcGhhc2U6IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5QaGFzZSxcbiAgICBwbHVnaW46IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpblxuICApOiBQcm9taXNlPElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbj4ge1xuICAgIGNvbnN0IGlkID0gcGx1Z2luLmlkO1xuICAgIGNvbnN0IHRyYW5zZm9ybWVycyA9IHRoaXMuX3RyYW5zZm9ybWVycztcblxuICAgIGlmICghcGx1Z2luLnNjaGVtYVsnanVweXRlci5sYWIudHJhbnNmb3JtJ10pIHtcbiAgICAgIHJldHVybiBwbHVnaW47XG4gICAgfVxuXG4gICAgaWYgKGlkIGluIHRyYW5zZm9ybWVycykge1xuICAgICAgY29uc3QgdHJhbnNmb3JtZWQgPSB0cmFuc2Zvcm1lcnNbaWRdW3BoYXNlXS5jYWxsKG51bGwsIHBsdWdpbik7XG5cbiAgICAgIGlmICh0cmFuc2Zvcm1lZC5pZCAhPT0gaWQpIHtcbiAgICAgICAgdGhyb3cgW1xuICAgICAgICAgIHtcbiAgICAgICAgICAgIGluc3RhbmNlUGF0aDogJycsXG4gICAgICAgICAgICBrZXl3b3JkOiAnaWQnLFxuICAgICAgICAgICAgbWVzc2FnZTogJ1BsdWdpbiB0cmFuc2Zvcm1hdGlvbnMgY2Fubm90IGNoYW5nZSBwbHVnaW4gSURzLicsXG4gICAgICAgICAgICBzY2hlbWFQYXRoOiAnJ1xuICAgICAgICAgIH0gYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JcbiAgICAgICAgXTtcbiAgICAgIH1cbiAgICAgIHJldHVybiB0cmFuc2Zvcm1lZDtcbiAgICB9XG4gICAgLy8gSWYgdGhlIHBsdWdpbiBoYXMgbm8gdHJhbnNmb3JtZXJzLCB0aHJvdyBhbiBlcnJvciBhbmQgYmFpbC5cbiAgICB0aHJvdyBbXG4gICAgICB7XG4gICAgICAgIGluc3RhbmNlUGF0aDogJycsXG4gICAgICAgIGtleXdvcmQ6ICd1bnNldCcsXG4gICAgICAgIG1lc3NhZ2U6IGAke3BsdWdpbi5pZH0gaGFzIG5vIHRyYW5zZm9ybWVycyB5ZXQuYCxcbiAgICAgICAgc2NoZW1hUGF0aDogJydcbiAgICAgIH0gYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JcbiAgICBdO1xuICB9XG5cbiAgLyoqXG4gICAqIFZhbGlkYXRlIGFuZCBwcmVsb2FkIGEgcGx1Z2luLCBjb21wb3NlIHRoZSBgY29tcG9zaXRlYCBkYXRhLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfdmFsaWRhdGUocGx1Z2luOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4pOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAvLyBWYWxpZGF0ZSB0aGUgdXNlciBkYXRhIGFuZCBjcmVhdGUgdGhlIGNvbXBvc2l0ZSBkYXRhLlxuICAgIGNvbnN0IGVycm9ycyA9IHRoaXMudmFsaWRhdG9yLnZhbGlkYXRlRGF0YShwbHVnaW4pO1xuXG4gICAgaWYgKGVycm9ycykge1xuICAgICAgdGhyb3cgZXJyb3JzO1xuICAgIH1cblxuICAgIC8vIEFwcGx5IGEgdHJhbnNmb3JtYXRpb24gaWYgbmVjZXNzYXJ5IGFuZCBzZXQgdGhlIGxvY2FsIGNvcHkuXG4gICAgdGhpcy5wbHVnaW5zW3BsdWdpbi5pZF0gPSBhd2FpdCB0aGlzLl90cmFuc2Zvcm0oJ2NvbXBvc2UnLCBwbHVnaW4pO1xuICB9XG5cbiAgcHJpdmF0ZSBfcGx1Z2luQ2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgc3RyaW5nPih0aGlzKTtcbiAgcHJpdmF0ZSBfcmVhZHkgPSBQcm9taXNlLnJlc29sdmUoKTtcbiAgcHJpdmF0ZSBfdHJhbnNmb3JtZXJzOiB7XG4gICAgW3BsdWdpbjogc3RyaW5nXToge1xuICAgICAgW3BoYXNlIGluIElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5QaGFzZV06IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5UcmFuc2Zvcm07XG4gICAgfTtcbiAgfSA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gIHByaXZhdGUgX3VubG9hZGVkUGx1Z2lucyA9IG5ldyBNYXA8c3RyaW5nLCBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4+KCk7XG59XG5cbi8qKlxuICogQmFzZSBzZXR0aW5ncyBzcGVjaWZpZWQgYnkgYSBKU09OIHNjaGVtYS5cbiAqL1xuZXhwb3J0IGNsYXNzIEJhc2VTZXR0aW5nczxcbiAgVCBleHRlbmRzIElTZXR0aW5nUmVnaXN0cnkuSVByb3BlcnR5ID0gSVNldHRpbmdSZWdpc3RyeS5JUHJvcGVydHlcbj4ge1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiB7IHNjaGVtYTogVCB9KSB7XG4gICAgdGhpcy5fc2NoZW1hID0gb3B0aW9ucy5zY2hlbWE7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHBsdWdpbidzIHNjaGVtYS5cbiAgICovXG4gIGdldCBzY2hlbWEoKTogVCB7XG4gICAgcmV0dXJuIHRoaXMuX3NjaGVtYTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDaGVja3MgaWYgYW55IGZpZWxkcyBhcmUgZGlmZmVyZW50IGZyb20gdGhlIGRlZmF1bHQgdmFsdWUuXG4gICAqL1xuICBpc0RlZmF1bHQodXNlcjogUmVhZG9ubHlQYXJ0aWFsSlNPTk9iamVjdCk6IGJvb2xlYW4ge1xuICAgIGZvciAoY29uc3Qga2V5IGluIHRoaXMuc2NoZW1hLnByb3BlcnRpZXMpIHtcbiAgICAgIGNvbnN0IHZhbHVlID0gdXNlcltrZXldO1xuICAgICAgY29uc3QgZGVmYXVsdFZhbHVlID0gdGhpcy5kZWZhdWx0KGtleSk7XG4gICAgICBpZiAoXG4gICAgICAgIHZhbHVlID09PSB1bmRlZmluZWQgfHxcbiAgICAgICAgZGVmYXVsdFZhbHVlID09PSB1bmRlZmluZWQgfHxcbiAgICAgICAgSlNPTkV4dC5kZWVwRXF1YWwodmFsdWUsIEpTT05FeHQuZW1wdHlPYmplY3QpIHx8XG4gICAgICAgIEpTT05FeHQuZGVlcEVxdWFsKHZhbHVlLCBKU09ORXh0LmVtcHR5QXJyYXkpXG4gICAgICApIHtcbiAgICAgICAgY29udGludWU7XG4gICAgICB9XG4gICAgICBpZiAoIUpTT05FeHQuZGVlcEVxdWFsKHZhbHVlLCBkZWZhdWx0VmFsdWUpKSB7XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cbiAgICB9XG4gICAgcmV0dXJuIHRydWU7XG4gIH1cblxuICAvKipcbiAgICogQ2FsY3VsYXRlIHRoZSBkZWZhdWx0IHZhbHVlIG9mIGEgc2V0dGluZyBieSBpdGVyYXRpbmcgdGhyb3VnaCB0aGUgc2NoZW1hLlxuICAgKlxuICAgKiBAcGFyYW0ga2V5IC0gVGhlIG5hbWUgb2YgdGhlIHNldHRpbmcgd2hvc2UgZGVmYXVsdCB2YWx1ZSBpcyBjYWxjdWxhdGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGNhbGN1bGF0ZWQgZGVmYXVsdCBKU09OIHZhbHVlIGZvciBhIHNwZWNpZmljIHNldHRpbmcuXG4gICAqL1xuICBkZWZhdWx0KGtleT86IHN0cmluZyk6IFBhcnRpYWxKU09OVmFsdWUgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiBQcml2YXRlLnJlaWZ5RGVmYXVsdCh0aGlzLnNjaGVtYSwga2V5KTtcbiAgfVxuXG4gIHByaXZhdGUgX3NjaGVtYTogVDtcbn1cblxuLyoqXG4gKiBBIG1hbmFnZXIgZm9yIGEgc3BlY2lmaWMgcGx1Z2luJ3Mgc2V0dGluZ3MuXG4gKi9cbmV4cG9ydCBjbGFzcyBTZXR0aW5nc1xuICBleHRlbmRzIEJhc2VTZXR0aW5nczxJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWE+XG4gIGltcGxlbWVudHMgSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3NcbntcbiAgLyoqXG4gICAqIEluc3RhbnRpYXRlIGEgbmV3IHBsdWdpbiBzZXR0aW5ncyBtYW5hZ2VyLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogU2V0dGluZ3MuSU9wdGlvbnMpIHtcbiAgICBzdXBlcih7IHNjaGVtYTogb3B0aW9ucy5wbHVnaW4uc2NoZW1hIH0pO1xuICAgIHRoaXMuaWQgPSBvcHRpb25zLnBsdWdpbi5pZDtcbiAgICB0aGlzLnJlZ2lzdHJ5ID0gb3B0aW9ucy5yZWdpc3RyeTtcbiAgICB0aGlzLnJlZ2lzdHJ5LnBsdWdpbkNoYW5nZWQuY29ubmVjdCh0aGlzLl9vblBsdWdpbkNoYW5nZWQsIHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBwbHVnaW4gbmFtZS5cbiAgICovXG4gIHJlYWRvbmx5IGlkOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFRoZSBzZXR0aW5nIHJlZ2lzdHJ5IGluc3RhbmNlIHVzZWQgYXMgYSBiYWNrLWVuZCBmb3IgdGhlc2Ugc2V0dGluZ3MuXG4gICAqL1xuICByZWFkb25seSByZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeTtcblxuICAvKipcbiAgICogQSBzaWduYWwgdGhhdCBlbWl0cyB3aGVuIHRoZSBwbHVnaW4ncyBzZXR0aW5ncyBoYXZlIGNoYW5nZWQuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIHZvaWQ+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY29tcG9zaXRlIG9mIHVzZXIgc2V0dGluZ3MgYW5kIGV4dGVuc2lvbiBkZWZhdWx0cy5cbiAgICovXG4gIGdldCBjb21wb3NpdGUoKTogUmVhZG9ubHlQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgcmV0dXJuIHRoaXMucGx1Z2luLmRhdGEuY29tcG9zaXRlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRlc3Qgd2hldGhlciB0aGUgcGx1Z2luIHNldHRpbmdzIG1hbmFnZXIgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIGdldCBwbHVnaW4oKTogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luIHtcbiAgICByZXR1cm4gdGhpcy5yZWdpc3RyeS5wbHVnaW5zW3RoaXMuaWRdITtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgcGx1Z2luIHNldHRpbmdzIHJhdyB0ZXh0IHZhbHVlLlxuICAgKi9cbiAgZ2V0IHJhdygpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLnBsdWdpbi5yYXc7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgc2V0dGluZ3MgaGF2ZSBiZWVuIG1vZGlmaWVkIGJ5IHRoZSB1c2VyIG9yIG5vdC5cbiAgICovXG4gIGdldCBpc01vZGlmaWVkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiAhdGhpcy5pc0RlZmF1bHQodGhpcy51c2VyKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgdXNlciBzZXR0aW5ncy5cbiAgICovXG4gIGdldCB1c2VyKCk6IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3Qge1xuICAgIHJldHVybiB0aGlzLnBsdWdpbi5kYXRhLnVzZXI7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHB1Ymxpc2hlZCB2ZXJzaW9uIG9mIHRoZSBOUE0gcGFja2FnZSBjb250YWluaW5nIHRoZXNlIHNldHRpbmdzLlxuICAgKi9cbiAgZ2V0IHZlcnNpb24oKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5wbHVnaW4udmVyc2lvbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm4gdGhlIGRlZmF1bHRzIGluIGEgY29tbWVudGVkIEpTT04gZm9ybWF0LlxuICAgKi9cbiAgYW5ub3RhdGVkRGVmYXVsdHMoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gUHJpdmF0ZS5hbm5vdGF0ZWREZWZhdWx0cyh0aGlzLnNjaGVtYSwgdGhpcy5pZCk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcGx1Z2luIHNldHRpbmdzIHJlc291cmNlcy5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuX2lzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpbmRpdmlkdWFsIHNldHRpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSBUaGUgbmFtZSBvZiB0aGUgc2V0dGluZyBiZWluZyByZXRyaWV2ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBzZXR0aW5nIHZhbHVlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgbWV0aG9kIHJldHVybnMgc3luY2hyb25vdXNseSBiZWNhdXNlIGl0IHVzZXMgYSBjYWNoZWQgY29weSBvZiB0aGVcbiAgICogcGx1Z2luIHNldHRpbmdzIHRoYXQgaXMgc3luY2hyb25pemVkIHdpdGggdGhlIHJlZ2lzdHJ5LlxuICAgKi9cbiAgZ2V0KGtleTogc3RyaW5nKToge1xuICAgIGNvbXBvc2l0ZTogUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkO1xuICAgIHVzZXI6IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgfSB7XG4gICAgY29uc3QgeyBjb21wb3NpdGUsIHVzZXIgfSA9IHRoaXM7XG5cbiAgICByZXR1cm4ge1xuICAgICAgY29tcG9zaXRlOlxuICAgICAgICBjb21wb3NpdGVba2V5XSAhPT0gdW5kZWZpbmVkID8gY29weShjb21wb3NpdGVba2V5XSEpIDogdW5kZWZpbmVkLFxuICAgICAgdXNlcjogdXNlcltrZXldICE9PSB1bmRlZmluZWQgPyBjb3B5KHVzZXJba2V5XSEpIDogdW5kZWZpbmVkXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBzaW5nbGUgc2V0dGluZy5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHJlbW92ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmVtb3ZlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGZ1bmN0aW9uIGlzIGFzeW5jaHJvbm91cyBiZWNhdXNlIGl0IHdyaXRlcyB0byB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIHJlbW92ZShrZXk6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLnJlZ2lzdHJ5LnJlbW92ZSh0aGlzLnBsdWdpbi5pZCwga2V5KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTYXZlIGFsbCBvZiB0aGUgcGx1Z2luJ3MgdXNlciBzZXR0aW5ncyBhdCBvbmNlLlxuICAgKi9cbiAgc2F2ZShyYXc6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLnJlZ2lzdHJ5LnVwbG9hZCh0aGlzLnBsdWdpbi5pZCwgcmF3KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgYSBzaW5nbGUgc2V0dGluZy5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHNldC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIHZhbHVlIG9mIHRoZSBzZXR0aW5nLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBzZXR0aW5nIGhhcyBiZWVuIHNhdmVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgZnVuY3Rpb24gaXMgYXN5bmNocm9ub3VzIGJlY2F1c2UgaXQgd3JpdGVzIHRvIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgc2V0KGtleTogc3RyaW5nLCB2YWx1ZTogSlNPTlZhbHVlKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMucmVnaXN0cnkuc2V0KHRoaXMucGx1Z2luLmlkLCBrZXksIHZhbHVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBWYWxpZGF0ZXMgcmF3IHNldHRpbmdzIHdpdGggY29tbWVudHMuXG4gICAqXG4gICAqIEBwYXJhbSByYXcgLSBUaGUgSlNPTiB3aXRoIGNvbW1lbnRzIHN0cmluZyBiZWluZyB2YWxpZGF0ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgbGlzdCBvZiBlcnJvcnMgb3IgYG51bGxgIGlmIHZhbGlkLlxuICAgKi9cbiAgdmFsaWRhdGUocmF3OiBzdHJpbmcpOiBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdIHwgbnVsbCB7XG4gICAgY29uc3QgZGF0YSA9IHsgY29tcG9zaXRlOiB7fSwgdXNlcjoge30gfTtcbiAgICBjb25zdCB7IGlkLCBzY2hlbWEgfSA9IHRoaXMucGx1Z2luO1xuICAgIGNvbnN0IHZhbGlkYXRvciA9IHRoaXMucmVnaXN0cnkudmFsaWRhdG9yO1xuICAgIGNvbnN0IHZlcnNpb24gPSB0aGlzLnZlcnNpb247XG5cbiAgICByZXR1cm4gdmFsaWRhdG9yLnZhbGlkYXRlRGF0YSh7IGRhdGEsIGlkLCByYXcsIHNjaGVtYSwgdmVyc2lvbiB9LCBmYWxzZSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHBsdWdpbiBjaGFuZ2VzIGluIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcHJpdmF0ZSBfb25QbHVnaW5DaGFuZ2VkKHNlbmRlcjogYW55LCBwbHVnaW46IHN0cmluZyk6IHZvaWQge1xuICAgIGlmIChwbHVnaW4gPT09IHRoaXMucGx1Z2luLmlkKSB7XG4gICAgICB0aGlzLl9jaGFuZ2VkLmVtaXQodW5kZWZpbmVkKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCB2b2lkPih0aGlzKTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgU2V0dGluZ1JlZ2lzdHJ5YCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFNldHRpbmdSZWdpc3RyeSB7XG4gIC8qKlxuICAgKiBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhIHNldHRpbmcgcmVnaXN0cnlcbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBkYXRhIGNvbm5lY3RvciB1c2VkIGJ5IHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgICAqL1xuICAgIGNvbm5lY3RvcjogSURhdGFDb25uZWN0b3I8SVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLCBzdHJpbmc+O1xuXG4gICAgLyoqXG4gICAgICogUHJlbG9hZGVkIHBsdWdpbiBkYXRhIHRvIHBvcHVsYXRlIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgICAqL1xuICAgIHBsdWdpbnM/OiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW5bXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBudW1iZXIgb2YgbWlsbGlzZWNvbmRzIGJlZm9yZSBhIGBsb2FkKClgIGNhbGwgdG8gdGhlIHJlZ2lzdHJ5IHdhaXRzXG4gICAgICogYmVmb3JlIHRpbWluZyBvdXQgaWYgaXQgcmVxdWlyZXMgYSB0cmFuc2Zvcm1hdGlvbiB0aGF0IGhhcyBub3QgYmVlblxuICAgICAqIHJlZ2lzdGVyZWQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhlIGRlZmF1bHQgdmFsdWUgaXMgNzAwMC5cbiAgICAgKi9cbiAgICB0aW1lb3V0PzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHZhbGlkYXRvciB1c2VkIHRvIGVuZm9yY2UgdGhlIHNldHRpbmdzIEpTT04gc2NoZW1hLlxuICAgICAqL1xuICAgIHZhbGlkYXRvcj86IElTY2hlbWFWYWxpZGF0b3I7XG4gIH1cblxuICAvKipcbiAgICogUmVjb25jaWxlIHRoZSBtZW51cy5cbiAgICpcbiAgICogQHBhcmFtIHJlZmVyZW5jZSBUaGUgcmVmZXJlbmNlIGxpc3Qgb2YgbWVudXMuXG4gICAqIEBwYXJhbSBhZGRpdGlvbiBUaGUgbGlzdCBvZiBtZW51cyB0byBhZGQuXG4gICAqIEBwYXJhbSB3YXJuIFdhcm4gaWYgdGhlIGNvbW1hbmQgaXRlbXMgYXJlIGR1cGxpY2F0ZWQgd2l0aGluIHRoZSBzYW1lIG1lbnUuXG4gICAqIEByZXR1cm5zIFRoZSByZWNvbmNpbGVkIGxpc3Qgb2YgbWVudXMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVjb25jaWxlTWVudXMoXG4gICAgcmVmZXJlbmNlOiBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51W10gfCBudWxsLFxuICAgIGFkZGl0aW9uOiBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51W10gfCBudWxsLFxuICAgIHdhcm46IGJvb2xlYW4gPSBmYWxzZSxcbiAgICBhZGROZXdJdGVtczogYm9vbGVhbiA9IHRydWVcbiAgKTogSVNldHRpbmdSZWdpc3RyeS5JTWVudVtdIHtcbiAgICBpZiAoIXJlZmVyZW5jZSkge1xuICAgICAgcmV0dXJuIGFkZGl0aW9uICYmIGFkZE5ld0l0ZW1zID8gSlNPTkV4dC5kZWVwQ29weShhZGRpdGlvbikgOiBbXTtcbiAgICB9XG4gICAgaWYgKCFhZGRpdGlvbikge1xuICAgICAgcmV0dXJuIEpTT05FeHQuZGVlcENvcHkocmVmZXJlbmNlKTtcbiAgICB9XG5cbiAgICBjb25zdCBtZXJnZWQgPSBKU09ORXh0LmRlZXBDb3B5KHJlZmVyZW5jZSk7XG5cbiAgICBhZGRpdGlvbi5mb3JFYWNoKG1lbnUgPT4ge1xuICAgICAgY29uc3QgcmVmSW5kZXggPSBtZXJnZWQuZmluZEluZGV4KHJlZiA9PiByZWYuaWQgPT09IG1lbnUuaWQpO1xuICAgICAgaWYgKHJlZkluZGV4ID49IDApIHtcbiAgICAgICAgbWVyZ2VkW3JlZkluZGV4XSA9IHtcbiAgICAgICAgICAuLi5tZXJnZWRbcmVmSW5kZXhdLFxuICAgICAgICAgIC4uLm1lbnUsXG4gICAgICAgICAgaXRlbXM6IHJlY29uY2lsZUl0ZW1zKFxuICAgICAgICAgICAgbWVyZ2VkW3JlZkluZGV4XS5pdGVtcyxcbiAgICAgICAgICAgIG1lbnUuaXRlbXMsXG4gICAgICAgICAgICB3YXJuLFxuICAgICAgICAgICAgYWRkTmV3SXRlbXNcbiAgICAgICAgICApXG4gICAgICAgIH07XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBpZiAoYWRkTmV3SXRlbXMpIHtcbiAgICAgICAgICBtZXJnZWQucHVzaChtZW51KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgcmV0dXJuIG1lcmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBNZXJnZSB0d28gc2V0IG9mIG1lbnUgaXRlbXMuXG4gICAqXG4gICAqIEBwYXJhbSByZWZlcmVuY2UgUmVmZXJlbmNlIHNldCBvZiBtZW51IGl0ZW1zXG4gICAqIEBwYXJhbSBhZGRpdGlvbiBOZXcgaXRlbXMgdG8gYWRkXG4gICAqIEBwYXJhbSB3YXJuIFdoZXRoZXIgdG8gd2FybiBpZiBpdGVtIGlzIGR1cGxpY2F0ZWQ7IGRlZmF1bHQgdG8gZmFsc2VcbiAgICogQHJldHVybnMgVGhlIG1lcmdlZCBzZXQgb2YgaXRlbXNcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiByZWNvbmNpbGVJdGVtczxUIGV4dGVuZHMgSVNldHRpbmdSZWdpc3RyeS5JTWVudUl0ZW0+KFxuICAgIHJlZmVyZW5jZT86IFRbXSxcbiAgICBhZGRpdGlvbj86IFRbXSxcbiAgICB3YXJuOiBib29sZWFuID0gZmFsc2UsXG4gICAgYWRkTmV3SXRlbXM6IGJvb2xlYW4gPSB0cnVlXG4gICk6IFRbXSB8IHVuZGVmaW5lZCB7XG4gICAgaWYgKCFyZWZlcmVuY2UpIHtcbiAgICAgIHJldHVybiBhZGRpdGlvbiA/IEpTT05FeHQuZGVlcENvcHkoYWRkaXRpb24pIDogdW5kZWZpbmVkO1xuICAgIH1cbiAgICBpZiAoIWFkZGl0aW9uKSB7XG4gICAgICByZXR1cm4gSlNPTkV4dC5kZWVwQ29weShyZWZlcmVuY2UpO1xuICAgIH1cblxuICAgIGNvbnN0IGl0ZW1zID0gSlNPTkV4dC5kZWVwQ29weShyZWZlcmVuY2UpO1xuXG4gICAgLy8gTWVyZ2UgYXJyYXkgZWxlbWVudCBkZXBlbmRpbmcgb24gdGhlIHR5cGVcbiAgICBhZGRpdGlvbi5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgc3dpdGNoIChpdGVtLnR5cGUgPz8gJ2NvbW1hbmQnKSB7XG4gICAgICAgIGNhc2UgJ3NlcGFyYXRvcic6XG4gICAgICAgICAgaWYgKGFkZE5ld0l0ZW1zKSB7XG4gICAgICAgICAgICBpdGVtcy5wdXNoKHsgLi4uaXRlbSB9KTtcbiAgICAgICAgICB9XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIGNhc2UgJ3N1Ym1lbnUnOlxuICAgICAgICAgIGlmIChpdGVtLnN1Ym1lbnUpIHtcbiAgICAgICAgICAgIGNvbnN0IHJlZkluZGV4ID0gaXRlbXMuZmluZEluZGV4KFxuICAgICAgICAgICAgICByZWYgPT5cbiAgICAgICAgICAgICAgICByZWYudHlwZSA9PT0gJ3N1Ym1lbnUnICYmIHJlZi5zdWJtZW51Py5pZCA9PT0gaXRlbS5zdWJtZW51Py5pZFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGlmIChyZWZJbmRleCA8IDApIHtcbiAgICAgICAgICAgICAgaWYgKGFkZE5ld0l0ZW1zKSB7XG4gICAgICAgICAgICAgICAgaXRlbXMucHVzaChKU09ORXh0LmRlZXBDb3B5KGl0ZW0pKTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgaXRlbXNbcmVmSW5kZXhdID0ge1xuICAgICAgICAgICAgICAgIC4uLml0ZW1zW3JlZkluZGV4XSxcbiAgICAgICAgICAgICAgICAuLi5pdGVtLFxuICAgICAgICAgICAgICAgIHN1Ym1lbnU6IHJlY29uY2lsZU1lbnVzKFxuICAgICAgICAgICAgICAgICAgaXRlbXNbcmVmSW5kZXhdLnN1Ym1lbnVcbiAgICAgICAgICAgICAgICAgICAgPyBbaXRlbXNbcmVmSW5kZXhdLnN1Ym1lbnUgYXMgYW55XVxuICAgICAgICAgICAgICAgICAgICA6IG51bGwsXG4gICAgICAgICAgICAgICAgICBbaXRlbS5zdWJtZW51XSxcbiAgICAgICAgICAgICAgICAgIHdhcm4sXG4gICAgICAgICAgICAgICAgICBhZGROZXdJdGVtc1xuICAgICAgICAgICAgICAgIClbMF1cbiAgICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIGNhc2UgJ2NvbW1hbmQnOlxuICAgICAgICAgIGlmIChpdGVtLmNvbW1hbmQpIHtcbiAgICAgICAgICAgIGNvbnN0IHJlZkluZGV4ID0gaXRlbXMuZmluZEluZGV4KFxuICAgICAgICAgICAgICByZWYgPT5cbiAgICAgICAgICAgICAgICByZWYuY29tbWFuZCA9PT0gaXRlbS5jb21tYW5kICYmXG4gICAgICAgICAgICAgICAgcmVmLnNlbGVjdG9yID09PSBpdGVtLnNlbGVjdG9yICYmXG4gICAgICAgICAgICAgICAgSlNPTkV4dC5kZWVwRXF1YWwocmVmLmFyZ3MgPz8ge30sIGl0ZW0uYXJncyA/PyB7fSlcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICBpZiAocmVmSW5kZXggPCAwKSB7XG4gICAgICAgICAgICAgIGlmIChhZGROZXdJdGVtcykge1xuICAgICAgICAgICAgICAgIGl0ZW1zLnB1c2goeyAuLi5pdGVtIH0pO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICBpZiAod2Fybikge1xuICAgICAgICAgICAgICAgIGNvbnNvbGUud2FybihcbiAgICAgICAgICAgICAgICAgIGBNZW51IGVudHJ5IGZvciBjb21tYW5kICcke2l0ZW0uY29tbWFuZH0nIGlzIGR1cGxpY2F0ZWQuYFxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgaXRlbXNbcmVmSW5kZXhdID0geyAuLi5pdGVtc1tyZWZJbmRleF0sIC4uLml0ZW0gfTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICByZXR1cm4gaXRlbXM7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGRpc2FibGVkIGVudHJpZXMgZnJvbSBtZW51IGl0ZW1zXG4gICAqXG4gICAqIEBwYXJhbSBpdGVtcyBNZW51IGl0ZW1zXG4gICAqIEByZXR1cm5zIEZpbHRlcmVkIG1lbnUgaXRlbXNcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBmaWx0ZXJEaXNhYmxlZEl0ZW1zPFQgZXh0ZW5kcyBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51SXRlbT4oXG4gICAgaXRlbXM6IFRbXVxuICApOiBUW10ge1xuICAgIHJldHVybiBpdGVtcy5yZWR1Y2U8VFtdPigoZmluYWwsIHZhbHVlKSA9PiB7XG4gICAgICBjb25zdCBjb3B5ID0geyAuLi52YWx1ZSB9O1xuICAgICAgaWYgKCFjb3B5LmRpc2FibGVkKSB7XG4gICAgICAgIGlmIChjb3B5LnR5cGUgPT09ICdzdWJtZW51Jykge1xuICAgICAgICAgIGNvbnN0IHsgc3VibWVudSB9ID0gY29weTtcbiAgICAgICAgICBpZiAoc3VibWVudSAmJiAhc3VibWVudS5kaXNhYmxlZCkge1xuICAgICAgICAgICAgY29weS5zdWJtZW51ID0ge1xuICAgICAgICAgICAgICAuLi5zdWJtZW51LFxuICAgICAgICAgICAgICBpdGVtczogZmlsdGVyRGlzYWJsZWRJdGVtcyhzdWJtZW51Lml0ZW1zID8/IFtdKVxuICAgICAgICAgICAgfTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgZmluYWwucHVzaChjb3B5KTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIGZpbmFsO1xuICAgIH0sIFtdKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZWNvbmNpbGUgZGVmYXVsdCBhbmQgdXNlciBzaG9ydGN1dHMgYW5kIHJldHVybiB0aGUgY29tcG9zaXRlIGxpc3QuXG4gICAqXG4gICAqIEBwYXJhbSBkZWZhdWx0cyAtIFRoZSBsaXN0IG9mIGRlZmF1bHQgc2hvcnRjdXRzLlxuICAgKlxuICAgKiBAcGFyYW0gdXNlciAtIFRoZSBsaXN0IG9mIHVzZXIgc2hvcnRjdXQgb3ZlcnJpZGVzIGFuZCBhZGRpdGlvbnMuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgbG9hZGFibGUgbGlzdCBvZiBzaG9ydGN1dHMgKG9taXR0aW5nIGRpc2FibGVkIGFuZCBvdmVycmlkZGVuKS5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiByZWNvbmNpbGVTaG9ydGN1dHMoXG4gICAgZGVmYXVsdHM6IElTZXR0aW5nUmVnaXN0cnkuSVNob3J0Y3V0W10sXG4gICAgdXNlcjogSVNldHRpbmdSZWdpc3RyeS5JU2hvcnRjdXRbXVxuICApOiBJU2V0dGluZ1JlZ2lzdHJ5LklTaG9ydGN1dFtdIHtcbiAgICBjb25zdCBtZW1vOiB7XG4gICAgICBba2V5czogc3RyaW5nXToge1xuICAgICAgICBbc2VsZWN0b3I6IHN0cmluZ106IGJvb2xlYW47IC8vIElmIGB0cnVlYCwgc2hvdWxkIHdhcm4gaWYgYSBkZWZhdWx0IHNob3J0Y3V0IGNvbmZsaWN0cy5cbiAgICAgIH07XG4gICAgfSA9IHt9O1xuXG4gICAgLy8gSWYgYSB1c2VyIHNob3J0Y3V0IGNvbGxpZGVzIHdpdGggYW5vdGhlciB1c2VyIHNob3J0Y3V0IHdhcm4gYW5kIGZpbHRlci5cbiAgICB1c2VyID0gdXNlci5maWx0ZXIoc2hvcnRjdXQgPT4ge1xuICAgICAgY29uc3Qga2V5cyA9XG4gICAgICAgIENvbW1hbmRSZWdpc3RyeS5ub3JtYWxpemVLZXlzKHNob3J0Y3V0KS5qb2luKFJFQ09SRF9TRVBBUkFUT1IpO1xuICAgICAgaWYgKCFrZXlzKSB7XG4gICAgICAgIGNvbnNvbGUud2FybihcbiAgICAgICAgICAnU2tpcHBpbmcgdGhpcyBzaG9ydGN1dCBiZWNhdXNlIHRoZXJlIGFyZSBubyBhY3Rpb25hYmxlIGtleXMgb24gdGhpcyBwbGF0Zm9ybScsXG4gICAgICAgICAgc2hvcnRjdXRcbiAgICAgICAgKTtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgaWYgKCEoa2V5cyBpbiBtZW1vKSkge1xuICAgICAgICBtZW1vW2tleXNdID0ge307XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IHsgc2VsZWN0b3IgfSA9IHNob3J0Y3V0O1xuICAgICAgaWYgKCEoc2VsZWN0b3IgaW4gbWVtb1trZXlzXSkpIHtcbiAgICAgICAgbWVtb1trZXlzXVtzZWxlY3Rvcl0gPSBmYWxzZTsgLy8gRG8gbm90IHdhcm4gaWYgYSBkZWZhdWx0IHNob3J0Y3V0IGNvbmZsaWN0cy5cbiAgICAgICAgcmV0dXJuIHRydWU7XG4gICAgICB9XG5cbiAgICAgIGNvbnNvbGUud2FybihcbiAgICAgICAgJ1NraXBwaW5nIHRoaXMgc2hvcnRjdXQgYmVjYXVzZSBpdCBjb2xsaWRlcyB3aXRoIGFub3RoZXIgc2hvcnRjdXQuJyxcbiAgICAgICAgc2hvcnRjdXRcbiAgICAgICk7XG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfSk7XG5cbiAgICAvLyBJZiBhIGRlZmF1bHQgc2hvcnRjdXQgY29sbGlkZXMgd2l0aCBhbm90aGVyIGRlZmF1bHQsIHdhcm4gYW5kIGZpbHRlcixcbiAgICAvLyB1bmxlc3Mgb25lIG9mIHRoZSBzaG9ydGN1dHMgaXMgYSBkaXNhYmxpbmcgc2hvcnRjdXQgKHNvIGxvb2sgdGhyb3VnaFxuICAgIC8vIGRpc2FibGVkIHNob3J0Y3V0cyBmaXJzdCkuIElmIGEgc2hvcnRjdXQgaGFzIGFscmVhZHkgYmVlbiBhZGRlZCBieSB0aGVcbiAgICAvLyB1c2VyIHByZWZlcmVuY2VzLCBmaWx0ZXIgaXQgb3V0IHRvbyAodGhpcyBpbmNsdWRlcyBzaG9ydGN1dHMgdGhhdCBhcmVcbiAgICAvLyBkaXNhYmxlZCBieSB1c2VyIHByZWZlcmVuY2VzKS5cbiAgICBkZWZhdWx0cyA9IFtcbiAgICAgIC4uLmRlZmF1bHRzLmZpbHRlcihzID0+ICEhcy5kaXNhYmxlZCksXG4gICAgICAuLi5kZWZhdWx0cy5maWx0ZXIocyA9PiAhcy5kaXNhYmxlZClcbiAgICBdLmZpbHRlcihzaG9ydGN1dCA9PiB7XG4gICAgICBjb25zdCBrZXlzID1cbiAgICAgICAgQ29tbWFuZFJlZ2lzdHJ5Lm5vcm1hbGl6ZUtleXMoc2hvcnRjdXQpLmpvaW4oUkVDT1JEX1NFUEFSQVRPUik7XG5cbiAgICAgIGlmICgha2V5cykge1xuICAgICAgICByZXR1cm4gZmFsc2U7XG4gICAgICB9XG4gICAgICBpZiAoIShrZXlzIGluIG1lbW8pKSB7XG4gICAgICAgIG1lbW9ba2V5c10gPSB7fTtcbiAgICAgIH1cblxuICAgICAgY29uc3QgeyBkaXNhYmxlZCwgc2VsZWN0b3IgfSA9IHNob3J0Y3V0O1xuICAgICAgaWYgKCEoc2VsZWN0b3IgaW4gbWVtb1trZXlzXSkpIHtcbiAgICAgICAgLy8gV2FybiBvZiBmdXR1cmUgY29uZmxpY3RzIGlmIHRoZSBkZWZhdWx0IHNob3J0Y3V0IGlzIG5vdCBkaXNhYmxlZC5cbiAgICAgICAgbWVtb1trZXlzXVtzZWxlY3Rvcl0gPSAhZGlzYWJsZWQ7XG4gICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgfVxuXG4gICAgICAvLyBXZSBoYXZlIGEgY29uZmxpY3Qgbm93LiBXYXJuIHRoZSB1c2VyIGlmIHdlIG5lZWQgdG8gZG8gc28uXG4gICAgICBpZiAobWVtb1trZXlzXVtzZWxlY3Rvcl0pIHtcbiAgICAgICAgY29uc29sZS53YXJuKFxuICAgICAgICAgICdTa2lwcGluZyB0aGlzIGRlZmF1bHQgc2hvcnRjdXQgYmVjYXVzZSBpdCBjb2xsaWRlcyB3aXRoIGFub3RoZXIgZGVmYXVsdCBzaG9ydGN1dC4nLFxuICAgICAgICAgIHNob3J0Y3V0XG4gICAgICAgICk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBmYWxzZTtcbiAgICB9KTtcblxuICAgIC8vIFJldHVybiBhbGwgdGhlIHNob3J0Y3V0cyB0aGF0IHNob3VsZCBiZSByZWdpc3RlcmVkXG4gICAgcmV0dXJuIChcbiAgICAgIHVzZXJcbiAgICAgICAgLmNvbmNhdChkZWZhdWx0cylcbiAgICAgICAgLmZpbHRlcihzaG9ydGN1dCA9PiAhc2hvcnRjdXQuZGlzYWJsZWQpXG4gICAgICAgIC8vIEZpeCBzaG9ydGN1dHMgY29tcGFyaXNvbiBpbiByanNmIEZvcm0gdG8gYXZvaWQgcG9sbHV0aW5nIHRoZSB1c2VyIHNldHRpbmdzXG4gICAgICAgIC5tYXAoc2hvcnRjdXQgPT4ge1xuICAgICAgICAgIHJldHVybiB7IGFyZ3M6IHt9LCAuLi5zaG9ydGN1dCB9O1xuICAgICAgICB9KVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogTWVyZ2UgdHdvIHNldCBvZiB0b29sYmFyIGl0ZW1zLlxuICAgKlxuICAgKiBAcGFyYW0gcmVmZXJlbmNlIFJlZmVyZW5jZSBzZXQgb2YgdG9vbGJhciBpdGVtc1xuICAgKiBAcGFyYW0gYWRkaXRpb24gTmV3IGl0ZW1zIHRvIGFkZFxuICAgKiBAcGFyYW0gd2FybiBXaGV0aGVyIHRvIHdhcm4gaWYgaXRlbSBpcyBkdXBsaWNhdGVkOyBkZWZhdWx0IHRvIGZhbHNlXG4gICAqIEByZXR1cm5zIFRoZSBtZXJnZWQgc2V0IG9mIGl0ZW1zXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVjb25jaWxlVG9vbGJhckl0ZW1zKFxuICAgIHJlZmVyZW5jZT86IElTZXR0aW5nUmVnaXN0cnkuSVRvb2xiYXJJdGVtW10sXG4gICAgYWRkaXRpb24/OiBJU2V0dGluZ1JlZ2lzdHJ5LklUb29sYmFySXRlbVtdLFxuICAgIHdhcm46IGJvb2xlYW4gPSBmYWxzZVxuICApOiBJU2V0dGluZ1JlZ2lzdHJ5LklUb29sYmFySXRlbVtdIHwgdW5kZWZpbmVkIHtcbiAgICBpZiAoIXJlZmVyZW5jZSkge1xuICAgICAgcmV0dXJuIGFkZGl0aW9uID8gSlNPTkV4dC5kZWVwQ29weShhZGRpdGlvbikgOiB1bmRlZmluZWQ7XG4gICAgfVxuICAgIGlmICghYWRkaXRpb24pIHtcbiAgICAgIHJldHVybiBKU09ORXh0LmRlZXBDb3B5KHJlZmVyZW5jZSk7XG4gICAgfVxuXG4gICAgY29uc3QgaXRlbXMgPSBKU09ORXh0LmRlZXBDb3B5KHJlZmVyZW5jZSk7XG5cbiAgICAvLyBNZXJnZSBhcnJheSBlbGVtZW50IGRlcGVuZGluZyBvbiB0aGUgdHlwZVxuICAgIGFkZGl0aW9uLmZvckVhY2goaXRlbSA9PiB7XG4gICAgICAvLyBOYW1lIG11c3QgYmUgdW5pcXVlIHNvIGl0J3Mgc3VmZmljaWVudCB0byBvbmx5IGNvbXBhcmUgaXRcbiAgICAgIGNvbnN0IHJlZkluZGV4ID0gaXRlbXMuZmluZEluZGV4KHJlZiA9PiByZWYubmFtZSA9PT0gaXRlbS5uYW1lKTtcbiAgICAgIGlmIChyZWZJbmRleCA8IDApIHtcbiAgICAgICAgaXRlbXMucHVzaCh7IC4uLml0ZW0gfSk7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBpZiAoXG4gICAgICAgICAgd2FybiAmJlxuICAgICAgICAgIEpTT05FeHQuZGVlcEVxdWFsKE9iamVjdC5rZXlzKGl0ZW0pLCBPYmplY3Qua2V5cyhpdGVtc1tyZWZJbmRleF0pKVxuICAgICAgICApIHtcbiAgICAgICAgICBjb25zb2xlLndhcm4oYFRvb2xiYXIgaXRlbSAnJHtpdGVtLm5hbWV9JyBpcyBkdXBsaWNhdGVkLmApO1xuICAgICAgICB9XG4gICAgICAgIGl0ZW1zW3JlZkluZGV4XSA9IHsgLi4uaXRlbXNbcmVmSW5kZXhdLCAuLi5pdGVtIH07XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICByZXR1cm4gaXRlbXM7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYFNldHRpbmdzYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFNldHRpbmdzIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgYFNldHRpbmdzYCBvYmplY3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgc2V0dGluZyB2YWx1ZXMgZm9yIGEgcGx1Z2luLlxuICAgICAqL1xuICAgIHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHN5c3RlbSByZWdpc3RyeSBpbnN0YW5jZSB1c2VkIGJ5IHRoZSBzZXR0aW5ncyBtYW5hZ2VyLlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgbW9kdWxlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGluZGVudGF0aW9uIGxldmVsLCB1c2VzIHNwYWNlcyBpbnN0ZWFkIG9mIHRhYnMuXG4gICAqL1xuICBjb25zdCBpbmRlbnQgPSAnICAgICc7XG5cbiAgLyoqXG4gICAqIFJlcGxhY2VtZW50IHRleHQgZm9yIHNjaGVtYSBwcm9wZXJ0aWVzIG1pc3NpbmcgYSBgZGVzY3JpcHRpb25gIGZpZWxkLlxuICAgKi9cbiAgY29uc3Qgbm9uZGVzY3JpcHQgPSAnW21pc3Npbmcgc2NoZW1hIGRlc2NyaXB0aW9uXSc7XG5cbiAgLyoqXG4gICAqIFJlcGxhY2VtZW50IHRleHQgZm9yIHNjaGVtYSBwcm9wZXJ0aWVzIG1pc3NpbmcgYSBgdGl0bGVgIGZpZWxkLlxuICAgKi9cbiAgY29uc3QgdW50aXRsZWQgPSAnW21pc3Npbmcgc2NoZW1hIHRpdGxlXSc7XG5cbiAgLyoqXG4gICAqIFJldHVybnMgYW4gYW5ub3RhdGVkIChKU09OIHdpdGggY29tbWVudHMpIHZlcnNpb24gb2YgYSBzY2hlbWEncyBkZWZhdWx0cy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhbm5vdGF0ZWREZWZhdWx0cyhcbiAgICBzY2hlbWE6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYSxcbiAgICBwbHVnaW46IHN0cmluZ1xuICApOiBzdHJpbmcge1xuICAgIGNvbnN0IHsgZGVzY3JpcHRpb24sIHByb3BlcnRpZXMsIHRpdGxlIH0gPSBzY2hlbWE7XG4gICAgY29uc3Qga2V5cyA9IHByb3BlcnRpZXNcbiAgICAgID8gT2JqZWN0LmtleXMocHJvcGVydGllcykuc29ydCgoYSwgYikgPT4gYS5sb2NhbGVDb21wYXJlKGIpKVxuICAgICAgOiBbXTtcbiAgICBjb25zdCBsZW5ndGggPSBNYXRoLm1heCgoZGVzY3JpcHRpb24gfHwgbm9uZGVzY3JpcHQpLmxlbmd0aCwgcGx1Z2luLmxlbmd0aCk7XG5cbiAgICByZXR1cm4gW1xuICAgICAgJ3snLFxuICAgICAgcHJlZml4KGAke3RpdGxlIHx8IHVudGl0bGVkfWApLFxuICAgICAgcHJlZml4KHBsdWdpbiksXG4gICAgICBwcmVmaXgoZGVzY3JpcHRpb24gfHwgbm9uZGVzY3JpcHQpLFxuICAgICAgcHJlZml4KCcqJy5yZXBlYXQobGVuZ3RoKSksXG4gICAgICAnJyxcbiAgICAgIGpvaW4oa2V5cy5tYXAoa2V5ID0+IGRlZmF1bHREb2N1bWVudGVkVmFsdWUoc2NoZW1hLCBrZXkpKSksXG4gICAgICAnfSdcbiAgICBdLmpvaW4oJ1xcbicpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybnMgYW4gYW5ub3RhdGVkIChKU09OIHdpdGggY29tbWVudHMpIHZlcnNpb24gb2YgYSBwbHVnaW4nc1xuICAgKiBzZXR0aW5nIGRhdGEuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYW5ub3RhdGVkUGx1Z2luKFxuICAgIHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLFxuICAgIGRhdGE6IEpTT05PYmplY3RcbiAgKTogc3RyaW5nIHtcbiAgICBjb25zdCB7IGRlc2NyaXB0aW9uLCB0aXRsZSB9ID0gcGx1Z2luLnNjaGVtYTtcbiAgICBjb25zdCBrZXlzID0gT2JqZWN0LmtleXMoZGF0YSkuc29ydCgoYSwgYikgPT4gYS5sb2NhbGVDb21wYXJlKGIpKTtcbiAgICBjb25zdCBsZW5ndGggPSBNYXRoLm1heChcbiAgICAgIChkZXNjcmlwdGlvbiB8fCBub25kZXNjcmlwdCkubGVuZ3RoLFxuICAgICAgcGx1Z2luLmlkLmxlbmd0aFxuICAgICk7XG5cbiAgICByZXR1cm4gW1xuICAgICAgJ3snLFxuICAgICAgcHJlZml4KGAke3RpdGxlIHx8IHVudGl0bGVkfWApLFxuICAgICAgcHJlZml4KHBsdWdpbi5pZCksXG4gICAgICBwcmVmaXgoZGVzY3JpcHRpb24gfHwgbm9uZGVzY3JpcHQpLFxuICAgICAgcHJlZml4KCcqJy5yZXBlYXQobGVuZ3RoKSksXG4gICAgICAnJyxcbiAgICAgIGpvaW4oa2V5cy5tYXAoa2V5ID0+IGRvY3VtZW50ZWRWYWx1ZShwbHVnaW4uc2NoZW1hLCBrZXksIGRhdGFba2V5XSkpKSxcbiAgICAgICd9J1xuICAgIF0uam9pbignXFxuJyk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJucyB0aGUgZGVmYXVsdCB2YWx1ZS13aXRoLWRvY3VtZW50YXRpb24tc3RyaW5nIGZvciBhXG4gICAqIHNwZWNpZmljIHNjaGVtYSBwcm9wZXJ0eS5cbiAgICovXG4gIGZ1bmN0aW9uIGRlZmF1bHREb2N1bWVudGVkVmFsdWUoXG4gICAgc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEsXG4gICAga2V5OiBzdHJpbmdcbiAgKTogc3RyaW5nIHtcbiAgICBjb25zdCBwcm9wcyA9IChzY2hlbWEucHJvcGVydGllcyAmJiBzY2hlbWEucHJvcGVydGllc1trZXldKSB8fCB7fTtcbiAgICBjb25zdCB0eXBlID0gcHJvcHNbJ3R5cGUnXTtcbiAgICBjb25zdCBkZXNjcmlwdGlvbiA9IHByb3BzWydkZXNjcmlwdGlvbiddIHx8IG5vbmRlc2NyaXB0O1xuICAgIGNvbnN0IHRpdGxlID0gcHJvcHNbJ3RpdGxlJ10gfHwgJyc7XG4gICAgY29uc3QgcmVpZmllZCA9IHJlaWZ5RGVmYXVsdChzY2hlbWEsIGtleSk7XG4gICAgY29uc3Qgc3BhY2VzID0gaW5kZW50Lmxlbmd0aDtcbiAgICBjb25zdCBkZWZhdWx0cyA9XG4gICAgICByZWlmaWVkICE9PSB1bmRlZmluZWRcbiAgICAgICAgPyBwcmVmaXgoYFwiJHtrZXl9XCI6ICR7SlNPTi5zdHJpbmdpZnkocmVpZmllZCwgbnVsbCwgc3BhY2VzKX1gLCBpbmRlbnQpXG4gICAgICAgIDogcHJlZml4KGBcIiR7a2V5fVwiOiAke3R5cGV9YCk7XG5cbiAgICByZXR1cm4gW3ByZWZpeCh0aXRsZSksIHByZWZpeChkZXNjcmlwdGlvbiksIGRlZmF1bHRzXVxuICAgICAgLmZpbHRlcihzdHIgPT4gc3RyLmxlbmd0aClcbiAgICAgIC5qb2luKCdcXG4nKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm5zIGEgdmFsdWUtd2l0aC1kb2N1bWVudGF0aW9uLXN0cmluZyBmb3IgYSBzcGVjaWZpYyBzY2hlbWEgcHJvcGVydHkuXG4gICAqL1xuICBmdW5jdGlvbiBkb2N1bWVudGVkVmFsdWUoXG4gICAgc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEsXG4gICAga2V5OiBzdHJpbmcsXG4gICAgdmFsdWU6IEpTT05WYWx1ZVxuICApOiBzdHJpbmcge1xuICAgIGNvbnN0IHByb3BzID0gc2NoZW1hLnByb3BlcnRpZXMgJiYgc2NoZW1hLnByb3BlcnRpZXNba2V5XTtcbiAgICBjb25zdCBkZXNjcmlwdGlvbiA9IChwcm9wcyAmJiBwcm9wc1snZGVzY3JpcHRpb24nXSkgfHwgbm9uZGVzY3JpcHQ7XG4gICAgY29uc3QgdGl0bGUgPSAocHJvcHMgJiYgcHJvcHNbJ3RpdGxlJ10pIHx8IHVudGl0bGVkO1xuICAgIGNvbnN0IHNwYWNlcyA9IGluZGVudC5sZW5ndGg7XG4gICAgY29uc3QgYXR0cmlidXRlID0gcHJlZml4KFxuICAgICAgYFwiJHtrZXl9XCI6ICR7SlNPTi5zdHJpbmdpZnkodmFsdWUsIG51bGwsIHNwYWNlcyl9YCxcbiAgICAgIGluZGVudFxuICAgICk7XG5cbiAgICByZXR1cm4gW3ByZWZpeCh0aXRsZSksIHByZWZpeChkZXNjcmlwdGlvbiksIGF0dHJpYnV0ZV0uam9pbignXFxuJyk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJucyBhIGpvaW5lZCBzdHJpbmcgd2l0aCBsaW5lIGJyZWFrcyBhbmQgY29tbWFzIHdoZXJlIGFwcHJvcHJpYXRlLlxuICAgKi9cbiAgZnVuY3Rpb24gam9pbihib2R5OiBzdHJpbmdbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIGJvZHkucmVkdWNlKChhY2MsIHZhbCwgaWR4KSA9PiB7XG4gICAgICBjb25zdCByb3dzID0gdmFsLnNwbGl0KCdcXG4nKTtcbiAgICAgIGNvbnN0IGxhc3QgPSByb3dzW3Jvd3MubGVuZ3RoIC0gMV07XG4gICAgICBjb25zdCBjb21tZW50ID0gbGFzdC50cmltKCkuaW5kZXhPZignLy8nKSA9PT0gMDtcbiAgICAgIGNvbnN0IGNvbW1hID0gY29tbWVudCB8fCBpZHggPT09IGJvZHkubGVuZ3RoIC0gMSA/ICcnIDogJywnO1xuICAgICAgY29uc3Qgc2VwYXJhdG9yID0gaWR4ID09PSBib2R5Lmxlbmd0aCAtIDEgPyAnJyA6ICdcXG5cXG4nO1xuXG4gICAgICByZXR1cm4gYWNjICsgdmFsICsgY29tbWEgKyBzZXBhcmF0b3I7XG4gICAgfSwgJycpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybnMgYSBkb2N1bWVudGF0aW9uIHN0cmluZyB3aXRoIGEgY29tbWVudCBwcmVmaXggYWRkZWQgb24gZXZlcnkgbGluZS5cbiAgICovXG4gIGZ1bmN0aW9uIHByZWZpeChzb3VyY2U6IHN0cmluZywgcHJlID0gYCR7aW5kZW50fS8vIGApOiBzdHJpbmcge1xuICAgIHJldHVybiBwcmUgKyBzb3VyY2Uuc3BsaXQoJ1xcbicpLmpvaW4oYFxcbiR7cHJlfWApO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIGZ1bGx5IGV4dHJhcG9sYXRlZCBkZWZhdWx0IHZhbHVlIGZvciBhIHJvb3Qga2V5IGluIGEgc2NoZW1hLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHJlaWZ5RGVmYXVsdChcbiAgICBzY2hlbWE6IElTZXR0aW5nUmVnaXN0cnkuSVByb3BlcnR5LFxuICAgIHJvb3Q/OiBzdHJpbmcsXG4gICAgZGVmaW5pdGlvbnM/OiBQYXJ0aWFsSlNPTk9iamVjdFxuICApOiBQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkIHtcbiAgICBkZWZpbml0aW9ucyA9IGRlZmluaXRpb25zID8/IChzY2hlbWEuZGVmaW5pdGlvbnMgYXMgUGFydGlhbEpTT05PYmplY3QpO1xuICAgIC8vIElmIHRoZSBwcm9wZXJ0eSBpcyBhdCB0aGUgcm9vdCBsZXZlbCwgdHJhdmVyc2UgaXRzIHNjaGVtYS5cbiAgICBzY2hlbWEgPSAocm9vdCA/IHNjaGVtYS5wcm9wZXJ0aWVzPy5bcm9vdF0gOiBzY2hlbWEpIHx8IHt9O1xuXG4gICAgaWYgKHNjaGVtYS50eXBlID09PSAnb2JqZWN0Jykge1xuICAgICAgLy8gTWFrZSBhIGNvcHkgb2YgdGhlIGRlZmF1bHQgdmFsdWUgdG8gcG9wdWxhdGUuXG4gICAgICBjb25zdCByZXN1bHQgPSBKU09ORXh0LmRlZXBDb3B5KHNjaGVtYS5kZWZhdWx0IGFzIFBhcnRpYWxKU09OT2JqZWN0KTtcblxuICAgICAgLy8gSXRlcmF0ZSB0aHJvdWdoIGFuZCBwb3B1bGF0ZSBlYWNoIGNoaWxkIHByb3BlcnR5LlxuICAgICAgY29uc3QgcHJvcHMgPSBzY2hlbWEucHJvcGVydGllcyB8fCB7fTtcbiAgICAgIGZvciAoY29uc3QgcHJvcGVydHkgaW4gcHJvcHMpIHtcbiAgICAgICAgcmVzdWx0W3Byb3BlcnR5XSA9IHJlaWZ5RGVmYXVsdChcbiAgICAgICAgICBwcm9wc1twcm9wZXJ0eV0sXG4gICAgICAgICAgdW5kZWZpbmVkLFxuICAgICAgICAgIGRlZmluaXRpb25zXG4gICAgICAgICk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiByZXN1bHQ7XG4gICAgfSBlbHNlIGlmIChzY2hlbWEudHlwZSA9PT0gJ2FycmF5Jykge1xuICAgICAgLy8gTWFrZSBhIGNvcHkgb2YgdGhlIGRlZmF1bHQgdmFsdWUgdG8gcG9wdWxhdGUuXG4gICAgICBjb25zdCByZXN1bHQgPSBKU09ORXh0LmRlZXBDb3B5KHNjaGVtYS5kZWZhdWx0IGFzIFBhcnRpYWxKU09OQXJyYXkpO1xuXG4gICAgICAvLyBJdGVtcyBkZWZpbmVzIHRoZSBwcm9wZXJ0aWVzIG9mIGVhY2ggaXRlbSBpbiB0aGUgYXJyYXlcbiAgICAgIGxldCBwcm9wcyA9IChzY2hlbWEuaXRlbXMgYXMgUGFydGlhbEpTT05PYmplY3QpIHx8IHt9O1xuICAgICAgLy8gVXNlIHJlZmVyZW5jZWQgZGVmaW5pdGlvbiBpZiBvbmUgZXhpc3RzXG4gICAgICBpZiAocHJvcHNbJyRyZWYnXSAmJiBkZWZpbml0aW9ucykge1xuICAgICAgICBjb25zdCByZWY6IHN0cmluZyA9IChwcm9wc1snJHJlZiddIGFzIHN0cmluZykucmVwbGFjZShcbiAgICAgICAgICAnIy9kZWZpbml0aW9ucy8nLFxuICAgICAgICAgICcnXG4gICAgICAgICk7XG4gICAgICAgIHByb3BzID0gKGRlZmluaXRpb25zW3JlZl0gYXMgUGFydGlhbEpTT05PYmplY3QpID8/IHt9O1xuICAgICAgfVxuICAgICAgLy8gSXRlcmF0ZSB0aHJvdWdoIHRoZSBpdGVtcyBpbiB0aGUgYXJyYXkgYW5kIGZpbGwgaW4gZGVmYXVsdHNcbiAgICAgIGZvciAoY29uc3QgaXRlbSBpbiByZXN1bHQpIHtcbiAgICAgICAgLy8gVXNlIHRoZSB2YWx1ZXMgdGhhdCBhcmUgaGFyZC1jb2RlZCBpbiB0aGUgZGVmYXVsdCBhcnJheSBvdmVyIHRoZSBkZWZhdWx0cyBmb3IgZWFjaCBmaWVsZC5cbiAgICAgICAgY29uc3QgcmVpZmllZCA9XG4gICAgICAgICAgKHJlaWZ5RGVmYXVsdChwcm9wcywgdW5kZWZpbmVkLCBkZWZpbml0aW9ucykgYXMgUGFydGlhbEpTT05PYmplY3QpID8/XG4gICAgICAgICAge307XG4gICAgICAgIGZvciAoY29uc3QgcHJvcCBpbiByZWlmaWVkKSB7XG4gICAgICAgICAgaWYgKChyZXN1bHRbaXRlbV0gYXMgUGFydGlhbEpTT05PYmplY3QpPy5bcHJvcF0pIHtcbiAgICAgICAgICAgIHJlaWZpZWRbcHJvcF0gPSAocmVzdWx0W2l0ZW1dIGFzIFBhcnRpYWxKU09OT2JqZWN0KVtwcm9wXTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgICAgcmVzdWx0W2l0ZW1dID0gcmVpZmllZDtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHJlc3VsdDtcbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHNjaGVtYS5kZWZhdWx0O1xuICAgIH1cbiAgfVxufVxuIiwiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG5cbmltcG9ydCB7IENlbGxUeXBlIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbmJmb3JtYXQnO1xuaW1wb3J0IHsgSURhdGFDb25uZWN0b3IgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7XG4gIFBhcnRpYWxKU09OT2JqZWN0LFxuICBQYXJ0aWFsSlNPTlZhbHVlLFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUsXG4gIFRva2VuXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBJU2NoZW1hVmFsaWRhdG9yIH0gZnJvbSAnLi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHR5cGUgeyBSSlNGU2NoZW1hLCBVaVNjaGVtYSB9IGZyb20gJ0ByanNmL3V0aWxzJztcblxuLyoqXG4gKiBUaGUgc2V0dGluZyByZWdpc3RyeSB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElTZXR0aW5nUmVnaXN0cnkgPSBuZXcgVG9rZW48SVNldHRpbmdSZWdpc3RyeT4oXG4gICdAanVweXRlcmxhYi9jb3JldXRpbHM6SVNldHRpbmdSZWdpc3RyeScsXG4gIGBBIHNlcnZpY2UgZm9yIHRoZSBKdXB5dGVyTGFiIHNldHRpbmdzIHN5c3RlbS5cbiAgVXNlIHRoaXMgaWYgeW91IHdhbnQgdG8gc3RvcmUgc2V0dGluZ3MgZm9yIHlvdXIgYXBwbGljYXRpb24uXG4gIFNlZSBcInNjaGVtYURpclwiIGZvciBtb3JlIGluZm9ybWF0aW9uLmBcbik7XG5cbi8qKlxuICogVGhlIHNldHRpbmdzIHJlZ2lzdHJ5IGludGVyZmFjZS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJU2V0dGluZ1JlZ2lzdHJ5IHtcbiAgLyoqXG4gICAqIFRoZSBkYXRhIGNvbm5lY3RvciB1c2VkIGJ5IHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcmVhZG9ubHkgY29ubmVjdG9yOiBJRGF0YUNvbm5lY3RvcjxJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4sIHN0cmluZywgc3RyaW5nPjtcblxuICAvKipcbiAgICogVGhlIHNjaGVtYSBvZiB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIHJlYWRvbmx5IHNjaGVtYTogSVNldHRpbmdSZWdpc3RyeS5JU2NoZW1hO1xuXG4gIC8qKlxuICAgKiBUaGUgc2NoZW1hIHZhbGlkYXRvciB1c2VkIGJ5IHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcmVhZG9ubHkgdmFsaWRhdG9yOiBJU2NoZW1hVmFsaWRhdG9yO1xuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCB0aGF0IGVtaXRzIHRoZSBuYW1lIG9mIGEgcGx1Z2luIHdoZW4gaXRzIHNldHRpbmdzIGNoYW5nZS5cbiAgICovXG4gIHJlYWRvbmx5IHBsdWdpbkNoYW5nZWQ6IElTaWduYWw8dGhpcywgc3RyaW5nPjtcblxuICAvKipcbiAgICogVGhlIGNvbGxlY3Rpb24gb2Ygc2V0dGluZyByZWdpc3RyeSBwbHVnaW5zLlxuICAgKi9cbiAgcmVhZG9ubHkgcGx1Z2luczoge1xuICAgIFtuYW1lOiBzdHJpbmddOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4gfCB1bmRlZmluZWQ7XG4gIH07XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpbmRpdmlkdWFsIHNldHRpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyByZXRyaWV2ZWQuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSBUaGUgbmFtZSBvZiB0aGUgc2V0dGluZyBiZWluZyByZXRyaWV2ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmV0cmlldmVkLlxuICAgKi9cbiAgZ2V0KFxuICAgIHBsdWdpbjogc3RyaW5nLFxuICAgIGtleTogc3RyaW5nXG4gICk6IFByb21pc2U8e1xuICAgIGNvbXBvc2l0ZTogUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgICB1c2VyOiBQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkO1xuICB9PjtcblxuICAvKipcbiAgICogTG9hZCBhIHBsdWdpbidzIHNldHRpbmdzIGludG8gdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyBsb2FkZWQuXG4gICAqXG4gICAqIEBwYXJhbSBmb3JjZVRyYW5zZm9ybSAtIEFuIG9wdGlvbmFsIHBhcmFtZXRlciB0byBmb3JjZSByZXBsYXkgdGhlIHRyYW5zZm9ybXMgbWV0aG9kcy5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2l0aCBhIHBsdWdpbiBzZXR0aW5ncyBvYmplY3Qgb3IgcmVqZWN0c1xuICAgKiBpZiB0aGUgcGx1Z2luIGlzIG5vdCBmb3VuZC5cbiAgICovXG4gIGxvYWQoXG4gICAgcGx1Z2luOiBzdHJpbmcsXG4gICAgZm9yY2VUcmFuc2Zvcm0/OiBib29sZWFuXG4gICk6IFByb21pc2U8SVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3M+O1xuXG4gIC8qKlxuICAgKiBSZWxvYWQgYSBwbHVnaW4ncyBzZXR0aW5ncyBpbnRvIHRoZSByZWdpc3RyeSBldmVuIGlmIHRoZXkgYWxyZWFkeSBleGlzdC5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZ3MgYXJlIGJlaW5nIHJlbG9hZGVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aXRoIGEgcGx1Z2luIHNldHRpbmdzIG9iamVjdCBvciByZWplY3RzXG4gICAqIHdpdGggYSBsaXN0IG9mIGBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcmAgb2JqZWN0cyBpZiBpdCBmYWlscy5cbiAgICovXG4gIHJlbG9hZChwbHVnaW46IHN0cmluZyk6IFByb21pc2U8SVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3M+O1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBzaW5nbGUgc2V0dGluZyBpbiB0aGUgcmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmcgaXMgYmVpbmcgcmVtb3ZlZC5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHJlbW92ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmVtb3ZlZC5cbiAgICovXG4gIHJlbW92ZShwbHVnaW46IHN0cmluZywga2V5OiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+O1xuXG4gIC8qKlxuICAgKiBTZXQgYSBzaW5nbGUgc2V0dGluZyBpbiB0aGUgcmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmcgaXMgYmVpbmcgc2V0LlxuICAgKlxuICAgKiBAcGFyYW0ga2V5IC0gVGhlIG5hbWUgb2YgdGhlIHNldHRpbmcgYmVpbmcgc2V0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgb2YgdGhlIHNldHRpbmcgYmVpbmcgc2V0LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBzZXR0aW5nIGhhcyBiZWVuIHNhdmVkLlxuICAgKlxuICAgKi9cbiAgc2V0KHBsdWdpbjogc3RyaW5nLCBrZXk6IHN0cmluZywgdmFsdWU6IFBhcnRpYWxKU09OVmFsdWUpOiBQcm9taXNlPHZvaWQ+O1xuXG4gIC8qKlxuICAgKiBSZWdpc3RlciBhIHBsdWdpbiB0cmFuc2Zvcm0gZnVuY3Rpb24gdG8gYWN0IG9uIGEgc3BlY2lmaWMgcGx1Z2luLlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIG5hbWUgb2YgdGhlIHBsdWdpbiB3aG9zZSBzZXR0aW5ncyBhcmUgdHJhbnNmb3JtZWQuXG4gICAqXG4gICAqIEBwYXJhbSB0cmFuc2Zvcm1zIC0gVGhlIHRyYW5zZm9ybSBmdW5jdGlvbnMgYXBwbGllZCB0byB0aGUgcGx1Z2luLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGRpc3Bvc2FibGUgdGhhdCByZW1vdmVzIHRoZSB0cmFuc2Zvcm1zIGZyb20gdGhlIHJlZ2lzdHJ5LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIC0gYGNvbXBvc2VgIHRyYW5zZm9ybWF0aW9uczogVGhlIHJlZ2lzdHJ5IGF1dG9tYXRpY2FsbHkgb3ZlcndyaXRlcyBhXG4gICAqIHBsdWdpbidzIGRlZmF1bHQgdmFsdWVzIHdpdGggdXNlciBvdmVycmlkZXMsIGJ1dCBhIHBsdWdpbiBtYXkgaW5zdGVhZCB3aXNoXG4gICAqIHRvIG1lcmdlIHZhbHVlcy4gVGhpcyBiZWhhdmlvciBjYW4gYmUgYWNjb21wbGlzaGVkIGluIGEgYGNvbXBvc2VgXG4gICAqIHRyYW5zZm9ybWF0aW9uLlxuICAgKiAtIGBmZXRjaGAgdHJhbnNmb3JtYXRpb25zOiBUaGUgcmVnaXN0cnkgdXNlcyB0aGUgcGx1Z2luIGRhdGEgdGhhdCBpc1xuICAgKiBmZXRjaGVkIGZyb20gaXRzIGNvbm5lY3Rvci4gSWYgYSBwbHVnaW4gd2FudHMgdG8gb3ZlcnJpZGUsIGUuZy4gdG8gdXBkYXRlXG4gICAqIGl0cyBzY2hlbWEgd2l0aCBkeW5hbWljIGRlZmF1bHRzLCBhIGBmZXRjaGAgdHJhbnNmb3JtYXRpb24gY2FuIGJlIGFwcGxpZWQuXG4gICAqL1xuICB0cmFuc2Zvcm0oXG4gICAgcGx1Z2luOiBzdHJpbmcsXG4gICAgdHJhbnNmb3Jtczoge1xuICAgICAgW3BoYXNlIGluIElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5QaGFzZV0/OiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4uVHJhbnNmb3JtO1xuICAgIH1cbiAgKTogSURpc3Bvc2FibGU7XG5cbiAgLyoqXG4gICAqIFVwbG9hZCBhIHBsdWdpbidzIHNldHRpbmdzLlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIG5hbWUgb2YgdGhlIHBsdWdpbiB3aG9zZSBzZXR0aW5ncyBhcmUgYmVpbmcgc2V0LlxuICAgKlxuICAgKiBAcGFyYW0gcmF3IC0gVGhlIHJhdyBwbHVnaW4gc2V0dGluZ3MgYmVpbmcgdXBsb2FkZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmdzIGhhdmUgYmVlbiBzYXZlZC5cbiAgICovXG4gIHVwbG9hZChwbHVnaW46IHN0cmluZywgcmF3OiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+O1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBzZXR0aW5nIHJlZ2lzdHJ5IGludGVyZmFjZXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVNldHRpbmdSZWdpc3RyeSB7XG4gIC8qKlxuICAgKiBUaGUgcHJpbWl0aXZlIHR5cGVzIGF2YWlsYWJsZSBpbiBhIEpTT04gc2NoZW1hLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgUHJpbWl0aXZlID1cbiAgICB8ICdhcnJheSdcbiAgICB8ICdib29sZWFuJ1xuICAgIHwgJ251bGwnXG4gICAgfCAnbnVtYmVyJ1xuICAgIHwgJ29iamVjdCdcbiAgICB8ICdzdHJpbmcnO1xuXG4gIC8qKlxuICAgKiBUaGUgbWVudSBpZHMgZGVmaW5lZCBieSBkZWZhdWx0LlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgRGVmYXVsdE1lbnVJZCA9XG4gICAgfCAnanAtbWVudS1maWxlJ1xuICAgIHwgJ2pwLW1lbnUtZmlsZS1uZXcnXG4gICAgfCAnanAtbWVudS1lZGl0J1xuICAgIHwgJ2pwLW1lbnUtaGVscCdcbiAgICB8ICdqcC1tZW51LWtlcm5lbCdcbiAgICB8ICdqcC1tZW51LXJ1bidcbiAgICB8ICdqcC1tZW51LXNldHRpbmdzJ1xuICAgIHwgJ2pwLW1lbnUtdmlldydcbiAgICB8ICdqcC1tZW51LXRhYnMnO1xuXG4gIC8qKlxuICAgKiBBbiBpbnRlcmZhY2UgZGVmaW5pbmcgYSBtZW51LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTWVudSBleHRlbmRzIFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBVbmlxdWUgbWVudSBpZGVudGlmaWVyXG4gICAgICovXG4gICAgaWQ6IERlZmF1bHRNZW51SWQgfCBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBNZW51IGl0ZW1zXG4gICAgICovXG4gICAgaXRlbXM/OiBJTWVudUl0ZW1bXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByYW5rIG9yZGVyIG9mIHRoZSBtZW51IGFtb25nIGl0cyBzaWJsaW5ncy5cbiAgICAgKi9cbiAgICByYW5rPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogTWVudSB0aXRsZVxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIERlZmF1bHQgd2lsbCBiZSB0aGUgY2FwaXRhbGl6ZWQgaWQuXG4gICAgICovXG4gICAgbGFiZWw/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBNZW51IGljb24gaWRcbiAgICAgKlxuICAgICAqICMjIyMgTm90ZVxuICAgICAqIFRoZSBpY29uIGlkIHdpbGwgbG9va2VkIGZvciBpbiByZWdpc3RlcmVkIExhYkljb24uXG4gICAgICovXG4gICAgaWNvbj86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbW5lbW9uaWMgaW5kZXggZm9yIHRoZSB0aXRsZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgZGVmYXVsdCB2YWx1ZSBpcyBgLTFgLlxuICAgICAqL1xuICAgIG1uZW1vbmljPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciBhIG1lbnUgaXMgZGlzYWJsZWQuIGBGYWxzZWAgYnkgZGVmYXVsdC5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIGFsbG93cyBhbiB1c2VyIHRvIHN1cHByZXNzIGEgbWVudS5cbiAgICAgKi9cbiAgICBkaXNhYmxlZD86IGJvb2xlYW47XG4gIH1cblxuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGRlc2NyaWJpbmcgYSBtZW51IGl0ZW0uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNZW51SXRlbSBleHRlbmRzIFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBUaGUgdHlwZSBvZiB0aGUgbWVudSBpdGVtLlxuICAgICAqXG4gICAgICogVGhlIGRlZmF1bHQgdmFsdWUgaXMgYCdjb21tYW5kJ2AuXG4gICAgICovXG4gICAgdHlwZT86ICdjb21tYW5kJyB8ICdzdWJtZW51JyB8ICdzZXBhcmF0b3InO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbW1hbmQgdG8gZXhlY3V0ZSB3aGVuIHRoZSBpdGVtIGlzIHRyaWdnZXJlZC5cbiAgICAgKlxuICAgICAqIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGFuIGVtcHR5IHN0cmluZy5cbiAgICAgKi9cbiAgICBjb21tYW5kPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFyZ3VtZW50cyBmb3IgdGhlIGNvbW1hbmQuXG4gICAgICpcbiAgICAgKiBUaGUgZGVmYXVsdCB2YWx1ZSBpcyBhbiBlbXB0eSBvYmplY3QuXG4gICAgICovXG4gICAgYXJncz86IFBhcnRpYWxKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJhbmsgb3JkZXIgb2YgdGhlIG1lbnUgaXRlbSBhbW9uZyBpdHMgc2libGluZ3MuXG4gICAgICovXG4gICAgcmFuaz86IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBzdWJtZW51IGZvciBhIGAnc3VibWVudSdgIHR5cGUgaXRlbS5cbiAgICAgKlxuICAgICAqIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGBudWxsYC5cbiAgICAgKi9cbiAgICBzdWJtZW51PzogSU1lbnUgfCBudWxsO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciBhIG1lbnUgaXRlbSBpcyBkaXNhYmxlZC4gYGZhbHNlYCBieSBkZWZhdWx0LlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoaXMgYWxsb3dzIGFuIHVzZXIgdG8gc3VwcHJlc3MgbWVudSBpdGVtcy5cbiAgICAgKi9cbiAgICBkaXNhYmxlZD86IGJvb2xlYW47XG4gIH1cblxuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGRlc2NyaWJpbmcgYSBjb250ZXh0IG1lbnUgaXRlbVxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ29udGV4dE1lbnVJdGVtIGV4dGVuZHMgSU1lbnVJdGVtIHtcbiAgICAvKipcbiAgICAgKiBUaGUgQ1NTIHNlbGVjdG9yIGZvciB0aGUgY29udGV4dCBtZW51IGl0ZW0uXG4gICAgICpcbiAgICAgKiBUaGUgY29udGV4dCBtZW51IGl0ZW0gd2lsbCBvbmx5IGJlIGRpc3BsYXllZCBpbiB0aGUgY29udGV4dCBtZW51XG4gICAgICogd2hlbiB0aGUgc2VsZWN0b3IgbWF0Y2hlcyBhIG5vZGUgb24gdGhlIHByb3BhZ2F0aW9uIHBhdGggb2YgdGhlXG4gICAgICogY29udGV4dG1lbnUgZXZlbnQuIFRoaXMgYWxsb3dzIHRoZSBtZW51IGl0ZW0gdG8gYmUgcmVzdHJpY3RlZCB0b1xuICAgICAqIHVzZXItZGVmaW5lZCBjb250ZXh0cy5cbiAgICAgKlxuICAgICAqIFRoZSBzZWxlY3RvciBtdXN0IG5vdCBjb250YWluIGNvbW1hcy5cbiAgICAgKi9cbiAgICBzZWxlY3Rvcjogc3RyaW5nO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBzZXR0aW5ncyBmb3IgYSBzcGVjaWZpYyBwbHVnaW4uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQbHVnaW4gZXh0ZW5kcyBQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogVGhlIG5hbWUgb2YgdGhlIHBsdWdpbi5cbiAgICAgKi9cbiAgICBpZDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbGxlY3Rpb24gb2YgdmFsdWVzIGZvciBhIHNwZWNpZmllZCBwbHVnaW4uXG4gICAgICovXG4gICAgZGF0YTogSVNldHRpbmdCdW5kbGU7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcmF3IHVzZXIgc2V0dGluZ3MgZGF0YSBhcyBhIHN0cmluZyBjb250YWluaW5nIEpTT04gd2l0aCBjb21tZW50cy5cbiAgICAgKi9cbiAgICByYXc6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBKU09OIHNjaGVtYSBmb3IgdGhlIHBsdWdpbi5cbiAgICAgKi9cbiAgICBzY2hlbWE6IElTY2hlbWE7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcHVibGlzaGVkIHZlcnNpb24gb2YgdGhlIE5QTSBwYWNrYWdlIGNvbnRhaW5pbmcgdGhlIHBsdWdpbi5cbiAgICAgKi9cbiAgICB2ZXJzaW9uOiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogQSBuYW1lc3BhY2UgZm9yIHBsdWdpbiBmdW5jdGlvbmFsaXR5LlxuICAgKi9cbiAgZXhwb3J0IG5hbWVzcGFjZSBJUGx1Z2luIHtcbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRoYXQgdHJhbnNmb3JtcyBhIHBsdWdpbiBvYmplY3QgYmVmb3JlIGl0IGlzIGNvbnN1bWVkIGJ5IHRoZVxuICAgICAqIHNldHRpbmcgcmVnaXN0cnkuXG4gICAgICovXG4gICAgZXhwb3J0IHR5cGUgVHJhbnNmb3JtID0gKHBsdWdpbjogSVBsdWdpbikgPT4gSVBsdWdpbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBwaGFzZXMgZHVyaW5nIHdoaWNoIGEgdHJhbnNmb3JtYXRpb24gbWF5IGJlIGFwcGxpZWQgdG8gYSBwbHVnaW4uXG4gICAgICovXG4gICAgZXhwb3J0IHR5cGUgUGhhc2UgPSAnY29tcG9zZScgfCAnZmV0Y2gnO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgbWluaW1hbCBzdWJzZXQgb2YgdGhlIGZvcm1hbCBKU09OIFNjaGVtYSB0aGF0IGRlc2NyaWJlcyBhIHByb3BlcnR5LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJUHJvcGVydHkgZXh0ZW5kcyBQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogVGhlIGRlZmF1bHQgdmFsdWUsIGlmIGFueS5cbiAgICAgKi9cbiAgICBkZWZhdWx0PzogUGFydGlhbEpTT05WYWx1ZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBzY2hlbWEgZGVzY3JpcHRpb24uXG4gICAgICovXG4gICAgZGVzY3JpcHRpb24/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2NoZW1hJ3MgY2hpbGQgcHJvcGVydGllcy5cbiAgICAgKi9cbiAgICBwcm9wZXJ0aWVzPzogeyBbcHJvcGVydHk6IHN0cmluZ106IElQcm9wZXJ0eSB9O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHRpdGxlIG9mIGEgcHJvcGVydHkuXG4gICAgICovXG4gICAgdGl0bGU/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdHlwZSBvciB0eXBlcyBvZiB0aGUgZGF0YS5cbiAgICAgKi9cbiAgICB0eXBlPzogUHJpbWl0aXZlIHwgUHJpbWl0aXZlW107XG4gIH1cblxuICAvKipcbiAgICogQSBzY2hlbWEgdHlwZSB0aGF0IGlzIGEgbWluaW1hbCBzdWJzZXQgb2YgdGhlIGZvcm1hbCBKU09OIFNjaGVtYSBhbG9uZyB3aXRoXG4gICAqIG9wdGlvbmFsIEp1cHl0ZXJMYWIgcmVuZGVyaW5nIGhpbnRzLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJU2NoZW1hIGV4dGVuZHMgSVByb3BlcnR5IHtcbiAgICAvKipcbiAgICAgKiBUaGUgSnVweXRlckxhYiBtZW51cyB0aGF0IGFyZSBjcmVhdGVkIGJ5IGEgcGx1Z2luJ3Mgc2NoZW1hLlxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi5tZW51cyc/OiB7XG4gICAgICBtYWluOiBJTWVudVtdO1xuICAgICAgY29udGV4dDogSUNvbnRleHRNZW51SXRlbVtdO1xuICAgIH07XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRoZSBzY2hlbWEgaXMgZGVwcmVjYXRlZC5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIGZsYWcgY2FuIGJlIHVzZWQgYnkgZnVuY3Rpb25hbGl0eSB0aGF0IGxvYWRzIHRoaXMgcGx1Z2luJ3Mgc2V0dGluZ3NcbiAgICAgKiBmcm9tIHRoZSByZWdpc3RyeS4gRm9yIGV4YW1wbGUsIHRoZSBzZXR0aW5nIGVkaXRvciBkb2VzIG5vdCBkaXNwbGF5IGFcbiAgICAgKiBwbHVnaW4ncyBzZXR0aW5ncyBpZiBpdCBpcyBzZXQgdG8gYHRydWVgLlxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi5zZXR0aW5nLWRlcHJlY2F0ZWQnPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBKdXB5dGVyTGFiIGljb24gaGludC5cbiAgICAgKi9cbiAgICAnanVweXRlci5sYWIuc2V0dGluZy1pY29uJz86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBKdXB5dGVyTGFiIGljb24gY2xhc3MgaGludC5cbiAgICAgKi9cbiAgICAnanVweXRlci5sYWIuc2V0dGluZy1pY29uLWNsYXNzJz86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBKdXB5dGVyTGFiIGljb24gbGFiZWwgaGludC5cbiAgICAgKi9cbiAgICAnanVweXRlci5sYWIuc2V0dGluZy1pY29uLWxhYmVsJz86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBKdXB5dGVyTGFiIHRvb2xiYXJzIGNyZWF0ZWQgYnkgYSBwbHVnaW4ncyBzY2hlbWEuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhlIHRvb2xiYXIgaXRlbXMgYXJlIGdyb3VwZWQgYnkgZG9jdW1lbnQgb3Igd2lkZ2V0IGZhY3RvcnkgbmFtZVxuICAgICAqIHRoYXQgd2lsbCBjb250YWluIGEgdG9vbGJhci5cbiAgICAgKi9cbiAgICAnanVweXRlci5sYWIudG9vbGJhcnMnPzogeyBbZmFjdG9yeTogc3RyaW5nXTogSVRvb2xiYXJJdGVtW10gfTtcblxuICAgIC8qKlxuICAgICAqIEEgZmxhZyB0aGF0IGluZGljYXRlcyBwbHVnaW4gc2hvdWxkIGJlIHRyYW5zZm9ybWVkIGJlZm9yZSBiZWluZyB1c2VkIGJ5XG4gICAgICogdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgdGhpcyB2YWx1ZSBpcyBzZXQgdG8gYHRydWVgLCB0aGUgc2V0dGluZyByZWdpc3RyeSB3aWxsIHdhaXQgdW50aWwgYVxuICAgICAqIHRyYW5zZm9ybWF0aW9uIGhhcyBiZWVuIHJlZ2lzdGVyZWQgKGJ5IGNhbGxpbmcgdGhlIGB0cmFuc2Zvcm0oKWAgbWV0aG9kXG4gICAgICogb2YgdGhlIHJlZ2lzdHJ5KSBmb3IgdGhlIHBsdWdpbiBJRCBiZWZvcmUgcmVzb2x2aW5nIGBsb2FkKClgIHByb21pc2VzLlxuICAgICAqIFRoaXMgbWVhbnMgdGhhdCBpZiB0aGUgYXR0cmlidXRlIGlzIHNldCB0byBgdHJ1ZWAgYnV0IG5vIHRyYW5zZm9ybWF0aW9uXG4gICAgICogaXMgcmVnaXN0ZXJlZCBpbiB0aW1lLCBjYWxscyB0byBgbG9hZCgpYCBhIHBsdWdpbiB3aWxsIGV2ZW50dWFsbHkgdGltZVxuICAgICAqIG91dCBhbmQgcmVqZWN0LlxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi50cmFuc2Zvcm0nPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBKdXB5dGVyTGFiIHNob3J0Y3V0cyB0aGF0IGFyZSBjcmVhdGVkIGJ5IGEgcGx1Z2luJ3Mgc2NoZW1hLlxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi5zaG9ydGN1dHMnPzogSVNob3J0Y3V0W107XG5cbiAgICAvKipcbiAgICAgKiBUaGUgSnVweXRlckxhYiBtZXRhZGF0YS1mb3JtIHNjaGVtYVxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi5tZXRhZGF0YWZvcm1zJz86IElNZXRhZGF0YUZvcm1bXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByb290IHNjaGVtYSBpcyBhbHdheXMgYW4gb2JqZWN0LlxuICAgICAqL1xuICAgIHR5cGU6ICdvYmplY3QnO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBzZXR0aW5nIHZhbHVlcyBmb3IgYSBwbHVnaW4uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElTZXR0aW5nQnVuZGxlIGV4dGVuZHMgUGFydGlhbEpTT05PYmplY3Qge1xuICAgIC8qKlxuICAgICAqIEEgY29tcG9zaXRlIG9mIHRoZSB1c2VyIHNldHRpbmcgdmFsdWVzIGFuZCB0aGUgcGx1Z2luIHNjaGVtYSBkZWZhdWx0cy5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgYGNvbXBvc2l0ZWAgdmFsdWVzIHdpbGwgYWx3YXlzIGJlIGEgc3VwZXJzZXQgb2YgdGhlIGB1c2VyYCB2YWx1ZXMuXG4gICAgICovXG4gICAgY29tcG9zaXRlOiBQYXJ0aWFsSlNPTk9iamVjdDtcblxuICAgIC8qKlxuICAgICAqIFRoZSB1c2VyIHNldHRpbmcgdmFsdWVzLlxuICAgICAqL1xuICAgIHVzZXI6IFBhcnRpYWxKU09OT2JqZWN0O1xuICB9XG5cbiAgLyoqXG4gICAqIEFuIGludGVyZmFjZSBmb3IgbWFuaXB1bGF0aW5nIHRoZSBzZXR0aW5ncyBvZiBhIHNwZWNpZmljIHBsdWdpbi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVNldHRpbmdzIGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIHRoYXQgZW1pdHMgd2hlbiB0aGUgcGx1Z2luJ3Mgc2V0dGluZ3MgaGF2ZSBjaGFuZ2VkLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGNoYW5nZWQ6IElTaWduYWw8dGhpcywgdm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29tcG9zaXRlIG9mIHVzZXIgc2V0dGluZ3MgYW5kIGV4dGVuc2lvbiBkZWZhdWx0cy5cbiAgICAgKi9cbiAgICByZWFkb25seSBjb21wb3NpdGU6IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcGx1Z2luJ3MgSUQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgaWQ6IHN0cmluZztcblxuICAgIC8qXG4gICAgICogVGhlIHVuZGVybHlpbmcgcGx1Z2luLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHBsdWdpbiBzZXR0aW5ncyByYXcgdGV4dCB2YWx1ZS5cbiAgICAgKi9cbiAgICByZWFkb25seSByYXc6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBwbHVnaW4ncyBzY2hlbWEuXG4gICAgICovXG4gICAgcmVhZG9ubHkgc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWE7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdXNlciBzZXR0aW5ncy5cbiAgICAgKi9cbiAgICByZWFkb25seSB1c2VyOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHB1Ymxpc2hlZCB2ZXJzaW9uIG9mIHRoZSBOUE0gcGFja2FnZSBjb250YWluaW5nIHRoZXNlIHNldHRpbmdzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHZlcnNpb246IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFJldHVybiB0aGUgZGVmYXVsdHMgaW4gYSBjb21tZW50ZWQgSlNPTiBmb3JtYXQuXG4gICAgICovXG4gICAgYW5ub3RhdGVkRGVmYXVsdHMoKTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQ2FsY3VsYXRlIHRoZSBkZWZhdWx0IHZhbHVlIG9mIGEgc2V0dGluZyBieSBpdGVyYXRpbmcgdGhyb3VnaCB0aGUgc2NoZW1hLlxuICAgICAqXG4gICAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIHdob3NlIGRlZmF1bHQgdmFsdWUgaXMgY2FsY3VsYXRlZC5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIEEgY2FsY3VsYXRlZCBkZWZhdWx0IEpTT04gdmFsdWUgZm9yIGEgc3BlY2lmaWMgc2V0dGluZy5cbiAgICAgKi9cbiAgICBkZWZhdWx0KGtleTogc3RyaW5nKTogUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIEdldCBhbiBpbmRpdmlkdWFsIHNldHRpbmcuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ga2V5IC0gVGhlIG5hbWUgb2YgdGhlIHNldHRpbmcgYmVpbmcgcmV0cmlldmVkLlxuICAgICAqXG4gICAgICogQHJldHVybnMgVGhlIHNldHRpbmcgdmFsdWUuXG4gICAgICovXG4gICAgZ2V0KGtleTogc3RyaW5nKToge1xuICAgICAgY29tcG9zaXRlOiBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUgfCB1bmRlZmluZWQ7XG4gICAgICB1c2VyOiBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUgfCB1bmRlZmluZWQ7XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIFJlbW92ZSBhIHNpbmdsZSBzZXR0aW5nLlxuICAgICAqXG4gICAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHJlbW92ZWQuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBzZXR0aW5nIGlzIHJlbW92ZWQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyBmdW5jdGlvbiBpcyBhc3luY2hyb25vdXMgYmVjYXVzZSBpdCB3cml0ZXMgdG8gdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAgICovXG4gICAgcmVtb3ZlKGtleTogc3RyaW5nKTogUHJvbWlzZTx2b2lkPjtcblxuICAgIC8qKlxuICAgICAqIFNhdmUgYWxsIG9mIHRoZSBwbHVnaW4ncyB1c2VyIHNldHRpbmdzIGF0IG9uY2UuXG4gICAgICovXG4gICAgc2F2ZShyYXc6IHN0cmluZyk6IFByb21pc2U8dm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBTZXQgYSBzaW5nbGUgc2V0dGluZy5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBrZXkgLSBUaGUgbmFtZSBvZiB0aGUgc2V0dGluZyBiZWluZyBzZXQuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgb2YgdGhlIHNldHRpbmcuXG4gICAgICpcbiAgICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBzZXR0aW5nIGhhcyBiZWVuIHNhdmVkLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoaXMgZnVuY3Rpb24gaXMgYXN5bmNocm9ub3VzIGJlY2F1c2UgaXQgd3JpdGVzIHRvIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgICAqL1xuICAgIHNldChrZXk6IHN0cmluZywgdmFsdWU6IFBhcnRpYWxKU09OVmFsdWUpOiBQcm9taXNlPHZvaWQ+O1xuXG4gICAgLyoqXG4gICAgICogVmFsaWRhdGVzIHJhdyBzZXR0aW5ncyB3aXRoIGNvbW1lbnRzLlxuICAgICAqXG4gICAgICogQHBhcmFtIHJhdyAtIFRoZSBKU09OIHdpdGggY29tbWVudHMgc3RyaW5nIGJlaW5nIHZhbGlkYXRlZC5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIEEgbGlzdCBvZiBlcnJvcnMgb3IgYG51bGxgIGlmIHZhbGlkLlxuICAgICAqL1xuICAgIHZhbGlkYXRlKHJhdzogc3RyaW5nKTogSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXSB8IG51bGw7XG4gIH1cblxuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGRlc2NyaWJpbmcgYSBKdXB5dGVyTGFiIGtleWJvYXJkIHNob3J0Y3V0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJU2hvcnRjdXQgZXh0ZW5kcyBQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogVGhlIG9wdGlvbmFsIGFyZ3VtZW50cyBwYXNzZWQgaW50byB0aGUgc2hvcnRjdXQncyBjb21tYW5kLlxuICAgICAqL1xuICAgIGFyZ3M/OiBQYXJ0aWFsSlNPTk9iamVjdDtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjb21tYW5kIGludm9rZWQgYnkgdGhlIHNob3J0Y3V0LlxuICAgICAqL1xuICAgIGNvbW1hbmQ6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgYSBrZXlib2FyZCBzaG9ydGN1dCBpcyBkaXNhYmxlZC4gYEZhbHNlYCBieSBkZWZhdWx0LlxuICAgICAqL1xuICAgIGRpc2FibGVkPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBrZXkgc2VxdWVuY2Ugb2YgdGhlIHNob3J0Y3V0LlxuICAgICAqXG4gICAgICogIyMjIE5vdGVzXG4gICAgICpcbiAgICAgKiBJZiB0aGlzIGlzIGEgbGlzdCBsaWtlIGBbJ0N0cmwgQScsICdCJ11gLCB0aGUgdXNlciBuZWVkcyB0byBwcmVzc1xuICAgICAqIGBDdHJsIEFgIGZvbGxvd2VkIGJ5IGBCYCB0byB0cmlnZ2VyIHRoZSBzaG9ydGN1dHMuXG4gICAgICovXG4gICAga2V5czogc3RyaW5nW107XG5cbiAgICAvKipcbiAgICAgKiBUaGUgQ1NTIHNlbGVjdG9yIGFwcGxpY2FibGUgdG8gdGhlIHNob3J0Y3V0LlxuICAgICAqL1xuICAgIHNlbGVjdG9yOiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGRlc2NyaWJpbmcgdGhlIG1ldGFkYXRhIGZvcm0uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNZXRhZGF0YUZvcm0gZXh0ZW5kcyBQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogVGhlIHNlY3Rpb24gdW5pcXVlIElELlxuICAgICAqL1xuICAgIGlkOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbWV0YWRhdGEgc2NoZW1hLlxuICAgICAqL1xuICAgIG1ldGFkYXRhU2NoZW1hOiBJTWV0YWRhdGFTY2hlbWE7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdWkgc2NoZW1hIGFzIHVzZWQgYnkgcmVhY3QtSlNPTi1zY2hlbWEtZm9ybS5cbiAgICAgKi9cbiAgICB1aVNjaGVtYT86IHsgW21ldGFkYXRhS2V5OiBzdHJpbmddOiBVaVNjaGVtYSB9O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGp1cHl0ZXIgcHJvcGVydGllcy5cbiAgICAgKi9cbiAgICBtZXRhZGF0YU9wdGlvbnM/OiB7IFttZXRhZGF0YUtleTogc3RyaW5nXTogSU1ldGFkYXRhT3B0aW9ucyB9O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHNlY3Rpb24gbGFiZWwuXG4gICAgICovXG4gICAgbGFiZWw/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgc2VjdGlvbiByYW5rIGluIG5vdGVib29rdG9vbHMgcGFuZWwuXG4gICAgICovXG4gICAgcmFuaz86IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdG8gc2hvdyB0aGUgbW9kaWZpZWQgZmllbGQgZnJvbSBkZWZhdWx0IHZhbHVlLlxuICAgICAqL1xuICAgIHNob3dNb2RpZmllZD86IGJvb2xlYW47XG5cbiAgICAvKipcbiAgICAgKiBLZWVwIHRoZSBwbHVnaW4gYXQgb3JpZ2luIG9mIHRoZSBtZXRhZGF0YSBmb3JtLlxuICAgICAqL1xuICAgIF9vcmlnaW4/OiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG1ldGFkYXRhIHNjaGVtYSBhcyBkZWZpbmVkIGluIEpTT04gc2NoZW1hLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTWV0YWRhdGFTY2hlbWEgZXh0ZW5kcyBSSlNGU2NoZW1hIHtcbiAgICAvKipcbiAgICAgKiBUaGUgcHJvcGVydGllcyBhcyBkZWZpbmVkIGluIEpTT04gc2NoZW1hLCBhbmQgaW50ZXJwcmV0YWJsZSBieSByZWFjdC1KU09OLXNjaGVtYS1mb3JtLlxuICAgICAqL1xuICAgIHByb3BlcnRpZXM6IHsgW29wdGlvbjogc3RyaW5nXTogYW55IH07XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcmVxdWlyZWQgZmllbGRzLlxuICAgICAqL1xuICAgIHJlcXVpcmVkPzogc3RyaW5nW107XG5cbiAgICAvKipcbiAgICAgKiBTdXBwb3J0IGZvciBhbGxPZiBmZWF0dXJlIG9mIEpTT04gc2NoZW1hICh1c2VmdWwgZm9yIGlmL3RoZW4vZWxzZSkuXG4gICAgICovXG4gICAgYWxsT2Y/OiBBcnJheTxQYXJ0aWFsSlNPTk9iamVjdD47XG4gIH1cblxuICAvKipcbiAgICogT3B0aW9ucyB0byBjdXN0b21pemUgdGhlIHdpZGdldCwgdGhlIGZpZWxkIGFuZCB0aGUgcmVsZXZhbnQgbWV0YWRhdGEuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElNZXRhZGF0YU9wdGlvbnMgZXh0ZW5kcyBQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogTmFtZSBvZiBhIGN1c3RvbSByZWFjdCB3aWRnZXQgcmVnaXN0ZXJlZC5cbiAgICAgKi9cbiAgICBjdXN0b21XaWRnZXQ/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBOYW1lIG9mIGEgY3VzdG9tIHJlYWN0IGZpZWxkIHJlZ2lzdGVyZWQuXG4gICAgICovXG4gICAgY3VzdG9tRmllbGQ/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBNZXRhZGF0YSBhcHBsaWVkIHRvIG5vdGVib29rIG9yIGNlbGwuXG4gICAgICovXG4gICAgbWV0YWRhdGFMZXZlbD86ICdjZWxsJyB8ICdub3RlYm9vayc7XG5cbiAgICAvKipcbiAgICAgKiBDZWxscyB3aGljaCBzaG91bGQgaGF2ZSB0aGlzIG1ldGFkYXRhLlxuICAgICAqL1xuICAgIGNlbGxUeXBlcz86IENlbGxUeXBlW107XG5cbiAgICAvKipcbiAgICAgKiBXaGV0aGVyIHRvIGF2b2lkIHdyaXRpbmcgZGVmYXVsdCB2YWx1ZSBpbiBtZXRhZGF0YS5cbiAgICAgKi9cbiAgICB3cml0ZURlZmF1bHQ/OiBib29sZWFuO1xuICB9XG5cbiAgLyoqXG4gICAqIEFuIGludGVyZmFjZSBkZXNjcmliaW5nIGEgdG9vbGJhciBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJVG9vbGJhckl0ZW0gZXh0ZW5kcyBQYXJ0aWFsSlNPTk9iamVjdCB7XG4gICAgLyoqXG4gICAgICogVW5pcXVlIHRvb2xiYXIgaXRlbSBuYW1lXG4gICAgICovXG4gICAgbmFtZTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbW1hbmQgdG8gZXhlY3V0ZSB3aGVuIHRoZSBpdGVtIGlzIHRyaWdnZXJlZC5cbiAgICAgKlxuICAgICAqIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGFuIGVtcHR5IHN0cmluZy5cbiAgICAgKi9cbiAgICBjb21tYW5kPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFyZ3VtZW50cyBmb3IgdGhlIGNvbW1hbmQuXG4gICAgICpcbiAgICAgKiBUaGUgZGVmYXVsdCB2YWx1ZSBpcyBhbiBlbXB0eSBvYmplY3QuXG4gICAgICovXG4gICAgYXJncz86IFBhcnRpYWxKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciB0aGUgdG9vbGJhciBpdGVtIGlzIGlnbm9yZWQgKGkuZS4gbm90IGNyZWF0ZWQpLiBgZmFsc2VgIGJ5IGRlZmF1bHQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyBhbGxvd3MgYW4gdXNlciB0byBzdXBwcmVzcyB0b29sYmFyIGl0ZW1zLlxuICAgICAqL1xuICAgIGRpc2FibGVkPzogYm9vbGVhbjtcblxuICAgIC8qKlxuICAgICAqIEl0ZW0gaWNvbiBpZFxuICAgICAqXG4gICAgICogIyMjIyBOb3RlXG4gICAgICogVGhlIGlkIHdpbGwgYmUgbG9va2VkIGZvciBpbiB0aGUgTGFiSWNvbiByZWdpc3RyeS5cbiAgICAgKiBUaGUgY29tbWFuZCBpY29uIHdpbGwgYmUgb3ZlcnJpZGRlbiBieSB0aGlzIGxhYmVsIGlmIGRlZmluZWQuXG4gICAgICovXG4gICAgaWNvbj86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEl0ZW0gbGFiZWxcbiAgICAgKlxuICAgICAqICMjIyMgTm90ZVxuICAgICAqIFRoZSBjb21tYW5kIGxhYmVsIHdpbGwgYmUgb3ZlcnJpZGRlbiBieSB0aGlzIGxhYmVsIGlmIGRlZmluZWQuXG4gICAgICovXG4gICAgbGFiZWw/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcmFuayBvcmRlciBvZiB0aGUgdG9vbGJhciBpdGVtIGFtb25nIGl0cyBzaWJsaW5ncy5cbiAgICAgKi9cbiAgICByYW5rPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHR5cGUgb2YgdGhlIHRvb2xiYXIgaXRlbS5cbiAgICAgKi9cbiAgICB0eXBlPzogJ2NvbW1hbmQnIHwgJ3NwYWNlcic7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==