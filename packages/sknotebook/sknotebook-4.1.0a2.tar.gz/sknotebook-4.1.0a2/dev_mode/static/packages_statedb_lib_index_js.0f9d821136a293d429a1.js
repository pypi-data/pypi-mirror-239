"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_statedb_lib_index_js"],{

/***/ "../packages/statedb/lib/dataconnector.js":
/*!************************************************!*\
  !*** ../packages/statedb/lib/dataconnector.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DataConnector = void 0;
/**
 * An abstract class that adheres to the data connector interface.
 *
 * @typeparam T - The basic entity response type a service's connector.
 *
 * @typeparam U - The basic entity request type, which is conventionally the
 * same as the response type but may be different if a service's implementation
 * requires input data to be different from output responses. Defaults to `T`.
 *
 * @typeparam V - The basic token applied to a request, conventionally a string
 * ID or filter, but may be set to a different type when an implementation
 * requires it. Defaults to `string`.
 *
 * @typeparam W - The type of the optional `query` parameter of the `list`
 * method. Defaults to `string`.
 *
 * #### Notes
 * The only abstract method in this class is the `fetch` method, which must be
 * reimplemented by all subclasses. The `remove` and `save` methods have a
 * default implementation that returns a promise that will always reject. This
 * class is a convenience superclass for connectors that only need to `fetch`.
 */
class DataConnector {
    /**
     * Retrieve the list of items available from the data connector.
     *
     * @param query - The optional query filter to apply to the connector request.
     *
     * @returns A promise that always rejects with an error.
     *
     * #### Notes
     * Subclasses should reimplement if they support a back-end that can list.
     */
    async list(query) {
        throw new Error('DataConnector#list method has not been implemented.');
    }
    /**
     * Remove a value using the data connector.
     *
     * @param id - The identifier for the data being removed.
     *
     * @returns A promise that always rejects with an error.
     *
     * #### Notes
     * Subclasses should reimplement if they support a back-end that can remove.
     */
    async remove(id) {
        throw new Error('DataConnector#remove method has not been implemented.');
    }
    /**
     * Save a value using the data connector.
     *
     * @param id - The identifier for the data being saved.
     *
     * @param value - The data being saved.
     *
     * @returns A promise that always rejects with an error.
     *
     * #### Notes
     * Subclasses should reimplement if they support a back-end that can save.
     */
    async save(id, value) {
        throw new Error('DataConnector#save method has not been implemented.');
    }
}
exports.DataConnector = DataConnector;


/***/ }),

/***/ "../packages/statedb/lib/index.js":
/*!****************************************!*\
  !*** ../packages/statedb/lib/index.js ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module statedb
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./dataconnector */ "../packages/statedb/lib/dataconnector.js"), exports);
__exportStar(__webpack_require__(/*! ./interfaces */ "../packages/statedb/lib/interfaces.js"), exports);
__exportStar(__webpack_require__(/*! ./restorablepool */ "../packages/statedb/lib/restorablepool.js"), exports);
__exportStar(__webpack_require__(/*! ./statedb */ "../packages/statedb/lib/statedb.js"), exports);
__exportStar(__webpack_require__(/*! ./tokens */ "../packages/statedb/lib/tokens.js"), exports);


/***/ }),

/***/ "../packages/statedb/lib/interfaces.js":
/*!*********************************************!*\
  !*** ../packages/statedb/lib/interfaces.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, exports) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));


/***/ }),

/***/ "../packages/statedb/lib/restorablepool.js":
/*!*************************************************!*\
  !*** ../packages/statedb/lib/restorablepool.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RestorablePool = void 0;
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
const properties_1 = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
const signaling_1 = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/**
 * An object pool that supports restoration.
 *
 * @typeparam T - The type of object being tracked.
 */
class RestorablePool {
    /**
     * Create a new restorable pool.
     *
     * @param options - The instantiation options for a restorable pool.
     */
    constructor(options) {
        this._added = new signaling_1.Signal(this);
        this._current = null;
        this._currentChanged = new signaling_1.Signal(this);
        this._hasRestored = false;
        this._isDisposed = false;
        this._objects = new Set();
        this._restore = null;
        this._restored = new coreutils_1.PromiseDelegate();
        this._updated = new signaling_1.Signal(this);
        this.namespace = options.namespace;
    }
    /**
     * A signal emitted when an object object is added.
     *
     * #### Notes
     * This signal will only fire when an object is added to the pool.
     * It will not fire if an object injected into the pool.
     */
    get added() {
        return this._added;
    }
    /**
     * The current object.
     *
     * #### Notes
     * The restorable pool does not set `current`. It is intended for client use.
     *
     * If `current` is set to an object that does not exist in the pool, it is a
     * no-op.
     */
    get current() {
        return this._current;
    }
    set current(obj) {
        if (this._current === obj) {
            return;
        }
        if (obj !== null && this._objects.has(obj)) {
            this._current = obj;
            this._currentChanged.emit(this._current);
        }
    }
    /**
     * A signal emitted when the current widget changes.
     */
    get currentChanged() {
        return this._currentChanged;
    }
    /**
     * Test whether the pool is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * A promise resolved when the restorable pool has been restored.
     */
    get restored() {
        return this._restored.promise;
    }
    /**
     * The number of objects held by the pool.
     */
    get size() {
        return this._objects.size;
    }
    /**
     * A signal emitted when an object is updated.
     */
    get updated() {
        return this._updated;
    }
    /**
     * Add a new object to the pool.
     *
     * @param obj - The object object being added.
     *
     * #### Notes
     * The object passed into the pool is added synchronously; its existence in
     * the pool can be checked with the `has()` method. The promise this method
     * returns resolves after the object has been added and saved to an underlying
     * restoration connector, if one is available.
     */
    async add(obj) {
        var _a, _b;
        if (obj.isDisposed) {
            const warning = 'A disposed object cannot be added.';
            console.warn(warning, obj);
            throw new Error(warning);
        }
        if (this._objects.has(obj)) {
            const warning = 'This object already exists in the pool.';
            console.warn(warning, obj);
            throw new Error(warning);
        }
        this._objects.add(obj);
        obj.disposed.connect(this._onInstanceDisposed, this);
        if (Private.injectedProperty.get(obj)) {
            return;
        }
        if (this._restore) {
            const { connector } = this._restore;
            const objName = this._restore.name(obj);
            if (objName) {
                const name = `${this.namespace}:${objName}`;
                const data = (_b = (_a = this._restore).args) === null || _b === void 0 ? void 0 : _b.call(_a, obj);
                Private.nameProperty.set(obj, name);
                await connector.save(name, { data });
            }
        }
        // Emit the added signal.
        this._added.emit(obj);
    }
    /**
     * Dispose of the resources held by the pool.
     *
     * #### Notes
     * Disposing a pool does not affect the underlying data in the data connector,
     * it simply disposes the client-side pool without making any connector calls.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._current = null;
        this._isDisposed = true;
        this._objects.clear();
        signaling_1.Signal.clearData(this);
    }
    /**
     * Find the first object in the pool that satisfies a filter function.
     *
     * @param - fn The filter function to call on each object.
     */
    find(fn) {
        const values = this._objects.values();
        for (const value of values) {
            if (fn(value)) {
                return value;
            }
        }
        return undefined;
    }
    /**
     * Iterate through each object in the pool.
     *
     * @param fn - The function to call on each object.
     */
    forEach(fn) {
        this._objects.forEach(fn);
    }
    /**
     * Filter the objects in the pool based on a predicate.
     *
     * @param fn - The function by which to filter.
     */
    filter(fn) {
        const filtered = [];
        this.forEach(obj => {
            if (fn(obj)) {
                filtered.push(obj);
            }
        });
        return filtered;
    }
    /**
     * Inject an object into the restorable pool without the pool handling its
     * restoration lifecycle.
     *
     * @param obj - The object to inject into the pool.
     */
    inject(obj) {
        Private.injectedProperty.set(obj, true);
        return this.add(obj);
    }
    /**
     * Check if this pool has the specified object.
     *
     * @param obj - The object whose existence is being checked.
     */
    has(obj) {
        return this._objects.has(obj);
    }
    /**
     * Restore the objects in this pool's namespace.
     *
     * @param options - The configuration options that describe restoration.
     *
     * @returns A promise that resolves when restoration has completed.
     *
     * #### Notes
     * This function should almost never be invoked by client code. Its primary
     * use case is to be invoked by a layout restorer plugin that handles
     * multiple restorable pools and, when ready, asks them each to restore their
     * respective objects.
     */
    async restore(options) {
        if (this._hasRestored) {
            throw new Error('This pool has already been restored.');
        }
        this._hasRestored = true;
        const { command, connector, registry, when } = options;
        const namespace = this.namespace;
        const promises = when
            ? [connector.list(namespace)].concat(when)
            : [connector.list(namespace)];
        this._restore = options;
        const [saved] = await Promise.all(promises);
        const values = await Promise.all(saved.ids.map(async (id, index) => {
            const value = saved.values[index];
            const args = value && value.data;
            if (args === undefined) {
                return connector.remove(id);
            }
            // Execute the command and if it fails, delete the state restore data.
            return registry
                .execute(command, args)
                .catch(() => connector.remove(id));
        }));
        this._restored.resolve();
        return values;
    }
    /**
     * Save the restore data for a given object.
     *
     * @param obj - The object being saved.
     */
    async save(obj) {
        var _a, _b;
        const injected = Private.injectedProperty.get(obj);
        if (!this._restore || !this.has(obj) || injected) {
            return;
        }
        const { connector } = this._restore;
        const objName = this._restore.name(obj);
        const oldName = Private.nameProperty.get(obj);
        const newName = objName ? `${this.namespace}:${objName}` : '';
        if (oldName && oldName !== newName) {
            await connector.remove(oldName);
        }
        // Set the name property irrespective of whether the new name is null.
        Private.nameProperty.set(obj, newName);
        if (newName) {
            const data = (_b = (_a = this._restore).args) === null || _b === void 0 ? void 0 : _b.call(_a, obj);
            await connector.save(newName, { data });
        }
        if (oldName !== newName) {
            this._updated.emit(obj);
        }
    }
    /**
     * Clean up after disposed objects.
     */
    _onInstanceDisposed(obj) {
        this._objects.delete(obj);
        if (obj === this._current) {
            this._current = null;
            this._currentChanged.emit(this._current);
        }
        if (Private.injectedProperty.get(obj)) {
            return;
        }
        if (!this._restore) {
            return;
        }
        const { connector } = this._restore;
        const name = Private.nameProperty.get(obj);
        if (name) {
            void connector.remove(name);
        }
    }
}
exports.RestorablePool = RestorablePool;
/*
 * A namespace for private data.
 */
