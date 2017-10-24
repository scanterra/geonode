# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcebase',
            name='doi',
            field=models.TextField(help_text='a DOI will be added by Admin before publication.', null=True, verbose_name='DOI', blank=True),
        ),
    ]
