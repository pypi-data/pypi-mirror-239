"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_theme-light-extension_lib_index_js"],{

/***/ "../packages/theme-light-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/theme-light-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module theme-light-extension
 */


/**
 * A plugin for the Jupyter Light Theme.
 */
const plugin = {
    id: '@jupyterlab/theme-light-extension:plugin',
    description: 'Adds a light theme.',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.ITranslator],
    activate: (app, manager, translator) => {
        const trans = translator.load('jupyterlab');
        const style = '@jupyterlab/theme-light-extension/index.css';
        manager.register({
            name: 'JupyterLab Light',
            displayName: trans.__('JupyterLab Light'),
            isLight: true,
            themeScrollbars: false,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    },
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdGhlbWUtbGlnaHQtZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy42MWQ1YzhhMWYzNWJmNzMwYWZlOS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBTWtEO0FBQ0M7QUFFdEQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBZ0M7SUFDMUMsRUFBRSxFQUFFLDBDQUEwQztJQUM5QyxXQUFXLEVBQUUscUJBQXFCO0lBQ2xDLFFBQVEsRUFBRSxDQUFDLCtEQUFhLEVBQUUsZ0VBQVcsQ0FBQztJQUN0QyxRQUFRLEVBQUUsQ0FDUixHQUFvQixFQUNwQixPQUFzQixFQUN0QixVQUF1QixFQUN2QixFQUFFO1FBQ0YsTUFBTSxLQUFLLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztRQUM1QyxNQUFNLEtBQUssR0FBRyw2Q0FBNkMsQ0FBQztRQUM1RCxPQUFPLENBQUMsUUFBUSxDQUFDO1lBQ2YsSUFBSSxFQUFFLGtCQUFrQjtZQUN4QixXQUFXLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxrQkFBa0IsQ0FBQztZQUN6QyxPQUFPLEVBQUUsSUFBSTtZQUNiLGVBQWUsRUFBRSxLQUFLO1lBQ3RCLElBQUksRUFBRSxHQUFHLEVBQUUsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQztZQUNsQyxNQUFNLEVBQUUsR0FBRyxFQUFFLENBQUMsT0FBTyxDQUFDLE9BQU8sQ0FBQyxTQUFTLENBQUM7U0FDekMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQztJQUNELFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRixpRUFBZSxNQUFNLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdGhlbWUtbGlnaHQtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSB0aGVtZS1saWdodC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJVGhlbWVNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogQSBwbHVnaW4gZm9yIHRoZSBKdXB5dGVyIExpZ2h0IFRoZW1lLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi90aGVtZS1saWdodC1leHRlbnNpb246cGx1Z2luJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIGEgbGlnaHQgdGhlbWUuJyxcbiAgcmVxdWlyZXM6IFtJVGhlbWVNYW5hZ2VyLCBJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbWFuYWdlcjogSVRoZW1lTWFuYWdlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHN0eWxlID0gJ0BqdXB5dGVybGFiL3RoZW1lLWxpZ2h0LWV4dGVuc2lvbi9pbmRleC5jc3MnO1xuICAgIG1hbmFnZXIucmVnaXN0ZXIoe1xuICAgICAgbmFtZTogJ0p1cHl0ZXJMYWIgTGlnaHQnLFxuICAgICAgZGlzcGxheU5hbWU6IHRyYW5zLl9fKCdKdXB5dGVyTGFiIExpZ2h0JyksXG4gICAgICBpc0xpZ2h0OiB0cnVlLFxuICAgICAgdGhlbWVTY3JvbGxiYXJzOiBmYWxzZSxcbiAgICAgIGxvYWQ6ICgpID0+IG1hbmFnZXIubG9hZENTUyhzdHlsZSksXG4gICAgICB1bmxvYWQ6ICgpID0+IFByb21pc2UucmVzb2x2ZSh1bmRlZmluZWQpXG4gICAgfSk7XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuZXhwb3J0IGRlZmF1bHQgcGx1Z2luO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9