var Private;
(function (Private) {
    /**
     * An attached property to indicate whether an object has been injected.
     */
    Private.injectedProperty = new properties_1.AttachedProperty({
        name: 'injected',
        create: () => false
    });
    /**
     * An attached property for an object's ID.
     */
    Private.nameProperty = new properties_1.AttachedProperty({
        name: 'name',
        create: () => ''
    });
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/statedb/lib/statedb.js":
/*!******************************************!*\
  !*** ../packages/statedb/lib/statedb.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.StateDB = void 0;
const signaling_1 = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/**
 * The default concrete implementation of a state database.
 */
class StateDB {
    /**
     * Create a new state database.
     *
     * @param options - The instantiation options for a state database.
     */
    constructor(options = {}) {
        this._changed = new signaling_1.Signal(this);
        const { connector, transform } = options;
        this._connector = connector || new StateDB.Connector();
        if (!transform) {
            this._ready = Promise.resolve(undefined);
        }
        else {
            this._ready = transform.then(transformation => {
                const { contents, type } = transformation;
                switch (type) {
                    case 'cancel':
                        return;
                    case 'clear':
                        return this._clear();
                    case 'merge':
                        return this._merge(contents || {});
                    case 'overwrite':
                        return this._overwrite(contents || {});
                    default:
                        return;
                }
            });
        }
    }
    /**
     * A signal that emits the change type any time a value changes.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Clear the entire database.
     */
    async clear() {
        await this._ready;
        await this._clear();
    }
    /**
     * Retrieve a saved bundle from the database.
     *
     * @param id - The identifier used to retrieve a data bundle.
     *
     * @returns A promise that bears a data payload if available.
     *
     * #### Notes
     * The `id` values of stored items in the state database are formatted:
     * `'namespace:identifier'`, which is the same convention that command
     * identifiers in JupyterLab use as well. While this is not a technical
     * requirement for `fetch()`, `remove()`, and `save()`, it *is* necessary for
     * using the `list(namespace: string)` method.
     *
     * The promise returned by this method may be rejected if an error occurs in
     * retrieving the data. Non-existence of an `id` will succeed with the `value`
     * `undefined`.
     */
    async fetch(id) {
        await this._ready;
        return this._fetch(id);
    }
    /**
     * Retrieve all the saved bundles for a namespace.
     *
     * @param filter - The namespace prefix to retrieve.
     *
     * @returns A promise that bears a collection of payloads for a namespace.
     *
     * #### Notes
     * Namespaces are entirely conventional entities. The `id` values of stored
     * items in the state database are formatted: `'namespace:identifier'`, which
     * is the same convention that command identifiers in JupyterLab use as well.
     *
     * If there are any errors in retrieving the data, they will be logged to the
     * console in order to optimistically return any extant data without failing.
     * This promise will always succeed.
     */
    async list(namespace) {
        await this._ready;
        return this._list(namespace);
    }
    /**
     * Remove a value from the database.
     *
     * @param id - The identifier for the data being removed.
     *
     * @returns A promise that is rejected if remove fails and succeeds otherwise.
     */
    async remove(id) {
        await this._ready;
        await this._remove(id);
        this._changed.emit({ id, type: 'remove' });
    }
    /**
     * Save a value in the database.
     *
     * @param id - The identifier for the data being saved.
     *
     * @param value - The data being saved.
     *
     * @returns A promise that is rejected if saving fails and succeeds otherwise.
     *
     * #### Notes
     * The `id` values of stored items in the state database are formatted:
     * `'namespace:identifier'`, which is the same convention that command
     * identifiers in JupyterLab use as well. While this is not a technical
     * requirement for `fetch()`, `remove()`, and `save()`, it *is* necessary for
     * using the `list(namespace: string)` method.
     */
    async save(id, value) {
        await this._ready;
        await this._save(id, value);
        this._changed.emit({ id, type: 'save' });
    }
    /**
     * Return a serialized copy of the state database's entire contents.
     *
     * @returns A promise that resolves with the database contents as JSON.
     */
    async toJSON() {
        await this._ready;
        const { ids, values } = await this._list();
        return values.reduce((acc, val, idx) => {
            acc[ids[idx]] = val;
            return acc;
        }, {});
    }
    /**
     * Clear the entire database.
     */
    async _clear() {
        await Promise.all((await this._list()).ids.map(id => this._remove(id)));
    }
    /**
     * Fetch a value from the database.
     */
    async _fetch(id) {
        const value = await this._connector.fetch(id);
        if (value) {
            return JSON.parse(value).v;
        }
    }
    /**
     * Fetch a list from the database.
     */
    async _list(namespace = '') {
        const { ids, values } = await this._connector.list(namespace);
        return {
            ids,
            values: values.map(val => JSON.parse(val).v)
        };
    }
    /**
     * Merge data into the state database.
     */
    async _merge(contents) {
        await Promise.all(Object.keys(contents).map(key => contents[key] && this._save(key, contents[key])));
    }
    /**
     * Overwrite the entire database with new contents.
     */
    async _overwrite(contents) {
        await this._clear();
        await this._merge(contents);
    }
    /**
     * Remove a key in the database.
     */
    async _remove(id) {
        return this._connector.remove(id);
    }
    /**
     * Save a key and its value in the database.
     */
    async _save(id, value) {
        return this._connector.save(id, JSON.stringify({ v: value }));
    }
}
exports.StateDB = StateDB;
/**
 * A namespace for StateDB statics.
 */
(function (StateDB) {
    /**
     * An in-memory string key/value data connector.
     */
    class Connector {
        constructor() {
            this._storage = {};
        }
        /**
         * Retrieve an item from the data connector.
         */
        async fetch(id) {
            return this._storage[id];
        }
        /**
         * Retrieve the list of items available from the data connector.
         *
         * @param namespace - If not empty, only keys whose first token before `:`
         * exactly match `namespace` will be returned, e.g. `foo` in `foo:bar`.
         */
        async list(namespace = '') {
            return Object.keys(this._storage).reduce((acc, val) => {
                if (namespace === '' ? true : namespace === val.split(':')[0]) {
                    acc.ids.push(val);
                    acc.values.push(this._storage[val]);
                }
                return acc;
            }, { ids: [], values: [] });
        }
        /**
         * Remove a value using the data connector.
         */
        async remove(id) {
            delete this._storage[id];
        }
        /**
         * Save a value using the data connector.
         */
        async save(id, value) {
            this._storage[id] = value;
        }
    }
    StateDB.Connector = Connector;
})(StateDB = exports.StateDB || (exports.StateDB = {}));


/***/ }),

/***/ "../packages/statedb/lib/tokens.js":
/*!*****************************************!*\
  !*** ../packages/statedb/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.IStateDB = void 0;
const coreutils_1 = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/**
 * The default state database token.
 */
