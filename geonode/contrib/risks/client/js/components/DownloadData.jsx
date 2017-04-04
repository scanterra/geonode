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
        riskAnalysisData: React.PropTypes.object,
        downloadOpen: React.PropTypes.func,
        download: React.PropTypes.bool,
        moreInfo: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            riskAnalysisData: {},
            downloadOpen: () => {},
            download: false,
            moreInfo: false
        };
    },
    componentDidMount() {
        this._notificationSystem = this.refs.notificationSystem;
    },
    render() {
        const active = this.props.download ? ' active' : '';
        return (
          <div className="pull-left">
              <button className={"btn btn-primary" + active} style={{borderRadius: 0}} onClick={!this.props.moreInfo && !this.props.download ? this._addNotification : this._notificationSystem.clearNotifications}>
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
                    <li className="text-center"><a href={`${dataFile}`} download>{'Data'}</a></li>
                    <li className="text-center"><a href={`${metadataFile}`} download>{'Metadata'}</a></li>
                </ul>
            </div>
        ) : ( <h4 className="text-center">{'No files available'}</h4>);
        this._notificationSystem.addNotification({
            level: 'info',
            autoDismiss: 0,
            position: 'bc',
            children: downloadFile,
            onAdd: this.props.downloadOpen.bind(null, true),
            onRemove: this.props.downloadOpen.bind(null, false)
        });
    }
});

module.exports = DownloadData;
