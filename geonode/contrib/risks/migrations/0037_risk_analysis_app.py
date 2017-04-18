# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from geonode.contrib.risks import models as risks_models


class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0036_costbenefit_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='riskanalysis',
            name='app',
            field=models.ForeignKey(default=risks_models.get_risk_app_default, to='risks.RiskApp'),
            preserve_default=False,
        ),
    ]
