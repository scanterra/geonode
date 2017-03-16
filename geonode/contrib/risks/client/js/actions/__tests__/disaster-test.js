/**
 * Copyright 2017, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */
 /**
  * Copyright 2016, GeoSolutions Sas.
  * All rights reserved.
  *
  * This source code is licensed under the BSD-style license found in the
  * LICENSE file in the root directory of this source tree.
  */

const expect = require('expect');
const {
    DATA_LOADING,
    DATA_LOADED,
    DATA_ERROR,
    TOGGLE_DIM,
    dataError,
    dataLoaded,
    dataLoading,
    getData,
    toggleDim
} = require('../disaster');

describe('Test correctness of the disaster actions', () => {
    it('toggle dimension', () => {
        const action = toggleDim();
        expect(action.type).toBe(TOGGLE_DIM);
    });
    it('data loading', () => {
        const action = dataLoading();
        expect(action.type).toBe(DATA_LOADING);
    });
    it('data loaded', () => {
        const action = dataLoaded(true);
        expect(action.type).toBe(DATA_LOADED);
        expect(action.data).toBe(true);
    });
    it('data error', () => {
        const action = dataError({message: "MESSAGE"});
        expect(action.error).toExist();
        expect(action.error.message).toBe("MESSAGE");
        expect(action.type).toBe(DATA_ERROR);
    });
    it('get data', (done) => {
        getData('base/js/test-resources/mockupData.json')((e) => {
            if (e.type === DATA_LOADING) {
                try {
                    expect(e).toExist();
                    expect(e.type).toBe(DATA_LOADING);
                } catch(ex) {
                    done(ex);
                }
            } else if (e.type === DATA_LOADED) {
                try {
                    expect(e).toExist();
                    expect(e.type).toBe(DATA_LOADED);
                    expect(e.data).toExist();
                    done();
                } catch(ex) {
                    done(ex);
                }
            }
        });
    });
});
