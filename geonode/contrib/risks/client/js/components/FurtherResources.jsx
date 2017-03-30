/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const FurtherResources = React.createClass({
    propTypes: {
        analysisType: React.PropTypes.array,
        hazardType: React.PropTypes.array
    },
    getDefaultProps() {
        return {
        };
    },
    getResources(resources = []) {
        return resources.map((res, idx) => (
            <li key={idx}>
                <a target="_blank" href={res.details}>
                    {res.text}
                </a>
            </li>)
        );
    },
    render() {
        const {analysisType, hazardType} = this.props;
        const resources = [...analysisType, ...hazardType];
        return resources.length > 0 ? (
            <div id="disaster-further-resources" className="disaster-fth-res-container">
                <h1>Further Resources</h1>
                <p>For further information the following resources could be consulted:
                </p>
                <ul>
                {this.getResources(resources)}
                </ul>
            </div>) : null;
    }
});

module.exports = FurtherResources;
