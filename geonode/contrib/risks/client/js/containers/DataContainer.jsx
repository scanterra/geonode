/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const React = require('react');
const {connect} = require('react-redux');
const {dataContainerSelector} = require('../selectors/disaster');

const {getAnalysisData, getData, setDimIdx} = require('../actions/disaster');
const Chart = require('../components/Chart');
const Overview = connect(({disaster = {}}) => ({riskItems: disaster.overview || [] }) )(require('../components/Overview'));
const {Panel} = require('react-bootstrap');

const DataContainer = React.createClass({
    propTypes: {
        getData: React.PropTypes.func,
        getAnalysis: React.PropTypes.func,
        setDimIdx: React.PropTypes.func,
        showHazard: React.PropTypes.bool,
        className: React.PropTypes.string,
        hazardTitle: React.PropTypes.string,
        analysisType: React.PropTypes.object,
        riskAnalysisData: React.PropTypes.object,
        dim: React.PropTypes.object,
        hazardType: React.PropTypes.shape({
            mnemonic: React.PropTypes.string,
            description: React.PropTypes.string,
            analysisTypes: React.PropTypes.arrayOf(React.PropTypes.shape({
                name: React.PropTypes.string,
                title: React.PropTypes.string,
                href: React.PropTypes.string
                }))
        })
    },
    getDefaultProps() {
        return {
            showHazard: false,
            getData: () => {},
            getAnalysis: () => {},
            className: "col-sm-7"
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
    getChartData(data, val) {
        const {dim} = this.props;
        const nameIdx = dim === 0 ? 1 : 0;
        return data.filter((d) => d[nameIdx] === val ).map((v) => {return {"name": v[dim], "value": parseInt(v[2], 10)}; });
    },
    renderAnalysisData() {
        const {dim, setDimIdx: sIdx} = this.props;
        const {hazardSet, data} = this.props.riskAnalysisData;
        return (<div className="container-fluid">
            <h4>{hazardSet.title}</h4><br/>
                <p>{hazardSet.purpose}</p>
                <br/>
                <ul>
                    {data.dimensions[dim.dim1].values.map((val, idx) => {
                        return idx === dim.dim1Idx ? (
                            <li key={val} style={{marginBottom: 30}}>
                                <span>{`${data.dimensions[dim.dim1].name} ${val}`}</span>
                                <Chart dimension={data.dimensions} values={data.values} val={val} dim={dim} setDimIdx={sIdx}/>
                            </li>) : (
                            <li key={val} style={{marginBottom: 20}}>
                                <span style={{color: 'blue', cursor: 'pointer'}} onClick={() => sIdx('dim1Idx', idx)}>{`${data.dimensions[dim.dim1].name} ${val}`}</span>
                            </li>);
                    })}
                    </ul>
                    </div>);
    },
    renderRiskAnalysisHeader(title, getAnalysis, rs) {
        return (
          <div className="row">
            <div className="col-xs-10">
              <div className="disaster-analysis-title" onClick={()=> getAnalysis(rs.href)}>{title}</div>
            </div>
            <div className="col-xs-2">
                <i className="pull-right fa fa-chevron-down"></i>
            </div>
          </div>
        );
    },
    renderRiskAnalysis() {
        const {analysisType = {}, getAnalysis} = this.props;
        return analysisType.riskAnalysis.map((rs, idx) => {
            const {title, fa_icon: faIcon, abstract} = rs.hazardSet;
            return (
              <div className="row">
                  <div className="col-xs-1 text-center">
                      <i className={'disaster-category fa ' + faIcon} onClick={()=> getAnalysis(rs.href)}></i>
                  </div>
                  <div className="col-xs-11">
                    <Panel key={idx} collapsible header={this.renderRiskAnalysisHeader(title, getAnalysis, rs)}>
                        {abstract}
                    </Panel>
                  </div>
              </div>
            );
        });
    },
    renderAnalysisTab() {
        const {hazardType = {}, analysisType = {}, getData: loadData} = this.props;
        return (hazardType.analysisTypes || []).map((type) => {
            const {href, name, title} = type;
            const active = name === analysisType.name;
            return (<li key={name} className={`text-center ${active ? 'active' : ''}`} onClick={() => loadData(href, true)}>
                    <a href="#" data-toggle="tab"><span>{title}</span></a>
                    </li>);
        });
    },
    renderHazard() {
        const {hazardTitle, riskAnalysisData} = this.props;
        return (<div className={this.props.className}>
                <div className="disaster-header">
                  <div className="disaster-header-title"><i className={`icon-${this.props.hazardType.mnemonic.toLowerCase()}`}/>&nbsp;{hazardTitle}</div>
                  <ul className="nav nav-tabs">
                    {this.renderAnalysisTab()}
                  </ul>
                  <br/>
                </div>
                    {riskAnalysisData.name ? this.renderAnalysisData() : (<div className="disaster-analysis">
                        <div className="container-fluid">
                        {this.renderRiskAnalysis()}
                    </div></div>)}
            </div>);
    },
    render() {
        const {showHazard, getData: loadData} = this.props;
        return showHazard ? this.renderHazard() : (<Overview className={this.props.className} getData={loadData}/>);
    }
});

module.exports = connect(dataContainerSelector, {getAnalysis: getAnalysisData, getData, setDimIdx})(DataContainer);
