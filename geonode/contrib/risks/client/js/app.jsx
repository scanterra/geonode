/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const ReactDOM = require('react-dom');
const {connect} = require('react-redux');
const assign = require('object-assign');
const appReducers = {
     disaster: require('./reducers/disaster')
 };
const {getData, initState} = require('./actions/disaster');
const epics = require('./epics/disaster');

const ConfigUtils = require('../MapStore2/web/client/utils/ConfigUtils');
ConfigUtils.setLocalConfigurationFile('/static/js/localConfig.json');
// Set one hour cache
ConfigUtils.setConfigProp("cacheDataExpire", 3600);
const StandardApp = require('../MapStore2/web/client/components/app/StandardApp');
const url = require('url');
const urlQuery = url.parse(window.location.href, true).query;
const init = urlQuery && urlQuery.init && JSON.parse(urlQuery.init);

const {pages, pluginsDef, initialState, storeOpts} = require('./appConfig');


const initDim = init && init.d || {};

const newInitState = assign({}, initialState, {defaultState: {disaster: {dim: initDim}}});

const StandardRouter = connect((state) => ({
    locale: state.locale || {},
    pages
}))(require('../MapStore2/web/client/components/app/StandardRouter'));

const appStore = require('../MapStore2/web/client/stores/StandardStore').bind(null, newInitState, appReducers, epics);

const initAction = init ? () => initState(init) : () => getData("/risks/risk_data_extraction/loc/AF/");
const appConfig = {
    storeOpts,
    appStore,
    pluginsDef,
    initialActions: [initAction],
    appComponent: StandardRouter
};

ReactDOM.render(
    <StandardApp {...appConfig}/>,
    document.getElementById('container')
);
