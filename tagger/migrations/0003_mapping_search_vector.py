# Generated by Django 3.2.9 on 2022-12-06 15:18

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tagger', '0002_annotation_category_icd_mapping_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='mapping',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]