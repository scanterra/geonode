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

import xlrd
from xlrd.sheet import ctype_text


class Command(BaseCommand):
    """
    For each Scenario / Round Period, check the Administrative Unit
    and store the value on the db:

    e.g.:

      Feature ==> Layer {dim1: "Hospital", dim2: "10", adm_code: "AF", value: 30000000}
      Feature ==> Layer {dim1: "Hospital", dim2: "10", adm_code: "AF15", value: 3000000}
      Feature ==> Layer {dim1: "SSP2", dim2: "250", adm_code: "AF29", value: 44340000}

    Example Usage:
    $> python manage.py importriskdata -r Afghanistan -k "WP6_future_proj_Hospital" -x WP6__Impact_analysis_results_future_projections_Hospital.xlsx
    $> python manage.py importriskdata -r Afghanistan -k "WP6_future_proj_Population" -x WP6__Impact_analysis_results_future_projections_Population.xlsx
    $> python manage.py importriskdata -r Afghanistan -k "WP6_loss_Afg_PML_split" -x WP6\ -\ 2050\ Scenarios\ -\ Loss\ Impact\ Results\ -\ Afghanistan\ PML\ Split.xlsx

    To import Metadata also, specify the Risk Metadada File wih the 'm' option

    $> python manage.py importriskdata -r Afghanistan -k "WP6_future_proj_Population"
                    -x WP6__Impact_analysis_results_future_projections_Population.xlsx -m WP6_Impact_analysis_results_future_projections_Population\ -\ metadata.xlsx

    The procedure requires a layer on GeoServer based on the following table definition:

        CREATE SEQUENCE public.{layer_name}_fid_seq
          INCREMENT 1
          MINVALUE 1
          MAXVALUE 9223372036854775807
          START 1
          CACHE 1;
        ALTER TABLE public.{layer_name}_fid_seq
          OWNER TO geonode;

        CREATE TABLE public.{layer_name}
        (
          fid integer NOT NULL DEFAULT nextval('{layer_name}_fid_seq'::regclass),
          the_geom geometry(MultiPolygon,4326),
          dim1 character varying(80),
          dim2 character varying(80),
          dim3 character varying(80),
          dim4 character varying(80),
          dim5 character varying(80),
          risk_analysis character varying(80),
          hazard_type character varying(30),
          admin character varying(150),
          adm_code character varying(30),
          region character varying(80),
          value character varying(255),
          CONSTRAINT {layer_name}_pkey PRIMARY KEY (fid)
        )
        WITH (
          OIDS=FALSE
        );
        ALTER TABLE public.{layer_name}
          OWNER TO geonode;

        CREATE INDEX spatial_{layer_name}_the_geom
          ON public.{layer_name}
          USING gist
          (the_geom);

    """

    help = 'Import Risk Data: Loss Impact and Impact Analysis Types.'

    option_list = BaseCommand.option_list + (
        make_option(
            '-c',
            '--commit',
            action='store_true',
            dest='commit',
            default=True,
            help='Commits Changes to the storage.'),
        make_option(
            '-r',
            '--region',
            dest='region',
            type="string",
            help='Destination Region.'),
        make_option(
            '-x',
            '--excel-file',
            dest='excel_file',
            type="string",
            help='Input Risk Data Table as XLSX File.'),
        make_option(
            '-m',
            '--excel-metadata-file',
            dest='excel_metadata_file',
            type="string",
            help='Input Risk Metadata Table as XLSX File.'),
        make_option(
            '-k',
            '--risk-analysis',
            dest='risk_analysis',
            type="string",
            help='Name of the Risk Analysis associated to the File.'))

    def handle(self, **options):
        commit = options.get('commit')
        region = options.get('region')
        excel_file = options.get('excel_file')
        risk_analysis = options.get('risk_analysis')
        excel_metadata_file = options.get('excel_metadata_file')

        if region is None:
            raise CommandError("Input Destination Region '--region' is mandatory")

        if risk_analysis is None:
            raise CommandError("Input Risk Analysis associated to the File '--risk_analysis' is mandatory")

        if not excel_file or len(excel_file) == 0:
            raise CommandError("Input Risk Data Table '--excel_file' is mandatory")

        wb = xlrd.open_workbook(filename=excel_file)
        risk = RiskAnalysis.objects.get(name=risk_analysis)
        region = Region.objects.get(name=region)
        region_code = region.administrative_divisions.filter(parent=None)[0].code

        scenarios = RiskAnalysisDymensionInfoAssociation.objects.filter(riskanalysis=risk, axis='x')
        round_periods = RiskAnalysisDymensionInfoAssociation.objects.filter(riskanalysis=risk, axis='y')

        for scenario in scenarios:
            # Dump Vectorial Data from DB
            datastore = settings.OGC_SERVER['default']['DATASTORE']
            if (datastore):
                ogc_db_name = settings.DATABASES[datastore]['NAME']
                ogc_db_user = settings.DATABASES[datastore]['USER']
                ogc_db_passwd = settings.DATABASES[datastore]['PASSWORD']
                ogc_db_host = settings.DATABASES[datastore]['HOST']
                ogc_db_port = settings.DATABASES[datastore]['PORT']

            sheet = wb.sheet_by_name(scenario.value)
            row_headers = sheet.row(0)
            for rp in round_periods:
                col_num = -1
                for idx, cell_obj in enumerate(row_headers):
                    # cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
                    # print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))
                    try:
                        if int(cell_obj.value) == int(rp.value):
                            # print('[%s] (%s) RP-%s' % (scenario.value, idx, rp.value))
                            col_num = idx
                            break
                    except:
                        pass
                if col_num > 0:
                    conn = self.get_db_conn(ogc_db_name, ogc_db_user, ogc_db_port, ogc_db_host, ogc_db_passwd)
                    try:
                        for row_num in range(1, sheet.nrows):
                            cell_obj = sheet.cell(row_num, 5)
                            cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
                            if cell_obj.value:
                                adm_code = cell_obj.value if cell_type_str == 'text' else region_code + '{:04d}'.format(int(cell_obj.value))
                                adm_div = AdministrativeDivision.objects.get(code=adm_code)
                                value = sheet.cell_value(row_num, col_num)
                                print('[%s] (RP-%s) %s / %s' % (scenario.value, rp.value, adm_div.name, value))

                                table_name = rp.layer.typename.split(":")[1] if ":" in rp.layer.typename else rp.layer.typename
                                db_values = {
                                    'table': table_name, # From rp.layer
                                    'the_geom': geos.fromstr(adm_div.geom, srid=adm_div.srid),
                                    'dim1': scenario.value,
                                    'dim2': rp.value,
                                    'dim3': None,
                                    'dim4': None,
                                    'dim5': None,
                                    'risk_analysis': risk_analysis,
                                    'hazard_type': risk.hazard_type.mnemonic,
                                    'admin': adm_div.name,
                                    'adm_code': adm_code,
                                    'region': region.name,
                                    'value': value
                                }
                                self.insert_db(conn, db_values)
                                risk_adm = RiskAnalysisAdministrativeDivisionAssociation.objects.filter(riskanalysis=risk, administrativedivision=adm_div)
                                if len(risk_adm) == 0:
                                    RiskAnalysisAdministrativeDivisionAssociation.objects.create(riskanalysis=risk, administrativedivision=adm_div)
                        conn.commit()
                    except Exception:
                        try:
                            conn.rollback()
                        except:
                            pass

                        traceback.print_exc()
                    finally:
                        conn.close()

        # Import or Update Metadata if Metadata File has been specified/found
        if excel_metadata_file:
            call_command('importriskmetadata', region=region.name, excel_file=excel_metadata_file, risk_analysis=risk_analysis)
            risk.metadata_file = excel_metadata_file

        # Finalize
        risk.data_file = excel_file
        if commit:
            risk.save()

        return risk_analysis


    def get_db_conn(self, db_name, db_user, db_port, db_host, db_passwd):
        """Get db conn (GeoNode)"""
        db_host = db_host if db_host is not None else 'localhost'
        db_port = db_port if db_port is not None else 5432
        conn = psycopg2.connect(
            "dbname='%s' user='%s' port='%s' host='%s' password='%s'" % (db_name, db_user, db_port, db_host, db_passwd)
        )
        return conn


    def insert_db(self, conn, values):
        """Remove spurious records from GeoNode DB"""
        curs = conn.cursor()

        insert_template = """INSERT INTO {table}(
                          the_geom,
                              dim1, dim2, dim3, dim4, dim5,
                              risk_analysis, hazard_type,
                              admin, adm_code,
                              region, value)
                          VALUES ('{the_geom}',
                              '{dim1}', '{dim2}', '{dim3}', '{dim4}', '{dim5}',
                              '{risk_analysis}', '{hazard_type}',
                              '{admin}', '{adm_code}',
                              '{region}', '{value}');"""

        curs.execute(insert_template.format(**values))
