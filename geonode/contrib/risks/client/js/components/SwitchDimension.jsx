/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const SwitchDim = React.createClass({
    propTypes: {
        toggleDim: React.PropTypes.func,
        dimName: React.PropTypes.string
    },
    getDefaultProps() {
        return {
            toggleDim: () => {}
        };
    },
    render() {
        return this.props.dimName ? (
            <div className="switch-dim" onClick={this.props.toggleDim}>{`Switch to ${this.props.dimName}`}
            </div>) : null;
    }
});

module.exports = SwitchDim;
