/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');
const NotificationSystem = require('react-notification-system');
const NotificationStyle = require('../../assets/js/NotificationStyle');

const DownloadData = React.createClass({
    propTypes: {
        riskAnalysisData: React.PropTypes.object
    },
    getDefaultProps() {
        return {
            riskAnalysisData: {}
        };
    },
    componentDidMount() {
        this._notificationSystem = this.refs.notificationSystem;
    },
    render() {
        return (
          <div className="pull-left">
              <button className="btn btn-primary" style={{borderRadius: 0}} onClick={this._addNotification}>
                  <i className="fa fa-download"/>
              </button>
              <NotificationSystem ref="notificationSystem" style={NotificationStyle}/>
          </div>
        );
    },
    _addNotification(event) {
        event.preventDefault();
        const {dataFile, metadataFile} = this.props.riskAnalysisData;
        const downloadFile = dataFile || metadataFile ? (
            <div>
                <h4 className="text-center"><i className="fa fa-download"/>&nbsp;{'Download'}</h4>
                <ul className="nav nav-pills nav-stacked">
                    <li className="text-center"><a data-toggle="tab" href={dataFile} download>{'Data'}</a></li>
                    <li className="text-center"><a data-toggle="tab" href={metadataFile} download>{'Metadata'}</a></li>
                </ul>
            </div>
        ) : ( <h4 className="text-center">{'No files available'}</h4>);
        this._notificationSystem.addNotification({
            level: 'info',
            autoDismiss: 0,
            position: 'bc',
            children: downloadFile
        });
    }
});

module.exports = DownloadData;
