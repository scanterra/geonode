/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const {connect} = require('react-redux');
const {getData, zoomInOut} = require('../actions/disaster');
const {topBarSelector} = require('../selectors/disaster');
const TopBar = connect(topBarSelector, {zoom: zoomInOut, getData})(require('../components/TopBar'));
const DataContainer = require('../containers/DataContainer');
const MapContainer = require('../containers/MapContainer');

const Home = React.createClass({
    propTypes: {
        params: React.PropTypes.object,
        locale: React.PropTypes.string,
        messages: React.PropTypes.object,
        plugins: React.PropTypes.object
    },
    componentWillMount() {
        console.log(this.props.params.splat);
    },
    componentWillReceiveProps(nextProps) {
        console.log(nextProps.params.splat !== this.props.params.splat);
    },
    render() {
        const {plugins} = this.props;
        return (
               <div className="disaster">
                    <TopBar/>
                    <div className="container-fluid">
                        <div className="row">
                            <DataContainer/>
                            {<MapContainer plugins={plugins}/>}
                        </div>
                    </div>
                </div>
        );
    }
});

module.exports = connect((state) => {
    return {
        error: state.loadingError || (state.locale && state.locale.localeError) || null,
        locale: state.locale && state.locale.current,
        messages: state.locale && state.locale.messages || {}
    };
})(Home);
