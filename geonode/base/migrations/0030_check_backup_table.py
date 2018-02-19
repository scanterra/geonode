# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection, migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_auto_20171114_0341'),
    ]

    db_cursor = connection.cursor()
    check_exists_query = "SELECT relname FROM pg_class WHERE relname=%s;"
    # base_query = "DROP TABLE {table};"
    base_query = "DROP TABLE {table} CASCADE;"
    tables = ['base_backup']
    existing_tables = []

    for table in tables:
        db_cursor.execute(check_exists_query, [table])
        result = db_cursor.fetchone()
        if result:
            existing_tables.append(table)
    print("DROP TABLEs {tables}".format(tables=existing_tables))

    operations = [
        migrations.RunSQL([base_query.format(table=existing_table) for existing_table in existing_tables]),
        migrations.CreateModel(
            name='Backup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=255, editable=False)),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('description_en', models.TextField(null=True, blank=True)),
                ('base_folder', models.CharField(max_length=100)),
                ('location', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ('date',),
                'verbose_name_plural': 'Backups',
            },
        )
    ]

