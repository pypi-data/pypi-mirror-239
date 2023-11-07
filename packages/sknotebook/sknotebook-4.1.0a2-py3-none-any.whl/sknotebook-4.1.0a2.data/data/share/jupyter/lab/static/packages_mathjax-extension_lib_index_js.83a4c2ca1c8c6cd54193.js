"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_mathjax-extension_lib_index_js"],{

/***/ "../packages/mathjax-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../packages/mathjax-extension/lib/index.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MathJaxTypesetter": () => (/* binding */ MathJaxTypesetter),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module mathjax-extension
 */


var CommandIDs;
(function (CommandIDs) {
    /**
     * Copy raw LaTeX to clipboard.
     */
    CommandIDs.copy = 'mathjax:clipboard';
    /**
     * Scale MathJax elements.
     */
    CommandIDs.scale = 'mathjax:scale';
})(CommandIDs || (CommandIDs = {}));
/**
 * The MathJax Typesetter.
 */
class MathJaxTypesetter {
    constructor() {
        this._initialized = false;
    }
    async _ensureInitialized() {
        if (!this._initialized) {
            this._mathDocument = await Private.ensureMathDocument();
            this._initialized = true;
        }
    }
    /**
     * Get an instance of the MathDocument object.
     */
    async mathDocument() {
        await this._ensureInitialized();
        return this._mathDocument;
    }
    /**
     * Typeset the math in a node.
     */
    async typeset(node) {
        try {
            await this._ensureInitialized();
        }
        catch (e) {
            console.error(e);
            return;
        }
        this._mathDocument.options.elements = [node];
        this._mathDocument.clear().render();
        delete this._mathDocument.options.elements;
    }
}
/**
 * The MathJax extension.
 */
const mathJaxPlugin = {
    id: '@jupyterlab/mathjax-extension:plugin',
    description: 'Provides the LaTeX mathematical expression interpreter.',
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_1__.ILatexTypesetter,
    activate: (app) => {
        const typesetter = new MathJaxTypesetter();
        app.commands.addCommand(CommandIDs.copy, {
            execute: async () => {
                const md = await typesetter.mathDocument();
                const oJax = md.outputJax;
                await navigator.clipboard.writeText(oJax.math.math);
            },
            label: 'MathJax Copy Latex'
        });
        app.commands.addCommand(CommandIDs.scale, {
            execute: async (args) => {
                const md = await typesetter.mathDocument();
                const scale = args['scale'] || 1.0;
                md.outputJax.options.scale = scale;
                md.rerender();
            },
            label: args => 'Mathjax Scale ' + (args['scale'] ? `x${args['scale']}` : 'Reset')
        });
        return typesetter;
    },
    autoStart: true
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (mathJaxPlugin);
/**
 * A namespace for module-private functionality.
 */
var Private;
(function (Private) {
    let _loading = null;
    async function ensureMathDocument() {
        if (!_loading) {
            _loading = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
            void Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlNodes_mo_js-node_modules_mathjax-full_js-e92534"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_Configuration_js-node_modules_mathjax-full_js_-8c4c26"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_require_RequireConfiguration_js")]).then(__webpack_require__.t.bind(__webpack_require__, /*! mathjax-full/js/input/tex/require/RequireConfiguration */ "../node_modules/mathjax-full/js/input/tex/require/RequireConfiguration.js", 23));
            const [{ mathjax }, { CHTML }, { TeX }, { TeXFont }, { AllPackages }, { SafeHandler }, { HTMLHandler }, { browserAdaptor }, { AssistiveMmlHandler }] = await Promise.all([
                __webpack_require__.e(/*! import() */ "node_modules_mathjax-full_js_mathjax_js").then(__webpack_require__.bind(__webpack_require__, /*! mathjax-full/js/mathjax */ "../node_modules/mathjax-full/js/mathjax.js")),
                Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlNodes_mo_js-node_modules_mathjax-full_js-e92534"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MathItem_js-node_modules_mathjax-full_js_core_MmlTr-144bb4"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_output_chtml_fonts_tex_js"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_output_chtml_js")]).then(__webpack_require__.t.bind(__webpack_require__, /*! mathjax-full/js/output/chtml */ "../node_modules/mathjax-full/js/output/chtml.js", 23)),
                Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlNodes_mo_js-node_modules_mathjax-full_js-e92534"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_Configuration_js-node_modules_mathjax-full_js_-8c4c26"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_ParseOptions_js-node_modules_mathjax-full_js_i-0c5d92"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_js")]).then(__webpack_require__.t.bind(__webpack_require__, /*! mathjax-full/js/input/tex */ "../node_modules/mathjax-full/js/input/tex.js", 23)),
                Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_mathjax-full_js_output_chtml_fonts_tex_js"), __webpack_require__.e("node_modules_mathjax-full_js_util_Options_js")]).then(__webpack_require__.t.bind(__webpack_require__, /*! mathjax-full/js/output/chtml/fonts/tex */ "../node_modules/mathjax-full/js/output/chtml/fonts/tex.js", 23)),
                Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlNodes_mo_js-node_modules_mathjax-full_js-e92534"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_Configuration_js-node_modules_mathjax-full_js_-8c4c26"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_ParseOptions_js-node_modules_mathjax-full_js_i-0c5d92"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_input_tex_AllPackages_js")]).then(__webpack_require__.bind(__webpack_require__, /*! mathjax-full/js/input/tex/AllPackages */ "../node_modules/mathjax-full/js/input/tex/AllPackages.js")),
                __webpack_require__.e(/*! import() */ "vendors-node_modules_mathjax-full_js_ui_safe_SafeHandler_js").then(__webpack_require__.t.bind(__webpack_require__, /*! mathjax-full/js/ui/safe/SafeHandler */ "../node_modules/mathjax-full/js/ui/safe/SafeHandler.js", 23)),
                Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlNodes_mo_js-node_modules_mathjax-full_js-e92534"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MathItem_js-node_modules_mathjax-full_js_core_MmlTr-144bb4"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlFactory_js"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_handlers_html_HTMLHandler_js")]).then(__webpack_require__.t.bind(__webpack_require__, /*! mathjax-full/js/handlers/html/HTMLHandler */ "../node_modules/mathjax-full/js/handlers/html/HTMLHandler.js", 23)),
                __webpack_require__.e(/*! import() */ "vendors-node_modules_mathjax-full_js_adaptors_browserAdaptor_js").then(__webpack_require__.bind(__webpack_require__, /*! mathjax-full/js/adaptors/browserAdaptor */ "../node_modules/mathjax-full/js/adaptors/browserAdaptor.js")),
                Promise.all(/*! import() */[__webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlNodes_mo_js-node_modules_mathjax-full_js-e92534"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MathItem_js-node_modules_mathjax-full_js_core_MmlTr-144bb4"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_core_MmlTree_MmlFactory_js"), __webpack_require__.e("vendors-node_modules_mathjax-full_js_a11y_assistive-mml_js")]).then(__webpack_require__.t.bind(__webpack_require__, /*! mathjax-full/js/a11y/assistive-mml */ "../node_modules/mathjax-full/js/a11y/assistive-mml.js", 23))
            ]);
            mathjax.handlers.register(AssistiveMmlHandler(SafeHandler(new HTMLHandler(browserAdaptor()))));
            class EmptyFont extends TeXFont {
            }
            EmptyFont.defaultFonts = {};
            const chtml = new CHTML({
                // Override dynamically generated fonts in favor of our font css
                font: new EmptyFont()
            });
            const tex = new TeX({
                packages: AllPackages.concat('require'),
                inlineMath: [
                    ['$', '$'],
                    ['\\(', '\\)']
                ],
                displayMath: [
                    ['$$', '$$'],
                    ['\\[', '\\]']
                ],
                processEscapes: true,
                processEnvironments: true
            });
            const mathDocument = mathjax.document(window.document, {
                InputJax: tex,
                OutputJax: chtml
            });
            _loading.resolve(mathDocument);
        }
        return _loading.promise;
    }
    Private.ensureMathDocument = ensureMathDocument;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWF0aGpheC1leHRlbnNpb25fbGliX2luZGV4X2pzLjgzYTRjMmNhMWM4YzZjZDU0MTkzLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDM0Q7OztHQUdHO0FBRWlEO0FBT007QUFJMUQsSUFBVSxVQUFVLENBU25CO0FBVEQsV0FBVSxVQUFVO0lBQ2xCOztPQUVHO0lBQ1UsZUFBSSxHQUFHLG1CQUFtQixDQUFDO0lBQ3hDOztPQUVHO0lBQ1UsZ0JBQUssR0FBRyxlQUFlLENBQUM7QUFDdkMsQ0FBQyxFQVRTLFVBQVUsS0FBVixVQUFVLFFBU25CO0FBUUQ7O0dBRUc7QUFDSSxNQUFNLGlCQUFpQjtJQUE5QjtRQWdDWSxpQkFBWSxHQUFZLEtBQUssQ0FBQztJQUUxQyxDQUFDO0lBakNXLEtBQUssQ0FBQyxrQkFBa0I7UUFDaEMsSUFBSSxDQUFDLElBQUksQ0FBQyxZQUFZLEVBQUU7WUFDdEIsSUFBSSxDQUFDLGFBQWEsR0FBRyxNQUFNLE9BQU8sQ0FBQyxrQkFBa0IsRUFBRSxDQUFDO1lBQ3hELElBQUksQ0FBQyxZQUFZLEdBQUcsSUFBSSxDQUFDO1NBQzFCO0lBQ0gsQ0FBQztJQUVEOztPQUVHO0lBQ0gsS0FBSyxDQUFDLFlBQVk7UUFDaEIsTUFBTSxJQUFJLENBQUMsa0JBQWtCLEVBQUUsQ0FBQztRQUNoQyxPQUFPLElBQUksQ0FBQyxhQUFhLENBQUM7SUFDNUIsQ0FBQztJQUVEOztPQUVHO0lBQ0gsS0FBSyxDQUFDLE9BQU8sQ0FBQyxJQUFpQjtRQUM3QixJQUFJO1lBQ0YsTUFBTSxJQUFJLENBQUMsa0JBQWtCLEVBQUUsQ0FBQztTQUNqQztRQUFDLE9BQU8sQ0FBQyxFQUFFO1lBQ1YsT0FBTyxDQUFDLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQztZQUNqQixPQUFPO1NBQ1I7UUFFRCxJQUFJLENBQUMsYUFBYSxDQUFDLE9BQU8sQ0FBQyxRQUFRLEdBQUcsQ0FBQyxJQUFJLENBQUMs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QUMsY0FBYyxFQUFFLENBQUMsQ0FBQyxDQUFDLENBQ3BFLENBQUM7WUFFRixNQUFNLFNBQVUsU0FBUSxPQUFPOztZQUNaLHNCQUFZLEdBQUcsRUFBUyxDQUFDO1lBRzVDLE1BQU0sS0FBSyxHQUFHLElBQUksS0FBSyxDQUFDO2dCQUN0QixnRUFBZ0U7Z0JBQ2hFLElBQUksRUFBRSxJQUFJLFNBQVMsRUFBRTthQUN0QixDQUFDLENBQUM7WUFFSCxNQUFNLEdBQUcsR0FBRyxJQUFJLEdBQUcsQ0FBQztnQkFDbEIsUUFBUSxFQUFFLFdBQVcsQ0FBQyxNQUFNLENBQUMsU0FBUyxDQUFDO2dCQUN2QyxVQUFVLEVBQUU7b0JBQ1YsQ0FBQyxHQUFHLEVBQUUsR0FBRyxDQUFDO29CQUNWLENBQUMsS0FBSyxFQUFFLEtBQUssQ0FBQztpQkFDZjtnQkFDRCxXQUFXLEVBQUU7b0JBQ1gsQ0FBQyxJQUFJLEVBQUUsSUFBSSxDQUFDO29CQUNaLENBQUMsS0FBSyxFQUFFLEtBQUssQ0FBQztpQkFDZjtnQkFDRCxjQUFjLEVBQUUsSUFBSTtnQkFDcEIsbUJBQW1CLEVBQUUsSUFBSTthQUMxQixDQUFDLENBQUM7WUFFSCxNQUFNLFlBQVksR0FBRyxPQUFPLENBQUMsUUFBUSxDQUFDLE1BQU0sQ0FBQyxRQUFRLEVBQUU7Z0JBQ3JELFFBQVEsRUFBRSxHQUFHO2dCQUNiLFNBQVMsRUFBRSxLQUFLO2FBQ2pCLENBQUMsQ0FBQztZQUVILFFBQVEsQ0FBQyxPQUFPLENBQUMsWUFBWSxDQUFDLENBQUM7U0FDaEM7UUFFRCxPQUFPLFFBQVEsQ0FBQyxPQUFPLENBQUM7SUFDMUIsQ0FBQztJQWxFcUIsMEJBQWtCLHFCQWtFdkM7QUFDSCxDQUFDLEVBdEVTLE9BQU8sS0FBUCxPQUFPLFFBc0VoQiIsInNvdXJjZXMiOlsid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy9tYXRoamF4LWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWF0aGpheC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQgeyBQcm9taXNlRGVsZWdhdGUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5cbmltcG9ydCB7XG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcblxuaW1wb3J0IHsgSUxhdGV4VHlwZXNldHRlciB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuXG5pbXBvcnQgdHlwZSB7IE1hdGhEb2N1bWVudCB9IGZyb20gJ21hdGhqYXgtZnVsbC9qcy9jb3JlL01hdGhEb2N1bWVudCc7XG5cbm5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgLyoqXG4gICAqIENvcHkgcmF3IExhVGVYIHRvIGNsaXBib2FyZC5cbiAgICovXG4gIGV4cG9ydCBjb25zdCBjb3B5ID0gJ21hdGhqYXg6Y2xpcGJvYXJkJztcbiAgLyoqXG4gICAqIFNjYWxlIE1hdGhKYXggZWxlbWVudHMuXG4gICAqL1xuICBleHBvcnQgY29uc3Qgc2NhbGUgPSAnbWF0aGpheDpzY2FsZSc7XG59XG5cbm5hbWVzcGFjZSBDb21tYW5kQXJncyB7XG4gIGV4cG9ydCB0eXBlIHNjYWxlID0ge1xuICAgIHNjYWxlOiBudW1iZXI7XG4gIH07XG59XG5cbi8qKlxuICogVGhlIE1hdGhKYXggVHlwZXNldHRlci5cbiAqL1xuZXhwb3J0IGNsYXNzIE1hdGhKYXhUeXBlc2V0dGVyIGltcGxlbWVudHMgSUxhdGV4VHlwZXNldHRlciB7XG4gIHByb3RlY3RlZCBhc3luYyBfZW5zdXJlSW5pdGlhbGl6ZWQoKSB7XG4gICAgaWYgKCF0aGlzLl9pbml0aWFsaXplZCkge1xuICAgICAgdGhpcy5fbWF0aERvY3VtZW50ID0gYXdhaXQgUHJpdmF0ZS5lbnN1cmVNYXRoRG9jdW1lbnQoKTtcbiAgICAgIHRoaXMuX2luaXRpYWxpemVkID0gdHJ1ZTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogR2V0IGFuIGluc3RhbmNlIG9mIHRoZSBNYXRoRG9jdW1lbnQgb2JqZWN0LlxuICAgKi9cbiAgYXN5bmMgbWF0aERvY3VtZW50KCk6IFByb21pc2U8TWF0aERvY3VtZW50PGFueSwgYW55LCBhbnk+PiB7XG4gICAgYXdhaXQgdGhpcy5fZW5zdXJlSW5pdGlhbGl6ZWQoKTtcbiAgICByZXR1cm4gdGhpcy5fbWF0aERvY3VtZW50O1xuICB9XG5cbiAgLyoqXG4gICAqIFR5cGVzZXQgdGhlIG1hdGggaW4gYSBub2RlLlxuICAgKi9cbiAgYXN5bmMgdHlwZXNldChub2RlOiBIVE1MRWxlbWVudCk6IFByb21pc2U8dm9pZD4ge1xuICAgIHRyeSB7XG4gICAgICBhd2FpdCB0aGlzLl9lbnN1cmVJbml0aWFsaXplZCgpO1xuICAgIH0gY2F0Y2ggKGUpIHtcbiAgICAgIGNvbnNvbGUuZXJyb3IoZSk7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgdGhpcy5fbWF0aERvY3VtZW50Lm9wdGlvbnMuZWxlbWVudHMgPSBbbm9kZV07XG4gICAgdGhpcy5fbWF0aERvY3VtZW50LmNsZWFyKCkucmVuZGVyKCk7XG4gICAgZGVsZXRlIHRoaXMuX21hdGhEb2N1bWVudC5vcHRpb25zLmVsZW1lbnRzO1xuICB9XG5cbiAgcHJvdGVjdGVkIF9pbml0aWFsaXplZDogYm9vbGVhbiA9IGZhbHNlO1xuICBwcm90ZWN0ZWQgX21hdGhEb2N1bWVudDogTWF0aERvY3VtZW50PGFueSwgYW55LCBhbnk+O1xufVxuXG4vKipcbiAqIFRoZSBNYXRoSmF4IGV4dGVuc2lvbi5cbiAqL1xuY29uc3QgbWF0aEpheFBsdWdpbjogSnVweXRlckZyb250RW5kUGx1Z2luPElMYXRleFR5cGVzZXR0ZXI+ID0ge1xuICBpZDogJ0BqdXB5dGVybGFiL21hdGhqYXgtZXh0ZW5zaW9uOnBsdWdpbicsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIExhVGVYIG1hdGhlbWF0aWNhbCBleHByZXNzaW9uIGludGVycHJldGVyLicsXG4gIHByb3ZpZGVzOiBJTGF0ZXhUeXBlc2V0dGVyLFxuICBhY3RpdmF0ZTogKGFwcDogSnVweXRlckZyb250RW5kKSA9PiB7XG4gICAgY29uc3QgdHlwZXNldHRlciA9IG5ldyBNYXRoSmF4VHlwZXNldHRlcigpO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5jb3B5LCB7XG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IG1kID0gYXdhaXQgdHlwZXNldHRlci5tYXRoRG9jdW1lbnQoKTtcbiAgICAgICAgY29uc3Qgb0pheDogYW55ID0gbWQub3V0cHV0SmF4O1xuICAgICAgICBhd2FpdCBuYXZpZ2F0b3IuY2xpcGJvYXJkLndyaXRlVGV4dChvSmF4Lm1hdGgubWF0aCk7XG4gICAgICB9LFxuICAgICAgbGFiZWw6ICdNYXRoSmF4IENvcHkgTGF0ZXgnXG4gICAgfSk7XG5cbiAgICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnNjYWxlLCB7XG4gICAgICBleGVjdXRlOiBhc3luYyAoYXJnczogQ29tbWFuZEFyZ3Muc2NhbGUpID0+IHtcbiAgICAgICAgY29uc3QgbWQgPSBhd2FpdCB0eXBlc2V0dGVyLm1hdGhEb2N1bWVudCgpO1xuICAgICAgICBjb25zdCBzY2FsZSA9IGFyZ3NbJ3NjYWxlJ10gfHwgMS4wO1xuICAgICAgICBtZC5vdXRwdXRKYXgub3B0aW9ucy5zY2FsZSA9IHNjYWxlO1xuICAgICAgICBtZC5yZXJlbmRlcigpO1xuICAgICAgfSxcbiAgICAgIGxhYmVsOiBhcmdzID0+XG4gICAgICAgICdNYXRoamF4IFNjYWxlICcgKyAoYXJnc1snc2NhbGUnXSA/IGB4JHthcmdzWydzY2FsZSddfWAgOiAnUmVzZXQnKVxuICAgIH0pO1xuXG4gICAgcmV0dXJuIHR5cGVzZXR0ZXI7XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuZXhwb3J0IGRlZmF1bHQgbWF0aEpheFBsdWdpbjtcblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgbW9kdWxlLXByaXZhdGUgZnVuY3Rpb25hbGl0eS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICBsZXQgX2xvYWRpbmc6IFByb21pc2VEZWxlZ2F0ZTxNYXRoRG9jdW1lbnQ8YW55LCBhbnksIGFueT4+IHwgbnVsbCA9IG51bGw7XG5cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIGVuc3VyZU1hdGhEb2N1bWVudCgpOiBQcm9taXNlPFxuICAgIE1hdGhEb2N1bWVudDxhbnksIGFueSwgYW55PlxuICA+IHtcbiAgICBpZiAoIV9sb2FkaW5nKSB7XG4gICAgICBfbG9hZGluZyA9IG5ldyBQcm9taXNlRGVsZWdhdGUoKTtcblxuICAgICAgdm9pZCBpbXBvcnQoJ21hdGhqYXgtZnVsbC9qcy9pbnB1dC90ZXgvcmVxdWlyZS9SZXF1aXJlQ29uZmlndXJhdGlvbicpO1xuXG4gICAgICBjb25zdCBbXG4gICAgICAgIHsgbWF0aGpheCB9LFxuICAgICAgICB7IENIVE1MIH0sXG4gICAgICAgIHsgVGVYIH0sXG4gICAgICAgIHsgVGVYRm9udCB9LFxuICAgICAgICB7IEFsbFBhY2thZ2VzIH0sXG4gICAgICAgIHsgU2FmZUhhbmRsZXIgfSxcbiAgICAgICAgeyBIVE1MSGFuZGxlciB9LFxuICAgICAgICB7IGJyb3dzZXJBZGFwdG9yIH0sXG4gICAgICAgIHsgQXNzaXN0aXZlTW1sSGFuZGxlciB9XG4gICAgICBdID0gYXdhaXQgUHJvbWlzZS5hbGwoW1xuICAgICAgICBpbXBvcnQoJ21hdGhqYXgtZnVsbC9qcy9tYXRoamF4JyksXG4gICAgICAgIGltcG9ydCgnbWF0aGpheC1mdWxsL2pzL291dHB1dC9jaHRtbCcpLFxuICAgICAgICBpbXBvcnQoJ21hdGhqYXgtZnVsbC9qcy9pbnB1dC90ZXgnKSxcbiAgICAgICAgaW1wb3J0KCdtYXRoamF4LWZ1bGwvanMvb3V0cHV0L2NodG1sL2ZvbnRzL3RleCcpLFxuICAgICAgICBpbXBvcnQoJ21hdGhqYXgtZnVsbC9qcy9pbnB1dC90ZXgvQWxsUGFja2FnZXMnKSxcbiAgICAgICAgaW1wb3J0KCdtYXRoamF4LWZ1bGwvanMvdWkvc2FmZS9TYWZlSGFuZGxlcicpLFxuICAgICAgICBpbXBvcnQoJ21hdGhqYXgtZnVsbC9qcy9oYW5kbGVycy9odG1sL0hUTUxIYW5kbGVyJyksXG4gICAgICAgIGltcG9ydCgnbWF0aGpheC1mdWxsL2pzL2FkYXB0b3JzL2Jyb3dzZXJBZGFwdG9yJyksXG4gICAgICAgIGltcG9ydCgnbWF0aGpheC1mdWxsL2pzL2ExMXkvYXNzaXN0aXZlLW1tbCcpXG4gICAgICBdKTtcblxuICAgICAgbWF0aGpheC5oYW5kbGVycy5yZWdpc3RlcihcbiAgICAgICAgQXNzaXN0aXZlTW1sSGFuZGxlcihTYWZlSGFuZGxlcihuZXcgSFRNTEhhbmRsZXIoYnJvd3NlckFkYXB0b3IoKSkpKVxuICAgICAgKTtcblxuICAgICAgY2xhc3MgRW1wdHlGb250IGV4dGVuZHMgVGVYRm9udCB7XG4gICAgICAgIHByb3RlY3RlZCBzdGF0aWMgZGVmYXVsdEZvbnRzID0ge30gYXMgYW55O1xuICAgICAgfVxuXG4gICAgICBjb25zdCBjaHRtbCA9IG5ldyBDSFRNTCh7XG4gICAgICAgIC8vIE92ZXJyaWRlIGR5bmFtaWNhbGx5IGdlbmVyYXRlZCBmb250cyBpbiBmYXZvciBvZiBvdXIgZm9udCBjc3NcbiAgICAgICAgZm9udDogbmV3IEVtcHR5Rm9udCgpXG4gICAgICB9KTtcblxuICAgICAgY29uc3QgdGV4ID0gbmV3IFRlWCh7XG4gICAgICAgIHBhY2thZ2VzOiBBbGxQYWNrYWdlcy5jb25jYXQoJ3JlcXVpcmUnKSxcbiAgICAgICAgaW5saW5lTWF0aDogW1xuICAgICAgICAgIFsnJCcsICckJ10sXG4gICAgICAgICAgWydcXFxcKCcsICdcXFxcKSddXG4gICAgICAgIF0sXG4gICAgICAgIGRpc3BsYXlNYXRoOiBbXG4gICAgICAgICAgWyckJCcsICckJCddLFxuICAgICAgICAgIFsnXFxcXFsnLCAnXFxcXF0nXVxuICAgICAgICBdLFxuICAgICAgICBwcm9jZXNzRXNjYXBlczogdHJ1ZSxcbiAgICAgICAgcHJvY2Vzc0Vudmlyb25tZW50czogdHJ1ZVxuICAgICAgfSk7XG5cbiAgICAgIGNvbnN0IG1hdGhEb2N1bWVudCA9IG1hdGhqYXguZG9jdW1lbnQod2luZG93LmRvY3VtZW50LCB7XG4gICAgICAgIElucHV0SmF4OiB0ZXgsXG4gICAgICAgIE91dHB1dEpheDogY2h0bWxcbiAgICAgIH0pO1xuXG4gICAgICBfbG9hZGluZy5yZXNvbHZlKG1hdGhEb2N1bWVudCk7XG4gICAgfVxuXG4gICAgcmV0dXJuIF9sb2FkaW5nLnByb21pc2U7XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==