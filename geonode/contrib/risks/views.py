#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView


from geonode.contrib.risks.models import HazardType, AnalysisType, AdministrativeDivision, RiskAnalysis
cost_benefit_index = TemplateView.as_view(template_name='risks/cost_benefit_index.html')



#risk_data_extraction_index = TemplateView.as_view(template_name='risks/risk_data_extraction_index.html')


class RiskDataExtraction(TemplateView):

    template_name = 'risks/risk_data_extraction_index.html'
    DEFAULT_LOC = 'AF'
    NO_VALUE = '-'
    DEFAULTS = {'loc': DEFAULT_LOC, 'ht': NO_VALUE, 'at': NO_VALUE}

    def get_location(self, loc=None):
        if not loc or loc == self.NO_VALUE: 
            loc = self.DEFAULT_LOC
        return AdministrativeDivision.objects.get(code=loc)

    def get_analysis_list(self, **kwargs):
        """
        Returns list of RiskAnalysis objects for given url args.
        """
        map_classes = {'loc': (AdministrativeDivision, 'code', 'administrative_divisions'),
                       'ht': (HazardType, 'mnemonic', 'hazard_type'),
                       'at': (AnalysisType, 'name', 'analysis_type')}

        filter_params = {}
        for k, v in kwargs.iteritems():
            if not v or v == self.NO_VALUE:
                continue
            # model class, model class arg name for .get(), filtering kwarg for RiskAnalysis
            try:
                klass, filter_field, filter_arg = map_classes[k]
            except KeyError:
                continue
            filter_params[filter_arg] = klass.objects.get(**{filter_field: v})
        
        # do not return results if we don't have all required params
        if len(filter_params.keys()) != len(map_classes.keys()):
            return []
        return RiskAnalysis.objects.filter(**filter_params)

    def get_context_data(self, *args, **kwargs):
        out = super(RiskDataExtraction, self).get_context_data(*args, **kwargs)
        out['hazard_types'] = HazardType.objects.all()
        out['analysis_types'] = AnalysisType.objects.all()
        defaults = out['defaults'] = self.DEFAULTS
        filtered_kwargs = dict([(k,v,) for k,v in kwargs.iteritems() if v])

        current = defaults.copy()
        current.update(filtered_kwargs)
        out['current'] = current
        out['risk_analysis_list'] = self.get_analysis_list(**kwargs)
        out['location'] = self.get_location(kwargs.get('loc'))

        return out



risk_data_extraction_index = RiskDataExtraction.as_view()
