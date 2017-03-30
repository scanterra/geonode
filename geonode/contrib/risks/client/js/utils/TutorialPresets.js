/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */


const tutorialPresets = {
    DATA_LOADED: [{
            title: 'Welcome on Risk Data Extraction & Visualization',
            text: 'click on start to initialize the tutorial',
            selector: '#intro-tutorial'
        },
        {
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
const introStyle = {
    backgroundColor: 'transparent',
    color: '#fff',
    mainColor: '#fff',
    textAlign: 'center',
    header: {
        padding: 5,
        fontFamily: 'Georgia, serif',
        fontSize: '2.0em'
    },
    main: {
        fontSize: '1.0em',
        padding: 5
    },
    footer: {
        padding: 10
    },
    button: {
        color: '#fff',
        backgroundColor: '#2c689c'
    },
    close: {
        display: 'none'
    },
    skip: {
        color: '#fff'
    }
};

module.exports = {
    defaultStep,
    introStyle,
    tutorialPresets
};
