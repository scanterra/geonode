/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */


const tutorialPresets = {
    DATA_LOADED: [{
            title: 'Disaster Risk Selector',
            text: '...text',
            selector: '#disaster-risk-selector-menu'
        },
        {
            title: 'Overview List',
            text: '...text',
            selector: '#disaster-overview-list'
        },
        {
            title: 'Map',
            text: '...text',
            selector: '#disaster-map-main-container'
        },
        {
            title: 'Navigation',
            text: '...text',
            selector: '#disaster-navigation'
        },
        {
            title: 'Tools',
            text: '...text',
            selector: '#disaster-page-tools'
        },
        {
            title: 'Download PDF',
            text: '...text',
            selector: '#disaster-download-pdf'
        },
        {
            title: 'Share',
            text: '...text',
            selector: '#disaster-share-link'
        },
        {
            title: 'Tutorial',
            text: '...text',
            selector: '#disaster-show-tutorial'
        }
    ],
    DATA_LOADED_R: [{
            title: 'Analysis Menu',
            text: '...text',
            selector: '#disaster-analysis-menu'
        },
        {
            title: 'Analysis List',
            text: '...text',
            selector: '#disaster-analysis-container'
        }
    ],
    ANALYSIS_DATA_LOADED: [{
            title: 'Analysis Data',
            text: '...text',
            selector: '#disaster-analysis-data-container'
        },
        {
            title: 'Charts',
            text: '...text',
            selector: '#disaster-chart-container'
        },
        {
            title: 'Map Tools',
            text: '...text',
            selector: '#disaster-map-tools'
        },
        {
            title: 'Map Slider',
            text: '...text',
            selector: '#disaster-map-slider'
        },
        {
            title: 'Map Legend',
            text: '...text',
            selector: '#disaster-map-legend'
        },
        {
            title: 'Further Resources',
            text: '...text',
            selector: '#disaster-further-resources'
        },
        {
            title: 'Layers Menu',
            text: '...text',
            selector: '#navigationBar-container'
        },
        {
            title: 'Back to Analysis',
            text: '...text',
            selector: '#disaster-back-button'
        }
    ]
};

const defaultStep = {
    title: '',
    text: '',
    position: 'bottom',
    type: 'click',
    allowClicksThruHole: true
};

module.exports = {
    defaultStep,
    tutorialPresets
};
