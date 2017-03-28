/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const {connect} = require('react-redux');
const Navigation = require('./Navigation');
const DownloadBtn = require('./DownloadBtn');
const RiskSelector = require('./RiskSelector');
const {shareUrlSelector} = require('../selectors/disaster');
const SharingLink = connect(shareUrlSelector)(require('./ShareLink'));
const TopBar = React.createClass({
    propTypes: {
        navItems: React.PropTypes.array,
        riskItems: React.PropTypes.array,
        getData: React.PropTypes.func,
        zoom: React.PropTypes.func,
        activeRisk: React.PropTypes.string,
        overviewHref: React.PropTypes.string,
        title: React.PropTypes.string.isRequired,
        context: React.PropTypes.string
    },
    getDefaultProps() {
        return {
            navItems: [],
            riskItems: [],
            getData: () => {},
            title: ''
        };
    },
    render() {
        const {navItems, context, riskItems, overviewHref, activeRisk, getData, zoom} = this.props;
        return (
            <div className="container-fluid">
                <div className="disaster-breadcrumbs">
                    <Navigation items={navItems} zoom={zoom} context={context}/>
                    <div className="pull-right">
                    <SharingLink bsSize=""/>
                        <DownloadBtn/>
                        <button className="btn btn-primary"><i className="fa fa-question"/></button>
                    </div>
                </div>
                <div className="disaster-risk-selector">
                    <RiskSelector riskItems={riskItems} overviewHref={overviewHref} activeRisk={activeRisk} getData={getData}/>
                </div>
            </div>);
    }
});

module.exports = TopBar;
