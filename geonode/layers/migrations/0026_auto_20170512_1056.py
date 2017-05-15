# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('layers', '0025_auto_20170509_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='layer',
            options={'permissions': (('change_layer_data', 'Can edit layer data'), ('change_layer_style', 'Can change layer style'))},
        ),
    ]
