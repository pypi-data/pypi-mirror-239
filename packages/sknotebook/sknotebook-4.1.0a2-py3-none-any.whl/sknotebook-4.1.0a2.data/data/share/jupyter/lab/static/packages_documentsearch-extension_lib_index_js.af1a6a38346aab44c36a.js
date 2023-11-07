"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_documentsearch-extension_lib_index_js"],{

/***/ "../packages/documentsearch-extension/lib/index.js":
/*!*********************************************************!*\
  !*** ../packages/documentsearch-extension/lib/index.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/documentsearch */ "webpack/sharing/consume/default/@jupyterlab/documentsearch/@jupyterlab/documentsearch");
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module documentsearch-extension
 */






/**
 * Class added to widgets that can be searched (have a search provider).
 */
const SEARCHABLE_CLASS = 'jp-mod-searchable';
/**
 * Class added to widgets with open search view (not necessarily focused).
 */
const SEARCH_ACTIVE_CLASS = 'jp-mod-search-active';
var CommandIDs;
(function (CommandIDs) {
    /**
     * Start search in a document
     */
    CommandIDs.search = 'documentsearch:start';
    /**
     * Start search and replace in a document
     */
    CommandIDs.searchAndReplace = 'documentsearch:startWithReplace';
    /**
     * Find next search match
     */
    CommandIDs.findNext = 'documentsearch:highlightNext';
    /**
     * Find previous search match
     */
    CommandIDs.findPrevious = 'documentsearch:highlightPrevious';
    /**
     * End search in a document
     */
    CommandIDs.end = 'documentsearch:end';
    /**
     * Toggle search in selection
     */
    CommandIDs.toggleSearchInSelection = 'documentsearch:toggleSearchInSelection';
})(CommandIDs || (CommandIDs = {}));
const labShellWidgetListener = {
    id: '@jupyterlab/documentsearch-extension:labShellWidgetListener',
    description: 'Active search on valid document',
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry],
    autoStart: true,
    activate: (app, labShell, registry) => {
        // If a given widget is searchable, apply the searchable class.
        // If it's not searchable, remove the class.
        const transformWidgetSearchability = (widget) => {
            if (!widget) {
                return;
            }
            if (registry.hasProvider(widget)) {
                widget.addClass(SEARCHABLE_CLASS);
            }
            else {
                widget.removeClass(SEARCHABLE_CLASS);
            }
        };
        // Update searchability of the active widget when the registry
        // changes, in case a provider for the current widget was added
        // or removed
        registry.changed.connect(() => transformWidgetSearchability(labShell.activeWidget));
        // Apply the searchable class only to the active widget if it is actually
        // searchable. Remove the searchable class from a widget when it's
        // no longer active.
        labShell.activeChanged.connect((_, args) => {
            const oldWidget = args.oldValue;
            if (oldWidget) {
                oldWidget.removeClass(SEARCHABLE_CLASS);
            }
            transformWidgetSearchability(args.newValue);
        });
    }
};
/**
 * Exposes the current keybindings to search box view.
 */
class SearchKeyBindings {
    constructor(_commandRegistry) {
        this._commandRegistry = _commandRegistry;
        this._cache = this._buildCache();
        this._commandRegistry.keyBindingChanged.connect(this._rebuildCache, this);
    }
    get next() {
        return this._cache.next;
    }
    get previous() {
        return this._cache.previous;
    }
    get toggleSearchInSelection() {
        return this._cache.toggleSearchInSelection;
    }
    _rebuildCache() {
        this._cache = this._buildCache();
    }
    _buildCache() {
        const next = this._commandRegistry.keyBindings.find(binding => binding.command === CommandIDs.findNext);
        const previous = this._commandRegistry.keyBindings.find(binding => binding.command === CommandIDs.findPrevious);
        const toggleSearchInSelection = this._commandRegistry.keyBindings.find(binding => binding.command === CommandIDs.toggleSearchInSelection);
        return {
            next,
            previous,
            toggleSearchInSelection
        };
    }
    dispose() {
        this._commandRegistry.keyBindingChanged.disconnect(this._rebuildCache, this);
    }
}
/**
 * Initialization data for the document-search extension.
 */
