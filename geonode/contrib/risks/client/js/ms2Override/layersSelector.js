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
    loading: state.disaster && state.disaster.loading
});
// TODO currently loading flag causes a re-creation of the selector on any pan
// to avoid this separate loading from the layer object


function getLayerName(disaster) {
    const {data} = disaster.riskAnalysis.riskAnalysisData;
    const dimVal = data.dimensions[disaster.dim.dim2].values[0];
    return data.dimensions[disaster.dim.dim2].layers[dimVal];
}

function getViewParam(disaster) {
    // d1 always Scenario, d2 always Round period
    return {"viewparams": disaster.riskAnalysis.wms.viewparams.replace('d1:{};d2:{}', `d1:SSP1;d2:10`)};
}

const layerSelectorWithMarkers = createSelector(
    [layersSelector, markerSelector, geoColderSelector, disasterSelector],
    (layers = [], markerPosition, geocoderPosition, disaster) => {
        let newLayers;
        if (disaster.riskAnalysis && !disaster.loading && layers.length > 0) {

            const wms = {
            "type": "wms",
            "url": disaster.riskAnalysis.wms.geonode + "wms",
            "name": getLayerName(disaster),
            "title": "disasterrisk",
            "visibility": true,
            "format": "image/png",
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

const groupsSelector = (state) => state.layers && state.layers.flat && state.layers.groups && LayersUtils.denormalizeGroups(state.layers.flat, state.layers.groups).groups || [];

module.exports = {
    layersSelector,
    layerSelectorWithMarkers,
    groupsSelector
};
