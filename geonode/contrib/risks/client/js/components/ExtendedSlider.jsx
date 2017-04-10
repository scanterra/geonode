/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const {connect} = require('react-redux');
const {Brush, LineChart, XAxis, ResponsiveContainer} = require('recharts');
const Nouislider = require('react-nouislider');
const {show, hide} = require('react-notification-system-redux');
const {labelSelector} = require('../selectors/disaster');
const {getSFurtherResourceData} = require('../actions/disaster');
const LabelResource = connect(labelSelector, { show, hide, getData: getSFurtherResourceData })(require('../components/LabelResource'));
// const values = require('../../assets/mockUpData/dimNum');

const CustomizedXLabel = (props) => {
    const {x, y, payload} = props;
    let label = payload.value.split(" ")[0];
    label = label.length > 8 ? label.substring(0, 8) + '...' : label;
    return (
      <g transform={`translate(${x},${y})`}>
          <text x={0} y={0} dy={4} dx={-4} textAnchor="end" fill="#666" transform="rotate(-90)">{label}</text>
      </g>
    );
};

const ExtendedSlider = React.createClass({
    propTypes: {
        uid: React.PropTypes.string,
        dimension: React.PropTypes.object,
        activeAxis: React.PropTypes.number,
        maxLength: React.PropTypes.number,
        sliders: React.PropTypes.object,
        setDimIdx: React.PropTypes.func,
        chartSliderUpdate: React.PropTypes.func,
        dimIdx: React.PropTypes.string,
        color: React.PropTypes.string
    },
    getDefaultProps() {
        return {
            uid: '',
            activeAxis: 0,
            maxLength: 10,
            sliders: {},
            setDimIdx: () => {},
            chartSliderUpdate: () => {},
            dimIdx: 'dim2Idx',
            dimensions: [],
            color: '#5d9bd1'
        };
    },
    componentDidUpdate() {
        const startIndex = this.props.sliders[this.props.uid] ? this.props.sliders[this.props.uid].startIndex : 0;
        const endIndex = this.props.sliders[this.props.uid] ? this.props.sliders[this.props.uid].endIndex : this.props.maxLength - 1;
        if (startIndex === endIndex) {
            this.props.chartSliderUpdate({startIndex, endIndex: startIndex + 1}, this.props.uid);
        }
    },
    getBrushData(data) {
        return data.map((val, idx) => { return {value: idx, name: val}; });
    },
    renderBrushSlider(data) {
        const graphData = this.getBrushData(data);
        const startIndex = this.props.sliders[this.props.uid] ? this.props.sliders[this.props.uid].startIndex : 0;
        let endIndex = this.props.sliders[this.props.uid] ? this.props.sliders[this.props.uid].endIndex : this.props.maxLength - 1;
        endIndex = startIndex === endIndex ? startIndex + 1 : endIndex;
        return (
            <div>
                <Nouislider
                    range={{min: startIndex, max: endIndex}}
                    start={[this.props.activeAxis]}
                    step={1}
                    tooltips={false}
                    onChange={(idx) => this.props.setDimIdx(this.props.dimIdx, Number.parseInt(idx[0]))}
                    />
                  <ResponsiveContainer width="100%" height={110}>
                    <LineChart data={graphData}>
                        <Brush startIndex={startIndex} endIndex={endIndex} height={20} dataKey="name" data={graphData} stroke={this.props.color} fill={'rgba(255,255,255,0.6)'}
                          onChange={(index) => {
                              this.props.chartSliderUpdate(index, this.props.uid);
                              /* should placed in epicss
                              if (activeAxis < index.startIndex
                              || activeAxis > index.endIndex) {
                                  this.props.setDimIdx(this.props.dimIdx, Number.parseInt(index.startIndex));
                              }*/
                          }}
                        />
                        <XAxis height={70} minTickGap={0} tick={<CustomizedXLabel/>} dataKey="name" interval={0}/>
                    </LineChart>
                </ResponsiveContainer>
            </div>
        );
    },
    renderSlider(data) {
        const {maxLength} = this.props;
        const graphData = this.getBrushData(data);
        return data.length > maxLength ? this.renderBrushSlider(data) : (
            <div>
                <Nouislider
                    range={{min: 0, max: data.length - 1}}
                    start={[this.props.activeAxis]}
                    step={1}
                    tooltips={false}
                    onChange={(idx) => this.props.setDimIdx(this.props.dimIdx, Number.parseInt(idx[0]))}
                    />
                  <ResponsiveContainer width="100%" height={70}>
                    <LineChart data={graphData}>
                        <XAxis height={50} minTickGap={0} tick={<CustomizedXLabel/>} dataKey="name" interval={0}/>
                    </LineChart>
                </ResponsiveContainer>
            </div>
        );
    },
    render() {
        const {values = [], name} = this.props.dimension || {};
        const slider = !this.props.dimension || values.length - 1 === 0 ? null : this.renderSlider(values);
        const label = !this.props.dimension ? null : (<LabelResource uid={this.props.uid} label={name + ' ' + values[this.props.activeAxis]} dimension={this.props.dimension}/>);
        return (
            <div>
                {label}
                {slider}
            </div>
        );
    }
});

module.exports = ExtendedSlider;
