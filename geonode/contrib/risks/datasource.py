#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
import json
import urllib

from owslib.wfs import WebFeatureService


class GeoserverDataSource(object):
    """
    Wrapper around WFS to get deserialized features for risk management app
    """
    LAYER_TEMPLATE = 'geonode:risk_analysis'
    OUTPUT_FORMATS = {'application/json': json.load}
    WFCLASS = staticmethod(WebFeatureService)

    def __init__(self, url, output_format='application/json', **kwargs):

        self.wfs = GeoserverDataSource.WFCLASS(url=url, version='2.0.0', **kwargs)

        self.output_format = output_format

    def get_layer_name(self):
        return self.LAYER_TEMPLATE

    def prepare_vparams(self, vparams):
        u = urllib.quote
        return [':'.join((u(k), u(v),)) for k, v in vparams.iteritems()]

    def get_features(self, dim_name, **kwargs):
        """
        Return deserialized featurelist for given params
        @param dim_name dim value for query (layer) name
        @param kwargs keyword args used in viewparams
        """
        lname = self.get_layer_name()
        kwargs['dim'] = dim_name
        vparams_list = self.prepare_vparams(kwargs)
        vparams = {'viewparams': ';'.join(vparams_list)}
        field_names = ['dim1', 'dim2', 'value']
        r = self.wfs.getfeature(lname, propertyname=field_names, outputFormat=self.output_format, storedQueryParams=vparams, storedQueryID=1)
        return self.deserialize(r)

    def deserialize(self, val):
        d = self.OUTPUT_FORMATS[self.output_format]
        return d(val)
