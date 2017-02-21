#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.views.generic import TemplateView


cost_benefit_index = TemplateView.as_view(template_name='risks/cost_benefit_index.html')
risk_data_extraction_index = TemplateView.as_view(template_name='risks/risk_data_extraction_index.html')


