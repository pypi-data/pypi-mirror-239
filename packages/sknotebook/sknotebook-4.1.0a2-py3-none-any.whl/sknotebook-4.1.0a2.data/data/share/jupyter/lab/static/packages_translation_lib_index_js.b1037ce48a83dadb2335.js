"use strict";
(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_translation_lib_index_js"],{

/***/ "../packages/translation/lib/base.js":
/*!*******************************************!*\
  !*** ../packages/translation/lib/base.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "nullTranslator": () => (/* binding */ nullTranslator)
/* harmony export */ });
/* harmony import */ var _gettext__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./gettext */ "../packages/translation/lib/gettext.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A translator that loads a dummy language bundle that returns the same input
 * strings.
 */
class NullTranslator {
    constructor(bundle) {
        this.languageCode = 'en';
        this._languageBundle = bundle;
    }
    load(domain) {
        return this._languageBundle;
    }
}
/**
 * A language bundle that returns the same input strings.
 */
class NullLanguageBundle {
    __(msgid, ...args) {
        return this.gettext(msgid, ...args);
    }
    _n(msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
    _p(msgctxt, msgid, ...args) {
        return this.pgettext(msgctxt, msgid, ...args);
    }
    _np(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.npgettext(msgctxt, msgid, msgid_plural, n, ...args);
    }
    gettext(msgid, ...args) {
        return _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext.strfmt(msgid, ...args);
    }
    ngettext(msgid, msgid_plural, n, ...args) {
        return _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext.strfmt(n == 1 ? msgid : msgid_plural, ...[n].concat(args));
    }
    pgettext(msgctxt, msgid, ...args) {
        return _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext.strfmt(msgid, ...args);
    }
    npgettext(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
    dcnpgettext(domain, msgctxt, msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
}
/**
 * The application null translator instance that just returns the same text.
 * Also provides interpolation.
 */
const nullTranslator = new NullTranslator(new NullLanguageBundle());


/***/ }),

/***/ "../packages/translation/lib/gettext.js":
/*!**********************************************!*\
  !*** ../packages/translation/lib/gettext.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Gettext": () => (/* binding */ Gettext)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "../packages/translation/lib/utils.js");
/* ----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|
| Base gettext.js implementation.
| Copyright (c) Guillaume Potier.
| Distributed under the terms of the Modified MIT License.
| See: https://github.com/guillaumepotier/gettext.js
|
| Type definitions.
| Copyright (c) Julien Crouzet and Florian Schwingenschlögl.
| Distributed under the terms of the Modified MIT License.
| See: https://github.com/DefinitelyTyped/DefinitelyTyped
|----------------------------------------------------------------------------*/

/**
 * Gettext class providing localization methods.
 */
class Gettext {
    constructor(options) {
        options = options || {};
        // default values that could be overridden in Gettext() constructor
        this._defaults = {
            domain: 'messages',
            locale: document.documentElement.getAttribute('lang') || 'en',
            pluralFunc: function (n) {
                return { nplurals: 2, plural: n != 1 ? 1 : 0 };
            },
            contextDelimiter: String.fromCharCode(4),
            stringsPrefix: ''
        };
        // Ensure the correct separator is used
        this._locale = (options.locale || this._defaults.locale).replace('_', '-');
        this._domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(options.domain || this._defaults.domain);
        this._contextDelimiter =
            options.contextDelimiter || this._defaults.contextDelimiter;
        this._stringsPrefix = options.stringsPrefix || this._defaults.stringsPrefix;
        this._pluralFuncs = {};
        this._dictionary = {};
        this._pluralForms = {};
        if (options.messages) {
            this._dictionary[this._domain] = {};
            this._dictionary[this._domain][this._locale] = options.messages;
        }
        if (options.pluralForms) {
            this._pluralForms[this._locale] = options.pluralForms;
        }
    }
    /**
     * Set current context delimiter.
     *
     * @param delimiter - The delimiter to set.
     */
    setContextDelimiter(delimiter) {
        this._contextDelimiter = delimiter;
    }
    /**
     * Get current context delimiter.
     *
     * @returns The current delimiter.
     */
    getContextDelimiter() {
        return this._contextDelimiter;
    }
    /**
     * Set current locale.
     *
     * @param locale - The locale to set.
     */
    setLocale(locale) {
        this._locale = locale.replace('_', '-');
    }
    /**
     * Get current locale.
     *
     * @returns The current locale.
     */
    getLocale() {
        return this._locale;
    }
    /**
     * Set current domain.
     *
     * @param domain - The domain to set.
     */
    setDomain(domain) {
        this._domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain);
    }
    /**
     * Get current domain.
     *
     * @returns The current domain string.
     */
    getDomain() {
        return this._domain;
    }
    /**
     * Set current strings prefix.
     *
     * @param prefix - The string prefix to set.
     */
    setStringsPrefix(prefix) {
        this._stringsPrefix = prefix;
    }
    /**
     * Get current strings prefix.
     *
     * @returns The strings prefix.
     */
    getStringsPrefix() {
        return this._stringsPrefix;
    }
    /**
     * `sprintf` equivalent, takes a string and some arguments to make a
     * computed string.
     *
     * @param fmt - The string to interpolate.
     * @param args - The variables to use in interpolation.
     *
     * ### Examples
     * strfmt("%1 dogs are in %2", 7, "the kitchen"); => "7 dogs are in the kitchen"
     * strfmt("I like %1, bananas and %1", "apples"); => "I like apples, bananas and apples"
     */
    static strfmt(fmt, ...args) {
        return (fmt
            // put space after double % to prevent placeholder replacement of such matches
            .replace(/%%/g, '%% ')
            // replace placeholders
            .replace(/%(\d+)/g, function (str, p1) {
            return args[p1 - 1];
        })
            // replace double % and space with single %
            .replace(/%% /g, '%'));
    }
    /**
     * Load json translations strings (In Jed 2.x format).
     *
     * @param jsonData - The translation strings plus metadata.
     * @param domain - The translation domain, e.g. "jupyterlab".
     */
    loadJSON(jsonData, domain) {
        if (!jsonData[''] ||
            !jsonData['']['language'] ||
            !jsonData['']['pluralForms']) {
            throw new Error(`Wrong jsonData, it must have an empty key ("") with "language" and "pluralForms" information: ${jsonData}`);
        }
        domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain);
        let headers = jsonData[''];
        let jsonDataCopy = JSON.parse(JSON.stringify(jsonData));
        delete jsonDataCopy[''];
        this.setMessages(domain || this._defaults.domain, headers['language'], jsonDataCopy, headers['pluralForms']);
    }
    /**
     * Shorthand for gettext.
     *
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @returns A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    __(msgid, ...args) {
        return this.gettext(msgid, ...args);
    }
    /**
     * Shorthand for ngettext.
     *
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation.
     *
     * @returns A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    _n(msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
    /**
     * Shorthand for pgettext.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @returns A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    _p(msgctxt, msgid, ...args) {
        return this.pgettext(msgctxt, msgid, ...args);
    }
    /**
     * Shorthand for npgettext.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation.
     *
     * @returns A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    _np(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.npgettext(msgctxt, msgid, msgid_plural, n, ...args);
    }
    /**
     * Translate a singular string with extra interpolation values.
     *
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @returns A translated string if found, or the original string.
     */
    gettext(msgid, ...args) {
        return this.dcnpgettext('', '', msgid, '', 0, ...args);
    }
    /**
     * Translate a plural string with extra interpolation values.
     *
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @returns A translated string if found, or the original string.
     */
    ngettext(msgid, msgid_plural, n, ...args) {
        return this.dcnpgettext('', '', msgid, msgid_plural, n, ...args);
    }
    /**
     * Translate a contextualized singular string with extra interpolation values.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @returns A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    pgettext(msgctxt, msgid, ...args) {
        return this.dcnpgettext('', msgctxt, msgid, '', 0, ...args);
    }
    /**
     * Translate a contextualized plural string with extra interpolation values.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation
     *
     * @returns A translated string if found, or the original string.
     */
    npgettext(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.dcnpgettext('', msgctxt, msgid, msgid_plural, n, ...args);
    }
    /**
     * Translate a singular string with extra interpolation values.
     *
     * @param domain - The translations domain.
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation
     *
     * @returns A translated string if found, or the original string.
     */
    dcnpgettext(domain, msgctxt, msgid, msgid_plural, n, ...args) {
        domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain) || this._domain;
        let translation;
        let key = msgctxt
            ? msgctxt + this._contextDelimiter + msgid
            : msgid;
        let options = { pluralForm: false };
        let exist = false;
        let locale = this._locale;
        let locales = this.expandLocale(this._locale);
        for (let i in locales) {
            locale = locales[i];
            exist =
                this._dictionary[domain] &&
                    this._dictionary[domain][locale] &&
                    this._dictionary[domain][locale][key];
            // check condition are valid (.length)
            // because it's not possible to define both a singular and a plural form of the same msgid,
            // we need to check that the stored form is the same as the expected one.
            // if not, we'll just ignore the translation and consider it as not translated.
            if (msgid_plural) {
                exist = exist && this._dictionary[domain][locale][key].length > 1;
            }
            else {
                exist = exist && this._dictionary[domain][locale][key].length == 1;
            }
            if (exist) {
                // This ensures that a variation is used.
                options.locale = locale;
                break;
            }
        }
        if (!exist) {
            translation = [msgid];
            options.pluralFunc = this._defaults.pluralFunc;
        }
        else {
            translation = this._dictionary[domain][locale][key];
        }
        // Singular form
        if (!msgid_plural) {
            return this.t(translation, n, options, ...args);
        }
        // Plural one
        options.pluralForm = true;
        let value = exist ? translation : [msgid, msgid_plural];
        return this.t(value, n, options, ...args);
    }
    /**
     * Split a locale into parent locales. "es-CO" -> ["es-CO", "es"]
     *
     * @param locale - The locale string.
     *
     * @returns An array of locales.
     */
    expandLocale(locale) {
        let locales = [locale];
        let i = locale.lastIndexOf('-');
        while (i > 0) {
            locale = locale.slice(0, i);
            locales.push(locale);
            i = locale.lastIndexOf('-');
        }
        return locales;
    }
    /**
     * Split a locale into parent locales. "es-CO" -> ["es-CO", "es"]
     *
     * @param pluralForm - Plural form string..
     * @returns An function to compute plural forms.
     */
    // eslint-disable-next-line @typescript-eslint/ban-types
    getPluralFunc(pluralForm) {
        // Plural form string regexp
        // taken from https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
        // plural forms list available here http://localization-guide.readthedocs.org/en/latest/l10n/pluralforms.html
        let pf_re = new RegExp('^\\s*nplurals\\s*=\\s*[0-9]+\\s*;\\s*plural\\s*=\\s*(?:\\s|[-\\?\\|&=!<>+*/%:;n0-9_()])+');
        if (!pf_re.test(pluralForm))
            throw new Error(Gettext.strfmt('The plural form "%1" is not valid', pluralForm));
        // Careful here, this is a hidden eval() equivalent..
        // Risk should be reasonable though since we test the pluralForm through regex before
        // taken from https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
        // TODO: should test if https://github.com/soney/jsep present and use it if so
        return new Function('n', 'let plural, nplurals; ' +
            pluralForm +
            ' return { nplurals: nplurals, plural: (plural === true ? 1 : (plural ? plural : 0)) };');
    }
    /**
     * Remove the context delimiter from string.
     *
     * @param str - Translation string.
     * @returns A translation string without context.
     */
    removeContext(str) {
        // if there is context, remove it
        if (str.indexOf(this._contextDelimiter) !== -1) {
            let parts = str.split(this._contextDelimiter);
            return parts[1];
        }
        return str;
    }
    /**
     * Proper translation function that handle plurals and directives.
     *
     * @param messages - List of translation strings.
     * @param n - The number for pluralization.
     * @param options - Translation options.
     * @param args - Any variables to interpolate.
     *
     * @returns A translation string without context.
     *
     * ### Notes
     * Contains juicy parts of https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
     */
    t(messages, n, options, ...args) {
        // Singular is very easy, just pass dictionary message through strfmt
        if (!options.pluralForm)
            return (this._stringsPrefix +
                Gettext.strfmt(this.removeContext(messages[0]), ...args));
        let plural;
        // if a plural func is given, use that one
        if (options.pluralFunc) {
            plural = options.pluralFunc(n);
            // if plural form never interpreted before, do it now and store it
        }
        else if (!this._pluralFuncs[options.locale || '']) {
            this._pluralFuncs[options.locale || ''] = this.getPluralFunc(this._pluralForms[options.locale || '']);
            plural = this._pluralFuncs[options.locale || ''](n);
            // we have the plural function, compute the plural result
        }
        else {
            plural = this._pluralFuncs[options.locale || ''](n);
        }
        // If there is a problem with plurals, fallback to singular one
        if ('undefined' === typeof !plural.plural ||
            plural.plural > plural.nplurals ||
            messages.length <= plural.plural)
            plural.plural = 0;
        return (this._stringsPrefix +
            Gettext.strfmt(this.removeContext(messages[plural.plural]), ...[n].concat(args)));
    }
    /**
     * Set messages after loading them.
     *
     * @param domain - The translation domain.
     * @param locale - The translation locale.
     * @param messages - List of translation strings.
     * @param pluralForms - Plural form string.
     *
     * ### Notes
     * Contains juicy parts of https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
     */
    setMessages(domain, locale, messages, pluralForms) {
        domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain);
        if (pluralForms)
            this._pluralForms[locale] = pluralForms;
        if (!this._dictionary[domain])
            this._dictionary[domain] = {};
        this._dictionary[domain][locale] = messages;
    }
}



