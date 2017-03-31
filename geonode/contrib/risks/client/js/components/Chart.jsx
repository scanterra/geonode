/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {BarChart, Bar, XAxis, Cell, YAxis, Tooltip, CartesianGrid, ResponsiveContainer} = require('recharts');
const ChartTooltip = require("./ChartTooltip");
const NumberFormat = require("../../MapStore2/web/client/components/I18N/Number");

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
        return values.filter((d) => d[dim.dim1] === val ).map((v) => {return {"name": v[dim.dim2], "value": parseFloat(v[2], 10)}; });
    },
    render() {
        const {dim, dimension} = this.props;
        const chartData = this.getChartData();
        /*const colors = chromaJs.scale('OrRd').colors(chartData.length);*/
        return (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart width={500} height={200} data={chartData}
                margin={{top: 20, right: 30, left: 30, bottom: 5}}>
                <XAxis dataKey="name" tickFormatter={this.formatXTiks}/>
                <Tooltip content={<ChartTooltip xAxisLabel={dimension[dim.dim2].name} xAxisUnit={dimension[dim.dim2].unit}/>}/>
                <YAxis label="Values" interval="preserveStart" tickFormatter={this.formatYTiks}/>
                <CartesianGrid strokeDasharray="3 3" />
                <Bar dataKey="value" onClick={this.handleClick}>
                    {chartData.map((entry, index) => {
                        const active = index === dim.dim2Idx;
                        return (
                            <Cell cursor="pointer" stroke={"#ff8f31"} strokeWidth={active ? 2 : 0}fill={active ? '#2c689c' : '#ff8f31'} key={`cell-${index}`}/>);
                    })
                    }
                </Bar>
            </BarChart></ResponsiveContainer>);
    },
    handleClick(data, index) {
        this.props.setDimIdx('dim2Idx', index);
    },
    formatYTiks(v) {
        return v.toLocaleString();
    },
    formatXTiks(v) {
        return !isNaN(v) && parseFloat(v).toLocaleString() || v;
    }
});

module.exports = Chart;
