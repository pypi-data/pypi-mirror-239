"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_markedparser-extension_lib_index_js-_d2760"],{

/***/ "../packages/markedparser-extension/lib/index.js":
/*!*******************************************************!*\
  !*** ../packages/markedparser-extension/lib/index.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "createMarkdownParser": () => (/* binding */ createMarkdownParser),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/mermaid */ "webpack/sharing/consume/default/@jupyterlab/mermaid/@jupyterlab/mermaid");
/* harmony import */ var _jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module markedparser-extension
 */





// highlight cache key separator
const FENCE = '```~~~';
/**
 * Create a markdown parser
 *
 * @param languages Editor languages
 * @returns Markdown parser
 */
function createMarkdownParser(languages, options) {
    return {
        render: (content) => {
            return Private.render(content, languages, options);
        }
    };
}
/**
 * The markdown parser plugin.
 */
const plugin = {
    id: '@jupyterlab/markedparser-extension:plugin',
    description: 'Provides the Markdown parser.',
    autoStart: true,
    provides: _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_3__.IMarkdownParser,
    requires: [_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_2__.IEditorLanguageRegistry],
    optional: [_jupyterlab_mermaid__WEBPACK_IMPORTED_MODULE_4__.IMermaidMarkdown],
    activate: (app, languages, mermaidMarkdown) => {
        return createMarkdownParser(languages, {
            blocks: mermaidMarkdown ? [mermaidMarkdown] : []
        });
    }
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * A namespace for private marked functions
 */
var Private;
(function (Private) {
    let _initializing = null;
    let _marked = null;
    let _blocks = [];
    let _languages = null;
    let _markedOptions = {};
    let _highlights = new _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.LruCache();
    async function render(content, languages, options) {
        _languages = languages;
        if (!_marked) {
            _marked = await initializeMarked(options);
        }
        return _marked(content, _markedOptions);
    }
    Private.render = render;
    /**
     * Load marked lazily and exactly once.
     */
    async function initializeMarked(options) {
        if (_marked) {
            return _marked;
        }
        if (_initializing) {
            return await _initializing.promise;
        }
        // order blocks by `rank`
        _blocks = (options === null || options === void 0 ? void 0 : options.blocks) || [];
        _blocks = _blocks.sort((a, b) => { var _a, _b; return ((_a = a.rank) !== null && _a !== void 0 ? _a : Infinity) - ((_b = b.rank) !== null && _b !== void 0 ? _b : Infinity); });
        _initializing = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.PromiseDelegate();
        // load marked lazily, and exactly once
        const [{ marked, Renderer }, plugins] = await Promise.all([
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_marked_marked").then(__webpack_require__.t.bind(__webpack_require__, /*! marked */ "webpack/sharing/consume/default/marked/marked", 23)),
            loadMarkedPlugins()
        ]);
        // use load marked plugins
        for (const plugin of plugins) {
            marked.use(plugin);
        }
        // finish marked configuration
        _markedOptions = {
            // use the explicit async paradigm for `walkTokens`
            async: true,
            // enable all built-in GitHub-flavored Markdown opinions
            gfm: true,
            // asynchronously prepare for any special tokens, like highlighting and mermaid
            walkTokens,
            // use custom renderer
            renderer: makeRenderer(Renderer)
        };
        // complete initialization
        _marked = marked;
        _initializing.resolve(_marked);
        return _marked;
    }
    Private.initializeMarked = initializeMarked;
    /**
     * Load and use marked plugins.
     *
     * As of writing, both of these features would work without plugins, but emit
     * deprecation warnings.
     */
    async function loadMarkedPlugins() {
        // use loaded marked plugins
        return Promise.all([
            (async () => (await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_marked-gfm-heading-id_marked-gfm-heading-id").then(__webpack_require__.t.bind(__webpack_require__, /*! marked-gfm-heading-id */ "webpack/sharing/consume/default/marked-gfm-heading-id/marked-gfm-heading-id", 23))).gfmHeadingId())(),
            (async () => (await __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_marked-mangle_marked-mangle").then(__webpack_require__.t.bind(__webpack_require__, /*! marked-mangle */ "webpack/sharing/consume/default/marked-mangle/marked-mangle", 23))).mangle())()
        ]);
    }
    /**
     * Build a custom marked renderer.
     */
    function makeRenderer(Renderer_) {
        const renderer = new Renderer_();
        const originalCode = renderer.code;
        renderer.code = (code, language) => {
            // handle block renderers
            for (const block of _blocks) {
                if (block.languages.includes(language)) {
                    const rendered = block.render(code);
                    if (rendered != null) {
                        return rendered;
                    }
                }
            }
            // handle known highlighting
            const key = `${language}${FENCE}${code}${FENCE}`;
            const highlight = _highlights.get(key);
            if (highlight != null) {
                return highlight;
            }
            // fall back to calling with the renderer as `this`
            return originalCode.call(renderer, code, language);
        };
        return renderer;
    }
    /**
     * Apply and cache syntax highlighting for code blocks.
     */
    async function highlight(token) {
        const { lang, text } = token;
        if (!lang || !_languages) {
            // no language(s), no highlight
            return;
        }
        const key = `${lang}${FENCE}${text}${FENCE}`;
        if (_highlights.get(key)) {
            // already cached, don't make another DOM element
            return;
        }
        const el = document.createElement('div');
        try {
            await _languages.highlight(text, _languages.findBest(lang), el);
            const html = `<pre><code class="language-${lang}">${el.innerHTML}</code></pre>`;
            _highlights.set(key, html);
        }
        catch (err) {
            console.error(`Failed to highlight ${lang} code`, err);
        }
        finally {
            el.remove();
        }
    }
    /**
     * After parsing, lazily load and render or highlight code blocks
     */
    async function walkTokens(token) {
        switch (token.type) {
            case 'code':
                if (token.lang) {
                    for (const block of _blocks) {
                        if (block.languages.includes(token.lang)) {
                            await block.walk(token.text);
                            return;
                        }
                    }
                }
                await highlight(token);
        }
    }
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfbWFya2VkcGFyc2VyLWV4dGVuc2lvbl9saWJfaW5kZXhfanMtX2QyNzYwLjdlN2U1MzYxZTAzNTVlMWYwNjkyLmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQUVpRDtBQU1IO0FBQ2dCO0FBQ1I7QUFDRjtBQU12RCxnQ0FBZ0M7QUFDaEMsTUFBTSxLQUFLLEdBQUcsUUFBUSxDQUFDO0FBb0J2Qjs7Ozs7R0FLRztBQUNJLFNBQVMsb0JBQW9CLENBQ2xDLFNBQWtDLEVBQ2xDLE9BQXdCO0lBRXhCLE9BQU87UUFDTCxNQUFNLEVBQUUsQ0FBQyxPQUFlLEVBQW1CLEVBQUU7WUFDM0MsT0FBTyxPQUFPLENBQUMsTUFBTSxDQUFDLE9BQU8sRUFBRSxTQUFTLEVBQUUsT0FBTyxDQUFDLENBQUM7UUFDckQsQ0FBQztLQUNGLENBQUM7QUFDSixDQUFDO0FBRUQ7O0dBRUc7QUFDSCxNQUFNLE1BQU0sR0FBMkM7SUFDckQsRUFBRSxFQUFFLDJDQUEyQztJQUMvQyxXQUFXLEVBQUUsK0JBQStCO0lBQzVDLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLG1FQUFlO0lBQ3pCLFFBQVEsRUFBRSxDQUFDLDJFQUF1QixDQUFDO0lBQ25DLFFBQVEsRUFBRSxDQUFDLGlFQUFnQixDQUFDO0lBQzVCLFFBQVEsRUFBRSxDQUNSLEdBQW9CLEVBQ3BCLFNBQWtDLEVBQ2xDLGVBQXdDLEVBQ3hDLEVBQUU7UUFDRixPQUFPLG9CQUFvQixDQUFDLFNBQVMsRUFBRTtZQUNyQyxNQUFNLEVBQUUsZUFBZSxDQUFDLENBQUMsQ0FBQyxDQUFDLGVBQWUsQ0FBQyxDQUFDLENBQUMsQ0FBQyxFQUFFO1NBQ2pELENBQUMsQ0FBQztJQUNMLENBQUM7Q0FDRixDQUFDO0FBRUY7O0dBRUc7QUFDSCxpRUFBZSxNQUFNLEVBQUM7QUFFdEI7O0dBRUc7QUFDSCxJQUFVLE9BQU8sQ0FnS2hCO0FBaEtELFdBQVUsT0FB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QWlEO1lBQ2pELE9BQU87U0FDUjtRQUNELE1BQU0sRUFBRSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsS0FBSyxDQUFDLENBQUM7UUFDekMsSUFBSTtZQUNGLE1BQU0sVUFBVSxDQUFDLFNBQVMsQ0FBQyxJQUFJLEVBQUUsVUFBVSxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsRUFBRSxFQUFFLENBQUMsQ0FBQztZQUNoRSxNQUFNLElBQUksR0FBRyw4QkFBOEIsSUFBSSxLQUFLLEVBQUUsQ0FBQyxTQUFTLGVBQWUsQ0FBQztZQUNoRixXQUFXLENBQUMsR0FBRyxDQUFDLEdBQUcsRUFBRSxJQUFJLENBQUMsQ0FBQztTQUM1QjtRQUFDLE9BQU8sR0FBRyxFQUFFO1lBQ1osT0FBTyxDQUFDLEtBQUssQ0FBQyx1QkFBdUIsSUFBSSxPQUFPLEVBQUUsR0FBRyxDQUFDLENBQUM7U0FDeEQ7Z0JBQVM7WUFDUixFQUFFLENBQUMsTUFBTSxFQUFFLENBQUM7U0FDYjtJQUNILENBQUM7SUFFRDs7T0FFRztJQUNILEtBQUssVUFBVSxVQUFVLENBQUMsS0FBWTtRQUNwQyxRQUFRLEtBQUssQ0FBQyxJQUFJLEVBQUU7WUFDbEIsS0FBSyxNQUFNO2dCQUNULElBQUksS0FBSyxDQUFDLElBQUksRUFBRTtvQkFDZCxLQUFLLE1BQU0sS0FBSyxJQUFJLE9BQU8sRUFBRTt3QkFDM0IsSUFBSSxLQUFLLENBQUMsU0FBUyxDQUFDLFFBQVEsQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLEVBQUU7NEJBQ3hDLE1BQU0sS0FBSyxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsSUFBSSxDQUFDLENBQUM7NEJBQzdCLE9BQU87eUJBQ1I7cUJBQ0Y7aUJBQ0Y7Z0JBQ0QsTUFBTSxTQUFTLENBQUMsS0FBb0IsQ0FBQyxDQUFDO1NBQ3pDO0lBQ0gsQ0FBQztBQUNILENBQUMsRUFoS1MsT0FBTyxLQUFQLE9BQU8sUUFnS2hCIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL21hcmtlZHBhcnNlci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgbWFya2VkcGFyc2VyLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7IFByb21pc2VEZWxlZ2F0ZSB9IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcblxuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgTHJ1Q2FjaGUgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuaW1wb3J0IHsgSUVkaXRvckxhbmd1YWdlUmVnaXN0cnkgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlbWlycm9yJztcbmltcG9ydCB7IElNYXJrZG93blBhcnNlciB9IGZyb20gJ0BqdXB5dGVybGFiL3JlbmRlcm1pbWUnO1xuaW1wb3J0IHsgSU1lcm1haWRNYXJrZG93biB9IGZyb20gJ0BqdXB5dGVybGFiL21lcm1haWQnO1xuXG5pbXBvcnQgdHlwZSB7IG1hcmtlZCwgUmVuZGVyZXIgfSBmcm9tICdtYXJrZWQnO1xuaW1wb3J0IHR5cGUgeyBNYXJrZWRFeHRlbnNpb24sIE1hcmtlZE9wdGlvbnMgfSBmcm9tICdNYXJrZWRPcHRpb25zJztcbmltcG9ydCB0eXBlIHsgVG9rZW4sIFRva2VucyB9IGZyb20gJ1Rva2Vucyc7XG5cbi8vIGhpZ2hsaWdodCBjYWNoZSBrZXkgc2VwYXJhdG9yXG5jb25zdCBGRU5DRSA9ICdgYGB+fn4nO1xuXG4vKipcbiAqIEFuIGludGVyZmFjZSBmb3IgZmVuY2VkIGNvZGUgYmxvY2sgcmVuZGVyZXJzLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElGZW5jZWRCbG9ja1JlbmRlcmVyIHtcbiAgbGFuZ3VhZ2VzOiBzdHJpbmdbXTtcbiAgcmFuazogbnVtYmVyO1xuICB3YWxrOiAodGV4dDogc3RyaW5nKSA9PiBQcm9taXNlPHZvaWQ+O1xuICByZW5kZXI6ICh0ZXh0OiBzdHJpbmcpID0+IHN0cmluZyB8IG51bGw7XG59XG5cbi8qKlxuICogT3B0aW9uc1xuICovXG5leHBvcnQgaW50ZXJmYWNlIElSZW5kZXJPcHRpb25zIHtcbiAgLyoqIGhhbmRsZXJzIGZvciBmZW5jZWQgY29kZSBibG9ja3MgKi9cbiAgYmxvY2tzPzogSUZlbmNlZEJsb2NrUmVuZGVyZXJbXTtcbn1cblxuLyoqXG4gKiBDcmVhdGUgYSBtYXJrZG93biBwYXJzZXJcbiAqXG4gKiBAcGFyYW0gbGFuZ3VhZ2VzIEVkaXRvciBsYW5ndWFnZXNcbiAqIEByZXR1cm5zIE1hcmtkb3duIHBhcnNlclxuICovXG5leHBvcnQgZnVuY3Rpb24gY3JlYXRlTWFya2Rvd25QYXJzZXIoXG4gIGxhbmd1YWdlczogSUVkaXRvckxhbmd1YWdlUmVnaXN0cnksXG4gIG9wdGlvbnM/OiBJUmVuZGVyT3B0aW9uc1xuKSB7XG4gIHJldHVybiB7XG4gICAgcmVuZGVyOiAoY29udGVudDogc3RyaW5nKTogUHJvbWlzZTxzdHJpbmc+ID0+IHtcbiAgICAgIHJldHVybiBQcml2YXRlLnJlbmRlcihjb250ZW50LCBsYW5ndWFnZXMsIG9wdGlvbnMpO1xuICAgIH1cbiAgfTtcbn1cblxuLyoqXG4gKiBUaGUgbWFya2Rvd24gcGFyc2VyIHBsdWdpbi5cbiAqL1xuY29uc3QgcGx1Z2luOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SU1hcmtkb3duUGFyc2VyPiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9tYXJrZWRwYXJzZXItZXh0ZW5zaW9uOnBsdWdpbicsXG4gIGRlc2NyaXB0aW9uOiAnUHJvdmlkZXMgdGhlIE1hcmtkb3duIHBhcnNlci4nLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIHByb3ZpZGVzOiBJTWFya2Rvd25QYXJzZXIsXG4gIHJlcXVpcmVzOiBbSUVkaXRvckxhbmd1YWdlUmVnaXN0cnldLFxuICBvcHRpb25hbDogW0lNZXJtYWlkTWFya2Rvd25dLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIGxhbmd1YWdlczogSUVkaXRvckxhbmd1YWdlUmVnaXN0cnksXG4gICAgbWVybWFpZE1hcmtkb3duOiBJTWVybWFpZE1hcmtkb3duIHwgbnVsbFxuICApID0+IHtcbiAgICByZXR1cm4gY3JlYXRlTWFya2Rvd25QYXJzZXIobGFuZ3VhZ2VzLCB7XG4gICAgICBibG9ja3M6IG1lcm1haWRNYXJrZG93biA/IFttZXJtYWlkTWFya2Rvd25dIDogW11cbiAgICB9KTtcbiAgfVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHBsdWdpbiBhcyBkZWZhdWx0LlxuICovXG5leHBvcnQgZGVmYXVsdCBwbHVnaW47XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgbWFya2VkIGZ1bmN0aW9uc1xuICovXG5uYW1lc3BhY2UgUHJpdmF0ZSB7XG4gIGxldCBfaW5pdGlhbGl6aW5nOiBQcm9taXNlRGVsZWdhdGU8dHlwZW9mIG1hcmtlZD4gfCBudWxsID0gbnVsbDtcbiAgbGV0IF9tYXJrZWQ6IHR5cGVvZiBtYXJrZWQgfCBudWxsID0gbnVsbDtcbiAgbGV0IF9ibG9ja3M6IElGZW5jZWRCbG9ja1JlbmRlcmVyW10gPSBbXTtcbiAgbGV0IF9sYW5ndWFnZXM6IElFZGl0b3JMYW5ndWFnZVJlZ2lzdHJ5IHwgbnVsbCA9IG51bGw7XG4gIGxldCBfbWFya2VkT3B0aW9uczogTWFya2VkT3B0aW9ucyA9IHt9O1xuICBsZXQgX2hpZ2hsaWdodHMgPSBuZXcgTHJ1Q2FjaGU8c3RyaW5nLCBzdHJpbmc+KCk7XG5cbiAgZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIHJlbmRlcihcbiAgICBjb250ZW50OiBzdHJpbmcsXG4gICAgbGFuZ3VhZ2VzOiBJRWRpdG9yTGFuZ3VhZ2VSZWdpc3RyeSxcbiAgICBvcHRpb25zPzogSVJlbmRlck9wdGlvbnNcbiAgKTogUHJvbWlzZTxzdHJpbmc+IHtcbiAgICBfbGFuZ3VhZ2VzID0gbGFuZ3VhZ2VzO1xuICAgIGlmICghX21hcmtlZCkge1xuICAgICAgX21hcmtlZCA9IGF3YWl0IGluaXRpYWxpemVNYXJrZWQob3B0aW9ucyk7XG4gICAgfVxuICAgIHJldHVybiBfbWFya2VkKGNvbnRlbnQsIF9tYXJrZWRPcHRpb25zKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBMb2FkIG1hcmtlZCBsYXppbHkgYW5kIGV4YWN0bHkgb25jZS5cbiAgICovXG4gIGV4cG9ydCBhc3luYyBmdW5jdGlvbiBpbml0aWFsaXplTWFya2VkKFxuICAgIG9wdGlvbnM/OiBJUmVuZGVyT3B0aW9uc1xuICApOiBQcm9taXNlPHR5cGVvZiBtYXJrZWQ+IHtcbiAgICBpZiAoX21hcmtlZCkge1xuICAgICAgcmV0dXJuIF9tYXJrZWQ7XG4gICAgfVxuXG4gICAgaWYgKF9pbml0aWFsaXppbmcpIHtcbiAgICAgIHJldHVybiBhd2FpdCBfaW5pdGlhbGl6aW5nLnByb21pc2U7XG4gICAgfVxuXG4gICAgLy8gb3JkZXIgYmxvY2tzIGJ5IGByYW5rYFxuICAgIF9ibG9ja3MgPSBvcHRpb25zPy5ibG9ja3MgfHwgW107XG4gICAgX2Jsb2NrcyA9IF9ibG9ja3Muc29ydChcbiAgICAgIChhLCBiKSA9PiAoYS5yYW5rID8/IEluZmluaXR5KSAtIChiLnJhbmsgPz8gSW5maW5pdHkpXG4gICAgKTtcblxuICAgIF9pbml0aWFsaXppbmcgPSBuZXcgUHJvbWlzZURlbGVnYXRlKCk7XG5cbiAgICAvLyBsb2FkIG1hcmtlZCBsYXppbHksIGFuZCBleGFjdGx5IG9uY2VcbiAgICBjb25zdCBbeyBtYXJrZWQsIFJlbmRlcmVyIH0sIHBsdWdpbnNdID0gYXdhaXQgUHJvbWlzZS5hbGwoW1xuICAgICAgaW1wb3J0KCdtYXJrZWQnKSxcbiAgICAgIGxvYWRNYXJrZWRQbHVnaW5zKClcbiAgICBdKTtcblxuICAgIC8vIHVzZSBsb2FkIG1hcmtlZCBwbHVnaW5zXG4gICAgZm9yIChjb25zdCBwbHVnaW4gb2YgcGx1Z2lucykge1xuICAgICAgbWFya2VkLnVzZShwbHVnaW4pO1xuICAgIH1cblxuICAgIC8vIGZpbmlzaCBtYXJrZWQgY29uZmlndXJhdGlvblxuICAgIF9tYXJrZWRPcHRpb25zID0ge1xuICAgICAgLy8gdXNlIHRoZSBleHBsaWNpdCBhc3luYyBwYXJhZGlnbSBmb3IgYHdhbGtUb2tlbnNgXG4gICAgICBhc3luYzogdHJ1ZSxcbiAgICAgIC8vIGVuYWJsZSBhbGwgYnVpbHQtaW4gR2l0SHViLWZsYXZvcmVkIE1hcmtkb3duIG9waW5pb25zXG4gICAgICBnZm06IHRydWUsXG4gICAgICAvLyBhc3luY2hyb25vdXNseSBwcmVwYXJlIGZvciBhbnkgc3BlY2lhbCB0b2tlbnMsIGxpa2UgaGlnaGxpZ2h0aW5nIGFuZCBtZXJtYWlkXG4gICAgICB3YWxrVG9rZW5zLFxuICAgICAgLy8gdXNlIGN1c3RvbSByZW5kZXJlclxuICAgICAgcmVuZGVyZXI6IG1ha2VSZW5kZXJlcihSZW5kZXJlcilcbiAgICB9O1xuXG4gICAgLy8gY29tcGxldGUgaW5pdGlhbGl6YXRpb25cbiAgICBfbWFya2VkID0gbWFya2VkO1xuICAgIF9pbml0aWFsaXppbmcucmVzb2x2ZShfbWFya2VkKTtcbiAgICByZXR1cm4gX21hcmtlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBMb2FkIGFuZCB1c2UgbWFya2VkIHBsdWdpbnMuXG4gICAqXG4gICAqIEFzIG9mIHdyaXRpbmcsIGJvdGggb2YgdGhlc2UgZmVhdHVyZXMgd291bGQgd29yayB3aXRob3V0IHBsdWdpbnMsIGJ1dCBlbWl0XG4gICAqIGRlcHJlY2F0aW9uIHdhcm5pbmdzLlxuICAgKi9cbiAgYXN5bmMgZnVuY3Rpb24gbG9hZE1hcmtlZFBsdWdpbnMoKTogUHJvbWlzZTxNYXJrZWRFeHRlbnNpb25bXT4ge1xuICAgIC8vIHVzZSBsb2FkZWQgbWFya2VkIHBsdWdpbnNcbiAgICByZXR1cm4gUHJvbWlzZS5hbGwoW1xuICAgICAgKGFzeW5jICgpID0+IChhd2FpdCBpbXBvcnQoJ21hcmtlZC1nZm0taGVhZGluZy1pZCcpKS5nZm1IZWFkaW5nSWQoKSkoKSxcbiAgICAgIChhc3luYyAoKSA9PiAoYXdhaXQgaW1wb3J0KCdtYXJrZWQtbWFuZ2xlJykpLm1hbmdsZSgpKSgpXG4gICAgXSk7XG4gIH1cblxuICAvKipcbiAgICogQnVpbGQgYSBjdXN0b20gbWFya2VkIHJlbmRlcmVyLlxuICAgKi9cbiAgZnVuY3Rpb24gbWFrZVJlbmRlcmVyKFJlbmRlcmVyXzogdHlwZW9mIFJlbmRlcmVyKTogUmVuZGVyZXIge1xuICAgIGNvbnN0IHJlbmRlcmVyID0gbmV3IFJlbmRlcmVyXygpO1xuICAgIGNvbnN0IG9yaWdpbmFsQ29kZSA9IHJlbmRlcmVyLmNvZGU7XG5cbiAgICByZW5kZXJlci5jb2RlID0gKGNvZGU6IHN0cmluZywgbGFuZ3VhZ2U6IHN0cmluZykgPT4ge1xuICAgICAgLy8gaGFuZGxlIGJsb2NrIHJlbmRlcmVyc1xuICAgICAgZm9yIChjb25zdCBibG9jayBvZiBfYmxvY2tzKSB7XG4gICAgICAgIGlmIChibG9jay5sYW5ndWFnZXMuaW5jbHVkZXMobGFuZ3VhZ2UpKSB7XG4gICAgICAgICAgY29uc3QgcmVuZGVyZWQgPSBibG9jay5yZW5kZXIoY29kZSk7XG4gICAgICAgICAgaWYgKHJlbmRlcmVkICE9IG51bGwpIHtcbiAgICAgICAgICAgIHJldHVybiByZW5kZXJlZDtcbiAgICAgICAgICB9XG4gICAgICAgIH1cbiAgICAgIH1cblxuICAgICAgLy8gaGFuZGxlIGtub3duIGhpZ2hsaWdodGluZ1xuICAgICAgY29uc3Qga2V5ID0gYCR7bGFuZ3VhZ2V9JHtGRU5DRX0ke2NvZGV9JHtGRU5DRX1gO1xuICAgICAgY29uc3QgaGlnaGxpZ2h0ID0gX2hpZ2hsaWdodHMuZ2V0KGtleSk7XG4gICAgICBpZiAoaGlnaGxpZ2h0ICE9IG51bGwpIHtcbiAgICAgICAgcmV0dXJuIGhpZ2hsaWdodDtcbiAgICAgIH1cblxuICAgICAgLy8gZmFsbCBiYWNrIHRvIGNhbGxpbmcgd2l0aCB0aGUgcmVuZGVyZXIgYXMgYHRoaXNgXG4gICAgICByZXR1cm4gb3JpZ2luYWxDb2RlLmNhbGwocmVuZGVyZXIsIGNvZGUsIGxhbmd1YWdlKTtcbiAgICB9O1xuXG4gICAgcmV0dXJuIHJlbmRlcmVyO1xuICB9XG5cbiAgLyoqXG4gICAqIEFwcGx5IGFuZCBjYWNoZSBzeW50YXggaGlnaGxpZ2h0aW5nIGZvciBjb2RlIGJsb2Nrcy5cbiAgICovXG4gIGFzeW5jIGZ1bmN0aW9uIGhpZ2hsaWdodCh0b2tlbjogVG9rZW5zLkNvZGUpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCB7IGxhbmcsIHRleHQgfSA9IHRva2VuO1xuICAgIGlmICghbGFuZyB8fCAhX2xhbmd1YWdlcykge1xuICAgICAgLy8gbm8gbGFuZ3VhZ2UocyksIG5vIGhpZ2hsaWdodFxuICAgICAgcmV0dXJuO1xuICAgIH1cbiAgICBjb25zdCBrZXkgPSBgJHtsYW5nfSR7RkVOQ0V9JHt0ZXh0fSR7RkVOQ0V9YDtcbiAgICBpZiAoX2hpZ2hsaWdodHMuZ2V0KGtleSkpIHtcbiAgICAgIC8vIGFscmVhZHkgY2FjaGVkLCBkb24ndCBtYWtlIGFub3RoZXIgRE9NIGVsZW1lbnRcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgZWwgPSBkb2N1bWVudC5jcmVhdGVFbGVtZW50KCdkaXYnKTtcbiAgICB0cnkge1xuICAgICAgYXdhaXQgX2xhbmd1YWdlcy5oaWdobGlnaHQodGV4dCwgX2xhbmd1YWdlcy5maW5kQmVzdChsYW5nKSwgZWwpO1xuICAgICAgY29uc3QgaHRtbCA9IGA8cHJlPjxjb2RlIGNsYXNzPVwibGFuZ3VhZ2UtJHtsYW5nfVwiPiR7ZWwuaW5uZXJIVE1MfTwvY29kZT48L3ByZT5gO1xuICAgICAgX2hpZ2hsaWdodHMuc2V0KGtleSwgaHRtbCk7XG4gICAgfSBjYXRjaCAoZXJyKSB7XG4gICAgICBjb25zb2xlLmVycm9yKGBGYWlsZWQgdG8gaGlnaGxpZ2h0ICR7bGFuZ30gY29kZWAsIGVycik7XG4gICAgfSBmaW5hbGx5IHtcbiAgICAgIGVsLnJlbW92ZSgpO1xuICAgIH1cbiAgfVxuXG4gIC8qKlxuICAgKiBBZnRlciBwYXJzaW5nLCBsYXppbHkgbG9hZCBhbmQgcmVuZGVyIG9yIGhpZ2hsaWdodCBjb2RlIGJsb2Nrc1xuICAgKi9cbiAgYXN5bmMgZnVuY3Rpb24gd2Fsa1Rva2Vucyh0b2tlbjogVG9rZW4pOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBzd2l0Y2ggKHRva2VuLnR5cGUpIHtcbiAgICAgIGNhc2UgJ2NvZGUnOlxuICAgICAgICBpZiAodG9rZW4ubGFuZykge1xuICAgICAgICAgIGZvciAoY29uc3QgYmxvY2sgb2YgX2Jsb2Nrcykge1xuICAgICAgICAgICAgaWYgKGJsb2NrLmxhbmd1YWdlcy5pbmNsdWRlcyh0b2tlbi5sYW5nKSkge1xuICAgICAgICAgICAgICBhd2FpdCBibG9jay53YWxrKHRva2VuLnRleHQpO1xuICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGF3YWl0IGhpZ2hsaWdodCh0b2tlbiBhcyBUb2tlbnMuQ29kZSk7XG4gICAgfVxuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=