/***/ }),

/***/ "../packages/translation/lib/index.js":
/*!********************************************!*\
  !*** ../packages/translation/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Gettext": () => (/* reexport safe */ _gettext__WEBPACK_IMPORTED_MODULE_1__.Gettext),
/* harmony export */   "ITranslator": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.ITranslator),
/* harmony export */   "ITranslatorConnector": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.ITranslatorConnector),
/* harmony export */   "TranslationManager": () => (/* reexport safe */ _manager__WEBPACK_IMPORTED_MODULE_2__.TranslationManager),
/* harmony export */   "TranslatorConnector": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.TranslatorConnector),
/* harmony export */   "nullTranslator": () => (/* reexport safe */ _base__WEBPACK_IMPORTED_MODULE_0__.nullTranslator),
/* harmony export */   "requestTranslationsAPI": () => (/* reexport safe */ _server__WEBPACK_IMPORTED_MODULE_3__.requestTranslationsAPI)
/* harmony export */ });
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base */ "../packages/translation/lib/base.js");
/* harmony import */ var _gettext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./gettext */ "../packages/translation/lib/gettext.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./manager */ "../packages/translation/lib/manager.js");
/* harmony import */ var _server__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./server */ "../packages/translation/lib/server.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokens */ "../packages/translation/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module translation
 */
// Note: keep in alphabetical order...







/***/ }),

/***/ "../packages/translation/lib/manager.js":
/*!**********************************************!*\
  !*** ../packages/translation/lib/manager.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TranslationManager": () => (/* binding */ TranslationManager)
/* harmony export */ });
/* harmony import */ var _gettext__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./gettext */ "../packages/translation/lib/gettext.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../packages/translation/lib/tokens.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "../packages/translation/lib/utils.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Translation Manager
 */
class TranslationManager {
    constructor(translationsUrl = '', stringsPrefix, serverSettings) {
        this._domainData = {};
        this._translationBundles = {};
        this._connector = new _tokens__WEBPACK_IMPORTED_MODULE_1__.TranslatorConnector(translationsUrl, serverSettings);
        this._stringsPrefix = stringsPrefix || '';
        this._englishBundle = new _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext({ stringsPrefix: this._stringsPrefix });
    }
    get languageCode() {
        return this._currentLocale;
    }
    /**
     * Fetch the localization data from the server.
     *
     * @param locale The language locale to use for translations.
     */
    async fetch(locale) {
        var _a, _b, _c, _d;
        this._languageData = await this._connector.fetch({ language: locale });
        if (this._languageData && locale === 'default') {
            try {
                for (const lang of Object.values((_a = this._languageData.data) !== null && _a !== void 0 ? _a : {})) {
                    this._currentLocale =
                        // If the language is provided by the system set up, we need to retrieve the final
                        // language. This is done through the `""` entry in `_languageData` that contains
                        // language metadata.
                        lang['']['language'].replace('_', '-');
                    break;
                }
            }
            catch (reason) {
                this._currentLocale = 'en';
            }
        }
        else {
            this._currentLocale = locale;
        }
        this._domainData = (_c = (_b = this._languageData) === null || _b === void 0 ? void 0 : _b.data) !== null && _c !== void 0 ? _c : {};
        const message = (_d = this._languageData) === null || _d === void 0 ? void 0 : _d.message;
        if (message && locale !== 'en') {
            console.warn(message);
        }
    }
    /**
     * Load translation bundles for a given domain.
     *
     * @param domain The translation domain to use for translations.
     */
    load(domain) {
        if (this._domainData) {
            if (this._currentLocale == 'en') {
                return this._englishBundle;
            }
            else {
                domain = (0,_utils__WEBPACK_IMPORTED_MODULE_2__.normalizeDomain)(domain);
                if (!(domain in this._translationBundles)) {
                    let translationBundle = new _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext({
                        domain: domain,
                        locale: this._currentLocale,
                        stringsPrefix: this._stringsPrefix
                    });
                    if (domain in this._domainData) {
                        let metadata = this._domainData[domain][''];
                        if ('plural_forms' in metadata) {
                            metadata.pluralForms = metadata.plural_forms;
                            delete metadata.plural_forms;
                            this._domainData[domain][''] = metadata;
                        }
                        translationBundle.loadJSON(this._domainData[domain], domain);
                    }
                    this._translationBundles[domain] = translationBundle;
                }
                return this._translationBundles[domain];
            }
        }
        else {
            return this._englishBundle;
        }
    }
}


/***/ }),

/***/ "../packages/translation/lib/server.js":
/*!*********************************************!*\
  !*** ../packages/translation/lib/server.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestTranslationsAPI": () => (/* binding */ requestTranslationsAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The url for the translations service.
 */
const TRANSLATIONS_SETTINGS_URL = 'api/translations';
/**
 * Call the API extension
 *
 * @param locale API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestTranslationsAPI(translationsUrl = '', locale = '', init = {}, serverSettings = undefined) {
    // Make request to Jupyter API
    const settings = serverSettings !== null && serverSettings !== void 0 ? serverSettings : _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    translationsUrl =
        translationsUrl || `${settings.appUrl}/${TRANSLATIONS_SETTINGS_URL}`;
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, translationsUrl, locale);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.error('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "../packages/translation/lib/tokens.js":
/*!*********************************************!*\
  !*** ../packages/translation/lib/tokens.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITranslator": () => (/* binding */ ITranslator),
/* harmony export */   "ITranslatorConnector": () => (/* binding */ ITranslatorConnector),
/* harmony export */   "TranslatorConnector": () => (/* binding */ TranslatorConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _server__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./server */ "../packages/translation/lib/server.js");
/* ----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



/**
 * A service to connect to the server translation endpoint
 */
const ITranslatorConnector = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('@jupyterlab/translation:ITranslatorConnector', 'A service to connect to the server translation endpoint.');
class TranslatorConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    constructor(translationsUrl = '', serverSettings) {
        super();
        this._translationsUrl = translationsUrl;
        this._serverSettings = serverSettings;
    }
    async fetch(opts) {
        return (0,_server__WEBPACK_IMPORTED_MODULE_2__.requestTranslationsAPI)(this._translationsUrl, opts.language, {}, this._serverSettings);
    }
}
/**
 * Translation provider token
 */
const ITranslator = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('@jupyterlab/translation:ITranslator', 'A service to translate strings.');


/***/ }),

/***/ "../packages/translation/lib/utils.js":
/*!********************************************!*\
  !*** ../packages/translation/lib/utils.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "normalizeDomain": () => (/* binding */ normalizeDomain)
/* harmony export */ });
/*
 * Copyright (c) Jupyter Development Team.
 * Distributed under the terms of the Modified BSD License.
 */
/**
 * Normalize domain
 *
 * @param domain Domain to normalize
 * @returns Normalized domain
 */
