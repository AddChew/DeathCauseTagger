# Generated by Django 3.2.9 on 2022-12-09 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tagger', '0011_auto_20221210_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threshold', models.PositiveSmallIntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_periods', to=settings.AUTH_USER_MODEL)),
                ('icd_above', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='above', to='tagger.newcode')),
                ('icd_below', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='below', to='tagger.newcode')),
                ('icd_equal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equal', to='tagger.newcode')),
                ('icd_input', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='period', to='tagger.newcode')),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modified_periods', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
