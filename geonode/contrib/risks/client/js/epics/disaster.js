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
const {setupTutorial} = require('../../MapStore2/web/client/actions/tutorial');
const {info, error} = require('react-notification-system-redux');
const bbox = require('turf-bbox');
const {changeLayerProperties, addLayer, removeNode} = require('../../MapStore2/web/client/actions/layers');
const assign = require('object-assign');
const {find} = require('lodash');
const {configLayer} = require('../utils/DisasterUtils');
const {defaultStep, tutorialPresets} = require('../utils/TutorialPresets');
const {
    GET_DATA,
    LOAD_RISK_MAP_CONFIG,
    GET_RISK_FEATURES,
    GET_ANALYSIS_DATA,
    INIT_RISK_APP,
    DATA_LOADED,
    ANALYSIS_DATA_LOADED,
    DATA_ERROR,
    dataLoaded,
    dataLoading,
    dataError,
    featuresLoaded,
    featuresLoading,
    featuresError,
    getFeatures,
    getAnalysisData,
    analysisDataLoaded,
    getData
} = require('../actions/disaster');
const {configureMap, configureError} = require('../../MapStore2/web/client/actions/config');
const getRiskDataEpic = (action$, store) =>
    action$.ofType(GET_DATA).switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1).
        map((data) => {
            const layers = (store.getState()).layers;
            const hasGis = find(layers.groups, g => g.id === 'Gis Overlays');
            const hasRiskAn = find(layers.flat, l => l.id === '_riskAn_');
            return [ hasGis && removeNode("Gis Overlays", "groups"), hasRiskAn && removeNode("_riskAn_", "layers"), dataLoaded(data, action.cleanState)].filter(a => a);
        })
        .mergeAll()
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
const getRiskFeatures = (action$, store) =>
    action$.ofType(GET_RISK_FEATURES)
    .audit(() => {
        const isMapConfigured = (store.getState()).mapInitialConfig && true;
        return isMapConfigured && Rx.Observable.of(isMapConfigured) || action$.ofType('MAP_CONFIG_LOADED');
    })
    .switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
        .retry(1)
        .map(val => [zoomToExtent(bbox(val.features[0]), "EPSG:4326"),
                changeLayerProperties("adminunits", {features: val.features.map((f, idx) => (assign({}, f, {id: idx}))) || []}),
                featuresLoaded(val.features)])
        .mergeAll()
        .startWith(featuresLoading())
        .catch(e => Rx.Observable.of(featuresError(e)))
    );
const getAnalysisEpic = (action$, store) =>
    action$.ofType(GET_ANALYSIS_DATA).switchMap(action =>
        Rx.Observable.defer(() => Api.getData(action.url))
            .retry(1)
            .map(val => {
                const baseUrl = val.wms && val.wms.baseurl;
                const anLayers = val.riskAnalysisData && val.riskAnalysisData.additionalLayers || [];
                const layers = (store.getState()).layers;
                const hasGis = find(layers.groups, g => g.id === 'Gis Overlays');
                const hasRiskAn = find(layers.flat, l => l.id === '_riskAn_');
                const actions = [analysisDataLoaded(val), hasGis && removeNode("Gis Overlays", "groups"), !hasRiskAn && addLayer(configLayer(baseUrl, "", "_riskAn_", "Risks Analysis", true, "Default"), false)].concat(anLayers.map((l) => addLayer(configLayer(baseUrl, l[1], `ral_${l[0]}`, l[1].split(':').pop(), false, 'Gis Overlays')))).filter(a => a);
                return actions;
            })
            .mergeAll()
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
                .catch( () => Rx.Observable.of(info({title: "Info", message: "Analysis not available at requested zoom level", position: 'tc', autoDismiss: 3})));
        });
const initStateEpic = action$ =>
    action$.ofType(INIT_RISK_APP) // Wait untile map config is loaded
        .audit( () => action$.ofType('MAP_CONFIG_LOADED'))
        .map(action => {
            const geomHref = action.href.replace('risk_data_extraction', 'geom');
            const analysisHref = action.ac && `${action.href}${action.ac}`;
            return [getData(`${action.href}${action.gc || ''}`), getFeatures(geomHref)].concat(analysisHref && getAnalysisData(analysisHref) || [] );
        }).
        mergeAll();
const changeTutorial = action$ =>
    action$.ofType(DATA_LOADED, ANALYSIS_DATA_LOADED).audit( () => action$.ofType('TOGGLE_CONTROL')).switchMap( action => {
        return Rx.Observable.of(action).flatMap((actn) => {
            let type = actn.data && actn.data.analysisType ? actn.type + '_R' : actn.type;
            return [setupTutorial(tutorialPresets[type], {}, '', defaultStep)];
        });
    });
const loadingError = action$ =>
    action$.ofType(DATA_ERROR).map(
        action => error({title: "Loading error", message: action.error.message,
            autoDismiss: 3}));

module.exports = {getRiskDataEpic, getRiskMapConfig, getRiskFeatures, getAnalysisEpic, zoomInOutEpic, initStateEpic, changeTutorial, loadingError};
