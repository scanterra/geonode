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
const {isArray, isObject} = require('lodash');

const MoreInfo = React.createClass({
    propTypes: {
        hazardSet: React.PropTypes.object
    },
    getDefaultProps() {
        return {
            hazardSet: {}
        };
    },
    componentDidMount() {
        this._notificationSystem = this.refs.notificationSystem;
    },
    render() {
        return (
            <div className="pull-left">
                <button className="btn btn-primary" style={{borderBottomLeftRadius: 0, borderTopLeftRadius: 0}} onClick={this._addNotification}>
                    <i className="fa fa-ellipsis-h"/>
                </button>
                <NotificationSystem ref="notificationSystem" style={NotificationStyle}/>
            </div>
        );
    },
    getDataAttributes(data) {
        const attributes = Object.keys(data);
        attributes.sort();
        return attributes.map((item, idx) => {
            let obj = data[item];
            return obj !== "" && obj !== null ? (
              <tbody key={idx}>
                  <tr>
                      <td>{item}</td>
                  </tr>
                  <tr>
                      {isObject(obj) ? (<table className="table table-striped" style={{width: 240, margin: '15px 0 15px 15px'}}>{this.getDataAttributes(obj)}</table>) : (<td>{obj}</td>)}
                  </tr>
              </tbody>
          ) : null;
        });
    },
    _addNotification(event) {
        event.preventDefault();
        const downloadFile = (
            <div style={{overflow: 'hidden'}}>
                <h4 className="text-center"><i className="fa fa-ellipsis-h"/>&nbsp;{'More info'}</h4>
                <div style={{overflowY: 'scroll', maxHeight: 400}}>
                    <table className="table table-striped" style={{width: 255}}>
                        {this.getDataAttributes(this.props.hazardSet)}
                    </table>
                </div>
            </div>
        );
        this._notificationSystem.addNotification({
            level: 'info',
            autoDismiss: 0,
            position: 'bc',
            children: downloadFile
        });
    }
});

module.exports = MoreInfo;
