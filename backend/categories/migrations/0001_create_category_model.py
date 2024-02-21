# Generated by Django 5.0.2 on 2024-02-21 15:31

import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
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
                        verbose_name="active_updated_on",
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
                        verbose_name="active_updated_by",
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
            options={"verbose_name_plural": "Categories",},
        ),
    ]
