"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_toc-extension_lib_index_js"],{

/***/ "../packages/toc-extension/lib/index.js":
/*!**********************************************!*\
  !*** ../packages/toc-extension/lib/index.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module toc-extension
 */





/**
 * A namespace for command IDs of table of contents plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.displayNumbering = 'toc:display-numbering';
    CommandIDs.displayH1Numbering = 'toc:display-h1-numbering';
    CommandIDs.displayOutputNumbering = 'toc:display-outputs-numbering';
    CommandIDs.showPanel = 'toc:show-panel';
    CommandIDs.toggleCollapse = 'toc:toggle-collapse';
})(CommandIDs || (CommandIDs = {}));
/**
 * Activates the ToC extension.
 *
 * @private
 * @param app - Jupyter application
 * @param tocRegistry - Table of contents registry
 * @param translator - translator
 * @param restorer - application layout restorer
 * @param labShell - Jupyter lab shell
 * @param settingRegistry - setting registry
 * @returns table of contents registry
 */
async function activateTOC(app, tocRegistry, translator, restorer, labShell, settingRegistry) {
    const trans = (translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator).load('jupyterlab');
    let configuration = { ..._jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContents.defaultConfig };
    // Create the ToC widget:
    const toc = new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsPanel(translator !== null && translator !== void 0 ? translator : undefined);
    toc.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.tocIcon;
    toc.title.caption = trans.__('Table of Contents');
    toc.id = 'table-of-contents';
    toc.node.setAttribute('role', 'region');
    toc.node.setAttribute('aria-label', trans.__('Table of Contents section'));
    app.commands.addCommand(CommandIDs.displayH1Numbering, {
        label: trans.__('Show first-level heading number'),
        execute: () => {
            if (toc.model) {
                toc.model.setConfiguration({
                    numberingH1: !toc.model.configuration.numberingH1
                });
            }
        },
        isEnabled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.supportedOptions.includes('numberingH1')) !== null && _b !== void 0 ? _b : false; },
        isToggled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.configuration.numberingH1) !== null && _b !== void 0 ? _b : false; }
    });
    app.commands.addCommand(CommandIDs.displayNumbering, {
        label: trans.__('Show heading number in the document'),
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.numberingIcon : undefined),
        execute: () => {
            if (toc.model) {
                toc.model.setConfiguration({
                    numberHeaders: !toc.model.configuration.numberHeaders
                });
                app.commands.notifyCommandChanged(CommandIDs.displayNumbering);
            }
        },
        isEnabled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.supportedOptions.includes('numberHeaders')) !== null && _b !== void 0 ? _b : false; },
        isToggled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.configuration.numberHeaders) !== null && _b !== void 0 ? _b : false; }
    });
    app.commands.addCommand(CommandIDs.displayOutputNumbering, {
        label: trans.__('Show output headings'),
        execute: () => {
            if (toc.model) {
                toc.model.setConfiguration({
                    includeOutput: !toc.model.configuration.includeOutput
                });
            }
        },
        isEnabled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.supportedOptions.includes('includeOutput')) !== null && _b !== void 0 ? _b : false; },
        isToggled: () => { var _a, _b; return (_b = (_a = toc.model) === null || _a === void 0 ? void 0 : _a.configuration.includeOutput) !== null && _b !== void 0 ? _b : false; }
    });
    app.commands.addCommand(CommandIDs.showPanel, {
        label: trans.__('Table of Contents'),
        execute: () => {
            app.shell.activateById(toc.id);
        }
    });
    function someExpanded(model) {
        return model.headings.some(h => { var _a; return !((_a = h.collapsed) !== null && _a !== void 0 ? _a : false); });
    }
    app.commands.addCommand(CommandIDs.toggleCollapse, {
        label: () => toc.model && !someExpanded(toc.model)
            ? trans.__('Expand All Headings')
            : trans.__('Collapse All Headings'),
        icon: args => args.toolbar
            ? toc.model && !someExpanded(toc.model)
                ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.expandAllIcon
                : _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.collapseAllIcon
            : undefined,
        execute: () => {
            if (toc.model) {
                if (someExpanded(toc.model)) {
                    toc.model.toggleCollapse({ collapsed: true });
                }
                else {
                    toc.model.toggleCollapse({ collapsed: false });
                }
            }
        },
        isEnabled: () => toc.model !== null
    });
    const tracker = new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsTracker();
    if (restorer) {
        // Add the ToC widget to the application restorer:
        restorer.add(toc, '@jupyterlab/toc:plugin');
    }
    // Attempt to load plugin settings:
    let settings;
    if (settingRegistry) {
        try {
            settings = await settingRegistry.load(registry.id);
            const updateSettings = (plugin) => {
                const composite = plugin.composite;
                for (const key of [...Object.keys(configuration)]) {
                    const value = composite[key];
                    if (value !== undefined) {
                        configuration[key] = value;
                    }
                }
                if (labShell) {
                    for (const widget of labShell.widgets('main')) {
                        const model = tracker.get(widget);
                        if (model) {
                            model.setConfiguration(configuration);
                        }
                    }
                }
                else {
                    if (app.shell.currentWidget) {
                        const model = tracker.get(app.shell.currentWidget);
                        if (model) {
                            model.setConfiguration(configuration);
                        }
                    }
                }
            };
            if (settings) {
                settings.changed.connect(updateSettings);
                updateSettings(settings);
            }
        }
        catch (error) {
            console.error(`Failed to load settings for the Table of Contents extension.\n\n${error}`);
        }
    }
    // Set up the panel toolbar
    const numbering = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.CommandToolbarButton({
        commands: app.commands,
        id: CommandIDs.displayNumbering,
        args: {
            toolbar: true
        },
        label: ''
    });
    numbering.addClass('jp-toc-numberingButton');
    toc.toolbar.addItem('display-numbering', numbering);
    toc.toolbar.addItem('spacer', _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.Toolbar.createSpacerItem());
    toc.toolbar.addItem('collapse-all', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.CommandToolbarButton({
        commands: app.commands,
        id: CommandIDs.toggleCollapse,
        args: {
            toolbar: true
        },
        label: ''
    }));
    const toolbarMenu = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.MenuSvg({ commands: app.commands });
    toolbarMenu.addItem({
        command: CommandIDs.displayH1Numbering
    });
    toolbarMenu.addItem({
        command: CommandIDs.displayOutputNumbering
    });
    const menuButton = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.ToolbarButton({
        tooltip: trans.__('More actions…'),
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.ellipsesIcon,
        actualOnClick: true,
        onClick: () => {
            const bbox = menuButton.node.getBoundingClientRect();
            toolbarMenu.open(bbox.x, bbox.bottom);
        }
    });
    toc.toolbar.addItem('submenu', menuButton);
    // Add the ToC to the left area:
    app.shell.add(toc, 'left', { rank: 400, type: 'Table of Contents' });
    // Update the ToC when the active widget changes:
    if (labShell) {
        labShell.currentChanged.connect(onConnect);
    }
    // Connect to current widget
    void app.restored.then(() => {
        onConnect();
    });
    return tracker;
    /**
     * Callback invoked when the active widget changes.
     *
     * @private
     */
    function onConnect() {
        var _a;
        let widget = app.shell.currentWidget;
        if (!widget) {
            return;
        }
        let model = tracker.get(widget);
        if (!model) {
            model = (_a = tocRegistry.getModel(widget, configuration)) !== null && _a !== void 0 ? _a : null;
            if (model) {
                tracker.add(widget, model);
            }
            widget.disposed.connect(() => {
                model === null || model === void 0 ? void 0 : model.dispose();
            });
        }
        if (toc.model) {
            toc.model.headingsChanged.disconnect(onCollapseChange);
            toc.model.collapseChanged.disconnect(onCollapseChange);
        }
        toc.model = model;
        if (toc.model) {
            toc.model.headingsChanged.connect(onCollapseChange);
            toc.model.collapseChanged.connect(onCollapseChange);
        }
        setToolbarButtonsState();
    }
    function setToolbarButtonsState() {
        app.commands.notifyCommandChanged(CommandIDs.displayNumbering);
        app.commands.notifyCommandChanged(CommandIDs.toggleCollapse);
    }
    function onCollapseChange() {
        app.commands.notifyCommandChanged(CommandIDs.toggleCollapse);
    }
}
/**
 * Table of contents registry plugin.
 */
