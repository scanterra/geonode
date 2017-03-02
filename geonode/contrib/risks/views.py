#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging

from django.conf import settings
from django.views.generic import TemplateView
from geonode.contrib.risks.models import (HazardType, AnalysisType,
                                          AdministrativeDivision, RiskAnalysis,
                                          DymensionInfo,
                                          RiskAnalysisDymensionInfoAssociation)

from geonode.contrib.risks.datasource import GeoserverDataSource

cost_benefit_index = TemplateView.as_view(template_name='risks/cost_benefit_index.html')

log = logging.getLogger(__name__)


class RiskDataExtractionView(TemplateView):

    template_name = 'risks/risk_data_extraction_index.html'
    DEFAULT_LOC = 'AF'
    NO_VALUE = '-'
    AXIS_X = 'x'
    AXIS_Y = 'y'
    DEFAULTS = {'loc': DEFAULT_LOC, 'ht': NO_VALUE, 'at': NO_VALUE, 'axis': AXIS_X}

    def get_location(self, loc=None):
        """
        Returns AdministrativeDivision object for loc code
        """
        if self._ommit_value(loc):
            loc = self.DEFAULT_LOC
        return AdministrativeDivision.objects.get(code=loc)

    def get_dyminfo(self, **kwargs):
        """

        """
        map_classes = {'an': (None, None, 'riskanalysis',),
                       'axis': (None, None, 'riskanalysis_associacion__axis',),
                       }
        filter_args = self._extract_args_from_request(map_classes, **kwargs)
        if not filter_args:
            return None

        return DymensionInfo.objects.filter(**filter_args).distinct().get()

    def get_dymensioninfo_list(self, **kwargs):
        """
        Returns DymensionInfo list for given params
        """
        map_classes = {'an': (None, None, 'riskanalysis',),
                       }
        filter_args = self._extract_args_from_request(map_classes, **kwargs)
        if not filter_args:
            return []

        return DymensionInfo.objects.filter(**filter_args).distinct()

    @classmethod
    def _extract_args_from_request(cls, required_map, optional_map=None, **kwargs):
        """
        Extract QuerySet.filter() arguments from provided kwargs from url.
        Method will use two dictionaries with mapping between url kwargs
        and fields for queryset. First dictionary is for required params,
        second is for optional.

        Mapping is in following format:

            url_kwarg: (ModelClass, get_lookup_field, filter_lookup,)

        or

            url_kwarg: (None, None, filter_lookup,)

        where:

        url_kwarg
            is kwarg from url. This should identify one entity from ModelClass

        ModelClass
            is class for model, which will be queried for one
            value only (with .get())

        get_lookup_field
            lookup field used in ModelClass.get(get_lookup_field=url_kwarg)

        filter_lookup
            target queryset field lookup used by caller

        if ModelClass is None, no instance lookup is performed, only
        filter_lookup: url_kwarg mapping is returned


        Returns dictionary with lookups to be used in QuerySet.filter():

        >>> kwargs = {'loc': 'A00'} # Afghanistan, from url like /risks/report/A00/.../
        >>> required = {'loc': (AdministrativeDivision, 'code', 'administrative_division',)}
        >>> self._extract_args_from_request(required, None, **kwargs) # we skip optional here
        {'administrative_division': <Afghanistan>}
        >>> RiskAnalysis.objects.filter(**_)

        """
        filter_params = {}
        if required_map:
            for k, v in kwargs.iteritems():
                if cls._ommit_value(v):
                    continue
                # model class, model class arg name for .get(), filtering kwarg for RiskAnalysis
                try:
                    klass, filter_field, filter_arg = required_map[k]
                except KeyError:
                    continue
                if klass is None:
                    filter_params[filter_arg] = v
                else:
                    filter_params[filter_arg] = klass.objects.get(**{filter_field: v})

            # do not return results if we don't have all required params
            if len(filter_params.keys()) != len(required_map.keys()):
                log.warning("Returning empty list of analysis. "
                            "Parsed params: %s are not covering all required keys",
                            filter_params)
                return {}

        if optional_map:
            for k, v in kwargs.iteritems():
                if cls._ommit_value(v):
                    continue
                try:
                    klass, filter_field, filter_arg = optional_map[k]
                except KeyError:
                    continue
                if klass is None:
                    filter_params[filter_arg] = v
                else:
                    filter_params[filter_arg] = klass.objects.get(**{filter_field: v})
        return filter_params

    def get_analysis(self, **kwargs):
        """
        Returns list of RiskAnalysis objects for given url args.
        """
        map_classes = {'loc': (AdministrativeDivision, 'code', 'administrative_divisions'),
                       'ht': (HazardType, 'mnemonic', 'hazard_type'),
                       'at': (AnalysisType, 'name', 'analysis_type'),
                       'an': (None, None, 'id'),
                       }

        filter_params = self._extract_args_from_request(map_classes, **kwargs)
        if not filter_params:
            return

        try:
            q = RiskAnalysis.objects.get(**filter_params)
        except Exception, err:
            pass
        return q
    
    def get_features(self, analysis, dyminfo, **kwargs):

        s = settings.OGC_SERVER['default']
        ass_list = RiskAnalysisDymensionInfoAssociation.objects.filter(riskanalysis=analysis, dymensioninfo=dyminfo)
        dim_list = set([a.axis_to_dim() for a in ass_list])
        if len(dim_list) != 1:
            raise ValueError("Cannot query more than one dimension at the moment, got {}".format(len(dim_list)))
        gs = GeoserverDataSource('{}/wfs'.format(s['LOCATION']),
                                 username=s['USER'], 
                                 password=s['PASSWORD'])

        return gs.get_features(list(dim_list)[0], **kwargs)

    def get_analysis_list(self, **kwargs):
        """
        Returns list of RiskAnalysis objects for given url args.
        
        """
        map_classes = {'loc': (AdministrativeDivision, 'code', 'administrative_divisions'),
                       'ht': (HazardType, 'mnemonic', 'hazard_type'),
                       'at': (AnalysisType, 'name', 'analysis_type'),
                       #'dym': (DymensionInfo, 'id', 'dymensioninfo',),
                       }

        filter_params = self._extract_args_from_request(map_classes, **kwargs)
        if not filter_params:
            return []

        q = RiskAnalysis.objects.filter(**filter_params)
        return q

    @classmethod
    def _ommit_value(cls, val):
        """
        Return True if provided val should be considered as no value
        """
        return not val or val == cls.NO_VALUE

    def get_context_data(self, *args, **kwargs):
        out = super(RiskDataExtractionView, self).get_context_data(*args, **kwargs)
        out['hazard_types'] = HazardType.objects.all()
        out['analysis_types'] = AnalysisType.objects.all()

        defaults = out['defaults'] = self.DEFAULTS

        # we skip empty values from url
        filtered_kwargs = dict([(k, v,) for k, v in kwargs.iteritems() if not self._ommit_value(v)])

        # and provide defaults
        current = defaults.copy()
        current.update(filtered_kwargs)
        out['current'] = current
        out['location'] = self.get_location(current.get('loc'))

        #out['dymensioninfo_types'] = self.get_dymensioninfo(**current)
        analysis = self.get_analysis(**current)
        analysis_list = out['risk_analysis_list'] = self.get_analysis_list(**current)
        if analysis:
            out['analysis'] = analysis
            out['dimensions'] = self.get_dymensioninfo_list(**current)
            out['dyminfo'] = dyminfo = self.get_dyminfo(**current)
            out['features'] = self.get_features(analysis, dyminfo, **current)

        return out


risk_data_extraction_index = RiskDataExtractionView.as_view()
