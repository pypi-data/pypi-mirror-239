"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_vega5-extension_lib_index_js"],{

/***/ "../packages/vega5-extension/lib/index.js":
/*!************************************************!*\
  !*** ../packages/vega5-extension/lib/index.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RenderedVega": () => (/* binding */ RenderedVega),
/* harmony export */   "VEGALITE3_MIME_TYPE": () => (/* binding */ VEGALITE3_MIME_TYPE),
/* harmony export */   "VEGALITE4_MIME_TYPE": () => (/* binding */ VEGALITE4_MIME_TYPE),
/* harmony export */   "VEGALITE5_MIME_TYPE": () => (/* binding */ VEGALITE5_MIME_TYPE),
/* harmony export */   "VEGA_MIME_TYPE": () => (/* binding */ VEGA_MIME_TYPE),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "rendererFactory": () => (/* binding */ rendererFactory)
/* harmony export */ });
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_0__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module vega5-extension
 */

/**
 * The CSS class to add to the Vega and Vega-Lite widget.
 */
const VEGA_COMMON_CLASS = 'jp-RenderedVegaCommon5';
/**
 * The CSS class to add to the Vega.
 */
const VEGA_CLASS = 'jp-RenderedVega5';
/**
 * The CSS class to add to the Vega-Lite.
 */
const VEGALITE_CLASS = 'jp-RenderedVegaLite';
/**
 * The MIME type for Vega.
 *
 * #### Notes
 * The version of this follows the major version of Vega.
 */
const VEGA_MIME_TYPE = 'application/vnd.vega.v5+json';
/**
 * The MIME type for Vega-Lite.
 *
 * #### Notes
 * The version of this follows the major version of Vega-Lite.
 */
const VEGALITE3_MIME_TYPE = 'application/vnd.vegalite.v3+json';
/**
 * The MIME type for Vega-Lite.
 *
 * #### Notes
 * The version of this follows the major version of Vega-Lite.
 */
const VEGALITE4_MIME_TYPE = 'application/vnd.vegalite.v4+json';
/**
 * The MIME type for Vega-Lite.
 *
 * #### Notes
 * The version of this follows the major version of Vega-Lite.
 */
const VEGALITE5_MIME_TYPE = 'application/vnd.vegalite.v5+json';
/**
 * A widget for rendering Vega or Vega-Lite data, for usage with rendermime.
 */
class RenderedVega extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_0__.Widget {
    /**
     * Create a new widget for rendering Vega/Vega-Lite.
     */
    constructor(options) {
        super();
        this._mimeType = options.mimeType;
        this._resolver = options.resolver;
        this.addClass(VEGA_COMMON_CLASS);
        this.addClass(this._mimeType === VEGA_MIME_TYPE ? VEGA_CLASS : VEGALITE_CLASS);
    }
    /**
     * Render Vega/Vega-Lite into this widget's node.
     */
    async renderModel(model) {
        const spec = model.data[this._mimeType];
        if (spec === undefined) {
            return;
        }
        const metadata = model.metadata[this._mimeType];
        const embedOptions = metadata && metadata.embed_options ? metadata.embed_options : {};
        // If the JupyterLab theme is dark, render this using a dark Vega theme.
        let bodyThemeDark = document.body.dataset.jpThemeLight === 'false';
        if (bodyThemeDark) {
            embedOptions.theme = 'dark';
        }
        const mode = this._mimeType === VEGA_MIME_TYPE ? 'vega' : 'vega-lite';
        const vega = Private.vega != null ? Private.vega : await Private.ensureVega();
        const el = document.createElement('div');
        // clear the output before attaching a chart
        this.node.textContent = '';
        this.node.appendChild(el);
        if (this._result) {
            this._result.finalize();
        }
        const loader = vega.vega.loader({
            http: { credentials: 'same-origin' }
        });
        const sanitize = async (uri, options) => {
            // Use the resolver for any URIs it wants to handle
            const resolver = this._resolver;
            if ((resolver === null || resolver === void 0 ? void 0 : resolver.isLocal) && resolver.isLocal(uri)) {
                const absPath = await resolver.resolveUrl(uri);
                uri = await resolver.getDownloadUrl(absPath);
            }
            return loader.sanitize(uri, options);
        };
        this._result = await vega.default(el, spec, {
            actions: true,
            defaultStyle: true,
            ...embedOptions,
            mode,
            loader: { ...loader, sanitize }
        });
        if (model.data['image/png']) {
            return;
        }
        // Add png representation of vega chart to output
        const imageURL = await this._result.view.toImageURL('png', typeof embedOptions.scaleFactor === 'number'
            ? embedOptions.scaleFactor
            : embedOptions.scaleFactor
                ? embedOptions.scaleFactor.png
                : embedOptions.scaleFactor);
        model.setData({
            data: { ...model.data, 'image/png': imageURL.split(',')[1] }
        });
    }
    dispose() {
        if (this._result) {
            this._result.finalize();
        }
        super.dispose();
    }
}
/**
 * A mime renderer factory for vega data.
 */
