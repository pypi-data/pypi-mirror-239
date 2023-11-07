"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_settingeditor_lib_tokens_js"],{

/***/ "../packages/settingeditor/lib/tokens.js":
/*!***********************************************!*\
  !*** ../packages/settingeditor/lib/tokens.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IJSONSettingEditorTracker": () => (/* binding */ IJSONSettingEditorTracker),
/* harmony export */   "ISettingEditorTracker": () => (/* binding */ ISettingEditorTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * The setting editor tracker token.
 */
const ISettingEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/settingeditor:ISettingEditorTracker', `A widget tracker for the interactive setting editor.
  Use this if you want to be able to iterate over and interact with setting editors
  created by the application.`);
/**
 * The setting editor tracker token.
 */
const IJSONSettingEditorTracker = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/settingeditor:IJSONSettingEditorTracker', `A widget tracker for the JSON setting editor.
  Use this if you want to be able to iterate over and interact with setting editors
  created by the application.`);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfc2V0dGluZ2VkaXRvcl9saWJfdG9rZW5zX2pzLjVhNmM2MDE4MGU5ODI3MzEzZmQ3LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBR2pCO0FBSTFDOztHQUVHO0FBQ0ksTUFBTSxxQkFBcUIsR0FBRyxJQUFJLG9EQUFLLENBQzVDLGlEQUFpRCxFQUNqRDs7OEJBRTRCLENBQzdCLENBQUM7QUFFRjs7R0FFRztBQUNJLE1BQU0seUJBQXlCLEdBQUcsSUFBSSxvREFBSyxDQUNoRCxxREFBcUQsRUFDckQ7OzhCQUU0QixDQUM3QixDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3NldHRpbmdlZGl0b3Ivc3JjL3Rva2Vucy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IElXaWRnZXRUcmFja2VyLCBNYWluQXJlYVdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSnNvblNldHRpbmdFZGl0b3IgYXMgSlNPTlNldHRpbmdFZGl0b3IgfSBmcm9tICcuL2pzb25zZXR0aW5nZWRpdG9yJztcbmltcG9ydCB7IFNldHRpbmdzRWRpdG9yIH0gZnJvbSAnLi9zZXR0aW5nc2VkaXRvcic7XG5cbi8qKlxuICogVGhlIHNldHRpbmcgZWRpdG9yIHRyYWNrZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJU2V0dGluZ0VkaXRvclRyYWNrZXIgPSBuZXcgVG9rZW48SVNldHRpbmdFZGl0b3JUcmFja2VyPihcbiAgJ0BqdXB5dGVybGFiL3NldHRpbmdlZGl0b3I6SVNldHRpbmdFZGl0b3JUcmFja2VyJyxcbiAgYEEgd2lkZ2V0IHRyYWNrZXIgZm9yIHRoZSBpbnRlcmFjdGl2ZSBzZXR0aW5nIGVkaXRvci5cbiAgVXNlIHRoaXMgaWYgeW91IHdhbnQgdG8gYmUgYWJsZSB0byBpdGVyYXRlIG92ZXIgYW5kIGludGVyYWN0IHdpdGggc2V0dGluZyBlZGl0b3JzXG4gIGNyZWF0ZWQgYnkgdGhlIGFwcGxpY2F0aW9uLmBcbik7XG5cbi8qKlxuICogVGhlIHNldHRpbmcgZWRpdG9yIHRyYWNrZXIgdG9rZW4uXG4gKi9cbmV4cG9ydCBjb25zdCBJSlNPTlNldHRpbmdFZGl0b3JUcmFja2VyID0gbmV3IFRva2VuPElKU09OU2V0dGluZ0VkaXRvclRyYWNrZXI+KFxuICAnQGp1cHl0ZXJsYWIvc2V0dGluZ2VkaXRvcjpJSlNPTlNldHRpbmdFZGl0b3JUcmFja2VyJyxcbiAgYEEgd2lkZ2V0IHRyYWNrZXIgZm9yIHRoZSBKU09OIHNldHRpbmcgZWRpdG9yLlxuICBVc2UgdGhpcyBpZiB5b3Ugd2FudCB0byBiZSBhYmxlIHRvIGl0ZXJhdGUgb3ZlciBhbmQgaW50ZXJhY3Qgd2l0aCBzZXR0aW5nIGVkaXRvcnNcbiAgY3JlYXRlZCBieSB0aGUgYXBwbGljYXRpb24uYFxuKTtcblxuLyoqXG4gKiBBIGNsYXNzIHRoYXQgdHJhY2tzIHRoZSBzZXR0aW5nIGVkaXRvci5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJSlNPTlNldHRpbmdFZGl0b3JUcmFja2VyXG4gIGV4dGVuZHMgSVdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8SlNPTlNldHRpbmdFZGl0b3I+PiB7fVxuXG4vKipcbiAqIEEgY2xhc3MgdGhhdCB0cmFja3MgdGhlIHNldHRpbmcgZWRpdG9yLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElTZXR0aW5nRWRpdG9yVHJhY2tlclxuICBleHRlbmRzIElXaWRnZXRUcmFja2VyPE1haW5BcmVhV2lkZ2V0PFNldHRpbmdzRWRpdG9yPj4ge31cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==