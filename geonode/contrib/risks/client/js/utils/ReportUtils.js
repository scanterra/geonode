/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const {Promise} = require('es6-promise');
const canvg = require('canvg-browser');
function chartToImg(svg) {
    return new Promise(function(resolve) {
        let svgOffsetX;
        let svgOffsetY;
        let svgH;
        let svgW;
        const svgCanv = document.createElement('canvas');
        const svgString = svg.outerHTML;
        [svgOffsetX = 0, svgOffsetY = 0, svgW =0, svgH = 0] = svg.getAttribute('viewBox').split(' ');
        svg.setAttribute("style", "");
        svgOffsetX = svgOffsetX ? svgOffsetX : 0;
        svgOffsetY = svgOffsetY ? svgOffsetY : 0;
        svgCanv.setAttribute("width", svgW);
        svgCanv.setAttribute("height", svgH);
        // svgCanv.getContext('2d').scale(2, 2);
        canvg(svgCanv, svgString, {
            ignoreMouse: true,
            ignoreAnimation: true,
            ignoreDimensions: true,
            ignoreClear: true,
            offsetX: svgOffsetX,
            offsetY: svgOffsetY,
            renderCallback: () => resolve(svgCanv.toDataURL("image/png"))
            }
        );
    });
}
module.exports = {chartToImg};
