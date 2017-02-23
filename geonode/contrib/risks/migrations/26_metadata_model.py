# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '24_to_26'),
        ('risks', '26_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisTypeFurtherResourceAssociation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('analysis_type', models.ForeignKey(to='risks.AnalysisType')),
            ],
            options={
                'db_table': 'risks_analysisfurtheresourceassociation',
            },
        ),
        migrations.CreateModel(
            name='FurtherResource',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.TextField()),
                ('resource', models.ForeignKey(related_name='resource', to='base.ResourceBase')),
            ],
            options={
                'db_table': 'risks_further_resource',
            },
        ),
        migrations.CreateModel(
            name='HazardSet',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=20)),
                ('date_type', models.CharField(max_length=20)),
                ('edition', models.CharField(max_length=30)),
                ('abstract', models.TextField()),
                ('purpose', models.TextField()),
                ('keyword', models.TextField()),
                ('use_contraints', models.CharField(max_length=255)),
                ('other_constraints', models.CharField(max_length=255)),
                ('spatial_representation_type', models.CharField(max_length=150)),
                ('language', models.CharField(max_length=80)),
                ('begin_date', models.CharField(max_length=20)),
                ('end_date', models.CharField(max_length=20)),
                ('bounds', models.CharField(max_length=150)),
                ('supplemental_information', models.CharField(max_length=255)),
                ('online_resource', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('reference_system_code', models.CharField(max_length=30)),
                ('data_quality_statement', models.TextField()),
            ],
            options={
                'db_table': 'risks_hazardset',
            },
        ),
        migrations.CreateModel(
            name='PointOfContact',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('individual_name', models.CharField(max_length=255)),
                ('organization_name', models.CharField(max_length=255)),
                ('position_name', models.CharField(max_length=255)),
                ('voice', models.CharField(max_length=255)),
                ('facsimile', models.CharField(max_length=30)),
                ('delivery_point', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=80)),
                ('postal_code', models.CharField(max_length=30)),
                ('e_mail', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('update_frequency', models.TextField()),
                ('administrative_area', models.ForeignKey(to='risks.AdministrativeDivision')),
                ('country', models.ForeignKey(to='risks.Region')),
            ],
            options={
                'db_table': 'risks_pointofcontact',
            },
        ),
        migrations.AlterModelOptions(
            name='hazardtype',
            options={'ordering': ['order', 'mnemonic'], 'verbose_name_plural': 'Hazards'},
        ),
        migrations.AddField(
            model_name='hazardtype',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='hazardtype',
            name='fa_class',
            field=models.CharField(default=b'fa-times', max_length=64),
        ),
        migrations.AddField(
            model_name='hazardtype',
            name='gn_description',
            field=models.TextField(default=b'', null=True, verbose_name=b'GeoNode description'),
        ),
        migrations.AddField(
            model_name='hazardset',
            name='author',
            field=models.ForeignKey(related_name='metadata_author', to='risks.PointOfContact'),
        ),
        migrations.AddField(
            model_name='hazardset',
            name='country',
            field=models.ForeignKey(to='risks.Region'),
        ),
        migrations.AddField(
            model_name='hazardset',
            name='poc',
            field=models.ForeignKey(related_name='point_of_contact', to='risks.PointOfContact'),
        ),
        migrations.AddField(
            model_name='hazardset',
            name='topic_category',
            field=models.ForeignKey(related_name='category', blank=True, to='base.TopicCategory', null=True),
        ),
        migrations.AddField(
            model_name='analysistypefurtherresourceassociation',
            name='hazard_type',
            field=models.ForeignKey(to='risks.HazardType'),
        ),
        migrations.AddField(
            model_name='analysistypefurtherresourceassociation',
            name='region',
            field=models.ForeignKey(to='risks.Region'),
        ),
        migrations.AddField(
            model_name='analysistypefurtherresourceassociation',
            name='resource',
            field=models.ForeignKey(related_name='further_resource', to='risks.FurtherResource'),
        ),
        migrations.AddField(
            model_name='hazardset',
            name='riskanalysis',
            field=models.ForeignKey(related_name='riskanalysis', default=None, to='risks.RiskAnalysis'),
            preserve_default=False,
        ),
    ]