const extension = {
    id: '@jupyterlab/documentsearch-extension:plugin',
    description: 'Provides the document search registry.',
    provides: _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.ISearchProviderRegistry,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_4__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry],
    autoStart: true,
    activate: (app, translator, palette, settingRegistry) => {
        const trans = translator.load('jupyterlab');
        let searchDebounceTime = 500;
        let autoSearchInSelection = 'never';
        // Create registry
        const registry = new _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.SearchProviderRegistry(translator);
        const searchViews = new Map();
        if (settingRegistry) {
            const loadSettings = settingRegistry.load(extension.id);
            const updateSettings = (settings) => {
                searchDebounceTime = settings.get('searchDebounceTime')
                    .composite;
                autoSearchInSelection = settings.get('autoSearchInSelection')
                    .composite;
            };
            Promise.all([loadSettings, app.restored])
                .then(([settings]) => {
                updateSettings(settings);
                settings.changed.connect(settings => {
                    updateSettings(settings);
                });
            })
                .catch((reason) => {
                console.error(reason.message);
            });
        }
        const isEnabled = () => {
            const widget = app.shell.currentWidget;
            if (!widget) {
                return false;
            }
            return registry.hasProvider(widget);
        };
        const getSearchWidget = (widget) => {
            if (!widget) {
                return;
            }
            const widgetId = widget.id;
            let searchView = searchViews.get(widgetId);
            if (!searchView) {
                const searchProvider = registry.getProvider(widget);
                if (!searchProvider) {
                    return;
                }
                const searchModel = new _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.SearchDocumentModel(searchProvider, searchDebounceTime);
                const keyBingingsInfo = new SearchKeyBindings(app.commands);
                const newView = new _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.SearchDocumentView(searchModel, translator, keyBingingsInfo);
                searchViews.set(widgetId, newView);
                // find next, previous and end are now enabled
                [
                    CommandIDs.findNext,
                    CommandIDs.findPrevious,
                    CommandIDs.end,
                    CommandIDs.toggleSearchInSelection
                ].forEach(id => {
                    app.commands.notifyCommandChanged(id);
                });
                /**
                 * Activate the target widget when the search panel is closing
                 */
                newView.closed.connect(() => {
                    if (!widget.isDisposed) {
                        widget.activate();
                        widget.removeClass(SEARCH_ACTIVE_CLASS);
                    }
                });
                /**
                 * Remove from mapping when the search view is disposed.
                 */
                newView.disposed.connect(() => {
                    if (!widget.isDisposed) {
                        widget.activate();
                        widget.removeClass(SEARCH_ACTIVE_CLASS);
                    }
                    searchViews.delete(widgetId);
                    // find next, previous and end are now disabled
                    [
                        CommandIDs.findNext,
                        CommandIDs.findPrevious,
                        CommandIDs.end,
                        CommandIDs.toggleSearchInSelection
                    ].forEach(id => {
                        app.commands.notifyCommandChanged(id);
                    });
                });
                /**
                 * Dispose resources when the widget is disposed.
                 */
                widget.disposed.connect(() => {
                    newView.dispose();
                    searchModel.dispose();
                    searchProvider.dispose();
                    keyBingingsInfo.dispose();
                });
                searchView = newView;
            }
            if (!searchView.isAttached) {
                _lumino_widgets__WEBPACK_IMPORTED_MODULE_5__.Widget.attach(searchView, widget.node);
                widget.addClass(SEARCH_ACTIVE_CLASS);
                if (widget instanceof _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget) {
                    // Offset the position of the search widget to not cover the toolbar nor the content header.
                    // TODO this does not update once the search widget is displayed.
                    searchView.node.style.top = `${widget.toolbar.node.getBoundingClientRect().height +
                        widget.contentHeader.node.getBoundingClientRect().height}px`;
                }
                if (searchView.model.searchExpression) {
                    searchView.model.refresh();
                }
            }
            return searchView;
        };
        app.commands.addCommand(CommandIDs.search, {
            label: trans.__('Find…'),
            isEnabled: isEnabled,
            execute: async (args) => {
                const searchWidget = getSearchWidget(app.shell.currentWidget);
                if (searchWidget) {
                    const searchText = args['searchText'];
                    if (searchText) {
                        searchWidget.setSearchText(searchText);
                    }
                    else {
                        searchWidget.setSearchText(searchWidget.model.suggestedInitialQuery);
                    }
                    const selectionState = searchWidget.model.selectionState;
                    let enableSelectionMode = false;
                    switch (autoSearchInSelection) {
                        case 'multiple-selected':
                            enableSelectionMode = selectionState === 'multiple';
                            break;
                        case 'any-selected':
                            enableSelectionMode =
                                selectionState === 'multiple' || selectionState === 'single';
                            break;
                        case 'never':
                            // no-op
                            break;
                    }
                    if (enableSelectionMode) {
                        await searchWidget.model.setFilter('selection', true);
                    }
                    searchWidget.focusSearchInput();
                }
            }
        });
        app.commands.addCommand(CommandIDs.searchAndReplace, {
            label: trans.__('Find and Replace…'),
            isEnabled: isEnabled,
            execute: args => {
                const searchWidget = getSearchWidget(app.shell.currentWidget);
                if (searchWidget) {
                    const searchText = args['searchText'];
                    if (searchText) {
                        searchWidget.setSearchText(searchText);
                    }
                    else {
                        searchWidget.setSearchText(searchWidget.model.suggestedInitialQuery);
                    }
                    const replaceText = args['replaceText'];
                    if (replaceText) {
                        searchWidget.setReplaceText(replaceText);
                    }
                    searchWidget.showReplace();
                    searchWidget.focusSearchInput();
                }
            }
        });
        app.commands.addCommand(CommandIDs.findNext, {
            label: trans.__('Find Next'),
            isEnabled: () => !!app.shell.currentWidget &&
                searchViews.has(app.shell.currentWidget.id),
            execute: async () => {
                var _a;
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return;
                }
                await ((_a = searchViews.get(currentWidget.id)) === null || _a === void 0 ? void 0 : _a.model.highlightNext());
            }
        });
        app.commands.addCommand(CommandIDs.findPrevious, {
            label: trans.__('Find Previous'),
            isEnabled: () => !!app.shell.currentWidget &&
                searchViews.has(app.shell.currentWidget.id),
            execute: async () => {
                var _a;
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return;
                }
                await ((_a = searchViews.get(currentWidget.id)) === null || _a === void 0 ? void 0 : _a.model.highlightPrevious());
            }
        });
        app.commands.addCommand(CommandIDs.end, {
            label: trans.__('End Search'),
            isEnabled: () => !!app.shell.currentWidget &&
                searchViews.has(app.shell.currentWidget.id),
            execute: async () => {
                var _a;
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return;
                }
                (_a = searchViews.get(currentWidget.id)) === null || _a === void 0 ? void 0 : _a.close();
            }
        });
        app.commands.addCommand(CommandIDs.toggleSearchInSelection, {
            label: trans.__('Search in Selection'),
            isEnabled: () => !!app.shell.currentWidget &&
                searchViews.has(app.shell.currentWidget.id) &&
                'selection' in
                    searchViews.get(app.shell.currentWidget.id).model.filtersDefinition,
            execute: async () => {
                var _a;
                const currentWidget = app.shell.currentWidget;
                if (!currentWidget) {
                    return;
                }
                const model = (_a = searchViews.get(currentWidget.id)) === null || _a === void 0 ? void 0 : _a.model;
                if (!model) {
                    return;
                }
                const currentValue = model.filters['selection'];
                return model.setFilter('selection', !currentValue);
            }
        });
        // Add the command to the palette.
        if (palette) {
            [
                CommandIDs.search,
                CommandIDs.findNext,
                CommandIDs.findPrevious,
                CommandIDs.end,
                CommandIDs.toggleSearchInSelection
            ].forEach(command => {
                palette.addItem({
                    command,
                    category: trans.__('Main Area')
                });
            });
        }
        // Provide the registry to the system.
        return registry;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([extension, labShellWidgetListener]);


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfZG9jdW1lbnRzZWFyY2gtZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy5hZjFhNmEzODM0NmFhYjQ0YzM2YS5qcyIsIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDc0M7QUFPbkM7QUFDMkI7QUFDVDtBQUViO0FBRXpDOztHQUVHO0FBQ0gsTUFBTSxnQkFBZ0IsR0FBRyxtQkFBbUIsQ0FBQztBQUM3Qzs7R0FFRztBQUNILE1BQU0sbUJBQW1CLEdBQUcsc0JBQXNCLENBQUM7QUFFbkQsSUFBVSxVQUFVLENBMEJuQjtBQTFCRCxXQUFVLFVBQVU7SUFDbEI7O09BRUc7SUFDVSxpQkFBTSxHQUFHLHNCQUFzQixDQUFDO0lBQzdDOztPQUVHO0lBQ1UsMkJBQWdCLEdBQUcsaUNBQWlDLENBQUM7SUFDbEU7O09BRUc7SUFDVSxtQkFBUSxHQUFHLDhCQUE4QixDQUFDO0lBQ3ZEOztPQUVHO0lBQ1UsdUJBQVksR0FBRyxrQ0FBa0MsQ0FBQztJQUMvRDs7T0FFRztJQUNVLGNBQUcsR0FBRyxvQkFBb0IsQ0FBQztJQUN4Qzs7T0FFRztJQUNVLGtDQUF1QixHQUNsQyx3Q0FBd0MsQ0FBQztBQUM3QyxDQUFDLEVBMUJTLFVBQVUsS0FBVixVQUFVLFFBMEJuQjtBQVdELE1BQU0sc0JBQXNCLEdBQWdDO0lBQzFELEVBQUUsRUFBRSw2REFBNkQ7SUFDakUsV0FBVyxFQUFFLGlDQUFpQztJQUM5QyxRQUFRLEVBQUUsQ0FBQyw4REFBUyxFQUFFLCtFQUF1QixDQUFDO0lBQzlDLFNBQVMsRUFBRSxJQUFJO0lBQ2YsUUFBUSxFQUFFLENBQ1IsR0FBb0IsRUFDcEIsUUFBbUIsRUFDbkIsUUFBaUMsRUFDakMsRUFBRTtRQUNGLCtEQUErRDtRQUMvRCw0Q0FBNEM7UUFDNUMsTUFBTSw0QkFBNEIsR0FBRyxDQUFDLE1BQXFCLEVBQUUsRUFBRTtZQUM3RCxJQUFJLENBQUMsTUFBTSxF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QUFDLE1BQU07Z0JBQ2pCLFVBQVUsQ0FBQyxRQUFRO2dCQUNuQixVQUFVLENBQUMsWUFBWTtnQkFDdkIsVUFBVSxDQUFDLEdBQUc7Z0JBQ2QsVUFBVSxDQUFDLHVCQUF1QjthQUNuQyxDQUFDLE9BQU8sQ0FBQyxPQUFPLENBQUMsRUFBRTtnQkFDbEIsT0FBTyxDQUFDLE9BQU8sQ0FBQztvQkFDZCxPQUFPO29CQUNQLFFBQVEsRUFBRSxLQUFLLENBQUMsRUFBRSxDQUFDLFdBQVcsQ0FBQztpQkFDaEMsQ0FBQyxDQUFDO1lBQ0wsQ0FBQyxDQUFDLENBQUM7U0FDSjtRQUVELHNDQUFzQztRQUN0QyxPQUFPLFFBQVEsQ0FBQztJQUNsQixDQUFDO0NBQ0YsQ0FBQztBQUVGLGlFQUFlLENBQUMsU0FBUyxFQUFFLHNCQUFzQixDQUFDLEVBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvZG9jdW1lbnRzZWFyY2gtZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBkb2N1bWVudHNlYXJjaC1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU2hlbGwsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IElDb21tYW5kUGFsZXR0ZSwgTWFpbkFyZWFXaWRnZXQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQge1xuICBJU2VhcmNoS2V5QmluZGluZ3MsXG4gIElTZWFyY2hQcm92aWRlclJlZ2lzdHJ5LFxuICBTZWFyY2hEb2N1bWVudE1vZGVsLFxuICBTZWFyY2hEb2N1bWVudFZpZXcsXG4gIFNlYXJjaFByb3ZpZGVyUmVnaXN0cnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvZG9jdW1lbnRzZWFyY2gnO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSB9IGZyb20gJ0BqdXB5dGVybGFiL3NldHRpbmdyZWdpc3RyeSc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBDbGFzcyBhZGRlZCB0byB3aWRnZXRzIHRoYXQgY2FuIGJlIHNlYXJjaGVkIChoYXZlIGEgc2VhcmNoIHByb3ZpZGVyKS5cbiAqL1xuY29uc3QgU0VBUkNIQUJMRV9DTEFTUyA9ICdqcC1tb2Qtc2VhcmNoYWJsZSc7XG4vKipcbiAqIENsYXNzIGFkZGVkIHRvIHdpZGdldHMgd2l0aCBvcGVuIHNlYXJjaCB2aWV3IChub3QgbmVjZXNzYXJpbHkgZm9jdXNlZCkuXG4gKi9cbmNvbnN0IFNFQVJDSF9BQ1RJVkVfQ0xBU1MgPSAnanAtbW9kLXNlYXJjaC1hY3RpdmUnO1xuXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIC8qKlxuICAgKiBTdGFydCBzZWFyY2ggaW4gYSBkb2N1bWVudFxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IHNlYXJjaCA9ICdkb2N1bWVudHNlYXJjaDpzdGFydCc7XG4gIC8qKlxuICAgKiBTdGFydCBzZWFyY2ggYW5kIHJlcGxhY2UgaW4gYSBkb2N1bWVudFxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IHNlYXJjaEFuZFJlcGxhY2UgPSAnZG9jdW1lbnRzZWFyY2g6c3RhcnRXaXRoUmVwbGFjZSc7XG4gIC8qKlxuICAgKiBGaW5kIG5leHQgc2VhcmNoIG1hdGNoXG4gICAqL1xuICBleHBvcnQgY29uc3QgZmluZE5leHQgPSAnZG9jdW1lbnRzZWFyY2g6aGlnaGxpZ2h0TmV4dCc7XG4gIC8qKlxuICAgKiBGaW5kIHByZXZpb3VzIHNlYXJjaCBtYXRjaFxuICAgKi9cbiAgZXhwb3J0IGNvbnN0IGZpbmRQcmV2aW91cyA9ICdkb2N1bWVudHNlYXJjaDpoaWdobGlnaHRQcmV2aW91cyc7XG4gIC8qKlxuICAgKiBFbmQgc2VhcmNoIGluIGEgZG9jdW1lbnRcbiAgICovXG4gIGV4cG9ydCBjb25zdCBlbmQgPSAnZG9jdW1lbnRzZWFyY2g6ZW5kJztcbiAgLyoqXG4gICAqIFRvZ2dsZSBzZWFyY2ggaW4gc2VsZWN0aW9uXG4gICAqL1xuICBleHBvcnQgY29uc3QgdG9nZ2xlU2VhcmNoSW5TZWxlY3Rpb24gPVxuICAgICdkb2N1bWVudHNlYXJjaDp0b2dnbGVTZWFyY2hJblNlbGVjdGlvbic7XG59XG5cbi8qKlxuICogV2hlbiBhdXRvbWF0aWMgc2VsZWN0aW9uIHNlYXJjaCBmaWx0ZXIgbG9naWMgc2hvdWxkIGJlIGFjdGl2ZS5cbiAqXG4gKiAtIGBtdWx0aXBsZS1zZWxlY3RlZGA6IHdoZW4gbXVsdGlwbGUgbGluZXMvY2VsbHMgYXJlIHNlbGVjdGVkXG4gKiAtIGBhbnktc2VsZWN0ZWRgOiB3aGVuIGFueSBudW1iZXIgb2YgY2hhcmFjdGVycy9jZWxscyBhcmUgc2VsZWN0ZWRcbiAqIC0gYG5ldmVyYDogbmV2ZXJcbiAqL1xudHlwZSBBdXRvU2VhcmNoSW5TZWxlY3Rpb24gPSAnbmV2ZXInIHwgJ211bHRpcGxlLXNlbGVjdGVkJyB8ICdhbnktc2VsZWN0ZWQnO1xuXG5jb25zdCBsYWJTaGVsbFdpZGdldExpc3RlbmVyOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvZG9jdW1lbnRzZWFyY2gtZXh0ZW5zaW9uOmxhYlNoZWxsV2lkZ2V0TGlzdGVuZXInLFxuICBkZXNjcmlwdGlvbjogJ0FjdGl2ZSBzZWFyY2ggb24gdmFsaWQgZG9jdW1lbnQnLFxuICByZXF1aXJlczogW0lMYWJTaGVsbCwgSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnldLFxuICBhdXRvU3RhcnQ6IHRydWUsXG4gIGFjdGl2YXRlOiAoXG4gICAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gICAgbGFiU2hlbGw6IElMYWJTaGVsbCxcbiAgICByZWdpc3RyeTogSVNlYXJjaFByb3ZpZGVyUmVnaXN0cnlcbiAgKSA9PiB7XG4gICAgLy8gSWYgYSBnaXZlbiB3aWRnZXQgaXMgc2VhcmNoYWJsZSwgYXBwbHkgdGhlIHNlYXJjaGFibGUgY2xhc3MuXG4gICAgLy8gSWYgaXQncyBub3Qgc2VhcmNoYWJsZSwgcmVtb3ZlIHRoZSBjbGFzcy5cbiAgICBjb25zdCB0cmFuc2Zvcm1XaWRnZXRTZWFyY2hhYmlsaXR5ID0gKHdpZGdldDogV2lkZ2V0IHwgbnVsbCkgPT4ge1xuICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuO1xuICAgICAgfVxuICAgICAgaWYgKHJlZ2lzdHJ5Lmhhc1Byb3ZpZGVyKHdpZGdldCkpIHtcbiAgICAgICAgd2lkZ2V0LmFkZENsYXNzKFNFQVJDSEFCTEVfQ0xBU1MpO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgd2lkZ2V0LnJlbW92ZUNsYXNzKFNFQVJDSEFCTEVfQ0xBU1MpO1xuICAgICAgfVxuICAgIH07XG5cbiAgICAvLyBVcGRhdGUgc2VhcmNoYWJpbGl0eSBvZiB0aGUgYWN0aXZlIHdpZGdldCB3aGVuIHRoZSByZWdpc3RyeVxuICAgIC8vIGNoYW5nZXMsIGluIGNhc2UgYSBwcm92aWRlciBmb3IgdGhlIGN1cnJlbnQgd2lkZ2V0IHdhcyBhZGRlZFxuICAgIC8vIG9yIHJlbW92ZWRcbiAgICByZWdpc3RyeS5jaGFuZ2VkLmNvbm5lY3QoKCkgPT5cbiAgICAgIHRyYW5zZm9ybVdpZGdldFNlYXJjaGFiaWxpdHkobGFiU2hlbGwuYWN0aXZlV2lkZ2V0KVxuICAgICk7XG5cbiAgICAvLyBBcHBseSB0aGUgc2VhcmNoYWJsZSBjbGFzcyBvbmx5IHRvIHRoZSBhY3RpdmUgd2lkZ2V0IGlmIGl0IGlzIGFjdHVhbGx5XG4gICAgLy8gc2VhcmNoYWJsZS4gUmVtb3ZlIHRoZSBzZWFyY2hhYmxlIGNsYXNzIGZyb20gYSB3aWRnZXQgd2hlbiBpdCdzXG4gICAgLy8gbm8gbG9uZ2VyIGFjdGl2ZS5cbiAgICBsYWJTaGVsbC5hY3RpdmVDaGFuZ2VkLmNvbm5lY3QoKF8sIGFyZ3MpID0+IHtcbiAgICAgIGNvbnN0IG9sZFdpZGdldCA9IGFyZ3Mub2xkVmFsdWU7XG4gICAgICBpZiAob2xkV2lkZ2V0KSB7XG4gICAgICAgIG9sZFdpZGdldC5yZW1vdmVDbGFzcyhTRUFSQ0hBQkxFX0NMQVNTKTtcbiAgICAgIH1cbiAgICAgIHRyYW5zZm9ybVdpZGdldFNlYXJjaGFiaWxpdHkoYXJncy5uZXdWYWx1ZSk7XG4gICAgfSk7XG4gIH1cbn07XG5cbnR5cGUgS2V5QmluZGluZ3NDYWNoZSA9IFJlY29yZDxcbiAgJ25leHQnIHwgJ3ByZXZpb3VzJyB8ICd0b2dnbGVTZWFyY2hJblNlbGVjdGlvbicsXG4gIENvbW1hbmRSZWdpc3RyeS5JS2V5QmluZGluZyB8IHVuZGVmaW5lZFxuPjtcblxuLyoqXG4gKiBFeHBvc2VzIHRoZSBjdXJyZW50IGtleWJpbmRpbmdzIHRvIHNlYXJjaCBib3ggdmlldy5cbiAqL1xuY2xhc3MgU2VhcmNoS2V5QmluZGluZ3MgaW1wbGVtZW50cyBJU2VhcmNoS2V5QmluZGluZ3Mge1xuICBjb25zdHJ1Y3Rvcihwcml2YXRlIF9jb21tYW5kUmVnaXN0cnk6IENvbW1hbmRSZWdpc3RyeSkge1xuICAgIHRoaXMuX2NhY2hlID0gdGhpcy5fYnVpbGRDYWNoZSgpO1xuICAgIHRoaXMuX2NvbW1hbmRSZWdpc3RyeS5rZXlCaW5kaW5nQ2hhbmdlZC5jb25uZWN0KHRoaXMuX3JlYnVpbGRDYWNoZSwgdGhpcyk7XG4gIH1cblxuICBnZXQgbmV4dCgpIHtcbiAgICByZXR1cm4gdGhpcy5fY2FjaGUubmV4dDtcbiAgfVxuXG4gIGdldCBwcmV2aW91cygpIHtcbiAgICByZXR1cm4gdGhpcy5fY2FjaGUucHJldmlvdXM7XG4gIH1cblxuICBnZXQgdG9nZ2xlU2VhcmNoSW5TZWxlY3Rpb24oKSB7XG4gICAgcmV0dXJuIHRoaXMuX2NhY2hlLnRvZ2dsZVNlYXJjaEluU2VsZWN0aW9uO1xuICB9XG5cbiAgcHJpdmF0ZSBfcmVidWlsZENhY2hlKCkge1xuICAgIHRoaXMuX2NhY2hlID0gdGhpcy5fYnVpbGRDYWNoZSgpO1xuICB9XG5cbiAgcHJpdmF0ZSBfYnVpbGRDYWNoZSgpOiBLZXlCaW5kaW5nc0NhY2hlIHtcbiAgICBjb25zdCBuZXh0ID0gdGhpcy5fY29tbWFuZFJlZ2lzdHJ5LmtleUJpbmRpbmdzLmZpbmQoXG4gICAgICBiaW5kaW5nID0+IGJpbmRpbmcuY29tbWFuZCA9PT0gQ29tbWFuZElEcy5maW5kTmV4dFxuICAgICk7XG4gICAgY29uc3QgcHJldmlvdXMgPSB0aGlzLl9jb21tYW5kUmVnaXN0cnkua2V5QmluZGluZ3MuZmluZChcbiAgICAgIGJpbmRpbmcgPT4gYmluZGluZy5jb21tYW5kID09PSBDb21tYW5kSURzLmZpbmRQcmV2aW91c1xuICAgICk7XG4gICAgY29uc3QgdG9nZ2xlU2VhcmNoSW5TZWxlY3Rpb24gPSB0aGlzLl9jb21tYW5kUmVnaXN0cnkua2V5QmluZGluZ3MuZmluZChcbiAgICAgIGJpbmRpbmcgPT4gYmluZGluZy5jb21tYW5kID09PSBDb21tYW5kSURzLnRvZ2dsZVNlYXJjaEluU2VsZWN0aW9uXG4gICAgKTtcbiAgICByZXR1cm4ge1xuICAgICAgbmV4dCxcbiAgICAgIHByZXZpb3VzLFxuICAgICAgdG9nZ2xlU2VhcmNoSW5TZWxlY3Rpb25cbiAgICB9O1xuICB9XG5cbiAgZGlzcG9zZSgpIHtcbiAgICB0aGlzLl9jb21tYW5kUmVnaXN0cnkua2V5QmluZGluZ0NoYW5nZWQuZGlzY29ubmVjdChcbiAgICAgIHRoaXMuX3JlYnVpbGRDYWNoZSxcbiAgICAgIHRoaXNcbiAgICApO1xuICB9XG5cbiAgcHJpdmF0ZSBfY2FjaGU6IEtleUJpbmRpbmdzQ2FjaGU7XG59XG5cbi8qKlxuICogSW5pdGlhbGl6YXRpb24gZGF0YSBmb3IgdGhlIGRvY3VtZW50LXNlYXJjaCBleHRlbnNpb24uXG4gKi9cbmNvbnN0IGV4dGVuc2lvbjogSnVweXRlckZyb250RW5kUGx1Z2luPElTZWFyY2hQcm92aWRlclJlZ2lzdHJ5PiA9IHtcbiAgaWQ6ICdAanVweXRlcmxhYi9kb2N1bWVudHNlYXJjaC1leHRlbnNpb246cGx1Z2luJyxcbiAgZGVzY3JpcHRpb246ICdQcm92aWRlcyB0aGUgZG9jdW1lbnQgc2VhcmNoIHJlZ2lzdHJ5LicsXG4gIHByb3ZpZGVzOiBJU2VhcmNoUHJvdmlkZXJSZWdpc3RyeSxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUNvbW1hbmRQYWxldHRlLCBJU2V0dGluZ1JlZ2lzdHJ5XSxcbiAgYXV0b1N0YXJ0OiB0cnVlLFxuICBhY3RpdmF0ZTogKFxuICAgIGFwcDogSnVweXRlckZyb250RW5kLFxuICAgIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yLFxuICAgIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSxcbiAgICBzZXR0aW5nUmVnaXN0cnk6IElTZXR0aW5nUmVnaXN0cnkgfCBudWxsXG4gICkgPT4ge1xuICAgIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG5cbiAgICBsZXQgc2VhcmNoRGVib3VuY2VUaW1lID0gNTAwO1xuICAgIGxldCBhdXRvU2VhcmNoSW5TZWxlY3Rpb246IEF1dG9TZWFyY2hJblNlbGVjdGlvbiA9ICduZXZlcic7XG5cbiAgICAvLyBDcmVhdGUgcmVnaXN0cnlcbiAgICBjb25zdCByZWdpc3RyeTogU2VhcmNoUHJvdmlkZXJSZWdpc3RyeSA9IG5ldyBTZWFyY2hQcm92aWRlclJlZ2lzdHJ5KFxuICAgICAgdHJhbnNsYXRvclxuICAgICk7XG5cbiAgICBjb25zdCBzZWFyY2hWaWV3cyA9IG5ldyBNYXA8c3RyaW5nLCBTZWFyY2hEb2N1bWVudFZpZXc+KCk7XG5cbiAgICBpZiAoc2V0dGluZ1JlZ2lzdHJ5KSB7XG4gICAgICBjb25zdCBsb2FkU2V0dGluZ3MgPSBzZXR0aW5nUmVnaXN0cnkubG9hZChleHRlbnNpb24uaWQpO1xuICAgICAgY29uc3QgdXBkYXRlU2V0dGluZ3MgPSAoc2V0dGluZ3M6IElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzKTogdm9pZCA9PiB7XG4gICAgICAgIHNlYXJjaERlYm91bmNlVGltZSA9IHNldHRpbmdzLmdldCgnc2VhcmNoRGVib3VuY2VUaW1lJylcbiAgICAgICAgICAuY29tcG9zaXRlIGFzIG51bWJlcjtcbiAgICAgICAgYXV0b1NlYXJjaEluU2VsZWN0aW9uID0gc2V0dGluZ3MuZ2V0KCdhdXRvU2VhcmNoSW5TZWxlY3Rpb24nKVxuICAgICAgICAgIC5jb21wb3NpdGUgYXMgQXV0b1NlYXJjaEluU2VsZWN0aW9uO1xuICAgICAgfTtcblxuICAgICAgUHJvbWlzZS5hbGwoW2xvYWRTZXR0aW5ncywgYXBwLnJlc3RvcmVkXSlcbiAgICAgICAgLnRoZW4oKFtzZXR0aW5nc10pID0+IHtcbiAgICAgICAgICB1cGRhdGVTZXR0aW5ncyhzZXR0aW5ncyk7XG4gICAgICAgICAgc2V0dGluZ3MuY2hhbmdlZC5jb25uZWN0KHNldHRpbmdzID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZVNldHRpbmdzKHNldHRpbmdzKTtcbiAgICAgICAgICB9KTtcbiAgICAgICAgfSlcbiAgICAgICAgLmNhdGNoKChyZWFzb246IEVycm9yKSA9PiB7XG4gICAgICAgICAgY29uc29sZS5lcnJvcihyZWFzb24ubWVzc2FnZSk7XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIGNvbnN0IGlzRW5hYmxlZCA9ICgpID0+IHtcbiAgICAgIGNvbnN0IHdpZGdldCA9IGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0O1xuICAgICAgaWYgKCF3aWRnZXQpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgcmV0dXJuIHJlZ2lzdHJ5Lmhhc1Byb3ZpZGVyKHdpZGdldCk7XG4gICAgfTtcblxuICAgIGNvbnN0IGdldFNlYXJjaFdpZGdldCA9ICh3aWRnZXQ6IFdpZGdldCB8IG51bGwpID0+IHtcbiAgICAgIGlmICghd2lkZ2V0KSB7XG4gICAgICAgIHJldHVybjtcbiAgICAgIH1cbiAgICAgIGNvbnN0IHdpZGdldElkID0gd2lkZ2V0LmlkO1xuICAgICAgbGV0IHNlYXJjaFZpZXcgPSBzZWFyY2hWaWV3cy5nZXQod2lkZ2V0SWQpO1xuICAgICAgaWYgKCFzZWFyY2hWaWV3KSB7XG4gICAgICAgIGNvbnN0IHNlYXJjaFByb3ZpZGVyID0gcmVnaXN0cnkuZ2V0UHJvdmlkZXIod2lkZ2V0KTtcbiAgICAgICAgaWYgKCFzZWFyY2hQcm92aWRlcikge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBzZWFyY2hNb2RlbCA9IG5ldyBTZWFyY2hEb2N1bWVudE1vZGVsKFxuICAgICAgICAgIHNlYXJjaFByb3ZpZGVyLFxuICAgICAgICAgIHNlYXJjaERlYm91bmNlVGltZVxuICAgICAgICApO1xuXG4gICAgICAgIGNvbnN0IGtleUJpbmdpbmdzSW5mbyA9IG5ldyBTZWFyY2hLZXlCaW5kaW5ncyhhcHAuY29tbWFuZHMpO1xuXG4gICAgICAgIGNvbnN0IG5ld1ZpZXcgPSBuZXcgU2VhcmNoRG9jdW1lbnRWaWV3KFxuICAgICAgICAgIHNlYXJjaE1vZGVsLFxuICAgICAgICAgIHRyYW5zbGF0b3IsXG4gICAgICAgICAga2V5QmluZ2luZ3NJbmZvXG4gICAgICAgICk7XG5cbiAgICAgICAgc2VhcmNoVmlld3Muc2V0KHdpZGdldElkLCBuZXdWaWV3KTtcbiAgICAgICAgLy8gZmluZCBuZXh0LCBwcmV2aW91cyBhbmQgZW5kIGFyZSBub3cgZW5hYmxlZFxuICAgICAgICBbXG4gICAgICAgICAgQ29tbWFuZElEcy5maW5kTmV4dCxcbiAgICAgICAgICBDb21tYW5kSURzLmZpbmRQcmV2aW91cyxcbiAgICAgICAgICBDb21tYW5kSURzLmVuZCxcbiAgICAgICAgICBDb21tYW5kSURzLnRvZ2dsZVNlYXJjaEluU2VsZWN0aW9uXG4gICAgICAgIF0uZm9yRWFjaChpZCA9PiB7XG4gICAgICAgICAgYXBwLmNvbW1hbmRzLm5vdGlmeUNvbW1hbmRDaGFuZ2VkKGlkKTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgLyoqXG4gICAgICAgICAqIEFjdGl2YXRlIHRoZSB0YXJnZXQgd2lkZ2V0IHdoZW4gdGhlIHNlYXJjaCBwYW5lbCBpcyBjbG9zaW5nXG4gICAgICAgICAqL1xuICAgICAgICBuZXdWaWV3LmNsb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICBpZiAoIXdpZGdldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgICB3aWRnZXQuYWN0aXZhdGUoKTtcbiAgICAgICAgICAgIHdpZGdldC5yZW1vdmVDbGFzcyhTRUFSQ0hfQUNUSVZFX0NMQVNTKTtcbiAgICAgICAgICB9XG4gICAgICAgIH0pO1xuXG4gICAgICAgIC8qKlxuICAgICAgICAgKiBSZW1vdmUgZnJvbSBtYXBwaW5nIHdoZW4gdGhlIHNlYXJjaCB2aWV3IGlzIGRpc3Bvc2VkLlxuICAgICAgICAgKi9cbiAgICAgICAgbmV3Vmlldy5kaXNwb3NlZC5jb25uZWN0KCgpID0+IHtcbiAgICAgICAgICBpZiAoIXdpZGdldC5pc0Rpc3Bvc2VkKSB7XG4gICAgICAgICAgICB3aWRnZXQuYWN0aXZhdGUoKTtcbiAgICAgICAgICAgIHdpZGdldC5yZW1vdmVDbGFzcyhTRUFSQ0hfQUNUSVZFX0NMQVNTKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgc2VhcmNoVmlld3MuZGVsZXRlKHdpZGdldElkKTtcbiAgICAgICAgICAvLyBmaW5kIG5leHQsIHByZXZpb3VzIGFuZCBlbmQgYXJlIG5vdyBkaXNhYmxlZFxuICAgICAgICAgIFtcbiAgICAgICAgICAgIENvbW1hbmRJRHMuZmluZE5leHQsXG4gICAgICAgICAgICBDb21tYW5kSURzLmZpbmRQcmV2aW91cyxcbiAgICAgICAgICAgIENvbW1hbmRJRHMuZW5kLFxuICAgICAgICAgICAgQ29tbWFuZElEcy50b2dnbGVTZWFyY2hJblNlbGVjdGlvblxuICAgICAgICAgIF0uZm9yRWFjaChpZCA9PiB7XG4gICAgICAgICAgICBhcHAuY29tbWFuZHMubm90aWZ5Q29tbWFuZENoYW5nZWQoaWQpO1xuICAgICAgICAgIH0pO1xuICAgICAgICB9KTtcblxuICAgICAgICAvKipcbiAgICAgICAgICogRGlzcG9zZSByZXNvdXJjZXMgd2hlbiB0aGUgd2lkZ2V0IGlzIGRpc3Bvc2VkLlxuICAgICAgICAgKi9cbiAgICAgICAgd2lkZ2V0LmRpc3Bvc2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICAgIG5ld1ZpZXcuZGlzcG9zZSgpO1xuICAgICAgICAgIHNlYXJjaE1vZGVsLmRpc3Bvc2UoKTtcbiAgICAgICAgICBzZWFyY2hQcm92aWRlci5kaXNwb3NlKCk7XG4gICAgICAgICAga2V5QmluZ2luZ3NJbmZvLmRpc3Bvc2UoKTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgc2VhcmNoVmlldyA9IG5ld1ZpZXc7XG4gICAgICB9XG5cbiAgICAgIGlmICghc2VhcmNoVmlldy5pc0F0dGFjaGVkKSB7XG4gICAgICAgIFdpZGdldC5hdHRhY2goc2VhcmNoVmlldywgd2lkZ2V0Lm5vZGUpO1xuICAgICAgICB3aWRnZXQuYWRkQ2xhc3MoU0VBUkNIX0FDVElWRV9DTEFTUyk7XG4gICAgICAgIGlmICh3aWRnZXQgaW5zdGFuY2VvZiBNYWluQXJlYVdpZGdldCkge1xuICAgICAgICAgIC8vIE9mZnNldCB0aGUgcG9zaXRpb24gb2YgdGhlIHNlYXJjaCB3aWRnZXQgdG8gbm90IGNvdmVyIHRoZSB0b29sYmFyIG5vciB0aGUgY29udGVudCBoZWFkZXIuXG4gICAgICAgICAgLy8gVE9ETyB0aGlzIGRvZXMgbm90IHVwZGF0ZSBvbmNlIHRoZSBzZWFyY2ggd2lkZ2V0IGlzIGRpc3BsYXllZC5cbiAgICAgICAgICBzZWFyY2hWaWV3Lm5vZGUuc3R5bGUudG9wID0gYCR7XG4gICAgICAgICAgICB3aWRnZXQudG9vbGJhci5ub2RlLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLmhlaWdodCArXG4gICAgICAgICAgICB3aWRnZXQuY29udGVudEhlYWRlci5ub2RlLmdldEJvdW5kaW5nQ2xpZW50UmVjdCgpLmhlaWdodFxuICAgICAgICAgIH1weGA7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKHNlYXJjaFZpZXcubW9kZWwuc2VhcmNoRXhwcmVzc2lvbikge1xuICAgICAgICAgIHNlYXJjaFZpZXcubW9kZWwucmVmcmVzaCgpO1xuICAgICAgICB9XG4gICAgICB9XG4gICAgICByZXR1cm4gc2VhcmNoVmlldztcbiAgICB9O1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zZWFyY2gsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRmluZOKApicpLFxuICAgICAgaXNFbmFibGVkOiBpc0VuYWJsZWQsXG4gICAgICBleGVjdXRlOiBhc3luYyBhcmdzID0+IHtcbiAgICAgICAgY29uc3Qgc2VhcmNoV2lkZ2V0ID0gZ2V0U2VhcmNoV2lkZ2V0KGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0KTtcbiAgICAgICAgaWYgKHNlYXJjaFdpZGdldCkge1xuICAgICAgICAgIGNvbnN0IHNlYXJjaFRleHQgPSBhcmdzWydzZWFyY2hUZXh0J10gYXMgc3RyaW5nO1xuICAgICAgICAgIGlmIChzZWFyY2hUZXh0KSB7XG4gICAgICAgICAgICBzZWFyY2hXaWRnZXQuc2V0U2VhcmNoVGV4dChzZWFyY2hUZXh0KTtcbiAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgc2VhcmNoV2lkZ2V0LnNldFNlYXJjaFRleHQoXG4gICAgICAgICAgICAgIHNlYXJjaFdpZGdldC5tb2RlbC5zdWdnZXN0ZWRJbml0aWFsUXVlcnlcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgfVxuICAgICAgICAgIGNvbnN0IHNlbGVjdGlvblN0YXRlID0gc2VhcmNoV2lkZ2V0Lm1vZGVsLnNlbGVjdGlvblN0YXRlO1xuXG4gICAgICAgICAgbGV0IGVuYWJsZVNlbGVjdGlvbk1vZGUgPSBmYWxzZTtcbiAgICAgICAgICBzd2l0Y2ggKGF1dG9TZWFyY2hJblNlbGVjdGlvbikge1xuICAgICAgICAgICAgY2FzZSAnbXVsdGlwbGUtc2VsZWN0ZWQnOlxuICAgICAgICAgICAgICBlbmFibGVTZWxlY3Rpb25Nb2RlID0gc2VsZWN0aW9uU3RhdGUgPT09ICdtdWx0aXBsZSc7XG4gICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAnYW55LXNlbGVjdGVkJzpcbiAgICAgICAgICAgICAgZW5hYmxlU2VsZWN0aW9uTW9kZSA9XG4gICAgICAgICAgICAgICAgc2VsZWN0aW9uU3RhdGUgPT09ICdtdWx0aXBsZScgfHwgc2VsZWN0aW9uU3RhdGUgPT09ICdzaW5nbGUnO1xuICAgICAgICAgICAgICBicmVhaztcbiAgICAgICAgICAgIGNhc2UgJ25ldmVyJzpcbiAgICAgICAgICAgICAgLy8gbm8tb3BcbiAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgfVxuICAgICAgICAgIGlmIChlbmFibGVTZWxlY3Rpb25Nb2RlKSB7XG4gICAgICAgICAgICBhd2FpdCBzZWFyY2hXaWRnZXQubW9kZWwuc2V0RmlsdGVyKCdzZWxlY3Rpb24nLCB0cnVlKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgc2VhcmNoV2lkZ2V0LmZvY3VzU2VhcmNoSW5wdXQoKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5zZWFyY2hBbmRSZXBsYWNlLCB7XG4gICAgICBsYWJlbDogdHJhbnMuX18oJ0ZpbmQgYW5kIFJlcGxhY2XigKYnKSxcbiAgICAgIGlzRW5hYmxlZDogaXNFbmFibGVkLFxuICAgICAgZXhlY3V0ZTogYXJncyA9PiB7XG4gICAgICAgIGNvbnN0IHNlYXJjaFdpZGdldCA9IGdldFNlYXJjaFdpZGdldChhcHAuc2hlbGwuY3VycmVudFdpZGdldCk7XG4gICAgICAgIGlmIChzZWFyY2hXaWRnZXQpIHtcbiAgICAgICAgICBjb25zdCBzZWFyY2hUZXh0ID0gYXJnc1snc2VhcmNoVGV4dCddIGFzIHN0cmluZztcbiAgICAgICAgICBpZiAoc2VhcmNoVGV4dCkge1xuICAgICAgICAgICAgc2VhcmNoV2lkZ2V0LnNldFNlYXJjaFRleHQoc2VhcmNoVGV4dCk7XG4gICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHNlYXJjaFdpZGdldC5zZXRTZWFyY2hUZXh0KFxuICAgICAgICAgICAgICBzZWFyY2hXaWRnZXQubW9kZWwuc3VnZ2VzdGVkSW5pdGlhbFF1ZXJ5XG4gICAgICAgICAgICApO1xuICAgICAgICAgIH1cbiAgICAgICAgICBjb25zdCByZXBsYWNlVGV4dCA9IGFyZ3NbJ3JlcGxhY2VUZXh0J10gYXMgc3RyaW5nO1xuICAgICAgICAgIGlmIChyZXBsYWNlVGV4dCkge1xuICAgICAgICAgICAgc2VhcmNoV2lkZ2V0LnNldFJlcGxhY2VUZXh0KHJlcGxhY2VUZXh0KTtcbiAgICAgICAgICB9XG4gICAgICAgICAgc2VhcmNoV2lkZ2V0LnNob3dSZXBsYWNlKCk7XG4gICAgICAgICAgc2VhcmNoV2lkZ2V0LmZvY3VzU2VhcmNoSW5wdXQoKTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5maW5kTmV4dCwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdGaW5kIE5leHQnKSxcbiAgICAgIGlzRW5hYmxlZDogKCkgPT5cbiAgICAgICAgISFhcHAuc2hlbGwuY3VycmVudFdpZGdldCAmJlxuICAgICAgICBzZWFyY2hWaWV3cy5oYXMoYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQuaWQpLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCBjdXJyZW50V2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGlmICghY3VycmVudFdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuXG4gICAgICAgIGF3YWl0IHNlYXJjaFZpZXdzLmdldChjdXJyZW50V2lkZ2V0LmlkKT8ubW9kZWwuaGlnaGxpZ2h0TmV4dCgpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5maW5kUHJldmlvdXMsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRmluZCBQcmV2aW91cycpLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PlxuICAgICAgICAhIWFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0ICYmXG4gICAgICAgIHNlYXJjaFZpZXdzLmhhcyhhcHAuc2hlbGwuY3VycmVudFdpZGdldC5pZCksXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IGN1cnJlbnRXaWRnZXQgPSBhcHAuc2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgaWYgKCFjdXJyZW50V2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgYXdhaXQgc2VhcmNoVmlld3MuZ2V0KGN1cnJlbnRXaWRnZXQuaWQpPy5tb2RlbC5oaWdobGlnaHRQcmV2aW91cygpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy5lbmQsIHtcbiAgICAgIGxhYmVsOiB0cmFucy5fXygnRW5kIFNlYXJjaCcpLFxuICAgICAgaXNFbmFibGVkOiAoKSA9PlxuICAgICAgICAhIWFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0ICYmXG4gICAgICAgIHNlYXJjaFZpZXdzLmhhcyhhcHAuc2hlbGwuY3VycmVudFdpZGdldC5pZCksXG4gICAgICBleGVjdXRlOiBhc3luYyAoKSA9PiB7XG4gICAgICAgIGNvbnN0IGN1cnJlbnRXaWRnZXQgPSBhcHAuc2hlbGwuY3VycmVudFdpZGdldDtcbiAgICAgICAgaWYgKCFjdXJyZW50V2lkZ2V0KSB7XG4gICAgICAgICAgcmV0dXJuO1xuICAgICAgICB9XG5cbiAgICAgICAgc2VhcmNoVmlld3MuZ2V0KGN1cnJlbnRXaWRnZXQuaWQpPy5jbG9zZSgpO1xuICAgICAgfVxuICAgIH0pO1xuXG4gICAgYXBwLmNvbW1hbmRzLmFkZENvbW1hbmQoQ29tbWFuZElEcy50b2dnbGVTZWFyY2hJblNlbGVjdGlvbiwge1xuICAgICAgbGFiZWw6IHRyYW5zLl9fKCdTZWFyY2ggaW4gU2VsZWN0aW9uJyksXG4gICAgICBpc0VuYWJsZWQ6ICgpID0+XG4gICAgICAgICEhYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQgJiZcbiAgICAgICAgc2VhcmNoVmlld3MuaGFzKGFwcC5zaGVsbC5jdXJyZW50V2lkZ2V0LmlkKSAmJlxuICAgICAgICAnc2VsZWN0aW9uJyBpblxuICAgICAgICAgIHNlYXJjaFZpZXdzLmdldChhcHAuc2hlbGwuY3VycmVudFdpZGdldC5pZCkhLm1vZGVsLmZpbHRlcnNEZWZpbml0aW9uLFxuICAgICAgZXhlY3V0ZTogYXN5bmMgKCkgPT4ge1xuICAgICAgICBjb25zdCBjdXJyZW50V2lkZ2V0ID0gYXBwLnNoZWxsLmN1cnJlbnRXaWRnZXQ7XG4gICAgICAgIGlmICghY3VycmVudFdpZGdldCkge1xuICAgICAgICAgIHJldHVybjtcbiAgICAgICAgfVxuICAgICAgICBjb25zdCBtb2RlbCA9IHNlYXJjaFZpZXdzLmdldChjdXJyZW50V2lkZ2V0LmlkKT8ubW9kZWw7XG4gICAgICAgIGlmICghbW9kZWwpIHtcbiAgICAgICAgICByZXR1cm47XG4gICAgICAgIH1cblxuICAgICAgICBjb25zdCBjdXJyZW50VmFsdWUgPSBtb2RlbC5maWx0ZXJzWydzZWxlY3Rpb24nXTtcbiAgICAgICAgcmV0dXJuIG1vZGVsLnNldEZpbHRlcignc2VsZWN0aW9uJywgIWN1cnJlbnRWYWx1ZSk7XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICAvLyBBZGQgdGhlIGNvbW1hbmQgdG8gdGhlIHBhbGV0dGUuXG4gICAgaWYgKHBhbGV0dGUpIHtcbiAgICAgIFtcbiAgICAgICAgQ29tbWFuZElEcy5zZWFyY2gsXG4gICAgICAgIENvbW1hbmRJRHMuZmluZE5leHQsXG4gICAgICAgIENvbW1hbmRJRHMuZmluZFByZXZpb3VzLFxuICAgICAgICBDb21tYW5kSURzLmVuZCxcbiAgICAgICAgQ29tbWFuZElEcy50b2dnbGVTZWFyY2hJblNlbGVjdGlvblxuICAgICAgXS5mb3JFYWNoKGNvbW1hbmQgPT4ge1xuICAgICAgICBwYWxldHRlLmFkZEl0ZW0oe1xuICAgICAgICAgIGNvbW1hbmQsXG4gICAgICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdNYWluIEFyZWEnKVxuICAgICAgICB9KTtcbiAgICAgIH0pO1xuICAgIH1cblxuICAgIC8vIFByb3ZpZGUgdGhlIHJlZ2lzdHJ5IHRvIHRoZSBzeXN0ZW0uXG4gICAgcmV0dXJuIHJlZ2lzdHJ5O1xuICB9XG59O1xuXG5leHBvcnQgZGVmYXVsdCBbZXh0ZW5zaW9uLCBsYWJTaGVsbFdpZGdldExpc3RlbmVyXTtcbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==