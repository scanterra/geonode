# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0027_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='recommendation',
            field=models.CharField(default=b'', max_length=50, null=True, help_text='Name of the person who recommended you IHP-WINS', blank=True),
        ),
    ]
