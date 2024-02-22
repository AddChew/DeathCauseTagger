# Generated by Django 5.0.2 on 2024-02-22 14:31

import json

from django.conf import settings
from django.db import migrations


def create_death_causes(apps, schema_editor):
    app = "deathcauses"
    DeathCause = apps.get_model(app, "DeathCause")

    with open(settings.FIXTURES[app], "r") as f:
        descriptions = json.load(f)

    DeathCause.objects.bulk_create([
        DeathCause(description = desc) for desc in descriptions 
    ])


class Migration(migrations.Migration):

    dependencies = [
        ("deathcauses", "0001_create_death_cause_model"),
    ]

    operations = [
        migrations.RunPython(create_death_causes)
    ]