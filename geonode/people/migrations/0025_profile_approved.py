# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '24_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='approved',
            field=models.BooleanField(default=False, help_text='approve user', verbose_name='Is the user approved?'),
        ),
    ]
