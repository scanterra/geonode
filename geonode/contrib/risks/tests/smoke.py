# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import os
import traceback
import StringIO

from django.test import TestCase
from django.core.management import call_command

from geonode.layers.models import Layer, Style
from geonode.contrib.risks.models import RiskAnalysis, HazardType
from geonode.contrib.risks.models import AnalysisType, DymensionInfo
from geonode.contrib.risks.models import RiskAnalysisDymensionInfoAssociation

TESTDATA_FILE_INI = os.path.join(
    os.path.dirname(__file__),
    'resources/impact_analysis_results_test.ini')


class RisksSmokeTests(TestCase):
    """
    To run the tests

      python manage.py test geonode.contrib.risks.tests.smoke

    """
    fixtures = [
        'sample_admin',
        'default_oauth_apps',
        'initial_data',
        '001_risks_adm_divisions',
        '002_risks_hazards',
        '003_risks_analysis',
        '004_risks_dymension_infos',
        '005_risks_test_base',
        '005_risks_test_layer'
    ]

    def test_smoke_createanalysis(self):
        """Test model here"""
        self.assertTrue(os.path.isfile(TESTDATA_FILE_INI))
        out = StringIO.StringIO()
        call_command('createriskanalysis',
                     descriptor_file=TESTDATA_FILE_INI, stdout=out)
        value = out.getvalue()
        try:
            risk = RiskAnalysis.objects.get(name=str(value).strip())
            self.assertIsNotNone(risk)
        except:
            traceback.print_exc()
            self.assertTrue(False)
