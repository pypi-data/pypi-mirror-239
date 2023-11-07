"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_imageviewer-extension_lib_index_js-_8dca1"],{

/***/ "../packages/imageviewer-extension/lib/index.js":
/*!******************************************************!*\
  !*** ../packages/imageviewer-extension/lib/index.js ***!
  \******************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/imageviewer */ "webpack/sharing/consume/default/@jupyterlab/imageviewer/@jupyterlab/imageviewer");
/* harmony import */ var _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module imageviewer-extension
 */




/**
 * The command IDs used by the image widget plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.resetImage = 'imageviewer:reset-image';
    CommandIDs.zoomIn = 'imageviewer:zoom-in';
    CommandIDs.zoomOut = 'imageviewer:zoom-out';
    CommandIDs.flipHorizontal = 'imageviewer:flip-horizontal';
    CommandIDs.flipVertical = 'imageviewer:flip-vertical';
    CommandIDs.rotateClockwise = 'imageviewer:rotate-clockwise';
    CommandIDs.rotateCounterclockwise = 'imageviewer:rotate-counterclockwise';
    CommandIDs.invertColors = 'imageviewer:invert-colors';
})(CommandIDs || (CommandIDs = {}));
/**
 * The list of file types for images.
 */
const FILE_TYPES = ['png', 'gif', 'jpeg', 'bmp', 'ico', 'tiff'];
/**
 * The name of the factory that creates image widgets.
 */
const FACTORY = 'Image';
/**
 * The name of the factory that creates image widgets.
 */
const TEXT_FACTORY = 'Image (Text)';
/**
 * The list of file types for images with optional text modes.
 */
const TEXT_FILE_TYPES = ['svg', 'xbm'];
/**
 * The test pattern for text file types in paths.
 */
const TEXT_FILE_REGEX = new RegExp(`[.](${TEXT_FILE_TYPES.join('|')})$`);
/**
 * The image file handler extension.
 */
const plugin = {
    activate,
    description: 'Adds image viewer and provide its tracker.',
    id: '@jupyterlab/imageviewer-extension:plugin',
    provides: _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__.IImageTracker,
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the image widget extension.
 */
function activate(app, translator, palette, restorer) {
    const trans = translator.load('jupyterlab');
    const namespace = 'image-widget';
    function onWidgetCreated(sender, widget) {
        var _a, _b;
        // Notify the widget tracker if restore data needs to update.
        widget.context.pathChanged.connect(() => {
            void tracker.save(widget);
        });
        void tracker.add(widget);
        const types = app.docRegistry.getFileTypesForPath(widget.context.path);
        if (types.length > 0) {
            widget.title.icon = types[0].icon;
            widget.title.iconClass = (_a = types[0].iconClass) !== null && _a !== void 0 ? _a : '';
            widget.title.iconLabel = (_b = types[0].iconLabel) !== null && _b !== void 0 ? _b : '';
        }
    }
    const factory = new _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__.ImageViewerFactory({
        name: FACTORY,
        label: trans.__('Image'),
        modelName: 'base64',
        fileTypes: [...FILE_TYPES, ...TEXT_FILE_TYPES],
        defaultFor: FILE_TYPES,
        readOnly: true
    });
    const textFactory = new _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_2__.ImageViewerFactory({
        name: TEXT_FACTORY,
        label: trans.__('Image (Text)'),
        modelName: 'text',
        fileTypes: TEXT_FILE_TYPES,
        defaultFor: TEXT_FILE_TYPES,
        readOnly: true
    });
    [factory, textFactory].forEach(factory => {
        app.docRegistry.addWidgetFactory(factory);
        factory.widgetCreated.connect(onWidgetCreated);
    });
    const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker({
        namespace
    });
    if (restorer) {
        // Handle state restoration.
        void restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({
                path: widget.context.path,
                factory: TEXT_FILE_REGEX.test(widget.context.path)
                    ? TEXT_FACTORY
                    : FACTORY
            }),
            name: widget => widget.context.path
        });
    }
    addCommands(app, tracker, translator);
    if (palette) {
        const category = trans.__('Image Viewer');
        [
            CommandIDs.zoomIn,
            CommandIDs.zoomOut,
            CommandIDs.resetImage,
            CommandIDs.rotateClockwise,
            CommandIDs.rotateCounterclockwise,
            CommandIDs.flipHorizontal,
            CommandIDs.flipVertical,
            CommandIDs.invertColors
        ].forEach(command => {
            palette.addItem({ command, category });
        });
    }
    return tracker;
}
/**
 * Add the commands for the image widget.
 */
