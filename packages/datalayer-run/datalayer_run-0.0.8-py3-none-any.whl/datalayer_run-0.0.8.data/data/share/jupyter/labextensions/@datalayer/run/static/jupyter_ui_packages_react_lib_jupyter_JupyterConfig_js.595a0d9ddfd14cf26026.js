"use strict";
(self["webpackChunk_datalayer_run"] = self["webpackChunk_datalayer_run"] || []).push([["jupyter_ui_packages_react_lib_jupyter_JupyterConfig_js"],{

/***/ "../../jupyter/ui/packages/react/lib/jupyter/JupyterConfig.js":
/*!********************************************************************!*\
  !*** ../../jupyter/ui/packages/react/lib/jupyter/JupyterConfig.js ***!
  \********************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getJupyterServerHttpUrl": () => (/* binding */ getJupyterServerHttpUrl),
/* harmony export */   "getJupyterServerWsUrl": () => (/* binding */ getJupyterServerWsUrl),
/* harmony export */   "getJupyterToken": () => (/* binding */ getJupyterToken),
/* harmony export */   "loadJupyterConfig": () => (/* binding */ loadJupyterConfig),
/* harmony export */   "setJupyterServerHttpUrl": () => (/* binding */ setJupyterServerHttpUrl),
/* harmony export */   "setJupyterServerWsUrl": () => (/* binding */ setJupyterServerWsUrl),
/* harmony export */   "setJupyterToken": () => (/* binding */ setJupyterToken)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The default Jupyter configuration.
 */
let config = {
    jupyterServerHttpUrl: '',
    jupyterServerWsUrl: '',
    jupyterToken: '',
    insideJupyterLab: false,
    insideJupyterHub: false,
};
/**
 * Setter for jupyterServerHttpUrl.
 */
const setJupyterServerHttpUrl = (jupyterServerHttpUrl) => {
    config.jupyterServerHttpUrl = jupyterServerHttpUrl;
};
/**
 * Getter for jupyterServerHttpUrl.
 */
const getJupyterServerHttpUrl = () => config.jupyterServerHttpUrl;
/**
 * Setter for jupyterServerWsUrl.
 */
const setJupyterServerWsUrl = (jupyterServerWsUrl) => {
    config.jupyterServerWsUrl = jupyterServerWsUrl;
};
/**
 * Getter for jupyterServerWsUrl.
 */
const getJupyterServerWsUrl = () => config.jupyterServerWsUrl;
/**
 * Setter for jupyterToken.
 */
const setJupyterToken = (jupyterToken) => {
    config.jupyterToken = jupyterToken;
};
/**
 * Getter for jupyterToken.
 */
const getJupyterToken = () => config.jupyterToken;
/**
 * Method to load the Jupyter configuration from the
 * host HTML page.
 */
const loadJupyterConfig = (props) => {
    const { lite, jupyterServerHttpUrl, jupyterServerWsUrl, collaborative, terminals, jupyterToken } = props;
    const datalayerConfigData = document.getElementById('datalayer-config-data');
    if (datalayerConfigData) {
        config = JSON.parse(datalayerConfigData.textContent || '');
        setJupyterServerHttpUrl(jupyterServerHttpUrl ?? config.jupyterServerHttpUrl ?? location.protocol + '//' + location.host + "/api/jupyter");
        setJupyterServerWsUrl(jupyterServerWsUrl ?? config.jupyterServerWsUrl ?? location.protocol.replace('http', 'ws') + '//' + location.host + "/api/jupyter");
        setJupyterToken(jupyterToken ?? config.jupyterToken ?? '');
    }
    else {
        // No Datalayer Config.
        const jupyterConfigData = document.getElementById('jupyter-config-data');
        if (jupyterConfigData) {
            const jupyterConfig = JSON.parse(jupyterConfigData.textContent || '');
            setJupyterServerHttpUrl(jupyterServerHttpUrl ?? location.protocol + '//' + location.host + jupyterConfig.baseUrl);
            setJupyterServerWsUrl(jupyterServerWsUrl ?? location.protocol === "https" ? "wss://" + location.host : "ws://" + location.host + jupyterConfig.baseUrl);
            setJupyterToken(jupyterToken ?? jupyterConfig.token);
            config.insideJupyterLab = jupyterConfig.appName === 'JupyterLab';
        }
        else {
            // No Datalayer and no JupyterLab Config.
            setJupyterServerHttpUrl(jupyterServerHttpUrl ?? location.protocol + '//' + location.host + "/api/jupyter");
            setJupyterServerWsUrl(jupyterServerWsUrl ?? location.protocol.replace('http', 'ws') + '//' + location.host + "/api/jupyter");
            setJupyterToken(jupyterToken ?? '');
        }
    }
    if (lite) {
        setJupyterServerHttpUrl(location.protocol + '//' + location.host);
        setJupyterServerWsUrl(location.protocol === "https" ? "wss://" + location.host : "ws://" + location.host);
    }
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('baseUrl', getJupyterServerHttpUrl());
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('wsUrl', getJupyterServerWsUrl());
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('token', getJupyterToken());
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('collaborative', String(collaborative));
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('disableRTC', String(!collaborative));
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('terminalsAvailable', String(terminals));
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('mathjaxUrl', 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js');
    _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.setOption('mathjaxConfig', 'TeX-AMS_CHTML-full,Safe');
    //  PageConfig.getOption('hubHost')
    //  PageConfig.getOption('hubPrefix')
    //  PageConfig.getOption('hubUser')
    //  PageConfig.getOption('hubServerName')
    config.insideJupyterHub = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PageConfig.getOption('hubHost') !== "";
    return config;
};


/***/ })

}]);
//# sourceMappingURL=jupyter_ui_packages_react_lib_jupyter_JupyterConfig_js.595a0d9ddfd14cf26026.js.map