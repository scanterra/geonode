/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {BarChart, Bar, XAxis, Cell, YAxis, Tooltip, CartesianGrid} = require('recharts');
const ChartTooltip = require("./ChartTooltip");
const chromaJs = require("chroma-js");

const Chart = React.createClass({
    propTypes: {
        values: React.PropTypes.array,
        dimension: React.PropTypes.array,
        dim: React.PropTypes.object,
        val: React.PropTypes.string,
        setDimIdx: React.PropTypes.func
    },
    getDefaultProps() {
        return {
        };
    },
    getChartData() {
        const {dim, values, val} = this.props;
        return values.filter((d) => d[dim.dim1] === val ).map((v) => {return {"name": v[dim.dim2], "value": parseInt(v[2], 10)}; });
    },
    render() {
        const {dim, dimension} = this.props;
        const chartData = this.getChartData();
        const colors = chromaJs.scale('OrRd').colors(chartData.length);
        return (
            <BarChart width={500} height={200} data={chartData}
                margin={{top: 20, right: 30, left: 30, bottom: 5}}>
                <XAxis dataKey="name"/>
                <Tooltip content={<ChartTooltip xAxisLabel={dimension[dim.dim2].name} xAxisUnit={dimension[dim.dim2].unit}/>}/>
                <YAxis label="Values" interval="preserveStart"/>
                <CartesianGrid strokeDasharray="3 3" />
                <Bar dataKey="value" onClick={this.handleClick}>
                    {chartData.map((entry, index) => {
                        const active = index === dim.dim2Idx;
                        return (
                            <Cell cursor="pointer" stroke={"black"} strokeWidth={active ? 1 : 0}fill={colors[index]} key={`cell-${index}`}/>);
                    })
                    }
                </Bar>
            </BarChart>);
    },
    handleClick(data, index) {
        this.props.setDimIdx('dim2Idx', index);
    }
});

module.exports = Chart;

