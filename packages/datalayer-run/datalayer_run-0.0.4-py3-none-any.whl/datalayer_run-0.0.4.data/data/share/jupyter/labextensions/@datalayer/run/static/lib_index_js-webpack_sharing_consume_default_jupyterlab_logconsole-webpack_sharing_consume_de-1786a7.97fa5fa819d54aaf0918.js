"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["lib_index_js-webpack_sharing_consume_default_jupyterlab_logconsole-webpack_sharing_consume_de-1786a7"],{

/***/ "./lib/RunJupyterLab.js":
/*!******************************!*\
  !*** ./lib/RunJupyterLab.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunJupyterLab": () => (/* binding */ RunJupyterLab),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @datalayer/jupyter-react */ "webpack/sharing/consume/default/@datalayer/jupyter-react/@datalayer/jupyter-react");
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/theme-light-extension */ "webpack/sharing/consume/default/@jupyterlab/theme-light-extension");
/* harmony import */ var _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyter_collaboration_extension__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyter/collaboration-extension */ "../../../node_modules/@jupyter/collaboration-extension/lib/index.js");
/* harmony import */ var _jupyterlab_index__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./jupyterlab/index */ "./lib/jupyterlab/index.js");





const JupyterLabComponent = () => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__.JupyterLabApp, { extensions: [
        _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_2__,
        _jupyter_collaboration_extension__WEBPACK_IMPORTED_MODULE_3__,
        _jupyterlab_index__WEBPACK_IMPORTED_MODULE_4__,
    ], disabledExtensions: [
    //      "@jupyterlab/apputils-extension:sessionDialogs"
    ], position: "absolute", height: "100vh" }));
const RunJupyterLab = () => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_1__.Jupyter, { startDefaultKernel: false, disableCssLoading: true, collaborative: true, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(JupyterLabComponent, {}) }));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (RunJupyterLab);


/***/ }),

/***/ "./lib/RunJupyterLabHeadless.js":
/*!**************************************!*\
  !*** ./lib/RunJupyterLabHeadless.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunJupyterLabHeadless": () => (/* binding */ RunJupyterLabHeadless),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! styled-components */ "webpack/sharing/consume/default/styled-components/styled-components?16a2");
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(styled_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @datalayer/jupyter-react */ "webpack/sharing/consume/default/@datalayer/jupyter-react/@datalayer/jupyter-react");
/* harmony import */ var _datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _Run__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./Run */ "./lib/Run.js");
/* harmony import */ var _jupyterlab_plugins__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./jupyterlab/plugins */ "./lib/jupyterlab/plugins.js");
/* harmony import */ var _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/theme-light-extension */ "webpack/sharing/consume/default/@jupyterlab/theme-light-extension");
/* harmony import */ var _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyter_collaboration_extension__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyter/collaboration-extension */ "../../../node_modules/@jupyter/collaboration-extension/lib/index.js");
/* harmony import */ var _jupyterlab_index__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./jupyterlab/index */ "./lib/jupyterlab/index.js");









const ThemeGlobalStyle = styled_components__WEBPACK_IMPORTED_MODULE_2__.createGlobalStyle `
  body {
    background-color: white !important;
    overflow: auto;
  }
`;
const JupyterLabHeadless = (props) => {
    const [jupyterLabAppAdapter, setJupyterLabAppAdapter] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)();
    const { inRouter } = props;
    const onJupyterLab = (jupyterLabAppAdapter) => {
        setJupyterLabAppAdapter(jupyterLabAppAdapter);
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: [jupyterLabAppAdapter && (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_Run__WEBPACK_IMPORTED_MODULE_5__["default"], { adapter: jupyterLabAppAdapter, inRouter: inRouter }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_3__.JupyterLabApp, { extensionPromises: (0,_jupyterlab_plugins__WEBPACK_IMPORTED_MODULE_6__.plugins)(false).extensionPromises, extensions: [
                    _jupyterlab_theme_light_extension__WEBPACK_IMPORTED_MODULE_4__,
                    _jupyter_collaboration_extension__WEBPACK_IMPORTED_MODULE_7__,
                    _jupyterlab_index__WEBPACK_IMPORTED_MODULE_8__,
                ], headless: true, disabledExtensions: [
                //          "@jupyterlab/apputils-extension:sessionDialogs"
                ], onJupyterLab: onJupyterLab })] }));
};
const RunJupyterLabHeadless = (props) => ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_datalayer_jupyter_react__WEBPACK_IMPORTED_MODULE_3__.Jupyter, { startDefaultKernel: false, disableCssLoading: true, collaborative: true, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(ThemeGlobalStyle, {}), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(JupyterLabHeadless, { ...props })] }));
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (RunJupyterLabHeadless);


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RunJupyterLab": () => (/* reexport safe */ _RunJupyterLab__WEBPACK_IMPORTED_MODULE_0__.RunJupyterLab),
/* harmony export */   "RunJupyterLabHeadless": () => (/* reexport safe */ _RunJupyterLabHeadless__WEBPACK_IMPORTED_MODULE_1__.RunJupyterLabHeadless),
/* harmony export */   "RunRoutes": () => (/* reexport safe */ _RunRoutes__WEBPACK_IMPORTED_MODULE_2__.RunRoutes)
/* harmony export */ });
/* harmony import */ var _RunJupyterLab__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./RunJupyterLab */ "./lib/RunJupyterLab.js");
/* harmony import */ var _RunJupyterLabHeadless__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./RunJupyterLabHeadless */ "./lib/RunJupyterLabHeadless.js");
/* harmony import */ var _RunRoutes__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./RunRoutes */ "./lib/RunRoutes.js");





