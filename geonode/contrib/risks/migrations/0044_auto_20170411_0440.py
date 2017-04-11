# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0043_auto_20170410_1150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='riskanalysisimportmetadata',
            options={'ordering': ['riskapp', 'region', 'riskanalysis'], 'verbose_name': 'Risks Analysis: Import or Update Risk Metadata from                         XLSX file', 'verbose_name_plural': 'Risks Analysis: Import or Update Risk Metadata                                from XLSX file'},
        ),
        migrations.AddField(
            model_name='riskanalysisimportmetadata',
            name='riskapp',
            field=models.ForeignKey(default=0, to='risks.RiskApp'),
            preserve_default=False,
        ),
    ]
