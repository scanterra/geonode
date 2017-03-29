/**
* Copyright 2017, GeoSolutions Sas.
* All rights reserved.
*
* This source code is licensed under the BSD-style license found in the
* LICENSE file in the root directory of this source tree.
*/

const {createSelector} = require('reselect');
const {head} = require('lodash');
const MapInfoUtils = require('../../MapStore2/web/client/utils/MapInfoUtils');
const LayersUtils = require('../../MapStore2/web/client/utils/LayersUtils');

const layersSelector = state => (state.layers && state.layers.flat) || (state.layers) || (state.config && state.config.layers);
const markerSelector = state => (state.mapInfo && state.mapInfo.showMarker && state.mapInfo.clickPoint);
const geoColderSelector = state => (state.search && state.search.markerPosition);
const disasterSelector = state => ({
    riskAnalysis: state.disaster && state.disaster.riskAnalysis,
    dim: state.disaster && state.disaster.dim || {dim1: 0, dim2: 1, dim1Idx: 0, dim2Idx: 0},
    showSubUnit: state.disaster.showSubUnit,
    loading: state.disaster && state.disaster.loading
});
// TODO currently loading flag causes a re-creation of the selector on any pan
// to avoid this separate loading from the layer object


function getLayerName({dim, riskAnalysis}) {
    const {dimensions} = riskAnalysis.riskAnalysisData.data;
    const dim1Val = dimensions[dim.dim1].values[dim.dim1Idx];
    return dimensions[dim.dim1].layers[dim1Val].layerName;
}
function getStyle({dim, riskAnalysis}) {
    const {dimensions} = riskAnalysis.riskAnalysisData.data;
    const dim1Val = dimensions[dim.dim1].values[dim.dim1Idx];
    return dimensions[dim.dim1].layers[dim1Val] && dimensions[dim.dim1].layers[dim1Val].layerStyle && dimensions[dim.dim1].layers[dim1Val].layerStyle.name;
}
function getViewParam({dim, showSubUnit, riskAnalysis} = {}) {
    const {dimensions} = riskAnalysis.riskAnalysisData.data;
    const {wms} = riskAnalysis;
    const dim1Val = dimensions[dim.dim1].values[dim.dim1Idx];
    const dim2Val = dimensions[dim.dim2].values[dim.dim2Idx];
    const dim1SearchDim = dimensions[dim.dim1].layers[dim1Val].layerAttribute;
    const dim2SearchDim = dimensions[dim.dim2].layers[dim2Val].layerAttribute;
    let viewparams = wms.viewparams.replace(`${dim1SearchDim}:{}`, `${dim1SearchDim}:${dim1Val}`).replace(`${dim2SearchDim}:{}`, `${dim2SearchDim}:${dim2Val}`);
    if (showSubUnit) {
        const admCode = viewparams.match(/(adm_code:)\w+/g)[0];
        const supCode = admCode.replace(/(adm_code:)/, "sub_adm_code:");
        const superCode = admCode.replace(/(adm_code:)/, "super_adm_code:");
        viewparams = viewparams.replace(admCode, `${supCode};${superCode}`);
    }
    return {viewparams};
}

const layerSelectorWithMarkers = createSelector(
    [layersSelector, markerSelector, geoColderSelector, disasterSelector],
    (layers = [], markerPosition, geocoderPosition, disaster) => {
        let newLayers;
        if (disaster.riskAnalysis && !disaster.loading && layers.length > 0) {

            const wms = {
            "id": "disasterrisk",
            "type": "wms",
            "url": disaster.riskAnalysis.wms.baseurl + "wms",
            "name": getLayerName(disaster),
            "title": "disasterrisk",
            "visibility": true,
            "format": "image/png",
            "style": getStyle(disaster),
            "tiled": true,
            "params": getViewParam(disaster)
            };
            newLayers = (layers.filter((l) => l.id !== "adminunits")).concat([wms, head(layers.filter((l) => l.id === "adminunits"))]);
        }else {
            newLayers = [...layers];
        }
        if ( markerPosition ) {
            newLayers.push(MapInfoUtils.getMarkerLayer("GetFeatureInfo", markerPosition.latlng));
        }
        if (geocoderPosition) {
            newLayers.push(MapInfoUtils.getMarkerLayer("GeoCoder", geocoderPosition, "marker",
                {
                    overrideOLStyle: true,
                    style: {
                        iconUrl: "https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    }
                }
            ));
        }

        return newLayers;
    }
);
const disasterRiskLayerSelector = createSelector([layerSelectorWithMarkers],
    (layers) => ({
        layer: head(layers.filter((l) => l.id === "disasterrisk"))
    }));
const groupsSelector = (state) => state.layers && state.layers.flat && state.layers.groups && LayersUtils.denormalizeGroups(state.layers.flat, state.layers.groups).groups || [];

module.exports = {
    layersSelector,
    layerSelectorWithMarkers,
    groupsSelector,
    disasterRiskLayerSelector
};