/***/ }),

/***/ "./lib/jupyterlab/plugins.js":
/*!***********************************!*\
  !*** ./lib/jupyterlab/plugins.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "plugins": () => (/* binding */ plugins)
/* harmony export */ });
const plugins = (collaborative) => {
    return {
        extensionPromises: [
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_application-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/application-extension */ "webpack/sharing/consume/default/@jupyterlab/application-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_apputils-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/apputils-extension */ "webpack/sharing/consume/default/@jupyterlab/apputils-extension", 23)).then(plugins => plugins.default.filter(({ id }) => !(id.endsWith(':sessionDialogs')))),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_codemirror-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/codemirror-extension */ "webpack/sharing/consume/default/@jupyterlab/codemirror-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_cell-toolbar-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/cell-toolbar-extension */ "webpack/sharing/consume/default/@jupyterlab/cell-toolbar-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_completer-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/completer-extension */ "webpack/sharing/consume/default/@jupyterlab/completer-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_console-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/console-extension */ "webpack/sharing/consume/default/@jupyterlab/console-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_docmanager-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/docmanager-extension */ "webpack/sharing/consume/default/@jupyterlab/docmanager-extension", 23)).then(plugins => plugins.default.filter(({ id }) => !(id.endsWith(':manager')))),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_documentsearch-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/documentsearch-extension */ "webpack/sharing/consume/default/@jupyterlab/documentsearch-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_filebrowser-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/filebrowser-extension */ "webpack/sharing/consume/default/@jupyterlab/filebrowser-extension", 23)).then(plugins => {
                if (collaborative) {
                    return plugins.default.filter(({ id }) => !(id.endsWith(':default-file-browser') // For RTC.
                    ));
                }
                else {
                    return plugins.default;
                }
            }),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_mainmenu-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/mainmenu-extension */ "webpack/sharing/consume/default/@jupyterlab/mainmenu-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_markdownviewer-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/markdownviewer-extension */ "webpack/sharing/consume/default/@jupyterlab/markdownviewer-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_markedparser-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/markedparser-extension */ "webpack/sharing/consume/default/@jupyterlab/markedparser-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_fileeditor-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/fileeditor-extension */ "webpack/sharing/consume/default/@jupyterlab/fileeditor-extension", 23)).then(plugins => plugins.default.filter(({ id }) => !(id.includes(':language-server')))),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_launcher-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/launcher-extension */ "webpack/sharing/consume/default/@jupyterlab/launcher-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_notebook-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/notebook-extension */ "webpack/sharing/consume/default/@jupyterlab/notebook-extension", 23)).then(plugins => {
                return plugins.default.filter(({ id }) => !(id.includes(':language-server') ||
                    id.endsWith(':update-raw-mimetype')));
            }),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_rendermime-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/rendermime-extension */ "webpack/sharing/consume/default/@jupyterlab/rendermime-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_shortcuts-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/shortcuts-extension */ "webpack/sharing/consume/default/@jupyterlab/shortcuts-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_statusbar-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/statusbar-extension */ "webpack/sharing/consume/default/@jupyterlab/statusbar-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_translation-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/translation-extension */ "webpack/sharing/consume/default/@jupyterlab/translation-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_toc-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/toc-extension */ "webpack/sharing/consume/default/@jupyterlab/toc-extension", 23)),
            __webpack_require__.e(/*! import() */ "webpack_sharing_consume_default_jupyterlab_ui-components-extension").then(__webpack_require__.t.bind(__webpack_require__, /*! @jupyterlab/ui-components-extension */ "webpack/sharing/consume/default/@jupyterlab/ui-components-extension", 23)),
        ],
    };
};


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_jupyterlab_logconsole-webpack_sharing_consume_de-1786a7.97fa5fa819d54aaf0918.js.map