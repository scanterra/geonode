# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2016 OSGeo
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

from django.test import TestCase
from geonode.base.models import ResourceBase, Region


class ThumbnailTests(TestCase):

    def setUp(self):
        self.rb = ResourceBase.objects.create()

    def test_initial_behavior(self):
        self.assertFalse(self.rb.has_thumbnail())
        missing = self.rb.get_thumbnail_url()
        self.assertEquals('/static/geonode/img/missing_thumb.png', missing)



class RegionTests(TestCase):
    
    fixtures = ['regions.json']

    def test_envelope(self):
        codes = ('GLO', 'PAC', 'EUR', 'ITA',)
        it = Region.objects.get(code='ITA')
        center = it.envelope.centroid
        code_check = tuple(Region.objects
                                 .filter(envelope__intersects=center)
                                 .order_by('level')
                                 .values_list('code', flat=True))
        self.assertEqual(codes, code_check)