function normalizeDomain(domain) {
    return domain.replace('-', '_');
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoicGFja2FnZXNfdHJhbnNsYXRpb25fbGliX2luZGV4X2pzLmIxMDM3Y2U0OGE4M2RhZGIyMzM1LmpzIiwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUV2QjtBQUdwQzs7O0dBR0c7QUFDSCxNQUFNLGNBQWM7SUFDbEIsWUFBWSxNQUF5QjtRQUk1QixpQkFBWSxHQUFXLElBQUksQ0FBQztRQUhuQyxJQUFJLENBQUMsZUFBZSxHQUFHLE1BQU0sQ0FBQztJQUNoQyxDQUFDO0lBSUQsSUFBSSxDQUFDLE1BQWM7UUFDakIsT0FBTyxJQUFJLENBQUMsZUFBZSxDQUFDO0lBQzlCLENBQUM7Q0FHRjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxrQkFBa0I7SUFDdEIsRUFBRSxDQUFDLEtBQWEsRUFBRSxHQUFHLElBQVc7UUFDOUIsT0FBTyxJQUFJLENBQUMsT0FBTyxDQUFDLEtBQUssRUFBRSxHQUFHLElBQUksQ0FBQyxDQUFDO0lBQ3RDLENBQUM7SUFFRCxFQUFFLENBQUMsS0FBYSxFQUFFLFlBQW9CLEVBQUUsQ0FBUyxFQUFFLEdBQUcsSUFBVztRQUMvRCxPQUFPLElBQUksQ0FBQyxRQUFRLENBQUMsS0FBSyxFQUFFLFlBQVksRUFBRSxDQUFDLEVBQUUsR0FBRyxJQUFJLENBQUMsQ0FBQztJQUN4RCxDQUFDO0lBRUQsRUFBRSxDQUFDLE9BQWUsRUFBRSxLQUFhLEVBQUUsR0FBRyxJQUFXO1FBQy9DLE9BQU8sSUFBSSxDQUFDLFFBQVEsQ0FBQyxPQUFPLEVBQUUsS0FBSyxFQUFFLEdBQUcsSUFBSSxDQUFDLENBQUM7SUFDaEQsQ0FBQztJQUVELEdBQUcsQ0FDRCxPQUFlLEVBQ2YsS0FBYSxFQUNiLFlBQW9CLEVBQ3BCLENBQVMsRUFDVCxHQUFHLElBQVc7UUFFZCxPQUFPLElBQUksQ0FBQyxTQUFTLENBQUMsT0FBTyxFQUFFLEtBQUssRUFBRSxZQUFZLEVBQUUsQ0FBQyxFQUFFLEdBQUcsSUFBSSxDQUFDLENBQUM7SUFDbEUsQ0FB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QUMxQjtBQUNRO0FBYWxEOztHQUVHO0FBQ0ksTUFBTSxvQkFBb0IsR0FBRyxJQUFJLG9EQUFLLENBQzNDLDhDQUE4QyxFQUM5QywwREFBMEQsQ0FDM0QsQ0FBQztBQUVLLE1BQU0sbUJBQ1gsU0FBUSw4REFBdUQ7SUFHL0QsWUFDRSxrQkFBMEIsRUFBRSxFQUM1QixjQUEyQztRQUUzQyxLQUFLLEVBQUUsQ0FBQztRQUNSLElBQUksQ0FBQyxnQkFBZ0IsR0FBRyxlQUFlLENBQUM7UUFDeEMsSUFBSSxDQUFDLGVBQWUsR0FBRyxjQUFjLENBQUM7SUFDeEMsQ0FBQztJQUVELEtBQUssQ0FBQyxLQUFLLENBQUMsSUFBMEI7UUFDcEMsT0FBTywrREFBc0IsQ0FDM0IsSUFBSSxDQUFDLGdCQUFnQixFQUNyQixJQUFJLENBQUMsUUFBUSxFQUNiLEVBQUUsRUFDRixJQUFJLENBQUMsZUFBZSxDQUNyQixDQUFDO0lBQ0osQ0FBQztDQUlGO0FBWUQ7O0dBRUc7QUFDSSxNQUFNLFdBQVcsR0FBRyxJQUFJLG9EQUFLLENBQ2xDLHFDQUFxQyxFQUNyQyxpQ0FBaUMsQ0FDbEMsQ0FBQzs7Ozs7Ozs7Ozs7Ozs7O0FDeEVGOzs7R0FHRztBQUVIOzs7OztHQUtHO0FBQ0ksU0FBUyxlQUFlLENBQUMsTUFBYztJQUM1QyxPQUFPLE1BQU0sQ0FBQyxPQUFPLENBQUMsR0FBRyxFQUFFLEdBQUcsQ0FBQyxDQUFDO0FBQ2xDLENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdHJhbnNsYXRpb24vc3JjL2Jhc2UudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RyYW5zbGF0aW9uL3NyYy9nZXR0ZXh0LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RyYW5zbGF0aW9uL3NyYy9tYW5hZ2VyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvc2VydmVyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvdXRpbHMudHMiXSwic291cmNlc0NvbnRlbnQiOlsiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBHZXR0ZXh0IH0gZnJvbSAnLi9nZXR0ZXh0JztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBUcmFuc2xhdGlvbkJ1bmRsZSB9IGZyb20gJy4vdG9rZW5zJztcblxuLyoqXG4gKiBBIHRyYW5zbGF0b3IgdGhhdCBsb2FkcyBhIGR1bW15IGxhbmd1YWdlIGJ1bmRsZSB0aGF0IHJldHVybnMgdGhlIHNhbWUgaW5wdXRcbiAqIHN0cmluZ3MuXG4gKi9cbmNsYXNzIE51bGxUcmFuc2xhdG9yIGltcGxlbWVudHMgSVRyYW5zbGF0b3Ige1xuICBjb25zdHJ1Y3RvcihidW5kbGU6IFRyYW5zbGF0aW9uQnVuZGxlKSB7XG4gICAgdGhpcy5fbGFuZ3VhZ2VCdW5kbGUgPSBidW5kbGU7XG4gIH1cblxuICByZWFkb25seSBsYW5ndWFnZUNvZGU6IHN0cmluZyA9ICdlbic7XG5cbiAgbG9hZChkb21haW46IHN0cmluZyk6IFRyYW5zbGF0aW9uQnVuZGxlIHtcbiAgICByZXR1cm4gdGhpcy5fbGFuZ3VhZ2VCdW5kbGU7XG4gIH1cblxuICBwcml2YXRlIF9sYW5ndWFnZUJ1bmRsZTogVHJhbnNsYXRpb25CdW5kbGU7XG59XG5cbi8qKlxuICogQSBsYW5ndWFnZSBidW5kbGUgdGhhdCByZXR1cm5zIHRoZSBzYW1lIGlucHV0IHN0cmluZ3MuXG4gKi9cbmNsYXNzIE51bGxMYW5ndWFnZUJ1bmRsZSB7XG4gIF9fKG1zZ2lkOiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5nZXR0ZXh0KG1zZ2lkLCAuLi5hcmdzKTtcbiAgfVxuXG4gIF9uKG1zZ2lkOiBzdHJpbmcsIG1zZ2lkX3BsdXJhbDogc3RyaW5nLCBuOiBudW1iZXIsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5uZ2V0dGV4dChtc2dpZCwgbXNnaWRfcGx1cmFsLCBuLCAuLi5hcmdzKTtcbiAgfVxuXG4gIF9wKG1zZ2N0eHQ6IHN0cmluZywgbXNnaWQ6IHN0cmluZywgLi4uYXJnczogYW55W10pOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLnBnZXR0ZXh0KG1zZ2N0eHQsIG1zZ2lkLCAuLi5hcmdzKTtcbiAgfVxuXG4gIF9ucChcbiAgICBtc2djdHh0OiBzdHJpbmcsXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5ucGdldHRleHQobXNnY3R4dCwgbXNnaWQsIG1zZ2lkX3BsdXJhbCwgbiwgLi4uYXJncyk7XG4gIH1cblxuICBnZXR0ZXh0KG1zZ2lkOiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gR2V0dGV4dC5zdHJmbXQobXNnaWQsIC4uLmFyZ3MpO1xuICB9XG5cbiAgbmdldHRleHQoXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICByZXR1cm4gR2V0dGV4dC5zdHJmbXQobiA9PSAxID8gbXNnaWQgOiBtc2dpZF9wbHVyYWwsIC4uLltuXS5jb25jYXQoYXJncykpO1xuICB9XG5cbiAgcGdldHRleHQobXNnY3R4dDogc3RyaW5nLCBtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIEdldHRleHQuc3RyZm10KG1zZ2lkLCAuLi5hcmdzKTtcbiAgfVxuXG4gIG5wZ2V0dGV4dChcbiAgICBtc2djdHh0OiBzdHJpbmcsXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5uZ2V0dGV4dChtc2dpZCwgbXNnaWRfcGx1cmFsLCBuLCAuLi5hcmdzKTtcbiAgfVxuXG4gIGRjbnBnZXR0ZXh0KFxuICAgIGRvbWFpbjogc3RyaW5nLFxuICAgIG1zZ2N0eHQ6IHN0cmluZyxcbiAgICBtc2dpZDogc3RyaW5nLFxuICAgIG1zZ2lkX3BsdXJhbDogc3RyaW5nLFxuICAgIG46IG51bWJlcixcbiAgICAuLi5hcmdzOiBhbnlbXVxuICApOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLm5nZXR0ZXh0KG1zZ2lkLCBtc2dpZF9wbHVyYWwsIG4sIC4uLmFyZ3MpO1xuICB9XG59XG5cbi8qKlxuICogVGhlIGFwcGxpY2F0aW9uIG51bGwgdHJhbnNsYXRvciBpbnN0YW5jZSB0aGF0IGp1c3QgcmV0dXJucyB0aGUgc2FtZSB0ZXh0LlxuICogQWxzbyBwcm92aWRlcyBpbnRlcnBvbGF0aW9uLlxuICovXG5leHBvcnQgY29uc3QgbnVsbFRyYW5zbGF0b3IgPSBuZXcgTnVsbFRyYW5zbGF0b3IobmV3IE51bGxMYW5ndWFnZUJ1bmRsZSgpKTtcbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58XG58IEJhc2UgZ2V0dGV4dC5qcyBpbXBsZW1lbnRhdGlvbi5cbnwgQ29weXJpZ2h0IChjKSBHdWlsbGF1bWUgUG90aWVyLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIE1JVCBMaWNlbnNlLlxufCBTZWU6IGh0dHBzOi8vZ2l0aHViLmNvbS9ndWlsbGF1bWVwb3RpZXIvZ2V0dGV4dC5qc1xufFxufCBUeXBlIGRlZmluaXRpb25zLlxufCBDb3B5cmlnaHQgKGMpIEp1bGllbiBDcm91emV0IGFuZCBGbG9yaWFuIFNjaHdpbmdlbnNjaGzDtmdsLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIE1JVCBMaWNlbnNlLlxufCBTZWU6IGh0dHBzOi8vZ2l0aHViLmNvbS9EZWZpbml0ZWx5VHlwZWQvRGVmaW5pdGVseVR5cGVkXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG5cbmltcG9ydCB7IG5vcm1hbGl6ZURvbWFpbiB9IGZyb20gJy4vdXRpbHMnO1xuXG4vKipcbiAqIEEgcGx1cmFsIGZvcm0gZnVuY3Rpb24uXG4gKi9cbnR5cGUgUGx1cmFsRm9ybSA9IChuOiBudW1iZXIpID0+IG51bWJlcjtcblxuLyoqXG4gKiBNZXRhZGF0YSBmb3IgYSBsYW5ndWFnZSBwYWNrLlxuICovXG5pbnRlcmZhY2UgSUpzb25EYXRhSGVhZGVyIHtcbiAgLyoqXG4gICAqIExhbmd1YWdlIGxvY2FsZS4gRXhhbXBsZTogZXNfQ08sIGVzLUNPLlxuICAgKi9cbiAgbGFuZ3VhZ2U6IHN0cmluZztcblxuICAvKipcbiAgICogVGhlIGRvbWFpbiBvZiB0aGUgdHJhbnNsYXRpb24sIHVzdWFsbHkgdGhlIG5vcm1hbGl6ZWQgcGFja2FnZSBuYW1lLlxuICAgKiBFeGFtcGxlOiBcImp1cHl0ZXJsYWJcIiwgXCJqdXB5dGVybGFiX2dpdFwiXG4gICAqXG4gICAqICMjIyMgTm90ZVxuICAgKiBOb3JtYWxpemF0aW9uIHJlcGxhY2VzIGAtYCBieSBgX2AgaW4gcGFja2FnZSBuYW1lLlxuICAgKi9cbiAgZG9tYWluOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFN0cmluZyBkZXNjcmliaW5nIHRoZSBwbHVyYWwgb2YgdGhlIGdpdmVuIGxhbmd1YWdlLlxuICAgKiBTZWU6IGh0dHBzOi8vd3d3LmdudS5vcmcvc29mdHdhcmUvZ2V0dGV4dC9tYW51YWwvaHRtbF9ub2RlL1RyYW5zbGF0aW5nLXBsdXJhbC1mb3Jtcy5odG1sXG4gICAqL1xuICBwbHVyYWxGb3Jtczogc3RyaW5nO1xufVxuXG4vKipcbiAqIFRyYW5zbGF0YWJsZSBzdHJpbmcgbWVzc2FnZXMuXG4gKi9cbmludGVyZmFjZSBJSnNvbkRhdGFNZXNzYWdlcyB7XG4gIC8qKlxuICAgKiBUcmFuc2xhdGlvbiBzdHJpbmdzIGZvciBhIGdpdmVuIG1zZ19pZC5cbiAgICovXG4gIFtrZXk6IHN0cmluZ106IHN0cmluZ1tdIHwgSUpzb25EYXRhSGVhZGVyO1xufVxuXG4vKipcbiAqIFRyYW5zbGF0YWJsZSBzdHJpbmcgbWVzc2FnZXMgaW5jbHVpbmcgbWV0YWRhdGEuXG4gKi9cbmludGVyZmFjZSBJSnNvbkRhdGEgZXh0ZW5kcyBJSnNvbkRhdGFNZXNzYWdlcyB7XG4gIC8qKlxuICAgKiBNZXRhZGF0YSBvZiB0aGUgbGFuZ3VhZ2UgYnVuZGxlLlxuICAgKi9cbiAgJyc6IElKc29uRGF0YUhlYWRlcjtcbn1cblxuLyoqXG4gKiBDb25maWd1cmFibGUgb3B0aW9ucyBmb3IgdGhlIEdldHRleHQgY29uc3RydWN0b3IuXG4gKi9cbmludGVyZmFjZSBJT3B0aW9ucyB7XG4gIC8qKlxuICAgKiBMYW5ndWFnZSBsb2NhbGUuIEV4YW1wbGU6IGVzX0NPLCBlcy1DTy5cbiAgICovXG4gIGxvY2FsZT86IHN0cmluZztcblxuICAvKipcbiAgICogVGhlIGRvbWFpbiBvZiB0aGUgdHJhbnNsYXRpb24sIHVzdWFsbHkgdGhlIG5vcm1hbGl6ZWQgcGFja2FnZSBuYW1lLlxuICAgKiBFeGFtcGxlOiBcImp1cHl0ZXJsYWJcIiwgXCJqdXB5dGVybGFiX2dpdFwiXG4gICAqXG4gICAqICMjIyMgTm90ZVxuICAgKiBOb3JtYWxpemF0aW9uIHJlcGxhY2VzIGAtYCBieSBgX2AgaW4gcGFja2FnZSBuYW1lLlxuICAgKi9cbiAgZG9tYWluPzogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBUaGUgZGVsaW1pdGVyIHRvIHVzZSB3aGVuIGFkZGluZyBjb250ZXh0dWFsaXplZCBzdHJpbmdzLlxuICAgKi9cbiAgY29udGV4dERlbGltaXRlcj86IHN0cmluZztcblxuICAvKipcbiAgICogVHJhbnNsYXRpb24gbWVzc2FnZSBzdHJpbmdzLlxuICAgKi9cbiAgbWVzc2FnZXM/OiBBcnJheTxzdHJpbmc+O1xuXG4gIC8qKlxuICAgKiBTdHJpbmcgZGVzY3JpYmluZyB0aGUgcGx1cmFsIG9mIHRoZSBnaXZlbiBsYW5ndWFnZS5cbiAgICogU2VlOiBodHRwczovL3d3dy5nbnUub3JnL3NvZnR3YXJlL2dldHRleHQvbWFudWFsL2h0bWxfbm9kZS9UcmFuc2xhdGluZy1wbHVyYWwtZm9ybXMuaHRtbFxuICAgKi9cbiAgcGx1cmFsRm9ybXM/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFRoZSBzdHJpbmcgcHJlZml4IHRvIGFkZCB0byBsb2NhbGl6ZWQgc3RyaW5ncy5cbiAgICovXG4gIHN0cmluZ3NQcmVmaXg/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFBsdXJhbCBmb3JtIGZ1bmN0aW9uLlxuICAgKi9cbiAgcGx1cmFsRnVuYz86IFBsdXJhbEZvcm07XG59XG5cbi8qKlxuICogT3B0aW9ucyBvZiB0aGUgbWFpbiB0cmFuc2xhdGlvbiBgdGAgbWV0aG9kLlxuICovXG5pbnRlcmZhY2UgSVRPcHRpb25zIHtcbiAgLyoqXG4gICAqIFN0cmluZyBkZXNjcmliaW5nIHRoZSBwbHVyYWwgb2YgdGhlIGdpdmVuIGxhbmd1YWdlLlxuICAgKiBTZWU6IGh0dHBzOi8vd3d3LmdudS5vcmcvc29mdHdhcmUvZ2V0dGV4dC9tYW51YWwvaHRtbF9ub2RlL1RyYW5zbGF0aW5nLXBsdXJhbC1mb3Jtcy5odG1sXG4gICAqL1xuICBwbHVyYWxGb3JtPzogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBQbHVyYWwgZm9ybSBmdW5jdGlvbi5cbiAgICovXG4gIHBsdXJhbEZ1bmM/OiBQbHVyYWxGb3JtO1xuXG4gIC8qKlxuICAgKiBMYW5ndWFnZSBsb2NhbGUuIEV4YW1wbGU6IGVzX0NPLCBlcy1DTy5cbiAgICovXG4gIGxvY2FsZT86IHN0cmluZztcbn1cblxuLyoqXG4gKiBHZXR0ZXh0IGNsYXNzIHByb3ZpZGluZyBsb2NhbGl6YXRpb24gbWV0aG9kcy5cbiAqL1xuY2xhc3MgR2V0dGV4dCB7XG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM/OiBJT3B0aW9ucykge1xuICAgIG9wdGlvbnMgPSBvcHRpb25zIHx8IHt9O1xuXG4gICAgLy8gZGVmYXVsdCB2YWx1ZXMgdGhhdCBjb3VsZCBiZSBvdmVycmlkZGVuIGluIEdldHRleHQoKSBjb25zdHJ1Y3RvclxuICAgIHRoaXMuX2RlZmF1bHRzID0ge1xuICAgICAgZG9tYWluOiAnbWVzc2FnZXMnLFxuICAgICAgbG9jYWxlOiBkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQuZ2V0QXR0cmlidXRlKCdsYW5nJykgfHwgJ2VuJyxcbiAgICAgIHBsdXJhbEZ1bmM6IGZ1bmN0aW9uIChuOiBudW1iZXIpIHtcbiAgICAgICAgcmV0dXJuIHsgbnBsdXJhbHM6IDIsIHBsdXJhbDogbiAhPSAxID8gMSA6IDAgfTtcbiAgICAgIH0sXG4gICAgICBjb250ZXh0RGVsaW1pdGVyOiBTdHJpbmcuZnJvbUNoYXJDb2RlKDQpLCAvLyBcXHUwMDA0XG4gICAgICBzdHJpbmdzUHJlZml4OiAnJ1xuICAgIH07XG5cbiAgICAvLyBFbnN1cmUgdGhlIGNvcnJlY3Qgc2VwYXJhdG9yIGlzIHVzZWRcbiAgICB0aGlzLl9sb2NhbGUgPSAob3B0aW9ucy5sb2NhbGUgfHwgdGhpcy5fZGVmYXVsdHMubG9jYWxlKS5yZXBsYWNlKCdfJywgJy0nKTtcbiAgICB0aGlzLl9kb21haW4gPSBub3JtYWxpemVEb21haW4ob3B0aW9ucy5kb21haW4gfHwgdGhpcy5fZGVmYXVsdHMuZG9tYWluKTtcbiAgICB0aGlzLl9jb250ZXh0RGVsaW1pdGVyID1cbiAgICAgIG9wdGlvbnMuY29udGV4dERlbGltaXRlciB8fCB0aGlzLl9kZWZhdWx0cy5jb250ZXh0RGVsaW1pdGVyO1xuICAgIHRoaXMuX3N0cmluZ3NQcmVmaXggPSBvcHRpb25zLnN0cmluZ3NQcmVmaXggfHwgdGhpcy5fZGVmYXVsdHMuc3RyaW5nc1ByZWZpeDtcbiAgICB0aGlzLl9wbHVyYWxGdW5jcyA9IHt9O1xuICAgIHRoaXMuX2RpY3Rpb25hcnkgPSB7fTtcbiAgICB0aGlzLl9wbHVyYWxGb3JtcyA9IHt9O1xuXG4gICAgaWYgKG9wdGlvbnMubWVzc2FnZXMpIHtcbiAgICAgIHRoaXMuX2RpY3Rpb25hcnlbdGhpcy5fZG9tYWluXSA9IHt9O1xuICAgICAgdGhpcy5fZGljdGlvbmFyeVt0aGlzLl9kb21haW5dW3RoaXMuX2xvY2FsZV0gPSBvcHRpb25zLm1lc3NhZ2VzO1xuICAgIH1cblxuICAgIGlmIChvcHRpb25zLnBsdXJhbEZvcm1zKSB7XG4gICAgICB0aGlzLl9wbHVyYWxGb3Jtc1t0aGlzLl9sb2NhbGVdID0gb3B0aW9ucy5wbHVyYWxGb3JtcztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU2V0IGN1cnJlbnQgY29udGV4dCBkZWxpbWl0ZXIuXG4gICAqXG4gICAqIEBwYXJhbSBkZWxpbWl0ZXIgLSBUaGUgZGVsaW1pdGVyIHRvIHNldC5cbiAgICovXG4gIHNldENvbnRleHREZWxpbWl0ZXIoZGVsaW1pdGVyOiBzdHJpbmcpOiB2b2lkIHtcbiAgICB0aGlzLl9jb250ZXh0RGVsaW1pdGVyID0gZGVsaW1pdGVyO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBjdXJyZW50IGNvbnRleHQgZGVsaW1pdGVyLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY3VycmVudCBkZWxpbWl0ZXIuXG4gICAqL1xuICBnZXRDb250ZXh0RGVsaW1pdGVyKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2NvbnRleHREZWxpbWl0ZXI7XG4gIH1cblxuICAvKipcbiAgICogU2V0IGN1cnJlbnQgbG9jYWxlLlxuICAgKlxuICAgKiBAcGFyYW0gbG9jYWxlIC0gVGhlIGxvY2FsZSB0byBzZXQuXG4gICAqL1xuICBzZXRMb2NhbGUobG9jYWxlOiBzdHJpbmcpOiB2b2lkIHtcbiAgICB0aGlzLl9sb2NhbGUgPSBsb2NhbGUucmVwbGFjZSgnXycsICctJyk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGN1cnJlbnQgbG9jYWxlLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY3VycmVudCBsb2NhbGUuXG4gICAqL1xuICBnZXRMb2NhbGUoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fbG9jYWxlO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBjdXJyZW50IGRvbWFpbi5cbiAgICpcbiAgICogQHBhcmFtIGRvbWFpbiAtIFRoZSBkb21haW4gdG8gc2V0LlxuICAgKi9cbiAgc2V0RG9tYWluKGRvbWFpbjogc3RyaW5nKTogdm9pZCB7XG4gICAgdGhpcy5fZG9tYWluID0gbm9ybWFsaXplRG9tYWluKGRvbWFpbik7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGN1cnJlbnQgZG9tYWluLlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgY3VycmVudCBkb21haW4gc3RyaW5nLlxuICAgKi9cbiAgZ2V0RG9tYWluKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2RvbWFpbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgY3VycmVudCBzdHJpbmdzIHByZWZpeC5cbiAgICpcbiAgICogQHBhcmFtIHByZWZpeCAtIFRoZSBzdHJpbmcgcHJlZml4IHRvIHNldC5cbiAgICovXG4gIHNldFN0cmluZ3NQcmVmaXgocHJlZml4OiBzdHJpbmcpOiB2b2lkIHtcbiAgICB0aGlzLl9zdHJpbmdzUHJlZml4ID0gcHJlZml4O1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBjdXJyZW50IHN0cmluZ3MgcHJlZml4LlxuICAgKlxuICAgKiBAcmV0dXJucyBUaGUgc3RyaW5ncyBwcmVmaXguXG4gICAqL1xuICBnZXRTdHJpbmdzUHJlZml4KCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX3N0cmluZ3NQcmVmaXg7XG4gIH1cblxuICAvKipcbiAgICogYHNwcmludGZgIGVxdWl2YWxlbnQsIHRha2VzIGEgc3RyaW5nIGFuZCBzb21lIGFyZ3VtZW50cyB0byBtYWtlIGFcbiAgICogY29tcHV0ZWQgc3RyaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gZm10IC0gVGhlIHN0cmluZyB0byBpbnRlcnBvbGF0ZS5cbiAgICogQHBhcmFtIGFyZ3MgLSBUaGUgdmFyaWFibGVzIHRvIHVzZSBpbiBpbnRlcnBvbGF0aW9uLlxuICAgKlxuICAgKiAjIyMgRXhhbXBsZXNcbiAgICogc3RyZm10KFwiJTEgZG9ncyBhcmUgaW4gJTJcIiwgNywgXCJ0aGUga2l0Y2hlblwiKTsgPT4gXCI3IGRvZ3MgYXJlIGluIHRoZSBraXRjaGVuXCJcbiAgICogc3RyZm10KFwiSSBsaWtlICUxLCBiYW5hbmFzIGFuZCAlMVwiLCBcImFwcGxlc1wiKTsgPT4gXCJJIGxpa2UgYXBwbGVzLCBiYW5hbmFzIGFuZCBhcHBsZXNcIlxuICAgKi9cbiAgc3RhdGljIHN0cmZtdChmbXQ6IHN0cmluZywgLi4uYXJnczogYW55W10pOiBzdHJpbmcge1xuICAgIHJldHVybiAoXG4gICAgICBmbXRcbiAgICAgICAgLy8gcHV0IHNwYWNlIGFmdGVyIGRvdWJsZSAlIHRvIHByZXZlbnQgcGxhY2Vob2xkZXIgcmVwbGFjZW1lbnQgb2Ygc3VjaCBtYXRjaGVzXG4gICAgICAgIC5yZXBsYWNlKC8lJS9nLCAnJSUgJylcbiAgICAgICAgLy8gcmVwbGFjZSBwbGFjZWhvbGRlcnNcbiAgICAgICAgLnJlcGxhY2UoLyUoXFxkKykvZywgZnVuY3Rpb24gKHN0ciwgcDEpIHtcbiAgICAgICAgICByZXR1cm4gYXJnc1twMSAtIDFdO1xuICAgICAgICB9KVxuICAgICAgICAvLyByZXBsYWNlIGRvdWJsZSAlIGFuZCBzcGFjZSB3aXRoIHNpbmdsZSAlXG4gICAgICAgIC5yZXBsYWNlKC8lJSAvZywgJyUnKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogTG9hZCBqc29uIHRyYW5zbGF0aW9ucyBzdHJpbmdzIChJbiBKZWQgMi54IGZvcm1hdCkuXG4gICAqXG4gICAqIEBwYXJhbSBqc29uRGF0YSAtIFRoZSB0cmFuc2xhdGlvbiBzdHJpbmdzIHBsdXMgbWV0YWRhdGEuXG4gICAqIEBwYXJhbSBkb21haW4gLSBUaGUgdHJhbnNsYXRpb24gZG9tYWluLCBlLmcuIFwianVweXRlcmxhYlwiLlxuICAgKi9cbiAgbG9hZEpTT04oanNvbkRhdGE6IElKc29uRGF0YSwgZG9tYWluOiBzdHJpbmcpOiB2b2lkIHtcbiAgICBpZiAoXG4gICAgICAhanNvbkRhdGFbJyddIHx8XG4gICAgICAhanNvbkRhdGFbJyddWydsYW5ndWFnZSddIHx8XG4gICAgICAhanNvbkRhdGFbJyddWydwbHVyYWxGb3JtcyddXG4gICAgKSB7XG4gICAgICB0aHJvdyBuZXcgRXJyb3IoXG4gICAgICAgIGBXcm9uZyBqc29uRGF0YSwgaXQgbXVzdCBoYXZlIGFuIGVtcHR5IGtleSAoXCJcIikgd2l0aCBcImxhbmd1YWdlXCIgYW5kIFwicGx1cmFsRm9ybXNcIiBpbmZvcm1hdGlvbjogJHtqc29uRGF0YX1gXG4gICAgICApO1xuICAgIH1cblxuICAgIGRvbWFpbiA9IG5vcm1hbGl6ZURvbWFpbihkb21haW4pO1xuXG4gICAgbGV0IGhlYWRlcnMgPSBqc29uRGF0YVsnJ107XG4gICAgbGV0IGpzb25EYXRhQ29weSA9IEpTT04ucGFyc2UoSlNPTi5zdHJpbmdpZnkoanNvbkRhdGEpKTtcbiAgICBkZWxldGUganNvbkRhdGFDb3B5WycnXTtcblxuICAgIHRoaXMuc2V0TWVzc2FnZXMoXG4gICAgICBkb21haW4gfHwgdGhpcy5fZGVmYXVsdHMuZG9tYWluLFxuICAgICAgaGVhZGVyc1snbGFuZ3VhZ2UnXSxcbiAgICAgIGpzb25EYXRhQ29weSxcbiAgICAgIGhlYWRlcnNbJ3BsdXJhbEZvcm1zJ11cbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIFNob3J0aGFuZCBmb3IgZ2V0dGV4dC5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBhcmdzIC0gQW55IGFkZGl0aW9uYWwgdmFsdWVzIHRvIHVzZSB3aXRoIGludGVycG9sYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgdHJhbnNsYXRlZCBzdHJpbmcgaWYgZm91bmQsIG9yIHRoZSBvcmlnaW5hbCBzdHJpbmcuXG4gICAqXG4gICAqICMjIyBOb3Rlc1xuICAgKiBUaGlzIGlzIG5vdCBhIHByaXZhdGUgbWV0aG9kIChzdGFydHMgd2l0aCBhbiB1bmRlcnNjb3JlKSBpdCBpcyBqdXN0XG4gICAqIGEgc2hvcnRlciBhbmQgc3RhbmRhcmQgd2F5IHRvIGNhbGwgdGhlc2UgbWV0aG9kcy5cbiAgICovXG4gIF9fKG1zZ2lkOiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5nZXR0ZXh0KG1zZ2lkLCAuLi5hcmdzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTaG9ydGhhbmQgZm9yIG5nZXR0ZXh0LlxuICAgKlxuICAgKiBAcGFyYW0gbXNnaWQgLSBUaGUgc2luZ3VsYXIgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIG1zZ2lkX3BsdXJhbCAtIFRoZSBwbHVyYWwgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIG4gLSBUaGUgbnVtYmVyIGZvciBwbHVyYWxpemF0aW9uLlxuICAgKiBAcGFyYW0gYXJncyAtIEFueSBhZGRpdGlvbmFsIHZhbHVlcyB0byB1c2Ugd2l0aCBpbnRlcnBvbGF0aW9uLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBub3QgYSBwcml2YXRlIG1ldGhvZCAoc3RhcnRzIHdpdGggYW4gdW5kZXJzY29yZSkgaXQgaXMganVzdFxuICAgKiBhIHNob3J0ZXIgYW5kIHN0YW5kYXJkIHdheSB0byBjYWxsIHRoZXNlIG1ldGhvZHMuXG4gICAqL1xuICBfbihtc2dpZDogc3RyaW5nLCBtc2dpZF9wbHVyYWw6IHN0cmluZywgbjogbnVtYmVyLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMubmdldHRleHQobXNnaWQsIG1zZ2lkX3BsdXJhbCwgbiwgLi4uYXJncyk7XG4gIH1cblxuICAvKipcbiAgICogU2hvcnRoYW5kIGZvciBwZ2V0dGV4dC5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2N0eHQgLSBUaGUgbWVzc2FnZSBjb250ZXh0LlxuICAgKiBAcGFyYW0gbXNnaWQgLSBUaGUgc2luZ3VsYXIgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvbi5cbiAgICpcbiAgICogQHJldHVybnMgQSB0cmFuc2xhdGVkIHN0cmluZyBpZiBmb3VuZCwgb3IgdGhlIG9yaWdpbmFsIHN0cmluZy5cbiAgICpcbiAgICogIyMjIE5vdGVzXG4gICAqIFRoaXMgaXMgbm90IGEgcHJpdmF0ZSBtZXRob2QgKHN0YXJ0cyB3aXRoIGFuIHVuZGVyc2NvcmUpIGl0IGlzIGp1c3RcbiAgICogYSBzaG9ydGVyIGFuZCBzdGFuZGFyZCB3YXkgdG8gY2FsbCB0aGVzZSBtZXRob2RzLlxuICAgKi9cbiAgX3AobXNnY3R4dDogc3RyaW5nLCBtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMucGdldHRleHQobXNnY3R4dCwgbXNnaWQsIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNob3J0aGFuZCBmb3IgbnBnZXR0ZXh0LlxuICAgKlxuICAgKiBAcGFyYW0gbXNnY3R4dCAtIFRoZSBtZXNzYWdlIGNvbnRleHQuXG4gICAqIEBwYXJhbSBtc2dpZCAtIFRoZSBzaW5ndWxhciBzdHJpbmcgdG8gdHJhbnNsYXRlLlxuICAgKiBAcGFyYW0gbXNnaWRfcGx1cmFsIC0gVGhlIHBsdXJhbCBzdHJpbmcgdG8gdHJhbnNsYXRlLlxuICAgKiBAcGFyYW0gbiAtIFRoZSBudW1iZXIgZm9yIHBsdXJhbGl6YXRpb24uXG4gICAqIEBwYXJhbSBhcmdzIC0gQW55IGFkZGl0aW9uYWwgdmFsdWVzIHRvIHVzZSB3aXRoIGludGVycG9sYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgdHJhbnNsYXRlZCBzdHJpbmcgaWYgZm91bmQsIG9yIHRoZSBvcmlnaW5hbCBzdHJpbmcuXG4gICAqXG4gICAqICMjIyBOb3Rlc1xuICAgKiBUaGlzIGlzIG5vdCBhIHByaXZhdGUgbWV0aG9kIChzdGFydHMgd2l0aCBhbiB1bmRlcnNjb3JlKSBpdCBpcyBqdXN0XG4gICAqIGEgc2hvcnRlciBhbmQgc3RhbmRhcmQgd2F5IHRvIGNhbGwgdGhlc2UgbWV0aG9kcy5cbiAgICovXG4gIF9ucChcbiAgICBtc2djdHh0OiBzdHJpbmcsXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5ucGdldHRleHQobXNnY3R4dCwgbXNnaWQsIG1zZ2lkX3BsdXJhbCwgbiwgLi4uYXJncyk7XG4gIH1cblxuICAvKipcbiAgICogVHJhbnNsYXRlIGEgc2luZ3VsYXIgc3RyaW5nIHdpdGggZXh0cmEgaW50ZXJwb2xhdGlvbiB2YWx1ZXMuXG4gICAqXG4gICAqIEBwYXJhbSBtc2dpZCAtIFRoZSBzaW5ndWxhciBzdHJpbmcgdG8gdHJhbnNsYXRlLlxuICAgKiBAcGFyYW0gYXJncyAtIEFueSBhZGRpdGlvbmFsIHZhbHVlcyB0byB1c2Ugd2l0aCBpbnRlcnBvbGF0aW9uLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKi9cbiAgZ2V0dGV4dChtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuZGNucGdldHRleHQoJycsICcnLCBtc2dpZCwgJycsIDAsIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRyYW5zbGF0ZSBhIHBsdXJhbCBzdHJpbmcgd2l0aCBleHRyYSBpbnRlcnBvbGF0aW9uIHZhbHVlcy5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBhcmdzIC0gQW55IGFkZGl0aW9uYWwgdmFsdWVzIHRvIHVzZSB3aXRoIGludGVycG9sYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgdHJhbnNsYXRlZCBzdHJpbmcgaWYgZm91bmQsIG9yIHRoZSBvcmlnaW5hbCBzdHJpbmcuXG4gICAqL1xuICBuZ2V0dGV4dChcbiAgICBtc2dpZDogc3RyaW5nLFxuICAgIG1zZ2lkX3BsdXJhbDogc3RyaW5nLFxuICAgIG46IG51bWJlcixcbiAgICAuLi5hcmdzOiBhbnlbXVxuICApOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLmRjbnBnZXR0ZXh0KCcnLCAnJywgbXNnaWQsIG1zZ2lkX3BsdXJhbCwgbiwgLi4uYXJncyk7XG4gIH1cblxuICAvKipcbiAgICogVHJhbnNsYXRlIGEgY29udGV4dHVhbGl6ZWQgc2luZ3VsYXIgc3RyaW5nIHdpdGggZXh0cmEgaW50ZXJwb2xhdGlvbiB2YWx1ZXMuXG4gICAqXG4gICAqIEBwYXJhbSBtc2djdHh0IC0gVGhlIG1lc3NhZ2UgY29udGV4dC5cbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBhcmdzIC0gQW55IGFkZGl0aW9uYWwgdmFsdWVzIHRvIHVzZSB3aXRoIGludGVycG9sYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgdHJhbnNsYXRlZCBzdHJpbmcgaWYgZm91bmQsIG9yIHRoZSBvcmlnaW5hbCBzdHJpbmcuXG4gICAqXG4gICAqICMjIyBOb3Rlc1xuICAgKiBUaGlzIGlzIG5vdCBhIHByaXZhdGUgbWV0aG9kIChzdGFydHMgd2l0aCBhbiB1bmRlcnNjb3JlKSBpdCBpcyBqdXN0XG4gICAqIGEgc2hvcnRlciBhbmQgc3RhbmRhcmQgd2F5IHRvIGNhbGwgdGhlc2UgbWV0aG9kcy5cbiAgICovXG4gIHBnZXR0ZXh0KG1zZ2N0eHQ6IHN0cmluZywgbXNnaWQ6IHN0cmluZywgLi4uYXJnczogYW55W10pOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLmRjbnBnZXR0ZXh0KCcnLCBtc2djdHh0LCBtc2dpZCwgJycsIDAsIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRyYW5zbGF0ZSBhIGNvbnRleHR1YWxpemVkIHBsdXJhbCBzdHJpbmcgd2l0aCBleHRyYSBpbnRlcnBvbGF0aW9uIHZhbHVlcy5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2N0eHQgLSBUaGUgbWVzc2FnZSBjb250ZXh0LlxuICAgKiBAcGFyYW0gbXNnaWQgLSBUaGUgc2luZ3VsYXIgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIG1zZ2lkX3BsdXJhbCAtIFRoZSBwbHVyYWwgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIG4gLSBUaGUgbnVtYmVyIGZvciBwbHVyYWxpemF0aW9uLlxuICAgKiBAcGFyYW0gYXJncyAtIEFueSBhZGRpdGlvbmFsIHZhbHVlcyB0byB1c2Ugd2l0aCBpbnRlcnBvbGF0aW9uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgdHJhbnNsYXRlZCBzdHJpbmcgaWYgZm91bmQsIG9yIHRoZSBvcmlnaW5hbCBzdHJpbmcuXG4gICAqL1xuICBucGdldHRleHQoXG4gICAgbXNnY3R4dDogc3RyaW5nLFxuICAgIG1zZ2lkOiBzdHJpbmcsXG4gICAgbXNnaWRfcGx1cmFsOiBzdHJpbmcsXG4gICAgbjogbnVtYmVyLFxuICAgIC4uLmFyZ3M6IGFueVtdXG4gICk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuZGNucGdldHRleHQoJycsIG1zZ2N0eHQsIG1zZ2lkLCBtc2dpZF9wbHVyYWwsIG4sIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRyYW5zbGF0ZSBhIHNpbmd1bGFyIHN0cmluZyB3aXRoIGV4dHJhIGludGVycG9sYXRpb24gdmFsdWVzLlxuICAgKlxuICAgKiBAcGFyYW0gZG9tYWluIC0gVGhlIHRyYW5zbGF0aW9ucyBkb21haW4uXG4gICAqIEBwYXJhbSBtc2djdHh0IC0gVGhlIG1lc3NhZ2UgY29udGV4dC5cbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBtc2dpZF9wbHVyYWwgLSBUaGUgcGx1cmFsIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBuIC0gVGhlIG51bWJlciBmb3IgcGx1cmFsaXphdGlvbi5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvblxuICAgKlxuICAgKiBAcmV0dXJucyBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKi9cbiAgZGNucGdldHRleHQoXG4gICAgZG9tYWluOiBzdHJpbmcsXG4gICAgbXNnY3R4dDogc3RyaW5nLFxuICAgIG1zZ2lkOiBzdHJpbmcsXG4gICAgbXNnaWRfcGx1cmFsOiBzdHJpbmcsXG4gICAgbjogbnVtYmVyLFxuICAgIC4uLmFyZ3M6IGFueVtdXG4gICk6IHN0cmluZyB7XG4gICAgZG9tYWluID0gbm9ybWFsaXplRG9tYWluKGRvbWFpbikgfHwgdGhpcy5fZG9tYWluO1xuXG4gICAgbGV0IHRyYW5zbGF0aW9uOiBBcnJheTxzdHJpbmc+O1xuICAgIGxldCBrZXk6IHN0cmluZyA9IG1zZ2N0eHRcbiAgICAgID8gbXNnY3R4dCArIHRoaXMuX2NvbnRleHREZWxpbWl0ZXIgKyBtc2dpZFxuICAgICAgOiBtc2dpZDtcbiAgICBsZXQgb3B0aW9uczogYW55ID0geyBwbHVyYWxGb3JtOiBmYWxzZSB9O1xuICAgIGxldCBleGlzdDogYm9vbGVhbiA9IGZhbHNlO1xuICAgIGxldCBsb2NhbGU6IHN0cmluZyA9IHRoaXMuX2xvY2FsZTtcbiAgICBsZXQgbG9jYWxlcyA9IHRoaXMuZXhwYW5kTG9jYWxlKHRoaXMuX2xvY2FsZSk7XG5cbiAgICBmb3IgKGxldCBpIGluIGxvY2FsZXMpIHtcbiAgICAgIGxvY2FsZSA9IGxvY2FsZXNbaV07XG4gICAgICBleGlzdCA9XG4gICAgICAgIHRoaXMuX2RpY3Rpb25hcnlbZG9tYWluXSAmJlxuICAgICAgICB0aGlzLl9kaWN0aW9uYXJ5W2RvbWFpbl1bbG9jYWxlXSAmJlxuICAgICAgICB0aGlzLl9kaWN0aW9uYXJ5W2RvbWFpbl1bbG9jYWxlXVtrZXldO1xuXG4gICAgICAvLyBjaGVjayBjb25kaXRpb24gYXJlIHZhbGlkICgubGVuZ3RoKVxuICAgICAgLy8gYmVjYXVzZSBpdCdzIG5vdCBwb3NzaWJsZSB0byBkZWZpbmUgYm90aCBhIHNpbmd1bGFyIGFuZCBhIHBsdXJhbCBmb3JtIG9mIHRoZSBzYW1lIG1zZ2lkLFxuICAgICAgLy8gd2UgbmVlZCB0byBjaGVjayB0aGF0IHRoZSBzdG9yZWQgZm9ybSBpcyB0aGUgc2FtZSBhcyB0aGUgZXhwZWN0ZWQgb25lLlxuICAgICAgLy8gaWYgbm90LCB3ZSdsbCBqdXN0IGlnbm9yZSB0aGUgdHJhbnNsYXRpb24gYW5kIGNvbnNpZGVyIGl0IGFzIG5vdCB0cmFuc2xhdGVkLlxuICAgICAgaWYgKG1zZ2lkX3BsdXJhbCkge1xuICAgICAgICBleGlzdCA9IGV4aXN0ICYmIHRoaXMuX2RpY3Rpb25hcnlbZG9tYWluXVtsb2NhbGVdW2tleV0ubGVuZ3RoID4gMTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGV4aXN0ID0gZXhpc3QgJiYgdGhpcy5fZGljdGlvbmFyeVtkb21haW5dW2xvY2FsZV1ba2V5XS5sZW5ndGggPT0gMTtcbiAgICAgIH1cblxuICAgICAgaWYgKGV4aXN0KSB7XG4gICAgICAgIC8vIFRoaXMgZW5zdXJlcyB0aGF0IGEgdmFyaWF0aW9uIGlzIHVzZWQuXG4gICAgICAgIG9wdGlvbnMubG9jYWxlID0gbG9jYWxlO1xuICAgICAgICBicmVhaztcbiAgICAgIH1cbiAgICB9XG5cbiAgICBpZiAoIWV4aXN0KSB7XG4gICAgICB0cmFuc2xhdGlvbiA9IFttc2dpZF07XG4gICAgICBvcHRpb25zLnBsdXJhbEZ1bmMgPSB0aGlzLl9kZWZhdWx0cy5wbHVyYWxGdW5jO1xuICAgIH0gZWxzZSB7XG4gICAgICB0cmFuc2xhdGlvbiA9IHRoaXMuX2RpY3Rpb25hcnlbZG9tYWluXVtsb2NhbGVdW2tleV07XG4gICAgfVxuXG4gICAgLy8gU2luZ3VsYXIgZm9ybVxuICAgIGlmICghbXNnaWRfcGx1cmFsKSB7XG4gICAgICByZXR1cm4gdGhpcy50KHRyYW5zbGF0aW9uLCBuLCBvcHRpb25zLCAuLi5hcmdzKTtcbiAgICB9XG5cbiAgICAvLyBQbHVyYWwgb25lXG4gICAgb3B0aW9ucy5wbHVyYWxGb3JtID0gdHJ1ZTtcbiAgICBsZXQgdmFsdWU6IEFycmF5PHN0cmluZz4gPSBleGlzdCA/IHRyYW5zbGF0aW9uIDogW21zZ2lkLCBtc2dpZF9wbHVyYWxdO1xuICAgIHJldHVybiB0aGlzLnQodmFsdWUsIG4sIG9wdGlvbnMsIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFNwbGl0IGEgbG9jYWxlIGludG8gcGFyZW50IGxvY2FsZXMuIFwiZXMtQ09cIiAtPiBbXCJlcy1DT1wiLCBcImVzXCJdXG4gICAqXG4gICAqIEBwYXJhbSBsb2NhbGUgLSBUaGUgbG9jYWxlIHN0cmluZy5cbiAgICpcbiAgICogQHJldHVybnMgQW4gYXJyYXkgb2YgbG9jYWxlcy5cbiAgICovXG4gIHByaXZhdGUgZXhwYW5kTG9jYWxlKGxvY2FsZTogc3RyaW5nKTogQXJyYXk8c3RyaW5nPiB7XG4gICAgbGV0IGxvY2FsZXM6IEFycmF5PHN0cmluZz4gPSBbbG9jYWxlXTtcbiAgICBsZXQgaTogbnVtYmVyID0gbG9jYWxlLmxhc3RJbmRleE9mKCctJyk7XG4gICAgd2hpbGUgKGkgPiAwKSB7XG4gICAgICBsb2NhbGUgPSBsb2NhbGUuc2xpY2UoMCwgaSk7XG4gICAgICBsb2NhbGVzLnB1c2gobG9jYWxlKTtcbiAgICAgIGkgPSBsb2NhbGUubGFzdEluZGV4T2YoJy0nKTtcbiAgICB9XG4gICAgcmV0dXJuIGxvY2FsZXM7XG4gIH1cblxuICAvKipcbiAgICogU3BsaXQgYSBsb2NhbGUgaW50byBwYXJlbnQgbG9jYWxlcy4gXCJlcy1DT1wiIC0+IFtcImVzLUNPXCIsIFwiZXNcIl1cbiAgICpcbiAgICogQHBhcmFtIHBsdXJhbEZvcm0gLSBQbHVyYWwgZm9ybSBzdHJpbmcuLlxuICAgKiBAcmV0dXJucyBBbiBmdW5jdGlvbiB0byBjb21wdXRlIHBsdXJhbCBmb3Jtcy5cbiAgICovXG4gIC8vIGVzbGludC1kaXNhYmxlLW5leHQtbGluZSBAdHlwZXNjcmlwdC1lc2xpbnQvYmFuLXR5cGVzXG4gIHByaXZhdGUgZ2V0UGx1cmFsRnVuYyhwbHVyYWxGb3JtOiBzdHJpbmcpOiBGdW5jdGlvbiB7XG4gICAgLy8gUGx1cmFsIGZvcm0gc3RyaW5nIHJlZ2V4cFxuICAgIC8vIHRha2VuIGZyb20gaHR0cHM6Ly9naXRodWIuY29tL09yYW5nZS1PcGVuU291cmNlL2dldHRleHQuanMvYmxvYi9tYXN0ZXIvbGliLmdldHRleHQuanNcbiAgICAvLyBwbHVyYWwgZm9ybXMgbGlzdCBhdmFpbGFibGUgaGVyZSBodHRwOi8vbG9jYWxpemF0aW9uLWd1aWRlLnJlYWR0aGVkb2NzLm9yZy9lbi9sYXRlc3QvbDEwbi9wbHVyYWxmb3Jtcy5odG1sXG4gICAgbGV0IHBmX3JlID0gbmV3IFJlZ0V4cChcbiAgICAgICdeXFxcXHMqbnBsdXJhbHNcXFxccyo9XFxcXHMqWzAtOV0rXFxcXHMqO1xcXFxzKnBsdXJhbFxcXFxzKj1cXFxccyooPzpcXFxcc3xbLVxcXFw/XFxcXHwmPSE8PisqLyU6O24wLTlfKCldKSsnXG4gICAgKTtcblxuICAgIGlmICghcGZfcmUudGVzdChwbHVyYWxGb3JtKSlcbiAgICAgIHRocm93IG5ldyBFcnJvcihcbiAgICAgICAgR2V0dGV4dC5zdHJmbXQoJ1RoZSBwbHVyYWwgZm9ybSBcIiUxXCIgaXMgbm90IHZhbGlkJywgcGx1cmFsRm9ybSlcbiAgICAgICk7XG5cbiAgICAvLyBDYXJlZnVsIGhlcmUsIHRoaXMgaXMgYSBoaWRkZW4gZXZhbCgpIGVxdWl2YWxlbnQuLlxuICAgIC8vIFJpc2sgc2hvdWxkIGJlIHJlYXNvbmFibGUgdGhvdWdoIHNpbmNlIHdlIHRlc3QgdGhlIHBsdXJhbEZvcm0gdGhyb3VnaCByZWdleCBiZWZvcmVcbiAgICAvLyB0YWtlbiBmcm9tIGh0dHBzOi8vZ2l0aHViLmNvbS9PcmFuZ2UtT3BlblNvdXJjZS9nZXR0ZXh0LmpzL2Jsb2IvbWFzdGVyL2xpYi5nZXR0ZXh0LmpzXG4gICAgLy8gVE9ETzogc2hvdWxkIHRlc3QgaWYgaHR0cHM6Ly9naXRodWIuY29tL3NvbmV5L2pzZXAgcHJlc2VudCBhbmQgdXNlIGl0IGlmIHNvXG4gICAgcmV0dXJuIG5ldyBGdW5jdGlvbihcbiAgICAgICduJyxcbiAgICAgICdsZXQgcGx1cmFsLCBucGx1cmFsczsgJyArXG4gICAgICAgIHBsdXJhbEZvcm0gK1xuICAgICAgICAnIHJldHVybiB7IG5wbHVyYWxzOiBucGx1cmFscywgcGx1cmFsOiAocGx1cmFsID09PSB0cnVlID8gMSA6IChwbHVyYWwgPyBwbHVyYWwgOiAwKSkgfTsnXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgdGhlIGNvbnRleHQgZGVsaW1pdGVyIGZyb20gc3RyaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gc3RyIC0gVHJhbnNsYXRpb24gc3RyaW5nLlxuICAgKiBAcmV0dXJucyBBIHRyYW5zbGF0aW9uIHN0cmluZyB3aXRob3V0IGNvbnRleHQuXG4gICAqL1xuICBwcml2YXRlIHJlbW92ZUNvbnRleHQoc3RyOiBzdHJpbmcpOiBzdHJpbmcge1xuICAgIC8vIGlmIHRoZXJlIGlzIGNvbnRleHQsIHJlbW92ZSBpdFxuICAgIGlmIChzdHIuaW5kZXhPZih0aGlzLl9jb250ZXh0RGVsaW1pdGVyKSAhPT0gLTEpIHtcbiAgICAgIGxldCBwYXJ0cyA9IHN0ci5zcGxpdCh0aGlzLl9jb250ZXh0RGVsaW1pdGVyKTtcbiAgICAgIHJldHVybiBwYXJ0c1sxXTtcbiAgICB9XG4gICAgcmV0dXJuIHN0cjtcbiAgfVxuXG4gIC8qKlxuICAgKiBQcm9wZXIgdHJhbnNsYXRpb24gZnVuY3Rpb24gdGhhdCBoYW5kbGUgcGx1cmFscyBhbmQgZGlyZWN0aXZlcy5cbiAgICpcbiAgICogQHBhcmFtIG1lc3NhZ2VzIC0gTGlzdCBvZiB0cmFuc2xhdGlvbiBzdHJpbmdzLlxuICAgKiBAcGFyYW0gbiAtIFRoZSBudW1iZXIgZm9yIHBsdXJhbGl6YXRpb24uXG4gICAqIEBwYXJhbSBvcHRpb25zIC0gVHJhbnNsYXRpb24gb3B0aW9ucy5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgdmFyaWFibGVzIHRvIGludGVycG9sYXRlLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHRyYW5zbGF0aW9uIHN0cmluZyB3aXRob3V0IGNvbnRleHQuXG4gICAqXG4gICAqICMjIyBOb3Rlc1xuICAgKiBDb250YWlucyBqdWljeSBwYXJ0cyBvZiBodHRwczovL2dpdGh1Yi5jb20vT3JhbmdlLU9wZW5Tb3VyY2UvZ2V0dGV4dC5qcy9ibG9iL21hc3Rlci9saWIuZ2V0dGV4dC5qc1xuICAgKi9cbiAgcHJpdmF0ZSB0KFxuICAgIG1lc3NhZ2VzOiBBcnJheTxzdHJpbmc+LFxuICAgIG46IG51bWJlcixcbiAgICBvcHRpb25zOiBJVE9wdGlvbnMsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICAvLyBTaW5ndWxhciBpcyB2ZXJ5IGVhc3ksIGp1c3QgcGFzcyBkaWN0aW9uYXJ5IG1lc3NhZ2UgdGhyb3VnaCBzdHJmbXRcbiAgICBpZiAoIW9wdGlvbnMucGx1cmFsRm9ybSlcbiAgICAgIHJldHVybiAoXG4gICAgICAgIHRoaXMuX3N0cmluZ3NQcmVmaXggK1xuICAgICAgICBHZXR0ZXh0LnN0cmZtdCh0aGlzLnJlbW92ZUNvbnRleHQobWVzc2FnZXNbMF0pLCAuLi5hcmdzKVxuICAgICAgKTtcblxuICAgIGxldCBwbHVyYWw7XG5cbiAgICAvLyBpZiBhIHBsdXJhbCBmdW5jIGlzIGdpdmVuLCB1c2UgdGhhdCBvbmVcbiAgICBpZiAob3B0aW9ucy5wbHVyYWxGdW5jKSB7XG4gICAgICBwbHVyYWwgPSBvcHRpb25zLnBsdXJhbEZ1bmMobik7XG5cbiAgICAgIC8vIGlmIHBsdXJhbCBmb3JtIG5ldmVyIGludGVycHJldGVkIGJlZm9yZSwgZG8gaXQgbm93IGFuZCBzdG9yZSBpdFxuICAgIH0gZWxzZSBpZiAoIXRoaXMuX3BsdXJhbEZ1bmNzW29wdGlvbnMubG9jYWxlIHx8ICcnXSkge1xuICAgICAgdGhpcy5fcGx1cmFsRnVuY3Nbb3B0aW9ucy5sb2NhbGUgfHwgJyddID0gdGhpcy5nZXRQbHVyYWxGdW5jKFxuICAgICAgICB0aGlzLl9wbHVyYWxGb3Jtc1tvcHRpb25zLmxvY2FsZSB8fCAnJ11cbiAgICAgICk7XG4gICAgICBwbHVyYWwgPSB0aGlzLl9wbHVyYWxGdW5jc1tvcHRpb25zLmxvY2FsZSB8fCAnJ10obik7XG5cbiAgICAgIC8vIHdlIGhhdmUgdGhlIHBsdXJhbCBmdW5jdGlvbiwgY29tcHV0ZSB0aGUgcGx1cmFsIHJlc3VsdFxuICAgIH0gZWxzZSB7XG4gICAgICBwbHVyYWwgPSB0aGlzLl9wbHVyYWxGdW5jc1tvcHRpb25zLmxvY2FsZSB8fCAnJ10obik7XG4gICAgfVxuXG4gICAgLy8gSWYgdGhlcmUgaXMgYSBwcm9ibGVtIHdpdGggcGx1cmFscywgZmFsbGJhY2sgdG8gc2luZ3VsYXIgb25lXG4gICAgaWYgKFxuICAgICAgJ3VuZGVmaW5lZCcgPT09IHR5cGVvZiAhcGx1cmFsLnBsdXJhbCB8fFxuICAgICAgcGx1cmFsLnBsdXJhbCA+IHBsdXJhbC5ucGx1cmFscyB8fFxuICAgICAgbWVzc2FnZXMubGVuZ3RoIDw9IHBsdXJhbC5wbHVyYWxcbiAgICApXG4gICAgICBwbHVyYWwucGx1cmFsID0gMDtcblxuICAgIHJldHVybiAoXG4gICAgICB0aGlzLl9zdHJpbmdzUHJlZml4ICtcbiAgICAgIEdldHRleHQuc3RyZm10KFxuICAgICAgICB0aGlzLnJlbW92ZUNvbnRleHQobWVzc2FnZXNbcGx1cmFsLnBsdXJhbF0pLFxuICAgICAgICAuLi5bbl0uY29uY2F0KGFyZ3MpXG4gICAgICApXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgbWVzc2FnZXMgYWZ0ZXIgbG9hZGluZyB0aGVtLlxuICAgKlxuICAgKiBAcGFyYW0gZG9tYWluIC0gVGhlIHRyYW5zbGF0aW9uIGRvbWFpbi5cbiAgICogQHBhcmFtIGxvY2FsZSAtIFRoZSB0cmFuc2xhdGlvbiBsb2NhbGUuXG4gICAqIEBwYXJhbSBtZXNzYWdlcyAtIExpc3Qgb2YgdHJhbnNsYXRpb24gc3RyaW5ncy5cbiAgICogQHBhcmFtIHBsdXJhbEZvcm1zIC0gUGx1cmFsIGZvcm0gc3RyaW5nLlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogQ29udGFpbnMganVpY3kgcGFydHMgb2YgaHR0cHM6Ly9naXRodWIuY29tL09yYW5nZS1PcGVuU291cmNlL2dldHRleHQuanMvYmxvYi9tYXN0ZXIvbGliLmdldHRleHQuanNcbiAgICovXG4gIHByaXZhdGUgc2V0TWVzc2FnZXMoXG4gICAgZG9tYWluOiBzdHJpbmcsXG4gICAgbG9jYWxlOiBzdHJpbmcsXG4gICAgbWVzc2FnZXM6IElKc29uRGF0YU1lc3NhZ2VzLFxuICAgIHBsdXJhbEZvcm1zOiBzdHJpbmdcbiAgKTogdm9pZCB7XG4gICAgZG9tYWluID0gbm9ybWFsaXplRG9tYWluKGRvbWFpbik7XG5cbiAgICBpZiAocGx1cmFsRm9ybXMpIHRoaXMuX3BsdXJhbEZvcm1zW2xvY2FsZV0gPSBwbHVyYWxGb3JtcztcblxuICAgIGlmICghdGhpcy5fZGljdGlvbmFyeVtkb21haW5dKSB0aGlzLl9kaWN0aW9uYXJ5W2RvbWFpbl0gPSB7fTtcblxuICAgIHRoaXMuX2RpY3Rpb25hcnlbZG9tYWluXVtsb2NhbGVdID0gbWVzc2FnZXM7XG4gIH1cblxuICBwcml2YXRlIF9zdHJpbmdzUHJlZml4OiBzdHJpbmc7XG4gIHByaXZhdGUgX3BsdXJhbEZvcm1zOiBhbnk7XG4gIHByaXZhdGUgX2RpY3Rpb25hcnk6IGFueTtcbiAgcHJpdmF0ZSBfbG9jYWxlOiBzdHJpbmc7XG4gIHByaXZhdGUgX2RvbWFpbjogc3RyaW5nO1xuICBwcml2YXRlIF9jb250ZXh0RGVsaW1pdGVyOiBzdHJpbmc7XG4gIHByaXZhdGUgX3BsdXJhbEZ1bmNzOiBhbnk7XG4gIHByaXZhdGUgX2RlZmF1bHRzOiBhbnk7XG59XG5cbmV4cG9ydCB7IEdldHRleHQgfTtcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHRyYW5zbGF0aW9uXG4gKi9cblxuLy8gTm90ZToga2VlcCBpbiBhbHBoYWJldGljYWwgb3JkZXIuLi5cbmV4cG9ydCAqIGZyb20gJy4vYmFzZSc7XG5leHBvcnQgKiBmcm9tICcuL2dldHRleHQnO1xuZXhwb3J0ICogZnJvbSAnLi9tYW5hZ2VyJztcbmV4cG9ydCAqIGZyb20gJy4vc2VydmVyJztcbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgU2VydmVyQ29ubmVjdGlvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcbmltcG9ydCB7IEdldHRleHQgfSBmcm9tICcuL2dldHRleHQnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlLCBUcmFuc2xhdG9yQ29ubmVjdG9yIH0gZnJvbSAnLi90b2tlbnMnO1xuaW1wb3J0IHsgbm9ybWFsaXplRG9tYWluIH0gZnJvbSAnLi91dGlscyc7XG5cbi8qKlxuICogVHJhbnNsYXRpb24gTWFuYWdlclxuICovXG5leHBvcnQgY2xhc3MgVHJhbnNsYXRpb25NYW5hZ2VyIGltcGxlbWVudHMgSVRyYW5zbGF0b3Ige1xuICBjb25zdHJ1Y3RvcihcbiAgICB0cmFuc2xhdGlvbnNVcmw6IHN0cmluZyA9ICcnLFxuICAgIHN0cmluZ3NQcmVmaXg/OiBzdHJpbmcsXG4gICAgc2VydmVyU2V0dGluZ3M/OiBTZXJ2ZXJDb25uZWN0aW9uLklTZXR0aW5nc1xuICApIHtcbiAgICB0aGlzLl9jb25uZWN0b3IgPSBuZXcgVHJhbnNsYXRvckNvbm5lY3Rvcih0cmFuc2xhdGlvbnNVcmwsIHNlcnZlclNldHRpbmdzKTtcbiAgICB0aGlzLl9zdHJpbmdzUHJlZml4ID0gc3RyaW5nc1ByZWZpeCB8fCAnJztcbiAgICB0aGlzLl9lbmdsaXNoQnVuZGxlID0gbmV3IEdldHRleHQoeyBzdHJpbmdzUHJlZml4OiB0aGlzLl9zdHJpbmdzUHJlZml4IH0pO1xuICB9XG5cbiAgZ2V0IGxhbmd1YWdlQ29kZSgpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLl9jdXJyZW50TG9jYWxlO1xuICB9XG5cbiAgLyoqXG4gICAqIEZldGNoIHRoZSBsb2NhbGl6YXRpb24gZGF0YSBmcm9tIHRoZSBzZXJ2ZXIuXG4gICAqXG4gICAqIEBwYXJhbSBsb2NhbGUgVGhlIGxhbmd1YWdlIGxvY2FsZSB0byB1c2UgZm9yIHRyYW5zbGF0aW9ucy5cbiAgICovXG4gIGFzeW5jIGZldGNoKGxvY2FsZTogc3RyaW5nKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgdGhpcy5fbGFuZ3VhZ2VEYXRhID0gYXdhaXQgdGhpcy5fY29ubmVjdG9yLmZldGNoKHsgbGFuZ3VhZ2U6IGxvY2FsZSB9KTtcbiAgICBpZiAodGhpcy5fbGFuZ3VhZ2VEYXRhICYmIGxvY2FsZSA9PT0gJ2RlZmF1bHQnKSB7XG4gICAgICB0cnkge1xuICAgICAgICBmb3IgKGNvbnN0IGxhbmcgb2YgT2JqZWN0LnZhbHVlcyh0aGlzLl9sYW5ndWFnZURhdGEuZGF0YSA/PyB7fSkpIHtcbiAgICAgICAgICB0aGlzLl9jdXJyZW50TG9jYWxlID1cbiAgICAgICAgICAgIC8vIElmIHRoZSBsYW5ndWFnZSBpcyBwcm92aWRlZCBieSB0aGUgc3lzdGVtIHNldCB1cCwgd2UgbmVlZCB0byByZXRyaWV2ZSB0aGUgZmluYWxcbiAgICAgICAgICAgIC8vIGxhbmd1YWdlLiBUaGlzIGlzIGRvbmUgdGhyb3VnaCB0aGUgYFwiXCJgIGVudHJ5IGluIGBfbGFuZ3VhZ2VEYXRhYCB0aGF0IGNvbnRhaW5zXG4gICAgICAgICAgICAvLyBsYW5ndWFnZSBtZXRhZGF0YS5cbiAgICAgICAgICAgICgobGFuZyBhcyBhbnkpWycnXVsnbGFuZ3VhZ2UnXSBhcyBzdHJpbmcpLnJlcGxhY2UoJ18nLCAnLScpO1xuICAgICAgICAgIGJyZWFrO1xuICAgICAgICB9XG4gICAgICB9IGNhdGNoIChyZWFzb24pIHtcbiAgICAgICAgdGhpcy5fY3VycmVudExvY2FsZSA9ICdlbic7XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHRoaXMuX2N1cnJlbnRMb2NhbGUgPSBsb2NhbGU7XG4gICAgfVxuXG4gICAgdGhpcy5fZG9tYWluRGF0YSA9IHRoaXMuX2xhbmd1YWdlRGF0YT8uZGF0YSA/PyB7fTtcbiAgICBjb25zdCBtZXNzYWdlOiBzdHJpbmcgPSB0aGlzLl9sYW5ndWFnZURhdGE/Lm1lc3NhZ2U7XG4gICAgaWYgKG1lc3NhZ2UgJiYgbG9jYWxlICE9PSAnZW4nKSB7XG4gICAgICBjb25zb2xlLndhcm4obWVzc2FnZSk7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIExvYWQgdHJhbnNsYXRpb24gYnVuZGxlcyBmb3IgYSBnaXZlbiBkb21haW4uXG4gICAqXG4gICAqIEBwYXJhbSBkb21haW4gVGhlIHRyYW5zbGF0aW9uIGRvbWFpbiB0byB1c2UgZm9yIHRyYW5zbGF0aW9ucy5cbiAgICovXG4gIGxvYWQoZG9tYWluOiBzdHJpbmcpOiBUcmFuc2xhdGlvbkJ1bmRsZSB7XG4gICAgaWYgKHRoaXMuX2RvbWFpbkRhdGEpIHtcbiAgICAgIGlmICh0aGlzLl9jdXJyZW50TG9jYWxlID09ICdlbicpIHtcbiAgICAgICAgcmV0dXJuIHRoaXMuX2VuZ2xpc2hCdW5kbGU7XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBkb21haW4gPSBub3JtYWxpemVEb21haW4oZG9tYWluKTtcbiAgICAgICAgaWYgKCEoZG9tYWluIGluIHRoaXMuX3RyYW5zbGF0aW9uQnVuZGxlcykpIHtcbiAgICAgICAgICBsZXQgdHJhbnNsYXRpb25CdW5kbGUgPSBuZXcgR2V0dGV4dCh7XG4gICAgICAgICAgICBkb21haW46IGRvbWFpbixcbiAgICAgICAgICAgIGxvY2FsZTogdGhpcy5fY3VycmVudExvY2FsZSxcbiAgICAgICAgICAgIHN0cmluZ3NQcmVmaXg6IHRoaXMuX3N0cmluZ3NQcmVmaXhcbiAgICAgICAgICB9KTtcbiAgICAgICAgICBpZiAoZG9tYWluIGluIHRoaXMuX2RvbWFpbkRhdGEpIHtcbiAgICAgICAgICAgIGxldCBtZXRhZGF0YSA9IHRoaXMuX2RvbWFpbkRhdGFbZG9tYWluXVsnJ107XG4gICAgICAgICAgICBpZiAoJ3BsdXJhbF9mb3JtcycgaW4gbWV0YWRhdGEpIHtcbiAgICAgICAgICAgICAgbWV0YWRhdGEucGx1cmFsRm9ybXMgPSBtZXRhZGF0YS5wbHVyYWxfZm9ybXM7XG4gICAgICAgICAgICAgIGRlbGV0ZSBtZXRhZGF0YS5wbHVyYWxfZm9ybXM7XG4gICAgICAgICAgICAgIHRoaXMuX2RvbWFpbkRhdGFbZG9tYWluXVsnJ10gPSBtZXRhZGF0YTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHRyYW5zbGF0aW9uQnVuZGxlLmxvYWRKU09OKHRoaXMuX2RvbWFpbkRhdGFbZG9tYWluXSwgZG9tYWluKTtcbiAgICAgICAgICB9XG4gICAgICAgICAgdGhpcy5fdHJhbnNsYXRpb25CdW5kbGVzW2RvbWFpbl0gPSB0cmFuc2xhdGlvbkJ1bmRsZTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdGhpcy5fdHJhbnNsYXRpb25CdW5kbGVzW2RvbWFpbl07XG4gICAgICB9XG4gICAgfSBlbHNlIHtcbiAgICAgIHJldHVybiB0aGlzLl9lbmdsaXNoQnVuZGxlO1xuICAgIH1cbiAgfVxuXG4gIHByaXZhdGUgX2Nvbm5lY3RvcjogVHJhbnNsYXRvckNvbm5lY3RvcjtcbiAgcHJpdmF0ZSBfY3VycmVudExvY2FsZTogc3RyaW5nO1xuICBwcml2YXRlIF9kb21haW5EYXRhOiBhbnkgPSB7fTtcbiAgcHJpdmF0ZSBfZW5nbGlzaEJ1bmRsZTogR2V0dGV4dDtcbiAgcHJpdmF0ZSBfbGFuZ3VhZ2VEYXRhOiBhbnk7XG4gIHByaXZhdGUgX3N0cmluZ3NQcmVmaXg6IHN0cmluZztcbiAgcHJpdmF0ZSBfdHJhbnNsYXRpb25CdW5kbGVzOiBhbnkgPSB7fTtcbn1cbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgVVJMRXh0IH0gZnJvbSAnQGp1cHl0ZXJsYWIvY29yZXV0aWxzJztcblxuaW1wb3J0IHsgU2VydmVyQ29ubmVjdGlvbiB9IGZyb20gJ0BqdXB5dGVybGFiL3NlcnZpY2VzJztcblxuLyoqXG4gKiBUaGUgdXJsIGZvciB0aGUgdHJhbnNsYXRpb25zIHNlcnZpY2UuXG4gKi9cbmNvbnN0IFRSQU5TTEFUSU9OU19TRVRUSU5HU19VUkwgPSAnYXBpL3RyYW5zbGF0aW9ucyc7XG5cbi8qKlxuICogQ2FsbCB0aGUgQVBJIGV4dGVuc2lvblxuICpcbiAqIEBwYXJhbSBsb2NhbGUgQVBJIFJFU1QgZW5kIHBvaW50IGZvciB0aGUgZXh0ZW5zaW9uXG4gKiBAcGFyYW0gaW5pdCBJbml0aWFsIHZhbHVlcyBmb3IgdGhlIHJlcXVlc3RcbiAqIEByZXR1cm5zIFRoZSByZXNwb25zZSBib2R5IGludGVycHJldGVkIGFzIEpTT05cbiAqL1xuZXhwb3J0IGFzeW5jIGZ1bmN0aW9uIHJlcXVlc3RUcmFuc2xhdGlvbnNBUEk8VD4oXG4gIHRyYW5zbGF0aW9uc1VybDogc3RyaW5nID0gJycsXG4gIGxvY2FsZSA9ICcnLFxuICBpbml0OiBSZXF1ZXN0SW5pdCA9IHt9LFxuICBzZXJ2ZXJTZXR0aW5nczogU2VydmVyQ29ubmVjdGlvbi5JU2V0dGluZ3MgfCB1bmRlZmluZWQgPSB1bmRlZmluZWRcbik6IFByb21pc2U8VD4ge1xuICAvLyBNYWtlIHJlcXVlc3QgdG8gSnVweXRlciBBUElcbiAgY29uc3Qgc2V0dGluZ3MgPSBzZXJ2ZXJTZXR0aW5ncyA/PyBTZXJ2ZXJDb25uZWN0aW9uLm1ha2VTZXR0aW5ncygpO1xuICB0cmFuc2xhdGlvbnNVcmwgPVxuICAgIHRyYW5zbGF0aW9uc1VybCB8fCBgJHtzZXR0aW5ncy5hcHBVcmx9LyR7VFJBTlNMQVRJT05TX1NFVFRJTkdTX1VSTH1gO1xuICBjb25zdCByZXF1ZXN0VXJsID0gVVJMRXh0LmpvaW4oc2V0dGluZ3MuYmFzZVVybCwgdHJhbnNsYXRpb25zVXJsLCBsb2NhbGUpO1xuICBsZXQgcmVzcG9uc2U6IFJlc3BvbnNlO1xuICB0cnkge1xuICAgIHJlc3BvbnNlID0gYXdhaXQgU2VydmVyQ29ubmVjdGlvbi5tYWtlUmVxdWVzdChyZXF1ZXN0VXJsLCBpbml0LCBzZXR0aW5ncyk7XG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uTmV0d29ya0Vycm9yKGVycm9yKTtcbiAgfVxuXG4gIGxldCBkYXRhOiBhbnkgPSBhd2FpdCByZXNwb25zZS50ZXh0KCk7XG5cbiAgaWYgKGRhdGEubGVuZ3RoID4gMCkge1xuICAgIHRyeSB7XG4gICAgICBkYXRhID0gSlNPTi5wYXJzZShkYXRhKTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgY29uc29sZS5lcnJvcignTm90IGEgSlNPTiByZXNwb25zZSBib2R5LicsIHJlc3BvbnNlKTtcbiAgICB9XG4gIH1cblxuICBpZiAoIXJlc3BvbnNlLm9rKSB7XG4gICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uUmVzcG9uc2VFcnJvcihyZXNwb25zZSwgZGF0YS5tZXNzYWdlIHx8IGRhdGEpO1xuICB9XG5cbiAgcmV0dXJuIGRhdGE7XG59XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuXG5pbXBvcnQgdHlwZSB7IElSZW5kZXJNaW1lIH0gZnJvbSAnQGp1cHl0ZXJsYWIvcmVuZGVybWltZS1pbnRlcmZhY2VzJztcbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBEYXRhQ29ubmVjdG9yLCBJRGF0YUNvbm5lY3RvciB9IGZyb20gJ0BqdXB5dGVybGFiL3N0YXRlZGInO1xuaW1wb3J0IHsgVG9rZW4gfSBmcm9tICdAbHVtaW5vL2NvcmV1dGlscyc7XG5pbXBvcnQgeyByZXF1ZXN0VHJhbnNsYXRpb25zQVBJIH0gZnJvbSAnLi9zZXJ2ZXInO1xuXG4vKlxuICogVHJhbnNsYXRpb25cbiAqL1xuZXhwb3J0IHR5cGUgTGFuZ3VhZ2UgPSB7IFtrZXk6IHN0cmluZ106IHN0cmluZyB9O1xuXG4vKipcbiAqIFRyYW5zbGF0aW9uIGNvbm5lY3Rpb24gaW50ZXJmYWNlLlxuICovXG5leHBvcnQgaW50ZXJmYWNlIElUcmFuc2xhdG9yQ29ubmVjdG9yXG4gIGV4dGVuZHMgSURhdGFDb25uZWN0b3I8TGFuZ3VhZ2UsIExhbmd1YWdlLCB7IGxhbmd1YWdlOiBzdHJpbmcgfT4ge31cblxuLyoqXG4gKiBBIHNlcnZpY2UgdG8gY29ubmVjdCB0byB0aGUgc2VydmVyIHRyYW5zbGF0aW9uIGVuZHBvaW50XG4gKi9cbmV4cG9ydCBjb25zdCBJVHJhbnNsYXRvckNvbm5lY3RvciA9IG5ldyBUb2tlbjxJVHJhbnNsYXRvckNvbm5lY3Rvcj4oXG4gICdAanVweXRlcmxhYi90cmFuc2xhdGlvbjpJVHJhbnNsYXRvckNvbm5lY3RvcicsXG4gICdBIHNlcnZpY2UgdG8gY29ubmVjdCB0byB0aGUgc2VydmVyIHRyYW5zbGF0aW9uIGVuZHBvaW50Lidcbik7XG5cbmV4cG9ydCBjbGFzcyBUcmFuc2xhdG9yQ29ubmVjdG9yXG4gIGV4dGVuZHMgRGF0YUNvbm5lY3RvcjxMYW5ndWFnZSwgTGFuZ3VhZ2UsIHsgbGFuZ3VhZ2U6IHN0cmluZyB9PlxuICBpbXBsZW1lbnRzIElUcmFuc2xhdG9yQ29ubmVjdG9yXG57XG4gIGNvbnN0cnVjdG9yKFxuICAgIHRyYW5zbGF0aW9uc1VybDogc3RyaW5nID0gJycsXG4gICAgc2VydmVyU2V0dGluZ3M/OiBTZXJ2ZXJDb25uZWN0aW9uLklTZXR0aW5nc1xuICApIHtcbiAgICBzdXBlcigpO1xuICAgIHRoaXMuX3RyYW5zbGF0aW9uc1VybCA9IHRyYW5zbGF0aW9uc1VybDtcbiAgICB0aGlzLl9zZXJ2ZXJTZXR0aW5ncyA9IHNlcnZlclNldHRpbmdzO1xuICB9XG5cbiAgYXN5bmMgZmV0Y2gob3B0czogeyBsYW5ndWFnZTogc3RyaW5nIH0pOiBQcm9taXNlPExhbmd1YWdlPiB7XG4gICAgcmV0dXJuIHJlcXVlc3RUcmFuc2xhdGlvbnNBUEkoXG4gICAgICB0aGlzLl90cmFuc2xhdGlvbnNVcmwsXG4gICAgICBvcHRzLmxhbmd1YWdlLFxuICAgICAge30sXG4gICAgICB0aGlzLl9zZXJ2ZXJTZXR0aW5nc1xuICAgICk7XG4gIH1cblxuICBwcml2YXRlIF9zZXJ2ZXJTZXR0aW5nczogU2VydmVyQ29ubmVjdGlvbi5JU2V0dGluZ3MgfCB1bmRlZmluZWQ7XG4gIHByaXZhdGUgX3RyYW5zbGF0aW9uc1VybDogc3RyaW5nO1xufVxuXG4vKipcbiAqIEJ1bmRsZSBvZiBnZXR0ZXh0LWJhc2VkIHRyYW5zbGF0aW9uIGZ1bmN0aW9ucyBmb3IgYSBzcGVjaWZpYyBkb21haW4uXG4gKi9cbmV4cG9ydCB0eXBlIFRyYW5zbGF0aW9uQnVuZGxlID0gSVJlbmRlck1pbWUuVHJhbnNsYXRpb25CdW5kbGU7XG5cbi8qKlxuICogVHJhbnNsYXRpb24gcHJvdmlkZXIgaW50ZXJmYWNlXG4gKi9cbmV4cG9ydCBpbnRlcmZhY2UgSVRyYW5zbGF0b3IgZXh0ZW5kcyBJUmVuZGVyTWltZS5JVHJhbnNsYXRvciB7fVxuXG4vKipcbiAqIFRyYW5zbGF0aW9uIHByb3ZpZGVyIHRva2VuXG4gKi9cbmV4cG9ydCBjb25zdCBJVHJhbnNsYXRvciA9IG5ldyBUb2tlbjxJVHJhbnNsYXRvcj4oXG4gICdAanVweXRlcmxhYi90cmFuc2xhdGlvbjpJVHJhbnNsYXRvcicsXG4gICdBIHNlcnZpY2UgdG8gdHJhbnNsYXRlIHN0cmluZ3MuJ1xuKTtcbiIsIi8qXG4gKiBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbiAqIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4gKi9cblxuLyoqXG4gKiBOb3JtYWxpemUgZG9tYWluXG4gKlxuICogQHBhcmFtIGRvbWFpbiBEb21haW4gdG8gbm9ybWFsaXplXG4gKiBAcmV0dXJucyBOb3JtYWxpemVkIGRvbWFpblxuICovXG5leHBvcnQgZnVuY3Rpb24gbm9ybWFsaXplRG9tYWluKGRvbWFpbjogc3RyaW5nKTogc3RyaW5nIHtcbiAgcmV0dXJuIGRvbWFpbi5yZXBsYWNlKCctJywgJ18nKTtcbn1cbiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==