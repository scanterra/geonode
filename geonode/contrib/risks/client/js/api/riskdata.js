/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const axios = require('../../MapStore2/web/client/libs/ajax');
const ConfigUtils = require('../../MapStore2/web/client/utils/ConfigUtils');
const riskdataCache = {};
const toBlob = require('canvas-to-blob');
const Api = {
    getData: function(url) {
        const cached = riskdataCache[url];
        if (cached && new Date().getTime() < cached.timestamp + (ConfigUtils.getConfigProp('cacheDataExpire') || 60) * 1000) {
            return new Promise((resolve) => {
                resolve(cached.data);
            });
        }
        return axios.get(url).then((response) => {
            riskdataCache[url] = {
                timestamp: new Date().getTime(),
                data: response.data
            };
            return response.data;
        });
    },
    getReport: function(url, mapImg, chartImg, legend) {
        const mapBlob = toBlob(mapImg);
        const chartBlob = toBlob(chartImg);
        let data = new FormData();
        data.append('map.png', mapBlob);
        data.append('chart.png', chartBlob);
        data.append('legendURL', legend);
        return axios.post(url, data);
    }
};

module.exports = Api;
