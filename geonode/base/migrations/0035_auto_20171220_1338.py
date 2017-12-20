# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0034_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hierarchicalkeyword',
            name='depth',
            field=models.PositiveIntegerField(),
        ),
    ]
