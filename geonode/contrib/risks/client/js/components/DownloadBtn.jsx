/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

const React = require('react');

const DownloadBtn = React.createClass({
    propTypes: {
        downloadAction: React.PropTypes.func,
        downloading: React.PropTypes.bool,
        label: React.PropTypes.string
    },
    getDefaultProps() {
        return {
            downloading: false,
            label: "Download Pdf"
        };
    },
    render() {
        const {label, downloading, downloadAction} = this.props;
        return (
            <button disabled={!downloadAction} className="btn btn-default" onClick={downloadAction}>
                  {downloading ? (<i className="icon-spinner fa-spin"/>) : (<i className="icon-download-arrow"/>)}&nbsp;
                  {label}
            </button>);
    }
});

module.exports = DownloadBtn;
