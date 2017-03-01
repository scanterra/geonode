#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from geonode.contrib.risks import views

urlpatterns = [
    url(r'cost_benefit/$', views.cost_benefit_index, name='risks_cost_benefit_index'),
    url(r'risk_data_extraction/$', views.risk_data_extraction_index, name='risks_risk_data_extraction_index'),
    url(r'risk_data_extraction/(?P<loc>[\w\-]+)/(?P<ht>[\w\-]+)/(?P<at>[\w\-]+)/$', views.risk_data_extraction_index, name='risks_risk_data_extraction'),
    url(r'risk_data_extraction/(?P<loc>[\w\-]+)/(?P<ht>[\w\-]+)/(?P<at>[\w\-]+)/(?P<dym>[\w\-]+)/$', views.risk_data_extraction_index, name='risks_risk_data_extraction_dym'),
    url(r'risk_data_extraction/(?P<loc>[\w\-]+)/(?P<ht>[\w\-]+)/(?P<at>[\w\-]+)/(?P<dym>[\w\-]+)/(?P<axis>[\w\-]+)/$', views.risk_data_extraction_index, name='risks_risk_data_extraction_dym_ax'),

]
