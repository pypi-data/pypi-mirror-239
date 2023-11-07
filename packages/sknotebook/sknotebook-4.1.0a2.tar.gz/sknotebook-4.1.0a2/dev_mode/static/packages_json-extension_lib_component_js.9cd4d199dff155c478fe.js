"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_json-extension_lib_component_js"],{

/***/ "../packages/json-extension/lib/component.js":
/*!***************************************************!*\
  !*** ../packages/json-extension/lib/component.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Component": () => (/* binding */ Component)
/* harmony export */ });
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lezer_highlight__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lezer/highlight */ "webpack/sharing/consume/default/@lezer/highlight/@lezer/highlight");
/* harmony import */ var _lezer_highlight__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react_highlight_words__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react-highlight-words */ "webpack/sharing/consume/default/react-highlight-words/react-highlight-words");
/* harmony import */ var react_highlight_words__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react_highlight_words__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var react_json_tree__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react-json-tree */ "webpack/sharing/consume/default/react-json-tree/react-json-tree");
/* harmony import */ var react_json_tree__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react_json_tree__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var style_mod__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! style-mod */ "webpack/sharing/consume/default/style-mod/style-mod");
/* harmony import */ var style_mod__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(style_mod__WEBPACK_IMPORTED_MODULE_8__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.









/**
 * Get the CodeMirror style for a given tag.
 */
function getStyle(tag) {
    var _a;
    return (_a = _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__.jupyterHighlightStyle.style([tag])) !== null && _a !== void 0 ? _a : '';
}
/**
 * A component that renders JSON data as a collapsible tree.
 */
class Component extends react__WEBPACK_IMPORTED_MODULE_5__.Component {
    constructor() {
        super(...arguments);
        this.state = { filter: '', value: '' };
        this.timer = 0;
        this.handleChange = (event) => {
            const { value } = event.target;
            this.setState({ value });
            window.clearTimeout(this.timer);
            this.timer = window.setTimeout(() => {
                this.setState({ filter: value });
            }, 300);
        };
    }
    componentDidMount() {
        style_mod__WEBPACK_IMPORTED_MODULE_8__.StyleModule.mount(document, _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_0__.jupyterHighlightStyle.module);
    }
    render() {
        const translator = this.props.translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        const trans = translator.load('jupyterlab');
        const { data, metadata, forwardedRef } = this.props;
        const root = metadata && metadata.root ? metadata.root : 'root';
        const keyPaths = this.state.filter
            ? filterPaths(data, this.state.filter, [root])
            : [root];
        return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "container", ref: forwardedRef },
            react__WEBPACK_IMPORTED_MODULE_5__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.InputGroup, { className: "filter", type: "text", placeholder: trans.__('Filter…'), onChange: this.handleChange, value: this.state.value, rightIcon: "ui-components:search" }),
            react__WEBPACK_IMPORTED_MODULE_5__.createElement(react_json_tree__WEBPACK_IMPORTED_MODULE_7__.JSONTree, { data: data, collectionLimit: 100, theme: {
                    extend: theme,
                    valueLabel: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.variableName),
                    valueText: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.string),
                    nestedNodeItemString: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.comment)
                }, invertTheme: false, keyPath: [root], getItemString: (type, data, itemType, itemString) => Array.isArray(data) ? (
                // Always display array type and the number of items i.e. "[] 2 items".
                react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", null,
                    itemType,
                    " ",
                    itemString)) : Object.keys(data).length === 0 ? (
                // Only display object type when it's empty i.e. "{}".
                react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", null, itemType)) : (null // Upstream typings don't accept null, but it should be ok
                ), labelRenderer: ([label, type]) => {
                    return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", { className: getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.keyword) },
                        react__WEBPACK_IMPORTED_MODULE_5__.createElement((react_highlight_words__WEBPACK_IMPORTED_MODULE_6___default()), { searchWords: [this.state.filter], textToHighlight: `${label}`, highlightClassName: "jp-mod-selected" })));
                }, valueRenderer: raw => {
                    let className = getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.string);
                    if (typeof raw === 'number') {
                        className = getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.number);
                    }
                    if (raw === 'true' || raw === 'false') {
                        className = getStyle(_lezer_highlight__WEBPACK_IMPORTED_MODULE_3__.tags.keyword);
                    }
                    return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("span", { className: className },
                        react__WEBPACK_IMPORTED_MODULE_5__.createElement((react_highlight_words__WEBPACK_IMPORTED_MODULE_6___default()), { searchWords: [this.state.filter], textToHighlight: `${raw}`, highlightClassName: "jp-mod-selected" })));
                }, shouldExpandNodeInitially: (keyPath, data, level) => metadata && metadata.expanded
                    ? true
                    : keyPaths.join(',').includes(keyPath.join(',')) })));
    }
}
// Provide an invalid theme object (this is on purpose!) to invalidate the
// react-json-tree's inline styles that override CodeMirror CSS classes
const theme = {
    scheme: 'jupyter',
    base00: 'invalid',
    base01: 'invalid',
    base02: 'invalid',
    base03: 'invalid',
    base04: 'invalid',
    base05: 'invalid',
    base06: 'invalid',
    base07: 'invalid',
    base08: 'invalid',
    base09: 'invalid',
    base0A: 'invalid',
    base0B: 'invalid',
    base0C: 'invalid',
    base0D: 'invalid',
    base0E: 'invalid',
    base0F: 'invalid',
    author: 'invalid'
};
function objectIncludes(data, query) {
    return JSON.stringify(data).includes(query);
}
function filterPaths(data, query, parent = ['root']) {
    if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.isArray(data)) {
        return data.reduce((result, item, index) => {
            if (item && typeof item === 'object' && objectIncludes(item, query)) {
                return [
                    ...result,
                    [index, ...parent].join(','),
                    ...filterPaths(item, query, [index, ...parent])
                ];
            }
            return result;
        }, []);
    }
    if (_lumino_coreutils__WEBPACK_IMPORTED_MODULE_4__.JSONExt.isObject(data)) {
        return Object.keys(data).reduce((result, key) => {
            const item = data[key];
            if (item &&
                typeof item === 'object' &&
                (key.includes(query) || objectIncludes(item, query))) {
                return [
                    ...result,
                    [key, ...parent].join(','),
                    ...filterPaths(item, query, [key, ...parent])
                ];
            }
            return result;
        }, []);
    }
    return [];
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfanNvbi1leHRlbnNpb25fbGliX2NvbXBvbmVudF9qcy45Y2Q0ZDE5OWRmZjE1NWM0NzhmZS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUVJO0FBQ087QUFDZjtBQUNWO0FBQ2lDO0FBQy9DO0FBQ2lCO0FBQ0w7QUFDSDtBQXdCeEM7O0dBRUc7QUFDSCxTQUFTLFFBQVEsQ0FBQyxHQUFROztJQUN4QixPQUFPLHFGQUEyQixDQUFDLENBQUMsR0FBRyxDQUFDLENBQUMsbUNBQUksRUFBRSxDQUFDO0FBQ2xELENBQUM7QUFFRDs7R0FFRztBQUNJLE1BQU0sU0FBVSxTQUFRLDRDQUErQjtJQUE5RDs7UUFDRSxVQUFLLEdBQUcsRUFBRSxNQUFNLEVBQUUsRUFBRSxFQUFFLEtBQUssRUFBRSxFQUFFLEVBQUUsQ0FBQztRQUVsQyxVQUFLLEdBQVcsQ0FBQyxDQUFDO1FBTWxCLGlCQUFZLEdBQUcsQ0FBQyxLQUEwQyxFQUFRLEVBQUU7WUFDbEUsTUFBTSxFQUFFLEtBQUssRUFBRSxHQUFHLEtBQUssQ0FBQyxNQUFNLENBQUM7WUFDL0IsSUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLEtBQUssRUFBRSxDQUFDLENBQUM7WUFDekIsTUFBTSxDQUFDLFlBQVksQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLENBQUM7WUFDaEMsSUFBSSxDQUFDLEtBQUssR0FBRyxNQUFNLENBQUMsVUFBVSxDQUFDLEdBQUcsRUFBRTtnQkFDbEMsSUFBSSxDQUFDLFFBQVEsQ0FBQyxFQUFFLE1BQU0sRUFBRSxLQUFLLEVBQUUsQ0FBQyxDQUFDO1lBQ25DLENBQUMsRUFBRSxHQUFHLENBQUMsQ0FBQztRQUNWLENBQUMsQ0FBQztJQW1GSixDQUFDO0lBOUZDLGlCQUFpQjtRQUNmLHdEQUFpQixDQUFDLFFBQVEsRUFBRSxnRkFBMkMsQ0FBQyxDQUFDO0lBQzNFLENBQUM7SUFXRCxNQUFNO1FBQ0osTUFBTSxVQUFVLEdBQUcsSUFBSSxDQUFDLEtBQUssQ0FBQyxVQUFVLElBQUksbUVBQWMsQ0FBQztRQUMzRCxNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBRTVDLE1BQU0sRUFBRSxJQUFJLEVBQUUsUUFBUSxFQUFFLFlBQVksRUFBRSxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUM7UUFDcEQsTUFBTSxJQUFJLEdBQUcsUUFBUSxJQUFJLFFBQVEsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFFLFFBQVEsQ0FBQyxJQUFlLENBQUMsQ0FBQyxDQUFDLE1BQU0sQ0FBQztRQUM1RSxNQUFNLFFBQVEsR0FBRyxJQUFJLENBQUMsS0FBSyxDQUFDLE1BQU07WUFDaEMsQ0FBQyxDQUFDLFdBQVcsQ0FBQyxJQUFJLEVBQUUsSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNLEVBQUUsQ0FBQyxJQUFJLENBQUMsQ0FBQztZQUM5QyxDQUFDLENBQUMsQ0FBQyxJQUFJLENBQUMsQ0FBQztRQUNYLE9BQU8sQ0FDTCwwREFBSyxTQUFTLEVBQUMsV0FBVyxFQUFDLEdBQUcsRUFBRSxZQUFZO1lBQzFDLGlEQUFDLGlFQUFVLElBQ1QsU0FBUyxFQUFDLFFBQVEsRUFDbEIsSUFBSSxFQUFDLE1BQU0sRUFDWCxXQUFXLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxTQUFTLENBQUMsRUFDaEMsUUFBUSxFQUFFLElBQUksQ0FBQyxZQUFZLEVBQzNCLEtBQUssRUFBRSxJQUFJLENBQUMsS0FBSyxDQUFDLEtBQUssRUFDdkIsU0FBUyxFQUFDLHNCQUFzQixHQUNoQztZQUNGLGlEQUFDLHFEQUFRLElBQ1AsSUFBSSxFQUFFLElBQUksRUFDVixlQUFlLEVBQUUsR0FBRyxFQUNwQixLQUFLLEVBQUU7b0JBQ0wsTUFBTSxFQUFFLEtBQUs7b0JBQ2IsVUFBVSxFQUFFLFFBQVEsQ0FBQywrREFBaUIsQ0FBQztvQkFDdkMsU0FBUyxFQUFFLFFBQVEsQ0FBQyx5REFBVyxDQUFDO29CQUNoQyxvQkFBb0IsRUFBRSxRQUFRLENBQUMsMERBQVksQ0FBQztpQkFDN0MsRUFDRCxXQUFXLEVBQUUsS0FBSyxFQUNsQixPQUFPLEVBQUUsQ0FBQyxJQUFJLENBQUMsRUFDZixhQUFhLEVBQUUsQ0FBQyxJQUFJLEVBQUUsSUFBSSxFQUFFLFFBQVEsRUFBRSxVQUFVLEVBQUUsRUFBRSxDQUNsRCxLQUFLLENBQUMsT0FBTyxDQUFDLElBQUksQ0FBQyxDQUFDLENBQUMsQ0FBQztnQkFDcEIsdUVBQXVFO2dCQUN2RTtvQkFDRyxRQUFROztvQkFBRyxVQUFVLENBQ2pCLENBQ1IsQ0FBQyxDQUFDLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxJQUFjLENBQUMsQ0FBQyxNQUFNLEtBQUssQ0FBQyxDQUFDLENBQUMsQ0FBQztnQkFDN0Msc0RBQXNEO2dCQUN0RCwrREFBTyxRQUFRLENBQVEsQ0FDeEIsQ0FBQyxDQUFDLENBQUMsQ0FDRixJQUFLLENBQUMsMERBQTBEO2lCQUNqRSxFQUVILGFBQWEsRUFBRSxDQUFDLENBQUMsS0FBSyxFQUFFLElBQUksQ0FBQyxFQUFFLEVBQUU7b0JBQy9CLE9BQU8sQ0FDTCwyREFBTSxTQUFTLEVBQUUsUUFBUSxDQUFDLDBEQUFZLENBQUM7d0JBQ3JDLGlEQUFDLDhEQUFXLElBQ1YsV0FBVyxFQUFFLENBQUMsSUFBSSxDQUFDLEtBQUssQ0FBQyxNQUFNLENBQUMsRUFDaEMsZUFBZSxFQUFFLEdBQUcsS0FBSyxFQUFFLEVBQzNCLGtCQUFrQixFQUFDLGlCQUFpQixHQUN2QixDQUNWLENBQ1IsQ0FBQztnQkFDSixDQUFDLEVBQ0QsYUFBYSxFQUFFLEdBQUcsQ0FBQyxFQUFFO29CQUNuQixJQUFJLFNBQVMsR0FBRyxRQUFRLENBQUMseURBQVcsQ0FBQyxDQUFDO29CQUN0QyxJQUFJLE9BQU8sR0FBRyxLQUFLLFFBQVEsRUFBRTt3QkFDM0IsU0FBUyxHQUFHLFFBQVEsQ0FBQyx5REFBVyxDQUFDLENBQUM7cUJBQ25DO29CQUNELElBQUksR0FBRyxLQUFLLE1BQU0sSUFBSSxHQUFHLEtBQUssT0FBTyxFQUFFO3dCQUNyQyxTQUFTLEdBQUcsUUFBUSxDQUFDLDBEQUFZLENBQUMsQ0FBQztxQkFDcEM7b0JBQ0QsT0FBTyxDQUNMLDJEQUFNLFNBQVMsRUFBRSxTQUFTO3dCQUN4QixpREFBQyw4REFBVyxJQUNWLFdBQVcsRUFBRSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsTUFBTSxDQUFDLEVBQ2hDLGVBQWUsRUFBRSxHQUFHLEdBQUcsRUFBRSxFQUN6QixrQkFBa0IsRUFBQyxpQkFBaUIsR0FDdkIsQ0FDVixDQUNSLENBQUM7Z0JBQ0osQ0FBQyxFQUNELHlCQUF5QixFQUFFLENBQUMsT0FBTyxFQUFFLElBQUksRUFBRSxLQUFLLEVBQUUsRUFBRSxDQUNsRCxRQUFRLElBQUksUUFBUSxDQUFDLFFBQVE7b0JBQzNCLENBQUMsQ0FBQyxJQUFJO29CQUNOLENBQUMsQ0FBQyxRQUFRLENBQUMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxDQUFDLEdBRXBELENBQ0UsQ0FDUCxDQUFDO0lBQ0osQ0FBQztDQUNGO0FBRUQsMEVBQTBFO0FBQzFFLHVFQUF1RTtBQUN2RSxNQUFNLEtBQUssR0FBRztJQUNaLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0lBQ2pCLE1BQU0sRUFBRSxTQUFTO0NBQ2xCLENBQUM7QUFFRixTQUFTLGNBQWMsQ0FBQyxJQUFlLEVBQUUsS0FBYTtJQUNwRCxPQUFPLElBQUksQ0FBQyxTQUFTLENBQUMsSUFBSSxDQUFDLENBQUMsUUFBUSxDQUFDLEtBQUssQ0FBQyxDQUFDO0FBQzlDLENBQUM7QUFFRCxTQUFTLFdBQVcsQ0FDbEIsSUFBNEIsRUFDNUIsS0FBYSxFQUNiLFNBQW9CLENBQUMsTUFBTSxDQUFDO0lBRTVCLElBQUksOERBQWUsQ0FBQyxJQUFJLENBQUMsRUFBRTtRQUN6QixPQUFPLElBQUksQ0FBQyxNQUFNLENBQUMsQ0FBQyxNQUFpQixFQUFFLElBQWUsRUFBRSxLQUFhLEVBQUUsRUFBRTtZQUN2RSxJQUFJLElBQUksSUFBSSxPQUFPLElBQUksS0FBSyxRQUFRLElBQUksY0FBYyxDQUFDLElBQUksRUFBRSxLQUFLLENBQUMsRUFBRTtnQkFDbkUsT0FBTztvQkFDTCxHQUFHLE1BQU07b0JBQ1QsQ0FBQyxLQUFLLEVBQUUsR0FBRyxNQUFNLENBQUMsQ0FBQyxJQUFJLENBQUMsR0FBRyxDQUFDO29CQUM1QixHQUFHLFdBQVcsQ0FBQyxJQUFJLEVBQUUsS0FBSyxFQUFFLENBQUMsS0FBSyxFQUFFLEdBQUcsTUFBTSxDQUFDLENBQUM7aUJBQ2hELENBQUM7YUFDSDtZQUNELE9BQU8sTUFBTSxDQUFDO1FBQ2hCLENBQUMsRUFBRSxFQUFFLENBQWMsQ0FBQztLQUNyQjtJQUNELElBQUksK0RBQWdCLENBQUMsSUFBSSxDQUFDLEVBQUU7UUFDMUIsT0FBTyxNQUFNLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxDQUFDLE1BQU0sQ0FBQyxDQUFDLE1BQWlCLEVBQUUsR0FBVyxFQUFFLEVBQUU7WUFDakUsTUFBTSxJQUFJLEdBQUcsSUFBSSxDQUFDLEdBQUcsQ0FBQyxDQUFDO1lBQ3ZCLElBQ0UsSUFBSTtnQkFDSixPQUFPLElBQUksS0FBSyxRQUFRO2dCQUN4QixDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsS0FBSyxDQUFDLElBQUksY0FBYyxDQUFDLElBQUksRUFBRSxLQUFLLENBQUMsQ0FBQyxFQUNwRDtnQkFDQSxPQUFPO29CQUNMLEdBQUcsTUFBTTtvQkFDVCxDQUFDLEdBQUcsRUFBRSxHQUFHLE1BQU0sQ0FBQyxDQUFDLElBQUksQ0FBQyxHQUFHLENBQUM7b0JBQzFCLEdBQUcsV0FBVyxDQUFDLElBQUksRUFBRSxLQUFLLEVBQUUsQ0FBQyxHQUFHLEVBQUUsR0FBRyxNQUFNLENBQUMsQ0FBQztpQkFDOUMsQ0FBQzthQUNIO1lBQ0QsT0FBTyxNQUFNLENBQUM7UUFDaEIsQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDO0tBQ1I7SUFDRCxPQUFPLEVBQUUsQ0FBQztBQUNaLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvanNvbi1leHRlbnNpb24vc3JjL2NvbXBvbmVudC50c3giXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBqdXB5dGVySGlnaGxpZ2h0U3R5bGUgfSBmcm9tICdAanVweXRlcmxhYi9jb2RlbWlycm9yJztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBudWxsVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IElucHV0R3JvdXAgfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IFRhZywgdGFncyB9IGZyb20gJ0BsZXplci9oaWdobGlnaHQnO1xuaW1wb3J0IHsgSlNPTkFycmF5LCBKU09ORXh0LCBKU09OT2JqZWN0LCBKU09OVmFsdWUgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgKiBhcyBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQgSGlnaGxpZ2h0ZXIgZnJvbSAncmVhY3QtaGlnaGxpZ2h0LXdvcmRzJztcbmltcG9ydCB7IEpTT05UcmVlIH0gZnJvbSAncmVhY3QtanNvbi10cmVlJztcbmltcG9ydCB7IFN0eWxlTW9kdWxlIH0gZnJvbSAnc3R5bGUtbW9kJztcblxuLyoqXG4gKiBUaGUgcHJvcGVydGllcyBmb3IgdGhlIEpTT04gdHJlZSBjb21wb25lbnQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVByb3BzIHtcbiAgZGF0YTogTm9uTnVsbGFibGU8SlNPTlZhbHVlPjtcbiAgbWV0YWRhdGE/OiBKU09OT2JqZWN0O1xuXG4gIC8qKlxuICAgKiBUaGUgYXBwbGljYXRpb24gbGFuZ3VhZ2UgdHJhbnNsYXRvci5cbiAgICovXG4gIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvcjtcbiAgZm9yd2FyZGVkUmVmPzogUmVhY3QuUmVmPEhUTUxEaXZFbGVtZW50Pjtcbn1cblxuLyoqXG4gKiBUaGUgc3RhdGUgb2YgdGhlIEpTT04gdHJlZSBjb21wb25lbnQuXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVN0YXRlIHtcbiAgZmlsdGVyPzogc3RyaW5nO1xuICB2YWx1ZTogc3RyaW5nO1xufVxuXG4vKipcbiAqIEdldCB0aGUgQ29kZU1pcnJvciBzdHlsZSBmb3IgYSBnaXZlbiB0YWcuXG4gKi9cbmZ1bmN0aW9uIGdldFN0eWxlKHRhZzogVGFnKTogc3RyaW5nIHtcbiAgcmV0dXJuIGp1cHl0ZXJIaWdobGlnaHRTdHlsZS5zdHlsZShbdGFnXSkgPz8gJyc7XG59XG5cbi8qKlxuICogQSBjb21wb25lbnQgdGhhdCByZW5kZXJzIEpTT04gZGF0YSBhcyBhIGNvbGxhcHNpYmxlIHRyZWUuXG4gKi9cbmV4cG9ydCBjbGFzcyBDb21wb25lbnQgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQ8SVByb3BzLCBJU3RhdGU+IHtcbiAgc3RhdGUgPSB7IGZpbHRlcjogJycsIHZhbHVlOiAnJyB9O1xuXG4gIHRpbWVyOiBudW1iZXIgPSAwO1xuXG4gIGNvbXBvbmVudERpZE1vdW50KCk6IHZvaWQge1xuICAgIFN0eWxlTW9kdWxlLm1vdW50KGRvY3VtZW50LCBqdXB5dGVySGlnaGxpZ2h0U3R5bGUubW9kdWxlIGFzIFN0eWxlTW9kdWxlKTtcbiAgfVxuXG4gIGhhbmRsZUNoYW5nZSA9IChldmVudDogUmVhY3QuQ2hhbmdlRXZlbnQ8SFRNTElucHV0RWxlbWVudD4pOiB2b2lkID0+IHtcbiAgICBjb25zdCB7IHZhbHVlIH0gPSBldmVudC50YXJnZXQ7XG4gICAgdGhpcy5zZXRTdGF0ZSh7IHZhbHVlIH0pO1xuICAgIHdpbmRvdy5jbGVhclRpbWVvdXQodGhpcy50aW1lcik7XG4gICAgdGhpcy50aW1lciA9IHdpbmRvdy5zZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgIHRoaXMuc2V0U3RhdGUoeyBmaWx0ZXI6IHZhbHVlIH0pO1xuICAgIH0sIDMwMCk7XG4gIH07XG5cbiAgcmVuZGVyKCk6IEpTWC5FbGVtZW50IHtcbiAgICBjb25zdCB0cmFuc2xhdG9yID0gdGhpcy5wcm9wcy50cmFuc2xhdG9yIHx8IG51bGxUcmFuc2xhdG9yO1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICBjb25zdCB7IGRhdGEsIG1ldGFkYXRhLCBmb3J3YXJkZWRSZWYgfSA9IHRoaXMucHJvcHM7XG4gICAgY29uc3Qgcm9vdCA9IG1ldGFkYXRhICYmIG1ldGFkYXRhLnJvb3QgPyAobWV0YWRhdGEucm9vdCBhcyBzdHJpbmcpIDogJ3Jvb3QnO1xuICAgIGNvbnN0IGtleVBhdGhzID0gdGhpcy5zdGF0ZS5maWx0ZXJcbiAgICAgID8gZmlsdGVyUGF0aHMoZGF0YSwgdGhpcy5zdGF0ZS5maWx0ZXIsIFtyb290XSlcbiAgICAgIDogW3Jvb3RdO1xuICAgIHJldHVybiAoXG4gICAgICA8ZGl2IGNsYXNzTmFtZT1cImNvbnRhaW5lclwiIHJlZj17Zm9yd2FyZGVkUmVmfT5cbiAgICAgICAgPElucHV0R3JvdXBcbiAgICAgICAgICBjbGFzc05hbWU9XCJmaWx0ZXJcIlxuICAgICAgICAgIHR5cGU9XCJ0ZXh0XCJcbiAgICAgICAgICBwbGFjZWhvbGRlcj17dHJhbnMuX18oJ0ZpbHRlcuKApicpfVxuICAgICAgICAgIG9uQ2hhbmdlPXt0aGlzLmhhbmRsZUNoYW5nZX1cbiAgICAgICAgICB2YWx1ZT17dGhpcy5zdGF0ZS52YWx1ZX1cbiAgICAgICAgICByaWdodEljb249XCJ1aS1jb21wb25lbnRzOnNlYXJjaFwiXG4gICAgICAgIC8+XG4gICAgICAgIDxKU09OVHJlZVxuICAgICAgICAgIGRhdGE9e2RhdGF9XG4gICAgICAgICAgY29sbGVjdGlvbkxpbWl0PXsxMDB9XG4gICAgICAgICAgdGhlbWU9e3tcbiAgICAgICAgICAgIGV4dGVuZDogdGhlbWUsXG4gICAgICAgICAgICB2YWx1ZUxhYmVsOiBnZXRTdHlsZSh0YWdzLnZhcmlhYmxlTmFtZSksXG4gICAgICAgICAgICB2YWx1ZVRleHQ6IGdldFN0eWxlKHRhZ3Muc3RyaW5nKSxcbiAgICAgICAgICAgIG5lc3RlZE5vZGVJdGVtU3RyaW5nOiBnZXRTdHlsZSh0YWdzLmNvbW1lbnQpXG4gICAgICAgICAgfX1cbiAgICAgICAgICBpbnZlcnRUaGVtZT17ZmFsc2V9XG4gICAgICAgICAga2V5UGF0aD17W3Jvb3RdfVxuICAgICAgICAgIGdldEl0ZW1TdHJpbmc9eyh0eXBlLCBkYXRhLCBpdGVtVHlwZSwgaXRlbVN0cmluZykgPT5cbiAgICAgICAgICAgIEFycmF5LmlzQXJyYXkoZGF0YSkgPyAoXG4gICAgICAgICAgICAgIC8vIEFsd2F5cyBkaXNwbGF5IGFycmF5IHR5cGUgYW5kIHRoZSBudW1iZXIgb2YgaXRlbXMgaS5lLiBcIltdIDIgaXRlbXNcIi5cbiAgICAgICAgICAgICAgPHNwYW4+XG4gICAgICAgICAgICAgICAge2l0ZW1UeXBlfSB7aXRlbVN0cmluZ31cbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgKSA6IE9iamVjdC5rZXlzKGRhdGEgYXMgb2JqZWN0KS5sZW5ndGggPT09IDAgPyAoXG4gICAgICAgICAgICAgIC8vIE9ubHkgZGlzcGxheSBvYmplY3QgdHlwZSB3aGVuIGl0J3MgZW1wdHkgaS5lLiBcInt9XCIuXG4gICAgICAgICAgICAgIDxzcGFuPntpdGVtVHlwZX08L3NwYW4+XG4gICAgICAgICAgICApIDogKFxuICAgICAgICAgICAgICBudWxsISAvLyBVcHN0cmVhbSB0eXBpbmdzIGRvbid0IGFjY2VwdCBudWxsLCBidXQgaXQgc2hvdWxkIGJlIG9rXG4gICAgICAgICAgICApXG4gICAgICAgICAgfVxuICAgICAgICAgIGxhYmVsUmVuZGVyZXI9eyhbbGFiZWwsIHR5cGVdKSA9PiB7XG4gICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICA8c3BhbiBjbGFzc05hbWU9e2dldFN0eWxlKHRhZ3Mua2V5d29yZCl9PlxuICAgICAgICAgICAgICAgIDxIaWdobGlnaHRlclxuICAgICAgICAgICAgICAgICAgc2VhcmNoV29yZHM9e1t0aGlzLnN0YXRlLmZpbHRlcl19XG4gICAgICAgICAgICAgICAgICB0ZXh0VG9IaWdobGlnaHQ9e2Ake2xhYmVsfWB9XG4gICAgICAgICAgICAgICAgICBoaWdobGlnaHRDbGFzc05hbWU9XCJqcC1tb2Qtc2VsZWN0ZWRcIlxuICAgICAgICAgICAgICAgID48L0hpZ2hsaWdodGVyPlxuICAgICAgICAgICAgICA8L3NwYW4+XG4gICAgICAgICAgICApO1xuICAgICAgICAgIH19XG4gICAgICAgICAgdmFsdWVSZW5kZXJlcj17cmF3ID0+IHtcbiAgICAgICAgICAgIGxldCBjbGFzc05hbWUgPSBnZXRTdHlsZSh0YWdzLnN0cmluZyk7XG4gICAgICAgICAgICBpZiAodHlwZW9mIHJhdyA9PT0gJ251bWJlcicpIHtcbiAgICAgICAgICAgICAgY2xhc3NOYW1lID0gZ2V0U3R5bGUodGFncy5udW1iZXIpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgaWYgKHJhdyA9PT0gJ3RydWUnIHx8IHJhdyA9PT0gJ2ZhbHNlJykge1xuICAgICAgICAgICAgICBjbGFzc05hbWUgPSBnZXRTdHlsZSh0YWdzLmtleXdvcmQpO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgPHNwYW4gY2xhc3NOYW1lPXtjbGFzc05hbWV9PlxuICAgICAgICAgICAgICAgIDxIaWdobGlnaHRlclxuICAgICAgICAgICAgICAgICAgc2VhcmNoV29yZHM9e1t0aGlzLnN0YXRlLmZpbHRlcl19XG4gICAgICAgICAgICAgICAgICB0ZXh0VG9IaWdobGlnaHQ9e2Ake3Jhd31gfVxuICAgICAgICAgICAgICAgICAgaGlnaGxpZ2h0Q2xhc3NOYW1lPVwianAtbW9kLXNlbGVjdGVkXCJcbiAgICAgICAgICAgICAgICA+PC9IaWdobGlnaHRlcj5cbiAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgKTtcbiAgICAgICAgICB9fVxuICAgICAgICAgIHNob3VsZEV4cGFuZE5vZGVJbml0aWFsbHk9eyhrZXlQYXRoLCBkYXRhLCBsZXZlbCkgPT5cbiAgICAgICAgICAgIG1ldGFkYXRhICYmIG1ldGFkYXRhLmV4cGFuZGVkXG4gICAgICAgICAgICAgID8gdHJ1ZVxuICAgICAgICAgICAgICA6IGtleVBhdGhzLmpvaW4oJywnKS5pbmNsdWRlcyhrZXlQYXRoLmpvaW4oJywnKSlcbiAgICAgICAgICB9XG4gICAgICAgIC8+XG4gICAgICA8L2Rpdj5cbiAgICApO1xuICB9XG59XG5cbi8vIFByb3ZpZGUgYW4gaW52YWxpZCB0aGVtZSBvYmplY3QgKHRoaXMgaXMgb24gcHVycG9zZSEpIHRvIGludmFsaWRhdGUgdGhlXG4vLyByZWFjdC1qc29uLXRyZWUncyBpbmxpbmUgc3R5bGVzIHRoYXQgb3ZlcnJpZGUgQ29kZU1pcnJvciBDU1MgY2xhc3Nlc1xuY29uc3QgdGhlbWUgPSB7XG4gIHNjaGVtZTogJ2p1cHl0ZXInLFxuICBiYXNlMDA6ICdpbnZhbGlkJyxcbiAgYmFzZTAxOiAnaW52YWxpZCcsXG4gIGJhc2UwMjogJ2ludmFsaWQnLFxuICBiYXNlMDM6ICdpbnZhbGlkJyxcbiAgYmFzZTA0OiAnaW52YWxpZCcsXG4gIGJhc2UwNTogJ2ludmFsaWQnLFxuICBiYXNlMDY6ICdpbnZhbGlkJyxcbiAgYmFzZTA3OiAnaW52YWxpZCcsXG4gIGJhc2UwODogJ2ludmFsaWQnLFxuICBiYXNlMDk6ICdpbnZhbGlkJyxcbiAgYmFzZTBBOiAnaW52YWxpZCcsXG4gIGJhc2UwQjogJ2ludmFsaWQnLFxuICBiYXNlMEM6ICdpbnZhbGlkJyxcbiAgYmFzZTBEOiAnaW52YWxpZCcsXG4gIGJhc2UwRTogJ2ludmFsaWQnLFxuICBiYXNlMEY6ICdpbnZhbGlkJyxcbiAgYXV0aG9yOiAnaW52YWxpZCdcbn07XG5cbmZ1bmN0aW9uIG9iamVjdEluY2x1ZGVzKGRhdGE6IEpTT05WYWx1ZSwgcXVlcnk6IHN0cmluZyk6IGJvb2xlYW4ge1xuICByZXR1cm4gSlNPTi5zdHJpbmdpZnkoZGF0YSkuaW5jbHVkZXMocXVlcnkpO1xufVxuXG5mdW5jdGlvbiBmaWx0ZXJQYXRocyhcbiAgZGF0YTogTm9uTnVsbGFibGU8SlNPTlZhbHVlPixcbiAgcXVlcnk6IHN0cmluZyxcbiAgcGFyZW50OiBKU09OQXJyYXkgPSBbJ3Jvb3QnXVxuKTogSlNPTkFycmF5IHtcbiAgaWYgKEpTT05FeHQuaXNBcnJheShkYXRhKSkge1xuICAgIHJldHVybiBkYXRhLnJlZHVjZSgocmVzdWx0OiBKU09OQXJyYXksIGl0ZW06IEpTT05WYWx1ZSwgaW5kZXg6IG51bWJlcikgPT4ge1xuICAgICAgaWYgKGl0ZW0gJiYgdHlwZW9mIGl0ZW0gPT09ICdvYmplY3QnICYmIG9iamVjdEluY2x1ZGVzKGl0ZW0sIHF1ZXJ5KSkge1xuICAgICAgICByZXR1cm4gW1xuICAgICAgICAgIC4uLnJlc3VsdCxcbiAgICAgICAgICBbaW5kZXgsIC4uLnBhcmVudF0uam9pbignLCcpLFxuICAgICAgICAgIC4uLmZpbHRlclBhdGhzKGl0ZW0sIHF1ZXJ5LCBbaW5kZXgsIC4uLnBhcmVudF0pXG4gICAgICAgIF07XG4gICAgICB9XG4gICAgICByZXR1cm4gcmVzdWx0O1xuICAgIH0sIFtdKSBhcyBKU09OQXJyYXk7XG4gIH1cbiAgaWYgKEpTT05FeHQuaXNPYmplY3QoZGF0YSkpIHtcbiAgICByZXR1cm4gT2JqZWN0LmtleXMoZGF0YSkucmVkdWNlKChyZXN1bHQ6IEpTT05BcnJheSwga2V5OiBzdHJpbmcpID0+IHtcbiAgICAgIGNvbnN0IGl0ZW0gPSBkYXRhW2tleV07XG4gICAgICBpZiAoXG4gICAgICAgIGl0ZW0gJiZcbiAgICAgICAgdHlwZW9mIGl0ZW0gPT09ICdvYmplY3QnICYmXG4gICAgICAgIChrZXkuaW5jbHVkZXMocXVlcnkpIHx8IG9iamVjdEluY2x1ZGVzKGl0ZW0sIHF1ZXJ5KSlcbiAgICAgICkge1xuICAgICAgICByZXR1cm4gW1xuICAgICAgICAgIC4uLnJlc3VsdCxcbiAgICAgICAgICBba2V5LCAuLi5wYXJlbnRdLmpvaW4oJywnKSxcbiAgICAgICAgICAuLi5maWx0ZXJQYXRocyhpdGVtLCBxdWVyeSwgW2tleSwgLi4ucGFyZW50XSlcbiAgICAgICAgXTtcbiAgICAgIH1cbiAgICAgIHJldHVybiByZXN1bHQ7XG4gICAgfSwgW10pO1xuICB9XG4gIHJldHVybiBbXTtcbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==