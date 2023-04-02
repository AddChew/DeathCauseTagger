# Generated by Django 3.2.9 on 2022-12-29 16:53

import tagger.models
import model_utils.fields
import authentication.models
import django.utils.timezone
import django.db.models.deletion
import django.contrib.postgres.indexes
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
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=50, unique=True)),
                ('created_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_statuses', to=settings.AUTH_USER_MODEL)),
                ('updated_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='modified_statuses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Statuses',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=200, unique=True)),
                ('created_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_categories', to=settings.AUTH_USER_MODEL)),
                ('updated_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='modified_categories', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(default=tagger.models.Status.get_default_status, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='tagger.status')),
                ('status_updated_on', model_utils.fields.MonitorField(default=django.utils.timezone.now, editable=False, monitor='status')),
                ('status_updated_by', models.ForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='status_updated_categories', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=4, unique=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='codes', to='tagger.category')),
                ('created_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_codes', to=settings.AUTH_USER_MODEL)),
                ('updated_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='modified_codes', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(default=tagger.models.Status.get_default_status, on_delete=django.db.models.deletion.CASCADE, related_name='codes', to='tagger.status')),
                ('status_updated_on', model_utils.fields.MonitorField(default=django.utils.timezone.now, editable=False, monitor='status')),
                ('status_updated_by', models.ForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='status_updated_codes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DeathCause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=200, unique=True)),
                ('created_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_deathcauses', to=settings.AUTH_USER_MODEL)),
                ('updated_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='modified_deathcauses', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(default=tagger.models.Status.get_default_status, on_delete=django.db.models.deletion.CASCADE, related_name='causes', to='tagger.status')),
                ('status_updated_on', model_utils.fields.MonitorField(default=django.utils.timezone.now, editable=False, monitor='status')),
                ('status_updated_by', models.ForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='status_updated_causes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Death Causes',
            },
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('threshold', models.PositiveSmallIntegerField()),
                ('created_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_periods', to=settings.AUTH_USER_MODEL)),
                ('icd_above', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='above', to='tagger.code')),
                ('icd_below', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='below', to='tagger.code')),
                ('icd_equal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equal', to='tagger.code')),
                ('icd_input', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='period', to='tagger.code')),
                ('updated_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='modified_periods', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(default=tagger.models.Status.get_default_status, on_delete=django.db.models.deletion.CASCADE, related_name='periods', to='tagger.status')),
                ('status_updated_on', model_utils.fields.MonitorField(default=django.utils.timezone.now, editable=False, monitor='status')),
                ('status_updated_by', models.ForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='status_updated_periods', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_option', models.BooleanField(default=False)),
                ('is_option_updated_on', model_utils.fields.MonitorField(default=django.utils.timezone.now, editable=False, monitor='is_option')),
                ('status_updated_on', model_utils.fields.MonitorField(default=django.utils.timezone.now, editable=False, monitor='status')),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='tagger.code')),
                ('created_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='created_mappings', to=settings.AUTH_USER_MODEL)),
                ('description', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='tagger.deathcause')),
                ('is_option_updated_by', models.ForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='is_option_updated_mappings', to=settings.AUTH_USER_MODEL)),
                ('status', models.ForeignKey(default=tagger.models.Status.get_default_status, on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='tagger.status')),
                ('status_updated_by', models.ForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='status_updated_mappings', to=settings.AUTH_USER_MODEL)),
                ('updated_by', tagger.models.CustomForeignKey(default=authentication.models.User.get_default_user, editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='modified_mappings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddIndex(
            model_name='deathcause',
            index=django.contrib.postgres.indexes.GinIndex(fields=['description'], name='tagger_deathcause_desc_gin_idx', opclasses=['gin_trgm_ops']),
        ),
    ]