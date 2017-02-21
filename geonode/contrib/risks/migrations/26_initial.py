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
            name='HazardType',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('mnemonic', models.CharField(max_length=30, db_index=True)),
                ('title', models.CharField(max_length=80)),
                ('order', models.IntegerField()),
            ],
            options={
                'ordering': ['order', 'mnemonic'],
                'db_table': 'risks_hazardtype',
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
            model_name='dymensioninfo',
            name='risks_analysis',
            field=models.ManyToManyField(to='risks.RiskAnalysis', through='risks.RiskAnalysisDymensionInfoAssociation'),
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
