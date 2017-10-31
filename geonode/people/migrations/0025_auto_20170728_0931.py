# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '24_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.CharField(choices=[(b'', 'No role'), (b'event-operator', 'Event Operator'), (b'impact-assessor', 'Impact Assessor'), (b'emergency-manager', 'Emergency Manager')], max_length=255, blank=True, help_text='role or position of the responsible person', null=True, verbose_name='Position Name'),
        ),
    ]
