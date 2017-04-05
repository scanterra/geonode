/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const Rx = require('rxjs');
const {chartToImg} = require('../utils/ReportUtils');
const API = require('../api/riskdata');
const {info, error, hide} = require('react-notification-system-redux');
const {
    GENERATE_REPORT,
    REPORT_MAP_READY,
    GENERATE_REPORT_ERROR,
    generateMapReport,
    generateReportError,
    reportReady
} = require('../actions/report');

const genReport = action$ =>
    action$
        .ofType(GENERATE_REPORT)
        .switchMap( () => {
            return Rx.Observable.of(generateMapReport())
            .startWith(info({title: "Info", message: "Grabbing map snapshot wait", position: 'tc', autoDismiss: 5, uid: 'grabmapnote'}));
        });
const uploadData = action$ =>
    action$.ofType(REPORT_MAP_READY).switchMap((action) => {
        return Rx.Observable.fromPromise(chartToImg(document.querySelector('.recharts-surface').cloneNode(true)))
        .map(val => {
            const legendUrl = (document.querySelector('#disaster-map-legend>img') || {}).src;
            return Rx.Observable.fromPromise(API.getReport("upload.php", action.dataUrl, val, legendUrl));
        }).map( () => {
            return reportReady();
        }).startWith(hide('grabmapnote')).catch((e) => generateReportError(e));
    });
const repError = action$ =>
    action$.ofType(GENERATE_REPORT_ERROR)
        .map(act => error({title: "Report error", message: act.error.message,
            autoDismiss: 3}));
module.exports = {genReport, uploadData, repError};
