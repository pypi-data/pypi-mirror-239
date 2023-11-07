"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_cell-toolbar-extension_lib_index_js"],{

/***/ "../packages/cell-toolbar-extension/lib/index.js":
/*!*******************************************************!*\
  !*** ../packages/cell-toolbar-extension/lib/index.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/cell-toolbar */ "webpack/sharing/consume/default/@jupyterlab/cell-toolbar/@jupyterlab/cell-toolbar");
/* harmony import */ var _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module cell-toolbar-extension
 */




const cellToolbar = {
    id: '@jupyterlab/cell-toolbar-extension:plugin',
    description: 'Add the cells toolbar.',
    autoStart: true,
    activate: async (app, settingRegistry, toolbarRegistry, translator) => {
        const toolbarItems = settingRegistry && toolbarRegistry
            ? (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.createToolbarFactory)(toolbarRegistry, settingRegistry, _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__.CellBarExtension.FACTORY_NAME, cellToolbar.id, translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator)
            : undefined;
        app.docRegistry.addWidgetExtension('Notebook', new _jupyterlab_cell_toolbar__WEBPACK_IMPORTED_MODULE_1__.CellBarExtension(app.commands, toolbarItems));
    },
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.IToolbarWidgetRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator]
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (cellToolbar);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY2VsbC10b29sYmFyLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuYzc2MzcwYWM3YTIyOWM2MTAxNTAuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUE7OzsrRUFHK0U7QUFDL0U7OztHQUdHO0FBTTREO0FBQ0g7QUFJOUI7QUFDd0M7QUFFdEUsTUFBTSxXQUFXLEdBQWdDO0lBQy9DLEVBQUUsRUFBRSwyQ0FBMkM7SUFDL0MsV0FBVyxFQUFFLHdCQUF3QjtJQUNyQyxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxLQUFLLEVBQ2IsR0FBb0IsRUFDcEIsZUFBd0MsRUFDeEMsZUFBOEMsRUFDOUMsVUFBOEIsRUFDOUIsRUFBRTtRQUNGLE1BQU0sWUFBWSxHQUNoQixlQUFlLElBQUksZUFBZTtZQUNoQyxDQUFDLENBQUMsMEVBQW9CLENBQ2xCLGVBQWUsRUFDZixlQUFlLEVBQ2YsbUZBQTZCLEVBQzdCLFdBQVcsQ0FBQyxFQUFFLEVBQ2QsVUFBVSxhQUFWLFVBQVUsY0FBVixVQUFVLEdBQUksbUVBQWMsQ0FDN0I7WUFDSCxDQUFDLENBQUMsU0FBUyxDQUFDO1FBRWhCLEdBQUcsQ0FBQyxXQUFXLENBQUMsa0JBQWtCLENBQ2hDLFVBQVUsRUFDVixJQUFJLHNFQUFnQixDQUFDLEdBQUcsQ0FBQyxRQUFRLEVBQUUsWUFBWSxDQUFDLENBQ2pELENBQUM7SUFDSixDQUFDO0lBQ0QsUUFBUSxFQUFFLENBQUMseUVBQWdCLEVBQUUsd0VBQXNCLEVBQUUsZ0VBQVcsQ0FBQztDQUNsRSxDQUFDO0FBRUYsaUVBQWUsV0FBVyxFQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NlbGwtdG9vbGJhci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgY2VsbC10b29sYmFyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9zZXR0aW5ncmVnaXN0cnknO1xuaW1wb3J0IHsgQ2VsbEJhckV4dGVuc2lvbiB9IGZyb20gJ0BqdXB5dGVybGFiL2NlbGwtdG9vbGJhcic7XG5pbXBvcnQge1xuICBjcmVhdGVUb29sYmFyRmFjdG9yeSxcbiAgSVRvb2xiYXJXaWRnZXRSZWdpc3RyeVxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbmNvbnN0IGNlbGxUb29sYmFyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvY2VsbC10b29sYmFyLWV4dGVuc2lvbjpwbHVnaW4nLFxuICBkZXNjcmlwdGlvbjogJ0FkZCB0aGUgY2VsbHMgdG9vbGJhci4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiBhc3luYyAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgc2V0dGluZ1JlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbCxcbiAgICB0b29sYmFyUmVnaXN0cnk6IElUb29sYmFyV2lkZ2V0UmVnaXN0cnkgfCBudWxsLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbFxuICApID0+IHtcbiAgICBjb25zdCB0b29sYmFySXRlbXMgPVxuICAgICAgc2V0dGluZ1JlZ2lzdHJ5ICYmIHRvb2xiYXJSZWdpc3RyeVxuICAgICAgICA/IGNyZWF0ZVRvb2xiYXJGYWN0b3J5KFxuICAgICAgICAgICAgdG9vbGJhclJlZ2lzdHJ5LFxuICAgICAgICAgICAgc2V0dGluZ1JlZ2lzdHJ5LFxuICAgICAgICAgICAgQ2VsbEJhckV4dGVuc2lvbi5GQUNUT1JZX05BTUUsXG4gICAgICAgICAgICBjZWxsVG9vbGJhci5pZCxcbiAgICAgICAgICAgIHRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3JcbiAgICAgICAgICApXG4gICAgICAgIDogdW5kZWZpbmVkO1xuXG4gICAgYXBwLmRvY1JlZ2lzdHJ5LmFkZFdpZGdldEV4dGVuc2lvbihcbiAgICAgICdOb3RlYm9vaycsXG4gICAgICBuZXcgQ2VsbEJhckV4dGVuc2lvbihhcHAuY29tbWFuZHMsIHRvb2xiYXJJdGVtcylcbiAgICApO1xuICB9LFxuICBvcHRpb25hbDogW0lTZXR0aW5nUmVnaXN0cnksIElUb29sYmFyV2lkZ2V0UmVnaXN0cnksIElUcmFuc2xhdG9yXVxufTtcblxuZXhwb3J0IGRlZmF1bHQgY2VsbFRvb2xiYXI7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=