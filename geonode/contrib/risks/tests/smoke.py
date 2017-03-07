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

from django.core.management import call_command

from geonode.layers.models import Layer, Style
from geonode.contrib.risks.models import RiskAnalysis, HazardType
from geonode.contrib.risks.models import AnalysisType, DymensionInfo
from geonode.contrib.risks.models import RiskAnalysisDymensionInfoAssociation
from geonode.contrib.risks.tests import RisksTestCase

TESTDATA_FILE_INI = os.path.join(
    os.path.dirname(__file__),
    'resources/impact_analysis_results_test.ini')

TESTDATA_FILE_DATA = os.path.join(
    os.path.dirname(__file__),
    'resources/impact_analysis_results_test.xlsx')



class RisksSmokeTests(RisksTestCase):
    """
    To run the tests

      python manage.py test geonode.contrib.risks.tests.smoke

    """
    def test_smoke_createanalysis(self):
        """Test model here"""
        self.assertTrue(os.path.isfile(TESTDATA_FILE_INI))

        try:
            hazard = HazardType.objects.get(mnemonic="EQ")
            self.assertIsNotNone(hazard)

            analysis = AnalysisType.objects.get(name="impact")
            self.assertIsNotNone(analysis)

            layer = Layer.objects.get(name="test")
            self.assertIsNotNone(layer)
        except:
            traceback.print_exc()
            self.assertTrue(False)

        out = StringIO.StringIO()
        call_command('createriskanalysis',
                     descriptor_file=TESTDATA_FILE_INI, stdout=out)
        value = out.getvalue()
        try:
            risk = RiskAnalysis.objects.get(name=str(value).strip())
            self.assertIsNotNone(risk)

            dim1 = DymensionInfo.objects.get(name="Scenario")
            self.assertIsNotNone(dim1)

            dim2 = DymensionInfo.objects.get(name="Round Period")
            self.assertIsNotNone(dim2)

            rd1 = RiskAnalysisDymensionInfoAssociation.objects.filter(dymensioninfo=dim1, riskanalysis=risk)
            self.assertIsNotNone(rd1)
            self.assertEqual(len(rd1), 2)
            self.assertEqual(rd1[0].order, 0)
            self.assertEqual(rd1[0].axis, u'x')
            self.assertEqual(rd1[0].value, u'Hospital')
            self.assertEqual(rd1[1].order, 1)
            self.assertEqual(rd1[1].axis, u'x')
            self.assertEqual(rd1[1].value, u'SSP1')

            rd2 = RiskAnalysisDymensionInfoAssociation.objects.filter(dymensioninfo=dim2, riskanalysis=risk)
            self.assertIsNotNone(rd2)
            self.assertEqual(len(rd2), 2)
            self.assertEqual(rd2[0].order, 0)
            self.assertEqual(rd2[0].axis, u'y')
            self.assertEqual(rd2[0].value, u'10')
            self.assertEqual(rd2[1].order, 1)
            self.assertEqual(rd2[1].axis, u'y')
            self.assertEqual(rd2[1].value, u'20')
        except:
            traceback.print_exc()
            self.assertTrue(False)
