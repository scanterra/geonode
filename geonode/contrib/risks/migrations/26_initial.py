from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '__first__'),
        ('layers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrativeDivision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=30, db_index=True)),
                ('name', models.CharField(max_length=30, db_index=True)),
                ('geom', models.TextField()),
                ('srid', models.IntegerField(default=4326)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='risks.AdministrativeDivision', null=True)),
            ],
            options={
                'ordering': ['code', 'name'],
                'db_table': 'risks_administrativedivision',
                'verbose_name_plural': 'Administrative Divisions',
            },
        ),
        migrations.CreateModel(
            name='AnalysisType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, db_index=True)),
                ('title', models.CharField(max_length=80)),
                ('description', models.TextField(default=b'', null=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'risks_analysistype',
            },
        ),
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
            name='DymensionInfo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, db_index=True)),
                ('abstract', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'risks_dymensioninfo',
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
            name='HazardType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('mnemonic', models.CharField(max_length=30, db_index=True)),
                ('title', models.CharField(max_length=80)),
                ('order', models.IntegerField()),
                ('description', models.TextField(default=b'')),
                ('gn_description', models.TextField(default=b'', null=True, verbose_name=b'GeoNode description')),
                ('fa_class', models.CharField(default=b'fa-times', max_length=64)),
            ],
            options={
                'ordering': ['order', 'mnemonic'],
                'db_table': 'risks_hazardtype',
                'verbose_name_plural': 'Hazards',
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
                ('administrative_area', models.ForeignKey(blank=True, to='risks.AdministrativeDivision', null=True)),
            ],
            options={
                'db_table': 'risks_pointofcontact',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, db_index=True)),
                ('level', models.IntegerField(db_index=True)),
                ('administrative_divisions', models.ManyToManyField(related_name='administrative_divisions', to='risks.AdministrativeDivision')),
            ],
            options={
                'ordering': ['name', 'level'],
                'db_table': 'risks_region',
                'verbose_name_plural': 'Regions',
            },
        ),
        migrations.CreateModel(
            name='RiskAnalysis',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, db_index=True)),
            ],
            options={
                'ordering': ['name'],
                'db_table': 'risks_riskanalysis',
                'verbose_name_plural': 'Risks Analysis',
            },
        ),
        migrations.CreateModel(
            name='RiskAnalysisAdministrativeDivisionAssociation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('administrativedivision', models.ForeignKey(to='risks.AdministrativeDivision')),
                ('riskanalysis', models.ForeignKey(to='risks.RiskAnalysis')),
            ],
            options={
                'db_table': 'risks_riskanalysisadministrativedivisionassociation',
            },
        ),
        migrations.CreateModel(
            name='RiskAnalysisDymensionInfoAssociation',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('order', models.IntegerField()),
                ('value', models.CharField(max_length=80, db_index=True)),
                ('axis', models.CharField(max_length=10, db_index=True)),
                ('layer_attribute', models.CharField(max_length=80)),
                ('dymensioninfo', models.ForeignKey(to='risks.DymensionInfo')),
                ('layer', models.ForeignKey(related_name='base_layer', to='layers.Layer')),
                ('riskanalysis', models.ForeignKey(to='risks.RiskAnalysis')),
            ],
            options={
                'ordering': ['order', 'value'],
                'db_table': 'risks_riskanalysisdymensioninfoassociation',
            },
        ),
        migrations.AddField(
            model_name='riskanalysis',
            name='administrative_divisions',
            field=models.ManyToManyField(to='risks.AdministrativeDivision', through='risks.RiskAnalysisAdministrativeDivisionAssociation'),
        ),
        migrations.AddField(
            model_name='riskanalysis',
            name='analysis_type',
            field=models.ForeignKey(related_name='riskanalysis_analysistype', to='risks.AnalysisType'),
        ),
        migrations.AddField(
            model_name='riskanalysis',
            name='dymension_infos',
            field=models.ManyToManyField(to='risks.DymensionInfo', through='risks.RiskAnalysisDymensionInfoAssociation'),
        ),
        migrations.AddField(
            model_name='riskanalysis',
            name='hazard_type',
            field=models.ForeignKey(related_name='riskanalysis_hazardtype', to='risks.HazardType'),
        ),
        migrations.AddField(
            model_name='riskanalysis',
            name='hazardset',
            field=models.ForeignKey(related_name='hazardset', blank=True, to='risks.HazardSet', null=True),
        ),
        migrations.AddField(
            model_name='pointofcontact',
            name='country',
            field=models.ForeignKey(blank=True, to='risks.Region', null=True),
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
            name='riskanalysis',
            field=models.ForeignKey(related_name='riskanalysis', to='risks.RiskAnalysis'),
        ),
        migrations.AddField(
            model_name='hazardset',
            name='topic_category',
            field=models.ForeignKey(related_name='category', blank=True, to='base.TopicCategory', null=True),
        ),
        migrations.AddField(
            model_name='dymensioninfo',
            name='risks_analysis',
            field=models.ManyToManyField(to='risks.RiskAnalysis', through='risks.RiskAnalysisDymensionInfoAssociation'),
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
            model_name='administrativedivision',
            name='region',
            field=models.ForeignKey(to='risks.Region'),
        ),
        migrations.AddField(
            model_name='administrativedivision',
            name='risks_analysis',
            field=models.ManyToManyField(to='risks.RiskAnalysis', through='risks.RiskAnalysisAdministrativeDivisionAssociation'),
        ),
    ]
