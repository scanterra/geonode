#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import json
from StringIO import StringIO
from django.test import Client
from django.core.urlresolvers import reverse
from geonode.utils import designals, resignals
from geonode.contrib.risks.models import DymensionInfo, RiskAnalysis, Layer
from geonode.contrib.risks.tests import RisksTestCase
from geonode.contrib.risks.tests.smoke import (TESTDATA_FILE_INI, TESTDATA_FILE_DATA,
                                               TEST_RISK_ANALYSIS, TEST_REGION, call_command)


class RisksViewTestCase(RisksTestCase):


    def test_risk_layers(self):
        """
        Check if layers are saved correctly along with risk analysis
        """
        out = StringIO()
        call_command('createriskanalysis', descriptor_file=TESTDATA_FILE_INI, stdout=out)
        call_command(
            'importriskdata',
            commit=True,
            excel_file=TESTDATA_FILE_DATA,
            region=TEST_REGION,
            risk_analysis=TEST_RISK_ANALYSIS,
            stdout=out)

        client = Client()

        url = '/risks/risk_data_extraction/loc/AF/'
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)

        risk_analysis = RiskAnalysis.objects.all().first()

        for ht in data['overview']:
            url = ht['href']
            resp = client.get(url)
            if ht['riskAnalysis'] > 0:
                risk_link = ht['href']
                resp = client.get(risk_link)
                data = json.loads(resp.content)
                for ra in data['analysisType']['riskAnalysis']:
                    risk_url = url = ra['href']
                    resp = client.get(url)
                    self.assertEqual(resp.status_code, 200,
                                     'wrong status on non-empty hazard type {}: {}'.format(url, resp.content))
                    
        layers_url = reverse('risks-api:layers', args=(risk_analysis.id,))
        l0 = client.get(layers_url)
        l0_data = json.loads(l0.content)
        self.assertEqual(l0.status_code, 200)
        self.assertEqual(l0_data.get('data').get('layers'), [])
        designals()
        _layers = []
        for lname in ['l1', 'l2', 'l3']:
            _layers.append(Layer.objects.create(name=lname))
        resignals()

        to_add = [str(_l.id) for _l in _layers[:2]]

        l1 = client.post(layers_url, {'layers': to_add})

        # check if additional layers match in db
        rq = risk_analysis.additional_layers.all()
        self.assertEqual(rq.count(), len(to_add))
        self.assertEqual([str(r.id) for r in rq], to_add)

        # .. and in response
        l1_data = json.loads(l1.content)
        self.assertEqual(l1.status_code, 200)
        self.assertEqual(len(l1_data.get('data').get('layers')), len(to_add))

        # update check
        to_add = [str(_l.id) for _l in _layers[2:]]

        l2 = client.post(layers_url, {'layers': to_add})
        self.assertEqual(l2.status_code, 200)
        self.assertTrue(len(to_add) == 1)

        l2_data = json.loads(l2.content)
        # check if additional layers match in db
        rq = risk_analysis.additional_layers.all()
        self.assertEqual(rq.count(), len(to_add))
        self.assertEqual([str(r.id) for r in rq], to_add)

        self.assertEqual(len(l2_data.get('data').get('layers')), len(to_add))

        resp = client.get(risk_url)
        self.assertEqual(resp.status_code, 200,
                         'wrong status on non-empty hazard type {}: {}'.format(url, resp.content))
        resp_data = json.loads(resp.content)
        self.assertEqual(len(resp_data['riskAnalysisData']['additionalLayers']), len(to_add))


    def test_data_views(self):
        """
        Check if data views returns proper data

        """
        out = StringIO()
        call_command('createriskanalysis', descriptor_file=TESTDATA_FILE_INI, stdout=out)
        call_command(
            'importriskdata',
            commit=True,
            excel_file=TESTDATA_FILE_DATA,
            region=TEST_REGION,
            risk_analysis=TEST_RISK_ANALYSIS,
            stdout=out)

        client = Client()
        url = '/risks/risk_data_extraction/loc/INVALID/'
        resp = client.get(url)
        self.assertEqual(resp.status_code, 404)
        data = json.loads(resp.content)
        self.assertFalse(data.get('navItems'))
        self.assertTrue(data.get('errors'))

        url = '/risks/risk_data_extraction/loc/AF/'
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue(data.get('navItems'))
        self.assertTrue(data.get('overview'))
        self.assertTrue(len(data['overview']) > 0)
        non_empty = []
        for ht in data['overview']:
            url = ht['href']
            resp = client.get(url)
            if ht['riskAnalysis'] > 0:
                non_empty.append(ht['href'])
                self.assertEqual(resp.status_code, 200,
                                 'wrong status on non-empty hazard type {}: {}'.format(url, resp.content))
                data = json.loads(resp.content)
                self.assertTrue(data.get('navItems'))
            else:
                self.assertEqual(resp.status_code, 404,
                                 'wrong status on empty hazard type {}: {}'.format(url, resp.content))
        self.assertTrue(len(non_empty) > 0, "There should be at least one RiskAnalysis available")

        # let's check non-empty hazard types, there should be some risk analysis here!
        for ne in non_empty:
            resp = client.get(ne)
            self.assertEqual(resp.status_code, 200,
                             'wrong status on non-empty hazard type {}: {}'.format(url, resp.content))
            data = json.loads(resp.content)
            self.assertTrue(data.get('analysisType'))
            self.assertTrue(data.get('hazardType'))
            self.assertTrue(data['hazardType'].get('analysisTypes'))
            self.assertTrue(data['analysisType'].get('riskAnalysis'))
            for ra in data['analysisType']['riskAnalysis']:
                url = ra['href']
                resp = client.get(url)
                self.assertEqual(resp.status_code, 200,
                                 'wrong status on non-empty hazard type {}: {}'.format(url, resp.content))
                data = json.loads(resp.content)
                self.assertTrue(data.get('riskAnalysisData'))
                self.assertTrue(data['riskAnalysisData'].get('data'))
                for d in data['riskAnalysisData']['data']['dimensions']:
                    self.assertEqual(DymensionInfo.objects.filter(name=d['name']).count(), 1)

                    # layerAttributes/layers should be in pair with values from 
                    # RiskAnalysisDymensionInfoAssociacion.value
                    la_keys = d['layerAttributes'].keys()
                    l_keys = d['layers'].keys()

                    self.assertTrue(len(d['values'])> 0)
                    self.assertTrue(isinstance(d['layerAttributes'], dict))
                    self.assertTrue(d['layerAttributes'])

                    self.assertTrue(isinstance(d['layers'], dict))
                    self.assertTrue(d['layers'])

                    self.assertTrue(la_keys == d['values'])
                    self.assertTrue(l_keys == d['values'])

                # cannot evaluate
                #self.assertTrue(len(data['riskAnalysisData']['data']['values'])>0)
