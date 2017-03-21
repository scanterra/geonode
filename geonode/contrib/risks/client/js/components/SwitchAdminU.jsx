/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const SwitchAdminU = React.createClass({
    propTypes: {
           toggleAdminUnit: React.PropTypes.func,
           showSubUnit: React.PropTypes.bool,
           show: React.PropTypes.bool
        },
        getDefaultProps() {
           return {
               toggleDim: () => {}
           };
       },
        render() {
            const {toggleAdminUnit, showSubUnit, show} = this.props;
            const lalbel = showSubUnit ? "Hide Sub-units values" : "Show Sub-units values";
            return show ? (<button className="btn btn-default" onClick={toggleAdminUnit}>{lalbel}
               </button>) : null;
        }
});

module.exports = SwitchAdminU;
