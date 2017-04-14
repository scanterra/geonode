/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const Rx = require('rxjs');
const {chartToImg, legendToImg} = require('../utils/ReportUtils');
const API = require('../api/riskdata');
const {head} = require('lodash');
const {info, error, hide} = require('react-notification-system-redux');
const {shareUrlSelector, dimSelector} = require('../selectors/disaster');
const {
    GENERATE_REPORT,
    REPORT_MAP_READY,
    GENERATE_REPORT_ERROR,
    GENERATE_MAP_ERROR,
    generateMapReport,
    generateReportError,
    reportReady
} = require('../actions/report');

const genReport = action$ =>
    action$
        .ofType(GENERATE_REPORT)
        .switchMap( () => {
            return Rx.Observable.of(generateMapReport())
            .startWith(info({title: "Info", message: "Wait map-report in progress", position: 'tc', autoDismiss: 0, uid: 'grabmapnote'}));
        });
const uploadData = (action$, store) =>
    action$.ofType(REPORT_MAP_READY).switchMap((action) => {
        return Rx.Observable.from([chartToImg(document.querySelectorAll('.recharts-surface')), legendToImg(document.querySelector('#disaster-map-legend>img'))]).combineAll()
        .switchMap( val => {
            const state = store.getState();
            const chartsObj = head(val.filter( o => o.name === 'charts'));
            const legendObj = head(val.filter( o => o.name === 'legend'));
            const url = state.disaster.riskAnalysis.pdfReport;
            const permalink = shareUrlSelector(state) || {};
            const dim = dimSelector(state);
            return Rx.Observable.from(API.getReport(url, permalink.shareUrl || '', dim, action.dataUrl, chartsObj.data, legendObj.data));
        }).map(() => {
            return reportReady();
        }).catch((e) => Rx.Observable.of(generateReportError(e))).startWith(hide('grabmapnote'));
    });
const mapError = action$ =>
        action$.ofType(GENERATE_MAP_ERROR)
            .switchMap( act =>
                Rx.Observable.of(error({title: "Grab Map error", message: act.e.message,
                        autoDismiss: 3}))
            .startWith(hide('grabmapnote')
            ));
const repError = action$ =>
    action$.ofType(GENERATE_REPORT_ERROR)
        .map(act => error({title: "Report error", message: act.e.message,
            autoDismiss: 3}));
module.exports = {genReport, uploadData, repError, mapError};
