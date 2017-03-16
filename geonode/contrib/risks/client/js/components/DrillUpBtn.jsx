/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const DrillUpBtn = React.createClass({
    propTypes: {
        label: React.PropTypes.string,
        href: React.PropTypes.string,
        geom: React.PropTypes.string,
        context: React.PropTypes.string,
        zoomOut: React.PropTypes.func,
        disabled: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            zoomOut: () => {}
        };
    },
    render() {
        const {label, disabled} = this.props;
        return disabled ? null : (
            <button className="btn btn-xs btn-default drillup" onClick={this.onClick}>
                <i className="btn-xs icon-zoom-out"/>
                {`Zoom out to ${label}`}
            </button>);
    },
    onClick() {
        const {href, context, zoomOut, geom} = this.props;
        zoomOut(`${href}${context}`, geom);
    }
});

module.exports = DrillUpBtn;
