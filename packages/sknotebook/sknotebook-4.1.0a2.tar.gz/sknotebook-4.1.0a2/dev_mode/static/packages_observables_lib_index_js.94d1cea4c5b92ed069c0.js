"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_observables_lib_index_js"],{

/***/ "../packages/observables/lib/index.js":
/*!********************************************!*\
  !*** ../packages/observables/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ModelDB": () => (/* reexport safe */ _modeldb__WEBPACK_IMPORTED_MODULE_0__.ModelDB),
/* harmony export */   "ObservableJSON": () => (/* reexport safe */ _observablejson__WEBPACK_IMPORTED_MODULE_1__.ObservableJSON),
/* harmony export */   "ObservableList": () => (/* reexport safe */ _observablelist__WEBPACK_IMPORTED_MODULE_2__.ObservableList),
/* harmony export */   "ObservableMap": () => (/* reexport safe */ _observablemap__WEBPACK_IMPORTED_MODULE_3__.ObservableMap),
/* harmony export */   "ObservableString": () => (/* reexport safe */ _observablestring__WEBPACK_IMPORTED_MODULE_4__.ObservableString),
/* harmony export */   "ObservableUndoableList": () => (/* reexport safe */ _undoablelist__WEBPACK_IMPORTED_MODULE_5__.ObservableUndoableList),
/* harmony export */   "ObservableValue": () => (/* reexport safe */ _modeldb__WEBPACK_IMPORTED_MODULE_0__.ObservableValue)
/* harmony export */ });
/* harmony import */ var _modeldb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./modeldb */ "../packages/observables/lib/modeldb.js");
/* harmony import */ var _observablejson__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./observablejson */ "../packages/observables/lib/observablejson.js");
/* harmony import */ var _observablelist__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./observablelist */ "../packages/observables/lib/observablelist.js");
/* harmony import */ var _observablemap__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./observablemap */ "../packages/observables/lib/observablemap.js");
/* harmony import */ var _observablestring__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./observablestring */ "../packages/observables/lib/observablestring.js");
/* harmony import */ var _undoablelist__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./undoablelist */ "../packages/observables/lib/undoablelist.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module observables
 */








/***/ }),

/***/ "../packages/observables/lib/modeldb.js":
/*!**********************************************!*\
  !*** ../packages/observables/lib/modeldb.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ModelDB": () => (/* binding */ ModelDB),
/* harmony export */   "ObservableValue": () => (/* binding */ ObservableValue)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _observablejson__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./observablejson */ "../packages/observables/lib/observablejson.js");
/* harmony import */ var _observablemap__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./observablemap */ "../packages/observables/lib/observablemap.js");
/* harmony import */ var _observablestring__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./observablestring */ "../packages/observables/lib/observablestring.js");
/* harmony import */ var _undoablelist__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./undoablelist */ "../packages/observables/lib/undoablelist.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * A concrete implementation of an `IObservableValue`.
 */
class ObservableValue {
    /**
     * Constructor for the value.
     *
     * @param initialValue: the starting value for the `ObservableValue`.
     */
    constructor(initialValue = null) {
        this._value = null;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal(this);
        this._isDisposed = false;
        this._value = initialValue;
    }
    /**
     * The observable type.
     */
    get type() {
        return 'Value';
    }
    /**
     * Whether the value has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The changed signal.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Get the current value, or `undefined` if it has not been set.
     */
    get() {
        return this._value;
    }
    /**
     * Set the current value.
     */
    set(value) {
        const oldValue = this._value;
        if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.JSONExt.deepEqual(oldValue, value)) {
            return;
        }
        this._value = value;
        this._changed.emit({
            oldValue: oldValue,
            newValue: value
        });
    }
    /**
     * Dispose of the resources held by the value.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_2__.Signal.clearData(this);
        this._value = null;
    }
}
/**
 * The namespace for the `ObservableValue` class statics.
 */
(function (ObservableValue) {
    /**
     * The changed args object emitted by the `IObservableValue`.
     */
    class IChangedArgs {
    }
    ObservableValue.IChangedArgs = IChangedArgs;
})(ObservableValue || (ObservableValue = {}));
/**
 * A concrete implementation of an `IModelDB`.
 */
class ModelDB {
    /**
     * Constructor for the `ModelDB`.
     */
    constructor(options = {}) {
        /**
         * Whether the model has been populated with
         * any model values.
         */
        this.isPrepopulated = false;
        /**
         * Whether the model is collaborative.
         */
        this.isCollaborative = false;
        /**
         * A promise resolved when the model is connected
         * to its backend. For the in-memory ModelDB it
         * is immediately resolved.
         */
        this.connected = Promise.resolve(void 0);
        this._toDispose = false;
        this._isDisposed = false;
        this._disposables = new _lumino_disposable__WEBPACK_IMPORTED_MODULE_1__.DisposableSet();
        this._basePath = options.basePath || '';
        if (options.baseDB) {
            this._db = options.baseDB;
        }
        else {
            this._db = new _observablemap__WEBPACK_IMPORTED_MODULE_3__.ObservableMap();
            this._toDispose = true;
        }
    }
    /**
     * The base path for the `ModelDB`. This is prepended
     * to all the paths that are passed in to the member
     * functions of the object.
     */
    get basePath() {
        return this._basePath;
    }
    /**
     * Whether the database is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Get a value for a path.
     *
     * @param path: the path for the object.
     *
     * @returns an `IObservable`.
     */
    get(path) {
        return this._db.get(this._resolvePath(path));
    }
    /**
     * Whether the `IModelDB` has an object at this path.
     *
     * @param path: the path for the object.
     *
     * @returns a boolean for whether an object is at `path`.
     */
    has(path) {
        return this._db.has(this._resolvePath(path));
    }
    /**
     * Create a string and insert it in the database.
     *
     * @param path: the path for the string.
     *
     * @returns the string that was created.
     */
    createString(path) {
        const str = new _observablestring__WEBPACK_IMPORTED_MODULE_4__.ObservableString();
        this._disposables.add(str);
        this.set(path, str);
        return str;
    }
    /**
     * Create an undoable list and insert it in the database.
     *
     * @param path: the path for the list.
     *
     * @returns the list that was created.
     *
     * #### Notes
     * The list can only store objects that are simple
     * JSON Objects and primitives.
     */
    createList(path) {
        const vec = new _undoablelist__WEBPACK_IMPORTED_MODULE_5__.ObservableUndoableList(new _undoablelist__WEBPACK_IMPORTED_MODULE_5__.ObservableUndoableList.IdentitySerializer());
        this._disposables.add(vec);
        this.set(path, vec);
        return vec;
    }
    /**
     * Create a map and insert it in the database.
     *
     * @param path: the path for the map.
     *
     * @returns the map that was created.
     *
     * #### Notes
     * The map can only store objects that are simple
     * JSON Objects and primitives.
     */
    createMap(path) {
        const map = new _observablejson__WEBPACK_IMPORTED_MODULE_6__.ObservableJSON();
        this._disposables.add(map);
        this.set(path, map);
        return map;
    }
    /**
     * Create an opaque value and insert it in the database.
     *
     * @param path: the path for the value.
     *
     * @returns the value that was created.
     */
    createValue(path) {
        const val = new ObservableValue();
        this._disposables.add(val);
        this.set(path, val);
        return val;
    }
    /**
     * Get a value at a path, or `undefined if it has not been set
     * That value must already have been created using `createValue`.
     *
     * @param path: the path for the value.
     */
    getValue(path) {
        const val = this.get(path);
        if (!val || val.type !== 'Value') {
            throw Error('Can only call getValue for an ObservableValue');
        }
        return val.get();
    }
    /**
     * Set a value at a path. That value must already have
     * been created using `createValue`.
     *
     * @param path: the path for the value.
     *
     * @param value: the new value.
     */
    setValue(path, value) {
        const val = this.get(path);
        if (!val || val.type !== 'Value') {
            throw Error('Can only call setValue on an ObservableValue');
        }
        val.set(value);
    }
    /**
     * Create a view onto a subtree of the model database.
     *
     * @param basePath: the path for the root of the subtree.
     *
     * @returns an `IModelDB` with a view onto the original
     *   `IModelDB`, with `basePath` prepended to all paths.
     */
    view(basePath) {
        const view = new ModelDB({ basePath, baseDB: this });
        this._disposables.add(view);
        return view;
    }
    /**
     * Set a value at a path. Not intended to
     * be called by user code, instead use the
     * `create*` factory methods.
     *
     * @param path: the path to set the value at.
     *
     * @param value: the value to set at the path.
     */
    set(path, value) {
        this._db.set(this._resolvePath(path), value);
    }
    /**
     * Dispose of the resources held by the database.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        if (this._toDispose) {
            this._db.dispose();
        }
        this._disposables.dispose();
    }
    /**
     * Compute the fully resolved path for a path argument.
     */
    _resolvePath(path) {
        if (this._basePath) {
            path = this._basePath + '.' + path;
        }
        return path;
    }
}


/***/ }),

/***/ "../packages/observables/lib/observablejson.js":
/*!*****************************************************!*\
  !*** ../packages/observables/lib/observablejson.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableJSON": () => (/* binding */ ObservableJSON)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _observablemap__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./observablemap */ "../packages/observables/lib/observablemap.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A concrete Observable map for JSON data.
 */
class ObservableJSON extends _observablemap__WEBPACK_IMPORTED_MODULE_2__.ObservableMap {
    /**
     * Construct a new observable JSON object.
     */
    constructor(options = {}) {
        super({
            itemCmp: _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.JSONExt.deepEqual,
            values: options.values
        });
    }
    /**
     * Serialize the model to JSON.
     */
    toJSON() {
        const out = Object.create(null);
        const keys = this.keys();
        for (const key of keys) {
            const value = this.get(key);
            if (value !== undefined) {
                out[key] = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.JSONExt.deepCopy(value);
            }
        }
        return out;
    }
}
/**
 * The namespace for ObservableJSON static data.
 */
(function (ObservableJSON) {
    /**
     * An observable JSON change message.
     */
    class ChangeMessage extends _lumino_messaging__WEBPACK_IMPORTED_MODULE_1__.Message {
        /**
         * Create a new metadata changed message.
         */
        constructor(type, args) {
            super(type);
            this.args = args;
        }
    }
    ObservableJSON.ChangeMessage = ChangeMessage;
})(ObservableJSON || (ObservableJSON = {}));


/***/ }),

/***/ "../packages/observables/lib/observablelist.js":
/*!*****************************************************!*\
  !*** ../packages/observables/lib/observablelist.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableList": () => (/* binding */ ObservableList)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A concrete implementation of [[IObservableList]].
 */
class ObservableList {
    /**
     * Construct a new observable map.
     */
    constructor(options = {}) {
        this._array = [];
        this._isDisposed = false;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        if (options.values) {
            for (const value of options.values) {
                this._array.push(value);
            }
        }
        this._itemCmp = options.itemCmp || Private.itemCmp;
    }
    /**
     * The type of this object.
     */
    get type() {
        return 'List';
    }
    /**
     * A signal emitted when the list has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The length of the list.
     */
    get length() {
        return this._array.length;
    }
    /**
     * Test whether the list has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the list.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.clearData(this);
        this.clear();
    }
    /**
     * Create an iterator over the values in the list.
     *
     * @returns A new iterator starting at the front of the list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     */
    [Symbol.iterator]() {
        return this._array[Symbol.iterator]();
    }
    /**
     * Get the value at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @returns The value at the specified index.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     */
    get(index) {
        return this._array[index];
    }
    /**
     * Set the value at the specified index.
     *
     * @param index - The positive integer index of interest.
     *
     * @param value - The value to set at the specified index.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral or out of range.
     */
    set(index, value) {
        const oldValue = this._array[index];
        if (value === undefined) {
            throw new Error('Cannot set an undefined item');
        }
        // Bail if the value does not change.
        const itemCmp = this._itemCmp;
        if (itemCmp(oldValue, value)) {
            return;
        }
        this._array[index] = value;
        this._changed.emit({
            type: 'set',
            oldIndex: index,
            newIndex: index,
            oldValues: [oldValue],
            newValues: [value]
        });
    }
    /**
     * Add a value to the end of the list.
     *
     * @param value - The value to add to the end of the list.
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Constant.
     *
     * #### Notes
     * By convention, the oldIndex is set to -1 to indicate
     * an push operation.
     *
     * #### Iterator Validity
     * No changes.
     */
    push(value) {
        const num = this._array.push(value);
        this._changed.emit({
            type: 'add',
            oldIndex: -1,
            newIndex: this.length - 1,
            oldValues: [],
            newValues: [value]
        });
        return num;
    }
    /**
     * Insert a value into the list at a specific index.
     *
     * @param index - The index at which to insert the value.
     *
     * @param value - The value to set at the specified index.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the list.
     *
     * By convention, the oldIndex is set to -2 to indicate
     * an insert operation.
     *
     * The value -2 as oldIndex can be used to distinguish from the push
     * method which will use a value -1.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     */
    insert(index, value) {
        if (index === this._array.length) {
            this._array.push(value);
        }
        else {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._array, index, value);
        }
        this._changed.emit({
            type: 'add',
            oldIndex: -2,
            newIndex: index,
            oldValues: [],
            newValues: [value]
        });
    }
    /**
     * Remove the first occurrence of a value from the list.
     *
     * @param value - The value of interest.
     *
     * @returns The index of the removed value, or `-1` if the value
     *   is not contained in the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed value and beyond are invalidated.
     */
    removeValue(value) {
        const itemCmp = this._itemCmp;
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.findFirstIndex(this._array, item => {
            return itemCmp(item, value);
        });
        this.remove(index);
        return index;
    }
    /**
     * Remove and return the value at a specific index.
     *
     * @param index - The index of the value of interest.
     *
     * @returns The value at the specified index, or `undefined` if the
     *   index is out of range.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the removed value and beyond are invalidated.
     *
     * #### Undefined Behavior
     * An `index` which is non-integral.
     */
    remove(index) {
        const value = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.removeAt(this._array, index);
        if (value === undefined) {
            return;
        }
        this._changed.emit({
            type: 'remove',
            oldIndex: index,
            newIndex: -1,
            newValues: [],
            oldValues: [value]
        });
        return value;
    }
    /**
     * Remove all values from the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * All current iterators are invalidated.
     */
    clear() {
        const copy = this._array.slice();
        this._array.length = 0;
        this._changed.emit({
            type: 'remove',
            oldIndex: 0,
            newIndex: 0,
            newValues: [],
            oldValues: copy
        });
    }
    /**
     * Move a value from one index to another.
     *
     * @param fromIndex - The index of the element to move.
     *
     * @param toIndex - The index to move the element to.
     *
     * #### Complexity
     * Constant.
     *
     * #### Iterator Validity
     * Iterators pointing at the lesser of the `fromIndex` and the `toIndex`
     * and beyond are invalidated.
     *
     * #### Undefined Behavior
     * A `fromIndex` or a `toIndex` which is non-integral.
     */
    move(fromIndex, toIndex) {
        if (this.length <= 1 || fromIndex === toIndex) {
            return;
        }
        const values = [this._array[fromIndex]];
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.move(this._array, fromIndex, toIndex);
        this._changed.emit({
            type: 'move',
            oldIndex: fromIndex,
            newIndex: toIndex,
            oldValues: values,
            newValues: values
        });
    }
    /**
     * Push a set of values to the back of the list.
     *
     * @param values - An iterable set of values to add.
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Notes
     * By convention, the oldIndex is set to -1 to indicate
     * an push operation.
     *
     * #### Iterator Validity
     * No changes.
     */
    pushAll(values) {
        const newIndex = this.length;
        for (const value of values) {
            this._array.push(value);
        }
        this._changed.emit({
            type: 'add',
            oldIndex: -1,
            newIndex,
            oldValues: [],
            newValues: Array.from(values)
        });
        return this.length;
    }
    /**
     * Insert a set of items into the list at the specified index.
     *
     * @param index - The index at which to insert the values.
     *
     * @param values - The values to insert at the specified index.
     *
     * #### Complexity.
     * Linear.
     *
     * #### Iterator Validity
     * No changes.
     *
     * #### Notes
     * The `index` will be clamped to the bounds of the list.
     * By convention, the oldIndex is set to -2 to indicate
     * an insert operation.
     *
     * #### Undefined Behavior.
     * An `index` which is non-integral.
     */
    insertAll(index, values) {
        const newIndex = index;
        for (const value of values) {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._array, index++, value);
        }
        this._changed.emit({
            type: 'add',
            oldIndex: -2,
            newIndex,
            oldValues: [],
            newValues: Array.from(values)
        });
    }
    /**
     * Remove a range of items from the list.
     *
     * @param startIndex - The start index of the range to remove (inclusive).
     *
     * @param endIndex - The end index of the range to remove (exclusive).
     *
     * @returns The new length of the list.
     *
     * #### Complexity
     * Linear.
     *
     * #### Iterator Validity
     * Iterators pointing to the first removed value and beyond are invalid.
     *
     * #### Undefined Behavior
     * A `startIndex` or `endIndex` which is non-integral.
     */
    removeRange(startIndex, endIndex) {
        const oldValues = this._array.slice(startIndex, endIndex);
        for (let i = startIndex; i < endIndex; i++) {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.removeAt(this._array, startIndex);
        }
        this._changed.emit({
            type: 'remove',
            oldIndex: startIndex,
            newIndex: -1,
            oldValues,
            newValues: []
        });
        return this.length;
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The default strict equality item cmp.
     */
    function itemCmp(first, second) {
        return first === second;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/observables/lib/observablemap.js":
/*!****************************************************!*\
  !*** ../packages/observables/lib/observablemap.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableMap": () => (/* binding */ ObservableMap)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of IObservableMap<T>.
 */
class ObservableMap {
    /**
     * Construct a new observable map.
     */
    constructor(options = {}) {
        this._map = new Map();
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._isDisposed = false;
        this._itemCmp = options.itemCmp || Private.itemCmp;
        if (options.values) {
            for (const key in options.values) {
                this._map.set(key, options.values[key]);
            }
        }
    }
    /**
     * The type of the Observable.
     */
    get type() {
        return 'Map';
    }
    /**
     * A signal emitted when the map has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Whether this map has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * The number of key-value pairs in the map.
     */
    get size() {
        return this._map.size;
    }
    /**
     * Set a key-value pair in the map
     *
     * @param key - The key to set.
     *
     * @param value - The value for the key.
     *
     * @returns the old value for the key, or undefined
     *   if that did not exist.
     *
     * @throws if the new value is undefined.
     *
     * #### Notes
     * This is a no-op if the value does not change.
     */
    set(key, value) {
        const oldVal = this._map.get(key);
        if (value === undefined) {
            throw Error('Cannot set an undefined value, use remove');
        }
        // Bail if the value does not change.
        const itemCmp = this._itemCmp;
        if (oldVal !== undefined && itemCmp(oldVal, value)) {
            return oldVal;
        }
        this._map.set(key, value);
        this._changed.emit({
            type: oldVal ? 'change' : 'add',
            key: key,
            oldValue: oldVal,
            newValue: value
        });
        return oldVal;
    }
    /**
     * Get a value for a given key.
     *
     * @param key - the key.
     *
     * @returns the value for that key.
     */
    get(key) {
        return this._map.get(key);
    }
    /**
     * Check whether the map has a key.
     *
     * @param key - the key to check.
     *
     * @returns `true` if the map has the key, `false` otherwise.
     */
    has(key) {
        return this._map.has(key);
    }
    /**
     * Get a list of the keys in the map.
     *
     * @returns - a list of keys.
     */
    keys() {
        const keyList = [];
        this._map.forEach((v, k) => {
            keyList.push(k);
        });
        return keyList;
    }
    /**
     * Get a list of the values in the map.
     *
     * @returns - a list of values.
     */
    values() {
        const valList = [];
        this._map.forEach((v, k) => {
            valList.push(v);
        });
        return valList;
    }
    /**
     * Remove a key from the map
     *
     * @param key - the key to remove.
     *
     * @returns the value of the given key,
     *   or undefined if that does not exist.
     *
     * #### Notes
     * This is a no-op if the value does not change.
     */
    delete(key) {
        const oldVal = this._map.get(key);
        const removed = this._map.delete(key);
        if (removed) {
            this._changed.emit({
                type: 'remove',
                key: key,
                oldValue: oldVal,
                newValue: undefined
            });
        }
        return oldVal;
    }
    /**
     * Set the ObservableMap to an empty map.
     */
    clear() {
        // Delete one by one to emit the correct signals.
        const keyList = this.keys();
        for (let i = 0; i < keyList.length; i++) {
            this.delete(keyList[i]);
        }
    }
    /**
     * Dispose of the resources held by the map.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
        this._map.clear();
    }
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The default strict equality item comparator.
     */
    function itemCmp(first, second) {
        return first === second;
    }
    Private.itemCmp = itemCmp;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/observables/lib/observablestring.js":
/*!*******************************************************!*\
  !*** ../packages/observables/lib/observablestring.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableString": () => (/* binding */ ObservableString)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of [[IObservableString]]
 */
class ObservableString {
    /**
     * Construct a new observable string.
     */
    constructor(initialText = '') {
        this._text = '';
        this._isDisposed = false;
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._text = initialText;
    }
    /**
     * The type of the Observable.
     */
    get type() {
        return 'String';
    }
    /**
     * A signal emitted when the string has changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * Set the value of the string.
     */
    set text(value) {
        if (value.length === this._text.length && value === this._text) {
            return;
        }
        this._text = value;
        this._changed.emit({
            type: 'set',
            start: 0,
            end: value.length,
            value: value
        });
    }
    /**
     * Get the value of the string.
     */
    get text() {
        return this._text;
    }
    /**
     * Insert a substring.
     *
     * @param index - The starting index.
     *
     * @param text - The substring to insert.
     */
    insert(index, text) {
        this._text = this._text.slice(0, index) + text + this._text.slice(index);
        this._changed.emit({
            type: 'insert',
            start: index,
            end: index + text.length,
            value: text
        });
    }
    /**
     * Remove a substring.
     *
     * @param start - The starting index.
     *
     * @param end - The ending index.
     */
    remove(start, end) {
        const oldValue = this._text.slice(start, end);
        this._text = this._text.slice(0, start) + this._text.slice(end);
        this._changed.emit({
            type: 'remove',
            start: start,
            end: end,
            value: oldValue
        });
    }
    /**
     * Set the ObservableString to an empty string.
     */
    clear() {
        this.text = '';
    }
    /**
     * Test whether the string has been disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the string.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
        this.clear();
    }
}


/***/ }),

