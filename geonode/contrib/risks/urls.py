#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from geonode.contrib.risks import views
from geonode.contrib.risks import geometry_views
from geonode.contrib.risks.models import RiskApp

KWARGS_DATA_EXTRACTION = {'app': RiskApp.APP_DATA_EXTRACTION}
KWARGS_COST_BENEFIT_ANALYSIS = {'app': RiskApp.APP_COST_BENEFIT}



geometry_urls = [
    url(r'loc/(?P<adm_code>[\w\-]+)/$', geometry_views.administrative_division_view, name='location'),
]
api_urls = [
    url(r'risk/(?P<risk_id>[\d]+)/layers/$', views.risk_layers, name='layers'),
]

urlpatterns = [
    url(r'^geom/', include(geometry_urls, namespace="geom")),
    url(r'^api/', include(api_urls, namespace='api')),
]

data_extraction_urls = ([
    url(r'^$', views.risk_data_extraction_index, name='index'),
    url(r'^geom/(?P<adm_code>[\w\-]+)/$', geometry_views.administrative_division_view, name='geometry'),
    url(r'loc/(?P<loc>[\w\-]+)/$', views.location_view, name='location'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/$', views.hazard_type_view, name='hazard_type'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-]+)/$', views.hazard_type_view, name='analysis_type'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-]+)/an/(?P<an>[\w\-]+)/$', views.data_extraction, name='analysis'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-]+)/an/(?P<an>[\w\-]+)/dym/(?P<dym>[\w\-]+)$', views.data_extraction, name='analysis_dym'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-]+)/an/(?P<an>[\w\-]+)/pdf/$', views.pdf_report, name='pdf_report'),
], RiskApp.APP_DATA_EXTRACTION, KWARGS_DATA_EXTRACTION)

cost_benefit_urls = ([
    url(r'^$', views.cost_benefit_index, name='index'),
    url(r'^geom/(?P<adm_code>[\w\-]+)/$', geometry_views.administrative_division_view, name='geometry'),
    url(r'loc/(?P<loc>[\w\-]+)/$', views.location_view, name='location'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/$', views.hazard_type_view, name='hazard_type'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-]+)/$', views.hazard_type_view, name='analysis_type'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-]+)/an/(?P<an>[\w\-]+)/$', views.data_extraction, name='data_extraction'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-]+)/an/(?P<an>[\w\-]+)/dym/(?P<dym>[\w\-]+)$', views.data_extraction, name='data_extraction_dym'),
    url(r'loc/(?P<loc>[\w\-]+)/ht/(?P<ht>[\w\-]+)/at/(?P<at>[\w\-_]+)/an/(?P<an>[\w\-]+)/pdf/$', views.pdf_report, name='pdf_report'),
], RiskApp.APP_COST_BENEFIT, KWARGS_COST_BENEFIT_ANALYSIS,)

for urls_list in (data_extraction_urls, cost_benefit_urls,):
    urllist, app_name, kwargs = urls_list
    for r in urllist:
        r.kwargs = kwargs
    new_urls = url(r'^{}/'.format(app_name), include(urllist, namespace=app_name))
    urlpatterns.append(new_urls)

