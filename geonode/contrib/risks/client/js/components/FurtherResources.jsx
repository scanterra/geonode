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
        analysisResourecs: React.PropTypes.array
    },
    getDefaultProps() {
        return {
        };
    },
    getResources() {
        const {analysisResourecs} = this.props;
        return analysisResourecs.map((res) => (
            <li>
                <a target="_blank" href={res.details}>
                    {res.text}
                </a>
            </li>)
        );
    },
    render() {
        const {analysisResourecs} = this.props;
        return analysisResourecs ? (
            <div className="disaster-fth-res-container">
                <h1>Further Resources</h1>
                <p>For further information the following resources could be consulted:
                </p>
                <ul>
                {this.getResources()}
                </ul>
            </div>) : null;
    }
});

module.exports = FurtherResources;
