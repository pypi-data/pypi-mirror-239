"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_pluginmanager-extension_lib_index_js-_b3011"],{

/***/ "../packages/pluginmanager-extension/lib/index.js":
/*!********************************************************!*\
  !*** ../packages/pluginmanager-extension/lib/index.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/pluginmanager */ "webpack/sharing/consume/default/@jupyterlab/pluginmanager/@jupyterlab/pluginmanager");
/* harmony import */ var _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module pluginmanager-extension
 */





/**
 * The command IDs used by the pluginmanager plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'pluginmanager:open';
    CommandIDs.refreshPlugins = 'pluginmanager:refresh';
})(CommandIDs || (CommandIDs = {}));
const PLUGIN_ID = '@jupyterlab/pluginmanager-extension:plugin';
/**
 * A plugin for managing status of other plugins.
 */
const pluginmanager = {
    id: PLUGIN_ID,
    description: 'Enable or disable individual plugins.',
    autoStart: true,
    requires: [],
    optional: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.ITranslator, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__.IPluginManager,
    activate: (app, translator, palette, restorer) => {
        const { commands, shell } = app;
        translator = translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator;
        const trans = translator.load('jupyterlab');
        // Translation strings.
        const category = trans.__('Plugin Manager');
        const widgetLabel = trans.__('Advanced Plugin Manager');
        const refreshPlugins = trans.__('Refresh Plugin List');
        const namespace = 'plugin-manager';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
            namespace: namespace
        });
        /**
         * Create a MainAreaWidget for Plugin Manager.
         */
        function createWidget(args) {
            const model = new _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__.PluginListModel({
                ...args,
                pluginData: {
                    availablePlugins: app.info.availablePlugins
                },
                serverSettings: app.serviceManager.serverSettings,
                extraLockedPlugins: [
                    PLUGIN_ID,
                    // UI will not proceed beyond splash without `layout` plugin
                    '@jupyterlab/application-extension:layout',
                    // State restoration does not work well without resolver,
                    // can leave user locked out of the plugin manager
                    // (if command palette and menu are disabled too)
                    '@jupyterlab/apputils-extension:resolver'
                ],
                translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator
            });
            const content = new _jupyterlab_pluginmanager__WEBPACK_IMPORTED_MODULE_4__.Plugins({
                model,
                translator: translator !== null && translator !== void 0 ? translator : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator
            });
            content.title.label = widgetLabel;
            content.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.extensionIcon;
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content, reveal: model.ready });
            main.toolbar.addItem('refresh-plugins', new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.CommandToolbarButton({
                id: CommandIDs.refreshPlugins,
                args: { noLabel: true },
                commands
            }));
            return main;
        }
        // Register commands.
        commands.addCommand(CommandIDs.open, {
            label: widgetLabel,
            execute: args => {
                const main = createWidget(args);
                shell.add(main, 'main', { type: 'Plugins' });
                // add to tracker so it can be restored, and update when choices change
                void tracker.add(main);
                main.content.model.trackerDataChanged.connect(() => {
                    void tracker.save(main);
                });
                return main;
            }
        });
        commands.addCommand(CommandIDs.refreshPlugins, {
            label: args => (args.noLabel ? '' : refreshPlugins),
            caption: trans.__('Refresh plugins list'),
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.refreshIcon,
            execute: async () => {
                var _a;
                return (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.model.refresh().catch((reason) => {
                    console.error(`Failed to refresh the available plugins list:\n${reason}`);
                });
            }
        });
        if (palette) {
            palette.addItem({ command: CommandIDs.open, category });
        }
        if (restorer) {
            void restorer.restore(tracker, {
                command: CommandIDs.open,
                name: _ => 'plugins',
                args: widget => {
                    const { query, isDisclaimed } = widget.content.model;
                    const args = {
                        query,
                        isDisclaimed
                    };
                    return args;
                }
            });
        }
        return {
            open: () => {
                return app.commands.execute(CommandIDs.open);
            }
        };
    }
};
const plugins = [pluginmanager];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfcGx1Z2lubWFuYWdlci1leHRlbnNpb25fbGliX2luZGV4X2pzLV9iMzAxMS40ZDU2ZmNjZGVmZDM4MDNiZDhiNS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQUs4QjtBQUtIO0FBQ3dDO0FBS25DO0FBTUE7QUFFbkM7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FJbkI7QUFKRCxXQUFVLFVBQVU7SUFDTCxlQUFJLEdBQUcsb0JBQW9CLENBQUM7SUFFNUIseUJBQWMsR0FBRyx1QkFBdUIsQ0FBQztBQUN4RCxDQUFDLEVBSlMsVUFBVSxLQUFWLFVBQVUsUUFJbkI7QUFFRCxNQUFNLFNBQVMsR0FBRyw0Q0FBNEMsQ0FBQztBQUUvRDs7R0FFRztBQUNILE1BQU0sYUFBYSxHQUEwQztJQUMzRCxFQUFFLEVBQUUsU0FBUztJQUNiLFdBQVcsRUFBRSx1Q0FBdUM7SUFDcEQsU0FBUyxFQUFFLElBQUk7SUFDZixRQUFRLEVBQUUsRUFBRTtJQUNaLFFBQVEsRUFBRSxDQUFDLGdFQUFXLEVBQUUsaUVBQWUsRUFBRSxvRUFBZSxDQUFDO0lBQ3pELFFBQVEsRUFBRSxxRUFBYztJQUN4QixRQUFRLEVBQUUsQ0FDUixHQUFlLEVBQ2YsVUFBOEIsRUFDOUIsT0FBK0IsRUFDL0IsUUFBZ0MsRUFDaEMsRUFBRTtRQUNGLE1BQU0sRUFBRSxRQUFRLEVBQUUsS0FBSyxFQUFFLEdBQUcsR0FBRyxDQUFDO1FBQ2hDLFVBQVUsR0FBRyxVQUFVLGFBQVYsVUFBVSxjQUFWLFVBQVUsR0FBSSxtRUFBYyxDQUFDO1FBQzFDLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFFNUMsdUJBQXVCO1FBQ3ZCLE1BQU0sUUFBUSxHQUFHLEtBQUssQ0FBQyxFQUFFLENBQUMsZ0JBQWdCLENBQUMsQ0FBQztRQUM1QyxNQUFNLFdBQVcsR0FBRyxLQUFLLENBQUMsRUFBRSxDQUFD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aWNhdGlvbi10b3AvLi4vcGFja2FnZXMvcGx1Z2lubWFuYWdlci1leHRlbnNpb24vc3JjL2luZGV4LnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuLyoqXG4gKiBAcGFja2FnZURvY3VtZW50YXRpb25cbiAqIEBtb2R1bGUgcGx1Z2lubWFuYWdlci1leHRlbnNpb25cbiAqL1xuaW1wb3J0IHtcbiAgSUxheW91dFJlc3RvcmVyLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW4sXG4gIEp1cHl0ZXJMYWJcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHtcbiAgSUNvbW1hbmRQYWxldHRlLFxuICBNYWluQXJlYVdpZGdldCxcbiAgV2lkZ2V0VHJhY2tlclxufSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciwgbnVsbFRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQge1xuICBDb21tYW5kVG9vbGJhckJ1dHRvbixcbiAgZXh0ZW5zaW9uSWNvbixcbiAgcmVmcmVzaEljb25cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvdWktY29tcG9uZW50cyc7XG5pbXBvcnQgeyBSZWFkb25seUpTT05PYmplY3QgfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQge1xuICBJUGx1Z2luTWFuYWdlcixcbiAgUGx1Z2luTGlzdE1vZGVsLFxuICBQbHVnaW5zXG59IGZyb20gJ0BqdXB5dGVybGFiL3BsdWdpbm1hbmFnZXInO1xuXG4vKipcbiAqIFRoZSBjb21tYW5kIElEcyB1c2VkIGJ5IHRoZSBwbHVnaW5tYW5hZ2VyIHBsdWdpbi5cbiAqL1xubmFtZXNwYWNlIENvbW1hbmRJRHMge1xuICBleHBvcnQgY29uc3Qgb3BlbiA9ICdwbHVnaW5tYW5hZ2VyOm9wZW4nO1xuXG4gIGV4cG9ydCBjb25zdCByZWZyZXNoUGx1Z2lucyA9ICdwbHVnaW5tYW5hZ2VyOnJlZnJlc2gnO1xufVxuXG5jb25zdCBQTFVHSU5fSUQgPSAnQGp1cHl0ZXJsYWIvcGx1Z2lubWFuYWdlci1leHRlbnNpb246cGx1Z2luJztcblxuLyoqXG4gKiBBIHBsdWdpbiBmb3IgbWFuYWdpbmcgc3RhdHVzIG9mIG90aGVyIHBsdWdpbnMuXG4gKi9cbmNvbnN0IHBsdWdpbm1hbmFnZXI6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJUGx1Z2luTWFuYWdlcj4gPSB7XG4gIGlkOiBQTFVHSU5fSUQsXG4gIGRlc2NyaXB0aW9uOiAnRW5hYmxlIG9yIGRpc2FibGUgaW5kaXZpZHVhbCBwbHVnaW5zLicsXG4gIGF1dG9TdGFydDogdHJ1ZSxcbiAgcmVxdWlyZXM6IFtdLFxuICBvcHRpb25hbDogW0lUcmFuc2xhdG9yLCBJQ29tbWFuZFBhbGV0dGUsIElMYXlvdXRSZXN0b3Jlcl0sXG4gIHByb3ZpZGVzOiBJUGx1Z2luTWFuYWdlcixcbiAgYWN0aXZhdGU6IChcbiAgICBhcHA6IEp1cHl0ZXJMYWIsXG4gICAgdHJhbnNsYXRvcjogSVRyYW5zbGF0b3IgfCBudWxsLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGwsXG4gICAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbiAgKSA9PiB7XG4gICAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcbiAgICB0cmFuc2xhdG9yID0gdHJhbnNsYXRvciA/PyBudWxsVHJhbnNsYXRvcjtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuXG4gICAgLy8gVHJhbnNsYXRpb24gc3RyaW5ncy5cbiAgICBjb25zdCBjYXRlZ29yeSA9IHRyYW5zLl9fKCdQbHVnaW4gTWFuYWdlcicpO1xuICAgIGNvbnN0IHdpZGdldExhYmVsID0gdHJhbnMuX18oJ0FkdmFuY2VkIFBsdWdpbiBNYW5hZ2VyJyk7XG4gICAgY29uc3QgcmVmcmVzaFBsdWdpbnMgPSB0cmFucy5fXygnUmVmcmVzaCBQbHVnaW4gTGlzdCcpO1xuXG4gICAgY29uc3QgbmFtZXNwYWNlID0gJ3BsdWdpbi1tYW5hZ2VyJztcbiAgICBjb25zdCB0cmFja2VyID0gbmV3IFdpZGdldFRyYWNrZXI8TWFpbkFyZWFXaWRnZXQ8UGx1Z2lucz4+KHtcbiAgICAgIG5hbWVzcGFjZTogbmFtZXNwYWNlXG4gICAgfSk7XG5cbiAgICAvKipcbiAgICAgKiBDcmVhdGUgYSBNYWluQXJlYVdpZGdldCBmb3IgUGx1Z2luIE1hbmFnZXIuXG4gICAgICovXG4gICAgZnVuY3Rpb24gY3JlYXRlV2lkZ2V0KGFyZ3M/OiBQbHVnaW5MaXN0TW9kZWwuSUNvbmZpZ3VyYWJsZVN0YXRlKSB7XG4gICAgICBjb25zdCBtb2RlbCA9IG5ldyBQbHVnaW5MaXN0TW9kZWwoe1xuICAgICAgICAuLi5hcmdzLFxuICAgICAgICBwbHVnaW5EYXRhOiB7XG4gICAgICAgICAgYXZhaWxhYmxlUGx1Z2luczogYXBwLmluZm8uYXZhaWxhYmxlUGx1Z2luc1xuICAgICAgICB9LFxuICAgICAgICBzZXJ2ZXJTZXR0aW5nczogYXBwLnNlcnZpY2VNYW5hZ2VyLnNlcnZlclNldHRpbmdzLFxuICAgICAgICBleHRyYUxvY2tlZFBsdWdpbnM6IFtcbiAgICAgICAgICBQTFVHSU5fSUQsXG4gICAgICAgICAgLy8gVUkgd2lsbCBub3QgcHJvY2VlZCBiZXlvbmQgc3BsYXNoIHdpdGhvdXQgYGxheW91dGAgcGx1Z2luXG4gICAgICAgICAgJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLWV4dGVuc2lvbjpsYXlvdXQnLFxuICAgICAgICAgIC8vIFN0YXRlIHJlc3RvcmF0aW9uIGRvZXMgbm90IHdvcmsgd2VsbCB3aXRob3V0IHJlc29sdmVyLFxuICAgICAgICAgIC8vIGNhbiBsZWF2ZSB1c2VyIGxvY2tlZCBvdXQgb2YgdGhlIHBsdWdpbiBtYW5hZ2VyXG4gICAgICAgICAgLy8gKGlmIGNvbW1hbmQgcGFsZXR0ZSBhbmQgbWVudSBhcmUgZGlzYWJsZWQgdG9vKVxuICAgICAgICAgICdAanVweXRlcmxhYi9hcHB1dGlscy1leHRlbnNpb246cmVzb2x2ZXInXG4gICAgICAgIF0sXG4gICAgICAgIHRyYW5zbGF0b3I6IHRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3JcbiAgICAgIH0pO1xuICAgICAgY29uc3QgY29udGVudCA9IG5ldyBQbHVnaW5zKHtcbiAgICAgICAgbW9kZWwsXG4gICAgICAgIHRyYW5zbGF0b3I6IHRyYW5zbGF0b3IgPz8gbnVsbFRyYW5zbGF0b3JcbiAgICAgIH0pO1xuICAgICAgY29udGVudC50aXRsZS5sYWJlbCA9IHdpZGdldExhYmVsO1xuICAgICAgY29udGVudC50aXRsZS5pY29uID0gZXh0ZW5zaW9uSWNvbjtcbiAgICAgIGNvbnN0IG1haW4gPSBuZXcgTWFpbkFyZWFXaWRnZXQoeyBjb250ZW50LCByZXZlYWw6IG1vZGVsLnJlYWR5IH0pO1xuXG4gICAgICBtYWluLnRvb2xiYXIuYWRkSXRlbShcbiAgICAgICAgJ3JlZnJlc2gtcGx1Z2lucycsXG4gICAgICAgIG5ldyBDb21tYW5kVG9vbGJhckJ1dHRvbih7XG4gICAgICAgICAgaWQ6IENvbW1hbmRJRHMucmVmcmVzaFBsdWdpbnMsXG4gICAgICAgICAgYXJnczogeyBub0xhYmVsOiB0cnVlIH0sXG4gICAgICAgICAgY29tbWFuZHNcbiAgICAgICAgfSlcbiAgICAgICk7XG5cbiAgICAgIHJldHVybiBtYWluO1xuICAgIH1cblxuICAgIC8vIFJlZ2lzdGVyIGNvbW1hbmRzLlxuICAgIGNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5vcGVuLCB7XG4gICAgICBsYWJlbDogd2lkZ2V0TGFiZWwsXG4gICAgICBleGVjdXRlOiBhcmdzID0+IHtcbiAgICAgICAgY29uc3QgbWFpbiA9IGNyZWF0ZVdpZGdldChhcmdzKTtcbiAgICAgICAgc2hlbGwuYWRkKG1haW4sICdtYWluJywgeyB0eXBlOiAnUGx1Z2lucycgfSk7XG5cbiAgICAgICAgLy8gYWRkIHRvIHRyYWNrZXIgc28gaXQgY2FuIGJlIHJlc3RvcmVkLCBhbmQgdXBkYXRlIHdoZW4gY2hvaWNlcyBjaGFuZ2VcbiAgICAgICAgdm9pZCB0cmFja2VyLmFkZChtYWluKTtcbiAgICAgICAgbWFpbi5jb250ZW50Lm1vZGVsLnRyYWNrZXJEYXRhQ2hhbmdlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICB2b2lkIHRyYWNrZXIuc2F2ZShtYWluKTtcbiAgICAgICAgfSk7XG4gICAgICAgIHJldHVybiBtYWluO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgY29tbWFuZHMuYWRkQ29tbWFuZChDb21tYW5kSURzLnJlZnJlc2hQbHVnaW5zLCB7XG4gICAgICBsYWJlbDogYXJncyA9PiAoYXJncy5ub0xhYmVsID8gJycgOiByZWZyZXNoUGx1Z2lucyksXG4gICAgICBjYXB0aW9uOiB0cmFucy5fXygnUmVmcmVzaCBwbHVnaW5zIGxpc3QnKSxcbiAgICAgIGljb246IHJlZnJlc2hJY29uLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICByZXR1cm4gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50Lm1vZGVsXG4gICAgICAgICAgLnJlZnJlc2goKVxuICAgICAgICAgIC5jYXRjaCgocmVhc29uOiBFcnJvcikgPT4ge1xuICAgICAgICAgICAgY29uc29sZS5lcnJvcihcbiAgICAgICAgICAgICAgYEZhaWxlZCB0byByZWZyZXNoIHRoZSBhdmFpbGFibGUgcGx1Z2lucyBsaXN0OlxcbiR7cmVhc29ufWBcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgfSk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICBpZiAocGFsZXR0ZSkge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZDogQ29tbWFuZElEcy5vcGVuLCBjYXRlZ29yeSB9KTtcbiAgICB9XG5cbiAgICBpZiAocmVzdG9yZXIpIHtcbiAgICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMub3BlbixcbiAgICAgICAgbmFtZTogXyA9PiAncGx1Z2lucycsXG4gICAgICAgIGFyZ3M6IHdpZGdldCA9PiB7XG4gICAgICAgICAgY29uc3QgeyBxdWVyeSwgaXNEaXNjbGFpbWVkIH0gPSB3aWRnZXQuY29udGVudC5tb2RlbDtcbiAgICAgICAgICBjb25zdCBhcmdzOiBQbHVnaW5MaXN0TW9kZWwuSUNvbmZpZ3VyYWJsZVN0YXRlID0ge1xuICAgICAgICAgICAgcXVlcnksXG4gICAgICAgICAgICBpc0Rpc2NsYWltZWRcbiAgICAgICAgICB9O1xuICAgICAgICAgIHJldHVybiBhcmdzIGFzIFJlYWRvbmx5SlNPTk9iamVjdDtcbiAgICAgICAgfVxuICAgICAgfSk7XG4gICAgfVxuICAgIHJldHVybiB7XG4gICAgICBvcGVuOiAoKSA9PiB7XG4gICAgICAgIHJldHVybiBhcHAuY29tbWFuZHMuZXhlY3V0ZShDb21tYW5kSURzLm9wZW4pO1xuICAgICAgfVxuICAgIH07XG4gIH1cbn07XG5cbmNvbnN0IHBsdWdpbnM6IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxhbnk+W10gPSBbcGx1Z2lubWFuYWdlcl07XG5cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbnM7XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=