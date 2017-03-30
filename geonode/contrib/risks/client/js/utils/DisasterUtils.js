/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

function configLayer(baseurl, layerName, layerId, layerTitle, visibility = true, group) {
    return {
    "id": layerId,
    "type": "wms",
    "url": baseurl + "wms",
    "name": layerName,
    "title": layerTitle,
    "visibility": visibility,
    "format": "image/png",
    "tiled": true,
    "group": group
    };
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


module.exports = {configLayer, getViewParam, getLayerName, getStyle};
