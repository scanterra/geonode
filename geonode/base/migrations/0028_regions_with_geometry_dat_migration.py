# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from itertools import chain
from django.db import migrations, models
from django.contrib.gis import geos

from geonode.utils import bbox_to_wkt


def migrate_regions(apps, schema_editor):
    Region = apps.get_model('base', 'Region')
    ResourceBase = apps.get_model('base', 'ResourceBase')

    
    def get_envelope_from_bbox(inst):
        wkt = geographic_bounding_box(inst)
        return geos.GEOSGeometry(wkt)

    def geographic_bounding_box(inst):
        return bbox_to_wkt(inst.bbox_x0, inst.bbox_x1, inst.bbox_y0, inst.bbox_y1, srid=inst.srid)

    for r in chain(Region.objects.all(), ResourceBase.objects.all()):
        r.envelope = get_envelope_from_bbox(r)
        r.save()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_regions_with_geometry'),
    ]
    operations = [
        migrations.RunPython(migrate_regions, reverse_code=migrations.RunPython.noop)
    ]
