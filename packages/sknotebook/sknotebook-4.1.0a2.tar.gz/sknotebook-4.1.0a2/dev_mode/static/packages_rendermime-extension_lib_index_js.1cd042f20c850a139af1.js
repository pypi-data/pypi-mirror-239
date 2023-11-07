"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_rendermime-extension_lib_index_js"],{

/***/ "../packages/rendermime-extension/lib/index.js":
/*!*****************************************************!*\
  !*** ../packages/rendermime-extension/lib/index.js ***!
  \*****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module rendermime-extension
 */




var CommandIDs;
(function (CommandIDs) {
    CommandIDs.handleLink = 'rendermime:handle-local-link';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin providing a rendermime registry.
 */
const plugin = {
    id: '@jupyterlab/rendermime-extension:plugin',
    description: 'Provides the render mime registry.',
    optional: [
        _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_1__.IDocumentManager,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.ILatexTypesetter,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ISanitizer,
        _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IMarkdownParser,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator
    ],
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.IRenderMimeRegistry,
    activate: activate,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the rendermine plugin.
 */
function activate(app, docManager, latexTypesetter, sanitizer, markdownParser, translator) {
    const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator).load('jupyterlab');
    if (docManager) {
        app.commands.addCommand(CommandIDs.handleLink, {
            label: trans.__('Handle Local Link'),
            execute: args => {
                const path = args['path'];
                const id = args['id'];
                if (!path) {
                    return;
                }
                // First check if the path exists on the server.
                return docManager.services.contents
                    .get(path, { content: false })
                    .then(() => {
                    // Open the link with the default rendered widget factory,
                    // if applicable.
                    const factory = docManager.registry.defaultRenderedWidgetFactory(path);
                    const widget = docManager.openOrReveal(path, factory.name);
                    // Handle the hash if one has been provided.
                    if (widget && id) {
                        widget.setFragment(id);
                    }
                });
            }
        });
    }
    return new _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.RenderMimeRegistry({
        initialFactories: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_2__.standardRendererFactories,
        linkHandler: !docManager
            ? undefined
            : {
                handleLink: (node, path, id) => {
                    // If node has the download attribute explicitly set, use the
                    // default browser downloading behavior.
                    if (node.tagName === 'A' && node.hasAttribute('download')) {
                        return;
                    }
                    app.commandLinker.connectNode(node, CommandIDs.handleLink, {
                        path,
                        id
                    });
                }
            },
        latexTypesetter: latexTypesetter !== null && latexTypesetter !== void 0 ? latexTypesetter : undefined,
        markdownParser: markdownParser !== null && markdownParser !== void 0 ? markdownParser : undefined,
        translator: translator !== null && translator !== void 0 ? translator : undefined,
        sanitizer: sanitizer !== null && sanitizer !== void 0 ? sanitizer : undefined
    });
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfcmVuZGVybWltZS1leHRlbnNpb25fbGliX2luZGV4X2pzLjFjZDA0MmYyMGM4NTBhMTM5YWYxLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQU0rQztBQUNRO0FBUTFCO0FBQ3NDO0FBRXRFLElBQVUsVUFBVSxDQUVuQjtBQUZELFdBQVUsVUFBVTtJQUNMLHFCQUFVLEdBQUcsOEJBQThCLENBQUM7QUFDM0QsQ0FBQyxFQUZTLFVBQVUsS0FBVixVQUFVLFFBRW5CO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBK0M7SUFDekQsRUFBRSxFQUFFLHlDQUF5QztJQUM3QyxXQUFXLEVBQUUsb0NBQW9DO0lBQ2pELFFBQVEsRUFBRTtRQUNSLG9FQUFnQjtRQUNoQixvRUFBZ0I7UUFDaEIsNERBQVU7UUFDVixtRUFBZTtRQUNmLGdFQUFXO0tBQ1o7SUFDRCxRQUFRLEVBQUUsdUVBQW1CO0lBQzdCLFFBQVEsRUFBRSxRQUFRO0lBQ2xCLFNBQVMsRUFBRSxJQUFJO0NBQ2hCLENBQUM7QUFFRjs7R0FFRztBQUNILGlFQUFlLE1BQU0sRUFBQztBQUV0Qjs7R0FFRztBQUNILFNBQVMsUUFBUSxDQUNmLEdBQW9CLEVBQ3BCLFVBQW1DLEVBQ25DLGVBQXdDLEVBQ3hDLFNBQXdDLEVBQ3hDLGNBQXNDLEVBQ3RDLFVBQThCO0lBRTlCLE1BQU0sS0FBSyxHQUFHLENBQUMsVUFBVSxhQUFWLFVBQVUsY0FBVixVQUFVLEdBQUksbUVBQWMsQ0FBQyxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUNoRSxJQUFJLFVBQVUsRUFBRTtRQUNkLEdBQUcsQ0FBQyxRQUFRLENBQUMsVUFBVSxDQUFDLFVBQVUsQ0FBQyxVQUFVLEVBQUU7WUFDN0MsS0FBSyxFQUFFLEtBQUssQ0FBQyxFQUFFLENBQUMsbUJBQW1CLENBQUM7WUFDcEMsT0FBTyxFQUFFLElBQUksQ0FBQyxFQUFFO2dCQUNkLE1BQU0sSUFBSSxHQUFHLElBQUksQ0FBQyxNQUFNLENBQThCLENBQUM7Z0JBQ3ZELE1BQU0sRUFBRSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQThCLENBQUM7Z0JBQ25ELElBQUksQ0FBQyxJQUFJLEVBQUU7b0JBQ1QsT0FBTztpQkFDUjtnQkFDRCxnREFBZ0Q7Z0JBQ2hELE9BQU8sVUFBVSxDQUFDLFFBQVEsQ0FBQyxRQUFRO3FCQUNoQyxHQUFHLENBQUMsSUFBSSxFQUFFLEVBQUUsT0FBTyxFQUFFLEtBQUssRUFBRSxDQUFDO3FCQUM3QixJQUFJLENBQUMsR0FBRyxFQUFFO29CQUNULDBEQUEwRDtvQkFDMUQsaUJBQWlCO29CQUNqQixNQUFNLE9BQU8sR0FDWCxVQUFVLENBQUMsUUFBUSxDQUFDLDRCQUE0QixDQUFDLElBQUksQ0FBQyxDQUFDO29CQUN6RCxNQUFNLE1BQU0sR0FBRyxVQUFVLENBQUMsWUFBWSxDQUFDLElBQUksRUFBRSxPQUFPLENBQUMsSUFBSSxDQUFDLENBQUM7b0JBRTNELDRDQUE0QztvQkFDNUMsSUFBSSxNQUFNLElBQUksRUFBRSxFQUFFO3dCQUNoQixNQUFNLENBQUMsV0FBVyxDQUFDLEVBQUUsQ0FBQyxDQUFDO3FCQUN4QjtnQkFDSCxDQUFDLENBQUMsQ0FBQztZQUNQLENBQUM7U0FDRixDQUFDLENBQUM7S0FDSjtJQUNELE9BQU8sSUFBSSxzRUFBa0IsQ0FBQztRQUM1QixnQkFBZ0IsRUFBRSw2RUFBeUI7UUFDM0MsV0FBVyxFQUFFLENBQUMsVUFBVTtZQUN0QixDQUFDLENBQUMsU0FBUztZQUNYLENBQUMsQ0FBQztnQkFDRSxVQUFVLEVBQUUsQ0FBQyxJQUFpQixFQUFFLElBQVksRUFBRSxFQUFXLEVBQUUsRUFBRTtvQkFDM0QsNkRBQTZEO29CQUM3RCx3Q0FBd0M7b0JBQ3hDLElBQUksSUFBSSxDQUFDLE9BQU8sS0FBSyxHQUFHLElBQUksSUFBSSxDQUFDLFlBQVksQ0FBQyxVQUFVLENBQUMsRUFBRTt3QkFDekQsT0FBTztxQkFDUjtvQkFDRCxHQUFHLENBQUMsYUFBYSxDQUFDLFdBQVcsQ0FBQyxJQUFJLEVBQUUsVUFBVSxDQUFDLFVBQVUsRUFBRTt3QkFDekQsSUFBSTt3QkFDSixFQUFFO3FCQUNILENBQUMsQ0FBQztnQkFDTCxDQUFDO2FBQ0Y7UUFDTCxlQUFlLEVBQUUsZUFBZSxhQUFmLGVBQWUsY0FBZixlQUFlLEdBQUksU0FBUztRQUM3QyxjQUFjLEVBQUUsY0FBYyxhQUFkLGNBQWMsY0FBZCxjQUFjLEdBQUksU0FBUztRQUMzQyxVQUFVLEVBQUUsVUFBVSxhQUFWLFVBQVUsY0FBVixVQUFVLEdBQUksU0FBUztRQUNuQyxTQUFTLEVBQUUsU0FBUyxhQUFULFNBQVMsY0FBVCxTQUFTLEdBQUksU0FBUztLQUNsQyxDQUFDLENBQUM7QUFDTCxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3JlbmRlcm1pbWUtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHJlbmRlcm1pbWUtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgSVNhbml0aXplciB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IElEb2N1bWVudE1hbmFnZXIgfSBmcm9tICdAanVweXRlcmxhYi9kb2NtYW5hZ2VyJztcbmltcG9ydCB7XG4gIElMYXRleFR5cGVzZXR0ZXIsXG4gIElNYXJrZG93blBhcnNlcixcbiAgSVJlbmRlck1pbWUsXG4gIElSZW5kZXJNaW1lUmVnaXN0cnksXG4gIFJlbmRlck1pbWVSZWdpc3RyeSxcbiAgc3RhbmRhcmRSZW5kZXJlckZhY3Rvcmllc1xufSBmcm9tICdAanVweXRlcmxhYi9yZW5kZXJtaW1lJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcblxubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgaGFuZGxlTGluayA9ICdyZW5kZXJtaW1lOmhhbmRsZS1sb2NhbC1saW5rJztcbn1cblxuLyoqXG4gKiBBIHBsdWdpbiBwcm92aWRpbmcgYSByZW5kZXJtaW1lIHJlZ2lzdHJ5LlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJUmVuZGVyTWltZVJlZ2lzdHJ5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9yZW5kZXJtaW1lLWV4dGVuc2lvbjpwbHVnaW4nLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIHRoZSByZW5kZXIgbWltZSByZWdpc3RyeS4nLFxuICBvcHRpb25hbDogW1xuICAgIElEb2N1bWVudE1hbmFnZXIsXG4gICAgSUxhdGV4VHlwZXNldHRlcixcbiAgICBJU2FuaXRpemVyLFxuICAgIElNYXJrZG93blBhcnNlcixcbiAgICBJVHJhbnNsYXRvclxuICBdLFxuICBwcm92aWRlczogSVJlbmRlck1pbWVSZWdpc3RyeSxcbiAgYWN0aXZhdGU6IGFjdGl2YXRlLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW4gYXMgZGVmYXVsdC5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2luO1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSByZW5kZXJtaW5lIHBsdWdpbi5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICBkb2NNYW5hZ2VyOiBJRG9jdW1lbnRNYW5hZ2VyIHwgbnVsbCxcbiAgbGF0ZXhUeXBlc2V0dGVyOiBJTGF0ZXhUeXBlc2V0dGVyIHwgbnVsbCxcbiAgc2FuaXRpemVyOiBJUmVuZGVyTWltZS5JU2FuaXRpemVyIHwgbnVsbCxcbiAgbWFya2Rvd25QYXJzZXI6IElNYXJrZG93blBhcnNlciB8IG51bGwsXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yIHwgbnVsbFxuKTogUmVuZGVyTWltZVJlZ2lzdHJ5IHtcbiAgY29uc3QgdHJhbnMgPSAodHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvcikubG9hZCgnanVweXRlcmxhYicpO1xuICBpZiAoZG9jTWFuYWdlcikge1xuICAgIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuaGFuZGxlTGluaywge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdIYW5kbGUgTG9jYWwgTGluaycpLFxuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHBhdGggPSBhcmdzWydwYXRoJ10gYXMgc3RyaW5nIHwgdW5kZWZpbmVkIHwgbnVsbDtcbiAgICAgICAgY29uc3QgaWQgPSBhcmdzWydpZCddIGFzIHN0cmluZyB8IHVuZGVmaW5lZCB8IG51bGw7XG4gICAgICAgIGlmICghcGF0aCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICAvLyBGaXJzdCBjaGVjayBpZiB0aGUgcGF0aCBleGlzdHMgb24gdGhlIHNlcnZlci5cbiAgICAgICAgcmV0dXJuIGRvY01hbmFnZXIuc2VydmljZXMuY29udGVudHNcbiAgICAgICAgICAuZ2V0KHBhdGgsIHsgY29udGVudDogZmFsc2UgfSlcbiAgICAgICAgICAudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAvLyBPcGVuIHRoZSBsaW5rIHdpdGggdGhlIGRlZmF1bHQgcmVuZGVyZWQgd2lkZ2V0IGZhY3RvcnksXG4gICAgICAgICAgICAvLyBpZiBhcHBsaWNhYmxlLlxuICAgICAgICAgICAgY29uc3QgZmFjdG9yeSA9XG4gICAgICAgICAgICAgIGRvY01hbmFnZXIucmVnaXN0cnkuZGVmYXVsdFJlbmRlcmVkV2lkZ2V0RmFjdG9yeShwYXRoKTtcbiAgICAgICAgICAgIGNvbnN0IHdpZGdldCA9IGRvY01hbmFnZXIub3Blbk9yUmV2ZWFsKHBhdGgsIGZhY3RvcnkubmFtZSk7XG5cbiAgICAgICAgICAgIC8vIEhhbmRsZSB0aGUgaGFzaCBpZiBvbmUgaGFzIGJlZW4gcHJvdmlkZWQuXG4gICAgICAgICAgICBpZiAod2lkZ2V0ICYmIGlkKSB7XG4gICAgICAgICAgICAgIHdpZGdldC5zZXRGcmFnbWVudChpZCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG4gIH1cbiAgcmV0dXJuIG5ldyBSZW5kZXJNaW1lUmVnaXN0cnkoe1xuICAgIGluaXRpYWxGYWN0b3JpZXM6IHN0YW5kYXJkUmVuZGVyZXJGYWN0b3JpZXMsXG4gICAgbGlua0hhbmRsZXI6ICFkb2NNYW5hZ2VyXG4gICAgICA/IHVuZGVmaW5lZFxuICAgICAgOiB7XG4gICAgICAgICAgaGFuZGxlTGluazogKG5vZGU6IEhUTUxFbGVtZW50LCBwYXRoOiBzdHJpbmcsIGlkPzogc3RyaW5nKSA9PiB7XG4gICAgICAgICAgICAvLyBJZiBub2RlIGhhcyB0aGUgZG93bmxvYWQgYXR0cmlidXRlIGV4cGxpY2l0bHkgc2V0LCB1c2UgdGhlXG4gICAgICAgICAgICAvLyBkZWZhdWx0IGJyb3dzZXIgZG93bmxvYWRpbmcgYmVoYXZpb3IuXG4gICAgICAgICAgICBpZiAobm9kZS50YWdOYW1lID09PSAnQScgJiYgbm9kZS5oYXNBdHRyaWJ1dGUoJ2Rvd25sb2FkJykpIHtcbiAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgYXBwLmNvbW1hbmRMaW5rZXIuY29ubmVjdE5vZGUobm9kZSwgQ29tbWFuZElEcy5oYW5kbGVMaW5rLCB7XG4gICAgICAgICAgICAgIHBhdGgsXG4gICAgICAgICAgICAgIGlkXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICB9XG4gICAgICAgIH0sXG4gICAgbGF0ZXhUeXBlc2V0dGVyOiBsYXRleFR5cGVzZXR0ZXIgPz8gdW5kZWZpbmVkLFxuICAgIG1hcmtkb3duUGFyc2VyOiBtYXJrZG93blBhcnNlciA/PyB1bmRlZmluZWQsXG4gICAgdHJhbnNsYXRvcjogdHJhbnNsYXRvciA/PyB1bmRlZmluZWQsXG4gICAgc2FuaXRpemVyOiBzYW5pdGl6ZXIgPz8gdW5kZWZpbmVkXG4gIH0pO1xufVxuIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9