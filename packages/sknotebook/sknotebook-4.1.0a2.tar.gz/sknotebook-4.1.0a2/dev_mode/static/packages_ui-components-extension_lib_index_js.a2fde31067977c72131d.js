"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_ui-components-extension_lib_index_js"],{

/***/ "../packages/ui-components-extension/lib/index.js":
/*!********************************************************!*\
  !*** ../packages/ui-components-extension/lib/index.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module ui-components-extension
 */

/**
 * Placeholder for future extension that will provide an icon manager class
 * to assist with overriding/replacing particular sets of icons
 */
const labiconManager = {
    id: '@jupyterlab/ui-components-extension:labicon-manager',
    description: 'Provides the icon manager.',
    provides: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.ILabIconManager,
    autoStart: true,
    activate: (app) => {
        return Object.create(null);
    }
};
/**
 * Sets up the renderer registry to be used by the FormEditor component.
 */
const formRendererRegistryPlugin = {
    id: '@jupyterlab/ui-components-extension:form-renderer-registry',
    description: 'Provides the settings form renderer registry.',
    provides: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.IFormRendererRegistry,
    autoStart: true,
    activate: (app) => {
        const formRendererRegistry = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.FormRendererRegistry();
        return formRendererRegistry;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([labiconManager, formRendererRegistryPlugin]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdWktY29tcG9uZW50cy1leHRlbnNpb25fbGliX2luZGV4X2pzLmEyZmRlMzEwNjc5NzdjNzIxMzFkLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBVWdDO0FBRW5DOzs7R0FHRztBQUNILE1BQU0sY0FBYyxHQUEyQztJQUM3RCxFQUFFLEVBQUUscURBQXFEO0lBQ3pELFdBQVcsRUFBRSw0QkFBNEI7SUFDekMsUUFBUSxFQUFFLHNFQUFlO0lBQ3pCLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQUMsR0FBb0IsRUFBRSxFQUFFO1FBQ2pDLE9BQU8sTUFBTSxDQUFDLE1BQU0sQ0FBQyxJQUFJLENBQUMsQ0FBQztJQUM3QixDQUFDO0NBQ0YsQ0FBQztBQUVGOztHQUVHO0FBQ0gsTUFBTSwwQkFBMEIsR0FDOUI7SUFDRSxFQUFFLEVBQUUsNERBQTREO0lBQ2hFLFdBQVcsRUFBRSwrQ0FBK0M7SUFDNUQsUUFBUSxFQUFFLDRFQUFxQjtJQUMvQixTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLEdBQW9CLEVBQXlCLEVBQUU7UUFDeEQsTUFBTSxvQkFBb0IsR0FBRyxJQUFJLDJFQUFvQixFQUFFLENBQUM7UUFDeEQsT0FBTyxvQkFBb0IsQ0FBQztJQUM5QixDQUFDO0NBQ0YsQ0FBQztBQUVKLGlFQUFlLENBQUMsY0FBYyxFQUFFLDBCQUEwQixDQUFDLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdWktY29tcG9uZW50cy1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHVpLWNvbXBvbmVudHMtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgRm9ybVJlbmRlcmVyUmVnaXN0cnksXG4gIElGb3JtUmVuZGVyZXJSZWdpc3RyeSxcbiAgSUxhYkljb25NYW5hZ2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMnO1xuXG4vKipcbiAqIFBsYWNlaG9sZGVyIGZvciBmdXR1cmUgZXh0ZW5zaW9uIHRoYXQgd2lsbCBwcm92aWRlIGFuIGljb24gbWFuYWdlciBjbGFzc1xuICogdG8gYXNzaXN0IHdpdGggb3ZlcnJpZGluZy9yZXBsYWNpbmcgcGFydGljdWxhciBzZXRzIG9mIGljb25zXG4gKi9cbmNvbnN0IGxhYmljb25NYW5hZ2VyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUxhYkljb25NYW5hZ2VyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzLWV4dGVuc2lvbjpsYWJpY29uLW1hbmFnZXInLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSBpY29uIG1hbmFnZXIuJyxcbiAgcHJvdmlkZXM6IElMYWJJY29uTWFuYWdlcixcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKSA9PiB7XG4gICAgcmV0dXJuIE9iamVjdC5jcmVhdGUobnVsbCk7XG4gIH1cbn07XG5cbi8qKlxuICogU2V0cyB1cCB0aGUgcmVuZGVyZXIgcmVnaXN0cnkgdG8gYmUgdXNlZCBieSB0aGUgRm9ybUVkaXRvciBjb21wb25lbnQuXG4gKi9cbmNvbnN0IGZvcm1SZW5kZXJlclJlZ2lzdHJ5UGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SUZvcm1SZW5kZXJlclJlZ2lzdHJ5PiA9XG4gIHtcbiAgICBpZDogJ0BqdXB5dGVybGFiL3VpLWNvbXBvbmVudHMtZXh0ZW5zaW9uOmZvcm0tcmVuZGVyZXItcmVnaXN0cnknLFxuICAgIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIHNldHRpbmdzIGZvcm0gcmVuZGVyZXIgcmVnaXN0cnkuJyxcbiAgICBwcm92aWRlczogSUZvcm1SZW5kZXJlclJlZ2lzdHJ5LFxuICAgIGF1dG9TdGFydDogdHJ1ZSxcbiAgICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKTogSUZvcm1SZW5kZXJlclJlZ2lzdHJ5ID0+IHtcbiAgICAgIGNvbnN0IGZvcm1SZW5kZXJlclJlZ2lzdHJ5ID0gbmV3IEZvcm1SZW5kZXJlclJlZ2lzdHJ5KCk7XG4gICAgICByZXR1cm4gZm9ybVJlbmRlcmVyUmVnaXN0cnk7XG4gICAgfVxuICB9O1xuXG5leHBvcnQgZGVmYXVsdCBbbGFiaWNvbk1hbmFnZXIsIGZvcm1SZW5kZXJlclJlZ2lzdHJ5UGx1Z2luXTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==