function addCommands(app, tracker, translator) {
    const trans = translator.load('jupyterlab');
    const { commands, shell } = app;
    /**
     * Whether there is an active image viewer.
     */
    function isEnabled() {
        return (tracker.currentWidget !== null &&
            tracker.currentWidget === shell.currentWidget);
    }
    commands.addCommand('imageviewer:zoom-in', {
        execute: zoomIn,
        label: trans.__('Zoom In'),
        isEnabled
    });
    commands.addCommand('imageviewer:zoom-out', {
        execute: zoomOut,
        label: trans.__('Zoom Out'),
        isEnabled
    });
    commands.addCommand('imageviewer:reset-image', {
        execute: resetImage,
        label: trans.__('Reset Image'),
        isEnabled
    });
    commands.addCommand('imageviewer:rotate-clockwise', {
        execute: rotateClockwise,
        label: trans.__('Rotate Clockwise'),
        isEnabled
    });
    commands.addCommand('imageviewer:rotate-counterclockwise', {
        execute: rotateCounterclockwise,
        label: trans.__('Rotate Counterclockwise'),
        isEnabled
    });
    commands.addCommand('imageviewer:flip-horizontal', {
        execute: flipHorizontal,
        label: trans.__('Flip image horizontally'),
        isEnabled
    });
    commands.addCommand('imageviewer:flip-vertical', {
        execute: flipVertical,
        label: trans.__('Flip image vertically'),
        isEnabled
    });
    commands.addCommand('imageviewer:invert-colors', {
        execute: invertColors,
        label: trans.__('Invert Colors'),
        isEnabled
    });
    function zoomIn() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.scale = widget.scale > 1 ? widget.scale + 0.5 : widget.scale * 2;
        }
    }
    function zoomOut() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.scale = widget.scale > 1 ? widget.scale - 0.5 : widget.scale / 2;
        }
    }
    function resetImage() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.scale = 1;
            widget.colorinversion = 0;
            widget.resetRotationFlip();
        }
    }
    function rotateClockwise() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.rotateClockwise();
        }
    }
    function rotateCounterclockwise() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.rotateCounterclockwise();
        }
    }
    function flipHorizontal() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.flipHorizontal();
        }
    }
    function flipVertical() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.flipVertical();
        }
    }
    function invertColors() {
        var _a;
        const widget = (_a = tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content;
        if (widget) {
            widget.colorinversion += 1;
            widget.colorinversion %= 2;
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfaW1hZ2V2aWV3ZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fOGRjYTEuNmU4MTU4NWZhNzZmZjg2YTAxOGEuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDcUM7QUFNckM7QUFDcUI7QUFFdEQ7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FnQm5CO0FBaEJELFdBQVUsVUFBVTtJQUNMLHFCQUFVLEdBQUcseUJBQXlCLENBQUM7SUFFdkMsaUJBQU0sR0FBRyxxQkFBcUIsQ0FBQztJQUUvQixrQkFBTyxHQUFHLHNCQUFzQixDQUFDO0lBRWpDLHlCQUFjLEdBQUcsNkJBQTZCLENBQUM7SUFFL0MsdUJBQVksR0FBRywyQkFBMkIsQ0FBQztJQUUzQywwQkFBZSxHQUFHLDhCQUE4QixDQUFDO0lBRWpELGlDQUFzQixHQUFHLHFDQUFxQyxDQUFDO0lBRS9ELHVCQUFZLEdBQUcsMkJBQTJCLENBQUM7QUFDMUQsQ0FBQyxFQWhCUyxVQUFVLEtBQVYsVUFBVSxRQWdCbkI7QUFFRDs7R0FFRztBQUNILE1BQU0sVUFBVSxHQUFHLENBQUMsS0FBSyxFQUFFLEtBQUssRUFBRSxNQUFNLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxNQUFNLENBQUMsQ0FBQztBQUVoRTs7R0FFRztBQUNILE1BQU0sT0FBTyxHQUFHLE9BQU8sQ0FBQztBQUV4Qjs7R0FFRztBQUNILE1BQU0sWUFBWSxHQUFHLGNBQWMsQ0FBQztBQUVwQzs7R0FFRztBQUNILE1BQU0sZUFBZSxHQUFHLENBQUMsS0FBSyxFQUFFLEtBQUssQ0FBQyxDQUFDO0FBRXZDOztHQUVHO0FBQ0gsTUFBTSxlQUFlLEdBQUcsSUFBSSxNQUFNLENBQUMsT0FBTyxlQUFlLENBQUMsSUFBSSxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBQztBQUV6RTs7R0FFRztBQUNILE1BQU0sTUFBTSxHQUF5QztJQUNuRCxRQUFR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QUFDO1NBQzVCO0lBQ0gsQ0FBQztJQUVELFNBQVMsZUFBZTs7UUFDdEIsTUFBTSxNQUFNLEdBQUcsYUFBTyxDQUFDLGFBQWEsMENBQUUsT0FBTyxDQUFDO1FBRTlDLElBQUksTUFBTSxFQUFFO1lBQ1YsTUFBTSxDQUFDLGVBQWUsRUFBRSxDQUFDO1NBQzFCO0lBQ0gsQ0FBQztJQUVELFNBQVMsc0JBQXNCOztRQUM3QixNQUFNLE1BQU0sR0FBRyxhQUFPLENBQUMsYUFBYSwwQ0FBRSxPQUFPLENBQUM7UUFFOUMsSUFBSSxNQUFNLEVBQUU7WUFDVixNQUFNLENBQUMsc0JBQXNCLEVBQUUsQ0FBQztTQUNqQztJQUNILENBQUM7SUFFRCxTQUFTLGNBQWM7O1FBQ3JCLE1BQU0sTUFBTSxHQUFHLGFBQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQztRQUU5QyxJQUFJLE1BQU0sRUFBRTtZQUNWLE1BQU0sQ0FBQyxjQUFjLEVBQUUsQ0FBQztTQUN6QjtJQUNILENBQUM7SUFFRCxTQUFTLFlBQVk7O1FBQ25CLE1BQU0sTUFBTSxHQUFHLGFBQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQztRQUU5QyxJQUFJLE1BQU0sRUFBRTtZQUNWLE1BQU0sQ0FBQyxZQUFZLEVBQUUsQ0FBQztTQUN2QjtJQUNILENBQUM7SUFFRCxTQUFTLFlBQVk7O1FBQ25CLE1BQU0sTUFBTSxHQUFHLGFBQU8sQ0FBQyxhQUFhLDBDQUFFLE9BQU8sQ0FBQztRQUU5QyxJQUFJLE1BQU0sRUFBRTtZQUNWLE1BQU0sQ0FBQyxjQUFjLElBQUksQ0FBQyxDQUFDO1lBQzNCLE1BQU0sQ0FBQyxjQUFjLElBQUksQ0FBQyxDQUFDO1NBQzVCO0lBQ0gsQ0FBQztBQUNILENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvaW1hZ2V2aWV3ZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBpbWFnZXZpZXdlci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGF5b3V0UmVzdG9yZXIsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IElDb21tYW5kUGFsZXR0ZSwgV2lkZ2V0VHJhY2tlciB9IGZyb20gJ0BqdXB5dGVybGFiL2FwcHV0aWxzJztcbmltcG9ydCB7IERvY3VtZW50UmVnaXN0cnksIElEb2N1bWVudFdpZGdldCB9IGZyb20gJ0BqdXB5dGVybGFiL2RvY3JlZ2lzdHJ5JztcbmltcG9ydCB7XG4gIElJbWFnZVRyYWNrZXIsXG4gIEltYWdlVmlld2VyLFxuICBJbWFnZVZpZXdlckZhY3Rvcnlcbn0gZnJvbSAnQGp1cHl0ZXJsYWIvaW1hZ2V2aWV3ZXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5cbi8qKlxuICogVGhlIGNvbW1hbmQgSURzIHVzZWQgYnkgdGhlIGltYWdlIHdpZGdldCBwbHVnaW4uXG4gKi9cbm5hbWVzcGFjZSBDb21tYW5kSURzIHtcbiAgZXhwb3J0IGNvbnN0IHJlc2V0SW1hZ2UgPSAnaW1hZ2V2aWV3ZXI6cmVzZXQtaW1hZ2UnO1xuXG4gIGV4cG9ydCBjb25zdCB6b29tSW4gPSAnaW1hZ2V2aWV3ZXI6em9vbS1pbic7XG5cbiAgZXhwb3J0IGNvbnN0IHpvb21PdXQgPSAnaW1hZ2V2aWV3ZXI6em9vbS1vdXQnO1xuXG4gIGV4cG9ydCBjb25zdCBmbGlwSG9yaXpvbnRhbCA9ICdpbWFnZXZpZXdlcjpmbGlwLWhvcml6b250YWwnO1xuXG4gIGV4cG9ydCBjb25zdCBmbGlwVmVydGljYWwgPSAnaW1hZ2V2aWV3ZXI6ZmxpcC12ZXJ0aWNhbCc7XG5cbiAgZXhwb3J0IGNvbnN0IHJvdGF0ZUNsb2Nrd2lzZSA9ICdpbWFnZXZpZXdlcjpyb3RhdGUtY2xvY2t3aXNlJztcblxuICBleHBvcnQgY29uc3Qgcm90YXRlQ291bnRlcmNsb2Nrd2lzZSA9ICdpbWFnZXZpZXdlcjpyb3RhdGUtY291bnRlcmNsb2Nrd2lzZSc7XG5cbiAgZXhwb3J0IGNvbnN0IGludmVydENvbG9ycyA9ICdpbWFnZXZpZXdlcjppbnZlcnQtY29sb3JzJztcbn1cblxuLyoqXG4gKiBUaGUgbGlzdCBvZiBmaWxlIHR5cGVzIGZvciBpbWFnZXMuXG4gKi9cbmNvbnN0IEZJTEVfVFlQRVMgPSBbJ3BuZycsICdnaWYnLCAnanBlZycsICdibXAnLCAnaWNvJywgJ3RpZmYnXTtcblxuLyoqXG4gKiBUaGUgbmFtZSBvZiB0aGUgZmFjdG9yeSB0aGF0IGNyZWF0ZXMgaW1hZ2Ugd2lkZ2V0cy5cbiAqL1xuY29uc3QgRkFDVE9SWSA9ICdJbWFnZSc7XG5cbi8qKlxuICogVGhlIG5hbWUgb2YgdGhlIGZhY3RvcnkgdGhhdCBjcmVhdGVzIGltYWdlIHdpZGdldHMuXG4gKi9cbmNvbnN0IFRFWFRfRkFDVE9SWSA9ICdJbWFnZSAoVGV4dCknO1xuXG4vKipcbiAqIFRoZSBsaXN0IG9mIGZpbGUgdHlwZXMgZm9yIGltYWdlcyB3aXRoIG9wdGlvbmFsIHRleHQgbW9kZXMuXG4gKi9cbmNvbnN0IFRFWFRfRklMRV9UWVBFUyA9IFsnc3ZnJywgJ3hibSddO1xuXG4vKipcbiAqIFRoZSB0ZXN0IHBhdHRlcm4gZm9yIHRleHQgZmlsZSB0eXBlcyBpbiBwYXRocy5cbiAqL1xuY29uc3QgVEVYVF9GSUxFX1JFR0VYID0gbmV3IFJlZ0V4cChgWy5dKCR7VEVYVF9GSUxFX1RZUEVTLmpvaW4oJ3wnKX0pJGApO1xuXG4vKipcbiAqIFRoZSBpbWFnZSBmaWxlIGhhbmRsZXIgZXh0ZW5zaW9uLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJSW1hZ2VUcmFja2VyPiA9IHtcbiAgYWN0aXZhdGUsXG4gIGRlc2NyaXB0aW9uOiAnQWRkcyBpbWFnZSB2aWV3ZXIgYW5kIHByb3ZpZGUgaXRzIHRyYWNrZXIuJyxcbiAgaWQ6ICdAanVweXRlcmxhYi9pbWFnZXZpZXdlci1leHRlbnNpb246cGx1Z2luJyxcbiAgcHJvdmlkZXM6IElJbWFnZVRyYWNrZXIsXG4gIHJlcXVpcmVzOiBbSVRyYW5zbGF0b3JdLFxuICBvcHRpb25hbDogW0lDb21tYW5kUGFsZXR0ZSwgSUxheW91dFJlc3RvcmVyXSxcbiAgYXV0b1N0YXJ0OiB0cnVlXG59O1xuXG4vKipcbiAqIEV4cG9ydCB0aGUgcGx1Z2luIGFzIGRlZmF1bHQuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IHBsdWdpbjtcblxuLyoqXG4gKiBBY3RpdmF0ZSB0aGUgaW1hZ2Ugd2lkZ2V0IGV4dGVuc2lvbi5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgcGFsZXR0ZTogSUNvbW1hbmRQYWxldHRlIHwgbnVsbCxcbiAgcmVzdG9yZXI6IElMYXlvdXRSZXN0b3JlciB8IG51bGxcbik6IElJbWFnZVRyYWNrZXIge1xuICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICBjb25zdCBuYW1lc3BhY2UgPSAnaW1hZ2Utd2lkZ2V0JztcblxuICBmdW5jdGlvbiBvbldpZGdldENyZWF0ZWQoXG4gICAgc2VuZGVyOiBhbnksXG4gICAgd2lkZ2V0OiBJRG9jdW1lbnRXaWRnZXQ8SW1hZ2VWaWV3ZXIsIERvY3VtZW50UmVnaXN0cnkuSU1vZGVsPlxuICApIHtcbiAgICAvLyBOb3RpZnkgdGhlIHdpZGdldCB0cmFja2VyIGlmIHJlc3RvcmUgZGF0YSBuZWVkcyB0byB1cGRhdGUuXG4gICAgd2lkZ2V0LmNvbnRleHQucGF0aENoYW5nZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICB2b2lkIHRyYWNrZXIuc2F2ZSh3aWRnZXQpO1xuICAgIH0pO1xuICAgIHZvaWQgdHJhY2tlci5hZGQod2lkZ2V0KTtcblxuICAgIGNvbnN0IHR5cGVzID0gYXBwLmRvY1JlZ2lzdHJ5LmdldEZpbGVUeXBlc0ZvclBhdGgod2lkZ2V0LmNvbnRleHQucGF0aCk7XG5cbiAgICBpZiAodHlwZXMubGVuZ3RoID4gMCkge1xuICAgICAgd2lkZ2V0LnRpdGxlLmljb24gPSB0eXBlc1swXS5pY29uITtcbiAgICAgIHdpZGdldC50aXRsZS5pY29uQ2xhc3MgPSB0eXBlc1swXS5pY29uQ2xhc3MgPz8gJyc7XG4gICAgICB3aWRnZXQudGl0bGUuaWNvbkxhYmVsID0gdHlwZXNbMF0uaWNvbkxhYmVsID8/ICcnO1xuICAgIH1cbiAgfVxuXG4gIGNvbnN0IGZhY3RvcnkgPSBuZXcgSW1hZ2VWaWV3ZXJGYWN0b3J5KHtcbiAgICBuYW1lOiBGQUNUT1JZLFxuICAgIGxhYmVsOiB0cmFucy5fXygnSW1hZ2UnKSxcbiAgICBtb2RlbE5hbWU6ICdiYXNlNjQnLFxuICAgIGZpbGVUeXBlczogWy4uLkZJTEVfVFlQRVMsIC4uLlRFWFRfRklMRV9UWVBFU10sXG4gICAgZGVmYXVsdEZvcjogRklMRV9UWVBFUyxcbiAgICByZWFkT25seTogdHJ1ZVxuICB9KTtcblxuICBjb25zdCB0ZXh0RmFjdG9yeSA9IG5ldyBJbWFnZVZpZXdlckZhY3Rvcnkoe1xuICAgIG5hbWU6IFRFWFRfRkFDVE9SWSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0ltYWdlIChUZXh0KScpLFxuICAgIG1vZGVsTmFtZTogJ3RleHQnLFxuICAgIGZpbGVUeXBlczogVEVYVF9GSUxFX1RZUEVTLFxuICAgIGRlZmF1bHRGb3I6IFRFWFRfRklMRV9UWVBFUyxcbiAgICByZWFkT25seTogdHJ1ZVxuICB9KTtcblxuICBbZmFjdG9yeSwgdGV4dEZhY3RvcnldLmZvckVhY2goZmFjdG9yeSA9PiB7XG4gICAgYXBwLmRvY1JlZ2lzdHJ5LmFkZFdpZGdldEZhY3RvcnkoZmFjdG9yeSk7XG4gICAgZmFjdG9yeS53aWRnZXRDcmVhdGVkLmNvbm5lY3Qob25XaWRnZXRDcmVhdGVkKTtcbiAgfSk7XG5cbiAgY29uc3QgdHJhY2tlciA9IG5ldyBXaWRnZXRUcmFja2VyPElEb2N1bWVudFdpZGdldDxJbWFnZVZpZXdlcj4+KHtcbiAgICBuYW1lc3BhY2VcbiAgfSk7XG5cbiAgaWYgKHJlc3RvcmVyKSB7XG4gICAgLy8gSGFuZGxlIHN0YXRlIHJlc3RvcmF0aW9uLlxuICAgIHZvaWQgcmVzdG9yZXIucmVzdG9yZSh0cmFja2VyLCB7XG4gICAgICBjb21tYW5kOiAnZG9jbWFuYWdlcjpvcGVuJyxcbiAgICAgIGFyZ3M6IHdpZGdldCA9PiAoe1xuICAgICAgICBwYXRoOiB3aWRnZXQuY29udGV4dC5wYXRoLFxuICAgICAgICBmYWN0b3J5OiBURVhUX0ZJTEVfUkVHRVgudGVzdCh3aWRnZXQuY29udGV4dC5wYXRoKVxuICAgICAgICAgID8gVEVYVF9GQUNUT1JZXG4gICAgICAgICAgOiBGQUNUT1JZXG4gICAgICB9KSxcbiAgICAgIG5hbWU6IHdpZGdldCA9PiB3aWRnZXQuY29udGV4dC5wYXRoXG4gICAgfSk7XG4gIH1cblxuICBhZGRDb21tYW5kcyhhcHAsIHRyYWNrZXIsIHRyYW5zbGF0b3IpO1xuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgY29uc3QgY2F0ZWdvcnkgPSB0cmFucy5fXygnSW1hZ2UgVmlld2VyJyk7XG4gICAgW1xuICAgICAgQ29tbWFuZElEcy56b29tSW4sXG4gICAgICBDb21tYW5kSURzLnpvb21PdXQsXG4gICAgICBDb21tYW5kSURzLnJlc2V0SW1hZ2UsXG4gICAgICBDb21tYW5kSURzLnJvdGF0ZUNsb2Nrd2lzZSxcbiAgICAgIENvbW1hbmRJRHMucm90YXRlQ291bnRlcmNsb2Nrd2lzZSxcbiAgICAgIENvbW1hbmRJRHMuZmxpcEhvcml6b250YWwsXG4gICAgICBDb21tYW5kSURzLmZsaXBWZXJ0aWNhbCxcbiAgICAgIENvbW1hbmRJRHMuaW52ZXJ0Q29sb3JzXG4gICAgXS5mb3JFYWNoKGNvbW1hbmQgPT4ge1xuICAgICAgcGFsZXR0ZS5hZGRJdGVtKHsgY29tbWFuZCwgY2F0ZWdvcnkgfSk7XG4gICAgfSk7XG4gIH1cblxuICByZXR1cm4gdHJhY2tlcjtcbn1cblxuLyoqXG4gKiBBZGQgdGhlIGNvbW1hbmRzIGZvciB0aGUgaW1hZ2Ugd2lkZ2V0LlxuICovXG5mdW5jdGlvbiBhZGRDb21tYW5kcyhcbiAgYXBwOiBKdXB5dGVyRnJvbnRFbmQsXG4gIHRyYWNrZXI6IElJbWFnZVRyYWNrZXIsXG4gIHRyYW5zbGF0b3I6IElUcmFuc2xhdG9yXG4pOiB2b2lkIHtcbiAgY29uc3QgdHJhbnMgPSB0cmFuc2xhdG9yLmxvYWQoJ2p1cHl0ZXJsYWInKTtcbiAgY29uc3QgeyBjb21tYW5kcywgc2hlbGwgfSA9IGFwcDtcblxuICAvKipcbiAgICogV2hldGhlciB0aGVyZSBpcyBhbiBhY3RpdmUgaW1hZ2Ugdmlld2VyLlxuICAgKi9cbiAgZnVuY3Rpb24gaXNFbmFibGVkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiAoXG4gICAgICB0cmFja2VyLmN1cnJlbnRXaWRnZXQgIT09IG51bGwgJiZcbiAgICAgIHRyYWNrZXIuY3VycmVudFdpZGdldCA9PT0gc2hlbGwuY3VycmVudFdpZGdldFxuICAgICk7XG4gIH1cblxuICBjb21tYW5kcy5hZGRDb21tYW5kKCdpbWFnZXZpZXdlcjp6b29tLWluJywge1xuICAgIGV4ZWN1dGU6IHpvb21JbixcbiAgICBsYWJlbDogdHJhbnMuX18oJ1pvb20gSW4nKSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZCgnaW1hZ2V2aWV3ZXI6em9vbS1vdXQnLCB7XG4gICAgZXhlY3V0ZTogem9vbU91dCxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1pvb20gT3V0JyksXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoJ2ltYWdldmlld2VyOnJlc2V0LWltYWdlJywge1xuICAgIGV4ZWN1dGU6IHJlc2V0SW1hZ2UsXG4gICAgbGFiZWw6IHRyYW5zLl9fKCdSZXNldCBJbWFnZScpLFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKCdpbWFnZXZpZXdlcjpyb3RhdGUtY2xvY2t3aXNlJywge1xuICAgIGV4ZWN1dGU6IHJvdGF0ZUNsb2Nrd2lzZSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1JvdGF0ZSBDbG9ja3dpc2UnKSxcbiAgICBpc0VuYWJsZWRcbiAgfSk7XG5cbiAgY29tbWFuZHMuYWRkQ29tbWFuZCgnaW1hZ2V2aWV3ZXI6cm90YXRlLWNvdW50ZXJjbG9ja3dpc2UnLCB7XG4gICAgZXhlY3V0ZTogcm90YXRlQ291bnRlcmNsb2Nrd2lzZSxcbiAgICBsYWJlbDogdHJhbnMuX18oJ1JvdGF0ZSBDb3VudGVyY2xvY2t3aXNlJyksXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoJ2ltYWdldmlld2VyOmZsaXAtaG9yaXpvbnRhbCcsIHtcbiAgICBleGVjdXRlOiBmbGlwSG9yaXpvbnRhbCxcbiAgICBsYWJlbDogdHJhbnMuX18oJ0ZsaXAgaW1hZ2UgaG9yaXpvbnRhbGx5JyksXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoJ2ltYWdldmlld2VyOmZsaXAtdmVydGljYWwnLCB7XG4gICAgZXhlY3V0ZTogZmxpcFZlcnRpY2FsLFxuICAgIGxhYmVsOiB0cmFucy5fXygnRmxpcCBpbWFnZSB2ZXJ0aWNhbGx5JyksXG4gICAgaXNFbmFibGVkXG4gIH0pO1xuXG4gIGNvbW1hbmRzLmFkZENvbW1hbmQoJ2ltYWdldmlld2VyOmludmVydC1jb2xvcnMnLCB7XG4gICAgZXhlY3V0ZTogaW52ZXJ0Q29sb3JzLFxuICAgIGxhYmVsOiB0cmFucy5fXygnSW52ZXJ0IENvbG9ycycpLFxuICAgIGlzRW5hYmxlZFxuICB9KTtcblxuICBmdW5jdGlvbiB6b29tSW4oKTogdm9pZCB7XG4gICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgaWYgKHdpZGdldCkge1xuICAgICAgd2lkZ2V0LnNjYWxlID0gd2lkZ2V0LnNjYWxlID4gMSA/IHdpZGdldC5zY2FsZSArIDAuNSA6IHdpZGdldC5zY2FsZSAqIDI7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gem9vbU91dCgpOiB2b2lkIHtcbiAgICBjb25zdCB3aWRnZXQgPSB0cmFja2VyLmN1cnJlbnRXaWRnZXQ/LmNvbnRlbnQ7XG5cbiAgICBpZiAod2lkZ2V0KSB7XG4gICAgICB3aWRnZXQuc2NhbGUgPSB3aWRnZXQuc2NhbGUgPiAxID8gd2lkZ2V0LnNjYWxlIC0gMC41IDogd2lkZ2V0LnNjYWxlIC8gMjtcbiAgICB9XG4gIH1cblxuICBmdW5jdGlvbiByZXNldEltYWdlKCk6IHZvaWQge1xuICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgIGlmICh3aWRnZXQpIHtcbiAgICAgIHdpZGdldC5zY2FsZSA9IDE7XG4gICAgICB3aWRnZXQuY29sb3JpbnZlcnNpb24gPSAwO1xuICAgICAgd2lkZ2V0LnJlc2V0Um90YXRpb25GbGlwKCk7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gcm90YXRlQ2xvY2t3aXNlKCk6IHZvaWQge1xuICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgIGlmICh3aWRnZXQpIHtcbiAgICAgIHdpZGdldC5yb3RhdGVDbG9ja3dpc2UoKTtcbiAgICB9XG4gIH1cblxuICBmdW5jdGlvbiByb3RhdGVDb3VudGVyY2xvY2t3aXNlKCk6IHZvaWQge1xuICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgIGlmICh3aWRnZXQpIHtcbiAgICAgIHdpZGdldC5yb3RhdGVDb3VudGVyY2xvY2t3aXNlKCk7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gZmxpcEhvcml6b250YWwoKTogdm9pZCB7XG4gICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgaWYgKHdpZGdldCkge1xuICAgICAgd2lkZ2V0LmZsaXBIb3Jpem9udGFsKCk7XG4gICAgfVxuICB9XG5cbiAgZnVuY3Rpb24gZmxpcFZlcnRpY2FsKCk6IHZvaWQge1xuICAgIGNvbnN0IHdpZGdldCA9IHRyYWNrZXIuY3VycmVudFdpZGdldD8uY29udGVudDtcblxuICAgIGlmICh3aWRnZXQpIHtcbiAgICAgIHdpZGdldC5mbGlwVmVydGljYWwoKTtcbiAgICB9XG4gIH1cblxuICBmdW5jdGlvbiBpbnZlcnRDb2xvcnMoKTogdm9pZCB7XG4gICAgY29uc3Qgd2lkZ2V0ID0gdHJhY2tlci5jdXJyZW50V2lkZ2V0Py5jb250ZW50O1xuXG4gICAgaWYgKHdpZGdldCkge1xuICAgICAgd2lkZ2V0LmNvbG9yaW52ZXJzaW9uICs9IDE7XG4gICAgICB3aWRnZXQuY29sb3JpbnZlcnNpb24gJT0gMjtcbiAgICB9XG4gIH1cbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==