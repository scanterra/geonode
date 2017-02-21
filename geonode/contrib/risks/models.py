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

from django.db import models
from django.contrib.gis.db import models as gismodels
from django.db.models import signals
from django.contrib.sites.models import Site
from django.conf import settings

from mptt.models import MPTTModel, TreeForeignKey

from geonode.base.models import ResourceBase
from geonode.base.models import Link
from geonode.layers.models import Layer
from geonode.documents.models import Document

class AnalysisType(models.Model):
    """
    For Risk Data Extraction it can be, as an instance, 'Loss Impact' or 'Impact Analysis'.
    This object should also refer to any additional description and/or related resource
    useful to the users to get details on the Analysis type.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False, db_index=True)
    title = models.CharField(max_length=80, null=False, blank=False)
    description = models.TextField(default='', null=True, blank=False)

    class Meta:
        ordering = ['name']
        db_table = 'risks_analysistype'


class HazardType(models.Model):
    """
    Describes an Hazard related to an Analysis and a Risk and pointing to additional resources on GeoNode.
    e.g.: Earthquake, Flood, Landslide, ...
    """
    id = models.AutoField(primary_key=True)
    mnemonic = models.CharField(max_length=30, null=False, blank=False, db_index=True)
    title = models.CharField(max_length=80, null=False, blank=False)
    order = models.IntegerField()

    class Meta:
        ordering = ['order', 'mnemonic']
        db_table = 'risks_hazardtype'


class RiskAnalysis(models.Model):
    """
    A type of Analysis associated to an Hazard (Earthquake, Flood, ...) and
    an Administrative Division.

    It defines a set of Dymensions (here we have the descriptors), to be used
    to filter SQLViews values on GeoServer.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False, db_index=True)

    # Relationships
    analysis_type = models.ForeignKey(
        AnalysisType,
        related_name='riskanalysis_analysistype',
        on_delete = models.CASCADE,
        blank = False,
        null = False
    )

    hazard_type = models.ForeignKey(
        HazardType,
        related_name='riskanalysis_hazardtype',
        on_delete = models.CASCADE,
        blank = False,
        null = False
    )

    administrative_divisions = models.ManyToManyField(
        "AdministrativeDivision",
        through='RiskAnalysisAdministrativeDivisionAssociation'
    )

    dymension_infos = models.ManyToManyField(
        "DymensionInfo",
        through='RiskAnalysisDymensionInfoAssociation'
    )

    class Meta:
        ordering = ['name']
        db_table = 'risks_riskanalysis'


class AdministrativeDivisionManager(models.Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class AdministrativeDivision(MPTTModel):
    """
    Administrative Division Gaul dataset.
    """
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=30, null=False, unique=True, db_index=True)
    name = models.CharField(max_length=30, null=False, blank=False, db_index=True)
    # GeoDjango-specific: a geometry field (MultiPolygonField)
    # geom = gismodels.MultiPolygonField() - does not work w/ default non-spatial db
    geom = models.TextField()  # As WKT
    srid = models.IntegerField(default=4326)

    # Relationships
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    region = models.ForeignKey('Region')

    risks_analysis = models.ManyToManyField(
        RiskAnalysis,
        through='RiskAnalysisAdministrativeDivisionAssociation'
    )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['code', 'name']
        db_table = 'risks_administrativedivision'
        verbose_name_plural = 'Administrative Divisions'

    class MPTTMeta:
        order_insertion_by = ['name']


class Region(models.Model):
    """
    Groups a set of AdministrativeDivisions
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False, db_index=True)
    # level:
    # 0 is global
    # 1 is continent
    # 2 is sub-continent
    # 3 is country
    level = models.IntegerField(null=False, blank=False, db_index=True)

    # Relationships
    administrative_divisions = models.ManyToManyField(
        AdministrativeDivision,
        related_name='administrative_divisions'
    )

    class Meta:
        ordering = ['name', 'level']
        db_table = 'risks_region'
        verbose_name_plural = 'Regions'



class DymensionInfo(models.Model):
    """
    Set of Dymensions (here we have the descriptors), to be used
    to filter SQLViews values on GeoServer.

    The multi-dimensional vectorial layer in GeoServer will be something like this:

       {riskanalysis, dim1, dim2, ..., dimN, value}

    A set of DymensionInfo is something like:

     {name:'Round Period', value: 'RP-10', order: 0, unit: 'Years', attribute_name: 'dim1'}
     {name:'Round Period', value: 'RP-20', order: 1, unit: 'Years', attribute_name: 'dim1'}
     {name:'Round Period', value: 'RP-50', order: 2, unit: 'Years', attribute_name: 'dim1'}

     {name:'Scenario', value: 'Base', order: 0, unit: 'NA', attribute_name: 'dim2'}
     {name:'Scenario', value: 'Scenario-1', order: 1, unit: 'NA', attribute_name: 'dim2'}
     {name:'Scenario', value: 'Scenraio-2', order: 2, unit: 'NA', attribute_name: 'dim2'}

    Values on GeoServer SQL View will be filtered like:

        {riskanalysis: risk.identifier, dim1: 'RP-10', dim2: 'Base'} -> [values]

    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=False, blank=False, db_index=True)
    abstract = models.CharField(max_length=255)
    unit = models.CharField(max_length=30)

    # Relationships
    risks_analysis = models.ManyToManyField(
        RiskAnalysis,
        through='RiskAnalysisDymensionInfoAssociation'
    )

    class Meta:
        ordering = ['name']
        db_table = 'risks_dymensioninfo'


class RiskAnalysisAdministrativeDivisionAssociation(models.Model):
    """
    Join table between RiskAnalysis and AdministrativeDivision
    """
    id = models.AutoField(primary_key=True)

    # Relationships
    riskanalysis = models.ForeignKey(RiskAnalysis)
    administrativedivision = models.ForeignKey(AdministrativeDivision)

    # TODO : hazardsets

    class Meta:
        db_table = 'risks_riskanalysisadministrativedivisionassociation'


class RiskAnalysisDymensionInfoAssociation(models.Model):
    """
    Join table between RiskAnalysis and DymensionInfo
    """
    id = models.AutoField(primary_key=True)
    order = models.IntegerField()
    value = models.CharField(max_length=80, null=False, blank=False, db_index=True)

    # Relationships
    riskanalysis = models.ForeignKey(RiskAnalysis)
    dymensioninfo = models.ForeignKey(DymensionInfo)

    # GeoServer Layer referenced by GeoNode resource
    layer = models.ForeignKey(
        Layer,
        blank=False,
        null=False,
        unique=False,
        related_name='base_layer')
    layer_attribute = models.CharField(max_length=80, null=False, blank=False)

    class Meta:
        ordering = ['order', 'value']
        db_table = 'risks_riskanalysisdymensioninfoassociation'