const registry = {
    id: '@jupyterlab/toc-extension:registry',
    description: 'Provides the table of contents registry.',
    autoStart: true,
    provides: _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.ITableOfContentsRegistry,
    activate: () => {
        // Create the ToC registry
        return new _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.TableOfContentsRegistry();
    }
};
/**
 * Table of contents tracker plugin.
 */
const tracker = {
    id: '@jupyterlab/toc-extension:tracker',
    description: 'Adds the table of content widget and provides its tracker.',
    autoStart: true,
    provides: _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.ITableOfContentsTracker,
    requires: [_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_2__.ITableOfContentsRegistry],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry],
    activate: activateTOC
};
/**
 * Exports.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([registry, tracker]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdG9jLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuMzA3ZWY1OGE0NTIyMjk2N2E1M2YuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBQzNEOzs7R0FHRztBQU84QjtBQUM4QjtBQVF0QztBQUM2QztBQVduQztBQUVuQzs7R0FFRztBQUNILElBQVUsVUFBVSxDQVVuQjtBQVZELFdBQVUsVUFBVTtJQUNMLDJCQUFnQixHQUFHLHVCQUF1QixDQUFDO0lBRTNDLDZCQUFrQixHQUFHLDBCQUEwQixDQUFDO0lBRWhELGlDQUFzQixHQUFHLCtCQUErQixDQUFDO0lBRXpELG9CQUFTLEdBQUcsZ0JBQWdCLENBQUM7SUFFN0IseUJBQWMsR0FBRyxxQkFBcUIsQ0FBQztBQUN0RCxDQUFDLEVBVlMsVUFBVSxLQUFWLFVBQVUsUUFVbkI7QUFFRDs7Ozs7Ozs7Ozs7R0FXRztBQUNILEtBQUssVUFBVSxXQUFXLENBQ3hCLEdBQW9CLEVBQ3BCLFdBQXFDLEVBQ3JDLFVBQStCLEVBQy9CLFFBQWlDLEVBQ2pDLFFBQTJCLEVBQzNCLGVBQXlDO0lBRXpDLE1BQU0sS0FBSyxHQUFHLENBQUMsVUFBVSxhQUFWLFVBQVUsY0FBVixVQUFVLEdBQUksbUVBQWMsQ0FBQyxDQUFDLElBQUksQ0FBQyxZQUFZLENBQUMsQ0FBQztJQUNoRSxJQUFJLGFBQWEsR0FBRyxFQUFFLEdBQUcsMEVBQTZCLEVBQUUsQ0FBQztJQUV6RCx5QkFBeUI7SUFDekIsTUFBTSxHQUFHLEdBQUcsSUFBSSxpRUFBb0IsQ0FBQyxVQUFVLGFBQVYsVUFBVSxjQUFWLFVBQVUsR0FBSSxTQUFTLENBQUMsQ0FBQztJQUM5RCxHQUFHLENBQUMsS0FBSyxDQUFDLElBQUksR0FBRyw4REFBTyxDQUFDO0lBQ3pCLEdBQUcsQ0FBQyxLQUFLLENBQUMsT0FBTyxHQUFHLEtBQUssQ0FBQyxFQUFFLENBQUMsbUJBQW1CLENBQUMsQ0FBQztJQUNsRCxHQUFH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LFdBQVc7Q0FDdEIsQ0FBQztBQUVGOztHQUVHO0FBQ0gsaUVBQWUsQ0FBQyxRQUFRLEVBQUUsT0FBTyxDQUFDLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdG9jLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgdG9jLWV4dGVuc2lvblxuICovXG5cbmltcG9ydCB7XG4gIElMYWJTaGVsbCxcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmQsXG4gIEp1cHl0ZXJGcm9udEVuZFBsdWdpblxufSBmcm9tICdAanVweXRlcmxhYi9hcHBsaWNhdGlvbic7XG5pbXBvcnQgeyBJU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElUYWJsZU9mQ29udGVudHNSZWdpc3RyeSxcbiAgSVRhYmxlT2ZDb250ZW50c1RyYWNrZXIsXG4gIFRhYmxlT2ZDb250ZW50cyxcbiAgVGFibGVPZkNvbnRlbnRzUGFuZWwsXG4gIFRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5LFxuICBUYWJsZU9mQ29udGVudHNUcmFja2VyXG59IGZyb20gJ0BqdXB5dGVybGFiL3RvYyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBjb2xsYXBzZUFsbEljb24sXG4gIENvbW1hbmRUb29sYmFyQnV0dG9uLFxuICBlbGxpcHNlc0ljb24sXG4gIGV4cGFuZEFsbEljb24sXG4gIE1lbnVTdmcsXG4gIG51bWJlcmluZ0ljb24sXG4gIHRvY0ljb24sXG4gIFRvb2xiYXIsXG4gIFRvb2xiYXJCdXR0b25cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIGNvbW1hbmQgSURzIG9mIHRhYmxlIG9mIGNvbnRlbnRzIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3QgZGlzcGxheU51bWJlcmluZyA9ICd0b2M6ZGlzcGxheS1udW1iZXJpbmcnO1xuXG4gIGV4cG9ydCBjb25zdCBkaXNwbGF5SDFOdW1iZXJpbmcgPSAndG9jOmRpc3BsYXktaDEtbnVtYmVyaW5nJztcblxuICBleHBvcnQgY29uc3QgZGlzcGxheU91dHB1dE51bWJlcmluZyA9ICd0b2M6ZGlzcGxheS1vdXRwdXRzLW51bWJlcmluZyc7XG5cbiAgZXhwb3J0IGNvbnN0IHNob3dQYW5lbCA9ICd0b2M6c2hvdy1wYW5lbCc7XG5cbiAgZXhwb3J0IGNvbnN0IHRvZ2dsZUNvbGxhcHNlID0gJ3RvYzp0b2dnbGUtY29sbGFwc2UnO1xufVxuXG4vKipcbiAqIEFjdGl2YXRlcyB0aGUgVG9DIGV4dGVuc2lvbi5cbiAqXG4gKiBAcHJpdmF0ZVxuICogQHBhcmFtIGFwcCAtIEp1cHl0ZXIgYXBwbGljYXRpb25cbiAqIEBwYXJhbSB0b2NSZWdpc3RyeSAtIFRhYmxlIG9mIGNvbnRlbnRzIHJlZ2lzdHJ5XG4gKiBAcGFyYW0gdHJhbnNsYXRvciAtIHRyYW5zbGF0b3JcbiAqIEBwYXJhbSByZXN0b3JlciAtIGFwcGxpY2F0aW9uIGxheW91dCByZXN0b3JlclxuICogQHBhcmFtIGxhYlNoZWxsIC0gSnVweXRlciBsYWIgc2hlbGxcbiAqIEBwYXJhbSBzZXR0aW5nUmVnaXN0cnkgLSBzZXR0aW5nIHJlZ2lzdHJ5XG4gKiBAcmV0dXJucyB0YWJsZSBvZiBjb250ZW50cyByZWdpc3RyeVxuICovXG5hc3luYyBmdW5jdGlvbiBhY3RpdmF0ZVRPQyhcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHRvY1JlZ2lzdHJ5OiBJVGFibGVPZkNvbnRlbnRzUmVnaXN0cnksXG4gIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvciB8IG51bGwsXG4gIHJlc3RvcmVyPzogSUxheW91dFJlc3RvcmVyIHwgbnVsbCxcbiAgbGFiU2hlbGw/OiBJTGFiU2hlbGwgfCBudWxsLFxuICBzZXR0aW5nUmVnaXN0cnk/OiBJU2V0dGluZ1JlZ2lzdHJ5IHwgbnVsbFxuKTogUHJvbWlzZTxJVGFibGVPZkNvbnRlbnRzVHJhY2tlcj4ge1xuICBjb25zdCB0cmFucyA9ICh0cmFuc2xhdG9yID8/IG51bGxUcmFuc2xhdG9yKS5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGxldCBjb25maWd1cmF0aW9uID0geyAuLi5UYWJsZU9mQ29udGVudHMuZGVmYXVsdENvbmZpZyB9O1xuXG4gIC8vIENyZWF0ZSB0aGUgVG9DIHdpZGdldDpcbiAgY29uc3QgdG9jID0gbmV3IFRhYmxlT2ZDb250ZW50c1BhbmVsKHRyYW5zbGF0b3IgPz8gdW5kZWZpbmVkKTtcbiAgdG9jLnRpdGxlLmljb24gPSB0b2NJY29uO1xuICB0b2MudGl0bGUuY2FwdGlvbiA9IHRyYW5zLl9fKCdUYWJsZSBvZiBDb250ZW50cycpO1xuICB0b2MuaWQgPSAndGFibGUtb2YtY29udGVudHMnO1xuICB0b2Mubm9kZS5zZXRBdHRyaWJ1dGUoJ3JvbGUnLCAncmVnaW9uJyk7XG4gIHRvYy5ub2RlLnNldEF0dHJpYnV0ZSgnYXJpYS1sYWJlbCcsIHRyYW5zLl9fKCdUYWJsZSBvZiBDb250ZW50cyBzZWN0aW9uJykpO1xuXG4gIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuZGlzcGxheUgxTnVtYmVyaW5nLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdTaG93IGZpcnN0LWxldmVsIGhlYWRpbmcgbnVtYmVyJyksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgaWYgKHRvYy5tb2RlbCkge1xuICAgICAgICB0b2MubW9kZWwuc2V0Q29uZmlndXJhdGlvbih7XG4gICAgICAgICAgbnVtYmVyaW5nSDE6ICF0b2MubW9kZWwuY29uZmlndXJhdGlvbi5udW1iZXJpbmdIMVxuICAgICAgICB9KTtcbiAgICAgIH1cbiAgICB9LFxuICAgIGlzRW5hYmxlZDogKCkgPT5cbiAgICAgIHRvYy5tb2RlbD8uc3VwcG9ydGVkT3B0aW9ucy5pbmNsdWRlcygnbnVtYmVyaW5nSDEnKSA/PyBmYWxzZSxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+IHRvYy5tb2RlbD8uY29uZmlndXJhdGlvbi5udW1iZXJpbmdIMSA/PyBmYWxzZVxuICB9KTtcblxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRpc3BsYXlOdW1iZXJpbmcsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgaGVhZGluZyBudW1iZXIgaW4gdGhlIGRvY3VtZW50JyksXG4gICAgaWNvbjogYXJncyA9PiAoYXJncy50b29sYmFyID8gbnVtYmVyaW5nSWNvbiA6IHVuZGVmaW5lZCksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgaWYgKHRvYy5tb2RlbCkge1xuICAgICAgICB0b2MubW9kZWwuc2V0Q29uZmlndXJhdGlvbih7XG4gICAgICAgICAgbnVtYmVySGVhZGVyczogIXRvYy5tb2RlbC5jb25maWd1cmF0aW9uLm51bWJlckhlYWRlcnNcbiAgICAgICAgfSk7XG4gICAgICAgIGFwcC5jb21tYW5kcy5ub3RpZnlDb21tYW5kQ2hhbmdlZChDb21tYW5kSURzLmRpc3BsYXlOdW1iZXJpbmcpO1xuICAgICAgfVxuICAgIH0sXG4gICAgaXNFbmFibGVkOiAoKSA9PlxuICAgICAgdG9jLm1vZGVsPy5zdXBwb3J0ZWRPcHRpb25zLmluY2x1ZGVzKCdudW1iZXJIZWFkZXJzJykgPz8gZmFsc2UsXG4gICAgaXNUb2dnbGVkOiAoKSA9PiB0b2MubW9kZWw/LmNvbmZpZ3VyYXRpb24ubnVtYmVySGVhZGVycyA/PyBmYWxzZVxuICB9KTtcblxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLmRpc3BsYXlPdXRwdXROdW1iZXJpbmcsIHtcbiAgICBsYWJlbDogdHJhbnMuX18oJ1Nob3cgb3V0cHV0IGhlYWRpbmdzJyksXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgaWYgKHRvYy5tb2RlbCkge1xuICAgICAgICB0b2MubW9kZWwuc2V0Q29uZmlndXJhdGlvbih7XG4gICAgICAgICAgaW5jbHVkZU91dHB1dDogIXRvYy5tb2RlbC5jb25maWd1cmF0aW9uLmluY2x1ZGVPdXRwdXRcbiAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSxcbiAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICB0b2MubW9kZWw/LnN1cHBvcnRlZE9wdGlvbnMuaW5jbHVkZXMoJ2luY2x1ZGVPdXRwdXQnKSA/PyBmYWxzZSxcbiAgICBpc1RvZ2dsZWQ6ICgpID0+IHRvYy5tb2RlbD8uY29uZmlndXJhdGlvbi5pbmNsdWRlT3V0cHV0ID8/IGZhbHNlXG4gIH0pO1xuXG4gIGFwcC5jb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuc2hvd1BhbmVsLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdUYWJsZSBvZiBDb250ZW50cycpLFxuICAgIGV4ZWN1dGU6ICgpID0+IHtcbiAgICAgIGFwcC5zaGVsbC5hY3RpdmF0ZUJ5SWQodG9jLmlkKTtcbiAgICB9XG4gIH0pO1xuXG4gIGZ1bmN0aW9uIHNvbWVFeHBhbmRlZChtb2RlbDogVGFibGVPZkNvbnRlbnRzLk1vZGVsKTogYm9vbGVhbiB7XG4gICAgcmV0dXJuIG1vZGVsLmhlYWRpbmdzLnNvbWUoaCA9PiAhKGguY29sbGFwc2VkID8/IGZhbHNlKSk7XG4gIH1cblxuICBhcHAuY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnRvZ2dsZUNvbGxhcHNlLCB7XG4gICAgbGFiZWw6ICgpID0+XG4gICAgICB0b2MubW9kZWwgJiYgIXNvbWVFeHBhbmRlZCh0b2MubW9kZWwpXG4gICAgICAgID8gdHJhbnMuX18oJ0V4cGFuZCBBbGwgSGVhZGluZ3MnKVxuICAgICAgICA6IHRyYW5zLl9fKCdDb2xsYXBzZSBBbGwgSGVhZGluZ3MnKSxcbiAgICBpY29uOiBhcmdzID0+XG4gICAgICBhcmdzLnRvb2xiYXJcbiAgICAgICAgPyB0b2MubW9kZWwgJiYgIXNvbWVFeHBhbmRlZCh0b2MubW9kZWwpXG4gICAgICAgICAgPyBleHBhbmRBbGxJY29uXG4gICAgICAgICAgOiBjb2xsYXBzZUFsbEljb25cbiAgICAgICAgOiB1bmRlZmluZWQsXG4gICAgZXhlY3V0ZTogKCkgPT4ge1xuICAgICAgaWYgKHRvYy5tb2RlbCkge1xuICAgICAgICBpZiAoc29tZUV4cGFuZGVkKHRvYy5tb2RlbCkpIHtcbiAgICAgICAgICB0b2MubW9kZWwudG9nZ2xlQ29sbGFwc2UoeyBjb2xsYXBzZWQ6IHRydWUgfSk7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgdG9jLm1vZGVsLnRvZ2dsZUNvbGxhcHNlKHsgY29sbGFwc2VkOiBmYWxzZSB9KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0sXG4gICAgaXNFbmFibGVkOiAoKSA9PiB0b2MubW9kZWwgIT09IG51bGxcbiAgfSk7XG5cbiAgY29uc3QgdHJhY2tlciA9IG5ldyBUYWJsZU9mQ29udGVudHNUcmFja2VyKCk7XG5cbiAgaWYgKHJlc3RvcmVyKSB7XG4gICAgLy8gQWRkIHRoZSBUb0Mgd2lkZ2V0IHRvIHRoZSBhcHBsaWNhdGlvbiByZXN0b3JlcjpcbiAgICByZXN0b3Jlci5hZGQodG9jLCAnQGp1cHl0ZXJsYWIvdG9jOnBsdWdpbicpO1xuICB9XG5cbiAgLy8gQXR0ZW1wdCB0byBsb2FkIHBsdWdpbiBzZXR0aW5nczpcbiAgbGV0IHNldHRpbmdzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyB8IHVuZGVmaW5lZDtcbiAgaWYgKHNldHRpbmdSZWdpc3RyeSkge1xuICAgIHRyeSB7XG4gICAgICBzZXR0aW5ncyA9IGF3YWl0IHNldHRpbmdSZWdpc3RyeS5sb2FkKHJlZ2lzdHJ5LmlkKTtcbiAgICAgIGNvbnN0IHVwZGF0ZVNldHRpbmdzID0gKHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JU2V0dGluZ3MpID0+IHtcbiAgICAgICAgY29uc3QgY29tcG9zaXRlID0gcGx1Z2luLmNvbXBvc2l0ZTtcbiAgICAgICAgZm9yIChjb25zdCBrZXkgb2YgWy4uLk9iamVjdC5rZXlzKGNvbmZpZ3VyYXRpb24pXSkge1xuICAgICAgICAgIGNvbnN0IHZhbHVlID0gY29tcG9zaXRlW2tleV0gYXMgYW55O1xuICAgICAgICAgIGlmICh2YWx1ZSAhPT0gdW5kZWZpbmVkKSB7XG4gICAgICAgICAgICBjb25maWd1cmF0aW9uW2tleV0gPSB2YWx1ZTtcbiAgICAgICAgICB9XG4gICAgICAgIH1cblxuICAgICAgICBpZiAobGFiU2hlbGwpIHtcbiAgICAgICAgICBmb3IgKGNvbnN0IHdpZGdldCBvZiBsYWJTaGVsbC53aWRnZXRzKCdtYWluJykpIHtcbiAgICAgICAgICAgIGNvbnN0IG1vZGVsID0gdHJhY2tlci5nZXQod2lkZ2V0KTtcbiAgICAgICAgICAgIGlmIChtb2RlbCkge1xuICAgICAgICAgICAgICBtb2RlbC5zZXRDb25maWd1cmF0aW9uKGNvbmZpZ3VyYXRpb24pO1xuICAgICAgICAgICAgfVxuICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICBpZiAoYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQpIHtcbiAgICAgICAgICAgIGNvbnN0IG1vZGVsID0gdHJhY2tlci5nZXQoYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQpO1xuICAgICAgICAgICAgaWYgKG1vZGVsKSB7XG4gICAgICAgICAgICAgIG1vZGVsLnNldENvbmZpZ3VyYXRpb24oY29uZmlndXJhdGlvbik7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICB9O1xuICAgICAgaWYgKHNldHRpbmdzKSB7XG4gICAgICAgIHNldHRpbmdzLmNoYW5nZWQuY29ubmVjdCh1cGRhdGVTZXR0aW5ncyk7XG4gICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgIH1cbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgYEZhaWxlZCB0byBsb2FkIHNldHRpbmdzIGZvciB0aGUgVGFibGUgb2YgQ29udGVudHMgZXh0ZW5zaW9uLlxcblxcbiR7ZXJyb3J9YFxuICAgICAgKTtcbiAgICB9XG4gIH1cblxuICAvLyBTZXQgdXAgdGhlIHBhbmVsIHRvb2xiYXJcbiAgY29uc3QgbnVtYmVyaW5nID0gbmV3IENvbW1hbmRUb29sYmFyQnV0dG9uKHtcbiAgICBjb21tYW5kczogYXBwLmNvbW1hbmRzLFxuICAgIGlkOiBDb21tYW5kSURzLmRpc3BsYXlOdW1iZXJpbmcsXG4gICAgYXJnczoge1xuICAgICAgdG9vbGJhcjogdHJ1ZVxuICAgIH0sXG4gICAgbGFiZWw6ICcnXG4gIH0pO1xuICBudW1iZXJpbmcuYWRkQ2xhc3MoJ2pwLXRvYy1udW1iZXJpbmdCdXR0b24nKTtcbiAgdG9jLnRvb2xiYXIuYWRkSXRlbSgnZGlzcGxheS1udW1iZXJpbmcnLCBudW1iZXJpbmcpO1xuXG4gIHRvYy50b29sYmFyLmFkZEl0ZW0oJ3NwYWNlcicsIFRvb2xiYXIuY3JlYXRlU3BhY2VySXRlbSgpKTtcblxuICB0b2MudG9vbGJhci5hZGRJdGVtKFxuICAgICdjb2xsYXBzZS1hbGwnLFxuICAgIG5ldyBDb21tYW5kVG9vbGJhckJ1dHRvbih7XG4gICAgICBjb21tYW5kczogYXBwLmNvbW1hbmRzLFxuICAgICAgaWQ6IENvbW1hbmRJRHMudG9nZ2xlQ29sbGFwc2UsXG4gICAgICBhcmdzOiB7XG4gICAgICAgIHRvb2xiYXI6IHRydWVcbiAgICAgIH0sXG4gICAgICBsYWJlbDogJydcbiAgICB9KVxuICApO1xuXG4gIGNvbnN0IHRvb2xiYXJNZW51ID0gbmV3IE1lbnVTdmcoeyBjb21tYW5kczogYXBwLmNvbW1hbmRzIH0pO1xuICB0b29sYmFyTWVudS5hZGRJdGVtKHtcbiAgICBjb21tYW5kOiBDb21tYW5kSURzLmRpc3BsYXlIMU51bWJlcmluZ1xuICB9KTtcbiAgdG9vbGJhck1lbnUuYWRkSXRlbSh7XG4gICAgY29tbWFuZDogQ29tbWFuZElEcy5kaXNwbGF5T3V0cHV0TnVtYmVyaW5nXG4gIH0pO1xuICBjb25zdCBtZW51QnV0dG9uID0gbmV3IFRvb2xiYXJCdXR0b24oe1xuICAgIHRvb2x0aXA6IHRyYW5zLl9fKCdNb3JlIGFjdGlvbnPigKYnKSxcbiAgICBpY29uOiBlbGxpcHNlc0ljb24sXG4gICAgYWN0dWFsT25DbGljazogdHJ1ZSxcbiAgICBvbkNsaWNrOiAoKSA9PiB7XG4gICAgICBjb25zdCBiYm94ID0gbWVudUJ1dHRvbi5ub2RlLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpO1xuICAgICAgdG9vbGJhck1lbnUub3BlbihiYm94LngsIGJib3guYm90dG9tKTtcbiAgICB9XG4gIH0pO1xuICB0b2MudG9vbGJhci5hZGRJdGVtKCdzdWJtZW51JywgbWVudUJ1dHRvbik7XG5cbiAgLy8gQWRkIHRoZSBUb0MgdG8gdGhlIGxlZnQgYXJlYTpcbiAgYXBwLnNoZWxsLmFkZCh0b2MsICdsZWZ0JywgeyByYW5rOiA0MDAsIHR5cGU6ICdUYWJsZSBvZiBDb250ZW50cycgfSk7XG5cbiAgLy8gVXBkYXRlIHRoZSBUb0Mgd2hlbiB0aGUgYWN0aXZlIHdpZGdldCBjaGFuZ2VzOlxuICBpZiAobGFiU2hlbGwpIHtcbiAgICBsYWJTaGVsbC5jdXJyZW50Q2hhbmdlZC5jb25uZWN0KG9uQ29ubmVjdCk7XG4gIH1cblxuICAvLyBDb25uZWN0IHRvIGN1cnJlbnQgd2lkZ2V0XG4gIHZvaWQgYXBwLnJlc3RvcmVkLnRoZW4oKCkgPT4ge1xuICAgIG9uQ29ubmVjdCgpO1xuICB9KTtcblxuICByZXR1cm4gdHJhY2tlcjtcblxuICAvKipcbiAgICogQ2FsbGJhY2sgaW52b2tlZCB3aGVuIHRoZSBhY3RpdmUgd2lkZ2V0IGNoYW5nZXMuXG4gICAqXG4gICAqIEBwcml2YXRlXG4gICAqL1xuICBmdW5jdGlvbiBvbkNvbm5lY3QoKSB7XG4gICAgbGV0IHdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuICAgIGxldCBtb2RlbCA9IHRyYWNrZXIuZ2V0KHdpZGdldCk7XG4gICAgaWYgKCFtb2RlbCkge1xuICAgICAgbW9kZWwgPSB0b2NSZWdpc3RyeS5nZXRNb2RlbCh3aWRnZXQsIGNvbmZpZ3VyYXRpb24pID8/IG51bGw7XG4gICAgICBpZiAobW9kZWwpIHtcbiAgICAgICAgdHJhY2tlci5hZGQod2lkZ2V0LCBtb2RlbCk7XG4gICAgICB9XG5cbiAgICAgIHdpZGdldC5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgbW9kZWw/LmRpc3Bvc2UoKTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIGlmICh0b2MubW9kZWwpIHtcbiAgICAgIHRvYy5tb2RlbC5oZWFkaW5nc0NoYW5nZWQuZGlzY29ubmVjdChvbkNvbGxhcHNlQ2hhbmdlKTtcbiAgICAgIHRvYy5tb2RlbC5jb2xsYXBzZUNoYW5nZWQuZGlzY29ubmVjdChvbkNvbGxhcHNlQ2hhbmdlKTtcbiAgICB9XG5cbiAgICB0b2MubW9kZWwgPSBtb2RlbDtcbiAgICBpZiAodG9jLm1vZGVsKSB7XG4gICAgICB0b2MubW9kZWwuaGVhZGluZ3NDaGFuZ2VkLmNvbm5lY3Qob25Db2xsYXBzZUNoYW5nZSk7XG4gICAgICB0b2MubW9kZWwuY29sbGFwc2VDaGFuZ2VkLmNvbm5lY3Qob25Db2xsYXBzZUNoYW5nZSk7XG4gICAgfVxuICAgIHNldFRvb2xiYXJCdXR0b25zU3RhdGUoKTtcbiAgfVxuXG4gIGZ1bmN0aW9uIHNldFRvb2xiYXJCdXR0b25zU3RhdGUoKSB7XG4gICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMuZGlzcGxheU51bWJlcmluZyk7XG4gICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKENvbW1hbmRJRHMudG9nZ2xlQ29sbGFwc2UpO1xuICB9XG5cbiAgZnVuY3Rpb24gb25Db2xsYXBzZUNoYW5nZSgpIHtcbiAgICBhcHAuY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoQ29tbWFuZElEcy50b2dnbGVDb2xsYXBzZSk7XG4gIH1cbn1cblxuLyoqXG4gKiBUYWJsZSBvZiBjb250ZW50cyByZWdpc3RyeSBwbHVnaW4uXG4gKi9cbmNvbnN0IHJlZ2lzdHJ5OiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48SVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi90b2MtZXh0ZW5zaW9uOnJlZ2lzdHJ5JyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgdGFibGUgb2YgY29udGVudHMgcmVnaXN0cnkuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5LFxuICBhY3RpdmF0ZTogKCk6IElUYWJsZU9mQ29udGVudHNSZWdpc3RyeSA9PiB7XG4gICAgLy8gQ3JlYXRlIHRoZSBUb0MgcmVnaXN0cnlcbiAgICByZXR1cm4gbmV3IFRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5KCk7XG4gIH1cbn07XG5cbi8qKlxuICogVGFibGUgb2YgY29udGVudHMgdHJhY2tlciBwbHVnaW4uXG4gKi9cbmNvbnN0IHRyYWNrZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJVGFibGVPZkNvbnRlbnRzVHJhY2tlcj4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvdG9jLWV4dGVuc2lvbjp0cmFja2VyJyxcbiAgZGVzY3JpcHRpb246ICdBZGRzIHRoZSB0YWJsZSBvZiBjb250ZW50IHdpZGdldCBhbmQgcHJvdmlkZXMgaXRzIHRyYWNrZXIuJyxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBwcm92aWRlczogSVRhYmxlT2ZDb250ZW50c1RyYWNrZXIsXG4gIHJlcXVpcmVzOiBbSVRhYmxlT2ZDb250ZW50c1JlZ2lzdHJ5XSxcbiAgb3B0aW9uYWw6IFtJVHJhbnNsYXRvciwgSUxheW91dFJlc3RvcmVyLCBJTGFiU2hlbGwsIElTZXR0aW5nUmVnaXN0cnldLFxuICBhY3RpdmF0ZTogYWN0aXZhdGVUT0Ncbn07XG5cbi8qKlxuICogRXhwb3J0cy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgW3JlZ2lzdHJ5LCB0cmFja2VyXTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==