# Generated by Django 5.1.4 on 2025-01-01 13:18

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=64)),
                ('definitions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128), size=None)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streak', models.PositiveSmallIntegerField(default=0)),
                ('learned', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('visited', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL)),
                ('dict_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.dictionary')),
            ],
        ),
    ]
