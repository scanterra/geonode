/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const ChartTooltip = React.createClass({
    propTypes: {
        type: React.PropTypes.string,
        payload: React.PropTypes.array,
        label: React.PropTypes.string,
        active: React.PropTypes.bool,
        xAxisLabel: React.PropTypes.string,
        xAxisUnit: React.PropTypes.string,
        uOm: React.PropTypes.string
    },
    render() {
        const {active, payload, label, xAxisLabel, xAxisUnit, uOm} = this.props;
        const val = active && uOm.replace(/#/, payload[0].value.toLocaleString()) || '';
        return active ? (
            <div className="disaster-chart-tooltip">
                <p className="disaster-chart-tooltip-label">{`${xAxisLabel} : ${!isNaN(label) && parseFloat(label).toLocaleString() || label} ${xAxisUnit}`}</p>
                <p className="disaster-chart-tooltip-values">{val}</p>
            </div>) : null;
    }
});

module.exports = ChartTooltip;
