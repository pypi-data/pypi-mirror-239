"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mermaid-extension_lib_index_js-_c5ed1"],{

/***/ "../packages/mermaid-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../packages/mermaid-extension/lib/index.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/mermaid */ "webpack/sharing/consume/default/@jupyterlab/mermaid/@jupyterlab/mermaid");
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * A namespace for mermaid text-based diagram commands.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.copySource = 'mermaid:copy-source';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin for the core rendering/cachine of mermaid text-based diagrams
 */
const core = {
    id: '@jupyterlab/mermaid-extension:core',
    description: 'Provides the Mermaid manager.',
    autoStart: true,
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    provides: _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidManager,
    activate: (app, themes) => {
        const manager = new _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MermaidManager({ themes });
        _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.RenderedMermaid.manager = manager;
        return manager;
    }
};
/**
 * A plugin for rendering mermaid text-based diagrams in markdown fenced code blocks
 */
const markdown = {
    id: '@jupyterlab/mermaid-extension:markdown',
    description: 'Provides the Mermaid markdown renderer.',
    autoStart: true,
    requires: [_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidManager],
    provides: _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidMarkdown,
    activate: (app, mermaid) => {
        return new _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MermaidMarkdown({ mermaid });
    }
};
/**
 * Contextual commands for mermaid text-based diagrams.
 */
const contextCommands = {
    id: '@jupyterlab/mermaid-extension:context-commands',
    description: 'Provides context menu commands for mermaid diagrams.',
    autoStart: true,
    requires: [_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.IMermaidManager],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator],
    activate: (app, mermaid, translator) => {
        const isMermaid = (node) => node.classList.contains(_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MERMAID_CLASS);
        const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator).load('jupyterlab');
        app.commands.addCommand(CommandIDs.copySource, {
            label: trans.__('Mermaid Copy Diagram Source'),
            execute: async (args) => {
                const node = app.contextMenuHitTest(isMermaid);
                if (!node) {
                    return;
                }
                const code = node.querySelector(`.${_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MERMAID_CODE_CLASS}`);
                if (!code || !code.textContent) {
                    return;
                }
                await navigator.clipboard.writeText(code.textContent);
            }
        });
        const options = { selector: `.${_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_1__.MERMAID_CLASS}`, rank: 13 };
        app.contextMenu.addItem({ command: CommandIDs.copySource, ...options });
        app.contextMenu.addItem({ type: 'separator', ...options });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([core, markdown, contextCommands]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWVybWFpZC1leHRlbnNpb25fbGliX2luZGV4X2pzLV9jNWVkMS4xMDQzZjI2MDNhOWJkYmU4Mjk5Yi5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFXTjtBQVN4QjtBQUN5QztBQUV0RTs7R0FFRztBQUNJLElBQVUsVUFBVSxDQUUxQjtBQUZELFdBQWlCLFVBQVU7SUFDWixxQkFBVSxHQUFHLHFCQUFxQixDQUFDO0FBQ2xELENBQUMsRUFGZ0IsVUFBVSxLQUFWLFVBQVUsUUFFMUI7QUFFRDs7R0FFRztBQUNILE1BQU0sSUFBSSxHQUEyQztJQUNuRCxFQUFFLEVBQUUsb0NBQW9DO0lBQ3hDLFdBQVcsRUFBRSwrQkFBK0I7SUFDNUMsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FBQywrREFBYSxDQUFDO0lBQ3pCLFFBQVEsRUFBRSxnRUFBZTtJQUN6QixRQUFRLEVBQUUsQ0FBQyxHQUFvQixFQUFFLE1BQTRCLEVBQUUsRUFBRTtRQUMvRCxNQUFNLE9BQU8sR0FBRyxJQUFJLCtEQUFjLENBQUMsRUFBRSxNQUFNLEVBQUUsQ0FBQyxDQUFDO1FBQy9DLHdFQUF1QixHQUFHLE9BQU8sQ0FBQztRQUNsQyxPQUFPLE9BQU8sQ0FBQztJQUNqQixDQUFDO0NBQ0YsQ0FBQztBQUVGOztHQUVHO0FBQ0gsTUFBTSxRQUFRLEdBQTRDO0lBQ3hELEVBQUUsRUFBRSx3Q0FBd0M7SUFDNUMsV0FBVyxFQUFFLHlDQUF5QztJQUN0RCxTQUFTLEVBQUUsSUFBSTtJQUNmLFFBQVEsRUFBRSxDQUFDLGdFQUFlLENBQUM7SUFDM0IsUUFBUSxFQUFFLGlFQUFnQjtJQUMxQixRQUFRLEVBQUUsQ0FBQyxHQUFvQixFQUFFLE9BQXdCLEVBQUUsRUFBRTtRQUMzRCxPQUFPLElBQUksZ0VBQWUsQ0FBQyxFQUFFLE9BQU8sRUFBRSxDQUFDLENBQUM7SUFDMUMsQ0FBQztDQUNGLENBQUM7QUFFRjs7R0FFRztBQUNILE1BQU0sZUFBZSxHQUFnQztJQUNuRCxFQUFFLEVBQUUsZ0RBQWdEO0lBQ3BELFdBQVcsRUFBRSxzREFBc0Q7SUFDbkUsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsQ0FBQyxnRUFBZSxDQUFDO0lBQzNCLFFBQVEsRUFBRSxDQUFDLGdFQUFXLENBQUM7SUFDdkIsUUFBUSxFQUFFLENBQ1IsR0FBb0IsRUFDcEIsT0FBd0IsRUFDeEIsVUFBOEIsRUFDOUIsRUFBRTtRQUNGLE1BQU0sU0FBUyxHQUFHLENBQUMsSUFBaUIsRUFBRSxFQUFFLENBQ3RDLElBQUksQ0FBQyxTQUFTLENBQUMsUUFBUSxDQUFDLDhEQUFhLENBQUMsQ0FBQztRQUV6QyxNQUFNLEtBQUssR0FBRyxDQUFDLFVBQVUsYUFBVixVQUFVLGNBQVYsVUFBVSxHQUFJLG1FQUFjLENBQUMsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDaEUsR0FBRyxDQUFDLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLFVBQVUsRUFBRTtZQUM3QyxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyw2QkFBNkIsQ0FBQztZQUM5QyxPQUFPLEVBQUUsS0FBSyxFQUFFLElBQVUsRUFBRSxFQUFFO2dCQUM1QixNQUFNLElBQUksR0FBRyxHQUFHLENBQUMsa0JBQWtCLENBQUMsU0FBUyxDQUFDLENBQUM7Z0JBQy9DLElBQUksQ0FBQyxJQUFJLEVBQUU7b0JBQ1QsT0FBTztpQkFDUjtnQkFDRCxNQUFNLElBQUksR0FBRyxJQUFJLENBQUMsYUFBYSxDQUFDLElBQUksbUVBQWtCLEVBQUUsQ0FBQyxDQUFDO2dCQUMxRCxJQUFJLENBQUMsSUFBSSxJQUFJLENBQUMsSUFBSSxDQUFDLFdBQVcsRUFBRTtvQkFDOUIsT0FBTztpQkFDUjtnQkFDRCxNQUFNLFNBQVMsQ0FBQyxTQUFTLENBQUMsU0FBUyxDQUFDLElBQUksQ0FBQyxXQUFXLENBQUMsQ0FBQztZQUN4RCxDQUFDO1NBQ0YsQ0FBQyxDQUFDO1FBRUgsTUFBTSxPQUFPLEdBQUcsRUFBRSxRQUFRLEVBQUUsSUFBSSw4REFBYSxFQUFFLEVBQUUsSUFBSSxFQUFFLEVBQUUsRUFBRSxDQUFDO1FBQzVELEdBQUcsQ0FBQyxXQUFXLENBQUMsT0FBTyxDQUFDLEVBQUUsT0FBTyxFQUFFLFVBQVUsQ0FBQyxVQUFVLEVBQUUsR0FBRyxPQUFPLEVBQUUsQ0FBQyxDQUFDO1FBQ3hFLEdBQUcsQ0FBQyxXQUFXLENBQUMsT0FBTyxDQUFDLEVBQUUsSUFBSSxFQUFFLFdBQVcsRUFBRSxHQUFHLE9BQU8sRUFBRSxDQUFDLENBQUM7SUFDN0QsQ0FBQztDQUNGLENBQUM7QUFFRixpRUFBZSxDQUFDLElBQUksRUFBRSxRQUFRLEVBQUUsZUFBZSxDQUFDLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbWVybWFpZC1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWVybWFpZC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJVGhlbWVNYW5hZ2VyIH0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwdXRpbHMnO1xuaW1wb3J0IHtcbiAgSU1lcm1haWRNYW5hZ2VyLFxuICBJTWVybWFpZE1hcmtkb3duLFxuICBNRVJNQUlEX0NMQVNTLFxuICBNRVJNQUlEX0NPREVfQ0xBU1MsXG4gIE1lcm1haWRNYW5hZ2VyLFxuICBNZXJtYWlkTWFya2Rvd24sXG4gIFJlbmRlcmVkTWVybWFpZFxufSBmcm9tICdAanVweXRlcmxhYi9tZXJtYWlkJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgbWVybWFpZCB0ZXh0LWJhc2VkIGRpYWdyYW0gY29tbWFuZHMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjb3B5U291cmNlID0gJ21lcm1haWQ6Y29weS1zb3VyY2UnO1xufVxuXG4vKipcbiAqIEEgcGx1Z2luIGZvciB0aGUgY29yZSByZW5kZXJpbmcvY2FjaGluZSBvZiBtZXJtYWlkIHRleHQtYmFzZWQgZGlhZ3JhbXNcbiAqL1xuY29uc3QgY29yZTogSnVweXRlckZyb250RW5kUGx1Z2luPElNZXJtYWlkTWFuYWdlcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvbWVybWFpZC1leHRlbnNpb246Y29yZScsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIE1lcm1haWQgbWFuYWdlci4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIG9wdGlvbmFsOiBbSVRoZW1lTWFuYWdlcl0sXG4gIHByb3ZpZGVzOiBJTWVybWFpZE1hbmFnZXIsXG4gIGFjdGl2YXRlOiAoYXBwOiBKdXB5dGVyRnJvbnRFbmQsIHRoZW1lczogSVRoZW1lTWFuYWdlciB8IG51bGwpID0+IHtcbiAgICBjb25zdCBtYW5hZ2VyID0gbmV3IE1lcm1haWRNYW5hZ2VyKHsgdGhlbWVzIH0pO1xuICAgIFJlbmRlcmVkTWVybWFpZC5tYW5hZ2VyID0gbWFuYWdlcjtcbiAgICByZXR1cm4gbWFuYWdlcjtcbiAgfVxufTtcblxuLyoqXG4gKiBBIHBsdWdpbiBmb3IgcmVuZGVyaW5nIG1lcm1haWQgdGV4dC1iYXNlZCBkaWFncmFtcyBpbiBtYXJrZG93biBmZW5jZWQgY29kZSBibG9ja3NcbiAqL1xuY29uc3QgbWFya2Rvd246IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTWVybWFpZE1hcmtkb3duPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9tZXJtYWlkLWV4dGVuc2lvbjptYXJrZG93bicsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIE1lcm1haWQgbWFya2Rvd24gcmVuZGVyZXIuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lNZXJtYWlkTWFuYWdlcl0sXG4gIHByb3ZpZGVzOiBJTWVybWFpZE1hcmtkb3duLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kLCBtZXJtYWlkOiBJTWVybWFpZE1hbmFnZXIpID0+IHtcbiAgICByZXR1cm4gbmV3IE1lcm1haWRNYXJrZG93bih7IG1lcm1haWQgfSk7XG4gIH1cbn07XG5cbi8qKlxuICogQ29udGV4dHVhbCBjb21tYW5kcyBmb3IgbWVybWFpZCB0ZXh0LWJhc2VkIGRpYWdyYW1zLlxuICovXG5jb25zdCBjb250ZXh0Q29tbWFuZHM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjx2b2lkPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9tZXJtYWlkLWV4dGVuc2lvbjpjb250ZXh0LWNvbW1hbmRzJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyBjb250ZXh0IG1lbnUgY29tbWFuZHMgZm9yIG1lcm1haWQgZGlhZ3JhbXMuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICByZXF1aXJlczogW0lNZXJtYWlkTWFuYWdlcl0sXG4gIG9wdGlvbmFsOiBbSVRyYW5zbGF0b3JdLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIG1lcm1haWQ6IElNZXJtYWlkTWFuYWdlcixcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvciB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgaXNNZXJtYWlkID0gKG5vZGU6IEhUTUxFbGVtZW50KSA9PlxuICAgICAgbm9kZS5jbGFzc0xpc3QuY29udGFpbnMoTUVSTUFJRF9DTEFTUyk7XG5cbiAgICBjb25zdCB0cmFucyA9ICh0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5U291cmNlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ01lcm1haWQgQ29weSBEaWFncmFtIFNvdXJjZScpLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKGFyZ3M/OiBhbnkpID0+IHtcbiAgICAgICAgY29uc3Qgbm9kZSA9IGFwcC5jb250ZXh0TWVudUhpdFRlc3QoaXNNZXJtYWlkKTtcbiAgICAgICAgaWYgKCFub2RlKSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IGNvZGUgPSBub2RlLnF1ZXJ5U2VsZWN0b3IoYC4ke01FUk1BSURfQ09ERV9DTEFTU31gKTtcbiAgICAgICAgaWYgKCFjb2RlIHx8ICFjb2RlLnRleHRDb250ZW50KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG4gICAgICAgIGF3YWl0IG5hdmlnYXRvci5jbGlwYm9hcmQud3JpdGVUZXh0KGNvZGUudGV4dENvbnRlbnQpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29uc3Qgb3B0aW9ucyA9IHsgc2VsZWN0b3I6IGAuJHtNRVJNQUlEX0NMQVNTfWAsIHJhbms6IDEzIH07XG4gICAgYXBwLmNvbnRleHRNZW51LmFkZEl0ZW0oeyBjb21tYW5kOiBDb21tYW5kSURzLmNvcHlTb3VyY2UsIC4uLm9wdGlvbnMgfSk7XG4gICAgYXBwLmNvbnRleHRNZW51LmFkZEl0ZW0oeyB0eXBlOiAnc2VwYXJhdG9yJywgLi4ub3B0aW9ucyB9KTtcbiAgfVxufTtcblxuZXhwb3J0IGRlZmF1bHQgW2NvcmUsIG1hcmtkb3duLCBjb250ZXh0Q29tbWFuZHNdO1xuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9