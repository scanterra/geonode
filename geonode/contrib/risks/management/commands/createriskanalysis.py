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
import time
import shutil
import requests
import simplejson as json

import traceback
import psycopg2

from requests.auth import HTTPBasicAuth
from optparse import make_option

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.gdal import DataSource
from django.contrib.gis import geos

from geonode.layers.models import Layer
from geonode.contrib.risks.models import RiskAnalysis, HazardType
from geonode.contrib.risks.models import AnalysisType, DymensionInfo
from geonode.contrib.risks.models import Region, AdministrativeDivision
from geonode.contrib.risks.models import RiskAnalysisDymensionInfoAssociation
from geonode.contrib.risks.models import RiskAnalysisAdministrativeDivisionAssociation

import ConfigParser

Config = ConfigParser.ConfigParser()


class Command(BaseCommand):
    """
    Allows to define a new Risk Analysis along with Dymentions descriptors.

    The command needs an 'ini' file defined as follows (this is only an example):

        [DEFAULT]
        # unique and less than 30 characters
        name = future_projections_Hospital

        # can be 'impact' or 'loss_impact'
        analysis_type = impact

        # must use mnemonics
        hazard_type = EQ

        # must exists on GeoNode and you have to use its native 'name' **not** the title
        layer = test

        [DIM1]
        # can be 'Scenario' or 'Round Period' for now
        dymensioninfo = Scenario

        # the first one must be always the baseline; the order is important
        values =
            Hospital
            SSP1
            SSP2
            SSP3
            SSP4
            SSP5

        # can be 'x', 'y', 'z', 't', 'e'; the order is important
        #  - layer 'x' always corresponds to the XLSX sheets
        #  - layer 'y' always corresponds to the XLSX columns
        axis = x

        # corresponding attribute name of the 'layer'
        layer_attribute = dim1

        [DIM2]
        # can be 'Scenario' or 'Round Period' for now
        dymensioninfo = Round Period

        # the first one must be always the baseline; the order is important
        values =
            10
            20
            50
            100
            250
            500
            1000
            2500

        # can be 'x', 'y', 'z', 't', 'e'; the order is important
        #  - layer 'x' always corresponds to the XLSX sheets
        #  - layer 'y' always corresponds to the XLSX columns
        axis = y

        # corresponding attribute name of the 'layer'
        layer_attribute = dim2

    Example Usage:
    $> python manage.py createriskanalysis -f WP6__Impact_analysis_results_future_projections_Hospital.ini
    $> python manage.py createriskanalysis -f WP6__Impact_analysis_results_future_projections_Population.ini
    $> python manage.py createriskanalysis -f WP6\ -\ 2050\ Scenarios\ -\ Loss\ Impact\ Results\ -\ Afghanistan\ PML\ Split.ini

    """

    help = 'Creates a new Risk Analysis descriptor: Loss Impact and Impact Analysis Types.'

    option_list = BaseCommand.option_list + (
        make_option(
            '-f',
            '--descriptor-file',
            dest='descriptor_file',
            type="string",
            help='Input Risk Analysis Descriptor INI File.'),)

    def handle(self, **options):
        descriptor_file = options.get('descriptor_file')

        if not descriptor_file or len(descriptor_file) == 0:
            raise CommandError("Input Risk Analysis Descriptor INI File '--descriptor_file' is mandatory")

        Config.read(descriptor_file)
        risk_name = Config.get('DEFAULT', 'name')
        analysis_type_name = Config.get('DEFAULT', 'analysis_type')
        hazard_type_name = Config.get('DEFAULT', 'hazard_type')
        layer_name = Config.get('DEFAULT', 'layer')

        if len(RiskAnalysis.objects.filter(name=risk_name)) > 0:
            raise CommandError("A Risk Analysis with name '"+risk_name+"' already exists on DB!")

        if len(HazardType.objects.filter(mnemonic=hazard_type_name)) == 0:
            raise CommandError("An Hazard Type with mnemonic '"+hazard_type_name+"' does not exist on DB!")

        if len(AnalysisType.objects.filter(name=analysis_type_name)) == 0:
            raise CommandError("An Analysis Type with name '"+analysis_type_name+"' does not exist on DB!")

        if len(Layer.objects.filter(name=layer_name)) == 0:
            raise CommandError("A Layer with name '"+layer_name+"' does not exist on DB!")

        hazard = HazardType.objects.get(mnemonic=hazard_type_name)
        analysis = AnalysisType.objects.get(name=analysis_type_name)
        layer = Layer.objects.get(name=layer_name)

        risk = RiskAnalysis(name=risk_name)
        risk.analysis_type = analysis
        risk.hazard_type = hazard
        risk.save()
        print ("Created Risk Analysis [%s] (%s) - %s" % (risk_name, hazard, analysis))

        for section in Config.sections():
            dimension_values = ConfigSectionMap(section)

            values = list(filter(None, (x.strip() for x in dimension_values['values'].splitlines())))
            for counter, dim_value in enumerate(values):
                rd = RiskAnalysisDymensionInfoAssociation(value=dim_value)
                rd.dymensioninfo = DymensionInfo.objects.get(name=dimension_values['dymensioninfo'])
                rd.riskanalysis = risk
                rd.order = counter
                rd.axis = dimension_values['axis']
                rd.layer = layer
                rd.layer_attribute = dimension_values['layer_attribute']
                rd.save()
                print ("Created Risk Analysis Dymension %s [%s] (%s) - axis %s" % (rd.order, dim_value, rd.dymensioninfo.name, rd.axis))


def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1
