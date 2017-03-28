/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const Rx = require('rxjs');
const Api = require('../api/riskdata');
const {zoomToExtent} = require('../../MapStore2/web/client/actions/map');
const bbox = require('turf-bbox');
const {changeLayerProperties} = require('../../MapStore2/web/client/actions/layers');
const assign = require('object-assign');
const {
    GET_DATA,
    LOAD_RISK_MAP_CONFIG,
    GET_RISK_FEATURES,
    GET_ANALYSIS_DATA,
    dataLoaded,
    dataLoading,
    dataError,
    featuresLoaded,
    featuresLoading,
    featuresError,
    getFeatures,
    getAnalysisData,
    analysisDataLoaded
} = require('../actions/disaster');
const {configureMap, configureError} = require('../../MapStore2/web/client/actions/config');
const getRiskDataEpic = action$ =>
    action$.ofType(GET_DATA).switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url).then((data) => {
            return dataLoaded(data, action.cleanState);
        })).retry(1)
        .startWith(dataLoading(true))
        .catch(e => Rx.Observable.of(dataError(e)))
    );
const getRiskMapConfig = action$ =>
    action$.ofType(LOAD_RISK_MAP_CONFIG).switchMap(action =>
            Rx.Observable.fromPromise(Api.getData(action.configName))
                .map(val => [configureMap(val), getFeatures(action.featuresUrl)])
                .mergeAll()
                .catch(e => Rx.Observable.of(configureError(e)))
        );
const getRiskFeatures = action$ =>
    action$.ofType(GET_RISK_FEATURES).switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
            .retry(1)
            .map(val => [zoomToExtent(bbox(val.features[0]), "EPSG:4326"),
                changeLayerProperties("adminunits", {features: val.features.map((f, idx) => (assign({}, f, {id: idx}))) || []}),
                featuresLoaded(val.features)])
            .mergeAll()
            .startWith(featuresLoading())
            .catch(e => Rx.Observable.of(featuresError(e)))
    );
const getAnalysisEpic = action$ =>
    action$.ofType(GET_ANALYSIS_DATA).switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
            .retry(1)
            .map(val => analysisDataLoaded(val))
            .startWith(dataLoading(true))
            .catch(e => Rx.Observable.of(dataError(e)))
    );
const zoomInOutEpic = (action$, store) =>
        action$.ofType("ZOOM_IN_OUT").switchMap( action => {
            const {riskAnalysis, context} = (store.getState()).disaster;
            const analysisHref = riskAnalysis && `${action.dataHref}${riskAnalysis.context}`;
            return Rx.Observable.defer(() => Api.getData(`${action.dataHref}${context || ''}`))
                .retry(1).
                map(data => [dataLoaded(data), getFeatures(action.geomHref)].concat(analysisHref && getAnalysisData(analysisHref) || []))
                .mergeAll()
                .startWith(dataLoading(true))
                .catch(e => Rx.Observable.of(dataError(e)));
        });

module.exports = {getRiskDataEpic, getRiskMapConfig, getRiskFeatures, getAnalysisEpic, zoomInOutEpic};
