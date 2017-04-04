/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
const assign = require('object-assign');
const {
    DATA_LOADING,
    DATA_LOADED,
    DATA_ERROR,
    TOGGLE_DIM,
    ANALYSIS_DATA_LOADED,
    SET_DIM_IDX,
    TOGGLE_ADMIN_UNITS
} = require('../actions/disaster');

function disaster(state = {dim: {dim1: 0, dim2: 1, dim1Idx: 0, dim2Idx: 0}}, action) {
    switch (action.type) {
        case DATA_LOADING:
            return assign({}, state, {
                loading: true
            });
        case DATA_LOADED: {
            return action.cleanState ? assign({}, { loading: false, error: null}, action.data) : assign({}, { loading: false, error: null, dim: state.dim, riskAnalysis: state.riskAnalysis}, action.data);
        }
        case ANALYSIS_DATA_LOADED: {
            return assign({}, state, { loading: false, error: null, riskAnalysis: action.data});
        }
        case TOGGLE_DIM: {
            const newDim = state.dim && {dim1: state.dim.dim2, dim2: state.dim.dim1, dim1Idx: 0, dim2Idx: 0} || {dim1: 1, dim2: 0, dim1Idx: 0, dim2Idx: 0};
            return assign({}, state, {dim: newDim});
        }
        case TOGGLE_ADMIN_UNITS: {
            return assign({}, state, {showSubUnit: !state.showSubUnit});
        }
        case SET_DIM_IDX: {
            const newDim = assign({dim1: 0, dim2: 1, dim1Idx: 0, dim2Idx: 0}, state.dim, {[action.dim]: action.idx});
            return assign({}, state, {dim: newDim});
        }
        case DATA_ERROR:
            return assign({}, state, {
                error: action.error,
                loading: false
            });
        default:
            return state;
    }
}

module.exports = disaster;
