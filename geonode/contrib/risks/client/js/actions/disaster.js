/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const axios = require('../../MapStore2/web/client/libs/ajax');
const assign = require('object-assign');
const {head} = require('lodash');
const bbox = require('turf-bbox');
const {changeLayerProperties} = require('../../MapStore2/web/client/actions/layers');
const {configureMap, configureError} = require('../../MapStore2/web/client/actions/config');
const {zoomToExtent} = require('../../MapStore2/web/client/actions/map');
const DATA_LOADING = 'DATA_LOADING';
const DATA_LOADED = 'DATA_LOADED';
const DATA_ERROR = 'DATA_ERROR';
const ANALYSIS_DATA_LOADED = 'ANALYSIS_DATA_LOADED';
const TOGGLE_DIM = 'TOGGLE_DIM';
const SET_DIM_IDX = 'SET_DIM_IDX';
const FEATURES_LOADING = 'FEATURES_LOADING';
const FEATURES_LOADED = 'FEATURES_LOADED';
const FEATURES_ERROR = 'FEATURES_ERROR';
const TOGGLE_ADMIN_UNITS = 'TOGGLE_ADMIN_UNITS';

function toggleDim() {
    return {
        type: TOGGLE_DIM
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
function analysisDataLoaded(data) {
    return {
        type: ANALYSIS_DATA_LOADED,
        data
    };
}
function dataError(error) {
    return {
        type: DATA_ERROR,
        error
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
    return (dispatch) => {
        dispatch(featuresLoading());
        return axios.get(url).then((response) => {
            let state = response.data;
            if (typeof state !== "object") {
                try {
                    state = JSON.parse(state);
                } catch(e) {
                    dispatch(featuresError(e.message));
                }
            }
            dispatch(changeLayerProperties("adminunits", {features: state.features.map((f, idx) => (assign({}, f, {id: idx}))) || []}));
            const newExtent = bbox(state.features[0]);
            dispatch(zoomToExtent(newExtent, "EPSG:4326"));
            dispatch(featuresLoaded(state));
        }).catch((e) => {
            dispatch(featuresError(e));
        });
    };
}
function getData(url, cleanState = false) {
    return (dispatch) => {
        dispatch(dataLoading());
        return axios.get(url).then((response) => {
            let state = response.data;
            dispatch(dataLoaded(state, cleanState));
        }).catch((e) => {
            dispatch(dataError(e));
            return e;
        });
    };
}
function getAnalysisData(url) {
    return (dispatch) => {
        dispatch(dataLoading());
        return axios.get(url).then((response) => {
            let state = response.data;
            if (typeof state !== "object") {
                try {
                    state = JSON.parse(state);
                } catch(e) {
                    dispatch(dataError(e.message));
                }
            }
            dispatch(analysisDataLoaded(state));
        }).catch((e) => {
            dispatch(dataError(e));
        });
    };
}
function zoom(dataHref, geomHref) {
    return (dispatch, getState) => {
        const {riskAnalysis, context} = (getState()).disaster;
        getData(dataHref)(dispatch).then((e) => {
            if (!e) {
                if (riskAnalysis) {
                    const analContext = riskAnalysis.context.replace(context, '');
                    getAnalysisData(`${dataHref}${analContext}`)(dispatch);
                }
                getFeatures(geomHref)(dispatch);
            }
        });
    };
}
function zoomTo({layerId, fId} = {}) {
    return (dispatch, getState) => {
        const {flat: layers} = (getState()).layers;
        let {context} = (getState()).disaster;
        context = context === null ? '' : context;
        const layer = head(layers.filter((l) => l.id === layerId));
        const feature = head(layer.features.filter((f) => f.id === fId));
        if (feature) {
            zoom(`${feature.properties.href}${context}`, feature.properties.geom)(dispatch, getState);
        }
    };
}
function loadMapConfig(configName, mapId, featuresUrl) {
    return (dispatch) => {
        return axios.get(configName).then((response) => {
            if (typeof response.data === 'object') {
                dispatch(configureMap(response.data, mapId));
                getFeatures(featuresUrl)(dispatch);
            } else {
                try {
                    JSON.parse(response.data);
                } catch(e) {
                    dispatch(configureError('Configuration file broken (' + configName + '): ' + e.message));
                }
            }
        }).catch((e) => {
            dispatch(configureError(e));
        });
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
    dataError,
    dataLoaded,
    dataLoading,
    getData,
    getFeatures,
    getAnalysisData,
    toggleDim,
    zoomTo,
    zoom,
    loadMapConfig,
    setDimIdx,
    toggleAdminUnit
};
