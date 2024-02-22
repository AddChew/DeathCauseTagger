# Generated by Django 5.0.2 on 2024-02-22 14:26

import django.contrib.postgres.indexes
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import users.models
import uuid
from django.conf import settings
from django.db import migrations, models
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        TrigramExtension(),
        migrations.CreateModel(
            name="DeathCause",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True, verbose_name="active")),
                (
                    "is_active_updated_on",
                    model_utils.fields.MonitorField(
                        default=django.utils.timezone.now,
                        editable=False,
                        monitor="is_active",
                        verbose_name="active updated on",
                    ),
                ),
                ("description", models.CharField(max_length=200, unique=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=users.models.User.get_default_user,
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "is_active_updated_by",
                    models.ForeignKey(
                        default=users.models.User.get_default_user,
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="is_active_updated_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="active updated by",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        default=users.models.User.get_default_user,
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modified_%(class)ss",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Death Causes",
                "indexes": [
                    django.contrib.postgres.indexes.GinIndex(
                        fields=["description"],
                        name="death_cause_desc_gin_idx",
                        opclasses=["gin_trgm_ops"],
                    )
                ],
            },
        ),
    ]