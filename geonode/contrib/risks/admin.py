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

from django.contrib import admin

from geonode.base.admin import MediaTranslationAdmin
from geonode.contrib.risks.models import RiskAnalysis
from geonode.contrib.risks.models import Region, AdministrativeDivision
from geonode.contrib.risks.models import AnalysisType, HazardType, DymensionInfo
from geonode.contrib.risks.models import PointOfContact, HazardSet
from geonode.contrib.risks.models import FurtherResource, AnalysisTypeFurtherResourceAssociation


class DymensionInfoInline(admin.TabularInline):
    model = DymensionInfo.risks_analysis.through
    extra = 3


class AdministrativeDivisionInline(admin.StackedInline):
    model = AdministrativeDivision.risks_analysis.through
    exclude = ['geom', 'srid']
    extra = 3


class FurtherResourceInline(admin.TabularInline):
    model = AnalysisTypeFurtherResourceAssociation
    extra = 3


class FurtherResourceAdmin(admin.ModelAdmin):
    model = FurtherResource
    list_display_links = ('resource',)
    list_display = ('resource',)
    group_fieldsets = True


class RegionAdmin(admin.ModelAdmin):
    model = Region
    list_display_links = ('name',)
    list_display = ('name', 'level')
    search_fields = ('name',)
    readonly_fields = ('administrative_divisions',)
    inlines = [FurtherResourceInline]
    group_fieldsets = True


class AdministrativeDivisionAdmin(admin.ModelAdmin):
    model = AdministrativeDivision
    list_display_links = ('name',)
    list_display = ('code', 'name', 'parent')
    search_fields = ('code', 'name',)
    readonly_fields = ('risks_analysis',)
    # inlines = [AdministrativeDivisionInline]
    group_fieldsets = True


class AnalysisTypeAdmin(admin.ModelAdmin):
    model = AnalysisType
    list_display_links = ('name',)
    list_display = ('name', 'title', 'description',)
    search_fields = ('name', 'title',)
    inlines = [FurtherResourceInline]
    group_fieldsets = True


class HazardTypeAdmin(admin.ModelAdmin):
    model = HazardType
    list_display_links = ('mnemonic',)
    list_display = ('mnemonic', 'gn_description', 'title',)
    search_fields = ('mnemonic', 'gn_description', 'title',)
    inlines = [FurtherResourceInline]
    group_fieldsets = True


class DymensionInfoAdmin(admin.ModelAdmin):
    model = DymensionInfo
    list_display_links = ('name',)
    list_display = ('name', 'unit', 'abstract',)
    search_fields = ('name',)
    filter_vertical = ('risks_analysis',)
    inlines = [DymensionInfoInline]
    group_fieldsets = True


class RiskAnalysisAdmin(admin.ModelAdmin):
    model = RiskAnalysis
    list_display_links = ('name',)
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('administrative_divisions',)
    # inlines = [AdministrativeDivisionInline, DymensionInfoInline]
    inlines = [DymensionInfoInline]
    group_fieldsets = True

    def has_add_permission(self, request):
        return False


class PointOfContactAdmin(admin.ModelAdmin):
    model = PointOfContact
    list_display_links = ('individual_name', 'organization_name',)
    list_display = ('individual_name', 'organization_name',)
    search_fields = ('individual_name', 'organization_name',)
    group_fieldsets = True


class HazardSetAdmin(admin.ModelAdmin):
    model = HazardSet
    list_display_links = ('title',)
    list_display = ('title',)
    search_fields = ('title', 'riskanalysis', 'country',)
    group_fieldsets = True

    def has_add_permission(self, request):
        return False


admin.site.register(Region, RegionAdmin)
admin.site.register(AdministrativeDivision, AdministrativeDivisionAdmin)
admin.site.register(AnalysisType, AnalysisTypeAdmin)
admin.site.register(HazardType, HazardTypeAdmin)
admin.site.register(DymensionInfo, DymensionInfoAdmin)
admin.site.register(RiskAnalysis, RiskAnalysisAdmin)
admin.site.register(PointOfContact, PointOfContactAdmin)
admin.site.register(HazardSet, HazardSetAdmin)
admin.site.register(FurtherResource, FurtherResourceAdmin)
