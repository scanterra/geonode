/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {Tooltip, OverlayTrigger} = require('react-bootstrap');

const IdentifyBtn = React.createClass({
    propTypes: {
        label: React.PropTypes.string,
        toggleTOC: React.PropTypes.func,
        enabled: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            label: "Query objects on map",
            toggleTOC: () => {},
            enabled: false
        };
    },
    render() {
        const {label, enabled} = this.props;
        const tooltip = (<Tooltip id={"tooltip-sub-value"} className="disaster">{label}</Tooltip>);
        const active = enabled ? ' active' : '';
        return (
          <OverlayTrigger placement="bottom" overlay={tooltip}>
            <button id="disaster-identify-button" className={"btn btn-primary" + active + " drc"} onClick={this.props.toggleTOC}><i className="glyphicon glyphicon-map-marker"/></button>
          </OverlayTrigger>);
    }
});

module.exports = IdentifyBtn;