const rendererFactory = {
    safe: true,
    mimeTypes: [
        VEGA_MIME_TYPE,
        VEGALITE3_MIME_TYPE,
        VEGALITE4_MIME_TYPE,
        VEGALITE5_MIME_TYPE
    ],
    createRenderer: options => new RenderedVega(options)
};
const extension = {
    id: '@jupyterlab/vega5-extension:factory',
    description: 'Provides a renderer for Vega 5 and Vega-Lite 3 to 5 content.',
    rendererFactory,
    rank: 57,
    dataType: 'json',
    documentWidgetFactoryOptions: [
        {
            name: 'Vega5',
            primaryFileType: 'vega5',
            fileTypes: ['vega5', 'json'],
            defaultFor: ['vega5']
        },
        {
            name: 'Vega-Lite5',
            primaryFileType: 'vega-lite5',
            fileTypes: ['vega-lite3', 'vega-lite4', 'vega-lite5', 'json'],
            defaultFor: ['vega-lite3', 'vega-lite4', 'vega-lite5']
        }
    ],
    fileTypes: [
        {
            mimeTypes: [VEGA_MIME_TYPE],
            name: 'vega5',
            extensions: ['.vg', '.vg.json', '.vega'],
            icon: 'ui-components:vega'
        },
        {
            mimeTypes: [VEGALITE5_MIME_TYPE],
            name: 'vega-lite5',
            extensions: ['.vl', '.vl.json', '.vegalite'],
            icon: 'ui-components:vega'
        },
        {
            mimeTypes: [VEGALITE4_MIME_TYPE],
            name: 'vega-lite4',
            extensions: [],
            icon: 'ui-components:vega'
        },
        {
            mimeTypes: [VEGALITE3_MIME_TYPE],
            name: 'vega-lite3',
            extensions: [],
            icon: 'ui-components:vega'
        }
    ]
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * Lazy-load and cache the vega-embed library
     */
    function ensureVega() {
        if (Private.vegaReady) {
            return Private.vegaReady;
        }
        Private.vegaReady = __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_vega-embed_vega-embed").then(__webpack_require__.t.bind(__webpack_require__, /*! vega-embed */ "webpack/sharing/consume/default/vega-embed/vega-embed", 23));
        return Private.vegaReady;
    }
    Private.ensureVega = ensureVega;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdmVnYTUtZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy4wZjg5ZmY0ZTJlYzU1NWE5YjE2MC5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTs7OytFQUcrRTtBQUMvRTs7O0dBR0c7QUFJc0M7QUFHekM7O0dBRUc7QUFDSCxNQUFNLGlCQUFpQixHQUFHLHdCQUF3QixDQUFDO0FBRW5EOztHQUVHO0FBQ0gsTUFBTSxVQUFVLEdBQUcsa0JBQWtCLENBQUM7QUFFdEM7O0dBRUc7QUFDSCxNQUFNLGNBQWMsR0FBRyxxQkFBcUIsQ0FBQztBQUU3Qzs7Ozs7R0FLRztBQUNJLE1BQU0sY0FBYyxHQUFHLDhCQUE4QixDQUFDO0FBRTdEOzs7OztHQUtHO0FBQ0ksTUFBTSxtQkFBbUIsR0FBRyxrQ0FBa0MsQ0FBQztBQUV0RTs7Ozs7R0FLRztBQUNJLE1BQU0sbUJBQW1CLEdBQUcsa0NBQWtDLENBQUM7QUFFdEU7Ozs7O0dBS0c7QUFDSSxNQUFNLG1CQUFtQixHQUFHLGtDQUFrQyxDQUFDO0FBRXRFOztHQUVHO0FBQ0ksTUFBTSxZQUFhLFNBQVEsbURBQU07SUFHdEM7O09BRUc7SUFDSCxZQUFZLE9BQXFDO1FBQy9DLEtBQUssRUFBRSxDQUFDO1FBQ1IsSUFBSSxDQUFDLFNBQVMsR0FBRyxPQUFPLENBQUMsUUFBUSxDQUFDO1FBQ2xDLElBQUksQ0FBQyxTQUFTLEdBQUcsT0FBTyxDQUFDLFFBQVEsQ0FBQztRQUNsQyxJQUFJLENBQUMsUUFBUSxDQUFDLGlCQUFpQixDQUFDLENBQUM7UUFDakMsSUFBSSxDQUFDLFFBQVEsQ0FDWCxJQUFJLENBQUMsU0FBUyxLQUFLLGNBQWMsQ0FBQyxDQUFDLENBQUMsVUFBVSxDQUFDLENBQUMsQ0FBQyxjQUFjLENBQ2hFLENBQUM7SUFDSixDQUFDO0lBRUQ7O09BRUc7SUFDSCxLQUFLLENBQUMsV0FBVyxDQUFDLEtBQTZCO1FBQzdDLE1BQU0sSUFBSSxHQUFHLEtBQUssQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLFNBQVMsQ0FBMkIsQ0FBQztRQUNsRSxJQUFJLElBQUksS0FBSyxTQUFTLEVBQUU7WUFDdEIsT0FBTztTQUNSO1FBQ0QsTUFBTSxRQUFRLEdBQUcsS0FBSyxDQUFDLFFBQVEsQ0FBQyxJQUFJLENBQUMsU0FBUyxDQUlqQyxDQUFDO1FBQ2QsTUFBTSxZQUFZLEdBQ2hCLFFBQVEsSUFBSSxRQUFRLENBQUMsYUFBYSxDQUFDLENBQUMsQ0FBQyxRQUFRLENBQUMsYUFBYSxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUM7UUFFbkUsd0VBQXdFO1FBQ3hFLElBQUksYUFBYSxHQUFHLFFBQVEsQ0FBQyxJQUFJLENBQUMsT0FBTyxDQUFDLFlBQVksS0FBSyxPQUFPLENBQUM7UUFDbkUsSUFBSSxhQUFhLEVBQUU7WUFDakIsWUFBWSxDQUFDLEtBQUssR0FBRyxNQUFNLENBQUM7U0FDN0I7UUFFRCxNQUFNLElBQUksR0FDUixJQUFJLENBQUMsU0FBUyxLQUFLLGNBQWMsQ0FBQyxDQUFDLENBQUMsTUFBTSxDQUFDLENBQUMsQ0FBQyxXQUFXLENBQUM7UUFFM0QsTUFBTSxJQUFJLEdBQ1IsT0FBTyxDQUFDLElBQUksSUFBSSxJQUFJLENBQUMsQ0FBQyxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLE1BQU0sT0FBTyxDQUFDLFVBQVUsRUFBRSxDQUFDO1FBRW5FLE1BQU0sRUFBRSxHQUFHLFFBQVEsQ0FBQyxhQUFhLENBQUMsS0FBSyxDQUFDLENBQUM7UUFFekMsNENBQTRDO1FBQzVDLElBQUksQ0FBQyxJQUFJLENBQUMsV0FBVyxHQUFHLEVBQUUsQ0FBQztRQUMzQixJQUFJLENBQUMsSUFBSSxDQUFDLFdBQVcsQ0FBQyxFQUFFLENBQUMsQ0FBQztRQUUxQixJQUFJLElBQUksQ0FBQyxPQUFPLEVBQUU7WUFDaEIsSUFBSSxDQUFDLE9BQU8sQ0FBQyxRQUFRLEVBQUUsQ0FBQztTQUN6QjtRQUVELE1BQU0sTUFBTSxHQUFHLElBQUksQ0FBQyxJQUFJLENBQUMsTUFBTSxDQUFDO1lBQzlCLElBQUksRUFBRSxFQUFFLFdBQVcsRUFBRSxhQUFhLEVBQUU7U0FDckMsQ0FBQyxDQUFDO1FBQ0gsTUFBTSxRQUFRLEdBQUcsS0FBSyxFQUFFLEdBQVcsRUFBRSxPQUFZLEVBQUUsRUFBRTtZQUNuRCxtREFBbUQ7WUFDbkQsTUFBTSxRQUFRLEdBQUcsSUFBSSxDQUFDLFNBQVMsQ0FBQztZQUNoQyxJQUFJLFNBQVEsYUFBUixRQUFRLHVCQUFSLFFBQVEsQ0FBRSxPQUFPLEtBQUksUUFBUSxDQUFDLE9BQU8sQ0FBQyxHQUFHLENBQUMsRUFBRTtnQkFDOUMsTUFBTSxPQUFPLEdBQUcsTUFBTSxRQUFRLENBQUMsVUFBVSxDQUFDLEdBQUcsQ0FBQyxDQUFDO2dCQUMvQyxHQUFHLEdBQUcsTUFBTSxRQUFRLENBQUMsY0FBYyxDQUFDLE9BQU8sQ0FBQyxDQUFDO2FBQzlDO1lBQ0QsT0FBTyxNQUFNLENBQUMsUUFBUSxDQUFDLEdBQUcsRUFBRSxPQUFPLENBQUMsQ0FBQztRQUN2QyxDQUFDLENBQUM7UUFFRixJQUFJLENBQUMsT0FBTyxHQUFHLE1BQU0sSUFBSSxDQUFDLE9BQU8sQ0FBQyxFQUFFLEVBQUUsSUFBSSxFQUFFO1lBQzFDLE9BQU8sRUFBRSxJQUFJO1lBQ2IsWUFBWSxFQUFFLElBQUk7WUFDbEIsR0FBRyxZQUFZO1lBQ2YsSUFBSTtZQUNKLE1BQU0sRUFBRSxFQUFFLEdBQUcsTUFBTSxFQUFFLFFBQVEsRUFBRTtTQUNoQyxDQUFDLENBQUM7UUFFSCxJQUFJLEtBQUssQ0FBQyxJQUFJLENBQUMsV0FBVyxDQUFDLEVBQUU7WUFDM0IsT0FBTztTQUNSO1FBRUQsaURBQWlEO1FBQ2pELE1BQU0sUUFBUSxHQUFHLE1BQU0sSUFBSSxDQUFDLE9BQU8sQ0FBQyxJQUFJLENBQUMsVUFBVSxDQUNqRCxLQUFLLEVBQ0wsT0FBTyxZQUFZLENBQUMsV0FBVyxLQUFLLFFBQVE7WUFDMUMsQ0FBQyxDQUFDLFlBQVksQ0FBQyxXQUFXO1lBQzFCLENBQUMsQ0FBQyxZQUFZLENBQUMsV0FBVztnQkFDMUIsQ0FBQyxDQUFFLFlBQVksQ0FBQyxXQUFtQixDQUFDLEdBQUc7Z0JBQ3ZDLENBQUMsQ0FBQyxZQUFZLENBQUMsV0FBVyxDQUM3QixDQUFDO1FBQ0YsS0FBSyxDQUFDLE9BQU8sQ0FBQztZQUNaLElBQUksRUFBRSxFQUFFLEdBQUcsS0FBSyxDQUFDLElBQUksRUFBRSxXQUFXLEVBQUUsUUFBUSxDQUFDLEtBQUssQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLENBQUMsRUFBRTtTQUM3RCxDQUFDLENBQUM7SUFDTCxDQUFDO0lBRUQsT0FBTztRQUNMLElBQUksSUFBSSxDQUFDLE9BQU8sRUFBRTtZQUNoQixJQUFJLENBQUMsT0FBTyxDQUFDLFFBQVEsRUFBRSxDQUFDO1NBQ3pCO1FBQ0QsS0FBSyxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQ2xCLENBQUM7Q0FJRjtBQUVEOztHQUVHO0FBQ0ksTUFBTSxlQUFlLEdBQWlDO0lBQzNELElBQUksRUFBRSxJQUFJO0lBQ1YsU0FBUyxFQUFFO1FBQ1QsY0FBYztRQUNkLG1CQUFtQjtRQUNuQixtQkFBbUI7UUFDbkIsbUJBQW1CO0tBQ3BCO0lBQ0QsY0FBYyxFQUFFLE9BQU8sQ0FBQyxFQUFFLENBQUMsSUFBSSxZQUFZLENBQUMsT0FBTyxDQUFDO0NBQ3JELENBQUM7QUFFRixNQUFNLFNBQVMsR0FBMkI7SUFDeEMsRUFBRSxFQUFFLHFDQUFxQztJQUN6QyxXQUFXLEVBQUUsOERBQThEO0lBQzNFLGVBQWU7SUFDZixJQUFJLEVBQUUsRUFBRTtJQUNSLFFBQVEsRUFBRSxNQUFNO0lBQ2hCLDRCQUE0QixFQUFFO1FBQzVCO1lBQ0UsSUFBSSxFQUFFLE9BQU87WUFDYixlQUFlLEVBQUUsT0FBTztZQUN4QixTQUFTLEVBQUUsQ0FBQyxPQUFPLEVBQUUsTUFBTSxDQUFDO1lBQzVCLFVBQVUsRUFBRSxDQUFDLE9BQU8sQ0FBQztTQUN0QjtRQUNEO1lBQ0UsSUFBSSxFQUFFLFlBQVk7WUFDbEIsZUFBZSxFQUFFLFlBQVk7WUFDN0IsU0FBUyxFQUFFLENBQUMsWUFBWSxFQUFFLFlBQVksRUFBRSxZQUFZLEVBQUUsTUFBTSxDQUFDO1lBQzdELFVBQVUsRUFBRSxDQUFDLFlBQVksRUFBRSxZQUFZLEVBQUUsWUFBWSxDQUFDO1NBQ3ZEO0tBQ0Y7SUFDRCxTQUFTLEVBQUU7UUFDVDtZQUNFLFNBQVMsRUFBRSxDQUFDLGNBQWMsQ0FBQztZQUMzQixJQUFJLEVBQUUsT0FBTztZQUNiLFVBQVUsRUFBRSxDQUFDLEtBQUssRUFBRSxVQUFVLEVBQUUsT0FBTyxDQUFDO1lBQ3hDLElBQUksRUFBRSxvQkFBb0I7U0FDM0I7UUFDRDtZQUNFLFNBQVMsRUFBRSxDQUFDLG1CQUFtQixDQUFDO1lBQ2hDLElBQUksRUFBRSxZQUFZO1lBQ2xCLFVBQVUsRUFBRSxDQUFDLEtBQUssRUFBRSxVQUFVLEVBQUUsV0FBVyxDQUFDO1lBQzVDLElBQUksRUFBRSxvQkFBb0I7U0FDM0I7UUFDRDtZQUNFLFNBQVMsRUFBRSxDQUFDLG1CQUFtQixDQUFDO1lBQ2hDLElBQUksRUFBRSxZQUFZO1lBQ2xCLFVBQVUsRUFBRSxFQUFFO1lBQ2QsSUFBSSxFQUFFLG9CQUFvQjtTQUMzQjtRQUNEO1lBQ0UsU0FBUyxFQUFFLENBQUMsbUJBQW1CLENBQUM7WUFDaEMsSUFBSSxFQUFFLFlBQVk7WUFDbEIsVUFBVSxFQUFFLEVBQUU7WUFDZCxJQUFJLEVBQUUsb0JBQW9CO1NBQzNCO0tBQ0Y7Q0FDRixDQUFDO0FBRUYsaUVBQWUsU0FBUyxFQUFDO0FBRXpCOztHQUVHO0FBQ0gsSUFBVSxPQUFPLENBdUJoQjtBQXZCRCxXQUFVLE9BQU87SUFXZjs7T0FFRztJQUNILFNBQWdCLFVBQVU7UUFDeEIsSUFBSSxpQkFBUyxFQUFFO1lBQ2IsT0FBTyxpQkFBUyxDQUFDO1NBQ2xCO1FBRUQsaUJBQVMsR0FBRyxtT0FBb0IsQ0FBQztRQUVqQyxPQUFPLGlCQUFTLENBQUM7SUFDbkIsQ0FBQztJQVJlLGtCQUFVLGFBUXpCO0FBQ0gsQ0FBQyxFQXZCUyxPQUFPLEtBQVAsT0FBTyxRQXVCaEIiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdmVnYTUtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHZlZ2E1LWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcbmltcG9ydCB7IEpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyBXaWRnZXQgfSBmcm9tICdAbHVtaW5vL3dpZGdldHMnO1xuaW1wb3J0ICogYXMgVmVnYU1vZHVsZVR5cGUgZnJvbSAndmVnYS1lbWJlZCc7XG5cbi8qKlxuICogVGhlIENTUyBjbGFzcyB0byBhZGQgdG8gdGhlIFZlZ2EgYW5kIFZlZ2EtTGl0ZSB3aWRnZXQuXG4gKi9cbmNvbnN0IFZFR0FfQ09NTU9OX0NMQVNTID0gJ2pwLVJlbmRlcmVkVmVnYUNvbW1vbjUnO1xuXG4vKipcbiAqIFRoZSBDU1MgY2xhc3MgdG8gYWRkIHRvIHRoZSBWZWdhLlxuICovXG5jb25zdCBWRUdBX0NMQVNTID0gJ2pwLVJlbmRlcmVkVmVnYTUnO1xuXG4vKipcbiAqIFRoZSBDU1MgY2xhc3MgdG8gYWRkIHRvIHRoZSBWZWdhLUxpdGUuXG4gKi9cbmNvbnN0IFZFR0FMSVRFX0NMQVNTID0gJ2pwLVJlbmRlcmVkVmVnYUxpdGUnO1xuXG4vKipcbiAqIFRoZSBNSU1FIHR5cGUgZm9yIFZlZ2EuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhlIHZlcnNpb24gb2YgdGhpcyBmb2xsb3dzIHRoZSBtYWpvciB2ZXJzaW9uIG9mIFZlZ2EuXG4gKi9cbmV4cG9ydCBjb25zdCBWRUdBX01JTUVfVFlQRSA9ICdhcHBsaWNhdGlvbi92bmQudmVnYS52NStqc29uJztcblxuLyoqXG4gKiBUaGUgTUlNRSB0eXBlIGZvciBWZWdhLUxpdGUuXG4gKlxuICogIyMjIyBOb3Rlc1xuICogVGhlIHZlcnNpb24gb2YgdGhpcyBmb2xsb3dzIHRoZSBtYWpvciB2ZXJzaW9uIG9mIFZlZ2EtTGl0ZS5cbiAqL1xuZXhwb3J0IGNvbnN0IFZFR0FMSVRFM19NSU1FX1RZUEUgPSAnYXBwbGljYXRpb24vdm5kLnZlZ2FsaXRlLnYzK2pzb24nO1xuXG4vKipcbiAqIFRoZSBNSU1FIHR5cGUgZm9yIFZlZ2EtTGl0ZS5cbiAqXG4gKiAjIyMjIE5vdGVzXG4gKiBUaGUgdmVyc2lvbiBvZiB0aGlzIGZvbGxvd3MgdGhlIG1ham9yIHZlcnNpb24gb2YgVmVnYS1MaXRlLlxuICovXG5leHBvcnQgY29uc3QgVkVHQUxJVEU0X01JTUVfVFlQRSA9ICdhcHBsaWNhdGlvbi92bmQudmVnYWxpdGUudjQranNvbic7XG5cbi8qKlxuICogVGhlIE1JTUUgdHlwZSBmb3IgVmVnYS1MaXRlLlxuICpcbiAqICMjIyMgTm90ZXNcbiAqIFRoZSB2ZXJzaW9uIG9mIHRoaXMgZm9sbG93cyB0aGUgbWFqb3IgdmVyc2lvbiBvZiBWZWdhLUxpdGUuXG4gKi9cbmV4cG9ydCBjb25zdCBWRUdBTElURTVfTUlNRV9UWVBFID0gJ2FwcGxpY2F0aW9uL3ZuZC52ZWdhbGl0ZS52NStqc29uJztcblxuLyoqXG4gKiBBIHdpZGdldCBmb3IgcmVuZGVyaW5nIFZlZ2Egb3IgVmVnYS1MaXRlIGRhdGEsIGZvciB1c2FnZSB3aXRoIHJlbmRlcm1pbWUuXG4gKi9cbmV4cG9ydCBjbGFzcyBSZW5kZXJlZFZlZ2EgZXh0ZW5kcyBXaWRnZXQgaW1wbGVtZW50cyBJUmVuZGVyTWltZS5JUmVuZGVyZXIge1xuICBwcml2YXRlIF9yZXN1bHQ6IFZlZ2FNb2R1bGVUeXBlLlJlc3VsdDtcblxuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHdpZGdldCBmb3IgcmVuZGVyaW5nIFZlZ2EvVmVnYS1MaXRlLlxuICAgKi9cbiAgY29uc3RydWN0b3Iob3B0aW9uczogSVJlbmRlck1pbWUuSVJlbmRlcmVyT3B0aW9ucykge1xuICAgIHN1cGVyKCk7XG4gICAgdGhpcy5fbWltZVR5cGUgPSBvcHRpb25zLm1pbWVUeXBlO1xuICAgIHRoaXMuX3Jlc29sdmVyID0gb3B0aW9ucy5yZXNvbHZlcjtcbiAgICB0aGlzLmFkZENsYXNzKFZFR0FfQ09NTU9OX0NMQVNTKTtcbiAgICB0aGlzLmFkZENsYXNzKFxuICAgICAgdGhpcy5fbWltZVR5cGUgPT09IFZFR0FfTUlNRV9UWVBFID8gVkVHQV9DTEFTUyA6IFZFR0FMSVRFX0NMQVNTXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW5kZXIgVmVnYS9WZWdhLUxpdGUgaW50byB0aGlzIHdpZGdldCdzIG5vZGUuXG4gICAqL1xuICBhc3luYyByZW5kZXJNb2RlbChtb2RlbDogSVJlbmRlck1pbWUuSU1pbWVNb2RlbCk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHNwZWMgPSBtb2RlbC5kYXRhW3RoaXMuX21pbWVUeXBlXSBhcyBKU09OT2JqZWN0IHwgdW5kZWZpbmVkO1xuICAgIGlmIChzcGVjID09PSB1bmRlZmluZWQpIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG4gICAgY29uc3QgbWV0YWRhdGEgPSBtb2RlbC5tZXRhZGF0YVt0aGlzLl9taW1lVHlwZV0gYXNcbiAgICAgIHwge1xuICAgICAgICAgIGVtYmVkX29wdGlvbnM/OiBWZWdhTW9kdWxlVHlwZS5FbWJlZE9wdGlvbnM7XG4gICAgICAgIH1cbiAgICAgIHwgdW5kZWZpbmVkO1xuICAgIGNvbnN0IGVtYmVkT3B0aW9ucyA9XG4gICAgICBtZXRhZGF0YSAmJiBtZXRhZGF0YS5lbWJlZF9vcHRpb25zID8gbWV0YWRhdGEuZW1iZWRfb3B0aW9ucyA6IHt9O1xuXG4gICAgLy8gSWYgdGhlIEp1cHl0ZXJMYWIgdGhlbWUgaXMgZGFyaywgcmVuZGVyIHRoaXMgdXNpbmcgYSBkYXJrIFZlZ2EgdGhlbWUuXG4gICAgbGV0IGJvZHlUaGVtZURhcmsgPSBkb2N1bWVudC5ib2R5LmRhdGFzZXQuanBUaGVtZUxpZ2h0ID09PSAnZmFsc2UnO1xuICAgIGlmIChib2R5VGhlbWVEYXJrKSB7XG4gICAgICBlbWJlZE9wdGlvbnMudGhlbWUgPSAnZGFyayc7XG4gICAgfVxuXG4gICAgY29uc3QgbW9kZTogVmVnYU1vZHVsZVR5cGUuTW9kZSA9XG4gICAgICB0aGlzLl9taW1lVHlwZSA9PT0gVkVHQV9NSU1FX1RZUEUgPyAndmVnYScgOiAndmVnYS1saXRlJztcblxuICAgIGNvbnN0IHZlZ2EgPVxuICAgICAgUHJpdmF0ZS52ZWdhICE9IG51bGwgPyBQcml2YXRlLnZlZ2EgOiBhd2FpdCBQcml2YXRlLmVuc3VyZVZlZ2EoKTtcblxuICAgIGNvbnN0IGVsID0gZG9jdW1lbnQuY3JlYXRlRWxlbWVudCgnZGl2Jyk7XG5cbiAgICAvLyBjbGVhciB0aGUgb3V0cHV0IGJlZm9yZSBhdHRhY2hpbmcgYSBjaGFydFxuICAgIHRoaXMubm9kZS50ZXh0Q29udGVudCA9ICcnO1xuICAgIHRoaXMubm9kZS5hcHBlbmRDaGlsZChlbCk7XG5cbiAgICBpZiAodGhpcy5fcmVzdWx0KSB7XG4gICAgICB0aGlzLl9yZXN1bHQuZmluYWxpemUoKTtcbiAgICB9XG5cbiAgICBjb25zdCBsb2FkZXIgPSB2ZWdhLnZlZ2EubG9hZGVyKHtcbiAgICAgIGh0dHA6IHsgY3JlZGVudGlhbHM6ICdzYW1lLW9yaWdpbicgfVxuICAgIH0pO1xuICAgIGNvbnN0IHNhbml0aXplID0gYXN5bmMgKHVyaTogc3RyaW5nLCBvcHRpb25zOiBhbnkpID0+IHtcbiAgICAgIC8vIFVzZSB0aGUgcmVzb2x2ZXIgZm9yIGFueSBVUklzIGl0IHdhbnRzIHRvIGhhbmRsZVxuICAgICAgY29uc3QgcmVzb2x2ZXIgPSB0aGlzLl9yZXNvbHZlcjtcbiAgICAgIGlmIChyZXNvbHZlcj8uaXNMb2NhbCAmJiByZXNvbHZlci5pc0xvY2FsKHVyaSkpIHtcbiAgICAgICAgY29uc3QgYWJzUGF0aCA9IGF3YWl0IHJlc29sdmVyLnJlc29sdmVVcmwodXJpKTtcbiAgICAgICAgdXJpID0gYXdhaXQgcmVzb2x2ZXIuZ2V0RG93bmxvYWRVcmwoYWJzUGF0aCk7XG4gICAgICB9XG4gICAgICByZXR1cm4gbG9hZGVyLnNhbml0aXplKHVyaSwgb3B0aW9ucyk7XG4gICAgfTtcblxuICAgIHRoaXMuX3Jlc3VsdCA9IGF3YWl0IHZlZ2EuZGVmYXVsdChlbCwgc3BlYywge1xuICAgICAgYWN0aW9uczogdHJ1ZSxcbiAgICAgIGRlZmF1bHRTdHlsZTogdHJ1ZSxcbiAgICAgIC4uLmVtYmVkT3B0aW9ucyxcbiAgICAgIG1vZGUsXG4gICAgICBsb2FkZXI6IHsgLi4ubG9hZGVyLCBzYW5pdGl6ZSB9XG4gICAgfSk7XG5cbiAgICBpZiAobW9kZWwuZGF0YVsnaW1hZ2UvcG5nJ10pIHtcbiAgICAgIHJldHVybjtcbiAgICB9XG5cbiAgICAvLyBBZGQgcG5nIHJlcHJlc2VudGF0aW9uIG9mIHZlZ2EgY2hhcnQgdG8gb3V0cHV0XG4gICAgY29uc3QgaW1hZ2VVUkwgPSBhd2FpdCB0aGlzLl9yZXN1bHQudmlldy50b0ltYWdlVVJMKFxuICAgICAgJ3BuZycsXG4gICAgICB0eXBlb2YgZW1iZWRPcHRpb25zLnNjYWxlRmFjdG9yID09PSAnbnVtYmVyJ1xuICAgICAgICA/IGVtYmVkT3B0aW9ucy5zY2FsZUZhY3RvclxuICAgICAgICA6IGVtYmVkT3B0aW9ucy5zY2FsZUZhY3RvclxuICAgICAgICA/IChlbWJlZE9wdGlvbnMuc2NhbGVGYWN0b3IgYXMgYW55KS5wbmdcbiAgICAgICAgOiBlbWJlZE9wdGlvbnMuc2NhbGVGYWN0b3JcbiAgICApO1xuICAgIG1vZGVsLnNldERhdGEoe1xuICAgICAgZGF0YTogeyAuLi5tb2RlbC5kYXRhLCAnaW1hZ2UvcG5nJzogaW1hZ2VVUkwuc3BsaXQoJywnKVsxXSB9XG4gICAgfSk7XG4gIH1cblxuICBkaXNwb3NlKCk6IHZvaWQge1xuICAgIGlmICh0aGlzLl9yZXN1bHQpIHtcbiAgICAgIHRoaXMuX3Jlc3VsdC5maW5hbGl6ZSgpO1xuICAgIH1cbiAgICBzdXBlci5kaXNwb3NlKCk7XG4gIH1cblxuICBwcml2YXRlIF9taW1lVHlwZTogc3RyaW5nO1xuICBwcml2YXRlIF9yZXNvbHZlcjogSVJlbmRlck1pbWUuSVJlc29sdmVyIHwgbnVsbDtcbn1cblxuLyoqXG4gKiBBIG1pbWUgcmVuZGVyZXIgZmFjdG9yeSBmb3IgdmVnYSBkYXRhLlxuICovXG5leHBvcnQgY29uc3QgcmVuZGVyZXJGYWN0b3J5OiBJUmVuZGVyTWltZS5JUmVuZGVyZXJGYWN0b3J5ID0ge1xuICBzYWZlOiB0cnVlLFxuICBtaW1lVHlwZXM6IFtcbiAgICBWRUdBX01JTUVfVFlQRSxcbiAgICBWRUdBTElURTNfTUlNRV9UWVBFLFxuICAgIFZFR0FMSVRFNF9NSU1FX1RZUEUsXG4gICAgVkVHQUxJVEU1X01JTUVfVFlQRVxuICBdLFxuICBjcmVhdGVSZW5kZXJlcjogb3B0aW9ucyA9PiBuZXcgUmVuZGVyZWRWZWdhKG9wdGlvbnMpXG59O1xuXG5jb25zdCBleHRlbnNpb246IElSZW5kZXJNaW1lLklFeHRlbnNpb24gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvdmVnYTUtZXh0ZW5zaW9uOmZhY3RvcnknLFxuICBkZXNjcmlwdGlvbjogJ1Byb3ZpZGVzIGEgcmVuZGVyZXIgZm9yIFZlZ2EgNSBhbmQgVmVnYS1MaXRlIDMgdG8gNSBjb250ZW50LicsXG4gIHJlbmRlcmVyRmFjdG9yeSxcbiAgcmFuazogNTcsXG4gIGRhdGFUeXBlOiAnanNvbicsXG4gIGRvY3VtZW50V2lkZ2V0RmFjdG9yeU9wdGlvbnM6IFtcbiAgICB7XG4gICAgICBuYW1lOiAnVmVnYTUnLFxuICAgICAgcHJpbWFyeUZpbGVUeXBlOiAndmVnYTUnLFxuICAgICAgZmlsZVR5cGVzOiBbJ3ZlZ2E1JywgJ2pzb24nXSxcbiAgICAgIGRlZmF1bHRGb3I6IFsndmVnYTUnXVxuICAgIH0sXG4gICAge1xuICAgICAgbmFtZTogJ1ZlZ2EtTGl0ZTUnLFxuICAgICAgcHJpbWFyeUZpbGVUeXBlOiAndmVnYS1saXRlNScsXG4gICAgICBmaWxlVHlwZXM6IFsndmVnYS1saXRlMycsICd2ZWdhLWxpdGU0JywgJ3ZlZ2EtbGl0ZTUnLCAnanNvbiddLFxuICAgICAgZGVmYXVsdEZvcjogWyd2ZWdhLWxpdGUzJywgJ3ZlZ2EtbGl0ZTQnLCAndmVnYS1saXRlNSddXG4gICAgfVxuICBdLFxuICBmaWxlVHlwZXM6IFtcbiAgICB7XG4gICAgICBtaW1lVHlwZXM6IFtWRUdBX01JTUVfVFlQRV0sXG4gICAgICBuYW1lOiAndmVnYTUnLFxuICAgICAgZXh0ZW5zaW9uczogWycudmcnLCAnLnZnLmpzb24nLCAnLnZlZ2EnXSxcbiAgICAgIGljb246ICd1aS1jb21wb25lbnRzOnZlZ2EnXG4gICAgfSxcbiAgICB7XG4gICAgICBtaW1lVHlwZXM6IFtWRUdBTElURTVfTUlNRV9UWVBFXSxcbiAgICAgIG5hbWU6ICd2ZWdhLWxpdGU1JyxcbiAgICAgIGV4dGVuc2lvbnM6IFsnLnZsJywgJy52bC5qc29uJywgJy52ZWdhbGl0ZSddLFxuICAgICAgaWNvbjogJ3VpLWNvbXBvbmVudHM6dmVnYSdcbiAgICB9LFxuICAgIHtcbiAgICAgIG1pbWVUeXBlczogW1ZFR0FMSVRFNF9NSU1FX1RZUEVdLFxuICAgICAgbmFtZTogJ3ZlZ2EtbGl0ZTQnLFxuICAgICAgZXh0ZW5zaW9uczogW10sXG4gICAgICBpY29uOiAndWktY29tcG9uZW50czp2ZWdhJ1xuICAgIH0sXG4gICAge1xuICAgICAgbWltZVR5cGVzOiBbVkVHQUxJVEUzX01JTUVfVFlQRV0sXG4gICAgICBuYW1lOiAndmVnYS1saXRlMycsXG4gICAgICBleHRlbnNpb25zOiBbXSxcbiAgICAgIGljb246ICd1aS1jb21wb25lbnRzOnZlZ2EnXG4gICAgfVxuICBdXG59O1xuXG5leHBvcnQgZGVmYXVsdCBleHRlbnNpb247XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgbW9kdWxlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIEEgY2FjaGVkIHJlZmVyZW5jZSB0byB0aGUgdmVnYSBsaWJyYXJ5LlxuICAgKi9cbiAgZXhwb3J0IGxldCB2ZWdhOiB0eXBlb2YgVmVnYU1vZHVsZVR5cGU7XG5cbiAgLyoqXG4gICAqIEEgUHJvbWlzZSBmb3IgdGhlIGluaXRpYWwgbG9hZCBvZiB2ZWdhLlxuICAgKi9cbiAgZXhwb3J0IGxldCB2ZWdhUmVhZHk6IFByb21pc2U8dHlwZW9mIFZlZ2FNb2R1bGVUeXBlPjtcblxuICAvKipcbiAgICogTGF6eS1sb2FkIGFuZCBjYWNoZSB0aGUgdmVnYS1lbWJlZCBsaWJyYXJ5XG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gZW5zdXJlVmVnYSgpOiBQcm9taXNlPHR5cGVvZiBWZWdhTW9kdWxlVHlwZT4ge1xuICAgIGlmICh2ZWdhUmVhZHkpIHtcbiAgICAgIHJldHVybiB2ZWdhUmVhZHk7XG4gICAgfVxuXG4gICAgdmVnYVJlYWR5ID0gaW1wb3J0KCd2ZWdhLWVtYmVkJyk7XG5cbiAgICByZXR1cm4gdmVnYVJlYWR5O1xuICB9XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=