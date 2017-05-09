# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '24_to_26'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='layer',
            options={'ordering': ['title'], 'permissions': (('change_layer_data', 'Can edit layer data'), ('change_layer_style', 'Can change layer style'))},
        ),
        migrations.AlterModelOptions(
            name='style',
            options={'ordering': ['sld_title', 'name']},
        ),
    ]
