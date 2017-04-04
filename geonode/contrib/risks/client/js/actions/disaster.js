/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const DATA_LOADING = 'DATA_LOADING';
const DATA_LOADED = 'DATA_LOADED';
const DATA_ERROR = 'DATA_ERROR';
const GET_DATA = 'GET_DATA';
const ANALYSIS_DATA_LOADED = 'ANALYSIS_DATA_LOADED';
const TOGGLE_DIM = 'TOGGLE_DIM';
const SET_DIM_IDX = 'SET_DIM_IDX';
const FEATURES_LOADING = 'FEATURES_LOADING';
const FEATURES_LOADED = 'FEATURES_LOADED';
const FEATURES_ERROR = 'FEATURES_ERROR';
const TOGGLE_ADMIN_UNITS = 'TOGGLE_ADMIN_UNITS';
const LOAD_RISK_MAP_CONFIG = 'LOAD_RISK_MAP_CONFIG';
const GET_RISK_FEATURES = 'GET_RISK_FEATURES';
const GET_ANALYSIS_DATA = 'GET_ANALYSIS_DATA';
const ZOOM_IN_OUT = 'ZOOM_IN_OUT';
const INIT_RISK_APP = 'INIT_RISK_APP';

function initState({href, gc, ac}) {
    return {
        type: INIT_RISK_APP,
        href,
        gc,
        ac
    };

}

function toggleDim() {
    return {
        type: TOGGLE_DIM
    };
}
function getData(url, cleanState = false) {
    return {
        type: GET_DATA,
        url,
        cleanState
    };
}
function dataLoading() {
    return {
        type: DATA_LOADING
    };
}
function dataLoaded(data, cleanState) {
    return {
        type: DATA_LOADED,
        data,
        cleanState
    };
}
function dataError(error) {
    return {
        type: DATA_ERROR,
        error
    };
}
function getAnalysisData(url) {
    return {
        type: GET_ANALYSIS_DATA,
        url
    };
}
function analysisDataLoaded(data) {
    return {
        type: ANALYSIS_DATA_LOADED,
        data
    };
}
function featuresError(error) {
    return {
        type: FEATURES_ERROR,
        error
    };
}
function featuresLoading() {
    return {
        type: FEATURES_LOADING
    };
}
function featuresLoaded(data) {
    return {
        type: FEATURES_LOADED,
        data
    };
}
function getFeatures(url) {
    return {
        type: 'GET_RISK_FEATURES',
        url
    };
}

function zoomInOut(dataHref, geomHref) {
    return {
        type: ZOOM_IN_OUT,
        dataHref,
        geomHref
    };
}
function loadMapConfig(configName, mapId, featuresUrl) {
    return {
        type: 'LOAD_RISK_MAP_CONFIG',
        configName,
        mapId,
        featuresUrl
    };
}
function setDimIdx(dim, idx) {
    return {
        type: SET_DIM_IDX,
        dim,
        idx
    };
}
function toggleAdminUnit() {
    return {
        type: TOGGLE_ADMIN_UNITS
    };
}
module.exports = {
    DATA_LOADING,
    DATA_LOADED,
    DATA_ERROR,
    ANALYSIS_DATA_LOADED,
    TOGGLE_DIM,
    SET_DIM_IDX,
    TOGGLE_ADMIN_UNITS,
    GET_DATA,
    LOAD_RISK_MAP_CONFIG,
    GET_RISK_FEATURES,
    GET_ANALYSIS_DATA,
    ZOOM_IN_OUT,
    INIT_RISK_APP,
    featuresLoaded,
    featuresLoading,
    featuresError,
    dataError,
    dataLoaded,
    dataLoading,
    getData,
    getFeatures,
    getAnalysisData,
    analysisDataLoaded,
    toggleDim,
    zoomInOut,
    loadMapConfig,
    setDimIdx,
    toggleAdminUnit,
    initState
};
