"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_theme-dark-extension_lib_index_js"],{

/***/ "../packages/theme-dark-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/theme-dark-extension/lib/index.js ***!
  \*****************************************************/
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
 * @module theme-dark-extension
 */


/**
 * A plugin for the Jupyter Dark Theme.
 */
const plugin = {
    id: '@jupyterlab/theme-dark-extension:plugin',
    description: 'Adds a dark theme.',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.ITranslator],
    activate: (app, manager, translator) => {
        const trans = translator.load('jupyterlab');
        const style = '@jupyterlab/theme-dark-extension/index.css';
        manager.register({
            name: 'JupyterLab Dark',
            displayName: trans.__('JupyterLab Dark'),
            isLight: false,
            themeScrollbars: true,
            load: () => manager.loadCSS(style),
            unload: () => Promise.resolve(undefined)
        });
    },
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdGhlbWUtZGFyay1leHRlbnNpb25fbGliX2luZGV4X2pzLmU2MDgxZmY5M2RmODIwNmE2MGFhLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNa0Q7QUFDQztBQUV0RDs7R0FFRztBQUNILE1BQU0sTUFBTSxHQUFnQztJQUMxQyxFQUFFLEVBQUUseUNBQXlDO0lBQzdDLFdBQVcsRUFBRSxvQkFBb0I7SUFDakMsUUFBUSxFQUFFLENBQUMsK0RBQWEsRUFBRSxnRUFBVyxDQUFDO0lBQ3RDLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLE9BQXNCLEVBQ3RCLFVBQXVCLEVBQ3ZCLEVBQUU7UUFDRixNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQzVDLE1BQU0sS0FBSyxHQUFHLDRDQUE0QyxDQUFDO1FBQzNELE9BQU8sQ0FBQyxRQUFRLENBQUM7WUFDZixJQUFJLEVBQUUsaUJBQWlCO1lBQ3ZCLFdBQVcsRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLGlCQUFpQixDQUFDO1lBQ3hDLE9BQU8sRUFBRSxLQUFLO1lBQ2QsZUFBZSxFQUFFLElBQUk7WUFDckIsSUFBSSxFQUFFLEdBQUcsRUFBRSxDQUFDLE9BQU8sQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDO1lBQ2xDLE1BQU0sRUFBRSxHQUFHLEVBQUUsQ0FBQyxPQUFPLENBQUMsT0FBTyxDQUFDLFNBQVMsQ0FBQztTQUN6QyxDQUFDLENBQUM7SUFDTCxDQUFDO0lBQ0QsU0FBUyxFQUFFLElBQUk7Q0FDaEIsQ0FBQztBQUVGLGlFQUFlLE1BQU0sRUFBQyIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90aGVtZS1kYXJrLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdGhlbWUtZGFyay1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJVGhlbWVNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogQSBwbHVnaW4gZm9yIHRoZSBKdXB5dGVyIERhcmsgVGhlbWUuXG4gKi9cbmNvbnN0IHBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPHZvaWQ+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL3RoZW1lLWRhcmstZXh0ZW5zaW9uOnBsdWdpbicsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyBhIGRhcmsgdGhlbWUuJyxcbiAgcmVxdWlyZXM6IFtJVGhlbWVNYW5hZ2VyLCBJVHJhbnNsYXRvcl0sXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbWFuYWdlcjogSVRoZW1lTWFuYWdlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHN0eWxlID0gJ0BqdXB5dGVybGFiL3RoZW1lLWRhcmstZXh0ZW5zaW9uL2luZGV4LmNzcyc7XG4gICAgbWFuYWdlci5yZWdpc3Rlcih7XG4gICAgICBuYW1lOiAnSnVweXRlckxhYiBEYXJrJyxcbiAgICAgIGRpc3BsYXlOYW1lOiB0cmFucy5fXygnSnVweXRlckxhYiBEYXJrJyksXG4gICAgICBpc0xpZ2h0OiBmYWxzZSxcbiAgICAgIHRoZW1lU2Nyb2xsYmFyczogdHJ1ZSxcbiAgICAgIGxvYWQ6ICgpID0+IG1hbmFnZXIubG9hZENTUyhzdHlsZSksXG4gICAgICB1bmxvYWQ6ICgpID0+IFByb21pc2UucmVzb2x2ZSh1bmRlZmluZWQpXG4gICAgfSk7XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuZXhwb3J0IGRlZmF1bHQgcGx1Z2luO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9