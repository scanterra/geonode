/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {BarChart, Bar, XAxis, Cell, Tooltip} = require('recharts');

const Chart = React.createClass({
    propTypes: {
        values: React.PropTypes.array,
        dimension: React.PropTypes.array,
        dim: React.PropTypes.object,
        val: React.PropTypes.string
    },
    getDefaultProps() {
        return {
        };
    },
    getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    },
    getChartData() {
        const {dim, values, val} = this.props;
        return values.filter((d) => d[dim.dim1] === val ).map((v) => {return {"name": v[dim.dim2], "value": parseInt(v[2], 10)}; });
    },

    render() {
        const chartData = this.getChartData();
        return (
            <BarChart width={500} height={200} data={chartData}
                margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                <XAxis dataKey="name"/>
                <Tooltip/>
                <Bar dataKey="value">
                    {chartData.map((entry, index) => {
                        return (
                            <Cell cursor="pointer" fill={this.getRandomColor()} key={`cell-${index}`}/>);
                    })
                    }
                </Bar>
            </BarChart>);
    }
});

module.exports = Chart;

