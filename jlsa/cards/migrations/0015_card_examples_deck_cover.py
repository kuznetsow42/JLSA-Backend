# Generated by Django 5.1.4 on 2025-02-08 06:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0014_remove_card_tags_deck_card_deck_delete_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='examples',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='deck',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='decks/'),
        ),
    ]
