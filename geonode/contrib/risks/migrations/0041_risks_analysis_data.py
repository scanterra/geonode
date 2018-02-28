# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from geonode.contrib.risks import models as risks_models

class Migration(migrations.Migration):

    dependencies = [
        ('risks', '0040_risk_analysis_layer'),
    ]

    operations = [
        migrations.RunPython(risks_models.migrate_layers, risks_models.unmigrate_layers),
    ]
