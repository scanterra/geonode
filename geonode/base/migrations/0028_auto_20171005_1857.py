# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_auto_20170801_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resourcebase',
            name='owner',
            field=models.ForeignKey(related_name='owned_resource', verbose_name='Responsible', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