/***/ "../packages/observables/lib/undoablelist.js":
/*!***************************************************!*\
  !*** ../packages/observables/lib/undoablelist.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ObservableUndoableList": () => (/* binding */ ObservableUndoableList)
/* harmony export */ });
/* harmony import */ var _observablelist__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./observablelist */ "../packages/observables/lib/observablelist.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A concrete implementation of an observable undoable list.
 */
class ObservableUndoableList extends _observablelist__WEBPACK_IMPORTED_MODULE_0__.ObservableList {
    /**
     * Construct a new undoable observable list.
     */
    constructor(serializer) {
        super();
        this._inCompound = false;
        this._isUndoable = true;
        this._madeCompoundChange = false;
        this._index = -1;
        this._stack = [];
        this._serializer = serializer;
        this.changed.connect(this._onListChanged, this);
    }
    /**
     * Whether the object can redo changes.
     */
    get canRedo() {
        return this._index < this._stack.length - 1;
    }
    /**
     * Whether the object can undo changes.
     */
    get canUndo() {
        return this._index >= 0;
    }
    /**
     * Begin a compound operation.
     *
     * @param isUndoAble - Whether the operation is undoable.
     *   The default is `true`.
     */
    beginCompoundOperation(isUndoAble) {
        this._inCompound = true;
        this._isUndoable = isUndoAble !== false;
        this._madeCompoundChange = false;
    }
    /**
     * End a compound operation.
     */
    endCompoundOperation() {
        this._inCompound = false;
        this._isUndoable = true;
        if (this._madeCompoundChange) {
            this._index++;
        }
    }
    /**
     * Undo an operation.
     */
    undo() {
        if (!this.canUndo) {
            return;
        }
        const changes = this._stack[this._index];
        this._isUndoable = false;
        for (const change of changes.reverse()) {
            this._undoChange(change);
        }
        this._isUndoable = true;
        this._index--;
    }
    /**
     * Redo an operation.
     */
    redo() {
        if (!this.canRedo) {
            return;
        }
        this._index++;
        const changes = this._stack[this._index];
        this._isUndoable = false;
        for (const change of changes) {
            this._redoChange(change);
        }
        this._isUndoable = true;
    }
    /**
     * Clear the change stack.
     */
    clearUndo() {
        this._index = -1;
        this._stack = [];
    }
    /**
     * Handle a change in the list.
     */
    _onListChanged(list, change) {
        if (this.isDisposed || !this._isUndoable) {
            return;
        }
        // Clear everything after this position if necessary.
        if (!this._inCompound || !this._madeCompoundChange) {
            this._stack = this._stack.slice(0, this._index + 1);
        }
        // Copy the change.
        const evt = this._copyChange(change);
        // Put the change in the stack.
        if (this._stack[this._index + 1]) {
            this._stack[this._index + 1].push(evt);
        }
        else {
            this._stack.push([evt]);
        }
        // If not in a compound operation, increase index.
        if (!this._inCompound) {
            this._index++;
        }
        else {
            this._madeCompoundChange = true;
        }
    }
    /**
     * Undo a change event.
     */
    _undoChange(change) {
        let index = 0;
        const serializer = this._serializer;
        switch (change.type) {
            case 'add':
                for (let length = change.newValues.length; length > 0; length--) {
                    this.remove(change.newIndex);
                }
                break;
            case 'set':
                index = change.oldIndex;
                for (const value of change.oldValues) {
                    this.set(index++, serializer.fromJSON(value));
                }
                break;
            case 'remove':
                index = change.oldIndex;
                for (const value of change.oldValues) {
                    this.insert(index++, serializer.fromJSON(value));
                }
                break;
            case 'move':
                this.move(change.newIndex, change.oldIndex);
                break;
            default:
                return;
        }
    }
    /**
     * Redo a change event.
     */
    _redoChange(change) {
        let index = 0;
        const serializer = this._serializer;
        switch (change.type) {
            case 'add':
                index = change.newIndex;
                for (const value of change.newValues) {
                    this.insert(index++, serializer.fromJSON(value));
                }
                break;
            case 'set':
                index = change.newIndex;
                for (const value of change.newValues) {
                    this.set(change.newIndex++, serializer.fromJSON(value));
                }
                break;
            case 'remove':
                for (let length = change.oldValues.length; length > 0; length--) {
                    this.remove(change.oldIndex);
                }
                break;
            case 'move':
                this.move(change.oldIndex, change.newIndex);
                break;
            default:
                return;
        }
    }
    /**
     * Copy a change as JSON.
     */
    _copyChange(change) {
        const oldValues = [];
        for (const value of change.oldValues) {
            oldValues.push(this._serializer.toJSON(value));
        }
        const newValues = [];
        for (const value of change.newValues) {
            newValues.push(this._serializer.toJSON(value));
        }
        return {
            type: change.type,
            oldIndex: change.oldIndex,
            newIndex: change.newIndex,
            oldValues,
            newValues
        };
    }
}
/**
 * Namespace for ObservableUndoableList utilities.
 */
