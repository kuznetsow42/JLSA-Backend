# Generated by Django 5.1.4 on 2025-01-04 12:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_alter_dictentry_options_dictentry_reading_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictentry',
            name='definitions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None),
        ),
        migrations.AlterField(
            model_name='dictentry',
            name='reading',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='dictentry',
            name='word',
            field=models.CharField(max_length=128),
        ),
    ]
