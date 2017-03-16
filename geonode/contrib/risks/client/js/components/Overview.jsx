/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');

const Overview = React.createClass({
    propTypes: {
        riskItems: React.PropTypes.arrayOf(React.PropTypes.shape({
            title: React.PropTypes.string.isRequired,
            mnemonic: React.PropTypes.string.isRequired,
            herf: React.PropTypes.string,
            riskAnalysis: React.PropTypes.number
        })),
        className: React.PropTypes.string,
        getData: React.PropTypes.func
    },
    getDefaultProps() {
        return {
            className: "col-sm-7",
            getData: () => {}
        };
    },
    getItems() {
        const {riskItems, getData} = this.props;
        return riskItems.map((item, idx) => {
            const {title, href, riskAnalysis} = item;
            const noData = !(riskAnalysis > 0);
            return (
            <div key={idx} className={`${noData ? 'level-no-data' : ''} overview`} onClick={noData ? undefined : () => getData(href, true)}>
                <h2 className="page-header">
                    {title}
                    <small>
                        <span className="level">{riskAnalysis ? riskAnalysis : 'no data available'}</span>
                    </small>
                   </h2>
            </div>);
        });
    },
    render() {
        return (
            <div style={{minHeight: 500}} className={this.props.className}>
                <aside className="hazard-level">Analysis</aside>
                {this.getItems()}
            </div>);
    }
});

module.exports = Overview;
