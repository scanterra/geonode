/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {Tooltip, OverlayTrigger} = require('react-bootstrap');

const LayerBtn = React.createClass({
    propTypes: {
        label: React.PropTypes.string,
        toggleTOC: React.PropTypes.func
    },
    getDefaultProps() {
        return {
            label: "Show layers",
            toggleTOC: () => {}
        };
    },
    render() {
        const {label} = this.props;
        const tooltip = (<Tooltip id={"tooltip-sub-value"} className="disaster">{label}</Tooltip>);
        return (
          <OverlayTrigger placement="bottom" overlay={tooltip}>
            <button id="disaster-layer-button" className="btn btn-primary drc" onClick={this.props.toggleTOC}><i className="glyphicon glyphicon-1-layer"/></button>
          </OverlayTrigger>);
    }
});

module.exports = LayerBtn;
