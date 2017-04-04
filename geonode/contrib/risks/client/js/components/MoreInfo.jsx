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
const {isObject} = require('lodash');

const MoreInfo = React.createClass({
    propTypes: {
        hazardSet: React.PropTypes.object,
        moreInfoOpen: React.PropTypes.func,
        download: React.PropTypes.bool,
        moreInfo: React.PropTypes.bool
    },
    getDefaultProps() {
        return {
            hazardSet: {},
            moreInfoOpen: () => {},
            download: false,
            moreInfo: false
        };
    },
    componentDidMount() {
        this._notificationSystem = this.refs.notificationSystem;
    },
    getDataAttributes(data) {
        const attributes = Object.keys(data);
        attributes.sort();
        return attributes.map((item, idx) => {
            let obj = data[item];
            return obj !== "" && obj !== null ? (
              <div key={idx}>
                  <div className="disaster-more-info-even">{item}</div>
                  {isObject(obj) ? (<div className="disaster-more-info-table-nested">{this.getDataAttributes(obj)}</div>) : (<div className="disaster-more-info-odd">{obj}</div>)}
              </div>
          ) : null;
        });
    },
    render() {
        const active = this.props.moreInfo ? ' active' : '';
        return (
            <div className="pull-left">
                <button className={"btn btn-primary" + active} style={{borderBottomLeftRadius: 0, borderTopLeftRadius: 0}} onClick={!this.props.moreInfo && !this.props.download ? this._addNotification : this._notificationSystem.clearNotifications}>
                    <i className="fa fa-ellipsis-h"/>
                </button>
                <NotificationSystem ref="notificationSystem" style={NotificationStyle}/>
            </div>
        );
    },
    _addNotification(event) {
        event.preventDefault();
        const downloadFile = (
            <div className="disaster-more-info-table-notification">
                <h4 className="text-center"><i className="fa fa-ellipsis-h"/>&nbsp;{'More info'}</h4>
                <div className="disaster-more-info-table-container">
                    <div className="disaster-more-info-table">
                        {this.getDataAttributes(this.props.hazardSet)}
                    </div>
                </div>
            </div>
        );
        this._notificationSystem.addNotification({
            level: 'info',
            autoDismiss: 0,
            position: 'bc',
            children: downloadFile,
            onAdd: this.props.moreInfoOpen.bind(null, true),
            onRemove: this.props.moreInfoOpen.bind(null, false)
        });
    }
});

module.exports = MoreInfo;
