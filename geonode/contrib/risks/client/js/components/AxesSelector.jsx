/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const AxesSelector = React.createClass({
    propTypes: {
        dimension: React.PropTypes.object.isRequired,
        activeAxis: React.PropTypes.number,
        setDimIdx: React.PropTypes.func
    },
    getDefaultProps() {
        return {
            activeAxis: 0,
            setDimIdx: () => {}
        };
    },
    getAxes() {
        const {values = []} = this.props.dimension || {};
        return values.map((val, idx) => {
            return idx === this.props.activeAxis ? (
                <li key={idx}className="map-axis active text-center">{val}</li>) : (<li key={idx} className="map-axis text-center" onClick={() => this.props.setDimIdx('dim2Idx', idx)}>{val}</li>);
        });
    },
    render() {
        return this.props.dimension ? (<ul className="map-axes horizontal list-unstyled">
            {this.getAxes()}
            </ul>) : null;
    }
});

module.exports = AxesSelector;
