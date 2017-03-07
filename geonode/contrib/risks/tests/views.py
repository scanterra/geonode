#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from django.test import Client
from geonode.contrib.risks.tests import RisksTestCase
from geonode.contrib.risks.views import LocationView


class RisksViewTestCase(RisksTestCase):

    def test_location_view(self):
        client = Client()
        url = '/risks/risk_data_extraction/loc/AF/'
        resp = client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertTrue('navItems' in data)
        
