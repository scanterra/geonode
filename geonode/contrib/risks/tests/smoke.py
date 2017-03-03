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

from django.test import TestCase
from geonode.layers.models import Layer
from geonode.contrib.risks.models import RiskAnalysis, HazardType
from geonode.contrib.risks.models import AnalysisType, DymensionInfo
from geonode.contrib.risks.models import RiskAnalysisDymensionInfoAssociation

TESTDATA_FILE_INI = os.path.join(
    os.path.dirname(__file__),
    'resources/WP6__Impact_analysis_results_future_projections_Hospital.ini')


class RisksSmokeTests(TestCase):
    """
    To run the tests

      python manage.py test geonode.contrib.risks

    """

    def setUp(self):
        os.path.isfile(TESTDATA_FILE_INI)

    def test_todo(self):
        """Test model here"""