(function (ObservableUndoableList) {
    /**
     * A default, identity serializer.
     */
    class IdentitySerializer {
        /**
         * Identity serialize.
         */
        toJSON(value) {
            return value;
        }
        /**
         * Identity deserialize.
         */
        fromJSON(value) {
            return value;
        }
    }
    ObservableUndoableList.IdentitySerializer = IdentitySerializer;
})(ObservableUndoableList || (ObservableUndoableList = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfb2JzZXJ2YWJsZXNfbGliX2luZGV4X2pzLjk0ZDFjZWE0YzViOTJlZDA2OWMwLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFFdUI7QUFDTztBQUNBO0FBQ0Q7QUFDRztBQUNKOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ2QvQiwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBT2hDO0FBQ3FDO0FBQ1o7QUFDZTtBQUNIO0FBQ1M7QUFJakQ7QUFvT3hCOztHQUVHO0FBQ0ksTUFBTSxlQUFlO0lBQzFCOzs7O09BSUc7SUFDSCxZQUFZLGVBQTBCLElBQUk7UUEyRGxDLFdBQU0sR0FBYyxJQUFJLENBQUM7UUFDekIsYUFBUSxHQUFHLElBQUkscURBQU0sQ0FBcUMsSUFBSSxDQUFDLENBQUM7UUFDaEUsZ0JBQVcsR0FBRyxLQUFLLENBQUM7UUE1RDFCLElBQUksQ0FBQyxNQUFNLEdBQUcsWUFBWSxDQUFDO0lBQzdCLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksSUFBSTtRQUNOLE9BQU8sT0FBTyxDQUFDO0lBQ2pCLENBQUM7SUFFRDs7T0FFRztJQUNILElBQUksVUFBVTtRQUNaLE9BQU8sSUFBSSxDQUFDLFdBQVcsQ0FBQztJQUMxQixDQUFDO0lBRUQ7O09BRUc7SUFDSCxJQUFJLE9BQU87UUFDVCxPQUFPLElBQUksQ0FBQyxRQUFRLENBQUM7SUFDdkIsQ0FBQztJQUVEOztPQUVHO0lBQ0gsR0FBRztRQUNELE9BQU8sSUFBSSxDQUFDLE1BQU0sQ0FBQztJQUNyQixDQUFDO0lBRUQ7O09BRUc7SUFDSCxHQUFHLENBQUMsS0FBZ0I7UUFDbEIsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLE1BQU0sQ0FBQztRQUM3QixJQUFJLGdFQUFpQixDQUFDLFFBQVEsRUFBRSxLQUFLLENBQUMsRUFBRTtZQUN0QyxPQUFPO1NBQ1I7UUFDRCxJQUFJLENBQUMsTUFBTSxHQUFHLEtBQUssQ0FB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SCxNQUFhLGtCQUFrQjtRQUc3Qjs7V0FFRztRQUNILE1BQU0sQ0FBQyxLQUFRO1lBQ2IsT0FBTyxLQUFLLENBQUM7UUFDZixDQUFDO1FBRUQ7O1dBRUc7UUFDSCxRQUFRLENBQUMsS0FBZ0I7WUFDdkIsT0FBTyxLQUFVLENBQUM7UUFDcEIsQ0FBQztLQUNGO0lBaEJZLHlDQUFrQixxQkFnQjlCO0FBQ0gsQ0FBQyxFQXJCZ0Isc0JBQXNCLEtBQXRCLHNCQUFzQixRQXFCdEMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb2JzZXJ2YWJsZXMvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vYnNlcnZhYmxlcy9zcmMvbW9kZWxkYi50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb2JzZXJ2YWJsZXMvc3JjL29ic2VydmFibGVqc29uLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vYnNlcnZhYmxlcy9zcmMvb2JzZXJ2YWJsZWxpc3QudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL29ic2VydmFibGVzL3NyYy9vYnNlcnZhYmxlbWFwLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9vYnNlcnZhYmxlcy9zcmMvb2JzZXJ2YWJsZXN0cmluZy50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvb2JzZXJ2YWJsZXMvc3JjL3VuZG9hYmxlbGlzdC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIG9ic2VydmFibGVzXG4gKi9cblxuZXhwb3J0ICogZnJvbSAnLi9tb2RlbGRiJztcbmV4cG9ydCAqIGZyb20gJy4vb2JzZXJ2YWJsZWpzb24nO1xuZXhwb3J0ICogZnJvbSAnLi9vYnNlcnZhYmxlbGlzdCc7XG5leHBvcnQgKiBmcm9tICcuL29ic2VydmFibGVtYXAnO1xuZXhwb3J0ICogZnJvbSAnLi9vYnNlcnZhYmxlc3RyaW5nJztcbmV4cG9ydCAqIGZyb20gJy4vdW5kb2FibGVsaXN0JztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHtcbiAgSlNPTkV4dCxcbiAgSlNPTk9iamVjdCxcbiAgSlNPTlZhbHVlLFxuICBQYXJ0aWFsSlNPTlZhbHVlXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IERpc3Bvc2FibGVTZXQsIElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IElPYnNlcnZhYmxlSlNPTiwgT2JzZXJ2YWJsZUpTT04gfSBmcm9tICcuL29ic2VydmFibGVqc29uJztcbmltcG9ydCB7IElPYnNlcnZhYmxlTWFwLCBPYnNlcnZhYmxlTWFwIH0gZnJvbSAnLi9vYnNlcnZhYmxlbWFwJztcbmltcG9ydCB7IElPYnNlcnZhYmxlU3RyaW5nLCBPYnNlcnZhYmxlU3RyaW5nIH0gZnJvbSAnLi9vYnNlcnZhYmxlc3RyaW5nJztcbmltcG9ydCB7XG4gIElPYnNlcnZhYmxlVW5kb2FibGVMaXN0LFxuICBPYnNlcnZhYmxlVW5kb2FibGVMaXN0XG59IGZyb20gJy4vdW5kb2FibGVsaXN0JztcblxuLyoqXG4gKiBTdHJpbmcgdHlwZSBhbm5vdGF0aW9ucyBmb3IgT2JzZXJ2YWJsZSBvYmplY3RzIHRoYXQgY2FuIGJlXG4gKiBjcmVhdGVkIGFuZCBwbGFjZWQgaW4gdGhlIElNb2RlbERCIGludGVyZmFjZS5cbiAqL1xuZXhwb3J0IHR5cGUgT2JzZXJ2YWJsZVR5cGUgPSAnTWFwJyB8ICdMaXN0JyB8ICdTdHJpbmcnIHwgJ1ZhbHVlJztcblxuLyoqXG4gKiBCYXNlIGludGVyZmFjZSBmb3IgT2JzZXJ2YWJsZSBvYmplY3RzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElPYnNlcnZhYmxlIGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhpcyBvYmplY3QuXG4gICAqL1xuICByZWFkb25seSB0eXBlOiBPYnNlcnZhYmxlVHlwZTtcbn1cblxuLyoqXG4gKiBJbnRlcmZhY2UgZm9yIGFuIE9ic2VydmFibGUgb2JqZWN0IHRoYXQgcmVwcmVzZW50c1xuICogYW4gb3BhcXVlIEpTT04gdmFsdWUuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9ic2VydmFibGVWYWx1ZSBleHRlbmRzIElPYnNlcnZhYmxlIHtcbiAgLyoqXG4gICAqIFRoZSB0eXBlIG9mIHRoaXMgb2JqZWN0LlxuICAgKi9cbiAgcmVhZG9ubHkgdHlwZTogJ1ZhbHVlJztcblxuICAvKipcbiAgICogVGhlIGNoYW5nZWQgc2lnbmFsLlxuICAgKi9cbiAgcmVhZG9ubHkgY2hhbmdlZDogSVNpZ25hbDxJT2JzZXJ2YWJsZVZhbHVlLCBPYnNlcnZhYmxlVmFsdWUuSUNoYW5nZWRBcmdzPjtcblxuICAvKipcbiAgICogR2V0IHRoZSBjdXJyZW50IHZhbHVlLCBvciBgdW5kZWZpbmVkYCBpZiBpdCBoYXMgbm90IGJlZW4gc2V0LlxuICAgKi9cbiAgZ2V0KCk6IFBhcnRpYWxKU09OVmFsdWUgfCB1bmRlZmluZWQ7XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgdmFsdWUuXG4gICAqL1xuICBzZXQodmFsdWU6IFBhcnRpYWxKU09OVmFsdWUpOiB2b2lkO1xufVxuXG4vKipcbiAqIEludGVyZmFjZSBmb3IgYW4gb2JqZWN0IHJlcHJlc2VudGluZyBhIHNpbmdsZSBjb2xsYWJvcmF0b3JcbiAqIG9uIGEgcmVhbHRpbWUgbW9kZWwuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUNvbGxhYm9yYXRvciBleHRlbmRzIEpTT05PYmplY3Qge1xuICAvKipcbiAgICogQSB1c2VyIGlkIGZvciB0aGUgY29sbGFib3JhdG9yLlxuICAgKiBUaGlzIG1pZ2h0IG5vdCBiZSB1bmlxdWUsIGlmIHRoZSB1c2VyIGhhcyBtb3JlIHRoYW5cbiAgICogb25lIGVkaXRpbmcgc2Vzc2lvbiBhdCBhIHRpbWUuXG4gICAqL1xuICByZWFkb25seSB1c2VySWQ6IHN0cmluZztcblxuICAvKipcbiAgICogQSBzZXNzaW9uIGlkLCB3aGljaCBzaG91bGQgYmUgdW5pcXVlIHRvIGFcbiAgICogcGFydGljdWxhciB2aWV3IG9uIGEgY29sbGFib3JhdGl2ZSBtb2RlbC5cbiAgICovXG4gIHJlYWRvbmx5IHNlc3Npb25JZDogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBBIGh1bWFuLXJlYWRhYmxlIGRpc3BsYXkgbmFtZSBmb3IgYSBjb2xsYWJvcmF0b3IuXG4gICAqL1xuICByZWFkb25seSBkaXNwbGF5TmFtZTogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBBIGNvbG9yIHRvIGJlIHVzZWQgdG8gaWRlbnRpZnkgdGhlIGNvbGxhYm9yYXRvciBpblxuICAgKiBVSSBlbGVtZW50cy5cbiAgICovXG4gIHJlYWRvbmx5IGNvbG9yOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIEEgaHVtYW4tcmVhZGFibGUgc2hvcnQgbmFtZSBmb3IgYSBjb2xsYWJvcmF0b3IsIGZvclxuICAgKiB1c2UgaW4gcGxhY2VzIHdoZXJlIHRoZSBmdWxsIGBkaXNwbGF5TmFtZWAgd291bGQgdGFrZVxuICAgKiB0b28gbXVjaCBzcGFjZS5cbiAgICovXG4gIHJlYWRvbmx5IHNob3J0TmFtZTogc3RyaW5nO1xufVxuXG4vKipcbiAqIEludGVyZmFjZSBmb3IgYW4gSU9ic2VydmFibGVNYXAgdGhhdCB0cmFja3MgY29sbGFib3JhdG9ycy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJQ29sbGFib3JhdG9yTWFwIGV4dGVuZHMgSU9ic2VydmFibGVNYXA8SUNvbGxhYm9yYXRvcj4ge1xuICAvKipcbiAgICogVGhlIGxvY2FsIGNvbGxhYm9yYXRvciBvbiBhIG1vZGVsLlxuICAgKi9cbiAgcmVhZG9ubHkgbG9jYWxDb2xsYWJvcmF0b3I6IElDb2xsYWJvcmF0b3I7XG59XG5cbi8qKlxuICogQW4gaW50ZXJmYWNlIGZvciBhIHBhdGggYmFzZWQgZGF0YWJhc2UgZm9yXG4gKiBjcmVhdGluZyBhbmQgc3RvcmluZyB2YWx1ZXMsIHdoaWNoIGlzIGFnbm9zdGljXG4gKiB0byB0aGUgcGFydGljdWxhciB0eXBlIG9mIHN0b3JlIGluIHRoZSBiYWNrZW5kLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElNb2RlbERCIGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAvKipcbiAgICogVGhlIGJhc2UgcGF0aCBmb3IgdGhlIGBJTW9kZWxEQmAuIFRoaXMgaXMgcHJlcGVuZGVkXG4gICAqIHRvIGFsbCB0aGUgcGF0aHMgdGhhdCBhcmUgcGFzc2VkIGluIHRvIHRoZSBtZW1iZXJcbiAgICogZnVuY3Rpb25zIG9mIHRoZSBvYmplY3QuXG4gICAqL1xuICByZWFkb25seSBiYXNlUGF0aDogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBkYXRhYmFzZSBoYXMgYmVlbiBkaXNwb3NlZC5cbiAgICovXG4gIHJlYWRvbmx5IGlzRGlzcG9zZWQ6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGRhdGFiYXNlIGhhcyBiZWVuIHBvcHVsYXRlZFxuICAgKiB3aXRoIG1vZGVsIHZhbHVlcyBwcmlvciB0byBjb25uZWN0aW9uLlxuICAgKi9cbiAgcmVhZG9ubHkgaXNQcmVwb3B1bGF0ZWQ6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIGRhdGFiYXNlIGlzIGNvbGxhYm9yYXRpdmUuXG4gICAqL1xuICByZWFkb25seSBpc0NvbGxhYm9yYXRpdmU6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIGRhdGFiYXNlXG4gICAqIGhhcyBjb25uZWN0ZWQgdG8gaXRzIGJhY2tlbmQsIGlmIGFueS5cbiAgICovXG4gIHJlYWRvbmx5IGNvbm5lY3RlZDogUHJvbWlzZTx2b2lkPjtcblxuICAvKipcbiAgICogQSBtYXAgb2YgdGhlIGN1cnJlbnRseSBhY3RpdmUgY29sbGFib3JhdG9yc1xuICAgKiBmb3IgdGhlIGRhdGFiYXNlLCBpbmNsdWRpbmcgdGhlIGxvY2FsIHVzZXIuXG4gICAqL1xuICByZWFkb25seSBjb2xsYWJvcmF0b3JzPzogSUNvbGxhYm9yYXRvck1hcDtcblxuICAvKipcbiAgICogR2V0IGEgdmFsdWUgZm9yIGEgcGF0aC5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgb2JqZWN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBhbiBgSU9ic2VydmFibGVgLlxuICAgKi9cbiAgZ2V0KHBhdGg6IHN0cmluZyk6IElPYnNlcnZhYmxlIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBgSU1vZGVsREJgIGhhcyBhbiBvYmplY3QgYXQgdGhpcyBwYXRoLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBvYmplY3QuXG4gICAqXG4gICAqIEByZXR1cm5zIGEgYm9vbGVhbiBmb3Igd2hldGhlciBhbiBvYmplY3QgaXMgYXQgYHBhdGhgLlxuICAgKi9cbiAgaGFzKHBhdGg6IHN0cmluZyk6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIHN0cmluZyBhbmQgaW5zZXJ0IGl0IGluIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgc3RyaW5nLlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgc3RyaW5nIHRoYXQgd2FzIGNyZWF0ZWQuXG4gICAqL1xuICBjcmVhdGVTdHJpbmcocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGVTdHJpbmc7XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiB1bmRvYWJsZSBsaXN0IGFuZCBpbnNlcnQgaXQgaW4gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgbGlzdCB0aGF0IHdhcyBjcmVhdGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBsaXN0IGNhbiBvbmx5IHN0b3JlIG9iamVjdHMgdGhhdCBhcmUgc2ltcGxlXG4gICAqIEpTT04gT2JqZWN0cyBhbmQgcHJpbWl0aXZlcy5cbiAgICovXG4gIGNyZWF0ZUxpc3Q8VCBleHRlbmRzIEpTT05WYWx1ZT4ocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGVVbmRvYWJsZUxpc3Q8VD47XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIG1hcCBhbmQgaW5zZXJ0IGl0IGluIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgbWFwLlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgbWFwIHRoYXQgd2FzIGNyZWF0ZWQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIG1hcCBjYW4gb25seSBzdG9yZSBvYmplY3RzIHRoYXQgYXJlIHNpbXBsZVxuICAgKiBKU09OIE9iamVjdHMgYW5kIHByaW1pdGl2ZXMuXG4gICAqL1xuICBjcmVhdGVNYXAocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGVKU09OO1xuXG4gIC8qKlxuICAgKiBDcmVhdGUgYW4gb3BhcXVlIHZhbHVlIGFuZCBpbnNlcnQgaXQgaW4gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSB2YWx1ZS5cbiAgICpcbiAgICogQHJldHVybnMgdGhlIHZhbHVlIHRoYXQgd2FzIGNyZWF0ZWQuXG4gICAqL1xuICBjcmVhdGVWYWx1ZShwYXRoOiBzdHJpbmcpOiBJT2JzZXJ2YWJsZVZhbHVlO1xuXG4gIC8qKlxuICAgKiBHZXQgYSB2YWx1ZSBhdCBhIHBhdGgsIG9yIGB1bmRlZmluZWQgaWYgaXQgaGFzIG5vdCBiZWVuIHNldFxuICAgKiBUaGF0IHZhbHVlIG11c3QgYWxyZWFkeSBoYXZlIGJlZW4gY3JlYXRlZCB1c2luZyBgY3JlYXRlVmFsdWVgLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSB2YWx1ZS5cbiAgICovXG4gIGdldFZhbHVlKHBhdGg6IHN0cmluZyk6IEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogU2V0IGEgdmFsdWUgYXQgYSBwYXRoLiBUaGF0IHZhbHVlIG11c3QgYWxyZWFkeSBoYXZlXG4gICAqIGJlZW4gY3JlYXRlZCB1c2luZyBgY3JlYXRlVmFsdWVgLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSB2YWx1ZS5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlOiB0aGUgbmV3IHZhbHVlLlxuICAgKi9cbiAgc2V0VmFsdWUocGF0aDogc3RyaW5nLCB2YWx1ZTogSlNPTlZhbHVlKTogdm9pZDtcblxuICAvKipcbiAgICogQ3JlYXRlIGEgdmlldyBvbnRvIGEgc3VidHJlZSBvZiB0aGUgbW9kZWwgZGF0YWJhc2UuXG4gICAqXG4gICAqIEBwYXJhbSBiYXNlUGF0aDogdGhlIHBhdGggZm9yIHRoZSByb290IG9mIHRoZSBzdWJ0cmVlLlxuICAgKlxuICAgKiBAcmV0dXJucyBhbiBgSU1vZGVsREJgIHdpdGggYSB2aWV3IG9udG8gdGhlIG9yaWdpbmFsXG4gICAqICAgYElNb2RlbERCYCwgd2l0aCBgYmFzZVBhdGhgIHByZXBlbmRlZCB0byBhbGwgcGF0aHMuXG4gICAqL1xuICB2aWV3KGJhc2VQYXRoOiBzdHJpbmcpOiBJTW9kZWxEQjtcblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIGRhdGFiYXNlLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkO1xufVxuXG4vKipcbiAqIEEgY29uY3JldGUgaW1wbGVtZW50YXRpb24gb2YgYW4gYElPYnNlcnZhYmxlVmFsdWVgLlxuICovXG5leHBvcnQgY2xhc3MgT2JzZXJ2YWJsZVZhbHVlIGltcGxlbWVudHMgSU9ic2VydmFibGVWYWx1ZSB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3RvciBmb3IgdGhlIHZhbHVlLlxuICAgKlxuICAgKiBAcGFyYW0gaW5pdGlhbFZhbHVlOiB0aGUgc3RhcnRpbmcgdmFsdWUgZm9yIHRoZSBgT2JzZXJ2YWJsZVZhbHVlYC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKGluaXRpYWxWYWx1ZTogSlNPTlZhbHVlID0gbnVsbCkge1xuICAgIHRoaXMuX3ZhbHVlID0gaW5pdGlhbFZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBvYnNlcnZhYmxlIHR5cGUuXG4gICAqL1xuICBnZXQgdHlwZSgpOiAnVmFsdWUnIHtcbiAgICByZXR1cm4gJ1ZhbHVlJztcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSB2YWx1ZSBoYXMgYmVlbiBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjaGFuZ2VkIHNpZ25hbC5cbiAgICovXG4gIGdldCBjaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgT2JzZXJ2YWJsZVZhbHVlLklDaGFuZ2VkQXJncz4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgY3VycmVudCB2YWx1ZSwgb3IgYHVuZGVmaW5lZGAgaWYgaXQgaGFzIG5vdCBiZWVuIHNldC5cbiAgICovXG4gIGdldCgpOiBKU09OVmFsdWUge1xuICAgIHJldHVybiB0aGlzLl92YWx1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIGN1cnJlbnQgdmFsdWUuXG4gICAqL1xuICBzZXQodmFsdWU6IEpTT05WYWx1ZSk6IHZvaWQge1xuICAgIGNvbnN0IG9sZFZhbHVlID0gdGhpcy5fdmFsdWU7XG4gICAgaWYgKEpTT05FeHQuZGVlcEVxdWFsKG9sZFZhbHVlLCB2YWx1ZSkpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgdGhpcy5fdmFsdWUgPSB2YWx1ZTtcbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgb2xkVmFsdWU6IG9sZFZhbHVlLFxuICAgICAgbmV3VmFsdWU6IHZhbHVlXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHZhbHVlLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5faXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICAgIHRoaXMuX3ZhbHVlID0gbnVsbDtcbiAgfVxuXG4gIHByaXZhdGUgX3ZhbHVlOiBKU09OVmFsdWUgPSBudWxsO1xuICBwcml2YXRlIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBPYnNlcnZhYmxlVmFsdWUuSUNoYW5nZWRBcmdzPih0aGlzKTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIHRoZSBgT2JzZXJ2YWJsZVZhbHVlYCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE9ic2VydmFibGVWYWx1ZSB7XG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBhcmdzIG9iamVjdCBlbWl0dGVkIGJ5IHRoZSBgSU9ic2VydmFibGVWYWx1ZWAuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgSUNoYW5nZWRBcmdzIHtcbiAgICAvKipcbiAgICAgKiBUaGUgb2xkIHZhbHVlLlxuICAgICAqL1xuICAgIG9sZFZhbHVlOiBKU09OVmFsdWUgfCB1bmRlZmluZWQ7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgbmV3IHZhbHVlLlxuICAgICAqL1xuICAgIG5ld1ZhbHVlOiBKU09OVmFsdWUgfCB1bmRlZmluZWQ7XG4gIH1cbn1cblxuLyoqXG4gKiBBIGNvbmNyZXRlIGltcGxlbWVudGF0aW9uIG9mIGFuIGBJTW9kZWxEQmAuXG4gKi9cbmV4cG9ydCBjbGFzcyBNb2RlbERCIGltcGxlbWVudHMgSU1vZGVsREIge1xuICAvKipcbiAgICogQ29uc3RydWN0b3IgZm9yIHRoZSBgTW9kZWxEQmAuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBNb2RlbERCLklDcmVhdGVPcHRpb25zID0ge30pIHtcbiAgICB0aGlzLl9iYXNlUGF0aCA9IG9wdGlvbnMuYmFzZVBhdGggfHwgJyc7XG4gICAgaWYgKG9wdGlvbnMuYmFzZURCKSB7XG4gICAgICB0aGlzLl9kYiA9IG9wdGlvbnMuYmFzZURCO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9kYiA9IG5ldyBPYnNlcnZhYmxlTWFwPElPYnNlcnZhYmxlPigpO1xuICAgICAgdGhpcy5fdG9EaXNwb3NlID0gdHJ1ZTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIGJhc2UgcGF0aCBmb3IgdGhlIGBNb2RlbERCYC4gVGhpcyBpcyBwcmVwZW5kZWRcbiAgICogdG8gYWxsIHRoZSBwYXRocyB0aGF0IGFyZSBwYXNzZWQgaW4gdG8gdGhlIG1lbWJlclxuICAgKiBmdW5jdGlvbnMgb2YgdGhlIG9iamVjdC5cbiAgICovXG4gIGdldCBiYXNlUGF0aCgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLl9iYXNlUGF0aDtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBkYXRhYmFzZSBpcyBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG1vZGVsIGhhcyBiZWVuIHBvcHVsYXRlZCB3aXRoXG4gICAqIGFueSBtb2RlbCB2YWx1ZXMuXG4gICAqL1xuICByZWFkb25seSBpc1ByZXBvcHVsYXRlZDogYm9vbGVhbiA9IGZhbHNlO1xuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBtb2RlbCBpcyBjb2xsYWJvcmF0aXZlLlxuICAgKi9cbiAgcmVhZG9ubHkgaXNDb2xsYWJvcmF0aXZlOiBib29sZWFuID0gZmFsc2U7XG5cbiAgLyoqXG4gICAqIEEgcHJvbWlzZSByZXNvbHZlZCB3aGVuIHRoZSBtb2RlbCBpcyBjb25uZWN0ZWRcbiAgICogdG8gaXRzIGJhY2tlbmQuIEZvciB0aGUgaW4tbWVtb3J5IE1vZGVsREIgaXRcbiAgICogaXMgaW1tZWRpYXRlbHkgcmVzb2x2ZWQuXG4gICAqL1xuICByZWFkb25seSBjb25uZWN0ZWQ6IFByb21pc2U8dm9pZD4gPSBQcm9taXNlLnJlc29sdmUodm9pZCAwKTtcblxuICAvKipcbiAgICogR2V0IGEgdmFsdWUgZm9yIGEgcGF0aC5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgb2JqZWN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBhbiBgSU9ic2VydmFibGVgLlxuICAgKi9cbiAgZ2V0KHBhdGg6IHN0cmluZyk6IElPYnNlcnZhYmxlIHwgdW5kZWZpbmVkIHtcbiAgICByZXR1cm4gdGhpcy5fZGIuZ2V0KHRoaXMuX3Jlc29sdmVQYXRoKHBhdGgpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBgSU1vZGVsREJgIGhhcyBhbiBvYmplY3QgYXQgdGhpcyBwYXRoLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBvYmplY3QuXG4gICAqXG4gICAqIEByZXR1cm5zIGEgYm9vbGVhbiBmb3Igd2hldGhlciBhbiBvYmplY3QgaXMgYXQgYHBhdGhgLlxuICAgKi9cbiAgaGFzKHBhdGg6IHN0cmluZyk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9kYi5oYXModGhpcy5fcmVzb2x2ZVBhdGgocGF0aCkpO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIHN0cmluZyBhbmQgaW5zZXJ0IGl0IGluIHRoZSBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgc3RyaW5nLlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgc3RyaW5nIHRoYXQgd2FzIGNyZWF0ZWQuXG4gICAqL1xuICBjcmVhdGVTdHJpbmcocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGVTdHJpbmcge1xuICAgIGNvbnN0IHN0ciA9IG5ldyBPYnNlcnZhYmxlU3RyaW5nKCk7XG4gICAgdGhpcy5fZGlzcG9zYWJsZXMuYWRkKHN0cik7XG4gICAgdGhpcy5zZXQocGF0aCwgc3RyKTtcbiAgICByZXR1cm4gc3RyO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiB1bmRvYWJsZSBsaXN0IGFuZCBpbnNlcnQgaXQgaW4gdGhlIGRhdGFiYXNlLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgbGlzdCB0aGF0IHdhcyBjcmVhdGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBsaXN0IGNhbiBvbmx5IHN0b3JlIG9iamVjdHMgdGhhdCBhcmUgc2ltcGxlXG4gICAqIEpTT04gT2JqZWN0cyBhbmQgcHJpbWl0aXZlcy5cbiAgICovXG4gIGNyZWF0ZUxpc3Q8VCBleHRlbmRzIEpTT05WYWx1ZT4ocGF0aDogc3RyaW5nKTogSU9ic2VydmFibGVVbmRvYWJsZUxpc3Q8VD4ge1xuICAgIGNvbnN0IHZlYyA9IG5ldyBPYnNlcnZhYmxlVW5kb2FibGVMaXN0PFQ+KFxuICAgICAgbmV3IE9ic2VydmFibGVVbmRvYWJsZUxpc3QuSWRlbnRpdHlTZXJpYWxpemVyPFQ+KClcbiAgICApO1xuICAgIHRoaXMuX2Rpc3Bvc2FibGVzLmFkZCh2ZWMpO1xuICAgIHRoaXMuc2V0KHBhdGgsIHZlYyk7XG4gICAgcmV0dXJuIHZlYztcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBtYXAgYW5kIGluc2VydCBpdCBpbiB0aGUgZGF0YWJhc2UuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIG1hcC5cbiAgICpcbiAgICogQHJldHVybnMgdGhlIG1hcCB0aGF0IHdhcyBjcmVhdGVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBtYXAgY2FuIG9ubHkgc3RvcmUgb2JqZWN0cyB0aGF0IGFyZSBzaW1wbGVcbiAgICogSlNPTiBPYmplY3RzIGFuZCBwcmltaXRpdmVzLlxuICAgKi9cbiAgY3JlYXRlTWFwKHBhdGg6IHN0cmluZyk6IElPYnNlcnZhYmxlSlNPTiB7XG4gICAgY29uc3QgbWFwID0gbmV3IE9ic2VydmFibGVKU09OKCk7XG4gICAgdGhpcy5fZGlzcG9zYWJsZXMuYWRkKG1hcCk7XG4gICAgdGhpcy5zZXQocGF0aCwgbWFwKTtcbiAgICByZXR1cm4gbWFwO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiBvcGFxdWUgdmFsdWUgYW5kIGluc2VydCBpdCBpbiB0aGUgZGF0YWJhc2UuXG4gICAqXG4gICAqIEBwYXJhbSBwYXRoOiB0aGUgcGF0aCBmb3IgdGhlIHZhbHVlLlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgdmFsdWUgdGhhdCB3YXMgY3JlYXRlZC5cbiAgICovXG4gIGNyZWF0ZVZhbHVlKHBhdGg6IHN0cmluZyk6IElPYnNlcnZhYmxlVmFsdWUge1xuICAgIGNvbnN0IHZhbCA9IG5ldyBPYnNlcnZhYmxlVmFsdWUoKTtcbiAgICB0aGlzLl9kaXNwb3NhYmxlcy5hZGQodmFsKTtcbiAgICB0aGlzLnNldChwYXRoLCB2YWwpO1xuICAgIHJldHVybiB2YWw7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGEgdmFsdWUgYXQgYSBwYXRoLCBvciBgdW5kZWZpbmVkIGlmIGl0IGhhcyBub3QgYmVlbiBzZXRcbiAgICogVGhhdCB2YWx1ZSBtdXN0IGFscmVhZHkgaGF2ZSBiZWVuIGNyZWF0ZWQgdXNpbmcgYGNyZWF0ZVZhbHVlYC5cbiAgICpcbiAgICogQHBhcmFtIHBhdGg6IHRoZSBwYXRoIGZvciB0aGUgdmFsdWUuXG4gICAqL1xuICBnZXRWYWx1ZShwYXRoOiBzdHJpbmcpOiBKU09OVmFsdWUgfCB1bmRlZmluZWQge1xuICAgIGNvbnN0IHZhbCA9IHRoaXMuZ2V0KHBhdGgpO1xuICAgIGlmICghdmFsIHx8IHZhbC50eXBlICE9PSAnVmFsdWUnKSB7XG4gICAgICB0aHJvdyBFcnJvcignQ2FuIG9ubHkgY2FsbCBnZXRWYWx1ZSBmb3IgYW4gT2JzZXJ2YWJsZVZhbHVlJyk7XG4gICAgfVxuICAgIHJldHVybiAodmFsIGFzIE9ic2VydmFibGVWYWx1ZSkuZ2V0KCk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IGEgdmFsdWUgYXQgYSBwYXRoLiBUaGF0IHZhbHVlIG11c3QgYWxyZWFkeSBoYXZlXG4gICAqIGJlZW4gY3JlYXRlZCB1c2luZyBgY3JlYXRlVmFsdWVgLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggZm9yIHRoZSB2YWx1ZS5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlOiB0aGUgbmV3IHZhbHVlLlxuICAgKi9cbiAgc2V0VmFsdWUocGF0aDogc3RyaW5nLCB2YWx1ZTogSlNPTlZhbHVlKTogdm9pZCB7XG4gICAgY29uc3QgdmFsID0gdGhpcy5nZXQocGF0aCk7XG4gICAgaWYgKCF2YWwgfHwgdmFsLnR5cGUgIT09ICdWYWx1ZScpIHtcbiAgICAgIHRocm93IEVycm9yKCdDYW4gb25seSBjYWxsIHNldFZhbHVlIG9uIGFuIE9ic2VydmFibGVWYWx1ZScpO1xuICAgIH1cbiAgICAodmFsIGFzIE9ic2VydmFibGVWYWx1ZSkuc2V0KHZhbHVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSB2aWV3IG9udG8gYSBzdWJ0cmVlIG9mIHRoZSBtb2RlbCBkYXRhYmFzZS5cbiAgICpcbiAgICogQHBhcmFtIGJhc2VQYXRoOiB0aGUgcGF0aCBmb3IgdGhlIHJvb3Qgb2YgdGhlIHN1YnRyZWUuXG4gICAqXG4gICAqIEByZXR1cm5zIGFuIGBJTW9kZWxEQmAgd2l0aCBhIHZpZXcgb250byB0aGUgb3JpZ2luYWxcbiAgICogICBgSU1vZGVsREJgLCB3aXRoIGBiYXNlUGF0aGAgcHJlcGVuZGVkIHRvIGFsbCBwYXRocy5cbiAgICovXG4gIHZpZXcoYmFzZVBhdGg6IHN0cmluZyk6IE1vZGVsREIge1xuICAgIGNvbnN0IHZpZXcgPSBuZXcgTW9kZWxEQih7IGJhc2VQYXRoLCBiYXNlREI6IHRoaXMgfSk7XG4gICAgdGhpcy5fZGlzcG9zYWJsZXMuYWRkKHZpZXcpO1xuICAgIHJldHVybiB2aWV3O1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIHZhbHVlIGF0IGEgcGF0aC4gTm90IGludGVuZGVkIHRvXG4gICAqIGJlIGNhbGxlZCBieSB1c2VyIGNvZGUsIGluc3RlYWQgdXNlIHRoZVxuICAgKiBgY3JlYXRlKmAgZmFjdG9yeSBtZXRob2RzLlxuICAgKlxuICAgKiBAcGFyYW0gcGF0aDogdGhlIHBhdGggdG8gc2V0IHRoZSB2YWx1ZSBhdC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlOiB0aGUgdmFsdWUgdG8gc2V0IGF0IHRoZSBwYXRoLlxuICAgKi9cbiAgc2V0KHBhdGg6IHN0cmluZywgdmFsdWU6IElPYnNlcnZhYmxlKTogdm9pZCB7XG4gICAgdGhpcy5fZGIuc2V0KHRoaXMuX3Jlc29sdmVQYXRoKHBhdGgpLCB2YWx1ZSk7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIGRhdGFiYXNlLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgIGlmICh0aGlzLl90b0Rpc3Bvc2UpIHtcbiAgICAgIHRoaXMuX2RiLmRpc3Bvc2UoKTtcbiAgICB9XG4gICAgdGhpcy5fZGlzcG9zYWJsZXMuZGlzcG9zZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIENvbXB1dGUgdGhlIGZ1bGx5IHJlc29sdmVkIHBhdGggZm9yIGEgcGF0aCBhcmd1bWVudC5cbiAgICovXG4gIHByaXZhdGUgX3Jlc29sdmVQYXRoKHBhdGg6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgaWYgKHRoaXMuX2Jhc2VQYXRoKSB7XG4gICAgICBwYXRoID0gdGhpcy5fYmFzZVBhdGggKyAnLicgKyBwYXRoO1xuICAgIH1cbiAgICByZXR1cm4gcGF0aDtcbiAgfVxuXG4gIHByaXZhdGUgX2Jhc2VQYXRoOiBzdHJpbmc7XG4gIHByaXZhdGUgX2RiOiBNb2RlbERCIHwgT2JzZXJ2YWJsZU1hcDxJT2JzZXJ2YWJsZT47XG4gIHByaXZhdGUgX3RvRGlzcG9zZSA9IGZhbHNlO1xuICBwcml2YXRlIF9pc0Rpc3Bvc2VkID0gZmFsc2U7XG4gIHByaXZhdGUgX2Rpc3Bvc2FibGVzID0gbmV3IERpc3Bvc2FibGVTZXQoKTtcbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgdGhlIGBNb2RlbERCYCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE1vZGVsREIge1xuICAvKipcbiAgICogT3B0aW9ucyBmb3IgY3JlYXRpbmcgYSBgTW9kZWxEQmAgb2JqZWN0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ3JlYXRlT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIGJhc2UgcGF0aCB0byBwcmVwZW5kIHRvIGFsbCB0aGUgcGF0aCBhcmd1bWVudHMuXG4gICAgICovXG4gICAgYmFzZVBhdGg/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBBIE1vZGVsREIgdG8gdXNlIGFzIHRoZSBzdG9yZSBmb3IgdGhpc1xuICAgICAqIE1vZGVsREIuIElmIG5vbmUgaXMgZ2l2ZW4sIGl0IHVzZXMgaXRzIG93biBzdG9yZS5cbiAgICAgKi9cbiAgICBiYXNlREI/OiBNb2RlbERCO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgZmFjdG9yeSBpbnRlcmZhY2UgZm9yIGNyZWF0aW5nIGBJTW9kZWxEQmAgb2JqZWN0cy5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUZhY3Rvcnkge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBgSU1vZGVsREJgIGluc3RhbmNlLlxuICAgICAqL1xuICAgIGNyZWF0ZU5ldyhwYXRoOiBzdHJpbmcpOiBJTW9kZWxEQjtcbiAgfVxufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQge1xuICBKU09ORXh0LFxuICBKU09OT2JqZWN0LFxuICBQYXJ0aWFsSlNPTk9iamVjdCxcbiAgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IE1lc3NhZ2UgfSBmcm9tICdAbHVtaW5vL21lc3NhZ2luZyc7XG5pbXBvcnQgeyBJT2JzZXJ2YWJsZU1hcCwgT2JzZXJ2YWJsZU1hcCB9IGZyb20gJy4vb2JzZXJ2YWJsZW1hcCc7XG5cbi8qKlxuICogQW4gb2JzZXJ2YWJsZSBKU09OIHZhbHVlLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElPYnNlcnZhYmxlSlNPTlxuICBleHRlbmRzIElPYnNlcnZhYmxlTWFwPFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZD4ge1xuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IFBhcnRpYWxKU09OT2JqZWN0O1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIElPYnNlcnZhYmxlSlNPTiByZWxhdGVkIGludGVyZmFjZXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSU9ic2VydmFibGVKU09OIHtcbiAgLyoqXG4gICAqIEEgdHlwZSBhbGlhcyBmb3Igb2JzZXJ2YWJsZSBKU09OIGNoYW5nZWQgYXJncy5cbiAgICovXG4gIGV4cG9ydCB0eXBlIElDaGFuZ2VkQXJncyA9XG4gICAgSU9ic2VydmFibGVNYXAuSUNoYW5nZWRBcmdzPFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZT47XG59XG5cbi8qKlxuICogQSBjb25jcmV0ZSBPYnNlcnZhYmxlIG1hcCBmb3IgSlNPTiBkYXRhLlxuICovXG5leHBvcnQgY2xhc3MgT2JzZXJ2YWJsZUpTT04gZXh0ZW5kcyBPYnNlcnZhYmxlTWFwPFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZT4ge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IG9ic2VydmFibGUgSlNPTiBvYmplY3QuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBPYnNlcnZhYmxlSlNPTi5JT3B0aW9ucyA9IHt9KSB7XG4gICAgc3VwZXIoe1xuICAgICAgaXRlbUNtcDogSlNPTkV4dC5kZWVwRXF1YWwsXG4gICAgICB2YWx1ZXM6IG9wdGlvbnMudmFsdWVzXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogU2VyaWFsaXplIHRoZSBtb2RlbCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKCk6IFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICBjb25zdCBvdXQ6IFBhcnRpYWxKU09OT2JqZWN0ID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcbiAgICBjb25zdCBrZXlzID0gdGhpcy5rZXlzKCk7XG5cbiAgICBmb3IgKGNvbnN0IGtleSBvZiBrZXlzKSB7XG4gICAgICBjb25zdCB2YWx1ZSA9IHRoaXMuZ2V0KGtleSk7XG5cbiAgICAgIGlmICh2YWx1ZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgIG91dFtrZXldID0gSlNPTkV4dC5kZWVwQ29weSh2YWx1ZSkgYXMgUGFydGlhbEpTT05PYmplY3Q7XG4gICAgICB9XG4gICAgfVxuICAgIHJldHVybiBvdXQ7XG4gIH1cbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBPYnNlcnZhYmxlSlNPTiBzdGF0aWMgZGF0YS5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBPYnNlcnZhYmxlSlNPTiB7XG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2UgdG8gaW5pdGlhbGl6ZSBhbiBvYnNlcnZhYmxlIEpTT04gb2JqZWN0LlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIG9wdGlvbmFsIGluaXRpYWwgdmFsdWUgZm9yIHRoZSBvYmplY3QuXG4gICAgICovXG4gICAgdmFsdWVzPzogSlNPTk9iamVjdDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiBvYnNlcnZhYmxlIEpTT04gY2hhbmdlIG1lc3NhZ2UuXG4gICAqL1xuICBleHBvcnQgY2xhc3MgQ2hhbmdlTWVzc2FnZSBleHRlbmRzIE1lc3NhZ2Uge1xuICAgIC8qKlxuICAgICAqIENyZWF0ZSBhIG5ldyBtZXRhZGF0YSBjaGFuZ2VkIG1lc3NhZ2UuXG4gICAgICovXG4gICAgY29uc3RydWN0b3IodHlwZTogc3RyaW5nLCBhcmdzOiBJT2JzZXJ2YWJsZUpTT04uSUNoYW5nZWRBcmdzKSB7XG4gICAgICBzdXBlcih0eXBlKTtcbiAgICAgIHRoaXMuYXJncyA9IGFyZ3M7XG4gICAgfVxuXG4gICAgLyoqXG4gICAgICogVGhlIGFyZ3VtZW50cyBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGFyZ3M6IElPYnNlcnZhYmxlSlNPTi5JQ2hhbmdlZEFyZ3M7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgQXJyYXlFeHQgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5cbi8qKlxuICogQSBsaXN0IHdoaWNoIGNhbiBiZSBvYnNlcnZlZCBmb3IgY2hhbmdlcy5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJT2JzZXJ2YWJsZUxpc3Q8VD4gZXh0ZW5kcyBJRGlzcG9zYWJsZSwgSXRlcmFibGU8VD4ge1xuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBsaXN0IGhhcyBjaGFuZ2VkLlxuICAgKi9cbiAgcmVhZG9ubHkgY2hhbmdlZDogSVNpZ25hbDx0aGlzLCBJT2JzZXJ2YWJsZUxpc3QuSUNoYW5nZWRBcmdzPFQ+PjtcblxuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhpcyBvYmplY3QuXG4gICAqL1xuICByZWFkb25seSB0eXBlOiAnTGlzdCc7XG5cbiAgLyoqXG4gICAqIFRoZSBsZW5ndGggb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBhIHJlYWQtb25seSBwcm9wZXJ0eS5cbiAgICovXG4gIGxlbmd0aDogbnVtYmVyO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgYWxsIHZhbHVlcyBmcm9tIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIEFsbCBjdXJyZW50IGl0ZXJhdG9ycyBhcmUgaW52YWxpZGF0ZWQuXG4gICAqL1xuICBjbGVhcigpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBHZXQgdGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBwb3NpdGl2ZSBpbnRlZ2VyIGluZGV4IG9mIGludGVyZXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwgb3Igb3V0IG9mIHJhbmdlLlxuICAgKi9cbiAgZ2V0KGluZGV4OiBudW1iZXIpOiBUO1xuXG4gIC8qKlxuICAgKiBJbnNlcnQgYSB2YWx1ZSBpbnRvIHRoZSBsaXN0IGF0IGEgc3BlY2lmaWMgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBpbmRleCBhdCB3aGljaCB0byBpbnNlcnQgdGhlIHZhbHVlLlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgdG8gc2V0IGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGUgYGluZGV4YCB3aWxsIGJlIGNsYW1wZWQgdG8gdGhlIGJvdW5kcyBvZiB0aGUgbGlzdC5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwuXG4gICAqL1xuICBpbnNlcnQoaW5kZXg6IG51bWJlciwgdmFsdWU6IFQpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBJbnNlcnQgYSBzZXQgb2YgaXRlbXMgaW50byB0aGUgbGlzdCBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXggLSBUaGUgaW5kZXggYXQgd2hpY2ggdG8gaW5zZXJ0IHRoZSB2YWx1ZXMuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZXMgLSBUaGUgdmFsdWVzIHRvIGluc2VydCBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHkuXG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBgaW5kZXhgIHdpbGwgYmUgY2xhbXBlZCB0byB0aGUgYm91bmRzIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvci5cbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwuXG4gICAqL1xuICBpbnNlcnRBbGwoaW5kZXg6IG51bWJlciwgdmFsdWVzOiBJdGVyYWJsZTxUPik6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIE1vdmUgYSB2YWx1ZSBmcm9tIG9uZSBpbmRleCB0byBhbm90aGVyLlxuICAgKlxuICAgKiBAcGFyYW0gZnJvbUluZGV4IC0gVGhlIGluZGV4IG9mIHRoZSBlbGVtZW50IHRvIG1vdmUuXG4gICAqXG4gICAqIEBwYXJhbSB0b0luZGV4IC0gVGhlIGluZGV4IHRvIG1vdmUgdGhlIGVsZW1lbnQgdG8uXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBDb25zdGFudC5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBJdGVyYXRvcnMgcG9pbnRpbmcgYXQgdGhlIGxlc3NlciBvZiB0aGUgYGZyb21JbmRleGAgYW5kIHRoZSBgdG9JbmRleGBcbiAgICogYW5kIGJleW9uZCBhcmUgaW52YWxpZGF0ZWQuXG4gICAqXG4gICAqICMjIyMgVW5kZWZpbmVkIEJlaGF2aW9yXG4gICAqIEEgYGZyb21JbmRleGAgb3IgYSBgdG9JbmRleGAgd2hpY2ggaXMgbm9uLWludGVncmFsLlxuICAgKi9cbiAgbW92ZShmcm9tSW5kZXg6IG51bWJlciwgdG9JbmRleDogbnVtYmVyKTogdm9pZDtcblxuICAvKipcbiAgICogQWRkIGEgdmFsdWUgdG8gdGhlIGJhY2sgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSB0byBhZGQgdG8gdGhlIGJhY2sgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICovXG4gIHB1c2godmFsdWU6IFQpOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFB1c2ggYSBzZXQgb2YgdmFsdWVzIHRvIHRoZSBiYWNrIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWVzIC0gQW4gaXRlcmFibGUgc2V0IG9mIHZhbHVlcyB0byBhZGQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIE5vIGNoYW5nZXMuXG4gICAqL1xuICBwdXNoQWxsKHZhbHVlczogSXRlcmFibGU8VD4pOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhbmQgcmV0dXJuIHRoZSB2YWx1ZSBhdCBhIHNwZWNpZmljIGluZGV4LlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXggLSBUaGUgaW5kZXggb2YgdGhlIHZhbHVlIG9mIGludGVyZXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleCwgb3IgYHVuZGVmaW5lZGAgaWYgdGhlXG4gICAqICAgaW5kZXggaXMgb3V0IG9mIHJhbmdlLlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogSXRlcmF0b3JzIHBvaW50aW5nIGF0IHRoZSByZW1vdmVkIHZhbHVlIGFuZCBiZXlvbmQgYXJlIGludmFsaWRhdGVkLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIHJlbW92ZShpbmRleDogbnVtYmVyKTogVCB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogUmVtb3ZlIGEgcmFuZ2Ugb2YgaXRlbXMgZnJvbSB0aGUgbGlzdC5cbiAgICpcbiAgICogQHBhcmFtIHN0YXJ0SW5kZXggLSBUaGUgc3RhcnQgaW5kZXggb2YgdGhlIHJhbmdlIHRvIHJlbW92ZSAoaW5jbHVzaXZlKS5cbiAgICpcbiAgICogQHBhcmFtIGVuZEluZGV4IC0gVGhlIGVuZCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVtb3ZlIChleGNsdXNpdmUpLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgbmV3IGxlbmd0aCBvZiB0aGUgbGlzdC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBJdGVyYXRvcnMgcG9pbnRpbmcgdG8gdGhlIGZpcnN0IHJlbW92ZWQgdmFsdWUgYW5kIGJleW9uZCBhcmUgaW52YWxpZC5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQSBgc3RhcnRJbmRleGAgb3IgYGVuZEluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwuXG4gICAqL1xuICByZW1vdmVSYW5nZShzdGFydEluZGV4OiBudW1iZXIsIGVuZEluZGV4OiBudW1iZXIpOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFJlbW92ZSB0aGUgZmlyc3Qgb2NjdXJyZW5jZSBvZiBhIHZhbHVlIGZyb20gdGhlIGxpc3QuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIGluZGV4IG9mIHRoZSByZW1vdmVkIHZhbHVlLCBvciBgLTFgIGlmIHRoZSB2YWx1ZVxuICAgKiAgIGlzIG5vdCBjb250YWluZWQgaW4gdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogSXRlcmF0b3JzIHBvaW50aW5nIGF0IHRoZSByZW1vdmVkIHZhbHVlIGFuZCBiZXlvbmQgYXJlIGludmFsaWRhdGVkLlxuICAgKi9cbiAgcmVtb3ZlVmFsdWUodmFsdWU6IFQpOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFNldCB0aGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIHBvc2l0aXZlIGludGVnZXIgaW5kZXggb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSB0byBzZXQgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIENvbnN0YW50LlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIE5vIGNoYW5nZXMuXG4gICAqXG4gICAqICMjIyMgVW5kZWZpbmVkIEJlaGF2aW9yXG4gICAqIEFuIGBpbmRleGAgd2hpY2ggaXMgbm9uLWludGVncmFsIG9yIG91dCBvZiByYW5nZS5cbiAgICovXG4gIHNldChpbmRleDogbnVtYmVyLCB2YWx1ZTogVCk6IHZvaWQ7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgSU9ic2VydmFibGVMaXN0IHJlbGF0ZWQgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJT2JzZXJ2YWJsZUxpc3Qge1xuICAvKipcbiAgICogVGhlIGNoYW5nZSB0eXBlcyB3aGljaCBvY2N1ciBvbiBhbiBvYnNlcnZhYmxlIGxpc3QuXG4gICAqL1xuICBleHBvcnQgdHlwZSBDaGFuZ2VUeXBlID1cbiAgICAvKipcbiAgICAgKiBJdGVtKHMpIHdlcmUgYWRkZWQgdG8gdGhlIGxpc3QuXG4gICAgICovXG4gICAgfCAnYWRkJ1xuXG4gICAgLyoqXG4gICAgICogQW4gaXRlbSB3YXMgbW92ZWQgd2l0aGluIHRoZSBsaXN0LlxuICAgICAqL1xuICAgIHwgJ21vdmUnXG5cbiAgICAvKipcbiAgICAgKiBJdGVtKHMpIHdlcmUgcmVtb3ZlZCBmcm9tIHRoZSBsaXN0LlxuICAgICAqL1xuICAgIHwgJ3JlbW92ZSdcblxuICAgIC8qKlxuICAgICAqIEFuIGl0ZW0gd2FzIHNldCBpbiB0aGUgbGlzdC5cbiAgICAgKi9cbiAgICB8ICdzZXQnO1xuXG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBhcmdzIG9iamVjdCB3aGljaCBpcyBlbWl0dGVkIGJ5IGFuIG9ic2VydmFibGUgbGlzdC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUNoYW5nZWRBcmdzPFQ+IHtcbiAgICAvKipcbiAgICAgKiBUaGUgdHlwZSBvZiBjaGFuZ2UgdW5kZXJnb25lIGJ5IHRoZSB2ZWN0b3IuXG4gICAgICovXG4gICAgdHlwZTogQ2hhbmdlVHlwZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBuZXcgaW5kZXggYXNzb2NpYXRlZCB3aXRoIHRoZSBjaGFuZ2UuXG4gICAgICovXG4gICAgbmV3SW5kZXg6IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBuZXcgdmFsdWVzIGFzc29jaWF0ZWQgd2l0aCB0aGUgY2hhbmdlLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoZSB2YWx1ZXMgd2lsbCBiZSBjb250aWd1b3VzIHN0YXJ0aW5nIGF0IHRoZSBgbmV3SW5kZXhgLlxuICAgICAqL1xuICAgIG5ld1ZhbHVlczogVFtdO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG9sZCBpbmRleCBhc3NvY2lhdGVkIHdpdGggdGhlIGNoYW5nZS5cbiAgICAgKi9cbiAgICBvbGRJbmRleDogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG9sZCB2YWx1ZXMgYXNzb2NpYXRlZCB3aXRoIHRoZSBjaGFuZ2UuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhlIHZhbHVlcyB3aWxsIGJlIGNvbnRpZ3VvdXMgc3RhcnRpbmcgYXQgdGhlIGBvbGRJbmRleGAuXG4gICAgICovXG4gICAgb2xkVmFsdWVzOiBUW107XG4gIH1cbn1cblxuLyoqXG4gKiBBIGNvbmNyZXRlIGltcGxlbWVudGF0aW9uIG9mIFtbSU9ic2VydmFibGVMaXN0XV0uXG4gKi9cbmV4cG9ydCBjbGFzcyBPYnNlcnZhYmxlTGlzdDxUPiBpbXBsZW1lbnRzIElPYnNlcnZhYmxlTGlzdDxUPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgb2JzZXJ2YWJsZSBtYXAuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBPYnNlcnZhYmxlTGlzdC5JT3B0aW9uczxUPiA9IHt9KSB7XG4gICAgaWYgKG9wdGlvbnMudmFsdWVzKSB7XG4gICAgICBmb3IgKGNvbnN0IHZhbHVlIG9mIG9wdGlvbnMudmFsdWVzKSB7XG4gICAgICAgIHRoaXMuX2FycmF5LnB1c2godmFsdWUpO1xuICAgICAgfVxuICAgIH1cbiAgICB0aGlzLl9pdGVtQ21wID0gb3B0aW9ucy5pdGVtQ21wIHx8IFByaXZhdGUuaXRlbUNtcDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgdHlwZSBvZiB0aGlzIG9iamVjdC5cbiAgICovXG4gIGdldCB0eXBlKCk6ICdMaXN0JyB7XG4gICAgcmV0dXJuICdMaXN0JztcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIGxpc3QgaGFzIGNoYW5nZWQuXG4gICAqL1xuICBnZXQgY2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8VD4+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKi9cbiAgZ2V0IGxlbmd0aCgpOiBudW1iZXIge1xuICAgIHJldHVybiB0aGlzLl9hcnJheS5sZW5ndGg7XG4gIH1cblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSBsaXN0IGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIGxpc3QuXG4gICAqL1xuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9pc0Rpc3Bvc2VkKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gICAgdGhpcy5jbGVhcigpO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhbiBpdGVyYXRvciBvdmVyIHRoZSB2YWx1ZXMgaW4gdGhlIGxpc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgbmV3IGl0ZXJhdG9yIHN0YXJ0aW5nIGF0IHRoZSBmcm9udCBvZiB0aGUgbGlzdC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIENvbnN0YW50LlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIE5vIGNoYW5nZXMuXG4gICAqL1xuICBbU3ltYm9sLml0ZXJhdG9yXSgpOiBJdGVyYWJsZUl0ZXJhdG9yPFQ+IHtcbiAgICByZXR1cm4gdGhpcy5fYXJyYXlbU3ltYm9sLml0ZXJhdG9yXSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCB0aGUgdmFsdWUgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIHBvc2l0aXZlIGludGVnZXIgaW5kZXggb2YgaW50ZXJlc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSB2YWx1ZSBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbCBvciBvdXQgb2YgcmFuZ2UuXG4gICAqL1xuICBnZXQoaW5kZXg6IG51bWJlcik6IFQge1xuICAgIHJldHVybiB0aGlzLl9hcnJheVtpbmRleF07XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSB2YWx1ZSBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiBAcGFyYW0gaW5kZXggLSBUaGUgcG9zaXRpdmUgaW50ZWdlciBpbmRleCBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIHZhbHVlIHRvIHNldCBhdCB0aGUgc3BlY2lmaWVkIGluZGV4LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwgb3Igb3V0IG9mIHJhbmdlLlxuICAgKi9cbiAgc2V0KGluZGV4OiBudW1iZXIsIHZhbHVlOiBUKTogdm9pZCB7XG4gICAgY29uc3Qgb2xkVmFsdWUgPSB0aGlzLl9hcnJheVtpbmRleF07XG4gICAgaWYgKHZhbHVlID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcignQ2Fubm90IHNldCBhbiB1bmRlZmluZWQgaXRlbScpO1xuICAgIH1cbiAgICAvLyBCYWlsIGlmIHRoZSB2YWx1ZSBkb2VzIG5vdCBjaGFuZ2UuXG4gICAgY29uc3QgaXRlbUNtcCA9IHRoaXMuX2l0ZW1DbXA7XG4gICAgaWYgKGl0ZW1DbXAob2xkVmFsdWUsIHZhbHVlKSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9hcnJheVtpbmRleF0gPSB2YWx1ZTtcbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ3NldCcsXG4gICAgICBvbGRJbmRleDogaW5kZXgsXG4gICAgICBuZXdJbmRleDogaW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IFtvbGRWYWx1ZV0sXG4gICAgICBuZXdWYWx1ZXM6IFt2YWx1ZV1cbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSB2YWx1ZSB0byB0aGUgZW5kIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgdG8gYWRkIHRvIHRoZSBlbmQgb2YgdGhlIGxpc3QuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogQnkgY29udmVudGlvbiwgdGhlIG9sZEluZGV4IGlzIHNldCB0byAtMSB0byBpbmRpY2F0ZVxuICAgKiBhbiBwdXNoIG9wZXJhdGlvbi5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKi9cbiAgcHVzaCh2YWx1ZTogVCk6IG51bWJlciB7XG4gICAgY29uc3QgbnVtID0gdGhpcy5fYXJyYXkucHVzaCh2YWx1ZSk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdhZGQnLFxuICAgICAgb2xkSW5kZXg6IC0xLFxuICAgICAgbmV3SW5kZXg6IHRoaXMubGVuZ3RoIC0gMSxcbiAgICAgIG9sZFZhbHVlczogW10sXG4gICAgICBuZXdWYWx1ZXM6IFt2YWx1ZV1cbiAgICB9KTtcbiAgICByZXR1cm4gbnVtO1xuICB9XG5cbiAgLyoqXG4gICAqIEluc2VydCBhIHZhbHVlIGludG8gdGhlIGxpc3QgYXQgYSBzcGVjaWZpYyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IGF0IHdoaWNoIHRvIGluc2VydCB0aGUgdmFsdWUuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSB0byBzZXQgYXQgdGhlIHNwZWNpZmllZCBpbmRleC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBObyBjaGFuZ2VzLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSBgaW5kZXhgIHdpbGwgYmUgY2xhbXBlZCB0byB0aGUgYm91bmRzIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiBCeSBjb252ZW50aW9uLCB0aGUgb2xkSW5kZXggaXMgc2V0IHRvIC0yIHRvIGluZGljYXRlXG4gICAqIGFuIGluc2VydCBvcGVyYXRpb24uXG4gICAqXG4gICAqIFRoZSB2YWx1ZSAtMiBhcyBvbGRJbmRleCBjYW4gYmUgdXNlZCB0byBkaXN0aW5ndWlzaCBmcm9tIHRoZSBwdXNoXG4gICAqIG1ldGhvZCB3aGljaCB3aWxsIHVzZSBhIHZhbHVlIC0xLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBbiBgaW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIGluc2VydChpbmRleDogbnVtYmVyLCB2YWx1ZTogVCk6IHZvaWQge1xuICAgIGlmIChpbmRleCA9PT0gdGhpcy5fYXJyYXkubGVuZ3RoKSB7XG4gICAgICB0aGlzLl9hcnJheS5wdXNoKHZhbHVlKTtcbiAgICB9IGVsc2Uge1xuICAgICAgQXJyYXlFeHQuaW5zZXJ0KHRoaXMuX2FycmF5LCBpbmRleCwgdmFsdWUpO1xuICAgIH1cbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ2FkZCcsXG4gICAgICBvbGRJbmRleDogLTIsXG4gICAgICBuZXdJbmRleDogaW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IFtdLFxuICAgICAgbmV3VmFsdWVzOiBbdmFsdWVdXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIHRoZSBmaXJzdCBvY2N1cnJlbmNlIG9mIGEgdmFsdWUgZnJvbSB0aGUgbGlzdC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIHZhbHVlIG9mIGludGVyZXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgaW5kZXggb2YgdGhlIHJlbW92ZWQgdmFsdWUsIG9yIGAtMWAgaWYgdGhlIHZhbHVlXG4gICAqICAgaXMgbm90IGNvbnRhaW5lZCBpbiB0aGUgbGlzdC5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIExpbmVhci5cbiAgICpcbiAgICogIyMjIyBJdGVyYXRvciBWYWxpZGl0eVxuICAgKiBJdGVyYXRvcnMgcG9pbnRpbmcgYXQgdGhlIHJlbW92ZWQgdmFsdWUgYW5kIGJleW9uZCBhcmUgaW52YWxpZGF0ZWQuXG4gICAqL1xuICByZW1vdmVWYWx1ZSh2YWx1ZTogVCk6IG51bWJlciB7XG4gICAgY29uc3QgaXRlbUNtcCA9IHRoaXMuX2l0ZW1DbXA7XG4gICAgY29uc3QgaW5kZXggPSBBcnJheUV4dC5maW5kRmlyc3RJbmRleCh0aGlzLl9hcnJheSwgaXRlbSA9PiB7XG4gICAgICByZXR1cm4gaXRlbUNtcChpdGVtLCB2YWx1ZSk7XG4gICAgfSk7XG4gICAgdGhpcy5yZW1vdmUoaW5kZXgpO1xuICAgIHJldHVybiBpbmRleDtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYW5kIHJldHVybiB0aGUgdmFsdWUgYXQgYSBzcGVjaWZpYyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGluZGV4IC0gVGhlIGluZGV4IG9mIHRoZSB2YWx1ZSBvZiBpbnRlcmVzdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIHZhbHVlIGF0IHRoZSBzcGVjaWZpZWQgaW5kZXgsIG9yIGB1bmRlZmluZWRgIGlmIHRoZVxuICAgKiAgIGluZGV4IGlzIG91dCBvZiByYW5nZS5cbiAgICpcbiAgICogIyMjIyBDb21wbGV4aXR5XG4gICAqIENvbnN0YW50LlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIEl0ZXJhdG9ycyBwb2ludGluZyBhdCB0aGUgcmVtb3ZlZCB2YWx1ZSBhbmQgYmV5b25kIGFyZSBpbnZhbGlkYXRlZC5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3JcbiAgICogQW4gYGluZGV4YCB3aGljaCBpcyBub24taW50ZWdyYWwuXG4gICAqL1xuICByZW1vdmUoaW5kZXg6IG51bWJlcik6IFQgfCB1bmRlZmluZWQge1xuICAgIGNvbnN0IHZhbHVlID0gQXJyYXlFeHQucmVtb3ZlQXQodGhpcy5fYXJyYXksIGluZGV4KTtcbiAgICBpZiAodmFsdWUgPT09IHVuZGVmaW5lZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ3JlbW92ZScsXG4gICAgICBvbGRJbmRleDogaW5kZXgsXG4gICAgICBuZXdJbmRleDogLTEsXG4gICAgICBuZXdWYWx1ZXM6IFtdLFxuICAgICAgb2xkVmFsdWVzOiBbdmFsdWVdXG4gICAgfSk7XG4gICAgcmV0dXJuIHZhbHVlO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhbGwgdmFsdWVzIGZyb20gdGhlIGxpc3QuXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eVxuICAgKiBMaW5lYXIuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogQWxsIGN1cnJlbnQgaXRlcmF0b3JzIGFyZSBpbnZhbGlkYXRlZC5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQge1xuICAgIGNvbnN0IGNvcHkgPSB0aGlzLl9hcnJheS5zbGljZSgpO1xuICAgIHRoaXMuX2FycmF5Lmxlbmd0aCA9IDA7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdyZW1vdmUnLFxuICAgICAgb2xkSW5kZXg6IDAsXG4gICAgICBuZXdJbmRleDogMCxcbiAgICAgIG5ld1ZhbHVlczogW10sXG4gICAgICBvbGRWYWx1ZXM6IGNvcHlcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBNb3ZlIGEgdmFsdWUgZnJvbSBvbmUgaW5kZXggdG8gYW5vdGhlci5cbiAgICpcbiAgICogQHBhcmFtIGZyb21JbmRleCAtIFRoZSBpbmRleCBvZiB0aGUgZWxlbWVudCB0byBtb3ZlLlxuICAgKlxuICAgKiBAcGFyYW0gdG9JbmRleCAtIFRoZSBpbmRleCB0byBtb3ZlIHRoZSBlbGVtZW50IHRvLlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogQ29uc3RhbnQuXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogSXRlcmF0b3JzIHBvaW50aW5nIGF0IHRoZSBsZXNzZXIgb2YgdGhlIGBmcm9tSW5kZXhgIGFuZCB0aGUgYHRvSW5kZXhgXG4gICAqIGFuZCBiZXlvbmQgYXJlIGludmFsaWRhdGVkLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBIGBmcm9tSW5kZXhgIG9yIGEgYHRvSW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIG1vdmUoZnJvbUluZGV4OiBudW1iZXIsIHRvSW5kZXg6IG51bWJlcik6IHZvaWQge1xuICAgIGlmICh0aGlzLmxlbmd0aCA8PSAxIHx8IGZyb21JbmRleCA9PT0gdG9JbmRleCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCB2YWx1ZXMgPSBbdGhpcy5fYXJyYXlbZnJvbUluZGV4XV07XG4gICAgQXJyYXlFeHQubW92ZSh0aGlzLl9hcnJheSwgZnJvbUluZGV4LCB0b0luZGV4KTtcbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ21vdmUnLFxuICAgICAgb2xkSW5kZXg6IGZyb21JbmRleCxcbiAgICAgIG5ld0luZGV4OiB0b0luZGV4LFxuICAgICAgb2xkVmFsdWVzOiB2YWx1ZXMsXG4gICAgICBuZXdWYWx1ZXM6IHZhbHVlc1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFB1c2ggYSBzZXQgb2YgdmFsdWVzIHRvIHRoZSBiYWNrIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWVzIC0gQW4gaXRlcmFibGUgc2V0IG9mIHZhbHVlcyB0byBhZGQuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIEJ5IGNvbnZlbnRpb24sIHRoZSBvbGRJbmRleCBpcyBzZXQgdG8gLTEgdG8gaW5kaWNhdGVcbiAgICogYW4gcHVzaCBvcGVyYXRpb24uXG4gICAqXG4gICAqICMjIyMgSXRlcmF0b3IgVmFsaWRpdHlcbiAgICogTm8gY2hhbmdlcy5cbiAgICovXG4gIHB1c2hBbGwodmFsdWVzOiBJdGVyYWJsZTxUPik6IG51bWJlciB7XG4gICAgY29uc3QgbmV3SW5kZXggPSB0aGlzLmxlbmd0aDtcbiAgICBmb3IgKGNvbnN0IHZhbHVlIG9mIHZhbHVlcykge1xuICAgICAgdGhpcy5fYXJyYXkucHVzaCh2YWx1ZSk7XG4gICAgfVxuICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICB0eXBlOiAnYWRkJyxcbiAgICAgIG9sZEluZGV4OiAtMSxcbiAgICAgIG5ld0luZGV4LFxuICAgICAgb2xkVmFsdWVzOiBbXSxcbiAgICAgIG5ld1ZhbHVlczogQXJyYXkuZnJvbSh2YWx1ZXMpXG4gICAgfSk7XG4gICAgcmV0dXJuIHRoaXMubGVuZ3RoO1xuICB9XG5cbiAgLyoqXG4gICAqIEluc2VydCBhIHNldCBvZiBpdGVtcyBpbnRvIHRoZSBsaXN0IGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBpbmRleCBhdCB3aGljaCB0byBpbnNlcnQgdGhlIHZhbHVlcy5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlcyAtIFRoZSB2YWx1ZXMgdG8gaW5zZXJ0IGF0IHRoZSBzcGVjaWZpZWQgaW5kZXguXG4gICAqXG4gICAqICMjIyMgQ29tcGxleGl0eS5cbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIE5vIGNoYW5nZXMuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhlIGBpbmRleGAgd2lsbCBiZSBjbGFtcGVkIHRvIHRoZSBib3VuZHMgb2YgdGhlIGxpc3QuXG4gICAqIEJ5IGNvbnZlbnRpb24sIHRoZSBvbGRJbmRleCBpcyBzZXQgdG8gLTIgdG8gaW5kaWNhdGVcbiAgICogYW4gaW5zZXJ0IG9wZXJhdGlvbi5cbiAgICpcbiAgICogIyMjIyBVbmRlZmluZWQgQmVoYXZpb3IuXG4gICAqIEFuIGBpbmRleGAgd2hpY2ggaXMgbm9uLWludGVncmFsLlxuICAgKi9cbiAgaW5zZXJ0QWxsKGluZGV4OiBudW1iZXIsIHZhbHVlczogSXRlcmFibGU8VD4pOiB2b2lkIHtcbiAgICBjb25zdCBuZXdJbmRleCA9IGluZGV4O1xuICAgIGZvciAoY29uc3QgdmFsdWUgb2YgdmFsdWVzKSB7XG4gICAgICBBcnJheUV4dC5pbnNlcnQodGhpcy5fYXJyYXksIGluZGV4KyssIHZhbHVlKTtcbiAgICB9XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdhZGQnLFxuICAgICAgb2xkSW5kZXg6IC0yLFxuICAgICAgbmV3SW5kZXgsXG4gICAgICBvbGRWYWx1ZXM6IFtdLFxuICAgICAgbmV3VmFsdWVzOiBBcnJheS5mcm9tKHZhbHVlcylcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSByYW5nZSBvZiBpdGVtcyBmcm9tIHRoZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gc3RhcnRJbmRleCAtIFRoZSBzdGFydCBpbmRleCBvZiB0aGUgcmFuZ2UgdG8gcmVtb3ZlIChpbmNsdXNpdmUpLlxuICAgKlxuICAgKiBAcGFyYW0gZW5kSW5kZXggLSBUaGUgZW5kIGluZGV4IG9mIHRoZSByYW5nZSB0byByZW1vdmUgKGV4Y2x1c2l2ZSkuXG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBuZXcgbGVuZ3RoIG9mIHRoZSBsaXN0LlxuICAgKlxuICAgKiAjIyMjIENvbXBsZXhpdHlcbiAgICogTGluZWFyLlxuICAgKlxuICAgKiAjIyMjIEl0ZXJhdG9yIFZhbGlkaXR5XG4gICAqIEl0ZXJhdG9ycyBwb2ludGluZyB0byB0aGUgZmlyc3QgcmVtb3ZlZCB2YWx1ZSBhbmQgYmV5b25kIGFyZSBpbnZhbGlkLlxuICAgKlxuICAgKiAjIyMjIFVuZGVmaW5lZCBCZWhhdmlvclxuICAgKiBBIGBzdGFydEluZGV4YCBvciBgZW5kSW5kZXhgIHdoaWNoIGlzIG5vbi1pbnRlZ3JhbC5cbiAgICovXG4gIHJlbW92ZVJhbmdlKHN0YXJ0SW5kZXg6IG51bWJlciwgZW5kSW5kZXg6IG51bWJlcik6IG51bWJlciB7XG4gICAgY29uc3Qgb2xkVmFsdWVzID0gdGhpcy5fYXJyYXkuc2xpY2Uoc3RhcnRJbmRleCwgZW5kSW5kZXgpO1xuICAgIGZvciAobGV0IGkgPSBzdGFydEluZGV4OyBpIDwgZW5kSW5kZXg7IGkrKykge1xuICAgICAgQXJyYXlFeHQucmVtb3ZlQXQodGhpcy5fYXJyYXksIHN0YXJ0SW5kZXgpO1xuICAgIH1cbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ3JlbW92ZScsXG4gICAgICBvbGRJbmRleDogc3RhcnRJbmRleCxcbiAgICAgIG5ld0luZGV4OiAtMSxcbiAgICAgIG9sZFZhbHVlcyxcbiAgICAgIG5ld1ZhbHVlczogW11cbiAgICB9KTtcbiAgICByZXR1cm4gdGhpcy5sZW5ndGg7XG4gIH1cblxuICBwcml2YXRlIF9hcnJheTogQXJyYXk8VD4gPSBbXTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xuICBwcml2YXRlIF9pdGVtQ21wOiAoZmlyc3Q6IFQsIHNlY29uZDogVCkgPT4gYm9vbGVhbjtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgSU9ic2VydmFibGVMaXN0LklDaGFuZ2VkQXJnczxUPj4odGhpcyk7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgYE9ic2VydmFibGVMaXN0YCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE9ic2VydmFibGVMaXN0IHtcbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gaW5pdGlhbGl6ZSBhbiBvYnNlcnZhYmxlIG1hcC5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnM8VD4ge1xuICAgIC8qKlxuICAgICAqIEFuIG9wdGlvbmFsIGluaXRpYWwgc2V0IG9mIHZhbHVlcy5cbiAgICAgKi9cbiAgICB2YWx1ZXM/OiBJdGVyYWJsZTxUPjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBpdGVtIGNvbXBhcmlzb24gZnVuY3Rpb24gZm9yIGNoYW5nZSBkZXRlY3Rpb24gb24gYHNldGAuXG4gICAgICpcbiAgICAgKiBJZiBub3QgZ2l2ZW4sIHN0cmljdCBgPT09YCBlcXVhbGl0eSB3aWxsIGJlIHVzZWQuXG4gICAgICovXG4gICAgaXRlbUNtcD86IChmaXJzdDogVCwgc2Vjb25kOiBUKSA9PiBib29sZWFuO1xuICB9XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgbW9kdWxlIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogVGhlIGRlZmF1bHQgc3RyaWN0IGVxdWFsaXR5IGl0ZW0gY21wLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGl0ZW1DbXA8VD4oZmlyc3Q6IFQsIHNlY29uZDogVCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiBmaXJzdCA9PT0gc2Vjb25kO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IElPYnNlcnZhYmxlIH0gZnJvbSAnLi9tb2RlbGRiJztcblxuLyoqXG4gKiBBIG1hcCB3aGljaCBjYW4gYmUgb2JzZXJ2ZWQgZm9yIGNoYW5nZXMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9ic2VydmFibGVNYXA8VD4gZXh0ZW5kcyBJRGlzcG9zYWJsZSwgSU9ic2VydmFibGUge1xuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhlIE9ic2VydmFibGUuXG4gICAqL1xuICB0eXBlOiAnTWFwJztcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBtYXAgaGFzIGNoYW5nZWQuXG4gICAqL1xuICByZWFkb25seSBjaGFuZ2VkOiBJU2lnbmFsPHRoaXMsIElPYnNlcnZhYmxlTWFwLklDaGFuZ2VkQXJnczxUPj47XG5cbiAgLyoqXG4gICAqIFRoZSBudW1iZXIgb2Yga2V5LXZhbHVlIHBhaXJzIGluIHRoZSBtYXAuXG4gICAqL1xuICByZWFkb25seSBzaXplOiBudW1iZXI7XG5cbiAgLyoqXG4gICAqIFNldCBhIGtleS12YWx1ZSBwYWlyIGluIHRoZSBtYXBcbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBrZXkgdG8gc2V0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgZm9yIHRoZSBrZXkuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBvbGQgdmFsdWUgZm9yIHRoZSBrZXksIG9yIHVuZGVmaW5lZFxuICAgKiAgIGlmIHRoYXQgZGlkIG5vdCBleGlzdC5cbiAgICovXG4gIHNldChrZXk6IHN0cmluZywgdmFsdWU6IFQpOiBUIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBHZXQgYSB2YWx1ZSBmb3IgYSBnaXZlbiBrZXkuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSB0aGUga2V5LlxuICAgKlxuICAgKiBAcmV0dXJucyB0aGUgdmFsdWUgZm9yIHRoYXQga2V5LlxuICAgKi9cbiAgZ2V0KGtleTogc3RyaW5nKTogVCB8IHVuZGVmaW5lZDtcblxuICAvKipcbiAgICogQ2hlY2sgd2hldGhlciB0aGUgbWFwIGhhcyBhIGtleS5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIHRoZSBrZXkgdG8gY2hlY2suXG4gICAqXG4gICAqIEByZXR1cm5zIGB0cnVlYCBpZiB0aGUgbWFwIGhhcyB0aGUga2V5LCBgZmFsc2VgIG90aGVyd2lzZS5cbiAgICovXG4gIGhhcyhrZXk6IHN0cmluZyk6IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIGtleXMgaW4gdGhlIG1hcC5cbiAgICpcbiAgICogQHJldHVybnMgLSBhIGxpc3Qgb2Yga2V5cy5cbiAgICovXG4gIGtleXMoKTogc3RyaW5nW107XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIHZhbHVlcyBpbiB0aGUgbWFwLlxuICAgKlxuICAgKiBAcmV0dXJucyAtIGEgbGlzdCBvZiB2YWx1ZXMuXG4gICAqL1xuICB2YWx1ZXMoKTogVFtdO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBrZXkgZnJvbSB0aGUgbWFwXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSB0aGUga2V5IHRvIHJlbW92ZS5cbiAgICpcbiAgICogQHJldHVybnMgdGhlIHZhbHVlIG9mIHRoZSBnaXZlbiBrZXksXG4gICAqICAgb3IgdW5kZWZpbmVkIGlmIHRoYXQgZG9lcyBub3QgZXhpc3QuXG4gICAqL1xuICBkZWxldGUoa2V5OiBzdHJpbmcpOiBUIHwgdW5kZWZpbmVkO1xuXG4gIC8qKlxuICAgKiBTZXQgdGhlIE9ic2VydmFibGVNYXAgdG8gYW4gZW1wdHkgbWFwLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZDtcblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIG1hcC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZDtcbn1cblxuLyoqXG4gKiBUaGUgaW50ZXJmYWNlcyBhc3NvY2lhdGVkIHdpdGggYW4gSU9ic2VydmFibGVNYXAuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSU9ic2VydmFibGVNYXAge1xuICAvKipcbiAgICogVGhlIGNoYW5nZSB0eXBlcyB3aGljaCBvY2N1ciBvbiBhbiBvYnNlcnZhYmxlIG1hcC5cbiAgICovXG4gIGV4cG9ydCB0eXBlIENoYW5nZVR5cGUgPVxuICAgIC8qKlxuICAgICAqIEFuIGVudHJ5IHdhcyBhZGRlZC5cbiAgICAgKi9cbiAgICB8ICdhZGQnXG5cbiAgICAvKipcbiAgICAgKiBBbiBlbnRyeSB3YXMgcmVtb3ZlZC5cbiAgICAgKi9cbiAgICB8ICdyZW1vdmUnXG5cbiAgICAvKipcbiAgICAgKiBBbiBlbnRyeSB3YXMgY2hhbmdlZC5cbiAgICAgKi9cbiAgICB8ICdjaGFuZ2UnO1xuXG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBhcmdzIG9iamVjdCB3aGljaCBpcyBlbWl0dGVkIGJ5IGFuIG9ic2VydmFibGUgbWFwLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ2hhbmdlZEFyZ3M8VD4ge1xuICAgIC8qKlxuICAgICAqIFRoZSB0eXBlIG9mIGNoYW5nZSB1bmRlcmdvbmUgYnkgdGhlIG1hcC5cbiAgICAgKi9cbiAgICB0eXBlOiBDaGFuZ2VUeXBlO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGtleSBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIGtleTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG9sZCB2YWx1ZSBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIG9sZFZhbHVlOiBUIHwgdW5kZWZpbmVkO1xuXG4gICAgLyoqXG4gICAgICogVGhlIG5ldyB2YWx1ZSBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIG5ld1ZhbHVlOiBUIHwgdW5kZWZpbmVkO1xuICB9XG59XG5cbi8qKlxuICogQSBjb25jcmV0ZSBpbXBsZW1lbnRhdGlvbiBvZiBJT2JzZXJ2YWJsZU1hcDxUPi5cbiAqL1xuZXhwb3J0IGNsYXNzIE9ic2VydmFibGVNYXA8VD4gaW1wbGVtZW50cyBJT2JzZXJ2YWJsZU1hcDxUPiB7XG4gIC8qKlxuICAgKiBDb25zdHJ1Y3QgYSBuZXcgb2JzZXJ2YWJsZSBtYXAuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBPYnNlcnZhYmxlTWFwLklPcHRpb25zPFQ+ID0ge30pIHtcbiAgICB0aGlzLl9pdGVtQ21wID0gb3B0aW9ucy5pdGVtQ21wIHx8IFByaXZhdGUuaXRlbUNtcDtcbiAgICBpZiAob3B0aW9ucy52YWx1ZXMpIHtcbiAgICAgIGZvciAoY29uc3Qga2V5IGluIG9wdGlvbnMudmFsdWVzKSB7XG4gICAgICAgIHRoaXMuX21hcC5zZXQoa2V5LCBvcHRpb25zLnZhbHVlc1trZXldKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhlIE9ic2VydmFibGUuXG4gICAqL1xuICBnZXQgdHlwZSgpOiAnTWFwJyB7XG4gICAgcmV0dXJuICdNYXAnO1xuICB9XG5cbiAgLyoqXG4gICAqIEEgc2lnbmFsIGVtaXR0ZWQgd2hlbiB0aGUgbWFwIGhhcyBjaGFuZ2VkLlxuICAgKi9cbiAgZ2V0IGNoYW5nZWQoKTogSVNpZ25hbDx0aGlzLCBJT2JzZXJ2YWJsZU1hcC5JQ2hhbmdlZEFyZ3M8VD4+IHtcbiAgICByZXR1cm4gdGhpcy5fY2hhbmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoaXMgbWFwIGhhcyBiZWVuIGRpc3Bvc2VkLlxuICAgKi9cbiAgZ2V0IGlzRGlzcG9zZWQoKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIHRoaXMuX2lzRGlzcG9zZWQ7XG4gIH1cblxuICAvKipcbiAgICogVGhlIG51bWJlciBvZiBrZXktdmFsdWUgcGFpcnMgaW4gdGhlIG1hcC5cbiAgICovXG4gIGdldCBzaXplKCk6IG51bWJlciB7XG4gICAgcmV0dXJuIHRoaXMuX21hcC5zaXplO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIGtleS12YWx1ZSBwYWlyIGluIHRoZSBtYXBcbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBrZXkgdG8gc2V0LlxuICAgKlxuICAgKiBAcGFyYW0gdmFsdWUgLSBUaGUgdmFsdWUgZm9yIHRoZSBrZXkuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSBvbGQgdmFsdWUgZm9yIHRoZSBrZXksIG9yIHVuZGVmaW5lZFxuICAgKiAgIGlmIHRoYXQgZGlkIG5vdCBleGlzdC5cbiAgICpcbiAgICogQHRocm93cyBpZiB0aGUgbmV3IHZhbHVlIGlzIHVuZGVmaW5lZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGlzIGEgbm8tb3AgaWYgdGhlIHZhbHVlIGRvZXMgbm90IGNoYW5nZS5cbiAgICovXG4gIHNldChrZXk6IHN0cmluZywgdmFsdWU6IFQpOiBUIHwgdW5kZWZpbmVkIHtcbiAgICBjb25zdCBvbGRWYWwgPSB0aGlzLl9tYXAuZ2V0KGtleSk7XG4gICAgaWYgKHZhbHVlID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHRocm93IEVycm9yKCdDYW5ub3Qgc2V0IGFuIHVuZGVmaW5lZCB2YWx1ZSwgdXNlIHJlbW92ZScpO1xuICAgIH1cbiAgICAvLyBCYWlsIGlmIHRoZSB2YWx1ZSBkb2VzIG5vdCBjaGFuZ2UuXG4gICAgY29uc3QgaXRlbUNtcCA9IHRoaXMuX2l0ZW1DbXA7XG4gICAgaWYgKG9sZFZhbCAhPT0gdW5kZWZpbmVkICYmIGl0ZW1DbXAob2xkVmFsLCB2YWx1ZSkpIHtcbiAgICAgIHJldHVybiBvbGRWYWw7XG4gICAgfVxuICAgIHRoaXMuX21hcC5zZXQoa2V5LCB2YWx1ZSk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6IG9sZFZhbCA/ICdjaGFuZ2UnIDogJ2FkZCcsXG4gICAgICBrZXk6IGtleSxcbiAgICAgIG9sZFZhbHVlOiBvbGRWYWwsXG4gICAgICBuZXdWYWx1ZTogdmFsdWVcbiAgICB9KTtcbiAgICByZXR1cm4gb2xkVmFsO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhIHZhbHVlIGZvciBhIGdpdmVuIGtleS5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIHRoZSBrZXkuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSB2YWx1ZSBmb3IgdGhhdCBrZXkuXG4gICAqL1xuICBnZXQoa2V5OiBzdHJpbmcpOiBUIHwgdW5kZWZpbmVkIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmdldChrZXkpO1xuICB9XG5cbiAgLyoqXG4gICAqIENoZWNrIHdoZXRoZXIgdGhlIG1hcCBoYXMgYSBrZXkuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSB0aGUga2V5IHRvIGNoZWNrLlxuICAgKlxuICAgKiBAcmV0dXJucyBgdHJ1ZWAgaWYgdGhlIG1hcCBoYXMgdGhlIGtleSwgYGZhbHNlYCBvdGhlcndpc2UuXG4gICAqL1xuICBoYXMoa2V5OiBzdHJpbmcpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fbWFwLmhhcyhrZXkpO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIGtleXMgaW4gdGhlIG1hcC5cbiAgICpcbiAgICogQHJldHVybnMgLSBhIGxpc3Qgb2Yga2V5cy5cbiAgICovXG4gIGtleXMoKTogc3RyaW5nW10ge1xuICAgIGNvbnN0IGtleUxpc3Q6IHN0cmluZ1tdID0gW107XG4gICAgdGhpcy5fbWFwLmZvckVhY2goKHY6IFQsIGs6IHN0cmluZykgPT4ge1xuICAgICAga2V5TGlzdC5wdXNoKGspO1xuICAgIH0pO1xuICAgIHJldHVybiBrZXlMaXN0O1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBhIGxpc3Qgb2YgdGhlIHZhbHVlcyBpbiB0aGUgbWFwLlxuICAgKlxuICAgKiBAcmV0dXJucyAtIGEgbGlzdCBvZiB2YWx1ZXMuXG4gICAqL1xuICB2YWx1ZXMoKTogVFtdIHtcbiAgICBjb25zdCB2YWxMaXN0OiBUW10gPSBbXTtcbiAgICB0aGlzLl9tYXAuZm9yRWFjaCgodjogVCwgazogc3RyaW5nKSA9PiB7XG4gICAgICB2YWxMaXN0LnB1c2godik7XG4gICAgfSk7XG4gICAgcmV0dXJuIHZhbExpc3Q7XG4gIH1cblxuICAvKipcbiAgICogUmVtb3ZlIGEga2V5IGZyb20gdGhlIG1hcFxuICAgKlxuICAgKiBAcGFyYW0ga2V5IC0gdGhlIGtleSB0byByZW1vdmUuXG4gICAqXG4gICAqIEByZXR1cm5zIHRoZSB2YWx1ZSBvZiB0aGUgZ2l2ZW4ga2V5LFxuICAgKiAgIG9yIHVuZGVmaW5lZCBpZiB0aGF0IGRvZXMgbm90IGV4aXN0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgaXMgYSBuby1vcCBpZiB0aGUgdmFsdWUgZG9lcyBub3QgY2hhbmdlLlxuICAgKi9cbiAgZGVsZXRlKGtleTogc3RyaW5nKTogVCB8IHVuZGVmaW5lZCB7XG4gICAgY29uc3Qgb2xkVmFsID0gdGhpcy5fbWFwLmdldChrZXkpO1xuICAgIGNvbnN0IHJlbW92ZWQgPSB0aGlzLl9tYXAuZGVsZXRlKGtleSk7XG4gICAgaWYgKHJlbW92ZWQpIHtcbiAgICAgIHRoaXMuX2NoYW5nZWQuZW1pdCh7XG4gICAgICAgIHR5cGU6ICdyZW1vdmUnLFxuICAgICAgICBrZXk6IGtleSxcbiAgICAgICAgb2xkVmFsdWU6IG9sZFZhbCxcbiAgICAgICAgbmV3VmFsdWU6IHVuZGVmaW5lZFxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiBvbGRWYWw7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSBPYnNlcnZhYmxlTWFwIHRvIGFuIGVtcHR5IG1hcC5cbiAgICovXG4gIGNsZWFyKCk6IHZvaWQge1xuICAgIC8vIERlbGV0ZSBvbmUgYnkgb25lIHRvIGVtaXQgdGhlIGNvcnJlY3Qgc2lnbmFscy5cbiAgICBjb25zdCBrZXlMaXN0ID0gdGhpcy5rZXlzKCk7XG4gICAgZm9yIChsZXQgaSA9IDA7IGkgPCBrZXlMaXN0Lmxlbmd0aDsgaSsrKSB7XG4gICAgICB0aGlzLmRlbGV0ZShrZXlMaXN0W2ldKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIG1hcC5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICAgIHRoaXMuX21hcC5jbGVhcigpO1xuICB9XG5cbiAgcHJpdmF0ZSBfbWFwOiBNYXA8c3RyaW5nLCBUPiA9IG5ldyBNYXA8c3RyaW5nLCBUPigpO1xuICBwcml2YXRlIF9pdGVtQ21wOiAoZmlyc3Q6IFQsIHNlY29uZDogVCkgPT4gYm9vbGVhbjtcbiAgcHJpdmF0ZSBfY2hhbmdlZCA9IG5ldyBTaWduYWw8dGhpcywgSU9ic2VydmFibGVNYXAuSUNoYW5nZWRBcmdzPFQ+Pih0aGlzKTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xufVxuXG4vKipcbiAqIFRoZSBuYW1lc3BhY2UgZm9yIGBPYnNlcnZhYmxlTWFwYCBjbGFzcyBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIE9ic2VydmFibGVNYXAge1xuICAvKipcbiAgICogVGhlIG9wdGlvbnMgdXNlZCB0byBpbml0aWFsaXplIGFuIG9ic2VydmFibGUgbWFwLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9uczxUPiB7XG4gICAgLyoqXG4gICAgICogQW4gb3B0aW9uYWwgaW5pdGlhbCBzZXQgb2YgdmFsdWVzLlxuICAgICAqL1xuICAgIHZhbHVlcz86IHsgW2tleTogc3RyaW5nXTogVCB9O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGl0ZW0gY29tcGFyaXNvbiBmdW5jdGlvbiBmb3IgY2hhbmdlIGRldGVjdGlvbiBvbiBgc2V0YC5cbiAgICAgKlxuICAgICAqIElmIG5vdCBnaXZlbiwgc3RyaWN0IGA9PT1gIGVxdWFsaXR5IHdpbGwgYmUgdXNlZC5cbiAgICAgKi9cbiAgICBpdGVtQ21wPzogKGZpcnN0OiBULCBzZWNvbmQ6IFQpID0+IGJvb2xlYW47XG4gIH1cbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBtb2R1bGUgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBUaGUgZGVmYXVsdCBzdHJpY3QgZXF1YWxpdHkgaXRlbSBjb21wYXJhdG9yLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIGl0ZW1DbXA8VD4oZmlyc3Q6IFQsIHNlY29uZDogVCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiBmaXJzdCA9PT0gc2Vjb25kO1xuICB9XG59XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwsIFNpZ25hbCB9IGZyb20gJ0BsdW1pbm8vc2lnbmFsaW5nJztcbmltcG9ydCB7IElPYnNlcnZhYmxlIH0gZnJvbSAnLi9tb2RlbGRiJztcblxuLyoqXG4gKiBBIHN0cmluZyB3aGljaCBjYW4gYmUgb2JzZXJ2ZWQgZm9yIGNoYW5nZXMuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSU9ic2VydmFibGVTdHJpbmcgZXh0ZW5kcyBJRGlzcG9zYWJsZSwgSU9ic2VydmFibGUge1xuICAvKipcbiAgICogVGhlIHR5cGUgb2YgdGhlIE9ic2VydmFibGUuXG4gICAqL1xuICB0eXBlOiAnU3RyaW5nJztcblxuICAvKipcbiAgICogQSBzaWduYWwgZW1pdHRlZCB3aGVuIHRoZSBzdHJpbmcgaGFzIGNoYW5nZWQuXG4gICAqL1xuICByZWFkb25seSBjaGFuZ2VkOiBJU2lnbmFsPHRoaXMsIElPYnNlcnZhYmxlU3RyaW5nLklDaGFuZ2VkQXJncz47XG5cbiAgLyoqXG4gICAqIFRoZSB2YWx1ZSBvZiB0aGUgc3RyaW5nLlxuICAgKi9cbiAgdGV4dDogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBJbnNlcnQgYSBzdWJzdHJpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBzdGFydGluZyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIHRleHQgLSBUaGUgc3Vic3RyaW5nIHRvIGluc2VydC5cbiAgICovXG4gIGluc2VydChpbmRleDogbnVtYmVyLCB0ZXh0OiBzdHJpbmcpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBzdWJzdHJpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBzdGFydCAtIFRoZSBzdGFydGluZyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGVuZCAtIFRoZSBlbmRpbmcgaW5kZXguXG4gICAqL1xuICByZW1vdmUoc3RhcnQ6IG51bWJlciwgZW5kOiBudW1iZXIpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBTZXQgdGhlIE9ic2VydmFibGVTdHJpbmcgdG8gYW4gZW1wdHkgc3RyaW5nLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZDtcblxuICAvKipcbiAgICogRGlzcG9zZSBvZiB0aGUgcmVzb3VyY2VzIGhlbGQgYnkgdGhlIHN0cmluZy5cbiAgICovXG4gIGRpc3Bvc2UoKTogdm9pZDtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBgSU9ic2VydmFibGVTdHJpbmdgIGFzc29jaWF0ZSBpbnRlcmZhY2VzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIElPYnNlcnZhYmxlU3RyaW5nIHtcbiAgLyoqXG4gICAqIFRoZSBjaGFuZ2UgdHlwZXMgd2hpY2ggb2NjdXIgb24gYW4gb2JzZXJ2YWJsZSBzdHJpbmcuXG4gICAqL1xuICBleHBvcnQgdHlwZSBDaGFuZ2VUeXBlID1cbiAgICAvKipcbiAgICAgKiBUZXh0IHdhcyBpbnNlcnRlZC5cbiAgICAgKi9cbiAgICB8ICdpbnNlcnQnXG5cbiAgICAvKipcbiAgICAgKiBUZXh0IHdhcyByZW1vdmVkLlxuICAgICAqL1xuICAgIHwgJ3JlbW92ZSdcblxuICAgIC8qKlxuICAgICAqIFRleHQgd2FzIHNldC5cbiAgICAgKi9cbiAgICB8ICdzZXQnO1xuXG4gIC8qKlxuICAgKiBUaGUgY2hhbmdlZCBhcmdzIG9iamVjdCB3aGljaCBpcyBlbWl0dGVkIGJ5IGFuIG9ic2VydmFibGUgc3RyaW5nLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJQ2hhbmdlZEFyZ3Mge1xuICAgIC8qKlxuICAgICAqIFRoZSB0eXBlIG9mIGNoYW5nZSB1bmRlcmdvbmUgYnkgdGhlIGxpc3QuXG4gICAgICovXG4gICAgdHlwZTogQ2hhbmdlVHlwZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBzdGFydGluZyBpbmRleCBvZiB0aGUgY2hhbmdlLlxuICAgICAqL1xuICAgIHN0YXJ0OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZW5kIGluZGV4IG9mIHRoZSBjaGFuZ2UuXG4gICAgICovXG4gICAgZW5kOiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdmFsdWUgb2YgdGhlIGNoYW5nZS5cbiAgICAgKlxuICAgICAqICMjIyBOb3Rlc1xuICAgICAqIElmIGBDaGFuZ2VUeXBlYCBpcyBgc2V0YCwgdGhlblxuICAgICAqIHRoaXMgaXMgdGhlIG5ldyB2YWx1ZSBvZiB0aGUgc3RyaW5nLlxuICAgICAqXG4gICAgICogSWYgYENoYW5nZVR5cGVgIGlzIGBpbnNlcnRgIHRoaXMgaXNcbiAgICAgKiB0aGUgdmFsdWUgb2YgdGhlIGluc2VydGVkIHN0cmluZy5cbiAgICAgKlxuICAgICAqIElmIGBDaGFuZ2VUeXBlYCBpcyByZW1vdmUgdGhpcyBpcyB0aGVcbiAgICAgKiB2YWx1ZSBvZiB0aGUgcmVtb3ZlZCBzdWJzdHJpbmcuXG4gICAgICovXG4gICAgdmFsdWU6IHN0cmluZztcbiAgfVxufVxuXG4vKipcbiAqIEEgY29uY3JldGUgaW1wbGVtZW50YXRpb24gb2YgW1tJT2JzZXJ2YWJsZVN0cmluZ11dXG4gKi9cbmV4cG9ydCBjbGFzcyBPYnNlcnZhYmxlU3RyaW5nIGltcGxlbWVudHMgSU9ic2VydmFibGVTdHJpbmcge1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IG9ic2VydmFibGUgc3RyaW5nLlxuICAgKi9cbiAgY29uc3RydWN0b3IoaW5pdGlhbFRleHQ6IHN0cmluZyA9ICcnKSB7XG4gICAgdGhpcy5fdGV4dCA9IGluaXRpYWxUZXh0O1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSB0eXBlIG9mIHRoZSBPYnNlcnZhYmxlLlxuICAgKi9cbiAgZ2V0IHR5cGUoKTogJ1N0cmluZycge1xuICAgIHJldHVybiAnU3RyaW5nJztcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCBlbWl0dGVkIHdoZW4gdGhlIHN0cmluZyBoYXMgY2hhbmdlZC5cbiAgICovXG4gIGdldCBjaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgSU9ic2VydmFibGVTdHJpbmcuSUNoYW5nZWRBcmdzPiB7XG4gICAgcmV0dXJuIHRoaXMuX2NoYW5nZWQ7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRoZSB2YWx1ZSBvZiB0aGUgc3RyaW5nLlxuICAgKi9cbiAgc2V0IHRleHQodmFsdWU6IHN0cmluZykge1xuICAgIGlmICh2YWx1ZS5sZW5ndGggPT09IHRoaXMuX3RleHQubGVuZ3RoICYmIHZhbHVlID09PSB0aGlzLl90ZXh0KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX3RleHQgPSB2YWx1ZTtcbiAgICB0aGlzLl9jaGFuZ2VkLmVtaXQoe1xuICAgICAgdHlwZTogJ3NldCcsXG4gICAgICBzdGFydDogMCxcbiAgICAgIGVuZDogdmFsdWUubGVuZ3RoLFxuICAgICAgdmFsdWU6IHZhbHVlXG4gICAgfSk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IHRoZSB2YWx1ZSBvZiB0aGUgc3RyaW5nLlxuICAgKi9cbiAgZ2V0IHRleHQoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fdGV4dDtcbiAgfVxuXG4gIC8qKlxuICAgKiBJbnNlcnQgYSBzdWJzdHJpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBpbmRleCAtIFRoZSBzdGFydGluZyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIHRleHQgLSBUaGUgc3Vic3RyaW5nIHRvIGluc2VydC5cbiAgICovXG4gIGluc2VydChpbmRleDogbnVtYmVyLCB0ZXh0OiBzdHJpbmcpOiB2b2lkIHtcbiAgICB0aGlzLl90ZXh0ID0gdGhpcy5fdGV4dC5zbGljZSgwLCBpbmRleCkgKyB0ZXh0ICsgdGhpcy5fdGV4dC5zbGljZShpbmRleCk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdpbnNlcnQnLFxuICAgICAgc3RhcnQ6IGluZGV4LFxuICAgICAgZW5kOiBpbmRleCArIHRleHQubGVuZ3RoLFxuICAgICAgdmFsdWU6IHRleHRcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBzdWJzdHJpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBzdGFydCAtIFRoZSBzdGFydGluZyBpbmRleC5cbiAgICpcbiAgICogQHBhcmFtIGVuZCAtIFRoZSBlbmRpbmcgaW5kZXguXG4gICAqL1xuICByZW1vdmUoc3RhcnQ6IG51bWJlciwgZW5kOiBudW1iZXIpOiB2b2lkIHtcbiAgICBjb25zdCBvbGRWYWx1ZTogc3RyaW5nID0gdGhpcy5fdGV4dC5zbGljZShzdGFydCwgZW5kKTtcbiAgICB0aGlzLl90ZXh0ID0gdGhpcy5fdGV4dC5zbGljZSgwLCBzdGFydCkgKyB0aGlzLl90ZXh0LnNsaWNlKGVuZCk7XG4gICAgdGhpcy5fY2hhbmdlZC5lbWl0KHtcbiAgICAgIHR5cGU6ICdyZW1vdmUnLFxuICAgICAgc3RhcnQ6IHN0YXJ0LFxuICAgICAgZW5kOiBlbmQsXG4gICAgICB2YWx1ZTogb2xkVmFsdWVcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgdGhlIE9ic2VydmFibGVTdHJpbmcgdG8gYW4gZW1wdHkgc3RyaW5nLlxuICAgKi9cbiAgY2xlYXIoKTogdm9pZCB7XG4gICAgdGhpcy50ZXh0ID0gJyc7XG4gIH1cblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSBzdHJpbmcgaGFzIGJlZW4gZGlzcG9zZWQuXG4gICAqL1xuICBnZXQgaXNEaXNwb3NlZCgpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faXNEaXNwb3NlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSByZXNvdXJjZXMgaGVsZCBieSB0aGUgc3RyaW5nLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5faXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICB0aGlzLl9pc0Rpc3Bvc2VkID0gdHJ1ZTtcbiAgICBTaWduYWwuY2xlYXJEYXRhKHRoaXMpO1xuICAgIHRoaXMuY2xlYXIoKTtcbiAgfVxuXG4gIHByaXZhdGUgX3RleHQgPSAnJztcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZDogYm9vbGVhbiA9IGZhbHNlO1xuICBwcml2YXRlIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCBJT2JzZXJ2YWJsZVN0cmluZy5JQ2hhbmdlZEFyZ3M+KHRoaXMpO1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBKU09OVmFsdWUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBJT2JzZXJ2YWJsZUxpc3QsIE9ic2VydmFibGVMaXN0IH0gZnJvbSAnLi9vYnNlcnZhYmxlbGlzdCc7XG5cbi8qKlxuICogQW4gb2JqZWN0IHdoaWNoIGtub3dzIGhvdyB0byBzZXJpYWxpemUgYW5kXG4gKiBkZXNlcmlhbGl6ZSB0aGUgdHlwZSBULlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElTZXJpYWxpemVyPFQ+IHtcbiAgLyoqXG4gICAqIENvbnZlcnQgdGhlIG9iamVjdCB0byBKU09OLlxuICAgKi9cbiAgdG9KU09OKHZhbHVlOiBUKTogSlNPTlZhbHVlO1xuXG4gIC8qKlxuICAgKiBEZXNlcmlhbGl6ZSB0aGUgb2JqZWN0IGZyb20gSlNPTi5cbiAgICovXG4gIGZyb21KU09OKHZhbHVlOiBKU09OVmFsdWUpOiBUO1xufVxuXG4vKipcbiAqIEFuIG9ic2VydmFibGUgbGlzdCB0aGF0IHN1cHBvcnRzIHVuZG8vcmVkby5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJT2JzZXJ2YWJsZVVuZG9hYmxlTGlzdDxUPiBleHRlbmRzIElPYnNlcnZhYmxlTGlzdDxUPiB7XG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBvYmplY3QgY2FuIHJlZG8gY2hhbmdlcy5cbiAgICovXG4gIHJlYWRvbmx5IGNhblJlZG86IGJvb2xlYW47XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlIG9iamVjdCBjYW4gdW5kbyBjaGFuZ2VzLlxuICAgKi9cbiAgcmVhZG9ubHkgY2FuVW5kbzogYm9vbGVhbjtcblxuICAvKipcbiAgICogQmVnaW4gYSBjb21wb3VuZCBvcGVyYXRpb24uXG4gICAqXG4gICAqIEBwYXJhbSBpc1VuZG9BYmxlIC0gV2hldGhlciB0aGUgb3BlcmF0aW9uIGlzIHVuZG9hYmxlLlxuICAgKiAgIFRoZSBkZWZhdWx0IGlzIGBmYWxzZWAuXG4gICAqL1xuICBiZWdpbkNvbXBvdW5kT3BlcmF0aW9uKGlzVW5kb0FibGU/OiBib29sZWFuKTogdm9pZDtcblxuICAvKipcbiAgICogRW5kIGEgY29tcG91bmQgb3BlcmF0aW9uLlxuICAgKi9cbiAgZW5kQ29tcG91bmRPcGVyYXRpb24oKTogdm9pZDtcblxuICAvKipcbiAgICogVW5kbyBhbiBvcGVyYXRpb24uXG4gICAqL1xuICB1bmRvKCk6IHZvaWQ7XG5cbiAgLyoqXG4gICAqIFJlZG8gYW4gb3BlcmF0aW9uLlxuICAgKi9cbiAgcmVkbygpOiB2b2lkO1xuXG4gIC8qKlxuICAgKiBDbGVhciB0aGUgY2hhbmdlIHN0YWNrLlxuICAgKi9cbiAgY2xlYXJVbmRvKCk6IHZvaWQ7XG59XG5cbi8qKlxuICogQSBjb25jcmV0ZSBpbXBsZW1lbnRhdGlvbiBvZiBhbiBvYnNlcnZhYmxlIHVuZG9hYmxlIGxpc3QuXG4gKi9cbmV4cG9ydCBjbGFzcyBPYnNlcnZhYmxlVW5kb2FibGVMaXN0PFQ+XG4gIGV4dGVuZHMgT2JzZXJ2YWJsZUxpc3Q8VD5cbiAgaW1wbGVtZW50cyBJT2JzZXJ2YWJsZVVuZG9hYmxlTGlzdDxUPlxue1xuICAvKipcbiAgICogQ29uc3RydWN0IGEgbmV3IHVuZG9hYmxlIG9ic2VydmFibGUgbGlzdC5cbiAgICovXG4gIGNvbnN0cnVjdG9yKHNlcmlhbGl6ZXI6IElTZXJpYWxpemVyPFQ+KSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl9zZXJpYWxpemVyID0gc2VyaWFsaXplcjtcbiAgICB0aGlzLmNoYW5nZWQuY29ubmVjdCh0aGlzLl9vbkxpc3RDaGFuZ2VkLCB0aGlzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBXaGV0aGVyIHRoZSBvYmplY3QgY2FuIHJlZG8gY2hhbmdlcy5cbiAgICovXG4gIGdldCBjYW5SZWRvKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pbmRleCA8IHRoaXMuX3N0YWNrLmxlbmd0aCAtIDE7XG4gIH1cblxuICAvKipcbiAgICogV2hldGhlciB0aGUgb2JqZWN0IGNhbiB1bmRvIGNoYW5nZXMuXG4gICAqL1xuICBnZXQgY2FuVW5kbygpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5faW5kZXggPj0gMDtcbiAgfVxuXG4gIC8qKlxuICAgKiBCZWdpbiBhIGNvbXBvdW5kIG9wZXJhdGlvbi5cbiAgICpcbiAgICogQHBhcmFtIGlzVW5kb0FibGUgLSBXaGV0aGVyIHRoZSBvcGVyYXRpb24gaXMgdW5kb2FibGUuXG4gICAqICAgVGhlIGRlZmF1bHQgaXMgYHRydWVgLlxuICAgKi9cbiAgYmVnaW5Db21wb3VuZE9wZXJhdGlvbihpc1VuZG9BYmxlPzogYm9vbGVhbik6IHZvaWQge1xuICAgIHRoaXMuX2luQ29tcG91bmQgPSB0cnVlO1xuICAgIHRoaXMuX2lzVW5kb2FibGUgPSBpc1VuZG9BYmxlICE9PSBmYWxzZTtcbiAgICB0aGlzLl9tYWRlQ29tcG91bmRDaGFuZ2UgPSBmYWxzZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBFbmQgYSBjb21wb3VuZCBvcGVyYXRpb24uXG4gICAqL1xuICBlbmRDb21wb3VuZE9wZXJhdGlvbigpOiB2b2lkIHtcbiAgICB0aGlzLl9pbkNvbXBvdW5kID0gZmFsc2U7XG4gICAgdGhpcy5faXNVbmRvYWJsZSA9IHRydWU7XG4gICAgaWYgKHRoaXMuX21hZGVDb21wb3VuZENoYW5nZSkge1xuICAgICAgdGhpcy5faW5kZXgrKztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVW5kbyBhbiBvcGVyYXRpb24uXG4gICAqL1xuICB1bmRvKCk6IHZvaWQge1xuICAgIGlmICghdGhpcy5jYW5VbmRvKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGNvbnN0IGNoYW5nZXMgPSB0aGlzLl9zdGFja1t0aGlzLl9pbmRleF07XG4gICAgdGhpcy5faXNVbmRvYWJsZSA9IGZhbHNlO1xuICAgIGZvciAoY29uc3QgY2hhbmdlIG9mIGNoYW5nZXMucmV2ZXJzZSgpKSB7XG4gICAgICB0aGlzLl91bmRvQ2hhbmdlKGNoYW5nZSk7XG4gICAgfVxuICAgIHRoaXMuX2lzVW5kb2FibGUgPSB0cnVlO1xuICAgIHRoaXMuX2luZGV4LS07XG4gIH1cblxuICAvKipcbiAgICogUmVkbyBhbiBvcGVyYXRpb24uXG4gICAqL1xuICByZWRvKCk6IHZvaWQge1xuICAgIGlmICghdGhpcy5jYW5SZWRvKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIHRoaXMuX2luZGV4Kys7XG4gICAgY29uc3QgY2hhbmdlcyA9IHRoaXMuX3N0YWNrW3RoaXMuX2luZGV4XTtcbiAgICB0aGlzLl9pc1VuZG9hYmxlID0gZmFsc2U7XG4gICAgZm9yIChjb25zdCBjaGFuZ2Ugb2YgY2hhbmdlcykge1xuICAgICAgdGhpcy5fcmVkb0NoYW5nZShjaGFuZ2UpO1xuICAgIH1cbiAgICB0aGlzLl9pc1VuZG9hYmxlID0gdHJ1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhciB0aGUgY2hhbmdlIHN0YWNrLlxuICAgKi9cbiAgY2xlYXJVbmRvKCk6IHZvaWQge1xuICAgIHRoaXMuX2luZGV4ID0gLTE7XG4gICAgdGhpcy5fc3RhY2sgPSBbXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBIYW5kbGUgYSBjaGFuZ2UgaW4gdGhlIGxpc3QuXG4gICAqL1xuICBwcml2YXRlIF9vbkxpc3RDaGFuZ2VkKFxuICAgIGxpc3Q6IElPYnNlcnZhYmxlTGlzdDxUPixcbiAgICBjaGFuZ2U6IElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8VD5cbiAgKTogdm9pZCB7XG4gICAgaWYgKHRoaXMuaXNEaXNwb3NlZCB8fCAhdGhpcy5faXNVbmRvYWJsZSkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICAvLyBDbGVhciBldmVyeXRoaW5nIGFmdGVyIHRoaXMgcG9zaXRpb24gaWYgbmVjZXNzYXJ5LlxuICAgIGlmICghdGhpcy5faW5Db21wb3VuZCB8fCAhdGhpcy5fbWFkZUNvbXBvdW5kQ2hhbmdlKSB7XG4gICAgICB0aGlzLl9zdGFjayA9IHRoaXMuX3N0YWNrLnNsaWNlKDAsIHRoaXMuX2luZGV4ICsgMSk7XG4gICAgfVxuICAgIC8vIENvcHkgdGhlIGNoYW5nZS5cbiAgICBjb25zdCBldnQgPSB0aGlzLl9jb3B5Q2hhbmdlKGNoYW5nZSk7XG4gICAgLy8gUHV0IHRoZSBjaGFuZ2UgaW4gdGhlIHN0YWNrLlxuICAgIGlmICh0aGlzLl9zdGFja1t0aGlzLl9pbmRleCArIDFdKSB7XG4gICAgICB0aGlzLl9zdGFja1t0aGlzLl9pbmRleCArIDFdLnB1c2goZXZ0KTtcbiAgICB9IGVsc2Uge1xuICAgICAgdGhpcy5fc3RhY2sucHVzaChbZXZ0XSk7XG4gICAgfVxuICAgIC8vIElmIG5vdCBpbiBhIGNvbXBvdW5kIG9wZXJhdGlvbiwgaW5jcmVhc2UgaW5kZXguXG4gICAgaWYgKCF0aGlzLl9pbkNvbXBvdW5kKSB7XG4gICAgICB0aGlzLl9pbmRleCsrO1xuICAgIH0gZWxzZSB7XG4gICAgICB0aGlzLl9tYWRlQ29tcG91bmRDaGFuZ2UgPSB0cnVlO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBVbmRvIGEgY2hhbmdlIGV2ZW50LlxuICAgKi9cbiAgcHJpdmF0ZSBfdW5kb0NoYW5nZShjaGFuZ2U6IElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8SlNPTlZhbHVlPik6IHZvaWQge1xuICAgIGxldCBpbmRleCA9IDA7XG4gICAgY29uc3Qgc2VyaWFsaXplciA9IHRoaXMuX3NlcmlhbGl6ZXI7XG4gICAgc3dpdGNoIChjaGFuZ2UudHlwZSkge1xuICAgICAgY2FzZSAnYWRkJzpcbiAgICAgICAgZm9yIChsZXQgbGVuZ3RoID0gY2hhbmdlLm5ld1ZhbHVlcy5sZW5ndGg7IGxlbmd0aCA+IDA7IGxlbmd0aC0tKSB7XG4gICAgICAgICAgdGhpcy5yZW1vdmUoY2hhbmdlLm5ld0luZGV4KTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3NldCc6XG4gICAgICAgIGluZGV4ID0gY2hhbmdlLm9sZEluZGV4O1xuICAgICAgICBmb3IgKGNvbnN0IHZhbHVlIG9mIGNoYW5nZS5vbGRWYWx1ZXMpIHtcbiAgICAgICAgICB0aGlzLnNldChpbmRleCsrLCBzZXJpYWxpemVyLmZyb21KU09OKHZhbHVlKSk7XG4gICAgICAgIH1cbiAgICAgICAgYnJlYWs7XG4gICAgICBjYXNlICdyZW1vdmUnOlxuICAgICAgICBpbmRleCA9IGNoYW5nZS5vbGRJbmRleDtcbiAgICAgICAgZm9yIChjb25zdCB2YWx1ZSBvZiBjaGFuZ2Uub2xkVmFsdWVzKSB7XG4gICAgICAgICAgdGhpcy5pbnNlcnQoaW5kZXgrKywgc2VyaWFsaXplci5mcm9tSlNPTih2YWx1ZSkpO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAnbW92ZSc6XG4gICAgICAgIHRoaXMubW92ZShjaGFuZ2UubmV3SW5kZXgsIGNoYW5nZS5vbGRJbmRleCk7XG4gICAgICAgIGJyZWFrO1xuICAgICAgZGVmYXVsdDpcbiAgICAgICAgcmV0dXJuO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBSZWRvIGEgY2hhbmdlIGV2ZW50LlxuICAgKi9cbiAgcHJpdmF0ZSBfcmVkb0NoYW5nZShjaGFuZ2U6IElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8SlNPTlZhbHVlPik6IHZvaWQge1xuICAgIGxldCBpbmRleCA9IDA7XG4gICAgY29uc3Qgc2VyaWFsaXplciA9IHRoaXMuX3NlcmlhbGl6ZXI7XG4gICAgc3dpdGNoIChjaGFuZ2UudHlwZSkge1xuICAgICAgY2FzZSAnYWRkJzpcbiAgICAgICAgaW5kZXggPSBjaGFuZ2UubmV3SW5kZXg7XG4gICAgICAgIGZvciAoY29uc3QgdmFsdWUgb2YgY2hhbmdlLm5ld1ZhbHVlcykge1xuICAgICAgICAgIHRoaXMuaW5zZXJ0KGluZGV4KyssIHNlcmlhbGl6ZXIuZnJvbUpTT04odmFsdWUpKTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ3NldCc6XG4gICAgICAgIGluZGV4ID0gY2hhbmdlLm5ld0luZGV4O1xuICAgICAgICBmb3IgKGNvbnN0IHZhbHVlIG9mIGNoYW5nZS5uZXdWYWx1ZXMpIHtcbiAgICAgICAgICB0aGlzLnNldChjaGFuZ2UubmV3SW5kZXgrKywgc2VyaWFsaXplci5mcm9tSlNPTih2YWx1ZSkpO1xuICAgICAgICB9XG4gICAgICAgIGJyZWFrO1xuICAgICAgY2FzZSAncmVtb3ZlJzpcbiAgICAgICAgZm9yIChsZXQgbGVuZ3RoID0gY2hhbmdlLm9sZFZhbHVlcy5sZW5ndGg7IGxlbmd0aCA+IDA7IGxlbmd0aC0tKSB7XG4gICAgICAgICAgdGhpcy5yZW1vdmUoY2hhbmdlLm9sZEluZGV4KTtcbiAgICAgICAgfVxuICAgICAgICBicmVhaztcbiAgICAgIGNhc2UgJ21vdmUnOlxuICAgICAgICB0aGlzLm1vdmUoY2hhbmdlLm9sZEluZGV4LCBjaGFuZ2UubmV3SW5kZXgpO1xuICAgICAgICBicmVhaztcbiAgICAgIGRlZmF1bHQ6XG4gICAgICAgIHJldHVybjtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogQ29weSBhIGNoYW5nZSBhcyBKU09OLlxuICAgKi9cbiAgcHJpdmF0ZSBfY29weUNoYW5nZShcbiAgICBjaGFuZ2U6IElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8VD5cbiAgKTogSU9ic2VydmFibGVMaXN0LklDaGFuZ2VkQXJnczxKU09OVmFsdWU+IHtcbiAgICBjb25zdCBvbGRWYWx1ZXM6IEpTT05WYWx1ZVtdID0gW107XG4gICAgZm9yIChjb25zdCB2YWx1ZSBvZiBjaGFuZ2Uub2xkVmFsdWVzKSB7XG4gICAgICBvbGRWYWx1ZXMucHVzaCh0aGlzLl9zZXJpYWxpemVyLnRvSlNPTih2YWx1ZSkpO1xuICAgIH1cbiAgICBjb25zdCBuZXdWYWx1ZXM6IEpTT05WYWx1ZVtdID0gW107XG4gICAgZm9yIChjb25zdCB2YWx1ZSBvZiBjaGFuZ2UubmV3VmFsdWVzKSB7XG4gICAgICBuZXdWYWx1ZXMucHVzaCh0aGlzLl9zZXJpYWxpemVyLnRvSlNPTih2YWx1ZSkpO1xuICAgIH1cbiAgICByZXR1cm4ge1xuICAgICAgdHlwZTogY2hhbmdlLnR5cGUsXG4gICAgICBvbGRJbmRleDogY2hhbmdlLm9sZEluZGV4LFxuICAgICAgbmV3SW5kZXg6IGNoYW5nZS5uZXdJbmRleCxcbiAgICAgIG9sZFZhbHVlcyxcbiAgICAgIG5ld1ZhbHVlc1xuICAgIH07XG4gIH1cblxuICBwcml2YXRlIF9pbkNvbXBvdW5kID0gZmFsc2U7XG4gIHByaXZhdGUgX2lzVW5kb2FibGUgPSB0cnVlO1xuICBwcml2YXRlIF9tYWRlQ29tcG91bmRDaGFuZ2UgPSBmYWxzZTtcbiAgcHJpdmF0ZSBfaW5kZXggPSAtMTtcbiAgcHJpdmF0ZSBfc3RhY2s6IElPYnNlcnZhYmxlTGlzdC5JQ2hhbmdlZEFyZ3M8SlNPTlZhbHVlPltdW10gPSBbXTtcbiAgcHJpdmF0ZSBfc2VyaWFsaXplcjogSVNlcmlhbGl6ZXI8VD47XG59XG5cbi8qKlxuICogTmFtZXNwYWNlIGZvciBPYnNlcnZhYmxlVW5kb2FibGVMaXN0IHV0aWxpdGllcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBPYnNlcnZhYmxlVW5kb2FibGVMaXN0IHtcbiAgLyoqXG4gICAqIEEgZGVmYXVsdCwgaWRlbnRpdHkgc2VyaWFsaXplci5cbiAgICovXG4gIGV4cG9ydCBjbGFzcyBJZGVudGl0eVNlcmlhbGl6ZXI8VCBleHRlbmRzIEpTT05WYWx1ZT5cbiAgICBpbXBsZW1lbnRzIElTZXJpYWxpemVyPFQ+XG4gIHtcbiAgICAvKipcbiAgICAgKiBJZGVudGl0eSBzZXJpYWxpemUuXG4gICAgICovXG4gICAgdG9KU09OKHZhbHVlOiBUKTogSlNPTlZhbHVlIHtcbiAgICAgIHJldHVybiB2YWx1ZTtcbiAgICB9XG5cbiAgICAvKipcbiAgICAgKiBJZGVudGl0eSBkZXNlcmlhbGl6ZS5cbiAgICAgKi9cbiAgICBmcm9tSlNPTih2YWx1ZTogSlNPTlZhbHVlKTogVCB7XG4gICAgICByZXR1cm4gdmFsdWUgYXMgVDtcbiAgICB9XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==