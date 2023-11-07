"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_csvviewer-extension_lib_searchprovider_js"],{

/***/ "../packages/csvviewer-extension/lib/searchprovider.js":
/*!*************************************************************!*\
  !*** ../packages/csvviewer-extension/lib/searchprovider.js ***!
  \*************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CSVSearchProvider": () => (/* binding */ CSVSearchProvider)
/* harmony export */ });
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/csvviewer */ "webpack/sharing/consume/default/@jupyterlab/csvviewer/@jupyterlab/csvviewer");
/* harmony import */ var _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/documentsearch */ "webpack/sharing/consume/default/@jupyterlab/documentsearch/@jupyterlab/documentsearch");
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * CSV viewer search provider
 */
class CSVSearchProvider extends _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_2__.SearchProvider {
    constructor() {
        super(...arguments);
        /**
         * Set to true if the widget under search is read-only, false
         * if it is editable.  Will be used to determine whether to show
         * the replace option.
         */
        this.isReadOnly = true;
    }
    /**
     * Instantiate a search provider for the widget.
     *
     * #### Notes
     * The widget provided is always checked using `isApplicable` before calling
     * this factory.
     *
     * @param widget The widget to search on
     * @param translator [optional] The translator object
     *
     * @returns The search provider on the widget
     */
    static createNew(widget, translator) {
        return new CSVSearchProvider(widget);
    }
    /**
     * Report whether or not this provider has the ability to search on the given object
     */
    static isApplicable(domain) {
        // check to see if the CSVSearchProvider can search on the
        // first cell, false indicates another editor is present
        return (domain instanceof _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget && domain.content instanceof _jupyterlab_csvviewer__WEBPACK_IMPORTED_MODULE_0__.CSVViewer);
    }
    /**
     * Clear currently highlighted match.
     */
    clearHighlight() {
        // no-op
        return Promise.resolve();
    }
    /**
     * Move the current match indicator to the next match.
     *
     * @param loop Whether to loop within the matches list.
     *
     * @returns The match is never returned by this provider
     */
    highlightNext(loop) {
        this.widget.content.searchService.find(this._query);
        return Promise.resolve(undefined);
    }
    /**
     * Move the current match indicator to the previous match.
     *
     * @param loop Whether to loop within the matches list.
     *
     * @returns The match is never returned by this provider
     */
    highlightPrevious(loop) {
        this.widget.content.searchService.find(this._query, true);
        return Promise.resolve(undefined);
    }
    /**
     * Replace the currently selected match with the provided text
     * Not implemented in the CSV viewer as it is read-only.
     *
     * @param newText The replacement text
     * @param loop Whether to loop within the matches list.
     *
     * @returns A promise that resolves once the action has completed.
     */
    replaceCurrentMatch(newText, loop) {
        return Promise.resolve(false);
    }
    /**
     * Replace all matches in the notebook with the provided text
     * Not implemented in the CSV viewer as it is read-only.
     *
     * @param newText The replacement text
     *
     * @returns A promise that resolves once the action has completed.
     */
    replaceAllMatches(newText) {
        return Promise.resolve(false);
    }
    /**
     * Initialize the search using the provided options.  Should update the UI
     * to highlight all matches and "select" whatever the first match should be.
     *
     * @param query A RegExp to be use to perform the search
     */
    startQuery(query) {
        this._query = query;
        this.widget.content.searchService.find(query);
        return Promise.resolve();
    }
    /**
     * Clears state of a search provider to prepare for startQuery to be called
     * in order to start a new query or refresh an existing one.
     */
    endQuery() {
        this.widget.content.searchService.clear();
        return Promise.resolve();
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfY3N2dmlld2VyLWV4dGVuc2lvbl9saWJfc2VhcmNocHJvdmlkZXJfanMuMjg1MDQxZjlkYzllNTFmNzA1NmIuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBLDBDQUEwQztBQUMxQywyREFBMkQ7QUFDVDtBQUNPO0FBQ29CO0FBTzdFOztHQUVHO0FBQ0ksTUFBTSxpQkFBa0IsU0FBUSxzRUFBaUM7SUFBeEU7O1FBK0JFOzs7O1dBSUc7UUFDTSxlQUFVLEdBQUcsSUFBSSxDQUFDO0lBbUY3QixDQUFDO0lBdEhDOzs7Ozs7Ozs7OztPQVdHO0lBQ0gsTUFBTSxDQUFDLFNBQVMsQ0FDZCxNQUF5QixFQUN6QixVQUF3QjtRQUV4QixPQUFPLElBQUksaUJBQWlCLENBQUMsTUFBTSxDQUFDLENBQUM7SUFDdkMsQ0FBQztJQUVEOztPQUVHO0lBQ0gsTUFBTSxDQUFDLFlBQVksQ0FBQyxNQUFjO1FBQ2hDLDBEQUEwRDtRQUMxRCx3REFBd0Q7UUFDeEQsT0FBTyxDQUNMLE1BQU0sWUFBWSxtRUFBYyxJQUFJLE1BQU0sQ0FBQyxPQUFPLFlBQVksNERBQVMsQ0FDeEUsQ0FBQztJQUNKLENBQUM7SUFTRDs7T0FFRztJQUNILGNBQWM7UUFDWixRQUFRO1FBQ1IsT0FBTyxPQUFPLENBQUMsT0FBTyxFQUFFLENBQUM7SUFDM0IsQ0FBQztJQUVEOzs7Ozs7T0FNRztJQUNILGFBQWEsQ0FBQyxJQUFjO1FBQzFCLElBQUksQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLGFBQWEsQ0FBQyxJQUFJLENBQUMsSUFBSSxDQUFDLE1BQU0sQ0FBQyxDQUFDO1FBQ3BELE9BQU8sT0FBTyxDQUFDLE9BQU8sQ0FBQyxTQUFTLENBQUMsQ0FBQztJQUNwQyxDQUFDO0lBRUQ7Ozs7OztPQU1HO0lBQ0gsaUJBQWlCLENBQUMsSUFBYztRQUM5QixJQUFJLENBQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxhQUFhLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxNQUFNLEVBQUUsSUFBSSxDQUFDLENBQUM7UUFDMUQsT0FBTyxPQUFPLENBQUMsT0FBTyxDQUFDLFNBQVMsQ0FBQyxDQUFDO0lBQ3BDLENBQUM7SUFFRDs7Ozs7Ozs7T0FRRztJQUNILG1CQUFtQixDQUFDLE9BQWUsRUFBRSxJQUFjO1FBQ2pELE9BQU8sT0FBTyxDQUFDLE9BQU8sQ0FBQyxLQUFLLENBQUMsQ0FBQztJQUNoQyxDQUFDO0lBRUQ7Ozs7Ozs7T0FPRztJQUNILGlCQUFpQixDQUFDLE9BQWU7UUFDL0IsT0FBTyxPQUFPLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyxDQUFDO0lBQ2hDLENBQUM7SUFFRDs7Ozs7T0FLRztJQUNILFVBQVUsQ0FBQyxLQUFhO1FBQ3RCLElBQUksQ0FBQyxNQUFNLEdBQUcsS0FBSyxDQUFDO1FBQ3BCLElBQUksQ0FBQyxNQUFNLENBQUMsT0FBTyxDQUFDLGFBQWEsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLENBQUM7UUFFOUMsT0FBTyxPQUFPLENBQUMsT0FBTyxFQUFFLENBQUM7SUFDM0IsQ0FBQztJQUVEOzs7T0FHRztJQUNILFFBQVE7UUFDTixJQUFJLENBQUMsTUFBTSxDQUFDLE9BQU8sQ0FBQyxhQUFhLENBQUMsS0FBSyxFQUFFLENBQUM7UUFFMUMsT0FBTyxPQUFPLENBQUMsT0FBTyxFQUFFLENBQUM7SUFDM0IsQ0FBQztDQUdGIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL2NzdnZpZXdlci1leHRlbnNpb24vc3JjL3NlYXJjaHByb3ZpZGVyLnRzIl0sInNvdXJjZXNDb250ZW50IjpbIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbmltcG9ydCB7IENTVlZpZXdlciB9IGZyb20gJ0BqdXB5dGVybGFiL2NzdnZpZXdlcic7XG5pbXBvcnQgeyBEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7IElTZWFyY2hQcm92aWRlciwgU2VhcmNoUHJvdmlkZXIgfSBmcm9tICdAanVweXRlcmxhYi9kb2N1bWVudHNlYXJjaCc7XG5pbXBvcnQgeyBJVHJhbnNsYXRvciB9IGZyb20gJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uJztcbmltcG9ydCB7IFdpZGdldCB9IGZyb20gJ0BsdW1pbm8vd2lkZ2V0cyc7XG5cbi8vIFRoZSB0eXBlIGZvciB3aGljaCBpc0FwcGxpY2FibGUgcmV0dXJucyB0cnVlXG5leHBvcnQgdHlwZSBDU1ZEb2N1bWVudFdpZGdldCA9IERvY3VtZW50V2lkZ2V0PENTVlZpZXdlcj47XG5cbi8qKlxuICogQ1NWIHZpZXdlciBzZWFyY2ggcHJvdmlkZXJcbiAqL1xuZXhwb3J0IGNsYXNzIENTVlNlYXJjaFByb3ZpZGVyIGV4dGVuZHMgU2VhcmNoUHJvdmlkZXI8Q1NWRG9jdW1lbnRXaWRnZXQ+IHtcbiAgLyoqXG4gICAqIEluc3RhbnRpYXRlIGEgc2VhcmNoIHByb3ZpZGVyIGZvciB0aGUgd2lkZ2V0LlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoZSB3aWRnZXQgcHJvdmlkZWQgaXMgYWx3YXlzIGNoZWNrZWQgdXNpbmcgYGlzQXBwbGljYWJsZWAgYmVmb3JlIGNhbGxpbmdcbiAgICogdGhpcyBmYWN0b3J5LlxuICAgKlxuICAgKiBAcGFyYW0gd2lkZ2V0IFRoZSB3aWRnZXQgdG8gc2VhcmNoIG9uXG4gICAqIEBwYXJhbSB0cmFuc2xhdG9yIFtvcHRpb25hbF0gVGhlIHRyYW5zbGF0b3Igb2JqZWN0XG4gICAqXG4gICAqIEByZXR1cm5zIFRoZSBzZWFyY2ggcHJvdmlkZXIgb24gdGhlIHdpZGdldFxuICAgKi9cbiAgc3RhdGljIGNyZWF0ZU5ldyhcbiAgICB3aWRnZXQ6IENTVkRvY3VtZW50V2lkZ2V0LFxuICAgIHRyYW5zbGF0b3I/OiBJVHJhbnNsYXRvclxuICApOiBJU2VhcmNoUHJvdmlkZXIge1xuICAgIHJldHVybiBuZXcgQ1NWU2VhcmNoUHJvdmlkZXIod2lkZ2V0KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXBvcnQgd2hldGhlciBvciBub3QgdGhpcyBwcm92aWRlciBoYXMgdGhlIGFiaWxpdHkgdG8gc2VhcmNoIG9uIHRoZSBnaXZlbiBvYmplY3RcbiAgICovXG4gIHN0YXRpYyBpc0FwcGxpY2FibGUoZG9tYWluOiBXaWRnZXQpOiBkb21haW4gaXMgQ1NWRG9jdW1lbnRXaWRnZXQge1xuICAgIC8vIGNoZWNrIHRvIHNlZSBpZiB0aGUgQ1NWU2VhcmNoUHJvdmlkZXIgY2FuIHNlYXJjaCBvbiB0aGVcbiAgICAvLyBmaXJzdCBjZWxsLCBmYWxzZSBpbmRpY2F0ZXMgYW5vdGhlciBlZGl0b3IgaXMgcHJlc2VudFxuICAgIHJldHVybiAoXG4gICAgICBkb21haW4gaW5zdGFuY2VvZiBEb2N1bWVudFdpZGdldCAmJiBkb21haW4uY29udGVudCBpbnN0YW5jZW9mIENTVlZpZXdlclxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IHRvIHRydWUgaWYgdGhlIHdpZGdldCB1bmRlciBzZWFyY2ggaXMgcmVhZC1vbmx5LCBmYWxzZVxuICAgKiBpZiBpdCBpcyBlZGl0YWJsZS4gIFdpbGwgYmUgdXNlZCB0byBkZXRlcm1pbmUgd2hldGhlciB0byBzaG93XG4gICAqIHRoZSByZXBsYWNlIG9wdGlvbi5cbiAgICovXG4gIHJlYWRvbmx5IGlzUmVhZE9ubHkgPSB0cnVlO1xuXG4gIC8qKlxuICAgKiBDbGVhciBjdXJyZW50bHkgaGlnaGxpZ2h0ZWQgbWF0Y2guXG4gICAqL1xuICBjbGVhckhpZ2hsaWdodCgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAvLyBuby1vcFxuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBNb3ZlIHRoZSBjdXJyZW50IG1hdGNoIGluZGljYXRvciB0byB0aGUgbmV4dCBtYXRjaC5cbiAgICpcbiAgICogQHBhcmFtIGxvb3AgV2hldGhlciB0byBsb29wIHdpdGhpbiB0aGUgbWF0Y2hlcyBsaXN0LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgbWF0Y2ggaXMgbmV2ZXIgcmV0dXJuZWQgYnkgdGhpcyBwcm92aWRlclxuICAgKi9cbiAgaGlnaGxpZ2h0TmV4dChsb29wPzogYm9vbGVhbik6IFByb21pc2U8dW5kZWZpbmVkPiB7XG4gICAgdGhpcy53aWRnZXQuY29udGVudC5zZWFyY2hTZXJ2aWNlLmZpbmQodGhpcy5fcXVlcnkpO1xuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUodW5kZWZpbmVkKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBNb3ZlIHRoZSBjdXJyZW50IG1hdGNoIGluZGljYXRvciB0byB0aGUgcHJldmlvdXMgbWF0Y2guXG4gICAqXG4gICAqIEBwYXJhbSBsb29wIFdoZXRoZXIgdG8gbG9vcCB3aXRoaW4gdGhlIG1hdGNoZXMgbGlzdC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIG1hdGNoIGlzIG5ldmVyIHJldHVybmVkIGJ5IHRoaXMgcHJvdmlkZXJcbiAgICovXG4gIGhpZ2hsaWdodFByZXZpb3VzKGxvb3A/OiBib29sZWFuKTogUHJvbWlzZTx1bmRlZmluZWQ+IHtcbiAgICB0aGlzLndpZGdldC5jb250ZW50LnNlYXJjaFNlcnZpY2UuZmluZCh0aGlzLl9xdWVyeSwgdHJ1ZSk7XG4gICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZSh1bmRlZmluZWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJlcGxhY2UgdGhlIGN1cnJlbnRseSBzZWxlY3RlZCBtYXRjaCB3aXRoIHRoZSBwcm92aWRlZCB0ZXh0XG4gICAqIE5vdCBpbXBsZW1lbnRlZCBpbiB0aGUgQ1NWIHZpZXdlciBhcyBpdCBpcyByZWFkLW9ubHkuXG4gICAqXG4gICAqIEBwYXJhbSBuZXdUZXh0IFRoZSByZXBsYWNlbWVudCB0ZXh0XG4gICAqIEBwYXJhbSBsb29wIFdoZXRoZXIgdG8gbG9vcCB3aXRoaW4gdGhlIG1hdGNoZXMgbGlzdC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgb25jZSB0aGUgYWN0aW9uIGhhcyBjb21wbGV0ZWQuXG4gICAqL1xuICByZXBsYWNlQ3VycmVudE1hdGNoKG5ld1RleHQ6IHN0cmluZywgbG9vcD86IGJvb2xlYW4pOiBQcm9taXNlPGJvb2xlYW4+IHtcbiAgICByZXR1cm4gUHJvbWlzZS5yZXNvbHZlKGZhbHNlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXBsYWNlIGFsbCBtYXRjaGVzIGluIHRoZSBub3RlYm9vayB3aXRoIHRoZSBwcm92aWRlZCB0ZXh0XG4gICAqIE5vdCBpbXBsZW1lbnRlZCBpbiB0aGUgQ1NWIHZpZXdlciBhcyBpdCBpcyByZWFkLW9ubHkuXG4gICAqXG4gICAqIEBwYXJhbSBuZXdUZXh0IFRoZSByZXBsYWNlbWVudCB0ZXh0XG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIG9uY2UgdGhlIGFjdGlvbiBoYXMgY29tcGxldGVkLlxuICAgKi9cbiAgcmVwbGFjZUFsbE1hdGNoZXMobmV3VGV4dDogc3RyaW5nKTogUHJvbWlzZTxib29sZWFuPiB7XG4gICAgcmV0dXJuIFByb21pc2UucmVzb2x2ZShmYWxzZSk7XG4gIH1cblxuICAvKipcbiAgICogSW5pdGlhbGl6ZSB0aGUgc2VhcmNoIHVzaW5nIHRoZSBwcm92aWRlZCBvcHRpb25zLiAgU2hvdWxkIHVwZGF0ZSB0aGUgVUlcbiAgICogdG8gaGlnaGxpZ2h0IGFsbCBtYXRjaGVzIGFuZCBcInNlbGVjdFwiIHdoYXRldmVyIHRoZSBmaXJzdCBtYXRjaCBzaG91bGQgYmUuXG4gICAqXG4gICAqIEBwYXJhbSBxdWVyeSBBIFJlZ0V4cCB0byBiZSB1c2UgdG8gcGVyZm9ybSB0aGUgc2VhcmNoXG4gICAqL1xuICBzdGFydFF1ZXJ5KHF1ZXJ5OiBSZWdFeHApOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0aGlzLl9xdWVyeSA9IHF1ZXJ5O1xuICAgIHRoaXMud2lkZ2V0LmNvbnRlbnQuc2VhcmNoU2VydmljZS5maW5kKHF1ZXJ5KTtcblxuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBDbGVhcnMgc3RhdGUgb2YgYSBzZWFyY2ggcHJvdmlkZXIgdG8gcHJlcGFyZSBmb3Igc3RhcnRRdWVyeSB0byBiZSBjYWxsZWRcbiAgICogaW4gb3JkZXIgdG8gc3RhcnQgYSBuZXcgcXVlcnkgb3IgcmVmcmVzaCBhbiBleGlzdGluZyBvbmUuXG4gICAqL1xuICBlbmRRdWVyeSgpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICB0aGlzLndpZGdldC5jb250ZW50LnNlYXJjaFNlcnZpY2UuY2xlYXIoKTtcblxuICAgIHJldHVybiBQcm9taXNlLnJlc29sdmUoKTtcbiAgfVxuXG4gIHByaXZhdGUgX3F1ZXJ5OiBSZWdFeHA7XG59XG4iXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=