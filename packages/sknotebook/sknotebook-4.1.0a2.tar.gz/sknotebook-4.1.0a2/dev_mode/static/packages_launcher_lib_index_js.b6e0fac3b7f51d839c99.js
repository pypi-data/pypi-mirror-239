"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_launcher_lib_index_js"],{

/***/ "../packages/launcher/lib/index.js":
/*!*****************************************!*\
  !*** ../packages/launcher/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ILauncher": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.ILauncher),
/* harmony export */   "Launcher": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.Launcher),
/* harmony export */   "LauncherModel": () => (/* reexport safe */ _widget__WEBPACK_IMPORTED_MODULE_1__.LauncherModel)
/* harmony export */ });
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "../packages/launcher/lib/tokens.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "../packages/launcher/lib/widget.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module launcher
 */




/***/ }),

/***/ "../packages/launcher/lib/tokens.js":
/*!******************************************!*\
  !*** ../packages/launcher/lib/tokens.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ILauncher": () => (/* binding */ ILauncher)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */

/**
 * The launcher token.
 */
const ILauncher = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/launcher:ILauncher', `A service for the application activity launcher.
  Use this to add your extension activities to the launcher panel.`);


/***/ }),

/***/ "../packages/launcher/lib/widget.js":
/*!******************************************!*\
  !*** ../packages/launcher/lib/widget.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Launcher": () => (/* binding */ Launcher),
/* harmony export */   "LauncherModel": () => (/* binding */ LauncherModel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_7__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.








/**
 * The class name added to Launcher instances.
 */
const LAUNCHER_CLASS = 'jp-Launcher';
/**
 * LauncherModel keeps track of the path to working directory and has a list of
 * LauncherItems, which the Launcher will render.
 */
class LauncherModel extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomModel {
    constructor() {
        super(...arguments);
        this.itemsList = [];
    }
    /**
     * Add a command item to the launcher, and trigger re-render event for parent
     * widget.
     *
     * @param options - The specification options for a launcher item.
     *
     * @returns A disposable that will remove the item from Launcher, and trigger
     * re-render event for parent widget.
     *
     */
    add(options) {
        // Create a copy of the options to circumvent mutations to the original.
        const item = Private.createItem(options);
        this.itemsList.push(item);
        this.stateChanged.emit(void 0);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_4__.DisposableDelegate(() => {
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.ArrayExt.removeFirstOf(this.itemsList, item);
            this.stateChanged.emit(void 0);
        });
    }
    /**
     * Return an iterator of launcher items.
     */
    items() {
        return this.itemsList[Symbol.iterator]();
    }
}
/**
 * A virtual-DOM-based widget for the Launcher.
 */
class Launcher extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.VDomRenderer {
    /**
     * Construct a new launcher widget.
     */
    constructor(options) {
        super(options.model);
        this._pending = false;
        this._cwd = '';
        this._cwd = options.cwd;
        this.translator = options.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._trans = this.translator.load('jupyterlab');
        this._callback = options.callback;
        this._commands = options.commands;
        this.addClass(LAUNCHER_CLASS);
    }
    /**
     * The cwd of the launcher.
     */
    get cwd() {
        return this._cwd;
    }
    set cwd(value) {
        this._cwd = value;
        this.update();
    }
    /**
     * Whether there is a pending item being launched.
     */
    get pending() {
        return this._pending;
    }
    set pending(value) {
        this._pending = value;
    }
    /**
     * Render the launcher to virtual DOM nodes.
     */
    render() {
        // Bail if there is no model.
        if (!this.model) {
            return null;
        }
        const knownCategories = [
            this._trans.__('Notebook'),
            this._trans.__('Console'),
            this._trans.__('Other')
        ];
        const kernelCategories = [
            this._trans.__('Notebook'),
            this._trans.__('Console')
        ];
        // First group-by categories
        const categories = Object.create(null);
        for (const item of this.model.items()) {
            const cat = item.category || this._trans.__('Other');
            if (!(cat in categories)) {
                categories[cat] = [];
            }
            categories[cat].push(item);
        }
        // Within each category sort by rank
        for (const cat in categories) {
            categories[cat] = categories[cat].sort((a, b) => {
                return Private.sortCmp(a, b, this._cwd, this._commands);
            });
        }
        // Variable to help create sections
        const sections = [];
        let section;
        // Assemble the final ordered list of categories, beginning with
        // KNOWN_CATEGORIES.
        const orderedCategories = [];
        for (const cat of knownCategories) {
            orderedCategories.push(cat);
        }
        for (const cat in categories) {
            if (knownCategories.indexOf(cat) === -1) {
                orderedCategories.push(cat);
            }
        }
        // Now create the sections for each category
        orderedCategories.forEach(cat => {
            if (!categories[cat]) {
                return;
            }
            const item = categories[cat][0];
            const args = { ...item.args, cwd: this.cwd };
            const kernel = kernelCategories.indexOf(cat) > -1;
            const iconClass = this._commands.iconClass(item.command, args);
            const icon = this._commands.icon(item.command, args);
            if (cat in categories) {
                section = (react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-Launcher-section", key: cat },
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-Launcher-sectionHeader" },
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon.resolveReact, { icon: icon, iconClass: (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.classes)(iconClass, 'jp-Icon-cover'), stylesheet: "launcherSection" }),
                        react__WEBPACK_IMPORTED_MODULE_7__.createElement("h2", { className: "jp-Launcher-sectionTitle" }, cat)),
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-Launcher-cardContainer" }, Array.from((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.map)(categories[cat], (item) => {
                        return Card(kernel, item, this, this._commands, this._trans, this._callback);
                    })))));
                sections.push(section);
            }
        });
        // Wrap the sections in body and content divs.
        return (react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-Launcher-body" },
            react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-Launcher-content" },
                react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-Launcher-cwd" },
                    react__WEBPACK_IMPORTED_MODULE_7__.createElement("h3", null, this.cwd)),
                sections)));
    }
}
/**
 * A pure tsx component for a launcher card.
 *
 * @param kernel - whether the item takes uses a kernel.
 *
 * @param item - the launcher item to render.
 *
 * @param launcher - the Launcher instance to which this is added.
 *
 * @param commands - the command registry holding the command of item.
 *
 * @param trans - the translation bundle.
 *
 * @returns a vdom `VirtualElement` for the launcher card.
 */
function Card(kernel, item, launcher, commands, trans, launcherCallback) {
    // Get some properties of the command
    const command = item.command;
    const args = { ...item.args, cwd: launcher.cwd };
    const caption = commands.caption(command, args);
    const label = commands.label(command, args);
    const title = kernel ? label : caption || label;
    // Build the onclick handler.
    const onclick = () => {
        // If an item has already been launched,
        // don't try to launch another.
        if (launcher.pending === true) {
            return;
        }
        launcher.pending = true;
        void commands
            .execute(command, {
            ...item.args,
            cwd: launcher.cwd
        })
            .then(value => {
            launcher.pending = false;
            if (value instanceof _lumino_widgets__WEBPACK_IMPORTED_MODULE_6__.Widget) {
                launcherCallback(value);
            }
        })
            .catch(err => {
            console.error(err);
            launcher.pending = false;
            void (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showErrorMessage)(trans._p('Error', 'Launcher Error'), err);
        });
    };
    // With tabindex working, you can now pick a kernel by tabbing around and
    // pressing Enter.
    const onkeypress = (event) => {
        if (event.key === 'Enter') {
            onclick();
        }
    };
    const iconClass = commands.iconClass(command, args);
    const icon = commands.icon(command, args);
    // Return the VDOM element.
    return (react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-LauncherCard", title: title, onClick: onclick, onKeyPress: onkeypress, tabIndex: 0, "data-category": item.category || trans.__('Other'), key: Private.keyProperty.get(item) },
        react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-LauncherCard-icon" }, kernel ? (item.kernelIconUrl ? (react__WEBPACK_IMPORTED_MODULE_7__.createElement("img", { src: item.kernelIconUrl, className: "jp-Launcher-kernelIcon" })) : (react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-LauncherCard-noKernelIcon" }, label[0].toUpperCase()))) : (react__WEBPACK_IMPORTED_MODULE_7__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.LabIcon.resolveReact, { icon: icon, iconClass: (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.classes)(iconClass, 'jp-Icon-cover'), stylesheet: "launcherCard" }))),
        react__WEBPACK_IMPORTED_MODULE_7__.createElement("div", { className: "jp-LauncherCard-label", title: title },
            react__WEBPACK_IMPORTED_MODULE_7__.createElement("p", null, label))));
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * An incrementing counter for keys.
     */
    let id = 0;
    /**
     * An attached property for an item's key.
     */
    Private.keyProperty = new _lumino_properties__WEBPACK_IMPORTED_MODULE_5__.AttachedProperty({
        name: 'key',
        create: () => id++
    });
    /**
     * Create a fully specified item given item options.
     */
    function createItem(options) {
        return {
            ...options,
            category: options.category || '',
            rank: options.rank !== undefined ? options.rank : Infinity
        };
    }
    Private.createItem = createItem;
    /**
     * A sort comparison function for a launcher item.
     */
    function sortCmp(a, b, cwd, commands) {
        // First, compare by rank.
        const r1 = a.rank;
        const r2 = b.rank;
        if (r1 !== r2 && r1 !== undefined && r2 !== undefined) {
            return r1 < r2 ? -1 : 1; // Infinity safe
        }
        // Finally, compare by display name.
        const aLabel = commands.label(a.command, { ...a.args, cwd });
        const bLabel = commands.label(b.command, { ...b.args, cwd });
        return aLabel.localeCompare(bLabel);
    }
    Private.sortCmp = sortCmp;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbGF1bmNoZXJfbGliX2luZGV4X2pzLmI2ZTBmYWMzYjdmNTFkODM5Yzk5LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFFc0I7QUFDQTs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNSekI7OztHQUdHO0FBSzJEO0FBSTlEOztHQUVHO0FBQ0ksTUFBTSxTQUFTLEdBQUcsSUFBSSxvREFBSyxDQUNoQyxnQ0FBZ0MsRUFDaEM7bUVBQ2lFLENBQ2xFLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDbkJGLDBDQUEwQztBQUMxQywyREFBMkQ7QUFFSDtBQUt2QjtBQU1FO0FBQ2U7QUFFbUI7QUFDZjtBQUNiO0FBQ1Y7QUFHL0I7O0dBRUc7QUFDSCxNQUFNLGNBQWMsR0FBRyxhQUFhLENBQUM7QUFFckM7OztHQUdHO0FBQ0ksTUFBTSxhQUFjLFNBQVEsZ0VBQVM7SUFBNUM7O1FBK0JZLGNBQVMsR0FBNkIsRUFBRSxDQUFDO0lBQ3JELENBQUM7SUEvQkM7Ozs7Ozs7OztPQVNHO0lBQ0gsR0FBRyxDQUFDLE9BQStCO1FBQ2pDLHdFQUF3RTtRQUN4RSxNQUFNLElBQUksR0FBRyxPQUFPLENBQUMsVUFBVSxDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBRXpDLElBQUksQ0FBQyxTQUFTLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxDQUFDO1FBQzFCLElBQUksQ0FBQyxZQUFZLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUM7UUFFL0IsT0FBTyxJQUFJLGtFQUFrQixDQUFDLEdBQUcsRUFBRTtZQUNqQyxxRUFBc0IsQ0FBQyxJQUFJLENBQUMsU0FBUyxFQUFFLElBQUksQ0FBQyxDQUFDO1lBQzdDLElBQUksQ0FBQyxZQUFZLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUM7UUFDakMsQ0FBQyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBRUQ7O09BRUc7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QixNQUFNLEVBQUUsR0FBRyxDQUFDLENBQUMsSUFBSSxDQUFDO1FBQ2xCLElBQUksRUFBRSxLQUFLLEVBQUUsSUFBSSxFQUFFLEtBQUssU0FBUyxJQUFJLEVBQUUsS0FBSyxTQUFTLEVBQUU7WUFDckQsT0FBTyxFQUFFLEdBQUcsRUFBRSxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsZ0JBQWdCO1NBQzFDO1FBRUQsb0NBQW9DO1FBQ3BDLE1BQU0sTUFBTSxHQUFHLFFBQVEsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLE9BQU8sRUFBRSxFQUFFLEdBQUcsQ0FBQyxDQUFDLElBQUksRUFBRSxHQUFHLEVBQUUsQ0FBQyxDQUFDO1FBQzdELE1BQU0sTUFBTSxHQUFHLFFBQVEsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLE9BQU8sRUFBRSxFQUFFLEdBQUcsQ0FBQyxDQUFDLElBQUksRUFBRSxHQUFHLEVBQUUsQ0FBQyxDQUFDO1FBQzdELE9BQU8sTUFBTSxDQUFDLGFBQWEsQ0FBQyxNQUFNLENBQUMsQ0FBQztJQUN0QyxDQUFDO0lBakJlLGVBQU8sVUFpQnRCO0FBQ0gsQ0FBQyxFQW5EUyxPQUFPLEtBQVAsT0FBTyxRQW1EaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbGF1bmNoZXIvc3JjL2luZGV4LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9sYXVuY2hlci9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9sYXVuY2hlci9zcmMvd2lkZ2V0LnRzeCJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBsYXVuY2hlclxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbmV4cG9ydCAqIGZyb20gJy4vd2lkZ2V0JztcbiIsIi8qXG4gKiBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbiAqIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4gKi9cblxuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBWRG9tUmVuZGVyZXIgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgUmVhZG9ubHlKU09OT2JqZWN0LCBUb2tlbiB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8qKlxuICogVGhlIGxhdW5jaGVyIHRva2VuLlxuICovXG5leHBvcnQgY29uc3QgSUxhdW5jaGVyID0gbmV3IFRva2VuPElMYXVuY2hlcj4oXG4gICdAanVweXRlcmxhYi9sYXVuY2hlcjpJTGF1bmNoZXInLFxuICBgQSBzZXJ2aWNlIGZvciB0aGUgYXBwbGljYXRpb24gYWN0aXZpdHkgbGF1bmNoZXIuXG4gIFVzZSB0aGlzIHRvIGFkZCB5b3VyIGV4dGVuc2lvbiBhY3Rpdml0aWVzIHRvIHRoZSBsYXVuY2hlciBwYW5lbC5gXG4pO1xuXG4vKipcbiAqIFRoZSBsYXVuY2hlciBpbnRlcmZhY2UuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSUxhdW5jaGVyIHtcbiAgLyoqXG4gICAqIEFkZCBhIGNvbW1hbmQgaXRlbSB0byB0aGUgbGF1bmNoZXIsIGFuZCB0cmlnZ2VyIHJlLXJlbmRlciBldmVudCBmb3IgcGFyZW50XG4gICAqIHdpZGdldC5cbiAgICpcbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUaGUgc3BlY2lmaWNhdGlvbiBvcHRpb25zIGZvciBhIGxhdW5jaGVyIGl0ZW0uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgZGlzcG9zYWJsZSB0aGF0IHdpbGwgcmVtb3ZlIHRoZSBpdGVtIGZyb20gTGF1bmNoZXIsIGFuZCB0cmlnZ2VyXG4gICAqIHJlLXJlbmRlciBldmVudCBmb3IgcGFyZW50IHdpZGdldC5cbiAgICpcbiAgICovXG4gIGFkZChvcHRpb25zOiBJTGF1bmNoZXIuSUl0ZW1PcHRpb25zKTogSURpc3Bvc2FibGU7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgYElMYXVuY2hlcmAgY2xhc3Mgc3RhdGljcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJTGF1bmNoZXIge1xuICAvKipcbiAgICogQW4gaW50ZXJmYWNlIGZvciB0aGUgbGF1bmNoZXIgbW9kZWxcbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU1vZGVsIGV4dGVuZHMgSUxhdW5jaGVyLCBWRG9tUmVuZGVyZXIuSU1vZGVsIHtcbiAgICAvKipcbiAgICAgKiBSZXR1cm4gYW4gaXRlcmF0b3Igb2YgbGF1bmNoZXIgaXRlbXMuXG4gICAgICovXG4gICAgaXRlbXMoKTogSXRlcmFibGVJdGVyYXRvcjxJTGF1bmNoZXIuSUl0ZW1PcHRpb25zPjtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgb3B0aW9ucyB1c2VkIHRvIGNyZWF0ZSBhIExhdW5jaGVyLlxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJT3B0aW9ucyB7XG4gICAgLyoqXG4gICAgICogVGhlIG1vZGVsIG9mIHRoZSBsYXVuY2hlci5cbiAgICAgKi9cbiAgICBtb2RlbDogSU1vZGVsO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGN3ZCBvZiB0aGUgbGF1bmNoZXIuXG4gICAgICovXG4gICAgY3dkOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29tbWFuZCByZWdpc3RyeSB1c2VkIGJ5IHRoZSBsYXVuY2hlci5cbiAgICAgKi9cbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFwcGxpY2F0aW9uIGxhbmd1YWdlIHRyYW5zbGF0aW9uLlxuICAgICAqL1xuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBjYWxsYmFjayB1c2VkIHdoZW4gYW4gaXRlbSBpcyBsYXVuY2hlZC5cbiAgICAgKi9cbiAgICBjYWxsYmFjazogKHdpZGdldDogV2lkZ2V0KSA9PiB2b2lkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBvcHRpb25zIHVzZWQgdG8gY3JlYXRlIGEgbGF1bmNoZXIgaXRlbS5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSUl0ZW1PcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgY29tbWFuZCBJRCBmb3IgdGhlIGxhdW5jaGVyIGl0ZW0uXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogSWYgdGhlIGNvbW1hbmQncyBgZXhlY3V0ZWAgbWV0aG9kIHJldHVybnMgYSBgV2lkZ2V0YCBvclxuICAgICAqIGEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdpdGggYSBgV2lkZ2V0YCwgdGhlbiB0aGF0IHdpZGdldCB3aWxsXG4gICAgICogcmVwbGFjZSB0aGUgbGF1bmNoZXIgaW4gdGhlIHNhbWUgbG9jYXRpb24gb2YgdGhlIGFwcGxpY2F0aW9uXG4gICAgICogc2hlbGwuIElmIHRoZSBgZXhlY3V0ZWAgbWV0aG9kIGRvZXMgc29tZXRoaW5nIGVsc2VcbiAgICAgKiAoaS5lLiwgY3JlYXRlIGEgbW9kYWwgZGlhbG9nKSwgdGhlbiB0aGUgbGF1bmNoZXIgd2lsbCBub3QgYmVcbiAgICAgKiBkaXNwb3NlZC5cbiAgICAgKi9cbiAgICBjb21tYW5kOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgYXJndW1lbnRzIGdpdmVuIHRvIHRoZSBjb21tYW5kIGZvclxuICAgICAqIGNyZWF0aW5nIHRoZSBsYXVuY2hlciBpdGVtLlxuICAgICAqXG4gICAgICogIyMjIE5vdGVzXG4gICAgICogVGhlIGxhdW5jaGVyIHdpbGwgYWxzbyBhZGQgdGhlIGN1cnJlbnQgd29ya2luZ1xuICAgICAqIGRpcmVjdG9yeSBvZiB0aGUgZmlsZWJyb3dzZXIgaW4gdGhlIGBjd2RgIGZpZWxkXG4gICAgICogb2YgdGhlIGFyZ3MsIHdoaWNoIGEgY29tbWFuZCBtYXkgdXNlIHRvIGNyZWF0ZVxuICAgICAqIHRoZSBhY3Rpdml0eSB3aXRoIHJlc3BlY3QgdG8gdGhlIHJpZ2h0IGRpcmVjdG9yeS5cbiAgICAgKi9cbiAgICBhcmdzPzogUmVhZG9ubHlKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNhdGVnb3J5IGZvciB0aGUgbGF1bmNoZXIgaXRlbS5cbiAgICAgKlxuICAgICAqIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGFuIGVtcHR5IHN0cmluZy5cbiAgICAgKi9cbiAgICBjYXRlZ29yeT86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSByYW5rIGZvciB0aGUgbGF1bmNoZXIgaXRlbS5cbiAgICAgKlxuICAgICAqIFRoZSByYW5rIGlzIHVzZWQgd2hlbiBvcmRlcmluZyBsYXVuY2hlciBpdGVtcyBmb3IgZGlzcGxheS4gQWZ0ZXIgZ3JvdXBpbmdcbiAgICAgKiBpbnRvIGNhdGVnb3JpZXMsIGl0ZW1zIGFyZSBzb3J0ZWQgaW4gdGhlIGZvbGxvd2luZyBvcmRlcjpcbiAgICAgKiAgIDEuIFJhbmsgKGxvd2VyIGlzIGJldHRlcilcbiAgICAgKiAgIDMuIERpc3BsYXkgTmFtZSAobG9jYWxlIG9yZGVyKVxuICAgICAqXG4gICAgICogVGhlIGRlZmF1bHQgcmFuayBpcyBgSW5maW5pdHlgLlxuICAgICAqL1xuICAgIHJhbms/OiBudW1iZXI7XG5cbiAgICAvKipcbiAgICAgKiBGb3IgaXRlbXMgdGhhdCBoYXZlIGEga2VybmVsIGFzc29jaWF0ZWQgd2l0aCB0aGVtLCB0aGUgVVJMIG9mIHRoZSBrZXJuZWxcbiAgICAgKiBpY29uLlxuICAgICAqXG4gICAgICogVGhpcyBpcyBub3QgYSBDU1MgY2xhc3MsIGJ1dCB0aGUgVVJMIHRoYXQgcG9pbnRzIHRvIHRoZSBpY29uIGluIHRoZSBrZXJuZWxcbiAgICAgKiBzcGVjLlxuICAgICAqL1xuICAgIGtlcm5lbEljb25Vcmw/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBNZXRhZGF0YSBhYm91dCB0aGUgaXRlbS4gIFRoaXMgY2FuIGJlIHVzZWQgYnkgdGhlIGxhdW5jaGVyIHRvXG4gICAgICogYWZmZWN0IGhvdyB0aGUgaXRlbSBpcyBkaXNwbGF5ZWQuXG4gICAgICovXG4gICAgbWV0YWRhdGE/OiBSZWFkb25seUpTT05PYmplY3Q7XG4gIH1cbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgc2hvd0Vycm9yTWVzc2FnZSB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7XG4gIElUcmFuc2xhdG9yLFxuICBudWxsVHJhbnNsYXRvcixcbiAgVHJhbnNsYXRpb25CdW5kbGVcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHtcbiAgY2xhc3NlcyxcbiAgTGFiSWNvbixcbiAgVkRvbU1vZGVsLFxuICBWRG9tUmVuZGVyZXJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBBcnJheUV4dCwgbWFwIH0gZnJvbSAnQGx1bWluby9hbGdvcml0aG0nO1xuaW1wb3J0IHsgQ29tbWFuZFJlZ2lzdHJ5IH0gZnJvbSAnQGx1bWluby9jb21tYW5kcyc7XG5pbXBvcnQgeyBEaXNwb3NhYmxlRGVsZWdhdGUsIElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IEF0dGFjaGVkUHJvcGVydHkgfSBmcm9tICdAbHVtaW5vL3Byb3BlcnRpZXMnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcbmltcG9ydCAqIGFzIFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7IElMYXVuY2hlciB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBUaGUgY2xhc3MgbmFtZSBhZGRlZCB0byBMYXVuY2hlciBpbnN0YW5jZXMuXG4gKi9cbmNvbnN0IExBVU5DSEVSX0NMQVNTID0gJ2pwLUxhdW5jaGVyJztcblxuLyoqXG4gKiBMYXVuY2hlck1vZGVsIGtlZXBzIHRyYWNrIG9mIHRoZSBwYXRoIHRvIHdvcmtpbmcgZGlyZWN0b3J5IGFuZCBoYXMgYSBsaXN0IG9mXG4gKiBMYXVuY2hlckl0ZW1zLCB3aGljaCB0aGUgTGF1bmNoZXIgd2lsbCByZW5kZXIuXG4gKi9cbmV4cG9ydCBjbGFzcyBMYXVuY2hlck1vZGVsIGV4dGVuZHMgVkRvbU1vZGVsIGltcGxlbWVudHMgSUxhdW5jaGVyLklNb2RlbCB7XG4gIC8qKlxuICAgKiBBZGQgYSBjb21tYW5kIGl0ZW0gdG8gdGhlIGxhdW5jaGVyLCBhbmQgdHJpZ2dlciByZS1yZW5kZXIgZXZlbnQgZm9yIHBhcmVudFxuICAgKiB3aWRnZXQuXG4gICAqXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVGhlIHNwZWNpZmljYXRpb24gb3B0aW9ucyBmb3IgYSBsYXVuY2hlciBpdGVtLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGRpc3Bvc2FibGUgdGhhdCB3aWxsIHJlbW92ZSB0aGUgaXRlbSBmcm9tIExhdW5jaGVyLCBhbmQgdHJpZ2dlclxuICAgKiByZS1yZW5kZXIgZXZlbnQgZm9yIHBhcmVudCB3aWRnZXQuXG4gICAqXG4gICAqL1xuICBhZGQob3B0aW9uczogSUxhdW5jaGVyLklJdGVtT3B0aW9ucyk6IElEaXNwb3NhYmxlIHtcbiAgICAvLyBDcmVhdGUgYSBjb3B5IG9mIHRoZSBvcHRpb25zIHRvIGNpcmN1bXZlbnQgbXV0YXRpb25zIHRvIHRoZSBvcmlnaW5hbC5cbiAgICBjb25zdCBpdGVtID0gUHJpdmF0ZS5jcmVhdGVJdGVtKG9wdGlvbnMpO1xuXG4gICAgdGhpcy5pdGVtc0xpc3QucHVzaChpdGVtKTtcbiAgICB0aGlzLnN0YXRlQ2hhbmdlZC5lbWl0KHZvaWQgMCk7XG5cbiAgICByZXR1cm4gbmV3IERpc3Bvc2FibGVEZWxlZ2F0ZSgoKSA9PiB7XG4gICAgICBBcnJheUV4dC5yZW1vdmVGaXJzdE9mKHRoaXMuaXRlbXNMaXN0LCBpdGVtKTtcbiAgICAgIHRoaXMuc3RhdGVDaGFuZ2VkLmVtaXQodm9pZCAwKTtcbiAgICB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm4gYW4gaXRlcmF0b3Igb2YgbGF1bmNoZXIgaXRlbXMuXG4gICAqL1xuICBpdGVtcygpOiBJdGVyYWJsZUl0ZXJhdG9yPElMYXVuY2hlci5JSXRlbU9wdGlvbnM+IHtcbiAgICByZXR1cm4gdGhpcy5pdGVtc0xpc3RbU3ltYm9sLml0ZXJhdG9yXSgpO1xuICB9XG5cbiAgcHJvdGVjdGVkIGl0ZW1zTGlzdDogSUxhdW5jaGVyLklJdGVtT3B0aW9uc1tdID0gW107XG59XG5cbi8qKlxuICogQSB2aXJ0dWFsLURPTS1iYXNlZCB3aWRnZXQgZm9yIHRoZSBMYXVuY2hlci5cbiAqL1xuZXhwb3J0IGNsYXNzIExhdW5jaGVyIGV4dGVuZHMgVkRvbVJlbmRlcmVyPElMYXVuY2hlci5JTW9kZWw+IHtcbiAgLyoqXG4gICAqIENvbnN0cnVjdCBhIG5ldyBsYXVuY2hlciB3aWRnZXQuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBJTGF1bmNoZXIuSU9wdGlvbnMpIHtcbiAgICBzdXBlcihvcHRpb25zLm1vZGVsKTtcbiAgICB0aGlzLl9jd2QgPSBvcHRpb25zLmN3ZDtcbiAgICB0aGlzLnRyYW5zbGF0b3IgPSBvcHRpb25zLnRyYW5zbGF0b3IgfHwgbnVsbFRyYW5zbGF0b3I7XG4gICAgdGhpcy5fdHJhbnMgPSB0aGlzLnRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIHRoaXMuX2NhbGxiYWNrID0gb3B0aW9ucy5jYWxsYmFjaztcbiAgICB0aGlzLl9jb21tYW5kcyA9IG9wdGlvbnMuY29tbWFuZHM7XG4gICAgdGhpcy5hZGRDbGFzcyhMQVVOQ0hFUl9DTEFTUyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIGN3ZCBvZiB0aGUgbGF1bmNoZXIuXG4gICAqL1xuICBnZXQgY3dkKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2N3ZDtcbiAgfVxuICBzZXQgY3dkKHZhbHVlOiBzdHJpbmcpIHtcbiAgICB0aGlzLl9jd2QgPSB2YWx1ZTtcbiAgICB0aGlzLnVwZGF0ZSgpO1xuICB9XG5cbiAgLyoqXG4gICAqIFdoZXRoZXIgdGhlcmUgaXMgYSBwZW5kaW5nIGl0ZW0gYmVpbmcgbGF1bmNoZWQuXG4gICAqL1xuICBnZXQgcGVuZGluZygpOiBib29sZWFuIHtcbiAgICByZXR1cm4gdGhpcy5fcGVuZGluZztcbiAgfVxuICBzZXQgcGVuZGluZyh2YWx1ZTogYm9vbGVhbikge1xuICAgIHRoaXMuX3BlbmRpbmcgPSB2YWx1ZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgdGhlIGxhdW5jaGVyIHRvIHZpcnR1YWwgRE9NIG5vZGVzLlxuICAgKi9cbiAgcHJvdGVjdGVkIHJlbmRlcigpOiBSZWFjdC5SZWFjdEVsZW1lbnQ8YW55PiB8IG51bGwge1xuICAgIC8vIEJhaWwgaWYgdGhlcmUgaXMgbm8gbW9kZWwuXG4gICAgaWYgKCF0aGlzLm1vZGVsKSB7XG4gICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICBjb25zdCBrbm93bkNhdGVnb3JpZXMgPSBbXG4gICAgICB0aGlzLl90cmFucy5fXygnTm90ZWJvb2snKSxcbiAgICAgIHRoaXMuX3RyYW5zLl9fKCdDb25zb2xlJyksXG4gICAgICB0aGlzLl90cmFucy5fXygnT3RoZXInKVxuICAgIF07XG4gICAgY29uc3Qga2VybmVsQ2F0ZWdvcmllcyA9IFtcbiAgICAgIHRoaXMuX3RyYW5zLl9fKCdOb3RlYm9vaycpLFxuICAgICAgdGhpcy5fdHJhbnMuX18oJ0NvbnNvbGUnKVxuICAgIF07XG5cbiAgICAvLyBGaXJzdCBncm91cC1ieSBjYXRlZ29yaWVzXG4gICAgY29uc3QgY2F0ZWdvcmllcyA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG4gICAgZm9yIChjb25zdCBpdGVtIG9mIHRoaXMubW9kZWwuaXRlbXMoKSkge1xuICAgICAgY29uc3QgY2F0ID0gaXRlbS5jYXRlZ29yeSB8fCB0aGlzLl90cmFucy5fXygnT3RoZXInKTtcbiAgICAgIGlmICghKGNhdCBpbiBjYXRlZ29yaWVzKSkge1xuICAgICAgICBjYXRlZ29yaWVzW2NhdF0gPSBbXTtcbiAgICAgIH1cbiAgICAgIGNhdGVnb3JpZXNbY2F0XS5wdXNoKGl0ZW0pO1xuICAgIH1cbiAgICAvLyBXaXRoaW4gZWFjaCBjYXRlZ29yeSBzb3J0IGJ5IHJhbmtcbiAgICBmb3IgKGNvbnN0IGNhdCBpbiBjYXRlZ29yaWVzKSB7XG4gICAgICBjYXRlZ29yaWVzW2NhdF0gPSBjYXRlZ29yaWVzW2NhdF0uc29ydChcbiAgICAgICAgKGE6IElMYXVuY2hlci5JSXRlbU9wdGlvbnMsIGI6IElMYXVuY2hlci5JSXRlbU9wdGlvbnMpID0+IHtcbiAgICAgICAgICByZXR1cm4gUHJpdmF0ZS5zb3J0Q21wKGEsIGIsIHRoaXMuX2N3ZCwgdGhpcy5fY29tbWFuZHMpO1xuICAgICAgICB9XG4gICAgICApO1xuICAgIH1cblxuICAgIC8vIFZhcmlhYmxlIHRvIGhlbHAgY3JlYXRlIHNlY3Rpb25zXG4gICAgY29uc3Qgc2VjdGlvbnM6IFJlYWN0LlJlYWN0RWxlbWVudDxhbnk+W10gPSBbXTtcbiAgICBsZXQgc2VjdGlvbjogUmVhY3QuUmVhY3RFbGVtZW50PGFueT47XG5cbiAgICAvLyBBc3NlbWJsZSB0aGUgZmluYWwgb3JkZXJlZCBsaXN0IG9mIGNhdGVnb3JpZXMsIGJlZ2lubmluZyB3aXRoXG4gICAgLy8gS05PV05fQ0FURUdPUklFUy5cbiAgICBjb25zdCBvcmRlcmVkQ2F0ZWdvcmllczogc3RyaW5nW10gPSBbXTtcbiAgICBmb3IgKGNvbnN0IGNhdCBvZiBrbm93bkNhdGVnb3JpZXMpIHtcbiAgICAgIG9yZGVyZWRDYXRlZ29yaWVzLnB1c2goY2F0KTtcbiAgICB9XG4gICAgZm9yIChjb25zdCBjYXQgaW4gY2F0ZWdvcmllcykge1xuICAgICAgaWYgKGtub3duQ2F0ZWdvcmllcy5pbmRleE9mKGNhdCkgPT09IC0xKSB7XG4gICAgICAgIG9yZGVyZWRDYXRlZ29yaWVzLnB1c2goY2F0KTtcbiAgICAgIH1cbiAgICB9XG5cbiAgICAvLyBOb3cgY3JlYXRlIHRoZSBzZWN0aW9ucyBmb3IgZWFjaCBjYXRlZ29yeVxuICAgIG9yZGVyZWRDYXRlZ29yaWVzLmZvckVhY2goY2F0ID0+IHtcbiAgICAgIGlmICghY2F0ZWdvcmllc1tjYXRdKSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IGl0ZW0gPSBjYXRlZ29yaWVzW2NhdF1bMF0gYXMgSUxhdW5jaGVyLklJdGVtT3B0aW9ucztcbiAgICAgIGNvbnN0IGFyZ3MgPSB7IC4uLml0ZW0uYXJncywgY3dkOiB0aGlzLmN3ZCB9O1xuICAgICAgY29uc3Qga2VybmVsID0ga2VybmVsQ2F0ZWdvcmllcy5pbmRleE9mKGNhdCkgPiAtMTtcbiAgICAgIGNvbnN0IGljb25DbGFzcyA9IHRoaXMuX2NvbW1hbmRzLmljb25DbGFzcyhpdGVtLmNvbW1hbmQsIGFyZ3MpO1xuICAgICAgY29uc3QgaWNvbiA9IHRoaXMuX2NvbW1hbmRzLmljb24oaXRlbS5jb21tYW5kLCBhcmdzKTtcblxuICAgICAgaWYgKGNhdCBpbiBjYXRlZ29yaWVzKSB7XG4gICAgICAgIHNlY3Rpb24gPSAoXG4gICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlci1zZWN0aW9uXCIga2V5PXtjYXR9PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlci1zZWN0aW9uSGVhZGVyXCI+XG4gICAgICAgICAgICAgIDxMYWJJY29uLnJlc29sdmVSZWFjdFxuICAgICAgICAgICAgICAgIGljb249e2ljb259XG4gICAgICAgICAgICAgICAgaWNvbkNsYXNzPXtjbGFzc2VzKGljb25DbGFzcywgJ2pwLUljb24tY292ZXInKX1cbiAgICAgICAgICAgICAgICBzdHlsZXNoZWV0PVwibGF1bmNoZXJTZWN0aW9uXCJcbiAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgPGgyIGNsYXNzTmFtZT1cImpwLUxhdW5jaGVyLXNlY3Rpb25UaXRsZVwiPntjYXR9PC9oMj5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlci1jYXJkQ29udGFpbmVyXCI+XG4gICAgICAgICAgICAgIHtBcnJheS5mcm9tKFxuICAgICAgICAgICAgICAgIG1hcChjYXRlZ29yaWVzW2NhdF0sIChpdGVtOiBJTGF1bmNoZXIuSUl0ZW1PcHRpb25zKSA9PiB7XG4gICAgICAgICAgICAgICAgICByZXR1cm4gQ2FyZChcbiAgICAgICAgICAgICAgICAgICAga2VybmVsLFxuICAgICAgICAgICAgICAgICAgICBpdGVtLFxuICAgICAgICAgICAgICAgICAgICB0aGlzLFxuICAgICAgICAgICAgICAgICAgICB0aGlzLl9jb21tYW5kcyxcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5fdHJhbnMsXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuX2NhbGxiYWNrXG4gICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICl9XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKTtcbiAgICAgICAgc2VjdGlvbnMucHVzaChzZWN0aW9uKTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIFdyYXAgdGhlIHNlY3Rpb25zIGluIGJvZHkgYW5kIGNvbnRlbnQgZGl2cy5cbiAgICByZXR1cm4gKFxuICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlci1ib2R5XCI+XG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtTGF1bmNoZXItY29udGVudFwiPlxuICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtTGF1bmNoZXItY3dkXCI+XG4gICAgICAgICAgICA8aDM+e3RoaXMuY3dkfTwvaDM+XG4gICAgICAgICAgPC9kaXY+XG4gICAgICAgICAge3NlY3Rpb25zfVxuICAgICAgICA8L2Rpdj5cbiAgICAgIDwvZGl2PlxuICAgICk7XG4gIH1cblxuICBwcm90ZWN0ZWQgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3I7XG4gIHByaXZhdGUgX3RyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZTtcbiAgcHJpdmF0ZSBfY29tbWFuZHM6IENvbW1hbmRSZWdpc3RyeTtcbiAgcHJpdmF0ZSBfY2FsbGJhY2s6ICh3aWRnZXQ6IFdpZGdldCkgPT4gdm9pZDtcbiAgcHJpdmF0ZSBfcGVuZGluZyA9IGZhbHNlO1xuICBwcml2YXRlIF9jd2QgPSAnJztcbn1cbi8qKlxuICogQSBwdXJlIHRzeCBjb21wb25lbnQgZm9yIGEgbGF1bmNoZXIgY2FyZC5cbiAqXG4gKiBAcGFyYW0ga2VybmVsIC0gd2hldGhlciB0aGUgaXRlbSB0YWtlcyB1c2VzIGEga2VybmVsLlxuICpcbiAqIEBwYXJhbSBpdGVtIC0gdGhlIGxhdW5jaGVyIGl0ZW0gdG8gcmVuZGVyLlxuICpcbiAqIEBwYXJhbSBsYXVuY2hlciAtIHRoZSBMYXVuY2hlciBpbnN0YW5jZSB0byB3aGljaCB0aGlzIGlzIGFkZGVkLlxuICpcbiAqIEBwYXJhbSBjb21tYW5kcyAtIHRoZSBjb21tYW5kIHJlZ2lzdHJ5IGhvbGRpbmcgdGhlIGNvbW1hbmQgb2YgaXRlbS5cbiAqXG4gKiBAcGFyYW0gdHJhbnMgLSB0aGUgdHJhbnNsYXRpb24gYnVuZGxlLlxuICpcbiAqIEByZXR1cm5zIGEgdmRvbSBgVmlydHVhbEVsZW1lbnRgIGZvciB0aGUgbGF1bmNoZXIgY2FyZC5cbiAqL1xuZnVuY3Rpb24gQ2FyZChcbiAga2VybmVsOiBib29sZWFuLFxuICBpdGVtOiBJTGF1bmNoZXIuSUl0ZW1PcHRpb25zLFxuICBsYXVuY2hlcjogTGF1bmNoZXIsXG4gIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnksXG4gIHRyYW5zOiBUcmFuc2xhdGlvbkJ1bmRsZSxcbiAgbGF1bmNoZXJDYWxsYmFjazogKHdpZGdldDogV2lkZ2V0KSA9PiB2b2lkXG4pOiBSZWFjdC5SZWFjdEVsZW1lbnQ8YW55PiB7XG4gIC8vIEdldCBzb21lIHByb3BlcnRpZXMgb2YgdGhlIGNvbW1hbmRcbiAgY29uc3QgY29tbWFuZCA9IGl0ZW0uY29tbWFuZDtcbiAgY29uc3QgYXJncyA9IHsgLi4uaXRlbS5hcmdzLCBjd2Q6IGxhdW5jaGVyLmN3ZCB9O1xuICBjb25zdCBjYXB0aW9uID0gY29tbWFuZHMuY2FwdGlvbihjb21tYW5kLCBhcmdzKTtcbiAgY29uc3QgbGFiZWwgPSBjb21tYW5kcy5sYWJlbChjb21tYW5kLCBhcmdzKTtcbiAgY29uc3QgdGl0bGUgPSBrZXJuZWwgPyBsYWJlbCA6IGNhcHRpb24gfHwgbGFiZWw7XG5cbiAgLy8gQnVpbGQgdGhlIG9uY2xpY2sgaGFuZGxlci5cbiAgY29uc3Qgb25jbGljayA9ICgpID0+IHtcbiAgICAvLyBJZiBhbiBpdGVtIGhhcyBhbHJlYWR5IGJlZW4gbGF1bmNoZWQsXG4gICAgLy8gZG9uJ3QgdHJ5IHRvIGxhdW5jaCBhbm90aGVyLlxuICAgIGlmIChsYXVuY2hlci5wZW5kaW5nID09PSB0cnVlKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGxhdW5jaGVyLnBlbmRpbmcgPSB0cnVlO1xuICAgIHZvaWQgY29tbWFuZHNcbiAgICAgIC5leGVjdXRlKGNvbW1hbmQsIHtcbiAgICAgICAgLi4uaXRlbS5hcmdzLFxuICAgICAgICBjd2Q6IGxhdW5jaGVyLmN3ZFxuICAgICAgfSlcbiAgICAgIC50aGVuKHZhbHVlID0+IHtcbiAgICAgICAgbGF1bmNoZXIucGVuZGluZyA9IGZhbHNlO1xuICAgICAgICBpZiAodmFsdWUgaW5zdGFuY2VvZiBXaWRnZXQpIHtcbiAgICAgICAgICBsYXVuY2hlckNhbGxiYWNrKHZhbHVlKTtcbiAgICAgICAgfVxuICAgICAgfSlcbiAgICAgIC5jYXRjaChlcnIgPT4ge1xuICAgICAgICBjb25zb2xlLmVycm9yKGVycik7XG4gICAgICAgIGxhdW5jaGVyLnBlbmRpbmcgPSBmYWxzZTtcbiAgICAgICAgdm9pZCBzaG93RXJyb3JNZXNzYWdlKHRyYW5zLl9wKCdFcnJvcicsICdMYXVuY2hlciBFcnJvcicpLCBlcnIpO1xuICAgICAgfSk7XG4gIH07XG5cbiAgLy8gV2l0aCB0YWJpbmRleCB3b3JraW5nLCB5b3UgY2FuIG5vdyBwaWNrIGEga2VybmVsIGJ5IHRhYmJpbmcgYXJvdW5kIGFuZFxuICAvLyBwcmVzc2luZyBFbnRlci5cbiAgY29uc3Qgb25rZXlwcmVzcyA9IChldmVudDogUmVhY3QuS2V5Ym9hcmRFdmVudCkgPT4ge1xuICAgIGlmIChldmVudC5rZXkgPT09ICdFbnRlcicpIHtcbiAgICAgIG9uY2xpY2soKTtcbiAgICB9XG4gIH07XG5cbiAgY29uc3QgaWNvbkNsYXNzID0gY29tbWFuZHMuaWNvbkNsYXNzKGNvbW1hbmQsIGFyZ3MpO1xuICBjb25zdCBpY29uID0gY29tbWFuZHMuaWNvbihjb21tYW5kLCBhcmdzKTtcblxuICAvLyBSZXR1cm4gdGhlIFZET00gZWxlbWVudC5cbiAgcmV0dXJuIChcbiAgICA8ZGl2XG4gICAgICBjbGFzc05hbWU9XCJqcC1MYXVuY2hlckNhcmRcIlxuICAgICAgdGl0bGU9e3RpdGxlfVxuICAgICAgb25DbGljaz17b25jbGlja31cbiAgICAgIG9uS2V5UHJlc3M9e29ua2V5cHJlc3N9XG4gICAgICB0YWJJbmRleD17MH1cbiAgICAgIGRhdGEtY2F0ZWdvcnk9e2l0ZW0uY2F0ZWdvcnkgfHwgdHJhbnMuX18oJ090aGVyJyl9XG4gICAgICBrZXk9e1ByaXZhdGUua2V5UHJvcGVydHkuZ2V0KGl0ZW0pfVxuICAgID5cbiAgICAgIDxkaXYgY2xhc3NOYW1lPVwianAtTGF1bmNoZXJDYXJkLWljb25cIj5cbiAgICAgICAge2tlcm5lbCA/IChcbiAgICAgICAgICBpdGVtLmtlcm5lbEljb25VcmwgPyAoXG4gICAgICAgICAgICA8aW1nIHNyYz17aXRlbS5rZXJuZWxJY29uVXJsfSBjbGFzc05hbWU9XCJqcC1MYXVuY2hlci1rZXJuZWxJY29uXCIgLz5cbiAgICAgICAgICApIDogKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqcC1MYXVuY2hlckNhcmQtbm9LZXJuZWxJY29uXCI+XG4gICAgICAgICAgICAgIHtsYWJlbFswXS50b1VwcGVyQ2FzZSgpfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgKVxuICAgICAgICApIDogKFxuICAgICAgICAgIDxMYWJJY29uLnJlc29sdmVSZWFjdFxuICAgICAgICAgICAgaWNvbj17aWNvbn1cbiAgICAgICAgICAgIGljb25DbGFzcz17Y2xhc3NlcyhpY29uQ2xhc3MsICdqcC1JY29uLWNvdmVyJyl9XG4gICAgICAgICAgICBzdHlsZXNoZWV0PVwibGF1bmNoZXJDYXJkXCJcbiAgICAgICAgICAvPlxuICAgICAgICApfVxuICAgICAgPC9kaXY+XG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImpwLUxhdW5jaGVyQ2FyZC1sYWJlbFwiIHRpdGxlPXt0aXRsZX0+XG4gICAgICAgIDxwPntsYWJlbH08L3A+XG4gICAgICA8L2Rpdj5cbiAgICA8L2Rpdj5cbiAgKTtcbn1cblxuLyoqXG4gKiBUaGUgbmFtZXNwYWNlIGZvciBtb2R1bGUgcHJpdmF0ZSBkYXRhLlxuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIC8qKlxuICAgKiBBbiBpbmNyZW1lbnRpbmcgY291bnRlciBmb3Iga2V5cy5cbiAgICovXG4gIGxldCBpZCA9IDA7XG5cbiAgLyoqXG4gICAqIEFuIGF0dGFjaGVkIHByb3BlcnR5IGZvciBhbiBpdGVtJ3Mga2V5LlxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGtleVByb3BlcnR5ID0gbmV3IEF0dGFjaGVkUHJvcGVydHk8XG4gICAgSUxhdW5jaGVyLklJdGVtT3B0aW9ucyxcbiAgICBudW1iZXJcbiAgPih7XG4gICAgbmFtZTogJ2tleScsXG4gICAgY3JlYXRlOiAoKSA9PiBpZCsrXG4gIH0pO1xuXG4gIC8qKlxuICAgKiBDcmVhdGUgYSBmdWxseSBzcGVjaWZpZWQgaXRlbSBnaXZlbiBpdGVtIG9wdGlvbnMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gY3JlYXRlSXRlbShcbiAgICBvcHRpb25zOiBJTGF1bmNoZXIuSUl0ZW1PcHRpb25zXG4gICk6IElMYXVuY2hlci5JSXRlbU9wdGlvbnMge1xuICAgIHJldHVybiB7XG4gICAgICAuLi5vcHRpb25zLFxuICAgICAgY2F0ZWdvcnk6IG9wdGlvbnMuY2F0ZWdvcnkgfHwgJycsXG4gICAgICByYW5rOiBvcHRpb25zLnJhbmsgIT09IHVuZGVmaW5lZCA/IG9wdGlvbnMucmFuayA6IEluZmluaXR5XG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNvcnQgY29tcGFyaXNvbiBmdW5jdGlvbiBmb3IgYSBsYXVuY2hlciBpdGVtLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHNvcnRDbXAoXG4gICAgYTogSUxhdW5jaGVyLklJdGVtT3B0aW9ucyxcbiAgICBiOiBJTGF1bmNoZXIuSUl0ZW1PcHRpb25zLFxuICAgIGN3ZDogc3RyaW5nLFxuICAgIGNvbW1hbmRzOiBDb21tYW5kUmVnaXN0cnlcbiAgKTogbnVtYmVyIHtcbiAgICAvLyBGaXJzdCwgY29tcGFyZSBieSByYW5rLlxuICAgIGNvbnN0IHIxID0gYS5yYW5rO1xuICAgIGNvbnN0IHIyID0gYi5yYW5rO1xuICAgIGlmIChyMSAhPT0gcjIgJiYgcjEgIT09IHVuZGVmaW5lZCAmJiByMiAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICByZXR1cm4gcjEgPCByMiA/IC0xIDogMTsgLy8gSW5maW5pdHkgc2FmZVxuICAgIH1cblxuICAgIC8vIEZpbmFsbHksIGNvbXBhcmUgYnkgZGlzcGxheSBuYW1lLlxuICAgIGNvbnN0IGFMYWJlbCA9IGNvbW1hbmRzLmxhYmVsKGEuY29tbWFuZCwgeyAuLi5hLmFyZ3MsIGN3ZCB9KTtcbiAgICBjb25zdCBiTGFiZWwgPSBjb21tYW5kcy5sYWJlbChiLmNvbW1hbmQsIHsgLi4uYi5hcmdzLCBjd2QgfSk7XG4gICAgcmV0dXJuIGFMYWJlbC5sb2NhbGVDb21wYXJlKGJMYWJlbCk7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==