exports.IStateDB = new coreutils_1.Token('@jupyterlab/coreutils:IStateDB', `A service for the JupyterLab state database.
  Use this if you want to store data that will persist across page loads.
  See "state database" for more information.`);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfc3RhdGVkYl9saWJfaW5kZXhfanMuMGY5ZDgyMTEzNmEyOTNkNDI5YTEuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7OztBQUkzRDs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0dBcUJHO0FBQ0gsTUFBc0IsYUFBYTtJQWdCakM7Ozs7Ozs7OztPQVNHO0lBQ0gsS0FBSyxDQUFDLElBQUksQ0FBQyxLQUFTO1FBQ2xCLE1BQU0sSUFBSSxLQUFLLENBQUMscURBQXFELENBQUMsQ0FBQztJQUN6RSxDQUFDO0lBRUQ7Ozs7Ozs7OztPQVNHO0lBQ0gsS0FBSyxDQUFDLE1BQU0sQ0FBQyxFQUFLO1FBQ2hCLE1BQU0sSUFBSSxLQUFLLENBQUMsdURBQXVELENBQUMsQ0FBQztJQUMzRSxDQUFDO0lBRUQ7Ozs7Ozs7Ozs7O09BV0c7SUFDSCxLQUFLLENBQUMsSUFBSSxDQUFDLEVBQUssRUFBRSxLQUFRO1FBQ3hCLE1BQU0sSUFBSSxLQUFLLENBQUMscURBQXFELENBQUMsQ0FBQztJQUN6RSxDQUFDO0NBQ0Y7QUEzREQsc0NBMkRDOzs7Ozs7Ozs7Ozs7QUN0RkQ7OzsrRUFHK0U7QUFDL0U7OztHQUdHOzs7Ozs7Ozs7Ozs7Ozs7O0FBRUgsOEdBQWdDO0FBQ2hDLHdHQUE2QjtBQUM3QixnSEFBaUM7QUFDakMsa0dBQTBCO0FBQzFCLGdHQUF5Qjs7Ozs7Ozs7Ozs7O0FDYnpCLDBDQUEwQztBQUMxQywyREFBMkQ7Ozs7Ozs7Ozs7Ozs7QUNEM0QsMENBQTBDO0FBQzFDLDJEQUEyRDs7O0FBRTNELHdJQUFvRDtBQUVwRCw0SUFBc0Q7QUFDdEQsd0lBQW9EO0FBR3BEOzs7O0dBSUc7QUFDSCxNQUFhLGNBQWM7SUFLekI7Ozs7T0FJRztJQUNILFlBQVksT0FBZ0M7UUFzVHBDLFdBQU0sR0FBRyxJQUFJLGtCQUFNLENBQVUsSUFBSSxDQUFDLENBQUM7UUFDbkMsYUFBUSxHQUFhLElBQUksQ0FBQztRQUMxQixvQkFBZSxHQUFHLElBQUks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QUMsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLFNBQVMsS0FBSyxHQUFHLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxFQUFFO29CQUM3RCxHQUFHLENBQUMsR0FBRyxDQUFDLElBQUksQ0FBQyxHQUFHLENBQUMsQ0FBQztvQkFDbEIsR0FBRyxDQUFDLE1BQU0sQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDO2lCQUNyQztnQkFDRCxPQUFPLEdBQUcsQ0FBQztZQUNiLENBQUMsRUFDRCxFQUFFLEdBQUcsRUFBRSxFQUFjLEVBQUUsTUFBTSxFQUFFLEVBQWMsRUFBRSxDQUNoRCxDQUFDO1FBQ0osQ0FBQztRQUVEOztXQUVHO1FBQ0gsS0FBSyxDQUFDLE1BQU0sQ0FBQyxFQUFVO1lBQ3JCLE9BQU8sSUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLENBQUMsQ0FBQztRQUMzQixDQUFDO1FBRUQ7O1dBRUc7UUFDSCxLQUFLLENBQUMsSUFBSSxDQUFDLEVBQVUsRUFBRSxLQUFhO1lBQ2xDLElBQUksQ0FBQyxRQUFRLENBQUMsRUFBRSxDQUFDLEdBQUcsS0FBSyxDQUFDO1FBQzVCLENBQUM7S0FHRjtJQTFDWSxpQkFBUyxZQTBDckI7QUFDSCxDQUFDLEVBMUdnQixPQUFPLEdBQVAsZUFBTyxLQUFQLGVBQU8sUUEwR3ZCOzs7Ozs7Ozs7Ozs7QUNoVkQsMENBQTBDO0FBQzFDLDJEQUEyRDs7O0FBRTNELHdJQUFvRTtBQUdwRTs7R0FFRztBQUNVLGdCQUFRLEdBQUcsSUFBSSxpQkFBSyxDQUMvQixnQ0FBZ0MsRUFDaEM7OzZDQUUyQyxDQUM1QyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXRlZGIvc3JjL2RhdGFjb25uZWN0b3IudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3N0YXRlZGIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0ZWRiL3NyYy9pbnRlcmZhY2VzLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9zdGF0ZWRiL3NyYy9yZXN0b3JhYmxlcG9vbC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdGVkYi9zcmMvc3RhdGVkYi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc3RhdGVkYi9zcmMvdG9rZW5zLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSURhdGFDb25uZWN0b3IgfSBmcm9tICcuL2ludGVyZmFjZXMnO1xuXG4vKipcbiAqIEFuIGFic3RyYWN0IGNsYXNzIHRoYXQgYWRoZXJlcyB0byB0aGUgZGF0YSBjb25uZWN0b3IgaW50ZXJmYWNlLlxuICpcbiAqIEB0eXBlcGFyYW0gVCAtIFRoZSBiYXNpYyBlbnRpdHkgcmVzcG9uc2UgdHlwZSBhIHNlcnZpY2UncyBjb25uZWN0b3IuXG4gKlxuICogQHR5cGVwYXJhbSBVIC0gVGhlIGJhc2ljIGVudGl0eSByZXF1ZXN0IHR5cGUsIHdoaWNoIGlzIGNvbnZlbnRpb25hbGx5IHRoZVxuICogc2FtZSBhcyB0aGUgcmVzcG9uc2UgdHlwZSBidXQgbWF5IGJlIGRpZmZlcmVudCBpZiBhIHNlcnZpY2UncyBpbXBsZW1lbnRhdGlvblxuICogcmVxdWlyZXMgaW5wdXQgZGF0YSB0byBiZSBkaWZmZXJlbnQgZnJvbSBvdXRwdXQgcmVzcG9uc2VzLiBEZWZhdWx0cyB0byBgVGAuXG4gKlxuICogQHR5cGVwYXJhbSBWIC0gVGhlIGJhc2ljIHRva2VuIGFwcGxpZWQgdG8gYSByZXF1ZXN0LCBjb252ZW50aW9uYWxseSBhIHN0cmluZ1xuICogSUQgb3IgZmlsdGVyLCBidXQgbWF5IGJlIHNldCB0byBhIGRpZmZlcmVudCB0eXBlIHdoZW4gYW4gaW1wbGVtZW50YXRpb25cbiAqIHJlcXVpcmVzIGl0LiBEZWZhdWx0cyB0byBgc3RyaW5nYC5cbiAqXG4gKiBAdHlwZXBhcmFtIFcgLSBUaGUgdHlwZSBvZiB0aGUgb3B0aW9uYWwgYHF1ZXJ5YCBwYXJhbWV0ZXIgb2YgdGhlIGBsaXN0YFxuICogbWV0aG9kLiBEZWZhdWx0cyB0byBgc3RyaW5nYC5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGUgb25seSBhYnN0cmFjdCBtZXRob2QgaW4gdGhpcyBjbGFzcyBpcyB0aGUgYGZldGNoYCBtZXRob2QsIHdoaWNoIG11c3QgYmVcbiAqIHJlaW1wbGVtZW50ZWQgYnkgYWxsIHN1YmNsYXNzZXMuIFRoZSBgcmVtb3ZlYCBhbmQgYHNhdmVgIG1ldGhvZHMgaGF2ZSBhXG4gKiBkZWZhdWx0IGltcGxlbWVudGF0aW9uIHRoYXQgcmV0dXJucyBhIHByb21pc2UgdGhhdCB3aWxsIGFsd2F5cyByZWplY3QuIFRoaXNcbiAqIGNsYXNzIGlzIGEgY29udmVuaWVuY2Ugc3VwZXJjbGFzcyBmb3IgY29ubmVjdG9ycyB0aGF0IG9ubHkgbmVlZCB0byBgZmV0Y2hgLlxuICovXG5leHBvcnQgYWJzdHJhY3QgY2xhc3MgRGF0YUNvbm5lY3RvcjxULCBVID0gVCwgViA9IHN0cmluZywgVyA9IHN0cmluZz5cbiAgaW1wbGVtZW50cyBJRGF0YUNvbm5lY3RvcjxULCBVLCBWLCBXPlxue1xuICAvKipcbiAgICogUmV0cmlldmUgYW4gaXRlbSBmcm9tIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgdXNlZCB0byByZXRyaWV2ZSBhbiBpdGVtLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aXRoIGEgZGF0YSBwYXlsb2FkIGlmIGF2YWlsYWJsZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgcHJvbWlzZSByZXR1cm5lZCBieSB0aGlzIG1ldGhvZCBtYXkgYmUgcmVqZWN0ZWQgaWYgYW4gZXJyb3Igb2NjdXJzIGluXG4gICAqIHJldHJpZXZpbmcgdGhlIGRhdGEuIE5vbmV4aXN0ZW5jZSBvZiBhbiBgaWRgIHdpbGwgc3VjY2VlZCB3aXRoIGB1bmRlZmluZWRgLlxuICAgKi9cbiAgYWJzdHJhY3QgZmV0Y2goaWQ6IFYpOiBQcm9taXNlPFQgfCB1bmRlZmluZWQ+O1xuXG4gIC8qKlxuICAgKiBSZXRyaWV2ZSB0aGUgbGlzdCBvZiBpdGVtcyBhdmFpbGFibGUgZnJvbSB0aGUgZGF0YSBjb25uZWN0b3IuXG4gICAqXG4gICAqIEBwYXJhbSBxdWVyeSAtIFRoZSBvcHRpb25hbCBxdWVyeSBmaWx0ZXIgdG8gYXBwbHkgdG8gdGhlIGNvbm5lY3RvciByZXF1ZXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBhbHdheXMgcmVqZWN0cyB3aXRoIGFuIGVycm9yLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFN1YmNsYXNzZXMgc2hvdWxkIHJlaW1wbGVtZW50IGlmIHRoZXkgc3VwcG9ydCBhIGJhY2stZW5kIHRoYXQgY2FuIGxpc3QuXG4gICAqL1xuICBhc3luYyBsaXN0KHF1ZXJ5PzogVyk6IFByb21pc2U8eyBpZHM6IFZbXTsgdmFsdWVzOiBUW10gfT4ge1xuICAgIHRocm93IG5ldyBFcnJvcignRGF0YUNvbm5lY3RvciNsaXN0IG1ldGhvZCBoYXMgbm90IGJlZW4gaW1wbGVtZW50ZWQuJyk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGEgdmFsdWUgdXNpbmcgdGhlIGRhdGEgY29ubmVjdG9yLlxuICAgKlxuICAgKiBAcGFyYW0gaWQgLSBUaGUgaWRlbnRpZmllciBmb3IgdGhlIGRhdGEgYmVpbmcgcmVtb3ZlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgYWx3YXlzIHJlamVjdHMgd2l0aCBhbiBlcnJvci5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBTdWJjbGFzc2VzIHNob3VsZCByZWltcGxlbWVudCBpZiB0aGV5IHN1cHBvcnQgYSBiYWNrLWVuZCB0aGF0IGNhbiByZW1vdmUuXG4gICAqL1xuICBhc3luYyByZW1vdmUoaWQ6IFYpOiBQcm9taXNlPGFueT4ge1xuICAgIHRocm93IG5ldyBFcnJvcignRGF0YUNvbm5lY3RvciNyZW1vdmUgbWV0aG9kIGhhcyBub3QgYmVlbiBpbXBsZW1lbnRlZC4nKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTYXZlIGEgdmFsdWUgdXNpbmcgdGhlIGRhdGEgY29ubmVjdG9yLlxuICAgKlxuICAgKiBAcGFyYW0gaWQgLSBUaGUgaWRlbnRpZmllciBmb3IgdGhlIGRhdGEgYmVpbmcgc2F2ZWQuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSBkYXRhIGJlaW5nIHNhdmVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBhbHdheXMgcmVqZWN0cyB3aXRoIGFuIGVycm9yLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFN1YmNsYXNzZXMgc2hvdWxkIHJlaW1wbGVtZW50IGlmIHRoZXkgc3VwcG9ydCBhIGJhY2stZW5kIHRoYXQgY2FuIHNhdmUuXG4gICAqL1xuICBhc3luYyBzYXZlKGlkOiBWLCB2YWx1ZTogVSk6IFByb21pc2U8YW55PiB7XG4gICAgdGhyb3cgbmV3IEVycm9yKCdEYXRhQ29ubmVjdG9yI3NhdmUgbWV0aG9kIGhhcyBub3QgYmVlbiBpbXBsZW1lbnRlZC4nKTtcbiAgfVxufVxuIiwiLyogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBzdGF0ZWRiXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9kYXRhY29ubmVjdG9yJztcbmV4cG9ydCAqIGZyb20gJy4vaW50ZXJmYWNlcyc7XG5leHBvcnQgKiBmcm9tICcuL3Jlc3RvcmFibGVwb29sJztcbmV4cG9ydCAqIGZyb20gJy4vc3RhdGVkYic7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHtcbiAgUmVhZG9ubHlQYXJ0aWFsSlNPTk9iamVjdCxcbiAgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlLCBJT2JzZXJ2YWJsZURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuaW1wb3J0IHsgSVNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcblxuLyoqXG4gKiBUaGUgZGVzY3JpcHRpb24gb2YgYSBnZW5lcmFsIHB1cnBvc2UgZGF0YSBjb25uZWN0b3IuXG4gKlxuICogQHR5cGVwYXJhbSBUIC0gVGhlIGJhc2ljIGVudGl0eSByZXNwb25zZSB0eXBlIGEgc2VydmljZSdzIGNvbm5lY3Rvci5cbiAqXG4gKiBAdHlwZXBhcmFtIFUgLSBUaGUgYmFzaWMgZW50aXR5IHJlcXVlc3QgdHlwZSwgd2hpY2ggaXMgY29udmVudGlvbmFsbHkgdGhlXG4gKiBzYW1lIGFzIHRoZSByZXNwb25zZSB0eXBlIGJ1dCBtYXkgYmUgZGlmZmVyZW50IGlmIGEgc2VydmljZSdzIGltcGxlbWVudGF0aW9uXG4gKiByZXF1aXJlcyBpbnB1dCBkYXRhIHRvIGJlIGRpZmZlcmVudCBmcm9tIG91dHB1dCByZXNwb25zZXMuIERlZmF1bHRzIHRvIGBUYC5cbiAqXG4gKiBAdHlwZXBhcmFtIFYgLSBUaGUgYmFzaWMgdG9rZW4gYXBwbGllZCB0byBhIHJlcXVlc3QsIGNvbnZlbnRpb25hbGx5IGEgc3RyaW5nXG4gKiBJRCBvciBmaWx0ZXIsIGJ1dCBtYXkgYmUgc2V0IHRvIGEgZGlmZmVyZW50IHR5cGUgd2hlbiBhbiBpbXBsZW1lbnRhdGlvblxuICogcmVxdWlyZXMgaXQuIERlZmF1bHRzIHRvIGBzdHJpbmdgLlxuICpcbiAqIEB0eXBlcGFyYW0gVyAtIFRoZSB0eXBlIG9mIHRoZSBvcHRpb25hbCBgcXVlcnlgIHBhcmFtZXRlciBvZiB0aGUgYGxpc3RgXG4gKiBtZXRob2QuIERlZmF1bHRzIHRvIGBzdHJpbmdgO1xuICovXG5leHBvcnQgaW50ZXJmYWNlIElEYXRhQ29ubmVjdG9yPFQsIFUgPSBULCBWID0gc3RyaW5nLCBXID0gc3RyaW5nPiB7XG4gIC8qKlxuICAgKiBSZXRyaWV2ZSBhbiBpdGVtIGZyb20gdGhlIGRhdGEgY29ubmVjdG9yLlxuICAgKlxuICAgKiBAcGFyYW0gaWQgLSBUaGUgaWRlbnRpZmllciB1c2VkIHRvIHJldHJpZXZlIGFuIGl0ZW0uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGJlYXJzIGEgZGF0YSBwYXlsb2FkIGlmIGF2YWlsYWJsZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgcHJvbWlzZSByZXR1cm5lZCBieSB0aGlzIG1ldGhvZCBtYXkgYmUgcmVqZWN0ZWQgaWYgYW4gZXJyb3Igb2NjdXJzIGluXG4gICAqIHJldHJpZXZpbmcgdGhlIGRhdGEuIE5vbmV4aXN0ZW5jZSBvZiBhbiBgaWRgIHJlc29sdmVzIHdpdGggYHVuZGVmaW5lZGAuXG4gICAqL1xuICBmZXRjaChpZDogVik6IFByb21pc2U8VCB8IHVuZGVmaW5lZD47XG5cbiAgLyoqXG4gICAqIFJldHJpZXZlIHRoZSBsaXN0IG9mIGl0ZW1zIGF2YWlsYWJsZSBmcm9tIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICpcbiAgICogQHBhcmFtIHF1ZXJ5IC0gVGhlIG9wdGlvbmFsIHF1ZXJ5IGZpbHRlciB0byBhcHBseSB0byB0aGUgY29ubmVjdG9yIHJlcXVlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGJlYXJzIGEgbGlzdCBvZiBgdmFsdWVzYCBhbmQgYW4gYXNzb2NpYXRlZCBsaXN0IG9mXG4gICAqIGZldGNoIGBpZHNgLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBwcm9taXNlIHJldHVybmVkIGJ5IHRoaXMgbWV0aG9kIG1heSBiZSByZWplY3RlZCBpZiBhbiBlcnJvciBvY2N1cnMgaW5cbiAgICogcmV0cmlldmluZyB0aGUgZGF0YS4gVGhlIHR3byBsaXN0cyB3aWxsIGFsd2F5cyBiZSB0aGUgc2FtZSBzaXplLiBJZiB0aGVyZVxuICAgKiBpcyBubyBkYXRhLCB0aGlzIG1ldGhvZCB3aWxsIHN1Y2NlZWQgd2l0aCBlbXB0eSBgaWRzYCBhbmQgYHZhbHVlc2AuXG4gICAqL1xuICBsaXN0KHF1ZXJ5PzogVyk6IFByb21pc2U8eyBpZHM6IFZbXTsgdmFsdWVzOiBUW10gfT47XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIHZhbHVlIHVzaW5nIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgZm9yIHRoZSBkYXRhIGJlaW5nIHJlbW92ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGlzIHJlamVjdGVkIGlmIHJlbW92ZSBmYWlscyBhbmQgc3VjY2VlZHMgb3RoZXJ3aXNlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgcHJvbWlzZSBtYXkgcmVzb2x2ZSB3aXRoIGEgYmFjay1lbmQgcmVzcG9uc2Ugb3IgYHVuZGVmaW5lZGAuXG4gICAqIEV4aXN0ZW5jZSBvZiByZXNvbHZlZCBjb250ZW50IGluIHRoZSBwcm9taXNlIGlzIG5vdCBwcmVzY3JpYmVkIGFuZCBtdXN0IGJlXG4gICAqIHRlc3RlZCBmb3IuIEZvciBleGFtcGxlLCBzb21lIGJhY2stZW5kcyBtYXkgcmV0dXJuIGEgY29weSBvZiB0aGUgaXRlbSBvZlxuICAgKiB0eXBlIGBUYCBiZWluZyByZW1vdmVkIHdoaWxlIG90aGVycyBtYXkgcmV0dXJuIG5vIGNvbnRlbnQuXG4gICAqL1xuICByZW1vdmUoaWQ6IFYpOiBQcm9taXNlPGFueT47XG5cbiAgLyoqXG4gICAqIFNhdmUgYSB2YWx1ZSB1c2luZyB0aGUgZGF0YSBjb25uZWN0b3IuXG4gICAqXG4gICAqIEBwYXJhbSBpZCAtIFRoZSBpZGVudGlmaWVyIGZvciB0aGUgZGF0YSBiZWluZyBzYXZlZC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIGRhdGEgYmVpbmcgc2F2ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGlzIHJlamVjdGVkIGlmIHNhdmluZyBmYWlscyBhbmQgc3VjY2VlZHMgb3RoZXJ3aXNlLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgcHJvbWlzZSBtYXkgcmVzb2x2ZSB3aXRoIGEgYmFjay1lbmQgcmVzcG9uc2Ugb3IgYHVuZGVmaW5lZGAuXG4gICAqIEV4aXN0ZW5jZSBvZiByZXNvbHZlZCBjb250ZW50IGluIHRoZSBwcm9taXNlIGlzIG5vdCBwcmVzY3JpYmVkIGFuZCBtdXN0IGJlXG4gICAqIHRlc3RlZCBmb3IuIEZvciBleGFtcGxlLCBzb21lIGJhY2stZW5kcyBtYXkgcmV0dXJuIGEgY29weSBvZiB0aGUgaXRlbSBvZlxuICAgKiB0eXBlIGBUYCBiZWluZyBzYXZlZCB3aGlsZSBvdGhlcnMgbWF5IHJldHVybiBubyBjb250ZW50LlxuICAgKi9cbiAgc2F2ZShpZDogViwgdmFsdWU6IFUpOiBQcm9taXNlPGFueT47XG59XG5cbi8qKlxuICogQSBwb29sIG9mIG9iamVjdHMgd2hvc2UgZGlzcG9zYWJsZSBsaWZlY3ljbGUgaXMgdHJhY2tlZC5cbiAqXG4gKiBAdHlwZXBhcmFtIFQgLSBUaGUgdHlwZSBvZiBvYmplY3QgaGVsZCBpbiB0aGUgcG9vbC5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJT2JqZWN0UG9vbDxUIGV4dGVuZHMgSU9ic2VydmFibGVEaXNwb3NhYmxlPlxuICBleHRlbmRzIElEaXNwb3NhYmxlIHtcbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhbiBvYmplY3QgaXMgYWRkZWQuXG4gICAqXG4gICAqICMjIyNcbiAgICogVGhpcyBzaWduYWwgZG9lcyBub3QgZW1pdCBpZiBhbiBvYmplY3QgaXMgYWRkZWQgdXNpbmcgYGluamVjdCgpYC5cbiAgICovXG4gIHJlYWRvbmx5IGFkZGVkOiBJU2lnbmFsPHRoaXMsIFQ+O1xuXG4gIC8qKlxuICAgKiBUaGUgY3VycmVudCBvYmplY3QuXG4gICAqL1xuICByZWFkb25seSBjdXJyZW50OiBUIHwgbnVsbDtcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBjdXJyZW50IG9iamVjdCBjaGFuZ2VzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIElmIHRoZSBsYXN0IG9iamVjdCBiZWluZyB0cmFja2VkIGlzIGRpc3Bvc2VkLCBgbnVsbGAgd2lsbCBiZSBlbWl0dGVkLlxuICAgKi9cbiAgcmVhZG9ubHkgY3VycmVudENoYW5nZWQ6IElTaWduYWw8dGhpcywgVCB8IG51bGw+O1xuXG4gIC8qKlxuICAgKiBUaGUgbnVtYmVyIG9mIG9iamVjdHMgaGVsZCBieSB0aGUgcG9vbC5cbiAgICovXG4gIHJlYWRvbmx5IHNpemU6IG51bWJlcjtcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIGFuIG9iamVjdCBpcyB1cGRhdGVkLlxuICAgKi9cbiAgcmVhZG9ubHkgdXBkYXRlZDogSVNpZ25hbDx0aGlzLCBUPjtcblxuICAvKipcbiAgICogRmluZCB0aGUgZmlyc3Qgb2JqZWN0IGluIHRoZSBwb29sIHRoYXQgc2F0aXNmaWVzIGEgZmlsdGVyIGZ1bmN0aW9uLlxuICAgKlxuICAgKiBAcGFyYW0gLSBmbiBUaGUgZmlsdGVyIGZ1bmN0aW9uIHRvIGNhbGwgb24gZWFjaCBvYmplY3QuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogSWYgbm90aGluZyBpcyBmb3VuZCwgdGhlIHZhbHVlIHJldHVybmVkIGlzIGB1bmRlZmluZWRgLlxuICAgKi9cbiAgZmluZChmbjogKG9iajogVCkgPT4gYm9vbGVhbik6IFQgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIEl0ZXJhdGUgdGhyb3VnaCBlYWNoIG9iamVjdCBpbiB0aGUgcG9vbC5cbiAgICpcbiAgICogQHBhcmFtIGZuIC0gVGhlIGZ1bmN0aW9uIHRvIGNhbGwgb24gZWFjaCBvYmplY3QuXG4gICAqL1xuICBmb3JFYWNoKGZuOiAob2JqOiBUKSA9PiB2b2lkKTogdm9pZDtcblxuICAvKipcbiAgICogRmlsdGVyIHRoZSBvYmplY3RzIGluIHRoZSBwb29sIGJhc2VkIG9uIGEgcHJlZGljYXRlLlxuICAgKlxuICAgKiBAcGFyYW0gZm4gLSBUaGUgZnVuY3Rpb24gYnkgd2hpY2ggdG8gZmlsdGVyLlxuICAgKi9cbiAgZmlsdGVyKGZuOiAob2JqOiBUKSA9PiBib29sZWFuKTogVFtdO1xuXG4gIC8qKlxuICAgKiBDaGVjayBpZiB0aGlzIHBvb2wgaGFzIHRoZSBzcGVjaWZpZWQgb2JqZWN0LlxuICAgKlxuICAgKiBAcGFyYW0gb2JqIC0gVGhlIG9iamVjdCB3aG9zZSBleGlzdGVuY2UgaXMgYmVpbmcgY2hlY2tlZC5cbiAgICovXG4gIGhhcyhvYmo6IFQpOiBib29sZWFuO1xufVxuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgYSBzdGF0ZSByZXN0b3Jlci5cbiAqXG4gKiBAdHlwZXBhcmFtIFQgLSBUaGUgcmVzdG9yYWJsZSBjb2xsZWN0aW9uJ3MgdHlwZS5cbiAqXG4gKiBAdHlwZXBhcmFtIFUgLSBUaGUgdHlwZSBvZiBvYmplY3QgaGVsZCBieSB0aGUgcmVzdG9yYWJsZSBjb2xsZWN0aW9uLlxuICpcbiAqIEB0eXBlcGFyYW0gViAtIFRoZSBgcmVzdG9yZWRgIHByb21pc2UgcmVzb2x1dGlvbiB0eXBlLiBEZWZhdWx0cyB0byBgYW55YC5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJUmVzdG9yZXI8XG4gIFQgZXh0ZW5kcyBJUmVzdG9yYWJsZTxVPiA9IElSZXN0b3JhYmxlPElPYnNlcnZhYmxlRGlzcG9zYWJsZT4sXG4gIFUgZXh0ZW5kcyBJT2JzZXJ2YWJsZURpc3Bvc2FibGUgPSBJT2JzZXJ2YWJsZURpc3Bvc2FibGUsXG4gIFYgPSBhbnlcbj4ge1xuICAvKipcbiAgICogUmVzdG9yZSB0aGUgb2JqZWN0cyBpbiBhIGdpdmVuIHJlc3RvcmFibGUgY29sbGVjdGlvbi5cbiAgICpcbiAgICogQHBhcmFtIHJlc3RvcmFibGUgLSBUaGUgcmVzdG9yYWJsZSBjb2xsZWN0aW9uIGJlaW5nIHJlc3RvcmVkLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBjb25maWd1cmF0aW9uIG9wdGlvbnMgdGhhdCBkZXNjcmliZSByZXN0b3JhdGlvbi5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgc2V0dGxlcyB3aGVuIHJlc3RvcmVkIHdpdGggYGFueWAgcmVzdWx0cy5cbiAgICpcbiAgICovXG4gIHJlc3RvcmUocmVzdG9yYWJsZTogVCwgb3B0aW9uczogSVJlc3RvcmFibGUuSU9wdGlvbnM8VT4pOiBQcm9taXNlPFY+O1xuXG4gIC8qKlxuICAgKiBBIHByb21pc2UgdGhhdCBzZXR0bGVzIHdoZW4gdGhlIGNvbGxlY3Rpb24gaGFzIGJlZW4gcmVzdG9yZWQuXG4gICAqL1xuICByZWFkb25seSByZXN0b3JlZDogUHJvbWlzZTxWPjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYElSZXN0b3JlcmAgaW50ZXJmYWNlIGRlZmluaXRpb25zLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElSZXN0b3JlciB7XG4gIC8qKlxuICAgKiBUaGUgc3RhdGUgcmVzdG9yYXRpb24gY29uZmlndXJhdGlvbiBvcHRpb25zLlxuICAgKlxuICAgKiBAdHlwZXBhcmFtIFQgLSBUaGUgdHlwZSBvZiBvYmplY3QgaGVsZCBieSB0aGUgcmVzdG9yYWJsZSBjb2xsZWN0aW9uLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9uczxUIGV4dGVuZHMgSU9ic2VydmFibGVEaXNwb3NhYmxlPiB7XG4gICAgLyoqXG4gICAgICogVGhlIGNvbW1hbmQgdG8gZXhlY3V0ZSB3aGVuIHJlc3RvcmluZyBpbnN0YW5jZXMuXG4gICAgICovXG4gICAgY29tbWFuZDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQSBmdW5jdGlvbiB0aGF0IHJldHVybnMgdGhlIGFyZ3MgbmVlZGVkIHRvIHJlc3RvcmUgYW4gaW5zdGFuY2UuXG4gICAgICovXG4gICAgYXJncz86IChvYmo6IFQpID0+IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBBIGZ1bmN0aW9uIHRoYXQgcmV0dXJucyBhIHVuaXF1ZSBwZXJzaXN0ZW50IG5hbWUgZm9yIHRoaXMgaW5zdGFuY2UuXG4gICAgICovXG4gICAgbmFtZTogKG9iajogVCkgPT4gc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHBvaW50IGFmdGVyIHdoaWNoIGl0IGlzIHNhZmUgdG8gcmVzdG9yZSBzdGF0ZS5cbiAgICAgKi9cbiAgICB3aGVuPzogUHJvbWlzZTxhbnk+IHwgQXJyYXk8UHJvbWlzZTxhbnk+PjtcbiAgfVxufVxuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3Igb2JqZWN0cyB0aGF0IGNhbiBiZSByZXN0b3JlZC5cbiAqXG4gKiBAdHlwZXBhcmFtIFQgLSBUaGUgdHlwZSBvZiBvYmplY3QgaGVsZCBieSB0aGUgcmVzdG9yYWJsZSBjb2xsZWN0aW9uLlxuICpcbiAqIEB0eXBlcGFyYW0gVSAtIFRoZSBgcmVzdG9yZWRgIHByb21pc2UgcmVzb2x1dGlvbiB0eXBlLiBEZWZhdWx0cyB0byBgYW55YC5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJUmVzdG9yYWJsZTxUIGV4dGVuZHMgSU9ic2VydmFibGVEaXNwb3NhYmxlLCBVID0gYW55PiB7XG4gIC8qKlxuICAgKiBSZXN0b3JlIHRoZSBvYmplY3RzIGluIHRoaXMgcmVzdG9yYWJsZSBjb2xsZWN0aW9uLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBjb25maWd1cmF0aW9uIG9wdGlvbnMgdGhhdCBkZXNjcmliZSByZXN0b3JhdGlvbi5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgc2V0dGxlcyB3aGVuIHJlc3RvcmVkIHdpdGggYGFueWAgcmVzdWx0cy5cbiAgICpcbiAgICovXG4gIHJlc3RvcmUob3B0aW9uczogSVJlc3RvcmFibGUuSU9wdGlvbnM8VD4pOiBQcm9taXNlPFU+O1xuXG4gIC8qKlxuICAgKiBBIHByb21pc2UgdGhhdCBzZXR0bGVzIHdoZW4gdGhlIGNvbGxlY3Rpb24gaGFzIGJlZW4gcmVzdG9yZWQuXG4gICAqL1xuICByZWFkb25seSByZXN0b3JlZDogUHJvbWlzZTxVPjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYElSZXN0b3JhYmxlYCBpbnRlcmZhY2UgZGVmaW5pdGlvbnMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVJlc3RvcmFibGUge1xuICAvKipcbiAgICogVGhlIHN0YXRlIHJlc3RvcmF0aW9uIGNvbmZpZ3VyYXRpb24gb3B0aW9ucy5cbiAgICpcbiAgICogQHR5cGVwYXJhbSBUIC0gVGhlIHR5cGUgb2Ygb2JqZWN0IGhlbGQgYnkgdGhlIHJlc3RvcmFibGUgY29sbGVjdGlvbi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnM8VCBleHRlbmRzIElPYnNlcnZhYmxlRGlzcG9zYWJsZT5cbiAgICBleHRlbmRzIElSZXN0b3Jlci5JT3B0aW9uczxUPiB7XG4gICAgLyoqXG4gICAgICogVGhlIGRhdGEgY29ubmVjdG9yIHRvIGZldGNoIHJlc3RvcmUgZGF0YS5cbiAgICAgKi9cbiAgICBjb25uZWN0b3I6IElEYXRhQ29ubmVjdG9yPFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZT47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29tbWFuZCByZWdpc3RyeSB3aGljaCBob2xkcyB0aGUgcmVzdG9yZSBjb21tYW5kLlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBDb21tYW5kUmVnaXN0cnk7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgUHJvbWlzZURlbGVnYXRlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSU9ic2VydmFibGVEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IEF0dGFjaGVkUHJvcGVydHkgfSBmcm9tICdAbHVtaW5vL3Byb3BlcnRpZXMnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgSU9iamVjdFBvb2wsIElSZXN0b3JhYmxlIH0gZnJvbSAnLi9pbnRlcmZhY2VzJztcblxuLyoqXG4gKiBBbiBvYmplY3QgcG9vbCB0aGF0IHN1cHBvcnRzIHJlc3RvcmF0aW9uLlxuICpcbiAqIEB0eXBlcGFyYW0gVCAtIFRoZSB0eXBlIG9mIG9iamVjdCBiZWluZyB0cmFja2VkLlxuICovXG5leHBvcnQgY2xhc3MgUmVzdG9yYWJsZVBvb2w8XG4gICAgVCBleHRlbmRzIElPYnNlcnZhYmxlRGlzcG9zYWJsZSA9IElPYnNlcnZhYmxlRGlzcG9zYWJsZVxuICA+XG4gIGltcGxlbWVudHMgSU9iamVjdFBvb2w8VD4sIElSZXN0b3JhYmxlPFQ+XG57XG4gIC8qKlxuICAgKiBDcmVhdGUgYSBuZXcgcmVzdG9yYWJsZSBwb29sLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgcmVzdG9yYWJsZSBwb29sLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogUmVzdG9yYWJsZVBvb2wuSU9wdGlvbnMpIHtcbiAgICB0aGlzLm5hbWVzcGFjZSA9IG9wdGlvbnMubmFtZXNwYWNlO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgbmFtZXNwYWNlIGZvciBhbGwgdHJhY2tlZCBvYmplY3RzLlxuICAgKi9cbiAgcmVhZG9ubHkgbmFtZXNwYWNlOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhbiBvYmplY3Qgb2JqZWN0IGlzIGFkZGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgc2lnbmFsIHdpbGwgb25seSBmaXJlIHdoZW4gYW4gb2JqZWN0IGlzIGFkZGVkIHRvIHRoZSBwb29sLlxuICAgKiBJdCB3aWxsIG5vdCBmaXJlIGlmIGFuIG9iamVjdCBpbmplY3RlZCBpbnRvIHRoZSBwb29sLlxuICAgKi9cbiAgZ2V0IGFkZGVkKCk6IElTaWduYWw8dGhpcywgVD4ge1xuICAgIHJldHVybiB0aGlzLl9hZGRlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgY3VycmVudCBvYmplY3QuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIHJlc3RvcmFibGUgcG9vbCBkb2VzIG5vdCBzZXQgYGN1cnJlbnRgLiBJdCBpcyBpbnRlbmRlZCBmb3IgY2xpZW50IHVzZS5cbiAgICpcbiAgICogSWYgYGN1cnJlbnRgIGlzIHNldCB0byBhbiBvYmplY3QgdGhhdCBkb2VzIG5vdCBleGlzdCBpbiB0aGUgcG9vbCwgaXQgaXMgYVxuICAgKiBuby1vcC5cbiAgICovXG4gIGdldCBjdXJyZW50KCk6IFQgfCBudWxsIHtcbiAgICByZXR1cm4gdGhpcy5fY3VycmVudDtcbiAgfVxuICBzZXQgY3VycmVudChvYmo6IFQgfCBudWxsKSB7XG4gICAgaWYgKHRoaXMuX2N1cnJlbnQgPT09IG9iaikge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBpZiAob2JqICE9PSBudWxsICYmIHRoaXMuX29iamVjdHMuaGFzKG9iaikpIHtcbiAgICAgIHRoaXMuX2N1cnJlbnQgPSBvYmo7XG4gICAgICB0aGlzLl9jdXJyZW50Q2hhbmdlZC5lbWl0KHRoaXMuX2N1cnJlbnQpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGN1cnJlbnQgd2lkZ2V0IGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY3VycmVudENoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBUIHwgbnVsbD4ge1xuICAgIHJldHVybiB0aGlzLl9jdXJyZW50Q2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUZXN0IHdoZXRoZXIgdGhlIHBvb2wgaXMgZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHByb21pc2UgcmVzb2x2ZWQgd2hlbiB0aGUgcmVzdG9yYWJsZSBwb29sIGhhcyBiZWVuIHJlc3RvcmVkLlxuICAgKi9cbiAgZ2V0IHJlc3RvcmVkKCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9yZXN0b3JlZC5wcm9taXNlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBudW1iZXIgb2Ygb2JqZWN0cyBoZWxkIGJ5IHRoZSBwb29sLlxuICAgKi9cbiAgZ2V0IHNpemUoKTogbnVtYmVyIHtcbiAgICByZXR1cm4gdGhpcy5fb2JqZWN0cy5zaXplO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiBhbiBvYmplY3QgaXMgdXBkYXRlZC5cbiAgICovXG4gIGdldCB1cGRhdGVkKCk6IElTaWduYWw8dGhpcywgVD4ge1xuICAgIHJldHVybiB0aGlzLl91cGRhdGVkO1xuICB9XG5cbiAgLyoqXG4gICAqIEFkZCBhIG5ldyBvYmplY3QgdG8gdGhlIHBvb2wuXG4gICAqXG4gICAqIEBwYXJhbSBvYmogLSBUaGUgb2JqZWN0IG9iamVjdCBiZWluZyBhZGRlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgb2JqZWN0IHBhc3NlZCBpbnRvIHRoZSBwb29sIGlzIGFkZGVkIHN5bmNocm9ub3VzbHk7IGl0cyBleGlzdGVuY2UgaW5cbiAgICogdGhlIHBvb2wgY2FuIGJlIGNoZWNrZWQgd2l0aCB0aGUgYGhhcygpYCBtZXRob2QuIFRoZSBwcm9taXNlIHRoaXMgbWV0aG9kXG4gICAqIHJldHVybnMgcmVzb2x2ZXMgYWZ0ZXIgdGhlIG9iamVjdCBoYXMgYmVlbiBhZGRlZCBhbmQgc2F2ZWQgdG8gYW4gdW5kZXJseWluZ1xuICAgKiByZXN0b3JhdGlvbiBjb25uZWN0b3IsIGlmIG9uZSBpcyBhdmFpbGFibGUuXG4gICAqL1xuICBhc3luYyBhZGQob2JqOiBUKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgaWYgKG9iai5pc0Rpc3Bvc2VkKSB7XG4gICAgICBjb25zdCB3YXJuaW5nID0gJ0EgZGlzcG9zZWQgb2JqZWN0IGNhbm5vdCBiZSBhZGRlZC4nO1xuICAgICAgY29uc29sZS53YXJuKHdhcm5pbmcsIG9iaik7XG4gICAgICB0aHJvdyBuZXcgRXJyb3Iod2FybmluZyk7XG4gICAgfVxuXG4gICAgaWYgKHRoaXMuX29iamVjdHMuaGFzKG9iaikpIHtcbiAgICAgIGNvbnN0IHdhcm5pbmcgPSAnVGhpcyBvYmplY3QgYWxyZWFkeSBleGlzdHMgaW4gdGhlIHBvb2wuJztcbiAgICAgIGNvbnNvbGUud2Fybih3YXJuaW5nLCBvYmopO1xuICAgICAgdGhyb3cgbmV3IEVycm9yKHdhcm5pbmcpO1xuICAgIH1cblxuICAgIHRoaXMuX29iamVjdHMuYWRkKG9iaik7XG4gICAgb2JqLmRpc3Bvc2VkLmNvbm5lY3QodGhpcy5fb25JbnN0YW5jZURpc3Bvc2VkLCB0aGlzKTtcblxuICAgIGlmIChQcml2YXRlLmluamVjdGVkUHJvcGVydHkuZ2V0KG9iaikpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBpZiAodGhpcy5fcmVzdG9yZSkge1xuICAgICAgY29uc3QgeyBjb25uZWN0b3IgfSA9IHRoaXMuX3Jlc3RvcmU7XG4gICAgICBjb25zdCBvYmpOYW1lID0gdGhpcy5fcmVzdG9yZS5uYW1lKG9iaik7XG5cbiAgICAgIGlmIChvYmpOYW1lKSB7XG4gICAgICAgIGNvbnN0IG5hbWUgPSBgJHt0aGlzLm5hbWVzcGFjZX06JHtvYmpOYW1lfWA7XG4gICAgICAgIGNvbnN0IGRhdGEgPSB0aGlzLl9yZXN0b3JlLmFyZ3M/LihvYmopO1xuXG4gICAgICAgIFByaXZhdGUubmFtZVByb3BlcnR5LnNldChvYmosIG5hbWUpO1xuICAgICAgICBhd2FpdCBjb25uZWN0b3Iuc2F2ZShuYW1lLCB7IGRhdGEgfSk7XG4gICAgICB9XG4gICAgfVxuXG4gICAgLy8gRW1pdCB0aGUgYWRkZWQgc2lnbmFsLlxuICAgIHRoaXMuX2FkZGVkLmVtaXQob2JqKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgcG9vbC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBEaXNwb3NpbmcgYSBwb29sIGRvZXMgbm90IGFmZmVjdCB0aGUgdW5kZXJseWluZyBkYXRhIGluIHRoZSBkYXRhIGNvbm5lY3RvcixcbiAgICogaXQgc2ltcGx5IGRpc3Bvc2VzIHRoZSBjbGllbnQtc2lkZSBwb29sIHdpdGhvdXQgbWFraW5nIGFueSBjb25uZWN0b3IgY2FsbHMuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLmlzRGlzcG9zZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fY3VycmVudCA9IG51bGw7XG4gICAgdGhpcy5faXNEaXNwb3NlZCA9IHRydWU7XG4gICAgdGhpcy5fb2JqZWN0cy5jbGVhcigpO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogRmluZCB0aGUgZmlyc3Qgb2JqZWN0IGluIHRoZSBwb29sIHRoYXQgc2F0aXNmaWVzIGEgZmlsdGVyIGZ1bmN0aW9uLlxuICAgKlxuICAgKiBAcGFyYW0gLSBmbiBUaGUgZmlsdGVyIGZ1bmN0aW9uIHRvIGNhbGwgb24gZWFjaCBvYmplY3QuXG4gICAqL1xuICBmaW5kKGZuOiAob2JqOiBUKSA9PiBib29sZWFuKTogVCB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3QgdmFsdWVzID0gdGhpcy5fb2JqZWN0cy52YWx1ZXMoKTtcbiAgICBmb3IgKGNvbnN0IHZhbHVlIG9mIHZhbHVlcykge1xuICAgICAgaWYgKGZuKHZhbHVlKSkge1xuICAgICAgICByZXR1cm4gdmFsdWU7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiB1bmRlZmluZWQ7XG4gIH1cblxuICAvKipcbiAgICogSXRlcmF0ZSB0aHJvdWdoIGVhY2ggb2JqZWN0IGluIHRoZSBwb29sLlxuICAgKlxuICAgKiBAcGFyYW0gZm4gLSBUaGUgZnVuY3Rpb24gdG8gY2FsbCBvbiBlYWNoIG9iamVjdC5cbiAgICovXG4gIGZvckVhY2goZm46IChvYmo6IFQpID0+IHZvaWQpOiB2b2lkIHtcbiAgICB0aGlzLl9vYmplY3RzLmZvckVhY2goZm4pO1xuICB9XG5cbiAgLyoqXG4gICAqIEZpbHRlciB0aGUgb2JqZWN0cyBpbiB0aGUgcG9vbCBiYXNlZCBvbiBhIHByZWRpY2F0ZS5cbiAgICpcbiAgICogQHBhcmFtIGZuIC0gVGhlIGZ1bmN0aW9uIGJ5IHdoaWNoIHRvIGZpbHRlci5cbiAgICovXG4gIGZpbHRlcihmbjogKG9iajogVCkgPT4gYm9vbGVhbik6IFRbXSB7XG4gICAgY29uc3QgZmlsdGVyZWQ6IFRbXSA9IFtdO1xuICAgIHRoaXMuZm9yRWFjaChvYmogPT4ge1xuICAgICAgaWYgKGZuKG9iaikpIHtcbiAgICAgICAgZmlsdGVyZWQucHVzaChvYmopO1xuICAgICAgfVxuICAgIH0pO1xuICAgIHJldHVybiBmaWx0ZXJlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbmplY3QgYW4gb2JqZWN0IGludG8gdGhlIHJlc3RvcmFibGUgcG9vbCB3aXRob3V0IHRoZSBwb29sIGhhbmRsaW5nIGl0c1xuICAgKiByZXN0b3JhdGlvbiBsaWZlY3ljbGUuXG4gICAqXG4gICAqIEBwYXJhbSBvYmogLSBUaGUgb2JqZWN0IHRvIGluamVjdCBpbnRvIHRoZSBwb29sLlxuICAgKi9cbiAgaW5qZWN0KG9iajogVCk6IFByb21pc2U8dm9pZD4ge1xuICAgIFByaXZhdGUuaW5qZWN0ZWRQcm9wZXJ0eS5zZXQob2JqLCB0cnVlKTtcbiAgICByZXR1cm4gdGhpcy5hZGQob2JqKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDaGVjayBpZiB0aGlzIHBvb2wgaGFzIHRoZSBzcGVjaWZpZWQgb2JqZWN0LlxuICAgKlxuICAgKiBAcGFyYW0gb2JqIC0gVGhlIG9iamVjdCB3aG9zZSBleGlzdGVuY2UgaXMgYmVpbmcgY2hlY2tlZC5cbiAgICovXG4gIGhhcyhvYmo6IFQpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fb2JqZWN0cy5oYXMob2JqKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXN0b3JlIHRoZSBvYmplY3RzIGluIHRoaXMgcG9vbCdzIG5hbWVzcGFjZS5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgY29uZmlndXJhdGlvbiBvcHRpb25zIHRoYXQgZGVzY3JpYmUgcmVzdG9yYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gcmVzdG9yYXRpb24gaGFzIGNvbXBsZXRlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGZ1bmN0aW9uIHNob3VsZCBhbG1vc3QgbmV2ZXIgYmUgaW52b2tlZCBieSBjbGllbnQgY29kZS4gSXRzIHByaW1hcnlcbiAgICogdXNlIGNhc2UgaXMgdG8gYmUgaW52b2tlZCBieSBhIGxheW91dCByZXN0b3JlciBwbHVnaW4gdGhhdCBoYW5kbGVzXG4gICAqIG11bHRpcGxlIHJlc3RvcmFibGUgcG9vbHMgYW5kLCB3aGVuIHJlYWR5LCBhc2tzIHRoZW0gZWFjaCB0byByZXN0b3JlIHRoZWlyXG4gICAqIHJlc3BlY3RpdmUgb2JqZWN0cy5cbiAgICovXG4gIGFzeW5jIHJlc3RvcmUob3B0aW9uczogSVJlc3RvcmFibGUuSU9wdGlvbnM8VD4pOiBQcm9taXNlPGFueT4ge1xuICAgIGlmICh0aGlzLl9oYXNSZXN0b3JlZCkge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKCdUaGlzIHBvb2wgaGFzIGFscmVhZHkgYmVlbiByZXN0b3JlZC4nKTtcbiAgICB9XG5cbiAgICB0aGlzLl9oYXNSZXN0b3JlZCA9IHRydWU7XG5cbiAgICBjb25zdCB7IGNvbW1hbmQsIGNvbm5lY3RvciwgcmVnaXN0cnksIHdoZW4gfSA9IG9wdGlvbnM7XG4gICAgY29uc3QgbmFtZXNwYWNlID0gdGhpcy5uYW1lc3BhY2U7XG4gICAgY29uc3QgcHJvbWlzZXMgPSB3aGVuXG4gICAgICA/IFtjb25uZWN0b3IubGlzdChuYW1lc3BhY2UpXS5jb25jYXQod2hlbilcbiAgICAgIDogW2Nvbm5lY3Rvci5saXN0KG5hbWVzcGFjZSldO1xuXG4gICAgdGhpcy5fcmVzdG9yZSA9IG9wdGlvbnM7XG5cbiAgICBjb25zdCBbc2F2ZWRdID0gYXdhaXQgUHJvbWlzZS5hbGwocHJvbWlzZXMpO1xuICAgIGNvbnN0IHZhbHVlcyA9IGF3YWl0IFByb21pc2UuYWxsKFxuICAgICAgc2F2ZWQuaWRzLm1hcChhc3luYyAoaWQsIGluZGV4KSA9PiB7XG4gICAgICAgIGNvbnN0IHZhbHVlID0gc2F2ZWQudmFsdWVzW2luZGV4XTtcbiAgICAgICAgY29uc3QgYXJncyA9IHZhbHVlICYmICh2YWx1ZSBhcyBhbnkpLmRhdGE7XG5cbiAgICAgICAgaWYgKGFyZ3MgPT09IHVuZGVmaW5lZCkge1xuICAgICAgICAgIHJldHVybiBjb25uZWN0b3IucmVtb3ZlKGlkKTtcbiAgICAgICAgfVxuXG4gICAgICAgIC8vIEV4ZWN1dGUgdGhlIGNvbW1hbmQgYW5kIGlmIGl0IGZhaWxzLCBkZWxldGUgdGhlIHN0YXRlIHJlc3RvcmUgZGF0YS5cbiAgICAgICAgcmV0dXJuIHJlZ2lzdHJ5XG4gICAgICAgICAgLmV4ZWN1dGUoY29tbWFuZCwgYXJncylcbiAgICAgICAgICAuY2F0Y2goKCkgPT4gY29ubmVjdG9yLnJlbW92ZShpZCkpO1xuICAgICAgfSlcbiAgICApO1xuICAgIHRoaXMuX3Jlc3RvcmVkLnJlc29sdmUoKTtcbiAgICByZXR1cm4gdmFsdWVzO1xuICB9XG5cbiAgLyoqXG4gICAqIFNhdmUgdGhlIHJlc3RvcmUgZGF0YSBmb3IgYSBnaXZlbiBvYmplY3QuXG4gICAqXG4gICAqIEBwYXJhbSBvYmogLSBUaGUgb2JqZWN0IGJlaW5nIHNhdmVkLlxuICAgKi9cbiAgYXN5bmMgc2F2ZShvYmo6IFQpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCBpbmplY3RlZCA9IFByaXZhdGUuaW5qZWN0ZWRQcm9wZXJ0eS5nZXQob2JqKTtcblxuICAgIGlmICghdGhpcy5fcmVzdG9yZSB8fCAhdGhpcy5oYXMob2JqKSB8fCBpbmplY3RlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIGNvbnN0IHsgY29ubmVjdG9yIH0gPSB0aGlzLl9yZXN0b3JlO1xuICAgIGNvbnN0IG9iak5hbWUgPSB0aGlzLl9yZXN0b3JlLm5hbWUob2JqKTtcbiAgICBjb25zdCBvbGROYW1lID0gUHJpdmF0ZS5uYW1lUHJvcGVydHkuZ2V0KG9iaik7XG4gICAgY29uc3QgbmV3TmFtZSA9IG9iak5hbWUgPyBgJHt0aGlzLm5hbWVzcGFjZX06JHtvYmpOYW1lfWAgOiAnJztcblxuICAgIGlmIChvbGROYW1lICYmIG9sZE5hbWUgIT09IG5ld05hbWUpIHtcbiAgICAgIGF3YWl0IGNvbm5lY3Rvci5yZW1vdmUob2xkTmFtZSk7XG4gICAgfVxuXG4gICAgLy8gU2V0IHRoZSBuYW1lIHByb3BlcnR5IGlycmVzcGVjdGl2ZSBvZiB3aGV0aGVyIHRoZSBuZXcgbmFtZSBpcyBudWxsLlxuICAgIFByaXZhdGUubmFtZVByb3BlcnR5LnNldChvYmosIG5ld05hbWUpO1xuXG4gICAgaWYgKG5ld05hbWUpIHtcbiAgICAgIGNvbnN0IGRhdGEgPSB0aGlzLl9yZXN0b3JlLmFyZ3M/LihvYmopO1xuICAgICAgYXdhaXQgY29ubmVjdG9yLnNhdmUobmV3TmFtZSwgeyBkYXRhIH0pO1xuICAgIH1cblxuICAgIGlmIChvbGROYW1lICE9PSBuZXdOYW1lKSB7XG4gICAgICB0aGlzLl91cGRhdGVkLmVtaXQob2JqKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ2xlYW4gdXAgYWZ0ZXIgZGlzcG9zZWQgb2JqZWN0cy5cbiAgICovXG4gIHByaXZhdGUgX29uSW5zdGFuY2VEaXNwb3NlZChvYmo6IFQpOiB2b2lkIHtcbiAgICB0aGlzLl9vYmplY3RzLmRlbGV0ZShvYmopO1xuXG4gICAgaWYgKG9iaiA9PT0gdGhpcy5fY3VycmVudCkge1xuICAgICAgdGhpcy5fY3VycmVudCA9IG51bGw7XG4gICAgICB0aGlzLl9jdXJyZW50Q2hhbmdlZC5lbWl0KHRoaXMuX2N1cnJlbnQpO1xuICAgIH1cblxuICAgIGlmIChQcml2YXRlLmluamVjdGVkUHJvcGVydHkuZ2V0KG9iaikpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBpZiAoIXRoaXMuX3Jlc3RvcmUpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICBjb25zdCB7IGNvbm5lY3RvciB9ID0gdGhpcy5fcmVzdG9yZTtcbiAgICBjb25zdCBuYW1lID0gUHJpdmF0ZS5uYW1lUHJvcGVydHkuZ2V0KG9iaik7XG5cbiAgICBpZiAobmFtZSkge1xuICAgICAgdm9pZCBjb25uZWN0b3IucmVtb3ZlKG5hbWUpO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2FkZGVkID0gbmV3IFNpZ25hbDx0aGlzLCBUPih0aGlzKTtcbiAgcHJpdmF0ZSBfY3VycmVudDogVCB8IG51bGwgPSBudWxsO1xuICBwcml2YXRlIF9jdXJyZW50Q2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgVCB8IG51bGw+KHRoaXMpO1xuICBwcml2YXRlIF9oYXNSZXN0b3JlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG4gIHByaXZhdGUgX29iamVjdHMgPSBuZXcgU2V0PFQ+KCk7XG4gIHByaXZhdGUgX3Jlc3RvcmU6IElSZXN0b3JhYmxlLklPcHRpb25zPFQ+IHwgbnVsbCA9IG51bGw7XG4gIHByaXZhdGUgX3Jlc3RvcmVkID0gbmV3IFByb21pc2VEZWxlZ2F0ZTx2b2lkPigpO1xuICBwcml2YXRlIF91cGRhdGVkID0gbmV3IFNpZ25hbDx0aGlzLCBUPih0aGlzKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYFJlc3RvcmFibGVQb29sYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFJlc3RvcmFibGVQb29sIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIHRoZSByZXN0b3JhYmxlIHBvb2wuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBBIG5hbWVzcGFjZSBkZXNpZ25hdGluZyBvYmplY3RzIGZyb20gdGhpcyBwb29sLlxuICAgICAqL1xuICAgIG5hbWVzcGFjZTogc3RyaW5nO1xuICB9XG59XG5cbi8qXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBbiBhdHRhY2hlZCBwcm9wZXJ0eSB0byBpbmRpY2F0ZSB3aGV0aGVyIGFuIG9iamVjdCBoYXMgYmVlbiBpbmplY3RlZC5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBpbmplY3RlZFByb3BlcnR5ID0gbmV3IEF0dGFjaGVkUHJvcGVydHk8XG4gICAgSU9ic2VydmFibGVEaXNwb3NhYmxlLFxuICAgIGJvb2xlYW5cbiAgPih7XG4gICAgbmFtZTogJ2luamVjdGVkJyxcbiAgICBjcmVhdGU6ICgpID0+IGZhbHNlXG4gIH0pO1xuXG4gIC8qKlxuICAgKiBBbiBhdHRhY2hlZCBwcm9wZXJ0eSBmb3IgYW4gb2JqZWN0J3MgSUQuXG4gICAqL1xuICBleHBvcnQgY29uc3QgbmFtZVByb3BlcnR5ID0gbmV3IEF0dGFjaGVkUHJvcGVydHk8XG4gICAgSU9ic2VydmFibGVEaXNwb3NhYmxlLFxuICAgIHN0cmluZ1xuICA+KHtcbiAgICBuYW1lOiAnbmFtZScsXG4gICAgY3JlYXRlOiAoKSA9PiAnJ1xuICB9KTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSVNpZ25hbCwgU2lnbmFsIH0gZnJvbSAnQGx1bWluby9zaWduYWxpbmcnO1xuaW1wb3J0IHsgSURhdGFDb25uZWN0b3IgfSBmcm9tICcuL2ludGVyZmFjZXMnO1xuaW1wb3J0IHsgSVN0YXRlREIgfSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgY29uY3JldGUgaW1wbGVtZW50YXRpb24gb2YgYSBzdGF0ZSBkYXRhYmFzZS5cbiAqL1xuZXhwb3J0IGNsYXNzIFN0YXRlREI8XG4gIFQgZXh0ZW5kcyBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUgPSBSZWFkb25seVBhcnRpYWxKU09OVmFsdWVcbj4gaW1wbGVtZW50cyBJU3RhdGVEQjxUPlxue1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHN0YXRlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gb3B0aW9ucyAtIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgc3RhdGUgZGF0YWJhc2UuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBTdGF0ZURCLklPcHRpb25zPFQ+ID0ge30pIHtcbiAgICBjb25zdCB7IGNvbm5lY3RvciwgdHJhbnNmb3JtIH0gPSBvcHRpb25zO1xuXG4gICAgdGhpcy5fY29ubmVjdG9yID0gY29ubmVjdG9yIHx8IG5ldyBTdGF0ZURCLkNvbm5lY3RvcigpO1xuICAgIGlmICghdHJhbnNmb3JtKSB7XG4gICAgICB0aGlzLl9yZWFkeSA9IFByb21pc2UucmVzb2x2ZSh1bmRlZmluZWQpO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9yZWFkeSA9IHRyYW5zZm9ybS50aGVuKHRyYW5zZm9ybWF0aW9uID0+IHtcbiAgICAgICAgY29uc3QgeyBjb250ZW50cywgdHlwZSB9ID0gdHJhbnNmb3JtYXRpb247XG5cbiAgICAgICAgc3dpdGNoICh0eXBlKSB7XG4gICAgICAgICAgY2FzZSAnY2FuY2VsJzpcbiAgICAgICAgICAgIHJldHVybjtcbiAgICAgICAgICBjYXNlICdjbGVhcic6XG4gICAgICAgICAgICByZXR1cm4gdGhpcy5fY2xlYXIoKTtcbiAgICAgICAgICBjYXNlICdtZXJnZSc6XG4gICAgICAgICAgICByZXR1cm4gdGhpcy5fbWVyZ2UoY29udGVudHMgfHwge30pO1xuICAgICAgICAgIGNhc2UgJ292ZXJ3cml0ZSc6XG4gICAgICAgICAgICByZXR1cm4gdGhpcy5fb3ZlcndyaXRlKGNvbnRlbnRzIHx8IHt9KTtcbiAgICAgICAgICBkZWZhdWx0OlxuICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICB9KTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQSBzaWduYWwgdGhhdCBlbWl0cyB0aGUgY2hhbmdlIHR5cGUgYW55IHRpbWUgYSB2YWx1ZSBjaGFuZ2VzLlxuICAgKi9cbiAgZ2V0IGNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBTdGF0ZURCLkNoYW5nZT4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIENsZWFyIHRoZSBlbnRpcmUgZGF0YWJhc2UuXG4gICAqL1xuICBhc3luYyBjbGVhcigpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBhd2FpdCB0aGlzLl9yZWFkeTtcbiAgICBhd2FpdCB0aGlzLl9jbGVhcigpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHJpZXZlIGEgc2F2ZWQgYnVuZGxlIGZyb20gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gaWQgLSBUaGUgaWRlbnRpZmllciB1c2VkIHRvIHJldHJpZXZlIGEgZGF0YSBidW5kbGUuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGJlYXJzIGEgZGF0YSBwYXlsb2FkIGlmIGF2YWlsYWJsZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgYGlkYCB2YWx1ZXMgb2Ygc3RvcmVkIGl0ZW1zIGluIHRoZSBzdGF0ZSBkYXRhYmFzZSBhcmUgZm9ybWF0dGVkOlxuICAgKiBgJ25hbWVzcGFjZTppZGVudGlmaWVyJ2AsIHdoaWNoIGlzIHRoZSBzYW1lIGNvbnZlbnRpb24gdGhhdCBjb21tYW5kXG4gICAqIGlkZW50aWZpZXJzIGluIEp1cHl0ZXJMYWIgdXNlIGFzIHdlbGwuIFdoaWxlIHRoaXMgaXMgbm90IGEgdGVjaG5pY2FsXG4gICAqIHJlcXVpcmVtZW50IGZvciBgZmV0Y2goKWAsIGByZW1vdmUoKWAsIGFuZCBgc2F2ZSgpYCwgaXQgKmlzKiBuZWNlc3NhcnkgZm9yXG4gICAqIHVzaW5nIHRoZSBgbGlzdChuYW1lc3BhY2U6IHN0cmluZylgIG1ldGhvZC5cbiAgICpcbiAgICogVGhlIHByb21pc2UgcmV0dXJuZWQgYnkgdGhpcyBtZXRob2QgbWF5IGJlIHJlamVjdGVkIGlmIGFuIGVycm9yIG9jY3VycyBpblxuICAgKiByZXRyaWV2aW5nIHRoZSBkYXRhLiBOb24tZXhpc3RlbmNlIG9mIGFuIGBpZGAgd2lsbCBzdWNjZWVkIHdpdGggdGhlIGB2YWx1ZWBcbiAgICogYHVuZGVmaW5lZGAuXG4gICAqL1xuICBhc3luYyBmZXRjaChpZDogc3RyaW5nKTogUHJvbWlzZTxUIHwgdW5kZWZpbmVkPiB7XG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG4gICAgcmV0dXJuIHRoaXMuX2ZldGNoKGlkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXRyaWV2ZSBhbGwgdGhlIHNhdmVkIGJ1bmRsZXMgZm9yIGEgbmFtZXNwYWNlLlxuICAgKlxuICAgKiBAcGFyYW0gZmlsdGVyIC0gVGhlIG5hbWVzcGFjZSBwcmVmaXggdG8gcmV0cmlldmUuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGJlYXJzIGEgY29sbGVjdGlvbiBvZiBwYXlsb2FkcyBmb3IgYSBuYW1lc3BhY2UuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogTmFtZXNwYWNlcyBhcmUgZW50aXJlbHkgY29udmVudGlvbmFsIGVudGl0aWVzLiBUaGUgYGlkYCB2YWx1ZXMgb2Ygc3RvcmVkXG4gICAqIGl0ZW1zIGluIHRoZSBzdGF0ZSBkYXRhYmFzZSBhcmUgZm9ybWF0dGVkOiBgJ25hbWVzcGFjZTppZGVudGlmaWVyJ2AsIHdoaWNoXG4gICAqIGlzIHRoZSBzYW1lIGNvbnZlbnRpb24gdGhhdCBjb21tYW5kIGlkZW50aWZpZXJzIGluIEp1cHl0ZXJMYWIgdXNlIGFzIHdlbGwuXG4gICAqXG4gICAqIElmIHRoZXJlIGFyZSBhbnkgZXJyb3JzIGluIHJldHJpZXZpbmcgdGhlIGRhdGEsIHRoZXkgd2lsbCBiZSBsb2dnZWQgdG8gdGhlXG4gICAqIGNvbnNvbGUgaW4gb3JkZXIgdG8gb3B0aW1pc3RpY2FsbHkgcmV0dXJuIGFueSBleHRhbnQgZGF0YSB3aXRob3V0IGZhaWxpbmcuXG4gICAqIFRoaXMgcHJvbWlzZSB3aWxsIGFsd2F5cyBzdWNjZWVkLlxuICAgKi9cbiAgYXN5bmMgbGlzdChuYW1lc3BhY2U6IHN0cmluZyk6IFByb21pc2U8eyBpZHM6IHN0cmluZ1tdOyB2YWx1ZXM6IFRbXSB9PiB7XG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG4gICAgcmV0dXJuIHRoaXMuX2xpc3QobmFtZXNwYWNlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSB2YWx1ZSBmcm9tIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIGlkIC0gVGhlIGlkZW50aWZpZXIgZm9yIHRoZSBkYXRhIGJlaW5nIHJlbW92ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGlzIHJlamVjdGVkIGlmIHJlbW92ZSBmYWlscyBhbmQgc3VjY2VlZHMgb3RoZXJ3aXNlLlxuICAgKi9cbiAgYXN5bmMgcmVtb3ZlKGlkOiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBhd2FpdCB0aGlzLl9yZWFkeTtcbiAgICBhd2FpdCB0aGlzLl9yZW1vdmUoaWQpO1xuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7IGlkLCB0eXBlOiAncmVtb3ZlJyB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTYXZlIGEgdmFsdWUgaW4gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gaWQgLSBUaGUgaWRlbnRpZmllciBmb3IgdGhlIGRhdGEgYmVpbmcgc2F2ZWQuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSBkYXRhIGJlaW5nIHNhdmVkLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCBpcyByZWplY3RlZCBpZiBzYXZpbmcgZmFpbHMgYW5kIHN1Y2NlZWRzIG90aGVyd2lzZS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgYGlkYCB2YWx1ZXMgb2Ygc3RvcmVkIGl0ZW1zIGluIHRoZSBzdGF0ZSBkYXRhYmFzZSBhcmUgZm9ybWF0dGVkOlxuICAgKiBgJ25hbWVzcGFjZTppZGVudGlmaWVyJ2AsIHdoaWNoIGlzIHRoZSBzYW1lIGNvbnZlbnRpb24gdGhhdCBjb21tYW5kXG4gICAqIGlkZW50aWZpZXJzIGluIEp1cHl0ZXJMYWIgdXNlIGFzIHdlbGwuIFdoaWxlIHRoaXMgaXMgbm90IGEgdGVjaG5pY2FsXG4gICAqIHJlcXVpcmVtZW50IGZvciBgZmV0Y2goKWAsIGByZW1vdmUoKWAsIGFuZCBgc2F2ZSgpYCwgaXQgKmlzKiBuZWNlc3NhcnkgZm9yXG4gICAqIHVzaW5nIHRoZSBgbGlzdChuYW1lc3BhY2U6IHN0cmluZylgIG1ldGhvZC5cbiAgICovXG4gIGFzeW5jIHNhdmUoaWQ6IHN0cmluZywgdmFsdWU6IFQpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBhd2FpdCB0aGlzLl9yZWFkeTtcbiAgICBhd2FpdCB0aGlzLl9zYXZlKGlkLCB2YWx1ZSk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHsgaWQsIHR5cGU6ICdzYXZlJyB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm4gYSBzZXJpYWxpemVkIGNvcHkgb2YgdGhlIHN0YXRlIGRhdGFiYXNlJ3MgZW50aXJlIGNvbnRlbnRzLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aXRoIHRoZSBkYXRhYmFzZSBjb250ZW50cyBhcyBKU09OLlxuICAgKi9cbiAgYXN5bmMgdG9KU09OKCk6IFByb21pc2U8eyByZWFkb25seSBbaWQ6IHN0cmluZ106IFQgfT4ge1xuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuXG4gICAgY29uc3QgeyBpZHMsIHZhbHVlcyB9ID0gYXdhaXQgdGhpcy5fbGlzdCgpO1xuXG4gICAgcmV0dXJuIHZhbHVlcy5yZWR1Y2UoXG4gICAgICAoYWNjLCB2YWwsIGlkeCkgPT4ge1xuICAgICAgICBhY2NbaWRzW2lkeF1dID0gdmFsO1xuICAgICAgICByZXR1cm4gYWNjO1xuICAgICAgfSxcbiAgICAgIHt9IGFzIHsgW2lkOiBzdHJpbmddOiBUIH1cbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIENsZWFyIHRoZSBlbnRpcmUgZGF0YWJhc2UuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9jbGVhcigpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBhd2FpdCBQcm9taXNlLmFsbCgoYXdhaXQgdGhpcy5fbGlzdCgpKS5pZHMubWFwKGlkID0+IHRoaXMuX3JlbW92ZShpZCkpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGZXRjaCBhIHZhbHVlIGZyb20gdGhlIGRhdGFiYXNlLlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfZmV0Y2goaWQ6IHN0cmluZyk6IFByb21pc2U8VCB8IHVuZGVmaW5lZD4ge1xuICAgIGNvbnN0IHZhbHVlID0gYXdhaXQgdGhpcy5fY29ubmVjdG9yLmZldGNoKGlkKTtcblxuICAgIGlmICh2YWx1ZSkge1xuICAgICAgcmV0dXJuIChKU09OLnBhcnNlKHZhbHVlKSBhcyBQcml2YXRlLkVudmVsb3BlKS52IGFzIFQ7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIEZldGNoIGEgbGlzdCBmcm9tIHRoZSBkYXRhYmFzZS5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX2xpc3QobmFtZXNwYWNlID0gJycpOiBQcm9taXNlPHsgaWRzOiBzdHJpbmdbXTsgdmFsdWVzOiBUW10gfT4ge1xuICAgIGNvbnN0IHsgaWRzLCB2YWx1ZXMgfSA9IGF3YWl0IHRoaXMuX2Nvbm5lY3Rvci5saXN0KG5hbWVzcGFjZSk7XG5cbiAgICByZXR1cm4ge1xuICAgICAgaWRzLFxuICAgICAgdmFsdWVzOiB2YWx1ZXMubWFwKHZhbCA9PiAoSlNPTi5wYXJzZSh2YWwpIGFzIFByaXZhdGUuRW52ZWxvcGUpLnYgYXMgVClcbiAgICB9O1xuICB9XG5cbiAgLyoqXG4gICAqIE1lcmdlIGRhdGEgaW50byB0aGUgc3RhdGUgZGF0YWJhc2UuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9tZXJnZShjb250ZW50czogU3RhdGVEQi5Db250ZW50PFQ+KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgUHJvbWlzZS5hbGwoXG4gICAgICBPYmplY3Qua2V5cyhjb250ZW50cykubWFwKFxuICAgICAgICBrZXkgPT4gY29udGVudHNba2V5XSAmJiB0aGlzLl9zYXZlKGtleSwgY29udGVudHNba2V5XSEpXG4gICAgICApXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBPdmVyd3JpdGUgdGhlIGVudGlyZSBkYXRhYmFzZSB3aXRoIG5ldyBjb250ZW50cy5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX292ZXJ3cml0ZShjb250ZW50czogU3RhdGVEQi5Db250ZW50PFQ+KTogUHJvbWlzZTx2b2lkPiB7XG4gICAgYXdhaXQgdGhpcy5fY2xlYXIoKTtcbiAgICBhd2FpdCB0aGlzLl9tZXJnZShjb250ZW50cyk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGEga2V5IGluIHRoZSBkYXRhYmFzZS5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3JlbW92ZShpZDogc3RyaW5nKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX2Nvbm5lY3Rvci5yZW1vdmUoaWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNhdmUgYSBrZXkgYW5kIGl0cyB2YWx1ZSBpbiB0aGUgZGF0YWJhc2UuXG4gICAqL1xuICBwcml2YXRlIGFzeW5jIF9zYXZlKGlkOiBzdHJpbmcsIHZhbHVlOiBUKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMuX2Nvbm5lY3Rvci5zYXZlKGlkLCBKU09OLnN0cmluZ2lmeSh7IHY6IHZhbHVlIH0pKTtcbiAgfVxuXG4gIHByaXZhdGUgX2NoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIFN0YXRlREIuQ2hhbmdlPih0aGlzKTtcbiAgcHJpdmF0ZSBfY29ubmVjdG9yOiBJRGF0YUNvbm5lY3RvcjxzdHJpbmc+O1xuICBwcml2YXRlIF9yZWFkeTogUHJvbWlzZTx2b2lkPjtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgU3RhdGVEQiBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFN0YXRlREIge1xuICAvKipcbiAgICogQSBzdGF0ZSBkYXRhYmFzZSBjaGFuZ2UuXG4gICAqL1xuICBleHBvcnQgdHlwZSBDaGFuZ2UgPSB7XG4gICAgLyoqXG4gICAgICogVGhlIGtleSBvZiB0aGUgZGF0YWJhc2UgaXRlbSB0aGF0IHdhcyBjaGFuZ2VkLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoaXMgZmllbGQgaXMgc2V0IHRvIGBudWxsYCBmb3IgZ2xvYmFsIGNoYW5nZXMgKGkuZS4gYGNsZWFyYCkuXG4gICAgICovXG4gICAgaWQ6IHN0cmluZyB8IG51bGw7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdHlwZSBvZiBjaGFuZ2UuXG4gICAgICovXG4gICAgdHlwZTogJ2NsZWFyJyB8ICdyZW1vdmUnIHwgJ3NhdmUnO1xuICB9O1xuXG4gIC8qKlxuICAgKiBBIGRhdGEgdHJhbnNmb3JtYXRpb24gdGhhdCBjYW4gYmUgYXBwbGllZCB0byBhIHN0YXRlIGRhdGFiYXNlLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgRGF0YVRyYW5zZm9ybTxcbiAgICBUIGV4dGVuZHMgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlID0gUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlXG4gID4gPSB7XG4gICAgLypcbiAgICAgKiBUaGUgY2hhbmdlIG9wZXJhdGlvbiBiZWluZyBhcHBsaWVkLlxuICAgICAqL1xuICAgIHR5cGU6ICdjYW5jZWwnIHwgJ2NsZWFyJyB8ICdtZXJnZScgfCAnb3ZlcndyaXRlJztcblxuICAgIC8qKlxuICAgICAqIFRoZSBjb250ZW50cyBvZiB0aGUgY2hhbmdlIG9wZXJhdGlvbi5cbiAgICAgKi9cbiAgICBjb250ZW50czogQ29udGVudDxUPiB8IG51bGw7XG4gIH07XG5cbiAgLyoqXG4gICAqIERhdGFiYXNlIGNvbnRlbnQgbWFwXG4gICAqL1xuICBleHBvcnQgdHlwZSBDb250ZW50PFQ+ID0geyBbaWQ6IHN0cmluZ106IFQgfCB1bmRlZmluZWQgfTtcblxuICAvKipcbiAgICogVGhlIGluc3RhbnRpYXRpb24gb3B0aW9ucyBmb3IgYSBzdGF0ZSBkYXRhYmFzZS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnM8XG4gICAgVCBleHRlbmRzIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSA9IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZVxuICA+IHtcbiAgICAvKipcbiAgICAgKiBPcHRpb25hbCBzdHJpbmcga2V5L3ZhbHVlIGNvbm5lY3Rvci4gRGVmYXVsdHMgdG8gaW4tbWVtb3J5IGNvbm5lY3Rvci5cbiAgICAgKi9cbiAgICBjb25uZWN0b3I/OiBJRGF0YUNvbm5lY3RvcjxzdHJpbmc+O1xuXG4gICAgLyoqXG4gICAgICogQW4gb3B0aW9uYWwgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdpdGggYSBkYXRhIHRyYW5zZm9ybWF0aW9uIHRoYXQgaXNcbiAgICAgKiBhcHBsaWVkIHRvIHRoZSBkYXRhYmFzZSBjb250ZW50cyBiZWZvcmUgdGhlIGRhdGFiYXNlIGJlZ2lucyByZXNvbHZpbmdcbiAgICAgKiBjbGllbnQgcmVxdWVzdHMuXG4gICAgICovXG4gICAgdHJhbnNmb3JtPzogUHJvbWlzZTxEYXRhVHJhbnNmb3JtPFQ+PjtcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiBpbi1tZW1vcnkgc3RyaW5nIGtleS92YWx1ZSBkYXRhIGNvbm5lY3Rvci5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBDb25uZWN0b3IgaW1wbGVtZW50cyBJRGF0YUNvbm5lY3RvcjxzdHJpbmc+IHtcbiAgICAvKipcbiAgICAgKiBSZXRyaWV2ZSBhbiBpdGVtIGZyb20gdGhlIGRhdGEgY29ubmVjdG9yLlxuICAgICAqL1xuICAgIGFzeW5jIGZldGNoKGlkOiBzdHJpbmcpOiBQcm9taXNlPHN0cmluZz4ge1xuICAgICAgcmV0dXJuIHRoaXMuX3N0b3JhZ2VbaWRdO1xuICAgIH1cblxuICAgIC8qKlxuICAgICAqIFJldHJpZXZlIHRoZSBsaXN0IG9mIGl0ZW1zIGF2YWlsYWJsZSBmcm9tIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICAgKlxuICAgICAqIEBwYXJhbSBuYW1lc3BhY2UgLSBJZiBub3QgZW1wdHksIG9ubHkga2V5cyB3aG9zZSBmaXJzdCB0b2tlbiBiZWZvcmUgYDpgXG4gICAgICogZXhhY3RseSBtYXRjaCBgbmFtZXNwYWNlYCB3aWxsIGJlIHJldHVybmVkLCBlLmcuIGBmb29gIGluIGBmb286YmFyYC5cbiAgICAgKi9cbiAgICBhc3luYyBsaXN0KG5hbWVzcGFjZSA9ICcnKTogUHJvbWlzZTx7IGlkczogc3RyaW5nW107IHZhbHVlczogc3RyaW5nW10gfT4ge1xuICAgICAgcmV0dXJuIE9iamVjdC5rZXlzKHRoaXMuX3N0b3JhZ2UpLnJlZHVjZShcbiAgICAgICAgKGFjYywgdmFsKSA9PiB7XG4gICAgICAgICAgaWYgKG5hbWVzcGFjZSA9PT0gJycgPyB0cnVlIDogbmFtZXNwYWNlID09PSB2YWwuc3BsaXQoJzonKVswXSkge1xuICAgICAgICAgICAgYWNjLmlkcy5wdXNoKHZhbCk7XG4gICAgICAgICAgICBhY2MudmFsdWVzLnB1c2godGhpcy5fc3RvcmFnZVt2YWxdKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgcmV0dXJuIGFjYztcbiAgICAgICAgfSxcbiAgICAgICAgeyBpZHM6IFtdIGFzIHN0cmluZ1tdLCB2YWx1ZXM6IFtdIGFzIHN0cmluZ1tdIH1cbiAgICAgICk7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogUmVtb3ZlIGEgdmFsdWUgdXNpbmcgdGhlIGRhdGEgY29ubmVjdG9yLlxuICAgICAqL1xuICAgIGFzeW5jIHJlbW92ZShpZDogc3RyaW5nKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgICBkZWxldGUgdGhpcy5fc3RvcmFnZVtpZF07XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogU2F2ZSBhIHZhbHVlIHVzaW5nIHRoZSBkYXRhIGNvbm5lY3Rvci5cbiAgICAgKi9cbiAgICBhc3luYyBzYXZlKGlkOiBzdHJpbmcsIHZhbHVlOiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAgIHRoaXMuX3N0b3JhZ2VbaWRdID0gdmFsdWU7XG4gICAgfVxuXG4gICAgcHJpdmF0ZSBfc3RvcmFnZTogeyBba2V5OiBzdHJpbmddOiBzdHJpbmcgfSA9IHt9O1xuICB9XG59XG5cbi8qXG4gKiBBIG5hbWVzcGFjZSBmb3IgcHJpdmF0ZSBtb2R1bGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogQW4gZW52ZWxvcGUgYXJvdW5kIGEgSlNPTiB2YWx1ZSBzdG9yZWQgaW4gdGhlIHN0YXRlIGRhdGFiYXNlLlxuICAgKi9cbiAgZXhwb3J0IHR5cGUgRW52ZWxvcGUgPSB7IHJlYWRvbmx5IHY6IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSB9O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUsIFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSURhdGFDb25uZWN0b3IgfSBmcm9tICcuL2ludGVyZmFjZXMnO1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHN0YXRlIGRhdGFiYXNlIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSVN0YXRlREIgPSBuZXcgVG9rZW48SVN0YXRlREI+KFxuICAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzOklTdGF0ZURCJyxcbiAgYEEgc2VydmljZSBmb3IgdGhlIEp1cHl0ZXJMYWIgc3RhdGUgZGF0YWJhc2UuXG4gIFVzZSB0aGlzIGlmIHlvdSB3YW50IHRvIHN0b3JlIGRhdGEgdGhhdCB3aWxsIHBlcnNpc3QgYWNyb3NzIHBhZ2UgbG9hZHMuXG4gIFNlZSBcInN0YXRlIGRhdGFiYXNlXCIgZm9yIG1vcmUgaW5mb3JtYXRpb24uYFxuKTtcblxuLyoqXG4gKiBUaGUgZGVzY3JpcHRpb24gb2YgYSBzdGF0ZSBkYXRhYmFzZS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJU3RhdGVEQjxcbiAgVCBleHRlbmRzIFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSA9IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZVxuPiBleHRlbmRzIElEYXRhQ29ubmVjdG9yPFQ+IHtcbiAgLyoqXG4gICAqIFJldHVybiBhIHNlcmlhbGl6ZWQgY29weSBvZiB0aGUgc3RhdGUgZGF0YWJhc2UncyBlbnRpcmUgY29udGVudHMuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IGJlYXJzIHRoZSBkYXRhYmFzZSBjb250ZW50cyBhcyBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IFByb21pc2U8eyBbaWQ6IHN0cmluZ106IFQgfT47XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=